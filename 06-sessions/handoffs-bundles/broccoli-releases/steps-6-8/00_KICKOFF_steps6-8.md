# KICKOFF -- Broccoli Steps 6-8 (consumer prose + the 7 compounds)

You are picking up **broccoli** for its FINAL authoring leg before certification. Steps 1-3 (biology / varieties /
companions / succession_policy, PLUS the fertilizer / watering / container / rotation / description / harvest_ready
prose -- broccoli authored more at 1-3 than most), Step 3.5 (region shells), and Steps 4-5.5 (all 10 regions filled:
windows + calendars + succession + the A8 `successions_realized`) are DONE and released. Your lane is **Steps 6-8:
the remaining consumer prose + the 7 compounds**. This is a LEANER leg than zucchini's (much of the prose is already
authored) -- the core of it is the region_notes, storage/yield, and the pest/disease/growth-stage/tip surfaces. When
the gate residual reaches the deferred-zero, broccoli hands back to Claude Code for Step 9 (sweep) + Step 11 (cert).
`lettuce-leaf` is the reference GS crop; the cherry / green-beans seasoned-depth bar is the quality target.

Operating model unchanged: you AUTHOR, Claude Code RELEASES. Don't introduce a claim with no T1 page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame + the COMPUTED worklist assembled by Claude Code; the
> final prompt is yours.
> **SCOPE: Steps 6-8 ONLY.** Region windows/calendars/succession are DONE (Steps 4-5.5) -- do NOT touch them. The
> cert flip (`verification_status`) is Step 11 (Claude Code). Do NOT set it.

---

## 0. Preflight (Step 0) -- do first, STOP on mismatch
- `shasum -a 256 ~/plant-dataset/crops_data_final.json` MUST equal `LATEST.txt` == `78ef87cd1211d15443b7d76ee6f3c9c16da0aba6b7e0d4bf9429659c5052e6d0`. Mismatch => STOP and reconcile.
- Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `a68e13ad…`.
- Read, in order: `CURRENT_STATE.md` + `STATE_HISTORY.md` (the two newest entries are this crop's Steps 4-5.5 release + Step 3.5); the **v2.0 checklist** Steps 6 / 7 / 8 + Appendix A (the auto-derived prose-field denominator) + the dual-register v1.1 five rules. **Re-derive your arc position from the checklist, not this prose.**

## 1. Files (the bundle)
**Upload:** this doc; `broccoli_current_slice.json` (the post-4-5.5 base -- regions FILLED, the 6-8 prose surface NULL); `SLICE_INTEGRITY.md`; `broccoli_sources_and_catalog.json` (the catalog + broccoli's `sources_summary` -- reuse parents, mint specific-page sub-ids under a trusted parent). `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`. (No `zone_frost_data` -- 6-8 is prose; windows are authored.)
**Project knowledge:** the v2.0 checklist + dual-register v1.1 + voice methodology are loaded. No design spec.

## 2. What these steps own (the checklist bars)
- **Step 6 -- Seasoned depth-lift:** every `X_seasoned` prose field meets the cherry seasoned-depth bar (mechanism / regional variation / numeric specificity / honest complexity). **Broccoli authored most of its 1-3 prose fresh to the GS bar, so this is mostly a VERIFY pass** -- lift any field that reads terse; author the NEW 6-8 seasoned fields (region_notes, storage, yield, the compounds). New claims carry T1 backing + anchoring URLs.
- **Step 7 -- Beginner siblings (top-level + dict-sub-field):** the `_beginner` sibling for every top-level / dict CP prose field, derived from the depth-lifted `_seasoned`. Pair only where the divergence is substantive.
- **Step 8 -- Beginner siblings (per-entry on the 7 compounds) + THE DUAL-VOICE COVERAGE GATE:** every `audience:"core"` compound entry has its required `_beginner` siblings; **0 missing keys AND 0 null** across the whole crop (Claude Code re-runs this at release).

## 3. THE COMPUTED WORKLIST (walk the crop -- do NOT hand-enumerate)
**35 register-prose nulls** + **7 empty compounds** + **`container_notes.shape_requirements`** (a CP pair dropped at Steps 1-3, re-author here). Much LESS than zucchini's 78 -- broccoli already authored fertilizer / watering / container-deep-prose / rotation / description / harvest_ready at Steps 1-3 (Step 6 just VERIFIES those at depth).

**Register-prose nulls, by block (each a `_seasoned`/`_beginner` pair unless noted):**
- **`region_notes_*` -- all 10 regions** (northern_tier, se_gulf, ca_interior, ca_north_coast, ca_south_coast, ca_desert, warm_arid, low_desert_az, fl_peninsula, hawaii_tropical): DERIVED from the windows already authored at 4-5.5. Carry the cool-season STRUCTURE: the **spring + fall split** with a midsummer `heat_pause` (interior/temperate), the **cold-zone** single-or-double window bracketed by `cold_pause`, the **frost-free** single cool-season window with summer `season_over`, and the **hawaii** bounded lowland winter window. Note where **fall often out-yields spring** (UMD, mid-Atlantic). 6 split + 4 continuous -- the geometry is in the slice.
- **`storage`** -- `room_temp` / `fridge` / `freezer` / `notes` pairs. Broccoli heads are perishable: best used within a few days, ~1 week in the fridge unwashed in a loose bag, freezes well after blanching florets. (Distinct from a keeper crop.)
- **`yield_expectations`** -- `per_plant` / `peak_production` / `first_year_note` pairs + `factors_seasoned` (single-register list). The main central head THEN the side-shoot secondary harvest (the cut-and-come-again beat -- variety-dependent; De Cicco/Calabrese are side-shoot-heavy).
- **`moon_phase_preference.source_note_seasoned`** -- N/A prose (no-evidence field, like carrot; never null).
- **`container_notes.shape_requirements`** -- author as a REAL dual-voice pair (dropped at 1-3 per the broccoli 1-3 findings): broccoli is a large, top-heavy plant -- a wide, sturdy, deep container; one plant per 5-gal.

## 4. The 7 compounds (Step 8 + A12 rendering-conformance)
Author each with `audience` tags + the dual-register per-entry siblings. **A12 HARD constraint:** `tips_by_stage` is a **dict keyed by `growth_stages[].id`**, each value a LIST of tip objects using **`text_seasoned`/`text_beginner`** (NOT `tip_*`); a tip renders ONLY if its key is a real stage id + the field is `text_*` + the list is non-empty. Define `growth_stages[].id` FIRST, then key `tips_by_stage` + `notifications` to those ids.
- **`growth_stages`** -- the broccoli arc: germination -> seedling -> transplant/establish -> vegetative (leafy frame) -> **heading** (the central head forms -- harvest BEFORE the buds open/yellow) -> **side shoots** (the cut-and-come-again secondary harvest) -> end_of_season. Each: `what_to_look_for` / `user_action` / `log_prompt` (+ `_beginner`). The ids are the load-bearing keys for tips + notifications.
- **`pests`** -- LEAD the **cabbage-worm complex** (imported cabbageworm / cabbage looper / diamondback moth -- the brassica signature; Bt + row cover), then **aphids** (esp. the waxy cabbage aphid in heads), **flea beetles** (seedling shot-holes), **cabbage root maggot** (transplant collars / row cover). Each: `symptoms` / `cause` / `organic_treatment` / `prevention` (+ `_beginner` incl. **`cause_beginner`**).
- **`diseases`** -- LEAD **clubroot** (the soilborne brassica rotation driver -- ties to the `rotation` block already authored; pH + 3-7yr rotation), then **black rot** (the V-lesion bacterial disease; clean seed/transplants), **downy mildew** (cool-wet foliar). Same 4 fields + `cause_beginner`.
- **`failure_diagnostics`** -- the 4-slot template (`label` / `what_happened` / `next_season_tip` + cause): **buttoning** (tiny premature heads from heat / transplant stress / undersized starts -- the signature broccoli failure, ties to `bolting` + the heat thresholds already authored), **bolting** (heat/long-day -> flowering before a head), **no head / loose head** (heat or N imbalance), **hollow stem** (boron / fast growth).
- **`notifications`** + **`weather_triggers`** -- `title` / `body` (+ `_beginner`); machinery carries no sibling. Load-bearing: the harvest-the-head-before-it-opens reminder, the heat-watch (buttoning/bolting) trigger, a frost-protection note (broccoli takes light frost, hard freeze damages heads).

## 5. Block-coherent authoring + anchoring (the cert-ready bot template)
Author each TOUCHED block as a UNIT -- the `_seasoned`/`_beginner` pairs + close its structured nulls + **ANCHOR the block** (`sources` + `anchoring_urls`) in ONE pass. Anchoring is REQUIRED cert work (Step 11), not optional polish. **N/A fields get N/A PROSE, never null.** Surface any beyond-prose change (retro-anchoring, structured nulls closed) as a LABELED sub-section for the release review.

## 6. Copy + sourcing rules
T1 only (seed-company / almanac = T2, evidence-log only). **No em dashes / no `--`; `°F` symbol (never "degrees F"); American English; "broccoli" lowercase.** Backend prose MAY spell "degrees F." CP fields are suffixed siblings (`parent.X_seasoned` / `parent.X_beginner`, never nested).

## 7. Deliverable
Hand back the authored slice (or a patch) + the post-author crop SHA + a LABELED list of any new source mints / retro-anchoring + any N/A-prose ruling. Claude Code preflights vs `LATEST.txt` (`78ef87cd`), applies, runs `whole_crop_gate` (residual -> **0** -- region_notes filled, all 7 compounds populated, dual-voice 0 missing / 0 null, A12 tips rendering-conformant) + `register_completeness` + `register_fill` + `release_verify`, and promotes. Then **Step 9** (whole-crop dash/temp sweep) -> **Step 11 cert** (the independent T1 source-fidelity WebFetch -- which also resolves broccoli's Steps-4-5.5 carry-forwards: F-broc-h11-001 hawaii window, F-broc-warmarid-001 Dona Ana Path-A, the se_gulf z9 heat_pause attestation -- then the flip).
