#!/usr/bin/env python3
"""GUARDED PROMOTE: remove 10 false University of Arkansas credits from mid_south herb prose.

ATTRIBUTION FIX ONLY. No number, suitability, citation or arm changes ride with it.
Evidence: docs/2026-07-31-mid-south-herb-hardiness-attribution-hunt.md.

THE DEFECT. Five herb crops (thyme, rosemary, oregano, sage, lavender) credit the University of
Arkansas with a plant-hardiness range -- and, on lavender, a disease "plant profile" -- across 7
mid_south cells, while citing `uada_ext`, the bare host https://www.uaex.uada.edu, as their SOLE
source. The mid_south prose is the mid_atlantic prose with the region words swapped and the
institution find-and-replaced. Every mid_atlantic herb cell anchors to the real NC State Plant
Toolbox page for the exact species; every mid_south herb cell anchors to a domain root.

Read from raw bytes, NC State's Toolbox matches our numbers to the character on four of five
(thyme 5a-9b, sage 4a-8b, lavender 5a-9b, oregano floor 4a), and lavender's disease sentence is
verbatim Toolbox ("susceptible to leaf spot and root rot. Root rot is caused by overwatering").

WHAT UAEX ACTUALLY PUBLISHES, per crop -- the answers differ, which is why they were adjudicated
one at a time rather than blanketed:
  thyme     nothing. Its only thyme material is a Q&A column (no zone) and a Plant of the Week on
            Thymus praecox, creeping thyme -- not our Thymus vulgaris.
  rosemary  nothing. Its page says "quite winter hardy in most parts of Arkansas" and repeats a
            NURSERY TAG's "hardy to 10 degrees F". The only archive page publishing a zone beside
            the word "rosemary" is Willow Rosemary -- Salix elaeagnos, a WILLOW.
  oregano   nothing. The only Origanum in the archive is the ornamental hybrid 'Amethyst Falls'.
  sage      nothing. Four ornamental salvias in the archive; none is Salvia officinalis, and the
            two that do give zones give 8-10 and 4-9, neither of them our 4 to 8.
  lavender  IT DOES -- and it is a DIFFERENT number. UAEX's English Lavender Plant of the Week
            (Lavandula angustifolia, our exact species) says "Lavender is hardy from zones 5 to 8".
            We credit it with "zones 5a to 9b", which is NC State's. Its humidity/root-rot framing
            IS supported by that page, but the page never mentions leaf spot.

Absence is document-scoped: 11 UAEX sources were read, including the COMPLETE 1,197-entry Plant of
the Week archive. UAEX publishes a hardiness range for exactly one of these five species.

THE FIX IS PURELY SUBTRACTIVE: delete the credit, keep the horticultural fact (the cherry-sweet
precedent, 2026-07-30). Every retained number is corroborated by the crop's own hardiness_zone_*
fields and its own pilot findings, so nothing is stranded. The credit is NOT repointed to NC State,
because the mid_south arms do not carry ncsu_ext -- naming a source the arm does not carry is the
exact failure promote_apple_mid_atlantic_bloom_reason.py refuses.

ALSO FILES 2 FINDINGS for what was surfaced and deliberately NOT fixed here (each its own ruling):
lavender's UAEX-vs-ours range divergence, and rosemary's mid_atlantic NC State credit, where NC
State's Toolbox says 8a-10b but our prose says "zone 7 to 8" (the number is sound -- it is our own
hardy-cultivar-inclusive floor per rosemary_pilot_finding_004 -- but NC State does not publish it).

FOOTPRINT: every edit asserts its exact prior text occurs exactly once and aborts on drift. After
the edits, ZERO University of Arkansas attributions may remain in any mid_south cell of these five
crops, every zone number must survive verbatim, and no rewritten string may name ANY institution.
COMPACT preserved.

    $ python3 tools/promote_mid_south_herb_hardiness_attributions.py --dry-run
    $ python3 tools/promote_mid_south_herb_hardiness_attributions.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'c6f50a1417a82786356fef764e524641143d41f973dc8f7097eb18454cb3fe5a'
SESSION = 'mid_south_herb_hardiness_attributions_2026_07_31'

CROPS = ('thyme', 'rosemary', 'oregano', 'sage', 'lavender')

# Any way this dataset names the institution. Used both to assert the ten are gone and to refuse
# to write a rewritten string that names an institution the arm does not carry.
UAEX_ATTR = re.compile(r'(?:the )?University of Arkansas|UAEX|Arkansas Cooperative Extension')
ANY_INSTITUTION = re.compile(
    r'University of Arkansas|UAEX|Arkansas Cooperative Extension|NC State|NCSU|'
    r'North Carolina State|Plant Toolbox')

# (slug, zone, field, exact text to remove-or-replace, replacement, zone tokens that must survive)
EDITS = [
    ('thyme', '7', 'synthesis_note_seasoned',
     'hardy to about zone 5 (the University of Arkansas: zones 5a to 9b), so',
     'hardy to about zone 5, so',
     ('zone 5',)),

    ('rosemary', '7', 'grown_as_note_seasoned',
     'hardy floor is about zone 7 (the University of Arkansas), so',
     'hardy floor is about zone 7, so',
     ('zone 7',)),
    ('rosemary', '7', 'synthesis_note_seasoned',
     'hardy only to about zone 7 to 8 (the University of Arkansas), so',
     'hardy only to about zone 7 to 8, so',
     ('zone 7 to 8',)),

    ('oregano', '7', 'synthesis_note_seasoned',
     'hardy to about zone 4 (the University of Arkansas Cooperative Extension), so',
     'hardy to about zone 4, so',
     ('zone 4',)),

    ('sage', '7', 'synthesis_note_seasoned',
     'hardy in roughly zones 4 to 8 (the University of Arkansas), so',
     'hardy in roughly zones 4 to 8, so',
     ('zones 4 to 8',)),
    ('sage', '8', 'synthesis_note_seasoned',
     "zone 4 to 8 ceiling (the University of Arkansas), so",
     'zone 4 to 8 ceiling, so',
     ('zone 4 to 8',)),

    ('lavender', '7', 'synthesis_note_seasoned',
     'hardy to about zone 5 (the University of Arkansas Cooperative Extension: zones 5a to 9b), so',
     'hardy to about zone 5, so',
     ('zone 5',)),
    ('lavender', '7', 'synthesis_note_seasoned',
     "the real constraint: the University of Arkansas's plant profile names root rot from "
     'overwatering and leaf spot as this species\' main threats, the closer analog',
     "the real constraint: root rot from overwatering and leaf spot are this species' main "
     'threats, the closer analog',
     ('root rot', 'leaf spot')),
    ('lavender', '7', 'grown_as_note_seasoned',
     "it is the region's humid summer: the University of Arkansas's own profile of the species "
     'flags root rot from wet soil and leaf spot as the real threats.',
     "it is the region's humid summer: root rot from wet soil and leaf spot are the real threats.",
     ('root rot', 'leaf spot')),
    ('lavender', '8', 'synthesis_note_seasoned',
     'zone 5 to 9b hardy range (the University of Arkansas Cooperative Extension).',
     'zone 5 to 9b hardy range.',
     ('zone 5 to 9b',)),
]

# Surfaced by this hunt, deliberately NOT fixed here. Each is its own ruling.
FINDINGS = [
    ('lavender', {
        'id': 'lavender_mid_south_uaex_zone_range_divergence',
        'summary': (
            'UAEX DOES publish a hardiness range for Lavandula angustifolia, and it differs from '
            'ours. Its English Lavender Plant of the Week (Gerald Klingaman, 2007-07-20) states '
            '"Lavender is hardy from zones 5 to 8"; our prose carries "zones 5a to 9b", which is '
            "NC State's Toolbox value and matches lavender.hardiness_zone_max = 9. The false UAEX "
            'credit was removed 2026-07-31 and the NC State number retained unattributed. IF '
            'mid_south lavender is ever repointed to the real UAEX Plant of the Week URL (the one '
            'genuine repoint this hunt found, and the fix for its bare host), the z8 cell MUST '
            'change with it: it reads "zone 8 sits comfortably inside English lavender\'s zone 5 '
            'to 9b hardy range", and under UAEX\'s number zone 8 is the CEILING, not comfortably '
            'inside. Note also that the UAEX page supports the root-rot/humidity framing but '
            'never mentions leaf spot.'),
        'severity': 'low',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'status': 'open',
    }),
    ('rosemary', {
        'id': 'rosemary_mid_atlantic_ncsu_zone_attribution',
        'summary': (
            'mid_atlantic z7 credits NC State with rosemary\'s "zone 7 to 8" hardy floor, but NC '
            "State's Plant Toolbox gives Salvia rosmarinus as 8a-10b, read from raw bytes "
            '2026-07-31. The NUMBER is sound and is not in question: 7 is our own '
            'hardy-cultivar-inclusive floor per rosemary_pilot_finding_004 ("Hill Hardy z7, Arp '
            'z6", with the species itself noted as z8 per NCSU), and it matches '
            'rosemary.hardiness_zone_min = 7. It is the CREDIT that overstates, since NC State '
            'does not publish 7. Same defect shape as the mid_south UAEX credits removed '
            '2026-07-31, but in a different region and so out of that hunt\'s scope. Needs its '
            'own ruling: either drop the NC State credit as mid_south\'s was dropped, or restate '
            'the sentence as our own cultivar-inclusive judgment.'),
        'severity': 'low',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'status': 'open',
    }),
]


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

    def cell(slug, z):
        return crops[slug]['regions']['mid_south']['resolved_by_zone'][z]

    # PREFLIGHT. The defect must still be there, and at exactly the size the evidence claims.
    # A hunt that has already been applied, or has drifted, must not proceed.
    pre_counts = {}
    for slug in CROPS:
        n = 0
        for z, c in (crops[slug]['regions']['mid_south'].get('resolved_by_zone') or {}).items():
            for k, v in c.items():
                if isinstance(v, str) and k.endswith(('_seasoned', '_beginner')):
                    n += len(UAEX_ATTR.findall(v))
        pre_counts[slug] = n
    EXPECT_PRE = {'thyme': 1, 'rosemary': 2, 'oregano': 1, 'sage': 2, 'lavender': 4}
    if pre_counts != EXPECT_PRE:
        print('ABORT: the defect is not the shape the evidence describes.\n'
              '  expected %s\n  found    %s' % (EXPECT_PRE, pre_counts))
        return 2
    print('preflight: %d UAEX attributions present across %d crops, as measured'
          % (sum(pre_counts.values()), len(CROPS)))

    # Every mid_south herb cell must still be citing ONLY the bare host. If a repoint has landed
    # in the meantime, the premise of this promote is gone and it must not run.
    for slug in CROPS:
        for z in ('7', '8'):
            if 'uada_ext' not in (cell(slug, z).get('sources') or []):
                print('ABORT: %s z%s no longer cites uada_ext -- premise changed' % (slug, z))
                return 2
    print('preflight: all 10 herb cells still cite uada_ext')

    applied = []
    for slug, z, field, old, new, keep in EDITS:
        c = cell(slug, z)
        cur = c.get(field)
        if not isinstance(cur, str) or cur.count(old) != 1:
            print('ABORT: %s z%s %s does not contain the expected text exactly once' % (slug, z, field))
            return 2
        c[field] = cur.replace(old, new)
        # the horticultural fact must survive the credit removal
        for tok in keep:
            if tok not in c[field]:
                print('ABORT: %s z%s %s lost the fact %r' % (slug, z, field, tok))
                return 2
        applied.append('%s z%s %s' % (slug, z, field))

    # LOAD-BEARING: not one University of Arkansas credit may remain in these crops' mid_south
    # prose. This is the check the whole promote exists to satisfy.
    for slug in CROPS:
        for z, c in (crops[slug]['regions']['mid_south'].get('resolved_by_zone') or {}).items():
            for k, v in c.items():
                if isinstance(v, str) and UAEX_ATTR.search(v):
                    print('ABORT: %s z%s %s still credits the University of Arkansas' % (slug, z, k))
                    return 2
    print('verified: 0 University of Arkansas attributions remain in the 5 crops\' mid_south prose')

    # HUNT-1 GUARD: a rewritten string may not name ANY institution -- not the one we removed, and
    # not NC State either, which these arms do not carry.
    for slug, z, field, _o, _n, _k in EDITS:
        v = cell(slug, z)[field]
        m = ANY_INSTITUTION.search(v)
        if m:
            print('ABORT: rewritten %s z%s %s names an institution the arm does not carry: %r'
                  % (slug, z, field, m.group(0)))
            return 2
    print('verified: no rewritten string names any institution')

    # house style
    EM = chr(8212)
    for slug, z, field, _o, _n, _k in EDITS:
        v = cell(slug, z)[field]
        if EM in v or '--' in v:
            print('ABORT: em dash or "--" in consumer copy: %s z%s %s' % (slug, z, field))
            return 2
        if '  ' in v or ' ,' in v or ' .' in v:
            print('ABORT: whitespace/punctuation artifact left by the removal: %s z%s %s'
                  % (slug, z, field))
            return 2
    print('verified: no em dash, doubled space, or orphaned punctuation')

    # file the two surfaced findings
    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        ofs = vs.setdefault('open_findings', [])
        if any(isinstance(f, dict) and f.get('id') == finding['id'] for f in ofs):
            print('ABORT: finding %s already filed' % finding['id'])
            return 2
        ofs.append(copy.deepcopy(finding))
        applied.append('%s finding %s filed' % (slug, finding['id']))

    # UAEX must be untouched everywhere ELSE in the dataset -- this hunt is herbs only. Runs
    # AFTER the findings are filed so it covers those too, not just the prose edits.
    def uaex_census(doc):
        return len(UAEX_ATTR.findall(json.dumps(doc, ensure_ascii=False)))
    other_before = {s: uaex_census(c) for s, c in {x['slug']: x for x in before['crops']}.items()
                    if s not in CROPS}
    other_after = {s: uaex_census(c) for s, c in crops.items() if s not in CROPS}
    if other_before != other_after:
        moved = [s for s in other_before if other_before[s] != other_after.get(s)]
        print('ABORT: UAEX mentions changed on non-herb crops: %s' % moved)
        return 2
    print('verified: UAEX mentions unchanged on all %d other crops' % len(other_before))

    # exact footprint
    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    EXPECT = sorted(CROPS)
    if changed != EXPECT:
        print('ABORT: crops changed = %s, expected %s' % (changed, EXPECT))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly %d crops changed, nothing else' % len(changed))

    # nothing but the ten strings and the two findings moved inside those crops
    for slug in CROPS:
        b, a = ba[slug], aa[slug]
        touched = {(z, k)
                   for z in (b.get('regions', {}).get('mid_south', {})
                             .get('resolved_by_zone') or {})
                   for k in b['regions']['mid_south']['resolved_by_zone'][z]
                   if b['regions']['mid_south']['resolved_by_zone'][z][k]
                   != a['regions']['mid_south']['resolved_by_zone'][z][k]}
        want = {(z, f) for s, z, f, _o, _n, _k in EDITS if s == slug}
        if touched != want:
            print('ABORT: %s touched fields %s, expected %s' % (slug, sorted(touched), sorted(want)))
            return 2
        for reg in b.get('regions', {}):
            if reg != 'mid_south' and b['regions'][reg] != a['regions'][reg]:
                print('ABORT: %s region %s changed' % (slug, reg))
                return 2
    print('verified: only the intended fields moved, and only in mid_south')

    print('\n%d edits:' % len(applied))
    for a in applied:
        print('  ' + a)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits across %d crops' % (len(applied), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
