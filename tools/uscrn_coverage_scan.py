#!/usr/bin/env python3
"""USCRN VALIDATION COVERAGE: every eligible direct-sow cell either carries a record or has a
reason it cannot.

SOFT, as of 2026-08-04, by Trevor's ruling. `uscrn_validation` deliberately has NO row in
`docs/field_addition_register.md` and is NOT an A39 presence-or-null cert requirement. The reason
is measured, not stylistic: the field is meaningful on 408 of 6,579 date entries, and on ZERO
entries for all 31 tree, berry and mushroom crops, none of which is ever seed-sown in a garden. A
hard presence-or-null rule would oblige every future fruit tree to carry a field that can never be
populated for it -- a certification treadmill bought for nothing. This scan is what replaces it:
it makes the gap VISIBLE without making it BLOCKING, in the shape of `soil_temp_floor_scan.py`.

WHAT IT ASKS. For every `direct_sow` cell on a seed-propagated crop, is there a record? If not,
exactly one of these must explain it, and the scan says which:

  no_uscrn_station   -- the cell's zone has no USCRN station. Zones 11, 12 and 13 are empty in the
                        archive, full stop; no method fixes that from this data.
  no_spring_window   -- the cell sows only in autumn, so there is no spring crossing to compare.
  threshold_off_ladder -- the crop's germination floor is not a measured threshold. Refused rather
                        than rounded to a neighbouring one.
  no_threshold       -- the crop carries no `germination_temp_f` at all.

Anything left over is an UNEXPLAINED gap and is what this scan exists to surface. As of the
promote it is 0.

HARD-FLIP CONDITION: if a future pass makes the direct-sow slice fully explainable AND the
threshold basis moves off the optimal-band floor (PLA-118, the real germination-minimum field),
revisit whether a register row is finally warranted. Do not flip on coverage alone -- coverage was
never the objection.

    $ python3 tools/uscrn_coverage_scan.py
    $ python3 tools/uscrn_coverage_scan.py --stages    # the eligibility narrowing, with counts
    $ python3 tools/uscrn_coverage_scan.py --risk      # the cells whose window runs ahead of soil
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_validate as UV  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')


def eligible_cells(data):
    """Yield (crop, kind, cid, zone, arm, window) for every direct-sow cell that could carry one."""
    for crop in data['crops']:
        if crop.get('propagule') != 'seed':
            continue
        for cid, node in sorted((crop.get('zones') or {}).items()):
            arms = (node.get('plantings') or [{}])[0].get('direct_sow') or []
            if arms and 'uscrn_validation' in arms[0]:
                yield crop, 'zones', cid, cid, arms[0], node.get('direct_sow')
        for cid, region in sorted((crop.get('regions') or {}).items()):
            arms = (region.get('plantings') or [{}])[0].get('direct_sow') or []
            if not (arms and 'uscrn_validation' in arms[0]):
                continue
            for zone, rnode in sorted((region.get('resolved_by_zone') or {}).items()):
                yield (crop, 'regions', cid, zone, arms[0],
                       rnode.get('direct_sow') or rnode.get('plant_out'))


def scan(data, table):
    """-> (covered_cells, reasons Counter, unexplained list, covered_cell_zones).

    TWO UNITS, reported separately and on purpose. A region cell carries ONE record covering
    several zones, so "cells with a record" (228) and "cell-zones covered" (532) are different
    numbers and only the second is commensurable with the per-zone reasons below. Collapsing them
    into one figure is how this arc's own denominator went wrong in the first place.
    """
    covered, unexplained = set(), []
    covered_zones = 0
    reasons = collections.Counter()
    for crop, kind, cid, zone, arm, window in eligible_cells(data):
        rec = crop[kind][cid]['plantings'][0]['direct_sow'][0].get('uscrn_validation')
        key = (crop['slug'], kind, cid)
        if rec:
            covered.add(key)
            covered_zones += 1
            continue
        zt = table.get(str(zone))
        if not zt:
            reasons['no_uscrn_station'] += 1
            continue
        thr, _prov = UV.crop_threshold(crop, arm, ladder=zt)
        if thr is None:
            g = crop.get('germination_temp_f')
            reasons['no_threshold' if not g else 'threshold_off_ladder'] += 1
            continue
        if UV.spring_sow_window(window) is None:
            reasons['no_spring_window'] += 1
            continue
        unexplained.append((crop['slug'], kind, cid, zone, window))
    return covered, reasons, unexplained, covered_zones


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stages', action='store_true')
    ap.add_argument('--risk', action='store_true')
    ap.add_argument('candidate', nargs='?', default=CANON)
    args = ap.parse_args()

    data = json.load(open(args.candidate, encoding='utf-8'))
    table = (data.get('uscrn_soil_temp') or {}).get('zones')
    if not table:
        print('uscrn_soil_temp is not in this canonical; nothing to scan against.')
        return 0

    covered, reasons, unexplained, covered_zones = scan(data, table)

    if args.stages:
        cells = list(eligible_cells(data))
        crops_seed = {c['slug'] for c in data['crops'] if c.get('propagule') == 'seed'}
        print('eligibility narrowing:')
        print('  crops on the roster                   : %3d' % len(data['crops']))
        print('  + propagule == seed                   : %3d' % len(crops_seed))
        print('  direct-sow cell-zones on those crops  : %3d' % len(cells))
        print('  -> cell-zones covered by a record     : %3d' % covered_zones)
        print('  -> distinct cells carrying a record   : %3d  (a region record covers its span)'
              % len(covered))
        print()

    print('USCRN validation coverage over the direct-sow slice')
    print('=' * 84)
    total = covered_zones + sum(reasons.values()) + len(unexplained)
    print('  cell-zones covered         : %d  (%d distinct cells)' % (covered_zones, len(covered)))
    for reason, n in reasons.most_common():
        print('  %-26s : %d' % (reason, n))
    print('  %-26s : %d' % ('UNEXPLAINED', len(unexplained)))
    print('  %-26s : %d' % ('total cell-zones', total))
    if unexplained:
        print('-' * 84)
        for slug, kind, cid, zone, window in unexplained[:40]:
            print('  %-22s %-9s %-16s z%-4s %r' % (slug, kind, cid, zone, window))
        print('\nRead every one before acting: an unexplained gap is either a real miss or a')
        print('category this scan does not yet name. Adding a category is a deliberate act.')
    else:
        print('-' * 84)
        print('  every uncovered cell has a named reason.')

    if args.risk:
        flagged = []
        for crop, kind, cid, _z, _a, _w in eligible_cells(data):
            rec = crop[kind][cid]['plantings'][0]['direct_sow'][0].get('uscrn_validation')
            if rec and rec.get('risk'):
                flagged.append((rec['risk'], crop['slug'], cid, rec))
        seen = set()
        print()
        print('DIRECTIONAL RISK -- sowing window runs ahead of the measured soil record')
        print('-' * 84)
        for risk, slug, cid, rec in sorted(flagged, key=lambda f: (f[0] != 'high', f[1])):
            if (slug, cid) in seen:
                continue
            seen.add((slug, cid))
            print('  %-9s %-22s %-16s stored %s  median %s  %s'
                  % (risk, slug, cid, rec['stored_date'], rec['uscrn_median_date'],
                     rec['anchor_threshold']))
        print('\nNOT a defect list. The threshold is the crop\'s OPTIMAL germination floor, which')
        print('reads early by construction; PLA-118 authors the real germination minimum.')

    return 1 if unexplained else 0


if __name__ == '__main__':
    sys.exit(main())
