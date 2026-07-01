# jalapeno -- author-fresh pilot NOTES

Session: `jalapeno_author_fresh_pilot` (2026-06-30, Claude Code lane, web access).
Output: `jalapeno_crop.json` (compact canonical) + `jalapeno_crop.pretty.json` (review) +
`build_jalapeno_p1..p5.py` (the deterministic builder, run in order).
Base canonical SHA: `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5` (READ-ONLY,
untouched -- verified byte-identical after the run, matches LATEST.txt).

## What this is
Gold-standard FILL of the existing `jalapeno` SHELL, structurally mirrored on the certified
`cherry-tomato` (Solanaceae, `warm_season_fruiting` / `frost_anchored`) and the gate-clean
`eggplant` pilot (same region/calendar harness). Structure borrowed; EVERY biological value
re-derived for jalapeno (Capsicum annuum, HOT pepper). Slug exactly `jalapeno`. 52 top-level keys
(exact key-set parity with the shell: 0 missing, 0 extra).

## Key jalapeno refits (cherry-tomato/eggplant = STRUCTURE ONLY; biology re-derived)
| dimension | refit for jalapeno |
|---|---|
| PUNGENCY (the signature) | capsaicin ~2,500-8,000 Scoville, produced on the placenta; heat RISES with maturity (red hotter than green) AND with plant/water stress. Woven through description, harvest_ready, watering, fertilizer, varieties, tips, failure_diagnostics. |
| harvest | pick GREEN (firm, dark/black-green, ~70-80 days from transplant) OR ripen RED (+2-3 wk) for more heat + sweetness. `harvest_urgency` medium (not high like eggplant). |
| corking | tan striping/netting on a mature pod is a PRIZED ripeness/vigor sign, NOT a defect (dedicated failure_diagnostic + prose). |
| heat response | heat-SENSITIVE like tomato (NOT heat-loving like eggplant): blossom drop + paused fruit set above ~90F day / 75F night -> backed heat_pause in the hot/desert cells. |
| pests | Aphids (+ mosaic viruses they vector), Flea beetles, Pepper maggot (Zonosemata electa; jalapeno's thin walls largely spare it), Pepper weevil (Anthonomus eugenii, South/SW), Hornworms. NOT eggplant's Colorado potato beetle / lace bug. |
| diseases | Bacterial spot, Mosaic viruses (CMV/TMV), Phytophthora blight (P. capsici), Anthracnose. NOT verticillium/phomopsis. |
| pH | 6.0-6.8 (Clemson 6.0-6.5 sweet spot; tolerated 5.5-7.5; peppers grown on alkaline Western soils). |
| spacing | 12-18 in in rows 24-36 (Clemson 12, ISU 18, UMD 12-24). |
| feeder | MODERATE (Clemson/UMD "medium"), not heavy; hold N back before fruit set (else leaf, no pods). |
| self-fertility | self-fertile, self-pollinating (one plant sets fruit). |
| storage | KEEPS + preserves better than eggplant: fridge 1-2 wk; freezes with NO blanching; red pods dry, and smoke-dried red jalapenos = chipotles. |
| handling | wear GLOVES: capsaicin oil burns skin/eyes (harvest_ready, tips, storage). |
| varieties | heat/mildness axis: Jalapeño M (standard), Early Jalapeño (cool-season), Mucho Nacho (large hybrid), TAM Mild (Texas A&M, low heat), Biker Billy (very hot), Purple Jalapeño (compact/container). |
| container | best-of-peppers container crop (compact); 3-5 gal, 10 in deep. |
| overwintering | N/A as annual, but note peppers are tender perennials -> optional indoor overwinter of a potted plant (honest hedge). |

## Calendar / heat_pause handling (the KEY differentiation from eggplant)
Full 10-region roster, zones 3-11, non-empty 12-token calendars DERIVED by `tools/annual_calendar.py`
from authored windows (guarantees A5/A24/A37 coherence). Warm-season Solanaceae shape: winter
`cold_pause`, spring transplant into warm soil, continuous summer-to-frost harvest.

Jalapeno is heat-SENSITIVE like tomato, so it carries a backed `heat_pause` in the SAME 8 cells as
the certified cherry-tomato: **se_gulf z8/z9, ca_desert z9/z10, warm_arid z8, low_desert_az z9,
fl_peninsula z10/z11** -- where fruit set fails above ~90F day / 75F night and the crop splits into a
spring and a fall flush. This footprint match is INDEPENDENTLY DERIVED (peppers share tomato's
blossom-drop physiology, sourced to NMSU H-240 "blossoms may not set above 90F" and UMD "evening
temps above 75F slow or stop pod production"), not pasted. Pause MONTHS were re-derived per cell:
se_gulf [7,8], deserts [6,7,8], fl [6,7,8] (jalapeno slightly more heat-sensitive than tomato +
FL's wet season) -- so they differ from tomato in several cells. ca_interior carries NO pause
(continuous, mirrors tomato: Central Valley set is transiently reduced, not blocked, with irrigation).

## Gate result (spliced into a SCRATCH copy of the canonical; canonical untouched)
- `python3 tools/whole_crop_gate.py jalapeno scratch_jalapeno.json` -> **GATE: PASS (exit 0)**; all
  A2-A37 zero violations. **A37 calendar-coherence: 0** (no growing-after-harvest, no harvest-hole --
  the heat_pause converts the hot-region summer lull to a walk-through token, so no A37 lines to
  report). B dual-voice: populated CP 140 / SP seasoned-only 16 / null_values 0. C/D dash+temp: 0.
  E: 19 distinct IDs / 0 uncatalogued / 0 non-T1. F anchoring: 48 leaves / 0 gaps. G flip-state
  `author_fresh_pilot`, 0 launch blockers.
- `tools/release_verify.py scratch_jalapeno.json --base crops_data_final.json --slug jalapeno --ref cherry-tomato`
  -> **RELEASE-VERIFY: clean (exit 0)**; only jalapeno changed, cherry-tomato byte-identical, no new
  violations. ONE non-blocking Step-5.5 note (G): `ca_desert z9/z10 heat_pause.months=[6,7,8]` is
  value-identical to cherry-tomato's -- ATTESTED independently derived (Jun-Aug is the desert's
  universal extreme-heat window for any warm-season fruiting crop), NOT pasted.
- `tools/derive_realized_successions.py --check` -> **up to date (exit 0)** (succession_policy.
  suitable=false, so no successions_realized authored -- A8 clean).
- `tools/verbatim_scan.py jalapeno` -> **0 HARD hits, 0 borderline** across 314 prose strings (all
  original copy). Temperatures render `°F` (75 occurrences); 0 em-dash, 0 spelled "degrees F".
- Canonical SHA after the run == base SHA (READ-ONLY honored).

## Sourcing (all EXISTING catalog T1 IDs; 19 distinct; 0 uncatalogued, 0 non-T1)
Core biology source-verified LIVE this session by WebFetch/WebSearch:
- **clemson_hgic** -- Clemson HGIC "Pepper" (pH 6.0-6.5; spacing 12 in/rows 3 ft; DTM 70-85 from
  transplant / 100-120 from seed; moderate feeder, side-dress calcium nitrate; harvest black-green;
  jalapeno 2,500-8,000 SHU).
- **umn_ext** -- UMN "Growing peppers" (start ~8 wk; heat mat 80-90F; transplant after nights >50F;
  black plastic mulch).
- **umd_ext** -- UMD "Growing Peppers in a Home Garden" (spacing 12-24 x 30-36; 8-10 wk transplants;
  soil 65F or plants "just sit there"; MEDIUM feeder; evening temps >75F slow/stop pod production;
  anthracnose/bacterial spot/viruses/BER/sunscald).
- **iastate_ext** -- Iowa State "Growing Peppers" (spacing 18 in/rows 24-30; 6-8 wk; full sun 6h;
  70-85F optimum).
- **ncsu_ext** -- NC State "Pests of Pepper" (green peach aphid + virus vector; flea beetles;
  pepper maggot Zonosemata electa; pepper weevil Anthonomus eugenii; tobacco hornworm).
- **nmsu_ext** -- NMSU H-240 / H-230 / Chile Pepper Institute (blossoms fail to set below 60F or
  above 90F; capsaicinoids on the placenta; environmental stress raises pungency; corking = tan
  stretch marks prized in markets).
- **tamu_agrilife** -- Texas A&M AgriLife "Is that chile pepper hot or not?" (jalapeno 2,500-10,000
  SHU; TAM mild jalapeno bred lower-heat + disease resistant at Texas A&M).
- **uc_ipm** -- UC IPM "Pepper Weevil" (sanitation/rotation; Anthonomus eugenii).
- **umass_ext** + **rutgers_njaes** -- pepper maggot (damage NEGLIGIBLE on thin-walled jalapeno).
Regional planting-window cells anchor to institution-level extension portals (uga_ext / uga_c963,
ucanr / uc_mg, nmsu, tamu, ufifas / uf_ifas_vh021, uariz_ext_az1005, uhawaii_ctahr) + uwi_hort for
containers -- same pattern as the eggplant pilot. NEVER used curl/wget/pip/pdftotext.

## FLAGS (verification_status.open_findings, all blocks_launch=false, modeled-and-flagged)
1. `jalapeno_pilot_regional_calendars_modeled` -- per-zone windows MODELED from DTM + crop-invariant
   frost anchors + representative extension dates; not each source-verified vs a live regional pepper
   calendar.
2. `jalapeno_pilot_heat_pause_footprint_matches_tomato` -- same 8 heat_pause cells as cherry-tomato,
   INDEPENDENTLY derived from shared blossom-drop physiology (NMSU/UMD-sourced); months re-derived
   per cell. release_verify may flag value-identical months -- attested independent.
3. `jalapeno_pilot_ca_interior_no_pause` -- Central Valley modeled continuous (mirrors tomato); a
   severe summer may show more midsummer blossom drop than the calendar implies.
4. `jalapeno_pilot_dtm_green_from_transplant` -- DTM [70,80] = GREEN from transplant; red +2-3 wk and
   ~100-120 from seed carried in prose, not the numeric field.
5. `jalapeno_pilot_ph_range` -- [6.0,6.8] (first prose range matches for A34); tolerated [5.5,7.5]
   honors Western alkaline-soil chile culture.
6. `jalapeno_pilot_variety_dtm_and_scoville_modeled` -- variety DTM + Scoville framing from
   breeder/seed-catalog norms + the sourced TAM (1,000-3,500 SHU) and standard jalapeno figures.
7. `jalapeno_pilot_gloves_handling_tip` -- wear-gloves/capsaicin-oil tip is universal food-safety
   guidance carried in prose but not pinned to a single fetched T1 page this session.
8. `jalapeno_pilot_regional_source_anchors_general` -- several regional cells anchor institution-level
   portals rather than a pepper-specific regional planting-date page read this session.
9. `jalapeno_pilot_hawaii_window_modeled` -- hawaii z11 broad frost-free default; catalogued CTAHR
   sources are scanned/image PDFs not WebFetch-readable. No fabricated source.

## Status / next
`status="author_fresh_pilot"`, `launch_ready_core=false`, `launch_ready_seasoned=false`. NOT
launch-ready: queued for the daily biology-fidelity review + a per-region source-truth sample to
confirm the modeled regional windows, the heat_pause footprint/months, the ca_interior no-pause
call, and variety DTM/Scoville before any flip. Promotion to canonical is a separate Trevor-gated
step.

## Authoring note
Heeded the pumpkin/eggplant trailing-comma lesson: `isinstance(..., str)` asserts on
`harvest_ready_seasoned`/`harvest_ready_beginner` in the builder (a stray trailing comma that shipped
a 1-tuple was caught and fixed before the gate run).
