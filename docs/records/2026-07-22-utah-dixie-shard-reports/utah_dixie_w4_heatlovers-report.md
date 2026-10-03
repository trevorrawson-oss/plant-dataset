# Utah Dixie shard report -- W4 heat-lovers (Task: warm Shape C, 8 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_w4_heatlovers.json` (8 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status`).

## Crops authored (all Shape C: single long heat-lover planting, NO `heat_pause`, no `second_planting`)
okra, sweet-potato, dry-bean, pole-beans, sweet-corn, field-corn, flint-corn, popcorn.

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_w4_heatlovers.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_w4_heatlovers.json` -> **0 issue(s) across 8 cell(s)**

| slug | region_harness | notes |
|---|---|---|
| okra | PASS | dtm 57 (from_sow), biology-authored (not in USU Table 1), plant Apr 1-May 15, harvest May 28-Oct 27 |
| sweet-potato | PASS | dtm 110 (from_planting/slips), biology-authored (not in USU Table 1), plant Apr 16-May 31, harvest Aug 4-Oct 27 |
| dry-bean | PASS | dtm 95, Group C Mar 15, plant Mar 15-Apr 5, harvest Jun 18-Jul 23 |
| pole-beans | PASS | dtm 65 (bearing habit), Group C Mar 15, harvest May 19-Jul 23 (~9.3wk bearing run) |
| sweet-corn | PASS | dtm 75, Group C Mar 15, harvest May 29-Jun 29; carries `successions_realized: 2` (the only succession-suitable crop in this family) |
| field-corn | PASS | dtm 110, Group C Mar 15, harvest Jul 3-Aug 7 (dry-down) |
| flint-corn | PASS | dtm 100, Group C Mar 15, harvest Jun 23-Jul 28 (dry-down) |
| popcorn | PASS | dtm 100, Group C Mar 15, harvest Jun 23-Jul 28 (dry-down + cure) |

Every cell derived its `calendar` via `annual_calendar.derive_annual_calendar` and was inspected:
January `cold_pause`; Mar/Apr `plant`; a `growing` gap where DTM outruns the plant window's end;
`harvest` months land honestly per each crop's own DTM math; Nov-Dec `cold_pause` (frost Nov 1).
No `heat_pause` token on any of the 8 cells; no phantom fall `plant`/`growing`, matching the
load-bearing "no warm-crop fall replant" rule (none of these 8 carry a `second_planting` key at all).

## Adversarial self-check (RED before GREEN)
Before trusting the clean run, I injected two defect classes into scratch copies (never touching
the real shard) and confirmed both bounce:
1. A stray `--`/em-dash in `okra.region_notes_beginner` -> `region_harness`'s C/D dash gate fired
   (`VIOLATION: dash: regions.utah_dixie.region_notes_beginner...`).
2. A phantom `heat_pause` injected onto `dry-bean`'s zone-8 cell -> `region_harness`'s A5 annual
   calendar coherence gate fired (`calendar heat_pause [] != heat_pause.months [7, 8]...`).
Both defects are caught, confirming the gates are load-bearing, not vacuously passing.

## Structural approach
- Group C (dry-bean, pole-beans, sweet-corn, field-corn, flint-corn, popcorn): USU Extension's
  "Suggested Vegetable Planting Dates for Utah" places all six in Group C (Tender), St. George date
  about **March 15**. Modeled as `plant_out` offset -15d/window 21d off `last_frost` (Mar 30) ->
  **Mar 15 - Apr 5**, mirroring the W1 batch's exact offset-from-frost convention. `harvest_start` =
  first-sown date + the crop's own `days_to_maturity_mid`; `harvest_end` = last-sown date + DTM +
  a margin (14 days for the four dry-down crops matching the Nevada donor's own dry-bean formula
  verified against its printed dates; 10 days for sweet-corn's shorter fresh-eating picking window;
  65 days of progressive bearing for pole-beans, matching the Nevada donor's own bearing-length
  convention). All six land well before the Nov 1 frost.
- okra + sweet-potato: **not in USU Table 1**, flagged honestly in both `plantings_provenance`-style
  synthesis notes and consumer prose. Authored from heat-lover biology per the task brief: direct-sow
  (no `start_indoors`, matching every other region's okra/sweet-potato cells in the canonical dataset)
  once soil is reliably warm, `Apr 1 - May 15` for okra (offset +2d/window 44d off last_frost) and the
  later `Apr 16 - May 31` for sweet-potato (offset +17d/window 45d, since slips need warmer soil than
  okra needs, mirroring the Nevada donor's own okra-before-sweet-potato start-date stagger).
  `harvest_end` for both = `first_frost` -5 days (continuous harvest to near frost), cloned from the
  Nevada donor cell's own convention for these two crops.
- Sources: every Group C cell cites only `usu_ext_veg_dates` (the Group C date); okra/sweet-potato
  cite only `usu_ext_wash_frost` (frost anchor + the "100°F in June-August" heat-lover-biology basis),
  since neither has a USU planting-date citation to make. One id -> one URL per cell throughout
  (audit-clean).
- `notes`/`zone_notes`/`planting_note` left `null` on every cell (matching the template). Dual-register
  `region_notes_beginner`/`region_notes_seasoned` are fully distinct per crop, covering each crop's own
  DTM, harvest shape (continuous pick vs. dry-down vs. bearing-habit), isolation-distance notes for the
  three dry-corn types, and the no-fall-crop rule.

## Judgment calls / concerns (flag for review)

1. **NO `heat_pause` on any of these 6 dry-bean/corn cells, even though `low_desert_az` (Phoenix,
   hotter) carries a real `heat_pause` for dry-bean/pole-beans/sweet-corn/field-corn/flint-corn/
   popcorn** (sourced to University of Arizona AZ1005 + a UNL corn-pollination fact sheet). I followed
   the bible's explicit Shape C instruction ("NO `heat_pause`") over the AZ analog: St. George (USU's
   own Group C guidance) documents no heat-abort mechanism for these crops, unlike Phoenix's more
   extreme summer. This also matches 5 of 6 Nevada donor cells directly (dry-bean/pole-beans/
   field-corn/flint-corn/popcorn carry no `heat_pause` in Nevada either).
2. **sweet-corn: dropped the Nevada donor's `heat_pause` + `second_planting` two-cycle structure.**
   Nevada's UNLV chart gives sweet corn a spring-plus-fall succession with a Jul heat_pause; USU
   documents no fall corn planting for St. George at all, so per the load-bearing "no warm-crop fall
   replant" rule I built sweet-corn identically to field-corn/flint-corn/popcorn (single Group C Mar 15
   planting), just with sweet corn's own 75-day fresh-eating DTM instead of a dry-down harvest. This is
   the one crop in the family where the Nevada donor's shape had to be structurally overridden rather
   than lightly re-windowed.
3. **sweet-corn is the only crop in this family carrying `successions_realized`** (A8 gate requirement):
   its `succession_policy.suitable == True` (a real 2-week staggered-block succession crop), unlike the
   other 7's `suitable == False` (single full-season plantings). Computed via
   `derive_realized_successions.derive_cell_realized` against the authored Mar 15-Apr 5 window -> `2`.
4. **okra/sweet-potato honesty flag (the two biology-authored crops).** Both explicitly state in
   `region_notes_seasoned` that they sit outside USU's Table 1 and that the window is authored from
   heat-lover biology plus the region's frost normals, not a cited USU planting date. This is the
   weakest-sourced pair in the shard; a content reviewer may want a harder Utah-specific citation for
   either crop if one surfaces later (none was found in the sourcing bible's registered USU sub-ids).
5. **No A9/second_planting concerns apply to this family**: day-length gating is allium-only, and none
   of the 8 cells carry a `second_planting` key at all (single-spring Shape C, per the load-bearing
   no-warm-crop-fall-replant rule).
