#!/usr/bin/env python3
"""timing-spine schema gate (Plan 3 field authoring). Validates the seed->harvest timing fields the
app's crop-timing.ts consumes: propagule, dtm_anchor, sow_depth_inches, thin_to_inches,
harvest_window_days, divide_every_years, and the per-stage day_range_from_sow ladder.

Runs OFFLINE, structural + coherence only. Two tiers:
  * VIOLATIONS (exit 1): shape / enum / ladder-coherence errors, and -- for a REQUIRED scope --
    coverage gaps (a required crop missing propagule). Absence of a new field on an out-of-scope
    crop is a coverage TODO, never a violation, so the un-authored roster stays green.
  * WARNINGS (exit unaffected): harvest-stage-vs-DTM sanity. This is anchor-dependent (a from_sow
    ladder vs a from_transplant DTM differ by the indoor period) and cut-and-come-again crops
    legitimately harvest before DTM -- so it is surfaced for review, not blocked.

Usage:
  python3 tools/timing_spine_gate.py [crops_data_final.json] [--slugs a,b,c | --all-certified] [--warnings]
"""
PROPAGULE_ENUM = {"seed", "transplant", "clove", "set", "tuber", "slip",
                  "crown", "bare_root", "division", "rhizome", "runner"}
DTM_ANCHOR_ENUM = {"from_sow", "from_transplant", "from_planting"}
# propagules whose planting depth is meaningful -> sow_depth_inches required (microgreens exempt).
SEED_LIKE = {"seed", "clove", "set", "tuber"}
# the columns THIS pass adds; day_range_from_sow is PRE-EXISTING (authored at cert) and excluded
# from the amend-not-recert provenance requirement.
NEW_COLUMNS = {"propagule", "dtm_anchor", "sow_depth_inches", "thin_to_inches",
               "harvest_window_days", "divide_every_years"}
ARRAY_FIELDS = ("sow_depth_inches", "thin_to_inches", "harvest_window_days")
DTM_ALIGN_TOL = 0.15  # +/-15% widened DTM band for the harvest-entry sanity warning


# --- archetype N-A predicates (module-level so the register-coverage gate imports, never re-encodes) ---
def dtm_empty(crop):
    """True for a crop with an empty days_to_maturity: perennials/trees/woody herbs with no annual
    maturity to anchor -> legitimately carry NO dtm_anchor and NO day_range_from_sow ladder."""
    dtm = crop.get("days_to_maturity")
    return isinstance(dtm, list) and len(dtm) == 0


def is_microgreen(crop):
    """True for a surface-sown tray crop (empty spacing_inches) -> exempt from sow_depth_inches /
    thin_to_inches (there is no planting depth or thinning for a broadcast tray)."""
    spacing = crop.get("spacing_inches")
    return isinstance(spacing, list) and len(spacing) == 0


def _is_pair(v):
    return isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v)


def _stages(crop):
    return [s for s in (crop.get("growth_stages") or []) if isinstance(s, dict)]


def _harvest_index(stages):
    """The harvest anchor, matched the way crop-timing.ts does: the stage with id 'harvest', else
    the last stage. Monotonicity is enforced up to and INCLUDING this index; later stages
    (dormancy / flowering / spring_regrowth / curing) are cyclic and exempt."""
    for i, s in enumerate(stages):
        if (s.get("id") or s.get("stage_id")) == "harvest":
            return i
    return len(stages) - 1


def _prose(crop):
    sm = crop.get("start_method") or {}
    return " ".join(str(sm.get(k, "")) for k in ("start", "notes_beginner", "notes_seasoned", "notes")).lower()


def timing_spine_violations(crop, catalog=None):
    """Return a list of HARD violation strings ([] = clean) for one crop's timing-spine fields."""
    V = []
    slug = crop.get("slug", "?")
    catalog = catalog or {}
    _dtm_empty = dtm_empty(crop)
    _is_microgreen = is_microgreen(crop)

    # --- enums
    prop = crop.get("propagule")
    if prop is not None and prop not in PROPAGULE_ENUM:
        V.append(f"{slug}: propagule {prop!r} not in {sorted(PROPAGULE_ENUM)}")
    anchor = crop.get("dtm_anchor")
    if anchor is not None and anchor not in DTM_ANCHOR_ENUM:
        V.append(f"{slug}: dtm_anchor {anchor!r} not in {sorted(DTM_ANCHOR_ENUM)}")
    # empty-DTM perennials (citrus, woody herbs) must NOT carry an anchor
    if _dtm_empty and anchor is not None:
        V.append(f"{slug}: dtm_anchor {anchor!r} present but days_to_maturity is empty (no annual maturity to anchor)")

    # --- [min,max] arrays
    for f in ARRAY_FIELDS:
        v = crop.get(f)
        if v is None:
            continue
        if not _is_pair(v):
            V.append(f"{slug}: {f} {v!r} must be a [min,max] numeric pair")
        elif v[0] > v[1]:
            V.append(f"{slug}: {f} {v!r} has min > max")
        elif v[0] < 0:
            V.append(f"{slug}: {f} {v!r} has a negative min")
    dey = crop.get("divide_every_years")
    if dey is not None and not (isinstance(dey, int) and not isinstance(dey, bool) and dey > 0):
        V.append(f"{slug}: divide_every_years {dey!r} must be a positive integer")

    # --- the ladder
    stages = _stages(crop)
    with_range = [s for s in stages if s.get("day_range_from_sow") is not None]
    if with_range and len(with_range) != len(stages):
        V.append(f"{slug}: ladder is partial -- {len(with_range)}/{len(stages)} stages carry "
                 f"day_range_from_sow (all-or-nothing)")
    elif with_range:  # full ladder -> shape + monotonic-min up to the harvest anchor
        for s in stages:
            dr = s.get("day_range_from_sow")
            sid = s.get("id") or s.get("stage_id") or "?"
            if not _is_pair(dr):
                V.append(f"{slug}: stage {sid!r} day_range_from_sow {dr!r} must be a [min,max] numeric pair")
            elif dr[0] > dr[1]:
                V.append(f"{slug}: stage {sid!r} day_range_from_sow {dr!r} has min > max")
        hi = _harvest_index(stages)
        mins = [stages[i].get("day_range_from_sow") for i in range(hi + 1)]
        if all(_is_pair(m) for m in mins):
            for i in range(len(mins) - 1):
                if mins[i + 1][0] < mins[i][0]:
                    sid = stages[i + 1].get("id") or stages[i + 1].get("stage_id")
                    V.append(f"{slug}: ladder mins non-decreasing violated at {sid!r} "
                             f"({mins[i + 1][0]} < {mins[i][0]}) up to the harvest anchor")
                    break

    # --- sow_depth required for seed-like propagules (microgreens surface-sown -> exempt)
    if prop in SEED_LIKE and not _is_microgreen and crop.get("sow_depth_inches") is None:
        V.append(f"{slug}: propagule {prop!r} requires sow_depth_inches (planting depth)")

    # --- propagule <-> start_method consistency
    if prop is not None:
        start = (crop.get("start_method") or {}).get("start")
        prose = _prose(crop)
        if prop == "seed" and start == "grafted_nursery_tree":
            V.append(f"{slug}: propagule 'seed' contradicts start_method.start 'grafted_nursery_tree'")
        for pw in ("clove", "slip", "tuber", "rhizome"):
            if prop == pw and pw not in prose:
                V.append(f"{slug}: propagule {pw!r} but start_method prose never mentions a {pw}")

    # --- amend-not-recert provenance: a certified crop carrying a NEW column must log it
    if crop.get("verification_status", {}).get("status") == "verified_gs_arc":
        if any(crop.get(col) is not None for col in NEW_COLUMNS):
            fa = crop.get("verification_status", {}).get("field_additions") or []
            timing_entries = [e for e in fa if isinstance(e, dict)
                              and e.get("field") in (NEW_COLUMNS | {"timing_spine"})]
            if not timing_entries:
                V.append(f"{slug}: timing-spine field present on a certified crop but no "
                         f"field_additions entry for it")
            for e in timing_entries:
                for s in (e.get("sources") or []):
                    entry = catalog.get(s)
                    if entry is None:
                        V.append(f"{slug}: timing field_additions source {s!r} not in source_catalog")
                    elif entry.get("tier") != "T1":
                        V.append(f"{slug}: timing field_additions source {s!r} is not T1 (tier={entry.get('tier')!r})")
    return V


def timing_spine_warnings(crop):
    """Surfaced-not-blocking: harvest-stage entry outside a +/-15% widened DTM band. Anchor-dependent
    and cut-and-come-again crops legitimately harvest before DTM, so this is advisory only."""
    W = []
    slug = crop.get("slug", "?")
    dtm = crop.get("days_to_maturity")
    stages = _stages(crop)
    if not (isinstance(dtm, list) and len(dtm) == 2) or not stages:
        return W
    harv = stages[_harvest_index(stages)]
    h = harv.get("day_range_from_sow")
    if not _is_pair(h):
        return W
    lo, hi = dtm[0] * (1 - DTM_ALIGN_TOL), dtm[1] * (1 + DTM_ALIGN_TOL)
    if not (lo <= h[0] <= hi):
        W.append(f"{slug}: harvest-stage entry {h[0]} outside +/-15% DTM band "
                 f"[{round(lo)},{round(hi)}] (DTM {dtm}); check dtm_anchor / individualize the ladder")
    return W


def coverage_report(crops, required_slugs):
    """counts = {'propagule_set': n}; todo = sorted required slugs still missing propagule
    (the one field every crop must carry)."""
    present = {c.get("slug") for c in crops if c.get("propagule") in PROPAGULE_ENUM}
    todo = sorted(s for s in required_slugs if s not in present)
    return {"propagule_set": len(present)}, todo


if __name__ == "__main__":
    import argparse
    import json
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="crops_data_final.json")
    ap.add_argument("--slugs", help="comma-separated slugs REQUIRED to carry the timing spine")
    ap.add_argument("--all-certified", action="store_true",
                    help="require the timing spine on ALL verified_gs_arc crops")
    ap.add_argument("--warnings", action="store_true", help="also print surfaced warnings")
    a = ap.parse_args()

    data = json.load(open(a.path, encoding="utf-8"))
    catalog = data.get("source_catalog", {})
    crops = data["crops"]

    total = 0
    for c in crops:
        for v in timing_spine_violations(c, catalog):
            print(f"  VIOLATION: {v}")
            total += 1

    warns = 0
    if a.warnings:
        for c in crops:
            for w in timing_spine_warnings(c):
                print(f"  WARNING: {w}")
                warns += 1

    required = set()
    if a.slugs:
        required = {s.strip() for s in a.slugs.split(",") if s.strip()}
    elif a.all_certified:
        required = {c.get("slug") for c in crops
                    if c.get("verification_status", {}).get("status") == "verified_gs_arc"}
    counts, todo = coverage_report(crops, required)

    print(f"timing_spine: propagule_set={counts['propagule_set']}/{len(crops)} | "
          f"violations={total} warnings={warns} | todo(required)={len(todo)}")
    if todo:
        print(f"  TODO (required but missing propagule): {todo}")
    sys.exit(1 if (total or todo) else 0)
