#!/usr/bin/env python3
"""Adversarial tests for tools/campaign_c_reprice.py.

The tool's whole value is that it collapses campaign C from 35 open decisions to 6, against a
kickoff that says no collapse is available. A tool that reports a collapse must be provably
capable of NOT reporting one, so every check here is mutation-tested: the scratch-copy tests
below each break one thing and assert the verdict changes. Written after the arc was burned
three times by guards that were green and vacuous
([[guard-derived-from-what-it-checks-is-vacuous]], [[guard-tests-pass-because-an-earlier-check-fires]]).

NEVER mutates canonical -- every mutation is applied to a deepcopy.
"""
import copy
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import campaign_c_reprice as R  # noqa: E402


# PINNED to `6b2dcb8e`, the canonical at campaign C's close, where this suite's published numbers
# (99 nodes / 33 claim / 66 container / 5 citrus rows) are true. Verified: the same collect() over
# the kickoff's `5a52a76c` yields 116 nodes, so these constants were always describing C's CLOSE
# state, not its start.
#
# Why it is pinned rather than re-baselined: the 2026-08-06 PLA-114 promote repointed
# `lemon/warm_arid/tamu_agrilife` -- which IS campaign C's hunt #8, whose citrus residue C
# explicitly deferred into campaign D. So C's bare set legitimately fell 99 -> 98 and its citrus
# rows 5 -> 4. Chasing that with new constants each time a later campaign closes one of C's
# deferred rows would erase the record of what C was priced at, and the number would slowly stop
# meaning anything. The TOOL still reads live canonical.
BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'


@pytest.fixture(scope='module')
def data():
    import promote_fixture
    return json.loads(promote_fixture.pre_state(BASE_SHA))


@pytest.fixture(scope='module')
def crops(data):
    return {c['slug']: c for c in data['crops']}


def verdicts(data):
    crops = {c['slug']: c for c in data['crops']}
    nodes = R.collect(data, crops)
    out = {}
    for _h, reg, sid, slug, _p, _a, _u, v, why in nodes:
        out[(slug, reg, sid)] = (v, why)
    return out


# --------------------------------------------------------------------------------------------
# 1. The measured shape. These pin the numbers the ledger and Linear will carry.
# --------------------------------------------------------------------------------------------

# These pin the POST-PROMOTE state (canonical 754c51a0). The pre-promote numbers this suite
# originally pinned are kept in the assertions' comments, because the DELTA is the campaign's
# result and a bare "112" tells the next reader nothing.

def test_shape_is_99_nodes_over_30_decisions(data, crops):
    """116 / 35 / 7 at kickoff. The closeout promote took it to 112 / 32 / 5 (carrot's
    heat_pause, both tomatoes' zone cells and garlic's plant_out stopped being bare hosts,
    closing hunts #17 and #24). The AZ1005 follow-up took it to 99 / 30: thirteen more
    low_desert_az nodes moved to uariz_ext_az1005, closing cantaloupe and honeydew-melon
    entirely and leaving watermelon only its two deliberately-held summer nodes."""
    nodes = R.collect(data, crops)
    assert len(nodes) == 99
    assert len({(n[3], n[1], n[2]) for n in nodes}) == 30
    assert len({n[0] for n in nodes}) == 5


def test_node_class_split_is_33_claim_66_container(data, crops):
    """34 claim / 82 container at kickoff. garlic's plant_out was the only claim arm ever
    repointed; everything the AZ1005 pass moved was a container, which is why the claim count
    is unchanged from the closeout while the container count fell by 13."""
    nodes = R.collect(data, crops)
    claim = [n for n in nodes if n[5] in R.CLAIM_ARMS]
    assert len(claim) == 33
    assert len(nodes) - len(claim) == 66


def test_nineteen_decisions_are_declared_by_an_anchor_finding(data):
    """Was 17. pumpkin's two decisions joined once the closeout filed the finding its five
    sibling cucurbits and peppers already carried."""
    v = verdicts(data)
    assert sum(1 for x in v.values() if x[0] == 'DECLARED-ANCHOR') == 19


def test_nothing_is_open_after_the_citrus_rescope(data):
    """The campaign's result. Six decisions were honestly open before the closeout promote:
    beefsteak-tomato plus the five rgv crops. Every one is now adjudicated, and the only OPEN
    rows left are lemon and lime, which belong to campaign D."""
    v = verdicts(data)
    still_open = [k for k, x in v.items() if x[0] == 'OPEN' and k[0] not in R.CITRUS]
    assert still_open == []
    assert sorted({k[0] for k, x in v.items() if x[0] == 'OPEN'}) == ['lemon', 'lime']


def test_the_six_rgv_crops_are_now_adjudicated_not_open(data):
    v = verdicts(data)
    for slug in ('arugula', 'broad-beans-fava', 'garlic', 'shallot', 'snow-peas',
                 'sugar-snap-peas'):
        verdict, why = v[(slug, 'rgv', 'tamu_agrilife')]
        assert verdict in ('DECLARED-ABSENCE', 'DECLARED-ANCHOR'), (slug, verdict, why)


def test_kickoff_53_region_test_no_longer_reproduces_zero_and_that_is_our_doing(data, crops):
    """The kickoff measured "0 of 35 decisions carry a finding naming their region" and it was
    correct. It is now 6 of 32 -- and every one of the six is a finding THIS campaign filed, whose
    ids begin `rgv_`. Recorded so the change reads as our own writing rather than as evidence the
    original measurement was wrong. It was right; it was the wrong question."""
    nodes = R.collect(data, crops)
    named = set()
    for _h, reg, _sid, slug, _p, _a, _u, _v, _w in nodes:
        for f in R.findings(crops[slug]):
            if reg in (f.get('id') or ''):
                named.add((slug, f['id']))
    assert sorted(s for s, _f in named) == [
        'arugula', 'broad-beans-fava', 'garlic', 'shallot', 'snow-peas', 'sugar-snap-peas',
        'watermelon']
    assert all(fid.startswith(('rgv_', 'low_desert_az_')) for _s, fid in named), named


# --------------------------------------------------------------------------------------------
# 2. The alias check. This is the load-bearing one -- it is what keeps the peas open.
# --------------------------------------------------------------------------------------------

@pytest.mark.parametrize('slug', ['snow-peas', 'sugar-snap-peas', 'broad-beans-fava'])
def test_peas_alias_is_refused_because_fall_veg_competes(crops, slug):
    ok, competing = R.alias_is_unambiguous(crops[slug], 'tamu_agrilife')
    assert not ok
    assert 'tamu_agrilife_fall_veg' in competing


@pytest.mark.parametrize('slug', ['beefsteak-tomato', 'heirloom-tomato'])
def test_tomato_alias_is_refused_because_two_nmsu_ids_compete(crops, slug):
    ok, competing = R.alias_is_unambiguous(crops[slug], 'nmsu_donaana_mg')
    assert not ok
    assert 'nmsu_ext' in competing


@pytest.mark.parametrize('slug', ['acorn-squash', 'butternut-squash', 'spaghetti-squash',
                                  'cayenne-pepper', 'eggplant'])
def test_squash_alias_is_accepted_because_nothing_competes(crops, slug):
    for sid in ('nmsu_ext', 'tamu_agrilife'):
        if sid in R.cited_ids(crops[slug]):
            ok, competing = R.alias_is_unambiguous(crops[slug], sid)
            assert ok, '%s/%s unexpectedly ambiguous: %s' % (slug, sid, competing)


def test_MUTATION_removing_the_competing_id_flips_snow_peas_to_declared(data):
    """Proves the competing `tamu_agrilife_fall_veg` citation is the ONLY thing that would keep
    snow-peas off the alias path.

    Since the closeout promote, snow-peas reads DECLARED-ABSENCE, and that verdict is decided
    BEFORE the alias logic is ever reached -- so this test has to strip the absence finding too,
    or it would pass without exercising the check it names
    ([[guard-tests-pass-because-an-earlier-check-fires]])."""
    assert verdicts(data)[('snow-peas', 'rgv', 'tamu_agrilife')][0] == 'DECLARED-ABSENCE'

    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'snow-peas'][0]
    crop['verification_status']['open_findings'] = [
        f for f in crop['verification_status']['open_findings']
        if f.get('id') != R.ABSENCE_FINDING[('rgv', 'snow-peas')]]
    assert verdicts(scratch)[('snow-peas', 'rgv', 'tamu_agrilife')][0] == 'OPEN'

    def strip(n):
        if isinstance(n, dict):
            a = n.get('anchoring_urls')
            if isinstance(a, dict):
                a.pop('tamu_agrilife_fall_veg', None)
            for k, v in n.items():
                if k != 'anchoring_urls':
                    strip(v)
        elif isinstance(n, list):
            for v in n:
                strip(v)

    strip(crop)
    # the finding must also name the bare id for the ALIAS path to be reachable at all
    for f in R.findings(crop):
        if f['id'] == 'snow_peas_pilot_regional_source_urls':
            f['summary'] = f['summary'].replace('tamu_agrilife_fall_veg', 'tamu_agrilife')
    R.ANCHOR_FINDING[('rgv', 'snow-peas', 'tamu_agrilife')] = \
        'snow_peas_pilot_regional_source_urls'
    try:
        after = verdicts(scratch)[('snow-peas', 'rgv', 'tamu_agrilife')]
    finally:
        del R.ANCHOR_FINDING[('rgv', 'snow-peas', 'tamu_agrilife')]
    assert after[0] == 'DECLARED-ANCHOR', after


def test_MUTATION_adding_a_competing_id_flips_acorn_to_open(data):
    """The mirror image: acorn is DECLARED only via the ALIAS path, so introducing a second
    nmsu-family citation must reopen it."""
    assert verdicts(data)[('acorn-squash', 'warm_arid', 'nmsu_ext')][0] == 'DECLARED-ANCHOR'

    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'acorn-squash'][0]
    crop['regions']['warm_arid']['plantings'][0].setdefault('anchoring_urls', {})[
        'nmsu_ext_cr457b'] = {'url': 'https://pubs.nmsu.edu/_circulars/CR457B/',
                              'verified': '2026-08-05'}
    v, why = verdicts(scratch)[('acorn-squash', 'warm_arid', 'nmsu_ext')]
    assert v == 'OPEN', (v, why)
    assert 'nmsu_ext_cr457b' in why


# --------------------------------------------------------------------------------------------
# 3. Presence. A table asserting an adjudication the data no longer carries must not fire.
# --------------------------------------------------------------------------------------------

def test_every_anchor_table_entry_is_present_and_names_its_source(crops):
    """COVERAGE, not overlap: every row must hold, so a deleted finding fails the suite."""
    for (reg, slug, sid), fid in sorted(R.ANCHOR_FINDING.items()):
        f = R.finding(crops[slug], fid)
        assert f is not None, '%s is NOT on %s' % (fid, slug)
        matched, mode, why = R.names_source(crops[slug], f, sid)
        assert matched, '%s does not name %s on %s (%s)' % (fid, sid, slug, why)
        assert mode in ('STRICT', 'ALIAS')


def test_every_modeled_table_entry_is_present(crops):
    for slug, fid in sorted(R.MODELED_FINDING.items()):
        assert R.finding(crops[slug], fid) is not None, '%s is NOT on %s' % (fid, slug)


def test_anchor_table_has_no_phantom_rows(data, crops):
    """Every table key must correspond to a decision the scan actually produces."""
    real = {(n[1], n[3], n[2]) for n in R.collect(data, crops)}
    for key in R.ANCHOR_FINDING:
        assert key in real, 'ANCHOR_FINDING row %s matches no SOLE decision' % (key,)


def test_MUTATION_deleting_the_finding_flips_okra_to_open(data):
    assert verdicts(data)[('okra', 'warm_arid', 'nmsu_ext')][0] == 'DECLARED-ANCHOR'
    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'okra'][0]
    fs = crop['verification_status']['open_findings']
    crop['verification_status']['open_findings'] = [
        f for f in fs if f.get('id') != 'okra_pilot_region_anchor_base_urls']
    v, why = verdicts(scratch)[('okra', 'warm_arid', 'nmsu_ext')]
    assert v == 'OPEN', (v, why)
    assert 'NOT ON THIS CROP' in why


def test_MUTATION_unnaming_the_source_flips_bell_pepper_to_open(data):
    """The finding stays present but stops naming the id -- STRICT must not survive that."""
    assert verdicts(data)[('bell-pepper', 'warm_arid', 'nmsu_ext')][0] == 'DECLARED-ANCHOR'
    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'bell-pepper'][0]
    for f in R.findings(crop):
        if f['id'] == 'bell_pepper_pilot_regional_source_anchors_general':
            f['summary'] = f['summary'].replace('nmsu_ext', 'uga_c963').replace('NMSU', 'UGA')
    v, why = verdicts(scratch)[('bell-pepper', 'warm_arid', 'nmsu_ext')]
    assert v == 'OPEN', (v, why)


# --------------------------------------------------------------------------------------------
# 4. The catalog-repointable class -- the defect this pass found.
# --------------------------------------------------------------------------------------------

def test_carrot_is_fixed_and_now_cites_the_catalog_document(data, crops):
    """The defect this pass found, now repaired. Before the closeout promote both nodes cited
    `nmsu_chart` at https://desert.tamu.edu/ -- a bare TEXAS host under a NEW MEXICO source id --
    and this decision read CATALOG-REPOINTABLE with "the hosts DISAGREE"."""
    assert ('carrot', 'warm_arid', 'nmsu_chart') not in verdicts(data)
    chart = data['source_catalog']['nmsu_chart']['url']
    node = crops['carrot']['regions']['warm_arid']['resolved_by_zone']['8']
    assert node['anchoring_urls']['nmsu_chart']['url'] == chart
    assert node['heat_pause']['anchoring_urls']['nmsu_chart']['url'] == chart


def test_the_wrong_institution_url_is_cited_nowhere_in_the_dataset(data):
    """Fixing the nodes the scan flagged while leaving the same attribution live on a third is
    the defect this arc keeps re-finding, so this checks the whole dataset, not the two nodes."""
    hits = []

    def walk(n, slug, path):
        if isinstance(n, dict):
            for sid, m in (n.get('anchoring_urls') or {}).items():
                if isinstance(m, dict) and m.get('url') == 'https://desert.tamu.edu/':
                    hits.append('%s:%s:%s' % (slug, path, sid))
            for k, v in n.items():
                if k != 'anchoring_urls':
                    walk(v, slug, '%s.%s' % (path, k))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                walk(v, slug, '%s[%d]' % (path, i))

    for c in data['crops']:
        walk(c, c['slug'], '')
    assert hits == [], hits


def test_MUTATION_the_catalog_repointable_verdict_is_still_reachable_and_still_conditional(data):
    """carrot no longer exercises this verdict, so rebuild the pre-promote condition on a scratch
    copy and check BOTH directions: it fires when the catalog knows a document, and stops firing
    when the catalog only knows a root. Without this the whole class would go untested the moment
    its one instance was fixed."""
    scratch = copy.deepcopy(data)
    crop = [c for c in scratch['crops'] if c['slug'] == 'carrot'][0]
    z8 = crop['regions']['warm_arid']['resolved_by_zone']['8']
    z8['heat_pause']['anchoring_urls']['nmsu_chart']['url'] = 'https://desert.tamu.edu/'
    v, why = verdicts(scratch)[('carrot', 'warm_arid', 'nmsu_chart')]
    assert v == 'CATALOG-REPOINTABLE', (v, why)
    assert 'hosts DISAGREE' in why

    scratch['source_catalog']['nmsu_chart']['url'] = 'https://donaanamastergardeners.nmsu.edu'
    v2, _why = verdicts(scratch)[('carrot', 'warm_arid', 'nmsu_chart')]
    assert v2 != 'CATALOG-REPOINTABLE', v2


# --------------------------------------------------------------------------------------------
# 5. Citrus stays visible. A campaign must never shrink by hiding rows.
# --------------------------------------------------------------------------------------------

def test_citrus_is_reported_not_dropped(data):
    v = verdicts(data)
    citrus = [k for k in v if k[0] in R.CITRUS]
    assert len(citrus) == 5, citrus
    nodes = [n for n in R.collect(data, {c['slug']: c for c in data['crops']})
             if n[3] in R.CITRUS]
    assert len(nodes) == 31
