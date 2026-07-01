#!/usr/bin/env python3
"""Tests for the calendar-coherence NORMALIZER (docs/calendar-coherence-fix-design-2026-06-30.md).
Run: python3 tools/test_normalize_calendar_coherence.py

The normalizer surgically rewrites ONLY the cells the A37 gate flags:
  Bug 2 -- bridge a bridgeable one-month harvest-display hole by merging the two flanking spans
    (day precision + notes preserved; the calendar TOKEN is left untouched -- plant-row-quiet).
  Bug 1 -- replace an impossible `growing` token via the ordered 7-rule bucket map:
    1 in-window -> harvest | 2 start_indoors -> indoors | 3 succ cold_pause -> cold_pause |
    4 succ season_over -> season_over | 5 succ indoors -> cold_pause |
    6 succ plant & winter(Nov-Feb) -> cold_pause | 7 else -> season_over.
It must be a no-op on everything the gate does not flag, so gate(after) == 0 and the diff touches
exactly the target cells.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize_calendar_coherence import (
    replacement_token, bridge_harvest_string, normalize_crop,
)
from calendar_coherence_gate import calendar_coherence_violations


def _cell(calendar=None, harvest=None, start_indoors=None):
    c = {}
    if calendar is not None:
        c["calendar"] = calendar
    if harvest is not None:
        c["harvest"] = harvest
    if start_indoors is not None:
        c["start_indoors"] = start_indoors
    return c


COLD = "cold_pause"


# ================================================= Bug 2: bridge_harvest_string
# lettuce Nov (Trevor's example)
assert bridge_harvest_string("Sep - Oct, Dec - May", [11]) == "Sep - May"
# kale Feb (wrap span before the hole)
assert bridge_harvest_string("Mar - May, Oct - Jan", [2]) == "Oct - May"
# cabbage Jan (bare-month span 'Dec' before the hole)
assert bridge_harvest_string("Feb - May, Dec", [1]) == "Dec - May"
# DAY-PRECISION preserved
assert bridge_harvest_string("Mar 15 - May 15, Nov 15 - Jan 31", [2]) == "Nov 15 - May 15"
# collards 'Mar - Jun, Oct - Jan' Feb -> 'Oct - Jun'
assert bridge_harvest_string("Mar - Jun, Oct - Jan", [2]) == "Oct - Jun"
# no holes -> unchanged
assert bridge_harvest_string("Apr - May, Nov - Jan", []) == "Apr - May, Nov - Jan"


# ================================================= Bug 1: replacement_token (0-indexed month)
# rule 1: growing month IS in the harvest window -> harvest
cell = _cell(calendar=["harvest", "growing"] + [COLD] * 10, harvest="Jan - Feb")  # Feb in window
assert replacement_token(cell, 1) == "harvest", "in-window growing -> harvest"

# rule 2: growing month is a start_indoors month -> indoors
cell = _cell(calendar=["harvest", "growing"] + ["indoors"] + [COLD] * 9,
             harvest="Jan", start_indoors="Feb")
assert replacement_token(cell, 1) == "indoors", "start_indoors month -> indoors"

# rule 3: successor is cold_pause -> cold_pause  (zucchini se_gulf Dec)
cell = _cell(calendar=["harvest", "growing", COLD] + ["plant"] * 9, harvest="Jan")
assert replacement_token(cell, 1) == "cold_pause", "succ cold_pause -> cold_pause"

# rule 4: successor is season_over -> season_over
cell = _cell(calendar=["harvest", "growing", "season_over"] + ["plant"] * 9, harvest="Jan")
assert replacement_token(cell, 1) == "season_over", "succ season_over -> season_over"

# rule 5: successor is indoors -> cold_pause  (winter gap before an indoor seed-start)
cell = _cell(calendar=["harvest", "growing", "indoors"] + ["plant"] * 9, harvest="Jan")
assert replacement_token(cell, 1) == "cold_pause", "succ indoors -> cold_pause"

# rule 6: successor is plant AND month is winter (Nov-Feb) -> cold_pause  (cabbage ca_interior Jan)
# Dec harvest, Jan growing, Feb plant -> Jan (winter) -> cold_pause
cell = _cell(calendar=["growing", "plant"] + ["growing"] * 2 + ["harvest"] * 6 + ["harvest", "harvest"],
             harvest="May - Oct, Nov - Dec")
# simpler explicit fixture:
cell = _cell(calendar=[  # Jan grow, Feb plant, ... Dec harvest
    "growing", "plant", "plant", "plant", "plant", "plant",
    "plant", "plant", "plant", "plant", "harvest", "harvest"], harvest="Nov - Dec")
assert replacement_token(cell, 0) == "cold_pause", "succ plant + winter month -> cold_pause"

# rule 7a: successor is plant AND month is NOT winter (summer gap before a fall plant) -> season_over
cell = _cell(calendar=["plant"] * 6 + ["growing", "plant"] + ["harvest"] * 4, harvest="Sep - Dec")
# Jul (index 6) growing, prev Jun=plant? -> not impossible. Use a cleaner fixture:
cell = _cell(calendar=["harvest", "harvest", "harvest", "plant", "plant", "harvest",
                       "growing", "plant", "harvest", "harvest", "harvest", "harvest"],
             harvest="Jan - Mar, Jun, Sep - Dec")
# Jul (index 6): prev Jun=harvest -> impossible; succ Aug=plant; Jul not winter -> season_over
assert replacement_token(cell, 6) == "season_over", "succ plant + summer month -> season_over"

# rule 7b: successor is heat_pause (summer shoulder) -> season_over  (parsnip Mar)
cell = _cell(calendar=["harvest", "harvest", "growing", "heat_pause", "heat_pause", "heat_pause",
                       "heat_pause", "heat_pause", "plant", "plant", "growing", "harvest"],
             harvest="Dec - Feb")
assert replacement_token(cell, 2) == "season_over", "succ heat_pause shoulder -> season_over"


# ================================================= normalize_crop end-to-end
def _crop(cells):
    return {"slug": "t", "calendar_basis": "frost_anchored",
            "regions": {"r1": {"resolved_by_zone": cells}}}


# a crop carrying BOTH bugs -> after normalize, the A37 gate returns 0 for it, and the specific
# fixes landed.
crop = _crop({
    "9": _cell(calendar=["growing", "plant", "growing", "harvest", "harvest", "heat_pause",
                         "heat_pause", "heat_pause", "plant", "growing", "harvest", "harvest"],
               harvest="Apr - May, Nov - Dec"),                 # cabbage-like: Jan growing (bug1)
    "8": _cell(calendar=["plant"] * 12, harvest="Sep - Oct, Dec - May"),  # lettuce-like: Nov hole (bug2)
})
changes = normalize_crop(crop)
z9 = crop["regions"]["r1"]["resolved_by_zone"]["9"]
z8 = crop["regions"]["r1"]["resolved_by_zone"]["8"]
assert z9["calendar"][0] == "cold_pause", f"Jan growing should become cold_pause: {z9['calendar']}"
assert z8["harvest"] == "Sep - May", f"Nov hole should bridge: {z8['harvest']}"
assert calendar_coherence_violations(crop) == [], \
    f"after normalize the gate must be clean: {calendar_coherence_violations(crop)}"
assert len(changes) == 2, f"exactly two changes (one token, one harvest): {changes}"

# mild-coastal override (Trevor ruling, 2026-06-30): a `cold_pause` replacement on
# ca_north_coast/ca_south_coast reads as "waiting", not "cold-stopped" -> re-rule to season_over.
# Jan growing (winter gap: Dec harvest -> Jan growing -> Feb plant) normally -> cold_pause (rule 6).
_mildcal = ["growing", "plant", "plant", "plant", "plant", "plant",
            "plant", "plant", "plant", "plant", "plant", "harvest"]
mild = {"slug": "t", "calendar_basis": "frost_anchored",
        "regions": {"ca_north_coast": {"resolved_by_zone": {"9": _cell(calendar=list(_mildcal), harvest="Dec")}}}}
normalize_crop(mild)
assert mild["regions"]["ca_north_coast"]["resolved_by_zone"]["9"]["calendar"][0] == "season_over", \
    "mild-coastal cold_pause (rule 6) must be re-ruled to season_over"
# the SAME pattern in a non-mild region stays cold_pause (proves it's the region, not the rule)
inland = {"slug": "t", "calendar_basis": "frost_anchored",
          "regions": {"ca_interior": {"resolved_by_zone": {"9": _cell(calendar=list(_mildcal), harvest="Dec")}}}}
normalize_crop(inland)
assert inland["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"][0] == "cold_pause", \
    "non-mild-coast winter gap stays cold_pause"

# a CLEAN crop -> no changes (no-op)
clean = _crop({"9": _cell(calendar=["plant", "growing", "harvest"] + [COLD] * 9, harvest="Mar")})
assert normalize_crop(clean) == [], "a clean crop must not be touched"

print("normalize_calendar_coherence: all tests passed")
