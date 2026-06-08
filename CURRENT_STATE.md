# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT (anchor 4) Steps 1-3 AUTHORED FRESH + released. 3 certified anchors stand (cherry/beefsteak/lettuce); carrot's non-region core (sources, soil/pH/container/succession/start_method, scalars, companions) is dual-register complete from its OWN sources. NEXT = carrot Step 3.5 (region shells) -> Step 4. Anchor TARGET ~18 (+6 family hubs; roadmap call).

## Canonical pointer
- **Current SHA:** `ae2061ba75f4b38aab8312774b67d403aa5b75610c14de74b962d3bccfb9ff58`. `LATEST.txt` session: `carrot_steps1-3_author_fresh` (2026-06-08).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9
  - `e8b46da5` -- M16 beefsteak Steps 6/7/8: dual-voice (30 siblings + 10 lifts) + NT region_notes
  - `8fdb3ee6` -- M16 beefsteak Steps 5 + 5.5: warm cells verified, NT cold_pause (22 tokens)
  - `3a482908` -- M16 beefsteak Step 4: warm regions sourced (9 cells)
  - `006cd0af` -- M16 beefsteak Step 3.5: region shells built (anchor 2/9)

## What just happened (2026-06-08, session `carrot_steps1-3_author_fresh`)
- **FIRST author-fresh release.** claude.ai authored carrot Steps 1-3 from carrot's OWN T1 sources into the empty shell (never verify-or-replace). 83-op canonical patch, single crop; self-apply triangulated to claude.ai's proposed SHA exactly. Carrot-specific reasoning held (organic matter `moderate` not tomato's `high`; germination 55-75 OPTIMUM not a warm-crop upper bound; `start_method.start=direct`; succession suitable/3wk/3; sunlight 6-10).
- **Step 1:** `botanical_name`=Daucus carota, `family`=Apiaceae, `verification_status.source_set` = 10 CANDIDATE IDs (verification is Step 5). **Step 2:** soil/ph/container_notes/succession_policy/start_method + scalars, each >=2 T1 + anchoring. **Step 3:** companions (3 good / 3 bad) at v1.4 rigor, honest research_backed/likely/traditional labels.
- **Claude Code release additions (this lane):** (1) minted catalog ID **`uga_c1232`** (UGA Circular 1232 Homegrown Carrots) and re-pointed carrot's pH/DTM/germ anchors off the provisional `uga_calendar` (Circular 943 is a planting calendar, does not state pH/germ -- the precise citation matters). (2) **Resolved a roster-gate HALT:** carrot's `container_notes.shape_requirements` + `drainage.saucer_practice` were authored as single-register prose because the wiped shell carried a non-canonical single-key shape; normalized both to canonical dual-register (`_seasoned` = authored; `_beginner` = Trevor-approved copy via the copywriting skill). carrot is now dual-complete (null_values 0).
- **Verify (protocol #6):** whole_crop_gate carrot 10 (all region-fill, expected -- Steps 3.5/4); register_completeness PASS; release_verify clean (only carrot + the `uga_c1232` admit; lettuce byte-identical; no new violations; calendars coherent; no user-facing dashes). Promoted end-SHA `ae2061ba` (differs from claude.ai's patch-only `04b5543b` by the uga_c1232 mint + the container dual-register normalization).

## Active work + next step
- **NEXT = carrot Step 3.5 (region shell build, Claude Code lane)** then Step 4. Carrot is direct-sow + succession, so Step 3.5 needs `tools/build_region_shells.py` EXTENDED for the direct-sow window shape (`direct_sow`, not `start_indoors`/`plant_out`) + succession tracks + a from-scratch NT (carrot's `zones{}` was wiped -- NT is re-sourced fresh like the warm regions, NOT promoted). Reference = lettuce (direct-sow), not cherry. Test-first (`tools/test_build_region_shells.py`). `start_method` + `succession_policy` (authored this session) are the load-bearing inputs.
- **PARKED:**
  - **Dataset-wide shell-shape normalization, folded into the schema 2.9 bump** (fresh session after carrot): conform all 120 shells to the GS crops' canonical universal KEY-shape (single->dual where it drifted, e.g. `shape_requirements`/`saucer_practice` on the other 119; add any missing universal keys) -- EMPTY shape only, never values, scoped to universal surfaces (not tomato-specific keys). 2.9 is additive/no-retrofit, same flavor of work -> one structural pass. **Guard:** if anchor 5 starts before 2.9, run the tiny single->dual sweep first so it does not re-trip the roster gate.
  - **v1.7 checklist amendment owed:** Step 3.5 "promote the VERIFIED cold-zone data" assumes a per-crop-verified `zones{}` (retro anchors only); from-scratch crops re-source NT like warm regions.
  - Pre-existing: register inventory on-disk; `fruit_set_temp_f`; minor copy calls.

## Gate record (generated 2026-06-08, on canonical `ae2061ba`)
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

## Live locked decisions / guardrails (carry into carrot Step 3.5+)
- **AUTHOR-FRESH is the motion.** Author every value from the crop's OWN sources into the empty shell; never verify-or-replace, never copy values across crops. The 3 GS crops are the verified ground truth; reference SHAPE = `cherry-tomato`, but derive biology + structure from the crop's own sources ("matches cherry" is never a value justification, v1.6 A1).
- **Dual-register is required for launch:** every user-facing prose field has `_seasoned` + `_beginner`; the dual-voice gate (whole_crop_gate B) blocks the Step 11 flip on any null `_beginner` sibling. Beginner siblings are normally authored at Steps 7-8; a null `_beginner` mid-arc is fine (gate-tracked), never skipped.
- **Canonical JSON is COMPACT** (`json.dumps(separators=(",",":"), ensure_ascii=False)`, single line, no trailing newline -- match `apply_patch.py`; never `indent=2`). **Catalog IDs are minted by Claude Code** (claude.ai flags; Claude Code mints + re-points) -- precise citation is the moat.
- **Anchor target ~18** (roadmap call; do not hardcode a denominator here). **Lane split:** claude.ai authors (biology, dates, copy, STATE_HISTORY snippet); Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + builds handoffs.
- **Release sequence:** `docs/release_runbook_v1_0.md`; protocol #6 + the roster gate before every promote. `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
