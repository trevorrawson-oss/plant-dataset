# popcorn -- T1 sourcing table

**Crop:** `popcorn` (Popcorn, *Zea mays* var. *everta*)
**Arc:** `popcorn_gs_arc` (corn family Task 3), authored 2026-07-15.
**Method:** cloned the certified `sweet-corn` warm_season_grass section-E shell (same species, so
thresholds / companions / pests / diseases / soil / watering / block-planting carry over unchanged) and
re-pointed it to a single full-season POPCORN crop grown to a dry-down and then cured to popping moisture.
All cited source IDs resolve to the live `source_catalog` at **tier T1** (university extension / gov).
**0 non-T1 load-bearing sources, 0 uncatalogued.** (whole_crop_gate E: distinct source IDs 14, non-T1 0.)

## Source catalog (all T1) + the URLs cited

| source_id | tier | publisher | URL(s) cited on popcorn |
|---|---|---|---|
| iastate_ext | T1 | Iowa State Ext. | .../how-to/growing-and-harvesting-popcorn-home-garden (300 ft) ; .../how-to/growing-sweet-corn-home-garden (14-day tassel stagger) ; .../faq/can-sweet-corn-be-planted-near-popcorn-garden |
| umn_ext | T1 | UMN Ext. | .../vegetables/growing-popcorn |
| unl_ext | T1 | UNL Ext. | heat-disrupts-corn-pollination ; g1850 (carried Zea mays biology) |
| ncsu_ext | T1 | NC State Ext. | organic-sweet-corn-production (carried corn biology) |
| cornell_ext | T1 | Cornell CCE | crop.php?id=34 (northern region) |
| uga_b577 | T1 | UGA Ext. | B577 planting chart (se_gulf) |
| ucanr_ext_mg_timeplanting | T1 | UC ANR | time-planting (CA regions) |
| nmsu_ext_cr457b | T1 | NMSU Ext. | CR-457-B (warm_arid) |
| tamu_agrilife | T1 | Texas A&M AgriLife | EHT-044 ; RGV Homeowner Vegetable Guide 2022 |
| uariz_ext_az1005 | T1 | U. Arizona CE | AZ1005 low-desert planting calendar |
| uf_ifas_vh021 | T1 | UF/IFAS | SP103/VH021 FL Vegetable Gardening Guide |
| uhawaii_ctahr | T1 | U. Hawaii CTAHR | corn2003.pdf |
| osu_ext | T1 | Oregon State Ext. | Willamette Valley home vegetable guide |
| wsu_ext | T1 | WSU Ext. | Home Vegetable Gardening in Washington |

## Load-bearing claim -> source

### Crop biology / harvest (the popcorn deltas)
| Claim | Source(s) |
|---|---|
| Popcorn grown to full dry maturity; let kernels dry on the ears in the field as long as possible, kernels hard and husks/shank completely dry at harvest; then shuck, bag in mesh, and hang in a warm, dry, well-ventilated place to finish drying | iastate_ext (popcorn home garden), umn_ext (growing-popcorn) |
| **Ideal moisture content for popping is 13 to 14 percent** ("If the kernels get too dry, they will not pop as well"; too wet = chewy/jagged pops); test-pop a sample once or twice a week before shelling the whole crop | iastate_ext, umn_ext (both state 13-14% verbatim) |
| Popping MECHANISM (hard hull + sealed moisture flashes to steam, kernel turns inside out) is general food-science, described in prose; the load-bearing NUMBER (13-14%) is the sourced fact | iastate_ext, umn_ext |
| Cross-pollination: **"If field corn or sweet corn pollinate popcorn, it may not pop well after harvest"**; do not plant sweet corn in the same garden as popcorn | umn_ext, iastate_ext (popcorn home garden + near-popcorn FAQ) |
| Cross-pollination ISOLATION DISTANCE: **"at least 300 feet"** between the types | **iastate_ext** (popcorn home garden, "at least 300 feet between the types") + **umn_ext** (growing-popcorn, "300 feet from the nearest cornfield") -- both popcorn-specific pages verbatim |
| Cross-pollination TASSEL-STAGGER alternative: ~2 weeks / "a minimum of 14 days should separate the tasseling time" (the practical home-garden lever) | iastate_ext (growing-sweet-corn-home-garden, "14 days" verbatim); umn_ext popcorn adds "wait three weeks"; iastate_ext near-popcorn FAQ ("tassel at different times") |
| Block planting for wind pollination: "Always plant corn in blocks of at least four rows" | umn_ext |
| Storage: sealed, airtight containers "to prevent it from drying out further"; retains popping quality for several years if stored properly | iastate_ext, umn_ext |
| Cold/wet soil below 60F rots seed / imbibitional chilling; sow when soil >= 60F | iastate_ext (carried from sweet-corn) |
| Heat over 95F at tasseling/silking kills pollen + desiccates silks (critical moisture window) | unl_ext, umn_ext (carried) |

### Varieties (LEGACY shape; NOT in variety_detail_gate scope -- no maturity_class)
All four rows are named with their DTM in the **Iowa State home-garden popcorn variety table** (T1).

| Variety | DTM | Source | Note |
|---|---|---|---|
| Tom Thumb | 85 | iastate_ext | Early dwarf for short seasons / small gardens; finishes where a full-season type will not. |
| Robust R128YH | 103 | iastate_ext | Dependable modern yellow hybrid, high popping expansion, butterfly-flake type (the everyday snacking popcorn). |
| Gourmet Mushroom | 103 | iastate_ext | Mushroom-type hybrid, pops into dense round balls that hold caramel/coatings. |
| Strawberry De-Lite | 98 | iastate_ext | Ornamental strawberry popcorn (deep-red strawberry-shaped ears) that still pops into small tender flakes. |

**Japanese Hulless** and **Dakota Black** (the two brief-named classics) are named in the description +
variety-note **prose only**: they are seed-trade heirlooms/ornamentals with **no T1 extension DTM**
(they did not resolve to any university extension source this session), so they are not carried as
sourced variety rows. Robust (T1) and Strawberry ornamental (T1) cover the brief's other two named types.

### Regional calendars (12 regions, single-crop dry-down, Option C all-plantable)
Frost anchors + plant windows inherit from the certified sweet-corn corn calendars (same species, same
regional frost model); each region keeps its corn source. The **harvest windows are a synthesis**: the
sweet-corn milk-stage pick shifted later to the 90-110 day dry-down (mid 100), using the single-crop
dry-down window pattern proven on the certified dry-bean sibling. Maturity offset is ~10 days shorter than
field-corn (popcorn mid 100 vs dent mid 110).

| Region | T1 source(s) | popcorn treatment |
|---|---|---|
| northern_tier | umn_ext, cornell_ext | frost-capped; z3 marginal (early-dwarf advisory) |
| se_gulf | uga_b577 | spring sow -> summer dry-down; humid finish advisory |
| ca_interior | ucanr_ext_mg_timeplanting | long dry season, field-dries on stalk |
| ca_north_coast | ucanr_ext_mg_timeplanting | cool/foggy, earlier variety |
| ca_south_coast | ucanr_ext_mg_timeplanting | mild, largely dry finish |
| ca_desert | ucanr_ext_mg_timeplanting (+ unl_ext for heat_pause) | early-only spring, heat_pause [6,7,8] |
| warm_arid | nmsu_ext_cr457b, tamu_agrilife | irrigated late-spring -> fall dry-down |
| low_desert_az | uariz_ext_az1005 | early-only spring, heat_pause [6,7] |
| fl_peninsula | uf_ifas_vh021 | cool-dry-season crop, heat_pause [6,7,8,9], humid advisory |
| hawaii_tropical | uhawaii_ctahr | year-round, humid finish advisory |
| rgv | tamu_agrilife | late-winter sow before summer; season_over off-season; humid advisory |
| pnw | osu_ext, wsu_ext | cool maritime, early variety, damp-finish advisory |

### Thresholds (unchanged from sweet-corn; same species Zea mays)
`germination_temp_f [60,90]`, `heat_threshold_f`, `frost_tolerance_f`, `chilling_sensitivity_f`, soil, pH,
fertilizer, watering critical window, spacing/sow-depth: carried over from sweet-corn's sourced values
(umn_ext, iastate_ext, unl_ext, tamu_agrilife). No popcorn source contradicts them.

## Provisional / flagged for the promote gate
- **days_to_maturity [90,110] mid 100 is PROVISIONAL** -- a synthesis (Trevor ratifies at the promote gate).
  No single T1 quotes the exact band; it is built from the Iowa State home-garden variety table (85 to 112
  days across the listed types) and UMN's "most varieties require 90 to 120 days to reach full maturity."
  `dtm_anchor = from_sow`.
- Regional **harvest month strings** are synthesized (sweet-corn calendar + the ~90-110 day maturity + the
  dry-bean single-crop dry-down pattern), not lifted verbatim from a per-region popcorn table.
- Desert cells (ca_desert, low_desert_az) and short-season northern z3 are **marginal, early-only**; kept
  plantable (Option C) with an honest advisory noting an early dwarf (Tom Thumb) helps.

## Isolation-distance resolution (content-review fix 2026-07-15: 250 -> 300 ft)
Three T1 figures exist for corn cross-pollination isolation:
- Iowa State **popcorn-specific** page: **"at least 300 feet between the types."**
- UMN **growing-popcorn**: **"300 feet from the nearest cornfield"** + "Wait three weeks before planting the sweet corn."
- Iowa State **sweet-corn home-garden** guide: "at least 250 feet apart" + "a minimum of 14 days should separate
  the tasseling time."

**Resolution (used):** popcorn is the most cross-pollination-sensitive corn (the victim; any foreign pollen,
sweet or dent, keeps it from popping), and BOTH popcorn-specific T1 sources agree on **300 ft**, so the
isolation DISTANCE is set to **"at least 300 feet" cited to iastate_ext (popcorn page) + umn_ext (popcorn
page)** -- not the laxer 250 ft from the sweet-corn guide (which would have been internally inconsistent, since
the ISU popcorn page is already cited here for moisture + varieties). The practical home-garden **tassel-stagger
alternative (~2 weeks)** is kept: the specific 14-day figure is verbatim in the ISU sweet-corn home-garden
guide, and UMN popcorn independently recommends a ~3-week stagger. The MECHANISM (sweet or dent pollen keeps
popcorn from popping) is backed by umn_ext popcorn + the iastate near-popcorn FAQ. NCSU's stricter 300 yards
(commercial) is not used. Applied to: description_beginner/seasoned, tips_by_stage.seedling isolation tip
(source/anchor moved from the sweet-corn guide to the two popcorn pages), failure_diagnostics popcorn_wont_pop,
and the verification_log.

**Non-T1 load-bearing sources: 0.**
