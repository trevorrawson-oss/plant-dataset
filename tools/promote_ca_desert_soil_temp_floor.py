#!/usr/bin/env python3
"""GUARDED PROMOTE: ca_desert z10/z11 winter-cucurbit spring windows off the frost date.

THE DEFECT. `acorn-squash`, `butternut-squash`, `spaghetti-squash` and `pumpkin` open their
ca_desert z10/z11 spring `plant_out` on `Jan 15`, and those cells' `resolved_from.last_frost`
IS `Jan 15`. So a frost-tender, direct-sown cucurbit is scheduled to go in the ground on the
mean last-frost date -- a coin flip on frost -- and 10 days earlier than the region's own
declared arm (`plant_out = last_frost + 10`).

WHY FROST IS THE WRONG ANCHOR HERE, in the crops' own words. `start_method.notes_seasoned`
on all four says direct sowing works "once the soil is reliably warm (at least 65 degrees F,
ideally 70 degrees F, at 2 inches)", and `germination_temp_f` is [70, 95]. Soil temperature
lags frost by weeks, so "frost has passed" does not mean "the soil will germinate seed".
The data already contained its own contradiction: the prose says wait for 70F soil, the
calendar said plant on the frost date.

EXTERNAL CORROBORATION (both fetched and read directly this session, urllib + pypdf/fitz --
never a WebFetch summary, per the kickoff sec 7 trap):
  - UC, "Recommended planting dates for major regions of California" (Master Gardener
    Handbook Table 13.2), https://ucanr.edu/program/uc-master-gardener-program/time-planting
    -- "squash, winter" x "Desert Valleys" (defined on the page as "Imperial and Coachella
    Valleys") = "Feb-March; Aug". January is outside it.
  - U of A AZ1005, Vegetable Planting Calendar for Maricopa County -- "Squash, Winter"
    earliest seeding mark is Mar 1, and the page directs growers to "check for optimal soil
    temperatures to be in a range of 65 to 85 degrees F".
  - pumpkin's own verification_log_ref already cites UMN for "soil 65F at 2in".

THE FIX. z10/z11 adopt z9's window and calendar. z9 (last frost Jan 31) already resolves to
`Feb 1 - Mar 1` with January as `cold_pause`, which is exactly the shape the sources support,
so no new numbers are invented -- the correct sibling is copied. Feb 1 sits inside UC's
"Feb-March". The spring harvest slides Apr 15-May 31 -> May 15-Jun 15, which also retires the
odd z10/z11 `season_over` June token (z9 has `harvest` there).

Note the sources give ONE desert window with no zone split, so z9/z10/z11 windows matching is
correct rather than suspicious -- the same call the rgv region documents ("the TAMU AgriLife
sources describe a single Valley-wide planting calendar, not a zone-9/zone-10 split").
Hardiness zones describe winter lows, not soil warmth, so a warmer zone does not license an
earlier sowing.

NOT IN SCOPE (deliberately, and surfaced instead of smuggled in):
  - The `Jul 1 - Jul 31` SECOND planting on these cells. UC says "Aug" and AZ1005 supports
    July; that is a separate adjudication.
  - The SAME Jan-15 defect on 6 more ca_desert z10/z11 crops (cucumber, slicing-cucumber,
    english-cucumber, pickling-cucumber, zucchini-courgette, yellow-summer-squash) and on 6
    utah_dixie z8 cells that open 15 days BEFORE last frost. Measured by
    tools/soil_temp_floor_scan.py; awaiting a decision.

FOOTPRINT: exactly 8 nodes x 7 keys, plus one open_finding per crop. Nothing else.
COMPACT preserved: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_ca_desert_soil_temp_floor.py --dry-run
    $ python3 tools/promote_ca_desert_soil_temp_floor.py --apply
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

# pinned pre-state -- abort on any drift
BASE_SHA = 'dd24b180939de37117719b96aec974873dfc8263ab8104af7f6026acdbf856f7'

CROPS = ['acorn-squash', 'butternut-squash', 'spaghetti-squash', 'pumpkin']
REGION = 'ca_desert'
ZONES = ['10', '11']
TEMPLATE_ZONE = '9'

# the exact pre-state each target cell must be in, or we abort
EXPECT_BEFORE = {
    'plant_out': 'Jan 15 - Feb 15',
    'first_plant_date': 'Jan 15',
    'last_plant_date': 'Feb 15',
    'harvest': 'Apr 15 - May 31',
    'harvest_start': 'Apr 15',
    'harvest_end': 'May 31',
    'calendar': ['plant', 'plant', 'growing', 'harvest', 'harvest', 'season_over',
                 'plant', 'growing', 'growing', 'harvest', 'harvest', 'cold_pause'],
}
KEYS = list(EXPECT_BEFORE)

FINDING_ID = 'ca_desert_z10_z11_soil_temp_floor_correction'
FINDING = {
    'id': FINDING_ID,
    'severity': 'medium',
    'blocks_launch': False,
    'status': 'resolved',
    'summary': (
        'CORRECTED 2026-07-29: ca_desert z10/z11 spring plant_out opened on Jan 15, which IS '
        'those cells\' last_frost, so a frost-tender direct-sown cucurbit was scheduled onto the '
        'mean last-frost date and 10 days earlier than the region arm\'s own last_frost+10 rule. '
        'Frost is the wrong anchor: this crop\'s own start_method notes require soil "reliably '
        'warm (at least 65 degrees F, ideally 70 degrees F, at 2 inches)" and germination_temp_f '
        'is [70,95], and soil temperature lags frost by weeks. Windows now adopt z9\'s already-'
        'correct Feb 1 - Mar 1 / May 15 - Jun 15 shape with January as cold_pause.'),
    'basis': (
        'UC Master Gardener planting-date table (California Master Gardener Handbook Table 13.2) '
        'gives winter squash x "Desert Valleys" (Imperial and Coachella) as "Feb-March; Aug", '
        'placing January outside it; U of A AZ1005 Maricopa calendar has its earliest winter-squash '
        'seeding mark at Mar 1 and directs growers to soil of 65 to 85 degrees F. Both read '
        'directly (urllib + pypdf/fitz geometry, AZ1005 validated against a control row), not via '
        'a WebFetch summary. No new values invented: z9 already resolved correctly and was copied. '
        'The sources give one desert window with no zone split, so matching z9/z10/z11 is correct '
        'here, as the rgv region documents for its own Valley-wide calendar. SEPARATE and still '
        'open: the Jul 1 - Jul 31 second planting (UC says Aug, AZ1005 supports July), and the '
        'same Jan-15 opening on 6 more ca_desert cucurbits plus 6 utah_dixie z8 cells '
        '(tools/soil_temp_floor_scan.py).'),
}


def load_raw():
    with open(CANON, 'rb') as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    raw = load_raw()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != BASE_SHA:
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (BASE_SHA, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    crops = {c['slug']: c for c in data['crops']}

    # --- read the template ONCE per crop and verify it is the shape we expect ---
    plan = []
    for slug in CROPS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        rbz = ((crop.get('regions') or {}).get(REGION) or {}).get('resolved_by_zone') or {}
        tpl = rbz.get(TEMPLATE_ZONE)
        if not isinstance(tpl, dict):
            print('ABORT: %s %s z%s template missing' % (slug, REGION, TEMPLATE_ZONE))
            return 2
        # the template must itself be the corrected shape
        if tpl.get('plant_out') != 'Feb 1 - Mar 1' or tpl.get('calendar', [None])[0] != 'cold_pause':
            print('ABORT: %s z%s template is not the expected corrected shape: %r' % (
                slug, TEMPLATE_ZONE, tpl.get('plant_out')))
            return 2
        after = {k: tpl[k] for k in KEYS}
        for zone in ZONES:
            node = rbz.get(zone)
            if not isinstance(node, dict):
                print('ABORT: %s %s z%s missing' % (slug, REGION, zone))
                return 2
            for k, want in EXPECT_BEFORE.items():
                if node.get(k) != want:
                    print('ABORT: %s z%s.%s pre-state mismatch\n  expected %r\n  found    %r' % (
                        slug, zone, k, want, node.get(k)))
                    return 2
            plan.append((slug, zone, node, after))

    print('pre-state verified on all %d target cells' % len(plan))
    if len(plan) != len(CROPS) * len(ZONES):
        print('ABORT: expected %d cells, planned %d' % (len(CROPS) * len(ZONES), len(plan)))
        return 2

    # --- report the change ---
    for slug, zone, _node, after in plan:
        print('\n  %s %s z%s' % (slug, REGION, zone))
        for k in KEYS:
            print('      %-18s %r\n      %-18s -> %r' % (
                k, EXPECT_BEFORE[k], '', after[k]))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    # --- apply ---
    touched = 0
    for slug, zone, node, after in plan:
        for k in KEYS:
            node[k] = json.loads(json.dumps(after[k]))   # deep copy, no shared refs
        touched += 1

    findings_added = 0
    for slug in CROPS:
        vs = crops[slug].setdefault('verification_status', {})
        ofs = vs.setdefault('open_findings', [])
        if any(isinstance(f, dict) and f.get('id') == FINDING_ID for f in ofs):
            print('ABORT: finding %s already present on %s' % (FINDING_ID, slug))
            return 2
        ofs.append(json.loads(json.dumps(FINDING)))
        findings_added += 1

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(CANON, 'wb') as fh:
        fh.write(out)
    new_sha = hashlib.sha256(out).hexdigest()
    print('\nAPPLIED: %d cells x %d keys, %d findings added' % (
        touched, len(KEYS), findings_added))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % new_sha)
    return 0


if __name__ == '__main__':
    sys.exit(main())
