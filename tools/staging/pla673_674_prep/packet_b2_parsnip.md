# PLA-673 B2: parsnip's three hilling leaves (seasoned)

Read-only on canonical `3ccc25f1`. Every claim in `diseases[0].prevention_seasoned`, `failure_diagnostics[3].next_season_tip_seasoned` and `growth_stages[2].user_action_seasoned` (no citation block today), from ALL hashed pages cited on parsnip plus the UMass canker factsheet (cited on parsnip, hashed into MANIFEST for this packet). **Nothing authored.**

## Pages

| key | page | sha256 |
| -- | -- | -- |
| umass | UMass Carrot & Parsnip, Itersonilia Canker (2013) [umass_ext_itersonilia_canker, PROPOSED mint]: https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/carrot-parsnip-itersonilia-canker | `e1f62141e5dc10fed18d714b510e8ea66787f9b587bd1ee7a3b87f79c2cedee6` |
| umn_cp | UMN Growing carrots and parsnips [umn_ext]: https://extension.umn.edu/vegetables/growing-carrots-and-parsnips | `14d9f7109dab4994e6818b4a0bc62bbdd853a76a47174bf35bedae019dbc287b` |
| clem_root | Clemson HGIC Carrot, Beet, Radish & Parsnip [clemson_hgic]: https://hgic.clemson.edu/factsheet/carrot-beet-radish-parsnip/ | `a02e152b4acee1a0d4c2b88aab076eb10feb2e2bb4eb6776e0488554b25df35b` |
| rhs | RHS Parsnips: grow your own [rhs]: https://www.rhs.org.uk/vegetables/parsnips/grow-your-own | `c9871301eaa660266923912bffe86785d0f73c859d9718ee270231bdc594069b` |

## The leaves today

* `diseases[0].prevention_seasoned`: Choose resistant varieties (Avonresister, Cobham Improved Marrow), rotate out of the carrot family for two to three years, hill soil over the shoulders through the season, control carrot rust fly, avoid waterlogged beds, harvest before very late in cold wet spells, and bury old parsnip residue by deep cultivation to lower inoculum. (UMass)
* `failure_diagnostics[3].next_season_tip_seasoned`: Choose resistant varieties (Avonresister, Cobham Improved Marrow), rotate out of the carrot family for three years, hill soil over the shoulders through the season, control carrot rust fly, avoid overly wet beds, and bury old parsnip residue. Fungicides do not control root cankers. (UMass)
* `growth_stages[2].user_action_seasoned`: Maintain even moisture, about 1 inch per week, to prevent cracking, and hill a little soil or mulch over the shoulders to suppress canker and greening. Feeding is rarely needed. Wear gloves and long sleeves when working among the foliage in bright sun, since parsnip sap can cause a skin rash.

## Claims

| # | leaf | claim | verdict | page | verbatim (norm_text) | location |
| -- | -- | -- | -- | -- | -- | -- |
| 1 | diseases[0].prevention_seasoned + failure_diagnostics[3].next_season_tip_seasoned | choose resistant varieties | STATED | umass `e1f62141` | "select and plant resistant cultivars." | char 5182 |
| 2 | diseases[0].prevention_seasoned + failure_diagnostics[3].next_season_tip_seasoned | choose resistant varieties | STATED | rhs `c9871301` (RHS variety rows ('Albion', 'Gladiator', 'Picador')) | "resistant to canker." | char 29470 |
| 3 | same | named: Avonresister, Cobham Improved Marrow | NOT STATED on any hashed cited page (RHS names Albion, Gladiator, Picador) | -- | (no hashed sentence) | -- |
| 4 | same | rotate out of the carrot family for two to three years (fd[3]: three years) | PARTIAL: rotation to NON-HOSTS STATED; hosts include carrot, coriander, parsley (carrot family) and chrysanthemum, aster, sunflower; NO year count | umass `e1f62141` | "rotate parsnip with non-host crops." | char 5220 |
| 5 | same | rotate out of the carrot family for two to three years (fd[3]: three years) | PARTIAL: rotation to NON-HOSTS STATED; hosts include carrot, coriander, parsley (carrot family) and chrysanthemum, aster, sunflower; NO year count | umass `e1f62141` | "the pathogen also affects carrot, coriander, parsley, chrysanthemum, aster, sunflower and wild plants." | char 4117 |
| 6 | same | hill soil over the shoulders through the season | STATED | umass `e1f62141` | "cover the shoulder of parsnips with soil throughout the growing season." | char 5389 |
| 7 | same | control carrot rust fly | STATED | umass `e1f62141` | "control carrot rust fly as larvae can predispose roots to infection." | char 5256 |
| 8 | same | avoid waterlogged / overly wet beds | PARTIAL: cool, wet WEATHER favors it; waterlogged beds not worded. Clemson: parsnips need well-drained soil | umass `e1f62141` | "disease development is enhanced by cool, wet weather." | char 5096 |
| 9 | same | avoid waterlogged / overly wet beds | PARTIAL: cool, wet WEATHER favors it; waterlogged beds not worded. Clemson: parsnips need well-drained soil | clem_root `a02e152b` (parsnip paragraph) | "similar to carrots, they need a loose, well-drained soil, and weeds should be controlled." | char 80517 |
| 10 | diseases[0] only | harvest before very late in cold wet spells | PARTIAL: 'especially in late harvested crops' STATED; 'cold wet spells' timing not worded | umass `e1f62141` | "itersonilia canker of parsnip can be a serious disease, especially in late harvested crops." | char 4025 |
| 11 | diseases[0] only | harvest before very late in cold wet spells | PARTIAL: 'especially in late harvested crops' STATED; 'cold wet spells' timing not worded | umass `e1f62141` | "disease development is enhanced by cool, wet weather." | char 5096 |
| 12 | same | bury old parsnip residue by deep cultivation to lower inoculum | STATED | umass `e1f62141` | "reduce soilborne inoculum by deep plowing to enhance decomposition of parsnip residue." | char 5461 |
| 13 | failure_diagnostics[3] only | fungicides do not control root cankers | STATED | umass `e1f62141` | "fungicide sprays are not effective for control of root cankers." | char 5325 |
| 14 | growth_stages[2].user_action_seasoned | maintain even moisture to prevent cracking | STATED (RHS: evenly moist to avoid splitting; UMN: drought splits roots) | rhs `c9871301` | "more mature plants are fairly drought tolerant, but to avoid the roots splitting , keep the soil evenly moist." | char 37210 |
| 15 | growth_stages[2].user_action_seasoned | maintain even moisture to prevent cracking | STATED (RHS: evenly moist to avoid splitting; UMN: drought splits roots) | umn_cp `14d9f710` | "a drought can also cause split roots." | char 17203 |
| 16 | growth_stages[2] | about 1 inch per week | NOT STATED on any hashed page cited on parsnip | -- | (no hashed sentence) | -- |
| 17 | growth_stages[2] | hill a little soil or mulch over the shoulders to suppress canker | STATED for SOIL (UMass); 'or mulch' NOT STATED | umass `e1f62141` | "cover the shoulder of parsnips with soil throughout the growing season." | char 5389 |
| 18 | growth_stages[2] | ... and greening | NOT STATED for parsnip: UMN's greening sentence is about carrot varieties that push up | umn_cp `14d9f710` (carrots) | "some carrot varieties will push the tops of the roots up out of the soil." | char 10216 |
| 19 | growth_stages[2] | ... and greening | NOT STATED for parsnip: UMN's greening sentence is about carrot varieties that push up | umn_cp `14d9f710` (carrots) | "hilling soil around these plants will keep the roots from turning green." | char 10290 |
| 20 | growth_stages[2] | feeding is rarely needed | NOT STATED; Clemson says to sidedress root crops at 4 in. (tension); UMN warns excess nitrogen favors leaves | clem_root `a02e152b` (carrot/beet/radish/parsnip page) | "sidedress fertilize these root crops when plants are 4 inches tall." | char 69911 |
| 21 | growth_stages[2] | feeding is rarely needed | NOT STATED; Clemson says to sidedress root crops at 4 in. (tension); UMN warns excess nitrogen favors leaves | umn_cp `14d9f710` | "excessive nitrogen fertilization can also contribute to lots of leaf growth at the expense of root growth." | char 17354 |
| 22 | growth_stages[2] | wear gloves and long sleeves among the foliage in bright sun; sap can cause a skin rash | STATED (UMN: rash from contact with the LEAVES on bright sunny days; long pants, sleeves, gloves). 'Sap' is not UMN's word | umn_cp `14d9f710` | "some people develop a rash from contact with parsnip leaves, particularly on bright sunny days." | char 17514 |
| 23 | growth_stages[2] | wear gloves and long sleeves among the foliage in bright sun; sap can cause a skin rash | STATED (UMN: rash from contact with the LEAVES on bright sunny days; long pants, sleeves, gloves). 'Sap' is not UMN's word | umn_cp `14d9f710` | "wear long pants, long sleeves and gloves when weeding or harvesting parsnips." | char 17610 |

## Headlines

* Hilling (soil over the shoulders) is STATED by UMass for canker. 'Or mulch' and 'greening' (a carrot sentence) are not.
* NOT STATED: Avonresister / Cobham Improved Marrow (RHS names Albion, Gladiator, Picador), any rotation year count, 1 inch per week, 'feeding rarely needed' (Clemson says sidedress root crops at 4 in.).
* The other hashed pages cited on parsnip (OSU chart, WSU) state none of these claims for parsnip.