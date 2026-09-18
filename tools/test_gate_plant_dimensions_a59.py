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


# The fixture crop is a CERTIFIED crop carrying no authored value and no plant_dimensions record on the
# canonical (a null row after the 2026-09-16 write), so every injection below is the ONLY value on it.
# apple is authored on the live canonical and would carry its own record, which answered for the
# "no provenance" case once the write landed.
NULL_CROP = "basil"
nc = next(c for c in base["crops"] if c["slug"] == NULL_CROP)
assert nc.get("mature_height_ft") is None and not any(x.get("field") == "plant_dimensions" for x in nc["verification_status"].get("field_additions") or []), \
    f"{NULL_CROP} is no longer a clean fixture for this test; pick a certified crop with no plant_dimensions value or record"
# The block is present and announced, and a null row is clean.
out = gate(NULL_CROP, lambda c: None)
assert "A59. plant dimensions" in out, "A59 block missing from whole_crop_gate"
assert "plant-dimensions:" not in out, out
# A malformed pair on a scratch copy bounces.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [4, 1]), with_fa(c)))
assert "plant-dimensions:" in out and "lo <= hi" in out, out
# A footprint at or above the minimum spacing bounces.
out = gate(NULL_CROP, lambda c: c.__setitem__("footprint_inches", c["spacing_inches"][0]))
assert "plant-dimensions:" in out and "below spacing_inches[0]" in out, out
# An authored value with no provenance record bounces.
out = gate(NULL_CROP, lambda c: c.__setitem__("mature_height_ft", [1, 2]))
assert "plant-dimensions:" in out and "field_additions" in out, out
# A good pair with its record is clean, and A33 accepts it on a non-tree base.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), c.__setitem__("mature_spread_ft", [1, 2]), with_fa(c)))
assert "plant-dimensions:" not in out and "mature_height_ft" not in out, out
# A33 bounds: a 60 ft basil is absurd on a non-tree base.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 60]), with_fa(c)))
assert "mature_height_ft" in out, out
# An authored crop on the live canonical carries its record and is clean.
out = gate("apple", lambda c: None)
assert "plant-dimensions:" not in out, out
# Presence arms in the same commit that writes the keys, never before: the flag must match the data.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
assert ("A59_PRESENCE_ARMED = True" in src) == any("mature_height_ft" in c for c in base["crops"]), \
    "presence floor must arm in the same commit that writes the keys, never before"
# With presence ARMED, a certified crop missing a key bounces.
if "A59_PRESENCE_ARMED = True" in src:
    out = gate(NULL_CROP, lambda c: c.pop("footprint_inches"))
    assert "plant-dimensions:" in out and "missing" in out, out
# With coverage ARMED, a WOODY crop whose null loses its explaining record bounces, and the message names
# the field. plum's ruling lives as an addendum on its pollination finding, so this drives the real shape.
if "A59_COVERAGE_ARMED = True" in src:
    def de_name(c):
        for f in c["verification_status"]["open_findings"]:
            f["summary"] = f["summary"].replace("mature_height_ft", "HEIGHT")
    out = gate("plum", de_name)
    assert "plant-dimensions:" in out and "no record names the field" in out, out
    # and an authored woody crop is clean under coverage
    out = gate("apple", lambda c: None)
    assert "plant-dimensions:" not in out, out
    # a cane fruit is exempt by the predicate even with its record de-named (the branch, in isolation)
    out = gate("raspberry", de_name)
    assert "plant-dimensions:" not in out, out
print("PASS gate A59 plant dimensions")
