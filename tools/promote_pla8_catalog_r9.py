#!/usr/bin/env python3
"""PLA-8 catalog round 9: WIDEN `even_watering` to reach common scab. Base 6a67a677.

The content, the sourcing, the verbatim quotes and the adjudications: build_pla8_catalog_r9_content.

WHAT MOVES. ONE existing method gains one `applies_to` target, two sources, two anchors, and
amended prose. `control_methods` stays at 64 -- nothing is minted. `source_catalog` is BYTE-IDENTICAL
(both sources already existed). NO crop, NO ladder.

--------------------------------------------------------------------------------------------------
THE GUARD SHAPE IS INVERTED FROM r7 AND r8
--------------------------------------------------------------------------------------------------
Both of those rounds asserted "no existing method is touched" and guarded exactly that. This round
modifies one on purpose, so the equivalent protection has to be built the other way round:

  * exactly ONE method may change, and it must be the declared one;
  * `applies_to` may only GAIN the declared target, never lose one;
  * **every claim the method already made must SURVIVE** -- 37 shipped rungs (25 mite, 12
    physiological) were authored against this text, and a widening that quietly rewrote what the
    method meant would change 37 rungs' meaning without touching a single crop record;
  * `source_catalog` must be byte-identical, since this round adds no source id;
  * the widening must actually UNBLOCK what it was made for, asserted rather than assumed.

That last one matters because a widening whose target does not reach its case is a no-op that reads
as progress. `unblocks_its_case` re-derives legality from `TYPE_TARGETS` and refuses if
beet/common-scab is still unreachable.

--------------------------------------------------------------------------------------------------
WHY THIS ROUND EXISTS AT ALL
--------------------------------------------------------------------------------------------------
r8's record claimed `even_watering` already carried the moisture half of scab control. It did not:
its `applies_to` was `['physiological','mite']`, which cannot reach a `bacterial` problem. That was
an availability claim made without a legality check, found by the thin-ladder scan the same day.

REFUSALS: base SHA mismatch; a widened key absent from the catalog; a target already present; a
target outside the gate vocabulary; a surviving-claim fragment lost; a source not in source_catalog
or not T1; an anchor that is not https or has no verified date; the case not unblocked; copy
hygiene; more than one method changed; any method count change; any source_catalog change; any crop
change.

Guard suite:      tools/test_promote_pla8_catalog_r9.py
Mutation harness: tools/mutate_pla8_catalog_r9_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_catalog_r9.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "6a67a677960afcf3a0a85069c73737243d8117869232ec66ce8b79e99bdc8797"

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")
EXPECTED_WIDENINGS = 1
EXPECTED_METHOD_COUNT = 64


def content():
    import build_pla8_catalog_r9_content as C
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
    if re.search(r"\d+\s*F\b", s):
        return "bare F without a degree sign"
    if "**" in s or "__" in s:
        return "markdown emphasis"
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


def unblocks_its_case(cm):
    """A widening whose target does not reach its case is a no-op that reads as progress. Legality
    is re-derived from TYPE_TARGETS rather than assumed from the target string."""
    from control_ladder_gate import TYPE_TARGETS
    C = content()
    data = unblocks_its_case.data
    for slug, pid in C.UNBLOCKS:
        crop = next((c for c in data["crops"] if c.get("slug") == slug), None)
        if crop is None:
            return f"unblock target crop {slug!r} is not on the roster"
        prob = None
        for fam in ("pests", "diseases"):
            for p in crop.get(fam) or []:
                if isinstance(p, dict) and p.get("id") == pid:
                    prob = p
        if prob is None:
            return f"unblock target {slug}/{pid} is not on the roster"
        key = next(iter(C.WIDENINGS))
        targets = set(TYPE_TARGETS.get(prob.get("type"), ()))
        if not targets & set(cm[key]["applies_to"]):
            return (f"{key} still cannot reach {slug}/{pid} (type {prob.get('type')!r}); the "
                    f"widening is a no-op and this round has no effect")
    return None


unblocks_its_case.data = None


def check(data):
    C = content()
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    vocab = gate_vocabulary()

    if len(C.WIDENINGS) != EXPECTED_WIDENINGS:
        return f"this round widens {len(C.WIDENINGS)} methods, expected {EXPECTED_WIDENINGS}"
    if C.NEW_SOURCES:
        return ("this round declares new sources; it was written to add none, and the source "
                "validation below would not cover them")

    for key, w in C.WIDENINGS.items():
        if key not in cm:
            return f"{key} is not in the catalog, so it cannot be widened"
        m = cm[key]
        for t in w["add_targets"]:
            if t not in vocab:
                return f"{key}: target {t!r} is outside the gate vocabulary"
            if t in m["applies_to"]:
                return f"{key}: already applies to {t!r}; this widening has already been done"
        for s in w["add_sources"]:
            if s not in sc:
                return f"{key}: source {s!r} is not in source_catalog"
            if (sc[s].get("tier") or "").upper() != "T1":
                return f"{key}: source {s!r} is not T1"
            if s not in w["add_anchors"]:
                return f"{key}: source {s!r} has no anchoring_url"
        for s, a in w["add_anchors"].items():
            if s not in w["add_sources"]:
                return f"{key}: anchoring_url {s!r} is not a declared source"
            if not str(a.get("url", "")).startswith("https://"):
                return f"{key}: anchoring_url {s!r} is not https"
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
                return f"{key}: anchoring_url {s!r} has no valid verified date"
        for s in list(w["set_fields"].values()) + list(w.get("add_pros") or []) \
                + list(w.get("add_cons") or []):
            bad = hygiene(s)
            if bad:
                return f"{key}: new prose fails copy hygiene ({bad}): {s[:70]!r}"

    # THE SURVIVING CLAIMS, checked against the TEXT THIS ROUND WILL WRITE, not against the old text.
    for key, fragments in C.MUST_SURVIVE.items():
        w = C.WIDENINGS.get(key)
        if w is None:
            return f"MUST_SURVIVE names {key!r}, which this round does not widen"
        blob = " ".join(list(w["set_fields"].values()) + list(w.get("add_pros") or [])
                        + list(w.get("add_cons") or [])).lower()
        old = " ".join(prose_of(cm[key])).lower()
        for f in fragments:
            if f.lower() not in old:
                return (f"{key}: MUST_SURVIVE fragment {f!r} is not in the CURRENT text, so this "
                        f"guard is checking something the method never said")
            if f.lower() not in blob:
                return (f"{key}: the widening drops the existing claim {f!r}. 37 shipped rungs were "
                        f"authored against this text; a widening is additive or it is a rewrite")
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": dump(data["source_catalog"]),
            "crops": dump(data["crops"])}


def apply_to(data):
    return content().apply_round(data)


def verify_post(pre, data):
    C = content()
    cm = data["control_methods"]
    post = snapshot(data)

    if set(post["methods"]) != set(pre["methods"]):
        added = sorted(set(post["methods"]) - set(pre["methods"]))
        dropped = sorted(set(pre["methods"]) - set(post["methods"]))
        return f"post: the method SET changed. added={added} dropped={dropped}"
    # FORWARD ASSERTION, deliberately not in the harness. The set comparison above fires first for
    # any addition or removal, so no post-state mutation can reach this line -- with equal sets the
    # count is equal by construction. What it actually guards is BASE DRIFT: if the pinned base ever
    # stops carrying 64 methods, this refuses rather than widening against a catalog that is not the
    # one the round was written for. Its mutation was withdrawn from the harness rather than left
    # reported as a gap (see docs/promote_suite_mutation_convention.md).
    if len(post["methods"]) != EXPECTED_METHOD_COUNT:
        return f"post: {len(post['methods'])} methods, expected {EXPECTED_METHOD_COUNT}"

    changed = sorted(k for k in pre["methods"] if post["methods"][k] != pre["methods"][k])
    if changed != sorted(C.WIDENINGS):
        return f"post: methods changed {changed}, expected exactly {sorted(C.WIDENINGS)}"

    for key, w in C.WIDENINGS.items():
        before = json.loads(pre["methods"][key])
        after = cm[key]
        lost = [t for t in before["applies_to"] if t not in after["applies_to"]]
        if lost:
            return f"post: {key} LOST applies_to target(s) {lost}; a widening never removes one"
        gained = [t for t in after["applies_to"] if t not in before["applies_to"]]
        if gained != list(w["add_targets"]):
            return f"post: {key} gained {gained}, expected exactly {list(w['add_targets'])}"
        for s in before["sources"]:
            if s not in after["sources"]:
                return f"post: {key} dropped source {s!r}"
        for f in C.MUST_SURVIVE.get(key, ()):
            if f.lower() not in " ".join(prose_of(after)).lower():
                return f"post: {key} no longer says {f!r}; the widening rewrote rather than added"

    unblocks_its_case.data = data
    problem = unblocks_its_case(cm)
    if problem:
        return "post: " + problem

    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this round adds no source id"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed, and this promote touches no crop"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    problem = check(data)
    if problem:
        raise SystemExit("REFUSED: " + problem)

    pre = snapshot(data)
    before = dict(data["control_methods"][next(iter(content().WIDENINGS))])
    summary = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        raise SystemExit("REFUSED: " + problem)

    after = data["control_methods"][next(iter(content().WIDENINGS))]
    blob = serialize(data)
    print("widened           : %s" % ", ".join(summary["widened"]))
    print("applies_to        : %s -> %s" % (before["applies_to"], after["applies_to"]))
    print("sources           : %d -> %d" % (len(before["sources"]), len(after["sources"])))
    print("control_methods   : %d (unchanged)" % len(data["control_methods"]))
    print("base  SHA         : %s" % sha)
    print("post  SHA         : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
