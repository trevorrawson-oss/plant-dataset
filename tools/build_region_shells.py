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
    if _is_woody_ornamental(crop):
        return _build_woody_ornamental_shells(crop)  # checked BEFORE _is_tree (defensive)
    if _is_berry_woody(crop):
        return _build_berry_woody_shells(crop)  # BEFORE _is_tree: blueberry is lifecycle=permanent
    if _is_tree(crop):
        return _build_tree_shells(crop)
    if _is_indoor(crop):
        return crop  # no frost/region axis -- the cycle lives in indoor_cycle{}; never inflate shells
    if _is_berry_herbaceous(crop):
        return _build_berry_herbaceous_shells(crop)
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
        # Deciduous region: keep the per-crop chill_basis prose (the crop's interpretation
        # of its chill situation), but NOT the chill-delivered number -- that climate datum
        # lives in the shared region_chill_delivered table now (F2 refactor; A18).
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
    # per-zone climate datum: min winter temp for a cold-gated evergreen. A DECIDUOUS
    # cell carries NO per-cell chill field -- chill-delivered is a CLIMATE datum that now
    # lives ONCE in the shared top-level region_chill_delivered table (F2 refactor,
    # 2026-06-24); per-crop chill_hours_delivered is forbidden (whole_crop_gate A18).
    if evergreen:
        cell.setdefault("min_winter_temp_f", [])
        if heat_gated:
            cell.setdefault("heat_summer_basis", None)
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


# ---------------------------------------------------------------------------
# BERRIES_HERBACEOUS region model (strawberry Step 3.5, anchor 13; the only crop with
# this archetype). A herbaceous perennial whose LIFECYCLE is region-dependent: the north
# grows it as a perennial matted row, hot-summer CA/FL as a fall-planted annual. The crop
# is planted from bare-root dormant crowns in a frost-anchored window, so frost resolution
# stays ON (basis perennial_herbaceous, not a tree basis). The per-cell grown_as picks the
# lifecycle the renderer + the A10/A11 gates branch on. See the 2026-06-18 design spec.
# ---------------------------------------------------------------------------

# resolved-cell keys belonging to the ANNUAL sowing model only -- a crown-planted perennial
# has no indoor start, no second sowing, no per-cell rule structure. Stripped.
_BERRY_CELL_DEAD = ("start_indoors", "direct_sow", "lifted_from_zone", "plantings",
                    "notes", "zone_notes", "planting_note",
                    "first_plant_date", "last_plant_date")


def _is_berry_herbaceous(crop):
    """A herbaceous-perennial berry (strawberry) takes the berry region path. Detected by the
    perennial_herbaceous basis marker (set by THIS builder, so re-runs stay on the path) or, on
    the first run before the flip, by the berries_herbaceous archetype. NOT a tree (_is_tree keys
    on *_fruit_tree / lifecycle permanent, neither of which strawberry is)."""
    return (crop.get("calendar_basis") == "perennial_herbaceous"
            or crop.get("archetype") == "berries_herbaceous")


def _build_berry_herbaceous_shells(crop):
    """Build every region cell to the berries_herbaceous reference shape. Pure transform; no
    biology invented; idempotent + no-clobber. Sets calendar_basis -> perennial_herbaceous, the
    marker that branches Step 5.5 + the A10/A11 gates onto the perennial-herbaceous criteria."""
    crop["calendar_basis"] = "perennial_herbaceous"
    for r in (crop.get("regions") or {}).values():
        if isinstance(r, dict):
            _build_berry_region(r)
    return crop


def _build_berry_region(r):
    lbl = r.get("region_label")
    if isinstance(lbl, str) and " -- " in lbl:
        r["region_label"] = lbl.replace(" -- ", ": ")
    r.setdefault("region_notes_seasoned", None)
    r.setdefault("region_notes_beginner", None)
    if r.get("sources_pending_admission") == []:
        r.pop("sources_pending_admission", None)
    # region-constant RULE layer: a SINGLE crown-setting establishment entry (no succession,
    # no second_planting -- a strawberry bed is planted once per replant cycle). Only (re)build
    # when it is not already the perennial entry -- never clobber a filled rule.
    pl = r.get("plantings")
    if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)
            and pl[0].get("track") == "perennial"):
        r["plantings"] = [{
            "succession_id": 1, "label": "establishment", "track": "perennial",
            "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": [],
            "anchoring_urls": {},
        }]
    r.setdefault("plantings_provenance", None)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            _build_berry_cell(cell)


def _build_berry_cell(cell):
    """Reshape one resolved_by_zone cell to the berries_herbaceous key-set, idempotent +
    no-clobber. The per-zone `grown_as` makes the region-dependent lifecycle first-class. The
    render keys reuse the annual/tree names (plant_out/bloom/harvest_*) so the renderer reads
    berry, tree, and annual cells uniformly. NO tree keys (suitability/chill_hours_delivered)."""
    for dead in _BERRY_CELL_DEAD:
        cell.pop(dead, None)
    cell.setdefault("grown_as", None)               # perennial (north) | annual (hot-summer CA/FL)
    cell.setdefault("grown_as_note_seasoned", None)
    cell.setdefault("grown_as_note_beginner", None)
    cell.setdefault("plant_out", None)              # crown-setting window (frost-anchored)
    cell.setdefault("bloom", None)
    cell.setdefault("harvest_start", None)
    cell.setdefault("harvest_end", None)
    cell.setdefault("harvest", None)
    cell.setdefault("calendar", [])                 # 12-month cycle, derived at Step 4 (A11)
    cell.setdefault("frost_risk_note_seasoned", None)  # late-frost-kills-open-blossom warning
    cell.setdefault("resolved_from", {})            # frost dates used (auditable)
    cell.setdefault("resolution_method", None)      # -> "perennial_herbaceous_precompute" once filled
    cell.setdefault("sources", [])
    cell.setdefault("anchoring_urls", {})


# ---------------------------------------------------------------------------
# PERENNIAL_WOODY_ORNAMENTAL region model (lavender Step 3.5, anchor 14; the FIRST and only crop
# with this archetype). A woody perennial subshrub grown for BLOOMS (not fruit) whose LIFECYCLE is
# region-dependent: cold-hardy zones grow it as an in-ground perennial shrub, the coldest zones /
# tender types as a container/replant annual. It is planted as a nursery transplant in a frost-
# anchored window, so frost resolution stays ON (basis perennial_woody_ornamental, not a tree
# basis). The per-cell grown_as picks the lifecycle the renderer + the A13/A14 gates branch on. The
# defining care act is the annual hard CUT-BACK (the derived `prune` calendar beat). There is NO
# harvest -- the BLOOM window IS the cut-for-use window. See the 2026-06-19 design spec (D1-D12).
# ---------------------------------------------------------------------------

# resolved-cell keys belonging to the ANNUAL sowing model only -- a transplant-set subshrub has no
# indoor start, no second sowing, no per-cell rule structure. The harvest_* keys are stripped too:
# an ornamental has NO harvest (the bloom window IS the cut-for-use window), so any harvest key left
# by the annual/scaffold shape is dead weight. Stripped.
_WOODY_CELL_DEAD = ("start_indoors", "direct_sow", "lifted_from_zone", "plantings",
                    "notes", "zone_notes", "planting_note",
                    "first_plant_date", "last_plant_date",
                    "harvest_start", "harvest_end", "harvest")

# The Step-1 archetype refinement that triggers the FIRST 3.5 run (before the basis flip), mirroring
# how strawberry's shell archetype became `berries_herbaceous`. The generic shell default for
# lavender is `companion_and_ornamental_flower` (shared with zinnia + 12 other flowers), so it is NOT
# a usable trigger -- the data arc must set this distinctive value, which also tells the herbaceous
# perennials (bee-balm/echinacea) that share the flower default apart from the woody subshrub.
WOODY_ORNAMENTAL_ARCHETYPE = "woody_ornamental"


def _is_woody_ornamental(crop):
    """A woody-perennial ornamental subshrub (lavender, anchor 14; the first) takes the woody-
    ornamental region path. Detected by the perennial_woody_ornamental basis marker (set by THIS
    builder, so re-runs stay on the path) or, on the FIRST run before the flip, by the distinctive
    `woody_ornamental` archetype (the Step-1 refinement of the generic companion_and_ornamental_flower
    shell default). NOT a tree (lifecycle is "perennial" not "permanent"; archetype does not end with
    _fruit_tree) and NOT an annual flower (zinnia stays companion_and_ornamental_flower)."""
    return (crop.get("calendar_basis") == "perennial_woody_ornamental"
            or crop.get("archetype") == WOODY_ORNAMENTAL_ARCHETYPE)


def _build_woody_ornamental_shells(crop):
    """Build every region cell to the woody-ornamental reference shape. Pure transform; no biology
    invented; idempotent + no-clobber. Sets calendar_basis -> perennial_woody_ornamental, the marker
    that branches Step 5.5 + the A13/A14 gates onto the woody-ornamental criteria."""
    crop["calendar_basis"] = "perennial_woody_ornamental"
    for r in (crop.get("regions") or {}).values():
        if isinstance(r, dict):
            _build_woody_ornamental_region(r)
    return crop


def _build_woody_ornamental_region(r):
    lbl = r.get("region_label")
    if isinstance(lbl, str) and " -- " in lbl:
        r["region_label"] = lbl.replace(" -- ", ": ")
    r.setdefault("region_notes_seasoned", None)
    r.setdefault("region_notes_beginner", None)
    if r.get("sources_pending_admission") == []:
        r.pop("sources_pending_admission", None)
    # region-constant RULE layer: a SINGLE transplant-setting establishment entry (no succession --
    # a subshrub is planted once per replant cycle). plant_out feeds the Plant track, bloom the Bloom
    # track; the `prune` beat is DERIVED (the month after bloom), so there is NO harvest/prune rule
    # arm. Only (re)build when it is not already the perennial entry -- never clobber a filled rule.
    pl = r.get("plantings")
    if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)
            and pl[0].get("track") == "perennial"):
        r["plantings"] = [{
            "succession_id": 1, "label": "establishment", "track": "perennial",
            "plant_out": [], "bloom": [],
            "anchoring_urls": {},
        }]
    r.setdefault("plantings_provenance", None)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            _build_woody_ornamental_cell(cell)


def _build_woody_ornamental_cell(cell):
    """Reshape one resolved_by_zone cell to the woody-ornamental key-set, idempotent + no-clobber.
    The per-zone grown_as makes the region-dependent lifecycle first-class. NO harvest keys (an
    ornamental's bloom window IS the cut-for-use window). NO tree keys (suitability/chill). The
    render keys reuse the annual/tree/berry names (plant_out/bloom) so the renderer reads them
    uniformly. The `prune` calendar beat is derived at Step 4, not a stored window."""
    for dead in _WOODY_CELL_DEAD:
        cell.pop(dead, None)
    cell.setdefault("grown_as", None)               # perennial (hardy in-ground shrub) | annual (cold/tender, replant)
    cell.setdefault("grown_as_note_seasoned", None)
    cell.setdefault("grown_as_note_beginner", None)
    cell.setdefault("plant_out", None)              # nursery-transplant window (frost-anchored)
    cell.setdefault("bloom", None)                  # bloom window = the cut-for-use window
    cell.setdefault("calendar", [])                 # 12-month cycle, derived at Step 4 (A14)
    cell.setdefault("frost_risk_note_seasoned", None)  # late-frost-kills-tender-new-growth warning
    cell.setdefault("resolved_from", {})            # frost dates used (auditable)
    cell.setdefault("resolution_method", None)      # -> "perennial_woody_ornamental_precompute" once filled
    cell.setdefault("sources", [])
    cell.setdefault("anchoring_urls", {})


# ---------------------------------------------------------------------------
# BERRIES_WOODY region model (blueberry Step 3.5, anchor 18; the FIRST and only crop with this
# archetype). A woody fruiting SHRUB whose growable TYPE is chill-gated by region (northern/southern
# highbush, rabbiteye) and whose calendar SHAPE splits by per-cell leaf_habit (deciduous North /
# evergreen South). Planted as a nursery transplant in a frost-anchored window, so frost resolution
# stays ON (basis berries_woody, not a tree basis). The per-cell recommended_type + leaf_habit pick
# the type + calendar shape the renderer + the A15/A16 gates branch on. UNLIKE the woody-ornamental
# subshrub, blueberry HAS a harvest (a fruiting shrub), so the harvest keys stay. The per-cell
# chill_hours_delivered is the gate basis (KEPT -- the inverse of the berry/woody-ornamental cell,
# which strips it). northern_tier is built FROM SCRATCH like every region (no zones{} promote). See
# the 2026-06-22 design spec (D1-D8).
# ---------------------------------------------------------------------------

# resolved-cell keys belonging to the ANNUAL sowing model only -- a crown-planted shrub has no indoor
# start, no second sowing, no per-cell rule structure. Stripped. (The harvest keys are KEPT --
# blueberry fruits, unlike the ornamental subshrub.)
_BERRY_WOODY_CELL_DEAD = ("start_indoors", "direct_sow", "lifted_from_zone", "plantings",
                          "notes", "zone_notes", "planting_note",
                          "first_plant_date", "last_plant_date")


def _is_berry_woody(crop):
    """A woody fruiting shrub (blueberry, anchor 18; the first) takes the berries_woody region path.
    Detected by the berries_woody basis marker (set by THIS builder, so re-runs stay on the path) or,
    on the FIRST run before the flip, by the berries_woody archetype. MUST be dispatched BEFORE
    _is_tree: blueberry is lifecycle=permanent, which _is_tree catches, so an un-ordered dispatch
    would mis-route it to the tree builder (the same defensive-ordering case as woody-ornamental)."""
    return (crop.get("calendar_basis") == "berries_woody"
            or crop.get("archetype") == "berries_woody")


def _build_berry_woody_shells(crop):
    """Build every region cell to the berries_woody reference shape. Pure transform; no biology
    invented; idempotent + no-clobber. Sets calendar_basis -> berries_woody, the marker that branches
    Step 5.5 + the A15/A16 gates onto the berries_woody criteria."""
    crop["calendar_basis"] = "berries_woody"
    for r in (crop.get("regions") or {}).values():
        if isinstance(r, dict):
            _build_berry_woody_region(r)
    return crop


def _build_berry_woody_region(r):
    lbl = r.get("region_label")
    if isinstance(lbl, str) and " -- " in lbl:
        r["region_label"] = lbl.replace(" -- ", ": ")
    r.setdefault("region_notes_seasoned", None)
    r.setdefault("region_notes_beginner", None)
    if r.get("sources_pending_admission") == []:
        r.pop("sources_pending_admission", None)
    # region-constant RULE layer: a SINGLE nursery-setting establishment entry (no succession, no
    # second_planting -- a blueberry is planted once for decades). plant_out feeds the Plant track,
    # bloom the Bloom track, harvest_* the Harvest track. Only (re)build when it is not already the
    # perennial entry -- never clobber a filled rule.
    pl = r.get("plantings")
    if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)
            and pl[0].get("track") == "perennial"):
        r["plantings"] = [{
            "succession_id": 1, "label": "establishment", "track": "perennial",
            "plant_out": [], "bloom": [], "harvest_start": [], "harvest_end": [],
            "anchoring_urls": {},
        }]
    r.setdefault("plantings_provenance", None)
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            _build_berry_woody_cell(cell)


def _build_berry_woody_cell(cell):
    """Reshape one resolved_by_zone cell to the berries_woody key-set, idempotent + no-clobber. The
    per-zone recommended_type + leaf_habit make the region-dependent TYPE + calendar SHAPE first-class
    (D1/D2). chill_hours_delivered is the per-cell gate basis (KEPT -- the inverse of the berry/woody-
    ornamental cell). The render keys reuse the annual/tree/berry names (plant_out/bloom/harvest_*) so
    the renderer reads them uniformly. The calendar is derived at Step 4 (A16). NO tree-only suitability."""
    for dead in _BERRY_WOODY_CELL_DEAD:
        cell.pop(dead, None)
    cell.setdefault("recommended_type", None)       # northern_highbush | southern_highbush | rabbiteye (D1)
    cell.setdefault("leaf_habit", None)             # deciduous (cold) | evergreen (warm South) (D2)
    # NO per-cell chill_hours_delivered: chill-delivered is the shared region_chill_delivered
    # table now (F2 refactor; A18). The chill GATE basis for blueberry is the crop-level
    # chill_hours_required + gating_factors, not a per-cell number.
    cell.setdefault("type_note_seasoned", None)     # why this type here -- chill
    cell.setdefault("type_note_beginner", None)
    cell.setdefault("plant_out", None)              # nursery-setting window (frost-anchored)
    cell.setdefault("bloom", None)
    cell.setdefault("harvest_start", None)
    cell.setdefault("harvest_end", None)
    cell.setdefault("harvest", None)                # display span the calendar deriver parses
    cell.setdefault("calendar", [])                 # 12-month cycle, derived at Step 4 (A16)
    cell.setdefault("frost_risk_note_seasoned", None)  # late frost on open bloom (the low-chill-south risk)
    cell.setdefault("resolved_from", {})            # frost dates used (auditable)
    cell.setdefault("resolution_method", None)      # -> "berries_woody_precompute" once filled
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
