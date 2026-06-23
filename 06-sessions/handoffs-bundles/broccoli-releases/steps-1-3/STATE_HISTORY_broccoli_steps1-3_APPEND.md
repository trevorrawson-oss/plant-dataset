## 2026-06-23 -- broccoli Steps 1-3 (author lane, claude.ai) -- session `phase_3_broccoli_steps1-3`

**Start-SHA (blank shell crop SHA):** `2f81cd13c3db2a74205d9caf85ef89ccda38d99909bfee7d8676b0d23691833c` (preflight PASS vs `SLICE_INTEGRITY.md`; live full-file base `LATEST.txt` = `0b767fc2…`, the blueberry cert)
**End-SHA (post-author crop SHA):** `7d2da816380daa53f760392d02e4d90cf8363070eecc81a45210129ba692c005`
**Gate:** not run this session (claude.ai authored the slice + this entry + a findings doc only; Claude Code preflights, applies, runs whole_crop_gate + register_completeness + register_fill, re-pins SHA, regenerates CURRENT_STATE, commits).

### What happened
Authored Steps 1-3 for **broccoli** -- the second of the two final rail-riders (with zucchini), a cool-season annual on the proven `cool_season_annual` rails (lettuce-leaf / carrot) plus a succession crop. No new archetype, no new tooling. Parallel to a separate zucchini Steps 1-3 session on the same `0b767fc2` base; independent slices, released one at a time.

- **Step 1 -- sources:** 9 T1 extension parents, all already in the catalog (no new parents): clemson_hgic, iastate_ext, ncsu_ext, osu_ext, umd_ext, umn_ext, usu_ext, uwi_hort, wvu_ext. Each anchored in-slice to its specific broccoli page (verified live 2026-06-23). `sources_summary.primary` rewritten to these 9.
- **Step 2 -- scalars + structured biology:** days_to_maturity [55,75] (+mid 65), spacing_inches [12,24] in-row, germination_temp_f [40,86] (OSU exact), weeks_indoors 5, sunlight full_sun [6,8]; full soil / ph ([6.0,6.5], tolerated 5.5-6.8) / fertilizer (heavy N feeder) / watering dual-register blocks; start_method `both` (transplant-led spring, direct-or-transplant fall, weeks_before 5); container_notes (T1-sourced); rotation (clubroot driver) and bolting (heat/buttoning); descriptions, harvest_ready, soil_prep.
- **Step 2 -- `succession_policy`** authored full (was all-null): suitable true, **interval_weeks 3**, successions 3 (nominal), max_successions_per_season 12 (global cap), window_type continuous, **pause_in_heat TRUE** (the cool-season inverse of the warm-season rail-riders -- broccoli cannot head in summer heat; 86F day / 77F night stops crown formation per UMN/ISU), trigger last_frost, dual-register tips.
- **Step 3 -- varieties:** 6 recommended ({name, days_to_maturity, note}): Calabrese, Green Magic, Belstar, De Cicco, Waltham 29, Sun King -- spanning the spring-heat-tolerant / fall-overwinter / side-shoot-heirloom range.
- **Step 3 -- companions:** certified three-array rich-object shape, vocab research_backed/likely/traditional. good_beginner_seasoned (tight: Dill, Onions, Lettuce); good_seasoned (fuller: + Spinach, Nasturtiums, Marigolds, Celery); bad_beginner_seasoned (Other brassicas) + bad_seasoned (Other brassicas, Strawberries, Tomatoes). No broccoli-specific companion T1 trial exists, so most pairings are honest `traditional`; the brassica adjacency caution is `likely` (clubroot/shared-pest principle) and nasturtium trap-cropping is `likely` (documented principle, not pair-tested).

### Fork decisions (Trevor-adjudicated via Claude Code)
1. **interval_weeks = 3, not 2.** The cool-season rail is not uniform (lettuce 2 / carrot 3); broccoli is a slower header and patterns with carrot. interval_weeks feeds the A8 successions_realized deriver, so a too-fast 2 would overestimate realized sowings; 3 is honest, and the short spring window shows up as low realized counts via Step-4 geometry. Sourced as "every 2-3 weeks."
2. **Container: min_pot_gallons 5 + depth_inches_min 12, T1-sourced** via uwi_hort ("minimum volume of five gallons and a depth of 12 to 18 inches"). Set, not flagged, not null -- the calculator offer rides on a non-null min_pot_gallons.
3. **Bad-companion labels split:** brassica adjacency = `likely` (clubroot grounding); strawberries/tomatoes = `traditional` (competition lore). rotation block carries the clubroot rotation rationale separately, T1-grounded.

### Items flagged for release (all blocks_launch:false)
- **F-broc-001:** rotation_years 3 rests on standard cole practice, not an explicit single-number T1 (same handling as green-beans). Principle (rotate brassicas / clubroot persists) is T1; the number is conventional.
- **F-broc-002:** source-mint decision (page sub-ids vs parent-level) deferred to release lane; no new parents needed.
- **F-broc-003:** two T2 numbers removed in the numeric pass (soil_prep "2-4 inches compost" -> "plenty of compost"; start_method fall "6-8 wk before frost" -> UMD-grounded "4-6 wk before setting out").
- **F-broc-004:** moon_phase left all-null (no-evidence field, matches carrot/green-beans).
- **F-broc-005 (carry-forward):** three PK docs still carry the OLD companion vocab/shape (visibility_map v1.0, methodology_page_companions_section, v1.6 checklist) and are owed a sync; authored to the live certified shape regardless.

### Self-checks (all PASS; Claude Code re-verifies at release)
Preflight SHA; scope guards (regions/zones byte-identical, compounds empty, storage/yield deferred); copy rules (0 dash / 0 spelled-degrees / 0 non-ASCII / 0 mid-sentence Broccoli -- one `bolting.triggers` "degrees F" caught and fixed to °F); source-verbatim 8-gram = 0 (4 numeric-phrase overlaps reworded); numeric fidelity (all figures vs cited T1; 2 T2 numbers removed); register distinctness = 0 identical prose pairs; companion shape + vocab; citation pairing on every populated block; pretty round-trip SHA matches.

### Deferred to later steps
storage, yield_expectations, container_notes.shape_requirements -> Steps 6-8 (null shells now, per the green-beans 1-3 precedent). A12 compounds -> Steps 6-8. regions/zones -> Steps 3.5 (transplant-shape shells) + 4 (region fill, spring/fall double-window, heat_pause, A8 successions_realized derivation).

---
