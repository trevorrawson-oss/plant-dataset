# flint-corn -- T1 sourcing table

**Crop:** `flint-corn` (Flint Corn, *Zea mays* var. *indurata*)
**Arc:** `flint_corn_gs_arc` (corn family Task 4), authored 2026-07-15.
**Method:** cloned the certified `sweet-corn` warm_season_grass section-E shell via the proven `field-corn`
dry-down template (same species + identical dry-down transform: 9-stage ladder, `harvest_window_days` omitted,
single-crop succession, 12-region Option C) and re-pointed it to a FLINT grain crop: hard, vitreous (flinty)
endosperm that hardens smooth and glassy (no dent), ground into cornmeal / polenta / hominy or grown for color.
All cited source IDs resolve to the live `source_catalog` at **tier T1** (university extension / gov). **0 non-T1
load-bearing sources, 0 uncatalogued.** No new catalog source was needed (all flint facts anchor to existing T1 ids).

## Source catalog (all T1) + the URLs cited on flint-corn

| source_id | tier | publisher | flint-corn use / URL |
|---|---|---|---|
| iastate_ext | T1 | Iowa State Ext. | Growing and Harvesting **Ornamental Corn** (names Painted Mountain + Glass Gem; cornmeal/flour use; harvest at full maturity, husks dry, cure 2-3 wk; and "A minimum of 14 days should separate the tasseling times" verbatim); **Popcorn Home Garden** page ("at least 300 feet between the types") -- the isolation DISTANCE citation; grain dry-down / black layer; imbibitional chilling |
| cornell_ext | T1 | Cornell CCE | Vegetable Varieties for Gardeners: **Painted Mountain** (OP flint, gold/orange/red/purple, **DTM 85**), **Roy's Calais Flint** (heirloom flint for cornmeal, DTM 85-95), names Glass Gem; northern_tier calendars |
| ncsu_ext | T1 | NC State Ext. | **Glass Gem** article (flint/popcorn type, translucent rainbow kernels, **DTM 105-110**, pick when kernels hard+glossy + husk dried, cure several weeks to 13-14.5%); block-planting/isolation; corn earworm |
| clemson_hgic | T1 | Clemson HGIC | dry-corn dry-down + shell + store (Homegrown Grits); storage of dry grain; grind to meal as needed |
| umn_ext | T1 | UMN Ext. | **Growing Popcorn** page ("300 feet from the nearest cornfield") -- the isolation DISTANCE citation; block planting / wind pollination; sidedress N; raccoon fence; pollination moisture |
| unl_ext | T1 | UNL Ext. | heat over 95F disrupts pollination; silking critical-moisture window |
| uga_b577 | T1 | UGA Ext. | se_gulf planting window |
| ucanr_ext_mg_timeplanting | T1 | UC ANR | ca_interior / north_coast / south_coast / desert windows |
| nmsu_ext_cr457b | T1 | NMSU Ext. | warm_arid window |
| tamu_agrilife | T1 | Texas A&M AgriLife | warm_arid + rgv windows |
| uariz_ext_az1005 | T1 | U. Arizona CE | low_desert_az window + heat_pause |
| uf_ifas_vh021 | T1 | UF/IFAS | fl_peninsula cool-dry-season window + heat_pause |
| uhawaii_ctahr | T1 | U. Hawaii CTAHR | hawaii year-round; harvest_ready |
| osu_ext | T1 | Oregon State Ext. | pnw window |
| wsu_ext | T1 | WSU Ext. | pnw window |

**Supporting authorities cited only in this note (NOT in the JSON object, so not gate-checked):** NMSU H-232
"Specialty Corns" ("Kernels of flint corn have mostly hard, glassy endosperms with smooth, hard seed coats");
OSU Agronomic Crops "Specialty Corns"; USDA GIPSA Flint & Dent visual reference; SARE FW08-034 (Dave
Christensen's Painted Mountain / Montana Morado short-season cold-hardy flint). These back the flint-endosperm
and Painted Mountain provenance in the description prose (descriptions carry no gate-anchored `sources` array).

## Load-bearing claim -> source

### Flint biology / harvest (the flint deltas vs field-corn dent)
| Claim | Source(s) |
|---|---|
| Flint corn = hard, vitreous (flinty), glassy endosperm; kernels harden smooth and rounded WITHOUT a dent | NMSU H-232, OSU/agcrops, NCSU (Glass Gem "hard and glossy") -- endosperm stated in note-only authorities + iastate ornamental |
| Uses: cornmeal, polenta, hominy, decorative/ornamental | iastate_ext (ornamental: "ground into cornmeal or flour"), ncsu_ext (popped or ground), clemson_hgic (dry-grain grind) |
| Harvest: ears fully mature, husks dry, kernels hard+glassy, black layer ~30-35% moisture, cure to 13-15% | iastate_ext (ornamental: harvest at full maturity, husks dry, store/cure 2-3 wk), ncsu_ext (hard+glossy, cure several wk, 13-14.5%), clemson_hgic, uhawaii_ctahr |
| Cross-pollination: corn is wind-pollinated so pollen crosses types (sweet corn -> starchy; popcorn -> no pop; flint colors muddied); isolate **at least 300 feet** OR stagger tasseling ~14 days | **iastate_ext** (popcorn home-garden page, "at least 300 feet between the types") + **umn_ext** (growing-popcorn, "300 feet from the nearest cornfield"); the 14-day / 2-week stagger from iastate_ext sweet-corn/ornamental page. See isolation-distance resolution below. |
| Heat over 95F at tasseling/silking kills pollen; silking most drought-sensitive | unl_ext, umn_ext |
| Cold/wet soil rots seed / imbibitional chilling | iastate_ext |

### Varieties (LEGACY shape; NOT in variety_detail_gate scope -- confirmed out of scope, in_scope=5 unchanged)
| Variety | DTM (row) | T1 source (name) | Note |
|---|---|---|---|
| Painted Mountain | 85 | cornell_ext ("DTM 85"), iastate_ext (ornamental) | Short-season, cold-hardy OP flint; gold/orange/red/purple; the reliable pick for short/cold seasons (also SARE FW08-034 Christensen provenance) |
| Glass Gem | 108 | ncsu_ext ("105-110 days"), iastate_ext, cornell_ext (named) | Ornamental rainbow flint/popcorn; DTM synthesized to 108 (mid of NCSU's 105-110); decorative, poppable or grindable |
| Roy's Calais Flint | 90 | cornell_ext ("Heirloom flint corn for cornmeal", DTM 85-95) | Classic Northeastern polenta/cornmeal flint; parent of Cascade Ruby-Gold; DTM synthesized to 90 within Cornell's 85-95 |

**Named in prose only (description + varieties note), NOT carried as sourced rows** -- honest, per clone-hygiene (d)
+ the field-corn precedent (Reid's Yellow Dent / Bloody Butcher): **Floriani Red Flint** (Italian polenta flint,
~100 days; only seed-trade T2 sources, e.g. Fedco Maine trials) and **Cascade Ruby-Gold** (Carol Deppe's early
Northwest polenta flint bred from Roy's Calais x Byron; OSSI + seed-trade T2 only). No catalog T1 names either
directly, so they are not rowed. (A UVM/SARE flint-corn variety evaluation names Floriani but is a PDF that could
not be decoded this session; adding that source to row Floriani is a promote-gate option for Trevor.)

### Regional calendars (12 regions, single-crop dry-down, Option C all-plantable)
Frost anchors + plant windows + harvest windows + calendars are INHERITED unchanged from the certified field-corn
dry-down synthesis (itself derived from the certified sweet-corn corn calendars). Flint's ~90-110 day maturity is
about 10 days shorter than dent, which is **within** the synthesized monthly windows, so the calendars carry over
and stay coherent (calendar_coherence flint-corn 0). Each region keeps its corn source; prose re-pointed to flint.

| Region | T1 source(s) | flint treatment |
|---|---|---|
| northern_tier | umn_ext, cornell_ext | frost-capped; z3 short-season advisory names **Painted Mountain (~85 d)** as the reliable fast flint |
| se_gulf | uga_b577 | spring sow -> summer dry-down; humid finish advisory |
| ca_interior | ucanr_ext_mg_timeplanting | long dry season, field-dries on stalk |
| ca_north_coast | ucanr_ext_mg_timeplanting | cool/foggy, favors an earlier flint (Painted Mountain) |
| ca_south_coast | ucanr_ext_mg_timeplanting | mild, largely dry finish |
| ca_desert | ucanr_ext_mg_timeplanting (+ unl_ext) | early-only spring, heat_pause [6,7,8] |
| warm_arid | nmsu_ext_cr457b, tamu_agrilife | irrigated late-spring -> fall dry-down |
| low_desert_az | uariz_ext_az1005 (+ unl_ext) | early-only spring, heat_pause [6,7] |
| fl_peninsula | uf_ifas_vh021 (+ unl_ext) | cool-dry-season crop, heat_pause [6,7,8,9], humid advisory |
| hawaii_tropical | uhawaii_ctahr | year-round, humid finish advisory |
| rgv | tamu_agrilife | late-winter sow before summer; season_over off-season; humid advisory |
| pnw | osu_ext, wsu_ext | cool maritime, early flint (Painted Mountain), damp-finish advisory |

### Thresholds (unchanged from sweet-corn / field-corn; same species Zea mays)
`germination_temp_f [60,90]`, `heat_threshold_f`, `frost_tolerance_f`, `chilling_sensitivity_f`, soil, pH,
fertilizer, watering critical window, spacing/sow-depth: carried over from the certified corn values
(umn_ext, iastate_ext, unl_ext). No flint source contradicts them. (Painted Mountain tolerates colder spring
soil than the 60F floor; that is noted as a variety/region advisory, not a threshold change.)

## Isolation-distance resolution (content-review fix 2026-07-15: 250 -> 300 ft)
The three corns (flint / dent field / popcorn) cross-pollinate each other, so they must present ONE isolation
figure across the family. Popcorn and field-corn are harmonized to **"at least 300 feet"** cited to the
popcorn-specific T1 pages (iastate popcorn home-garden "at least 300 feet between the types"; UMN growing-popcorn
"300 feet from the nearest cornfield"), popcorn being the shared cross-pollination victim. Flint is bumped from
the well-sourced-but-laxer "at least 250 feet" (iastate ornamental/sweet-corn guide) to **"at least 300 feet"**
cited to those same iastate + umn popcorn pages: 300 ft also satisfies iastate's "at least 250," so it is strictly
compatible with the ornamental-corn source, and it removes the internal inconsistency of showing 250 ft for flint
vs 300 ft for its two siblings. The 14-day / 2-week tassel-stagger alternative (iastate, "a minimum of 14 days
should separate the tasseling times"; UMN popcorn adds a ~3-week stagger) is kept. Only the isolation DISTANCE
changed; plant/row SPACING (spacing_inches [8,12], sow_depth [1,2], thin_to [8,12], pollination_block_min_rows 4)
and the DTM band [90,110]/100 are untouched. Applied to: description_seasoned/beginner, tips_by_stage.seedling
(sources iastate_ext + umn_ext, popcorn URLs), verification_log, and the rows above.

## Provisional / flagged for the promote gate
- **days_to_maturity [90,110] mid 100 is PROVISIONAL** (Trevor ratifies at promote). A synthesis: no single T1
  quotes the exact band. Built from convergent figures -- Painted Mountain ~85 (cornell_ext), Roy's Calais 85-95
  (cornell_ext), Floriani ~100 (seed trade), Glass Gem 105-110 (ncsu_ext). `dtm_anchor = from_sow`.
- **Region plant/harvest windows are INHERITED from the field-corn dry-down synthesis, not per-region shifted for
  flint's ~10-day-shorter DTM.** Rationale: the windows are month-bucketed and the difference is within synthesis
  tolerance; flint's short-season advantage is expressed instead through the Painted Mountain variety guidance in
  the cold/cool-short-season regions. If Trevor prefers per-region date shifts, that is a promote-gate refinement.
- **Floriani Red Flint + Cascade Ruby-Gold are prose-only, not sourced rows** (no catalog T1 names them). Roy's
  Calais Flint (T1, and Cascade's parent) substituted as the third polenta-flint row. Trevor may elect to add a
  UVM/SARE flint-eval catalog source at promote to row Floriani.
- **Glass Gem DTM 108** synthesized as the mid of NCSU's 105-110; **Roy's Calais 90** synthesized within Cornell's
  85-95; **Painted Mountain 85** is Cornell's stated figure (not synthesized).

**Non-T1 load-bearing sources: 0.** whole_crop_gate flint-corn **GATE: PASS** (15 T1, 0 non-T1, 0 uncatalogued,
0 dash, 0 temp-form); calendar_coherence flint-corn 0; timing_spine 0 violations / 0 warnings; variety_detail_gate
flint OUT of scope; canonical `crops_data_final.json` byte-UNCHANGED (sha c73d7fa...).
