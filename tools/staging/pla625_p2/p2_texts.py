"""p2_texts -- the texts and values of PLA-625 citrus promote 2 (lemon + lime rootstock rows), transcribed from the
claude.ai ruling (PLA-625 comment abaa4aa8, approved by Trevor, 2026-10-14). Nothing here is authored: every sentence is
the ruling's, in the ruling's order, and each carries the keys of the cached-page quotes it rests on (the ruling's
brackets, resolved to exact spans of the hashed bytes by the clause check). An unbracketed beginner sentence carries its
seasoned twin's quotes (the promote 1 convention).

QUOTES: key -> (label, quote), a span of the page's norm_text (cited_promote_common), checked again by the promote's
guard E against the MANIFEST bytes.
SOURCES: label -> (source id, url, sha256). CH092, CH093 and HS1260 are the ids minted by ruling A.1.
"""

SOURCES = {
    "CH092": ("uf_ifas_ch092", "https://ask.ifas.ufl.edu/publication/CH092",
              "e07230d4815d6bd180cf9366ba01375039e22f3a0fb7f535444f965c7c00379d"),
    "CH093": ("uf_ifas_ch093", "https://ask.ifas.ufl.edu/publication/CH093",
              "6fc9a10b6b331b5676fb16be747852eb56ffeecc9077aeca44cb6aaf4f9e92fa"),
    "HS1260": ("uf_ifas_hs1260", "https://ask.ifas.ufl.edu/publication/HS1260",
               "2d5d5bcd5cd1f80a6c427dbf1d8dec321d73a89ba7dac72117483c39bac1f1d7"),
    "HS402": ("uf_ifas_hs1153", "https://edis.ifas.ufl.edu/publication/HS402",
              "15801f6dc90c756b97102f8e2cd347ff30d9cb41b87fec4ba69bfeebb8246ea5"),
    "HS132": ("uf_ifas_hs132", "https://ask.ifas.ufl.edu/publication/HS132",
              "1022a27cf8b7eeda30a87755128be2e4748e3bd9ff0465cedebb7b684e1627fe"),
    "TAMU": ("tamu_agrilife", "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/",
             "23a8436d1d6d0715403a0ccb640429a5818921d601d50456726d8ff34019d28a"),
    "UCR-3771": ("ucr_citrus", "https://citrusvariety.ucr.edu/crc3771",
                 "b7c86be25f532cbdf26120a88d50564bdfd388621fb12681c373a45fc5fcc0c9"),
    "31-018C": ("ucce_placer_nevada_31_018c", "https://ucanr.edu/sites/default/files/2020-10/63813.pdf",
                "0bc08654ed55c45d539237840b220d108a9487bb6d8d5231dcc93de84336f0c1"),
    "ANR8100": ("uc_anr_8100", "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf",
                "efbfe5dc93eee7cc876804056d8e99f2dc5ed0d2f6620e58846ed8a153f4c347"),
}

HS1260_COLUMNS = ("seed germination* seedling uniformity tree size spacing yield per tree yield per acre juice quality "
                  "fruit size salinity high ph clay soil wet soil drought freeze hlb incidence blight phytophthora "
                  "p. palmivora weevil complex burrowing nematode citrus nematode tristeza")

QUOTES = {
    # HS1260 (SP248, 5th ed.). Scope on every use: Florida commercial groves; relative vigor; averaged across commercial
    # scions; not scion-specific (promote 1 ruling A.1).
    "H.cols": ("HS1260", HS1260_COLUMNS),
    "H.sour": ("HS1260", "sour orange long established >90% 91% i-lg 8-12 i-h i-h h+/h i g g g g+ i g l t+ t t s s s"),
    "H.swingle": ("HS1260", "swingle citrumelo 1974 >90% 95% i 8-12 i i i/i i p p p [g] p-i g i t t+ s [s] r t"),
    "H.rough": ("HS1260", "rough lemon long established 80%-90% 80%-90% lg 10-15 h i-h l/l lg i g i i g p s s s s s t"),
    "H.volk": ("HS1260", "volkamer lemon 1970 >90% 98% lg 12-15 h i-h l/l lg i t i i-g g p s t [s] s s t"),
    "H.vigor": ("HS1260", "tree size refers to the size of the canopy of a mature tree. the ratings indicate relative "
                          "tree vigor."),
    "H.lg": ("HS1260", "a tree on a selected rootstock would be rated large [lg] if it was comparable in vigor and size "
                       "to one on cleopatra mandarin or rough lemon, i.e., perhaps 14-20 ft tall."),
    "H.sm_i": ("HS1260", "a small tree [sm] would be less than 8 ft tall at maturity, and an intermediate tree [i] would "
                         "be like one on c-35 citrange and range in height from 8 to 14 ft tall."),
    # HS402 (uf_ifas_hs1153), lemon
    "L.soiltype": ("HS402", "recommended rootstocks vary with soil type"),
    "L.sandy": ("HS402", "trees planted on acid to neutral sandy soils do well on swingle citrumelo"),
    "L.calc": ("HS402", "trees to be planted in the high-ph, calcareous soils of south miami-dade county should be "
                        "grafted onto rough lemon ( c. jamhiri ) or macrophylla ( c. macrophylla )"),
    "L.used": ("HS402", "rootstocks used include rough lemon ( c. jambhiri ), 'cleopatra mandarin' ( c. reticulata ), "
                        "volkamer lemon ( c. volkameriana ), sour orange ( c. aurantium ) and macrophylla "
                        "( c. macrophylla )"),
    "L.rough": ("HS402", "trees on rough lemon rootstocks are extremely vigorous and susceptible to foot rot "
                         "(phytophthora)."),
    "L.macro": ("HS402", "trees on macrophylla are also very vigorous and susceptible to tristeza, hence rootstock sprout "
                         "removal is important to preclude infection."),
    "L.aphid": ("HS402", "the brown citrus aphid is a vector of citrus tristeza virus, which causes tree decline and death "
                         "of citrus on susceptible rootstocks (e.g., sour orange, alemeow)."),
    "L.browning": ("HS402", "resistance to foot rot varies by rootstock with trifoliate orange immune; swingle citrumelo, "
                            "cleopatra mandarin, and sour orange resistant; troyer and carrizo citranges and rangur lime "
                            "tolerant; and sweet orange and rough lemon highly susceptible"),
    "L.tristeza": ("HS402", "lemons are susceptible to severe tristeza virus strains regardless of rootstock, and less "
                            "severe strains when propagated on citrus macrophylla (macrophylla) and rough lemon ( c. "
                            "jambhiri ) rootstocks."),
    "L.cert": ("HS402", "purchasing certified disease-free trees under the florida budwood registration program will "
                        "greatly reduce the chances of purchasing a tree with this disease."),
    # CH092 (key lime)
    "K92.seed": ("CH092", "key lime is frequently propagated from seed since it is true-to-type due to its high degree "
                          "of polyembryony"),
    "K92.other": ("CH092", "key lime may also be propagated by hard wood cuttings, air-layers, or as budded or grafted "
                           "trees."),
    "K92.calc": ("CH092", "rootstocks suitable for key lime grown in calcareous soils include alemow ( c. macrophylla ), "
                          "rough lemon ( citrus jambhuri ), volkamer lemon (volk) ( c. volkameriana )"),
    "K92.tristeza": ("CH092", "key limes are susceptible to tristeza virus regardless of rootstock."),
    # CH093 (Tahiti lime)
    "K93.select": ("CH093", "select the appropriate rootstock for the soil type in your landscape."),
    "K93.calc": ("CH093", "appropriate rootstocks for grafted trees to be grown in high-ph, calcareous soils (rockland and "
                          "some sandy soils) include the following: rough lemon ( citrus jambhuri ), alemow ( c. "
                          "macrophylla ), rangpur lime ( c. limonia ), volkamer lemon ( c. volkameriana )"),
    "K93.swingle": ("CH093", "a rootstock appropriate for low-ph or neutral soils is swingle citrumelo ( c. paradise "
                             "'duncan' x poncirus trifoliate )."),
    "K93.flood": ("CH093", "air-layered and trees grafted onto alemow tolerate a few days of excessively wet or flooded "
                           "soil conditions"),
    "K93.aphid": ("CH093", "the brown citrus aphid is a major vector of citrus tristeza virus (ctv) and may cause tree "
                           "decline and death of 'tahiti' lime trees on susceptible rootstocks (e.g., sour orange, "
                           "alemeow)."),
    "K93.browning": ("CH093", "swingle citrumelo, cleopatra mandarin, and sour orange are resistant. troyer and carrizo "
                              "citranges and rangur lime are tolerant. sweet orange and rough lemon are highly susceptible"),
    "K93.severe": ("CH093", "'tahiti' limes may be susceptible to severe tristeza virus strains, regardless of rootstock."),
    "K93.less": ("CH093", "however, these trees may be susceptible to less-severe strains when propagated on citrus "
                          "macrophylla (macrophylla) and rough lemon ( c. jambhiri ) rootstocks"),
    # HS132
    "K.retail": ("HS132", "rootstocks are not usually a choice at retail nurseries and garden centers since they are "
                          "grafted to industry standard rootstocks."),
    # TAMU
    "T.common": ("TAMU", "sour orange, the most common rootstock in texas, is well-adapted to most soil conditions in "
                         "which citrus is grown."),
    "T.trif": ("TAMU", "trifoliate orange is more cold-hardy than sour orange and produces a smaller tree, but it is not "
                       "well adapted to saline or highly alkaline soils."),
    "T.pref": ("TAMU", "trifoliate orange is preferred for the upper gulf coast and colder areas where soil conditions "
                       "are suitable, but sour orange is recommended for the lower coast and most of southern texas."),
    "T.tristeza": ("TAMU", "tristeza is a virus disease that kills citrus trees quickly, particularly those growing on "
                           "sour orange rootstock."),
    # UCR-3771
    "U.parent": ("UCR-3771", "'duncan' grapefruit x poncirus trifoliata"),
    "U.most": ("UCR-3771", "these attributes lead 'swingle' to become the mostly highly utilized rootstock in florida"),
    "U.lisbon": ("UCR-3771", "'swingle' was observed to be particularly well adapted for use with grapefruits and in some "
                             "cases 'lisbon'-type lemons."),
    "U.resist": ("UCR-3771", "resistant to tristeza and phytophthora foot rot, blight, cold, and citrus nematode"),
    "U.soil": ("UCR-3771", "'swingle' is moderatlely salt tolerant but is not adapted to heavy clay soils or calcareous "
                           "soils."),
    # 31-018C
    "F.semi": ("31-018C", "a semi- dwarfing rootstock such as trifoliate"),
    # ANR8100
    "A.rough": ("ANR8100", "rough lemon or alemow citrus macrophylla h"),
    "A.key": ("ANR8100", "h = high sensitivity"),
}

LEMON, LIME = "lemon", "lime"
H_SOUR = ["H.cols", "H.sour"]
H_SW = ["H.cols", "H.swingle"]

# One entry per row, in list order. `old` is the base row name; `name` the post name (None = unchanged); `new` marks a
# row the ruling adds. prose: field -> [(sentence, quote keys)]. values: field -> (value, quote keys) or (None, reason).
ROWS = {
    LEMON: [
        {"old": "sour orange (Citrus aurantium)", "name": None, "new": False,
         "prose": {
             "traits_seasoned": [
                 ("Sour orange is one of the rootstocks UF/IFAS lists for lemons.", ["L.used"]),
                 ("It is the most common rootstock in Texas and adapts to most soils that citrus is grown in.",
                  ["T.common"]),
                 ("UF/IFAS rates it good in saline, high-pH and clay soils.", H_SOUR),
                 ("It resists Phytophthora foot rot.", ["L.browning"]),
                 ("Tristeza virus can kill citrus trees quickly on sour orange rootstock.", ["T.tristeza", "L.aphid"]),
                 ("Lemons are susceptible to severe tristeza strains whatever the rootstock.", ["L.tristeza"]),
                 ("Texas A&M recommends it for the lower Texas coast and most of southern Texas.", ["T.pref"]),
             ],
             "traits_beginner": [
                 ("Sour orange is a long-established rootstock that handles most soils and resists foot rot.",
                  H_SOUR + ["T.common", "L.browning"]),
                 ("Its weak spot is tristeza, a virus spread by aphids that can kill trees on sour orange quickly.",
                  ["L.aphid", "T.tristeza"]),
             ],
             "what_to_ask_nursery": [
                 ("Retail citrus usually comes already grafted, so ask which rootstock your tree is on.", ["K.retail"]),
                 ("Buy a certified disease-free tree.", ["L.cert"]),
             ],
         },
         "values": {
             "size_class": (None, "HS1260 'I-Lg' is an undefined form; PLA-567 A.3/A.4 (ruling C)"),
             "mature_height_ft": (None, "unchanged null (ruling C)"),
             "spread_ft": (None, "unchanged null (ruling C)"),
             "container_suitable": (None, "was false; ABSENT on every page read (ruling C)"),
             "container_size_gallons": (None, "unchanged null (ruling C)"),
             "bearing_age_years": (None, "unchanged null (ruling C)"),
         },
         "sources": ["HS402", "TAMU", "HS1260", "HS132"]},
        {"old": "trifoliate orange (Citrus trifoliata)", "name": None, "new": False,
         "prose": {
             "traits_seasoned": [
                 ("Trifoliate orange is more cold-hardy than sour orange and makes a smaller tree.", ["T.trif"]),
                 ("UC Cooperative Extension calls it semi-dwarfing.", ["F.semi"]),
                 ("It is immune to Phytophthora foot rot.", ["L.browning"]),
                 ("It is not well adapted to saline or highly alkaline soils.", ["T.trif"]),
                 ("Texas A&M prefers it for colder areas where the soil suits it.", ["T.pref"]),
             ],
             "traits_beginner": [
                 ("Trifoliate orange handles cold better than sour orange and keeps the tree somewhat smaller.",
                  ["T.trif", "F.semi"]),
                 ("It does not get foot rot, but it struggles in salty or very alkaline soil.",
                  ["L.browning", "T.trif"]),
             ],
             "what_to_ask_nursery": [
                 ("In a colder area with soil that is not salty or alkaline, ask whether the tree is on trifoliate "
                  "orange.", ["T.pref", "T.trif"]),
             ],
         },
         "values": {
             "size_class": ("semi_dwarf", ["F.semi"]),
             "mature_height_ft": (None, "no home-garden height; HS1260 Sm gives an upper bound only (ruling C)"),
             "spread_ft": (None, "unchanged null"),
             "container_suitable": (None, "unchanged null (ruling C)"),
             "container_size_gallons": (None, "unchanged null"),
             "bearing_age_years": (None, "unchanged null"),
         },
         "sources": ["TAMU", "HS402", "31-018C"]},
        {"old": "Carrizo / Swingle citrumelo (trifoliate hybrids)", "name": "Swingle citrumelo", "new": False,
         "prose": {
             "traits_seasoned": [
                 ("Swingle is a citrumelo, a cross of Duncan grapefruit and trifoliate orange.", ["U.parent"]),
                 ("UF/IFAS says lemons on acid to neutral sandy soils do well on it.", ["L.sandy"]),
                 ("UC Riverside found it well adapted in some cases to Lisbon-type lemons.", ["U.lisbon"]),
                 ("It resists Phytophthora foot rot and citrus nematode, and it tolerates tristeza virus.",
                  ["U.resist"] + H_SW),
                 ("Its cold hardiness is good.", H_SW + ["U.resist"]),
                 ("It is not adapted to heavy clay or calcareous soils.", ["U.soil"]),
             ],
             "traits_beginner": [
                 ("Swingle is a common rootstock for lemons on sandy soil that is not alkaline.",
                  ["U.most", "L.sandy"]),
                 ("It resists foot rot and holds up against tristeza virus and cold.", ["U.resist"] + H_SW),
                 ("It does poorly in heavy clay or alkaline soil.", ["U.soil"]),
             ],
             "what_to_ask_nursery": [
                 ("On sandy soil that is acid to neutral, ask whether the tree is on Swingle citrumelo.", ["L.sandy"]),
             ],
         },
         "values": {
             "size_class": ("semi_dwarf", H_SW + ["H.sm_i"]),
             "mature_height_ft": ([8, 14], H_SW + ["H.sm_i"]),
             "spread_ft": (None, "unchanged null"),
             "container_suitable": (None, "unchanged null (ruling C)"),
             "container_size_gallons": (None, "unchanged null"),
             "bearing_age_years": (None, "unchanged null"),
         },
         "sources": ["UCR-3771", "HS402", "HS1260"]},
        {"old": None, "name": "Rough lemon / macrophylla (alemow)", "new": True,
         "prose": {
             "traits_seasoned": [
                 ("UF/IFAS recommends rough lemon or macrophylla (alemow) for lemons in high-pH, calcareous soils.",
                  ["L.calc", "A.rough"]),
                 ("Trees on either rootstock are very vigorous.", ["L.rough", "L.macro"]),
                 ("Rough lemon is susceptible to Phytophthora foot rot.", ["L.rough"]),
                 ("Lemons on these rootstocks are susceptible to less-severe tristeza strains as well as severe ones.",
                  ["L.tristeza"]),
                 ("Because macrophylla is susceptible to tristeza, UF/IFAS says removing rootstock sprouts is "
                  "important.", ["L.macro"]),
                 ("UC rates both as highly sensitive to frost.", ["A.rough", "A.key"]),
             ],
             "traits_beginner": [
                 ("These are vigorous rootstocks for alkaline soil.", ["L.calc", "L.rough", "L.macro"]),
                 ("They are more prone to tristeza virus, rough lemon is prone to foot rot, and both are very sensitive "
                  "to frost.", ["L.tristeza", "L.rough", "A.rough", "A.key"]),
                 ("Pull off any shoots that sprout from below the graft.", ["L.macro"]),
             ],
             "what_to_ask_nursery": [
                 ("If your soil is alkaline, ask whether the tree is on rough lemon or macrophylla.", ["L.calc"]),
             ],
         },
         "values": {
             "size_class": (None, "mixed: rough lemon is Lg; macrophylla has no HS1260 row (ruling C)"),
             "mature_height_ft": (None, "ruling C"),
             "spread_ft": (None, "ruling C"),
             "container_suitable": (None, "ruling C"),
             "container_size_gallons": (None, "ruling C"),
             "bearing_age_years": (None, "ruling C"),
         },
         "sources": ["HS402", "ANR8100"]},
    ],
    LIME: [
        {"old": "rough lemon / Volkamer lemon (Citrus jambhiri, C. volkameriana)", "name": None, "new": False,
         "prose": {
             "traits_seasoned": [
                 ("UF/IFAS lists rough lemon and Volkamer lemon among rootstocks for limes in high-pH, calcareous "
                  "soils, including rockland and some sandy soils.", ["K93.calc", "K92.calc"]),
                 ("Trees on rough lemon are extremely vigorous.", ["L.rough"]),
                 ("Rough lemon is highly susceptible to Phytophthora foot rot.", ["K93.browning"]),
                 ("UF/IFAS rates both as large trees under Florida grove conditions.",
                  ["H.cols", "H.rough", "H.volk", "H.vigor", "H.lg"]),
                 ("On rough lemon, Tahiti limes may also be susceptible to less-severe tristeza strains.",
                  ["K93.less"]),
             ],
             "traits_beginner": [
                 ("A vigorous rootstock for alkaline soil, including rocky ground and some sandy soils.",
                  ["K93.calc", "L.rough"]),
                 ("Rough lemon is prone to foot rot.", ["K93.browning"]),
                 ("Both make large trees.", ["H.cols", "H.rough", "H.volk", "H.vigor", "H.lg"]),
             ],
             "what_to_ask_nursery": [
                 ("If your soil is alkaline, ask whether the tree is on rough lemon, Volkamer lemon or another rootstock "
                  "suited to high-pH soil.", ["K93.calc", "K93.select"]),
             ],
         },
         "values": {
             "size_class": ("standard", ["H.cols", "H.rough", "H.volk", "H.lg"]),
             "mature_height_ft": (None, "Lg waits on PLA-543 (ruling D)"),
             "spread_ft": (None, "unchanged null"),
             "container_suitable": (None, "was false; ABSENT on every page read (ruling D)"),
             "container_size_gallons": (None, "unchanged null"),
             "bearing_age_years": (None, "unchanged null"),
         },
         "sources": ["CH092", "CH093", "HS402", "HS1260"]},
        {"old": "Swingle citrumelo (trifoliate hybrid)", "name": None, "new": False,
         "prose": {
             "traits_seasoned": [
                 ("Swingle is a citrumelo, a cross of Duncan grapefruit and trifoliate orange.", ["K93.swingle"]),
                 ("UF/IFAS names it the rootstock for limes on low-pH or neutral soils.", ["K93.swingle"]),
                 ("It resists Phytophthora foot rot.", ["K93.browning"]),
                 ("UC Riverside lists resistance to tristeza and cold among its strengths.", ["U.resist"]),
                 ("It became the most widely used rootstock in Florida.", ["U.most"]),
                 ("It is not adapted to heavy clay or calcareous soils.", ["U.soil"]),
             ],
             "traits_beginner": [
                 ("A common rootstock that resists foot rot, best on soil that is not alkaline.",
                  ["U.most", "K93.browning", "K93.swingle", "U.soil"]),
                 ("It also holds up against tristeza virus and cold.", ["U.resist"]),
             ],
             "what_to_ask_nursery": [
                 ("On neutral or acidic soil, ask whether the tree is on Swingle citrumelo.", ["K93.swingle"]),
             ],
         },
         "values": {
             "size_class": ("semi_dwarf", H_SW + ["H.sm_i"]),
             "mature_height_ft": ([8, 14], H_SW + ["H.sm_i"]),
             "spread_ft": (None, "unchanged null"),
             "container_suitable": (None, "unchanged null (ruling D)"),
             "container_size_gallons": (None, "unchanged null"),
             "bearing_age_years": (None, "unchanged null"),
         },
         "sources": ["CH093", "UCR-3771", "HS1260"]},
        {"old": None, "name": "Alemow (Citrus macrophylla)", "new": True,
         "prose": {
             "traits_seasoned": [
                 ("Alemow (Citrus macrophylla) is on UF/IFAS's list of rootstocks for limes in high-pH, calcareous "
                  "soils.", ["K92.calc", "K93.calc"]),
                 ("Trees grafted onto alemow tolerate a few days of excessively wet or flooded soil.", ["K93.flood"]),
                 ("The brown citrus aphid spreads tristeza virus, which may cause decline and death of Tahiti lime "
                  "trees on alemow.", ["K93.aphid"]),
                 ("Tahiti limes on alemow may also be susceptible to less-severe tristeza strains.", ["K93.less"]),
                 ("UC rates it highly sensitive to frost.", ["A.rough", "A.key"]),
             ],
             "traits_beginner": [
                 ("Alemow is a rootstock for alkaline soil that copes with a few days of flooding.",
                  ["K93.calc", "K93.flood"]),
                 ("It is vulnerable to tristeza, a virus spread by aphids that can kill lime trees on it, and it is "
                  "very sensitive to frost.", ["K93.aphid", "A.rough", "A.key"]),
             ],
             "what_to_ask_nursery": [
                 ("Alemow suits alkaline soil and tolerates brief flooding.", ["K93.calc", "K93.flood"]),
                 ("It is very sensitive to frost.", ["A.rough", "A.key"]),
             ],
         },
         "values": {f: (None, "HS1260 has no alemow row (ruling D)") for f in
                    ("size_class", "mature_height_ft", "spread_ft", "container_suitable", "container_size_gallons",
                     "bearing_age_years")},
         "sources": ["CH092", "CH093", "ANR8100"]},
    ],
}

RECOMMENDED = {
    LEMON: (None, "No UF lemon page recommends sour orange (HS402 recommends by soil type); TAMU's recommendation is for "
                  "all citrus in south Texas (ruling C)"),
    LIME: (None, "unchanged null (ruling D)"),
}

NOTE = {
    LEMON: [
        ("Rootstocks are usually not a choice at retail garden centers, because trees come grafted onto "
         "industry-standard rootstocks.", ["K.retail"]),
        ("UF/IFAS matches lemon rootstocks to the soil: Swingle citrumelo on acid to neutral sandy soils, and rough "
         "lemon or macrophylla on high-pH, calcareous soils.", ["L.soiltype", "L.sandy", "L.calc"]),
        ("Lemons are susceptible to severe tristeza strains whatever the rootstock, and to less-severe strains on "
         "macrophylla and rough lemon.", ["L.tristeza"]),
        ("Tristeza can kill citrus trees quickly, especially on sour orange rootstock.", ["T.tristeza"]),
        ("Buying a certified disease-free tree reduces the chance of bringing home an infected one.", ["L.cert"]),
        ("In colder areas, trifoliate orange adds cold hardiness, but it does poorly in saline or highly alkaline soil.",
         ["T.trif", "T.pref"]),
    ],
    LIME: [
        ("Rootstocks are usually not a choice at retail garden centers, because trees come grafted onto "
         "industry-standard rootstocks.", ["K.retail"]),
        ("Match the rootstock to your soil.", ["K93.select"]),
        ("For high-pH, calcareous soils, UF/IFAS lists alemow, rough lemon and Volkamer lemon among suitable "
         "rootstocks.", ["K92.calc", "K93.calc"]),
        ("For low-pH or neutral soils, it names Swingle citrumelo.", ["K93.swingle"]),
        ("Key limes are susceptible to tristeza virus whatever the rootstock.", ["K92.tristeza"]),
        ("Tahiti limes may be susceptible to severe strains whatever the rootstock.", ["K93.severe"]),
        ("Key lime is often grown from seed, which comes true to type, and it can also be grown from cuttings, "
         "air-layers or grafted trees.", ["K92.seed", "K92.other"]),
    ],
}

NOTE_SOURCES = {
    LEMON: ["HS132", "HS402", "TAMU"],
    LIME: ["HS132", "CH092", "CH093"],
}

FINDINGS = {
    LEMON: [("lemon_trifoliate_orange_rootstock_in_use_unread_pla609",
             "No T1 page read names trifoliate orange as a lemon rootstock in use. HS402 names it only in its foot-rot "
             "list, and TAMU speaks of citrus generally.")],
    LIME: [],
}

# Ruling A.1: the per-publication ids this promote mints. Titles are read off each page's own <title> / metadata.
CATALOG = {
    "uf_ifas_ch092": {
        "id": "uf_ifas_ch092", "name": "UF/IFAS Key Lime Growing in the Florida Home Landscape (CH092)",
        "title": "Key Lime Growing in the Florida Home Landscape", "publisher": "UF/IFAS Extension",
        "url": "https://ask.ifas.ufl.edu/publication/CH092", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UF/IFAS EDIS publication CH092 (FC47) on key lime in the Florida home landscape: propagation "
                       "(true-to-type seed, cuttings, air-layers, budded or grafted trees), rootstocks for calcareous "
                       "soils, tristeza and foot rot. A document-scoped child of uf_ifas_edis (PLA-625 promote 2, "
                       "ruling A: per-publication ids)."},
    "uf_ifas_ch093": {
        "id": "uf_ifas_ch093", "name": "UF/IFAS Growing 'Tahiti' Limes in the Home Landscape (CH093)",
        "title": "Growing 'Tahiti' Limes in the Home Landscape", "publisher": "UF/IFAS Extension",
        "url": "https://ask.ifas.ufl.edu/publication/CH093", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UF/IFAS EDIS publication CH093 (HS8) on 'Tahiti' lime in the home landscape: rootstock "
                       "selection by soil type (high-pH calcareous vs low-pH or neutral), flood tolerance on alemow, "
                       "tristeza and foot rot by rootstock. A document-scoped child of uf_ifas_edis (PLA-625 promote 2, "
                       "ruling A: per-publication ids)."},
    "uf_ifas_hs1260": {
        "id": "uf_ifas_hs1260", "name": "UF/IFAS Florida Citrus Rootstock Selection Guide, 5th Edition (SP248/HS1260)",
        "title": "Florida Citrus Rootstock Selection Guide, 5th Edition", "publisher": "UF/IFAS Extension",
        "url": "https://ask.ifas.ufl.edu/publication/HS1260", "source_class": "peer_reviewed_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "Peer-reviewed UF/IFAS rootstock guide (SP248/HS1260, 5th ed.): a table rating each rootstock's "
                       "tree size, yield, juice quality, soil tolerances (salinity, high pH, clay, wet, drought), "
                       "freeze, and disease and pest responses. Scope on every use: Florida commercial groves; relative "
                       "vigor; averaged across commercial scions; not scion-specific. A document-scoped child of "
                       "uf_ifas_edis (PLA-625 promote 2, ruling A: per-publication ids)."},
}
