#!/usr/bin/env python3
"""Guard suite for tools/promote_pla122_rulings.py.

NEVER SKIPS: the fixture is rebuilt from the pinned base SHA via promote_fixture.scratch.

This promote is the first in the campaign C sequence to MOVE CONSUMER-FACING STRINGS, so the
blanket "no prose moves" tripwire the earlier ones used is gone and its replacements carry the
weight: an enumerated before/after set (G2), the untouched-neighbours checks (G3, G4) and the
anchor arithmetic (G1). Each is mutation-tested, and each test asserts the SPECIFIC abort message
so an earlier guard firing cannot be mistaken for the one under test.
"""
import copy
import io
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture                       # noqa: E402
import promote_pla122_rulings as P           # noqa: E402


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
    assert '13 edits:' in out
    assert 'verified: exactly 5 crops and 7 resolved cells changed' in out


def test_sha_drift_aborts():
    path, _sha = promote_fixture.scratch(P.BASE_SHA)
    argv, buf, real = sys.argv, io.StringIO(), sys.stdout
    sys.argv = ['promote', '--canonical', path, '--expect-sha', '0' * 64, '--dry-run']
    sys.stdout = buf
    try:
        rc = P.main()
    finally:
        sys.stdout, sys.argv = real, argv
    assert rc == 2 and 'canonical drifted' in buf.getvalue()


# --------------------------------------------------------------------------------------------
# The premise checks.
# --------------------------------------------------------------------------------------------

def test_a_moved_pre_state_value_aborts():
    def mutate(crops, _d):
        crops['cantaloupe']['regions']['low_desert_az']['resolved_by_zone']['9']['plant_out'] = \
            'Feb 5 - Mar 15'
    assert_aborts('expected \'Feb 1 - Mar 15\'', mutate=mutate)


def test_turnip_losing_its_already_correct_data_aborts_the_display_claim():
    """The whole justification for touching turnip is that the sourced window is ALREADY stored.
    If it were not, this would be a data change and would need different evidence."""
    def mutate(crops, _d):
        crops['turnip']['regions']['ca_south_coast']['resolved_by_zone']['9']['last_plant_date'] \
            = 'Oct 31'
    assert_aborts('the premise that the sourced window is already in the data does not hold',
                  mutate=mutate)


def test_a_finding_already_ruled_aborts():
    def mutate(crops, _d):
        for f in crops['lavender']['verification_status']['open_findings']:
            if f.get('id') == 'warm_arid_lavender_plant_out_window_is_unsourced':
                f['status'] = 'accepted'
    assert_aborts("not open -- already ruled?", mutate=mutate)


def test_a_missing_finding_aborts():
    def mutate(crops, _d):
        vs = crops['garlic']['verification_status']
        vs['open_findings'] = [f for f in vs['open_findings']
                               if f.get('id') != 'rgv_garlic_harvest_start_runs_ahead_of_every_source']
    assert_aborts('carries 0 findings with id', mutate=mutate)


# --------------------------------------------------------------------------------------------
# G1 -- the anchor arithmetic. This is the direct answer to PLA-122's precompute worry.
# --------------------------------------------------------------------------------------------

def test_the_new_start_agrees_with_the_cells_own_frost_anchor(data=None):
    """Feb 15 is within a day of last_frost (Jan 31) + the arm's 14-day offset = Feb 14. The
    PREVIOUS Feb 1 was 13 days out, which is why this guard could not have been written before."""
    rc, out, _ = run()
    assert rc == 0
    assert 'within 1 day of its own declared frost anchor' in out


def test_MUTATION_moving_the_frost_anchor_breaks_the_agreement(monkeypatch=None):
    def mutate(crops, _d):
        for z in ('9', '10'):
            crops['cantaloupe']['regions']['low_desert_az']['resolved_by_zone'][z][
                'resolved_from']['last_frost'] = 'Mar 1'
    assert_aborts('days from its own anchor arithmetic', mutate=mutate)


def test_MUTATION_a_different_target_date_breaks_the_agreement():
    """Proves the guard constrains the VALUE being written, not just the anchor."""
    bad = copy.deepcopy(P.DATE_EDITS)
    for z in ('9', '10'):
        bad[('cantaloupe', 'low_desert_az', z)] = {
            'plant_out': ('Feb 1 - Mar 15', 'Mar 10 - Mar 15'),
            'first_plant_date': ('Feb 1', 'Mar 10'),
        }
    assert_aborts('days from its own anchor arithmetic', patches={'DATE_EDITS': bad})


# --------------------------------------------------------------------------------------------
# G2/G3/G4 -- blast radius, which replaces the old blanket prose tripwire.
# --------------------------------------------------------------------------------------------

def test_g2_catches_a_row_that_declares_a_change_it_does_not_make():
    """G2 asserts set-EQUALITY between what a DATE_EDITS row declares and what actually moved.
    Neutering it left every other test green, so it needs a sabotage that reaches it: a row
    claiming to change `harvest` to the value it already holds. Nothing moves, so the declared
    set and the moved set diverge and G2 must fire. Without this the guard would be decoration."""
    bad = copy.deepcopy(P.DATE_EDITS)
    bad[('turnip', 'ca_south_coast', '9')] = {
        'plant_out': ('Sep - Oct', 'Sep - May'),
        'harvest': ('Nov - May', 'Nov - May'),        # a no-op the row still declares
    }
    assert_aborts("moved ['plant_out'], expected exactly ['harvest', 'plant_out']",
                  patches={'DATE_EDITS': bad})


def test_g3_catches_a_melon_harvest_arm_drifting():
    """Trevor's ruling keeps the melons' late ends and watermelon's summer planting untouched.
    G3 is the only guard covering that, and it too survived neutering, so this drives a real
    harvest edit through the promote and asserts G3's own message."""
    bad = copy.deepcopy(P.DATE_EDITS)
    bad[('watermelon', 'low_desert_az', '9')] = dict(
        bad[('watermelon', 'low_desert_az', '9')],
        harvest=('May 1 - Jun 30', 'May 1 - Jul 15'))
    assert_aborts('watermelon z9 harvest changed and must not have',
                  patches={'DATE_EDITS': bad})


def test_g7_catches_a_crop_changing_that_is_not_in_the_declared_footprint():
    """The footprint check also survived neutering. Shrinking CROPS makes the five crops the
    promote really touches disagree with what it claims to touch."""
    assert_aborts('crops changed =',
                  patches={'CROPS': ('cantaloupe', 'garlic', 'lavender', 'turnip')})


def test_MUTATION_moving_turnips_data_fields_aborts():
    """If a later edit turned the display reconciliation into a data change, G4 catches it."""
    bad = copy.deepcopy(P.DATE_EDITS)
    bad[('turnip', 'ca_south_coast', '9')] = {
        'plant_out': ('Sep - Oct', 'Sep - May'),
        'last_plant_date': ('May 31', 'Apr 30'),
    }
    assert_aborts('this was meant to be display only', patches={'DATE_EDITS': bad})


# --------------------------------------------------------------------------------------------
# G5/G6 -- the rulings themselves.
# --------------------------------------------------------------------------------------------

def test_MUTATION_a_ruling_without_its_date_aborts():
    bad = dict(P.RULINGS)
    k = ('lavender', 'warm_arid_lavender_plant_out_window_is_unsourced')
    bad[k] = ('accepted', 'Declared modeled, no date given.')
    assert_aborts('resolution carries no ruling date', patches={'RULINGS': bad})


def test_MUTATION_an_em_dash_in_a_ruling_aborts():
    bad = dict(P.RULINGS)
    k = ('turnip', 'ca_south_coast_turnip_source_supports_a_wider_window_than_we_publish')
    st, res = bad[k]
    bad[k] = (st, res + ' ' + chr(8212))
    assert_aborts('em dash in', patches={'RULINGS': bad})


def test_g6_permitted_set_is_hand_written_and_load_bearing():
    """G6 must be able to catch a status change outside the ruling set. Its permitted set was
    first computed as `{fid for _s, fid in RULINGS}`, which made it incapable of firing, since
    every change the promote makes comes from RULINGS. It is now the hand-written RULED_IDS,
    checked against RULINGS first, so dropping an entry is caught in one direction..."""
    short = tuple(x for x in P.RULED_IDS
                  if x != 'warm_arid_lavender_plant_out_window_is_unsourced')
    assert_aborts('RULED_IDS disagrees with RULINGS', patches={'RULED_IDS': short})


def test_g6_catches_a_status_change_outside_the_ruling_set():
    """...and adding a phantom entry is caught in the other, which together prove the set is a
    real constraint rather than a restatement of the edit table."""
    extra = P.RULED_IDS + ('some_finding_this_promote_does_not_touch',)
    assert_aborts('RULED_IDS disagrees with RULINGS', patches={'RULED_IDS': extra})


def test_MUTATION_an_unexpected_crop_in_the_footprint_aborts():
    bad = dict(P.CELLS_CHANGED_PER_CROP)
    bad['cantaloupe'] = 3
    assert_aborts('CELLS_CHANGED_PER_CROP[cantaloupe] = 3 but DATE_EDITS holds 2',
                  patches={'CELLS_CHANGED_PER_CROP': bad})


def test_garlic_provenance_is_not_filed_twice():
    def mutate(crops, _d):
        crops['garlic']['regions']['rgv']['plantings_provenance'] = {'model': 'x'}
    assert_aborts('already carries plantings_provenance', mutate=mutate)


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


def test_applied_stays_compact(applied):
    raw, _ = applied
    assert not raw.endswith(b'\n')


def test_applied_dates_landed(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    for slug in ('cantaloupe', 'watermelon'):
        for z in ('9', '10'):
            cell = crops[slug]['regions']['low_desert_az']['resolved_by_zone'][z]
            assert cell['plant_out'] == 'Feb 15 - Mar 15'
            assert cell['first_plant_date'] == 'Feb 15'
            assert cell['last_plant_date'] == 'Mar 15'
            # the ruling KEEPS these
            assert cell['second_planting']['plant_out'] == 'Jul 15 - Aug 15'
    for z in ('9', '10', '11'):
        cell = crops['turnip']['regions']['ca_south_coast']['resolved_by_zone'][z]
        assert cell['plant_out'] == 'Sep - May'
        assert cell['first_plant_date'] == 'Sep 1'
        assert cell['last_plant_date'] == 'May 31'


def test_applied_rulings_landed(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    for (slug, fid), (status, _res) in P.RULINGS.items():
        f = [x for x in crops[slug]['verification_status']['open_findings']
             if x.get('id') == fid][0]
        assert f['status'] == status, (slug, fid)
        assert f['resolved_in_session'] == P.SESSION
        assert 'RULED 2026-08-05' in f['resolution']


def test_applied_garlic_declares_harvest_modeled(applied):
    _raw, data = applied
    crops = {c['slug']: c for c in data['crops']}
    pp = crops['garlic']['regions']['rgv']['plantings_provenance']
    assert sorted(pp) == ['basis', 'model', 'supersedes']
    assert 'MODELED' in pp['basis']
    # the date itself must NOT have moved
    for z in ('9', '10'):
        assert crops['garlic']['regions']['rgv']['resolved_by_zone'][z]['harvest_start'] == 'Apr 13'


def test_applied_leaves_no_open_findings_from_campaign_c(applied):
    """The point of PLA-122: after these rulings, campaign C carries no open findings."""
    _raw, data = applied
    S = {'campaign_c_closeout_2026_08_05', 'az1005_and_divergence_2026_08_05'}
    still = [(c['slug'], f['id']) for c in data['crops']
             for f in ((c.get('verification_status') or {}).get('open_findings') or [])
             if isinstance(f, dict) and f.get('filed_in_session') in S
             and f.get('status') == 'open']
    assert still == [], still
