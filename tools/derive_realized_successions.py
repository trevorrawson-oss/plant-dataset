#!/usr/bin/env python3
"""Derive resolved_by_zone.<z>.successions_realized -- the per-zone count of distinct
sowings a zone's season supports at the crop's cadence.

Spec: 05-methodology/current/succession_realized_count_spec (v1.1, gap-aware,
LOCKED 2026-06-15). The crop-level succession_policy.successions cap is lossy: the
realized count is season-length-driven and therefore zone-dependent (lettuce runs
~7-12 in long zones vs a single crop-level cap). This deriver computes the honest
per-zone integer; it never re-sources -- it reads the SAME resolved windows the
calendar already carries.

Derivation per cell (first match wins; ALL outcomes capped at 12):
  1. year_round cell        -> min(floor(52 / interval_weeks), 12)
  2. authored sow-date lists -> min(count(succession_spring) + count(succession_fall), 12)
                                (carrot/lettuce northern_tier already enumerate the
                                 realized sowings day-precise -- the ground truth)
  3. else, day-precise       -> the authoritative sow window is
                                [first_plant_date, last_plant_date] (wrap-aware).
                                Split it ONLY at internal heat_pause/cold_pause months
                                (NOT harvest/growing/indoors tokens -- those are still
                                inside a continuous sow window). Sum, per sub-window,
                                floor(span_days / (interval_weeks * 7)) + 1. Cap at 12.

The CAP is global (Trevor 2026-06-15): the raw floor reads absurd for long warm
windows (lettuce coastal CA -> 20), the same reason the year_round cell is capped.

Scope: crops with succession_policy.suitable == True, region-filled, not indoor
(non_seasonal_indoor / zone_independent crops have no frost window -> N/A). cherry/
beefsteak are suitable=False (second_planting != succession) -> excluded by scope.

Strictly additive: only successions_realized is added per cell; succession_policy
.successions and .max_successions_per_season are set to max-over-zones (LOCK #4, keep
both). No existing value is changed, so the certs stay launch_ready (schema-2.9
precedent).

Usage:
  python3 tools/derive_realized_successions.py [--check] [slug ...] [path]
    (no slugs -> the 4 in-scope succession crops; default path crops_data_final.json)
    --check : report what WOULD change, write nothing (exit 1 if anything is stale).
"""
import json
import math
import sys

CAP = 12
_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]  # DOY before month i (non-leap)
_MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
           "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
_PAUSE_TOKENS = {"heat_pause", "cold_pause"}
DEFAULT_SLUGS = ("carrot", "basil", "lettuce-leaf", "zinnia")


def _doy(s):
    """'Apr 24' -> day-of-year (1..365), or None if not a 'Mon DD' date."""
    if not isinstance(s, str):
        return None
    p = s.split()
    if len(p) != 2 or p[0] not in _MONTHS:
        return None
    try:
        return _CUM[_MONTHS[p[0]] - 1] + int(p[1])
    except ValueError:
        return None


def _month_index(doy):
    """0-based month (Jan=0) of a day-of-year."""
    for i in range(12):
        if doy <= _CUM[i] + _MONTH_DAYS[i]:
            return i
    return 11


def _list_count(s):
    return len([x for x in s.split(",") if x.strip()]) if isinstance(s, str) and s.strip() else 0


def derive_cell_realized(cell, interval_weeks):
    """Return successions_realized for one resolved_by_zone cell, or None if the cell
    carries no resolvable sow window (an unfilled shell). Pure; deterministic."""
    iw = interval_weeks
    if not isinstance(iw, int) or iw <= 0:
        return None

    # rule 1: a genuinely pauseless year-round cell
    if cell.get("year_round") is True:
        return min(math.floor(52 / iw), CAP)

    # rule 2: authored per-zone sow-date lists are the ground truth where they exist
    n = _list_count(cell.get("succession_spring")) + _list_count(cell.get("succession_fall"))
    if n:
        return min(n, CAP)

    # rule 3: day-precise span [first_plant_date, last_plant_date], split on internal pauses
    fp, lp = _doy(cell.get("first_plant_date")), _doy(cell.get("last_plant_date"))
    if fp is None or lp is None:
        return None
    pause_months = {i for i, t in enumerate(cell.get("calendar") or []) if t in _PAUSE_TOKENS}
    span_total = (lp - fp) % 365  # inclusive window is span_total + 1 days, wrap-aware
    plantable = [d for d in (((fp - 1 + k) % 365) + 1 for k in range(span_total + 1))
                 if _month_index(d) not in pause_months]
    if not plantable:
        return None
    # contiguous runs in window order (a pause month cuts the run)
    runs, run = [], [plantable[0]]
    window = [((fp - 1 + k) % 365) + 1 for k in range(span_total + 1)]
    plantable_set = set(plantable)
    runs, run = [], []
    for d in window:
        if d in plantable_set:
            run.append(d)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    total = sum(math.floor((len(r) - 1) / (iw * 7)) + 1 for r in runs)
    return min(total, CAP)


def crop_in_scope(crop):
    """A crop is in scope iff it is succession-suitable, NOT indoor, and region-filled
    (has at least one resolved cell carrying a window). microgreens-mix is suitable but
    indoor (N/A); cherry/beefsteak are suitable=False (second_planting != succession)."""
    sp = crop.get("succession_policy") or {}
    if sp.get("suitable") is not True:
        return False
    if crop.get("calendar_basis") == "non_seasonal_indoor" or crop.get("zone_independent"):
        return False
    for r in (crop.get("regions") or {}).values():
        for cell in (r.get("resolved_by_zone") or {}).values():
            if isinstance(cell, dict) and (
                cell.get("year_round") or cell.get("calendar")
                or cell.get("succession_spring") or cell.get("succession_fall")
                or cell.get("first_plant_date")
            ):
                return True
    return False


def backfill_crop(crop):
    """Set successions_realized on every derivable cell + reconcile the crop-level cap
    (LOCK #4: successions AND max_successions_per_season := max over zones). Mutates in
    place; strictly additive. Returns a summary dict. No-op (in_scope False) off-scope."""
    if not crop_in_scope(crop):
        return {"slug": crop.get("slug"), "in_scope": False, "changed": []}
    iw = crop["succession_policy"]["interval_weeks"]
    realized, changed = [], []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            v = derive_cell_realized(cell, iw)
            if v is None:
                continue
            realized.append(v)
            if cell.get("successions_realized") != v:
                changed.append(f"{rk}.{z}: {cell.get('successions_realized')} -> {v}")
            cell["successions_realized"] = v
    if realized:
        mx = max(realized)
        sp = crop["succession_policy"]
        if sp.get("successions") != mx:
            changed.append(f"succession_policy.successions: {sp.get('successions')} -> {mx}")
        if sp.get("max_successions_per_season") != mx:
            changed.append(
                f"succession_policy.max_successions_per_season: {sp.get('max_successions_per_season')} -> {mx}")
        sp["successions"] = mx
        sp["max_successions_per_season"] = mx
    return {"slug": crop.get("slug"), "in_scope": True,
            "cells": len(realized), "max": max(realized) if realized else None,
            "changed": changed}


def _main(argv):
    check = "--check" in argv
    argv = [a for a in argv if a != "--check"]
    json_args = [a for a in argv if a.endswith(".json")]
    path = json_args[-1] if json_args else "crops_data_final.json"
    slugs = [a for a in argv if not a.endswith(".json")] or list(DEFAULT_SLUGS)

    data = json.load(open(path))
    by_slug = {c.get("slug"): c for c in data["crops"]}
    any_change = False
    for slug in slugs:
        crop = by_slug.get(slug)
        if crop is None:
            print(f"  {slug}: NOT FOUND")
            continue
        summary = backfill_crop(crop)
        if not summary["in_scope"]:
            print(f"  {slug}: out of scope (not suitable / indoor / unfilled) -- skipped")
            continue
        any_change = any_change or bool(summary["changed"])
        print(f"  {slug}: {summary['cells']} cells, crop-max={summary['max']}, "
              f"{len(summary['changed'])} change(s)")
        for c in summary["changed"]:
            print(f"      {c}")
    if check:
        print("\n--check: stale" if any_change else "\n--check: up to date")
        return 1 if any_change else 0
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)  # canonical: COMPACT
    print(f"\nwrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
