#!/usr/bin/env python3
"""Photoperiod (day-length) cert-gate branch -- the A9 invariants for a photoperiod-gated
crop (onion, anchor 12; the allium family inherits it). Fires ONLY for a crop with
"photoperiod" in gating_factors (a no-op otherwise). Imported + run by whole_crop_gate.py.

See onion-photoperiod-model-design.md. The COVERAGE invariant is the load-bearing rule:
every day-length type a region RESOLVES to must have >=1 recommended variety carrying it,
so the page can never say "grow short-day here" with zero short-day varieties on it.

B4 adds WINDOW FIT: a cell's day_length_type must agree with its planting-season shape
(long-day onions are spring-planted to bulb in summer's long days; short-day onions are
fall/winter-planted to bulb as short winter days lengthen -- the two are opposite). Keyed
on plant_out only; harvest shape is intentionally NOT checked (overstated harvest displays
would false-positive). 0 FP across onion's 20 real cells.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annual_calendar import parse_months

DAY_LENGTH_ENUM = {"long_day", "intermediate_day", "short_day"}

# Month sets for the planting-season window-fit (B4).
_SPRING = {3, 4, 5, 6}              # long-day onions transplant in spring
_FALL = {9, 10, 11}                 # long-day onions are NOT fall-planted
_SPRING_SUMMER = {3, 4, 5, 6, 7, 8}  # short-day onions avoid these (strictly fall/winter)
_LATE_SPRING_SUMMER = {4, 5, 6, 7, 8}  # intermediate-day onions avoid these (allows March)


def _plant_months(cell):
    """plant_out -> set of month numbers, tolerating 'early/mid/late <Month>' qualifiers
    ('Jan - early March' -> Jan..Mar). Empty set if absent/unparseable."""
    s = cell.get("plant_out")
    if not isinstance(s, str):
        return set()
    s = re.sub(r"(?i)\b(early|mid|late)[\s-]+", "", s)
    return parse_months(s)


def _window_fit_violation(rdlt, P):
    """One window-fit violation suffix for a (type, plant-month set), or None if it fits.
    Caller skips when P is empty (no parseable plant_out)."""
    months = sorted(P)
    if rdlt == "long_day":
        if not (P & _SPRING):
            return (f"long_day but plant_out window {months} is not spring-planted "
                    f"(long-day onions transplant in spring to bulb in summer's long days)")
        if P & _FALL:
            return (f"long_day but plant_out window {months} includes fall months "
                    f"(long-day onions are spring-planted, not fall-planted)")
    elif rdlt == "short_day":
        if P & _SPRING_SUMMER:
            return (f"short_day but plant_out window {months} includes spring/summer months "
                    f"(short-day onions are fall/winter-planted, bulbing as short days lengthen)")
    elif rdlt == "intermediate_day":
        if P & _LATE_SPRING_SUMMER:
            return (f"intermediate_day but plant_out window {months} includes late-spring/summer "
                    f"months (intermediate-day onions are fall-to-early-spring-planted)")
    return None


def _has_day_length_machinery(crop):
    """True if the crop carries a NON-NULL day_length_type (variety) or
    recommended_day_length_type (resolved cell) anywhere -- i.e. it declares day-length
    typing, which ONLY this gate validates. Used to require the 'photoperiod' gating token
    (a crop carrying real types but no token would silently no-op the whole gate -- C5)."""
    vs = (crop.get("varieties") or {}).get("recommended") or []
    if any(isinstance(v, dict) and v.get("day_length_type") is not None for v in vs):
        return True
    for r in (crop.get("regions") or {}).values():
        if not isinstance(r, dict):
            continue
        for cell in (r.get("resolved_by_zone") or {}).values():
            if isinstance(cell, dict) and cell.get("recommended_day_length_type") is not None:
                return True
    return False


def photoperiod_violations(crop):
    """Return a list of violation strings for a photoperiod-gated crop ([] = clean).
    No-op (returns []) unless "photoperiod" is in the crop's gating_factors -- EXCEPT a crop
    that carries day-length machinery without the token is itself a violation (C5: dropping the
    token silently disables variety typing + coverage + window-fit while the types still render).
    A null `recommended_day_length_type` on an UNFILLED cell is the Step-3.5 admission state
    (skipped -- whole_crop_gate A2 owns "this region is unauthored"); but a null type on a
    FILLED cell (one that carries a calendar) evades coverage while still rendering, so it is
    flagged. A9 enforces typing + coverage only on filled cells, like the perennial branch."""
    if "photoperiod" not in (crop.get("gating_factors") or []):
        # C5 (incognito-redteam 2026-06-27): a crop carrying NON-NULL day-length machinery but
        # missing the token would no-op this entire gate -- require the token in that case.
        if _has_day_length_machinery(crop):
            return ["gating_factors must contain 'photoperiod': the crop carries day_length_type "
                    "machinery (variety and/or resolved cell), which ONLY A9 validates; dropping "
                    "the token silently disables variety typing, the coverage invariant, and "
                    "window-fit. got %r" % (crop.get("gating_factors"),)]
        return []
    V = []

    # 1. VARIETY TYPING -- every recommended variety is an object with a valid type.
    variety_types = set()
    vs = (crop.get("varieties") or {}).get("recommended") or []
    for i, v in enumerate(vs):
        if not isinstance(v, dict):
            V.append(f"varieties.recommended[{i}]: a photoperiod crop needs object-shaped "
                     f"varieties with day_length_type, got {type(v).__name__}")
            continue
        dlt = v.get("day_length_type")
        if dlt not in DAY_LENGTH_ENUM:
            V.append(f"varieties.recommended[{i}] ({v.get('name')!r}): day_length_type "
                     f"{dlt!r} not in {sorted(DAY_LENGTH_ENUM)}")
        else:
            variety_types.add(dlt)

    # 2. CELL TYPING -- every FILLED resolved cell's recommended_day_length_type is valid.
    resolved_types = set()
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            rdlt = cell.get("recommended_day_length_type")
            if rdlt is None:
                # C5: a null type is the Step-3.5 admission state ONLY on an UNFILLED cell. A
                # FILLED cell (carries a calendar that renders) with a null type evades coverage
                # + window-fit while the page still shows a calendar -- flag it. A2 owns the
                # truly-unfilled (no-calendar) cells.
                if cell.get("calendar"):
                    V.append(f"{rk}.{z}: filled cell (carries a calendar) has a null "
                             f"recommended_day_length_type -- evades the coverage invariant; a "
                             f"photoperiod crop must type every cell it renders a calendar for")
                continue
            if rdlt not in DAY_LENGTH_ENUM:
                V.append(f"{rk}.{z}: recommended_day_length_type {rdlt!r} not in "
                         f"{sorted(DAY_LENGTH_ENUM)}")
            else:
                resolved_types.add(rdlt)

    # 3. COVERAGE INVARIANT -- every resolved type has >=1 matching recommended variety.
    for t in sorted(resolved_types - variety_types):
        V.append(f"coverage: region(s) resolve to {t!r} but no recommended variety carries "
                 f"that day_length_type")

    # 4. WINDOW FIT (B4) -- a filled cell's day_length_type must agree with its plant_out
    # season shape. Skips cells with no parseable plant_out (not this gate's concern).
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            rdlt = cell.get("recommended_day_length_type")
            if rdlt not in DAY_LENGTH_ENUM:
                continue  # null (admission state) or bad type already flagged in (2)
            P = _plant_months(cell)
            if not P:
                continue  # no parseable plant_out -> cannot assess fit
            suffix = _window_fit_violation(rdlt, P)
            if suffix:
                V.append(f"{rk}.{z}: {suffix}")
    return V
