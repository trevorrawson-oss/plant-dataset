#!/usr/bin/env python3
"""Guard suite for tools/promote_campaign_c_closeout.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch, so this
suite cannot go vacuous when canonical moves on ([[promote-guards-went-vacuous-on-sha-skip]]).

Every check below was MUTATION-TESTED by neutering the guard it targets and confirming this file
goes red. Where a sabotage could be caught by an EARLIER guard than the one under test, the test
asserts the SPECIFIC abort message, not just rc==2 -- that is the
[[guard-tests-pass-because-an-earlier-check-fires]] trap, hit three times in two days on this arc.

    $ python3 -m pytest tools/test_promote_campaign_c_closeout.py -q
"""
import copy
import hashlib
import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                              # noqa: E402
import promote_campaign_c_closeout as P             # noqa: E402

BASE = P.BASE_SHA


def run(mutate=None, patches=None, apply_=False):
    path, sha = promote_fixture.scratch(BASE, mutate)
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


# --------------------------------------------------------------------------------------------
# 0. The clean run, and the footprint it claims.
# --------------------------------------------------------------------------------------------

def test_clean_dry_run_passes_every_guard():
    rc, out, _ = run()
    assert rc == 0, out
    assert '13 edits:' in out
    assert 'preflight: all 5 repoint targets carry their pinned pre-state url' in out
    assert 'preflight: all 29 held nodes still cite the bare host SOLE' in out
    assert 'verified: 29 CASE 2 nodes still bare, as intended' in out
    assert 'verified: exactly 10 crops changed, nothing else at top level' in out


def test_all_three_vouching_rules_are_exercised():
    """Each repoint earns its citation a different way. If they collapsed to one rule, two of
    the three checks would be dead weight and nobody would notice."""
    rc, out, _ = run()
    assert rc == 0
    assert 'a: is the catalog url' in out
    assert 'b: document on the catalog root host donaanamastergardeners.nmsu.edu' in out
    assert 'c: this crop already cites it under tamu_agrilife' in out


def test_finding_ids_are_unique_and_crops_match_the_declared_footprint():
    ids = [f['id'] for _s, f in P.FINDINGS]
    assert len(ids) == len(set(ids))
    assert sorted({s for s, _f in P.FINDINGS} | {s for s, _r, _p in P.REPOINTS}
                  | {s for s, _r, _p in P.HELD}) == sorted(P.CROPS)


# --------------------------------------------------------------------------------------------
# 1. Pre-state pinning.
# --------------------------------------------------------------------------------------------

def test_sha_drift_aborts():
    path, sha = promote_fixture.scratch(BASE)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', '0' * 64, '--dry-run']
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
    assert rc == 2
    assert 'canonical drifted' in buf.getvalue()


def test_a_moved_repoint_target_aborts_rather_than_being_overwritten():
    def mutate(crops, _data):
        node = crops['carrot']['regions']['warm_arid']['resolved_by_zone']['8']
        node['anchoring_urls']['nmsu_chart']['url'] = 'https://example.edu/somewhere-else'
    assert_aborts('expected nmsu_chart', mutate=mutate)


def test_a_repointed_held_node_aborts():
    """If someone had already fixed one of the 29, the promote must notice, not sail past."""
    def mutate(crops, _data):
        node = crops['shallot']['regions']['rgv']['resolved_by_zone']['9']
        node['anchoring_urls'] = {'tamu_agrilife': {'url': 'https://agrilifeextension.tamu.edu/x',
                                                    'verified': '2026-08-05'}}
    assert_aborts('no longer cites the bare host SOLE', mutate=mutate)


def test_an_unaccounted_sole_rgv_node_aborts_on_scope():
    """Coverage is checked against bare_host_scan, not against this file, so a node that appears
    in the region cannot be silently forgotten."""
    def mutate(crops, _data):
        p = crops['arugula']['regions']['rgv']['plantings'][0]
        p['bloom'] = [{'from': 'plant_out', 'offset_days': 10, 'window_days': 0,
                       'sources': ['tamu_agrilife'],
                       'anchoring_urls': {'tamu_agrilife': {
                           'url': 'https://agrilifeextension.tamu.edu', 'verified': '2026-07-13'}}}]
    assert_aborts('scan and promote disagree on rgv scope', mutate=mutate)


def test_a_prefiled_finding_aborts():
    def mutate(crops, _data):
        vs = crops['pumpkin'].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(
            {'id': 'pumpkin_pilot_regional_source_anchors_general', 'summary': 'x'})
    assert_aborts('already filed', mutate=mutate)


# --------------------------------------------------------------------------------------------
# 2. G1 / G2 -- what a repoint is allowed to point at.
# --------------------------------------------------------------------------------------------

def test_a_non_t1_repoint_target_aborts():
    def mutate(_crops, data):
        data['source_catalog']['nmsu_chart']['tier'] = 'T2'
    assert_aborts('repoints at non-T1 id nmsu_chart', mutate=mutate)


def test_a_repoint_crossing_institutions_aborts():
    """G1 specifically. A first version of this test moved nmsu_chart's catalog url to
    pubs.nmsu.edu and expected an abort; the promote correctly allowed it, because carrot ALREADY
    cites the chart PDF under nmsu_chart on its direct_sow arms, so rule (c) vouched for it. The
    test was wrong, not the guard. Crossing to a genuinely different institution is the real
    violation."""
    def mutate(_crops, data):
        data['source_catalog']['nmsu_chart']['url'] = 'https://agrilifeextension.tamu.edu'
    assert_aborts('a different institution from its catalog url', mutate=mutate)


def test_an_uncatalogued_repoint_target_aborts():
    def mutate(_crops, data):
        del data['source_catalog']['nmsu_chart']
    assert_aborts('repoints at uncatalogued id nmsu_chart', mutate=mutate)


def test_garlic_loses_its_vouching_when_the_crop_stops_citing_bexar():
    """Rule (c) is the ONLY thing letting the Bexar page be cited without minting a catalog id.
    Strip the crop's other Bexar citations and the promote must refuse."""
    def mutate(crops, _data):
        def strip(n):
            if isinstance(n, dict):
                for _sid, m in (n.get('anchoring_urls') or {}).items():
                    if isinstance(m, dict) and m.get('url') == P.BEXAR_GARLIC:
                        m['url'] = 'https://agrilifeextension.tamu.edu'
                for k, v in n.items():
                    if k != 'anchoring_urls':
                        strip(v)
            elif isinstance(n, list):
                for v in n:
                    strip(v)
        strip(crops['garlic'])
    assert_aborts('neither the catalog nor this crop vouches for', mutate=mutate)


def test_g4_catches_a_node_listed_in_both_repoints_and_held():
    """G4 re-checks the held nodes AFTER the edits, and it is the only guard that can catch a
    path added to REPOINTS while it is still sitting in HELD. Neutering it left all 26 other
    tests green, which by this arc's own rule makes it either untested or dead weight; this test
    is what earns it its place. PREFLIGHT2 cannot cover this, because it runs before the edits
    and the node is still bare at that point."""
    onion_pdf = 'https://aggie-horticulture.tamu.edu/vegetable/files/2011/10/onion1.pdf'
    bad = dict(P.REPOINTS)
    bad[('shallot', 'rgv', 'regions.rgv.resolved_by_zone.9')] = (
        'tamu_agrilife', 'https://agrilifeextension.tamu.edu', onion_pdf)
    out = assert_aborts('is a deliberate CASE 2 node', patches={'REPOINTS': bad})
    assert 'shallot' in out


def test_the_wrong_institution_url_surviving_elsewhere_aborts():
    """G3 is dataset-wide on purpose: fixing the attribution on the two nodes the scan flagged
    while leaving it live on a third is the defect this arc has re-found repeatedly."""
    def mutate(crops, _data):
        cell = crops['kale']['regions']['warm_arid']['resolved_by_zone']['8']
        cell['anchoring_urls']['nmsu_chart']['url'] = P.WRONG_URL
    assert_aborts('the wrong-institution url survives', mutate=mutate)


# --------------------------------------------------------------------------------------------
# 3. G5 / G6 / G7 / G8 -- blast radius and finding hygiene.
# --------------------------------------------------------------------------------------------

def test_the_consumer_copy_tripwire_is_wired_and_can_fire():
    """No path in this promote writes prose, so the tripwire is proven by widening what it
    watches until the promote's own legitimate edits fall inside it. That shows the comparison
    fires on a real difference rather than comparing two identical empty dicts."""
    def watch_everything(crop):
        return crop.get('regions') or {}
    assert_aborts('consumer copy changed', patches={'prose_of': watch_everything})


def test_an_em_dash_in_a_finding_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad[0][1]['summary'] += ' ' + chr(8212) + ' oops'
    assert_aborts('em dash in', patches={'FINDINGS': bad})


def test_a_finding_naming_no_institution_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad[0][1]['summary'] = 'the window is modeled and nothing is cited'
    assert_aborts('names no institution', patches={'FINDINGS': bad})


def test_a_finding_with_no_read_date_in_its_basis_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad[0][1]['basis'] = 'Texas A&M AgriLife, read at some point'
    assert_aborts('carries no read date', patches={'FINDINGS': bad})


def test_an_unexpected_crop_in_the_footprint_aborts():
    bad = copy.deepcopy(P.FINDINGS)
    bad.append(('zucchini-courgette', {
        'id': 'campaign_c_test_only', 'severity': 'low', 'status': 'accepted',
        'blocks_launch': False, 'summary': 'Texas A&M AgriLife portal anchor.',
        'basis': 'read 2026-08-05', 'filed_in_session': P.SESSION}))
    assert_aborts('crops changed =', patches={'FINDINGS': bad})


def test_the_g8_constants_are_hand_written_and_load_bearing():
    """G8's expected sets used to be DERIVED from the edit tables, which made them incapable of
    disagreeing with what they validated. They are now hand-written, and these two mutations
    prove it: change either constant and the promote refuses."""
    bad = dict(P.FINDINGS_PER_CROP, arugula=2)
    assert_aborts('FINDINGS_PER_CROP[arugula] = 2 but FINDINGS holds 1',
                  patches={'FINDINGS_PER_CROP': bad})

    bad_regions = dict(P.TOUCHED_REGIONS, carrot={'warm_arid', 'rgv'})
    assert_aborts('TOUCHED_REGIONS[carrot]', patches={'TOUCHED_REGIONS': bad_regions})


def test_g8_catches_a_finding_landing_on_an_unlisted_crop():
    """FINDINGS_PER_CROP is checked against FINDINGS, so adding a finding for a crop the constant
    does not list fails before the data is even inspected."""
    bad = copy.deepcopy(P.FINDINGS)
    extra = copy.deepcopy(bad[0][1])
    extra['id'] = 'rgv_arugula_absent_second_copy'
    bad.append(('arugula', extra))
    assert_aborts('FINDINGS_PER_CROP[arugula] = 1 but FINDINGS holds 2',
                  patches={'FINDINGS': bad})


# --------------------------------------------------------------------------------------------
# 4. The apply path -- what actually lands.
# --------------------------------------------------------------------------------------------

@pytest.fixture(scope='module')
def applied():
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    with open(path, 'rb') as fh:
        raw = fh.read()
    return raw, json.loads(raw), out


def test_applied_output_stays_compact_with_no_trailing_newline(applied):
    raw, _data, _out = applied
    assert not raw.endswith(b'\n')
    assert b', "' not in raw[:20000] and b'\n  ' not in raw[:20000]


def test_applied_repoints_landed_exactly(applied):
    _raw, data, _out = applied
    crops = {c['slug']: c for c in data['crops']}
    for (slug, region, path), (sid, _old, new) in P.REPOINTS.items():
        node = P.resolve(crops[slug], region, path)
        assert node['anchoring_urls'][sid]['url'] == new, (slug, path)
        assert node['anchoring_urls'][sid]['verified'] == P.VERIFIED


def test_applied_findings_landed_and_carry_their_status(applied):
    _raw, data, _out = applied
    crops = {c['slug']: c for c in data['crops']}
    for slug, f in P.FINDINGS:
        got = [x for x in crops[slug]['verification_status']['open_findings']
               if x.get('id') == f['id']]
        assert len(got) == 1, (slug, f['id'])
        assert got[0]['status'] == f['status']
        assert got[0]['filed_in_session'] == P.SESSION


def test_applied_leaves_the_29_held_nodes_bare(applied):
    _raw, data, _out = applied
    crops = {c['slug']: c for c in data['crops']}
    for slug, region, path in P.HELD:
        assert P.cites_bare(P.resolve(crops[slug], region, path),
                            P.RGV_BARE[1], P.RGV_BARE[0]), (slug, path)


def test_applied_drops_the_carrot_decision_from_the_bare_host_scan(applied):
    """The whole point of hunt 24: after the fix, that node is no longer a bare host at all."""
    _raw, data, _out = applied
    from bare_host_scan import scan
    carrot = [(sid, path) for sid, slug, path, sole, _u in scan(data)
              if slug == 'carrot' and sole and sid == 'nmsu_chart']
    assert carrot == [], carrot


def test_applied_reprice_shows_hunt_13_and_24_resolved(applied):
    """End-to-end: the re-price tool, run on the applied state, must agree that the campaign
    moved. If the promote and the measurement tool disagreed, one of them is lying."""
    _raw, data, _out = applied
    import campaign_c_reprice as R
    crops = {c['slug']: c for c in data['crops']}
    nodes = R.collect(data, crops)
    dec = {(n[3], n[1], n[2]): n[7] for n in nodes}
    assert ('carrot', 'warm_arid', 'nmsu_chart') not in dec
    # garlic's harvest arms stay bare BY DESIGN, and the promote files the finding that
    # adjudicates them, so the decision reads DECLARED-ABSENCE rather than disappearing.
    assert dec[('garlic', 'rgv', 'tamu_agrilife')] == 'DECLARED-ABSENCE'
    # Everything this promote adjudicates must be closed. watermelon is the one exception and it
    # is an ORDERING fact, not a gap: its low_desert_az verdict was filed by the LATER AZ1005
    # follow-up, so against this promote's own fixture the reprice table correctly reports that
    # the finding it names is not yet on the crop. Asserting the exception by name keeps the
    # check honest -- a genuinely missed decision would still fail here.
    still_open = {k[0] for k, v in dec.items() if v == 'OPEN' and k[0] not in R.CITRUS}
    assert still_open == {'watermelon'}, still_open
    # 30 non-citrus decisions before; hunt 24's carrot and hunt 17's two tomatoes stop being
    # bare hosts entirely once repointed, so the campaign loses three decisions, not one.
    assert ('beefsteak-tomato', 'warm_arid', 'nmsu_donaana_mg') not in dec
    assert ('heirloom-tomato', 'warm_arid', 'nmsu_donaana_mg') not in dec
    assert len([k for k in dec if k[0] not in R.CITRUS]) == 27
