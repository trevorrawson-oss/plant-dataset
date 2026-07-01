# viola -- author-fresh PILOT notes (cool-season refit of certified zinnia)

**Slug:** `viola` | **archetype:** `companion_and_ornamental_flower` | **calendar_basis:** `frost_anchored`
**status:** `author_fresh_pilot` (launch flags false -- NOT certified, NOT live) | **flags:** false
**Output:** `viola_crop.json` (compact-canonical) + `viola_crop_pretty.json` (review copy)
**Base SHA:** `ed8abc662c3d1e1d01ba5ca65333969561c74ad88b8aea645580ae092db52795` (canonical at author time)

## Gate result (spliced into a SCRATCH copy of canonical; READ-ONLY on the real canonical)
- `whole_crop_gate.py viola` -> **GATE: PASS (exit 0, 0 violations)**, all branches A2-A36.
- `derive_realized_successions.py --check viola` -> **up to date (0 changes)**; per-zone counts derived, crop-max 11, `succession_policy.successions` == `max_successions_per_season` == 11.
- `release_verify.py --base <canonical> --slug viola --ref zinnia` -> **clean, no blocking concerns**: only viola changed; catalog +none -none; zinnia byte-identical; no new violations (the long "cleared" list is the empty shell's own violations, now filled); no calendar/heat_pause byte-identical to zinnia.
- `register_completeness_gate` (dataset-wide) -> PASS (0 unruled; only the by-design deferred companion `provenance.reason`). `register_fill_gate viola` -> PASS.
- App-side cool-season timing audit -> 0 broccoli-signature hits (viola is `companion_and_ornamental_flower`, not `cool_season_annual`, so not in that audit's cell set; reported for completeness).

## THE KEY INVERSION -- viola vs zinnia (COOL-season, the whole point)
Zinnia gave STRUCTURE ONLY; every biological value was re-derived from viola/pansy sources. The
load-bearing refit is the seasonal inversion:
- **COOL-season, frost-hardy, summer heat-fade.** Zinnia is a heat-loving summer annual that
  cold_pauses winter; viola is the exact inverse. In WARM zones (warm_arid / low_desert_az /
  ca_interior / ca_south_coast / se_gulf / fl_peninsula / ca_desert) viola **blooms through winter
  (Nov-Apr) and heat_pauses through summer (the `H` block May-Sep, longer in the desert/FL)** --
  the classic fall-planted winter annual. In COLD zones (northern_tier z3-7) it runs **spring +
  fall planting windows with a midsummer heat_pause in the warmer cold zones (z5-7) and a winter
  cold_pause**, the hardy violas/Johnny-jump-ups overwintering under snow. Cool coastal CA
  (ca_north_coast) blooms nearly year-round with no heat_pause.
- **Frost is reassuring, heat is the threat.** The weather_triggers are flipped: "Frost and light
  snow" = `severity:none` (viola blooms above freezing, shrugs off frost/light snow); "Hot weather
  ahead" = `severity:protect` (the season-ender). Zinnia's frost-kill diagnostic was replaced with
  a heat-decline/legginess one.
- **9 heat_pause objects, all viola-specific.** Every cell whose calendar shows `heat_pause`
  carries a backed object (months + `basis_seasoned` naming the ~75 °F bloom-fade + germination
  inhibition + 2 sources each anchored). Months align to the certified cool-season peers (lettuce/
  carrot) per the cool-season timing guardrail.
- **plant_out filled every cell**, and includes BOTH spring AND fall windows in cold zones (the
  guardrail's hard check); calendar `plant` tokens are a subset of plant_out everywhere.
- **Edible flowers, framed honestly.** Storage was refit from zinnia's "not edible, cut flower" to
  viola's edible-flower handling: pick day-of from PESTICIDE-FREE plants only (nursery stock is
  often treated), wash, remove the bitter white heel; uses = salad/garnish/dessert/candied/ice
  cubes. Caveats carried from UMN edible-flowers + Clemson.
- **Short-lived perennial grown as a cool annual; self-seeds.** Johnny-jump-ups (V. tricolor)
  naturalize (seed_saving stage + tip reflect this).

## Numbers re-derived (NOT zinnia's)
- pH **5.4-5.8** preferred (tol 5.2-6.5) -- the pansy-specific Clemson/UF optimum, tied to avoiding
  black root rot + iron chlorosis at higher pH (zinnia was 6.0-7.0). NCSU notes broader tolerance.
- spacing **6-10 in** (violas/Johnny-jump-ups 6-8, large pansies 9-12).
- sunlight **full sun to part shade**, **4-6 hrs** (afternoon shade in heat; zinnia was full sun 6-8).
- germination **65-75 °F, 10-14 days, DARK** (warm soil + light inhibit -- the reason it is started
  indoors in late summer, not direct-sown into warm beds; zinnia germinates at 70-80 °F warm).
- days_to_maturity **70-90** (seed-to-bloom ~10-14 wk; FLAGGED approximate).
- NPK **5-10-10** light feeder, low-nitrogen (zinnia 10-10-10) -- avoids cold-weather stretch.
- family **Violaceae** (zinnia Asteraceae); rotation away from beds where crown/root rot built up.
- **pests:** slugs and snails (the signature cool-damp viola pest, promoted to top), aphids, spider
  mites (late-season heat), foliage-feeding caterpillars (incl. fritillary larvae). Replaces zinnia's
  Japanese-beetle/mildew set.
- **diseases:** crown and root rot (black root rot / Pythium / Phytophthora -- the signature
  warm+wet+poor-drainage killer, the refit headline), downy mildew, powdery mildew, leaf spots /
  anthracnose, Botrytis. Replaces zinnia's powdery-mildew/Alternaria headline.
- **companions:** honestly modest -- viola is the cool-season color/edible layer, not a
  pest-manager: bulb underplanting (traditional/low), cool-season greens interplant (likely/low),
  cool-weather annual bedding (traditional/low), early-pollinator + fritillary host habitat
  (likely/medium). No biological antagonist; the caution is wet-bed rot pressure (mirrors zinnia's
  "no antagonist, siting is the caution," but rot/drainage instead of mildew/airflow).

## Sources (all EXISTING catalog ids, all T1, all viola/pansy pages WebFetch-verified live 2026-06-30)
| catalog id | viola/pansy page used as anchoring URL |
|---|---|
| `clemson_hgic` | hgic.clemson.edu/factsheet/pansies-and-johnny-jump-ups/ (primary culture) |
| `ncsu_ext` | plants.ces.ncsu.edu/plants/viola-x-wittrockiana/ (+ viola-cornuta, viola-tricolor toolbox) |
| `uf_ifas` | gardeningsolutions.ifas.ufl.edu/plants/ornamentals/pansies/ (winter-annual timing, heat decline) |
| `uc_ipm` | ipm.ucanr.edu/home-and-landscape/pansy-violet/ (pests + diseases) |
| `psu_ext` | extension.psu.edu/extend-the-season-with-resilient-pansies (cold/overwinter) |
| `umn_ext_edible_flowers` | extension.umn.edu/flowers/edible-flowers (edibility + safety caveats) |

Convention = the marigold/radish draft pattern: reuse the GENERIC catalogued publisher id, point its
anchoring URL at the crop-specific verified page. **No new catalog entries** (release_verify: catalog
+none -none). UGA's pansy bulletins (B1359/B1423) are strong but NOT catalogued under a generic UGA id
-> deliberately NOT cited (the source-or-flag rule), and not needed given 6 solid T1 anchors.

## FLAGS / modeled values (all in `verification_status.open_findings`, all `blocks_launch:false`)
1. **viola_zone_cold_end_species_basis (med).** Zones 3-5 cold-hardiness rests on the hardier genus
   members -- Johnny-jump-up (V. tricolor, NCSU zones 2-9) and viola (V. cornuta) + snow cover -- not
   garden pansies proper (V. x wittrockiana, NCSU zones 6-10). Modeled at the genus level (the slug
   spans pansies/violas/Johnny-jump-ups). Reviewer: should cold-zone copy foreground the hardy species?
2. **viola_regional_calendar_modeled (med).** Per-region windows + 12-token calendars modeled on the
   cool-season frost-bracketed pattern: region+zone frost dates carried from the shared climate table;
   summer heat_pause months aligned to lettuce/carrot per the guardrail. Crop-specific dated regional
   viola tables would tighten exact windows. Held to the generally-safe-now bar.
3. **viola_hawaii_elevation_limited (med).** hawaii_tropical near-year-round bloom assumes COOL
   high-elevation (upcountry) culture; pansies/violas are not suited to warm lowland tropics. Modeled
   as cool-upland year-round with two planting pulses; flagged.
4. **viola_dtm_approximate (low).** DTM [70,90] is an approximate seed-to-bloom estimate (sources give
   "indoors 6-8 wk before transplant" + cool-weather bloom + 10-14 day germination, not a single DTM).
5. **viola_ph_optimum_acidic (low).** pH 5.4-5.8 follows Clemson/UF pansy optimum (black-root-rot tie);
   NCSU notes broader tolerance toward neutral (tol 5.2-6.5).
6. **viola_succession_framing (low).** `succession_policy.suitable` kept True (mirrors zinnia) and
   framed as staggered transplant sets across the cool window; viola is more often a 1-2 window bedding
   planting than a continuously sown succession crop. `successions_realized` derived per zone from the
   window split on heat/cold pauses (crop-max 11). **Reviewer may prefer suitable=False** -- the one
   structural judgment call worth a ruling.

## Discipline notes
- READ-ONLY on `crops_data_final.json` throughout; all gate runs used a spliced scratch copy.
- Canonical JSON written compact (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline).
  No em dashes / no `--` / no "degrees F" in any user-facing string; American English; `°F`;
  "viola"/"plant" lowercase except sentence-start.
- Dispatch contract honored: `gating_factors` absent, `zone_independent` absent; full 10-region
  roster; zones 3-11; non-empty 12-token calendars; plant_out filled every cell; calendars + per-zone
  successions CC-DERIVED (deriver --check reproduces them exactly); heat_pause backed at the cell.
- Two residual "zinnia" strings remain by design in `verification_status` (verification_log_ref +
  open_findings[5].note) -- accurate provenance describing the structural template lineage, backend
  fields, not user-facing.
