#!/usr/bin/env python3
"""PLA-8 batch 4: promote the five squashes. Base e40cd8ec.

The authored content and the read: tools/staging/pla8_ladder_batch4/ (README.md carries the read).

WHAT MOVES. Five crops gain ladders: yellow-summer-squash, zucchini-courgette, acorn-squash,
butternut-squash, spaghetti-squash. 31 problems gain `id`, `type` and `control_ladder`; 139 rungs.
NO control_method is touched, NO source, NO crop outside the five. Roster laddered 19 -> 24.

THIS IS THE FIRST HYBRID BATCH, AND THE PROMOTE ASSERTS BOTH HALVES.

Batch 2 (the corns) was a true twin group and its promote refuses if the staged files DIVERGE.
Batch 3 (the cucumbers) was not a twin group at all and its promote refuses if they CONVERGE. This
batch is both at once, verified field by field before authoring:

  yellow-summer-squash + zucchini-courgette   40/40 prose fields identical  -> ONE authoring pass,
                                                                               propagated, identity ASSERTED
  acorn + butternut + spaghetti               73-80% identical              -> THREE authoring passes,
                                                                               distinctness ASSERTED

So `check()` refuses if the twin pair is not byte-identical AND refuses if any two of the trio are.

NOTE ON WHAT DISTINCTNESS MEANS HERE. The trio converges on IDENTICAL METHOD SEQUENCES, and that is
correct rather than suspicious: same seven problems, 73-80% shared prose, and none of the
crop-distinct variety claims that made batch 3's cucumbers diverge in methods. What must differ is
the PROSE. `verify_post` therefore compares full ladder CONTENT, notes included; comparing method
keys alone refused this batch on its first dry run.
Getting either wrong means the batching premise was wrong, and a promote that cannot tell the
difference would ship one of the two defects batches 2 and 3 exist to prevent.

WHAT THE READ CHANGED, all three found across siblings rather than within one crop:

 1. `copper_fungicide` REMOVED from butternut and spaghetti's downy-mildew ladders. All eight prose
    fields are byte-identical across the trio, yet two crops authored a copper rung and acorn
    refused. Acorn was right: these crops' prose says only "a labeled fungicide" and names no
    material, where certified cucumber's says "such as copper or chlorothalonil". Naming a product
    the crop's own prose does not carry is what the restate-from-own-prose rule forbids.
 2. `borer_stem_surgery` ADDED to all five borer ladders, replacing a `handpick` rung on two of them.
    Three agents independently reported stem surgery unplaceable and two rejected `handpick` by
    name, citing its own con, "Misses hidden eggs and tiny larvae". Minted in the preceding catalog
    round (cadaa6c) and scoped to `insect_boring` precisely so the gate can tell the two apart.
 3. The problem id `cucumber-beetle` NORMALIZED to `cucumber-beetles`. The summer-squash pair minted
    the singular while the trio and three shipped cucumbers use the plural. Ids are join keys; two
    independent passes producing different ids for the same problem is the defect CLAUDE.md's
    pin-at-first-authoring rule exists to prevent.

REFUSALS: base SHA mismatch; a crop already laddered; the twin pair not byte-identical; any two of
the trio identical; a problem id that disagrees with the roster's shipped spelling; a copper rung on
this batch's downy mildew; a borer ladder without borer_stem_surgery; staged/canonical problem-count
mismatch; a method not in the catalog; applies_to unreachable for the type; tiers decreasing; an
EMPTY ladder; a rung missing either register or with identical registers; any prune_out_infection.

Guard suite:      tools/test_promote_pla8_batch4.py
Mutation harness: tools/mutate_pla8_batch4_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch4.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch4")
BASE_SHA = "e40cd8ecb612a292880fa4a75f62ebc14267123914fa16d023903c9e63aac9bd"

TWIN = ("yellow-summer-squash", "zucchini-courgette")   # 40/40 identical: one pass, propagated
TRIO = ("acorn-squash", "butternut-squash", "spaghetti-squash")   # 73-80%: authored separately
CROPS = TWIN + TRIO
AUTHORED = "yellow-summer-squash"

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_RUNGS = {"yellow-summer-squash": 23, "zucchini-courgette": 23, "acorn-squash": 31,
                  "butternut-squash": 31, "spaghetti-squash": 31}
EXPECTED_PROBLEMS = {"yellow-summer-squash": 5, "zucchini-courgette": 5, "acorn-squash": 7,
                     "butternut-squash": 7, "spaghetti-squash": 7}

# The roster's shipped spelling for problems this batch also carries. A disagreement is a join-key
# defect, not a style nit: varieties[].resistance and ladder_delta point at these strings.
ID_CONVENTION = {"Cucumber beetles": "cucumber-beetles", "Squash bug": "squash-bug",
                 "Powdery mildew": "powdery-mildew", "Downy mildew": "downy-mildew",
                 "Bacterial wilt": "bacterial-wilt", "Aphids": "aphids",
                 "Squash vine borer": "squash-vine-borer"}

BORER_METHOD = "borer_stem_surgery"


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def rung_count(batch):
    return sum(len(p.get("control_ladder") or [])
               for crop in CROPS for fam in ("pests", "diseases")
               for p in batch[crop].get(fam, []))


def check_grouping(batch):
    """BOTH halves of the hybrid premise, asserted in opposite directions."""
    dg = staged_digests()
    if dg[TWIN[0]] != dg[TWIN[1]]:
        return (f"the twin pair {TWIN} is NOT byte-identical ({dg[TWIN[0]][:12]} vs "
                f"{dg[TWIN[1]][:12]}); they were verified 40/40 on prose, so one crop is authored "
                f"and the other propagated")
    trio_dg = {s: dg[s] for s in TRIO}
    if len(set(trio_dg.values())) != len(TRIO):
        return (f"two of {TRIO} are byte-identical: { {k: v[:12] for k, v in trio_dg.items()} }. "
                f"They share only 73-80% of their prose and must be authored separately")
    if dg[TWIN[0]] in trio_dg.values():
        return "a trio crop is byte-identical to the twin pair; that is a propagation across a family"
    return None


def check_read_fixes(batch, by):
    """The three cross-sibling corrections the read applied; each must hold in the staged batch.

    `by` is the CANONICAL crop map, and it is required rather than optional: the staged files carry
    only {id, type, control_ladder}, with no `name`, so resolving the problem name has to come from
    canonical at the same index. The first version read `p.get("name")` off the staged problem,
    which is always None, so `want` was always None and the id guard never fired ONCE. Its own test
    caught it -- the guard was dead the entire time it looked like coverage.
    """
    for slug in CROPS:
        for fam in ("pests", "diseases"):
            canon = (by[slug].get(fam) or [])
            for idx, p in enumerate(batch[slug].get(fam, [])):
                name = (canon[idx].get("name") if idx < len(canon) else None) or ""
                want = ID_CONVENTION.get(name)
                if want and p.get("id") != want:
                    return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the roster ships "
                            f"{want!r}; ids are join keys and must not diverge between passes")
                methods = [r["method"] for r in p.get("control_ladder") or []]
                if p.get("id") == "downy-mildew" and "copper_fungicide" in methods:
                    return (f"{slug}/downy-mildew carries copper_fungicide, but this crop's prose "
                            f"says only 'a labeled fungicide' and names no material")
                if p.get("id") == "squash-vine-borer":
                    if BORER_METHOD not in methods:
                        return (f"{slug}/squash-vine-borer has no {BORER_METHOD} rung; stem surgery "
                                f"is the crop's only in-season remedy and the method was minted for it")
                    if "handpick" in methods:
                        return (f"{slug}/squash-vine-borer still carries handpick, whose own con is "
                                f"'Misses hidden eggs and tiny larvae'")
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    order = {t: i for i, t in enumerate(TIERS)}
    for crop in CROPS:
        n_prob = 0
        for fam in ("pests", "diseases"):
            for p in batch[crop].get(fam, []):
                n_prob += 1
                if not p.get("id") or not p.get("type"):
                    return f"{crop}: a problem is missing id or type"
                lad = p.get("control_ladder")
                if lad is None:
                    return f"{crop}/{p.get('id')}: no control_ladder"
                if not lad:
                    return f"{crop}/{p.get('id')}: control_ladder is EMPTY"
                tiers = []
                for i, r in enumerate(lad):
                    m = r.get("method")
                    if m not in cm:
                        return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                    if m == "prune_out_infection":
                        return f"{crop}/{p.get('id')}#{i}: prune_out_infection is a woody method"
                    targets = TYPE_TARGETS.get(p.get("type")) or set()
                    if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):
                        return (f"{crop}/{p.get('id')}#{i}: {m!r} applies_to "
                                f"{sorted(cm[m]['applies_to'])} cannot reach type {p.get('type')!r}")
                    for k in ("note_beginner", "note_seasoned"):
                        if not str(r.get(k) or "").strip():
                            return f"{crop}/{p.get('id')}#{i}: {k} missing or empty"
                    if r["note_beginner"] == r["note_seasoned"]:
                        return f"{crop}/{p.get('id')}#{i}: registers are identical"
                    tiers.append(order[cm[m]["tier"]])
                if tiers != sorted(tiers):
                    return f"{crop}/{p.get('id')}: tiers decrease {tiers}"
        if n_prob != EXPECTED_PROBLEMS[crop]:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS[crop]}"
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    if BORER_METHOD not in cm:
        return f"{BORER_METHOD} is not in the catalog; the mint round must land first"
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for fam in ("pests", "diseases"):
            if any("control_ladder" in p for p in by[slug].get(fam) or [] if isinstance(p, dict)):
                return f"{slug} is already laddered; re-laddering changes shipped ids"
    batch = staged()
    for problem in (check_grouping(batch), check_read_fixes(batch, by)):
        if problem:
            return problem
    for slug in CROPS:
        for fam in ("pests", "diseases"):
            a, b = len(batch[slug].get(fam, [])), len(by[slug].get(fam) or [])
            if a != b:
                return f"{slug}/{fam}: staged {a} problems, canonical {b}"
    problem = validate_batch(batch, cm)
    if problem:
        return problem
    for slug in CROPS:
        n = sum(len(p.get("control_ladder") or [])
                for fam in ("pests", "diseases") for p in batch[slug].get(fam, []))
        if n != EXPECTED_RUNGS[slug]:
            return f"{slug}: {n} rungs, expected {EXPECTED_RUNGS[slug]}"
    if rung_count(batch) != sum(EXPECTED_RUNGS.values()):
        return f"rung count {rung_count(batch)}, expected {sum(EXPECTED_RUNGS.values())}"
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    batch = staged()
    by = {c.get("slug"): c for c in data["crops"]}
    minted = reused = 0
    for slug in CROPS:
        crop = by[slug]
        for fam in ("pests", "diseases"):
            for i, add in enumerate(batch[slug].get(fam, [])):
                tgt = crop[fam][i]
                if isinstance(tgt.get("id"), str) and tgt["id"]:
                    reused += 1
                else:
                    tgt["id"] = add["id"]
                    minted += 1
                tgt["type"] = add["type"]
                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])
    return minted, reused, rung_count(batch)


def verify_post(data):
    by = {c.get("slug"): c for c in data["crops"]}
    for slug in CROPS:
        for fam in ("pests", "diseases"):
            for p in by[slug].get(fam) or []:
                if isinstance(p, dict) and not p.get("control_ladder"):
                    return f"{slug}/{p.get('id')}: no ladder after promote"

    def sig(s):
        """FULL ladder content, notes included -- not the method sequence.

        The first version compared method keys alone and refused this batch, wrongly. The trio
        CONVERGES on identical method sequences and that is the correct outcome: they carry the same
        seven problems, share 73-80% of their prose, and have none of the crop-distinct variety
        claims that made batch 3's cucumbers diverge in methods. What must differ is the PROSE, and
        every note does. Method convergence across a shared-name family is evidence the catalog is
        being applied consistently, not evidence of a propagation.
        """
        c = by[s]
        return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                            for r in p["control_ladder"]]
                           for fam in ("pests", "diseases") for p in c.get(fam) or []
                           if isinstance(p, dict)], sort_keys=True)
    if sig(TWIN[0]) != sig(TWIN[1]):
        return "post: the twin pair does not carry identical ladders"
    if len({sig(s) for s in TRIO}) != len(TRIO):
        return ("post: two of the trio carry identical ladder CONTENT; they were authored "
                "separately and their prose must differ")
    for slug in CROPS:
        for fam in ("pests", "diseases"):
            for p in by[slug].get(fam) or []:
                if not isinstance(p, dict):
                    continue
                methods = [r["method"] for r in p.get("control_ladder") or []]
                if p.get("id") == "squash-vine-borer" and BORER_METHOD not in methods:
                    return f"post: {slug}/squash-vine-borer lost its {BORER_METHOD} rung"
                if p.get("id") == "downy-mildew" and "copper_fungicide" in methods:
                    return f"post: {slug}/downy-mildew regained copper_fungicide"
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
    minted, reused, rungs = apply_to(data)
    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 batch 4 -- the five squashes, the first HYBRID batch")
    print(f"  twin pair    : {', '.join(TWIN)}  (40/40 prose identical; {AUTHORED} authored, one propagated)")
    print(f"  trio         : {', '.join(TRIO)}  (73-80%; authored separately)")
    print(f"  rungs        : {rungs}   ids minted: {minted}  reused: {reused}")
    print(f"  read-fixes   : copper dropped x2, borer_stem_surgery x5, one id normalized")
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
