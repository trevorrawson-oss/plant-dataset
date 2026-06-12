# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**7 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon) of a ~18 target. **ORANGE-NAVEL = anchor 8 IN PROGRESS -- the SECOND evergreen, the HEAT-gate crop.** Steps 1-3 + **Step 3.5 (the heat-accumulation gate + evergreen region shells, test-first)** RELEASED 2026-06-12. **NEXT = orange Steps 4-5 (claude.ai authoring): the 10 region cells + the per-cell heat verdicts.**

## Canonical pointer
- **Current SHA:** `dee5de3aa2c00157dff23aa249957af2eb4f95d6e4497b62aa971469e5cf32e1`. `LATEST.txt` session: `orange_step3_5` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces (pests/diseases/journey/etc.)
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus

## What just happened (session `orange_step3_5`)
- **ORANGE Step 3.5 BUILT + RELEASED** (`43f2f44f` -> `dee5de3a`), the genuinely-new piece of anchor 8: the **HEAT-ACCUMULATION gate**, built TEST-FIRST (the v1.0 pattern -- gates built at their step against real shape, not in a vacuum).
- **`perennial_gate.py` heat branch (test-first, 7 new tests):** `HEAT_BASIS_ENUM = {high, adequate, marginal, insufficient}`; a `heat_accumulation` crop enforces the **heat FLOOR** -- a frost-safe (non-`unsuitable`) FILLED cell with `heat_summer_basis:"insufficient"` cannot be `fruits_reliably` (the navel sets fruit but it stays sour); a filled non-unsuitable cell must carry a valid `heat_summer_basis`. This is the THIRD no-fruit direction (vs lemon's cold-only MONOTONE + peach/apple's chill GOLDILOCKS band). Keyed on `gating_factors` -> fires ONLY for orange/grapefruit; peach/apple/lemon byte-identical.
- **`build_region_shells.py` heat climate layer (test-first, fixture 8 + cold-only regression):** when `heat_accumulation` in `gating_factors`, the evergreen shell adds `heat_summer_basis` + `heat_basis_seasoned`/`heat_basis_beginner` (present-null) ALONGSIDE the cold `min_winter_temp_f`/`cold_basis_*`, on both the region-constant layer and each resolved cell. Cold-only evergreens (lemon) get NO heat scaffolding (byte-identical).
- **Data:** orange `calendar_basis` flipped `frost_anchored -> perennial_evergreen`; 10 evergreen+heat region shells built (perennial establishment entry + cold+heat climate layers + reshaped cells), all suitability=null pre-fill.
- **Release verification:** only orange changed (10 regions); A3 (heat-aware perennial gate) = 0 + A4 = 0 on the null shells; whole_crop_gate 23 (the 10 "region unfilled (stub)" CLEARED -> 10 "region_notes both null", a wash, + 13 `_beginner` deferrals carried); release_verify exit 0; register_completeness PASS -- **forward-tested: populating `heat_summer_basis` + the heat_basis prose pair does NOT HALT register_completeness, so Steps 4-5 are unblocked, NO heat ruling owed.** Certified anchors (lemon/peach/apple) regression PASS.

## Active work + next step
- **NEXT = orange Steps 4-5 (claude.ai authoring lane):** the 10 region cells -- per-region `min_winter_temp_f` + `cold_basis_*` AND `heat_summer_basis` (the `{high|adequate|marginal|insufficient}` verdict) + `heat_basis_*`; per-zone `suitability` + `suitability_note_*`; bloom/harvest dates (Claude Code DERIVES the evergreen calendars via `derive_evergreen_calendar`). **The heat story is the region hero:** desert/warm-inland = high/adequate heat -> `fruits_reliably`; cool CA coast = `insufficient` heat -> `marginal`/`survives_no_fruit` (frost-safe, but sour) -- the gate's heat floor enforces this. Then 6A/6B prose, cert.
- Roster: 7 certified; orange-navel anchor 8 in progress (Steps 1-3 + 3.5 done); ~10 remaining after orange. orange = the heat exemplar for grapefruit + the rest.

## OWED
- **iOS-app forward dependency** (`lemon_app_enum_dependency`): support the 7 citrus enum values (notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`). Orange's heat axis (`guard_against_heat_stress`) is already in that set.
- **Tooling:** exclude `sources_summary[].name` from the verbatim scan; fold the region-meta + `verified`-date conventions into `_build_tree_shells` / the apply for future trees (FLAG B: `_build_tree_shells` still leaves `region_id`/`region_label`/`zone_span` null -> Steps 4-5 fills them); `apply_patch` reject-bare-slash hardening.
- **Process:** ship the exact lemon field shapes (the `pruning_window` object + the per-variety schema) in every future tree kickoff -- claude.ai authors off-exemplar because the canonical lemon crop is not in its context.
- **Schema:** start_method/moon_phase_preference sources-slot decision; perennial-aware `rotation` shape (shared peach/apple/lemon); Appendix A growth_stages `timing_*` reconcile.
- Carried: apple's 4 open_findings.

## Gate record (generated 2026-06-12, on canonical `dee5de3a`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lemon: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- (orange-navel: mid-arc, 23 violations = 10 region_notes-null + 13 `_beginner` deferrals; A3/A4 = 0 on the built-but-unfilled evergreen shells; not certifiable until cert.)

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- (orange-navel: 10 evergreen+heat region SHELLS built at Step 3.5; cells filled at Steps 4-5.)

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **7 anchors certified** (launch_ready true + status `verified_gs_arc`). orange-navel = in progress (status None, launch_ready False). (Target denominator is a roadmap call -- ~18 -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN model -- PROVEN end-to-end on lemon; HEAT axis now BUILT on orange (2026-06-12):** `perennial_evergreen` calendar_basis + crop-level `gating_factors`; cold-gated climate = `min_winter_temp_f`; **heat-gated climate = `heat_summer_basis` (qualitative `{high|adequate|marginal|insufficient}` verdict, NO GDD per spec) + `heat_basis_*` prose pair**; calendars DERIVED (`derive_evergreen_calendar`, A4-gated, no `dormant`, wrap-aware); z9 resolved per-region by frost; survives_no_fruit = honest empty; tropical year-round = `year_round:true` + harvest fill. **The `perennial_gate` no-fruit DIRECTION SPLIT is keyed on `gating_factors` -- THREE directions now:** chill-gated = chill Goldilocks band; cold-only evergreen = monotone (no band); **heat_accumulation = a heat FLOOR (insufficient summer heat caps a frost-safe cell below `fruits_reliably`).** Heat branch fires ONLY for orange/grapefruit (gating-keyed); the others stay byte-identical. Enum vocab grows per crop (REUSE canonical; new app-affecting values w/ Trevor's bless + an iOS-app forward-dep flag).
- **TREE per-variety schema (`varieties.recommended[]`):** trees use rich objects (lemon = `{name, subtitle, use, difficulty, bloom_group, bloom_window_relative, bloom_duration_days, chill_hours_required, notes_seasoned, recommended_note, delta}`; apple = the minimal subset). Annuals leave `recommended[]` empty + use `varieties_detail[]`. The schema-2.9 **variety-delta** (`delta.<attr>.{value,parent,changed}`) is ruled USER-FACING-CATEGORICAL. A bare `note` on a variety entry is NOT ruled (it HALTs `register_completeness`).
- **Cert mechanics:** anchoring `verified` = a DATE (not `true`); verbatim scan is flip-blocking on >=8-word HARD prose lifts (reword w/ Trevor; re-scan after each reword; source-name==title is benign); crop-SHA cross-check falls back to the collateral leaf-diff. **`register_completeness_gate` reads `crops_data_final.json` by default -- pass the candidate file explicitly when gating a scratch (else a false PASS).**
- variety-delta = CATEGORICAL; register-fill is a cert dimension; patch paths = leading-slash/dot; pre-cert anchoring = admission state (`drop_precert_anchoring`); claude.ai self-checks (dash/enum/SHA) are advisory -- Claude Code re-verifies, the gates are the defense.
