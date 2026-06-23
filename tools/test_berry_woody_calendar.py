#!/usr/bin/env python3
"""Deriver + coherence tests for the berries_woody (blueberry, anchor 18) calendar.
Run: python3 tools/test_berry_woody_calendar.py  ->  ALL PASS.

The blueberry calendar is DERIVED data (the tree_calendar lesson): a pure function of the
cell's leaf_habit + bloom/harvest display windows, so it cannot drift from them. Two shapes:
  - DECIDUOUS (northern highbush, cold zones): the tree cyclic vocab exactly --
    dormant winter / prune (the dormant-season cut, month before bloom) / bloom / growing /
    harvest / care (month after harvest). NEVER season_over.
  - EVERGREEN (rabbiteye + southern highbush in the warm South): growing year-round with
    bloom / harvest / care. NO dormant, NO season_over (the citrus/evergreen analog).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_woody_calendar import (
    derive_deciduous_berry_woody_calendar, derive_evergreen_berry_woody_calendar,
    derive_berry_woody_calendar, berry_woody_calendar_violations)

D, G, B, H, C, P, SO = "dormant", "growing", "bloom", "harvest", "care", "prune", "season_over"


def test_deciduous_frost_bracketed():
    # northern highbush z6: bloom Apr-May, harvest Jul-Aug -> dormant winter, prune the
    # month before bloom, single bloom-open month, growing into harvest, care after harvest.
    cal = derive_deciduous_berry_woody_calendar("Apr - May", "Jul - Aug")
    assert cal == [D, D, P, B, G, G, H, H, C, D, D, D], cal
    assert SO not in cal and "renovation" not in cal


def test_evergreen_warm_south():
    # rabbiteye south GA: bloom Mar, harvest Jun-Jul -> growing year-round, care after harvest.
    cal = derive_evergreen_berry_woody_calendar("Mar", "Jun - Jul")
    assert cal == [G, G, B, G, G, H, H, C, G, G, G, G], cal
    assert D not in cal and SO not in cal


def test_none_on_empty():
    assert derive_deciduous_berry_woody_calendar("", "Jul - Aug") is None
    assert derive_deciduous_berry_woody_calendar("Apr - May", "") is None
    assert derive_evergreen_berry_woody_calendar("Mar", "") is None
    assert derive_evergreen_berry_woody_calendar("", "Jun - Jul") is None


def test_dispatch_reads_leaf_habit():
    dcell = {"leaf_habit": "deciduous", "bloom": "Apr - May", "harvest": "Jul - Aug"}
    assert derive_berry_woody_calendar("deciduous", dcell) == [D, D, P, B, G, G, H, H, C, D, D, D]
    ecell = {"leaf_habit": "evergreen", "bloom": "Mar", "harvest": "Jun - Jul"}
    assert derive_berry_woody_calendar("evergreen", ecell) == [G, G, B, G, G, H, H, C, G, G, G, G]
    assert derive_berry_woody_calendar("semi_evergreen", ecell) is None


def test_coherence_noop_off_basis():
    crop = {"calendar_basis": "frost_anchored", "regions": {}}
    assert berry_woody_calendar_violations(crop) == []


def _crop(cell):
    return {"calendar_basis": "berries_woody",
            "regions": {"northern_tier": {"resolved_by_zone": {"6": cell}}}}


def test_coherence_clean():
    cell = {"leaf_habit": "deciduous", "bloom": "Apr - May", "harvest": "Jul - Aug",
            "calendar": [D, D, P, B, G, G, H, H, C, D, D, D]}
    assert berry_woody_calendar_violations(_crop(cell)) == []


def test_coherence_skips_empty_calendar():
    # an empty calendar is the Step-3.5 admission state -- not a violation
    cell = {"leaf_habit": None, "calendar": []}
    assert berry_woody_calendar_violations(_crop(cell)) == []


def test_coherence_flags_drift():
    drift = [D, D, P, B, G, G, H, H, C, D, D, D]
    drift[2] = D  # prune hand-edited away
    cell = {"leaf_habit": "deciduous", "bloom": "Apr - May", "harvest": "Jul - Aug",
            "calendar": drift}
    v = berry_woody_calendar_violations(_crop(cell))
    assert len(v) == 1 and "northern_tier" in v[0] and "6" in v[0] and "incoherent" in v[0], v


def test_coherence_flags_unparseable():
    cell = {"leaf_habit": "deciduous", "bloom": "", "harvest": "Jul - Aug",
            "calendar": [D] * 12}  # non-empty calendar but no parseable bloom
    v = berry_woody_calendar_violations(_crop(cell))
    assert len(v) == 1 and "missing or" in v[0], v


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print("ok", n)
    print("ALL PASS")
