#!/usr/bin/env python3
"""DIAGNOSTIC, NOT A GATE -- verification_log_ref count-assertion scanner.

READ docs/verification_log_ref_convention.md BEFORE using or wiring this.

WHY THIS IS NOT WIRED INTO THE SUITE, and must not be:
    Measured 2026-07-29 against canonical b0d01f13 it produces 14 findings, of which
    exactly TWO are defects. ~6 are regex noise on legitimate prose (pear "better with
    two varieties" is pollination advice, not a varieties-array count; strawberry's
    "the documented z3-11 fruiting"; swiss-chard's deliberate "(6 cells)" subset), and
    8 are CORRECT HISTORICAL STATEMENTS about the 10-region era that only look stale
    because the roster grew to 16.

    Tightening the regexes cannot rescue it: the dominant category is correct prose,
    and no pattern distinguishes "stale because the roster grew" (Class 1, no action)
    from "stale because the value was retired" (Class 2, needs a correction line).
    That is a judgment about CAUSES. See the convention doc's two-class rule.

    Wiring it anyway reproduces a25-tightening-floods / growth-stages-shape-not-gated:
    a noisy gate gets ignored, which is worse than no gate.

WHAT IT IS FOR:
    A periodic human-read sweep. Run it after a suitability-vocabulary change or a
    region-belt addition, READ every finding (do not count them), and classify each as
    Class 1 or Class 2 per the convention. Class 2 gets a dated correction line appended.

    $ python3 tools/logref_count_scan.py
"""
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

WORDNUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
    'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20,
}
NUM = (r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|'
       r'thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)')

COUNT_PATTERNS = [
    ('regions', re.compile(NUM + r'[\s-]+regions?\b', re.I), 'regions'),
    ('cells', re.compile(NUM + r'[\s-]+cells?\b', re.I), 'cells'),
    ('varieties', re.compile(NUM + r'[\s-]+varieties\b', re.I), 'varieties'),
]
SUIT_PATTERNS = [
    ('perennializes', re.compile(NUM + r'\s+(?:cells?\s+)?perennializ', re.I)),
    ('marginal', re.compile(NUM + r'\s+(?:cells?\s+)?(?:are\s+)?marginal', re.I)),
    ('unsuitable', re.compile(NUM + r'\s+(?:cells?\s+)?(?:are\s+)?unsuitable', re.I)),
    ('survives_no_fruit', re.compile(NUM + r'\s+(?:cells?\s+)?survives?[_ ]no[_ ]fruit', re.I)),
    ('annual_only', re.compile(NUM + r'\s+(?:cells?\s+)?annual[_ ]only', re.I)),
]
CORRECTION = re.compile(r'\[CORRECTION\s+\d{4}-\d{2}-\d{2}', re.I)


def word_to_int(tok):
    tok = tok.lower()
    return int(tok) if tok.isdigit() else WORDNUM.get(tok)


def measure(crop):
    """Live region/cell/suitability/variety counts for one crop."""
    nregions = ncells = 0
    suit = collections.Counter()
    for _rk, region in (crop.get('regions') or {}).items():
        cells = [c for c in ((region or {}).get('resolved_by_zone') or {}).values()
                 if isinstance(c, dict)]
        if cells:
            nregions += 1
        ncells += len(cells)
        for cell in cells:
            if cell.get('suitability'):
                suit[cell['suitability']] += 1
    return ({'regions': nregions, 'cells': ncells,
             'varieties': len(crop.get('varieties') or [])}, suit)


def scan(data):
    out = []
    for crop in data['crops']:
        log_ref = (crop.get('verification_status') or {}).get('verification_log_ref')
        if not log_ref:
            continue
        if not isinstance(log_ref, str):
            # lettuce-leaf carries the original LIST-of-filenames shape. Ruled: leave it.
            out.append((crop['slug'], [('shape', type(log_ref).__name__, 'str', str(log_ref))], False))
            continue
        actual, suit = measure(crop)
        findings = []
        for label, rx, key in COUNT_PATTERNS:
            for m in rx.finditer(log_ref):
                val = word_to_int(m.group(1))
                if val is not None and val != actual[key]:
                    findings.append((label, val, actual[key],
                                     log_ref[max(0, m.start() - 60):m.end() + 40]))
        for key, rx in SUIT_PATTERNS:
            for m in rx.finditer(log_ref):
                val = word_to_int(m.group(1))
                if val is not None and val != suit.get(key, 0):
                    findings.append(('suit:' + key, val, suit.get(key, 0),
                                     log_ref[max(0, m.start() - 60):m.end() + 40]))
        if findings:
            out.append((crop['slug'], findings, bool(CORRECTION.search(log_ref))))
    return out


def main():
    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    rows = scan(data)
    have = sum(1 for c in data['crops']
               if (c.get('verification_status') or {}).get('verification_log_ref'))
    print(f'crops with a verification_log_ref: {have}')
    print(f'crops with >=1 mismatched count assertion: {len(rows)}')
    print()
    print('READ EVERY FINDING. Classify each Class 1 (context growth, no action) or')
    print('Class 2 (retired reasoning / revalued vocabulary, correction line required).')
    print('See docs/verification_log_ref_convention.md.')
    print()
    for slug, findings, has_correction in rows:
        print('=' * 78)
        print(slug, '[correction line present]' if has_correction else '[no correction line]')
        for label, claimed, actual_val, ctx in findings:
            print(f'   {label}: claims {claimed}, actual {actual_val}')
            print(f'      ...{" ".join(str(ctx).split())}...')
    return 0


if __name__ == '__main__':
    sys.exit(main())
