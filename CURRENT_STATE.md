# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT Step 4 PARTIAL: northern_tier AUTHORED (from-scratch, anchor-relative). The 9 WARM regions are SOURCED but DEFERRED to a new HEAT-ANCHOR schema session (Trevor-chosen). 3 certified anchors stand (cherry/beefsteak/lettuce). Anchor TARGET ~18.

## Canonical pointer
- **Current SHA:** `12bb057215d84d608889f0291546bcd48785f30411c4790a8606089ba84ff8f7`. `LATEST.txt` session: `carrot_step4_northern_tier` (2026-06-08).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync
  - `973632ea` -- M16 beefsteak Steps 9/10/11: CERTIFIED (verified_gs_arc) -- anchor 3 of 9
  - `e8b46da5` -- M16 beefsteak Steps 6/7/8: dual-voice (30 siblings + 10 lifts) + NT region_notes
  - `8fdb3ee6` -- M16 beefsteak Steps 5 + 5.5: warm cells verified, NT cold_pause (22 tokens)

## What just happened (2026-06-08, session `carrot_step4_northern_tier` -- claude.ai authoring + Claude Code release)
- **Carrot Step 4, northern_tier authored FROM-SCRATCH** (zones 3-7). Windows are ANCHOR-RELATIVE (not smeared dates -- the opposite of the old 98.6%-bucket NT): direct_sow primary `soil_temp_40f`+0 (spring), secondary `first_frost`-80 (fall/storage); harvest_start `direct_sow_start`+60/+70; harvest_end `first_frost`+30. sources `[umn_ext, umd_ext, msu_ext, uga_c1232]`; dual-register region_notes. 9-op canonical patch, single crop, triangulated to `12bb0572` exactly.
- **STEP 4 IS PARTIAL.** The 9 WARM regions are fully SOURCED (windows locked, incl. 2 Path-A charts Trevor screenshot-confirmed) but NOT authored -- DEFERRED to a new **heat-anchor schema session** (Trevor's call): carrot is heat-bounded but does NOT bolt (forks/coarse roots in hot soil), so reusing lettuce's `bolt_threshold` token would embed a biology error (A1). That session introduces a crop-agnostic HEAT anchor (token + WeatherKit resolver tier + Claude Code wiring) -- sets the template for the whole cool-season ROOT family -- then authors the 9 warm regions (pure encoding, no re-sourcing). Sourced windows live in `~/Documents/plant-project/06-sessions/handoffs-bundles/carrot-releases/step4-nt/WARM_REGION_sourced_windows_handoff.md`.
- **USCRN flag (Claude Code correction):** claude.ai's snippet expected Claude Code to populate the spring window's `uscrn_validation` on promote -- but there is NO USCRN validator tool in the current flow (only 8 windows dataset-wide are populated, from the separate Phase 1.1 USCRN workstream; 292 are null). Left `uscrn_validation: null` -- NOT fabricated. So the promoted SHA = claude.ai's proposed `12bb0572` (no divergence). Carrot's soil-temp windows await the USCRN workstream like everyone else's.
- **Protocol #6 clean:** whole_crop_gate carrot 9 (the 9 warm region_notes-null, expected); release_verify exit 0 (only NT changed; lettuce byte-identical; NT notes-null cleared; no new violations; dash/exemplar/value-divergence ok); register PASS. Promoted `12bb0572` (base `66b43bda`).

## Active work + next step
- **NEXT = the HEAT-ANCHOR schema session** (Trevor-chosen path 1), which closes carrot Step 4:
  (a) define a crop-agnostic HEAT anchor (calendar token + WeatherKit resolver tier + Claude Code wiring) -- the cool-season-root analog of `bolt_threshold` for leafy crops;
  (b) author carrot's 9 warm regions from the already-locked sourced windows in `WARM_REGION_sourced_windows_handoff.md` (pure encoding, no re-sourcing; window COUNT per A5 -- do NOT normalize: se_gulf 2-win, fl_peninsula 1 long inverted, ca_interior 2, ca_north_coast 2, ca_south_coast 1 long, ca_desert 1, warm_arid 2 [Path A], low_desert_az 1 long [Path A], hawaii_tropical season-granularity);
  (c) add `ucanr_ext` (CA x4) / `nmsu_ext` (warm_arid) / `uariz_ext` (low_desert_az) / `uhawaii_ctahr` (hawaii) to carrot's `sources_summary` + wire anchoring -- catalog entries ALL EXIST (pool-add, NOT a mint);
  (d) author + attest the region-tip overrides (DEFERRED from Step 4; carrot's tip forks are warm-region: heat-avoidance windows, in-ground winter holding vs lift-and-store).
- After Step 4 closes: Steps 5 (side-by-side) / 5.5 (calendar tokens incl. the new heat-pause + NT cold_pause) / 6-8 / 9-11.
- **PARKED (unchanged):** USCRN validation of soil-temp windows (separate Phase 1.1 workstream; no tool in current flow); dataset-wide shell-shape normalization folded into 2.9; v1.7 checklist amendment (Step 3.5 promote = retro only); register inventory on-disk; `fruit_set_temp_f`.

## Gate record (generated 2026-06-08, on canonical `12bb0572`)
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

## Live locked decisions / guardrails (carry into the heat-anchor session)
- **HEAT ANCHOR (NEW, Trevor 2026-06-08):** cool-season ROOT crops (carrot/beet/radish/turnip/parsnip) are heat-bounded but do NOT bolt -- author a crop-agnostic HEAT anchor, never reuse lettuce's `bolt_threshold` token for them (A1: derive from the crop's own biology; shape borrowing is not value/biology borrowing).
- **AUTHOR-FRESH motion:** every value from the crop's own sources; never copy across crops; window COUNT is a source finding (A5), do not normalize to a common shape. Carrot is direct-sow + succession (lettuce is the SHAPE reference, never a value justification).
- **Do NOT fabricate USCRN (or any) validation data.** `uscrn_validation` is populated only by the Phase 1.1 USCRN workstream (8 windows so far); null is the correct pre-validation state. No validator tool exists in the current release flow.
- **Dual-register required for launch** (`_seasoned` + `_beginner`; dual-voice gate blocks the Step 11 flip on null `_beginner`). **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). **Catalog IDs minted by Claude Code**; precise citation = the moat. **Anchor target ~18** (roadmap call).
- **Lane split:** claude.ai authors; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + handoffs. **Release:** `docs/release_runbook_v1_0.md`; protocol #6 + roster gate before every promote. `zones{}` wiped on the 120 (kept on the 3 GS crops until Phase C).
