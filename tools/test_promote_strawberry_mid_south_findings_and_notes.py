#!/usr/bin/env python3
"""GUARD SUITE for promote_strawberry_mid_south_findings_and_notes.py -- MUTATION-TESTED.

Pre-state `09358167` (post-promote-2), rebuilt by REPLAY through promote_fixture.CHAIN across BOTH
earlier strawberry promotes. Never skipped on a SHA mismatch.

The load-bearing guard here is the APPEND check: `plantings_provenance` records what was believed
when the region was built, and the correction must sit on top of it with the original surviving
byte-for-byte. A rewrite would destroy the evidence that the template defect ever happened, so the
mutation below proves a rewrite aborts.
"""
import contextlib
import copy
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

PROMOTE = os.path.join(HERE, 'promote_strawberry_mid_south_findings_and_notes.py')
BASE_SHA = '093581673b519fa00337e61a238e99da725eaee7645c2e79d11e2c4f56ba0d51'
SLUG = 'strawberry'


def load():
    spec = importlib.util.spec_from_file_location('sb_fn', PROMOTE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(path, sha, mod=None):
    mod = mod or load()
    buf = io.StringIO()
    old = sys.argv
    sys.argv = [PROMOTE, '--dry-run', '--canonical', path, '--expect-sha', sha]
    try:
        with contextlib.redirect_stdout(buf):
            rc = mod.main()
    finally:
        sys.argv = old
    return rc, buf.getvalue()


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


def ms(crops):
    return crops[SLUG]['regions']['mid_south']


def _doctor_before(mod, fn):
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'crops' in out:
            state['first'] = False
            fn(out)
        return out

    mod.copy.deepcopy = doctor
    return real


# ---------------------------------------------------------------- baseline

def test_baseline_passes():
    path, sha = fixture()
    rc, out = run(path, sha)
    assert rc == 0, out
    assert 'ALL GUARDS PASS' in out
    assert 'strawberry_mid_south_bloom_offset_undocumented' in out
    assert 'byte-for-byte' in out


def test_baseline_is_not_vacuous():
    """The false claim and the template geography must both really be there to correct."""
    data = json.loads(promote_fixture.pre_state(BASE_SHA))
    crops = {c['slug']: c for c in data['crops']}
    prov = ms(crops)['plantings_provenance']
    assert 'the University of Arkansas pioneered and recommends' in prov
    assert 'Ozark uplands/VA' in prov
    assert '[CORRECTION' not in prov
    ids = {f.get('id') for f in crops[SLUG]['verification_status']['open_findings']}
    assert 'strawberry_mid_south_bloom_offset_undocumented' not in ids


# ---------------------------------------------------------------- INPUT mutations

def test_guard_already_filed_aborts():
    def mutate(crops, data):
        crops[SLUG]['verification_status']['open_findings'].append(
            {'id': 'strawberry_mid_south_bloom_offset_undocumented'})
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'already filed' in out


def test_guard_missing_pinned_claim_aborts():
    def mutate(crops, data):
        ms(crops)['plantings_provenance'] = 'Region fill. Nothing to correct.'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'pinned "recommends" claim is not in' in out


def test_guard_already_corrected_aborts():
    def mutate(crops, data):
        ms(crops)['plantings_provenance'] += ' [CORRECTION 2026-01-01: done already.]'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'already carries a correction' in out


def test_guard_missing_frost_note_aborts():
    def mutate(crops, data):
        ms(crops)['resolved_by_zone']['8'].pop('frost_risk_note_seasoned', None)
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'no frost_risk_note_seasoned' in out


def test_guard_base_sha_fires():
    path, sha = fixture()
    rc, out = run(path, 'deadbeef' * 8)
    assert rc == 1, out
    assert 'canonical sha' in out


# ---------------------------------------------------------------- IN-PROCESS mutations

def test_guard_rewrite_instead_of_append_aborts():
    """THE LOAD-BEARING GUARD. Replacing the provenance instead of appending must abort."""
    mod = load()
    # Doctor `before` so the live provenance no longer starts with the original: that is exactly
    # what a rewrite would look like to the guard.
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south'].__setitem__(
            'plantings_provenance', 'A COMPLETELY DIFFERENT ORIGINAL'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'REWRITTEN, not appended' in out


def test_guard_em_dash_in_copy_fires():
    mod = load()
    mod.NOTES = dict(mod.NOTES, **{'7': 'Blossoms open early — cover them.'})
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'em/en dash' in out


def test_guard_temperature_in_copy_fires():
    """fill-the-shape-is-the-defect: FSA6103 publishes no threshold, so none may be invented."""
    mod = load()
    mod.NOTES = dict(mod.NOTES, **{'7': 'Cover the bed below 32 degrees on a frosty night.'})
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'states a temperature' in out


def test_guard_institution_named_in_copy_fires():
    """These cells still cite a bare host, so the reader copy must not credit an institution."""
    mod = load()
    mod.NOTES = dict(mod.NOTES, **{
        '7': 'The University of Arkansas says to cover the bed on a frosty night.'})
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'names an institution' in out


def test_guard_finding_delta_fires():
    """Doctor `before` to DROP a pre-existing finding, so the computed delta gains an extra id.

    (Adding a phantom to `before` does not work: the delta is live-minus-before, so a phantom that
    exists only in `before` never appears in it. Mutation testing caught that the first attempt
    left this guard untested rather than proven.)
    """
    def fn(b):
        ofs = next(c for c in b['crops'] if c['slug'] == SLUG)['verification_status'][
            'open_findings']
        ofs.pop()
    mod = load()
    real = _doctor_before(mod, fn)
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'finding delta' in out


def test_guard_dates_moved_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south']
        ['resolved_by_zone']['7'].__setitem__('harvest', 'MUTATED'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'findings+prose only' in out


def test_guard_catalog_changed_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: b['source_catalog'].pop('uada_ext_chill', None))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'source_catalog changed' in out


def test_guard_other_crop_changed_fires():
    def fn(b):
        for c in b['crops']:
            if c['slug'] != SLUG:
                c['name'] = (c.get('name') or '') + ' MUTATED'
                return
    mod = load()
    real = _doctor_before(mod, fn)
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'only strawberry is in scope' in out


def test_guard_other_region_changed_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['se_gulf']
        .__setitem__('region_label', 'MUTATED'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'only mid_south is in scope' in out


def test_guard_trailing_newline_fires():
    mod = load()
    real = mod.json.dumps

    def shim(obj, **kw):
        s = real(obj, **kw)
        return s + '\n' if kw.get('separators') else s

    mod.json.dumps = shim
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.json.dumps = real
    assert rc == 1, out
    assert 'trailing newline' in out


CHECKS = [v for k, v in sorted(globals().items()) if k.startswith('test_')]

if __name__ == '__main__':
    failed = 0
    for fn in CHECKS:
        try:
            fn()
            print('  ok   %s' % fn.__name__)
        except AssertionError as e:
            failed += 1
            print('  FAIL %s\n       %s' % (fn.__name__, str(e)[:300]))
    print('\n%d/%d checks passed' % (len(CHECKS) - failed, len(CHECKS)))
    sys.exit(1 if failed else 0)
