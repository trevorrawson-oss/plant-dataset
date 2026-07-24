#!/usr/bin/env python3
"""Tests for the calendar-COHERENCE gate (whole_crop_gate A37).
Run: python3 tools/test_calendar_coherence_gate.py

WHAT IT ARMS AGAINST: the gate suite checked calendar STRUCTURE, not calendar LOGIC, so two
temporally-impossible token patterns shipped in certified anchors + the live 13 (found by Trevor
eyeballing rendered ca_interior guides, 2026-06-30; see docs/calendar-coherence-*-2026-06-30.md):

  Bug 1 -- "growing after harvest": a `growing` token that cannot be reached from a plant/indoors
    without first passing a crop-REMOVED state (harvest/season_over). You can't be vegetatively
    growing when the last lifecycle event was a harvest and nothing was replanted. frost_anchored
    only (an evergreen perennial legitimately grows after harvest). Dormancy (cold_pause) and
    heat pauses are walk-THROUGH -- the plant is still in the ground (garlic overwinters).

  Bug 2 -- "one-month harvest hole": a single non-harvest month punched out of an otherwise-
    continuous `harvest` display window (lettuce 'Sep - Oct, Dec - May', Nov missing). All crops;
    multi-month gaps (two discrete plantings) stay legal.

TDD RED-first: the gate must BOUNCE both injected signatures and produce ZERO false positives on
the legitimate patterns below (garlic overwintering, winter-wrapping, year-round, perennials,
multi-month gaps).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calendar_coherence_gate import (
    growing_reachability_violations,   # Bug 1 (frost_anchored)
    harvest_hole_violations,           # Bug 2 (all crops)
    calendar_coherence_violations,     # A37 entry point (both)
)


# ------------------------------------------------------------------ fixtures
def _crop(calendar_basis="frost_anchored", calendar=None, harvest=None,
          plant_out=None, start_indoors=None, heat_pause_months=None):
    """A one-region/one-zone crop fixture."""
    cell = {}
    if calendar is not None:
        cell["calendar"] = calendar
    if harvest is not None:
        cell["harvest"] = harvest
    if plant_out is not None:
        cell["plant_out"] = plant_out
    if start_indoors is not None:
        cell["start_indoors"] = start_indoors
    if heat_pause_months is not None:
        cell["heat_pause"] = {"months": heat_pause_months}
    return {"slug": "test", "calendar_basis": calendar_basis,
            "regions": {"r1": {"resolved_by_zone": {"9": cell}}}}


# months are 0=Jan .. 11=Dec
COLD = "cold_pause"


# ============================================================ BUG 1 -- RED
# 1. growing immediately after harvest -> VIOLATION
cal = ["harvest", "growing"] + [COLD] * 10          # Feb growing, prev Jan harvest
assert growing_reachability_violations(_crop(calendar=cal)), \
    "growing directly after harvest must be flagged"

# 2. growing after season_over -> VIOLATION (season_over is also a crop-removed blocker)
cal = ["season_over", "growing"] + [COLD] * 10
assert growing_reachability_violations(_crop(calendar=cal)), \
    "growing after season_over must be flagged"

# 3. a multi-month impossible run -> one violation per impossible growing-month
cal = ["harvest", "growing", "growing", "growing"] + [COLD] * 8
v = growing_reachability_violations(_crop(calendar=cal))
assert len(v) == 3, f"a 3-month growing-after-harvest run should flag 3 months, got {len(v)}: {v}"

# 4. the violation message names the offending month/location (for the §8.1 diff)
cal = ["harvest", "growing"] + [COLD] * 10
v = growing_reachability_violations(_crop(calendar=cal))
assert any("Feb" in m for m in v), f"message must name the month: {v}"


# ======================================================= BUG 1 -- 0 FALSE POS
# 5. growing after plant -> CLEAN (the normal grow-toward-harvest)
cal = ["plant", "growing", "harvest"] + [COLD] * 9
assert growing_reachability_violations(_crop(calendar=cal)) == [], "growing after plant is legit"

# 6. growing after indoors -> CLEAN
cal = ["indoors", "growing", "harvest"] + [COLD] * 9
assert growing_reachability_violations(_crop(calendar=cal)) == [], "growing after indoors is legit"

# 7. GARLIC overwintering: plant(Oct) -> cold_pause(winter) -> growing(spring) -> harvest.
#    cold_pause is dormancy (plant IS in the ground), so the spring growing traces back
#    THROUGH cold_pause to the fall plant -> CLEAN. (The 98->114 relaxation must not over-catch.)
cal = [COLD, COLD, "growing", "growing", "growing", "growing", "harvest",
       "season_over", "season_over", "plant", COLD, COLD]
assert growing_reachability_violations(_crop(calendar=cal)) == [], \
    "garlic growing-after-cold_pause (traces to fall plant) must NOT flag"

# 8. WINTER-WRAP: plant(Oct) -> growing(Nov..Feb across the year wrap) -> harvest(Mar).
#    Jan growing traces backward through Dec/Nov growing to the Oct plant via the wrap -> CLEAN.
cal = ["growing", "growing", "harvest", "season_over", "season_over", "season_over",
       "season_over", "season_over", "season_over", "plant", "growing", "growing"]
assert growing_reachability_violations(_crop(calendar=cal)) == [], \
    "winter-wrapping growing (traces to Oct plant via wrap) must NOT flag"

# 9. YEAR-ROUND 12x growing -> CLEAN (no blocker anywhere; not the growing-after-harvest bug)
assert growing_reachability_violations(_crop(calendar=["growing"] * 12)) == [], \
    "a continuous year-round growing calendar must NOT flag"

# 10. growing after heat_pause that traces to a plant -> CLEAN (heat pause = plant still alive)
cal = ["plant", "growing", "heat_pause", "growing", "harvest"] + [COLD] * 7
assert growing_reachability_violations(_crop(calendar=cal)) == [], \
    "growing after a heat_pause that traces back to plant must NOT flag"

# 11. PERENNIAL exemption: an evergreen citrus growing-after-harvest is correct biology -> CLEAN
cal = ["harvest", "growing", "bloom", "bloom", "growing", "growing",
       "growing", "growing", "growing", "growing", "harvest", "harvest"]
assert growing_reachability_violations(_crop("perennial_evergreen", calendar=cal)) == [], \
    "Bug 1 is frost_anchored-only; perennials are exempt"

# 11b. NEAR-YEAR-ROUND continuous producer (harvest window >= 10 months, e.g. hawaii zucchini
#      'Feb 15 - Dec 15') -> CLEAN. Interspersed `growing` is the tropical production lull, not the
#      growing-after-harvest bug (the annual analog of the perennial-evergreen exemption).
cal = ["growing", "plant", "plant", "growing", "harvest", "harvest",
       "growing", "growing", "harvest", "harvest", "harvest", "growing"]
assert growing_reachability_violations(
    _crop(calendar=cal, harvest="Feb 15 - Dec 15")) == [], \
    "a near-year-round (>=10-month harvest) continuous producer must NOT flag growing-after-harvest"
# but the SAME calendar with a sparse (two-crop) harvest window still flags (proves it's the
# coverage, not the calendar shape, that exempts):
assert growing_reachability_violations(
    _crop(calendar=cal, harvest="May - Jun, Sep - Nov")), \
    "the same growing tokens under a sparse two-crop harvest window must still flag"

# 11c. FORWARD-CLAUSE: an OUT-OF-WINDOW `growing` that leads FORWARD into a harvest (a fall crop
#      growing toward harvest whose plant token is masked by heat_pause, e.g. beefsteak se_gulf z8
#      Sep) is a producing arc, not growing-after-harvest -> CLEAN. But an IN-WINDOW growing on the
#      same run is still flagged (it should become harvest, not stay growing).
cal = ["cold_pause", "indoors", "plant", "growing", "harvest", "heat_pause", "heat_pause",
       "heat_pause", "growing", "growing", "harvest", "cold_pause"]
v = growing_reachability_violations(_crop(calendar=cal, harvest="May, Oct - Nov"))
assert not any("Sep" in m for m in v), \
    f"out-of-window growing leading forward to a harvest (Sep) must NOT flag: {v}"
assert any("Oct" in m for m in v), \
    f"in-window growing (Oct) must still flag so it becomes harvest: {v}"
# a growing that leads forward only to a PLANT (a real gap before a replant) still flags
cal2 = ["growing", "plant", "plant", "harvest", "harvest"] + ["heat_pause"] * 5 + ["harvest", "harvest"]
# Jan growing -> forward Feb=plant (not harvest) -> still a gap; but here Jan traces back (wrap) to
# Dec harvest -> must flag:
assert growing_reachability_violations(
    _crop(calendar=["harvest", "growing", "plant"] + ["cold_pause"] * 9, harvest="Jan, Mar")), \
    "growing that leads forward to a PLANT (not harvest) is a real gap and must still flag"


# ============================================================ BUG 2 -- RED
# 12. one-month harvest-display hole (lettuce ca_interior: Nov punched out) -> VIOLATION
v = harvest_hole_violations(_crop(harvest="Sep - Oct, Dec - May", calendar=["plant"] * 12))
assert v, "a one-month harvest-display hole must be flagged"
assert any("Nov" in m for m in v), f"message must name the hole month: {v}"

# 13. hole with a wrap (kale: 'Mar - May, Oct - Jan', Feb punched out) -> VIOLATION
v = harvest_hole_violations(_crop(harvest="Mar - May, Oct - Jan", calendar=["plant"] * 12))
assert any("Feb" in m for m in v), f"kale Feb hole must be flagged: {v}"

# 14. Bug 2 applies to ALL calendar bases (a perennial with a hole is still flagged)
assert harvest_hole_violations(_crop("perennial_evergreen", harvest="Sep - Oct, Dec - May")), \
    "Bug 2 is all-crops, not frost_anchored-only"


# ======================================================= BUG 2 -- 0 FALSE POS
# 15. a genuine TWO-CROP gap (arugula 'Apr - May, Nov - Jan') -> CLEAN (multi-month gaps are legal)
assert harvest_hole_violations(_crop(harvest="Apr - May, Nov - Jan")) == [], \
    "a multi-month two-crop harvest gap must NOT be bridged/flagged"

# 16. a single continuous span -> CLEAN
assert harvest_hole_violations(_crop(harvest="Mar - Jun")) == [], "a continuous span is clean"

# 17. year-round harvest -> CLEAN
assert harvest_hole_violations(_crop(harvest="Year round")) == [], "year-round harvest is clean"

# --- Bug-2 discriminator (2026-06-30 ruling): only WINTER/SHOULDER punch-outs between two
#     DISTINCT spans are bridged; summer heat gaps, single-span wrap-gaps, and heat_pause-adjacent
#     holes are legit and must NOT flag. ---

# 18. SUMMER hole (arugula northern 'Jun - Jul, Sep - Oct', Aug) -> CLEAN (real heat gap, two crops)
assert harvest_hole_violations(_crop(harvest="Jun - Jul, Sep - Oct")) == [], \
    "a Jun-Sep summer hole is a real heat gap between spring+fall crops, not a punch-out"

# 19. SINGLE-SPAN wrap-gap (hawaii 'Feb 15 - Dec 15', Jan) -> CLEAN (one span, not two; Jan is the
#     natural wrap-gap of a near-year-round window, not a hole punched BETWEEN two spans)
assert harvest_hole_violations(_crop(harvest="Feb 15 - Dec 15")) == [], \
    "a single-span near-year-round harvest's wrap-gap must NOT be bridged to year-round"

# 20. HEAT_PAUSE-adjacent shoulder hole -> CLEAN (a declared heat pause flanks the hole = real gap).
#     'Jan - Apr, Jun - Dec' has exactly one hole (May, a shoulder month inside Oct-May); heat_pause
#     on May marks it a real gap. Without the heat_pause it WOULD flag -> proves condition (3) is
#     what suppresses it (not the season rule).
assert harvest_hole_violations(_crop(harvest="Jan - Apr, Jun - Dec")), \
    "May punch-out (no heat_pause) must flag -- isolates condition (3)"
assert harvest_hole_violations(
    _crop(harvest="Jan - Apr, Jun - Dec", heat_pause_months=[5])) == [], \
    "the same May hole flanked by a declared heat_pause must NOT flag"

# 21. the WINTER punch-outs still FLAG (regression guard for the real bugs)
assert harvest_hole_violations(_crop(harvest="Sep - Oct, Dec - May")), "lettuce Nov must still flag"
assert harvest_hole_violations(_crop(harvest="Mar - May, Oct - Jan")), "kale Feb must still flag"
assert harvest_hole_violations(_crop(harvest="Feb - May, Dec")), "cabbage Jan (Dec|Feb-May) must still flag"


# ============================================ COMBINED A37 ENTRY POINT
# 18. a crop carrying BOTH bugs returns BOTH classes of violation
both = _crop(calendar=["harvest", "growing"] + [COLD] * 10, harvest="Sep - Oct, Dec - May")
v = calendar_coherence_violations(both)
assert any("growing" in m for m in v) and any("hole" in m.lower() for m in v), \
    f"the A37 entry point must return both Bug-1 and Bug-2 violations: {v}"

# 19. a fully clean crop -> no violations
clean = _crop(calendar=["plant", "growing", "harvest"] + [COLD] * 9, harvest="Mar")
assert calendar_coherence_violations(clean) == [], f"a clean crop must pass: {v}"

# herbaceous_perennial (asparagus) carve-out: the summer fern `growing` legitimately follows the
# spring spear `harvest` -- the frost_anchored analog of the evergreen "grows after harvest" exemption.
_hp = {"slug": "asparagus", "calendar_basis": "frost_anchored", "archetype": "herbaceous_perennial",
       "regions": {"northern_tier": {"resolved_by_zone": {"4": {"calendar":
           ["cold_pause","cold_pause","cold_pause","cold_pause","harvest","harvest",
            "growing","growing","growing","growing","cold_pause","cold_pause"]}}}}}
assert growing_reachability_violations(_hp) == [], growing_reachability_violations(_hp)
# REGRESSION: the same impossible growing-after-harvest on a NON-herbaceous_perennial frost_anchored
# crop STILL bounces.
_ann = dict(_hp, archetype="cool_season_annual")
assert growing_reachability_violations(_ann), growing_reachability_violations(_ann)


# ============================================ REAL DATA -- 0 FP on a known-legit pattern
# garlic's real cells overwinter (cold_pause -> growing); the gate must not false-flag them.
# (We deliberately do NOT assert 0 on the certified anchors here -- they currently CONTAIN the
#  bugs; the gate is correctly RED on canonical until the normalizer runs. That count is the
#  worklist, verified by the §8.1 diff, not a permanent unit-test assertion.)
import json
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    data = json.load(open(_path, encoding="utf-8"))
    crops = {c.get("slug"): c for c in data["crops"]}
    if "garlic" in crops:
        fp = growing_reachability_violations(crops["garlic"])
        assert fp == [], f"garlic (overwintering) must be 0-FP for Bug 1, got: {fp}"
        print(f"  real data: garlic overwintering 0-FP: PASS")

print("calendar_coherence_gate: all tests passed")
