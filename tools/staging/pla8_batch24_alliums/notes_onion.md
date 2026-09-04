# onion -- PLA-8 batch 24 authoring notes (r4, against the CORRECTED record)

Authored 2026-09-03 from `onion_source.json` (state 47e7b5c0). Every rung below was written fresh
against the corrected record; NOTHING from `prev_out_onion.json` was reused (reasons per problem).
Validator: `RESULT: PASS`, 17 rungs across 5 problems, precedent scan 15 + 2867 comparisons,
worst 0.516 (A: onion/onion-thrips/garden_sanitation vs spring-onion).

Rung count changed from 13 (previous authoring) to 17: thrips 3 -> 5, maggot 3 -> 4, botrytis 2,
fusarium 3, pink root 2 -> 3. `promote_pla8_batch24.EXPECTED_RUNGS["onion"]` (13) and
`TOTAL_RUNGS` need re-pinning by the orchestrator; so may `EXPECTED_TEMP_FIGURES` (this crop
carries ONE figure, `75 to 85°F`, in pink-root/crop_rotation note_seasoned).

## onion-thrips (insect) -- 5 rungs, ALL REWRITTEN (record changed in r4)
| method | status | why |
|---|---|---|
| garden_sanitation | NEW | corrected record: clear volunteers + debris at season end; thrips overwinter in onion material left on the surface. Written independently of garlic's and spring-onion's sanitation rungs (worst score 0.516). |
| weed_host_control | NEW | record: keep the bed away from small grains, alfalfa, clover, which shed thrips when they dry down or are cut. See findings for the fit judgment (siting vs clearing). |
| balance_nitrogen | NEW | record: adequate not heavy nitrogen, excess promotes thrips; vigor buys TOLERANCE, not fewer thrips. |
| water_spray | DECLARED COPY | byte-for-byte from spring-onion's onion-thrips water_spray rung, read programmatically from `shipped_precedents.json`, asserted identical at build time. |
| beneficial_predators | NEW | record: minute pirate bugs and lacewings help where broad-spectrum sprays are avoided; persistent outbreaks to local extension. |

DROPPED from the previous authoring: `crop_rotation` (the corrected record does not say to rotate
for thrips) and `reflective_mulch` (the corrected record no longer mentions it; the `_twins` note in
`pinned_ids.json` that says onion's thrips prose names reflective mulch is stale against r4).

## onion-maggot (insect) -- 4 rungs, ALL REWRITTEN (record changed in r3)
| method | status | why |
|---|---|---|
| crop_rotation | NEW | pupae overwinter in the SOIL around last season's onions (not "residue"); site off last year's allium ground AND away from any cull pile. |
| planting_time_avoidance | NEW | record: "Delaying planting until the first flight has passed reduces damage where the season allows"; first flight arrives with the cool, wet weather of mid-spring. See findings for the applies_to fit. |
| garden_sanitation | NEW | culls, volunteer onions, and keeping spring manure and green manure out of the bed (rotting organic matter draws egg-laying). Written independently; the previous note's 72-character lift from garlic's cull sentence is gone. |
| floating_row_cover | NEW | from planting, BEFORE the spring flight, sealed at the edges; the trap precondition (do not cover ground that grew alliums last year, or the emerging flies are sealed in with the crop) is in BOTH registers and matches the validator's TRAP pattern in both. No "at emergence". |

## botrytis-neck-rot (fungal) -- 2 rungs, BOTH REWRITTEN (record unchanged; two defects + one refusal)
| method | status | why |
|---|---|---|
| balance_nitrogen | REWRITTEN | the previous seasoned note said excess nitrogen was "the one governed purely by choice; the other is green tops bent over", contradicting the record (not knocking tops down is also a choice). Now: both aggravating factors are grower choices; nitrogen is settled through the season, tops at harvest. |
| cure_and_store | REWRITTEN | previous seasoned note contained "in the bin" (the validator's British list refuses `\bbin\b`) and "take the conditions from onion guidance" (attribution device). Now carries the harvest-maturity practice (let tops mature, do not knock down green tops) as the precondition to curing, then cure thoroughly, store cool and dry, white-skinned bulbs most susceptible, set aside bruised or spotted bulbs (catalog caution). |

## fusarium-basal-rot (fungal) -- 3 rungs, ALL REWRITTEN (record unchanged; defects + refusal)
| method | status | why |
|---|---|---|
| resistant_varieties | REWRITTEN | previous notes used "Onion guidance puts variety choice at the head of its list" and "The source hedges it as where available" (the mis-attributed hedge). Now states the practice: where available, chosen at seed-buying time; availability is the qualifier. |
| crop_rotation | REWRITTEN | previous note said "an organism described as persisting" (attribution) and shared the "shuffle" figure with spring-onion. Now: several years, soilborne, favored by warm soil; maggot damage is one of the two openings (this record's own claim). |
| cure_and_store | REWRITTEN | previous seasoned note contained "out of the bin" (refused). Now: gentle handling closes the wound entry route; rots from the basal plate in field and storage; damaged bulbs used first (catalog caution). |

## pink-root (fungal) -- 3 rungs, ALL REWRITTEN (record changed in r3)
| method | status | why |
|---|---|---|
| resistant_varieties | NEW | LEAD control: ask the seed supplier which hold up locally, resistance varies with the strain (Setophoma terrestris, penetrates roots without a wound, builds with every onion crop). |
| crop_rotation | NEW | three to six years, WITH the caveat that rotation reduces rather than clears it (fungus persists for years). Carries the record's `75 to 85°F` soil-temperature band in the seasoned register. |
| improve_drainage | NEW | heavy, poorly drained soil makes it worse; stressed plants most susceptible; raised bed as the standard fix on heavy ground comes from the method's own catalog text. |

DROPPED from the previous authoring: `certified_clean_stock` (the corrected record carries no
transplant or clean-stock claim).

## Checks run beyond the validator
- Word and sentence counts per note: all 34 notes between 59 and 88 words, 2 to 4 sentences.
- Absolutes, British spellings, ladder vocabulary, em/en dashes, spaced °F: none.
- Attribution devices (the guidance, 's own, the source, described as, named in/among, listed in/among):
  none in authored notes; "named here" in the water_spray seasoned note is inside the declared
  byte-identical copy and is exempt by design.
- Every temperature figure in the notes appears in the record (one: 75 to 85°F).

## Fixes applied 2026-09-03 (independent review, `review_onion.md`)

Rung count 17 -> 16 (thrips 5 -> 4); the orchestrator's `EXPECTED_RUNGS["onion"]` and
`TOTAL_RUNGS` pins move again. Validator after the fixes: `RESULT: PASS`, 16 rungs across 5 problems,
precedent scan 15 + 2804 comparisons, worst 0.563 (A: onion/onion-thrips/garden_sanitation vs
spring-onion). Every rung not listed below is byte-identical to the r4 authoring; water_spray is
still the declared byte-identical copy of spring-onion's.

- onion-thrips / weed_host_control / both: DROPPED (orchestrator's cross-crop decision: a grain,
  alfalfa and clover SITING claim sat under a WEED-removal method, and the record says nothing about
  weeds; the siting claim stays in the record). Findings #1 and #2 are moot with it.
- onion-thrips / garden_sanitation / beginner (#5): "Thrips ride out the winter in onion material
  lying on the soil, so a bed cleaned at the end of the season carries far fewer of them into next
  spring." -> "... so a bed cleaned at the end of the season gives them less to start from next
  spring." (the record states the overwintering qualitatively, no magnitude)
- botrytis-neck-rot / cure_and_store / seasoned (#8): "This is the harvest-and-after half of the
  control." -> "Neck rot starts at the neck in storage, so it is headed off at lifting and in the
  curing that follows." (identification_seasoned: a rot starting at the neck in storage)
- botrytis-neck-rot / cure_and_store / seasoned (#9): "Cure thoroughly, then store cool and dry; the
  curing and storage conditions belong to onions specifically and differ between crops, so do not
  borrow another crop's figures." -> "Cure thoroughly, then store cool and dry, since an
  insufficiently cured neck is the other opening Botrytis takes." (cause_seasoned: infection of
  immature or insufficiently cured necks)
- fusarium-basal-rot / resistant_varieties / beginner (#11): "Resistance is not offered for every
  onion type, so if you cannot find it, go ahead with the other steps rather than waiting on it." ->
  "Resistance is not offered in every variety, so if you cannot find it, go ahead with rotation and
  gentle handling rather than waiting on it."
- fusarium-basal-rot / resistant_varieties / seasoned (#12): "... resistance is not offered across
  every onion type, so take it where a catalog offers it ..." -> "... resistance is not offered in
  every variety, so take it where a catalog offers it ..." (record says only "where available")
- pink-root / resistant_varieties / beginner (#14): "This is the step that does the most, so start
  here." -> "Of everything you can do about pink root, a resistant variety does the most."
- pink-root / resistant_varieties / seasoned (#13): "The fungus penetrates roots directly without a
  wound and builds with every onion crop on the same ground, which is why resistance, acting in the
  root itself, leads the list." -> "The fungus penetrates roots directly, without a wound, and builds
  with every onion crop on the same ground." (the causal join and the position phrase removed)
- pink-root / improve_drainage / beginner (#15): "... and a plant sitting in waterlogged ground is a
  stressed plant, which is exactly the kind pink root hits hardest." -> "... and it hits weak,
  stressed plants hardest, so a bed that drains well takes away one of the conditions it does best
  in." (drainage and stress kept as the record's two separate facts)
- pink-root / improve_drainage / seasoned (#16): "... so drainage works on both halves of that at
  once: a waterlogged root zone stresses the plant and favors the fungus." -> "...; drainage settles
  the first of those directly." (reviewer's replacement minus its trailing "before planting" clause,
  which the next sentence already carries)

Left byte-identical on purpose (PASS rungs, not in the orchestrator's list): #4 "Once the bulbs are
up" (thrips/garden_sanitation beginner) and #6 the beneficial_predators seasoned join.
