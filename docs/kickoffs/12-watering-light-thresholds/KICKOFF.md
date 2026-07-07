KICKOFF -- Watering fill + light + thresholds (plant-dataset), post-spine

WHERE YOU ARE
- Work in ~/plant-dataset (the source of truth). Canonical is `6f584c3b`, working tree clean,
  origin/main IN SYNC (everything through the spine is pushed; HEAD == origin == `388bf2d`).
- READ FIRST, in order:
  1. CURRENT_STATE.md -- the live surface (read the header + the SPRING/SUMMER + TIMING-SPINE-COMPLETE
     entries).
  2. Auto-loaded memories: timing-spine-authoring (now says SPINE COMPLETE + what's next),
     weeks-indoors-canonical, current-state-md-drift, notifications-ai-architecture.
  3. docs/field_addition_register.md (#5 watering, #6 light, #7 thresholds -- your three tasks).
  4. The runbook: ~/plant-app/docs/superpowers/plans/2026-07-06-plan3-timing-spine-authoring-runbook.md
     (section 2.9 on watering.schedule_by_stage).
  5. The consumer contract: ~/plant-app/src/lib/guides.ts (the schedule_by_stage shape) +
     crop-timing.ts.
- Confirm state: `shasum -a 256 crops_data_final.json` == LATEST.txt; `git log -1`, `git status -sb`.

WHAT'S DONE (the TIMING SPINE is COMPLETE -- 114/114 certified)
- Every certified crop carries the spine: propagule; dtm_anchor + a from-sow day_range_from_sow
  ladder where it grows from a datable event; sow_depth_inches / thin_to_inches /
  harvest_window_days / divide_every_years where meaningful.
- Authored this campaign in 8 batches (winter set earlier; spring/summer + perennials on 2026-07-07):
  structuring stragglers (4), Solanaceae ladders (6), cucurbit ladders (13), flower ladders (13),
  microgreen ladders (8), empty-DTM perennials (29). All pushed.
- Gate state: timing_spine_gate --all-certified = 114/114, todo(required)=0, 0 violations.
  15 harvest-vs-DTM ADVISORIES stand (all from_transplant / no-'harvest'-id / cut-and-come cases;
  warnings-only, gate exit 0 -- expected, NOT bugs).
- ONE thing surfaced for the app team (in STATE_HISTORY, flowers batch): annual-flower stage sets
  have no id 'harvest', so crop-timing.ts's daysToHarvestFromStage anchors on the last (seed) stage,
  not 'flowering'. The app may want a 'flowering' anchor for ornamentals. Data is correct as-is.

WHAT'S LEFT (Trevor's confirmed order: #5 watering, then #6 light, then #7 thresholds)

1. REGISTER #5 -- WATERING FILL (the big one; per-stage watering PROSE). 70 certified crops still
   need `watering.schedule_by_stage[]` = {stage_id, system, rate, frequency, level, note_seasoned,
   note_beginner} (the 44 that already have it = the 23 winter crops + ~21 deciduous trees/berries).
   AUTHOR EACH CROP INDIVIDUALLY from its OWN certified crop-level watering prose (frequency/amount/
   method/critical_periods) + its own stage ids -- crop-specific, NOT an archetype template (Trevor's
   explicit blanket-authoring guard; surface the per-crop distinctions in each batch summary). The
   winter set's 5 batches (roots/alliums/brassicas/greens+fava, canonical history) are the pattern.
   The 70, by archetype (suggested batching):
     - warm_season_fruiting (30): 5 tomatoes + peppers(bell/banana/cayenne/habanero/jalapeno) +
       cucumbers(4) + squash(acorn/butternut/spaghetti/yellow/zucchini/pumpkin) + melons(cantaloupe/
       honeydew/watermelon) + eggplant + tomatillo + edamame + green-beans-bush + pole-beans + okra +
       sweet-potato
     - flowers (13), microgreens (8), culinary herbs (5: chives/cilantro/dill/mint/parsley),
       cool_season stragglers (4: celery/potato/snow-peas/sugar-snap-peas)
     - PERENNIAL JUDGMENT CALL (10): evergreen citrus (5) + woody herbs (lavender/oregano/rosemary/
       sage/thyme) also lack schedule_by_stage. Decide whether per-stage watering applies to these
       perennials (their stage sets are multi-year / establishment) or whether crop-level watering
       prose already covers them -- surface the call to Trevor, don't force an annual pattern.
   Microgreens (stage set sow/germination/blackout/light/harvest) and flowers (germination..
   seed_saving) have their own stage ids -- author against each crop's actual growth_stages ids.

2. REGISTER #6 -- SEEDLING LIGHT. NOT started. Trevor's ruling: seedling light is largely STANDARD
   across crops, so make #6 a cheap DEFAULT (bright seedling light, ~14-16 h under lights) + a few
   documented exceptions -- NOT a per-crop authored column. Design cheap; don't over-author. Decide
   the shape (a crop-level default the app assumes + an exceptions list, or a small field only on the
   exceptions). Contract-first + a light gate if it becomes a real field.

3. REGISTER #7 -- STRUCTURED CLIMATE THRESHOLDS (for next week's notifications/WeatherKit build).
   Promote the per-crop heat cutoff / frost tolerance from PROSE into clean numeric fields (e.g.
   `heat_threshold_f`, `frost_tolerance_f`); germination_temp_f already exists. A deterministic
   weather trigger (forecast_high > threshold -> alert) needs them STRUCTURED. Column GS arc.
   See memory notifications-ai-architecture; bridges the spine work to the notification build.

METHOD (hold this -- unchanged from the spine campaign)
- Author each crop INDIVIDUALLY from its own prose (the blanket-authoring guard). Archetype = a commit
  grouping only, never a content template. Surface per-crop distinctions in every batch summary.
- SHA-guard every batch: EXACTLY the intended crops change, all else byte-identical, count 124,
  canonical COMPACT (separators=(",",":"), ensure_ascii=False, NO trailing newline). A reusable splice
  template (load -> apply -> assert changed-set == target + top-level byte-identical -> write COMPACT)
  is in the spine batches; copy it.
- Gates per batch: for #5, whole_crop_gate.py <slug> (PASS each -- it enforces dual-register +
  no em-dashes + degF on the new consumer prose) + register_completeness_gate.py (PASS). Watering
  notes are consumer prose, so they must be dual-register and clean. (timing_spine_gate is spine-only;
  it won't police watering.)
- STATE TRIO each content release: bump LATEST.txt; append STATE_HISTORY.md (most-recent-first);
  SURGICALLY edit CURRENT_STATE.md (headline lead + Current-SHA line + the "114 certified anchors"
  SHA line). DO NOT run gen_current_state.py -- it CORRUPTS CURRENT_STATE.md (no --- separator; see
  memory current-state-md-drift).
- Trevor CONFIRMS EVERY PUSH. He pre-authorized committing verified batches without a per-batch
  approval; commit each verified batch, surface the per-crop distinctions in the summary, and hold
  the push for his confirmation.

KNOWN ADVISORIES (not bugs, carried from the spine): the 15 harvest-vs-DTM warnings (from_transplant
Solanaceae, cut-and-come herbs/lettuce, and the no-'harvest'-id flowers/microgreens are clean because
their ladders sit in-band). Advisory-only, exit 0.

START by confirming SHA/git state, then pick up at register #5: read the winter watering batches as
the pattern, propose the batch plan (suggest starting with warm_season_fruiting since those are what
alpha testers are planting now), and confirm the plan back to Trevor before authoring the first batch.
