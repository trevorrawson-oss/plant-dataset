#!/usr/bin/env python3
"""Mutation harness for variety_ladder_delta_gate (PLA-215 convention).

WHY THIS EXISTS: the suite is GREEN FROM BIRTH -- the gate and its tests were written together, so
there was no honest TDD RED phase and "all tests pass" is not evidence of anything. Worse, the gate
returns 0 on the live canonical because `ladder_delta` does not exist yet, which reads exactly like
coverage while providing none. The only evidence that each guard is REACHABLE and each test is
NON-VACUOUS is to break the guard and watch the suite notice.

Direction: we mutate the GATE (one guard family at a time) and require the SUITE to redden.

LIVENESS DEFENSE (PLA-138's harness silently graded the CLEAN fixture and reported every mutation as
surviving, so all three of these are mandatory):
  1. MUTATION-APPLIED marker -- the file about to execute is read back and asserted to contain the
     marker AND to differ from the original. A mutation that did not land cannot be graded.
  2. SENTINEL -- a mutation that neuters the gate entirely MUST redden. If it does not, the harness
     is not running what it thinks it is running and we exit HARNESS DEAD.
  3. POSITIVE CONTROL -- the UNMUTATED gate must pass. If the clean run fails, every "caught" verdict
     below is meaningless.

Usage: python3 tools/mutate_variety_ladder_delta_suite.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "variety_ladder_delta_gate.py")
TEST = os.path.join(HERE, "test_variety_ladder_delta_gate.py")
MARKER = "# MUTATION-APPLIED"

# (label, guard family, old, new) -- one per guard family, each independently reachable
MUTATIONS = [
    ("G1 problem-id referential check disabled", "G1",
     "if pid not in laddered:", "if False:"),
    ("G1 parent-ladder membership check disabled", "G1",
     "if m not in parent_by_method:", "if False:"),
    ("G1 'add' duplicate-of-parent check disabled", "G1",
     "if m in parent_by_method:", "if False:"),
    ("G1 unknown control_methods key allowed", "G1",
     "if m not in catalog:", "if False:"),
    ("G1 basis enum check disabled", "G1",
     "if basis not in BASES:", "if False:"),
    ("G1 source T1 tier check disabled", "G1",
     'elif source_catalog[s].get("tier") != "T1":', "elif False:"),
    ("G1 op enum check disabled", "G1",
     "if op not in OPS:", "if False:"),
    ("G2 empty-rungs check disabled", "G2",
     "if not rungs:", "if False:"),
    ("G2 duplicate-method check disabled", "G2",
     "if m in seen:", "if False:"),
    ("G2 BYTE-EQUAL duplicate check disabled", "G2",
     "if new == old:", "if False:"),
    ("G3 near-verbatim threshold raised out of reach", "G3",
     "NEAR_VERBATIM = 0.85", "NEAR_VERBATIM = 2.0"),
    ("G3 normalization removed (reflow dodges the guard)", "G3",
     're.sub(r"\\s+", " ", (s or "").strip().lower())', "(s or '')"),
    ("G4 resolved softest-first check disabled", "G4",
     "if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):", "if False:"),
    ("G4 resolver drops are ignored", "G4",
     'drops = {r["method"] for r in rungs if r.get("op") == "drop" and isinstance(r.get("method"), str)}',
     "drops = set()"),
    ("resolver mutates the parent in place", "resolver",
     'out.append(dict(pr, **{k: v for k, v in repl[m].items()\n                               if k.startswith("note_")}) if m in repl else dict(pr))',
     'pr.update({k: v for k, v in repl[m].items() if k.startswith("note_")}) if m in repl else None\n        out.append(pr)'),
]

SENTINEL = ("SENTINEL: delta_violations neutered to always return []",
            "def delta_violations(crop, catalog, source_catalog=None):\n    V = []",
            "def delta_violations(crop, catalog, source_catalog=None):\n    return []\n    V = []")


def run_suite(workdir):
    """Run the test suite against whatever gate sits in workdir. True == GREEN."""
    r = subprocess.run([sys.executable, os.path.join(workdir, os.path.basename(TEST))],
                       capture_output=True, text=True, cwd=workdir)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def stage(old, new):
    """Copy gate+test into a temp dir, apply one mutation, verify it LANDED. Returns workdir."""
    wd = tempfile.mkdtemp(prefix="mutate_vldg_")
    shutil.copy(TEST, wd)
    src = open(GATE).read()
    if src.count(old) != 1:
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: anchor is not unique ({src.count(old)}x): {old!r}")
    mutated = src.replace(old, new + "  " + MARKER, 1)
    dst = os.path.join(wd, os.path.basename(GATE))
    open(dst, "w").write(mutated)
    # -- liveness defense 1: the file about to execute really is mutated -----------------
    back = open(dst).read()
    if MARKER not in back:
        raise SystemExit("HARNESS DEAD: MUTATION-APPLIED marker absent from the staged file")
    if back == src:
        raise SystemExit("HARNESS DEAD: staged file is byte-identical to the original")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- variety_ladder_delta_gate")
    print("=" * 78)

    # -- liveness defense 3: POSITIVE CONTROL ------------------------------------------
    wd = tempfile.mkdtemp(prefix="mutate_vldg_control_")
    shutil.copy(TEST, wd); shutil.copy(GATE, wd)
    ok, out = run_suite(wd)
    shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: the POSITIVE CONTROL (unmutated gate) FAILS.")
        print(out)
        return 1
    print("positive control : GREEN (unmutated gate passes)\n")

    # -- liveness defense 2: SENTINEL ---------------------------------------------------
    label, old, new = SENTINEL
    wd = stage(old, new)
    ok, _ = run_suite(wd)
    shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED -- the suite is not grading the staged gate.")
        return 1
    print(f"sentinel         : RED as required ({label})\n")

    caught = survived = 0
    fam = {}
    for label, family, old, new in MUTATIONS:
        wd = stage(old, new)
        ok, out = run_suite(wd)
        shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for f in sorted(fam):
        c, s = fam[f]
        print(f"  {f:9s} {c} caught / {c + s} injected" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL -- a guard family is unreachable or its test is vacuous.")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
