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


def photoperiod_violations(crop):
    """Return a list of violation strings for a photoperiod-gated crop ([] = clean).
    No-op (returns []) unless "photoperiod" is in the crop's gating_factors. A null
    `recommended_day_length_type` on a cell is the Step-3.5 admission state (skipped --
    whole_crop_gate A2 owns "this region is unauthored"); A9 enforces typing + coverage
    only on FILLED cells, exactly as the perennial branch skips a null `suitability`."""
    if "photoperiod" not in (crop.get("gating_factors") or []):
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
                continue  # Step-3.5 admission state -- A2 owns region-fill
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
