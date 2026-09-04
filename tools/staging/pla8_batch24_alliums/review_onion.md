# onion -- independent source-truth review of the PLA-8 batch 24 ladders (r4)

Reviewed 2026-09-03 against `out_onion.json` (17 rungs, 34 notes), `onion_source.json` (the
corrected record), `control_methods.json`, `shipped_precedents.json`, and the nine anchoring
documents the record names. Read-only; nothing in the repo was edited except this file.

Method. (1) Every note sentence was mapped to the record field or catalog sentence that supports
it (section 3). (2) All nine anchoring URLs were fetched and read through WebFetch with
verbatim-quote prompts (a raw `curl` was refused by the sandbox, so the reader is WebFetch's
extraction model; two documents were re-read through `r.jina.ai` and one was read a third time as a
per-word search). (3) The byte-identity of the water_spray rung was asserted programmatically.
(4) Style was scanned programmatically (dashes, absolutes, British spellings, spaced degrees,
ladder vocabulary, Latin names in the beginner register, sentence counts, difflib similarity of
the two registers in both orders).

## 1. Verdict per rung

| problem | method | verdict | one-line reason |
|---|---|---|---|
| onion-thrips | garden_sanitation | PASS | provenance clean; two low-severity wording notes (#4, #5) |
| onion-thrips | weed_host_control | **FIX** | seasoned register asserts that unrelated weeds do not matter; the record does not say it and the record's own anchors say the opposite (#1, #2) |
| onion-thrips | balance_nitrogen | PASS | vigor framed as tolerance, not fewer thrips; no rotation claim |
| onion-thrips | water_spray | PASS | byte-identical to spring-onion's shipped water_spray rung in both registers (verified `==` on both strings) |
| onion-thrips | beneficial_predators | PASS | one low-severity join and an "only" that overstates the record (#6); keep |
| onion-maggot | crop_rotation | PASS | pupae in the SOIL, not residue; distance and cull pile both from the record |
| onion-maggot | planting_time_avoidance | PASS | fit accepted (see section 5); the cool-wet/mid-spring sentence is the record's own fusion (section 4) |
| onion-maggot | garden_sanitation | PASS | culls, volunteers, spring manure and green manure all from the record |
| onion-maggot | floating_row_cover | PASS | cover on at planting BEFORE the flight in both registers; trap precondition in BOTH registers; overwintering as pupae in soil; no "at emergence" |
| botrytis-neck-rot | balance_nitrogen | PASS | both aggravators from the record; note the anchor gap in section 4 |
| botrytis-neck-rot | cure_and_store | **FIX** | seasoned register describes the ladder's structure ("half of the control") and carries an author-facing catalog caution ("do not borrow another crop's figures") with no figures in the note (#8, #9) |
| fusarium-basal-rot | resistant_varieties | **FIX** (low) | "not offered for every onion type" is a specificity the record does not carry (#11, #12) |
| fusarium-basal-rot | crop_rotation | PASS | several years, soilborne, warm soil, maggot opening: all record |
| fusarium-basal-rot | cure_and_store | PASS | handling is inside the method's own catalog text; wound/maggot entry from the record |
| pink-root | resistant_varieties | **FIX** | seasoned register joins direct root penetration to "why resistance leads the list", a causal claim the record does not make, plus a ladder-position phrase (#13, #14) |
| pink-root | crop_rotation | PASS | three to six years, reduces-not-clears, persists for years, 75 to 85°F: all record |
| pink-root | improve_drainage | **FIX** | both registers make waterlogging THE stress that pink root hits hardest; the record states drainage and stress as two separate facts and the USU anchor lists drought, cold and nutrient stress, not waterlogging (#15, #16) |

Totals: 12 PASS, 5 FIX (one of them low). No em/en dashes, no absolutes from the banned list, no
British spellings, no spaced °F, no `rung|ladder|tier`, no Latin names in any beginner note, no
false-attribution device outside the declared byte-identical copy, every note 2 to 4 sentences and
59 to 88 words, register similarity 0.01 to 0.10 (both difflib orders). No thrips rung mentions
rotation. No pink-root rung mentions clean stock, transplants, or certification.

## 2. Findings table

| # | problem | method | register | severity | offending sentence (verbatim) | why | proposed replacement |
|---|---|---|---|---|---|---|---|
| 1 | onion-thrips | weed_host_control | seasoned | **WRONG** | "The relationship is host-specific, so clearing unrelated weeds around the bed is not the move this one describes." | The record carries no claim about unrelated weeds either way. Its anchors say weeds DO host onion thrips: UMass, "They spend the winter as adults in crop remnants, alfalfa, wheat, greenhouses and weeds along the border of crop fields"; UMD, "Remove weeds from garden areas so they do not harbor thrips or viruses that thrips can transmit"; UC IPM, "control nearby weeds that are alternate hosts of pest thrips". The sentence is derivable only from the catalog's GENERIC caution ("host-specific rather than general tidiness"), which is false for this polyphagous pest. "this one describes" also refers the reader to the catalog entry, a meta device. | "The relationship is host-specific: those three crops are the neighbors that shed thrips into onions in numbers, so distance from them does more than general tidiness around the bed." |
| 2 | onion-thrips | weed_host_control | seasoned | **WRONG** (same family as #1) | "Site the bed away from those crops rather than relying on general weed control, and keep the bed edges clear of the same plants." | "rather than relying on general weed control" tells the reader weed control is the wrong lever; two of the four anchors recommend it (UMD, UC IPM quoted above). The record says only to keep the bed away from grain, alfalfa and clover. | "Site the bed away from those crops, and keep the bed edges clear of the same plants through the season." |
| 3 | onion-thrips | weed_host_control | beginner | (none) | -- | Beginner register is clean: "Grain, alfalfa and clover all carry thrips, and when a patch of them dries out or is cut, the thrips leave it and move into the nearest onions." maps to management_seasoned "keep the bed away from small grains, alfalfa or clover, which shed thrips into onions when they dry down or are cut". | keep |
| 4 | onion-thrips | garden_sanitation | beginner | STYLE (low) | "Once the bulbs are up, do not leave the bed as it stands." | "up" reads as "sprouted" as readily as "lifted"; a beginner could take this as a mid-season instruction. | "Once the bulbs are out of the ground, do not leave the bed as it stands." |
| 5 | onion-thrips | garden_sanitation | beginner | UNSUPPORTED (low) | "Thrips ride out the winter in onion material lying on the soil, so a bed cleaned at the end of the season carries far fewer of them into next spring." | "far fewer" quantifies a reduction the record states only qualitatively ("thrips overwinter in onion material left on the surface"). USU says the material "can harbor thrips during the winter", no magnitude. | "Thrips ride out the winter in onion material lying on the soil, so a bed cleaned at the end of the season gives them less to start from next spring." |
| 6 | onion-thrips | beneficial_predators | seasoned | SYNTHESIS (low) | "Minute pirate bugs and lacewings help hold Thrips tabaci down, and they do it only where broad-spectrum sprays are avoided, so the conservation choice comes first: a general insecticide removes the predators along with the pest and leaves the thrips to rebuild in the leaf axils where the spray missed them anyway." | Joins cause_seasoned ("sheltering in the leaf axils where sprays miss them") to the broad-spectrum caution into a single causal chain (spray kills predators, thrips rebuild in the axils). Both halves are in the record; the chain is the author's. "only" hardens the record's "help where broad-spectrum sprays are avoided". Keep if the orchestrator accepts the join; the softened form removes both. | "Minute pirate bugs and lacewings help hold Thrips tabaci down where broad-spectrum sprays are avoided, so the conservation choice comes first: a general insecticide removes the predators along with the pest, while the thrips sheltering in the leaf axils are the ones a spray misses anyway." |
| 7 | onion-maggot | planting_time_avoidance | both | (record-level, not a rung defect) | beginner: "The flies show up with the cool, wet weather of mid-spring and lay their eggs at the base of young plants, so onions that go in after that wave take less damage." seasoned: "...since the first Delia antiqua flight arrives with the cool, wet weather of mid-spring and lays at the base of seedlings and sets." | Faithful to cause_seasoned ("the first flight arrives with the cool, wet weather of mid-spring"). At document level the two anchors hold the parts separately: UMN, "Make sure to set up the barrier in your garden by the time adult flies are laying eggs, usually early to mid-May" and "Root maggots can occur in any year but are more common during cool, wet springs"; UC IPM, maggots "thrive in cool, moist soils heavy in organic matter" and onion maggots are "restricted to cooler coastal climates". The fusion (flight ARRIVES WITH the cool wet weather) is the record's, inherited here. | keep; flag to the record owner, not the rung author |
| 8 | botrytis-neck-rot | cure_and_store | seasoned | STYLE | "This is the harvest-and-after half of the control." | Describes the ladder (this rung plus balance_nitrogen = two halves), not the world; goes false the day a third rung is added. Same defect class as the rung-note rule already on file. | "The control continues at harvest and after it." |
| 9 | botrytis-neck-rot | cure_and_store | seasoned | STYLE / FIT | "Cure thoroughly, then store cool and dry; the curing and storage conditions belong to onions specifically and differ between crops, so do not borrow another crop's figures." | The second clause is the catalog's author-facing caution ("take the figures from the crop's own guidance rather than from another crop's") rendered as consumer copy. The note gives no figures, so the reader is told not to borrow figures they were never shown. | "Cure thoroughly, warm and dry, then store cool and dry; onions cure and keep under different conditions from potatoes or sweet potatoes, so what suits those crops does not carry over." (catalog: "alliums cure warm and dry then store just above freezing"; record: "cure thoroughly, and store cool and dry") |
| 10 | botrytis-neck-rot | cure_and_store | seasoned | SYNTHESIS (accepted) | "Let the tops mature naturally rather than knocking them down to force bulbing, since Botrytis enters through immature or insufficiently cured necks and a top bent green leaves exactly that." | Author flagged (findings C7). Joins cause_seasoned "bent-over green tops worsen it" with "infection of immature or insufficiently cured necks". A green top bent over IS an immature neck; the join adds no new fact. | keep |
| 11 | fusarium-basal-rot | resistant_varieties | beginner | UNSUPPORTED | "Resistance is not offered for every onion type, so if you cannot find it, go ahead with the other steps rather than waiting on it." | The record says "Choose resistant varieties where available" / "Pick resistant varieties if you can". "onion type" asserts that availability tracks onion TYPE (a reader will hear red vs yellow, long-day vs short-day), which neither the record nor the anchor ("Resistant varieties are available for Fusarium basal rot") says. "the other steps" refers to the ladder. | "Resistance is not offered in every variety, so if you cannot find it, go ahead with rotation and gentle handling rather than waiting on it." |
| 12 | fusarium-basal-rot | resistant_varieties | seasoned | UNSUPPORTED | "Availability, not value, is the qualifier: resistance is not offered across every onion type, so take it where a catalog offers it and keep the rotation and the gentle handling in place whether or not one does." | Same as #11. | "Availability, not value, is the qualifier: resistance is not offered in every variety, so take it where a catalog offers it and keep the rotation and the gentle handling in place whether or not one does." |
| 13 | pink-root | resistant_varieties | seasoned | SYNTHESIS + STYLE | "The fungus penetrates roots directly without a wound and builds with every onion crop on the same ground, which is why resistance, acting in the root itself, leads the list." | The record states "penetrates onion roots directly without a wound" and "Resistant varieties are the best control" as separate facts; "which is why" makes the first the reason for the second, a causal claim no record field or anchor makes (USU: "The best management option is the use of resistant varieties", with no mechanism given). "leads the list" is a ladder-position phrase. | "The fungus penetrates roots directly, without a wound, and builds with every onion crop on the same ground." (the preceding sentence already carries "best control ... ahead of rotation") |
| 14 | pink-root | resistant_varieties | beginner | STYLE (low) | "This is the step that does the most, so start here." | "start here" is a ladder-position instruction; the world-claim is that resistant varieties are the best control. | "A resistant variety does the most against pink root, so choose one before anything else." |
| 15 | pink-root | improve_drainage | beginner | SYNTHESIS | "This fungus does worse damage in heavy, poorly drained soil, and a plant sitting in waterlogged ground is a stressed plant, which is exactly the kind pink root hits hardest." | Author flagged (findings C8). The record has two separate facts, "heavy, poorly drained soil makes it worse" and "weak or stressed plants are the most susceptible"; the rung fuses them by naming waterlogging as the stress. The USU anchor names the stresses: "Plant stresses such as drought, cold, nutrient deficiencies/toxicities, insects and other diseases can increase disease severity", and states the drainage effect separately: "The severity of the disease is higher in fields with heavy, poorly drained soils." Waterlogging-as-stress is the author's bridge. | "This fungus does worse damage in heavy, poorly drained soil, and it hits weak, stressed plants hardest, so a bed that drains well takes away one of the conditions it does best in." |
| 16 | pink-root | improve_drainage | seasoned | SYNTHESIS | "Heavy, poorly drained soil makes pink root worse, and weak or stressed plants are the most susceptible, so drainage works on both halves of that at once: a waterlogged root zone stresses the plant and favors the fungus." | Same as #15; "works on both halves of that at once" is the fused claim stated outright. | "Heavy, poorly drained soil makes pink root worse, and weak or stressed plants are the most susceptible; drainage settles the first of those directly, and it is settled before planting." |

Observations that are NOT findings (no rule broken; listed so the orchestrator can decide):

- Verbatim self-echo of the crop's own record prose. Eight notes carry a 40 to 67 character run
  lifted byte-for-byte from `onion_source.json` management/cause/identification text, e.g.
  thrips/balance_nitrogen seasoned "vigor buys tolerance of the feeding rather than fewer thrips"
  (61 chars, management_seasoned), maggot/planting_time_avoidance seasoned "delaying planting until
  the first flight has passed reduces damage" (67), maggot/floating_row_cover seasoned "the pupae
  overwinter in the soil around last season's onions" (63), pink-root/crop_rotation seasoned
  "common where alliums are grown repeatedly and in warm soils" (60), pink-root/improve_drainage
  seasoned "weak or stressed plants are the most susceptible" (51), fusarium/cure_and_store beginner
  "from the bottom in the field and in storage" (46), pink-root/resistant_varieties both registers
  (43 each), thrips/beneficial_predators seasoned "where broad-spectrum sprays are avoided" (40).
  The promote's echo guard scans OTHER crops' rung prose, not the crop's own record, so these pass;
  if the record fields and the rung render on the same page the reader sees the phrase twice.
- onion-maggot/floating_row_cover beginner uses "sets" without a gloss ("Cover the seedlings or
  sets"). The record's beginner register uses "young plants". Low.
- onion-maggot/garden_sanitation seasoned opens with a fragment, "Two reservoirs and one
  attractant." Not a listed rule; noting it.
- onion-maggot/crop_rotation seasoned, "Rotation is the decision the cover and the cleanup both
  rest on", refers to sibling rungs. It is true in the world (the record makes the cover conditional
  on rotated ground), so it does not fail the notes-describe-the-world rule. Keep.

## 3. Claim provenance, every rung, every sentence

Abbreviations: id_s / id_b = identification_seasoned / _beginner; cause_s / cause_b; mgmt_s /
mgmt_b = management_seasoned / _beginner; cm.<method>.<field> = `control_methods.json`.

### onion-thrips / garden_sanitation
- B "Once the bulbs are up, do not leave the bed as it stands." -> mgmt_b "At the end of the season pull any onions left in the bed and clear the debris" (framing; wording note #4).
- B "Pull any onion plants still in the ground, including the stray ones that sprouted on their own, and rake up the loose tops and skins." -> mgmt_s "Clear volunteer onions and crop debris at the end of the season".
- B "Thrips ride out the winter in onion material lying on the soil, so a bed cleaned at the end of the season carries far fewer of them into next spring." -> mgmt_s "thrips overwinter in onion material left on the surface" ("far fewer": #5).
- S "Thrips tabaci overwinters in onion material left on the soil surface, and volunteer onions carry it through as well, so the end-of-season cleanup is where the carryover is cut." -> mgmt_s (above) + cause_s "Onion thrips (Thrips tabaci)".
- S "Take out every onion still standing, volunteers included, and get the debris off the bed rather than leaving it on the surface where the insects sit." -> mgmt_s / mgmt_b.
- S "It is a fall task with a spring payoff: the population that builds through the first warm, dry spell starts from whatever was left behind." -> cause_s "build through warm, dry spells" + the overwintering claim. Light join; accepted.

### onion-thrips / weed_host_control
- B "Look at what grows next to the onion bed, not just what is in it." -> framing of mgmt_s "keep the bed away from small grains, alfalfa or clover".
- B "Grain, alfalfa and clover all carry thrips, and when a patch of them dries out or is cut, the thrips leave it and move into the nearest onions." -> mgmt_s "which shed thrips into onions when they dry down or are cut".
- B "So do not plant onions right beside a patch like that, and keep the edges of the bed clear of the same plants through the season." -> mgmt_b "do not put onions right beside a grain, alfalfa or clover patch"; cm.weed_host_control.best_use "kept clear at the edges".
- S "The hosts that matter here are specific: small grains, alfalfa and clover carry onion thrips and shed them into an adjacent onion planting when they dry down or are cut." -> mgmt_s.
- S "Site the bed away from those crops rather than relying on general weed control, and keep the bed edges clear of the same plants." -> mgmt_s + cm best_use; the "rather than relying on general weed control" clause: **WRONG** (#2).
- S "The relationship is host-specific, so clearing unrelated weeds around the bed is not the move this one describes." -> cm.weed_host_control.cautions "host-specific rather than general tidiness" (generic); not in the record; contradicted by the anchors for this pest: **WRONG** (#1).

### onion-thrips / balance_nitrogen
- B "Feed the onions enough and no more." -> mgmt_s "Hold nitrogen to adequate rather than heavy".
- B "Nitrogen is the part of fertilizer that pushes leafy growth, and piling it on makes thrips worse rather than better." -> mgmt_b "Go easy on nitrogen, which makes thrips worse"; cm.balance_nitrogen.how_it_works_beginner "high-nitrogen fertilizer ... soft, sappy new growth".
- B "Do not try to outgrow the pest with extra feeding either: a strong, well-watered plant puts up with the feeding better, but it does not end up with fewer thrips on it." -> mgmt_s "keep plants well watered: vigor buys tolerance of the feeding rather than fewer thrips"; mgmt_b "keep the plants well watered so they can shrug off the feeding".
- S "Hold nitrogen at adequate rather than heavy, since excess promotes Thrips tabaci." -> mgmt_s "Hold nitrogen to adequate rather than heavy, since excess promotes thrips".
- S "The distinction worth keeping in mind is that vigor buys tolerance of the feeding rather than fewer thrips, so the aim is a plant strong enough to size its bulb through the rasping, not a heavier feeding program." -> mgmt_s (verbatim phrase) + id_s "rasping ... heavy feeding reduces bulb size".
- S "Restraint here is a preventive habit, settled when the feeding is planned rather than once the silvering shows." -> cm.balance_nitrogen.best_use "A preventive feeding habit"; id_s "silvery streaks".

### onion-thrips / water_spray
- Declared byte-identical copy of spring-onion's shipped water_spray rung. Verified: `shipped['note_beginner'] == mine['note_beginner']` True; `shipped['note_seasoned'] == mine['note_seasoned']` True. "a material named here" is inside the copy and exempt by design. Not re-adjudicated.

### onion-thrips / beneficial_predators
- B "Not every small insect on the onions is a problem." -> framing.
- B "Minute pirate bugs and lacewings both hunt thrips, and they will do some of the work for you as long as you let them." -> mgmt_s "minute pirate bugs and lacewings help where broad-spectrum sprays are avoided".
- B "That means holding off on any spray that kills insects in general, since it takes out the helpers along with the thrips and leaves nothing in the bed to check the next wave." -> mgmt_s (above); cm.beneficial_predators.cautions "Avoid broad-spectrum insecticides, which kill the beneficials as well as the pests".
- S first sentence -> mgmt_s + cause_s "sheltering in the leaf axils where sprays miss them" (join, #6).
- S "Lean on the predators through a light infestation, and treat a persistent outbreak per local extension guidance rather than reaching for a broad material." -> mgmt_s "Treat persistent outbreaks per local extension guidance"; cm.beneficial_predators.best_use "lean on it before reaching for any spray".

### onion-maggot / crop_rotation
- B "Put this year's onions on ground that grew no onions or onion relatives last year." -> mgmt_b "Do not plant onions where onions or their relatives grew last year".
- B "The fly spends the winter as a pupa, its resting stage, in the soil around last year's onions, and it comes up in spring right where those plants stood." -> cause_s "the pupae overwinter in the soil around last season's onions"; cause_b "It spends the winter in the soil where onions grew the year before". Pupae in SOIL, not residue: correct.
- B "Choose the new bed well away from that spot, and away from any heap of discarded onions, since the fly keeps going on those between crops." -> mgmt_s "site new plantings away from it and from any cull pile"; cause_s "cull piles and volunteer onions keep the fly going between crops".
- S "Delia antiqua pupates in the soil around last season's onions, so a bed that carried alliums is the emergence site for the spring flight and the new planting belongs off it." -> cause_s + mgmt_s "Rotate off ground that carried alliums last season".
- S "Distance matters as well as sequence: site the crop away from last year's allium ground and from any cull pile, because culls and volunteer onions carry the fly between crops." -> mgmt_s + cause_s.
- S "Rotation is the decision the cover and the cleanup both rest on, and it is settled before anything is planted." -> mgmt_s (row cover "on ground that did not carry alliums last year"). Cross-rung framing, true in the world; accepted.

### onion-maggot / planting_time_avoidance
- B "If your growing season is long enough, wait to plant until the first wave of flies has come and gone." -> mgmt_s "Delaying planting until the first flight has passed reduces damage where the season allows."
- B "The flies show up with the cool, wet weather of mid-spring and lay their eggs at the base of young plants, so onions that go in after that wave take less damage." -> cause_s "lays at the base of the plant ... the first flight arrives with the cool, wet weather of mid-spring" (#7, record-level).
- B "Ask your local extension office when the flight usually runs where you live, since the timing shifts from place to place, and do not delay so long that the onions run out of season." -> cm.planting_time_avoidance.cautions "Emergence dates shift with the region and the season ... confirm it locally"; cm cons "A shifted sowing date trades against the harvest window"; mgmt_s "where the season allows".
- S "Where the season allows it, delaying planting until the first flight has passed reduces damage, since the first Delia antiqua flight arrives with the cool, wet weather of mid-spring and lays at the base of seedlings and sets." -> mgmt_s + cause_s; "seedlings and sets" from mgmt_s "cover seedlings or sets".
- S "The trade is against the season the crop has left, so this move in time suits a long season and costs a short one." -> cm cons (above); cm best_use "this one moves it in time".
- S "Emergence dates shift with region and year, so confirm the local flight period rather than carrying a calendar date across regions." -> cm cautions (above).

### onion-maggot / garden_sanitation
- B "Get rid of the onions you rejected at harvest, the undersized or damaged ones, and pull any onion plants that come up on their own, because the fly breeds on both between crops." -> mgmt_s "remove culls and volunteer onions"; cause_s "cull piles and volunteer onions keep the fly going between crops" ("breeds on" renders "keep the fly going"; accepted).
- B "Take that material out of the garden rather than leaving it in a heap by the bed." -> mgmt_s "away from ... any cull pile"; cm.garden_sanitation.cautions "Destroy diseased debris rather than leaving or burying it".
- B "In spring, keep fresh manure and freshly turned-in green cover crops out of the onion bed too: the fly is drawn to lay its eggs where something is rotting in the soil." -> mgmt_s "keep spring manure and green manure out of the bed"; cause_s "Rotting organic matter and spring manure draw egg-laying". "green manure" glossed in-line for the beginner: good.
- S "Two reservoirs and one attractant." -> framing.
- S "Culls and volunteer onions carry Delia antiqua between crops, so remove both and take them out of the garden rather than starting a cull pile, which is exactly what keeps the fly going." -> cause_s + mgmt_s.
- S "Rotting organic matter draws egg-laying, so spring manure and green manure stay out of the bed in the weeks when the first flight is looking for a place to lay." -> cause_s + mgmt_s.

### onion-maggot / floating_row_cover
- B "Cover the seedlings or sets with row-cover fabric on planting day, before the spring flight begins, and weight or bury the edges so nothing crawls under." -> mgmt_s "cover seedlings or sets with row cover sealed at the edges from planting, before the spring flight". TIMING CORRECT.
- B "The fly lays its eggs at the base of the plant, so a sealed cover keeps the eggs off the crop." -> cause_s; mgmt_b "so the fly cannot lay eggs on them".
- B "Do not put the cover over ground that grew onions or their relatives last year: the flies come up out of that soil, and a cover over it seals them in with the crop." -> mgmt_b "Do not cover a bed that grew alliums last year, or you seal the emerging flies in with the crop." TRAP PRECONDITION PRESENT (beginner).
- B "Use it only on rotated ground." -> mgmt_s "on ground that did not carry alliums last year".
- S "Exclusion works here only under two conditions." -> framing.
- S "Timing: the cover goes on from planting, ahead of the spring flight, sealed at the edges, because Delia antiqua lays at the base of the plant and a late or loose cover is no barrier." -> mgmt_s; cm.floating_row_cover.cons "Must be on before the pest arrives and sealed at the edges, or it fails". TIMING CORRECT.
- S "Siting: the pupae overwinter in the soil around last season's onions, so a bed that carried alliums last year seals the emerging flies in with the crop if it is covered." -> cause_s + mgmt_b; cm cautions "Do not lay row cover over a bed where the same-family crop grew last year, or emerging soil pests can be trapped under it with the crop". TRAP PRECONDITION PRESENT (seasoned). Overwintering = pupae in soil.
- S "Reserve the fabric for rotated ground." -> mgmt_s.

### botrytis-neck-rot / balance_nitrogen
- B "Go easy on the fertilizer, especially nitrogen, the part that drives leafy top growth." -> cause_b "Too much fertilizer ... make it worse"; cause_s "excess nitrogen".
- B "Too much of it is one of two things that make neck rot worse, and both are in your hands: the other is bending green tops over to hurry the bulbs along." -> cause_s "excess nitrogen and bent-over green tops worsen it"; mgmt_s "do not knock down green tops to force bulbing".
- B "Feed the onions moderately through the season and let the bulbs mature on their own schedule rather than pushing them." -> mgmt_s "Let tops mature naturally".
- S "Two aggravating factors sit behind neck rot, excess nitrogen and green tops bent over, and both are grower choices rather than weather." -> cause_s.
- S "Excess nitrogen worsens a rot that takes immature or insufficiently cured necks, so restraint in the feeding program is the first of the two to settle, and it is settled through the season because there is nothing to correct at lifting." -> cause_s "Botrytis infection of immature or insufficiently cured necks; excess nitrogen ... worsen it".
- S "The second is settled at harvest by letting the tops mature on their own." -> mgmt_s.

### botrytis-neck-rot / cure_and_store
- B "Leave the tops alone until they fall over by themselves, then lift the onions and dry them thoroughly before they go into storage." -> mgmt_b "Let the tops fall on their own, do not bend them over, dry (cure) the onions well".
- B "Curing, the drying-down of the neck and outer skins, is what keeps this mold out, because it takes hold in necks that were still green or were not dried enough." -> cause_b "A mold that gets into the neck of onions that were harvested too green or not dried properly"; cm.cure_and_store.how_it_works_beginner "dries its outer skin down".
- B "Store the cured bulbs cool and dry, set aside any that are soft, bruised or spotted to use first, and check white onions soonest, since they are the most prone." -> mgmt_b "store them somewhere cool and dry"; cm cautions "Set aside bruised, cut or spotted produce to use first"; id_b "It mostly hits white onions".
- S "This is the harvest-and-after half of the control." -> STYLE (#8).
- S "Let the tops mature naturally rather than knocking them down to force bulbing, since Botrytis enters through immature or insufficiently cured necks and a top bent green leaves exactly that." -> mgmt_s + cause_s (#10, accepted).
- S "Cure thoroughly, then store cool and dry; the curing and storage conditions belong to onions specifically and differ between crops, so do not borrow another crop's figures." -> mgmt_s + cm.cure_and_store.cautions (#9).
- S "White-skinned bulbs are the most susceptible, so they are the first to check in storage." -> id_s "white-skinned and immature or poorly cured bulbs are most susceptible".

### fusarium-basal-rot / resistant_varieties
- B "Start at the seed rack." -> cm.resistant_varieties.best_use "Chosen at seed-buying time".
- B "If a variety is sold as resistant to basal rot, choose it, because this fungus lives in the soil for years and a plant that resists it is the cheapest protection you can buy." -> mgmt_b "Pick resistant varieties if you can"; cause_b "A soil fungus that stays in the ground for years"; cm how_it_works_seasoned "the cheapest and most durable control".
- B "Resistance is not offered for every onion type, so if you cannot find it, go ahead with the other steps rather than waiting on it." -> UNSUPPORTED (#11).
- S "Where a resistant variety is available, choose it; the decision is made at seed-buying time, before anything is in the ground, and it costs nothing in the bed." -> mgmt_s "Choose resistant varieties where available"; cm best_use + pros "no spraying, cost, or labor once chosen".
- S "Availability, not value, is the qualifier: resistance is not offered across every onion type, so take it where a catalog offers it and keep the rotation and the gentle handling in place whether or not one does." -> UNSUPPORTED (#12).

### fusarium-basal-rot / crop_rotation
- B "Keep onions and their relatives out of a bed that has had this rot for several years, not just one." -> mgmt_b "do not grow onions in the same spot for several years".
- B "The fungus lives in the soil itself, so it is still there long after the sick bulbs are gone, and it likes warm ground." -> cause_b "A soil fungus that stays in the ground for years and likes warm soil".
- B "Plan several seasons away before onions or any relative go back in, because a single year off does little against something that lasts that long." -> mgmt_s "rotate out of alliums for several years"; cm.crop_rotation.cons "soil inoculum takes years to decline".
- S "Rotate out of alliums for several years." -> mgmt_s verbatim.
- S "The pathogen is soilborne, persists for years, and is favored by warm soil, so the length of the break is the substance of the step: a single year away leaves the population where it was." -> cause_s "Soilborne Fusarium that persists for years and is favored by warm soil". ("leaves the population where it was" is a hair stronger than "persists for years"; accepted.)
- S "Keep the maggot program running alongside it, since maggot damage is one of the two openings this fungus uses to get into a bulb." -> cause_s "wounds and maggot damage open the door".

### fusarium-basal-rot / cure_and_store
- B "Handle the bulbs gently from lifting through storage: no dropping, no tossing, no nicking them with a fork or knife." -> mgmt_b "handle the bulbs gently so they are not injured"; cm.cure_and_store.how_it_works_seasoned "avoiding bruising and other mechanical injury at harvest".
- B "This fungus gets into a bulb through a wound, or through the damage maggots leave, and it rots the bulb from the bottom in the field and in storage." -> cause_s + id_s "bulbs rot from the bottom in the field and in storage".
- B "Any bulb that is cut or bruised goes to the kitchen first rather than into the storage crate, since one rotting bulb spreads to the ones it touches." -> cm cautions "one rotting item spreads to what it touches".
- S "Gentle handling closes an entry route rather than acting on the fungus: wounds and maggot feeding are what open a bulb to Fusarium, and the rot then runs upward from the basal plate in the field and in storage alike." -> cause_s + id_s "decay ... at the basal plate ... rot from the bottom" ("runs upward" is a mild elaboration; accepted).
- S "Lift and cure without bruising or cutting, and keep any damaged bulb out of storage to use first, because a rotting bulb passes the problem to what it touches." -> cm how_it_works_seasoned + cautions.
- S "This guards bulbs that were sound at lifting and cannot rescue one the fungus reached in the bed." -> cm cons "Does nothing for a crop already infected in the ground; it protects sound produce".

### pink-root / resistant_varieties
- B "This is the step that does the most, so start here." -> mgmt_s "Resistant varieties are the best control" (STYLE #14).
- B "Look for a variety sold as resistant to pink root, and ask your seed supplier which ones hold up in your area, because the fungus comes in different strains and a variety that resists one may not resist another." -> mgmt_b "ask your seed supplier which ones do well in your area"; mgmt_s "resistance varies with the strain".
- B "A resistant variety is chosen once, when you buy seed, and from then on the plant does the defending itself." -> cm.resistant_varieties.how_it_works_beginner "so the plant defends itself"; best_use "Chosen at seed-buying time".
- S "Resistant varieties are the best control for pink root on onion, ahead of rotation, and the choice is local: resistance varies with the strain of Setophoma terrestris, so ask the seed supplier which varieties hold up in your area rather than relying on a catalog description alone." -> mgmt_s "Resistant varieties are the best control ... resistance varies with the strain"; cause_s "Setophoma terrestris"; "ahead of rotation" follows from mgmt_s ordering plus "rotation reduces the disease rather than clearing it". Accepted.
- S "The fungus penetrates roots directly without a wound and builds with every onion crop on the same ground, which is why resistance, acting in the root itself, leads the list." -> cause_s for the two facts; the "which is why" is SYNTHESIS (#13).

### pink-root / crop_rotation
- B "Give onions a bed that has had no onions or any of their relatives in it for three to six years." -> mgmt_s "Rotate off allium ground for three to six years".
- B "The fungus builds up a little more with every onion crop grown on the same ground, and it hangs on in the soil for years, so rotation lowers the amount of it in the bed but does not get rid of it." -> cause_s "builds up with every onion crop on the same ground"; mgmt_s "rotation reduces the disease rather than clearing it, because the fungus persists in soil for years". ROTATION CAVEAT PRESENT.
- B "Treat the break as a way to keep the disease down, and lean on a resistant variety to do the rest." -> mgmt_b "Rotation helps but does not clear the fungus".
- S "Rotate off allium ground for three to six years, and hold the expectation in check: rotation reduces pink root rather than clearing it, because Setophoma terrestris persists in soil for years and builds with every onion crop on the same ground." -> mgmt_s + cause_s. ROTATION CAVEAT PRESENT.
- S "The disease is most common where alliums are grown repeatedly and in warm soils, with the fungus most active at soil temperatures of 75 to 85°F, so a long break lowers the inoculum the next crop meets without resetting it." -> id_s "common where alliums are grown repeatedly and in warm soils"; cause_s "most active at soil temperatures of 75 to 85°F". Figure is in the record; no space before °F.

### pink-root / improve_drainage
- B "If the onion bed is heavy clay or stays wet after rain, fix the drainage before you plant." -> mgmt_s "improve drainage on heavy ground"; mgmt_b "improve drainage where the soil stays wet".
- B "This fungus does worse damage in heavy, poorly drained soil, and a plant sitting in waterlogged ground is a stressed plant, which is exactly the kind pink root hits hardest." -> SYNTHESIS (#15).
- B "A raised bed is the usual fix on heavy ground, and it is standard practice there rather than something to wait on until the roots turn pink." -> cm.improve_drainage.how_it_works_seasoned "Raised beds are the standard fix for vegetables on heavy ground"; best_use "as standard practice on heavy or low-lying ground before planting"; id_b "The roots turn pink".
- S "Heavy, poorly drained soil makes pink root worse, and weak or stressed plants are the most susceptible, so drainage works on both halves of that at once: a waterlogged root zone stresses the plant and favors the fungus." -> SYNTHESIS (#16).
- S "Improve drainage on heavy ground before planting, with a raised bed as the standard fix on vegetables, and treat it as a site decision; the pink-to-red shriveling of the roots is the outcome it is meant to prevent, not the signal to start." -> mgmt_s + cm + id_s "Roots turn pink then red and shrivel".

## 4. Document truth (spot-check of the record's anchors)

Everything below is what the fetched text holds; "NOT FOUND (n reads)" means the phrase or fact
did not appear in n independent WebFetch reads with prompts asking for verbatim quotes on that
exact topic. It is not a claim that the page lacks it in some form the reader could not surface.
No document was unreadable.

### onion-thrips (usu_ext, umass_ext, uc_ipm, umd_ext): SUPPORTED
- Overwinter in onion material on the surface + volunteers: USU "Remove or destroy volunteer onion plants and debris. Onion plant matter left on the soil surface can harbor thrips during the winter to survive and spread the following year."
- Grain / alfalfa / clover: USU "Avoid planting onions adjacent to grain and alfalfa fields. Adult thrips overwinter in these crops and their close proximity can increase thrips migration into onions."; UMass "Avoid planting onions near alfalfa, wheat or clover, as these crops can harbor large populations of thrips. Thrips may migrate to onions when these crops are cut or harvested."; UC IPM "move into gardens and landscapes when plants in weedy areas or grasslands begin to dry in spring or summer. Avoid planting susceptible plants next to these areas, and control nearby weeds that are alternate hosts of pest thrips."
- Nitrogen: UC IPM "avoid excessive applications of nitrogen fertilizer, which may promote higher populations of thrips."; UMD "Avoid over-fertilizing plants, especially with nitrogen."; USU "Fertilize onions with adequate, but not excessive amounts of nitrogen".
- Vigor = tolerance: UC IPM "keep plants vigorous and increase their tolerance to thrips damage"; UMass "Healthy vigorous plants can tolerate moderate populations."; USU "keep onion plants healthy and non-stressed will increase the crop's immunity to thrips feeding injury."
- Water spray: USU "apply a stiff spray of water from a hose to wash thrips from plants"; UMD "knock them off with a strong jet of plain water from a garden hose".
- Predators / broad-spectrum: USU "minute pirate bug (Orius spp.), and green lacewing (Chrysoperla spp.) larvae" and "avoid using broad-spectrum, toxic insecticides to preserve natural enemies"; UC IPM "green lacewings, minute pirate bugs ... avoid persistent pesticides".
- Axils / sprays miss: UMass "feeding occurs in protected, succulent areas ... deep between the leaf blades."; UMD "thrips tucked underneath deformed leaves or wedged into plant crevices can be difficult to treat."
- Rotation: NOT FOUND in all four (the record correctly dropped it; no rung carries it).
- General weeds as hosts (bears on finding #1): UMass "weeds along the border of crop fields"; UMD "Remove weeds from garden areas so they do not harbor thrips"; UC IPM as quoted. The rung's negative is contradicted here.

### onion-maggot (umn_ext root-maggots, uc_ipm maggots): SUPPORTED, one record-level fusion
- Pupae in soil: UMN "Root maggots spend the winter as pupae in the soil."; UC IPM "Mature larvae pupate in the soil." and fields near previous onions "most likely harbor overwintering onion maggot pupae."
- Eggs at the base: UMN "lay about 50-200 small, white eggs at the base of plant stems"; UC IPM "eggs on or near the soil surface near the base of the onion plant."
- Row cover timing + trap: UMN "Make sure to set up the barrier in your garden by the time adult flies are laying eggs, usually early to mid-May." and "Do not place row covers if onions or other root vegetables were planted in the same area the previous year... Placing a row cover will trap adults that hatch from the pupae and it will no longer protect the plants from the flies." The record's "from planting, before the spring flight" is stricter than the anchor and consistent with it.
- Rotation + distance + cull piles + volunteers: UC IPM "Remove and dispose of onion culls and volunteer onions. Avoid planting successive onion crops without rotating to other crops. Avoid planting onions near fields where onions were recently grown, or fields that are located near onion cull piles." and "no less than 3/4 of a mile"; UMN "Practice crop rotation".
- Manure / rotting matter: UMN "Do not use animal manure or green manure in your garden in spring. Rotting and decaying organic matter attracts root maggots"; farm section "Adult flies are attracted to freshly plowed fields and decaying organic matter." (UC IPM attributes the decaying-residue attraction to seedcorn maggot specifically; UMN's is the general root-maggot statement the record rests on.)
- Delayed planting: UMN "When possible, wait until June 1st" and "Planting later into the onion planting window will help them avoid the flight period for the first round of egg-laying onion maggot adults."; UC IPM "Wait to plant until later in the spring, after the first generation of adult flies has emerged."
- "the first flight arrives with the cool, wet weather of mid-spring" (record cause_seasoned, carried into both planting_time_avoidance notes): the anchors hold "usually early to mid-May" and "more common during cool, wet springs" (UMN) and "cool, moist soils" / "cooler coastal climates" (UC IPM) as separate statements. Record-level fusion, inherited by the rung (#7).
- Home-garden insecticide: UMN "There are no insecticides available as a pre-plant treatment for cabbage and onion maggots in the home garden." (not in the record; no rung claims it; consistent with the author's D-list.)

### botrytis-neck-rot (umn_ext growing-onions only, verified 2026-06-16): ANCHOR DOES NOT CARRY MOST OF THE RECORD
Three reads (direct summary; r.jina.ai dump of "Managing pests and diseases"; direct per-word search). Found:
- "Several kinds of rot can infect onions, including Fusarium basal rot, Botrytis neck rot and bacterial soft rot."
- "Onions require a good supply of available nitrogen, but too much nitrogen can result in late maturity, large necks that are difficult to cure, soft bulbs, green flesh and poor storage quality." (supports excess nitrogen -> hard-to-cure necks -> poor storage; the neck-rot link is one inference away)
- "Harvest onions when about half the tops are falling over and dry."; "Curing is essential if you plan to store your onions. Keep the onions in a warm (75°F - 90°F), well-ventilated area for two to four weeks, until outer bulb scales are dry and the neck is tight."; "Poor curing will result in decay during storage."; "Store onions in a cool, dry area."
NOT FOUND (3 reads): bent-over / knocked-down green tops; white-skinned bulbs most susceptible; gray mold; "immature or insufficiently cured necks" as such (closest: "large necks that are difficult to cure").
Rungs resting on the unfound claims: balance_nitrogen (both registers: bent tops as the second aggravator); cure_and_store (both: white onions most prone / most susceptible; seasoned: "a top bent green").

### fusarium-basal-rot (umn_ext growing-onions only, verified 2026-06-16): ANCHOR DOES NOT CARRY MOST OF THE RECORD
Found (3 reads): "Resistant varieties are available for Fusarium basal rot." and the rot list above.
NOT FOUND (3 reads): soilborne and persists for years; favored by warm soil; wounds and maggot damage as the entry; rotate out of alliums for several years; avoid wounding; rots from the bottom / basal plate in field and storage. (Per-word search: no sentence on the page contains "wound", "rotation", "rotate", or "years" in a disease sense.)
Every fusarium rung rests on at least one unfound claim. The rungs are faithful to the record; the record's anchor is thin. This is a record-provenance matter for the orchestrator (the correction pass re-verified thrips, maggot and pink root on 2026-09-03 and left these two at 2026-06-16), not a rung defect. I have not read any candidate replacement anchor and make no claim about what one holds.

### pink-root (uc_ipm pink-root, usu_ext pink-root-onion): SUPPORTED
- Direct penetration: UC IPM "penetrates onion roots directly. Wounds are not necessary for infection"; USU "It can penetrate onion roots directly without the need for wounds".
- Builds with every crop / persists: UC IPM "The more years onions are grown in the field, the more destructive the disease becomes."; USU "Disease incidence goes up with every onion crop" and "can survive for a very long time in soil."
- 75 to 85°F: UC IPM "Optimal temperatures for disease development are 75° to 85°F."; USU "most active at temperatures of 75 – 85F".
- Resistant varieties best, strain caveat, ask supplier: USU "The best management option is the use of resistant varieties. There are resistant onion varieties available but resistance levels can vary from field to field due to genetic variability of the pathogen. Talk to your local seed provider about varieties that may work in your area."; UC IPM "many resistant varieties are resistant in some locations but not in others."
- Rotation reduces, does not clear: UC IPM "Rotating to non-Allium crops for 3 to 6 years can reduce the incidence of pink root."; USU "Even though crop rotation does not have an effect on the disease, planting onion every five years can keep disease incidence low."
- Drainage / stress: USU "The severity of the disease is higher in fields with heavy, poorly drained soils." and "Plant stresses such as drought, cold, nutrient deficiencies/toxicities, insects and other diseases can increase disease severity." and "less vigorous plants are more susceptible"; UC IPM "weak plants are more susceptible". Waterlogging is not named as a stress (bears on #15, #16).
- Clean stock / transplants: NOT FOUND in either (correctly absent from record and rungs).
- Naming: both anchors say "Phoma terrestris"; the record's "Setophoma terrestris, long known as Phoma terrestris" supplies the current name from outside the anchors, and the two seasoned rungs use Setophoma. Not a rung defect (the record carries it); a reader checking the anchors will not find the name.

## 5. Fit judgments

| problem | method | keep / rewrite / drop | reason |
|---|---|---|---|
| onion-thrips | weed_host_control | **REWRITE** (keep the rung) | Closest method for a siting claim: the catalog's seasoned text names thrips explicitly ("For thrips it is the same move, to control nearby weeds that are alternate hosts") and its best_use is "cleared before sowing and kept clear at the edges"; UC IPM, an anchor, pairs siting with weed control in one sentence. Dropping it leaves the grain/alfalfa/clover claim unplaced. Rewrite the two seasoned sentences (#1, #2) so the rung stops dismissing weed control. |
| onion-maggot | planting_time_avoidance | **KEEP** | applies_to `insect_chewing|insect_boring` is reached through the problem type `insect`. The method's meaning (shift the planting so the susceptible window misses a locally published flight) is exactly the record's claim, and both anchors state it for this pest (UMN "Planting later into the onion planting window will help them avoid the flight period"; UC IPM "Wait to plant until later in the spring, after the first generation of adult flies has emerged"). The catalog's "sowing a second, quick crop" form is not claimed. |
| fusarium-basal-rot | cure_and_store | KEEP | The record's practice is "avoid wounding bulbs"; the method's own seasoned text covers handling ("avoiding bruising and other mechanical injury at harvest and inspecting bulbs before storing"). |
| botrytis-neck-rot | cure_and_store | REWRITE (two seasoned sentences) | Right method; the harvest-maturity precondition sits here reasonably (no catalog method covers letting tops mature). Fix #8, #9. |
| botrytis-neck-rot | balance_nitrogen | KEEP | Reaches `fungal`; the rung uses the record's mechanism (nitrogen -> immature necks), not the catalog's canopy mechanism. |
| pink-root | improve_drainage | REWRITE (both registers) | Right method (the record names drainage); the stress bridge is the defect (#15, #16). |
| pink-root | resistant_varieties | REWRITE (one seasoned sentence) | Lead control with the strain caveat: correct. Drop the "which is why" clause (#13). |
| all others | -- | KEEP | -- |

## 6. URL table

| url | status | how read |
|---|---|---|
| https://extension.usu.edu/pests/research/onion-thrips | fetched OK | WebFetch, verbatim-quote prompt on 9 topics (1 read) |
| https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/onion-thrips | fetched OK | WebFetch, verbatim-quote prompt (1 read) |
| https://ipm.ucanr.edu/home-and-landscape/thrips/ | fetched OK | WebFetch, verbatim-quote prompt + headings (1 read) |
| https://extension.umd.edu/resource/thrips-home-gardens | fetched OK | WebFetch; full "Thrips management tactics" section returned verbatim (1 read) |
| https://extension.umn.edu/yard-and-garden-insects/root-maggots | fetched OK | WebFetch, verbatim-quote prompt on 8 topics (1 read) |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/maggots/ | fetched OK | WebFetch direct, then r.jina.ai section dump (2 reads) |
| https://extension.umn.edu/vegetables/growing-onions | fetched OK | WebFetch direct summary; r.jina.ai dump of "Managing pests and diseases"; direct per-word search for 21 words (3 reads; the third surfaced nitrogen/curing sentences the first two omitted) |
| https://ipm.ucanr.edu/agriculture/onion-and-garlic/pink-root/ | fetched OK | WebFetch, verbatim-quote prompt on 7 topics (1 read) |
| https://extension.usu.edu/planthealth/research/pink-root-onion | fetched OK | WebFetch; full Management section returned verbatim (1 read) |

Caveat on "how read": the sandbox refused `curl`, so no raw HTML was inspected; each read is
WebFetch's extraction model answering a prompt that demanded verbatim sentences and an explicit
"NOT FOUND" per topic. Where a claim mattered and the first read was silent, the page was re-read
with a narrower prompt. The orchestrator can confirm the two UMN growing-onions gaps with a raw
fetch in one call.

## 7. The author's own doubts (findings_onion.md), adjudicated

- A1 straw mulch unplaced: agreed; no catalog mulch method reaches `insect` except reflective_mulch, which the corrected record no longer names.
- A2 / A3 vigor-for-tolerance unplaced: agreed; the tolerance framing inside balance_nitrogen is the right home and is correctly framed (tolerance, not fewer thrips).
- A4 let-tops-mature inside cure_and_store: agreed as placement; see #8, #9 for the two sentences around it.
- B5 weed_host_control as a siting rung: keep the rung, rewrite the seasoned negative (#1, #2).
- B6 planting_time_avoidance on a root maggot: keep (section 5).
- C7 "a top bent green leaves exactly that": accepted (#10).
- C8 waterlogging-stress bridge: NOT accepted (#15, #16); the USU anchor names the stresses and waterlogging is not among them.
- C9 "where the season allows" renderings: fine.
- C10 / C11 catalog-sourced "cheapest protection" and "raised bed": fine, both are in the catalog text.
- D (things deliberately not said): confirmed absent from the rungs: no home-garden-insecticide claim, no clean stock, no storage temperature, no 77 to 82°F, no reflective mulch, no thrips rotation.
- E pins: not re-derived here (read-only review); the author's count of 17 rungs / 1 temperature figure matches what I measured (17 rungs; the only `\d+°F` hit is "85°F" in pink-root/crop_rotation note_seasoned).
