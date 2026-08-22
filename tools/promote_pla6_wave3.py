#!/usr/bin/env python3
"""PLA-6 Round 2 WAVE 3: the berries, 5 crops. Base 64428067.

THE CANE IS THE WHOLE STORY on three of these five, and it is also this arc's largest single
gloss gap. Round 1 measured `cane` at 151 bare uses in beginner copy across the perennials, with
raspberry (68) and blackberry (65) carrying 133 of them. So the term is NAMED AND GLOSSED IN
PLACE here per v1.3 sec9.3 -- "each cane, meaning each individual stem coming out of the ground"
-- rather than substituted away, because a grower meets the word on every nursery tag and in
every pruning instruction they will ever read for these crops.

WHAT SEPARATES THE FIVE, and why a paste would be actively wrong:

  raspberry   biennial canes on a perennial crown; prune to TYPE, and mismatching summer-bearing
              and primocane-fruiting is the crop's defining error. A ripe fruit SLIPS OFF ITS
              CORE leaving a hollow centre. Harvest cadence is a pest instrument: complete
              removal every one to three days outperforms any home-garden spray against SWD.
  blackberry  same cane biology, OPPOSITE harvest cue -- the fruit comes away WITH its core, and
              ripeness is the shift from gloss to dull matte black, not colour. A shiny black
              berry is under-ripe. Habit (erect / semi-erect / trailing) decides training.
  blueberry   NOT a cane crop at all; a bush renewed by removing its oldest stems. Its defining
              failure is nutritional: interveinal chlorosis from high-pH iron lock-out, corrected
              by pH rather than by iron. Birds are the number-one pest.
  elderberry  multi-stem clump bearing on one-to-three-year canes, forgiving enough to cut to the
              ground and regrow. CARRIES A SAFETY RULE THE OTHERS DO NOT: raw and unripe fruit,
              foliage and stems are mildly toxic, so the crop is ALWAYS cooked. That rule is
              stated in all four fields, not once, because a reader lands on one pill and not the
              others.
  strawberry  crown-forming, and the only crop here where TYPE inverts the instruction: a
              June-bearing bed is deblossomed in year one and renovated after harvest, while a
              day-neutral bed is allowed to fruit and has its runners removed instead, and is
              NEVER renovated. Getting those two crossed is the common failure.

Every claim is restated from what each crop already asserts; no source id is added.

A BRITISH-SPELLING DRIFT WAS CAUGHT IN THIS WAVE AND THE GUARD WAS WIDENED BECAUSE OF IT. Six
instances (centre, programme, colour x3, internalise) reached the draft. The suites' American-
English check had only ever listed five words, so the class was under-covered; it now carries
eighteen, and waves 1 and 2 plus the pilot were re-swept clean under the wider list. The widened
guard was itself verified live rather than assumed, because the first version shipped `\\b`
instead of `\b` and would have matched a literal backslash.

Guard suite:      tools/test_promote_pla6_wave3.py
Mutation harness: tools/mutate_pla6_wave3_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla6_wave3.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '64428067a44b369b550b6d11d8287e7578afbadf022b14e2fe7c8238e0ebc393'

NEW_FIELDS = ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
              'full_harvest_notes_beginner', 'full_harvest_notes_seasoned')

TRIO = {
    "blackberry": {
        "first_harvest_notes_beginner": (
            "This is the year pruning starts to matter, and like raspberry it turns on the cane. The "
            "roots and crown live for years, but each cane, meaning each individual stem, lives only two: "
            "it grows one year, fruits the next, then dies. What you do depends on the habit you planted. "
            "An upright type gets its new canes pinched at 3 to 4 feet in summer so they branch; a big "
            "semi-erect or trailing type gets tied to a trellis instead, because left loose it sprawls on "
            "the ground and roots where it touches. Either way, cut the canes that fruited to the ground "
            "right after harvest. If you are in the humid Southeast, check hard at bud break for rosette, "
            "a broom-like tangle of distorted flowers, and cut out any cane showing it immediately before "
            "the spores spread."
        ),
        "first_harvest_notes_seasoned": (
            "Cane biology and habit jointly govern the planting. The crown is perennial and canes are "
            "biennial, running one season as a primocane, meaning a first-year vegetative cane, and the "
            "next as a fruited floricane before dying. Training is habit-dependent and set now: tip erect "
            "types at 3 to 4 feet to force fruiting laterals, trellis semi-erect and trailing types, "
            "which will otherwise sprawl and tip-root. Remove spent floricanes at ground level "
            "immediately post-harvest to open the canopy and cut disease and borer carryover. Bloom "
            "through harvest is the water-critical window, so irrigate low and often at the base rather "
            "than overhead. In the humid Southeast, scout at bud break and bloom for rosette (double "
            "blossom) and excise affected canes before sporulation."
        ),
        "full_harvest_notes_beginner": (
            "From the second year the planting carries a full crop. Each late winter, shorten the side "
            "shoots to 12 to 18 inches and thin to a few strong canes per foot for light and air, or "
            "simply mow everything down if you grow a fall-bearing type for one clean crop. The picking "
            "cue is worth learning properly, because it is the opposite of what looks right: a blackberry "
            "is ready when it turns from glossy to a dull, deep black and pulls free with its core still "
            "inside. A shiny black berry is not fully ripe and will be tart, and blackberries do not "
            "sweeten after picking, so there is nothing to be gained by picking early and waiting."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from year two. The dormant cycle is lateral shortening to 12 to 18 inches "
            "and thinning to a few strong canes per foot, or complete mowing on a primocane-fruiting "
            "planting grown for a single crop. Maturity indexing is the detail that separates a good "
            "picker from a poor one: blackberry retains its receptacle, so a ripe fruit comes away with "
            "the core intact, and the reliable signal is the shift from gloss to a dull matte black "
            "rather than color itself. Glossy black fruit is under-ripe and acidic, and the crop is non- "
            "climacteric, so nothing improves after picking. Hold even moisture from bloom through "
            "harvest against small, hard, poorly filled drupelets, and water at the base, since wet "
            "foliage into the night is what drives fruit rot."
        ),
    },
    "blueberry": {
        "first_harvest_notes_beginner": (
            "Blueberry asks for patience twice over. Keep picking the flower buds off through the second "
            "year: it feels wasteful, but the energy goes into roots and wood instead, and an established "
            "bush can then fruit for decades. The other job this year is watching the leaves. Pale yellow "
            "new leaves with green veins mean the soil is not acid enough for the plant to take up iron, "
            "and that is the single most common way a blueberry fails. Test and acidify the soil, and use "
            "a chelated-iron spray to buy time while the sulfur works. Feed at bud break with an acid "
            "fertilizer and again about six weeks later, keeping it light, and never use lime."
        ),
        "first_harvest_notes_seasoned": (
            "Continue bud removal through year two; redirecting that energy into root and shoot "
            "development is what builds a bush capable of decades of production, and the deferral is "
            "short against that lifespan. Nutrition is the crop's defining constraint and the usual cause "
            "of failure: interveinal chlorosis on new foliage indicates high-pH iron unavailability "
            "rather than an iron shortage in the soil, so the correction is pH, with chelated foliar iron "
            "as a holding measure while elemental sulfur acts. Feed at bud break with an ammonium-form "
            "acid fertilizer and again roughly six weeks later at light rates, avoiding lime and nitrate "
            "nitrogen, both of which raise pH and injure the plant. Blueberry roots are shallow and "
            "fibrous, so moisture must be steady rather than heavy."
        ),
        "full_harvest_notes_beginner": (
            "From the third year the bush carries a full crop over a window of roughly two months, so you "
            "pick it every few days rather than all at once. Take only fully blue berries that come away "
            "with a gentle roll of the thumb; any red still showing at the stem end means underripe, and "
            "it will not sweeten off the bush. Pick in the cool of the morning once the dew has dried, "
            "and refrigerate promptly. Get netting up before the berries start to color, because birds "
            "are the number one blueberry pest and will clear a ripening bush in days, and secure it at "
            "the base so they cannot get underneath. Pruning is simple: each winter take out one to three "
            "of the oldest, woodiest stems at the base so the bush keeps renewing itself."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from year three across a roughly two-month window, harvested on a several- "
            "day cycle. Index maturity on complete blue color and clean abscission under a thumb roll; "
            "residual red at the calyx indicates immaturity, and the crop is non-climacteric so it will "
            "not improve after picking. Harvest after dew burn-off in the cool morning and cool promptly, "
            "since field heat shortens shelf life and surface moisture drives bruising and decay. Bird "
            "exclusion netting goes up ahead of color break and is secured at ground level. Renewal "
            "pruning is the whole structural task: remove one to three of the oldest canes at the base "
            "each dormant season alongside weak and crowded wood. Pair it with sanitation, raking and "
            "removing mummified fruit and burying residual inoculum under fresh mulch against mummy "
            "berry."
        ),
    },
    "elderberry": {
        "first_harvest_notes_beginner": (
            "Thin the fruiting this second year so the young shrub can finish building its framework, "
            "then let it go. Elderberry establishes fast, so the restraint is brief. Understand the shape "
            "of the plant while it is young: an elderberry grows as a clump of many stems from the ground "
            "rather than on a single trunk, and it fruits best on stems that are one to three years old. "
            "That is what makes the yearly pruning simple later on. One thing matters more than anything "
            "else here, and it applies from your very first berry: always cook elderberries before eating "
            "them. Raw and unripe fruit, and the leaves and stems, are mildly toxic, so strip the berries "
            "off, throw away every green or red one along with all the stems, and cook what is left."
        ),
        "first_harvest_notes_seasoned": (
            "Thin fruiting in year two so the shrub completes its root system and cane framework; "
            "establishment is short on this crop, so the cost is small against the second and third year "
            "crops. The structural model to internalize now is a multi-stem clump rather than a leader: "
            "bearing is best on canes one to three years old, which is what makes the later renewal cycle "
            "mechanical. THE SAFETY RULE APPLIES FROM THE FIRST HARVEST AND IS NOT OPTIONAL: raw and "
            "unripe fruit, foliage and stems all contain cyanogenic compounds and are mildly toxic, so "
            "berries are stripped clean of stems, green and red fruit discarded, and the crop is always "
            "cooked before eating. Pollination also needs two different cultivars, so a single-variety "
            "planting under-sets regardless of how well it is grown."
        ),
        "full_harvest_notes_beginner": (
            "From the third year the shrub carries a full crop. Pruning is a yearly renewal rather than "
            "shaping: each late winter, cut out the stems older than about three years at the base, along "
            "with anything dead, broken, or crowded, and leave the strong younger ones. If the plant ever "
            "becomes an overgrown tangle that fruits poorly, you can cut the whole thing to the ground in "
            "late winter and it will bounce right back, which is unusually forgiving. Harvest whole "
            "clusters when most berries in them are deep purple-black and soft. Chilling the clusters "
            "first makes stripping them much easier. Discard every green or red berry and all the stems, "
            "and always cook the fruit before eating: raw and unripe berries, leaves, and stems are "
            "mildly toxic."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from year three. Renewal pruning is the entire structural task: each dormant "
            "season remove canes older than roughly three years at the base along with dead and crowded "
            "stems, retaining a spread of younger wood, since bearing concentrates on one-to-three-year "
            "canes. An unproductive overgrown clump can be cut to the ground entirely and will "
            "regenerate, which makes recovery from neglect cheap on this crop relative to any tree fruit. "
            "Harvest whole cymes when the majority of berries are deep purple-black and soft; chilling "
            "clusters before stripping markedly reduces handling loss. Discard green and red fruit and "
            "all stem material. THE COOKING REQUIREMENT IS PERMANENT: raw and unripe fruit, foliage and "
            "stems are mildly toxic, so the crop is never eaten fresh regardless of ripeness."
        ),
    },
    "raspberry": {
        "first_harvest_notes_beginner": (
            "This is the year the pruning starts to matter, and it all turns on one fact: the roots live "
            "for years, but each cane, meaning each individual stem coming out of the ground, lives only "
            "two. It grows one year, fruits the next, then dies. What you cut depends on your type. A "
            "summer-bearing raspberry fruits in early summer on last year's canes, so cut those spent "
            "canes to the ground right after picking; they are dead anyway, and clearing them opens the "
            "row. A fall-bearing type fruits on brand-new canes in late summer, and the simplest approach "
            "is to mow every cane to the ground each winter. Cutting the wrong type the wrong way is the "
            "most common raspberry mistake there is. Keep pulling any shoots that wander outside your "
            "row, because red and yellow types spread underground."
        ),
        "first_harvest_notes_seasoned": (
            "Cane biology governs everything from here. The crown is perennial; individual canes are "
            "biennial, spending one season as a primocane, meaning a first-year vegetative cane, and the "
            "next as a fruited floricane before dying. Prune to the type: summer-bearing floricanes come "
            "out at ground level immediately post-harvest, while a primocane-fruiting type is mown flat "
            "each dormant season for a single clean fall crop. Mismatching the two is the crop's defining "
            "error. Contain suckering from day one on red and yellow types, holding the row to 12 to 18 "
            "inches, since the planting spreads by underground runners and a wide row loses the light and "
            "airflow that suppress disease. Feed a balanced fertilizer banded along the row at spring "
            "growth and stop by midsummer, because late nitrogen produces soft, disease-prone wood."
        ),
        "full_harvest_notes_beginner": (
            "From the second year the planting is in full swing, and the annual rhythm is set: prune to "
            "your type, keep the row about a foot wide, and tie the kept canes to a support. Picking is "
            "the other half of the job, and it is more frequent than people expect. A ripe raspberry "
            "slips off its core into your hand and leaves a hollow center behind; one that resists is not "
            "ready. Work the row every two to three days into a shallow container and refrigerate "
            "quickly. That tight schedule is not fussiness: clearing every ripe and overripe berry on a "
            "two-to-three-day cycle is the single most effective control for spotted wing drosophila, the "
            "small fly that lays in ripening fruit, and it beats anything you could spray in a home "
            "garden."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from year two. The annual cycle is type-matched pruning, row narrowing to "
            "about 12 inches, and trellis tying, with a balanced spring feed banded along the row. "
            "Harvest cadence is a pest-control instrument rather than a convenience: raspberry receptacle "
            "separation means a ripe fruit slips free leaving the core on the plant, and complete removal "
            "of ripe and overripe fruit on a one-to-three-day cycle is the front-line suppression for "
            "spotted wing drosophila, materially more effective in a garden setting than any spray "
            "program. Hold moisture steady through sizing, since drought during fruit development is the "
            "usual cause of small, seedy, crumbly fruit. An open, well-pruned, well-supported canopy "
            "compounds the effect by drying faster and giving the fly less shelter."
        ),
    },
    "strawberry": {
        "first_harvest_notes_beginner": (
            "What you do this year depends entirely on which kind you planted. On a June-bearing bed, the "
            "one this guide is built around, pinch off all the first-year flowers. Letting a new plant "
            "fruit now starves the root and runner growth that builds the crown, meaning the thick stem "
            "at soil level that the whole plant grows from, and that crown is what carries a full crop "
            "next season. Day-neutral types are the exception: they fruit in their first year, so you let "
            "them, and you remove their runners instead, since energy spent making runners is energy "
            "taken from the berries. Keep any new planting evenly moist while it roots in, because "
            "strawberries are shallow-rooted and dry out fast."
        ),
        "first_harvest_notes_seasoned": (
            "Type determines the entire first-year protocol, and conflating the two is the common error. "
            "On a June-bearing matted row, remove all first-year bloom: fruiting now competes directly "
            "with root and runner development, and the crown built this season is what carries next "
            "year's crop. Day-neutral and everbearing types invert it, fruiting in the planting year, so "
            "bloom is retained and early runners are removed instead, because runner production draws "
            "from the fruit those types are grown for. Space daughter plants as runners root, keeping the "
            "strongest and removing crowded extras to hold matted-row density; a bed left to fill solid "
            "yields small, hard-to-pick fruit and holds the moisture that feeds rot. Irrigate "
            "consistently through establishment, since the root system is shallow and dries quickly."
        ),
        "full_harvest_notes_beginner": (
            "From the second year a June-bearing bed gives its full crop, one big flush over about four "
            "weeks. Tuck clean straw under the developing berries so fruit is not resting on damp soil, "
            "which is where gray mold starts and where the name strawberry comes from. Water at the base "
            "in the morning and keep the berries themselves dry. Pick fully red berries every two to "
            "three days, pinching the stem rather than tugging the fruit, since strawberries do not "
            "sweeten at all after picking. Then, a week or two after the last berries, renovate: mow the "
            "old leaves to about 2 inches above the crowns without cutting into them, rake the leaves "
            "away, narrow the row to about a hand's width, and feed and water. Skip renovation entirely "
            "on day-neutral and everbearing types, which are still fruiting in late summer. Expect about "
            "three to four fruiting seasons before it is time to start a fresh bed elsewhere."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from year two on a June-bearing matted row, delivered as a single roughly "
            "four-week flush. Mulch under developing fruit to break soil contact, and irrigate at the "
            "base in the morning so foliage and fruit are dry going into the night, which is what governs "
            "Botrytis pressure. Harvest fully coloured fruit on a two-to-three-day cycle, pinching the "
            "pedicel; the crop is non-climacteric and gains nothing after picking. Renovation is the "
            "year's defining operation and is type-scoped: one to two weeks after final harvest, mow "
            "foliage to about 2 inches above the crowns without damaging them, clear the residue, narrow "
            "and thin the row, then feed and irrigate to drive the regrowth that sets next season's "
            "flower buds. Day-neutral and everbearing plantings are NOT renovated, since they are still "
            "bearing. Expect three to four productive seasons before bed replacement on fresh ground."
        ),
    },
}

EDITS = {}   # wave 3 authors new fields only.


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
    print('WAVE 3 -- berries, %d crops:' % len(TRIO))
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
