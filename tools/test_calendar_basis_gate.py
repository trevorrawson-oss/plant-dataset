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

# 0. each of the 7 known bases -> clean
for b in VALID_CALENDAR_BASES:
    assert calendar_basis_violations({"slug": "x", "calendar_basis": b}) == [], b

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
    assert len(cert) == 18, f"expected 18 certified anchors, found {len(cert)}"
    fp = [(c["slug"], calendar_basis_violations(c)) for c in cert if calendar_basis_violations(c)]
    assert fp == [], f"calendar_basis FP on certified anchors: {fp}"
    print(f"  real data: 0 FP across {len(cert)} certified anchors: PASS")

print("calendar_basis_gate: all tests passed")
