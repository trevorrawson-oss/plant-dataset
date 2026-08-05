#!/usr/bin/env python3
"""Adversarial tests for uscrn_coverage_scan.

The defect this scan exists to prevent is a SILENT gap -- a cell that quietly carries no record
and no reason. So the tests that matter are the ones proving an uncovered cell cannot be absorbed
into an explanation it does not deserve.
"""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_coverage_scan as S  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')


def cell(window='Apr 1 - Apr 30', rec=None, germ=(50, 85), propagule='seed'):
    crop = {'slug': 'x', 'propagule': propagule, 'germination_temp_f': list(germ),
            'zones': {'6': {'direct_sow': window,
                            'plantings': [{'direct_sow': [{'from': 'last_frost',
                                                           'uscrn_validation': rec}]}]}}}
    return {'crops': [crop]}


def table(zones=('6',), thresholds=('50',)):
    st = {'median_date': '04-15', 'p10_date': '03-28', 'p90_date': '05-02',
          'spread_days_p10_p90': 35, 'station_count': 12, 'station_year_count': 180,
          'crossed_count': 180, 'never_count': 0, 'never_rate': 0.0,
          'already_above_rate': 0.0, 'year_round': False, 'single_station': False,
          'confidence': 'high'}
    return {z: {t: dict(st) for t in thresholds} for z in zones}


class TestExplanations(unittest.TestCase):
    def test_a_covered_cell_is_covered(self):
        cov, reasons, unexp, zones = S.scan(cell(rec={'status': 'brackets_crossing'}), table())
        self.assertEqual(zones, 1)
        self.assertEqual(len(unexp), 0)
        self.assertEqual(sum(reasons.values()), 0)

    def test_a_zone_with_no_station_is_explained(self):
        _c, reasons, unexp, _z = S.scan(cell(), table(zones=('7',)))
        self.assertEqual(reasons['no_uscrn_station'], 1)
        self.assertEqual(unexp, [])

    def test_a_fall_only_cell_is_explained(self):
        _c, reasons, unexp, _z = S.scan(cell(window='Sep 1 - Oct 15'), table())
        self.assertEqual(reasons['no_spring_window'], 1)
        self.assertEqual(unexp, [])

    def test_a_threshold_off_the_ladder_is_explained(self):
        _c, reasons, unexp, _z = S.scan(cell(germ=(43, 85)), table())
        self.assertEqual(reasons['threshold_off_ladder'], 1)
        self.assertEqual(unexp, [])

    def test_a_crop_with_no_germination_band_is_explained(self):
        d = cell()
        del d['crops'][0]['germination_temp_f']
        _c, reasons, unexp, _z = S.scan(d, table())
        self.assertEqual(reasons['no_threshold'], 1)
        self.assertEqual(unexp, [])


class TestUnexplainedIsNotAbsorbed(unittest.TestCase):
    """The whole point: a real gap must survive as UNEXPLAINED, not be filed under a reason."""

    def test_a_comparable_cell_with_no_record_is_unexplained(self):
        _c, reasons, unexp, _z = S.scan(cell(rec=None), table())
        self.assertEqual(len(unexp), 1, 'a spring-sowing cell in a covered zone with a valid '
                                        'threshold and no record is a REAL gap')
        self.assertEqual(sum(reasons.values()), 0, 'and it must not be absorbed into a reason')

    def test_exit_code_is_nonzero_only_on_unexplained(self):
        self.assertEqual(S.scan(cell(rec={'status': 'x'}), table())[2], [])


class TestUnitsReconcile(unittest.TestCase):
    """Cell-zones must add up. Mixing units is how this arc's own denominator went wrong."""

    def test_every_eligible_cell_zone_is_accounted_for(self):
        data = json.load(open(CANON, encoding='utf-8'))
        tbl = (data.get('uscrn_soil_temp') or {}).get('zones')
        if not tbl:
            self.skipTest('canonical carries no uscrn_soil_temp yet')
        cov, reasons, unexp, zones = S.scan(data, tbl)
        total = zones + sum(reasons.values()) + len(unexp)
        self.assertEqual(total, len(list(S.eligible_cells(data))),
                         'covered + explained + unexplained must equal every eligible cell-zone')

    def test_live_canonical_has_no_unexplained_gap(self):
        data = json.load(open(CANON, encoding='utf-8'))
        tbl = (data.get('uscrn_soil_temp') or {}).get('zones')
        if not tbl:
            self.skipTest('canonical carries no uscrn_soil_temp yet')
        _c, _r, unexp, _z = S.scan(data, tbl)
        self.assertEqual(unexp, [], 'every uncovered cell must carry a named reason')


if __name__ == '__main__':
    unittest.main(verbosity=2)
