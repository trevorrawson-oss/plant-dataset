#!/usr/bin/env python3
"""Structural-gate tests for the woody-ornamental (lavender, anchor 14) cert branch (A13).
Run: python3 tools/test_woody_ornamental_gate.py  ->  ALL PASS."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from woody_ornamental_gate import woody_ornamental_violations

_PERENNIAL_CAL = ["dormant", "dormant", "dormant", "growing", "growing", "bloom",
                  "bloom", "prune", "growing", "growing", "dormant", "dormant"]


def well_formed():
    return {"calendar_basis": "perennial_woody_ornamental", "gating_factors": [],
            "hardiness_zone_min": 5, "hardiness_zone_max": 9,
            "regions": {"r": {"resolved_by_zone": {
                "6": {"grown_as": "perennial", "calendar": list(_PERENNIAL_CAL)}}}}}


def test_clean():
    assert woody_ornamental_violations(well_formed()) == []


def test_noop_off_basis():
    c = well_formed(); c["calendar_basis"] = "frost_anchored"
    assert woody_ornamental_violations(c) == []


def test_admission_state_skipped():
    # a null grown_as + empty calendar is the Step-3.5 admission state, not a violation
    c = well_formed()
    c["regions"]["r"]["resolved_by_zone"]["6"] = {"grown_as": None, "calendar": []}
    assert woody_ornamental_violations(c) == []


def test_missing_scalar():
    c = well_formed(); c["hardiness_zone_min"] = None
    assert any("hardiness_zone_min" in v for v in woody_ornamental_violations(c))


def test_bad_grown_as():
    c = well_formed()
    c["regions"]["r"]["resolved_by_zone"]["6"]["grown_as"] = "biennial"
    assert any("grown_as" in v for v in woody_ornamental_violations(c))


def test_prune_in_annual():
    # an annual (replanted) cell must not carry the perennial prune token
    c = well_formed()
    cell = c["regions"]["r"]["resolved_by_zone"]["6"]
    cell["grown_as"] = "annual"
    cell["calendar"] = ["growing", "growing", "growing", "bloom", "bloom", "season_over",
                        "season_over", "prune", "season_over", "plant", "growing", "growing"]
    assert any("prune" in v for v in woody_ornamental_violations(c))


def test_season_over_in_perennial():
    c = well_formed()
    cell = c["regions"]["r"]["resolved_by_zone"]["6"]
    cell["calendar"] = list(_PERENNIAL_CAL); cell["calendar"][1] = "season_over"
    assert any("season_over" in v for v in woody_ornamental_violations(c))


def test_fruit_token_rejected():
    # ornamental: bloom IS the cut window -- no harvest/renovation token belongs in any cell
    c = well_formed()
    cell = c["regions"]["r"]["resolved_by_zone"]["6"]
    cell["calendar"] = list(_PERENNIAL_CAL); cell["calendar"][6] = "harvest"
    assert any("harvest" in v for v in woody_ornamental_violations(c))


def test_tree_key_rejected():
    c = well_formed(); c["rootstock"] = "dwarf"
    assert any("rootstock" in v or "tree" in v for v in woody_ornamental_violations(c))


def test_chill_gate_value_rejected():
    c = well_formed(); c["chill_hours_required"] = 800
    assert any("chill_hours_required" in v for v in woody_ornamental_violations(c))


def test_null_tree_key_ok():
    # a 2.9 null/empty scaffold of a tree key is NOT a violation (reject values, not keys)
    c = well_formed(); c["rootstock_options"] = []; c["chill_hours_required"] = None
    assert woody_ornamental_violations(c) == []


def test_tree_only_cell_key_rejected():
    c = well_formed()
    c["regions"]["r"]["resolved_by_zone"]["6"]["suitability"] = "survives_no_fruit"
    assert any("suitability" in v for v in woody_ornamental_violations(c))


def test_gating_factors_must_be_empty():
    c = well_formed(); c["gating_factors"] = ["cold_hardiness"]
    assert any("gating_factors" in v for v in woody_ornamental_violations(c))


def test_variety_cross_pollination_rejected():
    c = well_formed()
    c["varieties"] = {"recommended": [{"name": "Grosso", "pollinizer": "Munstead"}]}
    assert any("pollin" in v.lower() for v in woody_ornamental_violations(c))


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
