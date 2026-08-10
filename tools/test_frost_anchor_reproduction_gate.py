#!/usr/bin/env python3
"""TDD suite for frost_anchor_reproduction_gate -- RED before GREEN, then adversarially injected.

THE DEFECT CLASS, and it is a real one caught on 2026-08-03. `strawberry.regions.mid_south.
resolved_by_zone.7` DECLARED `resolved_from.last_frost = "Apr 10"` (the documented mid_south
anchor) while all four of its resolved arms reproduced EXACTLY from `Apr 15` -- `mid_atlantic`'s
z7 anchor. mid_south was built from the mid_atlantic template: the anchor FIELD was updated and
the resolved date STRINGS were carried across. Every Mid-South zone 7 strawberry date was five
days late, and it survived certification with 121/121 green because nothing compared a resolved
value against the anchor the cell itself declares.

WHY THE OBVIOUS GATE IS NOT THE ONE BUILT. "Every resolved value must reproduce from its own
anchor" was MEASURED before being written, three times, and it floods:

    no scope at all                                       1,300 cells
    scoped to resolution_method == frost_anchored_*          363 of 640 arm values

and the flood is not defects. `bell-pepper mid_atlantic z7` stores `Apr 20 - May 18` where the
arithmetic gives `Apr 19 - May 17` -- ONE DAY. Resolved windows are routinely authored to sensible
boundaries rather than emitted by strict arithmetic, so exact reproduction is simply not the
contract. Reporting 363 of those would be [[gate-findings-must-be-read-not-counted]] all over
again.

WHAT IS ACTUALLY GATED is the narrow signature that distinguishes template inheritance from
authored rounding, and every clause earns its place:

  1. SCOPE to cells whose own `resolution_method` claims frost derivation. This single clause is
     what excludes `onion`'s six `table_13_2_month_resolution` cells, whose values are UC-table
     month boundaries (`Mar 1`, `Jun 1`) that were never meant to reproduce from a frost offset --
     they were the entire false-positive cluster in the first cut.
  2. EXACT reproduction, zero tolerance, and the stored span must equal the arm's `window_days`.
     Rounding noise cannot reach the check.
  3. TWO OR MORE DISTINCT ARM TYPES must agree on the SAME non-declared anchor. One arm off is
     authoring latitude; `plant_out` AND `bloom` AND both harvest arms independently landing on
     one foreign date is arithmetic, and arithmetic has a cause.

Measured on canonical `78e5d8e3`: **0 violations across 1,113 in-scope cells**, and **1 violation
on the pre-fix state `3b7dc544`** -- strawberry, 4 arms. So it is a REGRESSION guard that is
provably not vacuous.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, 'crops_data_final.json')

import promote_fixture  # noqa: E402
import frost_anchor_reproduction_gate as G  # noqa: E402
from frost_anchor_reproduction_gate import violations, IN_SCOPE  # noqa: E402

PRE_FIX_SHA = '3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1'

# IN_SCOPE is a RULE, not rows -- nothing in a fixture can scope it -- so the value the
# historical measurement was made with is FROZEN here, literally, next to the SHA (PLA-162).
# Measured 2026-08-10 before the freeze: dropping one method from the live set turned five
# tests red including the pinned one. The pinned test below measures with this frozen value;
# test_live_in_scope_matches_the_frozen_measurement is the unpinned tripwire that goes red --
# once, loudly -- if the live rule ever changes. The live `violations()` BODY cannot be frozen
# the same way; the pinned test's exact expected tuple is the guard on it, and a deliberate
# behavior change there is SUPPOSED to fail that test until re-ruled.
IN_SCOPE_AT_MEASUREMENT = frozenset({
    'frost_anchored_resolved',
    'frost_anchored_offset',
    'authored_frost_offset',
    'northern_tier_frost_resolution',
    'two_source_derived_frost_anchored',
})


def test_live_in_scope_matches_the_frozen_measurement():
    """The unpinned equality tripwire. A deliberate IN_SCOPE change fails THIS test, once and
    loudly, instead of silently re-scoping the historical measurement below -- update the
    frozen copy only with the change spelled out in the diff."""
    assert G.IN_SCOPE == IN_SCOPE_AT_MEASUREMENT


def canonical():
    with open(CANON, encoding='utf-8') as fh:
        return json.load(fh)


def cell_of(data, slug, region, zone):
    crop = next(c for c in data['crops'] if c['slug'] == slug)
    return crop['regions'][region], crop['regions'][region]['resolved_by_zone'][zone]


# ---------------------------------------------------------------- the real historical defect

def test_red_on_the_pre_fix_state():
    """RED: the gate must FIRE on the state that actually shipped the defect.

    Measured with IN_SCOPE frozen as of the measurement -- the pin protects the fixture but
    not the rule the gate applies at run time, and this is the historical claim."""
    pre = json.loads(promote_fixture.pre_state(PRE_FIX_SHA))
    with promote_fixture.tables_frozen(G, {'IN_SCOPE': IN_SCOPE_AT_MEASUREMENT}):
        v = violations(pre)
    assert len(v) == 1, v
    slug, region, zone, declared, implied, arms = v[0]
    assert (slug, region, zone) == ('strawberry', 'mid_south', '7')
    assert declared == 'Apr 10' and implied == 'Apr 15'
    assert set(arms) == {'plant_out', 'bloom', 'harvest_start', 'harvest_end'}


def test_green_on_current_canonical():
    """GREEN: clean today, so this is a regression guard rather than a backlog report."""
    assert violations(canonical()) == []


def test_scope_is_not_empty():
    """A gate whose scope is empty passes vacuously. Pin that the scope is real."""
    data = canonical()
    n = 0
    for c in data['crops']:
        for r in (c.get('regions') or {}).values():
            if not isinstance(r, dict):
                continue
            for cell in (r.get('resolved_by_zone') or {}).values():
                if isinstance(cell, dict) and cell.get('resolution_method') in IN_SCOPE:
                    n += 1
    assert n > 1000, n


# ---------------------------------------------------------------- adversarial injection

def _reanchor(region, cell, foreign, arms):
    """Rewrite `arms` in `cell` as if they had been derived from `foreign` -- the real defect."""
    import datetime
    base = datetime.datetime.strptime(foreign + ' 2026', '%b %d %Y')
    p = region['plantings'][0]
    for arm in arms:
        a = p[arm][0]
        od, wd = a['offset_days'], a.get('window_days')
        start = base + datetime.timedelta(days=od)
        if wd:
            end = base + datetime.timedelta(days=od + wd)
            cell[arm] = '%s - %s' % (start.strftime('%b %-d'), end.strftime('%b %-d'))
        else:
            cell[arm] = start.strftime('%b %-d')


def test_injected_template_inheritance_bounces():
    """Inject the defect into a SCRATCH COPY of a clean crop and confirm the gate catches it."""
    data = canonical()
    region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    _reanchor(region, cell, 'Apr 15', ['plant_out', 'bloom', 'harvest_start', 'harvest_end'])
    v = violations(data)
    assert len(v) == 1, v
    assert v[0][:3] == ('strawberry', 'mid_south', '7')
    assert v[0][4] == 'Apr 15'


def test_two_arms_is_enough_to_fire():
    data = canonical()
    region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    _reanchor(region, cell, 'Apr 15', ['harvest_start', 'harvest_end'])
    assert len(violations(data)) == 1


# ---------------------------------------------------------------- the false positives it must NOT fire on

def test_single_diverging_arm_does_not_fire():
    """ONE arm off is authoring latitude, not arithmetic. 363 such arms exist; none may report."""
    data = canonical()
    region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    _reanchor(region, cell, 'Apr 15', ['plant_out'])
    assert violations(data) == []


def test_rounded_window_does_not_fire():
    """A hand-rounded window whose span no longer matches window_days must be ignored."""
    data = canonical()
    _region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    cell['plant_out'] = 'Mar 1 - Mar 31'
    cell['bloom'] = 'Apr 1 - Apr 30'
    assert violations(data) == []


def test_out_of_scope_resolution_method_does_not_fire():
    """THE ONION CLAUSE. A table-resolved cell holds month boundaries by design."""
    data = canonical()
    region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    _reanchor(region, cell, 'Apr 15', ['plant_out', 'bloom', 'harvest_start', 'harvest_end'])
    assert len(violations(data)) == 1, 'precondition: the injection fires while in scope'
    cell['resolution_method'] = 'table_13_2_month_resolution'
    assert violations(data) == [], 'a table-resolved cell must be out of scope'


def test_real_onion_cells_are_silent():
    """The six onion cells that survived the first two filters must not report."""
    v = violations(canonical())
    assert not [x for x in v if x[0] == 'onion'], v


def test_missing_anchor_is_skipped_not_crashed():
    data = canonical()
    _region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    cell['resolved_from'] = {}
    assert violations(data) == []


def test_unparseable_dates_are_skipped_not_crashed():
    data = canonical()
    _region, cell = cell_of(data, 'strawberry', 'mid_south', '7')
    cell['harvest_start'] = 'whenever the soil warms'
    cell['plant_out'] = ''
    assert violations(data) == []


CHECKS = [v for k, v in sorted(globals().items()) if k.startswith('test_')]

if __name__ == '__main__':
    failed = 0
    for fn in CHECKS:
        try:
            fn()
            print('  ok   %s' % fn.__name__)
        except AssertionError as e:
            failed += 1
            print('  FAIL %s\n       %s' % (fn.__name__, str(e)[:300]))
    print('\n%d/%d checks passed' % (len(CHECKS) - failed, len(CHECKS)))
    sys.exit(1 if failed else 0)
