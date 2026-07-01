# grape-tomato author notes (fresh pilot, modeled on certified cherry-tomato)

- base_sha (canonical, read-only): `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5`
- authored: 2026-06-30 | status: `author_fresh_pilot` | launch flags: both false
- output record: `grape_tomato_crop.json` (compact) | spliced-into-scratch: `canon_scratch.json`

## What makes grape honestly DISTINCT from the cherry-tomato donor (not a clone)
Same species (Solanum lycopersicum), same frost-anchored / warm-season-fruiting / indeterminate
culture, so the CALENDAR biology is genuinely identical and was inherited structurally. The
distinguishing biology was re-derived and authored fresh, and is web-verified (T1 extension +
seed-catalog corroboration):
- **Fruit shape**: small, OBLONG / grape-shaped (vs cherry's round). Woven through description,
  harvest_ready, varieties.
- **Thicker skin + meatier, less-watery flesh** -> the two real selling points below.
- **Crack resistance**: thick skin resists the rapid-swelling split that plagues thin-skinned
  cherries. Refit into watering.signs_overwater, watering.critical_periods, failure_diagnostics
  (too_much_water), harvest_ready (more forgiving on-vine hold), yield (missed picking day costs
  less). Confirmed by Cornell AgriTech contrast (cherry thin/cracks vs grape thick/meaty) and
  seed-trade data (Juliet/Sweet Hearts crack-resistant).
- **Longer shelf life**: storage room_temp bumped to 2-3 weeks (vs cherry's 1-2), with the
  thick-skin mechanism; fridge/freezer/notes all re-authored.
- **Heavy CLUSTERED indeterminate yields**: yield_expectations re-authored (long clusters ripening
  in sequence; still 4-8 lb/plant, upper end for vigorous grape hybrids).
- **Numbers refit**: days_to_maturity `[65,75]` mid `70` (vs cherry `[55,70]`/`62`);
  ph.preferred_range `[6.2,6.8]` (vs cherry `[6.0,6.8]`). germination `[70,85]`, sunlight `[6,8]`,
  spacing `[24,36]`, weeks_indoors `6` are true species-level values (kept, verified vs Clemson:
  "space plants 24 inches apart", Smarty grape 70 days indeterminate).
- **Pests refit**: added **Whiteflies** (authored + sourced), dropped cherry's Spider-mite entry
  per the grape steer. Kept Aphids / Tomato hornworm / Flea beetles.
- **Diseases refit**: added **Fusarium and Verticillium wilt** (authored + sourced, resistant-VFN
  framing) alongside Early blight / Late blight / Septoria / Blossom-end rot.
- **Varieties**: grape-specific and real: Santa, Juliet (AAS, mini-Roma), Sweet Hearts
  (best-seller), Five Star Grape, Smarty, Red Grape. det_indet + container_notes rewritten to note
  grape's vigorous indeterminate habit and the scarcity of compact/patio grape cultivars (unlike
  cherry's Tumbling Tom / Patio Choice).

## Gate result (self-verify on scratch)
`tools/whole_crop_gate.py grape-tomato canon_scratch.json` -> **GATE: PASS** (all A-gates 0
violations; B/C/D/E/F/G clean). `tools/register_completeness_gate.py` -> **PASS** (0 unruled prose).
- **A37 (calendar-coherence): 0 violations** -> NO A37 lines to report / hand off. The inherited
  cherry calendars were already A37-normalized (canonical session P0), so grape is clean.
- Contract items all satisfied: frost_anchored, warm_season_fruiting, full 10-region roster, zones
  3-11, 12-token calendars, plant_out filled, successions CC-derived (A8 clean), heat_pause backed
  (A28 clean), dual-register both (A36/B), no em dashes / canonical °F (C/D 0), all sources T1.

## Sources (existing catalog, T1 only)
All 43 cited IDs are catalogued + T1 (0 uncatalogued, 0 non-T1). Inherited from the donor's T1 set
(umn_ext, clemson_hgic, cornell_ext, umd_ext, iastate_ext, msu_ext, psu_ext, ncsu_ext, uc_ipm,
ucanr_ext, mu_ext, uga_ext, unh_ext, usu_ext, ok_state_ext, tamu_agrilife, ucd_postharvest,
uf_ifas_* , etc.). New claim anchors added for the refit fields point at real, web-verified pages:
- Whiteflies: `umn_ext` (extension.umn.edu whiteflies diagnostic) + `clemson_hgic`
  (hgic.clemson.edu/factsheet/tomato-insect-pests/).
- Fusarium/Verticillium wilt: `umn_ext` (disease-management/fusarium-wilt), `ncsu_ext`
  (content.ces.ncsu.edu/fusarium-wilt-of-tomato), `clemson_hgic` (tomato-diseases-disorders).
- Cherry-specific donor URL swapped: days_to_maturity / det_indet clemson anchor moved off
  `mild-peppers-unique-cherry-tomatoes` to the general `hgic.clemson.edu/factsheet/tomato/` (which I
  read: covers grape tomatoes, Smarty grape 70 days, 24-in spacing, pH 6.0-6.5, indeterminate).
- sources_summary.primary rebuilt from grape's actually-cited IDs (not the donor superset).

## Flags / judgment calls
- **Calendar layer inherited structurally** from cherry (same species, same frost-anchored culture,
  same heat tolerance). Recorded in `verification_status.open_findings[grape_pilot_001]`,
  blocks_launch=false. All crop-identity prose (zone_notes, region_notes, notes) refit to grape,
  with grape varieties (Juliet/Sweet Hearts/Santa) and grape DTM (65-75). No cherry-variety leakage
  in user-facing text (scanned clean).
- **Backend provenance labels left as-is**: deep `plantings_provenance.authored_session` values
  still read `m16_cherry_step4_*` and a few backend `synthesis_note` lines say "Grape and cherry
  ...". These are backend (excluded from dash/temp/anchoring gates) and are a truthful record that
  the calendar was derived from cherry's certified sessions. Left intentionally; normalize if the
  pipeline prefers grape-labeled provenance.
- **varieties.sources = null** (per donor convention; per-variety values uncited). Not a fabricated
  citation.
- No em dashes anywhere; the 24 `--` occurrences are all in backend fields (source_quote /
  synthesis_note) where `--` is tolerated; user-facing dash hits = 0.
- Canonical `crops_data_final.json` was NOT modified (SHA verified unchanged).
