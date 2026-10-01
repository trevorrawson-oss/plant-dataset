#!/usr/bin/env python3
"""PLA-532 content: the container and vertical TECHNIQUE sources admitted to source_catalog.

Base 00dda31c. Catalog only: no crop record changes, no crop-level sources array changes. Nothing
admitted here is cited by any crop at admission. Promote 2 of PLA-10 and PLA-533's remainder do the
citing, each under its own clause check.

--------------------------------------------------------------------------------------------------
WHAT WAS MEASURED BEFORE ANYTHING WAS ADMITTED (2026-09-30, canonical 00dda31c)
--------------------------------------------------------------------------------------------------
The rule was "admit nothing no queued claim needs". Four claim classes, and who queues them:

  A. TRELLIS SPACING BY CROP (PLA-10 promote 2, spec §10.2 and D7). Measured against the cached
     pages each crop already cites: the 6 tomatoes and the 4 cucumbers already have a support-
     conditional spacing on a cited page (Cornell, ISU, UNL G1650, Illinois, UMD; Clemson HGIC
     cucumber). sweet-pea has one (Cornell high tunnels, "2 to 4 plants per foot on a trellis").
     NO cited page gives a trellised spacing for cantaloupe, honeydew-melon, watermelon,
     butternut-squash, acorn-squash, spaghetti-squash, pumpkin, zucchini-courgette,
     yellow-summer-squash, snow-peas or sugar-snap-peas (11 crops).
  B. SUPPORT REQUIREMENT (promote 2: which crops get a stake/cage/trellis entry; the 3 peas'
     optional-vs-required call). Tomatoes, cucumbers, pole beans and the peas already have it on a
     cited page. Melons and squash do not say whether, or how, they may be supported.
  C. VERTICAL FOOTPRINT / YIELD / WATER / SHADING (PLA-534, Todo, "opens against the landed
     baseline" after promote 2). Not promote-2 authoring (spec §10.3), but a queued claim: the
     load-bearing sentence the ticket and the PLA-10 2026-09-16 comment both rest on.
  D. CONTAINER TECHNIQUE: per-crop minimum container size (PLA-533's audit, step 3: "where a
     PLA-532 source states a figure for that crop, compare"). 102 certified crops carry a non-null
     min_pot_gallons; orange-navel (15) and grapefruit (20) rest on no source (PLA-612).

--------------------------------------------------------------------------------------------------
NEW ID vs WIDEN THE INSTITUTION ENTRY (decided per institution; the ticket preferred widening)
--------------------------------------------------------------------------------------------------
NEW DOCUMENT-SCOPED IDS, for every institution, including the four the ticket named (umd_ext,
ncsu_ext, umn_ext, usu_ext). Widening would put a TECHNIQUE scope on an institution-root entry whose
catalog url is a site root (extension.umd.edu, content.ces.ncsu.edu, extension.umn.edu/vegetables,
extension.usu.edu/yardandgarden): the scope would then describe a document the entry cannot name,
the catalog would still not record which publication carries the claim, and a citation made
against it that fell back to the catalog url would be exactly the bare, sole anchor A63 fails.
The dataset's own convention since PLA-8 is a document id beside the portal id
(ncsu_ext_handbook_tree_fruit beside ncsu_ext, umd_ext_broccoli beside umd_ext), and each entry
below names its portal. usu_ext needs no decision: its only candidate is rejected.

--------------------------------------------------------------------------------------------------
THE UNIT PROBLEM, RECORDED FOR PLA-533, NOT SOLVED HERE
--------------------------------------------------------------------------------------------------
UMD, VCE 426-336 and UMaine #2762 publish VOLUME (gallons, quarts, pints): those compare to
min_pot_gallons directly. Penn State publishes DIAMETER only (20-inch, 14-inch), with a shape rule
("all pots should be at least as tall as they are wide"). UVM publishes DIAMETER AND QUARTS
together (6.5 inches / 2 quarts; 12 inches / 7 to 9 quarts), so it converts without a depth
assumption. VCE 426-336 gives a 6-inch POT (diameter) for chives, parsley and radish in its indoor
section. Turning a bare diameter into gallons needs a depth, which is a modeled step; PLA-533's
unit ruling (its options 1-3) decides how. Nothing here converts anything.
"""

ACCESSED = "2026-09-30"

# Raw bytes kept in tools/.evidence_cache/<sha256>.<ext>, recorded in MANIFEST.tsv. Fetched with
# urllib under two user-agents (a browser UA and a plain Python UA), the 2026-07-30 / 08-03
# standard; the deny list blocks curl. `url` is the FINAL url after redirects, which is what the
# catalog records.
EVIDENCE = {
    "umd_ext_containers_salad_tables": {
        "url": "https://extension.umd.edu/resource/growing-vegetables-containers-and-salad-tables",
        "sha256": "6d1c968f3e034eb9dd72319d81433c4f91178f4fcfbe21a52bcdfb1594d24a4a",
        "bytes": 120968, "ext": "html", "agents": "urllib browser+plain UA (byte-identical)"},
    "vce_426_336": {
        "url": "https://www.pubs.ext.vt.edu/426/426-336/426-336.html",
        "sha256": "b4227d8cc407b3013bfa628db44073c2ed5b32f5d678165015ae2dce57f7949d",
        "bytes": 105416, "ext": "html", "agents": "urllib browser+plain UA (byte-identical)"},
    "psu_ext_container_vegetables": {
        "url": "https://extension.psu.edu/container-vegetable-gardening-four-keys-to-success",
        "sha256": "bc9d06955ef49fcba506b0459eca81a83825415a9ca3f29757d91ec12649be66",
        "bytes": 384185, "ext": "html", "agents": "urllib browser+plain UA (byte-identical)"},
    "uvm_ext_small_spaces_budget": {
        "url": "https://www.uvm.edu/d10-files/documents/2024-10/containergardeningonabudget.pdf",
        "sha256": "42ad6f2474f4f44a245fd34f9ea931f01a0c82ecdd432214d48e99fa6d1fd574",
        "bytes": 157176, "ext": "pdf", "agents": "urllib browser+plain UA (byte-identical)"},
    "umaine_ext_2762": {
        "url": "https://extension.umaine.edu/publications/2762e/",
        "sha256": "f5763b3bd1e9736f82d30b366c9b872eb5a3eaa8f2c4d54259107dd7f4454643",
        "bytes": 82789, "ext": "html", "agents": "urllib browser UA (plain UA 403)"},
    "umn_ext_trellises_cages": {
        "url": "https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/trellises-and-cages",
        "sha256": "8ee29202ffee29b79e281af3abec17cbf2b98169465b8d66d09845bac2d8280b",
        "bytes": 92937, "ext": "html", "agents": "urllib browser UA (plain UA 403)"},
    "vce_hort_189": {
        "url": "https://www.pubs.ext.vt.edu/HORT/HORT-189/HORT-189.html",
        "sha256": "9a7d9d6a6d41eee8f80200e89fe126bdf6c89db88e1fcfd1902ccb6c2f63a71c",
        "bytes": 97023, "ext": "html", "agents": "urllib browser+plain UA (byte-identical)"},
    "ncsu_ext_handbook_vegetable": {
        "url": "https://content.ces.ncsu.edu/extension-gardener-handbook/16-vegetable-gardening",
        "sha256": "5ee8b2dff5f09598200122eec827149bf6f6e5045b4bd36cc718d62beb3cbc40",
        "bytes": 681592, "ext": "html", "agents": "urllib browser+plain UA (byte-identical)"},
}

# The verbatim sentences each entry's citable_for rests on. The suite asserts every one is present
# in the cached text of its document (whitespace-normalized), so a quote that drifts from the page
# fails at the suite, not at a later clause check.
QUOTES = {
    "umd_ext_containers_salad_tables": [
        "Minimum container size for common vegetables",
        "Squash (summer) 10 gallon",
        "Tomatoes (cherry) 2 gallon Tomatoes (standard) 5 gallon",
        "Vegetable varieties listed as bush, dwarf, or compact can be grown in smaller containers than those used for their full-size counterparts.",
        "Large-statured herbs (rosemary, bay leaf, sage, parsley, lavender, dill, and fennel) require 5-gallon or larger pots.",
        "Small-statured herbs (basil, cilantro, thyme, mint, oregano, tarragon, and marjoram) will grow well in 2- to 5-gallon pots.",
        "small-statured herbs like parsley, cilantro, and basil",
        "Indeterminate tomato plants growing in 25-gallon pots. Although they can be grown in smaller containers, they will grow larger and produce more fruit as container size increases.",
    ],
    "vce_426_336": [
        "Minimum Container Size Inches Between Plants in Containers Days from Seed to Harvest",
        "Cucumbers full sun 5 gallons 14-18 70-80 Require hot weather,vining types need support",
        "Tomatoes full sun 5 gal. 1 plant per container 55-100 Stake and prune or cage",
        "Tomatoes, cherry full sun 1 gallon 1 plant per container",
        "Most plants need containers at least 6 to 8 inches deep for adequate root growth.",
        "Plant seeds in a 6-inch pot. The plants should be about 1 inch apart over the entire surface area.",
    ],
    "psu_ext_container_vegetables": [
        "A single tomato plant will need at least a 20-inch-wide pot, while peppers and eggplants can thrive in a 14-inch pot.",
        "Smaller pots are good for herbs and greens.",
        "sweet corn, watermelon, winter squash, and zucchini are all better-suited for in-ground gardening.",
    ],
    "uvm_ext_small_spaces_budget": [
        "you will need a minimum size of 6.5” (2 quarts) as a container.",
        "Leafy greens and herbs grow well in these smaller pots.",
        "Aim for a 12” pot (7 to 9 quarts) to accommodate most other vegetables.",
    ],
    "umaine_ext_2762": [
        "Here are some common container-grown vegetables, container sizes, and recommended varieties:",
        "Broccoli 5-gallon pot (1 plant); 15-gallon tub (3 plants)",
        "Cucumber 2-gallon bucket (1 plant) Bush Champion, Littleleaf",
        "Squash, winter 5-gallon bucket Burpee’s Butterbush, Bush Buttercup",
        "Adapted with permission from Larry Bass",
        "Radishes 5-gallon window box Easter Egg, most other types",
    ],
    "umn_ext_trellises_cages": [
        "Plant the vines at the foot of the trellis at the same spacing between the seeds or transplants as if they were going to grow on the ground.",
        "Varieties with fruit weighing up to three pounds and no larger than a cucumber, small melon or small winter squash, work best.",
        "Larger squash and pumpkins are too heavy to trellis. Grow them on the ground.",
        "To prevent this, make hammocks or slings to support the developing fruit.",
        "Cucumbers and small squash do not slip from the vine, so they do not need support.",
        "While some beans are bush types, and some pea varieties do not grow long nor tall, others produce long vines that need support.",
        "Gardeners with small garden plots may bypass crops that need lots of space by planting short-vined or \"bush” varieties of melons, squash and cucumbers.",
        "Some gardeners leave four or more feet between plants in all directions, mulch heavily with clean straw, and allow the plants to sprawl.",
        "each plant takes up much more space than it would otherwise",
    ],
    "vce_hort_189": [
        "Pole beans, peas, cucumbers, melons, and tomatoes are excellent candidates.",
        "Caging is used for heavier crops, including melons and summer/winter squashes that may overburden a trellis or stake due to weight of produce.",
        "The size of cages varies depending on plant spacing and type of crop.",
    ],
    "ncsu_ext_handbook_vegetable": [
        "Vining and sprawling plants, including cucumbers, tomatoes, melons, and pole beans, are obvious candidates for this type of gardening.",
        "Vertical plantings cast a shadow, so place them on the north side of a garden bed to reduce shading, and plant shade-tolerant crops near the vertical ones.",
        "Plants grown vertically take up much less ground, and though the yield per plant may be less, the yield per square foot is much greater.",
        "Because vertically growing plants are more exposed, they dry out faster and require more water than if they were spread over the ground.",
        "Group tall crops (corn, okra, sunflowers) and trellised vines (peas, beans, squash) together on the north side of the garden to avoid shading shorter plants.",
    ],
}

# claim class(es) each admission serves; the suite pins this so an entry cannot enter without one.
CLAIM_CLASS = {
    "umd_ext_containers_salad_tables": ("D",),
    "vce_426_336": ("D",),
    "psu_ext_container_vegetables": ("D",),
    "uvm_ext_small_spaces_budget": ("D",),
    "umaine_ext_2762": ("D",),
    "umn_ext_trellises_cages": ("A", "B"),
    "vce_hort_189": ("B",),
    "ncsu_ext_handbook_vegetable": ("C", "B"),
}

_PROV = ("Minted {d} (PLA-532, catalog-only promote on 00dda31c). Technique-scoped: admitted for "
         "claim class {cls} (see build_pla532_catalog_content), cited by NO crop at admission. "
         "Raw bytes sha256 {sha} ({n} bytes), fetched {d} with {agents}; title read off the "
         "document. Parent portal entry: {portal}.")


def _prov(sid, portal):
    e = EVIDENCE[sid]
    return _PROV.format(d=ACCESSED, cls="+".join(CLAIM_CLASS[sid]), sha=e["sha256"], n=e["bytes"],
                        agents=e["agents"], portal=portal)


CATALOG_NEW = {
    "umd_ext_containers_salad_tables": {
        "id": "umd_ext_containers_salad_tables",
        "name": "UMD Extension -- Growing Vegetables in Containers and Salad Tables",
        "title": "Growing Vegetables in Containers and Salad Tables",
        "publisher": "University of Maryland Extension (Home and Garden Information Center)",
        "url": EVIDENCE["umd_ext_containers_salad_tables"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "CONTAINER TECHNIQUE (J. Traunfeld, March 2026; reviewed M. Talabac, HGIC; page updated September "
            "10, 2026). The table "
            "\"Minimum container size for common vegetables\" gives a VOLUME per crop: beans (bush) 2 "
            "gallon, beets 1/2 gallon, carrots 2 gallon, cabbage 5 gallon, cucumbers 5 gallon, eggplant "
            "5 gallon, lettuce (leaf) 1/2 gallon, peppers 5 gallon, radishes 1 pint, squash (summer) 10 "
            "gallon, Swiss chard 2 gallon, tomatoes (cherry) 2 gallon, tomatoes (standard) 5 gallon. "
            "Herb groups: \"Large-statured herbs (rosemary, bay leaf, sage, parsley, lavender, dill, and "
            "fennel) require 5-gallon or larger pots\"; \"Small-statured herbs (basil, cilantro, thyme, "
            "mint, oregano, tarragon, and marjoram) will grow well in 2- to 5-gallon pots\". The "
            "cultivar rule: \"Vegetable varieties listed as bush, dwarf, or compact can be grown in "
            "smaller containers than those used for their full-size counterparts.\" CAPTION, NOT BODY "
            "TEXT: \"Indeterminate tomato plants growing in 25-gallon pots. Although they can be grown in "
            "smaller containers, they will grow larger and produce more fruit as container size "
            "increases\" is ONE photo caption. The 25-gallon figure is not a minimum and must not be cited "
            "as one (the PLA-532 scouting pass reported it as a recommendation); the continuum sentence "
            "is illustrative, usable as the PLA-533 schema finding but not as body guidance. "
            "INCONSISTENCY ON THE PAGE: the herb table calls parsley large-statured, while the Salad Table "
            "section lists \"small-statured herbs like parsley, cilantro, and basil\"; cite the table. Serves PLA-533's per-crop min_pot_gallons comparison."),
        "_admission_provenance": _prov("umd_ext_containers_salad_tables", "umd_ext"),
    },
    "vce_426_336": {
        "id": "vce_426_336",
        "name": "Virginia Cooperative Extension Publication 426-336",
        "title": "Vegetable Gardening in Containers",
        "publisher": "Virginia Cooperative Extension, Virginia Tech",
        "url": EVIDENCE["vce_426_336"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "CONTAINER TECHNIQUE (VCE 426-336 / SPES-796P, D. Relf; reviewed E. Olsen; last revised "
            "March 2026). A per-crop table, \"Minimum Container Size / Inches Between Plants in "
            "Containers / Days from Seed to Harvest\", in VOLUME: beans (bush) 2 gallons, beets 1/2 "
            "gallon, carrots 1 quart, cabbage 5 gallons, Swiss chard 1/2 gallon, cucumbers 5 gallons "
            "(14-18 in between plants; \"vining types need support\"), eggplant 5 gallons, kale 5 "
            "gallons, leaf lettuce 1/2 gallon, mustard greens 1/2 gallon, green onions 1/2 gallon, bell "
            "peppers 2 gallons, radishes 1 pint, summer squash 5 gallons (\"Plant only bush type\"), "
            "tomatoes 5 gal. (\"Stake and prune or cage\"), cherry tomatoes 1 gallon, turnips 3 gal. "
            "General floor: \"Most plants need containers at least 6 to 8 inches deep for adequate root "
            "growth.\" Indoor section gives a pot size in inches, not a volume (read as diameter; the page "
            "does not say): chives, parsley and radish in a 6-inch pot, carrots grown the same way, parsley "
            "one vigorous plant per pot (chives \"about 1 inch apart over the entire surface area\", about 12 weeks from "
            "seed to first cut). Serves PLA-533's per-crop comparison; the 6-inch-pot rows carry the "
            "diameter unit problem."),
        "_admission_provenance": _prov("vce_426_336", "none (VCE publications are catalogued per document, cf. vce_426_331)"),
    },
    "psu_ext_container_vegetables": {
        "id": "psu_ext_container_vegetables",
        "name": "Penn State Extension -- Container Vegetable Gardening: Four Keys to Success",
        "title": "Container Vegetable Gardening - Four Keys to Success",
        "publisher": "Penn State Extension",
        "url": EVIDENCE["psu_ext_container_vegetables"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "CONTAINER TECHNIQUE (E. Kinley, Senior Extension Program Manager; updated March 30, 2026). DIAMETER, not volume: \"A single tomato plant will need at least a 20-inch-wide pot, "
            "while peppers and eggplants can thrive in a 14-inch pot. Smaller pots are good for herbs "
            "and greens.\" Shape rule stated beside it: for healthy root growth all pots should be at "
            "least as tall as they are wide. Recommends dwarf or shorter varieties labeled bush or "
            "determinate for containers. CONTAINER EXCLUSIONS, which conflict with UMaine #2762 and UMD: "
            "\"sweet corn, watermelon, winter squash, and zucchini are all better-suited for in-ground "
            "gardening\"; a later author citing a container figure for those crops must record the "
            "disagreement. Serves PLA-533's comparison for the tomatoes, peppers and "
            "eggplant; a gallon figure from it is a MODELED conversion (depth assumed), per PLA-533's "
            "unit ruling."),
        "_admission_provenance": _prov("psu_ext_container_vegetables", "psu_ext"),
    },
    "uvm_ext_small_spaces_budget": {
        "id": "uvm_ext_small_spaces_budget",
        "name": "UVM Extension -- Gardening in Small Spaces on a Budget",
        "title": "Gardening in Small Spaces on a Budget",
        "publisher": "University of Vermont Extension, Community Horticulture Program",
        "url": EVIDENCE["uvm_ext_small_spaces_budget"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "CONTAINER TECHNIQUE (D. Heleba, UVM Extension Community Horticulture Program, April 2023). "
            "The container floor, as an inch size AND a volume together: \"you "
            "will need a minimum size of 6.5\" (2 quarts) as a container. Leafy greens and herbs grow "
            "well in these smaller pots. Aim for a 12\" pot (7 to 9 quarts) to accommodate most other "
            "vegetables.\" The page never says diameter, and a 12-inch-diameter pot usually holds far more "
            "than 7 to 9 quarts, so do NOT derive a depth or a conversion from the pairing; cite the "
            "quarts. \"Most other vegetables\" names no crop: this is not a tomato or fruiting-crop "
            "minimum. Serves PLA-533's comparison for the greens and herbs carried at 1 gallon or less. TITLE NOTE: the scouting pass called this "
            "\"container gardening on a budget\" (the file name); the document's own heading, read off "
            "the rendered first page, is \"Gardening in Small Spaces on a Budget\"."),
        "_admission_provenance": _prov("uvm_ext_small_spaces_budget", "none (no uvm id catalogued)"),
    },
    "umaine_ext_2762": {
        "id": "umaine_ext_2762",
        "name": "UMaine Extension Bulletin #2762 -- Container Gardening Series: Growing Vegetables in Container Gardens",
        "title": "Bulletin #2762, Container Gardening Series: Growing Vegetables in Container Gardens",
        "publisher": "University of Maine Cooperative Extension",
        "url": EVIDENCE["umaine_ext_2762"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "CONTAINER TECHNIQUE (adapted for Maine by K. Hopkins, D. Coffin, F. Wertheim and C. Bowie, "
            "from L. Bass, Container Vegetable Gardening, North Carolina Cooperative Extension Service, "
            "1999). A table of \"common container-grown "
            "vegetables, container sizes, and recommended varieties\" in VOLUME, with plant counts for "
            "multi-plant tubs: broccoli, cabbage and Chinese cabbage 5-gallon pot (1 plant) or 15-gallon "
            "tub (3 plants); Brussels sprouts 5-gallon pot (1) or 15-gallon tub (2); sweet pepper "
            "2-gallon pot (1) or 15-gallon tub (5); cucumber 2-gallon bucket (1); eggplant 5-gallon "
            "bucket (1); tomatoes, zucchini and winter squash 5-gallon bucket; beans, beets, chard, "
            "lettuce, onions, radishes, spinach 5-gallon window box; carrots 5-gallon window box at "
            "least 12 inches deep; peas 5-gallon window bucket; herbs (parsley, chives, basil, thyme) in "
            "5-gallon window boxes. VARIETY-BOUND: every row names recommended cultivars, several of them "
            "compact (cucumber Bush Champion, winter squash Burpee's Butterbush and Bush Buttercup), so a "
            "row is a figure for those cultivars, the cultivar-conditional case PLA-533 records, not a "
            "species minimum; the radish (\"most other types\") and lettuce (\"any mini head variety\") "
            "rows are not cultivar-bound. Penn State lists winter squash and zucchini as better in-ground. Also carries per-pot counts relevant to plants_per_pot (PLA-580)."),
        "_admission_provenance": _prov("umaine_ext_2762", "umaine_ext"),
    },
    "umn_ext_trellises_cages": {
        "id": "umn_ext_trellises_cages",
        "name": "UMN Extension -- Trellises and cages to support garden vegetables",
        "title": "Trellises and cages to support garden vegetables",
        "publisher": "University of Minnesota Extension",
        "url": EVIDENCE["umn_ext_trellises_cages"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "VERTICAL TECHNIQUE: TRELLIS SPACING AND WHICH VINES MAY BE TRELLISED (J. MacKenzie, "
            "reviewed 2024). THE SPACING RULE promote 2 needs for melons, squash and peas: \"Plant the "
            "vines at the foot of the trellis at the same spacing between the seeds or transplants as "
            "if they were going to grow on the ground.\" So a trellis entry's in-row figure is the "
            "crop's own ground in-row figure. The rule sits under \"Trellises for vine crops\" (melons, "
            "squash, cucumbers); applying it to peas, which get their own section, is an inference. This "
            "page states NO row spacing for a trellised planting. "
            "SIZE LIMIT: varieties \"with fruit weighing up to three pounds and no larger than a "
            "cucumber, small melon or small winter squash, work best\"; \"Larger squash and pumpkins are "
            "too heavy to trellis. Grow them on the ground.\" MELONS: many slip from the vine when ripe, "
            "so \"make hammocks or slings to support the developing fruit\"; cucumbers and small squash "
            "do not slip and need no fruit support. PEAS AND BEANS: \"some pea varieties do not grow "
            "long nor tall, others produce long vines that need support\" (support is cultivar-"
            "conditional). BUSH BYPASS: small plots may plant short-vined or bush melons, squash and "
            "cucumbers instead (plant_habit, PLA-12). TOMATO SPRAWL: \"Some gardeners leave four or more "
            "feet between plants in all directions, mulch heavily with clean straw, and allow the plants "
            "to sprawl\", and \"each plant takes up much more space than it would otherwise\": a practice "
            "some gardeners use, not a recommendation, and the page gives no spacing for supported "
            "tomatoes, so it states no numeric delta. Serves promote 2's "
            "support entries and trellis in-row spacing on the 11 crops no cited page covered. Parent portal "
            "entry: umn_ext. Requested url https://extension.umn.edu/planting-and-growing-guides/"
            "trellises-and-cages redirects here."),
        "_admission_provenance": _prov("umn_ext_trellises_cages", "umn_ext"),
    },
    "vce_hort_189": {
        "id": "vce_hort_189",
        "name": "Virginia Cooperative Extension Publication HORT-189NP / SPES-450NP",
        "title": "Vertical Gardening Using Trellises, Stakes, and Cages",
        "publisher": "Virginia Cooperative Extension, Virginia Tech",
        "url": EVIDENCE["vce_hort_189"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "VERTICAL TECHNIQUE: SUPPORT TYPE BY CROP (K. Settlage and A. Hessler; reviewed M. A. "
            "Andruczyk; published December 12, 2022). Names balconies, decks, patios, windowsills, fence "
            "lines and backyard gardens as places for it. Candidates: \"Pole beans, peas, cucumbers, melons, and tomatoes are "
            "excellent candidates.\" The CAGE case promote 2's `support: cage` can rest on: \"Caging is "
            "used for heavier crops, including melons and summer/winter squashes that may overburden a "
            "trellis or stake due to weight of produce\"; melons and squash in cages may need slings. "
            "Stake-and-weave for longer rows of tomatoes and peppers (stake between every other plant, twine every 10 inches). "
            "States NO plant spacing (\"The size of cages varies depending on plant spacing and type of "
            "crop\"). Support build specs (posts driven at least 18 to 24 inches) are PLA-534's question 3, not "
            "promote 2's."),
        "_admission_provenance": _prov("vce_hort_189", "none (VCE publications are catalogued per document, cf. vce_426_331)"),
    },
    "ncsu_ext_handbook_vegetable": {
        "id": "ncsu_ext_handbook_vegetable",
        "name": "NC State Extension Gardener Handbook, ch. 16: Vegetable Gardening",
        "title": "16. Vegetable Gardening",
        "publisher": "North Carolina State Extension, NC State University",
        "url": EVIDENCE["ncsu_ext_handbook_vegetable"]["url"],
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": ACCESSED,
        "tier": "T1",
        "citable_for": (
            "VERTICAL TECHNIQUE: THE FOOTPRINT, WATER AND SHADING CLAIMS (C. Gunter). The sentence "
            "PLA-534 rests on: \"Plants grown vertically take up much less ground, and though the yield "
            "per plant may be less, the yield per square foot is much greater.\" Water: vertically "
            "grown plants \"dry out faster and require more water than if they were spread over the "
            "ground\", which the page calls advantageous for plants susceptible to fungal diseases. "
            "Shading: \"Vertical plantings cast a shadow, so place them on the north side of a garden "
            "bed to reduce shading, and plant shade-tolerant crops near the vertical ones\"; group "
            "\"trellised vines (peas, beans, squash)\" with tall crops on the north side. Candidates: "
            "cucumbers, tomatoes, melons and pole beans. These are QUALITATIVE deltas, no figure; they "
            "express against a ground baseline (PLA-10). Table 16-1 is an INTENSIVE planting guide "
            "(between-plant distances for intensive beds), not a row-garden spacing; not admitted for "
            "spacing. Parent portal entry: ncsu_ext; sibling chapter ncsu_ext_handbook_tree_fruit."),
        "_admission_provenance": _prov("ncsu_ext_handbook_vegetable", "ncsu_ext"),
    },
}

# Fetched from raw bytes, adjudicated, NOT admitted. Each carries its reason; the ticket's complete-
# when requires every candidate either admitted or rejected with a recorded reason.
REJECTED = {
    "https://extension.unr.edu/publication.aspx?PubID=3265": (
        "UNR FS-00-42 (Roberts 2000), candidate. The landing page is a stub; the full article "
        "(https://naes.agnt.unr.edu/PMS/Pubs/2000-3265.pdf, sha256 be20bc9f..., 224,860 bytes) "
        "carries container materials and general care, and NO per-crop size, spacing or support "
        "claim. No queued claim needs it."),
    "https://extension.usu.edu/utah4h/research/creating-sustainable-school-and-home-gardens-vertical-gardening": (
        "USU 'Creating Sustainable School and Home Gardens: Vertical Gardening', candidate. Generic "
        "benefits list and a commercial garden-tower example; no crop-level, spacing, support-type or "
        "footprint claim beyond what NCSU ch. 16 states with more precision (its one crop remark: "
        "asparagus may not grow as well in a container). usu_ext therefore needs "
        "no new-vs-widen decision."),
    "https://hort.extension.wisc.edu/articles/trellising-staking-and-caging-vertical-gardening-techniques-vine-type-vegetables/": (
        "UW-Madison A3933-01 (Tomesh, rev. 03/2011), candidate; the PDF rendition "
        "https://hort.extension.wisc.edu/files/2014/11/A3933-01.pdf was also fetched. Support "
        "candidacy (peas, squashes, melons) duplicates UMN and VCE HORT-189; its unique content "
        "(2-foot cage diameter, trellis posts 12 to 20 feet apart, yield per square foot as a listed "
        "benefit) is support-build spec (PLA-534 question 3) or NCSU ch. 16's claim. States no plant "
        "spacing. Redundancy is not a need."),
    "https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/426/426-336/SPES-796.pdf": (
        "The PDF rendition of VCE 426-336 (SPES-796). Same publication as the admitted HTML "
        "(vce_426_336); one id per publication."),
    "https://extension.umd.edu/resource/growing-vegetables-containers": (
        "UMD 'Growing Vegetables in Containers', the thinner sibling of the admitted Containers and "
        "Salad Tables page: carries the easy/challenging crop lists and the 20-inch-container weight "
        "note, and NO per-crop size table. Superseded."),
    "https://extension.umd.edu/resources/yard-garden/containers-and-small-spaces/container-food-gardening": (
        "UMD container food gardening INDEX page (links only). Not a document."),
    "https://extension.umd.edu/resource/growing-herbs-containers-and-indoors": (
        "UMD 'Growing Herbs in Containers and Indoors'. No container size; the herb size groups are "
        "on the admitted Containers and Salad Tables page."),
}

# Hunted for a queued claim and NOT FOUND in T1, recorded so the gap is not re-hunted blind.
NOT_FOUND = {
    "citrus container size (PLA-612: orange-navel 15, grapefruit 20 unanchored)": (
        "UF/IFAS 'Dwarf Fruit Trees' (gardeningsolutions.ifas.ufl.edu, fetched) states the Flying "
        "Dragon dwarfing mechanism and gives NO container size. The EDIS publication it links, HS57 "
        "'Growing Fruit Crops in Containers' (Williamson), is RETIRED on EDIS (publication/HS057 "
        "404, HS155 410); the copies found are mirrors on non-extension hosts, not T1. The UF St. Lucie "
        "county blog post returns UF's 404 page. PLA-612 stays open."),
    "pea trellis ROW spacing": (
        "No T1 page read states a row spacing for a trellised pea planting. UMN's rule covers the "
        "in-row figure (same as ground); OSU's snap pea tip sheet (Spanish printable, fetched) gives "
        "2 to 4 in apart in rows, pole types needing a trellis, not trellis-conditional."),
}
