#!/usr/bin/env python3
"""Build a crop's 10 region cells to the ratified reference shape (M16 Step 3.5).

Pure transform -- mutates the passed crop dict in place, no I/O, no SHA logic
(the apply wrapper owns that). North (northern_tier) is promoted from the
verified cold zones{}; warm/CA regions get a shape-complete RULE skeleton; the
4 `California -- X` region_label em-dashes become `California: X`.

NOT done here: no biology values invented; no second_planting data written
(claude.ai authors which-zones + dates at Step 4/5); resolved_by_zone cells of
warm regions are left as PENDING fill-targets (derived output, not rule shape).

See docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md
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
    return crop


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
