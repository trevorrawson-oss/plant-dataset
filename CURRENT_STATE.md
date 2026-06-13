# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel) of a ~18 target. **basil (anchor 9, the FIRST herb, the first return to the annual cadence after four consecutive trees) has ENTERED the arc: Steps 1-3 + 3.5 RELEASED 2026-06-13.** Source set (21 T1) + annual scalars + 2.9 universal fields + biology prose (both registers) + 6 varieties + companions are authored; the 10 annual region shells are built (frost_anchored, succession-capable, northern_tier from-scratch). basil status `in_progress_steps_1_3`, launch_ready False/False. **NEXT = claude.ai Steps 4-5 (warm-region sourcing + per-region biology, both registers, the 10 cells).**

## Canonical pointer
- **Current SHA:** `8318cc03b22bf331b999bd73680886aaeb195ea4aea27eaae6265c92572a358f`. `LATEST.txt` session: `basil_steps_1_3_3_5` (2026-06-13).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus
  - `f1fce747` -- feat(lemon): Step 6B -- the 65 register/care fields (register-complete)

## What just happened (session `basil_steps_1_3_3_5`)
- **basil Steps 1-3 applied** (`a0cc0178` -> `61cd1e92`): 30 edits, ONLY basil changed (lettuce byte-identical; no catalog/top-level delta). Source set = 21 T1 catalog IDs (umass_ext = the downy mildew authority). Annual scalars (days_to_maturity [60,90]/mid 75, germination_temp_f [70,85], spacing_inches [6,12], weeks_indoors 6, start "both"). Full 2.9 UNIVERSAL fields (watering w/ schedule_by_stage + drought_tolerance low + method_note + critical_periods; fertilizer w/ amount; container_notes w/ self_watering; soil; ph [6.0,7.5]) -- both registers. Biology prose both registers: description, harvest_ready, **bolting** (risk high, triggers long_days+heat -- photoperiodic, herb-central), rotation (Lamiaceae, 2yr), **storage** (chilling injury below 50°F -- no refrigeration; the herb-specific story). **pests** 3 (aphids/Japanese beetle/slugs); **diseases** 2 -- **downy mildew** (*Peronospora belbahrii*, oomycete, first US 2007, Rutgers DMR varieties Devotion/Obsession/Prospera) + Fusarium wilt. **varieties** 6 (annual list-of-strings shape). **companions** three-array (basil+tomato = the thrips field-study pairing). **All 7 claude.ai claim paths byte-verified.**
- **TWO register HALTs ruled by Trevor** (the first-herb touchpoint): (a) `container_notes.drainage.saucer_practice` was already ruled CP but authored as a bare string -> **honor the CP ruling**: reshaped to `saucer_practice_seasoned` + null `saucer_practice_beginner` (beginner sibling OWED at Steps 6-8). (b) `sources_summary._note` -> **EXCLUDED** (backend subtree; named backend machinery in checklist §2; synced to `register_completeness_gate.EXCLUDED_PATH_SUBSTR` + inventory §4). `register_completeness_gate` = PASS.
- **basil Step 3.5 region shells built** (`61cd1e92` -> `8318cc03`): 10 annual region cells, `calendar_basis` stays `frost_anchored` (NOT perennial), transplant shape (start_indoors + plant_out + harvest_*, track `beginner`, succession_id), `northern_tier` built FROM-SCRATCH (author-fresh -- no verified `zones{}` to promote), region_notes null (Step 4-8 fill targets). Zero tree-key contamination. ONLY basil changed.
- **Enabling tooling fix** (commit `ac2b096`): `apply_patch` `add` op now tolerates an empty-equivalent shell (`[]`/`{}`/`""`) the way `replace` already does (a populated value still refuses; `base_sha` remains the drift gate). The wiped author-fresh shell types list-scalars as `[]`, so claude.ai's `op:add` hit the old guard. History-replay reproduces 3 prior committed patch SHAs -- no behavior change to any shipped patch. Also excluded the `sources_summary` subtree from the roster gate (HALT b above).

## Active work + next step
- **basil admission gate = 11 violations, ALL expected pending-fill markers** (none structural): 10 `region_notes pair both null` (authored at Steps 4-8) + 1 `dual-voice null sibling: container_notes.drainage.saucer_practice_beginner` (OWED at Steps 6-8). This is the normal Step-3.5 admission end-state (shells shaped, notes/copy pending).
- **NEXT = claude.ai Steps 4-5:** warm-region sourcing + per-region biology, both registers, across the 10 cells. basil is a frost-anchored annual, succession-capable (interval 3wk, up to 4 successions); the limit on both ends is frost (no midsummer heat-pause up north). Verify window structure PER SOURCE (A5); do not lift by analogy.
- **OWED into later steps:** `saucer_practice_beginner` (Steps 6-8 dual-voice pass); `basil_s1_uconn_mint_flag` (mint `uconn_ext` before cert IF the UConn downy mildew URL becomes a primary anchor).
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; 4 certified trees to template from).

## Gate record (generated 2026-06-13, on canonical `8318cc03`)
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
- *(basil: 10 region shells BUILT at Step 3.5, region biology PENDING Steps 4-8 -- not a certified anchor, not listed above.)*

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
- **HERB ARCHETYPE (basil = the first herb; bot-briefing family observations):** bolting is herb-central (a bolting profile is as load-bearing as `days_to_maturity` is for roots; basil = photoperiod+heat); storage **chilling injury** (tender herbs cannot be refrigerated -- do NOT inherit the root-veg "refrigerate X weeks" template); the **foliar-wetness disease nexus** (downy mildew + Fusarium both promoted by overhead watering -> water at base); DMR variety notation is **sweet-basil-specific** (don't template forward); **container-as-frost-mitigation** (move inside before frost). Each herb's disease-resistance variety landscape is derived FRESH.
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells (`[]`/`{}`/`""`) -- author-fresh/bot crops type unpopulated list-scalars as `[]`, so `op:add` must not refuse them (a populated value still refuses; base_sha is the gate). The `sources_summary` subtree is EXCLUDED from register coverage (backend).
- **REGISTER SHAPE:** `saucer_practice` ruled CP (honored, not re-ruled universal). A bare CP prose key in a future patch is the §v1.9.4 bare-key shape bug -- reshape to the `_seasoned`/`_beginner` pair; `register_completeness_gate` catches it (suffix-based ruling).
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven on 2 anchors (lemon cold-only, orange cold+heat):** `perennial_evergreen` + `gating_factors`; cold = `min_winter_temp_f`/`cold_basis_*`; heat = `heat_summer_basis` (`{high|adequate|marginal|insufficient}`, no GDD) + `heat_basis_*`; calendars DERIVED; THREE no-fruit directions (chill Goldilocks / cold monotone / heat FLOOR). Hero verdict: heat `marginal` -> suitability `marginal` (reduced quality NOT failure); `insufficient`+`survives_no_fruit` for true non-sweetening. Ready to replicate to grapefruit.
- **CERT mechanics:** source-verbatim (vs cited URLs) is the flip gate (0 HARD); a SIBLING-CROP echo is a SEPARATE quality call -> route to Trevor (voice lane). `verified`=DATE not true. The cert FLIP = `verification_status` block (status/phase/date/launch_ready x2/last_audited/source_set/verification_log_ref/open_findings) + top-level last_reviewed/_session; open_findings all blocks_launch:false.
- **ANCHORING convention:** pests/diseases anchor via the catalog PORTAL id (`uc_ipm`) + the specific URL, NOT granular sub-ids; a cited source MUST be anchored (gate F); Claude Code reconciles claude.ai's granular drift at apply.
- **DERIVATION (`tree_calendar._months`):** parse ONLY before the first "(" (parenthetical prose carries stray months + "may"; A4 cannot catch a bad-source-date calendar).
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks (dash/enum/SHA/source-count) are advisory -- the gates are the defense.
