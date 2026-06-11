# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Step 5 VERIFIED -- the tree region/timing layer is source-confirmed (anchor 5, the first tree). claude.ai ran the 4-round side-by-side region verification vs the 17 cited T1 sources: **0 corrections.** Crop bands (survives 4-9 / fruits 5-9), the chill mechanism, all 10 region cells + 20 zone cells, and the FLAG-A no-fruit direction split all hold against source. **Verification-only -- canonical UNCHANGED at `3e07c4e1`** (no patch, no re-pin; like carrot Step 5). Peach is **NOT yet certified** (cert is Step 11); **4 anchors certified** (cherry/beefsteak/carrot/lettuce). NEXT = peach Steps 6-8 (bulk care prose). (Anchor TARGET ~18, a roadmap call.)

## Canonical pointer
- **Current SHA:** `3e07c4e1d2fc7b5a5c6d0f7496ed5db60d67f555519b4dd5fa16af521d75e0c2`. `LATEST.txt` session: `peach_step4` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)

## What just happened (2026-06-11, session `peach_step5` -- claude.ai region verification, NO dataset change)
- **Peach Step 4 region biology VERIFIED at the 4-round bar -- 0 corrections.** claude.ai re-confirmed every region/zone claim side-by-side against its cited T1 source (the carrot Step 5 standard): crop hardiness/fruit bands (bud-kill -13/-18°F 4-round; self-fertility), the chill mechanism (32-45°F window, >65°F subtracts, 4-round), all 10 region chill bands + the establishment rule, all 20 zone suitability verdicts (6/7/4/3) + dates + calendars (coherent, 0 conflations), and the FLAG-A direction split (z4 cold-edge has its calendar; the 3 chill-limited cells empty; unsuitable empty). 17 sources resolve, 0 dangling, 0 verbatim 6-gram overlap, 0 em-dash.
- **Verification-only -- nothing applied.** No patch, no gate re-run (0 bytes changed). Canonical UNCHANGED at `3e07c4e1`; logged so a future session does not re-run it. (Detail in STATE_HISTORY; log archived in `HANDOFF_peach_step5/FROM_CHAT/`.)

## Active work + next step
- **NEXT = peach Steps 6-8 (claude.ai):** the bulk care prose -- pests/diseases/growth_stages/`tips_by_stage` (tree-stage versions: dormancy/dormant_prune/establishment)/storage/watering/etc., dual-register -- same shape as carrot Steps 6-8. Then 9-11 (cert: verbatim scan + the flip).
- **CARRY into the Steps 6-8 kickoff (Step 5 forward note):** when the crop-level `pollinator_notes_*` / `pollination.notes_*` are authored (they drive the apple-guide pollination section, the inverse of apple), the "self-fertile -- a single tree fruits" headline MUST accommodate the recommended-variety **J.H. Hale exception** (NOT self-fertile) so the renderer section + the variety note don't contradict.
- **OWED:** (a) **PK re-upload of the UPDATED v1.8 amendment** -- claude.ai's Step 5 run saw the BLANKET rule still in PK; re-upload the master `05-methodology/current/gold_standard_arc_checklist_v1_8_amendment.md` (§5 two-way split), not an older copy. (b) **Tree spec §3 doc nit:** the worked-example JSON uses `plant_dates`/`bloom_dates`/`harvest_dates`, but §3a + the data + the amendment use the REUSED annual keys (`plant_out`/`bloom`/`harvest_*`); fix the example to match (PK re-upload, owed with the amendment). (c) **whole_crop_gate perennial CERT branch (Step 11)** enforcing the two-way `survives_no_fruit` rule. (d) **FLAG B `_build_tree_shells`** (region_id/label/zone_span + stray-key strip) for apple.
- **PARKED:** FLAG C (`usda_phzm` mint, optional); FLAG 1 (rootstock selection_basis) -> apple; WeatherKit; USCRN; C1 register-reshape + C3 vocab; soil `_seasoned` texture back-fill; evergreen/citrus `calendar_basis` -> lemon.

## Gate record (generated 2026-06-10, on canonical `3e07c4e1`)
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

## Live locked decisions / guardrails (carry into peach Steps 6-8 + every tree/perennial anchor)
- **NO-FRUIT CALENDAR = the DIRECTION SPLIT (FLAG A, Trevor; verified Step 5).** A `survives_no_fruit` cell carries a calendar IFF chill is reliably met (`chill_hours_delivered[0] >= the crop's lowest variety chill`, 400 for peach) -- COLD-edge (tree blooms every year, frost loses the crop; empty there UNDER-reports). Below the floor = CHILL-edge -> empty (a calendar OVER-promises). `unsuitable` -> always empty. Cert gate (Step 11) enforces two-way; v1.8 amendment §5 carries the rule (PK re-upload owed). Ref: peach z4 (has calendar) vs ca_south/ca_desert/fl_peninsula z10 (empty) vs hawaii z11 (empty).
- **SURVIVES != FRUITS is FIRST-CLASS (Trevor).** Crop-level `hardiness_zone_min/max` (survives) vs `reliable_fruit_zone_min/max` (fruits) -- distinct, never collapsed (peach 4-9 / 5-9); per-zone `suitability` `fruits_reliably`/`marginal`/`survives_no_fruit`/`unsuitable`. Honest "doesn't-grow-here" cells.
- **TREE REGION MODEL (`tree_region_model_spec_v1_0`):** region = "can I grow it + which varieties" (chill band + suitability); zone = "exactly when it blooms/fruits/goes dormant" (resolved dates + tree `calendar[]`). `calendar_basis = perennial_chill_gated`. plantings[] = ONE `track:"perennial"` establishment entry. Render keys REUSE the annual names (`plant_out`/`bloom`/`harvest_*`) -- the spec §3 EXAMPLE's `*_dates` names are an illustrative error to fix. `dormant` = the 14th calendar token. Feeds the apple-zone-6 3-track Gantt.
- **PEACH/tree biology:** SELF-FERTILE (crop-level), BUT recommended J.H. Hale is the exception (handled at variety level; the crop pollinator prose authored at 6-8 must accommodate it). Chill VARIETY-driven (range [200,1050], 8 varieties 400-1050). Rootstocks select by SOIL/NEMATODE tolerance not size (FLAG 1 -> apple). `dormancy_window`/`pruning_window` month-band = coarse default; calendar resolves the real prune/dormant months.
- **apply_patch numeric-key rule (hardened):** a numeric JSON-Pointer token resolves as a DICT string-key when the node is a dict (`resolved_by_zone/4`), a LIST index when a list (`rootstock_options/0`) -- branch on node type (RFC-6901). Test-first.
- **CANONICAL SUB-OBJECT SHAPES + COMPACT JSON:** `anchoring_urls = {id:{url,verified}}`; soil texture = enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. Canonical JSON COMPACT (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to a temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes, mints, the flip) + owns SHAPE/naming + the renderer. Dataset push autonomous (announce-then-execute); plant-astro Trevor-gated. A verification-only session (Step 5) records STATE_HISTORY + regenerates CURRENT_STATE but does NOT re-pin the SHA (no bytes changed).
