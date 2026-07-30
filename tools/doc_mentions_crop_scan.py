#!/usr/bin/env python3
"""Find cited documents that DO NOT MENTION THE CROP they are cited for.

READ docs/kickoffs/46-citation-integrity-cleanup-arc.md and
docs/2026-07-30-mid-south-uada-ext-citation-hunt.md before acting on this output.

WHY THIS EXISTS. `bare_host_scan.py` finds citations pointing at a domain root -- an honest
"cannot verify". This finds the WORSE and previously INVISIBLE case: a real, live, correctly
titled land-grant document cited for a claim it does not contain.

The 2026-07-30 mid_atlantic hunt found `vce_426_331` -- catalogued only as "Virginia
Cooperative Extension Publication 426-331. Mid-Atlantic regional coverage" -- is actually
"Virginia's Home Garden VEGETABLE Planting Guide". Word counts in the fetched document:
bean 12, lettuce 8, tomato 4, and cherry/apple/peach/pear/plum/apricot/fig/persimmon/
blueberry/raspberry/strawberry ALL ZERO. It is the SOLE source on 19 fruit nodes carrying
plant_out, harvest, bloom and suitability.

NO EXISTING CHECK CAN SEE THAT:
  bare_host_scan   the url is PATHED, so it is not a bare host
  url_health_gate  the url returns HTTP 200, so it is healthy
  whole_crop_gate  anchoring presence is satisfied -- a source IS cited
That is exactly why it survived. This is the unr_fs0261 shape, and it looks WELL sourced.

THE NARROWING, which is the whole design (the "narrow the CHECK, not its scope" lesson):

  1. Only nodes making a CROP-SPECIFIC claim are candidates -- a concrete plant_out /
     harvest / bloom window, a suitability, a recommended_type. Structural offset arms and
     chill/frost anchors are a different claim type and are out of scope.

  2. A node is flagged only when **NONE** of its cited documents mentions the crop. This is
     what stops the flood: a climate reference legitimately names no crops (uada_ext_chill is
     a chilling-hour table, nws_lzk a frost table), and it is normally cited ALONGSIDE a crop
     document. Requiring ALL sources to miss the crop means the companion document clears the
     node. When a climate table is genuinely the ONLY source for a per-crop planting window,
     that IS the defect.

  3. Matching is deliberately LENIENT -- head noun, plurals, and every alternate name. A
     document saying "cherries" clears cherry-sour. The failure mode being minimized is
     ACCUSING A GOOD CITATION, so the check errs toward silence.

  4. A URL that cannot be fetched is UNDETERMINED, never a defect (the tamu_agrilife 403
     lesson: record "could not determine", never absence).

NOT A GATE, and needs the network. Ships as a scan, like bare_host_scan and
citation_provenance_scan. Fetches are cached on disk so re-runs are free.

    $ python3 tools/doc_mentions_crop_scan.py --candidates   # no network: what would be checked
    $ python3 tools/doc_mentions_crop_scan.py --fetch        # populate the cache (slow, polite)
    $ python3 tools/doc_mentions_crop_scan.py --report       # read the findings
"""
import argparse
import collections
import io
import json
import os
import re
import sys
import time
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
CACHE = os.path.join(REPO, 'tools', '.doc_cache')

BARE = re.compile(r'https?://[^/]+/?$')
UA = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9'}

# claim keys that are CROP-SPECIFIC -- the only ones in scope
CLAIM_KEYS = ('plant_out', 'harvest', 'harvest_start', 'harvest_end', 'bloom',
              'suitability', 'recommended_type')

# hand-maintained, because a crop's document may use the other common name.
# Lenient by design: any one hit clears the node.
SYNONYMS = {
    'zucchini-courgette': ['zucchini', 'courgette', 'summer squash'],
    'broad-beans-fava': ['broad bean', 'fava', 'faba'],
    'edamame': ['edamame', 'soybean', 'soya'],
    'cilantro-coriander': ['cilantro', 'coriander'],
    'arugula': ['arugula', 'rocket'],
    'bok-choy': ['bok choy', 'pak choi', 'chinese cabbage'],
    'swiss-chard': ['chard'],
    'snow-peas': ['snow pea', 'pea'],
    'sugar-snap-peas': ['sugar snap', 'snap pea', 'pea'],
    'pear-asian': ['asian pear', 'pear'],
    'pear-european': ['pear'],
    'cherry-sour': ['sour cherry', 'tart cherry', 'pie cherry', 'cherry', 'cherries'],
    'cherry-sweet': ['sweet cherry', 'cherry', 'cherries'],
    'cherry-tomato': ['cherry tomato', 'tomato'],
    'orange-navel': ['navel', 'orange', 'citrus'],
    'mandarin-clementine': ['mandarin', 'clementine', 'tangerine', 'citrus'],
    'grapefruit': ['grapefruit', 'citrus'],
    'lemon': ['lemon', 'citrus'],
    'lime': ['lime', 'citrus'],
    'dry-bean': ['dry bean', 'dried bean', 'bean'],
    'pole-beans': ['pole bean', 'bean'],
    'green-beans-bush': ['bush bean', 'snap bean', 'green bean', 'bean'],
    'lettuce-leaf': ['lettuce'],
    'microgreens-mix': ['microgreen', 'micro green'],
    'sweet-corn': ['sweet corn', 'corn'],
    # extension planting tables say "corn"/"sweet corn" and never "popcorn";
    # whether sweet-corn DATES apply to popcorn is a claim-support question, not a
    # crop-presence one, and this scan only measures presence.
    'popcorn': ['popcorn', 'corn'],
    'yellow-summer-squash': ['summer squash', 'yellow squash', 'squash'],
    'acorn-squash': ['acorn squash', 'winter squash', 'squash'],
    'butternut-squash': ['butternut', 'winter squash', 'squash'],
    'spaghetti-squash': ['spaghetti squash', 'winter squash', 'squash'],
    'honeydew-melon': ['honeydew', 'melon'],
    'cantaloupe': ['cantaloupe', 'muskmelon', 'melon'],
    'beefsteak-tomato': ['tomato'],
    'heirloom-tomato': ['tomato'],
    'banana-pepper': ['banana pepper', 'pepper'],
    'bell-pepper': ['bell pepper', 'pepper'],
    'cayenne-pepper': ['cayenne', 'pepper'],
    'jalapeno': ['jalapeno', 'jalapeño', 'pepper'],
    'habanero': ['habanero', 'pepper'],
}


# Generic modifiers that must never stand alone as a match term. A term like "green" or
# "sweet" appears in nearly every horticultural document, so it would CLEAR the crop
# unconditionally and hide a real defect -- the same silent-false-negative class as the
# "fig" / "Figure" collision. `green-beans-bush` was the crop that exposed this.
STOPWORDS = {
    'green', 'sweet', 'dry', 'dried', 'pole', 'bush', 'snow', 'sugar', 'snap', 'red',
    'white', 'black', 'purple', 'yellow', 'baby', 'mix', 'wild', 'common', 'garden',
    'hot', 'mini', 'large', 'small', 'early', 'late', 'seed', 'plant', 'tree',
    'winter', 'summer', 'spring', 'fall',
}
# NOTE: 'fig', 'pea', 'bean' and 'bee' are deliberately NOT stopwords. They are legitimate
# crop names, and the word-boundary matcher already prevents the collisions that made them
# look dangerous. Stopwording them would empty those crops' term sets and flood instead.


def crop_terms(crop):
    """Lenient term family for one crop: alternate names, head nouns, plurals."""
    slug = crop['slug']
    if slug in SYNONYMS:
        terms = set(SYNONYMS[slug])
    else:
        terms = set()
        name = (crop.get('name') or '').lower()
        # "Cherry (Sour)" -> "cherry", "sour"; "Zucchini / Courgette" -> both
        for part in re.split(r'[/,]', name):
            part = part.strip()
            if not part:
                continue
            inner = re.findall(r'\(([^)]*)\)', part)
            head = re.sub(r'\([^)]*\)', '', part).strip()
            if head:
                terms.add(head)
                terms.add(head.split()[-1])          # head noun
            for i in inner:
                if i.strip():
                    terms.add('%s %s' % (i.strip(), head)) if head else None
        terms.add(slug.replace('-', ' '))
    out = set()
    for t in terms:
        t = t.strip().lower()
        if len(t) < 3 or t in STOPWORDS:
            continue
        out.add(t.rstrip('s') if t.endswith('s') and not t.endswith('ss') else t)
    return out


def crop_matcher(crop):
    """Compile a WORD-BOUNDARY matcher for a crop's term family.

    Word boundaries are load-bearing, not tidiness. Naive substring matching silently
    CLEARS the very defect this scan exists to find:
        "fig"  matches "Figure 1"   -- and figure captions appear in nearly every document
        "pea"  matches "peach", "peanut"
        "bee"  matches "been", "beetle"
    A false CLEAR is worse than a false flag here, because it hides a real defect instead of
    costing a read. Caught by the term-generator test before this scan was ever trusted.
    """
    terms = crop_terms(crop)
    if not terms:
        return None
    alts = sorted((re.escape(t) for t in terms), key=len, reverse=True)
    return re.compile(r'\b(?:%s)(?:es|s|ies)?\b' % '|'.join(alts))


def cache_path(url):
    import hashlib
    return os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + '.txt')


def extract(body):
    if body[:4] == b'%PDF':
        try:
            from pypdf import PdfReader
            rd = PdfReader(io.BytesIO(body))
            return '\n'.join((p.extract_text() or '') for p in rd.pages)
        except Exception as e:
            return '\x00PDFFAIL %s' % e
    t = body.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'(?s)<[^>]+>', ' ', t)
    import html
    return html.unescape(t)


def fetch_all(urls, delay=0.7):
    os.makedirs(CACHE, exist_ok=True)
    todo = [u for u in urls if not os.path.exists(cache_path(u))]
    print('cache: %d present, %d to fetch' % (len(urls) - len(todo), len(todo)))
    for i, u in enumerate(todo, 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                txt = extract(r.read())
            status = 'OK'
        except Exception as e:
            txt = '\x00FETCHFAIL %s: %s' % (type(e).__name__, e)
            status = 'FAIL'
        with open(cache_path(u), 'w') as fh:
            fh.write(txt)
        if i % 25 == 0 or status == 'FAIL':
            print('  [%d/%d] %s %s' % (i, len(todo), status, u[:95]))
        time.sleep(delay)
    print('fetch complete')


def load_doc(url):
    p = cache_path(url)
    if not os.path.exists(p):
        return None, 'nocache'
    txt = open(p).read()
    if txt.startswith('\x00'):
        return None, txt[1:60]
    return txt.lower(), 'ok'


def candidates(data):
    """Yield (crop, node_path, {source_id: url}, claim) for crop-specific claim nodes."""
    rows = []
    for crop in data['crops']:
        slug = crop['slug']

        def walk(n, path):
            if isinstance(n, dict):
                au = n.get('anchoring_urls')
                if isinstance(au, dict) and au:
                    claim = {k: n.get(k) for k in CLAIM_KEYS
                             if isinstance(n.get(k), str) and n.get(k).strip()}
                    if claim:
                        urls = {}
                        for k, v in au.items():
                            u = v.get('url') if isinstance(v, dict) else v
                            if u:
                                urls[k] = u
                        if urls:
                            rows.append((slug, path, urls, claim))
                for k, v in n.items():
                    if k != 'anchoring_urls':
                        walk(v, path + '.' + k)
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    walk(v, '%s[%d]' % (path, i))
        walk(crop.get('regions') or {}, 'regions')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidates', action='store_true')
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--delay', type=float, default=0.7)
    args = ap.parse_args()
    if not any((args.candidates, args.fetch, args.report)):
        ap.error('pass --candidates, --fetch or --report')

    data = json.load(open(CANON))
    crops = {c['slug']: c for c in data['crops']}
    stale = sorted(set(SYNONYMS) - set(crops))
    if stale:
        print('ABORT: SYNONYMS keys not on the roster (dead entries): %s' % stale)
        return 2
    # A crop with no usable term can never be matched, so it would be flagged on EVERY node
    # -- a flood caused by the checker, not by the data. Refuse to run instead.
    empty = sorted(s for s, c in crops.items() if not crop_terms(c))
    if empty:
        print('ABORT: no match terms derived for %d crop(s): %s' % (len(empty), empty))
        return 2
    rows = candidates(data)
    pathed_urls = sorted({u for _s, _p, urls, _c in rows for u in urls.values()
                          if not BARE.match(u)})

    if args.candidates:
        print('crop-specific claim nodes with a citation : %d' % len(rows))
        print('distinct PATHED urls they cite            : %d' % len(pathed_urls))
        bare_only = sum(1 for _s, _p, urls, _c in rows
                        if all(BARE.match(u) for u in urls.values()))
        print('nodes whose sources are ALL bare hosts    : %d  (out of scope -- bare_host_scan)'
              % bare_only)
        return 0

    if args.fetch:
        fetch_all(pathed_urls, delay=args.delay)
        return 0

    # ---- report ----
    flagged, undetermined, cleared = [], [], 0
    for slug, path, urls, claim in rows:
        matcher = crop_matcher(crops[slug])
        pathed = {k: u for k, u in urls.items() if not BARE.match(u)}
        if not pathed:
            continue                      # bare-only: bare_host_scan owns it
        any_hit, any_fail, checked = False, False, 0
        for sid, u in pathed.items():
            txt, st = load_doc(u)
            if txt is None:
                any_fail = True
                continue
            checked += 1
            if matcher is not None and matcher.search(txt):
                any_hit = True
                break
        if any_hit:
            cleared += 1
        elif checked == 0:
            undetermined.append((slug, path, pathed))
        elif any_fail:
            undetermined.append((slug, path, pathed))
        else:
            flagged.append((slug, path, pathed, claim))

    print('=' * 92)
    print('DOCUMENTS THAT DO NOT MENTION THE CROP THEY ARE CITED FOR')
    print('=' * 92)
    print('  crop-specific claim nodes checked   %d' % len(rows))
    print('  cleared (a cited doc names the crop) %d' % cleared)
    print('  UNDETERMINED (fetch failed)          %d  <- never a defect' % len(undetermined))
    print('  FLAGGED                              %d' % len(flagged))
    print()

    by_pair = collections.defaultdict(list)
    for slug, path, pathed, claim in flagged:
        for sid in pathed:
            by_pair[(sid, slug)].append((path, claim))
    print('  collapsed to %d (source, crop) decisions' % len(by_pair))
    print()

    # ---- THE NARROWING: how many crops does each document name at all? ----
    #
    # The raw flag conflates two findings that need OPPOSITE treatment, and the difference is
    # measurable from the document itself:
    #
    #   CROP-LIST document (names many crops, omits yours)  -> the unr_fs0261 defect. A real
    #       planting-date table that simply does not cover this crop. REPOINT or surface.
    #   REFERENCE document (names almost no crops)          -> a frost table, chill report or
    #       weather normal. It legitimately names no crop, and citing it as the SOLE source for
    #       a per-crop window is the "backs the derivation's INPUTS, never the claim" shape
    #       (NMSU CR457B). That is a DECLARE-the-derivation finding, not a repoint.
    #
    # Without this split the scan reports 549 undifferentiated hits and reads as a flood.
    matchers = {s: crop_matcher(c) for s, c in crops.items()}
    coverage = {}
    for url in {u for _s, _p, pathed, _c in flagged for u in pathed.values()}:
        txt, _st = load_doc(url)
        coverage[url] = 0 if txt is None else sum(
            1 for m in matchers.values() if m and m.search(txt))

    CROP_LIST_MIN = 8      # names at least this many roster crops => it IS a crop list
    cls = collections.defaultdict(list)
    for slug, path, pathed, claim in flagged:
        best = max((coverage.get(u, 0) for u in pathed.values()), default=0)
        cls['CROP-LIST omits this crop' if best >= CROP_LIST_MIN
            else 'REFERENCE doc (names ~no crops)'].append((slug, path, pathed, claim, best))

    print('  SPLIT BY WHAT THE DOCUMENT ACTUALLY IS')
    print('  ' + '-' * 88)
    for k in sorted(cls):
        pairs = {(sid, s) for s, _p, pd, _c, _b in cls[k] for sid in pd}
        print('  %-34s %4d nodes / %3d (source,crop) decisions' % (k, len(cls[k]), len(pairs)))
    print()
    actionable = cls['CROP-LIST omits this crop']
    if actionable:
        print('  >>> THE ACTIONABLE CLASS: a real crop list that omits the crop citing it <<<')
        agg = collections.defaultdict(set)
        for slug, _p, pd, _c, best in actionable:
            for sid, u in pd.items():
                # Attribute ONLY to the source that is itself a crop list. Without this a
                # co-cited frost table is printed as though it were the omitting document.
                if coverage.get(u, 0) >= CROP_LIST_MIN:
                    agg[(sid, coverage[u])].add(slug)
        for (sid, cov), slugs in sorted(agg.items(), key=lambda x: -len(x[1])):
            print('    %-26s names %3d crops, but NOT these %d: %s'
                  % (sid, cov, len(slugs), ', '.join(sorted(slugs)[:9])))
    print()
    bysrc = collections.Counter(sid for sid, _ in by_pair)
    print('  %-26s %6s  %s' % ('source id', 'crops', 'example url'))
    print('  ' + '-' * 88)
    for sid, n in bysrc.most_common():
        ex = next(u for slug, path, pathed, claim in flagged for k, u in pathed.items() if k == sid)
        print('  %-26s %6d  %s' % (sid, n, ex[:56]))
    print()
    print('  READ THESE, DO NOT COUNT THEM. A document can legitimately support a claim')
    print('  without naming the crop (a frost table, a chill report). This check only fires')
    print('  when NO cited document names it, which is the strong case -- but adjudicate.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
