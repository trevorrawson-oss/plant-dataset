# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**5 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, peach, lettuce-leaf) of a ~18 roadmap target. **Anchor 6 = apple:** Steps 6-8B released this session -- the register prose is now COMPLETE (null-register sweep = 0). **apple is ready for Steps 9-11 (cert).** NEXT = apple cert (verbatim scan + the A3/A4 gates + the launch_ready flip).

## Canonical pointer
- **Current SHA:** `0711aa990df1eff339d3303374dfe5f1399eb42a875283962b39785378262b4d`. `LATEST.txt` session: `apple_steps6-8b` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases

## What just happened (session `apple_steps6-8b`)
- **apple register prose COMPLETED** (`3c8ac5e9`->`0711aa99`, 48 fields): the 30 deferred register fields + the 18 tips' `text_beginner`. claude.ai independently re-derived the 48 by its own null-sweep (the 6-8A lesson applied). Slice-integrity matched `f115bbaa`. Biology N/A calls correct (hardening_off, companions tree-framing, succession). Patch was dot-path -> normalized to slash before apply.
- **Structural fix:** apple's 3 `_core` texture fields were strings (anomaly from Steps 1-3) while `_seasoned` is arrays; every certified crop uses arrays -> normalized apple's `_core` strings to arrays (claude.ai's flagged 4th shape class, rec a).
- **null-register sweep on canonical = 0** -- apple's register prose is complete (only the 3 correct-null frost cells + 4 out-of-scope companions-split remain, both expected).

## Active work + next step
- **NEXT = apple Steps 9-11 (CERT):** the verbatim scan (flip gate; fetch cited URLs, >=8-word run = HARD) + the A3 perennial cert-gate + the A4 calendar gate + the launch_ready flip -> apple becomes anchor 6 (`verified_gs_arc`). This is the first tree cert since the A4 gate + register-completeness sweep exist.
- **QUEUED -- peach 6-8C backfill** (Trevor greenlit): peach's ~29 unauthored register fields (container/soil/ph/companions/start_method); triage the watering/varieties/zones nulls.
- **SYSTEMIC FIX OWED -- register-completeness gate:** spec'd in checklist v2.0 §5; build a cert-time gate that flags null register fields vs a per-crop correct-null allowlist (would've caught apple's 30 + peach's 46). Build before apple's flip so it guards cert.
- **OWED:** the companions array-split reconciliation (out-of-scope reshape, dedicated session); perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`; repoint `gen_current_state` checklist ref v1.7+v1.8 -> v2.0.
- **Anchor 7 = lemon** (needs the citrus/chill-gating model decision -- evergreen sibling to `perennial_chill_gated` or a `suitability.gating_factor`).

## Gate record (generated 2026-06-11, on canonical `0711aa99`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **5 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
