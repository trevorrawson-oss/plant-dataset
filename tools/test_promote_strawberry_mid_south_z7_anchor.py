#!/usr/bin/env python3
"""GUARD SUITE for promote_strawberry_mid_south_z7_anchor.py -- every guard MUTATION-TESTED.

This promote moves consumer-visible planting and harvest dates, so the bar is higher than for the
citation-only pass: the guards must prove not just that the RIGHT cell changed but that it now
reproduces from the anchor it declares, and that the mid_atlantic arithmetic that caused the defect
cannot come back.

Pre-state is `0ab9b42b` (post-promote-1), rebuilt by REPLAY through promote_fixture.CHAIN -- it was
never committed on its own. Never skipped on a SHA mismatch
([[promote-guards-went-vacuous-on-sha-skip]]).

Two guards were REMOVED from the promote rather than tested, because no input can make them fail:
they re-read objects the edit had just written. Their intent is covered by the reproduction
invariant, which does fail. A check that cannot fail is not a guard.
"""
import contextlib
import copy
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

PROMOTE = os.path.join(HERE, 'promote_strawberry_mid_south_z7_anchor.py')
BASE_SHA = '0ab9b42b58e5a047d302a4dd865b82b997688ad21129a3bd64f2cc1f5116820c'
SLUG = 'strawberry'


def load():
    spec = importlib.util.spec_from_file_location('sb_z7', PROMOTE)
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


def z7(crops):
    return ms(crops)['resolved_by_zone']['7']


# ---------------------------------------------------------------- baseline

def test_baseline_passes_and_reports_the_defect():
    path, sha = fixture()
    rc, out = run(path, sha)
    assert rc == 0, out
    assert 'DEFECT CONFIRMED' in out
    assert 'ALL GUARDS PASS' in out
    assert 'Apr 1 - Apr 22     -> Mar 13 - Mar 20' in out
    assert 'May 27 - Jun 24    -> May 22 - Jun 19' in out


def test_baseline_is_not_vacuous_the_defect_is_really_there():
    """All four z7 arms must reproduce from Apr 15 and none from Apr 10, else this is air."""
    data = json.loads(promote_fixture.pre_state(BASE_SHA))
    crops = {c['slug']: c for c in data['crops']}
    cell = z7(crops)
    assert cell['resolved_from']['last_frost'] == 'Apr 10'
    assert cell['plant_out'] == 'Apr 1 - Apr 22'
    assert cell['bloom'] == 'Apr 29 - May 20'
    assert cell['harvest'] == 'May 27 - Jun 24'
    base = datetime.datetime(2026, 4, 15)
    p = ms(crops)['plantings'][0]
    got = base + datetime.timedelta(days=p['harvest_start'][0]['offset_days'])
    assert got.strftime('%b %-d') == 'May 27'


# ---------------------------------------------------------------- INPUT mutations

def test_guard_wrong_declared_anchor_aborts():
    def mutate(crops, data):
        z7(crops)['resolved_from']['last_frost'] = 'Apr 15'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'declared anchor is' in out


def test_guard_already_fixed_aborts_rather_than_reruns():
    """THE ANTI-STALE-RECORD GUARD. If the cell already reproduces, there is nothing to fix."""
    def mutate(crops, data):
        c = z7(crops)
        c['plant_out'] = 'Mar 27 - Apr 17'
        c['bloom'] = 'Apr 24 - May 15'
        c['harvest_start'] = 'May 22'
        c['harvest_end'] = 'Jun 19'
        c['harvest'] = 'May 22 - Jun 19'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'already reproduces' in out


def test_guard_already_catalogued_aborts():
    def mutate(crops, data):
        data['source_catalog']['uada_ext_fsa6103'] = {'id': 'uada_ext_fsa6103'}
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'already catalogued' in out


def test_guard_unexpected_arm_offsets_abort():
    def mutate(crops, data):
        ms(crops)['plantings'][0]['plant_out'][0]['offset_days'] = -21
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'plant_out arm is' in out


def test_guard_missing_synthesis_phrase_aborts():
    def mutate(crops, data):
        a = ms(crops)['plantings'][0]['plant_out'][0]
        a['synthesis_note'] = 'Set crowns whenever.'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'synthesis_note does not contain' in out


def test_guard_missing_grown_as_phrase_aborts():
    def mutate(crops, data):
        z7(crops)['grown_as_note_seasoned'] = 'A perennial bed.'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'grown_as_note_seasoned does not contain' in out


def test_guard_stray_two_weeks_phrase_elsewhere_is_caught():
    """The region-wide prose scan: a stray occurrence outside the two edited fields must trip."""
    def mutate(crops, data):
        z7(crops)['grown_as_note_beginner'] += ' Plant two weeks before the last spring frost.'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'prose still says' in out


def test_guard_base_sha_fires():
    path, sha = fixture()
    rc, out = run(path, 'deadbeef' * 8)
    assert rc == 1, out
    assert 'canonical sha' in out


# ---------------------------------------------------------------- IN-PROCESS mutations

def test_guard_reproduction_invariant_fires():
    """THE CORE GUARD. Break derive_expected after the edit so a stored value no longer matches."""
    mod = load()
    real = mod.derive_expected
    calls = {'n': 0}

    def wrapper(region):
        out = real(region)
        calls['n'] += 1
        if calls['n'] >= 3:      # 1=preflight, 2=the edit, 3+=the guard read
            out = dict(out, harvest_start='Jan 1')
        return out

    mod.derive_expected = wrapper
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'does not reproduce from declared anchor' in out


def test_guard_calendar_length_fires():
    mod = load()
    mod.derive_berry_calendar = lambda ga, cell: ['dormant'] * 11
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'not 12 months' in out


def test_guard_calendar_none_aborts():
    mod = load()
    mod.derive_berry_calendar = lambda ga, cell: None
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'calendar deriver returned None' in out


def test_guard_catalog_delta_fires():
    mod = load()
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'source_catalog' in out:
            state['first'] = False
            out['source_catalog'].pop('uada_ext_chill', None)
        return out

    mod.copy.deepcopy = doctor
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'catalog delta' in out


def _doctor_before(mod, fn):
    """Patch the FIRST copy.deepcopy (the `before` snapshot) with fn(before)."""
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


def test_guard_anchor_moved_fires():
    """'Fixing' the defect by moving the anchor to the dates must abort, not pass.

    Doctored on `before`, which is the only reachable form: the edit never writes resolved_from,
    so a re-read of the live cell can never disagree with itself.
    """
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south']
        ['resolved_by_zone']['7']['resolved_from'].__setitem__('last_frost', 'Apr 15'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'resolved_from changed' in out


def test_guard_z8_changed_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south']
        ['resolved_by_zone']['8'].__setitem__('plant_out', 'MUTATED'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'z8 changed' in out


def test_guard_sibling_arm_changed_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south']
        ['plantings'][0]['bloom'][0].__setitem__('offset_days', 999))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'arm changed' in out


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


def test_guard_out_of_scope_region_key_fires():
    mod = load()
    real = _doctor_before(mod, lambda b: next(
        c for c in b['crops'] if c['slug'] == SLUG)['regions']['mid_south']
        .__setitem__('region_notes_beginner', 'MUTATED'))
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'out of scope' in out


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
