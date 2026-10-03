# Utah Dixie shard report -- W3 quick warm crops (Task: warm Shape A, 8 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_w3_quick.json` (8 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status`).

## Crops authored (all Shape A: single spring window, `heat_pause` [7,8,9], no `second_planting`)
cucumber, slicing-cucumber, pickling-cucumber, english-cucumber, yellow-summer-squash,
zucchini-courgette, green-beans-bush, edamame.

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_w3_quick.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_w3_quick.json` -> **0 issue(s) across 8 cell(s)**

| slug | region_harness | notes |
|---|---|---|
| cucumber | PASS | dtm 58, harvest May 12-Jun 30 |
| slicing-cucumber | PASS | dtm 63, harvest May 17-Jun 30 (slowest cucumber type) |
| pickling-cucumber | PASS | dtm 53, harvest May 7-Jun 30 (fastest cucumber type) |
| english-cucumber | PASS | dtm 60, harvest May 14-Jun 30 |
| yellow-summer-squash | PASS | dtm 53, harvest May 7-Jun 30 |
| zucchini-courgette | PASS | dtm 55, harvest May 9-Jun 30 |
| green-beans-bush | PASS | dtm 55, harvest May 9-Jun 30 |
| edamame | PASS | dtm 85, harvest Jun 8-30 -- see judgment call below |

Every cell derived its `calendar` via `annual_calendar.derive_annual_calendar` and was inspected:
January/February `cold_pause`; March `plant`; April (-May for edamame) `growing`; May-June
`harvest` (June only for edamame); July-Sept `heat_pause`; Oct-Dec `cold_pause`. No phantom fall
plant/growing, matching the load-bearing "no warm-crop fall planting" rule.

## Structural approach
- Cloned the cherry-tomato template's schema exactly (single zone "8", `resolved_from`
  `{"last_frost":"Mar 30","first_frost":"Nov 1"}`, `resolution_method
  "frost_anchored_resolved"`, succession-level `anchoring_urls: {}` matching the template's own
  empty rollup), but used the **direct_sow** planting shape (no `start_indoors`, matching the
  Nevada donor's own direct-sow structure for these 8 crops -- these are Group C direct-sow
  crops, not Group D transplants).
- `plant_out` = "Mar 15 - Mar 29" (`first_plant_date` Mar 15, `last_plant_date` Mar 29), the USU
  Group C (Tender) St. George date, encoded as `offset_days: -15` / `window_days: 14` off
  `last_frost` (Mar 30) -- i.e. USU's explicit table date runs about two weeks *before* the
  average last frost, which the sources bible flags as expected ("St. George's row is ~2 weeks
  earlier than a naive derivation"), not a defect.
- `harvest_start` = March 15 + each crop's own `days_to_maturity_mid` (from
  `crops_data_final.json`, `dtm_anchor: from_sow` on all 8, matching the direct-sow anchor).
  `harvest_end` capped at a uniform "Jun 30" for all 8 (the same "harvest_end by late June"
  convention the W1 nightshade batch used), since all 8 are continuous/rolling-harvest crops
  (cucumbers, summer squash, bush beans, edamame all keep bearing right up to the July heat wall
  rather than a single clean cutoff), giving a real gap month before `heat_pause` begins in July.
- `heat_pause.months = [7, 8, 9]`, matching the template exactly.
- Sources: every cell cites **`usu_ext_veg_dates`** (the Group C window) + **`usu_ext_wash_frost`**
  (the frost anchor + the "100°F in June, July, August" regional heat fact). I deliberately did
  **not** cite `usu_ext_tomato` for this batch -- these are Cucurbitaceae/Fabaceae crops, not
  Solanaceae, and the task brief explicitly made `usu_ext_tomato` conditional on citing its
  specific >95°F flower-abort number; I judged that stretching a "Tomatoes in the Garden"
  citation across cucumbers/squash/beans/edamame by family analogy (the move the W1 nightshade
  batch made for genuine Solanaceae siblings) would be a real analogy stretch here, so the
  `heat_pause.basis_seasoned` instead names the crop's own heat-failure mechanism (bitter/
  unset fruit, dropped blossoms, aborting pods) as a mechanism claim backed by the general
  100°F regional fact, not a borrowed crop-specific threshold number. One id -> one URL per
  cell throughout (audit-clean).
- `planting_note`, `notes`, `zone_notes` left `null` on every cell, matching the cherry-tomato
  template.
- Added `successions_realized` (an existing crop-level `succession_policy` field, unrelated to
  the region's own second-planting question) to every z8 cell via
  `derive_realized_successions.derive_cell_realized`, required by gate A8 once a cell exists for
  a succession-scoped crop; all 8 of these crops carry `succession_policy.suitable=True`
  crop-wide, so the gate demands the field the moment a region cell exists. Values came out at
  1 (cucumber/slicing/english/yellow-summer-squash/zucchini) or 2 (pickling-cucumber,
  green-beans-bush, edamame) for the single 14-day March window, correctly small next to the
  crop-level cap of 12 realized in Nevada's much wider multi-month window -- the crop-level
  `succession_policy.successions`/`max_successions_per_season` (both 12, driven by the max
  across all of a crop's regions) were unaffected since utah_dixie's own realized count never
  exceeds the existing max.
- Dual-register `region_notes_beginner`/`region_notes_seasoned` are fully distinct per crop,
  covering DTM, harvest window, each crop's own use/type (all-purpose vs. slicing vs. pickling
  vs. English cucumber; yellow summer squash vs. zucchini; bush beans; edamame as a green
  soybean), the no-fall-crop rule, and the Nov 1 frost return. Crop names in prose follow the
  naming convention already established across the other regions' shards (e.g. "bush beans" not
  "green beans (bush)", "English cucumbers" capitalized, "zucchini" not "zucchini/courgette"),
  confirmed by grepping the existing mid_atlantic/mid_south/rgv/nevada donor prose for these
  same 8 slugs. Dates in prose use full month names ("June 8"), matching cherry-tomato's own
  prose convention, while the structured `resolved_by_zone` display fields keep the dataset's
  standard abbreviated "Mon D" form ("Jun 8").

## Judgment calls / concerns (flag for review)

1. **edamame -- the one real compressed-harvest finding of this batch, mirroring the W1
   habanero case.** Edamame has by far the longest `days_to_maturity_mid` of the 8 (85 days, vs.
   53-63 for the rest). With the fixed March 15 direct-sow date, `Mar 15 + 85 days = Jun 8`,
   leaving only a ~3-week harvest window (Jun 8-30) before the heat_pause. I kept this honest
   rather than inventing an earlier date. Unlike habanero (whose DTM pushed harvest past the
   heat_pause boundary entirely, suppressing the `harvest` calendar token), edamame's harvest
   still lands fully inside June, so the calendar shows a real (if short) `harvest` month. Still
   worth a second look: a genuinely narrow window for a crop USU itself does not list in Table 1
   for St. George timing specifics (edamame's Mar 15 date is inherited from the Group C "snap
   bean, dry bean" row by soybean-family/direct-sow-legume analogy, since USU's table does not
   name edamame specifically).
2. **The Mar 15-before-Mar-30-frost ordering is intentional, not a bug.** All 8 crops in this
   batch are frost-tender (`frost_tolerance_f: 32`), yet USU's own Group C St. George date (Mar
   15) precedes the average last frost (Mar 30) by about two weeks. The sources bible confirms
   this is the documented St. George reality (an explicit warm-adjusted local date, not a
   frost-relative derivation), so I followed the T1 source as given rather than second-guessing
   it or inventing a later date to "fix" the ordering.
3. **Dropping Nevada's second (fall) window was mechanically clean for all 8 crops** -- none of
   them needed special handling beyond deleting the second `plantings` succession and the
   `second_planting` block, and re-anchoring the single spring window to March 15/USU sourcing.
   The only real content-judgment work was in the `heat_pause.basis_seasoned` text (choosing to
   name each crop's own heat-failure mechanism rather than stretching a Solanaceae-specific USU
   citation across unrelated plant families) and the harvest_end cap choice (uniform Jun 30
   across a mix of rolling-harvest and shorter-window crops).

No A9/second_planting concerns apply to this family (day-length gating is an allium-only field;
these are all Shape A single-spring warm crops with no `second_planting` key at all, matching the
load-bearing "no warm-crop fall planting" rule).
