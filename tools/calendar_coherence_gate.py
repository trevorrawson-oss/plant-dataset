#!/usr/bin/env python3
"""Calendar-COHERENCE gate -- the missing calendar-LOGIC invariant (whole_crop_gate A37).

The gate suite proved calendar STRUCTURE (length-12, token enum, heat_pause alignment -- A5;
pause-on-active-window placement -- A24) but never that the 12-token sequence is temporally
COHERENT. Two impossible patterns shipped in certified anchors + the live 13, caught by Trevor
eyeballing rendered ca_interior guides (2026-06-30). Spec: docs/calendar-coherence-fix-design-
2026-06-30.md; bug report: docs/calendar-coherence-bugs-2026-06-30.md.

  Bug 1 -- "growing after harvest" (frost_anchored only). A `growing` token must be reachable
    from a `plant`/`indoors` without first passing a crop-REMOVED state. Walking backward
    (wrap-aware) from a `growing`:
      - WALK_THROUGH = {growing, cold_pause, heat_pause, wait}: the plant is still in the ground
        or dormant -- garlic overwinters (plant -> cold_pause -> growing is LEGIT), an
        indeterminate resumes after a heat pause. Keep walking.
      - LEGIT = {plant, indoors}: the growing is reachable -> clean.
      - BLOCKER = {harvest, season_over}: the crop was removed / the cycle ended -> the growing
        is impossible (nothing planted before it).
    If neither a LEGIT nor a BLOCKER is reached in 12 steps (a pure walk-through calendar, e.g.
    year-round 12x`growing`), it is NOT a growing-after-harvest defect -> clean. No-op for non-
    frost_anchored crops (an evergreen perennial legitimately grows after harvest).

  Bug 2 -- "one-month harvest hole" (ALL crops). A single non-harvest month sandwiched between
    two harvest months in the parsed `harvest` DISPLAY window is a punched-out hole in a
    continuous producing span. Multi-month gaps (two discrete plantings) stay legal. A crop whose
    genuine biology is staggered/discrete ripening is the documented carve-out (none in the
    current 49 -- log it rather than bridge if one ever appears).

This is a PRESENCE/COHERENCE check on the shipped tokens/windows, not a re-derivation: ~60% of
annual calendars are legitimately hand-authored multi-cycle shapes the deriver can't reproduce
(that is exactly why a full re-derive was rejected -- see the spec). No-op semantics keep it 0-FP
on the legit patterns (garlic overwintering, winter-wrapping, year-round, perennials, two-crop
gaps); it is RED on canonical until the normalizer runs (gate-as-worklist).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annual_calendar import parse_months, declared_heat_months

_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Bug-1 backward-walk classes.
_LEGIT = {"plant", "indoors"}                       # the growing is reachable
_BLOCKER = {"harvest", "season_over"}               # crop removed / cycle ended
# everything else (growing, cold_pause, heat_pause, wait, and any unknown token) is walk-through:
# the plant is still present/dormant, so keep walking back.

# Bug-2 bridge/flag window: only WINTER/SHOULDER punch-outs are rounding artifacts in a continuous
# producing span. A Jun-Sep hole is a real summer heat gap between a spring and a fall crop (the
# cool crops mark it plant/growing, not heat_pause, so season is the only signal) -- a legit
# two-crop structure, not a punch-out (Trevor + prior-session ruling, 2026-06-30).
_WINTER_SHOULDER = {1, 2, 3, 4, 5, 10, 11, 12}      # Oct..May (bridge); Jun..Sep is the heat window

# Bug-1 near-year-round exemption: a cell whose harvest window covers >= this many months is a
# CONTINUOUS producer (e.g. hawaii zucchini/cucumber 'Feb 15 - Dec 15', 11 mo). Its interspersed
# `growing` tokens are the tropical production lull, not the growing-after-harvest bug -- the annual
# analog of the perennial-evergreen exemption. Threshold isolates exactly those cells (next-highest
# real bug is 8-month coverage; clean gap). Ruling 2026-06-30 (extends the hawaii Bug-2 "leave").
_CONTINUOUS_HARVEST_MONTHS = 10


def _cells(crop):
    """Yield (loc, cell) for every resolved_by_zone cell."""
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in ((r or {}).get("resolved_by_zone") or {}).items():
            yield f"{rk}.z{z}", cell


def _leads_to_harvest(cal, i):
    """True if walking FORWARD from i through {growing, heat_pause} reaches a `harvest` before any
    plant/indoors/off-season token -- i.e. the growing is part of a producing arc heading into a
    harvest (a fall crop whose `plant` token is masked by heat_pause, e.g. beefsteak se_gulf z8)."""
    f = (i + 1) % 12
    for _ in range(12):
        t = cal[f]
        if t == "harvest":
            return True
        if t in ("growing", "heat_pause"):
            f = (f + 1) % 12
            continue
        return False                                # plant/indoors/cold_pause/season_over/wait
    return False


def impossible_growing_months(cell):
    """The shared Bug-1 detector (used by the gate AND the normalizer, so they target the same
    months). Returns a list of (month_index_0based, blocker_token) for each `growing` token not
    reachable from a plant/indoors without passing a harvest/season_over. Empty if the cell has no
    12-token calendar or is a near-year-round continuous producer (>=10-month harvest -> exempt).

    EXEMPT (not impossible): an OUT-OF-harvest-window `growing` that leads FORWARD into a harvest --
    it is growing TOWARD that harvest (a producing arc), not growing after a finished crop. An
    IN-window growing is still flagged (it should render as `harvest`, not `growing`)."""
    cal = cell.get("calendar")
    if not isinstance(cal, list) or len(cal) != 12:
        return []                                   # length/shape is A5's job
    H = parse_months(cell.get("harvest") or "")
    if len(H) >= _CONTINUOUS_HARVEST_MONTHS:
        return []                                   # near-year-round continuous producer -> exempt
    out = []
    for i in range(12):
        if cal[i] != "growing":
            continue
        if (i + 1) not in H and _leads_to_harvest(cal, i):
            continue                                # out-of-window growing-toward-harvest -> legit
        b = (i - 1) % 12
        for _ in range(12):
            t = cal[b]
            if t in _LEGIT:
                break                               # reachable -> clean
            if t in _BLOCKER:
                out.append((i, t))                  # growing after a crop-removed state
                break
            b = (b - 1) % 12                         # walk-through -> keep going
    return out


def growing_reachability_violations(crop):
    """Bug 1 (frost_anchored only). One violation per impossible growing-month. No-op off
    frost_anchored (an evergreen perennial legitimately grows after harvest)."""
    if crop.get("calendar_basis") != "frost_anchored":
        return []
    out = []
    for loc, cell in _cells(crop):
        for i, blk in impossible_growing_months(cell):
            out.append(f"{loc} {_MON[i]}: `growing` is not reachable from a plant/indoors "
                       f"(traces back to `{blk}` -- nothing is planted before it)")
    return out


def _harvest_pieces(hs):
    """The harvest display string split into its comma/semicolon spans, each as a month-set.
    Used to tell a punch-out BETWEEN two spans from the wrap-gap of ONE near-year-round span."""
    return [parse_months(p) for p in hs.replace(";", ",").split(",") if p.strip()]


def bridgeable_holes(cell):
    """The shared Bug-2 detector (used by the gate AND the normalizer). Returns the 1-indexed hole
    months to bridge. A hole `m` qualifies iff ALL:
      (1) m-1 and m+1 fall in DIFFERENT harvest spans -- a real punch-out between two windows, not
          the wrap-gap of a single near-year-round span (e.g. 'Feb 15 - Dec 15' leaves Jan alone);
      (2) m is in Oct..May -- a Jun..Sep hole is a real summer heat gap between a spring and a fall
          crop (a legit two-crop structure), not a rounding artifact;
      (3) neither m nor a flanking month is a declared heat_pause -- a heat pause abutting the hole
          marks a real gap.
    Multi-month gaps (two discrete plantings) never qualify (only single-month holes are checked)."""
    hs = cell.get("harvest")
    if not isinstance(hs, str):
        return []
    H = parse_months(hs)
    if not H:
        return []
    pieces = _harvest_pieces(hs)
    declared = declared_heat_months(cell)
    out = []
    for m in range(1, 13):
        prev_m = (m - 2) % 12 + 1
        next_m = m % 12 + 1
        if not (m not in H and prev_m in H and next_m in H):
            continue
        p_prev = {i for i, s in enumerate(pieces) if prev_m in s}
        p_next = {i for i, s in enumerate(pieces) if next_m in s}
        if p_prev & p_next:                          # (1) same span wraps around m -> not a punch-out
            continue
        if m not in _WINTER_SHOULDER:                # (2) Jun-Sep is a real heat gap
            continue
        if {prev_m, m, next_m} & declared:           # (3) heat_pause flanks the hole -> real gap
            continue
        out.append(m)
    return out


def harvest_hole_violations(crop):
    """Bug 2 (all crops). One violation per bridgeable single-month harvest hole."""
    out = []
    for loc, cell in _cells(crop):
        hs = cell.get("harvest")
        for m in bridgeable_holes(cell):
            out.append(f"{loc} {_MON[m - 1]}: one-month harvest hole in the harvest window "
                       f"{hs!r} (a single month punched out of a continuous producing span)")
    return out


def calendar_coherence_violations(crop):
    """A37 entry point -- both invariants (Bug 1 frost_anchored + Bug 2 all crops)."""
    return growing_reachability_violations(crop) + harvest_hole_violations(crop)


if __name__ == "__main__":
    import json
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    b1 = b2 = 0
    for c in data["crops"]:
        for v in growing_reachability_violations(c):
            print(f"  [bug1] {c.get('slug')}: {v}")
            b1 += 1
        for v in harvest_hole_violations(c):
            print(f"  [bug2] {c.get('slug')}: {v}")
            b2 += 1
    print(f"calendar_coherence gate: {b1} growing-after-harvest + {b2} harvest-hole "
          f"= {b1 + b2} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if (b1 + b2) else 0)
