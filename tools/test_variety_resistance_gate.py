#!/usr/bin/env python3
"""Tests for variety_resistance_gate. Run: python3 tools/test_variety_resistance_gate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_resistance_gate import resistance_violations

def crop(varieties, pests=None, diseases=None):
    return {"slug": "apple",
            "pests": pests or [],
            "diseases": diseases or [{"id": "apple-scab"}, {"id": "fire-blight"}],
            "varieties": {"recommended": varieties}}

# clean: graded resistance referencing real disease ids -> no violations
assert resistance_violations(crop([{"name": "Liberty",
    "resistance": {"apple-scab": "immune", "fire-blight": "resistant"}}])) == []
# N/A branch: no resistance key -> valid
assert resistance_violations(crop([{"name": "Nodata"}])) == []
# N/A branch: empty resistance dict -> valid
assert resistance_violations(crop([{"name": "Empty", "resistance": {}}])) == []
# documented susceptible -> valid grade
assert resistance_violations(crop([{"name": "Honeycrisp",
    "resistance": {"apple-scab": "susceptible"}}])) == []
# referential covers pest ids too
assert resistance_violations(crop([{"name": "P",
    "resistance": {"woolly-apple-aphid": "resistant"}}],
    pests=[{"id": "woolly-apple-aphid"}])) == []
# RED: dangling id (typo)
assert any("is not a pest/disease id" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"appel-scab": "immune"}}])))
# RED: invalid grade
assert any("not in" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"apple-scab": "highly_resistant"}}])))
# RED: value not a string
assert any("must be a string" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"apple-scab": ["immune"]}}])))
# RED: resistance not a dict
assert any("must be a dict" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": ["apple-scab"]}])))
# RED: key not kebab
assert any("is not a kebab id" in v for v in resistance_violations(
    crop([{"name": "X", "resistance": {"Apple_Scab": "immune"}}])))

print("All variety_resistance_gate tests passed.")
