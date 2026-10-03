# Utah Dixie shard report -- citrus (Task 7, 5 crops, cold-limited archetype)

**Status: DONE**

Shard file: `tools/staging/shards/utah_dixie_citrus.json` (5 cells, single zone "8").
`crops_data_final.json` was not touched (read-only, confirmed via `git status` and `git diff --stat`).

## Crops authored
grapefruit, lemon, lime, mandarin-clementine, orange-navel. All `calendar_basis="perennial_evergreen"`,
cold-limited (not chill-gated: `gating_factors` for all five carry `cold_hardiness` only, or
`cold_hardiness`+`heat_accumulation` for grapefruit/mandarin-clementine/orange-navel; none carry
`chill_hours`). Cloned the Nevada citrus donor structure (`resolution_method
perennial_evergreen_precompute`, `min_winter_temp_f`, `cold_basis_seasoned/beginner`, minimal/empty
calendar), re-anchored to `utah_dixie` single zone "8", re-sourced to USU (`usu_ext_wash_frost` +
`usu_ext_wash_fruits` only, no Nevada source ids carried over).

## Self-gate results (clean on first pass)
`python3 tools/region_harness.py utah_dixie 8 tools/staging/shards/utah_dixie_citrus.json <slug>` ->
**GATE: PASS** for all 5.
`python3 tools/region_cell_audit.py utah_dixie tools/staging/shards/utah_dixie_citrus.json` ->
**0 issue(s) across 5 cell(s)**.

| slug | region_harness | suitability |
|---|---|---|
| mandarin-clementine | PASS | `survives_no_fruit` |
| lemon | PASS | `survives_no_fruit` |
| orange-navel | PASS | `unsuitable` |
| lime | PASS | `unsuitable` |
| grapefruit | PASS | `unsuitable` |

## Per-crop suitability verdicts + reasoning
- **mandarin-clementine -- `survives_no_fruit`.** Explicitly the hardiest common citrus (clementine/
  satsuma types tolerate cold into the low-to-mid 20s°F). St. George's ordinary z8b winter low
  (roughly 15-20°F, USU Washington County frost data) still drops past that, so no in-ground planting,
  but a container tree brought under cover on hard-freeze nights is honestly a long-lived planting that
  may set fruit in an unusually mild winter. Heat-gated (`heat_summer_basis="high"`, St. George's
  100°F+ summers are ample; winter cold, not heat, is the limiting factor).
- **lemon -- `survives_no_fruit`.** Not heat-gated (dataset `gating_factors=["cold_hardiness"]` only,
  matching the Nevada donor's own lemon shape with no `heat_summer_basis` keys). True lemon (Eureka/
  Lisbon) is damaged in the high 20s°F and is called unsuitable-outdoors in the prose; the hardier Meyer
  lemon hybrid (low-to-mid 20s°F tolerance) still does not clear St. George's ordinary low, but is close
  enough that a protected container Meyer is an honest, non-fabricated call, mirroring the near-universal
  home-citrus convention that Meyer is the standard cold-marginal-climate lemon recommendation.
- **orange-navel -- `unsuitable`.** Wood damage near the mid-20s°F, fruit-freeze near 26°F, well past
  the z8b winter low, and (unlike lemon/mandarin) there is no widely grown cold-hardy navel selection to
  narrow that gap. Heat-gated but suitability is `unsuitable`, so `heat_summer_basis` is null at the
  cell level (heat is moot once cold decides the case); the crop-level field still carries `"high"` with
  prose noting St. Georges summer heat is not the limiting factor.
- **lime -- `unsuitable` (worst, per the task's framing).** The least cold-tolerant common citrus,
  damaged at or near the freezing point itself, with no hardy cultivar comparable to Meyer lemon or
  clementine/satsuma mandarin. Prose is explicit that this needs full indoor housing through the cold
  season, not just a container-brought-in-on-cold-nights arrangement.
- **grapefruit -- `unsuitable` (worst, per the task's framing).** Mid-20s°F wood/fruit damage with no
  cold-hardy selection, paired with the highest summer-heat requirement of the common citrus (moot here
  since cold decides first). Heat-gated, cell-level `heat_summer_basis` null (unsuitable), crop-level
  `"high"` with the same "heat is not the problem" framing as orange-navel.

## Judgment call (flag for content review)
The task text names mandarin-clementine as the sole "least bad" hardy option and lime + grapefruit as
"worst," leaving lemon and orange-navel unstated. I resolved that 3-way gap using a genuine, independent
horticultural distinction rather than an arbitrary split: **Meyer lemon and clementine/satsuma mandarin
are the two widely marketed, well-established cold-hardy citrus cultivars for marginal climates; no
comparably hardy navel-orange or grapefruit selection exists in ordinary cultivation.** That gave lemon
the same `survives_no_fruit` verdict as mandarin-clementine, and grouped orange-navel with grapefruit and
lime as `unsuitable` (three crops with no hardy-cultivar escape hatch). This is a defensible, sourced-in-
general-citrus-biology call, but since the task prompt did not explicitly bless lemon=survives_no_fruit
or orange-navel=unsuitable, a content reviewer should sanity-check this 2-vs-3 split before it certifies.

## Sourcing
Every cell cites exactly `usu_ext_wash_frost` (St. George z8b winter-low band + "100°F Jun-Aug" summer
heat fact) and `usu_ext_wash_fruits` (the Washington County recommended-fruit list, which omits citrus
entirely). No Nevada source ids (`nws_vef`, `unr_fs0261`) or other-region ids were carried over; the
Nevada donor was read for STRUCTURE only, per the guide. `min_winter_temp_f` is `[15, 20]` at the region
and zone level for all 5 crops (the USDA zone 8b band the task specified), not crop-differentiated --
the differentiation lives in the suitability verdict and the cold_basis/suitability_note prose, matching
the donor's own convention (a zone's winter-low band is a region property; the crop-specific judgment is
narrative).

## Structural notes
- `resolved_from = {"last_frost":"Mar 30","first_frost":"Nov 1"}` (fully populated, not `{}`) on every
  cell, satisfying `region_cell_audit`'s perennial-cell rule (must be `{}` or fully populated with both
  dates).
- `bloom`/`harvest_start`/`harvest_end`/`harvest` are `null` and `calendar` is `[]` on every cell
  regardless of suitability value, matching the Nevada citrus donor's own convention and the task's
  explicit "A32-exempt: minimal/empty calendar" instruction. `calendar_basis="perennial_evergreen"` is
  not in `coverage_floor_gate.CALENDAR_PRESENCE_BASES`, so A32 is a no-op here (confirmed by reading
  `tools/coverage_floor_gate.py`).
- `plantings` is the single `track:"perennial"` establishment entry (no `start_indoors`/`direct_sow`
  keys), region-constant across all 5 crops.
- No A9/day-length concerns (citrus has no `day_length_type` field; A9 is allium-only).
- No em dashes, no "degrees" spelling-out, no build-word leaks (grepped the file clean for em/en dash,
  "degrees", and terms like shard/delta/Nevada/archetype/donor/task/kickoff).
