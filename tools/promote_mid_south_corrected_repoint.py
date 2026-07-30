#!/usr/bin/env python3
"""GUARDED PROMOTE: repoint the three CORRECTED mid_south crops at their documents.

CITATION-ONLY. Not one value moves. This is the follow-on to
tools/promote_mid_south_fruit_corrections.py, deliberately split from it because a value change
and a citation change never ride in one promote.

Those three cells were held back from the earlier repoint (promote_mid_south_fruit_tree_repoint.py)
precisely BECAUSE the documents contradicted them -- citing a page that disagrees with the cell
publishes the contradiction. Now that the values are corrected, each document supports the cell it
is being attached to, and every claim below was checked against text read this session:

  fig        -> uada_ext_fruit_trees (existing id)
     "Fig trees should not be planted until early spring."   backs plant_out "Mar - Apr".
     Fig HARVEST remains undocumented by this page; the cell-level anchor carries the planting
     claim, the same treatment the twelve tree fruits already received.

  raspberry  -> uada_ext_fsa6107 (new)
     "Planting should occur in the spring as soon as the soil can be properly prepared."
        backs plant_out "March to April".
     "Summer bearing varieties produce one crop in the early summer."
        backs harvest "late June to July" (z7) / "June to July" (z8).

  blueberry  -> uada_ext_fsa6104 (new)
     "The northern highbush type is better adapted to the northern part of the state."
        backs z7 recommended_type northern_highbush.
     "Plant blueberries in the fall or spring."  backs plant_out "March to April".
     "it is possible to harvest fresh fruit in central Arkansas from the end of May until late
      July."  backs harvest "June to July" (z7) / "June to mid-July" (z8), both inside it.

FOOTPRINT: 2 new source_catalog entries; uada_ext -> the mapped id on exactly 10 anchoring_urls
nodes across 3 crops. Every other byte identical. COMPACT preserved.

    $ python3 tools/promote_mid_south_corrected_repoint.py --dry-run
    $ python3 tools/promote_mid_south_corrected_repoint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'd1b441c27f9d1cfe243977e794fc9207ed58361e87ea402af0a37e0845f0f65a'

OLD_ID = 'uada_ext'
BARE = 'https://www.uaex.uada.edu'
VERIFIED = '2026-07-30'

TARGET = {
    'fig': 'uada_ext_fruit_trees',
    'raspberry': 'uada_ext_fsa6107',
    'blueberry': 'uada_ext_fsa6104',
}
URLS = {
    'uada_ext_fruit_trees': 'https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx',
    'uada_ext_fsa6107': 'https://www.uaex.uada.edu/publications/PDF/FSA-6107.pdf',
    'uada_ext_fsa6104': 'https://www.uaex.uada.edu/publications/PDF/FSA-6104.pdf',
}
NEW_CATALOG = {
    'uada_ext_fsa6107': {
        'id': 'uada_ext_fsa6107',
        'name': 'UAEX FSA6107, Raspberry Production in the Home Garden (Keith Striegler)',
        'publisher': ('University of Arkansas Division of Agriculture, Cooperative Extension '
                      'Service'),
        'url': URLS['uada_ext_fsa6107'],
        'source_class': 'university_extension',
        'trust_tier': 'high',
        'accessed': '2026-07',
        'tier': 'T1',
        'citable_for': (
            'UAEX specific publication FSA6107 (Dr. Keith Striegler, Extension Horticulture '
            'Specialist, Fruit). Arkansas home-garden raspberry: PLANTING SEASON, "Planting should '
            'occur in the spring as soon as the soil can be properly prepared" -- backs the '
            'mid_south March-April plant_out and rules out the dormant winter window. Fruiting '
            'habit, "Summer bearing varieties produce one crop in the early summer", with UAEX '
            'recommending that everbearing types be cropped in the fall only under Arkansas '
            'conditions. Regional adaptation, "In general, they are not well-adapted to climates '
            'south of Missouri", and per-cultivar northern/southern Arkansas recommendations '
            '(Heritage and Jewel for northern Arkansas).'),
    },
    'uada_ext_fsa6104': {
        'id': 'uada_ext_fsa6104',
        'name': 'UAEX FSA6104, Blueberry Production in the Home Garden (M. Elena Garcia)',
        'publisher': ('University of Arkansas Division of Agriculture, Cooperative Extension '
                      'Service'),
        'url': URLS['uada_ext_fsa6104'],
        'source_class': 'university_extension',
        'trust_tier': 'high',
        'accessed': '2026-07',
        'tier': 'T1',
        'citable_for': (
            'UAEX specific publication FSA6104 (M. Elena Garcia, Extension Fruit and Nut '
            'Specialist). Arkansas blueberry TYPE BY REGION, which is the load-bearing claim: "The '
            'northern highbush type is better adapted to the northern part of the state"; "In '
            'southern Arkansas, southern highbush or rabbiteye varieties should be grown"; '
            '"Central Arkansas is the transition zone where all types of blueberries can be '
            'cultivated", with "northern highbush varieties can be grown at higher elevations, '
            'while southern highbush or rabbiteye varieties should be grown at lower elevations in '
            'central Arkansas". Corroborated by FSA6130 (headers "Northern Highbush (Northern and '
            'Central Ark.)" vs "Rabbiteye (Central and Southern Ark.)") and the UAEX Arkansas '
            'Berries page. PLANTING, "Plant blueberries in the fall or spring." HARVEST, "it is '
            'possible to harvest fresh fruit in central Arkansas from the end of May until late '
            'July." Soil pH 4.8 to 5.4 preferable in Arkansas; irrigation is a must.'),
    },
}

# the corrected value each repoint asserts, so we never cite a document that disagrees again
PRECONDITIONS = {
    'fig': lambda c: c.get('plant_out') == 'Mar - Apr (dormant plant)',
    'raspberry': lambda c: c.get('plant_out') == 'March to April',
    'blueberry': lambda c: c.get('plant_out') == 'March to April',
}
EXTRA = {'blueberry': lambda ms: ms['resolved_by_zone']['7'].get(
    'recommended_type') == 'northern_highbush'}


def _repoint(node, new_id, touched, label):
    au = node.get('anchoring_urls')
    if not isinstance(au, dict) or OLD_ID not in au:
        return False
    if (au[OLD_ID] or {}).get('url') != BARE:
        return False
    if new_id in au:
        return False
    node['anchoring_urls'] = {
        (new_id if k == OLD_ID else k): ({'url': URLS[new_id], 'verified': VERIFIED}
                                         if k == OLD_ID else v)
        for k, v in au.items()}
    srcs = node.get('sources')
    if isinstance(srcs, list) and OLD_ID in srcs:
        node['sources'] = [new_id if s == OLD_ID else s for s in srcs]
    touched.append(label)
    return True


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
    cat = data.setdefault('source_catalog', {})

    for cid in NEW_CATALOG:
        if cid in cat:
            print('ABORT: source_catalog already holds %s' % cid)
            return 2
    if 'uada_ext_fruit_trees' not in cat:
        print('ABORT: uada_ext_fruit_trees missing -- run the fruit-tree repoint first')
        return 2

    # THE GUARD THAT MATTERS: only cite a document whose claim the cell now makes
    for slug, pred in PRECONDITIONS.items():
        ms = crops[slug]['regions']['mid_south']
        for z, c in ms['resolved_by_zone'].items():
            if not pred(c):
                print('ABORT: %s z%s is not at its corrected value (%r) -- repointing here would '
                      'publish a contradiction' % (slug, z, c.get('plant_out')))
                return 2
        if slug in EXTRA and not EXTRA[slug](ms):
            print('ABORT: %s has not had its corrected type applied' % slug)
            return 2
    print('verified: all three crops carry their corrected values')

    touched = []
    for slug, new_id in TARGET.items():
        ms = crops[slug]['regions']['mid_south']
        for i, arm in enumerate(ms.get('plantings') or []):
            _repoint(arm, new_id, touched, '%s plantings[%d]' % (slug, i))
            for j, sub in enumerate(arm.get('plant_out') or []):
                if isinstance(sub, dict):
                    _repoint(sub, new_id, touched,
                             '%s plantings[%d].plant_out[%d]' % (slug, i, j))
        for z, c in (ms.get('resolved_by_zone') or {}).items():
            _repoint(c, new_id, touched, '%s resolved_by_zone.%s' % (slug, z))

    EXPECTED = 10
    if len(touched) != EXPECTED:
        print('ABORT: repointed %d nodes, expected exactly %d' % (len(touched), EXPECTED))
        for t in touched:
            print('    ' + t)
        return 2
    for cid, entry in NEW_CATALOG.items():
        cat[cid] = json.loads(json.dumps(entry))
    print('repointed %d nodes:' % len(touched))
    for t in touched:
        print('  ' + t)

    # prove nothing but citations moved
    stray = []

    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in set(a) | set(b):
                if k in ('anchoring_urls', 'sources'):
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

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    if set(ba) != set(aa):
        print('ABORT: crop roster changed')
        return 2
    for slug in ba:
        walk(ba[slug], aa[slug], slug)
    for k in before:
        if k not in ('crops', 'source_catalog'):
            walk(before[k], data[k], k)
    if stray:
        print('ABORT: %d change(s) outside citations: %s' % (len(stray), stray[:8]))
        return 2
    print('verified: ZERO changes outside anchoring_urls/sources')

    if set(cat) - set(before.get('source_catalog') or {}) != set(NEW_CATALOG):
        print('ABORT: unexpected source_catalog delta')
        return 2
    for k in (before.get('source_catalog') or {}):
        if before['source_catalog'][k] != cat[k]:
            print('ABORT: existing catalog entry %s mutated' % k)
            return 2
    print('verified: source_catalog gained exactly %d entries, none mutated' % len(NEW_CATALOG))

    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != ['blueberry', 'fig', 'raspberry']:
        print('ABORT: crops changed = %s' % changed)
        return 2
    print('verified: exactly the 3 corrected crops changed')

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d citations repointed, %d catalog entries added, 0 values changed'
          % (len(touched), len(NEW_CATALOG)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
