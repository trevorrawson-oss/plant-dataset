#!/usr/bin/env python3
"""Tests for the berries_herbaceous structural cert branch (strawberry, anchor 13).
Run: python3 tools/test_berry_herbaceous_gate.py

Invariants (2026-06-18-strawberry-berries-herbaceous-model-design.md D6-D9):
  - fires ONLY for calendar_basis == perennial_herbaceous (no-op otherwise).
  - lifecycle SCALARS present (Step 2, before 3.5 sets the basis -> admission-safe);
    self_fertile is True; "photoperiod" NOT in gating_factors (deliberate inverse of onion).
  - varieties carry NO tree cross-pollination keys (bloom_group/pollinizer/...).
  - per FILLED cell: grown_as in {perennial, annual}; no tree-only keys (suitability,
    chill_hours_delivered); annual cells carry no renovation/dormant, perennial cells no
    season_over. A cell with grown_as null AND empty calendar is the admission state (skip).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_herbaceous_gate import berry_herbaceous_violations, GROWN_AS_ENUM

def well_formed():
    """Minimal valid filled strawberry: scalars set, self-fertile, one perennial + one
    annual cell whose calendars carry the right tokens for their grown_as."""
    return {
        "slug": "strawberry-mini", "calendar_basis": "perennial_herbaceous",
        "self_fertile": True, "gating_factors": [],
        "establishment_years": 1, "productive_lifespan_years": 4,
        "years_to_first_harvest": [2], "years_to_full_production": [2, 3],
        "varieties": {"recommended": [
            {"name": "Honeoye", "type": "june_bearing"},
            {"name": "Albion", "type": "day_neutral"}]},
        "regions": {
            "northern_tier": {"resolved_by_zone": {"5": {"grown_as": "perennial",
                "calendar": ["dormant","dormant","dormant","growing","bloom","harvest",
                             "renovation","growing","growing","growing","dormant","dormant"]}}},
            "ca_interior": {"resolved_by_zone": {"9": {"grown_as": "annual",
                "calendar": ["growing","bloom","harvest","harvest","harvest","harvest",
                             "season_over","season_over","season_over","plant","growing","growing"]}}}},
    }

# 0. well-formed -> clean
assert berry_herbaceous_violations(well_formed()) == [], berry_herbaceous_violations(well_formed())

# 1. off-basis -> NO-OP even with garbage
off = {"slug": "carrot", "calendar_basis": "frost_anchored", "self_fertile": None,
       "gating_factors": ["photoperiod"], "regions": {}}
assert berry_herbaceous_violations(off) == [], "non-perennial_herbaceous crop must be a no-op"

# 2. ADMISSION STATE: scalars set (Step 2) but cells unfilled (grown_as null, calendar []) -> clean
c = well_formed()
for r in c["regions"].values():
    for cell in r["resolved_by_zone"].values():
        cell["grown_as"] = None; cell["calendar"] = []
assert berry_herbaceous_violations(c) == [], berry_herbaceous_violations(c)

# 3. missing lifecycle scalar -> violation
c = well_formed(); c["productive_lifespan_years"] = None
assert any("productive_lifespan_years" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 4. self_fertile not True -> violation
c = well_formed(); c["self_fertile"] = False
assert any("self_fertile" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 5. photoperiod in gating_factors -> violation (the onion-guard)
c = well_formed(); c["gating_factors"] = ["photoperiod"]
assert any("photoperiod" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 6. a variety carrying tree cross-pollination machinery -> violation
c = well_formed(); c["varieties"]["recommended"][0]["bloom_group"] = 2
assert any("bloom_group" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 7. a tree-only key on a cell (mis-route) -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["suitability"] = "fruits_reliably"
assert any("suitability" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 8. bad grown_as enum on a filled cell -> violation
c = well_formed(); c["regions"]["ca_interior"]["resolved_by_zone"]["9"]["grown_as"] = "biennial"
assert any("grown_as" in v and "biennial" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 9. annual cell carrying a perennial token -> violation
c = well_formed(); c["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"][6] = "renovation"
assert any("ca_interior" in v and "9" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

# 10. perennial cell carrying season_over -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"][10] = "season_over"
assert any("northern_tier" in v and "5" in v for v in berry_herbaceous_violations(c)), berry_herbaceous_violations(c)

assert GROWN_AS_ENUM == {"perennial", "annual"}, GROWN_AS_ENUM
print("berry_herbaceous_gate: all tests passed")
