"""PLA-10 promote 3 session 2: the ruled worklist (docs/kickoffs/59) as data. One entry per crop:
(H, S, [(fields, url, quote)], decision). fields is "H", "S" or "HS": which values the quote carries.
Quotes are norm_text form, verbatim substrings of the hashed bytes. build_stage.py turns this into the stage."""

UMD_PEP = "https://extension.umd.edu/resource/growing-peppers-home-garden"
PEP_Q = "peppers are produced on bushy plants that can reach 3-4 ft. in height."
CORNELL_TOM = "https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/tomato-growing-guide/"
NC = "https://plants.ces.ncsu.edu/plants/"

PEPPER_DEC = ("Worklist 59 row {n} (CLOSED{extra}): UMD 'growing peppers in the home garden' states 'peppers are produced "
              "on bushy plants that can reach 3-4 ft. in height.' Height [3,4]; the page states no spread: spread null.")

ROWS = {
 # ---- 2.1 tip-over
 "bell-pepper": ([3, 4], None, [("H", UMD_PEP, PEP_Q)], PEPPER_DEC.format(n=1, extra="")),
 "jalapeno": ([3, 4], None, [("H", UMD_PEP, PEP_Q)], PEPPER_DEC.format(n=2, extra="")),
 "banana-pepper": ([3, 4], None, [("H", UMD_PEP, PEP_Q)], PEPPER_DEC.format(n=3, extra="")),
 "cayenne-pepper": ([3, 4], None, [("H", UMD_PEP, PEP_Q)],
                    PEPPER_DEC.format(n=4, extra="; H2: the page names cayenne")),
 "habanero": ([3, 4], None, [("H", UMD_PEP, PEP_Q)],
              PEPPER_DEC.format(n=5, extra="; SCOPE-DOUBT ruled in by H2: the page names habanero, never C. chinense; "
                                          "the session-3 reviewer confirms")),
 "broccoli": (None, None, [],
              "Worklist 59 row 6, RE-RULED (Trevor, session 3, on the source-truth review): NULL. NCSU 'basics of "
              "broccoli production' states 'full-grown plants reach about 47 inches tall and 20 inches wide' in its "
              "Botany paragraph, between the inflorescence and 'relying on bees for cross-pollination ... seed pods': "
              "the flowering / seed plant, not the plant at harvest (the seed-stalk reasoning of section 3 row 3, onion). "
              "Hunt (session 3): UMN, UMD, UF Gardening Solutions, Clemson HGIC, Iowa State, USU and Ohioline broccoli "
              "pages fetched and hashed; none states a mature plant height (head diameters and side-dress heights "
              "only). Staged null, nothing written."),
 "brussels-sprouts": ([2, 4], [2, 4],
                      [("HS", NC + "brassica-oleracea-brussels-sprouts-group/",
                        "the plants can grow 2-4 feet tall and wide on a thick stalk.")],
                      "Worklist 59 row 7 (CLOSED): NCSU Toolbox brussels sprouts group states 'the plants can grow 2-4 "
                      "feet tall and wide'; the attributes line agrees (height 2-4)."),
 "broad-beans-fava": ([2, 6], None, [("H", NC + "vicia-faba/", "it is a stiffly erect plant that grows 2-6 feet tall")],
                      "Worklist 59 row 8 (CLOSED): NCSU Toolbox vicia-faba states 'a stiffly erect plant that grows 2-6 "
                      "feet tall'. No spread stated. D-FAVA TAKEN: the prose '2 to 4 feet' (beginner) and 'some to 5 or "
                      "6' (seasoned) sit inside [2,6] and agree; no edit."),
 "dill": ([1.5, 4], None, [("H", "https://hort.extension.wisc.edu/articles/dill-anethum-graveolens/",
                            "dill plants grow 18 inches to 4 feet tall")],
          "Worklist 59 row 9 (CLOSED): UW-Madison 'dill, anethum graveolens' states 'dill plants grow 18 inches to 4 feet "
          "tall'. Height [1.5,4]; no spread stated. H3 TAKEN: the uncited prose '3 to 5 feet' is edited to the cited "
          "figure."),
 "eggplant": ([2, 4], None, [("H", NC + "solanum-melongena/", "the plant may grow 2 to 4 feet tall and is multi-branched.")],
              "Worklist 59 row 10 (CLOSED): NCSU Toolbox solanum-melongena states 'the plant may grow 2 to 4 feet tall'; "
              "the attributes line agrees. No spread stated."),
 "cosmos": ([3, 6], None, [("H", "https://gardeningsolutions.ifas.ufl.edu/plants/ornamentals/cosmos/",
                            "garden cosmos can reach 3-6 feet")],
            "Worklist 59 row 11 / section 3 row 1 (DISAGREEMENT, H1 TAKEN): UF/IFAS gardening solutions 'cosmos' states "
            "'garden cosmos can reach 3-6 feet'. NCSU's attributes line states a closed [2,4] (H1's 'no lower bound' "
            "premise was incomplete; recorded). UF stands by tie-break (2): the crop's own prose says roughly 3 to 6 ft."),
 # ---- 2.2 closed statements
 **{t: ([2, 6], [2, 6], [("HS", CORNELL_TOM, "{CORNELL}")],
        "Worklist 59 row {n} / section 3 row 2 (DISAGREEMENT, TAKEN): Cornell 'tomato growing guide' states 'height: 2 "
        "to 6 feet' and 'spread: 2 to 6 feet'. Recorded HABIT-SPANNING: one closed range for the garden tomato covering "
        "determinate and indeterminate. NCSU Toolbox [1,10] is wider than any tomato grown on its default (scope). No "
        "support-entry height override (plan 58 section 2.4).".replace("{n}", str(n)))
    for t, n in (("cherry-tomato", 12), ("beefsteak-tomato", 13), ("grape-tomato", 15), ("heirloom-tomato", 16))},
 "roma-tomato": ([3, 4], None,
                 [("H", "https://extension.oregonstate.edu/catalog/ec-1333-grow-your-own-tomatoes-tomatillos",
                   "because of their branching and flowering characteristics, determinate cultivars tend to be fairly "
                   "short (3 to 4 feet tall) and bushy.")],
                 "Worklist 59 row 14 / section 3 row 2, DECISION-ROW CHANGE from the rulings commit's Cornell fallback "
                 "(Trevor, session 2): OSU EC1333 'grow your own tomatoes and tomatillos' was fetched and hashed this "
                 "session (browser UA; plain UA 403) and states 'determinate cultivars tend to be fairly short (3 to 4 "
                 "feet tall) and bushy.' roma is determinate (its own description), so the height is OSU [3,4] by "
                 "tie-break (1), scope. SPREAD NULL (Trevor, stage review): the height is now scoped to determinate "
                 "types; Cornell's 'spread: 2 to 6 feet' spans habits and reaches 6 ft, which is indeterminate sprawl, "
                 "so pairing it with a determinate height would make the record contradict itself. No cited page gives "
                 "a determinate spread. The other four tomatoes keep Cornell [2,6] / [2,6]."),
 "tomatillo": ([3, 4], [3, 4],
               [("HS", NC + "physalis-philadelphica/", "grow to 3 to 4 feet in height and width"),
                ("HS", "https://extension.usu.edu/yardandgarden/research/tomatillos-in-the-garden",
                 "tomatillos grow 3-4 feet tall and wide")],
               "Worklist 59 row 17 (CLOSED): NCSU Toolbox physalis-philadelphica ('grow to 3 to 4 feet in height and "
               "width') and USU 'tomatillos in the garden' ('tomatillos grow 3-4 feet tall and wide') agree on [3,4] / "
               "[3,4]; the crop's prose '3 to 4 feet tall and wide' agrees."),
 "kale": ([2.5, 3], None, [("H", "https://extension.umaine.edu/publications/4311e/15-stage-1/",
                            "kale is a large plant, often growing to 2.5-3 feet tall.")],
          "Worklist 59 row 18 (CLOSED): UMaine bulletin 4311e states 'kale is a large plant, often growing to 2.5-3 feet "
          "tall.' No spread stated."),
 "spinach": ([0.6667, 1], None, [("H", "https://extension.umd.edu/resource/growing-spinach-home-garden",
                                  "it grows to a height of 8-12 inches.")],
             "Worklist 59 row 19 (CLOSED): UMD 'growing spinach' states 'it grows to a height of 8-12 inches.' H4: 8/12 = "
             "0.6667. No spread stated."),
 "green-beans-bush": ([2, 2], None, [("H", "https://extension.umn.edu/vegetables/growing-beans",
                                      "bush beans are upright plants that do not need support, growing about two feet tall.")],
                      "Worklist 59 row 20 (CLOSED, point): UMN 'growing beans' (redirected; sentence intact) states 'bush "
                      "beans are upright plants that do not need support, growing about two feet tall.' No spread."),
 "edamame": ([3, 3], None, [("H", "https://yardandgarden.extension.iastate.edu/article/2022/07/all-about-beans",
                             "plants are approximately 3 feet tall and do not require support.")],
             "Worklist 59 row 21 (CLOSED, point): ISU 'all about beans' (redirected) states edamame 'plants are "
             "approximately 3 feet tall and do not require support.' UMN's 'up to three feet' is open: W2, the point "
             "stands. No spread."),
 "potato": ([1, 2], [1, 1.5], [("HS", NC + "solanum-tuberosum/",
                                 "height: 1 ft. 0 in. - 2 ft. 0 in. width: 1 ft. 0 in. - 1 ft. 6 in.")],
            "Worklist 59 row 22 (CLOSED): NCSU Toolbox solanum-tuberosum attributes 'height: 1 ft. 0 in. - 2 ft. 0 in. "
            "width: 1 ft. 0 in. - 1 ft. 6 in.' The crop's prose distances are hilling heights."),
 "sweet-potato": ([1, 1], None, [("H", "https://gardeningsolutions.ifas.ufl.edu/plants/edibles/vegetables/sweet-potatoes/",
                                  "about 12 inches in height when situated on the ground.")],
                  "Worklist 59 row 23 (CLOSED, point): UF/IFAS gardening solutions 'sweet potatoes' states 'about 12 "
                  "inches in height when situated on the ground.' The page's 15 ft vine run is not a spread (spec 4.5): "
                  "spread null."),
 "onion": ([1, 1.5], [0.5, 1], [("HS", NC + "allium-cepa/",
                                  "height: 1 ft. 0 in. - 1 ft. 6 in. width: 0 ft. 6 in. - 1 ft. 0 in.")],
           "Worklist 59 row 24 / section 3 row 3 (DISAGREEMENT, TAKEN): NCSU Toolbox allium-cepa [1,1.5] / [0.5,1], the "
           "bulb crop's foliage height; Cornell scene4983's 3 ft high end reaches seed-stalk height. Spreads agree."),
 "okra": ([3, 6], None, [("H", "https://gardeningsolutions.ifas.ufl.edu/plants/edibles/vegetables/okra/",
                          "plant heights vary by cultivar and pruning practices. most fall within the 3-6 foot range")],
          "Worklist 59 row 25 (CLOSED; D-OKRA TAKEN): UF/IFAS gardening solutions 'okra' states 'plant heights vary by "
          "cultivar and pruning practices. most fall within the 3-6 foot range': a typical range authors [3,6]. No spread."),
 "celery": ([1.5, 2], None, [("H", "https://extension.usu.edu/yardandgarden/research/celery-in-the-garden",
                              "celery grows to a height of 18 to 24 inches")],
            "Worklist 59 row 26 (CLOSED): USU 'celery in the garden' states 'celery grows to a height of 18 to 24 inches'. "
            "No spread. The crop's other prose heights are harvest-stage stalk heights."),
 "artichoke": ([3, 6], [2, 4], [("HS", "https://gardening.cals.cornell.edu/garden-guidance/foodgarden/vegetable-growing-guides/globe-artichokes-growing-guide/",
                                 "height: 3 to 6 feet spread: 2 to 4 feet")],
               "Worklist 59 row 27 / section 3 row 4 (DISAGREEMENT, TAKEN): Cornell 'globe artichokes growing guide' "
               "'height: 3 to 6 feet spread: 2 to 4 feet'. W2: a closed range beats TAMU EHT-065's point ('3 feet in "
               "height and width')."),
 "asparagus": ([5, 6], None, [("H", "https://extension.oregonstate.edu/news/growing-asparagus-takes-patience-rewards-gardeners-years",
                               "asparagus foliage can reach 5 to 6 feet in height")],
               "Worklist 59 row 28 (CLOSED): OSU 'growing asparagus takes patience' states 'asparagus foliage can reach 5 "
               "to 6 feet in height' (the fern). Spear heights in the prose are harvest-stage. No spread."),
 "leek": ([2, 3], None, [("H", "https://extension.umn.edu/vegetables/growing-leeks",
                          "plants grow two to three feet tall, and can have a width of two inches.")],
          "Worklist 59 row 29 (CLOSED; D-LEEK TAKEN): UMN 'growing leeks' (redirected) states 'plants grow two to three "
          "feet tall, and can have a width of two inches.' The 'width' is shaft diameter, never a canopy spread: spread null."),
 "basil": ([0.6667, 2], [0.6667, 1], [("HS", "https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/basil",
                                       "size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety")],
           "Worklist 59 row 30 / section 3 row 5 (DISAGREEMENT, TAKEN): UC Master Gardeners of Santa Clara County "
           "'basil' 'size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety' (scope: the crop covers many "
           "basils; UC Sonoma's figure is sweet basil only)."),
 "cilantro-coriander": ([1, 3], None, [("H", "https://extension.usu.edu/yardandgarden/research/cilantro-coriander-in-the-garden",
                                        "plants grow to 1-3 feet tall")],
                        "Worklist 59 row 31 / section 3 row 6 (DISAGREEMENT, TAKEN; D-CIL): USU 'cilantro/coriander in the "
                        "garden' states 'plants grow to 1-3 feet tall'. UW's changed page ('1 to 1⁄2 feet', U+2044) is a "
                        "known T4 reader gap; no T4 change. No spread."),
 "chives": ([1, 1.5], [1, 1.4167], [("HS", NC + "allium-schoenoprasum/",
                                     "height: 1 ft. 0 in. - 1 ft. 6 in. width: 1 ft. 0 in. - 1 ft. 5 in.")],
            "Worklist 59 row 32 / section 3 row 7 (DISAGREEMENT, TAKEN): NCSU Toolbox allium-schoenoprasum attributes, the "
            "species record giving both dimensions (17/12 = 1.4167); Illinois 'about 10-12 inches tall' not taken."),
 "mint": ([1, 2], [1, 2], [("HS", NC + "mentha-spicata/", "growing quickly 1 to 2 feet high and wide")],
          "Worklist 59 row 33 (SCOPE-DOUBT; D-MINT TAKEN, condition met): NCSU Toolbox mentha-spicata 'growing quickly 1 "
          "to 2 feet high and wide'. SCOPE RECORDED: the page is spearmint; the crop is genus-level garden mint and names "
          "spearmint the everyday mint. The session-3 reviewer confirms."),
 "lemongrass": ([3, 6], [2, 3], [("H", "https://extension.usu.edu/yardandgarden/research/lemongrass-in-the-garden",
                                  "it can grow 3 to 6 feet tall and 3 feet wide, when water, fertilizer and growing "
                                  "conditions are optimal."),
                                 ("S", NC + "cymbopogon-citratus/",
                                  "height: 2 ft. 0 in. - 4 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in.")],
                "Worklist 59 row 34 / section 3 row 8, RE-RULED (Trevor, session 3, on the source-truth review): the row's "
                "premise ('the prose 3 to 6 feet exceeds both pages') missed USU 'lemongrass in the garden', cited on the "
                "crop and hashed (e76666f1), which states 'it can grow 3 to 6 feet tall and 3 feet wide'. Three closed "
                "height ranges (NCSU [2,4], UC Santa Clara [3,4], USU [3,6]), all in scope; tie-break (2): USU's is the "
                "range the crop's prose already states. HEIGHT USU [3,6]; SPREAD NCSU attributes [2,3] (a closed range "
                "beats USU's '3 feet wide' point, W2; two values on two pages, W6). No prose edit."),
 "marigold": ([1, 4], [0.5, 1], [("HS", NC + "tagetes/",
                                  "height: 1 ft. 0 in. - 4 ft. 0 in. width: 0 ft. 6 in. - 1 ft. 0 in.")],
              "Worklist 59 row 35 / section 3 row 9 (DISAGREEMENT, TAKEN): NCSU Toolbox tagetes (genus page, matching "
              "the crop's erecta + patula scope) attributes [1,4] / [0.5,1]; the same page's prose 'typically 1 to 4 feet "
              "tall' agrees. Recorded cultivar-spanning (dwarf to giant)."),
 "nasturtium": (None, None, [], "Worklist 59 row 36 (CONDITIONAL; D-NAST TAKEN: null): NCSU Toolbox tropaeolum-majus "
                "'height: 1 ft. 0 in. - 10 ft. 0 in.' spans bush and climbing forms in one figure; which habit is grown is a "
                "plant_habit fact (PLA-12; spec 4.4 peas precedent). Staged null, nothing written."),
 "sunflower": ([1.5, 10], [1.5, 3], [("HS", NC + "helianthus-annuus/",
                                      "height: 1 ft. 6 in. - 10 ft. 0 in. width: 1 ft. 6 in. - 3 ft. 0 in.")],
               "Worklist 59 row 37 / section 3 row 10 (DISAGREEMENT, TAKEN): NCSU Toolbox helianthus-annuus attributes "
               "[1.5,10] / [1.5,3] (one statement, both dimensions; the K4 convention). Recorded cultivar-spanning "
               "(dwarf to giant)."),
 "borage": ([2, 3], [1, 1.3333],
            [("H", "https://ucanr.edu/site/uc-marin-master-gardeners/document/borage",
              "borage is an exuberant annual that grows two to three feet tall"),
             ("S", NC + "borago-officinalis/", "height: 1 ft. 7 in. - 3 ft. 2 in. width: 1 ft. 0 in. - 1 ft. 4 in.")],
            "Worklist 59 row 38 / section 3 row 11 (DISAGREEMENT, TAKEN): height UC Marin Master Gardeners 'borage' "
            "('grows two to three feet tall', agreeing with the crop's prose: rule 3); spread NCSU Toolbox "
            "borago-officinalis 'width: 1 ft. 0 in. - 1 ft. 4 in.' (16/12 = 1.3333), the one page stating it (W6)."),
 "calendula": ([1, 2], [1, 2], [("HS", "https://ask.ifas.ufl.edu/publication/FP087",
                                 "height: 1 to 2 feet spread: 1 to 2 feet")],
               "Worklist 59 row 39 / section 3 row 12 (DISAGREEMENT, TAKEN): UF/IFAS FP087 'height: 1 to 2 feet spread: 1 "
               "to 2 feet'; NCSU agrees exactly; USU's 8 in low end is the only dissent."),
 "zinnia": ([1, 3], [1, 2], [("HS", "https://edis.ifas.ufl.edu/publication/FP623",
                              "height: 1 to 3 feet spread: 1 to 2 feet")],
            "Worklist 59 row 40 / section 3 row 13 (DISAGREEMENT, TAKEN): UF/IFAS FP623 (redirected to ask.ifas) dimension "
            "statement 'height: 1 to 3 feet spread: 1 to 2 feet'; Clemson 6 in - 4 ft not taken."),
 "chamomile": ([1, 2], [1, 1.1667], [("HS", "https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/chamomile",
                                      "size: 1 to 2 feet tall, 12 to 14 inches wide")],
               "Worklist 59 row 41 / section 3 row 14 (DISAGREEMENT + UNFETCHABLE; D-CHA TAKEN: hunt first). HUNT RESULT: "
               "the cited UC Santa Clara MG URL (ucanr.edu/sites/mgscc2016/...) still 403s, but the same page lives at "
               "the site's current path ucanr.edu/site/uc-master-gardeners-santa-clara-county/chamomile (the move basil "
               "and lemongrass already made), fetched and hashed this session (browser UA; plain 403). Its bytes state "
               "'size: 1 to 2 feet tall, 12 to 14 inches wide', the doc-cache text verbatim. Per the ruled row, a hashed "
               "Santa Clara page gives [1,2] / [1,1.1667] (14/12). NCSU matricaria-chamomilla was also hashed: "
               "'height: 0 ft. 6 in. - 2 ft. 0 in. width: 0 ft. 6 in. - 2 ft. 0 in.' (NOT plan 58 D's 1'1\"-2'6\"; the "
               "page has changed), not taken."),
 "sweet-alyssum": ([0.25, 0.75], [0.5, 1],
                   [("H", "https://hort.extension.wisc.edu/articles/sweet-alyssum-lobularia-maritima/",
                     "sweet alyssum grows 3-9 inches tall with a wider spread."),
                    ("S", NC + "lobularia-maritima/", "height: 0 ft. 3 in. - 0 ft. 10 in. width: 0 ft. 6 in. - 1 ft. 0 in.")],
                   "Worklist 59 row 42 / section 3 row 15 (DISAGREEMENT, TAKEN): height UW-Madison 'sweet alyssum' "
                   "('grows 3-9 inches tall'; the crop's prose says just 3 to 9 inches tall); spread NCSU Toolbox "
                   "lobularia-maritima 'width: 0 ft. 6 in. - 1 ft. 0 in.', the one page with a figure."),
 "echinacea": ([3, 4], [1, 2], [("HS", NC + "echinacea-purpurea/",
                                 "dimensions: height: 3 ft. 0 in. - 4 ft. 0 in. width: 1 ft. 0 in. - 2 ft. 0 in.")],
               "Worklist 59 row 43 / section 3 row 16 (DISAGREEMENT, TAKEN; session 3 re-examined): NCSU Toolbox "
               "echinacea-purpurea attributes [3,4] / [1,2] (its prose 'it may grow 3 to 4 feet tall' agrees). SPREAD "
               "now authored (Trevor, session 3): the same attributes line's closed 'width: 1 ft. 0 in. - 2 ft. 0 in.'. "
               "Session-3 hunt for the prose's '2 to 4': UF EDIS FP192 (cited, hashed) states 'flowers stand 2 to "
               "4feettall' (the publisher's glued text, which T4 cannot read; its own dimensions block says 'height: 1 to "
               "3 feet'); Clemson HGIC echinacea (cited, hashed this session) states E. purpurea 'grows up to 2 to "
               "3 1/2 feet tall' with U+2044 fractions (the D-T4 reader gap; the second page needing it, recorded) and "
               "the genus-level open 'up to 4 feet'; PSU 24-36 in. No T4-readable page states 2-4, so the ruled "
               "fallback stands: NCSU [3,4], the prose '2 to 4 feet' edited to the authored figure."),
 "bee-balm": ([2, 4], [2, 3], [("HS", NC + "monarda-didyma/",
                                "height: 2 ft. 0 in. - 4 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in.")],
              "Worklist 59 row 44 (CLOSED): NCSU Toolbox monarda-didyma attributes [2,4] / [2,3]; the same page's prose "
              "'can reach a height of 4 feet' agrees."),
 "viola": ([0.5, 0.75], [0.75, 1], [("HS", NC + "viola-x-wittrockiana/",
                                     "it grows 6 to 9 inches in height and 9 to 12 inches in width.")],
           "Worklist 59 row 45 / section 3 row 17 (DISAGREEMENT + SCOPE-DOUBT, TAKEN): NCSU Toolbox viola-x-wittrockiana "
           "prose 'it grows 6 to 9 inches in height and 9 to 12 inches in width.' SCOPE RECORDED: every statement is "
           "pansy (V. x wittrockiana); the crop also covers cornuta / tricolor (W3)."),
 "sweet-pea": (None, None, [], "Worklist 59 row 46 (CONDITIONAL; D-SPEA TAKEN: null): NCSU Toolbox lathyrus-odoratus "
               "ties each figure to a habit ('if allowed to climb ... up to 8 feet. if grown as a bush ... 3 foot'); the "
               "peas precedent. Staged null, nothing written."),
}

# ---- 2.3 backfill: values kept, sibling anchored on the record's URL (K3), apple re-pointed (K1), blueberry kept (K2 b1)
BACKFILL = {
 "peach": [("HS", NC + "prunus-persica/", "the tree will grow quickly to 15-25 feet tall and wide")],
 "nectarine": [("HS", NC + "prunus-persica/", "the tree will grow quickly to 15-25 feet tall and wide")],
 "apple": [("H", "https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf",
            "m 26-semi-dwarf habit, 10'-14' tall")],
 "lemon": [("H", "https://edis.ifas.ufl.edu/publication/HS402", "trees may reach 10-20 ft (3.1-6.1 m) in height")],
 "blueberry": [("HS", "https://extension.psu.edu/blueberries-in-the-garden-and-the-kitchen",
                "this shrub can be 5 to 8 feet tall and wide at maturity or even larger")],
 "thyme": [("HS", NC + "thymus-vulgaris/", "about 6 to 12 inches high and 6 to 16 inches wide")],
 "rosemary": [("H", NC + "salvia-rosmarinus/", "the shrub grows from 4 to 5 feet tall"),
              ("S", NC + "salvia-rosmarinus/", "width: 3 ft. 0 in. - 4 ft. 0 in.")],
 "oregano": [("HS", NC + "origanum-vulgare/", "height: 1 ft. 0 in. - 3 ft. 0 in. width: 1 ft. 0 in. - 2 ft. 0 in.")],
 "sage": [("H", NC + "salvia-officinalis/", "height: 1 ft. 0 in. - 2 ft. 0 in."),
          ("S", NC + "salvia-officinalis/", "up to 2 feet tall and 2 to 3 feet wide")],
 "fig": [("HS", "https://hgic.clemson.edu/factsheet/fig/", "height & spread: 15 - 30 ft tall and wide")],
 "pomegranate": [("HS", NC + "punica-granatum/", "10 to 12 feet tall and 8 to 10 feet wide")],
 "elderberry": [("H", NC + "sambucus-canadensis/", "measuring 5 to 12 feet tall"),
                ("S", NC + "sambucus-canadensis/", "width: 6 ft. 0 in. - 12 ft. 0 in.")],
 "persimmon": [("HS", NC + "diospyros-kaki/", "height: 20 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 25 ft. 0 in.")],
 "mulberry": [("HS", NC + "morus-alba/", "height: 30 ft. 0 in. - 60 ft. 0 in. width: 30 ft. 0 in. - 50 ft. 0 in.")],
 "pawpaw": [("HS", NC + "asimina-triloba/", "height: 15 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 30 ft. 0 in.")],
 "lavender": [("HS", NC + "lavandula-angustifolia/", "height: 1 ft. 0 in. - 2 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in.")],
}
BACKFILL_ROW = {"peach": 47, "nectarine": 48, "apple": 49, "lemon": 50, "blueberry": 51, "thyme": 52, "rosemary": 53,
                "oregano": 54, "sage": 55, "fig": 56, "pomegranate": 57, "elderberry": 58, "persimmon": 59,
                "mulberry": 60, "pawpaw": 61, "lavender": 62}
