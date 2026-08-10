#!/usr/bin/env python3
"""Tests for promote_fixture.tables_as_of / as_of -- the table-scoping helper (PLA-162).

THE DEFECT CLASS THIS EXISTS FOR: a pinned suite freezes its FIXTURE but evaluates it through a
live analysis module whose adjudication tables are read at run time. Extending a table for a
later campaign then flips historical assertions red over a fixture that never moved -- measured
on `test_campaign_d_reprice` (one phantom MODELED_FINDING row, one red test, 2026-08-10).

The helper rebinds named tables to their state AS OF the pinned SHA: a row whose finding is not
on its crop in `pre_state(sha)` was not in the table at that state, so it is dropped for the
suite's duration and restored on teardown.

THE KEPT-COUNT IS LOAD-BEARING, not decoration. Without it the filter is a vacuity generator:
a resolver bug that filtered every row would turn every downstream presence loop into a green
no-op. The pinned state never changes (pre_state is hash-verified), so the kept count is a true
constant, stable under live growth -- live rows added later are exactly what SHOULD be dropped.

Uses campaign_d_reprice as the guinea pig because its tables carry all three key shapes
(slug / (region, slug) / (region, slug, source_id)). Every injection is undone in finally --
this suite never leaves a phantom row behind for another suite in the same process.
"""
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import campaign_d_reprice as R  # noqa: E402
import promote_fixture  # noqa: E402

# The state test_campaign_d_reprice pins. As of it: MODELED_FINDING had 4 rows, SCOPED_OPEN 2.
BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'

PHANTOM = 'phantom_finding_that_exists_nowhere'


def test_a_row_added_after_the_pin_is_dropped_and_restored():
    """The core behavior: a live-table row whose finding is absent from the pinned state is
    invisible inside the scope, and back untouched after it."""
    R.MODELED_FINDING['lemon'] = PHANTOM
    try:
        with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 4}):
            assert 'lemon' not in R.MODELED_FINDING
            assert len(R.MODELED_FINDING) == 4
            assert R.MODELED_FINDING['lime'] == 'lime_pilot_finding_001'
        assert R.MODELED_FINDING['lemon'] == PHANTOM, 'teardown must restore the full table'
    finally:
        del R.MODELED_FINDING['lemon']


def test_restore_happens_even_when_the_body_raises():
    R.MODELED_FINDING['lemon'] = PHANTOM
    try:
        with pytest.raises(RuntimeError):
            with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 4}):
                raise RuntimeError('a failing test mid-suite')
        assert R.MODELED_FINDING['lemon'] == PHANTOM
    finally:
        del R.MODELED_FINDING['lemon']


def test_all_three_key_shapes_resolve_their_crop():
    """slug alone, (region, slug), and (region, slug, source_id) -- the shapes the reprice
    tables actually use.

    ANCHOR_FINDING expects 4, not its live 19: the PLA-114 close filed 15 rows whose findings
    postdate `6b2dcb8e`, and dropping exactly those is the behavior under test -- it is the same
    set the D suite's original `_table_as_of_the_pinned_state` fixture filtered."""
    with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 4,
                                                    'SCOPED_OPEN': 2,
                                                    'ANCHOR_FINDING': 4}):
        assert set(R.SCOPED_OPEN) == {('ca_north_coast', 'pear-asian'),
                                      ('ca_north_coast', 'pear-european')}
        # the survivors are the pre-PLA-114 rows; every lemon/lime row postdates the pin
        assert not any(slug in ('lemon', 'lime') for _r, slug, _s in R.ANCHOR_FINDING)


def test_a_row_for_a_crop_absent_from_the_pinned_state_is_dropped():
    """The ghost-crop shape: no key element resolves to a crop in the fixture. That row cannot
    have been in the table at the pinned state, so it is filtered, not an error."""
    R.SCOPED_OPEN[('rgv', 'ghost-crop')] = PHANTOM
    try:
        with promote_fixture.tables_as_of(BASE_SHA, R, {'SCOPED_OPEN': 2}):
            assert ('rgv', 'ghost-crop') not in R.SCOPED_OPEN
    finally:
        del R.SCOPED_OPEN[('rgv', 'ghost-crop')]


def test_kept_count_too_low_fails_loudly_naming_the_table():
    """Expecting 5 kept when the pinned state supports 4 means a row the suite depends on got
    filtered -- the exact silent-shrink the count exists to catch."""
    with pytest.raises(AssertionError, match='MODELED_FINDING'):
        with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 5}):
            pass


def test_kept_count_too_high_fails_loudly():
    """Expecting 3 kept when 4 survive means a post-pin row escaped the filter."""
    with pytest.raises(AssertionError, match='MODELED_FINDING'):
        with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 3}):
            pass


def test_a_failed_expectation_restores_every_table_it_touched():
    """MODELED_FINDING binds before SCOPED_OPEN's bad expectation raises; the raise must not
    leave the module half-filtered."""
    R.MODELED_FINDING['lemon'] = PHANTOM
    try:
        with pytest.raises(AssertionError):
            with promote_fixture.tables_as_of(
                    BASE_SHA, R, {'MODELED_FINDING': 4, 'SCOPED_OPEN': 99}):
                pass
        assert R.MODELED_FINDING['lemon'] == PHANTOM
    finally:
        del R.MODELED_FINDING['lemon']


def test_an_ambiguous_key_is_an_error_not_a_guess():
    """A key tuple where two elements are both real crop slugs cannot be resolved -- guessing
    would silently key the presence check to the wrong crop."""
    R.SCOPED_OPEN[('lemon', 'lime')] = 'lime_pilot_finding_001'
    try:
        with pytest.raises(AssertionError, match='ambiguous'):
            with promote_fixture.tables_as_of(BASE_SHA, R, {'SCOPED_OPEN': 3}):
                pass
    finally:
        del R.SCOPED_OPEN[('lemon', 'lime')]


def test_the_scope_yields_the_full_tables_for_live_presence_checks():
    """A suite's live-canonical presence test runs INSIDE the autouse scope, so it must reach
    the unfiltered table through the yielded value -- iterating the filtered module attribute
    would let every post-pin row escape the live check."""
    R.MODELED_FINDING['lemon'] = PHANTOM
    try:
        with promote_fixture.tables_as_of(BASE_SHA, R, {'MODELED_FINDING': 4}) as full:
            assert full['MODELED_FINDING']['lemon'] == PHANTOM
            assert 'lemon' not in R.MODELED_FINDING
    finally:
        del R.MODELED_FINDING['lemon']


def test_tables_frozen_rebinds_a_rule_table_and_yields_the_live_value():
    """Rule-tables (HUNTS, IN_SCOPE, RULES, BARE) have no keyed record to filter by, so they
    are frozen BY VALUE next to the SHA. The saved live value is yielded so the suite's
    unpinned equality test can compare live against frozen without tautology."""
    live_hunts = R.OWN_HUNTS
    frozen_value = {('ca_north_coast', 'ucanr_marin_mg'): 16}
    with promote_fixture.tables_frozen(R, {'OWN_HUNTS': frozen_value}) as saved:
        assert R.OWN_HUNTS == frozen_value
        assert saved['OWN_HUNTS'] is live_hunts
    assert R.OWN_HUNTS is live_hunts, 'teardown must restore the live table'


def test_tables_frozen_restores_on_exception():
    live_hunts = R.OWN_HUNTS
    with pytest.raises(RuntimeError):
        with promote_fixture.tables_frozen(R, {'OWN_HUNTS': {}}):
            raise RuntimeError('a failing test mid-suite')
    assert R.OWN_HUNTS is live_hunts


def test_tables_frozen_refuses_a_name_the_module_does_not_define():
    """Freezing a misspelled name would pin nothing while reading as protection."""
    with pytest.raises(AttributeError, match='OWN_HUNTZ'):
        with promote_fixture.tables_frozen(R, {'OWN_HUNTZ': {}}):
            pass


def test_frozen_factory_returns_a_module_scoped_autouse_pytest_fixture():
    fx = promote_fixture.frozen(R, OWN_HUNTS={})
    marker = (getattr(fx, '_fixture_function_marker', None)
              or getattr(fx, '_pytestfixturefunction', None))
    assert marker is not None and marker.scope == 'module' and marker.autouse is True


def test_as_of_returns_a_module_scoped_autouse_pytest_fixture():
    """The factory form suites adopt: assignable at module level, collected by pytest."""
    fx = promote_fixture.as_of(BASE_SHA, R, MODELED_FINDING=4)
    # the marker attribute was renamed between pytest majors; accept either spelling
    marker = (getattr(fx, '_fixture_function_marker', None)
              or getattr(fx, '_pytestfixturefunction', None))
    assert marker is not None, 'as_of must return a real pytest fixture'
    assert marker.scope == 'module'
    assert marker.autouse is True
