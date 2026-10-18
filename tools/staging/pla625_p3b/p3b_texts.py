"""p3b_texts -- the texts and values of PLA-625 citrus promote 3b (mandarin-clementine rootstock rows), transcribed from the
claude.ai ruling (PLA-625 comment b4271661, approved by Trevor, 2026-10-16). Nothing here is authored: every sentence is
the ruling's, in the ruling's order, and each carries the keys of the cached-page quotes it rests on (the ruling's
brackets, resolved to exact spans of the hashed bytes by the clause check). An unbracketed beginner sentence carries its
seasoned twin's quotes (the promote 1 convention).

QUOTES: key -> (label, quote), a span of the page's norm_text (cited_promote_common).
SOURCES: label -> (source id, url, sha256). CH116 and FakeNorton are the ids this promote mints (ruling A).
"""

SOURCES = {
    "CH116": ("uf_ifas_ch116", "https://ask.ifas.ufl.edu/publication/CH116",
              "5100c446a76f04eb81a902f69cf0d7063758031c447efe684a327d95bf19b69c"),
    "HS1260": ("uf_ifas_hs1260", "https://ask.ifas.ufl.edu/publication/HS1260",
               "2d5d5bcd5cd1f80a6c427dbf1d8dec321d73a89ba7dac72117483c39bac1f1d7"),
    "HS132": ("uf_ifas_hs132", "https://ask.ifas.ufl.edu/publication/HS132",
              "1022a27cf8b7eeda30a87755128be2e4748e3bd9ff0465cedebb7b684e1627fe"),
    "UCR-3771": ("ucr_citrus", "https://citrusvariety.ucr.edu/crc3771",
                 "b7c86be25f532cbdf26120a88d50564bdfd388621fb12681c373a45fc5fcc0c9"),
    "TAMU": ("tamu_agrilife", "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/",
             "23a8436d1d6d0715403a0ccb640429a5818921d601d50456726d8ff34019d28a"),
    "31-018C": ("ucce_placer_nevada_31_018c", "https://ucanr.edu/sites/default/files/2020-10/63813.pdf",
                "0bc08654ed55c45d539237840b220d108a9487bb6d8d5231dcc93de84336f0c1"),
    "SantaClara": ("ucanr_santa_clara_mg", "https://ucanr.edu/sites/default/files/2020-02/319461.pdf",
                   "94c04c9338ac7a01673aaef0bc908b8dc7cd1f1374d57929b2501e4b029c7efb"),
    "AZ1001": ("az_coop_ext", "https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1001.pdf",
               "900da76c85fd9619578ec7b0da6e2cfeee44a0215838cb97c665bc6890bbfa2d"),
    "MaukShea": ("ucce_riverside_citrus_qa", "https://ucanr.edu/sites/default/files/2013-12/178097.pdf",
                 "9047f6edc73a988f32d74b5c888678944d0ec778844c535b13b8fa3d5f027ace"),
    "FakeNorton": ("ucce_placer_nevada_cold_damage",
                   "https://ucanr.edu/?legacy-file=134971.pdf&legacy-file-path=sites%2Fplacernevadasmallfarms%2Ffiles%2F",
                   "0a91abb2798941243ec6c00e6815aeb345229f6f2ee263903e54a87a23289a92"),
}

HS1260_COLUMNS = ("seed germination* seedling uniformity tree size spacing yield per tree yield per acre juice quality "
                  "fruit size salinity high ph clay soil wet soil drought freeze hlb incidence blight phytophthora "
                  "p. palmivora weevil complex burrowing nematode citrus nematode tristeza")

QUOTES = {
    # CH116 (HS195/CH116, The Satsuma Mandarin): every sentence resting on it says "satsuma" (ruling crop scope)
    "C.most": ("CH116", "trifoliate orange ( poncirus trifolata (l.) raf) is the most used rootstock for satsuma "
                        "mandarins, especially in cool climates where maximum cold tolerance is needed."),
    "C.gainesville": ("CH116", "however, in florida, where the winters can be relatively short and interrupted by brief "
                               "periods of warm temperatures, trifoliate orange does not provide consistent protection "
                               "from cold south of gainesville."),
    "C.footrot": ("CH116", "is poorly adapted to saline or calcareous conditions, but its resistance to foot rot, a "
                           "soil-borne disease, makes it a good choice for soils with poor drainage."),
    "C.fd": ("CH116", "many selections of p. trifoliata are available, including a dwarfing rootstock named 'flying "
                      "dragon'."),
    "C.seven": ("CH116", "since trees on 'flying dragon' will seldom exceed seven feet in height, mature trees can easily "
                         "be harvested without ladders."),
    "C.yield": ("CH116", "yield per year averaged 264 lbs/tree (19.2 tons/acre) for 'brown select'/'rubidoux', 218 "
                         "lbs/tree (15.8 tons/acre) for 'owari'/'rubidoux', 143 lbs/tree (10.4 tons/acre) for 'brown "
                         "select'/'flying dragon', and 107 lbs/tree (7.8 tons/acre) for 'owari'/'flying dragon'."),
    "C.yieldsize": ("CH116", "when calculating yield on the basis of tree size, yields were often similar for trees on the "
                             "two rootstocks ('rubidoux' and 'flying dragon')"),
    "C.swingle": ("CH116", "satsumas are often propagated on 'carrizo' and especially 'swingle' rootstocks. this is because "
                           "budding and early tree growth are better for satsumas on 'swingle' compared to p. trifoliata"),
    # FakeNorton (UCCE, Avoiding Cold Damage to Home Citrus)
    "N.hardy": ("FakeNorton", "satsuma mandarins on trifoliate rootstocks are the most cold hardy mandarins"),
    "N.less": ("FakeNorton", "clementines and other mandarin varieties are slightly less cold hardy"),
    "N.ucce": ("FakeNorton", "cindy fake and maxwell norton, uc cooperative extension"),
    # HS1260
    "H.cols": ("HS1260", HS1260_COLUMNS),
    "H.trif": ("HS1260", "trifoliate orange long established 80%-90% 80%-90% sm 6-8 l-i h h/h sm-i p- p- g g p i-g [s] t+ "
                         "[s] s r t+"),
    "H.fd": ("HS1260", "flying dragon tf 1978 80%-90% 80%-90% sm 5-7 l-i h h/h sm-i p p g i p g p t [i] s r t"),
    "H.swingle": ("HS1260", "swingle citrumelo 1974 >90% 95% i 8-12 i i i/i i p p p [g] p-i g i t t+ s [s] r t"),
    "H.sm_i": ("HS1260", "a small tree [sm] would be less than 8 ft tall at maturity, and an intermediate tree [i] would "
                         "be like one on c-35 citrange and range in height from 8 to 14 ft tall."),
    "H.small_yield": ("HS1260", "small trees usually produce less fruit per tree than larger trees"),
    "H.phyto": ("HS1260", "phytophthora nicotianae ratings are a combination of foot- and root-rot tolerances"),
    "H.murcott": ("HS1260", "there are just a few situations where a scion/rootstock combination, like murcott budded to "
                            "carrizo citrange or swingle citrumelo, declines from an apparent incompatibility that "
                            "manifests itself at the bud union."),
    "H.mandarins": ("HS1260", "mandarins are perhaps the most sensitive scions to incompatibility, especially with "
                              "trifoliate orange-hybrid rootstocks."),
    # TAMU
    "T.smaller": ("TAMU", "trifoliate orange is more cold-hardy than sour orange and produces a smaller tree, but it is "
                          "not well adapted to saline or highly alkaline soils."),
    # 31-018C
    "F.semi": ("31-018C", "these are rich 16-6 and rubidoux, both of which are semi-dwarfing and provide cold hardiness."),
    "F.slow": ("31-018C", "use the lower recommended amounts for trees on trifoliate rootstocks, which grow slowly."),
    "F.taste": ("31-018C", "blind taste tests of mountain mandarins® over many years have shown that the flavor profile of "
                           "trifoliate fruit is more desirable."),
    "F.fd": ("31-018C", "another trifoliate rootstock, flying dragon, has a greater dwarfing effect (~75%) and is well "
                        "suited for home-use or container citrus, but not for production orchards."),
    "F.moved": ("31-018C", "containerized trees in wine barrels or tubs can be moved next to south facing walls, or "
                           "indoors for protection in cold weather."),
    # SantaClara
    "S.fd": ("SantaClara", "only true dwarfing rootstock is flying dragon. tree will be 4-8 feet tall."),
    # MaukShea
    "M.iron": ("MaukShea", "in the desert, trifoliate orange typically will have iron deficiency and th erefore other "
                           "rootstocks are better suited under these conditions."),
    # AZ1001
    "Z.tag": ("AZ1001", "be sure the tree has a tag which identifies both the variety and the rootstock"),
    # HS132
    "K.retail": ("HS132", "rootstocks are not usually a choice at retail nurseries and garden centers since they are "
                          "grafted to industry standard rootstocks."),
    # UCR-3771
    "U.parent": ("UCR-3771", "'duncan' grapefruit x poncirus trifoliata"),
    "U.most": ("UCR-3771", "these attributes lead 'swingle' to become the mostly highly utilized rootstock in florida"),
    "U.resist": ("UCR-3771", "resistant to tristeza and phytophthora foot rot, blight, cold, and citrus nematode"),
    "U.soil": ("UCR-3771", "'swingle' is moderatlely salt tolerant but is not adapted to heavy clay soils or calcareous "
                           "soils."),
}

MA = "mandarin-clementine"
TRIF, FD, SW = "Trifoliate orange (Poncirus trifoliata)", "Flying Dragon trifoliate", "Swingle citrumelo"
H_T, H_F, H_S = ["H.cols", "H.trif"], ["H.cols", "H.fd"], ["H.cols", "H.swingle"]

ROWS = [
    {"name": TRIF,
     "prose": {
         "traits_seasoned": [
             ("UF/IFAS calls trifoliate orange the most used rootstock for satsuma, especially in cool climates where the "
              "most cold tolerance is needed.", ["C.most"]),
             ("UC Cooperative Extension notes that satsumas on trifoliate are the most cold-hardy mandarins, and that "
              "clementines and other mandarins are slightly less hardy.", ["N.hardy", "N.less", "N.ucce"]),
             ("In Florida, UF/IFAS notes it does not give consistent cold protection south of Gainesville, where winters "
              "are short and broken by warm spells.", ["C.gainesville"]),
             ("Its resistance to foot rot makes it a good choice for poorly drained soils.", ["C.footrot"]),
             ("UF/IFAS rates it tolerant of tristeza.", H_T),
             ("It produces a smaller tree that grows slowly.", ["T.smaller", "F.slow"]),
             ("Its Rubidoux and Rich 16-6 selections are semi-dwarfing and provide cold hardiness.", ["F.semi"]),
             ("Fruit quality is high.", H_T + ["F.taste"]),
             ("It is poorly adapted to saline, calcareous or highly alkaline soils, and in the desert it typically "
              "develops iron deficiency.", ["C.footrot", "T.smaller", "M.iron"]),
         ],
         "traits_beginner": [
             ("Trifoliate orange is the go-to rootstock for satsumas where winters get cold, and satsumas on it are the "
              "most cold-hardy mandarins.", ["C.most", "N.hardy"]),
             ("It resists root rot, keeps the tree smaller and gives good fruit.",
              ["C.footrot", "T.smaller"] + H_T + ["F.taste"]),
             ("It does poorly in salty or very alkaline soil, so other rootstocks suit desert gardens better.",
              ["T.smaller", "M.iron"]),
         ],
         "what_to_ask_nursery": [
             ("For a satsuma where winters get cold, ask for one on trifoliate orange, such as the Rubidoux selection.",
              ["C.most", "F.semi"]),
             ("Check that the tag names both the variety and the rootstock.", ["Z.tag"]),
             ("Confirm your soil is not highly alkaline or saline, which trifoliate dislikes.", ["T.smaller"]),
         ],
     },
     "values": {
         "size_class": ("semi_dwarf", ["F.semi"]),
         "mature_height_ft": (None, "no page gives a mandarin height; HS1260 Sm gives an upper bound only (ruling B)"),
         "spread_ft": (None, "ABSENT (ruling B)"),
         "container_suitable": (None, "was false, ABSENT (ruling B)"),
         "container_size_gallons": (None, "unchanged null"),
         "bearing_age_years": (None, "was 2, ABSENT; 31-018C says C-35 bears earlier than trifoliate (ruling B)"),
     },
     "sources": ["CH116", "HS1260", "TAMU", "31-018C", "FakeNorton", "MaukShea", "AZ1001"]},
    {"name": FD,
     "prose": {
         "traits_seasoned": [
             ("Flying Dragon is a dwarfing selection of trifoliate orange.", ["C.fd"]),
             ("UC Master Gardeners call it the only true dwarfing citrus rootstock, with trees 4 to 8 feet tall.",
              ["S.fd"]),
             ("UF/IFAS reports that satsumas on it seldom exceed seven feet, so mature trees can be harvested without "
              "ladders.", ["C.seven"]),
             ("UC Cooperative Extension calls it well suited to home and container citrus, but not to production "
              "orchards.", ["F.fd"]),
             ("UF/IFAS rates it tolerant of tristeza and Phytophthora, resistant to citrus nematode, and good in "
              "freezes.", H_F),
             ("It does poorly in saline and high-pH soils.", H_F),
             ("Its juice quality rates high, but small trees bear less fruit per tree.",
              H_F + ["H.small_yield", "C.yield"]),
             ("In a UF/IFAS satsuma trial, yields measured against tree size were often similar to those on Rubidoux.",
              ["C.yieldsize"]),
         ],
         "traits_beginner": [
             ("Flying Dragon is a dwarfing rootstock that keeps a mandarin small, usually 4 to 8 feet tall.", ["S.fd"]),
             ("That makes it a good fit for a pot or a small yard, and a potted tree can be moved to shelter in cold "
              "weather.", ["F.fd", "F.moved"]),
             ("It holds up well against tristeza virus, root rot and cold.", H_F + ["H.phyto"]),
             ("The smaller tree gives a smaller crop.", ["H.small_yield", "C.yield"]),
             ("It does poorly in salty or alkaline soil.", H_F),
         ],
         "what_to_ask_nursery": [
             ("Ask for Flying Dragon, a dwarfing selection of trifoliate orange, if you want a mandarin for a pot or a "
              "small yard.", ["C.fd", "F.fd"]),
         ],
     },
     "values": {
         "size_class": ("dwarf", ["C.fd"]),
         "mature_height_ft": ([4, 8], ["S.fd"]),
         "spread_ft": (None, "ABSENT (ruling B)"),
         "container_suitable": (True, ["F.fd"]),
         "container_size_gallons": (None, "was 15, PARTIAL: a general mandarin / satsuma minimum never tied to Flying "
                                          "Dragon, and it conflicted with the crop's min_pot_gallons of 10 (ruling B)"),
         "bearing_age_years": (None, "was 2, ABSENT (ruling B)"),
     },
     "sources": ["CH116", "SantaClara", "31-018C", "HS1260"]},
    {"name": SW,
     "prose": {
         "traits_seasoned": [
             ("Swingle is a citrumelo, a cross of Duncan grapefruit and trifoliate orange.", ["U.parent"]),
             ("UF/IFAS says satsumas are often propagated on it, because budding and early tree growth are better than "
              "on trifoliate orange.", ["C.swingle"]),
             ("It became the most widely used rootstock in Florida.", ["U.most"]),
             ("It resists Phytophthora foot rot and citrus nematode, and it tolerates tristeza virus.",
              ["U.resist"] + H_S),
             ("Its cold hardiness is good.", H_S + ["U.resist"]),
             ("UF/IFAS rates it an intermediate-size tree.", H_S + ["H.sm_i"]),
             ("It is not adapted to heavy clay or calcareous soils.", ["U.soil"]),
             ("UF/IFAS warns that mandarins are among the scions most sensitive to incompatibility with trifoliate-hybrid "
              "rootstocks, and names Murcott on Swingle as a combination that can decline.",
              ["H.mandarins", "H.murcott"]),
         ],
         "traits_beginner": [
             ("Swingle is a common rootstock, and young satsuma trees get off to a better start on it than on trifoliate "
              "orange.", ["C.swingle", "U.most"]),
             ("It resists root rot and holds up against tristeza virus and cold.", ["U.resist"] + H_S),
             ("It does poorly in heavy clay or alkaline soil.", ["U.soil"]),
             ("Some mandarins, such as Murcott, can decline on it, so check the pairing before you buy.",
              ["H.murcott", "H.mandarins"]),
         ],
         "what_to_ask_nursery": [
             ("If you are buying a Murcott, ask for a rootstock other than Swingle, since UF/IFAS lists that pairing as one "
              "that can decline.", ["H.murcott"]),
             ("Swingle is a poor match for heavy clay or alkaline soil.", ["U.soil"] + H_S),
         ],
     },
     "values": {
         "size_class": ("semi_dwarf", H_S + ["H.sm_i"]),
         "mature_height_ft": ([8, 14], H_S + ["H.sm_i"]),
         "spread_ft": (None, "was [8, 12], which equals HS1260's in-row Spacing, not spread (ruling B)"),
         "container_suitable": (None, "was false, ABSENT (ruling B)"),
         "container_size_gallons": (None, "unchanged null"),
         "bearing_age_years": (None, "was 3, ABSENT (ruling B)"),
     },
     "sources": ["UCR-3771", "CH116", "HS1260"]},
]

RECOMMENDED = (None, "was Trifoliate orange, PARTIAL: the one source recommendation is satsuma-only and climate-bound, and "
                     "trifoliate is a poor match in alkaline and desert soils (ruling C)")

NOTE = [
    ("Rootstocks are usually not a choice at retail garden centers, because trees come grafted onto industry-standard "
     "rootstocks.", ["K.retail"]),
    ("Check that the tag names both the variety and the rootstock.", ["Z.tag"]),
    ("Where winters get cold, trifoliate orange is the most used rootstock for satsumas, and satsumas on it are the most "
     "cold-hardy mandarins.", ["C.most", "N.hardy"]),
    ("Trifoliate does poorly in saline or highly alkaline soil, and in the desert it typically develops iron deficiency.",
     ["T.smaller", "M.iron"]),
    ("For a pot or a small yard, Flying Dragon makes a dwarf tree.", ["F.fd"]),
    ("UF/IFAS lists Murcott on Swingle citrumelo as a combination that can decline.", ["H.murcott"]),
]
NOTE_SOURCES = ["HS132", "AZ1001", "CH116", "FakeNorton", "TAMU", "MaukShea", "31-018C", "HS1260"]

CATALOG = {
    "uf_ifas_ch116": {
        "id": "uf_ifas_ch116", "name": "UF/IFAS The Satsuma Mandarin (HS195/CH116)", "title": "The Satsuma Mandarin",
        "publisher": "UF/IFAS Extension", "url": "https://ask.ifas.ufl.edu/publication/CH116",
        "source_class": "university_extension", "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UF/IFAS EDIS publication CH116 (HS195) on the satsuma mandarin: history, cultivars, cold "
                       "tolerance, rootstocks for satsuma (trifoliate orange, Flying Dragon, Swingle, Carrizo) and a "
                       "North Florida Flying Dragon / Rubidoux satsuma trial. Satsuma-scoped: a sentence resting on it says "
                       "satsuma. A document-scoped child of uf_ifas_edis (PLA-625 promote 3b, ruling A)."},
    "ucce_placer_nevada_cold_damage": {
        "id": "ucce_placer_nevada_cold_damage",
        "name": "Fake, C. & Norton, M., Avoiding Cold Damage to Home Citrus, UC Cooperative Extension Placer/Nevada",
        "title": "Avoiding Cold Damage to Home Citrus", "publisher": "UC Cooperative Extension (Placer and Nevada Counties)",
        "url": "https://ucanr.edu/?legacy-file=134971.pdf&legacy-file-path=sites%2Fplacernevadasmallfarms%2Ffiles%2F",
        "source_class": "university_extension", "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UCCE Placer/Nevada home-citrus cold guide (Cindy Fake, Maxwell Norton): frost preparation, and "
                       "relative cold hardiness (satsumas on trifoliate are the most cold-hardy mandarins; clementines and "
                       "other mandarins slightly less). PLA-625 promote 3b, ruling A (FakeNorton)."},
}

# ruling A: dropped credits (guard H)
DROPPED = {TRIF: ["uga_ext"], FD: ["tamu_agrilife"], SW: ["uf_ifas_hs132", "tamu_agrilife"]}
