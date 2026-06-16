#!/usr/bin/env python3
"""Build a crop's 10 region cells to the ratified reference shape (M16 Step 3.5).

Pure transform -- mutates the passed crop dict in place, no I/O, no SHA logic
(the apply wrapper owns that). North (northern_tier) is promoted from the
verified cold zones{}; warm/CA regions get a shape-complete RULE skeleton; the
4 `California -- X` region_label em-dashes become `California: X`.

NOT done here: no biology values invented; no second_planting data written
(claude.ai authors which-zones + dates at Step 4/5); resolved_by_zone cells of
warm regions are left as PENDING fill-targets (derived output, not rule shape).

PERMANENT TREES take a separate path (`_is_tree` -> `_build_tree_shells`): a tree is
planted once and lives for decades, so the annual sowing-window model is replaced by
the tree region model (per-zone suitability verdict where survives != fruits is
first-class, region chill-adequacy, the bloom -> harvest -> dormant-prune cycle). The
crop's `calendar_basis` flips to `perennial_chill_gated`. Annual crops are unaffected.

See docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md
and docs/tree_region_model_scope_v0.md (the tree model).
"""
SESSION = "m16_cherry_step3_5_region_shells"
DATE = "2026-06-05"


def build_region_shells(crop, session=SESSION, date=DATE):
    """Mutate `crop` so every region cell is at reference shape. Returns crop.

    `session`/`date` stamp the northern_tier promotion provenance. They DEFAULT to
    the cherry-era constants for backward compatibility, but every crop after cherry
    must pass its OWN session/date -- the provenance records when THIS crop's north
    was promoted, not cherry's. (The apply wrapper passes them per-run.)

    Shape is DERIVED from the crop (no analogy -- v1.6 A1):
      - `start_method.start == "direct"` -> direct-sow window shape (`direct_sow`),
        else the transplant shape (`start_indoors` + `plant_out`).
      - northern_tier is PROMOTED from the verified cold `zones{}` only when there is
        verified zone data to promote (a retro crop). Author-fresh crops (wiped shells,
        empty zones) have nothing to promote, so their NT is built FROM-SCRATCH like a
        warm region. (Succession tracks are NOT created here -- they are authored at
        Step 4/5.5 with the biology; Step 3.5 builds the beginner skeleton only.)
    """
    if _is_tree(crop):
        return _build_tree_shells(crop)
    if _is_indoor(crop):
        return crop  # no frost/region axis -- the cycle lives in indoor_cycle{}; never inflate shells
    direct = (crop.get("start_method") or {}).get("start") == "direct"
    promote_north = _north_should_promote(crop)
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        # slot scaffolding: region_notes keys present (null acceptable at admission)
        r.setdefault("region_notes_seasoned", None)
        r.setdefault("region_notes_beginner", None)
        # dash resolution on the structural label: "California -- X" -> "California: X"
        lbl = r.get("region_label")
        if isinstance(lbl, str) and " -- " in lbl:
            r["region_label"] = lbl.replace(" -- ", ": ")
        if rk == "northern_tier" and promote_north:
            _build_north_from_zones(r, session, date)
        else:
            _build_warm_shell(r, direct=direct)
        # photoperiod crops carry a per-cell day-length resolution layer alongside the frost
        # windows (which cultivar TYPE bulbs at that latitude), scaffolded null at 3.5.
        if _is_photoperiod(crop):
            for cell in (r.get("resolved_by_zone") or {}).values():
                if isinstance(cell, dict):
                    _scaffold_photoperiod_cell(cell)
    return crop


# ---------------------------------------------------------------------------
# TREE region model (peach Step 3.5, the FIRST permanent tree).
# A permanent tree is planted ONCE and lives for decades; the annual sowing-window
# model does not fit it. What varies by place is hardiness/suitability, winter
# chill adequacy (which gates the variety set), and the absolute phenology dates of
# the recurring bloom -> fruit -> harvest -> dormant-prune cycle. The two-layer cut
# (region-constant rule + zone-resolved render) is kept; the inner calendar model is
# replaced. See docs/tree_region_model_scope_v0.md.
# ---------------------------------------------------------------------------

# resolved-cell keys that belong to the ANNUAL model only -- a permanent tree has no
# second sowing, no indoor-start, no zone-lift, no per-cell rule structure. Stripped.
_TREE_CELL_DEAD = ("start_indoors", "direct_sow", "lifted_from_zone", "plantings",
                   "notes", "zone_notes", "planting_note",
                   "first_plant_date", "last_plant_date")


def _is_indoor(crop):
    """A non_seasonal_indoor crop (microgreens, sprouts) is grown year-round in a relative
    sow -> harvest CYCLE: no frost, no season, no hardiness zone, so no region axis. The cycle
    lives in indoor_cycle{} and the renderer reads calendar_basis. build_region_shells is a
    NO-OP for it -- never inflate the 10 frost region cells (anchor 11 microgreens-mix collapsed
    regions{} to {}; this keeps a future/bot run from rebuilding them)."""
    return (crop.get("calendar_basis") == "non_seasonal_indoor"
            or bool(crop.get("zone_independent")))


_PHOTOPERIOD_CELL_KEYS = ("recommended_day_length_type",
                          "day_length_note_seasoned", "day_length_note_beginner")


def _is_photoperiod(crop):
    """A photoperiod (day-length) gated crop (onion, anchor 12; the allium family) carries a
    per-cell day-length resolution layer ALONGSIDE the frost windows: which cultivar TYPE bulbs
    at that latitude. The crop stays on the normal frost-anchored annual path -- photoperiod
    gates the variety, not the calendar. Marker: "photoperiod" in gating_factors."""
    return "photoperiod" in (crop.get("gating_factors") or [])


def _scaffold_photoperiod_cell(cell):
    """Add the per-cell day-length slots (null) -- idempotent + no-clobber: a re-run never
    wipes a value Step 4 has filled (setdefault only fills an absent key)."""
    for k in _PHOTOPERIOD_CELL_KEYS:
        cell.setdefault(k, None)


def _is_tree(crop):
    """A permanent tree takes the tree region path. Detected by either perennial
    calendar_basis marker (set by THIS builder, so re-runs stay on the tree path) or,
    on the first run before the flip, by lifecycle/archetype. Annual crops unaffected."""
    if crop.get("calendar_basis") in ("perennial_chill_gated", "perennial_evergreen"):
        return True
    arch = crop.get("archetype") or ""
    return crop.get("lifecycle") == "permanent" or arch.endswith("_fruit_tree")


def _evergreen(crop):
    """Evergreen fruit trees (citrus/avocado/olive) take the EVERGREEN calendar shape
    (calendar_basis `perennial_evergreen`, no dormancy) and a cold-hardiness climate
    layer (`min_winter_temp_f`), not the deciduous chill-gated shape -- chill ~ 0 for
    them, frost is the limiter. Detected by the evergreen archetype or the already-
    flipped basis (so re-runs stay evergreen). See tree_region_model_evergreen_amendment_v1_0."""
    return (crop.get("calendar_basis") == "perennial_evergreen"
            or (crop.get("archetype") or "").endswith("evergreen_fruit_tree"))


def _build_tree_shells(crop):
    """Build every region cell to the TREE reference shape. Pure transform; no biology
    invented; idempotent + no-clobber (a re-run never wipes a cell Step 4 has filled).

    Sets the crop-level `calendar_basis` to `perennial_chill_gated` -- the one marker
    that makes the Step 5.5 gate branch off the annual sowing-window criteria and onto
    the tree criteria (suitability + chill + the single perennial establishment entry).
    """
    evergreen = _evergreen(crop)
    # a heat_accumulation crop (orange/grapefruit) banks a SECOND climate datum beyond cold;
    # gating_factors is the source of truth (evergreen amendment section 2-3).
    heat_gated = "heat_accumulation" in (crop.get("gating_factors") or [])
    crop["calendar_basis"] = "perennial_evergreen" if evergreen else "perennial_chill_gated"
    for r in (crop.get("regions") or {}).values():
        if isinstance(r, dict):
            _build_tree_region(r, evergreen, heat_gated)
    return crop


def _build_tree_region(r, evergreen=False, heat_gated=False):
    # dash resolution on the structural label (shared with the annual model)
    lbl = r.get("region_label")
    if isinstance(lbl, str) and " -- " in lbl:
        r["region_label"] = lbl.replace(" -- ", ": ")
    r.setdefault("region_notes_seasoned", None)
    r.setdefault("region_notes_beginner", None)
    # sweep the vestigial empty `sources_pending_admission` scaffold residue (the same
    # benign Step-3.5 leftover the carrot release swept). Only when empty -- never drop
    # a populated admission list.
    if r.get("sources_pending_admission") == []:
        r.pop("sources_pending_admission", None)
    # region-constant CLIMATE layer (present-but-empty at shell stage), keyed to the
    # gate: a deciduous tree banks winter CHILL (gates which varieties fruit); a
    # cold-gated evergreen banks ~0 chill, so its limiter is the typical winter LOW
    # (min_winter_temp_f) -- the frost-risk datum. (evergreen amendment section 3.)
    if evergreen:
        r.setdefault("min_winter_temp_f", [])
        r.setdefault("cold_basis_seasoned", None)
        r.setdefault("cold_basis_beginner", None)
        # a heat_accumulation crop (orange/grapefruit) ALSO banks summer heat: the
        # qualitative ripening-adequacy verdict + its prose pair, alongside cold.
        if heat_gated:
            r.setdefault("heat_summer_basis", None)
            r.setdefault("heat_basis_seasoned", None)
            r.setdefault("heat_basis_beginner", None)
    else:
        r.setdefault("chill_hours_delivered", [])
        r.setdefault("chill_basis_seasoned", None)
        r.setdefault("chill_basis_beginner", None)
    # region-constant RULE layer: a SINGLE one-time establishment entry, track:"perennial"
    # (no succession, no second_planting -- a tree is planted once). bloom + harvest rule
    # lists feed the Bloom/Harvest tracks; plant_out feeds the one-time Plant track. Only
    # (re)build when it is not already the perennial entry -- never clobber a filled rule.
    pl = r.get("plantings")
    if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)
            and pl[0].get("track") == "perennial"):
        r["plantings"] = [{
            "succession_id": 1, "label": "establishment", "track": "perennial",
            "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": [],
            "anchoring_urls": {},
        }]
    r.setdefault("plantings_provenance", None)
    # zone-resolved render layer: reshape each cell to the tree key-set
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            _build_tree_cell(cell, evergreen, heat_gated)


def _build_tree_cell(cell, evergreen=False, heat_gated=False):
    """Reshape one resolved_by_zone cell to the tree key-set, idempotent + no-clobber.
    The per-zone `suitability` verdict makes survives != fruits FIRST-CLASS: a tree may
    SURVIVE a zone yet not set a reliable crop there (survives_no_fruit), or be flatly
    unsuitable (no chill at all). The render keys reuse the annual resolved-cell names
    (plant_out/bloom/harvest_*) so the renderer reads tree and annual cells uniformly."""
    for dead in _TREE_CELL_DEAD:
        cell.pop(dead, None)
    # per-zone suitability verdict (survives vs fruits-reliably vs survives_no_fruit vs unsuitable)
    cell.setdefault("suitability", None)
    cell.setdefault("suitability_note_seasoned", None)
    cell.setdefault("suitability_note_beginner", None)
    # per-zone climate datum (refines the region band): chill for deciduous,
    # min winter temp for a cold-gated evergreen.
    if evergreen:
        cell.setdefault("min_winter_temp_f", [])
        if heat_gated:
            cell.setdefault("heat_summer_basis", None)
    else:
        cell.setdefault("chill_hours_delivered", [])
    # resolved render fields (reuse the annual keys; the renderer's resolved reader is shared)
    cell.setdefault("plant_out", None)      # one-time bare-root dormant window
    cell.setdefault("bloom", None)          # absolute bloom window (region-resolved)
    cell.setdefault("harvest_start", None)
    cell.setdefault("harvest_end", None)
    cell.setdefault("harvest", None)
    cell.setdefault("calendar", [])         # 12-month tree cycle (dormant/bloom/growing/harvest/prune/care)
    cell.setdefault("frost_risk_note_seasoned", None)  # late-frost-kills-early-bloom warning
    cell.setdefault("resolved_from", {})    # frost dates + chill band used (auditable)
    cell.setdefault("resolution_method", None)  # -> "perennial_precompute" once filled
    cell.setdefault("sources", [])
    cell.setdefault("anchoring_urls", {})


def _north_should_promote(crop):
    """Legacy retro path: promote northern_tier from the verified cold `zones{}` only
    when there IS verified zone data -- an already-promoted resolved cell (carries a
    `resolution_method`), a pre-hoist nested-`plantings` cell, or cold-zone `plantings`
    in `zones{}`. A wiped author-fresh shell has none of these -> build NT from-scratch."""
    nt = (crop.get("regions") or {}).get("northern_tier") or {}
    for cell in (nt.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict) and (cell.get("resolution_method") or cell.get("plantings")):
            return True
    z = crop.get("zones") or {}
    for zk in ("3", "4", "5", "6", "7"):
        c = z.get(zk)
        if isinstance(c, dict) and c.get("plantings"):
            return True
    return False


def _build_north_from_zones(r, session=SESSION, date=DATE):
    # region-constant RULE layer: every plantings entry carries a track
    for p in r.get("plantings") or []:
        if isinstance(p, dict):
            p.setdefault("track", "beginner")
    # resolved layer: strip the forbidden nested plantings and re-stamp
    # static_precompute -> zone_promoted_verified (these cells are promoted +
    # verified from the cold zones{}, not statically precomputed)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            cell.pop("plantings", None)
            # lifted_from_zone is tautological in the north (the region zone IS
            # the legacy zone, so it always equals the cell's own zone key) -- the
            # reference crop (lettuce northern_tier) sheds it on promotion. Drop it
            # for shape parity. (In multi-zone warm regions like se_gulf it is
            # informative and kept; that is not this north path.)
            cell.pop("lifted_from_zone", None)
            if cell.get("resolution_method") == "static_precompute":
                cell["resolution_method"] = "zone_promoted_verified"
    # provenance: replace the Phase-A verbatim-lift string with a promotion record
    r["plantings_provenance"] = (
        "Zone-promoted and re-verified from cold zones 3-7 "
        f"({session}, {date}). Supersedes the Phase A verbatim lift."
    )


def _build_warm_shell(r, direct=False):
    # shape-complete RULE skeleton: a single track:"beginner" rule object with the
    # archetype's window-rule keys present-but-empty, ready for Step 4 to fill values
    # into. `direct` selects the window shape: direct-sow crops (carrots, roots) carry
    # `direct_sow`; transplant crops carry `start_indoors` + `plant_out`. resolved_by_zone
    # cells are left untouched (derived output; PENDING until Step 4 sources them).
    # Only build the skeleton if plantings is still a stub (a PENDING sentinel string or
    # empty). If it is already a dict-shaped rule object, a later step has filled it -- do
    # not clobber it. Keeps the transform safe to re-run. (This path also builds the
    # FROM-SCRATCH northern_tier of author-fresh crops -- nothing to promote.)
    if not r.get("plantings") or not isinstance(r["plantings"][0], dict):
        entry = {"succession_id": 1, "label": "main", "track": "beginner"}
        if direct:
            entry["direct_sow"] = []
        else:
            entry["start_indoors"] = []
            entry["plant_out"] = []
        entry["harvest_start"] = []
        entry["harvest_end"] = []
        entry["anchoring_urls"] = {}
        r["plantings"] = [entry]
    # defensive: no rule-bearing structure may live in the resolved layer
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            cell.pop("plantings", None)
