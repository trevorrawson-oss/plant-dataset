# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**5 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, peach, lettuce-leaf) of a ~18 roadmap target. **Anchor 6 = apple IN PROGRESS:** Step 5 (region verification) released this session -- biology verified clean + a SYSTEMIC tree-calendar fix (calendars now DERIVED from dates + a new flip-blocking A4 gate; peach corrected post-cert). apple NOT yet certified. NEXT = apple Steps 6-8 (bulk care prose).

## Canonical pointer
- **Current SHA:** `09538e31ec5d325ba48bb0189cabdb8ce4a148f821bbf8e4c00b1efbd950ed98`. `LATEST.txt` session: `apple_step5` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split

## What just happened (session `apple_step5`)
- **apple Step 5 region verification** (`5cfe354e`->`09538e31`). claude.ai verified the biology clean (hardiness bands 3/9 + 4/8, suitability 7/7/4/2, FLAG-A split 17/3, sources all resolve) and resolved both flagged decisions WITHOUT data change: **`reliable_fruit_zone_min` stays 4** (roster-honest; ultra-hardy z3 cultivars absent -> queued roster-expansion candidate), **the 100-chill floor on ca_south_coast z10 + ca_desert z10 HOLDS** (anchored to Dorsett Golden + Ein Shemer at 100 chill).
- **SYSTEMIC tree-calendar fix.** claude.ai authored a 5-cell calendar correction (bloom-token conflation); the release-side recompute-from-dates check found the SAME error class in the HARVEST tokens of 11 more apple cells AND 10 of certified **peach**'s 14 calendars. Root cause: the tree `calendar[]` is DERIVED data that was hand-authored at Step 4 and drifted from the bloom/harvest dates.
- **The fix (test-first):** new `tools/tree_calendar.py` -- `derive_tree_calendar(bloom,harvest)` generator + `tree_calendar_violations` gate, wired as `whole_crop_gate` **A4** (flip-blocking, exhaustive). apple calendars REGENERATED (16 cells, supersedes claude.ai's 5-cell patch) + peach BACKFILLED (10 cells, post-cert correction). Only `calendar` tokens changed (apple 44 / peach 30 leaf diffs, 0 biology); both trees A4=0, gate PASS; launch_ready intact.

## Active work + next step
- **NEXT = apple Steps 6-8 (bulk care prose)** -> cert (9-11). Carry into 6-8: chill-window definition (32-45 °F) into `chill_hours_note_*`; the year-1 blossom-removal `year_one_notes_*` (peach has it; make it standard tree-care prose + surface in the calendar caption per tree spec §7); the not-self-fertile reminder into `suitability_note_beginner` / `pollinator_notes_*`. Step 5.5 (calendar coherence) is now largely satisfied by the A4 generator/gate.
- **CONVENTION CHANGE (tree authoring):** future trees AUTHOR the bloom/harvest DATES; Claude Code GENERATES the `calendar[]` (never hand-author the derived field). Recorded in `tree_region_model_spec_v1_0.md`; the Step-4 kickoff convention changes accordingly.
- **Queued candidate (non-blocking):** expand apple's cold-hardy roster to species-honest z3 (add Haralson/Honeygold as full variety objects, re-derive the z3 cell, lower `reliable_fruit_zone_min` to 3). Own pass.
- **Still owed (carried):** perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`.

## Gate record (generated 2026-06-11, on canonical `09538e31`)
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
