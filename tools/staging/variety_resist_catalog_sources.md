# Variety-resistance pilot: new `control_methods` T1 provenance

Per-method sourcing for the 13 NEW catalog entries in `variety_resist_catalog_content.json`.
All claims trace to a real, fetched Tier-1 extension page (verified `2026-07-23`). Existing catalog
methods referenced by the ladder skeleton keep their own pre-existing sources and are not restated here.

## Source-catalog status
- **All cited source ids are already catalogued and T1** except two additions needed for the
  Task 9 build:
  - **`ohio_state_ext`** -- Ohio State University Extension (Ohioline), T1. Needed to anchor
    `straw_mulch` to the OSU Ohioline Botrytis factsheet (the only fetched page that names *straw*
    mulch specifically; `osu_ext` in the catalog is *Oregon* State, a different institution, so it
    cannot be reused). URL: https://ohioline.osu.edu/factsheet/plpath-fru-36
  - **`ucanr_ext_woolly_apple_aphid`** -- UC IPM home Woolly Apple Aphid, a page sub-id under the
    already-catalogued T1 parent `ucanr_ext` (tier inherited, per the `umn_ext_broccoli` precedent).
    Added by the fidelity-review IMPORTANT fix to give `horticultural_oil`'s aphid claims an in-object
    anchor distinct from the pn7405 spider-mite page. URL:
    https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/PESTS/woolyapaph.html
- Reused catalogued ids: `ucanr_ext` (UC ANR / UC IPM), `ext_org_apples` (apples.extension.org),
  `psu_ext` (Penn State Extension), `ncsu_ext` (NC State Extension), `umn_ext` (UMN Extension --
  fidelity-review CRITICAL fix, anchors `fruit_bagging`'s apple-maggot claim), `msu_ext` (MSU
  Extension -- fidelity-review CRITICAL fix, anchors `swd_exclusion_netting`'s mesh-size + sealing
  claims).

---

## fruit_bagging (physical)
- **Source (codling moth):** `ucanr_ext` -- UC IPM Pest Notes 7412, Codling Moth. https://ipm.ucanr.edu/PMG/PESTNOTES/pn7412.html
- **Source (apple maggot):** `umn_ext` -- UMN Extension, Apple maggot. https://extension.umn.edu/yard-and-garden-insects/apple-maggot
- pro "excellent, spray-free control ... effective enough to use on its own" <- "Excellent control can be achieved by enclosing young fruit in bags"; "the only nonchemical control method that is effective enough to be used alone and in higher population situations."
- how/best_use timing (4-6 weeks after bloom, 1/2 to 1 inch, one fruit per cluster, slit + staple) <- pn7412 bagging instructions.
- con "very time consuming" <- "quite time consuming"; con "red varieties may not color up ... short-stemmed varieties are hard to bag" <- "Red varieties won't develop full color" and Gravenstein's "very short stems" make bagging difficult.
- Excludes apple maggot as well as codling moth: NOW ANCHORED to the fetched UMN Extension apple maggot page (verified 2026-07-23), which describes enclosing each apple in a bag and states "the apples are protected from apple maggots for the rest of the season." (Fidelity-review CRITICAL fix: pn7412 does not mention apple maggot; umn_ext supplies the in-object apple-maggot anchor, so the claim is kept.)

## kaolin_clay (physical)
- **Source:** `ext_org_apples` -- Apples/Cooperative Extension, "Can kaolin clay sprays reduce insect damage to apple fruit?" https://apples.extension.org/can-kaolin-clay-sprays-reduce-insect-damage-to-apple-fruit/
- how_it_works "dry white film ... particles agitate and repel ... masks the host" <- "a dry white film layer of interlocking microscopic particles"; repellent + "unsuitable for feeding/egg-laying" + color masking.
- pro "strong control of apple maggot" <- "Strong control: Apple maggot, white apple leafhopper, and pear psylla."
- con "only fair to moderate on plum curculio and codling moth" <- "Fair to moderate control: plum curculio and several species of fruit pest caterpillars (codling moth ...)."
- con "chalky white residue that must be washed off" <- "kaolin clay powdery film left on the fruit at harvest ... requiring washing before sale."
- caution "heavy use can harm beneficials ... flare-up of European red mites or San Jose scale" <- "heavy use is harmful to beneficial species, and can lead to a flare up of European red mites or San Jose scale."
- pro "physical film barrier and repellent rather than a nerve poison" <- physical-barrier / repellent mechanism as described (no neurotoxic mode).

## codling_moth_pheromone_trap (physical)
- **Source:** `ucanr_ext` -- UC IPM Pest Notes 7412. https://ipm.ucanr.edu/PMG/PESTNOTES/pn7412.html
- how/best_use "monitoring flight to time treatments"; hung mid- to late March, checked every few days <- "Codling moth pheromone traps are important for monitoring flight activity of moths to help time insecticide treatments."
- con "mainly a monitoring tool: hanging traps is not a reliable way to reduce damage by itself" <- "Hanging traps ... might help to reduce codling moth populations on isolated trees but isn't a reliable way to reduce damage."

## red_sphere_trap (physical)
- **Source:** `psu_ext` -- Penn State Extension, "Apple Maggot in the Home Fruit Planting." https://extension.psu.edu/apple-maggot-in-the-home-fruit-planting
- how_it_works "red sphere baited with an apple volatile mimics fruit, catches egg-laying females on glue" <- page's trap description.
- pro/best_use "trap-out at ~1 per 100 to 150 fruit from mid-June can serve as a control measure in small plantings" <- "Baited red spheres hung at a rate of 1 per 100 to 150 fruit are used to trap out females ..."; "can serve as a control measure for apple maggots in small plantings"; deploy "in mid-June."
- con "must be serviced through the season" <- monitoring guidance ("monitored twice a week").
- Fidelity-review MINOR fix: how_it_works_seasoned and find_it_beginner reworded from "increase spheres with tree size" / "the number the label suggests for your tree size" to the source's actual fruit-count rate ("one per 100 to 150 fruit"), since the page gives a fruit-count basis, not tree-size guidance.

## horticultural_oil (soft_chemical)
- **Source:** `ucanr_ext` -- UC IPM Pest Notes 7405, Spider Mites (anchor). https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html
- how/pro "smothers soft-bodied insects and mites on contact; coverage essential" <- "insecticidal soap or insecticidal oil" incl. "petroleum-based horticultural oils"; "Oils and soaps must contact mites to kill them, so excellent coverage, especially on the undersides of leaves, is essential."
- caution ">90°F / stressed plants" <- "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F."
- caution "no sulfur within 30 days of an oil spray" <- "don't apply sulfur within 30 days of an oil spray."
- **Source (aphids), NOW an in-object anchor:** `ucanr_ext_woolly_apple_aphid` (sub-id under `ucanr_ext`, T1 inherited) -- UC IPM home Woolly Apple Aphid, https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/PESTS/woolyapaph.html -- fetched + verified 2026-07-23: "During the growing season horticultural oil or insecticidal soap can be sprayed to thoroughly cover infested plant parts. These sprays can provide partial control." Anchors the soft-bodied-insect / aphid / "partial control" claims (applies_to insect_soft_bodied, best_use "aphids", how_it_works_seasoned "partial control of aphids such as woolly apple aphid", pro "soft-bodied insects and spider mites"). (Fidelity-review IMPORTANT fix: the aphid rationale previously rested only on pn7405, the spider-mite page, which never mentions aphids; woolyapaph.html is now listed on the method so every claim carries an in-object anchor.)
- NOTE: I deliberately did NOT claim dormant-season / overwintering-egg control, because none of the pages I fetched stated it in verifiable wording. (This is why the separate `dormant_oil` candidate was dropped -- see report.)

## prune_out_infection (physical)
- **Source:** `ucanr_ext` -- UC IPM Pest Notes 7414, Fire Blight. https://ipm.ucanr.edu/PMG/PESTNOTES/pn7414.html
- how/pro "cut 6 to 8 inches beyond the infection into healthy wood" <- "Remove 6 to 8 inches more beyond the infection."
- how "summer or winter when bacteria are not moving; cut advancing spring strikes on susceptible trees at once" <- "Prune in summer or winter when the bacteria no longer are spreading"; "rapidly advancing infections should be removed as soon as they appear in spring."
- pro "no spray cures wood infection; must be pruned out" <- "Sprays prevent new infections but won't eliminate wood infections; these must be pruned out."
- caution "10% bleach dip is wise but cut location matters more" <- "Dipping shears in 10% bleach between cuts might be wise," though "the location of the cut is far more important than the cleansing of tools."

## slug_traps_barriers (physical)
- **Source:** `ucanr_ext` -- UC IPM Pest Notes 7427, Snails and Slugs. https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html
- pro "handpicking done thoroughly and regularly can be very effective" <- "Hand-picking can be very effective if done thoroughly on a regular basis ... daily ... then weekly."
- how/pro "board and beer traps; copper foil/tape at least 2 inches repels until tarnished" <- board traps on 1-inch runners scraped daily; beer traps replenished "every few days"; "Copper foil or tape ... at least 2 inches tall ... will repel snails until it becomes tarnished."
- con "traps must be emptied/refreshed every few days" and "copper stops working once tarnished" <- same passages.

## iron_phosphate_slug_bait (soft_chemical)
- **Source:** `ucanr_ext` -- UC IPM Pest Notes 7427. https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html
- pro "safer around children, pets, birds, fish, and other wildlife than metaldehyde" <- iron phosphate baits "have the advantage of being safer for use around children, domestic animals, birds, fish, and other wildlife"; metaldehyde "particularly poisonous to dogs and cats."
- pro/how "stop feeding after eating even a small amount; death takes several days to a week" <- "Ingesting even small amounts of the bait will cause snails and slugs to stop feeding, although it can take several days to a week for the snails to die."
- con "baits alone do not give lasting control without habitat reduction" <- page frames baits as part of an IPM program, not a stand-alone; caution "still a pesticide, scatter on soil, follow label" = honest label-restraint (organic-isn't-automatically-harmless).

## swd_exclusion_netting (physical)
- **Source:** `ucanr_ext` -- UC IPM Home & Landscape, Spotted-Wing Drosophila. https://ipm.ucanr.edu/home-and-landscape/spotted-wing-drosophila/
- **Source (mesh size + sealing):** `msu_ext` -- MSU Extension, "Spotted wing Drosophila: A serious pest for the home gardener." https://www.canr.msu.edu/news/spotted_wing_drosophila_a_serious_pest_for_the_home_gardener -- fetched + verified 2026-07-23: "netting with 1-millimeter (0.03125 inch) mesh can be employed to help protect fruits from SWD. To be effective, the netting must completely cover the plants and be sealed to the surface of the ground."
- how/pro "fine ~0.98 to 1 mm mesh (no-see-um grade) excludes adult SWD" <- ucanr "0.98 mm mesh used for screening out no-see-um flies" + msu "1-millimeter ... mesh."
- con "must be on before fruit ripens" <- "netting must be applied before fruit begins to ripen so that flies will not be caught inside."
- how/con "must completely cover the planting and be sealed at every edge, down to the ground" <- ucanr "Netting must be secured so flies cannot enter" + msu "must completely cover the plants and be sealed to the surface of the ground."
- Fidelity-review CRITICAL fix: the original "drape it so it does not touch the fruit, since flies can lay through mesh pressed against a berry" / con "the net must be held off the fruit" clause was NOT on the cited UC IPM page. It was also absent from the fetched UMN (extension.umn.edu/yard-and-garden-insects/spotted-wing-drosophila) and MSU home-gardener pages. No fetched T1 page states the keep-net-off-fruit / lay-through-contact detail in verifiable wording, so the specific clause was DROPPED; the retained mesh-size, before-ripening, and complete-cover/edge-seal claims are all anchored to ucanr + msu.

## swd_monitoring_traps (physical)
- **Source:** `ucanr_ext` -- UC IPM Home & Landscape, Spotted-Wing Drosophila. https://ipm.ucanr.edu/home-and-landscape/spotted-wing-drosophila/
- how/find_it "1 to 2 inches of pure apple cider vinegar + a drop of unscented dish soap" <- "1 to 2 inches of pure apple cider vinegar; avoid flavored ... Add a drop of unscented liquid dishwashing soap to break the surface tension."
- how "hang in shade in early May / before fruit ripens; check weekly for dark-wing-spot flies" <- "Hang the trap in the shade ... in early May or well before fruit begins to ripen"; "Check the trap weekly ..."
- con "monitoring tool, not a control" <- the page frames traps as monitoring; control is by sanitation/exclusion/insecticide.

## bird_netting (physical, vertebrate)
- **Source:** `ucanr_ext` -- UC IPM, Birds on Tree Fruits and Vines (Pest Notes PDF). https://ipm.ucanr.edu/pdf/pestnotes/pnbirdstreefruitsvines.pdf
- how/pro "netting on a PVC/hoop frame excludes birds; extend to ground and tie ends" <- "PVC structures covered with netting can save your crop"; "extend netting to the ground and tie off all ends to stop birds from entering underneath."
- con "netting laid directly on the plant still lets birds reach fruit through it" <- "if netting is placed directly on the tree, birds will still be able to reach much of the fruit."

## bird_scare_deterrents (physical, vertebrate)
- **Source:** `ucanr_ext` -- UC IPM, Birds on Tree Fruits and Vines (Pest Notes PDF). https://ipm.ucanr.edu/pdf/pestnotes/pnbirdstreefruitsvines.pdf
- how/pro "mylar streamers, scare-eye balloons, noisemakers frighten some species" <- "a combination of noisemakers and visual repellents such as mylar streamers and 'scare-eye' balloons."
- con "effectiveness varies by species and birds habituate" <- "effectiveness varies by species ... less effective for others (e.g., house finches, house sparrows, robins, scrub-jays)."
- con "rotate/move at least weekly or birds ignore them" <- "rotate from one type ... to another and do not use one combination ... for more than a week; otherwise, birds will become used to it."

## straw_mulch (cultural)
- **Anchor:** `ohio_state_ext` -- OSU Ohioline PLPATH-FRU-36, Botrytis Fruit Rot "Gray Mold." https://ohioline.osu.edu/factsheet/plpath-fru-36
  - pro "keeps fruit off wet soil, aids greatly in controlling fruit rots" <- "A good layer of straw mulch (or other material) ... aids greatly in controlling fruit rots. The mulch acts as a barrier that reduces fruit contact with the soil."
  - best_use "emphasize cultural practices" <- "Homeowners are encouraged to emphasize the use of cultural practices in order to avoid the use of fungicides."
  - con "needs spacing/airflow" <- weed control / air movement passage.
- **Support:** `ncsu_ext` -- NC State Extension, Gray Mold / Botrytis Rot of Strawberry. https://content.ces.ncsu.edu/gray-mold-or-botrytis-rot-of-strawberry
  - pro "reduces rain splash and soil contact" <- "mulch helps keep down rain splash, plant and soil-surface contact." (NCSU names *plastic* mulch; the rain-splash/soil-contact benefit is the general-mulch mechanism straw shares -- the straw-specific barrier claim is anchored to Ohioline above.)
  - con "restrained nitrogen; dense damp canopy still rots" <- "excess nitrogen has been shown to increase fruit rot"; spacing "will improve airflow."

---

## Honesty notes carried into the skeleton (for the ladder authors)
- **Woolly apple aphid has NO conventional rung.** UC IPM: "Outbreaks of woolly apple aphid are most
  common following the use of pyrethroids, which destroys its natural enemies"
  (https://ipm.ucanr.edu/agriculture/apple/woolly-apple-aphid/) and the home page: it "can be
  completely controlled by ... _Aphelinus mali_ ... if broad-spectrum insecticide is not applied."
  A pyrethroid/carbaryl rescue rung would be actively harmful, so the ladder honestly bottoms out at
  soft_chemical (oil/soap = "partial control").
- **Fire blight, red-stele, verticillium, birds** bottom out with no home chemical cure
  (fire blight: pn7414 "these must be pruned out"; birds: netting/scares only). These are honest
  short/cultural-or-physical-only ladders.
- **Gray mold** is a cultural-only ladder (Ohioline: homeowners emphasize cultural practices).
