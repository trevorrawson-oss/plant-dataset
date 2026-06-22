#!/usr/bin/env python3
"""Deriver + coherence tests for the woody-ornamental (lavender, anchor 14) calendar.
Run: python3 tools/test_woody_ornamental_calendar.py  ->  ALL PASS."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from woody_ornamental_calendar import (
    derive_perennial_woody_calendar, derive_annual_woody_calendar,
    derive_woody_ornamental_calendar, woody_ornamental_calendar_violations)

D, G, B, P, SO, PL = "dormant", "growing", "bloom", "prune", "season_over", "plant"


def test_perennial_frost_bracketed():
    # bloom Jun-Jul, frost-free Apr..Oct -> dormant winter, prune the month after bloom
    cal = derive_perennial_woody_calendar("Jun - Jul", "Apr", "Oct")
    assert cal == [D, D, D, G, G, B, B, P, G, G, D, D], cal


def test_perennial_frost_free():
    # no frost dates -> grows year-round, bloom Feb-Apr, prune May (the evergreen analog)
    cal = derive_perennial_woody_calendar("Feb - Apr", None, None)
    assert cal == [G, B, B, B, P, G, G, G, G, G, G, G], cal


def test_annual_fall_plant_overwinter():
    # plant Oct, bloom Apr-May -> season_over fills the gap, no prune
    cal = derive_annual_woody_calendar("Oct", "Apr - May")
    assert cal == [G, G, G, B, B, SO, SO, SO, SO, PL, G, G], cal


def test_none_on_empty():
    assert derive_perennial_woody_calendar("", "Apr", "Oct") is None
    assert derive_annual_woody_calendar("Oct", "") is None


def test_dispatch_perennial_and_annual():
    pcell = {"grown_as": "perennial", "bloom": "Jun - Jul",
             "resolved_from": {"last_frost": "Apr", "first_frost": "Oct"}}
    assert derive_woody_ornamental_calendar("perennial", pcell) == [D, D, D, G, G, B, B, P, G, G, D, D]
    acell = {"grown_as": "annual", "plant_out": "Oct", "bloom": "Apr - May"}
    assert derive_woody_ornamental_calendar("annual", acell) == [G, G, G, B, B, SO, SO, SO, SO, PL, G, G]
    assert derive_woody_ornamental_calendar("biennial", acell) is None


def test_dispatch_and_coherence_noop_off_basis():
    crop = {"calendar_basis": "frost_anchored", "regions": {}}
    assert woody_ornamental_calendar_violations(crop) == []


def test_coherence_clean():
    cell = {"grown_as": "perennial", "bloom": "Jun - Jul",
            "resolved_from": {"last_frost": "Apr", "first_frost": "Oct"},
            "calendar": [D, D, D, G, G, B, B, P, G, G, D, D]}
    crop = {"calendar_basis": "perennial_woody_ornamental",
            "regions": {"r": {"resolved_by_zone": {"6": cell}}}}
    assert woody_ornamental_calendar_violations(crop) == []


def test_coherence_skips_empty_calendar():
    # an empty calendar is the Step-3.5 admission state -- not a violation
    cell = {"grown_as": None, "calendar": []}
    crop = {"calendar_basis": "perennial_woody_ornamental",
            "regions": {"r": {"resolved_by_zone": {"6": cell}}}}
    assert woody_ornamental_calendar_violations(crop) == []


def test_coherence_flags_mismatch():
    cell = {"grown_as": "perennial", "bloom": "Jun - Jul",
            "resolved_from": {"last_frost": "Apr", "first_frost": "Oct"},
            "calendar": [D] * 12}  # wrong
    crop = {"calendar_basis": "perennial_woody_ornamental",
            "regions": {"r": {"resolved_by_zone": {"6": cell}}}}
    v = woody_ornamental_calendar_violations(crop)
    assert len(v) == 1 and "incoherent" in v[0], v


def test_coherence_flags_unparseable():
    cell = {"grown_as": "perennial", "bloom": "",
            "resolved_from": {"last_frost": "Apr", "first_frost": "Oct"},
            "calendar": [D] * 12}  # non-empty calendar but no parseable bloom
    crop = {"calendar_basis": "perennial_woody_ornamental",
            "regions": {"r": {"resolved_by_zone": {"6": cell}}}}
    v = woody_ornamental_calendar_violations(crop)
    assert len(v) == 1 and "missing or" in v[0], v


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
