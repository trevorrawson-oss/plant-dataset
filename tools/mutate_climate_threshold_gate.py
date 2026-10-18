#!/usr/bin/env python3
"""mutate_climate_threshold_gate -- proof that test_climate_threshold_gate catches a regression in every
guard family of the PLA-750 P5 amendment (and the pre-existing heat pairing it sits inside).

Each mutation edits the GATE'S SOURCE in a scratch directory (never tools/), then runs the suite there.
A mutation must turn the suite RED.

LIVENESS (PLA-215 convention items 2 and 3):
  * POSITIVE CONTROL  the unmutated scratch copy passes the suite.
  * MUTATION-APPLIED  every mutation's `old` text must occur exactly once in the gate source and the
                      staged source must differ from the original, or the run exits HARNESS DEAD.
  * SENTINEL          emptying NULL_STRESS_KNOWN must redden; if it does not, HARNESS DEAD.

Usage: python3 tools/mutate_climate_threshold_gate.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "climate_threshold_gate.py")
SUITE = os.path.join(HERE, "test_climate_threshold_gate.py")

MUTATIONS = [
    # (family, label, old, new)
    ("allowlist", "null + ANY stress effect passes (the allowlist check dropped)",
     'if he != "heat_tolerant" and (slug, he) not in NULL_STRESS_KNOWN:',
     'if he != "heat_tolerant" and False:'),
    ("allowlist-key", "the allowlist keyed on slug only (effect ignored)",
     'if he != "heat_tolerant" and (slug, he) not in NULL_STRESS_KNOWN:',
     'if he != "heat_tolerant" and slug not in {s for s, _e in NULL_STRESS_KNOWN}:'),
    ("allowlist-entry", "a fourth crop slipped into the allowlist",
     'NULL_STRESS_KNOWN = {\n',
     'NULL_STRESS_KNOWN = {\n    ("borage", "quality_loss"): "PLA-750 D5: injected",\n'),
    ("stale", "the STALE check never runs on the roster",
     "    violations += stale_null_stress(crops)\n",
     "\n"),
    ("stale-effect", "STALE ignores a changed effect",
     ' or c.get("heat_effect") != effect:',
     ':'),
    ("pairing", "an int threshold with heat_tolerant passes (pre-existing rule dropped)",
     '            if he == "heat_tolerant":\n                v.append(f"{slug}: heat_effect \'heat_tolerant\' but',
     '            if False:\n                v.append(f"{slug}: heat_effect \'heat_tolerant\' but'),
    ("population", "the PASS line stops reporting its population",
     'f"\\nclimate_threshold_gate: PASS (0 violations across {len(crops)} crops; "',
     'f"\\nclimate_threshold_gate: PASS (0 violations; "'),
]
SENTINEL = ("SENTINEL: NULL_STRESS_KNOWN emptied", "NULL_STRESS_KNOWN = {\n", "NULL_STRESS_KNOWN = {} and {\n")


def run_suite(src):
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "climate_threshold_gate.py"), "w", encoding="utf-8") as f:
            f.write(src)
        shutil.copy(SUITE, td)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            os.path.join(td, "test_climate_threshold_gate.py")],
                           capture_output=True, text=True, cwd=td)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]


def stage(orig, old, new, label):
    if orig.count(old) != 1:
        raise SystemExit(f"HARNESS DEAD: {label}: the mutation's text occurs {orig.count(old)} times in the gate")
    src = orig.replace(old, new)
    if src == orig:
        raise SystemExit(f"HARNESS DEAD: {label}: MUTATION-APPLIED marker failed (source unchanged)")
    return src


def main():
    orig = open(GATE, encoding="utf-8").read()
    rc, tail = run_suite(orig)
    if rc != 0:
        print(f"HARNESS DEAD: positive control is RED on the unmutated gate: {tail}")
        return 1
    print(f"positive control : GREEN ({tail[0] if tail else ''})")
    label, old, new = SENTINEL
    rc, tail = run_suite(stage(orig, old, new, label))
    if rc == 0:
        print(f"HARNESS DEAD: {label} did not redden the suite")
        return 1
    print(f"sentinel         : REDDENS ({tail[0] if tail else ''})\n")
    caught = survived = 0
    for family, label, old, new in MUTATIONS:
        rc, tail = run_suite(stage(orig, old, new, label))
        if rc == 0:
            survived += 1
            print(f"  SURVIVED  [{family:15s}] {label}")
        else:
            caught += 1
            print(f"  caught    [{family:15s}] {label}  ({tail[0] if tail else ''})")
    print(f"\nTOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS -- every guard family of the P5 amendment reddens the suite when broken.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
