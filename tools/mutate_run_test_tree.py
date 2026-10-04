#!/usr/bin/env python3
"""Mutation harness for run_test_tree.py -- PLA close-out 2026-09-22.

Proves the runner REDDENS on one file of each test-file shape, per the bar in
docs/promote_suite_mutation_convention.md:

  (1) one mutation per guard family, injected into a scratch copy, verified RED;
  (2) a LIVENESS DEFENCE -- every mutation writes a MUTATION-APPLIED marker that
      is re-read from disk, plus a SENTINEL that must redden, or the run exits
      HARNESS DEAD rather than reporting survivors;
  (3) a POSITIVE CONTROL: the clean population must be GREEN before and after,
      or a "caught" verdict proves nothing (it was already red);
  (4) a REFUSAL SPEC: the old sys.exit shape is re-created in a temp file and
      shown to produce INTERNALERROR under pytest, which is the defect the three
      converted files no longer have.

  (5) M8-M12 (kickoff 60, 2026-10-03) mutate the RUNNER itself and drive
      test_run_test_tree_reporting.py: PLA-653's population check, STALE on an
      rc-0 run, ERROR lines read as failures, pytest skips counted (Fix 0), and
      the -rfEs report flags.

Run: python3 tools/mutate_run_test_tree.py
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNNER = os.path.join("tools", "run_test_tree.py")

# One file per shape.
SHAPE_A = "tools/test_chill_gate.py"            # module-level asserts
SHAPE_B = "tools/test_zone_order_gate.py"       # check() + raise (was sys.exit)
SHAPE_C = "tools/test_container_path_gate.py"   # pytest-collectable
POP = [SHAPE_A, SHAPE_B, SHAPE_C]


def run_runner(files):
    r = subprocess.run([sys.executable, RUNNER, "--files", *files],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def write(rel, s):
    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(s)


def mutate(rel, old, new, label):
    """Apply, CONFIRM APPLIED BY RE-READING, run, restore. Returns (rc, out)."""
    original = read(rel)
    if original.count(old) != 1:
        print(f"  HARNESS DEAD: anchor for {label!r} matched {original.count(old)} times in {rel}")
        sys.exit(3)
    try:
        write(rel, original.replace(old, new, 1))
        # LIVENESS: the marker must be readable FROM DISK, or we are running the clean file.
        if new not in read(rel):
            print(f"  HARNESS DEAD: mutation {label!r} did not reach disk in {rel}")
            sys.exit(3)
        return run_runner(POP)
    finally:
        write(rel, original)
        assert read(rel) == original, f"FAILED TO RESTORE {rel}"


def main():
    results = []

    # ---- POSITIVE CONTROL: the clean population is GREEN -------------------
    rc, out = run_runner(POP)
    if rc != 0:
        print("HARNESS DEAD: the CLEAN population is already red; every 'caught' below\n"
              "would be caught for the wrong reason.\n" + out[-1500:])
        return 3
    print(f"positive control: clean population GREEN (rc=0, {len(POP)} entry points)\n")

    # ---- M1: shape A, a module-level assert fails --------------------------
    rc, out = mutate(SHAPE_A, 'print("chill_gate: all tests passed")',
                     'assert False, "MUTATION-APPLIED-M1"\nprint("chill_gate: all tests passed")',
                     "M1 module-level assert failure")
    ok1 = rc != 0 and "MUTATION-APPLIED-M1" in out
    results.append(("M1 shape A (module-level assert) reddens the runner", ok1, rc))

    # ---- M2: shape B, a check() fails -> PLAIN failure, not INTERNALERROR --
    rc, out = mutate(SHAPE_B, 'MIN_CHECKS = 16',
                     'check("MUTATION-APPLIED-M2", False)\nMIN_CHECKS = 16',
                     "M2 check() failure")
    ok2 = rc != 0 and "INTERNALERROR" not in out
    results.append(("M2 shape B (check failure) reddens as a PLAIN failure, no INTERNALERROR", ok2, rc))

    # ---- M3: shape B vacuity, the check floor -----------------------------
    rc, out = mutate(SHAPE_B, "MIN_CHECKS = 16", "MIN_CHECKS = 99   # MUTATION-APPLIED-M3",
                     "M3 check floor")
    ok3 = rc != 0 and "VACUOUS" in out
    results.append(("M3 shape B floor: too few checks ran -> VACUOUS, refused", ok3, rc))

    # ---- M4: shape C, the file collects NOTHING (rc 5 in miniature) -------
    src_c = read(SHAPE_C)
    original_c = src_c
    try:
        write(SHAPE_C, src_c.replace("def test_", "def _MUTATION_APPLIED_M4_test_"))
        if "_MUTATION_APPLIED_M4_test_" not in read(SHAPE_C):
            print("  HARNESS DEAD: M4 did not reach disk"); sys.exit(3)
        rc, out = run_runner(POP)
    finally:
        write(SHAPE_C, original_c)
        assert read(SHAPE_C) == original_c, "FAILED TO RESTORE " + SHAPE_C
    ok4 = rc != 0 and "collected NO tests" in out
    results.append(("M4 shape C (0 tests collected) caught by per-file collection", ok4, rc))

    # ---- M5: the discovery floor (whole-tree mode) ------------------------
    probe = (
        "import sys, os; sys.path.insert(0, %r)\n"
        "import run_test_tree as R\n"
        "R.classify = lambda: (['tools/test_chill_gate.py'], [])  # MUTATION-APPLIED-M5\n"
        "sys.argv = ['run_test_tree.py']\n"
        "sys.exit(R.main())\n" % HERE
    )
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=ROOT) as fh:
        fh.write(probe)
        probe_path = fh.name
    try:
        r = subprocess.run([sys.executable, probe_path], cwd=ROOT, capture_output=True, text=True)
        ok5 = r.returncode != 0 and "BROKEN: discovery" in (r.stdout + r.stderr)
    finally:
        os.unlink(probe_path)
    results.append(("M5 discovery floor: too few entry points found -> BROKEN", ok5, r.returncode))

    # ---- M6: a THIRD failure (not waived) must fail the tree -------------
    # Re-homed 2026-09-30 (PLA-544): the bare_host_scan waiver was removed when its test was pinned
    # by identity and went green; the remaining waiver is cited_claim_scan's cache-coverage one.
    WPOP = ["tools/test_cited_claim_scan.py", "tools/test_container_path_gate.py"]
    def run_wpop(): return run_runner(WPOP)
    # baseline: the waived failure alone leaves the tree PASSING
    rc, out = run_wpop()
    if rc != 0 or "WAIVED" not in out:
        print("HARNESS DEAD: the waiver baseline is not green-with-a-waiver; "
              "every verdict below would be caught for the wrong reason.")
        sys.exit(3)
    print("waiver baseline: PASS with the waived failure reported (the waiver fires)\n")

    orig = read("tools/test_container_path_gate.py")
    try:
        # APPENDED at module level, not spliced in: this file's tests live inside a
        # unittest.TestCase, so an unindented def mid-class is an IndentationError --
        # the file then collects NOTHING and the per-file collection guard fires
        # FIRST, so the driver never reaches the waiver branch it is meant to test.
        # Measured while authoring; a driver that reddens for the wrong reason is
        # vacuous coverage.
        write("tools/test_container_path_gate.py",
              orig + "\n\ndef test_MUTATION_APPLIED_M6_third_failure():\n"
                     "    assert False, 'M6 a third, UNWAIVED failure'\n")
        if "M6 a third, UNWAIVED failure" not in read("tools/test_container_path_gate.py"):
            print("  HARNESS DEAD: M6 did not reach disk"); sys.exit(3)
        rc, out = run_wpop()
    finally:
        write("tools/test_container_path_gate.py", orig)
        assert read("tools/test_container_path_gate.py") == orig, "FAILED TO RESTORE"
    ok6 = rc != 0 and "unwaived test failure" in out
    results.append(("M6 a THIRD, unwaived failure FAILS the tree", ok6, rc))

    # ---- M7: a WAIVED test failing DIFFERENTLY must fail ------------------
    # Driven over WPOP, not POP: POP does not contain the waived file, so a mutation
    # there could never reach the waiver branch -- a driver that never reaches its
    # entry point is vacuous, which is this convention's own recurring lesson.
    W7 = "tools/test_cited_claim_scan.py"
    orig7 = read(W7)
    if orig7.count('f"CACHE COVERAGE, NOT A DATA DEFECT: {slug}: ') != 1:
        print("  HARNESS DEAD: M7 anchor not found exactly once"); sys.exit(3)
    try:
        write(W7, orig7.replace('f"CACHE COVERAGE, NOT A DATA DEFECT: {slug}: ',
                                'f"CACHE COVERAGE, NOT A DATA DEFECT: MUTATION-APPLIED-M7 {slug}: ', 1))
        if "MUTATION-APPLIED-M7" not in read(W7):
            print("  HARNESS DEAD: M7 did not reach disk"); sys.exit(3)
        rc, out = run_wpop()
    finally:
        write(W7, orig7)
        assert read(W7) == orig7, "FAILED TO RESTORE"
    ok7 = rc != 0 and "changed character" in out
    results.append(("M7 a WAIVED test failing DIFFERENTLY fails (character, not just id)", ok7, rc))

    # ---- M8-M12: the RUNNER's own reporting (kickoff 60, 2026-10-03) --------
    # These mutate run_test_tree.py ITSELF and drive test_run_test_tree_reporting.py, which runs the real
    # main() over throwaway probe files. Positive control first: that suite is GREEN on the clean runner.
    REP = "tools/test_run_test_tree_reporting.py"

    def run_reporting(sel):
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", REP, "-k", sel],
                           cwd=ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    rc, out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", REP],
                             cwd=ROOT, capture_output=True, text=True).returncode, ""
    if rc != 0:
        print("HARNESS DEAD: the reporting suite is already red on the clean runner"); sys.exit(3)
    print("reporting positive control: test_run_test_tree_reporting GREEN on the clean runner\n")

    def mutate_runner(old, new, label, sel):
        original = read(RUNNER)
        if original.count(old) != 1:
            print(f"  HARNESS DEAD: anchor for {label!r} matched {original.count(old)} times in {RUNNER}")
            sys.exit(3)
        try:
            write(RUNNER, original.replace(old, new + "  # MUTATION-APPLIED", 1))
            if "# MUTATION-APPLIED" not in read(RUNNER):
                print(f"  HARNESS DEAD: mutation {label!r} did not reach disk"); sys.exit(3)
            rc_, out_ = run_reporting(sel)
        finally:
            write(RUNNER, original)
            assert read(RUNNER) == original, f"FAILED TO RESTORE {RUNNER}"
        return rc_ not in (0, 5), rc_

    ok, rc = mutate_runner(
        '        (stale if tid.split("::", 1)[0] in collectable else not_run).append(f"{tid} [{w[\'ticket\']}]")',
        '        (stale if True else not_run).append(f"{tid} [{w[\'ticket\']}]")',
        "M8 population check dropped", "not_collected_is_not_STALE_when_another_test_fails")
    results.append(("M8 PLA-653: a waived test NOT collected reported STALE (population check dropped)", ok, rc))
    ok, rc = mutate_runner(
        "        stale, not_run = waiver_states(failed_ids, collectable, fired)",
        "        stale, not_run = waiver_states(failed_ids, collectable, fired) if failed_ids else ([], [])",
        "M9 STALE only when something failed", "now_passes_is_STALE_on_an_rc0_run")
    results.append(("M9 the `if failed_ids:` gate restored: a stale waiver on a green run goes silent", ok, rc))
    ok, rc = mutate_runner(
        '                     for l in r.stdout.splitlines() if l.startswith("ERROR ")]',
        '                     for l in r.stdout.splitlines() if l.startswith("ERROR-NEVER ")]',
        "M10 ERROR lines unread", "ERRORS_fails_the_tree")
    results.append(("M10 ERROR lines unread: a setup error must still fail the tree", ok, rc))
    ok, rc = mutate_runner(
        "        for n, path, why in PYTEST_SKIP_RE.findall(r.stdout):",
        "        for n, path, why in []:",
        "M11 pytest skips unread", "pytest_skip_is_counted_in_the_verdict")
    results.append(("M11 Fix 0: pytest skips unread, the VERDICT no longer counts them", ok, rc))
    ok, rc = mutate_runner(
        '"-q", "-rfEs", "-p"', '"-q", "-rs", "-p"',
        "M12 -r restated without fE", "ERRORS_fails_the_tree")
    results.append(("M12 -rs alone REPLACES pytest's default fE: FAILED/ERROR lines vanish", ok, rc))

    # ---- SENTINEL: a mutation that MUST redden, or the harness is dead ----
    rc, out = mutate(SHAPE_A, 'print("chill_gate: all tests passed")',
                     'import THIS_MODULE_DOES_NOT_EXIST_SENTINEL\nprint("chill_gate: all tests passed")',
                     "SENTINEL")
    if rc == 0:
        print("HARNESS DEAD: the sentinel (an unresolvable import) did NOT redden the runner.\n"
              "Every verdict above is untrustworthy.")
        return 3
    print("sentinel: reddened as required (the harness is live)\n")

    # ---- REFUSAL SPEC: the shape we removed really did INTERNALERROR ------
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "test_oldshape.py")
        open(p, "w").write("import sys\nsys.exit(1)\n")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", p],
                           capture_output=True, text=True, cwd=td)
        ok6 = "INTERNALERROR" in (r.stdout + r.stderr)
    results.append(("refusal spec: a module-level sys.exit(1) DOES produce INTERNALERROR "
                    "(the defect the 3 converted files no longer have)", ok6, r.returncode))

    # ---- POSITIVE CONTROL AGAIN: restoration worked -----------------------
    rc, out = run_runner(POP)
    if rc != 0:
        print("HARNESS DEAD: the population did not restore to GREEN after mutation.")
        return 3

    print("=" * 74)
    caught = sum(1 for _, ok, _ in results if ok)
    for name, ok, rc_ in results:
        print(f"  {'CAUGHT ' if ok else 'SURVIVED'} (rc={rc_})  {name}")
    print("=" * 74)
    print(f"{caught}/{len(results)} caught / {len(results) - caught} survived / 0 broken; "
          f"positive control GREEN before and after; sentinel reddened")
    return 0 if caught == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
