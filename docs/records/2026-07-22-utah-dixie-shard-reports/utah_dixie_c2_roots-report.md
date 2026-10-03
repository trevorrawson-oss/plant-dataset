# Utah Dixie shard report -- C2 cool roots/leafy (Task: 10 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_c2_roots.json` (10 cells, single zone "8").
`crops_data_final.json` was not touched (read-only; no writes made to it).

## Crops authored
beet, carrot, celery, lettuce-leaf, parsnip, potato, radish, spinach, swiss-chard, turnip.

- **Two-window (Shape E, spring + fall via `second_cycle.build_two_cycle_cell`):** beet,
  carrot, lettuce-leaf, spinach, turnip.
- **Spring-only:** celery, parsnip, potato, radish, swiss-chard.

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_c2_roots.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_c2_roots.json` -> **0 issue(s) across 10 cell(s)**

| slug | region_harness | spring window (Group) | fall window | heat_pause months |
|---|---|---|---|---|
| beet | PASS | Mar 1-15 (B) | Jul 1-Aug 1 | [6] |
| carrot | PASS | Mar 1-15 (B) | Jul 1-Aug 1 (analogy) | [6] |
| celery | PASS | Mar 1-11 (B, analogy) | none | [7,8,9] |
| lettuce-leaf | PASS | Mar 1-15 (B) | Jun 1-Aug 1 | [5] |
| parsnip | PASS | Mar 1-Apr 12 (B) | none (fall dig) | [6,7,8,9] |
| potato | PASS | Mar 1-22 (B) | none | [7,8,9] |
| radish | PASS | Feb 15-Mar 17 (A) | none | [5,6,7,8,9] |
| spinach | PASS | Feb 15-Mar 1 (A) | Jul 1-Aug 15 | [5,6] |
| swiss-chard | PASS | Mar 1-Apr 14 (B) | none | [7,8,9] |
| turnip | PASS | Feb 15-Mar 1 (A) | Jul 1-Aug 1 | [5,6] |

Every cell's `calendar` was DERIVED (`annual_calendar.derive_annual_calendar`, or
`second_cycle.build_two_cycle_cell` + `calendar_coherence_gate.impossible_growing_months`
for the two-window crops, exactly per the shard guide's recipe) and inspected: January
`cold_pause`; no phantom fall plant/growing after summer; the declared `heat_pause` months
match the rendered tokens exactly; Nov-Dec anchor to the Mar 30/Nov 1 frost dates.

## Structural approach
- All 10 cells: `region_id="utah_dixie"`, `zone_span=["8"]`,
  `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`,
  `resolution_method="frost_anchored_resolved"`. Cited ids only from the 8 registered USU
  sub-ids; never a Nevada (`unlv_*`/`unr_*`) or `warm_arid` id (grepped the finished shard
  for stray ids/build words -- 0 hits).
- **Spring Group dates** (from the bible's Table 1): Group A (Feb 15) for radish, turnip,
  spinach; Group B (Mar 1) for beet, carrot, lettuce-leaf, swiss chard, potato, parsnip.
  Celery is not in Table 1 at all -- treated by family analogy to its fellow cool-season
  Group B umbellifers parsley/parsnip (flagged below).
- **Window length is shape-dependent, not uniform.** Two-window crops (which connect into a
  real fall cycle) use a narrow 14-day spring window, matching the cherry-tomato/w1
  template convention, so a genuine heat gap survives between the spring harvest and the
  fall sowing. Spring-only crops use a wider Nevada-donor-length window (30-45 days,
  cloned from the Nevada donor's own window_days per crop) so the bed stays honestly
  active across a real succession-sowing stretch instead of leaving a false idle
  "growing" gap. This is a genuine, deliberate STRUCTURAL delta from a single uniform
  window rule, driven by inspecting each crop's derived calendar rather than assumed.
- **Fall windows** (Group E "Special Plants for Fall Harvest," `usu_ext_veg_dates`): beet
  Jul 1-Aug 1, turnip Jul 1-Aug 1, spinach Jul 1-Aug 15, lettuce-leaf Jun 1-Aug 1 (a full
  month earlier than the others -- taken verbatim from the table, not smoothed to match its
  siblings). Carrot is NOT in the Group E table; its Jul 1-Aug 1 fall window is authored by
  the bible's own explicit Heflebower analogy ("carrots direct-seed ~Jul, like beet/turnip"),
  cited to `usu_ext_fall_veg` instead of `usu_ext_veg_dates`.
- **Fall `harvest_end` extension past frost:** beet/carrot/turnip cite Heflebower's specific
  line ("turnips, carrots and beets can be left in the ground quite late into winter",
  `usu_ext_fall_veg`) to extend to `first_frost + ~17-20 days`. Lettuce-leaf/spinach extend
  more modestly (`first_frost + 16-18 days`) on general cold-tolerance biology, cited only to
  `usu_ext_wash_frost` (the frost-date source) since Heflebower's specific "held late" line
  does not name them.
- **`heat_pause` months are DERIVED, not asserted**, via
  `impossible_growing_months`/`build_two_cycle_cell` for the two-window crops: beet/carrot
  get a single-month June gap (their spring harvest finishes by mid/late May and the fall
  window opens Jul 1); lettuce-leaf gets only May (its Group E fall window opens a month
  early, Jun 1); spinach/turnip get May+June (two months). For the five spring-only crops,
  heat_pause is the post-harvest Jul-Sep bucket (matching the cherry-tomato/w1 precedent),
  widened to May-Sep for radish only (forced by A37, see below).
- `notes`/`zone_notes` populated with light agronomic tips (succession cadence, fresh
  parsnip seed, hotbed-start celery, seed-potato hilling) in fresh prose, not copied from any
  donor. `successions_realized` added to every succession-scoped cell (beet, carrot,
  lettuce-leaf, spinach, turnip, celery, radish) via
  `derive_realized_successions.derive_cell_realized`, matching each crop's real
  `succession_policy.interval_weeks`; swiss-chard/potato/parsnip are `suitable:false` in
  `succession_policy` (out of scope, correctly carry no field).

## Judgment calls / concerns (flag for review)

1. **Radish and Swiss chard ruled SPRING-ONLY, not two-window**, despite Nevada's own donor
   cells carrying a fall cycle for both. The task brief said "follow the Nevada donor -- if
   it has a backed fall/two-window, mirror it; else spring-only," but the shard bible is more
   specific and I followed it instead: it explicitly lists both "radish-as-fall only if the
   shard finds support (Heflebower... gives no fall date)" and "chard unless justified" in
   its no-USU-fall-window bucket. USU's Group E table does not list radish or Swiss chard,
   and Heflebower's fall-guidance prose (`usu_ext_fall_veg`) never names either crop (only
   cole crops, carrots, and the beet/turnip/carrot "held late" line) -- Heflebower does call
   radish seed "large and easy" but gives no date. I did not find independent support to
   justify a fall window for either, so both stay spring-only, and I said so directly in
   radish's own `region_notes_seasoned` (a transparency move, not just a silent omission).
2. **Radish's `heat_pause` had to be widened from [7,8,9] to [5,6,7,8,9], a real content
   fix, not a style choice.** With the narrower window, radish's very short DTM (26 days)
   meant harvest finished in April, leaving May-June as a `growing` token with nothing
   actually growing (a stale bed). `whole_crop_gate`'s A37 calendar-coherence check flagged
   this directly ("`growing` is not reachable from a plant/indoors -- traces back to
   `harvest`"), so I extended heat_pause to cover the true idle stretch and reworded its
   `basis_seasoned` to explain the bed rests "from May through the hottest months" rather
   than overclaiming a specific 100°F date for May itself (only Jun/Jul/Aug are the
   USU-sourced 100°F months; May's inclusion is framed as the lead-up, not asserted as
   independently 100°F-sourced).
3. **Celery's calendar was hand-touched (Oct/Nov `growing` -> `cold_pause`) after
   derivation.** `derive_annual_calendar`'s cold-walk anchors backward from January and
   stops at the first active month it hits; celery's Dec `start_indoors` (for the *next*
   cycle) sits right before January, so the algorithm's backward walk never reaches back
   through Oct/Nov to mark them cold, leaving them as a phantom `growing` filler (nothing is
   actually happening in a spring-only, no-fall-replant crop in October or November). This
   is the same defect class flagged for radish, just not caught by A37 in celery's case
   (probably because celery's own harvest sits earlier in the reachability walk); I fixed it
   proactively for consistency and content honesty. This is an explicit, legitimate
   hand-touch of a derived calendar (the guide's own recipe permits `growing`-gap patches;
   `annual_coherence_violations`'s docstring explicitly allows hand-authored calendars for
   complex cells) -- flagging it here per the report instructions rather than hiding it.
4. **Celery has no explicit USU Table 1 listing.** Treated by family analogy to Group B
   (parsley and parsnip, its fellow cool-season umbellifers), matching the guide's own
   precedent for treating tomatillo by Solanaceae-family analogy in the sibling w1 shard.
   Flagged in both `region_notes_seasoned` prose and here for a content reviewer.
5. **Carrot's fall window is a documented analogy, not a Group E table entry** -- USU's
   dated fall table does not include carrot, so its Jul 1-Aug 1 fall window and its
   "held into winter" extension both cite `usu_ext_fall_veg` (Heflebower) rather than
   `usu_ext_veg_dates`. This is exactly the analogy the task brief and bible both call for,
   surfaced here for visibility, not silently folded in as if it were table-dated like
   beet/turnip/spinach/lettuce.
6. **Turnip's fall `harvest_end` deliberately overrides the Nevada donor's own
   crop-specific claim.** Nevada's turnip cell says turnip "hold their quality best when dug
   close to frost rather than left long afterward" (harvest_end = first_frost - 1 day).
   Utah's own source (Heflebower) explicitly groups turnip with carrot and beet as roots
   that "can be left in the ground quite late into winter," which is the opposite framing.
   I followed Utah's own T1 source over the Nevada structural donor's crop-specific claim
   (per the guide: read Nevada donors for STRUCTURE only, never carry a Nevada fact
   forward when Utah's own source says something different) -- extended turnip's fall
   `harvest_end` to `first_frost + 20 days`, same as beet.

No A9 photoperiod-gating or `second_planting` A43-envelope issues apply to this family
(day-length gating is allium-only; all five two-window cells passed `region_harness` and
`region_cell_audit` cleanly with `second_planting` as a single nested span, primary-cycle
`harvest_end`/`last_plant_date` staying inside the spring window in every case).
