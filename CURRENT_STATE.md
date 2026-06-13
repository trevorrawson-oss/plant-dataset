# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**7 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon) of a ~18 target. **ORANGE-NAVEL = anchor 8 IN PROGRESS -- the SECOND evergreen, the HEAT-gate crop.** Steps 1-3 + 3.5 (heat gate) + **Steps 4-5 (the 10 evergreen+heat region cells, LIVE)** RELEASED 2026-06-12. **NEXT = orange 6A/6B (claude.ai authoring): the biology surfaces + register/care fields.**

## Canonical pointer
- **Current SHA:** `32b0c6e742393902e55b1fef4192d5a75910bfe189ccfea65d3bcbfa55b120a6`. `LATEST.txt` session: `orange_steps4_5` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces (pests/diseases/journey/etc.)
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)

## What just happened (session `orange_steps4_5`)
- **ORANGE Steps 4-5 RELEASED** (`dee5de3a` -> `32b0c6e7`): the 10 evergreen+heat region cells authored (claude.ai) + applied + region metadata filled + calendars DERIVED (Claude Code). orange's regions are LIVE. orange crop-SHA `6ac3ae4a`.
- **The heat story is live, gate-honest:** desert (`ca_desert`/`low_desert_az`) + Central Valley (`ca_interior` z9) = `high` heat -> `fruits_reliably`; Gulf/FL/warm = `adequate`; **the HERO contrast -- `ca_south_coast` = heat `marginal` -> `marginal`** (the same coast that grows flawless lemons leaves a navel only middling; corrected from the kickoff's over-framed `survives_no_fruit` per UC IPM + Santa Clara MG -- coast is sub-optimal, NOT failure); `ca_north_coast` = `insufficient` -> `marginal`; Hawaii = `marginal` (no cool nights, stays green, per CTAHR). northern_tier z3-7 = `unsuitable` (frost). A3 heat-floor = 0 (no `insufficient` cell is `fruits_reliably`).
- **A derivation bug caught + fixed test-first** (`tree_calendar._months`): the harvest field doubles as display + derivation source, and claude.ai's descriptive parentheticals carried stray months ("...can start late October") + the modal verb "may" ("rind may stay green"), which corrupted the parsed harvest span (low_desert_az read Dec->Oct; fl_peninsula read Nov->May) -- and A4 would NOT have caught it (it parses the same way). Fix: parse only the primary range before the first "(". RED watched fail (E8); GREEN; **0 certified cells affected** (byte-identical regression on lemon/peach/apple).
- **Release verification:** A3 (heat floor + no-fruit) = 0; A4 (calendar coherence) = 0; whole_crop_gate 23 -> 13 (the 10 region_notes-null CLEARED; the 13 residual = the top-level `_beginner` deferrals owed to 6-8); release_verify exit 0 -- vs the EVERGREEN exemplar (lemon) orange differs by ONLY the 3 heat keys (`heat_summer_basis`/`heat_basis_seasoned`/`heat_basis_beginner`), confirming orange = lemon + heat; dash/temp scans clean. crop-SHA cross-check used the collateral leaf-diff (claude.ai's slice-only SHA diverges by design -- CC fills region metadata + derives calendars).

## Active work + next step
- **NEXT = orange 6A/6B (claude.ai authoring lane):** 6A = the biology surfaces (pests/diseases/growing-journey/companions-detail/etc., apple/lemon shape -- 6 surfaces); 6B = the register/care fields (watering/container/fertilizer/storage/the 2.9 perennial prose). Then 9-11 cert. orange = the heat exemplar for grapefruit + the rest.
- **Step-5 biology confirm owed (non-blocking):** claude.ai reasoned the `se_gulf`/`warm_arid` winter-low BAND EDGES from documented citrus damage thresholds rather than a single zone table (the qualitative claims are sourced); confirm the numeric `[low,high]` edges against the cited sources at the cert side-by-side. Verbatim scan (cited-URL prose lifts across the new region prose) runs at cert (Step 11).
- Roster: 7 certified; orange anchor 8 in progress (1-3 + 3.5 + 4-5 done); ~10 remaining after orange.

## OWED
- **Tooling (recurring evergreen-tree release steps, currently ad-hoc):** region_id/region_label/zone_span fill + the per-cell `calendar[]` derivation are done by a one-off release transform each tree (lemon + orange both). Fold into a reusable `_build_tree_shells`/apply step (FLAG B). The `tree_calendar._months` paren-strip is now committed.
- **iOS-app forward dependency** (`lemon_app_enum_dependency`): the 7 citrus enum values incl. `guard_against_heat_stress` (orange's heat axis).
- **Process:** ship the exact lemon field shapes in every tree kickoff (claude.ai authors off-exemplar -- the canonical lemon crop is not in its context). The Steps 4-5 sources file's stale `orange_sources_summary.primary` scaffold caused a catalog misread -- regenerate the `primary` for the next tree handoff.
- **OPTIONAL mint (Trevor's call, not blocking):** pub-level `az_ext_az1850` (Glenn Wright); `az_coop_ext` portal covers it and is gate-clean.
- **Schema:** start_method/moon_phase sources-slot; perennial-aware `rotation` shape; Appendix A growth_stages `timing_*` reconcile. Carried: apple's 4 open_findings.

## Gate record (generated 2026-06-12, on canonical `32b0c6e7`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- (orange-navel: mid-arc, 13 violations = the top-level `_beginner` deferrals owed to 6-8; A3 heat-floor = 0, A4 coherence = 0; regions LIVE, not certifiable until cert.)

## Region fill state (generated)
- **cherry-tomato: 10/10**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10**; 8 heat_pause, 6 second_planting
- **carrot: 10/10**; 13 heat_pause
- **peach: 10/10** · **apple: 10/10** · **lemon: 10/10** · **lettuce-leaf: 10/10**; 15 heat_pause
- (orange-navel: 10/10 evergreen+heat region cells LIVE -- 15 fruiting cells with derived calendars + 5 unsuitable; region_notes dual-register complete.)

## Flip gates (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lemon / lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **7 anchors certified.** orange-navel = in progress (status None, launch_ready False). (Target ~18 -- a roadmap call.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN + HEAT model -- live end-to-end on orange (2026-06-12):** `perennial_evergreen` calendar_basis + crop `gating_factors`; cold climate = `min_winter_temp_f` + `cold_basis_*`; **heat climate = `heat_summer_basis` (`{high|adequate|marginal|insufficient}`, NO GDD) + `heat_basis_*`**; calendars DERIVED (`derive_evergreen_calendar`, A4-gated, no `dormant`, wrap-aware); z9 per-region by frost; survives_no_fruit honest-empty; tropical may be year_round OR dated (orange Hawaii is dated `marginal`). **THREE no-fruit directions, keyed on `gating_factors`:** chill Goldilocks (peach/apple) / cold monotone (lemon) / **heat FLOOR (orange: `insufficient` heat caps a frost-safe cell below `fruits_reliably`).** Heat branch fires only for orange/grapefruit. **Hero verdict precedent: heat `marginal` -> suitability `marginal` (reduced quality, NOT failure); reserve `insufficient`+`survives_no_fruit` for true non-sweetening (the fog-belt / Hawaii lowland), sourced -- do not borrow Hawaii's failure language for the CA coast.**
- **DERIVATION precedent (`tree_calendar._months`, fixed 2026-06-12):** the bloom/harvest field doubles as DISPLAY + derivation source; parse ONLY the primary range before the first "(" -- parenthetical prose carries stray months + the modal verb "may". A4 cannot catch a bad-source-date calendar (it parses identically), so the parse must be right at authoring; future tree kickoffs should keep month-bearing asides out of the headline range or expect the strip.
- **TREE per-variety schema:** trees use rich `varieties.recommended[]` objects (lemon's 11-key set incl. `delta`); annuals use `varieties_detail[]`. A bare `note` HALTs register_completeness.
- **Cert mechanics:** anchoring `verified` = a DATE; verbatim scan flip-blocking on >=8-word HARD lifts (re-scan after each reword; source-name==title benign); crop-SHA falls back to the collateral leaf-diff. **`register_completeness_gate` reads `crops_data_final.json` by default -- pass the candidate explicitly when gating a scratch.**
- variety-delta = CATEGORICAL; register-fill is a cert dimension; patch paths = leading-slash/dot; pre-cert anchoring = admission state; claude.ai self-checks are advisory -- the gates are the defense.
