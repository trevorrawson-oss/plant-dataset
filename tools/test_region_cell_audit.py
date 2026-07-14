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


# ---- pnw tree/citrus perennial archetypes (Task 6, cold-limited citrus) ----
# Task 5/6's worked examples (docs/pnw_cell_contract.md §1, §5.2) carry resolution_method
# perennial_precompute (chill-gated trees) / perennial_evergreen_precompute (citrus), NOT
# frost_anchored_resolved -- and citrus's resolved_from is legitimately {} (cold is the
# per-cell climate axis, not frost placement). The pre-fix "anchored" branch above demanded
# frost_anchored_resolved + real frost dates unconditionally, which would have flagged EVERY
# pnw tree/citrus cell as a violation (confirmed RED before this fix landed). These tests
# pin the fix + guard it never over-corrects into accepting a genuinely broken cell.

def _pnw_citrus_cell(resolved_from=None):
    rf = {} if resolved_from is None else resolved_from
    return {
        "region_id": "pnw",
        "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
        "zone_span": ["8", "9"],
        "resolved_by_zone": {
            z: {"plant_out": None, "resolution_method": "perennial_evergreen_precompute",
                "suitability": "unsuitable", "calendar": [], "resolved_from": dict(rf)}
            for z in ("8", "9")}}


def test_pnw_citrus_empty_resolved_from_clean():
    assert rca.audit_cell("orange-navel", _pnw_citrus_cell(), "pnw") == []
    print("  ok: pnw citrus cell (perennial_evergreen_precompute, resolved_from={}) is clean")


def test_pnw_chill_gated_tree_real_frost_dates_clean():
    cell = {
        "region_id": "pnw",
        "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
        "zone_span": ["8", "9"],
        "resolved_by_zone": {
            "8": {"plant_out": None, "resolution_method": "perennial_precompute",
                  "suitability": "fruits_reliably",
                  "calendar": ["bloom", "bloom", "bloom", "bloom", "growing", "growing",
                               "growing", "growing", "harvest", "harvest", "harvest", "harvest"],
                  "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1"}},
            "9": {"plant_out": None, "resolution_method": "perennial_precompute",
                  "suitability": "fruits_reliably",
                  "calendar": ["bloom", "bloom", "bloom", "bloom", "growing", "growing",
                               "growing", "growing", "harvest", "harvest", "harvest", "harvest"],
                  "resolved_from": {"last_frost": "Apr 1", "first_frost": "Nov 15"}}}}
    assert rca.audit_cell("apple", cell, "pnw") == []
    print("  ok: pnw chill-gated tree cell (perennial_precompute, real frost dates) is clean")


def test_pnw_perennial_half_populated_resolved_from_still_flagged():
    # ADVERSARIAL: a perennial cell whose resolved_from carries ONE of the two frost keys
    # (a copy-paste/partial-author defect) must still be caught, not waved through just
    # because the method string is in the exempt set.
    cell = _pnw_citrus_cell(resolved_from={"last_frost": "Apr 15", "first_frost": None})
    v = rca.audit_cell("orange-navel", cell, "pnw")
    assert any("partially populated" in x for x in v), v
    print("  ok: ADVERSARIAL -- half-populated resolved_from on a pnw perennial cell is still flagged")


def test_pnw_annual_wrong_method_still_flagged_after_perennial_fix():
    # REGRESSION: the perennial exemption must not leak into the annual branch -- an annual
    # cell with a frost-free method (or missing frost dates) is still a violation for pnw.
    cell = _pnw_annual_cell()
    for z in cell["resolved_by_zone"].values():
        z["resolution_method"] = "month_resolved_frost_free"
        z["resolved_from"] = {"last_frost": None, "first_frost": None}
    v = rca.audit_cell("broccoli", cell, "pnw")
    assert any("resolution_method" in x or "resolved_from" in x for x in v), v
    print("  ok: REGRESSION GUARD -- annual cell with wrong method still flagged post-fix")


# ---- pnw woody-ornamental herb archetype (Task 7a, lavender/oregano/rosemary/sage/thyme) ----
# This archetype's real gate code (woody_ornamental_gate.py, woody_ornamental_calendar.py) and
# every existing region cell for these 5 crops (northern_tier, se_gulf, ca_north_coast, ..., and
# the RGV Task 7 precedent) use resolution_method perennial_woody_ornamental_precompute
# (perennial) / woody_ornamental_annual_precompute (annual), NEVER frost_anchored_resolved --
# the same class of gap as the tree/citrus fix above, just unexercised until this archetype's
# first pnw cells. The pre-fix "anchored" branch demanded frost_anchored_resolved
# unconditionally, which would have flagged EVERY pnw woody-ornamental cell (confirmed RED
# before this fix landed: whole_crop_gate PASS, region_cell_audit 2 violations on a clean
# lavender cell). Unlike tree/citrus, this archetype's resolved_from must always carry REAL
# frost dates in a frost-anchored region (both derive_perennial_woody_calendar's dormancy
# bracket and every existing cell's own convention require it; only a frost-FREE region's
# perennial cell legitimately carries none), so this exemption does not relax the
# resolved_from check at all, only the resolution_method string match.

def _pnw_woody_ornamental_cell(method="perennial_woody_ornamental_precompute", resolved_from=None):
    rf = {"last_frost": "Mar 21", "first_frost": "Nov 12"} if resolved_from is None else resolved_from
    return {
        "region_id": "pnw",
        "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
        "zone_span": ["8", "9"],
        "resolved_by_zone": {
            z: {"plant_out": "Mar 21 - Apr 11", "resolution_method": method,
                "grown_as": "perennial", "bloom": "May 30 - Jul 11",
                "calendar": ["dormant", "dormant", "growing", "growing", "bloom", "bloom",
                             "bloom", "prune", "growing", "growing", "growing", "dormant"],
                "resolved_from": dict(rf)}
            for z in ("8", "9")}}


def test_pnw_woody_ornamental_perennial_real_frost_dates_clean():
    assert rca.audit_cell("lavender", _pnw_woody_ornamental_cell(), "pnw") == []
    print("  ok: pnw woody-ornamental perennial cell (perennial_woody_ornamental_precompute, "
          "real frost dates) is clean")


def test_pnw_woody_ornamental_annual_method_real_frost_dates_clean():
    cell = _pnw_woody_ornamental_cell(method="woody_ornamental_annual_precompute")
    assert rca.audit_cell("lavender", cell, "pnw") == []
    print("  ok: pnw woody-ornamental annual-flip cell (woody_ornamental_annual_precompute, "
          "real frost dates) is clean")


def test_pnw_woody_ornamental_missing_frost_dates_still_flagged():
    # ADVERSARIAL: unlike tree/citrus, this archetype never legitimately carries an empty/null
    # resolved_from in a frost-anchored region (derive_perennial_woody_calendar's dormancy
    # bracket needs real dates) -- a null-frost cell must still be caught, not waved through
    # just because the method string is in the exempt set.
    cell = _pnw_woody_ornamental_cell(resolved_from={"last_frost": None, "first_frost": None})
    v = rca.audit_cell("lavender", cell, "pnw")
    assert any("resolved_from missing non-null" in x for x in v), v
    print("  ok: ADVERSARIAL -- null resolved_from on a pnw woody-ornamental cell is still flagged")


def test_pnw_woody_ornamental_wrong_method_string_still_flagged():
    # ADVERSARIAL: a garbage/frost-free method string on a woody-ornamental-shaped cell must
    # still fall through to the strict frost_anchored_resolved branch, not silently pass.
    cell = _pnw_woody_ornamental_cell(method="month_resolved_frost_free")
    v = rca.audit_cell("lavender", cell, "pnw")
    assert any("resolution_method" in x for x in v), v
    print("  ok: ADVERSARIAL -- wrong method string on a woody-ornamental cell still flagged")


if __name__ == "__main__":
    test_valid_frost_anchored_cell_clean()
    test_cold_pause_allowed_for_frost_anchored()
    test_frost_free_resolution_method_flagged_for_pnw()
    test_emdash_flagged()
    test_rgv_regression_cold_pause_still_forbidden()
    test_rgv_regression_clean_cell_still_clean()
    test_pnw_citrus_empty_resolved_from_clean()
    test_pnw_chill_gated_tree_real_frost_dates_clean()
    test_pnw_perennial_half_populated_resolved_from_still_flagged()
    test_pnw_annual_wrong_method_still_flagged_after_perennial_fix()
    test_pnw_woody_ornamental_perennial_real_frost_dates_clean()
    test_pnw_woody_ornamental_annual_method_real_frost_dates_clean()
    test_pnw_woody_ornamental_missing_frost_dates_still_flagged()
    test_pnw_woody_ornamental_wrong_method_string_still_flagged()
    print("\nALL region_cell_audit TESTS PASSED")
