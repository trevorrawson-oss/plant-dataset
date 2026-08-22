#!/usr/bin/env python3
"""Mutation harness for tools/test_promote_pla6_year_trio.py -- the PLA-215 bar, liveness-defended.

WHY THIS IS THE ONLY NON-VACUITY EVIDENCE. The suite is REPLAY-PINNED: `pre` is rebuilt from the
base SHA and `post` is the promote's own output, so every guard is green from birth and can never
be observed failing first. "Green" and "not wired up" look identical from outside. The only way to
tell them apart is to inject, per guard family, the defect that family claims to catch.

WHAT IS MUTATED. The promote's own payload tables (`TRIO`, `EDITS`) and, for the two families that
read the dataset rather than the payload, the reconstructed base. The suite reads both, so a
mutation reaches it the same way a bad authoring decision would.

THE DISCRIMINATION PROBLEM, and how it is handled. `Fixture.test_post_serializes_to_the_pinned_
post_sha` reddens on EVERY mutation, because any payload change moves the output hash. A harness
that only asked "did the suite go red" would therefore report 100% caught while proving nothing
about the other families. So each mutation names the SPECIFIC test that must redden, and a
mutation caught only by the post-SHA guard is reported CAUGHT-BY-SHA-ONLY, which is a FAILURE.

THE LIVENESS DEFENCE (PLA-138's harness dedented an already-indented template, silently ran the
CLEAN fixture, and reported every mutation as surviving):

  1. MUTATION-APPLIED MARKER. Every mutator returns the value it wrote; the harness asserts it
     differs from the original before running the suite. A mutation that did not land is a
     harness fault, never a survivor.
  2. SENTINEL. One mutation targets a guard that is trivially checkable
     (`Mechanics.test_no_em_dash_en_dash_or_double_hyphen`). If the sentinel does not redden, the
     harness exits HARNESS DEAD and every other verdict is void.
  3. POSITIVE CONTROL. The unmutated suite must be fully green first. If the baseline is already
     red the mutations prove nothing, and the run aborts.
  4. RESTORE-AND-REVERIFY. After the last mutation the tables are restored and the suite is run
     again, which catches a mutator that failed to undo itself and left later verdicts meaningless.

Run: python3 tools/mutate_pla6_year_trio_suite.py
Exit 0 only when every family is caught by its OWN guard and every control holds.
"""
import copy
import io
import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, 'tools')
sys.path.insert(0, TOOLS)

import promote_pla6_year_trio as P  # noqa: E402
import test_promote_pla6_year_trio as S  # noqa: E402

SHA_GUARD = 'test_post_serializes_to_the_pinned_post_sha'


def run_suite():
    """Run the whole guard suite in-process. Returns the set of failed/errored test method names."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(S)
    buf = io.StringIO()
    result = unittest.TextTestRunner(stream=buf, verbosity=0).run(suite)
    bad = set()
    for case, _tb in list(result.failures) + list(result.errors):
        bad.add(case._testMethodName)
    return bad


# --------------------------------------------------------------------------- mutators
# Each returns (marker_before, marker_after) so the harness can prove the write landed.

def m_mechanics_em_dash():
    """MECHANICS: an em-dash enters authored consumer prose (v1.1 forbids it outright)."""
    before = P.TRIO['apple']['first_harvest_notes_beginner']
    P.TRIO['apple']['first_harvest_notes_beginner'] = before.replace('That is normal.', 'That is normal —', 1)
    return before, P.TRIO['apple']['first_harvest_notes_beginner']


def m_register_cosmetic():
    """DIFFERENTIATION (v1.3 sec9.1): the seasoned half becomes a thesaurus pass over the
    beginner half. This is the defect the standard exists to name, and a similarity metric alone
    would score it as substantively different."""
    before = P.TRIO['apple']['full_harvest_notes_seasoned']
    P.TRIO['apple']['full_harvest_notes_seasoned'] = (
        P.TRIO['apple']['full_harvest_notes_beginner']
        .replace('apple', 'fruit').replace('tree', 'specimen'))
    return before, P.TRIO['apple']['full_harvest_notes_seasoned']


def m_quantity_divergence():
    """QUANTITY (v1.3 sec9.2): the two registers give DIFFERENT figures for the same thing.
    This is the lemon 'hand's width' against 'a foot' class, on asparagus's year-2 ceiling --
    where getting it wrong costs the grower the bed."""
    before = P.TRIO['asparagus']['first_harvest_notes_seasoned']
    P.TRIO['asparagus']['first_harvest_notes_seasoned'] = before.replace('two weeks', 'four weeks')
    return before, P.TRIO['asparagus']['first_harvest_notes_seasoned']


def m_ramp_drift():
    """QUANTITY, second family: the prose ramp drifts off the crop's own harvest_ramp_weeks."""
    before = P.TRIO['asparagus']['full_harvest_notes_beginner']
    P.TRIO['asparagus']['full_harvest_notes_beginner'] = before.replace('six to ten', 'eight to twelve')
    return before, P.TRIO['asparagus']['full_harvest_notes_beginner']


def m_actionability_floor():
    """ACTIONABILITY (v1.2 sec9): the beginner half loses its instruction and keeps only the
    caution -- the f31/f32 defect, 'a beginner given a risk and denied the remedy'."""
    before = P.TRIO['asparagus']['first_harvest_notes_beginner']
    P.TRIO['asparagus']['first_harvest_notes_beginner'] = (
        'A young asparagus bed is fragile and easily set back for good.')
    return before, P.TRIO['asparagus']['first_harvest_notes_beginner']


def m_na_crop_populated():
    """TRIO SHAPE: an N/A crop is authored anyway. sage renders no pills, so prose here would
    land somewhere no reader can reach -- the year_one_notes_* failure this whole arc exists to
    end, reintroduced one crop at a time."""
    before = {k: v for k, v in P.TRIO.items()}
    P.TRIO['sage'] = {f: 'Take a light first cut in year two.' for f in P.NEW_FIELDS}
    return before, P.TRIO


def m_trio_field_nulled():
    """A29 COLLISION: a trio field ships null. A null _beginner/_seasoned field that EXISTS is
    exactly what A29 register-fill forbids, and it is what the contract originally specified
    before the gauntlet overruled it."""
    before = P.TRIO['apple']['full_harvest_notes_seasoned']
    P.TRIO['apple']['full_harvest_notes_seasoned'] = None
    return before, P.TRIO['apple']['full_harvest_notes_seasoned']


def m_pawpaw_distance_dropped():
    """ACTIONABILITY, Trevor's case: the pollinizer distance is dropped from the BEGINNER half,
    leaving the figure only where the more experienced reader sees it."""
    before = P.TRIO['pawpaw']['first_harvest_notes_beginner']
    P.TRIO['pawpaw']['first_harvest_notes_beginner'] = before.replace(
        'If your two trees are more than about 30 feet apart, that distance alone can be why a '
        'healthy, flowering pawpaw sets almost nothing.', '')
    return before, P.TRIO['pawpaw']['first_harvest_notes_beginner']


def m_edit_becomes_noop():
    """EDIT EFFECT: the rendered-field repair silently does nothing, which is the exact failure
    that let 'close together' ship in the first place."""
    key = ('pawpaw', 'pollinator_notes_beginner')
    before = P.EDITS[key]
    P.EDITS[key] = (before[0], before[0])
    return before, P.EDITS[key]


def m_blast_radius():
    """BLAST RADIUS: the promote reaches a crop and field nobody authorised."""
    before = copy.deepcopy(P.TRIO)
    P.TRIO['blueberry'] = {'first_harvest_notes_beginner': 'Unauthorised.'}
    return before, P.TRIO


MUTATIONS = [
    ('Mechanics', 'test_no_em_dash_en_dash_or_double_hyphen', m_mechanics_em_dash, True),
    ('Differentiation', 'test_no_pair_is_a_near_verbatim_copy', m_register_cosmetic, False),
    ('Quantity/ceiling', 'test_asparagus_year_two_ceiling_agrees', m_quantity_divergence, False),
    ('Quantity/ramp', 'test_asparagus_bed_age_ramp_agrees_across_registers_and_with_the_dataset',
     m_ramp_drift, False),
    ('Actionability', 'test_asparagus_year_two_ceiling_agrees', m_actionability_floor, False),
    ('TrioShape/NA', 'test_every_authored_crop_actually_renders_pills', m_na_crop_populated, False),
    ('TrioShape/null', 'test_no_trio_field_is_ever_null', m_trio_field_nulled, False),
    ('Actionability/distance', 'test_pawpaw_pollinizer_distance_is_in_BOTH_registers',
     m_pawpaw_distance_dropped, False),
    ('EditEffect', 'test_each_edit_removed_its_find_and_installed_its_replacement',
     m_edit_becomes_noop, False),
    ('BlastRadius', 'test_only_the_expected_crop_fields_differ', m_blast_radius, False),
]


def main():
    saved_trio = copy.deepcopy(P.TRIO)
    saved_edits = copy.deepcopy(P.EDITS)

    # ---- (3) POSITIVE CONTROL
    baseline = run_suite()
    print('POSITIVE CONTROL  clean suite failures: %d' % len(baseline))
    if baseline:
        print('HARNESS DEAD: the suite is not green before mutation: %s' % sorted(baseline))
        return 2

    sentinel_ok = False
    results = []
    for family, target, mutator, is_sentinel in MUTATIONS:
        before, after = mutator()
        # ---- (1) MUTATION-APPLIED MARKER
        if before == after:
            print('HARNESS DEAD: mutation %s did not change anything' % family)
            return 2
        failed = run_suite()
        P.TRIO.clear(); P.TRIO.update(copy.deepcopy(saved_trio))
        P.EDITS.clear(); P.EDITS.update(copy.deepcopy(saved_edits))

        if target in failed:
            verdict = 'CAUGHT'
            if is_sentinel:
                sentinel_ok = True
        elif failed == {SHA_GUARD} or failed <= {SHA_GUARD}:
            verdict = 'SHA-ONLY'
        elif failed:
            verdict = 'CAUGHT-BY-WRONG-GUARD'
        else:
            verdict = 'SURVIVED'
        results.append((family, target, verdict, sorted(failed - {SHA_GUARD})))
        mark = ' [SENTINEL]' if is_sentinel else ''
        print('  %-22s %-14s%s  target=%s' % (verdict, family, mark, target))
        if verdict in ('CAUGHT-BY-WRONG-GUARD', 'SHA-ONLY'):
            print('       other guards that fired: %s' % sorted(failed - {SHA_GUARD}))

    # ---- (4) RESTORE-AND-REVERIFY
    after_restore = run_suite()
    print('\nRESTORE-AND-REVERIFY  failures after restoring tables: %d' % len(after_restore))
    if after_restore:
        print('HARNESS DEAD: a mutator did not undo itself: %s' % sorted(after_restore))
        return 2

    # ---- (2) SENTINEL governs everything
    if not sentinel_ok:
        print('\nHARNESS DEAD: the sentinel mutation (an em-dash in consumer prose) did not redden '
              'its guard. Every verdict above is void.')
        return 2

    caught = [r for r in results if r[2] == 'CAUGHT']
    bad = [r for r in results if r[2] != 'CAUGHT']
    print('\nMUTATIONS: %d  CAUGHT: %d  NOT CAUGHT: %d' % (len(results), len(caught), len(bad)))
    print('sentinel: REDDENED   positive control: GREEN   restore: GREEN')
    for f, t, v, other in bad:
        print('  %s: %s (target %s, fired instead: %s)' % (v, f, t, other))
    print('\nRESULT:', 'PASS -- every guard family is live' if not bad else 'FAIL -- see above')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
