# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**7 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon) of a ~18 target. **ORANGE-NAVEL = anchor 8 IN PROGRESS -- the SECOND evergreen, the HEAT-gate crop.** Steps 1-3 (sources + 2.9 evergreen scalars + biology prose + varieties + companions) RELEASED 2026-06-12. **NEXT = orange Step 3.5 (Claude Code): the heat-accumulation gate, built test-first.**

## Canonical pointer
- **Current SHA:** `43f2f44f2f5d9fefe717b2010b8e2ae828f2aa641364bf773646d22e928b43e3`. `LATEST.txt` session: `orange_navel_steps1_3` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces (pests/diseases/journey/etc.)
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- 42 null register fields; register-complete

## What just happened (session `orange_navel_steps1_3`)
- **ORANGE-NAVEL Steps 1-3 RELEASED** (`670f14fa` -> `43f2f44f`), opening anchor 8 (the SECOND evergreen, the heat-gate crop). 49-op patch: 9 citrus T1 sources (no minting; all in the 94-entry catalog), the 2.9 evergreen scalars, **`gating_factors: ["cold_hardiness","heat_accumulation"]`** (the new axis vs lemon's cold-only), pollination (self-fertile + parthenocarpic), 3 citrus rootstocks, 4 navel varieties, 5 `_seasoned` biology surfaces, companions.
- **A first cut was HALTed by `register_completeness`** on two field-shape divergences from the lemon exemplar: `pruning_window` shipped as a bare string (lemon = object) and `varieties.recommended[]` used a novel unruled `note` key (lemon = the rich per-variety schema). **Re-cut to lemon shapes:** `pruning_window` -> object (byte-parity w/ lemon: `month_band:["spring"]`, `offset_from:"after_harvest"`); varieties -> the full lemon schema (`subtitle/use/difficulty/notes_seasoned/recommended_note/delta`), the `note` prose moved into `notes_seasoned`, each navel carrying a `delta` overlay vs Washington (flesh/season/color_dev). **Register gate now PASS.**
- **Release verification:** crop-SHA EXACT match (`a63b5136`); `release_verify` exit 0 (1 CONCERN = the 13 expected `_beginner` deferrals, blocks_launch:false); whole_crop_gate delta = only those deferrals, **no region regression**; 6 prior anchors byte-identical; no catalog / enum change; calendar_basis untouched at `frost_anchored` (3.5 flips it).
- **open_findings (all blocks_launch:false):** `orange_heat_gate_unbuilt` (resolved at Step 3.5), `orange_beginner_surfaces_owed` (the 5 `_seasoned` surfaces + pruning_window.note_seasoned authored; all `_beginner` siblings deferred to Steps 7-8).

## Active work + next step
- **NEXT = orange Step 3.5 (Claude Code-owned, the model build):** flip `calendar_basis -> perennial_evergreen`, build the evergreen region shells, and build the genuinely-new **HEAT-ACCUMULATION gate TEST-FIRST** -- the `heat_summer_basis` climate datum + a cool-summer no-fruit branch in `perennial_gate`, keyed on `gating_factors` containing `heat_accumulation`. The heat floor is the INVERSE of lemon's cold-only model: a cool-summer cell SURVIVES + may set fruit but stays sour/pale, so fruit-quality is heat-gated on top of the cold-survival ceiling. (Lemon's `perennial_gate` no-fruit DIRECTION SPLIT is keyed on `gating_factors`: chill-gated = chill Goldilocks band; cold-only evergreen = monotone, no band; **orange adds the third direction = a heat floor.**)
- Then **Steps 4-5** (region biology, 10 cells), **6A/6B** (biology surfaces + register fill), **cert**. orange = the heat exemplar for grapefruit + the rest.
- Roster: 7 certified; orange-navel anchor 8 in progress; ~10 remaining (then avocado-maybe, blueberry, strawberry + the 9 annual/indoor hubs).

## OWED
- **iOS-app forward dependency** (`lemon_app_enum_dependency`): support the 7 citrus enum values (notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`). Orange may add heat-gate-related app surfacing at 3.5+.
- **Tooling:** exclude `sources_summary[].name` from the verbatim scan; fold the region-meta + `verified`-date conventions into `_build_tree_shells` / the apply for future trees; `apply_patch` reject-bare-slash hardening.
- **Process (NEW 2026-06-12):** claude.ai authored two field shapes off-exemplar on the first orange cut (`pruning_window`, `varieties.recommended[]`) because the canonical lemon crop is not in its context -- it works from the kickoff description. **Include the exact lemon field shapes (the `pruning_window` object + the per-variety schema) in the next tree kickoff** to prevent the round-trip.
- **Schema:** start_method/moon_phase_preference sources-slot decision; perennial-aware `rotation` shape (shared peach/apple/lemon); Appendix A growth_stages `timing_*` reconcile (peach/apple fork; trees match apple).
- Carried: apple's 4 open_findings.

## Gate record (generated 2026-06-12, on canonical `43f2f44f`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lemon: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- (orange-navel: mid-arc, 23 violations = 10 region-unfilled shells + 13 `_beginner` deferrals; expected, not certifiable until cert.)

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- (orange-navel: 0/10 -- region shells built at Step 3.5, filled at Steps 4-5.)

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
- **EVERGREEN model -- PROVEN end-to-end on lemon (2026-06-12):** `perennial_evergreen` calendar_basis + crop-level `gating_factors`; cold-gated climate = `min_winter_temp_f`; calendars DERIVED (`derive_evergreen_calendar`, A4-gated, no `dormant`, wrap-aware); z9 resolved per-region by frost; survives_no_fruit = honest empty; tropical year-round = `year_round:true` + harvest fill (A4 skips); the 6 biology surfaces = apple shape (single `timing`). Evergreen = 2 anchors (lemon 7 cold-only DONE; **orange-navel 8 = +heat, IN PROGRESS**). The no-fruit DIRECTION SPLIT in `perennial_gate` is keyed on `gating_factors`: chill-gated = chill Goldilocks band; cold-only evergreen = monotone (no band); **orange's `heat_accumulation` adds a heat FLOOR (the cool-summer no-fruit branch), built test-first at orange 3.5.** Enum vocab grows per crop (REUSE canonical for existing concepts; new app-affecting values w/ Trevor's bless + an iOS-app forward-dep flag).
- **TREE per-variety schema (the evergreen/tree `varieties.recommended[]` shape):** rich objects (lemon = `{name, subtitle, use, difficulty, bloom_group, bloom_window_relative, bloom_duration_days, chill_hours_required, notes_seasoned, recommended_note, delta}`; apple = the minimal subset). Annuals (cherry/carrot) leave `recommended[]` empty and use `varieties_detail[]`. The schema-2.9 **variety-delta** (`delta.<attr>.{value,parent,changed}`) is ruled USER-FACING-CATEGORICAL (value/parent bare categorical, changed bool) -- the register treatment for the whole varietal-expansion model. A bare `note` on a variety entry is NOT a ruled field (it HALTs `register_completeness`).
- **Cert mechanics:** anchoring `verified` = a DATE (not `true`); verbatim scan is flip-blocking on >=8-word HARD prose lifts (reword w/ Trevor; a masked lift can hide behind another -- re-scan after each reword; source-name==title is benign); crop-SHA cross-check falls back to the collateral leaf-diff if claude.ai's hash method diverges. **`register_completeness_gate` reads `crops_data_final.json` by default -- pass the candidate file explicitly when gating a scratch.**
- variety-delta = CATEGORICAL; register-fill is a cert dimension; patch paths = leading-slash/dot; pre-cert anchoring = admission state (`drop_precert_anchoring`); claude.ai self-checks (dash/enum/SHA) are advisory -- Claude Code re-verifies, the gates are the defense.
