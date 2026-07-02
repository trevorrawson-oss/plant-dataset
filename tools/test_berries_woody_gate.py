#!/usr/bin/env python3
"""Structural-gate tests for the berries_woody (blueberry, anchor 18) cert branch (A15).
Run: python3 tools/test_berries_woody_gate.py  ->  ALL PASS.

The calendar coherence (stored == derived) is the SEPARATE A16
(berry_woody_calendar.berry_woody_calendar_violations); this gate covers the structural
invariants: lifecycle scalars + the chill gate signature + prose backstop, self_fertile
false, the per-cell recommended_type/leaf_habit typing, the type COVERAGE invariant, the
token placement (deciduous has dormant, evergreen has none, never season_over/renovation),
and no tree machinery / mis-route. NOTE the blueberry-specific INVERSION vs the woody-
ornamental gate: chill_hours_required is LEGIT (the gate basis, not tree machinery).
chill-DELIVERED moved to the shared region_chill_delivered table (F2 refactor); A15 does
NOT require a per-cell chill_hours_delivered, and whole_crop_gate A18 forbids one.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berries_woody_gate import (berries_woody_violations,
                                berries_woody_variety_chill_violations)

D, G, B, H, C, P, SO = "dormant", "growing", "bloom", "harvest", "care", "prune", "season_over"
_DECID = [D, D, P, B, G, G, H, H, C, D, D, D]
_EVER = [G, G, B, G, G, H, H, C, G, G, G, G]


def well_formed():
    return {"calendar_basis": "berries_woody", "gating_factors": ["chill_hours"],
            "chill_hours_required": 1000, "self_fertile": False,
            "establishment_years": [2, 3], "years_to_first_harvest": [2, 3],
            "years_to_full_production": [6, 8], "productive_lifespan_years": [20, 50],
            "type_selection_seasoned": "x", "type_selection_beginner": "x",
            "pollinator_notes_seasoned": "x", "pollinator_notes_beginner": "x",
            "chill_hours_note_seasoned": "x", "chill_hours_note_beginner": "x",
            "varieties": {"recommended": [{"name": "Duke", "type": "northern_highbush"}]},
            "regions": {"northern_tier": {"resolved_by_zone": {
                "6": {"recommended_type": "northern_highbush", "leaf_habit": "deciduous",
                      "calendar": list(_DECID)}}}}}


def test_clean():
    assert berries_woody_violations(well_formed()) == [], berries_woody_violations(well_formed())


def test_noop_off_basis():
    c = well_formed(); c["calendar_basis"] = "frost_anchored"
    assert berries_woody_violations(c) == []


def test_admission_state_skipped():
    # null recommended_type + null leaf_habit + empty calendar = Step-3.5 admission state
    c = well_formed()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"] = {
        "recommended_type": None, "leaf_habit": None, "calendar": []}
    assert berries_woody_violations(c) == []


def test_missing_lifecycle_scalar():
    c = well_formed(); c["productive_lifespan_years"] = None
    assert any("productive_lifespan_years" in v for v in berries_woody_violations(c))


def test_gating_factors_must_contain_chill_hours():
    c = well_formed(); c["gating_factors"] = []
    assert any("chill_hours" in v and "gating_factors" in v for v in berries_woody_violations(c))


def test_chill_hours_required_present():
    c = well_formed(); c["chill_hours_required"] = None
    assert any("chill_hours_required" in v for v in berries_woody_violations(c))


def test_self_fertile_must_be_false():
    c = well_formed(); c["self_fertile"] = True
    assert any("self_fertile" in v for v in berries_woody_violations(c))


def test_prose_pair_backstop():
    c = well_formed(); c["type_selection_seasoned"] = None
    assert any("type_selection_seasoned" in v for v in berries_woody_violations(c))


def test_bad_recommended_type():
    c = well_formed()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["recommended_type"] = "lowbush"
    assert any("recommended_type" in v for v in berries_woody_violations(c))


def test_bad_leaf_habit():
    c = well_formed()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["leaf_habit"] = "semi_evergreen"
    assert any("leaf_habit" in v for v in berries_woody_violations(c))


def test_coverage_invariant():
    # a cell recommends rabbiteye but no rabbiteye cultivar is in the recommended set
    c = well_formed()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["recommended_type"] = "rabbiteye"
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["leaf_habit"] = "evergreen"
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["calendar"] = list(_EVER)
    assert any("coverage" in v and "rabbiteye" in v for v in berries_woody_violations(c))


def test_season_over_rejected():
    c = well_formed()
    cell = c["regions"]["northern_tier"]["resolved_by_zone"]["6"]
    cell["calendar"] = list(_DECID); cell["calendar"][1] = SO
    assert any("season_over" in v for v in berries_woody_violations(c))


def test_renovation_rejected():
    c = well_formed()
    cell = c["regions"]["northern_tier"]["resolved_by_zone"]["6"]
    cell["calendar"] = list(_DECID); cell["calendar"][6] = "renovation"
    assert any("renovation" in v for v in berries_woody_violations(c))


def test_deciduous_must_have_dormant():
    c = well_formed()
    cell = c["regions"]["northern_tier"]["resolved_by_zone"]["6"]
    cell["calendar"] = [G] * 12  # deciduous but no dormant
    assert any("dormant" in v for v in berries_woody_violations(c))


def test_evergreen_no_dormant():
    c = well_formed()
    cell = c["regions"]["northern_tier"]["resolved_by_zone"]["6"]
    cell["recommended_type"] = "rabbiteye"; cell["leaf_habit"] = "evergreen"
    c["varieties"]["recommended"].append({"name": "Powderblue", "type": "rabbiteye"})
    cell["calendar"] = list(_EVER); cell["calendar"][0] = D  # evergreen must not carry dormant
    assert any("dormant" in v for v in berries_woody_violations(c))


def test_tree_only_cell_key_suitability_rejected():
    c = well_formed()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["suitability"] = "survives_no_fruit"
    assert any("suitability" in v for v in berries_woody_violations(c))


def test_chill_delivered_not_required_on_cell():
    # F2 refactor: chill-delivered is the shared region_chill_delivered table now. A15 does NOT
    # require a per-cell chill_hours_delivered (well_formed carries none) -- A18 owns its absence.
    assert berries_woody_violations(well_formed()) == []


def test_tree_machinery_rootstock_rejected():
    c = well_formed(); c["rootstock"] = "dwarf"
    assert any("rootstock" in v or "tree" in v for v in berries_woody_violations(c))


def test_chill_hours_required_value_ok():
    # blueberry-specific INVERSION of the woody-ornamental gate: a real chill_hours_required
    # is LEGIT (it is the gate basis), never rejected as tree machinery.
    c = well_formed(); c["chill_hours_required"] = 800
    assert not any("chill_hours_required" in v and "tree" in v for v in berries_woody_violations(c))


def test_variety_cross_pollination_rejected():
    c = well_formed()
    c["varieties"]["recommended"][0]["pollinizer"] = "Bluecrop"
    assert any("pollin" in v.lower() for v in berries_woody_violations(c))


# ---------------------------------------------------------------------------
# WI3 -- the variety-chill PRESENCE gate (a separate whole_crop_gate branch, A21).
# Locks the WI4 string->numeric migration: every recommended variety must carry a
# NUMERIC chill_hours_required + a chill_hours_range ([lo,hi] or null for a single-
# value cultivar); a STRING chill_hours (the dropped legacy form) is a violation; and
# the scalar must equal the range low end (the documented "scalar = the chill-gating
# threshold = the low end" semantic). No-op off berries_woody.
# ---------------------------------------------------------------------------

def wf_vchill():
    """A berries_woody crop whose recommended varieties carry the migrated chill shape:
    a genuine-range cultivar (range [lo,hi], required == lo) + a single-value cultivar
    (range null)."""
    c = well_formed()
    c["varieties"]["recommended"] = [
        {"name": "Duke", "type": "northern_highbush",
         "chill_hours_required": 800, "chill_hours_range": [800, 1000]},
        {"name": "Patriot", "type": "northern_highbush",
         "chill_hours_required": 1000, "chill_hours_range": None}]
    return c


def test_vchill_clean():
    assert berries_woody_variety_chill_violations(wf_vchill()) == [], \
        berries_woody_variety_chill_violations(wf_vchill())


def test_vchill_noop_off_basis():
    c = wf_vchill(); c["calendar_basis"] = "frost_anchored"
    assert berries_woody_variety_chill_violations(c) == []


def test_vchill_string_required_rejected():
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_required"] = "800"
    assert any("chill_hours_required" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_missing_required_rejected():
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_required"] = None
    assert any("chill_hours_required" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_string_chill_hours_rejected():
    # the dropped legacy string form must never reship (the WI4 lock)
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours"] = "800 to 1000"
    assert any("chill_hours" in v and "string" in v.lower()
               for v in berries_woody_variety_chill_violations(c))


def test_vchill_required_bool_rejected():
    # a bool is not a numeric chill value (isinstance(True, int) is True in Python)
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_required"] = True
    assert any("chill_hours_required" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_range_must_be_pair():
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_range"] = [800]
    assert any("chill_hours_range" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_range_lo_hi_order():
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_range"] = [1000, 800]
    c["varieties"]["recommended"][0]["chill_hours_required"] = 1000
    assert any("chill_hours_range" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_range_non_numeric_rejected():
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_range"] = ["lo", "hi"]
    assert any("chill_hours_range" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_range_null_ok():
    # a single-value cultivar legitimately carries a null range
    c = wf_vchill()
    assert not any("Patriot" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_range_key_required():
    # the migrated shape carries the key even for single-value cultivars (null) -- a
    # variety missing it entirely is an incomplete migration
    c = wf_vchill(); del c["varieties"]["recommended"][1]["chill_hours_range"]
    assert any("chill_hours_range" in v for v in berries_woody_variety_chill_violations(c))


def test_vchill_scalar_must_equal_range_lo():
    # the scalar is documented as the LOW end of the range (the chill-gating threshold)
    c = wf_vchill(); c["varieties"]["recommended"][0]["chill_hours_required"] = 900
    assert any("low end" in v or "range" in v for v in berries_woody_variety_chill_violations(c))


# ---------------------------------------------------------------------------
# SHRUB sub-form (elderberry, the 3rd berries_woody sub-form; 2026-07-02, decision 1).
# A multi-stem shrub: cane_type 'multistem_perennial', PARTIALLY self-fertile
# (self_fertile True), ONE type everywhere ('american_elderberry', room for european),
# NOT chill-class-typed. Option A: chill stays the gate basis (D1), the value is the
# honest winter-dormancy requirement -- never a faked gating role. Discriminated off
# cane_type, intercepting ONLY the shrub marker so the existing bush/cane routing (and
# the 'both_summer_and_everbearing' cane fruits) is untouched.
# ---------------------------------------------------------------------------

def well_formed_shrub():
    """A clean SHRUB sub-form crop, mirroring well_formed() with the shrub overrides."""
    c = well_formed()
    c["cane_type"] = "multistem_perennial"
    c["self_fertile"] = True  # partially self-fertile (honest True)
    c["varieties"]["recommended"] = [{"name": "Adams", "type": "american_elderberry"}]
    cell = c["regions"]["northern_tier"]["resolved_by_zone"]["6"]
    cell["recommended_type"] = "american_elderberry"  # one type everywhere
    return c


def test_shrub_clean():
    assert berries_woody_violations(well_formed_shrub()) == [], \
        berries_woody_violations(well_formed_shrub())


def test_shrub_chill_zero_ok():
    # a SHRUB that needs NO winter chill carries chill_hours_required 0 (0 is not None, so
    # the D1 chill-basis presence check passes) -- no gate carve-out needed. Locks that the
    # SHRUB branch accepts zero chill, not just elderberry's ~400h (Trevor's edge case).
    c = well_formed_shrub()
    c["chill_hours_required"] = 0
    assert berries_woody_violations(c) == [], berries_woody_violations(c)


def test_shrub_bad_type_rejected():
    # adversarial: a SHRUB cell recommending a type outside SHRUB_TYPE_ENUM must bounce.
    c = well_formed_shrub()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["recommended_type"] = "mystery_shrub"
    assert any("recommended_type" in v for v in berries_woody_violations(c))


def test_shrub_self_fertile_garbage_rejected():
    # adversarial: a non-bool self_fertile on a shrub must bounce (same bar as cane).
    c = well_formed_shrub(); c["self_fertile"] = "partly"
    assert any("self_fertile" in v for v in berries_woody_violations(c))


def test_shrub_coverage_invariant():
    # a valid shrub type with no matching variety trips the coverage invariant (proves the
    # SHRUB enum admits european_elderberry AND the invariant still fires for the shrub branch).
    c = well_formed_shrub()
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["recommended_type"] = "european_elderberry"
    assert any("coverage" in v and "european_elderberry" in v
               for v in berries_woody_violations(c))


def test_cane_clean():
    # regression: the _subform refactor must not disturb cane routing. A cane fixture
    # (cane_type a real non-shrub value, incl. the 'both_...' form) stays clean.
    c = well_formed()
    c["cane_type"] = "both_summer_and_everbearing"
    c["self_fertile"] = True
    c["varieties"]["recommended"] = [{"name": "Heritage", "type": "everbearing"}]
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["recommended_type"] = "everbearing"
    assert berries_woody_violations(c) == [], berries_woody_violations(c)


def test_vchill_shrub_zero_ok():
    # A21 needs NO change for a chill-less shrub: a variety with chill_hours_required 0 and a
    # null range is a valid numeric shape (0 is not None and _is_number(0) is True).
    c = well_formed_shrub()
    c["varieties"]["recommended"] = [
        {"name": "Adams", "type": "american_elderberry",
         "chill_hours_required": 0, "chill_hours_range": None}]
    assert berries_woody_variety_chill_violations(c) == [], \
        berries_woody_variety_chill_violations(c)


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
