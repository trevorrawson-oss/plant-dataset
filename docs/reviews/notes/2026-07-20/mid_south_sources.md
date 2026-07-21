# Mid-South region -- T1 sourcing table (roadmap item 9)

**Arc:** `docs/kickoffs/34-mid-south-region.md` (the launcher) + the mid-Atlantic plan template
(`docs/superpowers/plans/2026-07-20-mid-atlantic-region.md`). Mirrors the mid-Atlantic sources
note format (`docs/reviews/notes/2026-07-20/mid_atlantic_sources.md`).
**Region:** `mid_south`, `zone_span ["7","8"]`, frost-anchored, AR/OK/TN/MO.
**Region label:** `Mid-South: Ozark Uplands and Delta Lowlands`.

**Zone-span decision (the mid-Atlantic scoping lesson):** read from plant-app `zip-zones.json`
(2026-07-20). AR/OK/TN/MO ZIP distribution by USDA zone: z5 39, z6 754, **z7 1,883** (AR 236, MO
360, OK 640, TN 647), **z8 697** (AR 462, OK 106, TN 123, MO 6), z9 1 (a single TN sliver). Span
adopted `["7","8"]`: z7 is dominant (2.7x z8) and the same continuous belt a shade cooler; z8
carries the marquee (Little Rock, the ruling's anchor). The lone z9 TN ZIP rides the belt verdict
(the ruling's own closure, mirroring Nevada's z10 sliver). z5-z6 (793 ZIPs) are the colder
`northern_tier` belt, excluded exactly as mid-Atlantic excluded z6. This matches the kickoff's
predicted ~1,900 z7 / 697 z8.

**Sources.** Unlike mid-Atlantic (whose `vce_426_331`/`ncsu_ext` were pre-catalogued), the UAEX
publication set was NOT catalogued. The parent portals `uada_ext` (U of A Cooperative Extension),
`ok_state_ext`, `mu_ext`, `mo_ext_g6201/g6461` already exist; this arc registers the specific
load-bearing UAEX publications + NWS Little Rock as new `source_catalog` sub-IDs (the
`uariz_ext_az1005`-under-`uariz_ext` sub-ID pattern). All fetched/verified 2026-07-20 in the
controller env (`pypdf` for the two PDFs; subagent sandboxes block PDF tooling).

New `source_catalog` entries (staged in `tools/staging/mid_south_sources.json`, promoted with the batch):

| id | publication | url | backs |
|---|---|---|---|
| `nws_lzk` | NWS Little Rock, Frost/Freeze Information for Arkansas | https://www.weather.gov/lzk/frostfreeze.htm | z8 frost anchor (Little Rock: last frost Apr 3, first frost Oct 31) |
| `uada_ext_fsa6001` | UAEX FSA6001, Home Gardening Series planting dates + Arkansas frost zones | https://www.uaex.uada.edu/publications/pdf/FSA-6001.pdf | Arkansas frost-zone table (z7 anchor, Frost Zone D: Apr 10 / Oct 24); the climate-zone adjustment |
| `uada_ext_spring_veg` | UAEX, Arkansas spring and summer vegetable planting dates | https://www.uaex.uada.edu/yard-garden/vegetables/spring-summer-planting-dates.aspx | spring/summer windows (Zone C) |
| `uada_ext_fall_veg` | UAEX, Planting Dates for Fall Vegetable Production | https://www.uaex.uada.edu/yard-garden/vegetables/fall-planting-dates.aspx | the documented FALL cycle (DTM + fall windows) -- the reason the region exists |
| `uada_ext_chill` | UAEX, Chilling Hour Reports (AR Fruit/Veg/Nut Update blog) | https://www.uaex.uada.edu/farm-ranch/crops-commercial-horticulture/horticulture/ar-fruit-veg-nut-update-blog/posts/chillhours.aspx | the chill band (real AR station accumulation) |
| `uada_ext_fsa6105` | UAEX FSA6105, Blackberry Production in the Home Garden (M. Elena Garcia) | https://www.uaex.uada.edu/publications/PDF/FSA-6105.pdf | blackberry (the signature crop): UA-released cultivar chill figures, statewide adaptation, spring planting |

Citation discipline (`region_cell_audit`): within ONE cell a source id must map to exactly one
URL. A fall-cycle warm/cool cell therefore cites `uada_ext_spring_veg` on its spring windows +
`uada_ext_fall_veg` on its fall windows (two ids, two URLs, clean). Spring-only cells cite just
`uada_ext_spring_veg`.

---

## 1. Frost anchors (`resolved_from`) -- the deriver inputs

| Zone | last_frost | first_frost | Basis |
|---|---|---|---|
| **7** | **Apr 10** | **Oct 24** | UAEX FSA6001 Arkansas Frost Zone D (northern/upland edge). Belt z7 = NW AR Ozarks (Fayetteville, the U of A chill station) + eastern OK + most TN + southern MO uplands. Season 197 days. |
| **8** | **Apr 3** | **Oct 31** | NWS Little Rock (Adams Field, Pulaski Co.), 1991-2020 normals, 36 degF, 50% probability. The marquee central-AR anchor (the ruling's z8 station). Season 211 days. |

FSA6001 Arkansas frost-zone table (verbatim), for reference: Zone A Mar 20 / Nov 15; Zone B Mar
27 / Nov 7; **Zone C Apr 1 / Oct 30** (central AR, ~= Little Rock ~= USDA z8; the "Zone C" the
UAEX spring table is keyed to); **Zone D Apr 10 / Oct 24** (adopted z7 anchor); Zone E Apr 20 /
Oct 20 (highest/coldest, into `northern_tier`).

**Modeling note.** The frost-anchored deriver reads each crop's crop-intrinsic `plantings[]`
offsets (DTM, weeks-indoors) against the zone frost dates, so the resolved windows fall out of the
anchors; the UAEX planting tables (below) are the VALIDATION that they land in the right months,
plus the source of the FALL windows the naive single-cycle deriver omits. z7's ~14-day-shorter
frost-free season pulls its spring later and its fall earlier than z8, as UAEX's own
climate-zone-adjustment note (FSA6001) directs.

---

## 2. UAEX spring/summer planting windows (Zone C = central AR = z8)

`uada_ext_spring_veg`, verbatim Zone C periods (FSA6001 adjusts north/upland zones ~2-3 wk later):

| UAEX crop | Spring (Zone C / z8) |
|---|---|
| Lima Beans | April - August |
| Snap Beans | March - August |
| Pole Beans | March - August |
| Beets | February - April |
| Broccoli | February - April |
| Brussels Sprouts | February - April |
| Cabbage | February - April |
| Cantaloupe | April - May |
| Carrots | February - April |
| Cauliflower | February - April |
| Collards | February - July |
| Corn (Sweet) | March - August |
| Cucumbers (Pickling/Slicing) | April - May |
| Eggplant | April - May |
| Okra | April - May |
| Peppers | April - May |
| Popcorn | April - June |
| Sweet Potato | April - June |
| Squash (summer) | April - May |
| Squash (winter) | May - July |
| Tomato | March - May |
| Watermelon | April - May |

These broad Zone C windows are consistent with the frost-anchored spring dates (tomato plant_out
z8 Apr 10, inside "March - May"; peppers/eggplant/okra/melons after frost, inside "April - May").
Author the spring cycle from each crop's existing offsets re-resolved to the mid-South anchors;
cite `uada_ext_spring_veg`.

## 3. UAEX FALL vegetable planting windows (state-wide, ~= central AR / z8) -- THE reason the region exists

`uada_ext_fall_veg`, verbatim (with DTM). Header note: "To produce tomato, cabbage, broccoli or
cauliflower plants for fall crops, sow seed about four weeks earlier than the listed planting
dates." The naive single-cycle deriver omits this entire second cycle.

| UAEX crop | DTM | Fall window (z8 / state-wide) |
|---|---|---|
| Tomatoes (plants) | 75-80 | **Jul 1 - Jul 15** |
| Sweet Corn | 72-86 | Jul 1 - Jul 15 |
| Southern Peas | 55-75 | Jul 15 - Aug 1 |
| Summer Squash | 55-60 | Jul 15 - Aug 15 |
| Irish Potatoes | 90-100 | Jul 15 - Aug 1 |
| Beans (Bush) | 50-60 | Aug 1 - Sep 1 |
| Beans (Lima) | 70-75 | Aug 1 - Aug 15 |
| Cucumbers | 50-60 | Aug 1 - Aug 15 |
| Broccoli | 70-80 | Aug 1 - Sep 1 |
| Chinese Cabbage | 70-75 | Aug 1 - Sep 1 |
| Collards | 70-75 | Aug 1 - Sep 15 |
| Cabbage (plants) | 65-70 | Aug 10 - Sep 1 |
| Cauliflower (plants) | 60-70 | Aug 10 - Sep 1 |
| Carrots | 65-75 | Aug 1 - Aug 15 |
| Turnips | 50-60 | Aug 1 - Sep 15 |
| Mustard | 50-60 | Aug 1 - Sep 15 |
| Swiss Chard | 60-70 | Aug 15 - Sep 1 |
| Beets | 60-70 | Aug 15 - Sep 1 |
| Kale | 60-65 | Aug 20 - Sep 15 |
| Lettuce | 50-55 | Aug 20 - Sep 15 |
| Radish | 25-30 | Aug 20 - Sep 15 |
| Spinach | 40-50 | Aug 25 - Sep 15 |

**z7 fall windows:** UAEX's fall table is anchored to central AR (~z8). The colder z7 upland (first
frost ~1 week earlier, Oct 24 vs Oct 31) plants its fall crops earlier: shift each z8 fall window
~1 week earlier for z7, which is exactly the FSA6001 climate-zone adjustment UAEX directs. Anchor
the fall `plant_out` off `first_frost` so this falls out of the deriver.

## 4. The fall-cycle crop map (drives the warm/cool split + which crops get `second_planting`)

**Warm-season crops WITH a UAEX fall cycle (the headline finding):** tomatoes (fall Jul 1-15, DTM
75-80), cucumbers (Aug 1-15), summer squash / zucchini / yellow (Jul 15-Aug 15), bush snap beans
(Aug 1-Sep 1), lima beans (Aug 1-15), southern peas / cowpea (Jul 15-Aug 1), sweet corn (Jul 1-15).
Note vs mid-Atlantic: UAEX's tomato fall is TIGHTER (Jul 1-15 vs VCE Jul 1-Aug 10), UAEX ADDS a
sweet-corn + southern-pea fall cycle, and UAEX does NOT list a fall pole-bean window (bush only).

**Warm-season crops with NO fall cycle (author spring-only, honestly):** peppers (all), eggplant,
okra, tomatillo, cantaloupe / honeydew / watermelon, winter squash (acorn/butternut/spaghetti),
pumpkin, sweet potato, pole beans, edamame, dry-bean, broad-beans-fava. Their DTM does not finish a
fall planting before frost in this belt (UAEX lists no fall window).

**Cool-season crops WITH a UAEX fall cycle:** broccoli, cabbage, cauliflower, bok-choy (~chinese
cabbage), collards, kale, swiss-chard, beet, carrot, turnip, mustard-adjacent greens, lettuce-leaf,
radish, spinach. Fall is their strong season here. NO `heat_pause` on cool crops (the deriver
renders midsummer as `growing`).

**Irish/white potato:** UAEX documents a fall potato crop (Jul 15-Aug 1). Author potato's fall
cycle from that window.

**Garlic / shallot / onion (fall-set alliums):** NOT in UAEX's summer-sown fall-veg table. AR
garlic is fall-PLANTED (cloves overwinter) as its PRIMARY cycle, not a summer second crop; author
per each crop's existing biology (mirror the crop's `northern_tier` cell), cite `uada_ext_spring_veg`
as the belt planting-date authority, flag in `notes` where UAEX gives no explicit window.

**Coverage gaps (culinary herbs + crops with no UAEX row):** basil, cilantro, dill, parsley,
chamomile, borage, bee-balm, and the flowers/ornamentals are not in the UAEX vegetable tables.
Author them from a conservative frost-anchored spring window mirroring the crop's existing
`northern_tier` z7 cell (same states, cooler edge), cite `uada_ext_spring_veg` as the belt
frost/planting authority, flag in `notes`, NEVER invent a fall cycle a source does not document.
Enumerate the exact gap list against the live roster at authoring start. T1-or-it-doesn't-ship.

## 5. Chill (trees) -- UAEX Chilling Hour Reports

`uada_ext_chill`: average accumulated chilling hours by March 1 (Utah model; 1990-2000 baseline;
35-45 degF the good-accumulation band), verbatim by station:

| Station | USDA zone | Chill hrs by Mar 1 |
|---|---|---|
| Southwest Research Station, Hope (SW warm edge) | 8 | **901** |
| U of A Campus, Fayetteville (NW Ozark upland) | 7 | 1,024 |
| Wynne (NE Delta) | 8 | 1,069 |
| Fruit Research Station, Clarksville (western) | 7-8 | 1,081 |

**The intra-state gradient (delta #2 from mid-Atlantic).** Unlike mid-Atlantic's blanket ">1,000",
AR's own stations show a real spread (901-1,081). Hope, the belt's southwestern warm edge, banks
~901 hours -- essentially at the ceiling of the canonical apple variety set (McIntosh, 900) with
~1 hour of margin. The northern/upland z7 (Fayetteville 1,024) and the delta z8 (Wynne 1,069) bank
more. Chill still clears the whole canonical tree-variety range everywhere in the belt, so all
trees resolve `fruits_reliably` (with the apricot + sweet-cherry `marginal` exception below, which
is a frost/disease call, not a chill deficit), but author the band + provenance HONESTLY to the
gradient, tighter than mid-Atlantic's.

### Chill band adopted (`region_chill_delivered.mid_south`)

| Zone | band | basis |
|---|---|---|
| 7 | **[1000, 1300]** | NW/upland edge: Fayetteville 1,024 (z7) floor; cooler-continental TN/OK/MO uplands accrue more. |
| 8 | **[900, 1100]** | SW warm edge Hope 901 floor (the tight margin) up through the western/delta stations (Clarksville 1,081 / Wynne 1,069). |

Both bands clear the 900-hour apple ceiling (z8 floor 900 = the honest Hope figure), so the tree
set fruits. The band reads LOWER than mid-Atlantic's (z7 [1100,1500] / z8 [1000,1350]) because the
Mid-South, further south with a warm SW edge, genuinely banks less chill -- an honest delta, not a
copy. `chill_gate` validates shape only (numeric [lo,hi], lo<=hi); the A3 tree split uses each
crop's lowest recommended-variety requirement, cleared many times over here.

## 6. Trees / citrus / berries -- suitability

- **Chill-gated trees (14):** all `fruits_reliably` on the belt's real chill (band clears every
  canonical variety), EXCEPT **apricot + cherry-sweet = `marginal`** (carries from mid-Atlantic,
  Trevor's 2026-07-20 call: chill clears, but the humid East's early-bloom frost, brown rot, and
  fruit cracking make reliable crops marginal). **Sour cherry stays `fruits_reliably`.** Pomegranate
  marginal (as mid-Atlantic). Pawpaw is NATIVE to the Ozarks/Mid-South -- a genuine strength.
- **Citrus (5):** cold-limited (z7-8 winters kill citrus); `survives`/`unsuitable` with honest
  `cold_basis_*`, container culture only at the warm z8 edge if sourced. Same shape as mid-Atlantic.
- **Blackberry -- THE signature crop (delta #3).** UAEX FSA6105 (`uada_ext_fsa6105`): "Blackberries
  are adapted to all regions of Arkansas... Varieties developed by the University of Arkansas fruit
  breeding program are recommended for use in the state." UA-released cultivar chill figures (Table
  1), which line up with the canonical variety roster:
  Kiowa ~200-300, Prime-Jim/Prime-Jan ~300-400, Ouachita ~400-500, Chickasaw ~500, Apache ~800-900,
  Navaho ~800-900 (all UA releases). Planting: "Plant blackberry roots or rooted plants anytime in
  the spring before the soil warms"; "first crop... harvested the year after the planting is
  established." The belt's real chill (901-1,081) clears the entire range many times over -- chill
  is a NON-factor for blackberry. Lead the blackberry `mid_south` cell + prose on this home-state
  fit (the Mid-South analog of blueberry's mid-Atlantic highlight). Blueberry: rabbiteye for the
  belt's uplands, cite the belt planting authority.

## 7. Authoring method (mirror mid-Atlantic exactly)

Reuse the mid-Atlantic staging cell for each crop as the STRUCTURAL template (same 111 roster, same
frost-anchored model, same `["7","8"]` span, same fall-cycle machinery). Per crop:
1. Swap `region_id` -> `mid_south`, `region_label` -> `Mid-South: Ozark Uplands and Delta Lowlands`.
2. Swap source ids: `vce_426_331` -> `uada_ext_spring_veg` (spring) / `uada_ext_fall_veg` (fall) /
   `uada_ext_fsa6105` (blackberry). Update every `anchoring_urls`, `source_quote`, `sources`.
3. Re-resolve every `resolved_by_zone` date from the crop's SAME `plantings[]` offsets against the
   mid-South anchors (z7 Apr 10/Oct 24, z8 Apr 3/Oct 31) -- crop biology offsets are intrinsic, only
   the anchors change. `resolved_from` = the mid-South anchors; `resolution_method` unchanged.
4. FALL-CYCLE crops: set the fall `plant_out` to the UAEX fall window (Section 3), not VCE's. Keep
   primary windows single-span; nest the fall cycle in `second_planting` (A43). Use
   `tools/second_cycle.py:build_two_cycle_cell` to combine-then-split + derive the calendar[]
   (`derive_annual_calendar` does NOT render `second_planting` on its own -- see memory
   fall-cycle-deriver-combine-then-split).
5. Rewrite ALL prose (`region_notes_{beginner,seasoned}`, `heat_pause.basis_seasoned`,
   `synthesis_note_seasoned`) for the Mid-South / UAEX / Arkansas, dual-register house voice, NO em
   dashes, American English, `°F`.
6. `heat_pause` on warm-season fall-cycle crops only where a real midsummer set-failure gap exists
   (declaration-driven; the humid-subtropical se_gulf convention, NOT PNW cool-summer). Source it.
7. Gate each crop: `python3 tools/region_harness.py mid_south 7,8 <staging.json> <slug>` -> PASS +
   `region_cell_audit mid_south` 0 issues.
