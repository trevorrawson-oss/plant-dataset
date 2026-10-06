"""PLA-673 part B2 packet: the 7 leaves with unsupported claims (D8 + mound width), each claim with every hashed sentence on
pages cited on that crop that bears on it, curated by reading from build_b2_candidates.py's output. Every quote is proven
against its hashed bytes (build_packets.locate). Nothing authored."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_packets as bp  # noqa: E402

U = {
    "clem_pep": "https://hgic.clemson.edu/factsheet/pepper/",
    "isu_pep": "https://yardandgarden.extension.iastate.edu/how-to/growing-peppers-home-garden",
    "umd_pep": "https://extension.umd.edu/resource/growing-peppers-home-garden",
    "umn_pep": "https://extension.umn.edu/vegetables/growing-peppers",
    "uga_c1005": "https://fieldreport.caes.uga.edu/publications/C1005/home-garden-peppers/",
    "clem_egg": "https://hgic.clemson.edu/factsheet/eggplant-insect-pests-diseases/",
    "ncsu_egg": "https://plants.ces.ncsu.edu/plants/solanum-melongena/",
    "uf": "https://edis.ifas.ufl.edu/publication/VH021",
    "wsu": "https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf",
    "c1206": "https://fieldreport.caes.uga.edu/publications/C1206/homegrown-pumpkins/",
    "umn_pk": "https://extension.umn.edu/vegetables/pumpkins-and-winter-squash",
    "osu": "https://ir.library.oregonstate.edu/downloads/v979v342w",
    "vt": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html",
}
SHA = {k: None for k in U}
for s, us in bp.MAN.items():
    for k, u in U.items():
        if u in us:
            SHA[k] = s

PEP = [  # (claim, verdict, [(src, quote, scope note)])
    ("raised, well-drained beds or hills", "NOT STATED for pepper/eggplant or for Phytophthora on any hashed cited page. Raised beds appear only as WSU's general drainage advice; no page says hills",
     [("wsu", "soil drainage is determined mostly by the site but can be improved by using raised beds.", "general, all crops"),
      ("wsu", "in areas with heavy rainfall, plant in raised beds (see below) to allow for water drainage.", "general, all crops"),
      ("wsu", "raised beds improve drain- 15 age by allowing water to drain from the bed into the alleyway through the force of gravity.", "general, all crops")]),
    ("well-drained (soil)", "STATED (site/soil), not as a disease measure",
     [("clem_pep", "select a well-drained, loamy, or sandy loam soil for planting.", "peppers"),
      ("isu_pep", "location pepper plants perform best in well-drained soils in full sun.", "peppers"),
      ("umd_pep", "plant peppers in well-drained soil or containers (5-gallon minimum).", "peppers"),
      ("uga_c1005", "peppers need a well-drained soil that receives 8 to 10 hr of sun per day.", "peppers; cited on banana-pepper only"),
      ("ncsu_egg", "it prefers moist, well-drained, fertile, sandy, and loamy soils with a ph range of 5.5 to 6.8.", "eggplant"),
      ("uf", "irrigation and drainage vegetables cannot tolerate standing water from excessive rainfall or irrigation.", "general")]),
    ("avoid low spots that stay wet", "PARTIAL: excess soil moisture -> Phytophthora is STATED for eggplant (Clemson); 'low spots' is on no page",
     [("clem_egg", "avoiding excessive soil moisture is an important strategy for managing phytophthora diseases .", "eggplant"),
      ("clem_egg", "excessive soil moisture increases the incidence of root rots and blight caused by phytophthora and pythium .", "eggplant"),
      ("uga_c1005", "they self-pollinate, enjoy full sun, and do not tolerate frost or cool, wet soil.", "peppers; banana-pepper only"),
      ("uf", "irrigation and drainage vegetables cannot tolerate standing water from excessive rainfall or irrigation.", "general")]),
    ("water at the soil rather than overhead", "STATED (peppers: UMN, UMD, UGA; eggplant: Clemson)",
     [("umn_pep", "avoid overhead sprinkling.", "peppers"),
      ("umn_pep", "wet leaves are more disease prone.", "peppers"),
      ("umd_pep", "drip irrigation and soaker hoses are excellent methods for watering peppers.", "peppers"),
      ("uga_c1005", "water peppers with drip irrigation or soaker hoses when possible to keep the root zone moist.", "peppers; banana-pepper only"),
      ("isu_pep", "the disease organism can be spread by rain or during overhead irrigation.", "peppers, BACTERIAL SPOT paragraph"),
      ("clem_egg", "drip irrigation is the preferred method of watering versus overhead watering, as this keeps water off the foliage and fruit, reducing the severity of foliar diseases and fruit rots.", "eggplant"),
      ("clem_egg", "if unable to drip irrigate, direct water to the base of the plants and avoid wetting the leaves as much as possible.", "eggplant")]),
    ("do not overwater (pepper leaves only)", "PARTIAL: 'moist but not saturated' is STATED (Clemson pepper, blossom-end-rot context; Clemson eggplant)",
     [("clem_pep", "to prevent blossom end rot, keep the soil uniformly moist, but not saturated.", "peppers, blossom end rot"),
      ("clem_egg", "water frequently enough to keep the soil moist but not saturated.", "eggplant")]),
    ("mulch to limit splash", "NOT STATED: no page ties mulch to splash. UMN pepper says splashed soil carries spores, in its overhead-watering paragraph; the mulch sentences are about weeds and moisture",
     [("umn_pep", "soil splashed up onto the leaves can contain disease spores.", "peppers, overhead-watering paragraph"),
      ("clem_pep", "mulching can help to retain consistent soil moisture, conserve water, and reduce weeds.", "peppers"),
      ("umn_pep", "mulching with herbicide-free grass clippings, weed-free straw or other organic material to a depth of three to four inches can help prevent weed growth, decreasing the need for frequent cultivation.", "peppers"),
      ("uga_c1005", "mulch peppers with compost, straw or wood chips to prevent weeds from growing and to conserve water.", "peppers; banana-pepper only")]),
    ("rotation: peppers 'away from peppers and other susceptible crops for at least three to four years'; eggplant 'away from solanaceous and cucurbit crops'",
     "PEPPERS: rotation STATED, '3-4 years' NOT STATED. EGGPLANT: CONTRADICTED. Clemson eggplant (the leaf's own source) says avoid solanaceous crops for three years and 'instead, rotate WITH cucurbits'",
     [("clem_pep", "reduce disease problems by: rotating planting locations.", "peppers"),
      ("uga_c1005", "rotate planting locations regularly.", "peppers; banana-pepper only"),
      ("wsu", "crop rotation rotating crops by family (table 7) helps prevent soil-borne diseases, such as verticillium wilt and phytophthora root rot that are common in the pacific northwest, from building up in the soil.", "general"),
      ("wsu", "follow a 5-7 year rotation if possible, which means not planting crops within the same family in the same bed or row for 5-7 years.", "general"),
      ("clem_egg", "strategies for managing diseases in eggplant crop rotation is an important strategy for managing bacterial wilt, phytophthora blight, and southern blight because the pathogens survive in soil.", "eggplant"),
      ("clem_egg", "avoid planting eggplant where tomatoes, potatoes, peppers, or eggplant (all members of the solanaceae family) were planted within the last three years.", "eggplant"),
      ("clem_egg", "instead, rotate with cucurbits (squash, zucchini, melons, and cantaloupe), brassicas (collards, kale, cabbage, turnips, and broccoli), grasses (sweet corn and grains), alliums (onions, garlic, and leeks), etc.", "eggplant: CONTRADICTS 'away from ... cucurbit crops'")]),
    ("keep fruit up off saturated soil", "NOT STATED on any hashed cited page", []),
    ("the disease itself (Phytophthora blight)", "Named on Clemson eggplant only; NO hashed page cited on bell- or banana-pepper names Phytophthora",
     [("clem_egg", "avoiding excessive soil moisture is an important strategy for managing phytophthora diseases .", "eggplant")]),
]
SQ = [  # every claim of the four soil_prep_seasoned leaves, in leaf order
    ("deep, fertile, well-drained bed in full sun", "STATED for pumpkins (C1206: full sun, deep tilling, well-drained); 'fertile' is a soil-test/fertilizer topic on the pages",
     [("c1206", "site selection and preparation like most vegetables, pumpkins do best when grown in full sunlight conditions.", "pumpkins"),
      ("c1206", "planting in weed-free, well- drained soil will help ensure success.", "pumpkins"),
      ("c1206", "soil should be prepared by deep tilling and adding organic matter, if possible.", "pumpkins"),
      ("umn_pk", "the soil should be moisture retentive yet well-drained.", "pumpkins and winter squash")]),
    ("work several inches of compost or rotted manure in before planting", "PARTIAL: compost / well-rotted manure STATED (UMN), organic matter at prep STATED (C1206); 'several inches' NOT STATED",
     [("umn_pk", "you can improve your soil by adding well-rotted manure or compost in spring or fall.", "pumpkins and winter squash"),
      ("umn_pk", "do not use fresh manure as it may contain harmful bacteria and may increase weed problems.", "pumpkins and winter squash"),
      ("umn_pk", "if you use manure or compost, you may not need additional fertilizer applications, depending on how much organic matter you apply.", "pumpkins and winter squash")]),
    ("big / hungry / long-season plant", "PARTIAL: long season STATED for pumpkins (90-120 days); 'hungry' NOT STATED",
     [("c1206", "maturity dates can vary from 90 to 120 days, so gardeners should allow that much time for harvest.", "pumpkins")]),
    ("low hills or mounds", "STATED (UGA C1206, a PUMPKIN publication, cited on all four; UMN says raised BEDS for drainage)",
     [("c1206", "plant pumpkins in hills, with at least 8 feet of space on all sides.", "pumpkins"),
      ("c1206", "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage.", "pumpkins"),
      ("c1206", "seeds should be planted 1 inch deep in slightly raised hills, using four to five seeds per mound.", "pumpkins"),
      ("umn_pk", "forming raised beds will ensure good drainage, which these crops require.", "pumpkins and winter squash")]),
    ("about a foot across", "NOT STATED: no hashed cited page gives a mound width; C1206 gives height only ('a few inches')", []),
    ("warm faster (in spring)", "NOT STATED for hills or mounds. WSU says a DRIER soil (in its raised-bed passage) warms sooner; UMN says vine crops need warm soil",
     [("wsu", "a drier soil warms sooner and stays warmer longer, allowing for earlier spring planting and later fall production.", "general, raised-bed passage"),
      ("umn_pk", "starting seeds and transplanting direct seeding you can seed vine crops directly into the garden, but they need warm soils (65 degrees fahrenheit at 2 inches soil depth) to germinate properly.", "pumpkins and winter squash"),
      ("wsu", "black plastic mulch absorbs heat and warms the soil in the spring and summer, creat- ing a better environment early in the season for warm-season crops such as melons, tomatoes, and peppers.", "general (black plastic, not mounds)")]),
    ("drain better", "STATED (C1206 mound -> drainage; UMN raised beds -> drainage)",
     [("c1206", "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage.", "pumpkins"),
      ("umn_pk", "forming raised beds will ensure good drainage, which these crops require.", "pumpkins and winter squash")]),
    ("give the vines / plants a (clear) starting point", "NOT STATED; pages speak of sprawl and space only",
     [("c1206", "while pumpkins are not very difficult to grow, they do require a substantial amount of space for their sprawling vines.", "pumpkins")]),
    ("SPACING. pumpkin: hills at least 8 ft apart on all sides, closer for bush and miniature. butternut / spaghetti / vining acorn: 24-36 in in the row, 5-6 ft between rows, closer for bush. acorn bush and semi-bush: about 18-24 in",
     "pumpkin 8 ft STATED (C1206); 24-36 in x 5-6 ft STATED (UMN, pumpkin AND winter squash); closer for bush STATED (UMN); 'miniature' NOT STATED; acorn bush 18-24 in NOT STATED. Table rows below for comparison",
     [("c1206", "plant pumpkins in hills, with at least 8 feet of space on all sides.", "pumpkins"),
      ("umn_pk", "plant pumpkin and winter squash seeds three-fourths of an inch deep, 24 to 36 inches apart.", "pumpkins and winter squash"),
      ("umn_pk", "use the closer spacing if the variety is a bush type.", "pumpkins and winter squash"),
      ("umn_pk", "spacing between rows should be 5 to 6 feet.", "pumpkins and winter squash"),
      ("c1206", "spacing rows per plants 72 by 48 in.", "pumpkins (C1206 cultivar table)"),
      ("wsu", "squash, winter 1-11⁄2 24-36 72", "table 4: depth, between plants (in), between rows (in)"),
      ("wsu", "pumpkin 1-11⁄2 36 72", "table 4: depth, between plants (in), between rows (in)"),
      ("uf", "pumpkin early july mid july early aug 30 2-4 80-100 (70-90) 36-60 60", "table 1: ..., spacing (in) plants, rows"),
      ("vt", "squash, winter 2-4 ft 3-10 ft", "table 5: between plants in row, between rows"),
      ("vt", "pumpkin 2-4' 5-8'", "table 5: between plants in row, between rows"),
      ("osu", "squash (winter) 4 weeks may may may april 15-may 2-4 plants 72\" 48\"", "chart: ..., between rows, apart in the row"),
      ("osu", "pumpkins 4 weeks may may june april 15-june 1-3 plants 72\" 48\"", "chart: ..., between rows, apart in the row")]),
    ("vine run: pumpkin 10-20 ft; butternut 8-12 ft; acorn 4-8 ft; spaghetti 6-8 ft", "NOT STATED as figures; C1206 says some pumpkin varieties spread beyond 8 ft",
     [("c1206", "keep in mind that some varieties will spread out even further than 8 feet.", "pumpkins")]),
    ("on heavy or wet ground build the mounds up for drainage to head off crown and (pumpkin: Phytophthora) fruit rot",
     "PARTIAL: mounds/raised beds for drainage STATED; crown rot, fruit rot and Phytophthora are named on NO hashed page cited on these crops",
     [("c1206", "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage.", "pumpkins"),
      ("umn_pk", "forming raised beds will ensure good drainage, which these crops require.", "pumpkins and winter squash")]),
]


def section(rows, out, n):
    for claim, verdict, qs in rows:
        out += [f"**Claim: {claim}**: {verdict}", ""]
        if not qs:
            out += ["(no hashed sentence bears on it)", ""]
            continue
        out += ["| # | page | verbatim (norm_text) | scope | location |", "| -- | -- | -- | -- | -- |"]
        for src, quote, scope in qs:
            q, loc = bp.locate(SHA[src], U[src], quote)
            n += 1
            out.append(f"| {n} | {src} `{SHA[src][:8]}` | \"{q}\" | {scope} | {loc} |")
        out.append("")
    return n


def main(path):
    data = bp.DATA
    by = {c["slug"]: c for c in data["crops"]}
    out = ["# PLA-673 part B2 packet: the 7 unsupported-claim leaves", "",
           "Read-only on canonical `350eda38`. For each leaf: its full current text, then per claim every sentence on a HASHED page "
           "CITED ON THAT CROP that bears on it, in `norm_text` form, machine-checked as a substring of the hashed bytes. "
           "**Nothing authored.** Clemson eggplant (`635ebdeb`) was hashed into MANIFEST for this packet. Candidates were "
           "collected by `build_b2_candidates.py` and curated by reading; sentences about other crops on multi-crop pages are left out.", "",
           "## Pages", "", "| key | url | sha256 |", "| -- | -- | -- |"]
    for k, u in U.items():
        out.append(f"| {k} | {u} | `{SHA[k]}` |")
    out += ["", "## A. Pepper / eggplant: `prevention_seasoned` of the Phytophthora blight entry (seasoned register)", ""]
    for slug, i in (("bell-pepper", 1), ("banana-pepper", 1), ("eggplant", 3)):
        d = by[slug]["diseases"][i]
        out += [f"* **{slug}** `diseases[{i}].prevention_seasoned` (id `{d['id']}`; sources {d.get('sources')}):",
                f"  > {d['prevention_seasoned']}"]
    out += ["", "Hashed cited pages: bell-pepper 8 (UMN, UMD, ISU, Clemson pepper, UF, WSU, VT, OSU); banana-pepper 9 (adds UGA C1005); "
            "eggplant 6 (Clemson eggplant, now hashed; NCSU toolbox; UF, WSU, VT, OSU). Cited but NOT hashed, so not read: "
            "bell-pepper 22 urls, banana-pepper 20, eggplant 25, among them the peppers' Phytophthora anchor NCSU pepper-diseases "
            "(an index page of links when fetched to scratch). Rows marked 'banana-pepper only' are not cited on bell-pepper.", ""]
    n = section(PEP, out, 0)
    out += ["## B. Squash: `soil_prep_seasoned` (seasoned register)", ""]
    for slug in ("pumpkin", "butternut-squash", "acorn-squash", "spaghetti-squash"):
        out += [f"* **{slug}** `soil_prep_seasoned`:", f"  > {by[slug]['soil_prep_seasoned']}"]
    out += ["", "All four cite UGA C1206 (a pumpkin publication), UMN pumpkins-and-winter-squash, UF, WSU, VT, OSU; the beginner "
            "siblings state no width. Cited but NOT hashed: 19-20 urls per crop, not read. Every claim of each leaf is covered "
            "(the touched-leaf rule); claims a leaf does not make are marked by crop in the claim line.", ""]
    n = section(SQ, out, n)
    out += ["## Headlines", "",
            "* **Eggplant rotation is CONTRADICTED** by its own source: Clemson says rotate WITH cucurbits; the leaf says away from them.",
            "* **No hashed page cited on the peppers names Phytophthora**; the peppers' Phytophthora source (NCSU pepper-diseases) is an unhashed index page.",
            "* 'beds or hills', 'low spots', 'mulch to limit splash', 'keep fruit off saturated soil' (all 3 leaves) and '3-4 years' (peppers) are on no hashed cited page.",
            "* Squash: 'about a foot across', 'warm faster' (for mounds), 'a starting point', 'several inches' of compost, 'hungry', the vine-run figures, acorn bush 18-24 in, and crown / fruit rot / Phytophthora are on no hashed cited page; hills/mounds, drainage, full sun, compost/manure, 90-120 days and the 8 ft / 24-36 in x 5-6 ft spacings are (C1206, UMN)."]
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"{path}: {n} quotes, all proven against hashed bytes")


main(sys.argv[1])
