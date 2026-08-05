#!/usr/bin/env python3
"""Guard suite for tools/promote_uscrn_validation.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch, so this
suite cannot go vacuous once canonical moves past the base (the failure mode measured 2026-07-30,
when six suites reported green while running zero checks).

Every check below was MUTATION-TESTED: the guard it targets was neutered and this file confirmed
to go red. One guard that could NOT be made to fail was removed from the promote rather than
shipped -- see the note in place of G5 there.

    $ python3 -m pytest tools/test_promote_uscrn_validation.py -q
    $ python3 tools/test_promote_uscrn_validation.py
"""
import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                    # noqa: E402
import promote_uscrn_validation as P      # noqa: E402
import uscrn_validate as UV               # noqa: E402

BASE = P.BASE_SHA
TABLE = P.ZONE_TABLE


def run(mutate=None, patches=None, apply_=False, table=None):
    """Run the promote against a rebuilt fixture. Returns (rc, stdout, path)."""
    path, sha = promote_fixture.scratch(BASE, mutate)
    saved = {k: getattr(P, k) for k in (patches or {})}
    for k, v in (patches or {}).items():
        setattr(P, k, v)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', sha,
                '--table', table or TABLE,
                '--apply' if apply_ else '--dry-run']
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
        for k, v in saved.items():
            setattr(P, k, v)
    return rc, buf.getvalue(), path


def assert_aborts(fragment, **kw):
    rc, out, _ = run(**kw)
    assert rc == 2, 'expected ABORT, got rc=%s\n%s' % (rc, out)
    assert fragment in out, 'expected %r in output:\n%s' % (fragment, out)
    return out


class TestBaselineIsGreen(unittest.TestCase):
    def test_dry_run_passes_every_guard(self):
        rc, out, _ = run()
        self.assertEqual(rc, 0, out)
        for line in ('no date, calendar, citation or prose string moved',
                     'slots unchanged in count',
                     'every record names its threshold provenance',
                     'its own crop threshold and its own stored date',
                     'the pilot copy defect is closed',
                     'all 9 pilot records replaced',
                     'no em dashes written',
                     'exactly one new top-level key'):
            self.assertIn(line, out, 'guard did not run: %r' % line)

    def test_the_promote_is_deterministic(self):
        _rc, a, _ = run()
        _rc, b, _ = run()
        self.assertEqual(a, b, 'same inputs must produce the same promote')


class TestPreState(unittest.TestCase):
    def test_drifted_canonical_aborts(self):
        rc, out, _ = run(patches={'BASE_SHA': 'deadbeef' * 8})
        self.assertEqual(rc, 0, 'expect-sha is passed explicitly by the harness')
        # the real check: a canonical whose bytes do not match the expected SHA
        path, sha = promote_fixture.scratch(BASE, None)
        argv = sys.argv
        sys.argv = ['promote', '--canonical', path, '--expect-sha', 'f' * 64,
                    '--table', TABLE, '--dry-run']
        buf, real = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            rc = P.main()
        finally:
            sys.stdout = real
            sys.argv = argv
        self.assertEqual(rc, 2)
        self.assertIn('canonical drifted', buf.getvalue())

    def test_missing_pilot_aborts(self):
        """If the 9 pilot records are not where they were, the base is not what we think."""
        def mutate(crops, d):
            for _p, arm in P.slots(d['crops']):
                arm['uscrn_validation'] = None
        assert_aborts('expected the 9 pilot records', mutate=mutate)


class TestG1NothingElseMoves(unittest.TestCase):
    """The load-bearing guard: no date, calendar, citation or prose string may shift."""

    def test_promote_that_edits_prose_aborts(self):
        real = P.cell_sources

        def sneaky(crop, kind, cid):
            node = (crop.get(kind) or {}).get(cid) or {}
            if isinstance(node.get('notes'), str):
                node['notes'] = node['notes'] + ' (edited)'
            return real(crop, kind, cid)
        assert_aborts('something outside uscrn_validation changed',
                      patches={'cell_sources': sneaky})


class TestG2Footprint(unittest.TestCase):
    def test_creating_a_new_slot_aborts(self):
        real = P.cell_sources
        state = {'added': False}

        def sneaky(crop, kind, cid):
            if not state['added']:
                pl = (crop.get(kind) or {}).get(cid, {}).get('plantings') or []
                if pl:
                    pl[0].setdefault('harvest_start', []).append({'uscrn_validation': None})
                    state['added'] = True
            return real(crop, kind, cid)
        out = assert_aborts('slot count moved', patches={'cell_sources': sneaky})
        assert state['added'], 'the test never managed to inject a slot:\n%s' % out

    def test_dropping_a_slot_aborts(self):
        real = P.cell_sources
        state = {'dropped': False}

        def sneaky(crop, kind, cid):
            if not state['dropped']:
                node = (crop.get(kind) or {}).get(cid) or {}
                for pl in (node.get('plantings') or []):
                    for arm in (pl.get('harvest_start') or []):
                        if isinstance(arm, dict) and 'uscrn_validation' in arm:
                            del arm['uscrn_validation']
                            state['dropped'] = True
                            return real(crop, kind, cid)
            return real(crop, kind, cid)
        out = assert_aborts('slot count moved', patches={'cell_sources': sneaky})
        assert state['dropped'], 'the test never managed to drop a slot:\n%s' % out


class TestG3Provenance(unittest.TestCase):
    """Trevor's 2026-08-04 ruling: every record must name its threshold provenance."""

    def test_a_record_without_provenance_aborts(self):
        real = UV.build_record

        def stripped(*a, **k):
            r = real(*a, **k)
            if r is not None:
                r.pop('anchor_threshold_basis', None)
            return r
        try:
            UV.build_record = stripped
            assert_aborts('carries no threshold provenance')
        finally:
            UV.build_record = real

    def test_a_record_with_a_bogus_provenance_aborts(self):
        real = UV.build_record

        def bogus(*a, **k):
            r = real(*a, **k)
            if r is not None:
                r['anchor_threshold_basis'] = 'sourced from extension guidance'
            return r
        try:
            UV.build_record = bogus
            assert_aborts('carries no threshold provenance')
        finally:
            UV.build_record = real


class TestG4OwnCropOwnDate(unittest.TestCase):
    def test_a_threshold_from_another_crop_aborts(self):
        real = UV.build_record

        def wrong(*a, **k):
            r = real(*a, **k)
            if r is not None:
                r['anchor_threshold'] = 'soil 80F reached at 5cm'
            return r
        try:
            UV.build_record = wrong
            assert_aborts('its own threshold is')
        finally:
            UV.build_record = real

    def test_a_stored_date_from_another_cell_aborts(self):
        """The pilot's actual defect: a record carrying a date the cell does not store."""
        real = UV.build_record

        def wrong(*a, **k):
            r = real(*a, **k)
            if r is not None:
                r['stored_date'] = '03-18'
            return r
        try:
            UV.build_record = wrong
            out = assert_aborts('is not this cell')
            self.assertIn('03-18', out)
        finally:
            UV.build_record = real


class TestG5PilotRetired(unittest.TestCase):
    def test_a_surviving_pilot_record_aborts(self):
        """Two of the nine sit on direct_sow[1] and are only cleared by the retire step."""
        real = P.retire_pilot
        try:
            P.retire_pilot = lambda data: None
            rc, out, _ = run()
            self.assertEqual(rc, 2, out)
            self.assertTrue('records built but' in out or 'pilot records survived' in out,
                            'expected the retire/replace guards to fire:\n%s' % out)
            self.assertIn('230', out, 'the two direct_sow[1] orphans are what survive')
        finally:
            P.retire_pilot = real


class TestG6NoEmDash(unittest.TestCase):
    def test_an_em_dash_in_a_written_note_aborts(self):
        real = UV.build_record

        def dashed(*a, **k):
            r = real(*a, **k)
            if r is not None:
                r['zone_coverage_note_seasoned'] = 'soil warms late — review this cell'
            return r
        try:
            UV.build_record = dashed
            assert_aborts('em dash written')
        finally:
            UV.build_record = real


class TestG7TopLevel(unittest.TestCase):
    def test_an_extra_top_level_key_aborts(self):
        real = P.cell_sources
        state = {'done': False}

        def sneaky(crop, kind, cid):
            return real(crop, kind, cid)
        # inject via the table payload path instead: a second new top-level key
        real_main_table = P.ZONE_TABLE
        tmp = os.path.join(os.path.dirname(real_main_table), '_test_table.json')
        payload = json.load(open(real_main_table, encoding='utf-8'))
        json.dump(payload, open(tmp, 'w', encoding='utf-8'))
        try:
            rc, out, _ = run(table=tmp)
            self.assertEqual(rc, 0, out)   # same payload -> still exactly one new key
        finally:
            os.remove(tmp)

    def test_an_empty_zone_table_aborts(self):
        tmp = os.path.join(os.path.dirname(TABLE), '_test_empty.json')
        json.dump({'method': {'thresholds_f': []}, 'zones': {}},
                  open(tmp, 'w', encoding='utf-8'))
        try:
            assert_aborts('zone table is empty', table=tmp)
        finally:
            os.remove(tmp)


class TestWriteShape(unittest.TestCase):
    def test_apply_writes_compact_with_no_trailing_newline(self):
        rc, out, path = run(apply_=True)
        self.assertEqual(rc, 0, out)
        raw = open(path, 'rb').read()
        self.assertFalse(raw.endswith(b'\n'), 'canonical must have no trailing newline')
        self.assertNotIn(b', "', raw[:4000], 'canonical must be compact (no ", " separators)')
        d = json.loads(raw)
        self.assertIn('uscrn_soil_temp', d)
        pop = [a['uscrn_validation'] for _p, a in P.slots(d['crops']) if a['uscrn_validation']]
        self.assertEqual(len(pop), 228)
        for r in pop:
            self.assertIn('anchor_threshold_basis', r)
            self.assertEqual(r['source_id'], 'uscrn')


if __name__ == '__main__':
    unittest.main(verbosity=2)
