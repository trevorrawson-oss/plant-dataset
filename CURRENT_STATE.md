# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Step 3.5 DONE -- the TREE region/calendar model BUILT (anchor 5, the first PERMANENT tree, Stone Fruit hub). The 10 region cells were reshaped from the annual sowing-window model to the TREE model: a per-zone `suitability` verdict where **survives != fruits is FIRST-CLASS** (`fruits_reliably`/`marginal`/`survives_no_fruit`/`unsuitable`), a region `chill_hours_delivered` adequacy band (gates which varieties fruit), a single `track:"perennial"` establishment entry, and the bloom -> fruit -> harvest -> dormant-prune `calendar[]`. **`calendar_basis` flipped `frost_anchored` -> `perennial_chill_gated`.** Shells are EMPTY + structurally at-bar (region-unfilled = admission state, the IDENTICAL pattern carrot Step 3.5 ended on), PENDING Step 4 region biology. **4 anchors certified** (cherry/beefsteak/carrot/lettuce); peach = anchor 5 in progress. (Anchor TARGET ~18, a roadmap call -- do not hardcode the denominator.)

## Canonical pointer
- **Current SHA:** `e99001f2e70cf3b57b4b1c7ac74be788ca649dfb3a7c69b8e1c5a47d6fc1c919`. `LATEST.txt` session: `peach_step3_5` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells

## What just happened (2026-06-10, session `peach_step3_5` -- Claude Code structural lane, NEW territory)
- **Designed + ratified the TREE region/calendar model** (`docs/tree_region_model_scope_v0.md`; Trevor "Let's do it" on all 4 decisions). A permanent tree is planted ONCE and lives for decades, so the annual frost-anchored sowing-window model is a category error. What varies by place: hardiness/suitability (survives vs fruits-reliably, two bands), winter CHILL adequacy (which gates the variety set -- peach's 8 varieties span 400-1,050 chill hrs), and the absolute phenology dates of the recurring bloom->harvest->dormant-prune cycle. The two-layer cut (region-constant rule + zone-resolved render) + the outer container are KEPT; the inner calendar model is swapped. **Like 2.9, this formalizes an existing null scaffold:** the crop-level `hardiness_zone_min/max` + `reliable_fruit_zone_min/max` + `hardiness_notes_*` already existed scaffolded-null (the apple two-band data); Step 4 fills them.
- **Built peach's 10 tree region shells** (test-first; `build_region_shells.py` extended with `_is_tree` -> `_build_tree_shells`). Per region: a single `track:"perennial"`/`label:"establishment"` rule entry (`plant_out`/`bloom`/`harvest_start`/`harvest_end` rule lists, no succession/start_indoors); `chill_hours_delivered`[] + `chill_basis_*`. Per resolved cell: the tree key-set -- `suitability` + `suitability_note_*` (survives!=fruits slot), `chill_hours_delivered`, `bloom`/`harvest`/`plant_out` render keys (reused annual names -> uniform renderer), tree `calendar[]`, `frost_risk_note_seasoned`, `resolved_from`/`resolution_method`; annual-only keys (start_indoors/lifted_from_zone/nested plantings/first-last_plant_date/notes) STRIPPED; empty `sources_pending_admission` residue swept (carrot precedent). `calendar_basis` set to `perennial_chill_gated`.
- **Verification (protocol #6):** whole_crop_gate peach = 10 (ALL region_notes-null = admission state; **stub/null-track/stale = 0** -> tree SHAPE at-bar); base was 10 (stub/missing) -> a 1:1 region-unfilled KIND-swap, count conserved (release_verify flagged it; adjudicated benign -- identical to carrot Step 3.5's documented end-state). release_verify collateral CLEAN (only peach changed, no top-level/catalog change, lettuce byte-identical). register PASS (new tree prose fields are suffix-ruled or already-excluded -> 0 new unruled patterns; `suitability` was already an EXCLUDED enum). cherry/beefsteak/carrot/lettuce PASS. Tool suite 9/9 green. Promoted `e99001f2`.

## Active work + next step
- **NEXT = peach Step 4 (claude.ai authoring):** fill the tree shells from peach's pomology sources -- per-region `chill_hours_delivered` + `chill_basis_*`, per-zone `suitability` verdicts (the survives!=fruits calls), absolute bloom/harvest/plant dates, the tree `calendar[]` arrays, `frost_risk_note_seasoned`, region_notes; AND the crop-level `hardiness_zone_min/max` + `reliable_fruit_zone_min/max` + `hardiness_notes_*` (the apple two-band hardiness strip). The shape this session locked is what they fill. Hawaii peach is the model's honesty test (`suitability:"unsuitable"`, no fabricated window).
- **OWED methodology promotions (PK refresh):** promote `tree_region_model_scope_v0` -> `05-methodology/current/tree_region_model_spec_v1_0.md`; a **v1.8 checklist amendment** folding the `perennial_chill_gated` `calendar_basis` value + the **`dormant` calendar state** (13->14 enum, Trevor-ratified, additive; USED when Step 4 authors calendars) + the perennial Step-5.5 gate branch. (No code enforces the calendar enum yet, so `dormant` is a doc amendment, not a dataset change.)
- **DEFERRED to peach Step 11 (cert, when fill exists + is testable):** the `whole_crop_gate` perennial CERT branch (one-establishment-entry / no-succession / suitability-present-and-filled invariants). At Step 3.5 the gate already behaves correctly (reports region-unfilled), so no untested cert-gate change ships against empty shells. register_completeness needs NO change (confirmed).
- **FLAG 1 (rootstock `selection_basis`, for Trevor):** per-archetype enum (`size`[pome] | `soil_pest_tolerance`[stone]); peach rootstocks select by soil/nematode tolerance, not size. DEFER until apple gives the pome data point + a renderer consumer. Untouched by the tree region model.
- **PARKED (unchanged):** WeatherKit; USCRN; C1 register-reshape + C3 vocab value-reconcile; 2.9 per-anchor back-fill; soil `_seasoned` texture back-fill (peach Steps1-3 owed); evergreen/citrus `calendar_basis` variant (decided at the lemon anchor).

## Gate record (generated 2026-06-10, on canonical `e99001f2`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **4 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails (carry into peach Step 4 + every tree/perennial anchor)
- **TREE REGION MODEL (peach Step 3.5, the FIRST tree -- `docs/tree_region_model_scope_v0.md`).** A permanent tree's region cell answers *can I grow it here + which varieties* (region `chill_hours_delivered` band + per-zone `suitability` verdict); the zone answers *exactly when it blooms/fruits/goes dormant* (resolved bloom/harvest/plant dates + the tree `calendar[]`). `calendar_basis = perennial_chill_gated`. plantings[] = exactly ONE `track:"perennial"` establishment entry (no succession/second_planting/start_indoors -- a tree is planted once). Render keys REUSE the annual names (plant_out/bloom/harvest_*) so the resolved-cell renderer is shared. The model feeds the apple-zone-6.html 3-track Gantt (hardiness band + chill block + per-variety bloom Gantt + Plant/Bloom/Harvest calendar).
- **SURVIVES != FRUITS is FIRST-CLASS (Trevor, explicit 2026-06-10).** A tree can survive a zone yet not set a reliable crop there. Encoded at TWO levels: crop-level `hardiness_zone_min/max` (survives) vs `reliable_fruit_zone_min/max` (fruits) -- distinct fields, never collapsed; per-zone `suitability` enum `fruits_reliably`/`marginal`/`survives_no_fruit`/`unsuitable`. This also gives the region grid HONEST "doesn't-grow-here" cells (Hawaii peach = `unsuitable`, no fabricated window -- no `year_round` patch needed).
- **PEACH/tree biology:** SELF-FERTILE (do not import apple's needs-pollinizer -> the cross-pollination section degrades to "one tree fruits"); chill is VARIETY-driven (crop `chill_hours_required` null + `chill_hours_range` [200,1050] = "varies, see varieties", apple-mock convention); rootstocks select by SOIL/NEMATODE tolerance, not size (FLAG 1). `dormancy_window`/`pruning_window` month-band shape RATIFIED at crop level (coarse default; the region `calendar[]` resolves the actual prune/dormant months per place -- NOT reshaped to frost-relative).
- **`dormant` calendar state (RATIFIED, owed in the v1.8 checklist):** deciduous winter dormancy is a real renderer state distinct from `cold_pause` (a growing crop paused between sowings). 13->14 enum, additive; the prune-window month renders `prune`, other dormant months `dormant`.
- **SCHEMA 2.9 model (unchanged):** crop = entity/guide/URL; variety = DELTA overlay; bloom-overlap calendar rides curated `varieties.recommended[]` (peach has 8, 400-1050 chill, NO Phase-5 dep); perennial fields FLAT null-by-archetype; migrations additive null-scaffold (never un-earn a cert).
- **CANONICAL SUB-OBJECT SHAPES (claude.ai must match; Claude Code cleans on release):** `anchoring_urls = {source_id:{url,verified}}`; soil texture = snake_case enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to a temp then `mv` -- `>` truncates the header source before read).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes/migrations, catalog mints, the flip) + owns data SHAPE/naming + builds the renderer. Run protocol #6 + roster gate + verbatim scan before every promote/flip. **Dataset push is autonomous** (announce-then-execute); plant-astro merge stays Trevor-gated.
