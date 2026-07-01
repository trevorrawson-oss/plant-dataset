# plum -- author-fresh perennial fill (modeled on certified peach)

Author: Claude Code (scale lane). Date: 2026-06-30. Status: `author_fresh_pilot`, launch flags false.
Output record: `plum_crop.json` (COMPACT, `separators=(",",":")`, no trailing newline, `ensure_ascii=False`).
Canonical `crops_data_final.json` was READ-ONLY throughout; the record was spliced into a SCRATCH copy for gating.

## What was built
Filled the plum shell into a gold-standard perennial by mirroring ALL ~35 peach perennial fields
(deciduous_fruit_tree / `perennial_chill_gated`) and refitting every value to plum biology. Nothing
was omitted. Perennial fields mirrored + refit: `calendar_basis`, `chill_hours_required`/`_range`/
`chill_hours_note_*`, `bloom_time_*`/`bloom_duration_days`, `pollination{}`/`self_fertile`/
`pollinator_notes_*`, `hardiness_zone_min/max` + `reliable_fruit_zone_min/max` + `hardiness_notes_*`,
`recommended_rootstock`/`_note`/`rootstock_selection_basis`/`rootstock_options[]`, `establishment_years`/
`establishment_note`/`years_to_first_harvest`/`years_to_full_production`/`year_one_notes_*`,
`dormancy_window`/`pruning_window`, `growth_stages` (+ `growth_stages_year_one`/`_annual` = null),
`tasks` ([]), `varieties_detail` ([]), `regions{}` with per-zone `resolved_by_zone{}`.
The whole non-perennial body (soil, ph, fertilizer, watering, companions, pests, diseases, storage,
container, rotation, notifications, weather_triggers, tips_by_stage, yield, failure_diagnostics,
descriptions, harvest_ready) was authored fresh to plum.

Calendars are DERIVED, never hand-authored: each fruiting cell's 12-token `calendar[]` is computed by
`tools/tree_calendar.derive_tree_calendar(bloom, harvest)` (the A4 source of truth), so it cannot drift.

## The headline: European vs Japanese pollination split
This is set up as the record's defining story, per the brief.
- **European plums** (Prunus domestica: Stanley, Italian prune/Fellenberg, damson, Green Gage) are
  **mostly self-fruitful**: a single tree bears (most set somewhat more with a second European nearby).
- **Japanese plums** (Prunus salicina: Santa Rosa, Burbank, Methley) are **usually self-unfruitful**
  and need a **second compatible Japanese cultivar** blooming at the same time (Methley and Santa Rosa
  are partial exceptions and serve as good pollenizers).
- **European and Japanese bloom weeks apart and will NOT cross-pollinate each other**, so a pollenizer
  must match type; place within ~100 ft.
- Structured booleans reflect the DOMINANT home case (European, self-fruitful): `self_fertile: true`,
  `pollination.self_fertile: true`, `pollination.needs_pollinizer: false`. The full split is carried in
  `pollinator_notes_seasoned/_beginner`, `pollination.notes_*`, the companions note, the `blossom`
  growth-stage + tip, the bloom notification, and failure_diagnostic #1 ("bloomed but set no fruit" leads
  with "is it a lone Japanese plum with no pollinizer?"). This mirrors peach's self_fertile=true + the
  J.H. Hale exception pattern.

## Chill + hardiness refit
- European ~700-1000 h, hardier (reliable z4-8); Japanese ~400-800 h (Methley ~250), z5-9, earlier bloom
  = more frost-prone. Crop-level `chill_hours_range: [250, 900]`; `hardiness_zone_min/max: 4/9`;
  `reliable_fruit_zone_min/max: 5/9`.
- Variety chills: Methley 250, Santa Rosa 400, Burbank 400, Green Gage 700, Stanley 800, Italian Prune 800,
  Damson 900. Min-variety-chill FLOOR = 250 (drives the A3 no-fruit split).
- Regional suitability tracks the SHARED `region_chill_delivered` table (crop-invariant). Refit vs peach:
  northern z5 upgraded to fruits_reliably and z4 to marginal (European plums are hardier than peach);
  survives_no_fruit empty cells (ca_south_coast z10, ca_desert z10, fl_peninsula z10) all have delivered
  chill lo < 250 floor, so they are correctly EMPTY (over-promise guard); z3 / fl z11 / hawaii z11 unsuitable.

## Rootstocks
`recommended_rootstock: Myrobalan`. Options: **Myrobalan** (vigorous, wet-soil-tolerant default),
**Marianna 2624** (semi-dwarf, heavy/wet soils, disease/nematode resistance), **St. Julien A** (semi-dwarf,
European plums, cold-hardy), plus **Guardian/Nemaguard** (peach-seedling, Southeast Coastal Plain for
root-knot nematode resistance, per Clemson).

## Pests / diseases
Diseases (3): **black knot** (the SIGNATURE plum disease -- Apiosporina morbosa; prune 3-4 in below galls
in dormancy before sporulation, destroy prunings, manage wild Prunus reservoir), **brown rot**, **bacterial
spot**. Pests (4): **plum curculio**, **aphids** (leaf curl plum aphid + mealy plum aphid), **peachtree
borer**, **San Jose scale**. Black knot is woven through dormancy/dormant_prune stages, the prune
notification, end-of-season cleanup, and failure_diagnostic #2.

## Gate result (scratch splice: `_canonical_with_plum.json`)
`python3 tools/whole_crop_gate.py plum ...` -> **GATE: PASS (exit 0), 0 violations.**
All A-gates 0, including A3 (perennial invariants), A4 (tree calendar coherence), A22 (variety-chill type
lock), A25/A29/A36 (register completeness/fill/CP-required), A20/A23 (display), B/C/D (dual-voice/dash/temp),
E (source-tier: 9 IDs, 0 uncatalogued, 0 non-T1), F (anchoring: 98 claim leaves, 0 gaps).

### A37 (calendar-coherence) lines -- reported separately per the brief
**A37 = 0 violations.** Trees are exempt from Bug 1 (growing-after-harvest, frost_anchored only), and every
harvest window was authored as a single continuous span, so there are NO one-month harvest-holes to flag.
Nothing to hand off for central normalization. (Confirmed dataset-wide: `calendar_coherence_gate` = 0/125.)

`release_verify.py` on the scratch canonical: **clean, no blocking concerns.** (Its 2 Step-5.5 `wait`-month
review notes are PRE-EXISTING in canonical -- verified 2 in the untouched original; plum contains 0 `wait`
tokens.) Dataset-wide numeric_sanity 0/125, cross_consistency 0/125; peach (template) still exits 0.

## Sources (all T1, all in `source_catalog`)
- `clemson_hgic` -- https://hgic.clemson.edu/factsheet/plum/ (WebFetched: types/pollination, soil, spacing 18-22 ft, pH 6.0-6.5, rootstocks, yield 2-3 bu, pests)
- `mu_ext` -- https://extension.missouri.edu/publications/g6001 (WebFetched: European self-fruitful [Stanley, Damson] vs Japanese cross-pollination [Santa Rosa, Burbank, Shiro, Methley])
- `umn_ext` -- https://extension.umn.edu/plant-diseases/black-knot (WebFetched: Apiosporina morbosa, symptoms, 2-yr cycle, prune 4 in below, dormant timing)
- `umaine_ext` -- https://extension.umaine.edu/ipm/ipddl/publications/5091e/ (WebFetched: black knot host range EU/JP/American, prune 3-4 in below before Apr 1)
- `uc_ipm` -- https://ipm.ucanr.edu/agriculture/plum/mealy-plum-aphid/ (WebSearch-verified: leaf curl plum aphid + mealy plum aphid biology/management)
- `ucanr_ext` -- https://ucanr.edu/site/fruit-nut-research-information-center/plum-rootstock-scion-selection (WebSearch-verified: Myrobalan/Marianna 2624/St. Julien traits)
- `ncsu_ext` -- https://content.ces.ncsu.edu/north-carolina-production-guide-for-smaller-orchard-plantings (general stone-fruit orchard care; reused from peach)
- `aces_ext` -- https://www.aces.edu/blog/topics/crop-production/black-knot-disease-of-plum/ (black knot)
- `msu_ext` -- https://www.canr.msu.edu/news/controlling_black_knot_in_michigan (black knot)

## Flags (for the biology-fidelity / source-truth review lane)
- **`aces_ext` and `msu_ext` URLs are search-surfaced, not directly WebFetched** (network fetch not run on
  those two). Real extension pages; the black-knot claims they back are corroborated by the directly-fetched
  `umn_ext` + `umaine_ext`. Sample-verify at cert.
- **`ncsu_ext` is a general small-orchard stone-fruit guide**, not plum-specific; used only for generic
  orchard care (planting depth, watering, replant), not for a plum-unique claim.
- **Dates/windows are "generally-safe," not day-precise** (per the locked scale-phase rule): plant_out/bloom/
  harvest windows are reasonable regional ranges to refine at the variety-delta pass. Japanese-earlier /
  European-later bloom and Japanese-earlier / European-later harvest are represented directionally.
- **Regional suitability upgrades vs peach** (northern z4->marginal, z5->fruits_reliably) reflect European
  plum's genuine superior cold-hardiness; worth a reviewer eye that the SHARED chill table + floor=250 keep
  every survives_no_fruit cell honestly empty (they do -- all have delivered-chill lo < 250).
- **`self_fertile: true`** is the dominant-European home case by design (brief); a reviewer should confirm
  this framing is preferred over surfacing the Japanese cross-pollination requirement at the boolean level
  (the prose makes the split unmissable either way).
