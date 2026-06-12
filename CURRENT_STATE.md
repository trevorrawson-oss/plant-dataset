# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE.

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 target. **LEMON arc** (anchor 7, first evergreen): Steps 1-3 + 3.5 + **Steps 4-5 (region biology) done** -- the 10 evergreen regions are LIVE (12 cells crop, 8 honest no-crop). Pre-cert. NEXT = claude.ai lemon Steps 6-8 (care prose).

## Canonical pointer
- **Current SHA:** `6c9b9a5434e6701a9669d16ac295c2e4b6b38c189cbf9b20865427d5bdf868d4`. `LATEST.txt` session: `lemon_steps4_5` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill

## What just happened (session `lemon_steps4_5`)
- **LEMON Steps 4-5 -- the EVERGREEN region biology** (`3a094769`->`6c9b9a54`). claude.ai authored 316 ops (clean apply, crop SHA matched the claimed `5da0e6f1` pre-transform): per-region `min_winter_temp_f` band + `cold_basis_*`, the 20 per-zone `suitability` verdicts + notes, bloom/harvest/plant DATES, `frost_risk_note_seasoned`, `region_notes_*`, + the 4 deferred Steps-1-3 anchoring (companions + 3 rootstocks). whole_crop_gate lemon **19 -> 2**.
- **Two Claude Code transforms:** (a) populated `region_id`/`region_label`/`zone_span` from the canonical certified set (closes the OWED `_build_tree_shells` item for lemon); (b) GENERATED 12 cell calendars via `derive_evergreen_calendar` (10 fruits_reliably + 2 marginal carry calendars; 3 survives_no_fruit + 5 unsuitable stay empty -- honest no-crop).
- **YEAR-ROUND TROPICAL PRECEDENT (Trevor ruled):** `hawaii_tropical.11` fruits year-round (no seasonal window). Applied the LOCKED year_round-pauseless pattern: `year_round:true` + a declared 12-month `harvest` fill; **A4 gate taught to SKIP date-coherence on `year_round` cells** (test-first, E7). The rail for every tropical citrus cell.
- The three blessed calls landed as authored: the z9 region-split (coast/desert "9" fruits / interior/Gulf "9" marginal), survives_no_fruit cells EMPTY (no fabricated window), region meta left to Claude Code. Verified the 20-cell verdict map (10/2/3/5).
- **Protocol #6:** A3 (suitability/no-fruit) = 0; A4 (calendar coherence) = 0; region_notes all filled; dashes 0; sources catalogued. The 2 residual gate violations = pre-cert anchoring gaps (`varieties/sources`, `hawaii.11 ucanr_ext`), forgiven by `drop_precert_anchoring`. register PASS; pre-commit clean (cleared 17); only lemon + region cells changed, no catalog, lettuce + 6 anchors byte-identical.

## Active work + next step
- **NEXT = claude.ai lemon Steps 6-8 (care prose):** the bulk register/care prose (pests, diseases, the citrus growth journey, tips, watering/fertilizer flat prose, storage, failure_diagnostics, notifications/weather_triggers) -- both registers, authored fresh from lemon's biology. register_fill_gate is the worklist driver.
- **Then lemon 9-11 (cert):** the Step-11 verbatim scan (deferred from Steps 1-3/4-5; anchoring URLs now exist), the gates (A3/A4 evergreen-aware), close the 2 anchoring gaps + decide variety-attribution, the flip.
- **Anchor 8 = orange-navel** -- the heat-accumulation gate (`heat_summer_basis` + the cool-summer no-fruit branch), built test-first at orange's Step 3.5.

## OWED
- lemon cert items: the 2 anchoring gaps (`varieties/sources` + `hawaii.11 ucanr_ext`); whether `varieties.recommended[]` claims need a sources surface (claude.ai flagged); the Step-11 verbatim scan.
- Carried: apple's 4 open_findings; `peach_rotation_shape_finding`; perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region meta (now done for lemon inline -- fold into the builder for future trees); Appendix A growth_stages `timing_*`/`year_phase`; `apply_patch` reject-bare-slash hardening; repoint `gen_current_state` checklist ref -> v2.0.

## Gate record (generated 2026-06-12, on canonical `6c9b9a54`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- **lemon: 2 (pre-cert anchoring gaps only -- `varieties/sources` + `hawaii.11 ucanr_ext`; A3=0, A4=0, dashes=0; not cert-eligible until 6-8 + anchoring close)**

## Region fill state (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: 10/10 filled** (the 6 certified anchors)
- **lemon: 10/10 EVERGREEN regions FILLED** -- 12 fruiting cells (calendars derived) + 8 honest no-crop (3 survives_no_fruit, 5 unsuitable, empty); `hawaii_tropical.11` = `year_round:true`. Care prose (6-8) + cert (9-11) remain.

## Flip gates (generated)
- **6 anchors:** launch_ready true/true status=`verified_gs_arc`
- **lemon:** launch_ready False/False status=`None` (pre-cert; Steps 1-3 + 3.5 + 4-5 done)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **EVERGREEN model (BUILT + region-proven 2026-06-12):** `calendar_basis: perennial_evergreen` + crop-level `gating_factors`; cold-gated climate = `min_winter_temp_f`; calendars DERIVED via `derive_evergreen_calendar` (A4-gated, no `dormant`, wrap-aware). z9 resolved per-region by frost behavior (NOT zone number). survives_no_fruit = honest empty (no fabricated window). **Tropical year-round cell = `year_round:true` + declared `harvest` fill; A4 skips date-coherence on year_round cells.** Evergreen = 2 anchors (lemon 7 cold-only, orange-navel 8 heat).
- **variety-delta descriptors = USER-FACING-CATEGORICAL**; **register-fill is a cert dimension**; tree calendars DERIVED + A4-gated; **patch paths = leading-slash or dot-form** (bare-slash mis-applies); **claude.ai's self-dash check is unreliable** -- Claude Code re-scans, §D gate is the defense.
- **pre-cert anchoring is admission state** (`drop_precert_anchoring`): pre-cert crop may carry sources without per-field anchoring (cert closes it); a certified crop's gap still blocks.
