#!/usr/bin/env python3
"""GUARDED PROMOTE 1 of 3: repoint strawberry's mid_south HARVEST arms at the page that backs them.

CITATION-ONLY. Not one value moves. Campaign B, hunt #1 (`mid_south`/`uada_ext`).
Companions: promote_strawberry_mid_south_z7_plant_out.py (the DATA change) and
promote_strawberry_mid_south_findings_and_notes.py (findings + reader-facing prose).

WHY THIS EXISTS AT ALL. Hunt 1 (2026-07-30) located this document, quoted it, classified strawberry
z8 CASE 1 -- and then never applied it. It proposed the catalog ids `uada_ext_berries` and
`uada_ext_fsa6103`; NEITHER was ever added, so all 12 strawberry mid_south nodes still cite the
institution root. The research was done and the promote was not.

THE DOCUMENT, re-fetched with urllib from raw bytes 2026-08-03 (98,538 bytes, sha256 b4b98b24...)
and the sentence re-extracted from the HTML before use, never from a WebFetch summary
([[webfetch-markdown-table-column-shift]]). UAEX, "Arkansas Berries -- Home Garden",
https://www.uaex.uada.edu/yard-garden/fruits-nuts/berries.aspx :

    "In Arkansas, strawberries are favorites in home gardens. The bright red, flavorful fruit are
     picked from April thru June in our state."

That one sentence is the whole basis for these four nodes, and it covers BOTH zones:

    z7 (matted-row perennial)  harvest "May 27 - Jun 24"    inside April-June  OK
    z8 (plasticulture annual)  harvest "late Apr - early Jun" inside April-June  OK

WHAT IS DELIBERATELY *NOT* TOUCHED HERE, each for a stated reason:

  bloom arms   Neither this page nor FSA6103 publishes a bloom DATE. FSA6103 gives only the
      (x2)     qualitative "Strawberries bloom very early in the spring, and the blossoms are
               easily killed by frost." Repointing cannot fix an absent quantity -- that is the
               [[harvest-start-is-not-a-published-datum]] shape. Filed as a CASE 2 finding in
               promote 3 instead; Trevor ruled 2026-08-03 to LEAVE the +14 offset rather than swap
               one unsourced model for another.
  z7 plant_out FSA6103 says "set out early in the spring, about three or four weeks before the
               average date of the last frost" -- a DIFFERENT document and a VALUE change, so it
               belongs in promote 2, not in a citation-only pass.
  z8 plant_out "planted in the fall" supports the SEASON but this page gives no dates, so the
               specific "Sep 15 - Oct 5" window is not sourced by it. Left bare deliberately.
  containers   plantings[] roots and resolved_by_zone.7/.8 carry the region's provenance anchor,
      (x4)     not a datum. A container repoint is a different question; not smuggled in here.

So this promote fixes 4 of 12 nodes and leaves 8 bare ON PURPOSE.

FOOTPRINT: 1 new source_catalog entry (`uada_ext_berries`); `uada_ext` -> `uada_ext_berries` on
exactly 4 anchoring_urls nodes, all strawberry, all mid_south, all harvest. Every other byte
identical. COMPACT preserved, no trailing newline.

    $ python3 tools/promote_strawberry_mid_south_harvest_repoint.py --dry-run
    $ python3 tools/promote_strawberry_mid_south_harvest_repoint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1'

OLD_ID = 'uada_ext'
NEW_ID = 'uada_ext_berries'
BARE = 'https://www.uaex.uada.edu'
NEW_URL = 'https://www.uaex.uada.edu/yard-garden/fruits-nuts/berries.aspx'
VERIFIED = '2026-08-03'
SLUG = 'strawberry'
REGION = 'mid_south'

# The four nodes, PINNED BY PATH. Never derived from a global "all bare uada_ext" sweep -- campaign
# A's pear abort proved a global map writes the wrong document onto the wrong cell.
TARGETS = [
    (0, 'harvest_start'),
    (0, 'harvest_end'),
    (1, 'harvest_start'),
    (1, 'harvest_end'),
]

CATALOG_ENTRY = {
    'id': NEW_ID,
    'name': 'UAEX, Arkansas Berries -- Home Garden',
    'publisher': 'University of Arkansas Division of Agriculture, Cooperative Extension Service',
    'url': NEW_URL,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': (
        'UAEX Yard & Garden home-garden berry overview for Arkansas. HARVEST WINDOW, the '
        'load-bearing sentence: "In Arkansas, strawberries are favorites in home gardens. The '
        'bright red, flavorful fruit are picked from April thru June in our state" -- backs the '
        'mid_south strawberry harvest in BOTH zones (z7 matted-row May 27 - Jun 24; z8 '
        'plasticulture late Apr - early Jun). Also describes both home-garden systems: the annual, '
        '"if special cultivars like \'Chandler\' are planted in the fall on raised beds then '
        'picked one time the following spring", and the perennial matted row, "by planting '
        'cultivars like \'Cardinal\' in the fall either on beds or in rows". Publishes NO bloom '
        'date and NO specific planting dates. NOTE it offers the annual/plasticulture system to '
        'home gardeners, which FSA6103 (uada_ext_fsa6103) declines to recommend for home gardens; '
        'the two UAEX documents genuinely differ and that tension is recorded as a finding.'
    ),
}


def arms(data):
    """The four target arm dicts, resolved by pinned path. Raises if the shape moved."""
    crop = next(c for c in data['crops'] if c['slug'] == SLUG)
    out = []
    for idx, arm in TARGETS:
        node = crop['regions'][REGION]['plantings'][idx][arm][0]
        out.append(('regions.%s.plantings[%d].%s[0]' % (REGION, idx, arm), node))
    return out


def value_fingerprint(data):
    """Every harvest VALUE field, so a citation-only promote can prove it moved none of them."""
    fp = {}
    for path, node in arms(data):
        fp[path] = {k: v for k, v in node.items()
                    if k not in ('sources', 'anchoring_urls')}
    return json.dumps(fp, ensure_ascii=False, sort_keys=True)


def bare_uada_nodes(data):
    """Count anchoring_urls nodes across the WHOLE dataset still citing the bare uada_ext root."""
    n = 0

    def walk(node):
        nonlocal n
        if isinstance(node, dict):
            a = node.get('anchoring_urls')
            if isinstance(a, dict):
                m = a.get(OLD_ID)
                if isinstance(m, dict) and m.get('url') == BARE:
                    n += 1
            for k, v in node.items():
                if k != 'anchoring_urls':
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data['crops'])
    return n


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
        print('ABORT: canonical sha %s != expected %s' % (sha[:12], args.expect_sha[:12]))
        return 1
    data = json.loads(raw.decode('utf-8'))
    before = copy.deepcopy(data)

    # ---- preflight: the catalog id must be genuinely new -------------------------------------
    if NEW_ID in data['source_catalog']:
        print('ABORT: %s already in source_catalog -- this promote has already run' % NEW_ID)
        return 1
    if OLD_ID not in data['source_catalog']:
        print('ABORT: %s missing from source_catalog; wrong base' % OLD_ID)
        return 1

    # ---- preflight: PIN THE EXACT BARE URL PER NODE ------------------------------------------
    # Campaign A drafted one reason across five crops and it was false for two, because their
    # "bare ucanr_ext" was a DIFFERENT site. Read each node's own url; never a global map.
    pinned = []
    for path, node in arms(data):
        au = node.get('anchoring_urls') or {}
        entry = au.get(OLD_ID)
        if not isinstance(entry, dict):
            print('ABORT: %s does not cite %s at all' % (path, OLD_ID))
            return 1
        url = entry.get('url')
        if url != BARE:
            print('ABORT: %s cites %r, not the bare host %r -- refusing to repoint it'
                  % (path, url, BARE))
            return 1
        if list(au) != [OLD_ID] or node.get('sources') != [OLD_ID]:
            print('ABORT: %s is not SOLE on %s (sources=%r urls=%r)'
                  % (path, OLD_ID, node.get('sources'), sorted(au)))
            return 1
        pinned.append((path, url))
    print('PINNED %d nodes, each verified to cite exactly %s:' % (len(pinned), BARE))
    for path, url in pinned:
        print('   %-52s %s' % (path, url))

    value_before = value_fingerprint(data)
    bare_before = bare_uada_nodes(data)

    # ---- the edit ----------------------------------------------------------------------------
    data['source_catalog'][NEW_ID] = copy.deepcopy(CATALOG_ENTRY)
    changed = 0
    for path, node in arms(data):
        node['sources'] = [NEW_ID]
        node['anchoring_urls'] = {NEW_ID: {'url': NEW_URL, 'verified': VERIFIED}}
        changed += 1

    # ---- guards ------------------------------------------------------------------------------
    fails = []
    if changed != 4:
        fails.append('edited %d nodes, expected exactly 4' % changed)

    cat_added = set(data['source_catalog']) - set(before['source_catalog'])
    if cat_added != {NEW_ID}:
        fails.append('catalog delta is %r, expected exactly {%r}' % (sorted(cat_added), NEW_ID))
    if data['source_catalog'][NEW_ID]['url'] != NEW_URL:
        fails.append('catalog url is not the verified document url')

    if value_fingerprint(data) != value_before:
        fails.append('A HARVEST VALUE MOVED -- this promote is citation-only')

    bare_after = bare_uada_nodes(data)
    if bare_after != bare_before - 4:
        fails.append('bare %s nodes went %d -> %d, expected a drop of exactly 4'
                     % (OLD_ID, bare_before, bare_after))

    # NOTE: a "did the edit actually set sources/url on each target" pair of checks lived here and
    # was REMOVED, not left as decoration. arms() re-resolves the same node objects the edit loop
    # just wrote, so no input can make them fail -- they were unfailable by construction. The
    # repoint is instead proven end-to-end by the bare-count guard above (91 -> 87) and by the
    # catalog-delta guard, both of which ARE mutation-tested. Campaign A removed two checks of
    # exactly this shape; a check that cannot fail is not a guard.

    # the 8 NON-harvest strawberry mid_south nodes must be untouched, bare and all
    crop_a = next(c for c in data['crops'] if c['slug'] == SLUG)['regions'][REGION]
    crop_b = next(c for c in before['crops'] if c['slug'] == SLUG)['regions'][REGION]
    for key in ('resolved_by_zone', 'plantings_provenance'):
        if json.dumps(crop_a[key], sort_keys=True) != json.dumps(crop_b[key], sort_keys=True):
            fails.append('%s changed; this promote must not touch it' % key)
    for idx in (0, 1):
        for arm in ('plant_out', 'bloom'):
            a = crop_a['plantings'][idx][arm][0]
            b = crop_b['plantings'][idx][arm][0]
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                fails.append('plantings[%d].%s changed; out of scope' % (idx, arm))

    # nothing outside strawberry may move
    for c_a, c_b in zip(data['crops'], before['crops']):
        if c_a['slug'] != SLUG:
            if json.dumps(c_a, sort_keys=True) != json.dumps(c_b, sort_keys=True):
                fails.append('crop %s changed; only %s is in scope' % (c_a['slug'], SLUG))
                break
    if len(data['crops']) != len(before['crops']):
        fails.append('crop count moved')

    if fails:
        print('\nABORT -- %d guard(s) failed:' % len(fails))
        for f in fails:
            print('   x %s' % f)
        return 1

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: output has a trailing newline; canonical is COMPACT with none')
        return 1

    print('\nALL GUARDS PASS. 4 nodes repointed %s -> %s, 1 catalog entry added.'
          % (OLD_ID, NEW_ID))
    print('   bare %s nodes dataset-wide: %d -> %d' % (OLD_ID, bare_before, bare_after))
    print('   new sha256: %s' % hashlib.sha256(out).hexdigest())
    if args.dry_run:
        print('   DRY RUN -- nothing written.')
        return 0
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('   WRITTEN to %s' % args.canonical)
    return 0


if __name__ == '__main__':
    sys.exit(main())
