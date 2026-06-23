#!/usr/bin/env python3
"""Blueberry (`berries_woody`, anchor 18) `calendar[]` generator + coherence gate.

DERIVED data -- a pure function of the cell's leaf_habit + bloom/harvest display windows,
like tree_calendar / berry_calendar / woody_ornamental_calendar (single source of truth ->
cannot drift). Two shapes, selected by the per-cell `leaf_habit` (deciduous where winters
are cold enough for true dormancy = northern highbush; evergreen in the warm South =
rabbiteye + southern highbush). REUSE the tree tokens -- no new token (design D3):

  DECIDUOUS (the cold-zone northern highbush): the tree deciduous cycle EXACTLY --
    dormant winter / `prune` (the dormant-season cut, the month before bloom) / `bloom` /
    `growing` / `harvest` / `care` (the month after harvest end). NEVER `season_over`
    (a woody perennial's off-season is winter dormancy, not "season over").
  EVERGREEN (the warm-South rabbiteye / southern highbush): grows year-round --
    `growing` filler with `bloom` / `harvest` / `care` (month after harvest end). NO
    `dormant` and NO `season_over` (the citrus/evergreen analog).

`berry_woody_calendar_violations(crop)` recompute-from-dates per cell and fails on any
mismatch (wired into whole_crop_gate, flip-blocking, no-op unless basis is berries_woody).
See 2026-06-22-blueberry-berries-woody-model-design.md (D2/D3/D8).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import _months, derive_tree_calendar   # DRY: parser + the deciduous cycle


def derive_deciduous_berry_woody_calendar(bloom_field, harvest_field):
    """12-token deciduous (northern highbush) calendar, or None if bloom/harvest is
    empty/unparseable. IDENTICAL to the deciduous tree cycle: dormant default; prune the
    month before bloom; bloom the bloom-open month; growing between bloom and harvest;
    harvest the display span; care the month after harvest end."""
    return derive_tree_calendar(bloom_field, harvest_field)


def derive_evergreen_berry_woody_calendar(bloom_field, harvest_field):
    """12-token evergreen (warm-South rabbiteye / southern highbush) calendar, or None if
    bloom/harvest is empty/unparseable. Grows year-round (no dormancy, never season_over):
    `growing` filler, the harvest display span, the bloom span (overwrites harvest on an
    overlap month), and `care` the month after harvest end."""
    bm, hm = _months(bloom_field), _months(harvest_field)
    if not (bm and hm):
        return None
    cal = ["growing"] * 12
    m = hm[0]                              # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    m = bm[0]                              # bloom display span (forward, wrapping; overwrites harvest)
    while True:
        cal[m] = "bloom"
        if m == bm[-1]:
            break
        m = (m + 1) % 12
    cal[(hm[-1] + 1) % 12] = "care"        # post-harvest care, the month after harvest end
    return cal


def derive_berry_woody_calendar(leaf_habit, cell):
    """Dispatch on the cell's leaf_habit, reading its bloom + harvest display fields.
    None off-enum/unparseable."""
    if leaf_habit == "deciduous":
        return derive_deciduous_berry_woody_calendar(cell.get("bloom"), cell.get("harvest"))
    if leaf_habit == "evergreen":
        return derive_evergreen_berry_woody_calendar(cell.get("bloom"), cell.get("harvest"))
    return None


def berry_woody_calendar_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis berries_woody.
    For every cell with a NON-EMPTY calendar, stored must equal the calendar derived from
    that cell's own leaf_habit + dates. Empty calendars are the Step-3.5 admission state
    (skipped)."""
    if crop.get("calendar_basis") != "berries_woody":
        return []
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            cal = cell.get("calendar") or []
            if not cal:
                continue
            lh = cell.get("leaf_habit")
            expect = derive_berry_woody_calendar(lh, cell)
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but leaf_habit/dates missing or "
                         f"unparseable (leaf_habit={lh!r})")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with leaf_habit+dates "
                         f"(leaf_habit={lh!r}); stored {cal} != derived {expect}")
    return V
