# cantaloupe -- author_fresh_pilot NOTES (2026-06-30, Claude Code lane, web access)

Filled the `cantaloupe` shell. Structural template: certified **zucchini-courgette** (cucurbit
shape, dual-register pattern). Biology analog: certified single-harvest melon **watermelon**
(warm_season_fruiting, frost_anchored, no-heat_pause melon calendar model). Every biological value
RE-DERIVED for cantaloupe (Cucumis melo, reticulatus group / muskmelon) from T1 extension sources;
nothing carried from the donors' biology.

## The two load-bearing refits

**1. FULL SLIP single-harvest model (the signature harvest cue).** Cantaloupe is harvested once per
fruit, at ripeness, and the defining cue is **full slip**: press the thumb against the stem where it
joins the fruit and a ripe melon lets the stem separate cleanly, leaving a smooth round dished scar
(no twisting/pulling). Read alongside the supporting signs that come on in the last few days: coarse,
raised, corky **netting**; background skin shifting **green to tan/buff** under the net; a **sweet
musky aroma** at the stem end; and the **nearest tendril browning**. Modeled honestly: cantaloupe
does **not gain sugar off the vine** (it softens and grows more aromatic on the counter, but sweetness
is set at harvest), so pick at full slip for peak flavor; a melon held/shipped can be taken a hair
early at half slip. `harvest_urgency: moderate` -- a full-slip melon over-ripens on the vine within a
day or two, so the guidance is to check daily as slip nears. This cue is wired through
`harvest_ready_*`, the `harvest` growth_stage, `tips_by_stage.harvest`, the `harvest_ripeness`
notification, `failure_diagnostics` (bland melon = picked before full slip / over-watered), and
`storage`. (Distinct from watermelon, which slips NOT at all and reads by tendril + ground spot +
dull thump.)

**2. CUCUMBER BEETLE -> BACTERIAL WILT high susceptibility (the melon-specific danger).** The sharpest
divergence from the watermelon analog: cantaloupe/muskmelon is **among the most bacterial-wilt-
susceptible cucurbits**, far more than watermelon, which is nearly immune (UMD: cantaloupe/cucumber
"much more susceptible," watermelon "almost immune," squash "moderately susceptible"). Bacterial wilt
(Erwinia tracheiphila) is vectored by striped/spotted cucumber beetles, overwinters in the beetle gut,
and infects seedlings most readily (through the ~5-leaf stage), so early beetle exclusion is "the whole
game." This is authored as its own **disease entry** (bacterial wilt) PLUS elevated cucumber-beetle
severity in the pest entry, the `seedling` growth_stage/tip, the new `beetle_wilt_watch` notification
(severity `warning`), and a failure_diagnostic. Rotation is explicitly noted NOT to help bacterial wilt
(it comes from beetles, not soil), unlike the soilborne Fusarium wilt. Other pests refit as melon-
appropriate: aphids (vector CMV/WMV/ZYMV), spider mites (hot/dry), squash bug (minor, prefers squash),
squash vine borer (rarely attacks melons -- growing cantaloupe is most of the prevention). Diseases:
bacterial wilt, powdery mildew, downy mildew, Fusarium wilt (f. sp. **melonis**, muskmelon-specific,
not watermelon's niveum), gummy stem blight, Alternaria leaf blight.

## Other refit biology (re-derived, not donor-copied)
- pH 6.0-6.8 pref / 5.8-7.5 tol; spacing_inches [24,36] (in-row/hill; rows 5-6 ft in prose); DTM
  [75,90] mid 82; germination 70-95F, plant at soil 65-70F; weeks_indoors 3; sunlight 8-10 hr; water
  1-2 in/week with a deliberate dry finish to sweeten; 5-10-10 pre-plant + N sidedress before vines run
  and after bloom, ease off N after set.
- **self_fertile: true, monoecious** -- a single standard variety fruits on its own (bees required);
  NO seedless/triploid pollinizer complication (deliberately contrasted with watermelon in prose).
- Varieties re-picked for cantaloupe with per-variety DTM: Hale's Best (86), Ambrosia (86), Athena (80,
  disease-tolerant SE pick), Hearts of Gold (90), Minnesota Midget (65, short-season/container),
  Sarah's Choice (76).
- Calendars: full 10-region roster, 3-11, 12-token calendars, `plant_out` filled, successions
  CC-derived low (single long-season crop, suitable:false), heat-loving so **no heat_pause** (produces
  through southern/desert summer; FL/AZ hottest cells split spring/late-summer for crop turnover, same
  physiology call as the certified watermelon).

## Gate result (whole_crop_gate + register + release_verify on scratch splice)
- **whole_crop_gate: all of A2-A36 + B-G = PASS (0).** Source-tier: 14 distinct IDs, 0 uncatalogued,
  0 non-T1. Dash/temperature: 0. Anchoring: 0 gaps. Register-fill: 0.
- **register_completeness_gate: PASS** (0 unruled prose fields).
- **release_verify: clean** (its 2 `wait`-review notes are reference-crop cells, not cantaloupe).
- **A37 calendar-coherence: 3 lines -- REPORTED, NOT hand-fixed** (per the kickoff's A37 note ->
  normalized centrally):
  - `fl_peninsula.z10 Jul: growing not reachable from a plant/indoors (traces back to harvest)`
  - `fl_peninsula.z11 Jun: growing not reachable from a plant/indoors (traces back to harvest)`
  - `fl_peninsula.z11 Jul: growing not reachable from a plant/indoors (traces back to harvest)`
  These are the double-crop midsummer growing-bridge months between the spring and fall Florida crops
  (disease/rain gap, not heat). The central A37 normalizer resolves exactly this class -- confirmed
  against the current-canonical watermelon, whose identical FL bridges were normalized `growing ->
  season_over` (z10 Jul; z11 Jun+Jul). Left in the authored form deliberately; everything else gates
  to PASS.

## Sources (existing catalog T1 only; a source ID may carry different page URLs per claim, per the
## certified watermelon `clemson_hgic` precedent)
- clemson_hgic -- Cantaloupe & Honeydew Melons (soil temp, spacing, seed depth, 5-10-10 + sidedress,
  full slip, varieties)
- umn_ext -- Growing melons (pH 6.0-6.5, sandy loam, transplants, watering/taper, netting/color signs,
  <90-day varieties for the North) + UMN Bacterial wilt page (Erwinia, beetle vector, susceptibility)
- usu_ext -- Cantaloupe in the Garden (soil 65F, mounds/rows, 35-45 days from flowering, taper water,
  slip harvest, storage)
- uga_ext -- B1179 Cantaloupe & Specialty Melons (pH 6.0-6.5, spacing, powdery/downy mildew, Fusarium
  f.sp. melonis, gummy stem blight, Alternaria, beetle/aphid thresholds)
- iastate_ext -- Growing Cantaloupe/Muskmelon (hills/rows, soil 60-70F, transplant 3-4 wk, watering,
  full slip + flower-end softness + aroma, store 36-45F, disease/virus list, varieties)
- umd_ext -- Growing Melons (regional) + Striped Cucumber Beetles & Bacterial Wilt (the susceptibility
  ranking: cantaloupe >> watermelon)
- Region planting-calendar anchors reused from the certified watermelon roster (all catalogued T1):
  ucanr_ext, uc_mg, nmsu_ext, tamu_agrilife, uariz_ext, ufifas_ext, uf_ifas_vh021, uhawaii_ctahr.

## Flags / open_findings (all blocks_launch:false, status accepted -- draft, not launch-ready)
1. **Regional calendars MODELED** from DTM + shared frost anchors + representative extension dates;
   per-zone dates not each source-verified (daily biology review + per-region source-truth sample
   should confirm before any flip).
2. **pH preferred set to 6.0-6.8** while the two strongest cited sources (UMN, UGA) give a 6.0-6.5
   sweet spot; prose leads with the sourced 6.0-6.5 and states the broader 6.0-6.8 muskmelon band.
3. **spacing_inches [24,36]** carries in-row/hill spacing; wide row spacing (5-6 ft) is in prose (the
   numeric is placeability, same convention as watermelon's capped spacing).
4. **northern_tier z3-z4 + ca_north_coast MARGINAL** (cool-summer North / foggy coast) -- honest
   best-case short-season windows (early varieties + transplants + black plastic mulch); flagged, and
   the region_notes carry the warning, not encoded as unsuitable.
5. **No heat_pause modeled** (heat-loving; FL deep-summer gap is disease/rain-driven, represented as a
   growing bridge -> the A37 lines above; central normalizer handles it, a bare heat_pause would be
   rejected by A28).
6. **hawaii_tropical z11** is a broad frost-free default (catalogued CTAHR source is a scanned PDF, not
   WebFetch-parseable -- same honest broad default as watermelon; no fabricated source).

No fabricated sources or invented source IDs. Canonical `crops_data_final.json` untouched (read-only);
work done on a scratch splice.
