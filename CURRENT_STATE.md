# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT (anchor 4): Steps 1-3 + Step 3.5 DONE. Region shells built to the DIRECT-SOW shape (first non-tomato; `build_region_shells.py` extended). 3 certified anchors stand (cherry/beefsteak/lettuce). NEXT = carrot Step 4 (warm-region + NT window sourcing, claude.ai). Anchor TARGET ~18 (+6 family hubs; roadmap call).

## Canonical pointer
- **Current SHA:** `66b43bdac556b3836f33cc5811c23112a7a23f18f5dad9ef0f5fad0460306892`. `LATEST.txt` session: `carrot_step3_5_region_shells` (2026-06-08).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9
  - `e8b46da5` -- M16 beefsteak Steps 6/7/8: dual-voice (30 siblings + 10 lifts) + NT region_notes
  - `8fdb3ee6` -- M16 beefsteak Steps 5 + 5.5: warm cells verified, NT cold_pause (22 tokens)
  - `3a482908` -- M16 beefsteak Step 4: warm regions sourced (9 cells)

## What just happened (2026-06-08, session `carrot_step3_5_region_shells` -- Claude Code lane)
- **Carrot Step 3.5: region shells built** -- all 10 region cells to the reference shape, in the **DIRECT-SOW** window shape (`direct_sow` + harvest_start/end on the beginner track), NOT the tomato transplant shape. `northern_tier` built FROM-SCRATCH (not promoted -- carrot's `zones{}` was wiped, nothing verified to promote; it is re-sourced fresh at Step 4 like the warm regions).
- **`tools/build_region_shells.py` EXTENDED** (test-first; `tools/test_build_region_shells.py` now 4 fixtures, full tool suite 8/8 green): shape derived from the crop -- `start_method.start=="direct"` selects `direct_sow` vs `start_indoors`/`plant_out`; `_north_should_promote()` gates the legacy promote-from-zones path (retro anchors only) vs the from-scratch NT (author-fresh). Backward-compatible: cherry idempotency + the transplant fixture still pass.
- **Protocol #6:** whole_crop_gate carrot A2 = stub 0 / null-track 0 / stale 0 (region SHAPE at-bar); 10 violations remain = `region_notes` pair both null (the admission-acceptable state, filled at Steps 6/7). release_verify: collateral clean (only carrot's 10 cells changed; lettuce byte-identical; no catalog/top-level change); its 1 CONCERN is exactly the stub->region_notes-null graduation (documented Step-3.5 admission state; the pre-commit hook's `drop_shell_build_unmasks` recognizes it and passes -- committed clean, no --no-verify). Promoted `66b43bda` (base `ae2061ba`).

## Active work + next step
- **NEXT = carrot Step 4 (claude.ai authoring lane):** source verified region-appropriate windows into the 10 shells (warm regions + the from-scratch NT, all direct-sow). Per-region T1 anchors via the region->source map; succession windows authored here as `track:"succession"` entries (Step 5.5 gates beginner<->succession coherence). Region cells are currently empty `direct_sow`/`harvest_*` arrays + null `region_notes` -- ready to fill. Claude Code builds the Step 4 handoff next.
- Then Step 5 (side-by-side verification), 5.5 (calendar coherence + NT cold_pause), 6/7/8 (seasoned depth + the beginner siblings, incl. carrot's 2 deferred container beginner siblings -- N/A, those were authored at Steps 1-3), 9/10/11 (mechanical + flip).
- **PARKED (unchanged):** dataset-wide shell-shape normalization folded into the **2.9** bump (single->dual container fields on the other 119 + universal canonical-key conformance; guard: if anchor 5 precedes 2.9, run the 2-field sweep first); **v1.7 checklist amendment owed** (Step 3.5 "promote verified cold-zone data" = retro anchors only); register inventory on-disk; `fruit_set_temp_f`.

## Gate record (generated 2026-06-08, on canonical `66b43bda`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **3 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails (carry into carrot Step 4+)
- **AUTHOR-FRESH motion:** author every value from the crop's OWN sources; never verify-or-replace, never copy values across crops. Derive STRUCTURE from the crop too -- carrot is direct-sow (region windows use `direct_sow`, not transplant) + succession (lettuce is the structural reference for the direct-sow + succession shape, NOT cherry); "matches cherry/lettuce" is never a value justification (v1.6 A1).
- **Region SHAPE owner = Step 3.5 (`build_region_shells.py`, derives shape from start_method); succession tracks + windows = Step 4/5.5.** From-scratch NT for author-fresh crops (no promote-from-zones; v1.7 amendment owed).
- **Dual-register required for launch:** `_seasoned` + `_beginner`; dual-voice gate blocks the Step 11 flip on any null `_beginner` sibling (beginner siblings normally authored at Steps 7-8).
- **Canonical JSON is COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). **Catalog IDs minted by Claude Code** (precise citation = the moat). **Anchor target ~18** (roadmap call).
- **Lane split:** claude.ai authors (biology, dates, copy, STATE_HISTORY snippet); Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + handoffs. **Release:** `docs/release_runbook_v1_0.md`; protocol #6 + roster gate before every promote. A Step-3.5 release legitimately graduates stubs -> null region_notes (release_verify flags it; the pre-commit `drop_shell_build_unmasks` allows it). `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
