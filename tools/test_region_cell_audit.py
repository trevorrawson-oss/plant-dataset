#!/usr/bin/env python3
"""Unit tests for region_cell_audit -- the region-GENERIC staged-cell anomaly auditor
(Task 2 of the 2026-07-14 maritime PNW region arc). Generalized from rgv_cell_audit.py
(which had no standalone test file; RGV coverage lived in ad hoc review) with a per-region
REGION_CONFIG so the frost-model checks flip correctly per region_id:

- pnw (frost_model="anchored"): resolution_method must be 'frost_anchored_resolved',
  resolved_from must have NON-null last_frost + first_frost, cold_pause is ALLOWED.
- rgv (frost_model="free", unchanged/regression-guarded): resolution_method must be
  frost-FREE, resolved_from must be null-frost, cold_pause is an ERROR.

Run from repo root: cd tools && python3 -m pytest test_region_cell_audit.py -v
(or python3 test_region_cell_audit.py -- standalone, matching the rgv_harness convention.)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import region_cell_audit as rca


def _pnw_annual_cell():
    return {
        "region_id": "pnw",
        "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
        "zone_span": ["8", "9"],
        "resolved_by_zone": {
            z: {"plant_out": "Apr 1 - Jun 30", "harvest": "Jul 1 - Sep 30",
                "harvest_start": "Jul 1", "harvest_end": "Sep 30",
                "first_plant_date": "Apr 1", "last_plant_date": "Jun 30",
                "resolution_method": "frost_anchored_resolved",
                "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1"},
                "calendar": ["cold_pause", "cold_pause", "cold_pause", "plant", "plant", "plant",
                             "harvest", "harvest", "harvest", "growing", "cold_pause", "cold_pause"]}
            for z in ("8", "9")}}


def test_valid_frost_anchored_cell_clean():
    assert rca.audit_cell("broccoli", _pnw_annual_cell(), "pnw") == []
    print("  ok: valid frost-anchored pnw cell is clean")


def test_cold_pause_allowed_for_frost_anchored():
    # the RGV auditor forbade cold_pause; the pnw (frost-anchored) auditor must ALLOW it
    cell = _pnw_annual_cell()
    assert not any("cold_pause" in v for v in rca.audit_cell("broccoli", cell, "pnw"))
    print("  ok: cold_pause allowed for frost-anchored (pnw)")


def test_frost_free_resolution_method_flagged_for_pnw():
    cell = _pnw_annual_cell()
    for z in cell["resolved_by_zone"].values():
        z["resolution_method"] = "month_resolved_frost_free"
        z["resolved_from"] = {"last_frost": None, "first_frost": None}
    v = rca.audit_cell("broccoli", cell, "pnw")
    assert any("resolution_method" in x or "resolved_from" in x for x in v), v
    print("  ok: frost-free resolution_method flagged for pnw (must be frost_anchored_resolved)")


def test_emdash_flagged():
    cell = _pnw_annual_cell()
    cell["region_notes_seasoned"] = "cool summers — long season"
    assert any("em dash" in x.lower() or "—" in x for x in rca.audit_cell("broccoli", cell, "pnw"))
    print("  ok: em dash in consumer copy flagged")


def _rgv_annual_cell():
    """Minimal frost-FREE rgv cell -- the regression guard fixture (Step 9) proving the
    generalization did not change RGV's frost_model='free' behavior: cold_pause must still
    be an error, resolution_method must still be frost-free, resolved_from must be null."""
    return {
        "region_id": "rgv",
        "region_label": "Rio Grande Valley: Subtropical South Texas",
        "zone_span": ["9", "10"],
        "resolved_by_zone": {
            z: {"plant_out": "Sep 1 - Nov 30", "harvest": "Dec 1 - Feb 28",
                "harvest_start": "Dec 1", "harvest_end": "Feb 28",
                "first_plant_date": "Sep 1", "last_plant_date": "Nov 30",
                "resolution_method": "month_resolved_frost_free",
                "resolved_from": {"last_frost": None, "first_frost": None},
                "calendar": ["growing", "growing", "season_over", "season_over", "season_over",
                             "season_over", "season_over", "season_over", "plant", "plant",
                             "plant", "harvest"]}
            for z in ("9", "10")}}


def test_rgv_regression_cold_pause_still_forbidden():
    cell = _rgv_annual_cell()
    for z in cell["resolved_by_zone"].values():
        z["calendar"] = ["cold_pause"] + z["calendar"][1:]
    v = rca.audit_cell("broccoli", cell, "rgv")
    assert any("cold_pause" in x for x in v), v
    print("  ok: REGRESSION GUARD -- rgv (frost_model='free') still forbids cold_pause")


def test_rgv_regression_clean_cell_still_clean():
    assert rca.audit_cell("broccoli", _rgv_annual_cell(), "rgv") == []
    print("  ok: REGRESSION GUARD -- valid frost-free rgv cell still clean")


if __name__ == "__main__":
    test_valid_frost_anchored_cell_clean()
    test_cold_pause_allowed_for_frost_anchored()
    test_frost_free_resolution_method_flagged_for_pnw()
    test_emdash_flagged()
    test_rgv_regression_cold_pause_still_forbidden()
    test_rgv_regression_clean_cell_still_clean()
    print("\nALL region_cell_audit TESTS PASSED")
