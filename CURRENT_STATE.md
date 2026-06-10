# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Steps 1-3 IN PROGRESS -- anchor 5, the FIRST tree (Stone Fruit hub). Structured spine authored: scalars + the 2.9 perennial fields (chill/bloom/pollination/rootstock/windows/establishment) + the variety bloom-calendar data (8 recommended varieties) + universal watering + companions. **10 region cells STILL EMPTY -> NEXT = Step 3.5: the TREE region/calendar model (Claude Code, NEW territory).** 4 anchors certified (cherry/beefsteak/carrot/lettuce).

## Canonical pointer
- **Current SHA:** `621c79af3da48a4c376d65cb97fbd4690050ae8e8290638e26c4906c0c763e86`. `LATEST.txt` session: `peach_steps1_3` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register

## What just happened (2026-06-10, session `peach_steps1_3` -- claude.ai authoring + Claude Code release)
- **Peach Steps 1-3 RELEASED** (49-op patch, base `0be2652c` -> `621c79af`). claude.ai built the source set (7 T1 pomology IDs, all in-catalog, none invented) + authored scalars/structured incl. 2.9 perennial fields (chill_hours_range [200,1050]; **pollination self_fertile=true -- peaches are self-fertile, unlike apple**; rootstock_options x4; dormancy/pruning windows; establishment_years 3) + the variety bloom-calendar data (8 recommended varieties spanning low->high chill, each with bloom_group/bloom_window_relative/chill) + universal watering_method/schedule_by_stage + companions. Region cells UNTOUCHED (Step 3.5).
- **apply_patch HARDENED (test-first, absorbs 3 peach drifts):** (1) JSON-Pointer paths (`/sunlight`, `/soil/x`, `/opts/0/name`) -> dot/bracket; (2) top-level `crop` envelope key read for slug; (3) from-guard tolerates empty-equivalent (wipe types lists [] / dicts {} / scalars null) + no-op (cur==value on KEPT fields like `difficulty`) -- base_sha stays the authoritative drift gate. `test_apply_patch` +1d/+1e.
- **3 shape deviations cleaned on release (content SOUND, shape off):** companion vocab `extension_backed`->`research_backed` (match carrot, the current exemplar); soil texture `_core` prose strings -> canonical **enum-token arrays** (faithful token extraction; `_seasoned` left null = claude.ai back-fill owed); flat `{id:url}` anchoring_urls -> canonical `{id:{url,verified:"2026-06-10"}}` (27 entries / 30 blocks).
- **Gates:** register PASS; release_verify clean (only peach; lettuce byte-identical; no new violations); whole_crop_gate peach = 10 violations, ALL pre-existing region-unfilled (IDENTICAL to base -- Step 3.5 builds them). Promoted `621c79af`.

## Active work + next step
- **NEXT = peach Step 3.5: the TREE region/calendar model (Claude Code, NEW territory).** A permanent tree's cycle is bloom->fruit->harvest->dormant-prune + hardiness/chill-adequacy by zone, NOT an annual planting window. The 10 region cells + `resolved_by_zone` were scaffolded for the annual model; Step 3.5 designs what a region/zone cell MEANS for a permanent tree (hardiness/suitability; chill-adequacy resolution -> which varieties set fruit per region; absolute bloom-date resolution per 2.9 A4). `calendar_basis` may need a new value (`perennial_chill_gated`). (Emerges like the heat anchor did mid-carrot.)
- **claude.ai follow-ups owed (fold into the Step-4 kickoff):** (a) soil `_seasoned` texture variants back-fill; (b) ADOPT canonical sub-object shapes going forward -- `anchoring_urls = {id:{url,verified}}`, soil texture = enum-token arrays -- so apple/lemon don't repeat the deviation; (c) dormancy/pruning window shape ratified against the Step 3.5 calendar model.
- **FLAG 1 (rootstock model, for Trevor):** peach rootstocks do NOT control size (unlike apple) -- chosen for soil/nematode tolerance. Accepted claude.ai's pragmatic shape (size_class="standard" x4, choose-by axis in `what_to_ask_nursery`). OPEN: add a per-archetype rootstock `selection_basis` enum (`size`[pome] | `soil_pest_tolerance`[stone])? Defer until apple gives the pome data point + a renderer consumer.
- **PARKED (unchanged):** WeatherKit; USCRN; 2.9 per-anchor back-fill; C1 register-reshape + C3 vocab-value-reconcile; carrot region-tip override. **PK refresh owed:** v1.7 checklist + schema_2_9_spec + second_planting v1.1.

## Gate record (generated 2026-06-10, on canonical `621c79af`)
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

## Live locked decisions / guardrails (carry into peach Step 3.5 + the tree anchors)
- **CANONICAL SUB-OBJECT SHAPES (claude.ai must match; Claude Code cleans on release if not):** `anchoring_urls = {source_id: {url, verified}}` (NOT flat `{id:url}`); soil texture fields = arrays of snake_case enum tokens (`["sandy_loam","loam"]`, NOT prose); companion provenance vocab = `research_backed`/`likely`/`traditional` (carrot/current; cherry+lettuce still carry the OLD `extension_backed`/`mechanistic` -- a back-migration is a normalization item).
- **apply_patch absorbs claude.ai path/guard drift:** JSON-Pointer (`/a/b`) + dot + `$`-rooted + bracket-slug paths; slug from `crop`/`_meta.crop`/etc.; `ops` alias; `add` appends at list-index==len; from-guard tolerant of empty-equivalent + no-op (base_sha is the real drift gate). All test-first in `test_apply_patch`.
- **PEACH/tree biology:** peaches are SELF-FERTILE (don't import apple's needs-pollinizer); chill is VARIETY-driven (crop-level chill_hours_required null + chill_hours_range = "varies, see varieties", the apple-mock convention); peach rootstocks select by SOIL/NEMATODE tolerance, not size (FLAG 1). A permanent tree's region/calendar model (bloom/harvest/prune + chill-adequacy/hardiness) is NEW -- designed at Step 3.5, NOT the annual planting-window model.
- **SCHEMA 2.9 model:** crop = entity/guide/URL; variety = DELTA overlay ({value,parent,changed}); bloom-overlap calendar rides curated `varieties.recommended[]` objects (NO full Phase-5 dep); 3-tier info hierarchy; perennial fields FLAT null-by-archetype. Migrations are additive null-scaffold (never un-earn a cert). **SUCCESSION v1.1** (succession_continuous / spring+fall). **HEAT ANCHOR** = AIR.
- **AUTHOR-FRESH (A1):** every value from the crop's own sources; "matches an anchor" is never a justification. **CATALOG PRECISION** = Claude Code's lane. **Step-11 verbatim_scan** is flip-blocking. **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; `>` truncates before read -> gen CURRENT_STATE to a temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes/migrations, catalog mints, the flip) + owns data SHAPE/naming + builds the renderer. Run protocol #6 + roster gate + verbatim scan before every promote/flip.
