# Blueberry / `berries_woody` model -- design

**Date:** 2026-06-22
**Author:** Claude Code (structural lane)
**Status:** Approved design (Trevor, 2026-06-22). Spec review + implementation plan next.
**Milestone:** Blueberry gold-standard arc (anchor 18). Blueberry is the FIRST `berries_woody` crop -- and the ONLY one in the dataset at anchor time -- so this is the archetype's whole schema stress-test, not yet a template for a family (though it is the intended template for the other woody fruiting shrubs: raspberry/blackberry/currant/gooseberry/grape later).
**Reads against:** gold-standard arc checklist v2.0; `tools/build_region_shells.py` (the tree + `_build_berry_herbaceous_shells` precedents); `tools/whole_crop_gate.py` (the off-branch-safe A-section pattern -- A6/A8/A9/A10/A11/A13/A14); `tools/perennial_gate.py` + `tools/tree_calendar.py` (the chill-gated tree cert + derive-the-calendar precedents); `tools/photoperiod_gate.py` (onion A9 -- the per-cell-type + coverage-invariant precedent reused here); the strawberry `berries_herbaceous` design (the nearest sibling -- the per-cell-lifecycle + derive-the-calendar + new-A-section pattern) and the lavender `perennial_woody_ornamental` design (the woody perennial precedent: `nursery_transplant`, the `prune` token, woody care beats).
**Start SHA:** `196172a2d226c6d71b7f88b8d8ba78825edd3b1e6c9315edab73bb9f01b711b5` (canonical content SHA; must equal `LATEST.txt` at apply time -- Step 0 preflight). Blueberry shell crop SHA at design time: `e2e27dcb...` (archetype `berries_woody` already set, `calendar_basis frost_anchored` wipe default, lifecycle `permanent`, 10 region shells).

---

## 1. Problem

Blueberry does not fit any certified archetype, for four compounding reasons:

1. **It is a woody fruiting SHRUB, not an annual, not a tree, not a herbaceous perennial.** A planted bush runs a recurring woody cycle (dormant -> bloom -> fruit -> summer growth -> dormant) over a multi-decade lifespan. The annual "plant -> grow -> harvest -> `season_over`" calendar is a category error; the strawberry herbaceous "renovate every 3-4 years" model is wrong (a blueberry is planted once and lives 20-50 years); and it carries none of the tree machinery (rootstock/grafting -- blueberries are own-root; the single-trunk tree shape).

2. **The TYPE you can grow is chill-gated by region.** Three types -- **northern highbush** (high chill ~800-1000h, cold zones), **southern highbush** (low chill ~150-600h, warm zones), **rabbiteye** (low-moderate chill ~350-600h, warm/vigorous) -- and chill genuinely GATES them: a high-chill northern type gets too little winter cold in the South (erratic bloom, no crop); a low-chill southern type blooms too early and frost-kills in the North. This is the #1 home-grower failure. Unlike strawberry's June-bearing/day-neutral (both work at one latitude = a grower's choice), blueberry's type is region-DICTATED, closer to onion's photoperiod gate and the tree chill model.

3. **The calendar SHAPE itself splits North/South.** Northern highbush is deciduous (drops leaves, true winter dormancy, like a peach); southern highbush and rabbiteye in the warm South are semi-evergreen to evergreen (no real dormancy). One crop spans both -- exactly the two-axis split the fruit trees handle as `perennial_chill_gated` (deciduous) vs `perennial_evergreen` (citrus).

4. **Acid soil is a hard, defining requirement no other crop shares.** Blueberries need soil pH ~4.5-5.5 -- far below the 6.0-7.0 of nearly every other crop. In ordinary garden soil they develop iron chlorosis, stunt, and die. Deliberate acidification (elemental sulfur / peat) before planting and maintained after is make-or-break, and the classic beginner trap.

There is **zero woody-fruiting-shrub modeling in the dataset today.** Blueberry is the anchor precisely because getting it honest forces the schema to express a crop whose growable TYPE and calendar SHAPE both vary by region, on a multi-decade woody perennial.

**Product decision (Trevor, 2026-06-22): one guide, type-neutral spine, the type choice elevated + region-resolved.** `blueberry` stays a single crop at one URL. Crop-level content carries the type-NEUTRAL universal care (acid soil, cross-pollination, pruning, harvest, longevity). The "which type should you grow?" decision is an elevated dual-register section (the chill-match teaching), and the ACTUAL recommended type + calendar resolve PER REGION CELL -- because here the type genuinely IS region-determined (the inverse of strawberry, where it was a free choice anchored on one spine). No per-type pages, no per-type calendar toggle.

---

## 2. Decisions

**D1 -- Chill-gated type model (`gating_factors: ["chill_hours"]`).** The type axis is a real per-region gate, modeled on onion's photoperiod (A9) + the tree chill model, NOT strawberry's free type choice. Crop-level `gating_factors: ["chill_hours"]`. Each resolved cell carries `recommended_type in {northern_highbush, southern_highbush, rabbiteye}` + `chill_hours_delivered`. A coverage invariant (the gate, Section 4): every `recommended_type` that appears in a resolved cell has >= 1 matching variety in the recommended set, and the recommended set is honest about which types the page teaches. **Lowbush is NOT a 4th type (Trevor, 2026-06-22):** lowbush is a wild/commercial barren crop, not a backyard shrub; the far-north (z3-4) answer is cold-hardy northern highbush + the "half-high" (highbush x lowbush) cultivars, carried as `northern_highbush` varieties + a prose note, not a separate type.

**D2 -- New `calendar_basis` value `berries_woody` + per-cell `leaf_habit`.** Frost resolution stays **ON** (bloom/harvest windows anchor to frost dates; resolver math, frost reconcile, `zone_frost_data` usage unchanged). The basis is a SHAPE/semantic signal next to `perennial_chill_gated`/`perennial_evergreen`/`perennial_herbaceous`/`perennial_woody_ornamental`. A per-cell **`leaf_habit` in {deciduous, evergreen}** selects the calendar shape (the woody analog of strawberry's `grown_as` and the tree `suitability`): northern/cold cells = `deciduous` (true winter dormancy), warm-South cells = `evergreen` (no dormancy). Set by `build_region_shells` at Step 3.5 (flips the `frost_anchored` wipe default).

**D3 -- Calendar vocab: REUSE the tree tokens, no new token.** Deciduous cells use the tree cyclic vocab: `dormant` (leafless winter chill-banking), `prune` (the dormant-season pruning month -- the month-collision rule: a dormant month that is also the prune window renders `prune`), `bloom`, `growing`, `harvest`, `care`. Evergreen cells use `growing`/`bloom`/`harvest`/`care` with NO `dormant` and NO `season_over` (the citrus/evergreen analog: frost-free -> growing year-round). The HARD rule (the gate's teeth): a `deciduous` cell carries the `dormant` cycle and NEVER `season_over`; an `evergreen` cell carries no `dormant` and no `season_over`. One crop, two calendar shapes, selected by `leaf_habit`. No `renovation` token (that is strawberry's herbaceous-only); no new token is minted for blueberry.

**D4 -- Cross-pollination: light model (`self_fertile: false`), no apple machinery.** The universal blueberry advice is "plant 2+ different cultivars of the same type with overlapping bloom." Crop-level `self_fertile: false` + a dual-register `pollinator_notes_seasoned`/`_beginner` carrying the gradient (rabbiteye REQUIRES a second cultivar for any crop; highbush is partially self-fertile but yields far better, larger, earlier with cross-pollination). The recommended-variety set lists >= 2 cultivars per type the page teaches. **NO** `bloom_group`/`pollinizer`/`bloom_window` machinery (apple's specific A-pollinates-B precision is more than blueberry's "any two of the same type, overlapping bloom" needs). The gate (Section 4) defensively asserts `self_fertile == false` AND no variety carries pollinizer fields.

**D5 -- Acid soil is an ELEVATED care beat, not just a scalar (Trevor, 2026-06-22).** `ph`: preferred `[4.5, 5.5]`, tolerated ~`[4.0, 5.5]` (sourced at Step 5). Beyond the scalar, soil acidification gets prominent dual-register treatment -- a make-or-break "test your soil, and acidify with elemental sulfur / incorporate peat before planting; maintain with an acidifying (ammonium-sulfate) fertilizer" beat (in the soil/`ph` prose + a growth-stage/notification beat) -- AND a `failure_diagnostics` entry for high-pH iron chlorosis (yellowing leaves with green veins, stunting). It is the #1 blueberry failure, so it is surfaced front-and-center rather than buried. (This is a prose/authoring elevation, NOT a new structural field -- the `ph` block + the standard prose compounds carry it.)

**D6 -- Lifecycle: long-lived woody perennial, plant-once; `start_method.start = "nursery_transplant"`.** Uses the existing 2.9 lifecycle scaffold (no new fields). Crop-level: `lifecycle: permanent`, `perennial: true`, `establishment_years ~2-3` (to first real harvest -- pick off the first 1-2 years' bloom to build the bush), `years_to_full_production ~6-8`, `productive_lifespan_years` decades (20-50). Planted ONCE, not replaced (the strawberry "renovate every 3-4 years" model does NOT apply -- blueberry has no `renovation`). `start_method.start = "nursery_transplant"` (the lavender value): a container-grown nursery plant (the common backyard purchase, 1-3 yr old) or dormant bare-root (mail-order) -- both in prose; NOT seed (too slow/variable), NOT grafted (own-root). The window is a `plant_out`-only setting window, frost-anchored, more flexible than bare-root-only (containers can go spring or fall).

**D7 -- Type lives on varieties + one elevated explainer; the per-cell type is the gate's authority.** `varieties.recommended[]` become objects carrying `type in {northern_highbush, southern_highbush, rabbiteye}` (half-high cold-hardy cultivars ride as `northern_highbush` + a `hardiness_note`). A single crop-level dual-register pair `type_selection_seasoned`/`_beginner` holds the "which type for your region/chill?" teaching the renderer surfaces near the top (CP class, auto-covered by the register gates). Chill is a real `gating_factor` (D1) AND carries informational prose (`chill_hours_note_*`); the per-cell `recommended_type` is the rendered regional answer, the variety `type` tags are what the coverage gate checks against. Cultivars-WITHIN-a-type are clean Phase-5 deltas (Section 8).

**D8 -- A new cert-gate branch `berries_woody_violations(crop)` + a `berry_woody_calendar` deriver + a `build_region_shells` path.** Test-first, wired into `whole_crop_gate` as the next free A-section (no-op unless `calendar_basis == "berries_woody"`), consistent with how A6/A8/A9/A10/A11/A13/A14 were added off-branch-safe. The deriver computes each `calendar[]` from the resolved windows + `leaf_habit` (the tree/berry/woody-ornamental derive-the-calendar precedent), never hand-typed. `build_region_shells._build_berry_woody_shells` builds the 10 cells to shape at Step 3.5. These are the teeth of the model (Section 4).

---

## 3. Schema

### 3a. Crop level
```
"calendar_basis": "berries_woody",          // set by build_region_shells at 3.5
"archetype": "berries_woody",               // already set
"lifecycle": "permanent",   "perennial": true,
"gating_factors": ["chill_hours"],          // D1 -- the real gate (cf. onion photoperiod / tree chill)
"self_fertile": false,                      // D4
"start_method": { "start": "nursery_transplant", "weeks_before": null,
                  "hardening_off_seasoned": <N/A prose>, "hardening_off_beginner": <N/A prose>,
                  "notes_seasoned": "<container most common; dormant bare-root mail-order; set at the nursery soil line in well-drained ACID soil>", "notes_beginner": "<...>" },
"establishment_years": <~2-3>,              "years_to_first_harvest": [...],
"years_to_full_production": [...],          "productive_lifespan_years": <~20-50>,
"establishment_note": "<universal: pick off bloom the first 1-2 years to build the bush>",
"type_selection_seasoned": "<which type by chill/region + why>", "type_selection_beginner": "<...>",  // NEW CP pair (D7)
"chill_hours_required": <int|null>, "chill_hours_range": [...], "chill_hours_note_*": "<informational + the gate basis>",
"bloom_time_*": "<...>", "bloom_duration_days": <int|null>,
"pollinator_notes_seasoned": "<plant 2+ cultivars of the SAME type, overlapping bloom; rabbiteye requires it, highbush yields far better with it>", "pollinator_notes_beginner": "<...>",
"ph": { "preferred_range": [4.5, 5.5], "tolerated_range": [~4.0, 5.5], "note_seasoned": "<acidify BEFORE planting: sulfur/peat; the make-or-break>", "note_beginner": "<...>", "sources": [...], "anchoring_urls": {...} },
"hardiness_zone_min/max": <survives>, "reliable_fruit_zone_min/max": <fruits well>,
"succession_policy": { "suitable": false, ... }
```
`hardiness` (survives) and `reliable_fruit` (fruits well) stay distinct crop-level scalars. There is no per-cell `suitability` verdict (the per-cell story is `recommended_type` + `leaf_habit` + the calendar). NO rootstock / grafting / `bloom_group` / `pollinizer` fields.

### 3b. Variety level (`varieties.recommended[]`, objects)
```
{ "name": "Duke", "type": "northern_highbush", "chill_hours": "~800-1000", "season": "early",
  "use": "fresh + freezing", "hardiness_note": "z4-7; reliable cold-zone highbush",
  "note": "<a productive early northern highbush for cold-winter gardens>" }
{ "name": "Emerald", "type": "southern_highbush", "chill_hours": "~250", "season": "early",
  "use": "fresh", "note": "<a low-chill southern highbush for mild-winter gardens>" }
{ "name": "Powderblue", "type": "rabbiteye", "chill_hours": "~550", "season": "late",
  "use": "fresh + processing", "note": "<a vigorous, productive rabbiteye; needs a second rabbiteye nearby>" }
```
`type in {northern_highbush, southern_highbush, rabbiteye}`. Half-high cold-hardy cultivars (Northblue/Patriot) ride as `northern_highbush` + a `hardiness_note`. The recommended set spans the types the page teaches AND satisfies the coverage invariant (every per-cell `recommended_type` has a match). NO `bloom_group`/`pollinizer`/`bloom_window` (self-fertile false, D4).

### 3c. Region / zone cell
Region-constant: `recommended_type` + `leaf_habit` (authored per region, a SOURCE finding), one `plantings[]` nursery-setting establishment window (`plant_out` rule list; NO `succession`, `second_planting`, `start_indoors`, `direct_sow`), `region_notes_*`.
Per resolved cell (`resolved_by_zone.<zone>`):
```
"recommended_type": "rabbiteye",               // D1 -- the gate's per-cell authority
"leaf_habit": "evergreen",                     // or "deciduous" (D2) -- selects the calendar shape
"chill_hours_delivered": <int|range>,          // the region's chill (the gate basis)
"plant_out": "<nursery-setting window>", "bloom": "<...>", "harvest_start": "<...>", "harvest_end": "<...>",
"calendar": [ ... ],                           // DERIVED from leaf_habit + windows (D8), never hand-typed
"type_note_seasoned": "<why this type here -- chill>", "type_note_beginner": "<...>",
"frost_risk_note_seasoned": "<late frost on open bloom -- the low-chill-south risk>",
"resolved_from": { "last_frost": "...", "first_frost": "..." }, "resolution_method": "berries_woody_precompute"
```
A `deciduous` cell's `calendar[]` carries the `dormant`+`prune` cycle (never `season_over`); an `evergreen` cell's carries `growing`/`bloom`/`harvest` (no `dormant`, no `season_over`). STRIP tree keys (`suitability`, `chill_hours_delivered` is KEPT here as the gate basis but `rootstock`/pollinizer never appear). The `calendar[]` is GENERATED (D8), never hand-typed.

---

## 4. The gate -- `berries_woody_violations(crop)` (whole_crop_gate, next free A-section)

No-op unless `calendar_basis == "berries_woody"`. Otherwise returns a list of violation strings (`[]` = pass). Asserts:

1. **Lifecycle + chill fields present.** `establishment_years`, `years_to_first_harvest`, `years_to_full_production`, `productive_lifespan_years`, `type_selection_*`, `pollinator_notes_*`, `chill_hours_note_*` non-null (register-fill checks the prose pairs; this asserts the woody-specific set as a backstop). `gating_factors` contains `"chill_hours"`.
2. **Per-cell typed.** Every resolved cell with a non-empty planting window carries `recommended_type in {northern_highbush, southern_highbush, rabbiteye}` AND `leaf_habit in {deciduous, evergreen}`.
3. **Type COVERAGE invariant (the onion-A9 analog).** Every `recommended_type` appearing in a resolved cell has >= 1 variety in `varieties.recommended[]` with a matching `type`. (Guards "we recommend rabbiteye in se_gulf but list no rabbiteye cultivar.")
4. **`leaf_habit` <-> calendar coherence (the teeth).** A `deciduous` cell's `calendar[]` contains the `dormant` cycle and NO `season_over`; if its prune window is set it carries the `prune` token. An `evergreen` cell's `calendar[]` contains NO `dormant` and NO `season_over`. A resolved leaf-habit the calendar contradicts is a defect (the tree A4 / strawberry A11 shape).
5. **No herbaceous/annual tokens.** No `renovation` token (strawberry-only); no `season_over` in any cell (a woody perennial's off-season is `dormant` up North and continuous growth down South, never "season over").
6. **Cross-pollination honored.** `self_fertile == false`; no variety carries `bloom_group`/`pollinizer`/`bloom_window`.
7. **No tree mis-route.** No cell carries `suitability` or rootstock keys (catches a shell mis-built through the tree path).

Built test-first against FILLED blueberry data; the fill assertions run at Step 11 cert and on-demand. At Step 3.5 it behaves like the tree/berry shells -- region-unfilled = admission state (stub/null/stale all 0), the calendar-coherence checks no-op on empty calendars. Added to the always-on `whole_crop_gate` (no-op off-branch), so no other crop is affected. Paired with `berry_woody_calendar_violations` if the calendar coherence is split into its own A-section (mirrors the berry A10/A11 + woody-ornamental A13/A14 structural-vs-calendar split) -- decided at implementation.

---

## 5. Arc integration (no new steps; fields land inside existing steps)

- **Step 0 (preflight):** `sha256(crops_data_final.json) == LATEST.txt`.
- **Step 1-2 (sources + scalars/structured):** `soil`, `ph` (4.5-5.5, the elevated beat), `container_notes` (acid potting mix -- blueberries do well in containers, a real beginner on-ramp), `spacing_inches`, `companions` core; `succession_policy.suitable = false`; the 2.9 lifecycle scalars (D6); `self_fertile = false`; `gating_factors = ["chill_hours"]`; `start_method.start = "nursery_transplant"`; `chill_hours_required`/`range` per type. The variety set (D7) spanning the 3 types. Each with field-level `sources` (>= 2 T1) + `anchoring_urls`. **build_region_shells trigger:** archetype `berries_woody` is already set (the shell carries it), so 3.5 routes to `_build_berry_woody_shells`; confirm at Step 1-2 it is not overwritten.
- **Step 3 (companion walk):** carrot rich-object shape; vocab `research_backed`/`likely`/`traditional`. (Blueberry companions are thin -- acid-loving neighbors like azalea/rhododendron + the honest "not a heavy-companion crop.")
- **Step 3.5 (Claude Code lane -- region shell build):** new `build_region_shells._build_berry_woody_shells` (test-first, idempotent, no-clobber): set `calendar_basis -> berries_woody`; build all 10 region cells -- one `nursery_transplant` setting `plantings[]` window, the `recommended_type`/`leaf_habit` slots (null at 3.5), `chill_hours_delivered`, the cell key-set (`plant_out`/`bloom`/`harvest_start`/`harvest_end`/`calendar:[]`/`type_note_*`/`frost_risk_note_seasoned`/`resolved_from:{}`); strip annual-only AND tree-only keys; `northern_tier` from-scratch (author-fresh, no `zones{}` promote). Gate at 3.5 = shape/admission only.
- **Step 4 (region fill):** per-region `recommended_type` + `leaf_habit` + chill (SOURCE finding, A5 -- not inferred); the nursery-setting + bloom/harvest windows; GENERATE each `calendar[]` from the windows + `leaf_habit` with `berry_woody_calendar` (deciduous: `dormant`+`prune` cycle; evergreen: continuous growing), never hand-typed; frost reconcile against `zone_frost_data`.
- **Step 5 (verification):** the chill figures per type, `recommended_type` per region, `leaf_habit` boundary, `hardiness_zone`/`reliable_fruit_zone`, and the pH range all sourced to T1, not analogized; source FIDELITY (independent fetch at cert), not just lift-scan. (The yield-vs-cited-source lesson from green-beans applies.)
- **Step 5.5 (calendar branch):** the `berries_woody` branch -- `plantings[]` = exactly one nursery-setting window (no succession/second_planting); `calendar[]` uses the deciduous/evergreen vocab per `leaf_habit`; `leaf_habit <-> calendar` coherence; succession/heat-pause N/A.
- **Steps 6-8 (bulk prose, COMPUTED sweep):** populate every null `_seasoned`/`_beginner` -- the type_selection elevated section, pollinator_notes, chill_hours_note, the ELEVATED acid-soil beat (soil/ph prose + a growth-stage/notification + the chlorosis `failure_diagnostics` entry), pruning (a real woody care beat -- the `prune` calendar token + a notification), bloom/harvest, establishment/year-one (pick off early bloom), hardiness, type_note_*, region_notes_*, container, the 7 A12 compounds (growth_stages incl. a dormancy/prune + bloom + fruit-set + ripening sequence; pests = spotted-wing drosophila + birds; diseases = mummberry, Phytophthora root rot in wet soil; failure_diagnostics lead = chlorosis-from-high-pH) -- block-coherent + anchored.
- **Step 9 (sweep):** dash/temp/spelling, 0 user-facing `--`, degF symbol.
- **Step 11 (cert / the flip):** `verification_status` flip (status `verified_gs_arc` + launch_ready x2 + source_set + log_ref + open_findings all `blocks_launch:false`); run the new D8 gate's fill branch + `register_fill_gate` + calendar coherence + the verbatim/source-fidelity fetch sample.

---

## 6. What this explicitly does NOT do (YAGNI boundaries)

- **No lowbush 4th type** (D1) -- far-north = cold-hardy northern highbush + half-high cultivars as `northern_highbush` varieties + prose.
- **No apple pollinizer machinery** -- `self_fertile: false` + "plant 2 of the same type" prose (D4); no `bloom_group`/`pollinizer`/`bloom_window`.
- **No per-type pages / no per-type calendar toggle** -- one guide; type-neutral spine + elevated `type_selection` + per-cell `recommended_type`/calendar (D7 / Section 7). (Re-openable at the Phase-5 variety layer, the strawberry pattern.)
- **No rootstock / grafting / tree machinery** -- blueberries are own-root shrubs.
- **No `renovation` / `season_over` token** anywhere (D3) -- a woody perennial's off-season is `dormant` (North) or continuous growth (South).
- **No new lifecycle fields** -- the 2.9 scaffold carries them (D6).
- **`recommended_type` + `leaf_habit` are region-constant**, authored per region, not free per-zone UI toggles.

---

## 7. Open items (Step 4/5 authoring -- claude.ai sourcing lane, NOT design)

- **Per-region `recommended_type` + `leaf_habit` + `chill_hours_delivered`.** Expected lean (a sanity check, never the authority -- A5 governs, read a source per region): `northern_tier`/`ca_north_coast` deciduous northern highbush; `se_gulf`/`fl_peninsula`/`low_desert_az` evergreen rabbiteye or southern highbush; the CA interior/warm-arid + `hawaii_tropical` genuinely source-decided (chill is marginal/low; high-elevation niches). The transition zones (z7) are where both highbush + rabbiteye are grown -- a real source call on which to recommend.
- **Chill figures per type** (`chill_hours_required`/`range` + per-variety `chill_hours`): T1-sourced; the gate basis, so they must be real.
- **pH range** (preferred 4.5-5.5, tolerated low bound) -- Step-5 sourced.
- **`hardiness_zone` (survives) vs `reliable_fruit_zone` (fruits well)** per type -- both Step-5 sourced (a southern-highbush survives cold it won't fruit through, and vice versa).
- **Variety set:** how many cultivars per type, and whether half-high earns explicit entries -- claude.ai's recommended-set call, constrained by the coverage invariant.
- **Container model:** blueberries are a strong container crop (full pH control) -- a real beginner on-ramp; how prominently to surface it in `container_notes`.

---

## 8. Variety pages + the delta process (Phase 5 -- NOT anchor scope)

Mirrors the strawberry resolution so it is not re-litigated at the variety layer:
- **The anchor authors a descriptive recommended-variety SET** (objects `{name, type, ...}`) ON the crop page, not per-variety pages -- no delta issue in this spec's work.
- **Cultivars WITHIN a type are clean small deltas** (Duke vs Bluecrop, both northern highbush) -- season/chill/size/flavor, identical growing model; the delta overlay handles them as it does tomato cultivars.
- **The TYPE axis is the structural sub-mode** (northern_highbush vs rabbiteye changes chill, region, leaf_habit, calendar) -- carried ONCE per type at the Phase-5 variety layer, keyed off the variety `type` tag, NOT baked into each cultivar's delta. The crop stays ONE URL (`blueberry`); type is a structural sub-mode of that page, not a separate crop.
