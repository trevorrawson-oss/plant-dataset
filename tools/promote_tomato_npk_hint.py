#!/usr/bin/env python3
"""GUARDED PROMOTE: the tomato NPK hints teach the fertilizer label wrong. Trevor-ruled 2026-07-31.

SURFACED BY the external blind audit, which found three tomatoes saying "you want the third number
to be the highest" and then giving `5-10-10` and `8-32-16` -- in neither of which is the third
number highest.

IT IS FIVE CROPS, NOT THREE. `beefsteak-tomato` and `heirloom-tomato` carry the same error in a
form the audit's read did not catch: "a higher third number on the bag (like 5-10-10)", where the
third number is TIED with the second, not higher.

AND THE UNDERLYING CLAIM IS UNSOURCED, which is the bigger finding. Both cited sources were fetched
and read in full:

  * Clemson HGIC never mentions potassium at all. It says "A soil test is always the best method of
    determining the fertilization needs of the crop" and to apply pre-plant fertilizer to test.
  * UMN Extension: "Apply phosphorus (P) and potassium (K) according to soil test recommendations...
    Unless your soil test report specifically recommends additional phosphorus, use a LOW- OR
    NO-PHOSPHORUS fertilizer. Too much nitrogen fertilization will lead to plants that are bushy,
    leafy, and slow to bear fruit."

So "make potassium the highest number" is supported by neither, and `8-32-16` -- phosphorus 32, the
largest number on that bag -- is the OPPOSITE of what UMN advises. We were teaching people to read a
label and then pointing them at the one formula our own source warns against, on the crop most
likely to be a beginner's first.

THE FIX RETREATS TO WHAT IS SOURCED rather than inventing a replacement rule: soil test first (both
sources), go easy on nitrogen before fruit set (UMN, verbatim), do not add phosphorus unless a test
calls for it (UMN, verbatim). `8-32-16` is removed outright. `5-10-10` stays because it IS this
crop's `npk_ratio` and is a conventional low-nitrogen garden formula.

NOT CHANGED, DELIBERATELY: `npk_ratio` itself stays `5-10-10` on all five. Whether a
phosphorus-containing formula is the right default when UMN advises low-or-no-P is a real question,
but it is a different one, and a value change never rides along with a wording correction.

FOOTPRINT: 2 fields x 5 crops = 10 edits, inside `fertilizer` only.

    $ python3 tools/promote_tomato_npk_hint.py --dry-run
    $ python3 tools/promote_tomato_npk_hint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '72adc3667192a92d086e596cebd935c0ea0ec708cccc0e4611705ffa7f34b5bb'

TRIO = ('cherry-tomato', 'grape-tomato', 'roma-tomato')
PAIR = ('beefsteak-tomato', 'heirloom-tomato')
SLUGS = TRIO + PAIR

OLD_BEGINNER_TRIO = (
    'Look for three numbers on the fertilizer bag: those are the NPK ratio (nitrogen, phosphorus, '
    'potassium). For fruiting tomatoes, you want the third number to be the highest: something like '
    '5-10-10 or 8-32-16 works well.')
OLD_SEASONED_TRIO = 'high K, e.g. 5-10-10 or 8-32-16'
OLD_BEGINNER_PAIR = (
    "Look for a high-potassium formula, often labeled 'tomato food' or showing a higher third "
    'number on the bag (like 5-10-10). That third number is the potassium, which supports fruit '
    'development.')
OLD_SEASONED_PAIR = 'high K, e.g. 5-10-10'

NEW_BEGINNER = (
    'Look for three numbers on the fertilizer bag: those are the NPK ratio (nitrogen, phosphorus, '
    'potassium). A soil test is the surest guide, and it is what both extension services behind '
    'this guide recommend first. Without one, a low-nitrogen balanced formula such as 5-10-10 is a '
    'sensible default. Go easy on the first number: too much nitrogen gives you a big leafy plant '
    'that is slow to set fruit. Skip the high-phosphorus bags sold as bloom boosters unless a soil '
    'test actually calls for phosphorus, because many soils already hold plenty.')
NEW_SEASONED = (
    'Soil test governs. Absent one, a low-nitrogen balanced formula such as 5-10-10. UMN advises a '
    'low- or no-phosphorus feed unless a test specifically calls for phosphorus, and warns that '
    'excess nitrogen produces bushy, leafy plants slow to bear fruit.')

EM = chr(8212)


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
        ob = OLD_BEGINNER_TRIO if slug in TRIO else OLD_BEGINNER_PAIR
        os_ = OLD_SEASONED_TRIO if slug in TRIO else OLD_SEASONED_PAIR
        if f.get('npk_hint_beginner') != ob:
            print('ABORT: %s npk_hint_beginner is not the expected prior text' % slug)
            return 2
        if f.get('npk_hint_seasoned') != os_:
            print('ABORT: %s npk_hint_seasoned is not the expected prior text' % slug)
            return 2
    print('verified: all %d carry their exact prior hint text' % len(SLUGS))

    ratios_before = {s: crops[s]['fertilizer'].get('npk_ratio') for s in SLUGS}
    other_before = {s: json.dumps({k: v for k, v in crops[s]['fertilizer'].items()
                                   if k not in ('npk_hint_beginner', 'npk_hint_seasoned')},
                                  sort_keys=True) for s in SLUGS}

    for slug in SLUGS:
        f = crops[slug]['fertilizer']
        f['npk_hint_beginner'] = NEW_BEGINNER
        f['npk_hint_seasoned'] = NEW_SEASONED

    for slug in SLUGS:
        f = crops[slug]['fertilizer']
        for k in ('npk_hint_beginner', 'npk_hint_seasoned'):
            v = f[k]
            if '8-32-16' in v:
                print('ABORT: %s still recommends 8-32-16' % slug)
                return 2
            if 'third number' in v and 'highest' in v:
                print('ABORT: %s still claims the third number should be highest' % slug)
                return 2
            if EM in v or '--' in v:
                print('ABORT: em dash or "--" in consumer copy: %s %s' % (slug, k))
                return 2
        if f.get('npk_ratio') != ratios_before[slug]:
            print('ABORT: npk_ratio moved on %s -- this promote is wording only' % slug)
            return 2
        if json.dumps({k: v for k, v in f.items()
                       if k not in ('npk_hint_beginner', 'npk_hint_seasoned')},
                      sort_keys=True) != other_before[slug]:
            print('ABORT: a non-hint fertilizer field moved on %s' % slug)
            return 2
    print('verified: 8-32-16 gone, false rule gone, npk_ratio and every other field frozen')

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
    print('verified: exactly %d crops, fertilizer only, %d edits' % (len(SLUGS), 2 * len(SLUGS)))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits across %d tomatoes' % (2 * len(SLUGS), len(SLUGS)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
