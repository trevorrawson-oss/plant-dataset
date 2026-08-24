#!/usr/bin/env python3
"""PLA-8 batch 2: promote the four corns. Base 0754031d.

The authored content and the read: tools/staging/pla8_ladder_batch2/ (README.md carries the read's
findings). The staged files are read and NEVER written back.

WHAT MOVES. Four crops gain ladders: sweet-corn, field-corn, popcorn, flint-corn. Each of their 8
problems gains `id`, `type` and `control_ladder`; 22 rungs per crop, 88 total. NO control_method is
touched, NO source is minted, NO crop outside the four. Roster laddered 12 -> 16.

THIS IS THE FIRST FAMILY-CUT BATCH, AND THE PROMOTE ASSERTS THE CLAIM THAT JUSTIFIES IT. The four
staged files are byte-identical: one crop was authored and the ladders propagated mechanically,
because 276 of 288 source field instances across the siblings are byte-identical. `check()` REFUSES
if the four diverge, since a divergence would mean either the propagation broke or the crops are not
actually twins -- and either way the batching premise no longer holds.

NO READ-FIXES ARE APPLIED. Batch 1 needed 18; this batch needed zero, so unlike
promote_pla8_batch1.py there is no delta layer. That is a real difference in the input, not a
shortcut: the read verified 22 of 22 rungs and found no method-meaning mismatch.

REFUSALS: base SHA mismatch; a crop already laddered; the four staged files not identical;
staged/canonical problem-count mismatch; a method not in the catalog; a method whose applies_to
cannot reach the problem's type; a ladder whose tiers decrease; an EMPTY ladder; a rung missing
either register or with identical registers; any prune_out_infection in the batch.

Guard suite:      tools/test_promote_pla8_batch2.py
Mutation harness: tools/mutate_pla8_batch2_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch2.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch2")
BASE_SHA = "0754031d02261241e3ef56dda00f165af884101a85a8673db73016a6b2271263"

CROPS = ("field-corn", "flint-corn", "popcorn", "sweet-corn")
AUTHORED = "sweet-corn"          # the one crop actually authored; the rest are propagated
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_RUNGS_PER_CROP = 22
EXPECTED_PROBLEMS_PER_CROP = 8


def staged():
    """The authored batch, loaded fresh. Never written back."""
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def rung_count(batch):
    return sum(len(p.get("control_ladder") or [])
               for crop in CROPS for fam in ("pests", "diseases")
               for p in batch[crop].get(fam, []))


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


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}

    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for fam in ("pests", "diseases"):
            if any("control_ladder" in p for p in by[slug].get(fam) or [] if isinstance(p, dict)):
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    # THE FAMILY-BATCH PREMISE. If these diverge, either propagation broke or the crops are not
    # twins, and either way the reason this batch was cut this way no longer holds.
    digests = staged_digests()
    if len(set(digests.values())) != 1:
        return (f"the four staged files are NOT identical: "
                f"{ {k: v[:12] for k, v in digests.items()} }; this batch is a twin group and the "
                f"ladders were propagated from {AUTHORED}")

    batch = staged()
    for slug in CROPS:
        for fam in ("pests", "diseases"):
            a, b = len(batch[slug].get(fam, [])), len(by[slug].get(fam) or [])
            if a != b:
                return f"{slug}/{fam}: staged {a} problems, canonical {b}"

    problem = validate_batch(batch, cm)
    if problem:
        return problem

    if rung_count(batch) != EXPECTED_RUNGS_PER_CROP * len(CROPS):
        return (f"rung count {rung_count(batch)}, expected "
                f"{EXPECTED_RUNGS_PER_CROP * len(CROPS)}")
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
    # the four promoted crops must carry IDENTICAL ladders, which is what the twin cut asserts
    sig = {}
    for slug in CROPS:
        sig[slug] = json.dumps(
            [[r["method"] for r in p["control_ladder"]]
             for fam in ("pests", "diseases") for p in by[slug].get(fam) or []
             if isinstance(p, dict)], sort_keys=True)
    if len(set(sig.values())) != 1:
        return "the four promoted crops do not carry identical ladders"
    # raccoons must be laddered; its empty ladder is what exposed the gate hole
    for slug in CROPS:
        for p in by[slug].get("pests") or []:
            if isinstance(p, dict) and p.get("id") == "raccoons":
                if not p.get("control_ladder"):
                    return f"{slug}/raccoons is empty; exclusion_fencing exists to close this"
                if p["control_ladder"][0]["method"] != "exclusion_fencing":
                    return f"{slug}/raccoons does not lead with exclusion_fencing"
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

    print("PLA-8 batch 2 -- the four corns, cut by FAMILY")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  authored     : {AUTHORED} only; the other three are byte-identical propagations")
    print(f"  ids minted   : {minted}   reused: {reused}")
    print(f"  rungs        : {rungs}  ({EXPECTED_RUNGS_PER_CROP} per crop)")
    print(f"  read-fixes   : 0  (batch 1 needed 18; this read found no method-meaning mismatch)")
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
