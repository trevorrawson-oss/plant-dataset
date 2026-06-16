#!/usr/bin/env python3
"""Photoperiod (day-length) cert-gate branch -- the A9 invariants for a photoperiod-gated
crop (onion, anchor 12; the allium family inherits it). Fires ONLY for a crop with
"photoperiod" in gating_factors (a no-op otherwise). Imported + run by whole_crop_gate.py.

See onion-photoperiod-model-design.md. The COVERAGE invariant is the load-bearing rule:
every day-length type a region RESOLVES to must have >=1 recommended variety carrying it,
so the page can never say "grow short-day here" with zero short-day varieties on it.
"""
DAY_LENGTH_ENUM = {"long_day", "intermediate_day", "short_day"}


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
    return V
