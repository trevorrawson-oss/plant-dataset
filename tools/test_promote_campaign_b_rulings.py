#!/usr/bin/env python3
"""Guard suite for tools/promote_campaign_b_rulings.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch.
Every check was MUTATION-TESTED by neutering the guard it targets and confirming this file goes
red. Guards that could not be made to fail were removed from the promote.

    $ python3 -m pytest tools/test_promote_campaign_b_rulings.py -q
    $ python3 tools/test_promote_campaign_b_rulings.py
"""
import copy
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                        # noqa: E402
import promote_campaign_b_rulings as P        # noqa: E402

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
    assert '8 finding records open and ready to rule' in out
    assert '0 banned claims remain' in out
    assert 'no suitability, date, calendar or citation moved anywhere' in out


def test_apply_removes_the_banned_claims_and_keeps_the_facts():
    rc, out, path = run(apply_=True)
    assert rc == 0, out
    raw = open(path, 'rb').read()
    assert not raw.endswith(b'\n') and b'\n' not in raw
    crops = {c['slug']: c for c in json.loads(raw)['crops']}

    cs = P.cell_of(crops, 'cherry-sweet', 'mid_atlantic', '8')
    for reg in ('suitability_note_seasoned', 'suitability_note_beginner'):
        assert 'zone 8 growers toward' not in cs[reg]
        assert 'NC State' in cs[reg], 'the true NC State claims were dropped too'
        assert 'self fertile' in cs[reg]

    sb = P.cell_of(crops, 'strawberry', 'mid_south', '8')
    assert 'the University of Arkansas recommends' not in sb['grown_as_note_seasoned']
    assert 'plasticulture' in sb['grown_as_note_seasoned']
    assert '15 to 35 percent' in sb['grown_as_note_seasoned']
    assert 'still give you berries' in sb['grown_as_note_beginner']

    ap = P.cell_of(crops, 'apricot', 'mid_atlantic', '8')
    assert 'Pender County' in ap['suitability_note_seasoned']
    assert 'Pender County' in ap['suitability_note_beginner']


def test_apply_leaves_every_datum_alone():
    """The whole ruling turned on RETAINING the values, so this is the load-bearing assertion."""
    _rc, _out, path = run(apply_=True)
    after = {c['slug']: c for c in json.loads(open(path, 'rb').read())['crops']}
    base = {c['slug']: c for c in json.loads(promote_fixture.pre_state(BASE))['crops']}
    for slug in P.CROPS:
        for reg, r in (base[slug].get('regions') or {}).items():
            for z, bcell in ((r or {}).get('resolved_by_zone') or {}).items():
                acell = after[slug]['regions'][reg]['resolved_by_zone'][z]
                for k in ('suitability', 'plant_out', 'bloom', 'harvest', 'calendar',
                          'sources', 'anchoring_urls'):
                    assert bcell.get(k) == acell.get(k), '%s %s z%s %s moved' % (slug, reg, z, k)
    assert (P.cell_of(after, 'strawberry', 'mid_south', '8')['plant_out']
            == 'Sep 15 - Oct 5'), 'the window was trimmed; Trevor ruled to keep it'
    assert P.cell_of(after, 'apricot', 'mid_atlantic', '8')['suitability'] == 'marginal'


def test_rerun_aborts():
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
    assert rc == 2 and 'not open' in buf.getvalue()


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


def test_ruling_naming_a_missing_finding_aborts():
    r = dict(P.RULINGS)
    r['zz_no_such_finding'] = ('apricot', 'resolved', 'RULED 2026-08-04: probe.')
    assert_aborts('no crop carries it', patches={'RULINGS': r})


def test_ruling_on_a_finding_already_closed_aborts():
    def mutate(crops, _d):
        for f in P.findings_of(crops['apricot']):
            if f.get('id') == 'mid_atlantic_apricot_harvest_divergent':
                f['status'] = 'accepted_modeled'
    assert_aborts('not open', mutate=mutate)


def test_ruling_on_the_wrong_crop_aborts():
    r = dict(P.RULINGS)
    fid = 'mid_atlantic_apricot_harvest_divergent'
    r[fid] = ('pomegranate',) + r[fid][1:]
    assert_aborts('expected on pomegranate', patches={'RULINGS': r})


def test_plasticulture_tension_already_closed_aborts():
    def mutate(crops, _d):
        for f in P.findings_of(crops['strawberry']):
            if f.get('id') == 'strawberry_mid_south_plasticulture_home_garden_tension':
                f['status'] = 'resolved'
    assert_aborts('its premise changed', mutate=mutate)


def test_new_finding_already_filed_aborts():
    def mutate(crops, _d):
        P.findings_of(crops['strawberry']).append(
            {'id': 'mid_south_strawberry_grown_as_note_uaex_credit_removed', 'status': 'open'})
    assert_aborts('already filed', mutate=mutate)


def test_expected_text_missing_aborts():
    def mutate(crops, _d):
        cell = P.cell_of(crops, 'apricot', 'mid_atlantic', '8')
        cell['suitability_note_beginner'] = 'Rewritten by someone else.'
    assert_aborts('does not contain the expected text exactly once', mutate=mutate)


# --------------------------------------------------------------------------- post-edit guards

def test_banned_claim_surviving_elsewhere_aborts():
    """G1. The claim must be gone from EVERY cell, not just the one we edited."""
    def mutate(crops, _d):
        cell = P.cell_of(crops, 'cherry-sweet', 'mid_atlantic', '7')
        cell['suitability_note_seasoned'] += (
            ' NC State Extension steers zone 8 growers toward sour cherry instead.')
    assert_aborts('still carries the banned claim', mutate=mutate)


def test_rewrite_that_drops_a_kept_fact_aborts():
    edits = [list(e) for e in P.EDITS]
    edits[0][5] = 'NC State says nothing useful here.'      # loses 'sour cherry'/'self fertile'
    assert_aborts('lost the fact', patches={'EDITS': [tuple(e) for e in edits]})


def test_em_dash_in_rewrite_aborts():
    # keeps both kept-facts tokens, so the earlier kept-facts check cannot fire first and mask
    # the guard under test -- the "an earlier check catches the sabotage" trap
    edits = [list(e) for e in P.EDITS]
    edits[0][5] = 'A sour cherry is self fertile ' + chr(8212) + ' one tree crops alone.'
    assert_aborts('em dash or', patches={'EDITS': [tuple(e) for e in edits]})


def test_double_space_in_rewrite_aborts():
    edits = [list(e) for e in P.EDITS]
    edits[0][5] = 'A sour cherry is  self fertile, so one tree crops alone.'
    assert_aborts('whitespace/punctuation artifact', patches={'EDITS': [tuple(e) for e in edits]})


def test_changing_a_datum_aborts():
    """G3. The ruling was to RETAIN the values; a promote that moves one must abort."""
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'strawberry':
                c['regions']['mid_south']['resolved_by_zone']['8']['plant_out'] = 'Sep 15 - Sep 30'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'this promote is prose only' in out, out


def test_changing_a_suitability_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'apricot':
                c['regions']['mid_atlantic']['resolved_by_zone']['8']['suitability'] = 'unsuitable'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'this promote is prose only' in out, out


def test_changing_plantings_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'fig':
                pass
            if c['slug'] == 'elderberry':
                c['regions']['mid_south']['plantings'][0]['label'] = 'doctored'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'plantings changed' in out, out


def test_unintended_prose_move_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'pomegranate':
                c['regions']['mid_atlantic']['resolved_by_zone']['7'][
                    'suitability_note_beginner'] = 'DOCTORED'
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'prose moved' in out, out


def test_closing_the_plasticulture_tension_aborts():
    """G5. Trevor ruled to LEAVE IT OPEN."""
    r = dict(P.RULINGS)
    r['strawberry_mid_south_plasticulture_home_garden_tension'] = (
        'strawberry', 'resolved', 'RULED 2026-08-04: closed.')
    assert_aborts('ruled to leave it open', patches={'RULINGS': r})


def test_dropping_a_finding_aborts():
    def doctor(before):
        for c in before['crops']:
            if c['slug'] == 'pomegranate':
                c['verification_status']['open_findings'].append(
                    {'id': 'zz_phantom_in_before', 'status': 'open'})
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'reordered or dropped' in out, out


def test_resolution_without_a_date_aborts():
    r = dict(P.RULINGS)
    fid = 'mid_atlantic_apricot_harvest_divergent'
    r[fid] = r[fid][:2] + ('RULED: declare modeled, no date given.',)
    assert_aborts('carries no ruling date', patches={'RULINGS': r})


def test_top_level_key_change_aborts():
    """G7. Anything outside `crops` moving is outside this promote's remit."""
    def doctor(before):
        before['total_crops'] = -1
    rc, out, _ = _doctor_before(doctor)
    assert rc == 2, out
    assert 'top-level total_crops changed' in out, out


def test_touching_a_seventh_crop_aborts():
    edits = list(P.EDITS) + [
        ('peach', 'mid_atlantic', '8', 'suitability_note_beginner',
         'Peach', 'Peach tree', ('Peach',))]
    assert_aborts('crops changed', patches={'EDITS': edits})


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
