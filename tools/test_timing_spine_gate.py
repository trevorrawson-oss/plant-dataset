#!/usr/bin/env python3
"""Tests for the timing-spine gate (Plan 3 field authoring). Run:
    python3 tools/test_timing_spine_gate.py

WHY: the timing spine (propagule / dtm_anchor / sow_depth_inches / thin_to_inches /
harvest_window_days / divide_every_years + the per-stage day_range_from_sow ladder) feeds the
app's seed->harvest compute. A wrong stage offset, a bad DTM anchor, or a mislabeled propagule
becomes a wrong harvest date a grower plans around. Each assertion below sneaks ONE defect class at
the gate and confirms it bounces. HARD violations (exit 1) are shape/coherence errors; WARNINGS are
surfaced-not-blocking (anchor-dependent harvest<->DTM sanity). Absence of a new field is a COVERAGE
concern (the authoring TODO), never a shape violation -- so the un-authored roster stays green.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_spine_gate import timing_spine_violations, timing_spine_warnings, coverage_report

CATALOG = {
    "uga_ext": {"id": "uga_ext", "tier": "T1"},
    "clemson_hgic": {"id": "clemson_hgic", "tier": "T1"},
    "some_blog": {"id": "some_blog", "tier": "T2"},
}

FA_TIMING = [{"field": "timing_spine", "date": "2026-07-07",
             "sources": ["uga_ext"], "note": "timing-spine column pass; amend-not-recert"}]


def propagule_crop():
    """garlic-like: clove propagule, from_planting, full monotonic ladder w/ harvest anchor."""
    return {
        "slug": "garlic",
        "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
        "days_to_maturity": [180, 270],
        "spacing_inches": [4, 6],
        "propagule": "clove",
        "dtm_anchor": "from_planting",
        "sow_depth_inches": [2, 3],
        "start_method": {"start": "direct", "notes_beginner": "Garlic does not grow from seed; you plant the cloves pointy side up."},
        "growth_stages": [
            {"id": "planting", "day_range_from_sow": [0, 30]},
            {"id": "early_growth", "day_range_from_sow": [30, 150]},
            {"id": "established", "day_range_from_sow": [150, 210]},
            {"id": "bulb_forming", "day_range_from_sow": [210, 250]},
            {"id": "harvest", "day_range_from_sow": [250, 275]},
            {"id": "curing", "day_range_from_sow": [275, 300]},
        ],
    }


def annual_crop():
    """tomato-like: seed, from_transplant, thinnable, ladder harvest ~ DTM."""
    return {
        "slug": "cherry-tomato",
        "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
        "days_to_maturity": [55, 70],
        "spacing_inches": [24, 36],
        "propagule": "seed",
        "dtm_anchor": "from_transplant",
        "sow_depth_inches": [0.25, 0.5],
        "thin_to_inches": [24, 36],
        "harvest_window_days": [30, 60],
        "start_method": {"start": "indoors", "notes_beginner": "Start seeds indoors 6 weeks before last frost."},
        "growth_stages": [
            {"id": "germination", "day_range_from_sow": [5, 10]},
            {"id": "seedling", "day_range_from_sow": [7, 28]},
            {"id": "established", "day_range_from_sow": [28, 56]},
            {"id": "flowering", "day_range_from_sow": [45, 75]},
            {"id": "harvest", "day_range_from_sow": [55, 80]},
        ],
    }


def perennial_empty_dtm():
    """rosemary-like: empty DTM, NO dtm_anchor, NO ladder (all stages absent), transplant."""
    return {
        "slug": "rosemary",
        "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
        "days_to_maturity": [],
        "spacing_inches": [24, 36],
        "propagule": "transplant",
        "start_method": {"start": "nursery_transplant", "notes_beginner": "Buy a small plant or take a cutting; seed is slow."},
        "growth_stages": [
            {"id": "transplant"},
            {"id": "establishment"},
            {"id": "vegetative"},
        ],
    }


def microgreen_crop():
    """radish-microgreens-like: seed but surface-broadcast -> spacing_inches [] marks the
    exemption from BOTH sow_depth and thin_to_inches."""
    return {
        "slug": "radish-microgreens",
        "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
        "days_to_maturity": [7, 12],
        "spacing_inches": [],
        "propagule": "seed",
        "start_method": {"start": "indoors", "notes_beginner": "Scatter seed thickly; do not bury."},
        "growth_stages": [
            {"stage_id": "sow"}, {"stage_id": "germination"}, {"stage_id": "harvest"},
        ],
    }


# ---------------------------------------------------------------- clean fixtures
for f in (propagule_crop, annual_crop, perennial_empty_dtm, microgreen_crop):
    assert timing_spine_violations(f(), CATALOG) == [], (f.__name__, timing_spine_violations(f(), CATALOG))
    assert timing_spine_warnings(f()) == [], (f.__name__, timing_spine_warnings(f()))

# 0. an un-authored crop (no new fields, no ladder) -> no violations (coverage owns presence)
bare = {"slug": "x", "days_to_maturity": [50, 60], "growth_stages": [{"id": "a"}, {"id": "harvest"}]}
assert timing_spine_violations(bare, CATALOG) == [], timing_spine_violations(bare, CATALOG)

# 1. propagule not in enum -> violation
c = propagule_crop(); c["propagule"] = "bulbil"
assert any("propagule" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 2. dtm_anchor not in enum -> violation
c = annual_crop(); c["dtm_anchor"] = "from_moon"
assert any("dtm_anchor" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 3. empty-DTM crop carrying a dtm_anchor -> violation
c = perennial_empty_dtm(); c["dtm_anchor"] = "from_planting"
assert any("dtm_anchor" in v and "empty" in v.lower() for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 4. inverted [min,max] on a new array field -> violation
for field, bad in [("sow_depth_inches", [3, 2]), ("thin_to_inches", [10, 4]), ("harvest_window_days", [60, 30])]:
    c = annual_crop(); c[field] = bad
    assert any(field in v for v in timing_spine_violations(c, CATALOG)), (field, timing_spine_violations(c, CATALOG))

# 5. negative depth -> violation
c = annual_crop(); c["sow_depth_inches"] = [-1, 2]
assert any("sow_depth_inches" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 6. partial ladder (some stages have day_range, some don't) -> violation
c = annual_crop(); del c["growth_stages"][2]["day_range_from_sow"]
assert any("ladder" in v.lower() or "day_range" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 7. a stage day_range inverted (min>max) -> violation
c = annual_crop(); c["growth_stages"][1]["day_range_from_sow"] = [28, 7]
assert any("day_range" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 8. mins DECREASING within the productive ladder (up to harvest anchor) -> violation (shallot-class)
#    shallot: last stage is the harvest anchor (no 'harvest' id), so the whole ladder must be monotonic.
shallot = {
    "slug": "shallot", "days_to_maturity": [90, 120], "propagule": "set", "spacing_inches": [4, 6],
    "sow_depth_inches": [1, 2], "dtm_anchor": "from_planting",
    "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
    "start_method": {"start": "direct", "notes_beginner": "Plant sets pointy end up."},
    "growth_stages": [
        {"id": "germination_emergence", "day_range_from_sow": [7, 21]},
        {"id": "leaf_canopy_building", "day_range_from_sow": [21, 90]},
        {"id": "bulb_initiation", "day_range_from_sow": [70, 110]},
        {"id": "bulb_sizing", "day_range_from_sow": [95, 125]},
        {"id": "maturity_curing", "day_range_from_sow": [90, 140]},  # 90 < 95 -> defect
    ],
}
assert any("non-decreasing" in v or "monotonic" in v.lower() or "decreas" in v.lower()
           for v in timing_spine_violations(shallot, CATALOG)), timing_spine_violations(shallot, CATALOG)

# 9. post-harvest cyclic stages MAY dip below (chives-class) -> NO monotonicity violation
chives = {
    "slug": "chives", "days_to_maturity": [60, 90], "propagule": "division", "spacing_inches": [6, 12],
    "dtm_anchor": "from_planting",
    "verification_status": {"status": "verified_gs_arc", "field_additions": FA_TIMING},
    "start_method": {"start": "transplant", "notes_beginner": "Start from a plant or a division."},
    "growth_stages": [
        {"id": "germination", "day_range_from_sow": [14, 42]},
        {"id": "establishment", "day_range_from_sow": [30, 120]},
        {"id": "harvest", "day_range_from_sow": [60, 300]},
        {"id": "flowering", "day_range_from_sow": [300, 420]},
        {"id": "dormancy", "day_range_from_sow": [240, 400]},  # dips below flowering, but post-harvest
    ],
}
assert not any("decreas" in v.lower() or "monotonic" in v.lower() or "non-decreasing" in v
               for v in timing_spine_violations(chives, CATALOG)), timing_spine_violations(chives, CATALOG)

# 10. seed/clove/set/tuber propagule missing sow_depth_inches -> violation
for prop in ("seed", "clove", "set", "tuber"):
    c = annual_crop(); c["propagule"] = prop; del c["sow_depth_inches"]
    if prop == "clove":
        c["start_method"]["notes_beginner"] = "plant the cloves pointy side up"
    assert any("sow_depth" in v for v in timing_spine_violations(c, CATALOG)), (prop, timing_spine_violations(c, CATALOG))

# 11. microgreen (spacing_inches []) is EXEMPT from sow_depth + thin_to requirements
mg = microgreen_crop()
assert timing_spine_violations(mg, CATALOG) == [], timing_spine_violations(mg, CATALOG)

# 12. non-seed-like propagule (transplant/division/slip) need NOT carry sow_depth
c = perennial_empty_dtm()  # transplant, no sow_depth
assert not any("sow_depth" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 13. propagule<->start consistency: seed on a grafted tree -> violation
c = annual_crop(); c["propagule"] = "seed"; c["start_method"]["start"] = "grafted_nursery_tree"
assert any("propagule" in v and ("start" in v or "graft" in v) for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 14. propagule clove but prose never mentions a clove -> violation
c = propagule_crop(); c["start_method"]["notes_beginner"] = "Plant it in fall and mulch well."
assert any("propagule" in v and "clove" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 15. certified crop carrying a NEW column but NO field_additions provenance -> violation
c = propagule_crop(); c["verification_status"] = {"status": "verified_gs_arc"}
assert any("field_additions" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# 16. day_range_from_sow is a PRE-EXISTING column (authored at cert) -> its presence alone does NOT
#     demand a timing field_additions entry (only the 6 NEW columns do)
c = {"slug": "carrot", "days_to_maturity": [60, 75],
     "verification_status": {"status": "verified_gs_arc"},  # no field_additions
     "growth_stages": [{"id": "germination", "day_range_from_sow": [0, 21]},
                       {"id": "harvest", "day_range_from_sow": [60, 75]}]}
assert timing_spine_violations(c, CATALOG) == [], timing_spine_violations(c, CATALOG)

# 17. provenance source must be catalogued + T1
c = propagule_crop()
c["verification_status"]["field_additions"] = [{"field": "timing_spine", "sources": ["some_blog"]}]
assert any("T1" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)
c["verification_status"]["field_additions"] = [{"field": "timing_spine", "sources": ["not_a_source"]}]
assert any("not_a_source" in v for v in timing_spine_violations(c, CATALOG)), timing_spine_violations(c, CATALOG)

# ---------------------------------------------------------------- WARNINGS (surfaced, non-blocking)
# 18. harvest-stage entry far from DTM (anchor mismatch / templated ladder) -> WARNING, not violation
c = annual_crop(); c["days_to_maturity"] = [75, 90]  # beefsteak-class: harvest entry 55 vs DTM 75-90
assert timing_spine_violations(c, CATALOG) == [], timing_spine_violations(c, CATALOG)
assert any("dtm" in w.lower() or "harvest" in w.lower() for w in timing_spine_warnings(c)), timing_spine_warnings(c)

# 19. aligned harvest entry -> no warning
assert timing_spine_warnings(annual_crop()) == [], timing_spine_warnings(annual_crop())

# ---------------------------------------------------------------- coverage
crops = [propagule_crop(), annual_crop(), {"slug": "onion"}]  # onion un-authored
counts, todo = coverage_report(crops, {"garlic", "cherry-tomato", "onion"})
assert todo == ["onion"], todo
assert counts["propagule_set"] == 2, counts

# all required authored -> empty todo
counts, todo = coverage_report(crops, {"garlic", "cherry-tomato"})
assert todo == [], todo

# ---------------------------------------------------------------- CLI exit codes (subprocess)
import json as _json
import subprocess
import tempfile

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timing_spine_gate.py")


def _run(fixture, extra=None):
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        _json.dump(fixture, fh)
    try:
        r = subprocess.run([sys.executable, _GATE, p] + (extra or []),
                           capture_output=True, text=True)
        return r.returncode, r.stdout
    finally:
        os.unlink(p)


_clean = {"crops": [propagule_crop()], "source_catalog": CATALOG}
_bad = {"crops": [dict(propagule_crop(), propagule="bulbil")], "source_catalog": CATALOG}
_warn_only = {"crops": [dict(annual_crop(), days_to_maturity=[75, 90])], "source_catalog": CATALOG}
_cov_gap = {"crops": [{"slug": "garlic"}], "source_catalog": CATALOG}

assert _run(_clean)[0] == 0, "clean fixture should exit 0"
assert _run(_bad)[0] == 1, "bad-enum fixture should exit 1"
assert _run(_warn_only)[0] == 0, "warning-only fixture should exit 0 (warnings don't block)"
assert _run(_cov_gap, ["--slugs", "garlic"])[0] == 1, "coverage gap on a required slug should exit 1"
assert _run(_cov_gap)[0] == 0, "coverage gap with NO required scope should exit 0"

print("timing_spine_gate tests: OK")
