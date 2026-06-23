## 2026-06-23 -- zucchini-courgette Steps 4-5.5 AUTHORED: region windows + verification + calendars/succession [claude.ai author lane]

**base `2a47731a` (slice crop SHA `23a7977f`) -> post-author crop SHA `7cc97e20500b43ab09a4dbb00309203164766492420f02195ec9aa1884d7c8a9`.** The sourced region-fill leg of the first of the last 2 rail-riders. claude.ai authored Steps 4 (warm-region window sourcing, author-fresh) + 5 (own-source side-by-side) + 5.5 (calendar[12] + succession geometry + per-arm anchoring). NOT released yet -- Claude Code preflights `2a47731a`, applies, runs whole_crop_gate + A8 successions_realized derivation + register gates + release_verify, then promotes. NOT a flip (status null; cert is Step 11).

### Authored (Steps 4-5.5 scope; region_notes + compounds deferred to 6-8)
- **All 10 region cells filled** (windows + resolved_by_zone + calendar[12] + succession geometry + region label/zone_span/region_id). `region_notes_*` LEFT NULL (Steps 6-8). `calendar_basis` stays `frost_anchored`. Collateral: only `regions{}` changed (key-delta verified: 0 top-level keys added/removed/changed outside regions).
- **Succession geometry (mixed, per-region, second_planting spec v1.1 §4):** CONTINUOUS (`succession_continuous`) = northern_tier, ca_interior, ca_north_coast, ca_south_coast, warm_arid, fl_peninsula (inverted), hawaii_tropical. SPLIT (`succession_spring`+`succession_fall`) = se_gulf, ca_desert, low_desert_az. plantings[] arms: continuous = beginner + one `track:"succession"` arm; split = beginner + `track:"succession"` spring + `track:"succession"` fall. **NO `track:"second_planting"`** (that is the cherry NON-succession model; zucchini is a succession crop -> the lettuce/green-beans split model). `successions_realized` NOT authored (CC derives at A8).
- **Direct-sow-dominant (`start_method.start=="both"`):** `plant_out` = after-frost direct-sow/set-out in every region; `start_indoors` populated ONLY at the short-season cold end + the CA March-indoor-lead cells; empty elsewhere.
- **Calendars (5.5):** 13-state enum, len 12, 0 `wait` tokens (green-beans lesson held). Winter off-season `cold_pause` (frost-bracketed z3-10); frost-free FL summer off-season `season_over`; desert/SE mid-summer no-plant gap `heat_pause`; Hawaii growing/plant/harvest (no off-season token). fl_peninsula = inverted (Jun-Aug season_over). 
- **Frost reconcile:** all frost-bracketed cells byte-exact to zone_frost_data; z11 frost-free cells (fl_peninsula z11, hawaii z11) resolved_from null. Several warm windows are SOURCE-SET (not LF+offset), with resolved_from recording the frost AUDIT only (A5).

### Sourcing (T1 only; 0 mints, 0 non-T1)
10 catalogued T1 parents: umn_ext/umd_ext/iastate_ext (NT); ucanr_ext (CA interior/coasts/desert -- Pub 7245 + T13.2 + Marin squash guide); uga_ext (se_gulf -- B577 + C943); uariz_ext (low_desert_az -- AZ1005 + AZ1615); nmsu_ext+tamu_agrilife (warm_arid); ufifas_ext (fl_peninsula -- Gardening Solutions Summer Squash + VH021); uhawaii_ctahr (hawaii -- B-91). Per-arm + per-cell anchoring to specific verified pages (bare-parent + specific-URL, no sub-id fragmentation). **Source-mint flags: NONE.**

### Window-structure finding (A5)
se_gulf mapped continuous initially; UGA B577 (explicit spring + fall date columns) + C943 ("no later than Aug 31") overturned it to SPLIT. ca_interior confirmed CONTINUOUS by UC ANR 7245 (fall taper on virus, no no-plant gap). Final: 7 continuous, 3 split (the 3 hottest-summer regions).

### THREE FLAGS FOR CLAUDE CODE (Trevor approved all; flagged in case the author read is wrong)
1. **Desert `heat_pause` despite `pause_in_heat:false`** -- se_gulf/ca_desert/low_desert_az carry a mid-summer `heat_pause` token (a per-region A5 calendar finding: real no-plant gap between two harvest bands, AZ1005/UGA-sourced) even though the crop-level cadence flag is false (the flag describes the temperate cadence; the green-beans precedent). CC: confirm the gate/A8 deriver does not treat pause_in_heat:false as forbidding a region heat_pause token.
2. **Hawaii authored BOUNDED-CONTINUOUS, not year_round** -- no CTAHR continuous statement found; frost-free z11 alone insufficient (onion/zinnia rule). `plantings_provenance` instructs CC: if the release-lane CTAHR fetch finds an explicit continuous/year-round zucchini statement, upgrade to year_round + log blocks_launch:false open finding. Default authored = bounded-continuous, no fabricated source_quote.
3. **warm_arid z8 authored CONTINUOUS** -- no T1 mid-summer gap found for the z8 high-desert band (distinct from Sonoran low desert); mirrors green-beans warm_arid z8. CC: confirm the live NMSU CR457 squash row at release; if it shows a desert-style summer gap, this would split.

### Region-tip override (Step-4 rider): attestation present, 0 overrides
Core grower actions universal across zones 3-11; only timing/structure varies (expressed in windows/calendars). No materially different grower action -> no override warranted.

### Verification
Own-source side-by-side (A1; not "matches lettuce/green-beans"). 8-gram source-verbatim scan on plantings_provenance: 0 HARD lifts (reworded one ca_desert UC ANR run). Numeric fidelity: sampled windows match cited months.

### Next
Claude Code releases: preflight `2a47731a` -> apply -> whole_crop_gate + A8 `successions_realized` (`derive_realized_successions.py`) + register_completeness + register_fill + release_verify (frost-reconcile + cold_pause-not-wait + own-source check-G) -> promote. Then Steps 6-8 (region_notes + consumer prose + compounds: fertilizer on the MODERATE-feeder profile; pests squash vine borer/squash bug/cucumber beetle; disease powdery mildew/bacterial wilt; yield/storage) -> Step 9 -> Step 11 cert.
