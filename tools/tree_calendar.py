#!/usr/bin/env python3
"""Tree `calendar[]` generator + coherence gate.

The tree calendar is DERIVED data -- a pure function of the cell's bloom + harvest
DISPLAY windows -- not independent information. Hand-authoring it (the Step-4 convention)
let it drift from those fields: apple Step 5 found 5 bloom-token + 11 harvest-token
mismatches that a by-eye verification missed. The cure is to stop authoring it:

  - `derive_tree_calendar(bloom, harvest)` GENERATES the 12-token calendar from the
    display windows (single source of truth -> cannot drift);
  - `tree_calendar_violations(crop)` GATES it -- recompute-from-dates and fail on any
    mismatch -- so an incoherent tree calendar can never ship (wired into whole_crop_gate,
    flip-blocking, exhaustive over every cell).

Sequence rule (validated: reproduces claude.ai's hand-authored apple corrections +
ca_desert z10 byte-for-byte): prune = month before bloom; bloom = bloom-open month;
growing = bloom+1 .. harvest_start-1; harvest = the harvest display span; care = month
after harvest end; dormant = the rest. Derived from the DISPLAY fields so the month
rounding already baked into those strings (e.g. "Aug 30" shown as a Sep harvest) is
inherited -- zero residual judgment here.
"""
import re

_MON = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def _months(s):
    if not isinstance(s, str):
        return []
    return [_MON[m] for m in re.findall(
        r"jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec", s.lower())]


def derive_tree_calendar(bloom_field, harvest_field):
    """Return the 12-token tree calendar derived from the bloom + harvest display
    windows, or None if either window is empty/unparseable (a no-fruit cell carries
    no calendar -- the caller / A3 owns that)."""
    bm = _months(bloom_field)
    hm = _months(harvest_field)
    if not bm or not hm:
        return None
    bloom_m, hs, he = bm[0], hm[0], hm[-1]
    cal = ["dormant"] * 12
    # harvest display span (forward, wrapping)
    m = hs
    while True:
        cal[m] = "harvest"
        if m == he:
            break
        m = (m + 1) % 12
    # growing: between bloom and the start of harvest
    m = (bloom_m + 1) % 12
    while m != hs:
        cal[m] = "growing"
        m = (m + 1) % 12
    cal[bloom_m] = "bloom"
    cal[(bloom_m - 1) % 12] = "prune"      # dormant-season prune, the month before bloom
    cal[(he + 1) % 12] = "care"            # post-harvest, the month after harvest end
    return cal


def derive_evergreen_calendar(bloom_field, harvest_field):
    """Return the 12-token EVERGREEN calendar from the bloom + harvest display windows,
    or None if either is empty/unparseable. An evergreen (citrus/avocado/olive) never
    goes dormant: bloom and harvest are the dated states and EVERYTHING ELSE is `growing`
    (never `dormant`). The harvest span may WRAP the year (citrus blooms in spring and
    is picked the following winter). bloom overwrites harvest on an overlap month --
    flowering is the notable transition, and citrus can carry flowers + ripe fruit at
    once. See tree_region_model_evergreen_amendment_v1_0 section 1."""
    bm = _months(bloom_field)
    hm = _months(harvest_field)
    if not bm or not hm:
        return None
    cal = ["growing"] * 12
    m = hm[0]                              # harvest display span (forward, wrapping)
    while True:
        cal[m] = "harvest"
        if m == hm[-1]:
            break
        m = (m + 1) % 12
    m = bm[0]                              # bloom span (forward, wrapping); overwrites harvest
    while True:
        cal[m] = "bloom"
        if m == bm[-1]:
            break
        m = (m + 1) % 12
    return cal


def tree_calendar_violations(crop):
    """Return a list of violation strings for a perennial_chill_gated crop ([] = clean).
    For every cell with a NON-EMPTY calendar, the stored calendar must equal the calendar
    derived from that cell's own bloom + harvest fields. Empty calendars are skipped (the
    no-fruit direction split in perennial_cert_violations owns emptiness). No-op for
    non-perennial crops. The deciduous basis derives via `derive_tree_calendar`; the
    evergreen basis via `derive_evergreen_calendar` (no dormancy, growing filler, wrap)."""
    basis = crop.get("calendar_basis")
    if basis not in ("perennial_chill_gated", "perennial_evergreen"):
        return []
    derive = derive_evergreen_calendar if basis == "perennial_evergreen" else derive_tree_calendar
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            cal = cell.get("calendar") or []
            if not cal:
                continue  # empty cell -- A3 (no-fruit split) owns whether it SHOULD be empty
            expect = derive(cell.get("bloom"), cell.get("harvest"))
            if expect is None:
                V.append(f"{rk}.{z}: non-empty calendar but bloom/harvest dates are "
                         f"missing/unparseable (cannot verify coherence)")
            elif cal != expect:
                V.append(f"{rk}.{z}: calendar incoherent with its bloom/harvest dates "
                         f"(bloom={cell.get('bloom')!r} harvest={cell.get('harvest')!r}); "
                         f"stored {cal} != derived {expect}")
    return V
