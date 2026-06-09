# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT through Step 5: region layer complete (10/10) + Steps 1-4 VERIFIED side-by-side (0 corrections, 0 template-copy flags). whole_crop_gate PASS (0, structural). NOT certified: bulk prose (pests/diseases/growth_stages/tips/storage/etc.) still WIPED -> authored Steps 6-8. NEXT = Step 5.5 (calendar tokens). 3 certified anchors (cherry/beefsteak/lettuce). Anchor TARGET ~18.

## Canonical pointer
- **Current SHA:** `a9908c4a13b32366a4e4b4d8bb46977de735e36d2cc322652b23880ee0a23c2b`. `LATEST.txt` session: `carrot_step4_warm_close` (2026-06-09).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9

## What just happened (2026-06-09, session `carrot_step5_verify` -- claude.ai verification lane)
- **Carrot Step 5 side-by-side verification COMPLETE -- 0 corrections, 0 template-copy flags.** Every Step 1-4 authored surface re-confirmed against its cited T1 (4-round bar, live-fetched). NO dataset change -> no patch, no promote; canonical stays `a9908c4a`. Verification log archived (`06-sessions/.../step5-verify/`); it is the side-by-side record this arc.
- **Heat ceiling VERIFIED-TRUE (the linchpin, 9 cells anchor to it):** AE588 states verbatim "optimum growth and root color when the air temperatures are 61F-75F" -- confirms `heat_threshold_temp_f`=75/air/ufifas_ae588 (the contentious item from last session resolved TRUE on direct read).
- CA 4 cells VERIFIED EXACT vs UC ANR Table 13.2; warm_arid DTH 72 vs NMSU CR457-B; se_gulf/fl_peninsula/NT vs their sources; low_desert_az + hawaii verified on existing Path-A / season basis. Scalars/structured/companions all true; sub-checks (stage-temp conflation, cultivar-type, R1) all PASS.
- **Claude Code release:** verification-only -- nothing applied, no gate run needed (no bytes changed); confirmed canonical unchanged at `a9908c4a` == LATEST; recorded the STATE_HISTORY entry + archived the log. (Predecessor chain + gate/region/flip below are unchanged from the Step-4 close.)

## Active work + next step
- **NEXT = carrot Step 5.5** (calendar coherence + tokens): author the `heat_pause` months on the warm cells + NT `cold_pause`; populate per-zone `resolved_by_zone` calendars/dates from the verified region windows; check `calendar[]`<->`plantings[]` coherence + beginner<->succession envelope. Sweep the vestigial empty `sources_pending_admission` key on the 9 warm cells while there.
- Then **Steps 6-8** (author-fresh): author the bulk prose from scratch (pests, diseases, growth_stages, tips_by_stage, storage, watering, yield, rotation, fertilizer, varieties, failure_diagnostics) in both registers -- **the 6-8 handoff MUST bundle `language_and_copy_architecture_v1_0.md` + voice methodology v1.4, have claude.ai read them FIRST, and author with copy-convention flags ON from the start (°F, no `--`/em-dash, American English, plant-lowercase, dual-register pairing, provenance labels) so there is NO Step-9 remediation** (Trevor). Authoring `tips_by_stage` RE-TRIGGERS the region-tip fork check. Then 9-11.
- **STANDING re-fetch follow-ups (from Step 5, non-blocking):** live re-fetch AZ1005 grid (low_desert_az) + CTAHR B-91/HGV-1 (hawaii) -- both verify on existing Path-A/season basis; C943 month table is JS-rendered (se_gulf corroborated via C1232 + B577).
- **PARKED (unchanged):** WeatherKit resolver deferred (stored_date carries it); USCRN workstream (uscrn_validation null); 2.9 shell-shape normalization (+ sweep `sources_pending_admission`); v1.7 checklist amendment (Step 3.5 promote = retro only) + author-fresh Steps-6-8-author-from-scratch note; register inventory on-disk; `fruit_set_temp_f`.

## Gate record (generated 2026-06-09, on canonical `a9908c4a`)
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

## Live locked decisions / guardrails (carry into carrot Step 5.5+)
- **Verification-only sessions** (Step 5: 0 corrections) = NO promote / NO SHA re-pin; Claude Code just records the STATE_HISTORY entry + archives the verification log. The 4-round side-by-side log IS the per-arc verification record (don't re-do it; trust the verifier, no bytes to gate).
- **HEAT ANCHOR (live + verified):** `heat_threshold_start/end` (crop-agnostic backend token) + `heat_threshold_temp_f` (carrot = AIR 75°F, UF/IFAS AE588, verified verbatim). Germination stays `soil_temp_40f` (soil). Simple-vs-precise framing = dual-register region_notes copy.
- **AUTHOR-FRESH motion:** every value from the crop's own sources; never copy across crops; A5 window counts not normalized. Bulk prose authored Steps 6-8 (from scratch for author-fresh; gate=0 here is STRUCTURAL, carrot far from certified).
- **Do NOT fabricate** validation/sources; surface gaps (the cross-check caught real drift). Catalog IDs minted by Claude Code; precise citation = the moat. **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). **Anchor target ~18** (roadmap call). Dual-register required for launch (gate blocks Step-11 flip on null `_beginner`).
- **Lane split:** claude.ai authors/verifies; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, source_set curation, the flip) + handoffs. **Release:** `docs/release_runbook_v1_0.md`; protocol #6 + roster gate before every promote. `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
