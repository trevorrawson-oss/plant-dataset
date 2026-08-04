#!/usr/bin/env python3
"""Guard suite for tools/promote_mid_atlantic_ncsu_fruit_repoint.py.

NEVER SKIPS. The fixture is rebuilt from the pinned base SHA via promote_fixture.scratch, so this
suite keeps running after canonical moves on -- the failure mode that left six promote suites green
and vacuous (121 checks dark) on 2026-07-30.

Every check below was MUTATION-TESTED by deleting the guard it targets from the promote and
confirming this file goes red. Guards that could not be made to fail were removed from the promote
rather than kept as decoration.

Runs both ways, and both were verified:
    $ python3 -m pytest tools/test_promote_mid_atlantic_ncsu_fruit_repoint.py -q
    $ python3 tools/test_promote_mid_atlantic_ncsu_fruit_repoint.py
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                                          # noqa: E402
import promote_mid_atlantic_ncsu_fruit_repoint as P             # noqa: E402

BASE = P.BASE_SHA


def run(mutate=None, patches=None, apply_=False):
    """Run the promote against a rebuilt scratch pre-state. -> (exit_code, stdout)."""
    path, sha = promote_fixture.scratch(BASE, mutate)
    saved = {k: getattr(P, k) for k in (patches or {})}
    for k, v in (patches or {}).items():
        setattr(P, k, v)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', sha,
                '--apply' if apply_ else '--dry-run']
    import io
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


# --------------------------------------------------------------------------- the happy path

def test_clean_pre_state_passes():
    rc, out, _ = run()
    assert rc == 0, out
    assert '9 repoints agree with the catalog' in out
    assert '15 CASE 2 nodes still bare' in out
    assert '13 findings' in out


def test_apply_writes_compact_and_repoints():
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    raw = open(path, 'rb').read()
    assert not raw.endswith(b'\n'), 'trailing newline written'
    assert b'\n' not in raw, 'canonical is not compact'
    data = json.loads(raw)
    crops = {c['slug']: c for c in data['crops']}
    # the nine that moved
    for slug, key in [('apricot', P.ROOT), ('apricot', P.PLANT_OUT), ('apricot', P.ZONE8),
                      ('cherry-sour', P.ROOT), ('cherry-sour', P.PLANT_OUT),
                      ('cherry-sour', P.ZONE8),
                      ('cherry-sweet', P.ROOT), ('cherry-sweet', P.PLANT_OUT)]:
        assert P.nodes_of(crops[slug])[key]['sources'] == ['ncsu_ext_handbook_tree_fruit']
    assert (P.nodes_of(crops['pomegranate'])[P.ZONE8]['sources']
            == ['ncsu_ext_toolbox_punica_granatum'])
    # the fifteen that did not
    for slug in P.CROPS:
        for key in (P.BLOOM, P.H_START, P.H_END):
            assert P.cites_bare(P.nodes_of(crops[slug])[key]), '%s %s moved' % (slug, key)
    assert P.cites_bare(P.nodes_of(crops['cherry-sweet'])[P.ZONE8])
    assert P.cites_bare(P.nodes_of(crops['pomegranate'])[P.ROOT])
    assert P.cites_bare(P.nodes_of(crops['pomegranate'])[P.PLANT_OUT])
    assert 'ncsu_ext_toolbox_punica_granatum' in data['source_catalog']


def test_apply_is_idempotent_only_once():
    """Re-running against the already-promoted state must ABORT, not double-file."""
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    import hashlib
    raw = open(path, 'rb').read()
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path,
                '--expect-sha', hashlib.sha256(raw).hexdigest(), '--dry-run']
    import io
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc2 = P.main()
    finally:
        sys.stdout = real
        sys.argv = argv
    assert rc2 == 2
    assert 'premise changed' in buf.getvalue()


# --------------------------------------------------------------------------- preflight guards

def test_sha_drift_aborts():
    path, sha = promote_fixture.scratch(BASE)
    argv = sys.argv
    sys.argv = ['promote', '--canonical', path, '--expect-sha', 'f' * 64, '--dry-run']
    import io
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
        P.nodes_of(crops['apricot'])[P.PLANT_OUT]['sources'] = ['ncsu_ext_handbook_tree_fruit']
    assert_aborts('premise changed', mutate=mutate)


def test_bloom_node_already_moved_aborts():
    """A held node that someone else repointed also breaks the premise."""
    def mutate(crops, _d):
        n = P.nodes_of(crops['pomegranate'])[P.BLOOM]
        n['sources'] = ['ncsu_ext_toolbox_punica_granatum']
        n['anchoring_urls'] = {'ncsu_ext_toolbox_punica_granatum': {
            'url': P.TOOLBOX_POM[1], 'verified': '2026-08-03'}}
    assert_aborts('premise changed', mutate=mutate)


def test_second_bare_url_aborts():
    """Campaign A's pear lesson: a node whose bare URL is a DIFFERENT site is not in this hunt.

    Caught by the per-node URL pin, not by a set comparison across decisions -- that separate
    pass was removed from the promote as unfailable once this test showed preflight 1 reaching
    the defect first.
    """
    def mutate(crops, _d):
        n = P.nodes_of(crops['cherry-sweet'])[P.H_END]
        n['anchoring_urls']['ncsu_ext']['url'] = 'https://plants.ces.ncsu.edu'
    assert_aborts('no longer cites the bare host SOLE', mutate=mutate)


def test_finding_already_filed_aborts():
    def mutate(crops, _d):
        crops['apricot']['verification_status']['open_findings'].append(
            {'id': 'mid_atlantic_apricot_harvest_divergent', 'status': 'open'})
    assert_aborts('already filed', mutate=mutate)


def test_catalog_id_already_minted_aborts():
    def mutate(_c, data):
        data['source_catalog']['ncsu_ext_toolbox_punica_granatum'] = {'id': 'x'}
    assert_aborts('already exists', mutate=mutate)


# --------------------------------------------------------------------------- the post-edit guards

def test_repointing_a_held_case2_node_aborts():
    """G2. The 15 deliberate CASE 2 nodes are the hunt's output as much as the 9 repoints."""
    extra = dict(P.REPOINTS)
    extra[('apricot', P.H_START)] = P.HANDBOOK
    assert_aborts('deliberate CASE 2 node', patches={'REPOINTS': extra})


def test_node_in_neither_list_aborts():
    """The coverage assertion: a node in scope may not be silently forgotten."""
    short = tuple(h for h in P.HELD if h != ('pomegranate', P.BLOOM))
    assert_aborts('do not cover all 24 nodes', patches={'HELD': short})


def test_citing_handbook_for_pomegranate_aborts():
    """G3. ch. 15 never names pomegranate; citing it there is the vce_426_331 defect.

    Reached by ALSO dropping the node from HELD, so the CASE 2 data guard does not fire first.
    Both orderings were checked; each guard fails on its own injection.
    """
    extra = dict(P.REPOINTS)
    extra[('pomegranate', P.ROOT)] = P.HANDBOOK
    held = tuple(h for h in P.HELD if h != ('pomegranate', P.ROOT))
    assert_aborts('a document that never mentions the crop',
                  patches={'REPOINTS': extra, 'HELD': held})


def test_handbook_url_anywhere_on_pomegranate_aborts():
    """G3's second arm: the URL may not arrive via a finding either."""
    fs = list(P.FINDINGS) + [('pomegranate', {
        'id': 'zz_probe', 'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': 'NC State handbook %s covers this crop.' % P.HANDBOOK[1],
        'basis': 'read 2026-08-03', 'filed_in_session': 'probe'})]
    assert_aborts('references the handbook URL', patches={'FINDINGS': fs})


def test_consumer_copy_change_aborts():
    """G4. This promote is citations and findings only."""
    class Shim:
        """Doctor ONLY the first deepcopy -- the `before` snapshot -- so the diff sees a change
        the edit loop never made. Otherwise this guard is unreachable from data injection."""
        def __init__(self):
            self.n = 0
            self.real = copy.deepcopy

        def __call__(self, obj, *a, **k):
            out = self.real(obj, *a, **k)
            self.n += 1
            if self.n == 1:
                for c in out['crops']:
                    if c['slug'] == 'apricot':
                        cell = c['regions']['mid_atlantic']['resolved_by_zone']['8']
                        cell['suitability_note_beginner'] = 'DOCTORED'
            return out

    shim = Shim()
    saved = copy.deepcopy
    copy.deepcopy = shim
    try:
        rc, out, _ = run()
    finally:
        copy.deepcopy = saved
    assert rc == 2, out
    assert 'consumer copy changed' in out, out


def test_em_dash_in_finding_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['summary'] = fs[0][1]['summary'] + chr(8212) + ' NC State.'
    assert_aborts('em dash in', patches={'FINDINGS': fs})


def test_finding_naming_no_institution_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['summary'] = 'The window is modeled and nobody publishes it.'
    assert_aborts('names no institution', patches={'FINDINGS': fs})


def test_finding_without_read_date_aborts():
    fs = [(s, dict(f)) for s, f in P.FINDINGS]
    fs[0][1]['basis'] = 'NC State handbook, read at some point.'
    assert_aborts('carries no read date', patches={'FINDINGS': fs})


def test_zone7_change_aborts():
    """G6. Zone 7 cites vce_426_331 and is not in this hunt."""
    class Shim:
        def __init__(self):
            self.n = 0
            self.real = copy.deepcopy

        def __call__(self, obj, *a, **k):
            out = self.real(obj, *a, **k)
            self.n += 1
            if self.n == 1:
                for c in out['crops']:
                    if c['slug'] == 'cherry-sour':
                        # a NON-string zone-7 field, so this reaches G6 rather than being
                        # caught by the consumer-copy guard, which only scans string values
                        cell = c['regions']['mid_atlantic']['resolved_by_zone']['7']
                        cell['resolved_from'] = dict(cell['resolved_from'], last_frost='Apr 1')
            return out

    saved = copy.deepcopy
    copy.deepcopy = Shim()
    try:
        rc, out, _ = run()
    finally:
        copy.deepcopy = saved
    assert rc == 2, out
    assert 'zone 7 changed' in out, out


def test_touching_a_fifth_crop_aborts():
    """G7. Exact footprint."""
    fs = list(P.FINDINGS) + [('peach', {
        'id': 'zz_probe_peach', 'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': 'NC State probe.', 'basis': 'read 2026-08-03', 'filed_in_session': 'probe'})]
    assert_aborts('crops changed', patches={'FINDINGS': fs})


def test_modifying_an_existing_catalog_entry_aborts():
    entry = dict(P.CATALOG_ENTRY)
    entry['id'] = 'ncsu_ext'          # collide with the live parent instead of minting
    assert_aborts('already exists', patches={'CATALOG_ENTRY': entry})


def test_finding_count_mismatch_aborts():
    """G8. The per-crop tally must notice a filing that did not land as intended.

    Patching FINDINGS cannot test this: the guard derives its expectation from the same list, so
    the two move together and the check stays green. Doctoring the `before` snapshot instead
    makes the live-minus-before delta disagree with the intended count, which is the only way
    this guard is reachable.
    """
    class Shim:
        def __init__(self):
            self.n = 0
            self.real = copy.deepcopy

        def __call__(self, obj, *a, **k):
            out = self.real(obj, *a, **k)
            self.n += 1
            if self.n == 1:
                for c in out['crops']:
                    if c['slug'] == 'apricot':
                        c['verification_status']['open_findings'].append(
                            {'id': 'zz_phantom_in_before', 'status': 'open'})
            return out

    saved = copy.deepcopy
    copy.deepcopy = Shim()
    try:
        rc, out, _ = run()
    finally:
        copy.deepcopy = saved
    assert rc == 2, out
    assert 'gained' in out, out


def _doctor_before(fn):
    """Run the promote with the `before` snapshot doctored by fn(before_data).

    The first deepcopy in main() IS the before snapshot. Doctoring only that one simulates a
    difference the edit loop never made, which is the only way the footprint guards -- which
    compare before against after -- are reachable at all.
    """
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


def test_top_level_key_change_aborts():
    """G7. Anything outside crops/source_catalog moving is out of this promote's remit."""
    def doctor(before):
        before['total_crops'] = -1
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'top-level total_crops changed' in out, out


def test_other_region_change_aborts():
    """G8. This hunt is mid_atlantic only; a sibling region moving is a bug."""
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'apricot':
                c['regions']['mid_south']['zone_span'] = ['9', '9']
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'region mid_south changed' in out, out


def test_crop_level_key_change_aborts():
    """G8. Only verification_status may move at crop level."""
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'cherry-sweet':
                c['days_to_maturity'] = 1
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'crop-level keys changed' in out, out


def test_trailing_newline_on_write_aborts():
    """The COMPACT invariant. json.dumps never emits a trailing newline, so this guard is only
    reachable by shimming the serializer -- the technique the 2026-07-31 herb pass established."""
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


def test_repoint_url_disagreeing_with_catalog_aborts():
    """G1. The repoint table and the source catalog are authored separately and must agree."""
    bad = ('ncsu_ext_handbook_tree_fruit',
           'https://content.ces.ncsu.edu/extension-gardener-handbook/14-small-fruit')
    rep = {k: (bad if v[0] == bad[0] else v) for k, v in P.REPOINTS.items()}
    assert_aborts('disagrees with catalog id', patches={'REPOINTS': rep})


def test_repoint_at_uncatalogued_id_aborts():
    """G1. A repoint may not invent a source id the catalog has never admitted."""
    rep = dict(P.REPOINTS)
    rep[('pomegranate', P.ZONE8)] = ('ncsu_ext_toolbox_not_admitted', P.TOOLBOX_POM[1])
    assert_aborts('repoints at uncatalogued id', patches={'REPOINTS': rep})


def test_repoint_at_non_t1_id_aborts():
    """G1. `source_catalog` is the admission authority, and T2 here means SEED TRADE."""
    entry = dict(P.CATALOG_ENTRY)
    entry['tier'] = 'T2'
    assert_aborts('repoints at non-T1 id', patches={'CATALOG_ENTRY': entry})


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
