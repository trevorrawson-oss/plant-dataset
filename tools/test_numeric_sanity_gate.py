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

# 10. REAL DATA: every certified anchor is numerically sane (0 false positives)
fp = [(c["slug"], numeric_sanity_violations(c)) for c in _cert if numeric_sanity_violations(c)]
assert fp == [], f"numeric-sanity FP on certified anchors: {fp}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified anchors: PASS")

print("numeric_sanity_gate: all tests passed")
