# Utah "Dixie" region -- per-archetype cell contract (the column contract)

The authoritative `regions.utah_dixie` cell template Tasks 4-8 author against. **Utah is Nevada's
near-twin**: the on-disk Nevada staging cells (`tools/staging/nevada_*.json`) are the STRUCTURAL
DONORS. Author each Utah cell by taking the crop's Nevada cell, **collapsing the 3 zones to the single
zone `"8"`**, **re-anchoring the windows to USU St. George dates** (the `utah_dixie_sources.md` note),
and **applying the three deltas**. Windows are re-authored from USU, not transformed blindly.

## Region-constant fields (every cell, every class)
- `region_id = "utah_dixie"`
- `region_label = "Utah: St. George Dixie (Mojave-edge high desert)"`
- `zone_span = ["8"]`  (SINGLE zone; A45 single-zone parity)
- `resolved_by_zone` has **EXACTLY the one key `"8"`** (A45 span<->key parity; a stray `"9"`/`"10"` key bounces).
- Per-zone frost anchor: `resolution_method = "frost_anchored_resolved"`,
  `resolved_from = {"last_frost": "Mar 30", "first_frost": "Nov 1"}` (USU Washington County actual-record, St. George).
- `sources` + `anchoring_urls` cite the USU pages (per `utah_dixie_sources.md`), `verified` `2026-07-22`.
- `plantings` non-empty (frost_model=anchored REQUIRES a non-empty `plantings[]` + `frost_anchored_resolved` -- the Nevada allium gotcha).
- Dual-register `region_notes_beginner` / `region_notes_seasoned`, house voice, **NO em dashes**, temps as the `°F` glyph (never "90 degrees").

## THE THREE DELTAS (author these deliberately)
- **4a warm annuals:** single spring window + summer `heat_pause` (**months Jun-Aug = [6,7,8]**, USU >90-95°F blossom/fruit-set abort; SOURCE it) + **NO `second_planting`** (USU St. George fall guidance is cool-season only) + `cold_pause` winter (frost Nov 1). **NO early-Feb indoor-start trick** -- a late-Feb `start_indoors` (~6 weeks before the ~Apr 1 transplant) + Mar 30 frost leaves January naturally inactive. VERIFY the derived tail: Jan-Feb `cold_pause`, spring cycle, Jun-Aug `heat_pause`, then `season_over`/light-fall-harvest, then Nov-Dec `cold_pause`.
- **4b apple + pear-asian + pear-european = `marginal`:** the Washington County "Fruits" elevation split is the direct suitability authority (apple/pear are the county's higher-elevation-only crops). Region-level `chill_basis_seasoned`/`chill_basis_beginner` name the lowest-chill third that crops (Dorsett Golden 100, Anna 200, Ein Shemer 100) and state the county recommends apple only for its higher-elevation towns (5,300+ ft, outside the z8 belt). pawpaw `unsuitable`.
- **4c raspberry + blackberry `marginal`:** fall-bearing/low-chill prose steer; MIRROR the existing `warm_arid` raspberry `region_notes_seasoned` (verbatim template below). strawberry a low-elevation THRIVER. blueberry very-marginal (alkaline, container-only honesty).

---

## 1. Warm-season annual cell (single spring, Shapes A/B/C/D)
Donor: `cherry-tomato nevada` (Shape A). z-cell keys: `plant_out`, `start_indoors`, `harvest`,
`harvest_start`, `harvest_end`, `first_plant_date`, `last_plant_date`, `notes`, `zone_notes`,
`planting_note`, `sources`, `anchoring_urls`, `resolution_method`, `resolved_from`, `heat_pause`,
`calendar`. Deltas from the Nevada donor:
- `start_indoors` **late Feb** (no early-Feb workaround); `plant_out` **~Apr 1** (USU Group D; later than Nevada's mid-March).
- `heat_pause.months = [6,7,8]` (Jun-Aug; Nevada used [7,8,9]). `basis_seasoned`/`basis_beginner` cite the USU tomato/frost pages.
- **Shape A** (tomato/pepper/eggplant): single spring + heat_pause + NO fall. `calendar[]` ~ `[cold_pause, cold_pause, indoors, plant, growing, harvest, heat_pause, heat_pause, heat_pause, season_over, cold_pause, cold_pause]` (DERIVE + inspect per crop).
- **Shape B** (bush-bean/sweet-corn/cucumber/summer-squash): spring + a quick mid-summer replant ONLY IF USU's planting-date table shows a second St. George window; else single spring. (Verify in Task 4.)
- **Shape C** (okra/sweet-potato/melons/winter-squash/pumpkin/dry-corn/dry-bean/pole-bean): single long heat-lover season, **NO heat_pause** (they set through the heat).
- **Shape D** (basil/lemongrass + warm flowers cosmos/marigold/nasturtium/sunflower/zinnia): warm-herb/flower shape.
- `calendar[]` DERIVED by `annual_calendar.derive_annual_calendar(cell)`; set to the derived array; assert the honest tail (NO phantom fall `plant`/`growing`; Nov-Dec `cold_pause`).

## 2. Cool-season annual cell (two-window, Shapes E/F)
Donor: `lettuce-leaf nevada` (Shape E) + `garlic`/`onion nevada` (Shape F). Built with
`second_cycle.build_two_cycle_cell(base, spring, fall)` (combine-derive-then-split; A43 single-span +
envelope-inside). Spring (Feb-Apr) + fall (**USU St. George fall cool-season window**, Heflebower "Fall
Gardening in the St. George Area": broccoli/cabbage/cauliflower/lettuce/carrots/spinach/onions/turnips/
beets), summer `heat_pause` between, `cold_pause` winter.
- **Shape F alliums (delta 4d):** onion/shallot a single FALL `plant_out` (no spring), `recommended_day_length_type = "intermediate_day"` (St. George ~37°N; source it) -> A9 window-fit satisfied by construction (VERIFY A9 = 0). Shallot "follows onion." **Garlic** a single FALL clove `plant_out` per USU's St. George window (source the exact dates; do NOT inherit warm_arid/low_desert_az verbatim).

## 3. Tree cell (chill-gated)
Donor: `apple`/`peach nevada` tree cells. Region-level `chill_basis_seasoned`/`chill_basis_beginner`
(prose lives at REGION level, not per-zone). z-cell keys: `plant_out`, `resolution_method`,
`suitability`, `suitability_note_seasoned`/`_beginner`, `bloom`, `harvest_start`, `harvest_end`,
`harvest`, `calendar`, `frost_risk_note_seasoned`, `resolved_from`, `sources`, `anchoring_urls`.
- **apple + pear-asian + pear-european: `suitability="marginal"`** (delta 4b). Region `chill_basis_*`:
  the honest lowest-chill-third steer (see the delta text above). Cite the Washington County "Fruits" page.
- **Low-elevation column `fruits_reliably`:** apricot, cherry-sour, cherry-sweet, fig, mulberry,
  nectarine, peach, persimmon, plum, pomegranate. Re-judged arid (late frost + sunburn, not humid
  brown-rot); low-chill variety steer in `chill_basis_*` where nominal chill is high (peach).
- **pawpaw `unsuitable`** (humid-forest tree, dry alkaline Mojave mismatch).
- A3 (`perennial_gate`): `fruits_reliably` needs a calendar; `marginal`/`unsuitable` handled (the mid-Atlantic/mid-South marginal-tree precedent).

## 4. Citrus cell (cold-limited)
Donor: `orange-navel nevada`. `suitability="survives"`/`"unsuitable"`, `min_winter_temp_f`,
`cold_basis_{seasoned,beginner}`. St. George is a cold-limited desert winter (colder than Phoenix);
mandarin least bad, lime/grapefruit worst. A32-exempt; minimal calendar.

## 5. Berry / woody-herb / strawberry cell
Donor: `nevada_perennials.json`. Real frost-anchored calendars (A32 applies).
- **Woody herbs** (lavender/oregano/rosemary/sage/thyme): desert-STRONG; summer is the growing season.
- **raspberry (delta 4c):** `marginal`, fall-bearing/low-chill steer. MIRROR this `warm_arid` text:
  > `region_notes_seasoned`: "The warm arid interior is variable: higher elevations with real chill grow raspberries well, while hot, low, alkaline-soil sites are marginal and need heat-tolerant, low-chill everbearing types. Plant dormant in late winter, amend alkaline soils with organic matter, watch for iron chlorosis, mulch the shallow roots, and irrigate steadily through the dry heat."

  Re-cast for St. George (name Bababerry/Dorman Red/Caroline/Autumn Bliss/Heritage/Anne as the primocane/fall-bearing types; cite USU "Raspberry Management for Utah" naming "Utah's Dixie"). blackberry `marginal` (county higher-elevation column). blueberry very-marginal (alkaline, container-only). elderberry marginal. Berries carry no suitability field -> honesty in prose.
- **strawberry (delta 4c):** a low-elevation THRIVER (USU low-elevation "Fruits" column). Real calendar.
