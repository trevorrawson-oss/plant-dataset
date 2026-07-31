#!/usr/bin/env python3
"""GUARDED PROMOTE: mid_atlantic sour cherry fruits_reliably -> marginal, with the odds explained.

Trevor-ruled 2026-07-30, revising his own 2026-07-20 call on evidence that did not exist then.

WHAT THE CLAIM RESTED ON. Nothing. z7 cited `vce_426_331`, which is "Virginia's Home Garden
VEGETABLE Planting Guide" and mentions cherry ZERO times; z8 cited `https://content.ces.ncsu.edu`,
NC State's website homepage. Our top suitability rating was backed by a vegetable table and a front
door.

WHAT NC STATE ACTUALLY SAYS. Extension Gardener Handbook ch. 15, verbatim:
    "Apricot and cherry trees grow in certain areas where the climate is favorable, but need
     careful management and will not consistently bear fruit."
It says "cherry" without splitting sour from sweet, and gives cultivar tables for apples, pears,
peaches and nectarines but NO cherry table at all. The one NC State office that does recommend
sour cherry is Macon County -- "we recommend apples, pears, and sour cherries for tree fruits
here" -- and Macon is in the far-western mountains, which `mid_atlantic` ("Piedmont and Coastal
Plain") explicitly excludes. Henderson County, also mountains, is cooler still: a tart cherry is
worth trying "for fun" if you have space. Cherry's two failure modes here -- early bloom into a
late freeze, and rain splitting fruit at ripening -- are both WORSE in the humid Piedmont and
Coastal Plain than in the mountains, so the single pro-sour recommendation comes from the part of
the state least like this region.

CONSISTENCY, which is the argument that needs no geography: apricot and cherry-sweet are ALREADY
`marginal` in this same region, and NC State's single sentence covers all three together. And
mid_south sour cherry was moved to `marginal` earlier today on the equivalent UAEX sentence, so
leaving mid_atlantic at `fruits_reliably` rated one crop differently in two neighbouring regions
with no evidence for the difference.

TREVOR'S FRAMING, and it is the reason the prose is rewritten rather than just the enum flipped:
"say based on its characteristics a grower might find more luck with it fruiting". `marginal` must
not read as "don't bother". Sour cherry's own characteristics genuinely tilt the odds, and both are
SOURCED to NC State county pages read this session:
    "Sour cherries (Prunus cerasus) are self fertile while sweet cherries (Prunus avium) need two
     varieties to pollinate."                                    -- NC State, Henderson County
    "Cherries will grow here with sour types being hardier."     -- NC State, Macon County
So: one tree can set a crop alone, it is the hardier of the two, and it handles the belt's humidity
better than sweet. A grower here has a real chance of fruit. What goes away is the PROMISE of a
dependable annual crop, which nothing backed.

FOOTPRINT: 6 edits on 1 crop (2 x suitability + 4 x prose). No other crop, region, date, calendar
or citation moves. The citations are deliberately left as they are -- fixing those is a separate
promote, because a value change and a citation change never ride together.

    $ python3 tools/promote_mid_atlantic_cherry_sour_marginal.py --dry-run
    $ python3 tools/promote_mid_atlantic_cherry_sour_marginal.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b'

SLUG = 'cherry-sour'
CHILL = {'7': '1100 to 1500', '8': '1000 to 1350'}

SEASONED = (
    "Chill is never the limiter here: the belt delivers roughly {chill} chilling hours a year in "
    "zone {z}, clearing this crop's variety range with margin (NC State Extension; regional "
    "four-source chill basket). What limits it is bloom and harvest weather, and NC State is "
    "direct about it: apricot and cherry trees grow where the climate is favorable but need "
    "careful management and will not consistently bear fruit. Cherries bloom early enough to meet "
    "a late freeze, and rain at ripening splits the fruit and invites brown rot, both of which "
    "run harder on the humid Piedmont and Coastal Plain than in the mountains. That said, sour "
    "cherry's own characteristics tilt the odds toward a crop: NC State notes the sour types are "
    "the hardier of the two cherries, and that sour cherry is self fertile while sweet cherry "
    "needs a second variety to pollinate, so a single tree can set fruit on its own. It also "
    "carries the belt's humidity better than sweet and ripens quickly, shortening its exposure to "
    "harvest rain. Treat it as the cherry to choose here and expect fruit in good years rather "
    "than every year.")

BEGINNER = (
    "Winters here are cold enough for this tree, so chilling is not the problem. Spring and summer "
    "weather is: cherries bloom early and can lose the flowers to a late freeze, and heavy rain "
    "right as the fruit ripens splits it and brings rot. NC State says cherries will not bear "
    "fruit consistently in this part of the country, so do not count on a crop every year. Even "
    "so, sour cherry is the one to pick if you want a cherry. It is the hardier of the two, and "
    "unlike sweet cherry it is self fertile, so one tree on its own can set fruit without a "
    "partner nearby. It also handles humid summers better and ripens fast, which gets the fruit "
    "off the tree before too much rain can spoil it. Plant it expecting good years and lean ones, "
    "not a crop every season.")

EDITS = []
for _z in ('7', '8'):
    EDITS.append((_z, 'suitability', 'fruits_reliably', 'marginal'))
    EDITS.append((_z, 'suitability_note_seasoned', None,
                  SEASONED.format(chill=CHILL[_z], z=_z)))
    EDITS.append((_z, 'suitability_note_beginner', None, BEGINNER))

FINDING = {
    'id': 'mid_atlantic_cherry_sour_marginal_ruling',
    'severity': 'low',
    'status': 'resolved',
    'blocks_launch': False,
    'summary': (
        'mid_atlantic sour cherry was `fruits_reliably` on evidence that turned out to be absent: '
        'the zone 7 cell cited "Virginia\'s Home Garden VEGETABLE Planting Guide" (zero mentions '
        'of cherry) and the zone 8 cell cited NC State\'s website homepage. NC State\'s Extension '
        'Gardener Handbook says apricot and cherry trees "will not consistently bear fruit", '
        'without distinguishing sour from sweet, and gives no cherry cultivar table at all while '
        'listing them for apples, pears, peaches and nectarines. The one NC State recommendation '
        'of sour cherry comes from Macon County in the far-western mountains, which this region '
        'explicitly excludes. Apricot and cherry-sweet were already `marginal` here on the same '
        'sentence, and mid_south sour cherry moved to `marginal` the same day on the equivalent '
        'UAEX sentence.'),
    'resolution': (
        'RULED 2026-07-30 by Trevor, revising his own 2026-07-20 call on evidence that did not '
        'exist then: mid_atlantic sour cherry -> `marginal` in both zones. Per his direction the '
        'prose does NOT read as discouragement -- it explains that sour cherry\'s own '
        'characteristics tilt the odds toward fruiting, each sourced to NC State county pages: '
        'sour types are the hardier of the two cherries (Macon County), and sour cherry is self '
        'fertile while sweet needs a second variety to pollinate (Henderson County), so one tree '
        'can set a crop alone. What was removed is the promise of a dependable annual crop, not '
        'the steer toward sour over sweet.'),
    'resolved_in': 'mid_atlantic_cherry_sour_ruling_2026_07_30',
    'basis': 'NC State Extension Gardener Handbook ch. 15; NC State Macon and Henderson County '
             'Extension pages; all fetched and read 2026-07-30. See '
             'docs/kickoffs/47-citation-arc-continuation-handoff.md section 6.',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    with open(args.canonical, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)
    crops = {c['slug']: c for c in data['crops']}
    if SLUG not in crops:
        print('ABORT: %s absent' % SLUG)
        return 2
    rbz = crops[SLUG]['regions']['mid_atlantic']['resolved_by_zone']
    if set(rbz) != {'7', '8'}:
        print('ABORT: mid_atlantic zones are %s, expected 7+8' % sorted(rbz))
        return 2

    # the sibling crops this ruling aligns with must already be marginal
    for sib in ('apricot', 'cherry-sweet'):
        for z, cell in crops[sib]['regions']['mid_atlantic']['resolved_by_zone'].items():
            if cell.get('suitability') != 'marginal':
                print('ABORT: %s z%s is %r, not marginal -- the consistency argument for this '
                      'ruling no longer holds' % (sib, z, cell.get('suitability')))
                return 2
    print('verified: apricot and cherry-sweet are already marginal here')

    cal_before = {z: list(rbz[z].get('calendar') or []) for z in rbz}
    dates_before = {z: {k: rbz[z].get(k) for k in
                        ('plant_out', 'harvest', 'harvest_start', 'harvest_end', 'bloom')}
                    for z in rbz}
    cites_before = json.dumps({z: rbz[z].get('anchoring_urls') for z in rbz}, sort_keys=True)

    for z, field, old, new in EDITS:
        cur = rbz[z].get(field)
        if old is not None and cur != old:
            print('ABORT: z%s %s expected %r, found %r' % (z, field, old, cur))
            return 2
        if cur == new:
            print('ABORT: z%s %s already at the new value' % (z, field))
            return 2
        rbz[z][field] = new

    for z in rbz:
        if list(rbz[z].get('calendar') or []) != cal_before[z]:
            print('ABORT: calendar moved in z%s' % z)
            return 2
        for k, v in dates_before[z].items():
            if rbz[z].get(k) != v:
                print('ABORT: %s moved in z%s' % (k, z))
                return 2
    if json.dumps({z: rbz[z].get('anchoring_urls') for z in rbz}, sort_keys=True) != cites_before:
        print('ABORT: a citation moved -- this promote is values only')
        return 2
    print('verified: no calendar, date or citation moved')

    ofs = crops[SLUG].setdefault('verification_status', {}).setdefault('open_findings', [])
    if any(isinstance(f, dict) and f.get('id') == FINDING['id'] for f in ofs):
        print('ABORT: finding already present')
        return 2
    ofs.append(json.loads(json.dumps(FINDING)))

    EM = chr(8212)
    for z, field, _o, _n in EDITS:
        v = rbz[z][field]
        if isinstance(v, str) and (EM in v or '--' in v):
            print('ABORT: em dash or "--" in consumer copy: z%s %s' % (z, field))
            return 2
    print('verified: no em dash or "--" in the rewritten copy')

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != [SLUG]:
        print('ABORT: crops changed = %s, expected only %s' % (changed, SLUG))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    for rid in ba[SLUG].get('regions', {}):
        if rid != 'mid_atlantic' and ba[SLUG]['regions'][rid] != aa[SLUG]['regions'][rid]:
            print('ABORT: region %s of %s changed' % (rid, SLUG))
            return 2
    print('verified: only %s / mid_atlantic changed' % SLUG)

    if args.dry_run:
        for z, field, _o, _n in EDITS:
            print('  z%s %s' % (z, field))
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits + 1 finding on %s' % (len(EDITS), SLUG))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
