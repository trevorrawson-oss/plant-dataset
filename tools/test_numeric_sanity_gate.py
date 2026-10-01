#!/usr/bin/env python3
"""Tests for the numeric-sanity truth-layer gate (whole_crop_gate A33; incognito-redteam C7,
the deterministic layer). Run: python3 tools/test_numeric_sanity_gate.py

WHY (truth layer, brainstorm -> Trevor picked deterministic first): the cert suite validates
SHAPE, never that a NUMBER is physically plausible. The fabricated-crop attack (C7, "rutabaga that
is basil verbatim") shipped days_to_maturity:[3,5], sunlight_hours:[0,1], spacing_inches:[120,144]
(tree spacing on an annual), ph:[3.0,3.4] -- all well-SHAPED, all absurd. This gate bounds every
key numeric to a physical range; spacing is ARCHETYPE-AWARE (an annual at 120in is absurd; a tree at
300in is normal). Bounds carry margin over the observed 18 (0 false positives). It catches the
EGREGIOUS / copy-template-don't-refit numeric; the plausible-but-wrong value (a pH inside [3,10] that
contradicts the prose) is the cross-consistency layer's job, not this one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numeric_sanity_gate import numeric_sanity_violations

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]


def annual():
    return {"slug": "x", "calendar_basis": "frost_anchored",
            "ph": {"preferred_range": [6.0, 6.8], "tolerated_range": [5.5, 7.5]},
            "days_to_maturity": [55, 70], "sunlight_hours": [6, 8],
            "spacing_inches": [12, 24], "germination_temp_f": [70, 85]}


# 0. a clean annual -> no violations
assert numeric_sanity_violations(annual()) == [], numeric_sanity_violations(annual())

# 1. days_to_maturity:[3,5] (the C7 value) -> violation (below the 7-day floor)
c = annual(); c["days_to_maturity"] = [3, 5]
assert any("days_to_maturity" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)

# 2. sunlight_hours:[0,1] (the C7 value) -> violation (0 below the 1h floor)
c = annual(); c["sunlight_hours"] = [0, 1]
assert any("sunlight_hours" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)

# 3. spacing_inches:[120,144] on an ANNUAL (the C7 value -- tree spacing on a rutabaga) -> violation
c = annual(); c["spacing_inches"] = [120, 144]
assert any("spacing_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)

# 4. ARCHETYPE-AWARE: the SAME [120,144] spacing on a real tree is FINE (no violation)
tree = {"slug": "peach", "calendar_basis": "perennial_chill_gated", "spacing_inches": [216, 240]}
assert numeric_sanity_violations(tree) == [], numeric_sanity_violations(tree)

# 5. ph out of the physical [3,10] band -> violation (e.g. a 14 or a negative)
c = annual(); c["ph"] = {"preferred_range": [13.0, 14.0], "tolerated_range": [12.0, 14.0]}
assert any("ph" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# but blueberry's acid 4.5 is FINE (within [3,10])
c = annual(); c["ph"] = {"preferred_range": [4.5, 5.5], "tolerated_range": [4.0, 6.0]}
assert numeric_sanity_violations(c) == [], numeric_sanity_violations(c)

# 6. germination_temp_f absurd (e.g. 200F) -> violation
c = annual(); c["germination_temp_f"] = [180, 200]
assert any("germination_temp_f" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)

# 7. negative numerics anywhere bounded -> violation
c = annual(); c["days_to_maturity"] = [-5, -10]
assert any("days_to_maturity" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)

# 8. EMPTY days_to_maturity ([] perennial N/A) -> no violation (skip when absent/empty)
c = annual(); c["days_to_maturity"] = []
assert numeric_sanity_violations(c) == [], numeric_sanity_violations(c)

# 9. a tree variety chill of 1050 is fine; 9000 is absurd -> violation
tree2 = {"slug": "peach", "calendar_basis": "perennial_chill_gated",
         "varieties": {"recommended": [{"name": "x", "chill_hours_required": 9000}]}}
assert any("chill_hours_required" in v for v in numeric_sanity_violations(tree2)), numeric_sanity_violations(tree2)

# 9b. per-variety days_to_maturity is bounded like the crop-level number: a 3-day or 500-day variety
# DTM is absurd -> violation; a normal 75 is fine; a season-typed variety (no DTM) is skipped. (A33
# bounded the crop DTM + variety chill but never variety DTM -- the fabricated-crop slip. 2026-07-07.)
c = {"slug": "x", "calendar_basis": "frost_anchored",
     "varieties": {"recommended": [{"name": "TooFast", "days_to_maturity": 3}]}}
assert any("days_to_maturity" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
c = {"slug": "x", "calendar_basis": "frost_anchored",
     "varieties": {"recommended": [{"name": "TooSlow", "days_to_maturity": 500}]}}
assert any("days_to_maturity" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
c = {"slug": "x", "calendar_basis": "frost_anchored",
     "varieties": {"recommended": [{"name": "California Wonder", "days_to_maturity": 75},
                                    {"name": "Duke", "season": "early"}]}}
assert numeric_sanity_violations(c) == [], numeric_sanity_violations(c)

# 10. REAL DATA: every certified anchor is numerically sane (0 false positives)
fp = [(c["slug"], numeric_sanity_violations(c)) for c in _cert if numeric_sanity_violations(c)]
assert fp == [], f"numeric-sanity FP on certified anchors: {fp}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified anchors: PASS")

print("numeric_sanity_gate: all tests passed")


# --- PLA-465 plant dimensions (register row 30): archetype-aware like spacing ---------------------
def tree():
    c = annual(); c["calendar_basis"] = "perennial_chill_gated"; c["spacing_inches"] = [120, 300]
    return c


# a tree at 30-60 ft (a standard mulberry) is fine; the same on an annual is absurd
c = tree(); c["mature_height_ft"] = [30, 60]; c["mature_spread_ft"] = [30, 50]
assert not any("mature_" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
c = annual(); c["mature_height_ft"] = [30, 60]
assert any("mature_height_ft" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# a 500 ft tree is absurd on any basis
c = tree(); c["mature_height_ft"] = [1, 500]
assert any("mature_height_ft" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# a rosemary at 6 ft and a sunflower at 12 ft fit the non-tree ceiling
c = annual(); c["mature_height_ft"] = [3, 6]; c["mature_spread_ft"] = [2, 4]
assert not any("mature_" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# footprint_inches: 4 in fine, 90 in absurd, 0 absurd
c = annual(); c["footprint_inches"] = 4
assert not any("footprint" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
c = annual(); c["footprint_inches"] = 90
assert any("footprint_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# null is not a violation
c = annual(); c["mature_height_ft"] = None; c["mature_spread_ft"] = None; c["footprint_inches"] = None
assert not any("mature_" in v or "footprint" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
print("PASS numeric_sanity plant-dimension bounds (PLA-465)")


# --- PLA-10 promote 1 (spec §10.1): planting_layout entries + the row mirror + rootstock spacing ----
def _e(**kw):
    e = {"id": "row-none", "arrangement": "row", "support": "none", "default": True,
         "in_row_inches": [12, 18], "row_spacing_inches": [30, 36]}
    e.update(kw)
    return e


def with_layout(base, *entries, **root):
    c = base(); c["planting_layout"] = list(entries); c.update(root)
    return c


# clean annual row entry + root mirror; clean watermelon hill at 96; clean blackberry rows at 120
assert numeric_sanity_violations(with_layout(annual, _e(), row_spacing_inches=[30, 36])) == []
assert numeric_sanity_violations(with_layout(annual, _e(id="hill-none", arrangement="hill",
    hill_spacing_inches=[96, 96], plants_per_hill=[2, 2], row_spacing_inches=[96, 96]))) == []
assert numeric_sanity_violations(with_layout(tree, _e(in_row_inches=[24, 48], row_spacing_inches=[120, 120]))) == []
# a string layout (the pre-promote form) and [] are skipped
assert numeric_sanity_violations(with_layout(annual)) == []
c = annual(); c["planting_layout"] = "block"
assert numeric_sanity_violations(c) == []

# in_row_inches: the spacing ceilings (72 non-tree, 360 tree)
c = with_layout(annual, _e(in_row_inches=[60, 96]))
assert any("planting_layout[0].in_row_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
assert not any("in_row_inches" in v for v in numeric_sanity_violations(with_layout(tree, _e(in_row_inches=[144, 300], row_spacing_inches=[300, 400]))))
assert any("in_row_inches" in v for v in numeric_sanity_violations(with_layout(tree, _e(in_row_inches=[144, 400], row_spacing_inches=[400, 400]))))
# hill_spacing_inches: 120 non-tree ceiling (the 96-inch watermelon hill fits, 144 does not)
c = with_layout(annual, _e(id="hill-none", arrangement="hill", hill_spacing_inches=[96, 144], plants_per_hill=[2, 2]))
assert any("hill_spacing_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# row_spacing_inches: 144 non-tree, 480 tree; on the entry AND the crop-root mirror
c = with_layout(annual, _e(row_spacing_inches=[150, 160]))
assert any("planting_layout[0].row_spacing_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
c = with_layout(annual, _e(), row_spacing_inches=[150, 160])
assert any(v.startswith("row_spacing_inches") for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
assert not any("row_spacing" in v for v in numeric_sanity_violations(with_layout(tree, _e(in_row_inches=[144, 180], row_spacing_inches=[240, 480]))))
assert any("row_spacing" in v for v in numeric_sanity_violations(with_layout(tree, _e(in_row_inches=[144, 180], row_spacing_inches=[240, 600]))))
# plants_per_hill: a count in [1, 10]
c = with_layout(annual, _e(id="hill-none", arrangement="hill", hill_spacing_inches=[30, 30], plants_per_hill=[4, 40]))
assert any("plants_per_hill" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# ordering on a ROW entry: rows can't be narrower than the plants in them
c = with_layout(annual, _e(in_row_inches=[36, 48], row_spacing_inches=[18, 24]))
assert any("ordering" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
# ... but a block or hill entry is not held to it, and a null row figure is skipped
assert not any("ordering" in v for v in numeric_sanity_violations(with_layout(annual, _e(id="block-none", arrangement="block", in_row_inches=[36, 48], row_spacing_inches=[18, 24]))))
assert not any("ordering" in v for v in numeric_sanity_violations(with_layout(annual, _e(row_spacing_inches=None))))
# rootstock_options[].spacing_inches: the tree bound, null skipped
c = tree(); c["rootstock_options"] = [{"name": "M9", "spacing_inches": [72, 96]}, {"name": "M26", "spacing_inches": None}]
assert numeric_sanity_violations(c) == [], numeric_sanity_violations(c)
c["rootstock_options"][0]["spacing_inches"] = [72, 400]
assert any("rootstock_options[0].spacing_inches" in v for v in numeric_sanity_violations(c)), numeric_sanity_violations(c)
print("PASS numeric_sanity planting_layout bounds (PLA-10)")
