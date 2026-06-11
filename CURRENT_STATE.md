# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH AUTHORING COMPLETE -- Steps 6-8c (the events layer) RELEASED; the first tree is fully authored and ready for cert (Steps 9-11). claude.ai authored the last gap: 8 `notifications` (tree events: bare-root planting, dormant prune, bloom-frost watch, fruit thinning, establishment watering, final-swell harvest, sanitation, inactivity) + 5 `weather_triggers` (FROST_WARNING high = the crop-killer, humidity/rain for brown rot, drought, heat). SHA `59876b61` -> `0d3ed015`. **All bulk prose is now filled** (pests/diseases/stages/tips/diagnostics/care dicts/perennial prose/events). **NEXT = Steps 9-11 (cert, mostly Claude Code's lane):** the cross-crop verbatim scan + the perennial CERT gate branch + the launch_ready flip. **4 anchors certified; peach is anchor 5, authoring-complete, pre-cert.** (Anchor TARGET ~18.)

## Canonical pointer
- **Current SHA:** `0d3ed015dbc10fa8a6bbf2ac62fa14053f219469bcbe2bf52502d0eb5f8c111e`. `LATEST.txt` session: `peach_steps6_8c` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)

## What just happened (2026-06-11, session `peach_steps6_8c` -- claude.ai authoring + Claude Code release)
- **Peach Steps 6-8c (the EVENTS layer) RELEASED -- the last bulk-prose gap (FLAG 3) closed.** 2 ops, base `59876b61`: `notifications` []->8, `weather_triggers` []->5. Authored as a TREE (NOT annual sow/harden-off): 8 notifications (`bareroot_planting`/`dormant_prune`/`bloom_frost_watch`/`fruit_thinning`/`establishment_watering`/`final_swell_harvest`/`end_of_season_nudge`/`inactivity`, offset_from last_frost/first_frost/bloom_start) + 5 weather_triggers (FROST_WARNING high [the late-frost-on-bloom crop-killer], HIGH_HUMIDITY + HEAVY_RAIN [brown rot], DROUGHT high [final swell], HEAT_STRESS low). Each consistent with the already-authored frost_risk_note / brown-rot disease / thinning tip / watering critical_periods / year_one_notes. No new catalog IDs (events reference already-sourced biology; the cherry/carrot shape carries no `sources` on event nudges).
- **Claude Code release:** slice-integrity SHA MATCHED byte-for-byte (peach crop object `72e2dd85`). Gates: whole_crop_gate peach PASS(0) (18 sources, 101 claim-leaves 0 gaps); register PASS; release_verify clean (only peach, no catalog change, lettuce byte-identical, the 10 benign tree-chill-key concerns); 4 anchors PASS. Verbatim scan still DEFERRED to Step 11. Promoted `0d3ed015`. (Also fixed the stale `v1.6` checklist pointer in this protocol header -> `v1.7 + v1.8 amendment`.)
- **PEACH BULK PROSE IS NOW COMPLETE** -- every authoring section is filled (verified: pests 5 / diseases 3 / growth_stages 8 / tips_by_stage 9 / failure_diagnostics 4 / storage / fertilizer / watering / yield / rotation / the 2.9 perennial prose / notifications 8 / weather_triggers 5). The honest-nulls (rotation_years, moon_phase.phase, the N/A-for-tree annual scalars, the vestigial growth_stages_year_one/annual) are intentional.

## Active work + next step
- **NEXT = peach Steps 9-11 (CERT -- mostly Claude Code's lane):** (1) the **definitive cross-crop verbatim scan** (`tools/verbatim_scan.py` -- fetch the cited URLs + scan; the flip-blocking gate; reword any HARD hits with Trevor); (2) build + run the **whole_crop_gate perennial CERT branch** (the two-way `survives_no_fruit` no-fruit-calendar rule, the one-establishment-entry / no-succession invariants -- against FILLED peach); (3) a per-crop §3 cross-field pass; (4) the **launch_ready flip** (status `verified_gs_arc`, launch_ready_core/seasoned true, last_reviewed set). claude.ai may do a Step-9/10 side-by-side verification pass first (its lane).
- **Fold into the cert pass (the deferred structural tidy):** the **perennial-aware `rotation` shape** (FLAG 2: `rotation_applicable:false`/`replant_disease_*` variant in the tree spec); null the vestigial `growth_stages_year_one`/`_annual` to match the certified crops; **FLAG B `_build_tree_shells`** (region_id/label/zone_span + stray-key strip) for apple; Appendix A registration of the growth_stages `timing_*`/`year_phase` stems.
- **OWED (Trevor):** the PK cleanup -- `PK_CLEANUP/` (delete 4 superseded + replace 3 stale-current incl. the v1.8 amendment + tree spec).
- **PARKED:** FLAG C (`usda_phzm`); FLAG 1 (rootstock selection_basis) -> apple; WeatherKit; USCRN; C1/C3 vocab; soil `_seasoned` back-fill; evergreen/citrus `calendar_basis` -> lemon.

## Gate record (generated 2026-06-11, on canonical `0d3ed015`)
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

## Live locked decisions / guardrails (carry into peach cert + every tree/perennial anchor)
- **TREE events (peach 6-8c):** authored as a tree (no annual sow/harden-off/transplant); `notifications`/`weather_triggers` carry the dual-register `title_*`/`body_*` pair only (the rest -- id/trigger_type/offset_from/stage/action/condition/severity/active_stages/audience -- is machinery, no `sources` array on event nudges). FROST_WARNING (late-frost-on-bloom) is the highest-severity peach weather event.
- **NO-FRUIT CALENDAR = the DIRECTION SPLIT (FLAG A; verified Step 5):** `survives_no_fruit` carries a calendar IFF `chill_hours_delivered[0] >= the crop's lowest variety chill` (400). v1.8 amendment §5. **SURVIVES != FRUITS first-class** (crop `hardiness_zone_*` vs `reliable_fruit_zone_*`; per-zone `suitability`).
- **TREE REGION MODEL (`tree_region_model_spec_v1_0`):** `calendar_basis=perennial_chill_gated`; ONE `track:"perennial"` establishment entry; render keys REUSE the annual names (`plant_out`/`bloom`/`harvest_*`); `dormant` = 14th calendar token. **TREE care honesty:** `rotation_years:null` (replant-disease angle instead), `moon_phase.phase:null` (`evidence_tier:"none"`), N/A-for-tree annual scalars null, vestigial `growth_stages_year_one/_annual` null (all certified crops). growth_stages: `day_range_from_sow:null` + `year_phase` enum + `timing_*` prose; no growth_stages<->tips_by_stage parity.
- **PEACH/tree biology:** SELF-FERTILE at crop level BUT recommended J.H. Hale is the exception (consistent across pollinator_notes / pollination.notes / blossom tip / no-fruit diagnostic / bloom-frost notification). Chill VARIETY-driven [200,1050]. Rootstocks by SOIL/NEMATODE tolerance not size (FLAG 1 -> apple).
- **apply_patch numeric-key rule:** numeric JSON-Pointer token -> dict string-key vs list index by node type (RFC-6901). **Slice-integrity:** verify the applied peach crop hashes to claude.ai's post-apply crop-object SHA (3/3 matches this arc, 0 drift).
- **CANONICAL SHAPES + COMPACT JSON:** `anchoring_urls={id:{url,verified}}`; soil texture = enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. COMPACT (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + owns SHAPE/naming + renderer. Dataset push autonomous (announce-then-execute); plant-astro Trevor-gated. **The definitive verbatim scan is Claude Code's at the Step-11 flip** (intermediate authoring releases defer it; claude.ai self-scans). **Methodology disk is master; PK copies drift -> refresh (see PK_CLEANUP).**
