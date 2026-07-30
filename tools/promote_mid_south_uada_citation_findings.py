#!/usr/bin/env python3
"""GUARDED PROMOTE: surface what the mid_south / uada_ext document hunt found. NO VALUE CHANGES.

Full write-up: docs/2026-07-30-mid-south-uada-ext-citation-hunt.md

The hunt located nine UAEX documents that were recorded nowhere in the dataset (the region built a
VEGETABLE citation vocabulary in 2026-07-20 and the fruit crops need a different publication set).
Reading them supported 13 crops -- and contradicted three, raised a ruling question on a fourth,
and exposed one gap shared by thirteen.

THIS SCRIPT RECORDS ONLY. Every contradiction below is a DATA change, and the arc's rule is that a
value change and a citation change never ride in one promote -- so the values stay exactly as they
are and Trevor decides. The companion citation-only repoint is a separate script.

  1. blueberry  CONTRADICTED, both zones (z7 worse). z7 is the Ozark uplands -- "NW AR Ozarks
     (Fayetteville)" per the region's own sourcing note -- and recommends RABBITEYE while saying
     "Northern highbush is heat-stressed here and is not recommended". THREE UAEX documents say the
     opposite: FSA-6104 ("The northern highbush type is better adapted to the northern part of the
     state"; northern highbush at HIGHER elevations, rabbiteye at LOWER), FSA-6130 (section headers
     "Northern Highbush (Northern and Central Ark.)" vs "Rabbiteye (Central and Southern Ark.)"),
     and berries.aspx ("northern highbush blueberries are grown in the northern counties, and
     rabbiteyes are grown in more central and southern areas"). Chill corroborates UAEX, not the
     cell: z7 banks [1000,1300] and FSA-6130 puts northern-highbush cultivars at 700-1200.

  2. fig  CONTRADICTED, both zones. plant_out "Dec - Feb (dormant plant)" against fruit-trees.aspx
     "Fig trees should not be planted until early spring" -- and the same page's carve-out, "Fruit
     trees OTHER THAN FIGS, could be planted in the fall". The exception is stated in the very
     sentence that licenses the rule for fig's twelve siblings.

  3. raspberry  CONTRADICTED, both zones. plant_out "December to March" against FSA-6107
     "Planting should occur in the spring as soon as the soil can be properly prepared."

     2 and 3 are ONE authoring shape: the build applied a single dormant-season woody-planting
     template to all woody fruit. UAEX endorses it for tree fruit and documents exactly two
     exceptions on this roster -- fig and raspberry -- and both were missed.

  4. cherry-sour  RULING NEEDED, not a defect call I get to make. FSA-6129: "both apricots and
     cherries trees can be grown but will not reliably set fruit". apricot and cherry-sweet are
     already `marginal` (SUPPORTED); cherry-sour is `fruits_reliably`. But mid_south_sources.md
     section 6 records Trevor's 2026-07-20 call that sour cherry STAYS fruits_reliably, carried
     from mid-Atlantic where NC State steers z8 growers TOWARD sour cherry. Two land-grants
     disagree and a ruling is already on the record.

  5. bloom offsets  UNDOCUMENTED on 13 tree fruits. Every bloom[0] arm is
     {from: last_frost, offset_days: -7..+21, window_days: 21} cited SOLE to the bare host, and NO
     UAEX document read this session publishes a bloom date for any fruit crop -- FSA-6129 treats
     bloom only as relative risk language ("tend to bloom early", "Late blooming"). Same shape as
     harvest-start-is-not-a-published-datum. Repointing cannot fix it; declaring it can. apple is
     EXCLUDED: its bloom arm already cites a pathed ext_org_apples URL.

FOOTPRINT: exactly one open_finding appended per (crop, finding). ZERO value changes -- the script
proves nothing outside open_findings moved. COMPACT preserved.

    $ python3 tools/promote_mid_south_uada_citation_findings.py --dry-run
    $ python3 tools/promote_mid_south_uada_citation_findings.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '13d42f95413034636325ff14abb5346d6e044f61ddf313948ff49cdfb82fcda7'

DOC = 'docs/2026-07-30-mid-south-uada-ext-citation-hunt.md'

_METHOD = (
    'Documents fetched with urllib and read with pypdf or from raw HTML this session (2026-07-30); '
    'no WebFetch summary was used as evidence, and every load-bearing sentence was re-extracted '
    'from the raw bytes before being relied on. Full adjudication in ' + DOC + '.')

# crops carrying an undocumented bloom offset on mid_south. apple excluded: its bloom arm
# already cites a pathed ext_org_apples url.
BLOOM_CROPS = ['apricot', 'cherry-sour', 'cherry-sweet', 'fig', 'mulberry', 'nectarine',
               'pawpaw', 'peach', 'pear-asian', 'pear-european', 'persimmon', 'plum',
               'pomegranate']

BLOOM_FINDING = {
    'id': 'mid_south_bloom_offset_undocumented',
    'severity': 'low',
    'status': 'accepted_modeled',
    'blocks_launch': False,
    'summary': (
        'The mid_south bloom window is a MODELED offset from the zone last-frost date '
        '(bloom[0] = {from: last_frost, offset_days, window_days: 21}), not a quoted datum. The '
        'UAEX fruit publication set was located and read in full this session (FSA6129 Tree Fruit '
        'Cultivar Recommendations, FSA6130 Small Fruit Cultivar Recommendations, the Home Garden '
        'Fruit Trees page, and the Reference Desk fruit pages) and NONE of them publishes a bloom '
        'date for any fruit crop: FSA6129 refers to bloom only as relative risk language ("tend '
        'to bloom early", "Late blooming", "blooms relatively late"). The quantity is absent from '
        'the literature for this geography, the same shape as the harvest-start-is-not-a-'
        'published-datum finding, so repointing cannot fix it and the derivation is declared '
        'instead. The offset itself is defensible and internally consistent across the roster.'),
    'basis': _METHOD,
}

FINDINGS = {
    'blueberry': {
        'id': 'mid_south_blueberry_recommended_type_inverted',
        'severity': 'medium',
        'status': 'open',
        'blocks_launch': False,
        'summary': (
            'CONTRADICTED by the citing institution, both zones, worst in z7. The z7 cell (the '
            'Ozark uplands: the region sourcing note defines z7 as "NW AR Ozarks (Fayetteville, '
            'the U of A chill station)") sets recommended_type "rabbiteye" and states "Northern '
            'highbush is heat-stressed here and is not recommended". THREE University of Arkansas '
            'documents place the types the other way round. FSA6104 Blueberry Production in the '
            'Home Garden: "The northern highbush type is better adapted to the northern part of '
            'the state", and "northern highbush varieties can be grown at higher elevations, '
            'while southern highbush or rabbiteye varieties should be grown at lower elevations '
            'in central Arkansas". FSA6130 Small Fruit Cultivar Recommendations uses explicit '
            'region headers: "Northern Highbush (Northern and Central Ark.)" against "Rabbiteye '
            '(Central and Southern Ark.)". The UAEX Arkansas Berries page: "In Arkansas, northern '
            'highbush blueberries are grown in the northern counties, and rabbiteyes are grown in '
            'more central and southern areas." So z7 recommends the type UAEX assigns to the '
            'opposite end of the state and rules out the type UAEX assigns to z7. The belt chill '
            'band corroborates UAEX rather than the cell: z7 is [1000, 1300] hours and FSA6130 '
            'puts the northern-highbush cultivars at 700 to 1200 hours, comfortably cleared. z8 '
            'is milder: rabbiteye is right for central Arkansas, but the z8 note\'s categorical '
            '"northern highbush is too heat-stressed to recommend here" is still contradicted, '
            'because FSA6130 lists Northern Highbush for "Northern and CENTRAL Ark.". NOT '
            'repointed: pointing this cell at FSA6104 would make the contradiction visible on the '
            'page. A variety-selection steer is long-lived for a home grower, so this is a data '
            'decision for Trevor, not a citation fix.'),
        'basis': _METHOD,
    },
    'fig': {
        'id': 'mid_south_fig_dormant_planting_contradicted',
        'severity': 'medium',
        'status': 'open',
        'blocks_launch': False,
        'summary': (
            'CONTRADICTED by the citing institution, both zones. plant_out is "Dec - Feb (dormant '
            'plant)" while the UAEX Home Garden Fruit Trees page states "Fig trees should not be '
            'planted until early spring." The same page carves figs out of the rule that supports '
            'every other mid_south tree fruit: "Fruit trees other than figs, could be planted in '
            'the fall, but often the best variety availability will be in late winter." The '
            'exception is stated in the very sentence that licenses the dormant window for fig\'s '
            'twelve siblings. This is not a provenance nicety: fig is the most cold-tender woody '
            'fruit on the mid_south roster and a December planting in z7 is the failure mode the '
            'document is warning about. Value left unchanged pending Trevor; a citation change '
            'and a value change do not ride in one promote.'),
        'basis': _METHOD,
    },
    'raspberry': {
        'id': 'mid_south_raspberry_dormant_planting_contradicted',
        'severity': 'medium',
        'status': 'open',
        'blocks_launch': False,
        'summary': (
            'CONTRADICTED by the citing institution, both zones. plant_out is "December to March" '
            'while UAEX FSA6107 Raspberry Production in the Home Garden states "Planting should '
            'occur in the spring as soon as the soil can be properly prepared." December through '
            'February sit outside that; March is defensible. This is the same authoring shape as '
            'the fig finding: the mid_south build applied one dormant-season woody-planting '
            'template across all woody fruit, and UAEX endorses that template for tree fruit '
            'while documenting exactly two exceptions on this roster, fig and raspberry. Both '
            'were missed. Value left unchanged pending Trevor.'),
        'basis': _METHOD,
    },
    'cherry-sour': {
        'id': 'mid_south_cherry_sour_suitability_ruling_needed',
        'severity': 'low',
        'status': 'open',
        'blocks_launch': False,
        'summary': (
            'RULING NEEDED, deliberately not adjudicated here. UAEX FSA6129 Tree Fruit Cultivar '
            'Recommendations states: "Given the climate in Arkansas, both apricots and cherries '
            'trees can be grown but will not reliably set fruit. Both crops tend to bloom early '
            'and be exposed to frost or freeze damage during bloom. In the case of cherries, '
            'heavy rainfall common in our region during fruit ripening will result in fruit '
            'splitting prior to harvest." It says "cherries" without qualification, gives NO '
            'cherry cultivar table at all (unlike apples, pears, peaches and nectarines), and '
            'both stated mechanisms apply to sour cherry. On that reading mid_south cherry-sour '
            'suitability "fruits_reliably" is contradicted, while apricot and cherry-sweet '
            '"marginal" are supported by the same sentence. HOWEVER '
            'docs/reviews/notes/2026-07-20/mid_south_sources.md section 6 records Trevor\'s '
            '2026-07-20 call that sour cherry STAYS fruits_reliably, carried from mid_atlantic '
            'where NC State steers zone 8 growers specifically TOWARD sour cherry. Two land-grant '
            'institutions point opposite ways and a ruling is already on the record, so this is '
            'surfaced rather than changed.'),
        'basis': _METHOD,
    },
}

# RE-VERIFY guards: the defect each finding describes must still be in the data.
# (crop, zone) -> callable(cell) -> bool


def _blueberry_ok(cell):
    return (cell.get('recommended_type') == 'rabbiteye'
            and 'not recommended' in (cell.get('type_note_seasoned') or ''))


def _blueberry_z8_ok(cell):
    return (cell.get('recommended_type') == 'rabbiteye'
            and 'heat-stressed' in (cell.get('type_note_seasoned') or ''))


PRECONDITIONS = {
    'blueberry': [('7', _blueberry_ok), ('8', _blueberry_z8_ok)],
    'fig': [('7', lambda c: (c.get('plant_out') or '').startswith('Dec - Feb')),
            ('8', lambda c: (c.get('plant_out') or '').startswith('Dec - Feb'))],
    'raspberry': [('7', lambda c: c.get('plant_out') == 'December to March'),
                  ('8', lambda c: c.get('plant_out') == 'December to March')],
    'cherry-sour': [('7', lambda c: c.get('suitability') == 'fruits_reliably'),
                    ('8', lambda c: c.get('suitability') == 'fruits_reliably')],
}


def _bloom_arm_is_sole_bare(crop):
    """The crop's mid_south bloom[0] arm must cite ONLY the bare uada_ext host."""
    ms = (crop.get('regions') or {}).get('mid_south') or {}
    for arm in ms.get('plantings') or []:
        for b in arm.get('bloom') or []:
            au = b.get('anchoring_urls') or {}
            if set(au) == {'uada_ext'} and au['uada_ext'].get('url') == 'https://www.uaex.uada.edu':
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON, help='override target (scratch-copy testing)')
    ap.add_argument('--expect-sha', default=BASE_SHA, help='override pin (scratch-copy testing)')
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

    plan = []

    # --- the four adjudicated crops ---
    for slug, finding in FINDINGS.items():
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        rbz = ((crop.get('regions') or {}).get('mid_south') or {}).get('resolved_by_zone') or {}
        if not rbz:
            print('ABORT: %s has no mid_south resolved_by_zone' % slug)
            return 2
        for zone, pred in PRECONDITIONS[slug]:
            cell = rbz.get(zone)
            if not isinstance(cell, dict):
                print('ABORT: %s mid_south z%s missing' % (slug, zone))
                return 2
            if not pred(cell):
                print('ABORT: %s mid_south z%s NO LONGER carries the defect this finding '
                      'describes -- re-verify before recording it' % (slug, zone))
                return 2
        ofs = (crop.get('verification_status') or {}).get('open_findings') or []
        if any(isinstance(f, dict) and f.get('id') == finding['id'] for f in ofs):
            print('ABORT: finding %s already present on %s' % (finding['id'], slug))
            return 2
        plan.append((slug, finding))

    # --- the shared bloom-derivation finding ---
    for slug in BLOOM_CROPS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        if not _bloom_arm_is_sole_bare(crop):
            print('ABORT: %s mid_south bloom arm is not a SOLE bare uada_ext host -- the '
                  'finding does not describe it' % slug)
            return 2
        ofs = (crop.get('verification_status') or {}).get('open_findings') or []
        if any(isinstance(f, dict) and f.get('id') == BLOOM_FINDING['id'] for f in ofs):
            print('ABORT: finding %s already present on %s' % (BLOOM_FINDING['id'], slug))
            return 2
        plan.append((slug, BLOOM_FINDING))

    # apple must NOT receive the bloom finding -- its bloom arm is already pathed
    if 'apple' in BLOOM_CROPS:
        print('ABORT: apple is in BLOOM_CROPS but its bloom arm cites a pathed url')
        return 2

    print('re-verified every described defect still present; %d findings planned' % len(plan))
    for slug, f in plan:
        print('  %-16s <- %s' % (slug, f['id']))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    for slug, finding in plan:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(json.loads(json.dumps(finding)))

    # prove NOTHING outside open_findings moved
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
        print('ABORT: %d value change(s) outside open_findings: %s' % (len(stray), stray[:8]))
        return 2
    print('verified: ZERO value changes outside open_findings')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d findings added, 0 values changed' % len(plan))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
