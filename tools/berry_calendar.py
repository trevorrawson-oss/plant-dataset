#!/usr/bin/env python3
"""Strawberry (`berries_herbaceous`, anchor 13) `calendar[]` generator + coherence gate.

The strawberry calendar is DERIVED data -- a pure function of the cell's grown_as +
display windows -- not independent information, exactly like the tree calendar. Two shapes,
selected by the per-cell `grown_as` (perennial in the north, annual in hot-summer CA/FL):

  PERENNIAL (June-bearing matted-row spine): dormant winter bracketed by the frost dates;
    growing inside the frost-free season; bloom; harvest; renovation = the month after
    harvest end (mow + thin the row). Never season_over (a perennial bed does not end).
  ANNUAL (CA interior/desert + FL): plant in fall; growing; bloom; harvest; the planting
    then ENDS -> season_over fills the rest. Never renovation/dormant.

`berry_calendar_violations(crop)` recompute-from-dates per cell and fails on any mismatch
(wired into whole_crop_gate, flip-blocking, no-op unless basis is perennial_herbaceous).
See 2026-06-18-strawberry-berries-herbaceous-model-design.md (D2/D4/D9).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import _months   # DRY: identical "leading month range" parser


def derive_perennial_berry_calendar(bloom_field, harvest_field, last_frost_field, first_frost_field):
    """12-token perennial matted-row calendar, or None if bloom/harvest is empty/unparseable.
    Frost-BEARING cells (last_frost + first_frost present) bracket winter dormancy. A FROST-FREE
    perennial (e.g. hawaii upcountry: no frost dates, resolved_from null) has NO dormancy and grows
    year-round -- the evergreen analog. Renovation is the month after harvest end either way."""
    bm, hm = _months(bloom_field), _months(harvest_field)
    lf, ff = _months(last_frost_field), _months(first_frost_field)
    if not (bm and hm):
        return None
    if not (lf and ff):
        cal = ["growing"] * 12             # frost-free perennial: no dormancy, grows year-round
    else:
        cal = ["dormant"] * 12
        m = lf[0]                          # frost-free growing season (last_frost .. first_frost)
        while True:
            cal[m] = "growing"
            if m == ff[-1]:
                break
            m = (m + 1) % 12
    m = hm[0]                              # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    cal[bm[0]] = "bloom"
    cal[(hm[-1] + 1) % 12] = "renovation"  # mow + thin the month after the June flush
    return cal


def derive_annual_berry_calendar(plant_out_field, bloom_field, harvest_field):
    """12-token annual (fall-plant, winter-wrap) calendar, or None if plant_out or harvest
    is empty/unparseable. The planting ENDS after harvest -> season_over fills the rest."""
    pm, hm = _months(plant_out_field), _months(harvest_field)
    if not (pm and hm):
        return None
    cal = ["season_over"] * 12
    p, hs = pm[0], hm[0]
    cal[p] = "plant"
    m = (p + 1) % 12                       # growing: plant+1 up to harvest_start-1 (wrapping)
    while m != hs:
        cal[m] = "growing"
        m = (m + 1) % 12
    m = hs                                 # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    bm = _months(bloom_field)              # bloom overlay (a month within the pre-harvest run)
    if bm:
        cal[bm[0]] = "bloom"
    return cal


def derive_berry_calendar(grown_as, cell):
    """Dispatch on the cell's grown_as, reading its display fields. None off-enum/unparseable."""
    if grown_as == "perennial":
        rf = cell.get("resolved_from") or {}
        return derive_perennial_berry_calendar(
            cell.get("bloom"), cell.get("harvest"), rf.get("last_frost"), rf.get("first_frost"))
    if grown_as == "annual":
        return derive_annual_berry_calendar(
            cell.get("plant_out"), cell.get("bloom"), cell.get("harvest"))
    return None


def berry_calendar_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis perennial_herbaceous.
    For every cell with a NON-EMPTY calendar, stored must equal the calendar derived from that
    cell's own grown_as + dates. Empty calendars are the Step-3.5 admission state (skipped)."""
    if crop.get("calendar_basis") != "perennial_herbaceous":
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
            ga = cell.get("grown_as")
            expect = derive_berry_calendar(ga, cell)
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but grown_as/dates missing or "
                         f"unparseable (grown_as={ga!r})")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with grown_as+dates "
                         f"(grown_as={ga!r}); stored {cal} != derived {expect}")
    return V
