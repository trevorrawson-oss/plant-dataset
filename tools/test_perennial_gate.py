#!/usr/bin/env python3
"""Tests for the perennial (tree) cert-gate branch -- the tree-shape invariants the
generic whole_crop_gate does not encode. Run: python3 tools/test_perennial_gate.py

Invariants (v1.8 amendment §4-5; gold_standard_arc_checklist tree branch):
  - calendar_basis perennial_chill_gated -> exactly ONE track:"perennial" establishment
    plantings entry per region (no succession/second_planting/start_indoors/direct_sow).
  - every resolved cell carries a `suitability` in the 4-value enum.
  - the NO-FRUIT DIRECTION SPLIT: a survives_no_fruit cell carries a calendar IFF
    chill_hours_delivered[0] >= the crop's lowest variety chill (under-report vs over-promise);
    unsuitable -> empty; fruits_reliably/marginal -> non-empty.
  - an annual crop (frost_anchored) is a NO-OP (the branch only fires for trees).
"""
import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from perennial_gate import perennial_cert_violations


def well_formed_tree():
    """A minimal, valid perennial_chill_gated crop (lowest variety chill = 400)."""
    return {
        "slug": "peach-mini",
        "calendar_basis": "perennial_chill_gated",
        "varieties": {"recommended": [
            {"name": "Florida King", "chill_hours_required": 400},
            {"name": "Contender", "chill_hours_required": 1050}]},
        "regions": {
            "se_gulf": {
                "plantings": [{"succession_id": 1, "label": "establishment", "track": "perennial",
                               "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": []}],
                "resolved_by_zone": {
                    "8": {"suitability": "fruits_reliably", "chill_hours_delivered": [700, 900],
                          "calendar": ["dormant", "prune", "bloom", "growing", "harvest", "harvest",
                                       "growing", "care", "dormant", "dormant", "dormant", "dormant"]},
                    "9": {"suitability": "marginal", "chill_hours_delivered": [500, 700],
                          "calendar": ["dormant", "prune", "bloom", "growing", "harvest", "care",
                                       "dormant", "dormant", "dormant", "dormant", "dormant", "dormant"]}}},
            "northern_tier": {
                "plantings": [{"succession_id": 1, "label": "establishment", "track": "perennial",
                               "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": []}],
                "resolved_by_zone": {
                    "3": {"suitability": "unsuitable", "chill_hours_delivered": [1200, 1500], "calendar": []},
                    "4": {"suitability": "survives_no_fruit", "chill_hours_delivered": [1100, 1500],
                          "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "harvest",
                                       "harvest", "care", "dormant", "dormant", "dormant", "dormant"]}}}},
    }


# 0. the well-formed tree -> no violations
assert perennial_cert_violations(well_formed_tree()) == [], perennial_cert_violations(well_formed_tree())

# 1. annual crop (frost_anchored) -> NO-OP even if malformed for a tree
annual = {"slug": "carrot", "calendar_basis": "frost_anchored",
          "regions": {"se_gulf": {"plantings": [{"track": "succession"}], "resolved_by_zone": {}}}}
assert perennial_cert_violations(annual) == [], "annual must be a no-op"

# 2. a succession entry on a tree -> violation
t = well_formed_tree()
t["regions"]["se_gulf"]["plantings"].append({"track": "succession", "label": "spring"})
assert any("exactly 1" in v or "succession" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 3. start_indoors on the establishment entry -> violation
t = well_formed_tree()
t["regions"]["se_gulf"]["plantings"][0]["start_indoors"] = []
assert any("start_indoors" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 4. bad suitability value -> violation
t = well_formed_tree()
t["regions"]["se_gulf"]["resolved_by_zone"]["8"]["suitability"] = "great"
assert any("suitability" in v and "8" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 5. survives_no_fruit + chill MET but EMPTY calendar -> under-report violation
t = well_formed_tree()
t["regions"]["northern_tier"]["resolved_by_zone"]["4"]["calendar"] = []
assert any("under-report" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 6. survives_no_fruit + chill BELOW floor but NON-empty calendar -> over-promise violation
t = well_formed_tree()
c = t["regions"]["northern_tier"]["resolved_by_zone"]["4"]
c["chill_hours_delivered"] = [200, 350]  # below the 400 floor -> must be empty
assert any("over-promise" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 7. unsuitable cell with a NON-empty calendar -> violation
t = well_formed_tree()
t["regions"]["northern_tier"]["resolved_by_zone"]["3"]["calendar"] = ["bloom"]
assert any("unsuitable" in v and "3" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 8. fruits_reliably with an EMPTY calendar -> violation
t = well_formed_tree()
t["regions"]["se_gulf"]["resolved_by_zone"]["8"]["calendar"] = []
assert any("must carry a calendar" in v for v in perennial_cert_violations(t)), perennial_cert_violations(t)

# 9. SHELL state (Step 3.5: cells unfilled, suitability=null) -> A3 skips unfilled cells
# (the empty region is the region-fill check's job, not a malformed-suitability violation).
# The perennial establishment entry (built by build_region_shells) is still present + valid.
t = well_formed_tree()
for r in t["regions"].values():
    for cell in r["resolved_by_zone"].values():
        cell["suitability"] = None
        cell["calendar"] = []
assert perennial_cert_violations(t) == [], perennial_cert_violations(t)

# ============ EVERGREEN branch (perennial_evergreen, gating-aware no-fruit) ============
# tree_region_model_evergreen_amendment_v1_0: a perennial_evergreen crop runs the SAME
# universal invariants, but the no-fruit DIRECTION SPLIT is keyed on gating_factors. A
# cold-only evergreen (citrus) has no chill Goldilocks band -- colder is monotonically
# worse -- so survives_no_fruit is NOT forced to carry-or-empty a calendar by chill.
def well_formed_evergreen():
    """A minimal valid perennial_evergreen crop, cold-only gating (lemon-like).
    Climate datum is min_winter_temp_f (chill ~ 0), NOT chill_hours_delivered."""
    return {
        "slug": "lemon-mini",
        "calendar_basis": "perennial_evergreen",
        "gating_factors": ["cold_hardiness"],
        "regions": {
            "ca_south_coast": {
                "plantings": [{"succession_id": 1, "label": "establishment", "track": "perennial",
                               "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": []}],
                "resolved_by_zone": {
                    "10": {"suitability": "fruits_reliably", "min_winter_temp_f": [36, 42],
                           "calendar": ["harvest", "harvest", "bloom", "bloom", "growing", "growing",
                                        "growing", "growing", "growing", "growing", "harvest", "harvest"]}}},
            "northern_tier": {
                "plantings": [{"succession_id": 1, "label": "establishment", "track": "perennial",
                               "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": []}],
                "resolved_by_zone": {
                    "7": {"suitability": "unsuitable", "min_winter_temp_f": [0, 10], "calendar": []},
                    "8": {"suitability": "survives_no_fruit", "min_winter_temp_f": [15, 25], "calendar": []}}}},
    }


# 10. well-formed evergreen -> fires + clean (survives_no_fruit with empty calendar is OK, cold-only)
assert perennial_cert_violations(well_formed_evergreen()) == [], perennial_cert_violations(well_formed_evergreen())

# 11. evergreen survives_no_fruit WITH a calendar is ALSO fine (no chill over/under split for cold-only)
e = well_formed_evergreen()
e["regions"]["northern_tier"]["resolved_by_zone"]["8"]["calendar"] = [
    "harvest", "harvest", "bloom", "growing", "growing", "growing",
    "growing", "growing", "growing", "growing", "harvest", "harvest"]
assert perennial_cert_violations(e) == [], perennial_cert_violations(e)

# 12. universal invariant still fires on an evergreen: unsuitable cell with a calendar
e = well_formed_evergreen()
e["regions"]["northern_tier"]["resolved_by_zone"]["7"]["calendar"] = ["bloom"]
assert any("unsuitable" in v and "7" in v for v in perennial_cert_violations(e)), perennial_cert_violations(e)

# 13. universal: fruits_reliably with an empty calendar on an evergreen -> violation
e = well_formed_evergreen()
e["regions"]["ca_south_coast"]["resolved_by_zone"]["10"]["calendar"] = []
assert any("must carry a calendar" in v for v in perennial_cert_violations(e)), perennial_cert_violations(e)

# 14. universal: a succession entry on an evergreen tree -> violation
e = well_formed_evergreen()
e["regions"]["ca_south_coast"]["plantings"].append({"track": "second_planting", "label": "x"})
assert any("exactly 1" in v or "second_planting" in v for v in perennial_cert_violations(e)), perennial_cert_violations(e)

# 15. SHELL state on an evergreen (Step 3.5: suitability null) -> A3 skips unfilled cells
e = well_formed_evergreen()
for r in e["regions"].values():
    for cell in r["resolved_by_zone"].values():
        cell["suitability"] = None
        cell["calendar"] = []
assert perennial_cert_violations(e) == [], perennial_cert_violations(e)

print("PASS perennial_gate")
