#!/usr/bin/env python3
"""PLA-8 thin-ladder backfill: 8 rungs onto 6 problems across 4 SHIPPED crops. Base 4f33522c.

The content, the warrants and the adjudications: build_pla8_thin_ladder_backfill_content.

WHAT MOVES. Six problems on beet, fig, garlic and strawberry gain 8 rungs. NO existing rung's prose
changes; NO catalog method changes; NO source changes; no other crop is touched.

--------------------------------------------------------------------------------------------------
THIS IS THE FIRST PROMOTE IN THE ARC THAT EDITS ALREADY-LADDERED, SHIPPED CROPS
--------------------------------------------------------------------------------------------------
Every PLA-8 batch so far added ladders to problems that had none, so "already laddered" was a
REFUSAL. Here it is the precondition, and the protection has to be rebuilt accordingly:

  * `expect_before` pins each ladder's exact current method sequence. A drifted ladder REFUSES
    rather than being silently rebuilt.
  * every pre-existing rung must be BYTE-IDENTICAL after, dict for dict. Reordering is permitted
    only because `expect_after` declares the whole sequence explicitly.
  * the rungs added must be exactly the set difference, no more and no fewer.

--------------------------------------------------------------------------------------------------
EVERY ADDED RUNG MUST BE WARRANTED BY ITS OWN RECORD
--------------------------------------------------------------------------------------------------
`check_warrants` requires a declared phrase from the problem's OWN prose for each added rung, and
asserts that phrase is actually present. That is the restate-the-record discipline made checkable: a
rung whose warrant is not in the record is an invention, however plausible it sounds. It is the
guard that would have caught the 4 FALSE POSITIVES the thin-ladder scan produced, every one of which
looked reasonable and every one of which the prose named only to DISCOUNT.

REFUSALS: base SHA mismatch; a target problem missing; a ladder that does not match `expect_before`;
an existing rung's prose changed; rungs added that are not exactly the declared set; a warrant
phrase absent from the record; a method not in the catalog; a method illegal for the problem's type;
a tier decrease; a duplicate method; identical registers; a rung carrying keys beyond the note pair;
copy hygiene; counts off; any catalog, source_catalog or bystander-crop change.

Guard suite:      tools/test_promote_pla8_thin_ladder_backfill.py
Mutation harness: tools/mutate_pla8_thin_ladder_backfill_suite.py (PLA-215)
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "4f33522cbbf945ea1fe878c64f038623d4a98d0c3cf0211bf57cfa7b5c161866"

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")
PROSE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "prevention_beginner", "prevention_seasoned", "organic_treatment_beginner",
                "organic_treatment_seasoned", "management_beginner", "management_seasoned",
                "note_beginner", "note_seasoned")

from control_ladder_gate import TYPE_TARGETS  # noqa: E402


def content():
    import build_pla8_thin_ladder_backfill_content as C
    return C


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\d\s+°F", s):
        return "spaced degF"
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


def find_problem(data, slug, pid):
    crop = next((c for c in data["crops"] if c.get("slug") == slug), None)
    if crop is None:
        return None
    for fam in ("pests", "diseases"):
        for p in crop.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    return None


def record_prose(p):
    return " ".join(str(p.get(k) or "") for k in PROSE_FIELDS)


def check_warrants(data):
    """Every added rung must be traceable to a phrase in ITS OWN record. This is the guard that
    would have caught the scan's 4 false positives: each of those named a control only to discount
    it, and none could have produced a warrant phrase that survived reading."""
    C = content()
    seen = 0
    for (slug, pid), spec in C.BACKFILL.items():
        p = find_problem(data, slug, pid)
        if p is None:
            return f"{slug}/{pid} is not on the roster"
        blob = record_prose(p).lower()
        added = [m for m in spec["expect_after"] if m not in spec["expect_before"]]
        for m in added:
            key = (slug, pid, m)
            phrase = C.WARRANTS.get(key)
            if phrase is None:
                return (f"{slug}/{pid}/{m} has no declared warrant; a rung whose warrant is not in "
                        f"the record is an invention, however plausible")
            if phrase.lower() not in blob:
                return (f"{slug}/{pid}/{m}: warrant {phrase!r} is NOT in the record. Either the "
                        f"rung is unwarranted or the record changed under it")
            seen += 1
    if seen != C.EXPECTED_NEW_RUNGS:
        return f"warrant check covered {seen} rungs, expected {C.EXPECTED_NEW_RUNGS}"
    if set(C.WARRANTS) != {(s, p, m) for (s, p), sp in C.BACKFILL.items()
                           for m in sp["expect_after"] if m not in sp["expect_before"]}:
        return "the WARRANTS table does not exactly cover the rungs being added"
    return None


def check(data):
    C = content()
    cm = data.get("control_methods") or {}

    if len(C.BACKFILL) != C.EXPECTED_PROBLEMS:
        return f"backfill covers {len(C.BACKFILL)} problems, expected {C.EXPECTED_PROBLEMS}"
    if tuple(sorted({s for s, _ in C.BACKFILL})) != tuple(sorted(C.EXPECTED_CROPS)):
        return f"backfill touches {sorted({s for s, _ in C.BACKFILL})}, expected {sorted(C.EXPECTED_CROPS)}"

    total_added = 0
    for (slug, pid), spec in C.BACKFILL.items():
        p = find_problem(data, slug, pid)
        if p is None:
            return f"{slug}/{pid} is not on the roster"
        before = [r["method"] for r in p.get("control_ladder") or []]
        if before != spec["expect_before"]:
            return (f"{slug}/{pid} ladder is {before}, expected {spec['expect_before']}; it has "
                    f"drifted and this backfill was written against the old shape")
        added = [m for m in spec["expect_after"] if m not in spec["expect_before"]]
        dropped = [m for m in spec["expect_before"] if m not in spec["expect_after"]]
        if dropped:
            return f"{slug}/{pid} would DROP rung(s) {dropped}; this promote only adds"
        if sorted(added) != sorted(spec["add"]):
            return f"{slug}/{pid} adds {sorted(added)} but declares prose for {sorted(spec['add'])}"
        total_added += len(added)

        last = -1
        seen = set()
        for m in spec["expect_after"]:
            if m not in cm:
                return f"{slug}/{pid}: unknown method {m!r}"
            if m in seen:
                return f"{slug}/{pid}: duplicate method {m!r}"
            seen.add(m)
            t = TIERS.index(cm[m]["tier"])
            if t < last:
                return f"{slug}/{pid}: tier decrease at {m!r}"
            last = t
            applies = cm[m].get("applies_to") or []
            if "any" not in applies and not (set(TYPE_TARGETS.get(p.get("type"), ())) & set(applies)):
                return f"{slug}/{pid}: method {m!r} is illegal for type {p.get('type')!r}"

        for m, rung in spec["add"].items():
            if set(rung) != set(ADVICE_FIELDS):
                return f"{slug}/{pid}/{m}: rung carries {sorted(rung)}, expected the note pair"
            if rung["note_beginner"].strip() == rung["note_seasoned"].strip():
                return f"{slug}/{pid}/{m}: identical registers"
            for f in ADVICE_FIELDS:
                if not rung[f].strip():
                    return f"{slug}/{pid}/{m}: missing {f}"
                bad = hygiene(rung[f])
                if bad:
                    return f"{slug}/{pid}/{m} {f} fails copy hygiene ({bad})"

    if total_added != C.EXPECTED_NEW_RUNGS:
        return f"backfill adds {total_added} rungs, expected {C.EXPECTED_NEW_RUNGS}"
    return check_warrants(data)


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    out = {"methods": dump(data["control_methods"]), "sources": dump(data["source_catalog"]),
           "problems": {}}
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict):
                    out["problems"][(c["slug"], fam, p.get("name"))] = dump(p)
    return out


def apply_to(data):
    return content().apply_round(data)


def verify_post(pre, data):
    C = content()
    post = snapshot(data)

    # SET EQUALITY BEFORE VALUE COMPARISON (PLA-162).
    if set(pre["problems"]) != set(post["problems"]):
        added = sorted(set(post["problems"]) - set(pre["problems"]))[:4]
        dropped = sorted(set(pre["problems"]) - set(post["problems"]))[:4]
        return f"post: the problem SET changed. added={added} dropped={dropped}"

    targets = set(C.BACKFILL)
    changed = []
    for k in pre["problems"]:
        if post["problems"][k] != pre["problems"][k]:
            changed.append(k)
    for slug, fam, name in changed:
        p = json.loads(post["problems"][(slug, fam, name)])
        if (slug, p.get("id")) not in targets:
            return f"post: bystander problem {slug}/{name!r} changed"
    if len(changed) != C.EXPECTED_PROBLEMS:
        return f"post: {len(changed)} problems changed, expected {C.EXPECTED_PROBLEMS}"

    added = 0
    for (slug, pid), spec in C.BACKFILL.items():
        p = find_problem(data, slug, pid)
        after = [r["method"] for r in p["control_ladder"]]
        if after != spec["expect_after"]:
            return f"post: {slug}/{pid} ladder is {after}, expected {spec['expect_after']}"
        before_p = None
        for k, blob in pre["problems"].items():
            q = json.loads(blob)
            if k[0] == slug and q.get("id") == pid:
                before_p = q
        old = {r["method"]: r for r in before_p["control_ladder"]}
        for r in p["control_ladder"]:
            if r["method"] in old:
                if r != old[r["method"]]:
                    return (f"post: {slug}/{pid}/{r['method']} is an EXISTING rung and its prose "
                            f"changed; this promote adds rungs and rewrites none")
            else:
                added += 1
        for f in PROSE_FIELDS:
            if (p.get(f) or "") != (before_p.get(f) or ""):
                return f"post: {slug}/{pid} record prose field {f!r} changed; this promote adds rungs only"
    # FORWARD ASSERTION, deliberately not in the harness. Each ladder above is pinned to its
    # `expect_after`, so once those match, the number of rungs added is fixed by construction
    # and no post-state mutation can reach this line. What it guards is a future edit to this
    # function that loosens the per-problem comparison. Withdrawn rather than left reported as
    # a permanent survivor (see docs/promote_suite_mutation_convention.md).
    if added != C.EXPECTED_NEW_RUNGS:
        return f"post: {added} rungs added, expected {C.EXPECTED_NEW_RUNGS}"

    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints nothing"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed"
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
    summary = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        raise SystemExit("REFUSED: " + problem)

    blob = serialize(data)
    print("problems backfilled : %d" % summary["problems"])
    print("rungs added         : %d" % summary["rungs_added"])
    print("base  SHA           : %s" % sha)
    print("post  SHA           : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
