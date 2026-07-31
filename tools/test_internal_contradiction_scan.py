"""Adversarial tests for tools/internal_contradiction_scan.py.

This scan finds cells that contradict OTHER DATA WE ALREADY HOLD -- no network, no document
hunt. It exists because the blueberry defect was authored while the numbers refuting it were
already in the file: mid_south z7 banks 1000-1300 chill hours, our own variety table says
rabbiteye needs 350-600 and northern highbush 800-1000, and our own northern_tier already
used northern highbush at z7. Nothing external was required to notice.

EVERY prototype of these checks produced a count that was mostly artifact. So the tests below
are weighted toward the false-positive machinery, and each one pins a bug that was actually
made:

  * "15.5-0-0" (calcium nitrate) parsed as the ratio 5-0-0, inventing 7 defects
  * a SIDE-DRESS product ratio (27-3-3) read as the crop's primary NPK ratio
  * leafy greens legitimately fed 21-0-0 flagged as "says low nitrogen"
  * over-delivered chill scored the same as under-delivered, putting a VERIFIED-CORRECT cell
    (mid_atlantic rabbiteye, which NC State explicitly recommends) at the top of the list

The scan reports CONTESTED cells, never verdicts. A human adjudicates.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import internal_contradiction_scan as S  # noqa: E402


# ---------------------------------------------------------------- NPK parsing

def test_decimal_ratio_is_not_chopped_into_a_fake_ratio():
    """15.5-0-0 is calcium nitrate. It must not yield 5-0-0."""
    assert S.parse_ratios('calcium nitrate (15.5-0-0) as a side-dress') == []


def test_plain_ratio_parses():
    assert S.parse_ratios('a balanced 5-10-10 at planting') == [(5, 10, 10)]


def test_two_digit_ratio_parses():
    assert S.parse_ratios('use 21-0-0 once') == [(21, 0, 0)]


def test_ratio_inside_a_longer_number_run_is_rejected():
    assert S.parse_ratios('lot 2020-10-10-10 batch') == []


# ------------------------------------------------------- NPK claim vs. ratio

def test_the_real_tomato_defect_is_caught():
    """npk_hint says the THIRD number should be highest, then gives 8-32-16."""
    f = {'npk_ratio': '5-10-10',
         'npk_hint_beginner': 'you want the third number to be the highest: '
                              'something like 5-10-10 or 8-32-16 works well.'}
    hits = S.npk_contradictions('cherry-tomato', f)
    assert hits, 'the 8-32-16 example contradicts "third number highest"'
    assert any('8-32-16' in h['detail'] for h in hits)


def test_leafy_green_fed_high_nitrogen_is_not_a_defect():
    """arugula: 21-0-0 with 'nitrogen-rich' prose AGREES. Must stay silent."""
    f = {'npk_ratio': '21-0-0',
         'npk_hint_beginner': 'Use a nitrogen-rich feed such as blood meal or a 21-0-0 '
                              'fertilizer once, when the plants are a couple of weeks old.',
         'npk_hint_seasoned': 'High N for fast leafy growth; do not overfeed a 3-to-4-week crop.'}
    assert S.npk_contradictions('arugula', f) == []


def test_side_dress_ratio_is_not_treated_as_the_primary_ratio():
    """collards: primary is 10-10-10; 27-3-3 is a nitrogen side-dress and is correct."""
    f = {'npk_ratio': '10-10-10',
         'example_product': '10-10-10 at planting, then calcium nitrate, blood meal, or '
                            '27-3-3 to side-dress',
         'npk_hint_seasoned': 'A balanced feed such as 10-10-10 at planting, then nitrogen '
                              'side-dressings 3 to 4 weeks later.'}
    assert S.npk_contradictions('collards', f) == []


def test_pepper_primary_ratio_is_used_not_the_calcium_nitrate_side_dress():
    f = {'npk_ratio': '5-10-10',
         'example_product': '5-10-10 at planting, then calcium nitrate (15.5-0-0) as a side-dress',
         'npk_hint_seasoned': 'Avoid heavy nitrogen, which gives leaf at the expense of fruit.'}
    assert S.npk_contradictions('bell-pepper', f) == []


def test_a_genuine_high_nitrogen_claim_against_a_low_nitrogen_ratio_is_caught():
    f = {'npk_ratio': '5-10-10',
         'npk_hint_seasoned': 'This crop wants high nitrogen all season.'}
    hits = S.npk_contradictions('made-up', f)
    assert hits and 'nitrogen' in hits[0]['detail'].lower()


# ------------------------------------------------------------- chill matching

def test_under_delivered_chill_is_the_serious_direction():
    r = S.chill_verdict(delivered=(150, 600), required=(700, 800))
    assert r == 'UNDER'


def test_over_delivered_chill_is_advisory_not_a_defect():
    """mid_atlantic rabbiteye: 1100-1500 delivered, 350-600 needed, and NC State is right."""
    r = S.chill_verdict(delivered=(1100, 1500), required=(350, 600))
    assert r == 'OVER', 'excess chill is not a failure; it must not rank as one'


def test_matched_chill_is_silent():
    assert S.chill_verdict(delivered=(800, 1000), required=(800, 1000)) is None


def test_under_and_over_are_never_collapsed_into_one_score():
    assert S.chill_verdict((150, 600), (700, 800)) != S.chill_verdict((1100, 1500), (350, 600))


# ------------------------------------------------------ cross-region contrast

def test_month_overlap_detects_a_true_outlier():
    assert S.months('Dec - Feb') & S.months('Jan')
    assert not (S.months('Dec - Feb') & S.months('Jun - Jul'))


def test_month_wraparound_is_handled():
    m = S.months('Nov - Feb')
    assert {10, 11, 0, 1} <= m and 5 not in m


def test_unparseable_window_is_none_not_empty():
    assert S.months('whenever soil can be worked') is None


# ------------------------------------------------- template prose inheritance

def test_near_identical_prose_with_a_swapped_institution_is_flagged():
    a = ('NC State Extension steers zone 8 growers toward sour cherry instead, because the '
         'humid summers here favour it over sweet cherry in the Piedmont.')
    b = ('University of Arkansas Cooperative Extension steers zone 8 growers toward sour cherry '
         'instead, because the humid summers here favour it over sweet cherry in the Piedmont.')
    assert S.institution_swap(a, b) is not None


def test_same_institution_repeated_is_not_a_swap():
    a = 'NC State Extension recommends planting in late winter for this belt and region.'
    assert S.institution_swap(a, a) is None


def test_different_prose_is_not_a_swap():
    a = 'NC State Extension recommends planting in late winter for this belt and region.'
    b = 'University of Arkansas suggests a completely different management approach entirely.'
    assert S.institution_swap(a, b) is None
