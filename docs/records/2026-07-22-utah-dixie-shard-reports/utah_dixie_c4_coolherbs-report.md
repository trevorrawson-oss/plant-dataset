# Utah Dixie shard report -- C4 cool herbs + annual flowers (Task: cool two-window family, 8 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_c4_coolherbs.json` (8 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status --short`).

## Crops authored
borage, calendula, cilantro-coriander, dill, parsley, sweet-alyssum, sweet-pea, viola.

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_c4_coolherbs.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_c4_coolherbs.json` -> **0 issue(s) across 8 cell(s)**

| slug | region_harness | shape |
|---|---|---|
| borage | PASS | 2-window (spring Feb15 Group-A-analog + fall Aug1, heat_pause Jun-Jul) |
| calendula | PASS | 2-window (spring Feb15 Group-A-analog + fall Aug1, heat_pause Jun-Jul) |
| cilantro-coriander | PASS | 2-window (spring Feb15 Group-A-analog + fall Aug1, heat_pause Jun-Jul) |
| dill | PASS | 2-window (spring Feb15 Group-A-analog + fall Aug1, heat_pause Jun-Jul) |
| parsley | PASS | 2-window (spring Mar1 explicit Group B + fall Aug1, heat_pause Jul only) |
| sweet-alyssum | PASS | single fall-anchored continuous bloom (Sep1-Dec1 plant, no second_planting, heat_pause Jun-Aug) |
| sweet-pea | PASS | single fall-anchored continuous bloom (Sep24-Nov1 plant, no second_planting, heat_pause Jun-Aug) |
| viola | PASS | single fall-anchored continuous bloom (Sep1-Dec1 plant, no second_planting, heat_pause Jun-Aug) |

## Structural approach
- Read each crop's Nevada donor (`nevada_annuals_cool.json`) first. Two donor shapes actually appear in
  that file, not one: borage/calendula/cilantro/dill/parsley are genuine **spring + fall two-window**
  crops (comma-joined `plant_out` in the Nevada donor), while sweet-alyssum/viola/sweet-pea are a
  **single fall-anchored continuous-bloom** crop (one fall `plant_out`, harvest wraps straight through
  winter into spring, no separate spring sowing, no `second_planting`). Cloned each crop's own donor
  shape, per the task instruction, rather than forcing all 8 into one template.
- Two-window crops built with `tools/second_cycle.build_two_cycle_cell` (spring primary + fall
  `second_planting`), then `calendar` re-derived after attaching the sourced `heat_pause` object.
  Single-window crops built directly (matching the nasturtium/`utah_dixie_w5_warmherbs.json` pattern) --
  `derive_annual_calendar` run straight on the cell.
- **Spring window placement (2-window crops):** parsley is one of USU's own named Table 1 rows (Group B,
  Semi-Hardy, Mar 1) -- used verbatim. Borage, calendula, cilantro, dill are **not** in USU's Table 1 at
  all (it is a vegetable table); placed at the Group A (Hardy, Feb 15) date by frost-tolerance analogy
  (`frost_tolerance_f` 25-28°F for all four, comparable to Group A's spinach/peas), flagged as an analogy
  in each `synthesis_note_seasoned`, matching the honesty convention `utah_dixie_w5_warmherbs.json`
  already used for basil/nasturtium's own "not itemized in Table 1" spring placement.
- **Fall window (2-window crops):** none of these 5 are on USU's dated Group E fall list either (that
  list is beets/cabbage/kale/lettuce/onion/spinach/turnip only). Authored a uniform Aug 1-15 fall sowing
  by analogy to USU's general "Fall Gardening in the St. George Area" (Heflebower) guidance for
  restarting cool-season crops in late summer, flagged the same way. Fall `harvest_end` = first frost
  minus 3 days (Oct 29) for the four frost-tender herbs/flowers; parsley's fall stand is instead carried
  through winter to Feb 28, sourced to its own dataset `frost_tolerance_f` of 10°F (it does not die back
  at typical St. George winter lows) -- this also closes an `impossible_growing_months` gap that a Jan
  15 cutoff left in February (see Judgment calls).
- **heat_pause months, backed and internally coherent, not copy-pasted from Nevada:** every cell cites
  only `usu_ext_wash_frost`'s "100°F in June, July, and August" fact (never Nevada's `unr_fs0261`
  90°F-ceiling number, which cannot travel into a utah_dixie cell). Borage/calendula/dill get `[6,7]`
  (2 months) so August is free for their Aug 1 fall sowing; cilantro gets `[6,7]` too (its own
  `heat_threshold_f`=75°F is the lowest of the set, named in its own basis text); parsley gets `[7]` only,
  reflecting its dataset `heat_threshold_f`=None + "does not bolt in its first year" biology (matches the
  Nevada donor's own 1-month-only parsley heat_pause). The 3 single-window flowers get `[6,7,8]`
  (Jun-Aug) uniformly, chosen so August/September stay free for their Sep-planted fall window.
- **Dates for the 3 single-window flowers** were re-derived from Utah's own frost anchor (Mar 30/Nov 1)
  using the SAME relative day-offsets the Nevada z8 donor cells show from their own frost anchor (Mar
  15/Nov 8) -- e.g. sweet-alyssum/viola plant_out = first_frost -61d to +30d = "Sep 1 - Dec 1"; harvest_end
  = last_frost +38d = "May 7". Sweet-pea's plant window was nudged from the donor-proportional Sep 24
  start (see Judgment calls) to keep the calendar internally coherent -- the content (fall-only, no
  summer, no second sowing) is unchanged from the donor.
- Every calendar was DERIVED (`annual_calendar.derive_annual_calendar`), never hand-authored, and
  inspected via `calendar_coherence_gate.impossible_growing_months` before finalizing (see below).
- `successions_realized` added to every z8 cell via `tools/derive_realized_successions.derive_cell_realized`
  (all 8 crops carry `succession_policy.suitable=true` in the real canonical, so this is gate-required,
  A8). Verified each crop's computed value sits at or below its existing crop-level
  `succession_policy.successions` cap (borage 1<=9, calendula 1<=12, cilantro 2<=12, dill 2<=12,
  parsley 1<=9, sweet-alyssum 5<=11, viola 5<=11, sweet-pea 2<=3) -- none needed (or could get, being
  read-only) a crop-level cap bump.
- Sources: 2-window crops cite `usu_ext_veg_dates` + `usu_ext_wash_frost` (spring) and `usu_ext_fall_veg`
  + `usu_ext_wash_frost` (fall); the 3 single-window flowers cite only `usu_ext_wash_frost` (frost anchor
  + heat basis), since neither USU vegetable-dates page describes their fall-bedding-flower pattern.
  Never carried a Nevada id (`unr_fs0261`, `unlv_mg_svn`) into any cell -- confirmed by grep.
- Dual-register `region_notes_beginner`/`region_notes_seasoned` are fully distinct per crop (DTM, bolt/
  heat behavior, frost tolerance, edible-flower/companion notes, sweet-pea's seed/pod toxicity warning).
  No em dashes (grepped 0 hits), degF glyph used throughout (`°F`, grepped, no "N degrees" form), no
  build-word leaks (grepped for "shard", "Shape A/D/E", "delta 4", "second_cycle", Nevada source ids --
  none found).

## Judgment calls / concerns (flag for review)
1. **Borage/calendula/cilantro/dill's Group A (Feb 15) spring placement is an analogy, not a USU Table 1
   citation** -- these 4 are not vegetables, so USU's own table has no row for them. Placed by
   frost-tolerance comparison to Group A's cold-hardy crops. Flagged in-prose on every cell; a content
   reviewer may want a harder USU ornamental/herb-specific citation if one exists.
2. **All 5 two-window crops' fall Aug 1-15 sowing is authored by analogy to Heflebower's general
   fall-gardening guidance**, not a dated Table-1/Group-E entry (none of these 5 are on that list either).
   Same honesty caveat as #1, worded into each fall `synthesis_note_seasoned`.
3. **Parsley's fall harvest_end was moved from an initial Jan 15 draft to Feb 28.** The Jan 15 draft left
   a lone, incoherent "growing" token in February (nothing planted, nothing harvested, flagged by
   `impossible_growing_months`). Extending the fall harvest to Feb 28 -- honestly, since parsley's own
   10°F frost tolerance supports it -- closes the gap cleanly and keeps the calendar internally coherent
   without inventing a spring gap that isn't there.
4. **Sweet-pea's fall plant_out window start was moved from a donor-proportional Sep 24 to accommodate
   internal coherence, then moved BACK to Sep 24** once the actual conflict was found to be a real
   calendar-coherence bug (a bare September "growing" island with no backing plant/harvest either side),
   not a heat_pause conflict as first assumed -- the fix was widening `plant_out` to include September
   (matching the donor's own proportional timing) rather than narrowing it. Final window: "Sep 24 - Nov
   1", ending exactly at the average first frost, mirroring the Nevada z8 donor's own plant_out-ends-at-
   first-frost relationship.
5. **The two Nevada donor shapes were not what I originally assumed.** Borage/calendula looked, on a
   first read, like they might share sweet-alyssum/viola/sweet-pea's continuous fall-through-spring
   shape; the Nevada JSON's actual comma-joined `plant_out` values ("Feb 22 - Apr 22, Aug 8 - Oct 8")
   confirm they are real two-window (spring+fall) crops instead, matching cilantro/dill/parsley
   structurally. Re-derived from the literal donor JSON, not a paraphrase, to avoid this misread landing
   in the shard.

No A9/photoperiod concerns (day-length gating is allium-only; none of these 8 are alliums). No
warm-crop-fall-replant rule applies (all 8 are cool-season; the load-bearing "no warm-crop fall
planting" rule is scoped to Shapes A/C/D).
