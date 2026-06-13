# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, **orange-navel**) of a ~18 target. **ORANGE-NAVEL CERTIFIED 2026-06-12 -- anchor 8, the SECOND evergreen, the HEAT-gate crop; the heat-accumulation model proven end-to-end.** **NEXT = anchor 9, a ROADMAP CALL (Trevor): demand-first `basil` (Herbs) + `zinnia` (Flowers) per go-live (annual template, no new UI); then the indoor + family hubs + `blueberry`/`strawberry`. grapefruit/lime/mandarin/avocado/olive are bot-derivable deltas or parked -- NOT roster anchors (orange is the heat EXEMPLAR they derive from).**

## Canonical pointer
- **Current SHA:** `a0cc0178d95e4f6a31b7e4a4b425653ccc793e033cdcfc376878d473e2c4dbfa`. `LATEST.txt` session: `orange_cert` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces (pests/diseases/journey/etc.)

## What just happened (session `orange_cert`)
- **ORANGE-NAVEL CERTIFIED** (`7b2f8179` -> `a0cc0178`), anchor 8, the 8th of ~18, the SECOND evergreen. orange crop-SHA `1d8f026d`. whole_crop_gate orange = PASS, G flip-state = verified_gs_arc + both launch_ready true + 0 open-finding blockers.
- **The cert verbatim (two passes):** (1) **source-verbatim CLEAN** -- 0 HARD lifts from cited sources (17/22 URLs covered; 5 not-covered filed). (2) **lemon-echo reworded** -- the cert flagged orange's shared-citrus prose converging with the certified lemon (HLB/sooty-mold/watering/pests, 9-13 word runs); Trevor chose REWORD for distinctiveness; claude.ai reworded 28 passages (facts/dates held exact; 3 numeric enrichments -- zones 9-11, 27°F, >95°F -- all accurate + consistent), 31 -> 5 residual benign-irreducible (3 plant_out windows + the feeding-season window + 1 generic construction; adjudicated convergence-not-lift). Targeted re-scan: the reworded strings introduce 0 new source lifts.
- **THE FLIP:** `verification_status` = status verified_gs_arc, phase phase_3_orange_gold_standard_arc, both launch_ready true, source_set (9 IDs), verification_log_ref, + 6 open_findings (all blocks_launch:false). `last_reviewed`/`last_reviewed_session` set.
- Only orange changed; lemon byte-identical; release_verify 10 CONCERN = the intentional evergreen+heat key-diffs vs lemon (orange = lemon + heat). register_fill 0, register_completeness PASS, A3/A4 0.

## Active work + next step
- **THE TWO-AXIS EVERGREEN MODEL IS COMPLETE:** both evergreen anchors certified -- lemon (cold-only) + orange (cold + HEAT). The heat-accumulation gate (`heat_summer_basis` + the cool-summer no-fruit branch in perennial_gate) is built, cert-proven, and ready to replicate. orange = the heat exemplar for **grapefruit** + the rest of the citrus/heat-gated pipeline.
- **NEXT = anchor 9 -- a ROADMAP CALL (Trevor).** ~10 anchors remain, all from the locked GS-18 roster: **9 annual/indoor hubs** (basil, zinnia, microgreens-mix, broccoli, bell-pepper, zucchini-courgette, onion, green-beans-bush, oyster-mushroom[maybe-cut]) + **2 perennials** (blueberry, strawberry). Recommended order (demand + archetype-coverage): (1) **basil** + (2) **zinnia** -- the ONLY crops with search demand (herbs/flowers, go-live) and they render on the existing annual template; (3) **microgreens-mix** -- the never-exercised `non_seasonal_indoor` archetype, needed in the set BEFORE the bots derive (else frost-blind); (4-8) the family hubs for bot per-family coverage; (9) **blueberry** (chill-gated, rides peach/apple rails -- fast); (10) **strawberry** (new renovation archetype -- depth, do last). grapefruit/avocado/lime/mandarin/olive = bot-derived deltas or parked, NOT anchors.
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; net-new UI; now have 4 certified trees to template from).

## OWED (orange open_findings + carried)
- **orange_app_enum_dependency** (blocks_launch:false): the citrus enum values incl. the Trevor-ratified `guard_against_heat_stress` as a NOTIFICATION action (not only weather) drive the iOS engine; app must support them.
- **orange_verbatim_uncovered:** 5 cited URLs not text-compared (L2304 301, arizona 403, mgsantaclara 404, ctahr PDF, lsu 404).
- **orange_biology_band_edge_confirm:** se_gulf/warm_arid winter-low band EDGES + the >95°F heat-spike specific (consistent w/ az1850's 90s°F, but az1850 was a not-covered URL).
- **orange_lemon_echo_residual:** 5 benign 8-9w convergences w/ lemon (plant_out/feeding windows + generic phrasing), adjudicated not-a-lift.
- **Shared/carried:** orange_rotation_shape + orange_start_method_sources_slot (perennial-aware rotation + the slot-less-container sources decision -- shared w/ lemon/peach/apple).
- **Tooling:** region-meta fill + calendar derivation + granular-anchoring->portal reconciliation are still one-off transforms each tree; fold into a reusable evergreen-apply step (FLAG B). For the next tree kickoff: ship the lemon field shapes + curated sources + the portal-anchoring convention.

## Gate record (generated 2026-06-12, on canonical `a0cc0178`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf / orange-navel: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **all 8 certified anchors: 10/10 region cells filled** (orange-navel: evergreen+heat, 15 fruiting cells + 5 unsuitable).

## Flip gates (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf / orange-navel:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **8 anchors certified.** (Target denominator is a roadmap call -- ~18.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven on 2 anchors (lemon cold-only, orange cold+heat):** `perennial_evergreen` + `gating_factors`; cold = `min_winter_temp_f`/`cold_basis_*`; heat = `heat_summer_basis` (`{high|adequate|marginal|insufficient}`, no GDD) + `heat_basis_*`; calendars DERIVED; THREE no-fruit directions (chill Goldilocks / cold monotone / heat FLOOR). Hero verdict: heat `marginal` -> suitability `marginal` (reduced quality NOT failure); `insufficient`+`survives_no_fruit` for true non-sweetening. Heat fields need NO register ruling. Ready to replicate to grapefruit.
- **CERT mechanics (reconfirmed orange):** source-verbatim (vs cited URLs) is the flip gate (0 HARD); a SIBLING-CROP echo (orange vs certified lemon on shared citrus facts) is a SEPARATE quality call -- routed to Trevor (voice lane), reworded for distinctiveness, residual formulaic fact-windows adjudicated benign. `verified`=DATE not true. The cert FLIP = `verification_status` block (status/phase/date/launch_ready x2/last_audited/source_set/verification_log_ref/open_findings) + top-level last_reviewed/_session; open_findings all blocks_launch:false.
- **ANCHORING convention:** pests/diseases anchor via the catalog PORTAL id (`uc_ipm`) + the specific URL, NOT granular sub-ids; a cited source MUST be anchored (gate F); Claude Code reconciles claude.ai's granular drift at apply.
- **DERIVATION (`tree_calendar._months`):** parse ONLY before the first "(" (parenthetical prose carries stray months + "may"; A4 cannot catch a bad-source-date calendar).
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks (dash/enum/SHA/source-count) are advisory -- the gates are the defense.
