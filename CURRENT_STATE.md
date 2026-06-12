# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**7 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, **lemon**) of a ~18 target. **LEMON CERTIFIED 2026-06-12 -- anchor 7, the FIRST evergreen / first citrus.** The two-axis evergreen model is proven end-to-end (design -> build -> region -> biology -> cert, all in one day). **NEXT = anchor 8 = orange-navel** (the heat-accumulation gate).

## Canonical pointer
- **Current SHA:** `670f14fa37fe6f8d7c18cb0b90d21dd46b5d8369c434de208ea8bc61bd0e6b4e`. `LATEST.txt` session: `lemon_cert` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)

## What just happened (session `lemon_cert`)
- **LEMON CERTIFIED** (`f1fce747`->`670f14fa`), anchor 7, the 7th of ~18, the FIRST evergreen. whole_crop_gate lemon = **0**.
- **Steps 9-11:** anchoring closed (4 gaps -> 0, from the catalog) + `verified`-format normalized (145 `true` -> the date convention; lemon was the lone outlier -> the evergreen exemplar now seeds the right format); variety-attribution resolved (precedent: no per-entry sources, matches peach/apple); verbatim scan = 1 real HARD prose lift (`rootstock_options[1].traits_seasoned` vs TAMU) **Trevor-approved reword** (fuller rewrite, cleared a masked 2nd lift in the same field) -> 0 real lifts (the 1 remaining HARD = source name == doc title, benign citation); the flip (`verified_gs_arc` + both `launch_ready`).
- **open_findings filed (all blocks_launch:false):** `lemon_app_enum_dependency` (the 7 new citrus enum values -> iOS-app track owed), `lemon_start_method_sources_slot` (schema), `lemon_rotation_shape` (perennial rotation owed, shared), `lemon_verbatim_uncovered` (postharvest.ucdavis 403).
- Only lemon changed; no catalog change (94); 6 prior anchors byte-identical; release_verify 10 CONCERN = intentional evergreen-vs-annual key-diffs; pre-commit clean.

## Active work + next step
- **NEXT = anchor 8 = orange-navel** (the SECOND evergreen). Rides lemon's evergreen rails (the model + gates are built + cert-proven) -- a compression repeat -- EXCEPT the one genuinely-new piece: the **heat-accumulation gate** (`heat_summer_basis` climate datum + the cool-summer no-fruit branch), built **test-first at orange's Step 3.5** (the way lemon's cold-only model was built). orange = `gating_factors:["cold_hardiness","heat_accumulation"]`.
- Roster: 7 certified; ~11 remaining (orange-navel next, then avocado-maybe, blueberry, strawberry + the 9 annual/indoor hubs).

## OWED
- **iOS-app forward dependency** (`lemon_app_enum_dependency`): support the 7 new citrus enum values (notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`).
- **Tooling:** exclude `sources_summary[].name` from the verbatim scan (a source name should equal its doc title -> spurious HARD hit); fold the region-meta + `verified`-date conventions into `_build_tree_shells` / the apply for future trees; `apply_patch` reject-bare-slash hardening.
- **Schema:** start_method/moon_phase_preference sources-slot decision; perennial-aware `rotation` shape (shared peach/apple/lemon); Appendix A growth_stages `timing_*` reconcile (peach/apple fork; trees match apple).
- Carried: apple's 4 open_findings.

## Gate record (generated 2026-06-12, on canonical `670f14fa`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf / lemon: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **7 certified anchors: 10/10 filled** (lemon: evergreen regions + 6 biology surfaces + 65 register fields, all complete).

## Flip gates (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf / lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **7 anchors certified.** (Target denominator is a roadmap call -- ~18.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN model -- PROVEN end-to-end on lemon (2026-06-12):** `perennial_evergreen` calendar_basis + crop-level `gating_factors`; cold-gated climate = `min_winter_temp_f`; calendars DERIVED (`derive_evergreen_calendar`, A4-gated, no `dormant`, wrap-aware); z9 resolved per-region by frost; survives_no_fruit = honest empty; tropical year-round = `year_round:true` + harvest fill (A4 skips); the 6 biology surfaces = apple shape (single `timing`). Evergreen = 2 anchors (lemon 7 cold-only DONE, orange-navel 8 = +heat). Enum vocab grows per crop (REUSE canonical for existing concepts; new app-affecting values w/ Trevor's bless + an iOS-app forward-dep flag).
- **Cert mechanics:** anchoring `verified` = a DATE (not `true`); verbatim scan is flip-blocking on >=8-word HARD prose lifts (reword w/ Trevor; a masked lift can hide behind another -- re-scan after each reword; source-name==title is benign); crop-SHA cross-check falls back to the collateral leaf-diff if claude.ai's hash method diverges.
- variety-delta = CATEGORICAL; register-fill is a cert dimension; patch paths = leading-slash/dot; pre-cert anchoring = admission state (`drop_precert_anchoring`); claude.ai self-checks (dash/enum/SHA) are advisory -- Claude Code re-verifies, the gates are the defense.
