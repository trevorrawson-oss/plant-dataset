# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**5 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, peach, lettuce-leaf) of a ~18 roadmap target. **Anchor 6 = apple IN PROGRESS:** Steps 6-8A (bulk care prose) released this session -- 107 ops authored + a key-shape reconcile (apple-specific drift). apple NOT yet certified. NEXT = apple 6-8B (48-field sweep). **Also found: certified peach has a register-completeness gap (a 6-8C backfill is queued).**

## Canonical pointer
- **Current SHA:** `3c8ac5e905a92d14a43a69f61a676e2393a36ab45f95115a1dac2fa990501392`. `LATEST.txt` session: `apple_steps6-8a` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)

## What just happened (session `apple_steps6-8a`)
- **apple bulk care prose authored** (`09538e31`->`3c8ac5e9`, 107 ops; slice matched claude.ai's `5d027fd1`): the cross-pollination HERO prose (apple needs a 2nd variety -- inverse of peach), 2.9 perennial prose, pests/diseases/growth_stages/tips/notifications/weather_triggers, the Step-5 carry-ins (chill-window def, year-1 blossom-removal, ultra-hardy-z3 note).
- **Finding 1 (narrow worklist):** 30 register fields (soil/ph/companions/start_method/container_notes/succession) fell out -- the kickoff didn't list them; claude.ai authored exactly the named set. An independent null-register sweep confirmed the 30 EXACTLY. Deferred to 6-8B.
- **Finding 2 (key-shape drift, register gate caught it):** claude.ai wrote the seasoned register with BARE keys (`symptoms` not `symptoms_seasoned`) + single-register tips. **Reconciled mechanically:** 96 bare-seasoned -> `_seasoned`, 18 tips `text` -> `text_seasoned` (content identical; shape now matches peach). The 18 tips' missing `_beginner` -> 6-8B. apple slice `5d027fd1`->`d8fe3877`.
- **PEACH AUDIT (Trevor's question):** peach key-shapes CLEAN, but certified peach has **46 null register fields** -- the same container/soil/ph/companions/start_method gap (~29 real) -- because the gate tolerates null register prose. A peach 6-8C backfill is warranted.

## Active work + next step
- **NEXT = apple 6-8B (48-field sweep-derived scope):** the 30 deferred register fields + the 18 tips `text_beginner`. Biology calls: `start_method/hardening_off`=N/A (bare-root tree); `companions/note`=tree framing (pollinizer proximity + trunk competition); `succession_policy/reason`=N/A perennial.
- **QUEUED -- peach 6-8C backfill** (Trevor greenlit 2026-06-11): author peach's ~29 unauthored register fields (container/soil/ph/companions/start_method); triage the watering/varieties/zones nulls (correct-null vs real).
- **SYSTEMIC FIX OWED -- register-completeness gate:** whole_crop_gate tolerates null register prose (caught neither apple's 30 nor peach's 46). Build a cert-time gate (parallel to A4) that flags null `_seasoned`/`_beginner` fields against a per-crop correct-null allowlist, so the bots can't ship unauthored register prose + so kickoff worklists are computed not hand-listed.
- **Anchor 7 = lemon** (3rd tree) on deck after apple certifies. **Still owed (carried):** perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`.

## Gate record (generated 2026-06-11, on canonical `3c8ac5e9`)
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
