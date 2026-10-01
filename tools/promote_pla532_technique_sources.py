#!/usr/bin/env python3
"""PLA-532: admit the container and vertical TECHNIQUE sources to source_catalog. Base 00dda31c.

The content, the claim-class measurement, the new-id-vs-widen decision, the verbatim quotes and the
rejections: build_pla532_catalog_content.

WHAT MOVES. `source_catalog` gains EXACTLY the 8 declared document-scoped ids. NOTHING ELSE: no crop,
no crop-level sources array, no existing catalog entry, no other top-level key. This is the first
canonical write of the PLA-10 arc and it is catalog only; promote 2 does the citing.

--------------------------------------------------------------------------------------------------
THE GUARDS (one family each; the suite drives every one, the harness mutates every one)
--------------------------------------------------------------------------------------------------
  0. ENTRY. The canonical's sha256 must be BASE_SHA.
  1. SPEC SHAPE. Exactly EXPECTED_NEW_SOURCES ids, and the four content tables (CATALOG_NEW,
     EVIDENCE, QUOTES, CLAIM_CLASS) name the SAME ids (set equality, checked before any value).
     Every entry carries exactly the standard key set, its `id` equals its key, and every claim
     class is one of A/B/C/D.
  2. ENTRY VALIDITY. Each new entry is T1, trust_tier high, university_extension, accessed on the
     admission date, titled (non-empty), with a non-empty citable_for; its url is https, pathed, and
     NOT bare by bare_host_gate.is_bare (imported, never retyped: the A63 predicate), and equals its
     EVIDENCE url.
  3. PRE-STATE. No declared id already exists (an admission must never overwrite), and no existing
     catalog entry already carries the same url (one document, one id).
  4. EVIDENCE (promote-time, against the local caches). Each document's raw bytes are present in
     tools/.evidence_cache with the recorded sha256 and a MANIFEST.tsv row naming that digest and
     url; every QUOTES sentence is present in the cached text of its document. A missing cache
     REFUSES: an admission whose evidence cannot be re-read is not admitted.
  5. POST-STATE. set(pre catalog) is a subset of set(post catalog) and the difference is EXACTLY the
     declared ids (checked as sets BEFORE any value comparison, so an addition in post is never
     invisible); every pre entry is byte-identical; every other top-level key is byte-identical; the
     crop list is byte-identical; A54 (`source_catalog_title_gate.title_violations`, imported) is
     clean on the post catalog; and no crop cites a new id.

REFUSALS print `REFUSED:` and exit non-zero; the canonical is written only with --apply.

Guard suite:      tools/test_promote_pla532_technique_sources.py
Mutation harness: tools/mutate_pla532_technique_sources_suite.py (PLA-215)
"""
import argparse
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
EVIDENCE_DIR = os.path.join(HERE, ".evidence_cache")

from bare_host_gate import is_bare  # noqa: E402  -- A63's predicate, imported never retyped
from source_catalog_title_gate import title_violations  # noqa: E402  -- A54, imported never retyped

BASE_SHA = "00dda31cc6616b9ea865f04fe0ce97fb1fb5d821f0c94724d3a03dbad8c8dd8e"
EXPECTED_NEW_SOURCES = 8
EXPECTED_PRE_CATALOG = 221
CLAIM_CLASSES = {"A", "B", "C", "D"}
ENTRY_KEYS = {"id", "name", "title", "publisher", "url", "source_class", "trust_tier", "accessed",
              "tier", "citable_for", "_admission_provenance"}


def content():
    import build_pla532_catalog_content as C
    return C


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """The canonical's compact form: no indent, no trailing newline, UTF-8 unescaped."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def norm(s):
    return " ".join(s.replace(" ", " ").split())


def staged():
    C = content()
    return {"catalog_new": copy.deepcopy(C.CATALOG_NEW), "evidence": copy.deepcopy(C.EVIDENCE),
            "quotes": copy.deepcopy(C.QUOTES), "claim_class": copy.deepcopy(C.CLAIM_CLASS),
            "accessed": C.ACCESSED}


def check_base(blob):
    got = sha256_bytes(blob)
    if got != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical sha256 {got[:8]} is not the base {BASE_SHA[:8]}; re-measure before running")
    return got


def check_spec_shape(spec):
    new = spec["catalog_new"]
    if len(new) != EXPECTED_NEW_SOURCES:
        raise SystemExit(f"REFUSED: spec admits {len(new)} catalog ids, expected {EXPECTED_NEW_SOURCES}")
    ids = set(new)
    for name in ("evidence", "quotes", "claim_class"):
        if set(spec[name]) != ids:
            raise SystemExit(f"REFUSED: {name} names {sorted(set(spec[name]) ^ ids)} that catalog_new does not (or vice versa)")
    for sid, e in new.items():
        if set(e) != ENTRY_KEYS:
            raise SystemExit(f"REFUSED: {sid} key set differs from the entry shape: {sorted(set(e) ^ ENTRY_KEYS)}")
        if e["id"] != sid:
            raise SystemExit(f"REFUSED: {sid} carries id {e['id']!r}")
        cls = spec["claim_class"][sid]
        if not cls or not set(cls) <= CLAIM_CLASSES:
            raise SystemExit(f"REFUSED: {sid} claim class {cls!r} is empty or outside A/B/C/D")
        if not spec["quotes"][sid]:
            raise SystemExit(f"REFUSED: {sid} pins no verbatim quote")
    return len(new)


def check_entries(spec):
    for sid, e in spec["catalog_new"].items():
        url = e["url"]
        if not (isinstance(url, str) and url.startswith("https://")):
            raise SystemExit(f"REFUSED: {sid} url is not https: {url!r}")
        if is_bare(url):
            raise SystemExit(f"REFUSED: {sid} url is a bare host or site root (A63): {url!r}")
        if url != spec["evidence"][sid]["url"]:
            raise SystemExit(f"REFUSED: {sid} url is not the url its evidence was fetched from")
        if e["tier"] != "T1" or e["trust_tier"] != "high" or e["source_class"] != "university_extension":
            raise SystemExit(f"REFUSED: {sid} is not a T1 high-trust university_extension source")
        if e["accessed"] != spec["accessed"]:
            raise SystemExit(f"REFUSED: {sid} accessed {e['accessed']!r} is not the admission date")
        if not (isinstance(e["title"], str) and e["title"].strip()):
            raise SystemExit(f"REFUSED: {sid} has no title read off the document (A54)")
        if not (isinstance(e["citable_for"], str) and e["citable_for"].strip()):
            raise SystemExit(f"REFUSED: {sid} has no citable_for")
    return len(spec["catalog_new"])


def check_pre_state(spec, data):
    sc = data["source_catalog"]
    if len(sc) != EXPECTED_PRE_CATALOG:
        raise SystemExit(f"REFUSED: pre catalog has {len(sc)} ids, expected {EXPECTED_PRE_CATALOG}; re-measure before running")
    urls = {v.get("url"): k for k, v in sc.items()}
    for sid, e in spec["catalog_new"].items():
        if sid in sc:
            raise SystemExit(f"REFUSED: catalog id {sid!r} already exists; this would overwrite it")
        if e["url"] in urls:
            raise SystemExit(f"REFUSED: {sid} url is already catalogued as {urls[e['url']]!r}")
    return len(sc)


def manifest_rows(path=None):
    path = path or os.path.join(EVIDENCE_DIR, "MANIFEST.tsv")
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    return {tuple(ln.split("\t")[i] for i in (0, 4)) for ln in lines[1:] if ln.strip()}


def cached_text(url):
    import doc_mentions_crop_scan as D
    p = D.cache_path(url)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def check_evidence(spec, evidence_dir=None, manifest=None, text_of=cached_text):
    evidence_dir = evidence_dir or EVIDENCE_DIR
    rows = manifest_rows(manifest) if manifest is not False else set()
    for sid, ev in spec["evidence"].items():
        f = os.path.join(evidence_dir, f"{ev['sha256']}.{ev['ext']}")
        if not os.path.exists(f):
            raise SystemExit(f"REFUSED: {sid} raw bytes absent from the evidence cache ({ev['sha256'][:12]})")
        with open(f, "rb") as fh:
            got = sha256_bytes(fh.read())
        if got != ev["sha256"]:
            raise SystemExit(f"REFUSED: {sid} cached bytes hash {got[:12]}, recorded {ev['sha256'][:12]}")
        if (ev["sha256"], ev["url"]) not in rows:
            raise SystemExit(f"REFUSED: {sid} has no MANIFEST.tsv row for its digest and url")
        text = text_of(ev["url"])
        if text is None:
            raise SystemExit(f"REFUSED: {sid} has no cached text to check its quotes against")
        body = norm(text)
        for q in spec["quotes"][sid]:
            if norm(q) not in body:
                raise SystemExit(f"REFUSED: {sid} quote not on the page: {q[:70]!r}")
    return sum(len(q) for q in spec["quotes"].values())


def apply_to(data, spec):
    out = copy.deepcopy(data)
    for sid, e in spec["catalog_new"].items():
        out["source_catalog"][sid] = copy.deepcopy(e)
    return out


def cites(crop, ids):
    """Every catalog id this crop names anywhere: `sources`/`*_sources` lists and anchor-dict keys."""
    hit = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if (k == "sources" or k.endswith("_sources")) and isinstance(v, list):
                    hit.update(x for x in v if x in ids)
                elif (k == "anchoring_urls" or k.endswith("_anchoring_urls")) and isinstance(v, dict):
                    hit.update(x for x in v if x in ids)
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(crop)
    return hit


def verify_post(pre, post, spec):
    declared = set(spec["catalog_new"])
    psc, qsc = pre["source_catalog"], post["source_catalog"]
    if not set(psc) <= set(qsc):
        raise SystemExit(f"REFUSED: source_catalog DROPPED {sorted(set(psc) - set(qsc))}")
    added = set(qsc) - set(psc)
    if added != declared:
        raise SystemExit(f"REFUSED: source_catalog gained {sorted(added)}, declared {sorted(declared)}")
    for k in psc:
        if json.dumps(psc[k], sort_keys=True, ensure_ascii=False) != json.dumps(qsc[k], sort_keys=True, ensure_ascii=False):
            raise SystemExit(f"REFUSED: existing catalog entry {k!r} changed")
    if set(pre) != set(post):
        raise SystemExit(f"REFUSED: top-level keys changed: {sorted(set(pre) ^ set(post))}")
    for k in pre:
        if k == "source_catalog":
            continue
        if serialize(pre[k]) != serialize(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    tv = title_violations(qsc)
    if tv:
        raise SystemExit(f"REFUSED: A54 on the post catalog: {tv[:3]}")
    for c in post["crops"]:
        hit = cites(c, declared)
        if hit:
            raise SystemExit(f"REFUSED: {c.get('slug')} cites {sorted(hit)}; this promote admits, it does not cite")
    return len(added)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", default=CANON)
    ap.add_argument("--apply", action="store_true", help="write the post-state over the canonical")
    ap.add_argument("--out", default=None, help="write the post-state HERE (canonical untouched)")
    ap.add_argument("--expect-sha", default=None)
    args = ap.parse_args(argv)

    with open(args.canonical, "rb") as f:
        blob = f.read()
    check_base(blob)
    data = json.loads(blob)
    spec = staged()

    n = check_spec_shape(spec)
    print(f"  spec shape       {n} ids; catalog_new, evidence, quotes, claim_class name the same set")
    check_entries(spec)
    print("  entries          all T1, titled, pathed https, not bare (A63 predicate), url == fetched url")
    n = check_pre_state(spec, data)
    print(f"  pre-state        {n} catalog ids; none declared exists; no url already catalogued")
    n = check_evidence(spec)
    print(f"  evidence         raw bytes + MANIFEST row per document; {n} quotes found on their pages")
    post = apply_to(data, spec)
    n = verify_post(data, post, spec)
    print(f"  post-state       +{n} catalog ids, nothing else moved; A54 clean; no crop cites a new id")

    out = serialize(post)
    new_sha = sha256_bytes(out)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        raise SystemExit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.out:
        with open(args.out, "wb") as f:
            f.write(out)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
    elif args.apply:
        with open(args.canonical, "wb") as f:
            f.write(out)
        print(f"  WROTE {args.canonical}")
    else:
        print("  dry run: nothing written (pass --apply or --out)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
