#!/usr/bin/env python3
"""Guard suite for tools/promote_az1005_and_divergence.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch.
Every guard below was mutation-tested by neutering it and confirming this file goes red, and each
test asserts the SPECIFIC abort message so an earlier guard firing cannot be mistaken for the one
under test ([[guard-tests-pass-because-an-earlier-check-fires]]).
"""
import copy
import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                                # noqa: E402
import promote_az1005_and_divergence as P             # noqa: E402


def run(mutate=None, patches=None, apply_=False):
    path, sha = promote_fixture.scratch(P.BASE_SHA, mutate)
    saved = {k: getattr(P, k) for k in (patches or {})}
    for k, v in (patches or {}).items():
        setattr(P, k, v)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', sha,
                '--apply' if apply_ else '--dry-run']
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
        for k, v in saved.items():
            setattr(P, k, v)
    return rc, buf.getvalue(), path


def assert_aborts(fragment, **kw):
    rc, out, _ = run(**kw)
    assert rc == 2, 'expected ABORT, got rc=%s\n%s' % (rc, out)
    assert fragment in out, 'expected %r in output:\n%s' % (fragment, out)
    return out


def test_clean_dry_run_passes_every_guard():
    rc, out, _ = run()
    assert rc == 0, out
    assert '26 edits:' in out
    assert 'verified: 3 held nodes untouched, as intended' in out
    assert 'verified: exactly 6 crops changed, nothing else at top level' in out


def test_sha_drift_aborts():
    path, sha = promote_fixture.scratch(P.BASE_SHA)
    argv, buf, real = sys.argv, io.StringIO(), sys.stdout
    sys.argv = ['promote', '--canonical', path, '--expect-sha', '0' * 64, '--dry-run']
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout, sys.argv = real, argv
    assert rc == 2 and 'canonical drifted' in buf.getvalue()


def test_a_moved_repoint_target_aborts():
    def mutate(crops, _d):
        cell = crops['cantaloupe']['regions']['low_desert_az']['resolved_by_zone']['9']
        cell['anchoring_urls'] = {'uariz_ext': {'url': 'https://extension.arizona.edu/somewhere',
                                                'verified': '2026-01-01'}}
    assert_aborts('no longer cites uariz_ext', mutate=mutate)


def test_an_unaccounted_divergence_row_aborts_on_scope():
    """Coverage is checked against the SCAN, so a new bare-root-vs-catalogued-document node
    appearing anywhere in the dataset stops this promote rather than being missed."""
    def mutate(crops, _d):
        cell = crops['beet']['regions']['ca_south_coast']['resolved_by_zone']['9']
        cell['anchoring_urls']['ucanr_san_diego_mg']['url'] = 'https://www.mastergardenersd.org/'
    assert_aborts('divergence scan and promote disagree', mutate=mutate)


def test_a_prefiled_finding_aborts():
    def mutate(crops, _d):
        vs = crops['lavender'].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(
            {'id': 'warm_arid_lavender_plant_out_window_is_unsourced', 'summary': 'x'})
    assert_aborts('already filed', mutate=mutate)


def test_a_non_t1_target_aborts():
    def mutate(_c, data):
        data['source_catalog']['uariz_ext_az1005']['tier'] = 'T2'
    assert_aborts('is uncatalogued or not T1', mutate=mutate)


def test_rule_a_aborts_when_the_catalog_moves_az1005():
    """AZ1005_URL is a pinned CONSTANT, so this guard is a real assertion. The first version read
    the url out of the catalog and then compared it to the catalog, which could never fire."""
    def mutate(_c, data):
        data['source_catalog']['uariz_ext_az1005']['url'] = \
            'https://extension.arizona.edu/pubs/az9999.pdf'
    assert_aborts('AZ1005_URL disagrees with the catalog entry', mutate=mutate)


def test_rule_a_aborts_when_the_promote_pins_the_wrong_url():
    """The mirror direction: the constant is wrong and the catalog is right."""
    assert_aborts('AZ1005_URL disagrees with the catalog entry',
                  patches={'AZ1005_URL': 'https://extension.arizona.edu/pubs/az0000.pdf'})


def test_rule_b_a_turnip_page_on_an_unvouched_host_aborts():
    """The ONLY thing licensing mastergardenersd.org under this id is that the repo already uses
    it there. Strip those citations and the promote must refuse."""
    def mutate(crops, _d):
        # turnip is deliberately EXCLUDED: stripping its own bare root would trip PREFLIGHT 1
        # first and this test would pass while never reaching the guard it names.
        for slug in ('beet', 'cabbage', 'spinach', 'swiss-chard', 'brussels-sprouts',
                     'collards', 'kale', 'apple', 'pear-asian', 'pear-european'):
            def strip(n):
                if isinstance(n, dict):
                    m = (n.get('anchoring_urls') or {}).get('ucanr_san_diego_mg')
                    if isinstance(m, dict) and 'mastergardenersd.org' in (m.get('url') or ''):
                        m['url'] = 'https://ucanr.edu/site/uc-master-gardener-program-san-diego-county'
                    for k, v in n.items():
                        if k != 'anchoring_urls':
                            strip(v)
                elif isinstance(n, list):
                    for v in n:
                        strip(v)
            strip(crops[slug])
    assert_aborts('never used by ucanr_san_diego_mg', mutate=mutate)


def test_a_surviving_bare_root_aborts():
    """G3 is per-crop and dataset-wide within those crops: repointing the nodes the scan flagged
    while leaving the same bare root live on another node of the same crop must not pass."""
    bad = [r for r in P.REPOINT_ID if r[0] != 'cantaloupe' or 'resolved_by_zone.9' not in r[2]]
    assert_aborts('still cites the bare root', patches={'REPOINT_ID': bad})


def test_repointing_a_held_node_aborts():
    extra = P.REPOINT_ID + [('watermelon', 'low_desert_az',
                             'regions.low_desert_az.resolved_by_zone.9.second_planting')]
    assert_aborts('is a deliberate hold', patches={'REPOINT_ID': extra})


def test_the_consumer_copy_tripwire_is_wired_and_can_fire():
    assert_aborts('consumer copy changed',
                  patches={'prose_of': lambda crop: crop.get('regions') or {}})


def test_an_em_dash_in_a_finding_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad[0][1]['summary'] += ' ' + chr(8212)
    assert_aborts('em dash in', patches={'FINDINGS': bad})


def test_a_finding_with_no_read_date_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad[0][1]['basis'] = 'Arizona, read some time'
    assert_aborts('carries no read date', patches={'FINDINGS': bad})


def test_an_unexpected_crop_in_the_footprint_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad.append(('zucchini-courgette', {
        'id': 'test_only_extra', 'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'summary': 'Arizona portal anchor.', 'basis': 'read 2026-08-05',
        'filed_in_session': P.SESSION}))
    assert_aborts('crops changed =', patches={'FINDINGS': bad})


def test_the_g8_constants_are_hand_written_and_load_bearing():
    assert_aborts('FINDINGS_PER_CROP[lavender] disagrees',
                  patches={'FINDINGS_PER_CROP': dict(P.FINDINGS_PER_CROP, lavender=2)})
    assert_aborts('TOUCHED_REGIONS[lavender]',
                  patches={'TOUCHED_REGIONS': dict(P.TOUCHED_REGIONS, lavender={'warm_arid'})})


# --------------------------------------------------------------------------------------------
# The apply path.
# --------------------------------------------------------------------------------------------

@pytest.fixture(scope='module')
def applied():
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    with open(path, 'rb') as fh:
        raw = fh.read()
    return raw, json.loads(raw)


def test_applied_output_stays_compact(applied):
    raw, _ = applied
    assert not raw.endswith(b'\n')


def test_applied_melons_cite_az1005_and_sources_moved_with_them(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    az = data['source_catalog']['uariz_ext_az1005']['url']
    for slug, region, path in P.REPOINT_ID:
        node = P.resolve(crops[slug], region, path)
        assert node['anchoring_urls']['uariz_ext_az1005']['url'] == az, (slug, path)
        assert 'uariz_ext' not in node['anchoring_urls'], (slug, path)
        if isinstance(node.get('sources'), list):
            assert 'uariz_ext' not in node['sources'], (slug, path)
            assert 'uariz_ext_az1005' in node['sources'], (slug, path)


def test_applied_watermelon_summer_nodes_stay_bare(applied):
    """The load-bearing half of the watermelon verdict: AZ1005 gives it no summer window, so
    those two nodes must NOT have been swept along with the spring three."""
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    for z in ('9', '10'):
        node = crops['watermelon']['regions']['low_desert_az']['resolved_by_zone'][z]['second_planting']
        assert node['anchoring_urls']['uariz_ext']['url'] == 'https://extension.arizona.edu'
        assert 'uariz_ext_az1005' not in node['anchoring_urls']


def test_applied_turnip_cites_the_singular_page(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    for _slug, region, path in P.REPOINT_URL:
        node = P.resolve(crops['turnip'], region, path)
        assert node['anchoring_urls']['ucanr_san_diego_mg']['url'] == \
            'https://www.mastergardenersd.org/turnip/'


def test_applied_divergence_scan_reports_only_the_held_edamame_node(applied):
    """End to end: the scan that motivated this promote must now report exactly the one row that
    was deliberately held, and nothing else."""
    _raw, data = applied
    from catalog_divergence_scan import divergences
    nodes = sorted(n for v in divergences(data).values() for n in v)
    assert nodes == ['edamame:varieties'], nodes


def test_applied_findings_all_landed(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    for slug, f in P.FINDINGS:
        got = [x for x in crops[slug]['verification_status']['open_findings']
               if x.get('id') == f['id']]
        assert len(got) == 1 and got[0]['status'] == f['status'], (slug, f['id'])
