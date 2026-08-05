#!/usr/bin/env python3
"""Tests for tools/catalog_divergence_scan.py.

Both halves of the narrow check are mutation-tested: a node that stops being a root must drop out,
and an id whose catalog entry stops naming a document must drop out. A check that cannot stop
firing is not a check.

The last test pins the MEASUREMENT that justifies the narrowing. Without it, the next reader sees
a scan reporting 8 rows, assumes it is too timid, widens it, and re-discovers the 729-row flood
the hard way.
"""
import copy
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import catalog_divergence_scan as S  # noqa: E402


@pytest.fixture(scope='module')
def data():
    with open(S.CANONICAL, encoding='utf-8') as fh:
        return json.load(fh)


def nodes_of(found):
    return sorted(n for v in found.values() for n in v)


def test_only_the_deliberately_held_edamame_node_remains(data):
    """The scan found 8 nodes when it was built. Seven were turnip's, repointed the same day at
    mastergardenersd.org/turnip/. The one that remains is held ON PURPOSE: no Cornell edamame
    variety document exists to repoint at, which is recorded in
    edamame_varieties_no_cornell_edamame_document_exists."""
    assert nodes_of(S.divergences(data)) == ['edamame:varieties']


def test_carrot_is_absent_because_it_was_already_repaired(data):
    """The defect that motivated the scan. It must NOT reappear."""
    assert not [n for n in nodes_of(S.divergences(data)) if n.startswith('carrot:')]


def test_MUTATION_reintroducing_carrots_defect_makes_it_reappear(data):
    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'carrot'][0]
    z8 = crop['regions']['warm_arid']['resolved_by_zone']['8']
    z8['anchoring_urls']['nmsu_chart']['url'] = 'https://desert.tamu.edu/'
    found = S.divergences(scratch)
    assert 'carrot:regions.warm_arid.resolved_by_zone.8' in nodes_of(found)
    key = [k for k in found if k[0] == 'nmsu_chart'][0]
    assert S.host(key[1]) != S.host(key[2]), 'the host-disagreement signal should also fire'


def test_MUTATION_a_pathed_node_url_drops_out(data):
    """Half one: the node must actually be a domain ROOT. Rebuilt on a scratch copy, since the
    real turnip nodes were repointed once this scan surfaced them."""
    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'turnip'][0]
    cell = crop['regions']['ca_south_coast']['resolved_by_zone']['9']
    cell['anchoring_urls']['ucanr_san_diego_mg']['url'] = 'https://www.mastergardenersd.org/'
    assert 'turnip:regions.ca_south_coast.resolved_by_zone.9' in nodes_of(S.divergences(scratch))
    cell['anchoring_urls']['ucanr_san_diego_mg']['url'] = \
        'https://www.mastergardenersd.org/turnip/'
    assert 'turnip:regions.ca_south_coast.resolved_by_zone.9' not in \
        nodes_of(S.divergences(scratch))


def test_MUTATION_a_root_catalog_url_drops_the_whole_id(data):
    """Half two: the catalog must already NAME a document. If it is itself a root there is
    nothing to repoint at, and the row would be noise rather than a cheap fix."""
    scratch = copy.deepcopy(data)
    assert nodes_of(S.divergences(scratch)) == ['edamame:varieties']
    scratch['source_catalog']['cornell_ext']['url'] = 'https://cals.cornell.edu'
    assert nodes_of(S.divergences(scratch)) == []


def test_the_wider_definitions_really_do_flood(data):
    """Pins the 2026-08-05 measurement that justifies the narrowing, so nobody widens this scan
    on the assumption that 8 rows means it is too timid."""
    catalog = data.get('source_catalog') or {}
    by_domain = 0
    for sid, _slug, _path, url in S.walk(data):
        cu = (catalog.get(sid) or {}).get('url')
        if cu and S.host(url) != S.host(cu):
            by_domain += 1
    assert by_domain > 500, by_domain

    # and the "catalog names a pathed document, node cites something else" variant
    pathed_variant = 0
    for sid, _slug, _path, url in S.walk(data):
        cu = (catalog.get(sid) or {}).get('url')
        if cu and not S.BARE.fullmatch(cu) and url != cu:
            pathed_variant += 1
    assert pathed_variant > 500, pathed_variant

    assert sum(len(v) for v in S.divergences(data).values()) == 1
