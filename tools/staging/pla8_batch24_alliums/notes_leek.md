# notes_leek.md -- PLA-8 batch 24, leek, authored 2026-09-03 against the CORRECTED record

Authority: `leek_source.json` in this directory (byte-identical to the leek `pests[]`/`diseases[]` in
the r4 candidate, checked). Every leek record changed in the correction pass, so EVERY ladder below
was re-authored from the corrected record. No previous rung was reused: the closest carry-overs
(thrips water_spray, maggot crop_rotation/garden_sanitation) were rewritten because the previous
notes either quoted the OLD flight timing, used the retired "the guidance" device, or lacked the
row-cover trap precondition the corrected record now carries.

Ladder order is by tier; within the cultural tier the order is spatial (rotation) -> temporal
(planting time) -> hygiene (sanitation), matching the record's own sentence order where it has one.

Rung total: 29 across 7 problems (previous authoring: 18). The promote pins `EXPECTED_RUNGS["leek"] = 18`
and `TOTAL_RUNGS = 82`; both need re-pinning after the orchestrator accepts the count.

## Onion thrips (`onion-thrips`, insect, severity high) -- 5 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| garden_sanitation | rewritten (new) | volunteers + debris at season's end; thrips overwinter in allium material on the surface |
| weed_host_control | new | cultivate weedy edges early, before they dry down and push thrips onto the crop; siting away from small grains, alfalfa, clover (see findings: a host CROP, not a weed, placed here on the same shed-when-it-dries mechanism) |
| balance_nitrogen | new | nitrogen adequate not heavy; vigor buys tolerance, not fewer thrips |
| water_spray | rewritten | hard spray into leaf folds and the neck, light infestations; persistent outbreaks to local extension |
| beneficial_predators | new | minute pirate bugs and lacewings where broad-spectrum sprays are avoided |
Dropped from the previous authoring: crop_rotation (the corrected record does not say rotate for thrips).
Not laddered: straw mulch, even watering (method reach; see findings).

## Leek moth (`leek-moth`, insect, severity medium, novel id) -- 6 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| crop_rotation | rewritten | rotate off last year's allium ground; adults overwinter in debris; rotation is the precondition for covering |
| planting_time_avoidance | new | delay planting past the first emergence where the season allows; emergence at ~50°F, sometimes March; NY first flight mid-April to mid-May |
| garden_sanitation | new | clear allium debris at season's end, since adults overwinter in it |
| floating_row_cover | rewritten | on BEFORE the overwintered moths emerge (~50°F, sometimes March) or on planting day if later; sealed; left on for the season, not lifted between flights; do NOT cover last year's allium bed (both registers) |
| handpick | rewritten | remove larvae and cocoons from the plants; larvae feed 2 to 3 weeks inside folded leaves; net-like cocoon on the foliage; injury June through September, 2 to 3 generations |
| spinosad | new | 7 to 10 days after a peak flight; pheromone trap set by mid-April marks the peak; Bt did not significantly reduce larvae in lab tests |
The previous note's "two generations, roughly May to June and August to October" and "through the flight
periods" timing is GONE; the record's US timing (two to three generations, injury June through
September, flights mid-April to mid-May / mid-June to mid-July / late July to late August) is used instead.
The record's "remove larvae and cocoons from the plants" is placed under handpick (the catalog's
"physically removing larvae ... on a regular scouting schedule"), not folded into garden_sanitation,
so the two rungs carry different claims: in-season roguing vs end-of-season debris.

## Onion maggot (`onion-maggot`, insect, severity medium) -- 4 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| crop_rotation | rewritten | rotate off last season's allium ground AND site new plantings away from it; pupae overwinter in soil around last season's alliums |
| planting_time_avoidance | new | planting later in spring, once the first flight has passed, where the season allows |
| garden_sanitation | rewritten | culls; lifted plants with roots in fall; no spring manure or green manure (rotting organic matter draws egg-laying) |
| floating_row_cover | rewritten | from planting day, BEFORE the spring flight, sealed; trap precondition in both registers |
"At emergence" / "while they establish" is gone; the cover goes on from planting day, ahead of the flight.

## Allium leaf miner (`allium-leafminer`, insect, severity medium) -- 5 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| crop_rotation | rewritten | rotate, and site as far as possible from last year's alliums; pupae overwinter in tissue or surrounding soil |
| planting_time_avoidance | new | transplant after mid-May, harvest by early September, dodging both flights; fall leeks worst hit |
| garden_sanitation | new | destroy infested debris after harvest to remove overwintering pupae |
| floating_row_cover | rewritten | on BEFORE each flight (late March / early September), edges buried, ~8 weeks; two weeks late = MORE larvae and pupae; trap precondition both registers |
| spinosad | new | twice in the 2 to 4 weeks after the flies first appear |
The previous "March into April and September into November" timing is gone; the record has late March
through April (sometimes May) and about September into October.

## Leek rust (`leek-rust`, fungal, severity low) -- 5 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| airflow_spacing | rewritten | space so foliage dries; 57 to 75°F, optimum near 59°F, several hours of leaf wetness; leek comparatively resistant |
| balance_nitrogen | rewritten | hold nitrogen back; dense stands and heavy nitrogen both increase it |
| water_at_the_base | new | irrigate at the soil line rather than over the leaves |
| garden_sanitation | rewritten | destroy volunteer alliums; clear debris at season's end |
| crop_rotation | new | 2 to 3 years off that ground, separated from an infected planting |
Dropped: resistant_varieties. The corrected record carries NO variety recommendation for leek, and the
previous note's "rust-tolerant varieties" claim had nothing under it.

## White rot (`white-rot`, fungal, severity high) -- 2 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| certified_clean_stock | rewritten | plant only clean stock; no cure; sclerotia persist over 20 years; even a few per soil sample can start it; rotation alone will not control it |
| garden_sanitation | rewritten | remove and destroy infected plants; strict sanitation against moving infested soil |
Not laddered: crop_rotation. The record's only rotation statement is negative ("rotation alone will not
control it"; "do not rely on rotation alone"), with no duration and no positive instruction, so that
caveat is carried INSIDE the two rungs rather than made a rung of its own. Flagged in findings for the
orchestrator to overrule if a rung is wanted.
The sclerotia figure follows the record ("even a few sclerotia per soil sample"), NOT the brief's
"one sclerotium per about 20 pounds of soil", which is not in the record. See findings.

## Pink root (`pink-root`, fungal, severity low) -- 2 rungs, all REWRITTEN
| method | status | source claim placed |
|---|---|---|
| crop_rotation | rewritten | 3 to 6 years; reduces rather than clears; persists for years and lives on other crops; leek a lesser host |
| improve_drainage | new | raised or well-drained beds where soil sits wet; weak or stressed plants most susceptible |
Dropped: certified_clean_stock (the corrected record makes no clean-stock claim). No resistant-variety
claim exists for leek and none is made. Not laddered: steady water and fertility (see findings).

## Temperature figures
Six regex hits in the file, all warranted by the record: 50°F x4 (leek moth, both registers of
planting_time_avoidance and both registers of floating_row_cover), plus 75°F and 59°F (leek rust,
airflow_spacing seasoned). Measured by the build script: 6. The promote pins `EXPECTED_TEMP_FIGURES = 3` batch-wide and will need
re-pinning after all four crops land.

## Fixes applied 2026-09-03 (the independent review, `review_leek.md`)

Nine rungs edited (12 register strings); the other 20 rungs are byte-identical to the reviewed file.
Rung count unchanged at 29 across 7 problems, temperature figures unchanged at 6 (50°F x4, 75°F, 59°F).
`validate_out.py leek r4_candidate.json`: RESULT: PASS. Sources for the new wording are the record and the
catalog method text only. The scratchpad `build_leek.py` still emits the pre-review strings; `out_leek.json`
is the authority for these twelve.

- onion-thrips/weed_host_control/beginner (2a, 2b): "...sends the pest your way at the worst time. A patch of
  grain, alfalfa or clover next door does the same when it dries or is cut, so give the bed some distance
  from one." -> "...sends the pest your way. Do this while there is no crop for the thrips to land on; once
  the leeks are up, leave the edges alone." The small-grain/alfalfa/clover siting sentence is out of the
  rung and left to the record (garden_sanitation is a PASS rung and was not touched), so the "siting away
  from small grains, alfalfa, clover" clause in the thrips table above no longer applies.
- onion-thrips/weed_host_control/seasoned (2a WRONG): "Cultivate weedy margins early in the season, while the
  crop is still small, because thrips move off weeds as those dry down and the crop then takes the population
  in one pulse. Small grains, alfalfa and clover shed thrips the same way when they dry or are cut, so site
  leeks away from those plantings where you have the choice. Weed clearance acts before the crop is exposed;
  it does nothing for thrips already in the leaf folds." -> "Cultivate weedy margins early in the year,
  before the crop is up, because thrips move off weeds as those dry down and onto the crop. Leave the margins
  alone once the crop is up: the clearance is worth most before the crop emerges, while there is no allium
  standing for the displaced thrips to move onto. It is preventive only; it does nothing for thrips already
  in the leaf folds."
- onion-thrips/balance_nitrogen/beginner (3 STYLE): "A plant that is fed properly but not pushed also handles
  the feeding it does get better, which on this pest is a large part of what you can do." -> "A plant that
  is fed properly but not pushed also holds up better against what the thrips do to it, and on this pest
  that toughness is a large part of what you can do."
- leek-moth/crop_rotation/seasoned (6 SYNTHESIS): "...a source of the first flight in its own right, and with
  two to three generations following from mid-April into late August a planting left in place is exposed
  all season." -> "...a source of the first flight in its own right; it is that overwintered generation the
  move addresses."
- leek-moth/floating_row_cover/seasoned (9 STYLE, 60-word sentence): split after "if that is later." ->
  "Seal the edges and leave it in place through all two to three generations rather than lifting it between
  them." Content and the trap precondition unchanged.
- leek-moth/spinosad/beginner (11a UNSUPPORTED, 11b STYLE): "If caterpillars are getting past the cover" ->
  "If caterpillars get past the cover"; "Time it to the moths: a pheromone trap, a lure that draws the male
  moths and shows when a wave peaks, set out by mid-April, tells you when, and the spray goes on 7 to 10
  days after that peak." -> "Time it to the moths. A pheromone trap, a scented lure that catches the moths
  and shows when a wave peaks, goes out by mid-April; spray 7 to 10 days after that peak."; "Bt did not make
  a real dent in the caterpillars in testing, so do not count on it." -> "Bt, a bacterial spray sold for
  caterpillars, did not make a real dent in this pest in testing, so do not count on it." ("male" dropped;
  Bt explained from the catalog's `bt` entry; first sentence trimmed to hold the note under 90 words.)
- onion-maggot/planting_time_avoidance/beginner (13a SYNTHESIS): "The maggots hit hardest in the cool, wet
  weather of early spring, when young plants are just settling in, so a planting that goes in after that
  stretch misses the worst of it." -> "Those first flies lay their eggs at the base of young plants, so a
  planting that goes in after that wave has passed misses the worst of it."
- onion-maggot/planting_time_avoidance/seasoned (13b SYNTHESIS): "...sidesteps the heaviest egg-laying, which
  falls on young transplants in cool, wet conditions early in the season." -> "...sidesteps the first round
  of egg-laying, the round that falls on young transplants." (The cool-wet-spring fact already sits in
  garden_sanitation seasoned and is not repeated here.)
- onion-maggot/floating_row_cover/seasoned (15 SYNTHESIS): "Keep it in place through the cool, wet
  early-season stretch when stand loss peaks." -> "Keep it in place until the spring flight's egg-laying has
  passed, since that is what it blocks." (Duration is the flight, per the catalog's "until the pest's
  egg-laying period passes", not the weather.)
- leek-rust/crop_rotation/seasoned (25a, 25b UNSUPPORTED): "Spores are airborne, so the separation carries as
  much weight as the years: ..." -> "Spores are airborne, so the separation matters as well as the years:
  ..."; "Rotation is a supplement here; on leek, a comparatively resistant host, the airflow, nitrogen and
  watering steps do most of the work." -> dropped. The "comparatively resistant / cultural steps usually
  carry it" claim now sits in two rungs (airflow_spacing, garden_sanitation), both PASS and untouched.
- pink-root/improve_drainage/beginner (29b SYNTHESIS): "Weak, stressed roots are the ones this fungus takes,
  and a raised or well-drained bed keeps them out of standing water." -> "This fungus is worse where the
  ground stays wet, and a raised or well-drained bed takes that away; it cannot help a plant whose roots
  have already turned pink."
- pink-root/improve_drainage/seasoned (29a SYNTHESIS): "Use raised or well-drained beds where soil sits wet.
  The fungus infects roots directly and takes weak or stressed plants first, so drainage works on the host's
  condition rather than on the inoculum, and it does nothing for a plant whose roots are already pink." ->
  "Use raised or well-drained beds where soil sits wet; the disease runs harder in ground that stays wet,
  and drainage does nothing for a plant whose roots are already pink. On heavy or low-lying ground it is
  settled before planting, since there is no rescue once the roots have gone." The "weak or stressed plants
  most susceptible" fact is left to the record, so the improve_drainage row in the pink-root table above no
  longer carries it.

Not changed (PASS rungs, kept byte-identical): the reviewer's optional STYLE notes on rungs 7, 8, 21, 26/27,
28 and the cross-rung-reference pattern. The review's section 0 dependency stands: this file lands after r3
and r4, never before.
