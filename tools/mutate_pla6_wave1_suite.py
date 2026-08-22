#!/usr/bin/env python3
"""Mutation harness for tools/test_promote_pla6_wave1.py -- PLA-215 bar, liveness-defended.

The wave 1 suite is replay-pinned and green from birth, so this is its only non-vacuity evidence.
Each mutation names the SPECIFIC guard that must redden; a mutation caught only by the post-SHA
guard is a FAILURE, not a catch, because any payload edit moves that hash and would otherwise let
the harness report 100% while proving nothing.

WAVE 1'S OWN FAMILY is TEMPLATE-PASTE: eight biologically similar crops authored in one pass is
exactly where a paragraph gets pasted with the crop name swapped, and that is the defect a
similarity metric scores as substantively different while a reader sees one text. It caught a real
0.837 peach/nectarine collision during drafting, so it is mutated here deliberately.
"""
import copy
import io
import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_pla6_wave1 as P  # noqa: E402
import test_promote_pla6_wave1 as S  # noqa: E402

SHA_GUARD = 'test_post_serializes_to_the_pinned_post_sha'


def run_suite():
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromModule(S))
    return {c._testMethodName for c, _ in list(result.failures) + list(result.errors)}


def m_template_paste():
    """TEMPLATE-PASTE: nectarine becomes peach with the name swapped. THE defect of this wave,
    and the one the drafting check actually caught at 0.837."""
    before = P.TRIO['nectarine']['full_harvest_notes_beginner']
    P.TRIO['nectarine']['full_harvest_notes_beginner'] = (
        P.TRIO['peach']['full_harvest_notes_beginner'].replace('peach', 'nectarine'))
    return before, P.TRIO['nectarine']['full_harvest_notes_beginner']


def m_cherry_told_to_thin():
    """BEARING HABIT: a cherry is given a peach's thinning instruction. Real harm -- a grower
    strips fruit that would have sized on its own, and cherries do not re-set."""
    before = P.TRIO['cherry-sweet']['first_harvest_notes_beginner']
    P.TRIO['cherry-sweet']['first_harvest_notes_beginner'] = (
        'Thin the young cherries to one every 6 to 8 inches about a month after bloom.')
    return before, P.TRIO['cherry-sweet']['first_harvest_notes_beginner']


def m_spur_crop_pruned_like_peach():
    """BEARING HABIT: the spur-bearing advice is lost from a spur bearer, which is how a grower
    prunes away the wood that carries the crop."""
    before = P.TRIO['apricot']['first_harvest_notes_seasoned']
    P.TRIO['apricot']['first_harvest_notes_seasoned'] = (
        'Expect a light first set. Renewal-prune hard every dormant season to replace fruiting '
        'wood, as for peach.')
    return before, P.TRIO['apricot']['first_harvest_notes_seasoned']


def m_thinning_distance_drift():
    """QUANTITY (v1.3 sec9.2): the prose distance drifts off the crop's OWN fruit_set tip."""
    before = P.TRIO['plum']['first_harvest_notes_beginner']
    P.TRIO['plum']['first_harvest_notes_beginner'] = before.replace('4 to 6', '8 to 10')
    return before, P.TRIO['plum']['first_harvest_notes_beginner']


def m_wrong_full_harvest_year():
    """QUANTITY: the full-harvest year stops matching years_to_first_harvest[1]."""
    before = P.TRIO['pear-european']['full_harvest_notes_beginner']
    P.TRIO['pear-european']['full_harvest_notes_beginner'] = before.replace('sixth', 'fourth')
    return before, P.TRIO['pear-european']['full_harvest_notes_beginner']


def m_pears_stop_inverting():
    """BEARING HABIT: the European pear is told to ripen on the tree, which produces the exact
    browned, gritty fruit its own record warns about."""
    before = P.TRIO['pear-european']['full_harvest_notes_beginner']
    P.TRIO['pear-european']['full_harvest_notes_beginner'] = (
        'From about the sixth year the tree carries a full crop. Pick each pear tree-ripe when '
        'it tastes sweet, and thin to one fruit per cluster each spring.')
    return before, P.TRIO['pear-european']['full_harvest_notes_beginner']


def m_cosmetic_pair():
    """DIFFERENTIATION (v1.3 sec9.1): the seasoned half becomes a thesaurus pass."""
    before = P.TRIO['plum']['full_harvest_notes_seasoned']
    P.TRIO['plum']['full_harvest_notes_seasoned'] = (
        P.TRIO['plum']['full_harvest_notes_beginner'].replace('plum', 'fruit'))
    return before, P.TRIO['plum']['full_harvest_notes_seasoned']


def m_em_dash():
    """MECHANICS (v1.1): an em-dash enters consumer prose. THE SENTINEL -- trivially checkable,
    so a failure to redden means the harness is not gating the mutated tables at all."""
    before = P.TRIO['peach']['first_harvest_notes_beginner']
    P.TRIO['peach']['first_harvest_notes_beginner'] = before.replace(
        'and the crop will be light.', 'and the crop will be light \u2014', 1)
    return before, P.TRIO['peach']['first_harvest_notes_beginner']


def m_blast_radius():
    """BLAST RADIUS: the wave reaches a crop nobody authorised."""
    before = copy.deepcopy(P.TRIO)
    P.TRIO['blueberry'] = {f: 'Unauthorised.' for f in P.NEW_FIELDS}
    return before, P.TRIO


MUTATIONS = [
    ('Mechanics', 'test_no_em_dash_en_dash_or_double_hyphen', m_em_dash, True),
    ('TemplatePaste', 'test_no_two_crops_share_a_near_identical_field', m_template_paste, False),
    ('BearingHabit/cherry', 'test_the_cherries_are_told_NOT_to_thin_and_are_given_no_spacing',
     m_cherry_told_to_thin, False),
    ('BearingHabit/spur', 'test_spur_bearers_say_prune_LIGHTER_in_BOTH_registers', m_spur_crop_pruned_like_peach, False),
    ('BearingHabit/pears', 'test_the_two_pears_invert_each_other_in_EVERY_field', m_pears_stop_inverting, False),
    ('Quantity/spacing', 'test_thinning_distance_matches_the_crops_own_fruit_set_tip',
     m_thinning_distance_drift, False),
    ('Quantity/year', 'test_full_harvest_year_equals_years_to_first_harvest_high',
     m_wrong_full_harvest_year, False),
    ('Differentiation', 'test_no_pair_is_a_near_verbatim_copy', m_cosmetic_pair, False),
    ('BlastRadius', 'test_only_the_expected_fields_differ', m_blast_radius, False),
]


def main():
    saved = copy.deepcopy(P.TRIO)
    baseline = run_suite()
    print('POSITIVE CONTROL  clean suite failures: %d' % len(baseline))
    if baseline:
        print('HARNESS DEAD: suite not green before mutation: %s' % sorted(baseline))
        return 2

    sentinel_ok = False
    bad = []
    for family, target, mutator, is_sentinel in MUTATIONS:
        before, after = mutator()
        if before == after:
            print('HARNESS DEAD: mutation %s did not land' % family)
            return 2
        failed = run_suite()
        P.TRIO.clear(); P.TRIO.update(copy.deepcopy(saved))
        if target in failed:
            verdict = 'CAUGHT'
            if is_sentinel:
                sentinel_ok = True
        elif failed <= {SHA_GUARD}:
            verdict = 'SHA-ONLY'
        elif failed:
            verdict = 'WRONG-GUARD'
        else:
            verdict = 'SURVIVED'
        if verdict != 'CAUGHT':
            bad.append((family, target, verdict, sorted(failed - {SHA_GUARD})))
        print('  %-12s %-22s%s' % (verdict, family, ' [SENTINEL]' if is_sentinel else ''))

    after_restore = run_suite()
    print('\nRESTORE-AND-REVERIFY failures: %d' % len(after_restore))
    if after_restore:
        print('HARNESS DEAD: a mutator did not undo itself: %s' % sorted(after_restore))
        return 2
    if not sentinel_ok:
        print('\nHARNESS DEAD: the sentinel did not redden. Every verdict above is void.')
        return 2

    print('\nMUTATIONS: %d  CAUGHT: %d  NOT CAUGHT: %d' % (len(MUTATIONS), len(MUTATIONS) - len(bad), len(bad)))
    print('sentinel: REDDENED   positive control: GREEN   restore: GREEN')
    for f, t, v, other in bad:
        print('  %s: %s (target %s, fired instead: %s)' % (v, f, t, other))
    print('\nRESULT:', 'PASS -- every guard family is live' if not bad else 'FAIL')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
