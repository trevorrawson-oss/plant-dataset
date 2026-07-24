#!/usr/bin/env python3
"""Merge the staged asparagus reference into a SCRATCH copy of the canonical and run the gates on
it -- WITHOUT touching crops_data_final.json (READ-ONLY until promote). Reused by every authoring
task to validate progress. Prints A46 / control_ladder / variety_resistance / whole_crop_gate results.
Usage: python3 tools/staging/asparagus_scratch_merge.py
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRATCH = "/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/69d736a9-c2b0-4eb2-affb-db3557b2d671/scratchpad"
OUT = os.path.join(SCRATCH, "asparagus_scratch_canonical.json")

sys.path.insert(0, os.path.join(ROOT, "tools"))
from herbaceous_perennial_gate import herbaceous_perennial_violations
from control_ladder_gate import ladder_violations, identity_violations
from variety_resistance_gate import resistance_violations

def main():
    data = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
    ref = json.load(open(os.path.join(HERE, "asparagus_reference.json"), encoding="utf-8"))["crop"]
    crops = data["crops"]
    for i, c in enumerate(crops):
        if c.get("slug") == "asparagus":
            crops[i] = ref
            break
    else:
        crops.append(ref)
    os.makedirs(SCRATCH, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("A46:", herbaceous_perennial_violations(ref) or "clean")
    print("control_ladder (ladder):", ladder_violations(data, ref) or "clean")
    print("control_ladder (identity):", identity_violations(ref) or "clean")
    print("variety_resistance:", resistance_violations(ref) or "clean")
    print("--- whole_crop_gate asparagus (scratch) ---")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "whole_crop_gate.py"),
                        "asparagus", OUT], capture_output=True, text=True)
    tail = [l for l in r.stdout.splitlines() if l.startswith("GATE:") or "FAIL" in l or "violation" in l.lower()]
    print("\n".join(tail[-40:]))
    print(r.stdout.splitlines()[-1] if r.stdout else "(no output)")

if __name__ == "__main__":
    main()
