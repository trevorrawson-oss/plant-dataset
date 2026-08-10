#!/usr/bin/env python3
"""SOIL-TEMPERATURE FLOOR: warm-soil crops scheduled to be direct-sown at or before frost.

Exit contract (PLA-160, 2026-08-10):
  1  UNRULED hit(s) -- the defect class, read each before acting
  3  soil_temp_floor_scan UNDETERMINED -- zero hits but >0 in-scope cells could not be
     evaluated (missing resolved_from.last_frost / unparseable start). A zero over a
     population the scan could not measure is NOT a green, and this exit is what keeps a
     gate_all flip from locking the blind spot in. Measured 2026-08-10: 131 of 547 old-scope
     cells were silently skipped this way, nearly all in the frost-free regions
     (hawaii_tropical, fl_peninsula, rgv).
  0  zero hits AND zero unevaluable cells -- the only honest green.
NOT flip-eligible while either count is non-zero. Adversarially tested in
tools/test_soil_temp_floor_scan.py.
Read docs/2026-07-29-citation-cleanup-sample-pass-outcome.md first.

THE CLAIM. Frost passing does not warm soil. Soil temperature lags the last-frost date by
weeks, so a crop that needs warm soil to germinate cannot be sown the day frost clears. Where
a crop's own `start_method` prose says so -- acorn squash: direct sow "once the soil is
reliably warm (at least 65 degrees F, ideally 70 degrees F, at 2 inches)" -- and the calendar
opens on the frost date anyway, the DATA CONTRADICTS ITS OWN COPY. That is the shape this
finds, and it is how the ca_desert z10/z11 cucurbits came to open on Jan 15 against a Jan 15
last frost (corrected 2026-07-29, tools/promote_ca_desert_soil_temp_floor.py).

THE NARROWING MATTERS -- this is the "narrow the CHECK, not its scope" lesson in action:
  - naive "resolved start != declared frost offset":        751 cells / 66 crops -- FLOODS.
    Almost all legitimate: mild-region fall/winter cycles compared against a spring arm, plus
    a large benign cluster where resolved windows snap to clean calendar dates (`Feb 1` for
    `Jan 31 + 14`) instead of exact arithmetic. NOT SHIPPED, and should not be.
  - + frost-tender and same-spring-cycle only:              114 cells -- still mostly snapping.
  - + germination_temp_f low >= 70 (needs warm soil):        53 cells -- but 27 are thyme /
    rosemary / lavender, whose germination temp governs INDOOR seed starting while their
    plant_out is a nursery-transplant date. False positives.
  - + propagule == 'seed' (actually direct-sown):            26 cells / 10 crops -- TIGHT.
    Every remaining hit is the same real class.

Requiring `propagule == 'seed'` is the load-bearing filter: it is what separates "this seed
must go into warm soil" from "this hardened nursery plant may go out after frost".

THE PREDICATE WAS CORRECTED 2026-08-10 (PLA-160). The original "needs warm soil" test was a
bare `germination_temp_f[0] >= 70`, which reads an OPTIMAL band's floor as a minimum
(germination-temp-is-optimal-not-minimum) and excluded all four corns and four beans
(germ floor 60, frost_effect 'killed') -- the exact protected class. The predicate is now
`frost_effect == 'killed' AND germination_temp_f[0] >= 60`: frost-tender is what makes
sowing at frost lethal, and the hardy annuals whose germ floor is also 60-65 (dill,
calendula, borage, sweet-alyssum -- frost_effect 'foliage_damaged') legitimately open
before frost and stay out of scope. Measured on 060b91b8: the correction surfaces 42 new
UNRULED lead cells across the 8 corn/bean crops (utah_dixie z8 explicit-date candidates,
ca_desert bean cells matching the corrected 2026-07-29 cucurbit shape, northern_tier beans
opening ON frost, mid_atlantic/mid_south corn opening days before frost). Those are LEADS:
read each before acting; a sourced explicit local date belongs in RULED, a real defect in
the corrections log. Do not loosen the predicate to make them disappear.

RULED EXCEPTIONS -- the class that keeps this from ever reaching zero, and should not.
An extension table that publishes an EXPLICIT LOCAL DATE may legitimately place it before the
mean last frost, and CLAUDE.md is explicit that "explicit source dates govern over arithmetic".
The 6 utah_dixie z8 cucurbit cells are exactly that, and the region note already said so
before this scan existed:

    "Direct-sow around March 15, the Group C (Tender) date for St. George, about two weeks
     ahead of the March 30 average last frost; the table's explicit local date runs earlier
     than a generic frost-relative rule would."
     -- USU Extension, Suggested Vegetable Planting Dates for Utah

So they are RULED NOT A DEFECT (2026-07-29) and are annotated rather than reported as findings.
Adding to RULED below is a deliberate act: it records that a human read the cell and found a
sourced reason, which is why the reason string is required -- and the key is the CELL
(slug, region, zone), because a ruling covers exactly what was read (PLA-160: the old
(region, zone) key was earned by reading 6 cells and would have suppressed every future hit
in the zone, a suppression key coarser than its evidence).

HARD-FLIP CONDITION: wire this into tools/gate_all.py only when BOTH the unruled count and
the UNDETERMINED count reach 0, together with a test that injects the defect and confirms it
bounces. As of 2026-08-10 it is NOT flip-eligible (42 unruled leads, 100+ unevaluable cells).

    $ python3 tools/soil_temp_floor_scan.py
    $ python3 tools/soil_temp_floor_scan.py --stages   # show the narrowing, all four counts
    $ python3 tools/soil_temp_floor_scan.py --all      # include the ruled exceptions
"""
import argparse
import collections
import datetime
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')

MON = {m: i for i, m in enumerate(
    ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
) if m}
WARM_SOIL_F = 60          # germination_temp_f lower bound; paired with frost_effect 'killed'
SPRING_WINDOW_DAYS = 60   # keep the comparison inside one spring cycle

# (slug, region, zone) -> why an explicit sourced local date legitimately precedes last frost.
# A reason string is REQUIRED: this records that a human read THE CELL, not that it was muted.
_USU_GROUP_C = (
    "USU Extension 'Suggested Vegetable Planting Dates for Utah' publishes an explicit "
    "Group C (Tender) date of March 15 for St. George, ~2 weeks ahead of the Mar 30 mean "
    "last frost. The region note documents this. Explicit source dates govern over "
    "arithmetic (CLAUDE.md). Ruled 2026-07-29; the six cells read are enumerated here "
    "(PLA-160 narrowed the key to the cells the ruling actually read).")
RULED = {
    ('cucumber', 'utah_dixie', '8'): _USU_GROUP_C,
    ('slicing-cucumber', 'utah_dixie', '8'): _USU_GROUP_C,
    ('pickling-cucumber', 'utah_dixie', '8'): _USU_GROUP_C,
    ('english-cucumber', 'utah_dixie', '8'): _USU_GROUP_C,
    ('zucchini-courgette', 'utah_dixie', '8'): _USU_GROUP_C,
    ('yellow-summer-squash', 'utah_dixie', '8'): _USU_GROUP_C,
}


def parse(s):
    if not isinstance(s, str):
        return None
    p = s.replace(',', ' ').split()
    if len(p) < 2:
        return None
    mon = MON.get(p[0].rstrip('.')[:3])
    try:
        day = int(p[1])
    except (ValueError, IndexError):
        return None
    return datetime.date(2001, mon, day) if mon else None


def daydiff(a, b):
    d = (b - a).days
    if d > 182:
        d -= 365
    if d < -182:
        d += 365
    return d


def _in_scope_cells(data, require_seed=True, require_warm=True):
    """Yield (crop, g, rname, zone, node) for every cell the predicate covers.

    "Needs warm soil AND dies at frost" = frost_effect 'killed' + germination floor >= 60F.
    A bare germ-floor test reads an optimal band as a minimum and misses the corns/beans
    (germination-temp-is-optimal-not-minimum); a bare frost test floods with hardy annuals
    that legitimately open before frost.
    """
    for crop in data['crops']:
        g = crop.get('germination_temp_f')
        warm = (isinstance(g, list) and len(g) == 2
                and isinstance(g[0], (int, float)) and g[0] >= WARM_SOIL_F
                and crop.get('frost_effect') == 'killed')
        if require_warm and not warm:
            continue
        if require_seed and crop.get('propagule') != 'seed':
            continue
        for rname, region in (crop.get('regions') or {}).items():
            if not isinstance(region, dict):
                continue
            for zone, node in (region.get('resolved_by_zone') or {}).items():
                if not isinstance(node, dict) or node.get('start_indoors'):
                    continue
                yield crop, g, rname, zone, node


def scan(data, require_seed=True, require_warm=True):
    hits = []
    for crop, g, rname, zone, node in _in_scope_cells(data, require_seed, require_warm):
        lf = parse((node.get('resolved_from') or {}).get('last_frost'))
        st = parse(node.get('first_plant_date')
                   or (node.get('plant_out') or '').split(' - ')[0])
        if not lf or not st:
            continue
        delta = daydiff(lf, st)
        if -SPRING_WINDOW_DAYS < delta <= 0:
            hits.append((crop['slug'], g, rname, zone, delta,
                         node.get('plant_out'),
                         (node.get('resolved_from') or {}).get('last_frost')))
    return hits


def undetermined(data):
    """In-scope cells the scan CANNOT evaluate -- missing/unparseable last_frost or start.

    These are the cells a nulled `resolved_from.last_frost` would move a defect into (the
    escape-hatch shape). They are UNDETERMINED, never clean: a zero over them is not a green.
    """
    out = []
    for crop, g, rname, zone, node in _in_scope_cells(data):
        lf = parse((node.get('resolved_from') or {}).get('last_frost'))
        st = parse(node.get('first_plant_date')
                   or (node.get('plant_out') or '').split(' - ')[0])
        if lf and st:
            continue
        missing = ('last_frost+start' if not lf and not st
                   else 'last_frost' if not lf else 'start')
        out.append((crop['slug'], g, rname, zone, missing))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stages', action='store_true', help='show the narrowing counts')
    ap.add_argument('--all', action='store_true',
                    help='include cells covered by a RULED sourced exception')
    ap.add_argument('candidate', nargs='?', default=CANON)
    args = ap.parse_args()

    with open(args.candidate, encoding='utf-8') as fh:
        data = json.load(fh)

    if args.stages:
        print('narrowing (each filter is additive):')
        print('  warm-soil only, incl. transplants : %3d cells' % len(
            scan(data, require_seed=False)))
        print('  + propagule == seed (direct-sown) : %3d cells' % len(scan(data)))
        print('  - RULED sourced exceptions        : %3d cells   <- the shipped check' % len(
            [h for h in scan(data) if (h[0], h[2], h[3]) not in RULED]))
        print()

    allhits = scan(data)
    ruled = [h for h in allhits if (h[0], h[2], h[3]) in RULED]
    hits = allhits if args.all else [h for h in allhits if (h[0], h[2], h[3]) not in RULED]
    unev = undetermined(data)
    print('frost-killed warm-soil (germination_temp_f low >= %dF) direct-sown crops opening '
          'AT OR BEFORE last frost' % WARM_SOIL_F)
    print('=' * 100)
    if not hits:
        print('  none')
    else:
        print('%-22s %-11s %-15s %-3s %6s  %-20s %s' % (
            'crop', 'germ_temp', 'region', 'z', 'delta', 'plant_out', 'last_frost'))
        print('-' * 100)
        for h in sorted(hits, key=lambda h: (h[4], h[2], h[0])):
            print('%-22s %-11s %-15s %-3s %6d  %-20s %s' % (
                h[0], str(h[1]), h[2], h[3], h[4], (h[5] or '')[:20], h[6]))
    print('-' * 100)
    print('TOTAL: %d cells / %d crops / regions %s' % (
        len(hits), len({h[0] for h in hits}),
        dict(collections.Counter(h[2] for h in hits))))
    print()
    print('delta 0  = sown ON the mean last-frost date. delta < 0 = sown BEFORE it.')
    if ruled:
        print()
        print('RULED SOURCED EXCEPTIONS (%d cell(s), not counted above; --all to list):' % len(ruled))
        for key in sorted({(h[0], h[2], h[3]) for h in ruled}):
            print('  %s / %s z%s: %s' % (key[0], key[1], key[2], RULED[key][:80] + '...'))
    print()
    print('UNDETERMINED: %d in-scope cells could NOT be evaluated (never counted as clean):'
          % len(unev))
    if unev:
        by_reason = collections.Counter('%s missing %s' % (u[2], u[4]) for u in unev)
        for reason, n in sorted(by_reason.items()):
            print('  %4d  %s' % (n, reason))
    print()
    print('Read every hit before acting -- an explicit sourced local date may legitimately')
    print('precede last frost; that belongs in RULED with its reason, not in a "fix".')
    if hits:
        return 1
    if unev:
        print()
        print('soil_temp_floor_scan UNDETERMINED: 0 hits, but %d in-scope cells were not '
              'evaluable (missing resolved_from.last_frost or unparseable start). A zero '
              'over an unmeasured population is not a green. Exit 3.' % len(unev))
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
