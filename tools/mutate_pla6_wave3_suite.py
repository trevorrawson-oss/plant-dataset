#!/usr/bin/env python3
"""Mutation harness for tools/test_promote_pla6_wave3.py -- PLA-215 bar, liveness-defended.

The wave 3 suite is replay-pinned and green from birth, so this is its only non-vacuity evidence.
Each mutation names the SPECIFIC guard that must redden; a mutation caught only by the post-SHA
guard is a FAILURE, not a catch, because any payload edit moves that hash and would otherwise let
the harness report 100% while proving nothing.

WAVE 3'S OWN FAMILY is TEMPLATE-PASTE: eight biologically similar crops authored in one pass is
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

import promote_pla6_wave3 as P  # noqa: E402
import test_promote_pla6_wave3 as S  # noqa: E402

SHA_GUARD = 'test_post_serializes_to_the_pinned_post_sha'


def run_suite():
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestLoader().loadTestsFromModule(S))
    return {c._testMethodName for c, _ in list(result.failures) + list(result.errors)}


def m_template_paste():
    """TEMPLATE-PASTE: blackberry becomes raspberry with the name swapped. These two share cane
    biology almost exactly and diverge on the one thing a picker acts on, so this is the paste
    that would be easiest to make and hardest to notice.
    ISOLATED ON PURPOSE. The first version pasted raspberry's full_harvest_beginner into
    blackberry, which also stripped the receptacle cue and fired the harvest-cue guard first --
    caught, but by the wrong family, which proves nothing about TEMPLATE-PASTE. This pastes the
    first_harvest SEASONED half instead, which carries no cue token, so only the paste guard can
    fire."""
    before = P.TRIO['blackberry']['first_harvest_notes_seasoned']
    P.TRIO['blackberry']['first_harvest_notes_seasoned'] = (
        P.TRIO['raspberry']['first_harvest_notes_seasoned'].replace('raspberr', 'blackberr'))
    return before, P.TRIO['blackberry']['first_harvest_notes_seasoned']


def m_cooking_rule_dropped():
    """SAFETY: elderberry's cooking rule is dropped from ONE field. This is the mutation that
    matters most in the wave. Raw and unripe fruit, foliage and stems are mildly toxic, and a
    reader lands on ONE pill rather than reading all four, so a rule surviving in three fields
    is a rule missing for anyone who opens the fourth."""
    before = P.TRIO['elderberry']['full_harvest_notes_beginner']
    P.TRIO['elderberry']['full_harvest_notes_beginner'] = (
        'From the third year the shrub carries a full crop. Cut out stems older than about '
        'three years each late winter. Harvest whole clusters when most berries are deep '
        'purple-black and soft.')
    return before, P.TRIO['elderberry']['full_harvest_notes_beginner']


def m_harvest_cues_swapped():
    """BERRY FACTS: blackberry inherits raspberry's slips-off-the-core cue. The receptacle
    behaviour is opposite between the two, so this sends a picker after fruit that will never
    behave the way the text promises."""
    before = P.TRIO['blackberry']['full_harvest_notes_beginner']
    P.TRIO['blackberry']['full_harvest_notes_beginner'] = before.replace(
        'pulls free with its core still inside', 'slips off its core leaving a hollow centre')
    return before, P.TRIO['blackberry']['full_harvest_notes_beginner']


def m_renovation_unscoped():
    """BERRY FACTS: strawberry loses the type scoping on renovation. Renovating a day-neutral
    bed mows off fruit the plant is still carrying, so the exemption is the load-bearing half."""
    before = P.TRIO['strawberry']['full_harvest_notes_beginner']
    P.TRIO['strawberry']['full_harvest_notes_beginner'] = (
        'From the second year the bed gives its full crop. A week or two after the last '
        'berries, renovate: mow the old leaves to about 2 inches above the crowns, rake them '
        'away, narrow the row, then feed and water.')
    return before, P.TRIO['strawberry']['full_harvest_notes_beginner']


def m_cane_gloss_removed():
    """GLOSS (v1.3 sec9.3): `cane` is left bare in a beginner half. This arc measured 151 bare
    uses of the term in beginner copy across the perennials, 133 of them on these two crops, so
    it is the single largest gloss gap the arc owns."""
    before = P.TRIO['raspberry']['first_harvest_notes_beginner']
    P.TRIO['raspberry']['first_harvest_notes_beginner'] = before.replace(
        'each cane, meaning each individual stem coming out of the ground, lives only two',
        'each cane lives only two')
    return before, P.TRIO['raspberry']['first_harvest_notes_beginner']


def m_blueberry_as_cane_crop():
    """BERRY FACTS: blueberry loses its defining nutritional failure. Interveinal chlorosis from
    high-pH iron lock-out is the top cause of a blueberry that grows but never crops."""
    before = P.TRIO['blueberry']['first_harvest_notes_seasoned']
    P.TRIO['blueberry']['first_harvest_notes_seasoned'] = (
        'Continue bud removal through year two so the planting builds root and shoot mass '
        'before it carries fruit, and feed lightly at bud break.')
    return before, P.TRIO['blueberry']['first_harvest_notes_seasoned']


def m_wrong_full_harvest_year():
    """QUANTITY: the full-harvest year stops matching years_to_first_harvest[1]."""
    before = P.TRIO['blueberry']['full_harvest_notes_beginner']
    P.TRIO['blueberry']['full_harvest_notes_beginner'] = before.replace('third', 'second')
    return before, P.TRIO['blueberry']['full_harvest_notes_beginner']


def m_cosmetic_pair():
    """DIFFERENTIATION (v1.3 sec9.1): the seasoned half becomes a thesaurus pass over the
    beginner half.

    THIS INJECTS A PASTE, NOT A THESAURUS PASS, because a paste is what the guard can actually
    catch. Chasing this mutation is what exposed the guard's real reach: a first version swapped
    a word everywhere and scored 0.375, a three-word swap scored 0.986, and a true thesaurus pass
    over every word scores 0.333 -- BELOW honest prose. The metric is inverted against the sec9.1
    defect, so the guard was renamed to what it does (refuse a near-verbatim copy) and the sec9.1
    defect proper is left to reading, per v1.2 sec11."""
    before = P.TRIO['raspberry']['full_harvest_notes_seasoned']
    P.TRIO['raspberry']['full_harvest_notes_seasoned'] = (
        P.TRIO['raspberry']['full_harvest_notes_beginner']
        .replace('shallow container', 'shallow tray'))
    return before, P.TRIO['raspberry']['full_harvest_notes_seasoned']


def m_british_spelling():
    """MECHANICS (v1.1): a British spelling enters consumer copy. Included deliberately because
    six reached this wave's draft and the guard had only ever listed five words; it now carries
    eighteen, and the widened version was itself verified live rather than assumed."""
    before = P.TRIO['blueberry']['full_harvest_notes_beginner']
    P.TRIO['blueberry']['full_harvest_notes_beginner'] = before.replace('color', 'colour')
    return before, P.TRIO['blueberry']['full_harvest_notes_beginner']


def m_em_dash():
    """MECHANICS (v1.1). THE SENTINEL: trivially checkable, so a failure to redden means the
    harness is not gating the mutated tables at all."""
    before = P.TRIO['strawberry']['first_harvest_notes_beginner']
    P.TRIO['strawberry']['first_harvest_notes_beginner'] = before.replace(
        'which kind you planted.', 'which kind you planted — it matters.', 1)
    return before, P.TRIO['strawberry']['first_harvest_notes_beginner']


def m_blast_radius():
    """BLAST RADIUS: the wave reaches a crop nobody authorised."""
    before = copy.deepcopy(P.TRIO)
    P.TRIO['fig'] = {f: 'Unauthorised.' for f in P.NEW_FIELDS}
    return before, P.TRIO


MUTATIONS = [
    ('Mechanics/em-dash', 'test_no_em_dash_en_dash_or_double_hyphen', m_em_dash, True),
    ('Mechanics/British', 'test_american_english', m_british_spelling, False),
    ('TemplatePaste', 'test_no_two_crops_share_a_near_identical_field', m_template_paste, False),
    ('SAFETY/cooking', 'test_elderberrys_COOKING_RULE_is_in_every_field',
     m_cooking_rule_dropped, False),
    ('Berry/harvest-cue', 'test_raspberry_and_blackberry_have_OPPOSITE_harvest_cues',
     m_harvest_cues_swapped, False),
    ('Berry/renovation', 'test_strawberry_scopes_renovation_to_JUNE_BEARING_only',
     m_renovation_unscoped, False),
    ('Berry/blueberry', 'test_blueberry_is_not_treated_as_a_cane_crop', m_blueberry_as_cane_crop, False),
    ('Gloss/cane', 'test_the_cane_term_is_GLOSSED_where_a_beginner_meets_it',
     m_cane_gloss_removed, False),
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
