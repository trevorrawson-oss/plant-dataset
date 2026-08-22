#!/usr/bin/env python3
"""Mutation harness for tools/test_promote_pla6_wave4.py -- PLA-215 bar, liveness-defended.

The wave 4 suite is replay-pinned and green from birth, so this is its only non-vacuity evidence.
Each mutation names the SPECIFIC guard that must redden; a mutation caught only by the post-SHA
guard is a FAILURE, not a catch, because any payload edit moves that hash and would otherwise let
the harness report 100% while proving nothing.

WAVE 4'S OWN FAMILY is TEMPLATE-PASTE: eight biologically similar crops authored in one pass is
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

import promote_pla6_wave4 as P  # noqa: E402
import test_promote_pla6_wave4 as S  # noqa: E402

SHA_GUARD = 'test_post_serializes_to_the_pinned_post_sha'


def run_suite():
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromModule(S))
    return {c._testMethodName for c, _ in list(result.failures) + list(result.errors)}


def m_template_paste():
    """TEMPLATE-PASTE: mulberry's first_harvest_seasoned becomes fig's. Isolated deliberately on
    a field carrying no fact-guard token, so only the paste family can fire."""
    before = P.TRIO['mulberry']['first_harvest_notes_seasoned']
    P.TRIO['mulberry']['first_harvest_notes_seasoned'] = (
        P.TRIO['fig']['first_harvest_notes_seasoned'].replace('Fig', 'Mulberry').replace('fig', 'mulberry'))
    return before, P.TRIO['mulberry']['first_harvest_notes_seasoned']


def m_bract_gloss_removed():
    """GLOSS (v1.3 sec9.3): artichoke's `bract` goes bare in a beginner half. THE DEFECT THAT
    OPENED THIS ARC -- Trevor's 2026-08-05 report was an unexplained technical term in artichoke's
    mature-bed copy, so this is the one mutation that maps directly onto the original complaint."""
    before = P.TRIO['artichoke']['full_harvest_notes_beginner']
    P.TRIO['artichoke']['full_harvest_notes_beginner'] = before.replace(
        'its bracts, the tough overlapping scales, are', 'its bracts are')
    return before, P.TRIO['artichoke']['full_harvest_notes_beginner']


def m_artichoke_indexed_on_size():
    """FACT: artichoke is indexed on size rather than closure, which is the harvest error UC is
    explicit about -- a mature bud neither enlarges further nor re-tightens."""
    before = P.TRIO['artichoke']['full_harvest_notes_seasoned']
    P.TRIO['artichoke']['full_harvest_notes_seasoned'] = (
        'Full production from roughly year two on a persisting planting. Cut each bud once it '
        'has reached full size for its position on the stalk.')
    return before, P.TRIO['artichoke']['full_harvest_notes_seasoned']


def m_cutback_reduced_to_tidying():
    """FACT: the annual cut-back loses its scheduling function and becomes housekeeping, which
    is the mature-bed content no truncation could ever have carried."""
    before = P.TRIO['artichoke']['full_harvest_notes_beginner']
    P.TRIO['artichoke']['full_harvest_notes_beginner'] = before.replace(
        'Cut back between mid-April and mid-June and the plant crops in fall, winter and spring; '
        'cut back in late August or September and you get a summer harvest instead.',
        'Cut the plant back each year to tidy it up.')
    return before, P.TRIO['artichoke']['full_harvest_notes_beginner']


def m_fig_told_color_is_ripeness():
    """FACT: fig loses the color-is-not-ripeness warning, sending a grower after hard fruit that
    will never finish, since fig is non-climacteric."""
    before = P.TRIO['fig']['first_harvest_notes_beginner']
    P.TRIO['fig']['first_harvest_notes_beginner'] = (
        'Fig is one of the quickest perennials to pay you back, often giving a little fruit in '
        'its first or second year. Pick each fig once it has colored up fully.')
    return before, P.TRIO['fig']['first_harvest_notes_beginner']


def m_fig_told_to_prune_hard():
    """FACT: fig is told to renewal-prune, which forfeits the breba crop it carries on last
    year's wood."""
    before = P.TRIO['fig']['full_harvest_notes_seasoned']
    P.TRIO['fig']['full_harvest_notes_seasoned'] = before.replace(
        'Dormant pruning stays light and late', 'Renewal pruning is essential each dormant season')
    return before, P.TRIO['fig']['full_harvest_notes_seasoned']


def m_mulberry_told_to_thin():
    """FACT: mulberry is told to thin fruit, which is work for nothing on a crop that sizes
    without it and ripens sequentially over weeks."""
    before = P.TRIO['mulberry']['first_harvest_notes_beginner']
    P.TRIO['mulberry']['first_harvest_notes_beginner'] = before.replace(
        'Do not thin them;', 'Thin the young berries to one every few inches;')
    return before, P.TRIO['mulberry']['first_harvest_notes_beginner']


def m_persimmon_type_scoping_lost():
    """FACT: persimmon loses its type scoping. Eating an astringent Hachiya firm is the
    memorable way to get this crop wrong, so collapsing the two types is real harm."""
    before = P.TRIO['persimmon']['full_harvest_notes_beginner']
    P.TRIO['persimmon']['full_harvest_notes_beginner'] = (
        'From about the fifth year the tree carries a full crop. Pick each persimmon once it '
        'turns fully deep orange and eat it crisp, clipping it free with its leafy cap on.')
    return before, P.TRIO['persimmon']['full_harvest_notes_beginner']


def m_pomegranate_splitting_dropped():
    """FACT: pomegranate loses splitting, its defining failure, from a field."""
    before = P.TRIO['pomegranate']['first_harvest_notes_beginner']
    P.TRIO['pomegranate']['first_harvest_notes_beginner'] = (
        'Your first pomegranates usually arrive in the second year. Keep the soil evenly moist '
        'from fruit set until you pick, and watch for leaf-footed bug from fruit set onward.')
    return before, P.TRIO['pomegranate']['first_harvest_notes_beginner']


def m_wrong_full_harvest_year():
    """QUANTITY: the full-harvest year stops matching years_to_first_harvest[1]."""
    before = P.TRIO['persimmon']['full_harvest_notes_beginner']
    P.TRIO['persimmon']['full_harvest_notes_beginner'] = before.replace('fifth', 'second')
    return before, P.TRIO['persimmon']['full_harvest_notes_beginner']


def m_near_verbatim_copy():
    """COPY DETECTOR (see the guard's own docstring for what it does and does not reach): the
    seasoned half is pasted from the beginner half with one phrase changed."""
    before = P.TRIO['pomegranate']['full_harvest_notes_seasoned']
    P.TRIO['pomegranate']['full_harvest_notes_seasoned'] = (
        P.TRIO['pomegranate']['full_harvest_notes_beginner'].replace('with clippers', 'with secateurs'))
    return before, P.TRIO['pomegranate']['full_harvest_notes_seasoned']


def m_british_spelling():
    """MECHANICS (v1.1): a British spelling enters consumer copy."""
    before = P.TRIO['mulberry']['full_harvest_notes_beginner']
    P.TRIO['mulberry']['full_harvest_notes_beginner'] = before.replace('color', 'colour')
    return before, P.TRIO['mulberry']['full_harvest_notes_beginner']


def m_em_dash():
    """MECHANICS (v1.1). THE SENTINEL."""
    before = P.TRIO['fig']['full_harvest_notes_beginner']
    P.TRIO['fig']['full_harvest_notes_beginner'] = before.replace(
        'So pick every day or two.', 'So pick every day — or two.', 1)
    return before, P.TRIO['fig']['full_harvest_notes_beginner']


def m_blast_radius():
    """BLAST RADIUS: the wave reaches a crop nobody authorised."""
    before = copy.deepcopy(P.TRIO)
    P.TRIO['blueberry'] = {f: 'Unauthorised.' for f in P.NEW_FIELDS}
    return before, P.TRIO


MUTATIONS = [
    ('Mechanics/em-dash', 'test_no_em_dash_en_dash_or_double_hyphen', m_em_dash, True),
    ('Mechanics/British', 'test_american_english', m_british_spelling, False),
    ('TemplatePaste', 'test_no_two_crops_share_a_near_identical_field', m_template_paste, False),
    ('GLOSS/bract', 'test_artichokes_BRACT_TERM_is_glossed_in_every_beginner_half',
     m_bract_gloss_removed, False),
    ('Artichoke/tightness', 'test_artichoke_indexes_on_TIGHTNESS_not_size_in_every_field',
     m_artichoke_indexed_on_size, False),
    ('Artichoke/cutback', 'test_artichokes_cutback_is_framed_as_SCHEDULING',
     m_cutback_reduced_to_tidying, False),
    ('Fig/color', 'test_fig_says_color_is_NOT_ripeness', m_fig_told_color_is_ripeness, False),
    ('Fig/pruning', 'test_fig_is_never_told_to_prune_hard', m_fig_told_to_prune_hard, False),
    ('Mulberry/thin', 'test_mulberry_is_told_NOT_to_thin_and_given_no_spacing', m_mulberry_told_to_thin, False),
    ('Persimmon/type', 'test_persimmon_scopes_harvest_by_TYPE_in_every_field',
     m_persimmon_type_scoping_lost, False),
    ('Pomegranate/split', 'test_pomegranate_names_SPLITTING_and_its_cause_in_every_field',
     m_pomegranate_splitting_dropped, False),
    ('Quantity/year', 'test_full_harvest_year_equals_years_to_first_harvest_high',
     m_wrong_full_harvest_year, False),
    ('CopyDetector', 'test_no_pair_is_a_near_verbatim_copy', m_near_verbatim_copy, False),
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
