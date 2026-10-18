"""PLA-750 promote texts: every value the promote writes, with the hashed-page quote each new clause rests on.

Rulings: 47a09951 (D1 to D6 + per-row verdicts), b963b423 (P1 to P5), 7c155149 (fetches, P5 as built, the
calendula rule). Quotes are copied from the raw hashed bytes (tools/.evidence_cache, MANIFEST-listed);
build_stage.py re-checks every one through cited_promote_common.cached_quote and refuses a miss.
"""
V = "2026-10-18"   # anchor `verified` date: the day the raw bytes were fetched and checked

URL = {
    "umn_spinach": "https://extension.umn.edu/vegetables/growing-spinach-and-swiss-chard",
    "usu_leafy": "https://extension.usu.edu/vegetableguide/leafy-greens/planting-spacing",
    "usu_cilantro": "https://extension.usu.edu/yardandgarden/research/cilantro-coriander-in-the-garden",
    "usu_beet": "https://extension.usu.edu/yardandgarden/research/beets-in-the-garden",
    "ucmg_sonoma_radish": "https://ucanr.edu/site/uc-master-gardener-program-sonoma-county/radish",
    "umn_kohlrabi": "https://extension.umn.edu/vegetables/growing-kohlrabi",
    "usu_kohlrabi": "https://extension.usu.edu/yardandgarden/research/kohlrabi-in-the-garden",
    "usu_peas": "https://extension.usu.edu/yardandgarden/research/peas-in-the-garden",
    "eberle": "https://experts.umn.edu/en/publications/seed-germination-of-calendula-in-response-to-temperature/",
    "uf_pansies": "https://gardeningsolutions.ifas.ufl.edu/plants/ornamentals/pansies/",
    "uf_fp609": "https://edis.ifas.ufl.edu/publication/FP609",
    "tamu_celery": "https://aggiehorticulture.tamu.edu/vegetable/wp-content/uploads/sites/10/2011/10/celery2.pdf",
    "ucanr_7243": "https://my.ucanr.edu/repository/fileaccess.cfm?article=54051&p=+FLPUZE",
    "umn_broccoli": "https://extension.umn.edu/vegetables/growing-broccoli",
    "usu_broccoli": "https://extension.usu.edu/yardandgarden/research/broccoli-in-the-garden",
    "usu_cauliflower": "https://extension.usu.edu/yardandgarden/research/cauliflower-in-the-garden",
    "umn_cauliflower": "https://extension.umn.edu/vegetables/growing-cauliflower",
    "usu_cabbage": "https://extension.usu.edu/yardandgarden/research/cabbage-in-the-garden",
    "clemson_cabbage": "https://hgic.clemson.edu/factsheet/cabbage-chinese-cabbage/",
    "umn_cabbage": "https://extension.umn.edu/vegetables/growing-cabbage",
    "usu_brussels": "https://extension.usu.edu/yardandgarden/research/brussel-sprouts-in-the-garden",
    "umd_brussels": "https://extension.umd.edu/resource/brussels-sprouts",
    "clemson_brussels": "https://hgic.clemson.edu/start-brussels-sprouts-now-for-a-winter-harvest/",
    "umn_collards_kale": "https://extension.umn.edu/vegetables/growing-collards-and-kale",
    "umd_leafy": "https://extension.umd.edu/resource/growing-leafy-greens-home-garden",
    "mu_edamame": "https://extension.missouri.edu/news/the-soy-of-gardening-includes-edamame",
    "uiuc_borage": "https://extension.illinois.edu/herbs/borage",
    "clemson_carrot": "https://hgic.clemson.edu/factsheet/carrot-beet-radish-parsnip/",
    "sare_arugula": "https://www.sare.org/publications/northeast-crop-production-harvest-manual/arugula/",
    "steiner": "https://www.redalyc.org/pdf/995/99515218004.pdf",
    "clemson_herbs": "https://hgic.clemson.edu/factsheet/herbs/",
    "usu_turnip": "https://extension.usu.edu/yardandgarden/research/rutabagas-and-turnips-in-the-garden",
    "purdue_ho186": "https://www.extension.purdue.edu/extmedia/HO/HO-186-W.pdf",
    "umn_bokchoy": "https://extension.umn.edu/vegetables/growing-chinese-cabbage-and-bok-choy",
    "uiuc_sweetpea": "https://web.extension.illinois.edu/hortanswers/PlantDetail.cfm?PlantID=532&PlantTypeID=5",
    "uf_nasturtium": "https://blogs.ifas.ufl.edu/charlotteco/2024/12/20/nasturtiums-make-me-smile/",
    "uwi_chamomile": "https://hort.extension.wisc.edu/articles/chamomile-matricaria-chamomilla/",
    "clemson_alyssum": "https://hgic.clemson.edu/sweet-alyssum/",
    "usu_spinach": "https://extension.usu.edu/yardandgarden/research/spinach-in-the-garden",
    "clemson_spinach": "https://hgic.clemson.edu/factsheet/spinach/",
    "uiuc_spinach": "https://extension.illinois.edu/gardening/spinach",
}

# ---------------------------------------------------------------- D6 + catalog mints (document-scoped, T1)
MINTS = {
    "sare_necphm_arugula": {
        "id": "sare_necphm_arugula", "name": "USDA SARE, Northeast Crop Production & Harvest Manual: Arugula",
        "title": "Arugula", "publisher": "USDA Sustainable Agriculture Research and Education (SARE)",
        "url": URL["sare_arugula"], "source_class": "government_program", "trust_tier": "high", "accessed": V,
        "tier": "T1", "citable_for": "Arugula germination and soil-temperature table, bolting, planting timing."},
    "steiner_2010_arugula": {
        "id": "steiner_2010_arugula",
        "name": "Steiner et al. 2010, Scientia Agraria 11(2):119-124 (peer-reviewed)",
        "title": "Germination of rocket (Eruca sativa, Diplotaxis tenuifolia) seeds at different temperatures",
        "publisher": "Scientia Agraria (Universidade Federal do Parana)", "url": URL["steiner"],
        "source_class": "peer_reviewed_journal", "trust_tier": "high", "accessed": V, "tier": "T1",
        "citable_for": "Arugula seed germination across 10 to 35 degrees C (PLA-750 D6: peer-reviewed anchor where "
                       "T1 extension is thinner, cited as journal and year)."},
    "eberle_2014_calendula": {
        "id": "eberle_2014_calendula",
        "name": "Eberle et al. 2014, Industrial Crops and Products 52:199-204 (peer-reviewed)",
        "title": "Seed germination of calendula in response to temperature",
        "publisher": "Industrial Crops and Products (abstract on Experts@Minnesota)", "url": URL["eberle"],
        "source_class": "peer_reviewed_journal", "trust_tier": "high", "accessed": V, "tier": "T1",
        "citable_for": "Calendula germination temperatures and the sow-below-30-degrees-C soil rule (PLA-750 D6). "
                       "Cite the 2014 paper only, never the 2013 conference abstract (ruling 7c155149)."},
    "ucanr_pub7243": {
        "id": "ucanr_pub7243", "name": "UC ANR Publication 7243, Green Onion Production in California",
        "title": "Green Onion Production in California", "publisher": "University of California ANR",
        "url": URL["ucanr_7243"], "source_class": "university_extension", "trust_tier": "high", "accessed": V,
        "tier": "T1", "citable_for": "Green onion planting seasons and production (spring-onion)."},
    "tamu_celery_crop_sheet": {
        "id": "tamu_celery_crop_sheet", "name": "Texas A&M AgriLife Extension (J. Masabni), Celery crop sheet",
        "title": "Celery", "publisher": "Texas A&M AgriLife Extension", "url": URL["tamu_celery"],
        "source_class": "university_extension", "trust_tier": "high", "accessed": V, "tier": "T1",
        "citable_for": "Celery temperature requirements and quality."},
}

# ---------------------------------------------------------------- sowing_heat_ceiling (30 crops)
PROXY = ("The source's figure is a soil temperature; the app compares a forecast air high against it. That is a "
         "stated proxy (PLA-750 D2), not a sourced air threshold: hot days ahead usually mean hot soil, and the "
         "held line says so in house voice.")
SEEDZONE = (" The sentence gives a germination temperature without saying soil; a germination temperature is a "
            "seed-zone temperature (PLA-750 P3).")


def held(temp, measures, basis, claim, cs, cs_url, note=None, ts=None, ts_url=None):
    f = {"temp_f": temp, "measures": measures, "basis": basis, "claim": claim, "claim_source": cs}
    srcs, anc = [cs], {cs: {"url": cs_url, "verified": V}}
    if ts:
        f["temp_source"] = ts
        srcs.append(ts)
        anc[ts] = {"url": ts_url, "verified": V}
    if note:
        f["note"] = note
    f["sources"], f["anchoring_urls"] = srcs, anc
    return f


def nulled(note, *cites):
    return {"temp_f": None, "note": note, "sources": [c for c, _u in cites],
            "anchoring_urls": {c: {"url": u, "verified": V} for c, u in cites}}


UNSOURCED = "No sowing hold until a source ties heat to the sowing itself (PLA-750 ruling 47a09951). "

FIELDS = {
    # ---- held (10) --------------------------------------------------------------------------------
    "spinach": held(80, "air", "sowing_statement",
                    "For a continuous spring supply, plant spinach seeds every one to two weeks, until outdoor "
                    "temperatures reach 80°F.", "umn_ext", URL["umn_spinach"]),
    "lettuce-leaf": held(80, "soil", "germination",
                         "Soil temperatures above 80 °F cause the seeds of some crops (lettuce, spinach, others) to "
                         "go dormant and they will not germinate until cooler soil temperatures return.",
                         "usu_ext", URL["usu_leafy"], note=PROXY),
    "cilantro-coriander": held(75, "soil", "bolting",
                               "Try to keep the soil temperature below 75°F, especially if grown near a heat source "
                               "or a particular window that becomes quite warm",
                               "usu_ext", URL["usu_cilantro"],
                               note=PROXY + " USU gives the figure as a bolting measure, not a germination one."),
    "beet": held(80, "soil", "germination", "Temperatures above 80°F reduce seed germination.",
                 "usu_ext", URL["usu_beet"], note=PROXY + SEEDZONE),
    "radish": held(75, "air", "maturity_coupled",
                   "Plant fast-growing varieties in shallow beds or containers during spring and fall when "
                   "temperatures are 50-75 degrees.", "uc_mg", URL["ucmg_sonoma_radish"],
                   note="The page gives degrees with no unit or medium; read as °F air, a planting-season sentence "
                        "on a US page (PLA-750 P3). The hold rests on maturity: a radish sown into a hot spell "
                        "matures in it (D3)."),
    "kohlrabi": held(75, "air", "maturity_coupled",
                     "Avoid planting after May 1. The high temperatures will not produce good quality.",
                     "umn_ext", URL["umn_kohlrabi"],
                     note="UMN ties the sowing date to the heat harm (D3); the number is USU's growing ceiling, "
                          "\"Kohlrabi grows best when temperatures do not exceed 75°F.\"",
                     ts="usu_ext", ts_url=URL["usu_kohlrabi"]),
    "sugar-snap-peas": held(80, "air", "germination",
                            "Peas are cool weather, frost tolerant vegetables that require soil and air temperatures "
                            "to remain below 80ºF for best germination and plant growth.", "usu_ext", URL["usu_peas"]),
    "snow-peas": held(80, "air", "germination",
                      "Peas are cool weather, frost tolerant vegetables that require soil and air temperatures to "
                      "remain below 80ºF for best germination and plant growth.", "usu_ext", URL["usu_peas"]),
    "calendula": held(86, "soil", "sowing_statement",
                      "Accordingly, calendula seed should be sown in the field only if forecasted soil conditions "
                      "are expected to be below 30. °C during seed germination.",
                      "eberle_2014_calendula", URL["eberle"],
                      note=PROXY + " 30 °C is 86 °F. The abstract page renders the figure as \"30. °C\" (publisher "
                                   "markup); the claim keeps it verbatim. heat_threshold_f stays 85, USU's bloom "
                                   "number (P2)."),
    "viola": held(75, "soil", "germination",
                  "If planting by seed, keep in mind that they only germinate at temperatures between 65˚ and "
                  "75˚Fahrenheit.", "uf_ifas", URL["uf_pansies"], note=PROXY + SEEDZONE),
    # ---- not held: the 10 ruled changes ----------------------------------------------------------
    "celery": nulled("No sowing hold: celery is started indoors and transplanted, so an outdoor forecast cannot "
                     "bear on its sowing. Its heat harm is near harvest: Texas A&M, \"Average high temperature above "
                     "75°F in month preceding harvest limits vegetative growth and quality.\"",
                     ("tamu_celery_crop_sheet", URL["tamu_celery"])),
    "spring-onion": nulled("No sowing hold: no source ties heat to sowing green onions, and UC ANR plants them in "
                           "summer too: \"Green onions are plant- ed during the fall, spring, and summer for harvest "
                           "60 to 120 days later.\"", ("ucanr_pub7243", URL["ucanr_7243"])),
    "broccoli": nulled("No sowing hold: the heat harm is at heading, not sowing. UMN, \"While summer heat harms the "
                       "quality of the developing head, heat while the leafy broccoli plant is growing is fine.\" "
                       "and \"Direct seed broccoli in July.\" The heading reason lives in "
                       "tips_by_stage.head_forming (D4).", ("umn_ext", URL["umn_broccoli"])),
    "cauliflower": nulled("No sowing hold: the heat harm is at curd formation. USU, \"Low (32°F) or high (greater "
                          "than 80°F) temperatures decrease plant growth, lower yields and decrease head quality.\" "
                          "UMN, \"Direct seed cauliflower in July.\" The reason lives in tips_by_stage.curd_forming "
                          "(D4).", ("usu_ext", URL["usu_cauliflower"]), ("umn_ext", URL["umn_cauliflower"])),
    "cabbage": nulled("No sowing hold: the heat harm is to the maturing head. USU, \"Cabbage grows best when "
                      "temperatures do not exceed 80°F and is not seriously damaged by temperatures down to 25°F.\" "
                      "UMN, \"For a fall crop, plant seed directly in the garden in early July.\" The reason lives "
                      "in tips_by_stage.head_forming (D4).",
                      ("usu_ext", URL["usu_cabbage"]), ("umn_ext", URL["umn_cabbage"])),
    "brussels-sprouts": nulled("No sowing hold: the heat harm is to maturing sprouts. USU, \"High summer "
                               "temperatures reduce plant growth, decrease sprout quality, and cause internal "
                               "tipburn.\" The reason lives in tips_by_stage.sprout_formation (D4).",
                               ("usu_ext", URL["usu_brussels"])),
    "kale": nulled("No sowing hold: the heat harm is to leaves at harvest. UMN, \"For the spring crop, flavor is best "
                   "if you harvest the plants before the weather becomes hot and dry.\" The reason lives in "
                   "tips_by_stage.harvest (D4).", ("umn_ext", URL["umn_collards_kale"])),
    "collards": nulled("No sowing hold: the heat harm is to leaves at harvest, and collards tolerate heat. UMD, "
                       "\"Collards are more heat-tolerant than kale or turnip greens.\" The reason lives in "
                       "tips_by_stage.harvest (D4).", ("umd_ext", URL["umd_leafy"])),
    "edamame": nulled("No sowing hold: edamame is a warm-season crop sown through summer. MU Extension, \"For a "
                      "continuous supply of edamame throughout the growing season, plant every 7-14 days up to "
                      "mid-July, depending on location.\"", ("mu_ext", URL["mu_edamame"])),
    "borage": nulled("No sowing hold: no T1 source ties heat to sowing borage. Illinois, \"If grown for culinary "
                     "use, successive sowings of seed at four week intervals will result in a good supply of fresh "
                     "foliage.\"", ("uiuc_ext", URL["uiuc_borage"])),
    # ---- not held: the 9 unsourced holds (weak lead carried for the next pass) ----------------------
    "carrot": nulled(UNSOURCED + "Weak lead, germination only at the extreme: Clemson, \"Seeds will not germinate "
                     "above 95 °F.\"", ("clemson_hgic", URL["clemson_carrot"])),
    "arugula": nulled(UNSOURCED + "Weak lead, mature plant only: SARE, \"Arugula bolts due to longer days and high "
                      "temperatures.\"", ("sare_necphm_arugula", URL["sare_arugula"])),
    "dill": nulled(UNSOURCED + "Weak lead, mature plant only: Clemson, \"At the onset of hot weather, this "
                   "cool-weather annual will go to seed.\"", ("clemson_hgic", URL["clemson_herbs"])),
    "turnip": nulled(UNSOURCED + "Weak lead, mature plant only: USU, \"Turnips grow best when temperatures do not "
                     "exceed 85ºF.\"", ("usu_ext", URL["usu_turnip"])),
    "parsley": nulled(UNSOURCED + "Weak lead, germination only (Harrington soil table, optimum 75, range 50-85, "
                      "limits 40/90): Purdue, \"Parsley 75/50-85 40/90\"", ("purdue_ext", URL["purdue_ho186"])),
    "bok-choy": nulled(UNSOURCED + "Weak lead, mature plant only: UMN, \"Warm weather can cause bok choy to "
                       "flower.\"", ("umn_ext", URL["umn_bokchoy"])),
    "sweet-pea": nulled(UNSOURCED + "Weak lead, mature plant only: Illinois, \"will bloom poorly (or not at all) "
                        "when weather is hot.\"", ("uiuc_ext", URL["uiuc_sweetpea"])),
    "nasturtium": nulled(UNSOURCED + "Weak lead, mature plant only: UF/IFAS, \"Nasturtiums do best in the cooler "
                         "part of the year and will tend to decline when the temperatures get too hot.\"",
                         ("uf_ifas", URL["uf_nasturtium"])),
    "chamomile": nulled(UNSOURCED + "No T1 heat statement found; the one temperature lead favors warmth: "
                        "UW-Madison, \"Under warm conditions, germination generally occurs within a week.\"",
                        ("uwi_hort", URL["uwi_chamomile"])),
    # ---- not held: D3 ----------------------------------------------------------------------------
    "sweet-alyssum": nulled("No sowing hold: the heat effect is on mature plants, with no sowing-date source and no "
                            "number (D3). Clemson, \"As summer temperatures rise, alyssum grown from seed may stop "
                            "producing flowers.\"", ("clemson_hgic", URL["clemson_alyssum"])),
}

# ---------------------------------------------------------------- D5: heat_tolerant -> quality_loss (P5)
ENUMS = {"sweet-pea": ("heat_tolerant", "quality_loss"), "sweet-alyssum": ("heat_tolerant", "quality_loss"),
         "nasturtium": ("heat_tolerant", "quality_loss")}

# ---------------------------------------------------------------- prose edits (touched-leaf rule)
# (crop, path, [(old_sub, new_sub)], cited_at, [(new_sub, source_id, url, quote)], decision or None)
G = "tips_by_stage.germination"
PROSE = [
    # D4 broccoli: re-sourced to UMN + USU
    ("broccoli", "tips_by_stage.head_forming[0].text_seasoned",
     [("heat above about 86°F by day and warm nights during heading cause bolting and loose, open heads",
       "summer heat harms the developing head, and hot weather above about 86°F by day with nights over 77°F can "
       "keep a crown from forming, while high temperatures cause loose heads that taste bitter")],
     "tips_by_stage.head_forming[0]",
     [("umn_ext", URL["umn_broccoli"], "While summer heat harms the quality of the developing head"),
      ("umn_ext", URL["umn_broccoli"], "Hot weather (86 degrees Fahrenheit in the day and over 77 degrees "
                                       "Fahrenheit at night) can cause broccoli to grow no crown."),
      ("usu_ext", URL["usu_broccoli"], "High summer temperatures reduce growth, decrease quality, and cause loose "
                                       "heads to form, which taste bitter.")], None),
    ("broccoli", "tips_by_stage.head_forming[0].text_beginner",
     [("Hot days over about 86°F and warm nights now can make the head loose or cause it to flower.",
       "Hot days over about 86°F and warm nights now can hurt the head and make it loose and bitter.")],
     "tips_by_stage.head_forming[0]",
     [("umn_ext", URL["umn_broccoli"], "While summer heat harms the quality of the developing head"),
      ("usu_ext", URL["usu_broccoli"], "cause loose heads to form, which taste bitter.")], None),
    # D4 cauliflower: the heat clause re-sourced to USU
    ("cauliflower", "tips_by_stage.curd_forming[1].text_seasoned",
     [("heat causes ricing and discoloration", "temperatures above 80°F lower head quality")],
     "tips_by_stage.curd_forming[1]",
     [("usu_ext", URL["usu_cauliflower"], "Low (32°F) or high (greater than 80°F) temperatures decrease plant "
                                          "growth, lower yields and decrease head quality.")], None),
    # live: arugula germination claim rewritten to SARE + Steiner
    ("arugula", G + "[0].text_seasoned",
     [("Arugula germinates fast and in cool soil, but germination drops off sharply above about 80°F, which is why "
       "midsummer sowings fail.",
       "Arugula germinates fast in cool soil, fastest near 75°F, and still germinates well in warm soil; midsummer "
       "sowings fail because long days and high temperatures make it bolt.")],
     G + "[0]",
     [("sare_necphm_arugula", URL["sare_arugula"], "Optimum germination is 75°."),
      ("steiner_2010_arugula", URL["steiner"], "possess satisfactory germination (more than 94%)"),
      ("steiner_2010_arugula", URL["steiner"], "ranging from 10 to 35 oc"),
      ("sare_necphm_arugula", URL["sare_arugula"], "Arugula bolts due to longer days and high temperatures.")],
     None),
    ("arugula", G + "[0].text_beginner",
     [("Arugula sprouts quickly, even in cold soil, but not in hot soil, so do not sow in the heat of summer.",
       "Arugula sprouts quickly in cold or warm soil, but long, hot days make it flower early, so do not sow in the "
       "heat of summer.")],
     G + "[0]",
     [("steiner_2010_arugula", URL["steiner"], "possess satisfactory germination (more than 94%)"),
      ("sare_necphm_arugula", URL["sare_arugula"], "Arugula bolts due to longer days and high temperatures.")],
     None),
    ("arugula", "start_method.notes_seasoned",
     [("since warm soil above about 80°F cuts germination and lengthening warm days bolt the crop",
       "since long days and high temperatures bolt the crop")], None,
     [("sare_necphm_arugula", URL["sare_arugula"], "Arugula bolts due to longer days and high temperatures.")],
     "evidence-only"),
    ("arugula", "start_method.notes_beginner",
     [("because heat keeps the seeds from sprouting well and makes the plants bolt",
       "because long, hot days make the plants bolt")], None,
     [("sare_necphm_arugula", URL["sare_arugula"], "Arugula bolts due to longer days and high temperatures.")],
     "evidence-only"),
    # live: cilantro's 75°F leaves the germination tip (moved to a bolting tip, TIP_ADDS)
    ("cilantro-coriander", G + "[tip_id=tip_cil_germ1].text_seasoned",
     [(" Sow shallowly into cool, moist soil, since warm soil above about 75°F slows germination and pushes early "
       "bolting.", " Sow shallowly into cool, moist soil.")], None, [], "struck"),
    # live: viola re-anchored to UF; the unsupported light claim dropped
    ("viola", G + "[0].text_seasoned",
     [("warm soil and light both inhibit viola germination", "viola seed germinates only in that cool range")],
     G + "[0]",
     [("uf_ifas", URL["uf_pansies"], "they only germinate at temperatures between 65˚ and 75˚Fahrenheit")], None),
    ("viola", G + "[0].text_beginner",
     [("Warm soil and light both keep the seeds from sprouting", "Warm soil keeps the seeds from sprouting")],
     G + "[0]",
     [("uf_ifas", URL["uf_pansies"], "they only germinate at temperatures between 65˚ and 75˚Fahrenheit")], None),
    # live: borage's heat clause dropped
    ("borage", G + "[1].text_seasoned", [(", since borage struggles in extreme summer heat", "")], None, [],
     "struck"),
    # live: spinach's two tips re-anchored from the evidence file
    ("spinach", G + "[0].text_seasoned",
     [("spinach germinates from about 40°F and reliably at 60 to 70°F, but poorly above 75 to 85°F",
       "spinach germinates best at 55 to 65°F, soil above 80°F reduces germination, and soil above 85°F inhibits "
       "it")], G + "[0]",
     [("usu_ext", URL["usu_spinach"], "Seeds germinate best at 55-65 degrees F"),
      ("usu_ext", URL["usu_spinach"], "Temperatures above 80 ° F reduce seed germination."),
      ("clemson_hgic", URL["clemson_spinach"], "Soil temperature above 85 °F will inhibit seed germination.")],
     None),
    ("spinach", G + "[1].text_seasoned",
     [("For the fall crop, pre-sprout or water the furrow to cool it, or wait for soil to drop below 75°F, since "
       "warm soil is the main cause of poor late-summer stands.",
       "For a summer or fall sowing, chill the seed in the refrigerator for 1 or 2 weeks before planting, and stop "
       "spring sowings once outdoor temperatures reach 80°F.")], G + "[1]",
     [("uiuc_ext", URL["uiuc_spinach"], "Chill seeds for summer or fall plantings in the refrigerator for 1 or 2 "
                                        "weeks before planting."),
      ("umn_ext", URL["umn_spinach"], "plant spinach seeds every one to two weeks, until outdoor temperatures "
                                      "reach 80°F.")], None),
    ("spinach", G + "[1].text_beginner",
     [("If you sow in late summer for fall, wait until the soil cools down, because spinach seeds will not come up "
       "well in hot soil.",
       "For a summer or fall sowing, keep the seed in the refrigerator for a week or two first, and stop spring "
       "sowings once the weather reaches 80°F.")], G + "[1]",
     [("uiuc_ext", URL["uiuc_spinach"], "Chill seeds for summer or fall plantings in the refrigerator for 1 or 2 "
                                        "weeks before planting."),
      ("umn_ext", URL["umn_spinach"], "plant spinach seeds every one to two weeks, until outdoor temperatures "
                                      "reach 80°F.")], None),
    # live: celery's unsupported drought-bolting clause struck
    ("celery", "weather_triggers[condition=HEAT_STRESS].body_seasoned",
     [("coarsens stalks, turns them bitter, and combined with drought can trigger bolting.",
       "coarsens stalks and turns them bitter.")], None,
     [("tamu_celery_crop_sheet", URL["tamu_celery"], "Average high temperature above 75°F in month preceding "
                                                      "harvest limits vegetative growth and quality.")],
     "evidence-only"),
    ("celery", "weather_triggers[condition=HEAT_STRESS].body_beginner",
     [("celery gets tough and bitter and may bolt (run to seed), especially if it also gets dry.",
       "celery gets tough and bitter.")], None, [], "struck"),
]

# ---------------------------------------------------------------- citation additions on touched tips
# (crop, block, {id: url}) -- the ids join the block's sources + anchoring_urls (created if absent)
CITES = [
    ("broccoli", "tips_by_stage.head_forming[0]", {"umn_ext": URL["umn_broccoli"], "usu_ext": URL["usu_broccoli"]}),
    ("cauliflower", "tips_by_stage.curd_forming[1]", {"usu_ext": URL["usu_cauliflower"]}),
    ("lettuce-leaf", G + "[0]", {"usu_ext": URL["usu_leafy"]}),
    ("arugula", G + "[0]", {"sare_necphm_arugula": URL["sare_arugula"], "steiner_2010_arugula": URL["steiner"]}),
    ("viola", G + "[0]", {"uf_ifas": URL["uf_pansies"], "ufifas_ext": URL["uf_fp609"]}),
    ("calendula", G + "[1]", {"eberle_2014_calendula": URL["eberle"]}),
    ("spinach", G + "[0]", {"usu_ext": URL["usu_spinach"], "clemson_hgic": URL["clemson_spinach"]}),
    ("spinach", G + "[1]", {"uiuc_ext": URL["uiuc_spinach"], "umn_ext": URL["umn_spinach"]}),
]
# evidence for an id added to a block whose text did not change (the id supports an existing clause)
CITE_EVIDENCE = [
    ("lettuce-leaf", G + "[0]", "usu_ext", URL["usu_leafy"],
     "Soil temperatures above 80 °F cause the seeds of some crops (lettuce, spinach, others) to go dormant"),
    ("viola", G + "[0]", "ufifas_ext", URL["uf_fp609"], "Cover the seed to exclude light."),
    ("calendula", G + "[1]", "eberle_2014_calendula", URL["eberle"],
     "stand establishment was susceptible to high soil temperatures immediately after planting in spring"),
]


def tip(tid, ts, tb, cites):
    return {"tip_id": tid, "sources": [c for c, _u in cites], "evidence_tier": "extension_backed",
            "author": {"type": "plant_team"}, "added_in": "pla750_heat_hold", "last_reviewed": V, "audience": "core",
            "anchoring_urls": {c: {"url": u, "verified": V} for c, u in cites},
            "text_seasoned": ts, "text_beginner": tb}


# ---------------------------------------------------------------- D4 + cilantro: new tips
# (crop, stage, tip, [(source_id, url, quote)])
TIP_ADDS = [
    ("brussels-sprouts", "sprout_formation",
     tip("tip_bru_heat1",
         "Heat while the sprouts form costs quality: high summer temperatures decrease sprout quality and cause "
         "internal tipburn, and plants maturing in hot, dry weather may turn bitter or fail to form compact "
         "sprouts. Keep plants well watered through hot spells.",
         "Hot weather while the sprouts form makes them worse: they can turn bitter, stay loose, or brown inside. "
         "Keep the plants well watered when it is hot.",
         [("usu_ext", URL["usu_brussels"]), ("umd_ext", URL["umd_brussels"]), ("clemson_hgic", URL["clemson_brussels"])]),
     [("usu_ext", URL["usu_brussels"], "High summer temperatures reduce plant growth, decrease sprout quality, and "
                                       "cause internal tipburn."),
      ("umd_ext", URL["umd_brussels"], "Plants maturing in hot and dry conditions may develop bitterness or fail to "
                                       "form compact sprouts."),
      ("clemson_hgic", URL["clemson_brussels"], "Keep them well-watered during the hot days of August and "
                                                "September.")]),
    ("cabbage", "head_forming",
     tip("tip_cab_heat1",
         "Cabbage grows best when temperatures stay below about 80°F, so time a spring crop to be harvested before "
         "the weather turns hot; a fall crop seeded in early July forms its head as summer turns to fall.",
         "Cabbage likes it cool while the head grows, below about 80°F. Pick spring cabbage before hot weather sets "
         "in. Cabbage seeded in early July forms its head as the weather cools in fall.",
         [("usu_ext", URL["usu_cabbage"]), ("clemson_hgic", URL["clemson_cabbage"]), ("umn_ext", URL["umn_cabbage"])]),
     [("usu_ext", URL["usu_cabbage"], "Cabbage grows best when temperatures do not exceed 80°F"),
      ("clemson_hgic", URL["clemson_cabbage"], "cabbages must be planted early enough to ensure that they are "
                                               "harvested before temperatures become too hot."),
      ("umn_ext", URL["umn_cabbage"], "A July planting will begin to form a head as summer turns to fall")]),
    ("kale", "harvest",
     tip("tip_kal_heat1",
         "For the spring crop, harvest before the weather turns hot and dry: heat slows growth and the leaves "
         "become tough and strong-flavored. In fall, the cooler the weather, the better the flavor.",
         "Pick spring kale before hot, dry weather arrives, because heat makes the leaves tough and strong tasting. "
         "Fall kale tastes better as the weather cools.",
         [("umn_ext", URL["umn_collards_kale"])]),
     [("umn_ext", URL["umn_collards_kale"], "For the spring crop, flavor is best if you harvest the plants before "
                                            "the weather becomes hot and dry."),
      ("umn_ext", URL["umn_collards_kale"], "Heat will slow growth and leaves will become tough and "
                                            "strong-flavored."),
      ("umn_ext", URL["umn_collards_kale"], "For the fall crop, the cooler the weather, the better the flavor")]),
    ("collards", "harvest",
     tip("tip_col_heat1",
         "Collards handle heat better than kale, but for the spring crop flavor is still best if you harvest before "
         "the weather turns hot and dry; heat slows growth and makes the leaves tough and strong-flavored.",
         "Collards take heat better than kale, but spring collards still taste best picked before hot, dry weather, "
         "which makes the leaves tough and strong tasting.",
         [("umd_ext", URL["umd_leafy"]), ("umn_ext", URL["umn_collards_kale"])]),
     [("umd_ext", URL["umd_leafy"], "Collards are more heat-tolerant than kale or turnip greens."),
      ("umn_ext", URL["umn_collards_kale"], "For the spring crop, flavor is best if you harvest the plants before "
                                            "the weather becomes hot and dry."),
      ("umn_ext", URL["umn_collards_kale"], "Heat will slow growth and leaves will become tough and "
                                            "strong-flavored.")]),
    ("cilantro-coriander", "established",
     tip("tip_cil_bolt2",
         "To slow bolting, keep the soil below about 75°F: mulch to keep it cool, water well, and keep plants away "
         "from a heat source or a window that gets hot.",
         "To keep cilantro from flowering early, keep its soil cool, under about 75°F. Mulch it, water it well, and "
         "keep it away from heaters and hot windows.",
         [("usu_ext", URL["usu_cilantro"])]),
     [("usu_ext", URL["usu_cilantro"], "Try to keep the soil temperature below 75°F, especially if grown near a heat "
                                       "source or a particular window that becomes quite warm"),
      ("usu_ext", URL["usu_cilantro"], "Mulch the soil to keep it cool and make sure the plant is well watered.")]),
]

# ---------------------------------------------------------------- struck weather triggers
# (crop, selector key, value, why)
TRIGGER_DROPS = [
    ("edamame", "condition", "HEAT_STRESS",
     "the trigger's figure (95 to 100°F flower and pod drop) and its snap-bean comparison are on no cited page"),
    ("chamomile", "condition", "high",
     "neither cited page (msu_bozeman, uwi_hort) mentions heat, humidity, mildew or botrytis"),
]
