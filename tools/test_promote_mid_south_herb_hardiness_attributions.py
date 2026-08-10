#!/usr/bin/env python3
"""Adversarial guard suite for tools/promote_mid_south_herb_hardiness_attributions.py.

THE DEFECT. Five herb crops credit the University of Arkansas with a hardiness range -- and, on
lavender, a disease "plant profile" -- across 10 sentences in 7 mid_south cells, while citing
`uada_ext`, a bare domain root, as their sole source. The prose is the mid_atlantic prose with the
institution find-and-replaced; NC State's Plant Toolbox carries our numbers to the character.

UAEX publishes a hardiness range for exactly ONE of the five species (English lavender, "zones 5
to 8" -- and that is not the "5a to 9b" we credit it with). The fix is purely subtractive: delete
the credit, keep the fact.

EVERY SABOTAGE HERE PINS THE ABORT MESSAGE, not just the exit code. That is deliberate. Several of
these guards overlap in what they can detect -- the post-edit "zero attributions remain" sweep is
a superset of the preflight count, for instance -- so an exit-code-only assertion would stay green
with the guard under test DELETED, because a later check would catch the sabotage instead. That is
the vacuous-guard failure mode hit three times in two days. Pinning the message makes deleting any
single check observable.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_mid_south_herb_hardiness_attributions as promote  # noqa: E402
from promote_mid_south_herb_hardiness_attributions import (  # noqa: E402
    BASE_SHA, CROPS, EDITS, FINDINGS, UAEX_ATTR)

SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_south_herb_hardiness_attributions.py')


def run(path, sha, apply_=False):
    return subprocess.run(
        [sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
         '--canonical', path, '--expect-sha', sha],
        capture_output=True, text=True)


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


def in_process(path, sha, apply_=False, **patches):
    """Run main() in-process with module attributes patched. Returns (rc, stdout)."""
    import io
    saved = {k: getattr(promote, k) for k in patches}
    argv, stdout = sys.argv, sys.stdout
    buf = io.StringIO()
    try:
        for k, v in patches.items():
            setattr(promote, k, v)
        sys.argv = ['p', '--apply' if apply_ else '--dry-run',
                    '--canonical', path, '--expect-sha', sha]
        sys.stdout = buf
        rc = promote.main()
    finally:
        for k, v in saved.items():
            setattr(promote, k, v)
        sys.argv, sys.stdout = argv, stdout
    return rc, buf.getvalue()


def before_shim(doctor):
    """A `copy` stand-in that doctors ONLY the first deepcopy -- the `before` snapshot.

    Lets a test simulate a change the EDITS loop never made, which is the only way to reach the
    guards that compare before-vs-after outside the edited fields.
    """
    real = copy.deepcopy

    class Shim:
        def __init__(self):
            self.n = 0

        def deepcopy(self, x):
            out = real(x)
            self.n += 1
            if self.n == 1:
                doctor(out)
            return out

    return Shim()


def cell(data, slug, z):
    return next(c for c in data['crops']
                if c['slug'] == slug)['regions']['mid_south']['resolved_by_zone'][z]


def load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- clean run

class TestCleanRun(unittest.TestCase):
    def test_dry_run_passes(self):
        path, sha = fixture()
        r = run(path, sha)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_apply_removes_every_uaex_credit_from_the_five_crops(self):
        path, sha = fixture()
        self.assertEqual(run(path, sha, apply_=True).returncode, 0)
        data = load(path)
        for slug in CROPS:
            ms = next(c for c in data['crops'] if c['slug'] == slug)['regions']['mid_south']
            for z, c in (ms.get('resolved_by_zone') or {}).items():
                for k, v in c.items():
                    if isinstance(v, str):
                        self.assertIsNone(UAEX_ATTR.search(v),
                                          f'{slug} z{z} {k} still credits the University of Arkansas')

    def test_the_horticultural_facts_survive_verbatim(self):
        """The credit goes; the number stays. Deleting a correct fact is the failure mode
        the cherry-sweet precedent exists to prevent."""
        path, sha = fixture()
        run(path, sha, apply_=True)
        data = load(path)
        expect = {
            ('thyme', '7', 'synthesis_note_seasoned'): 'reliably hardy to about zone 5, so',
            ('rosemary', '7', 'grown_as_note_seasoned'): 'hardy floor is about zone 7, so',
            ('rosemary', '7', 'synthesis_note_seasoned'): 'hardy only to about zone 7 to 8, so',
            ('oregano', '7', 'synthesis_note_seasoned'): 'hardy to about zone 4, so',
            ('sage', '7', 'synthesis_note_seasoned'): 'hardy in roughly zones 4 to 8, so',
            ('sage', '8', 'synthesis_note_seasoned'): "sage's stated zone 4 to 8 ceiling, so",
            ('lavender', '7', 'synthesis_note_seasoned'): 'hardy to about zone 5, so',
            ('lavender', '8', 'synthesis_note_seasoned'):
                "English lavender's zone 5 to 9b hardy range.",
        }
        for (slug, z, field), frag in expect.items():
            self.assertIn(frag, cell(data, slug, z)[field], f'{slug} z{z} {field}')

    def test_the_two_lavender_disease_sentences_keep_both_diseases(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        data = load(path)
        syn = cell(data, 'lavender', '7')['synthesis_note_seasoned']
        grown = cell(data, 'lavender', '7')['grown_as_note_seasoned']
        self.assertIn("root rot from overwatering and leaf spot are this species' main threats", syn)
        self.assertIn('root rot from wet soil and leaf spot are the real threats.', grown)

    def test_nothing_but_the_ten_fields_and_two_findings_moves(self):
        before = json.loads(promote_fixture.pre_state(BASE_SHA))
        path, sha = fixture()
        run(path, sha, apply_=True)
        after = load(path)
        ba = {c['slug']: c for c in before['crops']}
        aa = {c['slug']: c for c in after['crops']}
        # key-set first: iterating ba alone cannot see a crop APPENDED by the promote (PLA-162)
        self.assertEqual(set(ba), set(aa), 'a crop appeared or vanished')
        self.assertEqual(sorted(s for s in ba if ba[s] != aa[s]), sorted(CROPS))
        self.assertEqual(set(before), set(after), 'a top-level key appeared or vanished')
        for k in before:
            if k != 'crops':
                self.assertEqual(before[k], after[k], f'top-level {k} moved')
        # inside the five, only the intended (zone, field) pairs and open_findings moved
        for slug in CROPS:
            b, a = copy.deepcopy(ba[slug]), copy.deepcopy(aa[slug])
            want = {(z, f) for s, z, f, _o, _n, _k in EDITS if s == slug}
            for z, f in want:
                b['regions']['mid_south']['resolved_by_zone'][z][f] = \
                    a['regions']['mid_south']['resolved_by_zone'][z][f]
            b.setdefault('verification_status', {})['open_findings'] = \
                a['verification_status']['open_findings']
            self.assertEqual(b, a, f'{slug} moved somewhere unintended')

    def test_both_surfaced_findings_are_filed_open(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        data = load(path)
        for slug, finding in FINDINGS:
            ofs = next(c for c in data['crops']
                       if c['slug'] == slug)['verification_status']['open_findings']
            hit = [f for f in ofs if f.get('id') == finding['id']]
            self.assertEqual(len(hit), 1, f'{finding["id"]} not filed exactly once')
            self.assertEqual(hit[0]['status'], 'open')
            self.assertFalse(hit[0]['blocks_launch'])

    def test_output_stays_compact_with_no_trailing_newline(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        with open(path, 'rb') as fh:
            out = fh.read()
        self.assertFalse(out.endswith(b'\n'))
        self.assertNotIn(b'\n', out)
        self.assertNotIn(b'", "', out, 'compact separators lost')

    def test_no_em_dash_reaches_consumer_copy(self):
        path, sha = fixture()
        run(path, sha, apply_=True)
        data = load(path)
        for slug, z, field, _o, _n, _k in EDITS:
            v = cell(data, slug, z)[field]
            self.assertNotIn(chr(8212), v)
            self.assertNotIn('--', v)
            self.assertNotIn('  ', v)


# --------------------------------------------------------------------------- sabotage

class TestGuards(unittest.TestCase):

    def test_sha_drift_aborts(self):
        path, _sha = fixture()
        r = run(path, 'f' * 64)
        self.assertEqual(r.returncode, 2)
        self.assertIn('canonical drifted', r.stdout)

    def test_preflight_rejects_a_defect_of_the_wrong_size(self):
        """An 11th attribution appearing anywhere in these cells means the evidence no longer
        describes the data. Pinned to the preflight message: the post-edit sweep would also
        catch this, so an exit-code assertion would survive deleting the preflight."""
        def mutate(crops, _data):
            c = crops['thyme']['regions']['mid_south']['resolved_by_zone']['8']
            c['grown_as_note_beginner'] += ' The University of Arkansas agrees.'
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertIn('not the shape the evidence describes', r.stdout)

    def test_preflight_rejects_a_cell_that_no_longer_cites_uada_ext(self):
        """If a repoint has landed, the premise -- 'the sole source is a bare host' -- is gone."""
        def mutate(crops, _data):
            crops['lavender']['regions']['mid_south']['resolved_by_zone']['7']['sources'] = \
                ['ncsu_ext_lavandula_angustifolia']
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertIn('no longer cites uada_ext', r.stdout)

    def test_reworded_prose_aborts_rather_than_silently_missing(self):
        def mutate(crops, _data):
            c = crops['sage']['regions']['mid_south']['resolved_by_zone']['7']
            c['synthesis_note_seasoned'] = c['synthesis_note_seasoned'].replace(
                'hardy in roughly zones 4 to 8 (the University of Arkansas)',
                'hardy in roughly zones 4 to 8 (per the University of Arkansas)')
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertIn('does not contain the expected text exactly once', r.stdout)

    def test_a_replacement_that_drops_the_zone_number_is_refused(self):
        """Removing the credit must not take the fact with it."""
        bad = [list(e) for e in EDITS]
        bad[0][4] = 'hardy, so'          # thyme: credit AND "zone 5" both gone
        path, sha = fixture()
        rc, out = in_process(path, sha, EDITS=[tuple(e) for e in bad])
        self.assertEqual(rc, 2)
        self.assertIn('lost the fact', out)

    def test_an_uncovered_attribution_is_caught_by_the_post_edit_sweep(self):
        """Drop lavender's z8 edit: its credit survives and the sweep must fail the run."""
        bad = [e for e in EDITS if not (e[0] == 'lavender' and e[1] == '8')]
        path, sha = fixture()
        rc, out = in_process(path, sha, EDITS=bad)
        self.assertEqual(rc, 2)
        self.assertIn('still credits the University of Arkansas', out)

    def test_repointing_the_credit_to_nc_state_is_refused(self):
        """The hunt-1 guard: never name a source the arm does not carry. mid_south herb cells
        cite uada_ext only, so swapping in NC State would be the same defect facing the other way."""
        bad = [list(e) for e in EDITS]
        bad[0][4] = 'hardy to about zone 5 (NC State: zones 5a to 9b), so'
        path, sha = fixture()
        rc, out = in_process(path, sha, EDITS=[tuple(e) for e in bad])
        self.assertEqual(rc, 2)
        self.assertIn('names an institution the arm does not carry', out)

    def test_an_em_dash_in_a_rewritten_string_is_refused(self):
        bad = [list(e) for e in EDITS]
        bad[0][4] = 'hardy to about zone 5 ' + chr(8212) + ' so'
        path, sha = fixture()
        rc, out = in_process(path, sha, EDITS=[tuple(e) for e in bad])
        self.assertEqual(rc, 2)
        self.assertIn('em dash', out)

    def test_a_doubled_space_left_by_the_removal_is_refused(self):
        bad = [list(e) for e in EDITS]
        bad[0][4] = 'hardy to about zone 5,  so'
        path, sha = fixture()
        rc, out = in_process(path, sha, EDITS=[tuple(e) for e in bad])
        self.assertEqual(rc, 2)
        self.assertIn('whitespace/punctuation artifact', out)

    def test_a_finding_already_filed_aborts(self):
        def mutate(crops, _data):
            ofs = crops['lavender']['verification_status']['open_findings']
            ofs.append({'id': FINDINGS[0][1]['id'], 'summary': 'x', 'status': 'open'})
        path, sha = fixture(mutate)
        r = run(path, sha)
        self.assertEqual(r.returncode, 2)
        self.assertIn('already filed', r.stdout)

    def test_touching_uaex_on_a_non_herb_crop_is_refused(self):
        """This hunt is herbs only. A UAEX mention appearing on any other crop must abort."""
        bad = list(FINDINGS) + [('apple', {
            'id': 'sabotage_apple', 'summary': 'the University of Arkansas says so',
            'severity': 'low', 'blocks_launch': False, 'filed_in_session': 'x', 'status': 'open'})]
        path, sha = fixture()
        rc, out = in_process(path, sha, FINDINGS=bad)
        self.assertEqual(rc, 2)
        self.assertIn('UAEX mentions changed on non-herb crops', out)

    def test_widening_the_footprint_to_another_crop_is_refused(self):
        """Same sabotage with no UAEX text, so the census passes and the footprint check is the
        only thing standing between this and a silently wider promote."""
        bad = list(FINDINGS) + [('apple', {
            'id': 'sabotage_apple', 'summary': 'unrelated text', 'severity': 'low',
            'blocks_launch': False, 'filed_in_session': 'x', 'status': 'open'})]
        path, sha = fixture()
        rc, out = in_process(path, sha, FINDINGS=bad)
        self.assertEqual(rc, 2)
        self.assertIn('crops changed', out)

    def test_a_field_moving_outside_the_edit_list_is_refused(self):
        """Simulate any change the EDITS loop did not make -- a stray mutation, a round-trip
        artifact -- by doctoring the `before` snapshot so an extra field differs."""
        def doctor(d):
            for c in d['crops']:
                if c['slug'] == 'thyme':
                    c['regions']['mid_south']['resolved_by_zone']['8'][
                        'synthesis_note_seasoned'] += ' drift'
        path, sha = fixture()
        rc, out = in_process(path, sha, copy=before_shim(doctor))
        self.assertEqual(rc, 2)
        self.assertIn('touched fields', out)

    def test_a_change_to_another_region_of_a_herb_crop_is_refused(self):
        """mid_atlantic is the SOURCE of this prose and must not be edited by a mid_south hunt.
        Its own NC State credits are a separate ruling (rosemary_mid_atlantic_ncsu_zone_attribution)."""
        def doctor(d):
            for c in d['crops']:
                if c['slug'] == 'thyme':
                    c['regions']['mid_atlantic']['resolved_by_zone']['7'][
                        'synthesis_note_seasoned'] += ' drift'
        path, sha = fixture()
        rc, out = in_process(path, sha, copy=before_shim(doctor))
        self.assertEqual(rc, 2)
        self.assertIn('region mid_atlantic changed', out)

    def test_a_top_level_key_moving_is_refused(self):
        """source_catalog, version and the rest are out of scope for a prose promote."""
        def doctor(d):
            key = next(k for k in d if k != 'crops')
            d[key] = 'sabotage' if not isinstance(d[key], dict) else dict(d[key], _s=1)
        path, sha = fixture()
        rc, out = in_process(path, sha, copy=before_shim(doctor))
        self.assertEqual(rc, 2)
        self.assertIn('top-level', out)

    def test_a_trailing_newline_in_the_written_bytes_is_refused(self):
        """Canonical is COMPACT with no trailing newline. Only reachable on --apply."""
        real_json = promote.json

        class Shim:
            def loads(self, *a, **k):
                return real_json.loads(*a, **k)

            def dumps(self, *a, **k):
                return real_json.dumps(*a, **k) + '\n'

        path, sha = fixture()
        rc, out = in_process(path, sha, apply_=True, json=Shim())
        self.assertEqual(rc, 2)
        self.assertIn('trailing newline', out)


class TestFixtureIsReal(unittest.TestCase):
    def test_fixture_hashes_to_the_pinned_base(self):
        _p, sha = fixture()
        self.assertEqual(sha, BASE_SHA)

    def test_the_defect_is_actually_present_in_the_pre_state(self):
        """Re-verify the record before acting on it: the ten sentences must still be there."""
        data = json.loads(promote_fixture.pre_state(BASE_SHA))
        n = 0
        for slug in CROPS:
            ms = next(c for c in data['crops'] if c['slug'] == slug)['regions']['mid_south']
            for z, c in (ms.get('resolved_by_zone') or {}).items():
                for k, v in c.items():
                    if isinstance(v, str) and k.endswith(('_seasoned', '_beginner')):
                        n += len(UAEX_ATTR.findall(v))
        self.assertEqual(n, 10, 'the pre-state no longer carries the 10 attributions')


if __name__ == '__main__':
    unittest.main()
