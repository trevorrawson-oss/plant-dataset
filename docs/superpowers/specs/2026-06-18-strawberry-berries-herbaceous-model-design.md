# Strawberry / berries_herbaceous model -- design

**Date:** 2026-06-18
**Author:** Claude Code (structural lane)
**Status:** Approved design (Trevor, 2026-06-18). Spec review + implementation plan next.
**Milestone:** Strawberry gold-standard arc (anchor 13). Strawberry is the FIRST `berries_herbaceous` crop -- and the ONLY one in the dataset -- so this is the archetype's whole schema stress-test, not a template for a family.
**Reads against:** gold-standard arc checklist v2.0 (Steps 0 / 2 / 3 / 3.5 / 4 / 5 / 5.5 / 6-8 / 9 / 11); `tools/build_region_shells.py` (the `_build_tree_shells` precedent); `tools/whole_crop_gate.py` (the A-section gate pattern, A6/A8/A9 off-branch no-op); `tools/perennial_gate.py` + `tools/tree_calendar.py` (the perennial cert + derive-the-calendar precedents); the v1.8 tree branch + the evergreen `gating_factors` amendment; the onion photoperiod design (the model we DEPART from -- see D7).
**Start SHA:** `6f48eb11374edea5a2b0ae893d7a71169ed71c68404b75cb12e116fe65d319e7` (canonical content SHA; must equal `LATEST.txt` at apply time -- Step 0 preflight).

---

## 1. Problem

Strawberry does not fit any certified archetype, for three compounding reasons:

1. **It is a herbaceous perennial, not an annual and not a tree.** An established bed runs a recurring cycle (dormant -> bloom -> fruit -> renovate -> runners -> dormant), so the annual "plant -> grow -> harvest -> `season_over`" calendar is a category error. But it is not a tree either: it is planted from stock in a frost-anchored window and the bed is replaced every ~3-4 years, so the tree's plant-once / chill-gated model is also wrong.

2. **Its lifecycle is region-dependent.** In the north (matted row) it is grown as a perennial; in hot-summer regions (California interior/desert, Florida) summer heat exhausts the planting, so it is grown as a fall-planted **annual** that is pulled and replanted every year. A single crop-level lifecycle label mismatches half the regions.

3. **It is really three growing models** -- June-bearing (short-day, matted row, annual renovation, one early-summer flush), day-neutral (photoperiod-insensitive, continuous, the basis of the California/Florida annual systems), and everbearing (two flushes). The type changes the calendar, the lifecycle, and whether renovation applies -- far more than a normal variety difference.

There is **zero herbaceous-perennial modeling in the dataset today**. Strawberry is the gold-standard anchor precisely because getting it honest forces the schema to express a crop whose lifecycle itself varies by region.

**Product decision (Trevor, 2026-06-18): one guide, June-bearing matted-row spine, the type choice elevated.** `strawberry` stays a single crop at one URL (the term growers actually search). The calendar and lifecycle are anchored on the dominant US backyard model (June-bearing matted-row perennial). The June-bearing / day-neutral / everbearing choice is surfaced as a first-class on-page section (a genuine "which type should you grow?" decision), not buried as a variety footnote. Day-neutral and everbearing are variety-tagged alternatives; the warm-region annual reality is carried by the region cells. A per-type calendar toggle was rejected (see D7 / Section 6): the planting axis is mostly region-driven and already captured by the region cells, so a toggle would mostly re-encode the region axis at ~3x the authoring, for an archetype of one.

---

## 2. Decisions

**D1 -- One crop, June-bearing matted-row spine, type elevated.** One `/guides/crops/strawberry/[zone]/`. Crop-level calendar and lifecycle scalars carry the June-bearing matted-row perennial model. The type choice is an elevated dual-register section (D8); day-neutral/everbearing differences ride that section + the per-variety `type` tag + the `grown_as: annual` cells. No separate per-type pages, no per-type calendar toggle.

**D2 -- New `calendar_basis` value `perennial_herbaceous` (the 6th).** Frost resolution stays **ON** -- strawberry's plant/bloom/harvest windows anchor to frost dates exactly like an annual, so the resolver math, frost reconcile, and `zone_frost_data` usage are unchanged. The basis is a SHAPE/semantic signal: it tells the renderer and gates "render the perennial-bed lifecycle, consult the per-cell `grown_as`," distinct from `frost_anchored` (annual plant-and-pull, wrong `season_over` semantics for a perennial), the tree bases, and `non_seasonal_indoor`. It completes the perennial basis family: `perennial_chill_gated` (deciduous trees) / `perennial_evergreen` (citrus) / `perennial_herbaceous` (strawberry). Set by `build_region_shells` at Step 3.5 (flips the `frost_anchored` wipe default), the same way the tree path sets its basis.

**D3 -- Per-cell `grown_as` is the lifecycle discriminator.** New resolved-cell field `grown_as` in `{perennial, annual}`, mirroring the tree per-cell `suitability`. Region-constant in practice (a region is uniformly one mode), authored per region and resolved down to its zone cells. North (`northern_tier`) = `perennial`; hot-summer warm regions (`ca_interior`, `ca_desert`, `low_desert_az`, `fl_peninsula`) = `annual`. The renderer picks the lifecycle to display from this field; the cert gate branches on it (D9). The exact per-region assignment is a Step-4/5 SOURCE finding (A5 discipline), not an inference -- the expected set above is a sanity check, never the authority (mild-coastal CA and `se_gulf`/`hawaii_tropical` are genuinely source calls; see Section 7).

**D4 -- Calendar vocab: reuse `dormant`, add one token `renovation`.** Perennial cells use the cyclic vocab: reuse `dormant` (the tree branch already added it) for winter die-back, and add the single new state **`renovation`** (perennial June-bearing cells, the month after harvest -- mow tops, narrow the row, fertilize). Annual cells use the annual vocab **including `season_over`**, which is correct there because the planting genuinely ends. The HARD rule: an `annual` cell carries no `renovation`/`dormant`; a `perennial` cell carries the `dormant` cycle (+ `renovation` for the June-bearing spine) and NEVER `season_over`. One crop, two calendar shapes, selected by `grown_as`. `renovation` is added to the calendar state enum (checklist prose) and to the `annual_coherence` (A5) valid-token set for this basis.

**D5 -- Propagation reuses `start_method.start = "bare_root_dormant"`.** Strawberry crowns are dormant bare-root stock, planted like a bare-root fruit tree -- the exact value peach and apple already carry. No new enum value. The window is a `plant_out`-only crown-setting window (no `start_indoors`, no `direct_sow`), frost-anchored. `hardening_off` is N/A for dormant crowns (authored as N/A prose, never null). The potted-plug source (the norm for fall/warm-region planting), the matted-row runner self-propagation, and seed-from-alpine are prose nuances (planting + `renovation_*` + `year_one_notes_*`), not window-shape changes. `build_region_shells` needs a NEW `perennial_herbaceous` path: strawberry is not `_is_tree` (lifecycle `perennial` not `permanent`, archetype `berries_herbaceous` not `*_fruit_tree`, basis not chill-gated) so it will not route to the tree shells, and it must not route to the annual seed-window path.

**D6 -- Lifecycle uses the existing 2.9 scaffold; no new lifecycle fields.** The 2.9 migration already null-scaffolded the full perennial set on strawberry. Populate them: `renovation_seasoned`/`_beginner`, `year_one_notes_*`, `establishment_years`, `establishment_note`, `years_to_first_harvest`, `years_to_full_production`, `productive_lifespan_years`, `self_fertile`. Crop-level scalars carry the June-bearing matted-row perennial spine (first real harvest year 2 after pinching, ~3-4 year bed life); day-neutral/annual variations ride the type section + `grown_as: annual` cells + variety notes. Runners need no field -- they live in `year_one_notes_*` + `renovation_*`.

**D7 -- Photoperiod is NOT a gate (the deliberate inverse of onion).** The June-bearing/day-neutral/everbearing distinction IS photoperiod (short-day flower induction vs day-neutral), but it is modeled as a TYPE attribute, never as onion's region gate. Concretely strawberry carries **no** `gating_factors: ["photoperiod"]`, **no** per-cell day-length field, and the A9 photoperiod gate does **not** fire on it. Rationale: for onion, latitude DICTATES which type bulbs (wrong type -> no bulb -> a hard zone gate). For strawberry, type is a grower's HARVEST-PATTERN choice -- June-bearing for one big flush, day-neutral for all-season fruit -- and both work at the same latitude. The soft regional lean (day-neutrals in hot-summer systems) is already captured by `grown_as`. The gate (D9) defensively asserts `"photoperiod"` is NOT in `gating_factors`, to guard against importing the onion model by reflex.

**D8 -- Type lives on varieties + one elevated explainer; self-fertile, no cross-pollination feature.** Recommended varieties become objects carrying `type in {june_bearing, day_neutral, everbearing}`. A single new crop-level dual-register pair `type_selection_seasoned`/`_beginner` holds the "which type should you grow?" teaching the renderer surfaces near the top (CP class, auto-covered by the register gates). `self_fertile: true`; `pollinator_notes_*` note that bees improve fruit shape/size but no pollinizer is needed. Strawberry's variety objects are therefore SIMPLER than the tree ones -- `{name, type, days_or_season, use, recommended_note}` -- and carry NONE of the tree bloom_group / pollinizer / bloom-window machinery. Chill is informational prose (`chill_hours_note_*`), not a `gating_factor` and not a per-cell suitability verdict; the chill figure is a Step-5 sourcing call (Section 7).

**D9 -- A new cert-gate branch, `berries_herbaceous_violations(crop)`.** Test-first, wired into `whole_crop_gate` as the next free A-section (no-op unless `calendar_basis == "perennial_herbaceous"`), consistent with how A6/A8/A9 were added off-branch-safe. It is the teeth of the model (Section 4).

---

## 3. Schema

### 3a. Crop level
```
"calendar_basis": "perennial_herbaceous",      // set by build_region_shells at 3.5
"lifecycle": "perennial",   "perennial": true,
"archetype": "berries_herbaceous",             // already set
"start_method": { "start": "bare_root_dormant", "weeks_before": null,
                  "hardening_off_seasoned": <N/A prose>, "hardening_off_beginner": <N/A prose>,
                  "notes_seasoned": <set crowns at the crown line...>, "notes_beginner": <...> },
"self_fertile": true,
"establishment_years": <int>,            "productive_lifespan_years": <int>,   // ~3-4 (matted row)
"years_to_first_harvest": [...],         "years_to_full_production": [...],
"renovation_seasoned": "<...>",          "renovation_beginner": "<...>",
"year_one_notes_seasoned": "<pinch flowers, let runners fill the row>", "year_one_notes_beginner": "<...>",
"establishment_note": "<universal>",
"type_selection_seasoned": "<which type to grow + why>", "type_selection_beginner": "<...>",   // NEW CP pair (D8)
"chill_hours_required": <int|null>, "chill_hours_range": [...], "chill_hours_note_*": "<informational, NOT a gate>",
"bloom_time_*": "<...>", "bloom_duration_days": <int|null>, "pollinator_notes_*": "<bees help shape; self-fertile>",
"hardiness_zone_min/max": <survives>, "reliable_fruit_zone_min/max": <fruits well>,
"succession_policy": { "suitable": false, ... }
```
No `gating_factors` key for photoperiod (D7). `hardiness` (survives) and `reliable_fruit` (fruits well) stay distinct crop-level scalars; unlike the trees there is no per-cell `suitability` verdict (the per-cell story is `grown_as` + the calendar).

### 3b. Variety level (`varieties.recommended[]`, objects)
```
{ "name": "Honeoye", "type": "june_bearing", "days_or_season": "early-season June-bearer",
  "use": "fresh + freezing", "recommended_note": "A hardy, productive early June-bearer for cold-winter matted rows." }
{ "name": "Albion", "type": "day_neutral", "days_or_season": "summer-through-fall",
  "use": "fresh", "recommended_note": "A day-neutral that fruits the first season; good in raised beds and containers." }
```
`type in {june_bearing, day_neutral, everbearing}`. The recommended set spans the types the page teaches. NO bloom_group / pollinizer / bloom_window fields (self-fertile, D8).

### 3c. Region / zone cell
Region-constant: `grown_as` (authored per region), one `plantings[]` crown-setting establishment window (`plant_out` rule list; NO `succession`, `second_planting`, `start_indoors`, `direct_sow`), `region_notes_*`.
Per resolved cell (`resolved_by_zone.<zone>`):
```
"grown_as": "perennial",                       // or "annual"
"plant_out": "<crown-setting window>", "bloom": "<...>", "harvest_start": "<...>", "harvest_end": "<...>",
"calendar": [ "dormant","dormant","growing","bloom","harvest","renovation","growing","growing","care","dormant","dormant","dormant" ],
"grown_as_note_seasoned": "<why perennial/annual here>", "grown_as_note_beginner": "<...>",
"frost_risk_note_seasoned": "<late frost on open blossoms>",
"resolved_from": { "last_frost": "...", "first_frost": "..." }, "resolution_method": "perennial_herbaceous_precompute"
```
An `annual` cell instead carries an annual-shaped `calendar` ending in `season_over` and NO `renovation`/`dormant`. STRIP the tree keys (`suitability`, `chill_hours_delivered`) -- their presence is a mis-route (D9 check 5). The `calendar[]` is GENERATED from the dates, never hand-typed (v1.9 discipline; Section 5).

---

## 4. The gate -- `berries_herbaceous_violations(crop)` (whole_crop_gate, next free A-section)

No-op unless `calendar_basis == "perennial_herbaceous"`. Otherwise returns a list of violation strings (`[]` = pass). Asserts:

1. **Lifecycle fields present.** `renovation_*`, `year_one_notes_*`, `establishment_years`, `years_to_first_harvest`, `years_to_full_production`, `productive_lifespan_years`, `self_fertile`, `type_selection_*` all non-null (register-fill checks the prose pairs; this asserts the perennial-specific set as a backstop).
2. **`grown_as` typed.** Every resolved cell with a non-empty planting window carries `grown_as in {perennial, annual}`.
3. **`grown_as` <-> calendar coherence (the teeth).** An `annual` cell's `calendar[]` contains no `renovation` and no `dormant`, and may contain `season_over`. A `perennial` cell's `calendar[]` contains the `dormant` cycle and never `season_over`; if the spine type is present it carries exactly the `renovation`-after-harvest token. A resolved lifecycle the calendar contradicts is a defect, the same shape as the tree calendar-coherence gate (A4) and the perennial `survives != fruits` invariant.
4. **`renovation` placement.** The `renovation` token appears only in `perennial` cells.
5. **No tree keys.** No cell carries `suitability` or `chill_hours_delivered` (catches a shell mis-routed through the tree builder).
6. **No cross-pollination machinery + self-fertile honored.** `self_fertile == true`; no variety carries `bloom_group`/`pollinizer`/`bloom_window`.
7. **Not photoperiod-gated (D7 guard).** `"photoperiod"` not in `(crop.get("gating_factors") or [])`.

Built test-first against FILLED strawberry data; the fill assertions run at Step 11 cert and on-demand. At Step 3.5 it behaves like the tree shells -- region-unfilled = admission state (stub/null/stale all 0), the calendar coherence checks no-op on empty calendars. Added to the always-on `whole_crop_gate` (no-op off-branch), so no other crop is affected.

---

## 5. Arc integration (no new steps; fields land inside existing steps)

- **Step 0 (preflight):** `sha256(crops_data_final.json) == LATEST.txt`.
- **Step 2 (scalars/structured):** `soil`, `ph`, `container_notes`, `spacing_inches`, `companions` core; `succession_policy.suitable = false`; the 2.9 lifecycle scalars (D6); `self_fertile = true`; `start_method.start = "bare_root_dormant"`; `chill_hours_required`/`range` if cleanly sourced (Section 7). Each with field-level `sources` (>= 2 T1) + `anchoring_urls`.
- **Step 3 (companion walk):** carrot rich-object shape; vocab `research_backed`/`likely`/`traditional`.
- **Step 3.5 (Claude Code lane -- region shell build):** new `build_region_shells` `_build_berry_herbaceous_shells` (test-first, idempotent, no-clobber): set `calendar_basis -> perennial_herbaceous`; build all 10 region cells -- one `bare_root_dormant` crown-setting `plantings[]` window, the `grown_as` slot (null at 3.5), the cell key-set (`plant_out`/`bloom`/`harvest_start`/`harvest_end`/`calendar:[]`/`grown_as_note_*`/`frost_risk_note_seasoned`/`resolved_from:{}`); strip annual-only AND tree-only keys; `northern_tier` from-scratch (author-fresh, no `zones{}` promote). Gate at 3.5 = shape/admission only.
- **Step 4 (region fill):** per-region crown windows + `grown_as` per region (SOURCE finding, A5 -- not inferred); GENERATE each `calendar[]` from the dates with a `berry_herbaceous_calendar` deriver (emits the `dormant`+`renovation` cycle for `perennial` cells, the `season_over`-terminated shape for `annual` cells), never hand-typed (v1.9); frost reconcile against `zone_frost_data` (the onion NT lesson).
- **Step 5 (verification):** chill figure, `hardiness_zone`/`reliable_fruit_zone`, and the `grown_as` boundary all sourced to T1, not analogized; source FIDELITY (independent fetch at cert), not just lift-scan.
- **Step 5.5 (calendar branch):** the `perennial_herbaceous` branch -- `plantings[]` = exactly one crown window (no succession/second_planting); `calendar[]` uses the perennial/annual vocab per `grown_as`; `grown_as <-> calendar` coherence; succession/heat-pause N/A.
- **Steps 6-8 (bulk prose, COMPUTED sweep):** populate every null `_seasoned`/`_beginner` -- `renovation_*`, `year_one_notes_*`, `type_selection_*`, `chill_hours_note_*`, `bloom_time_*`, `pollinator_notes_*`, `establishment_note`, `hardiness_notes_*`, the day-neutral alternative content, `grown_as_note_*`, `region_notes_*`, `container_notes`, soil/ph/companion/watering prose -- block-coherent + anchored.
- **Step 9 (sweep):** dash/temp/spelling, 0 user-facing `--`.
- **Step 11 (cert / the flip):** `verification_status` flip (status `verified_gs_arc` + launch_ready x2 + source_set + log_ref + open_findings all `blocks_launch:false`); run the new D9 gate's fill branch + `register_fill_gate` (no null register field) + calendar coherence + the verbatim/source-fidelity fetch sample.

---

## 6. What this explicitly does NOT do (YAGNI boundaries)

- **No per-type calendar toggle / no per-type calendars.** One calendar = the regionally-appropriate spine; day-neutral/annual differences are prose + `grown_as`. (Rejected: ~3x authoring + a new renderer pattern for an archetype of one; mostly re-encodes the region axis. Re-openable if usage ever shows the day-neutral annual calendar needs its own structural track.)
- **No photoperiod gate / `gating_factors` / A9 firing on strawberry** (D7).
- **No cross-pollination / bloom-overlap variety calendar** (self-fertile, D8).
- **No new propagation field** (reuse `bare_root_dormant` + prose, D5).
- **No chill suitability gate** (chill is informational, D8); strawberry has no per-cell `suitability` verdict.
- **`grown_as` is region-constant**, not a free per-zone UI toggle.

---

## 7. Open items (Step 4/5 authoring -- claude.ai sourcing lane, NOT design)

- **Per-region `grown_as` assignment.** Expected: `northern_tier` perennial; `ca_interior`/`ca_desert`/`low_desert_az`/`fl_peninsula` annual. Genuinely source-decided (not inferred): mild-coastal `ca_north_coast`/`ca_south_coast` (perennial vs long day-neutral annual), `se_gulf` (humid-summer decline), `warm_arid`, and `hawaii_tropical` (strawberries are an elevation/niche crop there). A5 governs: read a source for each region, do not analogize from a neighbor.
- **Chill figure** (`chill_hours_required` / `chill_hours_range`): author if a clean T1 figure exists; else honest `chill_hours_note_*` with the field left null. Informational, never a gate.
- **`hardiness_zone` (survives, with mulch) vs `reliable_fruit_zone` (fruits well)** -- both Step-5 sourced.
- **Variety set:** how many of June-bearing / day-neutral / everbearing to list, and whether everbearing earns its own entries or a mention (claude.ai's recommended-set call).
- **`bloom_duration_days`:** author if relevant to the frost-on-blossom guidance, else null.
```

