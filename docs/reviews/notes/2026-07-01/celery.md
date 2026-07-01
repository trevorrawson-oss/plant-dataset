# celery -- author-bot pilot notes (Claude Code lane)

**Output:** `celery_crop.json` (full crop dict, canonical-COMPACT, spliceable byte-for-byte; 63 keys,
10 regions, 20 resolved cells). Slug exactly `celery`. status `author_fresh_pilot`, launch flags
false. Authored FRESH (no carrot content bleed), modeled structurally on certified **carrot**
(Apiaceae, cool-season); the transplant/heat-pause/succession calendar layer modeled on certified
**broccoli**.

## Gate result (scratch splice into the canonical, base SHA 1bc569dc -- 0f6d5af, 50 certified; celery still a shell)
- `python3 tools/whole_crop_gate.py celery <scratch>` -> **GATE: PASS** (exit 0), all A2-A36 + B-G clean.
- `derive_realized_successions.py --check celery` -> **up to date** (exit 0); 20 cells, crop-max 4,
  `succession_policy.successions = max_successions_per_season = 4` reconciled.
- cross_consistency / numeric_sanity / cp_required / coverage_floor / register_completeness
  (dataset-wide) / calendar_basis / verbatim copyright scan -> **celery clean**.
- `release_verify.py` -> **clean, no blocking concerns** (the 2 `wait`-token review notes are the
  reference crop's cells, not celery; celery emits zero `wait` tokens).
- The 38 `calendar_basis` dataset-wide violations PRE-EXIST in the canonical (indoor crops:
  wheatgrass, cilantro-microgreens, ...); celery is NOT among them.

## Key celery-vs-carrot refits (template gives STRUCTURE only; biology re-derived)
- **Long-season TRANSPLANT, not direct-sow.** `start_method.start = "transplant"`, `weeks_indoors = 10`
  (start indoors 8-10 wk before set-out), `days_to_maturity [80,120]` from transplant (mid 100).
  Calendars carry `indoors` tokens (vs carrot's direct-sow). `thinning.needs_thinning = false`
  (set at final 6-10 in spacing as transplants).
- **MOISTURE is the signature.** Heavy, constant, even water is the whole craft: any dry-down ->
  stringy / bitter / hollow / pithy / cracked stalks (irreversible). `water = "High"`,
  `drainage_requirement = "moisture_retentive"`, `organic_matter_preference = "high"`, soil prefers
  water-holding loam/silt loam/muck (the OPPOSITE of carrot's light, open, low-N channel). DROUGHT
  weather-trigger severity raised to `high`.
- **HEAVY FEEDER (high N).** `fertilizer.frequency = "high"`, npk 10-10-10 + nitrogen side-dress
  every 3-4 wk (vs carrot's low-nitrogen). Underfeeding directly toughens stalks.
- **Cold-snap BOLTING (vernalization).** Plant out only AFTER hard-frost danger / prolonged cold:
  ~2+ weeks near or below 50 F vernalizes young transplants -> bolt. Harden off by easing WATER, not
  by chilling. New `COLD_SNAP` weather-trigger + a `bolting` failure-diagnostic. (Consistent with the
  locked rule: bolting is vernalization, NOT photoperiod -> no `gating_factors`.)
- **Blanching + self-blanching vs trench types** carried in varieties/established-stage prose
  (Utah/Pascal green self-blanching, Golden self-blanching, Tango/Conquistador easier).
- **Pests refit:** celery leafminer (Liriomyza), aphids (vector celery mosaic virus), carrot rust fly
  (shared Apiaceae). **Diseases refit:** early blight (Cercospora apii), late blight (Septoria
  apiicola, seedborne, the worse of the two), pink rot (Sclerotinia sclerotiorum), blackheart
  (physiological calcium deficiency, triggered by uneven water). None carried over from carrot.
- **pH 6.0-6.8** (carrot 6.0-6.8 too, but celery's upper-end emphasis is calcium/blackheart-driven).
- **Calendar archetype = inverse-season in warm regions:** cold zones = single summer crop (no
  heat_pause, grows through mild northern summer); warm/hot zones (FL, desert, Gulf, CA interior/
  south) = winter crop with a summer `heat_pause`; cool CA coast = long mild season. Every shown
  heat_pause is backed (months + crop-specific basis + sources). plant_out FILLED in every cell.

## Source ids used (all existing-catalog T1; real celery pages read via WebFetch/WebSearch)
`usu_ext` (USU "Celery in the Garden"), `msu_ext` ("How to Grow Celery"), `uc_ipm` (UC IPM celery:
early/late blight, pink rot, leafminers, aphids, mosaic), `ucanr_santa_clara_mg` (UC MG Santa Clara
celery), `tamu_agrilife` (Aggie-Hort celery), `uf_ifas_vh021` (FL Veg Gardening Guide), `uhawaii_ctahr`.
No T2 (no almanac/johnny/harvest-to-table). No invented ids; no placeholder URLs.

## FLAGS (modeled / judgment calls -- mirrored in verification_status.open_findings, blocks_launch:false)
1. **Regional windows modeled from the NEAREST readable T1 source** + celery biology, not a
   region-specific celery planting chart for all 10 regions: UGA b577 and several state planting-date
   PDFs are SCANNED PDFs that could not be read this session (NOT fetched/extracted per the deny
   rule). Windows are generally-safe; tighten exact months at the variety-delta pass. (finding_001)
2. **hawaii_tropical is lowest-confidence:** celery is marginal in tropical lowland; modeled as a
   cool-season window with a warm-month heat_pause, cited to UH CTAHR generally rather than a
   celery-specific Hawaii calendar. Confirm in review. (finding_002)
3. **Companions are TRADITIONAL/low-medium only** (brassicas, bush beans, alliums as goods; carrot-
   family + fennel as the grounded avoids via documented shared-pest overlap). No celery-specific
   companion trial found in a readable T1 source. (finding_003)
4. **Judgment calls** (finding_004): pH preferred set `[6.0,6.8]` (sources cluster 5.8-6.8, tolerating
   ~7.0; the kickoff hinted 6.0-7.0). `category = "Leafy Greens"` (no stalk/petiole category exists;
   UGA groups celery with leafy petiole vegetables; shell's "Fruiting Veg" was wrong). DTM 80-120 from
   transplant per MSU (some sources give 98-130 from seed). `succession_policy.suitable = true` with
   modest realized counts (2-4) following the broccoli precedent for a long-season cool transplant.

## READ-ONLY honored
Canonical `crops_data_final.json` was NOT modified. All work was on a scratch copy
(`scratch_canonical.json`) under the session scratchpad.
