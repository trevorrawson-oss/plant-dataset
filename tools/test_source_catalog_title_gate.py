#!/usr/bin/env python3
"""Tests for source_catalog_title_gate (A54, PLA-199). TDD: written RED before the gate exists.

Runs BOTH ways (pytest and `python3 tools/test_source_catalog_title_gate.py`) with every check
in the test body -- a skip guard under __main__ is invisible to pytest (memory rule).

The suite works pre- AND post-promote: when the live canonical is still the PLA-199 base
(no titles), the post-state is synthesized via promote_pla199_titles.apply(); once the promote
lands, the live file IS the post-state. Either way the same assertions bind.
"""
import copy
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

import promote_pla199_titles as promote  # noqa: E402
from source_catalog_title_gate import LEGACY_UNFILLED, title_violations  # noqa: E402


def _load_states():
    raw = open(CANONICAL, 'rb').read()
    d = json.loads(raw)
    if 'title' in d['source_catalog']['vce_426_331']:
        post = d
        pre = None  # promote already landed; pre-state only via fixture, not needed here
    else:
        pre = d
        post = promote.apply(json.loads(raw))
    return pre, post


PRE, POST = _load_states()
POST_CAT = POST['source_catalog']


def _mini(url, title=None, name='X'):
    e = {'id': 'x', 'name': name, 'url': url, 'tier': 'T1'}
    if title is not None:
        e['title'] = title
    return e


def test_legacy_unfilled_is_the_hand_counted_52():
    # The frozen exemption list IS the unfilled record: 50 uncached + unr_sp2007 (unreadable
    # cache) + lsu_agcenter_3363 (no title line in text layer). Hand-counted, not derived.
    assert len(LEGACY_UNFILLED) == 52
    assert 'unr_sp2007' in LEGACY_UNFILLED
    assert 'lsu_agcenter_3363' in LEGACY_UNFILLED
    assert 'uscrn' in LEGACY_UNFILLED and 'aspca' in LEGACY_UNFILLED
    # and it matches the promote's own unfilled record, both directions
    assert LEGACY_UNFILLED == frozenset(promote.UNFILLED)


def test_post_state_is_clean():
    assert title_violations(POST_CAT) == []


def test_pre_state_floods_at_exactly_101():
    # RED evidence at the data level: without the backfill, every non-exempt document-scoped
    # id (101, hand-counted) violates. Run only while the pre-state is on hand.
    if PRE is None:
        return
    v = title_violations(PRE['source_catalog'])
    assert len(v) == 101, f'expected 101 pre-backfill violations, got {len(v)}'
    assert all('A54' in m for m in v)


def test_new_docscoped_id_without_title_bounces():
    cat = copy.deepcopy(POST_CAT)
    cat['new_ext_pub_999'] = _mini('https://ext.example.edu/pubs/999/growing-things')
    v = title_violations(cat)
    assert len(v) == 1
    assert 'A54' in v[0] and 'new_ext_pub_999' in v[0]


def test_new_docscoped_id_with_title_is_clean():
    cat = copy.deepcopy(POST_CAT)
    cat['new_ext_pub_999'] = _mini('https://ext.example.edu/pubs/999/growing-things',
                                   title='Growing Things')
    assert title_violations(cat) == []


def test_institution_root_with_title_bounces():
    # D2: a bare anchor states no title; decorating one is the fill-the-shape trap.
    cat = copy.deepcopy(POST_CAT)
    cat['some_ext'] = _mini('https://ext.example.edu/', title='Example Extension')
    v = title_violations(cat)
    assert len(v) == 1
    assert 'A54' in v[0] and 'some_ext' in v[0] and 'institution-root' in v[0]


def test_institution_root_without_title_is_clean():
    cat = copy.deepcopy(POST_CAT)
    cat['some_ext'] = _mini('https://ext.example.edu')
    assert title_violations(cat) == []


def test_blank_or_nonstring_title_bounces():
    for bad in ('', '   ', 42, None):
        cat = copy.deepcopy(POST_CAT)
        cat['new_ext_pub_999'] = _mini('https://ext.example.edu/pubs/999', title=bad)
        v = title_violations(cat)
        assert len(v) == 1 and 'A54' in v[0], f'title={bad!r} not caught'


def test_stripping_a_backfilled_title_bounces():
    # A filled id is NOT exempt: deleting its title regresses and must flag.
    cat = copy.deepcopy(POST_CAT)
    del cat['vce_426_331']['title']
    v = title_violations(cat)
    assert len(v) == 1 and 'vce_426_331' in v[0]


def test_exempt_id_without_title_is_clean_but_stale_exemption_bounces():
    # unr_sp2007 sits unfilled and exempt: clean. Retire the id and the exemption is stale:
    # the list must shrink honestly, so the gate flags it.
    cat = copy.deepcopy(POST_CAT)
    assert title_violations(cat) == []
    del cat['unr_sp2007']
    v = title_violations(cat)
    assert len(v) == 1
    assert 'A54' in v[0] and 'unr_sp2007' in v[0] and 'exempt' in v[0].lower()


def test_a54_dormant_on_prebackfill_canonical():
    # D3 is two-phase: hard gate AFTER the backfill, convention until then. The wiring arms
    # off the DATA (any title present), so a pre-backfill canonical -- the live tree while
    # PLA-160 runs in parallel -- must not red 121 crops on PLA-199's unpromoted work.
    if PRE is None:
        return  # promote landed; dormancy no longer reachable from the live file
    out = subprocess.run(
        [sys.executable, os.path.join(HERE, 'whole_crop_gate.py'), 'cherry-tomato', CANONICAL],
        capture_output=True, text=True).stdout
    assert 'A54' in out, 'A54 section missing entirely'
    assert 'DORMANT' in out, 'A54 not marked dormant on a pre-backfill catalog'
    assert not any('catalog-title' in l and 'VIOLATION' in l for l in out.splitlines()), \
        'A54 red on the pre-backfill canonical -- this floods every parallel gauntlet'


def test_a54_reachable_through_whole_crop_gate():
    # Reachability is MEASURED, not assumed (a gate can be green and unreachable). Sabotage a
    # scratch copy with a titleless minted id and the REAL runner must go red on it, naming A54.
    scratch = os.path.join(HERE, '.a54_reachability_scratch.json')
    sab = copy.deepcopy(POST)
    sab['source_catalog']['new_ext_pub_999'] = _mini(
        'https://ext.example.edu/pubs/999/growing-things')
    try:
        with open(scratch, 'w', encoding='utf-8') as f:
            f.write(json.dumps(sab, separators=(',', ':'), ensure_ascii=False))
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, 'whole_crop_gate.py'), 'cherry-tomato', scratch],
            capture_output=True, text=True).stdout
        assert 'A54' in out, 'whole_crop_gate never printed the A54 section'
        assert any('VIOLATION' in l and 'new_ext_pub_999' in l for l in out.splitlines()), \
            'sabotaged catalog did not go red through the real runner'
    finally:
        if os.path.exists(scratch):
            os.remove(scratch)


TESTS = [v for k, v in sorted(globals().items()) if k.startswith('test_')]

if __name__ == '__main__':
    for t in TESTS:
        t()
        print(f'ok {t.__name__}')
    print(f'{len(TESTS)}/{len(TESTS)} green (direct runner)')
