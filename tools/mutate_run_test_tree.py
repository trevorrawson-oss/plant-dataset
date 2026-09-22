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
