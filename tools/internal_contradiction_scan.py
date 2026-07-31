#!/usr/bin/env python3
"""Find cells that contradict data we ALREADY HOLD. No network. No document hunt.

WHY THIS EXISTS. The citation arc's yield has been user-facing data defects, found because
locating a document forces you to read the cell against it. But the deciding evidence was
usually already in the file. Blueberry is the case that proves it: mid_south z7 was authored
`rabbiteye` while `region_chill_delivered` said that zone banks 1000-1300 chill hours, our own
variety table said rabbiteye needs 350-600 and northern highbush 800-1000, our own
northern_tier already used northern highbush at z7, and our own variety note said "match the
type to your winter chill". Four internal facts, no documents. Nobody looked across.

So the hunt was the wrong UNIT. Detection needs no document at all; only adjudication does,
and then it is ONE targeted lookup for ONE crop rather than every publication for a region.

WHAT IT REPORTS -- five families, each the shape of a defect this arc actually found:

  CHILL      recommended type mismatched to the chill the zone banks   (blueberry)
  TYPE       regions disagree on a categorical recommendation          (blueberry)
  SUIT       regions disagree on suitability at the same zone          (sour cherry)
  DATES      a region shares no planting month with any peer           (fig, raspberry)
  TEMPLATE   near-identical prose crediting a DIFFERENT institution    (fabricated UAEX claim)
  NPK        fertilizer prose contradicts the ratio it recommends      (tomato 8-32-16)

THESE ARE CONTESTED CELLS, NOT VERDICTS. Every prototype of these checks flagged cells that
turned out to be RIGHT: mid_atlantic rabbiteye ranked first on chill and NC State explicitly
recommends it; mid_south fig is still a date outlier after being corrected; the minority-of-one
heuristic pointed at northern_tier, which was correct. The scan says "two things you hold
disagree" -- a human decides which. It must never become a gate on that basis, with one
possible exception noted under CHILL.

    python3 tools/internal_contradiction_scan.py            # everything
    python3 tools/internal_contradiction_scan.py --family NPK
"""
import argparse
import collections
import difflib
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, 'crops_data_final.json')

MONTHS = {m: i for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}

INSTITUTION = re.compile(
    r'\b(?:NC State|North Carolina State|University of Arkansas|UAEX|Clemson|Virginia Cooperative|'
    r'Penn State|Rutgers|UMass|UMaine|UNH|Texas A&M|AgriLife|Utah State|Oregon State|'
    r'Washington State|Michigan State|Iowa State|New Mexico State|LSU|Kansas State|'
    r'Oklahoma State|University of (?:Arizona|Florida|Georgia|Nevada|California|Minnesota|'
    r'Missouri|Maine|Hawaii))\b')

# A bare N-P-K run. The negative lookarounds are load-bearing: without them "15.5-0-0"
# (calcium nitrate) yields the phantom ratio 5-0-0, which invented seven defects in the
# prototype, and a lot number like 2020-10-10-10 parses as a fertilizer.
RATIO = re.compile(r'(?<![\d.\-])(\d{1,2})-(\d{1,2})-(\d{1,2})(?![\d.\-])')


def parse_ratios(text):
    if not isinstance(text, str):
        return []
    return [(int(a), int(b), int(c)) for a, b, c in RATIO.findall(text)]


def months(window):
    """Month index set for a window string, or None if nothing parseable."""
    if not isinstance(window, str):
        return None
    found = [MONTHS[m] for m in re.findall(r'\b(%s)\b' % '|'.join(MONTHS), window)]
    if not found:
        return None
    a, b = found[0], found[-1]
    return set((a + k) % 12 for k in range((b - a) % 12 + 1))


def chill_verdict(delivered, required):
    """UNDER (serious), OVER (advisory) or None.

    Direction is NOT symmetric and must never be scored as one number. Under-delivery is a
    real agronomic failure: the plant never satisfies dormancy and fruit set collapses.
    Over-delivery is usually harmless -- NC State recommends rabbiteye across most of North
    Carolina for SOIL and HEAT tolerance even where chill far exceeds its requirement, which
    no arithmetic here can see.
    """
    dlo, dhi = delivered
    rlo, rhi = required
    if dhi < rlo:
        return 'UNDER'
    if dlo > rhi + 400:
        return 'OVER'
    return None


def institution_swap(a, b, threshold=0.85):
    """Near-identical prose crediting different institutions -> (ratio, inst_a, inst_b)."""
    if not isinstance(a, str) or not isinstance(b, str) or len(a) < 120 or len(b) < 120:
        return None
    ia, ib = set(INSTITUTION.findall(a)), set(INSTITUTION.findall(b))
    if not ia or not ib or ia == ib:
        return None
    if difflib.SequenceMatcher(None, a, b).quick_ratio() < threshold:
        return None
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    if ratio < threshold:
        return None
    return (round(ratio, 2), sorted(ia), sorted(ib))


# --------------------------------------------------------------------------- NPK

_N_HIGH = re.compile(r'\b(?:high|higher|highest|rich in|plenty of)\b[^.]{0,30}\bnitrogen\b'
                     r'|\bnitrogen-rich\b|\bhigh N\b|\bfirst number\b[^.]{0,30}\bhighest\b', re.I)
_K_HIGH = re.compile(r'\b(?:high|higher|highest)\b[^.]{0,30}\b(?:potassium|potash)\b'
                     r'|\bhigh K\b|\bthird number\b[^.]{0,30}\bhighest\b', re.I)
_P_HIGH = re.compile(r'\b(?:high|higher|highest)\b[^.]{0,30}\bphosph'
                     r'|\bsecond number\b[^.]{0,30}\bhighest\b', re.I)


def npk_contradictions(slug, fert):
    """Fertilizer prose that contradicts a ratio the SAME cell recommends.

    Only ratios the cell presents as its own recommendation are judged. A side-dress named
    alongside the primary ratio (calcium nitrate for a leafy green, 27-3-3 for collards) is a
    deliberate second product, not a contradiction -- reading those as the primary ratio was
    the prototype's other false-positive source.
    """
    if not isinstance(fert, dict):
        return []
    hints = ' '.join(str(fert.get(k) or '') for k in ('npk_hint_beginner', 'npk_hint_seasoned'))
    primary = parse_ratios(str(fert.get('npk_ratio') or ''))
    judged = list(primary)
    # a ratio quoted inside the hint prose is being recommended there, so it is in scope --
    # unless the sentence marks it as a follow-on feed.
    for sentence in re.split(r'(?<=[.;])\s+', hints):
        if re.search(r'side-?dress|then\b|follow|later|after', sentence, re.I):
            continue
        judged += parse_ratios(sentence)
    if not judged:
        return []

    claims = set()
    if _N_HIGH.search(hints):
        claims.add('N')
    if _K_HIGH.search(hints):
        claims.add('K')
    if _P_HIGH.search(hints):
        claims.add('P')
    if not claims:
        return []

    out, seen = [], set()
    for n, p, k in judged:
        vals = {'N': n, 'P': p, 'K': k}
        for c in sorted(claims):
            if vals[c] < max(vals.values()):
                key = (c, n, p, k)
                if key in seen:
                    continue
                seen.add(key)
                name = {'N': 'nitrogen', 'P': 'phosphorus', 'K': 'potassium'}[c]
                out.append({'crop': slug, 'family': 'NPK',
                            'detail': 'prose calls for high %s but recommends %d-%d-%d, '
                                      'where %s is not the largest number'
                                      % (name, n, p, k, name)})
    return out


# ------------------------------------------------------------------- the scan

def _varieties(crop):
    v = crop.get('varieties')
    if isinstance(v, dict):
        v = v.get('recommended')
    if isinstance(v, list) and v and isinstance(v[0], list):
        v = v[0]
    return [x for x in (v or []) if isinstance(x, dict)]


def scan(data):
    rcd = data.get('region_chill_delivered') or {}
    findings = []

    bands = collections.defaultdict(list)
    for crop in data['crops']:
        for var in _varieties(crop):
            t, ch = var.get('type'), var.get('chill_hours_required')
            if t and isinstance(ch, (int, float)):
                bands[(crop['slug'], t)].append(ch)

    cat = collections.defaultdict(lambda: collections.defaultdict(set))
    windows = collections.defaultdict(dict)
    prose = collections.defaultdict(list)

    for crop in data['crops']:
        slug = crop['slug']
        types = {t: (min(v), max(v)) for (s, t), v in bands.items() if s == slug}
        findings.extend(npk_contradictions(slug, crop.get('fertilizer')))

        for rid, region in (crop.get('regions') or {}).items():
            for z, cell in (region.get('resolved_by_zone') or {}).items():
                rt = cell.get('recommended_type')
                if rt and rt in types and (rcd.get(rid) or {}).get(z):
                    v = chill_verdict(tuple(rcd[rid][z]), types[rt])
                    if v:
                        findings.append({
                            'crop': slug, 'family': 'CHILL', 'severity': v,
                            'detail': '%s/z%s recommends %s (needs %d-%d h) where the zone '
                                      'banks %d-%d h' % (rid, z, rt, types[rt][0], types[rt][1],
                                                         rcd[rid][z][0], rcd[rid][z][1])})
                for f in ('recommended_type', 'suitability'):
                    val = cell.get(f)
                    if isinstance(val, str) and val:
                        cat[(slug, f, z)][val].add(rid)
                m = months(cell.get('plant_out'))
                if m:
                    windows[(slug, z)][rid] = (m, cell.get('plant_out'))
                for f in ('suitability_note_seasoned', 'suitability_note_beginner'):
                    val = cell.get(f)
                    if isinstance(val, str):
                        prose[(slug, f)].append((rid, val))

    for (slug, f, z), vals in cat.items():
        if len(vals) > 1 and sum(len(r) for r in vals.values()) >= 3:
            findings.append({
                'crop': slug, 'family': 'TYPE' if f == 'recommended_type' else 'SUIT',
                'detail': 'z%s: %s' % (z, '; '.join(
                    '%s=%s' % (v, ','.join(sorted(r))) for v, r in sorted(vals.items())))})

    for (slug, z), byreg in windows.items():
        if len(byreg) < 4:
            continue
        for rid, (m, raw) in byreg.items():
            if not any(m & other for k, (other, _) in byreg.items() if k != rid):
                findings.append({'crop': slug, 'family': 'DATES',
                                 'detail': '%s/z%s plants %r, sharing no month with any of the '
                                           '%d peer regions' % (rid, z, raw, len(byreg) - 1)})

    for (slug, f), items in prose.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                (ra, a), (rb, b) = items[i], items[j]
                if ra == rb:
                    continue
                sw = institution_swap(a, b)
                if sw:
                    findings.append({
                        'crop': slug, 'family': 'TEMPLATE',
                        'detail': '%s vs %s prose %d%% identical but credits %s vs %s'
                                  % (ra, rb, round(sw[0] * 100), '/'.join(sw[1]),
                                     '/'.join(sw[2]))})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--family')
    ap.add_argument('--crop')
    args = ap.parse_args()
    with open(DATA, encoding='utf-8') as fh:
        data = json.load(fh)
    findings = scan(data)
    if args.family:
        findings = [f for f in findings if f['family'] == args.family.upper()]
    if args.crop:
        findings = [f for f in findings if f['crop'] == args.crop]

    by = collections.defaultdict(list)
    for f in findings:
        by[f['family']].append(f)

    print('=' * 92)
    print('INTERNAL CONTRADICTIONS -- cells that disagree with data we already hold')
    print('=' * 92)
    print('CONTESTED CELLS, NOT VERDICTS. Several known-CORRECT cells appear here by design.')
    print('Read each one; do not quote the total as a defect count.\n')
    for fam in ('NPK', 'CHILL', 'TYPE', 'DATES', 'TEMPLATE', 'SUIT'):
        rows = by.get(fam) or []
        if not rows:
            continue
        extra = ''
        if fam == 'CHILL':
            u = sum(1 for r in rows if r.get('severity') == 'UNDER')
            extra = '  (%d UNDER = serious, %d OVER = advisory)' % (u, len(rows) - u)
        print('--- %s : %d%s' % (fam, len(rows), extra))
        for r in sorted(rows, key=lambda x: (x.get('severity') != 'UNDER', x['crop']))[:40]:
            tag = (r.get('severity') + ' ') if r.get('severity') else ''
            print('    %-18s %s%s' % (r['crop'], tag, r['detail'][:150]))
        if len(rows) > 40:
            print('    ... %d more' % (len(rows) - 40))
        print()
    print('total contested cells: %d' % len(findings))


if __name__ == '__main__':
    main()
