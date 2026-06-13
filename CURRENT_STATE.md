# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel) of a ~18 target. **basil (anchor 9, the FIRST herb) is mid-arc: its REGION LAYER is now COMPLETE -- Steps 1-3 + 3.5 + 4-5 RELEASED 2026-06-13.** All 10 region cells carry warm-season windows + per-zone dates + dual-register region_notes + per-arm anchoring (specific verified URLs); the heat-loving annual model held (A6 cleared, NO heat_pause). basil status `in_progress_steps_1_3`, launch_ready False/False. **NEXT = Step 5.5: derive the per-zone `calendar[]` arrays from the windows (build the annual calendar deriver -- none exists yet), then Steps 6-8 bulk prose, then cert.**

## Canonical pointer
- **Current SHA:** `954565ee4bb743c25835629dcac2f0b16b9bf042fb4a819943afdf9ef9c3d3bb`. `LATEST.txt` session: `basil_steps_4_5` (2026-06-13).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `8318cc03` -- feat(basil): Steps 1-3 + 3.5 -- anchor 9, the first herb
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `670f14fa` -- feat(lemon): CERTIFIED -- anchor 7, the FIRST evergreen / first citrus

## What just happened (session `basil_steps_4_5`)
- **basil Steps 4-5 (amended) applied** (`8318cc03` -> `954565ee`): 131 ops, ONLY basil changed (lettuce byte-identical; 0 catalog/top-level delta). **All 10 region cells now filled** with warm-season `plantings[]` windows (transplant + succession arms) + per-zone `plant_out`/`harvest` dates + `region_notes` both registers + **per-arm `anchoring_urls` (82 arms, SPECIFIC verified URLs, not publisher homepages)**.
- **The 2 deferred cells authored:** `low_desert_az` (z9, `uariz_ext` az2061 -- warm-season annual Apr-Nov in the Sonoran Desert, single arm, shade-cloth = care not a pause) + `hawaii_tropical` (z11, `uhawaii_ctahr` -- `year_round` below 700 ft, continuous, the prime pauseless cell). **`uariz_ext` + `uhawaii_ctahr` admitted to `sources_summary.primary[]`** (Trevor-approved 2026-06-13; both already T1-cataloged).
- **A6 cleared:** NO `heat_pause` anywhere (basil heat-loving; UA az2061 manages desert summer with shade cloth, not a pause). The inverted-from-lettuce model held end-to-end.
- **Two-pass release:** pass-1 (windows) was HELD -- it lacked per-arm anchoring (homepage URLs on some arms) + the 2 cells. The amended pass fixed both; Claude Code swept 5 cells' vestigial empty `sources_pending_admission` residue.
- **Calendars NOT derived yet** -- there is no annual calendar-derivation tool (only `tree_calendar.py`); deferred to a focused Step 5.5 (build the deriver test-first).
- **Verification:** release_verify CLEAN (only basil; lettuce byte-identical; dash/temp 0; all arms anchored; no homepage URLs; no `heat_pause`; year_round on hawaii). whole_crop_gate = **1 violation** (the carried `saucer_practice_beginner` null sibling); **no NEW violations** (10 region_notes-null CLEARED). All 8 certified anchors untouched.

## Active work + next step
- **basil region layer COMPLETE (10/10 cells: windows + dates + region_notes + per-arm anchoring).** Gate = 1 (the owed `saucer_practice_beginner`, Steps 6-8).
- **NEXT = Step 5.5 -- derive every cell's `calendar[]` from its windows.** No annual deriver exists (only the tree one). BUILD it test-first: the annual analog of `tree_calendar` -- map each zone's `plant_out`/`harvest` windows + declared pauses to the 12-month token array (precedence pause > plant > harvest > growing > wait; `cold_pause` winter where cool; `year_round:true` -> continuous, no frost offset for hawaii). Then run it on basil's 10 cells, gate calendar coherence, release. The deriver is reusable for every annual + the bot pipeline.
- **Then Steps 6-8** (seasoned depth + beginner siblings incl. the owed `saucer_practice_beginner` + dual-voice coverage), **then Step 11 cert.**
- **OWED:** `saucer_practice_beginner` (Steps 6-8); `basil_s1_uconn_mint_flag` (mint `uconn_ext` before cert IF the UConn downy mildew URL becomes a primary anchor).
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; 4 certified trees to template from).

## Gate record (generated 2026-06-13, on canonical `954565ee`)
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
- *(basil: 10/10 region cells filled WITH windows + anchoring at Steps 4-5; `calendar[]` arrays PENDING Step 5.5. Not a certified anchor, not listed above.)*

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
- **ANNUAL CALENDAR DERIVATION -- OWED TOOL (basil Step 5.5):** there is NO annual `calendar[]` deriver yet (only `tree_calendar.py`). Build the annual analog test-first: zone windows + pauses -> 12-month tokens (precedence pause > plant > harvest > growing > wait); `year_round:true` cells are continuous. Per v1.9 "compute, never hand-author"; reusable for every annual + the bots.
- **ANCHORING (reaffirmed at basil 4-5):** every `plantings[]` window arm anchors to the SPECIFIC verified page (the lettuce exemplar = the B577 PDF / VH021), NEVER the publisher homepage; nested `{id:{url,verified:DATE}}`. claude.ai drifting to homepages is reconciled at release. A cited source MUST be anchored (gate F).
- **HERB ARCHETYPE (basil = first herb):** heat-LOVING (inverse of lettuce -- summer is peak, NO heat_pause, `pause_in_heat:false`); frost-limited both ends; `year_round:true` for frost-free hawaii; bolting herb-central; chilling-injury storage (no root-veg "refrigerate X weeks"); foliar-wetness disease nexus; DMR notation sweet-basil-specific (derive each herb fresh).
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells (`[]`/`{}`/`""`); `sources_summary` subtree EXCLUDED from register coverage. `saucer_practice` ruled CP (a bare CP prose key = the §v1.9.4 shape bug, reshape to `_seasoned`/`_beginner`).
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat):** `perennial_evergreen` + `gating_factors`; heat `heat_summer_basis {high|adequate|marginal|insufficient}`; THREE no-fruit directions; heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call -> Trevor. The cert FLIP = `verification_status` block + top-level last_reviewed; open_findings all blocks_launch:false.
- **ANCHORING convention (pests/diseases):** via the catalog PORTAL id (`uc_ipm`) + the specific URL, NOT granular sub-ids; Claude Code reconciles claude.ai's granular drift at apply.
- **DERIVATION (`tree_calendar._months`):** parse ONLY before the first "(" (parenthetical prose carries stray months + "may").
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
