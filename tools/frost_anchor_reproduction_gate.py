#!/usr/bin/env python3
"""A resolved cell must not be derived from a DIFFERENT region's frost anchor (2026-08-03).

THE DEFECT THIS EXISTS FOR. `strawberry.regions.mid_south.resolved_by_zone.7` declared
`resolved_from.last_frost = "Apr 10"` -- the documented mid_south z7 anchor, UAEX FSA6001 Arkansas
Frost Zone D -- while all four of its resolved arms reproduced EXACTLY from `Apr 15`, which is
`mid_atlantic`'s z7 anchor:

    arm             stored            from Apr 10 (declared)   from Apr 15 (mid_atlantic)
    plant_out       Apr 1 - Apr 22    Mar 27 - Apr 17          Apr 1 - Apr 22    <-- matches
    bloom           Apr 29 - May 20   Apr 24 - May 15          Apr 29 - May 20   <-- matches
    harvest_start   May 27            May 22                   May 27            <-- matches
    harvest_end     Jun 24            Jun 19                   Jun 24            <-- matches

`mid_south` was built from the `mid_atlantic` template. The anchor FIELD was correctly updated to
Apr 10; the resolved date STRINGS were carried across from the template's arithmetic. Every
Mid-South zone 7 strawberry planting and harvest date was five days late, and it survived
certification with `gate_all` 121/121 green, because **every existing gate reads a cell's values
against each other or against a neighbouring zone -- none reads a value against the anchor the
cell itself declares.** It was found by accident while working an unrelated citation hunt, which
is the real argument for this gate: discovery by luck does not scale.

WHY THIS IS NOT THE OBVIOUS GATE. "Every resolved value must reproduce from its own anchor" was
MEASURED before being written, and it floods:

    no scope at all                                    1,300 cells
    scoped to a frost-anchored resolution_method         363 of 640 arm values

and the flood is not defects. `bell-pepper mid_atlantic z7` stores `Apr 20 - May 18` where the
arithmetic gives `Apr 19 - May 17` -- one day. Resolved windows are routinely authored to sensible
month boundaries rather than emitted by strict arithmetic, so exact reproduction is not the
contract and never was. Shipping 363 of those would repeat the 38-findings-1-real mistake.

THE THREE CLAUSES, each of which earns its place by removing a measured false-positive class:

  1. SCOPE by the cell's OWN `resolution_method`. Only cells that claim frost derivation are
     checked. This is what excludes `onion`'s six `table_13_2_month_resolution` cells, whose
     values are UC-table month boundaries (`Mar 1`, `Jun 1`) never meant to reproduce from an
     offset -- they were the ENTIRE false-positive cluster left after the first two filters.
  2. EXACT reproduction, zero tolerance, and the stored span must equal the arm's `window_days`.
     Rounding noise cannot reach the check.
  3. TWO OR MORE DISTINCT ARM TYPES agreeing on the SAME non-declared anchor. One arm off is
     authoring latitude; `plant_out` AND `bloom` AND both harvest arms independently landing on
     one foreign date is arithmetic, and arithmetic has a cause. Counting the same arm type twice
     across succession cycles does NOT count -- that was a false-positive class of its own (76
     hits, almost all `harvest_start,harvest_start` from multi-planting crops).

DELIBERATELY NOT REPORTED: a cell that fails to reproduce from its own anchor in only one arm, or
by a day or two. That is the 363, it is authored latitude, and narrowing the CHECK rather than the
SCOPE is what made this shippable.

Measured on canonical `78e5d8e3`: **0 violations / 1,113 cells in scope.** On the pre-fix state
`3b7dc544`: **1 violation** (strawberry, 4 arms). A regression guard, provably not vacuous.

NOT YET WIRED INTO `whole_crop_gate`. Standalone first, like `zone_order_gate` and
`region_prose_gate` were. HARD-FLIP TRIGGER: the next region built from an existing region's
template, or the next cross-region calendar pass -- either is the moment this class can recur.

    $ python3 tools/frost_anchor_reproduction_gate.py
    $ python3 tools/frost_anchor_reproduction_gate.py --verbose
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

# Only methods that CLAIM frost derivation. A cell resolved from a published table holds month
# boundaries by design and is none of this gate's business.
IN_SCOPE = frozenset({
    'frost_anchored_resolved',
    'frost_anchored_offset',
    'authored_frost_offset',
    'northern_tier_frost_resolution',
    'two_source_derived_frost_anchored',
})

ARMS = ('plant_out', 'bloom', 'harvest_start', 'harvest_end')
_YEAR = 2026
_DATE = re.compile(r'^[A-Z][a-z]{2} \d{1,2}$')


def _dt(s):
    s = (s or '').strip()
    if not _DATE.match(s):
        return None
    try:
        return datetime.datetime.strptime('%s %d' % (s, _YEAR), '%b %d %Y')
    except ValueError:
        return None


def _fmt(d):
    return d.strftime('%b %-d')


def _implied_anchor(cell, planting, arm, base):
    """The anchor that WOULD produce this stored value, or 'OK' if the declared one already does.

    None means "this arm says nothing" -- unparseable, absent, or a span that does not match the
    arm's own window_days (a hand-rounded window, which is not evidence of anything).
    """
    lst = planting.get(arm) or []
    if not lst or not isinstance(lst[0], dict):
        return None
    a = lst[0]
    if a.get('from') != 'last_frost' or a.get('offset_days') is None:
        return None
    stored = cell.get(arm)
    if not isinstance(stored, str) or not stored.strip():
        return None
    parts = [p.strip() for p in stored.split(' - ')]
    start = _dt(parts[0])
    if start is None:
        return None
    od, wd = a['offset_days'], a.get('window_days')
    if wd is not None and len(parts) == 2:
        end = _dt(parts[1])
        if end is None or (end - start).days != wd:
            return None
    if _fmt(base + datetime.timedelta(days=od)) == _fmt(start):
        return 'OK'
    return _fmt(start - datetime.timedelta(days=od))


def violations(data):
    """-> [(slug, region, zone, declared_anchor, implied_anchor, [arm, ...])]"""
    out = []
    for crop in data.get('crops') or []:
        for rkey, region in (crop.get('regions') or {}).items():
            if not isinstance(region, dict):
                continue
            for zone, cell in (region.get('resolved_by_zone') or {}).items():
                if not isinstance(cell, dict):
                    continue
                if cell.get('resolution_method') not in IN_SCOPE:
                    continue
                declared = (cell.get('resolved_from') or {}).get('last_frost')
                base = _dt(declared)
                if base is None:
                    continue
                # per DISTINCT arm type; an arm votes only if every planting agrees on one answer
                per = collections.defaultdict(set)
                for planting in (region.get('plantings') or []):
                    if not isinstance(planting, dict):
                        continue
                    for arm in ARMS:
                        got = _implied_anchor(cell, planting, arm, base)
                        if got is not None:
                            per[arm].add(got)
                votes = collections.Counter()
                for arm, vals in per.items():
                    if len(vals) == 1 and 'OK' not in vals:
                        votes[next(iter(vals))] += 1
                if not votes:
                    continue
                implied, n = votes.most_common(1)[0]
                if n >= 2:
                    arms = sorted(a for a, v in per.items() if v == {implied})
                    out.append((crop.get('slug'), rkey, zone, declared, implied, arms))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--verbose', action='store_true', help='also report the scope size')
    args = ap.parse_args()
    with open(args.canonical, encoding='utf-8') as fh:
        data = json.load(fh)

    scoped = sum(
        1
        for c in data.get('crops') or []
        for r in (c.get('regions') or {}).values() if isinstance(r, dict)
        for cell in (r.get('resolved_by_zone') or {}).values()
        if isinstance(cell, dict) and cell.get('resolution_method') in IN_SCOPE
    )
    v = violations(data)
    for slug, rkey, zone, declared, implied, arms in v:
        print('  %s %s z%s: declares last_frost %r but %d arms (%s) reproduce exactly from %r '
              '-- a different region\'s anchor'
              % (slug, rkey, zone, declared, len(arms), ', '.join(arms), implied))
    print('frost anchor reproduction gate: %d violation(s); %d cell(s) in scope of %d scanned'
          % (len(v), scoped, len(data.get('crops') or [])))
    if args.verbose and not v:
        print('  scope = resolution_method in %s' % sorted(IN_SCOPE))
    return 1 if v else 0


if __name__ == '__main__':
    sys.exit(main())
