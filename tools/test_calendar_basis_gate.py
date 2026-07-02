#!/usr/bin/env python3
"""Tests for the calendar_basis enum guard (whole_crop_gate A30, incognito-redteam C1).
Run: python3 tools/test_calendar_basis_gate.py

WHAT IT ARMS AGAINST: `calendar_basis` is THE dispatch key -- every calendar gate (A3/A4
perennial, A5/A24/A28 annual, A9 photoperiod off frost_anchored, A10/A11 berries_herbaceous,
A13/A14 woody_ornamental, A15/A16 berries_woody) no-ops itself off a string-equality check
against this field, and NOTHING validated the field. A typo ("frost_anchored "), a case slip
("Frost_anchored"), a synonym ("annual"), or a novel value ("generic_placeholder") silently
disabled the crop's whole calendar layer while the suite still printed GATE: PASS. This guard
asserts the value is one of the 7 known bases; an unknown one is a hard cert violation.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calendar_basis_gate import calendar_basis_violations, VALID_CALENDAR_BASES

# 0. each of the 7 known bases -> clean (non_seasonal_indoor must carry zone_independent:true per D1)
for b in VALID_CALENDAR_BASES:
    crop = {"slug": "x", "calendar_basis": b}
    if b == "non_seasonal_indoor":
        crop["zone_independent"] = True
    assert calendar_basis_violations(crop) == [], b

# 1. the exact set is the 7 archetype bases (no accidental drift)
assert VALID_CALENDAR_BASES == {
    "frost_anchored", "perennial_chill_gated", "perennial_evergreen", "perennial_herbaceous",
    "berries_woody", "perennial_woody_ornamental", "non_seasonal_indoor",
}, sorted(VALID_CALENDAR_BASES)

# 2. trailing-space typo -> violation (the audit's self-verified basil injection)
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored "}), \
    "trailing-space basis must be flagged"

# 3. case slip -> violation
assert calendar_basis_violations({"slug": "x", "calendar_basis": "Frost_anchored"}), \
    "case-slip basis must be flagged"

# 4. plausible synonym -> violation
assert calendar_basis_violations({"slug": "x", "calendar_basis": "annual"}), \
    "synonym basis must be flagged"

# 5. novel/placeholder value (the live heirloom-tomato shell) -> violation
assert calendar_basis_violations({"slug": "x", "calendar_basis": "generic_placeholder"}), \
    "generic_placeholder must be flagged (a shell must not certify on this dimension)"

# 6. missing / null calendar_basis -> violation
assert calendar_basis_violations({"slug": "x"}), "missing calendar_basis must be flagged"
assert calendar_basis_violations({"slug": "x", "calendar_basis": None}), "null basis must be flagged"

# 7. the violation message names the offending value
v = calendar_basis_violations({"slug": "x", "calendar_basis": "annual"})
assert any("annual" in m for m in v), v

# 8. REAL DATA: every certified anchor carries a valid basis -> 0 violations (zero false positives)
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    data = json.load(open(_path, encoding="utf-8"))
    cert = [c for c in data["crops"]
            if c.get("verification_status", {}).get("status") == "verified_gs_arc"]
    assert len(cert) >= 18, f"certified set unexpectedly small (>=18 anchors), found {len(cert)}"
    fp = [(c["slug"], calendar_basis_violations(c)) for c in cert if calendar_basis_violations(c)]
    assert fp == [], f"calendar_basis FP on certified anchors: {fp}"
    print(f"  real data: 0 FP across {len(cert)} certified anchors: PASS")

# ---- re-audit #2 D1/D8 (2026-06-28): the dispatch guard must validate the OTHER dispatch fields
#      (zone_independent, archetype) against calendar_basis, not just the one key. ----

# 9. D1: zone_independent:true on a non-indoor basis -> violation (the master kill-switch)
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "zone_independent": True}), "zone_independent on a non-indoor basis must flag"
# and the inverse: a non_seasonal_indoor crop that is NOT zone_independent -> violation
assert calendar_basis_violations({"slug": "x", "calendar_basis": "non_seasonal_indoor",
                                  "zone_independent": None}), "indoor crop must be zone_independent"
# the consistent pairs are clean
assert calendar_basis_violations({"slug": "x", "calendar_basis": "non_seasonal_indoor",
                                  "zone_independent": True}) == [], "indoor + zi=True is clean"
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "zone_independent": None}) == [], "non-indoor + zi=None is clean"
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "zone_independent": False}) == [], "zi=False is not 'true'"

# 10. D8: a known archetype that maps to a DIFFERENT basis -> violation
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "archetype": "deciduous_fruit_tree"}), "archetype/basis mismatch must flag"
# a NOVEL archetype -> violation (unknown archetype, like a novel basis)
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "archetype": "spaceship"}), "novel archetype must flag"
# the matching archetype is clean; a null archetype is skipped (not over-flagged)
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "archetype": "warm_season_fruiting"}) == [], "matching archetype clean"
assert calendar_basis_violations({"slug": "x", "calendar_basis": "frost_anchored",
                                  "archetype": None}) == [], "null archetype skipped"

# 11. REAL DATA still 0 FP after D1/D8 (the 18 carry consistent zone_independent + archetype)
if os.path.exists(_path):
    fp2 = [(c["slug"], calendar_basis_violations(c)) for c in cert if calendar_basis_violations(c)]
    assert fp2 == [], f"D1/D8 FP on certified anchors: {fp2}"

print("calendar_basis_gate: all tests passed")
