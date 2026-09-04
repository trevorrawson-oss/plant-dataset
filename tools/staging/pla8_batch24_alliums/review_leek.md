# review_leek.md -- independent source-truth review of the leek IPM ladders (PLA-8 batch 24)

Reviewer: independent (did not author `out_leek.json`). Date: 2026-09-03. Read-only; nothing in the repo was edited.

Inputs read in full: `out_leek.json` (29 rungs / 7 problems), `leek_source.json`, the 14 catalog entries used
(`control_methods.json`), `notes_leek.md`, `findings_leek.md`, `validate_out.py`, and ALL 18 anchoring
documents (fetched raw and read, not summarized; see the URL table at the end).

Mechanical pass, re-run here rather than trusted from the author's notes:
- `validate_out.py leek crops_data_final.json` -> `RESULT: PASS`, 29 rungs, precedent worst 0.553.
- My own regexes: 0 em/en dashes, 0 banned absolutes, 0 British spellings, 0 ladder vocabulary, 0 spaced
  `°F`, 0 Latin names in any `note_beginner`, every note 2 to 5 sentences, register similarity max 0.22
  (difflib, both orders), 6 temperature figures (50°F x4, 75°F, 59°F), all in the record.

## 0. One dependency the orchestrator must see first

`leek_source.json` is NOT the canonical leek record. Canonical `crops_data_final.json` is at `50ffedb0`
(allium corrections **r2**), and its leek record still says, verbatim:
- onion thrips `management_seasoned`: "Keep plants vigorous and evenly watered, hose off light infestations,
  and **rotate away from alliums**; treat persistent outbreaks per local extension guidance." (sources
  `usu_ext`, `umn_ext`)
- onion maggot `management_seasoned`: "Rotate away from alliums, remove cull plants and crop residue, and use
  floating row cover **at establishment** to block egg-laying." (sources `usu_ext`, `umn_ext`)
- pink root `management_seasoned`: "Rotate away from alliums for several years, **start with clean
  transplants**, and keep plants unstressed and evenly watered." (sources `uf_ifas`; severity `medium`)

`leek_source.json` carries the r3/r4 candidate versions (thrips re-sourced to osu/umass/uc_ipm/umd with no
rotation claim; maggot with uc_ipm and "from planting day, before the spring flight"; pink root re-sourced
to uc_ipm/usu/uf_ifas, severity `low`, no clean-stock claim). The ladders below are correct AGAINST THE
CANDIDATE and would carry three claim-provenance defects (no thrips rotation, no maggot "at establishment",
no pink-root clean stock) if promoted against the r2 canonical. **`out_leek.json` must land after r3 and
r4, never before.** The validator passed against canonical only because its record checks are shape and
number checks, not claim checks.

## 1. Verdict per rung

| # | problem | method | verdict | one-line reason |
|---|---|---|---|---|
| 1 | onion-thrips | garden_sanitation | PASS | every claim in record; UMass/PNW verified |
| 2 | onion-thrips | weed_host_control | **FIX** | seasoned says cultivate "while the crop is still small"; PNW says that INCREASES thrips; beginner says "before the leeks are up" |
| 3 | onion-thrips | balance_nitrogen | **FIX** (style) | beginner "handles the feeding it does get better" uses "feeding" in two senses in one clause |
| 4 | onion-thrips | water_spray | PASS | UMD "strong jet of plain water from a garden hose" verified |
| 5 | onion-thrips | beneficial_predators | PASS | UMass/UC IPM/UMD verified |
| 6 | leek-moth | crop_rotation | **FIX** (synthesis, low) | seasoned implies rotation covers the later generations |
| 7 | leek-moth | planting_time_avoidance | PASS | all figures in record and in Cornell doc_764 |
| 8 | leek-moth | garden_sanitation | PASS | minor redundancy in seasoned sentences 1 and 2 |
| 9 | leek-moth | floating_row_cover | PASS | every timing element present in both registers; one 60-word sentence |
| 10 | leek-moth | handpick | PASS | Cornell lists "removal of larvae from the plant"; keep the method |
| 11 | leek-moth | spinosad | **FIX** | beginner adds "male moths" (unsupported) and uses "Bt" unexplained; sentence 2 unreadable |
| 12 | onion-maggot | crop_rotation | PASS | UMN/UC IPM verified; pupae in SOIL, correct |
| 13 | onion-maggot | planting_time_avoidance | **FIX** (synthesis) | both registers tie the planting-date mechanism to weather instead of the first flight |
| 14 | onion-maggot | garden_sanitation | PASS | UMN verified line by line |
| 15 | onion-maggot | floating_row_cover | **FIX** (synthesis, low) | seasoned invents a cover duration ("through the cool, wet early-season stretch") |
| 16 | allium-leafminer | crop_rotation | PASS | Cornell verified; "exposed twice" is loose but harmless |
| 17 | allium-leafminer | planting_time_avoidance | PASS | Cornell/UMD/UMass verified |
| 18 | allium-leafminer | garden_sanitation | PASS | Cornell/UMass verified |
| 19 | allium-leafminer | floating_row_cover | PASS | before-each-flight, 8 weeks, two-weeks-late, trap precondition, all verified in UMass/Cornell |
| 20 | allium-leafminer | spinosad | PASS | UMass "applied 2 times, 2-4 weeks after first detecting" verified |
| 21 | leek-rust | airflow_spacing | PASS | 57 to 75°F / 59°F verified in UC IPM; note the literal "midsummer" hit |
| 22 | leek-rust | balance_nitrogen | PASS | PNW "Avoid over application of nitrogen" verified |
| 23 | leek-rust | water_at_the_base | PASS | PNW "Avoid wetting of the leaves" verified |
| 24 | leek-rust | garden_sanitation | PASS | UC IPM/PNW volunteers verified |
| 25 | leek-rust | crop_rotation | **FIX** | seasoned ranks methods ("as much weight as the years", "do most of the work") and names three sibling methods |
| 26 | white-rot | certified_clean_stock | PASS | "over 20 years", "a few ... per soil sample": record's figure, no pounds/kg |
| 27 | white-rot | garden_sanitation | PASS | UC IPM "do not move cull bulbs, litter, and soil" verified |
| 28 | pink-root | crop_rotation | PASS | 3 to 6 years, caveat, other hosts, all verified in UC IPM |
| 29 | pink-root | improve_drainage | **FIX** (synthesis, low) | seasoned asserts a mechanism ("works on the host's condition rather than on the inoculum") the record does not give |

**PASS 21 / FIX 8** (1 WRONG, 3 UNSUPPORTED, 4 SYNTHESIS, 4 STYLE items; some rungs carry more than one).

Orchestrator's named checks, all confirmed clean:
- Leek moth: cover BEFORE emergence (~50°F, "sometimes as early as March") or planting day, season-long, not
  lifted between flights; two to three generations; injury June through September; trap precondition in both
  registers. No "during the flights", "May to June", "August to October" or "two generations" anywhere.
- Allium leafminer: before each flight, "by late March" / "by early September", "about eight weeks", two
  weeks late = more larvae, spring "late March through April, sometimes into May", fall "September into
  October"; trap precondition both registers. No "March to April and September to November", no "during
  the flight".
- Onion maggot: cover "on the day you plant them ... before the spring flies"; pupae "in the soil", never
  "residue"; no "at emergence"; trap precondition both registers.
- Thrips: zero rotation claims; vigor framed as tolerance ("buys tolerance of the rasping rather than fewer
  insects").
- Leek rust: cool framing 57 to 75°F; no variety recommendation; no "autumn"; "midsummer" appears once as a
  NEGATION (see finding 21).
- Pink root: no clean-stock claim; rotation caveat in both registers; no variety claim.
- White rot: "over 20 years" / "more than 20 years", never "20 to 30"; no pounds or kilogram figure.

## 2. Findings table

Severity key: WRONG = contradicts the record or an anchoring document; UNSUPPORTED = not derivable from the
record or the method's catalog text; SYNTHESIS = joins record sentences into a causal claim the record does
not make; STYLE = hard style rule or readability; FIT = method choice.

| # | problem | method | register | severity | offending sentence (verbatim) | why | proposed replacement |
|---|---|---|---|---|---|---|---|
| 2a | onion-thrips | weed_host_control | seasoned | **WRONG** | "Cultivate weedy margins early in the season, while the crop is still small, because thrips move off weeds as those dry down and the crop then takes the population in one pulse." | The record says "cultivate weedy edges early in the year, before they dry down"; the catalog says "the clearance is worth most before the crop emerges"; the anchoring PNW page says, verbatim, "Cultivating nearby weedy areas early in the year reduces the potential of a thrips problem when the weeds begin to dry out. **Cultivating weedy areas after plant emergence may increase thrips problems.**" "While the crop is still small" is after emergence, which is the timing the source warns against, and it contradicts this rung's own beginner register ("before the leeks are up"). "In one pulse" is an unsupported flourish. | "Cultivate weedy margins early in the year, before the crop is up, because thrips move off weeds as those dry down and onto whatever allium is standing." |
| 2b | onion-thrips | weed_host_control | beginner | UNSUPPORTED (low) | "Weeds that dry down later in the season push thrips off themselves and onto the crop, so a rough margin left standing sends the pest your way at the worst time." | "At the worst time" is not in the record (the record gives no timing for the weed-to-crop move relative to crop stage). Harmless, but a flourish. | "Weeds that dry down later in the season push thrips off themselves and onto the crop, so a rough margin left standing sends the pest your way." |
| 2c | onion-thrips | weed_host_control | both | FIT | "A patch of grain, alfalfa or clover next door does the same when it dries or is cut, so give the bed some distance from one." / "Small grains, alfalfa and clover shed thrips the same way when they dry or are cut, so site leeks away from those plantings where you have the choice." | The author's own doubt. These are host CROPS, not weeds, but the catalog mechanism is "Weedy alternate hosts are a reservoir ... For thrips it is the same move, to control nearby weeds that are alternate hosts", and the catalog cons already concede "a reservoir over the fence is outside what you can clear". The sentence is honest that these are crops and gives a siting action. **KEEP.** Document nuance for the record, not the rung: UMass says these crops shed thrips "when these crops are cut or harvested"; the "dry" half comes from PNW/UC IPM sentences about weeds and grasslands, so the record's "when they dry or are cut" merges two sources. | none |
| 3 | onion-thrips | balance_nitrogen | beginner | STYLE | "A plant that is fed properly but not pushed also handles the feeding it does get better, which on this pest is a large part of what you can do." | "Feeding" has just meant fertilizer in the previous sentence and here means thrips feeding; a beginner reads "handles the feeding it does get" as "handles the fertilizer". The tolerance claim itself is in the record ("vigor buys tolerance of the feeding, not fewer thrips"). | "A plant that is fed properly but not pushed also stands up to the thrips' rasping better, and on this pest that tolerance is a large part of what you can do." |
| 5 | onion-thrips | beneficial_predators | seasoned | (note, no fix) | "Conservation is the whole of the practice: nothing is bought or released, and what protects it is keeping broad-spectrum materials off the bed." | Not in the leek record; supported by the catalog ("Conserving resident natural enemies") and by the anchoring UMD page ("You do not need to purchase predators to eat thrips on outdoor plants"). Acceptable. | none |
| 6 | leek-moth | crop_rotation | seasoned | SYNTHESIS (low) | "Acrolepiopsis assectella overwinters as an adult in sheltered plant debris, so a bed that carried alliums is a source of the first flight in its own right, and with two to three generations following from mid-April into late August a planting left in place is exposed all season." | The first half is derivable (record `management_beginner` ties the moths in "that old debris" to the bed). The second half attaches the later flights to rotation: the record says nothing about where the second and third generations come from, and rotation only addresses the overwintered adults in the old bed's debris; the later flights arrive on the wing regardless of bed. The clause reads as a benefit rotation does not confer. | "Acrolepiopsis assectella overwinters as an adult in sheltered plant debris, so a bed that carried alliums is a source of the first flight in its own right. Rotation addresses that overwintered generation only; the mid-June and late-July flights arrive on the wing, which is what the cover is for." |
| 7 | leek-moth | planting_time_avoidance | seasoned | STYLE (optional) | "Adults emerge when spring temperatures reach about 50°F, sometimes in a March warm spell, and New York records the first flight around mid-April to mid-May, so a transplanting set after that window escapes the first round of egg-laying." | "New York records" is a sentence claiming what a source observed. It is the record's own phrasing ("New York records two to three generations a year") and a regional anchor the date needs, so I would not fail it; flagged because the brief bans "any sentence claiming what a source says". | "... and in New York the first flight runs around mid-April to mid-May, so ..." |
| 8 | leek-moth | garden_sanitation | seasoned | STYLE (low) | "Adults overwinter in sheltered plant debris, so the end-of-season clearance of allium residue is what lowers the overwintering population before the first spring flight. Clear it at the end of the season and remove it from the site rather than leaving it on the surface." | Sentence 2 restates sentence 1's "end-of-season clearance". | "Adults overwinter in sheltered plant debris, so clearing allium residue at the end of the season is what lowers the overwintering population before the first spring flight. Remove it from the site rather than leaving it on the surface." |
| 9 | leek-moth | floating_row_cover | seasoned | STYLE (low) | "Exclusion is the main control at garden scale and its timing decides it: insect netting or row cover goes on before the overwintered adults emerge, at about 50°F in early spring, or on the day of transplanting if that is later, sealed at the edges and left in place through all two to three generations rather than lifted between them." | 60 words in one sentence. Content is correct and complete. | Split after "if that is later.": "Seal the edges and leave it in place through all two to three generations rather than lifting it between them." |
| 11a | leek-moth | spinosad | beginner | UNSUPPORTED | "Time it to the moths: a pheromone trap, a lure that draws the male moths and shows when a wave peaks, set out by mid-April, tells you when, and the spray goes on 7 to 10 days after that peak." | "Male" is in neither the record ("A pheromone trap set by mid-April shows when each flight peaks"), the catalog, nor Cornell doc_764 ("Pheromone lures are placed on a sticky card"). True in general, not derivable here. The sentence is also structurally unreadable (four nested clauses) for a beginner register. | "Time it to the moths. A pheromone trap, a scented lure that catches the adults and shows when a wave peaks, goes out by mid-April, and the spray goes on 7 to 10 days after that peak." |
| 11b | leek-moth | spinosad | beginner | STYLE | "Bt did not make a real dent in the caterpillars in testing, so do not count on it." | "Bt" is an unexplained abbreviation in the beginner register (the rule: terms explained in-line). | "Bt, the bacterial caterpillar spray sold for cabbage worms, did not make a real dent in these caterpillars in testing, so do not count on it." |
| 11c | leek-moth | spinosad | seasoned | (document note) | "Spinosad applied 7 to 10 days after a peak flight is the organic material with trial support against this moth." | This is the record's sentence, so the rung is in order. But doc_764's support is narrower than "trial support" suggests: "**Laboratory** studies indicated that all but DiPel significantly reduced leek moth larval populations", the 7-10 day timing is "Canadian research ... pheromone traps alone can be used to properly time insecticide applications", and the guide adds "These insecticides need to be tested for their effectiveness under field conditions". Record-level wording, flagged for the orchestrator. | (record decision) "the organic material with laboratory support against this moth" |
| 13a | onion-maggot | planting_time_avoidance | beginner | SYNTHESIS | "The maggots hit hardest in the cool, wet weather of early spring, when young plants are just settling in, so a planting that goes in after that stretch misses the worst of it." | The record's mechanism for delayed planting is the FIRST FLIGHT ("Planting later in spring, once the first flight has passed, also sidesteps the worst of it"); "stand loss is worst in cool, wet conditions early in the season" is a separate identification sentence. The rung makes the weather the thing being dodged. UC IPM's mechanism is explicit: "This will avoid the first generation of egg-laying by adult flies that overwintered in the soil". | "The first flies of spring lay on young plants just after they go in, so a planting set after that first flight has passed misses the heaviest egg-laying." |
| 13b | onion-maggot | planting_time_avoidance | seasoned | SYNTHESIS (low) | "Planting later in spring, after the first flight has passed, sidesteps the heaviest egg-laying, which falls on young transplants in cool, wet conditions early in the season." | Same join: the record says cool, wet springs favor the MAGGOTS, not that egg-laying falls in cool, wet conditions. | "Planting later in spring, after the first flight has passed, sidesteps the first round of egg-laying, which is the one that falls on young transplants; a cool, wet spring makes the resulting larvae worse." |
| 15 | onion-maggot | floating_row_cover | seasoned | SYNTHESIS (low) | "Keep it in place through the cool, wet early-season stretch when stand loss peaks." | The record gives no cover duration; it says on "from planting day, before the spring flight". Tying removal to weather invents a schedule. The anchoring UMN page's duration is the flight, not the weather: "Keep the barrier in place until the end of the month when the flies are finished laying eggs." | "Keep it in place through the spring flight, which is the egg-laying that costs stand." |
| 16 | allium-leafminer | crop_rotation | seasoned | (note, no fix) | "... and with a spring flight from late March and a fall flight from about September the same bed is exposed twice." | Loose (every bed is exposed to both flights); as an emergence-site claim it is derivable from the record ("the pupae rest through summer"). Not worth a rewrite. | none |
| 21 | leek-rust | airflow_spacing | seasoned | STYLE (orchestrator call) | "The disease tracks cool, damp spring and fall weather rather than midsummer, so the layout matters most for the stretches leeks spend in cool conditions." | Literal hit on the brief's "no mid-summer" ban. It is the record's own sentence ("so it tracks cool damp spring and fall weather rather than midsummer") and a NEGATION that supports the cool-weather framing, so the sense is right. If the ban is literal: | "... rather than summer heat, so ..." |
| 21/24/25 | leek-rust | airflow_spacing, garden_sanitation, crop_rotation | both | STYLE (low) | "On leeks the cultural steps are usually enough, since they carry rust better than garlic does." / "Leek is a comparatively resistant host, and spacing plus the other cultural steps usually carry it." / "On leek this and the other cultural steps are usually what carries it." / "Rotation is a supplement here; on leek, a comparatively resistant host, the airflow, nitrogen and watering steps do most of the work." | The same record sentence ("On leek the cultural steps usually carry it") is restated in four rungs. One of the five should carry it. | Keep it in airflow_spacing (both registers); drop from garden_sanitation seasoned and crop_rotation seasoned. |
| 25a | leek-rust | crop_rotation | seasoned | UNSUPPORTED | "Spores are airborne, so the separation carries as much weight as the years: a fresh bed beside a rusted one is within reach of its spores." | The record lists both ("two to three years off that ground and separated from an infected planting") and ranks neither; "as much weight as the years" is the author's weighting. UC IPM verbatim: "Rotate away from Allium crops for 2 to 3 years, keep Allium fields separated to prevent movement, and destroy volunteer Allium plants during this period." | "Spores are airborne, so the separation matters as well as the years: a fresh bed beside a rusted one is within reach of its spores." |
| 25b | leek-rust | crop_rotation | seasoned | UNSUPPORTED + ladder-describing | "Rotation is a supplement here; on leek, a comparatively resistant host, the airflow, nitrogen and watering steps do most of the work." | The record does not call rotation a supplement or say the other steps "do most of the work"; rotation is one of the cultural steps the record says "usually carry it". The sentence also names three sibling methods, which is a note describing the ladder rather than the world (it goes false if a rung is added or dropped). | "On leek, a comparatively resistant host, this is one of the cultural steps that usually carry the disease without a spray." (or drop the sentence; see the repetition row) |
| 29a | pink-root | improve_drainage | seasoned | SYNTHESIS (low) | "The fungus infects roots directly and takes weak or stressed plants first, so drainage works on the host's condition rather than on the inoculum, and it does nothing for a plant whose roots are already pink." | The record gives the instruction ("use raised or well-drained beds where soil sits wet") and, separately, the susceptibility fact ("weak or stressed plants are the most susceptible"); it does not say drainage works THROUGH plant condition, and neither anchoring document does (USU: "severity of the disease is higher in fields with heavy, poorly drained soils", no mechanism). | "Use raised or well-drained beds where soil sits wet; the disease runs harder in ground that stays wet, and drainage does nothing for a plant whose roots are already pink." |
| 29b | pink-root | improve_drainage | beginner | SYNTHESIS (low) | "Weak, stressed roots are the ones this fungus takes, and a raised or well-drained bed keeps them out of standing water." | Same join in the beginner register. | "This fungus is worse where the soil stays wet, and it goes for weak, stressed roots, so a raised or well-drained bed takes away one of the things it needs." |
| 28 | pink-root | crop_rotation | beginner | STYLE (very low) | "Leeks usually get off lighter than onions anyway." | "Anyway" is a flippant closer. The claim itself is the record's (`cause_beginner`: "leeks usually get off lighter"); see the document note below on whether the record's claim is sourced. | "Leeks usually get off lighter than onions do." |
| 26/27 | white-rot | certified_clean_stock, garden_sanitation | both | STYLE (low) | Both rungs carry "no cure", "over 20 years", "germinate in response to allium roots" and "rotation alone will not control it". | A two-rung ladder from a short record; the overlap is expected, but each fact is stated four times across the two rungs. | Leave "germinate in response to allium roots" and the sclerotia threshold to clean_stock; leave "rotation alone will not control it" to sanitation. |
| several | cross-rung references | | | STYLE (pattern, low) | thrips beneficial_predators B "try the hose and the cleanup first"; leek-moth planting_time S "still have to be met with the cover"; ALM garden_sanitation S "It is the fall half of the practice, and rotation is the spring half."; rust water_at_the_base S "which is where spacing and rotation take over"; pink-root improve_drainage B/S "It works alongside the long break ... not instead of it." / "Pair it with the long rotation; neither replaces the other." | These describe the ladder, not the world (memory: a note claiming which rungs exist goes false when a rung changes). They read naturally and most mirror record sentences ("rotation alone will not"), so I would not block on them; listed so the pattern is visible. Worst instance is 25b above. | leave, except 25b |

Author's four raised doubts, adjudicated:
1. **weed_host_control carrying a siting claim**: keep (2c above).
2. **handpick for larvae and cocoons**: keep. Cornell doc_764 lists "removal of larvae from the plant,
   destroying pupae or larvae" among recommended cultural controls and gives the finding method the rung
   uses ("unfold or split open damaged leaves and look for larvae or frass"). The catalog's handpick
   reaches `insect_chewing`/`insect_general` and its best_use is "on a regular scouting routine".
3. **pheromone trap inside the spinosad rung**: keep. The record ties the spray to the trap ("7 to 10 days
   after a peak flight" / "A pheromone trap set by mid-April shows when each flight peaks"), and doc_764
   says the same ("Insecticide applications made 7-10 days following a peak flight ... determined through
   the use of the pheromone trap system"). Fix the beginner wording (11a).
4. **white rot with no rotation rung**: correct against the RECORD, which carries only the negative. Note
   for the record, not the rung: the anchoring UC IPM page DOES carry a positive instruction the record
   dropped: "In addition, follow a long-term rotation schedule, and do not follow Allium crops with other
   Allium crops. Rotation alone will not control white rot because sclerotia can survive in soil for more
   than two decades. However, rotation does help prevent an increase in the soilborne inoculum of the
   pathogen." If a rotation rung is wanted, that sentence goes into the record first.

## 3. Document truth: what the anchoring documents actually say (record-level notes, not rung defects)

These are places where a rung faithfully follows the record but the record's claim is wider, narrower or
differently scoped than its anchoring document. None is the author's defect; all are for the orchestrator.

- **Pink root, "leek is a lesser host" (carried in rungs 28 B "Leeks usually get off lighter than onions
  anyway." and 28 S "Leek is a lesser host than onion, so the pressure this has to hold is lower here to
  begin with."): UNSUPPORTED by all three anchoring documents.** UC IPM: "Pink root is primarily a problem
  on onion. It can infect garlic, but rarely causes economically significant damage." (leek is not
  mentioned). USU: "Phoma terrestris is primarily an onion pathogen but can occasionally cause disease on
  other plants such as cereals, corn, cucurbits, pepper, spinach or soybean." (leek not mentioned).
  UF/IFAS HS1388: "Leek is also susceptible to pink root rot but dipping transplant roots in a 2% solution
  of fresh garlic (Allium sativum) extract has been shown to be effective in treating this disease." "Mainly
  an onion disease" is sourced; "leek is a lesser host" is an inference from silence.
- **Leek rust, "comparatively resistant" (four rungs)**: California-scoped. UC IPM: "Leek, elephant garlic,
  and shallot are more resistant." PNW, same page as the cultural controls: "California isolates did not
  infect leek, shallot or elephant garlic. **However, P. allii in Europe is extremely damaging on leek.**"
  The record's framing is UC IPM's; the PNW caveat is the reason to state it once, not four times.
- **White rot threshold**: the record says "even a few sclerotia per soil sample". UC IPM's actual figure:
  "As few as one sclerotium per 10 kilograms of soil can initiate disease. Only one sclerotium per kilogram
  of soil can cause measurable yield loss, and 10 to 20 sclerotia per kilogram cause essentially all plants
  to become infected." So the brief's "one sclerotium per about 20 pounds" (10 kg = 22 lb) was
  document-true and record-false; the author was right not to put it in a rung, and the record is the place
  to fix if the figure is wanted.
- **Leek moth, Cornell doc_764**: the guide supports before-emergence timing ("It is important to have the
  row cover in place over the crop before the moths emerge ... Moths may emerge extremely early during warm
  spells in March"), planting-day timing ("the row cover needs to be installed on the day of planting before
  sunset"), rotation, delayed planting, larval removal, trap timing, DiPel. It does NOT say "sealed at the
  edges", "left in place rather than lifted between flights", the trap precondition, or "clear allium debris
  at the end of the season" (it says only that the moth "overwinters as an adult ... in protected areas such
  as plant debris, hedges and row covers"). Those four are record + catalog claims. UNH 2025 is a one-paragraph
  county-detection notice; it adds only "three generations", "active starting in very early spring (once the
  soil temperatures hit 50°F) in cycles through mid-late August", and "row covers, and other methods of
  exclusion can be effective".
- **Onion thrips overwintering "in allium material left on the surface"**: UMass says "They spend the winter
  as adults in crop remnants, alfalfa, wheat, greenhouses and weeds along the border of crop fields."; UMD
  says "Overwintering occurs in protected places like within soil, plant foliage, plant debris". "On the
  surface" is the record's.
- **Allium leafminer distance**: the two anchoring documents disagree on flight range. Cornell: "ALM does not
  seem to be a long-distance flier." UMass: "ALM adults are strong fliers and can move relatively long
  distances across fields, so rotating further away is better." Both support the rung's instruction ("as far
  from last year's onion-family beds as your garden allows"); neither rung states a range, which is right.
- **Onion maggot cover duration**: UMN, verbatim: "Make sure to set up the barrier in your garden by the time
  adult flies are laying eggs, usually early to mid-May. Keep the barrier in place until the end of the month
  when the flies are finished laying eggs." UMN is also the document that carries the trap precondition
  explicitly: "Do not place row covers if onions or other root vegetables were planted in the same area the
  previous year ... Placing a row cover will trap adults that hatch from the pupae".

## 4. URL table (all 18 anchoring URLs)

| problem | key | url | status | how read |
|---|---|---|---|---|
| onion thrips | osu_ext | https://pnwhandbooks.org/insect/vegetable/vegetable-pests/hosts-pests/leek-shallot-thrips | 200 | r.jina.ai returned 403; fetched raw with a browser User-Agent via urllib, HTML stripped to text, read in full (12 KB) |
| onion thrips | umass_ext | https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/onion-thrips | 200 | urllib raw, HTML to text, read in full (3.6 KB) |
| onion thrips | uc_ipm | https://ipm.ucanr.edu/home-and-landscape/thrips/ | 200 | urllib raw, HTML to text (33 KB); management paragraphs read in full, the rest keyword-scanned |
| onion thrips | umd_ext | https://extension.umd.edu/resource/thrips-home-gardens | 200 | urllib raw, HTML to text, read in full (18.6 KB) |
| leek moth | cornell_ext | https://rvpadmin.cce.cornell.edu/uploads/doc_764.pdf | 200 (4.5 MB PDF) | urllib download, pypdf 6.14.2, 28 pages, 12.8 K chars, read in full |
| leek moth | unh_ext | https://extension.unh.edu/blog/2025/07/leek-moth-nh | 200 | urllib raw, HTML to text, read in full (one paragraph of content) |
| onion maggot | usu_ext | https://extension.usu.edu/yardandgarden/research/leeks-in-the-garden | 200 | urllib raw, HTML to text, read in full (7.5 KB) |
| onion maggot | umn_ext | https://extension.umn.edu/yard-and-garden-insects/root-maggots | 200 | urllib raw, HTML to text, read in full (8.1 KB) |
| onion maggot | uc_ipm | https://ipm.ucanr.edu/agriculture/onion-and-garlic/maggots/ | 200 | urllib raw, HTML to text, read in full (9.7 KB) |
| allium leafminer | umd_ext | https://extension.umd.edu/resource/allium-onion-leafminer | 200 | urllib raw, HTML to text, read in full (4.4 KB) |
| allium leafminer | cornell_ext | https://cals.cornell.edu/integrated-pest-management/outreach-education/fact-sheets/allium-leafminer | 200 | urllib raw, HTML to text, read in full (15.8 KB) |
| allium leafminer | umass_ext | https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/allium-leafminer | 200 | urllib raw, HTML to text, read in full (7.3 KB) |
| leek rust | uc_ipm | https://ipm.ucanr.edu/agriculture/onion-and-garlic/rust/ | 200 | urllib raw, HTML to text, read in full (5.8 KB) |
| leek rust | osu_ext | https://pnwhandbooks.org/plantdisease/host-disease/garlic-allium-sativum-rust | 200 | r.jina.ai 403; raw with browser UA via urllib, read in full (5 KB); WebFetch via r.jina.ai also returned matching quotes as a cross-check |
| white rot | uc_ipm | https://ipm.ucanr.edu/agriculture/onion-and-garlic/white-rot/ | 200 | urllib raw, HTML to text, read in full (8.2 KB) |
| pink root | uc_ipm | https://ipm.ucanr.edu/agriculture/onion-and-garlic/pink-root/ | 200 | urllib raw, HTML to text, read in full (6 KB) |
| pink root | usu_ext | https://extension.usu.edu/planthealth/research/pink-root-onion | 200 | urllib raw, HTML to text, read in full (7.8 KB) |
| pink root | uf_ifas | https://ask.ifas.ufl.edu/publication/HS1388 | 200 | urllib raw, HTML to text (22.8 KB); every paragraph mentioning pink root, rotation, drainage, stress, host or leek read; it is a leek production guide with one pink-root sentence |

No document was UNREAD. Raw copies are in the session scratchpad (`scratchpad/src/*.txt`, `*.pdf`).
