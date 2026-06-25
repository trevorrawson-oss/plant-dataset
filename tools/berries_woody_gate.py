#!/usr/bin/env python3
"""Berries_woody structural cert branch (blueberry, anchor 18; the FIRST and only crop with
this archetype). Fires ONLY for calendar_basis == berries_woody (a no-op otherwise). Imported
+ run by whole_crop_gate.py as section A15. The calendar coherence (stored == derived) is the
SEPARATE A16 (berry_woody_calendar.berry_woody_calendar_violations), mirroring the strawberry
A10/A11, woody-ornamental A13/A14, and tree A3/A4 splits.

Blueberry is a woody fruiting SHRUB whose growable TYPE is CHILL-GATED by region and whose
calendar SHAPE splits by per-cell leaf_habit. The distinctive guards this asserts that the
generic checks do not encode:
  - the lifecycle SCALARS are present (Step-2 data; admission-safe, present before 3.5 sets basis);
  - gating_factors contains "chill_hours" and chill_hours_required is set -- chill IS the gate (D1),
    the deliberate INVERSE of the woody-ornamental gate, which REJECTS chill_hours_required;
  - the woody-specific prose pairs are non-null (a backstop; register_fill owns the full set, D8 4.1);
  - self_fertile is false + NO apple cross-pollination machinery on the varieties (the light model, D4);
  - NO tree structural machinery (rootstock / pollinizer) carries a value -- own-root shrub;
  - per-cell: recommended_type + leaf_habit typed, the type COVERAGE invariant (every per-cell
    recommended_type has >=1 matching variety -- the onion-A9 analog), NO tree-only cell key
    (suitability), and the leaf_habit<->token placement (deciduous carries dormant, evergreen
    carries none, NEVER season_over/renovation). chill-DELIVERED is the shared
    region_chill_delivered table now (F2 refactor); A18 forbids a per-cell chill_hours_delivered.
Admission-safe: a cell with null recommended_type + null leaf_habit + empty calendar is the
Step-3.5 admission state (skipped). See 2026-06-22-blueberry-berries-woody-model-design.md (D1-D8).
"""
TYPE_ENUM = {"northern_highbush", "southern_highbush", "rabbiteye"}
LEAF_ENUM = {"deciduous", "evergreen"}
LIFECYCLE_SCALARS = ("establishment_years", "years_to_first_harvest",
                     "years_to_full_production", "productive_lifespan_years")
PROSE_PAIRS = ("type_selection", "pollinator_notes", "chill_hours_note")  # _seasoned + _beginner
# tree structural machinery that must not carry a real value on an own-root shrub. NOTE
# chill_hours_required is NOT here -- for blueberry it is the legit gate basis (D1), the inverse
# of the woody-ornamental gate.
_TREE_CROP_KEYS = ("rootstock", "rootstock_options", "pollinizer")
# tree-only resolved-cell keys (mis-route markers). chill_hours_delivered is NOT a cell key at
# all anymore -- chill-delivered moved to the shared region_chill_delivered table (F2 refactor),
# and A18 forbids a per-crop copy; only suitability marks a tree mis-route here.
_TREE_ONLY_CELL_KEYS = ("suitability",)
_CROSS_POLLINATION_KEYS = ("bloom_group", "pollinizer", "pollinizer_distance_ft",
                           "bloom_window_relative")


def _nonempty(v):
    return v not in (None, [], {}, "")


def berries_woody_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless basis berries_woody."""
    if crop.get("calendar_basis") != "berries_woody":
        return []
    V = []

    # 1. lifecycle scalars present (Step-2 data; admission-safe).
    for f in LIFECYCLE_SCALARS:
        v = crop.get(f)
        if v is None or v == []:
            V.append(f"lifecycle scalar {f} empty (required once basis is berries_woody)")

    # 2. chill IS the gate (D1) -- gating_factors signature + the basis figure present.
    if "chill_hours" not in (crop.get("gating_factors") or []):
        V.append(f"gating_factors must contain 'chill_hours' (the per-region type gate, D1); "
                 f"got {crop.get('gating_factors')!r}")
    if crop.get("chill_hours_required") is None:
        V.append("chill_hours_required empty (the chill gate basis, D1)")

    # 1b. woody-specific prose-pair backstop (register_fill owns the full set; D8 4.1).
    for base in PROSE_PAIRS:
        for reg in ("seasoned", "beginner"):
            k = f"{base}_{reg}"
            if not _nonempty(crop.get(k)):
                V.append(f"prose pair {k} empty (backstop; register_fill owns the full set)")

    # 6. cross-pollination: the light model -- self_fertile false, no apple machinery.
    if crop.get("self_fertile") is not False:
        V.append(f"self_fertile must be false (blueberry needs cross-pollination, the light "
                 f"model); got {crop.get('self_fertile')!r}")

    # 3b. no tree structural machinery on an own-root shrub (reject VALUES, not 2.9 null keys).
    for k in _TREE_CROP_KEYS:
        if _nonempty(crop.get(k)):
            V.append(f"tree machinery {k!r} carries a value ({crop.get(k)!r}); blueberry is "
                     f"own-root, no grafting")

    # 4. no apple cross-pollination machinery on the varieties; collect variety types for coverage.
    variety_types = set()
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            if v.get("type"):
                variety_types.add(v.get("type"))
            for k in _CROSS_POLLINATION_KEYS:
                if k in v:
                    V.append(f"varieties.recommended[{i}] ({v.get('name')!r}): {k} is apple "
                             f"cross-pollination machinery; blueberry uses the light "
                             f"self_fertile=false model")

    # 5. per-cell: typing, no tree-only keys, token placement; collect cell types for coverage.
    cell_types = set()
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
            rt = cell.get("recommended_type")
            lh = cell.get("leaf_habit")
            cal = cell.get("calendar") or []
            if rt is None and lh is None and not cal:
                continue  # Step-3.5 admission state
            if rt not in TYPE_ENUM:
                V.append(f"{rk}.{z}: recommended_type {rt!r} not in {sorted(TYPE_ENUM)}")
            else:
                cell_types.add(rt)
            if lh not in LEAF_ENUM:
                V.append(f"{rk}.{z}: leaf_habit {lh!r} not in {sorted(LEAF_ENUM)}")
            if cal:
                if "renovation" in cal:
                    V.append(f"{rk}.{z}: cell carries renovation (strawberry-only token): {cal}")
                if "season_over" in cal:
                    V.append(f"{rk}.{z}: cell carries season_over (a woody perennial never "
                             f"ends -- dormant up North, continuous growth down South): {cal}")
                if lh == "deciduous" and "dormant" not in cal:
                    V.append(f"{rk}.{z}: deciduous cell lacks the dormant cycle: {cal}")
                if lh == "evergreen" and "dormant" in cal:
                    V.append(f"{rk}.{z}: evergreen cell carries dormant (no winter dormancy in "
                             f"the warm South): {cal}")

    # 3. type COVERAGE invariant: every per-cell recommended_type has >=1 matching variety.
    for ct in sorted(cell_types - variety_types):
        V.append(f"recommended_type {ct!r} appears in a resolved cell but no variety carries "
                 f"that type (coverage invariant)")
    return V


def _is_number(v):
    # a bool passes isinstance(_, int) in Python -- exclude it, it is not a chill value.
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def berries_woody_variety_chill_violations(crop):
    """WI3 -- the variety-chill PRESENCE gate (whole_crop_gate A21). Fires ONLY for
    calendar_basis == berries_woody (a no-op otherwise). Locks the WI4 string->numeric
    migration so a future berries_woody crop cannot reship the legacy `chill_hours` STRING
    that broke blueberry's chill gauge (audit F2/WI4). The crop-LEVEL chill gate basis is
    A15's job; THIS branch polices the per-VARIETY chill shape that chillBuckets/tree.ts
    reads. Every recommended variety must carry:
      - a NUMERIC chill_hours_required (the chill-gating threshold; a string/None violates);
      - a chill_hours_range key that is null (a single-value cultivar) OR a valid [lo,hi]
        pair of numbers with lo<=hi AND lo == chill_hours_required (the scalar IS the range
        low end -- the documented "= the chill-gating threshold" semantic);
      - NO string `chill_hours` -- the dropped legacy form; its reappearance is the exact
        regression this gate prevents.
    """
    if crop.get("calendar_basis") != "berries_woody":
        return []
    V = []
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if not isinstance(v, dict):
            continue
        name = v.get("name")
        chr_ = v.get("chill_hours_required")
        if not _is_number(chr_):
            V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_required must be "
                     f"numeric (the WI4 string->numeric lock); got {chr_!r}")
        if isinstance(v.get("chill_hours"), str):
            V.append(f"varieties.recommended[{i}] ({name!r}): a string chill_hours "
                     f"({v.get('chill_hours')!r}) is the dropped legacy form -- use the numeric "
                     f"chill_hours_required + chill_hours_range")
        if "chill_hours_range" not in v:
            V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_range key missing "
                     f"(the migrated shape carries it -- null for a single-value cultivar)")
        else:
            rng = v.get("chill_hours_range")
            if rng is None:
                pass  # single-value cultivar -- legitimately null
            elif (not isinstance(rng, list) or len(rng) != 2
                  or not all(_is_number(x) for x in rng)):
                V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_range must be "
                         f"null or a [lo,hi] pair of numbers; got {rng!r}")
            elif rng[0] > rng[1]:
                V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_range lo>hi: {rng!r}")
            elif _is_number(chr_) and chr_ != rng[0]:
                V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_required {chr_} must "
                         f"equal the chill_hours_range low end {rng[0]} (the scalar is the chill-"
                         f"gating threshold = the range low end)")
    return V
