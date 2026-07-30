#!/usr/bin/env python3
"""GUARDED PROMOTE: repoint mid_south fruit-tree bare hosts at the document that backs them.

CITATION-ONLY. Not one value moves. Companion to
tools/promote_mid_south_uada_citation_findings.py; full hunt write-up in
docs/2026-07-30-mid-south-uada-ext-citation-hunt.md.

THE DOCUMENT, and the single sentence this whole promote rests on. UAEX, "Home Garden Fruit Trees
in Arkansas" (https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx), fetched with
urllib and the sentence re-extracted from the raw HTML before use:

    "Fruit trees other than figs, could be planted in the fall, but often the best variety
     availability will be in late winter."

That supports `plant_out = "Dec - Feb (dormant, bare-root...)"` on twelve tree fruits: December
through February is late winter plus the tail of the fall option. The same page supplies two
explicit ripening windows:

    "Pawpaw fruit ripens between mid-August and into October, depending on the weather."
    "Oriental persimmons fruit ripens from late August until early December, depending on the
     variety and weather conditions."

which cover pawpaw's harvest (Sep 9 - Oct 7 / Sep 2 - Sep 30) and persimmon's (Sep 13 - Oct 18 /
Sep 6 - Oct 11). Both sit inside their document's window.

WHAT IS DELIBERATELY *NOT* REPOINTED, and why each exclusion is the point:

  fig        The SAME sentence excludes it by name, and the page says so again: "Fig trees should
             not be planted until early spring." Its Dec-Feb window is CONTRADICTED, recorded as
             mid_south_fig_dormant_planting_contradicted. Pointing it here would publish the
             contradiction.
  raspberry  FSA6107 says "Planting should occur in the spring". Same shape, own finding.
  blueberry  Its recommended_type is contradicted by three UAEX documents. Own finding.
  bloom arms NO UAEX document publishes a bloom date for any fruit crop. Recorded as
             mid_south_bloom_offset_undocumented on 13 crops. Repointing cannot fix an absent
             quantity -- that is the harvest-start-is-not-a-published-datum shape.
  pawpaw     plant_out is "Spring (potted, from container)", a container claim the page's
    plant_out bare-root/late-winter sentence does not make. Its HARVEST is repointed; its planting
             is not.
  harvest    Left on the bare host for apple (already pathed to ext_org_apples), and for apricot /
    elsewhere cherry / mulberry / peach / pear / plum / pomegranate, because UAEX publishes NO
             harvest dates for them. FSA6129 has no plum section at all and gives peach/nectarine
             only a relative "days before Elberta" ladder with no anchor date.

So this promote fixes 40 nodes and leaves the rest bare ON PURPOSE. The honest result of the hunt
is that UAEX publishes suitability, cultivar and ripening guidance but not the offset model our
schema stores, so most of these citations cannot be repointed at all.

FOOTPRINT: 1 new source_catalog entry; `uada_ext` -> `uada_ext_fruit_trees` on exactly 40
anchoring_urls nodes across 12 crops. Every other byte identical. COMPACT preserved.

    $ python3 tools/promote_mid_south_fruit_tree_repoint.py --dry-run
    $ python3 tools/promote_mid_south_fruit_tree_repoint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '14c8eab246859c63a3fc9bf68c8f8fcef9ee39f360661589d26245f5924504c3'

OLD_ID = 'uada_ext'
NEW_ID = 'uada_ext_fruit_trees'
BARE = 'https://www.uaex.uada.edu'
NEW_URL = 'https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx'
VERIFIED = '2026-07-30'

CATALOG_ENTRY = {
    'id': NEW_ID,
    'name': 'UAEX, Home Garden Fruit Trees in Arkansas',
    'publisher': 'University of Arkansas Division of Agriculture, Cooperative Extension Service',
    'url': NEW_URL,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-07',
    'tier': 'T1',
    'citable_for': (
        'UAEX Yard & Garden home fruit-tree guidance for Arkansas. Dormant-season planting: '
        '"Fruit trees other than figs, could be planted in the fall, but often the best variety '
        'availability will be in late winter" -- backs the mid_south Dec-Feb bare-root plant_out '
        'across the tree-fruit roster, and by its own exception EXCLUDES fig ("Fig trees should '
        'not be planted until early spring"). Ripening windows: pawpaw "between mid-August and '
        'into October"; oriental persimmon "from late August until early December". Also names '
        'the fire-blight-resistant apple (William\'s Pride, Enterprise) and pear (Harrow Delight, '
        'Maxine, Kiefer, Magness, Moonglow) selections for Arkansas, and states that pawpaw needs '
        'two different trees with flies and beetles as pollinators. Does NOT publish bloom dates '
        'for any crop.'),
}

# crop -> list of node selectors to repoint.
#   ('arm', field)  -> regions.mid_south.plantings[*].<field>[*]
#   ('cell',)       -> regions.mid_south.resolved_by_zone.<zone>
PLANT_OUT_CROPS = ['apple', 'apricot', 'cherry-sour', 'cherry-sweet', 'mulberry', 'nectarine',
                   'peach', 'pear-asian', 'pear-european', 'persimmon', 'plum', 'pomegranate']
HARVEST_CROPS = ['pawpaw', 'persimmon']

EXCLUDED = {'fig', 'raspberry', 'blueberry', 'strawberry', 'elderberry',
            'oregano', 'rosemary', 'sage', 'thyme'}


def _repoint(node, touched, label):
    """Swap OLD_ID -> NEW_ID in one anchoring_urls dict. Returns True if it fired."""
    au = node.get('anchoring_urls')
    if not isinstance(au, dict) or OLD_ID not in au:
        return False
    if (au[OLD_ID] or {}).get('url') != BARE:
        return False
    if NEW_ID in au:
        return False
    # rebuild preserving key order, replacing in place
    new_au = {}
    for k, v in au.items():
        if k == OLD_ID:
            new_au[NEW_ID] = {'url': NEW_URL, 'verified': VERIFIED}
        else:
            new_au[k] = v
    node['anchoring_urls'] = new_au
    srcs = node.get('sources')
    if isinstance(srcs, list) and OLD_ID in srcs:
        node['sources'] = [NEW_ID if s == OLD_ID else s for s in srcs]
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

    if NEW_ID in (data.get('source_catalog') or {}):
        print('ABORT: source_catalog already holds %s' % NEW_ID)
        return 2

    # --- preconditions: the claim each repoint asserts must still be in the cell ---
    for slug in PLANT_OUT_CROPS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        rbz = ((crop.get('regions') or {}).get('mid_south') or {}).get('resolved_by_zone') or {}
        if set(rbz) != {'7', '8'}:
            print('ABORT: %s mid_south zones are %s, expected 7+8' % (slug, sorted(rbz)))
            return 2
        for z, cell in rbz.items():
            po = cell.get('plant_out') or ''
            if not po.startswith('Dec - Feb (dormant'):
                print('ABORT: %s z%s plant_out is %r -- the document sentence backs a Dec-Feb '
                      'dormant window and nothing else' % (slug, z, po))
                return 2
    if set(PLANT_OUT_CROPS) & EXCLUDED:
        print('ABORT: an excluded crop is in the repoint set')
        return 2

    # pawpaw/persimmon harvest windows must still sit inside the document's stated ripening span
    HARVEST_OK = {
        'pawpaw': {'7': ('Sep 9', 'Oct 7'), '8': ('Sep 2', 'Sep 30')},
        'persimmon': {'7': ('Sep 13', 'Oct 18'), '8': ('Sep 6', 'Oct 11')},
    }
    for slug, zones in HARVEST_OK.items():
        rbz = crops[slug]['regions']['mid_south']['resolved_by_zone']
        for z, (hs, he) in zones.items():
            if rbz[z].get('harvest_start') != hs or rbz[z].get('harvest_end') != he:
                print('ABORT: %s z%s harvest moved (%r - %r), re-adjudicate against the document'
                      % (slug, z, rbz[z].get('harvest_start'), rbz[z].get('harvest_end')))
                return 2

    # --- apply the repoints ---
    touched = []
    for slug in PLANT_OUT_CROPS:
        ms = crops[slug]['regions']['mid_south']
        for i, arm in enumerate(ms.get('plantings') or []):
            for j, sub in enumerate(arm.get('plant_out') or []):
                _repoint(sub, touched, '%s plantings[%d].plant_out[%d]' % (slug, i, j))
        for z, cell in (ms.get('resolved_by_zone') or {}).items():
            _repoint(cell, touched, '%s resolved_by_zone.%s' % (slug, z))
    for slug in HARVEST_CROPS:
        ms = crops[slug]['regions']['mid_south']
        for i, arm in enumerate(ms.get('plantings') or []):
            for field in ('harvest_start', 'harvest_end'):
                for j, sub in enumerate(arm.get(field) or []):
                    _repoint(sub, touched, '%s plantings[%d].%s[%d]' % (slug, i, field, j))

    EXPECTED = 40
    if len(touched) != EXPECTED:
        print('ABORT: repointed %d nodes, expected exactly %d' % (len(touched), EXPECTED))
        for t in touched:
            print('    ' + t)
        return 2
    print('repointed %d nodes across %d crops:' % (len(touched), len(set(
        t.split()[0] for t in touched))))
    for t in touched:
        print('  ' + t)

    data.setdefault('source_catalog', {})[NEW_ID] = json.loads(json.dumps(CATALOG_ENTRY))

    # --- prove NOTHING but citations moved ---
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

    # the only source_catalog delta is the one new key
    cat_before = set(before.get('source_catalog') or {})
    cat_after = set(data.get('source_catalog') or {})
    if cat_after - cat_before != {NEW_ID} or cat_before - cat_after:
        print('ABORT: unexpected source_catalog delta')
        return 2
    for k in cat_before:
        if before['source_catalog'][k] != data['source_catalog'][k]:
            print('ABORT: existing catalog entry %s mutated' % k)
            return 2
    print('verified: source_catalog gained exactly 1 entry, none mutated')

    # no bare uada_ext survives on a node we claimed to fix
    for slug in PLANT_OUT_CROPS:
        for z, cell in crops[slug]['regions']['mid_south']['resolved_by_zone'].items():
            au = cell.get('anchoring_urls') or {}
            if (au.get(OLD_ID) or {}).get('url') == BARE:
                print('ABORT: %s z%s still carries the bare host' % (slug, z))
                return 2
    print('verified: no bare host survives on a repointed cell')

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d citations repointed, 1 catalog entry added, 0 values changed'
          % len(touched))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
