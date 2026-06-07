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
    """
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
        if rk == "northern_tier":
            _build_north_from_zones(r, session, date)
        else:
            _build_warm_shell(r)
    return crop


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


def _build_warm_shell(r):
    # shape-complete RULE skeleton (warm_season_fruiting transplant archetype):
    # a single track:"beginner" rule object with the archetype window-rule keys
    # present-but-empty, ready for Step 4 to fill values into. resolved_by_zone
    # cells are left untouched (derived output; PENDING until Step 4 sources them).
    # Only build the skeleton if plantings is still a stub (a PENDING sentinel
    # string or empty). If it is already a dict-shaped rule object, a later step
    # has filled it -- do not clobber it. Keeps the transform safe to re-run.
    if not r.get("plantings") or not isinstance(r["plantings"][0], dict):
        r["plantings"] = [{
            "succession_id": 1,
            "label": "main",
            "track": "beginner",
            "start_indoors": [],
            "plant_out": [],
            "harvest_start": [],
            "harvest_end": [],
            "anchoring_urls": {},
        }]
    # defensive: no rule-bearing structure may live in the resolved layer
    for cell in (r.get("resolved_by_zone") or {}).values():
        if isinstance(cell, dict):
            cell.pop("plantings", None)
