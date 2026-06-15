#!/usr/bin/env python3
"""Integration test: the §3 container check accepts the INDOOR TRAY model.

A potted crop is dimensioned by volume (min_pot_gallons); an indoor tray crop
(microgreens/sprouts, anchor 11) by depth (depth_inches_min) -- a 1020-style tray is
not measured in gallons. container_ok therefore requires ONE of the two dimensions,
not min_pot_gallons specifically. Potted crops (a real min_pot_gallons) are unchanged.
Run from repo root: python3 tools/test_gate_container_tray.py"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

base = json.load(open("crops_data_final.json"))


def run_gate_with_container(cn_value):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == "cherry-tomato")
    c["container_notes"] = cn_value
    tmp = os.path.join(HERE, "_tmp_container_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "whole_crop_gate.py"), "cherry-tomato", tmp],
            capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)
    return out


V = "§3 container fields"

# TRAY model: container_ok + depth_inches_min, pot-gallons N/A -> NO §3 container violation
tray = run_gate_with_container({"container_ok": True, "min_pot_gallons": None,
                                "depth_inches_min": 1, "shape_requirements": "shallow 1020-style tray"})
assert V not in tray, "tray (depth-dimensioned) container wrongly flagged §3"

# POTTED model: container_ok + pot-gallons (no depth) -> unchanged, still PASS
potted = run_gate_with_container({"container_ok": True, "min_pot_gallons": 5, "depth_inches_min": None})
assert V not in potted, "potted (gallon-dimensioned) container wrongly flagged §3"

# DIMENSIONLESS: container_ok but NEITHER gallons nor depth -> real gap, still a violation
bad = run_gate_with_container({"container_ok": True, "min_pot_gallons": None, "depth_inches_min": None})
assert V in bad, "container_ok with no dimension at all should still flag §3"

print("PASS gate container tray model")
