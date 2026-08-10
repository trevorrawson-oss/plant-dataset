#!/usr/bin/env python3
"""Copyright/verbatim scan -- flip-blocking Step 11 criterion, crop-agnostic.

Ported from the M15 lettuce Step 11 run (2026-06-05), where the first
systematic run caught a 10-word verbatim lift (s11_finding_002) that a Step 10
spot-check had passed because it compared against the wrong source. Systematic
beats spot-check; this tool is the systematic version.

Method: compare every user-facing prose string on the crop against the text of
every anchoring URL the crop cites, by shared consecutive-word run.
  >= 8 shared words  -> HARD hit (flip-blocking until adjudicated)
  6-7 shared words   -> borderline (report; citations/attributions/universal
                        facts/numeric conventions are typically benign-class)
Adjudication notes from the lettuce run: `.provenance.` paths are BACKEND
(excluded here); generic numeric horticultural conventions can be ruled benign
(s11_finding_003 precedent) -- but route the ruling to the voice lane, do not
self-dismiss.

Usage (the cache is tools/.doc_cache, SHARED with doc_mentions_crop_scan /
bloom_datum_scan / cited_claim_scan -- one fetch layer, whose extractor handles
PDFs via pypdf and stores extracted text keyed sha1(url).txt):
  1. python3 tools/verbatim_scan.py <slug> --urls     # print URL list
  2. python3 tools/verbatim_scan.py <slug> --fetch    # populate the shared cache
  3. python3 tools/verbatim_scan.py <slug> [--cache=DIR]   # run the scan
Unreadable URLs (unfetched, fetch failures, WAF challenge pages, PDFs with no
text layer) are listed as NOT COVERED -- state coverage honestly, never silently
truncate.

THE COVERAGE FLOOR (PLA-160). Until 2026-08-10 this scan read an always-empty
cache (/tmp/verbatim_cache, a retired .body/.meta format), printed
`sources text-compared: 0/N` on line one, and exited 0 -- a flip-blocking
criterion that never blocked, because the verdict ignored its own coverage
figure. A zero-hit verdict is now reportable ONLY when at least one source was
compared and none is uncovered.
Exit contract:
  0  no HARD hits AND full coverage (len(sources) > 0 and len(uncovered) == 0)
  1  HARD hit(s) found -- adjudication owed before any flip
  2  COVERAGE INSUFFICIENT -- a zero over an unmeasured population is not a verdict
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from doc_mentions_crop_scan import fetch_all, unreadable_reason  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
if not args:
    print(__doc__)
    sys.exit(2)
SLUG = args[0]
PATH = args[1] if len(args) > 1 else "crops_data_final.json"
CACHE = os.path.join(HERE, ".doc_cache")
for f in flags:
    if f.startswith("--cache="):
        CACHE = f.split("=", 1)[1]

data = json.load(open(PATH))
matches = [c for c in data["crops"] if c.get("slug") == SLUG]
assert len(matches) == 1, f"slug {SLUG!r}: {len(matches)} matches"
crop = matches[0]

# ---- URL inventory (every anchoring entry incl. sibling-named dicts) ----
urls = set()

def url_walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("anchoring_urls") and isinstance(v, dict):
                for sid, e in v.items():
                    if isinstance(e, dict) and e.get("url"):
                        urls.add(e["url"])
            url_walk(v)
    elif isinstance(o, list):
        for x in o:
            url_walk(x)

url_walk(crop)
URLS = sorted(urls)
if "--urls" in flags:
    for u in URLS:
        print(u)
    sys.exit(0)
if "--fetch" in flags:
    fetch_all(URLS)
    sys.exit(0)

# ---- user-facing prose collection (Step 9 layer classification) ----
BACKEND_KEYS = {
    "id","slug","stage_id","tip_id","region_id","evidence_tier","added_in",
    "last_reviewed","last_reviewed_session","last_operation","last_session",
    "schema_version","last_updated","date","stored_date","resolution_tier",
    "resolution_method","anchor_threshold","fallback_beyond_horizon",
    "calendar_state","window_type","timing_relative","phase","status","image",
    "plantings_provenance","provenance","lifted_from_zone","botanical_name",
    "family","calendar_basis","resolution_source","from","from_year_round_note",
    "url","verified","accessed","publisher","source_class","source_note",
    "verification_log_ref","filing_record","disposition","scope","session",
    "field","assigned_to","deferred_to","last_audited","resolution_note",
    "filed_in","filed_in_session","resolved_in","resolved_by","note_internal",
    "synthesis_note","synthesis_note_seasoned","design_note","design_note_seasoned",
    "source_quote","source_quote_seasoned","zone_coverage_note",
    "zone_coverage_note_seasoned","uscrn_validation","classification",
    "source","source_id","claim","tier","trust_tier","citable_for","archetype",
    "succession_id","track","added_by","sources_summary","description_sources",
}
BACKEND_PATH_SUBSTR = ("plantings_provenance", "verification_status",
                       "anchoring_urls", ".provenance", "uscrn_validation")
BACKEND_KEY_RE = re.compile(r"zone_\d+_")

prose = []

def collect(o, pat):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{pat}.{k}" if pat else k
            if (isinstance(v, str) and len(v) >= 40 and k not in BACKEND_KEYS
                    and not BACKEND_KEY_RE.match(k) and not k.endswith("_sources")
                    and not any(s in pat for s in BACKEND_PATH_SUBSTR)):
                prose.append((p, v))
            collect(v, p)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            collect(x, f"{pat}[{i}]")

collect(crop, "")

# ---- source text (the shared cache stores extracted text, PDFs already through pypdf) ----
def norm_words(text):
    return re.sub(r"[^a-z0-9°\s]", " ", text.lower()).split()

sources, uncovered = {}, []
for u in URLS:
    p = os.path.join(CACHE, hashlib.sha1(u.encode()).hexdigest() + ".txt")
    if not os.path.exists(p):
        uncovered.append((u, "not fetched")); continue
    txt = open(p, encoding="utf-8", errors="replace").read()
    reason = unreadable_reason(txt)
    if reason is not None:
        uncovered.append((u, reason)); continue
    w = norm_words(txt)
    if len(w) < 50:
        uncovered.append((u, f"only {len(w)} words extracted (JS-rendered?)")); continue
    sources[u] = w

def ngrams(words, n):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}

SRC8 = {u: ngrams(w, 8) for u, w in sources.items()}
SRC6 = {u: ngrams(w, 6) for u, w in sources.items()}

hard, borderline = [], []
for path, text in prose:
    w = norm_words(text)
    if len(w) < 6:
        continue
    p8 = ngrams(w, 8) if len(w) >= 8 else set()
    p6 = ngrams(w, 6)
    for u in sources:
        if p8 & SRC8[u]:
            hard.append((path, u, sorted(p8 & SRC8[u])[0]))
        elif p6 & SRC6[u]:
            borderline.append((path, u, sorted(p6 & SRC6[u])[0]))

print(f"crop: {SLUG} | prose strings scanned: {len(prose)} | sources text-compared: {len(sources)}/{len(URLS)}")
print(f"\nHARD hits (>=8-word shared run) -- adjudication owed before any flip: {len(hard)}")
for path, u, g in hard:
    print(f"  {path}\n    vs {u}\n    shared: \"{g}...\"")
print(f"\nBorderline (6-7 words): {len(borderline)}")
for path, u, g in borderline:
    print(f"  {path}  vs {u}  \"{g}\"")
print(f"\nNOT COVERED ({len(uncovered)}):")
for u, r in uncovered:
    print(f"  {r}: {u}")

if hard:
    sys.exit(1)
# The coverage floor: a zero-hit verdict over an unmeasured population is not a verdict.
if not sources or uncovered:
    print(f"\nverbatim_scan COVERAGE INSUFFICIENT: compared {len(sources)} of {len(URLS)} "
          f"sources -- 'HARD hits: 0' is NOT reportable as verbatim-clean. "
          f"Fetch the uncovered URLs (--fetch) or adjudicate them before any flip.")
    sys.exit(2)
sys.exit(0)
