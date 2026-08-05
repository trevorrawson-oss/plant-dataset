#!/usr/bin/env python3
"""Adversarial tests for uscrn_validate -- the crop x zone soil-temperature comparison.

Defect classes injected here, each of which would put a confident wrong verdict in the canonical:

  - validating a crop against the WRONG threshold (the shipped pilot did exactly this: bok-choy,
    whose germination floor is 45F, carries a record computed at 40F, copied wholesale from
    lettuce -- see the arc doc)
  - reading a FALL sowing window as the spring one, which compares an October date against an
    April soil crossing and reports a 200-day "misalignment"
  - emitting a verdict from a zone the USCRN network does not cover, or from an `unreliable` /
    `insufficient` zone record, without saying so
  - treating a warm zone's Jan-1 saturation as a real spring crossing
  - losing the SIGN of the comparison: sowing 20 days after the soil is ready is a gardener's
    choice, sowing 20 days before it is seed rot. A symmetric band cannot tell those apart.
  - reading a sowing WINDOW as if it were a point: a window opens before the typical crossing by
    construction, so an opening-date comparison calls healthy cells too cold.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_validate as V  # noqa: E402


def zone_stats(median='04-15', p10='03-28', p90='05-02', conf='high',
               year_round=False, station_count=12, station_year_count=180):
    return {'median_date': median, 'p10_date': p10, 'p90_date': p90,
            'spread_days_p10_p90': 35, 'station_count': station_count,
            'station_year_count': station_year_count, 'crossed_count': station_year_count,
            'never_count': 0, 'never_rate': 0.0, 'already_above_rate': 0.0,
            'year_round': year_round, 'single_station': False, 'confidence': conf}


class TestSpringWindow(unittest.TestCase):
    def test_picks_the_spring_segment(self):
        self.assertEqual(V.spring_sow_date('Apr 15 - May 6, Aug 3 - Aug 24'), (4, 15))

    def test_picks_spring_when_fall_is_listed_first(self):
        # lettuce zone 8 stores its fall arm first; a naive "first segment" read gets September
        self.assertEqual(V.spring_sow_date('Sep 23 - Nov 7, Feb 1 - Feb 22'), (2, 1))

    def test_fall_only_cell_has_no_spring_sowing(self):
        self.assertIsNone(V.spring_sow_date('Sep 23 - Nov 7'))

    def test_month_only_span_uses_the_first_of_the_month(self):
        self.assertEqual(V.spring_sow_date('March - May'), (3, 1))

    def test_unparseable_string_is_none_not_a_guess(self):
        self.assertIsNone(V.spring_sow_date('when the soil is workable'))
        self.assertIsNone(V.spring_sow_date(None))


class TestThreshold(unittest.TestCase):
    def test_declared_soil_anchor_wins(self):
        crop = {'germination_temp_f': [35, 75], 'propagule': 'seed'}
        thr, prov = V.crop_threshold(crop, {'from': 'soil_temp_40f'})
        self.assertEqual(thr, 40)
        self.assertIn('planting arm', prov)

    def test_falls_back_to_the_germination_floor(self):
        crop = {'germination_temp_f': [45, 85], 'propagule': 'seed'}
        thr, prov = V.crop_threshold(crop, {'from': 'last_frost'})
        self.assertEqual(thr, 45, 'bok-choy must validate at ITS floor (45F), never lettuce\'s 40F')
        self.assertIn('germination_temp_f', prov)

    def test_no_germination_band_yields_no_threshold(self):
        thr, prov = V.crop_threshold({'propagule': 'seed'}, {'from': 'last_frost'})
        self.assertIsNone(thr)
        self.assertIsNone(prov)

    def test_threshold_off_the_ladder_is_refused(self):
        # a floor the ingest never measured must not be silently rounded to a neighbour
        ladder = {'40': {}, '45': {}, '50': {}}
        crop = {'germination_temp_f': [43, 85], 'propagule': 'seed'}
        thr, _ = V.crop_threshold(crop, {'from': 'last_frost'}, ladder=ladder)
        self.assertIsNone(thr, '43F is not on the measured ladder; refuse rather than round')
        on, _ = V.crop_threshold({'germination_temp_f': [45, 85], 'propagule': 'seed'},
                                 {'from': 'last_frost'}, ladder=ladder)
        self.assertEqual(on, 45, 'a floor ON the ladder must still resolve')

    def test_declared_anchor_off_the_ladder_is_also_refused(self):
        ladder = {'40': {}, '45': {}}
        thr, _ = V.crop_threshold({'germination_temp_f': [40, 85], 'propagule': 'seed'},
                                  {'from': 'soil_temp_42f'}, ladder=ladder)
        self.assertIsNone(thr, 'an unmeasured declared anchor must not fall back to the floor')


class TestClassify(unittest.TestCase):
    def test_bands_follow_the_phase_1_1_methodology(self):
        self.assertEqual(V.classify_offset(0), 'aligned')
        self.assertEqual(V.classify_offset(3), 'aligned')
        self.assertEqual(V.classify_offset(-3), 'aligned')
        self.assertEqual(V.classify_offset(4), 'drift')
        self.assertEqual(V.classify_offset(-10), 'drift')
        self.assertEqual(V.classify_offset(11), 'misaligned')
        self.assertEqual(V.classify_offset(-40), 'misaligned')



class TestPosition(unittest.TestCase):
    """The verdict compares the sowing WINDOW against the measured crossing distribution."""

    ST = dict(median='04-15', p10='03-28', p90='05-02')

    def test_window_closing_before_p10_is_the_defect_shape(self):
        st = zone_stats(**self.ST)
        self.assertEqual(V.position(((2, 1), (3, 1)), st), 'window_too_early')

    def test_window_closing_before_the_median_opens_early(self):
        st = zone_stats(**self.ST)
        self.assertEqual(V.position(((3, 1), (4, 5)), st), 'opens_early')

    def test_window_containing_the_median_is_healthy(self):
        st = zone_stats(**self.ST)
        self.assertEqual(V.position(((4, 1), (4, 30)), st), 'brackets_crossing')

    def test_a_long_window_opening_early_still_brackets(self):
        """The whole reason the opening-date read was dropped: a wide window is not a defect."""
        st = zone_stats(**self.ST)
        self.assertEqual(V.position(((2, 15), (5, 30)), st), 'brackets_crossing')

    def test_window_opening_after_p90_is_late_not_flagged(self):
        st = zone_stats(**self.ST)
        self.assertEqual(V.position(((6, 1), (6, 20)), st), 'opens_late')
        self.assertIsNone(V.risk_level(((6, 1), (6, 20)), st),
                          'sowing after the soil is ready is a choice, never a defect')

    def test_year_round_zone_short_circuits(self):
        st = zone_stats(year_round=True)
        self.assertEqual(V.position(((2, 1), (3, 1)), st), 'not_soil_limited')

    def test_risk_is_only_ever_raised_on_the_early_side(self):
        st = zone_stats(**self.ST)
        self.assertEqual(V.risk_level(((2, 1), (3, 1)), st), 'high')
        self.assertEqual(V.risk_level(((3, 1), (4, 5)), st), 'moderate')
        self.assertIsNone(V.risk_level(((4, 1), (4, 30)), st))


class TestSpringWindowSpan(unittest.TestCase):
    def test_window_end_is_parsed(self):
        self.assertEqual(V.spring_sow_window('Apr 15 - May 6, Aug 3 - Aug 24'),
                         ((4, 15), (5, 6)))

    def test_month_only_end_uses_the_last_of_the_month(self):
        self.assertEqual(V.spring_sow_window('March - May'), ((3, 1), (5, 31)))

    def test_spring_window_chosen_when_fall_listed_first(self):
        self.assertEqual(V.spring_sow_window('Sep 23 - Nov 7, Feb 1 - Feb 22'),
                         ((2, 1), (2, 22)))


class TestRecord(unittest.TestCase):
    def crop(self, **kw):
        c = {'slug': 'x', 'propagule': 'seed', 'germination_temp_f': [50, 85]}
        c.update(kw)
        return c

    def test_happy_path(self):
        r = V.build_record(self.crop(), {'from': 'last_frost'}, '5',
                           'Apr 20 - May 10', {'50': zone_stats()})
        self.assertEqual(r['stored_date'], '04-20')
        self.assertEqual(r['uscrn_median_date'], '04-15')
        self.assertEqual(r['offset_days_median'], 5)
        self.assertEqual(r['status'], 'brackets_crossing')
        self.assertEqual(r['offset_band'], 'drift',
                         'the Phase 1.1 magnitude band is still reported alongside the verdict')
        self.assertEqual(r['anchor_threshold'], 'soil 50F reached at 5cm')
        self.assertEqual(r['source_id'], 'uscrn')

    def test_zone_not_covered_by_the_network_yields_nothing(self):
        self.assertIsNone(V.build_record(self.crop(), {'from': 'last_frost'}, '11',
                                         'Apr 20 - May 10', {}))

    def test_year_round_zone_is_not_soil_limited(self):
        r = V.build_record(self.crop(), {'from': 'last_frost'}, '10', 'Feb 1 - Mar 1',
                           {'50': zone_stats(median='01-01', p10='01-01', p90='01-26',
                                             year_round=True)})
        self.assertEqual(r['status'], 'not_soil_limited')
        self.assertIsNone(r['risk'],
                          'soil already above threshold when the year opens cannot be a risk')

    def test_insufficient_confidence_is_flagged_not_dropped(self):
        r = V.build_record(self.crop(), {'from': 'last_frost'}, '5', 'Apr 20 - May 10',
                           {'50': zone_stats(conf='insufficient', station_year_count=12)})
        self.assertEqual(r['status'], 'flagged_for_review')
        self.assertIn('12', r['zone_coverage_note'])

    def test_unreliable_zone_record_is_flagged(self):
        r = V.build_record(self.crop(), {'from': 'last_frost'}, '3', 'Jun 1 - Jun 20',
                           {'50': zone_stats(conf='unreliable')})
        self.assertEqual(r['status'], 'flagged_for_review')

    def test_fall_only_cell_yields_nothing(self):
        self.assertIsNone(V.build_record(self.crop(), {'from': 'first_frost'}, '5',
                                         'Sep 1 - Oct 1', {'50': zone_stats()}))

    def test_record_carries_no_em_dash(self):
        r = V.build_record(self.crop(), {'from': 'last_frost'}, '5', 'Apr 20 - May 10',
                           {'50': zone_stats(conf='insufficient')})
        for k, v in r.items():
            if isinstance(v, str):
                self.assertNotIn('—', v, 'consumer copy takes no em dashes (CLAUDE.md)')


if __name__ == '__main__':
    unittest.main(verbosity=2)
