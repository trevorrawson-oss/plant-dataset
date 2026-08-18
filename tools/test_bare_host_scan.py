#!/usr/bin/env python3
"""RED-first suite for tools/bare_host_scan.py, and for SELF-PATHED (PLA-161).

SELF-PATHED is the check class nobody implemented: a bare-host citation whose OWN crop already
cites that exact source id PATHED somewhere else. It is strictly cheaper to adjudicate than
SIBLING-PATHED, because there is no cross-crop transfer question at all -- the crop has already
decided this source resolves to that document.

THE NAMED RED CASE, chosen and re-verified at `76f92a20` before this file was written:

    lemon / regions.se_gulf.resolved_by_zone.8 / clemson_hgic

  bare at `https://hgic.clemson.edu`, while lemon itself cites `clemson_hgic` PATHED at
  `https://hgic.clemson.edu/cold-tolerance-in-citrus/` on 14 other nodes -- one URL, 14 times, no
  ambiguity about which document the crop means. It is also hunt #28, and it is MASKED
  (`is_sole=False`) because `tamu_agrilife` on the same node was repointed, which is why no
  campaign ever counted it.

UNITS, stated because this arc keeps re-pricing itself by sliding between them. At `76f92a20`:

    315 bare CITATIONS  /  155 of them SOLE
     78 DECISIONS (crop, region, source_id; crop-level nodes bucketed as their own)
     37 CROPS

A lead is NOT a repoint. SELF-PATHED says "this crop has already resolved this id to a document
elsewhere"; whether that document supports THIS cell's claim is a read
([[sibling-pathed-is-a-discovery-not-a-verdict]], [[sibling-precedent-pressures-a-wrong-repoint]]).
"""
import json
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import bare_host_scan as B  # noqa: E402

HUNT_28 = ('lemon', 'regions.se_gulf.resolved_by_zone.8', 'clemson_hgic')
CLEMSON_COLD = 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'


@pytest.fixture(scope='module')
def data():
    with open(os.path.join(REPO, 'crops_data_final.json'), encoding='utf-8') as fh:
        return json.load(fh)


@pytest.fixture(scope='module')
def crops(data):
    return {c['slug']: c for c in data['crops']}


def region_of(path):
    m = re.match(r'regions\.([^.\[]+)', path)
    return m.group(1) if m else None


# --- the RED case, both halves --------------------------------------------------------------

def test_the_hunt_28_node_is_still_bare_and_still_masked(data):
    """Re-verify the case before relying on it -- a record is not the data it describes."""
    slug, path, sid = HUNT_28
    rows = [r for r in B.scan(data) if (r[1], r[2], r[0]) == (slug, path, sid)]
    assert len(rows) == 1, f'expected exactly one bare row for hunt #28, got {len(rows)}'
    _sid, _slug, _path, is_sole, url = rows[0]
    assert url == 'https://hgic.clemson.edu', f'the bare url moved: {url}'
    assert is_sole is False, (
        'hunt #28 must still be MASKED -- if it went SOLE, a campaign now counts it and the '
        'framing of this case changes')


def test_lemon_already_resolves_clemson_hgic_to_one_document(crops):
    """The other half: the crop has already decided, 14 times, and to a single URL."""
    pathed = B.pathed_by_self(crops['lemon'])
    urls = {u for _p, u in pathed.get('clemson_hgic', [])}
    assert urls == {CLEMSON_COLD}, f'expected one settled document, got {urls}'
    assert len(pathed['clemson_hgic']) == 14, 'the 14-node count moved -- re-read before trusting'


def test_SELF_PATHED_finds_hunt_28(data, crops):
    """The check must reach the case the issue names as its own repoint target."""
    hits = {(r['crop'], r['path'], r['source_id']) for r in B.self_pathed(data)}
    assert HUNT_28 in hits, 'SELF-PATHED missed hunt #28'


# --- the population, with its units pinned ---------------------------------------------------

def test_self_pathed_population_at_this_canonical(data):
    """Pinned so a later reader can tell drift from a re-price. Units are named, not implied."""
    rows = B.self_pathed(data)
    citations = len(rows)
    sole = sum(1 for r in rows if r['is_sole'])
    decisions = {(r['crop'], region_of(r['path']), r['source_id']) for r in rows}
    crops_touched = {r['crop'] for r in rows}
    assert (citations, sole) == (315, 155), f'CITATIONS/SOLE moved: {citations}/{sole}'
    assert len(decisions) == 78, f'DECISIONS moved: {len(decisions)}'
    assert len(crops_touched) == 37, f'CROPS moved: {len(crops_touched)}'


def test_every_self_pathed_row_names_a_real_alternative_document(data):
    """A lead with no document is not a lead. Each row must carry where the crop pathed it."""
    for r in B.self_pathed(data):
        assert r['pathed_at'], f"{r['crop']}/{r['path']}/{r['source_id']} has no document"
        for _p, url in r['pathed_at']:
            assert not B.BARE.fullmatch(url), f'{url} is itself a bare host'


def test_self_pathed_never_points_a_node_at_itself(data):
    """The alternative must be a DIFFERENT node, or the row is circular."""
    for r in B.self_pathed(data):
        assert all(p != r['path'] for p, _u in r['pathed_at']), (
            f"{r['crop']}/{r['path']} cites itself as its own evidence")


# --- non-vacuity ------------------------------------------------------------------------------

def test_MUTATION_removing_the_self_pathed_citations_drops_the_row(data, crops):
    """If lemon stopped citing the Clemson page pathed anywhere, hunt #28 has no self lead."""
    import copy
    d = copy.deepcopy(data)
    cr = {c['slug']: c for c in d['crops']}

    def strip(node):
        if isinstance(node, dict):
            a = node.get('anchoring_urls')
            if isinstance(a, dict) and 'clemson_hgic' in a:
                m = a['clemson_hgic']
                if isinstance(m, dict) and m.get('url') and not B.BARE.fullmatch(m['url']):
                    m['url'] = 'https://hgic.clemson.edu'
            for k, v in node.items():
                if k != 'anchoring_urls':
                    strip(v)
        elif isinstance(node, list):
            for v in node:
                strip(v)

    strip(cr['lemon'])
    hits = {(r['crop'], r['path'], r['source_id']) for r in B.self_pathed(d)}
    assert HUNT_28 not in hits, 'the mutation must remove the lead, or the check is vacuous'


def test_MUTATION_a_bare_only_source_id_is_not_self_pathed(data):
    """A crop citing an id ONLY bare has resolved nothing, and must not produce a lead."""
    import copy
    d = copy.deepcopy(data)
    rows = B.self_pathed(d)
    assert rows, 'need a non-empty population for this to mean anything'
    crop = {c['slug']: c for c in d['crops']}[rows[0]['crop']]
    sid = rows[0]['source_id']

    def bare_everything(node):
        if isinstance(node, dict):
            a = node.get('anchoring_urls')
            if isinstance(a, dict) and sid in a and isinstance(a[sid], dict):
                a[sid]['url'] = 'https://example.edu'
            for k, v in node.items():
                if k != 'anchoring_urls':
                    bare_everything(v)
        elif isinstance(node, list):
            for v in node:
                bare_everything(v)

    bare_everything(crop)
    still = [r for r in B.self_pathed(d)
             if r['crop'] == rows[0]['crop'] and r['source_id'] == sid]
    assert not still, 'an id that is bare everywhere on the crop cannot be SELF-PATHED'


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
