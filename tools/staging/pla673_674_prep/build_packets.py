"""PLA-673 prep: the two quote packets (`hill`, `hilling`) as markdown, every quote PROVEN against hashed bytes.

Each entry names a sha256 + url that must be a MANIFEST row; the quote must be a substring of the page's norm_text
(PDFs through the pinned extractor). Location = character offset in norm_text, plus the PDF page for PDFs. A quote
that fails refuses the build. Nothing here is authored: quotes only, plus a `sense` label per quote.
"""
import glob, io, json, os, sys

import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cited_promote_common import manifest, norm_text, pdf_text, sha256_bytes  # noqa: E402

EV = os.path.join(ROOT, "tools", ".evidence_cache")
MAN = manifest(EV)
DATA = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
_text, _pages = {}, {}


def load(sha):
    if sha in _text:
        return
    f = glob.glob(os.path.join(EV, sha + ".*"))
    assert len(f) == 1, sha
    raw = open(f[0], "rb").read()
    assert sha256_bytes(raw) == sha, sha
    if f[0].endswith(".pdf"):
        _text[sha] = norm_text(pdf_text(raw))
        r = pypdf.PdfReader(io.BytesIO(raw))
        _pages[sha] = [norm_text(p.extract_text() or "") for p in r.pages]
    else:
        _text[sha] = norm_text(raw.decode("utf-8", "replace"))


def locate(sha, url, quote):
    if url not in MAN.get(sha, set()):
        raise SystemExit(f"({sha[:12]}, {url}) is not a MANIFEST row")
    load(sha)
    q = norm_text(quote)
    off = _text[sha].find(q)
    if off < 0:
        raise SystemExit(f"NOT IN HASHED TEXT {sha[:8]}: {quote[:90]!r}")
    loc = f"char {off}"
    if sha in _pages:
        hits = [i + 1 for i, p in enumerate(_pages[sha]) if q[:60] in p]
        loc = f"p. {hits[0]}, " + loc if hits else loc + " (spans a page break)"
    return q, loc


def cited_on(url):
    out = []
    for c in DATA["crops"]:
        if url in json.dumps(c):
            out.append(c["slug"])
    return out


SRC = {
    "purdue": ("740cafac55dd6af4815320a980c96395be32c5721d15f7cee8e61f5693e8ff79",
               "https://edustore.purdue.edu/media/wysiwyg/downloads/pubs/HO/HO-8-W-A.pdf",
               "Purdue HO-8-W-A, Growing Cucumbers, Melons, Squash, Pumpkins and Gourds (rev. 4/01) [purdue_ext_ho8wa, PROPOSED mint]"),
    "csu": ("751295b31e9054c8d7e8ad6166cbc49a5286cd0fc01b5c46c95d68611a8369c1",
            "https://extension.colostate.edu/resource/cucumbers-pumpkins-squash-and-melons/",
            "CSU Fact Sheet 7.609, Cucumbers, Pumpkins, Squash, and Melons [csu_ext_cucurbits_07609, PROPOSED mint]"),
    "b577": ("61333de7f17ad9b4858596e438d9ed4daeba4dc9dc90e8dcd34cf771258965c4",
             "https://fieldreport.caes.uga.edu/publications/B577/", "UGA B577, Home Gardening [uga_b577]"),
    "ncsu": ("5ee8b2dff5f09598200122eec827149bf6f6e5045b4bd36cc718d62beb3cbc40",
             "https://content.ces.ncsu.edu/extension-gardener-handbook/16-vegetable-gardening",
             "NC State Extension Gardener Handbook ch. 16 [ncsu_ext_handbook_vegetable]"),
    "c1206": ("77c14ecc0f33684af662ad9e5573a363c4ca6d0049ce783d773de0f340a41c1b",
              "https://fieldreport.caes.uga.edu/publications/C1206/homegrown-pumpkins/",
              "UGA C1206, Homegrown Pumpkins [uga_c1206_homegrown_pumpkins]"),
    "c1035": ("121640611939808d0be0f7242de4a5d426e0eb30d596b8c1d09cc81731c8ddf9",
              "https://fieldreport.caes.uga.edu/publications/C1035/", "UGA C1035 [uga_ext anchor]"),
    "isu_melon": ("d84b3b2fe25b97578d07f4746e4a10701acf11fa777728043b52aba2539abe6b",
                  "https://yardandgarden.extension.iastate.edu/how-to/growing-cantaloupe-muskmelon-and-other-melons-home-garden",
                  "Iowa State, Growing Cantaloupe, Muskmelon and Other Melons [iastate_ext anchor]"),
    "isu_cuc": ("cc412f7c6e90545ba976ac67ce6a4bb5b2e586708e6f19174720cadcf3e7f06f",
                "https://yardandgarden.extension.iastate.edu/how-to/growing-cucumbers-home-garden",
                "Iowa State, Growing Cucumbers [iastate_ext anchor]"),
    "isu_corn": ("a2bf1671", "https://yardandgarden.extension.iastate.edu/how-to/growing-sweet-corn-home-garden",
                 "Iowa State, Growing Sweet Corn [iastate_ext anchor]"),
    "umn_cuc": ("5645fa79d76fc167dc3329cf6366c203cfd8a84a89e0d0f08e131fdf8db5202a",
                "https://extension.umn.edu/vegetables/growing-cucumbers", "UMN, Growing Cucumbers [umn_ext anchor]"),
    "umd_cuc": ("da454800", "https://extension.umd.edu/resource/growing-cucumbers-home-garden",
                "UMD, Growing Cucumbers [umd_ext anchor]"),
    "umd_sq": ("ee47396a", "https://extension.umd.edu/resource/growing-summer-squash-zucchini-home-garden",
               "UMD, Growing Summer Squash and Zucchini [umd_ext anchor]"),
    "usu_cant": ("3699b298", "https://extension.usu.edu/yardandgarden/research/cantaloupe-in-the-garden",
                 "USU, Cantaloupe in the Garden [usu_ext anchor]"),
    "usu_hd": ("b3737423", "https://extension.usu.edu/yardandgarden/research/honeydew-and-other-melons-in-the-garden",
               "USU, Honeydew and Other Melons [usu_ext anchor]"),
    "nmsu": ("25dbbeb414fb39a5bd78c71de835ec5e032326081a88baca43e74fcad6c5fae8", "https://pubs.nmsu.edu/_circulars/CR457.pdf",
             "NMSU Circular 457 (PDF) [nmsu_ext]"),
    "umn_rasp": ("2e413287db204c6b283af3e5e7bb257302e30301a36db468f5ffb883ffae181a",
                 "https://extension.umn.edu/fruit/growing-raspberries-home-garden",
                 "UMN, Growing Raspberries (cited url; 301s to the garden-and-home path, same bytes) [umn_ext anchor on raspberry]"),
    # packet 2
    "umn_pot": ("fccae103", "https://extension.umn.edu/vegetables/growing-potatoes", "UMN, Growing Potatoes [umn_ext anchor]"),
    "ncsu_pot": ("5c639406", "https://plants.ces.ncsu.edu/plants/solanum-tuberosum/",
                 "NC State Plant Toolbox, Solanum tuberosum [ncsu_ext anchor]"),
    "umn_carrot": ("14d9f710", "https://extension.umn.edu/vegetables/growing-carrots-and-parsnips",
                   "UMN, Growing Carrots and Parsnips [umn_ext anchor]"),
    "umn_leek": ("153697ad", "https://extension.umn.edu/vegetables/growing-leeks", "UMN, Growing Leeks [umn_ext anchor]"),
    "usu_leek": ("ce41cd51", "https://extension.usu.edu/yardandgarden/research/leeks-in-the-garden",
                 "USU, Leeks in the Garden [usu_ext anchor]"),
    "clem_grits": ("65d1d7cb", "https://hgic.clemson.edu/homegrown-grits/", "Clemson HGIC, Homegrown Grits [clemson_hgic anchor]"),
}

P1 = [  # (src, sense, quote)
    ("purdue", "mound + size", "to form a hill, mound soil to make a low, broad hill about 8-10 inches high."),
    ("purdue", "group: seeds per hill", "plant 4-6 seeds in a circle in 5 inch intervals for each hill."),
    ("purdue", "spacing", "each hill should be 4-8 feet apart, depending on the variety you select."),
    ("purdue", "group: plants per hill", "remove all but 2-3 large, healthy, well-spaced plants per hill."),
    ("purdue", "group: plants per hill", "more than 3 plants per hill will lead to crowding, greater chance of disease, and lower yields."),
    ("purdue", "soil-warming (the hilling word)", "methods used to warm the soil include the use of black plastic and the practice of"),
    ("purdue", "soil-warming (the hilling word), after the page-1 footer", "mounding or hilling the soil."),
    ("csu", "mound + why (drainage)", "these plants are usually planted in hills or mounds so excess water drains away from the seedlings."),
    ("csu", "group + spacing", "plant five or six seeds together in hills 4 to 6 feet apart."),
    ("csu", "group: thin", "after emergence, thin each hill to the two or three strongest seedlings."),
    ("b577", "group vs drill", "most crops are best planted in drills, although some widely-spaced crops such as squash and melons may be easier to cultivate and care for if they are planted in hills."),
    ("b577", "drill (contrast)", "a drill is a single row of plants spaced more-or-less evenly."),
    ("b577", "CLUSTER, NOT A MOUND", "a hill is a cluster of plants, not a mound of soil."),
    ("b577", "fertilizing around a hill", "for plants such as watermelons, cantaloupes, cucumbers and pumpkins, which are planted in widely-spaced hills, form a circular furrow 4 to 5 in. from the plants and follow the same general directions."),
    ("ncsu", "group (called HILLING)", "seeds that are large enough to handle can be planted by hilling or by row planting ( drilling )."),
    ("ncsu", "group (called HILLING)", "hilling is placing several seeds in one spot at definite intervals."),
    ("ncsu", "crops", "squashes, pumpkins, and melons are often planted this way."),
    ("ncsu", "group: thin", "once the seeds germinate, the hills are thinned, leaving one or two plants per hill, depending on the vegetable."),
    ("c1206", "spacing", "plant pumpkins in hills, with at least 8 feet of space on all sides."),
    ("c1206", "MOUND + size (\"a few inches\") + why", "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage."),
    ("c1206", "mound + seeds", "seeds should be planted 1 inch deep in slightly raised hills, using four to five seeds per mound."),
    ("c1206", "group: thin", "as seeds germinate, thin seedlings down to two to three plants per mound."),
    ("c1035", "spacing (\"small hills\")", "plant watermelon from seed in small hills with a spacing of 8 ft on all sides."),
    ("c1035", "group: seeds", "sow four to five seeds per hill at a depth of 1 in."),
    ("c1035", "group: thin", "a week after they have germinated, thin the seedlings to two per hill."),
    ("isu_melon", "usage", "melons are usually planted in hills."),
    ("isu_melon", "group: seeds", "plant 4 or 5 seeds per hill at a depth of 1 inch."),
    ("isu_melon", "group: thin", "later, remove all but 2 or 3 healthy, well-spaced plants per hill when seedlings have 1 or 2 true leaves."),
    ("isu_melon", "spacing", "melon hills should be spaced 1.5 to 2 feet apart, with 5 to 6 feet between the rows."),
    ("isu_cuc", "usage (in quotes)", 'cucumbers are normally planted in "hills."'),
    ("isu_cuc", "group: thin", "later, remove all but 2 or 3 plants per hill when seedlings have 1 or 2 true leaves."),
    ("isu_cuc", "spacing", "hills of cucumbers should be spaced 3 to 5 feet apart within the row."),
    ("isu_corn", "PLANTING sense on a CORN page", 'sweet corn may also be planted in "hills." sow 4 to 5 seeds per hill with approximately 3 inches between seeds.'),
    ("isu_corn", "spacing", "hills should be spaced 21⁄2 feet apart with 21⁄2 to 3 feet between rows."),
    ("umn_cuc", "GROUP (in quotes)", 'a "hill" of three or four seeds sown close together is another way to plant cucumbers in the garden.'),
    ("umn_cuc", "spacing", "allow five to six feet between hills."),
    ("umn_cuc", "spacing (bush)", "you can plant bush types, with very short vines, in closely spaced rows or hills, with only two to three feet between rows or hills."),
    ("umd_cuc", "group", "or plant in a hill (two to three plants per hill)."),
    ("umd_sq", "group + spacing", "spacing : hills (two to three plants per hill) 3'- 4' in-row x 4'- 6' between rows; single plants 2'- 3' in-row x 3'- 5' between rows."),
    ("usu_cant", "mound + spacing", "seeds should be planted 1-2 inches deep, in mounds 4 feet apart."),
    ("usu_cant", "mound: thin", "after they have two leaves, thin to 2 plants per mound."),
    ("usu_hd", "mound + spacing", "plant 4-6 seeds in mounds 4 feet apart."),
    ("usu_hd", "mound: thin", "after they have two leaves, thin to two plants per mound."),
    ("nmsu", "method", "another technique for direct seeding is the hill method, which works well for vegetables that should be planted deeper in the soil."),
    ("nmsu", "crops", "squash, melons, cucumbers, corn, and even chile are often planted in hills."),
    ("nmsu", "HOW (a hole, not a mound)", "use a hoe to make a hole in the soil, then drop four or five seeds in the bottom of the hole."),
    ("nmsu", "group: thin (\"one to three\")", "thin to one to three of the most vigorous seedlings after emergence when plants have their first true leaves."),
    ("nmsu", "spacing (bush squash)", "in general, bush types of squash can be planted in hills 24-45 in. apart in rows 36-60 in. apart."),
    ("nmsu", "spacing (vining squash)", "space hills 36-96 in. apart in rows 72-96 in. apart."),
    ("nmsu", "corn in hills", "corn can also be planted in hills with three or four plants per hill to ensure good pollination."),
    ("umn_rasp", "THIRD SENSE (exclusion)", 'the "hill" is not made by mounding the soil; it refers to the cluster of canes that develops from a single plant.'),
    ("umn_rasp", "THIRD SENSE (exclusion)", "set black and purple raspberries 4 feet apart because these types do not produce root suckers, they will create what is commonly called a hill."),
]

P2 = [
    ("umn_pot", "what + when", "once the green shoots emerge, hill soil up around plants as they grow."),
    ("umn_pot", "why", "hilling keeps shallow tubers from exposure to light and turning green."),
    ("umn_pot", "why (stolons)", "the plant will grow more stolons if more of the main stem is underground."),
    ("umn_pot", "when", "start hilling plants when stems are about a foot tall, and once or twice more during the growing season."),
    ("umn_pot", "HOW MUCH", "at the end of the season, you will have hilled six to eight inches of soil in total along the plants."),
    ("umn_pot", "trench alternative", "some gardeners plant seed tubers in shallow trenches to make hilling easier."),
    ("umn_pot", "trench alternative", "instead of mounding soil up, they push the plant down into the trench."),
    ("umn_pot", "NOUN: the hill (harvest)", "dig the hills using a spading fork, being careful not to pierce tubers with fork tines."),
    ("ncsu_pot", "trench alternative", "potatoes also may be grown in trenches to make the process of hilling easier."),
    ("nmsu", "potato, by backfill", "as foliage devel- ops and plants reach 5-6 in. tall, backfill the trench with a mixture of soil and compost throughout the first part of the summer, hilling up the soil around the developing foli- age."),
    ("nmsu", "potato: how much stays above", "keep at least three-quarters of the foliage above the soil line."),
    ("umn_carrot", "carrot/parsnip: why", "hilling soil around these plants will keep the roots from turning green."),
    ("umn_leek", "leek: what + why", "hill the plants to produce a longer white shaft, or plant in a furrow and fill it in."),
    ("umn_leek", "leek: DEFINES hilling", "another method is to hill the plants by planting them at normal soil level, then mounding compost or soil around the plants several times during the growing season."),
    ("usu_leek", "leek: how much, how often", "during the growing season, hill soil around seeded plants 2-3 times adding 2-3 inches of banked soil."),
    ("usu_leek", "leek: why", "hilling encourages taller growth thus producing a longer blanched edible stem."),
    ("usu_leek", "leek: storage use", "in more mild areas of utah, leeks can be stored in the garden by hilling up the soil around the plants and covering them with mulch."),
    ("clem_grits", "corn: support", "these heirloom dent corns grow tall, up to 15 feet, and smaller plantings may blow over more easily in a storm unless spaced a little further apart (2 ft) and hilled with soil."),
    ("purdue", "cucurbit soil-warming (same word, cucurbit page)", "mounding or hilling the soil."),
]


def full_sha(prefix):
    hits = [s for s in MAN if s.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return hits[0]


def render(title, rows, intro):
    out = [f"# {title}", "", intro, ""]
    by = {}
    for src, sense, quote in rows:
        by.setdefault(src, []).append((sense, quote))
    n = 0
    for src, items in by.items():
        sha, url, name = SRC[src]
        sha = full_sha(sha)
        cited = cited_on(url)
        out += [f"## {name}", "", f"* url: {url}", f"* sha256: `{sha}`",
                f"* cited on: {', '.join(cited) if cited else 'NO crop'}", "",
                "| # | sense | verbatim (norm_text) | location |", "| -- | -- | -- | -- |"]
        for sense, quote in items:
            q, loc = locate(sha, url, quote)
            n += 1
            out.append(f"| {n} | {sense} | \"{q}\" | {loc} |")
        out.append("")
    return "\n".join(out), n


if __name__ == "__main__":
    out_dir = sys.argv[1]
    intro1 = ("**PLA-673 quote packet 1: `hill` (planting group / mound).** Read-only on canonical `350eda38`. Every sentence "
              "below is in `norm_text` form and was machine-checked as a substring of its page's HASHED bytes (MANIFEST row + "
              "cache file hashing to its name; PDFs through pypdf " + __import__("pypdf").__version__ + "). Location = "
              "character offset in norm_text (and PDF page). **Nothing here is authored**; the `sense` column is a label "
              "for the reader, not a definition. Definitions come from claude.ai.")
    intro2 = ("**PLA-673 quote packet 2: `hilling` (mounding soil around stems).** Same method as packet 1, drawn from hashed "
              "pages ALREADY CITED on the 11 hilling crops where they define or size the practice, plus Purdue's cucurbit "
              "soil-warming use of the same word. Nothing here is authored.")
    for name, title, rows, intro in (("packet1_hill.md", "PLA-673 packet 1: hill", P1, intro1),
                                     ("packet2_hilling.md", "PLA-673 packet 2: hilling", P2, intro2)):
        md, n = render(title, rows, intro)
        open(os.path.join(out_dir, name), "w", encoding="utf-8").write(md)
        print(f"{name}: {n} quotes, all proven against hashed bytes")
