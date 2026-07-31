#!/usr/bin/env python3
"""GUARDED PROMOTE: the five tomatoes' fertilizer cadence, per Clemson. Trevor-ruled 2026-07-31.

THE DEFECT. Every tomato record carried `frequency: "every 2 weeks"` with `notify_days_after: 14`,
while its own `amount_*` prose said "repeated every 3 to 4 weeks". Surfaced by Trevor's independent
blind audit and confirmed here. It is not only a prose contradiction: `notify_days_after` drives the
app's reminder, so the shipped cadence tells a gardener to feed roughly twice as often as the
sourced guidance supports.

WHAT THE CITED SOURCE ACTUALLY SAYS. Clemson HGIC, already cited on this node, fetched and read
from raw bytes:

    "Side dress 1 pound of calcium nitrate (15.5-0-0) per 100 square feet (30 feet of row) three
     to four weeks after planting. On sandier soil, this may need to be split into two applications
     three to four weeks apart..."

So the interval is three to four weeks and the FIRST feed is three to four weeks after planting.
UMN, the other cited source, carries no interval at all.

THREE START TRIGGERS WERE IN ONE NODE: `timing` said first flowers, `stage_id` said flowering, and
the prose said first fruit at quarter size. Trevor ruled: use Clemson's.

STAGE MAPPING IS PRECEDENTED, NOT INVENTED. `established` + `notify_days_after: 21` +
"side-dress about 3 to 4 weeks later" is exactly the shape cauliflower, cabbage and kohlrabi
already use, and tomatillo (same family) uses `established` + 28.

THE UGA ATTRIBUTION IS DROPPED, not repointed (Trevor-ruled). The prose credited "per UGA
Extension" for a rate-and-interval claim, but UGA is not among this node's sources (umn_ext,
clemson_hgic) and the catalog's `uga_ext` entry is a bare host, `https://extension.uga.edu`, with
no document behind it. The composite claim (1 lb of 10-10-10) is also not Clemson's product, so no
new institution is credited in its place; the node's structural citations stand on their own.

THE FORMULA SWITCH IS PRESERVED. Feeding cadence and the balanced-to-high-potassium switch at
flowering are two different facts. Moving the reminder to establishment would have silently dropped
the switch, so the notification message now carries both.

FOOTPRINT: 8 fields x 5 crops = 40 edits. Fertilizer only. No calendar, date, region, suitability
or citation node moves; `sources` and `anchoring_urls` are asserted frozen.

    $ python3 tools/promote_tomato_fertilizer_cadence.py --dry-run
    $ python3 tools/promote_tomato_fertilizer_cadence.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'd77b9c5166896fa15a815ec25140d9531f966a592abc881fe528875647bb4590'

SLUGS = ('cherry-tomato', 'beefsteak-tomato', 'roma-tomato', 'heirloom-tomato', 'grape-tomato')

OLD_SCALAR = {'frequency': 'every 2 weeks', 'notify_days_after': 14,
              'stage_id': 'flowering', 'timing': 'start when first flowers appear'}
NEW_SCALAR = {'frequency': 'every 3 to 4 weeks', 'notify_days_after': 21,
              'stage_id': 'established',
              'timing': 'starter at transplanting, then side-dress about 3 to 4 weeks later'}

# Exact prior -> new prose, per crop. Two variants exist across the five.
SMALL = ('cherry-tomato', 'roma-tomato', 'grape-tomato')
BIG = ('beefsteak-tomato', 'heirloom-tomato')

BEGINNER_OLD_SMALL = 'starting when the first little tomatoes form and then every 3 to 4 weeks'
BEGINNER_NEW_SMALL = 'starting about 3 to 4 weeks after transplanting and then every 3 to 4 weeks'
BEGINNER_OLD_BIG = 'beginning when the first fruits form and repeating every 3 to 4 weeks'
BEGINNER_NEW_BIG = 'beginning about 3 to 4 weeks after transplanting and repeating every 3 to 4 weeks'

SEASONED_OLD_SMALL = ('side-dressed when the first fruits reach about the size of a quarter, '
                      'repeated every 3 to 4 weeks through harvest, per UGA Extension;')
SEASONED_NEW_SMALL = ('side-dressed three to four weeks after transplanting, repeated every 3 to 4 '
                      'weeks through harvest;')
SEASONED_OLD_BIG = ('side-dressed once the first fruits reach about the size of a quarter, '
                    'repeated every 3 to 4 weeks through harvest, per UGA Extension;')
SEASONED_NEW_BIG = ('side-dressed three to four weeks after transplanting, repeated every 3 to 4 '
                    'weeks through harvest;')

MSG_BEGINNER = ('Time for your tomatoes\' first side-dressing, about 3 to 4 weeks after planting '
                'out, then again every 3 to 4 weeks. Once flowers appear, switch to a tomato or '
                'high-potassium fertilizer to keep the fruit coming.')
MSG_SEASONED = ('First side-dress is due, about 3 to 4 weeks after transplanting, then every 3 to '
                '4 weeks through harvest. Switch to the high-potassium formula at flowering.')

EM = chr(8212)


def _sub(text, old, new, label):
    if old not in text:
        raise AssertionError('%s: expected fragment not found' % label)
    return text.replace(old, new, 1)


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

    for slug in SLUGS:
        if slug not in crops:
            print('ABORT: %s absent' % slug)
            return 2
        f = crops[slug].get('fertilizer')
        if not isinstance(f, dict):
            print('ABORT: %s has no fertilizer dict' % slug)
            return 2
        for k, v in OLD_SCALAR.items():
            if f.get(k) != v:
                print('ABORT: %s fertilizer.%s is %r, expected %r' % (slug, k, f.get(k), v))
                return 2
    print('verified: all 5 tomatoes carry the exact prior cadence')

    # the stage we move to must really exist on each crop
    for slug in SLUGS:
        ids = {s.get('id') for s in (crops[slug].get('growth_stages') or []) if isinstance(s, dict)}
        if NEW_SCALAR['stage_id'] not in ids:
            print('ABORT: %s has no growth stage %r (has %s)'
                  % (slug, NEW_SCALAR['stage_id'], sorted(ids)))
            return 2
    print('verified: every crop has the %r stage we point at' % NEW_SCALAR['stage_id'])

    cites_before = {s: json.dumps({k: crops[s]['fertilizer'].get(k)
                                   for k in ('sources', 'anchoring_urls')}, sort_keys=True)
                    for s in SLUGS}

    edits = 0
    for slug in SLUGS:
        f = crops[slug]['fertilizer']
        for k, v in NEW_SCALAR.items():
            f[k] = v
            edits += 1
        b_old, b_new = ((BEGINNER_OLD_SMALL, BEGINNER_NEW_SMALL) if slug in SMALL
                        else (BEGINNER_OLD_BIG, BEGINNER_NEW_BIG))
        s_old, s_new = ((SEASONED_OLD_SMALL, SEASONED_NEW_SMALL) if slug in SMALL
                        else (SEASONED_OLD_BIG, SEASONED_NEW_BIG))
        try:
            f['amount_beginner'] = _sub(f['amount_beginner'], b_old, b_new, slug + '/beginner')
            f['amount_seasoned'] = _sub(f['amount_seasoned'], s_old, s_new, slug + '/seasoned')
        except AssertionError as e:
            print('ABORT: %s' % e)
            return 2
        f['notify_message_beginner'] = MSG_BEGINNER
        f['notify_message_seasoned'] = MSG_SEASONED
        edits += 4

    for slug in SLUGS:
        f = crops[slug]['fertilizer']
        if 'UGA' in f['amount_seasoned']:
            print('ABORT: %s still credits UGA' % slug)
            return 2
        for k in ('amount_beginner', 'amount_seasoned', 'notify_message_beginner',
                  'notify_message_seasoned', 'timing', 'frequency'):
            v = f[k]
            if isinstance(v, str) and (EM in v or '--' in v):
                print('ABORT: em dash or "--" in consumer copy: %s %s' % (slug, k))
                return 2
        if json.dumps({k: f.get(k) for k in ('sources', 'anchoring_urls')},
                      sort_keys=True) != cites_before[slug]:
            print('ABORT: a citation moved on %s -- this promote is values only' % slug)
            return 2
    print('verified: UGA attribution gone, no em dash, citations frozen')

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != sorted(SLUGS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(SLUGS)))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    for slug in SLUGS:
        diff = sorted(k for k in set(ba[slug]) | set(aa[slug]) if ba[slug].get(k) != aa[slug].get(k))
        if diff != ['fertilizer']:
            print('ABORT: %s changed %s, expected only fertilizer' % (slug, diff))
            return 2
    print('verified: exactly 5 crops, fertilizer only, %d field writes' % edits)

    if args.dry_run:
        print('\n  %s -> %s' % (OLD_SCALAR['frequency'], NEW_SCALAR['frequency']))
        print('  notify_days_after %s -> %s' % (OLD_SCALAR['notify_days_after'],
                                                NEW_SCALAR['notify_days_after']))
        print('  stage_id %s -> %s' % (OLD_SCALAR['stage_id'], NEW_SCALAR['stage_id']))
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits across %d tomatoes' % (edits, len(SLUGS)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
