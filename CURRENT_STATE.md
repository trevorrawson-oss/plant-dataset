# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT STEP 4 CLOSED -- all 10 region cells filled (NT + 9 warm); heat anchor live (AIR). whole_crop_gate carrot = PASS (0) STRUCTURALLY. NOT certified: pests/diseases/growth_stages/tips/storage/watering etc. are still WIPED (empty) -> authored at Steps 6-8; Steps 5 / 5.5 remain. 3 anchors still the only certified (cherry/beefsteak/lettuce). Anchor TARGET ~18.

## Canonical pointer
- **Current SHA:** `a9908c4a13b32366a4e4b4d8bb46977de735e36d2cc322652b23880ee0a23c2b`. `LATEST.txt` session: `carrot_step4_warm_close` (2026-06-09).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9
  - `e8b46da5` -- M16 beefsteak Steps 6/7/8: dual-voice (30 siblings + 10 lifts) + NT region_notes

## What just happened (2026-06-09, session `carrot_step4_warm_close` -- claude.ai authoring + Claude Code release)
- **Carrot Step 4 CLOSED: 9 warm region cells authored** from the locked sourced windows, using the ratified **heat anchor** (`heat_threshold_start`/`_end`) + `last_frost`/`direct_sow_start`, all with `stored_date` fallback. Window counts are A5 source findings (NOT normalized): se_gulf 2 / fl_peninsula 1-long-inverted+succession / ca_interior 2 / ca_north_coast 2 / ca_south_coast 1-long+succession / ca_desert 1 / warm_arid 2 (Path A) / low_desert_az 1-long+succession (Path A) / hawaii_tropical season-granularity. Dual-register region_notes per cell.
- **Heat anchor value RESOLVED (Trevor, option a -- AIR):** `heat_threshold_temp_f = {temp_f:75, measures:"air", sources:[ufifas_ae588]}`. The proposal's "soil ~75-80°F" was unsourced; T1 (UF/IFAS AE588) frames it as AIR 61-75°F. Air is also what WeatherKit resolves directly (the air->soil model is moot for this anchor; germination keeps `soil_temp_40f`). `heat_anchor_proposal_v0.md` corrected soil->air.
- **Claude Code release fixes (protocol #6 cross-check caught 5 uncatalogued source IDs):** minted 4 catalog docs (`ufifas_ae588`, `nmsu_chart`, `uhawaii_ctahr_b91`, `uhawaii_ctahr_hgv1`); `uga_c943` was a DUPLICATE of `uga_calendar` (Circular 943) -> re-pointed (not minted). Added the 8 cited region IDs to `verification_status.source_set`.
- **Two decisions claude.ai surfaced (handled, not unilateral):** (1) the air-vs-soil value above; (2) region-tip override attestation = nothing to attest (carrot's `tips_by_stage` is empty; succession tip is already climate-aware/portable) -- RE-RUN the fork check when `tips_by_stage` is authored at Steps 6-8.
- **Verify:** whole_crop_gate carrot PASS (0); register PASS; release_verify exit 0 (only carrot's 9 warm cells + the 4 catalog mints; lettuce byte-identical; 9 region_notes-null cleared; calendar/dash/exemplar/value-divergence ok; benign empty `sources_pending_admission` scaffold residue on the 9 cells -- minor cleanup, noted). Promoted `a9908c4a` (base `12bb0572`; differs from claude.ai's patch-only `02fa1f40` by the mints + re-point + source_set + heat_threshold_temp_f).

## Active work + next step
- **NEXT = carrot Step 5** (side-by-side verification of every region window + the heat ceiling against its T1) then **Step 5.5** (calendar tokens: heat_pause months in the warm cells + NT cold_pause + per-zone `resolved_by_zone` date/calendar population + coherence).
- **IMPORTANT (author-fresh reality):** carrot's BULK crop content is still WIPED/empty -- pests, diseases, growth_stages, tips_by_stage, storage, watering, yield, rotation, fertilizer, varieties, failure_diagnostics. The retro arc assumed these pre-existed; for author-fresh crops they must be AUTHORED at **Steps 6-8** (re-interpreted: author, not just depth-lift/sibling). whole_crop_gate=0 is STRUCTURAL only (the surfaces that exist are clean) -- carrot is far from certified. (Methodology note for the checklist: Steps 6-8 own from-scratch authoring of the prose sections for author-fresh crops; the region-tip fork check re-runs once `tips_by_stage` exists.)
- **Minor cleanup:** the 9 warm cells carry a vestigial empty `sources_pending_admission` key (Step-3.5 scaffold residue; release_verify rules it benign) -- sweep at Step 5.5 or the 2.9 shape pass.
- **PARKED (unchanged):** WeatherKit resolver DEFERRED until plant-astro has a dynamic surface (stored_date carries everything; air heat anchor needs no air->soil model); USCRN workstream (uscrn_validation null, not fabricated); 2.9 shell-shape normalization; v1.7 checklist amendment; register inventory on-disk; `fruit_set_temp_f`.

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

## Live locked decisions / guardrails (carry into carrot Step 5+)
- **HEAT ANCHOR (live):** `heat_threshold_start/end` (crop-agnostic, BACKEND token) + per-crop `heat_threshold_temp_f` (carrot = AIR 75°F, UF/IFAS AE588). The simple-vs-precise framing is dual-register region_notes COPY, not two tokens. Coexists with `bolt_threshold` (bolting crops). Germination stays `soil_temp_40f` (T1-stated in soil).
- **AUTHOR-FRESH motion:** every value from the crop's own sources; never copy across crops; window counts are A5 source findings (do NOT normalize). Bulk prose sections (pests/diseases/etc.) are authored at Steps 6-8 for author-fresh crops.
- **Do NOT fabricate** USCRN or any validation/source not actually found; surface gaps (claude.ai over-claimed 5 catalog IDs -- the cross-check caught it). Catalog IDs minted by Claude Code; precise citation = the moat.
- **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). **Anchor target ~18** (roadmap call). Dual-register required for launch (gate blocks Step 11 flip on null `_beginner`).
- **Lane split:** claude.ai authors; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints/re-points, source_set/pool curation, the flip) + handoffs. **Release:** `docs/release_runbook_v1_0.md`; protocol #6 + roster gate before every promote. `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
