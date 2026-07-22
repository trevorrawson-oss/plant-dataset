# Utah "Dixie" region -- authoring shard guide (read this first)

You author `regions.utah_dixie` cells for a subset of crops in `~/plant-dataset`. This is a roster-wide
region column. Your output is a set of cells written to ONE shard file; the controller merges + commits.
**DO NOT git commit. DO NOT touch crops_data_final.json (READ-ONLY). Write ONLY your shard file under
`tools/staging/shards/`.** Utah is Nevada's near-twin, so you clone Nevada cells and re-window to USU.

## Read these first (in order)
1. `docs/reviews/notes/2026-07-22/utah_dixie_sources.md` -- THE BIBLE: frost anchor, USU Group dates,
   the per-class shape+window map, the deltas, and the source-id map (which USU sub-id to cite per claim).
2. `tools/staging/utah_dixie_annuals_warm.json` -> the `cherry-tomato` cell = the gate-PASSED **Shape A
   worked template** (exact schema, single zone, USU sub-id sourcing, derived calendar). CLONE its shape.
3. For EACH crop, read its **Nevada donor cell** (the structural donor -- same desert shape) and its
   `warm_arid`/`low_desert_az` cell (prose voice, biology):
   - Nevada: `python3 -c "import json;d=json.load(open('tools/staging/nevada_annuals_warm.json'));import json as j;print(j.dumps(d.get('<slug>'),ensure_ascii=False)[:1800])"` (or nevada_annuals_cool/trees/citrus/perennials.json)
   - biology: `python3 -c "import json;d=json.load(open('crops_data_final.json'));c=[x for x in d['crops'] if x['slug']=='<slug>'][0];print('wi',c.get('weeks_indoors'),'dtm',c.get('days_to_maturity_mid'),'anchor',c.get('dtm_anchor'),'frost_tol',c.get('frost_tolerance_f'))"`

## Cell schema (every cell) -- SINGLE ZONE
`region_id="utah_dixie"`, `region_label="Utah: St. George Dixie (Mojave-edge high desert)"`,
`zone_span=["8"]`, `sources=[...the usu sub-ids this cell cites...]`, `plantings=[...]`,
`plantings_provenance=null`, `resolved_by_zone={"8":{...}}` (EXACTLY the one key "8"),
`region_notes_beginner`, `region_notes_seasoned`. The `resolved_by_zone["8"]`: `plant_out`,
`start_indoors` (if tray-started), `harvest`, `harvest_start`, `harvest_end`, `first_plant_date`,
`last_plant_date`, `notes`/`zone_notes`/`planting_note` (null unless authored), `sources`,
`anchoring_urls`, `resolution_method="frost_anchored_resolved"`,
`resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1"}`, `heat_pause` (if the shape has one),
and `calendar` (12 tokens, DERIVED).

## USU St. George planting dates (from the bible)
Group A (hardy) Feb 15; Group B (semi-hardy) Mar 1; Group C (tender) Mar 15; Group D (very tender) Apr 1.
For transplanted crops, `start_indoors` ~6 weeks before `plant_out`. **NO early-Feb workaround needed**
(Apr 1 plant + late-Feb indoors leaves January inactive -> honest `cold_pause` renders on its own).

## Deriving calendar[]
```python
import sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell_z = {...your resolved_by_zone["8"]...}   # must include resolved_from (+ heat_pause if the shape has one)
cell_z["calendar"] = derive_annual_calendar(cell_z)
```
INSPECT every calendar: January `cold_pause`; no phantom fall `plant`/`growing` after summer on Shape
A/C; Nov-Dec `cold_pause` (frost Nov 1). A declared `heat_pause` month MUST show as `heat_pause` in the
calendar (or a backed action token); no `heat_pause` token outside the declared months.

## Shape rules (your dispatch names your shape)
- **A (warm heat-abort: tomatoes/peppers/eggplant/tomatillo; also the heat-sensitive quick crops
  cucumber/summer-squash/bush-bean/edamame):** ONE spring succession, NO second_planting. Group D crops
  plant ~Apr 1 (start_indoors late Feb); Group C quick crops direct-sow ~Mar 15. `heat_pause.months`
  typically **[7,8,9]** (June is the spring harvest; July-Sept is the >95degF abort). Cite
  `usu_ext_veg_dates` (windows) + `usu_ext_tomato` (heat) + `usu_ext_wash_frost` (frost/100degF).
  cherry-tomato is the exact template -- clone + adjust DTM.
- **C (long-season heat-lover: melons/winter-squash/pumpkin/okra/sweet-potato/dry-bean/pole-bean/
  sweet-corn/field-corn/flint-corn/popcorn):** ONE long planting (Group C Mar 15 or Group D Apr 1),
  grows THROUGH the heat -> **NO heat_pause** (check the crop's low_desert_az/nevada cell: it carries
  none). Harvest summer into fall, then cold_pause. okra/sweet-potato are NOT in USU Table 1 -> author
  from heat-lover biology (they thrive in the St. George summer), flag it. Cite `usu_ext_veg_dates`.
- **D (warm herb/flower: basil/lemongrass/cosmos/marigold/nasturtium/sunflower/zinnia):** single
  warm-season planting, grow through summer, cold_pause. Usually NO heat_pause (basil/lemongrass love
  heat); nasturtium may fade in peak heat (light heat_pause ok if the analog has one). Cite
  `usu_ext_veg_dates`.
- **E (cool two-window: brassicas/roots/greens/cool-legumes/cool-herbs/cool-flowers/potato):** spring
  (Group A Feb 15 or B Mar 1) + a FALL window **ONLY where USU documents one** (see the bible's fall
  set). Build the two-window with `second_cycle` (recipe below). Fall-window set (Group E dated):
  beets, cabbage, kale, lettuce, spinach, turnip (+ broccoli/cauliflower/carrot by Heflebower analogy,
  cite `usu_ext_fall_veg`). Cool crops with NO USU fall window -> **spring-only** (peas, Brussels
  sprouts, parsnip, potato, chard unless justified). Cite `usu_ext_veg_dates` (+ `usu_ext_fall_veg`).
- **F (fall-planted allium: garlic/onion/shallot):** garlic single FALL clove window **late Sep-Nov**
  (USU "Garlic in the Garden", cite `usu_ext_garlic`), harvest early-mid summer. onion (bulb)
  FALL-planted for storage (Heflebower, cite `usu_ext_fall_veg`), `recommended_day_length_type
  ="intermediate_day"`, harvest next summer -> NO spring bulb set -> **A9 must be 0** (no April+
  plant_out). shallot "follows onion." spring-onion (green) two-window (spring or fall, Heflebower).

## LOAD-BEARING: no warm-crop fall replant
USU documents fall planting ONLY for cool crops. So ALL warm crops (Shapes A/C/D) are **SINGLE spring,
NO second_planting** (delta 4a; do NOT author a Nevada-style quick-crop summer replant -- USU has none).

## TWO-WINDOW recipe (Shape E) -- second_cycle drops heat_pause, you must patch it
```python
import sys; sys.path.insert(0,'tools')
from second_cycle import build_two_cycle_cell
from calendar_coherence_gate import impossible_growing_months
cell = build_two_cycle_cell(base, spring, fall)          # base carries resolved_from Mar30/Nov1
bad = impossible_growing_months(cell)                    # summer gap months
for m,_ in bad: cell["calendar"][m] = "heat_pause"
cell["heat_pause"] = {"months":[m+1 for m,_ in bad], "classification":"heat_pause",
  "basis_seasoned":"St. George summers reach 100 degF in June, July, and August, so cool crops pause "
                   "in the summer heat between the spring and fall windows (USU Extension).",
  "sources":["usu_ext_wash_frost"], "anchoring_urls":{"usu_ext_wash_frost":{"url":"https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf","verified":"2026-07-22"}}}
```
Cap the spring `harvest_end` at a fixed pre-heat date so a real gap MONTH exists before the fall sow
(parse_months ignores day-of-month). Read `second_cycle.build_two_cycle_cell` docstring. A43 envelope:
`second_planting` single-span; `harvest_end`/`last_plant_date` inside the FIRST windows.

## Sourcing (T1-or-it-does-not-ship) -- the id -> URL map
Cite ONLY these usu sub-ids (verified "2026-07-22"). A cell's `sources` = the ids it cites; each id's
URL goes in `anchoring_urls`. **One id -> one URL per cell (never two URLs for one id).**
- `usu_ext_veg_dates` -> https://extension.usu.edu/yardandgarden/research/suggested-vegetable-planting-dates-for-utah
- `usu_ext_tomato` -> https://extension.usu.edu/yardandgarden/research/tomatoes-in-the-garden
- `usu_ext_wash_fruits` -> https://extension.usu.edu/washington/gardening/fruits/
- `usu_ext_raspberry` -> https://extension.usu.edu/yardandgarden/research/raspberry-management-for-utah
- `usu_ext_garlic` -> https://extension.usu.edu/yardandgarden/research/garlic-in-the-garden
- `usu_ext_fall_veg` -> https://extension.usu.edu/washington/files/Fall_Vegetable.pdf
- `usu_ext_wash_frost` -> https://extension.usu.edu/washington/files/2020_Frost_dates_and_elevation.pdf
- `usu_ext_peaches` -> https://extension.usu.edu/yardandgarden/research/peaches-in-the-garden
NEVER carry a Nevada id (unr_*/unlv_*/nws_vef) or a warm_arid id (nmsu_ext/uariz_ext) into a utah_dixie
cell -- read those analogs for STRUCTURE only.

## Hard rules
- NO em dashes in consumer copy (region_notes_*, notes, basis_*, chill_basis_*, suitability_note_*,
  cold_basis_*). Use commas/colons/semicolons/periods.
- Temps as the degF glyph (e.g. 95 + degree-glyph + F), NEVER "95 degrees". American English. "plant"
  lowercase mid-sentence.
- Dual-register `region_notes_beginner` + `region_notes_seasoned`, house voice (see cherry-tomato). Lead
  the seasoned note with the St. George reality; name USU where a window comes from it. Do NOT leak build
  words (shard, delta, Shape A) into consumer prose. Do NOT invent a window USU does not give (no
  fabricated fall windows).

## Self-gate EVERY crop (iterate until clean)
```
python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/<YOUR_SHARD>.json <slug>   # -> GATE: PASS
python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/<YOUR_SHARD>.json          # -> 0 issue(s)
```
For onion/shallot, confirm the A9 photoperiod line reads 0. Fix every violation before reporting.

## Write target + report
- Write your cells as one JSON dict `{slug: cell, ...}` to `tools/staging/shards/<YOUR_SHARD>.json`.
- Report: status DONE/BLOCKED, slugs authored, each crop's `region_harness` (PASS) + `region_cell_audit`
  (0), any judgment call (window/suitability/thin-source/heat_pause-months choice), any A9/second_planting
  note. Do NOT paste full cell JSON into the report.
