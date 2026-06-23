<!-- APPEND to STATE_HISTORY.md, most-recent-first, below the header. Do NOT rewrite existing entries. -->

## 2026-06-23 -- broccoli Steps 4-5.5 authored (claude.ai lane): region windows + verification + calendars/succession

**Start crop SHA:** `04698276600f1b6a49c4761f8a5df66353290411911d4e972561769e2a66b935` (post-3.5; preflight PASS vs SLICE_INTEGRITY.md at full-file `20a34223`).
**Post-author crop SHA:** `cb2d61f1a7012de680ff88063f994af8d492b2675df4a5f76be77f70548d19f1`
**Gate:** not run this session (claude.ai authored slice + this entry; Claude Code releases -- preflight `20a34223`, apply, whole_crop_gate + A8 `successions_realized` derivation + register gates + release_verify [frost-reconcile + cold_pause-not-wait + own-source check-G], re-pin SHA, regenerate CURRENT_STATE, commit).

### What happened
All 10 broccoli region cells filled with sourced windows + own-source verification + derived `calendar[12]` + per-region succession geometry. Region fill 0/10 -> 10/10. broccoli's signature SPRING+FALL double-window with a midsummer `heat_pause` is now encoded in the warm/temperate split regions; the cold tier carries cold_pause winters with no heat_pause; frost-free single-window regions carry `season_over` hot off-seasons. No `year_round` anywhere (broccoli cannot head through summer heat -- the cool-season inverse of zucchini).

### Fork rulings (Trevor, release-lane, in-session)
- **Fork 1:** per-region geometry authored with `track:"succession"` arms; crop-level `succession_policy.window_type` left `"continuous"` (vestigial categorical label; no deriver/gate reads it; consistent with carrot/lettuce/green-beans/zucchini). 6 split regions (`succession_spring`/`succession_fall`), 4 continuous (`succession_continuous`). northern_tier authored SPLIT per its own UMN source (A5), not forced.
- **Fork 2:** hawaii_tropical = bounded lowland WINTER window (CTAHR B-91: low-elevation winter crop; year-round only at high elevation), NOT `year_round` -- the onion/zinnia z11 precedent, confirmed by a real CTAHR source. blocks_launch:false finding for the season-not-exact-months sourcing.
- **Fork 3:** ca_north_coast = SPLIT per UC ANR Table 13.2 (`Feb-April; July-Sept`); the column overrode the marine-layer "likely continuous" prior.

### Per-region geometry (A5 source findings)
- SPLIT (spring+fall, heat_pause or cold_pause between): northern_tier (cold_pause, NO heat_pause), se_gulf, ca_interior, ca_north_coast (no hard pause), ca_south_coast, warm_arid.
- CONTINUOUS (single cool run, season_over hot months): ca_desert (single Sep window), low_desert_az (Aug-Feb), fl_peninsula (z10 Sep-Feb / z11 Oct-Dec), hawaii_tropical (Nov-Dec lowland winter).
- Tally: 7 cells heat_pause, 6 cells season_over (sibling objects), 14 cells second_planting, 6 cells succession_continuous, 20 resolved cells total.

### Precedents reinforced
- **A5 anti-cross-region:** every cell's continuous-vs-split + window structure decided from its own region's T1 (UMN/UGA/UC ANR T13.2/U of A AZ1005/UF/IFAS/CTAHR/TAMU/NMSU), never by neighbor analogy. ca_north_coast SPLIT and northern_tier SPLIT both came from reading the source, against the obvious prior.
- **A1 exemplar-identity:** heat-stall basis (~86°F day/77°F night) sourced to UMN + UC IPM, not "matches lettuce/carrot."
- **A3 user-facing °F:** all heat_pause/season_over `basis_seasoned` use the °F symbol; backend synthesis_note arms spell "degrees F" where natural.
- **cold_pause-not-wait:** cold zones + warm_arid winter edge use cold_pause; zero `wait` tokens. season_over reserved for the frost-free hot off-season.
- **Region-tip override:** none owed -- the succession tip's grower action is invariant across regions (timing gradient, not divergent action).

### Hygiene
Collateral: only `regions` changed at crop-field level. Stripped `lifted_from_zone` (A2) and stray `sources_pending_admission`. 8-gram source-verbatim scan 0 after one reword. 13 specific-page sub-ids minted under already-admitted T1 parents (re-point at release).

### Open findings (blocks_launch:false)
- F-broc-h11-001: hawaii lowland window dated from CTAHR season statement, not an exact month table (Step 11 to confirm/refine).
- F-broc-warmarid-001: Dona Ana MG Las Cruces chart is a visual bar grid (A5 Path A); warm_arid z8 anchored on readable TAMU Region II + TAMU fall guide + NMSU CR457-B instead. Optional Path A human-read at cert would refine, not overturn.
- Carry-forwards unchanged: F-broc-001 (rotation_years=3 confirm at cert); F-broc-005 (3 PK docs companion-vocab sync, claude.ai lane).

### Next
Claude Code release (above) -> Steps 6-8 (consumer prose + 7 compounds: cabbage-worm complex/aphids/flea beetles/cabbage root maggot; clubroot/black rot/downy mildew; storage/yield/container shape) -> Step 9 (dash/temp sweep) -> Step 11 cert. broccoli is the cool-season final rail-rider; zucchini (warm-season) is the parallel.
