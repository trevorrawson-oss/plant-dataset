# pear-asian -- author_fresh_pilot authoring notes (2026-06-30)

**Output:** `/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/40a00cf0-e9bc-44ac-8cf5-3e1f21550e3a/scratchpad/pear_asian_crop.json`
(compact, `separators=(",",":")`, `ensure_ascii=False`, no trailing newline). Canonical `crops_data_final.json` was READ-ONLY (SHA `84321950...`, unchanged).

## Approach
Filled the `pear-asian` shell modeled on certified **apple** (`archetype: deciduous_fruit_tree`, `calendar_basis: perennial_chill_gated`). Used the sibling `scratchpad/pear_european_crop.json` (a pome-pear on the identical apple rails, gate-PASS baseline confirmed) as the structural scaffold, then refit every field into Pyrus pyrifolia. All ~35 apple perennial fields are present and refit (none omitted): `calendar_basis=perennial_chill_gated`, `chill_hours_range=[250,600]` + per-variety `chill_hours_required`, `bloom_duration_days`, `pollination{}` + `pollinator_notes_*`, `self_fertile=false`, `hardiness_zone_min/max`, `reliable_fruit_zone_min/max`, `hardiness_notes_*`, `chill_hours_note_*`, `bloom_time_*`, `recommended_rootstock` + `_note` + `rootstock_options[]` + `rootstock_selection_basis`, `establishment_years` + `establishment_note` + `year_one_notes_*`, `dormancy_window`, `pruning_window`, `growth_stages` (year_one + annual), `notifications`, `weather_triggers`, `tips_by_stage`, `yield_expectations`, `failure_diagnostics`, `varieties_detail`, `regions{}` with per-cell `resolved_by_zone{}` calendars.

**Shell fix:** the shell shipped `calendar_basis: "frost_anchored"` (a placeholder that would have failed A30's archetype/basis dispatch check against `deciduous_fruit_tree`). Set to `perennial_chill_gated`.

## Asian-pear refits (Pyrus pyrifolia)
- **POLLINATION = CROSS-POLLINATION (the flagged refit).** `self_fertile=false`, `pollination.needs_pollinizer=true`, `pollinizer_distance_ft=50`. Plant two different, bloom-overlapping compatible cultivars. Threaded: a couple are *partially* self-fruitful (Shinseiki, 20th Century) but crop far better with a pollinizer; the very-early Chinese pears (Ya Li, Tsu Li) bloom too early to cross the Japanese types (pair them together); Niitaka is a weak pollen source (needs two partners, not a pollinizer); a European Bartlett can cross Japanese Asian pears where bloom overlaps.
- **SIGNATURE difference vs European pear: RIPENS ON THE TREE, eaten CRISP like an apple.** The opposite of European pear's pick-firm / ripen-off-tree / post-harvest-chill rule. Threaded through `description_*`, `harvest_ready_*`, `storage.*` (stores crisp in the fridge 1-3 months, no ripening rest), `growth_stages.harvest` (renamed "Harvest tree-ripe"; taste for sweetness), `notifications.harvest_window`, `tips_by_stage.harvest`, and `failure_diagnostics` (European "mealy/rotten core" from tree-ripening REPLACED with `picked_too_early_bland`: Asian pears do not sweeten off the tree). Verified: no "ripen OFF the tree / pick FIRM / mature but firm / post-harvest chilling" strings remain.
- **Round, apple-shaped, russeted** (smooth yellow types vs brown-russet types) in description/harvest_ready/varieties.
- **THIN HEAVILY (sets very heavily).** Threaded into `growth_stages.fruit_set`, `tips_by_stage.fruit_set`, `notifications.petal_fall`, `yield_expectations`, and a new `small_gritty_unthinned` failure (replaces biennial-bearing; folds it in).
- **Chill ~250-600 h** (`chill_hours_range=[250,600]`; roster floor 250 = Shinseiki). **Moderate, lower than European pear**, more heat-tolerant.
- **FIREBLIGHT-prone** (highly susceptible; 20th Century/Niitaka worst; resistant picks Shinko/Chojuro) in disease + prevention prose.
- **Rootstocks Pyrus betulifolia / calleryana / OHxF** (`rootstock_options[]`: betulifolia standard, calleryana standard, OHxF 97/87/333). `recommended_rootstock="OHxF 87"`. Quince noted as graft-incompatible with most Asian pears (not offered).
- **Hardiness z5-9** (`hardiness_zone_min=5`, `max=9`; `reliable_fruit_zone_min=5`, `max=9`). One zone less cold-hardy than European pear.
- **Pests:** codling moth, pear psylla, **stink bug (added, brown marmorated + natives, catfacing/corky pitting)**, pear scab. **Diseases:** fire blight, pear scab, pear decline. (Dropped European-set Fabraea leaf spot.)
- **`years_to_first_harvest=[3,5]`** (earlier than European), `years_to_full_production=[5,8]`, `establishment_years=3`.

## Region model
Kept pear_european's 10-region `resolved_by_zone` calendar structure. `resolved_from.chill_hours` is the crop-invariant shared `region_chill_delivered` table (unchanged, A18-clean). At Asian pear's chill floor of 250, every fruiting cell stays valid (ca_south_coast z9's band [200,550] straddles the floor -> legitimately `marginal` with a calendar). The **only** structural change reflects the warmer z5 hardiness floor, in `northern_tier`:
- **z3 -> `unsuitable`, empty calendar** (winter-kills below ~-30 F; Pyrus pyrifolia hardy to ~z5). Windows nulled.
- **z4 -> `survives_no_fruit`, keeps its calendar** (survives + blooms at the cold edge on ample chill, fruit unreliable). A4 tree-calendar stays coherent (bloom/harvest unchanged).
Per-cell + region prose refit to Asian cultivars (Shinseiki, 20th Century, Hosui, Chojuro, Shinko, Olympic, Ya Li) and Asian chill/heat framing; no European cultivar names remain in `regions`.

## Gate result (spliced into scratch canonical, canonical untouched)
- **`whole_crop_gate.py pear-asian` -> GATE: PASS (exit 0).** All A2-A37 sections 0 violations.
- **A37 calendar-coherence = 0 (no A37 lines to report).** Tree is exempt from Bug-1 (growing-after-harvest, `frost_anchored`-only); single-span harvest strings do not trip Bug-2 (one-month harvest-hole). Nothing to hand off for central normalization.
- Standalone dataset-wide gates: pear-asian contributes **0** to `calendar_coherence`, `coverage_floor`, `numeric_sanity`, `cross_consistency`, `calendar_basis`. (The 1232 coverage_floor / 37 calendar_basis totals are the pre-existing unfilled shells, not pear-asian.)
- **`release_verify.py` -> clean, no blocking concerns.** The 2 non-blocking `wait`-legibility review notes (ca_north_coast.z10, ca_south_coast.z10) are from OTHER crops; pear-asian's z10 cells are empty (`calendar: []`), so they carry no `wait`.
- **Adversarial confirmation (gate is live, not no-op):** emptying a `fruits_reliably` calendar -> A3 bounces; a string `chill_hours_required` -> A22 bounces.

## Sources (existing catalog T1 only)
Reused catalog T1 IDs already carried by the pear/apple set: `clemson_hgic, ncsu_ext, psu_ext, umn_ext, wsu_ext, uc_ipm, osu_ext, ucd_fruitnut, uf_ifas, uga_ext, ucanr_marin_mg, ucanr_santa_clara_mg`, etc. Gate E (source-tier): all cited IDs catalogued + T1. Gate F (anchoring): every claim-leaf carries a well-formed http(s) URL + `verified` date.

**FLAG (source-truth deferred, consistent with `author_fresh_pilot`):** anchoring URLs are inherited from the existing pear catalog set (general extension pear/rootstock/harvest pages); I did **not** independently WebFetch each Asian-pear-specific claim against these exact URLs, and no shell-out/PDF extraction was used (per the deny rule). A Step-10 anchoring re-point to Asian-pear-specific pages + a load-bearing source-truth sample are owed at certification, exactly as for the pear_european pilot. No non-catalog sources were cited; no unreadable/PDF-only source was relied on.

## State
`verification_status.status = "author_fresh_pilot"`, `launch_ready_core=false`, `launch_ready_seasoned=false`, `open_findings=[]`, `phase="perennial_pilot_pear_asian"`. No em dashes / spelled "degrees F" in consumer copy (temps render `°F`); American English; "plant" lowercase.
