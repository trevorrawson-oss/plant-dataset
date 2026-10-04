# watermelon -- Phase C evidence packet (item 4)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on watermelon
| source | url | sha256 |
|---|---|---|
| Clemson HGIC Watermelon | https://hgic.clemson.edu/factsheet/watermelon/ | 77feea897363955a4b7c7321298faceb3f6e3ed17e5b7f3925ae78f35f03c568 |
| UGA C1035 | https://fieldreport.caes.uga.edu/publications/C1035/ | 121640611939808d0be0f7242de4a5d426e0eb30d596b8c1d09cc81731c8ddf9 |
| Clemson cucurbit insect pests | https://hgic.clemson.edu/factsheet/cucumber-squash-melon-other-cucurbit-insect-pests/ | 535e3615dc912a7fd78ca2996208390dad9e06dca0c7b80dc8e416daccf89c25 (no relevant sentence) |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 |
| OSU chart | https://ir.library.oregonstate.edu/downloads/v979v342w | f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33 |
| WSU | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | 7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34 |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 |

Cited, NOT hashed: aggie-horticulture.tamu.edu watermelons-in-texas; cameron.agrilife.org RGV guide; cucurbitbreeding.wordpress.ncsu.edu disease descriptions; edis.ifas.ufl.edu (root); extension.arizona.edu (+ az1005-2018 pdf); extension.umd.edu; **extension.umn.edu/fruit/growing-melons-home-garden**; extension.usu.edu frost pdf + planting dates; **extension.usu.edu/yardandgarden/research/watermelon-in-the-garden** (anchors yield_expectations); pubs.nmsu.edu; ucanr.edu time-planting; ctahr.hawaii.edu; uaex.uada.edu; unlv.edu; yardandgarden.extension.iastate.edu.

`yield_expectations.sources` = ["uga_ext", "usu_ext"] (UGA C1035 hashed; USU watermelon NOT hashed).

## Decision-row quote: Clemson's 24 sq ft sentence (clause ruled DROPPED)
Clemson 77feea89, in sequence:
> "watermelons need a lot of room." / "plant them in rows 6 to 8 feet apart." / "transplants or seed in 6 foot row spacing should be 4 feet apart and 3 feet apart in 8 foot row spacing." / **"a rule of thumb is to allow 24 square feet per plant."**

## The "vine runs 8 to 12 feet" claim
**NO HASHED CITED PAGE STATES IT.** Searched every hashed cited page for "12 feet/ft", "8 to 12", "8-12", "10 feet", "vine(s) grow/spread/run/reach/sprawl". Closest hashed sentences (none gives a vine length): VH021 (watermelon row): "watermelon large : jubilee (aka fl giant), crimson sweet, charleston grey 133 small : sugar baby, mickeylee vines require lots of space."; Clemson: "watermelons need a lot of room."; UGA: "it requires a lot of space, sunshine, water and nutrients." -> **cut unless Trevor rules otherwise.**

## Leaf: `yield_expectations.per_plant_seasoned`
CURRENT:
> A healthy full-size watermelon vine typically yields 2 to 4 marketable melons, while icebox and bush types set more, smaller fruit. Limiting fruit to two or three per vine on full-size types channels energy into larger, better-filled melons. Plants need plenty of room, roughly 24 square feet each for full-size types, and even moisture and modest feeding through sizing build sweet fruit.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | full-size vine yields 2 to 4 melons | NOT STATED per plant. WSU table gives 3 plants and 6-12 melons per 10-ft row (2-4/plant only by arithmetic) | WSU (table header "table plants per 10-ft row production per 10-ft row average pounds consumed per adult per year fresh processed total"): "...watermelon 3 6-12 melons 10 0 10..." |
| 2 | "marketable" | NO HASHED CITED PAGE STATES IT |
| 3 | icebox and bush types set more, smaller fruit | NO HASHED CITED PAGE STATES IT (UGA only lists varieties by size/type) | UGA: "...varieties by size size varieties large mardi gras, royal majesty, sangria, au-producer round baby doll, crimson sweet, ice box, imagination, jade star small palm melon, solitaire varieties by type type varieties early bush sugar baby, golden crown, sugar baby, yellow baby seedless..." |
| 4 | limit to two or three fruit per vine for larger melons | NO HASHED CITED PAGE STATES IT |
| 5 | plants need plenty of room | MAPPED | Clemson: "watermelons need a lot of room."; UGA: "it requires a lot of space, sunshine, water and nutrients." |
| 6 | roughly 24 sq ft each for full-size | RULED DROP (Clemson states it, quote above; "for full-size types" qualifier is not on the page) |
| 7 | even moisture through sizing | MAPPED | Clemson: "although watermelon plants should not suffer from lack of water during any growth stage, it is extremely important to maintain consistent irrigation cycles during fruit set and development." |
| 8 | modest feeding through sizing | PARTIAL | Clemson: "sidedress a second time after bloom when fruit is developing on the vine." / "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth." |
| 9 | (moisture + feeding) build sweet fruit | NO HASHED CITED PAGE STATES the link to sweetness |

## Leaf: `yield_expectations.factors_seasoned[2]`
CURRENT:
> Space and vine vigor: full-size vines sprawl 8 to 12 feet and need about 24 square feet each; crowding cuts yield and worsens disease.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | full-size vines sprawl 8 to 12 feet | NO HASHED CITED PAGE STATES IT |
| 2 | need about 24 sq ft each | RULED DROP |
| 3 | crowding cuts yield | MAPPED | Clemson: "excessive vine growth and few fruit are usually the result of an over-application of nitrogen fertilizer or by planting too close." |
| 4 | crowding worsens disease | NO HASHED CITED PAGE STATES IT for watermelon (WSU general: "if planted too close, plants will compete with their neighbors for light, water, and fertilizer." -- competition, not disease) |

## Leaf: `soil_prep_seasoned`
CURRENT:
> Prepare a deep, light, well-drained bed in full sun and work a few inches of compost into the soil before planting, easing off heavy nitrogen so the plant builds fruit rather than runaway vine. Most growers plant on low, wide hills or raised mounds, which warm faster, drain better, and give the trailing vines a starting point. Space generously: hills run about 8 feet apart on all sides for full-size types (closer for icebox and bush kinds), because a full-size vine can run 8 to 12 feet and wants about 24 square feet to itself. Black plastic mulch is a real help in shorter or cooler-summer areas, warming the soil and speeding an early start. On heavy or wet ground, build the mounds up to improve drainage and head off wilt and fruit rot.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | well-drained bed | MAPPED | UGA: "watermelons need a well-drained soil that receives 8 to 10 hr of sunlight per day." |
| 2 | deep, light soil | NO HASHED CITED PAGE STATES IT (USU/UMN sandy-soil pages not hashed) |
| 3 | full sun | MAPPED | UGA (as #1) |
| 4 | work compost in before planting | MAPPED | UGA: "adding organic matter in the form of topsoil, compost or a bagged amendment and incorporating into the native soil can help improve soil quality." |
| 5 | "a few inches" of compost | NO HASHED CITED PAGE STATES IT |
| 6 | ease off heavy nitrogen so plant builds fruit, not vine | MAPPED | Clemson: "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth." |
| 7 | plant on hills | MAPPED | UGA: "starting seeds plant watermelon from seed in small hills with a spacing of 8 ft on all sides." |
| 8 | "most growers"; "low, wide" hills or raised mounds | NO HASHED CITED PAGE STATES IT (UGA says "small hills") |
| 9 | hills warm faster, drain better, give vines a starting point | NO HASHED CITED PAGE STATES IT |
| 10 | hills about 8 feet apart on all sides | MAPPED | UGA (as #7) |
| 11 | ...for full-size types | NOT STATED (UGA gives 8 ft without a type qualifier) |
| 12 | closer for icebox and bush kinds | NO HASHED CITED PAGE STATES IT |
| 13 | a full-size vine can run 8 to 12 feet | NO HASHED CITED PAGE STATES IT |
| 14 | wants about 24 sq ft | RULED DROP |
| 15 | black plastic warms the soil / early start | MAPPED | Clemson: "black plastic in the field gives watermelons an early start to growth." / "the black plastic absorbs the sun's warmth, allowing the soil to warm quickly." / "the black plastic will warm the soil faster in the spring and will also conserve moisture throughout the season." |
| 16 | ...especially in shorter or cooler-summer areas | NO HASHED CITED PAGE STATES IT (WSU general: "black plastic mulch absorbs heat and warms the soil in the spring and summer, creat- ing a better environment early in the season for warm-season crops such as melons, tomatoes, and peppers.") |
| 17 | on heavy/wet ground build mounds up for drainage | NO HASHED CITED PAGE STATES IT |
| 18 | ...to head off wilt and fruit rot | NO HASHED CITED PAGE STATES IT (Clemson credits plastic mulch, not mounds: "other advantages of this type of mulch are weed control and a reduction of fruit rot.") |

## Other watermelon leaves that also carry "8 to 12 feet" (not named in the item; listed so Trevor can decide)
- `yield_expectations.first_year_note_seasoned` ("...how much room the vines take (8 to 12 feet for full-size types)...")
- `growth_stages[2].user_action_seasoned` ("...give the runners room to spread, 8 to 12 feet for full-size types.")
- `tips_by_stage.vining[0].text_seasoned` ("Give full-size types 8 to 12 feet to sprawl.")
- `soil_prep_beginner` ("...since the vines can spread 8 to 12 feet (icebox and bush types need less).")
No other leaf states 24 sq ft except `verification_status.verification_log_ref` and `open_findings[1].summary` (append-only records).

## Spacing context (not a conflict; for completeness)
planting_layout hill-none (default) hill 96 / rows 96 / 2 per hill <- UGA "plant watermelon from seed in small hills with a spacing of 8 ft on all sides." / "a week after they have germinated, thin the seedlings to two per hill."; row-none in_row [60,72] <- Clemson "plants should be spaced 5 to 6 feet apart within the row.", rows [72,96] <- Clemson "seeds or transplants should be planted in rows spaced 6 to 8 feet apart." (pla10_promote1 EVIDENCE).


## ADDITION B: four more leaves carrying "8 to 12 feet"

Canonical read: sha256 b331e5f2..., HEAD 6e444f3 (main). Hashes re-verified over the bytes this pass (all 7 hashed cited pages: sha OK). Quotes in `norm_text` form, each machine-checked as a substring of its hashed text. Source shorthand = the hashed-page table at the top of this packet (Clemson 77feea89; Clemson insects 535e3615; UGA 12164061; VH021 7ff585e6; WSU 7378f653; OSU f2fdb1d6).

The "8 to 12 feet" vine run: **NO HASHED CITED PAGE STATES IT** (established above; re-searched this pass, same result). The only watermelon-row figures on OSU are planting spacing, not vine length: OSU: "watermelons 4 weeks not suitable may not suitable may 6 plants 72" 60"".

### Leaf: `yield_expectations.first_year_note_seasoned`
CURRENT:
> The usual first-year surprises are how much room the vines take (8 to 12 feet for full-size types), how pollinator-dependent fruit set is, and how much ripeness judgment matters, since the melon does not finish off the vine. Give plants far more space than seems necessary, grow flowers nearby for bees, and learn the tendril-and-ground-spot check before you cut.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | the vines take a lot of room | MAPPED | Clemson: "watermelons need a lot of room." / UGA: "it requires a lot of space, sunshine, water and nutrients." |
| 2 | 8 to 12 feet for full-size types | NO HASHED CITED PAGE STATES IT |
| 3 | fruit set is pollinator-dependent | MAPPED | Clemson: "consequently, wind movement of pollen from male to female flowers is inadequate, and insects, such as honeybees, native bumblebees, and others, are necessary for proper pollination." / VH021: "all cucurbits have male and and female flowers separated on the plant and pollination by insects is required for fruit set." |
| 4 | ripeness judgment matters | MAPPED (pages give multi-sign ripeness checks) | Clemson: "a few rules of thumb to use to help determine if the watermelon variety is ready for harvest: the fruit looks to be expected size, the tendril closest to the fruit turns brown, the skin color loses its gloss and becomes dull in color, and the bottom of the fruit has a large white to cream color oval spot." |
| 5 | the melon does not finish (ripen) off the vine | NO HASHED CITED PAGE STATES IT |
| 6 | "first-year surprises" framing | NO HASHED CITED PAGE STATES IT (framing) |
| 7 | give far more space than seems necessary | PARTIAL ("a lot of room"; "far more than seems necessary" is not stated) | Clemson: "watermelons need a lot of room." |
| 8 | grow flowers nearby for bees | NO HASHED CITED PAGE STATES IT for watermelon/bees. VH021 says plant flowers, but in its BENEFICIAL-INSECT (pest-predator) list; WSU says companion planting can attract pollinators (general); Clemson's own pollinator advice is a honeybee colony | VH021: "plant flowers in the vegetable garden." / WSU: "companion planting can help attract pollinators, improving pollination for certain crops that may be less desirable to pollinators." / Clemson: "to promote proper pollination, consider establishing a honeybee colony on site." |
| 9 | tendril check | MAPPED | UGA: "the watermelon is ready to be picked when the tendril opposite the fruit stem is completely dry." / VH021: "harvest when the melon underside begins to turn yellow or when fruit tendril shrivels." |
| 10 | ground-spot check | MAPPED | UGA: "other signs of ripeness include yellowing of the underside of the fruit and a dull thump sound when tapping the fruit." / Clemson (as #4: "...the bottom of the fruit has a large white to cream color oval spot.") |

### Leaf: `growth_stages[2].user_action_seasoned` (stage id "vining")
CURRENT:
> Side-dress with a little nitrogen as the vines run, then ease off, mulch to hold moisture, and give the runners room to spread, 8 to 12 feet for full-size types. Scout for spider mites and aphids on leaf undersides.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | side-dress with nitrogen as the vines run | MAPPED, but TIMING DIFFERS: Clemson says side-dress BEFORE the vines start to run, then again after bloom | Clemson: "melons should be side-dressed before the vines start to "run." side-dress with 34-0-0 at 1 pound per 100 feet of row or calcium nitrate (15.5-0-0) at 2 pounds per 100 feet of row." / Clemson: "sidedress a second time after bloom when fruit is developing on the vine." |
| 2 | "a little" nitrogen | PARTIAL (Clemson gives a rate, not "a little") | Clemson (as #1) |
| 3 | then ease off (nitrogen) | MAPPED as rationale | Clemson: "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth." |
| 4 | mulch to hold moisture | MAPPED | UGA: "mulch the plants with weed-free grass clippings (already dried, not green), straw or wood chips to prevent weeds from growing and to conserve water." |
| 5 | give the runners room to spread | MAPPED | Clemson: "watermelons need a lot of room." |
| 6 | 8 to 12 feet for full-size types | NO HASHED CITED PAGE STATES IT |
| 7 | scout for spider mites | MAPPED (pest named; damage described on UPPER leaf sides) | Clemson insects: "spider mites two-spotted spider mites ( tetranychus urticae ) can be a serious problem on cucurbits, especially on watermelons and cantaloupes, during hot, dry weather." / Clemson insects: "this damage appears as pale yellow and reddish-brown spots ranging in size from small specks to large whitish, stippled areas on the upper sides of leaves." |
| 8 | scout for aphids | MAPPED | Clemson insects: "melon aphids ( aphis gossyppi ) and several other aphid species attack cucurbits, particularly melons and cucumbers." / "usually, cucurbits are not attacked by aphids until the vines form runners." |
| 9 | ...on leaf undersides | MAPPED for APHIDS only; for spider mites NO HASHED CITED PAGE STATES undersides (Clemson describes the mite damage on upper sides, #7) | Clemson insects (melon aphids): "they are found chiefly on the underside of the leaves, where they suck the sap from the plants and cause a reduction in the quality and quantity of the fruit." |

### Leaf: `tips_by_stage.vining[0].text_seasoned`
CURRENT:
> Go easy on nitrogen once the vines run. Too much gives lush vine at the expense of fruit and sugar, which is the classic watermelon mistake. Give full-size types 8 to 12 feet to sprawl.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | go easy on nitrogen once the vines run | PARTIAL: the caution is stated; the "once the vines run" timing is not (Clemson side-dresses before the run and again after bloom) | Clemson: "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth." / Clemson: "sidedress a second time after bloom when fruit is developing on the vine." |
| 2 | too much gives lush vine at the expense of fruit | MAPPED | Clemson: "excessive vine growth and few fruit are usually the result of an over-application of nitrogen fertilizer or by planting too close." |
| 3 | ...and (at the expense of) sugar | NO HASHED CITED PAGE STATES IT (VH021 links sugar loss to water, not nitrogen: "overwatering or heavy rainfall reduces sugar content of maturing fruit.") |
| 4 | the classic watermelon mistake | NO HASHED CITED PAGE STATES IT |
| 5 | give full-size types 8 to 12 feet to sprawl | NO HASHED CITED PAGE STATES IT |

### Leaf: `soil_prep_beginner`
CURRENT:
> Pick a sunny spot with light, well-drained soil and mix in some compost before planting, but do not overdo rich, high-nitrogen material, or you get more vine than melon. Plant watermelon on low hills or mounds, which warm up and drain better. Give it lots of room: space hills about 8 feet apart on all sides for full-size types, since the vines can spread 8 to 12 feet (icebox and bush types need less). In cooler or shorter-summer areas, laying down black plastic mulch warms the soil and gives the plants an earlier, faster start. If your soil is heavy or stays wet, build the mounds up higher so water drains away from the roots and fruit.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | sunny spot | MAPPED | UGA: "watermelons need a well-drained soil that receives 8 to 10 hr of sunlight per day." |
| 2 | well-drained soil | MAPPED | UGA (as #1) |
| 3 | light soil | NO HASHED CITED PAGE STATES IT |
| 4 | mix in some compost before planting | MAPPED | UGA: "adding organic matter in the form of topsoil, compost or a bagged amendment and incorporating into the native soil can help improve soil quality." |
| 5 | don't overdo high-nitrogen material, or more vine than melon | MAPPED | Clemson: "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth." |
| 6 | plant on hills | MAPPED | UGA: "starting seeds plant watermelon from seed in small hills with a spacing of 8 ft on all sides." |
| 7 | "low" hills or mounds | NO HASHED CITED PAGE STATES IT (UGA says "small hills") |
| 8 | hills warm up and drain better | NO HASHED CITED PAGE STATES IT |
| 9 | give it lots of room | MAPPED | Clemson: "watermelons need a lot of room." |
| 10 | hills about 8 feet apart on all sides | MAPPED | UGA (as #6) |
| 11 | ...for full-size types | NOT STATED (UGA gives 8 ft with no type qualifier) |
| 12 | the vines can spread 8 to 12 feet | NO HASHED CITED PAGE STATES IT |
| 13 | icebox and bush types need less | NO HASHED CITED PAGE STATES IT (UGA lists them by size/type only: "...varieties by size size varieties large mardi gras, royal majesty, sangria, au-producer round baby doll, crimson sweet, ice box, imagination, jade star small palm melon, solitaire varieties by type type varieties early bush sugar baby, golden crown, sugar baby, yellow baby seedless...") |
| 14 | black plastic warms the soil, earlier/faster start | MAPPED | Clemson: "black plastic in the field gives watermelons an early start to growth." / Clemson: "the black plastic will warm the soil faster in the spring and will also conserve moisture throughout the season." |
| 15 | ...in cooler or shorter-summer areas | NO HASHED CITED PAGE STATES IT (WSU general, not area-qualified: "black plastic mulch absorbs heat and warms the soil in the spring and summer, creat- ing a better environment early in the season for warm-season crops such as melons, tomatoes, and peppers.") |
| 16 | heavy / wet soil: build mounds up higher for drainage | NO HASHED CITED PAGE STATES IT for watermelon mounds. WSU (general vegetables) recommends RAISED BEDS for drainage | WSU: "in areas with heavy rainfall, plant in raised beds (see below) to allow for water drainage." / WSU: "soil drainage is determined mostly by the site but can be improved by using raised beds." |
| 17 | ...so water drains away from roots and fruit | NO HASHED CITED PAGE STATES IT (fruit-rot reduction is credited to plastic mulch, not mounds: Clemson: "other advantages of this type of mulch are weed control and a reduction of fruit rot.") |

No other watermelon leaf carries "8 to 12 feet" beyond these four and the three in the item (`yield_expectations.per_plant_seasoned` does not; `yield_expectations.factors_seasoned[2]` and `soil_prep_seasoned` do, both above). Grep of the crop for "8 to 12|12 feet" returns exactly 6 leaves.
