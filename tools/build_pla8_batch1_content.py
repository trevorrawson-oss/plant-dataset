#!/usr/bin/env python3
"""PLA-8 batch 1: the 18 rung fixes the READ found, applied to the staged ladders before promotion.

THE STAGED CONTENT IS NOT EDITED IN PLACE. `tools/staging/pla8_ladder_batch1/out_*.json` stays
exactly as authored; this module is the DELTA applied on top of it. That keeps the authored content
reviewable against what the bots actually produced, and keeps this file to the decisions rather than
to 165 rungs of prose.

WHAT THE READ FOUND: 22 of 165 rungs (13%) named a method whose meaning differs from what the rung
says. 18 are fixed here. The remaining 4 are listed in STILL_OPEN with their reasons -- they are not
oversights and must not be quietly closed.

THE EIGHT MERGES ARE THE BULK, AND THEY ARE MERGES RATHER THAN MINTS FOR A MEASURED REASON. The read
first proposed minting a herbaceous infected-foliage method and narrowing `garden_sanitation` away
from in-season removal. Checked against shipped data, ~14 of garden_sanitation's 42 rungs on SEVEN
CERTIFIED CROPS depend on that meaning, so narrowing it would have created 14 new mismatches. Every
one of these eight ladders ALREADY carries a garden_sanitation rung saying half of the same thing,
which is why each is a merge: the two rungs were one action split across two keys.
"""

# ---------------------------------------------------------------------------------------------
# MERGE: fold the prune_out_infection rung into the garden_sanitation rung the ladder already has.
# `keep` is the surviving rung index (garden_sanitation), `drop` is the prune_out_infection rung.
# Indices are validated against the staged file and a mismatch is a REFUSAL.
# ---------------------------------------------------------------------------------------------
MERGES = [
    {
        "crop": "basil", "pid": "downy-mildew", "keep": 3, "drop": 4,
        "note_beginner":
            "Pull infected plants as soon as you find the fuzzy gray-purple growth under the "
            "leaves, and carry them out of the garden. If only part of a plant is affected, cut "
            "those heavily infected stems out instead and take them away rather than dropping them "
            "on the ground. Every infected plant left standing is shedding spores onto its "
            "neighbors.",
        "note_seasoned":
            "Prompt removal and destruction of infected plants cuts the local spore load, which "
            "matters because warm, humid weather can carry this disease across a planting inside a "
            "few days. Where a plant is only partly involved, taking out the heavily infected stems "
            "buys time instead; once infection turns systemic no organic curative applies, so treat "
            "either move as spore-load reduction rather than a cure.",
    },
    {
        "crop": "swiss-chard", "pid": "cercospora-leaf-spot", "keep": 2, "drop": 5,
        "note_beginner":
            "Pick off the worst-spotted leaves and throw them out, starting with the older outer "
            "ones where the spots turn up first. Spotted leaves will not heal, so taking them off "
            "slows the march inward toward the leaves you want to eat. At the end of the season "
            "rake up and dispose of the old chard and beet leaves and debris, and pull related "
            "weeds nearby, since that is where the fungus lives between crops.",
        "note_seasoned":
            "Spotted tissue does not recover, so removing the heavily infected older outer leaves "
            "cuts the inoculum that moves inward; it slows progression rather than arresting it, "
            "and opens the canopy slightly at the same time. Cercospora beticola then survives the "
            "off-season on infected chard and beet residue and on related weed hosts, so destroying "
            "that debris removes the reservoir that supplies the following season's splash-borne "
            "spores.",
    },
    {
        "crop": "swiss-chard", "pid": "downy-mildew", "keep": 1, "drop": 5,
        "note_beginner":
            "Strip out the leaves that are furthest gone, the twisted, thickened ones in the middle "
            "of the plant included, and bin them. They will not come back from it, and taking them "
            "off leaves less there to spread. Clear old leaves and crop leftovers from the bed as "
            "well, and stay out of the planting while the leaves are still wet, since brushing past "
            "wet plants carries it from leaf to leaf.",
        "note_seasoned":
            "Infected tissue cannot be cured, so removing the yellow-blotched and distorted leaves "
            "reduces the sporulating surface on the undersides while opening the canopy for drying. "
            "Destroy the crop residue that carries the pathogen over, and keep out of the stand "
            "while foliage is wet, when spores move most readily on contact and splash.",
    },
    {
        "crop": "heirloom-tomato", "pid": "early-blight", "keep": 4, "drop": 5,
        "note_beginner":
            "Pick off the spotted lower leaves as soon as you notice them, since getting them off "
            "the plant early slows how fast the disease climbs. Bag what you pull and put it in the "
            "trash rather than the compost pile, and clear old tomato debris out of the bed too, "
            "since the fungus rides out the winter on it.",
        "note_seasoned":
            "In-season removal of symptomatic lower leaves takes out sporulating tissue and slows "
            "the upward progression, so act on the first bullseye lesions rather than waiting for "
            "the lower canopy to yellow and shed. The pathogen overwinters on infected debris, so "
            "offsite disposal of both the removed foliage and the end-of-season residue lowers what "
            "is available to splash up the following spring. Composting symptomatic tissue keeps it "
            "in circulation.",
    },
    {
        "crop": "heirloom-tomato", "pid": "septoria-leaf-spot", "keep": 4, "drop": 5,
        "note_beginner":
            "Strip off the spotted lower leaves as soon as you find them. The sooner they are off "
            "the plant, the slower the spots climb. Send what you remove to the trash rather than "
            "the compost pile, and clear old tomato debris out of the bed, since the fungus carries "
            "over on it.",
        "note_seasoned":
            "Prompt removal of symptomatic lower leaves reduces the sporulating tissue driving "
            "defoliation from the bottom up; pair it with canopy opening rather than treating it as "
            "the alternative. Carryover lives on debris and in infested soil, so offsite disposal "
            "of removed foliage and end-of-season debris keeps that reservoir from rebuilding.",
    },
    {
        "crop": "heirloom-tomato", "pid": "late-blight", "keep": 1, "drop": 3,
        "note_beginner":
            "Pull off and bin affected leaves and stems the moment you spot them, and if a plant is "
            "badly hit, take the whole plant out so it cannot spread to its neighbors. Clear every "
            "bit of tomato debris out of the garden before winter, and send affected material to "
            "the trash rather than the compost pile.",
        "note_seasoned":
            "Immediate removal of infected tissue, and roguing whole plants that are badly "
            "affected, is the highest-value in-season action against a pathogen that can take a "
            "plant down in days. Tomato debris left in the garden over winter is the local carryover "
            "to close: bag and bin infected material, since composting it returns the tissue to the "
            "bed.",
    },
    {
        "crop": "jalapeno", "pid": "bacterial-spot", "keep": 2, "drop": 6,
        "note_beginner":
            "Take out plants that are badly spotted and shedding their leaves, since you cannot cure "
            "them and leaving them standing keeps feeding the spread down the row. Clear the old "
            "pepper plants out at the end of the season too, and keep your hands and tools off the "
            "plants while the leaves are wet, which is when the bacteria move most easily.",
        "note_seasoned":
            "Removing heavily affected plants cuts the inoculum load in the planting; infected "
            "tissue cannot be cured, so the goal is slowing spread rather than rescue, and "
            "defoliated plants also expose fruit to sunscald. Crop debris carries the bacteria over, "
            "so strip it at season's end, and note that handling wet foliage moves the pathogen "
            "plant to plant, which makes dry-weather timing part of the control.",
    },
    {
        "crop": "jalapeno", "pid": "mosaic-viruses", "keep": 2, "drop": 3,
        "note_beginner":
            "Pull any plant that is stunted with mottled, puckered leaves and get rid of it, since "
            "it will not recover and aphids feeding on it will carry the virus onward to healthy "
            "plants. Keep weeds down around the bed, wash your hands before handling the plants, "
            "and clean your tools between plants. Some of these viruses ride on hands and tools, "
            "and if you use tobacco, keep it away from your peppers.",
        "note_seasoned":
            "Rogue symptomatic plants early: they are a standing source that vectors sample, and "
            "since infected plants do not recover, removal protects the remainder of the planting. "
            "Weed reservoirs sustain the viruses between crops, and tobamoviruses move mechanically "
            "on hands, tools, and tobacco products, so hygiene between plants belongs in the control "
            "program rather than beside it.",
    },
]

# ---------------------------------------------------------------------------------------------
# REPOINT: the prose already describes the new method's action; only the KEY was wrong.
# ---------------------------------------------------------------------------------------------
REPOINTS = [
    # Fall tillage is soil disturbance, not debris removal. Found independently by two bots on two
    # crops for the same pest, which is the signature of a missing method rather than a bot error.
    {"crop": "jalapeno", "pid": "hornworms", "rung": 0,
     "from": "garden_sanitation", "to": "off_season_tillage"},
    {"crop": "heirloom-tomato", "pid": "tomato-hornworm", "rung": 0,
     "from": "garden_sanitation", "to": "off_season_tillage"},
    # "Pick ripe figs often instead of letting them hang" is prompt harvest, not sanitation.
    {"crop": "fig", "pid": "birds-and-squirrels", "rung": 0,
     "from": "garden_sanitation", "to": "prompt_harvest"},
]

# ---------------------------------------------------------------------------------------------
# MERGE_TO: two rungs collapse into ONE rung under a NEW method. Distinct from MERGES, where the
# surviving rung keeps its existing key.
# ---------------------------------------------------------------------------------------------
MERGE_TO = [
    {
        # `sensible_seeding_rate` meant DENSITY while the rung meant depth, seed freshness and a
        # presoak; `water_at_the_base` meant PLACEMENT while the rung meant moisture restraint.
        # UC IPM presents all of it as one sowing practice, so the two rungs become one.
        "crop": "swiss-chard", "pid": "damping-off", "keep": 1, "drop": 2,
        "to": "sound_sowing_practice",
        "note_beginner":
            "Sow fresh seed at the depth it calls for and resist burying it deeper, and wait for "
            "the bed to warm before sowing. Soaking chard's corky seedballs in water for a day "
            "first gets them up faster, which cuts the time they spend at risk. Keep the seedbed "
            "just moist rather than wet, and if seedlings start flopping over, hold off watering "
            "and let the surface dry down a little.",
        "note_seasoned":
            "Old or weak seed and excessive sowing depth prolong emergence and therefore exposure, "
            "so seed quality, depth and soil warmth work together by compressing the susceptible "
            "window. A day's presoak of the seedball brings emergence forward in a crop whose "
            "seedball is slow to begin with. Overwatering is the other controllable driver: keep "
            "the bed evenly moist without saturating it, and once collapse begins, withholding "
            "water to dry the surface is the main lever left.",
    },
]

# ---------------------------------------------------------------------------------------------
# SPLIT: one rung carried two distinct actions. The original rung keeps one and is rewritten to
# only that; a NEW rung is inserted for the other.
# ---------------------------------------------------------------------------------------------
SPLITS = [
    {
        # The rung was mostly clean propagation stock with a roguing tail. Both are real; they are
        # two methods.
        "crop": "fig", "pid": "fig-mosaic", "rung": 0,
        "keep_method": "certified_clean_stock",
        "keep_beginner":
            "Start with a plant or cutting whose leaves look clean and un-mottled, and do not take "
            "cuttings from a fig showing the blotchy pattern, since the virus goes along with the "
            "wood. There is no cure once a plant has it, so the stock you start from is the "
            "decision that matters.",
        "keep_seasoned":
            "Clean propagation stock is the practical lever, since the virus complex is systemic "
            "and permanent in an infected plant and moves readily in cuttings taken from it. Where "
            "you propagate your own, take wood only from an unmottled plant.",
        "insert_at": 1,
        "new_method": "garden_sanitation",
        "new_beginner":
            "Keep the fig well cared for otherwise, since many infected plants still fruit alright. "
            "If one is badly stunted and barely setting figs, taking it out is reasonable.",
        "new_seasoned":
            "Rogue out severely stunted, poor-cropping specimens; lightly affected plants often "
            "crop acceptably and can be kept in production, so this is a judgment about that plant "
            "rather than a blanket removal.",
    },
    {
        # Cultivar choice and grafting a susceptible top onto a resistant root are different
        # actions. The rung did both under `resistant_varieties`.
        "crop": "heirloom-tomato", "pid": "fusarium-verticillium-wilt", "rung": 1,
        "keep_method": "resistant_varieties",
        "keep_beginner":
            "For heirlooms this is the control that matters most. Most heirlooms have little or no "
            "resistance to these two soil fungi, while many hybrids are bred to resist them; look "
            "for V and F on a hybrid's tag. Cherokee Purple is one heirloom reported to have some "
            "tolerance.",
        "keep_seasoned":
            "The V and F of the VFN codes mark exactly the bred resistance heirlooms lack, leaving "
            "them fully susceptible where these pathogens are established. Cherokee Purple is a "
            "noted heirloom exception with some tolerance.",
        "insert_at": 2,
        "new_method": "resistant_rootstock",
        "new_beginner":
            "Where wilt has struck before, an heirloom can be grafted onto resistant rootstock, "
            "meaning the root system of a resistant plant supporting the heirloom top. That lets "
            "you keep growing the variety you want on ground a rotation cannot clear.",
        "new_seasoned":
            "On infested ground, grafting onto resistant rootstock keeps the heirloom fruit on a "
            "root system that holds up. It is the option that matters here because both pathogens "
            "persist as resting structures in soil for many years, so rotation alone does not free "
            "a bed.",
    },
    {
        # The rung did conservation (interplanting to recruit residents) AND augmentation (buying
        # and releasing). UC IPM rates conservation the better of the two, so the split keeps that
        # order: conserve first, buy second.
        "crop": "heirloom-tomato", "pid": "aphids", "rung": 2,
        "keep_method": "beneficial_predators",
        "keep_beginner":
            "Ladybugs, lacewings and small parasitic wasps feed on aphids and will usually bring an "
            "outbreak down on their own. Planting marigolds or nasturtiums near your tomatoes draws "
            "them in and gives them a reason to stay, and skipping broad sprays keeps them working.",
        "keep_seasoned":
            "Conserving resident natural enemies is the higher-return move: interplanted marigold "
            "and nasturtium recruit them without a purchase, and avoiding broad-spectrum material "
            "is what keeps them in the planting.",
        "insert_at": 3,
        "new_method": "augmentative_release",
        "new_beginner":
            "You can also buy ladybugs or lacewings and release them onto active clusters. Treat it "
            "as a top-up rather than the plan: they need aphids already there or they move on, and "
            "in an open garden they are free to leave.",
        "new_seasoned":
            "Released predators supplement the resident population rather than replacing it. UC IPM "
            "notes the best results come from creating favorable conditions for naturally occurring "
            "predators, and that released predators starve or migrate elsewhere if prey is not "
            "available when they arrive, so time a release to a located infestation.",
    },
]

# ---------------------------------------------------------------------------------------------
# REPOINT_REWRITE: the key changes AND the prose needs rewriting to match the new method.
# ---------------------------------------------------------------------------------------------
REPOINT_REWRITES = [
    {
        # Purely augmentative already ("you can buy and release predatory mites"), but it carried
        # none of the source's limiting half.
        "crop": "heirloom-tomato", "pid": "spider-mites", "rung": 2,
        "from": "beneficial_predators", "to": "augmentative_release",
        "note_beginner":
            "You can buy and release predatory mites, which are mites that hunt spider mites, so a "
            "living control is working on the plants for you. Release them onto an infestation you "
            "have actually found: with no spider mites to eat, they starve or move on.",
        "note_seasoned":
            "Released predatory mites put a control into the canopy itself, which is useful late in "
            "the season when spider mite populations are compounding fastest. UC IPM names the "
            "western predatory mite and Phytoseiulus as the commercially available species and puts "
            "a working ratio at about one predator per ten spider mites, while noting that the best "
            "results still come from favoring the predators already present.",
    },
]

# ---------------------------------------------------------------------------------------------
# EDIT_NOTES: the method key was RIGHT; the prose carried an unsourced claim.
# ---------------------------------------------------------------------------------------------
EDIT_NOTES = [
    {
        # THE HUNT CORRECTED THE READ HERE. This was recorded as a method-meaning mismatch, which
        # would have meant minting `pheromone_trap`. UF/IFAS EENY-278 shows YELLOW sticky traps are
        # the published pepper-weevil monitoring tool; the key was right and the rung's
        # "baited with the weevil's scent lure" was the unsourced part. Neither of the problem's two
        # cited anchors (uc_ipm, ncsu_ext) mentions traps at all, so the correct anchor is added.
        "crop": "jalapeno", "pid": "pepper-weevil", "rung": 2,
        "expect_method": "yellow_sticky_traps",
        "note_beginner":
            "Set yellow sticky traps around the edge of the bed, down low near the soil, so you "
            "catch the first arrivals before buds start yellowing and dropping. One card watches "
            "the planting for you between hand inspections.",
        "note_seasoned":
            "Yellow sticky traps give early detection: UF/IFAS reports a single trap catching as "
            "many weevils as inspecting 50 buds, set roughly 4 to 24 inches above the soil. "
            "Catching the first adults tells you what pressure the sanitation program is facing "
            "well before bud and fruit drop announces it.",
    },
]

# A cited anchor that does not support the claim is MIS-ANCHORED, not unsourceable. This adds the
# document the claim actually comes from.
ADD_SOURCES = [
    {"crop": "jalapeno", "pid": "pepper-weevil", "source": "uf_ifas_edis",
     "url": "https://ask.ifas.ufl.edu/publication/IN555", "verified": "2026-08-24",
     "why": "UF/IFAS EENY-278. The trap claim is not in uc_ipm's pepper weevil page or ncsu_ext's "
            "pests-of-pepper, both fetched and read. This is the document it comes from."},
]

# ---------------------------------------------------------------------------------------------
# NOT FIXED. Each is a decision, not an oversight, and the guard suite asserts they remain.
# ---------------------------------------------------------------------------------------------
STILL_OPEN = {
    "fig/root-knot-nematode":
        "`garden_sanitation` carries site selection plus container culture. Needs `container_culture`, "
        "which has THREE negative source reads (UC IPM nematode note, UF/IFAS VH021, and the crop's "
        "own anchors). Not mintable yet.",
    "swiss-chard/root-knot-nematode":
        "`crop_rotation` carries five controls in one note, including container culture and "
        "cool-season scheduling. Same missing method.",
    "jalapeno/pepper-maggot":
        "A padded 4-rung ladder on a problem the crop's own source says jalapeno largely escapes. "
        "Trevor ruled LEAVE on 2026-08-24.",
    "heirloom-tomato/fruit-cracking":
        "`even_watering` explains calcium movement on a turgor disorder. The action is right and the "
        "METHOD PROSE is wrong, which belongs to the deferred prose-generalization arc, not here.",
}

EXPECTED_FIX_COUNT = 18
