# onion -- PLA-8 batch 24 findings (r4)

## A. Record claims that could NOT be placed in any catalog method (left in the record, no rung forced)
1. **onion-thrips: straw mulch.** Record: "straw mulch on the bed has been shown to reduce
   populations" (both registers). `straw_mulch` applies_to `disease_general`/`fungal_foliar` only, so
   it cannot reach an `insect` problem. Catalog gap: no mulch method reaches insects (reflective_mulch
   does, but the corrected record no longer names reflective mulch, so it is not a substitute).
2. **onion-thrips: watering for vigor.** Record: "keep plants well watered: vigor buys tolerance of
   the feeding rather than fewer thrips." `even_watering` does not reach `insect`. The claim is
   carried only where it already sits in the declared byte-identical water_spray copy ("keep the
   plants healthy and watered so they can carry the feeding they do get" / "vigor and steady water
   matter alongside the physical pass") and as the tolerance-not-fewer-thrips framing inside
   balance_nitrogen. No dedicated rung.
3. **pink-root: steady water and fertility for vigor.** Record: "Keep plants vigorous with steady
   water and fertility" / "keep them watered and fed so the roots stay strong." `even_watering` does
   not reach `fungal`, and there is no fertility-for-vigor method (`balance_nitrogen` is about
   EXCESS). Not placed. The stress link is used inside improve_drainage only as far as the record
   supports it (poorly drained soil makes it worse; weak or stressed plants most susceptible).
4. **botrytis-neck-rot: let tops mature naturally / do not knock down green tops to force bulbing.**
   No catalog method covers harvest MATURITY: `prompt_harvest` points the other way (harvest sooner)
   and `garden_sanitation` is culls and debris. Placed as the precondition sentence inside
   `cure_and_store` (immature necks do not cure) and referenced in `balance_nitrogen` as the second
   grower choice. If the orchestrator wants it out of cure_and_store, the claim becomes unplaced.

## B. Fit judgments the orchestrator may want to overrule
5. **onion-thrips / weed_host_control.** The record's practice is SITING ("keep the bed away from
   small grains, alfalfa or clover"), not weed clearing. weed_host_control is the closest method (other
   plants hosting the problem near the bed, "kept clear at the edges" per its catalog text, and its
   seasoned text names thrips' alternate hosts explicitly). The rung states the siting practice from
   the record and the edge-clearing from the method text; the specific hosts named are only the
   record's three. Dropping it leaves the grain/alfalfa/clover claim unplaced.
6. **onion-maggot / planting_time_avoidance.** applies_to is `insect_chewing`/`insect_boring`; the
   validator accepts it because problem type `insect` reaches `insect_chewing`, but a root maggot is
   neither in the catalog's sense and the method's documented cases are squash vine borer and Mexican
   bean beetle. The record's claim ("Delaying planting until the first flight has passed reduces
   damage where the season allows") fits the method's MEANING exactly (a move in time against a
   locally published flight). If rejected, onion drops to 16 rungs and the delayed-planting claim goes
   unplaced.

## C. Inferences that join two record statements (flagged, not invented)
7. botrytis-neck-rot / cure_and_store note_seasoned: "a top bent green leaves exactly that"
   (an immature neck). Joins "bent-over green tops worsen it" with "infection of immature or
   insufficiently cured necks" and "do not knock down green tops to force bulbing."
8. pink-root / improve_drainage: "a waterlogged root zone stresses the plant and favors the fungus."
   Joins "heavy, poorly drained soil makes it worse" with "weak or stressed plants are the most
   susceptible."
9. onion-maggot / planting_time_avoidance note_beginner: "do not delay so long that the onions run
   out of season" renders the record's "where the season allows"; the seasoned note's "suits a long
   season and costs a short one" is the same rendering.
10. fusarium-basal-rot / resistant_varieties note_beginner: "the cheapest protection you can buy"
    comes from the METHOD's catalog text ("the cheapest and most durable control"), not the record.
11. pink-root / improve_drainage: "raised bed" comes from the method's catalog text ("Raised beds are
    the standard fix for vegetables on heavy ground"), not the record.

## D. Things deliberately NOT said (present in sibling records, absent from onion's)
- No "no home-garden insecticide is available" for onion maggot (garlic's record, not onion's).
- No clean-stock / tested-cloves claim for fusarium or pink root (garlic's record; the corrected
  onion pink-root record dropped the transplant claim).
- No storage temperature for botrytis or fusarium (garlic carries "below about 39°F"; onion's record
  says only "cool and dry"; the catalog's cure_and_store text says alliums "store just above freezing"
  but the record's wording governs).
- No "77 to 82°F" band for fusarium (garlic's record). The only figure used is pink root's 75 to 85°F.
- No reflective mulch for thrips and no crop rotation for thrips (neither in the corrected record).

## E. Pins the promote must re-derive after this authoring
- `EXPECTED_RUNGS["onion"]`: 13 -> 17 (thrips 5, maggot 4, botrytis 2, fusarium 3, pink root 3);
  `TOTAL_RUNGS` moves accordingly.
- `EXPECTED_TEMP_FIGURES`: onion contributes exactly ONE (`85°F` as the regex counts it, from
  "75 to 85°F" in pink-root/crop_rotation note_seasoned).
- `pinned_ids.json` `_twins` and the onion thrips `evidence` string still describe reflective mulch
  and a spring-onion template twin; both are stale against the r4 record (the corrected
  management fields differ). Ids and types themselves are unchanged and used verbatim.
