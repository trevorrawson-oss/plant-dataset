# RGV / subtropical South Texas -- T1 sourcing table (Task 3)

**Date:** 2026-07-13
**Arc:** RGV / subtropical-TX region (roadmap item 3); design spec
`docs/superpowers/specs/2026-07-13-rgv-subtropical-tx-region-design.md`; cell contract
`docs/rgv_cell_contract.md`.
**Purpose:** the single source of truth Tasks 4-7 cite when authoring the 108 `regions.rgv` cells.
Every row is Tier 1 (university `.edu` extension or a government agency). Where a class's T1
month windows are thin or PDF-locked, that is stated explicitly and the crop is flagged for a
**conservative cell** -- never fabricate a window.

**All URLs verified live 2026-07-13.**

---

## 0. Source catalog ids (for `sources` / `anchoring_urls` in the cells)

`tamu_agrilife` (Texas A&M AgriLife Extension, `https://agrilifeextension.tamu.edu`) is already
catalogued and is the **safe primary id** for every RGV cell: the per-cell `anchoring_urls` map
carries the SPECIFIC publication URL per class (the `url` field is free per cell), so no new
catalog id is strictly required. `lsu_agcenter` is also already catalogued (chill corroboration).
Optional finer-grained ids are **proposed** below for Task 8 to add to `source_catalog` if it wants
per-publication precision; if it declines, fall back to `tamu_agrilife` + the specific URL in
`anchoring_urls`.

| proposed id | publication | url |
|---|---|---|
| `tamu_rgv_veg_guide` | RGV Homeowner Vegetable Guide (Dr. Juan Anciso), Cameron Co. AgriLife | https://cameron.agrilife.org/files/2022/05/RGV-Homeowner-Vegetable-Guide-2022.pdf |
| `tamu_lrgv_veg_bilingual` | Vegetable Crops of the Lower Rio Grande Valley (Bilingual Planting Guide, 2025) | https://agrilifeextension.tamu.edu/wp-content/uploads/2025/08/Bilingual-Vegetable-Planting-Guide.pdf |
| `tamu_agrilife_citrus` | Aggie Horticulture Fruit & Nut Resources -- Citrus fact sheet | https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/ |
| `tamu_agrilifetoday_chill` | AgriLife Today -- "Texas fruit crops need rain, chill hours" (Larry Stein, Ph.D.) | https://agrilifetoday.tamu.edu/2022/02/15/texas-fruit-crops-need-rain-chill-hours/ |
| `tamu_smallacreage_strawberry` | Aggie Horticulture Small Acreage -- Strawberries crop guide | https://aggie-horticulture.tamu.edu/smallacreage/crops-guides/fruits-nuts/strawberries/ |

Already-catalogued ids reused here: `tamu_agrilife`, `tamu_agrilife_aggie_spring`
(`https://aggie-hort.tamu.edu/archives/parsons/earthkind/ekgarden14.html`),
`tamu_agrilife_fall_veg`
(`https://agrilifeextension.tamu.edu/wp-content/uploads/2025/06/Fall-Vegetable-Gardening-Guide.pdf`),
`lsu_agcenter`.

---

## 1. The sourcing table

| crop_or_class | source_id | url | windows (T1) | tier | notes |
|---|---|---|---|---|---|
| **Annuals -- cool-season (winter garden):** beet, broccoli, brussels-sprouts, cabbage, carrot, cauliflower, swiss-chard, collards, garlic, kale, lettuce, mustard, bulb-onion, spinach, turnip, radish, pea/english-pea, parsley, cilantro, arugula, etc. | `tamu_rgv_veg_guide` (+ `tamu_lrgv_veg_bilingual`, `tamu_agrilife_fall_veg`) | RGV guide PDF (above); Bilingual LRGV guide PDF; Fall Vegetable Gardening Guide | **Winter garden.** Plant **Sep-Oct** (cole crops "planted beginning in October"; some fall crops from September); harvest ~**Nov-Mar**; summer (~Apr/May-Sep) = planting gap (`season_over`). Verbatim: "Cole crops such as broccoli, cabbage, cauliflower, kale, mustard, and turnips are planted beginning in October." Frost-tolerant set (quoted): "beet, broccoli, Brussels sprouts, cabbage, carrot, cauliflower, chard, collard, garlic, kale, lettuce, mustard, onion, parsley, spinach and turnip." | T1 | **Source is T1 and rich; NOT thin.** The per-crop month rows live in the RGV Homeowner Vegetable Guide / Bilingual LRGV guide **PDF tables**, which this session's tooling could not parse (WebFetch cannot read these compressed PDFs; `pdftotext`/`curl` are blocked in this environment). **Tasks 4/7 must open the PDF table (or the `tamu_agrilife_aggie_spring` Region-V column) and read the exact per-crop dates.** Extraction gap, not a sourcing gap. |
| **Annuals -- warm-season (spring + fall around mid-summer pause):** tomato, pepper, eggplant, bush-bean, pole-bean, southern-pea, summer-squash, winter-squash, zucchini, cucumber, cantaloupe/muskmelon, watermelon, sweet-corn, okra, sweet-potato, potato, warm herbs (basil), etc. | `tamu_rgv_veg_guide` (+ `tamu_lrgv_veg_bilingual`, `tamu_agrilife_aggie_spring`) | RGV guide PDF; Bilingual LRGV guide PDF; Aggie Hort Spring Planting Guide (Regions I-V) | **Spring window starts late Feb-early Mar** (verbatim: "You may start planting warm weather vegetables (corn, green beans, peppers, zucchini, etc.) in late February and early March"); long spring harvest into early summer; **fall window ~Aug-Sep** planting; **mid-summer heat pause ~Jun-Aug** (`heat_pause` only where a T1 heat-stop is stated, else `season_over`). | T1 | Same PDF-extraction caveat as the cool-season row. Class-level model is T1-verified; per-crop months are in the PDF table. `second_planting` (fall) shape applies where the guide gives a fall date. |
| **Citrus (5):** grapefruit, orange-navel, lemon, lime, mandarin-clementine | `tamu_agrilife_citrus` (+ Valley Citrus Notes; citrus crop brief) | https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/ ; https://aggie-horticulture.tamu.edu/vegetable/guides/crop-briefs/citrus-in-texas/ ; https://aggie-horticulture.tamu.edu/citrus/citrus_notes/ | **Harvest Oct-May** (verbatim: "Citrus harvesting in the Lower Rio Grande Valley normally begins in October and lasts into April or May"; grapefruit "hand harvested from October to May"). **Bloom ~Feb-Apr** (verbatim: "By March, navels have about bloomed out, while earlies and Valencias are close to it, though grapefruit bloom is yet to come" -> navel/orange bloom Feb-Mar, grapefruit Mar-Apr). Commercial citrus "mostly limited to the Lower Rio Grande Valley" (70% grapefruit, 30% oranges). Cold context: satsuma "may withstand 18 degrees F ... completely dormant ... but may be seriously damaged at 24 degrees F in early December." | T1 | **GOOD coverage.** `suitability: fruits_reliably`. Per-type harvest nuance for the flagship calendars: navel/early oranges peak fall (Oct-Jan); Valencia/late oranges into spring (Mar-May); grapefruit Oct-May; lemon/lime main fall-winter. Bloom Feb-Apr. Grapefruit + orange-navel + mandarin-clementine are the heat-gated three (`heat_summer_basis: high`); lemon/lime are NOT heat-gated (contract 3.4). |
| **Chill-gated NO-FRUIT trees (10):** apple, apricot, cherry-sour, cherry-sweet, nectarine, peach, pear-asian, pear-european, plum, pawpaw | `tamu_agrilifetoday_chill` (+ `lsu_agcenter`) | https://agrilifetoday.tamu.edu/2022/02/15/texas-fruit-crops-need-rain-chill-hours/ ; https://www.lsuagcenter.com/articles/page1766001059887 | RGV delivered chill **~0-300 hours** (see the chill band, section 2). Verbatim (Larry Stein, Ph.D., AgriLife Extension horticulturist): "Orchards in the Rio Grande Valley might have trees that require 200-300 chill hours" vs North Texas "900-1,000 hours." | T1 | **No windows to author** -- `suitability: survives_no_fruit`, **empty calendar** (A3: band low edge 0 < every crop's `min_variety_chill`, so all are chill-limited -> empty calendar; see section 3). Honest note: apple (floor 100) / peach (400) etc. have ultra-low-chill cultivars that MIGHT crop in a cold Valley winter, but delivery is unreliable (warm winters bank ~0), so the crop-level "survives, does not reliably fruit" verdict is honest and matches the design. `pawpaw` also needs real summer chill/humidity tolerance -- check if it warrants `unsuitable` over `survives_no_fruit`. |
| **Low-chill fruit -- LIKELY FRUIT (4):** fig, mulberry, persimmon, pomegranate | `tamu_agrilife` (library pages: figs / pomegranates / persimmons) | https://agrilifeextension.tamu.edu/library/farming/texas-fruit-and-nut-production-figs/ ; https://agrilifeextension.tamu.edu/library/farming/texas-fruit-and-nut-production-pomegranates/ ; https://agrilifeextension.tamu.edu/asset-external/path-to-the-plate-persimmons/ | Adaptation T1-supported: pomegranate "Many fruiting types ... should survive most winters throughout the central, southern, and southeastern parts of Texas"; persimmon "adapted to most of Texas"; figs grown across Texas (TAMU fig production guide). These four are LOW-CHILL / subtropical-adapted fruit that TAMU reports cropping in South Texas dooryards. Their `fruits_reliably`/`marginal` verdict is a HORTICULTURAL authoring judgment on that adaptation evidence, NOT a band-vs-floor calculation (the band low edge is 0, below the 100 floor, exactly as for apple -- see the A3-mechanics note in section 4); A3 then requires each to carry a real (conservative) calendar. | T1 | **THIN on exact RGV bloom/harvest months.** Suitability (`fruits_reliably` / `marginal`) is T1-backed; the per-crop RGV month windows are NOT in accessible T1 text. **Conservative cells needed.** **`mulberry` is the thinnest** (TAMU RGV guidance did not specifically address mulberry) -> consider `marginal` + honest note. Task 6 pulls harvest months from the specific TAMU production guides (PDFs) or authors conservatively. |
| **Berries (4):** blackberry, blueberry, raspberry, elderberry | `tamu_agrilife` (Berry & Nut Crops, Crops of Texas) | https://aggie-horticulture.tamu.edu/vegetable/guides/the-crops-of-texas/berry-and-nut-crops/ ; https://agrilifeextension.tamu.edu/asset-external/texas-fruit-and-nut-production-blackberries/ | TAMU "Berry and Nut Crops" Table 14 (commercial acreage): **blackberry/dewberry 0 acres, blueberry 0 acres, raspberry 0 acres in the Lower Valley.** Blueberry needs acid soil (RGV soils are alkaline) + chill. "Rabbiteye is grown in acid soils." | T1 | **Suitability partly T1-backed; windows THIN -> conservative cells.** **blueberry: unsuitable/marginal** (alkaline Valley soils + chill -- strong T1 signal). **raspberry: marginal/unsuitable** (heat + chill). **blackberry: marginal** (low-chill Texas cultivars e.g. Brazos/Rosborough + dewberries grow in South/Central TX, but 0 commercial Lower-Valley acres -- design's "strong" is optimistic; treat as marginal-to-adapted dooryard with a low-chill-cultivar note). **elderberry: marginal/adaptable** (native to Texas). Task 7 authors conservative calendars + honest suitability notes. |
| **Strawberry (1):** strawberry | `tamu_smallacreage_strawberry` | https://aggie-horticulture.tamu.edu/smallacreage/crops-guides/fruits-nuts/strawberries/ | Adapted "South of Houston, San Antonio and Del Rio" (includes the RGV); **"harvest late March to early April"**; grown as a **winter annual** (fall plant -> spring harvest). | T1 | Harvest (late Mar-early Apr) + winter-annual model are T1. **Planting month slightly thin** in accessible T1 text (fall set-out ~Oct-Nov is the standard South-Texas winter-annual timing) -> author the plant window conservatively / corroborate at authoring. Task 7. |
| **Woody-ornamental herbs (5):** rosemary, oregano, sage, thyme, lavender | `tamu_agrilife` (targeted herb source TBD) | https://aggie-horticulture.tamu.edu/ (herb guidance) | **Not a primary Task-3 research target; RGV-specific T1 windows THIN.** Rosemary/oregano/sage/thyme are Mediterranean perennials that grow year-round in subtropical South Texas (fall/spring establishment); lavender struggles in Valley heat + humidity. | T1 (pending targeted pull) | **Conservative cells + honesty note.** Task 7 should pull a targeted Aggie Horticulture / AgriLife herb guide for RGV-region windows, or author conservative year-round-establishment cells with a **lavender humidity-struggle note** (design 3, spec section 5). Do not fabricate precise windows. |

---

## 2. The chill band (delivered to `tools/staging/rgv_chill_band.json`)

`region_chill_delivered.rgv = {"9": [0, 300], "10": [0, 300]}`

**Figure + source.** Texas A&M AgriLife Extension (AgriLife Today, 2022-02-15; Larry Stein, Ph.D.,
AgriLife Extension horticulturist, Uvalde): *"Orchards in the Rio Grande Valley might have trees
that require 200-300 chill hours"* (vs North Texas 900-1,000). The Valley is subtropical with about
340 frost-free days (Aggie Horticulture, Crops of Texas), so in warm winters it banks essentially
**no** chill -- hence the `0` low edge. Corroborated by LSU AgCenter (T1): coastal south Louisiana,
a comparably subtropical Gulf climate, receives 200-300 chill hours; the RGV is warmer, so equal or
lower.

**Why `[0, 300]` for both zones.** The `200-300 hr` TAMU figure is Valley-wide (not split by z9/z10),
so both zone rows carry the same envelope -- the established pattern for a single-figure region
(`low_desert_az` z9/z10 are both `[100,400]`; `hawaii_tropical` all zones `[0,150]`). Ordering: RGV
`[0,300]` sits just above the deep-tropical `fl_peninsula` z11 / `hawaii_tropical` `[0,150]` (design's
"RGV runs slightly higher") and below `se_gulf` z8-9 (`[350,650]`). Matches the design spec's
order-of-magnitude `[0,300]` and the cell-contract chill_basis prose ("roughly 0 to 300 chill
hours") exactly.

**Shape validated:** `chill_gate.chill_table_violations` returns `[]` with `rgv` spliced into the
real table (region -> {zone -> [lo,hi]}, numeric, 0 <= lo <= hi).

---

## 3. Provenance shape finding (for the Task 8 promote emitter)

**`region_chill_delivered_provenance` is a single top-level STRING, NOT a per-region dict.** The
plan's assumed path `region_chill_delivered_provenance.rgv` **does not exist** and must not be
created.

- **Band splice path:** `region_chill_delivered.rgv` (add key `"rgv"` to the existing
  `region_chill_delivered` dict). Staging key: `"region_chill_delivered.rgv"`.
- **Provenance splice path:** the top-level scalar `region_chill_delivered_provenance` (replace the
  whole string). Staging key: `"region_chill_delivered_provenance"` (**no `.rgv` suffix**). The
  staging value is the **complete new string** = the existing canonical provenance string with the
  RGV clause spliced in (before "Bands are the climate's typical winter delivery envelope..."), so
  Task 8 assigns it directly: `data["region_chill_delivered_provenance"] = staging[key]`. A naive
  dotted-path setter over the two staging keys does the right thing (band = sub-key add; provenance
  = top-level scalar set).

---

## 4. A3 no-fruit split -- chill floors checked (for Task 6)

`perennial_gate.min_variety_chill` (lowest recommended-variety `chill_hours_required`, default 400)
for the 14 chill-gated crops, vs the band low edge `0`:

| crop | min_variety_chill | A3 result at chill_lo=0 |
|---|---|---|
| apple | 100 | 0 < 100 -> survives_no_fruit, **empty calendar** |
| apricot | 350 | empty calendar |
| cherry-sour | 700 | empty calendar |
| cherry-sweet | 250 | empty calendar |
| nectarine | 300 | empty calendar |
| peach | 400 | empty calendar |
| pear-asian | 250 | empty calendar |
| pear-european | 200 | empty calendar |
| plum | 250 | empty calendar |
| pawpaw | 400 | empty calendar |
| fig | 100 | Archetype 2 (`fruits_reliably`/`marginal`, real calendar) |
| mulberry | 100 | Archetype 2 |
| persimmon | 100 | Archetype 2 |
| pomegranate | 100 | Archetype 2 |

**The band's `0` low edge is load-bearing:** apple's floor is only 100, so any low edge >= 100 would
flip apple to a "must carry a calendar" verdict and break the design's no-fruit intent. Keep `lo = 0`.

**A3-mechanics note (verified against `tools/perennial_gate.py:128-148`, for Task 6):** A3 does NOT
derive the suitability verdict from the chill band. The AUTHOR declares the verdict; A3 only enforces
its calendar-presence CONSISTENCY: a `survives_no_fruit` chill-gated cell with `chill_lo < floor`
must have an EMPTY calendar (over-promise guard), a `survives_no_fruit` cell with `chill_lo >= floor`
must CARRY one (under-report guard), and a `fruits_reliably`/`marginal` cell must carry one. So the
split between the no-fruit set (apple/apricot/cherries/nectarine/peach/pears/plum -- declared
`survives_no_fruit`, forced empty because `chill_lo=0 < floor`) and the fruiting set
(fig/mulberry/persimmon/pomegranate -- declared `fruits_reliably`/`marginal` on TAMU adaptation
evidence, requiring a real calendar) is an AUTHORING call, not something the band computes: apple and
fig share a floor of 100, and the band treats them identically. Task 6 authors the four low-chill
fruits with real (conservative) calendars and the ten no-fruit trees with empty ones; pawpaw is a
candidate for `unsuitable` (needs summer chill/humidity tolerance it lacks in the Valley).

---

## 5. Thin-source flags (crops that get a CONSERVATIVE cell)

- **fig, mulberry, persimmon, pomegranate** -- suitability T1-backed, exact RGV bloom/harvest months
  thin; **mulberry the thinnest** (consider `marginal`).
- **blackberry, blueberry, raspberry, elderberry** -- blueberry unsuitable/marginal (alkaline soil),
  raspberry marginal/unsuitable (heat), blackberry marginal (0 commercial Lower-Valley acres),
  elderberry marginal; windows thin -> conservative calendars + honest suitability notes.
- **strawberry** -- harvest + winter-annual model T1; fall plant month slightly thin.
- **rosemary, oregano, sage, thyme, lavender** -- RGV-specific T1 windows thin (not a Task-3 target);
  conservative year-round-establishment cells + lavender humidity note; pull a targeted herb source.
- **All 79 annuals** -- NOT thin (T1 source is rich), but the per-crop month rows are **PDF-locked**
  from this session's tooling; Tasks 4/7 read them directly from the RGV / Bilingual LRGV guide
  tables (or the `tamu_agrilife_aggie_spring` Region-V column).

---

## 6. Self-review

- [x] Every window in the table has a T1 citation OR is explicitly flagged thin / PDF-locked.
- [x] Every source is Tier 1 (`.tamu.edu` / `.agrilife.org` AgriLife Extension, or `lsuagcenter.com`
      LSU AgCenter -- a university extension). No T2 (seed-trade / commercial nursery) sources used;
      the `fourwindsgrowers.com` hit surfaced in search was **excluded** as non-T1.
- [x] Chill band passes `chill_gate.chill_table_violations` shape check (`[]`).
- [x] Chill figure is T1-sourced (TAMU AgriLife / Larry Stein) with LSU AgCenter corroboration; no
      fabricated precision (order-of-magnitude `[0,300]`, matching the design).
- [x] Provenance shape verified against the real canonical (single STRING, not a dict); correct
      splice path documented.
- [x] Canonical `crops_data_final.json` untouched (read-only); only the two new files created.
- [x] No em dashes in the provenance string; American English; catalog-id style matches the existing
      provenance string.
