#!/usr/bin/env python3
"""GUARDED PROMOTE: record that 3 of the 12 fruit-trees repoints rest on a GENERIC sentence.

DOCUMENTATION ONLY. Zero value changes, zero citation changes.

`tools/doc_mentions_crop_scan.py`, run blind over the roster, flagged work committed hours
earlier in 07b7dbf: the UAEX Home Garden Fruit Trees page (`uada_ext_fruit_trees`) never names
apricot, mulberry or pomegranate. Measured on the fetched page:

    apple 16   pear 13   peach 14   nectarine 10   plum 4
    persimmon 8   pawpaw 8   fig 7   cherry 1
    apricot ZERO   mulberry ZERO   pomegranate ZERO

Nine of the twelve repointed crops are named outright. These three are covered only by the
page's GENERIC sentence -- "Fruit trees other than figs, could be planted in the fall, but
often the best variety availability will be in late winter." Apricot, mulberry and pomegranate
ARE deciduous fruit trees, so the citation is defensible and is NOT being reverted. But it is
an inference from a general statement rather than a crop-specific mention, which is weaker
than the other nine, and the difference belongs on the record rather than in my head.

This is the scan earning its keep on its first run: it audited careful hand work from the same
day and found the soft spot in it.

FOOTPRINT: exactly one open_finding appended to each of 3 crops. Nothing else moves.

    $ python3 tools/promote_fruit_trees_generic_basis_caveat.py --dry-run
    $ python3 tools/promote_fruit_trees_generic_basis_caveat.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '7ca9e487df51e9d6cd2882c7305c12f536b3733154ac5298bdbd4c0fb079bbe9'

CROPS = ['apricot', 'mulberry', 'pomegranate']
FINDING_ID = 'mid_south_fruit_trees_citation_generic_basis'
NEW_ID = 'uada_ext_fruit_trees'

FINDING = {
    'id': FINDING_ID,
    'severity': 'low',
    'status': 'accepted_modeled',
    'blocks_launch': False,
    'summary': (
        'The mid_south plant_out citation to uada_ext_fruit_trees (UAEX, Home Garden Fruit Trees '
        'in Arkansas) rests on that page\'s GENERIC sentence, not on a crop-specific mention. The '
        'page names apple, pear, peach, nectarine, plum, persimmon, pawpaw, fig and cherry, but '
        'it does NOT name apricot, mulberry or pomegranate anywhere. What supports this cell is '
        '"Fruit trees other than figs, could be planted in the fall, but often the best variety '
        'availability will be in late winter", which is a statement about fruit trees as a class; '
        'this crop is a deciduous fruit tree, so the Dec-Feb dormant window follows. Defensible '
        'and deliberately NOT reverted, but weaker than the nine crops the page names outright, '
        'and recorded so the distinction is not lost. Surfaced by tools/doc_mentions_crop_scan.py '
        'auditing the repoint made the same day in commit 07b7dbf.'),
    'basis': (
        'Measured 2026-07-30 on the page fetched with urllib and counted with word-boundary '
        'matching: apple 16, pear 13, peach 14, nectarine 10, plum 4, persimmon 8, pawpaw 8, '
        'fig 7, cherry 1, and apricot / mulberry / pomegranate ZERO. See '
        'docs/2026-07-30-mid-south-uada-ext-citation-hunt.md.'),
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

    for slug in CROPS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        ms = (crop.get('regions') or {}).get('mid_south') or {}
        # the finding describes a citation that must actually be present
        found = False
        for _z, cell in (ms.get('resolved_by_zone') or {}).items():
            if NEW_ID in (cell.get('anchoring_urls') or {}):
                found = True
        if not found:
            print('ABORT: %s mid_south does not cite %s -- the finding would misdescribe it'
                  % (slug, NEW_ID))
            return 2
        ofs = (crop.get('verification_status') or {}).get('open_findings') or []
        if any(isinstance(f, dict) and f.get('id') == FINDING_ID for f in ofs):
            print('ABORT: finding already present on %s' % slug)
            return 2

    print('verified the citation exists on all %d crops' % len(CROPS))
    if args.dry_run:
        for s in CROPS:
            print('  %-14s <- %s' % (s, FINDING_ID))
        print('\nDRY RUN -- nothing written.')
        return 0

    for slug in CROPS:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(json.loads(json.dumps(FINDING)))

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    stray = []

    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in set(a) | set(b):
                if k == 'open_findings':
                    continue
                if k not in a or k not in b:
                    stray.append(path + '.' + str(k))
                else:
                    walk(a[k], b[k], path + '.' + str(k))
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                stray.append(path + '[len]')
                return
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, path + '[%d]' % i)
        elif a != b:
            stray.append(path)

    if set(ba) != set(aa):
        print('ABORT: crop roster changed')
        return 2
    for slug in ba:
        walk(ba[slug], aa[slug], slug)
    for k in before:
        if k != 'crops':
            walk(before[k], data[k], k)
    if stray:
        print('ABORT: %d change(s) outside open_findings: %s' % (len(stray), stray[:8]))
        return 2
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
        return 2
    print('verified: ZERO changes outside open_findings, exactly %d crops' % len(changed))

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d findings added, 0 values changed' % len(CROPS))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
