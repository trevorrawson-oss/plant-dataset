#!/usr/bin/env python3
"""Integration test: whole_crop_gate A59 (plant dimensions) fires on a scratch fixture and is a
no-op on a canonical carrying no values. Run: python3 tools/test_gate_plant_dimensions_a59.py"""
import copy, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))
FA = {"field": "plant_dimensions", "date": "2026-09-16", "sources": ["umd_ext"], "note": "test"}


def gate(slug, mutate):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    mutate(c)
    tmp = os.path.join(HERE, "_tmp_a59_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


def with_fa(c):
    c["verification_status"]["field_additions"] = list(c["verification_status"].get("field_additions") or []) + [FA]


# The block is present and announced.
out = gate("apple", lambda c: None)
assert "A59. plant dimensions" in out, "A59 block missing from whole_crop_gate"
assert "plant-dimensions:" not in out, out
# A malformed pair on a scratch copy bounces.
out = gate("apple", lambda c: (c.__setitem__("mature_height_ft", [14, 10]), with_fa(c)))
assert "plant-dimensions:" in out and "lo <= hi" in out, out
# A footprint at or above the minimum spacing bounces.
out = gate("apple", lambda c: c.__setitem__("footprint_inches", c["spacing_inches"][0]))
assert "plant-dimensions:" in out and "below spacing_inches[0]" in out, out
# An authored value with no provenance record bounces.
out = gate("apple", lambda c: c.__setitem__("mature_height_ft", [10, 14]))
assert "plant-dimensions:" in out and "field_additions" in out, out
# A good pair with its record is clean, and A33 accepts it on a tree base.
out = gate("apple", lambda c: (c.__setitem__("mature_height_ft", [10, 14]), c.__setitem__("mature_spread_ft", [8, 12]), with_fa(c)))
assert "plant-dimensions:" not in out and "mature_height_ft" not in out, out
# A33 bounds: a 500 ft apple is absurd.
out = gate("apple", lambda c: (c.__setitem__("mature_height_ft", [1, 500]), with_fa(c)))
assert "mature_height_ft" in out, out
# Presence is OFF until the canonical carries the keys; it flips in the write commit.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
assert ("A59_PRESENCE_ARMED = True" in src) == any("mature_height_ft" in c for c in base["crops"]), \
    "presence floor must arm in the same commit that writes the keys, never before"
print("PASS gate A59 plant dimensions")
