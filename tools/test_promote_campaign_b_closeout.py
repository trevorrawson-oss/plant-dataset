#!/usr/bin/env python3
"""Guard suite for tools/promote_campaign_b_closeout.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch.
Every check below was MUTATION-TESTED by neutering the guard it targets and confirming this file
goes red. Guards that could not be made to fail were removed from the promote.

    $ python3 -m pytest tools/test_promote_campaign_b_closeout.py -q
    $ python3 tools/test_promote_campaign_b_closeout.py
"""
import copy
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                              # noqa: E402
import promote_campaign_b_closeout as P             # noqa: E402

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


def _doctor_before(fn):
    class Shim:
        def __init__(self):
            self.n = 0
            self.real = copy.deepcopy

        def __call__(self, obj, *a, **k):
            out = self.real(obj, *a, **k)
            self.n += 1
            if self.n == 1:
                fn(out)
            return out

    saved = copy.deepcopy
    copy.deepcopy = Shim()
    try:
        return run()
    finally:
        copy.deepcopy = saved


# --------------------------------------------------------------------------- happy path

def test_clean_pre_state_passes():
    rc, out, _ = run()
    assert rc == 0, out
    assert '4 repoints agree with the catalog' in out
    assert '14 CASE 2 nodes still bare' in out
    assert 'promote scope == bare_host_scan scope (18 nodes)' in out


def test_apply_writes_compact_and_repoints():
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    raw = open(path, 'rb').read()
    assert not raw.endswith(b'\n') and b'\n' not in raw, 'canonical is not compact'
    data = json.loads(raw)
    crops = {c['slug']: c for c in data['crops']}
    for (slug, region, p), (sid, _u) in P.REPOINTS.items():
        assert set(P.resolve(crops[slug], region, p)['anchoring_urls']) == {sid}
    for slug, region, p in P.HELD:
        bsid, burl = P.BARE[region]
        assert P.cites_bare(P.resolve(crops[slug], region, p), bsid, burl), '%s %s moved' % (slug, p)
    assert 'ncsu_ext_toolbox_vicia_faba' in data['source_catalog']


def test_repoint_preserves_node_shape():
    """strawberry's container has no `sources` key; the promote must not invent one."""
    _rc, _out, path = run(apply_=True)
    crops = {c['slug']: c for c in json.loads(open(path, 'rb').read())['crops']}
    sb = P.resolve(crops['strawberry'], 'mid_south', 'regions.mid_south.plantings[0]')
    assert 'sources' not in sb, 'a sources key was invented on a node that had none'
    ap = P.resolve(crops['apple'], 'mid_south', 'regions.mid_south.plantings[0]')
    assert ap['sources'] == ['uada_ext_fruit_trees'], 'an existing sources key was not updated'


def test_rerun_against_promoted_state_aborts():
    _rc, _out, path = run(apply_=True)
    import hashlib
    raw = open(path, 'rb').read()
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha',
                hashlib.sha256(raw).hexdigest(), '--dry-run']
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
    assert rc == 2 and 'premise changed' in buf.getvalue()


# --------------------------------------------------------------------------- preflight

def test_sha_drift_aborts():
    path, _sha = promote_fixture.scratch(BASE)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', 'f' * 64, '--dry-run']
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
    assert rc == 2 and 'canonical drifted' in buf.getvalue()


def test_already_repointed_node_aborts():
    def mutate(crops, _d):
        n = P.resolve(crops['apple'], 'mid_south', 'regions.mid_south.plantings[0]')
        n['anchoring_urls'] = {'uada_ext_fruit_trees': {'url': P.FRUIT_TREES[1],
                                                        'verified': '2026-08-04'}}
    assert_aborts('premise changed', mutate=mutate)


def test_new_bare_node_in_scope_aborts():
    """The coverage guard: a node the SCAN reports and the promote does not account for.

    This is the guard that caught fig's mid_atlantic bloom node on the first dry run.
    """
    held = tuple(h for h in P.HELD if h[0] != 'elderberry')
    assert_aborts('scan and promote disagree on scope', patches={'HELD': held})


def test_finding_already_filed_aborts():
    def mutate(crops, _d):
        crops['fig']['verification_status']['open_findings'].append(
            {'id': 'mid_south_fig_harvest_undocumented', 'status': 'open'})
    assert_aborts('already filed', mutate=mutate)


def test_catalog_id_already_minted_aborts():
    def mutate(_c, data):
        data['source_catalog']['ncsu_ext_toolbox_vicia_faba'] = {'id': 'x'}
    assert_aborts('already exists', mutate=mutate)


# --------------------------------------------------------------------------- post-edit guards

def test_repointing_a_held_case2_node_aborts():
    rep = dict(P.REPOINTS)
    rep[('fig', 'mid_south', 'regions.mid_south.plantings[0].harvest_start[0]')] = P.FRUIT_TREES
    assert_aborts('deliberate CASE 2 node', patches={'REPOINTS': rep})


def test_citing_the_uaex_hosted_ncsu_guide_aborts():
    """G3. Hosted by UAEX, authored by NC State, calendared for North Carolina.

    Modelled on the REAL failure mode: a later pass finds the PDF on the UAEX server, mints it
    as a uada_ext sub-id, and repoints the z8 plasticulture container at it. The id is therefore
    catalogued and T1 here, so the earlier catalog guards pass and G3 is the one that must fire.
    """
    url = ('https://www.uaex.uada.edu/farm-ranch/crops-commercial-horticulture/docs/'
           'Guide%20to%20Strawberry%20Plasticulture.pdf')
    sid = 'uada_ext_plasticulture_guide'

    def mutate(_crops, data):
        # an earlier session admitted it to the catalog, which is how this would really happen
        data['source_catalog'][sid] = dict(P.CATALOG_ENTRY, id=sid, url=url)

    rep = dict(P.REPOINTS)
    rep[('strawberry', 'mid_south', 'regions.mid_south.plantings[1]')] = (sid, url)
    held = tuple(h for h in P.HELD
                 if h != ('strawberry', 'mid_south', 'regions.mid_south.plantings[1]'))
    assert_aborts('plasticulture guide is cited',
                  mutate=mutate, patches={'REPOINTS': rep, 'HELD': held})


def test_repoint_at_uncatalogued_id_aborts():
    rep = dict(P.REPOINTS)
    rep[('apple', 'mid_south', 'regions.mid_south.plantings[0]')] = (
        'uada_ext_not_admitted', P.FRUIT_TREES[1])
    assert_aborts('repoints at uncatalogued id', patches={'REPOINTS': rep})


def test_repoint_url_disagreeing_with_catalog_aborts():
    rep = dict(P.REPOINTS)
    rep[('apple', 'mid_south', 'regions.mid_south.plantings[0]')] = (
        'uada_ext_fruit_trees', 'https://www.uaex.uada.edu/yard-garden/fruits-nuts/berries.aspx')
    assert_aborts('disagrees with catalog id', patches={'REPOINTS': rep})


def test_repoint_at_non_t1_id_aborts():
    entry = dict(P.CATALOG_ENTRY)
    entry['tier'] = 'T2'
    assert_aborts('repoints at non-T1 id', patches={'CATALOG_ENTRY': entry})


def test_consumer_copy_change_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'fig':
                cell = c['regions']['mid_south']['resolved_by_zone']['7']
                cell['harvest'] = 'DOCTORED'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'consumer copy changed' in out, out


def test_heat_pause_prose_change_aborts():
    """G4 must reach NESTED prose too -- heat_pause.basis_seasoned is a dict member."""
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'broad-beans-fava':
                hp = c['regions']['mid_atlantic']['resolved_by_zone']['7']['heat_pause']
                hp['basis_seasoned'] = 'DOCTORED'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'consumer copy changed' in out, out


def test_em_dash_in_finding_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['summary'] += chr(8212) + ' UAEX.'
    assert_aborts('em dash in', patches={'FINDINGS': fs})


def test_finding_naming_no_institution_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['summary'] = 'The window is modeled and nobody publishes it.'
    assert_aborts('names no institution', patches={'FINDINGS': fs})


def test_finding_without_read_date_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['basis'] = 'Read at some point.'
    assert_aborts('carries no read date', patches={'FINDINGS': fs})


def test_touching_a_sixth_crop_aborts():
    fs = list(P.FINDINGS) + [('peach', {
        'id': 'zz_probe_peach', 'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': 'UAEX probe.', 'basis': 'read 2026-08-04', 'filed_in_session': 'probe'})]
    assert_aborts('crops changed', patches={'FINDINGS': fs})


def test_top_level_key_change_aborts():
    def doctor(before):
        before['total_crops'] = -1
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'top-level total_crops changed' in out, out


def test_untouched_region_change_aborts():
    """G7. fig is in this hunt for mid_south only; its mid_atlantic must not move."""
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'fig':
                c['regions']['mid_atlantic']['zone_span'] = ['9', '9']
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'region mid_atlantic changed and is not in this hunt' in out, out


def test_crop_level_key_change_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'elderberry':
                c['days_to_maturity'] = 1
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'crop-level keys changed' in out, out


def test_finding_count_mismatch_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'fig':
                c['verification_status']['open_findings'].append(
                    {'id': 'zz_phantom_in_before', 'status': 'open'})
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'gained' in out, out


def test_trailing_newline_on_write_aborts():
    real = json.dumps

    def shim(obj, **kw):
        return real(obj, **kw) + '\n'

    json.dumps = shim
    try:
        rc, out, _ = run(apply_=True)
    finally:
        json.dumps = real
    assert rc == 2, out
    assert 'trailing newline introduced' in out, out


TESTS = [v for k, v in sorted(globals().items()) if k.startswith('test_') and callable(v)]

if __name__ == '__main__':
    failed = 0
    for t in TESTS:
        try:
            t()
            print('PASS %s' % t.__name__)
        except AssertionError as e:
            failed += 1
            print('FAIL %s: %s' % (t.__name__, str(e)[:300]))
    print('\n%d/%d passed' % (len(TESTS) - failed, len(TESTS)))
    sys.exit(1 if failed else 0)
