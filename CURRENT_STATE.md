# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Step 4 RELEASED -- the tree REGION BIOLOGY is filled (anchor 5, the first tree). claude.ai authored all 10 region cells + 20 zone cells + the crop-level two-band hardiness strip (survives 4-9 / fruits 5-9), and Claude Code released the merged Step 4 + z4 patch (456 ops, SHA `e99001f2` -> `3e07c4e1`). **FLAG A resolved (Trevor picked the direction split):** a `survives_no_fruit` cell carries a calendar IFF chill is reliably met (`chill_delivered[0] >= lowest variety chill, 400`) -- cold-edge z4 (banks 1,100-1,500, blooms every May, frost-loses the crop) gets its calendar; the 3 chill-limited warm cells stay empty; hawaii `unsuitable` empty. Suitability: 6 fruits_reliably / 7 marginal / 4 survives_no_fruit / 3 unsuitable. Peach is **NOT yet certified** (Step 4 = fill; cert is Step 11); **4 anchors certified** (cherry/beefsteak/carrot/lettuce). (Anchor TARGET ~18, a roadmap call.)

## Canonical pointer
- **Current SHA:** `3e07c4e1d2fc7b5a5c6d0f7496ed5db60d67f555519b4dd5fa16af521d75e0c2`. `LATEST.txt` session: `peach_step4` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)

## What just happened (2026-06-10, session `peach_step4` -- claude.ai authoring + Claude Code release)
- **Peach Step 4 (tree region biology fill) RELEASED.** claude.ai authored, per the tree_region_model spec: crop-level `hardiness_zone_min/max` 4/9 (survives) + `reliable_fruit_zone_min/max` 5/9 (fruits) + `hardiness_notes_*` + `chill_hours_note_*`; per region (all 10) `chill_hours_delivered` band + `chill_basis_*` + `region_notes_*` + the `track:"perennial"` establishment `plantings[0]` rule; per zone (20 cells) `suitability` verdict + notes, zone chill, absolute bloom/harvest/plant render strings, the 12-month tree `calendar[]` (first use of `dormant`), `frost_risk_note_seasoned`, `resolved_from`, `resolution_method:"perennial_precompute"`. Calendars generated deterministically from the dates (coherence-by-construction). 17 source IDs, all in-catalog T1 (no mints).
- **FLAG A (no-fruit calendar) resolved -> the DIRECTION SPLIT (Trevor).** Replaced the blanket "survives_no_fruit -> empty" with: carry a calendar IFF `chill_delivered[0] >= min variety chill (400)`. z4 (cold-edge, chill abundantly met, blooms every May) re-authored with its cycle + an "unreliable crop" caveat (a `peach_step4_z4_followup` one-cell patch, merged into the release); the 3 chill-limited warm cells (ca_south/ca_desert/fl_peninsula z10) stay empty; unsuitable empty. The v1.8 amendment Section 5 now encodes this two-way rule (PK re-upload owed). This dissolves the spec-vs-amendment contradiction (spec example = the cold-edge case; both consistent).
- **Release (protocol #6):** applied the 456-op merged patch (448 Step 4 + 8 z4), base `e99001f2`. Claude Code structural cleanup: stripped 3 stray annual-residue keys (`zone_8_presence`x2, `zone_10_desert_fold`). whole_crop_gate peach PASS(0); register PASS; release_verify collateral clean (only peach, lettuce byte-identical, no catalog change) + calendar coherence PASS (incl. z4) + the 10 "novel tree-key vs annual-exemplar" concerns adjudicated benign; 4 anchors PASS. Cross-check: every claude.ai claim matches (20 cells, 6/7/4/3 suitability, dormant used, honesty test). **apply_patch HARDENED (test-first):** numeric JSON-Pointer token vs a DICT now resolves as a string key, not a list index (`resolved_by_zone/4/...` was the first patch to touch zone-keyed cells; `_child`/`leaf_get`/`leaf_set`/`leaf_del` branch on node type per RFC-6901). Promoted `3e07c4e1`.

## Active work + next step
- **NEXT = peach Step 5+ (claude.ai):** Step 5 side-by-side region verification, then Steps 6-8 (the bulk prose: pests/diseases/growth_stages/tips_by_stage/storage/etc., dual-register, the tree-stage versions), then 9-11 (cert). Peach's region/timing layer is now authored; the bulk prose is the next push (same shape as carrot Steps 6-8).
- **OWED:** (a) **re-upload the updated `gold_standard_arc_checklist_v1_8_amendment.md` to PK** (Section 5 now carries the two-way no-fruit-calendar rule). (b) **whole_crop_gate perennial CERT branch (Step 11)** -- build + test against FILLED peach; it now has the two-way `survives_no_fruit` rule to enforce (chill-vs-floor), not the blanket one. (c) **FLAG B (build_region_shells):** fold `region_id`/`region_label`/`zone_span` population (claude.ai filled them this arc) + the stray-key strip into `_build_tree_shells` so apple's shells set them automatically.
- **FLAG C (deferred):** optional `usda_phzm` first-party USDA hardiness source mint -- not needed (extension sources sufficient); attach in a later verification pass if wanted.
- **PARKED (unchanged):** WeatherKit; USCRN; C1 register-reshape + C3 vocab-value-reconcile; soil `_seasoned` texture back-fill; evergreen/citrus `calendar_basis` variant -> lemon; FLAG 1 rootstock selection_basis -> apple.

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

## Live locked decisions / guardrails (carry into peach Step 5+ + every tree/perennial anchor)
- **NO-FRUIT CALENDAR = the DIRECTION SPLIT (FLAG A resolved, Trevor 2026-06-10).** A `survives_no_fruit` cell carries a calendar IFF chill is reliably met (`chill_hours_delivered[0] >= the crop's lowest variety chill`, 400 for peach) -- that is the COLD-edge case (tree blooms every year, frost loses the crop), and an empty calendar there UNDER-reports. Below the floor = CHILL-edge (no coherent bloom) -> empty (a calendar there OVER-promises). `unsuitable` -> always empty. The cert gate (Step 11) enforces this two-way; v1.8 amendment Section 5 carries the rule. Reference: peach z4 (cold-edge, has calendar) vs ca_south/ca_desert/fl_peninsula z10 (chill-edge, empty) vs hawaii z11 (unsuitable, empty).
- **SURVIVES != FRUITS is FIRST-CLASS (Trevor, explicit).** Crop-level `hardiness_zone_min/max` (survives) vs `reliable_fruit_zone_min/max` (fruits) -- distinct, never collapsed (peach 4-9 survives / 5-9 fruits); per-zone `suitability` = `fruits_reliably`/`marginal`/`survives_no_fruit`/`unsuitable`. Honest "doesn't-grow-here" cells (hawaii unsuitable, no fabricated window).
- **TREE REGION MODEL (`tree_region_model_spec_v1_0`):** region = "can I grow it + which varieties" (chill-adequacy band + suitability); zone = "exactly when it blooms/fruits/goes dormant" (resolved dates + tree `calendar[]`). `calendar_basis = perennial_chill_gated`. plantings[] = ONE `track:"perennial"` establishment entry (no succession/start_indoors). Render keys REUSE annual names. Feeds the apple-zone-6 3-track Gantt. `dormant` = the 14th calendar token.
- **PEACH/tree biology:** SELF-FERTILE; chill is VARIETY-driven (range [200,1050], 8 recommended varieties 400-1050); rootstocks select by SOIL/NEMATODE tolerance not size (FLAG 1 -> apple). `dormancy_window`/`pruning_window` month-band = coarse crop default; the per-zone calendar resolves the actual prune/dormant months.
- **apply_patch numeric-key rule (hardened 2026-06-10):** a numeric JSON-Pointer token resolves as a DICT string-key when the node is a dict (`resolved_by_zone/4`), a LIST index when the node is a list (`rootstock_options/0`) -- branch on node type (RFC-6901). Test-first in `test_apply_patch` (1f/1f-ii).
- **CANONICAL SUB-OBJECT SHAPES + COMPACT JSON:** `anchoring_urls = {id:{url,verified}}`; soil texture = enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. Canonical JSON COMPACT (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to a temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes/migrations, catalog mints, the flip) + owns SHAPE/naming + the renderer. Dataset push autonomous (announce-then-execute); plant-astro stays Trevor-gated. Run protocol #6 + roster gate + verbatim scan before every promote/flip.
