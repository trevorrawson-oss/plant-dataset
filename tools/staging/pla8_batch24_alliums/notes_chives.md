# chives -- batch 24 r4 authoring notes (2026-09-03)

Authored against `chives_source.json` (byte-identical to the chives record in `r4_candidate.json`,
checked field by field before writing). Ids and types from `pinned_ids.json` verbatim. 7 problems,
27 rungs (was 8 problems / 30 rungs with the retired Aphids entry).

Legend: VERBATIM = prev rung reused unchanged after re-reading against the current record;
EDITED = prev rung kept in shape but one or both registers rewritten; NEW = rung did not exist.

## onion-thrips (insect) -- record unchanged -- 5 rungs
| method | status | why |
|---|---|---|
| garden_sanitation | VERBATIM | the shear-to-the-base reset; every claim in the record |
| water_spray | VERBATIM | hosing into the leaf folds; morning timing is the method's own caution |
| beneficial_predators | VERBATIM | lacewings + minute pirate bugs; "hold off broad sprays" is the method's caution |
| insecticidal_soap | VERBATIM | 90°F is the method's caution text; rinse-before-use is the record |
| spinosad | EDITED (both registers) | seasoned carried "chives' guidance names", the false-attribution device; beginner and seasoned both claimed "chive blooms draw bees and hoverflies", which is in neither the record nor the method text. Rewritten to the method's bee caution + the record's rinse instruction |

Note: the previous validator run never checked any pest rung (the 4-vs-3 length mismatch
short-circuits the pests loop), so every VERBATIM pest rung above was re-read by hand, not
inherited as "already passed".

## allium-leafminer (insect) -- record unchanged -- 4 rungs
| method | status | why |
|---|---|---|
| crop_rotation | VERBATIM | "rotation away from recently infested allium ground reduces carryover" |
| garden_sanitation | VERBATIM | mined leaves + pupae in leaf bases + debris; secondary rots from the record |
| floating_row_cover | EDITED (both registers) | beginner lacked BEFORE and lacked the trap precondition; seasoned's precondition was phrased "ground that did not grow", which the promote's TRAP pattern does not read. Now: cover before each flight (spring, and before September for the fall flight), both registers carry the trap precondition, seasoned gives the record's March-into-May / September-into-October windows |
| spinosad | EDITED (both registers) | seasoned carried the "chives' guidance names" device; beginner rephrased so it is not a near-duplicate of the thrips spinosad beginner |

## onion-maggot (insect) -- record CHANGED -- 3 rungs, all re-authored
| method | status | why |
|---|---|---|
| crop_rotation | EDITED (re-authored) | off last year's allium ground AND away from it; mechanism is pupae overwintering in the SOIL around last season's alliums (prev said "residue") |
| garden_sanitation | EDITED (re-authored) | culls, volunteer alliums, lifted plants with roots (pupae leave with them), spring manure and green manure out (rotting organic matter draws the fly), rogue infested plants; no home-garden insecticide |
| floating_row_cover | EDITED (re-authored) | on AT PLANTING, BEFORE the spring flight (prev said "early in spring" / "at emergence"-adjacent); trap precondition now in BOTH registers (prev beginner had none) |

## downy-mildew (fungal) -- record unchanged -- 4 rungs
| method | status | why |
|---|---|---|
| airflow_spacing | VERBATIM | 75°F is in the record |
| improve_drainage | VERBATIM | "soggy, shaded, crowded", "site in well-drained sun"; heavy/low-lying is the method text |
| water_at_the_base | VERBATIM | splash IS this record's mechanism ("spread by wind and splashing water") |
| garden_sanitation | VERBATIM | remove infected foliage; shear to regrow in drier weather; no reliable cure |

## chives-rust (fungal) -- record CHANGED -- 4 rungs, all re-authored
| method | status | why |
|---|---|---|
| airflow_spacing | EDITED (re-authored) | prev seasoned carried "the guidance names"; now moisture + dense stand + airborne urediniospores from the corrected record |
| balance_nitrogen | EDITED (re-authored) | excess nitrogen / lush high-nitrogen growth; moderate nitrogen |
| water_at_the_base | EDITED (re-authored) | airborne spores, so this shortens leaf wetness rather than stopping arrival |
| garden_sanitation | EDITED (re-authored) | shear / remove spotted blades early; end-of-season debris; fungicides rarely warranted |

## white-rot (fungal) -- record unchanged -- 3 rungs
| method | status | why |
|---|---|---|
| certified_clean_stock | EDITED (seasoned only) | prev seasoned's "the decision made before anything reaches the ground" paraphrased spring-onion's shipped certified_clean_stock seasoned ("the decision that carries the most weight here because it is made before anything reaches the ground"). Passed the 0.70 scan but the rule is no paraphrase, so rephrased. Beginner VERBATIM |
| crop_rotation | VERBATIM | sclerotia / decade or more / quarantine; all record |
| garden_sanitation | EDITED (both registers) | prev seasoned lifted "treat the soil itself as a thing that moves" word for word from garlic's shipped white-rot garden_sanitation seasoned, and the beginner closely tracked garlic's beginner. Both rewritten from the record |

## botrytis-leaf-blight-neck-rot (fungal) -- record CHANGED -- 4 rungs, all re-authored
| method | status | why |
|---|---|---|
| airflow_spacing | EDITED (re-authored) | no "gray mold"; 20-or-more-hours leaf wetness; airborne spores; poor air circulation |
| water_at_the_base | EDITED (re-authored) | no splash; time watering so foliage dries before night |
| garden_sanitation | EDITED (re-authored) | prev seasoned carried "the guidance names" and told the reader to strip senescing leaves in-season; now shear + remove cut foliage (sclerotia form on infected leaves), end-of-season debris and culls, fungicides seldom warranted |
| crop_rotation | NEW | three years off ground that carried diseased alliums; sclerotia persist months to years |

## Tally
VERBATIM 11 rungs, EDITED 15 rungs, NEW 1 rung (computed from the per-rung statuses above: 4+2+4+1 / 1+2+3+4+2+3 / 1). Temperature figures: 2 (75°F downy mildew,
90°F insecticidal soap), down from 3 because the retired Aphids ladder carried the third 90°F.

## Fixes applied 2026-09-03

Applied from `review_chives.md` (independent source-truth review). Every PASS rung is byte-identical to the
r4 file; 7 notes on 6 rungs were edited; `validate_out.py chives r4_candidate.json` -> PASS (27 rungs / 7
problems; worst precedent echo 0.612, down from 0.617). No claim was added that is not in the record or the
method text. Both temperature figures (75°F, 90°F) stand.

| problem / method / register | old sentence | new sentence |
|---|---|---|
| onion-thrips / water_spray / seasoned (SYNTHESIS) | "Thrips sit down in the leaf axils, the folds where blade meets stem, which is why a directed water pass reaches them when a general wetting does not." | "Thrips sit down in the leaf axils, the folds where one blade wraps the next, so aim the jet into those folds rather than across the open blade." (record: "feeding in the leaf axils and folds", "Dislodge with a strong water jet"; chives have no stem) |
| allium-leafminer / crop_rotation / seasoned (SYNTHESIS) | "Siting a new planting away from allium ground that was mined recently lowers what carries over into it. The fly works two flights a year against the same host group, so ground it has already found presents the same target in spring and again in fall." | "Siting a new planting away from allium ground that was mined recently lowers what carries over into it, and keeping it apart from other allium beds under pressure does the same for what arrives from outside. The fly is specific to the onion family and works two flights a year, spring and fall." (record: prevention_seasoned "separate new plantings from pressured allium beds"; cause_seasoned "allium-specific fly with a spring flight ... and a fall flight") |
| downy-mildew / improve_drainage / seasoned (STYLE, order reference) | "On heavy or low-lying ground, correct that first rather than leaning on the practices further along." | "On heavy or low-lying ground, correct that first rather than leaning on spacing and watering to make up for it." |
| downy-mildew / water_at_the_base / beginner (WRONG vs record) | "Wet blades and splashing water are how this one travels, so watering low takes away part of its route." | "This disease travels on the wind, so you cannot keep it from arriving, but it needs wet leaves to take hold, and watering low keeps the blades dry for as long as the weather lets you." (record: "spread by wind ... long leaf-wetness periods"; method: "need the foliage to stay wet to take hold") |
| downy-mildew / water_at_the_base / seasoned (UNSUPPORTED, splash) | "Basal irrigation removes the splash route and holds leaf wetness to what the weather imposes. The pathogen moves on wind and splashing water and needs long wet periods, so this is the practice half of the defense that spacing sets at planting." | "Basal irrigation holds leaf wetness to what the weather imposes. The pathogen arrives on the wind and needs a long wet period on the blade to infect, so this is the practice half of the defense that spacing sets at planting." |
| downy-mildew / garden_sanitation / seasoned (STYLE, order reference) | "... which is what puts the weight on removing tissue and on the cultural steps above." | "... which is what puts the weight on removing tissue and on spacing, drainage and dry foliage." (record: "Open the canopy by dividing, water at the base, site in well-drained sun") |
| white-rot / garden_sanitation / seasoned (WRONG) | "Rogue out infected plants with the surrounding soil: the sclerotia form in abundance at the base alongside the white mycelium, and they travel with the soil rather than the plant. The fungus moves in soil, on tools and on transplants, so sanitize tools after working the infested spot and do not carry divisions or soil out of it; ..." | "Rogue out infected plants with the surrounding soil: the sclerotia form in abundance at the base alongside the white mycelium, and they move on soil, on tools and on planting material. Sanitize tools after working the infested spot and do not carry divisions or soil out of it; ..." (record: "avoid spreading infested soil on tools or transplants"; the now-redundant second-sentence clause was folded in) |

HELD, not changed: white-rot / crop_rotation / seasoned (reviewer row "understated vs anchor"). The rung
already carries the record's own persistence wording verbatim ("persist for many years", "a decade or
more"), and the instruction is to keep the record's figure rather than invent one from the anchor. The
"over 20 years" correction is a record-level item (review R6) and belongs to the record, after which this
rung and the "decade-long problem" clause in white-rot / garden_sanitation seasoned follow it. The
reviewer's low-severity "take or leave" rows were not applied.
