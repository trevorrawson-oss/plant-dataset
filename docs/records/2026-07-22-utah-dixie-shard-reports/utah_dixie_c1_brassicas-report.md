# Utah Dixie shard report -- C1 brassicas/greens (Task: cool Shape E, 9 crops)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_c1_brassicas.json` (9 cells, single zone "8").
`crops_data_final.json` was not touched (read-only; confirmed via `git status -sb`, the file
does not appear as modified).

## Crops authored
arugula, bok-choy, broccoli, brussels-sprouts, cabbage, cauliflower, collards, kale, kohlrabi.

Spring set: Group A (Feb 15) for all 8 except cauliflower, which is USU's own Group B (Mar 1).
Two-window (spring + fall, built via `second_cycle.build_two_cycle_cell`): arugula, bok-choy,
broccoli, cabbage, cauliflower, collards, kale, kohlrabi. Spring-only, single planting, no
`second_planting`: brussels-sprouts (USU documents no St. George fall date for it).

## Self-gate results (iterated to clean; final state)
Every crop: `python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_c1_brassicas.json <slug>` -> **GATE: PASS**
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_c1_brassicas.json` -> **0 issue(s) across 9 cell(s)**

| slug | region_harness | fall window basis | heat_pause months |
|---|---|---|---|
| arugula | PASS | Heflebower analogy (quick greens ~Jul-Aug), `usu_ext_fall_veg` | [5,6] |
| bok-choy | PASS | Heflebower analogy (quick greens ~Jul-Aug), `usu_ext_fall_veg` | [5,6] |
| broccoli | PASS | Heflebower analogy (cole transplants ~Jul-early Aug), `usu_ext_fall_veg` | [5] |
| brussels-sprouts | PASS | none (spring-only, single planting) | [7,8] |
| cabbage | PASS | USU Group E dated "May 1-Jul 15", `usu_ext_veg_dates` (narrowed, see judgment call 1) | none needed |
| cauliflower | PASS | Heflebower analogy (cole transplants ~Jul-early Aug, same window as broccoli), `usu_ext_fall_veg` | [6] |
| collards | PASS | "like cabbage" per assignment, `usu_ext_fall_veg` | [5] |
| kale | PASS | USU Group E dated "Jul 1-Aug 15", `usu_ext_veg_dates` | [5,6] |
| kohlrabi | PASS | Heflebower analogy (quick greens ~Jul-Aug), `usu_ext_fall_veg` | [5] |

Every two-window cell was built with `second_cycle.build_two_cycle_cell` (combine-then-split,
A43-safe), then `calendar_coherence_gate.impossible_growing_months` identified the real summer
gap month(s), which were patched to `heat_pause` (sourced `usu_ext_wash_frost`, "100°F in
June, July, August"). Brussels-sprouts used a direct `derive_annual_calendar` call (single
cycle, no `second_planting`) with a hand-declared `heat_pause` (the deriver's precedence rules
handle a heat exclusion sitting inside a longer harvest display natively, no patch needed).
Every calendar was inspected: January `cold_pause` (or `indoors` where a spring indoor-start
genuinely begins in January -- broccoli/kohlrabi/brussels-sprouts); no phantom fall
plant/growing on the single-planting brussels-sprouts cell; Nov-Dec `cold_pause` on all 8
two-window crops; no impossible growing months remain (verified via
`calendar_coherence_gate.impossible_growing_months` returning empty after the patch pass).

## Bug found + fixed: false winter heat_pause on Jan-indoors crops
For broccoli and kohlrabi (the two crops whose spring `start_indoors` genuinely starts in
January), `derive_annual_calendar`'s cold_pause computation is skipped entirely once January is
active (`if 1 not in active` -- the "near-year-round" exemption), which left Nov/Dec as bare
`growing` after the fall harvest ended in October. `impossible_growing_months` correctly flags
those as unreachable (blocked by the preceding harvest), but blindly patching every flagged
month to `heat_pause` would have mislabeled real WINTER dead months as a heat exclusion --
exactly the false-positive class `build_mid_south_cells.py`'s `_fix_winter_growing` helper
exists to catch. I ported that fix (convert trailing `growing` after the season's last
plant/indoors/harvest token to `cold_pause`, non-wrapping) and ran it **before** reading
`impossible_growing_months`, so only the genuine mid-season summer gap (May, in both cases)
gets patched to `heat_pause`. Confirmed clean by re-running the gate suite (both crops PASS,
0 audit issues, and the final calendars show Nov/Dec `cold_pause` correctly).

## Judgment calls / concerns (flag for review)

1. **cabbage's USU Group E fall window ("May 1 - Jul 15") narrowed to its later half
   ("Jun 15 - Jul 15").** Cabbage's own spring set-out (Feb 15) plus its 85-day DTM pushes the
   spring harvest into May, which collides at calendar-month granularity with the literal start
   of USU's documented May-1 fall-planting window (the deriver reads `plant_out`/`harvest`
   month-by-month, not day-by-day, so any fall plant_out touching May would silently overwrite
   the spring May harvest with a `plant` token). I used the later half of USU's own documented
   range (mid-June to mid-July) so the fall cycle starts cleanly after the spring harvest ends,
   still within the USU-cited window and still citing `usu_ext_veg_dates`. Net finding: with
   this window, cabbage needs **no heat_pause at all** -- June/July become `plant` (fall) instead
   of an idle gap, and August is a legitimate growing-toward-harvest month -- a genuine content
   delta from the Nevada donor (which carries `heat_pause=[6,7]`), because USU's own dated
   window is wider than Nevada's UNLV chart. Collards ("like cabbage" per the assignment) uses
   the same mid-June to mid-July window but DOES get one heat_pause month (May), since its
   faster 65-day DTM finishes the spring harvest in April, a month earlier than cabbage.
2. **brussels-sprouts harvest display ("Jun 5 - Dec 31") spans across its own declared
   heat_pause (months 7,8).** Because `derive_annual_calendar` gives heat_pause precedence over
   harvest, June shows `harvest` (first sprouts, before the heat hits), July-August show
   `heat_pause`, and September-December show `harvest` again (the stalk resumes sizing sprouts
   as it cools, sprouts sweetening after light frost). This is a single-planting, long-season
   crop with an interrupted-but-resumed harvest, not the habanero-style "harvest window entirely
   swallowed by heat_pause" case from the W1 nightshades batch. USU documents no St. George fall
   planting date for Brussels sprouts, so per the assignment it stays spring-only.
3. **Group A/B point dates rendered as 14-day windows** ("Feb 15 - Mar 1", "Mar 1 - Mar 15",
   etc.), mirroring the cherry-tomato template's own convention of extending USU's single
   planting date forward into a short practical window, rather than storing a bare point date.
4. No A9/second_planting concerns: A9 photoperiod window-fit is allium-only and does not apply
   to this family. `second_planting_gate` (A43, "de-mux violations") reported 0 for every crop;
   every two-window cell is single-span in `plant_out`/`harvest`/`start_indoors` at the primary
   level with `second_planting` carrying the fall cycle, and `harvest_end`/`last_plant_date` sit
   inside their own primary windows by construction.
5. `successions_realized` was computed via `derive_realized_successions.derive_cell_realized`
   (not hand-set) once the gate flagged a stale hardcoded value; note this deriver only reads
   the primary (spring) `first_plant_date`/`last_plant_date` span, so the reported count (1 or 2)
   reflects spring-window succession-sowing room only, not the fall cycle -- this matches the
   existing roster-wide convention (confirmed against `build_mid_south_cells.py`'s identical
   usage), not a defect specific to this shard.
