# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel) of a ~18 target. **basil (anchor 9, the FIRST herb) is at Step 11 -- the verbatim flip gate is essentially clean, but THE FLIP IS HELD on one content-accuracy finding.** Steps 1-3 + 3.5 + 4-5 + 5C + 5.5 + 6-8 done; the Step-11 verbatim reword + a citation re-pin released 2026-06-14. basil status still `in_progress_steps_1_3`, launch_ready False/False. **NEXT = resolve the `low_desert_az` source-fidelity finding (re-source the AZ window), then THE FLIP -> basil = anchor 9, the first certified herb.**

## Canonical pointer
- **Current SHA:** `de9f54bfecc6a0e653c5d9ba5d1d4b40304c302f7d85f0752229511514fc7f34`. `LATEST.txt` session: `basil_step11_verbatim` (2026-06-14).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `83ed20e5` -- feat(basil): Steps 6-8 -- bulk prose; register-complete + gate-clean
  - `48c9580f` -- feat(basil): Steps 5C + 5.5 -- per-zone harvest resolution + derived calendars
  - `954565ee` -- feat(basil): Steps 4-5 -- region layer complete (10 cells + per-arm anchoring)
  - `8318cc03` -- feat(basil): Steps 1-3 + 3.5 -- anchor 9, the first herb
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)

## What just happened (session `basil_step11_verbatim`)
- **basil Step 11 verbatim flip gate run** (claude.ai verify lane): 312 user-facing strings vs basil's cited sources (16 of 23 URLs fetched; UConn moot; 4 broken cites = 1 re-pinned + 3 honest NOT-COVERED). **1 HARD lift** (`regions.hawaii_tropical.region_notes_seasoned` reproduced the CTAHR sentence 17 words) -> **REWORDED** to own-voice, facts exact, 0 residual. 8 borderline 6-7w hits, all benign (standard horticultural instructions + a properly-attributed research finding). **Verbatim front is clean.**
- **Applied the verbatim patch** (`83ed20e5` -> `de9f54bf`): the hawaii reword + the UMN Japanese-beetle anchoring-URL re-pin (cited URL 404'd; live page verified). 2 ops, only basil; all gates PASS; dash-clean.
- **THE FLIP IS HELD** on one HIGH-severity content-accuracy finding (below). The cert verbatim gate caught it -- exactly its job.

## Active work + next step
- **THE BLOCKER -- `low_desert_az` season unsupported by its sole source.** The cited `uariz_ext` az2061 ("Growing Herbs In Tucson", fetched live at cert) states the Sonoran Desert warm season as **May through mid-September**, but basil's `low_desert_az` cells claim **"April through November"** in BOTH registers with explicit attribution, sole-anchored to az2061. The Steps 4-5 authoring MIS-STATED the source (the 4-5 findings claimed az2061 says "April to November"; the live page does not). A citation-integrity failure -> must fix before cert.
- **NEXT = AZ re-source (claude.ai), then THE FLIP (Claude Code).** Trevor's call: send claude.ai back to re-source `low_desert_az` -- find the UA/T1 source that actually supports the real low-desert basil window + reconcile window/attribution (lean: April-Nov is likely biologically right for irrigated Phoenix-z9 basil but was cited to the wrong bulletin -> find the UA low-desert PLANTING calendar; if none supports beyond az2061's May-mid-Sept, narrow to match). Also fold in: the **hawaii CTAHR URL re-pin** (cited URL is the directory root; real page `/new/fjgi/Garden/pop-basil.htm`, quote confirmed via search). Then Claude Code applies + re-runs verbatim_scan + the gates + **THE FLIP**.
- **OPEN FINDINGS staged for the flip** (all blocks_launch:false EXCEPT the AZ one which blocks until resolved): 3 NOT-COVERED URLs (PSU x2 host-blocked, UMaine 404 no-replacement -- NT co-anchors to UMN), benign verbatim residuals, the RESOLVED uconn flag (moot). See `basil_step11_open_findings.json`.
- **Separate track:** the tree GUIDE PAGE on plant-astro; the annual-deriver full-generality extension (not basil).

## Gate record (generated 2026-06-14, on canonical `de9f54bf`)
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
- *(basil: 10/10 cells + anchoring + 20 calendars + register-complete + verbatim-clean. Flip HELD on the AZ finding -- not yet certified, not listed above.)*

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
- **THE CERT VERBATIM GATE CATCHES SOURCE-FIDELITY, not just lifts:** basil's flip was held when the verbatim run FETCHED az2061 and found `low_desert_az`'s attributed window unsupported by the live source -- a Steps-4-5 mis-statement that every prior gate (structural, register, calendar) passed. Source-claims must be verified against the LIVE source at cert; "the findings said the source says X" is not proof. Re-source, never quick-edit dates.
- **CITATION HYGIENE at cert:** a cited URL must be live + actually contain the claim; re-pin only after fetch+verify (no blind swaps); an unreachable/404 URL with no verified replacement is filed NOT-COVERED (blocks_launch:false), never hidden. (basil: UMN-JB re-pinned; PSU x2 + UMaine NOT-COVERED; hawaii CTAHR re-pin owed.)
- **PROCESS ATTESTATIONS belong in STATE_HISTORY, not crop data** (basil 6-8: `region_tip_override_assessment` stripped). Structured in-data audit lives in `verification_status`.
- **`*_basis` evidence prose is BACKEND (A3):** bare `*_basis` keys (e.g. `year_round_basis`) EXCLUDED via `_basis_family`; register-suffixed `*_basis_seasoned/_beginner` are CP (caught by suffix).
- **ANNUAL CALENDAR DERIVATION -- BUILT (`tools/annual_calendar.py`):** computed from resolved windows; `cold_pause` anchored at deep winter (Jan); Jan-active near-year-round cell -> no cold pause (inactive month = `growing`); `year_round` -> 12x growing. Reproduces carrot NT z5 exactly. Scope = summer-centered frost-anchored; not yet always-on.
- **6-8 WORKLIST is a COMPUTED SWEEP (v1.9):** `register_fill_gate` + empty-compound sweep; the release re-runs to 0. Never hand-list.
- **ANCHORING (basil 4-5):** every `plantings[]` arm anchors to the SPECIFIC verified page (lettuce = B577 PDF / VH021), never the homepage; nested `{id:{url,verified:DATE}}`.
- **HERB ARCHETYPE (basil = first herb):** heat-LOVING (inverse of lettuce; NO heat_pause); frost-limited both ends; `year_round` for hawaii; bolting herb-central; chilling-injury storage; foliar-wetness disease nexus; DMR notation sweet-basil-specific.
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat).** heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call. The FLIP = `verification_status` block + top-level last_reviewed; open_findings all blocks_launch:false.
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
