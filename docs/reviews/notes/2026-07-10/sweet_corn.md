# sweet-corn — T1 source research + pinned data (Task 1)

**Date:** 2026-07-10. **Purpose:** pin every sweet-corn-specific value to a Tier-1 source before
authoring the GS anchor. Modeled structurally on certified `green-beans-bush` (same warm-season
direct-sow shape: `dtm_anchor from_sow`, `calendar_basis frost_anchored`), but sweet corn is
wind-pollinated (block planting, not row planting), harvested green at the **milk stage** (never
dried down), and its variety selection is driven by **sugar genetics (su / se / sh2)** rather than
disease packages. This is the first GRASS-family, wind-pollinated crop on the register — no
inherited-culture shortcut from a same-genus certified crop exists (unlike dry-bean's reuse of
green-beans-bush), so every value below is freshly sourced.

**Source set used (13 T1 institutions, all university/government extension):** `umn_ext`,
`iastate_ext`, `msu_ext` (Michigan State), `msstate_ext` (Mississippi State), `ncsu_ext`,
`uga_ext`/`uga_b577`, `tamu_agrilife`, `nmsu_ext_cr457b`, `uariz_ext`/`uariz_ext_az1005`,
`ucanr_ext_mg_timeplanting`, `uf_ifas_vh021`, `uhawaii_ctahr`, `cornell_ext`, `unl_ext`. All 13
source_ids already exist in `source_catalog` (see Task 3 catalog-gap section — **zero new
top-level source_ids required**; three new specific-publication sub-ids are recommended, all
nested under already-cataloged institutions, same pattern as `uga_b577` / `uariz_ext_az1005`).

---

## 1. Core biology — pinned values

| field | value | source | source_id | url |
|---|---|---|---|---|
| `spacing_inches` | `[8, 12]` (in-row) | UMN "8 to 12 inches apart"; Iowa State "8 to 12 inches apart"; UGA "8 to 12 in. between each seed in the row"; NMSU "8—12 [inches] between plants" — four independent T1 sources converge exactly | `umn_ext`, `iastate_ext`, `uga_ext` (C905), `nmsu_ext_cr457b` | https://extension.umn.edu/vegetables/growing-sweet-corn ; https://yardandgarden.extension.iastate.edu/how-to/growing-sweet-corn-home-garden ; https://fieldreport.caes.uga.edu/publications/C905/growing-home-garden-sweet-corn/ ; https://pubs.nmsu.edu/_circulars/CR457B/ |
| `sow_depth_inches` | `[1, 2]` (shallower, ~0.5–1 in, for sh2 in warm soil) | UGA "approximately 1 in. deep"; Iowa State "1 inch in heavy soils" to "2 inches" in light sandy soils; NMSU "1—2 [inches]" standard, "1/2—1" for supersweet (sh2) | `uga_ext` (C905), `iastate_ext`, `nmsu_ext_cr457b` | (as above) |
| `thin_to_inches` | `[8, 12]` (most guides sow at final spacing; TAMU sows dense 3–4 in and thins to 12 in) | TAMU: "Plant the corn seeds about 1 inch deep and 3 to 4 inches apart in the row... After the plants are up, thin them to 1 foot apart" | `tamu_agrilife` | https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2013/09/EHT-044.pdf |
| `germination_temp_f` | `[60, 90]` (practical recommend-to-plant floor 60°F; su types tolerate down to 50–55°F, se/sh2 need ≥60°F; UGA frames the full operational range as 60–90°F) | UMN: "seeds germinate best when soil temperatures are close to 60°F"; NC State: "Minimum soil temperatures for germination are 50°F for su varieties and 60°F for se, sh2, and sy varieties"; Iowa State: su/se "55 to 60°F", sh2 "at least 60°F"; UGA: "soil temperatures between 60–90°F" | `umn_ext`, `ncsu_ext`, `iastate_ext`, `uga_ext` (C905) | https://extension.umn.edu/vegetables/growing-sweet-corn ; https://content.ces.ncsu.edu/organic-sweet-corn-production ; https://fieldreport.caes.uga.edu/publications/C905/growing-home-garden-sweet-corn/ |
| `planting_layout` | `"block"` (NOT single/double rows) | UMN: "Plant in blocks of at least four rows rather than a long single row for proper pollination"; TAMU: "Sweet corn grows best when planted in several short rows instead of one long row" | `umn_ext`, `tamu_agrilife` | https://extension.umn.edu/vegetables/growing-sweet-corn |
| `pollination_block_min_rows` | `4` | NC State (verbatim): **"Plant the corn in blocks of at least 4 rows to insure good pollination"**; UMN (verbatim): **"Plant in blocks of at least four rows"**; independently corroborated by UGA/USU/WSU/OK State per multi-source search sweep | `ncsu_ext`, `umn_ext` | https://content.ces.ncsu.edu/organic-sweet-corn-production ; https://extension.umn.edu/vegetables/growing-sweet-corn |
| isolation (context, not a listed field but load-bearing for the block-planting design rationale) | sh2 isolated from su/se by ≥250–300 ft OR ≥14 days' difference in tasseling/maturity date; all sweet corn isolated from field/pop/ornamental corn by ≥300 yd | NC State: "Plant supersweet varieties at least 300 feet from non-supersweet varieties, or stagger planting dates... two weeks apart"; "separated from different types of corn... by at least 300 yards"; Iowa State FAQ: "at least 250 feet apart" or "14 days should separate the tasseling time" | `ncsu_ext`, `iastate_ext` | https://content.ces.ncsu.edu/organic-sweet-corn-production ; https://yardandgarden.extension.iastate.edu/faq/what-are-differences-between-various-types-sweet-corn |
| `heat_threshold_f` | `95` (Purdue's more conservative 90°F noted as a secondary figure — see flag below) | UNL CropWatch (verbatim): **"Heat over 95°F depresses pollen production"**; "when temperatures reach the high 90s to the 100s, the heat can... desiccate silks and reduce silk fertility" | `unl_ext` | https://cropwatch.unl.edu/how-extended-high-heat-disrupts-corn-pollination-0/ |
| `heat_effect` | `"poor_fruit_set"` *(reused existing enum value — see flag below)* | same as above; heat during the pollination window kills pollen viability and desiccates silks, reducing kernel set — functionally the corn analogue of the beans/cucumber "poor_fruit_set" effect already in the dataset's vocabulary | `unl_ext` | (as above) |
| `frost_tolerance_f` | `32` | UMN: wait to plant "until at least two weeks after the last average killing frost" (implies zero frost tolerance at planting); NC State: "Frost will injure sweet corn at any stage of growth" | `umn_ext`, `ncsu_ext` | https://extension.umn.edu/vegetables/growing-sweet-corn ; https://content.ces.ncsu.edu/organic-sweet-corn-production |
| `frost_effect` | `"killed"` | (as above) | `ncsu_ext` | (as above) |
| `chilling_sensitivity_f` | `50` | Iowa State ICM (verbatim): **"A chilling effect occurs when water colder than 50 degrees F is imbibed"** during the first 24–48 hours after planting (imbibitional chilling injury) | `iastate_ext` | https://crops.extension.iastate.edu/cropnews/2014/05/imbibitional-chilling-and-frost-damage-corn-and-soybean-seedlings |

## 2. Days to maturity — crop-level (JUDGMENT CALL, needs Trevor's ratification)

**No single T1 page gives one crop-wide DTM number** — every source gives a range, and the range
shifts by sugar type, region, and season (fall crops mature faster on higher summer heat units).
Convergent T1 figures:

- UMN: "Ranges span 63–92 days across varieties"
- Iowa State: "Most sweet corn varieties mature in about 60–90 days"
- TAMU: "Most sweet corn varieties... mature between 60 to 90 days after seeding"
- U of A Yavapai (Backyard Gardener #223): "maturity range of 60 to 90 days depending on variety"
- MSU (Michigan) bucket system: "Early (less than 70 days), mid-season (70–84 days) and late (more
  than 84 days)"
- UGA's own Home Garden Planting Chart (B577) lists **Corn 80–100 days** (a fuller-season regional
  pick for Georgia's long season)
- NMSU CR457B Table 2: **81 days** flat for su/se/sh2 alike (a single regional cultivar set)
- U of A AZ1005 (Maricopa): **"Corn, Sweet 70–90 days"**
- UH CTAHR (Hawaii, subtropical, fastest cycle): **"sweet corn is ripe in 70 days"**

**Proposed:** `days_to_maturity = [60, 90]`, `days_to_maturity_mid = 75` — the composite matches
the majority-repeated general figure (UMN/Iowa State/TAMU/AZ Yavapai) and sits centered between
Hawaii's 70-day fast end and the Southeast's 80–100-day full-season regional pick. **Flag for
Trevor:** should the headline mid lean later (78–80) to better track UGA/NMSU/AZ1005's regional
picks, which are all ≥70? Recommend keeping 75 as the honest cross-regional middle and letting
`regions{}` carry the per-region skew (as `green-beans-bush`/`dry-bean` already do).

## 3. Growth-stage ladder (`day_range_from_sow`) — SYNTHESIS, needs Trevor's ratification

No single T1 source publishes a full day-by-day sweet-corn stage table (agronomic corn-stage
literature — Iowa State's `corn-growth-stages`, Purdue, SDSU — publishes VE/V-stages/VT/R1–R6 but
keys them to *days-after-silking* or GDD, not a calendar-day table for a home-garden sweet corn
crop). The ladder below is built from convergent day-count facts across multiple T1 sources,
anchored to the `[60,90]` mid-75 DTM above — the same honest-synthesis discipline `dry-bean` used
for its ladder. **This needs Trevor's eyeball before it becomes canon.**

| stage id | `day_range_from_sow` | T1 anchor facts |
|---|---|---|
| `germination` | `[0, 10]` | Iowa State ICM: emergence "4 to 6 days after planting" (warm, moist soil); UH CTAHR: coleoptile emergence "between five and six days after planting in Hawaii". Cool soil extends this; the imbibitional-chilling window (first 24–48 hr) sits inside this stage. |
| `seedling` | `[7, 21]` | TAMU: second planting timed for "when the first corn plants have three to five leaves. This usually takes 2 to 3 weeks"; UH CTAHR: "three leaves, each about 2 inches long" by 10 days after planting. |
| `vegetative` | `[18, 45]` | UH CTAHR: stem elongation ("knee-high") begins "about three weeks after planting"; U of A Yavapai: nitrogen sidedress "when plants have 8 to 10 leaves"; reproductive (ear/tassel) initiation begins "between three and four weeks after planting" (UH CTAHR) — vegetative bridges seedling to that initiation point. |
| `tasseling` | `[43, 55]` | UH CTAHR: tassel "begins to form about four weeks after planting"; VT is "2 to 3 days before silk emergence" (general corn-growth-stage literature); Univ. of Illinois: "Beginning 9–10 weeks after emergence, tassels become fully visible" (describes a fuller-season type — the faster end of this range reflects home-garden early/mid varieties and Hawaii's accelerated cycle). |
| `silking` | `[48, 60]` | Silks emerge "2 to 3 days after the tassel opens" (multi-source convergence); silks "remain receptive to pollen for up to two weeks" (general corn-growth-stage literature). |
| `kernel_fill` | `[55, 72]` | Post-fertilization ear/kernel development through the approach to milk stage; UH CTAHR: cob reaches full length within a week of pollination, kernels "obviously swollen" at two weeks. |
| `harvest` | `[68, 85]` | Milk-stage harvest window: Iowa State "18 to 23 days after silking" (15 days or less in hot weather); MSU/UGA/UH CTAHR converge on **~18–20 days after silking**; NC State: the milk stage "only lasts 4 to 5 days" once reached. |

Mins are non-decreasing through the ladder (0, 7, 18, 43, 48, 55, 68); maxes likewise (10, 21, 45,
55, 60, 72, 85) — same overlapping-window shape as `green-beans-bush`.

## 4. Milk-stage harvest cue (sourced, not a judgment call)

| field | value | source | source_id | url |
|---|---|---|---|---|
| harvest readiness cue | silks brown/dry at the tip; kernels release milky (not clear, not doughy) juice when punctured; ear feels full/firm to the squeeze | Iowa State FAQ (verbatim): "the silks are brown and dry at the ear tip... When punctured with a thumbnail, the soft kernels produce a milky juice"; UH CTAHR: "silks have turned dark brown... kernels on the tips... are plump and milky. Sweet corn is not ready when the juice... is watery. It is overripe when the kernels get large, chewy and pasty" | `iastate_ext`, `uhawaii_ctahr` | https://yardandgarden.extension.iastate.edu/faq/when-should-i-harvest-sweet-corn |
| days from silking to harvest | 17–24 days (18–20 most common; as few as 15 in hot weather, up to 24 in cool weather) | Iowa State: "approximately 18 to 23 days... 15 days or less if... exceptionally warm"; NC State: "17 to 18 days after silking under warm... or 22 to 24 days... during cool weather"; UGA C905: "about 20 days after the appearance of the first silk strands"; UH CTAHR: "18 days after the silks appear" | `iastate_ext`, `ncsu_ext`, `uga_ext` (C905), `uhawaii_ctahr` | (as above) |
| harvest window length once reached | ~4–5 days (NCSU); "less than a week" (Univ. of Illinois) | NC State: "This stage only lasts 4 to 5 days" | `ncsu_ext` | https://content.ces.ncsu.edu/organic-sweet-corn-production |
| sugar-type effect on harvest window | su: narrow, 1–2 days at peak quality; se: 1–2 days longer than su; sh2: longest window, up to ~1 week refrigerated | Iowa State FAQ: su "retain their high quality for only 1 or 2 days"; se "storage life is 1 to 2 days longer" than su; sh2 "storage life for up to one week with refrigeration" | `iastate_ext` | https://yardandgarden.extension.iastate.edu/faq/what-are-differences-between-various-types-sweet-corn |

## 5. Sugar genetics (su / se / sh2) — variety DTMs (sourced, cross-referenced across 2 T1 lists each)

Genetics explainer (T1-sourced): standard sugary (**su**) is the oldest type, ~9–15% sugar at
harvest, converts to starch fastest, narrowest quality window; sugary-enhanced (**se**) carries
the added `se` gene for higher, more stable sugar and tender kernels, holds 1–2 days longer than
su; supersweet/shrunken-2 (**sh2**) has the `sh2` gene, 4–10x the sugar of su, converts to starch
very slowly, longest storage — but has a tougher seed coat and needs warmer soil to germinate.
Source: MSU (Michigan) Extension "primer on decoding the sweet corn section of your seed
catalogue"; NC State organic sweet corn production page.

| sugar type | representative variety | days_to_maturity | source | source_id | url |
|---|---|---|---|---|---|
| **su** (standard sugary) | Sweet G-90 | **75 days** | Mississippi State Extension (verbatim): "Sweet G-90—bicolor; very tender and sweet; 75 days." Cross-referenced as a `su` ("Normal sugary") type variety in TAMU's own EHT-044 variety table. | `msstate_ext`, `tamu_agrilife` | https://extension.msstate.edu/lawn-and-garden/vegetable-gardens/corn-sweet ; https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2013/09/EHT-044.pdf |
| **se** (sugary enhanced) | Bodacious | **75 days** | Mississippi State Extension (verbatim): "Bodacious—homozygous se; yellow; early (75 days)." Cross-referenced as an `se` type variety in TAMU's EHT-044 table. | `msstate_ext`, `tamu_agrilife` | (as above) |
| **sh2** (supersweet / shrunken-2) | How Sweet It Is | **88 days** | Mississippi State Extension (verbatim): "How Sweet It Is—white; 8-inch ears; late; requires isolation; 88 days." Cross-referenced as an `sh2` type variety ("Honey n Pearl" list) in TAMU's EHT-044 table AND in USU's sh2 recommendation list. AAS 1986 winner. | `msstate_ext`, `tamu_agrilife` | (as above) |
| **sh2** (secondary example) | Summer Sweet 7210 | **78 days** | Mississippi State Extension (verbatim): "Summer Sweet 7210—yellow; 8-inch ears; midseason; requires isolation; 78 days." | `msstate_ext` | (as above) |

**Not T1-precise (flag):** "Silver Queen" (su) is the most widely cross-referenced variety across
ALL THREE regional T1 lists gathered (USU, TAMU, MSU) — it is clearly the industry-standard su
benchmark — but none of the three gives an explicit DTM figure (MSU only says "late"). Seed-trade
sources consistently cite 88–96 days (widely ~92). If a fourth, more traditional/heirloom-leaning
su example is wanted alongside Sweet G-90, Silver Queen ~92 days is defensible but not T1-pinned;
flag for Trevor.

## 6. Per-region sow → harvest timing (the 10 `regions{}` keys, read from `green-beans-bush`)

| region | sow window | DTM used regionally | source | source_id | url |
|---|---|---|---|---|---|
| `northern_tier` | wait for soil ≥60°F, then sow; typically mid-May (south of zone) to early June (north of zone); NY: fresh-market corn under plastic in March, processing corn "begins around May 1st" statewide | favor early types (<70 days, MSU bucket) to finish before first fall frost | `umn_ext`, `cornell_ext` | https://extension.umn.edu/vegetables/growing-sweet-corn ; https://cvp.cce.cornell.edu/crop.php?id=34 |
| `se_gulf` | Spring: **Mar 15 – Jun 1**; Fall: **Jun 1 – Jul 20** (Middle Georgia anchor; shift ±2 wk north/south per UGA's standing north/south adjustment note) | **80–100 days** (chart); fall crops finish faster on higher summer heat units (UGA notes fall DTM can shorten to as little as 58 days vs. a typical 77) | `uga_ext` (B577) | https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf |
| `ca_interior` | **Mar – Jul; also Aug** | 65–90 days (general UC ANR figure) | `ucanr_ext_mg_timeplanting` | https://ucanr.edu/program/uc-master-gardener-program/time-planting |
| `ca_north_coast` | **May – Jul** (marine-layer, heat-limited; later start than interior) | 65–90 days | `ucanr_ext_mg_timeplanting` | (as above) |
| `ca_south_coast` | **Mar – Jul** | 65–90 days | `ucanr_ext_mg_timeplanting` | (as above) |
| `ca_desert` | **Feb – Mar** only (avoid summer pollination heat — consistent with the 95°F heat threshold pinned above) | 65–90 days | `ucanr_ext_mg_timeplanting` | (as above) |
| `warm_arid` (S. NM / W. TX, zone 8) | spring, after soil warms and frost risk passes (exact NM half-month window not resolved from CR457B's Table 2 alone — **flag: needs a direct read of CR457B's zone-by-zone planting-date table at authoring time**) | **81 days** (NMSU CR457B Table 2, flat across su/se/sh2) | `nmsu_ext_cr457b`, `tamu_agrilife` | https://pubs.nmsu.edu/_circulars/CR457B/ |
| `low_desert_az` (Maricopa, zone 9b) | spring-dominant (AZ1005's two-season model: spring + fall, with summer excluded per the climate section's soil/heat-extreme warning); **exact half-month S-markers in AZ1005's table not cleanly resolved by text extraction — flag: needs a direct visual re-check of the az1005 planting-calendar table at authoring time** | **70–90 days** (AZ1005 Table, verbatim row: "Corn, Sweet 70-90 days") | `uariz_ext_az1005` | https://extension.arizona.edu/sites/default/files/2024-08/az1005-2018.pdf |
| `fl_peninsula` | North FL: **Mar–Apr**; Central FL: **Aug**; South FL: **Jan–Apr** and **Oct–Mar** (inverted-calendar region, per the standing SE/Gulf-at-z10-11 model) | **65–90 days** | `uf_ifas_vh021` | https://edis.ifas.ufl.edu/publication/VH021 |
| `hawaii_tropical` | year-round (subtropical, no true dormant season; UH-bred hybrids adapted to short winter daylength — mainland-bred hybrids are NOT recommended, they underperform/fail in Hawaii's <14-hr days) | **70 days** (UH CTAHR, verbatim: "In Hawaii's lowlands, sweet corn is ripe in 70 days") — the fastest of all 10 regions | `uhawaii_ctahr` | https://www.ctahr.hawaii.edu/oc/freepubs/pdf/corn2003.pdf |

**Option C precedent applies cleanly here, probably with NO hard `suitable:false` regions at
all** (unlike dry-bean, which had 3). Every region above has a genuine T1-sourced planting window;
even `ca_desert`'s narrow Feb–Mar window and `northern_tier`'s short-season squeeze are workable
with early varieties — an honest advisory ("short window, pick an early <70-day su or se type")
rather than a hard exclusion. Flag for Trevor: confirm no region needs `suitable:false` before
authoring — this is a materially different ruling shape than dry-bean's.

## 7. Catalog gaps (Step 3 — grep of `crops_data_final.json`'s `source_catalog`)

All 13 source_ids used above **already exist** in `source_catalog` (grep-verified against the
134-entry catalog: `umn_ext`, `iastate_ext`, `msu_ext`, `msstate_ext`, `ncsu_ext`, `uga_ext`,
`uga_b577`, `tamu_agrilife`, `nmsu_ext_cr457b`, `uariz_ext`, `uariz_ext_az1005`,
`ucanr_ext_mg_timeplanting`, `uf_ifas_vh021`, `uhawaii_ctahr`, `cornell_ext`, `unl_ext` — 16 ids,
all present). **Zero new top-level `source_catalog` entries required.**

**Recommended NEW sub-ids** (following the existing `uga_b577` / `uariz_ext_az1005` pattern of
giving a frequently-cited specific publication its own catalog sub-id under an already-cataloged
institution — these are enrichments, not blockers):

| proposed source_id | publisher | title | url |
|---|---|---|---|
| `uga_c905_sweet_corn` | UGA Extension | Growing Home Garden Sweet Corn (Circular 905, 2024) | https://fieldreport.caes.uga.edu/publications/C905/growing-home-garden-sweet-corn/ |
| `uariz_ext_byg223` | U of A Cooperative Extension (Yavapai County) | Backyard Gardener #223 — Sweet Corn | https://extension.arizona.edu/sites/default/files/2024-10/SweetCorn_0.pdf |
| `uhawaii_ctahr_corn2003` | UH CTAHR | Corn Production in the Tropics: The Hawaii Experience (Brewbaker, 2003) | https://www.ctahr.hawaii.edu/oc/freepubs/pdf/corn2003.pdf |

These three become `add` ops in the Task 6 catalog batch if Trevor wants the extra citation
precision; the crop can also cert with just the parent institution ids if that level of
granularity isn't needed.

## 8. Open findings / flags for Trevor (summary)

1. **Crop-level `days_to_maturity` `[60,90]` mid `75`** is a synthesis (no single T1 page states
   one number) — same honest-synthesis discipline as dry-bean's DTM. Needs ratification.
2. **Growth-stage ladder (7 stages)** is a synthesis from convergent day-count facts, not a single
   T1 table. Needs ratification, same as dry-bean's ladder.
3. **`heat_effect` reuses the existing `"poor_fruit_set"` enum value** rather than minting a new
   one (e.g. `"poor_pollination"`) — flagged as a vocabulary-reuse judgment call for the authoring
   task; the existing 5-value enum (`bolting`, `quality_loss`, `heat_tolerant`, `crown_failure`,
   `poor_fruit_set`) has no exact "poor kernel set from heat" term, and `poor_fruit_set` is the
   closest semantic fit.
4. **`heat_threshold_f` = 95** (UNL, "depresses pollen production") vs. Purdue's more conservative
   90°F ("temperatures above 90°F have the potential to negatively impact pollination") — two
   T1 figures, chose the more decisive one; flag if Trevor prefers the more conservative 90.
5. **`warm_arid` and `low_desert_az` exact sow-window half-months not fully resolved** — NMSU
   CR457B's Table 2 gave DTM (81 days) and depth/spacing but the fetch tool couldn't confirm the
   region's specific planting month range; the AZ1005 PDF's planting-calendar table read correctly
   for the DTM row ("Corn, Sweet 70-90 days") but the exact half-month S-markers didn't resolve
   cleanly from the text extraction of a dense 24-column table. Both are readable directly (I have
   the raw PDFs) — recommend a follow-up direct visual pass at authoring time if the exact sow
   window (not just DTM) is load-bearing for those two regions.
6. **Per Option C**, no region on this list looks like it needs `suitable:false` — a notable
   contrast with dry-bean (which had 3 unsuitable regions for the dry-down/cure step). Corn's
   milk-stage fresh harvest sidesteps dry-bean's humid-region field-drying problem entirely.
   Confirm this reading before authoring the `regions{}` block.
7. **4th su example** (Silver Queen, ~92 days) is well cross-referenced by name across all three
   regional variety lists but has no T1-pinned DTM number — optional addition, flagged as not
   T1-precise.
