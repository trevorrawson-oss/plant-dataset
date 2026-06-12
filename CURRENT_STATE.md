# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, **apple**) of a ~18 roadmap target. **APPLE CERTIFIED this session** (anchor 6, the second tree) -- the first crop certified under the full hardened bar (A4 calendar gate + register-fill gate + verbatim scan). NEXT = peach 6-8C backfill, then anchor 7 = lemon.

## Canonical pointer
- **Current SHA:** `a821d6d456d7e8cff1748ba2ce1abbdd609bc846286d539b6128c9e6a898951c`. `LATEST.txt` session: `apple_cert` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE

## What just happened (session `apple_cert`)
- **APPLE CERTIFIED** (`0711aa99`->`a821d6d4`), anchor 6, the second tree. Steps 9-11: all structural cert gates PASS (A3=0, A4=0, register, **register_fill PASS -- apple is the first register-complete crop**); verbatim scan = **1 HARD hit** ("as soon as the soil can be worked", an 8-word stock phrase vs the UMN page) -> Trevor-approved reword ("...once the soil thaws enough to dig") -> re-scan **0 HARD**; 7 borderline benign. The flip set `verification_status.status=verified_gs_arc` + both `launch_ready` booleans.
- **open_findings filed (all blocks_launch:false):** rotation shape (owed, shared w/ peach); 3 dead anchor URLs (ncsu/HS764/UC-Davis -- Step-10 repair owed); companions array-split (out-of-scope reshape); reliable_fruit_zone roster-expansion candidate.
- Only apple changed (reword + flip); no catalog change. The first cert under the fully hardened bar (the A4 + register-fill gates this session built).

## Active work + next step
- **NEXT = peach 6-8C backfill** (Trevor: after apple's arc, now): peach's 42 register-fill gaps via `register_fill_gate.py peach` as the COMPUTED worklist -- 26 genuine worklist-gaps (soil/ph/companions/start_method/container/watering/varieties) + 16 of the 2.9-deferred set. Author -> release -> re-run register_fill (must return 0) to close the certified-but-incomplete state.
- **Then anchor 7 = lemon** (3rd tree) -- needs the citrus/chill-gating MODEL decision first (an evergreen sibling to `perennial_chill_gated`, or a `suitability.gating_factor`; flagged in checklist v2.0 §1). Not a pure compression repeat.
- **Dataset-wide register-fill backlog (the gate's computed to-do):** the 4 certified annuals carry ~10 null register fields each -- almost all the 2.9-deferred null-scaffolded fields (watering.method_note/critical_periods, fertilizer.amount, container self_watering/overwintering). A planned 2.9-completion sweep, lower priority than the anchors.
- **OWED:** apple's 4 open_findings (dead-anchor repair, rotation shape, companions split, roster expansion); perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`; repoint `gen_current_state` checklist ref -> v2.0.

## Gate record (generated 2026-06-11, on canonical `a821d6d4`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **6 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
