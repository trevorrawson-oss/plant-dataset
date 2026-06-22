#!/usr/bin/env python3
"""Woody-ornamental structural cert branch (lavender, anchor 14; the FIRST and only crop with
this archetype). Fires ONLY for calendar_basis == perennial_woody_ornamental (a no-op otherwise).
Imported + run by whole_crop_gate.py as section A13. The calendar coherence (stored == derived)
is the SEPARATE A14 (woody_ornamental_calendar.woody_ornamental_calendar_violations), mirroring
the strawberry A10/A11 and tree A3/A4 splits.

Lavender is a woody perennial subshrub grown for BLOOMS whose LIFECYCLE is region-dependent: a
per-cell grown_as in {perennial, annual} (a cold-hardy in-ground shrub vs a container/replant
annual in the coldest zones or for tender types). The distinctive guards this asserts that the
generic checks do not encode:
  - the boundary scalars (hardiness_zone_min/max) are present (consumer visual, D12);
  - gating_factors is EMPTY -- cold-hardiness is handled lighter than citrus, with no per-region
    cultivar gate (D7), so no A9-style coverage machinery;
  - NO tree structural machinery (rootstock / chill-hours gate / pollinizer) carries a value --
    a subshrub is not a grafted, chill-gated tree (reject VALUES, not 2.9 null-scaffold keys);
  - NO tree-only resolved-cell keys (suitability / chill_hours_delivered);
  - the calendar tokens match the lifecycle: `prune`/`dormant` are PERENNIAL-only, `season_over`
    is ANNUAL-only, and NO fruit/mow token (harvest/renovation) appears in any cell -- for an
    ornamental the BLOOM window IS the cut-for-use window.
Admission-safe: a per-cell grown_as that is null AND has an empty calendar is the Step-3.5
admission state (skipped). See 2026-06-19-lavender-woody-ornamental-model-design.md (D7-D12).
"""
GROWN_AS_ENUM = {"perennial", "annual"}
REQUIRED_SCALARS = ("hardiness_zone_min", "hardiness_zone_max")
# tree structural machinery that must not carry a real VALUE on a subshrub (2.9 may null-scaffold
# the keys; only a non-empty value is a violation).
_TREE_CROP_KEYS = ("rootstock", "rootstock_options", "pollinizer", "chill_hours_required")
_TREE_ONLY_CELL_KEYS = ("suitability", "chill_hours_delivered")
_CROSS_POLLINATION_KEYS = ("bloom_group", "pollinizer", "pollinizer_distance_ft",
                           "bloom_window_relative")
_FRUIT_TOKENS = ("harvest", "renovation")  # bloom is the cut window; no fruit/mow token


def _nonempty(v):
    return v not in (None, [], {}, "")


def woody_ornamental_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis perennial_woody_ornamental."""
    if crop.get("calendar_basis") != "perennial_woody_ornamental":
        return []
    V = []

    # 1. boundary scalars present (consumer visual per D12; admission-safe Step-2 data).
    for f in REQUIRED_SCALARS:
        if crop.get(f) is None:
            V.append(f"boundary scalar {f} empty (required once basis is perennial_woody_ornamental)")

    # 2. cold-hardiness handled LIGHTER than citrus -- gating_factors must be empty (D7 guard).
    if crop.get("gating_factors"):
        V.append(f"gating_factors must be empty (lavender has no per-region cultivar gate, D7); "
                 f"got {crop.get('gating_factors')!r}")

    # 3. no tree structural machinery on a subshrub (reject VALUES, not 2.9 null-scaffold keys).
    for k in _TREE_CROP_KEYS:
        if _nonempty(crop.get(k)):
            V.append(f"tree machinery {k!r} carries a value ({crop.get(k)!r}); a woody-ornamental "
                     f"subshrub is not a grafted/chill-gated tree")

    # 4. no tree cross-pollination machinery on the varieties.
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            for k in _CROSS_POLLINATION_KEYS:
                if k in v:
                    V.append(f"varieties.recommended[{i}] ({v.get('name')!r}): {k} is tree "
                             f"cross-pollination machinery; a subshrub has none")

    # 5. per-cell: grown_as typing, no tree-only keys, token placement vs grown_as.
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
                for ft in _FRUIT_TOKENS:
                    if ft in cal:
                        V.append(f"{rk}.{z}: ornamental cell carries fruit/mow token {ft!r} "
                                 f"(bloom is the cut-for-use window; no harvest/renovation): {cal}")
                if ga == "annual" and ("prune" in cal or "dormant" in cal):
                    V.append(f"{rk}.{z}: annual cell carries a perennial token "
                             f"(prune/dormant): {cal}")
                if ga == "perennial" and "season_over" in cal:
                    V.append(f"{rk}.{z}: perennial cell carries season_over "
                             f"(annual-only token): {cal}")
    return V
