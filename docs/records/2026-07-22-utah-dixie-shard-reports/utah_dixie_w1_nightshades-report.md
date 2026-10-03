# Utah Dixie shard report -- W1 nightshades (Task: warm Shape A, 11 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_w1_nightshades.json` (11 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status`).

## Crops authored (all Shape A: single spring window, `heat_pause` [7,8,9], no `second_planting`)
beefsteak-tomato, grape-tomato, heirloom-tomato, roma-tomato, bell-pepper, banana-pepper,
cayenne-pepper, habanero, jalapeno, eggplant, tomatillo.

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_w1_nightshades.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_w1_nightshades.json` -> **0 issue(s) across 11 cell(s)**

| slug | region_harness | notes |
|---|---|---|
| beefsteak-tomato | PASS | dtm 82, harvest Jun 22-30 (short ~1wk window, slowest tomato) |
| grape-tomato | PASS | dtm 70, harvest Jun 10-30 |
| heirloom-tomato | PASS | dtm 80, harvest Jun 20-30 |
| roma-tomato | PASS | dtm 75, harvest Jun 15-30 |
| bell-pepper | PASS | dtm 75, heat_threshold_f 90, harvest Jun 15-30 |
| banana-pepper | PASS | dtm 77, heat_threshold_f 90, harvest Jun 17-30 |
| cayenne-pepper | PASS | dtm 75, heat_threshold_f 95, harvest Jun 15-30 |
| habanero | PASS | dtm 95, heat_threshold_f 95, harvest Jul 5-25 -- see judgment call below |
| jalapeno | PASS | dtm 75, heat_threshold_f 90, harvest Jun 15-30 |
| eggplant | PASS | dtm 75, no heat_threshold_f in dataset (used general Solanaceae ceiling framing, matching Nevada donor's own eggplant text) |
| tomatillo | PASS | dtm 80, harvest Jun 20-30, two-plant pollination note carried into prose |

Every cell derived its `calendar` via `annual_calendar.derive_annual_calendar` and was inspected:
January `cold_pause`; Feb-Mar `indoors`; Apr `plant`; May (-Jun) `growing`; a `harvest` month where
the window lands before July; `heat_pause` Jul-Sep; Oct-Dec `cold_pause`. No phantom fall
plant/growing, matching the load-bearing "no warm-crop fall planting" rule.

## Structural approach
- Cloned the cherry-tomato template exactly: single zone "8", `plant_out` "Apr 1 - Apr 15" (offset
  +2d/window 14d off last_frost Mar 30), `start_indoors` "Feb 18 - Mar 4" (offset -40d/window 14d,
  ~6 weeks ahead), `resolved_from` {"last_frost":"Mar 30","first_frost":"Nov 1"}, `resolution_method
  "frost_anchored_resolved"`.
- `harvest_start` = Apr 1 + `days_to_maturity_mid` (from crops_data_final, `dtm_anchor
  from_transplant`), matching the exact convention the Nevada donor cells use (verified Nevada's own
  habanero harvest_start = Mar 25 + 95 days = Jun 28 to the day). `harvest_end` capped at Jun 30 for
  10 of 11 crops per the guide's "harvest_end by late June" instruction; habanero is the one
  exception (below).
- All 11 Nevada donor cells carry `heat_pause.months=[7,8,9]` (including eggplant), so all 11 utah
  cells keep that same shape -- no crop needed the "shorter/absent heat_pause" eggplant carve-out.
- Sources: every cell cites exactly `usu_ext_veg_dates` (windows) + `usu_ext_tomato` (heat threshold,
  extended by Solanaceae-family analogy to the peppers/eggplant/tomatillo, mirroring how the Nevada
  donor cells extend their own UNR tomato-family fact sheet to non-tomato crops) + `usu_ext_wash_frost`
  (frost anchor + 100 degF Jun-Aug fact). One id -> one URL per cell throughout (audit-clean).
- Per-crop heat_pause `basis_seasoned` names each crop's own `heat_threshold_f` where the dataset has
  one (90 for the sweet peppers, 95 for cayenne/habanero, 92 for the tomatoes), matching the Nevada
  donor's "this crop's own heat_threshold_f" convention; eggplant has no `heat_threshold_f` value in
  the dataset, so it uses the general 95 degF/50 degF ceiling framing by family analogy (same call the
  Nevada eggplant donor cell made).
- `notes`/`zone_notes`/`planting_note` left `null` on every cell, matching the cherry-tomato template
  exactly (the `planting_note` field is a categorical season-shape enum used elsewhere in the roster,
  e.g. `single_season`/`multi_season`; the template does not populate it for utah_dixie, so I did not
  invent a value).
- Dual-register `region_notes_beginner`/`region_notes_seasoned` are fully distinct per crop (not
  copied from cherry-tomato), covering DTM, harvest window, each crop's own heat threshold/use
  (slicer vs. paste vs. snack tomato; sweet vs. hot peppers; tomatillo's two-plant pollination need;
  eggplant's family-heat framing), the no-fall-crop rule, and the Nov 1 frost return.

## Judgment calls / concerns (flag for review)

1. **habanero -- compressed/marginal harvest, the one real finding of this batch.** Habanero has by
   far the longest `days_to_maturity_mid` of the 11 (95 days, vs. 70-82 for the rest). With the fixed
   USU Group D Apr 1 set-out date, `Apr 1 + 95 days = Jul 5` -- past the start of the Jul-Sep
   `heat_pause` window. I kept the harvest window honest (`harvest_start "Jul 5"`, `harvest_end "Jul
   25"`) rather than fabricating an earlier date to make it fit inside June like the other 10 crops.
   Because `derive_annual_calendar`'s precedence is `heat_pause > harvest`, the derived calendar for
   habanero shows **no `harvest` token at all** (`plant` in Apr, `growing` May-Jun, `heat_pause`
   Jul-Sep) -- the harvest window is real (and documented in the granular `harvest`/`harvest_start`/
   `harvest_end` display fields, same pattern Nevada's own habanero cell uses for its July portion),
   but the coarse 12-month calendar summary never surfaces a harvest month. This is gate-clean (no
   rule requires a `harvest` token to appear) but is a genuine content tension worth a second look:
   habanero may deserve either an explicit "marginal/optimistic pick" framing (which I added to both
   region_notes) or a content-team call on whether to exclude/flag it differently at the region level.
   I did not invent an earlier harvest date to paper over this -- the DTM math is what it is.
2. **tomatillo not explicitly named in USU's Table 1** (Group A-D lists tomato/pepper/eggplant/
   watermelon/cantaloupe/pumpkin/winter squash, not tomatillo). Treated by Solanaceae-family analogy
   to tomato (Group D, Apr 1), mirroring the exact analogy the Nevada donor cell already makes
   (Nevada's UNLV chart's "Tomato*" row explicitly covers tomatillo). Not flagged as a defect, just
   noting the analogy basis in case a reviewer wants a harder USU citation for tomatillo specifically.
3. **eggplant has no `heat_threshold_f` in the dataset.** Used the same general-ceiling framing the
   Nevada eggplant donor cell uses (citing the shared Solanaceae heat-abort logic rather than a
   crop-specific number).

No A9/second_planting concerns apply to this family (day-length gating is an allium-only field;
these are all Shape A single-spring warm crops with no `second_planting` key at all, matching the
load-bearing "no warm-crop fall planting" rule).
