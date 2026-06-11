# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑 PEACH Steps 6-8b RELEASED -- the bulk care prose is COMPLETE except the events layer (anchor 5, the first tree). claude.ai authored (both registers) the care dicts (storage/fertilizer/watering prose/yield/rotation), the 2.9 perennial prose (bloom_time/pollinator_notes/rootstock traits/year_one), + top-level description/harvest_ready. 77 ops, SHA `4a3a4801` -> `59876b61`; minted `clemson_peach_diseases` (the no-replant anchor). J.H. Hale exception consistent across pollinator_notes + pollination.notes + the 6-8a blossom tip. **GAP (FLAG 3): `notifications` + `weather_triggers` are STILL empty -- they fell through the 6-8a/6-8b split and peach is NOT cert-ready until authored** (a 6-8c events pass, or fold into 9-11 prep -- Trevor's call). 4 anchors certified; peach NOT yet certified.

## Canonical pointer
- **Current SHA:** `59876b61468a7b6460725e92110a3f2e4a5870bb9fb0b77afef72bb1279e9e61`. `LATEST.txt` session: `peach_steps6_8b` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)

## What just happened (2026-06-11, session `peach_steps6_8b` -- claude.ai authoring + Claude Code release)
- **Peach Steps 6-8b (the second half of the bulk care prose) RELEASED.** 77 ops, base `4a3a4801`. claude.ai authored, both registers: top-level `description_*` + `harvest_ready_*`; `storage` (counter-ripen, chilling-injury/mealiness caveat), `yield_expectations` (~50-150 lb/mature tree, full bearing yr 4-6), `fertilizer` (incl. `amount_*`: ~1 cup 10-10-10 per yr of tree age, spring, never late-season; skip post-harvest if frost took the crop), `watering` prose (`method_note_*` keep canopy dry; `critical_periods_*` = the final-swell last 2-4 wk; `schedule_by_stage[].note_*`), `rotation` (HONEST for a tree: `rotation_years:null` + the replant-disease angle), `moon_phase_preference` (honest NONE, `evidence_tier:"none"`); 2.9 perennial prose: `bloom_time_*`, `pollinator_notes_*` + `pollination.notes_*` (self-fertile, INVERSE of apple, WITH the J.H. Hale exception), `rootstock_options[0-3].traits_*` (Lovell/Halford/Guardian/Nemaguard), `year_one_notes_*`. Sources: clemson_hgic/ncsu_ext/umd_ext (FS-1141 chilling injury)/uf_ifas_edis (HS1413 irrigation).
- **Claude Code release:** **slice-integrity SHA matched byte-for-byte** (claude.ai's 77 ops reproduced exactly; b2b1c1b3 on the peach crop object). **MINTED `clemson_peach_diseases`** (FLAG 1 -- Clemson HGIC Peach Diseases factsheet, T1, the distinct no-replant anchor for `rotation`; catalog 87 -> 88). Gates: whole_crop_gate peach PASS(0) (18 sources, 101 claim-leaves 0 gaps); register PASS; release_verify (only peach + catalog +clemson_peach_diseases [the mint] + the 10 benign tree-chill-key concerns); 4 anchors PASS. Verbatim scan still DEFERRED to Step 11. Promoted `59876b61`.

## Active work + next step
- **GAP -> NEXT (Trevor's call): `notifications` + `weather_triggers` are unauthored** (both empty `[]`). They fell through the 6-8a/6-8b split (the original 6-8 kickoff listed them, but the 6-8a snippet's carry-forward + the 6-8b kickoff omitted them). The cert gate needs them (cherry has 7 notifications / 5 weather_triggers). For a tree these are the dormant-prune reminder, the late-frost-on-bloom alert, the establishment-year deep-watering, harvest. **Author them in a small 6-8c events pass (recommended) or fold into the Steps 9-11 prep before the flip.**
- **Then Steps 9-11 (cert):** the definitive cross-crop verbatim scan (the flip gate) + the perennial CERT branch (the two-way no-fruit rule, built + tested against FILLED peach) + the launch_ready flip.
- **OWED:** PK re-upload of the v1.8 amendment + tree spec (in `HANDOFF_peach_steps6-8b/2_ADD_TO_PROJECT_KNOWLEDGE/`); Appendix A registration of the tree growth_stages stems; **perennial-aware `rotation` shape** (FLAG 2: a `rotation_applicable:false`/`replant_disease_*` variant in the tree spec before apple, so the renderer doesn't imply a rotation interval); FLAG B `_build_tree_shells` (region_id/label/zone_span + stray-key strip) for apple; the whole_crop_gate perennial CERT branch.
- **PARKED:** FLAG C (`usda_phzm`); FLAG 1 (rootstock selection_basis) -> apple; WeatherKit; USCRN; C1/C3 vocab; soil `_seasoned` back-fill; evergreen/citrus `calendar_basis` -> lemon.

## Gate record (generated 2026-06-11, on canonical `59876b61`)
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

## Live locked decisions / guardrails (carry into peach events + cert + every tree/perennial anchor)
- **TREE care-prose honesty (peach 6-8b):** a permanent tree's `rotation_years` is `null` (N/A) -- the honest angle is replant-disease (no Prunus-after-Prunus). `moon_phase_preference.phase` is `null` + `evidence_tier:"none"` (no T1 basis). `fertilizer` rate ~1 cup 10-10-10 per yr-of-age, spring only. `harvest_urgency` = a LEVEL ("high"). `rotation` dict shape is annual-built -> a perennial-aware variant (`rotation_applicable:false`/`replant_disease_*`) is OWED in the tree spec before apple.
- **TREE growth_stages SHAPE:** `day_range_from_sow:null` + `year_phase` enum (ruled MACHINERY) + `timing_*` prose; growth_stages (journey) and tips_by_stage (tip roster) need NO 1:1 parity.
- **NO-FRUIT CALENDAR = the DIRECTION SPLIT (FLAG A; verified Step 5):** `survives_no_fruit` carries a calendar IFF `chill_hours_delivered[0] >= the crop's lowest variety chill` (400). v1.8 amendment §5.
- **SURVIVES != FRUITS FIRST-CLASS:** crop `hardiness_zone_min/max` (survives) vs `reliable_fruit_zone_min/max` (fruits), distinct (4-9 / 5-9); per-zone `suitability` enum.
- **TREE REGION MODEL (`tree_region_model_spec_v1_0`):** `calendar_basis=perennial_chill_gated`; ONE `track:"perennial"` establishment entry; render keys REUSE the annual names (`plant_out`/`bloom`/`harvest_*`); `dormant` = 14th calendar token.
- **PEACH/tree biology:** SELF-FERTILE at crop level BUT recommended J.H. Hale is the exception -- consistent across pollinator_notes_* / pollination.notes_* / the blossom tip / the no-fruit failure_diagnostic. Chill VARIETY-driven [200,1050]. Rootstocks by SOIL/NEMATODE tolerance not size (FLAG 1 -> apple).
- **apply_patch numeric-key rule (hardened):** numeric JSON-Pointer token -> dict string-key vs list index by node type (RFC-6901). **Slice-integrity check:** claude.ai may ship a post-apply crop-object SHA; verify the applied peach crop hashes to it (caught 0 drift on 6-8b).
- **CANONICAL SHAPES + COMPACT JSON:** `anchoring_urls={id:{url,verified}}`; soil texture = enum-token arrays; companion provenance = `research_backed`/`likely`/`traditional`. COMPACT (`separators=(",",":")`, no trailing newline; gen CURRENT_STATE to temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the flip) + owns SHAPE/naming + renderer. Dataset push autonomous (announce-then-execute); plant-astro Trevor-gated. The definitive verbatim scan is Claude Code's at the Step-11 flip (intermediate 6-8 releases defer it).
