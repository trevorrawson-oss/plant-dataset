# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**5 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, peach, lettuce-leaf) of a ~18 roadmap target. **Anchor 6 = apple IN PROGRESS:** Steps 1-3 + 3.5 released this session (the second tree, a compressed repeat on peach's rails); its 10 region cells are admission-state shells awaiting Step 4 fill. NEXT = apple Step 4 region-fill kickoff.

## Canonical pointer
- **Current SHA:** `510edafe7e122b1488058c4d952bbc4cda75d3969f29cc5817efc794edf49a99`. `LATEST.txt` session: `apple_steps1_3` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)

## What just happened (session `apple_steps1_3`)
- **apple Steps 1-3 + 3.5, COMPRESSED into one release** (the first tree-repeat; toward 2-3 anchors/day). claude.ai authored Steps 1-3 (source set + 2.9 perennial block + the 13-variety bloom-overlap calendar) from apple's OWN biology; Claude Code applied the 62-op patch (slice-integrity MATCHED `b12ade1f`), ran protocol #6, and built the Step-3.5 tree shells in the same release.
- **Apple's biology (A1, not inherited):** NOT self-fertile (`needs_pollinizer:true` -- the bloom-overlap calendar is apple's hero feature); pome rootstocks are SIZE-controlling (M9/M26/MM106/MM111/seedling); chill `[100,1000]`; hardier than peach (survives `[3,9]` / fruits `[4,8]`).
- **5 release decisions:** Q1 companion shape `good_beginner` is canonical (no re-path); Q2 minted `uf_ifas_hs764` (catalog 88->89); **Q3 RESOLVED FLAG 1** -- added `rootstock_selection_basis` (apple=`size`, peach backfilled=`soil_pest_tolerance`, additive, cert intact); Q4 nulled apple DTM to match certified peach; Q5 perennial `rotation` shape stays OWED.
- **Tooling (test-first):** `perennial_gate` A3 now skips null-suitability shell cells (apple's 3.5 shells were over-firing before fill; test #9 added); register ruled `varieties.recommended[].use` categorical. release_verify's 2 concerns (peach+apple changed, catalog +1) both adjudicated INTENTIONAL.

## Active work + next step
- **NEXT = apple Step 4 region-fill kickoff** -- per-zone `suitability` + `chill_hours_delivered` bands + the no-fruit DIRECTION SPLIT across all 10 region cells (peach's Step-4 is the exemplar). Apple's region cells are currently admission-state shells (`suitability:null`, `region_notes:null`), so whole_crop_gate apple intentionally reports 10 region-unfilled (NOT a defect -- the Step-3.5 state); apple is not in the Gate/Region tables below until it certifies.
- **OWED, fold into apple Step 4+:** perennial-aware `rotation` shape (Q5 / peach open_finding); `_build_tree_shells` to set region_id/label/zone_span + sweep stray keys (FLAG B); Appendix A registration of growth_stages `timing_*`/`year_phase` stems.
- **Separate track (plant-astro UI):** the tree GUIDE PAGE (net-new, the apple-zone-6 mock -- bloom-overlap Gantt); build after ~2 tree anchors certify.

## Gate record (generated 2026-06-11, on canonical `510edafe`)
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
