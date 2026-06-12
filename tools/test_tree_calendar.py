#!/usr/bin/env python3
"""Tests for the tree-calendar generator + coherence gate (tools/tree_calendar.py).

The tree `calendar[]` is DERIVED data: a pure function of the cell's bloom + harvest
DISPLAY windows. Hand-authoring it (Step-4 convention) let it drift from those fields
(apple Step 5: 5 bloom + 11 harvest mismatches). The generator makes it computed; the
gate makes drift impossible to ship.

Sequence rule (validated against claude.ai's hand-authored apple corrections + ca_desert z10):
  prune = month before bloom; bloom = bloom-open month; growing = bloom+1..harvest_start-1;
  harvest = the harvest display span; care = month after harvest end; dormant = the rest.

Run: python3 tools/test_tree_calendar.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import derive_tree_calendar, derive_evergreen_calendar, tree_calendar_violations

D, P, B, G, H, C = "dormant", "prune", "bloom", "growing", "harvest", "care"

# 1. reproduces claude.ai's corrected northern_tier z3 (cold, late bloom)
assert derive_tree_calendar("May 5 - May 25", "Sep - Oct") == \
    [D, D, D, P, B, G, G, G, H, H, C, D], derive_tree_calendar("May 5 - May 25", "Sep - Oct")

# 2. reproduces a warm early-bloom cell (ca_south_coast z10): bloom Feb, harvest Jun-Aug
assert derive_tree_calendar("Feb 25 - Mar 15", "Jun - Aug") == \
    [P, B, G, G, G, H, H, H, C, D, D, D], derive_tree_calendar("Feb 25 - Mar 15", "Jun - Aug")

# 3. single-month harvest window
assert derive_tree_calendar("Apr 1 - Apr 20", "Aug") == \
    [D, D, P, B, G, G, G, H, C, D, D, D], derive_tree_calendar("Apr 1 - Apr 20", "Aug")

# 4. empty / unparseable inputs -> None (caller decides; a no-fruit cell carries no calendar)
assert derive_tree_calendar("", "Jun - Aug") is None
assert derive_tree_calendar("Feb 25 - Mar 15", "") is None
assert derive_tree_calendar(None, None) is None

# --- the gate ---
def perennial_crop(cells):
    """cells: list of (region, zone, bloom, harvest, calendar)."""
    regions = {}
    for rid, z, bloom, harvest, cal in cells:
        regions.setdefault(rid, {"resolved_by_zone": {}})
        regions[rid]["resolved_by_zone"][z] = {
            "bloom": bloom, "harvest": harvest, "calendar": cal}
    return {"slug": "x", "calendar_basis": "perennial_chill_gated", "regions": regions}

# 5. a coherent cell -> no violation
coherent = derive_tree_calendar("May 5 - May 25", "Sep - Oct")
assert tree_calendar_violations(perennial_crop([("nt", "3", "May 5 - May 25", "Sep - Oct", coherent)])) == []

# 6. a harvest-token-early cell (the apple Step-5 bug) -> violation naming the cell
bad = [D, D, D, P, B, G, H, H, H, C, D, D]  # harvest Jul-Sep but field says Aug-Oct
viol = tree_calendar_violations(perennial_crop([("nt", "6", "Apr 15 - May 5", "Aug - Oct", bad)]))
assert any("nt" in v and "6" in v for v in viol), viol

# 7. an empty-calendar cell (no-fruit / unsuitable) is SKIPPED (A3 owns emptiness, not this gate)
assert tree_calendar_violations(perennial_crop([("fl", "10", "n/a", "n/a", [])])) == []

# 8. annual crop (not perennial) -> no-op
assert tree_calendar_violations({"slug": "carrot", "calendar_basis": "frost_anchored",
                                 "regions": {"x": {"resolved_by_zone": {"8": {"calendar": [D]}}}}}) == []

# 9. non-empty calendar with unparseable dates -> violation (cannot verify a calendar with no dates)
viol9 = tree_calendar_violations(perennial_crop([("nt", "3", "", "", [B] * 12)]))
assert any("nt" in v and "3" in v for v in viol9), viol9

# ============ EVERGREEN calendar (no dormancy, growing filler, year-wrap) ============
# An evergreen (citrus) never goes dormant: the off-season is `growing`, never `dormant`,
# and the bloom->harvest span commonly WRAPS the year (bloom spring, harvest the following
# winter). bloom + harvest are the dated facts; everything else is growing.
# tree_region_model_evergreen_amendment_v1_0 section 1.

# E1. lemon wrap: bloom Mar-Apr, harvest Nov-Feb -> harvest straddles the year, no dormant
assert derive_evergreen_calendar("Mar - Apr", "Nov - Feb") == \
    [H, H, B, B, G, G, G, G, G, G, H, H], derive_evergreen_calendar("Mar - Apr", "Nov - Feb")

# E2. single-month bloom + harvest -> the entire off-season is growing (zero dormant tokens)
ev = derive_evergreen_calendar("Apr", "Oct")
assert ev == [G, G, G, B, G, G, G, G, G, H, G, G], ev
assert D not in ev, f"evergreen calendar must never carry a dormant token: {ev}"

# E3. empty / unparseable -> None (a no-fruit evergreen cell carries no calendar)
assert derive_evergreen_calendar("", "Nov - Feb") is None
assert derive_evergreen_calendar(None, None) is None

# --- the A4 gate recognizes the evergreen basis + uses the evergreen derivation ---
def evergreen_crop(cells):
    regions = {}
    for rid, z, bloom, harvest, cal in cells:
        regions.setdefault(rid, {"resolved_by_zone": {}})
        regions[rid]["resolved_by_zone"][z] = {"bloom": bloom, "harvest": harvest, "calendar": cal}
    return {"slug": "lemon", "calendar_basis": "perennial_evergreen", "regions": regions}

# E4. a coherent evergreen cell -> no violation
co = derive_evergreen_calendar("Mar - Apr", "Nov - Feb")
assert tree_calendar_violations(evergreen_crop([("ca", "10", "Mar - Apr", "Nov - Feb", co)])) == []

# E5. an evergreen cell whose stored calendar carries a (deciduous) dormant token it can't
# derive -> incoherent -> violation naming the cell
baddec = [D, D, B, B, G, G, G, G, G, G, H, H]  # would-be evergreen but Jan/Feb are dormant not harvest
viol5 = tree_calendar_violations(evergreen_crop([("ca", "10", "Mar - Apr", "Nov - Feb", baddec)]))
assert any("ca" in v and "10" in v for v in viol5), viol5

# E6. an empty evergreen calendar (no-fruit cell) is skipped (A3 owns emptiness)
assert tree_calendar_violations(evergreen_crop([("nt", "7", "n/a", "n/a", [])])) == []

# E7. a year_round:true cell (genuinely pauseless tropical, e.g. Hawaii citrus) is SKIPPED by
# A4: its calendar is a DECLARED outcome (the locked year_round pattern), not date-derived, so
# coherence-checking it against unparseable "Year-round" strings is wrong. (A3 still requires the
# fruits_reliably cell to carry a non-empty calendar -- satisfied by the declared harvest fill.)
yr = {"slug": "lemon", "calendar_basis": "perennial_evergreen", "regions": {
    "hawaii": {"resolved_by_zone": {"11": {
        "year_round": True,
        "bloom": "Year-round (peaks vary)", "harvest": "Year-round (continuous)",
        "calendar": ["harvest"] * 12}}}}}
assert tree_calendar_violations(yr) == [], tree_calendar_violations(yr)
# but a NON-year_round cell with the same unparseable dates is still a violation (regression guard)
nyr = {"slug": "lemon", "calendar_basis": "perennial_evergreen", "regions": {
    "hawaii": {"resolved_by_zone": {"11": {
        "bloom": "Year-round", "harvest": "Year-round", "calendar": ["harvest"] * 12}}}}}
assert any("hawaii" in v and "11" in v for v in tree_calendar_violations(nyr)), tree_calendar_violations(nyr)

print("PASS tree_calendar")
