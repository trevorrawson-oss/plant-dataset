#!/usr/bin/env python3
"""GUARDED PROMOTE 2/2: ca_desert z10/z11 SUMMER-cucurbit + cucumber spring openings.

Companion to tools/promote_ca_desert_soil_temp_floor.py, which fixed the four WINTER
cucurbits. Same defect, six more crops: cucumber, slicing-cucumber, english-cucumber,
pickling-cucumber, zucchini-courgette, yellow-summer-squash -- all open their ca_desert
z10/z11 SPRING window on `Jan 15` while those cells' `resolved_from.last_frost` IS `Jan 15`.

WHY THIS ONE IS WORSE THAN THE WINTER-SQUASH BATCH. These twelve cells do NOT cite a bare
host. They already cite the PATHED document --
`https://ucanr.edu/program/uc-master-gardener-program/time-planting` -- and that document's
own table says, for "Desert Valleys" (defined on the page as Imperial and Coachella):
    cucumbers      -> "Feb-May; Aug"
    squash, summer -> "Feb-Mar; Aug-Sep"
Both start in FEBRUARY. So the cell cites the exact page that contradicts it. U of A AZ1005
(Maricopa) agrees independently: its earliest Cucumbers seeding mark is `Feb 15` and its
earliest Squash, Summer mark is `Feb 15`. Both documents read directly (urllib + pypdf/fitz
geometry, AZ1005 validated against a control row), never via a WebFetch summary.

And as with the winter squashes, the crops' own copy already stated the real constraint:
`start_method.notes_seasoned` requires soil "reliably warm (at least 70 degrees F at 2 inches;
seed will not germinate below about 50 degrees F)" and `germination_temp_f` is [70, 95] / [70, 90].
Soil temperature lags frost by weeks.

THE FIX IS NARROWER THAN BATCH 1, DELIBERATELY. These are TWO-CYCLE cells: a spring window and
a fall window in one comma-joined string, with a Jul/Aug `heat_pause` between. Only the SPRING
half is wrong. The FALL half is bound by FIRST frost, which genuinely differs by zone
(z10/z11 `Dec 31` vs z9 `Dec 15`), so z10/z11 correctly run later than z9 there --
`last_plant_date` `Oct 1` vs `Sep 30`, `harvest_end` `Dec 20` vs `Dec 10`, `succession_fall`
`Sep 1, Sep 22` vs `Sep 1, Sep 30`. Copying z9 wholesale, as batch 1 could safely do, would
DESTROY that correct differentiation. So this script splices ONLY the spring segment from z9
and preserves each target's own fall segment byte-for-byte.

NOT IN SCOPE (surfaced, not smuggled): the FALL windows run later than both sources
(ours `Sep 1 - Oct 1`; UC says "Aug" for cucumbers and "Aug-Sep" for summer squash; AZ1005
marks Aug 15 / Sep 1 / Sep 15). Same family as the winter-squash Jul-vs-Aug second planting.
A separate adjudication.

RULED NOT A DEFECT, and therefore untouched: the 6 `utah_dixie` z8 cells the scan also reports.
Their region note already documents the reason -- "Direct-sow around March 15, the Group C
(Tender) date for St. George, about two weeks ahead of the March 30 average last frost; the
table's explicit local date runs earlier than a generic frost-relative rule would" -- citing
USU Extension's Suggested Vegetable Planting Dates for Utah. CLAUDE.md: explicit source dates
govern over arithmetic.

FOOTPRINT: exactly 12 cells x 6 keys, plus one open_finding per crop. Nothing else.
COMPACT preserved: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_ca_desert_cucurbit_spring_floor.py --dry-run
    $ python3 tools/promote_ca_desert_cucurbit_spring_floor.py --apply
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

# pinned pre-state: the canonical AFTER promote 1/2 (the winter-cucurbit batch)
BASE_SHA = '2702917e6a849005c1f961e1d87a0f8f89d96d4e00552827ecb23c34e8e83c6f'

CROPS = ['cucumber', 'slicing-cucumber', 'english-cucumber', 'pickling-cucumber',
         'zucchini-courgette', 'yellow-summer-squash']
REGION = 'ca_desert'
ZONES = ['10', '11']
TEMPLATE_ZONE = '9'

# every target cell must be in exactly this pre-state, or we abort
EXPECT_BEFORE = {
    'plant_out': 'Jan 15 - Mar 1, Sep 1 - Oct 1',
    'first_plant_date': 'Jan 15',
    'succession_spring': 'Jan 15, Feb 5, Feb 26',
    'calendar': ['plant', 'plant', 'harvest', 'harvest', 'harvest', 'harvest',
                 'heat_pause', 'heat_pause', 'plant', 'harvest', 'harvest', 'harvest'],
}
# the corrected z9 template must look like this
EXPECT_TEMPLATE = {
    'plant_out': 'Feb 1 - Mar 15, Sep 1 - Sep 30',
    'first_plant_date': 'Feb 1',
    'succession_spring': 'Feb 1, Feb 22, Mar 15',
    'calendar': ['cold_pause', 'plant', 'plant', 'harvest', 'harvest', 'harvest',
                 'heat_pause', 'heat_pause', 'plant', 'harvest', 'harvest', 'harvest'],
}
# fall-cycle fields that MUST NOT move (first-frost bound, legitimately zone-differentiated)
PRESERVE = ['harvest_end', 'last_plant_date', 'succession_fall', 'successions_realized']

FINDING_ID = 'ca_desert_z10_z11_spring_soil_temp_floor_correction'


def split2(s, label):
    """Split a two-cycle 'spring, fall' string into exactly two segments."""
    parts = [p.strip() for p in s.split(',')]
    if len(parts) != 2:
        raise ValueError('%s: expected exactly 2 comma segments, got %d in %r'
                         % (label, len(parts), s))
    return parts


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
    crops = {c['slug']: c for c in data['crops']}

    plan = []
    for slug in CROPS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        rbz = ((crop.get('regions') or {}).get(REGION) or {}).get('resolved_by_zone') or {}
        tpl = rbz.get(TEMPLATE_ZONE)
        if not isinstance(tpl, dict):
            print('ABORT: %s z%s template missing' % (slug, TEMPLATE_ZONE))
            return 2
        for k, want in EXPECT_TEMPLATE.items():
            if tpl.get(k) != want:
                print('ABORT: %s z%s template.%s is not the expected corrected shape\n'
                      '  expected %r\n  found    %r' % (slug, TEMPLATE_ZONE, k, want, tpl.get(k)))
                return 2

        try:
            tpl_po_spring, _tpl_po_fall = split2(tpl['plant_out'], '%s z9 plant_out' % slug)
            tpl_h_spring, _tpl_h_fall = split2(tpl['harvest'], '%s z9 harvest' % slug)
        except ValueError as e:
            print('ABORT: %s' % e)
            return 2

        for zone in ZONES:
            node = rbz.get(zone)
            if not isinstance(node, dict):
                print('ABORT: %s z%s missing' % (slug, zone))
                return 2
            for k, want in EXPECT_BEFORE.items():
                if node.get(k) != want:
                    print('ABORT: %s z%s.%s pre-state mismatch\n  expected %r\n  found    %r'
                          % (slug, zone, k, want, node.get(k)))
                    return 2
            try:
                _po_spring, po_fall = split2(node['plant_out'], '%s z%s plant_out' % (slug, zone))
                _h_spring, h_fall = split2(node['harvest'], '%s z%s harvest' % (slug, zone))
            except ValueError as e:
                print('ABORT: %s' % e)
                return 2

            after = {
                'plant_out': '%s, %s' % (tpl_po_spring, po_fall),   # z9 spring + own fall
                'harvest': '%s, %s' % (tpl_h_spring, h_fall),
                'harvest_start': tpl['harvest_start'],
                'first_plant_date': tpl['first_plant_date'],
                'succession_spring': tpl['succession_spring'],
                'calendar': tpl['calendar'],
            }
            # the fall half must survive untouched
            if not after['plant_out'].endswith(po_fall) or not after['harvest'].endswith(h_fall):
                print('ABORT: %s z%s fall segment would not survive' % (slug, zone))
                return 2
            plan.append((slug, zone, node, after, {k: node.get(k) for k in PRESERVE}))

    if len(plan) != len(CROPS) * len(ZONES):
        print('ABORT: expected %d cells, planned %d' % (len(CROPS) * len(ZONES), len(plan)))
        return 2
    print('pre-state verified on all %d target cells' % len(plan))

    for slug, zone, node, after, preserved in plan:
        print('\n  %s %s z%s' % (slug, REGION, zone))
        for k in ('plant_out', 'harvest', 'harvest_start', 'first_plant_date',
                  'succession_spring'):
            print('      %-18s %r -> %r' % (k, node.get(k), after[k]))
        print('      %-18s %r -> %r' % ('calendar[0]', node['calendar'][0], after['calendar'][0]))
        print('      %-18s %r -> %r' % ('calendar[2]', node['calendar'][2], after['calendar'][2]))
        print('      PRESERVED (fall cycle, first-frost bound): %s' % preserved)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    for slug, zone, node, after, preserved in plan:
        for k, v in after.items():
            node[k] = json.loads(json.dumps(v))
        for k, v in preserved.items():                       # prove they did not move
            if node.get(k) != v:
                print('ABORT MID-APPLY: %s z%s preserved field %s changed' % (slug, zone, k))
                return 2

    finding = {
        'id': FINDING_ID,
        'severity': 'medium',
        'blocks_launch': False,
        'status': 'resolved',
        'summary': (
            'CORRECTED 2026-07-29: ca_desert z10/z11 SPRING plant_out opened on Jan 15, which IS '
            'those cells\' last_frost, so a frost-tender direct-sown cucurbit was scheduled onto '
            'the mean last-frost date. These cells already cited the PATHED UC planting-date page, '
            'and that page contradicts them: it gives cucumbers "Feb-May; Aug" and summer squash '
            '"Feb-Mar; Aug-Sep" for "Desert Valleys" (Imperial and Coachella). Frost is the wrong '
            'anchor -- this crop\'s own start_method notes require soil at about 70 degrees F at 2 '
            'inches and germination_temp_f starts at 70, and soil temperature lags frost by weeks. '
            'The SPRING segment now adopts z9\'s already-correct Feb 1 - Mar 15 opening; the FALL '
            'segment is untouched because it is first-frost bound and z10/z11 genuinely run later '
            'than z9 there (first frost Dec 31 vs Dec 15).'),
        'basis': (
            'UC Master Gardener planting-date table (California Master Gardener Handbook Table '
            '13.2) and U of A AZ1005 Maricopa calendar, both read directly (urllib + pypdf/fitz '
            'geometry, AZ1005 validated against a control row), never via a WebFetch summary. '
            'AZ1005\'s earliest seeding marks are Feb 15 for both Cucumbers and Squash, Summer. '
            'No new values invented: z9\'s spring segment was spliced in and each cell\'s own fall '
            'segment preserved byte-for-byte. Companion to the winter-cucurbit batch '
            '(ca_desert_z10_z11_soil_temp_floor_correction). SEPARATE and still open: the FALL '
            'windows run later than both sources (ours Sep 1 - Oct 1 vs UC "Aug"/"Aug-Sep" and '
            'AZ1005 Aug 15 / Sep 1 / Sep 15). RULED NOT A DEFECT and untouched: the 6 utah_dixie '
            'z8 cells, whose region note documents USU Extension\'s explicit Group C (Tender) '
            'March 15 St. George date running two weeks ahead of the March 30 last frost -- '
            'explicit source dates govern over arithmetic.'),
    }
    for slug in CROPS:
        vs = crops[slug].setdefault('verification_status', {})
        ofs = vs.setdefault('open_findings', [])
        if any(isinstance(f, dict) and f.get('id') == FINDING_ID for f in ofs):
            print('ABORT: finding already present on %s' % slug)
            return 2
        ofs.append(json.loads(json.dumps(finding)))

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(CANON, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d cells, %d findings added' % (len(plan), len(CROPS)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
