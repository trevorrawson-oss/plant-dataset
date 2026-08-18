#!/usr/bin/env python3
"""Guards for the hunt #28 declaration promote (PLA-161).

REPLAY-PINNED: base `76f92a20` -> post state, so every guard compares the PRE state reconstructed
from git against live canonical rather than against a snapshot of itself. Never skip on a SHA
mismatch -- rebuild the pre-state ([[promote-guards-went-vacuous-on-sha-skip]]).

The blast-radius guard iterates the PRE state AND asserts the key sets match, because a guard that
walks pre only cannot see an ADDITION ([[blast-radius-guards-iterate-pre-only]]).
"""
import copy
import hashlib
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_pla161_hunt28_declaration as P  # noqa: E402

CANONICAL = os.path.join(REPO, 'crops_data_final.json')
MIRROR = 'lemon_regional_anchor_ids_declared_modeled_where_no_document_exists'


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope='module')
def post():
    with open(CANONICAL, encoding='utf-8') as fh:
        return json.load(fh)


def crop(data, slug='lemon'):
    return next(c for c in data['crops'] if c['slug'] == slug)


def findings(data, slug='lemon'):
    return crop(data, slug)['verification_status']['open_findings']


# --- the declaration itself --------------------------------------------------------------------

def test_the_declaration_is_filed(post):
    ids = [f['id'] for f in findings(post)]
    assert P.FINDING['id'] in ids
    assert ids.count(P.FINDING['id']) == 1, 'filed twice'


def test_it_mirrors_the_warm_arid_declarations_key_shape_exactly(post):
    """Ruling: mirror the exact keys of the existing warm_arid clemson_hgic declaration."""
    filed = next(f for f in findings(post) if f['id'] == P.FINDING['id'])
    mirror = next(f for f in findings(post) if f['id'] == MIRROR)
    assert list(filed.keys()) == list(mirror.keys()), (
        f'key shape diverged: {list(filed.keys())} vs {list(mirror.keys())}')
    assert (filed['severity'], filed['status'], filed['blocks_launch']) == (
        mirror['severity'], mirror['status'], mirror['blocks_launch'])


def test_the_summary_carries_the_document_read_not_a_conclusion(post):
    """Every load-bearing fact from the read must survive in the record."""
    s = next(f for f in findings(post) if f['id'] == P.FINDING['id'])['summary']
    for fragment in ('15F for satsuma', 'taxonomy list', 'no lemon damage temperature',
                     'no zone-level judgement for the Southeast Gulf', 'uc_anr_8100',
                     'lemon_cold_threshold_was_miscredited_now_uc8100',
                     'No claim on this node rests on this document'):
        assert fragment in s, f'missing from the declaration: {fragment!r}'


def test_the_summary_uses_commas_not_dashes(post):
    """Ruling: commas rather than dashes, so it reads consistently beside its neighbours."""
    s = next(f for f in findings(post) if f['id'] == P.FINDING['id'])['summary']
    assert '--' not in s, 'double-hyphen dash in the declaration'
    for dash in ('—', '–'):
        assert dash not in s, f'{dash!r} in the declaration'


# --- what it must NOT have done -----------------------------------------------------------------

def test_the_citation_is_still_bare(post):
    """CASE 2: the decision is declared, the URL is NOT repointed."""
    region, zone = P.NODE_PATH
    node = crop(post)['regions'][region]['resolved_by_zone'][zone]
    assert node['anchoring_urls'][P.SOURCE_ID]['url'] == P.BARE_URL
    assert P.SOURCE_ID in node['sources'], 'the citation must stay recorded, not be dropped'


def test_the_node_is_otherwise_byte_identical(pre, post):
    region, zone = P.NODE_PATH
    a = crop(pre)['regions'][region]['resolved_by_zone'][zone]
    b = crop(post)['regions'][region]['resolved_by_zone'][zone]
    assert a == b, 'the promote must not have touched the node at all'


def test_nothing_else_in_the_dataset_moved(pre, post):
    """Blast radius. Compares BOTH directions so an ADDITION cannot hide."""
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    fa = crop(a)['verification_status']['open_findings']
    fb = crop(b)['verification_status']['open_findings']
    added = [f for f in fb if f['id'] == P.FINDING['id']]
    assert len(added) == 1
    fb.remove(added[0])
    assert set(x['id'] for x in fa) == set(x['id'] for x in fb), 'finding id sets diverged'
    assert a == b, 'the promote changed something outside the one appended finding'


def test_no_other_crop_was_touched(pre, post):
    pre_by = {c['slug']: c for c in pre['crops']}
    post_by = {c['slug']: c for c in post['crops']}
    assert set(pre_by) == set(post_by), 'the crop roster changed'
    for slug in pre_by:
        if slug == 'lemon':
            continue
        assert pre_by[slug] == post_by[slug], f'{slug} changed'


def test_canonical_is_still_compact(post):
    raw = open(CANONICAL, 'rb').read()
    assert b'\n' not in raw, 'canonical gained a newline; it must stay COMPACT'
    assert raw == json.dumps(post, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


# --- non-vacuity ---------------------------------------------------------------------------------

def test_MUTATION_the_blast_radius_guard_catches_a_stray_edit(pre, post):
    """A guard that cannot fail is not a guard. Perturb the post state and demand a difference."""
    b = copy.deepcopy(post)
    crop(b)['regions'][P.NODE_PATH[0]]['resolved_by_zone'][P.NODE_PATH[1]]['suitability'] = 'x'
    a = copy.deepcopy(pre)
    fb = crop(b)['verification_status']['open_findings']
    fb.remove(next(f for f in fb if f['id'] == P.FINDING['id']))
    assert a != b, 'the blast-radius comparison would not have noticed a stray edit'


def test_MUTATION_the_promote_refuses_a_wrong_base_sha(tmp_path, monkeypatch):
    """The SHA preflight must exit 1, never proceed on a base it does not recognise."""
    fake = tmp_path / 'crops.json'
    fake.write_bytes(b'{"crops":[]}')
    monkeypatch.setattr(P, 'CANONICAL', str(fake))
    monkeypatch.setattr(sys, 'argv', ['promote'])
    assert P.main() == 1


def test_MUTATION_the_promote_refuses_when_the_node_is_no_longer_bare(tmp_path, monkeypatch, pre):
    """If someone repointed the citation, a CASE 2 declaration is the wrong act and must abort."""
    d = copy.deepcopy(pre)
    region, zone = P.NODE_PATH
    node = crop(d)['regions'][region]['resolved_by_zone'][zone]
    node['anchoring_urls'][P.SOURCE_ID]['url'] = 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'
    raw = json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    fake = tmp_path / 'crops.json'
    fake.write_bytes(raw)
    monkeypatch.setattr(P, 'CANONICAL', str(fake))
    monkeypatch.setattr(P, 'BASE_SHA', hashlib.sha256(raw).hexdigest())
    monkeypatch.setattr(sys, 'argv', ['promote'])
    assert P.main() == 1


def test_MUTATION_the_promote_refuses_to_file_twice(tmp_path, monkeypatch, post):
    """Re-running must abort rather than append a duplicate declaration."""
    raw = open(CANONICAL, 'rb').read()
    fake = tmp_path / 'crops.json'
    fake.write_bytes(raw)
    monkeypatch.setattr(P, 'CANONICAL', str(fake))
    monkeypatch.setattr(P, 'BASE_SHA', hashlib.sha256(raw).hexdigest())
    monkeypatch.setattr(sys, 'argv', ['promote'])
    assert P.main() == 1


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
