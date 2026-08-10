#!/usr/bin/env python3
"""Adversarial guard suite for tools/promote_asparagus_null_fields.py.

THE DEFECT. Asparagus lacks 7 of the 56 top-level fields carried by >=90% of the roster, and
it is the SOLE crop missing each (every one is present on the other 127). Kickoff 48 records
this as "a perennial-schema question, not an omission to backfill" -- the data does not support
that: artichoke, the only other herbaceous_perennial, carries all 56.

THIS PROMOTE HANDLES THE FIVE WHOSE ARCHETYPE-APPROPRIATE VALUE IS `null`, measured:
  days_to_maturity_mid        36 of the 37 crops with days_to_maturity == [] carry null,
                              and ZERO carry a value. Asparagus is the 37th.
  weeks_indoors               asparagus propagule == "crown" -- no indoor start exists, and
                              the only other crown crop carries null.
  first_planting_notify_days  52 crops null, artichoke among them.
  last_reviewed               22 null, artichoke among them.
  last_reviewed_session       22 null, artichoke among them.

`null` here is the HONEST value, not a shape being filled: writing a date into `last_reviewed`
would assert a top-level review that never happened -- the lettuce-leaf `verified` lesson.

NOT IN SCOPE, deliberately: `yield_expectations` (present AND non-null on all 127 others, so a
null would be a lie -- it needs real sourced authoring) and `zones` (a genuine schema question,
and plant-astro reads zones{} and fails open). Separate rulings, separate promotes.
"""
import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
from promote_asparagus_null_fields import BASE_SHA, NULL_FIELDS, OUT_OF_SCOPE  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_asparagus_null_fields.py')


def run(path, sha, apply_=False):
    return subprocess.run(
        [sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
         '--canonical', path, '--expect-sha', sha],
        capture_output=True, text=True)


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


def asparagus(data):
    return next(c for c in data['crops'] if c['slug'] == 'asparagus')


class TestCleanRun(unittest.TestCase):
    def test_dry_run_passes(self):
        path, sha = fixture()
        r = run(path, sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_apply_adds_exactly_the_five_keys_as_null(self):
        path, sha = fixture()
        self.assertEqual(run(path, sha, apply_=True).returncode, 0)
        with open(path, encoding='utf-8') as fh:
            asp = asparagus(json.load(fh))
        for f in NULL_FIELDS:
            self.assertIn(f, asp)
            self.assertIsNone(asp[f], f'{f} must be null, got {asp[f]!r}')

    def test_the_out_of_scope_fields_are_NOT_added(self):
        """yield_expectations must not be nulled -- it is non-null on all 127 other crops,
        so a null would assert 'no yield data exists' when the truth is 'nobody wrote it'."""
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            asp = asparagus(json.load(fh))
        for f in OUT_OF_SCOPE:
            self.assertNotIn(f, asp, f'{f} was added but is a separate ruling')

    def test_no_existing_asparagus_value_is_touched(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        b, a = asparagus(before), asparagus(after)
        self.assertEqual(set(b) | set(NULL_FIELDS), set(a))
        for k in b:
            self.assertEqual(b[k], a[k], f'asparagus.{k} moved')

    def test_no_other_crop_moves(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        b = {c['slug']: c for c in before['crops']}
        a = {c['slug']: c for c in after['crops']}
        # key-set first: iterating b alone cannot see a crop APPENDED by the promote (PLA-162)
        self.assertEqual(set(b), set(a), 'a crop appeared or vanished')
        self.assertEqual(sorted(s for s in b if b[s] != a[s]), ['asparagus'])
        self.assertEqual(set(before), set(after), 'a top-level key appeared or vanished')
        for k in before:
            if k != 'crops':
                self.assertEqual(before[k], after[k])

    def test_compact_preserved(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, 'rb') as fh:
            raw = fh.read()
        self.assertFalse(raw.endswith(b'\n'))
        self.assertEqual(raw, json.dumps(json.loads(raw), ensure_ascii=False,
                                         separators=(',', ':')).encode('utf-8'))


class TestGuards(unittest.TestCase):
    def test_aborts_on_sha_drift(self):
        path, _sha = fixture()
        self.assertEqual(run(path, 'f' * 64).returncode, 2)

    def test_aborts_if_a_target_field_already_exists(self):
        """If someone backfilled one by hand, the measured footprint no longer holds."""
        def mutate(crops, _d):
            crops['asparagus']['weeks_indoors'] = None
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)

    def test_aborts_if_asparagus_gains_a_days_to_maturity(self):
        """days_to_maturity_mid: null is only correct while DTM is empty. If DTM is ever
        populated, a null mid is wrong and this pass must stop rather than write it."""
        def mutate(crops, _d):
            crops['asparagus']['days_to_maturity'] = [60, 90]
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn('days_to_maturity', r.stdout)

    def test_aborts_if_asparagus_stops_being_crown_propagated(self):
        """weeks_indoors: null rests on there being no indoor start."""
        def mutate(crops, _d):
            crops['asparagus']['propagule'] = 'seed'
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn('propagule', r.stdout)

    def test_guard_catches_a_non_null_value_written_during_apply(self):
        """Sabotage the PASS: these fields must be null, never a plausible-looking value."""
        import promote_asparagus_null_fields as promote
        real = promote.backfill

        def sabotaged(data):
            out = real(data)
            asparagus(out)['last_reviewed'] = '2026-07-31'
            return out

        path, sha = fixture()
        argv = sys.argv
        promote.backfill = sabotaged
        try:
            sys.argv = ['p', '--dry-run', '--canonical', path, '--expect-sha', sha]
            rc = promote.main()
        finally:
            promote.backfill = real
            sys.argv = argv
        self.assertEqual(rc, 2, 'a non-null backfill was not caught')


class TestFixtureIsReal(unittest.TestCase):
    def test_fixture_hashes_to_the_pinned_base(self):
        _p, sha = fixture()
        self.assertEqual(sha, BASE_SHA)


if __name__ == '__main__':
    unittest.main()
