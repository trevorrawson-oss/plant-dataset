#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compound_population_gate import empty_compound_violations, content_count


def well_formed():
    """An outdoor crop with every required consumer compound populated."""
    return {
        "calendar_basis": "frost_anchored",
        "tips_by_stage": {"seedling": [{"text": "t"}], "harvest": [{"text": "t"}]},
        "growth_stages": [{"id": "x"}],
        "notifications": [{"id": "n"}],
        "weather_triggers": [{"id": "w"}],
        "pests": [{"name": "p"}],
        "diseases": [{"name": "d"}],
        "failure_diagnostics": [{"id": "f"}],
    }


def test_content_count_recurses_dict_of_lists():
    assert content_count({"established": [], "harvest": []}) == 0      # the strawberry trap
    assert content_count({"established": [{"x": 1}], "harvest": []}) == 1
    assert content_count([]) == 0
    assert content_count([1, 2]) == 2
    assert content_count(None) is None


def test_clean_when_all_populated():
    assert empty_compound_violations(well_formed()) == []


def test_flags_tips_dict_of_empty_lists():
    c = well_formed()
    c["tips_by_stage"] = {"established": [], "harvest": []}            # exactly the shipped bug
    v = empty_compound_violations(c)
    assert any(x.startswith("tips_by_stage") and "EMPTY" in x for x in v), v


def test_flags_empty_list_compound():
    c = well_formed()
    c["pests"] = []
    assert any(x.startswith("pests") and "EMPTY" in x for x in empty_compound_violations(c))


def test_flags_absent_compound():
    c = well_formed()
    del c["diseases"]
    assert any(x.startswith("diseases") and "absent" in x for x in empty_compound_violations(c))


def test_outdoor_requires_weather_triggers():
    c = well_formed()
    c["weather_triggers"] = []
    assert any(x.startswith("weather_triggers") for x in empty_compound_violations(c))


def test_indoor_exempts_weather_triggers():
    c = well_formed()
    c["calendar_basis"] = "non_seasonal_indoor"
    c["weather_triggers"] = []                                        # legitimately N/A indoors
    assert not any(x.startswith("weather_triggers") for x in empty_compound_violations(c))


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
