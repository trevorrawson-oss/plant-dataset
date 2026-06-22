#!/usr/bin/env python3
"""Lavender (`perennial_woody_ornamental`, anchor 14) `calendar[]` generator + coherence gate.

DERIVED data -- a pure function of the cell's grown_as + display windows, like
berry_calendar / tree_calendar (single source of truth -> cannot drift). Two shapes,
selected by the per-cell `grown_as` (perennial where the species is cold-hardy, annual /
container-overwinter in the coldest zones or for tender types):

  PERENNIAL (the woody subshrub spine): dormant winter bracketed by the frost dates;
    growing inside the frost-free season; bloom; `prune` = the hard cut-back, the month
    AFTER bloom end (shear by ~1/3, never into bare wood -- the load-bearing care act).
    A FROST-FREE perennial (no frost dates, resolved_from null) has NO dormancy and grows
    year-round -- the evergreen analog. NO harvest token (bloom IS the cut-for-use window);
    NEVER season_over (a shrub does not end).
  ANNUAL (coldest zones / tender types, replanted): plant -> growing -> bloom -> season_over.
    A replanted annual is not cut-back-to-overwinter, so NO prune / dormant token.

`woody_ornamental_calendar_violations(crop)` recompute-from-dates per cell and fails on any
mismatch (wired into whole_crop_gate A14, flip-blocking, no-op unless basis is
perennial_woody_ornamental). See 2026-06-19-lavender-woody-ornamental-model-design.md (D3/D9).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree_calendar import _months   # DRY: identical "leading month range" parser


def derive_perennial_woody_calendar(bloom_field, last_frost_field, first_frost_field):
    """12-token perennial subshrub calendar, or None if bloom is empty/unparseable.
    Frost-BEARING cells (last_frost + first_frost present) bracket winter dormancy. A FROST-FREE
    perennial (no frost dates) has NO dormancy and grows year-round -- the evergreen analog.
    `prune` (the hard cut-back) is the month after bloom end either way; no harvest token."""
    bm = _months(bloom_field)
    lf, ff = _months(last_frost_field), _months(first_frost_field)
    if not bm:
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
    m = bm[0]                              # bloom display span (forward, wrapping)
    while True:
        cal[m] = "bloom"
        if m == bm[-1]:
            break
        m = (m + 1) % 12
    cal[(bm[-1] + 1) % 12] = "prune"       # the hard cut-back, the month after bloom end
    return cal


def derive_annual_woody_calendar(plant_out_field, bloom_field):
    """12-token annual (replanted, e.g. tender type in a pot) calendar, or None if plant_out
    or bloom is empty/unparseable. The planting ENDS after bloom -> season_over fills the rest;
    no prune/dormant (a replant is not cut back to overwinter)."""
    pm, bm = _months(plant_out_field), _months(bloom_field)
    if not (pm and bm):
        return None
    cal = ["season_over"] * 12
    p, bs = pm[0], bm[0]
    cal[p] = "plant"
    m = (p + 1) % 12                       # growing: plant+1 up to bloom_start-1 (wrapping)
    while m != bs:
        cal[m] = "growing"
        m = (m + 1) % 12
    m = bm[0]                              # bloom display span (forward, wrapping)
    while True:
        cal[m] = "bloom"
        if m == bm[-1]:
            break
        m = (m + 1) % 12
    return cal


def derive_woody_ornamental_calendar(grown_as, cell):
    """Dispatch on the cell's grown_as, reading its display fields. None off-enum/unparseable."""
    if grown_as == "perennial":
        rf = cell.get("resolved_from") or {}
        return derive_perennial_woody_calendar(
            cell.get("bloom"), rf.get("last_frost"), rf.get("first_frost"))
    if grown_as == "annual":
        return derive_annual_woody_calendar(cell.get("plant_out"), cell.get("bloom"))
    return None


def woody_ornamental_calendar_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis
    perennial_woody_ornamental. For every cell with a NON-EMPTY calendar, stored must equal
    the calendar derived from that cell's own grown_as + dates. Empty calendars are the
    Step-3.5 admission state (skipped)."""
    if crop.get("calendar_basis") != "perennial_woody_ornamental":
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
            expect = derive_woody_ornamental_calendar(ga, cell)
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but grown_as/dates missing or "
                         f"unparseable (grown_as={ga!r})")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with grown_as+dates "
                         f"(grown_as={ga!r}); stored {cal} != derived {expect}")
    return V
