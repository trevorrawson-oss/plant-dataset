# Utah Dixie shard report -- W2 cucurbits (Task: warm Shape C, 7 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_w2_cucurbits.json` (7 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status`). No commit made.

## Crops authored (all Shape C: single spring window, NO `heat_pause`, NO `second_planting`)
cantaloupe, honeydew-melon, watermelon, pumpkin, acorn-squash, butternut-squash, spaghetti-squash.

## Self-gate results -- 7/7 GATE PASS, audit 0
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_w2_cucurbits.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_w2_cucurbits.json` -> **0 issue(s) across 7 cell(s)**

| slug | region_harness | dtm (from_sow) | harvest window |
|---|---|---|---|
| cantaloupe | PASS | 82 | Jun 22 - Oct 22 |
| honeydew-melon | PASS | 92 | Jul 2 - Oct 22 |
| watermelon | PASS | 85 | Jun 25 - Oct 22 |
| pumpkin | PASS | 100 | Jul 10 - Oct 25 |
| acorn-squash | PASS | 85 | Jun 25 - Oct 25 |
| butternut-squash | PASS | 100 | Jul 10 - Oct 25 |
| spaghetti-squash | PASS | 95 | Jul 5 - Oct 25 |

Every cell's `calendar` was derived via `annual_calendar.derive_annual_calendar` and inspected: Jan-Mar
`cold_pause`, Apr `plant`, May (and Jun for the 100+/95-day crops) `growing`, a multi-month `harvest`
block landing in summer through late October, Nov-Dec `cold_pause`. No `heat_pause` token anywhere
(confirmed: none of the 7 Nevada donor cells for these crops carry a `heat_pause` key either -- all
seven grow through the Las Vegas summer the same way). No phantom fall plant/growing.

## Structural approach
- Confirmed via the Nevada donor (`tools/staging/nevada_annuals_warm.json`) that all 7 crops carry
  `dtm_anchor="from_sow"` (direct-sown, no transplant) and NO `start_indoors`, NO `heat_pause`, NO
  `second_planting` in their Nevada cells -- so the Utah cells mirror that: direct-sown, no
  `start_indoors` (field present as `null` in `resolved_by_zone["8"]`, matching schema), no `heat_pause`
  key at all.
- `plant_out` = USU Group D "Very Tender" St. George date, April 1, modeled as a narrow "Apr 1 - Apr 15"
  window (offset +2 / window 14 off `last_frost` Mar 30), exactly cloning the cherry-tomato template's
  own `plant_out` anchoring (the same Group D date all warm Group D crops share).
- `harvest_start` = April 1 + each crop's own `days_to_maturity_mid` (from `crops_data_final.json`,
  exact day arithmetic, matching the w1 shard's confirmed-working convention of anchoring straight off
  April 1 rather than off the cherry-tomato template's own slightly-off displayed date).
- `harvest_end`: since Shape C carries no heat abort, harvest was NOT capped in June. Anchored instead to
  `first_frost` (Nov 1) with a negative offset: -10 days for the three melons (cantaloupe/honeydew/
  watermelon, mirroring the Nevada donor's own -10 convention for these crops), -7 days for pumpkin and
  the three winter squash (mirroring Nevada donor's own -7 convention). This produces the "harvest summer
  into fall, then cold_pause" shape the guide specifies for Shape C, honestly reflecting that these vines
  keep setting and finishing fruit through the desert's hottest months rather than aborting, right up to
  the frost margin.
- Sources: every cell cites `usu_ext_veg_dates` (the Group D planting date) + `usu_ext_wash_frost` (the
  frost anchor Mar 30/Nov 1, and the "100°F in June-August" fact used in prose to explain, by contrast,
  why these crops carry NO heat_pause where the Shape A nightshades do). `usu_ext_tomato` was NOT cited
  (no heat-abort claim is made for this family). One id -> one URL per cell throughout (audit-clean).
- `notes`/`zone_notes`/`planting_note` left `null` on every cell, matching the template.
- Dual-register `region_notes_beginner`/`region_notes_seasoned` are fully distinct per crop: each covers
  the crop's own DTM, its ripeness cue (stem-slip for cantaloupe, rind-color/blossom-give for honeydew,
  thump/ground-spot for watermelon, hardened-rind/dry-stem for pumpkin, cure-for-storage framing for
  acorn, matte-tan-rind for butternut, solid-pale-yellow for spaghetti squash), the no-heat-pause
  through-summer contrast with the region's heat-abort crops, and the Nov 1 frost return. USU is named
  where a window comes from it.

## Judgment calls / concerns (flag for review)
1. **Harvest-end anchoring choice (melon -10d vs. squash/pumpkin -7d).** USU's Suggested Vegetable
   Planting Dates page gives only the Group D START date (Apr 1), not an explicit harvest-window END
   date for any of these crops -- there is no USU source for exactly how late St. George gardeners keep
   picking. I anchored `harvest_end` to `first_frost` using the same per-crop offsets the Nevada donor
   cells already use for these same 7 crops (a reasonable, non-fabricated inference: same desert biology,
   same "keeps producing until frost" shape, just re-anchored to Utah's Nov 1 frost instead of Nevada's
   Nov 8), and named it honestly in `harvest_end`'s `synthesis_note_seasoned` as inference from the
   crop's own frost-driven-cutoff biology rather than a distinct USU-dated claim. Not flagged as a defect,
   but a reviewer may want to sanity-check the exact -7/-10 day margins.
2. **pumpkin Halloween framing.** Pumpkin's math (Apr 1 + 100 days = Jul 10 first harvest, running to
   Oct 25) happens to land right at a Halloween-appropriate finish. I noted this in prose as an observed
   natural fit of the date math, not as a separately-sourced USU claim -- USU does not mention Halloween
   timing for St. George.
3. No A9/second_planting concerns apply to this family (day-length gating is allium-only; all 7 are
   Shape C single-spring crops with no `second_planting` key, matching the load-bearing "no warm-crop
   fall replant" rule -- confirmed by the Nevada donor cells' own absence of `second_planting`).
