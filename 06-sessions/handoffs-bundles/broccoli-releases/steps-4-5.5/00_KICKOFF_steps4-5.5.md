# KICKOFF -- Broccoli Steps 4-5.5 (region windows + verification + calendars/succession)

You are picking up **broccoli** mid-arc. Steps 1-3 (sources / scalars / biology / varieties / companions /
`succession_policy`) and Step 3.5 (region shells, Claude Code) are DONE and released. Your lane is the
**sourced region biology that fills the 10 region shells**: **Step 4 (region window sourcing) -> Step 5
(side-by-side verification) -> Step 5.5 (planting + succession calendars)**. This is a **rail-rider**: a
`cool_season_annual` + succession crop on the proven rails (NO new archetype/tooling/design spec). The
reference cool-season exemplars are **lettuce-leaf** (the succession + `heat_pause` model) and **carrot** -- do
NOT reshape them. zucchini is the PARALLEL session (a warm-season rail-rider); broccoli is its cool-season inverse.

Operating model unchanged: you AUTHOR (windows + verification + calendar derivation), Claude Code RELEASES
(gates + the A8 `successions_realized` derivation + promote). Don't invent a window with no T1 page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame assembled by Claude Code; the final prompt is yours.
> **SCOPE: Steps 4-5.5 ONLY.** Consumer prose + compounds (`region_notes_*`, `description_*`, `growth_stages`,
> `pests`, `diseases`, `tips_by_stage`, `storage`, `yield`, `container_notes.shape_requirements`) are the NEXT
> kickoff (Steps 6-8). The cert flip is Step 11 (Claude Code). Do NOT author 6-8 surfaces here.
> **PARALLEL:** zucchini Steps 4-5.5 is authored in a separate session against its own base. Independent slices.

---

## 0. Preflight (Step 0) -- do first, STOP on mismatch
- `shasum -a 256 ~/plant-dataset/crops_data_final.json` MUST equal `LATEST.txt` == `20a3422398414260790f43984ab529c56986be8d39b3e23cae660e49851a698e`. Mismatch => STOP and reconcile.
- Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `04698276…`.
- Read, in order: `CURRENT_STATE.md` + `STATE_HISTORY.md` (the newest entries are this crop's Steps 1-3 release + the Step 3.5 shell build); the **v2.0 checklist** Steps 4 / 5 / 5.5; the `second_planting` spec + its v1.1 succession-geometry amendment. **Re-derive your arc position from the checklist, not this prose.**

## 1. Files (the bundle)
**Upload:** this doc; `broccoli_current_slice.json` (the post-3.5 base -- region shells built, windows EMPTY); `SLICE_INTEGRITY.md`; **`zone_frost_data.json`** (REQUIRED -- reconcile every resolved window's `resolved_from` to THESE frost dates, never remembered ones); `broccoli_sources_and_catalog.json` (the 122-parent catalog + broccoli's `sources_summary` + `region_source_map`, the per-region anchor candidates -- reuse parents, mint specific-page sub-ids under a trusted parent); `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`.
**Project knowledge:** the v2.0 checklist is already loaded; broccoli needs NO design spec. Skip the PK step.

## 2. Where broccoli is + what these steps own
Steps 1-3 + 3.5 are DONE. The 10 region cells carry the **transplant-shape RULE skeleton** Step 3.5 built: each region's `plantings[0]` = `{succession_id:1, label:"main", track:"beginner", start_indoors:[], plant_out:[], harvest_start:[], harvest_end:[], anchoring_urls:{}}`; `region_notes_*` null; `resolved_by_zone` cells PENDING. `calendar_basis` = `frost_anchored`. The shape is fixed -- you fill VALUES into it.

Steps 4-5.5 DELIVER: sourced region windows -> verified -> `resolved_by_zone` materialized + `calendar[12]` derived + succession geometry encoded + per-arm anchoring + the Step-4 region-tip-override rider. They do NOT deliver `region_notes_*` prose or any compound (Steps 6-8).

## 3. Broccoli's region biology (what you are sourcing) -- the COOL-season inverse of zucchini
- **HEAT IS THE ENEMY (the defining cool-season rail difference).** Broccoli is grown in the COOL shoulders; it BOLTS / "buttons" (forms tiny premature heads) in heat -- crown formation stalls above roughly **86°F day / 77°F night** (UMN/ISU). So in most regions it is a **SPRING crop that must mature before summer heat + a FALL crop planted as the heat breaks**, with a **mid-summer NO-GROW GAP**. This is the lettuce/carrot pattern and the INVERSE of the warm-season rail-riders.
- **TRANSPLANT-LED.** Spring: start indoors ~4-6 weeks ahead, set out before heat. Fall: direct-sow or transplant in mid-to-late summer for a fall harvest. `start_method.start == "both"` (the 3.5 shells are the transplant shape: `start_indoors` + `plant_out`). Source per region whether spring is transplant-led and whether fall is direct or transplant.
- **`succession_policy.pause_in_heat` is TRUE** -- so warm/temperate regions carry a mid-summer **`heat_pause`** in the derived calendar (the lettuce model), and the season SPLITS into spring + fall windows.
- **Warm / low-frost regions grow broccoli in the COOL season, NOT year-round.** In the hot-summer South / Florida / desert, broccoli is a FALL-WINTER-SPRING crop; the hot months are the off-season, NOT a growing window. **`hawaii_tropical` (frost-free z11) is NOT `year_round` for broccoli** (the inverse of a heat-lover) -- it grows in the cool months only, if at all; source the real window (it may be a narrow winter window or genuinely marginal). **Cool maritime regions (`ca_north_coast`) can grow it through a long cool season** -- source the actual span.

## 4. Step 4 -- region window sourcing (all 10 regions, AUTHOR-FRESH)
Source verified region-appropriate windows from T1 into the shells. **AUTHOR-FRESH: there is NO legacy `zones{}` to de-multiplex** -- every region, including `northern_tier`, is sourced FROM SCRATCH. Reuse catalog parents; mint specific-page sub-ids under a trusted parent, anchored to the exact page; consult `region_source_map.regions` for the per-region anchor candidates.
- **Per region's `plantings[]` rule arm(s):** the spring arm (`start_indoors` + `plant_out` + `harvest_start`/`harvest_end`) and, where a fall crop is grown, a SECOND window -- as `offset_days`-from-frost OR explicit dates; **>= 4 T1** + per-arm `anchoring_urls`. **Verify window STRUCTURE per source** -- one-window (a single cool season) vs two-window (spring + fall around a summer gap) is a SOURCE finding, never a default (checklist A5). Two-window display strings use a COMMA separator.
- **`resolved_by_zone`:** materialize each zone's resolved window strings + `resolved_from: {last_frost, first_frost}` reconciled to **`zone_frost_data.json`** (the manual frost-reconcile). `resolution_method` set.
- **`region_label`:** the **COLON** convention (`California: North Coast`, `Southeast: Gulf & Coastal Plain`), conforming to lettuce-leaf's labels. NEVER ` -- `.
- **Region-tip overrides (the Step-4 rider):** author a dual-register override ONLY where >= 2 T1 sources from different regions prescribe a DIFFERENT grower action (tips only). Record the one-line attestation (the gate wants: attestation present AND 0 PENDING/placeholder overrides). If no fork, none owed.
- **`northern_tier`** is author-fresh, so source it like any region: the short-season zones 3-7 spring transplant window + (where the season allows) a fall window.

## 5. Step 5 -- verification (side-by-side, OWN-source)
Every window value verified **side-by-side against its OWN T1 source** -- the A1 rule: "matches lettuce/carrot" is NEVER a valid justification; where a value converges, justify it by broccoli's own source and state why. Status does NOT inherit. Run the 4-round side-by-side on each claim incl. every region window; repair any null-URL anchor you cite.

## 6. Step 5.5 -- planting + succession calendars (the coherence step)
Derive each resolved cell's **`calendar[12]`** from its windows + declared pauses (precedence: pause > plant > harvest > growing). Token vocab for a `frost_anchored` annual: `plant` / `growing` / `harvest` + `cold_pause` / `heat_pause` / `season_over`.
- **THE MID-SUMMER `heat_pause`** is broccoli's signature (the lettuce model): the no-grow gap between the spring and fall windows in warm/temperate regions where T1 documents heat stops heading. A `heat_pause` month that is ALSO a planting month at the gap edge follows checklist A6.
- **`cold_pause`** for a frost-killed / dormant WINTER off-season in the cold zones (NEVER `wait` -- the illegible token 5.5 resolves). **`season_over`** for a frost-free region's hot off-season (the warm South / hawaii hot months when broccoli is not grown). **NO `year_round`** for broccoli (it cannot head through summer heat -- the inverse of a heat-lover).
- **SUCCESSION GEOMETRY (mixed, keyed PER-REGION by continuous-vs-split):** a region with the spring+fall SPLIT (most warm/temperate regions) -> `succession_spring` / `succession_fall` comma-lists; a region with a single CONTINUOUS cool window (a long cool maritime shoulder, or the short northern spring) -> `succession_continuous` (from `first_plant_date`/`last_plant_date`). Each region carries only the geometry it actually is (second_planting spec v1.1 §4). The rule-2 split-count wins before the rule-3 heat_pause split, so the legibility token and the count never collide.
- **DO NOT author per-zone `successions_realized` counts.** Claude Code DERIVES them at release (`tools/derive_realized_successions.py`, gated at whole_crop_gate **A8**: authored spring/fall lists -> count; else day-precise `[first_plant_date,last_plant_date]` split at internal pauses). You author the WINDOWS + GEOMETRY; CC derives + reconciles the integers (and reconciles `succession_policy.successions` to max-over-zones). GLOBAL cap 12.

## 7. Copy + sourcing rules
T1 only (university-extension vegetable guides; seed-company / almanac = T2, evidence-log only, never a dataset citation). The user-facing strings you touch at 4-5.5 are the resolved window/display strings + region labels + any region-tip override: **no em dashes / no `--`; `°F` symbol (never "degrees F"); American English; "broccoli" lowercase.** Backend prose (`*_basis`, `synthesis_note_*`, `source_quote`, provenance) MAY spell "degrees F." `region_notes_*` and all consumer prose stay NULL here (Steps 6-8).

## 8. Deliverable
Hand back the authored slice (or a patch) + the post-author crop SHA + per-region source-mint flags + the region-tip-override attestation + a note of any window-structure finding (one-vs-two windows per region; which regions carry the mid-summer `heat_pause`) or any cut/demoted claim. Claude Code preflights vs `LATEST.txt` (`20a34223`), applies, runs `whole_crop_gate` + the **A8 `successions_realized`** derivation + `register_completeness` + `register_fill` + `release_verify` (frost-reconcile + the `cold_pause`-not-`wait` check + own-source check-G), and promotes. Then the **Steps 6-8 kickoff** (consumer prose + compounds: `region_notes_*`, `description_*`, `growth_stages` / `tips_by_stage`, pests = cabbage-worm complex / aphids / flea beetles / cabbage root maggot, disease = clubroot / black rot / downy mildew, `storage` / `yield` / `container_notes.shape_requirements`) -> Step 9 (dash/temp sweep) -> Step 11 cert.
