#!/usr/bin/env python3
"""Mutation harness for tools/test_promote_pla6_wave2.py -- PLA-215 bar, liveness-defended.

The wave 2 suite is replay-pinned and green from birth, so this is its only non-vacuity evidence.
Each mutation names the SPECIFIC guard that must redden; a mutation caught only by the post-SHA
guard is a FAILURE, not a catch, because any payload edit moves that hash and would otherwise let
the harness report 100% while proving nothing.

WAVE 2'S OWN FAMILY is TEMPLATE-PASTE: eight biologically similar crops authored in one pass is
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

import promote_pla6_wave2 as P  # noqa: E402
import test_promote_pla6_wave2 as S  # noqa: E402

SHA_GUARD = 'test_post_serializes_to_the_pinned_post_sha'


def run_suite():
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromModule(S))
    return {c._testMethodName for c, _ in list(result.failures) + list(result.errors)}


def m_template_paste():
    """TEMPLATE-PASTE: lime's year-one note becomes lemon's with the name swapped. THE risk of
    this wave -- all five citrus share graft-union depth, foot rot, psyllid scouting and
    little-and-often feeding, so year_one_notes is where a template is easiest to reach for and
    hardest to see."""
    before = P.TRIO['lime']['year_one_notes_beginner']
    P.TRIO['lime']['year_one_notes_beginner'] = (
        P.TRIO['lemon']['year_one_notes_beginner'].replace('lemon', 'lime'))
    return before, P.TRIO['lime']['year_one_notes_beginner']


def m_lime_picked_yellow():
    """CITRUS FACTS: lime loses its pick-green rule. Its own record calls picking yellow the
    most common lime-harvest mistake, and the rule is the exact inverse of lemon's, so a crop
    that quietly inherits the lemon rule sends the grower to overripe, low-acid fruit."""
    before = P.TRIO['lime']['full_harvest_notes_beginner']
    P.TRIO['lime']['full_harvest_notes_beginner'] = (
        'From about the third year the tree carries a real crop. Pick each lime once it has '
        'turned a full even yellow and feels heavy for its size.')
    return before, P.TRIO['lime']['full_harvest_notes_beginner']


def m_lime_told_to_store_on_tree():
    """CITRUS FACTS: lime is given the lemon storage advice. Lime is chilling-sensitive and
    short-lived off the tree; telling a grower to leave it hanging or refrigerate it properly
    cold spoils the crop."""
    before = P.TRIO['lime']['full_harvest_notes_seasoned']
    P.TRIO['lime']['full_harvest_notes_seasoned'] = (
        'Full production from roughly year three. The tree is your storage: fruit holds on the '
        'branch for months, so pick against demand.')
    return before, P.TRIO['lime']['full_harvest_notes_seasoned']


def m_mandarin_told_it_holds():
    """CITRUS FACTS: mandarin is told it holds on the tree like a navel. Most cultivars puff and
    desiccate on the branch, so this loses the crop to waiting."""
    before = P.TRIO['mandarin-clementine']['full_harvest_notes_beginner']
    P.TRIO['mandarin-clementine']['full_harvest_notes_beginner'] = (
        'From about the third year the tree carries a real crop. Leave ripe fruit on the tree '
        'and pick over a long window; it stores itself outdoors.')
    return before, P.TRIO['mandarin-clementine']['full_harvest_notes_beginner']


def m_graft_union_drift():
    """QUANTITY (v1.3 sec9.2): the same physical instruction drifts between crops. Five crops
    stating one depth is exactly where a number quietly diverges."""
    before = P.TRIO['grapefruit']['year_one_notes_beginner']
    P.TRIO['grapefruit']['year_one_notes_beginner'] = before.replace(
        'two to three inches', 'an inch or so')
    return before, P.TRIO['grapefruit']['year_one_notes_beginner']


def m_gloss_removed():
    """GLOSS (v1.3 sec9.3): "graft union" is used bare in a beginner half. A first-season grower
    meets the term on a nursery tag, so leaving it unexplained in the field where it appears is
    the defect the standard names."""
    before = P.TRIO['lemon']['year_one_notes_beginner']
    P.TRIO['lemon']['year_one_notes_beginner'] = before.replace(
        'the graft union, the knobby joint low on the trunk where your lemon variety was joined '
        'to its roots,', 'the graft union')
    return before, P.TRIO['lemon']['year_one_notes_beginner']


def m_wrong_full_harvest_year():
    """QUANTITY: the full-harvest year stops matching years_to_first_harvest[1]."""
    before = P.TRIO['orange-navel']['full_harvest_notes_beginner']
    P.TRIO['orange-navel']['full_harvest_notes_beginner'] = before.replace('fourth', 'second')
    return before, P.TRIO['orange-navel']['full_harvest_notes_beginner']


def m_cosmetic_pair():
    """DIFFERENTIATION (v1.3 sec9.1): the seasoned half becomes a thesaurus pass."""
    before = P.TRIO['grapefruit']['full_harvest_notes_seasoned']
    P.TRIO['grapefruit']['full_harvest_notes_seasoned'] = (
        P.TRIO['grapefruit']['full_harvest_notes_beginner'].replace('grapefruit', 'the fruit'))
    return before, P.TRIO['grapefruit']['full_harvest_notes_seasoned']


def m_em_dash():
    """MECHANICS (v1.1). THE SENTINEL: trivially checkable, so a failure to redden means the
    harness is not gating the mutated tables at all."""
    before = P.TRIO['lemon']['first_harvest_notes_beginner']
    P.TRIO['lemon']['first_harvest_notes_beginner'] = before.replace(
        'treat this as a taste rather than a crop.', 'treat this as a taste — not a crop.', 1)
    return before, P.TRIO['lemon']['first_harvest_notes_beginner']


def m_blast_radius():
    """BLAST RADIUS: the wave reaches a crop nobody authorised."""
    before = copy.deepcopy(P.TRIO)
    P.TRIO['blueberry'] = {f: 'Unauthorised.' for f in P.NEW_FIELDS}
    return before, P.TRIO


MUTATIONS = [
    ('Mechanics', 'test_no_em_dash_en_dash_or_double_hyphen', m_em_dash, True),
    ('TemplatePaste', 'test_no_two_crops_share_a_near_identical_field', m_template_paste, False),
    ('Citrus/lime-green', 'test_lime_is_picked_GREEN_in_BOTH_full_harvest_registers', m_lime_picked_yellow, False),
    ('Citrus/lime-store', 'test_lime_is_never_told_to_store_like_a_lemon',
     m_lime_told_to_store_on_tree, False),
    ('Citrus/mandarin', 'test_mandarin_does_NOT_hold_in_BOTH_full_harvest_registers', m_mandarin_told_it_holds, False),
    ('Quantity/union', 'test_graft_union_depth_agrees_across_every_crop_and_register',
     m_graft_union_drift, False),
    ('Gloss', 'test_the_graft_union_is_GLOSSED_in_every_beginner_half', m_gloss_removed, False),
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
