#!/usr/bin/env python3
"""SOIL-TEMPERATURE FLOOR: warm-soil crops scheduled to be direct-sown at or before frost.

HARD, as of 2026-07-29: exits 1 on any UNRULED hit, and the roster is currently at 0. Belongs in
the release gauntlet alongside calendar_coherence_gate / numeric_sanity_gate (it is roster-wide,
so it is NOT a whole_crop_gate A-number and gate_all does not reach it -- gate_all only loops
whole_crop_gate per crop). Adversarially tested in tools/test_soil_temp_floor_scan.py.
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

RULED EXCEPTIONS -- the class that keeps this from ever reaching zero, and should not.
An extension table that publishes an EXPLICIT LOCAL DATE may legitimately place it before the
mean last frost, and CLAUDE.md is explicit that "explicit source dates govern over arithmetic".
The 6 utah_dixie z8 cells are exactly that, and the region note already said so before this
scan existed:

    "Direct-sow around March 15, the Group C (Tender) date for St. George, about two weeks
     ahead of the March 30 average last frost; the table's explicit local date runs earlier
     than a generic frost-relative rule would."
     -- USU Extension, Suggested Vegetable Planting Dates for Utah

So they are RULED NOT A DEFECT (2026-07-29) and are annotated rather than reported as findings.
Adding to RULED below is a deliberate act: it records that a human read the cell and found a
sourced reason, which is why the reason string is required.

HARD-FLIP CONDITION: wire this into tools/gate_all.py when the unruled count reaches 0. As of
2026-07-29 it is 0 -- both ca_desert batches are corrected and utah_dixie is ruled -- so this is
now flip-ELIGIBLE. Flip it only together with a test that injects the defect and confirms it
bounces, and keep RULED as the escape hatch for the next sourced local date.

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
WARM_SOIL_F = 70          # germination_temp_f lower bound at/above which soil must be warm
SPRING_WINDOW_DAYS = 60   # keep the comparison inside one spring cycle

# (region, zone) -> why an explicit sourced local date legitimately precedes last frost.
# A reason string is REQUIRED: this records that a human read the cell, not that it was muted.
RULED = {
    ('utah_dixie', '8'): (
        "USU Extension 'Suggested Vegetable Planting Dates for Utah' publishes an explicit "
        "Group C (Tender) date of March 15 for St. George, ~2 weeks ahead of the Mar 30 mean "
        "last frost. The region note documents this. Explicit source dates govern over "
        "arithmetic (CLAUDE.md). Ruled 2026-07-29."),
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


def scan(data, require_seed=True, require_warm=True):
    hits = []
    for crop in data['crops']:
        g = crop.get('germination_temp_f')
        warm = (isinstance(g, list) and len(g) == 2
                and isinstance(g[0], (int, float)) and g[0] >= WARM_SOIL_F)
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
            [h for h in scan(data) if (h[2], h[3]) not in RULED]))
        print()

    allhits = scan(data)
    ruled = [h for h in allhits if (h[2], h[3]) in RULED]
    hits = allhits if args.all else [h for h in allhits if (h[2], h[3]) not in RULED]
    print('warm-soil (germination_temp_f low >= %dF) direct-sown crops opening AT OR BEFORE '
          'last frost' % WARM_SOIL_F)
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
        for key in sorted({(h[2], h[3]) for h in ruled}):
            n = sum(1 for h in ruled if (h[2], h[3]) == key)
            print('  %s z%s (%d cells): %s' % (key[0], key[1], n, RULED[key]))
    print()
    print('Read every hit before acting -- an explicit sourced local date may legitimately')
    print('precede last frost; that belongs in RULED with its reason, not in a "fix".')
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
