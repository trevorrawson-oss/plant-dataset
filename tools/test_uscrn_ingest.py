#!/usr/bin/env python3
"""Adversarial tests for uscrn_ingest -- the USCRN CRND0103 daily-archive parser.

Every test here injects a defect class into synthetic station rows and confirms the parser
refuses it, per CLAUDE.md's RED-before-GREEN rule. The defect classes that matter:

  - the -9999.0 missing sentinel read as a real temperature (it is -9999C; a crossing scan
    that treats it as a number would find "soil never warms" everywhere, or worse, would
    average it into an annual minimum and hand every station zone 1)
  - a sustained crossing declared across a DATA GAP (4 warm days, a hole, one more warm day
    is not 5 sustained days of evidence)
  - a single warm day counted as a crossing (the whole point of the 5-day sustain window)
  - an autumn re-crossing beating the spring one (scan order must be date order)
  - a year whose winter is missing scored for its annual extreme minimum (a station that
    lost January reports a falsely warm minimum, which walks it a zone or two south)
"""
import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_ingest as U  # noqa: E402


def row(date, tmin_c=10.0, soil5_c=10.0, lat=35.0, lon=-80.0):
    """Build one CRND0103 daily record as the 28 whitespace-separated fields the archive uses."""
    f = ['-9999.0'] * 28
    f[0] = '99999'
    f[1] = date.strftime('%Y%m%d')
    f[2] = '2.423'
    f[3] = '%.2f' % lon
    f[4] = '%.2f' % lat
    f[6] = '-9999.0' if tmin_c is None else '%.1f' % tmin_c
    f[11] = 'C'
    f[23] = '-9999.0' if soil5_c is None else '%.1f' % soil5_c
    return ' '.join(f)


def year_rows(year, soil_by_doy=None, tmin_by_doy=None, default_soil=0.0, default_tmin=0.0):
    """A full calendar year of rows; soil_by_doy/tmin_by_doy override individual days (1-indexed)."""
    soil_by_doy = soil_by_doy or {}
    tmin_by_doy = tmin_by_doy or {}
    out = []
    d = datetime.date(year, 1, 1)
    doy = 1
    while d.year == year:
        out.append(row(d,
                       tmin_c=tmin_by_doy.get(doy, default_tmin),
                       soil5_c=soil_by_doy.get(doy, default_soil)))
        d += datetime.timedelta(days=1)
        doy += 1
    return out


class TestSentinels(unittest.TestCase):
    def test_missing_sentinel_is_not_a_temperature(self):
        r = U.parse_row(row(datetime.date(2015, 3, 1), tmin_c=None, soil5_c=None))
        self.assertIsNone(r.soil5_f, '-9999.0 soil temp must parse as None, not -9999')
        self.assertIsNone(r.tmin_f, '-9999.0 air min must parse as None, not -9999')

    def test_real_reading_converts_c_to_f(self):
        r = U.parse_row(row(datetime.date(2015, 3, 1), tmin_c=0.0, soil5_c=10.0))
        self.assertAlmostEqual(r.soil5_f, 50.0, places=3)
        self.assertAlmostEqual(r.tmin_f, 32.0, places=3)

    def test_coordinates_parse(self):
        r = U.parse_row(row(datetime.date(2015, 3, 1), lat=35.49, lon=-82.61))
        self.assertAlmostEqual(r.lat, 35.49, places=2)
        self.assertAlmostEqual(r.lon, -82.61, places=2)


class TestCrossing(unittest.TestCase):
    """first_sustained_crossing: first day beginning SUSTAIN consecutive days at/above threshold."""

    def series(self, **kw):
        return U.parse_rows(year_rows(2015, **kw))

    def test_five_sustained_days_cross(self):
        # cold all year except doy 100-104 at 15C (59F), threshold 50F
        s = self.series(soil_by_doy={d: 15.0 for d in range(100, 105)}, default_soil=0.0)
        got = U.first_sustained_crossing(s, 50.0, sustain=5)
        self.assertEqual(got, datetime.date(2015, 4, 10))  # doy 100

    def test_four_warm_days_do_not_cross(self):
        s = self.series(soil_by_doy={d: 15.0 for d in range(100, 104)}, default_soil=0.0)
        self.assertIsNone(U.first_sustained_crossing(s, 50.0, sustain=5),
                          'four sustained days is not five; must not report a crossing')

    def test_single_warm_spike_does_not_cross(self):
        s = self.series(soil_by_doy={150: 30.0}, default_soil=0.0)
        self.assertIsNone(U.first_sustained_crossing(s, 50.0, sustain=5))

    def test_gap_inside_the_window_blocks_the_crossing(self):
        # doy 100,101 warm; 102 MISSING; 103,104,105 warm -> not 5 sustained VALID days
        warm = {d: 15.0 for d in (100, 101, 103, 104, 105)}
        warm[102] = None
        s = self.series(soil_by_doy=warm, default_soil=0.0)
        self.assertIsNone(U.first_sustained_crossing(s, 50.0, sustain=5),
                          'a missing day inside the window is not evidence of sustained warmth')

    def test_gap_does_not_silently_shift_the_date_earlier(self):
        # a real 5-day run starts at 110; a broken run sits at 100. Must report 110.
        warm = {d: 15.0 for d in (100, 101, 103, 104)}
        warm[102] = None
        warm.update({d: 15.0 for d in range(110, 116)})
        s = self.series(soil_by_doy=warm, default_soil=0.0)
        self.assertEqual(U.first_sustained_crossing(s, 50.0, sustain=5),
                         datetime.date(2015, 4, 20))  # doy 110

    def test_spring_crossing_beats_autumn_recrossing(self):
        # warm Apr-Sep; the scan must return the APRIL date, not a later one
        s = self.series(soil_by_doy={d: 20.0 for d in range(91, 274)}, default_soil=0.0)
        self.assertEqual(U.first_sustained_crossing(s, 50.0, sustain=5),
                         datetime.date(2015, 4, 1))

    def test_already_above_at_year_start(self):
        s = self.series(default_soil=25.0)  # 77F all year
        self.assertEqual(U.first_sustained_crossing(s, 50.0, sustain=5),
                         datetime.date(2015, 1, 1))

    def test_never_reached_returns_none(self):
        s = self.series(default_soil=0.0)
        self.assertIsNone(U.first_sustained_crossing(s, 50.0, sustain=5))

    def test_threshold_is_inclusive(self):
        s = self.series(soil_by_doy={d: 10.0 for d in range(100, 106)}, default_soil=0.0)
        self.assertEqual(U.first_sustained_crossing(s, 50.0, sustain=5),
                         datetime.date(2015, 4, 10), '10C == 50F must count as reaching 50F')


class TestAnnualExtremeMin(unittest.TestCase):
    def test_extreme_min_is_the_minimum_daily_min(self):
        s = U.parse_rows(year_rows(2015, tmin_by_doy={40: -20.0}, default_tmin=5.0))
        lo, valid = U.annual_extreme_min(s)
        self.assertAlmostEqual(lo, -4.0, places=3)  # -20C == -4F
        self.assertEqual(valid, 365)

    def test_sentinel_days_are_not_the_minimum(self):
        s = U.parse_rows(year_rows(2015, tmin_by_doy={40: None}, default_tmin=5.0))
        lo, valid = U.annual_extreme_min(s)
        self.assertAlmostEqual(lo, 41.0, places=3)  # 5C == 41F
        self.assertEqual(valid, 364)

    def test_year_missing_its_winter_is_rejected_by_the_coverage_rule(self):
        # drop all of January -> a falsely warm annual minimum
        s = U.parse_rows(year_rows(2015, tmin_by_doy={d: None for d in range(1, 32)},
                                   default_tmin=5.0))
        self.assertFalse(U.year_is_scorable(s),
                         'a year missing January must not score an annual extreme minimum')

    def test_complete_year_is_scorable(self):
        self.assertTrue(U.year_is_scorable(U.parse_rows(year_rows(2015, default_tmin=5.0))))


class TestUsdaZone(unittest.TestCase):
    """zone = floor((T+60)/10)+1 over the mean annual extreme minimum, half a/b on the 5F split."""

    def test_known_boundaries(self):
        for temp_f, expect in [(-40, '3a'), (-35, '3b'), (-30, '4a'), (0, '7a'), (5, '7b'),
                               (12, '8a'), (17, '8b'), (22, '9a'), (32, '10a'), (44, '11a'),
                               (46, '11b')]:
            self.assertEqual(U.usda_zone(temp_f), expect, 'mean extreme min %sF' % temp_f)

    def test_zone_int_strips_the_half(self):
        self.assertEqual(U.usda_zone_int(12), 8)
        self.assertEqual(U.usda_zone_int(-35), 3)

    def test_clamped_to_the_published_range(self):
        self.assertEqual(U.usda_zone_int(-100), 1)
        self.assertEqual(U.usda_zone_int(200), 13)


if __name__ == '__main__':
    unittest.main(verbosity=2)
