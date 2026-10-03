"""PLA-10 promote 3 session 2: every height restatement on a moving crop, adjudicated. Two populations:
(1) the promote's scanner hits (P.height_strings: a distance + a height word, + a width word when a spread is
authored), which guard S requires; (2) leaves a wider sweep found that the scanner cannot see (a height with no
height word in its sentence: "reaches 3 to 5 feet", "2 to 4 foot stems", "a 3-to-6-foot clump"), adjudicated
too, because an unadjudicated contradiction is the defect either way. EDITS: (old substring, new substring,
reason); the builder applies the replacement to the base leaf, refusing unless the substring occurs exactly once."""

A = "agrees"
POT = "Not a plant-height restatement: a container depth / pot size beside a 'tall' or 'deep' word."
SPACING = "Not a plant-height restatement: a spacing / thinning distance."
STAGE = "A stage or harvest-time height (seedling, cutting, hilling), not the mature height: agrees."
VARIETY = "A variety- or type-level figure, not the crop-level range; the authored range is the crop's: agrees."

RESTATE = {
 "brussels-sprouts": {
  "container_notes.shape_requirements_beginner": (A, POT),
  "container_notes.shape_requirements_seasoned": (A, POT),
  "tips_by_stage.seedling[0].text_beginner": (A, SPACING),
 },
 "broad-beans-fava": {p: (A, "D-FAVA TAKEN: '2 to 4 feet' (and 'some to 5 or 6') sits inside the cited [2,6] and "
                             "does not contradict it: agrees, no edit.")
                      for p in ("container_notes.notes_beginner", "container_notes.notes_seasoned",
                                "description_beginner", "description_seasoned",
                                "growth_stages[2].what_to_look_for_seasoned", "tips_by_stage.vegetative[0].text_seasoned",
                                "varieties.note_seasoned", "growth_stages[2].what_to_look_for_beginner")},
 "dill": {
  "container_notes.notes_beginner": (A, POT),
  "container_notes.shape_requirements_beginner": (A, POT),
  "container_notes.shape_requirements_seasoned": (A, POT),
  "description_beginner": ("edited", "H3 TAKEN: the uncited '3 to 5 feet' exceeds UW's cited 4 ft; edited to the cited figure."),
  "description_seasoned": ("edited", "H3 TAKEN: the uncited '3 to 5 feet' exceeds UW's cited 4 ft; edited to the cited figure."),
  "container_notes.notes_seasoned": ("edited", "H3 TAKEN (scanner-invisible leaf: no height word): 'Standard dill reaches "
                                               "3 to 5 feet' edited to the cited figure."),
  "varieties.recommended[1].note": ("edited", "H3 TAKEN: the Long Island Mammoth note's '3 to 5 feet' edited to the cited figure."),
  "growth_stages[2].what_to_look_for_seasoned": (A, STAGE),
  "harvest_ready_beginner": (A, STAGE),
  "harvest_ready_seasoned": (A, STAGE),
  "varieties.recommended[0].note": (A, "'reaches about 2 to 3 feet' sits inside [1.5,4]: agrees."),
 },
 "edamame": {
  "growth_stages[2].what_to_look_for_beginner": ("edited", "BELOW THE FLOOR ('two to three feet' vs the point [3,3]; ISU "
                                                 "'approximately 3 feet tall'): the H3 pattern, edited to the cited figure. "
                                                 "Scanner-invisible (word numbers, PLA-655 class); found by the session-3 review."),
  "growth_stages[2].what_to_look_for_seasoned": ("edited", "BELOW THE FLOOR ('its full two to three feet' vs [3,3]): the H3 "
                                                 "pattern, edited to the cited figure. Scanner-invisible (PLA-655 class)."),
 },
 "green-beans-bush": {
  "growth_stages[2].what_to_look_for_beginner": ("edited", "BELOW THE FLOOR ('one to two feet' vs the point [2,2]; UMN "
                                                 "'growing about two feet tall'): the H3 pattern, edited to the cited "
                                                 "figure. Scanner-invisible (word numbers, PLA-655 class); found by the "
                                                 "session-3 review."),
  "growth_stages[2].what_to_look_for_seasoned": ("edited", "BELOW THE FLOOR ('one-to-two-foot height' vs [2,2]): the H3 "
                                                 "pattern, edited to the cited figure. Scanner-invisible (PLA-655 class)."),
 },
 "eggplant": {"growth_stages[5].what_to_look_for_seasoned": (A, "A fruit size (2 inches across), not the plant: agrees.")},
 "cosmos": {
  "deadheading_beginner": (A, "A cut-back height (12 to 18 inches), not the mature height: agrees."),
  "deadheading_seasoned": (A, "A cut-back height (12 to 18 in), not the mature height: agrees."),
  "tips_by_stage.flowering[1].text_beginner": (A, "A cut-back height, not the mature height: agrees."),
  "tips_by_stage.flowering[1].text_seasoned": (A, "A cut-back height, not the mature height: agrees."),
  "varieties.recommended[0]": (A, "Sensation 3 to 4 ft sits inside UF's [3,6]: agrees."),
  "description_seasoned": (A, "'Garden cosmos (C. bipinnatus) reaches roughly 3 to 6 ft' is UF's figure exactly; the "
                              "same leaf's 'C. sulphureus ... 1 to 3 ft' is BELOW the floor but type-level and stated by "
                              "the authoring page itself ('orange cosmos ... is shorter, usually between 1-3 feet tall'): "
                              "agrees (session-3 review corrected this note)."),
 },
 "beefsteak-tomato": {
  "container_notes.shape_requirements_beginner": (A, POT),
  "description_beginner": (A, "'5 to 6 feet tall' sits at Cornell's high end: agrees (worklist row 13)."),
  "det_indet.detail_beginner": (A, "ABOVE THE CEILING ('6 feet tall or more' vs [2,6]), SUPPORTED: Cornell's hashed "
                                   "clause 'staked and pruned plants can grow to well over 6 feet tall' (restatement-support "
                                   "row): agrees."),
  "det_indet.detail_seasoned": (A, "ABOVE THE CEILING ('Can reach 6-8 feet' vs [2,6]), SUPPORTED: OSU EC1333 on "
                                   "indeterminate plants 'they can easily grow 7 to 8 feet high' and Cornell's 'well over "
                                   "6 feet tall' clause (restatement-support rows): agrees."),
  "companions.note_seasoned": (A, "'6-foot cages' is a support size, and the spacing is a spacing: agrees."),
 },
 "heirloom-tomato": {
  "container_notes.shape_requirements_beginner": (A, POT),
  "description_beginner": (A, "ABOVE THE CEILING ('5 to 6 feet tall or more' vs [2,6]), SUPPORTED: Cornell's hashed "
                              "'well over 6 feet tall' clause (restatement-support row): agrees."),
  "det_indet.detail_beginner": (A, "ABOVE THE CEILING ('6 feet or more' vs [2,6]), SUPPORTED: Cornell's hashed 'well over "
                                   "6 feet tall' clause (restatement-support row): agrees."),
  "det_indet.detail_seasoned": (A, "ABOVE THE CEILING ('6 to 8 feet' vs [2,6]), SUPPORTED: OSU EC1333 'they can easily "
                                   "grow 7 to 8 feet high' (indeterminate) and Cornell's 'well over 6 feet tall' clause "
                                   "(restatement-support rows): agrees."),
  "companions.note_seasoned": (A, "'6-foot cages' is a support size, and the spacing is a spacing: agrees."),
 },
 "roma-tomato": {
  "det_indet.detail_beginner": (A, "'about 3 to 4 feet' is OSU EC1333's determinate figure exactly: agrees."),
  "det_indet.detail_seasoned": (A, "'typically 3 to 4 feet' is OSU EC1333's determinate figure exactly: agrees."),
 },
 "tomatillo": {
  "description_seasoned": (A, "'3 to 4 feet tall and wide' is the cited figure: agrees."),
  "description_beginner": (A, "'3 to 4 feet across' is the cited spread: agrees."),
  "growth_stages[2].user_action_beginner": (A, "'sprawl to 3 to 4 feet' is the cited figure: agrees."),
  "growth_stages[2].user_action_seasoned": (A, "'reach 3 to 4 ft' is the cited figure: agrees."),
  "tips_by_stage.established[0].text_beginner": (A, "'sprawl to 3 to 4 feet' is the cited figure: agrees."),
  "tips_by_stage.established[0].text_seasoned": (A, "'sprawl to 3 to 4 feet' is the cited figure: agrees."),
 },
 "potato": {p: (A, "A hilling height (6 to 12 inches), not the mature height: agrees.")
            for p in ("growth_stages[1].user_action_beginner", "growth_stages[1].what_to_look_for_beginner",
                      "notifications[2].body_beginner", "tips_by_stage.vegetative[0].text_beginner")},
 "sweet-potato": {p: (A, "A ridge height (8 to 10 inches), not the plant: agrees.")
                  for p in ("soil_prep_beginner", "soil_prep_seasoned")},
 "onion": {"container_notes.notes_beginner": (A, POT), "container_notes.notes_seasoned": (A, POT)},
 "okra": {
  "container_notes.shape_requirements_seasoned": (A, POT),
  "description_beginner": (A, "'often 4 to 6 feet' sits inside UF's [3,6]: agrees (worklist row 25)."),
  "description_seasoned": ("edited", "ABOVE THE CEILING as a claim ('4 to 6 feet and more' vs [3,6]): UF's 'most fall "
                                     "within the 3-6 foot range' says nothing above 6 ft (session-3 review: the support "
                                     "row did not support 'and more'), so 'and more' is dropped and '4 to 6 feet' kept."),
  "thinning.tip_beginner": (A, SPACING),
  "thinning.tip_seasoned": (A, SPACING),
  "varieties.recommended[0].recommended_note": (A, VARIETY),
  "varieties.recommended[7].recommended_note": ("edited", "ABOVE THE CEILING (Cow Horn '6 to 8 feet' vs [3,6]), NO cited "
                                                          "hashed page states it: the number is dropped and the claim "
                                                          "('tall heirloom') kept."),
  "varieties.recommended[1].recommended_note": (A, VARIETY),
  "varieties.recommended[6].recommended_note": (A, VARIETY),
 },
 "celery": {
  "fertilizer.notes_seasoned": (A, "A row length (10 feet of row), not a height: agrees."),
  **{p: (A, "A harvest-stage stalk height (6 to 8 inches), not the mature height: agrees.")
     for p in ("growth_stages[3].what_to_look_for_beginner", "growth_stages[3].what_to_look_for_seasoned",
               "harvest_ready_beginner", "harvest_ready_seasoned", "notifications[4].body_beginner",
               "notifications[4].body_seasoned")},
 },
 "asparagus": {p: (A, "A spear cutting height (6 to 8 inches), not the fern height: agrees.")
               for p in ("first_harvest_notes_beginner", "growth_stages[1].what_to_look_for_beginner",
                         "harvest_ready_beginner", "tips_by_stage.spear_emergence[0].text_beginner")},
 "leek": {p: (A, "A transplant-seedling height (about 8 inches), not the mature height: agrees.")
          for p in ("growth_stages[1].what_to_look_for_beginner", "growth_stages[1].what_to_look_for_seasoned",
                    "start_method.hardening_off_beginner", "start_method.hardening_off_seasoned",
                    "tips_by_stage.seedling_growth[0].text_beginner", "tips_by_stage.seedling_growth[0].text_seasoned")},
 "cilantro-coriander": {p: (A, STAGE) for p in ("growth_stages[2].what_to_look_for_seasoned", "harvest_ready_beginner",
                                                "harvest_ready_seasoned")},
 "chives": {
  "container_notes.shape_requirements_seasoned": (A, POT),
  "growth_stages[2].what_to_look_for_beginner": (A, STAGE),
  "growth_stages[2].what_to_look_for_seasoned": (A, STAGE),
  "harvest_ready_beginner": (A, STAGE),
  "harvest_ready_seasoned": (A, STAGE),
  "varieties.recommended[0].note": (A, VARIETY + " (worklist section 3 row 7). Session-3 review: this entry is 'the "
                                       "standard Allium schoenoprasum', and its '8 to 14 inches' sits BELOW the 1 ft floor; "
                                       "kept as ruled (section 3 row 7 named the 8-14 in variety prose agrees), raised to "
                                       "Trevor."),
  "varieties.recommended[3].note": (A, "ABOVE THE CEILING (Forescate '18 to 20 inches' vs [1,1.5]), SUPPORTED: UW-Madison "
                                       "''forescate' is larger than the species, growing 18 to 20 inches tall' "
                                       "(restatement-support row): agrees."),
 },
 "mint": {p: (A, "A spray-timing trigger (plants 4 to 6 inches tall), not the mature height: agrees.")
          for p in ("diseases[2].control_ladder[3].note_seasoned", "diseases[2].organic_treatment_seasoned")},
 "lemongrass": {
  "description_seasoned": (A, "'3 to 6 feet tall' is USU's cited figure exactly (section 3 row 8, re-ruled session 3): agrees."),
  "growth_stages[2].what_to_look_for_seasoned": (A, "'3 to 6 feet tall' is USU's cited figure: agrees."),
  "companions.note_seasoned": (A, "'reaches 3 to 6 feet' is USU's cited figure (scanner-invisible leaf): agrees."),
  "tips_by_stage.vegetative[0].text_seasoned": (A, "'3-to-6-foot clump' is USU's cited figure (scanner-invisible leaf): agrees."),
  "regions.northern_tier.region_notes_seasoned": (A, "'3-to-6-foot clump' is USU's cited figure (scanner-invisible leaf): "
                                                     "agrees."),
  "notifications[1].body_beginner": (A, "'room to grow (2 to 3 feet)' is a spacing; it matches the cited spread: agrees."),
 },
 "marigold": {p: (A, SPACING) for p in ("growth_stages[1].user_action_beginner", "tips_by_stage.seedling[0].text_beginner",
                                        "tips_by_stage.seedling[0].text_seasoned")},
 "sunflower": {
  "description_beginner": ("edited", "ABOVE THE CEILING ('giants over 10 feet' vs [1.5,10]), NO cited hashed page states "
                                     "it (NCSU: 'grow 2 to10 feet tall'): edited into range."),
  "description_seasoned": ("edited", "ABOVE THE CEILING ('giants that top 10 feet' vs [1.5,10]), NO cited hashed page "
                                     "states it: edited into range."),
  "varieties.recommended[0]": ("edited", "ABOVE THE CEILING (Mammoth '9 to 12 ft' vs [1.5,10]), NO cited hashed page states "
                                         "it: the number is dropped and the claim ('giant single-stem') kept."),
  "varieties.recommended[1]": ("edited", "ABOVE THE CEILING (Sunzilla / American Giant '12+ ft' vs [1.5,10]), NO cited "
                                         "hashed page states it (scanner-invisible, PLA-655 class; found by the session-3 "
                                         "review): the number is dropped and the claim ('giant single-stem') kept."),
 },
 "borage": {
  "description_seasoned": ("edited", "Section 3 row 11 (adjudicate: agrees at the low end, or edit): EDITED. The height "
                                     "'2 to 3 ft tall' is UC Marin's and stays; the width '1 to 2 ft wide' exceeds NCSU's "
                                     "cited 'width: 1 ft. 0 in. - 1 ft. 4 in.', so it is edited to 12 to 16 in (the H3 "
                                     "pattern: prose above the cited high end is edited)."),
 },
 "zinnia": {
  "description_seasoned": (A, "ABOVE THE CEILING ('cut-flower types reaching 3 to 4 ft' vs [1,3]), SUPPORTED: FP623 "
                              "stops at 3 ft, but Clemson HGIC (cited on the crop, hashed) states zinnias 'range in height "
                              "from 6 inches to 4 feet tall' and Benary's Giant (a cut-flower series) 'plants are 2 to 3 "
                              "feet wide and 3 to 4 feet tall' (restatement-support rows): agrees. The same leaf's "
                              "'dwarf bedding types near 6 in' is BELOW the floor, type-level, and inside Clemson's "
                              "'6 inches to 4 feet' (session-3 review)."),
 },
 "chamomile": {
  "description_beginner": (A, "'grows about 2 ft tall' is the cited high end: agrees."),
  "description_seasoned": (A, "'erect, branching stems to about 2 ft' is the cited high end: agrees."),
  "growth_stages[2].what_to_look_for_seasoned": (A, "'erect stems to about 2 ft' is the cited high end: agrees."),
 },
 "sweet-alyssum": {"description_seasoned": (A, "'just 3 to 9 inches tall with a wider spread' is UW's figure exactly: agrees.")},
 "echinacea": {
  "description_beginner": ("edited", "Section 3 row 16 TAKEN: '2 to 4 feet' falls below NCSU's cited 3 ft floor; edited to "
                                     "the authored figure."),
  "description_seasoned": ("edited", "Section 3 row 16, same figure (scanner-invisible leaf): '2 to 4 foot stems' edited "
                                     "to the authored figure."),
  "growth_stages[1].what_to_look_for_seasoned": ("edited", "Section 3 row 16, same figure: 'flower stems 2 to 4 feet tall' "
                                                           "edited to the authored figure."),
  "varieties.recommended[4]": (A, VARIETY + " Kim's Knee High is a dwarf cultivar."),
  "varieties.recommended[0]": (A, "BELOW THE FLOOR, variety-level (Magnus 'about 30 to 36 in' vs [3,4]), SUPPORTED: Clemson "
                                  "HGIC echinacea (cited on the crop, hashed session 3) states \"'magnus' reaches 30 to 36 "
                                  "inches tall\" (restatement-support row; scanner-invisible, found by the session-3 "
                                  "review): agrees."),
  "varieties.recommended[3]": (A, "BELOW THE FLOOR, variety-level (Ruby Star 'about 30 to 36 in' vs [3,4]), SUPPORTED: "
                                  "Clemson HGIC echinacea states \"'ruby star' reaches 30 to 36 inches tall\" "
                                  "(restatement-support row): agrees."),
 },
 "bee-balm": {"description_seasoned[0]": (A, "'2 to 4 foot ... stems' is the cited height: agrees.")},
}

EDITS = {
 "dill": {
  "description_beginner": ("a tall flower stalk that can reach 3 to 5 feet,", "a tall flower stalk that can reach up to 4 feet,",
                           "H3: the cited UW figure is 18 inches to 4 feet."),
  "description_seasoned": ("(the plant reaches 3 to 5 feet in flower)", "(the plant reaches up to 4 feet in flower)",
                           "H3: the cited UW figure is 18 inches to 4 feet."),
  "container_notes.notes_seasoned": ("Standard dill reaches 3 to 5 feet", "Standard dill reaches up to 4 feet",
                                     "H3: the cited UW figure is 18 inches to 4 feet."),
  "varieties.recommended[1].note": ("A tall heirloom, 3 to 5 feet,", "A tall heirloom, up to 4 feet,",
                                    "H3: the cited UW figure is 18 inches to 4 feet."),
 },
 "echinacea": {
  "description_beginner": ("It grows about 2 to 4 feet tall", "It grows about 3 to 4 feet tall",
                           "Section 3 row 16: the authored NCSU height [3,4]."),
  "description_seasoned": ("sturdy 2 to 4 foot stems", "sturdy 3 to 4 foot stems",
                           "Section 3 row 16: the authored NCSU height [3,4]."),
  "growth_stages[1].what_to_look_for_seasoned": ("flower stems 2 to 4 feet tall", "flower stems 3 to 4 feet tall",
                                                 "Section 3 row 16: the authored NCSU height [3,4]."),
 },
 "edamame": {
  "growth_stages[2].what_to_look_for_beginner": ("usually two to three feet tall", "usually about three feet tall",
                                                 "H3: ISU, the cited page, states 'approximately 3 feet tall'."),
  "growth_stages[2].what_to_look_for_seasoned": ("its full two to three feet,", "its full height of about three feet,",
                                                 "H3: ISU, the cited page, states 'approximately 3 feet tall'."),
 },
 "green-beans-bush": {
  "growth_stages[2].what_to_look_for_beginner": ("usually one to two feet tall", "usually about two feet tall",
                                                 "H3: UMN, the cited page, states 'growing about two feet tall'."),
  "growth_stages[2].what_to_look_for_seasoned": ("its full one-to-two-foot height", "its full height of about two feet",
                                                 "H3: UMN, the cited page, states 'growing about two feet tall'."),
 },
 "okra": {
  "varieties.recommended[7].recommended_note": ("Tall heirloom (6 to 8 feet) with long pods", "Tall heirloom with long pods",
                                                "Trevor's ceiling rule: no cited hashed page states 6 to 8 ft."),
  "description_seasoned": ("commonly 4 to 6 feet and more,", "commonly 4 to 6 feet,",
                           "Trevor's ceiling rule: UF states 'most fall within the 3-6 foot range', nothing above it."),
 },
 "sunflower": {
  "description_beginner": ("towering giants over 10 feet tall", "towering giants up to 10 feet tall",
                           "Trevor's ceiling rule: NCSU, the cited page, states 2 to 10 feet."),
  "description_seasoned": ("single-stem giants that top 10 feet", "single-stem giants that reach 10 feet",
                           "Trevor's ceiling rule: NCSU, the cited page, states 2 to 10 feet."),
  "varieties.recommended[0]": ("(giant single-stem, 9 to 12 ft, one huge head,", "(giant single-stem, one huge head,",
                               "Trevor's ceiling rule: no cited hashed page states 9 to 12 ft."),
  "varieties.recommended[1]": ("(giant single-stem, 12+ ft, large heads", "(giant single-stem, large heads",
                               "Trevor's ceiling rule: no cited hashed page states 12 ft."),
 },
 "borage": {
  "description_seasoned": ("about 2 to 3 ft tall and 1 to 2 ft wide", "about 2 to 3 ft tall and 12 to 16 in wide",
                           "Section 3 row 11: NCSU 'width: 1 ft. 0 in. - 1 ft. 4 in.', the authored spread [1,1.3333]."),
 },
}

# RESTATEMENT SUPPORT (Trevor's ceiling rule, stage review): a restatement whose figure exceeds the authored range
# is "agrees" ONLY if a hashed page cited on the crop states that figure. Rows: crop -> path -> [(url, quote)].
# Written to EVIDENCE_RESTATEMENT_SUPPORT.tsv (EVIDENCE columns, entry_id "restatement-support", field = the leaf
# path, value = the prose figure), a sibling of EVIDENCE.tsv because the promote's guard E owns that file and
# refuses any row that is not a mature_dimensions value.
CORNELL_TOM = "https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/tomato-growing-guide/"
CORNELL_Q = "staked and pruned plants can grow to well over 6 feet tall in favorable growing seasons."
OSU_TOM = "https://extension.oregonstate.edu/catalog/ec-1333-grow-your-own-tomatoes-tomatillos"
OSU_Q = "indeterminate plants usually produce from one to four main stems and continue to grow until frost. they can easily grow 7 to 8 feet high."
CLEMSON_Z = "https://hgic.clemson.edu/factsheet/how-to-grow-zinnias-the-best-varieties-care-tips"
SUPPORT = {
 "beefsteak-tomato": {"det_indet.detail_beginner": ("6 feet tall or more", [(CORNELL_TOM, CORNELL_Q)]),
                      "det_indet.detail_seasoned": ("6-8 feet", [(OSU_TOM, OSU_Q), (CORNELL_TOM, CORNELL_Q)])},
 "heirloom-tomato": {"description_beginner": ("5 to 6 feet tall or more", [(CORNELL_TOM, CORNELL_Q)]),
                     "det_indet.detail_beginner": ("6 feet or more", [(CORNELL_TOM, CORNELL_Q)]),
                     "det_indet.detail_seasoned": ("6 to 8 feet", [(OSU_TOM, OSU_Q), (CORNELL_TOM, CORNELL_Q)])},
 "chives": {"varieties.recommended[3].note": ("roughly 18 to 20 inches",
                                              [("https://hort.extension.wisc.edu/articles/chives-allium-schoenoprasum",
                                                "'forescate' is larger than the species, growing 18 to 20 inches tall")])},
 "echinacea": {"varieties.recommended[0]": ("about 30 to 36 in",
                                            [("https://hgic.clemson.edu/factsheet/echinacea/",
                                              "'magnus' reaches 30 to 36 inches tall.")]),
               "varieties.recommended[3]": ("about 30 to 36 in",
                                            [("https://hgic.clemson.edu/factsheet/echinacea/",
                                              "'ruby star' reaches 30 to 36 inches tall")])},
 "zinnia": {"description_seasoned": ("cut-flower types reaching 3 to 4 ft",
                                     [(CLEMSON_Z, "range in height from 6 inches to 4 feet tall."),
                                      (CLEMSON_Z, "benary's giant series has large, double flowers 4 to 5 inches in "
                                                  "diameter that range in white and shades of orange, pink, purple, red, "
                                                  "salmon, and yellow. the plants are 2 to 3 feet wide and 3 to 4 feet tall.")])},
}
