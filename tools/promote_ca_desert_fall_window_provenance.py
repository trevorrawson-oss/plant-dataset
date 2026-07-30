#!/usr/bin/env python3
"""GUARDED PROMOTE: record the ca_desert FALL-CYCLE provenance gap. NO VALUE CHANGES.

THE ADJUDICATION, and why it ends in a finding rather than an edit.

The ca_desert second/fall cycle diverges from the UC table these cells cite:

  crop group                   ours                 UC (Desert Valleys)   AZ1005 (Maricopa, AZ)
  winter squash (acorn/        Jul 1 - Jul 31       "Aug"                 Jul 1 / Jul 15 / Aug 1
    butternut/spaghetti)
  pumpkin                      Jul 1 - Jul 31       NONE ("March-June")   Jul 1 / Jul 15 / Aug 1
  cucumbers (x4)               Sep 1 - Sep 30/Oct 1 "Aug"                 Aug 15 / Sep 1 / Sep 15
  summer squash (x2)           Sep 1 - Sep 30/Oct 1 "Aug-Sep"             Aug 15 / Sep 1

NO DATES ARE CHANGED, deliberately, and this is the reasoning:

  1. NOTHING SHOWS THE WINDOWS ARE WRONG. A July sowing of winter squash / pumpkin for an
     Oct-Nov desert harvest is standard low-desert practice and AZ1005 marks exactly it. Our
     Sep 1 cucumber/summer-squash start sits at the late edge of what both documents allow,
     which is CONSERVATIVE for a home gardener -- it avoids sowing into a 110F September.
  2. TRIMMING ON ARIZONA'S AUTHORITY WOULD BE A GEOGRAPHY STRETCH (kickoff sec 7). AZ1005 is
     titled "Vegetable Planting Calendar for Maricopa County". It is a legitimate CLIMATIC
     ANALOGUE for Imperial/Coachella -- same Sonoran low desert -- but it is not a California
     document, and narrowing a Californian window to its last mark would assert coverage it
     does not claim.
  3. UC PUBLISHES NO CALIFORNIA-DESERT FALL WINDOW AT ALL. Searched and read this session:
       - UC MG statewide Table 13.2 -- one coarse row for all "Desert Valleys", and the page
         self-limits ("planting dates are only approximate").
       - UC ANR's own Imperial County Planting Calendar
         (ucanr.edu/sites/default/files/2020-10/337028.pdf, Rev 8/2017) -- a GENUINE UC ANR
         document whose warm-weather table runs Jan-Apr and cool-weather table Sep-Dec, so it
         has NO May-Aug columns and cannot address a summer-sown fall cycle.
       - UC IPM cucurbits landing page -- no planting dates.
       - UC VRIC cucumber PDF -- 404.
       - UC MG Riverside's linked "planting calendar" -- already documented as a Grangetto's
         Farm & Garden retail chart served from a ucanr.edu URL (a T2 trap wearing a T1 host).
     So the quantity does not exist in the California literature for this region and cycle --
     the same shape as the harvest-start-is-not-a-published-datum lesson.

Therefore this is a CONTENT finding, not a URL fix and not a date fix, and the kickoff is
explicit that the second kind must be surfaced rather than quietly repointed at a
plausible-looking page. Recording it is the deliverable.

SEPARATE, NOT TOUCHED HERE, and owed a decision: pumpkin's ca_desert SPRING window is
`Feb 1 - Mar 1` while UC gives pumpkins "March-June" and AZ1005's earliest pumpkin mark is
`Mar 1` -- neither has February. Winter squash legitimately IS February (UC "Feb-March"), and
promote 1/2 copied the winter-squash sibling shape into pumpkin rather than checking pumpkin's
own row. That is a real residual from that batch and needs its own re-derivation (UC's
"March-June" also implies a window extending into June, so it is not a one-line shift).

FOOTPRINT: exactly one open_finding appended to each of 10 crops. ZERO value changes -- the
script asserts that no field outside open_findings moved.
COMPACT preserved: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_ca_desert_fall_window_provenance.py --dry-run
    $ python3 tools/promote_ca_desert_fall_window_provenance.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '04fcbc7476ff6b4a7d10aa21f9d8816ce37f44693f5d15f42a621b4b03b918d9'

WINTER = ['acorn-squash', 'butternut-squash', 'spaghetti-squash', 'pumpkin']
SUMMER = ['cucumber', 'slicing-cucumber', 'english-cucumber', 'pickling-cucumber',
          'zucchini-courgette', 'yellow-summer-squash']

FINDING_ID = 'ca_desert_fall_cycle_provenance_gap'

_SHARED_BASIS = (
    'Sources read directly this session (urllib + pypdf/fitz geometry, never a WebFetch '
    'summary): UC Master Gardener planting-date table (California Master Gardener Handbook '
    'Table 13.2), which self-limits ("planting dates are only approximate"); U of A AZ1005 '
    'Vegetable Planting Calendar for Maricopa County, read by word geometry and validated '
    'against a control row. AZ1005 is cited here as a CLIMATIC ANALOGUE for the Sonoran low '
    'desert, explicitly NOT as a California source -- trimming a Californian window to its '
    'marks would be the geography stretch the arc warns about. Searched for a '
    'California-desert-specific fall window and found none: UC ANR\'s own Imperial County '
    'Planting Calendar (ucanr.edu/sites/default/files/2020-10/337028.pdf, Rev 8/2017) is a '
    'genuine UC document but its warm-weather table runs Jan-Apr and its cool-weather table '
    'Sep-Dec, so it has no May-Aug columns and cannot address a summer-sown fall cycle; UC IPM '
    'cucurbits carries no planting dates; the UC VRIC cucumber PDF 404s; and UC MG Riverside\'s '
    'linked "planting calendar" is a Grangetto\'s retail chart served from a ucanr.edu URL. '
    'NO DATES CHANGED: nothing shows the window is wrong, and this is recorded as a content '
    'finding rather than repointed at a plausible-looking page.')

FINDING = {
    'winter': {
        'id': FINDING_ID,
        'severity': 'low',
        'blocks_launch': False,
        'status': 'accepted',
        'summary': (
            'The ca_desert Jul 1 - Jul 31 second planting (fall harvest Oct 1 - Nov 1) is a '
            'MODELED desert second cycle that the cited UC planting-date table does not carry: '
            'UC gives winter squash "Feb-March; Aug" for Desert Valleys, one month later than '
            'ours, and gives PUMPKINS "March-June" with no fall cycle at all. The window is '
            'independently corroborated by U of A AZ1005, whose low-desert winter-squash and '
            'pumpkin marks are Jul 1 / Jul 15 / Aug 1 -- standard low-desert practice for an '
            'October-November harvest. Left unchanged; the gap is provenance, not correctness.'),
        'basis': _SHARED_BASIS,
    },
    'summer': {
        'id': FINDING_ID,
        'severity': 'low',
        'blocks_launch': False,
        'status': 'accepted',
        'summary': (
            'The ca_desert fall segment (Sep 1 - Sep 30 in z9, Sep 1 - Oct 1 in z10/z11) sits at '
            'or past the late edge of both available documents: UC gives cucumbers "Aug" and '
            'summer squash "Aug-Sep" for Desert Valleys, and U of A AZ1005 marks Aug 15 / Sep 1 / '
            'Sep 15 for cucumbers and Aug 15 / Sep 1 for summer squash. Our later start is '
            'CONSERVATIVE for a home gardener -- it avoids sowing into a 110 degrees F September '
            '-- and the end runs past both marks but stays inside the zone\'s own first-frost '
            'bound. Left unchanged; the gap is provenance, not correctness.'),
        'basis': _SHARED_BASIS,
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    with open(CANON, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != BASE_SHA:
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (BASE_SHA, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)
    crops = {c['slug']: c for c in data['crops']}

    plan = []
    for group, slugs in (('winter', WINTER), ('summer', SUMMER)):
        for slug in slugs:
            crop = crops.get(slug)
            if crop is None:
                print('ABORT: crop %s absent' % slug)
                return 2
            rbz = ((crop.get('regions') or {}).get('ca_desert') or {}).get(
                'resolved_by_zone') or {}
            if not rbz:
                print('ABORT: %s has no ca_desert resolved_by_zone' % slug)
                return 2
            # confirm the fall cycle this finding describes actually exists
            found = False
            for zone, node in rbz.items():
                if not isinstance(node, dict):
                    continue
                if group == 'winter':
                    sp = node.get('second_planting')
                    if isinstance(sp, dict) and sp.get('plant_out') == 'Jul 1 - Jul 31':
                        found = True
                else:
                    po = node.get('plant_out') or ''
                    if ',' in po and po.split(',')[1].strip().startswith('Sep 1'):
                        found = True
            if not found:
                print('ABORT: %s does not carry the %s fall cycle this finding describes'
                      % (slug, group))
                return 2
            ofs = (crop.get('verification_status') or {}).get('open_findings') or []
            if any(isinstance(f, dict) and f.get('id') == FINDING_ID for f in ofs):
                print('ABORT: finding %s already present on %s' % (FINDING_ID, slug))
                return 2
            plan.append((slug, group))

    print('verified the described fall cycle on all %d crops' % len(plan))
    for slug, group in plan:
        print('  %-22s <- %s finding' % (slug, group))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    for slug, group in plan:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(json.loads(json.dumps(FINDING[group])))

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
    with open(CANON, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d findings added, 0 values changed' % len(plan))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
