# field-corn (dent) -- T1 sourcing table

**Crop:** `field-corn` (Field Corn / dent corn, *Zea mays* var. *indentata*)
**Arc:** `field_corn_gs_arc` (corn family Task 1), authored 2026-07-15.
**Method:** cloned the certified `sweet-corn` warm_season_grass section-E shell (same species, so
thresholds / companions / pests / diseases / soil / watering / block-planting carry over unchanged) and
re-pointed it to a single full-season DENT crop grown to a dry-down grain harvest. All cited source IDs
resolve to the live `source_catalog` at **tier T1** (university extension / gov). **0 non-T1 load-bearing
sources, 0 uncatalogued.**

## Source catalog (all T1) + the URLs cited

| source_id | tier | publisher | URL(s) cited on field-corn |
|---|---|---|---|
| clemson_hgic | T1 | Clemson HGIC | https://hgic.clemson.edu/homegrown-grits/ |
| iastate_ext | T1 | Iowa State Ext. | .../corn-grain-dry-down-field-maturity-harvest ; .../imbibitional-chilling... ; .../growing-sweet-corn-home-garden |
| umn_ext | T1 | UMN Ext. | .../corn-hybrid-selection/selecting-corn-hybrids-grain-production ; .../dry-conditions-during-corn-pollination ; .../vegetables/growing-sweet-corn |
| unl_ext | T1 | UNL Ext. | .../how-extended-high-heat-disrupts-corn-pollination ; .../publication/g1850/2008/html/view |
| ncsu_ext | T1 | NC State Ext. | https://content.ces.ncsu.edu/organic-sweet-corn-production |
| cornell_ext | T1 | Cornell CCE | https://cvp.cce.cornell.edu/crop.php?id=34 |
| uga_b577 | T1 | UGA Ext. | B577 planting chart |
| ucanr_ext_mg_timeplanting | T1 | UC ANR | .../time-planting |
| nmsu_ext_cr457b | T1 | NMSU Ext. | CR-457-B |
| tamu_agrilife | T1 | Texas A&M AgriLife | EHT-044 ; RGV Homeowner Vegetable Guide 2022 |
| uariz_ext_az1005 | T1 | U. Arizona CE | AZ1005 low-desert planting calendar |
| uf_ifas_vh021 | T1 | UF/IFAS | SP103/VH021 FL Vegetable Gardening Guide |
| uhawaii_ctahr | T1 | U. Hawaii CTAHR | corn2003.pdf |
| osu_ext | T1 | Oregon State Ext. | Willamette Valley home vegetable guide |
| wsu_ext | T1 | WSU Ext. | Home Vegetable Gardening in Washington |

## Load-bearing claim -> source

### Crop biology / harvest (the dry-corn deltas)
| Claim | Source(s) |
|---|---|
| Dent corn grown to full dry maturity, ears dry on the stalk, "from 90 to 120 days after planting for most varieties"; harvest when husks are dry/brown/papery; shuck + spread to finish drying indoors (fan speeds it); shell + store the dry grain | clemson_hgic (Homegrown Grits) |
| Black layer = physiological maturity ~30-35% kernel moisture; storage target ~13-15%; in-field drydown ~0.5-1.0%/day Sep, ~0.25-0.5%/day Oct | iastate_ext (corn grain dry-down) |
| Grain-corn variety choice by relative maturity (modern hybrids stand + dry more evenly) | umn_ext (selecting corn hybrids for grain) |
| Cross-pollination MECHANISM: dent pollen crosses sweet corn to starchy kernels + keeps popcorn from popping | iastate_ext, ncsu_ext |
| Cross-pollination ISOLATION FIGURE: "at least 300 feet" apart OR stagger tasseling by ~2 weeks | **iastate_ext** (growing-and-harvesting-popcorn-home-garden: "at least 300 feet"), **umn_ext** (growing-popcorn: "plant popcorn 300 feet from the nearest cornfield" + wait 3 weeks) |
| Heat over 95F at tasseling/silking kills pollen + desiccates silks (critical moisture window) | unl_ext, umn_ext |
| Cold/wet soil below 60F rots seed / imbibitional chilling | iastate_ext |

### Varieties (LEGACY shape; NOT in variety_detail_gate scope -- no maturity_class)
| Variety | DTM | Source | Note |
|---|---|---|---|
| John Haulk (yellow dent, OP) | 115 | clemson_hgic | Southern heirloom grits/cornmeal dent, named in Homegrown Grits; DTM synthesized within Clemson's 90-120 band (tall full-season OP dent). |
| Cocke's Prolific (white dent, OP) | 115 | clemson_hgic | White dent, often >1 ear/stalk, named in Homegrown Grits; DTM synthesized within Clemson's 90-120 band. |
| Grain hybrid (by relative maturity) | 100 | umn_ext | The "buy a modern grain hybrid" option; DTM synthesized as a shorter/faster hybrid within band. |

Reid's Yellow Dent and Bloody Butcher are named in the description **prose only** (well-known examples, no
numeric claim); they are **not** carried as sourced variety rows because a T1 extension DTM could not be
resolved this session (Bloody Butcher 105-110d appears in U. Wisconsin Hort, which is not in the catalog).

### Regional calendars (12 regions, single-crop dry-down, Option C all-plantable)
Frost anchors + plant windows inherit from the certified sweet-corn corn calendars (same species, same
regional frost model); each region keeps its corn source. The **harvest windows are a synthesis**: shifted
later than sweet-corn's milk-stage pick to the 110-120 day grain dry-down, using the single-crop dry-down
window pattern proven on the certified dry-bean sibling.

| Region | T1 source(s) | field-corn treatment |
|---|---|---|
| northern_tier | umn_ext, cornell_ext | frost-capped; z3 marginal (early-only advisory) |
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
(umn_ext, iastate_ext, unl_ext, tamu_agrilife). No dry-corn source contradicts them.

## Provisional / flagged for the promote gate
- **days_to_maturity [95,120] mid 110 is PROVISIONAL** -- a synthesis (Trevor ratifies at the promote gate).
  No single T1 quotes the exact band; it is built from Clemson HGIC "90 to 120 days," Bloody Butcher 105-110d,
  and grain-hybrid relative-maturity ranges. `dtm_anchor = from_sow`.
- Regional **harvest month strings** are synthesized (sweet-corn calendar + the ~110-120 day grain maturity +
  the dry-bean single-crop dry-down pattern), not lifted verbatim from a per-region dry-corn table.
- Desert cells (ca_desert, low_desert_az) are **marginal, early-only**: a full-season dent barely fits the
  cool window before the summer heat pause. Kept plantable (Option C) with an honest advisory.
- Variety DTMs (115/115/100) are synthesized within Clemson's 90-120 band, not individually quoted.

- **Cross-poll isolation distance = "at least 300 feet" (2026-07-15 review fixes):** first re-anchored off the
  clone's wrong ncsu_ext attribution (NCSU's primary figure is the stricter "at least 300 yards"); then
  **harmonized 250 ft -> 300 ft** for corn-family consistency -- popcorn (the cross-poll victim) is set to
  "at least 300 feet" per its popcorn-specific sources, and the three corn types cross-pollinate each other,
  so field-corn recommending a shorter separation than popcorn would contradict across the family. The
  conservative 300 ft is now cited to **iastate_ext** (Growing and Harvesting Popcorn in the Home Garden:
  "at least 300 feet") + **umn_ext** (Growing popcorn: "plant popcorn 300 feet from the nearest cornfield").
  The ~2-week tassel-stagger alternative is kept (both popcorn pages offer a time-based alternative; umn says
  "wait three weeks"). ncsu_ext still backs the mechanism (starchy / no-pop).

**Non-T1 load-bearing sources: 0.**
