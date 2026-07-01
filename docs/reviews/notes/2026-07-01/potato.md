# potato -- author-bot pilot notes (Claude Code lane)

Slug: `potato`. Status `author_fresh_pilot`, launch flags both false (DRAFT). Built by FILLING the
shell, modeled on certified **carrot** for the cool-season frost-anchored ROOT calendar SHAPE only;
all biology refit for **Solanum tuberosum (Solanaceae)**.

Output: `potato_crop.json` (this dir). Verified by splicing into a fresh copy of the LIVE canonical
(`_live_spliced.json`):
- `whole_crop_gate.py potato` -> **GATE: PASS** (exit 0; 0 violations across A2-A36 + B-G)
- `derive_realized_successions.py --check potato` -> out of scope (succession suitable=False), up to date
- `release_verify.py` -> **clean** (exit 0)
- `register_completeness_gate.py` (dataset-wide) -> PASS (potato adds 0 unruled prose fields)

## Key potato refits off the carrot template (donor biology NOT kept)
- **Family / rotation:** Solanaceae (Nightshade), `botanical_name` Solanum tuberosum. Rotate 3-4 yr
  AWAY from tomato/pepper/eggplant (shared late blight, early blight, Verticillium). (carrot = Apiaceae.)
- **Propagation:** grown from **certified seed potatoes / cut seed pieces** (1.5-2 oz, 1-2 eyes,
  suberized), NOT true seed and NOT started indoors. `start_method.start="direct"` (planted directly,
  like garlic cloves); `weeks_indoors=0`; hardening-off N/A authored.
- **Hilling** = the signature practice: mound soil over the row as plants grow; prevents tuber greening
  (light -> bitter, mildly toxic **solanine**). Woven through soil_prep, growth_stages
  (vegetative + tuber_initiation), tips_by_stage, container_notes, weather, and a `green_tubers`
  failure diagnostic. (carrot's analog was thinning; potato is NOT thinned -- `thinning` block omitted.)
- **pH 5.0-6.0 (acidic, LOWER than carrot's 6.0-6.8)** to suppress **common scab** (Streptomyces
  scabies; worse above ~pH 5.5 + dry soil + fresh manure). "Do not lime a potato bed." `ph.preferred_range
  [5.0,6.0]`, tolerated `[4.8,6.5]`.
- **Pests (4):** Colorado potato beetle (signature; Leptinotarsa decemlineata), flea beetles, aphids +
  the viruses they vector (PVY/leafroll -> use certified seed), wireworms. (carrot's rust fly / nematode dropped.)
- **Diseases (4):** late blight (Phytophthora infestans -- the historic one), early blight (Alternaria
  solani), common scab, blackleg + bacterial soft rot. Plus physiological hollow_heart, knobby/misshapen,
  no-tubers in failure_diagnostics.
- **Frost-TENDER foliage** (cool-season tuber but tops killed by hard frost): cold zones = single SPRING
  crop; mild/hot zones = fall-through-winter crop. **Tubers set best ~60-70°F soil**, fall off in heat ->
  warm-region summers are heat_pause.
- Numbers: spacing **10-12 in** (rows 30-36), DTM **70-120** (mid 100), depth 3-5 in, germ/plant soil
  **50-70°F** (plant ~2-4 wk before last frost), NPK **10-10-10** (moderate feeder, avoid excess N + manure).
  Harvest when tops die back; new potatoes ~7-8 wk.

## No-perfect-template modeling (how carrot was used, and where it was abandoned)
- KEPT from carrot: the `cool_season_annual` / `frost_anchored` archetype, the 10-region/zone roster and
  per-cell calendar shape, the dual-register prose pattern, the rich companion-provenance + pest/disease +
  growth-stage + tips objects, and the heat_pause-object pattern for warm regions.
- ABANDONED: succession (carrot succession-wells; **potato is NOT a succession crop** ->
  `succession_policy.suitable=False`, so NO `successions_realized`/`succession_spring/fall` on any cell,
  no thinning, no overwintering-in-ground harvest). Frost behavior INVERTED: carrot tolerates frost and
  sweetens; potato tops are frost-killed.
- Calendars were **derived deterministically** with `tools/annual_calendar.derive_annual_calendar`
  (plant_out + harvest + heat_pause_months), never hand-authored, so A5/A24/A28 coherence holds by
  construction. 12 of 20 cells carry a backed heat_pause.

## Regional calendar sourcing (per region)
- **SOLID T1 (verified live this session):** northern_tier spring windows (UMN early-April Twin Cities,
  Iowa State early-mid April, UMaine); se_gulf spring (Clemson Feb-Mar coastal / Mar-Apr Piedmont, fall
  NOT recommended in SC; UGA mid-late Feb); **all four CA regions** keyed to **UC IPM** exact months
  (north coast Feb + Apr-May; south coast Feb-Aug; interior Feb-Mar + Aug; desert Dec-Feb); fl_peninsula
  (UF/IFAS: Jan statewide, Oct-Jan S FL).
- **MODELED (flagged, see open_findings):**
  - **warm_arid (NM):** NMSU CR457B confirms 102-day maturity + 4-in depth, but NOT month windows;
    spring+fall windows modeled on the regional cool-season pattern.
  - **low_desert_az:** UA `IrishPotatoes.pdf` is an **image-only PDF, NOT machine-readable** -> FLAGGED,
    cited as the real publication, windows modeled (Jan-Feb spring + Sep fall, summer heat gap).
  - **hawaii_tropical:** CTAHR B-91 is **PDF-only** -> FLAGGED; potato modeled as a cool-season /
    elevation crop (Oct-Dec plant, Jan-Apr harvest, warm-lowland summer = heat gap).

## Source set (all cataloged + T1, all anchor URLs verified live 2026-06-30)
umn_ext (growing-potatoes + Colorado-potato-beetle), umaine_ext (Bulletin 2077), clemson_hgic (potato
factsheet + Irish/sweet-potato diseases factsheet -- BOTH cited under the single cataloged id
`clemson_hgic`, with the right per-claim URL in anchoring_urls), uga_ext (C1011, via fieldreport.caes
redirect), iastate_ext (planting-potatoes-home-garden, via redirect), uf_ifas (Gardening Solutions
potatoes), uf_ifas_south_cal (EP452), uc_ipm (cultural-tips-for-growing-potato), nmsu_ext_cr457b (CR457B),
auburn_aces (harvest guide -- already in catalog for potatoes), uariz_ext (PDF, flagged),
uhawaii_ctahr_b91 (PDF, flagged).

## Flags carried in `verification_status.open_findings` (all blocks_launch=false)
1. **finding_001** -- modeled regional windows for warm_arid / low_desert_az / hawaii_tropical
   (PDF-only / pattern-based sources); source-truth review.
2. **finding_002** -- aphid/virus + flea-beetle + wireworm pests cited at the comprehensive UMN/Clemson
   potato PAGE level (which name them) rather than pest-specific factsheets; CPB has the dedicated UMN
   page. Recommend a source-truth sample of the aphid/virus entry.
3. **finding_003** -- heat_pause thermal backing anchored to potato cool-tuber physiology (UC IPM,
   cool-weather crop; cool-season-only desert/FL calendars) + each region's planting source, rather than
   a single numeric soil-temp ceiling (no fetched T1 home-garden page stated ~80°F explicitly; the 60-70°F
   optimum is broadly established). Per-region heat-month boundaries are modeled; revisit at the
   variety/precision pass.

## Judgment calls
- se_gulf kept SPRING-ONLY (Clemson/UGA are spring; SC explicitly discourages fall) with a summer
  heat_pause + winter cold_pause; the Gulf-Coast fall option is noted in prose but NOT given a fall plant
  window (would be unsourced).
- `germination_temp_f [50,70]` is the sprouting/planting **soil** temp (potato has no true-seed
  germination); clarified in description.
- `heat_threshold_temp_f` set to 80°F **soil** (vs carrot's 75°F air), hedged in basis as variety-dependent.
- Two `wait`-token review notes in `release_verify` belong to OTHER crops (pre-existing); potato is
  frost_anchored and carries **zero** `wait` tokens.

## IMPORTANT environment note for Trevor (not caused by this task)
During this session the repo was **advanced concurrently** by another session: HEAD moved from `7b20d73`
to `0f6d5af` ("bok-choy -> ALL 50 CERTIFIED"), and `crops_data_final.json` + `LATEST.txt` moved from
`ed8abc66...` (session start, per the CURRENT_STATE I read) to **`1bc569dc...`** (now). The working tree
is clean and matches HEAD. I verified potato against this CURRENT live canonical. I did **not** write to
`crops_data_final.json` (confirmed: `git diff` shows it unchanged vs HEAD; my scripts only target scratch
paths). Also note `tools/berries_woody_gate.py` shows as locally modified -- that change is NOT mine.
Heads-up only: CURRENT_STATE.md in my read context (22 certified + 28 drafts) is now stale relative to
the live "all 50 certified" state.

## Integration
`potato_crop.json` is a complete DRAFT record (62 top-level keys, 10 regions / 20 cells). Apply it over
the existing potato shell in the live canonical, then queue for the daily biology-fidelity review
(prioritize the 3 flagged findings). Expect a correction loop -- that is the workflow.
