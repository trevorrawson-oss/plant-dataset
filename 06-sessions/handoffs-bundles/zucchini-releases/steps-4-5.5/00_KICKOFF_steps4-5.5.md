# KICKOFF -- Zucchini / Courgette Steps 4-5.5 (region windows + verification + calendars/succession)

You are picking up **zucchini-courgette** mid-arc. Steps 1-3 (sources / scalars / biology / varieties /
companions / `succession_policy`) and Step 3.5 (region shells, Claude Code) are DONE and released. Your lane
is the **sourced region biology that fills the 10 region shells**: **Step 4 (warm-region window sourcing) ->
Step 5 (side-by-side verification) -> Step 5.5 (planting + succession calendars)**. This is a **rail-rider**:
a `warm_season_fruiting` annual + succession crop on the proven rails (NO new archetype/tooling/design spec).
Same arc shape as **green-beans-bush** (the most recent warm-season succession rail-rider) and **cherry-tomato**
(the archetype exemplar). `lettuce-leaf` is the reference GS crop for SHAPE -- do NOT reshape it.

Operating model unchanged: you AUTHOR (windows + verification + calendar derivation), Claude Code RELEASES
(gates + the A8 `successions_realized` derivation + promote). Don't invent a window with no T1 page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame assembled by Claude Code; the final prompt is yours.
> **SCOPE: Steps 4-5.5 ONLY.** Consumer prose + compounds (`region_notes_*`, `description_*`, `growth_stages`,
> `pests`, `diseases`, `tips_by_stage`, `yield`, `storage`, watering/fertilizer prose) are the NEXT kickoff
> (Steps 6-8). The cert flip is Step 11 (Claude Code). Do NOT author 6-8 surfaces here.

---

## 0. Preflight (Step 0) -- do first, STOP on mismatch
- `shasum -a 256 ~/plant-dataset/crops_data_final.json` MUST equal `LATEST.txt` == `2a47731a43c4f5e35187ba0e7f81290e91d095175f677e7b8d09e3c452f644af`. Mismatch => STOP and reconcile.
- Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `23a7977f…`.
- Read, in order: `CURRENT_STATE.md` + `STATE_HISTORY.md` (the two newest entries are this crop's Steps 1-3 release + the Step 3.5 shell build); the **v2.0 checklist** (`05-methodology/current/gold_standard_arc_checklist_v2_0.md`) Steps 4 / 5 / 5.5; the `second_planting` spec (`docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`) and its v1.1 succession-geometry amendment.
- **Re-derive your arc position from the checklist, not from this prose.** This kickoff SUMMARIZES; the checklist + the live crop are authority. (Standing lesson: a prior kickoff conflated "a slice is done" with "the arc is done.")

## 1. Files (the bundle)
**Upload:** this doc; `zucchini-courgette_current_slice.json` (the post-3.5 base -- region shells built, windows EMPTY); `SLICE_INTEGRITY.md`; **`zone_frost_data.json`** (REQUIRED -- reconcile every resolved window's `resolved_from` to THESE frost dates, never remembered ones); `zucchini_sources_and_catalog.json` (the 122-parent catalog + zucchini's `sources_summary` + `region_source_map`, the per-region anchor candidates -- reuse parents, mint specific-page sub-ids under a trusted parent); `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`.
**Project knowledge:** the v2.0 checklist is already loaded; zucchini needs NO design spec (standard warm-season annual). Skip the PK step.

## 2. Where zucchini is + what these steps own
Steps 1-3 + 3.5 are DONE. The 10 region cells carry the **transplant-shape RULE skeleton** Step 3.5 built: each region's `plantings[0]` = `{succession_id:1, label:"main", track:"beginner", start_indoors:[], plant_out:[], harvest_start:[], harvest_end:[], anchoring_urls:{}}`; `region_notes_*` null; `resolved_by_zone` cells PENDING (empty). `calendar_basis` = `frost_anchored`. The shape is fixed -- you fill VALUES into it.

Steps 4-5.5 DELIVER: sourced region windows -> verified -> `resolved_by_zone` materialized + `calendar[12]` derived + succession geometry encoded + per-arm anchoring + the Step-4 region-tip-override rider. They do NOT deliver `region_notes_*` prose or any compound (those are Steps 6-8).

## 3. Zucchini's region biology (what you are sourcing)
- **Direct-sow-DOMINANT.** Cucurbits resent root disturbance, so squash is usually **direct-sown** after the last spring frost once soil is past 60°F (ideally 70°F); transplants (started ~3 weeks early) are used only to gain time in **short-season** zones. The 3.5 shell is the transplant shape (`start_indoors` + `plant_out`) because `start_method.start == "both"` -- so use `plant_out` as the **after-frost direct-sow / set-out window** in every region, and populate `start_indoors` ONLY where a region genuinely uses the transplant-for-an-early-crop option (the short-season cold end). Source which leads per region.
- **HEAT-LOVING -- the off-season is WINTER, not summer (the contrast to lettuce/carrot).** The season runs last-spring-frost -> first-fall-frost; the frost-killed winter is the limiter at both ends. **NO mid-season heat pause UNLESS a T1 source documents a real desert fruit-set / production STALL** (checklist A5 + the desert-heat-stall rule: no T1 stall = NO `heat_pause`; express peak heat as a planting-window edge instead). The frost-free **z11 hawaii_tropical** cell = `year_round` (CLIMATE-derived; state it honestly in `calendar_basis`/the cell, NEVER a fabricated `source_quote`; it becomes a `blocks_launch:false` open finding at cert).
- **SUCCESSION (the rail-rider feature).** `succession_policy` is `suitable:true`, `window_type:continuous`, **`pause_in_heat:false`** (heat-loving -- the fall succession is squash-vine-borer / powdery-mildew-driven, NOT a heat pause; the green-beans contrast to carrot). So most regions carry a **CONTINUOUS** planting window; only a region with a real **mid-summer gap** (a desert region, IF T1-sourced) splits into spring + fall.

## 4. Step 4 -- warm-region window sourcing (all 10 regions, AUTHOR-FRESH)
Source verified region-appropriate windows from T1 into the shells. **AUTHOR-FRESH: there is NO legacy `zones{}` to de-multiplex** (unlike the retro cherry/beefsteak arc) -- every region, including `northern_tier`, is sourced FROM SCRATCH. Reuse catalog parents; mint specific-page sub-ids under a trusted parent, anchored to the exact page; consult `region_source_map.regions` for the per-region anchor candidates.
- **Per region's `plantings[]` rule arm:** the `plant_out` (after-frost sow/set) window + `harvest_start` / `harvest_end`, plus `start_indoors` where the transplant-early option applies; as `offset_days`-from-frost OR explicit dates; **>= 4 T1** (UX policy) + per-arm `anchoring_urls`. **Verify window STRUCTURE per source** -- one-window (continuous summer) vs two-window (spring + fall) is a SOURCE finding, never a default (checklist A5). Two-window display strings use a COMMA separator.
- **`resolved_by_zone`:** materialize each zone's resolved window strings + `resolved_from: {last_frost, first_frost}` reconciled to **`zone_frost_data.json`** (the manual frost-reconcile -- a cell resolved from remembered frost dates is internally coherent but WRONG). `resolution_method` set (e.g. `static_precompute` for warm cells; the resolved layer carries no rule structure).
- **`region_label`:** the **COLON** convention (`California: Interior Valleys`, `Southeast: Gulf & Coastal Plain`), conforming to lettuce-leaf's labels. NEVER ` -- ` (a gate-C user-facing dash).
- **Region-tip overrides (the Step-4 rider):** author a dual-register override ONLY where >= 2 T1 sources from different regions prescribe a DIFFERENT grower action for a tip (tips only -- `tips_by_stage` / `succession_policy.tip_*`; pests / `sunlight` out of scope). Record the one-line per-crop attestation (the Step-4 gate wants: attestation present AND 0 PENDING/placeholder overrides). If no fork, none are owed.
- **`northern_tier`** is author-fresh (built from scratch at 3.5 -- nothing to promote), so source it like any region: the short-season zones 3-7 with the direct-sow-after-last-frost window and (where used) the transplant-early lead.

## 5. Step 5 -- verification (side-by-side, OWN-source)
Every window value verified **side-by-side against its OWN T1 source** -- the A1 rule: "matches the exemplar" / "same as lettuce" is NEVER a valid justification; where a value converges with another crop's, justify it by zucchini's own source and state why it converges. Status does NOT inherit; only Step 5's side-by-side confers it. Run the 4-round side-by-side on each claim incl. every region window. Repair any null-URL anchor you cite.

## 6. Step 5.5 -- planting + succession calendars (the coherence step)
Derive each resolved cell's **`calendar[12]`** from its windows + declared pauses (precedence: pause > plant > harvest > growing). Token vocab for a `frost_anchored` annual: `plant` / `growing` / `harvest` + `cold_pause` / `heat_pause` / `season_over`.
- **OFF-SEASON TOKEN = `cold_pause`, NEVER `wait`** for the frost-killed WINTER off-season (the green-beans lesson -- `wait` is the ILLEGIBLE token 5.5 exists to resolve; it is NOT a valid resting state for a populated calendar). The frost-free **z11 hawaii** cell = `year_round` (no `cold_pause`). A frost-free region with a bounded heat / off season uses `season_over`.
- **SUCCESSION GEOMETRY (mixed, keyed PER-REGION by continuous-vs-split, NOT warm-vs-cold)** -- the proven green-beans inverse-of-carrot pattern (second_planting spec v1.1 §4): a **continuous** region window -> `succession_continuous` (derived from `first_plant_date`/`last_plant_date`); a **split** region (a real mid-summer gap) -> `succession_spring` / `succession_fall` comma-lists. Each region carries only the geometry it actually is.
- **DO NOT author per-zone `successions_realized` counts.** Claude Code DERIVES them at release (`tools/derive_realized_successions.py`, gated at whole_crop_gate **A8**: year_round -> `min(floor(52/interval_weeks),12)`; authored spring/fall lists -> count; else day-precise `[first_plant_date,last_plant_date]` split at internal pauses). You author the WINDOWS + GEOMETRY; CC derives + reconciles the integers (and reconciles `succession_policy.successions` to max-over-zones). GLOBAL cap 12.

## 7. Copy + sourcing rules
T1 only (university-extension vegetable guides; seed-company / almanac = T2, evidence-log only, never a dataset citation). The user-facing strings you DO touch at 4-5.5 are the resolved window/display strings + region labels + any region-tip override: **no em dashes / no `--`; `°F` symbol (never "degrees F"); American English; "zucchini" / "squash" lowercase.** Backend prose (`*_basis`, `synthesis_note_*`, `source_quote`, provenance) MAY spell "degrees F." `region_notes_*` and all consumer prose stay NULL here (Steps 6-8).

## 8. Deliverable
Hand back the authored slice (or a patch) + the post-author crop SHA + per-region source-mint flags + the region-tip-override attestation + a note of any window-structure finding (one-vs-two windows per region) or any cut/demoted claim. Claude Code preflights vs `LATEST.txt` (`2a47731a`), applies, runs `whole_crop_gate` + the **A8 `successions_realized`** derivation + `register_completeness` + `register_fill` + `release_verify` (the frost-reconcile + the `cold_pause`-not-`wait` release check + the own-source check-G scan), and promotes. Then the **Steps 6-8 kickoff** (consumer prose + compounds: `region_notes_*`, `description_*`, the fertilizer block on the MODERATE-feeder profile recorded in the Steps 1-3 findings, `growth_stages` / `tips_by_stage`, pests = squash vine borer / squash bug / cucumber beetle, disease = powdery mildew / bacterial wilt, `yield` / `storage` / watering prose) -> Step 9 (dash/temp sweep) -> Step 11 cert.
