#!/usr/bin/env python3
"""Tests for the herbaceous_perennial structural cert branch (asparagus GS arc, 2026-07-23).
Run: python3 tools/test_herbaceous_perennial_gate.py

Invariants (docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md):
  - fires ONLY for archetype == 'herbaceous_perennial' (no-op otherwise -- keeps the 119 certified,
    incl. the herbaceous herbs chives/mint on culinary_herb, untouched).
  - perennial true; lifecycle in {perennial, permanent}; succession_policy.suitable False + reason;
    establishment fields sane (years_to_first_harvest non-empty min>=1, years_to_full_production
    non-empty, productive_lifespan_years positive int); no succession/second_planting planting
    tracks; per filled cell: suitability in enum + a marginal/unsuitable cell carries a reason note
    + a non-empty calendar (A32 honesty floor); rotation present.
  - a cell with suitability null AND empty calendar is the admission state (skip).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from herbaceous_perennial_gate import herbaceous_perennial_violations, SUITABILITY_ENUM

def well_formed():
    """Minimal valid herbaceous_perennial crop: one thriving + one unsuitable region cell."""
    return {
        "slug": "asparagus-mini", "archetype": "herbaceous_perennial",
        "calendar_basis": "frost_anchored", "perennial": True, "lifecycle": "perennial",
        "succession_policy": {"suitable": False, "reason_seasoned": "A permanent 15-to-20-year bed is established once, never succession-planted."},
        "years_to_first_harvest": [2, 3], "years_to_full_production": [3, 4],
        "productive_lifespan_years": 18, "rotation": "Permanent bed; do not rotate. Choose the site for the long haul.",
        "regions": {
            "northern_tier": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"4": {"suitability": "perennializes",
                    "calendar": ["cold_pause","cold_pause","cold_pause","harvest","harvest","harvest",
                                 "growing","growing","growing","growing","cold_pause","cold_pause"]}}},
            "hawaii_tropical": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"12": {"suitability": "unsuitable",
                    "suitability_note_seasoned": "Asparagus needs a real winter dormancy it will not get here; it declines instead of perennializing.",
                    "calendar": ["growing","growing","growing","growing","growing","growing",
                                 "growing","growing","growing","growing","growing","growing"]}}}},
    }

# 0. well-formed -> clean
assert herbaceous_perennial_violations(well_formed()) == [], herbaceous_perennial_violations(well_formed())

# 1. off-archetype -> NO-OP even with garbage (chives-style herb stays untouched)
off = {"slug": "chives", "archetype": "culinary_herb", "calendar_basis": "frost_anchored",
       "perennial": True, "lifecycle": "perennial", "regions": {}}
assert herbaceous_perennial_violations(off) == [], "non-herbaceous_perennial crop must be a no-op"

# 2. ADMISSION STATE: unfilled shell cell (suitability null, calendar []) -> skipped
c = well_formed()
c["regions"]["northern_tier"]["resolved_by_zone"]["4"] = {"suitability": None, "calendar": []}
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 3. perennial not true -> violation
c = well_formed(); c["perennial"] = False
assert any("perennial" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 4. lifecycle annual -> violation
c = well_formed(); c["lifecycle"] = "annual"
assert any("lifecycle" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5. succession suitable true -> violation
c = well_formed(); c["succession_policy"]["suitable"] = True
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5b. succession suppressed but no reason -> violation
c = well_formed(); c["succession_policy"]["reason_seasoned"] = None
assert any("reason_seasoned" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6. empty years_to_first_harvest -> violation
c = well_formed(); c["years_to_first_harvest"] = []
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6b. years_to_first_harvest min 0 (no real establishment lag) -> violation
c = well_formed(); c["years_to_first_harvest"] = [0]
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6c. productive_lifespan_years null -> violation
c = well_formed(); c["productive_lifespan_years"] = None
assert any("productive_lifespan_years" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 7. a succession planting track -> violation
c = well_formed(); c["regions"]["northern_tier"]["plantings"].append({"track": "succession", "label": "fill"})
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 8. bad suitability enum on a filled cell -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "fruits_reliably"
assert any("suitability" in v and "fruits_reliably" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 9. unsuitable cell missing the reason note -> violation
c = well_formed(); c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"].pop("suitability_note_seasoned")
assert any("hawaii_tropical" in v and "12" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 10. a suitability-marked cell with an EMPTY calendar (A32 honesty floor) -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["calendar"] = []
assert any("northern_tier" in v and "calendar" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 11. rotation missing -> violation
c = well_formed(); c["rotation"] = None
assert any("rotation" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 12. years_to_first_harvest = [True] -> violation (bool is an int subclass; guard must reject it)
c = well_formed(); c["years_to_first_harvest"] = [True]
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 13. productive_lifespan_years = True -> violation (bool is an int subclass; guard must reject it)
c = well_formed(); c["productive_lifespan_years"] = True
assert any("productive_lifespan_years" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 14. empty years_to_full_production -> violation
c = well_formed(); c["years_to_full_production"] = []
assert any("years_to_full_production" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 15. a second_planting planting track -> violation (sibling of succession, same enum)
c = well_formed(); c["regions"]["northern_tier"]["plantings"].append({"track": "second_planting", "label": "fill"})
assert any("second_planting" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 16. lifecycle permanent -> VALID (proves the accepted-value branch, not just the reject branch)
c = well_formed(); c["lifecycle"] = "permanent"
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 17. non-list years_to_first_harvest (None) -> violation
c = well_formed(); c["years_to_first_harvest"] = None
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

assert SUITABILITY_ENUM == {"perennializes", "marginal", "unsuitable"}, SUITABILITY_ENUM
print("herbaceous_perennial_gate: all tests passed")
