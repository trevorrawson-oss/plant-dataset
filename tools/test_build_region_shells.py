#!/usr/bin/env python3
"""Unit test for build_region_shells -- asserts the post-transform shape.
Run from repo root: python3 tools/test_build_region_shells.py"""
import json, copy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_region_shells import build_region_shells

REGION_KEYS = {"northern_tier", "se_gulf", "ca_interior", "ca_north_coast",
               "ca_south_coast", "ca_desert", "warm_arid", "low_desert_az",
               "fl_peninsula", "hawaii_tropical"}

data = json.load(open("crops_data_final.json"))
cherry = copy.deepcopy(next(c for c in data["crops"] if c["slug"] == "cherry-tomato"))
build_region_shells(cherry)
regions = cherry["regions"]

# all 10 regions present
assert set(regions) == REGION_KEYS, f"region set: {set(regions)}"

# no stub plantings; every plantings entry is a dict with a valid track
for rk, r in regions.items():
    pl = r["plantings"]
    assert isinstance(pl, list) and pl and isinstance(pl[0], dict), f"{rk}: stub plantings"
    for p in pl:
        assert p.get("track") in {"beginner", "second_planting", "succession"}, f"{rk}: bad track {p.get('track')!r}"

# no nested plantings in any resolved_by_zone cell (the forbidden shape)
for rk, r in regions.items():
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        assert "plantings" not in cell, f"{rk}.{z}: nested plantings survived"

# northern_tier promoted from zones
nt = regions["northern_tier"]
for z, cell in nt["resolved_by_zone"].items():
    assert cell.get("resolution_method") == "zone_promoted_verified", f"nt.{z}: not restamped"
assert isinstance(nt["plantings_provenance"], str) and "Zone-promoted" in nt["plantings_provenance"]

# region_label em-dashes resolved
for rk, r in regions.items():
    assert " -- " not in (r.get("region_label") or ""), f"{rk}: region_label still has --"

# region_notes keys present on every region (value may be null at shell stage)
for rk, r in regions.items():
    assert "region_notes_seasoned" in r and "region_notes_beginner" in r, f"{rk}: missing region_notes keys"

# warm shells: shape-complete RULE skeleton with empty archetype window arrays
for rk in ["se_gulf", "ca_interior", "hawaii_tropical"]:
    p0 = regions[rk]["plantings"][0]
    assert p0["track"] == "beginner", f"{rk}: warm track"
    for w in ["start_indoors", "plant_out", "harvest_start", "harvest_end"]:
        assert p0.get(w) == [], f"{rk}: {w} should be present-but-empty, got {p0.get(w)!r}"

print("PASS build_region_shells")
