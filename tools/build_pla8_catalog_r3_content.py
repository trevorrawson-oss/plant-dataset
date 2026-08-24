#!/usr/bin/env python3
"""PLA-8 catalog round 3: four mints, each closing a batch-1 rung that had nowhere to point.

EVERY ONE OF THESE WAS FIRST RECORDED AS "UNSOURCED" AND THEN FOUND AT T1. That is the finding.
Batch-1's read flagged several crop claims as unsupported by their own cited anchors, and the
tempting response was to admit a T2 source or annotate the prose. A proper hunt found a T1 document
for every single one -- the crops were citing the WRONG documents, not making unsourceable claims.
This repo already knew that: absence findings are DOCUMENT-SCOPED, and "no extension publishes X"
was once true of two documents and false at twelve institutions.

THE HUNT ALSO CORRECTED A READ FINDING. jalapeno/pepper-weevil's rung was recorded as a
method-meaning mismatch: it names `yellow_sticky_traps` while describing a pheromone-baited trap, so
a `pheromone_trap` mint looked owed. UF/IFAS EENY-278 says yellow sticky traps ARE the published
pepper-weevil monitoring tool ("one 375 sq cm trap captures as many weevils as are detected by
inspecting 50 buds", "Traps should be placed 10 to 60 cm above the soil"), and confirms an
aggregation pheromone exists WITHOUT describing pheromone-lured traps. So the method key was right
all along and the rung's "baited with the weevil's scent lure" is an unsourced embellishment.
`pheromone_trap` IS NOT MINTED. The fix is a rung edit in promote 3.

EACH MINT NAMES WHAT IT IS NOT. Four of these sit next to an existing method that means something
close but different, which is precisely how batch 1's 22 mismatches happened:
    prompt_harvest        vs garden_sanitation  -- taking the crop you want, not removing what you don't
    sound_sowing_practice vs sensible_seeding_rate -- depth/seed/warmth, not sowing DENSITY
    augmentative_release  vs beneficial_predators -- BUYING and releasing, not conserving what is there
    resistant_rootstock   vs resistant_varieties  -- a grafted root, not a cultivar choice

SOURCES: all already-catalogued T1, NOTHING minted. Every anchor fetched and READ 2026-08-24.
`ucanr_ext` is used for ipm.ucanr.edu URLs, matching the 34 existing control_methods anchors.
"""

NEW_METHODS = {
    "prompt_harvest": {
        "name": "Prompt harvest",
        "tier": "cultural",
        # vertebrate rests on umd_ext, which links regular picking to birds and squirrels only
        # loosely; the prose below is deliberately worded to match that strength and no more.
        "applies_to": ["insect_general", "fungal_foliar", "disease_general", "vertebrate"],
        "how_it_works_beginner": (
            "Pick fruit as it ripens instead of letting it hang, and clear away anything that has "
            "gone over or dropped. Soft, over-ripe fruit is what draws sap beetles and vinegar "
            "flies, and they are what carry the organisms that sour the fruit from the inside. "
            "Tightening how often you pick leaves less of that sitting there at any one time."
        ),
        "how_it_works_seasoned": (
            "Harvest interval is the control variable. Over-ripe and fallen fruit is the substrate "
            "that recruits driedfruit beetles and vinegar flies, which are the primary carriers of "
            "the souring organisms, so shortening the interval and removing drops together lower "
            "both the attractant and the inoculum. On a crop that ripens over many weeks the "
            "planting is exposed repeatedly, which is what makes picking frequency worth treating "
            "as a control rather than as harvesting."
        ),
        "best_use": (
            "Fruit crops where over-ripe or fallen fruit feeds the problem: fig souring, fruit rots, "
            "and sap beetles, and where birds and squirrels take ripe fruit. Distinct from garden "
            "sanitation, which removes debris and culls you never intended to eat; this is about "
            "taking the crop you do want, sooner."
        ),
        "pros": [
            "Costs nothing and uses a job you are doing anyway",
            "Acts on the attractant itself, which matters where no spray reaches the organism inside the fruit",
        ],
        "cons": [
            "Needs a short, regular interval through ripening, not a single pass",
            "Does nothing about fruit already affected, which has to come off and be disposed of",
        ],
        "sources": ["ucanr_ext", "umd_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/DISEASE/figsouring.html",
                          "verified": "2026-08-24"},
            "umd_ext": {"url": "https://extension.umd.edu/resource/growing-figs-maryland",
                        "verified": "2026-08-24"},
        },
    },
    "sound_sowing_practice": {
        "name": "Sound sowing practice",
        "tier": "cultural",
        "applies_to": ["fungal_soilborne", "disease_general"],
        "how_it_works_beginner": (
            "Get the seed up fast and it spends less time at risk. Sow fresh seed at the depth it "
            "calls for rather than deeper, wait for the soil to warm enough for quick germination, "
            "and keep the bed moist without letting it sit wet. Seedlings are vulnerable to "
            "damping-off only until they are up and growing, so anything that shortens that window "
            "is doing the work."
        ),
        "how_it_works_seasoned": (
            "Damping-off risk is a function of how long the seed and hypocotyl sit in the "
            "susceptible stage, so depth, seed vigor and soil temperature act together by "
            "compressing that window: vigorously growing seedlings pass through it fairly quickly "
            "and become established plants. UC IPM puts general planting depth at about twice the "
            "width of the seed and favorable germination temperatures at 65 to 70°F for most seeds, "
            "and NC State names proper planting depth and soil temperature as the levers that "
            "assure rapid emergence. Keeping the medium moist but not saturated denies the "
            "pathogens the free water they need without checking growth."
        ),
        "best_use": (
            "Direct-sown beds and seed trays with a damping-off history, set at sowing by seed "
            "quality, depth, soil warmth and restrained watering. Distinct from sensible seeding "
            "rate, which is about sowing DENSITY and crowding rather than about how fast the seed "
            "comes up."
        ),
        "find_it_beginner": (
            "Check the seed packet for its sow-by date and its depth; if a crop has a hard or corky "
            "seed, look up whether a presoak is usual for it."
        ),
        "pros": [
            "Free, and it is set once at sowing rather than managed through the season",
            "There is no home rescue for damping-off once it starts, so the sowing decisions carry the load",
        ],
        "cons": [
            "Prevention only; it does nothing for seedlings that have already collapsed",
            "Waiting for warm-enough soil can mean sowing later than you wanted to",
        ],
        "sources": ["ucanr_ext", "ncsu_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/damping-off-diseases-in-the-garden/",
                          "verified": "2026-08-24"},
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu/damping-off-in-flower-and-vegetable-seedlings",
                         "verified": "2026-08-24"},
        },
    },
    "augmentative_release": {
        "name": "Buying and releasing natural enemies",
        "tier": "biological",
        "applies_to": ["insect_soft_bodied", "mite", "insect_general"],
        "how_it_works_beginner": (
            "You can buy predatory insects and mites and release them onto an active infestation. "
            "It can help, but it is not the strong option it sounds like: the predators need prey "
            "already present or they starve or move on, and in a garden they are free to leave. "
            "Making the garden a place resident predators want to stay generally does more, so "
            "treat a release as a top-up rather than the plan."
        ),
        "how_it_works_seasoned": (
            "Augmentative release supplements resident natural enemies rather than substituting for "
            "them. UC IPM puts it plainly: purchase and release can be useful for establishing "
            "populations in large plantings or orchards, but the best results come from creating "
            "favorable conditions for naturally occurring predators, and released predators starve "
            "or migrate elsewhere if prey is not available when they arrive. The commercially "
            "available mite predators are the western predatory mite and Phytoseiulus, and a "
            "working guideline is roughly one predator for every ten spider mites."
        ),
        "best_use": (
            "An active, located infestation you can release onto, once conservation is already in "
            "place. Distinct from beneficial predators, which is about CONSERVING the natural "
            "enemies already present and costs nothing; this one is bought, and its results are "
            "more conditional."
        ),
        "pros": [
            "Puts a living control directly into the canopy on an infestation you can see",
            "Specific to the pest, so it does not strip out the predators already working",
        ],
        "cons": [
            "Released predators starve or move on if prey is not present when they arrive",
            "Costs money and needs the right ratio and timing, and a garden is open, so they can leave",
        ],
        "cautions": [
            "Buy a release only for an infestation you have actually found; releasing ahead of the "
            "pest wastes it"
        ],
        "sources": ["ucanr_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/spider-mites/",
                          "verified": "2026-08-24"},
        },
    },
    "resistant_rootstock": {
        "name": "Grafting onto resistant rootstock",
        "tier": "cultural",
        "applies_to": ["fungal_soilborne", "disease_general"],
        "how_it_works_beginner": (
            "A grafted plant is two plants joined: the root system of a variety that resists a soil "
            "disease, carrying the top of the variety you actually want to eat. It is the way to "
            "keep growing a susceptible favorite on ground where a soil disease is established, "
            "since the roots are where these diseases get in."
        ),
        "how_it_works_seasoned": (
            "Soilborne vascular pathogens invade through the roots, so a resistant rootstock "
            "intercepts the infection court while the scion supplies the fruit. UMN states that "
            "varieties without resistance can be grafted onto disease-resistant rootstock, which is "
            "what makes it the option for heirlooms on infested ground: they carry none of the bred "
            "resistance, and the pathogen survives as resting structures in soil for many years, so "
            "rotation alone does not clear a bed."
        ),
        "best_use": (
            "A susceptible variety you want to keep growing on ground where a soilborne wilt is "
            "already established. Distinct from resistant varieties, which is choosing a different "
            "cultivar outright; here you keep the cultivar and change its roots."
        ),
        "pros": [
            "Keeps a susceptible favorite growing on ground a rotation cannot clear",
            "Acts at the root, which is where soilborne wilts get in",
        ],
        "cons": [
            "Grafted plants cost more, and grafting your own takes practice",
            "Protects against what the rootstock resists and nothing else",
        ],
        "sources": ["umn_ext"],
        "anchoring_urls": {
            "umn_ext": {"url": "https://extension.umn.edu/disease-management/fusarium-wilt",
                        "verified": "2026-08-24"},
        },
    },
}

# Each mint must name the neighbour it could be confused with, in best_use. Guarded.
DISAMBIGUATION = {
    "prompt_harvest": "garden sanitation",
    "sound_sowing_practice": "sensible seeding rate",
    "augmentative_release": "beneficial predators",
    "resistant_rootstock": "resistant varieties",
}

SOURCE_READS = [
    {"id": "ucanr_ext", "for": "prompt_harvest", "read": "2026-08-24",
     "url": "https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/DISEASE/figsouring.html",
     "quote": "Pick fruit promptly as it becomes ripe. Promptly remove and dispose of fallen and "
              "over-ripe fruit."},
    {"id": "umd_ext", "for": "prompt_harvest", "read": "2026-08-24",
     "url": "https://extension.umd.edu/resource/growing-figs-maryland",
     "quote": "Since figs are fragile and enjoyed by birds and squirrels, it's a good idea to pick "
              "fully-ripened and mostly-ripened fruits regularly."},
    {"id": "ucanr_ext", "for": "sound_sowing_practice", "read": "2026-08-24",
     "url": "https://ipm.ucanr.edu/home-and-landscape/damping-off-diseases-in-the-garden/",
     "quote": "Maximize seedling vigor and rapid emergence by using fresh, high-quality seeds."},
    {"id": "ncsu_ext", "for": "sound_sowing_practice", "read": "2026-08-24",
     "url": "https://content.ces.ncsu.edu/damping-off-in-flower-and-vegetable-seedlings",
     "quote": "Proper planting depth and soil temperature to assure rapid seeding emergence and growth."},
    {"id": "ucanr_ext", "for": "augmentative_release", "read": "2026-08-24",
     "url": "https://ipm.ucanr.edu/home-and-landscape/spider-mites/",
     "quote": "The purchase and release of predatory mites can be useful in establishing "
              "populations in large plantings or orchards, but the best results are obtained by "
              "creating favorable conditions for naturally occurring predators"},
    {"id": "umn_ext", "for": "resistant_rootstock", "read": "2026-08-24",
     "url": "https://extension.umn.edu/disease-management/fusarium-wilt",
     "quote": "Varieties without resistance can be grafted onto disease resistant root stock."},
]

# Recorded, deliberately NOT minted. Kept from r2 and updated.
NOT_MINTED = {
    "pheromone_trap": "NOT NEEDED. UF/IFAS EENY-278 shows yellow sticky traps ARE the published "
                      "pepper-weevil monitoring tool, so `yellow_sticky_traps` was the right key; "
                      "the rung's 'scent lure' clause is an unsourced embellishment, fixed in "
                      "promote 3 as a rung edit.",
    "container_culture": "third negative read (UF/IFAS VH021); still owed, still unanchored",
    "staking_support": "UMN attributes staking to airflow; the read's splash-lift rationale was "
                       "weaker than stated",
}

# Sourced advice that still has no home, recorded rather than forced into a near-miss method.
UNPLACED = {
    "heirloom-tomato/fruit-cracking": "harvest near-ripe fruit ahead of heavy rain -- prompt_harvest "
                                      "is not applies_to `physiological`, and the fig anchors do not "
                                      "cover a turgor disorder. Needs its own read of the crop's "
                                      "ncsu_ext cracking anchor before the target set is widened.",
    "artichoke/bacterial-crown-rot": "improve drainage before replanting -- improve_drainage's prose "
                                     "is water-mould-specific and this is a bacterial rot (from r2)",
}

# Found while anchoring, NOT fixed here: bird_netting's prose omits a safety point its own family of
# sources makes. UMD: "fine polyethylene netting that will not entangle birds and snakes like the
# larger holes in nylon netting." The catalog's bird_netting says nothing about mesh gauge or
# entanglement. That is a PROSE defect, and prose generalization is the deferred arc.
PROSE_ARC_NOTES = {
    "bird_netting": "omits mesh-gauge/entanglement safety point (umd_ext fig page)",
}
