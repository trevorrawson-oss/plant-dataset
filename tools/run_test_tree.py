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
        failures.append(f"pytest rc={r.returncode}")
        for l in r.stdout.splitlines()[-12:]:
            print(f"    | {l[:150]}")

    # 3. The script-style population, run as scripts.
    print(f"\n[3/3] {len(script)} script-style files, each as `python3 <file>`")
    ran_ok = 0
    for f in script:
        rs = run([sys.executable, f])
        if rs.returncode == 0:
            ran_ok += 1
        else:
            last = [l for l in (rs.stdout + rs.stderr).splitlines() if l.strip()][-1:] or [""]
            print(f"  FAIL rc={rs.returncode} {f} | {last[0][:130]}")
            failures.append(f"{f}: rc={rs.returncode}")
    print(f"  ok: {ran_ok}/{len(script)} script-style files exited 0")

    print("\n" + "=" * 72)
    if failures:
        print(f"VERDICT: FAIL -- {len(failures)} problem(s)")
        for m in failures[:30]:
            print(f"  - {m}")
        return 1
    print(f"VERDICT: PASS -- {len(collectable)} collectable files (all yielding tests) "
          f"+ {len(script)} script-style files, every entry point inspected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
