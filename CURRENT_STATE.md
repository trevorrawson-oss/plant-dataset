# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🥕 CARROT CERTIFIED -- anchor 4 of ~18 (`verified_gs_arc`; launch_ready core + seasoned). The FIRST crop taken from wiped shell -> certified entirely AUTHOR-FRESH, full arc (Steps 1-11): region/timing layer + all bulk prose authored from scratch, both registers. 4 anchors certified (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf). NEXT = anchor 5 (roadmap call: microgreen for the non_seasonal_indoor archetype, or a family hub). Carrot is now the author-fresh reference exemplar for the bots.

## Canonical pointer
- **Current SHA:** `b34bd6fcb2112753b91989d32620c000c2df2143b008b3b165d95b4071c237a2`. `LATEST.txt` session: `carrot_steps6_8` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells
  - `ab389f72` -- register: source_quote SP -> EXCLUDED; un-rename dataset-wide + gate sync

## What just happened (2026-06-10, session `carrot_steps6_8` -- claude.ai authoring + Claude Code release)
- **Carrot Steps 6-8 DONE + FLIPPED.** claude.ai authored every wiped bulk section from carrot's own sources, both registers: the 7 compounds (pests 2, diseases 4, growth_stages 4, tips_by_stage 11 tips / 5 stages, failure_diagnostics 6, notifications 5, weather_triggers 5), the 8 dict shells (storage/watering/yield/rotation/fertilizer/varieties/thinning/moon_phase), top-level prose (description/harvest_ready/soil_prep). 26-op patch, base `ea16404c`; dual-voice coverage 0 missing / 0 null.
- **Claude Code release (all 10 snippet flags resolved):** re-pointed 5 `ipm.ucanr.edu` citations `ucanr_ext` -> **`uc_ipm`** (the precise catalog ID claude.ai could not see in its 19-source subset; added `uc_ipm` to source_set, `ucanr_ext` stays for region content); `fertilizer.type` snake_case -> human-readable; tips metadata set; nematode typed `pest`; growth_stages / moon_phase / varieties shapes confirmed vs anchors; dict-shell sources-plumbing + `harvest_urgency`/`fertilizer.frequency` vocab deferred to 2.9; region-tip override deferred (logged as carrot `open_finding` `carrot_s68_finding_001`).
- **Step 11 verbatim scan = real flip gate again:** 3 HARD hits (8+ word runs) on a generic thinning-instruction echo of a Clemson page; Trevor approved a reword; 10 strings reworded (biology-fixed numbers kept, connective wording varied) -> 0 HARD hits. 10 borderline = benign (binomials, generic instructions). Coverage 24/33 URLs (9 PDFs/404s/JS NOT COVERED, stated honestly).
- **Verify:** whole_crop_gate PASS(0), register PASS, release_verify clean (only carrot changed; lettuce byte-identical; no new violations), verbatim 0 HARD. Flipped `verification_status` -> full certified anchor shape (`verified_gs_arc`). Promoted `b34bd6fc`.

## Active work + next step
- **NEXT = anchor 5 (roadmap call).** Per the anchor expansion: microgreen (covers the non_seasonal_indoor archetype before the bots derive the pipeline) or one of the 6 family hubs (peach/broccoli/bell-pepper/zucchini/onion/green-beans-bush).
- **Carrot deferrals (non-blocking):** region-tip override shape (`carrot_s68_finding_001`; build when a renderer consumes region-conditioned tips); dict-shell `sources`/`anchoring_urls` plumbing inconsistency (watering/fertilizer/thinning/varieties lack it; dataset-wide drift) -> 2.9 normalization; `harvest_urgency` + `fertilizer.frequency` value-vocab (level "low" vs cadence "daily"/"every 2 weeks") -> dataset-wide vocab ruling at 2.9.
- **PARKED (unchanged):** WeatherKit resolver deferred; USCRN workstream (uscrn_validation null); 2.9 shell-shape normalization; v1.7 checklist amendment (Step 3.5 promote = retro; + author-fresh Steps-6-8-author-from-scratch note); register inventory on-disk; `fruit_set_temp_f`. PK refresh owed: `second_planting_structure_spec` **v1.1** (promoted to 05-methodology/current 2026-06-10).

## Gate record (generated 2026-06-10, on canonical `b34bd6fc`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **4 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails (carry into anchor 5)
- **AUTHOR-FRESH model proven end-to-end:** carrot is the first crop taken wiped-shell -> certified entirely author-fresh. Every value from the crop's own sources; bulk prose authored from scratch at Steps 6-8 (the retro arc assumed it pre-existed). "Matches an anchor" is never a justification (A1); derive + attest independently.
- **CATALOG PRECISION (Exeter moat) is Claude Code's lane:** `ipm.ucanr.edu` -> `uc_ipm`, NOT the umbrella `ucanr_ext`. Claude Code holds the full catalog; claude.ai only gets the crop's source subset, so it cannot see IDs outside it -- re-point on release. This is exactly what the protocol #6 cross-check catches.
- **Step-11 verbatim scan is flip-blocking:** a >=8-word shared run with a cited source = HARD hit; reword to break the run (route to the voice lane / Trevor, do NOT self-dismiss). Generic numeric conventions + binomials are benign-class. `tools/verbatim_scan.py` (two-step: fetch URLs to cache, then scan); state coverage honestly (PDFs/JS = NOT COVERED).
- **SUCCESSION shape (spec v1.1):** `succession_continuous` (string) for window_type continuous; `succession_spring`/`succession_fall` for split; one crop can hold both. **HEAT ANCHOR:** `heat_threshold_temp_f` = AIR (carrot 75°F, UF/IFAS AE588); germination stays soil_temp_40f.
- **AUTHOR-FRESH discipline:** don't fabricate (uscrn null). **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). GOTCHA: shell `>` TRUNCATES before read -- `gen_current_state` reads the old file for its protocol header, so generate to a temp then `mv`. Catalog IDs minted/re-pointed by Claude Code. Anchor target ~18.
- **apply_patch.py** accepts the `ops` edit-list alias + APPENDS on `add` at list-index==len.
- **Lane split:** claude.ai authors/verifies; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints/re-points, the flip) + owns data SHAPE/naming. Run protocol #6 + roster gate + verbatim scan before every promote/flip. `zones{}` wiped on the 120 (kept on GS crops until Phase C).
