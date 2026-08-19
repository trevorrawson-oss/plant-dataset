#!/usr/bin/env python3
"""PLA-220 -- export the COMPLETE borderline (6-7 shared word) frame, roster-wide.

Why this exists: `verbatim_scan.py` classifies a (prose field, source URL) pair as
borderline when it shares a 6- or 7-word consecutive run with the cited document but
no 8-word run (the HARD floor). Roster-wide that population is ~2.4k pairs and NONE of
it is adjudicated. PLA-220's deliverable is the SELECTION RULE over that population --
which is why this exporter draws the WHOLE frame and applies no sample, no filter, no
rank and no dedupe. A pre-filtered export would inherit a selection nobody wrote down
(INSTANCE 8's worklist-derivation problem), so the filtering happens downstream of a
written rule, never here.

THE ONE EXCLUSION, and it is deliberate and named: the 22 fields rewritten under
PLA-202 (tools/staging/pla202_rewrites.json) are dropped so this frame cannot collide
with completed work. Every dropped record is itemized in the manifest -- an exclusion
that cannot show its own contents is indistinguishable from a filter.

CLASSIFICATION IS verbatim_scan's, NOT A REIMPLEMENTATION OF IT. The prose collection
rules (BACKEND_KEYS, the >=40-char floor, the backend path substrings), the
normalization, the coverage floor and the hard/borderline split are lifted from that
tool byte-for-byte. The only change is the direction of the n-gram comparison: this
exporter inverts it (prose n-grams into a dict, source words streamed against it) so
it can attribute WHICH run matched WHERE in the document without holding every source's
n-gram set in memory. Equivalence with the shipped tool is asserted by
tools/test_pla220_borderline_frame.py, which diffs (path, url, first-6gram) over all
128 crops against verbatim_scan's own stdout.

WHAT A RECORD CARRIES (one record per borderline (field, URL) pair -- the same unit
verbatim_scan counts):
  crop_slug, field_path            -- where our prose lives
  our_prose                        -- the COMPLETE field value, never the matched span alone
  run_normalized / run_in_our_prose-- the maximal shared run, as matched and as written
  run_words                        -- 6 or 7, by construction
  all_maximal_runs                 -- every run at that length, not just the first
  source_id(s) / source_url        -- the document, by catalog id and URL
  source_context                   -- +/- one sentence around the run in the cached document

COVERAGE IS PART OF THE FRAME. A borderline count taken over documents that were never
read is understated, so the manifest records every uncovered URL and its reason per crop.
Do not quote the record count without the coverage figure beside it.

Usage:
  python3 tools/pla220_borderline_frame.py [--out=DIR] [--cache=DIR] [--data=PATH]
Writes DIR/<slug>.json shards, DIR/_all_records.jsonl, and DIR/_manifest.json.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from doc_mentions_crop_scan import unreadable_reason  # noqa: E402

flags = [a for a in sys.argv[1:] if a.startswith("--")]
OUT = os.path.join(HERE, "staging", "pla220_borderline_frame")
CACHE = os.path.join(HERE, ".doc_cache")
DATA = "crops_data_final.json"
EXCL = os.path.join(HERE, "staging", "pla202_rewrites.json")
for f in flags:
    if f.startswith("--out="):
        OUT = f.split("=", 1)[1]
    elif f.startswith("--cache="):
        CACHE = f.split("=", 1)[1]
    elif f.startswith("--data="):
        DATA = f.split("=", 1)[1]

# ---------------------------------------------------------------- verbatim_scan parity
# Lifted from tools/verbatim_scan.py. If that tool's layer classification changes, this
# must change with it -- the test asserts they agree, so drift fails loudly.
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
NORM_RE = re.compile(r"[^a-z0-9°\s]")


def norm_words(text):
    return NORM_RE.sub(" ", text.lower()).split()


def collect_prose(crop):
    """verbatim_scan's user-facing prose walk, in its own path notation."""
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
    return prose


def collect_urls(crop):
    """URL -> {source_ids, anchor_paths}. verbatim_scan keeps only the URL set; the
    frame needs the citing id too, so the walk records the key it was found under."""
    found = {}

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if k.endswith("anchoring_urls") and isinstance(v, dict):
                    for sid, e in v.items():
                        if isinstance(e, dict) and e.get("url"):
                            rec = found.setdefault(e["url"], {"source_ids": set(),
                                                             "anchor_paths": set()})
                            rec["source_ids"].add(sid)
                            rec["anchor_paths"].add(f"{p}.{sid}")
                walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]")

    walk(crop, "")
    return found


# ------------------------------------------------------------- offset-preserving words
def words_with_spans(text):
    """(words, spans) where spans index back into `text`.

    norm_words' substitution is length-preserving (each stripped char becomes ONE
    space), so offsets in the normalized string are offsets in the source string --
    which is what lets a matched run be quoted as it was actually WRITTEN (case and
    punctuation intact) rather than only in its normalized form. str.lower() is
    length-preserving for every character in this corpus but not in Unicode generally
    (U+0130 is the classic counterexample), so the caller is told when it is not and
    falls back to the normalized text rather than slicing at wrong offsets.
    """
    low = text.lower()
    aligned = len(low) == len(text)
    flat = NORM_RE.sub(" ", low)
    words, spans = [], []
    for m in re.finditer(r"\S+", flat):
        words.append(m.group(0))
        spans.append((m.start(), m.end()))
    return words, spans, aligned


SENT_BOUND = re.compile(r"[.!?]\s+")
MIN_SIDE = 80   # chars of context each side before a boundary is allowed to trim
PAD = 420       # chars of raw window each side before trimming


def context_around(text, start, end):
    """One or two sentences either side of [start,end) in `text`.

    Expands OUTWARD from the known character span and only ever trims the
    padding, so the run is contained by construction. The earlier version
    re-located the run by string search inside a sentence-split chunk, which
    silently lost it on three records: the binomial `Fusarium oxysporum f. sp.
    lycopersici` splits into three "sentences" at the abbreviation points, and
    the +/- 1 sentence window then cut the run in half. Containment must be
    structural, not something the extractor hopes for -- a context that does not
    hold its own run is an adjudicator reading the wrong paragraph. MIN_SIDE
    keeps abbreviation-dense text (`f. sp.`, `spp.`, `var.`) from trimming down
    to a uselessly tight window.
    """
    lo = max(0, start - PAD)
    hi = min(len(text), end + PAD)
    left = [m.end() for m in SENT_BOUND.finditer(text[lo:start])]
    left = [b for b in left if (start - (lo + b)) >= MIN_SIDE]
    if left:
        lo += left[-1]
    right = [m.end() for m in SENT_BOUND.finditer(text[end:hi])]
    right = [b for b in right if b >= MIN_SIDE]
    if right:
        hi = end + right[0]
    return " ".join(text[lo:hi].split())


def ngrams_index(words, n):
    """ngram -> list of start positions."""
    idx = {}
    for i in range(len(words) - n + 1):
        idx.setdefault(" ".join(words[i:i + n]), []).append(i)
    return idx


# --------------------------------------------------------------------------- exclusion
excl_raw = json.load(open(EXCL))
EXCLUDED = {(slug, path) for slug, fields in excl_raw.items() for path in fields}

data = json.load(open(DATA))
catalog = data.get("source_catalog", {})

os.makedirs(OUT, exist_ok=True)

manifest = {
    "issue": "PLA-220",
    "canonical_sha": hashlib.sha256(open(DATA, "rb").read()).hexdigest(),
    "data_path": DATA,
    "cache_dir": os.path.relpath(CACHE, HERE),
    "definition": ("one record per (user-facing prose field, cited source URL) pair "
                   "sharing a 6- or 7-word consecutive normalized run with the cached "
                   "document and NO 8-word run; the unit verbatim_scan counts as "
                   "'Borderline (6-7 words)'"),
    "selection_applied": "NONE -- complete frame; no sample, filter, rank or dedupe",
    "exclusion_applied": ("the 22 fields rewritten under PLA-202 "
                          "(tools/staging/pla202_rewrites.json), itemized below"),
    "pla202_excluded_fields": sorted(f"{s}::{p}" for s, p in EXCLUDED),
    "crops": {},
    "totals": {},
}

all_records = []
excluded_hits = []
hard_total = 0

for crop in sorted(data["crops"], key=lambda c: c["slug"]):
    slug = crop["slug"]
    prose = collect_prose(crop)
    urlinfo = collect_urls(crop)
    URLS = sorted(urlinfo)

    # --- source coverage, on verbatim_scan's exact rules ---
    covered, uncovered = {}, []
    for u in URLS:
        p = os.path.join(CACHE, hashlib.sha1(u.encode()).hexdigest() + ".txt")
        if not os.path.exists(p):
            uncovered.append({"url": u, "reason": "not fetched"})
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        reason = unreadable_reason(txt)
        if reason is not None:
            uncovered.append({"url": u, "reason": reason})
            continue
        w = norm_words(txt)
        if len(w) < 50:
            uncovered.append({"url": u,
                              "reason": f"only {len(w)} words extracted (JS-rendered?)"})
            continue
        covered[u] = (txt, p)

    # --- prose n-gram index, inverted: ngram -> [prose row ids] ---
    prose_meta = []
    idx = {6: {}, 7: {}, 8: {}}
    for pid, (path, text) in enumerate(prose):
        w, spans, aligned = words_with_spans(text)
        prose_meta.append({"path": path, "text": text, "words": w,
                           "spans": spans, "aligned": aligned})
        if len(w) < 6:
            continue
        for n in (6, 7, 8):
            if len(w) < n:
                continue
            for i in range(len(w) - n + 1):
                idx[n].setdefault(" ".join(w[i:i + n]), []).append((pid, i))

    # --- stream each covered document against the prose index ---
    # hits[(pid, url)][n] = {ngram: [source word positions]}
    hits = {}
    doc_words = {}
    for u, (txt, _) in covered.items():
        sw, sspans, saligned = words_with_spans(txt)
        doc_words[u] = (sw, sspans, saligned, txt)
        for n in (6, 7, 8):
            if len(sw) < n:
                continue
            for j in range(len(sw) - n + 1):
                g = " ".join(sw[j:j + n])
                rows = idx[n].get(g)
                if not rows:
                    continue
                for pid, _i in rows:
                    hits.setdefault((pid, u), {}).setdefault(n, {}).setdefault(g, []).append(j)

    # --- classify exactly as verbatim_scan does ---
    crop_records = []
    crop_hard = 0
    for (pid, u), byn in sorted(hits.items(), key=lambda kv: (prose[kv[0][0]][0], kv[0][1])):
        if byn.get(8):
            crop_hard += 1
            continue
        if not byn.get(6):
            continue
        run_words = 7 if byn.get(7) else 6
        pm = prose_meta[pid]
        path = pm["path"]

        if (slug, path) in EXCLUDED:
            excluded_hits.append({"crop_slug": slug, "field_path": path,
                                  "source_url": u, "run_words": run_words})
            continue

        maximal = sorted(byn[run_words])
        chosen = maximal[0]
        # verbatim_scan prints sorted(p6 & SRC6)[0]; carried for equivalence diffing.
        tool_gram = sorted(byn[6])[0]

        # the run as WRITTEN in our prose (first occurrence)
        occ = idx[run_words][chosen]
        our_i = next(i for (q, i) in occ if q == pid)
        if pm["aligned"] and pm["spans"]:
            s0 = pm["spans"][our_i][0]
            s1 = pm["spans"][our_i + run_words - 1][1]
            run_in_prose = pm["text"][s0:s1]
        else:
            run_in_prose = chosen

        # source context around the first occurrence of the run in the document
        sw, sspans, saligned, stxt = doc_words[u]
        j = byn[run_words][chosen][0]
        if saligned and sspans:
            c0, c1 = sspans[j][0], sspans[j + run_words - 1][1]
            ctx = context_around(stxt, c0, c1)
        else:
            ctx = ""

        info = urlinfo[u]
        sids = sorted(info["source_ids"])
        crop_records.append({
            "crop_slug": slug,
            "field_path": path,
            "our_prose": pm["text"],
            "run_normalized": chosen,
            "run_in_our_prose": run_in_prose,
            "run_words": run_words,
            "all_maximal_runs": maximal,
            "maximal_run_count": len(maximal),
            "source_ids": sids,
            # `name` is on all 208 catalog entries; `title` is on 101, so reading
            # `title` returned null for most records -- a field that looks present
            # and carries nothing.
            "source_names": [catalog[s]["name"] for s in sids
                             if isinstance(catalog.get(s), dict) and "name" in catalog[s]],
            "source_publishers": [catalog[s].get("publisher") for s in sids
                                  if isinstance(catalog.get(s), dict)],
            "source_tiers": [catalog[s].get("tier") for s in sids
                             if isinstance(catalog.get(s), dict)],
            "source_url": u,
            "anchor_paths": sorted(info["anchor_paths"]),
            "source_context": ctx,
            "source_context_available": bool(ctx),
            "tool_first_6gram": tool_gram,
        })

    hard_total += crop_hard
    all_records.extend(crop_records)
    manifest["crops"][slug] = {
        "records": len(crop_records),
        "hard_hits_skipped": crop_hard,
        "prose_strings_scanned": len(prose),
        "sources_text_compared": len(covered),
        "sources_cited": len(URLS),
        "uncovered": uncovered,
        "shard": f"{slug}.json" if crop_records else None,
    }
    if crop_records:
        with open(os.path.join(OUT, f"{slug}.json"), "w", encoding="utf-8") as fh:
            json.dump({"crop_slug": slug, "record_count": len(crop_records),
                       "records": crop_records}, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

with open(os.path.join(OUT, "_all_records.jsonl"), "w", encoding="utf-8") as fh:
    for r in all_records:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

manifest["totals"] = {
    "records_exported": len(all_records),
    "pla202_excluded_hits": len(excluded_hits),
    "borderline_before_exclusion": len(all_records) + len(excluded_hits),
    "hard_hits_skipped": hard_total,
    "crops_total": len(data["crops"]),
    "crops_with_records": sum(1 for v in manifest["crops"].values() if v["records"]),
    "sources_cited_total": sum(v["sources_cited"] for v in manifest["crops"].values()),
    "sources_uncovered_total": sum(len(v["uncovered"]) for v in manifest["crops"].values()),
    "crops_with_uncovered_sources": sum(1 for v in manifest["crops"].values() if v["uncovered"]),
    "records_missing_source_context": sum(1 for r in all_records if not r["source_context"]),
}
manifest["pla202_excluded_hits"] = excluded_hits

with open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

t = manifest["totals"]
print(f"PLA-220 borderline frame -> {OUT}")
print(f"  records exported:            {t['records_exported']}")
print(f"  PLA-202 excluded hits:       {t['pla202_excluded_hits']}")
print(f"  borderline before exclusion: {t['borderline_before_exclusion']}")
print(f"  HARD hits skipped (>=8):     {t['hard_hits_skipped']}")
print(f"  crops with records:          {t['crops_with_records']}/{t['crops_total']}")
print(f"  source coverage:             {t['sources_cited_total'] - t['sources_uncovered_total']}"
      f"/{t['sources_cited_total']} cited URLs read "
      f"({t['sources_uncovered_total']} uncovered across {t['crops_with_uncovered_sources']} crops)")
print(f"  records without source context: {t['records_missing_source_context']}")
