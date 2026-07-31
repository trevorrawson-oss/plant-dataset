#!/usr/bin/env python3
"""Adversarial guard suite for tools/promote_artichoke_findings_key.py.

THE DEFECT. Artichoke is the ONLY crop of 128 that stores its findings at the TOP level as
`crop["open_findings"]`. 120 crops use `verification_status.open_findings`; the remaining 7 are
uncertified shells with neither. Every gate and scan reads the nested key -- `whole_crop_gate`
line 1062 is `vs.get("open_findings") or []` -- so artichoke's 12 findings are invisible and every
roster-wide finding count in this repo is short by one crop.

ORIGIN, found in source rather than guessed: `tools/promote_artichoke.py` line 340 writes
`crop["open_findings"] = copy.deepcopy(prose.OPEN_FINDINGS)`. The cert promote wrote the wrong
path. It was a bug, not a deliberate archetype choice -- asparagus, the other herbaceous perennial,
uses the nested key.

SCOPE IS RELOCATION ONLY, deliberately. Artichoke's entries also use `title` + `note_internal`
where the roster uses `summary`, but `summary` is read by NO gate and NO general scan (only by
one-off promote scripts pinned to a specific finding, one of which already tolerates alternate
keys). So the key-shape divergence is a separate, smaller question and is NOT bundled here:
one ruling per promote. The 12 entries must move byte-for-byte.

Fixture is REBUILT from the pinned base SHA via promote_fixture, never copied from live canonical.
"""
import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
from promote_artichoke_findings_key import BASE_SHA, EXPECTED_FINDINGS  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_artichoke_findings_key.py')


def run(path, sha, apply_=False):
    return subprocess.run(
        [sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
         '--canonical', path, '--expect-sha', sha],
        capture_output=True, text=True)


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


def artichoke(data):
    return next(c for c in data['crops'] if c['slug'] == 'artichoke')


class TestCleanRun(unittest.TestCase):
    def test_dry_run_passes_on_the_true_pre_state(self):
        path, sha = fixture()
        r = run(path, sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_apply_relocates_all_twelve_findings(self):
        path, sha = fixture()
        self.assertEqual(run(path, sha, apply_=True).returncode, 0)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        art = artichoke(after)
        self.assertNotIn('open_findings', art, 'top-level key survived')
        self.assertEqual(len(art['verification_status']['open_findings']), EXPECTED_FINDINGS)

    def test_findings_move_BYTE_FOR_BYTE(self):
        """Relocation, not rewriting. A pass that 'tidies' the text on the way is a
        different ruling and must not ride along."""
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        self.assertEqual(
            artichoke(before)['open_findings'],
            artichoke(after)['verification_status']['open_findings'])

    def test_roster_now_has_121_crops_with_nested_findings(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        n_before = sum(1 for c in before['crops']
                       if 'open_findings' in (c.get('verification_status') or {}))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        n_after = sum(1 for c in after['crops']
                      if 'open_findings' in (c.get('verification_status') or {}))
        self.assertEqual(n_before, 120)
        self.assertEqual(n_after, 121)

    def test_no_crop_but_artichoke_moves(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        b = {c['slug']: c for c in before['crops']}
        a = {c['slug']: c for c in after['crops']}
        moved = sorted(s for s in b if b[s] != a[s])
        self.assertEqual(moved, ['artichoke'])
        for k in before:
            if k != 'crops':
                self.assertEqual(before[k], after[k], f'top-level {k} moved')

    def test_artichokes_other_keys_and_verification_status_survive(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        b, a = artichoke(before), artichoke(after)
        self.assertEqual(set(b) - {'open_findings'}, set(a))
        for k in set(a) - {'verification_status'}:
            self.assertEqual(b[k], a[k], f'artichoke.{k} moved')
        bvs, avs = b['verification_status'], a['verification_status']
        self.assertEqual(set(bvs) | {'open_findings'}, set(avs))
        for k in bvs:
            self.assertEqual(bvs[k], avs[k], f'verification_status.{k} moved')

    def test_compact_serialization_preserved(self):
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
        r = run(path, 'f' * 64)
        self.assertEqual(r.returncode, 2)
        self.assertIn('drifted', r.stdout)

    def test_aborts_if_the_nested_key_already_exists(self):
        """Never silently merge or clobber an existing findings list.

        Mutation-testing note: adding the nested key to artichoke ALSO pushes the
        nested-crop count 120 -> 121, so a naive version of this test aborts at the count
        preflight and passes even with the refusal deleted. To make the refusal itself
        load-bearing, drop another crop's nested key so the count stays 120 and the
        refusal is the only check standing.
        """
        def mutate(crops, _d):
            crops['artichoke']['verification_status']['open_findings'] = [{'id': 'x'}]
            del crops['basil']['verification_status']['open_findings']
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn('ALREADY has', r.stdout)

    def test_aborts_if_the_top_level_key_is_missing(self):
        def mutate(crops, _d):
            del crops['artichoke']['open_findings']
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)

    def test_aborts_if_the_finding_count_is_not_twelve(self):
        def mutate(crops, _d):
            crops['artichoke']['open_findings'].pop()
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)

    def test_aborts_if_a_second_crop_carries_a_top_level_findings_key(self):
        """The premise is that artichoke is unique. If it stops being unique, the
        footprint assertion is wrong and the pass must stop rather than fix one of two."""
        def mutate(crops, _d):
            crops['asparagus']['open_findings'] = [{'id': 'y'}]
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)

    def test_guard_catches_text_edited_during_the_move(self):
        """Sabotage the PASS: if relocation ever starts rewriting a finding, abort."""
        import promote_artichoke_findings_key as promote
        real = promote.relocate

        def sabotaged(data):
            out = real(data)
            art = next(c for c in out['crops'] if c['slug'] == 'artichoke')
            art['verification_status']['open_findings'][0]['title'] = 'tidied'
            return out

        path, sha = fixture()
        argv = sys.argv
        promote.relocate = sabotaged
        try:
            sys.argv = ['p', '--dry-run', '--canonical', path, '--expect-sha', sha]
            rc = promote.main()
        finally:
            promote.relocate = real
            sys.argv = argv
        self.assertEqual(rc, 2, 'a text edit during relocation was not caught')


class TestFixtureIsReal(unittest.TestCase):
    def test_fixture_hashes_to_the_pinned_base(self):
        _p, sha = fixture()
        self.assertEqual(sha, BASE_SHA)

    def test_unknown_sha_raises_rather_than_skipping(self):
        with self.assertRaises(AssertionError):
            promote_fixture.pre_state('0' * 64)


if __name__ == '__main__':
    unittest.main()
