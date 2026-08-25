#!/usr/bin/env python3
"""PLA-8 batch 3: promote the three cucumbers. Base c13ddea5.

The authored content and the read: tools/staging/pla8_ladder_batch3/ (README.md carries the read's
findings). The staged files are read and NEVER written back; the single read-fix lives in
tools/build_pla8_batch3_content.py as a delta on top of them.

WHAT MOVES. Three crops gain ladders: cucumber, pickling-cucumber, slicing-cucumber. Each of their 9
problems gains `id`, `type` and `control_ladder`; 45 + 47 + 45 = 137 rungs. NO control_method is
touched, NO source is minted, NO crop outside the three. Roster laddered 16 -> 19.

THIS BATCH INVERTS BATCH 2'S CENTRAL GUARD, AND THAT IS THE POINT.

`ladder_batch.py families` reported these three as a TWIN GROUP and instructed a mechanical
propagation: author one crop, copy the ladders, assert the copies are byte-identical -- which is
exactly what promote_pla8_batch2.py does for the corns. That instruction was WRONG HERE. The tool's
twin signature was `tuple(sorted(problem_name(p)))`, problem NAMES ONLY; it never compared prose.
Measured against c13ddea5 the three cucumbers share 72.2% of their problem fields, not 100%.

So this promote asserts the OPPOSITE of batch 2's: it REFUSES if the three crops come out carrying
identical ladders, because that would mean a propagation happened after all. And it pins the four
crop-distinct claims that a propagation would have destroyed:

  * pickling-cucumber alone claims wilt TOLERANCE ("wilt-tolerant varieties such as County Fair"),
    on BOTH cucumber-beetles and bacterial-wilt.
  * pickling-cucumber alone claims CMV-RESISTANT varieties, on aphids.
  * cucumber and slicing-cucumber instead claim NON-BITTER varieties attract fewer beetles, which is
    a claim about the VECTOR, so neither carries resistant_varieties on bacterial-wilt.

Copying cucumber onto pickling would erase County Fair and two earned rungs; copying pickling
outward would invent CMV resistance on two crops that never claim it. Both directions are content
defects, and `check()`/`verify_post()` refuse either.

ONE READ-FIX. cucumber was missing the resistant_varieties rung its own prose earns on Cucumber
beetles; see build_pla8_batch3_content.py for the precedent that settles it. Batch 1 needed 18,
batch 2 needed 0, this needed 1.

REFUSALS: base SHA mismatch; a crop already laddered; the three staged files IDENTICAL to each other;
the three promoted crops carrying identical ladders; any crop-distinct claim landing on the wrong
crop; staged/canonical problem-count mismatch; a method not in the catalog; a method whose applies_to
cannot reach the problem's type; a ladder whose tiers decrease; an EMPTY ladder; a rung missing
either register or with identical registers; any prune_out_infection in the batch.

Guard suite:      tools/test_promote_pla8_batch3.py
Mutation harness: tools/mutate_pla8_batch3_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch3.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch3")
BASE_SHA = "c13ddea5f1320d766847b707d3795c8cc81251d71ed864f61260f9eeb12e73f5"

CROPS = ("cucumber", "pickling-cucumber", "slicing-cucumber")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_RUNGS = {"cucumber": 45, "pickling-cucumber": 47, "slicing-cucumber": 45}
EXPECTED_PROBLEMS_PER_CROP = 9
EXPECTED_READ_FIXES = 1

# The claims that make these three crops NOT a twin group. Each is (crop, problem, method, present).
# A propagation in either direction breaks at least one of these, which is why they are pinned here
# rather than described in a comment.
DISTINCT_CLAIMS = (
    ("pickling-cucumber", "cucumber-beetles", "resistant_varieties", True),
    ("pickling-cucumber", "bacterial-wilt", "resistant_varieties", True),
    ("pickling-cucumber", "aphids", "resistant_varieties", True),
    ("cucumber", "bacterial-wilt", "resistant_varieties", False),
    ("slicing-cucumber", "bacterial-wilt", "resistant_varieties", False),
    ("cucumber", "aphids", "resistant_varieties", False),
    ("slicing-cucumber", "aphids", "resistant_varieties", False),
    # the read-fix: both non-bitter crops DO earn it on the beetle itself
    ("cucumber", "cucumber-beetles", "resistant_varieties", True),
    ("slicing-cucumber", "cucumber-beetles", "resistant_varieties", True),
)

# Substrings that must survive into the promoted prose, pinned to the ONE crop entitled to them.
# These are the sourced claims a propagation would have carried onto a crop that never made them.
PINNED_PROSE = (
    ("pickling-cucumber", "County Fair"),
    ("pickling-cucumber", "CMV-resistant"),
)


def staged():
    """The authored batch plus the read delta. Never written back to the staging files."""
    from build_pla8_batch3_content import apply_read_fixes
    batch = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}
    n = apply_read_fixes(batch)
    if n != EXPECTED_READ_FIXES:
        raise AssertionError(f"{n} read-fixes applied, expected {EXPECTED_READ_FIXES}")
    return batch


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def rung_count(batch):
    return sum(len(p.get("control_ladder") or [])
               for crop in CROPS for fam in ("pests", "diseases")
               for p in batch[crop].get(fam, []))


def ladder_of(crop_obj, pid):
    for fam in ("pests", "diseases"):
        for p in crop_obj.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p.get("control_ladder") or []
    return None


def validate_batch(batch, cm):
    """Structural truth about the batch, before it touches canonical."""
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
                    return (f"{crop}/{p.get('id')}: control_ladder is EMPTY. Author a rung, or the "
                            f"method it needs does not exist yet and the catalog is the fix")
                tiers = []
                for i, r in enumerate(lad):
                    m = r.get("method")
                    if m not in cm:
                        return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                    if m == "prune_out_infection":
                        return (f"{crop}/{p.get('id')}#{i}: prune_out_infection is a woody "
                                f"cut-back-into-clean-tissue method")
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
        if n_prob != EXPECTED_PROBLEMS_PER_CROP:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS_PER_CROP}"
    return None


def check_distinctness(batch):
    """THE INVERSE OF BATCH 2'S PREMISE. These crops are NOT twins; a propagation is the defect."""
    digests = staged_digests()
    if len(set(digests.values())) != len(CROPS):
        return (f"staged files are not all distinct: "
                f"{ {k: v[:12] for k, v in digests.items()} }; these crops are NOT a twin group "
                f"(72.2% field identity) and each must be authored separately")

    sig = {s: json.dumps([[r["method"] for r in p["control_ladder"]]
                          for fam in ("pests", "diseases") for p in batch[s].get(fam, [])],
                         sort_keys=True) for s in CROPS}
    if len(set(sig.values())) == 1:
        return ("the three crops carry IDENTICAL ladders; that is what a mechanical propagation "
                "looks like, and it would erase pickling-cucumber's County Fair and CMV claims")

    for crop, pid, method, want in DISTINCT_CLAIMS:
        lad = ladder_of(batch[crop], pid)
        if lad is None:
            return f"distinct-claim check: {crop} has no problem {pid!r}"
        has = any(r["method"] == method for r in lad)
        if has != want:
            verb = "must carry" if want else "must NOT carry"
            return (f"{crop}/{pid} {verb} {method!r}. This is a crop-distinct claim: "
                    f"pickling-cucumber's prose names wilt-tolerant County Fair and CMV-resistant "
                    f"varieties, while cucumber's and slicing's name non-bitter varieties that "
                    f"attract fewer beetles, a claim about the VECTOR")

    for owner, needle in PINNED_PROSE:
        for crop in CROPS:
            blob = json.dumps(batch[crop], ensure_ascii=False)
            present = needle in blob
            if crop == owner and not present:
                return f"{owner} lost its {needle!r} claim; that is the claim this batch protects"
            if crop != owner and present:
                return (f"{crop} carries {needle!r}, which belongs only to {owner}; "
                        f"a propagation invented a claim this crop's prose never makes")
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}

    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for fam in ("pests", "diseases"):
            if any("control_ladder" in p for p in by[slug].get(fam) or [] if isinstance(p, dict)):
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()

    problem = check_distinctness(batch)
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
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
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
                # ID STABILITY (CLAUDE.md hard rule): an existing id is a join key. Never overwrite.
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
                if not isinstance(p, dict):
                    continue
                if not p.get("control_ladder"):
                    return f"{slug}/{p.get('id')}: no ladder after promote"
                if not p.get("id") or not p.get("type"):
                    return f"{slug}: a problem is missing id or type"

    # the distinctness premise must hold on the PROMOTED data, not only on the staged batch
    sig = {s: json.dumps([[r["method"] for r in p["control_ladder"]]
                          for fam in ("pests", "diseases") for p in by[s].get(fam) or []
                          if isinstance(p, dict)], sort_keys=True) for s in CROPS}
    if len(set(sig.values())) == 1:
        return "the three promoted crops carry identical ladders; a propagation reached canonical"

    for crop, pid, method, want in DISTINCT_CLAIMS:
        lad = ladder_of(by[crop], pid)
        if lad is None:
            return f"post: {crop} has no problem {pid!r}"
        if any(r["method"] == method for r in lad) != want:
            return f"post: {crop}/{pid} {method!r} presence is wrong"

    for owner, needle in PINNED_PROSE:
        for crop in CROPS:
            if (needle in json.dumps(by[crop], ensure_ascii=False)) != (crop == owner):
                return f"post: {needle!r} is on the wrong crop"
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

    print("PLA-8 batch 3 -- the three cucumbers, authored THREE TIMES because they are NOT twins")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  rungs        : {rungs}  ({', '.join(f'{k} {v}' for k, v in EXPECTED_RUNGS.items())})")
    print(f"  ids minted   : {minted}   reused: {reused}")
    print(f"  read-fixes   : {EXPECTED_READ_FIXES}  (batch 1 needed 18, batch 2 needed 0)")
    print(f"  distinctness : {len(DISTINCT_CLAIMS)} crop-distinct claims pinned, "
          f"{len(PINNED_PROSE)} prose claims pinned to their owner")
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
