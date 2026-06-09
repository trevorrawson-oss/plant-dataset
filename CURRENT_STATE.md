# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT through Step 5.5: per-zone calendars + pause tokens (heat_pause/cold_pause) + succession shapes RESOLVED; calendar coherence PASS. Region/timing layer DONE + coherent. whole_crop_gate PASS (0, structural). NEXT = Steps 6-8 (author the still-WIPED bulk prose from scratch + dual-voice). 3 certified anchors (cherry/beefsteak/lettuce). Anchor TARGET ~18.

## Canonical pointer
- **Current SHA:** `ea16404c9d727dcbbce7fb57fe4d39f21c9a35a85d2b4edd3d554972e05419be`. `LATEST.txt` session: `carrot_step5_5_calendar_coherence` (2026-06-09).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9

## What just happened (2026-06-09, session `carrot_step5_5_calendar_coherence` -- claude.ai authoring + Claude Code release)
- **Carrot Step 5.5 DONE:** resolved 20 per-zone `resolved_by_zone` calendars + dates + pause tokens from the verified region windows. `heat_pause` (warm summers, carrot's 75°F air ceiling) + `cold_pause` (NT winters). **Succession encoded per the v1.1 spec:** `succession_continuous` (string) on the 3 continuous regions (ca_south_coast, low_desert_az, fl_peninsula); `succession_spring`/`succession_fall` + 2 new `track:"succession"` `plantings[]` entries on NT. 22-op patch; triangulated to claude.ai's `273ddd47`.
- **Claude Code release additions:** (1) **apply_patch hardened (test-first):** accepts the `ops` edit-list alias, and `add` at a list index == len now APPENDS (the 2 NT succession entries needed a real list-append -- it only index-assigned before). (2) **Swept the vestigial empty `sources_pending_admission`** off the 9 warm regions (Step-3.5 scaffold residue). So the promoted SHA `ea16404c` differs from claude.ai's patch-only `273ddd47` (= patch + the sweep).
- **G value-convergence attestation (A1):** 3 `heat_pause.months` are byte-identical to lettuce (`ca_interior` z8/z9 `[5,6,7]`, `fl_peninsula` z10 `[5,6,7,8]`) -- **independently-derived, not pasted:** carrot's air-temp heat ceiling and lettuce's bolt threshold are both ~75°F, so both cool-season crops are excluded by the SAME regional hot months; the months come from carrot's own verified windows. Legitimate climate convergence.
- **Verify:** whole_crop_gate carrot PASS (0); register PASS; release_verify exit 0 (only carrot's 10 cells; lettuce byte-identical; **calendar coherence PASS -- no waits, heat_pause aligned**; no novel non-benign keys; the residue notes cleared by the sweep). claude.ai omitted the STATE_HISTORY snippet -> authored from the patch + its `summary`. Promoted `ea16404c` (base `a9908c4a`).

## Active work + next step
- **NEXT = carrot Steps 6-8 (claude.ai authoring lane) -- the big from-scratch prose push.** Author all the wiped bulk sections (pests, diseases, growth_stages, tips_by_stage, storage, watering, yield, rotation, fertilizer, varieties, failure_diagnostics) in BOTH registers, from carrot's T1 sources. **The 6-8 handoff MUST bundle `language_and_copy_architecture_v1_0.md` + voice methodology v1.4, have claude.ai read them FIRST, and author with copy-convention flags ON from the start** (°F, no `--`/em-dash, American English, plant-lowercase, dual-register pairing + pair-vs-universal test, provenance labels, copywriting process) -- so NO Step-9 remediation (Trevor). Authoring `tips_by_stage` RE-TRIGGERS the region-tip override fork check (deferred from Step 4/5.5). Then Steps 9-11 (mechanical + the flip).
- **STANDING re-fetch follow-ups (non-blocking, from Step 5):** AZ1005 grid (low_desert_az) + CTAHR B-91/HGV-1 (hawaii) live re-fetch; C943 month table is JS-rendered (se_gulf corroborated via C1232 + B577).
- **PARKED (unchanged):** WeatherKit resolver deferred (stored_date carries it; air heat anchor needs no air->soil model); USCRN workstream (uscrn_validation null); 2.9 shell-shape normalization; v1.7 checklist amendment (Step 3.5 promote = retro only; + author-fresh Steps-6-8-author-from-scratch note); register inventory on-disk; `fruit_set_temp_f`. PK refresh owed: second_planting_structure_spec **v1.1** (succession_continuous).

## Gate record (generated 2026-06-09, on canonical `ea16404c`)
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

## Live locked decisions / guardrails (carry into carrot Steps 6-8)
- **SUCCESSION shape (spec v1.1, ratified):** two `window_type`-keyed resolved shapes -- `succession_continuous` (string) for `window_type:"continuous"`; `succession_spring`/`succession_fall` for split. One crop can hold both (carrot does). Shape + naming = Claude Code lane (we build the renderer). **HEAT ANCHOR:** `heat_threshold_temp_f` carrot = AIR 75°F (UF/IFAS AE588); germination stays `soil_temp_40f`.
- **A1 value-convergence:** where a value equals the exemplar's, attest it from the crop's OWN source + state why it converges (carrot's heat_pause months == lettuce's because the same regional hot months exclude both cool-season crops) -- NEVER "same as lettuce."
- **AUTHOR-FRESH:** every value from the crop's own sources; bulk prose authored from scratch at Steps 6-8 (gate=0 is structural; carrot NOT certified). Don't fabricate (uscrn null). **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). Catalog IDs minted by Claude Code. Anchor target ~18.
- **apply_patch.py** now accepts the `ops` edit-list alias + APPENDS on `add` at list-index==len (real list-append for new plantings entries). Dual-register required for launch (gate blocks Step-11 flip on null `_beginner`).
- **Lane split:** claude.ai authors/verifies; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + handoffs + owns data SHAPE/naming. Release: `docs/release_runbook_v1_0.md`; protocol #6 + roster gate before every promote. `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
