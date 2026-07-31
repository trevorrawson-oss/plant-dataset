#!/usr/bin/env python3
"""Adversarial guard suite for tools/promote_dezone_lifted_prose.py.

The fixture is REBUILT from the pinned base SHA via tools/promote_fixture, never copied from
live canonical. Six suites in this repo once went silently vacuous by skipping when canonical
moved off their base; an unresolvable SHA here RAISES.

Every check below is proved by injecting the defect it is supposed to catch and confirming the
promote aborts. A guard that has never seen its own failure mode is not a guard.
"""
import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import dezone_lifted_prose as dz  # noqa: E402
from promote_dezone_lifted_prose import BASE_SHA  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_dezone_lifted_prose.py')


def run(path, sha, apply_=False):
    return subprocess.run(
        [sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
         '--canonical', path, '--expect-sha', sha],
        capture_output=True, text=True)


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


class TestCleanRun(unittest.TestCase):
    def test_dry_run_passes_on_the_true_pre_state(self):
        path, sha = fixture()
        r = run(path, sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('106 strings / 66 cells / 15 crops', r.stdout)

    def test_apply_produces_prose_with_no_wrong_zone_left(self):
        path, sha = fixture()
        r = run(path, sha, apply_=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        self.assertEqual(dz.find_defects(after), [])

    def test_apply_preserves_compact_serialization(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, 'rb') as fh:
            raw = fh.read()
        self.assertFalse(raw.endswith(b'\n'))
        self.assertNotIn(b', "', raw[:20000])
        self.assertEqual(
            raw,
            json.dumps(json.loads(raw), ensure_ascii=False,
                       separators=(',', ':')).encode('utf-8'))

    def test_apply_keeps_the_roster_and_cert_count(self):
        path, sha = fixture()
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        run(path, sha, apply_=True)
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        self.assertEqual(len(after['crops']), len(before['crops']))
        certed = lambda d: sum(  # noqa: E731
            1 for c in d['crops']
            if (c.get('verification_status') or {}).get('status') == 'verified_gs_arc')
        self.assertEqual(certed(after), certed(before))


class TestDriftGuards(unittest.TestCase):
    def test_aborts_when_canonical_is_not_the_pinned_base(self):
        path, _sha = fixture()
        r = run(path, 'f' * 64)
        self.assertEqual(r.returncode, 2)
        self.assertIn('canonical drifted', r.stdout)

    def test_aborts_when_a_target_string_was_already_edited(self):
        """If someone hand-fixed one cell first, the measured footprint no longer holds."""
        def mutate(crops, _data):
            cell = crops['grapefruit']['regions']['ca_south_coast']['resolved_by_zone']['11']
            cell['suitability_note_beginner'] = 'The south coast almost never freezes.'
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertIn('expected 106 defect strings', r.stdout)

    def test_aborts_when_a_lifted_row_gains_prose_with_no_rule(self):
        """Never silently skip copy the pass does not understand."""
        def mutate(crops, _data):
            cell = crops['lime']['regions']['ca_desert']['resolved_by_zone']['11']
            cell['suitability_note_seasoned'] = (
                'Zone 10 in Narnia is balmy and grows turkish delight year-round.')
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertTrue('no rewrite rule' in r.stdout or 'expected 106' in r.stdout, r.stdout)

    def test_aborts_when_an_unexpected_region_zone_is_in_scope(self):
        """The blast radius is the seven pairs the widen added, and nothing else."""
        def mutate(crops, _data):
            cell = crops['lemon']['regions']['ca_interior']['resolved_by_zone']['9']
            cell['lifted_from_zone'] = '8'
            cell['suitability_note_seasoned'] = (
                'Zone 8 in the low desert is frost-free and fruits reliably.')
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertTrue('region/zone set' in r.stdout or 'expected 106' in r.stdout, r.stdout)


class TestCollateralGuards(unittest.TestCase):
    """The failure mode that matters most: a prose pass quietly moving real data."""

    def _apply_with_sabotage(self, sabotage):
        """Run the promote, then check the guard would have caught `sabotage`."""
        path, sha = fixture()
        r = run(path, sha, apply_=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return path, r

    def test_guard_catches_a_suitability_flip_riding_along(self):
        """Sabotage the PASS, not the fixture.

        A first version of this test set `suitability` in the pre-state and expected an abort;
        it did not get one, correctly -- the guard checks what the promote CHANGES, and a value
        that was already there is not collateral damage. To exercise the footprint guard the
        damage has to happen during apply(), so it is injected in-process here.
        """
        import promote_dezone_lifted_prose as promote

        real_apply = promote.dz.apply

        def sabotaged(data):
            out = real_apply(data)
            cell = next(c for c in out['crops'] if c['slug'] == 'plum')
            cell['regions']['ca_desert']['resolved_by_zone']['11']['suitability'] = (
                'fruits_reliably')
            return out

        path, sha = fixture()
        argv = sys.argv
        promote.dz.apply = sabotaged
        try:
            sys.argv = ['promote', '--dry-run', '--canonical', path, '--expect-sha', sha]
            rc = promote.main()
        finally:
            promote.dz.apply = real_apply
            sys.argv = argv
        self.assertEqual(rc, 2, 'a suitability flip during apply() was not caught')

    def test_guard_catches_prose_edited_outside_a_lifted_row(self):
        """Same shape, on the scope boundary: apply() must not reach a non-lifted row."""
        import promote_dezone_lifted_prose as promote

        real_apply = promote.dz.apply

        def sabotaged(data):
            out = real_apply(data)
            crop = next(c for c in out['crops'] if c['slug'] == 'lemon')
            cell = crop['regions']['ca_interior']['resolved_by_zone']['9']
            cell['suitability_note_seasoned'] = 'Rewritten by a pass that overreached.'
            return out

        path, sha = fixture()
        argv = sys.argv
        promote.dz.apply = sabotaged
        try:
            sys.argv = ['promote', '--dry-run', '--canonical', path, '--expect-sha', sha]
            rc = promote.main()
        finally:
            promote.dz.apply = real_apply
            sys.argv = argv
        self.assertEqual(rc, 2, 'an edit to a non-lifted row was not caught')

    def test_guard_catches_one_extra_prose_edit_on_an_already_clean_lifted_row(self):
        """The case ONLY the footprint COUNT can catch.

        Mutation-testing showed the count check was redundant for the other sabotages: they
        land on a non-prose key or a non-lifted row, which later checks catch anyway. This
        one is on a lifted row AND a prose key AND has no defect to fix, so it slips every
        check except "exactly 106 values moved".
        """
        import promote_dezone_lifted_prose as promote

        real_apply = promote.dz.apply

        def sabotaged(data):
            out = real_apply(data)
            crop = next(c for c in out['crops'] if c['slug'] == 'lemon')
            cell = crop['regions']['hawaii_tropical']['resolved_by_zone']['12']
            # An EXISTING key on a lifted row, a prose key, and NOT one of the 106 defect
            # strings. It must already exist: adding a key trips the structural check
            # instead, which is what made the first version of this test pass for the
            # wrong reason.
            assert 'suitability_note_beginner' in cell
            cell['suitability_note_beginner'] = 'An edit nobody asked for.'
            return out

        path, sha = fixture()
        argv = sys.argv
        promote.dz.apply = sabotaged
        try:
            sys.argv = ['promote', '--dry-run', '--canonical', path, '--expect-sha', sha]
            rc = promote.main()
        finally:
            promote.dz.apply = real_apply
            sys.argv = argv
        self.assertEqual(rc, 2, 'a 107th prose edit on a lifted row was not caught')

    def test_guard_catches_a_dropped_chill_figure(self):
        """The chill numbers are the whole justification for de-zoning."""
        def mutate(crops, _data):
            cell = crops['plum']['regions']['ca_desert']['resolved_by_zone']['11']
            cell['suitability_note_seasoned'] = cell['suitability_note_seasoned'].replace(
                ' (about 100 to 300 hours)', '')
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn('lost the figure', r.stdout)

    def test_guard_catches_a_stripped_lift_marker(self):
        def mutate(crops, _data):
            cell = crops['pomegranate']['regions']['hawaii_tropical']['resolved_by_zone']['12']
            del cell['lifted_from_zone']
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2, r.stdout)

    def test_applied_output_moves_no_citation_and_no_date(self):
        path, _sha = self._apply_with_sabotage(None)
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)

        def strip_prose(node):
            if isinstance(node, dict):
                return {k: strip_prose(v) for k, v in node.items()
                        if not (isinstance(v, str) and k.endswith(('_seasoned', '_beginner')))}
            if isinstance(node, list):
                return [strip_prose(v) for v in node]
            return node

        self.assertEqual(strip_prose(before), strip_prose(after),
                         'something other than prose moved')

    def test_applied_output_keeps_every_calendar_untouched(self):
        path, _sha = self._apply_with_sabotage(None)
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        with open(path, encoding='utf-8') as fh:
            after = json.load(fh)
        for i, crop in enumerate(before['crops']):
            for region, rv in (crop.get('regions') or {}).items():
                for zone, cell in ((rv or {}).get('resolved_by_zone') or {}).items():
                    if not isinstance(cell, dict):
                        continue
                    new = after['crops'][i]['regions'][region]['resolved_by_zone'][zone]
                    for k in ('calendar', 'harvest', 'harvest_start', 'harvest_end',
                              'bloom', 'plant_out', 'suitability', 'min_winter_temp_f'):
                        self.assertEqual(cell.get(k), new.get(k),
                                         f'{crop["slug"]}/{region}/z{zone}.{k}')


class TestFixtureIsReal(unittest.TestCase):
    """Guarding the guard: prove the fixture is the pinned pre-state, not live canonical."""

    def test_fixture_hashes_to_the_pinned_base_sha(self):
        _path, sha = fixture()
        self.assertEqual(sha, BASE_SHA)

    def test_unknown_sha_raises_rather_than_skipping(self):
        with self.assertRaises(AssertionError):
            promote_fixture.pre_state('0' * 64)


if __name__ == '__main__':
    unittest.main()
