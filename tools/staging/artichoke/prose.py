#!/usr/bin/env python3
"""Artichoke GS arc -- the crop-level consumer layer.

Companion to cells.py (the 39 region/zone cells) and sources.py (the catalog + anchors). This
file carries everything the whole_crop_gate register-fill pass wants and cells.py does not own:
the dual-register prose blocks, the display scalars, the two new duration fields, the cultivars,
and the 16 region_notes pairs.

THREE RULES THIS FILE OBEYS, all of them scars.

1. EVERY NUMBER TRACES TO A DOCUMENT SOMEONE OPENED. Each block's `sources` name only documents
   whose claim sentence was read in the fetched text during this arc, not documents that are
   merely about artichoke. That is R4, and it is the rule asparagus broke four times.

2. THE DUAL MODE IS CARRIED IN THE PROSE, NOT FLATTENED. Artichoke is a perennial in mild-winter
   regions and an annual almost everywhere else, and a crop-level string that picks one silently
   misinforms half the roster. Where a claim is mode-specific the sentence says which mode.

3. NO NUMBER IS INVENTED TO FILL A SHAPE. Where the corpus does not publish a figure -- a USDA
   zone, a Central Valley stand life, a per-cultivar disease-resistance grade -- the field says so
   rather than carrying a plausible one. See `open_findings`.
"""

V = "2026-07-28"


def anch(ids, urls):
    return {i: {"url": urls[i], "verified": V} for i in ids if i in urls}


# =============================================================================================
# Crop-level narrative registers
# =============================================================================================

DESCRIPTION_SEASONED = (
    "Globe artichoke is a big herbaceous perennial thistle grown for an immature flower bud, "
    "which is the single fact that explains everything else about it. Because the crop is a "
    "flower, the plant has to be persuaded to flower, and it does that after a run of cool "
    "weather: roughly 500 hours between 35°F and 50°F is the figure the peer-reviewed trial work "
    "converges on, though published requirements span 205 to 1356 hours and the spread is driven "
    "by cultivar rather than by measurement error. The requirement is quantitative, not "
    "absolute. Rutgers recorded 74 percent of Imperial Star and 57 percent of Green Globe "
    "Improved setting buds with no cold treatment at all, rising to 98 and 86 percent with it, "
    "so cold advances and synchronizes budding rather than permitting it. That is why artichoke "
    "runs two completely different careers. Where winters stay above roughly 15°F it is a "
    "permanent bed cropping for years from crown divisions, the Castroville model; everywhere "
    "colder it is an annual, started indoors, chilled deliberately as a seedling, set out, "
    "cropped in its first season and lost to winter. Both are real, both are extension "
    "documented, and which one applies to you is a question about your winter, not about your "
    "skill.")
DESCRIPTION_BEGINNER = (
    "An artichoke is a flower bud you pick before it opens, growing on a plant that looks like a "
    "five-foot silver thistle. That one fact drives everything: to get artichokes, the plant "
    "first has to be convinced to make flowers, and it does that after a stretch of cool weather. "
    "In mild-winter places like coastal California you plant once and pick from the same plants "
    "for years. Anywhere with a real winter you grow it as a yearly crop instead: start seed "
    "indoors, give the young plants a few weeks in the cold on purpose, plant them out, pick in "
    "late summer, and start over next spring. Neither way is harder than the other, they are just "
    "different, and your winter decides which one you are doing.")

HARVEST_READY_SEASONED = (
    "Cut on bract tightness, not on size. A bud is ready once it has reached full size for its "
    "position on the stalk and while its bracts are still closed flat against each other; the "
    "moment they loosen and begin to spread, the bud turns woody and bitter and is finished as "
    "food. University of California is explicit that on seeded varieties a mature bud stops "
    "enlarging, so waiting past that point buys nothing and costs the bud. Take the terminal bud "
    "first, since it matures well ahead of the two or three secondaries below it, and cut with 2 "
    "to 3 inches of stem attached. Heat compresses this window sharply: above 86°F buds open "
    "quickly and the heart loses tenderness and compactness, so in a hot spell check daily rather "
    "than every few days.")
HARVEST_READY_BEGINNER = (
    "Squeeze the bud. If it is firm and the scales are still shut tight against each other, cut "
    "it. If the scales have started to loosen and open out, you waited too long, and it will be "
    "woody and bitter no matter how you cook it. Size is not the signal, tightness is. Cut the "
    "big bud at the top of the stalk first, taking 2 to 3 inches of stem with it, and the smaller "
    "ones lower down will come along afterward. In hot weather check every day, because heat "
    "makes buds open fast.")

HARDINESS_NOTES_SEASONED = (
    "Four different temperatures matter here and they are commonly confused with one another. "
    "Bud tissue starts to freeze at about 29.9°F, which blisters and bronzes the outer bracts "
    "without harming eating quality, and the damage turns serious below about 24.8°F. Texas A&M "
    "sets 25°F as the practical management floor, the point at which you cover plants with straw "
    "or a frost blanket. The crown itself is far tougher and is the thing that decides whether a "
    "planting persists: Oregon State reports severe crown loss below 15°F even under mulch, and a "
    "peer-reviewed study independently puts the perennial limit at about 14°F. There is no "
    "published foliage-damage temperature for this crop, so beware anyone quoting one. Deliberately "
    "absent from this guide: a USDA hardiness zone. Three extension sources give three "
    "incompatible answers, from zone 7 and warmer to zone 6 with mulch to occasional zone 5, and "
    "all three are warmer-tolerant than the measured crown-kill temperature allows. Picking one "
    "would mean preferring a source over two others with no basis, so the temperatures do the "
    "work instead.")
HARDINESS_NOTES_BEGINNER = (
    "Think about it as two separate questions: will the buds get damaged, and will the plant "
    "survive the winter. Buds start taking frost damage around 30°F, which mostly just blisters "
    "the outside and still tastes fine, and gets serious in the mid 20s. Cover plants when a "
    "night below 25°F is coming. The roots are much hardier and only die around 15°F, even under "
    "mulch, which is the real dividing line between a plant that comes back next year and one "
    "that does not. You may see artichoke listed as hardy to zone 7, or zone 6, or zone 5. Those "
    "numbers disagree with each other and with the measured temperatures, so we do not publish "
    "one. Go by your actual winter lows.")

YEAR_ONE_NOTES_SEASONED = (
    "The first year is where this crop is won or lost, and the step people skip is the cold "
    "treatment. Sow 6 to 8 weeks ahead of the intended set-out date, germinate at 70°F to 80°F, "
    "then grow the seedlings at about 75°F day and 65°F night. Once they reach four to six true "
    "leaves, chill them for roughly three weeks at 35°F to 50°F. That duration is not folklore: a "
    "three-year replicated University of Maine trial measured 3 to 33 percent of plants flowering "
    "after 303 hours and 68 to 100 percent after 550 hours, and its conclusion is that duration "
    "is the key driver above 35°F. Supplemental light during chilling accompanied the higher "
    "figure, so give them light rather than a dark refrigerator if you can. Afterwards keep them "
    "under 80°F, because heat reverses accumulated chilling; Connecticut measured bare-soil "
    "temperatures of 84°F to 102°F devernalizing plants outright and leaving them barren. "
    "Virginia runs the inverse system, setting transplants out at or just before last frost so "
    "the seedlings take their 190 to 240 hours at 50°F or below in the ground. Either route "
    "works, but do not blend them, and expect 15 to 25 percent of plants to stay barren even when "
    "chilling was adequate.")
YEAR_ONE_NOTES_BEGINNER = (
    "There is one step in the first year that decides whether you get artichokes at all, and it "
    "is easy to skip because it sounds strange: you have to make the young plants cold on "
    "purpose. Start seed indoors 6 to 8 weeks before you plan to plant out. Once each seedling "
    "has four to six real leaves, put the tray somewhere between 35°F and 50°F for about three "
    "weeks. A spare refrigerator, an unheated garage, or a cold frame all work, and a bit of "
    "light during those weeks helps. In trials, plants given about three weeks of cold flowered "
    "at up to 100 percent, while plants given only half that flowered as little as 3 percent. "
    "Same seed, same year, and the only difference was the cold. After that, keep them under 80°F "
    "until they go outside, because heat undoes the cold treatment. Even done right, one plant in "
    "five may never make a bud, so plant a couple more than you think you need.")

SOIL_PREP_SEASONED = (
    "Site this crop the way you would site a small shrub, because that is the footprint. Plants "
    "reach four feet across and want deep, fertile, well-drained ground in full sun with a "
    "generous amount of organic matter worked in; University of California puts the target pH at "
    "6.0 to 6.5 and suggests lime or gypsum where calcium is low. Clear perennial weeds before "
    "planting rather than after, and UC's pre-plant trick is worth the fortnight it costs: "
    "irrigate the cleared bed deeply, let a flush of weed seed germinate, then work the ground "
    "again to kill the seedlings. Space plants 18 to 36 inches apart depending on whose spacing "
    "you follow, with 2 to 4 feet between rows; crowded plants make smaller buds and are "
    "miserable to harvest from. Where the bed is permanent, take the time to loosen it deeply, "
    "because you will not get another chance for years.")
SOIL_PREP_BEGINNER = (
    "Give artichoke more room than you think. A mature plant is about four feet wide, so allow at "
    "least a foot and a half between plants and two to three feet between rows. It wants full "
    "sun, deep soil that drains well, and plenty of compost dug in. Aim for a soil pH around 6.0 "
    "to 6.5. Get the perennial weeds out before you plant: water the bed, wait a couple of weeks "
    "for the weed seeds to sprout, then hoe them off and plant into clean ground. If the plants "
    "are going to stay put for years, it is worth digging the bed properly now.")

# =============================================================================================
# Structured blocks
# =============================================================================================

PH = {
    "preferred_range": [6.0, 6.5],
    # No source in this corpus publishes a TOLERATED band for artichoke. Left null rather than
    # widened by analogy; a made-up tolerance is exactly the kind of plausible filler this arc
    # exists to refuse.
    "tolerated_range": None,
    "note_seasoned": (
        "University of California puts the target at pH 6.0 to 6.5 and adds that lime or gypsum "
        "can be worked into soils low in calcium. That is the only pH figure the artichoke "
        "extension corpus publishes, so no tolerated band is given here rather than inferring "
        "one; if a soil test comes back well outside that range, correct toward it before "
        "establishing a bed you intend to keep."),
    "note_beginner": (
        "Aim for a slightly acidic soil, around pH 6.0 to 6.5. If a soil test comes back much "
        "lower than that, work in some lime before planting. Artichoke is not especially fussy, "
        "but since a plant may sit in the same spot for years it is worth getting right at the "
        "start."),
    "sources": ["uc_ipm"],
}

FERTILIZER = {
    "frequency": "twice per year",
    "type": "Nitrogen-forward fertilizer, or a balanced 10-10-10 on ground that was not enriched",
    "timing": "at planting, then again as the plants begin active growth ahead of budding",
    "example_product": "Calcium nitrate or ammonium sulfate for the nitrogen feeding; 10-10-10 "
                       "balanced garden fertilizer where no compost or manure was worked in",
    # RATIO-LESS BY EVIDENCE, not by omission: UC IPM's position is that on properly amended
    # ground "the only nutrient needed is nitrogen, if anything", and it prescribes a rate of
    # ACTUAL NITROGEN rather than a blend. npk_ratio null + npk_tag is exactly the branch the
    # NPK gate provides for crops whose feeding does not reduce to an N-P-K pill.
    "npk_ratio": None,
    "npk_tag": "Nitrogen-forward",
    "npk_hint_seasoned": (
        "Nitrogen is the nutrient that actually moves this crop. University of California's "
        "guidance is that where the ground has been properly amended with compost or manure, "
        "nitrogen is the only nutrient likely to be needed at all, applied at 0.5 to 1 pound of "
        "actual nitrogen per 100 feet of row; where it has not been amended, use a fertilizer "
        "carrying both nitrogen and phosphorus before planting."),
    "npk_hint_beginner": (
        "Nitrogen is the one that matters. If you dug in compost or manure, that plus a nitrogen "
        "feed is usually all the plant wants. If you did not, use a balanced fertilizer such as "
        "10-10-10 before planting instead."),
    "amount_seasoned": (
        "0.5 to 1 pound of actual nitrogen per 100 feet of row, which for a home bed of a few "
        "plants is a modest handful of a nitrogen source scratched in around each plant rather "
        "than broadcast. Container plants are the exception and need far more: University of "
        "Maine's container guidance is to feed weekly, because frequent watering flushes "
        "nutrients straight out of a soilless mix."),
    "amount_beginner": (
        "In the ground, a handful of fertilizer scratched into the soil around each plant is "
        "enough, twice a season. In a pot it is completely different: feed weekly, because every "
        "watering washes nutrients out the bottom."),
    "notes_seasoned": (
        "Feed at planting and again as growth picks up ahead of bud formation. Utah State's "
        "guidance pairs two instructions deliberately, a steady nitrogen feed alongside ground kept "
        "damp right through summer, and the pairing is the point, since a dry plant cannot use "
        "the nitrogen you gave it. One caution specific to this crop: Rutgers found black plastic "
        "mulch reduced early and total yields in New Jersey trials, likely by raising root "
        "temperatures enough to devernalize the plants, so warm-soil tricks that help other "
        "transplants can work against this one."),
    "notes_beginner": (
        "Feed once when you plant and again when the plant starts growing strongly in spring, "
        "using something nitrogen-rich. Keep the soil moist at the same time, because a thirsty "
        "plant cannot use fertilizer. Skip black plastic mulch with artichoke; it warms the roots "
        "and can undo the cold treatment the plant needs to make buds."),
    "notify_message_seasoned": (
        "Time to feed the artichokes. Nitrogen now, ahead of bud formation, and water it in."),
    "notify_message_beginner": (
        "Feed your artichokes now with a nitrogen-rich fertilizer, and water afterward."),
    "sources": ["uc_ipm", "usu_ext_artichoke", "umaine_2075", "rutgers_fs044"],
}

WATERING = {
    "watering_method": "drip",
    "drought_tolerance": "low",
    # stage_ids MUST match ipm.GROWTH_STAGES or the app has no stage to hang these on.
    "schedule_by_stage": [
        {
            "stage_id": "seedling_and_chill", "system": "hand_water",
            "rate": "keep the mix just moist, never wet",
            "frequency": "check_daily_indoors", "level": "important",
            "note_seasoned": (
                "Indoors the risk inverts: damping-off kills more artichoke seedlings than drought "
                "does. Keep the mix just moist and let the surface dry slightly between waterings. "
                "During the chilling weeks the plants transpire very little, so cut back sharply "
                "rather than watering on the same schedule you used at 75°F."),
            "note_beginner": (
                "Keep the seed mix damp but not soggy, and let the top dry a little between "
                "waterings. While the seedlings are in the cold they barely drink at all, so water "
                "much less than you did on the windowsill or they will rot."),
        },
        {
            "stage_id": "establishment", "system": "soaker_or_drip",
            "rate": "1 to 2 inches per week, split across several applications",
            "frequency": "even_while_establishing", "level": "critical",
            "note_seasoned": (
                "The fortnight after set-out is one of the two windows that cannot be missed. "
                "Water frequently rather than heavily, since the feeding roots sit shallow, and "
                "mulch 2 to 3 inches to hold it even and keep the soil cool."),
            "note_beginner": (
                "Water often for the first few weeks after planting out, aiming for an inch or two "
                "a week spread over two or three waterings. Mulch around the plants to hold the "
                "moisture in."),
        },
        {
            "stage_id": "budding", "system": "soaker_or_drip",
            "rate": "1 to 2 inches per week, more in heat; never let it dry",
            "frequency": "steady_through_harvest", "level": "critical",
            "note_seasoned": (
                "The other window that cannot be missed, and the one with a visible penalty: Utah "
                "State's rule is not to water stress the plant once flower buds form, and the "
                "failure shows as black tip and as loose buds that open early and small. In heat, "
                "irrigation is also cooling the canopy, which is what slows bud opening."),
            "note_beginner": (
                "From the moment buds appear until you pick them, do not let the soil dry out. A "
                "plant that goes thirsty now gives you tough buds with brown tips. In hot weather "
                "water generously even if the plant looks fine, because it cools the plant down "
                "and stops the buds opening too fast."),
        },
        {
            "stage_id": "after_harvest", "system": "soaker_or_drip",
            "rate": "taper off, then resume about a month after a cut-back",
            "frequency": "reduced", "level": "optional",
            "note_seasoned": (
                "Mode-dependent. Where the planting is pulled, stop. Where it persists, University "
                "of California's cycle holds water off after the cut-back and resumes irrigation "
                "about a month later to start the new flush; in the Central Valley, by contrast, "
                "summer water is what carries the stand and must not be withdrawn."),
            "note_beginner": (
                "If you are pulling the plants up, stop watering. If you are keeping them, cut "
                "them down and then hold off watering for about a month before starting again, "
                "which is what triggers the next round of growth. The exception is a hot inland "
                "valley, where the plants need water all summer to survive at all."),
        },
    ],
    "frequency_seasoned": (
        "Water on a schedule rather than on the plant's appearance, because by the time an "
        "artichoke looks thirsty a bud has usually already been damaged. One to two inches per "
        "week, split across several applications, is what both Utah State and University of Maine "
        "publish. The root architecture explains why frequency beats volume: the plant makes a "
        "taproot straight down, yet University of Maine reports most of its feeding roots sitting "
        "near the surface, so it cannot forage far between waterings."),
    "frequency_beginner": (
        "Give artichoke 1 to 2 inches of water a week, split over two or three waterings rather "
        "than one big soak. It has a deep central root but most of its feeding roots are shallow, "
        "so it dries out faster than its size suggests. Do not wait for it to look thirsty."),
    "amount_seasoned": (
        "One to two inches per week through the growing season, more in a hot dry spell and more "
        "again in a container, where daily watering may be needed. Two to three inches of organic "
        "mulch is close to mandatory rather than optional here: Utah State recommends it "
        "explicitly to conserve moisture, suppress weeds and keep the soil cool, and all three of "
        "those jobs are load-bearing for this crop."),
    "amount_beginner": (
        "About an inch or two a week, and more when it is hot. Mulch the plants with 2 to 3 "
        "inches of compost or straw, which keeps the soil damp and cool and saves you a lot of "
        "watering. Plants in pots may need water every single day in summer."),
    "method_seasoned": (
        "Drip or soaker line, laid under the mulch. Utah State recommends drip where possible, "
        "and it pays twice here: it delivers the frequent light applications the shallow root mass "
        "wants, and it keeps water off the foliage and buds, which is the main cultural control "
        "for gray mold and for snails."),
    "method_beginner": (
        "Use a drip line or soaker hose under the mulch rather than a sprinkler. Wet leaves and "
        "wet buds invite gray mold and attract snails, and drip keeps them dry while still "
        "watering often, which is what this plant wants."),
    "method_note_seasoned": (
        "Summer irrigation is doing a second job beyond hydration in hot regions. Texas A&M states "
        "it directly: in summer, irrigation helps keep temperatures down inside the crop canopy "
        "and that is what prevents buds opening early. So in a heat wave, watering is a quality "
        "intervention and not just a survival one."),
    "method_note_beginner": (
        "In hot weather, watering does double duty. It keeps the plant alive, and it also cools "
        "the air inside the leafy canopy, which stops the buds popping open before you can pick "
        "them. So water generously through a heat wave even if the plant looks fine."),
    "critical_periods_seasoned": (
        "From bud initiation onward is the period that cannot be missed. Utah State's instruction "
        "is blunt, that once the flower buds form you do not water stress the plant. The failure "
        "this prevents is black tip, a browning of the bract tips that Texas A&M attributes to "
        "moisture stress and reports as most common in sunny, warm, windy conditions. The other "
        "critical window is the fortnight after transplanting, where consistent water drives the "
        "root establishment the rest of the season rests on."),
    "critical_periods_beginner": (
        "Two moments matter most. The first is right after planting out, when steady water gets "
        "the roots going. The second is from the time you see buds forming until you pick them: "
        "let the plant go dry then and the bud tips turn brown and the buds toughen up. Once buds "
        "appear, do not let it dry out."),
    "signs_overwater_seasoned": (
        "Standing water and saturated ground are a real risk for this crop rather than a "
        "theoretical one, since bacterial crown rot and damping-off both establish in wet soil "
        "and the crown is the part you cannot replace. Yellowing lower leaves on a bed that has "
        "not dried out between waterings, or a plant that wilts despite wet soil, point at the "
        "crown rather than at thirst."),
    "signs_overwater_beginner": (
        "If the soil never dries out between waterings and the lower leaves are yellowing, or the "
        "plant wilts even though the ground is wet, you are watering too much. Artichoke wants "
        "frequently moist soil, not soggy soil, and a waterlogged crown rots."),
    "signs_underwater_seasoned": (
        "Grey-green leaves that lose their gloss and wilt through the middle of the day are the "
        "early sign. On buds it shows as black tip, the browning of the bract tips, and as buds "
        "that feel loose and open early at a smaller size than they should. Because bud quality "
        "responds to water within days, treat any midday wilt during the bud period as urgent."),
    "signs_underwater_beginner": (
        "Wilting in the middle of the day and dull, drooping leaves mean it needs water. On the "
        "buds, look for brown tips on the scales and buds that open early while they are still "
        "small. Both mean the plant went dry at the wrong moment."),
    "sources": ["usu_ext_artichoke", "umaine_2075", "tamu_eht065", "uc_ipm"],
}

STORAGE = {
    "room_temp_seasoned": (
        "Do not hold cut buds at room temperature. Artichoke is a growing organ picked in mid "
        "development and it respires fast, so it dries and toughens on a counter within a day. "
        "Cool it promptly after cutting."),
    "room_temp_beginner": (
        "Do not leave cut artichokes sitting out. They dry out and go tough within a day. Get "
        "them into the fridge soon after picking."),
    "fridge_seasoned": (
        "Refrigerate cold and damp. The UC Davis Postharvest Technology Center's optimum is 32°F "
        "at above 95 percent relative humidity, so in a domestic fridge that means the coldest "
        "shelf with the stem end wrapped in a damp cloth or the whole bud in a loosely closed "
        "bag. Utah State gives 3 to 5 days for home storage; commercial storage potential is "
        "under 21 days even at optimum, because visual and sensory quality fall away quickly. "
        "Artichoke has low sensitivity to ethylene, so it is not fussy about what it is stored "
        "next to."),
    "fridge_beginner": (
        "Keep artichokes cold and damp, on the coldest shelf of the fridge in a loosely closed "
        "bag, ideally with the cut stem wrapped in a damp cloth. Expect 3 to 5 days of good "
        "quality. They do not mind being stored next to other fruit and vegetables."),
    "freezer_seasoned": (
        "Do not freeze buds whole and raw; blanch first or trim to hearts. University of "
        "California notes artichokes and artichoke hearts can be frozen, canned or dried, and the "
        "heart is what most people actually preserve, usually blanched in acidulated water and "
        "then frozen or marinated."),
    "freezer_beginner": (
        "You can freeze artichokes, but trim them down to the hearts and blanch them in water "
        "with a squeeze of lemon first. Frozen raw and whole, they turn to mush. Hearts also can "
        "well and take marinades nicely."),
    "notes_seasoned": (
        "Cut with 2 to 3 inches of stem attached and keep the stem on until you cook: the stem is "
        "an extension of the heart, edible once peeled, and it also slows moisture loss from the "
        "cut. Commercially the stem is cut 1 to 1.5 inches below the base for the same reason."),
    "notes_beginner": (
        "Leave 2 to 3 inches of stem on when you cut, and leave it attached until you cook. The "
        "stem keeps the bud from drying out, and once you peel the tough outside it tastes just "
        "like the heart, so do not throw it away."),
    "sources": ["ucd_postharvest", "usu_ext_artichoke", "uc_ipm"],
}

SOIL = {
    "preferred_texture_core": ["loam", "sandy_loam"],
    "preferred_texture_seasoned": ["deep fertile loam", "sandy loam"],
    "tolerated_texture_core": ["clay_loam", "sandy"],
    "tolerated_texture_seasoned": ["amended clay loam", "amended sandy soil"],
    "problematic_texture_core": ["waterlogged", "heavy_clay"],
    "problematic_texture_seasoned": ["ground that stays saturated", "unamended heavy clay"],
    "drainage_requirement": "well_draining",
    "organic_matter_preference": "high",
    "preferred_description_seasoned": (
        "Deep, fertile, well-drained ground carrying plenty of organic matter is what University "
        "of California asks for, and depth matters more than texture: this is a plant that throws "
        "a taproot and then feeds from a shallow mass above it, so it wants a bed that is loose "
        "well down and moist near the top. Clay and sandy soils both work once amended with "
        "compost, manure or leaf mold. What it will not tolerate is ground that stays saturated, "
        "because the crown rots and the crown is the part that carries a perennial planting from "
        "one year into the next."),
    "preferred_description_beginner": (
        "Artichoke wants deep, rich soil that drains well, in full sun, with lots of compost "
        "worked in. Heavy clay or light sand are both fine once you have improved them. The one "
        "thing to avoid is a low spot where water sits after rain, because a waterlogged plant "
        "rots at the base and does not come back."),
    "sources": ["uc_ipm", "usu_ext_artichoke", "umaine_2075"],
}

ROTATION = {
    "family": "Sunflower and daisy family (Asteraceae)",
    "rotation_years": None,
    "good_after": ["broccoli", "cabbage", "cauliflower"],
    "avoid_after_seasoned": (
        "Do not plant artichoke after lettuce or strawberry, and this is a specific finding rather "
        "than general rotation hygiene. UC IPM reports that Verticillium dahliae isolates from "
        "artichoke, lettuce and strawberry can each infect all three crops, and its instruction "
        "is not to plant annual artichokes in ground with a history of the disease and to rotate "
        "infected ground into broccoli. The fungus produces microsclerotia that survive many "
        "years in soil without any host present, so this is a siting decision with a long memory, "
        "not something a single season off fixes. If you are propagating from crowns, never take "
        "divisions from a planting where wilt has appeared."),
    "avoid_after_beginner": (
        "Do not plant artichoke where lettuce or strawberries have grown, and do not plant it "
        "where an artichoke wilted and died before. The same soil fungus attacks all three, and "
        "it survives in the ground for years, so a season's gap does not clear it. Broccoli and "
        "the other cabbage-family crops are a good thing to follow, and a good thing to plant "
        "into ground where the problem has shown up."),
    "note_seasoned": (
        "Rotation means different things for the two modes. Grown as an annual, treat artichoke "
        "as a normal rotation crop and keep it off lettuce, strawberry and old artichoke ground. "
        "Grown as a permanent bed there is no rotation at all, so the same rule becomes a one-time "
        "siting decision that you cannot revisit for five to ten years, which makes it worth more "
        "care rather than less."),
    "note_beginner": (
        "If you are growing artichoke as a yearly crop, move it around the garden like anything "
        "else and keep it off ground that grew lettuce or strawberries. If you are planting a "
        "permanent bed, you only get one chance to choose the spot, so choose it carefully: it "
        "will be there for years."),
    "sources": ["uc_ipm"],
}

START_METHOD = {
    "start": "transplant",
    "hardening_off_seasoned": (
        "Harden for seven to ten days in a cold frame or other protected spot before setting out, "
        "which is Virginia Cooperative Extension's instruction. There is a neat efficiency "
        "available here that is worth knowing: University of Maine notes the hardening-off period "
        "can be combined with vernalization, since a cold frame in early spring sits in the same "
        "35°F to 50°F band the chilling wants, provided the seedlings are not allowed to overheat "
        "on a sunny day. Watch that vent, because the same frame can run past 80°F by noon and "
        "start undoing the chilling it is supposed to be delivering."),
    "hardening_off_beginner": (
        "Move the seedlings outside gradually over seven to ten days before planting, using a "
        "cold frame or a sheltered spot. If you are doing this in early spring you can often "
        "combine it with the cold treatment the plants need, since a cold frame is about the "
        "right temperature. Just prop it open on sunny days, because if it gets above 80°F inside "
        "it starts to cancel out the cold."),
    "notes_seasoned": (
        "Raise your own transplants; Virginia Cooperative Extension recommends greenhouse-grown "
        "transplants over direct field seeding specifically so vernalization can be controlled. "
        "Sow six to eight weeks ahead of the intended set-out, germinating at 70°F to 80°F, "
        "and use deep cells of three to four inches because the taproot circles in a shallow one. "
        "Three other propagation routes are real and dominant in perennial regions, and each "
        "carries a caveat: crown divisions and rooted offshoots come true to type where seed does "
        "not, and are what California's permanent plantings are built from, but UC IPM warns that "
        "artichoke curly dwarf virus spreads by dividing infected plants and that there is no "
        "evidence it is seedborne, so seed-raised transplants are the clean route into new "
        "ground. Where a region's guidance names crown pieces rather than transplants, the cell "
        "for that region says so."),
    "notes_beginner": (
        "Grow your own transplants from seed rather than sowing straight into the garden, because "
        "the young plants need a controlled spell of cold and you cannot give them that outdoors "
        "in most places. Sow six to eight weeks before planting out, keep them warm to germinate, "
        "and use deep pots, since artichoke sends down a long root early. In mild-winter areas "
        "you can also plant divisions taken off an established clump, which produce plants "
        "identical to the parent. Just take them from a healthy plant, since dividing a sick one "
        "spreads a virus that seed-grown plants avoid."),
}

YIELD_EXPECTATIONS = {
    "per_plant_seasoned": (
        "Structure sets the count: each flower stalk carries one terminal bud plus two to three "
        "smaller secondaries, and a plant throws several stalks. Utah State frames it that way "
        "and reports three to five buds per stalk. Texas A&M expects six to nine buds from a "
        "healthy plant. University of Maine and the New England guide both report 10 to 20 buds "
        "per plant under annual culture, of which only two or three are primaries. Read those "
        "numbers with the size caveat attached, below."),
    "per_plant_beginner": (
        "Each flower stalk gives you one big artichoke at the top and two or three smaller ones "
        "below it, and a healthy plant sends up several stalks. Depending on where you are, "
        "expect somewhere between six and twenty buds from a mature plant over the season, but "
        "only two or three of them will be the large ones you picture."),
    "peak_production_seasoned": (
        "Where artichoke perennializes, peak production is a spring event: University of "
        "California puts the peak for perennial plantings in March and April, with the highest "
        "volume between March and May, and cutting plants back after that peak brings a lighter "
        "second crop later in the year. Under annual culture there is one concentrated flush "
        "instead, most of it inside a six to eight week window, followed by a sporadic light "
        "picking of secondary buds until frost. Connecticut measured that concentration precisely, "
        "with 86 percent of buds harvested in a 5.9 week span."),
    "peak_production_beginner": (
        "If your plants live for years, the big harvest comes in spring, roughly March through "
        "May, and cutting the plants back afterward can bring a smaller second crop. If you are "
        "growing it as a yearly crop, you get one main flush instead, with most of the harvest "
        "packed into about six to eight weeks and then a trickle of small side buds until frost "
        "ends it."),
    "first_year_note_seasoned": (
        "Two first-year realities worth setting expectations against. Some plants will simply not "
        "bud: Virginia Cooperative Extension reports 15 to 25 percent barren in the planting year "
        "even where chilling was adequate, and the figure is far worse with a cultivar not bred "
        "for annual production, with barely one Green Globe plant in seven bearing anything at all "
        "in Virginia. And the buds run small. University of Maine's trials found most under 3 inches "
        "across, against the 3 to 4 inch buds sold in shops, and its researchers advise growers "
        "to be sure their market wants small artichokes before scaling up. A first-year crop is a "
        "real crop; it is just not a supermarket one."),
    "first_year_note_beginner": (
        "Expect two surprises in year one. First, some plants never produce anything, often one in "
        "five even when you did everything right, so plant a few spare. Second, your artichokes "
        "will mostly be smaller than shop ones, usually under 3 inches across. They taste better "
        "than they look, and the plants get more productive in later years if yours survive the "
        "winter."),
    "factors_seasoned": [
        "cultivar bred for annual production versus a perennial type",
        "hours of chilling actually delivered, and whether summer heat reversed any of it",
        "bed age, where the planting persists",
        "steady moisture from bud initiation onward",
    ],
    "sources": ["usu_ext_artichoke", "tamu_eht065", "umaine_2075", "umass_nevmg", "vce_438_108",
                "uc_anr_7221"],
}

CONTAINER_NOTES = {
    "container_ok": True,
    "container_recommended": False,
    "min_pot_gallons": 5,
    "recommended_pot_gallons": 10,
    "depth_inches_min": 14,
    "shape_requirements": "Wide and deep; a plant reaching four feet across needs a stable base",
    "drainage": {"drainage_holes_required": True, "gravel_layer": False,
                 "saucer_practice": "empty_after_watering"},
    "soil_mix": {
        "type_seasoned": (
            "A lightweight soilless growing medium, which is what University of Maine specifies "
            "for artichoke containers; garden soil compacts in a pot and this plant is in it for "
            "a long season."),
        "type_beginner": (
            "Use a bagged potting mix, not soil from the garden. Garden soil packs down hard in a "
            "pot and the roots suffer."),
        "amendments_seasoned": (
            "Blend in compost for water-holding capacity and a slow-release fertilizer at "
            "planting, then plan to feed liquid weekly regardless, because frequent watering "
            "leaches a soilless mix quickly."),
        "amendments_beginner": (
            "Mix in some compost to help the pot hold water, and add a slow-release fertilizer. "
            "You will still need to feed weekly through the season."),
    },
    "watering_adjustment_beginner": (
        "Pots dry out far faster than ground. In summer expect to water a container artichoke "
        "every day, and check it by hand rather than by schedule during a heat wave."),
    "watering_adjustment_seasoned": (
        "Daily watering in summer is normal rather than exceptional, per University of Maine's "
        "container guidance. The bud period is unforgiving of a missed day, so a container plant "
        "is a poor candidate if you travel."),
    "fertilizer_adjustment_beginner": (
        "Feed a container plant every week during the growing season. Watering that often washes "
        "the nutrients straight out of the pot."),
    "fertilizer_adjustment_seasoned": (
        "Weekly liquid feeding, which is University of Maine's explicit container recommendation "
        "and a large step up from the twice-a-season feeding an in-ground plant wants."),
    "overwintering": {
        "applicable": True,
        "approach_seasoned": (
            "This is the strongest argument for growing artichoke in a pot in a cold region, and "
            "it is a documented method rather than an improvisation. University of Maine's "
            "protocol: once the first hard frost has hit, strip off every bit of top growth, then move "
            "the container somewhere dark and held between 32°F and 35°F, bringing it back out "
            "roughly a fortnight before your expected last frost. An unheated garage or a root cellar suits. "
            "The payoff is real, since an overwintered plant starts its second season already "
            "established and crops far earlier than a spring transplant."),
        "approach_beginner": (
            "A pot is the easiest way to keep an artichoke alive through a cold winter. After the "
            "first hard frost, cut all the leaves off, then move the pot somewhere dark and just "
            "above freezing, like an unheated garage, and leave it. Bring it back out about two "
            "weeks before your last frost date. A plant that comes through winter crops much "
            "earlier the next year than a new one."),
    },
    "self_watering_notes_seasoned": (
        "A self-watering container suits artichoke better than most crops, because the plant wants "
        "frequent light moisture rather than a deep soak and cycle, and the bud period tolerates "
        "no missed days. Two cautions specific to this crop. Keep the reservoir topped rather than "
        "letting it run empty and refill, since the swing is what produces black tip. And do not "
        "let the wicking mix stay saturated at the crown, because bacterial crown rot and "
        "damping-off both establish in wet ground and the crown is the part you cannot replace."),
    "self_watering_notes_beginner": (
        "Self-watering pots work well for artichoke, since it likes steady moisture and hates "
        "drying out, especially once buds appear. Keep the reservoir topped up rather than "
        "letting it empty and refilling, and make sure the top of the soil is damp rather than "
        "soaking, because a constantly wet crown rots."),
    "container_specific_pests": ["snails and slugs", "aphids"],
    "container_suitable_varieties": ["Imperial Star", "Colorado Star"],
    "notes_seasoned": (
        "Containers work for artichoke but are a considered choice rather than a default. "
        "University of Maine puts the floor at five-gallon pails or similar with a lightweight "
        "soilless mix, and adds a siting detail specific to this crop: place them in bright sun "
        "but with only moderate direct midday sun, since a pot in full afternoon sun can warm the "
        "root zone far enough to devernalize the plant and leave it barren. That is the same "
        "mechanism that makes black plastic mulch counterproductive in the ground. The cost of a "
        "container is daily watering and weekly feeding; the benefit is that you can move the "
        "plant, which is what makes both overwintering in a cold region and chilling in a warm "
        "one possible at all."),
    "notes_beginner": (
        "Artichoke does grow in a big pot, five gallons at the very least and bigger is better. "
        "Put it somewhere bright but out of the harshest afternoon sun, because a hot pot can "
        "warm the roots enough that the plant never makes buds. Be realistic about the work: "
        "daily watering in summer and feeding every week. The reward is that you can move it, "
        "which lets you overwinter it somewhere cold in a cold climate, or give it a cool spell "
        "in a warm one."),
    "sources": ["umaine_2075", "rutgers_fs044"],
}

MOON_PHASE = {
    "phase": "none",
    "evidence_tier": "none",
    "source_note_seasoned": (
        "No extension or peer-reviewed source supports timing artichoke planting or harvest by "
        "moon phase. What this crop actually responds to is measurable and worth attending to "
        "instead: hours accumulated between 35°F and 50°F before bud initiation, soil and air "
        "temperature staying under 80°F afterward so that chilling is not reversed, and bract "
        "tightness at harvest."),
}

COMPANIONS = {
    "note_seasoned": (
        "No extension source publishes companion planting guidance for artichoke, and this guide "
        "does not invent any. Two neighbor questions do have sourced answers and they matter more "
        "than any companion list would. What must not precede it: lettuce and strawberry, which "
        "share the Verticillium strain that infects artichoke. What suits it as a following or "
        "preceding crop: broccoli and the other brassicas, which UC IPM names as the rotation for "
        "infected ground. Beyond that, the practical constraint on neighbors is physical rather "
        "than chemical, since a mature plant is around four feet across and casts real shade, so "
        "site it at the north end of a bed in the northern hemisphere and give short crops "
        "somewhere else to live."),
    "note_beginner": (
        "There is no reliable companion planting advice for artichoke, so we do not offer any. "
        "Two things are worth knowing about its neighbors though. Do not plant it where lettuce "
        "or strawberries grew, because they share a soil disease. And remember it gets about four "
        "feet wide and tall enough to shade whatever is behind it, so put it at the back or the "
        "north side of a bed."),
    "sources": ["uc_ipm"],
}

# =============================================================================================
# The two duration fields (register rows 26 and 27), authored natively at cert
# =============================================================================================

HARVEST_STOP_RULE = {
    "signal": "bract_opening",
    # NO threshold_inches, deliberately. The signal is a state change rather than a measurement,
    # and none of the three T1 sources that state the rule attaches a size to it. The gate's
    # requirement is keyed to the signal for exactly this reason (harvest_duration_gate,
    # DIMENSIONAL_SIGNALS); carrying inches here would assert a precision nobody published.
    "note_seasoned": (
        "Artichoke's stop rule governs the individual bud, not the season, and that is a real "
        "difference from the other crop on this archetype rather than a wording choice. Cut each "
        "bud while its bracts are still closed flat against one another. Once they loosen and "
        "begin to spread, the bud has passed: University of California notes that on seeded "
        "varieties a mature bud neither enlarges further nor re-tightens, and that buds left past "
        "their prime turn woody and bitter. Size is not the trigger, since a small secondary bud "
        "is perfectly good eating and a large one that has begun to open is not. Heat compresses "
        "the window, because above 86°F buds open quickly and the heart loses tenderness and "
        "compactness, so switch to daily checks in hot weather. There is no reserve-protection "
        "stop for this crop of the kind asparagus has; harvesting does not draw down a storage "
        "organ, so you pick until frost or until the flush ends rather than stopping to spare the "
        "plant."),
    "note_beginner": (
        "Pick each artichoke while it is still tight. Run a thumb over it: if the scales are shut "
        "flat against each other, cut it now. If they have started to loosen and spread apart, "
        "that one is past its best and will be tough and bitter however you cook it. Do not wait "
        "for a bud to get bigger, because once it is fully grown it stops growing and only opens. "
        "In hot weather check every day, since heat makes them open fast. Unlike some crops there "
        "is no point where you have to stop picking to protect the plant, so keep going until "
        "frost or until the plant runs out of buds."),
    "sources": ["uc_ipm", "usu_ext_artichoke", "umaine_2075", "uf_ifas_hs1289"],
}

# harvest_ramp_weeks: NULL. THE HONEST-N/A BRANCH IS THE WHOLE ANSWER HERE, FOR TWO REASONS.
#
# A first draft of this file authored a three-year ramp -- year 1 [0,4], year 2 [6,10], year 3
# [8,14] -- and every one of those numbers was INVENTED to fill the field's shape. That is the
# defect class this entire arc exists to refuse, committed while writing the file that documents
# refusing it, so it is recorded here rather than quietly deleted.
#
# REASON 1: NO SOURCE PUBLISHES A BED-AGE WEEK RAMP FOR ARTICHOKE. The corpus was re-checked
# specifically for it. UC ANR 7221 gives a peak (March to April) and a year-round coastal harvest
# but no duration by bed age; UC Master Gardener gives "Production starts about a year after
# planting, although some buds usually develop the first spring after early fall plantings", which
# is an onset and not a length; OSU's news article gives a stand life of three to four years and no
# weeks. Nothing anywhere converts bed age into a picking duration for this crop. Asparagus has a
# ramp because five extension services publish one; artichoke has none because nobody does.
#
# REASON 2: EVEN IF ONE EXISTED IT WOULD DESCRIBE 6 CELLS OUT OF 39. A ramp is a perennial-crown
# concept -- a planting that yields a little, then more, as the crown builds. Artichoke has that
# career only in the two California coastal regions and pnw z9. In the other 25 productive cells it
# is grown as an ANNUAL, so there is no bed age at all: every planting is a year-one planting.
#
# CONSEQUENCE AT THE GATE. With the field null, RAMP-FIRST and RAMP-PROSE both go silent, and that
# silence is correct rather than lucky. RAMP-PROSE compares any bare week range in crop-level prose
# against the ramp's mature entry, on the premise that a crop has ONE duration story. Artichoke
# breaks that premise: `yield_expectations` legitimately carries "six to eight weeks" (VCE's
# annual-culture concentration) and a 5.9-week Connecticut span, neither of which is a bed-age
# figure. Had the fabricated ramp shipped, those true sentences would have been flagged against a
# false field, and the tempting repair would have been to edit the prose. The scope limit is
# recorded in open_findings for whatever crop meets it next.
HARVEST_RAMP_WEEKS = None

HARVEST_RAMP_NA_SEASONED = (
    "No bed-age harvest ramp is published for artichoke, so this guide does not carry one. Two "
    "things are true at once. Where artichoke perennializes, on the California coast and the warm "
    "maritime Northwest, the crown does get more productive with age, and University of California "
    "describes a first-year planting as giving a light pick about a year after planting; but no "
    "source turns that into a picking duration by bed year, and inventing one would put a "
    "manufactured number where a real one is missing. Everywhere else the question does not arise "
    "at all, because artichoke is grown as an annual and every planting is a year-one planting "
    "with no crown carried into a second season. What can be said about duration is said where it "
    "is actually sourced: the concentrated six to eight week flush of annual culture, in "
    "yield_expectations, and the two regional durations carried on the cells that have them.")
HARVEST_RAMP_NA_BEGINNER = (
    "You may have seen crops here that tell you how many weeks of picking to expect in a bed's "
    "second or third year. Artichoke does not get one, because nobody publishes that figure for "
    "it. If your plants live from year to year they do get more productive as they get older, and "
    "if you replant every spring then every plant you grow is a first-year plant and the question "
    "does not apply. Either way, what to expect from a season is under yields.")

# Per-cell harvest_duration_weeks: SPARSE, and only where a source states a regional duration.
# Absence inherits; do not invent regional differentiation. Measured against the corpus, exactly
# three cells have a stated duration, and all three are stated as durations rather than derived
# by subtracting one month name from another:
#   mid_atlantic z7/z8  VCE 438-108: "Expect the production period to be most concentrated over a
#                       six- to eight-week period."  (Virginia, annual culture, both zones)
#   northern_tier z5    CAES, measured: "86% of the buds were harvested between July 17 and
#                       August 27, a 5.9-week span."  (Connecticut, annual culture)
# Everything else inherits. That is the honest outcome of a real check, not a gap.
CELL_DURATION_WEEKS = {
    ("mid_atlantic", "7"): [6, 8],
    ("mid_atlantic", "8"): [6, 8],
    ("northern_tier", "5"): [5, 8],
}


# =============================================================================================
# Cultivars
# =============================================================================================
#
# DELIBERATELY OUTSIDE THE FLAT VARIETY-DETAIL SCHEMA, and this is a decision rather than an
# oversight. `variety_detail_gate` goes in scope the moment any variety carries `maturity_class`,
# and it then requires a per-variety `days_to_maturity` plus the annual_dtm trait set. Artichoke
# cannot supply the first honestly: the only anchored DTM in the whole corpus is crop-level (VCE's
# "60 to 100 days after transplanting"), and the one per-cultivar DTM table that circulates --
# UMaine 2021's bare "Days to Maturity" column -- has no stated basis, matches seed-catalog copy,
# and is contradicted by UMaine's OWN measurements the following year (Green Globe Improved
# measured 76 days after transplanting against a listed 75; Wonder 94 against 90). This arc
# laundered that column once already and retracted it. Opting into the schema would mean putting
# it back to satisfy a required field.
#
# So the varieties stay in the simple shape, and the cost is stated plainly: no gate checks them.
# Recorded in open_findings with the fix named -- a herbaceous-perennial variety archetype whose
# discriminating trait is CHILL REQUIREMENT rather than days to maturity, which is what the
# sources actually differentiate these cultivars on.
#
# `resistance` is ABSENT on every one of them. That is the gate's own N/A branch and it is the
# honest answer: no extension source publishes a cultivar-by-disease rating for artichoke. The
# four resistance-adjacent statements that exist are ungradeable and two contradict each other
# outright (UC IPM: annual varieties "more susceptible to V. dahliae than the perennial Green
# Globe variety"; UC ANR 7221: "All artichoke varieties are susceptible to Verticillium wilt").

_UM = ["umaine_2075"]

VARIETIES = [
    {
        "id": "imperial-star", "name": "Imperial Star", "is_reference": True,
        "confidence_tier": "T1",
        "hero_description": "The one bred to crop in its first year, and the reason artichoke "
                            "works outside California at all.",
        "note_beginner": (
            "Start here if you are anywhere with a real winter. Imperial Star was bred "
            "specifically to produce artichokes in its first season, so it does not need a "
            "long cold spell to get going the way the old types do. Strong, vigorous plants and "
            "reliable yields. The bracts are a little spiny and the buds slightly cone-shaped."),
        "note_seasoned": (
            "The first artichoke bred for annual production, and the cultivar the northeastern "
            "trial literature settles on: Rangarajan's two years of New York trials record it as "
            "producing the higher marketable yields and recommend it for the northeastern United "
            "States. The number that matters is its chill response, where Welbaum measured 83 "
            "percent of Imperial Star flowering after only 205 hours against 25 percent for Green "
            "Globe. Utah State calls it excellent as an annual crop. One conflict worth knowing: "
            "University of Maine describes the plants as strong and vigorous while Texas A&M "
            "calls it less vigorous than Green Globe, and no source reconciles them."),
        "sources": ["umaine_2075", "usu_ext_artichoke", "tamu_eht065", "unr_ext_fs1305"],
    },
    {
        "id": "green-globe", "name": "Green Globe", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "The California perennial standard: superb from an established "
                            "clump, and close to useless in its first year.",
        "note_beginner": (
            "The classic artichoke, and the right choice only if you live somewhere it survives "
            "the winter and you are planting a permanent bed. Grown as a one-year crop it usually "
            "gives you nothing at all, because it needs far more cold than a single spring "
            "provides. It is also grown from divisions rather than seed, which can be hard to "
            "find."),
        "note_seasoned": (
            "University of California's recommended variety for California, and the vegetatively "
            "propagated backbone of perennial plantings. Its chill requirement is the whole story: "
            "roughly 1300 hours below 50°F for complete vernalization, with only 25 percent of "
            "plants flowering at 205 hours. In Virginia barely one plant in seven bore anything at all "
            "during its first season, which is what rules it out of annual culture. Oregon State "
            "notes planting stock is difficult to obtain. Do not confuse it with Green Globe "
            "Improved, which is a separate seed-propagated cultivar."),
        "sources": ["uc_ipm", "vce_438_108", "osu_oregon_veg", "unr_ext_fs1305"],
    },
    {
        "id": "green-globe-improved", "name": "Green Globe Improved", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "Seed-grown and open-pollinated, and its first-year performance "
                            "depends entirely on where you are.",
        "note_beginner": (
            "A seed-grown version of the classic, so you can raise it yourself. How well it does "
            "in its first year depends a lot on your climate: it did well in Maine trials and "
            "poorly in Virginia ones. Give it the full three weeks of cold treatment, since it "
            "needs more than Imperial Star does."),
        "note_seasoned": (
            "An open-pollinated seed cultivar that University of Maine explicitly notes was NOT "
            "bred for annual production, and its results are genuinely regionally split rather "
            "than simply mixed: Ginakes and colleagues report it producing consistently high "
            "yields of marketable artichokes in Maine under 550 hours of chilling, while Virginia "
            "saw it fail in the heat. Read that as a chilling-and-heat interaction rather than a "
            "verdict on the cultivar, and do not state its annual suitability as an absolute. "
            "Sources also disagree on the bracts, with University of Maine calling it spiny and "
            "UF/IFAS thornless."),
        "sources": ["umaine_2075", "umaine_highmoor", "vce_438_108"],
    },
    {
        "id": "emerald", "name": "Emerald", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "The low-chill one, developed for a warm winter and about two weeks "
                            "earlier than Imperial Star.",
        "note_beginner": (
            "Worth looking for if your winters are mild or your springs are short. Emerald needs "
            "very little cold treatment compared with other artichokes, and it crops about two "
            "weeks earlier than Imperial Star. Oregon State recommends it, and it has done well "
            "in Virginia trials too."),
        "note_seasoned": (
            "Oregon State records it as appearing to require very little vernalization, and Texas "
            "A&M puts it about two weeks ahead of Imperial Star with little if any chilling "
            "needed. Connecticut's bulletin adds the provenance that explains the trait: Emerald "
            "and Amethyst were developed for the winter growing area of Arizona, so a low chill "
            "requirement is what they were selected for. Virginia Cooperative Extension reports "
            "Emerald and Early Emerald Pro producing well near Blacksburg, and a Utah SARE "
            "project recommends either Emerald or Imperial Star."),
        "sources": ["osu_oregon_veg", "tamu_eht065", "vce_438_108"],
    },
    {
        "id": "violetto", "name": "Violetto", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "Purple, best-flavored by reputation, and the one that asks most of "
                            "your winter.",
        "note_beginner": (
            "The purple Italian type, widely considered the best eating of the lot. The trade-off "
            "is that it needs more cold than the others and yields less, so treat it as the "
            "choice for flavor rather than for quantity. It suits mild-winter gardens better than "
            "short-season ones. Nevada Extension lists it for southern Nevada."),
        "note_seasoned": (
            "Oregon State's vegetable breeder rates its flavor the best of the cultivars he "
            "discusses while noting a greater vernalization requirement and lower yields, which "
            "is a coherent package rather than a contradiction: it is a perennial-leaning Italian "
            "type being asked to behave like an annual. University of Nevada includes Violetta "
            "among its recommendations for the state's low desert alongside Green Globe and "
            "Imperial Star."),
        "sources": ["osu_ext", "unr_ext_fs1305"],
    },
    {
        "id": "tavor", "name": "Tavor", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "A heavy yielder in Maine trials that loses its cold treatment "
                            "easily, so it rewards getting the chilling right.",
        "note_beginner": (
            "Capable of large crops, and University of Maine's top yielder in one trial year. The "
            "catch is that it loses the benefit of its cold treatment more easily than most, so "
            "keep it under 80°F after chilling and do not skimp on the three weeks."),
        "note_seasoned": (
            "University of Maine records it as seeming to devernalize readily, which puts a "
            "premium on both chilling duration and post-chilling temperature control, and it was "
            "nonetheless the top yielder in the 2023 Maine trial. Carry one unresolved conflict: "
            "the New England Vegetable Management Guide marks Tavor as bred for annual "
            "production while University of Maine's 2021 and 2023 tables mark it as not, and the "
            "two come from the same author group."),
        "sources": ["umaine_2075", "umaine_highmoor", "umass_nevmg"],
    },
    {
        "id": "wonder", "name": "Wonder", "is_reference": False,
        "confidence_tier": "T1",
        "hero_description": "A spineless hybrid bred for annual growing, which makes trimming "
                            "and handling far easier.",
        "note_beginner": (
            "Spineless, which sounds like a small thing until you have trimmed a few spiny "
            "artichokes. Bred for growing as a one-year crop. Like Tavor it loses its cold "
            "treatment easily, so give it the full three weeks and keep it cool afterward."),
        "note_seasoned": (
            "A spineless hybrid bred for annual production. University of Maine flags that it "
            "devernalizes easily and that adequate spring vernalization is therefore especially "
            "important for it. A small documentation conflict inside the same trial series: the "
            "2022 table lists it as F1 and the 2023 table as open-pollinated, both structurally "
            "parsed, and neither is corrected by the other."),
        "sources": ["umaine_2075", "umaine_highmoor"],
    },
]

# NOT CARRIED, and each for a stated reason. Recorded here rather than silently omitted so the
# next pass does not "discover" them and add them back.
#   Colorado Star   -- appears in T1 only inside UMaine's trial tables. Despite the name NO
#                      Colorado State document names it, and its "bred by Keith Mayberry"
#                      attribution traces only to seed-catalog copy. May be discontinued.
#   Talpiot, Grande Buerre -- actively counter-recommended for anywhere needing first-year
#                      cropping: Welbaum measured NO plants of either flowering after as much as
#                      528 hours of chilling.
#   Imperial Star Purple, Madrigal, Opal, Desert Globe, Big Heart, Harmony, Romanesco,
#   Purple Sicilian -- real cultivars with real T1 mentions, but nothing that differentiates them
#                      usefully for a home grower beyond what the seven above already cover.

VARIETIES_NOTE_SEASONED = (
    "Choose on chill requirement first, because it is the trait that decides whether you get a "
    "crop at all, and it is the one the sources actually differentiate these cultivars on. If you "
    "are growing artichoke as an annual, take a cultivar bred for it: Imperial Star is the "
    "reference, with Emerald the low-chill early alternative and Wonder the spineless one. If you "
    "are planting a permanent bed in a mild-winter region, Green Globe is University of "
    "California's recommendation and its high chill requirement stops being a liability once the "
    "plant is established. Flavor is where Violetto earns its place, at the cost of yield and a "
    "longer chilling need. Two cultivars are worth actively avoiding for first-year cropping, "
    "since Welbaum recorded no Talpiot or Grande Buerre plants flowering after as much as 528 "
    "hours of chilling. No disease-resistance ratings are given for any of them, and that is a "
    "finding rather than a gap: see the note on resistance below.")
VARIETIES_NOTE_BEGINNER = (
    "Pick your variety based on how much cold your artichokes will get, not on the picture on the "
    "packet. If you are replanting every year, choose one bred for that, and Imperial Star is the "
    "safe first choice everywhere. Emerald is good if your spring is short or your winter mild, "
    "and Wonder is the one without spines, which your hands will thank you for. If your plants "
    "survive winter and you want a permanent bed, Green Globe is the classic. Violetto is the "
    "purple one people grow for flavor, though you get fewer of them. Avoid Talpiot and Grande "
    "Buerre unless your plants overwinter, because in trials they simply never flowered in their "
    "first year.")

VARIETIES_RESISTANCE_NOTE = (
    "No disease-resistance ratings are published for artichoke cultivars by any extension "
    "service, so none are given here. This is a deliberate blank rather than missing homework. "
    "Four resistance-adjacent statements exist in the literature and none is gradeable: UC IPM "
    "reports that all annual varieties are more susceptible to Verticillium than the perennial "
    "Green Globe, UC ANR 7221 states flatly that all artichoke varieties are susceptible to "
    "Verticillium wilt, University of Maine offers a hedged and uncited claim about Green Globe "
    "Improved, and Utah State credits Imperial Star with good disease resistance without naming a "
    "single disease. The first two contradict each other. A fifth claim in circulation, grading "
    "two cultivars moderately resistant, could not be resolved to a readable source. Manage "
    "artichoke disease by siting, rotation and sanitation rather than by cultivar choice.")


# =============================================================================================
# Region notes -- 16 pairs
# =============================================================================================
#
# R7 IS THE RULE THAT GOVERNS THIS BLOCK. Region prose and cell ratings are two layers and, until
# this arc, NO gate compared them. The asparagus repair left `ca_north_coast` saying its zones
# "perennialize only marginally" for two cells it had just promoted to `perennializes` -- a
# contradiction between two strings the same guide renders to the same reader. Then the asparagus
# lane reproduced the same defect within an hour of documenting it, while watching for it.
#
# So every pair below was written FROM the cells rather than about the region, and where a region
# splits, the note names the split and which zone is which. `tools/region_prose_gate.py` (built in
# this arc) checks exactly that, and these 39 cells are the first thing it ever read.

REGION_NOTES = {
    "northern_tier": (
        # z3,4,5,6,7 -- all marginal, annual culture
        "Every zone here is annual culture, and the rating is marginal all the way down for one "
        "reason: the planting does not survive winter. That is measured rather than assumed. "
        "Upstate New York found no surviving plants at all under six inches of straw, Connecticut "
        "describes field mulches as generally unsuccessful with survival in about one winter in "
        "twenty, and the best result anywhere in this band is 30 to 40 percent at Blacksburg under "
        "hooped vented plastic plus a row cover. So plan to replant. The cropping itself is real: "
        "zones 5, 6 and 7 have the best-documented cycle in the whole crop, with University of "
        "Maine running multi-year trials on this ground. Zone 3 is the exception worth flagging, "
        "since it sits beyond the published record entirely, the northernmost documented trials "
        "being central Maine, upstate New York and Connecticut, and no extension service publishes "
        "a zone 3 protocol. Warmer zones start earlier and pick longer, from July into October at "
        "zone 6 and 7 against August and September further north.",
        "Grow artichoke as a yearly crop everywhere in this region and expect to replant each "
        "spring. Plants almost never survive the winter here, whatever you do, so treat any that "
        "come through as a bonus rather than a plan. The crop itself works well: start seed "
        "indoors in late winter, chill the young plants for about three weeks, plant out after "
        "frost, and pick from late summer until a hard freeze finishes them. If you are in the "
        "coldest zone 3 areas, treat it as an experiment, because nobody publishes instructions "
        "for ground that cold."),
    "mid_atlantic": (
        # z7,8 -- both marginal
        "Both zones are annual culture, and this region is unusual in having its own extension "
        "crop profile: Virginia Cooperative Extension's Specialty Crop Profile is the anchor for "
        "the whole band. Its system is the inverse of the northern one and worth understanding "
        "before you plant, because the chilling happens AFTER planting rather than before. "
        "Transplants go out at or a week or two before the last frost so the seedlings pick up "
        "190 to 240 hours at or below 50°F in the ground, which is why the planting date is "
        "pinned to frost rather than chosen for convenience. Both zones are marginal because the "
        "planting does not persist, and the measured overwintering is poor. The two zones differ "
        "in what limits them: zone 7 is a straightforward spring-planted annual, while zone 8 is "
        "warm enough that summer heat rather than winter is the binding constraint, which is why "
        "Virginia recommends its middle and upper Piedmont and mountains for this crop and "
        "advises against its own southern tier counties outright.",
        "This region has its own extension guide for artichoke, which is rare, and its advice is "
        "worth following exactly. Set transplants out in early spring, around or slightly before "
        "your last frost date, and cover them if a hard freeze threatens. That early planting is "
        "the whole trick: the cool weather right after planting is what makes the plant form buds "
        "later. Harvest in August and September, then pull the plants and start again next "
        "spring. If you are in the warmer zone 8 part, plant as early as you can and give the "
        "plants some afternoon shade, because summer heat is your main enemy here."),
    "mid_south": (
        # z7,8 -- both marginal, documented absence
        "Both zones are marginal and neither is sourced, which is itself the headline for this "
        "region. Not one of the four state extension services covering Arkansas, Oklahoma, "
        "Tennessee and Missouri publishes an artichoke planting date, variety list or crop "
        "profile, and that was established by enumerating their full crop lists rather than by a "
        "failed search. Missouri's perennial-vegetable category contains only asparagus and "
        "rhubarb; Oklahoma lists cardoon, the leaf-stalk form of the same species, and no "
        "artichoke at all. So both windows here are carried over from the Virginia annual system "
        "at a matching last-frost date, and the cells say so. Treat artichoke as a spring-planted "
        "annual, expect summer heat to shorten the crop, and expect the zone 8 side to be tighter "
        "still, which is why it is planted a few weeks earlier to finish bud set before midsummer.",
        "Your state extension service does not cover artichoke at all, so treat this as a trial "
        "rather than a recommendation. The timings here are borrowed from Virginia, which has "
        "similar frost dates and does publish a guide. Set out chilled transplants in early "
        "spring, as early as you can protect them, and pick in late summer. Do not count on "
        "plants surviving the winter, and do not be surprised if a wet winter rots any that try."),
    "warm_arid": (
        # z8 -- marginal
        "The single zone here is a spring-planted annual, deliberately not the Texas fall system, "
        "and the reasoning matters because Texas A&M's fact sheet is the nearest source and it "
        "describes something else. Its fall-planted, summer-dormant cycle is written for Central "
        "Texas, and inland zone 8 winter minima sit below the 25°F floor Texas A&M itself sets "
        "for the crop, so a planting left in the ground over winter is at real risk. New Mexico "
        "State publishes nothing on artichoke at all, its perennial-vegetable section naming only "
        "asparagus and rhubarb. Summer is the other limit: the plant sits through the hottest "
        "weeks and resumes for a fall crop, and dry desert air opens buds faster than heat alone "
        "would.",
        "Plant in early spring rather than fall, and expect to replant each year. Winter here gets "
        "cold enough to kill plants left outside. Through the worst of the summer the plants will "
        "mostly sit still, and they will start growing again in fall, which is when you pick. "
        "Give them shade and steady water in high summer, since dry heat makes buds open before "
        "they are worth eating."),
    "nevada": (
        # z8,9,10 -- all marginal
        "All three zones are marginal and all three are spring-planted annuals, which is the "
        "surprise in this region and it is sourced. The southern Nevada Master Gardener planting "
        "chart gives artichoke a February through late March window and, unlike almost every "
        "other cool-season crop on that chart, no autumn window at all, so there is a single "
        "spring planting that crops in late spring and is finished by the summer heat. Zone 8 is "
        "the higher, colder end of the belt and its window is pushed back to clear the later "
        "frost, with harvest following in midsummer rather than late spring; zones 9 and 10 are "
        "the Las Vegas Valley proper and share the chart's own dates. Nevada Extension separately "
        "recommends Green Globe, Imperial Star and Violetta for the state's low desert. Nothing "
        "in the Nevada material says the planting persists, and summer heat is why it does not.",
        "Plant in late winter or early spring, not in fall, and start seed indoors around the turn "
        "of the year. This catches people out, because most cool-season crops here get a second "
        "autumn planting and artichoke does not. Expect to cut buds in late spring or early "
        "summer depending on how high up you are, then the heat ends it and you start again next "
        "winter. Green Globe, Imperial Star and Violetta are the varieties Nevada Extension "
        "suggests."),
    "utah_dixie": (
        # z8 -- marginal
        "The single zone here is an annual, and its window is assembled rather than sourced, which "
        "the cell records honestly. Utah State's statewide fact sheet places artichoke in its "
        "hardy Group A, to be set out three to four weeks before the frost-free date, but the same "
        "fact sheet explicitly says its dates do not apply to Washington County, and the county "
        "material it defers to never mentions artichoke even though it does list rhubarb, "
        "asparagus and chives. That is a source declining to speak rather than a source not found. "
        "Combining the statewide rule with the county's own hardy window gives the February to "
        "mid-March date here. Utah State's own summer caution applies with force on the hottest "
        "ground in the state: hot weather while the flower stalk is forming often leaves the plant "
        "with no flowers at all.",
        "Start seed indoors in early January and set plants out in late February. That early date "
        "is the whole trick, because artichoke needs cool weather to form its buds and St George "
        "warms up fast. Be aware that no Utah guide actually gives a date for this corner of the "
        "state, so this timing is worked out from the statewide advice rather than read off a "
        "chart. Expect to replant each year."),
    "pnw": (
        # z8 marginal, z9 perennializes -- A SPLIT REGION
        "This region splits, and the split is the winter minimum rather than the summer. Zone 9, "
        "the warm maritime edge in the Puget lowlands and along the immediate coast, stays above "
        "the roughly 15°F line where crowns are lost even under mulch, so the planting persists "
        "and the same crowns carry on for years: that cell is rated perennializes. Zone 8 does "
        "not clear that line reliably and is rated marginal, which is exactly what Oregon State's "
        "vegetable breeder describes, calling western Oregon artichokes short-lived perennials "
        "that need cutting back and mulching and warning that in colder winters they may not "
        "survive even mulched. Plan on three to four productive years there at best. Both zones "
        "share a cool maritime summer that avoids the heat ending the crop inland, and Oregon "
        "State recommends deliberately targeting the late-summer and early-fall crop because "
        "midsummer heat pushes bud stalks up too fast.",
        "This is one of the better climates for artichoke outside California. Plant in spring, cut "
        "the plants back and mulch them heavily in fall, and harvest in September and October. In "
        "the mildest coastal and Puget-area gardens the same plants will keep going year after "
        "year. A little further inland they usually last a few years and then a hard winter takes "
        "them, so enjoy them while they last and be ready to replant."),
    "ca_interior": (
        # z8,9 -- both marginal, short-lived perennial, WATER-limited
        "Both zones are marginal, and the reason is summer water rather than summer heat acting "
        "on its own. Artichoke here is a short-lived perennial rather than either a one-season "
        "annual or a permanent bed: carried through the summer on generous irrigation the same "
        "crowns crop for several years, and left to dry out once in a hot week they are gone. "
        "Texas A&M connects the two directly, noting that summer irrigation keeps temperatures "
        "down inside the crop canopy and that this is what prevents buds opening early. University "
        "of California sources split four ways on this region, from a July set-out to a December "
        "sowing with a March transplant, and one leaflet declines to recommend planting here at "
        "all, though that leaflet is specifically about perennial root-division culture. The July "
        "set-out is what two of them agree on. No source publishes how long a stand lasts in the "
        "Central Valley; the only sourced figure, five to ten years, is commercial coastal "
        "California and is longer than this ground gives.",
        "Plant in July, which feels wrong but is right: the plants grow through fall and give you "
        "buds through the cool months. You do not have to pull them up afterwards. The one thing "
        "that decides whether they last is water. Carrying a big artichoke through a valley "
        "summer takes a lot of it, and that summer watering also cools the plant enough to stop "
        "the buds opening too early. On deep, regular irrigation, ideally drip, the same plants "
        "will crop for several years. Let them dry out once in a heat wave and you will be "
        "starting over."),
    "ca_north_coast": (
        # z9,10 -- both perennializes
        "Both zones perennialize, and this is the crop's home ground: the Monterey and Santa Cruz "
        "coast is where most of the United States artichoke crop is grown. The mechanism here is "
        "different from everywhere else in this guide and that difference is load-bearing. Cool "
        "coastal California does not deliver a chilling EVENT; it sits inside the 45°F to 85°F "
        "band more or less continuously, which extends the flower-bud induction period and "
        "lengthens the production season. University of California's own production bulletin never "
        "mentions chill, vernalization or dormancy at all. So plant rooted offshoots or crown "
        "divisions from late summer into winter, six to eight inches deep, and expect peak "
        "production from March into May. Cutting plants back after the spring peak brings a "
        "second, lighter crop in late fall, and two crops a year are normal from San Francisco to "
        "Santa Barbara. Zone 10 is the warmer, more frost-free strip and opens a few weeks "
        "earlier.",
        "This is the best artichoke ground in the country, and you can treat it as a permanent "
        "planting. Put in root divisions or rooted side shoots between late summer and the end of "
        "the year, six to eight inches deep, and leave them be. The main harvest comes in spring, "
        "around March to May. Cut the plants down after that and you will usually get a second, "
        "smaller crop in the fall. The same clump will keep producing for years before it needs "
        "dividing."),
    "ca_south_coast": (
        # z9,10,11 -- all perennializes
        "All three zones perennialize on a winter-cropping calendar, which is the inverse of what "
        "most people expect from a vegetable and is why this district supplies the winter market. "
        "Set plants in midsummer and harvest from October through April. University of California "
        "gives this district three different windows, running May to July, July to August, and "
        "October to December; the midsummer setting is the one two of the three support, and the "
        "cells say so rather than presenting it as settled. Frost is rare enough here that bud "
        "damage is the exception rather than the rule, and zone 11 is effectively frost-free, "
        "rated from the adjacent zone under a University of California window whose stated scope "
        "is San Luis Obispo County and south with no zone exclusion.",
        "Plant in mid to late summer and pick right through the winter and into spring. That "
        "sounds backwards, but this is a cool-season crop and your winter is its growing season. "
        "The plants stay put and crop again the following year, so this is a permanent bed rather "
        "than something you replant. Frost is rarely a problem, though a hard night can blister "
        "the outside of the buds, which does not affect how they taste."),
    "ca_desert": (
        # z9,10 marginal; z11 unsuitable (VACANT GROUND) -- A SPLIT REGION
        "Zones 9 and 10 are a genuine, commercially important winter crop and are rated marginal "
        "only because the planting does not persist: fields go in from late August through October, "
        "crop from December through April, and are finished by the heat, with University of "
        "California Cooperative Extension noting desert artichokes are seldom marketable after "
        "early April. This is a limit on persistence, not on productivity. Note the organ, which "
        "differs from the coast: desert plantings start from direct-sown seed or from transplants, "
        "with almost none raised from the mother-plant cuttings coastal California relies on. Zone 11 is "
        "a different kind of entry altogether and is rated unsuitable for a non-agronomic reason. "
        "No California desert ground actually reaches zone 11, so that cell is vacant rather than "
        "a verdict on the crop; growers in the low desert should read the zone 9 and zone 10 "
        "guidance.",
        "In the low desert this is a winter crop, which surprises people. Plant in late summer or "
        "early fall, pick from December through spring, and pull the plants when the weather turns "
        "hot. Start again the following fall. Around here artichoke is usually grown from seed or "
        "from bought transplants rather than from divisions off an old plant."),
    "low_desert_az": (
        # z9,10 -- both marginal, DIFFERENT windows per zone
        "Both zones are cool-season annuals finished by the summer heat, but they plant at "
        "opposite ends of the year and that is deliberate rather than an inconsistency. Arizona "
        "publishes two faculty-reviewed low-desert calendars that genuinely differ, and each zone "
        "follows the one written for its own ground rather than averaging them. Zone 9 follows the "
        "cooler Phoenix-side Maricopa County calendar, which transplants from mid January through "
        "March with seed sown from early November to mid December. Zone 10 follows the Yuma "
        "calendar, which plants in September and October and runs the plant through the whole mild "
        "winter for a May and June harvest. Both end the same way, because a low-desert summer is "
        "far past the 86°F ceiling above which bud quality falls apart.",
        "Which end of the low desert you are in decides when you plant, and the two answers are "
        "months apart. Around Phoenix, set transplants out in late winter for a late-spring "
        "harvest, starting seed indoors in November if you are growing your own. Around Yuma and "
        "the warmest ground, plant in early fall instead and let the plants grow all winter for a "
        "May and June crop. Either way the plants are done when the real heat arrives, so plan to "
        "start over."),
    "se_gulf": (
        # z8,9 marginal; z10 survives_no_fruit -- A SPLIT REGION
        "This region splits, and the boundary is the supply of cool hours. Zones 8 and 9 are a "
        "fall-planted, spring-harvested crop rated marginal, on LSU AgCenter's guidance: plant "
        "from October into early November, harvest in spring, and expect to replant, because LSU "
        "is candid that although artichoke is technically a perennial the plants are often lost "
        "over the summer to disease. Winter is not the constraint in that band, since these "
        "winters do bank the 250 to 500 hours below 50°F that bud initiation needs, though the "
        "supply is thinner on the zone 9 side and the set is correspondingly less uniform. Zone "
        "10 is the peninsular-Florida end and crosses the line: there the plant grows well and "
        "never buds at all, so it is rated survives_no_fruit and is an ornamental rather than a "
        "crop. Louisiana is the only Gulf state whose extension service covers artichoke at all, "
        "with Georgia, Alabama, Mississippi and South Carolina all omitting it.",
        "In most of this region artichoke is a fall-planted crop: put plants in during October or "
        "early November, harvest in spring, and replant the following autumn, because summer "
        "disease usually finishes them off. The far southern tip of the region is different. "
        "There the winters never get cool enough for the plant to make buds at all, so you get a "
        "handsome silver-leaved plant and nothing to eat. Check which zone you are in before you "
        "plan a crop."),
    "rgv": (
        # z9,10 -- both marginal
        "Both zones are marginal and both are derived rather than sourced, which is the important "
        "thing to know here. No Texas publication gives a Rio Grande Valley artichoke date. Texas "
        "A&M covers the crop statewide, but every Valley-specific document omits it, including "
        "both editions of the Lower Rio Grande Valley vegetable crops guide and the Valley "
        "homeowner vegetable guide. The single Texas sentence that touches this coast says some "
        "a few home gardeners on the Texas coast do grow it, from crown divisions, seeing a first "
        "harvest roughly a year later, and it names no month. These windows follow the Texas A&M "
        "statewide fall system shifted earlier for a subtropical winter. Rated marginal rather "
        "than lower on the strength of that positive statement, but the cool hours here are few "
        "and summer heat can reverse what does accumulate, so expect an uneven set and expect "
        "some plants to make leaves and never make buds. Zone 10 is warmer and thinner still.",
        "Texas extension does not publish a Valley planting date for artichoke, so treat this as a "
        "trial rather than a plan. Plant in early fall and hope for a late-winter crop. Our "
        "winters barely get cool enough to trigger bud formation, so accept that some plants will "
        "grow well and never produce anything. If you want the best odds, choose a low-chill "
        "variety such as Emerald."),
    "fl_peninsula": (
        # z10,11 -- both survives_no_fruit
        "Both zones are ornamental only, and the evidence is unusually direct because this is "
        "UF/IFAS's own ground. Artichoke needs a run of hours below 50°F to initiate flower buds "
        "and peninsular Florida does not deliver one, so UF/IFAS states that bud formation must be "
        "induced artificially or there is no bud formation in Florida at all. Its own trial reports "
        "the other half: plants treated with gibberellic acid formed buds, while the untreated "
        "ones stayed leafy to the end of the season and never bolted. The untreated plants did not fail, they "
        "simply never bolted. That is why both cells are rated survives_no_fruit rather than "
        "unsuitable. What you get is the plant itself, which UF/IFAS describes as a rosette of "
        "arching, deeply toothed, silvery, woolly leaves 20 to 32 inches long. Treat it as a "
        "single cool-season foliage planting, October to May, since the hot wet summer ends it.",
        "You can grow artichoke here, but you will not get artichokes. The part you eat is a "
        "flower bud, and the plant only makes buds after a stretch of cool weather Florida does "
        "not get, so it stays a large silver-leaved rosette instead. Plenty of people grow it for "
        "exactly that. Plant in October or early November, enjoy the foliage through winter and "
        "spring, and expect the summer heat and rain to finish it off. If you want to eat one, "
        "grow it in a pot you can move somewhere cool for a few weeks."),
    "hawaii_tropical": (
        # z10,11,12,13 -- all survives_no_fruit
        "All four zones are ornamental only. No Hawaii extension source addresses artichoke at "
        "all, so both the rating and the planting window rest on the physiology plus the nearest "
        "documented parallel, which is peninsular Florida, and the cells record that derivation "
        "rather than dressing it as sourced. The mechanism is straightforward: bud initiation "
        "needs a run of hours below 50°F, this climate never banks one, and UF/IFAS's trial found "
        "untreated plants remaining vegetative all season under exactly that condition. The plant "
        "thrives regardless. Unlike Florida there is no hot wet break that ends the planting, so "
        "expect the rosette to persist and keep making leaves indefinitely, and treat the "
        "November to February planting window as a convenience for easier establishment rather "
        "than a deadline the plant is waiting on.",
        "Artichoke grows happily here and will never give you an artichoke. The buds you eat only "
        "form after a spell of cool weather that this climate does not have, so instead you get a "
        "big silver rosette of deeply cut leaves, which is a fine thing to grow on purpose. Plant "
        "in the cooler months if you can, though it is not critical, and once it takes hold it "
        "will just keep growing. If you want to actually eat one, it would have to be in a pot "
        "you can move somewhere cold for several weeks."),
}


# =============================================================================================
# open_findings -- the deliberate absences, on the record
# =============================================================================================
#
# Every entry here is a place this crop declines to publish a number that a reader might expect,
# or a source hazard the next pass would otherwise rediscover the hard way. None blocks launch;
# they are all "we looked, and this is what the record actually supports".

def _f(fid, title, detail, status="accepted", blocks=False):
    # KEY NAMES ARE THE SUITE'S EXISTING VOCABULARY, NOT NEW ONES, and getting there took two
    # tries worth recording. `detail` is unruled, so it flagged register-completeness. Renaming it
    # `detail_seasoned` made it worse: the suffix classifies it as CONSUMER prose, so cp_required
    # then demanded a `detail_beginner` for all twelve -- beginner-register copy for sentences like
    # "RAMP-PROSE assumes one duration story per crop", which nobody should ever read.
    #
    # An open finding is an AUDIT surface, not consumer copy, and the suite already has a name for
    # exactly that: `note_internal`, in register_completeness_gate's AUDIT-LEAF class, ruled bare
    # so no register pairing is demanded. `filed_in_session` and `date` come from the same list.
    # The lesson is the one the suffix system encodes: the suffix is a claim about WHO READS IT.
    return {"id": fid, "title": title, "note_internal": detail, "status": status,
            "blocks_launch": blocks, "filed_in_session": "artichoke_cert_gs_arc", "date": V}


OPEN_FINDINGS = [
    _f("artichoke-hardiness-zone-null",
       "hardiness_zone_min/_max are deliberately null: three T1 sources, three incompatible answers",
       "UMaine Bulletin #2075 calls artichoke hardy in USDA zone 7 and greater; Cornell says "
       "normally hardy to zone 6 if well mulched and occasionally zone 5 in mild winters; OSU and "
       "Welbaum independently measure crown kill at 15°F and 14°F, which is zone 8a-8b ground. The "
       "zone claims are warmer-tolerant than the measured crown-kill temperature allows. Choosing "
       "one would mean preferring a source over two others with no basis, so the field stays null "
       "and the measured temperatures carry the ratings instead."),
    _f("artichoke-no-bed-age-ramp-published",
       "harvest_ramp_weeks is null because no source publishes a bed-age ramp for artichoke",
       "The corpus was checked specifically for it. UC ANR 7221 gives a March-April peak and a "
       "year-round coastal harvest but no duration by bed age; UC Master Gardener gives an onset "
       "('production starts about a year after planting') and not a length; OSU's news article "
       "gives a three-to-four-year stand life and no weeks. A first draft of prose.py authored a "
       "three-year ramp with every figure invented, and it was retracted. Compounding it, a ramp "
       "would describe 6 of 39 cells, since the other 25 productive cells are annual culture with "
       "no bed age at all."),
    _f("artichoke-ramp-prose-scope-dual-mode",
       "RAMP-PROSE assumes one duration story per crop, which a dual-mode crop breaks",
       "harvest_duration_gate's RAMP-PROSE compares any bare week range in crop-level prose "
       "against harvest_ramp_weeks' mature entry. Artichoke legitimately carries week counts that "
       "are NOT bed-age figures: VCE's six-to-eight-week annual-culture concentration and CAES's "
       "measured 5.9-week Connecticut span, both in yield_expectations. Artichoke does not trip "
       "the check today only because its ramp is null. The next crop that carries both a ramp and "
       "a second documented mode will need the check to distinguish them, and the fix is to scope "
       "the comparison rather than to edit true prose."),
    _f("artichoke-variety-resistance-na",
       "Per-cultivar disease resistance ships honest-N/A: no extension source publishes a rating",
       "Four resistance-adjacent statements exist and none is gradeable. Two contradict each "
       "other outright: UC IPM reports all annual varieties more susceptible to V. dahliae than "
       "the perennial Green Globe, while UC ANR 7221 states all artichoke varieties are "
       "susceptible to Verticillium wilt. UMaine's claim for Green Globe Improved is hedged and "
       "uncited and concerns a different plant from UC IPM's Green Globe. USU credits Imperial "
       "Star with 'good disease resistance' and names no disease. A 2021 Turkish paper grading "
       "two cultivars moderately resistant could not be resolved to a readable source and is not "
       "carried. Every variety omits the `resistance` key, which is variety_resistance_gate's own "
       "N/A branch."),
    _f("artichoke-varieties-outside-flat-schema",
       "Cultivars are deliberately outside variety_detail_gate's scope, so nothing gates their shape",
       "Opting in requires a per-variety days_to_maturity, and no anchorable per-cultivar DTM "
       "exists: the only anchored figure in the corpus is crop-level (VCE, 60 to 100 days after "
       "transplanting), and the circulating per-cultivar column (UMaine 2021) states no basis, "
       "matches seed-catalog copy, and is contradicted by UMaine's own measurements the next "
       "year. This arc laundered that column once and retracted it; opting in would mean putting "
       "it back to satisfy a required field. THE COST IS STATED: variety_detail_gate is a no-op "
       "for artichoke. FOLLOW-ON: a herbaceous-perennial variety archetype whose discriminating "
       "trait is CHILL REQUIREMENT rather than days to maturity, which is what the sources "
       "actually differentiate these cultivars on."),
    _f("artichoke-annual-only-suitability-declined",
       "An `annual_only` suitability value would fit 25 cells better than `marginal` does",
       "For a crop that is a productive annual in cold regions, none of the roster's five "
       "suitability values says 'good crop, just replant it'. `marginal` is used literally, "
       "answering whether the planting persists, with the dual-register notes carrying the "
       "annual-culture instruction. Adding the value was declined because it is a "
       "frontend-visible vocabulary change with no renderer support, shipping mid-arc on top of a "
       "category move the frontend has not absorbed either. Recorded as a candidate follow-on "
       "rather than smuggled in as a side effect of this arc."),
    _f("artichoke-no-central-valley-stand-life",
       "productive_lifespan_years is 7, which is coastal-derived, and no Central Valley figure exists",
       "UC's five-to-ten-year replant interval is the only sourced stand life and it describes "
       "commercial coastal California. The ca_interior cells are a short-lived perennial limited "
       "by summer water demand and certainly shorter, but every candidate figure in circulation "
       "is unusable: three-to-five is hearsay, three-to-seven came from an AI summary, "
       "three-to-four is OSU western Oregon, and four-to-seven is UA Yavapai County, a "
       "mid-elevation region. The shortening is therefore stated qualitatively in the cells and "
       "never as a number."),
    _f("artichoke-per-zone-calendar-is-a-modeling-act",
       "No extension source publishes a per-USDA-zone artichoke calendar, so every zone split here is ours",
       "Confirmed across OSU, WSU, UNR, USU, NMSU, VCE, UC and TAMU: sources frame artichoke by "
       "state, by named region, and by last-frost date, never by zone. Zero hits for 'hardiness "
       "zone' or 'USDA zone' in an artichoke context in any of them. Each cell's "
       "resolution_method records the derivation rather than dressing it as sourced, and there is "
       "no zone-3 protocol anywhere in the corpus, the coldest documented trial sites being "
       "central Maine, upstate New York and Connecticut."),
    _f("artichoke-uc-ipm-planting-table-is-degraded",
       "UC IPM's home-garden planting table is a degraded copy of MG Handbook Table 13.2: do not anchor windows to it",
       "It reproduces the same four-district table but DROPS both organ notes and CHANGES Desert "
       "Valleys from September to July, a value four other UC sources contradict. A cell anchored "
       "to it would inherit an organ-less window and a wrong month. District windows are anchored "
       "to the Handbook table instead; uc_ipm remains the correct anchor for IPM ladders, "
       "cultural tips and pH. Separately, Table 13.2 states its own lineage as adapted from a "
       "1994 trade book, so it is republished inside a peer-reviewed handbook but is not original "
       "UC field research."),
    _f("artichoke-wsu-dtm-anchor-ambiguous",
       "WSU EM057E's 'Days to Maturity 85-120' is not used, because its anchor operation is ambiguous",
       "The figure sits in a table titled 'Seeding recommendations' whose other columns are "
       "seed-relative, so whether it counts from seed or from transplant is unstated. An "
       "ambiguous datum does not get to define an anchored field, so days_to_maturity is set from "
       "VCE 438-108, which is explicit about the operation ('bud production will commence 60 to "
       "100 days after transplanting')."),
    _f("artichoke-root-depth-sources-disagree",
       "Sources describe the root system as both deep and shallow; UMaine reconciles them",
       "TAMU EHT-065 calls artichokes deep-rooted; USU says artichoke has a shallow root system. "
       "UMaine #2075 resolves it rather than splitting the difference: the plant makes a taproot, "
       "but most of its feeding roots sit near the surface, so watering often is what helps. "
       "The watering block states it that way, since both sources' practical advice (water often, "
       "do not let it dry out) agrees regardless."),
    _f("artichoke-low-desert-az-calendars-contradict",
       "Two faculty-reviewed Arizona low-desert calendars give opposite planting seasons, and both are kept",
       "AZ1005 (Maricopa County) transplants January 15 to March 31 with seed sown November to "
       "mid December; AZ1615 (Yuma) plants September to October for a May-June harvest. These are "
       "genuinely different low-desert sub-climates rather than an error, so they are NOT merged "
       "or averaged: low_desert_az z9 follows the Phoenix-side calendar and z10 follows Yuma. "
       "AZ1615 carries a known quirk, that its 'dates are for seed unless noted' header is "
       "demonstrably not applied to perennials in the same table, which the z10 note records."),
]
