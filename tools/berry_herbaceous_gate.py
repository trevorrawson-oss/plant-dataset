#!/usr/bin/env python3
"""Berries_herbaceous structural cert branch (strawberry, anchor 13; the ONLY crop with
this archetype). Fires ONLY for calendar_basis == perennial_herbaceous (a no-op otherwise).
Imported + run by whole_crop_gate.py as section A10. The calendar coherence (stored ==
derived) is the SEPARATE A11 (berry_calendar.berry_calendar_violations), mirroring how the
tree split A3 (perennial cert) from A4 (calendar coherence).

Admission-safe: the lifecycle SCALARS are Step-2 data (authored BEFORE Step 3.5 sets the
basis, so they are present whenever this gate fires, exactly as photoperiod_gate asserts
variety typing). The prose pairs (renovation_*, year_one_notes_*, type_selection_*,
grown_as_note_*) are owned by register_fill_gate at Step 11, NOT here. A per-cell grown_as
that is null AND has an empty calendar is the Step-3.5 admission state (skipped).
See 2026-06-18-strawberry-berries-herbaceous-model-design.md (D6-D9).
"""
GROWN_AS_ENUM = {"perennial", "annual"}
LIFECYCLE_SCALARS = ("establishment_years", "productive_lifespan_years",
                     "years_to_first_harvest", "years_to_full_production")
_TREE_ONLY_CELL_KEYS = ("suitability", "chill_hours_delivered")
_CROSS_POLLINATION_KEYS = ("bloom_group", "pollinizer", "pollinizer_distance_ft",
                           "bloom_window_relative")


def berry_herbaceous_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis perennial_herbaceous."""
    if crop.get("calendar_basis") != "perennial_herbaceous":
        return []
    V = []

    # 1. lifecycle SCALARS present (Step-2 data; admission-safe -- see module docstring).
    for f in LIFECYCLE_SCALARS:
        v = crop.get(f)
        if v is None or v == []:
            V.append(f"lifecycle scalar {f} empty (required once basis is perennial_herbaceous)")
    if crop.get("self_fertile") is not True:
        V.append(f"self_fertile must be true (strawberry is self-fertile, no cross-pollination "
                 f"calendar); got {crop.get('self_fertile')!r}")

    # 2. photoperiod guard -- strawberry type is a VARIETY attribute, not an onion zone gate.
    if "photoperiod" in (crop.get("gating_factors") or []):
        V.append("photoperiod must NOT be in gating_factors (strawberry type is a variety "
                 "attribute, not a latitude gate)")

    # 3. no tree cross-pollination machinery on the varieties.
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            for k in _CROSS_POLLINATION_KEYS:
                if k in v:
                    V.append(f"varieties.recommended[{i}] ({v.get('name')!r}): {k} is tree "
                             f"cross-pollination machinery; strawberry is self-fertile")

    # 4. per-cell: grown_as typing, no tree-only keys, token placement vs grown_as.
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            for tk in _TREE_ONLY_CELL_KEYS:
                if tk in cell:
                    V.append(f"{rk}.{z}: tree-only key {tk!r} present "
                             f"(mis-routed through the tree builder?)")
            ga = cell.get("grown_as")
            cal = cell.get("calendar") or []
            if ga is None and not cal:
                continue  # Step-3.5 admission state
            if ga not in GROWN_AS_ENUM:
                V.append(f"{rk}.{z}: grown_as {ga!r} not in {sorted(GROWN_AS_ENUM)}")
                continue
            if cal:
                if ga == "annual" and ("renovation" in cal or "dormant" in cal):
                    V.append(f"{rk}.{z}: annual cell carries a perennial token "
                             f"(renovation/dormant): {cal}")
                if ga == "perennial" and "season_over" in cal:
                    V.append(f"{rk}.{z}: perennial cell carries season_over "
                             f"(annual-only token): {cal}")
    return V
