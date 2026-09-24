#!/usr/bin/env python3
"""promote_pla581_critical_warnings -- PLA-581 / PLA-7 Plan D, `critical_warnings` + `container_safety`
(spec docs/superpowers/specs/2026-09-21-pla581-critical-warnings-field-shape.md; register row 32).
Base 526788f2 (PLA-580's plants_per_pot landing).

WHAT MOVES.
  * On every one of the 121 CERTIFIED crops, one new top-level crop key: `critical_warnings: null`,
    meaning NOT ASSESSED. Not `[]`, which would assert "assessed, none found" for PLA-142's harvest
    class on crops nobody has assessed -- an unsourced negative (ruling 2). null needs no record.
  * One new top-level DATASET key, `container_safety`: the 3 crop-invariant container warnings
    that survived the section 4.5 evidence test (balcony_load, container_material,
    hanging_security), each with its own T1 sources, plus one provenance record per warning.
  * The 7 uncertified shells are NOT touched and stay byte-identical. Nothing else moves: no crop
    carries a field_additions entry from this pass, because null is not a claim.

WHY EACH GUARD EXISTS.
 1. THE SPEC IS THE SHAPE THAT WAS RULED. base_sha and fetch_date pinned; the warning ids (in
    order), severity, stage, class, sources and anchor urls compared to INDEPENDENT LITERALS; the
    title and body copy compared to the APPROVED SPEC DOCUMENT's section 14 (amendment 3, which
    supersedes 4.4's bodies; 4.4 itself stays byte for byte), re-read at run time, so the builder
    cannot validate its own copy; the titles ALSO pinned as literals. The canonical write REFUSES
    while any staged title is a placeholder (pending_titles), so interim wording can never ship.
 2. THE CUTS ARE A DECISION. The spec's three cut candidates are recorded in a `cut` ledger with
    reasons; a ledger that is not exactly those three, or carries a blank reason, REFUSES.
 3. EVERY DIGEST IS MEASURED, AND AGAINST ITS OWN PAGE. Each page's sha256 is compared to
    EVIDENCE_HASHES keyed by URL (a set would miss two pages' digests swapped); each record must
    name every page its warning rests on, quote that page's measured digest, and quote EVERY
    sentence in EVIDENCE for that warning (a warning can rest on several sentences and pages); and no
    64-hex token anywhere in the staged artifact may be other than a measured digest or the base.
 4. THE WARNINGS PASS THE GATE BEFORE THEY ARE WRITTEN: critical_warnings_gate.dataset_violations
    (imported, never retyped) with presence ON, on a synthetic dataset carrying the object.
 5. THE BASE CARRIES NEITHER KEY and no critical_warnings / container_safety record anywhere.
 6. THE GATE RUNS ON THE POST-STATE with presence ON over all 128, and the INSPECTED POPULATION is
    pinned (121 null, 0 [], 0 authored, 0 shells carrying, 3 warnings), so a green gate cannot be a
    gate that inspected nothing.
 7. NULL IS CHECKED BY IDENTITY, NEVER BY TRUTHINESS. `x is None`, not `not x` and never
    `not (x or [])`: the PLA-533 ratchet collapses null and [] on purpose, and here that idiom would
    let one crop's null become [] -- "assessed, none found" -- and pass.
 8. BLAST RADIUS, SET BEFORE VALUE: the top-level key set must be the base's plus exactly
    container_safety; every other top-level value byte-identical; roster unchanged; every shell
    byte-identical; every certified crop's key set the base's plus exactly critical_warnings and
    every other key byte-identical (verification_status included).

Usage:
    promote_pla581_critical_warnings.py --check
    promote_pla581_critical_warnings.py --out /path/scratch.json
    promote_pla581_critical_warnings.py --expect-sha <sha>       # writes canonical, on approval only
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla581_critical_warnings")
SPEC = os.path.join(STAGE, "spec.json")
SPEC_DOC = os.path.join(REPO, "docs", "superpowers", "specs",
                        "2026-09-21-pla581-critical-warnings-field-shape.md")

sys.path.insert(0, HERE)
import critical_warnings_gate as CWG  # noqa: E402  -- imported, never retyped

BASE_SHA = "526788f2c34a7fe1c59e9427271c1d1738c6b6cce2c1d0524df715e4fc359659"  # PLA-580, 2588678
ROSTER = 128
CERTIFIED = "verified_gs_arc"
FIELD = CWG.FIELD
DKEY = CWG.DATASET_KEY
FETCH_DATE = "2026-09-23"

EXPECTED_CERTIFIED = 121
EXPECTED_SHELLS = 7
EXPECTED_WARNINGS = 3
EXPECTED_PAGES = 4

# THE RULING, as independent literals (spec 4.5, 9, 14; severity ruled 2026-09-23).
EXPECTED_IDS = ["balcony_load", "container_material", "hanging_security"]
EXPECTED_SEVERITY = "high"   # UNIFORM and MODELED: no source grades these, no ranking is claimed
EXPECTED_SOURCES = {
    "balcony_load": {"uiuc_ext": "https://extension.illinois.edu/container-gardens/container-size"},
    "container_material": {
        "csu_ext": "https://extension.colostate.edu/resource/container-gardens/",
        "uiuc_ext": "https://extension.illinois.edu/container-gardens/vegetable-containers"},
    "hanging_security": {
        "uiuc_ext": "https://extension.illinois.edu/container-gardens/container-material-choices"},
}
# Titles are user-facing prose authored in the claude.ai lane, sent by Trevor 2026-09-23 and pinned
# here as literals, independent of the builder's copy. main() still REFUSES the canonical write if a
# staged title is a placeholder (TITLE_PENDING below), so interim wording can never ship.
EXPECTED_TITLES = {
    "balcony_load": "Ask what your balcony or roof can carry",
    "container_material": "Never grow food in a container with anything toxic in it",
    "hanging_security": "Secure hanging containers well",
}
TITLE_PENDING = re.compile(r"TITLE PENDING")
# THE SENTENCES EACH WARNING RESTS ON, as (page url, verbatim sentence), per spec section 14 and the
# independent clause check recorded there. A warning can rest on several sentences and several pages
# (container_material's treated-lumber clause is on container-material-choices, a page it does not
# anchor), so this is keyed by WARNING, not by page. The balcony "no weight figure" clause is an
# ABSENCE verified by reading the whole page, so it has no sentence here. The one declared inference
# (container_material seasoned, last sentence) is deliberately NOT given a sentence. hanging_security's
# "since" is ILLINOIS'S OWN link (the drip sentence followed by "Consider this when determining
# placement ..."), which is why that second sentence is here; the page's wood sentence is NOT, because
# it sits under the rot question and the copy no longer uses it.
_SIZE = "https://extension.illinois.edu/container-gardens/container-size"
_CSU = "https://extension.colostate.edu/resource/container-gardens/"
_VEG = "https://extension.illinois.edu/container-gardens/vegetable-containers"
_MAT = "https://extension.illinois.edu/container-gardens/container-material-choices"
EVIDENCE = {
    "balcony_load": [
        (_SIZE, "Consult with a building architect concerning weight limitations when placing heavy "
                "pots on balcony or rooftop gardens."),
    ],
    "container_material": [
        (_CSU, "About any container can be used including clay (often called terra cotta), plastic "
               "pots, wood barrels, wire baskets lined with sphagnum moss or coconut coir, planter "
               "boxes, ceramic pots (often found in bold colors), and even cement blocks."),
        (_CSU, "However, make sure you never use a container that holds toxic materials, especially "
               "if edible plants are going to be grown."),
        (_VEG, "The container needs to have good drainage, and should not contain chemicals that are "
               "toxic to plants and human beings."),
        (_MAT, "Exercise caution with treated lumber when growing food, or where toddlers are "
               "concerned."),
    ],
    "hanging_security": [
        (_MAT, "Examples are a hanging basket, window, fence or rail box."),
        (_MAT, "Secure hanging items well and consider potential safety issues when hanging."),
        (_MAT, "It may drip on people or possessions below."),
        (_MAT, "Consider this when determining placement of a hanging container."),
    ],
}
EXPECTED_CUT = {"mosquito", "lifting", "pounds_figure"}

# MEASURED 2026-09-23, raw bytes under two user-agents, keyed by PAGE. A digest not on this list
# REFUSES (the shape of a hash field pulls a fabricated digest out of you -- PLA-465: 16 chars
# measured, 48 invented). Keyed rather than a set so a swap between two pages is visible.
# Three of the four REPRODUCE the spec's 2026-09-21 digests exactly. csu_ext does NOT: same
# 141,247 bytes, a different digest, the verbatim sentence present, both agents byte-identical; no
# 09-21 copy was kept, so the cause is UNDETERMINED and the record says so rather than guessing.
EVIDENCE_HASHES = {
    "https://extension.illinois.edu/container-gardens/container-size":
        "0b482e6ef1b9d9093dc0a0029e2753cf20bf787c7c329dd9ff23f7cbe0fe9705",  # 28,186 bytes
    "https://extension.colostate.edu/resource/container-gardens/":
        "a4dec7f1631e49d06f9e7fc2673d2064bdd7f641266ce78b579a88cf186badf5",  # 141,247 bytes (DRIFTED)
    "https://extension.illinois.edu/container-gardens/vegetable-containers":
        "62b5e5c5f5ce244fb868faccdc9ac11e0babb38aad6be60a6776d97577ed8d89",  # 24,343 bytes
    "https://extension.illinois.edu/container-gardens/container-material-choices":
        "5ab9a68fcdf516a59c964c9ee6715ef0abfbd10a7ab0cac83682128e54637452",  # 32,678 bytes
}
MEASURED_DIGESTS = set(EVIDENCE_HASHES.values())
SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _j(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def pending_titles(spec):
    """The warning ids whose title is still a placeholder. The write refuses while any remains."""
    return [w["id"] for w in spec[DKEY]["warnings"] if TITLE_PENDING.search(w["title"])]


def load_canonical(path=None):
    with open(path or CANON, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


def staged():
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f)


def approved_copy(doc_path=SPEC_DOC):
    """{id: (title, beginner, seasoned)} read from the approved spec's SECTION 14 (amendment 3),
    whitespace-collapsed.

    The oracle for the copy is the document Trevor ruled, not the builder that wrote the spec file,
    so a copy edit in the builder that nobody ruled REFUSES. Section 14 supersedes 4.4's bodies; 4.4
    stays in the document byte for byte as the record of what was first approved, and is pinned by
    the suite so it cannot be edited into agreement.
    """
    text = open(doc_path, encoding="utf-8").read()
    try:
        sec = text.split("\n## 14. ", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        raise SystemExit("REFUSED: cannot locate section 14 in the approved spec")
    out = {}
    # The header after an id may WRAP onto several lines (container_material's does); the tempered
    # `(?:(?!\*\*`).)*?` lets it, while forbidding a match from running into the NEXT id's header.
    for m in re.finditer(r"\*\*`(\w+)`\*\*(?:(?!\*\*`).)*?\n\n- \*title:\* \"(.*?)\"\s*\n- \*beginner:\* \"(.*?)\"\s*\n"
                         r"- \*seasoned:\* \"(.*?)\"", sec, re.S):
        out[m.group(1)] = tuple(re.sub(r"\s+", " ", g).strip() for g in m.group(2, 3, 4))
    if sorted(out) != sorted(EXPECTED_IDS):
        raise SystemExit(f"REFUSED: the approved spec's section 14 yields copy for {sorted(out)}, "
                         f"ruled {sorted(EXPECTED_IDS)}")
    return out


def check_spec_shape(spec, doc_path=SPEC_DOC):
    if not EVIDENCE_HASHES:
        raise SystemExit("REFUSED: EVIDENCE_HASHES is empty; no digest has been measured")
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    if spec.get("fetch_date") != FETCH_DATE:
        raise SystemExit(f"REFUSED: spec fetch_date {spec.get('fetch_date')!r} is not {FETCH_DATE}")
    if spec.get("expected") != {"certified_null": EXPECTED_CERTIFIED, "shells": EXPECTED_SHELLS,
                                "warnings": EXPECTED_WARNINGS, "records": EXPECTED_WARNINGS,
                                "pages": EXPECTED_PAGES}:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")

    # GUARD 3a: the pages, keyed by url, set before value.
    pages = spec["pages"]
    by_url = {p["url"]: p for p in pages.values()}
    if len(by_url) != len(pages) or set(by_url) != set(EVIDENCE_HASHES):
        raise SystemExit(f"REFUSED: spec pages are {sorted(by_url)}, measured {sorted(EVIDENCE_HASHES)}")
    for url, p in by_url.items():
        if p["sha256"] != EVIDENCE_HASHES[url]:
            raise SystemExit(f"REFUSED: {url} carries digest {p['sha256'][:16]}..., measured "
                             f"{EVIDENCE_HASHES[url][:16]}... for that page")
    # The evidence sentences, per warning, set before value.
    ev = spec["evidence"]
    if set(ev) != set(EVIDENCE):
        raise SystemExit(f"REFUSED: spec evidence covers {sorted(ev)}, ruled {sorted(EVIDENCE)}")
    for wid, pairs in EVIDENCE.items():
        if [(e["url"], e["sentence"]) for e in ev[wid]] != list(pairs):
            raise SystemExit(f"REFUSED: {wid} evidence is not the ruled sentences")
    # GUARD 3b: no fabricated digest anywhere in the staged artifact.
    for d in set(SHA256_RE.findall(json.dumps(spec, ensure_ascii=False))):
        if d not in MEASURED_DIGESTS and d != BASE_SHA:
            raise SystemExit(f"REFUSED: the spec quotes sha256 {d[:16]}... which is not a measured "
                             f"evidence digest")

    # GUARD 2: the cuts are a decision.
    cut = spec["cut"]
    if {c.get("candidate") for c in cut} != EXPECTED_CUT or len(cut) != len(EXPECTED_CUT):
        raise SystemExit(f"REFUSED: cut ledger is {[c.get('candidate') for c in cut]}, ruled "
                         f"{sorted(EXPECTED_CUT)}")
    for c in cut:
        if set(c) != {"candidate", "why"} or not (c["why"] or "").strip():
            raise SystemExit(f"REFUSED: cut {c.get('candidate')!r} records no reason")

    # GUARD 1: the warnings are the ruling.
    cs = spec[DKEY]
    if set(cs) != set(CWG.CS_KEYS):
        raise SystemExit(f"REFUSED: {DKEY} has keys {sorted(cs)}")
    ws = cs["warnings"]
    if [w.get("id") for w in ws] != EXPECTED_IDS:
        raise SystemExit(f"REFUSED: warning ids are {[w.get('id') for w in ws]}, ruled {EXPECTED_IDS}")
    copy_ok = approved_copy(doc_path)
    for w in ws:
        wid = w["id"]
        if w["class"] != "safety" or w["stage"] is not None:
            raise SystemExit(f"REFUSED: {wid} must be class safety with stage null")
        if w["severity"] != EXPECTED_SEVERITY:
            raise SystemExit(f"REFUSED: {wid} severity {w['severity']!r}; ruled {EXPECTED_SEVERITY!r} "
                             f"on all three (uniform, modeled)")
        if w["title"] != EXPECTED_TITLES[wid] or w["title"] != copy_ok[wid][0]:
            raise SystemExit(f"REFUSED: {wid} title is not the pinned one")
        if (w["body_beginner"], w["body_seasoned"]) != copy_ok[wid][1:]:
            raise SystemExit(f"REFUSED: {wid} body copy is not the approved spec's section 14")
        want = EXPECTED_SOURCES[wid]
        if sorted(w["sources"]) != sorted(want):
            raise SystemExit(f"REFUSED: {wid} cites {w['sources']}, ruled {sorted(want)}")
        for s, url in want.items():
            if w["anchoring_urls"].get(s) != {"url": url, "verified": FETCH_DATE}:
                raise SystemExit(f"REFUSED: {wid} anchor for {s} is not {url} verified {FETCH_DATE}")

    # GUARD 3c: each record names every page its warning rests on, quotes THAT page's digest, and
    # quotes every sentence the warning rests on.
    recs = {r.get("field"): r for r in cs["field_additions"]}
    if len(recs) != len(cs["field_additions"]) or set(recs) != {f"{DKEY}.{i}" for i in EXPECTED_IDS}:
        raise SystemExit(f"REFUSED: records are {sorted(recs)}; one per ruled warning")
    for w in ws:
        r = recs[f"{DKEY}.{w['id']}"]
        if r["date"] != FETCH_DATE:
            raise SystemExit(f"REFUSED: record for {w['id']} is dated {r['date']!r}, not {FETCH_DATE}")
        for url in dict.fromkeys(u for u, _ in EVIDENCE[w["id"]]):
            if EVIDENCE_HASHES[url] not in r["note"]:
                raise SystemExit(f"REFUSED: record for {w['id']} credits {url} but does not quote "
                                 f"that page's measured digest")
        for url, sentence in EVIDENCE[w["id"]]:
            if sentence not in r["note"]:
                raise SystemExit(f"REFUSED: record for {w['id']} does not quote the sentence it rests "
                                 f"on from {url}")
    return len(ws)


def check_pre_state(spec, data):
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    cert = [c for c in data["crops"] if _certified(c)]
    if len(cert) != EXPECTED_CERTIFIED:
        raise SystemExit(f"REFUSED: {len(cert)} certified crops, pinned {EXPECTED_CERTIFIED}")
    if DKEY in data:
        raise SystemExit(f"REFUSED: the dataset already carries {DKEY}")
    for c in data["crops"]:
        if FIELD in c:
            raise SystemExit(f"REFUSED: {c['slug']} already carries {FIELD}")
        fa = (c.get("verification_status") or {}).get("field_additions") or []
        if any(isinstance(x, dict) and str(x.get("field", "")).startswith((FIELD, DKEY)) for x in fa):
            raise SystemExit(f"REFUSED: {c['slug']} already records a {FIELD}/{DKEY} addition")
    syn = {"source_catalog": data["source_catalog"], DKEY: copy.deepcopy(spec[DKEY])}
    v = CWG.dataset_violations(syn, presence=True)
    if v:
        raise SystemExit(f"REFUSED: the staged {DKEY} fails critical_warnings_gate: {v[:3]}")
    return len(cert)


def apply_to(data, spec):
    post = copy.deepcopy(data)
    post[DKEY] = copy.deepcopy(spec[DKEY])
    for c in post["crops"]:
        if _certified(c):
            c[FIELD] = None
    return post


EXPECTED_POPULATION = {"certified": 121, "null": 121, "empty": 0, "authored": 0, "invalid": 0,
                       "absent_certified": 0, "entries": 0, "shells_carrying": 0,
                       "container_safety_warnings": 3}


def check_post(post):
    v = CWG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: critical_warnings_gate on the post-state: " + "; ".join(v[:5]))
    p = CWG.population(post)
    if p != EXPECTED_POPULATION:
        raise SystemExit(f"REFUSED: the gate inspected {p}, pinned {EXPECTED_POPULATION}")
    return p


def verify_post(pre, post, spec):
    """SET COMPARISON BEFORE VALUE COMPARISON, at every level. Null by identity, never truthiness."""
    if set(post) != set(pre) | {DKEY} or DKEY in pre:
        raise SystemExit(f"REFUSED: top-level key set is not the base's plus {DKEY}")
    for k in pre:
        if k != "crops" and _j(pre[k]) != _j(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    if _j(post[DKEY]) != _j(spec[DKEY]):
        raise SystemExit(f"REFUSED: the written {DKEY} is not the staged one")
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop roster changed")
    nulls = 0
    for slug, s in pre_i.items():
        g = post_i[slug]
        if not _certified(s):
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: shell {slug} changed")
            continue
        if set(g) != set(s) | {FIELD}:
            raise SystemExit(f"REFUSED: {slug} crop key set is not the base's plus {FIELD}")
        for k in s:
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed; this pass adds {FIELD} only")
        if g[FIELD] is not None:
            raise SystemExit(f"REFUSED: {slug} {FIELD} is {g[FIELD]!r}; the ruling writes null (not "
                             f"assessed) on every certified crop, and [] would assert 'assessed, none found'")
        nulls += 1
    # No closing `nulls != 121` refusal: check_pre_state pins 121 certified and every certified
    # crop must carry the key as null above, so a total check could never fire first in the
    # pipeline and would read as coverage (the PLA-580 closing-totals lesson). Informational only.
    return nulls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("--canonical", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    if args.out and os.path.abspath(args.out) == os.path.abspath(args.canonical or CANON):
        sys.exit("REFUSED: --out may not target the canonical; use --expect-sha for the write")

    data = load_canonical(args.canonical)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} warnings match the ruling (ids, class, severity {EXPECTED_SEVERITY}, "
          f"stage null, sources, anchors); titles + bodies = the approved spec's section 14; "
          f"{len(spec['pages'])} pages at their measured digests; "
          f"{sum(len(v) for v in EVIDENCE.values())} evidence sentences quoted; "
          f"{len(spec['cut'])} cuts recorded with reasons")
    n = check_pre_state(spec, data)
    print(f"  pre-state         no {FIELD} key, no {DKEY}, no record anywhere; {n} certified; the "
          f"staged object passes the gate with presence on")
    post = apply_to(data, spec)
    p = check_post(post)
    print(f"  post gates        critical_warnings_gate (presence ON, all 128) 0 violations; inspected "
          f"{p['certified']} certified: {p['null']} null, {p['empty']} [], {p['authored']} authored; "
          f"{p['container_safety_warnings']} warnings")
    nulls = verify_post(data, post, spec)
    print(f"  verify post       {nulls} certified crops took {FIELD}: null (by identity); "
          f"{DKEY} added; nothing else")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.out:
        with open(args.out, "wb") as f:
            f.write(blob)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
        return 0
    if args.check:
        print("  --check: nothing written")
        return 0
    if not args.expect_sha:
        sys.exit("REFUSED: writing canonical requires --expect-sha (the gauntleted scratch SHA)")
    pending = pending_titles(spec)
    if pending:
        sys.exit(f"REFUSED: titles still pending for {pending}; titles are authored in the claude.ai "
                 f"lane and nothing ships with placeholder wording")
    with open(args.canonical or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {args.canonical or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
