#!/usr/bin/env python3
"""PLA-6 Round 2 WAVE 4, THE LAST: artichoke, fig, mulberry, persimmon, pomegranate. Base 97c63704.

THIS WAVE CLOSES THE ROLLOUT. With it, all 26 pill-rendering perennials carry the year-pill trio,
and `perennial_year_gate`'s PILL-CAPTION family goes to zero, at which point it can arm as a
whole_crop_gate A-number instead of running standalone.

ARTICHOKE IS WHY THIS ARC EXISTS. Trevor's original report, 2026-08-05, was that artichoke's
year-three description rested on an unexplained technical term with no gloss and thin operational
detail. Round 1 found the cause was not authoring at all: the Full-harvest pill rendered
`firstSentence(harvest_ready_seasoned)`, which sheared a full sourced paragraph down to "Cut on
bract tightness, not on size." -- seven words, opening on the exact term he flagged. The beginner
register was worse at three words: "Squeeze the bud."

Both are fixed here at the root rather than by rewriting the paragraph that was never the problem.
`full_harvest_notes_*` now carries purpose-written mature-bed guidance, and per v1.3 sec9.3 the
BEGINNER half names and glosses the term in place -- "its bracts, the tough overlapping scales" --
rather than substituting it away, because a grower meets the word in every artichoke instruction
they will read. The seasoned half uses it bare, which is the register working: sec9.3 scopes the
gloss requirement to the beginner half explicitly ("a defect in the beginner half alone").

Artichoke's real mature-bed content also turned out to be something no truncation could have
carried: the annual cut-back is a SCHEDULING instrument, not tidying. Cut back mid-April to
mid-June and the planting crops in fall, winter and spring; cut back in late August or September
and it crops in summer instead. UC IPM further quantifies the same operation as pest control,
reporting roughly 95 percent reduction in plume moth where plants are cut 2 to 3 inches below soil
level and the tops shredded and buried under at least 6 inches of soil.

THE OTHER FOUR, and what keeps them apart:

  fig          color is NOT ripeness; a fully colored fig can be hard and inedible. Ripe means
               soft with a BENT NECK so the fruit droops. Prune light and late: fig carries a
               breba crop on last year's wood, so heavy heading forfeits the early crop.
  mulberry     no thinning, no firm-pick stage, picked dead ripe and perishable in hours. A
               mature tree outproduces a household, so the honest advice is shaking branches onto
               a sheet and freezing the surplus.
  persimmon    TYPE decides everything: non-astringent (Fuyu) picked firm and eaten crisp;
               astringent (Hachiya) picked at full color and INEDIBLE until ripened jelly-soft.
               Late bloom in May to June evades the frosts that cost earlier crops their year.
  pomegranate  rind SPLITTING is the defining failure and it is a scheduling problem: a dry
               interval followed by heavy water or rain. Harvest is indexed on a cluster of
               signals including a hexagonal profile and a tinny note when tapped, and the fruit
               is NOT chilling-sensitive, unlike most subtropical fruit.

Every claim is restated from what each crop already asserts; no source id is added.

Guard suite:      tools/test_promote_pla6_wave4.py
Mutation harness: tools/mutate_pla6_wave4_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla6_wave4.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '97c63704812e2192fe8ec27ba0007e24db5dadbc88473aeccca5bba217c1521c'

NEW_FIELDS = ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
              'full_harvest_notes_beginner', 'full_harvest_notes_seasoned')

TRIO = {
    "artichoke": {
        "first_harvest_notes_beginner": (
            "A perennializing artichoke gives you a light pick about a year after planting, and the skill "
            "to learn now is knowing when a bud is ready. It is not size. Squeeze it: if the bracts, the "
            "tough overlapping scales that make up the bud, are still shut flat against one another, cut "
            "it. Once they loosen and start to spread apart, that bud has gone woody and bitter and no "
            "amount of cooking brings it back. Take the big bud at the top of the stalk first, cutting 2 "
            "to 3 inches of stem with it; the smaller ones lower down come along afterward. Keep the "
            "water steady once buds start forming, because a plant under moisture stress opens its buds "
            "early and shows black tips."
        ),
        "first_harvest_notes_seasoned": (
            "A perennializing planting yields a light pick roughly a year after set. Index maturity on "
            "bract tightness, meaning how tightly the overlapping scales are still closed, rather than on "
            "diameter: University of California is explicit that on seeded varieties a mature bud neither "
            "enlarges further nor re-tightens, so waiting past closure buys nothing and costs the bud to "
            "woodiness. Take the terminal bud first, since it matures well ahead of the two or three "
            "secondaries below it, and cut with 2 to 3 inches of stem attached. Irrigation through the "
            "bud period is a quality intervention rather than a survival one: Texas A&M attributes canopy "
            "cooling to summer irrigation and identifies it as what prevents buds opening early, while "
            "Utah State's rule is simply not to water-stress a plant once flower buds have formed. "
            "Moisture stress presents as black tip."
        ),
        "full_harvest_notes_beginner": (
            "From about the second year the planting is in full production, and two things run the year. "
            "The first is picking on tightness rather than size: squeeze each bud, and cut it while its "
            "bracts, the tough overlapping scales, are still shut flat against each other. Once they "
            "loosen the bud is woody and bitter. Heat compresses that window sharply, so above about 86\u00b0F "
            "check every day instead of every few days. The second is the annual cut-back, and it is a "
            "scheduling tool rather than tidying up. Cut back between mid-April and mid-June and the "
            "plant crops in fall, winter and spring; cut back in late August or September and you get a "
            "summer harvest instead. Start watering again about a month after. Do the cut-back properly "
            "and it doubles as pest control: cutting 2 to 3 inches below soil level, then shredding and "
            "burying the tops under at least 6 inches of soil, cuts artichoke plume moth by about 95 "
            "percent."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year two on a persisting planting. Harvest indexing stays on "
            "bract tightness, meaning bracts still closed flat against one another, never on diameter, "
            "and heat above 86\u00b0F compresses the window enough to force daily rather than periodic "
            "checking, since the heart loses tenderness and compactness as buds open. The annual cut-back "
            "is the year's real decision and it SCHEDULES the crop rather than tidying the plant: a cut- "
            "back between mid-April and mid-June sets up fall, winter and spring cropping, while one in "
            "late August or September sets up a summer harvest, with irrigation resuming about a month "
            "afterwards. Do not confuse it with stumping, the removal of spent bearing stalks at three- "
            "to-four-week intervals through the year. UC IPM quantifies the cut-back's second function: "
            "cutting plants 2 to 3 inches below soil level, shredding the tops and incorporating them "
            "under at least 6 inches of soil reduces plume moth infestation in perennial fields by "
            "roughly 95 percent. Clear nearby thistles, which host it too."
        ),
    },
    "fig": {
        "first_harvest_notes_beginner": (
            "Fig is one of the quickest perennials to pay you back, often giving a little fruit in its "
            "first or second year. The thing to learn now is what ripe actually looks like, because color "
            "will fool you: a fig can be fully colored and still hard and inedible. Wait for it to go "
            "soft and for its neck to bend so the fruit droops down instead of standing out from the "
            "branch. A drop of syrup at the base is a good sign. Figs do not ripen at all after picking, "
            "so there is nothing to gain by picking early. Prune lightly and only after the hardest cold "
            "has passed, because fig carries an early crop on last year's wood and cutting hard trades "
            "that crop away."
        ),
        "first_harvest_notes_seasoned": (
            "Fig is precocious and commonly sets a light crop in its first or second season. Maturity "
            "indexing is the skill to establish: color is not ripeness, and a fully colored fig can "
            "remain firm and unready. The reliable signals are full softening, neck bend so the fruit "
            "droops rather than standing out from the shoot, and a nectar drop at the eye. The crop is "
            "non-climacteric, so early picking is unrecoverable. Prune lightly and only after the hardest "
            "cold has passed: fig bears a breba crop on the previous season's wood as well as a main crop "
            "on new growth, so heavy heading trades the early crop away. In cold climates train as an "
            "open multi-stem bush rather than a single trunk, so that a winter that kills the top regrows "
            "from several low stems and ripens a main crop far faster."
        ),
        "full_harvest_notes_beginner": (
            "From about the second year the plant is in full production, and it ripens a few figs at a "
            "time over many weeks rather than all at once. So pick every day or two. A ripe fig is soft, "
            "droops on a bent neck, has colored up fully, and comes away with the lightest pull. Ripe "
            "figs spoil within a day or two, so eat, chill, freeze or dry them promptly. Get netting on "
            "as the fruit starts to color, because birds find figs fast, and pick up any soured or "
            "dropped fruit as you go so beetles and souring yeasts do not build up. Keep the winter "
            "pruning light, since fig fruits on both last year's wood and this year's."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year two, ripening a few fruit at a time across many weeks, "
            "which makes harvest a standing every-day-or-two task rather than an event. Index on "
            "softening, neck bend and effortless detachment; the crop is non-climacteric and gains "
            "nothing after picking. Shelf life is a day or two, so consumption, refrigeration, freezing "
            "or drying follows harvest immediately. Exclusion netting goes up at color break, and soured "
            "and dropped fruit is removed on each pass to suppress dried fruit beetle and souring yeasts, "
            "which build on fermenting fruit rather than on sound fruit. Dormant pruning stays light and "
            "late, after the hardest cold: fig carries both a breba crop on last season's wood and a main "
            "crop on current growth, so heavy heading forfeits the early crop outright."
        ),
    },
    "mulberry": {
        "first_harvest_notes_beginner": (
            "Your first mulberries usually arrive in the second year. Do not thin them; the tree ripens "
            "its whole crop gradually over several weeks and it sizes its fruit perfectly well on its "
            "own. What matters far more is getting bird netting ready as the first berries start to "
            "color, because birds will find a mulberry before you do. If you want easy picking later, "
            "this is also the moment to head the young tree down to a reachable height: mulberry "
            "tolerates hard shaping while it is young, and it needs far less structural pruning than a "
            "stone fruit ever will."
        ),
        "first_harvest_notes_seasoned": (
            "Bearing typically begins in year two. Thinning is not practiced on this crop: ripening is "
            "sequential over several weeks and fruit sizes without intervention, so labor is better spent "
            "on exclusion netting timed to first color break. Formative decisions are cheap now and "
            "expensive later: mulberry tolerates hard heading while young, so establishing a reachable "
            "working height early is the single most useful structural intervention, and the species "
            "needs far less renewal pruning than stone fruit. Mulberry is self-fruitful and wind- "
            "pollinated, with many cultivars setting parthenocarpically, so no pollinizer is required and "
            "a single named tree crops alone."
        ),
        "full_harvest_notes_beginner": (
            "From about the third year the tree carries a full crop, and it will be a lot of fruit; a "
            "mature mulberry yields more than a household can use. There is no picking firm and ripening "
            "later the way you would with a peach: a mulberry is picked dead ripe. It should be fully "
            "dark (or the ripe color of your variety, since some are white or pink), soft, sweet, and "
            "ready to fall into your hand at the lightest touch. Shaking the branches onto a sheet spread "
            "underneath is the practical way to bring in a big crop. The fruit is extremely perishable, "
            "so pick into shallow containers and refrigerate or freeze the same day, freeze the surplus, "
            "and clear fallen fruit so it does not stain paving or draw pests."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year three, at volumes that routinely exceed household use. The "
            "crop is picked dead ripe and has no firm-pick stage: index on full cultivar color, "
            "softening, sweetness and detachment at the gentlest touch. Shaking branches onto a ground "
            "sheet is the standard method at volume. Perishability is the binding constraint, measured in "
            "hours rather than days, so harvest into shallow containers and refrigerate or freeze the "
            "same day, with freezing as the realistic outlet for surplus. Manage the drop deliberately: "
            "fallen fruit stains hard surfaces and draws pests, so siting and routine clearing both "
            "matter. Dormant pruning stays light, confined to dead, crossing and crowding wood plus any "
            "height reduction, since mulberry fruits without the hard annual renewal stone fruit demands."
        ),
    },
    "persimmon": {
        "first_harvest_notes_beginner": (
            "Persimmon takes its time, usually giving a first crop somewhere in the third to fifth year. "
            "The most important thing to sort out is which type you have, because it changes how you "
            "harvest completely. A non-astringent type such as Fuyu is picked firm and eaten crisp, like "
            "an apple. An astringent type such as Hachiya, and most American persimmons, is picked at "
            "full orange color but is not edible yet: it has to sit until it goes completely soft and "
            "jelly-like before the pucker clears. Either way, clip or gently twist the fruit off with its "
            "leafy cap attached rather than pulling. A natural fruit drop in early summer is normal; a "
            "heavy one usually means water stress or too much nitrogen."
        ),
        "first_harvest_notes_seasoned": (
            "First cropping typically falls between years three and five. Cultivar type governs harvest "
            "protocol entirely and is the fact to establish first: non-astringent types (Fuyu) are picked "
            "firm and eaten crisp, while astringent types (Hachiya and most American persimmons) are "
            "harvested at full color but require post-harvest ripening to a jelly-soft, nearly "
            "translucent stage before astringency clears. Detach by clipping or twisting with the calyx "
            "attached rather than pulling. Early-summer physiological drop is normal; disproportionate "
            "drop indicates water stress or excess nitrogen. Build the framework deliberately while the "
            "tree is young, because persimmon wood is brittle and heavy fruit loads break poorly "
            "structured limbs, so well-spaced, wide-angled scaffolds are worth more here than on a "
            "tougher-wooded species."
        ),
        "full_harvest_notes_beginner": (
            "From about the fifth year the tree carries a full crop, and it is an unusually relaxed "
            "harvest. Persimmon blooms late, in May or June, so it escapes the spring frosts that ruin "
            "earlier fruit, and the fruit then hangs on the tree well into cool fall weather, so there is "
            "no rush to strip it. Harvest by type: pick Fuyu and other non-astringent kinds firm for "
            "crisp eating, and pick Hachiya and American types at full deep orange, then let them ripen "
            "indoors until they are jelly-soft before you eat them. Clip or twist each fruit off with its "
            "leafy cap on. Prune far more lightly than you would a peach, and shorten any long, heavy "
            "limbs so they do not break under a load of fruit."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year five. Two characteristics make this the least time- "
            "pressured harvest on the roster: late bloom in May to June, which largely evades the spring "
            "frost events that cost earlier-blooming fruit their crop, and prolonged on-tree holding into "
            "cool fall weather. Harvest remains type-scoped: non-astringent cultivars firm for crisp "
            "consumption, astringent cultivars at full color followed by ripening to jelly-soft before "
            "eating. Detach with the calyx attached. Dormant pruning is far lighter than stone fruit, "
            "limited to dead and crossing wood and thinning for light, with no hard renewal cuts; shorten "
            "long, heavy limbs specifically to reduce breakage, since persimmon wood is brittle, and make "
            "clean cuts to limit the wounds that admit borers and canker."
        ),
    },
    "pomegranate": {
        "first_harvest_notes_beginner": (
            "Your first pomegranates usually arrive in the second year. One thing outweighs everything "
            "else from now on: keep the soil moisture EVEN from the moment fruit sets until you pick. A "
            "dry spell followed by heavy watering or rain is what splits pomegranates open, and splitting "
            "is the single most common way this crop fails. Steady water is the whole answer. Start "
            "watching for leaf-footed bug from fruit set too. Its feeding leaves no mark you can see on "
            "the outside, but it darkens and shrivels the seeds inside and opens the fruit to rot, so the "
            "damage is invisible until you cut one open."
        ),
        "first_harvest_notes_seasoned": (
            "Bearing typically begins in year two. Moisture consistency from fruit set through harvest is "
            "the dominant variable and outranks every other input: rind splitting, the crop's most common "
            "failure, is driven by a dry interval followed by heavy irrigation or rain, so the correction "
            "is scheduling rather than volume. Scout for leaf-footed bug from set onward. Its feeding "
            "produces no external symptom while darkening and withering the arils and opening the fruit "
            "to internal rot, so infestation is undetectable without cutting fruit. Prune to shape and "
            "open the plant rather than heading it back: pomegranate bears on spurs on older wood as well "
            "as on shoot tips, so hard heading removes bearing surface directly."
        ),
        "full_harvest_notes_beginner": (
            "From about the third year the plant carries a full crop. Ripeness has several signs worth "
            "learning together: the skin reaches its full color (deep red for 'Wonderful'), it shifts "
            "from shiny to slightly dull, the round fruit flattens into more of a six-sided shape as the "
            "seeds swell and press outward, it feels heavy for its size, and it makes a light metallic, "
            "tinny sound when you tap it. Pomegranates do not sweeten after picking, so wait for full "
            "color, but do not leave them hanging into the fall rains, because wet fruit splits. Cut each "
            "one off with clippers, leaving a short stem, rather than pulling and tearing the skin. Whole "
            "fruit then keeps for weeks to months, and unlike a peach it is not harmed by cold, so "
            "refrigerate freely."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year three. Maturity is indexed on a cluster of signals rather "
            "than one: full varietal rind color, a shift from glossy to slightly matte, the flattening of "
            "the round profile to a faintly hexagonal, ridged shape as arils swell, weight for size, and "
            "a metallic, tinny note when tapped. The crop is non-climacteric, so harvest at full color, "
            "but bias EARLY rather than late, because fruit held into the fall rains splits. Cut with a "
            "short stem attached rather than pulling, which tears the rind and creates a rot entry. "
            "Storage is a genuine advantage here: whole fruit holds for weeks to months and pomegranate "
            "is not chilling-sensitive, unlike most subtropical fruit, so refrigeration is unrestricted. "
            "Dormant pruning stays light and spur-preserving, thinning for light and air and clearing "
            "basal suckers."
        ),
    },
}

EDITS = {}   # wave 4 authors new fields only.


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
    print('WAVE 4 (final) -- %d crops:' % len(TRIO))
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
