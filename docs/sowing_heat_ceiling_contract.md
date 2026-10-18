# `sowing_heat_ceiling` field contract (register #35) -- v1

**Status:** PILOT, 30 reviewed crops (PLA-750). Ruled D1 to D6 (PLA-750 comment 47a09951) and P1 to P5
(comment b963b423), 2026-10-17. Column GS arc per `docs/gs_cross_crop_field_addition_v0.md`. The rest of the
roster is TODO (key absent); the A39 / A-gate fold waits until the column is complete.

## Why this field exists

The app holds a crop's next succession sowing when the 10-day forecast daily HIGH reaches a ceiling. It read
`heat_threshold_f`, which `docs/climate_thresholds_contract.md` defines as the **mature-plant** heat-stress
number (bolting, quality, crown failure). That is a different number from the one a sowing hold needs, and
for most crops the harm it describes happens weeks or months after sowing. PLA-750's evidence pass (301
verbatim quotes, 30 crops) showed the two diverge (spinach mature 75 per UMN, sowing 80; calendula bloom 85
per USU, sowing 86 per Eberle's 30°C). So the sowing ceiling gets its own field, with its own sources, and
`heat_threshold_f` keeps its contract meaning: the weather-alert number. **The hold never reads
`heat_threshold_f`.**

## Shape (crop-level, sibling of `heat_threshold_f`)

Modeled on `heat_threshold_temp_f` (ratified 2026-06-08). Three states:

| state | meaning |
|---|---|
| key absent | TODO: not reviewed |
| `temp_f: <int>` | reviewed, a sowing is held at or above this forecast daily high |
| `temp_f: null` | reviewed, **no sowing hold**: the null is a claim, sourced like any other |

| key | held | not held | notes |
|---|---|---|---|
| `temp_f` | int °F, 60 to 100 | `null` | |
| `measures` | `air` \| `soil` | absent | what the SOURCE's number measures (D2). A germination temperature is a seed-zone temperature, so `soil` (P3) |
| `basis` | `sowing_statement` \| `germination` \| `bolting` \| `maturity_coupled` | absent | the mechanism the source states. `maturity_coupled` = the crop matures inside the hot spell it is sown into (radish), or a source ties the sowing date to the harm (kohlrabi) (D3) |
| `claim` | the source's sentence, verbatim | absent | **the only rendered key**: the held line's first sentence (D2). Printed as the source wrote it, units included |
| `claim_source` | catalog id | absent | must be in `sources` |
| `temp_source` | catalog id, optional | absent | only when the number comes from a different page than the claim (kohlrabi) |
| `note` | required when `measures: soil` | required | backend. On a soil row: the air-for-soil proxy in plain words (D2: "so nobody mistakes it for a sourced threshold later"). On a null: why there is no hold, quoting the evidence (for the nine unsourced holds, their weak mature-plant quote, "so the next pass starts from it") |
| `sources` / `anchoring_urls` | the usual pair | the usual pair | ids equal; each anchor document-scoped with a `verified` date |

## Invariants (gated by `tools/sowing_heat_ceiling_gate.py`)

1. `succession_policy.pause_in_heat` is `true` **exactly** when `sowing_heat_ceiling.temp_f` is an int. A crop
   with `pause_in_heat: true` and no field is a hold with no reviewed reason, and fails.
2. `claim` is found verbatim in the **raw hashed bytes** of the page at `anchoring_urls[claim_source]`
   (`tools/.evidence_cache`, MANIFEST-listed), never in the tag-stripped doc cache (PLA-768: that stripper eats
   a literal "<" and what follows).
3. The number: with no `temp_source`, `temp_f` (or its °C rounding, e.g. 86 for "30°C") appears in `claim`;
   with a `temp_source`, `temp_f` appears with a degree unit in that page's hashed bytes.
4. Every double-quoted span of 12+ characters in `note` is found in the hashed bytes of one of the field's
   anchored pages.
5. Population: the gate reports the crops it inspected and refuses below its floor (30 at the pilot).

## The pilot (30 crops, PLA-750)

10 held: spinach 80 (air, sowing_statement, UMN), lettuce-leaf 80 (soil, germination, USU), cilantro-coriander
75 (soil, bolting, USU), beet 80 (soil, germination, USU), radish 75 (air, maturity_coupled, UC Sonoma MG),
kohlrabi 75 (air, maturity_coupled, UMN claim + USU number), sugar-snap-peas 80 and snow-peas 80 (air,
germination, USU "soil and air"), calendula 86 (air, sowing_statement, Eberle 30°C), viola 75 (soil,
germination, UF).

20 not held: the 10 ruled changes (celery, spring-onion, broccoli, cauliflower, cabbage, brussels-sprouts, kale,
collards, edamame, borage), the 9 unsourced holds (carrot, arugula, dill, turnip, parsley, bok-choy, sweet-pea,
nasturtium, chamomile) and sweet-alyssum (D3). The per-row evidence is
`tools/staging/pla750/ruled_table.json`.

## Not in scope

The regional `heat_pause` calendar cells and the succession tip prose ("skip summer") are the climate-window
mechanism, not the forecast hold, and are untouched. Mature-plant heat reasons for crops that no longer hold
live in `tips_by_stage` at the stage where the harm happens (D4).
