# Nevada region -- authoring shard guide (read this first)

You are authoring `regions.nevada` cells for a subset of crops in the plant-dataset repo
(`~/plant-dataset`). This is a roster-wide region column. Your output is a set of cells written to
ONE shard file; the controller merges + commits. **DO NOT git commit. DO NOT touch
crops_data_final.json (READ-ONLY). Write ONLY your shard file under `tools/staging/shards/`.**

## Read these first (in order)
1. `docs/reviews/notes/2026-07-21/nevada_sources.md` -- THE BIBLE: frost anchors, chill band, the 6
   shape classes (A-F), per-crop windows, the deltas, and the exact T1 source ids to cite.
2. `tools/staging/nevada_annuals_warm.json` -> the `cherry-tomato` cell = the gate-PASSED **Shape A
   worked template** (exact schema: plantings[], resolved_by_zone[8/9/10], heat_pause object,
   region_notes_*). Copy its structure.
3. For EACH of your crops, read its existing analog cell(s) in `crops_data_final.json` for STRUCTURE
   and biology (DTM, weeks_indoors, the desert calendar shape):
   - `regions.low_desert_az` (Phoenix) -- the primary desert structural donor.
   - `regions.mid_south` -- the frost-anchored deriver shape (heat_pause + cold_pause).
   Query: `python3 -c "import json;d=json.load(open('crops_data_final.json'));c=[x for x in d['crops'] if x['slug']=='<slug>'][0];print(c.get('weeks_indoors'),c.get('days_to_maturity_mid'),c.get('dtm_anchor'),c.get('frost_tolerance_f'));import json as j;print(j.dumps(c['regions'].get('low_desert_az'),ensure_ascii=False)[:1500])"`

## Cell schema (every cell)
`region_id="nevada"`, `region_label="Nevada: Mojave High Desert (Las Vegas Valley)"`,
`zone_span=["8","9","10"]`, `sources=[...nevada ids...]`, `plantings=[...]`, `plantings_provenance=null`,
`resolved_by_zone={"8":{...},"9":{...},"10":{...}}`, `region_notes_beginner`, `region_notes_seasoned`.
Each `resolved_by_zone[z]`: `plant_out`, `start_indoors` (if tray-started), `harvest`, `harvest_start`,
`harvest_end`, `first_plant_date`, `last_plant_date`, `notes`/`zone_notes`/`planting_note` (null unless
authored), `sources`, `anchoring_urls`, `resolution_method="frost_anchored_resolved"`,
`resolved_from={"last_frost","first_frost"}`, and a `calendar` (12 tokens, DERIVED -- see below).

## Frost anchors (resolved_from) -- use verbatim
- z9: last_frost "Feb 28", first_frost "Nov 25"
- z8: last_frost "Mar 15", first_frost "Nov 8"
- z10: last_frost "Feb 15", first_frost "Dec 5"

## Deriving calendar[]
```python
import sys; sys.path.insert(0,'tools')
from annual_calendar import derive_annual_calendar
cell_z = {...your resolved_by_zone[z]...}   # must include heat_pause + resolved_from
cell_z["calendar"] = derive_annual_calendar(cell_z)
```
**Keep January INACTIVE** (author `start_indoors` at early February, never January) so the deriver
renders the honest winter `cold_pause`. INSPECT every calendar: no phantom fall `plant`/`growing`
after the summer on Shape A/C; Nov-Dec must be `cold_pause`.

## Shape rules (your dispatch names your shape)
- **A (warm fruiting: tomato/pepper/eggplant/tomatillo):** ONE spring succession. `start_indoors`
  early Feb, `plant_out` mid-Mar (z9; z8 later ~Apr, z10 earlier ~late-Feb), harvest May-Jun.
  `heat_pause.months` = [7,8,9] (z10 [6,7,8,9]). NO `second_planting`. Cite unlv_mg_svn + unr_sp9911
  + unr_fs0261. (cherry-tomato is the exact template -- clone + adjust DTM.)
- **B (warm quick two-window: bush bean/sweet-corn/cucumber/summer-squash):** spring (Mar-Apr) + a
  late-summer replant (Jul-Aug) via `second_planting` (build with `second_cycle.build_two_cycle_cell`;
  read its docstring `python3 -c "import sys;sys.path.insert(0,'tools');import second_cycle;help(second_cycle.build_two_cycle_cell)"`). heat_pause on the peak-summer gap. A43 envelope rule
  (single-span primary windows; second_planting inside them). Cite unlv_mg_svn.
- **C (long-season heat-lover: okra/sweet-potato/melons/winter-squash/pumpkin/dry-corn/dry-bean/
  pole-bean):** ONE long spring-to-summer planting (Mar-May), grows THROUGH the heat -> **NO
  heat_pause** (check the crop's low_desert_az cell: it carries none). Harvest summer into fall, then
  cold_pause. Cite unlv_mg_svn.
- **D (warm herb/flower: basil/lemongrass/cosmos/marigold/nasturtium/sunflower/zinnia):** single
  warm-season planting (Mar-May), grow through summer, cold_pause. NO heat_pause. Cite unr_fs0261 +
  the crop's analog. Perennial-in-place herbs keep their existing perennial handling if the analog does.
- **E (cool two-window: brassicas/roots/greens/cool-legumes/cool-herbs/cool-flowers/potato):** spring
  (Feb-Apr) + fall (`second_planting` mid-Aug-Oct) via `second_cycle`. heat_pause [6,7,8,9] (or
  season_over) on the summer between. cold_pause winter. A43 envelope. Cite unlv_mg_svn + unr_fs0261.
- **F (fall-planted allium: garlic/onion/shallot/leek/spring-onion):** see the bible's Shape F. garlic
  single FALL Sep 1-Oct 15 (NARROWER than the neighbors -- do not inherit verbatim). onion/shallot
  fall-planted (Oct-Nov sets -> spring harvest), `recommended_day_length_type` short_day or
  intermediate_day (NOT long_day; NO April-or-later plant_out -- A9 must be 0). shallot "follows onion".
  leek/spring-onion are Shape E (two-window). Cite unlv_mg_svn.

## TWO-WINDOW recipe (Shape B and Shape E) -- REQUIRED, second_cycle drops heat_pause
`second_cycle.build_two_cycle_cell(base, spring, fall)` builds a scratch cell with NO heat_pause, so
the summer gap between the spring harvest and the fall replant renders as `growing` and trips A37
(growing-after-harvest). You MUST patch it. The gate-PASSED worked example is
`tools/staging/shards/nevada_w3_quick.json` -> the `cucumber` cell (read it). Per zone:
```python
import sys; sys.path.insert(0,'tools')
from second_cycle import build_two_cycle_cell
from calendar_coherence_gate import impossible_growing_months
cell = build_two_cycle_cell(base, spring, fall)          # base carries resolved_from for THIS zone
bad = impossible_growing_months(cell)                    # [(month_idx0, blocker), ...] = the summer gap
for m,_ in bad: cell["calendar"][m] = "heat_pause"
cell["heat_pause"] = {"months":[m+1 for m,_ in bad], "classification":"heat_pause",
  "basis_seasoned":"<sourced text: Las Vegas summers run past 100 degF Jun-Sep; UNR FS-02-61 notes "
                   "plants do not grow well above 90 degF, so <crop> pauses in the summer heat.>",
  "sources":["unr_fs0261"], "anchoring_urls":{"unr_fs0261":{"url":"https://naes.agnt.unr.edu/PMS/Pubs/2002-3280.pdf","verified":"2026-07-21"}}}
```
Also: cap the spring `harvest_end` at a fixed pre-heat date (so a real gap MONTH exists between spring
harvest and the fall sow -- parse_months ignores day-of-month, so a Jun 20 harvest_end and a Jul 1
fall sow are calendar-adjacent with NO gap token). And if the crop has a `succession_policy`, read its
real `interval_weeks` for `successions_realized` (A8 catches a wrong interval). Follow `low_desert_az`
for direct-sow-vs-tray (mid_south's `second_planting.start_indoors` can be a builder default-fill
artifact). All verified by the W3 shard -- mirror it.

## Sourcing (T1-or-it-does-not-ship)
Cite ONLY nevada source ids (`unlv_mg_svn`, `unr_sp9911`, `unr_fs0261`, `unr_sp2007`, `nws_vef`) in
every cell's `sources`/`anchoring_urls`. NEVER carry `uariz_ext`/`nmsu_ext`/etc. from the analog into
a nevada cell -- read the analog for STRUCTURE only. anchoring_urls: unlv_mg_svn ->
`https://www.unlv.edu/sites/default/files/page_files/27/CampusLife_Planting-Calendar-LasVegas.pdf`;
unr_sp9911 -> `https://extension.unr.edu/publication.aspx?PubID=3267`; unr_fs0261 ->
`https://naes.agnt.unr.edu/PMS/Pubs/2002-3280.pdf`; unr_sp2007 ->
`https://naes.agnt.unr.edu/PMS/Pubs/2020-3713.pdf`; nws_vef ->
`https://www.weather.gov/media/wrh/online_publications/TMs/TM-235.pdf`. verified date "2026-07-21".

## Hard rules
- NO em dashes in any consumer copy (region_notes_*, notes, basis_*). Use commas/colons/semicolons/
  periods. `--` is fine only in code, never in prose.
- Temps as the degF glyph (e.g. `90` + degree + `F`), never "90 degrees". American English. "plant"
  lowercase mid-sentence.
- Dual-register `region_notes_beginner` + `region_notes_seasoned`, house voice (see cherry-tomato).
  Lead the seasoned note with the Nevada-specific reality; name UNR/UNLV where a window comes from them.
- z8/z10 frost dates are gradient-derived off the z9 NWS anchor -- fine to use, do not claim a z8/z10
  station measurement.

## Self-gate EVERY crop (iterate until clean)
```
python3 tools/region_harness.py nevada 8,9,10 tools/staging/shards/<YOUR_SHARD>.json <slug>   # -> GATE: PASS
python3 tools/region_cell_audit.py nevada tools/staging/shards/<YOUR_SHARD>.json               # -> 0 issue(s)
```
`region_harness` runs the full whole_crop_gate on the crop in a scratch env (with nevada_sources.json
injected). It must print `GATE: PASS`. Fix every violation before reporting. For onion/shallot,
confirm the A9 photoperiod line reads 0.

## Write target + report
- Write your cells as one compact-or-pretty JSON dict `{slug: cell, ...}` to
  `tools/staging/shards/<YOUR_SHARD>.json` (the controller re-serializes compact on merge; either is
  fine here).
- Report (to your report file): status DONE / BLOCKED, the slugs authored, each crop's
  `region_harness` result (PASS) + `region_cell_audit` (0), any crop where you made a judgment call
  (window choice, suitability, a thin-source conservative cell), and any A9/heat_pause/second_planting
  note. Do NOT paste full cell JSON into the report -- it is in the shard file.
