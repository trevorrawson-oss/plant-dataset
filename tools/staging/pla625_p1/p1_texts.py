"""p1_texts -- the texts and values of PLA-625 citrus promote 1 (orange-navel + grapefruit rootstock rows), transcribed
from the claude.ai ruling (PLA-625 comment 6ab0c56a, approved by Trevor, 2026-10-13). Nothing here is authored: every
sentence is the ruling's, in the ruling's order, and each carries the keys of the cached-page quotes it rests on
(the ruling's brackets, resolved to exact spans of the hashed bytes by the clause check). A beginner sentence carries
its seasoned twin's quotes: the ruling brackets the seasoned register only.

QUOTES: key -> (label, quote). The quote is a span of the page's norm_text (cited_promote_common), checked again by the
promote's guard E against the MANIFEST bytes.
SOURCES: label -> (source id, url, sha256).
"""

SOURCES = {
    "HS1260": ("uf_ifas_edis", "https://ask.ifas.ufl.edu/publication/HS1260",
               "2d5d5bcd5cd1f80a6c427dbf1d8dec321d73a89ba7dac72117483c39bac1f1d7"),
    "UCR-2863": ("ucr_citrus", "https://citrusvariety.ucr.edu/crc2863",
                 "651bd22c46ba74e1630d3a0e4479d7602aa557d9b55edbf46f0e7fac040e88cb"),
    "UCR-3771": ("ucr_citrus", "https://citrusvariety.ucr.edu/crc3771",
                 "b7c86be25f532cbdf26120a88d50564bdfd388621fb12681c373a45fc5fcc0c9"),
    "31-018C": ("ucce_placer_nevada_31_018c", "https://ucanr.edu/sites/default/files/2020-10/63813.pdf",
                "0bc08654ed55c45d539237840b220d108a9487bb6d8d5231dcc93de84336f0c1"),
    "SantaClara": ("ucanr_santa_clara_mg", "https://ucanr.edu/sites/default/files/2020-02/319461.pdf",
                   "94c04c9338ac7a01673aaef0bc908b8dc7cd1f1374d57929b2501e4b029c7efb"),
    "ANR8100": ("uc_anr_8100", "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf",
                "efbfe5dc93eee7cc876804056d8e99f2dc5ed0d2f6620e58846ed8a153f4c347"),
    "AZ1001": ("az_coop_ext", "https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1001.pdf",
               "900da76c85fd9619578ec7b0da6e2cfeee44a0215838cb97c665bc6890bbfa2d"),
    "TAMU": ("tamu_agrilife", "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/",
             "23a8436d1d6d0715403a0ccb640429a5818921d601d50456726d8ff34019d28a"),
    "HS132": ("uf_ifas_hs132", "https://ask.ifas.ufl.edu/publication/HS132",
              "1022a27cf8b7eeda30a87755128be2e4748e3bd9ff0465cedebb7b684e1627fe"),
}

HS1260_COLUMNS = ("seed germination* seedling uniformity tree size spacing yield per tree yield per acre juice quality "
                  "fruit size salinity high ph clay soil wet soil drought freeze hlb incidence blight phytophthora "
                  "p. palmivora weevil complex burrowing nematode citrus nematode tristeza")

QUOTES = {
    # HS1260 (SP248, 5th ed., May 2026). Scope on every use: Florida commercial groves; relative vigor; averaged across
    # commercial scions; not scion-specific (ruling A.1).
    "H.cols": ("HS1260", HS1260_COLUMNS),
    "H.carrizo": ("HS1260", "carrizo citrange 1932 90% 90% lg 8-12 h i-h i-h/i i-lg p p p i g g i-h i i [s] [s] s t"),
    "H.swingle": ("HS1260", "swingle citrumelo 1974 >90% 95% i 8-12 i i i/i i p p p [g] p-i g i t t+ s [s] r t"),
    "H.fd": ("HS1260", "flying dragon tf 1978 80%-90% 80%-90% sm 5-7 l-i h h/h sm-i p p g i p g p t [i] s r t"),
    "H.vigor": ("HS1260", "tree size refers to the size of the canopy of a mature tree. the ratings indicate relative "
                          "tree vigor."),
    "H.lg": ("HS1260", "a tree on a selected rootstock would be rated large [lg] if it was comparable in vigor and size "
                       "to one on cleopatra mandarin or rough lemon, i.e., perhaps 14-20 ft tall."),
    "H.sm_i": ("HS1260", "a small tree [sm] would be less than 8 ft tall at maturity, and an intermediate tree [i] would "
                         "be like one on c-35 citrange and range in height from 8 to 14 ft tall."),
    "H.phyto": ("HS1260", "phytophthora nicotianae ratings are a combination of foot- and root-rot tolerances"),
    "H.small_yield": ("HS1260", "small trees usually produce less fruit per tree than larger trees"),
    "U2863.parent": ("UCR-2863", "a cross of washington navel and trifoliate orange"),
    "U3771.parent": ("UCR-3771", "'duncan' grapefruit x poncirus trifoliata"),
    "U3771.most": ("UCR-3771", "these attributes lead 'swingle' to become the mostly highly utilized rootstock in florida"),
    "U3771.gf": ("UCR-3771", "'swingle' was observed to be particularly well adapted for use with grapefruits"),
    "U3771.resist": ("UCR-3771", "resistant to tristeza and phytophthora foot rot, blight, cold, and citrus nematode"),
    "U3771.soil": ("UCR-3771", "'swingle' is moderatlely salt tolerant but is not adapted to heavy clay soils or "
                               "calcareous soils."),
    "F.fd": ("31-018C", "another trifoliate rootstock, flying dragon, has a greater dwarfing effect (~75%) and is well "
                        "suited for home-use or container citrus, but not for production orchards."),
    "F.carrizo": ("31-018C", "carrizo rootstock is sometimes used in the foothills, producing high quality fruit later "
                             "in the season."),
    "F.carrizo_cold": ("31-018C", "carrizo does not impart quite as much cold tolerance as trifoliate, however."),
    "F.cert": ("31-018C", "a reputable nursery will sell trees that are certified disease-free and true-to-type."),
    "S.fd": ("SantaClara", "only true dwarfing rootstock is flying dragon. tree will be 4-8 feet tall."),
    "A.carrizo": ("ANR8100", "trifoliate orange poncirus trifoliata m troyer and carrizo citrange"),
    "A.key": ("ANR8100", "m = moderate sensitivity"),
    "Z.tag": ("AZ1001", "be sure the tree has a tag which identifies both the variety and the rootstock, i.e. , "
                        "'fukumoto' navel orange on a 'carrizo' citrange rootstock."),
    "T.tristeza": ("TAMU", "tristeza is a virus disease that kills citrus trees quickly"),
    "T.bear": ("TAMU", "most budded citrus trees can produce a few fruit in the second year after planting, but usually "
                       "do not produce until the third year."),
    "K.retail": ("HS132", "rootstocks are not usually a choice at retail nurseries and garden centers since they are "
                          "grafted to industry standard rootstocks."),
    "K.soil": ("HS132", "rootstocks are important since they vary in soil adaptation and can influence fruit quality."),
}

ORANGE, GRAPEFRUIT = "orange-navel", "grapefruit"
BOTH = (ORANGE, GRAPEFRUIT)
CARRIZO, SWINGLE, FD = "Carrizo citrange", "Swingle citrumelo", "Flying Dragon trifoliate"

# A sentence: (text, quote keys, crops it appears on). Order is the ruling's.
PROSE = {
    CARRIZO: {
        "traits_seasoned": [
            ("Carrizo is a citrange, a cross of Washington navel orange and trifoliate orange.", ["U2863.parent"], BOTH),
            ("UF/IFAS rates it a large, vigorous tree under Florida grove conditions.",
             ["H.cols", "H.carrizo", "H.vigor", "H.lg"], BOTH),
            ("It tolerates tristeza virus, and UF/IFAS rates its Phytophthora tolerance intermediate.",
             ["H.cols", "H.carrizo"], BOTH),
            ("It does poorly in saline, high-pH and heavy clay soils, and it is susceptible to citrus nematode.",
             ["H.cols", "H.carrizo"], BOTH),
            ("Its cold tolerance is moderate, a little below that of trifoliate orange.",
             ["A.carrizo", "A.key", "F.carrizo_cold"], BOTH),
            ("Foothill growers sometimes use it, and it produces high-quality fruit later in the season.",
             ["F.carrizo"], BOTH),
            ("The University of Arizona uses a navel orange on Carrizo as its example of a correctly labeled nursery tree.",
             ["Z.tag"], (ORANGE,)),
        ],
        "traits_beginner": [
            ("Carrizo grows a large, vigorous tree.", ["H.cols", "H.carrizo", "H.vigor", "H.lg"], BOTH),
            ("It holds up well against tristeza, a virus that can kill citrus trees quickly.",
             ["H.cols", "H.carrizo", "T.tristeza"], BOTH),
            ("Its protection from root rot is only middling.", ["H.cols", "H.carrizo", "H.phyto"], BOTH),
            ("It struggles in salty, alkaline or heavy clay soil.", ["H.cols", "H.carrizo"], BOTH),
            ("It handles cold moderately well, a bit less well than trifoliate orange.",
             ["A.carrizo", "A.key", "F.carrizo_cold"], BOTH),
        ],
        "what_to_ask_nursery": [
            ("Ask for a certified disease-free tree whose tag names both the variety and the rootstock.",
             ["F.cert", "Z.tag"], BOTH),
            ("Carrizo does poorly in salty or alkaline soil, so it is a poor match where your soil is either.",
             ["H.cols", "H.carrizo"], BOTH),
        ],
    },
    SWINGLE: {
        "traits_seasoned": [
            ("Swingle is a citrumelo, a cross of Duncan grapefruit and trifoliate orange.", ["U3771.parent"], BOTH),
            ("It became the most widely used rootstock in Florida.", ["U3771.most"], BOTH),
            ("UC Riverside observed it to be particularly well adapted to grapefruit.", ["U3771.gf"], (GRAPEFRUIT,)),
            ("It resists Phytophthora foot rot and citrus nematode, and it tolerates tristeza virus.",
             ["U3771.resist", "H.cols", "H.swingle"], BOTH),
            ("Its cold hardiness is good.", ["H.cols", "H.swingle", "U3771.resist"], BOTH),
            ("UF/IFAS rates it an intermediate-size tree, smaller than one on Carrizo.",
             ["H.cols", "H.swingle", "H.carrizo", "H.sm_i", "H.lg"], BOTH),
            ("It is not adapted to heavy clay or calcareous soils.", ["U3771.soil", "H.cols", "H.swingle"], BOTH),
            ("On salt the sources differ: UF/IFAS rates its salinity tolerance poor, while UC Riverside calls it "
             "moderately salt tolerant.", ["H.cols", "H.swingle", "U3771.soil"], BOTH),
        ],
        "traits_beginner": [
            ("Swingle is a tough rootstock that became Florida's most widely used.", ["U3771.most"], BOTH),
            ("It is known to suit grapefruit especially well.", ["U3771.gf"], (GRAPEFRUIT,)),
            ("It resists foot rot and root rot, and a root pest called citrus nematode.",
             ["U3771.resist", "H.cols", "H.swingle", "H.phyto"], BOTH),
            ("It holds up well against tristeza virus and cold.", ["U3771.resist", "H.cols", "H.swingle"], BOTH),
            ("It makes a medium-size tree, smaller than Carrizo.",
             ["H.cols", "H.swingle", "H.carrizo", "H.sm_i", "H.lg"], BOTH),
            ("It does poorly in heavy clay or alkaline, lime-rich soil.", ["U3771.soil", "H.cols", "H.swingle"], BOTH),
        ],
        "what_to_ask_nursery": [
            ("Swingle is a good rootstock to ask for with grapefruit.", ["U3771.gf"], (GRAPEFRUIT,)),
            ("It is a poor match for heavy clay or alkaline soil.", ["U3771.soil", "H.cols", "H.swingle"],
             (GRAPEFRUIT,)),
            ("Swingle is a poor match for heavy clay or alkaline soil, so ask about another rootstock if yours is "
             "either.", ["U3771.soil", "H.cols", "H.swingle"], (ORANGE,)),
        ],
    },
    FD: {
        "traits_seasoned": [
            ("Flying Dragon is a trifoliate rootstock with a dwarfing effect of about 75 percent.", ["F.fd"], BOTH),
            ("UC Master Gardeners call it the only true dwarfing citrus rootstock, with trees 4 to 8 feet tall.",
             ["S.fd"], BOTH),
            ("UC Cooperative Extension calls it well suited to home and container citrus, but not to production "
             "orchards.", ["F.fd"], BOTH),
            ("UF/IFAS rates it tolerant of tristeza and Phytophthora, resistant to citrus nematode, and good in "
             "freezes.", ["H.cols", "H.fd"], BOTH),
            ("It does poorly in saline and high-pH soils.", ["H.cols", "H.fd"], BOTH),
            ("Its juice quality rates high, but small trees bear less fruit per tree.",
             ["H.cols", "H.fd", "H.small_yield"], BOTH),
        ],
        "traits_beginner": [
            ("Flying Dragon is a dwarfing rootstock that keeps a citrus tree small, usually 4 to 8 feet tall.",
             ["S.fd", "F.fd"], BOTH),
            ("That makes it a good fit for a pot or a small yard.", ["F.fd", "S.fd"], BOTH),
            ("It holds up well against tristeza virus, root rot and cold.", ["H.cols", "H.fd", "H.phyto"], BOTH),
            ("Its fruit is good, but a smaller tree means a smaller crop.", ["H.cols", "H.fd", "H.small_yield"], BOTH),
            ("It does poorly in salty or alkaline soil.", ["H.cols", "H.fd"], BOTH),
        ],
        "what_to_ask_nursery": [
            ("Ask for Flying Dragon if you want a citrus tree for a pot or a small yard.", ["F.fd"], BOTH),
            ("It is a dwarfing trifoliate rootstock that keeps the tree small.", ["F.fd", "S.fd"], BOTH),
        ],
    },
}

# Row values. A value is (new, quote keys) when cited, or (None, reason) when nulled by the ruling.
VALUES = {
    CARRIZO: {
        "size_class": ("standard", ["H.cols", "H.carrizo", "H.lg"]),
        "mature_height_ft": (None, "A.3: HS1260 Lg ('perhaps 14-20 ft') waits on PLA-543 (self-declared estimates)"),
        "spread_ft": (None, "no page read gives a spread for Carrizo"),
        "container_suitable": (None, "no page read states container suitability for Carrizo"),
        "container_size_gallons": (None, "unchanged null; no page gives a container size"),
        "bearing_age_years": (3, ["T.bear"]),
    },
    SWINGLE: {
        "size_class": ("semi_dwarf", ["H.cols", "H.swingle", "H.sm_i"]),
        "mature_height_ft": ([8, 14], ["H.cols", "H.swingle", "H.sm_i"]),
        "spread_ft": (None, "no page read gives a spread for Swingle"),
        "container_suitable": (None, "no page read states container suitability for Swingle"),
        "container_size_gallons": (None, "unchanged null; no page gives a container size"),
        "bearing_age_years": (3, ["T.bear"]),
    },
    FD: {
        "size_class": ("dwarf", ["S.fd", "H.cols", "H.fd", "H.sm_i"]),
        "mature_height_ft": ([4, 8], ["S.fd"]),
        "spread_ft": (None, "no page read gives a spread for Flying Dragon"),
        "container_suitable": (True, ["F.fd"]),
        "container_size_gallons": (None, "no page read gives a container size for Flying Dragon"),
        "bearing_age_years": (3, ["T.bear"]),
    },
}

ROW_SOURCES = {
    CARRIZO: ["UCR-2863", "HS1260", "ANR8100", "31-018C", "AZ1001", "TAMU"],
    SWINGLE: ["UCR-3771", "HS1260", "TAMU"],
    FD: ["31-018C", "SantaClara", "HS1260", "TAMU"],
}

RECOMMENDED = {
    ORANGE: (None, "graded PARTIAL: AZ1001 uses Carrizo only as a tag example, and no page read recommends a stock for "
                   "oranges (ruling E)"),
    GRAPEFRUIT: ("Swingle citrumelo", ["U3771.gf"]),
}

NOTE = {
    ORANGE: [
        ("Rootstocks are usually not a choice at retail garden centers, because trees come grafted onto "
         "industry-standard rootstocks.", ["K.retail"]),
        ("Ask which rootstock your tree is on, and look for a tag that names both the variety and the rootstock.",
         ["Z.tag"]),
        ("Rootstocks differ in the soils they suit, and they can affect fruit quality.", ["K.soil"]),
        ("For a pot or a small yard, Flying Dragon is a dwarfing rootstock well suited to home and container citrus.",
         ["F.fd"]),
    ],
    GRAPEFRUIT: [
        ("Swingle citrumelo is particularly well adapted to grapefruit.", ["U3771.gf"]),
        ("It resists Phytophthora foot rot and citrus nematode, and it tolerates tristeza, a virus that can kill citrus "
         "trees quickly.", ["U3771.resist", "H.cols", "H.swingle", "T.tristeza"]),
        ("Rootstocks are usually not a choice at retail garden centers, so ask which one your tree is on.",
         ["K.retail", "Z.tag"]),
        ("For a pot or a small yard, Flying Dragon makes a dwarf tree.", ["F.fd"]),
        ("Swingle does poorly in calcareous soil, and Flying Dragon does poorly in high-pH soil.",
         ["U3771.soil", "H.cols", "H.fd"]),
    ],
}

NOTE_SOURCES = {
    ORANGE: ["HS132", "AZ1001", "31-018C"],
    GRAPEFRUIT: ["UCR-3771", "HS1260", "TAMU", "HS132", "AZ1001", "31-018C"],
}

# Non-blocking open findings (PLA-612), appended to verification_status.open_findings.
FINDINGS = {
    GRAPEFRUIT: [("grapefruit_carrizo_scion_pairing_unread_pla612",
                  "No T1 page read pairs Carrizo with a grapefruit scion. The row describes the stock, as HS1260 rates "
                  "stocks averaged across scions."),
                 ("grapefruit_flying_dragon_scion_pairing_unread_pla612",
                  "No T1 page read pairs Flying Dragon with grapefruit. 31-018C and Santa Clara name no scion.")],
    ORANGE: [("orange-navel_swingle_scion_pairing_unread_pla612",
              "No T1 page read pairs Swingle with an orange scion. The row describes the stock.")],
}
