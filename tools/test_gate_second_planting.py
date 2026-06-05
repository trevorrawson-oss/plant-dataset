#!/usr/bin/env python3
"""Integration test: the gate validates the second_planting structure.
Reuses real cherry (post-transform) + injects a second_planting into a resolved
cell, runs the gate as a subprocess, and checks the specific violation string.
Run from repo root: python3 tools/test_gate_second_planting.py"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_region_shells import build_region_shells

base = json.load(open("crops_data_final.json"))
build_region_shells(next(c for c in base["crops"] if c["slug"] == "cherry-tomato"))


def run_gate_with(sp_value):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == "cherry-tomato")
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["second_planting"] = sp_value
    tmp = os.path.join(HERE, "_tmp_sp_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "whole_crop_gate.py"), "cherry-tomato", tmp],
            capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)
    return out

# missing window keys -> violation
bad = run_gate_with({"plant_out": "Aug 1 - Aug 14"})
assert "second_planting missing window keys" in bad, "expected missing-keys violation"

# non-dict -> violation
nd = run_gate_with("PENDING")
assert "second_planting not a dict" in nd, "expected not-a-dict violation"

# well-formed (all window keys present; values may be null at admission) -> no sp violation
good = run_gate_with({"plant_out": "Aug 1 - Aug 14", "start_indoors": None,
                      "harvest_start": "Oct 1", "harvest_end": "Dec 10",
                      "sources": [], "anchoring_urls": {}})
assert "second_planting missing window keys" not in good, "well-formed should not flag missing keys"
assert "second_planting not a dict" not in good, "well-formed should not flag dict"

print("PASS gate second_planting validation")
