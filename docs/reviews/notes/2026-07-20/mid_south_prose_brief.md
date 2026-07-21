# Mid-South prose-review brief (for the authoring subagents)

The mid_south region cells are STRUCTURALLY COMPLETE and gate-green (windows, calendars, sources,
suitability all correct). Their PROSE is a mechanical name-swap DRAFT of the certified mid_atlantic
cells and carries stale specifics. Your job: rewrite the prose for HONESTY + house voice, changing
ONLY prose fields, never structural fields.

## Ground truth (read these in the cell + the sources note)
- `docs/reviews/notes/2026-07-20/mid_south_sources.md` -- frost anchors, UAEX windows, chill, blackberry.
- **Region:** `Mid-South: Ozark Uplands and Delta Lowlands` (AR/OK/TN/MO), zone_span ["7","8"].
- **Frost anchors:** z8 last frost Apr 3 / first frost Oct 31 (NWS Little Rock); z7 last frost Apr 10 /
  first frost Oct 24 (northern/upland).
- **THE governing rule:** every date/window/number your prose mentions MUST match the cell's OWN
  `resolved_by_zone[z]` fields (`plant_out`, `harvest`, `second_planting.plant_out`, `heat_pause.months`,
  `resolved_from.chill_hours`). Read the cell and describe THOSE numbers. Do not carry a mid_atlantic
  number.

## Rewrite ONLY these prose fields (leave every other field byte-identical)
- Cell top level: `region_notes_beginner`, `region_notes_seasoned`, and (perennials) `chill_basis_beginner`,
  `chill_basis_seasoned`.
- Inside each `resolved_by_zone[z]`: `heat_pause.basis_seasoned`/`basis_beginner`,
  `suitability_note_seasoned`/`_beginner`, `type_note_*`, `grown_as_note_*`, `frost_risk_note_*`,
  `day_length_note_*`, and any `synthesis_note_*` in `plantings[]`.
- NEVER change: `plant_out`, `start_indoors`, `harvest*`, `second_planting` windows, `calendar`,
  `sources`, `anchoring_urls`, `suitability`, `recommended_type`, `recommended_day_length_type`,
  `min_winter_temp_f`, `resolved_from`, `heat_pause.months`, `resolution_method`, region_id/label/zone_span.

## Known stale specifics to fix (by crop type)
- **Tomatoes (beefsteak/cherry/grape/heirloom/roma):** the draft says the fall window is "July 1 to
  August 10 / June 20 to August 1" (that is the OLD Virginia number). The real cell carries UAEX's
  fall transplant window: z8 `Jul 1 - Jul 15`, z7 `Jun 24 - Jul 8`. Describe THAT (UAEX: "sow seed
  about four weeks earlier"; a tight early-July fall transplant, distinct from the long spring set).
- **Cucumbers / summer squash / zucchini:** fall window is z8 cucumber `Aug 1 - Aug 15`, summer squash
  `Jul 15 - Aug 15` (read the cell). Not the old July window.
- **Sweet-corn / green-beans-bush / potato:** these gained a UAEX fall cycle (read the cell's
  second_planting). Frame it as the UAEX-documented fall crop.
- **Trees (chill_basis + region_notes):** replace the mid_atlantic multi-state chill prose (NC State,
  Penn State, Maryland, ">1,000 / >1,400 hours") with the AR gradient from `uada_ext_chill`: the belt
  banks about 1,000 to 1,300 chill hours in the cooler Ozark/upland north (zone 7) and about 900 to
  1,100 in the warmer lowland south (zone 8); the southwestern warm edge (Hope, ~901 hours) clears the
  highest-chill canonical variety (McIntosh, ~900) by the slimmest margin, so favor lower-chill
  varieties there. apricot / sweet-cherry / pomegranate are `marginal` (chill clears, but humid-East
  early-bloom frost, brown rot, fruit cracking make a reliable crop marginal); sour cherry, pawpaw
  (native to the Ozarks), and the rest are fruits_reliably. Cite the University of Arkansas.
- **Blackberry (THE signature crop):** lead the prose on it. UAEX FSA6105: blackberries are "adapted to
  all regions of Arkansas"; the University of Arkansas fruit breeding program bred the canonical
  cultivars for Arkansas (Ouachita, Navaho, Apache, Kiowa, Arapaho, plus the Prime-Ark primocanes);
  chill is a non-factor (cleared many times over). Home-state fit, authored with confidence.
- **Blueberry:** rabbiteye is the right choice for most of the belt (the cell's `recommended_type`);
  drop the NC-specific "Duke, Jersey" Coastal-Plain highbush framing and cite Arkansas rabbiteye +
  southern-highbush guidance.
- **Citrus:** cold-limited in zone 7-8 winters; keep it honest (survives/unsuitable per the cell).
- **Woody herbs (lavender/rosemary/sage/oregano/thyme):** humidity, not cold, is the Mid-South
  constraint (the humid-South framing), same as the draft but verify no Virginia/NC leftovers.
- **Residual stragglers:** remove any leftover "Virginia", "Penn State", "Maryland", "Raleigh",
  "NC State", "Duke, Jersey" unless genuinely accurate for AR/OK/TN/MO.

## Style
Dual-register house voice. NO em dashes (commas/colons/semicolons/periods). American English. Temps
render `°F`. "plant" lowercase except at sentence start or "Plant Pro". `region_notes_beginner` is
warm + practical; `_seasoned` is precise + sources-aware.

## Output + gate
Write the FULL revised cells for your assigned slugs to your shard file
`tools/staging/shards/<your-shard>.json` as `{slug: cell}`. Then gate EACH:
`python3 tools/region_harness.py mid_south 7,8 tools/staging/shards/<your-shard>.json <slug>` must
print `GATE: PASS`. Fix until all pass. Report which slugs you completed + any honesty item you could
not resolve.
