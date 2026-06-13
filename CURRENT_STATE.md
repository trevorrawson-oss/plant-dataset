# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**8 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel) of a ~18 target. **basil (anchor 9, the FIRST herb) is mid-arc: its REGION LAYER is fully resolved + CALENDARED -- Steps 1-3 + 3.5 + 4-5 + 5C + 5.5 RELEASED 2026-06-13.** All 10 region cells carry windows + per-zone dates + per-arm anchoring + dual-register region_notes + a DERIVED 12-month `calendar[]`. basil status `in_progress_steps_1_3`, launch_ready False/False. **NEXT = Steps 6-8 (seasoned depth + beginner siblings incl. the owed `saucer_practice_beginner` + dual-voice coverage), then Step 11 cert.**

## Canonical pointer
- **Current SHA:** `48c9580fcfb80c1193bffc6a8a551dbedbcbd7b4980f014b7bc417212d273baf`. `LATEST.txt` session: `basil_5c_5_5` (2026-06-13).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `954565ee` -- feat(basil): Steps 4-5 -- region layer complete (10 cells + per-arm anchoring)
  - `8318cc03` -- feat(basil): Steps 1-3 + 3.5 -- anchor 9, the first herb
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop
  - `7b2f8179` -- feat(orange-navel): Step 6 -- 6 biology surfaces + 79 register/care fields (whole_crop_gate PASS)
  - `32b0c6e7` -- feat(orange-navel): Steps 4-5 -- the evergreen+heat region biology (10 cells live)
  - `dee5de3a` -- feat(orange-navel): Step 3.5 -- the heat-accumulation gate + evergreen region shells (test-first)
  - `43f2f44f` -- feat(orange-navel): Steps 1-3 -- anchor 8, the SECOND evergreen / the HEAT-gate crop

## What just happened (session `basil_5c_5_5`)
- **Step 5C (claude.ai transcription) applied** (`954565ee` -> intermediate): the 15 warm cells were carrying ONLY `plant_out`; 5C transcribed their per-zone `harvest`/`harvest_start`/`harvest_end` + `start_indoors` + plant dates + `planting_note` from the Steps 4-5 findings (101 ops, no new sourcing). The region layer is now fully resolved per zone (matches the certified-annual cell shape).
- **Step 5.5 (Claude Code) -- calendars DERIVED, not hand-authored.** Built `tools/annual_calendar.py` (the annual analog of `tree_calendar`, test-first) and derived all **20 region-cell `calendar[]` arrays** from the resolved windows. `annual_calendar_violations(basil)` = 0 (stored == re-derived by construction); release_verify C = "all filled calendars coherent (no waits; heat_pause aligned)."
- **Deriver fix surfaced by basil:** South FL `fl_peninsula z11` is near-year-round (harvest wraps Oct->Jan). The first cut marked its Jul/Aug summer lull `cold_pause` (absurd); fixed by anchoring `cold_pause` at deep winter (January) -- a January-active cell has no winter off-season, so an inactive month is `growing`. Reproduces carrot `northern_tier` z5 unchanged. `hawaii_tropical` = `year_round` -> 12x `growing`.
- **Verification:** release_verify CLEAN (only basil; lettuce byte-identical; dash/temp 0; calendars coherent); whole_crop_gate = **1 violation** (the carried `saucer_practice_beginner`); **no NEW violations**; 8 certified anchors untouched. Commits: deriver `dfbd27c`, fl-z11 fix `15076e7`, data `[this]`.

## Active work + next step
- **basil region layer COMPLETE + CALENDARED (10/10 cells: windows + per-arm anchoring + region_notes + derived calendar).** Gate = 1 (the owed `saucer_practice_beginner`).
- **NEXT = Steps 6-8 (claude.ai):** the bulk dual-register prose pass -- seasoned depth-lift + beginner siblings across every prose surface (sweep ALL null `_seasoned`/`_beginner`, §v1.9.3), INCLUDING the owed `container_notes.drainage.saucer_practice_beginner`. Then dual-voice coverage to 0, then Step 11 cert (register_fill_gate must return 0; verbatim flip gate; the launch_ready x2 + status `verified_gs_arc` flip).
- **OWED:** `saucer_practice_beginner` (Steps 6-8); `basil_s1_uconn_mint_flag` (mint `uconn_ext` before cert IF the UConn downy mildew URL becomes a primary anchor).
- **ANNUAL DERIVER -- future extension (not basil):** `annual_calendar.py` is scoped to summer-centered frost-anchored cells (basil's archetype). Winter-wrapping harvest + lettuce-style heat-inverted two-cool-season cells need a cycle-segmentation extension (17 of carrot's warm cells diverge by design). Build that + retro the certified annuals + wire `annual_calendar_violations` into the always-on gate as its own project before the bots scale.
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; 4 certified trees to template from).

## Gate record (generated 2026-06-13, on canonical `48c9580f`)
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
- *(basil: 10/10 region cells filled + per-arm anchoring + 20 DERIVED calendars (5C+5.5). Not a certified anchor, not listed above.)*

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
- **ANNUAL CALENDAR DERIVATION -- BUILT (`tools/annual_calendar.py`, test-first):** calendars are COMPUTED from resolved per-zone windows, never hand-authored (v1.9). Rules: explicit `plant_out` authoritative (plant > harvest in overlap); else direct-sow envelope MINUS harvest; `cold_pause` anchored at deep winter (January) -- a Jan-active near-year-round cell has no cold pause, an inactive month is a `growing` lull; `year_round` -> 12x growing; declared `heat_pause` honored. Reproduces carrot `northern_tier` z5 exactly. SCOPE = summer-centered frost-anchored (basil); NOT yet wired into the always-on gate (would false-flag the certified annuals' hand-authored calendars). `annual_calendar_violations()` ready for the future full-generality + retro pass.
- **PER-ZONE RESOLUTION precedes calendars:** a region cell needs per-zone `harvest` (not just `plant_out`) before its calendar can derive. basil's warm cells were under-resolved at 4-5 (Step 5C transcription gap); the certified annuals carry full per-zone harvest. claude.ai resolves the per-zone windows (its lane); Claude Code derives the calendars.
- **ANCHORING (basil 4-5):** every `plantings[]` window arm anchors to the SPECIFIC verified page (lettuce exemplar = the B577 PDF / VH021), NEVER the publisher homepage; nested `{id:{url,verified:DATE}}`. claude.ai homepage drift reconciled at release.
- **HERB ARCHETYPE (basil = first herb):** heat-LOVING (inverse of lettuce -- summer is peak, NO heat_pause, `pause_in_heat:false`); frost-limited both ends; `year_round` for frost-free hawaii; bolting herb-central; chilling-injury storage; foliar-wetness disease nexus; DMR notation sweet-basil-specific.
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells; `sources_summary` subtree EXCLUDED from register coverage. `saucer_practice` ruled CP (bare CP key = §v1.9.4 shape bug -> reshape to `_seasoned`/`_beginner`).
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat):** `perennial_evergreen` + `gating_factors`; heat `heat_summer_basis {high|adequate|marginal|insufficient}`; THREE no-fruit directions; heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call -> Trevor. The cert FLIP = `verification_status` block + top-level last_reviewed; open_findings all blocks_launch:false.
- **ANCHORING convention (pests/diseases):** via the catalog PORTAL id (`uc_ipm`) + the specific URL; Claude Code reconciles claude.ai's granular drift at apply.
- **DERIVATION (`tree_calendar._months`):** parse ONLY before the first "(".
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
