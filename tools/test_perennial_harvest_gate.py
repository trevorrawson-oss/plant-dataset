#!/usr/bin/env python3
"""Tests for the herbaceous-perennial HARVEST-window floor (whole_crop_gate A48, artichoke GS arc).
Run: python3 tools/test_perennial_harvest_gate.py

WHY THIS GATE EXISTS. A47 (perennial_plant_out_gate) closed HALF of the asparagus defect: a
perennial certified with no `plant_out` on any cell, so the app could not say WHEN TO PLANT.
The other half was never closed -- asparagus also shipped with ZERO `harvest` strings across all
39 cells, so the app could not say WHEN TO EXPECT FOOD. Both fields are OPTIONAL, so both go
vacuous when absent; A47 only ever looked at one of them.

SCOPE -- archetype == 'herbaceous_perennial', deliberately narrower than A47's `perennial is True`.
Measured on canonical 34025ee3: the broader perennial scope would flood 195 cells across five
cut-as-needed perennial HERBS (thyme, rosemary, oregano, sage, lavender -- 39 cells each), which
have no discrete harvest window because you cut sprigs whenever you cook. Whether those should
carry a harvest string is a separate ruling, recorded and NOT decided here. On the archetype scope
the gate reports 0 for asparagus, so it ships enforcing a convention the archetype already meets.

EXEMPTIONS -- both mirror A47 exactly, for the same reasons:
  - empty calendar  -> skip (an unfilled shell cell is an admission state, not a defect)
  - unsuitable      -> skip (promising food where the crop will not grow is worse than silence)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from perennial_harvest_gate import perennial_harvest_violations

CAL = ["cold_pause", "cold_pause", "cold_pause", "harvest", "harvest", "harvest",
       "growing", "growing", "growing", "growing", "cold_pause", "cold_pause"]
ALL_GROWING = ["growing"] * 12


def crop(cells, archetype="herbaceous_perennial"):
    """Minimal crop carrying one region whose resolved_by_zone is `cells`."""
    return {"slug": "probe", "archetype": archetype, "perennial": True,
            "regions": {"northern_tier": {"resolved_by_zone": cells}}}


# 0. well-formed: a calendared cell that states its harvest -> clean
assert perennial_harvest_violations(crop({
    "4": {"suitability": "perennializes", "calendar": CAL,
          "plant_out": "Apr 10 - May 20 (dormant crowns, one-time planting)",
          "harvest": "Apr - Jun"}})) == []

# 1. OFF-ARCHETYPE NO-OP. A perennial herb with no harvest on any cell must stay untouched --
#    this is the thyme/rosemary/oregano/sage/lavender class (195 cells). If this assert ever
#    fails, the gate has widened into a flood.
assert perennial_harvest_violations(crop(
    {"4": {"suitability": "perennializes", "calendar": CAL, "plant_out": "Apr"}},
    archetype="culinary_herb")) == []

# 2. ADMISSION STATE: an unfilled shell cell (empty calendar) is skipped, harvest or not.
assert perennial_harvest_violations(crop({
    "4": {"suitability": None, "calendar": []}})) == []
assert perennial_harvest_violations(crop({
    "4": {"suitability": None, "calendar": [], "plant_out": None, "harvest": None}})) == []

# 3. UNSUITABLE is skipped -- an all-growing honesty-floor calendar with no harvest is correct,
#    because telling someone when to expect food from a crop that will not grow there is a lie.
assert perennial_harvest_violations(crop({
    "10": {"suitability": "unsuitable", "calendar": ALL_GROWING}})) == []

# 4. THE ASPARAGUS DEFECT: a calendared, non-unsuitable cell with NO harvest -> VIOLATION.
v = perennial_harvest_violations(crop({
    "4": {"suitability": "perennializes", "calendar": CAL,
          "plant_out": "Apr 10 - May 20 (dormant crowns, one-time planting)"}}))
assert len(v) == 1, v
assert "northern_tier.4" in v[0], v
assert "harvest" in v[0], v

# 5. marginal is covered too, and an EMPTY STRING is not a harvest window.
v = perennial_harvest_violations(crop({
    "9": {"suitability": "marginal", "calendar": CAL, "plant_out": "Jan", "harvest": ""}}))
assert len(v) == 1, v

# 6. a cell missing BOTH plant_out and harvest reports here for the harvest half only
#    (A47 owns the plant_out half -- the two gates are complementary, not redundant).
v = perennial_harvest_violations(crop({
    "4": {"suitability": "perennializes", "calendar": CAL}}))
assert len(v) == 1, v

# 7. several cells -> one violation each, deterministic order not assumed
v = perennial_harvest_violations(crop({
    "4": {"suitability": "perennializes", "calendar": CAL},
    "5": {"suitability": "marginal", "calendar": CAL},
    "6": {"suitability": "perennializes", "calendar": CAL, "harvest": "May - Jun"}}))
assert len(v) == 2, v

# 8. no regions / malformed shapes must not crash
assert perennial_harvest_violations({"slug": "x", "archetype": "herbaceous_perennial"}) == []
assert perennial_harvest_violations({"slug": "x", "archetype": "herbaceous_perennial",
                                     "regions": {"r": None}}) == []
assert perennial_harvest_violations({"slug": "x", "archetype": "herbaceous_perennial",
                                     "regions": {"r": {"resolved_by_zone": {"4": None}}}}) == []

# 9. REAL-DATA REGRESSION: asparagus, the only crop on the archetype today, must be clean --
#    the gate ships enforcing a convention the archetype already meets.
import json
_here = os.path.dirname(os.path.abspath(__file__))
_data = json.load(open(os.path.join(_here, "..", "crops_data_final.json"), encoding="utf-8"))
for c in _data["crops"]:
    if c.get("archetype") == "herbaceous_perennial":
        got = perennial_harvest_violations(c)
        assert got == [], f"{c.get('slug')}: {got}"

print("test_perennial_harvest_gate: all assertions passed")
