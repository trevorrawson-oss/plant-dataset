# PLA-673 part B2 packet: the 7 unsupported-claim leaves

Read-only on canonical `350eda38`. For each leaf: its full current text, then per claim every sentence on a HASHED page CITED ON THAT CROP that bears on it, in `norm_text` form, machine-checked as a substring of the hashed bytes. **Nothing authored.** Clemson eggplant (`635ebdeb`) was hashed into MANIFEST for this packet. Candidates were collected by `build_b2_candidates.py` and curated by reading; sentences about other crops on multi-crop pages are left out.

## Pages

| key | url | sha256 |
| -- | -- | -- |
| clem_pep | https://hgic.clemson.edu/factsheet/pepper/ | `38a7621d2872c397731525703a8805c3a30d2690221a02b826a5b21655ed7b8b` |
| isu_pep | https://yardandgarden.extension.iastate.edu/how-to/growing-peppers-home-garden | `2ac60d9db000b01b642f9708d92ac558cb563977bd615236afa95ce69cb1bb2e` |
| umd_pep | https://extension.umd.edu/resource/growing-peppers-home-garden | `4fe5a4ddae5c61744f5919ac66105662c70483d16207334fe7d5221db9612c6f` |
| umn_pep | https://extension.umn.edu/vegetables/growing-peppers | `63c34d25065b048a01c6d94658a1f1a588be3c96bd1bfc8a7b335ddd5ad59a18` |
| uga_c1005 | https://fieldreport.caes.uga.edu/publications/C1005/home-garden-peppers/ | `0e405e6e03e1a37799c1bac71389bbbb940d838dbd6b51633b3ed9e1a5902cd0` |
| clem_egg | https://hgic.clemson.edu/factsheet/eggplant-insect-pests-diseases/ | `635ebdeb95b6eef707da87fd518791271c2288e0499e9972611f7f4261380362` |
| ncsu_egg | https://plants.ces.ncsu.edu/plants/solanum-melongena/ | `1b4f38949eaee005a240cb656da863d660710bcc6eea6aeae72bb1ec912ca72a` |
| uf | https://edis.ifas.ufl.edu/publication/VH021 | `7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994` |
| wsu | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | `7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34` |
| c1206 | https://fieldreport.caes.uga.edu/publications/C1206/homegrown-pumpkins/ | `77c14ecc0f33684af662ad9e5573a363c4ca6d0049ce783d773de0f340a41c1b` |
| umn_pk | https://extension.umn.edu/vegetables/pumpkins-and-winter-squash | `fbdd655463e4b574a2798b457bcb0e469bc6456036f60615f04cc3619384e91f` |
| osu | https://ir.library.oregonstate.edu/downloads/v979v342w | `f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33` |
| vt | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | `52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720` |

## A. Pepper / eggplant: `prevention_seasoned` of the Phytophthora blight entry (seasoned register)

* **bell-pepper** `diseases[1].prevention_seasoned` (id `phytophthora-blight`; sources ['ncsu_ext', 'clemson_hgic']):
  > Plant on raised, well-drained beds or hills, avoid low spots that stay wet, water at the soil rather than overhead, do not overwater, mulch to limit splash, rotate away from peppers and other susceptible crops for at least three to four years, and keep fruit up off saturated soil.
* **banana-pepper** `diseases[1].prevention_seasoned` (id `phytophthora-blight`; sources ['ncsu_ext', 'clemson_hgic']):
  > Plant on raised, well-drained beds or hills, avoid low spots that stay wet, water at the soil rather than overhead, do not overwater, mulch to limit splash, rotate away from peppers and other susceptible crops for at least three to four years, and keep fruit up off saturated soil.
* **eggplant** `diseases[3].prevention_seasoned` (id `phytophthora-blight`; sources ['clemson_hgic']):
  > Plant on raised, well-drained beds or hills, avoid low spots that stay wet, water at the soil rather than overhead, mulch to limit splash, rotate away from solanaceous and cucurbit crops, and keep fruit up off saturated soil.

Hashed cited pages: bell-pepper 8 (UMN, UMD, ISU, Clemson pepper, UF, WSU, VT, OSU); banana-pepper 9 (adds UGA C1005); eggplant 6 (Clemson eggplant, now hashed; NCSU toolbox; UF, WSU, VT, OSU). Cited but NOT hashed, so not read: bell-pepper 22 urls, banana-pepper 20, eggplant 25, among them the peppers' Phytophthora anchor NCSU pepper-diseases (an index page of links when fetched to scratch). Rows marked 'banana-pepper only' are not cited on bell-pepper.

**Claim: raised, well-drained beds or hills**: NOT STATED for pepper/eggplant or for Phytophthora on any hashed cited page. Raised beds appear only as WSU's general drainage advice; no page says hills

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 1 | wsu `7378f653` | "soil drainage is determined mostly by the site but can be improved by using raised beds." | general, all crops | p. 3, char 5748 |
| 2 | wsu `7378f653` | "in areas with heavy rainfall, plant in raised beds (see below) to allow for water drainage." | general, all crops | p. 9, char 16602 |
| 3 | wsu `7378f653` | "raised beds improve drain- 15 age by allowing water to drain from the bed into the alleyway through the force of gravity." | general, all crops | char 31413 (spans a page break) |

**Claim: well-drained (soil)**: STATED (site/soil), not as a disease measure

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 4 | clem_pep `38a7621d` | "select a well-drained, loamy, or sandy loam soil for planting." | peppers | char 70056 |
| 5 | isu_pep `2ac60d9d` | "location pepper plants perform best in well-drained soils in full sun." | peppers | char 11059 |
| 6 | umd_pep `4fe5a4dd` | "plant peppers in well-drained soil or containers (5-gallon minimum)." | peppers | char 5728 |
| 7 | uga_c1005 `0e405e6e` | "peppers need a well-drained soil that receives 8 to 10 hr of sun per day." | peppers; cited on banana-pepper only | char 97128 |
| 8 | ncsu_egg `1b4f3894` | "it prefers moist, well-drained, fertile, sandy, and loamy soils with a ph range of 5.5 to 6.8." | eggplant | char 1941 |
| 9 | uf `7ff585e6` | "irrigation and drainage vegetables cannot tolerate standing water from excessive rainfall or irrigation." | general | char 9425 |

**Claim: avoid low spots that stay wet**: PARTIAL: excess soil moisture -> Phytophthora is STATED for eggplant (Clemson); 'low spots' is on no page

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 10 | clem_egg `635ebdeb` | "avoiding excessive soil moisture is an important strategy for managing phytophthora diseases ." | eggplant | char 76582 |
| 11 | clem_egg `635ebdeb` | "excessive soil moisture increases the incidence of root rots and blight caused by phytophthora and pythium ." | eggplant | char 80343 |
| 12 | uga_c1005 `0e405e6e` | "they self-pollinate, enjoy full sun, and do not tolerate frost or cool, wet soil." | peppers; banana-pepper only | char 96709 |
| 13 | uf `7ff585e6` | "irrigation and drainage vegetables cannot tolerate standing water from excessive rainfall or irrigation." | general | char 9425 |

**Claim: water at the soil rather than overhead**: STATED (peppers: UMN, UMD, UGA; eggplant: Clemson)

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 14 | umn_pep `63c34d25` | "avoid overhead sprinkling." | peppers | char 15311 |
| 15 | umn_pep `63c34d25` | "wet leaves are more disease prone." | peppers | char 15338 |
| 16 | umd_pep `4fe5a4dd` | "drip irrigation and soaker hoses are excellent methods for watering peppers." | peppers | char 8060 |
| 17 | uga_c1005 `0e405e6e` | "water peppers with drip irrigation or soaker hoses when possible to keep the root zone moist." | peppers; banana-pepper only | char 98039 |
| 18 | isu_pep `2ac60d9d` | "the disease organism can be spread by rain or during overhead irrigation." | peppers, BACTERIAL SPOT paragraph | char 15963 |
| 19 | clem_egg `635ebdeb` | "drip irrigation is the preferred method of watering versus overhead watering, as this keeps water off the foliage and fruit, reducing the severity of foliar diseases and fruit rots." | eggplant | char 79892 |
| 20 | clem_egg `635ebdeb` | "if unable to drip irrigate, direct water to the base of the plants and avoid wetting the leaves as much as possible." | eggplant | char 80074 |

**Claim: do not overwater (pepper leaves only)**: PARTIAL: 'moist but not saturated' is STATED (Clemson pepper, blossom-end-rot context; Clemson eggplant)

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 21 | clem_pep `38a7621d` | "to prevent blossom end rot, keep the soil uniformly moist, but not saturated." | peppers, blossom end rot | char 75263 |
| 22 | clem_egg `635ebdeb` | "water frequently enough to keep the soil moist but not saturated." | eggplant | char 80277 |

**Claim: mulch to limit splash**: NOT STATED: no page ties mulch to splash. UMN pepper says splashed soil carries spores, in its overhead-watering paragraph; the mulch sentences are about weeds and moisture

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 23 | umn_pep `63c34d25` | "soil splashed up onto the leaves can contain disease spores." | peppers, overhead-watering paragraph | char 15373 |
| 24 | clem_pep `38a7621d` | "mulching can help to retain consistent soil moisture, conserve water, and reduce weeds." | peppers | char 72961 |
| 25 | umn_pep `63c34d25` | "mulching with herbicide-free grass clippings, weed-free straw or other organic material to a depth of three to four inches can help prevent weed growth, decreasing the need for frequent cultivation." | peppers | char 16179 |
| 26 | uga_c1005 `0e405e6e` | "mulch peppers with compost, straw or wood chips to prevent weeds from growing and to conserve water." | peppers; banana-pepper only | char 97899 |

**Claim: rotation: peppers 'away from peppers and other susceptible crops for at least three to four years'; eggplant 'away from solanaceous and cucurbit crops'**: PEPPERS: rotation STATED, '3-4 years' NOT STATED. EGGPLANT: CONTRADICTED. Clemson eggplant (the leaf's own source) says avoid solanaceous crops for three years and 'instead, rotate WITH cucurbits'

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 27 | clem_pep `38a7621d` | "reduce disease problems by: rotating planting locations." | peppers | char 76813 |
| 28 | uga_c1005 `0e405e6e` | "rotate planting locations regularly." | peppers; banana-pepper only | char 100061 |
| 29 | wsu `7378f653` | "crop rotation rotating crops by family (table 7) helps prevent soil-borne diseases, such as verticillium wilt and phytophthora root rot that are common in the pacific northwest, from building up in the soil." | general | p. 22, char 42419 |
| 30 | wsu `7378f653` | "follow a 5-7 year rotation if possible, which means not planting crops within the same family in the same bed or row for 5-7 years." | general | p. 22, char 42627 |
| 31 | clem_egg `635ebdeb` | "strategies for managing diseases in eggplant crop rotation is an important strategy for managing bacterial wilt, phytophthora blight, and southern blight because the pathogens survive in soil." | eggplant | char 78910 |
| 32 | clem_egg `635ebdeb` | "avoid planting eggplant where tomatoes, potatoes, peppers, or eggplant (all members of the solanaceae family) were planted within the last three years." | eggplant | char 79103 |
| 33 | clem_egg `635ebdeb` | "instead, rotate with cucurbits (squash, zucchini, melons, and cantaloupe), brassicas (collards, kale, cabbage, turnips, and broccoli), grasses (sweet corn and grains), alliums (onions, garlic, and leeks), etc." | eggplant: CONTRADICTS 'away from ... cucurbit crops' | char 79255 |

**Claim: keep fruit up off saturated soil**: NOT STATED on any hashed cited page

(no hashed sentence bears on it)

**Claim: the disease itself (Phytophthora blight)**: Named on Clemson eggplant only; NO hashed page cited on bell- or banana-pepper names Phytophthora

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 34 | clem_egg `635ebdeb` | "avoiding excessive soil moisture is an important strategy for managing phytophthora diseases ." | eggplant | char 76582 |

## B. Squash: `soil_prep_seasoned` (seasoned register)

* **pumpkin** `soil_prep_seasoned`:
  > Prepare a deep, fertile, well-drained bed in full sun, working several inches of compost or rotted manure into the soil before planting, since pumpkins are big, hungry, long-season plants. Most growers plant in low hills or mounds about a foot across, which warm faster, drain better, and give the sprawling vines a starting point. Space hills generously: at least 8 feet apart on all sides for full-size vining types (closer for bush and miniature kinds), because a full-size vine can run 10 to 20 feet. On heavy or wet ground, build the mounds up for drainage to head off crown and Phytophthora fruit rot.
* **butternut-squash** `soil_prep_seasoned`:
  > Prepare a deep, fertile, well-drained bed in full sun, working several inches of compost or rotted manure into the soil before planting, since butternut is a big, hungry, long-season plant. Many growers plant in low hills or mounds about a foot across, which warm faster, drain better, and give the sprawling vines a starting point. Space generously: roughly 24 to 36 inches between plants in the row with 5 to 6 feet between rows for full-size vining types (closer for the bush Butterbush), because a full-size vine can run 8 to 12 feet. On heavy or wet ground, build the mounds up for drainage to head off crown and fruit rot.
* **acorn-squash** `soil_prep_seasoned`:
  > Prepare a fertile, well-drained bed in full sun, working several inches of compost or rotted manure into the soil before planting, since acorn squash is a hungry, warm-season plant. Many growers set plants in low hills or mounds about a foot across, which warm faster in spring, drain better, and give the plants a clear starting point. Space to the type: bush and semi-bush acorn squash can go about 18 to 24 inches apart, while vining types want 24 to 36 inches in the row with 5 to 6 feet between rows, since the vines run 4 to 8 feet. On heavy or wet ground, build the mounds up for drainage to head off crown and fruit rot.
* **spaghetti-squash** `soil_prep_seasoned`:
  > Prepare a fertile, well-drained bed in full sun, working several inches of compost or rotted manure into the soil before planting, since spaghetti squash is a hungry, long-season plant. Many growers set plants in low hills or mounds about a foot across, which warm faster in spring, drain better, and give the vines a clear starting point. Space generously: roughly 24 to 36 inches between plants in the row with 5 to 6 feet between rows for vining types (closer for bush types like Tivoli), because the vines can run 6 to 8 feet. On heavy or wet ground, build the mounds up for drainage to head off crown and fruit rot.

All four cite UGA C1206 (a pumpkin publication), UMN pumpkins-and-winter-squash, UF, WSU, VT, OSU; the beginner siblings state no width. Cited but NOT hashed: 19-20 urls per crop, not read. Every claim of each leaf is covered (the touched-leaf rule); claims a leaf does not make are marked by crop in the claim line.

**Claim: deep, fertile, well-drained bed in full sun**: STATED for pumpkins (C1206: full sun, deep tilling, well-drained); 'fertile' is a soil-test/fertilizer topic on the pages

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 35 | c1206 `77c14ecc` | "site selection and preparation like most vegetables, pumpkins do best when grown in full sunlight conditions." | pumpkins | char 95079 |
| 36 | c1206 `77c14ecc` | "planting in weed-free, well- drained soil will help ensure success." | pumpkins | char 95189 |
| 37 | c1206 `77c14ecc` | "soil should be prepared by deep tilling and adding organic matter, if possible." | pumpkins | char 95525 |
| 38 | umn_pk `fbdd6554` | "the soil should be moisture retentive yet well-drained." | pumpkins and winter squash | char 12852 |

**Claim: work several inches of compost or rotted manure in before planting**: PARTIAL: compost / well-rotted manure STATED (UMN), organic matter at prep STATED (C1206); 'several inches' NOT STATED

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 39 | umn_pk `fbdd6554` | "you can improve your soil by adding well-rotted manure or compost in spring or fall." | pumpkins and winter squash | char 12451 |
| 40 | umn_pk `fbdd6554` | "do not use fresh manure as it may contain harmful bacteria and may increase weed problems." | pumpkins and winter squash | char 12536 |
| 41 | umn_pk `fbdd6554` | "if you use manure or compost, you may not need additional fertilizer applications, depending on how much organic matter you apply." | pumpkins and winter squash | char 12627 |

**Claim: big / hungry / long-season plant**: PARTIAL: long season STATED for pumpkins (90-120 days); 'hungry' NOT STATED

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 42 | c1206 `77c14ecc` | "maturity dates can vary from 90 to 120 days, so gardeners should allow that much time for harvest." | pumpkins | char 96125 |

**Claim: low hills or mounds**: STATED (UGA C1206, a PUMPKIN publication, cited on all four; UMN says raised BEDS for drainage)

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 43 | c1206 `77c14ecc` | "plant pumpkins in hills, with at least 8 feet of space on all sides." | pumpkins | char 95257 |
| 44 | c1206 `77c14ecc` | "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage." | pumpkins | char 95326 |
| 45 | c1206 `77c14ecc` | "seeds should be planted 1 inch deep in slightly raised hills, using four to five seeds per mound." | pumpkins | char 96224 |
| 46 | umn_pk `fbdd6554` | "forming raised beds will ensure good drainage, which these crops require." | pumpkins and winter squash | char 12908 |

**Claim: about a foot across**: NOT STATED: no hashed cited page gives a mound width; C1206 gives height only ('a few inches')

(no hashed sentence bears on it)

**Claim: warm faster (in spring)**: NOT STATED for hills or mounds. WSU says a DRIER soil (in its raised-bed passage) warms sooner; UMN says vine crops need warm soil

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 47 | wsu `7378f653` | "a drier soil warms sooner and stays warmer longer, allowing for earlier spring planting and later fall production." | general, raised-bed passage | p. 17, char 31535 |
| 48 | umn_pk `fbdd6554` | "starting seeds and transplanting direct seeding you can seed vine crops directly into the garden, but they need warm soils (65 degrees fahrenheit at 2 inches soil depth) to germinate properly." | pumpkins and winter squash | char 13332 |
| 49 | wsu `7378f653` | "black plastic mulch absorbs heat and warms the soil in the spring and summer, creat- ing a better environment early in the season for warm-season crops such as melons, tomatoes, and peppers." | general (black plastic, not mounds) | p. 24, char 49579 |

**Claim: drain better**: STATED (C1206 mound -> drainage; UMN raised beds -> drainage)

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 50 | c1206 `77c14ecc` | "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage." | pumpkins | char 95326 |
| 51 | umn_pk `fbdd6554` | "forming raised beds will ensure good drainage, which these crops require." | pumpkins and winter squash | char 12908 |

**Claim: give the vines / plants a (clear) starting point**: NOT STATED; pages speak of sprawl and space only

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 52 | c1206 `77c14ecc` | "while pumpkins are not very difficult to grow, they do require a substantial amount of space for their sprawling vines." | pumpkins | char 2735 |

**Claim: SPACING. pumpkin: hills at least 8 ft apart on all sides, closer for bush and miniature. butternut / spaghetti / vining acorn: 24-36 in in the row, 5-6 ft between rows, closer for bush. acorn bush and semi-bush: about 18-24 in**: pumpkin 8 ft STATED (C1206); 24-36 in x 5-6 ft STATED (UMN, pumpkin AND winter squash); closer for bush STATED (UMN); 'miniature' NOT STATED; acorn bush 18-24 in NOT STATED. Table rows below for comparison

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 53 | c1206 `77c14ecc` | "plant pumpkins in hills, with at least 8 feet of space on all sides." | pumpkins | char 95257 |
| 54 | umn_pk `fbdd6554` | "plant pumpkin and winter squash seeds three-fourths of an inch deep, 24 to 36 inches apart." | pumpkins and winter squash | char 13588 |
| 55 | umn_pk `fbdd6554` | "use the closer spacing if the variety is a bush type." | pumpkins and winter squash | char 13680 |
| 56 | umn_pk `fbdd6554` | "spacing between rows should be 5 to 6 feet." | pumpkins and winter squash | char 13734 |
| 57 | c1206 `77c14ecc` | "spacing rows per plants 72 by 48 in." | pumpkins (C1206 cultivar table) | char 98889 |
| 58 | wsu `7378f653` | "squash, winter 1-11⁄2 24-36 72" | table 4: depth, between plants (in), between rows (in) | p. 11, char 21283 |
| 59 | wsu `7378f653` | "pumpkin 1-11⁄2 36 72" | table 4: depth, between plants (in), between rows (in) | p. 11, char 20901 |
| 60 | uf `7ff585e6` | "pumpkin early july mid july early aug 30 2-4 80-100 (70-90) 36-60 60" | table 1: ..., spacing (in) plants, rows | char 22878 |
| 61 | vt `52fda56c` | "squash, winter 2-4 ft 3-10 ft" | table 5: between plants in row, between rows | char 21109 |
| 62 | vt `52fda56c` | "pumpkin 2-4' 5-8'" | table 5: between plants in row, between rows | char 20817 |
| 63 | osu `f2fdb1d6` | "squash (winter) 4 weeks may may may april 15-may 2-4 plants 72" 48"" | chart: ..., between rows, apart in the row | p. 1, char 3919 |
| 64 | osu `f2fdb1d6` | "pumpkins 4 weeks may may june april 15-june 1-3 plants 72" 48"" | chart: ..., between rows, apart in the row | p. 1, char 3444 |

**Claim: vine run: pumpkin 10-20 ft; butternut 8-12 ft; acorn 4-8 ft; spaghetti 6-8 ft**: NOT STATED as figures; C1206 says some pumpkin varieties spread beyond 8 ft

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 65 | c1206 `77c14ecc` | "keep in mind that some varieties will spread out even further than 8 feet." | pumpkins | char 95450 |

**Claim: on heavy or wet ground build the mounds up for drainage to head off crown and (pumpkin: Phytophthora) fruit rot**: PARTIAL: mounds/raised beds for drainage STATED; crown rot, fruit rot and Phytophthora are named on NO hashed page cited on these crops

| # | page | verbatim (norm_text) | scope | location |
| -- | -- | -- | -- | -- |
| 66 | c1206 `77c14ecc` | "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage." | pumpkins | char 95326 |
| 67 | umn_pk `fbdd6554` | "forming raised beds will ensure good drainage, which these crops require." | pumpkins and winter squash | char 12908 |

## Headlines

* **Eggplant rotation is CONTRADICTED** by its own source: Clemson says rotate WITH cucurbits; the leaf says away from them.
* **No hashed page cited on the peppers names Phytophthora**; the peppers' Phytophthora source (NCSU pepper-diseases) is an unhashed index page.
* 'beds or hills', 'low spots', 'mulch to limit splash', 'keep fruit off saturated soil' (all 3 leaves) and '3-4 years' (peppers) are on no hashed cited page.
* Squash: 'about a foot across', 'warm faster' (for mounds), 'a starting point', 'several inches' of compost, 'hungry', the vine-run figures, acorn bush 18-24 in, and crown / fruit rot / Phytophthora are on no hashed cited page; hills/mounds, drainage, full sun, compost/manure, 90-120 days and the 8 ft / 24-36 in x 5-6 ft spacings are (C1206, UMN).