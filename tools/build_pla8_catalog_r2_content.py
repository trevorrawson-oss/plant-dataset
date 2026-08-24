#!/usr/bin/env python3
"""PLA-8 catalog round 2: two mints, one narrowing, and the artichoke repoint it requires.

WHY THIS SHAPE, AND WHY IT IS SMALLER THAN THE READ SUGGESTED.

The batch-1 read found 8 rungs naming `prune_out_infection` for what is actually leaf-picking or
whole-plant roguing on herbaceous crops. The obvious fix -- mint a herbaceous removal method and
narrow `garden_sanitation` away from in-season removal -- WAS CHECKED AGAINST SHIPPED DATA AND
ABANDONED. `garden_sanitation`'s best_use already claims "in-season removal of the first infected
leaves", and **~14 of its 42 rungs on the 7 already-certified crops depend on exactly that**:
broccoli downy mildew "Strip off the worst-affected leaves", strawberry gray mold "Pick off and
destroy moldy berries", celery pink rot, asparagus rust, artichoke botrytis. Narrowing it would
have manufactured ~14 NEW method-meaning mismatches on live certified data -- the defect this arc
exists to remove. So `garden_sanitation` is LEFT ALONE and the 8 batch-1 rungs merge into the
`garden_sanitation` rung each of those ladders ALREADY carries (all 8 do; that is promote 3).

WHAT NARROWS INSTEAD IS `prune_out_infection`, AND THE AXIS IS THE ACTION, NOT THE HOST. The first
draft narrowed it to woody hosts. That was wrong: `artichoke/botrytis-gray-mold` says "Cut out
infected parts back into clean tissue", which is the same action on a herbaceous perennial and is
CORRECT. The distinguishing action is cutting BEYOND THE VISIBLE MARGIN INTO CLEAN TISSUE, versus
simply removing the affected part. Narrowed on that axis, `apple/fire-blight` and
`artichoke/botrytis-gray-mold` both stay correct and the two genuine misuses fall out.

THE DEFECT IS ALREADY LIVE IN CERTIFIED DATA, which is why this promote touches artichoke:
  * `artichoke/artichoke-curly-dwarf` rung 2 -- "grow from seed rather than from divisions off an
    old plant". That is clean planting stock, not pruning.
  * `artichoke/bacterial-crown-rot` rung 2 -- "Take out affected plants completely, roots and all,
    RATHER THAN trying to cut back to healthy tissue." A rung filed under "Pruning out infections"
    that explicitly instructs the reader NOT to perform the method's action.
Narrowing without repointing these would leave two mismatches on a certified crop.

SOURCES: all already-catalogued T1, NOTHING minted. Every anchor below was fetched and READ
2026-08-24, not taken from an existing paraphrase.

WHAT WAS **NOT** MINTED, AND WHY -- the playbook's "do not mint one you cannot anchor" rule:
  * `pheromone_trap`. jalapeno/pepper-weevil's rung says "Pheromone-baited sticky traps give early
    detection". BOTH of that problem's cited anchors were fetched and read: UC IPM's pepper weevil
    page and NC State's pests-of-pepper page say NOTHING about pheromone, lure, or sticky traps.
    The claim is very likely real in the wider literature, so this is MIS-ANCHORED rather than
    false -- it needs a source hunt, not a mint on faith.
  * `container_culture`. THIRD negative read: UF/IFAS VH021 (chard root-knot's own anchor) mentions
    containers only as an aside in its introduction and gives no guidance on containers against
    nematodes. Still owed, still unanchored.
  * `staking_support`. **A CORRECTION TO THE READ'S OWN FINDING.** The read claimed staking is a
    distinct mechanism from `airflow_spacing` (lifting foliage clear of splash). UMN attributes
    staking explicitly to airflow -- "Stake or trellis your tomatoes" to "increase air circulation
    around your plants and help leaves dry quickly". The splash-lift rationale was weaker than the
    read stated, so nothing is minted on it.
"""

# --------------------------------------------------------------------------- mints
NEW_METHODS = {
    "off_season_tillage": {
        "name": "Off-season tillage",
        "tier": "cultural",
        "applies_to": ["insect_chewing", "insect_general"],
        "how_it_works_beginner": (
            "Turn the soil over in the bed once the crop is finished. Some caterpillars drop off "
            "the plant and spend the winter underground as pupae, the resting stage between "
            "caterpillar and moth. Digging the bed opens those chambers up and leaves the pupae "
            "exposed to cold, to birds, and to drying out, so fewer moths reach next year's crop."
        ),
        "how_it_works_seasoned": (
            "Working the top few inches of a finished bed disrupts the pupal cells of soil-pupating "
            "Lepidoptera such as the hornworms, killing some outright and exposing the rest to "
            "predation and desiccation. It acts on next season's emerging adults rather than on "
            "anything currently feeding, so the payoff is a year out and the timing is after "
            "harvest, not during it."
        ),
        "best_use": (
            "A finished bed that carried a soil-pupating caterpillar such as tomato or tobacco "
            "hornworm, worked once after harvest. Distinct from garden sanitation, which clears "
            "plant debris off the surface rather than disturbing the soil the pupae are sitting in."
        ),
        "pros": [
            "Free, needs no product, and acts on the overwintering stage rather than the feeding one",
            "One pass after harvest, on ground you are clearing anyway",
        ],
        "cons": [
            "Does nothing for the current season's caterpillars, which are already feeding",
            "Only reaches pests that pupate in the soil of that bed, and adults can fly in from elsewhere",
        ],
        "cautions": [
            "Tillage works against no-dig beds and against soil structure and earthworms, so weigh "
            "it where the pest pressure is light and handpicking is keeping up"
        ],
        "sources": ["umn_ext"],
        "anchoring_urls": {
            "umn_ext": {"url": "https://extension.umn.edu/yard-and-garden-insects/tomato-hornworms",
                        "verified": "2026-08-24"},
        },
    },
    "certified_clean_stock": {
        "name": "Clean planting stock",
        "tier": "cultural",
        "applies_to": ["viral", "bacterial", "fungal_foliar", "fungal_soilborne", "disease_general"],
        "how_it_works_beginner": (
            "Start the planting from material that is not already carrying the disease: tested or "
            "treated seed, healthy bought transplants, or, if you propagate your own, cuttings, "
            "crowns or divisions taken only from a clean plant. Several diseases arrive inside the "
            "planting material rather than blowing in later, and for most of those there is no cure "
            "once a plant has it, so this is the decision that does the work."
        ),
        "how_it_works_seasoned": (
            "Seed- and propagule-borne inoculum starts an epidemic inside the planting rather than "
            "at its edge, which is why clean stock sits ahead of every in-season measure for these "
            "diseases. Basil downy mildew is seed-borne, and seed is now lab-tested and steam "
            "treated for it, though basil seed is not amenable to hot-water treatment because it "
            "produces a gelatinous exudate in water. Artichoke curly dwarf runs the other way: "
            "there is no evidence it is seedborne, so seed and the transplants raised from it are "
            "the clean route into new ground where a crown division would carry the virus in."
        ),
        "best_use": (
            "Diseases that travel in the planting material itself: seed-borne foliar and vascular "
            "pathogens, and viruses carried in cuttings, crowns or divisions. Set once, at purchase "
            "or propagation, before anything is in the ground."
        ),
        "find_it_beginner": (
            "Look for seed sold as certified disease-free, pathogen-tested, or steam or hot-water "
            "treated; for transplants, inspect them before buying and pass over any with spotting, "
            "mottling or wilt."
        ),
        "pros": [
            "Acts before planting, on diseases that have no cure once the plant has them",
            "One decision covers the whole planting, and it costs nothing extra to inspect a transplant",
        ],
        "cons": [
            "Does nothing about the same disease blowing or splashing in from outside the garden",
            "Tested or treated seed is not offered for every crop, and not every treatment suits every seed",
        ],
        "sources": ["cornell_ext", "ucanr_ext"],
        "anchoring_urls": {
            "cornell_ext": {
                "url": "https://www.vegetables.cornell.edu/pest-management/disease-factsheets/basil-downy-mildew/",
                "verified": "2026-08-24"},
            "ucanr_ext": {
                "url": "https://ipm.ucanr.edu/agriculture/artichoke/artichoke-curly-dwarf/",
                "verified": "2026-08-24"},
        },
    },
}

# --------------------------------------------------------------------------- narrowing
# `prune_out_infection` keeps its fire-blight worked example and its applies_to. What changes is
# that it now states the ACTION that distinguishes it, and names where the other action belongs.
NARROW = {
    "key": "prune_out_infection",
    "best_use": {
        "old": ("The core fire blight control on a backyard apple or pear: cut well below each "
                "strike and destroy the prunings, since no spray will cure an infection already "
                "in the wood."),
        "new": ("Cutting an infection out of a stem or branch by taking the cut well beyond the "
                "visible margin, back into clean tissue, and destroying what comes off. The core "
                "fire blight control on a backyard apple or pear. Distinct from garden sanitation, "
                "which is where simply picking off a spotted leaf or a rotted fruit, or pulling a "
                "plant that cannot be saved, belongs."),
    },
    "how_it_works_beginner": {
        "old": ("For fire blight there is no spray that cures the tree. You cut off the infected "
                "branches well below the damage and destroy them, physically removing the bacteria "
                "before they spread further into the tree."),
        "new": ("What matters here is where you cut, not that you cut. You take the blade well "
                "below the visible damage, into tissue that is still clean, so the part of the "
                "infection you cannot see comes off with the part you can. For fire blight there is "
                "no spray that cures the tree, so cutting the infected branches out and destroying "
                "them is the control."),
    },
    "how_it_works_seasoned": {
        "old": ("The location of the cut matters more than sterilizing tools, though dipping shears "
                "in 10% bleach between cuts is reasonable."),
        "new": ("The location of the cut matters more than sterilizing tools, though dipping shears "
                "in 10% bleach between cuts is reasonable. Where the affected part is simply "
                "removed rather than cut back into clean tissue, a spotted leaf picked off, a "
                "rotted fruit taken away, a plant too far gone to save pulled out, that is garden "
                "sanitation and not this."),
    },
}

# --------------------------------------------------------------------------- artichoke repoint
# (problem id, rung index, expected current method, new method or None to DROP, new notes or None)
ARTICHOKE = [
    {
        "id": "artichoke-curly-dwarf",
        "rung": 1,
        "from": "prune_out_infection",
        "to": "certified_clean_stock",
        # prose already describes clean planting stock exactly; it is the KEY that was wrong.
        "notes": None,
        "why": ("The rung says 'grow from seed rather than from divisions off an old plant' and its "
                "seasoned half attributes to UC IPM, whose artichoke curly dwarf page reads "
                "'If propagating by crowns, use only disease-free stock' and 'There is no evidence "
                "that artichoke curly dwarf virus is seedborne'. That is clean planting stock. The "
                "prose was right and the method key was wrong, so only the key moves."),
    },
    {
        "id": "bacterial-crown-rot",
        "rung": 1,
        "from": "prune_out_infection",
        "to": None,          # DROP; its roguing content merges into rung 0
        "notes": None,
        "why": ("The rung reads 'Take out affected plants completely, roots and all, RATHER THAN "
                "trying to cut back to healthy tissue' -- it instructs the reader NOT to perform "
                "the method it is filed under. Its roguing content merges into rung 0's "
                "garden_sanitation note, which already covers clean crowns and clearing rotted "
                "material. It is NOT repointed to `improve_drainage`: that method's prose explains "
                "water-mould disease ('Phytophthora and the other soilborne rots are water-mold "
                "diseases'), and this is a BACTERIAL rot, so moving it there would recreate the "
                "exact prose mismatch this promote removes. The drainage-before-replanting advice "
                "is therefore an UNPLACED CONTROL, recorded, pending the deferred prose arc. "
                "This rung also carried note_seasoned = None, a missing register half that every "
                "gate passes."),
    },
]

# rung 0 of bacterial-crown-rot absorbs the roguing sentence.
ARTICHOKE_MERGE = {
    "id": "bacterial-crown-rot",
    "rung": 0,
    "field": "note_beginner",
    "old": ("Do not use crowns off an infected plant for propagation, and clear out rotted material "
            "rather than leaving it in the bed. If you grow artichoke as a yearly crop from seed or "
            "bought transplants, you may never see this at all."),
    # "completely" reworded out: the copy-hygiene guard flags it as an absolute, and although it is
    # descriptive here rather than a claim, the positive phrasing is better copy. Same call the
    # water_at_the_base promote made on two descriptive uses of "never".
    "new": ("Do not use crowns off an infected plant for propagation, and clear out rotted material "
            "rather than leaving it in the bed. Once a plant is affected, lift it out with its "
            "roots rather than trying to cut back to healthy tissue. If you grow artichoke as a "
            "yearly crop from seed or bought transplants, you may never see this at all."),
}

SOURCE_READS = [
    {"id": "umn_ext", "for": "off_season_tillage", "read": "2026-08-24",
     "url": "https://extension.umn.edu/yard-and-garden-insects/tomato-hornworms",
     "quote": "Till the soil after harvest to destroy burrowing caterpillars and pupae."},
    {"id": "cornell_ext", "for": "certified_clean_stock", "read": "2026-08-24",
     "url": "https://www.vegetables.cornell.edu/pest-management/disease-factsheets/basil-downy-mildew/",
     "quote": "Seed companies (including High Mowing Organic Seeds) are starting to steam treat "
              "basil seed. It is not amenable to hot-water treatment because while in water the "
              "seed produces a gelatinous exudate."},
    {"id": "ucanr_ext", "for": "certified_clean_stock", "read": "2026-08-24",
     "url": "https://ipm.ucanr.edu/agriculture/artichoke/artichoke-curly-dwarf/",
     "quote": "If propagating by crowns, use only disease-free stock."},
]

# Recorded, deliberately NOT minted or fixed here.
NOT_MINTED = {
    "pheromone_trap": "both cited anchors read and silent; mis-anchored, needs a source hunt",
    "container_culture": "third negative read (UF/IFAS VH021); still owed",
    "staking_support": "UMN attributes staking to airflow; the read's splash-lift rationale was weaker than stated",
}
UNPLACED = {
    "artichoke/bacterial-crown-rot": "improve drainage before replanting -- improve_drainage's prose "
                                     "is water-mould-specific and this is a bacterial rot",
}
