#!/usr/bin/env python3
"""GUARDED PROMOTE 3 of 3: strawberry mid_south findings, the attribution correction, reader copy.

FINDINGS + PROSE. Not one date moves. Campaign B, hunt #1. Closes the strawberry pass opened by
promote 1 (harvest citations) and promote 2 (the z7 anchor re-derivation).

WHAT THIS RECORDS.

1. `strawberry_mid_south_bloom_offset_undocumented` -- the CASE 2 the hunt owed. Strawberry was
   the ONE crop in this hunt carrying bloom arms with no bloom finding at all: the roster-wide
   `mid_south_bloom_offset_undocumented` sits on 13 fruit crops and strawberry is not among them.
   Two UAEX documents were read in full and neither publishes a bloom date. Trevor ruled
   2026-08-03 to RETAIN the +14-day offset rather than swap one unsourced model for another.

2. `strawberry_mid_south_plasticulture_home_garden_tension` -- two T1 documents from the SAME
   institution disagree about whether the z8 annual system belongs in a home garden. Recorded, not
   silently resolved, because neither document is wrong.

3. THE ATTRIBUTION CORRECTION, and why it is an APPEND rather than a rewrite. `plantings_provenance`
   claims the z8 system is one "the University of Arkansas pioneered and RECOMMENDS for this belt's
   lowland South conditions". FSA6103 says the opposite for our audience: "This training system is
   not recommended for home garden strawberry production at this time." "Pioneered" is defensible
   (UAEX credits commercial growers with it); "recommends" is a fabricated attribution of the same
   class as the ten false UAEX herb credits and the cherry-sweet fabrication. The same string also
   carries "Ozark uplands/VA" and "lowland South/NC" -- Virginia and North Carolina are
   `mid_atlantic` states, not `mid_south` (AR/OK/TN/MO), which is the template's geography left in
   place by find-and-replace.

   Both are corrected by APPENDING a dated `[CORRECTION ...]` and leaving the original prose
   BYTE-FOR-BYTE, mirroring the `verification_log_ref` convention: a provenance record states what
   was believed when it was written, and rewriting it destroys the evidence that the template
   defect happened at all. The guard below pins the original substring to prove it survived.

4. THE READER-FACING NOTE (Trevor's ask: bring the bloom-frost risk to the attention of people
   actually planting there). It goes in `frost_risk_note_seasoned` on BOTH zones, which
   `BerryYearCalendarCard.astro` renders TODAY as a "Protect the blossoms" callout -- verified in
   plant-astro before writing, because a note in an unrendered field cannot inform anyone.
   `region_notes_*` would have been invisible. The copy DELIBERATELY STATES NO TEMPERATURE: FSA6103
   gives no threshold, and inventing one is fill-the-shape-is-the-defect. It also names NO
   institution, because these cells still cite a bare host.

FOOTPRINT: 2 new open_findings on strawberry; 1 appended correction to plantings_provenance; 2
rewritten frost_risk_note_seasoned strings. NO dates, NO citations, NO catalog change.

    $ python3 tools/promote_strawberry_mid_south_findings_and_notes.py --dry-run
    $ python3 tools/promote_strawberry_mid_south_findings_and_notes.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '093581673b519fa00337e61a238e99da725eaee7645c2e79d11e2c4f56ba0d51'

SLUG = 'strawberry'
REGION = 'mid_south'

# pinned original substrings -- these must SURVIVE the append, byte for byte
PIN_RECOMMENDS = 'the University of Arkansas pioneered and recommends'
PIN_VA = 'Ozark uplands/VA'

CORRECTION = (
    ' [CORRECTION 2026-08-03: two claims above are no longer asserted. (1) The University of '
    'Arkansas does NOT recommend the annual plasticulture system for HOME GARDEN production. '
    'FSA6103, Strawberry Production in the Home Garden, states "This training system is not '
    'recommended for home garden strawberry production at this time due to the susceptibility of '
    'these varieties to diseases and the need for soil fumigation." The z8 annual cycle is '
    'retained on the authority of the UAEX Arkansas Berries home-garden page, which does offer '
    'that system to home gardeners, and the disagreement between the two documents is filed as '
    'strawberry_mid_south_plasticulture_home_garden_tension. "Pioneered" stands; "recommends" was '
    'never true of the home-garden literature. (2) The state abbreviations VA and NC are '
    'mid_atlantic geography carried in from the template this region was built from; mid_south is '
    'AR/OK/TN/MO. Original prose left byte-for-byte per the verification_log_ref convention.]'
)

FINDINGS = [
    {
        'id': 'strawberry_mid_south_bloom_offset_undocumented',
        'severity': 'low',
        'status': 'accepted_modeled',
        'blocks_launch': False,
        'summary': (
            'The mid_south bloom windows are MODELED offsets from the zone last-frost date '
            '(z7 bloom[0] = {from: last_frost, offset_days: 14, window_days: 21}; z8 an absolute '
            'Mar - Apr window), not quoted data. Both UAEX strawberry documents were located and '
            'read in full this session and NEITHER publishes a bloom date: FSA6103 gives only the '
            'qualitative "Strawberries bloom very early in the spring, and the blossoms are '
            'easily killed by frost", and the Arkansas Berries home-garden page gives harvest '
            'months only. The quantity is absent from the literature for this geography, the same '
            'shape as the harvest-start-is-not-a-published-datum finding, so repointing cannot '
            'fix it and the derivation is declared instead. Trevor ruled 2026-08-03 to RETAIN the '
            '+14-day z7 offset rather than replace one unsourced model with another; FSA6103\'s '
            '"very early in the spring" is directionally earlier than a +14-day offset, but it is '
            'qualitative and cannot adjudicate a date. The practical consequence is carried to '
            'readers instead, in the frost_risk_note_seasoned callout on both zones. NOTE this '
            'crop was the one gap in the mid_south bloom ruling: '
            'mid_south_bloom_offset_undocumented covers 13 fruit crops and never included '
            'strawberry, so these two arms sat unruled until the campaign B re-price found them.'
        ),
        'basis': (
            'Documents fetched with urllib from raw bytes 2026-08-03 and every load-bearing '
            'sentence re-extracted from the raw bytes before use; no WebFetch summary was relied '
            'on. UAEX Arkansas Berries -- Home Garden (98,538 bytes, sha256 b4b98b24...); UAEX '
            'FSA6103 Strawberry Production in the Home Garden (169,561 bytes, sha256 b55b80b5..., '
            '4 pages, read with pypdf).'
        ),
    },
    {
        'id': 'strawberry_mid_south_plasticulture_home_garden_tension',
        'severity': 'low',
        'status': 'open',
        'blocks_launch': False,
        'summary': (
            'Two T1 documents from the SAME institution disagree about whether the z8 annual '
            'plasticulture system belongs in a home garden, and this dataset is home-garden '
            'facing. FSA6103, Strawberry Production in the Home Garden, says the annual hill or '
            'plasticulture system "is not recommended for home garden strawberry production at '
            'this time due to the susceptibility of these varieties to diseases and the need for '
            'soil fumigation", and recommends the matted row instead: "Use of the matted-row '
            'system is recommended for home garden production." The UAEX Arkansas Berries '
            'home-garden page offers exactly the annual system to home gardeners: strawberries '
            '"can be produced as annuals ... if special cultivars like \'Chandler\' are planted '
            'in the fall on raised beds then picked one time the following spring". The z8 cycle '
            'is RETAINED on the berries page\'s authority and nothing was re-modelled; what was '
            'removed is the claim that UAEX "recommends" the system for this belt, which the '
            'home-garden literature never said. Left open because it is a genuine disagreement '
            'between two sound documents rather than an error in either, and whether a '
            'home-garden product should model a system one of its own extension services '
            'discourages is a product call, not a sourcing one.'
        ),
        'basis': (
            'Both documents fetched with urllib from raw bytes and re-read 2026-08-03 (see '
            'strawberry_mid_south_bloom_offset_undocumented for hashes). Surfaced by the campaign '
            'B re-price while verifying hunt 1\'s CASE 1 classification of strawberry z8.'
        ),
    },
]

NOTES = {
    '7': (
        'Blossoms open very early, from late April into May, and an open blossom is easily killed '
        'by a late frost even though the plants themselves are hardy. Treat those dates as a '
        'guide rather than a schedule: they are modeled from the zone frost date, not a published '
        'bloom calendar, so watch your own forecast through bloom and throw row cover over the '
        'bed on any night frost is predicted. A frost during bloom costs you that year\'s crop, '
        'not the bed.'
    ),
    '8': (
        'Plants overwinter as small crowns under row covers, and the spring blossoms that follow '
        'are easily damaged by a hard freeze. Treat the March to April bloom window as a guide '
        'rather than a schedule: it is modeled rather than taken from a published bloom calendar, '
        'so watch your own forecast and keep row cover or other frost protection on hand for a '
        'late cold snap. A freeze during bloom costs the crop, not the planting.'
    ),
}


def region_of(data):
    crop = next(c for c in data['crops'] if c['slug'] == SLUG)
    return crop, crop['regions'][REGION]


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

    crop, region = region_of(data)
    vs = crop.setdefault('verification_status', {})
    findings = vs.setdefault('open_findings', [])

    # ---- preflight ---------------------------------------------------------------------------
    have = {f.get('id') for f in findings if isinstance(f, dict)}
    for f in FINDINGS:
        if f['id'] in have:
            print('ABORT: finding %s already filed -- promote already run' % f['id'])
            return 1
    prov = region.get('plantings_provenance')
    if not isinstance(prov, str):
        print('ABORT: plantings_provenance is %s, expected a string' % type(prov).__name__)
        return 1
    if PIN_RECOMMENDS not in prov:
        print('ABORT: the pinned "recommends" claim is not in plantings_provenance')
        return 1
    if '[CORRECTION' in prov:
        print('ABORT: plantings_provenance already carries a correction')
        return 1
    for z in NOTES:
        if not (region['resolved_by_zone'].get(z) or {}).get('frost_risk_note_seasoned'):
            print('ABORT: z%s has no frost_risk_note_seasoned to replace' % z)
            return 1

    # ---- the edit ----------------------------------------------------------------------------
    findings.extend(copy.deepcopy(FINDINGS))
    region['plantings_provenance'] = prov + CORRECTION
    for z, text in NOTES.items():
        region['resolved_by_zone'][z]['frost_risk_note_seasoned'] = text

    # ---- guards ------------------------------------------------------------------------------
    fails = []
    b_crop, b_region = region_of(before)

    ids = [f.get('id') for f in findings if isinstance(f, dict)]
    if len(ids) != len(set(ids)):
        fails.append('duplicate finding ids after append')
    added = set(ids) - {f.get('id') for f in b_crop['verification_status']['open_findings']
                        if isinstance(f, dict)}
    if added != {f['id'] for f in FINDINGS}:
        fails.append('finding delta is %r' % sorted(added))

    # the ORIGINAL provenance must survive byte-for-byte: this is an APPEND, not a rewrite
    newprov = region['plantings_provenance']
    if not newprov.startswith(b_region['plantings_provenance']):
        fails.append('plantings_provenance was REWRITTEN, not appended to')
    if PIN_RECOMMENDS not in newprov or PIN_VA not in newprov:
        fails.append('the pinned original claims did not survive the append')
    if '[CORRECTION 2026-08-03' not in newprov:
        fails.append('correction marker missing')

    # consumer-copy house rules on every string this promote writes
    written = list(NOTES.values()) + [CORRECTION] + \
        [f['summary'] for f in FINDINGS] + [f['basis'] for f in FINDINGS]
    for s in written:
        if '—' in s or '–' in s:
            fails.append('em/en dash in authored copy')
            break
    for z, text in NOTES.items():
        cur = region['resolved_by_zone'][z]['frost_risk_note_seasoned']
        if cur != text:
            fails.append('z%s note not written' % z)
        if '--' in cur:
            fails.append('z%s note contains a double hyphen' % z)
        if '°' in cur or 'degree' in cur.lower():
            fails.append('z%s note states a temperature; FSA6103 publishes no threshold' % z)
        for inst in ('University of Arkansas', 'UAEX', 'Extension'):
            if inst in cur:
                fails.append('z%s note names an institution while the cell cites a bare host' % z)
                break

    # NOTHING numeric or citational may move in a findings+prose promote
    for z in ('7', '8'):
        a, b = region['resolved_by_zone'][z], b_region['resolved_by_zone'][z]
        for k in ('plant_out', 'bloom', 'harvest', 'harvest_start', 'harvest_end', 'calendar',
                  'resolved_from', 'sources', 'anchoring_urls', 'grown_as'):
            if json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True):
                fails.append('z%s.%s changed; this promote is findings+prose only' % (z, k))
    if json.dumps(region['plantings'], sort_keys=True) != \
       json.dumps(b_region['plantings'], sort_keys=True):
        fails.append('plantings[] changed; this promote is findings+prose only')
    if json.dumps(data['source_catalog'], sort_keys=True) != \
       json.dumps(before['source_catalog'], sort_keys=True):
        fails.append('source_catalog changed; no citation work here')

    for c_a, c_b in zip(data['crops'], before['crops']):
        if c_a['slug'] != SLUG and json.dumps(c_a, sort_keys=True) != \
                json.dumps(c_b, sort_keys=True):
            fails.append('crop %s changed; only %s is in scope' % (c_a['slug'], SLUG))
            break
    for rk in region:
        if rk not in ('plantings_provenance', 'resolved_by_zone'):
            if json.dumps(region[rk], sort_keys=True) != json.dumps(b_region[rk], sort_keys=True):
                fails.append('mid_south.%s changed; out of scope' % rk)
    for rk, r in crop['regions'].items():
        if rk != REGION and json.dumps(r, sort_keys=True) != \
                json.dumps(b_crop['regions'][rk], sort_keys=True):
            fails.append('region %s changed; only %s is in scope' % (rk, REGION))
            break

    if fails:
        print('\nABORT -- %d guard(s) failed:' % len(fails))
        for f in fails:
            print('   x %s' % f)
        return 1

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: output has a trailing newline; canonical is COMPACT with none')
        return 1

    print('ALL GUARDS PASS.')
    print('   findings filed : %s' % ', '.join(f['id'] for f in FINDINGS))
    print('   provenance     : appended %d chars, original %d preserved byte-for-byte'
          % (len(CORRECTION), len(b_region['plantings_provenance'])))
    print('   reader copy    : frost_risk_note_seasoned rewritten on z7 and z8')
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
