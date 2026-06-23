# Broccoli Steps 1-3 -- Author-Lane Findings

**Session:** phase_3_broccoli_steps1-3 (claude.ai author lane)
**Date:** 2026-06-23
**Crop:** broccoli (anchor ~17; rail-rider on the proven `cool_season_annual` rails + succession crop)
**Base crop SHA (blank shell):** `2f81cd13c3db2a74205d9caf85ef89ccda38d99909bfee7d8676b0d23691833c` (preflight PASS vs `SLICE_INTEGRITY.md`)
**Post-author crop SHA:** `7d2da816380daa53f760392d02e4d90cf8363070eecc81a45210129ba692c005`
**Live base `LATEST.txt`:** `0b767fc2…` (`blueberry_step11_cert`)
**Parallel session note:** zucchini Steps 1-3 authored against the same `0b767fc2` base in a separate session. Independent author-lane slices; release one at a time, re-preflighting `LATEST.txt` before each apply.

---

## Scope authored (Steps 1-3)

**Step 1 -- source set:** 9 T1 university-extension parents, all already in the catalog (no new parents minted). Cited: `clemson_hgic`, `iastate_ext`, `ncsu_ext`, `osu_ext`, `umd_ext`, `umn_ext`, `usu_ext`, `uwi_hort`, `wvu_ext`. `sources_summary.primary` rewritten to these 9 (de-duped, alphabetical).

**Step 2 -- scalars + structured biology:** difficulty, days_to_maturity (+ `_mid`), spacing_inches, germination_temp_f, sunlight (+ hours), water, weeks_indoors, lifecycle/perennial, harvest_urgency, first_planting_notify_days; soil, ph, fertilizer, watering (full dual-register blocks), start_method, container_notes; rotation, bolting; descriptions, harvest_ready, soil_prep (top-level CP siblings). **The full `succession_policy`** (was all-null).

**Step 3 -- varieties + companions:** `varieties.recommended[]` (6 entries, `{name, days_to_maturity, note}`); companions in the certified three-array rich-object shape.

**Deferred to Steps 6-8 (left as null shells, matching the green-beans 1-3 precedent + the kickoff Step 2 scope):** `storage`, `yield_expectations`, `container_notes.shape_requirements`. The A12 compounds (pests, diseases, growth_stages, tips_by_stage, notifications, weather_triggers, failure_diagnostics) remain empty. `regions`/`zones` untouched (Steps 3.5/4).

---

## Fork decisions (Trevor-adjudicated via Claude Code, this session)

1. **`succession_policy.interval_weeks` = 3** (NOT 2). The cool-season rail is not uniform (lettuce-leaf 2, carrot 3); broccoli is a slower 55-75-day header and patterns with carrot. Decisive point: `interval_weeks` feeds the A8 `successions_realized` deriver (`floor(span/(iw*7))+1`), so a too-fast 2 would overestimate broccoli's realized sowings in its short spring window. Sourced as "every 2 to 3 weeks" (WVU successive plantings); 3 is the representative value. The short window now shows up honestly as low realized counts via the Step-4 geometry.

2. **Container: `container_ok=true` + `min_pot_gallons=5` + `depth_inches_min=12`, T1-SOURCED (not flagged).** Found a clean T1 anchor: **`uwi_hort`** (Wisconsin Horticulture Extension, "Growing Vegetables in Containers") tables broccoli among larger plants needing "a minimum volume of five gallons and a depth of 12 to 18 inches." Both figures are exact-from-T1. (Corroborated by multiple T2 sources at 5 gal / one plant per pot; not cited.) `min_pot_gallons` is NOT null -- it carries the offer in the garden calculator.

3. **Bad-companion labels split:** brassica adjacency caution = **`likely`** (clubroot is a documented soilborne disease and shared cabbage-family pest buildup is real -- a known agronomic principle, not formally pair-tested); strawberries + tomatoes (competition lore) = **`traditional`**. The `rotation` block carries the clubroot "don't grow brassicas after brassicas" rationale separately, T1-grounded (`umn_ext` clubroot, `ncsu_ext`).

---

## Items to confirm / flag for release lane

### F-broc-001 (low, blocks_launch:false) -- `rotation.rotation_years = 3` rests on standard cole guidance, not an explicit single-number T1 citation.
T1 sources document the *principle* (rotate brassicas; clubroot persists in soil -- `umn_ext`, `ncsu_ext`), but the specific "3 years" interval is standard cole-crop practice rather than an explicit T1 figure. Cited honestly to the rotation/clubroot pages; the *number* is conventional. Same handling as the green-beans `rotation_years` flag. Confirm or refine at release. NOTE: clubroot ideally wants longer (up to ~7 yr) where present; the `note_seasoned` says so.

### F-broc-002 (informational) -- source-mint decision deferred to release lane.
All 9 cited IDs are existing catalog PARENTS, each anchored in-slice to its specific broccoli page URL (verified live 2026-06-23). Release lane decides whether to mint page-specific sub-ids (e.g. `ncsu_ext_broccoli`, `umd_ext_broccoli`) under each parent per the autonomous sub-id mint convention, or keep parent-level anchoring. No new parents required.

### F-broc-003 (informational) -- two T2-sourced numbers removed during the numeric-fidelity pass.
- `soil_prep` originally said "2 to 4 inches of compost" -- that figure traces to the almanac (T2), not the cited T1 soil pages (which say "high organic matter / work in compost" without the depth). Reworded to "plenty of compost" to avoid an unsourced number.
- `start_method` fall-timing originally "6 to 8 weeks before the first fall frost" (almanac T2); reconciled to the UMD-grounded "start transplants in mid to late summer, about 4 to 6 weeks before setting them out."

### F-broc-004 (informational) -- moon_phase_preference left all-null.
No-evidence field, consistent with carrot and green-beans. Not flagged as a gap.

### F-broc-005 (informational) -- companion vocabulary / PK staleness (carry-forward, not blocking).
Authored to the live certified shape: three-array membership (`good_beginner` / `good_beginner_seasoned` / `good_seasoned` + bad triple) with vocab `research_backed` / `likely` / `traditional`, matching carrot/green-beans/zinnia/strawberry and the live shell. Three project-knowledge docs still carry the OLD vocab/shape and are owed a sync so the bot pipeline does not trip on them: `schema_2_7_visibility_map_v1_0.md` (line ~123, `good_core`/`good_seasoned` two-array), `methodology_page_companions_section.md` (`extension_backed`/`mechanistic`/`disputed`), and the v1.6 checklist text. This is the same conflict the zinnia session resolved in favor of the new vocab.

---

## Validation gauntlet (self-checks, all PASS)

- **Preflight:** base crop SHA == `2f81cd13…` (blank shell). PASS.
- **Scope guards:** top-level key set unchanged; `regions`/`zones` byte-identical to base; all 7 A12 compounds + tips_by_stage empty; `storage`/`yield_expectations` == base null shells. PASS.
- **Copy rules** (158 user-facing strings): 0 em/en-dash or `--`; 0 spelled "degrees F" (one instance in `bolting.triggers` was caught and converted to `°F`); 0 non-ASCII beyond the degree sign; 0 mid-sentence "Broccoli". PASS.
- **Source-verbatim 8-gram scan** vs the 9 cited T1 pages: 0 overlaps (4 numeric-phrase overlaps in `ph.note_seasoned` + `watering.frequency_seasoned` were caught and reworded; advisory 7-gram also clean). PASS.
- **Numeric fidelity:** every figure cross-checked vs its cited T1 (germination 40-86 OSU exact; pH 6.0-6.5 / tolerated 5.5-6.8 NCSU exact; container 5 gal / 12 in uwi_hort exact; 86/77°F heading ceiling UMN/ISU exact; 35-50°F cold-bolt Clemson exact; half-cup 21-0-0 / quarter-size USU exact; spacing/DTM spans within T1 ranges). Two T2 numbers removed (F-broc-003). PASS.
- **Register distinctness:** 0 byte-identical prose pairs across 55 seasoned/beginner pairs. (`hardening_off` boolean True/True and is not a prose pair; `watering.amount` differentiated to match the green-beans precedent.) PASS.
- **Companion shape:** vocab subset of {research_backed, likely, traditional}; tight set (good_beginner_seasoned: Dill, Onions, Lettuce) is a subset of the full good_seasoned roster; both bad arrays populated (bad_beginner_seasoned: 1; bad_seasoned: 3). PASS.
- **Citation pairing:** every populated block with a non-empty `sources` array has a matching `anchoring_urls` keyset. PASS.
- **Round-trip:** pretty-printed handback file yields the identical crop SHA. PASS.

---

## Release-lane checklist (Claude Code)

1. Preflight `sha256(crops_data_final.json) == LATEST.txt` (`0b767fc2…`) before applying (rebase if zucchini released first).
2. Apply broccoli slice (paths broccoli-crop-relative).
3. Decide source-mint (F-broc-002): page-specific sub-ids vs parent-level.
4. Run `whole_crop_gate` + `register_completeness_gate` + `register_fill_gate`.
5. Collateral hash audit: only `broccoli` changes; all 122 other crops + non-crop top-level keys byte-identical.
6. Promote. Then Step 3.5 (transplant-shape region shells, `start:"both"` -> transplant path), Step 4 (region fill + spring/fall double-window + heat_pause + the A8 `successions_realized` derivation), Steps 6-8 (compounds: cabbage-worm complex / aphids / flea beetles / cabbage root maggot; clubroot / black rot / downy mildew; + storage, yield_expectations, shape_requirements), Step 9, cert.

**Feed-forward conventions applied (from green-beans):** `succession_policy` is the Step-2 deliverable, `successions_realized` stays OUT (A8 derives at Step 4); companion rich-object shape + vocab; `soil.organic_matter_preference` as a categorical token (`high`); `container_notes.shape_requirements` dropped at 1-3 (deferred to 6-8 as a real dual-voice pair, not a null half-pair).
