#!/usr/bin/env python3
"""PLA-6 Round 2 WAVE 2: citrus, 5 crops, SIX fields each. Base 647fe432.

WHY SIX AND NOT FOUR. Every other pill-rendering crop already carried `year_one_notes_*` and
needed only the two new fields. THE FIVE CITRUS CARRY NONE -- measured, not assumed -- which is
exactly why they were the five crops still showing an identical Establishing and First-harvests
pill after PLA-362 wired the app up. So this wave authors the Establishing caption as well, and
citrus is the last of the roster's rendered duplication.

THE FIVE ARE NOT ONE CROP WITH FIVE NAMES, and the wave is built around the ways they diverge,
because a paste here would be invisible and wrong:

  lemon       picked on WEIGHT AND TASTE, not color: fully juicy while still green-tinged.
              The tree is the store, holding fruit for weeks to months.
  lime        picked at full size while still dark to medium green, when juice and acid peak.
              THE FRAMING HERE WAS CORRECTED ON REVIEW. The first draft led with "pick limes
              GREEN" and called it the inverse of the lemon rule, which is how the source frames
              it -- and Trevor's response was that people know what colour a lime is. He was
              right: that sentence tells the reader something they already know, and buries the
              part they do not. What is actually non-obvious is that a lime LEFT ON THE TREE
              slowly turns yellow, and a grower watching that can easily read it as ripening. So
              yellowing is now framed as a HARVEST DEADLINE rather than as a colour rule, which
              is the same sourced fact carrying the information the reader lacks.
              It also does NOT store, is chilling-sensitive, and is held near 50F rather than
              properly cold. Tenderest citrus on the roster; cold that merely nips a mandarin
              kills lime wood.
  mandarin    WILL NOT WAIT: most cultivars puff and desiccate on the branch, so it is picked
              promptly, against navel which holds for weeks. Alternate bearing is pronounced and
              early-summer thinning of an on-year is the highest-leverage intervention.
              Rootstock is a nursery decision -- trifoliate orange is what carries satsuma to
              zone 8.
  navel       ten-to-twelve-month hang; the post-set drop is physiological self-thinning and the
              correct response is none, which is worth saying because the instinct is to feed.
  grapefruit  nine-to-thirteen-month hang, the longest; maturity and quality are DECOUPLED, so
              it reaches legal maturity months before peak flavor and keeps sweetening on the
              tree. Largest of the common citrus, so spacing is a year-one decision that cannot
              be undone. Succumbs to huanglongbing faster than the rest.

EVERY CLAIM IS RESTATED FROM WHAT THE CROP ALREADY ASSERTS: hang lengths, harvest indices,
rootstock and spacing guidance all come from each crop's own `tips_by_stage` and
`establishment_note`. No source id is added.

CROSS-CROP PASTE CHECKED AND CLEAN AT 0 PAIRS above 0.55, which matters more here than in wave 1:
all five share graft-union depth, foot rot, psyllid scouting and little-and-often feeding, so the
year-one strings are where a template would have been easiest to reach for and hardest to spot.

Guard suite:      tools/test_promote_pla6_wave2.py
Mutation harness: tools/mutate_pla6_wave2_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla6_wave2.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '647fe432076030a3bef240d953a31b04c8a4b31140b445d00b78f1b9a18f108f'

NEW_FIELDS = ('year_one_notes_beginner', 'year_one_notes_seasoned',
              'first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
              'full_harvest_notes_beginner', 'full_harvest_notes_seasoned')

TRIO = {
    "grapefruit": {
        "year_one_notes_beginner": (
            "The first year is about building a frame, and with grapefruit it starts with giving it room. "
            "This makes the largest of the common citrus trees, so allow generous spacing, at least about "
            "15 feet from the next citrus, rather than crowding it against a wall or another tree. Strip "
            "the fruit for the first few years: grapefruit hangs its crop for nine to thirteen months, "
            "which is a very long draw on a young tree, and one allowed to carry that load early grows "
            "slowly and stays weak. Plant with the graft union, the knobby joint low on the trunk where "
            "your variety was joined to its roots, two to three inches clear of the finished soil, and "
            "keep mulch pulled back, since a damp union is how citrus gets foot rot. Check soft new "
            "growth for Asian citrus psyllid."
        ),
        "year_one_notes_seasoned": (
            "Spacing is a first-year decision that cannot be undone later: grapefruit makes the largest "
            "of the common citrus trees, and extension guidance of a minimum 15 feet between citrus puts "
            "grapefruit at the roomy end of that range. Strip set for the first several seasons, longer "
            "than for quicker citrus, because the nine-to-thirteen-month hang is an exceptional "
            "carbohydrate draw for a tree still building frame. Set the graft union two to three inches "
            "proud of grade with mulch pulled back, against foot rot. Scout tender flush for Asian citrus "
            "psyllid with particular diligence: grapefruit succumbs to huanglongbing faster than most "
            "citrus, so early detection on an inspectable young tree carries more weight here than "
            "elsewhere on the roster."
        ),
        "first_harvest_notes_beginner": (
            "Grapefruit usually begins bearing in the third or fourth year. Hold soil moisture steady "
            "through the roughly three-week spring bloom, and understand what you are protecting: the "
            "fruit set from these flowers will not be ripe for the better part of a year, so a dry spell "
            "now costs you a crop you will not miss until next winter. A few weeks after set the tree "
            "drops a lot of small fruit by itself. That is self-thinning rather than a fault, and the "
            "fruit that stays sizes up better for it, so do not react by overwatering or overfeeding."
        ),
        "first_harvest_notes_seasoned": (
            "Bearing typically begins in year three or four. Moisture stability through the roughly "
            "three-week bloom protects an unusually long-dated crop, since fruit set now will not reach "
            "maturity for the better part of a year, which makes bloom-period stress uniquely costly on "
            "this crop relative to quicker-ripening citrus. Post-set drop is physiological self-thinning "
            "and warrants no intervention; remaining fruit sizes better for it, and compensating with "
            "water or fertilizer is counterproductive. Grapefruit is self-fruitful, so bloom management "
            "is confined to leaving flowering wood undisturbed. Where seedlessness matters, keep low-seed "
            "varieties away from pollen-heavy citrus, whose pollen adds seed to an otherwise seedless "
            "crop."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year the tree bears, building to full production by year six to nine, "
            "later than quicker citrus because the fruit hangs so long. Grapefruit develops over nine to "
            "thirteen months, so steady deep watering right through summer is the priority; uneven "
            "moisture over that stretch shows up as splitting, dropped fruit, and dry granular flesh "
            "inside. The reward is a fruit that improves while you wait. Grapefruit reaches legal "
            "maturity months before it reaches peak flavor and keeps sweetening on the tree as its acid "
            "falls, so early fruit is tart and late fruit is best. Taste, then taste again later, and "
            "pick over months rather than all at once. In hot desert areas, keep tasting late in the "
            "season and pick before the flesh granulates and dries."
        ),
        "full_harvest_notes_seasoned": (
            "Bearing from roughly year four, full production by year six to nine, later than quicker- "
            "ripening citrus precisely because of the hang. The nine-to-thirteen-month development window "
            "makes irrigation consistency the dominant variable: uneven moisture across it produces "
            "splitting, pre-harvest drop and granulated, dry flesh. Maturity and quality are decoupled "
            "here more than anywhere else in citrus. Grapefruit attains legal maturity months ahead of "
            "peak flavor and continues sweetening on the tree as acid declines, so harvest is a long "
            "taste-led window rather than an event, and the tree functions as the store. The exception is "
            "hot, dry desert: taste through the late season and pick ahead of granulation. Keep pruning "
            "minimal, removing deadwood, which harbors melanose in humid climates, crossing limbs, and "
            "rootstock suckers below the graft."
        ),
    },
    "lemon": {
        "year_one_notes_beginner": (
            "The first year is about building a tree, not picking lemons. Set the plant so the graft "
            "union, the knobby joint low on the trunk where your lemon variety was joined to its roots, "
            "stands two to three inches clear of the finished soil, and keep mulch pulled back from the "
            "trunk: a union that sits damp is the classic way citrus gets foot rot. Water it in well, "
            "then wait for new growth before the first feeding, because fertilizer given to roots that "
            "have not started working just washes past them. Pinch off every flower and any fruit that "
            "sets this year. One or two early lemons are not worth the slower, weaker tree you trade for "
            "them. Feed little and often through the season rather than one heavy dose, since young "
            "citrus roots are shallow and burn easily."
        ),
        "year_one_notes_seasoned": (
            "Prioritize root and canopy development over fruit in the planting year. Set the graft union "
            "two to three inches proud of the finished grade on a mound and keep mulch off the trunk; a "
            "buried or mulch-packed union is the standard entry point for Phytophthora foot rot and "
            "gummosis, and a settling mound can swallow a union that looked correct on planting day. "
            "Irrigate in thoroughly to collapse air pockets, then withhold fertilizer until active flush, "
            "since feeding an inactive root system leaches nitrogen past it and raises salt load. Strip "
            "all first-year bloom and set. Little-and-often citrus feeding through the growing season "
            "suits a shallow, salt-sensitive young root system far better than a single heavy "
            "application. Scout tender flush for Asian citrus psyllid while the tree is still small "
            "enough to inspect properly."
        ),
        "first_harvest_notes_beginner": (
            "A grafted lemon usually sets its first few fruit in the second year, and it is genuinely a "
            "few: treat this as a taste rather than a crop. Keep the soil moisture even right through "
            "flowering, because a dry spell during bloom is what makes a young tree drop its blossoms and "
            "its small fruit. Do not prune hard now. Lemons flower on recent growth, so cutting the tree "
            "back at bloom removes the very wood carrying this year's lemons; save shaping for after "
            "harvest. As the fruit sizes, water deeply and on a steady rhythm rather than swinging "
            "between bone-dry and soaked, since that swing is what splits rinds."
        ),
        "first_harvest_notes_seasoned": (
            "Expect a token second-year set on a grafted tree, sized to sample rather than to crop. "
            "Moisture stability through bloom is the controlling variable: drought stress during "
            "flowering drives blossom and young-fruit abscission, and lemon is self-fruitful so there is "
            "no pollinator to protect, only the flowers the tree already carries. Defer structural "
            "pruning past harvest; lemon flowers on recent growth, so heavy cuts at bloom remove the "
            "current crop's bearing wood. Through fruit development, irrigate deeply on a consistent "
            "interval: the pulp swells faster than the rind can stretch, so wet-dry oscillation is what "
            "produces rind split and drop. On high-pH or sandy ground, watch new leaves for interveinal "
            "yellowing and correct with a citrus feed carrying iron, zinc and manganese, which a general "
            "fertilizer will not."
        ),
        "full_harvest_notes_beginner": (
            "From about the third year the tree carries a real crop, and lemon has a habit worth knowing: "
            "judge ripeness by feel and taste, not by color. A lemon can be fully juicy while still "
            "greenish, and waiting for a deep yellow often means picking past its best. Lift a fruit that "
            "feels heavy for its size, taste one, and let that set your standard for the tree. Then use "
            "the tree as your storage. Ripe lemons hold on the branch for weeks and even months with "
            "little loss, so pick as you need them rather than stripping the tree and scrambling to use "
            "the crop. Keep pruning light: deadwood, crossing limbs, and any shoots coming from below the "
            "graft union, which are rootstock and will never bear a lemon."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year three. Harvest on weight and flavor rather than rind "
            "color: lemon reaches eating quality while still green-tinged in many climates, and color-led "
            "picking runs late. The tree is also the store. Fruit holds on the branch for weeks to months "
            "with minimal quality loss, so harvest incrementally against demand instead of stripping and "
            "then racing the crop. Maintenance pruning stays minimal: deadwood, crossing limbs, and "
            "rootstock suckers below the graft union, which carry rootstock genetics and will never bear "
            "your variety, yet will take the canopy if left. In borderline-cold zones a mature tree still "
            "needs frost protection: citrus injury escalates from leaf and fruit loss into wood kill as "
            "temperature drops and the cold holds, so cover or add heat before a hard night, not after."
        ),
    },
    "lime": {
        "year_one_notes_beginner": (
            "The first year is about establishing the tree, and with lime the first decision is where it "
            "lives. Limes are the most cold-tender citrus there is, so outside a truly frost-free area an "
            "in-ground lime is a gamble that a potted one avoids. Plant only once all frost danger has "
            "passed. Set the graft union, the knobby joint low on the trunk where your lime was joined to "
            "its roots, two to three inches clear of the finished soil, and keep mulch off the trunk, "
            "because a union sitting damp is how citrus gets foot rot. Pinch off every flower and any "
            "fruit that sets this year: one or two early limes cost you a slower, weaker tree. Feed "
            "little and often with a citrus fertilizer rather than one heavy dose."
        ),
        "year_one_notes_seasoned": (
            "Siting is the governing first-year decision for this crop specifically: lime is the most "
            "cold-sensitive of the common citrus, so outside genuinely frost-free ground a container is "
            "the defensible choice and keeps the tree movable. Plant after all frost risk has passed. Set "
            "the graft union two to three inches proud of finished grade and keep mulch clear of the "
            "trunk, against foot rot and gummosis. Strip all first-year bloom and set. Feed little and "
            "often through the season; UF/IFAS starts young limes at roughly a quarter pound per "
            "application, which suits a shallow, salt-sensitive root system far better than one heavy "
            "dose. In humid regions, water the ground rather than the canopy, since wetting open tissue "
            "feeds the Colletotrichum postbloom fruit drop that makes lime fruitlets abscise."
        ),
        "first_harvest_notes_beginner": (
            "A grafted lime usually sets its first few fruit in the second year. Keep soil moisture even "
            "right through flowering, since a dry spell at bloom is what makes a young tree shed its "
            "blossoms and small fruit. In a humid area, water the ground rather than the flowers: wetting "
            "open blossoms feeds postbloom fruit drop, a disease that makes the tiny limes fall off. "
            "Limes mature fast once set, in roughly 90 to 120 days, so the window between flower and "
            "fruit is short and steady watering through it matters more than anything else you can do."
        ),
        "first_harvest_notes_seasoned": (
            "Expect a token second-year set on a grafted tree; air-layered or cutting-grown Key limes can "
            "fruit inside a year, seedlings a year or two later. Moisture stability through bloom governs "
            "retention, and lime is self-fruitful with Persian lime parthenocarpic, so the task is "
            "protecting existing flowers from stress rather than securing pollination. In humid regions "
            "irrigate at ground level: wetting open blossoms feeds Colletotrichum postbloom fruit drop, "
            "and full sun with airflow suppresses it. Fruit development runs only about 90 to 120 days, "
            "so the interval between set and maturity is short and unforgiving of wet-dry swings. On "
            "calcareous or sandy ground, interveinal chlorosis on new leaves signals the iron, manganese "
            "and zinc deficiency lime shows on alkaline soil; chelated iron and nutritional sprays "
            "correct it, a plain fertilizer will not."
        ),
        "full_harvest_notes_beginner": (
            "From about the third year the tree carries a real crop, and the thing to watch is how long "
            "you leave fruit hanging. A lime that stays on the tree too long turns yellow, and that "
            "yellow is not ripeness, it is the fruit going past: acid has dropped, flavor has flattened, "
            "and it is close to falling. So treat yellowing as your deadline rather than your signal. "
            "Pick at full size while the skin is still dark to medium green, which is when juice and acid "
            "are at their peak. Do not try to store them like lemons either. Limes are short-lived once "
            "picked and are damaged by cold, so keep them only cool, around 50\u00b0F, rather than properly "
            "cold, use them fresh, and turn a heavy summer pick into frozen juice and zest. Protect the "
            "tree on every freeze night even when mature, because cold that merely nips a mandarin can "
            "kill lime wood."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year three. Harvest at full size while the rind is still dark "
            "to medium green, when juice and acid peak. Yellowing on the tree is a harvest deadline "
            "rather than a maturity index: it marks declining acid and imminent abscission, so fruit "
            "allowed to color is already past its useful window. Postharvest handling also diverges from "
            "the rest of citrus: lime is short-lived off the tree and chilling-sensitive, so hold around "
            "50\u00b0F rather than refrigerating properly cold, move fruit fresh, and process a heavy flush to "
            "frozen juice and zest. Keep pruning light, confined to deadwood, crossing limbs and "
            "rootstock suckers below the graft, and time shaping to late winter or early spring ahead of "
            "the flush rather than fall, so tender growth is not pushed into cold. Freeze protection "
            "remains mandatory at every maturity: temperatures that merely defoliate a mandarin kill lime "
            "wood."
        ),
    },
    "mandarin-clementine": {
        "year_one_notes_beginner": (
            "The first year is about building the tree, not picking fruit, and mandarins make that harder "
            "than most because they are eager to fruit young. Strip the first year's fruit anyway: a "
            "young tree carrying a crop grows slowly and stays structurally weak. Plant with the graft "
            "union, the knobby joint low on the trunk where your variety was joined to its roots, "
            "standing two to three inches clear of the finished soil, and keep mulch off the trunk, since "
            "a damp union is how citrus gets foot rot. If you garden at the cold edge of citrus country, "
            "buy a tree grafted onto trifoliate orange rootstock; that is the graft that lets a satsuma "
            "push into zone 8. Check the soft new growth for Asian citrus psyllid while the tree is small "
            "enough to inspect properly."
        ),
        "year_one_notes_seasoned": (
            "Strip first-year set despite the crop's precocity: satsuma in particular will try to fruit "
            "early, and a young tree carrying a load grows slowly and stays structurally weak. Set the "
            "graft union two to three inches proud of finished grade with mulch pulled back, against foot "
            "rot. Rootstock is the load-bearing purchase decision at the cold margin: trifoliate orange "
            "(Poncirus trifoliata) is the standard for maximum cold hardiness and is what carries satsuma "
            "into zone 8, so it is chosen at the nursery rather than corrected later. Scout tender flush "
            "for Asian citrus psyllid while inspection is still practical; the psyllid vectors "
            "huanglongbing and feeds and oviposits on new growth, so detection on a small tree is worth "
            "more than on a large one."
        ),
        "first_harvest_notes_beginner": (
            "Mandarins are precocious and usually start bearing in the second or third year, a little "
            "earlier than a navel orange. Hold the soil moisture steady through the roughly three-week "
            "spring bloom, because the whole crop sets from that one flush and drought stress now drops "
            "the flowers and the young fruit behind them. If you are growing a seedless variety such as "
            "Clementine, keep it away from other pollen-bearing citrus during bloom: seedless kinds stay "
            "seedless only in isolation, and a fertile neighbour will put seeds in an otherwise seedless "
            "crop."
        ),
        "first_harvest_notes_seasoned": (
            "Mandarin is precocious and typically begins bearing in year two or three, ahead of navel. "
            "Moisture stability through the roughly three-week bloom is the controlling variable, since "
            "the crop sets from a single main flush. Isolation matters for seedless cultivars: Clementine "
            "and W. Murcott are seedless only without cross-pollination and will set seed when fertile "
            "pollen is nearby, so bloom-period proximity to other citrus is a varietal decision rather "
            "than a general one. Begin managing alternate bearing from the first substantial crop rather "
            "than after it becomes established, because mandarin swings harder between on and off years "
            "than the rest of the roster."
        ),
        "full_harvest_notes_beginner": (
            "From about the third year the tree carries a real crop, and mandarins bring two habits that "
            "catch people out. First, they will not wait for you. Unlike a navel, most mandarins do not "
            "hold on the tree: a satsuma left too long goes puffy and dries out inside. Taste before you "
            "pick, then pick promptly and refrigerate. The exceptions are late holding types such as Gold "
            "Nugget and Pixie, which do store well on the branch into spring. Second, mandarins swing "
            "hard between a heavy year and a light one. On a heavy year, thin the fruit in early summer; "
            "that single pass is the most effective thing you can do, because it cuts the drain before it "
            "suppresses next year's bloom. Keep pruning minimal, and pull any suckers from below the "
            "graft."
        ),
        "full_harvest_notes_seasoned": (
            "Full production builds by roughly year four to seven depending on rootstock and conditions. "
            "Two crop-specific behaviors govern the mature tree. Fruit does not hold: mandarin colors "
            "ahead of full sweetness in some climates and most cultivars puff and desiccate on the "
            "branch, so sample for flavor, then harvest promptly and refrigerate. Late holding types "
            "(Gold Nugget, Pixie) are the deliberate exception and store on the tree into spring. And "
            "alternate bearing is pronounced: early-summer thinning of a heavy set is the highest- "
            "leverage intervention available, cutting carbohydrate drain before it suppresses the "
            "following season's bloom, with steady fertility and consistent irrigation damping the rest. "
            "A sharp unexplained drop is not alternate bearing and points instead at a root, water or "
            "disease problem. Pruning stays minimal, with rootstock suckers, often thorny trifoliate, "
            "removed on sight."
        ),
    },
    "orange-navel": {
        "year_one_notes_beginner": (
            "The first year is about building a frame, not growing oranges. Strip the fruit for the first "
            "couple of years: a navel carries its crop for ten to twelve months, which is a long, heavy "
            "draw on the tree, and one allowed to hold that load young grows slowly and stays weak. Plant "
            "with the graft union, the knobby joint low on the trunk where your navel was joined to its "
            "roots, standing two to three inches clear of the finished soil, and keep mulch pulled back "
            "from the trunk, because a damp union is the classic way citrus gets foot rot. Water in well "
            "to settle the soil, then wait for new growth before feeding, since fertilizer given before "
            "the roots are working simply washes past them. Check soft new growth for Asian citrus "
            "psyllid while the tree is small."
        ),
        "year_one_notes_seasoned": (
            "Strip set for the first two seasons rather than one: navel carries a ten-to-twelve-month "
            "crop, an unusually long carbohydrate draw, and a young tree permitted to hold it develops "
            "slowly and stays structurally weak. Set the graft union two to three inches proud of "
            "finished grade with mulch pulled back, against foot rot. Irrigate in to settle the profile, "
            "then defer the first feed until active flush, since fertilizer applied to inactive roots "
            "leaches past them and adds salt load for nothing. Scout tender flush for Asian citrus "
            "psyllid while the tree is small enough to inspect thoroughly; the psyllid vectors "
            "huanglongbing, and new growth is where it feeds and lays."
        ),
        "first_harvest_notes_beginner": (
            "Navels usually begin producing in the third year after planting a grafted tree. Hold the "
            "soil moisture steady through the roughly three-week spring bloom, because a navel sets its "
            "entire crop from that one flush and drought stress now drops the flowers and the young fruit "
            "behind them. A few weeks after set the tree will drop a lot of small fruit on its own. That "
            "is not a problem and not something to fix: the tree is self-thinning to what it can actually "
            "finish, and the fruit that stays will size up better for it. Do not respond by overwatering "
            "or overfeeding. Skip heavy pruning during and just after bloom, and leave the flowering wood "
            "alone."
        ),
        "first_harvest_notes_seasoned": (
            "Bearing typically begins in year three on a grafted nursery tree. Moisture stability through "
            "the roughly three-week bloom governs the season, since navel sets its entire crop from one "
            "main flush. The June-drop several weeks after set is physiological self-thinning, not "
            "stress, and the correct response is none: the tree is shedding beyond its carrying capacity "
            "and remaining fruit sizes better for it, so overwatering or overfeeding in reaction is "
            "actively counterproductive. Navel is self-fruitful and requires no pollinizer, so bloom- "
            "period management reduces to leaving flowering wood and developing fruit undisturbed and "
            "deferring structural pruning."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year the tree carries a real crop, building toward full production by "
            "year five to eight. Navels take their time in every direction: the fruit develops over ten "
            "to twelve months, so water deeply and on a steady rhythm right across the summer, since "
            "uneven moisture over that long stretch shows up later as split and dropped fruit. When it "
            "comes to picking, taste first. Navels color up before they are actually sweet, and in a mild "
            "winter the orange skin is a poor guide, so sample a fruit from the sunny side and let flavor "
            "call it. Then take your time: ripe navels hold well on the branch for weeks, so pick what "
            "you need and let the rest keep storing themselves outdoors."
        ),
        "full_harvest_notes_seasoned": (
            "Full production is reached by roughly year five to eight depending on rootstock and "
            "conditions. The defining constraint is the ten-to-twelve-month hang: irrigation consistency "
            "across that entire development window, not just at set, is what prevents late splitting and "
            "pre-harvest drop, so a steady summer rhythm outranks volume. Harvest on flavor rather than "
            "rind color, which colors ahead of maturity and is an unreliable index in mild-winter "
            "regions; sample from the sun side before committing. Fruit stores on the tree for weeks, so "
            "pick incrementally against demand rather than stripping. Expect alternate bearing and damp "
            "it with steady fertility and consistent irrigation; a sharp unexplained drop is a different "
            "signal and points at a root, water or disease problem worth chasing."
        ),
    },
}

EDITS = {}   # wave 2 authors new fields only.


def renders_pills(crop):
    """plant-app's own gate, reproduced. An N/A crop takes the trio by ABSENCE, never by null --
    A29 register-fill forbids a `_beginner`/`_seasoned` field that exists and is unauthored, and
    that ruling came from this arc's own pilot bouncing on sage."""
    y = crop.get('years_to_first_harvest')
    return (isinstance(y, list) and len(y) >= 2
            and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in y[:2]))


def apply_to(data):
    by = {c['slug']: c for c in data['crops']}
    for slug, fields in TRIO.items():
        for field, value in fields.items():
            by[slug][field] = value
    for (slug, field), (find, replace) in EDITS.items():
        by[slug][field] = by[slug][field].replace(find, replace)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

    raw = open(canonical, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print('ABORT: base SHA mismatch\n  expected %s\n  found    %s' % (args.expect_sha, sha),
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    by = {c['slug']: c for c in data['crops']}

    for slug in TRIO:
        if slug not in by:
            print('ABORT: no crop %r' % slug, file=sys.stderr)
            return 1
        if not renders_pills(by[slug]):
            print('ABORT: %s renders no pills; it takes the trio by ABSENCE' % slug, file=sys.stderr)
            return 1
        for field, value in TRIO[slug].items():
            if field in by[slug]:
                print('ABORT: %s.%s already exists; this promote creates it' % (slug, field),
                      file=sys.stderr)
                return 1
            if not value:
                print('ABORT: %s.%s is empty' % (slug, field), file=sys.stderr)
                return 1

    apply_to(data)
    print('WAVE 2 -- citrus, %d crops, six fields each:' % len(TRIO))
    for slug in sorted(TRIO):
        hi = by[slug]['years_to_first_harvest'][1]
        chars = sum(len(v) for v in TRIO[slug].values())
        print('  %-15s full harvest from year %d   %5d chars' % (slug, hi, chars))

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print('DRY RUN -- would write %d bytes, sha %s' % (len(out), new_sha))
        return 0
    with open(canonical, 'wb') as fh:
        fh.write(out)
    print('wrote %d bytes\nnew canonical SHA: %s' % (len(out), new_sha))
    return 0


if __name__ == '__main__':
    sys.exit(main())
