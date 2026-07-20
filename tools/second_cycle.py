#!/usr/bin/env python3
"""second_cycle.py -- deterministic fall-cycle (two-cycle) cell builder.

ADDENDUM to Task 2 of the 2026-07-20 Mid-Atlantic region arc (added after Task 3's sourcing
pass found a plan bug). Full detail: docs/reviews/notes/2026-07-20/mid_atlantic_sources.md
Section 8.

WHY THIS EXISTS: `annual_calendar.derive_annual_calendar` reads only the TOP-LEVEL
`plant_out` / `harvest` / `start_indoors` fields of a resolved cell -- it never reads
`second_planting`. A roster-wide check found all 272 existing `second_planting` cells have
a stored `calendar[]` that does NOT re-derive from their split storage form: the real
two-cycle calendars were built from COMBINED (comma-joined) windows, then the windows were
split into a single-span primary + a nested `second_planting` object by the 2026-07-09
de-mux migration (A43 forbids storing the comma shape -- see second_planting_gate.py).

~30 Mid-Atlantic warm-season crops need a fall cycle (VCE 426-331's documented fall windows
for tomato, beans, cucumbers, summer squash, etc.). Rather than have each authoring batch
hand-roll "build combined windows, derive, then split back apart," this helper does it
once, deterministically:

  1. Build a SCRATCH combined cell: `plant_out` = "<spring.plant_out>, <fall.plant_out>",
     `harvest` = "<spring.harvest>, <fall.harvest_start> - <fall.harvest_end>",
     `start_indoors` = both cycles' indoor spans comma-joined (only the cycles that have one).
     `annual_calendar.parse_months` handles the comma-joined form natively (verified:
     "Mar 25 - Apr 15, Jul 6 - Jul 20" -> months {3,4,7}), so `derive_annual_calendar` on
     this scratch cell renders BOTH cycles (spring plant/harvest, a growing lull, the fall
     plant/harvest, cold_pause winter).
  2. Split for STORAGE (A43): the returned cell carries `base` + `spring` fields VERBATIM at
     the top level (single-span primary -- what a resolved_by_zone cell normally looks like),
     `fall` verbatim as the nested `second_planting` object, and the calendar computed in
     step 1 (never a second, separately hand-authored calendar).

This mirrors the real, certified `cherry-tomato.regions.se_gulf.z8` cell's shape (see
docs/mid_atlantic_cell_contract.md Section 2.5, itself verified clean against
`annual_coherence_violations`, `annual_calendar_violations`, `heat_pause_backing_violations`,
and `second_planting_gate.check_crop`).

CALLER CONTRACT (the caller's job, not this helper's):
  - `spring`'s fields must be genuinely single-span (no commas) and internally consistent --
    in particular, `spring["harvest"]`'s display string must actually COVER
    `spring["harvest_end"]` (and `spring["plant_out"]` must cover `spring["last_plant_date"]`),
    matching every existing frost-anchored cell's convention. If it doesn't, A43's Rule A
    envelope-containment check (`second_planting_gate.check_crop`) will catch it downstream --
    this helper does not re-validate the caller's own window consistency, it only combines
    and splits deterministically.
  - `base["resolution_method"]` / `base["resolved_from"]` are also what the scratch combined
    cell derives its calendar against (frost-anchored regions gate cold_pause off real frost
    dates, but `derive_annual_calendar` itself only needs `calendar_basis`, so these two keys
    ride along for parity/documentation, not because the deriver reads them here).

Usage: from a Python authoring script (not a CLI) --
    from second_cycle import build_two_cycle_cell
    cell = build_two_cycle_cell(base, spring, fall)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from annual_calendar import derive_annual_calendar

# base-only fields that ride verbatim onto the result's top level if present.
_BASE_FIELDS = ("region_id", "region_label", "zone_span", "sources", "anchoring_urls",
                "region_notes_beginner", "region_notes_seasoned", "resolution_method",
                "resolved_from", "plantings")


def build_two_cycle_cell(base, spring, fall):
    """Combine a spring (primary) cycle + a fall (second_planting) cycle into one
    storage-shaped resolved_by_zone cell with a calendar[] that renders BOTH cycles.

    base: shared cell fields (region_id, region_label, zone_span, sources, anchoring_urls,
        region_notes_beginner, region_notes_seasoned, resolution_method, resolved_from,
        plantings if given) -- copied verbatim onto the result's top level.
    spring: the PRIMARY single-span cycle (plant_out, harvest, harvest_start, harvest_end,
        first_plant_date, last_plant_date, optional start_indoors) -- copied verbatim onto
        the result's top level (single-span primary, per A43).
    fall: the SECOND cycle (plant_out, harvest_start, harvest_end, optional start_indoors) --
        becomes the result's `second_planting` object, verbatim.

    Returns a new dict; does not mutate any of its arguments.
    """
    cell = {}
    for k in _BASE_FIELDS:
        if k in base:
            cell[k] = base[k]
    cell.update(spring)
    cell["second_planting"] = dict(fall)

    combined = {
        "plant_out": f"{spring['plant_out']}, {fall['plant_out']}",
        "harvest": f"{spring['harvest']}, {fall['harvest_start']} - {fall['harvest_end']}",
        "resolution_method": base.get("resolution_method"),
        "resolved_from": base.get("resolved_from"),
    }
    indoor_spans = [s for s in (spring.get("start_indoors"), fall.get("start_indoors")) if s]
    if indoor_spans:
        combined["start_indoors"] = ", ".join(indoor_spans)

    cell["calendar"] = derive_annual_calendar(combined, "frost_anchored")
    return cell
