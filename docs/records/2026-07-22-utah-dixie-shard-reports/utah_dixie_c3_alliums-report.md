# Utah Dixie shard report -- C3 cool legumes + alliums (9 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_c3_alliums.json` (9 cells, single zone "8").
`crops_data_final.json` was not touched (read-only; confirmed via `git status -sb`, no
modification shown for it).

## Crops authored
Cool legumes (Shape E, spring-only): broad-beans-fava, snow-peas, sugar-snap-peas.
Alliums (Shape F): chives, garlic, onion, shallot, spring-onion. Plus leek (long-season
cool crop, two-cycle, follows the Nevada donor's structure).

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_c3_alliums.json <slug>` -> **GATE: PASS** (all 9)
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_c3_alliums.json` -> **0 issue(s) across 9 cell(s)**

| slug | region_harness | notes |
|---|---|---|
| broad-beans-fava | PASS | Group A analogy (Feb 15), dtm 90, spring-only, heat_pause [6,7,8,9] |
| snow-peas | PASS | Group A (Feb 15, "peas" line), dtm 62, spring-only, `successions_realized`=2 |
| sugar-snap-peas | PASS | Group A (Feb 15), dtm 64, spring-only, `successions_realized`=2 |
| chives | PASS | no USU table line, modeled by analogy; `plantings_provenance` disclosed |
| garlic | PASS | fall clove Sep 20-Oct 25, hand-authored winter-wrapping calendar |
| onion | PASS | **A9 photoperiod violations: 0** -- see below |
| shallot | PASS | **A9 photoperiod violations: 0** -- follows onion |
| spring-onion | PASS | two-window (spring+fall), `successions_realized`=2, no day-length gating |
| leek | PASS | no USU table line; two-cycle mirrors the Nevada donor structurally |

**onion/shallot A9 = 0** -- confirmed explicitly: `python3 tools/region_harness.py utah_dixie 8 ... onion` and `... shallot` both print `gating_factors=['photoperiod'] | photoperiod violations: 0`, and the window-fit sub-check (which forbids any April-August month in `plant_out` for `intermediate_day`) passes because `plant_out` is `"Sep 26 - Oct 5"` for both -- fully outside the forbidden band.

## Structural approach

**Cool legumes (broad-beans-fava, snow-peas, sugar-snap-peas):** all three direct-sown at
USU's St. George Group A (hardy) date, Feb 15 (the same table line "peas" occupies), window
Feb 15 - Mar 1. Harvest computed from each crop's own `days_to_maturity_mid` off that window.
Ran through `annual_calendar.derive_annual_calendar` directly (no hand-authoring needed, no
winter-wrap). Declared `heat_pause.months=[6,7,8,9]` (Jun stays literally sourced from "100°F
in June, July, and August"; Sep added by the same one-month climate-continuation judgment the
sibling W1-nightshades shard already made for this region, needed so the deriver's
frost-anchored cold-walk doesn't mislabel a still-hot St. George September as `cold_pause`).
No `second_planting` on any of the three -- see the judgment call below.

**Chives:** no dedicated USU table line, so timing is modeled from its own cool-hardy
perennial envelope at the Group A slot (matches the Nevada donor's own no-table-line
handling), disclosed via `plantings_provenance`. Single spring establishment + `heat_pause`
[6,7,8,9], run through the mechanical deriver.

**Garlic:** single fall clove window (`usu_ext_garlic`, "late September to November"),
narrowed to Sep 20 - Oct 25. Harvest Jun 5 - Jul 15 ("when tops begin to yellow"). Calendar is
**hand-authored, not run through `derive_annual_calendar`** -- see the finding below.

**Onion + shallot:** fall-set for storage, `recommended_day_length_type="intermediate_day"`.
USU's Group E date "onion Aug 1-10" is read as the seed-start/set-sourcing point
(`start_indoors`); the actual outdoor `plant_out` (what A9 checks) is set about 8 weeks later,
Sep 26 - Oct 5, deliberately inside the A9-legal fall/winter/early-spring band. Harvest Jun 1 -
Jun 20 next summer. No spring bulb set authored. Hand-authored calendar (same winter-wrap
reason as garlic). Shallot mirrors onion's dates and cites exactly, per "shallot follows
onion."

**Spring-onion:** two-window (Heflebower: "planted spring or fall... do not take long to
mature"), built with `second_cycle.build_two_cycle_cell` + `impossible_growing_months` per the
guide's recipe: spring Feb 15 - Mar 1 (harvest Apr 16-30), fall Aug 1-20 (harvest Sep 30-Oct
19). No day-length gating (harvested green). `successions_realized`=2 (required once I hit A8;
see finding below).

**Leek:** no USU table line at all (absent from Groups A-D and the Group E fall list), so
authored by analogy to onion's Group A timing and structured on the Nevada donor's own
two-cycle shape (spring stand pushed out by summer heat + a frost-hardy fall-transplanted
stand standing through winter), disclosed via `plantings_provenance`. Hand-authored calendar
token sequence directly mirrors Nevada zone8's pattern (Jan=harvest, Feb-Mar=plant,
Apr-Jun=harvest, Jul-Aug=heat_pause, Sep-Oct=plant, Nov=growing, Dec=harvest), re-dated to
USU's frost anchor.

## Findings / judgment calls (flag for review)

1. **Cool legumes are spring-only -- a real tension between the task brief and the bible,
   resolved toward the bible.** The task brief's general fallback said "no USU fall date ->
   spring-only UNLESS the Nevada donor carries a backed fall/two-window (then mirror)," and
   Nevada's own snow-peas/sugar-snap-peas/fava cells DO carry two windows. But both the shard
   guide's per-class map and `utah_dixie_sources.md` (the bible) explicitly and by name rule
   "peas (snow/sugar-snap/fava)" into the **spring-only** list (USU's Group E fall-harvest table
   lists only beets, cabbage, kale, lettuce, onion, spinach, turnip -- no peas). I followed the
   bible's specific, source-grounded ruling over the brief's generic fallback clause, per
   "T1-sourced-or-it-doesn't-ship": there is no USU citation for a St. George fall pea planting,
   so authoring one would be a fabricated window. Flagging this explicitly in case the
   reconciliation should go the other way.

2. **Garlic/onion/shallot calendars are hand-authored, not run through
   `derive_annual_calendar`.** I tested the mechanical deriver against these fall-planted,
   next-summer-harvest cells and it produces `cold_pause` for the entire winter growing period
   (Dec-May) -- wrong, since these alliums are genuinely growing through the mild St. George
   winter, not paused. `annual_calendar.py`'s own docstring flags this exact gap ("winter-
   wrapping harvest... need a cycle-segmentation extension -- NOT basil"). I instead cloned the
   Nevada donor's own hand-authored token pattern (`growing` through winter, `harvest`,
   `season_over` for the empty-bed gap, `plant`/`indoors` at the real action months) and
   re-dated it to USU's frost anchor -- exactly what the shard guide's opening line asks for
   ("clone Nevada cells and re-window to USU"). Verified clean against both
   `annual_coherence_violations`-style checks (via the harness) and `region_cell_audit`'s
   in-ground/`season_over` defect check.

3. **Onion/shallot plant_out timing diverges from a literal reading of the bible's "Aug 1-10"
   date, deliberately, to satisfy the load-bearing A9 gate.** The bible names "Group E onion
   Aug 1-Aug 10" as "the fall set date" and separately says plant_out runs "~Aug-Oct" -- but
   photoperiod_gate.py's window-fit rule hard-forbids any `intermediate_day` cell from having
   an April-through-August month anywhere in `plant_out`. Setting `plant_out` in August would
   have failed A9. I resolved this by reading Aug 1-10 as the seed-start/set-sourcing date
   (`start_indoors`) and placing the actual outdoor transplant (`plant_out`) about 8 weeks
   later, Sep 26 - Oct 5, safely inside the legal band. This is the one interpretive choice most
   worth a second look from whoever wrote the bible passage.

4. **`successions_realized` was required and initially missing** on snow-peas, sugar-snap-peas,
   and spring-onion (all three have `succession_policy.suitable=True`; A8 requires the field
   and checks it against `derive_realized_successions.derive_cell_realized`). Computed via that
   function against each cell's own `first_plant_date`/`last_plant_date`/`calendar` (2-week
   interval, 14-day spring window -> 2 realized sowings each); confirmed the field is scoped to
   the top-level/primary window only, not the fall `second_planting` window (matches Nevada's
   own stored values, verified by re-running the deriver against Nevada's actual snow-peas
   cell). broad-beans-fava, chives, garlic, onion, shallot, leek all have
   `succession_policy.suitable=False`, so the field does not apply to them.

5. **Fava beans and leek are not named in USU's Table 1 at all** (only "peas" and, for leek,
   no analog whatsoever). Both are handled by disclosed analogy (a `notes` field for fava, a
   `plantings_provenance` field for leek and chives), never presented as a direct USU citation
   they don't have.

No other concerns. All 9 cells cite only `usu_ext_*` sub-ids from the region's registered
catalog (no Nevada/warm_arid ids carried over), no em dashes in consumer copy, `°F` glyph
throughout, no build-word leaks in `region_notes_*`.
