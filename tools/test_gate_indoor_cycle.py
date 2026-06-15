#!/usr/bin/env python3
"""Integration test: whole_crop_gate enforces the non_seasonal_indoor cycle presence
(the Step 5.5 indoor-branch check). An indoor crop (microgreens/sprouts/mushrooms) has no
frost/region/zone axis -- its source of truth is the indoor_cycle block. The gate must
require it (days_to_harvest non-empty + dual-register tip pair) for a non_seasonal_indoor
crop, and be a NO-OP for any other calendar_basis.
Run from repo root: python3 tools/test_gate_indoor_cycle.py"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

base = json.load(open("crops_data_final.json"))
V = "indoor_cycle incomplete"


def run_gate(slug, mutate=None):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    if mutate:
        mutate(c)
    tmp = os.path.join(HERE, "_tmp_indoor_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
            capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)
    return out

# microgreens-mix as-is (indoor_cycle populated) -> NO indoor-cycle violation
assert V not in run_gate("microgreens-mix"), "populated indoor_cycle wrongly flagged"

# empty days_to_harvest -> violation (no cycle length = no source of truth)
def empty_dth(c): c["indoor_cycle"]["days_to_harvest"] = []
assert V in run_gate("microgreens-mix", empty_dth), "empty days_to_harvest should flag"

# a null register tip -> violation (the cycle must be dual-register)
def null_tip(c): c["indoor_cycle"]["tip_beginner"] = None
assert V in run_gate("microgreens-mix", null_tip), "null tip_beginner should flag"

# a frost_anchored crop has no indoor_cycle and must NOT be flagged (no-op off-branch)
assert V not in run_gate("cherry-tomato"), "frost crop wrongly subjected to the indoor check"

print("PASS gate indoor_cycle presence")
