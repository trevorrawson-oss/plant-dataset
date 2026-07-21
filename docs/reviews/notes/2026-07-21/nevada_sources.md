# Nevada high-desert region -- T1 sourcing table + per-crop window/shape reference

**Region:** `nevada` = "Nevada: Mojave High Desert (Las Vegas Valley)", `zone_span ["8","9","10"]`.
**Base canonical:** `a071f0c1`. **Plan:** `docs/superpowers/plans/2026-07-21-nevada-high-desert-region.md`.
This note is the single source of truth the Task 4-8 authoring shards follow. Every window/verdict
traces to a T1 source below. All sources fetched/rendered in the build controller env 2026-07-21
(subagent sandboxes cannot run pypdf/fitz).

## New source_catalog entries (staged in `tools/staging/nevada_sources.json`, added in the atomic promote)

| id | backs | tier |
|---|---|---|
| `nws_vef` | NWS Las Vegas WR-235 frost normals: z9 last Feb 28 / first Nov 25 | T1 (.gov) |
| `unr_sp2007` | UNR SP-20-07 North Las Vegas apple field trial (variety + chill) | T1 (sub-ID of unr_ext) |
| `unr_fs0261` | UNR FS-02-61 warm/cool season framework + 90 degF ceiling | T1 (sub-ID of unr_ext) |
| `unr_sp9911` | UNR SP-99-11 tomato: Mar 15 practical frost, >90/<55 cutoff, NO fall tomato | T1 (sub-ID of unr_ext) |
| `unlv_mg_svn` | UNLV/UNR Master Gardener per-crop planting chart (the load-bearing window source) | T1 (extension_master_gardener_program) |

`unr_ext` (the parent portal) is already catalogued -- NOT modified; the three `unr_*` ids are net-new
sub-IDs under it (the `uada_ext_fsa6001`-under-`uada_ext` pattern). The Almanac.com 1991-2020
cross-check (~Feb 20 / ~Dec 8, directionally consistent) is corroboration only, NOT registered.

## Frost anchors (resolved_from) per zone

| zone | last_frost | first_frost | basis |
|---|---|---|---|
| 9 (Las Vegas Valley, 94 ZIPs, marquee) | **Feb 28** | **Nov 25** | NWS WR-235 (`nws_vef`), 1961-90 normals, verbatim |
| 8 (cooler/higher pockets, 15 ZIPs) | **Mar 15** | **Nov 8** | gradient-derived: ~2 wk later last / ~2.5 wk earlier first than z9 |
| 10 (Laughlin/Colorado River, 1 ZIP) | **Feb 15** | **Dec 5** | gradient-derived: ~2 wk earlier last / ~1.5 wk later first than z9 |

z8/z10 are gradient-derived off the z9 NWS anchor (no direct z8/z10 Nevada station normal was
T1-fetchable); this is flagged honestly in `region_chill_delivered_provenance` and should be reflected
in the cell provenance too. **Warm-crop transplant windows are authored to UNR's grower-facing dates**
(mid-March, `unr_sp9911` / `unlv_mg_svn`), not the raw Feb 28 meteorological mean. To keep January a
`cold_pause` month (so the frost-anchored deriver renders the honest Nov-Dec cold_pause and does NOT
suppress it on a January-active cell), author indoor starts at **early February** (six weeks before a
mid-March transplant -- the short end of `unr_sp9911`'s "6 to 8 weeks before" range).

## Chill band (`tools/staging/nevada_chill_band.json`)

`region_chill_delivered.nevada = {"8":[500,900], "9":[300,700], "10":[150,450]}`. z9 trial-anchored
(SP-20-07 Granny Smith 700 hr = confirmed ceiling); z8/z10 elevation-gradient derived. Sits between
Phoenix `low_desert_az [100,400]` and NM high desert `warm_arid [450,850]`.

## The seasonal framework (`unr_fs0261` / `unlv_mg_svn`, verbatim-confirmed)

- **Warm-season vegetables:** planted **March through May** (`unr_fs0261`: "March until May").
- **Cool-season vegetables:** **mid-February through April** AND **mid-August through the end of
  October** (`unr_fs0261`, verbatim) -- a two-window (spring + fall) structure.
- **Heat ceiling:** plants "do not grow well at temperatures above 90 degF" (`unr_fs0261`); tomato
  fruit set fails >90 degF day / <55 degF night (`unr_sp9911`). Las Vegas routinely exceeds 100 degF
  June-September -> the summer `heat_pause` months are **Jun-Sep** for the crops it binds (see shapes).
- **No fall tomato:** `unr_sp9911` explicitly does not recommend a fall/second tomato planting for
  Southern Nevada (unlike Phoenix's fall reflush) -- the delta-1 divergence.

## Per-crop SHAPE reference (from the UNLV Master Gardener chart `unlv_mg_svn`, read from the rendered image + text layer)

The chart's shading gives each crop's real Southern Nevada window(s). Mapped to the roster's 82
frost_anchored slugs + the 5 shape classes below. Windows are the PLANTING (transplant/sow) months;
the frost-anchored deriver computes exact dates from `resolved_from` + crop biology, refined to these.

### Shape A -- warm fruiting: single spring, heat_pause Jun-Sep, NO second_planting (delta 1)
Fruit set fails in the summer heat; UNR recommends no fall replant. Spring transplant **mid-Mar**
(indoor start early Feb), harvest May-Jun before the heat wall, `heat_pause` Jun-Sep, then
`season_over` -> `cold_pause` (no fall crop). Cite `unlv_mg_svn` + `unr_sp9911` + `unr_fs0261`.
- **cherry-tomato, beefsteak-tomato, grape-tomato, heirloom-tomato, roma-tomato, tomatillo** (Tomato* row: spring only).
- **bell-pepper, banana-pepper, cayenne-pepper, habanero, jalapeno** (Pepper* row: spring Mar-Apr + a small May window; no fall).
- **eggplant** (Eggplant* row: spring Mar-Apr, hotbed-started; no fall).

### Shape B -- warm quick: two-window (spring Mar-Apr + late-summer Jul-Aug), heat_pause between
The chart shades these in both spring AND Jul-Aug (a real fall-harvest replant the desert supports for
fast crops). Use `second_cycle.build_two_cycle_cell`; A43 envelope applies. Cite `unlv_mg_svn`.
- **green-beans-bush** (Beans-bush: Mar-Apr + Jul-Aug), **edamame** (follows bush bean).
- **sweet-corn** (Corn-sweet: Mar-Apr + Jul-Aug).
- **cucumber, english-cucumber, pickling-cucumber, slicing-cucumber** (Cucumber: Mar-Apr + Aug).
- **yellow-summer-squash, zucchini-courgette** (Squash-summer: Mar-Apr + Jun + Aug).

### Shape C -- long-season heat-lover: single long spring-to-summer planting, NO heat_pause (grows through the heat)
These thrive in the >100 degF summer and produce right through it -- NO heat_pause (matches their
existing hot-region cells, which carry none). Plant Mar-May, harvest summer into fall, `cold_pause`
winter. Cite `unlv_mg_svn`.
- **okra** (Okra: Mar-May), **sweet-potato** (Potato-sweet: Apr-May).
- **cantaloupe, honeydew-melon, watermelon** (Cantaloupe/Muskmelon/Watermelon: Mar-Apr + Jun).
- **acorn-squash, butternut-squash, spaghetti-squash, pumpkin** (Squash-winter/Pumpkin: Mar-Apr + Jun-Jul).
- **pole-beans, dry-bean** (Beans-pole: Mar-Apr, single long season -- dry-down needs the full run, no Jul replant).
- **field-corn, flint-corn, popcorn** (dry corns follow sweet-corn's spring window but single long-season for the dry-down; no Jul replant).

### Shape D -- warm herbs/flowers not on the chart: single spring, grow through summer
Author from Shape C framework + the crop's existing hot-region cell. Cite `unr_fs0261` (warm-season
framework) + the crop's analog.
- **basil, lemongrass** (warm herbs, Mar-May, heat-tolerant).
- **cosmos, marigold, nasturtium, sunflower, zinnia** (warm-season flowers, Mar-May).

### Shape E -- cool-season: two-window (spring Feb-Apr + fall mid-Aug-Oct), heat_pause Jun-Sep
The desert cool-crop pattern the chart confirms crop-by-crop. Spring Feb-Apr, `heat_pause` (or
`season_over`) Jun-Sep, fall replant mid-Aug-Oct (`second_planting`), `cold_pause` winter. Cite
`unlv_mg_svn` + `unr_fs0261`.
- **Brassicas:** broccoli, cauliflower, cabbage, brussels-sprouts, kale, collards, kohlrabi, bok-choy, arugula (chart: spring Feb + fall Aug-Sept-Oct).
- **Roots:** beet, carrot, turnip, radish, parsnip (chart: spring Feb-Mar + fall Aug/Sept-Oct; radish Feb-Mar-Apr + Sept-Oct).
- **Greens:** lettuce-leaf, spinach, swiss-chard, celery (chart: spring Feb-Mar + fall Aug-Oct/Nov; celery Mar-Apr hotbed).
- **Cool legumes:** snow-peas, sugar-snap-peas, broad-beans-fava (Pea: spring Feb-Mar + fall Sept-Oct).
- **potato** (Potatoes-Irish: spring Feb-Mar; a fall crop is optional/marginal -- author spring-primary).
- **Cool herbs:** cilantro-coriander, dill, parsley, chives, chamomile (spring Feb-Apr + fall Aug-Sept).
- **Cool/perennial flowers + herbs:** calendula, viola, borage, sweet-alyssum, sweet-pea, bee-balm, echinacea, mint (cool framework; the perennial ones -- bee-balm, echinacea, mint -- carry their existing perennial-in-place handling).

### Shape F -- fall-planted alliums (deltas)
- **garlic (DELTA 3):** single FALL clove planting **Sept 1 - Oct 15** (chart: garlic shaded Sept
  through early Oct), harvest the following early summer. NARROWER than warm_arid ("late Sep-Nov") /
  low_desert_az ("mid-Sep-Nov") -- do NOT inherit either verbatim. Cite `unlv_mg_svn`.
- **onion (A9 WATCH):** dry onions are **fall-planted** (chart: Onions-dry shaded Sept-Oct, plus an
  early-Feb set option that is BEFORE April so it does not trip A9 either). Author the FALL plant_out
  (Oct-Nov sets -> late-spring harvest) as primary; `recommended_day_length_type` = **short_day** or
  **intermediate_day** (Las Vegas ~36 degN; matches low_desert_az/warm_arid onion). No April-or-later
  plant_out -> A9 photoperiod window-fit satisfied by construction. Cite `unlv_mg_svn`.
- **shallot:** follows onion by species identity (both Allium cepa Aggregatum); cell says "follows onion".
- **spring-onion** (Onions-green): spring Feb-Mar + fall Aug-Sept (Shape E cool, not a bulbing allium).
- **leek** (Leek: spring Feb-Mar + fall Aug-Oct -- a two-window cool allium, Shape E).

## Trees (Task 6) -- apple delta 2 (`unr_sp2007`)

Apple `fruits_reliably` (SP-20-07 North Las Vegas field trial). `chill_basis_*` prose NAMES the
trial-confirmed reliable picks + the safely low-chill set, FLAGS the high-chill unproven tier:
- **Reliable (named):** Dorsett Golden (Top Choice, 100 hr), Pink Lady (Top Choice, 300-400 hr trial),
  Mutsu (Top Choice, 500 hr), Anna (Notable, 200 hr), Fuji (Notable, <500 hr), Granny Smith (Notable,
  700 hr = ceiling). Plus safely low-chill: Ein Shemer (100), Dolgo (500), Gala (600, under ceiling).
- **Flagged unproven for Las Vegas (>=700 hr, no local trial evidence):** Zestar! (800), McIntosh
  (900), Empire (700), Honeycrisp (800), Golden Delicious (700), Jonagold (700), **plus Liberty (800,
  trial "under review"/inconclusive)**.
Other 13 trees: judged vs the `[300,700]` z9 band per each crop's `chill_hours_required` (Task 6).
peach/apricot/nectarine re-judged from the ARID reality (NO humid brown-rot rationale). pawpaw is a
humid-forest understory tree -> honest `marginal`/`unsuitable` in the dry Mojave. pomegranate / fig /
persimmon / mulberry desert-strong. NO fabricated per-tree Nevada chill numbers -- the band + the
crop's own requirement + honest arid framing.

## Citrus (Task 7)

Las Vegas is COLDER than Phoenix (SP-20-07: colder winter nights). Citrus MORE cold-limited than
low_desert_az -> mostly `survives` (protected/container, sourced) or `unsuitable`; mandarin/kumquat
least bad, lime/grapefruit worst. Re-judged fresh, not cloned from Phoenix's warmer verdict.

## Perennials (Task 8)

Woody herbs (lavender/rosemary/oregano/sage/thyme) desert-STRONG (arid heat + alkaline soil).
Berries MARGINAL in prose (no suitability field): blackberry/raspberry marginal (heat + alkaline,
fall-bearing/low-chill steer where sourced), blueberry very-marginal (acid-soil need vs alkaline
Mojave -> container-only honesty), elderberry marginal. Strawberry a cool-window annual (fall-set /
winter-spring harvest).

## Method notes for the shards

1. STRUCTURAL donor = the crop's `low_desert_az` (Phoenix) cell (heat_pause placement, calendar[]
   shape, plantings/resolved_by_zone/provenance structure). RE-ANCHOR windows to the Nevada frost
   dates + the shape above; RE-CITE to the Nevada sources (never carry uariz_ext into a nevada cell).
2. Add the z8 column (Phoenix has none); z10 rides z9's shape with the warmer frost anchor.
3. Derive calendar[] with `annual_calendar.derive_annual_calendar`; INSPECT the tail (no phantom fall
   growing on Shape A; Nov-Dec = cold_pause). Two-window shapes (B, E) via `second_cycle`.
4. Dual-register `region_notes_*`, house voice, NO em dashes, American English, degF.
5. Gate each crop: `region_harness.py nevada 8,9,10 <staging.json> <slug>` + `region_cell_audit.py
   nevada <staging.json>` -> both clean. Onion/shallot: A9 must be 0.
