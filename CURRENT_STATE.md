# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Steps 6-8a RELEASED -- the core biology compounds + tree-stage journey (anchor 5, the first tree). claude.ai authored (both registers) peach's pests (5), diseases (3), growth_stages (8, the TREE journey), failure_diagnostics (4), all 9 `tips_by_stage` tree stages (17 tips), + `harvest_urgency`. Released SHA `3e07c4e1` -> `4a3a4801`. **Steps 6-8 SPLIT into 6-8a (done) + 6-8b (next):** 6-8b = the care dicts (storage/fertilizer/watering prose/yield/rotation) + the 2.9 perennial prose (bloom_time/pollinator_notes [J.H. Hale exception]/rootstock traits) + events (notifications/weather_triggers) + top-level (description/harvest_ready). Peach **NOT yet certified** (cert = Step 11); **4 anchors certified**. (Anchor TARGET ~18.)

## Canonical pointer
- **Current SHA:** `4a3a48012ee9f2edfb620a650679878812be269ba013011a40eeefb4d83b19f9`. `LATEST.txt` session: `peach_steps6_8a` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)

## What just happened (2026-06-11, session `peach_steps6_8a` -- claude.ai authoring + Claude Code release)
- **Peach Steps 6-8a (the first half of the bulk care prose) RELEASED.** claude.ai authored, both registers, as a TREE: 5 pests (peachtree borer, plum curculio, OFM, catfacing, lesser peachtree borer), 3 diseases (leaf curl, brown rot, bacterial spot), 8 `growth_stages` (the perennial JOURNEY: planting -> establishment -> scaffold_formation -> dormancy -> dormant_prune -> blossom -> fruit_set -> harvest), 4 `failure_diagnostics`, 17 `tips_by_stage` tips across all 9 tree stages, + `harvest_urgency:"high"`. 14 ops, base `3e07c4e1`. Sources: clemson_hgic + iastate_ext + mu_ext + ncsu_ext (all in the 17-set, 0 out-of-set). The J.H. Hale self-incompatibility caveat is ALREADY stated correctly in the `blossom` tip + the no-fruit `failure_diagnostics` (6-8b's `pollinator_notes_*` must stay consistent).
- **Claude Code flag resolutions (the 4 FLAGS were addressed to me):** FLAG1 -- accepted the tree growth_stages shape (`day_range_from_sow:null` since a tree has no sow date; new `year_phase` enum [establishment|annual_cycle] + `timing_seasoned/_beginner` prose carry the journey timing); explicitly RULED `year_phase` in `register_completeness EXCLUDED_KEYS` (timing_* are suffix-ruled). FLAG2 -- the gate walks generically; growth_stages (8 ids) and tips_by_stage (9 keys) need NO 1:1 parity, gate PASS confirms. FLAG3 -- accepted the correctly-attributed portal IDs (clemson/iastate/mu/ncsu with peach-specific factsheet URLs); the optional precision mint (iastate_plc etc.) + the out-of-set corroborators (PSU/UC IPM) DEFERRED, not needed (every claim anchored in-set). FLAG4 -- `harvest_urgency:"high"` is a valid LEVEL (carrot uses "low"; the field's level-vs-cadence inconsistency across crops is the known C3 vocab item).
- **Gates (protocol #6):** whole_crop_gate peach PASS(0); register PASS (year_phase ruled); release_verify clean (only peach, lettuce byte-identical, the 10 benign tree-chill-key concerns); 4 anchors PASS; counts cross-check (5/3/8/4/17). **Verbatim scan DEFERRED to Step 11** (the definitive cross-crop flip gate, run when all 6-8 prose is in; claude.ai self-scanned 0 6-gram overlap). Promoted `4a3a4801`.

## Active work + next step
- **NEXT = peach Steps 6-8b (claude.ai):** the SECOND half of the bulk prose -- `description_*`, `harvest_ready_*`, `storage`, `yield_expectations`, `fertilizer` (incl. amount_*), `watering` prose (`method_note_*`/`critical_periods_*`/`schedule_by_stage[].note_*`), `rotation` (N/A-for-a-tree honesty + replant-disease angle), `varieties.note_*`, `moon_phase_preference`, + the 2.9 perennial prose (`bloom_time_*`, `pollinator_notes_*` [MUST accommodate the J.H. Hale exception], `pollination.notes_*`, `rootstock_options[].traits_*`, `year_one_notes_*`). Handoff = `HANDOFF_peach_steps6-8b/`. Then 9-11 (cert: the verbatim scan + the flip).
- **OWED:** (a) PK re-upload of the UPDATED v1.8 amendment (§5 two-way) + tree spec (§3 render keys) -- in `HANDOFF_peach_steps6-8/2_ADD_TO_PROJECT_KNOWLEDGE/`. (b) Appendix A registration of the tree growth_stages stems (`timing_*` CORE-PROSE, `year_phase` MACHINERY). (c) whole_crop_gate perennial CERT branch (Step 11). (d) FLAG B `_build_tree_shells` (region_id/label/zone_span + stray-key strip) for apple. (e) optional `iastate_plc`/UC-IPM catalog precision (deferred).
- **PARKED:** FLAG C (`usda_phzm`); FLAG 1 (rootstock selection_basis) -> apple; WeatherKit; USCRN; C1/C3 vocab; soil `_seasoned` back-fill; evergreen/citrus `calendar_basis` -> lemon.

## Gate record (generated 2026-06-11, on canonical `4a3a4801`)
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

## Live locked decisions / guardrails (carry into peach Steps 6-8b + every tree/perennial anchor)
- **TREE growth_stages SHAPE (peach 6-8a):** a permanent tree has no sow date, so `growth_stages[].day_range_from_sow` is `null`; the journey timing lives in `year_phase` (enum `establishment`|`annual_cycle`, MACHINERY, ruled in register EXCLUDED_KEYS) + `timing_seasoned`/`timing_beginner` (CORE-PROSE prose locator). growth_stages = the narrative JOURNEY (8 ids); `tips_by_stage` = the authoritative tip roster (9 keys); NO 1:1 parity required (the gate walks generically). Appendix A registration of the stems owed.
- **NO-FRUIT CALENDAR = the DIRECTION SPLIT (FLAG A; verified Step 5):** a `survives_no_fruit` cell carries a calendar IFF `chill_hours_delivered[0] >= the crop's lowest variety chill` (400 for peach) -- COLD-edge keeps it (under-reports if empty), CHILL-edge stays empty (over-promises if not); `unsuitable` always empty. v1.8 amendment §5 carries the rule.
- **SURVIVES != FRUITS is FIRST-CLASS:** crop `hardiness_zone_min/max` (survives) vs `reliable_fruit_zone_min/max` (fruits), distinct (peach 4-9 / 5-9); per-zone `suitability` enum. Honest "doesn't-grow-here" cells.
- **TREE REGION MODEL (`tree_region_model_spec_v1_0`):** region = "can I grow it + which varieties"; zone = "exactly when". `calendar_basis = perennial_chill_gated`; ONE `track:"perennial"` establishment plantings entry; render keys REUSE the annual names (`plant_out`/`bloom`/`harvest_*` -- NOT the spec example's `*_dates`, fixed); `dormant` = 14th calendar token.
- **PEACH/tree biology:** SELF-FERTILE at crop level BUT recommended J.H. Hale is the exception (handled at variety level + the blossom tip + failure_diagnostics; 6-8b `pollinator_notes_*` must stay consistent). Chill VARIETY-driven [200,1050]. Rootstocks by SOIL/NEMATODE tolerance not size (FLAG 1 -> apple). `harvest_urgency` = LEVEL (peach "high"); the level-vs-cadence inconsistency across crops is the C3 vocab deferral.
- **apply_patch numeric-key rule (hardened):** numeric JSON-Pointer token -> dict string-key when node is a dict (`resolved_by_zone/4`), list index when a list (`rootstock_options/0`); RFC-6901, test-first.
- **CANONICAL SUB-OBJECT SHAPES + COMPACT JSON:** `anchoring_urls={id:{url,verified}}`; soil texture = enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. COMPACT (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to a temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes, mints, the flip) + owns SHAPE/naming + renderer. Dataset push autonomous (announce-then-execute); plant-astro Trevor-gated. The definitive verbatim scan is Claude Code's at the Step-11 flip (intermediate 6-8 releases defer it; claude.ai self-scans).
