"""p3a_texts -- the edits of PLA-625 citrus promote 3a (citrus mulch, graft-union height, brown rot), transcribed from the
claude.ai ruling (PLA-625 comment 356a763f, approved by Trevor, 2026-10-16). Nothing here is authored: every replacement
is the ruling's, exact substring for exact substring, and every new clause carries the keys of the cached-page quotes it
rests on (the ruling's brackets, resolved to exact spans of the hashed bytes by the clause check).

QUOTES: key -> (label, quote), a span of the page's norm_text (cited_promote_common).
SOURCES: label -> (source id, url, sha256).
EDITS: one entry per touched string: crop, path, subs [(old, new, quote keys)]. An empty new with no keys is a ruled
deletion. The citation block each string belongs to is derived in build_stage (the ruling's citation rule).
"""

SOURCES = {
    "HS402": ("uf_ifas_hs1153", "https://edis.ifas.ufl.edu/publication/HS402",
              "15801f6dc90c756b97102f8e2cd347ff30d9cb41b87fec4ba69bfeebb8246ea5"),
    "CH092": ("uf_ifas_ch092", "https://ask.ifas.ufl.edu/publication/CH092",
              "e07230d4815d6bd180cf9366ba01375039e22f3a0fb7f535444f965c7c00379d"),
    "CH093": ("uf_ifas_ch093", "https://ask.ifas.ufl.edu/publication/CH093",
              "6fc9a10b6b331b5676fb16be747852eb56ffeecc9077aeca44cb6aaf4f9e92fa"),
    "HS132": ("uf_ifas_hs132", "https://ask.ifas.ufl.edu/publication/HS132",
              "1022a27cf8b7eeda30a87755128be2e4748e3bd9ff0465cedebb7b684e1627fe"),
    "HS141": ("uf_ifas_hs141", "https://ask.ifas.ufl.edu/publication/HS141",
              "70844740696e5b28cfe1381f44e7f2ed2f646c4d8c54e359a8af84a6221de724"),
    "TAMU": ("tamu_agrilife", "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/",
             "23a8436d1d6d0715403a0ccb640429a5818921d601d50456726d8ff34019d28a"),
    "GN127": ("uc_mg_sacramento_gn127", "https://ucanr.edu/sites/default/files/2013-07/72239.pdf",
              "9a52c5e56dbc098c77e8e8441fd80e1f1311fa1912da918513430f44ef6ad9c6"),
    "SCfab": ("ucanr_santa_clara_mg", "https://ucanr.edu/sites/default/files/2020-02/319461.pdf",
              "94c04c9338ac7a01673aaef0bc908b8dc7cd1f1374d57929b2501e4b029c7efb"),
    "31-018C": ("ucce_placer_nevada_31_018c", "https://ucanr.edu/sites/default/files/2020-10/63813.pdf",
                "0bc08654ed55c45d539237840b220d108a9487bb6d8d5231dcc93de84336f0c1"),
    "MaukShea": ("ucce_riverside_citrus_qa", "https://ucanr.edu/sites/default/files/2013-12/178097.pdf",
                 "9047f6edc73a988f32d74b5c888678944d0ec778844c535b13b8fa3d5f027ace"),
    "UCIPM-BR": ("uc_ipm", "https://ipm.ucanr.edu/home-and-landscape/brown-rot-of-citrus/",
                 "75f5366f02aa9e1c8f41ead56876a35059fe7232a9da872f3da77e374c47b5c6"),
}

QUOTES = {
    "L.mulch": ("HS402", "keep mulch 8 to 12 inches (20-30 cm) away from the trunk because mulch against the tree trunk "
                         "may cause trunk rot."),
    "L.grass": ("HS402", "to prevent damage, maintain a grass-free area 2 to 5 or more feet (0.5-1.5 m) away from the "
                         "trunk of the tree."),
    "K92.mulch": ("CH092", "keep mulch 8 to 12 inches (20-30 cm) away from the trunk."),
    "K92.grass": ("CH092", "maintain a grass-free area 2 to 5 or more feet (0.5-1.5 m) away from the trunk of the tree."),
    "K93.mulch": ("CH093", "keep mulch 8-12 inches (20-30 cm) from the trunk."),
    "K.mulch": ("HS132", "mulches are not recommended around citrus trees, but if trees are located in a cultivated plant "
                         "bed where mulch is used, it should be kept at least a foot away from tree trunks."),
    "H141.grass": ("HS141", "the area under the tree canopy should be kept free of grass and weeds."),
    "T.foot": ("TAMU", "if used, keep mulches at least a foot away from the tree trunk."),
    "T.notrec": ("TAMU", "organic mulches are not recommended for citrus trees because of the potential for inducing foot "
                         "rot disease."),
    "GN.mulch": ("GN127", "use 4 to 6 inches of organic matter such as compost, leaves, straw, or wood chips under the tree "
                          "to conserve water and"),
    "GN.keep": ("GN127", "but keep it 4 to 6 inches away from the trunk."),
    "GN.freeze": ("GN127", "rake back mulch to encourage the absorption of daytime heat in the soil"),
    "SC.layer": ("SCfab", "maintain 3 - 4 inch layer of mulch."),
    "SC.keep": ("SCfab", "keep mulch 6-12 inches away from trunk."),
    "F.spread": ("31-018C", "after planting, spread 2-4 inches of compost or mulch on the surface of the soil around the "
                            "tree."),
    "F.keep": ("31-018C", "keep the mulch 4 inches away from the trunk."),
    "MS.grass": ("MaukShea", "keep the area around young trees free from grass for at least one foot (preferably 4 feet) "
                             "from the trunk"),
    "MS.graft": ("MaukShea", "the graft union (slight dogleg shape in the trunk) should be located several inches above "
                             "the soil level."),
    "BR.prune": ("UCIPM-BR", "where brown rot has been a problem, prune the lower canopy of citrus so branches and foliage "
                             "are at least 2 feet from the ground."),
    "BR.sprinkler": ("UCIPM-BR", "do not let irrigation sprinklers wet foliage or fruit."),
    "BR.drop": ("UCIPM-BR", "pick up and dispose of any fruit that has dropped on the ground."),
}

LE, LI, ON, GF, MA = "lemon", "lime", "orange-navel", "grapefruit", "mandarin-clementine"
FR = "diseases[id=phytophthora-foot-rot]"
BR = "diseases[id=citrus-brown-rot]"
FOOT = "a foot"
HAND = "a hand's width"
A_KEYS = {LE: ["L.mulch"], LI: ["K92.mulch", "K93.mulch"], ON: ["T.foot"], GF: ["T.foot"]}
MAUK_GRAFT = ["MS.graft"]
MAUK_GRASS = ["MS.grass"]

B1_OLD = {ON: "Maintain a mulched, grass-free basin, with mulch pulled back from the trunk.",
          GF: "Maintain a mulched, grass-free basin, with mulch pulled back from the trunk.",
          MA: "Maintain a mulched, grass-free basin with mulch pulled back from the trunk."}
B1_SENTENCES = [
    ("UC Master Gardener guides recommend a layer of mulch under citrus, kept back from the trunk.",
     ["GN.mulch", "GN.keep", "SC.layer", "SC.keep", "F.spread", "F.keep"]),
    ("UF/IFAS's general citrus guide and Texas A&M advise against mulching citrus, and say any mulch should stay at least "
     "a foot from the trunk.",
     ["K.mulch", "T.notrec", "T.foot"]),
    ("Before a hard freeze, rake mulch back so the bare soil can absorb heat during the day.", ["GN.freeze"]),
    ("Keep the area under the canopy free of grass and weeds.", ["H141.grass"]),
]
B2_OLD = {ON: "Mulch the area under the tree (but keep the mulch away from the trunk) and keep grass out.",
          GF: "Mulch the area under the tree (but keep the mulch away from the trunk) and keep grass out.",
          MA: "Mulch under the tree, keeping the mulch away from the trunk, and keep grass out."}
B2_SENTENCES = [
    ("Guides disagree on mulch for citrus.", ["GN.mulch", "K.mulch"]),
    ("UC says to mulch under the tree, while Florida's general citrus guide and Texas A&M say not to.",
     ["GN.mulch", "K.mulch", "T.notrec"]),
    ("Texas A&M warns that mulch can encourage foot rot, a disease at the base of the trunk.", ["T.notrec"]),
    ("If you do mulch, keep it a foot from the trunk and rake it back before a hard freeze.", ["T.foot", "GN.freeze"]),
    ("Keep grass and weeds out from under the tree.", ["H141.grass"]),
]
B4_OLD = {ON: "A mulched, grass-free area extending to the canopy dripline is the standard recommendation for all citrus.",
          GF: "A mulched, grass-free area extending to the canopy dripline is the standard recommendation for all citrus.",
          MA: "A mulched, grass-free basin out to the canopy dripline is the standard recommendation for all citrus, "
              "mandarins included."}
B4_DELETE = {ON: "Low-growing nitrogen fixers like white clover or shallow-rooted ground covers planted outside the trunk "
                 "flare provide living mulch without root competition. ",
             GF: "Low-growing legume cover or shallow-rooted ground covers planted outside the trunk flare provide living "
                 "mulch without root competition. ",
             MA: "Low, shallow-rooted covers or a cool-season legume kept outside the trunk flare add living mulch without "
                 "root competition. "}
B5_OLD = {ON: "A ring of mulch (kept back from the trunk) is better than grass right up to the tree.",
          GF: "A wide ring of mulch (kept back from the trunk) is better than grass right up to the tree.",
          MA: "A ring of mulch, kept back from the trunk, beats grass growing right up to the tree."}
B7_OLD = {ON: "Keep a clear or mulched circle around the base of your orange tree and hold the grass back beyond it, since "
              "it will keep trying to spread in.",
          GF: "Keep a clear or mulched circle around the base and hold the grass back beyond it.",
          MA: "Keep a clear or mulched circle around the base and hold the grass back beyond it.",
          LE: "Keep a clear or mulched circle around the base instead.",
          LI: "Keep a clear or mulched circle around the base instead."}
B7_NEW = {c: ("Keep a grass-free circle around the base, at least a foot out from a young tree's trunk and preferably four "
              "feet.", MAUK_GRASS) for c in (ON, GF, MA)}
B7_NEW[LE] = ("Keep grass 2 to 5 feet or more back from the trunk instead.", ["L.grass"])
B7_NEW[LI] = ("Keep grass 2 to 5 feet or more back from the trunk instead.", ["K92.grass"])
B8_OLD = {LE: "Keep a mulched, grass-free area out to the dripline.", LI: "Keep a mulched, grass-free area out to the drip line."}
B8_NEW = "Keep grass 2 to 5 feet or more back from the trunk, and keep any mulch a foot away from it."
B8_KEYS = {LE: ["L.grass", "L.mulch"], LI: ["K92.grass", "K92.mulch"]}

D_TEXT = {
    "prevention_seasoned": ("Skirt-prune the tree so no foliage or fruit hangs within about two feet of the ground, keep "
                            "sprinklers from wetting foliage and fruit, and pick up and dispose of any fruit that drops.",
                            ["BR.prune", "BR.sprinkler", "BR.drop"]),
    "prevention_beginner": ("Trim the lowest branches so no fruit or leaves hang within about two feet of the ground, keep "
                            "sprinkler water off the leaves and fruit, and throw away any fruit that falls.",
                            ["BR.prune", "BR.sprinkler", "BR.drop"]),
    "organic_treatment_seasoned": ("Where brown rot has been a problem, UC IPM advises pruning the lower canopy so branches "
                                   "and foliage are at least 2 feet from the ground.", ["BR.prune"]),
    "organic_treatment_beginner": ("If brown rot has shown up before, trim the low branches so they stay at least 2 feet off "
                                   "the ground.", ["BR.prune"]),
}


def _edits():
    E = {}

    def add(crop, path, old, new, keys):
        E.setdefault((crop, path), []).append((old, new, keys))

    # A. clearance distance
    for crop, fields in ((LE, ["companions.note_seasoned", "soil_prep_seasoned"]),
                         (LI, ["companions.note_seasoned", "soil_prep_seasoned"])):
        for f in fields:
            add(crop, f, "at least a foot", FOOT, A_KEYS[crop])
    for crop, fields in ((LE, ["companions.note_beginner", "soil_prep_beginner", f"{FR}.prevention_beginner"]),
                         (LI, ["companions.note_beginner", "soil_prep_beginner", f"{FR}.prevention_beginner",
                               f"{FR}.control_ladder[0].note_beginner"]),
                         (ON, [f"{FR}.prevention_beginner", f"{FR}.control_ladder[0].note_beginner"]),
                         (GF, [f"{FR}.prevention_beginner"])):
        for f in fields:
            add(crop, f, HAND, FOOT, A_KEYS[crop])
    # B1 / B2 / B3
    for crop in (ON, GF, MA):
        add(crop, "watering.method_seasoned", B1_OLD[crop], " ".join(s for s, _k in B1_SENTENCES),
            sorted({k for _s, ks in B1_SENTENCES for k in ks}))
        add(crop, "watering.method_beginner", B2_OLD[crop], " ".join(s for s, _k in B2_SENTENCES),
            sorted({k for _s, ks in B2_SENTENCES for k in ks}))
    add(MA, "watering.method_note_seasoned",
        ", and hold a grass-free, mulched basin so the shallow roots are not competing with turf",
        ", and keep grass out from under the canopy so it does not compete with the tree's shallow roots", ["H141.grass"])
    # B4 / B5 / B6 / B7 / B8
    for crop in (ON, GF, MA):
        add(crop, "companions.note_seasoned", B4_OLD[crop], "Keep the area under the canopy free of grass and weeds.",
            ["H141.grass"])
        add(crop, "companions.note_seasoned", B4_DELETE[crop], "", [])
        add(crop, "companions.note_beginner", B5_OLD[crop],
            "UC advises keeping grass at least a foot from a young tree's trunk, and preferably four feet.", MAUK_GRASS)
        add(crop, "companions.bad_beginner[0].why_beginner", "A ring of mulch, kept back from the trunk, is better than grass.",
            "Keep grass at least a foot from a young tree's trunk, and preferably four feet.", MAUK_GRASS)
    for crop in (ON, GF, MA, LE, LI):
        new, ks = B7_NEW[crop]
        add(crop, "companions.bad_beginner_seasoned[0].why_beginner", B7_OLD[crop], new, ks)
    for crop in (LE, LI):
        add(crop, "companions.bad_seasoned[0].why_seasoned", B8_OLD[crop], B8_NEW, B8_KEYS[crop])
    # C1 / C2 / C3
    for crop in (LE, LI, ON, GF, MA):
        for f in ("tips_by_stage.planting[0].text_seasoned", "year_one_notes_seasoned", "year_one_notes_beginner"):
            old = "a good two to three inches" if (crop == LE and f.startswith("tips")) else "two to three inches"
            add(crop, f, old, "several inches", MAUK_GRAFT)
    for crop in (ON, GF, MA):
        add(crop, "tips_by_stage.planting[0].text_beginner", "a couple inches above the soil", "several inches above the soil",
            MAUK_GRAFT)
    C3 = [
        (ON, f"{FR}.prevention_beginner", "hold the graft union clear of the soil (UF/IFAS says more than six inches above it)",
         "hold the graft union several inches above the soil"),
        (ON, f"{FR}.prevention_seasoned", "keep the graft union at least six inches above finished grade per UF/IFAS guidance",
         "keep the graft union several inches above finished grade"),
        (ON, f"{FR}.control_ladder[0].note_beginner", "UF/IFAS puts that at six inches or more above finished grade",
         "UC puts that at several inches above the soil"),
        (ON, f"{FR}.control_ladder[0].note_seasoned", "the graft union held at least six inches above finished grade per UF/IFAS",
         "the graft union held several inches above finished grade"),
        (LE, f"{FR}.prevention_seasoned", " (UF/IFAS advises more than six inches above the soil)", ""),
        (LE, f"{FR}.prevention_beginner", "UF/IFAS says keep the union more than six inches above the soil",
         "keep the union several inches above the soil"),
        (LE, f"{FR}.control_ladder[0].note_beginner", "UF/IFAS puts that at more than six inches above the soil",
         "UC puts that at several inches above the soil"),
        (LE, "start_method.notes_seasoned", "(UF/IFAS advises several inches of clearance)",
         "(UC advises several inches above the soil)"),
    ]
    for crop, path, old, new in C3:
        add(crop, path, old, new, MAUK_GRAFT if new else [])
    # D. orange-navel brown rot (whole-string replacements)
    for f, (new, ks) in D_TEXT.items():
        add(ON, f"{BR}.{f}", None, new, ks)
    return E


EDITS = _edits()

# Ruled citation moves (C4, D), and the mechanical re-keys / repoints a touched block needs so that one id carries one
# URL per block (logged decisions; see DECISIONS.tsv).
# C4, as amended (PLA-625 comment 5dde3208): CG009 stays as a real source for the 11 clauses only it supports (young
# trees x8, Carrizo x3; independent read, stop report 00ee5ba1). Its anchors are re-keyed to the minted uf_ifas_cg009 at
# the same url, with the scope recorded on the anchor; no anchor is removed.
ANCHOR_REMOVALS = []
CG009_NOTE = "Florida commercial production guide; cited only where no home-garden page covers the claim"
CG009_REKEYS = [(ON, FR, "uf_ifas_edis"), (LE, FR, "uf_ifas_hs132")]
REKEYS = [  # (crop, block, from id, to id): the same URL, the correct per-publication / per-document id
    (LI, "companions", "uf_ifas_edis", "uf_ifas_ch092"),
    (LI, FR, "uf_ifas_edis", "uf_ifas_ch092"),
    (LI, FR, "ufifas_ext", "uf_ifas_ch093"),
    (MA, "watering", "ucanr_santa_clara_mg", "uc_mg_santa_clara_citrus"),
] + [(c, b, frm, "uf_ifas_cg009") for c, b, frm in CG009_REKEYS]
REPOINTS = [  # D: uc_ipm on orange-navel brown rot -> the cached home-and-landscape page
    (ON, BR, "uc_ipm", "https://ipm.ucanr.edu/home-and-landscape/brown-rot-of-citrus/"),
]
LADDER_REMOVE = [(ON, BR, 1, "splash_barrier_mulch")]
FINDING_RESOLVE = []
# Amendment stop 2: the finding stays OPEN past 3a (no status change); the record says so.
FINDING_NOTE = [(GF, "grapefruit_mulched_basin_contradicted_pla533",
                 "2026-10-16 (PLA-625 promote 3a, rulings 356a763f + 5dde3208): watering.method_* mulch sentences "
                 "re-authored (UC Master Gardener guides recommend mulch with clearance; UF/IFAS's general citrus guide and "
                 "Texas A&M advise against it). An independent clause check graded 14 of 20 clauses supported, 6 partial; "
                 "the four pre-existing partial clauses ('ideal', 'never wet the graft union' in both registers, drip-line "
                 "watering with no young-tree note) are held watering text. STAYS OPEN: closes in promote 4, when watering "
                 "is re-authored whole and the independent check passes on every clause.")]

CATALOG = {
    "uf_ifas_cg009": {
        "id": "uf_ifas_cg009",
        "name": "UF/IFAS Florida Citrus Production Guide: Phytophthora Foot Rot, Crown Rot, and Root Rot (PP-156/CG009)",
        "title": "2026–2029 Florida Citrus Production Guide: Phytophthora Foot Rot, Crown Rot, and Root Rot",
        "publisher": "UF/IFAS Extension", "url": "https://ask.ifas.ufl.edu/publication/CG009",
        "source_class": "university_extension", "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UF/IFAS Florida Citrus Production Guide chapter CG009 (PP-156): Phytophthora foot rot, crown rot "
                       "and root rot in COMMERCIAL groves. Cited only where no home-garden page covers the claim (the "
                       "commercial-page rule; PLA-625 promote 3a amendment): the young-tree overwatering risk, and Carrizo "
                       "citrange named as normally tolerant of P. nicotianae. Not cited for graft-union height. A "
                       "document-scoped child of uf_ifas_edis."},
    "uf_ifas_hs141": {
        "id": "uf_ifas_hs141", "name": "UF/IFAS Citrus Problems in the Home Landscape (HS876/HS141)",
        "title": "Citrus Problems in the Home Landscape", "publisher": "UF/IFAS Extension",
        "url": "https://ask.ifas.ufl.edu/publication/HS141", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UF/IFAS EDIS publication HS141 (HS876) on home-landscape citrus problems, including foot rot "
                       "management: morning irrigation to limit bark wetness, and an area under the canopy kept free of "
                       "grass and weeds. A document-scoped child of uf_ifas_edis (PLA-625 promote 3a; the per-publication "
                       "id pattern of promote 2 ruling A.1)."},
}

# Ruling E: resolved ONLY on an independent clause check of every clause of both watering.method_* registers. Filled in
# from that check's result; the stage refuses to build while it is the placeholder.
RESOLUTION_NOTE = "PENDING-INDEPENDENT-CHECK"
