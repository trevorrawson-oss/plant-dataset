# Corn Family GS-Anchor Implementation Plan (field-corn / popcorn / flint-corn)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify three new §E crops -- `field-corn` (dent), `popcorn`, `flint-corn` -- as frost-anchored, direct-sown, dry-down *Zea mays* annuals, modeled field-by-field on sweet-corn + dry-bean, with NO new gate and NO new field.

**Architecture:** Each crop is authored as a full §E crop record by CLONING sweet-corn's record and applying a fixed set of deltas (dry-down `growth_stages`, DTM band, dry-corn uses/varieties/prose, 12 re-authored regional calendars with Option-C humid advisories), T1-sourced. Each is validated to `whole_crop_gate` PASS on a scratch canonical. The three are then spliced in via one SHA-guarded `apply_patch` add-batch, put through the full release battery, and promoted (Trevor-gated).

**Tech Stack:** Python 3 standalone gates (`whole_crop_gate.py`, `gate_all.py`, `calendar_coherence_gate.py`, `timing_spine_gate.py`, `release_verify.py`), `tools/apply_patch.py` (SHA-guarded JSONPath splicer), compact JSON.

## Global Constraints

- Canonical `crops_data_final.json` is **COMPACT**: `json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline, never `indent=`. Never reformat it.
- Canonical is **READ-ONLY** until the Task 6 promote. All authoring goes to scratch crop-object files; gates run against a scratch canonical (`base + the new crop(s)`), never the live one.
- **No new gate, no new field, no new archetype** (kickoff #21 reframe: the gate dispatch key is `calendar_basis`, not `archetype`). Reuse `warm_season_grass` + `planting_layout`/`pollination_block_min_rows` exactly as sweet-corn.
- **Legacy variety shape** (`varieties.recommended[] = {name, days_to_maturity, note}`). NOT the flat variety_detail schema; no `hero_description`, no `maturity_class` (these crops must NOT opt into `variety_detail_gate`).
- **No em dashes** in any consumer-facing string. American English. Temps render `°F`. Per-variety/regional/threshold claims **T1-sourced** (university .edu extension / gov); the DTM synthesis band is Trevor-ratified.
- Base canonical **`c73d7fa`** (125 crops, 116 certified); re-stamp `base_sha` from the live worktree canonical at build time.
- Working in the isolated worktree `.claude/worktrees/corn-family` (branch `worktree-corn-family`). Commit freely on this branch; **merge to main + push + plant-astro bump are Trevor-gated at the very end (Task 6)**.
- Slugs: `field-corn`, `popcorn`, `flint-corn` (confirm against the master crop list at authoring; `field-corn` chosen over bare `corn` for clarity).

## §E crop record shape (what each authored crop MUST carry)

Clone the full top-level key set from sweet-corn (do not invent or drop keys). The ~70 keys include:
`slug, name, type, category("Corn"), difficulty, days_to_maturity, days_to_maturity_mid, dtm_anchor,
calendar_basis("frost_anchored"), archetype("warm_season_grass"), perennial(false), lifecycle,
propagule("seed"), weeks_indoors(0), seedling_light("na"), tray_sowing("na"), germination_light,
germination_temp_f, sow_depth_inches, spacing_inches, thin_to_inches, thinning, planting_layout("block"),
pollination_block_min_rows(4), sunlight, sunlight_hours, water, watering, soil, ph, fertilizer,
frost_effect("killed"), frost_tolerance_f, heat_threshold_f, heat_effect, chilling_sensitivity_f,
growth_stages[], harvest_window_days(OMIT for dry corns), harvest_urgency, harvest_ready_*,
description_beginner, description_seasoned, soil_prep_*, container_notes, companions, pests, diseases,
rotation, storage, recipes, yield_expectations, failure_diagnostics, tips_by_stage, notifications,
weather_triggers, moon_phase_preference, start_method, succession_policy(single-crop), first_planting_notify_days,
regions{12}, varieties, sources_summary, verification_status, last_reviewed*, zones`.

**Region cell** (per the 12 regions): `region_id, region_label, zone_span, region_notes_beginner,
region_notes_seasoned, plantings[], plantings_provenance, sources, resolved_by_zone{}`. Each
`resolved_by_zone[zone]`: `calendar[], first_plant_date, last_plant_date, plant_out, start_indoors(na for
direct-sow), harvest, harvest_start, harvest_end, resolution_method, resolved_from, notes, planting_note,
zone_notes, sources, anchoring_urls, successions_realized`. **DRY-CORN delta:** `harvest` lands at
dry-down (later than sweet-corn); humid regions carry a field-drying advisory in `notes`/`zone_notes`.

**growth_stages** (9 stages, each with `id, name, audience, day_range_from_sow[from,to],
user_action_beginner/seasoned, what_to_look_for_beginner/seasoned, log_prompt_beginner/seasoned`):
`germination -> seedling -> vegetative -> tasseling -> silking -> kernel_fill -> dry_down -> harvest -> cure_thresh`.
`day_range_from_sow` monotonic non-decreasing; the `harvest` id is the A40 anchor carrying the crop DTM band.

---

### Task 1: Author `field-corn` (dent) -- full §E record

**Files:**
- Create: `/private/tmp/field_corn.json` (the one crop object)
- Create: `docs/reviews/notes/2026-07-15/corn_field_sourcing.md`

**Interfaces:**
- Produces: a `field-corn` crop object (all §E keys) consumed by the Task 5 builder.

- [ ] **Step 1: Clone the sweet-corn record as the starting template.** Load the live canonical, deep-copy the `sweet-corn` crop object. This gives every §E key in the correct shape.

- [ ] **Step 2: Apply the field-corn deltas.** Change:
  - `slug:"field-corn"`, `name:"Field Corn"` (or "Field / Dent Corn"), `type` per sweet-corn's convention, `category:"Corn"`.
  - `days_to_maturity:[95,120]`, `days_to_maturity_mid:110` (Trevor-ratified synthesis; flag at the checkpoint), `dtm_anchor` = sweet-corn's (`from_sow`).
  - `growth_stages`: rebuild to the 9-stage dry-down ladder above -- keep sweet-corn's germination..kernel_fill prose, then author `dry_down` (kernels dry hard on the stalk), re-point `harvest` to the DRY ear pick (kernels hard/dent, not milk), add `cure_thresh` (finish drying + shell off the cob for storage). Monotonic `day_range_from_sow`.
  - **OMIT `harvest_window_days`** (one-shot dry harvest; delete the key).
  - `succession_policy`: single-crop (copy dry-bean's, not sweet-corn's staggered-block).
  - `harvest_ready_*` / `harvest_urgency`: dry-down readiness (kernels hard, husks dry, ~black-layer), low urgency.
  - `description_beginner`/`description_seasoned`: dry-corn (grain/cornmeal/masa/feed), name the representative varieties, include the CROSS-POLLINATION note (isolate ~250+ ft or stagger tassel ~2 weeks; dent pollen ruins popcorn). No em dashes; `°F`.
  - `varieties`: legacy shape, dry-corn dents (e.g. Reid's Yellow Dent, Wapsie Valley, a hybrid grain dent) `{name, days_to_maturity, note}`; `note_beginner`/`note_seasoned` + T1 `sources`/`anchoring_urls`.
  - `storage`/`recipes`/`yield_expectations`/`companions`/`pests`/`diseases`/`rotation`: dry-corn appropriate (copy+adjust from sweet-corn; corn earworm/borer/smut, etc.).
  - Thresholds (`frost_tolerance_f`/`heat_threshold_f`/`chilling_sensitivity_f`/`germination_temp_f`): copy sweet-corn's sourced Zea mays values (same species) unless a dry-corn source differs.
  - `verification_status`: `status:"verified_gs_arc"`, `phase`, `date:"2026-07-15"`, `source_set` = the T1 ids actually cited, fresh `verification_log`.

- [ ] **Step 3: Author the 12 regional calendars.** For each of `northern_tier, se_gulf, ca_interior,
  ca_north_coast, ca_south_coast, ca_desert, warm_arid, low_desert_az, fl_peninsula, hawaii_tropical, rgv,
  pnw`: T1-anchored sow -> dry-down calendar (harvest at dry-down, later than sweet-corn). **Option C (all
  plantable):** humid regions (`fl_peninsula, se_gulf, hawaii_tropical, rgv, pnw`) keep a populated
  calendar but `notes`/`zone_notes` advise harvesting at hard-dent and finishing the dry-down indoors
  (dry-bean precedent). Short-season northern zones: honest DTM advisory. `heat_pause` only where a desert
  summer genuinely pauses set. Direct-sow so `start_indoors` = na. Use the sweet-corn region cells as the
  structural template + shift `harvest` for dry-down. Every regional claim T1-cited.

- [ ] **Step 4: Record the sourcing note** `docs/reviews/notes/2026-07-15/corn_field_sourcing.md` (per-region + per-variety + threshold -> T1 source id + URL). Confirm 0 non-T1 load-bearing sources.

- [ ] **Step 5: Validate to `whole_crop_gate` PASS on a scratch canonical.** Build `/tmp/corn_scratch.json` = live canonical with `field-corn` appended at `$.crops[len]`; run:
  `python3 tools/whole_crop_gate.py field-corn /tmp/corn_scratch.json` -> **GATE: PASS**;
  `python3 tools/calendar_coherence_gate.py /tmp/corn_scratch.json` -> field-corn 0;
  `python3 tools/timing_spine_gate.py /tmp/corn_scratch.json` -> 0.
  Iterate the crop object until all pass. Write `/private/tmp/field_corn.json` (the validated crop object). Commit the sourcing note.

```bash
git add docs/reviews/notes/2026-07-15/corn_field_sourcing.md
git commit -m "docs(corn): field-corn T1 sourcing table"
```

---

### Task 2: Representative adversarial RED proof (corn dry-down §E shape)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/corn_family_red_proof.md`

**Interfaces:**
- Consumes: `/private/tmp/field_corn.json` (the validated exemplar; the 3 crops share this §E shape, so one proof covers all three -- the dry-bean/sweet-corn one-proof-per-arc precedent).

- [ ] **Step 1: Green baseline.** Scratch canonical with `field-corn` added -> `whole_crop_gate field-corn` PASS, `gate_all` PASS.
- [ ] **Step 2: Inject each §E defect class on a scratch copy of field-corn and confirm it BOUNCES** (non-empty violation + expected substring; canonical READ-ONLY): non-monotonic `growth_stages.day_range_from_sow`; dropped `germination_light`; absurd `days_to_maturity` (e.g. `[7,9]` -- note if it sits inside the universal `[7,400]` floor per the sweet-corn finding); an em dash in a consumer string; a bad enum (`calendar_basis:"bogus"`); a dropped canonical region (11/12) -> A31 coverage floor; a `growth_stages` missing the `harvest` id -> A40.
- [ ] **Step 3: Record + commit** `corn_family_red_proof.md` (defect class -> expected substring -> observed bounce; canonical SHA unchanged; note the shared-shape coverage of all 3 crops).

```bash
git add docs/reviews/notes/2026-07-15/corn_family_red_proof.md
git commit -m "test(corn): adversarial RED proof on the dry-corn §E shape (covers all 3)"
```

---

### Task 3: Author `popcorn` -- full §E record

**Files:**
- Create: `/private/tmp/popcorn.json`
- Create: `docs/reviews/notes/2026-07-15/corn_popcorn_sourcing.md`

**Interfaces:**
- Produces: a `popcorn` crop object consumed by the Task 5 builder. Same method + §E shape as Task 1.

- [ ] **Step 1: Clone sweet-corn, apply popcorn deltas.** `slug:"popcorn"`, `name:"Popcorn"`, `days_to_maturity:[90,110]`, `days_to_maturity_mid:100`; same 9-stage dry-down `growth_stages` (kernels must dry to the right moisture to pop), `harvest_window_days` OMITTED, single-crop. `description_*`: popping use (hard endosperm, moisture flash), name varieties (Robust, Japanese Hulless, Dakota Black, Strawberry ornamental), cross-pollination note (**dent/sweet pollen ruins popping** -- the sharpest isolation case). `varieties` legacy shape. Storage: dry to ~13-14% moisture for popping.
- [ ] **Step 2: Author the 12 regional calendars** (same method + Option C humid advisories as Task 1 Step 3).
- [ ] **Step 3: Record sourcing note** `corn_popcorn_sourcing.md`.
- [ ] **Step 4: Validate to `whole_crop_gate popcorn` PASS** (same battery as Task 1 Step 5); write `/private/tmp/popcorn.json`; commit the sourcing note (`docs(corn): popcorn T1 sourcing table`).

---

### Task 4: Author `flint-corn` -- full §E record

**Files:**
- Create: `/private/tmp/flint_corn.json`
- Create: `docs/reviews/notes/2026-07-15/corn_flint_sourcing.md`

**Interfaces:**
- Produces: a `flint-corn` crop object consumed by the Task 5 builder. Same method + §E shape as Task 1.

- [ ] **Step 1: Clone sweet-corn, apply flint deltas.** `slug:"flint-corn"`, `name:"Flint Corn"`, `days_to_maturity:[90,110]`, `days_to_maturity_mid:100`; same 9-stage dry-down `growth_stages`, `harvest_window_days` OMITTED, single-crop. `description_*`: cornmeal/polenta/hominy/decorative use, name varieties (Painted Mountain -- short-season, Floriani Red Flint, Cascade Ruby-Gold, Glass Gem ornamental), cross-pollination note. `varieties` legacy shape.
- [ ] **Step 2: Author the 12 regional calendars** (same method + Option C). Note Painted Mountain's short-season fit for the northern/short-season zones.
- [ ] **Step 3: Record sourcing note** `corn_flint_sourcing.md`.
- [ ] **Step 4: Validate to `whole_crop_gate flint-corn` PASS**; write `/private/tmp/flint_corn.json`; commit the sourcing note (`docs(corn): flint-corn T1 sourcing table`).

---

### Task 5: Builder + add-batch + scratch apply + full release battery

**Files:**
- Create: `tools/build_corn_family_patch.py`
- Create: `tools/batches/corn_family_add.json` (generated)
- Test: `tools/test_build_corn_family_patch.py`

**Interfaces:**
- Consumes: `/private/tmp/{field_corn,popcorn,flint_corn}.json`; `tools/apply_patch.py`.
- Produces: one atomic add-batch (3 `add` ops) + a footprint the battery verifies.

- [ ] **Step 1: Write the builder** `tools/build_corn_family_patch.py`: load the live canonical, stamp `base_sha`; emit 3 `add` ops appending each crop object at the next index (`$.crops[125]`, `$.crops[126]`, `$.crops[127]`) from the 3 scratch files; assert no em dash in any authored string across the 3 objects; print the batch JSON to stdout.
- [ ] **Step 2: Builder test** `tools/test_build_corn_family_patch.py`: `base_sha` matches live canonical; exactly 3 add ops; each value is a well-formed crop object with `slug in {field-corn, popcorn, flint-corn}`, `calendar_basis=="frost_anchored"`, `planting_layout=="block"`, `harvest_window_days` ABSENT, `growth_stages` last-id chain ends `...dry_down, harvest, cure_thresh`, 12 regions, NO `maturity_class` on any variety (legacy shape). Run: `python3 tools/test_build_corn_family_patch.py` -> PASS.
- [ ] **Step 3: Generate + apply to scratch.**
```bash
python3 tools/build_corn_family_patch.py > tools/batches/corn_family_add.json
python3 tools/apply_patch.py tools/batches/corn_family_add.json --base crops_data_final.json --out /tmp/corn_candidate.json
```
Expected: `crops changed` shows +3 new slugs; count 125 -> 128; `catalog +<only genuinely-new ids>`.
- [ ] **Step 4: Full release battery on `/tmp/corn_candidate.json`.**
```bash
python3 tools/whole_crop_gate.py field-corn /tmp/corn_candidate.json    # PASS
python3 tools/whole_crop_gate.py popcorn    /tmp/corn_candidate.json    # PASS
python3 tools/whole_crop_gate.py flint-corn /tmp/corn_candidate.json    # PASS
python3 tools/gate_all.py /tmp/corn_candidate.json                      # 119/119
python3 tools/calendar_coherence_gate.py /tmp/corn_candidate.json       # 0
python3 tools/timing_spine_gate.py /tmp/corn_candidate.json             # 0
python3 tools/release_verify.py /tmp/corn_candidate.json --base crops_data_final.json --slug field-corn
```
Plus a byte-diff footprint audit: EXACTLY the 3 new crops added; all 125 existing crops byte-identical; count 128; compact (no trailing newline). Fix authoring/builder and re-run until green.
- [ ] **Step 5: Commit tooling** (NOT the canonical).
```bash
git add tools/build_corn_family_patch.py tools/test_build_corn_family_patch.py tools/batches/corn_family_add.json docs/reviews/notes/2026-07-15/corn_*_sourcing.md
git commit -m "build(corn): family add-batch builder + generated batch + sourcing tables"
```

---

### Task 6: Promote (Trevor-gated) + state trio + roadmap + merge

**Files:**
- Modify: `crops_data_final.json`, `LATEST.txt`, `CURRENT_STATE.md`, `STATE_HISTORY.md`, `docs/crop_expansion_roadmap.md`

**Interfaces:**
- Consumes: `tools/batches/corn_family_add.json`.

- [ ] **Step 1: STOP -- get Trevor's explicit go** for the promote (canonical content change + the DTM synthesis bands + variety picks). Do not proceed without it.
- [ ] **Step 2: Apply to the real canonical** (re-check `shasum` base immediately before; the guard fails closed):
```bash
shasum -a 256 crops_data_final.json    # confirm base
python3 tools/apply_patch.py tools/batches/corn_family_add.json --base crops_data_final.json --out crops_data_final.json
shasum -a 256 crops_data_final.json    # new sha
```
- [ ] **Step 3: Re-run the full battery on the promoted canonical** (same commands as Task 5 Step 4 against `crops_data_final.json`): 3x `whole_crop_gate` PASS, `gate_all` 119/119, `calendar_coherence` 0, `timing_spine` 0, `release_verify` clean; footprint exact; count 128; compact.
- [ ] **Step 4: State trio + roadmap.** `LATEST.txt` (new SHA + session); `CURRENT_STATE.md` surgical top-entry prepend (NO gen_current_state regen -- it corrupts the no-separator file); `STATE_HISTORY.md` most-recent-first append; `docs/crop_expansion_roadmap.md` row 1 (corn family) flipped QUEUED -> SHIPPED. NO field-addition register row (no new field). Record: canonical `c73d7fa -> <new>`, 3 new dry corns, count 125 -> 128, 116 -> 119 certified, no new gate/field.
- [ ] **Step 5: Commit the promote** (explicit pathspec, collision-safe):
```bash
git add crops_data_final.json LATEST.txt CURRENT_STATE.md STATE_HISTORY.md docs/crop_expansion_roadmap.md
git status --porcelain    # read: exactly these 5
git commit crops_data_final.json LATEST.txt CURRENT_STATE.md STATE_HISTORY.md docs/crop_expansion_roadmap.md -m "feat(corn): certify field-corn/popcorn/flint-corn (dry corn family, 125->128)"
git show --stat HEAD    # confirm exactly 5 files
```
- [ ] **Step 6: Merge to main + push + plant-astro (ALL Trevor-gated, separate).** Merge `worktree-corn-family` into `main`, push, bump plant-astro -- each on Trevor's explicit go. (This step is a checklist item, not auto-run.)

---

## Self-Review

**Spec coverage** (each spec section -> task): §1-2 archetype/no-new-machinery -> the §E-shape section + Global Constraints. §3 three crops shared shape -> Tasks 1/3/4 clone-sweet-corn. §4 dry-down harvest ladder -> Task 1 Step 2 (+ 3/4). §5 12 regions + Option C -> Task 1 Step 3 (+ 3/4 Step 2). §6 per-crop identity/DTM/varieties/cross-poll -> Tasks 1/3/4 Step 1. §7 sourcing -> the sourcing-note steps + T1 constraint. §8 gates/footprint/RED -> Task 2 (RED) + Task 5 (battery/footprint). §9 scope-out (sorghum/broom-corn/no-new-gate/no-hero) -> Global Constraints + honored (nothing builds a gate/field/flat-variety). §10 success criteria -> Task 5/6 battery. §11 open items (slugs/DTM/varieties/heat_pause) -> resolved in Tasks 1/3/4 + the Task 6 Trevor checkpoint.

**Placeholder scan:** the crop field VALUES (regional dates, variety notes, thresholds) are authored content + T1 research (the deliverable), not code placeholders; their structure, method, deltas, and validation gate are fully specified. The DTM bands + variety picks are Trevor-ratified at the Task 6 checkpoint (spec §11). No "TBD"/"similar to Task N" (Tasks 3/4 restate the method).

**Type consistency:** `field-corn`/`popcorn`/`flint-corn` slugs, the 9-stage `growth_stages` id chain, `planting_layout:"block"` + `pollination_block_min_rows:4`, omitted `harvest_window_days`, legacy `varieties.recommended[]={name,days_to_maturity,note}`, and the 12-region set are used identically across Tasks 1/3/4/5. The builder's 3 add ops (`$.crops[125..127]`) match the 3 scratch files.
