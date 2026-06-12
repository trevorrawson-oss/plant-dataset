# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8) so the plant-project top level shows only numbered folders + the single active handoff.
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE.

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 roadmap target. **LEMON arc** (anchor 7, the FIRST evergreen / first citrus): Steps 1-3 + **Step 3.5 (the evergreen region/calendar model BUILT) done**. Lemon is pre-cert (region cells empty). NEXT = claude.ai lemon Steps 4-5 (region biology + bloom/harvest dates).

## Canonical pointer
- **Current SHA:** `3a0947696b1bb904ed1e5a00006fe8f184b5cafffab292fb4bb443273f817e3e`. `LATEST.txt` session: `lemon_step3_5` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- 42 null register fields; register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)

## What just happened (session `lemon_step3_5`)
- **LEMON Step 3.5 -- the EVERGREEN region/calendar model BUILT** (`08556e21`->`3a094769`), Claude Code structural lane, all TEST-FIRST. Lemon's 10 annual-shape shells -> evergreen tree shells; `calendar_basis frost_anchored -> perennial_evergreen`. The first build of the two-axis evergreen model (`tree_region_model_evergreen_amendment_v1_0`). peach/apple/annual regression green; lemon still pre-cert (cells empty, Steps 4-5 fill them).
- **Four tool changes (test-first, RED watched then GREEN):**
  - `build_region_shells`: `_evergreen()` detection; sets `calendar_basis perennial_evergreen`; the region CLIMATE layer is gating-keyed -- cold-gated evergreen gets `min_winter_temp_f` + `cold_basis_*` (NOT `chill_hours_delivered`). Deciduous path byte-identical (fixture 7 evergreen / fixture 5 deciduous regression).
  - `perennial_gate`: `PERENNIAL_BASES` + `gating_factors()` (chill-gated default `["chill_hours","cold_hardiness"]` -> peach/apple unchanged); the no-fruit split keyed on gating (cold-only evergreen has no chill Goldilocks band -- `survives_no_fruit` may carry-or-empty a calendar). Universal invariants apply to both.
  - `tree_calendar`: `derive_evergreen_calendar` (no `dormant`; `growing` filler; harvest WRAPS the year; bloom overwrites harvest on overlap); A4 recognizes the evergreen basis.
  - `whole_crop_gate` A3/A4: no change -- inherit the generalized functions. Confirmed `calendar_basis='perennial_evergreen' | perennial violations: 0` on the built lemon.
- **Verification:** `apply_region_shells` SHA-gated; only lemon changed (no catalog/top-level; 6 anchors + lettuce byte-identical); full tool-test sweep GREEN; whole_crop_gate lemon = 19 (10 region_notes-null from the stub->shell graduation + 9 pre-cert anchoring -- both admission state); release_verify CLEARED the 10 `region unfilled`; pre-commit hook = NO concerns; no dashes.

## Active work + next step
- **NEXT = claude.ai lemon Steps 4-5 (region biology):** author per-region `min_winter_temp_f` bands + `cold_basis_*`, the per-zone `suitability` verdicts (survives != fruits; a hard-winter zone = `unsuitable`, no fabricated window), and bloom/harvest/plant DATES (**dates only** -- Claude Code GENERATES each cell's `calendar[]` via `derive_evergreen_calendar`; A4 enforces coherence), `frost_risk_note_seasoned`, region_notes. The evergreen cells reuse the annual render keys.
- **Then lemon 6-8** (care prose), **9-11** (cert + the Step-11 verbatim scan, deferred from Steps 1-3 since anchoring URLs are empty now). lemon's 9 anchoring gaps fill at Steps 4-5.
- **Anchor 8 = orange-navel** -- adds the `heat_accumulation` gate + `heat_summer_basis` climate datum (first exercise of the heat axis), test-first there.

## OWED
- lemon's region biology + 9 anchoring gaps (Steps 4-5); the Step-11 verbatim scan.
- Carried: apple's 4 open_findings (dead-anchor repair, rotation shape, companions array-split, reliable_fruit_zone roster); `peach_rotation_shape_finding`; perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`; `apply_patch` reject-bare-slash hardening; repoint `gen_current_state` checklist ref -> v2.0.

## Gate record (generated 2026-06-12, on canonical `3a094769`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- **lemon: 19 (10 region_notes-null [stub->shell graduation] + 9 anchoring-deferred -- expected Step-3.5 admission state; cells empty, not cert-eligible)**

## Region fill state (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: 10/10 filled** (the 6 certified anchors)
- **lemon: 10/10 EVERGREEN shells built** (calendar_basis `perennial_evergreen`; `min_winter_temp_f` climate layer; cells EMPTY -- suitability/dates/calendars authored Steps 4-5)

## Flip gates (generated)
- **6 anchors:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=False launch_ready_seasoned=False status=`None` (pre-cert; Steps 1-3 + 3.5 done)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **EVERGREEN two-axis model (BUILT 2026-06-12):** `calendar_basis: perennial_evergreen` (shape: no dormancy, `growing` filler, wrap/multi-bloom) + crop-level `gating_factors` list `{cold_hardiness, heat_accumulation, chill_hours}` (gate). Gates use `PERENNIAL_BASES`; chill-gated crops w/o gating_factors default `["chill_hours","cold_hardiness"]` (peach/apple byte-identical). Cold-gated evergreen climate layer = `min_winter_temp_f`. Spec = `tree_region_model_evergreen_amendment_v1_0`. Evergreen calendars are DERIVED via `derive_evergreen_calendar` (A4-gated), never hand-authored.
- **variety-delta descriptors (`delta.*.value`/`.parent`) = USER-FACING-CATEGORICAL** (no register sibling). The variety-delta register precedent dataset-wide.
- **register-fill is a cert dimension** (`register_fill_gate`); tree calendars DERIVED + A4-gated; **patch paths = leading-slash RFC-6901 or dot-form** (bare-slash mis-applies silently); **claude.ai's self-dash check is unreliable** -- Claude Code re-scans, §D gate is the defense.
- **pre-cert anchoring is admission state** (`drop_precert_anchoring`): a crop with status != `verified_gs_arc` may carry sources without per-field anchoring (Step 4+ fills it); a certified crop's anchoring gap still blocks.
