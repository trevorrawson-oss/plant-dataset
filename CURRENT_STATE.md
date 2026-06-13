# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel) of a ~18 target. **basil (anchor 9, the FIRST herb) is REGISTER-COMPLETE + gate-clean -- Steps 1-3 + 3.5 + 4-5 + 5C + 5.5 + 6-8 RELEASED 2026-06-13.** All prose surfaces authored in both registers; `whole_crop_gate basil = PASS` (0 violations), `register_fill_gate = PASS`, `register_completeness_gate = PASS`. basil status still `in_progress_steps_1_3`, launch_ready False/False. **NEXT = Step 11 CERT: the verbatim flip gate (fetch + compare basil's prose vs its cited source URLs) + the `launch_ready` x2 + status `verified_gs_arc` flip. basil becomes anchor 9 at the flip.**

## Canonical pointer
- **Current SHA:** `83ed20e5e0f4f99a517bf86aa36d4b5f1c8671bf89d5c3045a4c22ef5b55fc56`. `LATEST.txt` session: `basil_steps_6_8` (2026-06-13).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `48c9580f` -- feat(basil): Steps 5C + 5.5 -- per-zone harvest resolution + derived calendars
  - `954565ee` -- feat(basil): Steps 4-5 -- region layer complete (10 cells + per-arm anchoring)
  - `8318cc03` -- feat(basil): Steps 1-3 + 3.5 -- anchor 9, the first herb
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)

## What just happened (session `basil_steps_6_8`)
- **basil Steps 6-8 (bulk prose) applied** (`48c9580f` -> `83ed20e5`): 19 ops, ONLY basil. Authored the empty compounds (`tips_by_stage` 5 stages, `growth_stages`, `failure_diagnostics`, `notifications`, `weather_triggers`) + the dict-shell stragglers (`yield_expectations`, `moon_phase_preference`, `fertilizer.notify_message`) + the owed `container_notes.drainage.saucer_practice_beginner`, all dual-register. **`register_fill_gate basil` = PASS** (was 8 nulls); whole_crop_gate null_values 0, populated CP 129. Did NOT touch regions/calendars or `launch_ready`.
- **The worklist was COMPUTED, not hand-listed** (v1.9 §3) -- `register_fill_gate` gave the exact 8 null fields, the empty compounds added by sweep. basil's 6-8 was light (its 1-3 authored most biology prose in both registers already).
- **Two register-gate rulings (the 6-8 touchpoint, Trevor):** (a) `region_tip_override_assessment` (a NEW crop-level process attestation: rider assessed -> no override) -> **STRIPPED** (process metadata belongs in STATE_HISTORY, not crop data; consistent with cherry/carrot; structured in-data audit would live in `verification_status`, not a bespoke key). The attestation: care actions (pinch-above-node / base-watering / frost timing / succession) are biologically universal z3-11; warm-region differentiation (FL year-round, HI tropical) is TIMING-ONLY, already in the region cells -> no override. (b) `regions.*.plantings[].year_round_basis` (the hawaii year-round reason, a 5C field) -> **EXCLUDED backend** (`*_basis` evidence, checklist A3; enum-prefixed, never rendered). Gate fix: `register_completeness_gate` now rules bare `*_basis` via the shared `_basis_family` predicate (commit `09b5d51`).
- **Verification:** release_verify CLEAN (only basil; lettuce byte-identical; **violation-diff: CLEARED the saucer_practice_beginner**, no new); whole_crop_gate / register_fill / register_completeness all PASS; 8 certified anchors untouched.

## Active work + next step
- **basil is REGISTER-COMPLETE + gate-clean** (whole_crop_gate PASS, both register gates PASS). The only thing between basil and cert is the verbatim flip gate + the flip.
- **NEXT = Step 11 CERT:**
  - **Verbatim flip gate** (claude.ai lane / fetch step): fetch basil's cited source URLs + run `verbatim_scan` (two-step) -- basil's authored prose vs the cited bodies; 0 HARD lifts is the flip gate. basil is the FIRST herb (no sibling-herb echo concern, unlike orange-vs-lemon).
  - **Step 10 anchoring hygiene** confirm (per-arm anchoring done at 4-5; re-confirm no claim-leaf gap).
  - **The FLIP (Claude Code):** `verification_status` -> status `verified_gs_arc` + phase + `launch_ready_core`/`launch_ready_seasoned` True + last_audited + source_set + verification_log_ref + open_findings (all blocks_launch:false) + top-level `last_reviewed`/`_session`. basil -> anchor 9 (9 of ~18).
- **OWED into cert:** `basil_s1_uconn_mint_flag` (mint `uconn_ext` IF the UConn downy mildew URL is cited as a primary anchor -- check basil's authored diseases/tips for it before the flip).
- **ANNUAL DERIVER -- future extension (not basil):** `annual_calendar.py` scoped to summer-centered frost-anchored cells; winter-wrap/heat-inverted needs a cycle-segmentation extension before retro-ing the certified annuals + wiring `annual_calendar_violations` into the always-on gate.
- **Separate track:** the tree GUIDE PAGE on plant-astro.

## Gate record (generated 2026-06-13, on canonical `83ed20e5`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lemon: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **orange-navel: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- **orange-navel: 10/10 region cells filled**
- *(basil: 10/10 cells + per-arm anchoring + 20 derived calendars + register-complete prose. Not yet certified (status `in_progress`, awaiting the Step 11 flip) -- not listed above.)*

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **orange-navel:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **8 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **PROCESS ATTESTATIONS belong in STATE_HISTORY, not crop data:** a rider/assessment record (e.g. region-tip-override "assessed -> no override") is process metadata -> STATE_HISTORY entry, never a bespoke crop field. Structured in-data audit lives in the `verification_status` subtree. (basil 6-8: `region_tip_override_assessment` stripped.)
- **`*_basis` evidence prose is BACKEND (checklist A3):** bare `*_basis` keys (e.g. `year_round_basis`) are EXCLUDED -- never rendered, dash-exempt, no register suffix; `register_completeness_gate` rules them via `_basis_family`. Register-suffixed `*_basis_seasoned/_beginner` (evergreen cold/heat basis) are CP, caught by the suffix.
- **ANNUAL CALENDAR DERIVATION -- BUILT (`tools/annual_calendar.py`):** computed from resolved per-zone windows, never hand-authored. `cold_pause` anchored at deep winter (January); a Jan-active near-year-round cell has no cold pause (inactive month = `growing` lull); `year_round` -> 12x growing. Reproduces carrot `northern_tier` z5 exactly. Scope = summer-centered frost-anchored; not yet always-on (would false-flag certified annuals' hand-authored calendars).
- **6-8 WORKLIST is a COMPUTED SWEEP (v1.9 §3):** `register_fill_gate` gives the null-register worklist + the empty compounds; the release re-runs it to 0. Never hand-list sections (apple missed 30, peach shipped 46).
- **ANCHORING (basil 4-5):** every `plantings[]` arm anchors to the SPECIFIC verified page (lettuce exemplar = B577 PDF / VH021), never the homepage; nested `{id:{url,verified:DATE}}`.
- **HERB ARCHETYPE (basil = first herb):** heat-LOVING (inverse of lettuce; NO heat_pause, `pause_in_heat:false`); frost-limited both ends; `year_round` for hawaii; bolting herb-central; chilling-injury storage; foliar-wetness disease nexus; DMR notation sweet-basil-specific.
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells; `sources_summary` subtree EXCLUDED; `saucer_practice` ruled CP.
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat).** Heat `heat_summer_basis {high|adequate|marginal|insufficient}`; heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call -> Trevor. The FLIP = `verification_status` block + top-level last_reviewed; open_findings all blocks_launch:false.
- **DERIVATION (`tree_calendar._months`):** parse ONLY before the first "(".
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
