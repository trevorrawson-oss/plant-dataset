#!/usr/bin/env python3
"""Tests for the chill-delivered refactor gate (Phase A, audit F2). Run:
python3 tools/test_chill_gate.py

THE BUG (audit F2): chill_hours_delivered is a CLIMATE value (how much chill a
region+zone banks) but it was authored PER CROP, so peach/apple/blueberry disagree
at the same region+zone (20/20 cells), and blueberry stored it as a STRING so its
gauge never rendered. THE FIX: one shared, crop-invariant per-region/per-zone table
`region_chill_delivered` (normalized to [lo,hi]); the per-crop field is stripped;
chill-REQUIRED stays per-variety. This gate makes the conflation un-re-introducible:

  chill_delivered_absent_violations(crop): a per-crop cert check -- NO crop may carry
    chill_hours_delivered anywhere (region rollup or resolved cell). With no per-crop
    overrides + one shared table, "crop-invariant per region+zone" holds by construction.

  chill_table_violations(data): the dataset-level shape check -- region_chill_delivered
    is a dict of region -> {zone -> [lo, hi]} where lo,hi are numbers and 0 <= lo <= hi.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chill_gate import chill_delivered_absent_violations, chill_table_violations


# ── chill_delivered_absent_violations (per-crop) ──────────────────────────────
def clean_tree():
    return {"slug": "peach", "regions": {
        "northern_tier": {"resolved_by_zone": {
            "3": {"suitability": "fruits_reliably", "calendar": ["dormant"]}}}}}


# 0. a crop with NO chill_hours_delivered anywhere -> clean
assert chill_delivered_absent_violations(clean_tree()) == [], chill_delivered_absent_violations(clean_tree())

# 1. a region-rollup chill_hours_delivered -> violation
c = clean_tree(); c["regions"]["northern_tier"]["chill_hours_delivered"] = [700, 1600]
assert any("northern_tier" in v and "chill_hours_delivered" in v for v in chill_delivered_absent_violations(c)), \
    chill_delivered_absent_violations(c)

# 2. a per-cell chill_hours_delivered -> violation
c = clean_tree(); c["regions"]["northern_tier"]["resolved_by_zone"]["3"]["chill_hours_delivered"] = [1200, 1500]
assert any("northern_tier" in v and "3" in v for v in chill_delivered_absent_violations(c)), \
    chill_delivered_absent_violations(c)

# 3. a string-typed cell value (blueberry's old shape) -> still a violation (it must be GONE)
c = clean_tree(); c["regions"]["northern_tier"]["resolved_by_zone"]["3"]["chill_hours_delivered"] = "1200 or more"
assert chill_delivered_absent_violations(c), chill_delivered_absent_violations(c)

# 4. an annual crop with no regions chill at all -> clean (no-op)
assert chill_delivered_absent_violations({"slug": "carrot", "regions": {
    "se_gulf": {"resolved_by_zone": {"9": {"plant_out": "Mar"}}}}}) == [], "annual crop must be clean"


# ── chill_table_violations (dataset-level) ────────────────────────────────────
def good_table():
    return {"region_chill_delivered": {
        "northern_tier": {"3": [1100, 1600], "7": [700, 1100]},
        "hawaii_tropical": {"11": [0, 150]}}}


# 5. a well-formed table -> clean
assert chill_table_violations(good_table()) == [], chill_table_violations(good_table())

# 6. the table missing entirely -> violation (the shared source of truth must exist)
assert any("region_chill_delivered" in v for v in chill_table_violations({})), chill_table_violations({})

# 7. a region whose value is not a dict -> violation
d = good_table(); d["region_chill_delivered"]["northern_tier"] = [1100, 1600]
assert any("northern_tier" in v for v in chill_table_violations(d)), chill_table_violations(d)

# 8. a cell that is not a 2-element list -> violation
d = good_table(); d["region_chill_delivered"]["northern_tier"]["3"] = [1100]
assert any("northern_tier" in v and "3" in v for v in chill_table_violations(d)), chill_table_violations(d)

# 9. lo > hi -> violation
d = good_table(); d["region_chill_delivered"]["northern_tier"]["3"] = [1600, 1100]
assert any("northern_tier" in v and "3" in v and ("lo" in v.lower() or "<=" in v or "order" in v.lower())
           for v in chill_table_violations(d)), chill_table_violations(d)

# 10. a non-numeric bound (the string bug, re-introduced at the table level) -> violation
d = good_table(); d["region_chill_delivered"]["hawaii_tropical"]["11"] = ["0", "150"]
assert any("hawaii_tropical" in v and "11" in v for v in chill_table_violations(d)), chill_table_violations(d)

# 11. a negative lower bound -> violation
d = good_table(); d["region_chill_delivered"]["hawaii_tropical"]["11"] = [-50, 150]
assert any("hawaii_tropical" in v and "11" in v for v in chill_table_violations(d)), chill_table_violations(d)

print("chill_gate: all tests passed")
