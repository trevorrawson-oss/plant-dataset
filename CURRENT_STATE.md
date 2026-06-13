# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**7 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon) of a ~18 target. **ORANGE-NAVEL = anchor 8, STRUCTURALLY COMPLETE -- only cert remains.** Steps 1-3 + 3.5 + 4-5 + **Step 6 (6 biology surfaces + 79 register fields, `whole_crop_gate` PASS)** all RELEASED 2026-06-12. **NEXT = orange cert (9-11, Claude Code): the verbatim scan vs FULL lemon prose + anchoring closure + the flip.**

## Canonical pointer
- **Current SHA:** `7b2f8179d4f585919047ad356b1dfa55f449ac02c65d7c0642dc31bc4a4d36b5`. `LATEST.txt` session: `orange_step6` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces (pests/diseases/journey/etc.)
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)

## What just happened (session `orange_step6`)
- **ORANGE Step 6 RELEASED** (`32b0c6e7` -> `7b2f8179`): the 6 biology surfaces (pests/diseases/growth_stages/failure_diagnostics/weather_triggers/notifications) + the 79 register/care fields, dual-register, heat axis threaded. **`register_fill_gate orange` 79 -> 0; `whole_crop_gate orange` = PASS.** orange crop-SHA `f04ed533`.
- **Catalog reconciliation (Claude Code lane, the apple precedent):** claude.ai's `anchoring_urls` used 11 granular UC IPM per-pest sub-IDs (`uc_ipm_psyllid`/`uc_ipm_hlb`/...) + `uf_ifas_cg009` that are NOT catalog entries (its self-check counted only the `sources` arrays). lemon anchors pests/diseases via the PORTAL `uc_ipm` + the specific URL -> remapped all 13 to `uc_ipm` / `uf_ifas_edis` (kept the URLs), no minting. Also anchored a cited-but-unanchored `uf_ifas_hs132` on diseases[1] (Phytophthora) to its catalog URL. Source-tier gate: uncatalogued 0.
- **Release verification:** whole_crop_gate PASS (A3 heat-floor 0, A4 coherence 0, dual-voice null_values 0, source-tier uncatalogued 0); register_completeness PASS; release_verify exit 0 (CONCERN = the intended 3 heat keys vs lemon; G note = northern_tier z3-7 calendars empty-because-unsuitable, attested cold-decided/derived-not-pasted); dash/temp clean. crop-SHA via leaf-diff (diverges from claude.ai's `8c65825b` by design -- the anchoring reconciliation).
- **NO flip** -- launch_ready stays False; that is cert (9-11).

## Active work + next step
- **NEXT = orange cert (Steps 9-11, Claude Code lane):**
  1. **Verbatim scan vs the FULL lemon crop prose** (flip-blocking). claude.ai only had the SCOPE exemplar items as lemon text and self-de-risked to 0 against those (787->0 n-grams over 4 passes); Claude Code re-runs against lemon's live prose (the surfaces are the main lift risk).
  2. **Anchoring closure** -- confirm every claim-bearing leaf is anchored (whole_crop_gate F already PASS post-reconciliation; re-confirm at cert).
  3. **The se_gulf/warm_arid winter-low band-edge confirm** (carried from 4-5; claude.ai reasoned the edges from damage thresholds).
  4. **THE FLIP** -- `verification_status.status = verified_gs_arc`, `launch_ready_core/seasoned = true`, the phase + log_ref. orange-navel certifies = anchor 8.
- Roster: 7 certified; orange = anchor 8 at the cert gate; ~10 remaining after. orange = the heat exemplar for grapefruit + the rest.

## OWED
- **iOS-app enum -- RESOLVED 2026-06-12 (Trevor ratified):** the `summer_heat_irrigation` notification KEEPS `action:"guard_against_heat_stress"`. Decision: the notification-action namespace INCLUDES the heat-axis action `guard_against_heat_stress` (richer than lemon's generic `water` for the same heat-irrigation reminder; lemon's irrigation notification uses `water`, orange's uses the heat-specific token). **iOS-app forward-dep:** the app must support `guard_against_heat_stress` as a NOTIFICATION action, not only a weather action -- folds into `lemon_app_enum_dependency` (formalized as an orange open_finding at cert). No longer an open question.
- **Tooling:** the granular-anchoring->portal reconciliation + region-meta fill + calendar derivation are still one-off transforms each tree; fold into a reusable evergreen-apply step (FLAG B). The `tree_calendar._months` paren-strip is committed.
- **Process:** ship the exact lemon field shapes + curated citrus sources in every tree kickoff (done for Step 6). For the NEXT tree, also ship the lemon pests/diseases ANCHORING convention (portal `uc_ipm` + URL, not granular sub-IDs).
- **Schema:** start_method/moon_phase sources-slot; perennial-aware `rotation` shape; Appendix A growth_stages `timing_*` reconcile. Carried: apple's 4 open_findings.

## Gate record (generated 2026-06-12, on canonical `7b2f8179`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- (orange-navel: `whole_crop_gate` = **PASS** structurally; register_fill 0; A3/A4 0. NOT flipped -- cert (9-11) adds the verbatim scan + the launch_ready flip.)

## Region fill state (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf: 10/10.**
- (orange-navel: 10/10 evergreen+heat region cells LIVE; all biology surfaces + 79 register fields authored.)

## Flip gates (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **7 anchors certified.** orange-navel = structurally complete, NOT flipped (status None, launch_ready False) -- cert is the next + final step. (Target ~18.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN + HEAT model -- live + register-complete on orange (2026-06-12):** `perennial_evergreen` + `gating_factors`; cold = `min_winter_temp_f`/`cold_basis_*`; heat = `heat_summer_basis` (`{high|adequate|marginal|insufficient}`, no GDD) + `heat_basis_*`; calendars DERIVED; THREE no-fruit directions (chill Goldilocks / cold monotone / heat FLOOR). Hero verdict precedent: heat `marginal` -> suitability `marginal` (reduced quality, NOT failure); `insufficient`+`survives_no_fruit` reserved for true non-sweetening. Heat fields need NO register ruling (forward-tested).
- **ANCHORING convention (lemon precedent, reconfirmed orange Step 6):** pests/diseases/surfaces anchor via the catalog PORTAL id (`uc_ipm`) + the specific page URL in the anchor -- NOT granular per-page sub-ids (`uc_ipm_psyllid`). A cited source in `sources[]` MUST carry a matching `anchoring_urls` entry (whole_crop_gate F). Claude Code reconciles granular->portal at apply (the apple/carrot drift-absorption precedent); claude.ai's source self-count omits anchoring keys -- the gate is the defense.
- **DERIVATION precedent (`tree_calendar._months`):** parse ONLY the primary range before the first "(" -- parenthetical prose carries stray months + the modal verb "may"; A4 cannot catch a bad-source-date calendar.
- **Cert mechanics:** anchoring `verified` = a DATE; verbatim scan flip-blocking at cert on >=8-word HARD lifts (re-scan after each reword; claude.ai only sees scope exemplars, so the FULL-lemon-prose scan is Claude Code's at Step 11); crop-SHA falls back to the collateral leaf-diff (diverges when Claude Code reconciles anchoring/metadata). **`register_completeness_gate` + `register_fill_gate` read `crops_data_final.json` by default -- pass the candidate explicitly when gating a scratch.**
- TREE per-variety schema = lemon's 11-key set incl. `delta` (CATEGORICAL); a bare `note` HALTs register_completeness. claude.ai self-checks are advisory -- the gates are the defense.
