# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE, re-pin `LATEST.txt`, regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**9 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel, **basil**) of a ~18 target. **BASIL CERTIFIED 2026-06-14 -- anchor 9, the FIRST certified herb / the first `culinary_herb` archetype; the heat-LOVING annual model (inverse of lettuce) proven end-to-end.** **NEXT = anchor 10, a ROADMAP CALL (Trevor): the locked demand-first sequence puts `zinnia` (Flowers) next (the other go-live search-demand crop, annual template), then the indoor/family hubs (microgreens-mix, broccoli, bell-pepper, zucchini-courgette, onion, green-beans-bush) + `blueberry`/`strawberry`.**

## Canonical pointer
- **Current SHA:** `94d647f84ccfbf608d1eb5ac779fb8c11547bcd877f0b31b9058fc0956a249d6`. `LATEST.txt` session: `annual_calendar_coherence_gate` (2026-06-14). *(9 anchors stay certified; this wired the always-on annual calendar coherence gate + normalized the tomato `start_indoors` token defect.)*
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `b5a9229` -- fix(basil): citation hygiene -- remove dead UMaine link, confirm PSU URLs live
  - `30ad063` -- feat(basil): CERTIFIED -- anchor 9, the first herb
  - `de9f54bf` -- feat(basil): Step 11 verbatim reword + JB re-pin (flip HELD on AZ finding)
  - `83ed20e5` -- feat(basil): Steps 6-8 -- bulk prose; register-complete + gate-clean
  - `48c9580f` -- feat(basil): Steps 5C + 5.5 -- per-zone harvest resolution + derived calendars
  - `954565ee` -- feat(basil): Steps 4-5 -- region layer complete (10 cells + per-arm anchoring)
  - `8318cc03` -- feat(basil): Steps 1-3 + 3.5 -- anchor 9, the first herb
  - `a0cc0178` -- feat(orange-navel): CERTIFIED -- anchor 8, the SECOND evergreen / the HEAT-gate crop

## What just happened (session `basil_cert`)
- **BASIL CERTIFIED** (`de9f54bf` -> `c998b1cb`), anchor 9, the FIRST herb. THE FLIP: `verification_status` = status `verified_gs_arc` + phase + `launch_ready_core`/`launch_ready_seasoned` True + last_audited + source_set (20 cited IDs) + verification_log_ref + 6 open_findings (all blocks_launch:false) + top-level `last_reviewed`/`_session`. whole_crop_gate G = flip-state clean, 0 blockers.
- **The AZ blocker RESOLVED via re-sourcing** (the held finding): az2061 ("Growing Herbs In Tucson") is internally self-contradicting on the warm-window dates and its basil row marks spring-only, so it could NOT sole-anchor the "April-November" window. claude.ai re-anchored `low_desert_az` to **az1005** (UA Maricopa County Vegetable Planting Calendar -- already NAMED in the `uariz_ext` catalog entry; its basil row supports spring-through-fall), kept the window (plant_out Apr / harvest May-Oct, now supported), and demoted az2061 to a CARE-only co-anchor via the new sub-ID **`uariz_ext_az2061`** (minted to the catalog; mirrors the `uf_ifas_vh021` precedent). Both registers re-authored, verbatim-clean (max 4-word run vs all 3 live sources).
- **Also:** all 6 hawaii `uhawaii_ctahr` URLs re-pinned off the directory root to the real basil page; the `low_desert_az` calendar re-derived (window unchanged -> reproduced). release_verify clean (only basil + the catalog admit; lettuce byte-identical); register_fill / register_completeness / whole_crop_gate all PASS.
- **The cert verbatim gate earned its keep:** it FETCHED az2061 and caught that the Steps-4-5 authoring mis-stated the source -- a content-accuracy defect that the structural / register / calendar gates all passed.

## Active work + next step
- **basil DONE.** 9 of ~18 anchors certified. The annual archetype set now spans: warm-season fruiting (cherry, beefsteak), root (carrot), cool-season leaf (lettuce), and **heat-loving herb (basil)**; the evergreen+heat tree model is complete (lemon, orange); deciduous trees (peach, apple).
- **NEXT = anchor 10, a ROADMAP CALL (Trevor).** Locked sequence (demand + archetype coverage): **(1) `zinnia`** (Flowers -- the other go-live search-demand crop, annual template, no new UI); then **microgreens-mix** (the never-exercised `non_seasonal_indoor` archetype, needed BEFORE the bots derive); then the family hubs (broccoli, bell-pepper, zucchini-courgette, onion, green-beans-bush) for bot per-family coverage; then `blueberry` (chill-gated, rides peach/apple rails) + `strawberry` (new renovation archetype, do last). Recommended: zinnia next.
- **Citation loose-end CLOSED (2026-06-14):** the UMaine dead-404 link REMOVED from basil (NT z3/z4 retain the live `umn_ext` co-anchor; dropped from source_set, source_set 20 -> 19); PSU x2 (`herbs-in-the-garden`, `fusarium-wilt`) confirmed LIVE via curl (HTTP 403 -- the host WAF blocks automated fetchers, NOT dead pages) -> retained as correct citations, machine-unscannable (benign permanent limitation), findings updated. basil now carries 0 dead citation URLs.
- **ANNUAL CALENDAR DRIFT -- LOOSE END CLOSED (2026-06-14).** The forward-fix is now ENFORCED, not just convention: `whole_crop_gate` section A5 (`annual_coherence_violations`) is wired ALWAYS-ON for every frost_anchored crop. It does NOT re-derive (complex winter-wrap/heat-inverted cells are legitimately hand-authored and a clean deriver would DEGRADE them -- measured: the 75/100 "divergences" are mostly the deriver being too simple, not the calendars being wrong) -- it consistency-checks: HARD on bad length / token-outside-the-enum / heat_pause-object-vs-token mismatch; NOTE on `wait`. The one REAL defect it caught is fixed: cherry + beefsteak mixed `indoors` and `start_indoors` for the same concept, and SuccessionCard renders only `indoors` -> normalized 28 `start_indoors` -> `indoors`. All 9 anchors PASS. Net: new annuals (deriver-computed) AND hand-authored complex cells are now both drift-guarded by the always-on gate. (Residual: 4 cool-coast tomato cells carry a `wait` token -- surfaced as a pause-legibility NOTE, non-blocking; a true between-window gap is legitimate there.)
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; 4 certified trees to template from).

## Gate record (generated 2026-06-14, on canonical `94d647f8`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **basil: `PASS` (0)**
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
- **basil: 10/10 region cells filled**
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- **orange-navel: 10/10 region cells filled**

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **basil:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **orange-navel:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **9 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **HERB ARCHETYPE -- cert-proven on basil (anchor 9):** heat-LOVING (inverse of lettuce -- summer is peak, NO heat_pause, `pause_in_heat:false`); frost-limited both ends; `year_round` for frost-free hawaii; bolting herb-central; chilling-injury storage (no root-veg "refrigerate X weeks"); foliar-wetness disease nexus; DMR variety notation sweet-basil-specific (derive each herb fresh). The template for the other tender heat-loving annual herbs.
- **CERT VERBATIM GATE = SOURCE FIDELITY, not just lifts:** verify source CLAIMS against the LIVE source at cert; a self-contradicting source cannot sole-anchor a window; re-source (re-anchor to a cleaner catalog-named publication + demote the weak one to its supported scope), never quick-edit dates. "The findings said the source says X" is not proof. (basil low_desert_az: az2061 -> az1005 primary + az2061 care co-anchor.) CITATION HYGIENE: re-pin only after fetch+verify; unreachable URLs filed NOT-COVERED (blocks_launch:false), never hidden.
- **ANNUAL CALENDAR DERIVATION + COHERENCE (`tools/annual_calendar.py`):** the DERIVER computes simple summer-centered calendars from resolved windows (explicit plant_out authoritative; direct-sow = envelope minus harvest; `cold_pause` anchored at deep winter; `year_round` -> 12x growing; reproduces carrot NT z5 exactly). It is NOT used to re-derive complex multi-cycle (winter-wrap / heat-inverted) cells -- those are legitimately hand-authored and a clean deriver would degrade them. The always-on enforcement is `annual_coherence_violations` (whole_crop_gate A5): consistency, not re-derivation -- bad length / non-enum token (catches `start_indoors`) / heat_pause-object-vs-token mismatch are HARD; `wait` is a NOTE. So: derive the simple, hand-author the complex, gate BOTH for coherence.
- **PROCESS ATTESTATIONS -> STATE_HISTORY, not crop data** (basil 6-8: `region_tip_override_assessment` stripped). **`*_basis` evidence prose is BACKEND (A3):** bare `*_basis` keys EXCLUDED via `_basis_family`. **6-8 worklist is a COMPUTED SWEEP** (`register_fill_gate` + empty compounds; release re-runs to 0).
- **ANCHORING:** every `plantings[]` arm anchors to the SPECIFIC verified page (lettuce = B577 PDF / VH021), never the homepage; nested `{id:{url,verified:DATE}}`. A split sub-ID (`uariz_ext_az2061`, `uf_ifas_vh021`) scopes a multi-topic publisher to the specific bulletin.
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells; `sources_summary` subtree EXCLUDED.
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat).** heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics / THE FLIP:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call. The FLIP = `verification_status` block (status verified_gs_arc + phase + launch_ready x2 + last_audited + source_set + verification_log_ref + open_findings all blocks_launch:false) + top-level last_reviewed/_session.
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
