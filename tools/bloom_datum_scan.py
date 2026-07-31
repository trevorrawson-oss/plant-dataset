#!/usr/bin/env python3
"""Does the document cited for a BLOOM claim actually publish a bloom date?

Background. The citation-integrity arc reached a working premise that "no
extension service publishes bloom dates", established at UAEX (hunt 1) and
NC State (hunt 2). That premise was about to license one roster-wide
declaration asserting the quantity is absent from the literature.

It is too strong. apples.extension.org -- already cited on nine of our own
bloom arms -- states that apple "will generally bloom in mid-April" in western
North Carolina and "in mid-May" in Minnesota. That is month-granular published
bloom timing. Declaring those arms undocumented would write a false statement
into the dataset.

So the declaration has to be CLASSIFIED per document, not blanket. This scan
produces that classification.

Verdicts, per document:
  PUBLISHES_TIMING  a bloom-family word sits within PROXIMITY chars of a month
                    -> do NOT declare; the arm may be supportable, go read it
  MENTION_NO_DATE   bloom discussed, only as risk/management language
                    -> the declaration shape fits
  NO_MENTION        the document never mentions bloom at all
                    -> declare, and note the document does not address bloom
  UNDETERMINED      unfetchable or uncached. NEVER absence. (lesson 7)

This is a SCAN a human reads, not a gate. The verdicts are a triage list: a
PUBLISHES_TIMING document may still not publish a date for OUR crop, and a
MENTION_NO_DATE document may still be the right citation for the derivation's
inputs. Read the quoted evidence.

    python3 tools/bloom_datum_scan.py --candidates   # no network, sizes the work
    python3 tools/bloom_datum_scan.py --fetch        # cached in tools/.doc_cache
    python3 tools/bloom_datum_scan.py --report
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

DATA = os.path.join(REPO, 'crops_data_final.json')

# Reuse hunt 2's fetch/cache/extract layer rather than growing a second one.
from doc_mentions_crop_scan import (cache_path, extract, fetch_all,  # noqa: E402
                                    unreadable_reason)

PROXIMITY = 120

BLOOM_RE = re.compile(r'\b(?:bloom(?:s|ing|ed)?|blossom(?:s|ing|ed)?|flowering)\b', re.I)

_MONTHS = ('January|February|March|April|June|July|August|September|October|November|December'
           r'|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec')
MONTH_RE = re.compile(r'\b(?:%s)\b\.?' % _MONTHS)

# "May" is both a month and a modal verb, and the modal is far more common in
# extension prose ("a warm spell may cause the tree to bloom"). Count it as a
# month only in explicit temporal context. Lowercase "may" is never a month.
MAY_RE = re.compile(
    r'(?:(?<=\bin )|(?<=\bby )|(?<=\bof )|(?<=\bto )|(?<=\bthrough )|(?<=\buntil )'
    r'|(?<=\bfrom )|(?<=\bduring )|(?<=\bearly )|(?<=\bmid )|(?<=\blate )'
    r'|(?<=\bmid-)|(?<=\blate-)|(?<=\bearly-)|(?<=-))May\b'
    r'|May\s+\d{1,2}\b|May,?\s+\d{4}\b')


def _month_spans(text):
    spans = [m.span() for m in MONTH_RE.finditer(text)]
    spans += [m.span() for m in MAY_RE.finditer(text)]
    return spans


def classify(text):
    """Classify raw document text. Returns {'verdict', 'evidence'}."""
    if text is None:
        return {'verdict': 'UNDETERMINED', 'evidence': ''}
    flat = re.sub(r'\s+', ' ', text)
    blooms = [m.span() for m in BLOOM_RE.finditer(flat)]
    if not blooms:
        return {'verdict': 'NO_MENTION', 'evidence': ''}
    months = _month_spans(flat)
    for bs, be in blooms:
        for ms, me in months:
            gap = ms - be if ms >= be else bs - me
            if gap <= PROXIMITY:
                lo = max(0, min(bs, ms) - 90)
                hi = min(len(flat), max(be, me) + 90)
                return {'verdict': 'PUBLISHES_TIMING', 'evidence': flat[lo:hi].strip()}
    bs, be = blooms[0]
    return {'verdict': 'MENTION_NO_DATE',
            'evidence': flat[max(0, bs - 90):be + 90].strip()}


def classify_doc(cached_text):
    """Classify cached text. A body that is not the document is UNDETERMINED, never absence.

    Delegates to the shared detector so this scan and doc_mentions_crop_scan agree on what
    counts as "read": the NUL fetch sentinel, WAF challenge pages served as HTTP 200, and
    PDFs with no extractable text layer.
    """
    reason = unreadable_reason(cached_text)
    if reason is not None:
        return {'verdict': 'UNDETERMINED', 'evidence': reason}
    return classify(cached_text)


def _urls_of(node):
    au = node.get('anchoring_urls')
    if not isinstance(au, dict):
        return []
    return sorted({v['url'] for v in au.values()
                   if isinstance(v, dict) and isinstance(v.get('url'), str)})


def bloom_arms(data):
    """Every bloom claim in the roster, across all three encodings."""
    arms = []
    for crop in data['crops']:
        for rid, region in (crop.get('regions') or {}).items():
            for planting in (region.get('plantings') or []):
                bloom = planting.get('bloom')
                if not isinstance(bloom, list) or not bloom:
                    continue
                literals = [b for b in bloom if isinstance(b, str)]
                for arm in bloom:
                    if not isinstance(arm, dict):
                        continue
                    if arm.get('offset_days') is not None:
                        shape = 'offset'
                    elif arm.get('window') is not None:
                        shape = 'synthesis_window'
                    else:
                        shape = 'other'
                    arms.append({'crop': crop['slug'], 'region': rid, 'shape': shape,
                                 'label': arm.get('label'), 'from': arm.get('from'),
                                 'offset_days': arm.get('offset_days'),
                                 'window_days': arm.get('window_days'),
                                 'value': arm.get('window'),
                                 'sources': list(arm.get('sources') or []),
                                 'urls': _urls_of(arm)})
                if literals:
                    arms.append({'crop': crop['slug'], 'region': rid,
                                 'shape': 'month_literal', 'label': planting.get('label'),
                                 'from': None, 'offset_days': None, 'window_days': None,
                                 'value': ' - '.join(literals),
                                 'sources': list(planting.get('sources') or []),
                                 'urls': _urls_of(planting)})
    return arms


def declared(data):
    """(crop, region_token) pairs that already carry a bloom declaration."""
    out = set()
    for crop in data['crops']:
        for f in (crop.get('verification_status') or {}).get('open_findings') or []:
            fid = f.get('id') or ''
            if fid.endswith('_bloom_offset_undocumented'):
                out.add((crop['slug'], fid[:-len('_bloom_offset_undocumented')]))
    return out


def load_data():
    with open(DATA, encoding='utf-8') as fh:
        return json.load(fh)


def load_cached(url):
    p = cache_path(url)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidates', action='store_true')
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--refetch-unreadable', action='store_true',
                    help='also retry cached bodies that are not the document')
    ap.add_argument('--crop')
    args = ap.parse_args()

    data = load_data()
    arms = bloom_arms(data)
    if args.crop:
        arms = [a for a in arms if a['crop'] == args.crop]
    urls = sorted({u for a in arms for u in a['urls']})
    dec = declared(data)

    if args.candidates or not (args.fetch or args.report):
        by_shape = {}
        for a in arms:
            by_shape.setdefault(a['shape'], []).append(a)
        print('bloom arms: %d  crops: %d  regions: %d  distinct documents: %d'
              % (len(arms), len({a['crop'] for a in arms}),
                 len({a['region'] for a in arms}), len(urls)))
        for shape, rows in sorted(by_shape.items()):
            n_dec = sum(1 for a in rows if (a['crop'], a['region']) in dec)
            print('  %-16s %4d arms  (%d already declared, %d not)'
                  % (shape, len(rows), n_dec, len(rows) - n_dec))
        cached = sum(1 for u in urls if os.path.exists(cache_path(u)))
        print('cache: %d/%d documents present' % (cached, len(urls)))

    if args.fetch:
        fetch_all(urls, refetch_unreadable=args.refetch_unreadable)

    if args.report:
        verdicts = {u: classify_doc(load_cached(u)) for u in urls}
        tally = {}
        for a in arms:
            vs = [verdicts[u]['verdict'] for u in a['urls']]
            best = ('PUBLISHES_TIMING' if 'PUBLISHES_TIMING' in vs
                    else 'MENTION_NO_DATE' if 'MENTION_NO_DATE' in vs
                    else 'UNDETERMINED' if 'UNDETERMINED' in vs
                    else 'NO_MENTION' if vs else 'NO_URL')
            a['verdict'] = best
            key = (best, (a['crop'], a['region']) in dec)
            tally[key] = tally.get(key, 0) + 1

        print('\n=== ARM VERDICTS (best verdict across the arm\'s documents) ===')
        for (v, isdec), n in sorted(tally.items(), key=lambda kv: -kv[1]):
            print('  %-18s %s  %4d' % (v, 'declared    ' if isdec else 'NOT declared', n))

        print('\n=== DOCUMENTS PUBLISHING BLOOM TIMING (do not declare these blind) ===')
        for u in urls:
            if verdicts[u]['verdict'] != 'PUBLISHES_TIMING':
                continue
            users = sorted({(a['crop'], a['region']) for a in arms if u in a['urls']})
            print('\n  %s' % u)
            print('    cited on %d arms: %s' % (len(users), ', '.join(
                '%s/%s' % cr for cr in users[:6]) + (' ...' if len(users) > 6 else '')))
            print('    evidence: %s' % verdicts[u]['evidence'][:300])

        print('\n=== UNDETERMINED DOCUMENTS (not evidence of absence) ===')
        for u in urls:
            if verdicts[u]['verdict'] == 'UNDETERMINED':
                print('  %-95s %s' % (u[:95], verdicts[u]['evidence'][:50]))


if __name__ == '__main__':
    main()
