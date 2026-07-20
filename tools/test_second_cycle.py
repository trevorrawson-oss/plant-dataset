#!/usr/bin/env python3
"""Unit tests for second_cycle.py -- the fall-cycle (two-cycle) cell-building helper
(ADDENDUM to Task 2 of the 2026-07-20 Mid-Atlantic region arc).

Why this helper exists: `annual_calendar.derive_annual_calendar` reads only the TOP-LEVEL
`plant_out`/`harvest`/`start_indoors` -- it does NOT read `second_planting`. A roster-wide
check found all 272 existing `second_planting` cells have a stored `calendar[]` that does
NOT re-derive from their split storage form: the real two-cycle calendars are built from
COMBINED (comma-joined) windows, THEN the windows are split into a single-span primary +
nested `second_planting` (A43 forbids storing the comma shape). `build_two_cycle_cell`
makes that combined-derive-then-split deterministic. Full detail:
docs/reviews/notes/2026-07-20/mid_atlantic_sources.md Section 8.

Fixture note: the cherry-tomato-shaped input mirrors the addendum brief's example, with
one internal-consistency fix -- `spring["harvest"]` is `"Jun - Aug"` (not the brief's literal
`"Jun - Jul"`), because `spring["harvest_end"]` is `"Aug 1"`: a display string must cover its
own `harvest_end` (the real `cherry-tomato.regions.se_gulf.z8` cell and the Mid-Atlantic cell
contract's own worked example both hold this invariant -- e.g. contract section 2.5's z8 row
has `harvest: "Jun 16 - Jun 30"` with `harvest_end: "Jun 30"`, never a display that undershoots
harvest_end). A43's Rule A envelope check (`harvest_end` must parse INSIDE the first harvest
span) is exactly what would catch a real crop shipping the brief's literal inconsistent pair,
so the fixture here is deliberately the sourceable-shape version of that same example.

Run from repo root: cd tools && python3 -m pytest test_second_cycle.py -v
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import second_cycle
import second_planting_gate


def _cherry_tomato_fixture():
    base = {
        "region_id": "mid_atlantic",
        "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
        "zone_span": ["7", "8"],
        "resolution_method": "frost_anchored_resolved",
        "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30"},
        "sources": ["vce_426_331"],
    }
    spring = {
        "start_indoors": "Mar 4 - Mar 18",
        "plant_out": "Apr 15 - May 1",
        "harvest": "Jun - Aug",
        "harvest_start": "Jun 25",
        "harvest_end": "Aug 1",
        "first_plant_date": "Apr 15",
        "last_plant_date": "May 1",
    }
    fall = {
        "start_indoors": "Jun 1 - Jun 15",
        "plant_out": "Jul 1 - Aug 10",
        "harvest_start": "Sep 15",
        "harvest_end": "Oct 25",
    }
    return base, spring, fall


def test_two_cycle_cell_shape_and_calendar_and_gate():
    base, spring, fall = _cherry_tomato_fixture()
    result = second_cycle.build_two_cycle_cell(base, spring, fall)

    # (a) second_planting == the fall dict verbatim
    assert result["second_planting"] == fall

    # base fields present verbatim at the top level too
    assert result["region_id"] == "mid_atlantic"
    assert result["region_label"] == "Mid-Atlantic: Piedmont and Coastal Plain"
    assert result["zone_span"] == ["7", "8"]
    assert result["resolution_method"] == "frost_anchored_resolved"
    assert result["resolved_from"] == {"last_frost": "Apr 8", "first_frost": "Oct 30"}
    assert result["sources"] == ["vce_426_331"]
    # spring fields present verbatim at the top level
    for k, v in spring.items():
        assert result[k] == v, f"top-level {k!r} != spring[{k!r}]"

    # (b) top-level plant_out / harvest are single-span (no comma) -- the primary cycle only
    assert "," not in result["plant_out"]
    assert "," not in result["harvest"]

    # (c) calendar has a harvest token in a FALL month (Sep idx 8 / Oct idx 9) AND a
    # spring/summer month (Jun idx 5 / Jul idx 6) -- proving BOTH cycles render
    cal = result["calendar"]
    assert len(cal) == 12
    assert cal[8] == "harvest" or cal[9] == "harvest", cal
    assert cal[5] == "harvest" or cal[6] == "harvest", cal
    print(f"  ok: two-cycle calendar renders both cycles: {cal}")

    # (d) A43 passes: a minimal crop shaped around this cell returns zero violations
    crop = {
        "slug": "cherry-tomato",
        "succession_policy": {"suitable": True},
        "regions": {"mid_atlantic": {"resolved_by_zone": {"8": result}}},
    }
    v = second_planting_gate.check_crop(crop, rules=frozenset("AB"))
    assert v == [], v
    print("  ok: second_planting_gate.check_crop (A43, rules AB) returns zero violations")


def test_two_cycle_cell_omits_second_planting_start_indoors_when_absent():
    # a fall cycle legitimately has no separate start_indoors (direct-sow fall crop, e.g.
    # beans/cucumbers/squash per the VCE table) -- the helper must not fabricate one.
    base, spring, fall = _cherry_tomato_fixture()
    del fall["start_indoors"]
    result = second_cycle.build_two_cycle_cell(base, spring, fall)
    assert "start_indoors" not in result["second_planting"]
    assert result["second_planting"] == fall
    cal = result["calendar"]
    assert len(cal) == 12
    assert cal[8] == "harvest" or cal[9] == "harvest", cal
    print("  ok: fall cycle with no start_indoors (direct-sow) still renders cleanly")


if __name__ == "__main__":
    test_two_cycle_cell_shape_and_calendar_and_gate()
    test_two_cycle_cell_omits_second_planting_start_indoors_when_absent()
    print("\nALL second_cycle TESTS PASSED")
