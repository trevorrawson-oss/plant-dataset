#!/usr/bin/env python3
"""Adversarial tests for uscrn_zone_table -- station-years -> per-zone soil crossing statistics.

The defect classes injected here are the ones that would put a confident, wrong date into the
canonical:

  - an UNWATCHED year counted as "the soil never got there" (absence-as-data; the same shape as
    `waf-block-pages-cached-as-absence`)
  - a median computed only over the years that DID cross, while most years did not -- which
    reports an early spring date for a threshold the zone barely reaches
  - a zone summarized from one station, or from a handful of station-years, without that being
    visible to the consumer
  - warm-zone SATURATION: where soil sits above the threshold all winter, every year crosses on
    Jan 1 and the "median crossing date" is an artifact of the calendar, not a spring event
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_zone_table as Z  # noqa: E402


def station(name, zone, years, thresh='50', scan_days=200):
    """years: {year: 'MM-DD' | None}; None means watched-but-never-crossed."""
    return {
        'station': name, 'zone': zone, 'lat': 35.0, 'lon': -80.0,
        'mean_annual_extreme_min_f': 0.0, 'zone_half': '%da' % zone,
        'scorable_years': sorted(int(y) for y in years),
        'soil_coverage': 0.9,
        'years': {str(y): {'soil_days_jan_jul': scan_days,
                           'crossings': {thresh: v}} for y, v in years.items()},
    }


class TestAttemptedYears(unittest.TestCase):
    def test_unwatched_year_is_not_a_never(self):
        s = station('A', 6, {2010: '04-01', 2011: None})
        s['years']['2011']['soil_days_jan_jul'] = 3      # essentially no observation
        t = Z.build_zone_table([s], min_station_years=1)['6']['50']
        self.assertEqual(t['station_year_count'], 1,
                         'a year with no soil observation must not be counted at all')
        self.assertEqual(t['never_count'], 0,
                         'an unwatched year is not evidence the soil never warmed')

    def test_watched_year_that_never_crosses_is_counted(self):
        s = station('A', 6, {2010: '04-01', 2011: None})
        t = Z.build_zone_table([s], min_station_years=1)['6']['50']
        self.assertEqual(t['station_year_count'], 2)
        self.assertEqual(t['never_count'], 1)
        self.assertAlmostEqual(t['never_rate'], 0.5, places=3)


class TestPercentiles(unittest.TestCase):
    def test_median_of_a_clean_spread(self):
        s = station('A', 6, {2010: '04-01', 2011: '04-05', 2012: '04-09',
                             2013: '04-13', 2014: '04-17'})
        t = Z.build_zone_table([s], min_station_years=1)['6']['50']
        self.assertEqual(t['median_date'], '04-09')
        self.assertEqual(t['p10_date'], '04-01')
        self.assertEqual(t['p90_date'], '04-17')
        self.assertEqual(t['spread_days_p10_p90'], 16)

    def test_never_years_are_excluded_from_the_median_but_flagged(self):
        # 1 year crossed in March, 4 years never -> a bare median would say "March"
        s = station('A', 6, {2010: '03-01', 2011: None, 2012: None, 2013: None, 2014: None})
        t = Z.build_zone_table([s], min_station_years=1)['6']['50']
        self.assertAlmostEqual(t['never_rate'], 0.8, places=3)
        self.assertEqual(t['confidence'], 'unreliable',
                         'a threshold missed in 80% of watched years cannot carry a median date')


class TestSaturation(unittest.TestCase):
    def test_all_years_crossing_jan_1_are_reported_as_year_round(self):
        s = station('A', 10, {y: '01-01' for y in range(2010, 2020)})
        t = Z.build_zone_table([s], min_station_years=1)['10']['50']
        self.assertAlmostEqual(t['already_above_rate'], 1.0, places=3)
        self.assertTrue(t['year_round'],
                        'soil above threshold at Jan 1 in every year is a year-round state, '
                        'not a spring crossing on Jan 1')

    def test_minority_saturation_is_not_year_round(self):
        yrs = {y: '01-01' for y in range(2010, 2014)}
        yrs.update({y: '03-%02d' % (y - 2000) for y in range(2014, 2020)})
        t = Z.build_zone_table([station('A', 9, yrs)], min_station_years=1)['9']['50']
        self.assertAlmostEqual(t['already_above_rate'], 0.4, places=3)
        self.assertFalse(t['year_round'])

    def test_majority_saturation_is_year_round(self):
        # zone 8 at 40F measures 67% already-above: a real case, and the median there is 01-01
        yrs = {y: '01-01' for y in range(2010, 2017)}
        yrs.update({y: '02-%02d' % (y - 2006) for y in range(2017, 2020)})
        t = Z.build_zone_table([station('A', 8, yrs)], min_station_years=1)['8']['50']
        self.assertAlmostEqual(t['already_above_rate'], 0.7, places=3)
        self.assertTrue(t['year_round'])


class TestCoverageVisibility(unittest.TestCase):
    def test_station_and_station_year_counts_are_reported(self):
        ss = [station('A', 6, {2010: '04-01', 2011: '04-03'}),
              station('B', 6, {2010: '04-05', 2011: '04-07', 2012: '04-09'})]
        t = Z.build_zone_table(ss, min_station_years=1)['6']['50']
        self.assertEqual(t['station_count'], 2)
        self.assertEqual(t['station_year_count'], 5)

    def test_below_the_floor_is_marked_insufficient_not_dropped(self):
        t = Z.build_zone_table([station('A', 6, {2010: '04-01'})],
                               min_station_years=30)['6']['50']
        self.assertEqual(t['confidence'], 'insufficient')
        self.assertEqual(t['station_year_count'], 1)
        self.assertIsNotNone(t['median_date'],
                             'the number is kept and labelled, not silently dropped')

    def test_single_station_zone_is_flagged(self):
        t = Z.build_zone_table([station('A', 6, {y: '04-01' for y in range(2010, 2026)})],
                               min_station_years=10)['6']['50']
        self.assertEqual(t['station_count'], 1)
        self.assertTrue(t['single_station'],
                        'a zone summarized from one station must say so')

    def test_multi_station_zone_is_not_flagged(self):
        ss = [station('A', 6, {y: '04-01' for y in range(2010, 2026)}),
              station('B', 6, {y: '04-05' for y in range(2010, 2026)})]
        t = Z.build_zone_table(ss, min_station_years=10)['6']['50']
        self.assertFalse(t['single_station'])
        self.assertEqual(t['confidence'], 'high')


class TestZoneWithNoStations(unittest.TestCase):
    def test_absent_zone_is_absent_not_zero(self):
        table = Z.build_zone_table([station('A', 6, {2010: '04-01'})], min_station_years=1)
        self.assertNotIn('11', table,
                         'a zone with no USCRN station must be absent, never an empty record '
                         'that reads as a measurement')


if __name__ == '__main__':
    unittest.main(verbosity=2)
