#!/usr/bin/env python3
"""Guards for the PLA-253 nematode-anchor promote.

REPLAY-PINNED BOTH ENDS: the PRE state is reconstructed from git by hash and the POST state by
REPLAYING this promote on that fixture, so the suite never reads live canonical
([[promote-guards-went-vacuous-on-sha-skip]] -- never skip on a SHA mismatch, rebuild;
[[promote-suite-post-must-be-replayed-not-live]] -- and never read live canonical either).

The blast-radius guard asserts KEY-SET EQUALITY BEFORE comparing any value, in both
directions, because a guard that walks the PRE state cannot see anything ADDED in POST --
the shape behind all four PLA-162 defects ([[blast-radius-guards-iterate-pre-only]]). This
promote ADDS a catalog entry and ADDS a source, so a one-directional guard here would be
blind to the two things most worth watching.

Mutation evidence: tools/mutate_pla253_nematode_suite.py
"""
import copy
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_pla253_nematode_anchor as P  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_pla253_nematode_anchor.py')

_post = {}


def post_bytes():
    """The bytes THIS promote produces, by replaying it on the rebuilt pre-state.

    WAS live canonical, and that was a defect, not a style choice: the two blast-radius
    guards compared the pinned pre-state against whatever canonical happened to be, so the
    NEXT promote by anyone reddened them. PLA-290 converted 59 variety entries across 11
    crops and turned both red for a reason that had nothing to do with this promote. A
    promote suite validates ITS OWN promote; live canonical is release_verify's and
    gate_all's job ([[promote-suite-post-must-be-replayed-not-live]]). Repaired 2026-08-21.
    """
    if 'raw' not in _post:
        path, sha = promote_fixture.scratch(P.BASE_SHA)
        assert sha == P.BASE_SHA
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-800:]}'
        _post['raw'] = open(path, 'rb').read()
    return _post['raw']


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope='module')
def post():
    return json.loads(post_bytes())


def method(data):
    return data['control_methods'][P.METHOD]


# --- the prose ------------------------------------------------------------------------------

def test_the_beginner_line_is_exactly_the_authored_delivery(post):
    assert method(post)['how_it_works_beginner'] == P.NEW_BEGINNER


def test_the_pro_is_exactly_the_authored_delivery(post):
    assert method(post)['pros'][1] == P.NEW_PRO_1


def test_the_unanchored_safety_phrasings_are_gone(post):
    """The defect was a safety claim resting on an efficacy document. Both places that made
    it in the old, unsupported words must be gone -- not just the one that was rewritten."""
    entry = method(post)
    assert 'safe for people and pets' not in entry['how_it_works_beginner'].lower()
    assert P.PREV_PRO_1 not in entry['pros']
    assert P.PREV_BEGINNER != entry['how_it_works_beginner']


def test_the_claim_names_all_three_protected_classes(post):
    """The document's claim is about plants AND vertebrates. Prose that quietly narrowed back
    to people-and-pets would re-open the gap this promote closed, while still reading fixed."""
    line = method(post)['how_it_works_beginner'].lower()
    for cls in ('people', 'pets', 'plants'):
        assert cls in line, f'{cls} dropped from the safety claim'
    assert 'exempt' in line, 'the EPA exemption claim is gone'


def test_no_em_dash_in_the_consumer_copy(post):
    entry = method(post)
    assert '—' not in entry['how_it_works_beginner']
    assert '—' not in entry['pros'][1]


# --- the anchor -----------------------------------------------------------------------------

def test_the_new_source_is_in_the_catalog_as_t1(post):
    e = post['source_catalog'][P.NEW_SOURCE_ID]
    assert e['tier'] == 'T1'
    assert e['url'] == P.NEW_CATALOG_ENTRY['url']


def test_the_new_catalog_entry_is_titled_at_mint_time(post):
    """A54: a document-scoped (pathed) id must carry a title READ OFF the document. New mints
    are never exempt -- mint time is when the author has the document open."""
    e = post['source_catalog'][P.NEW_SOURCE_ID]
    assert isinstance(e.get('title'), str) and e['title'].strip()
    assert e['title'] == 'Entomopathogenic Nematodes'


def test_the_method_cites_the_new_source_and_still_cites_uc_ipm(post):
    """ADD, never replace. UC IPM is the efficacy anchor and the PNW handbook is the safety
    anchor; dropping either leaves a claim uncovered."""
    entry = method(post)
    assert P.NEW_SOURCE_ID in entry['sources']
    assert P.KEPT_SOURCE_ID in entry['sources']


def test_anchoring_urls_match_sources_exactly(post):
    """control_ladder_gate's CATALOG rule, asserted here so a break is attributed to this
    promote rather than surfacing later as a roster-wide gate failure."""
    entry = method(post)
    assert set(entry['anchoring_urls']) == set(entry['sources'])


def test_the_uc_ipm_anchor_is_untouched(pre, post):
    """The efficacy anchor must not be silently re-verified or re-pointed by a safety pass."""
    assert method(post)['anchoring_urls'][P.KEPT_SOURCE_ID] == \
        method(pre)['anchoring_urls'][P.KEPT_SOURCE_ID]


# --- blast radius ---------------------------------------------------------------------------

def test_nothing_else_in_the_dataset_moved(pre, post):
    """Both directions. Key sets FIRST, then values -- this promote ADDS a catalog id and
    ADDS a source, and a pre-only walk cannot see either."""
    a, b = copy.deepcopy(pre), copy.deepcopy(post)

    # the catalog: exactly one id added, nothing else touched
    ca, cb = a['source_catalog'], b['source_catalog']
    assert set(cb) - set(ca) == {P.NEW_SOURCE_ID}, 'catalog gained something else'
    assert set(ca) - set(cb) == set(), 'catalog entries were DROPPED'
    del cb[P.NEW_SOURCE_ID]
    assert ca == cb, 'an existing catalog entry changed'

    # the method: exactly the four intended edits
    ma, mb = a['control_methods'][P.METHOD], b['control_methods'][P.METHOD]
    assert set(ma) == set(mb), 'the method gained or lost a key'
    ma['how_it_works_beginner'] = mb['how_it_works_beginner']
    ma['pros'] = list(mb['pros'])
    ma['sources'] = list(mb['sources'])
    ma['anchoring_urls'] = dict(mb['anchoring_urls'])
    assert ma == mb, 'the method changed outside the four intended fields'

    assert set(a) == set(b), 'a top-level dataset key was added or dropped'
    assert a == b, 'the promote changed something outside the nematode entry and its source'


def test_no_other_control_method_was_touched(pre, post):
    ka, kb = set(pre['control_methods']), set(post['control_methods'])
    assert ka == kb, 'the control_methods roster changed'
    for k in ka:
        if k == P.METHOD:
            continue
        assert pre['control_methods'][k] == post['control_methods'][k], f'{k} changed'


def test_no_crop_was_touched(pre, post):
    a = {c['slug']: c for c in pre['crops']}
    b = {c['slug']: c for c in post['crops']}
    assert set(a) == set(b), 'the crop roster changed'
    for s in a:
        assert a[s] == b[s], f'{s} changed'


def test_the_pros_list_kept_its_length_and_its_other_entry(pre, post):
    """A rewrite of pros[1] must not become an append, a reorder, or a drop of pros[0]."""
    pa, pb = method(pre)['pros'], method(post)['pros']
    assert len(pa) == len(pb) == 2
    assert pa[0] == pb[0], 'pros[0] moved'


def test_canonical_is_still_compact(post):
    raw = post_bytes()
    assert b'\n' not in raw, 'canonical gained a newline; it must stay COMPACT'
    assert raw == json.dumps(post, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


# --- non-vacuity ----------------------------------------------------------------------------

def test_MUTATION_the_blast_radius_guard_catches_a_stray_edit(pre, post):
    """The blast-radius guard asserted above is worth nothing unless a planted edit reddens
    it. Sabotage a field the promote does not touch and confirm the comparison fails."""
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    b['control_methods']['bt']['best_use'] = 'SABOTAGE'
    with pytest.raises(AssertionError):
        ka, kb = set(a['control_methods']), set(b['control_methods'])
        assert ka == kb
        for k in ka:
            if k == P.METHOD:
                continue
            assert a['control_methods'][k] == b['control_methods'][k], f'{k} changed'


def test_MUTATION_the_catalog_guard_catches_an_extra_mint(pre, post):
    """The one-id-added assertion must fail when a second id rides along."""
    ca = dict(pre['source_catalog'])
    cb = dict(post['source_catalog'])
    cb['ghost_source'] = {'id': 'ghost_source', 'tier': 'T1'}
    with pytest.raises(AssertionError):
        assert set(cb) - set(ca) == {P.NEW_SOURCE_ID}, 'catalog gained something else'


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
