#!/usr/bin/env python3
"""PLA-8 catalog round 7: mint 2 methods, mint 1 source, and REFUSE one widening. Base 7c3e5d71.

The content, the sourcing, the verbatim quotes and the adjudications: build_pla8_catalog_r7_content.

WHAT MOVES. `control_methods` 53 -> 55 (`biofungicide`, `weed_host_control`); `source_catalog`
213 -> 214 (`ucanr_ext_thrips`). NO existing method is touched, NO crop, NO ladder, NO other source.

WHY THERE IS A GUARD FOR SOMETHING THIS ROUND DID *NOT* DO. Both peas assert, in consumer prose on
their highest-severity problem, that planting early prevents powdery mildew, and r5 had already
noted that timing a sowing against a DISEASE was a real practice awaiting evidence. Six T1 documents
were fetched and read looking for it. They support "plant early because peas are a cool-season crop"
and "powdery mildew arrives in the later weather" as SEPARATE statements, and not one of them makes
the causal claim. Assembling a recommendation out of two true sentences from different parts of a
document is exactly how this same method acquired a wrong criterion at r5, so the widening was
refused.

**A refusal that leaves no trace is indistinguishable from an oversight.** `check` and `verify_post`
both assert that `planting_time_avoidance` still carries NO disease target, so a later pass cannot
quietly add one without bringing a document. The guard suite drives it and the harness proves it
fires.

REFUSALS: base SHA mismatch; a mint key already present; a new source id already present; a missing
required field; an unknown tier; an `applies_to` value outside the gate vocabulary; a source not in
source_catalog or not T1; a declared source with no anchoring_url; an anchoring_url that is not
https or has no verified date; a document-scoped source without a title, or one claiming the frozen
A54 exemption; a dropped source hedge; the refused widening appearing anyway; copy hygiene; and
post-state blast radius on methods, sources and every crop.

Guard suite:      tools/test_promote_pla8_catalog_r7.py
Mutation harness: tools/mutate_pla8_catalog_r7_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_catalog_r7.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "7c3e5d71ae875e013a20b77c3d8dd1f12960bfb8c413e7f8b728df79ef24d145"

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def content():
    import build_pla8_catalog_r7_content as C
    return C


def gate_vocabulary():
    from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET
    v = {UNIVERSAL_TARGET}
    for targets in TYPE_TARGETS.values():
        v |= set(targets)
    return v


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def _check_sources(m, key, sc, new_sources):
    known = dict(sc)
    known.update(new_sources)
    for s in m["sources"]:
        if s not in known:
            return f"{key}: source {s!r} is not in source_catalog"
        if (known[s].get("tier") or "").upper() != "T1":
            return f"{key}: source {s!r} is not T1"
        if s not in m["anchoring_urls"]:
            return f"{key}: source {s!r} has no anchoring_url"
    for s, a in m["anchoring_urls"].items():
        if s not in m["sources"]:
            return f"{key}: anchoring_url {s!r} is not a declared source"
        if not str(a.get("url", "")).startswith("https://"):
            return f"{key}: anchoring_url {s!r} is not https"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
            return f"{key}: anchoring_url {s!r} has no valid verified date"
    return None


def refused_widening_holds(cm):
    """THE REFUSAL, ASSERTED. See the module docstring: the evidence for timing a sowing against a
    disease was hunted across six T1 documents and not found, so the target was not added. A refusal
    that leaves no trace cannot be told apart from an oversight."""
    C = content()
    key, forbidden = C.REFUSED_WIDENING
    if key not in cm:
        return f"{key} is not in the catalog, so the refusal cannot be checked"
    present = sorted(set(cm[key].get("applies_to") or []) & set(forbidden))
    if present:
        return (f"{key} carries {present}, a disease target this round deliberately REFUSED: six T1 "
                f"documents support planting early and mildew arriving later as separate statements "
                f"and none makes the causal claim. Adding it needs a document, not an inference")
    return None


def check(data):
    C = content()
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    vocab = gate_vocabulary()

    for key, m in C.MINTS.items():
        if key in cm:
            return f"{key} is already in the catalog"
        for f in REQUIRED:
            if f not in m or not m[f]:
                return f"{key}: mint is missing required field {f!r}"
        if m["tier"] not in TIERS:
            return f"{key}: tier {m['tier']!r} is not one of {TIERS}"
        bad = [t for t in m["applies_to"] if t not in vocab]
        if bad:
            return (f"{key}: applies_to {bad} is outside the gate vocabulary, so no problem could "
                    f"ever reach this method")
        err = _check_sources(m, key, sc, C.NEW_SOURCES)
        if err:
            return err

    from source_catalog_title_gate import LEGACY_UNFILLED, _doc_scoped
    for sid, entry in C.NEW_SOURCES.items():
        if sid in sc:
            return f"source id {sid!r} is already in source_catalog"
        if (entry.get("tier") or "").upper() != "T1":
            return f"source {sid!r} is not T1"
        if sid in LEGACY_UNFILLED:
            return (f"source {sid!r} claims the frozen A54 exemption; that list is shrink-only and "
                    f"a new mint is never exempt")
        if _doc_scoped(entry) and not str(entry.get("title") or "").strip():
            return f"source {sid!r} is document-scoped and carries no title (A54)"
        if not _doc_scoped(entry) and entry.get("title"):
            return f"source {sid!r} is an institution root and must not carry a title (A54)"

    problem = refused_widening_holds(cm)
    if problem:
        return problem

    for key, hedges in C.REQUIRED_HEDGES.items():
        blob = " ".join(prose_of(C.MINTS[key])).lower()
        for h in hedges:
            if h.lower() not in blob:
                return f"{key}: the source qualifier {h!r} is missing from the prose"

    for key, m in C.MINTS.items():
        for s in prose_of(m):
            bad = hygiene(s)
            if bad:
                return f"{key}: prose fails copy hygiene ({bad}): {s[:70]!r}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": {k: dump(v) for k, v in data["source_catalog"].items()},
            "crops": dump(data["crops"])}


def apply_to(data):
    return content().apply_round(data)


def verify_post(pre, data):
    C = content()
    cm = data["control_methods"]
    sc = data["source_catalog"]
    post = snapshot(data)

    # SET EQUALITY BEFORE VALUE COMPARISON (PLA-162), both dicts, both directions.
    added_m = set(post["methods"]) - set(pre["methods"])
    if added_m != set(C.MINTS):
        return f"post: methods added {sorted(added_m)}, expected exactly {sorted(C.MINTS)}"
    if set(pre["methods"]) - set(post["methods"]):
        return f"post: methods dropped {sorted(set(pre['methods']) - set(post['methods']))}"
    added_s = set(post["sources"]) - set(pre["sources"])
    if added_s != set(C.NEW_SOURCES):
        return f"post: sources added {sorted(added_s)}, expected exactly {sorted(C.NEW_SOURCES)}"
    if set(pre["sources"]) - set(post["sources"]):
        return f"post: sources dropped {sorted(set(pre['sources']) - set(post['sources']))}"

    # THE SUBSTANTIVE INVARIANT RUNS BEFORE THE BLAST-RADIUS COMPARISON, and the ordering is
    # load-bearing. Adding the refused target IS a change to an existing method, so below the
    # bystander loop this guard could never fire -- its own test caught that, the same shape as the
    # r6 criterion scan. The refusal is the claim; blast radius is bookkeeping.
    problem = refused_widening_holds(cm)
    if problem:
        return "post: " + problem

    for k, before in pre["methods"].items():
        if post["methods"][k] != before:
            return f"post: existing method {k!r} changed, and this round mints only"
    for k, before in pre["sources"].items():
        if post["sources"][k] != before:
            return f"post: existing source {k!r} changed"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed, and this promote touches no crop"

    for key in C.MINTS:
        if key not in cm:
            return f"post: {key} was not minted"
        if cm[key] != C.MINTS[key]:
            return f"post: {key} does not match the authored method"
    for sid in C.NEW_SOURCES:
        if sc[sid] != C.NEW_SOURCES[sid]:
            return f"post: source {sid!r} does not match the authored entry"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != a.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr)
        return 1
    data = json.loads(raw.decode("utf-8"))
    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    pre = snapshot(data)
    before_m, before_s = len(data["control_methods"]), len(data["source_catalog"])
    summary = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    C = content()
    print("PLA-8 catalog round 7 -- two mints, one refusal")
    print(f"  control_methods : {before_m} -> {len(data['control_methods'])}")
    print(f"  source_catalog  : {before_s} -> {len(data['source_catalog'])}")
    for k in summary["minted"]:
        print(f"  mint            : {k}  (tier {C.MINTS[k]['tier']}, applies_to {C.MINTS[k]['applies_to']})")
    print(f"  REFUSED         : {C.REFUSED_WIDENING[0]} gains no disease target "
          f"(six T1 documents read, none makes the claim)")
    print(f"  crops touched   : 0   existing methods touched: 0   existing sources touched: 0")

    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
