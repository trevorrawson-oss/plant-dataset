# Phase 3 -- broccoli Steps 4-5.5 findings (region windows + verification + calendars/succession)

**Lane:** claude.ai author. **Scope:** Steps 4 (region window sourcing) -> 5 (side-by-side verification) -> 5.5 (calendars + succession geometry). NOT Steps 6-8 (consumer prose / compounds stay null).
**Start crop SHA (post-3.5):** `04698276600f1b6a49c4761f8a5df66353290411911d4e972561769e2a66b935` (preflight PASS against SLICE_INTEGRITY.md; full-file `20a34223` per LATEST.txt).
**Post-author crop SHA:** `cb2d61f1a7012de680ff88063f994af8d492b2675df4a5f76be77f70548d19f1`
**Collateral:** only `regions` changed at the crop-field level; all other top-level keys byte-identical. Stripped `lifted_from_zone` (A2) and the stray `sources_pending_admission` keys (sources already-admitted T1 parents). Zero `PENDING`, zero `year_round` anywhere.

---

## Fork outcomes (per your release-lane rulings)

- **Fork 1 (geometry):** per-region split/continuous authored with `track:"succession"` arms. `succession_policy.window_type` left `"continuous"` untouched (vestigial). 6 split regions carry `succession_spring`/`succession_fall`; 4 continuous regions carry `succession_continuous`. **northern_tier = SPLIT** (A5 read: UMN states an explicit spring crop AND a fall crop with no midsummer heat exclusion -- frost-limited both ends, not one continuous run).
- **Fork 2 (hawaii):** bounded lowland **winter** window, NOT `year_round`. CTAHR B-91 states broccoli is an excellent low-elevation crop *during winter*, year-round only *at high elevation* (cooler zones, not the z11 lowland the cell represents). Authored Nov-Dec set-out, Jan-Mar harvest, Apr-Oct `season_over`. **Open finding F-broc-h11-001 (blocks_launch:false):** B-91 gives the cool-SEASON window, not exact lowland-z11 month dates; the authored months are the best-supported reading. Same pattern as zucchini's hawaii cell; Step 11 cert resolves.
- **Fork 3 (ca_north_coast):** **SPLIT**, not continuous. A5 read of UC ANR Table 13.2 North/North Coast column = `Feb-April; July-Sept` -- two windows with a gap, so `succession_spring`/`succession_fall`, light/no heat_pause (marine layer keeps summers cool; June marked `growing`, not a hard heat stop). The column overrode the marine-layer "likely continuous" prior.

---

## Per-region geometry + window-structure table (A5 source findings)

| region | zones | structure | geometry | pauses | primary T1 anchor (window) |
|---|---|---|---|---|---|
| northern_tier | 3-7 | two-window split | spring+fall | cold_pause winter; NO heat_pause | UMN broccoli (spring start indoors early-mid Apr; fall start indoors/out July); UMD (spring set 4wk pre-frost; fall set ~1st wk Aug) |
| se_gulf | 8-9 | two-window split | spring+fall | heat_pause Jun-Aug | UGA C963 (spring Jan15-Mar1, fall Sep1-Oct15 mid-GA; z9 ~2wk earlier/later) |
| ca_interior | 8-9 | two-window split | spring+fall | heat_pause May-Jun; cold_pause Nov | UC ANR T13.2 Interior Valleys (`Dec-Feb; July`) |
| ca_north_coast | 9-10 | two-window split | spring+fall | none hard (marine) | UC ANR T13.2 North/North Coast (`Feb-April; July-Sept`) |
| ca_south_coast | 9-10 | two-window split (inverted) | spring+fall | heat_pause Aug | UC ANR T13.2 South Coast (`June-July; Jan-Feb`) |
| ca_desert | 9-10 | single fall window | continuous | season_over Apr-Aug | UC ANR T13.2 Desert Valleys (`Sept`) |
| warm_arid | 8 | two-window split | spring+fall | heat_pause Jun-Jul; cold_pause Jan | TAMU Aggie Region II (spring Feb15-Mar20) + TAMU fall guide (fall ~Aug 10-25); NMSU CR457-B (warm-zone both-window) |
| low_desert_az | 9 | single long cool window (Aug-Feb) | continuous | season_over May-Jul | U of A AZ1005 Maricopa (T/S Aug->Dec, S Jan-Feb) |
| fl_peninsula | 10-11 | single winter window | continuous | season_over hot months | UF/IFAS broccoli (Central z10 mid-Sep-mid-Feb; South z11 Oct-Dec) |
| hawaii_tropical | 11 | single short winter window | continuous (likely 1-2 sowings) | season_over Apr-Oct | UH CTAHR B-91 (lowland winter only) |

**heat_pause vs cold_pause vs season_over:** heat_pause = interior midsummer no-grow gap between spring & fall crops (split frost-bracketed regions). cold_pause = winter frost-killed/dormant off-season in cold zones (northern_tier z3-7) + the short z8 warm_arid winter edge. season_over = the hot off-season in frost-free / near-frost-free single-window regions where broccoli simply is not grown in summer. No `year_round` (broccoli cannot head through summer heat -- the inverse of a heat-lover).

---

## Step 5 verification (own-source, side-by-side; A1 -- exemplar identity is NOT a justification)

Every window verified against its OWN T1 source (not against lettuce/carrot). Convergences justified by broccoli's own source:
- **Heat-stall threshold (~86°F day / 77°F night stops crown formation):** UMN broccoli page (verbatim) + UC IPM (upper threshold 77-86°F reverts/stops heading; prolonged <50°F bolts). This is the biological basis for every heat_pause and for season_over in the hot regions.
- **Transplant-led + light-frost tolerance:** UMN, UMD, UC MG county guides. Spring start indoors ~5-7wk ahead; fall direct or transplant.
- **Fall-often-better-than-spring (cold/temperate):** UMD ("fall broccoli often produces higher yields than spring plantings in the mid-Atlantic"). Reflected in northern_tier prose intent (Steps 6-8) + the fall second_planting arm.
- **se_gulf split:** UGA C963 chart + C943 calendar (two independent UGA pubs); UF/IFAS corroborates the inverted/peninsular boundary.
- **CA columns:** UC ANR Master Gardener Handbook Table 13.2 (one row per region column, transplants), fetched live.
- **low_desert_az continuous Aug-Feb:** U of A AZ1005 monthly grid (broccoli T=90-100/S=120-130 days; markers Aug->Feb), corroborated by the Maricopa MG "planted Sep/Oct, harvested Jan/Feb" note.
- **fl_peninsula:** UF/IFAS broccoli page (Central mid-Sep-mid-Feb; South Oct-Dec; 80-100 day Waltham; pH 6.2-6.5).
- **hawaii lowland winter:** CTAHR B-91.

**No template-copy / cross-region analogy.** Each cell's window rests on its own region's source (A5). Continuous-vs-split decided per source, never by neighbor analogy.

---

## Step 5.5 calendars + succession geometry

- All 20 resolved cells carry a derived `calendar[12]` (programmatic, precedence pause > plant > harvest > growing; zero silent `wait`). Tokens validated against the 13-state enum.
- **Succession geometry mixed per-region (second_planting spec v1.1 sec4):** split -> `succession_spring`+`succession_fall` comma-lists; continuous -> `succession_continuous`. Each region carries only the geometry it is. rule-arm `track:"succession"` entries present in every region (gate-critical: suitable+successions>1).
- **`successions_realized` NOT authored** -- left for Claude Code A8 derivation (`derive_realized_successions.py`); authored the windows + geometry only. The hawaii/short-window cells will derive a low realized count (the continuous run is short).
- **heat_pause sibling objects** authored on the 7 split-region heat-gap cells with `{months, classification, basis_seasoned, sources, anchoring_urls}`; months kept coherent with the calendar heat_pause tokens (A6). **season_over sibling objects** on the 6 frost-free single-window cells, months coherent with calendar.

---

## Region-tip-override attestation (Step 4 v1.4 rider)

Scope = `succession_policy.tip_*` (tips_by_stage is Steps 6-8). Checked the editorial succession tip against the regional T1 read for all 10 regions. **The grower ACTION is invariant** -- succession-sow within the cool window(s), pause through heat. Regional differences are timing/structure (months; one-vs-two windows), carried by the per-cell windows + geometry + calendar pauses, NOT a divergent tip action. **No override authored** (a pressure gradient is not a divergent action). Mechanical: 0 override fields, 0 PENDING/placeholder. PASS.

---

## Copy + sourcing compliance

- **Copy sweep (253 user-facing strings):** 0 `--`, 0 em/en-dash, 0 smart quotes, 0 mid-sentence "Broccoli" caps. All 5 user-facing `heat_pause`/`season_over` `basis_seasoned` strings use the `°F` symbol (A3). Backend `synthesis_note_seasoned` arms may spell "degrees F" and do where natural.
- **Source-verbatim 8-gram scan:** 0 overlaps after rewording one northern_tier fall note that mirrored UMN too closely.
- **region_label colon convention:** all 10 use the colon form (e.g. `California: Interior Valleys`, `Southeast: Gulf & Coastal Plain`, `Florida: Peninsula`), zero ` -- `.

---

## Source mint flags (for Claude Code release lane)

All anchors are specific-page sub-ids under already-admitted T1 catalog parents. Re-point bare keys to family parents per the autonomous mint rule:

| sub-id (authored) | parent (catalog) | page |
|---|---|---|
| umn_ext_broccoli | umn_ext | extension.umn.edu/vegetables/growing-broccoli |
| umd_ext_broccoli | umd_ext | extension.umd.edu/resource/growing-broccoli-home-garden |
| iastate_ext_colecrops | iastate_ext | hortnews.extension.iastate.edu/2018/03/planting-broccoli-cabbage-and-cauliflower-home-garden |
| uga_c963_chart | uga_ext | C963 planting chart PDF |
| uga_c943_calendar | uga_ext | C943 vegetable garden calendar |
| ufifas_broccoli | ufifas_ext | gardeningsolutions.ifas.ufl.edu/.../broccoli |
| ufifas_vh021 | ufifas_ext | ask.ifas.ufl.edu/publication/VH021 |
| ucanr_mg_timeplanting | ucanr_ext | ucanr.edu/program/uc-master-gardener-program/time-planting (Table 13.2) |
| uariz_az1005 | uariz_ext | AZ1005 (Maricopa County) |
| nmsu_cr457b | nmsu_ext | pubs.nmsu.edu/_circulars/CR457B |
| tamu_aggie_spring | tamu_agrilife | aggie-hort spring planting guide (Regions I-V) |
| tamu_fall_veg | tamu_agrilife | AgriLife Fall Vegetable Gardening Guide |
| uhawaii_ctahr_b91 | uhawaii_ctahr | CTAHR B-91 |

All anchoring URLs verified live 2026-06-23. Tier inherited T1 from parent.

---

## Open findings (all blocks_launch:false)

- **F-broc-h11-001:** hawaii_tropical z11 lowland window dated from CTAHR B-91's cool-SEASON statement, not an exact lowland month table. Best-supported reading; Step 11 cert to confirm or refine (mirrors zucchini hawaii).
- **F-broc-warmarid-001 (Path A note):** the Dona Ana County MG Las Cruces chart (a region-specific z8 corroborator) is a visual bar grid that does not survive text extraction (A5 Path A case). warm_arid z8 was anchored on readable TAMU Aggie Region II (spring) + TAMU fall guide + NMSU CR457-B prose instead, so no chart-bar inference was made. If a Path A human-read of the Dona Ana chart is desired at cert, it would refine (not overturn) the authored months.

---

## Handback for Claude Code (release lane)

1. Preflight `sha256(crops_data_final.json) == LATEST.txt` (`20a34223`) before applying.
2. Apply the authored broccoli slice (post-author crop SHA `cb2d61f1...`).
3. Re-point the 13 sub-ids to their T1 parents in `source_catalog` (mint table above); record `_admission_provenance`.
4. Run `whole_crop_gate` + **A8 `successions_realized` derivation** (`derive_realized_successions.py`; reconcile `succession_policy.successions` to max-over-zones; GLOBAL cap 12) + `register_completeness` + `register_fill` + `release_verify` (frost-reconcile each cell's `resolved_from` vs `zone_frost_data.json`; `cold_pause`-not-`wait` check; own-source check-G).
5. Promote -> then the Steps 6-8 kickoff (region_notes_*, description_*, growth_stages/tips_by_stage, pests = cabbage-worm complex/aphids/flea beetles/cabbage root maggot, diseases = clubroot/black rot/downy mildew, storage/yield/container_notes.shape_requirements) -> Step 9 -> Step 11 cert.
