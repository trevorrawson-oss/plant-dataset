#!/usr/bin/env python3
"""Run the WHOLE tools/ test tree, and refuse a green that inspected nothing.

WHY THIS EXISTS. `pytest tools/` cannot see the whole suite. 72 of the 247
`tools/test_*.py` entry points are SCRIPT-STYLE -- module-level asserts with no
`def test_` -- so pytest reports `no tests ran` and exits **5** whether they
passed or were never reached, and they contribute ZERO to the tree's "N passed".
A reader of that summary cannot tell a suite that ran and was clean from one
that never ran at all. CLAUDE.md, 2026-09-22: **a check that cannot distinguish
"inspected and clean" from "inspected nothing" is not a check.**

WHAT THIS ENFORCES, the rule the mutation convention already states for promote
suites, applied to the test tree:

  * **rc 5 is BROKEN, not green.** Any pytest entry point that collects nothing
    fails this runner.
  * **Per-FILE collection.** A whole-tree pytest run returning 0 hides a single
    file that silently yields no tests, because the aggregate is not 5. Every
    collectable file must yield at least one test, checked by name.
  * **Script-style files are RUN, as scripts**, `python3 tools/<name>.py` from
    the repo root, and must exit 0.
  * **This runner obeys its own rule.** It reports both populations and REFUSES
    when either is empty, so a discovery bug cannot present as a clean tree.

A script-style test signals failure by RAISING, never by `sys.exit`: a bare
module-level `sys.exit(1)` surfaces under pytest as `INTERNALERROR`, which reads
as a broken harness rather than a real failure.

Run:  python3 tools/run_test_tree.py            # the whole tree
      python3 tools/run_test_tree.py --classify # populations only, runs nothing
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# A file is pytest-collectable if it declares tests the collector can find.
COLLECTABLE = re.compile(r"^\s*def test_|^\s*class Test|unittest\.TestCase", re.M)
# Floors: the runner refuses if discovery returns fewer than this. Measured
# 2026-09-22 at 174 collectable / 72 script-style. These are FLOORS, not pins --
# adding entry points is fine, losing them silently is the defect.
MIN_COLLECTABLE = 150
MIN_SCRIPT = 60

# ---------------------------------------------------------------- WAIVERS
# A CHECK THAT IS ALWAYS RED IS AS USELESS AS ONE THAT IS ALWAYS GREEN, and both
# are closed the same way: waive the EXACT known cases and fail on everything else
# (Trevor, 2026-09-22). This tree has carried the same two failures through four
# landed promotes, each landing asserting in prose that they were pre-existing --
# a convention doing a gate's job, the third instance of that pattern after E1's
# `--no-verify` bypass and plant-astro's 26-error baseline.
#
# A waiver is keyed on test id AND FAILURE CHARACTER. A third failure fails. Either
# of these two failing DIFFERENTLY fails, because "still red" is not the same fact
# as "red for the reason we accepted".
WAIVERS = {
    "tools/test_bare_host_scan.py::test_self_pathed_population_at_this_canonical": {
        "ticket": "PLA-544",
        "reason": "the pinned self-pathed population is stale; RED since 2026-09-04 and rode "
                  "through four landed promotes without being re-measured",
        # Measured 2026-09-22: expected (315, 155), actual (321, 161). Moving off
        # 321/161 in EITHER direction breaks the waiver and fails the tree.
        "character": re.compile(r"CITATIONS/SOLE moved: 321/161\b"),
    },
    "tools/test_cited_claim_scan.py::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass": {
        "ticket": "PLA-161",
        "reason": "8 of 28 cited URLs are uncached, so absence is UNDETERMINED rather than "
                  "proven; the guard is correctly REFUSING, not wrong",
        # If UNDETERMINED ever becomes a real absence, or the uncached count moves,
        # the character no longer matches and the tree fails.
        "character": re.compile(
            r"UnreportableAbsence: \d+ of 28 cited URLs are uncached and therefore "
            r"UNDETERMINED, not absent"),
    },
}

# A script-style file may legitimately SKIP (its staged inputs are gone). It says so
# by printing a line beginning SKIP and exiting 0. Exit 0 alone must NOT read as a
# pass: measured 2026-09-22, tools/test_build_berry_pilot_patch.py exits 0 having run
# ZERO of its assertions, and its own message says "NOT COVERED".
SKIP_RE = re.compile(r"^SKIP\b", re.M)


def classify():
    """(collectable, script_style) -- repo-relative paths, sorted."""
    collectable, script = [], []
    for name in sorted(os.listdir(HERE)):
        if not (name.startswith("test_") and name.endswith(".py")):
            continue
        rel = os.path.join("tools", name)
        src = open(os.path.join(HERE, name), encoding="utf-8", errors="replace").read()
        (collectable if COLLECTABLE.search(src) else script).append(rel)
    return collectable, script


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def check_collection(collectable):
    """Every collectable file must yield >= 1 test. Returns the empty ones."""
    r = run([sys.executable, "-m", "pytest", "--collect-only", "-q",
             "-p", "no:cacheprovider", *collectable])
    if r.returncode == 5:
        return collectable, r  # collected nothing at all
    seen = set()
    for line in r.stdout.splitlines():
        # "tools/test_x.py::test_y" or "tools/test_x.py::Class::test_y"
        if "::" in line:
            seen.add(line.split("::", 1)[0].strip())
    return [f for f in collectable if f not in seen], r


def failure_blocks(out):
    """{test_name: its failure text} from pytest's `____ test_name ____` sections, so a
    waiver's character is matched against ITS OWN failure and not the whole log."""
    parts = re.split(r"\n_{5,} (\S+) _{5,}\n", out)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classify", action="store_true",
                    help="print the two populations and exit; runs no tests")
    ap.add_argument("--files", nargs="+", metavar="PATH",
                    help="DIAGNOSTIC: run only these entry points. Discovery floors do not "
                         "apply, because an explicit list is not discovery -- the floors exist "
                         "to catch a DISCOVERY bug in the whole-tree run. Used by the mutation "
                         "harness to drive this same main() over a small population.")
    a = ap.parse_args()

    if a.files:
        collectable, script = [], []
        for rel in a.files:
            src = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
            (collectable if COLLECTABLE.search(src) else script).append(rel)
        print(f"DIAGNOSTIC MODE: explicit file list, discovery floors not applicable")
    else:
        collectable, script = classify()
    print(f"test tree: {len(collectable)} pytest-collectable + {len(script)} script-style "
          f"= {len(collectable) + len(script)} entry points")

    # The runner obeys its own rule: an empty population is a defect, not a pass.
    fatal = []
    if a.files:
        pass  # explicit list: nothing was discovered, so there is no discovery to floor
    elif len(collectable) < MIN_COLLECTABLE:
        fatal.append(f"only {len(collectable)} collectable files found, floor {MIN_COLLECTABLE}")
    if not a.files and len(script) < MIN_SCRIPT:
        fatal.append(f"only {len(script)} script-style files found, floor {MIN_SCRIPT}")
    if fatal:
        for m in fatal:
            print(f"  BROKEN: discovery -- {m}")
        print("\nVERDICT: BROKEN (discovery inspected too little to be trusted)")
        return 3
    if a.classify:
        for f in script:
            print(f"    script-style: {f}")
        return 0

    failures = []
    waived_ok, skipped, ran_ok = [], [], 0

    # 1. Per-file collection: rc 5 at file granularity.
    print("\n[1/3] per-file collection (a file yielding 0 tests is rc-5 in miniature)")
    empty, rcol = check_collection(collectable)
    if empty:
        for f in empty:
            print(f"  BROKEN: {f} collected NO tests")
            failures.append(f"{f}: collected no tests")
    else:
        print(f"  ok: all {len(collectable)} collectable files yield at least one test")

    # 2. The pytest population.
    print(f"\n[2/3] pytest over {len(collectable)} files")
    r = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *collectable])
    tail = [l for l in r.stdout.splitlines() if l.strip()][-1:] or ["<no summary>"]
    print(f"  rc={r.returncode} | {tail[0][:160]}")
    if r.returncode == 5:
        print("  BROKEN: pytest exited 5 -- NOTHING WAS COLLECTED. Graded BROKEN, not green.")
        failures.append("pytest rc=5 (nothing collected)")
    elif r.returncode != 0:
        failed_ids = [l.split(" ", 1)[1].split(" ")[0]
                      for l in r.stdout.splitlines() if l.startswith("FAILED ")]
        blocks = failure_blocks(r.stdout)
        fired = set()
        for tid in failed_ids:
            w = WAIVERS.get(tid)
            body = blocks.get(tid.split("::")[-1], r.stdout)
            if w is None:
                print(f"  FAIL (not waived): {tid}")
                failures.append(f"unwaived test failure: {tid}")
            elif w["character"].search(body):
                fired.add(tid)
                waived_ok.append(f"{tid} [{w['ticket']}]")
            else:
                print(f"  FAIL (WAIVED TEST FAILING DIFFERENTLY): {tid} [{w['ticket']}] -- the "
                      f"waiver covers a specific failure character and this is not it")
                failures.append(f"waived test changed character: {tid}")
        for t in waived_ok:
            print(f"  WAIVED: {t}")
        # A waiver that no longer fires is a standing permission nobody revisits.
        # Reported loudly, but NOT failed: failing here would punish whoever fixed it.
        # Only meaningful when pytest actually RAN and reported failures. On a
        # collection error (rc 2) there are no FAILED lines at all, so "the test now
        # passes" would be a false reading of a tree that never ran.
        if failed_ids:
            for tid, w in WAIVERS.items():
                if tid not in fired and tid not in failed_ids:
                    print(f"  STALE WAIVER (the test now passes -- remove it): {tid} [{w['ticket']}]")

    # 3. The script-style population, run as scripts.
    print(f"\n[3/3] {len(script)} script-style files, each as `python3 <file>`")
    for f in script:
        rs = run([sys.executable, f])
        if rs.returncode != 0:
            last = [l for l in (rs.stdout + rs.stderr).splitlines() if l.strip()][-1:] or [""]
            print(f"  FAIL rc={rs.returncode} {f} | {last[0][:130]}")
            failures.append(f"{f}: rc={rs.returncode}")
        elif SKIP_RE.search(rs.stdout):
            # Exit 0 having run nothing. Counting this as a pass is the very defect
            # this runner exists to refuse, so it is reported as its own state.
            skipped.append(f)
        else:
            ran_ok += 1
    print(f"  ok: {ran_ok}/{len(script)} script-style files RAN and exited 0")
    for f in skipped:
        print(f"  SKIPPED (exited 0 having run nothing -- NOT a pass): {f}")

    print("\n" + "=" * 72)
    if failures:
        print(f"VERDICT: FAIL -- {len(failures)} problem(s)")
        for m in failures[:30]:
            print(f"  - {m}")
        return 1
    # The verdict states what was INSPECTED, waived and skipped, never a bare PASS:
    # a summary that cannot distinguish "ran and was clean" from "ran nothing" is the
    # defect this runner exists to refuse, and that applies to its own output.
    print(f"VERDICT: PASS -- {len(collectable)} collectable files (all yielding tests); "
          f"{ran_ok} of {len(script)} script-style files RAN"
          + (f", {len(skipped)} SKIPPED (ran nothing)" if skipped else "")
          + (f"; {len(waived_ok)} waived failure(s)" if waived_ok else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
