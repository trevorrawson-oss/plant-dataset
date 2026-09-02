#!/usr/bin/env python3
"""PLA-8 catalog round 10: WIDEN `certified_clean_stock` to reach insect-typed problems, and
GENERALIZE its prose from pathogens to planting-stock-borne pests. Base e6c986e3.

The content, the sourcing, the verbatim quotes and the adjudications: build_pla8_catalog_r10_content.

WHAT MOVES. ONE existing method gains one `applies_to` target, one source, one anchor, and amended
prose. `control_methods` stays at 64 -- nothing is minted. `source_catalog` gains EXACTLY ONE id.
NO crop, NO ladder.

--------------------------------------------------------------------------------------------------
THE GUARD SHAPE INVERTS r9 IN ONE PLACE, AND THAT PLACE IS THE SOURCE CATALOG
--------------------------------------------------------------------------------------------------
r9 was a widening too, and its whole source guard was the single line "source_catalog changed, and
this round adds no source id". This round DOES add one, so that protection has to be rebuilt the
other way round: `source_catalog` may gain exactly the declared id and nothing else, every existing
entry must be byte-identical, and the new entry must be T1 with a pathed https anchor. A round that
can add one source is a round that can quietly add two, or edit an existing one, unless it says so.

Everything else follows r9, because the hazard is the same:

  * exactly ONE method may change, and it must be the declared one;
  * `applies_to` may only GAIN the declared target, never lose one;
  * **every claim the method already made must SURVIVE** -- **93 shipped rungs** (55 fungal, 30
    bacterial, 6 viral, 2 nematode) were authored against this text, and a widening that quietly
    rewrote what the method meant would change 93 rungs' meaning without touching a crop record.
    (86 was the count on b118f19d, before batch 23 itself added 7 more; measured against THIS
    round's base, not carried over from the sentence that was true last commit.)
  * the widening must actually UNBLOCK its declared cases, re-derived from TYPE_TARGETS rather than
    assumed from the target string;
  * NO crop changes at all.

--------------------------------------------------------------------------------------------------
WHY THE PROSE MOVES AND NOT JUST THE TARGET
--------------------------------------------------------------------------------------------------
Widening alone would have been a defect. 4 of the 14 blocked rungs are about a PEST riding inside
the planting material (weevil-free slips, borer-free stock), and the shipped text told those readers
to look for "certified DISEASE-free" seed and to reject transplants showing "spotting, mottling or
wilt". `applies_to` governs what the GATE accepts and does nothing to what a READER sees. The
generalization is the point; the target is the mechanism.

The method's own seasoned text already reached past pathogens -- it calls the garlic stem and bulb
nematode "a pest ... inside the tissue you planted" -- so this extends an existing concept rather
than inventing one, which is why one method is generalized instead of a near-duplicate being minted.

REFUSALS: base SHA mismatch; a widening count other than the declared one; a target outside the gate
vocabulary; a target already present; a declared source missing from source_catalog or not T1 or
without a pathed https anchor and a valid verified date; new prose failing copy hygiene; a
MUST_SURVIVE fragment absent from the CURRENT text (the guard would be checking something the method
never said) or dropped by the amendment; the method set changing; a method other than the declared
one changing; an applies_to target lost; a source dropped; the widening failing to unblock any
declared case; source_catalog gaining anything but the declared id or altering an existing entry;
ANY crop change.

Guard suite:      tools/test_promote_pla8_catalog_r10.py
Mutation harness: tools/mutate_pla8_catalog_r10_suite.py (PLA-215)
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "e6c986e38e15a0219d64c805cfc11a8786e974320f915e1dd35e6031422f0419"

BRITISH = ("colour", "favour", "organise", "organised", "recognise", "practise", "fibre",
           "centre", "labelled", "tunnelling", "moulds", "sulphur")

EXPECTED_WIDENINGS = 1
EXPECTED_METHOD_COUNT = 64
EXPECTED_NEW_SOURCES = 1
EXPECTED_RUNGS_ON_METHOD = 93

def content():
    import build_pla8_catalog_r10_content as C
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
    # r9 REFUSED new sources outright. This round adds one, so the refusal becomes a validation:
    # the count is pinned, the id must not already exist, and the entry must be T1 with a pathed
    # https url. A round that can add one source can quietly add two unless it says how many.
    if len(C.NEW_SOURCES) != EXPECTED_NEW_SOURCES:
        return (f"this round declares {len(C.NEW_SOURCES)} new sources, expected "
                f"{EXPECTED_NEW_SOURCES}")
    for sid, entry in C.NEW_SOURCES.items():
        if sid in sc:
            return f"new source {sid!r} already exists in source_catalog; this would overwrite it"
        if (entry.get("tier") or "").upper() != "T1":
            return f"new source {sid!r} is not T1"
        u = str(entry.get("url") or "")
        if not u.startswith("https://"):
            return f"new source {sid!r} url is not https"
        if len(u.split("://", 1)[1].strip("/").split("/")) < 2:
            return (f"new source {sid!r} url is a BARE HOST; a citation must point at the document "
                    f"that carries the claim")
        if not entry.get("citable_for"):
            return f"new source {sid!r} has no citable_for"
    # A54 IS A ROSTER GATE, AND THIS PROMOTE'S 49-MUTATION HARNESS DID NOT COVER IT. The first run
    # of this round applied cleanly, passed its own suite and harness, and then took gate_all from
    # 121/121 to 0/121 because the minted id carried `name` but no `title`. A promote that mints a
    # source must run the roster gate that reads source_catalog, not just its own guards. The gate
    # function is IMPORTED, never retyped, so it cannot drift from the one gate_all runs.
    from source_catalog_title_gate import title_violations
    probe = dict(sc)
    probe.update({k: dict(v) for k, v in C.NEW_SOURCES.items()})
    tv = title_violations(probe)
    if tv:
        return f"the minted source(s) would fail A54 at the gauntlet: {tv[0]}"

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
            # A source cited by this widening is valid if it is ALREADY in source_catalog or if this
            # same round declares it. Anything else is a citation to an id that will not exist.
            entry = sc.get(s) or C.NEW_SOURCES.get(s)
            if entry is None:
                return (f"{key}: source {s!r} is neither in source_catalog nor declared by this "
                        f"round")
            if (entry.get("tier") or "").upper() != "T1":
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
        # set_fields may hold LISTS (pros, cons) as well as strings, unlike r9 where every replaced
        # field was a string. Flatten, or hygiene silently never runs on the list-valued fields.
        checked = 0
        for v in list(w["set_fields"].values()) + list(w.get("add_pros") or []) \
                + list(w.get("add_cons") or []):
            for s in (v if isinstance(v, list) else [v]):
                checked += 1
                bad = hygiene(s)
                if bad:
                    return f"{key}: new prose fails copy hygiene ({bad}): {s[:70]!r}"
        if checked == 0:
            return f"{key}: no new prose was scanned for hygiene; this check would be vacuous"

    # THE SURVIVING CLAIMS, checked against the TEXT THIS ROUND WILL WRITE, not against the old text.
    for key, fragments in C.MUST_SURVIVE.items():
        w = C.WIDENINGS.get(key)
        if w is None:
            return f"MUST_SURVIVE names {key!r}, which this round does not widen"
        parts = []
        for v in list(w["set_fields"].values()) + list(w.get("add_pros") or []) \
                + list(w.get("add_cons") or []):
            parts.extend(v if isinstance(v, list) else [v])
        blob = " ".join(parts).lower()
        old = " ".join(prose_of(cm[key])).lower()
        for f in fragments:
            if f.lower() not in old:
                return (f"{key}: MUST_SURVIVE fragment {f!r} is not in the CURRENT text, so this "
                        f"guard is checking something the method never said")
            if f.lower() not in blob:
                return (f"{key}: the widening drops the existing claim {f!r}. {EXPECTED_RUNGS_ON_METHOD} "
                            f"shipped rungs were "
                        f"authored against this text; a widening is additive or it is a rewrite")
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            # PER-KEY, not one blob: a blob comparison can only say "something changed", which is
            # useless in a round that changes source_catalog on purpose. Per-key lets the guard say
            # exactly the declared id was added and every existing entry is byte-identical.
            "sources": {k: dump(v) for k, v in data["source_catalog"].items()},
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

    added = sorted(set(post["sources"]) - set(pre["sources"]))
    dropped = sorted(set(pre["sources"]) - set(post["sources"]))
    if dropped:
        return f"post: source_catalog DROPPED {dropped}"
    if added != sorted(C.NEW_SOURCES):
        return f"post: source_catalog added {added}, expected exactly {sorted(C.NEW_SOURCES)}"
    for k in pre["sources"]:
        if post["sources"][k] != pre["sources"][k]:
            return (f"post: existing source_catalog entry {k!r} was MODIFIED; this round only adds "
                    f"{sorted(C.NEW_SOURCES)}")
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
