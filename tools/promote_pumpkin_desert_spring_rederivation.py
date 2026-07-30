#!/usr/bin/env python3
"""GUARDED PROMOTE: re-derive pumpkin's DESERT SPRING cycle onto its sourced March start.

WHY THIS EXISTS -- it closes a defect I introduced. promote_ca_desert_soil_temp_floor.py
(batch 1/3) moved the four winter cucurbits off their Jan 15 opening by COPYING z9's already
correct `Feb 1 - Mar 1`. That was right for acorn / butternut / spaghetti squash, whose UC row
is "Feb-March; Aug" -- February is explicitly permitted. It was WRONG for pumpkin, which sits
on a DIFFERENT UC row, and I did not check it:

    UC (Master Gardener Handbook Table 13.2), Desert Valleys column
      squash, winter -> "Feb-March; Aug"     <- February permitted
      pumpkins       -> "March-June"         <- NO February
    U of A AZ1005 (Maricopa County), Pumpkin
      spring marks   -> Mar 1, Mar 15        <- NO February

THE LESSON, recorded because it generalises: copying a correct sibling is safe ONLY when the
sibling's own source row covers the target crop. Batch 1 improved pumpkin from `Jan 15` to
`Feb 1` and left it a month early.

BOTH DESERT REGIONS ARE CONTRADICTED, and low_desert_az is the cleaner case:
    ca_desert     z9/z10/z11  `Feb 1 - Mar 1`   vs UC "March-June"        (UC is the CA source)
    low_desert_az z9/z10      `Feb 15 - Mar 15` vs AZ1005 Mar 1 / Mar 15
low_desert_az cells cite AZ1005 by its CORRECT PATHED URL
(extension.arizona.edu/sites/default/files/2024-08/az1005-2018.pdf) -- so that cell is
contradicted by its own directly-cited governing document, with NO geography question at all.
ca_desert is governed by UC's California row, which also starts at March. Both therefore land on
the same window, which is correct for two adjacent Sonoran low-desert regions.

THE RE-DERIVATION (not a one-line shift):
  plant_out -> `Mar 1 - Mar 15`. Starts where BOTH documents start; spans exactly AZ1005's two
  pumpkin marks; sits inside UC's "March-June".
  harvest -> `Jun 15 - Jun 30`, derived from PUMPKIN'S OWN cross-region offset convention rather
  than an invented number. Its hot-desert cells run start+103..106 (ca_desert) and start+106..107
  (low_desert_az); applied to Mar 1 / Mar 15 both give Jun 15 / Jun 30 after month-boundary
  snapping. DTM is [85, 120] (mid 100), so the window sits inside the crop's own range.
  calendar -> February stops being a planting month. Feb becomes `cold_pause`, which is
  semantically right here: the constraint is SOIL TEMPERATURE (germination_temp_f [70, 95];
  start_method wants ~70F at 2 inches), and desert soil in February has not reached it. Both
  regions converge on one array.

WHY UC's "March-June" IS NOT ADOPTED WHOLE: it appears to merge both desert cycles into one
envelope (a March spring crop and a June-onward Halloween crop). Our model splits them
explicitly -- spring here, plus the existing `Jul 1 - Jul 31` second planting -- and AZ1005
backs that split with separate Mar and Jul/Aug mark clusters. Widening spring to June would
collapse a two-cycle model that both the data and AZ1005 keep separate.

NOT IN SCOPE, deliberately:
  - The `Jul 1 - Jul 31` second planting and its provenance gap: already adjudicated and
    recorded as `ca_desert_fall_cycle_provenance_gap` (promote 3/4). Untouched here.
  - REPOINTING ca_desert's bare `ucanr.edu` / `mg.ucanr.edu` anchors at the pathed UC table.
    Now that the spring window matches that document it would be a clean repoint, but mixing a
    value change with a citation change in one promote is exactly what the arc warns against.
    Left as a flagged citation-arc candidate.
  - pumpkin's non-desert regions: no document read this session governs them.

FOOTPRINT: exactly 5 cells x 7 keys, plus one open_finding. Nothing else.
COMPACT preserved: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_pumpkin_desert_spring_rederivation.py --dry-run
    $ python3 tools/promote_pumpkin_desert_spring_rederivation.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '6eddf48f074bdf92406ef0df84ca98a1d5a0cfbe2383ffbeac42cb81d854f6ee'

SLUG = 'pumpkin'
NEW_CALENDAR = ['cold_pause', 'cold_pause', 'plant', 'growing', 'growing', 'harvest',
                'plant', 'growing', 'growing', 'harvest', 'harvest', 'cold_pause']
AFTER = {
    'plant_out': 'Mar 1 - Mar 15',
    'first_plant_date': 'Mar 1',
    'last_plant_date': 'Mar 15',
    'harvest': 'Jun 15 - Jun 30',
    'harvest_start': 'Jun 15',
    'harvest_end': 'Jun 30',
    'calendar': NEW_CALENDAR,
}
KEYS = list(AFTER)

# region -> zones -> exact required pre-state
TARGETS = {
    'ca_desert': {
        'zones': ['9', '10', '11'],
        'before': {
            'plant_out': 'Feb 1 - Mar 1',
            'first_plant_date': 'Feb 1',
            'last_plant_date': 'Mar 1',
            'harvest': 'May 15 - Jun 15',
            'harvest_start': 'May 15',
            'harvest_end': 'Jun 15',
            'calendar': ['cold_pause', 'plant', 'plant', 'growing', 'harvest', 'harvest',
                         'plant', 'growing', 'growing', 'harvest', 'harvest', 'cold_pause'],
        },
    },
    'low_desert_az': {
        'zones': ['9', '10'],
        'before': {
            'plant_out': 'Feb 15 - Mar 15',
            'first_plant_date': 'Feb 15',
            'last_plant_date': 'Mar 15',
            'harvest': 'Jun 1 - Jun 30',
            'harvest_start': 'Jun 1',
            'harvest_end': 'Jun 30',
            'calendar': ['cold_pause', 'plant', 'plant', 'growing', 'growing', 'harvest',
                         'plant', 'growing', 'growing', 'harvest', 'harvest', 'cold_pause'],
        },
    },
}
# the fall cycle must survive untouched
PRESERVE_SECOND = {'plant_out': 'Jul 1 - Jul 31', 'harvest_start': 'Oct 1',
                   'harvest_end': 'Nov 1'}

FINDING_ID = 'pumpkin_desert_spring_march_rederivation'
FINDING = {
    'id': FINDING_ID,
    'severity': 'medium',
    'blocks_launch': False,
    'status': 'resolved',
    'summary': (
        'CORRECTED 2026-07-29: pumpkin\'s desert SPRING window opened in February, which neither '
        'governing document permits. UC (Master Gardener Handbook Table 13.2) gives pumpkins '
        '"March-June" for Desert Valleys and U of A AZ1005 marks pumpkin spring sowings at Mar 1 '
        'and Mar 15 -- neither has February. ca_desert z9/z10/z11 read "Feb 1 - Mar 1" and '
        'low_desert_az z9/z10 read "Feb 15 - Mar 15"; both are now "Mar 1 - Mar 15" with harvest '
        're-derived to "Jun 15 - Jun 30" from this crop\'s own cross-region offset convention '
        '(start+103..107 in its hot-desert cells), and February is no longer a planting month in '
        'the calendar because the binding constraint is soil temperature, not frost. NOTE ON '
        'PROVENANCE: the earlier same-day fix (ca_desert_z10_z11_soil_temp_floor_correction) moved '
        'this crop off a Jan 15 opening by copying the winter-squash sibling zone, which was right '
        'for acorn/butternut/spaghetti squash (UC row "Feb-March; Aug", February permitted) but '
        'wrong for pumpkin, which sits on a different UC row. Copying a correct sibling is safe '
        'only when the sibling\'s own source row covers the target crop.'),
    'basis': (
        'Both documents read directly this session (urllib + pypdf/fitz word geometry, AZ1005 '
        'validated against a control row), never via a WebFetch summary. low_desert_az is the '
        'cleaner case: those cells already cite AZ1005 by its correct pathed URL, so the cell was '
        'contradicted by its own directly-cited governing document with no geography question. '
        'ca_desert is governed by UC\'s California row, which also starts at March, so both '
        'regions correctly converge on one window. UC\'s "March-June" is NOT adopted whole because '
        'it appears to merge the desert\'s two cycles into a single envelope, while our model and '
        'AZ1005 both keep a March spring crop separate from a Jul/Aug fall crop. The Jul 1 - Jul 31 '
        'second planting is untouched and its own provenance gap is recorded separately as '
        'ca_desert_fall_cycle_provenance_gap. STILL AVAILABLE, not done here: ca_desert\'s bare '
        'ucanr.edu / mg.ucanr.edu anchors could now be cleanly repointed at the pathed UC table '
        'that supports this window, but mixing a value change with a citation change in one '
        'promote is what the arc warns against.'),
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
    crop = crops.get(SLUG)
    if crop is None:
        print('ABORT: %s absent' % SLUG)
        return 2

    plan = []
    for region, spec in TARGETS.items():
        rbz = ((crop.get('regions') or {}).get(region) or {}).get('resolved_by_zone') or {}
        for zone in spec['zones']:
            node = rbz.get(zone)
            if not isinstance(node, dict):
                print('ABORT: %s %s z%s missing' % (SLUG, region, zone))
                return 2
            for k, want in spec['before'].items():
                if node.get(k) != want:
                    print('ABORT: %s %s z%s.%s pre-state mismatch\n  expected %r\n  found    %r'
                          % (SLUG, region, zone, k, want, node.get(k)))
                    return 2
            sp = node.get('second_planting')
            if not isinstance(sp, dict):
                print('ABORT: %s %s z%s has no second_planting to preserve' % (SLUG, region, zone))
                return 2
            for k, want in PRESERVE_SECOND.items():
                if sp.get(k) != want:
                    print('ABORT: %s %s z%s second_planting.%s is %r, expected %r'
                          % (SLUG, region, zone, k, sp.get(k), want))
                    return 2
            plan.append((region, zone, node))

    expected = sum(len(s['zones']) for s in TARGETS.values())
    if len(plan) != expected:
        print('ABORT: expected %d cells, planned %d' % (expected, len(plan)))
        return 2
    print('pre-state verified on all %d target cells' % len(plan))

    for region, zone, node in plan:
        print('\n  %s %s z%s' % (SLUG, region, zone))
        for k in KEYS:
            print('      %-18s %r\n      %-18s -> %r' % (k, node.get(k), '', AFTER[k]))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    for region, zone, node in plan:
        for k in KEYS:
            node[k] = json.loads(json.dumps(AFTER[k]))
        sp = node['second_planting']
        for k, want in PRESERVE_SECOND.items():
            if sp.get(k) != want:
                print('ABORT MID-APPLY: %s z%s second_planting drifted' % (region, zone))
                return 2

    ofs = crop.setdefault('verification_status', {}).setdefault('open_findings', [])
    if any(isinstance(f, dict) and f.get('id') == FINDING_ID for f in ofs):
        print('ABORT: finding already present')
        return 2
    ofs.append(json.loads(json.dumps(FINDING)))

    # prove the footprint: only pumpkin changed, only the named keys
    stray = []

    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in set(a) | set(b):
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
    bad = [s for s in stray
           if not (s.startswith('pumpkin.')
                   and ('open_findings[' in s
                        or any(s.endswith('.' + k) for k in KEYS if k != 'calendar')
                        or '.calendar[' in s))]
    if bad:
        print('ABORT: %d unexpected change(s): %s' % (len(bad), bad[:8]))
        return 2
    print('verified footprint: only pumpkin, only the 7 named keys + 1 finding')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(CANON, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d cells x %d keys + 1 finding' % (len(plan), len(KEYS)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
