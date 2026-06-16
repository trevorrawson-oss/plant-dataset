#!/usr/bin/env python3
"""Tests for the photoperiod (day-length) cert-gate branch -- the A9 invariants for a
photoperiod-gated crop (onion, anchor 12; the allium family inherits it). Run:
python3 tools/test_photoperiod_gate.py

Invariants (onion-photoperiod-model-design.md; gold-standard arc A9):
  - fires ONLY for a crop with "photoperiod" in gating_factors (no-op otherwise).
  - VARIETY TYPING: every varieties.recommended[] entry is an object with a valid
    day_length_type in {long_day, intermediate_day, short_day}.
  - CELL TYPING: every FILLED resolved cell's recommended_day_length_type is valid; a
    null cell is the Step-3.5 admission state (skipped -- A2 owns region-fill).
  - COVERAGE INVARIANT: every day-length type a region RESOLVES to has >=1 recommended
    variety carrying that type (no "grow short-day here" with zero short-day varieties).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photoperiod_gate import photoperiod_violations, DAY_LENGTH_ENUM


def well_formed_photoperiod():
    """Minimal valid photoperiod crop: 3 typed varieties spanning the enum; filled cells
    resolving only to types that have a matching variety."""
    return {
        "slug": "onion-mini",
        "calendar_basis": "frost_anchored",
        "gating_factors": ["photoperiod"],
        "varieties": {"recommended": [
            {"name": "Walla Walla", "day_length_type": "long_day"},
            {"name": "Candy", "day_length_type": "intermediate_day"},
            {"name": "Texas 1015Y", "day_length_type": "short_day"}]},
        "regions": {
            "northern_tier": {"resolved_by_zone": {
                "3": {"recommended_day_length_type": "long_day"},
                "5": {"recommended_day_length_type": "long_day"}}},
            "se_gulf": {"resolved_by_zone": {
                "9": {"recommended_day_length_type": "short_day"}}},
            "ca_interior": {"resolved_by_zone": {
                "8": {"recommended_day_length_type": "intermediate_day"}}}},
    }


def shell_admission():
    """Step-3.5 admission state: varieties typed (from Steps 1-3), but every cell's
    recommended_day_length_type is still null (Step 4 fills it). Must be a no-op."""
    c = well_formed_photoperiod()
    for r in c["regions"].values():
        for cell in r["resolved_by_zone"].values():
            cell["recommended_day_length_type"] = None
    return c


# 0. the well-formed crop -> no violations
assert photoperiod_violations(well_formed_photoperiod()) == [], photoperiod_violations(well_formed_photoperiod())

# 1. a crop WITHOUT photoperiod in gating_factors -> NO-OP even if varieties are untyped
non_photo = {"slug": "carrot", "calendar_basis": "frost_anchored", "gating_factors": [],
             "varieties": {"recommended": ["Nantes types", "Danvers"]},
             "regions": {"se_gulf": {"resolved_by_zone": {"9": {"recommended_day_length_type": "bogus"}}}}}
assert photoperiod_violations(non_photo) == [], "non-photoperiod crop must be a no-op"
# also no-op when gating_factors is missing entirely
assert photoperiod_violations({"slug": "x", "varieties": {"recommended": [123]}}) == [], "missing gating_factors -> no-op"

# 2. a variety with a bad day_length_type -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"][0]["day_length_type"] = "medium_day"
assert any("day_length_type" in v and "medium_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 3. a bare-string variety (not the object shape) -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"][1] = "Candy (intermediate)"
assert any("recommended[1]" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 4. a FILLED cell with a bad recommended_day_length_type -> violation
c = well_formed_photoperiod()
c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["recommended_day_length_type"] = "winter_day"
assert any("se_gulf" in v and "9" in v and "winter_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 5. Step-3.5 ADMISSION STATE: all cells null -> NO-OP (the load-bearing mid-arc case)
assert photoperiod_violations(shell_admission()) == [], photoperiod_violations(shell_admission())

# 6. COVERAGE GAP: a cell resolves to short_day but no recommended variety is short_day -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"] = [v for v in c["varieties"]["recommended"] if v["day_length_type"] != "short_day"]
assert any("coverage" in v.lower() and "short_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 7. COVERAGE satisfied with EXTRA varieties (more varieties than resolved types) -> clean
c = well_formed_photoperiod()
c["varieties"]["recommended"].append({"name": "Red Burgundy", "day_length_type": "short_day"})
assert photoperiod_violations(c) == [], photoperiod_violations(c)

# 8. the enum is exactly the 3 classes (day-neutral folds into intermediate_day)
assert DAY_LENGTH_ENUM == {"long_day", "intermediate_day", "short_day"}, DAY_LENGTH_ENUM

print("photoperiod_gate: all tests passed")
