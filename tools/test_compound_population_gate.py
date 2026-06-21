#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compound_population_gate import (
    empty_compound_violations, content_count, tips_violations)


def well_formed():
    """An outdoor crop with every required consumer compound populated + conformant tips."""
    return {
        "calendar_basis": "frost_anchored",
        "growth_stages": [{"id": "seedling"}, {"id": "harvest"}],
        "notifications": [{"id": "n"}],
        "weather_triggers": [{"id": "w"}],
        "pests": [{"name": "p"}],
        "diseases": [{"name": "d"}],
        "failure_diagnostics": [{"id": "f"}],
        "tips_by_stage": {
            "seedling": [{"text_seasoned": "s", "text_beginner": "b"}],
            "harvest": [{"text_seasoned": "s", "text_beginner": "b"}],
        },
    }


# ---- content_count + empty_compound_violations (the non-tips compounds) ----
def test_content_count_recurses_dict_of_lists():
    assert content_count({"established": [], "harvest": []}) == 0
    assert content_count({"established": [{"x": 1}], "harvest": []}) == 1
    assert content_count([]) == 0 and content_count([1, 2]) == 2 and content_count(None) is None


def test_empty_compound_clean():
    assert empty_compound_violations(well_formed()) == []


def test_empty_compound_flags_empty_list():
    c = well_formed(); c["pests"] = []
    assert any(x.startswith("pests") and "EMPTY" in x for x in empty_compound_violations(c))


def test_empty_compound_flags_absent():
    c = well_formed(); del c["diseases"]
    assert any(x.startswith("diseases") and "absent" in x for x in empty_compound_violations(c))


def test_outdoor_requires_weather_triggers():
    c = well_formed(); c["weather_triggers"] = []
    assert any(x.startswith("weather_triggers") for x in empty_compound_violations(c))


def test_indoor_exempts_weather_triggers():
    c = well_formed(); c["calendar_basis"] = "non_seasonal_indoor"; c["weather_triggers"] = []
    assert not any(x.startswith("weather_triggers") for x in empty_compound_violations(c))


def test_tips_no_longer_in_generic_required():
    # tips_by_stage is policed by tips_violations now, not the generic emptiness sweep
    c = well_formed(); c["tips_by_stage"] = {}
    assert not any("tips_by_stage" in x for x in empty_compound_violations(c))


# ---- tips_violations (the three rendering traps) ----
def test_tips_clean():
    assert tips_violations(well_formed()) == []


def test_tips_empty_dict_of_empty_lists():
    c = well_formed(); c["tips_by_stage"] = {"seedling": [], "harvest": []}
    assert any("EMPTY" in x for x in tips_violations(c))


def test_tips_wrong_field():
    c = well_formed()
    c["tips_by_stage"] = {"seedling": [{"tip_seasoned": "s", "tip_beginner": "b"}]}
    assert any("text_seasoned" in x for x in tips_violations(c)), tips_violations(c)


def test_tips_orphaned_key():
    c = well_formed()
    c["tips_by_stage"]["storage"] = [{"text_seasoned": "s", "text_beginner": "b"}]  # no 'storage' stage
    assert any("ORPHANED" in x and "storage" in x for x in tips_violations(c))


def test_tips_indoor_exempt():
    c = well_formed(); c["calendar_basis"] = "non_seasonal_indoor"
    c["tips_by_stage"] = {"sow": [{"tip_seasoned": "s"}]}   # wrong field, orphaned -- all OK indoors
    assert tips_violations(c) == []


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
