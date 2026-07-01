# cayenne-pepper -- author-fresh pilot NOTES

Session: `cayenne_pepper_author_fresh_pilot` (2026-06-30, Claude Code lane, web access).
Output: `cayenne_pepper_crop.json` (compact canonical) + `cayenne_pepper_crop.pretty.json` (review) + `build_cayenne.py` (the deterministic builder).
Base canonical SHA: `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5` (READ-ONLY, untouched -- verified byte-identical after the run).

## What this is
Gold-standard FILL of the existing `cayenne-pepper` SHELL, structurally mirrored on the certified
`cherry-tomato` (same family, Solanaceae; `warm_season_fruiting` / `frost_anchored`) and the gate-clean
`eggplant` author-fresh pilot (same archetype + region/calendar build harness). Structure was borrowed;
EVERY biological value was re-derived for cayenne pepper (Capsicum annuum, hot cayenne type). Slug exactly
`cayenne-pepper`. 52 top-level keys (matches the shell key set exactly; asserted in the builder).

## Key cayenne-vs-tomato refits (cherry-tomato = STRUCTURE ONLY; biology re-derived)
| dimension | cherry-tomato (donor) | cayenne (re-derived) |
|---|---|---|
| fruit | round red cherry fruit | **thin-walled, tapering pod, 4-6 in, curved/wrinkled, waxy green -> bright RED** |
| heat | mild/sweet | **~30,000-50,000 Scoville (extension ~25,000-50,000); several times hotter than jalapeno (~2,500-8,000)** |
| signature use | fresh eating | **harvested RED and DRIED: strung/hung or dehydrated, then ground into cayenne powder; gloves for capsaicin oils** |
| feeder | high-K at flowering | **MODERATE feeder; the cardinal rule is go easy on nitrogen (excess N -> leaf, few pods)** |
| DTM | [55,70] from transplant | **[70,80] from transplant to GREEN; ~90-100 to red-ripe for drying (prose + flag)** |
| germ | [70,85] | **[70,90]** (UMN heat mat 80-90, ideal soil 70; UC MG optimum ~65-85, max 95) |
| spacing | [24,36] | **[18,24]** in-row (UMN 18 in / rows 30-36; Iowa/PSU 18 in / rows 24-30) |
| pH | 6.0-6.8 | **6.0-6.8** (PSU best yields 6.0-6.8; Clemson/UGA 6.0-6.5); first prose range matches structured for A34 |
| habit | indeterminate, needs staking | **compact, self-supporting, NO staking; excellent container crop (5-gal)** |
| pests | hornworm/aphid/BER | **aphids (virus vectors) lead; flea beetle (seedlings); pepper maggot + pepper weevil (warm South; cayenne LOW-susceptibility, thin-walled); hornworm; cutworms** |
| diseases | early/late blight, septoria | **bacterial leaf spot, mosaic virus complex, Phytophthora blight, anthracnose (ripe-fruit rot, matters for red drying), + physiological blossom-end rot** |
| varieties | cherry-tomato cultivars | **Long Slim Cayenne, Large Thick Cayenne, Carolina Cayenne, Super Cayenne II, Charleston Hot (extension-confirmed)** |
| overwintering | N/A (annual) | **container_notes.overwintering.applicable=True: cayenne is a tender perennial; a potted plant can overwinter indoors (optional)** |
| succession | one long-season planting | **one long-season planting (suitable:false, 1); prolific over the season** |

## Calendar handling
- Full 10-region roster, zones 3-11, non-empty 12-token calendars, DERIVED by `tools/annual_calendar.py`
  from authored windows (guarantees A5/A24/A37 coherence). Warm-season Solanaceae shape: winter
  `cold_pause`, spring transplant into warm soil (>= 60-65F), long CONTINUOUS summer-to-frost `harvest`.
- **THE HEAT-PAUSE REFIT (differentiation from tomato):** cayenne, a hot pepper, is somewhat MORE
  heat-tolerant than tomato, so it RUNS THROUGH the upper-Gulf (`se_gulf` z8) and warm-arid (`warm_arid`
  z8) summers that pause cherry-tomato. It carries a backed `heat_pause` (A28: months + basis_seasoned +
  URL-anchored source) in **6 cells** vs tomato's 8: the true low deserts (`ca_desert` z9/z10 [6,7,8],
  `low_desert_az` z9 [7,8]) and the deep-Gulf / peninsular-Florida humid heat (`se_gulf` z9 [7,8],
  `fl_peninsula` z10/z11 [7,8]), where sustained days above ~90F and nights above ~75F drop pepper
  flowers and stop pod set. The thermal basis cites UMD "Poor Blossom and Fruit Set" + "Growing Peppers"
  (evening temps above 75F slow/stop pepper pod production). Modeled + flagged.
- **Persisting-plant vs replant:** desert + `se_gulf` z9 cells model ONE spring planting whose pod set
  pauses through the heat and resumes in fall (peppers are tender perennials that persist). `fl_peninsula`
  cells model a spring + a fall REPLANT (Florida grows peppers as a fall/winter/spring crop, replanting
  around the disease-heavy, hot midsummer). Both are region-appropriate and noted in region_notes.
- **Cool cells marginal for RED (flagged):** `northern_tier` z3/z4 and cool/foggy `ca_north_coast` grow
  cayenne but the long warm runway red pods need for drying is short; region_notes honestly hedge that
  growers pick more green than fully red there.

## Sourcing (all EXISTING source_catalog IDs; all T1; gate E: 19 distinct IDs, 0 uncatalogued, 0 non-T1)
Core biology + real pepper URLs source-verified LIVE this session by WebFetch/WebSearch:
- **clemson_hgic** Pepper (DTM 70-85 transplant / 100-120 seed; pH 6.0-6.5; start 6-8 wk; side-dress
  calcium nitrate; over-N -> foliage few fruit; hot peppers green or ripened, whole plants pulled/hung
  before frost; cayenne cultivars Carolina Cayenne/Charleston Hot/Long Slim Cayenne/Super Cayenne II;
  jalapeno 2,500-8,000 SHU; BER from Ca/water; store 45-50F 2-3 wk).
- **umn_ext** Growing peppers (start ~8 wk; germ 80-90F, ideal soil 70F; transplant nights >50F; spacing
  18 in / rows 30-36; over-N -> bushy leafy; 1 in/wk; BER; harvest green or colored).
- **umd_ext** Growing Peppers (DTM 70-85; sun 6-10 hr; start 8-10 wk; soil <65F "just sit there") +
  Poor Blossom & Fruit Set (nights <60F/>75F, day >95F drop flowers -> the heat_pause backing) + Hornworm.
- **psu_ext** Growing Hot Peppers (cayenne 25,000-50,000 SHU; stress raises heat) + Preserving Those
  Colorful Garden Peppers (string/hang red pods 3-4 wk; dehydrator 140F->130F; grind to cayenne powder;
  store airtight cool dark; wear gloves).
- **ncsu_ext** Pests of Pepper (flea beetle; pepper maggot -- LOW on thin-walled cayenne; pepper weevil;
  green peach aphid vectors viruses; hornworm) + Bacterial Spot + Phytophthora Blight + Anthracnose +
  Blossom-End Rot + Root-Knot Nematodes (Carolina Cayenne resistant).
- **iastate_ext** Growing Peppers (18 in / rows 24-30; ~15-20 lb/10-ft row) + Crop Rotation (Solanaceae 3-4 yr+).
- **ufifas_ext** Peppers by Scoville Units (cayenne 25,000-50,000; jalapeno 2,000-8,000) + VH054 pepper virus/disease.
- **uc_ipm** peppers flea beetles / pepper weevil / verticillium; **uc_mg** seed germination temps.
- **usu_ext** peppers (1-2 in/wk, drip, critical at fruit set); **msu_ext** Michigan Fresh Hot Peppers
  (fully colored hotter/sweeter; dehydrate + crush to store; fridge 2-3 wk; freeze raw no blanch).
- **uga_ext** C1005 Home Garden Peppers (70-85 days; pH 6.0-6.5; soil 70F/nights 50F to plant; 8-10 hr sun).
Regional planting-window cells anchor institution-level extension portals (ucanr/uc_mg, nmsu/tamu,
uariz_az1005, ufifas/uf_ifas_vh021, uhawaii_ctahr, uga) -- same pattern as the eggplant pilot.

## Gate result (spliced into a SCRATCH copy of the canonical; canonical untouched)
- `python3 tools/whole_crop_gate.py cayenne-pepper scratch_cayenne.json` -> **GATE: PASS (exit 0)**; all
  A2-A37 zero violations. **A37 (calendar-coherence) = 0 -- no A37 lines to report** (the eggplant-style
  contiguous windows + growing-toward-harvest desert/FL splits derive clean; NOT hand-fixed, genuinely 0).
  B dual-voice: populated CP 148 / SP seasoned-only 15 / null_values 0. C/D dash+temp: 0 user-facing hits.
  E: 19 distinct IDs / 0 uncatalogued / 0 non-T1. F anchoring: 48 claim-leaves / 0 gaps. G flip-state
  `author_fresh_pilot`, 0 launch blockers.
- `tools/release_verify.py scratch_cayenne.json --base crops_data_final.json --slug cayenne-pepper --ref cherry-tomato`
  -> **RELEASE-VERIFY: clean (exit 0)**; only cayenne-pepper changed among crops, cherry-tomato byte-identical,
  no new violations (the long "cleared" list is the shell's null fields now filled). ONE non-blocking Step-5.5
  review note (G): 5 heat_pause.months are value-identical to cherry-tomato's -- **ATTESTED independently
  derived** (Jun-Aug in the CA/AZ deserts and Jul-Aug in the deep-Gulf/FL are the peak-heat windows for ANY
  warm-season crop, and I derived them from pepper-specific fruit-set physiology via UMD; note the
  differentiation is real -- I dropped se_gulf z8 + warm_arid z8 that tomato pauses, and se_gulf z9 uses
  [7,8] vs tomato's [7]).
- `tools/calendar_coherence_gate.py scratch_cayenne.json` -> 0 growing-after-harvest + 0 harvest-hole.
- `tools/derive_realized_successions.py --check scratch_cayenne.json` -> **up to date (exit 0)**
  (out of scope: `succession_policy.suitable=false`, so no `successions_realized` authored -- A8 clean).
- Temperatures render as `°F` (71 consumer occurrences); 0 bare "F"/spelled "degrees F", 0 em-dash, 0 `--`,
  0 mid-sentence "Plant" in consumer copy (bare-F/`--` appear ONLY in the backend verification_status
  metadata, which is is_backend and not consumer-rendered -- same accepted precedent as the eggplant pilot).

## FLAGS (verification_status.open_findings, all blocks_launch=false, modeled-and-flagged)
1. `cayenne_pilot_regional_calendars_modeled` -- per-zone windows MODELED from DTM + crop-invariant frost
   anchors + representative extension dates; not each source-verified vs a live regional pepper calendar.
2. `cayenne_pilot_dtm_green_vs_red` -- days_to_maturity [70,80] is FROM TRANSPLANT to GREEN (well sourced);
   the ~90-100 red-ripe figure is a green+2-3wk inference (UMD), no cayenne-specific red day count exists;
   lives in prose, not the numeric field.
3. `cayenne_pilot_scoville_range` -- ~30,000-50,000 SHU stated (task + common usage); extension gives
   ~25,000-50,000 (UF/IFAS, PSU); prose hedged to "roughly 30,000 to 50,000"; jalapeno contrast T1-sourced.
4. `cayenne_pilot_heat_pause_modeled` -- 6 heat_pause cells (deserts + deep-Gulf/FL); more heat-tolerant
   than tomato so runs through se_gulf z8 + warm_arid z8; thermal basis UMD-sourced; months/split modeled.
5. `cayenne_pilot_cool_region_marginal` -- northern z3/z4 + ca_north_coast marginal for ripening RED pods
   for drying; calendars provided, region_notes hedge (pick more green).
6. `cayenne_pilot_varieties_extension_confirmed` -- shipped EXTENSION-CONFIRMED cultivars (Long Slim/Large
   Thick/Carolina Cayenne/Super Cayenne II/Charleston Hot). **The task brief's 'Ring of Fire', 'Golden
   Cayenne', 'Large Red Thick Cayenne', 'Long Red Thin' could NOT be confirmed from any T1 extension source
   and were deliberately DROPPED** (source-or-flag). Carolina Cayenne correctly attributed to USDA ARS
   Charleston SC (NOT Clemson), with root-knot-nematode resistance.
7. `cayenne_pilot_yield_general_pepper` -- no cayenne-specific per-plant yield in extension; qualitative
   (prolific, dozens of small pods) + general ~15-20 lb/10-ft row (Iowa State).
8. `cayenne_pilot_regional_source_anchors_general` -- several regional cells anchor institution portals.
9. `cayenne_pilot_hawaii_window_modeled` -- z11 broad frost-free default; CTAHR PDFs not WebFetch-readable;
   no fabricated source.
10. `cayenne_pilot_container_size_general` -- 5-gal min from UMD general pepper; no cayenne-specific size;
    compact habit makes 5-gal ample.

## Status / next
`status="author_fresh_pilot"`, `launch_ready_core=false`, `launch_ready_seasoned=false`. NOT launch-ready:
queued for the daily biology-fidelity review + a per-region source-truth sample to confirm the modeled
regional windows, the 6-cell heat_pause + spring/fall splits, the cool-region red-ripening framing, the
extension-confirmed variety list, and the green-vs-red DTM before any flip. Promotion to canonical is a
separate Trevor-gated step.
