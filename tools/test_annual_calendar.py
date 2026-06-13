#!/usr/bin/env python3
"""Tests for the annual calendar deriver (Step 5.5). Run from repo root:
    python3 tools/test_annual_calendar.py

Ground truth = the certified annuals' resolved cells. The deriver must reproduce
a clean cold-cycle calendar (carrot northern_tier z5) EXACTLY from its windows,
and produce coherent calendars for basil's frost-anchored summer-season cells.

SCOPE (basil archetype + cold multi-cycle): frost-anchored annuals whose harvest
falls inside the frost-free season (summer-centered), explicit `plant_out` OR a
direct-sow first/last-plant envelope, cold_pause winters, year_round cells, and
honoring a DECLARED heat_pause. OUT OF SCOPE for now (documented, not basil):
winter-wrapping harvest (carrot se_gulf "Sep - May") + lettuce-style heat-inverted
two-cool-season cells -- those need the cycle-segmentation extension.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import annual_calendar as ac

# ---------- month parser ----------
assert ac.parse_months("Jun - Sep") == {6, 7, 8, 9}, ac.parse_months("Jun - Sep")
assert ac.parse_months("May - Aug, Oct - Nov") == {5, 6, 7, 8, 10, 11}
assert ac.parse_months("May 8 - May 22") == {5}
assert ac.parse_months("Mar 27 - Apr 10") == {3, 4}
assert ac.parse_months("Mar 15 - Apr 15; Aug 15 - Sep 15") == {3, 4, 8, 9}
assert ac.parse_months("Sep - May") == {9, 10, 11, 12, 1, 2, 3, 4, 5}   # wrap
assert ac.parse_months("Year round") == set(range(1, 13))
assert ac.parse_months(None) == set()
print("  month parser: PASS")

# ---------- GROUND TRUTH: carrot northern_tier z5 (direct-sow envelope, double cycle) ----------
# plant_out None -> plant inferred from first/last_plant envelope MINUS harvest months.
carrot_nt5 = {
    "plant_out": None, "start_indoors": None,
    "first_plant_date": "Mar 25", "last_plant_date": "Aug 17",
    "harvest": "May - Jun, Oct - Nov", "harvest_start": "May 24", "harvest_end": "Nov 14",
}
EXPECT_CARROT_NT5 = ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                     "plant", "plant", "growing", "harvest", "harvest", "cold_pause"]
got = ac.derive_annual_calendar(carrot_nt5, calendar_basis="frost_anchored")
assert got == EXPECT_CARROT_NT5, ("carrot NT z5 regression", got)
print("  carrot northern_tier z5 reproduced EXACTLY: PASS")

# ---------- basil northern_tier z5 (explicit plant_out + start_indoors, single summer) ----------
basil_nt5 = {
    "start_indoors": "Mar 27 - Apr 10", "plant_out": "May 8 - May 22",
    "harvest": "Jun - Sep", "harvest_start": "Jun 7", "harvest_end": "Sep 26",
    "first_plant_date": "May 8", "last_plant_date": "May 22",
}
EXPECT_BASIL_NT5 = ["cold_pause", "cold_pause", "indoors", "indoors", "plant", "harvest",
                    "harvest", "harvest", "harvest", "cold_pause", "cold_pause", "cold_pause"]
got = ac.derive_annual_calendar(basil_nt5, calendar_basis="frost_anchored")
assert got == EXPECT_BASIL_NT5, ("basil NT z5", got)
print("  basil northern_tier z5 (explicit plant_out + indoors): PASS")

# ---------- basil se_gulf z9 (double warm-season arm; plant overlaps harvest in Aug) ----------
# plant_out explicit -> authoritative; plant > harvest in the Aug overlap.
basil_seg9 = {
    "plant_out": "Mar 15 - Apr 15; Aug 15 - Sep 15", "start_indoors": None,
    "harvest": "May - Aug, Oct - Nov", "harvest_start": "May 1", "harvest_end": "Nov 15",
    "first_plant_date": "Mar 15", "last_plant_date": "Sep 15",
}
EXPECT_BASIL_SEG9 = ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                     "harvest", "plant", "plant", "harvest", "harvest", "cold_pause"]
got = ac.derive_annual_calendar(basil_seg9, calendar_basis="frost_anchored")
assert got == EXPECT_BASIL_SEG9, ("basil se_gulf z9", got)
print("  basil se_gulf z9 (double arm, plant>harvest overlap): PASS")

# ---------- near-year-round cell with a SUMMER lull (fl_peninsula z11): no cold_pause ----------
# harvest wraps Oct->Jan, so January is ACTIVE -> there is NO winter off-season. The Jul/Aug
# inactive gap is a SUMMER lull -> "growing", never "cold_pause" (a season-span model wrongly
# marks it cold_pause). cold_pause is anchored at deep winter (January), not a contiguous span.
fl_z11 = {
    "start_indoors": "Dec 15 - Feb 15", "plant_out": "Feb 1 - Apr 30; Sep 1 - Nov 15",
    "harvest": "Mar - Jun, Oct - Jan", "harvest_start": "Mar 15", "harvest_end": "Jan 15",
    "first_plant_date": "Feb 1", "last_plant_date": "Nov 15",
}
EXPECT_FL_Z11 = ["harvest", "plant", "plant", "plant", "harvest", "harvest",
                 "growing", "growing", "plant", "plant", "plant", "harvest"]
got = ac.derive_annual_calendar(fl_z11, calendar_basis="frost_anchored")
assert "cold_pause" not in got, ("no cold_pause in a January-active near-year-round cell", got)
assert got == EXPECT_FL_Z11, ("fl_peninsula z11 near-year-round", got)
print("  fl_peninsula z11 (near-year-round, summer lull -> growing): PASS")

# ---------- year_round cell (hawaii) -> continuous, no pause ----------
hawaii = {"plant_out": "Year round", "year_round": True,
          "harvest": "Year round", "harvest_start": None, "harvest_end": None}
got = ac.derive_annual_calendar(hawaii, calendar_basis="frost_anchored")
assert got == ["growing"] * 12, ("hawaii year_round", got)
print("  hawaii year_round (continuous): PASS")

# ---------- declared heat_pause overrides (general-case honoring; basil has none) ----------
hp = {"plant_out": "Mar - Apr", "start_indoors": None, "harvest": "May - Sep",
      "harvest_start": "May 1", "harvest_end": "Sep 30", "heat_pause_months": {7, 8}}
got = ac.derive_annual_calendar(hp, calendar_basis="frost_anchored")
assert got[6] == "heat_pause" and got[7] == "heat_pause", ("heat_pause override", got)
assert got[4] == "harvest", got            # May still harvest
print("  declared heat_pause override: PASS")

print("PASS annual_calendar deriver")
