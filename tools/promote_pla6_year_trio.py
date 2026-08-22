#!/usr/bin/env python3
"""PLA-6 Round 2, the year-pill trio PILOT: 4 crops + 2 rendered-field repairs. Base fe26f783.

WHAT THIS IS. plant-app renders three establishment pills on every perennial guide --
Establishing / First harvests / Full harvest -- and until PLA-362 it composed their captions
from prose authored for other purposes, pointing TWO pills at ONE string. Measured on this
base: Establishing and First harvests were byte-identical on 36 of 38 perennials, and 22 of
the 26 pill-rendering crops put text explicitly scoped to YEAR ONE into the First-harvests
pill. Apple's First-harvests state covers bed years 2, 3 and 4 and said only "Pinch off all
the flowers the first spring", under a ribbon reading LIGHT HARVEST.

PLA-362 (plant-app) rewired each pill to its own field. This promote authors the first of
that content. Contract: docs/2026-08-22-perennial-year-pill-trio-contract.md, field-addition
register row 28, ruled by Trevor 2026-08-22.

    Establishing    -> year_one_notes_{level}          (already existed on 26 crops)
    First harvests  -> first_harvest_notes_{level}     NEW, authored here
    Full harvest    -> full_harvest_notes_{level}      NEW, authored here

THE PILOT SET IS DIVERSE BY DESIGN, per the column-GS-arc method's requirement that a pilot
include a legitimately-N/A case:

  apple      the deblossom class, and the longest First-harvests span (bed years 2 to 4)
  pawpaw     the longest establishment on the roster (first harvests 4 to 6, full at 7)
  asparagus  herbaceous, and the only crop with a real `harvest_ramp_weeks`; its year-2
             over-cut is the classic way a home planting is lost, so the beginner register
             has to carry the ACTION and not only the caution
  sage       THE N/A CASE, and it is carried by ABSENCE rather than by null.

             The contract first specified `null` on N/A crops, so that a presence floor could
             gate the field and no backfill treadmill could open. THE GAUNTLET OVERRULED THAT,
             and correctly: A29 register-fill requires every `_beginner`/`_seasoned` field that
             EXISTS to be authored and non-null -- the rule that exists because apple once
             shipped 30 null register fields and peach 46. Four explicit nulls on sage bounced
             it, and A29 is a long-standing roster rule while "present-or-null" was a fresh
             invention of this contract. So the contract changed, not the gate.

             sage is therefore a deliberate NON-TARGET: it takes none of the four fields, and
             the guard suite asserts that by name so the omission is a recorded decision rather
             than a crop someone forgot. Its EXISTING year_one_notes_* are real authored prose
             and are untouched. The presence floor survives intact, keyed on the crops that
             actually render pills: perennial_year_gate's TRIO family will require non-null
             wherever renders_pills() is true, which needs no nulls anywhere else.

EVERY CLAIM IS RESTATED FROM WHAT THE CROP ALREADY ASSERTS. Nothing here is newly researched:
apple's one-fruit-per-cluster thinning and petal-fall timing come from its own
`tips_by_stage.fruit_set`, asparagus's week-by-bed-year ramp from its own `harvest_ramp_weeks`
and the pencil-diameter stop from its own `harvest_stop_rule`, pawpaw's hand-pollination from
its own `tips_by_stage.blossom`. The fields are prose siblings of `year_one_notes_*`, which
carries no per-field `sources` key, so none is added here.

TWO REPAIRS TO EXISTING RENDERED FIELDS, and they are the reason this promote is 5 crops and
not 4. Trevor, reviewing the pawpaw draft: "You don't want them putting one in the front yard
and one in the back and thinking they're good at 100 plus feet." Chasing that found a live
defect wider than the field being drafted. `TreePollinationCard` renders the CROP-LEVEL
`pollinator_notes_{level}`; pawpaw and cherry-sweet keep their pollinizer distance only in the
NESTED `pollination.notes_beginner`, which no consumer reads. So:

  pawpaw        rendered copy said "plant at least two different trees ... close together",
                while the 30 feet sat in the unread field. "Close together" is precisely the
                phrase that produces the front-yard/back-yard failure.
  cherry-sweet  rendered copy gave no distance at all; the 100 feet sat in the unread field.
                A grower plants Bing plus a compatible partner too far apart and gets nothing.

Both are one sentence, both are the same class, and holding cherry-sweet for a later wave to
keep the pilot at exactly four crops would have left a known no-fruit defect live.

pawpaw's `year_one_notes_beginner` gains the same figure, because the siting decision is made
in year one and the Establishing pill is where a first-year owner reads it. The rule this
generalises to, for the remaining 22 crops: A FIGURE THAT DETERMINES WHETHER THE CROP PRODUCES
AT ALL IS LOAD-BEARING AND BELONGS IN THE FIELD THAT RENDERS, not only in the more precise one.

STANDARD APPLIED: language_and_copy_architecture v1.1 + v1.2 + v1.3. Checked against the
drafts, not assumed: 0 mechanics violations (no em-dash, en-dash or double-hyphen, American
English); beginner/seasoned similarity 0.015 to 0.085 against v1.3 sec9.1; one v1.3 sec9.2
divergence found and fixed before staging (asparagus cadence, see the suite's QUANTITY guard).

A sec9.2 FINDING ON CERTIFIED ASPARAGUS, recorded and NOT fixed here: `tips_by_stage
.spear_emergence` and `harvest_ready_*` say "every day or two" (beginner) against "every one to
three days" (seasoned) -- a different upper bound in both field families. The new fields agree
with each other rather than inheriting it. Fixing certified prose belongs in asparagus's own
checklist pass, not in a pilot promote.

Guard suite:      tools/test_promote_pla6_year_trio.py
Mutation harness: tools/mutate_pla6_year_trio_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla6_year_trio.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = 'fe26f7833cb9c932fa621c20fb6ebc08af2eb5e66866089e21d847fa4970f57c'

# The four new fields, in a fixed order so output and guards agree.
NEW_FIELDS = ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
              'full_harvest_notes_beginner', 'full_harvest_notes_seasoned')

# Crops whose pills plant-app actually renders (a well-formed years_to_first_harvest).
# Every TRIO crop must be one of these; an N/A crop takes the fields by ABSENCE (see sage).
PILL_CROPS = ('apple', 'pawpaw', 'asparagus')

TRIO = {
    "apple": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first apples now, and the crop will be small and uneven for a few "
            "years. That is normal. About a month after bloom, thin the little apples to one per cluster "
            "by pinching off the extras. It feels wasteful, but it gives you bigger fruit and it stops "
            "the tree falling into biennial bearing, the habit of cropping heavily one year and barely at "
            "all the next. Keep shaping the framework each winter while the wood is still young and easy "
            "to bend. And now that there is fruit worth protecting, the days just after the petals drop "
            "are your window to deal with codling moth and plum curculio, the two grubs that tunnel into "
            "apples."
        ),
        "first_harvest_notes_seasoned": (
            "Expect a light, irregular crop while the tree finishes its framework. Thin to one fruit per "
            "cluster within about a month of bloom: hand thinning at that stage both sizes the remaining "
            "fruit and relieves the return-bloom suppression that drives biennial bearing, and thinning "
            "later buys far less of either. Keep selecting and training scaffolds through each dormant "
            "season, because a limb that starts carrying fruit sets its crotch angle for good. Petal fall "
            "is the timing anchor for codling moth and plum curculio now that there is fruit on the tree, "
            "and a first crop on a dwarfing rootstock is heavy enough that the stake earns its keep "
            "another season."
        ),
        "full_harvest_notes_beginner": (
            "From about the fifth year your tree carries a full crop, and the job changes from building "
            "it to keeping it steady. Prune every winter before the buds open, thin the young apples to "
            "one per cluster each spring, and pick by taste and feel rather than by the calendar: a ripe "
            "apple comes away with a gentle upward twist, and if you have to tug hard it needs longer. In "
            "autumn, rake up the fallen leaves and pick up every dropped apple, which breaks the cycle "
            "for apple scab, codling moth and apple maggot. Good keepers such as Fuji, Granny Smith and "
            "Pink Lady will hold for months somewhere cold and humid."
        ),
        "full_harvest_notes_seasoned": (
            "A mature tree is a maintenance system rather than a project: annual dormant pruning to keep "
            "light in the canopy, annual thinning to one fruit per cluster to hold return bloom and keep "
            "the tree out of biennial bearing, and sanitation each fall. Harvest on ground color, seed "
            "color and detachment rather than on a date, since starch converts to sugar late and picking "
            "a week early costs the flavor the variety is grown for. Clearing fallen leaves and dropped "
            "fruit breaks apple scab, codling moth and apple maggot in one pass. Expect full production "
            "from roughly year five on a dwarfing rootstock and later on a standard."
        ),
    },
    "pawpaw": {
        "first_harvest_notes_beginner": (
            "Your first pawpaws usually arrive about four years after planting a grafted tree, and later, "
            "often five to eight years, if yours was grown from seed. The shade you gave it early is no "
            "longer wanted: once it is established, a pawpaw fruits best in full sun. Whether you get "
            "fruit at all now comes down to pollination. Pawpaw flowers are pollinated by flies and "
            "beetles rather than bees, and they set poorly on their own, so take a small brush and move "
            "pollen from the just-opened flowers of one tree to the sticky centers of the flowers on a "
            "different tree, several times through bloom. If your two trees are more than about 30 feet "
            "apart, that distance alone can be why a healthy, flowering pawpaw sets almost nothing. If a "
            "young tree sets heavily, pull off a few clusters so the branches are not overloaded; most "
            "set lightly enough that you can leave them alone."
        ),
        "first_harvest_notes_seasoned": (
            "Grafted trees generally begin bearing around year four; seedlings run five to eight. Lift "
            "the establishment shade now, since a rooted pawpaw fruits best in full sun. Set is the "
            "limiting factor and is worth treating as a scheduled task rather than a hope: pawpaw is "
            "self-incompatible, so a lone tree, or a cultivar and its own root suckers, will not crop, "
            "and it is fly- and beetle-pollinated with unreliable natural set. Brush fresh pollen from "
            "just-opened flowers onto the ripe, sticky stigmas of a genetically distinct tree within "
            "about 30 feet, repeating across the bloom period. Thinning is optional and far lighter than "
            "for peach: only a heavily set young tree needs clusters removed so the large fruit sizes "
            "properly and limbs are not overloaded."
        ),
        "full_harvest_notes_beginner": (
            "A settled pawpaw carries a full crop from about its seventh year, and it asks very little of "
            "you: it grows itself into a neat pyramid with one main stem, so cut out only dead, broken or "
            "crossing branches. Keep hand-pollinating every spring, because set stays unreliable without "
            "it. The picking window is short and the fruit is fragile, so check the tree daily. Pick each "
            "fruit as it just begins to soften and give to a gentle squeeze, then let it finish indoors "
            "over a few days. Brown or black speckles on the skin are normal ripening, not rot. Ripe "
            "fruit keeps only a few days, so scoop out and freeze the pulp of anything you cannot eat "
            "straight away."
        ),
        "full_harvest_notes_seasoned": (
            "Expect full production from around year seven. Maintenance stays minimal: pawpaw trains "
            "itself to a pyramidal central leader, so limit pruning to dead, broken and crossing wood, "
            "and remove root suckers unless you want a spreading clonal patch, since a single-genotype "
            "thicket fruits poorly. Hand pollination remains an annual job, not an establishment measure. "
            "Ripening runs from roughly August in the South to October in the North across a short "
            "window, and tree-ripe fruit is fragile and quickly taken by wildlife, so pick over the tree "
            "in several passes as fruit begins to soften and finish it indoors. Refrigerate ripe fruit "
            "only briefly, and scoop and freeze pulp for anything beyond a few days."
        ),
    },
    "asparagus": {
        "first_harvest_notes_beginner": (
            "This is the year you may take your first small cut, and it is also the year the bed is "
            "easiest to ruin. Take at most two weeks of spears, and only if the planting came through its "
            "first season looking strong. If it looks thin or weak, take nothing and wait another year. "
            "Cut spears at about 6 to 8 inches while the tips are still tight and closed, then stop, even "
            "if more are coming, and let everything else grow into tall ferns for the rest of the summer. "
            "Cutting a young bed too hard, too soon, can permanently weaken the crown, the underground "
            "bud and root cluster the whole planting grows back from each spring."
        ),
        "first_harvest_notes_seasoned": (
            "Year two is a token pick, taken on the bed's condition rather than by right: up to two "
            "weeks, and only if the planting came through its first season vigorous. The extension "
            "literature genuinely splits here, with some guidance waiting for year three altogether, so "
            "on a thin stand the conservative call is the correct one. Cut at 6 to 8 inches with the "
            "bracts still closed, then release the bed and let the fern stand all season. The reason the "
            "ceiling sits this low is reserve accounting: the crown has had a single season to bank "
            "carbohydrate, and a season cut to its own natural end at this age draws down more than one "
            "summer of fern can replace, which is how a home planting ends up permanently spindly."
        ),
        "full_harvest_notes_beginner": (
            "From the third year the bed is genuinely producing, but the season keeps growing along with "
            "it: about two to four weeks in year three, six to eight in year four, and six to ten weeks "
            "from year five onward, which is as long as it will ever get. Cut spears at 6 to 8 inches "
            "with tight tips, and check the bed every day or two, or daily once the weather warms, "
            "because spears shoot up and open into ferns fast. Let the spears end the season rather than "
            "the calendar: when the new ones coming up turn thin, about pencil width, the crown is "
            "running low on stored food, so stop cutting and let the rest fern out. Those ferns feed next "
            "spring's crop, so leave them standing until frost browns them."
        ),
        "full_harvest_notes_seasoned": (
            "The bed bears from year three, but the mature ceiling is not reached until year five: "
            "roughly two to four weeks at year three, six to eight at year four, and six to ten from year "
            "five on. Cut at 6 to 8 inches with the bracts still closed, working the bed every day or two "
            "and daily in warm weather, since elongation is fast once temperatures climb. Close the "
            "season on spear caliper rather than on elapsed days: when the majority of emerging spears "
            "fall to about pencil diameter, between a quarter and a half inch depending on which "
            "extension standard you follow, the crown's reserves are drawn down and further cutting is "
            "taken from next spring's yield. Release the bed at that threshold, then feed it, keep the "
            "fern watered and clear of asparagus beetles and rust, and leave the canopy standing until "
            "frost."
        ),
    },
}

# (crop, field) -> (find, replace) on an EXISTING field. Each find-string was verified
# present in the base before this promote was written; the suite re-proves it.
EDITS = {
    ("pawpaw", "year_one_notes_beginner"): (
        "Plant at least two different trees so they can pollinate each other once they start "
        "fruiting.",
        "Plant at least two different trees, within about 30 feet of each other, so they can "
        "pollinate each other once they start fruiting. Two pawpaws at opposite ends of a yard are "
        "too far apart to work.",
    ),
    ("pawpaw", "pollinator_notes_beginner"): (
        "so you must plant at least two different trees (two different named varieties, or two or "
        "more seedlings) close together.",
        "so you must plant at least two different trees (two different named varieties, or two or "
        "more seedlings) within about 30 feet of each other. Two pawpaws at opposite ends of a yard "
        "are too far apart to pollinate each other.",
    ),
    ("cherry-sweet", "pollinator_notes_beginner"): (
        "The second tree has to be a different, compatible variety that blooms at the same time "
        "(watch out: Bing, Lambert, and Royal Ann cannot pollinate each other).",
        "The second tree has to be a different, compatible variety that blooms at the same time, "
        "planted within about 100 feet so bees can carry pollen between them (watch out: Bing, "
        "Lambert, and Royal Ann cannot pollinate each other).",
    ),
}


def renders_pills(crop):
    """plant-app's own gate, reproduced: the pill row is hidden without a well-formed range,
    and establishmentState() fails OPEN to 'full' on anything malformed."""
    y = crop.get('years_to_first_harvest')
    return (isinstance(y, list) and len(y) >= 2
            and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in y[:2]))


def apply_to(data):
    """The whole transform as one function, so the guard suite exercises the code the promote
    runs rather than a re-implementation of it."""
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

    # ---- preconditions. Each ABORTS rather than proceeding on a surprise. ----
    for slug in list(TRIO) + [s for s, _ in EDITS]:
        if slug not in by:
            print('ABORT: no crop %r' % slug, file=sys.stderr)
            return 1

    # These fields are CREATED here. If one already exists the base is not what this was
    # written against, and a silent overwrite would destroy authored prose.
    for slug, fields in TRIO.items():
        for field in fields:
            if field in by[slug]:
                print('ABORT: %s.%s already exists; this promote creates it' % (slug, field),
                      file=sys.stderr)
                return 1

    # Every authored crop must actually render pills, re-derived from the data rather than
    # trusted from authoring. A crop that renders none takes the fields by ABSENCE, because
    # A29 register-fill forbids a null _beginner/_seasoned field that exists.
    for slug in TRIO:
        if not renders_pills(by[slug]):
            print('ABORT: %s renders no pills; an N/A crop takes the trio by ABSENCE, not null'
                  % slug, file=sys.stderr)
            return 1
        for field, value in TRIO[slug].items():
            if not value:
                print('ABORT: %s renders pills but %s is empty' % (slug, field), file=sys.stderr)
                return 1

    # Every edit must be REACHABLE, and reachable exactly once, or the replace is a silent no-op
    # or a double edit.
    for (slug, field), (find, _replace) in EDITS.items():
        current = by[slug].get(field)
        if not isinstance(current, str):
            print('ABORT: %s.%s is not a string' % (slug, field), file=sys.stderr)
            return 1
        n = current.count(find)
        if n != 1:
            print('ABORT: %s.%s contains its find-string %d times, expected exactly 1'
                  % (slug, field, n), file=sys.stderr)
            return 1

    apply_to(data)

    print('TRIO authored:')
    for slug, fields in TRIO.items():
        nulls = sum(1 for v in fields.values() if v is None)
        chars = sum(len(v) for v in fields.values() if v)
        note = '  (N/A: renders no pills)' if nulls == len(fields) else ''
        print('  %-11s %d fields, %d null, %5d chars%s' % (slug, len(fields), nulls, chars, note))
    print('RENDERED-FIELD repairs:')
    for (slug, field), (find, replace) in EDITS.items():
        print('  %-13s %s  %+d chars' % (slug, field, len(replace) - len(find)))

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
