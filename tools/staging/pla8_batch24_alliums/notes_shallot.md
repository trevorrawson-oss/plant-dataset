# shallot -- PLA-8 batch 24 authoring notes (r4, against the corrected record)

Authored from `shallot_source.json` (dumped from the corrected state 47e7b5c0). Ids and types taken
verbatim from `pinned_ids.json`. Output `out_shallot.json`: 24 rungs across 7 problems
(prev_out had 21). Validator: `RESULT: PASS`, precedent scan 119 + 4939 comparisons, worst 0.571
(onion-thrips/water_spray vs spring-onion, beginner), no shipped-sentence echo.

Per-rung disposition. "Reused" = carried from prev_out with at most a word or two changed;
"edited" = kept the shape, changed a sentence; "rewritten" = new prose from the record.

## onion-thrips (insect) -- 5 rungs, all REWRITTEN; record CHANGED
prev_out had crop_rotation, reflective_mulch, water_spray. The corrected record names none of
rotation or reflective mulch, so both are DROPPED.
- garden_sanitation -- rewritten. Volunteers + debris at season's end; overwintering in surface
  allium material.
- balance_nitrogen -- rewritten. Adequate-not-heavy; carries the record's "vigor buys tolerance,
  not fewer thrips" point (the watering half stays in prose here, see findings).
- weed_host_control -- rewritten. The grain/alfalfa/clover siting claim, framed host-specifically
  per the method's own caution.
- water_spray -- rewritten independently (NOT a declared copy on shallot). Hard spray into the
  folds, light infestations only, morning per the catalog caution, persistent outbreaks to the
  local extension office.
- beneficial_predators -- new. Minute pirate bugs and lacewings where broad-spectrum sprays are
  avoided.

## onion-maggot (insect) -- 4 rungs, all REWRITTEN; record CHANGED
- crop_rotation -- rewritten. Pupae overwinter in the SOIL of last year's allium bed (prev_out
  said "residue"; corrected). Site the new bed at a distance.
- garden_sanitation -- rewritten. Culls, volunteers, spring manure AND green manure out of the bed.
- planting_time_avoidance -- new. Delayed planting where the season allows, after the first flight.
- floating_row_cover -- rewritten. From planting BEFORE the spring flight (prev_out's "at
  emergence" is gone); trap precondition in BOTH registers.

## allium-leafminer (insect) -- 3 rungs; record UNCHANGED, every rung still REWRITTEN
Re-read each prev rung against the record and the rules; each failed at least one:
- crop_rotation -- seasoned carried "the crop's guidance lists"; rewritten both registers.
- floating_row_cover -- beginner said "ahead of" (the validator requires "before"); seasoned lacked
  a trap sentence the validator recognizes and imported the "confirm dates locally" caution from a
  different method. Rewritten both registers; spring flight March into May, fall September into
  October, both from the record.
- spinosad -- seasoned carried "the crop's guidance names" and an unsourced coverage claim;
  beginner was sound in substance but reworded alongside it. Rewritten both registers.

## white-rot (fungal) -- 3 rungs; record UNCHANGED
- certified_clean_stock -- beginner REUSED (one clause tightened to the record's "no cure once it
  shows up"); seasoned EDITED to name Sclerotium cepivorum and the record's "no rescue once it
  appears".
- garden_sanitation -- beginner REUSED; seasoned EDITED ("off the property" -> "away from the
  garden", otherwise intact).
- crop_rotation -- beginner REUSED; seasoned EDITED: prev said "20 to 30 years", the record says
  "over 20 years", so the 30 is gone; added the record's "attacks only alliums".

## downy-mildew (fungal) -- 5 rungs, all REWRITTEN; record CHANGED
prev_out led with resistant_varieties ("tolerant varieties"). The corrected record states no
resistant variety exists, so that rung is DROPPED and each seasoned note says so where it bears.
- airflow_spacing, water_at_the_base, crop_rotation (three years or longer), garden_sanitation
  (debris, cull piles, volunteers), balance_nitrogen (succulent leaves promote it) -- all new prose.

## botrytis-neck-rot (fungal) -- 2 rungs; record UNCHANGED
- balance_nitrogen -- REWRITTEN both registers. Beginner carried "is named as"; seasoned shared
  its spine ("among the factors that worsen neck rot ... feeding schedule settles outright") with
  garlic's shipped rung and was rewritten for independence rather than left to the scan.
- cure_and_store -- beginner REUSED; seasoned REWRITTEN (prev carried "this crop's own guidance").

## pink-root (fungal) -- 2 rungs, all REWRITTEN; record CHANGED
prev_out had crop_rotation + certified_clean_stock. The corrected record makes NO clean-stock claim
and NO resistant-variety claim for shallot, so certified_clean_stock is DROPPED.
- crop_rotation -- rewritten. Three to six years WITH the caveat that rotation reduces rather than
  clears; Setophoma terrestris; the record's 75 to 85°F soil-temperature band appears in the
  seasoned register (see findings: it adds one temperature figure to the batch count).
- improve_drainage -- new. Heavy, wet ground; weak or stressed plants are the ones it takes.

## Style checks applied to every note
Two registers differing substantially; 25 to 90 words and 2 to 5 sentences each (measured by the
build script, range 45 to 88 words); no Latin in beginner; no absolutes; no rung/ladder/tier; no
"the guidance ..." or "X's own sourcing" device; no British spellings; no dashes; the only figure is
the sourced 85°F. Every temperature or number checked against the problem's own record.

## Fixes applied 2026-09-03 (reviewer findings, review_shallot.md)
Applied to `out_shallot.json` only. Rung count 24 -> 23 across 7 problems (onion-thrips 4,
onion-maggot 4, allium-leafminer 3, white-rot 3, downy-mildew 5, botrytis-neck-rot 2, pink-root 2).
Every PASS rung is byte-identical (38 of 46 notes unchanged, verified by diff). Validator against the
corrected state 47e7b5c0: `RESULT: PASS`, precedent scan 119 + 4876, worst 0.571 (unchanged; the
water_spray beginner note was not touched). botrytis-neck-rot/cure_and_store left as authored: faithful
to the record; the record-level anchor question is filed separately.

- onion-thrips/weed_host_control (both registers): DROPPED. A grain/alfalfa/clover SITING claim sat
  under a weed-REMOVAL method, and the record makes no weed claim; the siting claim already lives in
  garden_sanitation seasoned ("handled by siting rather than by sanitation") and in the record. The
  three remaining rungs keep their tier order (cultural, cultural, physical, biological).
- onion-thrips/balance_nitrogen/seasoned: "Excess nitrogen promotes onion thrips, and on a crop that
  shelters them in the leaf axils where sprays miss, a bigger population is a bigger problem than
  usual." -> "Excess nitrogen promotes onion thrips, and the population it builds shelters in the leaf
  axils where sprays miss it." (comparative the record does not make, removed)
- onion-thrips/water_spray/seasoned: "A hard jet of water into the leaf folds knocks a light
  infestation back, and it earns more here than on most crops because the axils that hide Thrips
  tabaci from a spray of any kind are exactly where a directed stream reaches." -> "A hard jet of
  water aimed down into the leaf folds knocks a light infestation back; Thrips tabaci shelters in the
  axils, so a stream that only sweeps the outside of the clump leaves most of the population where it
  sits." (unsupported "more here than on most crops" and reach mechanism dropped)
- onion-thrips/beneficial_predators/beginner: "the sprays that kill every insect they touch" -> "the
  sprays that kill most insects they touch" (absolute)
- onion-thrips/beneficial_predators/seasoned: "A broad-spectrum material clears the predators along
  with the thrips it reaches and leaves the axil-sheltered survivors to rebuild through the next warm,
  dry spell with nothing feeding on them." -> "A broad-spectrum material kills the predators along
  with whatever thrips it reaches, and it does not reach the ones sheltered in the leaf axils."
  (three-fact causal chain no source states, reduced to the catalog caution + the record's axil fact)
- allium-leafminer/spinosad/beginner: "Time it to the spring or fall flight rather than spraying on a
  calendar." -> "Use it in spring or fall once the grubs are in the leaves, rather than on a calendar
  date." (no longer implies the spray targets the flight)
- allium-leafminer/spinosad/seasoned: "Spinosad is the option where covers are not practical, and it
  substitutes for exclusion rather than backing it up; with a sealed cover in place it has no role.
  Time applications to the spring and fall flights, when adults are laying, since that is the stage a
  spray meets." -> "Spinosad is the option where covers are not practical; under a cover that went on
  in time it adds little. It penetrates the leaf to reach the larvae mining inside it, so time it to
  the larvae rather than the calendar in either generation: the rows of white dots along a leaf edge
  are the egg-laying scars, and the larvae behind them are what the spray meets." (WRONG adult-stage
  claim replaced with the catalog mechanism, penetrates leaf tissue to reach leafminers, timed to the
  record's egg-laying scars; "no role" softened to the record's "if covers are not practical")
- downy-mildew/airflow_spacing/seasoned: "so spacing is set at planting for two effects at once: a
  canopy that dries sooner after dew, and more distance between an infected leaf and the next one."
  -> "so spacing is set at planting for one effect: a canopy that airs out and dries sooner after dew,
  which takes away the lingering wetness the pathogen needs to infect and sporulate." (leaf-to-leaf
  spread mechanism not in the record, removed; the drying reason is the record's and the method's)
- pink-root/improve_drainage/beginner: "Getting the water away from the roots is the one part of this
  you can still fix on ground that already carries the fungus." -> "Getting water away from the roots
  is one fix still open on ground that carries the fungus; keeping the plants watered and fed so the
  roots stay strong is the other." (WRONG exclusivity; the record also names steady water and
  fertility, and the rung's own seasoned note already said so)
