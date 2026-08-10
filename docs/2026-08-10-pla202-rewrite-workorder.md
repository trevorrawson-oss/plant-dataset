# PLA-202 rewrite work-order — 25 hits, 22 fields, 15 crops, 15 writing units

Export for the rewrite pass. Each unit is one writing decision; duplicates are grouped
so one rewrite clears every listed hit. Per entry: crop slug + full field path (patch
target), class, the matched run ONLY (no further source text), and our entire current
field value. Registers are the path suffixes (`_seasoned` / `_beginner`); `zone_notes`
and `suitability_note_seasoned` fields are single-value per zone (no register pair
beyond what the suffix says).

**R1 pattern note (11 of 15 units):** all R1s are the same authoring move — "Institution
notes/says/frames + the source's clause verbatim, no quotation marks." The consistent
fix: keep the attribution, restate the CONTENT in our words (the fact, number, or
window is what the citation supports — the sentence must be ours). The R2s (4 units)
are lifted clauses in our own voice; same fix, minus the attribution question.

**Two paraphrase-catch flags** (units 3 and 13): the original author already reworded
these lightly (single-word swaps) and it wasn't enough distance. The true overlap
extends beyond the printed run — treat the WHOLE sentence as owed a fresh structure,
not just the flagged words.

---

## Unit 1 — asparagus, UC IPM "two distinct periods" clause (R1, appears in TWO fields)

One decision, two applications. The same UC IPM clause is near-quoted in both fields
(worded slightly differently each time). Rewrite the idea (asparagus needs an active
season and a real dormant rest to persist) in our own structure in both places.

**1a. `asparagus` :: `description_seasoned`** — run (11w):
"requires two distinct periods a growing period and a resting period"

Current value:
> Asparagus (Asparagus officinalis) is a long-lived herbaceous perennial grown for the tender spring spears it pushes from a deep, cold-hardy crown. Established once from one-year-old crowns in a deep trench, a well-sited bed yields for 15 to 20 years and sometimes far longer. The rhythm is fixed: spears emerge as the soil warms and are cut for a spring window that lengthens with bed age, reaching six to ten weeks on a mature crown, after which every remaining spear grows into a tall fern canopy that recharges the crown for the next season. It is a temperate crop by physiology, not a tropical one; UC IPM notes asparagus requires two distinct periods, a growing period and a resting period, so it needs a real winter dormancy to persist. Variety choice sets the ceiling. All-male hybrids outyield the open-pollinated types and skip the weedy volunteer seedlings: Millennium, a cold-hardy University of Guelph hybrid, is the modern high-yield northern standard but runs more susceptible to rust, while the Rutgers Jersey hybrids, represented here by Jersey Knight, carry the class's vigor-based field tolerance to rust and to Fusarium crown and root rot. Among the open-pollinated types, Mary Washington is the century-old heirloom standard, hardy but lighter-yielding with mixed male and female plants, and Purple Passion is a sweeter, purple-speared strain that yields less and catches foliage disease more easily. Give asparagus full sun and deep, well-drained ground, and choose the site with care, since the crowns will hold it for two decades.

**1b. `asparagus` :: `hardiness_notes_seasoned`** — run (10w):
"two distinct periods a growing period and a resting period"
(Field value under Unit 2 — this field carries BOTH lifts; rewrite them together.)

## Unit 2 — asparagus, Missouri spring-freeze clause (R1)

**`asparagus` :: `hardiness_notes_seasoned`** — run (15w):
"spring freezes will not harm the crowns or subsequent harvests but can damage emerging spears"

⚠ This field also contains Unit 1's UC IPM clause (hit 1b). One pass over this field
should replace both.

Current value:
> The distinction that matters is crown versus top growth: the crown is deeply cold-hardy and overwinters dormant in the ground, riding out hard freezes, while the ferns and emerged spears are frost-tender. Missouri notes that spring freezes will not harm the crowns or subsequent harvests but can damage emerging spears, and a fall frost is what triggers the ferns to die back. That winter dormancy is not merely tolerated but needed: UC IPM describes asparagus as running on two distinct periods, a growing period and a resting period, so without a real cold-season rest the crown cannot recharge and a bed slowly declines, which is why it is a temperate crop rather than a tropical one. In the coldest, snow-poor winters, mulch the crowns, since the least cold-hardy types can injure in a deep freeze without snow cover.

## Unit 3 — asparagus soil, UMN sentence ⚠ PARAPHRASE CATCH (R1)

**`asparagus` :: `soil.preferred_description_seasoned`** — run (10w):
"in heavy medium or sandy soils as long as the"

⚠ Flag: the true overlap is the whole ~16-word UMN sentence; the author already swapped
single words (source's "soil" → our "ground", "rains" → "rain") and the structure still
matches. The full clause "grows in heavy, medium, or sandy soils as long as the ground
is well-drained and does not pool water after rain" needs a new structure, not another
word swap. The soil-tolerance FACTS (any texture if well-drained, no standing water)
are free to keep.

Current value:
> Give asparagus a deep, fertile, well-drained bed rich in organic matter and sited in full sun. The University of Minnesota notes it grows in heavy, medium, or sandy soils as long as the ground is well-drained and does not pool water after rain, and Michigan State stresses it does not tolerate saturated conditions: if water stands even an hour in the spot, it is too wet. A deep sandy loam is the classic asparagus soil because it drains freely and lets you dig the planting trench. Work in generous compost and clear perennial weeds before planting, because the crowns will hold that ground for 15 to 20 years.

## Unit 4 — USU Dixie "left in the ground quite late into winter" (R1, ×3 crops)

One sentence pattern from the same USU Washington-County fall-gardening PDF, repeated
across three crops with only the crop name changed. Write the replacement once, adapt
per crop. All three fields are `_beginner` register.

**4a. `beet` :: `regions.utah_dixie.region_notes_beginner`** — run (10w):
"beets can be left in the ground quite late into"

> In St. George's Dixie, sow beets direct in early March for a spring crop pulled by mid-May, before the real summer heat sets in. The bed then sits idle through June, since St. George routinely tops 100°F that month. Sow again from July 1 to August 1 for a fall crop: USU Extension notes beets can be left in the ground quite late into winter, so you can dig them as needed well past the first frost around November 1.

**4b. `carrot` :: `regions.utah_dixie.region_notes_beginner`** — run (9w):
"can be left in the ground quite late into"

> In St. George's Dixie, sow carrots direct in early March for a spring crop pulled by late May, before the summer heat sets in. The bed then sits idle through June, since St. George routinely tops 100°F that month. Sow again in July for a fall crop: USU Extension guidance notes carrots can be left in the ground quite late into winter, so you can dig them as needed well past the first frost around November 1.

**4c. `turnip` :: `regions.utah_dixie.region_notes_beginner`** — run (9w):
"can be left in the ground quite late into"

> In St. George's Dixie, sow turnips direct in mid-February for a spring crop pulled by late April, before the heat builds. The bed then sits idle through May and June, since St. George routinely tops 100°F in June. Sow again from July 1 to August 1 for a fall crop: USU Extension notes turnips can be left in the ground quite late into winter, so you can dig them as needed well past the first frost around November 1.

## Unit 5 — spring-onion, USU "planted spring or fall" sentence (R1)

Same USU PDF as Unit 4, different sentence — the longest attributed near-quote in the
set (16 words). Register `_seasoned`.

**`spring-onion` :: `regions.utah_dixie.region_notes_seasoned`** — run (16w):
"green onions can be planted spring or fall as they do not take long to mature"

> St. George grows green onions on two direct-sown cycles, since USU Extension's fall-gardening guidance for the St. George area notes green onions can be planted spring or fall as they do not take long to mature. The spring sowing runs from about Feb 15, USU's St. George Group A date for onions, with a quick harvest by late April. St. George's low desert heats up fast each spring and reaches 100°F in June, July, and August, so sowing pauses from May until a second sowing from about Aug 1 to Aug 20 restarts the crop once that heat begins to ease, cropping from late September up to the Nov 1 first frost, which a light touch sweetens but a hard freeze ends. Unlike the bulbing storage onion, green onion is harvested young and carries no day-length restriction.

## Unit 6 — cabbage, CTAHR "excellent garden crops" sentence (R1, ×5 hits, 2 text variants)

ONE CTAHR sentence. Four zone_notes carry identical text; region_notes_seasoned carries
a slight variant. One rewritten sentence clears all five hits.

**6a–6d. `cabbage` :: `regions.hawaii_tropical.resolved_by_zone.{10,11,12,13}.zone_notes`**
— run (10w): "are excellent garden crops at low elevations during winter and"
(identical value in all four zones):

> Cabbage is marginal in lowland tropical Hawaii and grown in the cool season; CTAHR notes the cabbages are excellent garden crops at low elevations during winter and year-round at cool high elevations. The low-elevation winter window (about October-November transplant) is modeled because the cited CTAHR bulletin B-91 is a scanned PDF that did not parse and does not table cabbage months. Harvest months derived.

**6e. `cabbage` :: `regions.hawaii_tropical.region_notes_seasoned`** — run (9w):
"excellent garden crops at low elevations during winter and"

> Cabbage is marginal in tropical lowland Hawaii: CTAHR frames the cabbages as excellent garden crops at low elevations during winter and as year-round crops at cool high elevations, where leaf diseases become the main concern. The low-elevation cool-season window is modeled on that qualitative guidance, since the cited CTAHR Bulletin B-91 is a scanned PDF that did not parse and does not list cabbage months directly. Treat the window and the derived harvest as a modeled estimate pending a parseable modern CTAHR source.

## Unit 7 — cherry-sour, NC State "favorable but need careful management" clause (R1, ×2 zones)

Identical sentence in both zones' suitability notes (fields differ only in the chill
numbers). Write once, apply twice.

**7a/7b. `cherry-sour` :: `regions.mid_atlantic.resolved_by_zone.{7,8}.suitability_note_seasoned`**
— run (15w): "where the climate is favorable but need careful management and will not consistently bear fruit"

Zone 7 value (zone 8 is identical except "roughly 1000 to 1350 chilling hours a year in
zone 8"):

> Chill is never the limiter here: the belt delivers roughly 1100 to 1500 chilling hours a year in zone 7, clearing this crop's variety range with margin (NC State Extension; regional four-source chill basket). What limits it is bloom and harvest weather, and NC State is direct about it: apricot and cherry trees grow where the climate is favorable but need careful management and will not consistently bear fruit. Cherries bloom early enough to meet a late freeze, and rain at ripening splits the fruit and invites brown rot, both of which run harder on the humid Piedmont and Coastal Plain than in the mountains. That said, sour cherry's own characteristics tilt the odds toward a crop: NC State notes the sour types are the hardier of the two cherries, and that sour cherry is self fertile while sweet cherry needs a second variety to pollinate, so a single tree can set fruit on its own. It also carries the belt's humidity better than sweet and ripens quickly, shortening its exposure to harvest rain. Treat it as the cherry to choose here and expect fruit in good years rather than every year.

## Unit 8 — chives, UF "cool-season herb that thrives" (R1)

**`chives` :: `regions.fl_peninsula.region_notes_beginner`** — run (12w):
"a cool season herb that thrives in florida s fall and spring"

Note: our own FIRST sentence already paraphrases this fact well; the second sentence
re-quotes it. Likely fix is deleting/merging the near-quote rather than adding words.

> On the Florida peninsula (zones 10 and 11), chives are a cool-season herb, best planted in fall and harvested through the mild winter and spring. UF/IFAS calls chives a cool-season herb that thrives in Florida's fall and spring; the plant rests through the hot, humid summer, so give it afternoon shade and water and let it come back as it cools.

## Unit 9 — echinacea, UF "fizzle out" voice (R1)

**`echinacea` :: `regions.fl_peninsula.region_notes_beginner`** — run (9w):
"a year or two and then fizzle out though"

The colloquial "fizzle out" is the source's voice; the fact (short-lived in FL, drainage
extends life) is free to keep.

> In peninsular Florida (zones 10 to 11), coneflowers can bloom from spring into late fall, but they often do not last long: the state's experts note some just grow a year or two and then fizzle out, though good drainage helps. Plant in late winter in full sun and the best-draining soil you can, keep it lean, and stick with the plain, tough kinds. Be ready to replant, since it may not come back for years the way it does up north.

## Unit 10 — english-cucumber, downy mildew importance sentence (R2)

**`english-cucumber` :: `diseases[1].symptoms_seasoned`** — run (12w):
"downy mildew is one of the most important leaf diseases of cucurbits"

Unattributed, in our voice. The symptom description around it is ours and fine.

> Angular yellow blotches bounded by the leaf veins appear on the upper surface, with a grayish or purplish fuzzy growth beneath in humid weather. Spots brown and run together, and severe infection rapidly defoliates the vines. Downy mildew is one of the most important leaf diseases of cucurbits, and the high humidity under cover can drive it hard.

## Unit 11 — fig, "leading killer" phrase (R2)

**`fig` :: `companions.bad_seasoned[0].why_seasoned`** — run (8w):
"root knot nematodes are the leading killer of"

The "leading killer" personification is the source's editorial phrase.

> Do not plant a fig into sandy soil known to carry heavy root-knot nematode populations, or straight into ground where a nematode-declined fig was just removed. Root-knot nematodes are the leading killer of figs in warm sandy regions, and because figs grow on their own roots there is no resistant rootstock to fall back on the way there is for stone fruit. The fix is site selection, not a companion plant: choose the best-drained, least infested ground, or replace a generous volume of soil.

## Unit 12 — lime, anthracnose epidemiology clause (R2)

**`lime` :: `diseases[5].cause_seasoned`** — run (11w):
"is most prevalent during the rainy season when flowers are present"

Our second sentence is the source's clause with the subject swapped to "It". The first
sentence is ours and already carries the same content — likely a delete/merge.

> The fungus Colletotrichum acutatum infects open flowers during rainy, humid conditions, causing the young fruit to abscise. It is most prevalent during the rainy season when flowers are present.

## Unit 13 — pawpaw, peduncle-borer sentence ⚠ PARAPHRASE CATCH (R2)

**`pawpaw` :: `pests[0].cause_seasoned`** — run (8w):
"into the fleshy tissues of the flower causing"

⚠ Flag: the true overlap is the source's whole ~20-word sentence; the author swapped
"burrows" → "bores" and compressed, and the structure still matches ("a small moth
larva … bores into the fleshy tissues of the flower, causing it to wither and drop").
Needs a new sentence shape. The facts (5 mm moth larva, feeds inside flowers, flowers
wither and drop, year-to-year variation) are free.

> Larvae of the pawpaw peduncle borer (Talponia plummeriana), a small moth. The larva, only about 5 millimeters long, bores into the fleshy tissues of the flower, causing it to wither and drop before it can set fruit. Populations vary sharply year to year.

## Unit 14 — raspberry, USU ripens-after-heat reasoning (R1)

**`raspberry` :: `regions.utah_dixie.region_notes_seasoned`** — run (11w):
"fruit ripens after the hottest part of the summer is over"

The reasoning chain (fall-bearers ripen post-heat → escape sunburn) is the source's
clause plus its "thus avoiding" logic, attributed "(USU Extension)".

> Raspberry is marginal in the St. George Dixie core: this is a hot, low, alkaline-soil site, the kind Utah State University Extension flags as difficult for the crop, while the county's dependable raspberry ground is its higher-elevation towns above the valley. The steer here is toward heat-tolerant, low-chill, fall-bearing (primocane) types, because in Utah's Dixie their fruit ripens after the hottest part of the summer is over and so escapes the sunburn that scorches a summer crop (USU Extension). Look to the fall-bearing cultivars Caroline, Josephine, Polana, Joan J, and Polka, or the low-chill desert canes Bababerry and Dorman Red. Plant dormant canes in late winter, and expect the alkaline soil to drive iron chlorosis, so treat yellowing leaves with a chelated iron. Give the planting afternoon shade to cut sunburn, mulch the shallow roots, use raised beds in heavy soil, and water steadily through the dry heat. Even managed well, treat this as a hard-won, shorter-lived planting than a cooler climate would give.

## Unit 15 — strawberry, "production highest in year one" clause (R2, ×3 hits, ONE field)

One field, one sentence, matched by THREE separate UC documents (the clause is UC
boilerplate repeated across their pubs). One rewrite clears all three hits.

**`strawberry` :: `regions.ca_north_coast.region_notes_seasoned`** — runs (12w/10w,
same sentence): "highest in the first full season after planting and declines after that"

> On California's cool, foggy north and central coast (zones 9 and 10, Monterey County north), strawberries are grown as a fall-planted annual system rather than a long-lived perennial bed. Set short-day (June-bearing) transplants from mid August to early September, or in the fall, and day-neutral types from late September into November; mid to late August is a good planting time in all coastal locations. Production is highest in the first full season after planting and declines after that, so replace the bed rather than carrying it for years. The cool maritime climate puts little heat stress on fruit set, the main flush builds to heaviest production in May and June, and day-neutral varieties can fruit across much of the year on the mild coast. Hard frost is rare, but protect open blossoms in any inland cold pocket. Grow on raised, well-drained beds and keep moisture off the flowers to limit fruit rot in the damp coastal air.

---

## Checklist recap

| unit | crop(s) | fields | hits | class |
|---|---|---|---|---|
| 1 | asparagus | description_seasoned + hardiness_notes_seasoned | 2 | R1 |
| 2 | asparagus | hardiness_notes_seasoned (same field as 1b) | 1 | R1 |
| 3 | asparagus | soil.preferred_description_seasoned ⚠ paraphrase catch | 1 | R1 |
| 4 | beet, carrot, turnip | regions.utah_dixie.region_notes_beginner ×3 | 3 | R1 |
| 5 | spring-onion | regions.utah_dixie.region_notes_seasoned | 1 | R1 |
| 6 | cabbage | hawaii zone_notes ×4 + region_notes_seasoned | 5 | R1 |
| 7 | cherry-sour | mid_atlantic suitability z7 + z8 | 2 | R1 |
| 8 | chives | regions.fl_peninsula.region_notes_beginner | 1 | R1 |
| 9 | echinacea | regions.fl_peninsula.region_notes_beginner | 1 | R1 |
| 10 | english-cucumber | diseases[1].symptoms_seasoned | 1 | R2 |
| 11 | fig | companions.bad_seasoned[0].why_seasoned | 1 | R2 |
| 12 | lime | diseases[5].cause_seasoned | 1 | R2 |
| 13 | pawpaw | pests[0].cause_seasoned ⚠ paraphrase catch | 1 | R2 |
| 14 | raspberry | regions.utah_dixie.region_notes_seasoned | 1 | R1 |
| 15 | strawberry | regions.ca_north_coast.region_notes_seasoned (3 sources) | 3 | R2 |

Verification after applying: `python3 tools/verbatim_scan.py <slug>` per touched crop —
the touched hits must disappear and no new HARD hits appear. Full ledger (for the
benign 308, NOT needed for this pass): `docs/pla202_verbatim_adjudication_c16071bc.json`.
