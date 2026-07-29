#!/usr/bin/env python3
"""Artichoke GS arc -- the consumer compounds: growth stages, pests, diseases, notifications,
weather triggers, failure diagnostics and staged tips.

EVERY LADDER RUNG BELOW WAS READ IN THE FETCHED SOURCE DURING THIS ARC, not carried from a
research summary. The UC IPM artichoke pages were pulled as raw HTML and the management sections
read directly, because the one thing this suite cannot tolerate is a control recommendation that
nobody checked.

TWO DELIBERATE OMISSIONS, both stated rather than silent:

  `resistant_varieties` DOES NOT APPEAR IN THE VERTICILLIUM LADDER, even though it is the obvious
  first rung for a soilborne wilt on almost any other crop. No extension source publishes a
  cultivar-by-disease rating for artichoke, and the two statements that come closest contradict
  each other: UC IPM says all annual varieties are MORE susceptible than perennial Green Globe,
  and UC ANR 7221 says all artichoke varieties are susceptible. A `resistant_varieties` rung would
  tell a grower to do something no source can tell them how to do.

  NO VERTEBRATE PROBLEM IS CARRIED. UC ANR 7221 names gophers and voles for commercial fields, but
  UC IPM's artichoke pest guidelines have no vertebrate section at all and the only published
  ladder is the phrase "trapping and baits". There is also no vertebrate control method in the
  shared catalog that fits a burrowing rodent. Omitted for lack of a real ladder rather than
  because the animals do not exist.

TIER ORDER IS MONOTONIC IN EVERY LADDER: cultural, physical, biological, soft_chemical,
conventional. Short ladders are valid, and three of these terminate early on purpose -- see the
spider mite note in particular, where UC states outright that miticides are not available.
"""

# =============================================================================================
# Growth stages -- chosen so they describe BOTH modes of a dual-mode crop
# =============================================================================================
#
# The obvious stage list for a perennial (establishment / cropping / dormancy) describes six of
# artichoke's 39 cells. The obvious list for an annual describes the other 25 and has no dormancy
# at all. These four work for both, because they follow the PLANT rather than the bed: a seedling
# that must be chilled, a plant that must bulk up, buds, and then an ending that is a cut-back in
# one mode and a compost heap in the other.

GROWTH_STAGES = [
    {
        "id": "seedling_and_chill",
        "name": "Seedling and cold treatment",
        "audience": "core",
        "what_to_look_for_seasoned": (
            "Germination in 8 to 14 days at 65°F to 82°F soil, then steady leaf production toward "
            "the four-to-six-leaf stage that is the trigger point for chilling. Watch root "
            "development against cell depth, since the taproot circles in a shallow tray; deep "
            "three-to-four-inch cells are what Virginia Cooperative Extension advises."),
        "what_to_look_for_beginner": (
            "Seeds come up in one to two weeks in warm soil. After that you are counting leaves, "
            "because when each seedling has four to six real leaves it is time for its cold "
            "treatment. Use deep pots, since artichoke sends a long root straight down early."),
        "user_action_seasoned": (
            "At four to six true leaves, move the seedlings to 35°F to 50°F for about three weeks, "
            "with light if you can supply it. Do not shorten it: a replicated Maine trial measured "
            "3 to 33 percent flowering after 303 hours against 68 to 100 percent after 550. "
            "Afterwards hold them under 80°F, because heat reverses accumulated chilling."),
        "user_action_beginner": (
            "Once a seedling has four to six real leaves, give it about three weeks somewhere "
            "between 35°F and 50°F. A spare refrigerator, cold frame or unheated garage all work. "
            "This is the step that decides whether you get artichokes at all, so do not skip it or "
            "cut it short, and keep the plants under 80°F afterwards."),
        "log_prompt_seasoned": "Note the date chilling started and ended, and the temperature held.",
        "log_prompt_beginner": "Write down when you started and finished the cold treatment.",
    },
    {
        "id": "establishment",
        "name": "Establishment",
        "audience": "core",
        "what_to_look_for_seasoned": (
            "New leaf initiation within a fortnight of set-out is the sign the plant has taken. "
            "Expect slow visible progress at first while root mass builds. In cold regions the "
            "transplant is frost-tender at this point, which is the case the archetype's A24 "
            "carve-out deliberately does NOT cover for this crop."),
        "what_to_look_for_beginner": (
            "For the first couple of weeks the plant will not look like it is doing much. That is "
            "normal, it is growing roots. New leaves appearing from the center means it has "
            "settled in."),
        "user_action_seasoned": (
            "Water consistently through the fortnight after transplanting; this and the bud period "
            "are the two windows that cannot be missed. Mulch two to three inches. Where a hard "
            "freeze threatens a young transplant, cover it, since 25°F is the management floor."),
        "user_action_beginner": (
            "Keep the soil evenly moist for the first few weeks and mulch around the plants. If a "
            "hard frost is coming, throw a row cover or a bucket over them overnight."),
        "log_prompt_seasoned": "Record the set-out date and any frost protection used.",
        "log_prompt_beginner": "Note the date you planted them out.",
    },
    {
        "id": "budding",
        "name": "Budding and harvest",
        "audience": "core",
        "what_to_look_for_seasoned": (
            "A stalk rises from the rosette carrying one terminal bud and two or three smaller "
            "secondaries below it. Bud production commences 60 to 100 days after transplanting. "
            "Watch bract tightness rather than diameter, and watch it daily above 86°F, where "
            "buds open quickly and the heart loses tenderness and compactness."),
        "what_to_look_for_beginner": (
            "A thick stalk pushes up out of the middle of the plant with one big bud on top and a "
            "few smaller ones below. This starts about two to three months after you planted out. "
            "Check them every few days, and every day in hot weather."),
        "user_action_seasoned": (
            "Cut while the bracts are still closed flat, taking 2 to 3 inches of stem. Terminal "
            "bud first, secondaries as they size up. Do not let the plant go dry from bud "
            "initiation onward, which is what causes black tip and loose, early-opening buds."),
        "user_action_beginner": (
            "Cut each bud while it is still tight and firm, with 2 to 3 inches of stem attached. "
            "Take the big one at the top first. Keep the water up now, because a plant that dries "
            "out at this stage gives you tough buds with brown tips."),
        "log_prompt_seasoned": "Log first harvest date, bud count and typical bud diameter.",
        "log_prompt_beginner": "Note when you picked your first one and how many you got.",
    },
    {
        "id": "after_harvest",
        "name": "After harvest",
        "audience": "core",
        "what_to_look_for_seasoned": (
            "What happens here is the one thing that differs completely between the two modes. "
            "Where the planting persists, the crown is alive and will push new shoots after a "
            "cut-back. Where it does not, the plant is finished by the first hard freeze or by a "
            "hot wet summer, and there is nothing to carry over."),
        "what_to_look_for_beginner": (
            "This is where it matters whether artichoke lives through the winter where you are. In "
            "mild-winter places the plant carries on and will grow again from the base. In colder "
            "places, the first hard freeze ends it."),
        "user_action_seasoned": (
            "Perennial mode: cut plants to ground level to stimulate new shoots, on the schedule "
            "the region's cells give, and mulch where winter minima approach the crown-kill line. "
            "Annual mode: pull and compost, and plan next year's sowing date backwards from your "
            "chilling window. Container growers in cold regions have a third option, storing the "
            "pot dark at 32°F to 35°F over winter."),
        "user_action_beginner": (
            "If your plants survive winter where you live, cut them right down and mulch them "
            "heavily in fall. If they do not, pull them out and start again next year. If yours "
            "is in a pot, you can cut it back and keep the pot somewhere dark and just above "
            "freezing until spring."),
        "log_prompt_seasoned": "Record whether the planting was carried over or replaced, and why.",
        "log_prompt_beginner": "Note whether you kept the plants or pulled them out.",
    },
]

# =============================================================================================
# Pests
# =============================================================================================

PESTS = [
    {
        "id": "artichoke-plume-moth",
        "type": "insect",
        "name": "Artichoke plume moth (Platyptilia carduidactyla)",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "The single most effective thing you can do, and it is a once-a-year job: cut "
                    "the plants right down to ground level and get rid of the tops. The "
                    "caterpillars live inside the plant, so clearing it out is what breaks the "
                    "cycle."),
                "note_seasoned": (
                    "UC IPM quantifies this rung, which is rare: cutting plants off 2 to 3 inches "
                    "below soil level, shredding the tops and incorporating them reduces plume "
                    "moth infestations in perennial fields by about 95 percent. Nothing else on "
                    "this ladder comes close. In a home planting, cut down, chop and bury the "
                    "residue under at least 6 inches of soil, and clear thistles and related "
                    "plants nearby, since they host it too."),
            },
            {
                "method": "handpick",
                "note_beginner": (
                    "Learn to spot an infested bud, which shows small holes and frass around the "
                    "base, and pick it off straight away whatever size it is. Do not leave it on "
                    "the plant hoping it will come good."),
                "note_seasoned": (
                    "UC IPM's instruction is to identify infested buds and pick them immediately "
                    "regardless of stage of maturity, then remove them from the planting. "
                    "Sacrificing an immature bud is worth it, since the larva inside will "
                    "otherwise complete development in place."),
            },
            {
                "method": "beneficial_nematodes",
                "note_beginner": (
                    "When planting or replanting, you can soak the crowns in a solution of "
                    "beneficial nematodes first. Done properly it is very effective at keeping a "
                    "new planting clean."),
                "note_seasoned": (
                    "A preplant soak of replant stumps in Steinernema carpocapsae is UC IPM's "
                    "recommendation, and it reports that done correctly this can reduce plume moth "
                    "infestations to under 1 percent and cut first-year treatments. Note the "
                    "contrast with in-season nematode applications, which UC describes as not "
                    "reliable; the value is in the preplant soak specifically."),
            },
            {
                "method": "bt",
                "note_beginner": (
                    "Bt is a naturally occurring bacterium that only affects caterpillars, so it "
                    "is safe around bees and beneficial insects. Spray when you see fresh damage, "
                    "and repeat, because it does not last long on the plant."),
                "note_seasoned": (
                    "Bacillus thuringiensis applied by itself is on UC IPM's organically "
                    "acceptable list for this pest. Timing is everything, since the larva bores "
                    "into the bud early and is protected from contact materials once inside, so "
                    "sprays have to land on young larvae before they enter."),
            },
            {
                "method": "spinosad",
                "note_beginner": (
                    "If the earlier steps have not held, spinosad is the next option and is "
                    "allowed in organic growing. Spray at dusk to spare bees."),
                "note_seasoned": (
                    "The Entrust formulation of spinosad is UC IPM's other organically acceptable "
                    "in-season material for plume moth. It is toxic to bees while wet, so apply at "
                    "dusk. Do not expect it to rescue a planting that has skipped the annual "
                    "cut-back, which is the rung that does the real work."),
            },
        ],
    },
    {
        "id": "artichoke-aphid",
        "type": "insect",
        "name": "Artichoke aphid (Capitophorus elaeagni)",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Clear out the old plant material as soon as you have finished harvesting. "
                    "That is where the next generation builds up."),
                "note_seasoned": (
                    "UC IPM's cultural control for this aphid is one line and this is it: destroy "
                    "crop residue immediately after harvest. Outbreaks are most likely during "
                    "periods of high average daily temperature coupled with high humidity, so "
                    "residue left through a warm humid spell is the worst case."),
            },
            {
                "method": "water_spray",
                "note_beginner": (
                    "A firm jet of water knocks aphids off and most of them do not make it back. "
                    "Repeat every few days while numbers are building."),
            },
            {
                "method": "beneficial_predators",
                "note_beginner": (
                    "Ladybugs, lacewings, hoverfly larvae and tiny parasitic wasps all work on "
                    "these aphids, and they usually arrive on their own if you do not spray. Give "
                    "them a week or two before reaching for anything stronger."),
                "note_seasoned": (
                    "Parasitic wasps in Diaeretiella and Lysiphlebus, plus ladybugs, syrphid fly "
                    "larvae, lacewings and the fungus Entomophthora aphidis all attack it. UC "
                    "IPM's advice is to preserve them by avoiding unnecessary insecticide "
                    "applications, and notes a lag between aphid buildup and the natural enemy "
                    "response, so patience is part of the method."),
            },
            {
                "method": "insecticidal_soap",
                "note_beginner": (
                    "Insecticidal soap works on aphids but only where it actually lands, so spray "
                    "thoroughly including under the leaves. It has no lasting effect, which is "
                    "also why it is gentle on the helpful insects."),
            },
            {
                "method": "neem_oil",
                "note_beginner": (
                    "Neem oil is the next step and is allowed in organic growing. Do not spray oil "
                    "in hot weather or in strong sun, since it can burn the leaves."),
                "note_seasoned": (
                    "Neem oil is on UC IPM's organically acceptable list for artichoke aphid. "
                    "Avoid applying oils above roughly 90°F. Worth noting that the other aphid "
                    "species on artichoke, green peach, black bean and pea aphid, are mostly "
                    "cosmetic, and UC advises they do not normally warrant control unless "
                    "contamination of the buds is a concern."),
            },
        ],
    },
    {
        "id": "snails-and-slugs",
        "type": "mollusk",
        "name": "Snails and slugs (Cornu aspersum, Deroceras reticulatum)",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Clear boards, pots, dense ground cover and weedy edges from around the "
                    "plants, since that is where snails spend the day. Doing this before you try "
                    "anything else makes everything else work better."),
                "note_seasoned": (
                    "Habitat removal first. UC IPM describes mollusks as of major concern on "
                    "perennial artichokes especially in winter, and notes they do not pose a "
                    "threat to annual artichokes, so this problem largely belongs to the "
                    "mild-winter perennial regions. Switching from sprinklers to drip is part of "
                    "this rung rather than a separate one, since it cuts the overnight moisture "
                    "they move in."),
            },
            {
                "method": "slug_traps_barriers",
                "note_beginner": (
                    "Go out after dark with a torch and pick them off, which is more effective "
                    "than it sounds if you do it several nights running. Boards or an upturned "
                    "melon rind left out overnight give you a place to collect them from, and a "
                    "copper band around a raised bed or pot stops them crossing. Crushed eggshells "
                    "and coffee grounds have been tested and do not work."),
                "note_seasoned": (
                    "Handpicking at night, board and melon-rind traps and copper barriers are the "
                    "physical rungs UC IPM's Pest Notes carries. It states explicitly that crushed "
                    "eggshells and coffee grounds have not been shown to be effective deterrents, "
                    "which is worth knowing given how widely they are recommended elsewhere. "
                    "Decollate snail release is county-restricted in California."),
            },
            {
                "method": "iron_phosphate_slug_bait",
                "note_beginner": (
                    "Iron phosphate bait is the safest option to use around pets and wildlife. "
                    "Scatter it thinly around the plants rather than in piles, and refresh it "
                    "after rain."),
            },
        ],
    },
    {
        "id": "cutworms",
        "type": "insect",
        "name": "Cutworms",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Clear weeds and plant debris from the bed a couple of weeks before you plant "
                    "out. Cutworms are already in the soil living on that material, and removing "
                    "it early makes them leave or starve before your transplants arrive."),
            },
            {
                "method": "stem_collars",
                "note_beginner": (
                    "Push a collar of cardboard or a cut-off cup an inch into the soil around each "
                    "new transplant, standing an inch or two proud. Cutworms chew through stems at "
                    "ground level and a collar simply stops them reaching."),
                "note_seasoned": (
                    "The highest-value rung for this pest on artichoke, because the damage window "
                    "is narrow: cutworms take young transplants at the soil line and an "
                    "established plant is not at risk. Collar at set-out and remove them once the "
                    "stems lignify."),
            },
            {
                "method": "handpick",
                "note_beginner": (
                    "Go out after dark and check around the base of any plant that has been cut "
                    "off. The culprit is usually curled up in the top inch of soil within a few "
                    "inches of the damage."),
            },
            {
                "method": "bt",
                "note_beginner": (
                    "Bt affects only caterpillars and is safe around bees. Apply it in the evening "
                    "around the base of the plants, since cutworms feed at night."),
            },
            {
                "method": "spinosad",
                "note_beginner": (
                    "Spinosad is the last step here and is allowed in organic growing. Apply at "
                    "dusk, both because that is when cutworms feed and to spare bees."),
            },
        ],
    },
    {
        "id": "twospotted-spider-mite",
        "type": "mite",
        "name": "Twospotted spider mite (Tetranychus urticae)",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Clear weedy edges around the planting and pull out badly infested lower "
                    "leaves. Keeping the plants unstressed and well watered matters more than "
                    "usual here, because dusty, drought-stressed plants are where mites explode."),
                "note_seasoned": (
                    "THIS LADDER TERMINATES DELIBERATELY, and the reason is worth stating: UC IPM "
                    "records that miticides are not available for the control of spider mites on "
                    "artichokes. There is no chemical rung to escalate to, so cultural management "
                    "is not the gentle first option here, it is the whole of the response. Keep "
                    "plants watered, keep dust down, avoid the broad-spectrum insecticides that "
                    "flare mites by removing their predators, and tolerate low populations."),
            },
        ],
    },
]

# =============================================================================================
# Diseases
# =============================================================================================

DISEASES = [
    {
        "id": "verticillium-wilt",
        "type": "fungal",
        "name": "Verticillium wilt (Verticillium dahliae)",
        "control_ladder": [
            {
                "method": "crop_rotation",
                "note_beginner": (
                    "This one is about where you plant, not what you spray. Never put artichoke "
                    "where lettuce or strawberries have grown, or where an artichoke wilted "
                    "before. The same fungus attacks all three and it survives in the soil for "
                    "years. Broccoli and other cabbage-family crops are the right thing to plant "
                    "into ground that has the problem."),
                "note_seasoned": (
                    "UC IPM reports that V. dahliae isolates from artichoke, lettuce and "
                    "strawberry can each infect all three crops, and instructs growers not to "
                    "plant annual artichokes in ground with a history of the disease and to rotate "
                    "infected ground into broccoli. The microsclerotia survive many years in soil "
                    "with no host present, so a single season off does nothing. For a permanent "
                    "bed this collapses into a one-time siting decision you cannot revisit."),
            },
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Never take divisions off a plant that has wilted, and pull out and bin "
                    "affected plants rather than composting them. Keep the plants unstressed, "
                    "since stressed plants show the worst symptoms."),
                "note_seasoned": (
                    "UC IPM: do not take crowns for propagation from ground where the disease has "
                    "occurred, and practice proper cultural practices to avoid stressing plants, "
                    "since stressed plants develop the most severe symptoms. In severe cases "
                    "yields fall by as much as 50 percent. NOTE WHAT IS ABSENT FROM THIS LADDER: "
                    "there is no resistant-variety rung, because no extension source publishes a "
                    "cultivar-by-disease rating for artichoke, and the two closest statements "
                    "contradict each other."),
            },
        ],
    },
    {
        "id": "botrytis-gray-mold",
        "type": "fungal",
        "name": "Gray mold (Botrytis cinerea)",
        "control_ladder": [
            {
                "method": "airflow_spacing",
                "note_beginner": (
                    "Give the plants room and run the rows so the wind moves along them, so leaves "
                    "and buds dry quickly after rain or dew. Water at the base with a drip line "
                    "rather than over the top."),
                "note_seasoned": (
                    "University of Maine ranks gray mold first among the artichoke diseases it has "
                    "seen in trials, on both frequency and damage, so this rung earns real effort. "
                    "Spacing, row orientation for air movement and drip rather than overhead "
                    "irrigation are the levers."),
            },
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Take off dead and damaged leaves and any rotting buds as soon as you see "
                    "them, and get them out of the garden. The mold gets in through damage, so "
                    "protecting buds from frost, slugs and insect injury is part of preventing "
                    "it."),
                "note_seasoned": (
                    "Botrytis enters through wounds, which makes frost injury, snail grazing and "
                    "insect damage into gray mold entry points rather than separate problems. That "
                    "is the practical link between this ladder and the frost and mollusk ones."),
            },
            {
                "method": "prune_out_infection",
                "note_beginner": (
                    "Cut out infected parts back into clean tissue and dispose of them away from "
                    "the plant. When you harvest, cut the stem at a slight angle so water runs off "
                    "the cut instead of sitting on it."),
                "note_seasoned": (
                    "University of Maine adds a detail specific to this crop worth adopting: make "
                    "angled harvest cuts so water does not pool on the cut surface, which is "
                    "otherwise a ready infection court on a plant being cut repeatedly through a "
                    "wet season."),
            },
        ],
    },
    {
        "id": "powdery-mildew",
        "type": "fungal",
        "name": "Powdery mildew (Leveillula taurica, Erysiphe cichoracearum)",
        "control_ladder": [
            {
                "method": "airflow_spacing",
                "note_beginner": (
                    "Space plants generously and keep the middle of the plant open. Powdery mildew "
                    "is mostly a cosmetic nuisance on artichoke and usually does not need anything "
                    "more than this."),
            },
            {
                "method": "sulfur",
                "note_beginner": (
                    "Only worth spraying if the mildew gets bad enough to damage the plant. Sulfur "
                    "is the usual organic option, but do not use it above about 90°F or it burns "
                    "the leaves."),
                "note_seasoned": (
                    "UC's own framing sets the threshold: fungicides are not needed unless the "
                    "disease becomes severe. Sulfur is effective but phytotoxic in heat, which in "
                    "the regions where artichoke summers hardest is a real constraint rather than "
                    "a footnote."),
            },
        ],
    },
    {
        "id": "artichoke-curly-dwarf",
        "type": "viral",
        "name": "Artichoke curly dwarf virus",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "There is no cure, so this is entirely about not bringing it in and not "
                    "spreading it. Pull out and destroy any plant that is badly stunted with "
                    "distorted, dark-spotted leaves. Never take divisions from it."),
                "note_seasoned": (
                    "UC IPM: rogue diseased plants, and if propagating by crowns use only "
                    "disease-free stock. Infected plants yield up to 40 percent less and the buds "
                    "they do make are deformed. Under experimental conditions the virus can also "
                    "infect other Asteraceae including cardoon, sunflower and zinnia, so bear that "
                    "in mind when siting."),
            },
            {
                "method": "prune_out_infection",
                "note_beginner": (
                    "If you are starting a new planting and you have a choice, grow from seed "
                    "rather than from divisions off an old plant. The virus spreads by dividing "
                    "infected plants, and there is no evidence it travels in seed."),
                "note_seasoned": (
                    "This is the propagation decision made into a control, and it is the strongest "
                    "lever available: UC IPM states there is no evidence artichoke curly dwarf "
                    "virus is seedborne, so seed and the transplants raised from it may prevent "
                    "the problem occurring in new plantings. It is also why this guide's crop-wide "
                    "propagule is `transplant` rather than division despite division dominating "
                    "the perennial regions. Carry one unresolved conflict: UC IPM says no vector "
                    "has been identified, while UC ANR 7221 says the virus is insect-transmitted "
                    "with the specific vector unknown."),
            },
        ],
    },
    {
        "id": "bacterial-crown-rot",
        "type": "bacterial",
        "name": "Bacterial crown rot (Dickeya, formerly Erwinia chrysanthemi)",
        "control_ladder": [
            {
                "method": "garden_sanitation",
                "note_beginner": (
                    "Do not use crowns off an infected plant for propagation, and clear out rotted "
                    "material rather than leaving it in the bed. If you grow artichoke as a yearly "
                    "crop from seed or bought transplants, you may never see this at all."),
                "note_seasoned": (
                    "UC IPM: do not use infected crowns for propagation, and notes that annually "
                    "grown artichokes planted from seed or transplants may not develop the disease "
                    "at all. That makes this a mostly perennial-mode problem, and another entry on "
                    "the list of reasons a seed-raised transplant is the clean route into new "
                    "ground."),
            },
            {
                "method": "prune_out_infection",
                "note_beginner": (
                    "Take out affected plants completely, roots and all, rather than trying to cut "
                    "back to healthy tissue. Improve the drainage before you replant there, since "
                    "the rot establishes in wet ground."),
            },
        ],
    },
    {
        "id": "black-tip",
        "type": "physiological",
        "name": "Black tip (moisture-stress disorder)",
        "control_ladder": [
            {
                "method": "even_watering",
                "note_beginner": (
                    "Brown or blackened tips on the bud scales are not a disease and nothing is "
                    "eating your plant. It is the plant telling you it went short of water. The "
                    "bud is still perfectly good to eat, since only the outside is affected. Water "
                    "more evenly and it stops."),
                "note_seasoned": (
                    "Texas A&M attributes black tip to moisture stress and reports it as most "
                    "common when conditions are sunny, warm and windy, which is exactly when a "
                    "large canopy transpires hardest. The damage is cosmetic and the edible "
                    "portion of the bud is unaffected. Treat it as an instrument reading rather "
                    "than a problem: it tells you the irrigation is not keeping up with the bud "
                    "period, which is the one window Utah State says must not be water-stressed. "
                    "Worth distinguishing from frost blistering, which whitens and blisters the "
                    "outer bracts instead, and from the separate disorder UC calls black tip whose "
                    "cause it says is not known."),
            },
        ],
    },
]

# =============================================================================================
# Notifications, weather triggers, failure diagnostics
# =============================================================================================

NOTIFICATIONS = [
    {
        "title_seasoned": "Chill the artichoke seedlings now",
        "title_beginner": "Time to give your artichokes their cold spell",
        "body_seasoned": (
            "Your seedlings should be at four to six true leaves. Move them to 35°F to 50°F for "
            "about three weeks, with light if you can. Trials measured 3 to 33 percent flowering "
            "at 303 hours against 68 to 100 percent at 550, so duration is the variable that "
            "matters. Hold them under 80°F afterwards."),
        "body_beginner": (
            "If your artichoke seedlings have four to six real leaves, it is time for their cold "
            "treatment: about three weeks somewhere between 35°F and 50°F. This is the step that "
            "decides whether they make artichokes at all, so do not skip it."),
        "stage_id": "seedling_and_chill",
        "trigger_offset_days": 0,
        "audience": "core",
    },
    {
        "title_seasoned": "Keep artichokes under 80°F after chilling",
        "title_beginner": "Keep your chilled artichokes cool",
        "body_seasoned": (
            "Heat reverses accumulated chilling. Connecticut measured bare-soil temperatures of "
            "84°F to 102°F devernalizing plants and leaving them barren, and Rutgers found black "
            "plastic mulch cut yields in New Jersey trials for the same reason. Skip the "
            "warm-soil tricks that help other transplants."),
        "body_beginner": (
            "Now that your plants have had their cold treatment, keep them under 80°F until they "
            "go outside. Heat can undo the cold and leave you with plants that never make buds. "
            "Do not use black plastic mulch with artichoke."),
        "stage_id": "seedling_and_chill",
        "trigger_offset_days": 21,
        "audience": "core",
    },
    {
        "title_seasoned": "Do not let artichokes dry out from now on",
        "title_beginner": "Keep the water up now that buds are coming",
        "body_seasoned": (
            "Bud initiation onward is the window that cannot be missed. Utah State's instruction "
            "is not to water stress the plant once flower buds form. Moisture stress shows as "
            "black tip and as loose buds that open early at a smaller size than they should."),
        "body_beginner": (
            "Your plants are starting to make buds. From here until you pick them, do not let the "
            "soil dry out. A plant that goes dry now gives you tough buds with brown tips."),
        "stage_id": "budding",
        "trigger_offset_days": 0,
        "audience": "core",
    },
    {
        "title_seasoned": "Check artichokes daily in the heat",
        "title_beginner": "Check your artichokes every day now",
        "body_seasoned": (
            "Above 86°F buds open quickly and the heart loses tenderness and compactness. Cut on "
            "bract tightness rather than size, and move to daily checks; a bud that has begun to "
            "spread is past use however large it is."),
        "body_beginner": (
            "In hot weather artichokes open fast, and once the scales start to spread they turn "
            "woody and bitter. Check every day and cut them while they are still tight, even if "
            "they seem small."),
        "stage_id": "budding",
        "trigger_offset_days": 7,
        "audience": "core",
    },
]

WEATHER_TRIGGERS = [
    {
        "condition": "hard_freeze",
        "active_stages": ["establishment", "budding", "after_harvest"],
        "action": "FROST_PROTECT",
        "severity": "medium",
        "audience": "core",
        "title_seasoned": "Frost and your artichokes",
        "title_beginner": "Frost and your artichokes",
        "body_seasoned": (
            "Three different thresholds apply and confusing them leads to both panic and "
            "complacency. Bud tissue begins to freeze at about 29.9°F, which blisters and bronzes "
            "the outer bracts without affecting eating quality, and UC notes mature plants usually "
            "survive heavy frosts with reduced yield. Damage turns serious below about 24.8°F, and "
            "Texas A&M sets 25°F as the point to cover plants with 6 inches of straw, leaves or a "
            "frost blanket. The crown is the one that decides next year: below about 15°F expect "
            "severe crown loss even under mulch. A young transplant is the vulnerable case, not "
            "the established plant."),
        "body_beginner": (
            "A light frost is usually not a disaster. It can blister the outside of the buds, "
            "which looks bad but still tastes fine. Below about 25°F, cover the plants with a "
            "thick layer of straw, leaves, a bucket or a frost blanket. Below about 15°F the roots "
            "themselves die even under mulch, and that is the point where the plant will not come "
            "back next year. Young plants just set out are the ones to worry about most."),
    },
    {
        "condition": "heat_wave",
        "active_stages": ["seedling_and_chill", "budding"],
        "action": "PROTECT_QUALITY",
        "severity": "high",
        "audience": "core",
        "title_seasoned": "Heat and your artichokes",
        "title_beginner": "Hot weather and your artichokes",
        "body_seasoned": (
            "Heat does two separate things to this crop and both matter. On buds, above 86°F they "
            "open quickly and the heart loses tenderness and compactness, so switch to daily "
            "checks and cut on bract tightness. On chilled seedlings and recent transplants, heat "
            "REVERSES accumulated chilling: keep them under 80°F, since measured soil temperatures "
            "of 84°F to 102°F have devernalized plants outright. Irrigation is the lever for both, "
            "and Texas A&M is explicit that summer irrigation keeps temperatures down inside the "
            "crop canopy and that this is what prevents buds opening early. Water generously and "
            "shade young plants through the worst of it."),
        "body_beginner": (
            "Hot weather causes two different problems. Buds open fast above about 86°F and go "
            "woody, so check daily and pick them while they are tight. And if your plants have had "
            "their cold treatment recently, heat can cancel it out and leave them making leaves "
            "and no buds, so keep them under 80°F. Water generously through a heat wave even if "
            "the plants look fine, because watering actually cools the air inside the leaves. "
            "Shade young plants if you can."),
    },
]

FAILURE_DIAGNOSTICS = [
    {
        "label": "Plants grew well all season and never made a single bud",
        "audience": "core",
        "cause_beginner": "They did not get enough cold, or the cold they did get was undone by heat.",
        "cause_seasoned": "Insufficient or reversed vernalization.",
        "what_happened_beginner": (
            "This is the most common artichoke disappointment and it is not your watering or your "
            "soil. Artichoke only makes buds after a stretch of cool weather, and a big healthy "
            "leafy plant with no buds means it never got that signal. Either the cold treatment "
            "was too short, or it was warm enough afterwards to cancel it out. Next year, chill "
            "the seedlings for a full three weeks at 35°F to 50°F once they have four to six real "
            "leaves, keep them under 80°F afterwards, and choose a variety bred for first-year "
            "cropping such as Imperial Star or Emerald."),
        "what_happened_seasoned": (
            "The plants stayed vegetative, which means the vernalization requirement for flower-bud "
            "initiation was not met or was reversed. Three things to check in order. Duration: a "
            "replicated trial measured 3 to 33 percent flowering at 303 hours against 68 to 100 "
            "percent at 550, so a ten-day chill is likely the culprit. Devernalization: soil or air "
            "above roughly 80°F after chilling reverses it, with measured soil at 84°F to 102°F "
            "rendering plants barren, and black plastic mulch is a documented cause. Cultivar: "
            "Green Globe needs around 1300 hours for complete vernalization, and in Virginia "
            "barely one plant in seven bore during its first season, so it is the wrong choice "
            "for annual culture. Note also that 15 to 25 percent barren plants is normal even when "
            "everything was done correctly."),
        "next_season_tip_beginner": (
            "Give the seedlings a full three weeks between 35°F and 50°F, keep them under 80°F "
            "afterwards, and grow Imperial Star or Emerald."),
        "next_season_tip_seasoned": (
            "Chill to roughly 500 hours rather than the widely-copied ten days, supply light during "
            "chilling, hold under 80°F afterwards, avoid black plastic, and use a cultivar bred for "
            "annual production."),
    },
    {
        "label": "Buds opened before I could pick them, and were tough and bitter",
        "audience": "core",
        "cause_beginner": "Heat, or checking too infrequently.",
        "cause_seasoned": "Bud development outran the harvest interval, usually heat-driven.",
        "what_happened_beginner": (
            "Once an artichoke reaches full size it does not keep growing, it just opens, and an "
            "open bud is woody and bitter however you cook it. Heat speeds this up a lot: above "
            "about 86°F buds can go from perfect to past it in a day or two. Check every day in "
            "hot weather, cut on tightness rather than waiting for size, and water generously "
            "through a heat wave, because watering cools the air inside the canopy and slows the "
            "whole thing down."),
        "what_happened_seasoned": (
            "A mature bud neither enlarges further nor re-tightens, so any wait past maturity is "
            "pure loss. Above 86°F, UF/IFAS reports reduced tenderness and compactness of the "
            "heart and rapid opening, and Texas A&M attributes the same effect to hot dry "
            "conditions with irrigation as the countermeasure via canopy cooling. Shorten the "
            "harvest interval to daily above 86°F and cut on bract tightness. Dry air compounds "
            "it, and UC's earlier bulletin describes hot dry windy conditions producing woody, "
            "bitter, less compact buds with recurved bracts."),
        "next_season_tip_beginner": (
            "Check daily in hot weather and cut buds while they are tight, even if they look "
            "small. Keep the water up."),
        "next_season_tip_seasoned": (
            "Move to a daily harvest interval above 86°F, irrigate for canopy cooling, and where "
            "the region allows it shift the cropping window out of peak heat."),
    },
    {
        "label": "Brown or black tips on the bud scales",
        "audience": "core",
        "cause_beginner": "The plant went short of water.",
        "cause_seasoned": "Black tip, a moisture-stress disorder.",
        "what_happened_beginner": (
            "Nothing is eating your plant and it is not a disease. Brown or blackened scale tips "
            "mean the plant ran short of water at some point, most often in bright, warm, windy "
            "weather. The good news is that only the outside is affected and the artichoke is "
            "still perfectly good to eat. Water more evenly and it stops."),
        "what_happened_seasoned": (
            "Black tip, which Texas A&M attributes to moisture stress and reports as most common "
            "in sunny, warm and windy conditions, and describes as cosmetic damage that does not "
            "affect the edible portion of the bud. Treat it as an instrument reading on your "
            "irrigation during the bud period, which is the window Utah State says must not be "
            "water-stressed. Distinguish it from frost injury, which blisters and whitens the "
            "outer bracts instead, and note that UC separately describes a black tip disorder "
            "whose exact cause it says is not known."),
        "next_season_tip_beginner": (
            "Water more often rather than more heavily, and mulch, especially once buds appear."),
        "next_season_tip_seasoned": (
            "Move to drip on a frequent light schedule through the bud period; the shallow bulk of "
            "the root system does not forage between long intervals."),
    },
    {
        "label": "The plants died over winter",
        "audience": "core",
        "cause_beginner": "Winter got colder than the roots can take.",
        "cause_seasoned": "Crown kill, and in most regions it is expected rather than preventable.",
        "what_happened_beginner": (
            "Below about 15°F the roots die even under mulch, so in most of the country losing "
            "artichoke over winter is normal and not a mistake you made. Check your region's page: "
            "in most places this guide tells you to grow artichoke as a yearly crop and replant "
            "each spring for exactly this reason. If you want to try keeping one, a pot is far "
            "more reliable than mulch, since you can cut it back after the first hard frost and "
            "store it somewhere dark and just above freezing."),
        "what_happened_seasoned": (
            "Crown loss below roughly 15°F, corroborated independently at 14°F, and mulch does not "
            "bridge it. The measured field results are blunt: zero survivors in upstate New York "
            "under six inches of straw, 4.3 percent in a Utah and southeast Idaho trial whose "
            "authors concluded they could not recommend growing artichokes as perennials, one "
            "winter in twenty in Connecticut, and a best case of 30 to 40 percent at Blacksburg "
            "under hooped vented plastic plus a floating row cover, with few plants surviving "
            "under straw, a single cover or plastic alone. Container storage at 32°F to 35°F is "
            "the reliable alternative, and the payoff is real: a New Hampshire project recorded "
            "first harvest on 4 July from an overwintered plant against 8 August as an annual."),
        "next_season_tip_beginner": (
            "Plan on replanting each spring, or grow one in a pot you can store in an unheated "
            "garage over winter."),
        "next_season_tip_seasoned": (
            "Where the region cell says marginal, budget for annual replacement. Overwinter in "
            "containers rather than in the ground unless you can supply the hooped-plastic plus "
            "row-cover combination that produced the only respectable field survival figure."),
    },
    {
        "label": "Plants wilted and died one at a time through the season",
        "audience": "core",
        "cause_beginner": "Probably a soil disease, most likely Verticillium wilt.",
        "cause_seasoned": "Verticillium wilt or bacterial crown rot, distinguished by siting history.",
        "what_happened_beginner": (
            "Plants dying one by one, wilting and yellowing with browning leaf edges, usually means "
            "a fungus in the soil rather than anything you did. The key question is what grew "
            "there before: lettuce and strawberries carry the same one. There is no spray for it. "
            "Do not plant artichoke there again, do not take divisions off an affected plant, and "
            "plant broccoli or cabbage in that ground instead."),
        "what_happened_seasoned": (
            "Wilting, chlorosis, stunting and marginal leaf necrosis point at Verticillium "
            "dahliae, whose isolates from artichoke, lettuce and strawberry each infect all three, "
            "and whose microsclerotia persist many years without a host. Severe cases lose as much "
            "as 50 percent of yield. If the collapse was at the crown in wet ground, consider "
            "bacterial crown rot instead, which UC notes annually grown artichokes from seed or "
            "transplants may not develop at all. Both push the same conclusion: site on ground "
            "with no lettuce, strawberry or artichoke history, propagate from seed rather than "
            "from divisions of unknown status, and rotate affected ground into broccoli."),
        "next_season_tip_beginner": (
            "Plant somewhere that has not grown artichoke, lettuce or strawberries, and grow from "
            "seed rather than from divisions."),
        "next_season_tip_seasoned": (
            "Rotate the affected ground into brassicas, re-site the planting, and treat propagation "
            "material provenance as a disease control rather than a convenience."),
    },
]

# =============================================================================================
# Staged tips -- keys MUST be growth_stage ids or the renderer never grabs them
# =============================================================================================

def _tip(tid, stage_sources, text_s, text_b):
    return {
        "tip_id": tid, "sources": stage_sources, "evidence_tier": "extension_backed",
        "author": {"type": "plant_team"}, "added_in": "artichoke_cert_gs_arc",
        "last_reviewed": "2026-07-28", "audience": "core",
        "text_seasoned": text_s, "text_beginner": text_b,
    }


TIPS_BY_STAGE = {
    "seedling_and_chill": [
        _tip("tip_arti_chill1", ["umaine_highmoor", "umaine_2075", "umass_nevmg"],
             "Chill on hours, not on the calendar cliche. The widely-copied 'ten days at 45 to "
             "50°F' has weak support relative to its circulation; the direct replicated test "
             "measured 3 to 33 percent flowering at 303 hours and 68 to 100 percent at 550, and "
             "concluded that roughly three weeks at 35°F to 50°F should give reliable flowering. "
             "Supply light during chilling if you can, since the higher figure came from the year "
             "that had it.",
             "Give the seedlings about three weeks in the cold, not ten days. In trials, plants "
             "chilled for around three weeks flowered up to 100 percent of the time, while plants "
             "given half that flowered as little as 3 percent. A little light during those weeks "
             "helps too."),
        _tip("tip_arti_chill2", ["vce_438_108"],
             "Use deep cells, three to four inches, because artichoke throws a taproot early and "
             "circles it in a shallow tray. Virginia Cooperative Extension recommends "
             "greenhouse-grown transplants over direct field seeding specifically so vernalization "
             "can be controlled, and germination runs seven to ten days at 75°F to 85°F days with "
             "60°F to 65°F nights.",
             "Start seeds in deep pots rather than shallow trays, because artichoke sends a long "
             "root straight down within weeks and it will spiral in a small cell. Sow indoors "
             "rather than straight into the garden, so you can control the cold treatment."),
    ],
    "establishment": [
        _tip("tip_arti_estab1", ["vce_438_108", "usu_ext_artichoke"],
             "Where the region plants in spring, the set-out date is pinned to frost rather than "
             "chosen for convenience, and planting late is a common way to get no crop: Utah State "
             "notes that if planted too late the plants do not get the required chilling and will "
             "not flower. Virginia's system sets transplants at or a week or two before last frost "
             "so seedlings take 190 to 240 hours at or below 50°F in the ground.",
             "Plant out earlier than feels comfortable, around your last frost date, and cover the "
             "plants if a hard freeze threatens. Planting late is one of the main reasons "
             "artichokes never form buds, because the young plants miss the cool weather that "
             "triggers them."),
        _tip("tip_arti_estab2", ["usu_ext_artichoke", "umaine_2075"],
             "Mulch two to three inches at establishment. It is doing three jobs at once here: "
             "conserving the even moisture a shallow-bulk root system needs, suppressing the weeds "
             "that a slow-starting transplant loses to, and keeping the soil cool, which on this "
             "crop is a vernalization concern and not just a comfort one.",
             "Put 2 to 3 inches of compost or straw mulch around the plants once they are in. It "
             "holds moisture, keeps weeds down, and keeps the soil cool, which matters more for "
             "artichoke than for most things."),
    ],
    "budding": [
        _tip("tip_arti_bud1", ["uc_ipm", "usu_ext_artichoke"],
             "Harvest on bract tightness, never on diameter. On seeded varieties a mature bud "
             "neither enlarges further nor re-tightens, so waiting buys nothing; once the bracts "
             "spread the bud is woody and bitter. Take the terminal bud first and the secondaries "
             "as they size, cutting 2 to 3 inches of stem, and switch to daily checks above 86°F.",
             "Cut each artichoke while it is still tight and firm, with a couple of inches of "
             "stem. Do not wait for it to get bigger, because once it is full size it only opens "
             "from there. Take the big one at the top first."),
        _tip("tip_arti_bud2", ["tamu_eht065", "usu_ext_artichoke"],
             "Irrigation during the bud period is a quality intervention, not just a survival one: "
             "Texas A&M states that summer irrigation keeps temperatures down in the crop canopy "
             "and that this is what prevents buds opening early. Utah State's rule is not to water "
             "stress the plant once flower buds form. Moisture stress shows up as black tip.",
             "Keep the water up from the moment you see buds forming. Watering does not just keep "
             "the plant alive, it cools the air inside the leaves and stops the buds opening too "
             "early. Let it dry out now and you get brown-tipped, tough artichokes."),
    ],
    "after_harvest": [
        _tip("tip_arti_after1", ["uc_ipm", "uc_anr_7221"],
             "Where the planting persists, the cut-back is a scheduling tool rather than tidying. "
             "A cut-back made between the middle of April and the middle of June sets up cropping in "
             "fall, winter and spring; one made in late August or September sets up a summer "
             "harvest instead, and irrigation resumes about a month afterwards. Do not confuse this with stumping, the removal of spent bearing "
             "stalks at three-to-four-week intervals through the year.",
             "In mild-winter areas, cutting the plants down to the ground is how you choose when "
             "the next crop arrives rather than just tidying up. Cut back in late spring for a "
             "fall and winter crop, or in late summer for a summer one. Hold off watering for "
             "about a month after you cut them down."),
        _tip("tip_arti_after2", ["uc_ipm"],
             "Make the annual cut-back do double duty as your plume moth control. UC IPM "
             "quantifies it, reporting that cutting plants off 2 to 3 inches below soil level, "
             "shredding the tops and incorporating them reduces plume moth infestations in "
             "perennial fields by about 95 percent. Chop and bury residue under at least 6 inches "
             "of soil, and clear nearby thistles, which host it too.",
             "When you cut the plants back, do it properly and get rid of the tops, because that "
             "one job is also the best control there is for the caterpillar that bores into the "
             "buds. Chop the old growth and bury it, and pull out any thistles growing nearby."),
    ],
}
