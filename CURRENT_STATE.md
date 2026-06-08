# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY CERTIFIED. 🍅 BEEFSTEAK (anchor 2/9): Steps 3.5+4+5+5.5+6/7/8 DONE, gate=3, NEXT = Steps 9/10 then 11
**2 of 9 anchors certified** (`cherry-tomato` + `lettuce-leaf`, `status="verified_gs_arc"`, `GATE: PASS`). **M16 `beefsteak-tomato` (anchor 2 of 9) nearly there:** region shells -> warm sourcing -> side-by-side verification -> NT cold_pause -> **dual-voice (30 beginner siblings + 10 seasoned depth-lifts) + NT region_notes** all DONE. **Dual-voice coverage gate = 0; §A2 = 0 (all 10 region cells carry both region_notes registers).** beefsteak `GATE: 3` -- only the Step 9 dash + Step 10 T2 + anchoring gap remain before the Step 11 flip. **NEXT = Steps 9 + 10 (small, mostly mechanical) then Step 11 (launch_ready reset-then-flip + status).** **(Operating model: claude.ai authors, Claude Code releases.)**

## Canonical pointer
- **Current SHA:** `e8b46da50e043428d14be82136fba5e765040215564c29ff414004937746ea81` (beefsteak Steps 6/7/8: 30 dual-voice `_beginner` siblings + 10 `_seasoned` depth-lifts + NT `region_notes` both registers; ONLY `beefsteak-tomato` changed -- cherry + lettuce + catalog + `verification_status` byte-identical). `LATEST.txt` session: `m16_beefsteak_steps678_dual_voice_nt_region_notes`.
- **NEXT: beefsteak Step 9 (dash) + Step 10 (T2 + anchoring) -- preflight against `e8b46da5`.**
- **Predecessor chain:** `e8b46da5` (Steps 6/7/8) <- `8fdb3ee6` (Step 5.5 NT cold_pause) <- `3a482908` (Step 4 warm) <- `006cd0af` (Step 3.5 shells) <- `87c8e0a1` <- `b6777ef6` (cherry CERTIFIED) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-08, session `m16_beefsteak_steps678_dual_voice_nt_region_notes`)
- **Steps 6/7/8 -- dual-voice (claude.ai authored, Claude Code released).** **30 `_beginner` siblings** authored (companions `why` x5, pests/diseases `cause` x8, `growth_stages.log_prompt` x6, watering x3, container x2, storage x3, yield x2, rotation x1) from depth-lifted seasoned text per dual-register v1.1; **10 `_seasoned` depth-lifts** (8 `cause_seasoned` + `rotation.avoid_after` + `container drainage.saucer_practice`; the rest ruled already-at-depth). **Dual-voice coverage gate -> 0 missing / 0 null.** No new source mints (added facts traced to each field's existing T1).
- **(B) northern_tier `region_notes` -- BOTH registers authored.** The last region_notes-null cell, now filled (10/10 region cells carry both registers).
- **A PUNCH-LIST ERROR OF MINE, CAUGHT + CORRECTED BY claude.ai.** My Step-6/7/8 punch list + kickoff told claude.ai to author "the z6-7 two-crops-possible second planting" in the NT notes -- that is CHERRY's NT shape; **beefsteak's NT is single-crop** (its 75-90 DTM leaves no room for a cold-zone second crop). claude.ai correctly refused the instruction (v1.6 A1: derive from own biology, "matches cherry" is not a justification), authored the notes to the TRUE single-crop structure, and flagged it. Released data is correct. Lesson: punch lists must derive NT shape from the crop's own structure, not cherry's.
- **Patch format: structure canonical + `ensure_ascii=False` SHA (both prior flags honored)**, BUT the json_paths were crop-RELATIVE (`$.pests[0]...`, no crop selector). Reconciled by prefixing `crops[?(@.slug=='beefsteak-tomato')]` to all 42 paths, then applied via `apply_patch.py` -- triangulated to claude.ai's `e8b46da5` exactly. New flag (below).

## Verification (protocol #6, this release)
- **(a) gate:** beefsteak **34 -> 3** (dual-voice null_values **0**; §A2 NT region_notes-null cleared; temp-form 0); cherry + lettuce `GATE: PASS`. The residual 3 = 1 `sources_summary[19].name` dash (Step 9) + 1 `harvest_to_table` T2 (Step 10) + 1 `harvest_urgency` anchoring gap (Step 10). **(b) release_verify:** collateral clean (only `beefsteak-tomato`; cherry + lettuce + catalog + `verification_status` byte-identical); §B **no new violations** (the 10 depth-lifts introduced zero new dash/temp); §F NT now has both registers; §E ok; §D 6 dashes = SAME pre-existing legacy `zones{}` strings. **(c) claim cross-check:** 42 ops (30 siblings + 2 NT registers + 10 lifts) on the manifest paths; dual-voice 0/0; NT notes verified single-crop (not the erroneous z6-7 second crop); `verification_status` byte-identical (stale flags intact).

## Active work + parked decisions
- **NEXT MILESTONE: beefsteak Steps 9 + 10 (small, mostly MECHANICAL -- candidate for the Claude Code lane), then Step 11.**
  - **Step 9:** 1 `sources_summary[19].name` user-facing `--` -> per-sense (cherry resolved its identical one to a comma).
  - **Step 10:** `harvest_to_table` cites a T2 (de-cite or replace with T1, no grandfathering) + `harvest_urgency` `sources:[umn_ext,ncsu_ext]` has no `anchoring_urls` dict (add the URLs).
  - **Step 11:** validation re-run (all gates 0 except any intentional) + `launch_ready` reset-then-flip + `status` -> `verified_gs_arc`. **Beefsteak's stale `launch_ready_core/seasoned=true` + `status="verified_complete"` (M11 artifacts) stay UNTOUCHED until then -- reset-then-re-earn at Step 11** (exactly as cherry's stale M10 flags were).
- **PARKED -- Trevor decisions:** (1) **`fruit_set_temp_f` schema shape** (warm_arid Aug structural set; re-surfaced at Steps 4 + 5). (2) optional `ca_south_coast` z9 soft-`cold_pause` revert. (3) lettuce `why_beginner` copy (3 fields) Claude-Code-drafted -- sanity-check.
- **PARKED -- Claude Code lane / claude.ai flags (non-blocking):**
  1. **Patch path format (NEW this session):** claude.ai's json_paths were crop-RELATIVE (`$.pests[0]...`); the spec requires FULL paths from root with the crop selector (`$.crops[?(@.slug=='...')].pests[0]...`). Reconciled by hand. Flag in the Step 9/10 handoff. (RESOLVED this session: the `ensure_ascii` SHA flag -- claude.ai computed `e8b46da5` correctly.)
  2. **Gate/release_verify `basis_seasoned` classification:** `whole_crop_gate` §D temp-scans `basis_seasoned` but exempts `synthesis_note_seasoned`; align them; settle user-facing-vs-backend for `*_basis`.
  3. `release_verify` §D over-flags pre-existing legacy `zones{}` anchoring-note dashes.

## Gate record (2026-06-08, on canonical `e8b46da5`)
- **cherry `GATE: PASS` (0); lettuce `GATE: PASS` (0).** Both `verified_gs_arc`, launch_ready true.
- **beefsteak `GATE: 3`** -- §A2 0, dual-voice 0; the 3 = 1 `sources_summary` dash (Step 9) + 1 `harvest_to_table` T2 (Step 10) + 1 `harvest_urgency` anchoring gap (Step 10). One short step from flip-eligible.

## Region fill state
**cherry-tomato -- 10/10 verified, CERTIFIED (reference exemplar).**
**beefsteak-tomato -- 10/10 region cells SOURCED + VERIFIED + dual-register region_notes; whole-crop dual-voice = 0.** Heat biology T1-verified (wider-than-cherry pauses: se_gulf/ca_desert/low_desert Jun-Aug, fl_peninsula Jun-Sep, warm_arid Jul-legibility; cool CA coast + Hawaii no pause; hawaii year_round). NT = single frost-bracketed crop (NOT a z6-7 second-crop crop -- that is cherry), winter `cold_pause` derived, region_notes both registers. Remaining: the 3 Steps-9/10 items + the Step 11 flip.

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce, ✅ cherry. **Beefsteak: 3.5+4+5+5.5+6/7/8 done; Steps 9/10/11 remain (gate 3, near flip-eligible).** Then 6 more anchors.
2. **Region read-layer flip** -- shape + fill + verification proven on lettuce + cherry; beefsteak 10/10 filled + verified (owes only Steps 9-11). Ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward region-first. 3 provers (cherry done; beefsteak prover 2, nearly complete).
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into beefsteak Steps 9/10/11)
- **Reference gold-standard crop = `cherry-tomato`** (shape + convention reference) -- BUT derive each crop's biology + STRUCTURE from its OWN sources; "matches cherry" is not a justification (v1.6 A1; the NT single-crop catch this session is the live example).
- **Step 11 entry guard:** assert `launch_ready_core == false AND launch_ready_seasoned == false` at entry. Beefsteak's are STALE true -> **reset to false first, confirm gates, then re-flip earned** (the cherry M10 pattern). `status` -> `verified_gs_arc` at the flip.
- **`harvest_to_table` T2-as-evidence: T1-only, NO grandfathering** (Step 10). **TEMPERATURE user-facing = `°F`** (backend prose may spell it). Dashes per-sense (Step 9).
- **HANDOFF PATCHES: `base_sha` + `patches[]`, FULL `$.crops[?(@.slug=='...')]...` paths, `from`=current value, proposed end-SHA `ensure_ascii=False`.** (claude.ai has hit each of these once; all now flagged.)
- **DUAL-VOICE COMPLETE for beefsteak** (gate 0) -- do not re-author. Backend prose (`synthesis_note`, `*_basis`, `source_quote`) is seasoned-only.
- **Lane split:** STRUCTURAL/MECHANICAL/notation = Claude Code; biology + consumer copy + voice/IP + dates = claude.ai. (Steps 9/10 are mostly mechanical -- candidate for the Claude Code lane directly.)
- **Keep `zones{}` coherent until Phase C.** **Release sequence:** `docs/release_runbook_v1_0.md`; protocol #6 before every promote.
