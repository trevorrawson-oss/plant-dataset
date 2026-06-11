# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🍑🌳 PEACH CERTIFIED -- anchor 5, the FIRST PERMANENT TREE (`verified_gs_arc`, launch_ready core+seasoned). Steps 9-11 closed: the cross-crop verbatim scan (2 brown-rot rewords, Trevor-approved -> 0 HARD hits), the NEW perennial cert-gate branch (`tools/perennial_gate.py`, test-first -> 0 violations: one establishment entry / suitability enum / the no-fruit DIRECTION SPLIT enforced), §3 clean, the launch_ready flip. SHA `0d3ed015` -> `7345b944`. **5 of ~18 anchors certified** (cherry/beefsteak/carrot/lettuce + peach -- the first tree, exemplar for apple/lemon/blueberry). The annual arc AND the tree arc are now both proven end-to-end. **NEXT = apple** (the first compressed tree-repeat -- it rides peach's rails, no structural redesign) toward the 2-3/day pace.

## Canonical pointer
- **Current SHA:** `7345b94469e5cbc0b783aa7b6c67c1940f52d0f65d7c179038af302131baba2c`. `LATEST.txt` session: `peach_steps9_11` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)
  - `621c79af` -- feat(peach): Steps 1-3 -- anchor 5, the first tree (scalars + 2.9 perennial + variety bloom calendar)
  - `0be2652c` -- feat(schema): migrate 2.8 -> 2.9 -- perennial/tree extension + watering/container + plumbing (additive)

## What just happened (2026-06-11, session `peach_steps9_11` -- the cert close + the flip)
- **Peach CERTIFIED.** Steps 9-11 ran in one pass: (9) copy conventions already clean (0 dash, °F, both registers, gates green through 6-8c); (10) §3 cross-field PASS (fruit band [5,9] strictly inside survival [4,9]; ph nesting; self_fertile + the J.H. Hale exception consistent across pollinator_notes/pollination.notes/blossom tip/no-fruit diagnostic); (11) the verbatim scan + the perennial cert-gate + the flip.
- **Verbatim scan (the flip gate):** fetched 23 cited URLs (17 text-comparable; 6 PDFs/403s stated). 2 HARD hits, both brown-rot strings echoing the Clemson peach-diseases factsheet -> **2 surgical rewords, Trevor-approved** (`diseases[1].symptoms_beginner` "wilt and turn brown"->"go limp and brown"; `cause_seasoned` "(on the tree and on the ground)"->"whether still hanging in the canopy or fallen below") -> re-scan **0 HARD hits**. The 11 borderline (6-7 word) are benign-class (Latin binomials, "1 cup of 10-10-10", generic instructions).
- **NEW perennial cert-gate branch (Claude Code, test-first):** `tools/perennial_gate.py` (`perennial_cert_violations`) + `test_perennial_gate.py` (8 fixtures), wired into `whole_crop_gate.py` as section A3. Enforces the tree invariants the generic gate did not: exactly ONE `track:"perennial"` establishment entry/region (no succession/start_indoors), the suitability enum, and the **no-fruit DIRECTION SPLIT** (survives_no_fruit carries a calendar IFF `chill_delivered[0] >= min variety chill (400)`; unsuitable empty). No-op for annuals (the 4 anchors confirm). peach = 0 violations.
- **The flip:** `verification_status` -> `verified_gs_arc` (phase `phase_3_peach_gold_standard_arc`, 18-source set, launch_ready_core+seasoned True, `last_audited:2026-06-11`, one DEFERRED non-blocking `open_finding` = the rotation perennial-shape); top-level `last_reviewed`/`last_reviewed_session` set; the vestigial `growth_stages_year_one/_annual` nulled to match the certified crops. Gates: whole_crop_gate peach PASS(0); register PASS; release_verify clean (only peach, no catalog change, lettuce byte-identical, the 10 benign region-key concerns); 4 anchors PASS. Promoted `7345b944`.

## Active work + next step
- **NEXT = apple (anchor 6, the first COMPRESSED tree-repeat).** Apple rides peach's rails -- the tree region model, the perennial cert-gate, the build_region_shells tree branch all exist; NO structural redesign. The goal: run the full arc in 1-2 passes (not peach's 7) to test the **2-3 anchors/day** target. I'll pre-stage the apple kickoff. (Apple also gives the pome data point that unblocks FLAG 1, the rootstock `selection_basis` enum, and the perennial-aware `rotation` shape.)
- **A separate TRACK (not gating the anchor count): the tree GUIDE PAGE on the site.** Net-new UI (hardiness band + chill block + per-variety bloom Gantt + the dormant-prune calendar + cross-pollination -- the apple-zone-6.html mock is the design; the current plant-astro template is annual-only). Best sequenced AFTER ~2 tree anchors certify so it renders more than peach.
- **Fold into apple (the deferred tree tidy):** the perennial-aware `rotation` shape (peach's open_finding); `_build_tree_shells` setting region_id/label/zone_span + sweeping stray keys (so apple's shells come out clean); Appendix A registration of the growth_stages `timing_*`/`year_phase` stems.
- **PARKED:** FLAG C (`usda_phzm`); WeatherKit; USCRN; C1/C3 vocab; soil `_seasoned` back-fill; evergreen/citrus `calendar_basis` -> lemon. (PK cleanup -- DONE by Trevor.)

## Gate record (generated 2026-06-11, on canonical `7345b944`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **5 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails (carry into apple + every tree/perennial anchor)
- **PERENNIAL CERT-GATE (peach Step 11):** `tools/perennial_gate.py::perennial_cert_violations` enforces, for `calendar_basis==perennial_chill_gated`: exactly ONE `track:"perennial"` establishment plantings entry/region (no succession/second_planting/start_indoors/direct_sow); the 4-value `suitability` enum; the **no-fruit DIRECTION SPLIT** (survives_no_fruit carries a calendar IFF `chill_delivered[0] >= min recommended-variety chill`; unsuitable empty; fruits_reliably/marginal non-empty). Wired into whole_crop_gate as A3; no-op for annuals. Run it on every tree anchor at cert.
- **VERBATIM SCAN = the Step-11 flip gate (Claude Code):** fetch the cited URLs -> `verbatim_scan.py <slug> [path]` (flag `--cache=DIR`; default `/tmp/verbatim_cache`). >=8-word run = HARD (flip-blocking); 6-7 = borderline (binomials / numeric conventions / generic instructions are benign). Reword HARD hits with Trevor (keep the biology, break the run); route to the voice lane, do not self-dismiss.
- **SURVIVES != FRUITS first-class** + the **TREE REGION MODEL** (`tree_region_model_spec_v1_0`): region = "can I grow it + which varieties"; zone = "exactly when"; `calendar_basis=perennial_chill_gated`; render keys REUSE annual names; `dormant` = 14th calendar token. TREE care honesty: `rotation_years:null` (replant-disease angle; perennial-aware shape OWED), `moon_phase.phase:null`, vestigial `growth_stages_year_one/_annual` null, growth_stages `day_range_from_sow:null` + `year_phase`/`timing_*`.
- **PEACH/tree biology:** SELF-FERTILE crop-level BUT J.H. Hale is the exception (consistent everywhere). Chill VARIETY-driven [200,1050]. Rootstocks by soil/nematode tolerance not size (FLAG 1 -> apple).
- **apply_patch numeric-key rule** (RFC-6901 dict-key vs list-index by node type); **slice-integrity** (verify the applied crop hashes to claude.ai's post-apply crop-object SHA -- 3/3 this arc).
- **CANONICAL SHAPES + COMPACT JSON** (`anchoring_urls={id:{url,verified}}`; enum-token soil arrays; `research_backed`/`likely`/`traditional`; `separators=(",",":")`, no trailing newline; gen CURRENT_STATE to temp then `mv`).
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes, catalog mints, the verbatim scan + the flip) + owns SHAPE/naming + renderer. Dataset push autonomous (announce-then-execute); plant-astro Trevor-gated. **Methodology disk is master.**
