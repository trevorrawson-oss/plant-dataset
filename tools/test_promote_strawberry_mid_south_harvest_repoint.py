#!/usr/bin/env python3
"""GUARD SUITE for promote_strawberry_mid_south_harvest_repoint.py -- every guard MUTATION-TESTED.

The binding lesson from campaign A: **a check that cannot fail is not a guard.** Mutation testing
found 8 of 21 vacuous on that campaign's first promote. So every check in the promote gets a
mutation here that makes it FIRE, and each assertion pins the guard's own MESSAGE rather than the
exit code -- the checks deliberately overlap, and an exit code cannot tell them apart.

Two families of mutation, because the guards split that way:

  INPUT mutations   rebuild the pinned pre-state through promote_fixture.scratch() with a defect
                    injected, then run the promote against it. These reach the preflight guards.
  IN-PROCESS        load the promote as a MODULE and patch its internals -- shim json.dumps to
  mutations         append a newline, doctor the first copy.deepcopy (the `before` snapshot) to
                    simulate a change the edit loop never made, wrap arms() to move a value on the
                    edit-time call. These reach guards no input can trip.

Fixtures are REBUILT from the pinned pre-state, never skipped on a SHA mismatch
([[promote-guards-went-vacuous-on-sha-skip]]: six suites once ran ZERO checks while green).
"""
import copy
import hashlib
import importlib.util
import io
import json
import os
import sys
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

PROMOTE = os.path.join(HERE, 'promote_strawberry_mid_south_harvest_repoint.py')
BASE_SHA = '3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1'
SLUG = 'strawberry'


def load():
    """Fresh module instance so patches never leak between checks."""
    spec = importlib.util.spec_from_file_location('sb_promote', PROMOTE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(path, sha, mod=None):
    """Run the promote --dry-run against `path`, returning (rc, combined output)."""
    mod = mod or load()
    argv = [PROMOTE, '--dry-run', '--canonical', path, '--expect-sha', sha]
    buf = io.StringIO()
    old = sys.argv
    sys.argv = argv
    try:
        with contextlib.redirect_stdout(buf):
            rc = mod.main()
    finally:
        sys.argv = old
    return rc, buf.getvalue()


def fixture(mutate=None):
    return promote_fixture.scratch(BASE_SHA, mutate)


def target(crops):
    return crops[SLUG]['regions']['mid_south']['plantings'][0]['harvest_start'][0]


# ---------------------------------------------------------------- baseline

def test_baseline_clean_pre_state_passes():
    path, sha = fixture()
    rc, out = run(path, sha)
    assert rc == 0, out
    assert 'ALL GUARDS PASS' in out
    assert 'PINNED 4 nodes' in out
    assert 'bare uada_ext nodes dataset-wide: 91 -> 87' in out


def test_baseline_is_not_vacuous():
    """The pre-state really does hold 4 bare SOLE harvest nodes -- else every check below is air."""
    data = json.loads(promote_fixture.pre_state(BASE_SHA))
    crop = next(c for c in data['crops'] if c['slug'] == SLUG)
    ms = crop['regions']['mid_south']
    for idx in (0, 1):
        for arm in ('harvest_start', 'harvest_end'):
            node = ms['plantings'][idx][arm][0]
            assert node['sources'] == ['uada_ext'], (idx, arm)
            assert node['anchoring_urls']['uada_ext']['url'] == 'https://www.uaex.uada.edu'
    assert 'uada_ext_berries' not in data['source_catalog']


# ---------------------------------------------------------------- INPUT mutations

def test_guard_pinned_url_fires_on_a_different_site():
    """THE CAMPAIGN A PEAR GUARD. A node whose bare host is a DIFFERENT site must abort."""
    def mutate(crops, data):
        target(crops)['anchoring_urls']['uada_ext']['url'] = 'https://homeorchard.ucanr.edu/'
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'not the bare host' in out
    assert 'homeorchard.ucanr.edu' in out


def test_guard_sole_fires_when_a_second_source_is_present():
    def mutate(crops, data):
        n = target(crops)
        n['sources'] = ['uada_ext', 'uada_ext_fsa6107']
        n['anchoring_urls']['uada_ext_fsa6107'] = {'url': 'https://x.example/p.pdf',
                                                   'verified': '2026-08-03'}
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'is not SOLE' in out


def test_guard_already_run_fires_when_catalog_id_exists():
    def mutate(crops, data):
        data['source_catalog']['uada_ext_berries'] = {'id': 'uada_ext_berries'}
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'already in source_catalog' in out


def test_guard_missing_old_id_fires():
    def mutate(crops, data):
        del data['source_catalog']['uada_ext']
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'missing from source_catalog' in out


def test_guard_node_not_citing_old_id_fires():
    def mutate(crops, data):
        n = target(crops)
        n['anchoring_urls'] = {'uada_ext_fsa6107': {'url': 'https://x.example/p.pdf'}}
        n['sources'] = ['uada_ext_fsa6107']
    path, sha = fixture(mutate)
    rc, out = run(path, sha)
    assert rc == 1, out
    assert 'does not cite' in out


def test_guard_base_sha_fires_on_wrong_expectation():
    path, sha = fixture()
    rc, out = run(path, 'deadbeef' * 8)
    assert rc == 1, out
    assert 'canonical sha' in out and '!= expected' in out


# ---------------------------------------------------------------- IN-PROCESS mutations

def test_guard_trailing_newline_fires_when_dumps_is_shimmed():
    """Write-time guard: no input can trip it, so shim json.dumps to append a newline."""
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


def test_guard_value_moved_fires_when_the_edit_touches_a_value():
    """Citation-only guard. Wrap arms() so the EDIT-time call also moves a harvest value."""
    mod = load()
    real = mod.arms
    calls = {'n': 0}

    def wrapper(data):
        out = real(data)
        calls['n'] += 1
        if calls['n'] == 3:          # 1=preflight pin, 2=value fingerprint, 3=the edit loop
            out[0][1]['offset_days'] = 999
        return out

    mod.arms = wrapper
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'A HARVEST VALUE MOVED' in out


def test_guard_bare_count_fires_when_the_drop_is_wrong():
    mod = load()
    mod.bare_uada_nodes = lambda data: 91          # never drops
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'expected a drop of exactly 4' in out


def test_guard_catalog_delta_fires_on_an_extra_key():
    """Doctor the `before` snapshot so the computed delta is 2 keys, not 1."""
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
    assert 'catalog delta is' in out


def test_guard_catalog_url_fires_when_entry_url_is_wrong():
    mod = load()
    mod.CATALOG_ENTRY = dict(mod.CATALOG_ENTRY, url='https://www.uaex.uada.edu')
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'not the verified document url' in out


def test_guard_out_of_scope_crop_fires():
    """Doctor `before` so another crop looks changed -- the edit loop never touches one."""
    mod = load()
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'crops' in out:
            state['first'] = False
            for c in out['crops']:
                if c['slug'] != SLUG:
                    c['name'] = (c.get('name') or '') + ' MUTATED'
                    break
        return out

    mod.copy.deepcopy = doctor
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'only strawberry is in scope' in out


def test_guard_container_prose_fires():
    """resolved_by_zone / plantings_provenance are explicitly out of scope for promote 1."""
    mod = load()
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'crops' in out:
            state['first'] = False
            c = next(x for x in out['crops'] if x['slug'] == SLUG)
            c['regions']['mid_south']['resolved_by_zone']['7']['plant_out'] = 'MUTATED'
        return out

    mod.copy.deepcopy = doctor
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'resolved_by_zone changed' in out


def test_guard_sibling_arm_fires():
    """bloom / plant_out must not move in a harvest-only promote."""
    mod = load()
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'crops' in out:
            state['first'] = False
            c = next(x for x in out['crops'] if x['slug'] == SLUG)
            c['regions']['mid_south']['plantings'][0]['bloom'][0]['offset_days'] = 777
        return out

    mod.copy.deepcopy = doctor
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'plantings[0].bloom changed' in out


def test_guard_crop_count_fires():
    mod = load()
    real = copy.deepcopy
    state = {'first': True}

    def doctor(obj):
        out = real(obj)
        if state['first'] and isinstance(out, dict) and 'crops' in out:
            state['first'] = False
            out['crops'] = out['crops'][:-1]
        return out

    mod.copy.deepcopy = doctor
    try:
        path, sha = fixture()
        rc, out = run(path, sha, mod=mod)
    finally:
        mod.copy.deepcopy = real
    assert rc == 1, out
    assert 'crop count moved' in out


def test_guard_node_count_fires_when_targets_shrink():
    mod = load()
    mod.TARGETS = mod.TARGETS[:3]
    path, sha = fixture()
    rc, out = run(path, sha, mod=mod)
    assert rc == 1, out
    assert 'edited 3 nodes, expected exactly 4' in out


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
