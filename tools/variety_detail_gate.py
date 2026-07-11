#!/usr/bin/env python3
"""variety_detail_gate -- validates the flat, load-bearing per-variety schema (spec 2026-07-11).

SOFT gate (timing_spine pattern): a crop OPTS IN by carrying `maturity_class` on any variety object;
off-scope crops (the legacy simple/delta/string shapes) are silent, so the un-migrated roster stays
green. It is standalone + NOT wired into whole_crop_gate/A39 this spec (that hard-flip is Spec 2).

VIOLATIONS (exit 1, in-scope crops only): required-field presence, enum membership, exactly-one
is_reference, slug-shaped + unique id, DTM present-int-in-[7,400]. A season-only crop (empty crop
days_to_maturity) may omit variety DTM and carry maturity_class alone.

WARNINGS (advisory, never block, honoring 'the source is authoritative'): a variety DTM outside the
crop band +/-MARGIN AND with no per-variety source; class/DTM ordering (fastest labeled 'late' /
slowest 'early'). A sourced value never warns, however far out of band.

Usage: variety_detail_gate.py [PATH] [--warnings] [--coverage]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_spine_gate import dtm_empty  # season-only predicate (empty days_to_maturity); do not re-encode

MATURITY_CLASS = {"early", "mid", "late"}
CONFIDENCE = {"T1", "T2", "T3", "T4"}
# annual (dry-bean) archetype
SEED_TYPE = {"open_pollinated", "hybrid", "heirloom"}
SEED_SIZE = {"small", "medium", "large"}
PLANT_HABIT = {"bush", "half_runner", "pole"}
PRIMARY_USE = {"soup", "baked", "chili", "fresh_shell", "multi"}
# tree_fruit (apple) archetype
BLOOM_GROUP = {"very_early", "early", "mid", "late", "very_late"}
SELF_FRUITFUL = {"no", "partial", "yes"}

DTM_FLOOR, DTM_CEIL = 7, 400   # mirrors numeric_sanity A33; the only HARD numeric bound
DTM_MARGIN = 10                # advisory band widening; low-stakes (sourced values never warn)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

COMMON_CORE = ("id", "name", "maturity_class", "confidence_tier",
               "note_beginner", "note_seasoned", "sources")
ANNUAL_TRAITS = ("seed_type", "seed_color", "seed_size", "plant_habit", "primary_use")
TREE_TRAITS = ("bloom_group", "bloom_window_relative", "bloom_duration_days",
               "chill_hours_required", "use")
COMMON_ENUMS = (("maturity_class", MATURITY_CLASS), ("confidence_tier", CONFIDENCE))
ANNUAL_ENUMS = (("seed_type", SEED_TYPE), ("seed_size", SEED_SIZE),
                ("plant_habit", PLANT_HABIT), ("primary_use", PRIMARY_USE))
TREE_ENUMS = (("bloom_group", BLOOM_GROUP),)


def archetype(crop):
    """Crop declares its variety archetype; absence defaults to annual_dtm (dry-bean stays untouched)."""
    a = crop.get("variety_archetype")
    return a if a in ("annual_dtm", "tree_fruit") else "annual_dtm"


def _variety_objs(crop):
    v = crop.get("varieties")
    if not isinstance(v, dict):
        return []
    rec = v.get("recommended")
    if not isinstance(rec, list):
        return []
    return [x for x in rec if isinstance(x, dict)]


def in_scope(crop):
    """A crop opts into the flat variety-detail schema by carrying maturity_class on any variety."""
    return any("maturity_class" in x for x in _variety_objs(crop))


def _int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def variety_violations(crop):
    V = []
    if not in_scope(crop):
        return V
    slug = crop.get("slug", "?")
    arch = archetype(crop)
    season_only = dtm_empty(crop)
    required = COMMON_CORE + (TREE_TRAITS if arch == "tree_fruit" else ANNUAL_TRAITS)
    enums = COMMON_ENUMS + (TREE_ENUMS if arch == "tree_fruit" else ANNUAL_ENUMS)
    vars_ = _variety_objs(crop)
    ids, ref_count = [], 0
    for x in vars_:
        nm = x.get("name") or x.get("id") or "?"
        for f in required:
            if f not in x or x[f] in (None, "", []):
                V.append(f"{slug}/{nm}: missing required variety field {f!r}")
        for f, enum in enums:
            if f in x and x[f] not in enum:
                V.append(f"{slug}/{nm}: {f} {x[f]!r} not in {sorted(enum)}")
        vid = x.get("id")
        if isinstance(vid, str):
            if not SLUG_RE.match(vid):
                V.append(f"{slug}/{nm}: id {vid!r} is not slug-shaped")
            ids.append(vid)
        ir = x.get("is_reference")
        if not isinstance(ir, bool):
            V.append(f"{slug}/{nm}: is_reference {ir!r} must be a bool")
        elif ir:
            ref_count += 1
        if arch == "annual_dtm":
            V += _annual_dtm_checks(slug, nm, x, season_only)
        else:
            V += _tree_checks(slug, nm, x)
    if ref_count != 1:
        V.append(f"{slug}: exactly one variety must have is_reference true (found {ref_count})")
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        V.append(f"{slug}: duplicate variety id(s) {dupes}")
    return V


def _annual_dtm_checks(slug, nm, x, season_only):
    """days_to_maturity presence/int/[7,400] for the annual archetype (unchanged behavior)."""
    V = []
    dtm = x.get("days_to_maturity")
    if dtm is None:
        if not season_only:
            V.append(f"{slug}/{nm}: days_to_maturity missing (crop is DTM-based)")
    elif not _int(dtm):
        V.append(f"{slug}/{nm}: days_to_maturity {dtm!r} must be an int")
    elif not (DTM_FLOOR <= dtm <= DTM_CEIL):
        V.append(f"{slug}/{nm}: days_to_maturity {dtm} outside [{DTM_FLOOR},{DTM_CEIL}]")
    return V


def _tree_checks(slug, nm, x):
    """Tree-fruit block: bloom-window shape, positive-int chill/duration, triploid bool, self_fruitful enum."""
    V = []
    bwr = x.get("bloom_window_relative")
    if bwr is not None:
        if (not isinstance(bwr, list) or len(bwr) != 2
                or not all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in bwr)
                or not (0.0 <= bwr[0] < bwr[1] <= 1.0)):
            V.append(f"{slug}/{nm}: bloom_window_relative {bwr!r} must be [start,end] floats "
                     f"in [0,1] with start < end")
    for f in ("bloom_duration_days", "chill_hours_required"):
        val = x.get(f)
        if val is not None and (not _int(val) or val <= 0):
            V.append(f"{slug}/{nm}: {f} {val!r} must be a positive int")
    trip = x.get("triploid")
    if not isinstance(trip, bool):
        V.append(f"{slug}/{nm}: triploid {trip!r} must be a bool")
    sf = x.get("self_fruitful")
    if sf is not None and sf not in SELF_FRUITFUL:
        V.append(f"{slug}/{nm}: self_fruitful {sf!r} not in {sorted(SELF_FRUITFUL)}")
    return V


def variety_warnings(crop):
    W = []
    if not in_scope(crop):
        return W
    slug = crop.get("slug", "?")
    vars_ = _variety_objs(crop)
    if archetype(crop) == "tree_fruit":
        return _tree_warnings(slug, vars_)
    # --- annual archetype (unchanged) ---
    band = crop.get("days_to_maturity")
    if isinstance(band, list) and len(band) == 2 and all(_int(b) for b in band):
        lo, hi = band[0] - DTM_MARGIN, band[1] + DTM_MARGIN
        for x in vars_:
            dtm = x.get("days_to_maturity")
            if _int(dtm) and not (lo <= dtm <= hi) and not x.get("sources"):
                W.append(f"{slug}/{x.get('name', '?')}: DTM {dtm} outside band+/-{DTM_MARGIN} "
                         f"[{lo},{hi}] and UNSOURCED -- verify or source")
    dtms = [(x.get("name", "?"), x.get("days_to_maturity"), x.get("maturity_class"))
            for x in vars_ if _int(x.get("days_to_maturity"))]
    if len(dtms) >= 2:
        fastest = min(dtms, key=lambda t: t[1])
        slowest = max(dtms, key=lambda t: t[1])
        if fastest[2] == "late":
            W.append(f"{slug}/{fastest[0]}: fastest variety (DTM {fastest[1]}) labeled 'late'")
        if slowest[2] == "early":
            W.append(f"{slug}/{slowest[0]}: slowest variety (DTM {slowest[1]}) labeled 'early'")
    return W


BLOOM_RANK = {"very_early": 0, "early": 1, "mid": 2, "late": 3, "very_late": 4}


def _tree_warnings(slug, vars_):
    """Advisory: bloom_group ordering must agree with bloom_window_relative start ordering."""
    W = []
    pairs = []
    for x in vars_:
        g = BLOOM_RANK.get(x.get("bloom_group"))
        bwr = x.get("bloom_window_relative")
        if g is not None and isinstance(bwr, list) and len(bwr) == 2:
            pairs.append((x.get("name", "?"), g, bwr[0]))
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            ni, gi, si = pairs[i]
            nj, gj, sj = pairs[j]
            if gi < gj and si > sj:
                W.append(f"{slug}/{ni}: bloom_group '{list(BLOOM_RANK)[gi]}' earlier than "
                         f"{nj} '{list(BLOOM_RANK)[gj]}' but relative start {si} > {sj} (order mismatch)")
    return W


def coverage_report(crops):
    slugs = sorted(c.get("slug") for c in crops if in_scope(c))
    objs = sum(len(_variety_objs(c)) for c in crops if in_scope(c))
    return {"in_scope_crops": len(slugs), "variety_objs": objs, "slugs": slugs}


if __name__ == "__main__":
    args = list(sys.argv[1:])
    show_warn = "--warnings" in args
    show_cov = "--coverage" in args
    args = [a for a in args if a not in ("--warnings", "--coverage")]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    total = 0
    for c in crops:
        for v in variety_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    warns = 0
    if show_warn:
        for c in crops:
            for w in variety_warnings(c):
                print(f"  WARNING: {w}")
                warns += 1
    cov = coverage_report(crops)
    if show_cov:
        print(f"  COVERAGE: in_scope_crops={cov['in_scope_crops']} variety_objs={cov['variety_objs']} "
              f"slugs={cov['slugs']}")
    print(f"variety_detail: in_scope={cov['in_scope_crops']} objs={cov['variety_objs']} | "
          f"violations={total} warnings={warns}")
    sys.exit(1 if total else 0)
