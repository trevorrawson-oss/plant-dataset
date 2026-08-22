#!/usr/bin/env python3
"""PLA-6 Round 2 WAVE 1: the stone and pome fruit, 8 crops. Base 0cc37afe.

The pilot (`fe26f783` -> `0cc37afe`) proved the shape on apple, pawpaw and asparagus, and
repaired two rendered-field pollinizer distances. This is the first rollout wave.

WAVE COMPOSITION IS BY ARCHETYPE AND BY BEARING HABIT, not alphabetical, because the content
clusters that way and authoring a coherent group at once is what keeps each crop honest about
how it differs from its neighbour:

  one-year-wood bearers   peach, nectarine -- renewal pruning is not optional; miss a winter and
                          the tree hollows out to bare scaffolds with fruit only at the tips
  mixed / spur bearers    apricot, plum, cherry-sweet, cherry-sour -- pruned LIGHTER than peach,
                          because cutting spur wood removes bearing surface rather than renewing it
  the pears               pear-european, pear-asian -- which invert each other at harvest: the
                          European is picked MATURE BUT FIRM and ripened indoors (tree-ripening
                          browns the core), the Asian ripens ON the tree and never finishes indoors

EVERY CLAIM IS RESTATED FROM WHAT THE CROP ALREADY ASSERTS -- thinning distances from each crop's
own `tips_by_stage.fruit_set`, bearing habit and pruning weight from its own `dormant_prune` and
`scaffold_formation`, harvest indicators from its own `harvest` tips. Nothing is newly researched
and no source id is added; these are prose siblings of `year_one_notes_*`, which carries no
per-field `sources` key.

THE FULL-HARVEST YEAR IN EVERY STRING IS `years_to_first_harvest[1]`, not a remembered figure,
and the guard suite re-derives it from the dataset per crop rather than trusting the prose.

A CROSS-CROP TEMPLATE CHECK WAS RUN AND CAUGHT ONE REAL PASTE. peach and nectarine are the same
species group and their first drafts of `full_harvest_notes_beginner` measured 0.837 similar --
close enough that a reader holding both guides would see it. Rewritten to lead with the one thing
that genuinely separates them: a nectarine is a peach without the fuzz, and the fuzz was doing a
job (bare skin bruises, splits in wet weather and admits brown rot faster). 0.837 -> 0.106. The
check is in the guard suite so a later edit cannot quietly re-converge them.

Guard suite:      tools/test_promote_pla6_wave1.py
Mutation harness: tools/mutate_pla6_wave1_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla6_wave1.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '0cc37afe6597d43eac4e867b5eefa625aed5002dfc20628e4a5fbac80215e66b'

NEW_FIELDS = ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
              'full_harvest_notes_beginner', 'full_harvest_notes_seasoned')

TRIO = {
    "apricot": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first apricots now. Thin them to one fruit every 4 to 6 inches about a "
            "month after bloom, closer spacing than a peach gets because apricots are smaller. Thinning "
            "does three things at once here: it sizes the fruit, it keeps a young limb from breaking, and "
            "it heads off apricot's habit of cropping heavily one year and hardly at all the next. Prune "
            "more gently than you would a peach. Apricot fruits on spurs, the short stubby side shoots "
            "that keep bearing for several years, so cutting away too much of that wood costs you crops "
            "rather than renewing them."
        ),
        "first_harvest_notes_seasoned": (
            "Expect a light first set. Thin to one fruit every 4 to 6 inches within about a month of "
            "bloom, tighter than stone fruit of similar habit because apricot fruit is smaller, and treat "
            "the pass as three jobs at once: sizing, limb protection on young scaffold wood, and damping "
            "the alternate-bearing swing apricot is unusually prone to. Prune conservatively from here. "
            "Apricot carries a mixed bearing habit, long-lived spurs plus one-year wood, so it needs "
            "renewal pruning far lighter than peach and over-thinning the spur wood removes bearing "
            "surface rather than refreshing it. In canker-prone wet-spring regions, move major cuts to "
            "dry summer weather, since bacterial canker enters cool, wet-season wounds."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year you get a full crop. Each spring, thin the young fruit to one "
            "every 4 to 6 inches; that pass never becomes optional. Apricot is an early tree in every "
            "sense: it blooms before anything else, which makes a late frost the single biggest threat to "
            "a year's fruit, and it ripens over one to three weeks so you pick in several passes. Ripe "
            "fruit is fully orange-yellow, gives a little, and twists off easily; pick slightly firm if "
            "you plan to dry it. Handle the fruit gently, since bruises let in brown rot and tree-ripe "
            "apricots are fragile. When you are done, clear every remaining and dropped fruit, because "
            "fruit left to shrivel on the tree or ground is what starts brown rot again next spring. "
            "Apricots dry and freeze exceptionally well, which is the usual answer to a tree that ripens "
            "all at once."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year four. The annual cycle is light pruning that preserves "
            "spur wood, thinning to one fruit every 4 to 6 inches, and thorough post-harvest sanitation. "
            "Apricot reaches open bloom earlier than any other stone fruit, so frost, not pests, is the "
            "usual reason for a lost year, and a small tree is worth covering overnight against a hard "
            "late frost. Harvest over one to three weeks in several passes on full orange-yellow ground "
            "color, slight give, and clean release; pick firmer for drying or any handling. Clear all "
            "mummies and drops: they are the primary brown-rot inoculum. The concentrated ripening window "
            "makes drying and freezing the practical outlet, and apricot holds up to both unusually well."
        ),
    },
    "cherry-sour": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first sour cherries now, and unlike a peach there is no thinning to "
            "do; they size on their own. Put that effort into netting instead, and get it on as the fruit "
            "starts to color, before the birds find it, with the bottom edge tied down. Keep pruning "
            "light, because sour cherry fruits on spurs, the short stubby side shoots that keep bearing "
            "for years, so you are building permanent structure rather than replacing fruiting wood each "
            "winter. Do not wait for these to taste sweet: a ripe sour cherry is still tart, so judge it "
            "by full deep-red color and juiciness instead."
        ),
        "first_harvest_notes_seasoned": (
            "A first set is small and worth protecting rather than thinning; sour cherry sizes without "
            "hand thinning. Redirect that labor into bird exclusion, netting as color breaks and securing "
            "the skirt, which is the practical argument for keeping the tree small enough to cover. Prune "
            "conservatively and preserve spur wood, since the tree builds permanent bearing structure "
            "rather than renewing it annually. Judge maturity on deep red color and juiciness, never on "
            "sweetness: sour cherry stays tart at full ripeness and does not improve after picking, so "
            "waiting for sugar just loses the crop to birds and cracking. In wet climates, shift major "
            "pruning to dry summer against bacterial canker."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year the tree carries a full crop. Sour cherries stay tart even when "
            "fully ripe and do not sweeten after picking, so go by full deep-red color and juiciness "
            "rather than taste. Pull by the stem; if a dead-ripe cherry slips off its stem that is fine "
            "for pies. Two things cost crops faster than any pest: birds, so keep the net on, and rain, "
            "since a soaking on ripe fruit cracks it. Pick ahead of a forecast wet spell. Work through "
            "the tree every couple of days, pick it clean rather than leaving stragglers behind, and "
            "chill what you pick quickly. Sour cherry is self-fruitful, so one tree is a whole orchard "
            "here."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year four. Sour cherry is non-climacteric and stays acid at "
            "full maturity, so harvest on deep red color and juiciness rather than on sugar. Pull by the "
            "stem where possible; stem-slip on a dead-ripe fruit is acceptable for processing. Birds and "
            "rain-cracking are the two crop-losing risks: hold exclusion netting through color and pick "
            "ahead of forecast rain. Work the tree every couple of days, strip it completely, and chill "
            "fast, since leftover ripe and split fruit builds spotted wing drosophila pressure for the "
            "rest of the season. Keep dormant pruning light and spur-preserving, and in wet regions move "
            "heavy cuts into dry summer weather against bacterial canker, the crop's most serious "
            "disease."
        ),
    },
    "cherry-sweet": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first sweet cherries now, and the job changes from the one you did on "
            "a peach. Do not thin cherries; they size perfectly well on their own. Put that effort into "
            "netting instead, and get the net on as the fruit starts to color, before the birds find it, "
            "with the bottom edge tied down. This is the real reason to keep a cherry small on a dwarfing "
            "rootstock, because a tree you cannot cover is a tree you will not harvest. Keep pruning "
            "light. Cherry fruits on spurs, the short stubby side shoots that keep bearing for years, so "
            "you are building permanent structure rather than replacing fruiting wood each winter."
        ),
        "first_harvest_notes_seasoned": (
            "A first set is likely to be small and worth protecting rather than thinning. Cherry sizes "
            "without hand thinning, so redirect that labor into bird exclusion: net as color breaks, "
            "ahead of first bird damage, and secure the skirt. Tree size is the binding constraint on "
            "whether netting is even possible, which is the practical argument for a dwarfing rootstock. "
            "Keep pruning conservative and spur-preserving, since sweet cherry bears on long-lived spurs "
            "and builds permanent structure rather than renewing annually. Pick by the stem rather than "
            "the fruit, which protects the spur for next year. In wet climates move major cuts to dry "
            "summer weather, because fresh cuts in cool damp conditions are the main entry point for "
            "bacterial canker."
        ),
        "full_harvest_notes_beginner": (
            "From about the fifth year the tree carries a full crop. Cherries do not ripen after picking, "
            "so taste one before you commit and pick only fully colored, sweet fruit. Pull each cherry by "
            "the stem rather than the fruit, which leaves the spur intact to bear again next year. Two "
            "things will cost you a crop faster than any pest: birds, so keep the net on, and rain, "
            "because a soaking on ripe fruit splits it. If rain is forecast, pick ahead of it. Work "
            "through the tree every couple of days once it starts, pick it clean rather than leaving "
            "stragglers, and chill what you pick quickly."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year five. Sweet cherry is non-climacteric, so it will not "
            "improve off the tree: sample for sugar before committing to a pick, and harvest only fully "
            "colored fruit. Pull by the stem to preserve the fruiting spur. The two crop-losing risks are "
            "birds and rain-cracking, so keep exclusion netting on through color and pick ahead of a "
            "forecast soaking. Work the tree every couple of days, strip it completely rather than "
            "leaving stragglers, and chill promptly: leftover ripe and split fruit is what builds spotted "
            "wing drosophila pressure through the rest of the season. Keep dormant pruning light and "
            "spur-preserving, and in wet regions move heavy cuts to dry summer against bacterial canker."
        ),
    },
    "nectarine": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first real nectarines now, and the crop will be light. Thin it anyway, "
            "and thin it hard: about a month after bloom, take the little fruit down to one nectarine "
            "every 6 to 8 inches along the branch. On a young tree that is as much about saving the limbs "
            "as about fruit size, because a branch that snaps under its first crop does not grow back. "
            "Pull off any fruit with a crescent scar as you go, since those are plum curculio and "
            "clearing them now means fewer next year. Keep pruning hard every winter: nectarine fruits on "
            "wood that grew the previous summer, so a tree that is not renewed each year slowly stops "
            "cropping."
        ),
        "first_harvest_notes_seasoned": (
            "A light, uneven first crop is normal while the framework fills in. Thin to one fruit every 6 "
            "to 8 inches within about a month of bloom, and on a young tree the governing reason is limb "
            "protection rather than sizing, since scaffold wood is still setting its permanent crotch "
            "angles. Cull curculio-stung fruit in the same pass to reduce next season's pressure. Renewal "
            "pruning is now non-negotiable: nectarine bears on one-year-old wood, so every dormant season "
            "must replace the fruiting wood the last crop consumed. Nectarine's thinner skin also makes "
            "it more brown-rot prone than peach, so spacing fruit so none touch is worth more here than "
            "the extra minutes cost."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year the tree carries a full crop, and the thing to know is that a "
            "nectarine is a peach without the fuzz, and that fuzz was doing a job. Bare skin bruises more "
            "easily, splits in a wet spell, and lets brown rot in faster, so nectarine asks for more care "
            "in the same season a peach would coast through. Thin to one fruit every 6 to 8 inches after "
            "bloom and space them so no two touch. Prune hard in late winter, because the fruit comes on "
            "wood that grew last summer. Pick over one to two weeks in several passes, when the green "
            "undertone has gone and the fruit gives slightly, and get it into the fridge quickly rather "
            "than letting it sit on a counter. Clear every leftover and dropped fruit at the end, since "
            "shrivelled fruit is what infects next year's crop."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year four. The tree becomes a maintenance system: annual "
            "renewal pruning to replace spent fruiting wood, annual thinning to one fruit every 6 to 8 "
            "inches, a late-summer borer inspection at the soil line, and end-of-season sanitation. "
            "Harvest on the green undertone fading, slight give, and clean release on an upward twist, "
            "over one to two weeks in several passes. Skinless fruit bruises and rots faster than peach, "
            "so cool it promptly and never pile it deep. Strip every mummy and clear dropped fruit: "
            "mummified fruit is the primary brown-rot inoculum for the following spring."
        ),
    },
    "peach": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first real peaches now, and the crop will be light. Thin it anyway, "
            "and thin it hard: about a month after bloom, take the little fruit down to one peach every 6 "
            "to 8 inches along the branch. On a young tree this is as much about protecting the limbs as "
            "about fruit size, because a branch that snaps under its first crop is gone for good. Pull "
            "off any fruit with a crescent scar on it as you go, since those are plum curculio and "
            "clearing them now means fewer next year. Keep pruning hard every winter: peach fruits on "
            "wood that grew the previous summer, so a tree that is not renewed each year slowly stops "
            "cropping."
        ),
        "first_harvest_notes_seasoned": (
            "Expect a light, uneven first crop while the framework fills in. Thin to one fruit every 6 to "
            "8 inches within about a month of bloom, and treat limb protection rather than sizing as the "
            "reason on a young tree, since scaffold wood at this age is still setting its permanent "
            "crotch angles and a break is not recoverable. Cull curculio-stung fruit in the same pass to "
            "cut next season's pressure. Renewal pruning becomes non-negotiable from here: peach bears on "
            "one-year-old wood, so each dormant season has to replace the fruiting wood the last crop "
            "used up, and a tree pruned timidly now declines into a shell of bare scaffolds with fruit "
            "only at the tips."
        ),
        "full_harvest_notes_beginner": (
            "From about the fourth year the tree carries a full crop, and the work settles into a yearly "
            "rhythm: prune hard in late winter, thin to one peach every 6 to 8 inches after bloom, and "
            "check the trunk at the soil line in late summer for the fresh gum and sawdust that mean "
            "borers. The tree ripens over one to two weeks, so pick it in several passes rather than all "
            "at once. A ripe peach has lost its green undertone, gives slightly to a gentle squeeze, and "
            "pulls free with a small twist. Handle it like an egg, because every bruise is a doorway for "
            "brown rot, and clear every leftover and dropped fruit at the end, since fruit left to "
            "shrivel on the tree is what infects next year's crop."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year four, and the tree is now a maintenance system rather than "
            "a project: annual renewal pruning to replace spent fruiting wood, annual thinning to one "
            "fruit every 6 to 8 inches, a late-summer borer inspection at the soil line, and end-of- "
            "season sanitation. Harvest on ground color losing its green cast, slight give, and clean "
            "abscission on an upward twist, over one to two weeks in several passes rather than a single "
            "strip. Bruising is the brown-rot entry point, so cool the fruit promptly if it is not eaten "
            "soon. Strip every mummy from the tree and clear dropped fruit: mummified fruit is the "
            "primary brown-rot inoculum, and leaving it is the difference between a clean season and a "
            "lost one."
        ),
    },
    "pear-asian": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first Asian pears now, and there are two things to get right. First, "
            "thin hard: within about a month of bloom take the fruit down to one per cluster and roughly "
            "6 inches apart. Asian pears set far more fruit than they can size, so this is the single "
            "biggest lever you have. Second, these ripen ON the tree, the opposite of a European pear. "
            "Pick them tree-ripe, by full color, an easy upward-twist release, and above all by taste. A "
            "pear picked early stays hard and bland and will not improve indoors. Keep spreading the "
            "limbs while the wood is young, and prune only in dry weather, because wet cuts invite fire "
            "blight."
        ),
        "first_harvest_notes_seasoned": (
            "Thin hard from the first real set: one fruit per cluster and roughly 6 inches apart, within "
            "about a month of bloom. Asian pear over-sets reliably, so thinning is the dominant lever on "
            "both size and annual regularity, and a light hand here produces a tree of small fruit and an "
            "off year following. The harvest rule inverts the European one: Asian pear is climacteric on "
            "the tree and is picked tree-ripe, on full color, clean upward-twist release, and sweetness "
            "confirmed by tasting. Early picking yields hard, bland fruit that never finishes. Continue "
            "limb spreading while the wood is young against pear's upright, narrow natural habit, and "
            "confine pruning to dry weather, since succulent regrowth from heavy cuts is what fire blight "
            "exploits."
        ),
        "full_harvest_notes_beginner": (
            "From about the fifth year the tree carries a full crop, and it will be a big one, because "
            "Asian pears over-set every year. Thin to one fruit per cluster and about 6 inches apart each "
            "spring; this never becomes optional. Pick tree-ripe and taste before you commit, since these "
            "do not finish indoors. The reward is storage: kept cold, most Asian pears hold for one to "
            "three months and stay crisp, with the late russet types such as Chojuro, Shinko and Olympic "
            "keeping longest. Handle them gently even so, because the thin skin bruises easily. Prune in "
            "late winter and only in dry weather, and wipe the pruners between cuts if fire blight has "
            "been around."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year five. Annual thinning to one fruit per cluster at about 6 "
            "inches remains mandatory rather than optional, because the over-setting habit does not "
            "moderate with age and an unthinned mature tree gives small fruit and an alternate-bearing "
            "cycle. Harvest tree-ripe on full color, clean release and confirmed sweetness. Storage is "
            "this crop's real advantage over European pear: most cultivars hold one to three months "
            "refrigerated with texture intact, the late russets (Chojuro, Shinko, Olympic) longest, so a "
            "large crop is an asset rather than a glut. The thin skin bruises readily, so handle for "
            "storage from the moment of picking. Dormant pruning stays in dry weather with fire-blight "
            "hygiene between cuts."
        ),
    },
    "pear-european": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first pears now, and the picking rule is the surprising part: a "
            "European pear is picked while it is still firm, not ripe. Left to ripen on the tree it goes "
            "brown and gritty at the core. Pick when it has reached full size, its green has begun to "
            "lighten, and the stem snaps free on an upward twist, then ripen it indoors. Thin the young "
            "fruit to one per cluster about a month after bloom for bigger pears and steadier crops. Keep "
            "training the framework with limb spreaders, since pears grow stubbornly upright and a narrow "
            "crotch angle is a branch that breaks later. Prune only in dry weather, because wet cuts "
            "invite fire blight."
        ),
        "first_harvest_notes_seasoned": (
            "A light first set is normal on a tree this age. Thin to one fruit per cluster within about a "
            "month of bloom. The harvest rule is the one to internalize now, because it is "
            "counterintuitive and it is the difference between fruit and compost: European pear is picked "
            "MATURE BUT FIRM and ripened off the tree, on full varietal size, lightening ground color, "
            "corky lenticels and clean stem separation on an upward twist. Tree-ripening produces core "
            "browning and grit cells. Keep spreading limbs while the wood is young, since pear's "
            "naturally upright, narrow habit sets weak crotch angles that fail under later crop loads. "
            "Prune conservatively and only in dry conditions: heavy cuts force succulent regrowth, which "
            "is exactly what fire blight exploits."
        ),
        "full_harvest_notes_beginner": (
            "From about the sixth year the tree carries a full crop. European pear takes longer to get "
            "going than most fruit trees and then keeps producing for decades, so the wait buys "
            "something. Pick firm, never tree-ripe, and finish the fruit indoors. Winter pears such as "
            "Anjou and Bosc need several weeks somewhere near freezing before they will ripen properly, "
            "while a summer Bartlett only needs a few days cool. Thin to one fruit per cluster each "
            "spring, prune in late winter and only when the weather is dry, and wipe your pruners between "
            "cuts if fire blight has been around, since it spreads on the blade."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year six, later than most of the roster, against a productive "
            "life measured in decades. The annual cycle is dormant pruning in dry weather only, thinning "
            "to one fruit per cluster, and disciplined fire-blight hygiene: disinfect between cuts when "
            "blight is present and excise cankers 8 to 12 inches below visible damage. Harvest mature but "
            "firm on size, lightening ground color, corky lenticels and clean stem snap; never tree-ripe. "
            "Post-harvest conditioning is cultivar-dependent and not optional: winter pears (Anjou, Bosc) "
            "require several weeks of near-freezing storage before they will ripen, while Bartlett "
            "conditions after a few days cool. Skipping the cold rest on a winter pear yields fruit that "
            "never softens properly."
        ),
    },
    "plum": {
        "first_harvest_notes_beginner": (
            "Your tree may set its first plums now. Thin them to one fruit every 4 to 6 inches about a "
            "month after bloom, and space them so no two plums touch, because touching fruit is how brown "
            "rot walks from one plum to the next through a cluster. If yours is a Japanese type (Santa "
            "Rosa, Methley) it will over-set and needs heavier thinning than a European type (Stanley, "
            "damson). Prune more lightly than you would a peach: plum bears largely on spurs, the short "
            "stubby side shoots that keep fruiting for years, so open the canopy rather than cutting "
            "everything back hard. Watch for black knot, a rough black swelling on a twig, and cut it out "
            "in winter well below the swelling."
        ),
        "first_harvest_notes_seasoned": (
            "A light first set is normal. Thin to one fruit every 4 to 6 inches within about a month of "
            "bloom, spacing so fruit do not touch, since contact is the transmission route for brown rot "
            "within a cluster. Japanese cultivars over-set and need markedly heavier thinning than "
            "Europeans. Prune conservatively and preserve spur wood: plum bears largely on long-lived "
            "spurs, so thin to open the canopy rather than heading back hard. Black knot management "
            "begins in earnest once the tree is bearing: cut every gall 3 to 4 inches below the visible "
            "swelling into clean wood during dormancy, before the fungus sporulates, and destroy the "
            "prunings off site rather than composting them on the property."
        ),
        "full_harvest_notes_beginner": (
            "From about the fifth year the tree carries a full crop, and the year settles into a rhythm: "
            "light dormant pruning that keeps the spurs, black knot cut out while the tree is bare, and "
            "thinning to one plum every 4 to 6 inches after bloom. The tree ripens over one to two weeks, "
            "so pick in several passes. A ripe plum shows full color, wears a dusty bloom on the skin, "
            "gives slightly, and pulls free easily; a European prune type is ripe when it is soft right "
            "down to the pit. Handle gently and clear the dropped fruit, because bruises let in brown rot "
            "and fruit left to shrivel on the tree or ground is next year's infection waiting to happen."
        ),
        "full_harvest_notes_seasoned": (
            "Full production from roughly year five. The annual cycle is light dormant pruning that "
            "preserves spur wood, black-knot excision while the structure is visible, thinning to one "
            "fruit every 4 to 6 inches, and post-harvest sanitation. Harvest over one to two weeks in "
            "several passes on full varietal color, intact bloom, slight give and clean release; European "
            "prune types are ripe when soft to the pit, which is later than they look. Handle gently, "
            "since bruising is the brown-rot entry point, and clear every mummy and drop, which are the "
            "following season's inoculum. Type still governs the tree: Japanese cultivars keep over- "
            "setting and keep needing the heavier thinning pass every year, not only while young."
        ),
    },
}

EDITS = {}   # wave 1 authors new fields only; no existing field is edited.


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
    print('WAVE 1 -- stone and pome, %d crops:' % len(TRIO))
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
