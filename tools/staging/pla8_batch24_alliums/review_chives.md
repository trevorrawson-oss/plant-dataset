# chives -- independent source-truth review of the batch 24 r4 ladders (2026-09-03)

Reviewer did not author `out_chives.json`. Read-only. Inputs: `out_chives.json` (27 rungs, 7 problems),
`chives_source.json` (the corrected record; confirmed against the live canonical `50ffedb0`: thrips,
leafminer, downy, rust prose and white rot are byte-identical to live; onion maggot and botrytis prose +
rust/botrytis anchors are the unpromoted r3/r4 text), `control_methods.json`, `notes_chives.md`,
`findings_chives.md`, `prev_out_chives.json`. `validate_out.py chives crops_data_final.json` -> PASS
(the REFUSED on `scratch_canonical.json` is that fixture still carrying the retired Aphids entry).

Method: every sentence of every note was checked for provenance against the problem's record fields and
the method's catalog text; the eight readable anchors were fetched raw (curl, HTML stripped) and grepped
for each claim; the two pnwhandbooks.org anchors are behind a Cloudflare challenge for curl (403 both via
r.jina.ai and direct) and were read through WebFetch over r.jina.ai with a verbatim section-reproduction
prompt, run twice with agreeing output. Mechanical scans: dashes, absolutes, British spellings,
temperature format, ladder vocabulary, the false-attribution device, Latin in beginner copy, sentence
count, register similarity (difflib, max of both orders), cross-rung and shipped-precedent echo.

## 1. Verdict per rung

| # | problem / method | verdict | one-line reason |
|---|---|---|---|
| 1 | onion-thrips / garden_sanitation | PASS | record-derivable; see R1 (anchor gap) |
| 2 | onion-thrips / water_spray | FIX (low) | seasoned: SYNTHESIS, "which is why a directed water pass reaches them when a general wetting does not"; "blade meets stem" |
| 3 | onion-thrips / beneficial_predators | PASS | record + method caution; see R1 |
| 4 | onion-thrips / insecticidal_soap | PASS | 90°F is the method caution; rinse is the record; see R1 |
| 5 | onion-thrips / spinosad | PASS | device removed; bee caution is the method's; beginner is 0.58 similar to the leafminer spinosad beginner (low) |
| 6 | allium-leafminer / crop_rotation | FIX (low) | seasoned: SYNTHESIS, a mechanism the record does not carry; see R2 |
| 7 | allium-leafminer / garden_sanitation | PASS | record-derivable; see R2 (anchor gap) |
| 8 | allium-leafminer / floating_row_cover | PASS | BEFORE each flight in both registers; trap precondition in both; windows are the record's |
| 9 | allium-leafminer / spinosad | PASS | record + method |
| 10 | onion-maggot / crop_rotation | PASS | pupae in the SOIL around last season's alliums, both registers; distance as well as absence |
| 11 | onion-maggot / garden_sanitation | PASS | culls, volunteers, manure, roguing, no home insecticide; FIT note on "lifted in fall" (perennial) |
| 12 | onion-maggot / floating_row_cover | PASS | at planting, before the spring flight; trap precondition both registers; "flies waiting in its soil" (low) |
| 13 | downy-mildew / airflow_spacing | PASS | 75°F is the record's; all claims record/method |
| 14 | downy-mildew / improve_drainage | FIX (style) | seasoned: "the practices further along" is a ladder-order reference |
| 15 | downy-mildew / water_at_the_base | FIX | beginner WRONG against the record (drops wind, makes splash the route); splash is in neither anchor; see R4 |
| 16 | downy-mildew / garden_sanitation | FIX (style) | seasoned: "the cultural steps above" is a ladder-order reference |
| 17 | chives-rust / airflow_spacing | PASS | moisture + dense stand + airborne urediniospores, all record |
| 18 | chives-rust / balance_nitrogen | PASS | excess nitrogen / lush growth / moderate, record + method |
| 19 | chives-rust / water_at_the_base | PASS | leaf-wetting only, no splash; airborne arrival stated |
| 20 | chives-rust / garden_sanitation | PASS | within the record; see R5 (in-season removal and "fungicides rarely warranted" are in neither anchor) |
| 21 | white-rot / certified_clean_stock | PASS | record + method |
| 22 | white-rot / crop_rotation | FIX | seasoned: "a decade or more" understates the anchor's "over 20 years"; record-level first |
| 23 | white-rot / garden_sanitation | FIX | seasoned WRONG: "they travel with the soil rather than the plant" contradicts record, anchor and its own next sentence |
| 24 | botrytis-leaf-blight-neck-rot / airflow_spacing | PASS | 20 hours, airborne, poor air circulation; no gray mold |
| 25 | botrytis-leaf-blight-neck-rot / water_at_the_base | PASS | no splash; dry before night; "the one variable" (low) |
| 26 | botrytis-leaf-blight-neck-rot / garden_sanitation | PASS | shear + remove, sclerotia on infected leaves, end-of-season, no senescing-leaf removal |
| 27 | botrytis-leaf-blight-neck-rot / crop_rotation | PASS | three years is the record's and UC IPM's ("rotate away from Allium crops for three years") |

PASS 20 / FIX 7 (2 WRONG, 2 UNSUPPORTED, 2 SYNTHESIS, 2 STYLE; rung 15 carries one WRONG and one
UNSUPPORTED). Hard rules that were checked and hold on every rung: no em/en dashes; none of never / always
/ completely / totally / harmless / guaranteed / eliminate; no autumn / bin / colour / practise / whilst /
mould / favour; both temperature figures are `NN°F` with no space and are warranted (90°F = insecticidal
soap caution, 75°F = downy record); no rung / ladder / tier; no false-attribution device in any of the 54
notes (the 11 VERBATIM-reused rungs were each re-read: none carries "the guidance names", "chives'
guidance" or "X's own sourcing"); no binomial in any beginner note; every note is 2 to 4 sentences;
register similarity is 0.02 to 0.47 on every rung (no paraphrase pairs); worst shipped-precedent echo
0.539 (downy water_at_the_base beginner vs garlic), under the 0.70 scan. Timing rules hold: onion maggot
cover "on the day the chives go in, before the spring flies are out" / "from planting ... ahead of the
spring flight"; leafminer cover "before each flight" / "up ahead of each one"; the trap precondition is
in BOTH registers of BOTH floating_row_cover rungs; maggot pupae are "in the soil" in all six maggot
notes that name them, never "residue". Thrips carries no rotation claim. Rust conditions are crowding,
nitrogen and leaf wetting only. Botrytis is foliar, airborne, 20-hour, no gray mold, no splash, no
senescing leaves, three years. No note says "20 to 30".

## 2. Findings table

Severity key: WRONG = contradicts the record or the anchor; UNSUPPORTED = not derivable from the record
or method text (or, marked "(anchor)", derivable from the record but absent from the record's anchoring
document); SYNTHESIS = joins record sentences into a causal claim the record does not make; STYLE; FIT.

| problem | method | register | severity | offending sentence (verbatim) | why | proposed replacement |
|---|---|---|---|---|---|---|
| white-rot | garden_sanitation | seasoned | WRONG | "Rogue out infected plants with the surrounding soil: the sclerotia form in abundance at the base alongside the white mycelium, and they travel with the soil rather than the plant." | Contradicts the record ("avoid spreading infested soil on tools or transplants"; beginner: "Never move infected soil or plants to a clean bed"), the anchor (UC IPM white rot: "Sclerotia can spread throughout a field, or from field to field, via flood water, equipment, or plant material"; "infected transplants and sets can carry sclerotia"), and the note's own next sentence ("The fungus moves in soil, on tools and on transplants"). | "Rogue out infected plants with the surrounding soil: the sclerotia form in abundance at the base alongside the white mycelium, and they leave in the soil around the roots as readily as in the plant itself." |
| downy-mildew | water_at_the_base | beginner | WRONG (vs record) + UNSUPPORTED (anchor) | "Wet blades and splashing water are how this one travels, so watering low takes away part of its route." | The record says "spread by wind and splashing water"; the note drops wind and makes splash THE travel route. The anchor (UC IPM downy mildew) says "Spores are airborne. After landing on healthy plants, they require leaf wetness for infection to occur" and its irrigation instruction is "Minimize canopy leaf wetness: Avoid sprinkler irrigation, especially when the canopy begins to fill"; the word "splash" does not appear on the page. | "The spores ride the wind, so you cannot keep them off, but they need the leaves to stay wet to take hold, and watering low keeps the blades as dry as the weather allows." |
| downy-mildew | water_at_the_base | seasoned | UNSUPPORTED (anchor) | "Basal irrigation removes the splash route and holds leaf wetness to what the weather imposes. The pathogen moves on wind and splashing water and needs long wet periods, so this is the practice half of the defense that spacing sets at planting." | Record-derivable (cause_seasoned: "spread by wind and splashing water"), but the splash clause is absent from the anchor, which carries only airborne spores plus leaf wetness. The sibling botrytis record was corrected this batch on exactly this airborne-not-splash point; downy's record still carries the uncorrected clause and this VERBATIM-reused rung inherits it. | "Basal irrigation holds leaf wetness to what the weather imposes. The spores arrive on the wind and need a long wet period on the blade to infect, so this is the practice half of the defense that spacing sets at planting." (And correct the record's "and splashing water" or anchor it.) |
| white-rot | crop_rotation | seasoned | UNSUPPORTED (anchor: understated) | "Long rotation is the standing management, and its length comes from the sclerotia, which persist for many years and can leave a site unusable for alliums for a decade or more." | Record-derivable (cause_seasoned: "a decade or more"), but the anchor says "can survive in the soil for over 20 years" and "Rotation alone will not control white rot because sclerotia can survive in soil for more than two decades", and the batch rule for white rot is "over 20 years". The chives record was not among the r1 white-rot figure corrections. | "Long rotation is the standing management, and its length comes from the sclerotia, which can survive in the soil for over 20 years and leave a site closed to alliums for that long." Correct `cause_seasoned` first so the rung does not outrun its record; then also "keeping a decade-long problem to the bed that has it" (garden_sanitation seasoned) -> "keeping a twenty-year problem to the bed that has it". |
| onion-thrips | water_spray | seasoned | SYNTHESIS | "Thrips sit down in the leaf axils, the folds where blade meets stem, which is why a directed water pass reaches them when a general wetting does not." | Record: "feeding in the leaf axils and folds" and "Dislodge with a strong water jet". Neither the record nor the method contrasts a directed pass with a general wetting; the "which is why" is the note's own causal claim. Also chives have no stem; the anchor puts them "near where the leaf and bulb meet". | "Thrips sit down in the leaf axils, the folds where one blade wraps the next, so aim the jet into those folds rather than across the open blade." |
| allium-leafminer | crop_rotation | seasoned | SYNTHESIS | "The fly works two flights a year against the same host group, so ground it has already found presents the same target in spring and again in fall." | The record's only rotation claim is "Rotation away from recently infested allium ground reduces carryover"; the mechanism offered (the fly returning to ground it "has already found") is the note's own and is not how carryover works (UMD: "Allium leafminers overwinter as pupae in plant tissue or surrounding soil"). The record does not carry soil overwintering either, so the note cannot state that instead. | "Siting a new planting away from allium ground that was mined recently lowers what carries over into it, and keeping it apart from other allium beds under pressure does the same for what arrives from outside. The fly is specific to the onion family and works two flights a year, spring and fall." (Both sentences are in prevention_seasoned and cause_seasoned.) |
| downy-mildew | improve_drainage | seasoned | STYLE (ladder-order reference) | "On heavy or low-lying ground, correct that first rather than leaning on the practices further along." | "The practices further along" points at the ladder's order, the same internal reference as "the rotation rung" without the word; the promote's vocabulary scan does not see it. VERBATIM-reused rung. | "On heavy or low-lying ground, correct that first rather than leaning on spacing and watering to make up for it." |
| downy-mildew | garden_sanitation | seasoned | STYLE (ladder-order reference) | "Once it is established the home garden has no reliable cure, which is what puts the weight on removing tissue and on the cultural steps above." | "The cultural steps above" is a layout reference into the ladder. VERBATIM-reused rung. | "Once it is established the home garden has no reliable cure, which is what puts the weight on removing tissue and on spacing, drainage and dry foliage." |

Low-severity notes (not counted as FIX; take or leave):

| problem | method | register | severity | sentence | why | suggestion |
|---|---|---|---|---|---|---|
| onion-thrips + allium-leafminer | spinosad | beginner | STYLE (near-duplicate within crop, 0.579) | thrips: "It is hard on bees while it is fresh, so spray at dusk and keep it off a clump that is in flower." / leafminer: "Bees are harmed by it while it is fresh, so spray at dusk and skip any planting that is in flower." | Same three-part caution in the same order; the notes file says the leafminer beginner was rephrased to avoid this, and it is still the closest pair in the crop. | Let the leafminer note carry the method's leafminer-specific fact instead: "It soaks into the leaf, which is how it reaches a maggot tunneling inside where a surface spray cannot." (method: "penetrates leaf tissue to reach protected pests such as leafminers"; record: "larvae tunnel inside onion-family leaves"). |
| onion-maggot | floating_row_cover | beginner | STYLE (imprecise) | "a bed that carried them last season has flies waiting in its soil, and a cover seals them in with the crop" | What waits in the soil is pupae; the record's beginner says "you trap the emerging flies under it". | "has next spring's flies waiting in its soil as pupae, and a cover seals them in with the crop" |
| onion-maggot | garden_sanitation | seasoned | FIT | "plants lifted in fall with their roots carry the pupae out of the ground with them" | Record sentence (prevention_seasoned), but on a perennial chive clump nothing is "lifted in fall" unless a clump is being removed; the instruction reads as an onion practice. | "a clump you do lift in fall, roots and all, carries the pupae out of the ground with it" |
| botrytis-leaf-blight-neck-rot | water_at_the_base | seasoned | STYLE (overclaim) | "which on a perennial cut and regrown all season is the one variable the gardener sets" | Spacing is the other variable the same ladder sets. | "is a variable the gardener sets" |
| allium-leafminer | floating_row_cover | beginner | STYLE (near-absolute) | "since a cover laid after eggs are in the leaves shuts nothing out" | Not on the banned list, but the method says "or it fails" and the maggot seasoned says "it protects little". | "shuts little out" |

## 3. Record-level document-truth findings (the rung author cannot fix these; the record owns them)

R1. **onion-thrips: the single anchor supports almost none of the ladder.** USU "Onions in the Garden"
carries, in full: "Thrips Tiny, slender insects that feed on leaves. Leaves turn silver or gray, may
twist and die. Thrips hide near where the leaf and bulb meet. Thrips are best managed with cultural
practices and natural biological control. Add compost, use mulches or apply a stiff spray of water to
wash thrips from plants." NOT on the page: shear to the base, insecticidal soap, spinosad, minute pirate
bugs, lacewings, hot or dry weather, drought stress, rinsing leaves, cosmetic damage, chives (the word does
not appear). So rungs 1 (shear), 3 (named predators, "usually cosmetic"), 4 (soap, "the same hot, dry
weather thrips build in", rinse) and 5 (spinosad) are record-derivable and anchor-unsupported. Only rung 2
(water spray) and the phrase "natural biological control" are on the page. The record needs a second
anchor that actually carries these claims before the ladder can be called sourced; this review did not
read a candidate and does not name one.

R2. **allium-leafminer: UMD carries no rotation and no leaf removal.** UMD supports: chive host
("chive (A. schoenoprasum)"), the flights ("Adults emerge in late winter (March) into spring (throughout
April, perhaps into May)"; "emerge in the autumn (September / October)"), pupae "in the base of leaves or
into bulbs" and "overwinter as pupae in plant tissue or surrounding soil", punctures, "entry routes for
bacterial and fungal pathogens", cover "in February, prior to the emergence of adults", "Covering fall
plantings during the 2nd generation flight", azadirachtin/spinosad. NOT on the page: "rotation" (0 hits),
"remove", "destroy", "sanitize", "debris", "residue" (0 hits). The record's "Rotation away from recently
infested allium ground reduces carryover" and "remove and destroy mined foliage, and sanitize crop
debris" have no anchor. UMD DOES support the separation claim the catalog cannot key ("Growing leeks as
far as possible from chives has been suggested").

R3. **onion-maggot: well anchored.** UMN: "Root maggots spend the winter as pupae in the soil"; "lay ...
eggs at the base of plant stems"; "more common during cool, wet springs"; "Do not use animal manure or
green manure in your garden in spring. Rotting and decaying organic matter attracts root maggots"; "Do
not place row covers if onions or other root vegetables were planted in the same area the previous year.
Root maggots live through the winter as pupae in the soil near their target plants. Placing a row cover
will trap adults that hatch from the pupae"; "Remove target plants in the fall, including their roots,
and destroy them. This will kill any pupae"; "There are no rescue treatments available once maggots are
already feeding on onions". UC IPM: "Mature larvae pupate in the soil"; "Avoid planting onions near
fields where onions were recently grown ... These fields most likely harbor overwintering onion maggot
pupae"; "Remove and dispose of onion culls and volunteer onions"; "Pesticides are ineffective or
impossible to apply to maggots attacking a standing crop". Minor: in-season roguing of an infested plant
"roots and all" is not verbatim in either (UMN's is fall removal of target plants); row cover timing is
"by the time adult flies are laying eggs, usually early to mid-May" (UMN), which the record's "at
planting, before the flies are out" reads conservatively.

R4. **downy-mildew: splash is not in the anchor.** UC IPM: "Spores are airborne"; "require leaf wetness
for infection"; "Spore production declines at temperatures above 75°F"; "only infects species in the
genus Allium, including garlic, onion, shallot, chives, and leek"; "Avoid sprinkler irrigation"; "Plant
in fields where there is good air movement. Select fields that are well drained"; "Remove and destroy
material of any Allium plants, including residue from the previous crop". "splash" 0 hits. Also not on the
page: shearing a clump to regrow, and "no reliable cure" (the page lists fungicides; the record's framing
is home-garden). The record's cause_seasoned "spread by wind and splashing water" needs the splash clause
sourced or dropped.

R5. **rust: in-season removal and the fungicide framing are in neither anchor.** UC IPM: "In addition
to garlic, onion and chives can be affected severely"; "Reddish airborne spores (urediniospores)";
"between 57º and 75ºF"; "Rotate away from Allium crops for 2 to 3 years, keep Allium fields separated";
"Fungicide sprays may be warranted if more than a few pustules develop". "nitrogen", "dense", "irrigat"
(as a practice) 0 hits. PNW garlic rust: "Avoid dense plantings which favors disease. Avoid over
application of nitrogen, which enhances infections. Avoid wetting of the leaves."; "Plow under infected
plant residues"; no "chive", no "wind"/"airborne", no "remove"; "California isolates did not infect leek,
shallot or elephant garlic." So crowding, nitrogen and leaf wetting are anchored (PNW), airborne spores
and the chives host claim are anchored (UC IPM), and the record's "cut off and destroy rusty leaves or
shear the clump" and "Fungicides are rarely warranted in a home planting" are anchored nowhere; rung 20
follows the record on both.

R6. **white-rot: the anchor says over 20 years, the record says a decade.** UC IPM: "can survive in the
soil for over 20 years"; "Rotation alone will not control white rot because sclerotia can survive in soil
for more than two decades"; "the size of a pin head or poppy seed"; "via flood water, equipment, or plant
material"; "infected transplants and sets can carry sclerotia"; "plant only clean stock from known
origins"; "do not move cull bulbs, litter, and soil from infested to noninfested fields. Always clean the
soil off of equipment". Not on the page: "chive" (0 hits), roguing infected plants with soil ("remove",
"rogue", "destroy" 0 hits), a flat "no cure".

R7. **botrytis: strongly anchored; neither anchor names chives (the record says so itself).** UC IPM:
"Leaf surfaces must be wet from dew or rain for long periods (20 or more hours) for leaf spots to
develop"; "spores are airborne"; "sclerotia ... can persist in soil for months to years"; "Poor air
circulation in the onion canopy also favors the disease. This may occur when onions are planted too
closely together"; "rotate away from Allium crops for three years. Destroy volunteer and cull onions";
"Time sprinkler irrigation to prevent extended leaf wetness". PNW: "overwinters in cull piles, in field
debris, or in soil. Wind disperses the spores. Cool temperatures (55°F to 75°F) and long periods of leaf
wetness"; "Get rid of cull piles and debris"; "Rotate field out of allium crops at least 2 to 3 years";
"Avoid extended overhead irrigation". "splash", "neck rot", "gray mold" 0 hits on both. Not anchored:
shear-to-regrow; "Fungicides are seldom warranted" (UC IPM: "apply a fungicide at the first evidence of
leaf spotting", commercial). The name "Botrytis (leaf blight and neck rot)" still promises a neck rot no
field or anchor describes (batch findings 6.1 stands).

## 4. FIT calls

- The shear-the-clump reset inside `garden_sanitation` (thrips, downy, rust, botrytis): KEEP as keyed. It
  is a whole-plant in-season reset rather than debris cleanup, but no other catalog key reaches it, the
  brief placed it there by design, and every note also carries the method's own removal/destroy content.
- `improve_drainage` on downy mildew: KEEP. The method text is root-rot shaped, but the record carries
  "poorly drained plantings hold it" / "site in well-drained sun" and the anchor carries "Select fields
  that are well drained".
- `crop_rotation` on allium leafminer: KEEP the rung (the record carries the claim) but rewrite the
  seasoned mechanism (finding above) and flag the record's anchor gap (R2).
- `crop_rotation` on botrytis (NEW rung): KEEP; "three years" is in the record and verbatim in UC IPM.
- `water_at_the_base` on downy mildew: KEEP the rung, REWRITE both registers to the leaf-wetness
  mechanism (findings above); the method's "shortens the leaf-wetness period" half is what the anchor
  supports.
- Nothing to DROP.

## 5. URL table

| url | status | how read | what it carries for chives |
|---|---|---|---|
| https://extension.usu.edu/yardandgarden/research/onions-in-the-garden | 200 | curl raw, HTML stripped, grepped; WebFetch summary agrees | thrips: hiding site, silver/gray leaves, "stiff spray of water", "natural biological control"; nothing else the record claims |
| https://extension.umd.edu/resource/allium-onion-leafminer | 200 | curl raw, grepped | chive host, flights, pupae in tissue/soil, February cover before emergence, fall cover, spinosad/azadirachtin, leek-chive separation; NO rotation, NO removal/sanitation |
| https://extension.umn.edu/yard-and-garden-insects/root-maggots | 200 | curl raw, grepped | pupae in soil, base of stems, cool wet springs, spring manure, culls, row cover timing + trap precondition + mechanism, rotation, fall removal with roots, no rescue |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/maggots/ | 200 | curl raw, grepped | pupate in soil, overwintering pupae near previous onions, culls and volunteers, rotation + distance, pesticides ineffective on a standing crop; no row cover |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/downy-mildew/ | 200 | curl raw, grepped | airborne, leaf wetness, 75°F, chives named, avoid sprinklers, air movement, well drained, residue removal, 3-year rotation; NO splash |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/rust/ | 200 | curl raw, grepped | chives "affected severely", airborne urediniospores, 57 to 75°F, 2 to 3 year rotation, separation, volunteers; NO nitrogen, NO crowding, NO irrigation practice, NO leaf removal |
| https://pnwhandbooks.org/plantdisease/host-disease/garlic-allium-sativum-rust | curl: 403 Cloudflare challenge via r.jina.ai; direct curl blocked by sandbox permission | READ via WebFetch over r.jina.ai, verbatim section reproduction, two prompts agreeing | dense plantings, over-application of nitrogen, "Avoid wetting of the leaves", plow under residues, 2 to 3 years; NO chives, NO wind/airborne, NO remove |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/white-rot/ | 200 | curl raw, grepped | "over 20 years" / "more than two decades", poppy seed, spread via water/equipment/plant material, transplants and sets, clean stock, do not move soil, clean equipment, long rotation; NO chives, NO roguing |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/botrytis-leafspot/ | 200 | curl raw, grepped | 20+ hours, airborne, sclerotia months to years, poor air circulation / too close, 12-inch spacing, time sprinklers, three years, culls and volunteers; NO chives, NO splash, NO neck rot |
| https://pnwhandbooks.org/plantdisease/host-disease/onion-allium-cepa-botrytis-leaf-blight | curl: 403 Cloudflare challenge via r.jina.ai; direct curl blocked by sandbox permission | READ via WebFetch over r.jina.ai, verbatim section reproduction, two prompts agreeing | overwinters in cull piles/debris/soil, wind, 55 to 75°F, get rid of culls and debris, at least 2 to 3 years, avoid extended overhead irrigation; NO chives, NO sclerotia by name, NO 20 hours, NO splash |

Raw text of the eight curl-read pages is in the session scratchpad under `docs/` (not in the repo).
