#!/usr/bin/env python3
"""Split `bottom_watering`: mint `water_at_the_base` and revert a widening that was attached to the
wrong entry. Base 208e213c.

THE DEFECT, found by READING the pilot batch and not by any gate. `bottom_watering`'s catalog entry
says "Water FROM BELOW so the surface of the MIX stays drier", best_use "Indoor trays and seedlings,
especially microgreens". The two rungs already shipped on microgreens-mix use it exactly that way.
But ALL TWELVE rungs in the pilot batch use it to mean something else: water at the BASE rather than
overhead, on outdoor plants. Zero of twelve mean tray bottom-watering. You do not bottom-water a fig.

AND THE WIDENING I SHIPPED IN d19abe60 WAS ATTACHED TO THE WRONG METHOD. I added `bacterial` and
`mollusk` to `bottom_watering` on the strength of UC IPM sources about OVERHEAD-VS-BASE irrigation
("change from overhead to furrow irrigation", "switching from sprinkler irrigation to drip"). Neither
describes bottom-watering. That is the exact defect I had refused an hour earlier for
`balance_nitrogen` and `straw_mulch` -- applies_to governs what the GATE accepts and does nothing to
the PROSE -- committed in the promote immediately before. Every gate passed; the mutation harness
passed 11/11. No guard can see that a method means a different ACTION from what its rungs describe.

THE FIX, ruled with Trevor 2026-08-23:
  * `bottom_watering` KEEPS its tray/seedling meaning and REVERTS to its original applies_to and
    sources. The two microgreens rungs already in canonical stay correct and untouched.
  * `water_at_the_base` is minted for the outdoor control, carrying the targets and the two sources
    that were wrongly attached to bottom_watering, plus a foliar anchor.
  * The 12 pilot rungs repoint to it. They are unpromoted scratch, so nothing shipped is wrong yet.

SOURCES, all fetched and read; all three already catalogued T1, so nothing is minted:
  clemson_hgic              foliar splash -- "don't wet tomato foliage with irrigation water" and
                            "Keep foliage dry ... avoid overhead watering, especially late in the day"
  ucanr_ext_bacterial_speck bacterial -- "change from overhead to furrow irrigation" (MOVED here from
                            bottom_watering, where it was its only user)
  ucanr_ext_snails_slugs    mollusk -- "Switching from sprinkler irrigation to drip irrigation will
                            reduce humidity and moist surfaces" (still also used by `handpick`)
"""
NEW_METHOD = {
    "water_at_the_base": {
        "name": "Water at the base",
        "tier": "cultural",
        "applies_to": ["fungal_foliar", "fungal_soilborne", "bacterial", "mollusk"],
        "how_it_works_beginner": (
            "Put the water on the ground at the foot of the plant instead of spraying it over the "
            "leaves. Most leaf diseases travel in splashing droplets and need the foliage to stay "
            "wet to take hold, so a plant whose leaves stay dry gives them far less to work "
            "with. Watering early in the day helps for the same reason: the surface has hours to dry."
        ),
        "how_it_works_seasoned": (
            "Two mechanisms, not one. Directing irrigation to the soil removes the splash that "
            "carries spores and bacteria from soil and lower foliage onto clean tissue, and it "
            "shortens the leaf-wetness period that most foliar pathogens need to germinate. On a "
            "damp-loving pest such as a slug it works differently again, by drying the surface "
            "before the nocturnal feeding window rather than by interrupting any infection."
        ),
        "best_use": (
            "Outdoor plantings with splash-dispersed foliar disease, and beds where slugs are "
            "sustained by a surface that stays damp. Distinct from bottom watering, which is a "
            "tray and seedling technique for keeping a potting mix surface dry."
        ),
        "find_it_beginner": (
            "A watering can with the rose taken off, a hose laid at the soil, or a soaker line. "
            "Anything that keeps the spray off the leaves."
        ),
        "pros": [
            "Removes the dispersal route rather than treating the plant, so it helps every "
            "splash-spread problem in the bed at once",
            "Costs nothing beyond changing how you already water",
        ],
        "cons": [
            "Preventive only; it does nothing for tissue already infected",
            "Rain does the same job as overhead watering, so in a wet spell it buys much less",
        ],
        "sources": ["clemson_hgic", "ucanr_ext_bacterial_speck", "ucanr_ext_snails_slugs"],
        "anchoring_urls": {
            "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/tomato-diseases-disorders/",
                             "verified": "2026-08-23"},
            "ucanr_ext_bacterial_speck": {"url": "https://ipm.ucanr.edu/agriculture/tomato/bacterial-speck/",
                                          "verified": "2026-08-23"},
            "ucanr_ext_snails_slugs": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html",
                                       "verified": "2026-08-23"},
        },
    }
}

# bottom_watering reverts to exactly what it was before d19abe60 widened the wrong entry.
REVERT = {
    "applies_to": ["fungal_soilborne", "insect_general"],
    "sources": ["ucanr_ext", "umn_ext"],
    "drop_anchors": ["ucanr_ext_bacterial_speck", "ucanr_ext_snails_slugs"],
}
