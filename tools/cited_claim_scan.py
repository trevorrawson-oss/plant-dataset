#!/usr/bin/env python3
"""Scan the documents a crop CITES for a numeric claim, without lying about a zero.

READ-ONLY on canonical. Not a gate, not a promote.

WHY THIS EXISTS. On 2026-08-05 campaign D scanned "all 29 URLs lemon cites (17 cached and
readable) for a lemon-adjacent temperature in the 24-32F band" and reported ZERO hits. That
zero became finding F1 ("the number is uncited, and three institutions are credited for it that
do not publish it") and finding F5 ("four publish no lemon-applicable damage temperature at
all"). Both were false, and the instrument was the reason.

`uf_ifas_hs1153` -- UF/IFAS HS1153/HS402, "Lemon Growing in the Florida Home Landscape", a
document lemon cites in 87 places and which was cached and readable the whole time -- says:

    "trees are susceptible to freezing temperatures: defoliated at 22-24F, severe wood damaged
     at 20F, flowers and young fruit are killed at 29F, and mature fruit damaged at 28F to 31F"

Four lemon-specific figures. The scan missed all four because of the word "lemon-adjacent": the
nearest "lemon" is 333 characters from the temperatures. On a crop MONOGRAPH the crop is the
subject of the section and is not repeated in every sentence, so the tighter the proximity
window the more confident the wrong answer. This is [[adjudication-vocabulary-outruns-the-test]]
applied to documents rather than findings -- the document declares its subject in the TITLE, and
the test looked for it in the sentence.

SO THIS TOOL REFUSES TO REPORT AN ABSENCE IT CANNOT SUPPORT. `assert_absence_reportable` raises
`UnreportableAbsence` when

  * any cited URL is UNCACHED -- unread is UNDETERMINED, never absent
    ([[absence-findings-are-document-scoped]], [[waf-block-pages-cached-as-absence]]); or
  * a proximity filter was used and the set contains a document whose TITLE names the crop; or
  * the cached set came back empty, which means the cache lookup broke rather than the
    literature being silent ([[a-clean-zero-can-be-your-own-parser]]).

`proximity_band_hits` is kept deliberately, as the WRONG method, so the regression test can
re-introduce the original bug and prove the guard fires.

    $ python3 tools/cited_claim_scan.py lemon              # the 24-32F band, per document
    $ python3 tools/cited_claim_scan.py lemon --lo 20 --hi 35
    $ python3 tools/cited_claim_scan.py lemon --proximity 200   # show what the bug reported
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
DOC_CACHE = os.path.join(REPO, 'tools', '.doc_cache')

# Matches "29F", "29 F", "29 degrees F", "22-24F" (both endpoints), with or without the degree
# sign. Kept broad on purpose: narrowing a claim scan is how the last one produced a zero.
_TEMP = re.compile(
    r'(?<![\d.])(\d{1,3})\s*(?:[°º]\s*F|\s*degrees?\s*F)(?![a-z])',
    re.IGNORECASE)
_RANGE = re.compile(
    r'(?<![\d.])(\d{1,3})\s*(?:-|–|—|\s+to\s+)\s*(\d{1,3})\s*(?:[°º]\s*F|\s*degrees?\s*F)',
    re.IGNORECASE)

Hit = collections.namedtuple('Hit', 'value start context')


class UnreportableAbsence(Exception):
    """Raised when a zero result cannot honestly be written down as an absence."""


class Report:
    def __init__(self, slug, lo, hi):
        self.slug = slug
        self.lo = lo
        self.hi = hi
        self.rows = []          # (source_id, url, state, [Hit])
        self.uncached = []      # [(source_id, url)]

    @property
    def cached_count(self):
        return sum(1 for r in self.rows if r[2] == 'CACHED')

    @property
    def hit_documents(self):
        return [r for r in self.rows if r[3]]

    @property
    def subject_documents(self):
        return [r for r in self.rows if r[2] == 'CACHED' and r[4]]


def cache_path(url):
    """Where bare_host_scan's fetcher parks a document. Keyed by sha1 of the exact URL."""
    return os.path.join(DOC_CACHE, hashlib.sha1(url.encode()).hexdigest() + '.txt')


# A cached FILE is not a cached DOCUMENT. The fetcher writes its own failures into the cache as
# content -- 48 `\x00FETCHFAIL ...` stubs and 10 Incapsula challenge pages were sitting in
# tools/.doc_cache on 2026-08-06. Left unfiltered they read as CACHED and scan clean, which is
# [[waf-block-pages-cached-as-absence]] arriving through our own fetcher instead of the network.
_NOT_A_DOCUMENT = re.compile(
    r'FETCHFAIL|Request unsuccessful\. Incapsula|Access Denied|Attention Required', re.I)
MIN_DOCUMENT_BYTES = 300


def is_document(text):
    """False when the cached bytes are a fetch failure, a WAF challenge, or implausibly short."""
    return len(text) >= MIN_DOCUMENT_BYTES and not _NOT_A_DOCUMENT.search(text[:400])


def _load():
    with open(CANONICAL, encoding='utf-8') as fh:
        return json.load(fh)


def cited_urls(slug, data=None):
    """Every (source_id, url) pair the crop cites in an `anchoring_urls` block."""
    data = data or _load()
    crop = next((c for c in data['crops'] if c.get('slug') == slug), None)
    if crop is None:
        raise SystemExit(f"no crop with slug {slug!r}")
    pairs = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'anchoring_urls' and isinstance(value, dict):
                    for sid, entry in value.items():
                        url = entry.get('url') if isinstance(entry, dict) else entry
                        if url:
                            pairs.add((sid, url))
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(crop)
    return sorted(pairs)


def band_hits(text, lo, hi):
    """Every temperature in [lo, hi], with NO proximity filter. Read these, do not count them.

    A bare "22-24F" carries its unit only once, so both endpoints come from `_RANGE`. A written-
    out "28F to 31F" carries it twice and is two `_TEMP` matches. Suppression is therefore scoped
    to the exact span of a matched range -- an early cut suppressed any `_TEMP` hit within 40
    characters of an earlier one, which silently ate the 31 in "mature fruit damaged at 28F to
    31F". Dropping a second figure is the same class of defect this whole tool exists to catch.
    """
    hits, spans = [], []
    for match in _RANGE.finditer(text):
        spans.append((match.start(), match.end()))
        for value in (int(match.group(1)), int(match.group(2))):
            if lo <= value <= hi:
                hits.append(Hit(value, match.start(), _ctx(text, match.start(), match.end())))
    for match in _TEMP.finditer(text):
        value = int(match.group(1))
        if not lo <= value <= hi:
            continue
        if any(start <= match.start() < end for start, end in spans):
            continue
        hits.append(Hit(value, match.start(), _ctx(text, match.start(), match.end())))
    return sorted(hits, key=lambda h: (h.start, h.value))


def proximity_band_hits(text, term, window, lo, hi):
    """THE WRONG METHOD, kept so the regression test can prove it lies. Do not call it."""
    return [h for h in band_hits(text, lo, hi)
            if term.lower() in text[max(0, h.start - window):h.start + window].lower()]


def document_subject_is(text, term, head_chars=400):
    """True when the document's TITLE names the crop -- i.e. the crop is its subject.

    A crop monograph mentions the crop in its title and then stops repeating it, which is exactly
    what defeats a proximity filter. HS402's head is "HS1153/HS402: Lemon Growing in the Florida
    Home Landscape"; Clemson's is "Cold Tolerance in Citrus" and TAMU's is "Citrus".
    """
    return term.lower() in re.sub(r'\s+', ' ', text[:head_chars]).lower()


def _ctx(text, start, end, pad=200):
    return re.sub(r'\s+', ' ', text[max(0, start - pad):end + pad]).strip()


def scan_crop(slug, lo, hi, data=None):
    report = Report(slug, lo, hi)
    for sid, url in cited_urls(slug, data):
        path = cache_path(url)
        if not os.path.exists(path):
            report.uncached.append((sid, url))
            report.rows.append((sid, url, 'UNCACHED', [], False))
            continue
        text = open(path, encoding='utf-8', errors='replace').read()
        if not is_document(text):
            # cached, but what was cached is not the document -- UNDETERMINED, never absence
            report.uncached.append((sid, url))
            report.rows.append((sid, url, 'NOT-A-DOCUMENT', [], False))
            continue
        report.rows.append(
            (sid, url, 'CACHED', band_hits(text, lo, hi), document_subject_is(text, slug)))
    return report


def assert_absence_reportable(report, used_proximity):
    """Raise unless a zero over this report could honestly be written down as an absence.

    EVERY reason is collected and raised together. Returning on the first one would hide the
    others, and "the check that fires first masks the rest" is the exact shape of
    [[guard-tests-pass-because-an-earlier-check-fires]] -- a reader who fixes the uncached URLs
    must not then be told, as if it were news, that the proximity method was invalid too.
    """
    reasons = []
    if report.cached_count == 0:
        reasons.append(
            f"0 of {len(report.rows)} cited documents were readable -- the cache lookup is "
            f"broken, not the literature silent")
    if report.uncached:
        reasons.append(
            f"{len(report.uncached)} of {len(report.rows)} cited URLs are uncached and therefore "
            f"UNDETERMINED, not absent: "
            + ", ".join(u for _, u in report.uncached[:3])
            + (" ..." if len(report.uncached) > 3 else ""))
    if used_proximity and report.subject_documents:
        reasons.append(
            "a proximity filter cannot establish absence over a subject document (its title "
            "names the crop, so the crop name is not repeated near the claim): "
            + ", ".join(r[1] for r in report.subject_documents))
    if reasons:
        raise UnreportableAbsence("; ".join(reasons))
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('slug')
    parser.add_argument('--lo', type=int, default=24)
    parser.add_argument('--hi', type=int, default=32)
    parser.add_argument('--proximity', type=int, default=None,
                        help="re-run the WRONG method with this window, to show what it hides")
    args = parser.parse_args()

    report = scan_crop(args.slug, args.lo, args.hi)
    print(f"{args.slug}: {len(report.rows)} cited (source, url) pairs; "
          f"{report.cached_count} cached, {len(report.uncached)} uncached")
    print(f"band {args.lo}-{args.hi}F, NO proximity filter\n")

    for sid, url, state, hits, subject in report.rows:
        if state == 'UNCACHED':
            print(f"  UNDETERMINED  {sid:18s} {url}")
            continue
        flag = ' [SUBJECT DOCUMENT]' if subject else ''
        print(f"  {'HIT ' if hits else 'none'}          {sid:18s} {url}{flag}")
        for hit in hits[:6]:
            print(f"        {hit.value}F > {hit.context[:240]}")

    print(f"\n{len(report.hit_documents)} of {report.cached_count} readable documents carry a "
          f"figure in band.")
    if args.proximity is not None:
        total = 0
        for sid, url, state, _hits, _subject in report.rows:
            if state != 'CACHED':
                continue
            text = open(cache_path(url), encoding='utf-8', errors='replace').read()
            total += len(proximity_band_hits(text, args.slug, args.proximity, args.lo, args.hi))
        print(f"the WRONG method (+/-{args.proximity} chars of {args.slug!r}) would report "
              f"{total} hits.")

    try:
        assert_absence_reportable(report, used_proximity=args.proximity is not None)
        print("\nan absence over this set WOULD be reportable.")
    except UnreportableAbsence as exc:
        print(f"\nABSENCE NOT REPORTABLE: {exc}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
