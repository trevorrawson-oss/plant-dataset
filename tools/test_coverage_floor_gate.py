#!/usr/bin/env python3
"""Tests for the coverage-floor cert gates (whole_crop_gate A31 region roster + A32 calendar
presence; incognito-redteam C3 + C4). Run: python3 tools/test_coverage_floor_gate.py

C3 (A31 region_roster_violations): a non-indoor crop ships with regions:{} (zero coverage) or
a single region and PASSES -- "10 regions" was enforced nowhere. The 10-region roster is the
coverage floor; an indoor / zone_independent crop legitimately collapses regions to {}.

C4 (A32 calendar_presence_violations): delete calendar[] on every filled cell of a frost_anchored
annual (keep plantings + region_notes) and it certifies -- A5/A24/A28 all `continue` on an absent
calendar, A2 checks plantings not the calendar. A frost_anchored resolved cell must carry a
non-empty calendar (the page's core deliverable). Trees/indoor are out of scope (tree empty cells
are governed by A3; indoor has no cells).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage_floor_gate import (region_roster_violations, calendar_presence_violations,
                                  CANONICAL_REGIONS)

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]


def _full_regions():
    return {r: {"plantings": [{"track": "succession"}], "resolved_by_zone": {"8": {"calendar": ["growing"]}}}
            for r in CANONICAL_REGIONS}


# ============================== C3 -- region roster floor (A31) ==============================
# 0. the canonical roster is the 10-region model
assert CANONICAL_REGIONS == {
    "ca_desert", "ca_interior", "ca_north_coast", "ca_south_coast", "fl_peninsula",
    "hawaii_tropical", "low_desert_az", "northern_tier", "se_gulf", "warm_arid",
}, sorted(CANONICAL_REGIONS)

# 1. a non-indoor crop with the full roster -> clean
ok = {"slug": "x", "calendar_basis": "frost_anchored", "regions": _full_regions()}
assert region_roster_violations(ok) == [], region_roster_violations(ok)

# 2. regions:{} on a non-indoor crop (the audit injection) -> violation
bad = {"slug": "x", "calendar_basis": "frost_anchored", "regions": {}}
assert region_roster_violations(bad), "empty regions on a non-indoor crop must be flagged"

# 3. a SINGLE region (partial roster) -> violation, names what's missing
one = {"slug": "x", "calendar_basis": "frost_anchored",
       "regions": {"se_gulf": {"plantings": [{"track": "succession"}]}}}
v = region_roster_violations(one)
assert v and "missing" in v[0].lower(), v

# 4. an UNKNOWN region key (typo) -> violation
typo = {"slug": "x", "calendar_basis": "frost_anchored", "regions": dict(_full_regions(), mars={})}
assert region_roster_violations(typo), "an unknown region key must be flagged"

# 5. indoor crop (non_seasonal_indoor) collapses regions to {} -> clean (legit N/A)
indoor = {"slug": "microgreens-mix", "calendar_basis": "non_seasonal_indoor", "regions": {}}
assert region_roster_violations(indoor) == [], region_roster_violations(indoor)
# also via zone_independent flag
zi = {"slug": "x", "zone_independent": True, "regions": {}}
assert region_roster_violations(zi) == [], region_roster_violations(zi)

# 6. an indoor crop that ANOMALOUSLY carries regions -> violation (off-model)
indoor_regions = {"slug": "x", "calendar_basis": "non_seasonal_indoor", "regions": _full_regions()}
assert region_roster_violations(indoor_regions), "indoor crop with non-empty regions is off-model"

# 7. REAL DATA: every certified anchor passes the roster floor (0 FP)
fp = [(c["slug"], region_roster_violations(c)) for c in _cert if region_roster_violations(c)]
assert fp == [], f"C3 region-roster FP on certified anchors: {fp}"

# ============================ C4 -- calendar presence floor (A32) ============================
def _annual():
    return {"slug": "x", "calendar_basis": "frost_anchored", "regions": {
        "se_gulf": {"plantings": [{"track": "succession"}], "resolved_by_zone": {
            "8": {"calendar": ["growing", "harvest"]}, "9": {"calendar": ["growing"]}}},
        "northern_tier": {"plantings": [{"track": "succession"}], "resolved_by_zone": {
            "3": {"calendar": ["cold_pause", "growing"]}}}}}


# 8. a frost_anchored crop with calendars on every cell -> clean
assert calendar_presence_violations(_annual()) == [], calendar_presence_violations(_annual())

# 9. the audit injection: a filled cell whose calendar[] is EMPTY -> violation
c = _annual(); c["regions"]["se_gulf"]["resolved_by_zone"]["8"]["calendar"] = []
assert any("se_gulf" in v and "8" in v for v in calendar_presence_violations(c)), calendar_presence_violations(c)

# 10. a filled cell whose calendar key is ABSENT entirely -> violation
c = _annual(); del c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["calendar"]
assert any("se_gulf" in v and "9" in v for v in calendar_presence_violations(c)), calendar_presence_violations(c)

# 11. NON-frost_anchored is OUT OF SCOPE: a tree (perennial) with empty cells is NOT flagged here
#     (A3 governs tree empty cells -- unsuitable / chill-limited cells are legitimately empty).
tree = {"slug": "peach", "calendar_basis": "perennial_chill_gated", "regions": {
    "northern_tier": {"resolved_by_zone": {"3": {"suitability": "unsuitable", "calendar": []}}}}}
assert calendar_presence_violations(tree) == [], calendar_presence_violations(tree)

# 12. indoor crop (no regions) -> no-op
assert calendar_presence_violations({"slug": "x", "calendar_basis": "non_seasonal_indoor", "regions": {}}) == []

# 13. REAL DATA: every certified anchor passes the calendar-presence floor (0 FP)
fp = [(c["slug"], calendar_presence_violations(c)) for c in _cert if calendar_presence_violations(c)]
assert fp == [], f"C4 calendar-presence FP on certified anchors: {fp}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified anchors (both floors): PASS")

print("coverage_floor_gate: all tests passed")
