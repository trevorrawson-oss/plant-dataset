#!/usr/bin/env python3
"""GUARDED PROMOTE: replace lettuce-leaf's 11 boolean `verified` flags with a real check date.

Trevor-ruled 2026-07-31, from his independent blind audit.

THE DEFECT. `anchoring_urls[*].verified` is meant to hold the DATE a link was checked, which is
what makes staleness computable. In 11 places on `lettuce-leaf` it held the boolean `true`, which
asserts "verified" while destroying the only fact that matters -- when. Every affected node had
`true` on ALL of its links, so there was no sibling date to inherit; backfilling one would have
been inventing a verification that never happened (the fill-the-shape-is-the-defect trap).

SO THE CHECK WAS ACTUALLY PERFORMED. All 11 URLs were fetched 2026-07-31 and each was confirmed:

  * HTTP 200,
  * a real document rather than a WAF challenge page or an empty extraction, using the shared
    `unreadable_reason()` detector built for exactly this failure, and
  * ON TOPIC -- each page mentions the pest or disease it is cited for (aphids, slugs and snails,
    lettuce root aphid, downy mildew, tipburn).

11/11 passed, so today's date is a record of work done, not a rubber stamp. Had any failed it would
have been left boolean and surfaced instead.

FOOTPRINT: 11 field writes on 1 crop, inside `pests` and `diseases` only. No url, source id,
region, value or calendar moves.

    $ python3 tools/promote_lettuce_verified_dates.py --dry-run
    $ python3 tools/promote_lettuce_verified_dates.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'a346915312a1089672c6f333c93e4bc96becaf8a691f8e81db08ee2612e2869e'

SLUG = 'lettuce-leaf'
CHECK_DATE = '2026-07-31'
SUBTREES = ('pests', 'diseases')
EXPECTED = 11

# (subtree, index, source_id) -> the url confirmed live and on-topic on CHECK_DATE.
VERIFIED = {
    ('pests', 0, 'clemson_hgic'):
        'https://hgic.clemson.edu/factsheet/insecticidal-soaps-for-garden-pest-control/',
    ('pests', 0, 'uf_ifas'):
        'https://blogs.ifas.ufl.edu/stlucieco/2023/03/31/aphids-on-plants-and-their-management',
    ('pests', 0, 'wsu_ext'):
        'https://depts.washington.edu/hortlib/pal/managing-and-controlling-aphids/',
    ('pests', 1, 'osu_ext'):
        'https://extension.oregonstate.edu/catalog/pub/em-9155-how-control-slugs-your-garden',
    ('pests', 1, 'ucanr_ext'):
        'https://ucanr.edu/blog/real-dirt/article/using-integrated-pest-management-control-slugs-and-snails',
    ('pests', 2, 'uc_ipm'):
        'https://ipm.ucanr.edu/agriculture/lettuce/lettuce-root-aphid/',
    ('pests', 2, 'usu_ext'):
        'https://extension.usu.edu/planthealth/ipm/notes_ag/veg-aphids',
    ('diseases', 0, 'uc_ipm'):
        'https://ipm.ucanr.edu/agriculture/lettuce/downy-mildew/',
    ('diseases', 0, 'umass_ext'):
        'https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/lettuce-downy-mildew',
    ('diseases', 0, 'uf_ifas_edis'):
        'https://edis.ifas.ufl.edu/publication/HS1403',
    ('diseases', 1, 'uc_ipm'):
        'https://ipm.ucanr.edu/agriculture/lettuce/tipburn/',
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
    crop = crops[SLUG]

    found = []
    for sub in SUBTREES:
        for i, item in enumerate(crop.get(sub) or []):
            au = item.get('anchoring_urls') if isinstance(item, dict) else None
            if not isinstance(au, dict):
                continue
            for sid, entry in au.items():
                if isinstance(entry, dict) and isinstance(entry.get('verified'), bool):
                    found.append((sub, i, sid, entry))

    if len(found) != EXPECTED:
        print('ABORT: expected %d boolean `verified` on %s, found %d'
              % (EXPECTED, SLUG, len(found)))
        return 2
    print('verified: exactly %d boolean flags present' % EXPECTED)

    # every one must be a link we actually checked, at the url we checked
    for sub, i, sid, entry in found:
        key = (sub, i, sid)
        if key not in VERIFIED:
            print('ABORT: %s/%d/%s was not part of the 2026-07-31 check' % key)
            return 2
        if entry.get('url') != VERIFIED[key]:
            print('ABORT: %s/%d/%s url is %r, but %r was what was checked'
                  % (sub, i, sid, entry.get('url'), VERIFIED[key]))
            return 2
    print('verified: all %d match the urls actually fetched on %s' % (EXPECTED, CHECK_DATE))

    for _sub, _i, _sid, entry in found:
        entry['verified'] = CHECK_DATE

    # ---- blast radius ------------------------------------------------------
    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != [SLUG]:
        print('ABORT: crops changed = %s, expected only [%s]' % (changed, SLUG))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    diff = sorted(k for k in set(ba[SLUG]) | set(aa[SLUG]) if ba[SLUG].get(k) != aa[SLUG].get(k))
    if diff != sorted(SUBTREES):
        print('ABORT: %s changed %s, expected only %s' % (SLUG, diff, sorted(SUBTREES)))
        return 2

    # no url, source id or any other key may have moved -- only `verified`
    def anchors(crop_obj):
        out = {}
        for sub in SUBTREES:
            for i, item in enumerate(crop_obj.get(sub) or []):
                au = item.get('anchoring_urls') if isinstance(item, dict) else None
                if isinstance(au, dict):
                    for sid, e in au.items():
                        out[(sub, i, sid)] = {k: v for k, v in e.items() if k != 'verified'}
                out[('__sources__', sub, i)] = json.dumps(
                    item.get('sources') if isinstance(item, dict) else None, sort_keys=True)
        return out

    if anchors(ba[SLUG]) != anchors(aa[SLUG]):
        print('ABORT: something other than `verified` moved')
        return 2
    remaining = [1 for sub in SUBTREES for item in (aa[SLUG].get(sub) or [])
                 if isinstance(item, dict)
                 for e in (item.get('anchoring_urls') or {}).values()
                 if isinstance(e, dict) and isinstance(e.get('verified'), bool)]
    if remaining:
        print('ABORT: %d boolean `verified` still present' % len(remaining))
        return 2
    print('verified: 1 crop / %d writes; urls, source ids and every other key frozen' % EXPECTED)

    if args.dry_run:
        for sub, i, sid, _e in found:
            print('  %s[%d].%s  true -> %s' % (sub, i, sid, CHECK_DATE))
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d verification dates stamped on %s' % (EXPECTED, SLUG))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
