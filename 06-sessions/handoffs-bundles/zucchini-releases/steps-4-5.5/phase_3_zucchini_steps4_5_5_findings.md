# Zucchini / Courgette Steps 4-5.5 -- region windows + verification + calendars/succession
## claude.ai author-lane findings (session: zucchini_steps4-5.5_author)

**Base:** full-file canonical `2a47731a` (LATEST.txt); slice crop SHA `23a7977f` (SLICE_INTEGRITY) -- BOTH confirmed at preflight.
**Post-author crop SHA (sorted-min, ensure_ascii=False):** `7cc97e20500b43ab09a4dbb00309203164766492420f02195ec9aa1884d7c8a9`
**Scope delivered:** Step 4 (warm-region window sourcing, author-fresh, all 10 regions) + Step 5 (own-source side-by-side verification) + Step 5.5 (calendar[12] derivation + per-region succession geometry + per-arm anchoring). Region labels (colon form) + zone_span + region_id filled. `region_notes_*` LEFT NULL (Steps 6-8). `calendar_basis` stays `frost_anchored`.
**Collateral:** only `regions{}` changed; all other top-level keys byte-identical (key-delta verified -- 0 added, 0 removed, 0 non-regions key changed).

---

## TWO STRUCTURAL DECISIONS FLAGGED FOR CLAUDE CODE (Trevor approved both; flagging in case I read either wrong)

### FLAG 1 -- DESERT `heat_pause` despite crop-level `pause_in_heat:false`
The split desert/SE regions (`se_gulf`, `ca_desert`, `low_desert_az`) carry a `heat_pause` calendar token in their mid-summer no-plant month(s), even though `succession_policy.pause_in_heat == false`.
- **Why this is correct (my read):** `pause_in_heat:false` is the crop-level statement that zucchini's TYPICAL (temperate/northern) succession cadence is not interrupted by heat -- the fall succession is squash-vine-borer / powdery-mildew driven, not a heat pause. But the desert/SE regions have a LITERAL mid-summer no-plant gap that is a per-region SOURCE finding (A5): AZ1005 states the low desert has two planting seasons because few annuals survive the summer extreme; UGA B577/C943 give a spring window ending in heat and a distinct fall window. The calendar token for that documented gap is `heat_pause` (the legible Step-5.5 token; `wait` is forbidden). This is exactly the green-beans precedent (CURRENT_STATE locked decision: continuous->succession_continuous, split->succession_spring/fall; the desert mid-summer gap rendered heat_pause while pause_in_heat stayed false).
- **What CC should check:** that the A8 deriver + whole_crop_gate do not treat `pause_in_heat:false` as forbidding a region `heat_pause` token. If the gate flags this, the resolution is the green-beans one (the per-region token is a calendar finding, not a contradiction of the crop-level cadence flag). If I have mis-modeled this, the alternative is to express the desert summer as a planting-window edge with no heat_pause token -- but the sources document a genuine no-plant GAP between two harvest bands, which is a pause, not an edge.

### FLAG 2 -- HAWAII authored BOUNDED-CONTINUOUS, not year_round
`hawaii_tropical` z11 is authored as bounded-continuous (`succession_continuous`, plant_out "Jan - Oct", harvest "Feb 15 - Dec 15", resolved_from null), NOT `year_round`.
- **Why (my read):** I found NO CTAHR source explicitly stating continuous year-round zucchini cultivation. Per the locked rule (onion/zinnia precedents), frost-free z11 alone is insufficient to declare year_round. So I defaulted to the honest bounded-continuous shape with no fabricated source_quote, and stated the basis in `plantings_provenance`.
- **What CC should do:** the `plantings_provenance` carries an explicit instruction -- if CC's release-lane CTAHR fetch (B-91 / a CTAHR production guide) finds an explicit continuous/year-round zucchini statement, UPGRADE the cell to `year_round` (the basil/zinnia Hawaii pattern) and log a `blocks_launch:false` open finding. Default authored = bounded-continuous. The calendar uses growing/plant/harvest tokens (no season_over, since it is not bounded by a hot off-season the way frost-free FL is -- Hawaii's limiter is wet-season pest/disease pressure, qualitative).

### (minor) FLAG 3 -- warm_arid z8 authored CONTINUOUS
`warm_arid` z8 (S NM / W TX) is authored continuous (single long warm season), NOT split. No T1 documents a mid-summer no-plant gap for this higher-elevation z8 band (distinct from the Sonoran low desert's two-season pattern in AZ1005). This mirrors the green-beans warm_arid z8 "bridge" finding. If CC's NMSU read shows a desert-style summer gap at z8, it would split; authored continuous on the evidence in hand. Noted in `plantings_provenance`.

---

## SUCCESSION GEOMETRY (mixed, keyed per-region by continuous-vs-split; second_planting spec v1.1 §4)
- **CONTINUOUS (`succession_continuous` cell string):** northern_tier, ca_interior, ca_north_coast, ca_south_coast, warm_arid, fl_peninsula (inverted), hawaii_tropical.
- **SPLIT (`succession_spring` + `succession_fall` cell strings):** se_gulf, ca_desert, low_desert_az.
- **plantings[] arm shape:** continuous regions = `beginner`(main) + ONE `track:"succession"` cadence arm. Split regions = `beginner`(main) + `track:"succession"` label:spring + `track:"succession"` label:fall. **NO `track:"second_planting"` anywhere** -- that is the cherry NON-succession model; zucchini is `succession_policy.suitable:true`, so the split bands are succession cadence (the lettuce/green-beans model, per CURRENT_STATE locked decision). (Initial draft used second_planting arms; corrected before delivery.)
- **`successions_realized` NOT authored** -- CC derives at release via `derive_realized_successions.py` (A8). The cells carry `succession_continuous`/`succession_spring`/`succession_fall` for the deriver to count; `succession_policy.successions` reconciles to max-over-zones at release.

## DIRECT-SOW-DOMINANT handling (start_method.start == "both")
- `plant_out` = the after-frost direct-sow / set-out window in every region (the cucurbit hero method; squash resents root disturbance, so direct sowing leads once soil >=70F per UMN/UC ANR).
- `start_indoors` populated ONLY where the transplant-for-an-early-crop option genuinely applies: the short-season cold end (northern_tier z3-5; ca_interior z8-9, coastal CA, warm_arid carry a March indoor lead per the CA MG charts). z6-7 and the desert/FL/HI cells leave start_indoors empty (direct-sow only).

## CALENDAR DERIVATION (Step 5.5)
- 13-state enum only; precedence pause > plant > harvest > growing. Verified all 120 cells (10 regions x their zones) -- enum-legal, length 12, 0 `wait` tokens.
- Frost-killed WINTER off-season = `cold_pause` (frost-bracketed z3-10). Frost-free FL summer off-season = `season_over`. Desert/SE mid-summer no-plant gap = `heat_pause` (FLAG 1). Hawaii (frost-free, qualitatively limited) = growing/plant/harvest, no off-season token.
- fl_peninsula = inverted calendar (winter growing season, Jun-Aug season_over), the sharpest inversion; z11 resolved_from null.

## FROST RECONCILE (manual, Step 5)
All frost-bracketed cells' `resolved_from` reconciled byte-exact to `zone_frost_data.json` base zones (z3 May15/Sep15 ... z10 Jan15/Dec31). Frost-free z11 cells (fl_peninsula z11, hawaii z11) carry `resolved_from: {last_frost:"none (frost-free)", first_frost:"none (frost-free)"}`. **A5 note:** several warm-region windows are SOURCE-SET, not last_frost+offset (e.g. se_gulf z8 spring is UGA's Apr middle-GA window, not LF Feb15+offset; ca_desert z9 spring is UC ANR's early-spring window). resolved_from records the frost-date AUDIT; the window rests on its own T1 source. Documented per region in `plantings_provenance`.

## SOURCING (Step 4/5; T1 only, all catalogued parents, 0 mints, 0 non-T1)
10 distinct T1 sources used: umn_ext, umd_ext, iastate_ext (northern_tier); ucanr_ext (ca_interior/north_coast/south_coast/ca_desert); uga_ext (se_gulf); uariz_ext (low_desert_az); nmsu_ext + tamu_agrilife (warm_arid); ufifas_ext (fl_peninsula); uhawaii_ctahr (hawaii). All present in the 122-parent catalog at tier T1. Per-arm + per-cell `anchoring_urls` populated to the SPECIFIC verified page (no homepages). **Source-mint flags: NONE** -- every cited parent was already catalogued; specific pages anchored via the per-arm/per-cell URL (the bare-parent + specific-URL pattern, no sub-id fragmentation needed).

**Per-region anchor pages (verified live this session):**
- umn_ext -> extension.umn.edu/vegetables/growing-summer-squash-and-zucchini
- umd_ext -> extension.umd.edu/resource/growing-summer-squash-zucchini-home-garden
- ucanr_ext -> sfp.ucanr.edu/crops/squash1 (Pub 7245) + ucanr.edu/program/uc-master-gardener-program/time-planting (T13.2) + ucanr.edu/site/uc-marin-master-gardeners/documents/squash-summer
- uga_ext -> secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf
- uariz_ext -> extension.arizona.edu/sites/default/files/2024-08/az1005-2018.pdf (AZ1005)
- ufifas_ext -> gardeningsolutions.ifas.ufl.edu/plants/edibles/vegetables/summer-squash/
- uhawaii_ctahr -> ctahr.hawaii.edu/oc/freepubs/pdf/B-91.pdf
- nmsu_ext -> pubs.nmsu.edu/_circulars/CR457/ ; tamu_agrilife -> aggie-horticulture.tamu.edu vegetable guide
  (NOTE for CC: nmsu_ext/tamu_agrilife pages cited for warm_arid were located via search; CC should confirm the live NMSU CR457 squash row at release and confirm whether it forces a z8 split per FLAG 3.)

## REGION-TIP OVERRIDE (Step-4 rider) -- ATTESTATION
Each editorial tip surface (`tips_by_stage`, `succession_policy.tip_*`) was checked against the regional T1 sources read for this step for a DIVERGENT GROWER ACTION across regions. **No region-tip override is warranted.** Zucchini's core grower actions are universal across zones 3-11: direct-sow once soil >=70F, base-water, harvest young (6-8 in), succession every ~3 weeks, and sow a fall replacement counting back from the frost (or, in the desert/SE, a distinct fall band). What varies by region is the TIMING/structure (continuous vs split, inverted in FL), which is fully expressed in the region windows + calendars, not a different action. The heat-loving trait is encoded architecturally (no mid-season heat pause in the temperate cadence; `pause_in_heat:false`). A timing/structure difference is not a materially different grower action (v1.4 criterion). **Attestation present; 0 PENDING/placeholder overrides.**

## VERIFICATION (Step 5, own-source)
Every window verified side-by-side against its OWN T1 source (A1 -- not "matches lettuce/green-beans"). Where a value converges with another crop, it rests on zucchini's own source. 8-gram source-verbatim scan on authored `plantings_provenance` prose: 0 HARD lifts after rewording one ca_desert run that mirrored UC ANR 7245's "December and January" sentence. Numeric fidelity pass: all sampled windows match cited source months (see fidelity table in bundle).

## WINDOW-STRUCTURE FINDING (the A5 deliverable)
se_gulf was initially mapped continuous but the SOURCE (UGA B577 explicit spring AND fall date columns + C943 "second planting" + "no later than Aug 31") overturned that to SPLIT. ca_interior was confirmed CONTINUOUS by source (UC ANR 7245: production tapers in fall on virus, no mid-summer no-plant gap). This is the A5 rule working as intended: structure is a per-region source finding, not analogy. Final geometry: 7 continuous, 3 split (the 3 hottest-summer regions: SE/Gulf, CA desert, AZ low desert).

## DELIVERABLES
1. `zucchini-courgette_steps4-5.5_authored_slice.json` -- the authored slice (post crop SHA `7cc97e20`).
2. This findings doc.
3. STATE_HISTORY append snippet.
