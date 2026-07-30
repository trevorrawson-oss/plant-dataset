#!/usr/bin/env python3
"""GUARDED PROMOTE: get mid_atlantic fruit off a VEGETABLE guide and onto the tree-fruit handbook.

CITATIONS + FINDINGS. ZERO value changes -- the guards prove it.

THE DEFECT. `vce_426_331` is catalogued only as "Virginia Cooperative Extension Publication
426-331. Mid-Atlantic regional coverage". Fetched and read, it is *Virginia's Home Garden
**VEGETABLE** Planting Guide*: bean 12, lettuce 8, tomato 4, and cherry / apple / peach / pear /
plum / apricot / persimmon / blueberry / raspberry / strawberry ALL ZERO. It is the SOLE source on
19 fruit nodes carrying plant_out, harvest, bloom and suitability. Invisible to every existing
check -- the url is PATHED (so not a bare host), returns 200 (so healthy), and a source IS cited
(so anchoring passes). Found by tools/doc_mentions_crop_scan.py.

THE DOCUMENT IT SHOULD REST ON, located and read this session: the NC State Extension Gardener
Handbook, ch. 15 "Tree Fruit and Nuts".

  PLANTING, verbatim: "The best time to plant a fruit or nut tree in North Carolina is late fall
  or early winter. When trees are planted in the fall, the roots grow through the winter..."
  -> supports `Dec - Feb (dormant, bare-root)` on every tree fruit here. Note this is the
  OPPOSITE of Arkansas, where UAEX puts it in late winter and excludes fig -- the same template
  is correct in one region and wrong in the other, which is why the mid_south fix was scoped to
  mid_south.

  HARVEST, Table 5 "APPROXIMATE HARVEST DATES", parsed from real <td> cells (never flattened
  text -- HTML tables column-shift):
      apple Aug-Nov | fig Jun-Aug | pawpaw "August to September or to first frost"
      peach Jun-Aug | pears (Asian + European) Aug-Oct | persimmon Sep-Nov | plum Jun-Aug
  Our windows sit inside every one of those.

TWO NUANCES, DECLARED RATHER THAN GLOSSED (both would have been easy to "fix" wrongly):

  nectarine  Table 5 says May-Jul; ours runs to Aug 20 (z7) / Aug 10 (z8). The column header is
             "APPROXIMATE", and the same table gives PEACH Jun-Aug -- nectarine IS a peach
             (Prunus persica var. nucipersica), so a nectarine running into August is coherent.
             DIVERGENT on an approximate source, not a defect. Recorded.
  mulberry   Table 5's row is "Mulberry, RED" -- Morus rubra, the native species. NONE of our
             canonical varieties is red mulberry: Illinois Everbearing, Dwarf Everbearing, Silk
             Hope, Pakistan, Black Beauty and Oscar are everbearing hybrids and M. nigra, which
             fruit over a long season. Trimming our Jun-Jul window to the row's "May to June"
             would have made it WRONG for every variety we recommend. Row does not govern.
             Recorded.

BLOOM ARMS ARE NOT REPOINTED. The handbook carries 31 bloom mentions and NOT ONE bloom date (its
only month near "bloom" is about pruning in February). That independently reproduces hunt 1's
largest finding at a SECOND institution: the extension literature does not publish bloom dates for
fruit crops. Repointing cannot fix an absent quantity, so it is declared instead.

FOOTPRINT: 1 new catalog entry; vce_426_331 / bare ncsu_ext -> ncsu_ext_handbook_tree_fruit on the
non-bloom nodes of 10 crops; 12 findings. No value moves.

    $ python3 tools/promote_mid_atlantic_handbook_repoint.py --dry-run
    $ python3 tools/promote_mid_atlantic_handbook_repoint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'eb5926edf5e1d75c56ef2f1469bfd1c5cd484c388cb94fc71eb18f9fa8669516'

NEW_ID = 'ncsu_ext_handbook_tree_fruit'
NEW_URL = 'https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts'
VEG_URL = 'https://www.pubs.ext.vt.edu/426/426-331/426-331.html'
BARE_NCSU = 'https://content.ces.ncsu.edu'
VERIFIED = '2026-07-30'

# crops the handbook NAMES. apricot / cherry-sour / cherry-sweet / pomegranate are deliberately
# excluded: the handbook mentions apricot and cherry only in passing risk language and never
# names pomegranate, so repointing them would repeat the generic-basis weakness recorded on
# mid_south's apricot / mulberry / pomegranate.
CROPS = ['apple', 'fig', 'mulberry', 'nectarine', 'pawpaw', 'peach',
         'pear-asian', 'pear-european', 'persimmon', 'plum']

CATALOG = {
    'id': NEW_ID,
    'name': 'NC State Extension Gardener Handbook, ch. 15: Tree Fruit and Nuts',
    'publisher': 'North Carolina State Extension, NC State University',
    'url': NEW_URL,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-07',
    'tier': 'T1',
    'citable_for': (
        'NC State Extension Gardener Handbook chapter 15 (Tree Fruit and Nuts). PLANTING TIME: '
        '"The best time to plant a fruit or nut tree in North Carolina is late fall or early '
        'winter. When trees are planted in the fall, the roots grow through the winter, resulting '
        'in greater tree growth during the first season" -- backs the mid_atlantic Dec-Feb '
        'dormant bare-root window across the tree-fruit roster. HARVEST: Table 5, "Approximate '
        'harvest dates", gives apples August to November, figs June to August, red mulberry May '
        'to June, nectarines May to July, pawpaw "August to September or to first frost", peaches '
        'June to August, Asian and European pears August to October, persimmons September to '
        'November, plums June to August, plus years-to-harvest and ripeness indicators per crop. '
        'SUITABILITY: recommends apples, chestnuts, figs, pears, pecans, persimmons and plums for '
        'eastern and central North Carolina, and states that "apricot and cherry trees grow in '
        'certain areas where the climate is favorable, but need careful management and will not '
        'consistently bear fruit". Publishes NO bloom dates for any crop.'),
}

BLOOM_FINDING = {
    'id': 'mid_atlantic_bloom_offset_undocumented',
    'severity': 'low',
    'status': 'accepted_modeled',
    'blocks_launch': False,
    'summary': (
        'The mid_atlantic bloom window is a MODELED offset from the zone last-frost date, not a '
        'quoted datum. The NC State Extension Gardener Handbook chapter 15 was located and read '
        'in full this session and publishes NO bloom date for any fruit crop: it carries 31 '
        'mentions of bloom, all of them risk or management language ("any warm period during the '
        'remainder of the winter will cause the tree to bloom prematurely"), and the only month '
        'appearing near bloom refers to pruning in February. This independently reproduces the '
        'same finding at a second institution after UAEX, so the quantity appears simply not to '
        'be published for this geography -- the harvest-start-is-not-a-published-datum shape. '
        'Repointing cannot fix an absent quantity; the derivation is declared instead.'),
    'basis': 'tools/doc_mentions_crop_scan.py + full read of the handbook, 2026-07-30. See '
             'docs/2026-07-30-mid-south-uada-ext-citation-hunt.md.',
}

EXTRA_FINDINGS = {
    'nectarine': {
        'id': 'mid_atlantic_nectarine_harvest_divergent',
        'severity': 'low',
        'status': 'accepted_modeled',
        'blocks_launch': False,
        'summary': (
            'The mid_atlantic harvest window (Jul 5 - Aug 20 in zone 7, Jun 25 - Aug 10 in zone '
            '8) runs past the NC State handbook Table 5 row for nectarines, which gives "May to '
            'July". Left unchanged, deliberately: that column is headed "APPROXIMATE harvest '
            'dates", and the SAME table gives peaches "June to August" while nectarine is '
            'botanically a peach (Prunus persica var. nucipersica), so a nectarine ripening into '
            'August is coherent with the document read as a whole. Recorded as a divergence '
            'against an approximate source rather than treated as a defect.'),
        'basis': 'NC State Extension Gardener Handbook ch. 15, Table 5, parsed from table cells '
                 '2026-07-30.',
    },
    'mulberry': {
        'id': 'mid_atlantic_mulberry_table_row_species_scoped',
        'severity': 'low',
        'status': 'accepted_modeled',
        'blocks_launch': False,
        'summary': (
            'The NC State handbook Table 5 row that looks applicable here is "Mulberry, RED" '
            '(Morus rubra, the native species) and gives "May to June", a month earlier than our '
            'window (Jun 7 - Jul 27 in zone 7, May 31 - Jul 20 in zone 8). The row does NOT '
            'govern this crop: none of the canonical varieties is red mulberry. Illinois '
            'Everbearing, Dwarf Everbearing, Silk Hope and Oscar are everbearing M. alba x rubra '
            'hybrids, Black Beauty is M. nigra and Pakistan is a long-fruited type, all of which '
            'crop over an extended season rather than the native species\' short May-June window. '
            'Trimming to the row would have made the cell wrong for every variety we recommend. '
            'Left unchanged; the species mismatch is recorded so the row is not "fixed" later.'),
        'basis': 'NC State Extension Gardener Handbook ch. 15, Table 5, against this crop\'s own '
                 'canonical variety list, 2026-07-30.',
    },
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
    cat = data.setdefault('source_catalog', {})
    if NEW_ID in cat:
        print('ABORT: source_catalog already holds %s' % NEW_ID)
        return 2

    # preconditions: the plant_out claim the handbook backs must still be the Dec-Feb dormant one
    for slug in CROPS:
        if slug not in crops:
            print('ABORT: crop %s absent' % slug)
            return 2
        ma = (crops[slug].get('regions') or {}).get('mid_atlantic')
        if not ma:
            print('ABORT: %s has no mid_atlantic' % slug)
            return 2
        for z, cell in (ma.get('resolved_by_zone') or {}).items():
            po = cell.get('plant_out') or ''
            if slug == 'pawpaw':
                continue                      # container/spring claim, different shape
            if not po.startswith('Dec - Feb'):
                print('ABORT: %s z%s plant_out is %r -- the handbook backs a late fall/early '
                      'winter dormant window and nothing else' % (slug, z, po))
                return 2

    touched = []

    def repoint(node, label):
        au = node.get('anchoring_urls')
        if not isinstance(au, dict):
            return
        for sid, v in list(au.items()):
            u = v.get('url') if isinstance(v, dict) else v
            if u in (VEG_URL, BARE_NCSU):
                if NEW_ID in au and sid != NEW_ID:
                    del au[sid]
                else:
                    au[NEW_ID] = {'url': NEW_URL, 'verified': VERIFIED}
                    if sid != NEW_ID:
                        del au[sid]
                srcs = node.get('sources')
                if isinstance(srcs, list):
                    node['sources'] = sorted({NEW_ID if s == sid else s for s in srcs})
                touched.append(label)
                return

    for slug in CROPS:
        ma = crops[slug]['regions']['mid_atlantic']
        for i, arm in enumerate(ma.get('plantings') or []):
            repoint(arm, '%s plantings[%d]' % (slug, i))
            for field in ('plant_out', 'harvest_start', 'harvest_end'):
                for j, sub in enumerate(arm.get(field) or []):
                    if isinstance(sub, dict):
                        repoint(sub, '%s plantings[%d].%s[%d]' % (slug, i, field, j))
            # bloom[] deliberately skipped: the handbook publishes no bloom dates
        for z, cell in (ma.get('resolved_by_zone') or {}).items():
            repoint(cell, '%s resolved_by_zone.%s' % (slug, z))

    if not touched:
        print('ABORT: nothing repointed')
        return 2
    cat[NEW_ID] = json.loads(json.dumps(CATALOG))

    # bloom arms must remain un-repointed
    for slug in CROPS:
        for arm in crops[slug]['regions']['mid_atlantic'].get('plantings') or []:
            for b in arm.get('bloom') or []:
                if isinstance(b, dict) and NEW_ID in (b.get('anchoring_urls') or {}):
                    print('ABORT: %s bloom arm was repointed; the handbook has no bloom dates'
                          % slug)
                    return 2
    print('verified: no bloom arm repointed')

    # findings
    findings = 0
    for slug in CROPS:
        vs = crops[slug].setdefault('verification_status', {})
        ofs = vs.setdefault('open_findings', [])
        if any(isinstance(f, dict) and f.get('id') == BLOOM_FINDING['id'] for f in ofs):
            print('ABORT: bloom finding already on %s' % slug)
            return 2
        ofs.append(json.loads(json.dumps(BLOOM_FINDING)))
        findings += 1
        if slug in EXTRA_FINDINGS:
            ofs.append(json.loads(json.dumps(EXTRA_FINDINGS[slug])))
            findings += 1

    # prove no value moved
    stray = []

    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in set(a) | set(b):
                if k in ('anchoring_urls', 'sources', 'open_findings'):
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
        print('ABORT: %d value change(s): %s' % (len(stray), stray[:8]))
        return 2
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s' % changed)
        return 2
    print('verified: ZERO value changes; exactly the %d intended crops' % len(changed))
    print('repointed %d nodes, %d findings added' % (len(touched), findings))
    for t in touched:
        print('   ' + t)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d citations repointed, %d findings, 1 catalog entry, 0 values changed'
          % (len(touched), findings))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
