# spring-onion (scallion) -- author-pilot notes

Slug: `spring-onion` | name "Spring Onion / Scallion" | status `author_fresh_pilot` (launch flags false).
Output record: `spring_onion_crop.json` (pretty for review; the canonical splice MUST be re-serialized
COMPACT -- `separators=(",",":")`, `ensure_ascii=False`, no trailing newline). READ-ONLY on canonical
was respected; all gate runs used scratch copies.

## What this is
A fast green bunching onion / scallion, harvested YOUNG for the green tops + slim white shank, BEFORE
bulbing. Structural model = certified **onion** (same Allium: region/zone roster, consumer block
shapes, allium pests/companions). Calendar/succession shape modeled on certified **radish** (the
fast cool-season succession sibling, photoperiod-free). All biology re-derived for scallion.

## Key spring-onion vs onion refits (the load-bearing differences)
- **Harvested GREEN -> photoperiod/bulbing machinery DROPPED entirely.** No `gating_factors` key, no
  top-level `photoperiod` block, no per-cell `recommended_day_length_type` / `day_length_note_*`, no
  variety `day_length_type`. Day length gates bulbing; we pull before bulbing, so per the gate-on-
  biology rule day length is irrelevant (same call garlic/leek made). `calendar_basis` stays
  `frost_anchored`, `archetype` stays `cool_season_annual`. A9 photoperiod gate no-ops on `[]`.
- **Fast (days_to_maturity [50,70], mid 60)** vs onion [90,120]/100. `weeks_indoors` 4 (UMN: start
  seed indoors ~4 wk before set-out) vs onion 10. `harvest_urgency` "moderate" (fresh) vs onion
  "cure_and_store"; no curing/storage-bulb narrative.
- **Heavy succession** (`succession_policy.suitable=true`, `interval_weeks=2`, every 2-3 wk) vs onion
  (suitable=false -- a single day-length-gated planting). `successions_realized` CC-DERIVED by
  `tools/derive_realized_successions.py` (20 cells, crop-max 12; `--check` clean).
- **Dense spacing [1,2] in** (Clemson/UMD/UF green-onion rows) vs onion [4,6]. **pH [6.0,7.0]**
  (Clemson ideal 6.2-6.5). **Moderate feeder** (`organic_matter_preference` "moderate",
  balanced 10-10-10, no bulb-sizing N taper) vs onion high-N-early.
- **Very cold hardy / can overwinter** (bunching Allium fistulosum) -> northern_tier runs CONTINUOUS
  spring-through-fall with NO heat_pause (scallions tolerate the northern summer like kale/chard,
  per the heat-tolerant-run-through rule), cold_pause only in deep winter; overwintering noted in
  prose + container_notes.overwintering.applicable=true.
- **Plant nearly year-round in mild regions**; in hot regions (desert/gulf/FL/interior/warm-arid) a
  cool-season fall-through-spring crop with a peak-summer heat_pause, mirroring radish's windows +
  the cool-season-timing guardrail (plant tokens never land in the summer months the cool-season
  peers pause). 20 resolved cells, full 12-token calendars, plant_out filled every cell, heat_pause
  objects backed with °F basis + source (A28).
- **Two-route framing kept honest:** true bunching types (A. fistulosum, never bulb, perennial/cold-
  hardy) OR regular onions sown thick + pulled young. Varieties carry NO day_length_type.

## Gate result
`tools/whole_crop_gate.py spring-onion` -> **GATE: PASS** (exit 0), all A2-A36 + B-G at 0, reproducible.
`derive_realized_successions.py --check` -> up to date (exit 0). `verbatim_scan.py` -> 0 hard hits,
0 borderline. Verified twice: (1) splice + derive + gate; (2) re-splice the standalone file alone into
a pristine canonical -> gate exit 0, derive-check exit 0 (the file itself is the gate-passing record).

## Source ids cited (all catalogued T1, all fetched & corroborated 2026-06-30)
- `umn_ext` -- UMN Extension "Growing scallions in home gardens" (full sun, direct-sow / 4-wk indoor
  transplant, 2-in band + thin to 1/in, ~1 in/wk water, onion maggot, Botrytis/Fusarium basal rot).
- `clemson_hgic` -- Clemson HGIC "Onion, Leek, Shallot & Garlic" green-onion section (sets/transplants
  spring, ready 6-8 wk, spacing 1-2 in, full sun, pH 6.2-6.5, Beltsville/Evergreen Bunching, harvest
  tops 6-8 in, fridge ~2 wk, thrips + onion maggot, 9 lb 10-10-10 / 1000 sq ft).
- `umd_ext` -- UMD Extension "Growing Onions" green-onion guidance (5-hr sun tolerance, thin to 2 in,
  harvest tops 6 in, allium leafminer, white rot, high nutrient need).
- `uf_ifas_vh021` -- UF/IFAS VH021 Florida guide: "Onions, bunching (green)" plant Sep-Mar, ~2-in
  in-row spacing, days to harvest 50-75 (green). Anchors the Florida cells.
(`verification_status.source_set` = these 4. Distinct cited IDs across the record: 4; uncatalogued 0,
non-T1 0.)

## Flags (open_findings, all blocks_launch=false; for the daily biology-fidelity review)
1. **Regional planting windows are MODELED** on the certified cool-season pattern (radish/onion
   shoulder-season windows), not pinned to a per-region scallion date chart for every region. Florida
   uses uf_ifas_vh021; the rest cite the general scallion T1 set + the modeled flag. Per Trevor's
   generally-safe-now rule, ship reasonable windows, refine exact dates at the variety pass.
2. **NCSU "Green Bunch Onions" returns HTTP 403** on direct fetch; its numbers were corroborated via
   the fetchable siblings and NCSU is NOT cited in the record (corroboration only).
3. **Disease set substitution:** authored to the documented, fetchable T1 allium set -- Botrytis neck
   rot + Fusarium basal rot (umn_ext) + White rot (umd_ext) -- NOT the kickoff-listed "downy mildew +
   pink root". Those two are real allium diseases but were not covered in the fetchable scallion/green-
   onion pages, so they were not cited (source-or-flag, no fabricated citation). Surfaced for the
   review to add with a T1 source (onion's pink-root cited the tamu_agrilife PDF, an accepted-
   unfetchable precedent that could be reused).
4. **Variety names:** Clemson pins Beltsville Bunching + Evergreen Bunching; White Lisbon / Tokyo Long
   White / Parade are widely-grown standards not individually T1-pinned (editorial list, flagged).

## Judgment calls
- `interval_weeks=2` (every 2 wk) chosen from the "2-3 weeks" guidance; crop-level successions/
  max reconcile to 12 (the global cap) in long-season regions.
- northern_tier given NO heat_pause (continuous summer) -- a deliberate scallion refit vs radish,
  justified by bunching-onion heat tolerance + the heat-tolerant-run-through rule. Hot/warm regions
  keep radish's heat_pause months so the cool-season-timing guardrail holds (no plant token in a
  peer's paused summer month).
- `successions_realized` left to the deriver (not hand-authored); A8 re-derives and matches.
- Field set matches the spring-onion SHELL (no `thinning` block, no photoperiod/gating_factors keys);
  legacy top-level `zones{}` block left as the shell's nulls (gate-excluded layer).
