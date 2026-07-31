#!/usr/bin/env python3
"""GUARDED PROMOTE: lifted zone rows tell the reader they are in the DONOR zone.

Trevor-ruled 2026-07-31: "I don't want anything reader visible being incorrect."

THE DEFECT. `tools/build_zonespan_widen_patch.py` reconciled five warm regions to the 2023 USDA
map by `copy.deepcopy`-ing a donor zone's `resolved_by_zone` row onto the new zone label and
stamping `lifted_from_zone`. That was the right DATA call -- the map moved the cities the regions
were authored for, so the row genuinely is that city's data, and the marker records the lift
honestly. But the pass never rewrote the PROSE. 106 consumer-facing strings across 66 cells and
15 crops therefore name the donor's zone: a `ca_south_coast` z11 gardener reads "Zone 10 on the
south coast almost never freezes", and a Hawaii z13 gardener reads "Zone 11 in Hawaii".

The affected (region, zone) pairs are exactly the ones that pass had to add -- the zones carried
by 113 crops rather than 120: ca_south_coast z11, ca_desert z11, hawaii_tropical z10/z12/z13,
low_desert_az z10, se_gulf z10.

DE-ZONING, NOT RENUMBERING, and that is a correctness call:
  * Renumbering would assert zone-specific claims we cannot source. The clearest case is
    mandarin's `ca_south_coast` cell, which names the Ojai Pixie: Ojai is not zone 11.
  * De-zoning is safe for every NUMBER in the copy because each donor->lifted pair carries an
    IDENTICAL `region_chill_delivered` band (low_desert_az 9/10 [100,400]; ca_south_coast 10/11
    [50,350]; ca_desert 10/11 [100,300]; hawaii_tropical 10-13 [0,150]; se_gulf 9/10 [350,650]).
    Checked before authoring; the guards below re-assert the figures survive.

SCOPE. Prose only, and only on rows carrying `lifted_from_zone`. No suitability, no date, no
calendar, no citation, no `lifted_from_zone` marker, and no non-lifted row moves. A wrong zone
label on a row the widen never touched is a DIFFERENT defect needing its own ruling.

    $ python3 tools/promote_dezone_lifted_prose.py --dry-run
    $ python3 tools/promote_dezone_lifted_prose.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import dezone_lifted_prose as dz  # noqa: E402

CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '8d2b1a91eea725e66cd6317a4a5a395f0db3b3302fb93e4994262c3e6d42b289'

EXPECTED_STRINGS = 106
EXPECTED_CELLS = 66
EXPECTED_CROPS = 15

# The (region, zone) pairs the zone-span widen added. Nothing outside this set may move.
EXPECTED_REGION_ZONES = {
    ('ca_south_coast', '11'), ('ca_desert', '11'),
    ('hawaii_tropical', '10'), ('hawaii_tropical', '12'), ('hawaii_tropical', '13'),
    ('low_desert_az', '10'), ('se_gulf', '10'),
}

# Chill figures that MUST survive verbatim -- they are the reason de-zoning is safe at all.
CHILL_WITNESSES = [
    ('plum', 'ca_desert', '11', 'about 100 to 300 hours'),
    ('plum', 'ca_south_coast', '11', 'roughly 50 to 350 hours'),
    ('plum', 'hawaii_tropical', '12', '0 to 150 hours'),
    ('persimmon', 'ca_south_coast', '11', 'about 50 to 350 hours'),
    ('persimmon', 'low_desert_az', '10', 'roughly 100 to 400 chill hours'),
    ('peach', 'low_desert_az', '10', 'about 300 to 400 chill hours'),
    ('nectarine', 'low_desert_az', '10', 'about 300 to 400 chill hours'),
    ('orange-navel', 'se_gulf', '10', 'below 27°F'),
]


def _fail(msg):
    print('ABORT: %s' % msg)
    return 2


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
        return _fail('canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)

    # ---- preflight: the defect set is exactly what was measured ---------------
    defects = dz.find_defects(data)
    cells = {(d.slug, d.region, d.zone) for d in defects}
    crops_hit = {d.slug for d in defects}
    if len(defects) != EXPECTED_STRINGS:
        return _fail('expected %d defect strings, found %d' % (EXPECTED_STRINGS, len(defects)))
    if len(cells) != EXPECTED_CELLS:
        return _fail('expected %d cells, found %d' % (EXPECTED_CELLS, len(cells)))
    if len(crops_hit) != EXPECTED_CROPS:
        return _fail('expected %d crops, found %d' % (EXPECTED_CROPS, len(crops_hit)))
    rz = {(d.region, d.zone) for d in defects}
    if rz != EXPECTED_REGION_ZONES:
        return _fail('region/zone set is %s, expected %s'
                     % (sorted(rz), sorted(EXPECTED_REGION_ZONES)))
    unruled = [d for d in defects if dz.rewrite(d.text) is None]
    if unruled:
        return _fail('%d strings have no rewrite rule, e.g. %s'
                     % (len(unruled), unruled[0].text[:90]))
    print('verified: %d strings / %d cells / %d crops, all on lifted rows, all covered by a rule'
          % (len(defects), len(cells), len(crops_hit)))

    # ---- apply ---------------------------------------------------------------
    dz.apply(data)

    # ---- the defect is gone, and did not move somewhere else -----------------
    if dz.find_defects(data):
        return _fail('%d defects remain after the pass' % len(dz.find_defects(data)))

    # ---- footprint: ONLY the 106 target strings moved ------------------------
    moved = []

    def walk(a, b, path):
        if isinstance(a, dict):
            if set(a) != set(b):
                moved.append(('KEYSET', path))
                return
            for k in a:
                walk(a[k], b[k], '%s.%s' % (path, k))
        elif isinstance(a, list):
            if len(a) != len(b):
                moved.append(('LEN', path))
                return
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, '%s[%d]' % (path, i))
        elif a != b:
            moved.append(('VALUE', path))

    walk(before, data, '$')
    if len(moved) != EXPECTED_STRINGS:
        return _fail('expected exactly %d changed values, got %d (first: %s)'
                     % (EXPECTED_STRINGS, len(moved), moved[:3]))
    for kind, path in moved:
        if kind != 'VALUE':
            return _fail('structural change at %s' % path)
        if '.resolved_by_zone.' not in path:
            return _fail('change outside resolved_by_zone: %s' % path)
        if not path.endswith(('_seasoned', '_beginner')):
            return _fail('change on a non-prose key: %s' % path)

    # ---- every non-prose key, the lift marker, and non-lifted rows are frozen -
    for i, crop in enumerate(before['crops']):
        for region, rv in (crop.get('regions') or {}).items():
            for zone, cell in ((rv or {}).get('resolved_by_zone') or {}).items():
                if not isinstance(cell, dict):
                    continue
                new = data['crops'][i]['regions'][region]['resolved_by_zone'][zone]
                if 'lifted_from_zone' not in cell:
                    if cell != new:
                        return _fail('non-lifted row moved: %s/%s/z%s'
                                     % (crop['slug'], region, zone))
                    continue
                if cell.get('lifted_from_zone') != new.get('lifted_from_zone'):
                    return _fail('lift marker changed on %s/%s/z%s'
                                 % (crop['slug'], region, zone))
                for k, v in cell.items():
                    if k.endswith(('_seasoned', '_beginner')):
                        continue
                    if v != new[k]:
                        return _fail('non-prose key %s moved on %s/%s/z%s'
                                     % (k, crop['slug'], region, zone))

    # ---- the numbers that justify de-zoning must still be there --------------
    idx = {c['slug']: c for c in data['crops']}
    for slug, region, zone, figure in CHILL_WITNESSES:
        cell = idx[slug]['regions'][region]['resolved_by_zone'][zone]
        blob = ' '.join(v for k, v in cell.items()
                        if isinstance(v, str) and k.endswith(('_seasoned', '_beginner')))
        if figure not in blob:
            return _fail('%s/%s/z%s lost the figure %r' % (slug, region, zone, figure))
    print('verified: %d chill/temperature witnesses survive verbatim' % len(CHILL_WITNESSES))

    # ---- consumer-copy rules on every string we touched ----------------------
    for _kind, path in moved:
        node, parts = data, path[2:].split('.')
        for p in parts:
            while '[' in p:
                head, _, rest = p.partition('[')
                if head:
                    node = node[head]
                p = rest.rstrip(']')
                node = node[int(p)] if p.isdigit() else node
                p = ''
            if p:
                node = node[p]
        if not isinstance(node, str):
            return _fail('changed value at %s is not a string' % path)
        for bad in ('—', '--', ' degrees'):
            if bad in node:
                return _fail('consumer-copy violation %r at %s' % (bad, path))

    # ---- top-level keys frozen ----------------------------------------------
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            return _fail('top-level %s changed' % k)
    print('verified: footprint is exactly %d prose strings on %d crops; every other key frozen'
          % (len(moved), len(crops_hit)))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        return _fail('trailing newline introduced')
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d prose strings de-zoned across %d crops' % (len(moved), len(crops_hit)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
