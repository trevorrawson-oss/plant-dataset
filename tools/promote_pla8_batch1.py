#!/usr/bin/env python3
"""PLA-8 batch 1: apply the READ's 18 fixes to the staged ladders and promote 5 crops. Base 0f911326.

The 18 fixes, their reasons, and the 4 deliberately left open: tools/build_pla8_batch1_content.py
The staged content: tools/staging/pla8_ladder_batch1/out_*.json, read but NEVER edited in place.

WHAT MOVES. Five crops gain ladders: heirloom-tomato, jalapeno, swiss-chard, basil, fig. Each of
their 38 problems gains `id`, `type` and `control_ladder`. One problem gains a source
(jalapeno/pepper-weevil, the mis-anchored trap claim). NO control_method is touched, NO source is
minted, NO crop outside the five is touched. Roster laddered 7 -> 12.

IDS ARE JOIN KEYS. `varieties[].resistance` and `varieties[].ladder_delta` point at problem ids, so
an id minted here is permanent. Where canonical already carries an id, it WINS over the staged one
and a disagreement is reported rather than silently resolved. (These five carry none today; the rule
is enforced anyway, because the day it matters is the day someone re-runs an authoring pass.)

REFUSALS: base SHA mismatch; a crop already laddered; staged/canonical problem-count mismatch; a
fix whose rung index or current method does not match the staged file EXACTLY; a method not in the
catalog; a method whose applies_to cannot reach the problem's type; a ladder whose tiers decrease; a
rung missing either register; any `prune_out_infection` surviving in the batch content; a rung count
that does not match the arithmetic of the fixes.

Guard suite:      tools/test_promote_pla8_batch1.py
Mutation harness: tools/mutate_pla8_batch1_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch1.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch1")
BASE_SHA = "0f911326d2f4ca20c4b92e199afca3c8e842eb8fa422b1b2a1d537a3d20ac093"

CROPS = ("basil", "fig", "heirloom-tomato", "jalapeno", "swiss-chard")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")


def content():
    import build_pla8_batch1_content as B
    return B


def staged():
    """The authored batch, loaded fresh. Never written back."""
    out = {}
    for slug in CROPS:
        out[slug] = json.load(open(os.path.join(STAGING, f"out_{slug}.json")))
    return out


def _lad(batch, crop, pid):
    for fam in ("pests", "diseases"):
        for p in batch[crop].get(fam, []):
            if p.get("id") == pid:
                return p["control_ladder"]
    return None


def fixed_batch():
    """The staged batch with the READ's 18 fixes applied. This is the promoted content."""
    B, batch = content(), staged()

    def check_at(crop, pid, idx, expect):
        L = _lad(batch, crop, pid)
        if L is None:
            raise SystemExit(f"ABORT: {crop}/{pid} not found in staged batch")
        if idx >= len(L):
            raise SystemExit(f"ABORT: {crop}/{pid} has no rung {idx}")
        if L[idx]["method"] != expect:
            raise SystemExit(f"ABORT: {crop}/{pid}#{idx} is {L[idx]['method']!r}, expected {expect!r}")
        return L

    # order matters only within a ladder; every op below is index-checked before it mutates
    for m in B.MERGES:
        L = check_at(m["crop"], m["pid"], m["keep"], "garden_sanitation")
        check_at(m["crop"], m["pid"], m["drop"], "prune_out_infection")
        L[m["keep"]]["note_beginner"] = m["note_beginner"]
        L[m["keep"]]["note_seasoned"] = m["note_seasoned"]
        L.pop(m["drop"])

    for m in B.MERGE_TO:
        L = check_at(m["crop"], m["pid"], m["keep"], "sensible_seeding_rate")
        check_at(m["crop"], m["pid"], m["drop"], "water_at_the_base")
        L[m["keep"]]["method"] = m["to"]
        L[m["keep"]]["note_beginner"] = m["note_beginner"]
        L[m["keep"]]["note_seasoned"] = m["note_seasoned"]
        L.pop(m["drop"])

    for r in B.REPOINTS:
        L = check_at(r["crop"], r["pid"], r["rung"], r["from"])
        L[r["rung"]]["method"] = r["to"]

    for r in B.REPOINT_REWRITES:
        L = check_at(r["crop"], r["pid"], r["rung"], r["from"])
        L[r["rung"]]["method"] = r["to"]
        L[r["rung"]]["note_beginner"] = r["note_beginner"]
        L[r["rung"]]["note_seasoned"] = r["note_seasoned"]

    for s in B.SPLITS:
        cur = _lad(batch, s["crop"], s["pid"])[s["rung"]]["method"]
        expect = s["keep_method"] if s["keep_method"] != "certified_clean_stock" else "garden_sanitation"
        L = check_at(s["crop"], s["pid"], s["rung"], expect)
        L[s["rung"]]["method"] = s["keep_method"]
        L[s["rung"]]["note_beginner"] = s["keep_beginner"]
        L[s["rung"]]["note_seasoned"] = s["keep_seasoned"]
        L.insert(s["insert_at"], {"method": s["new_method"],
                                  "note_beginner": s["new_beginner"],
                                  "note_seasoned": s["new_seasoned"]})

    for e in B.EDIT_NOTES:
        L = check_at(e["crop"], e["pid"], e["rung"], e["expect_method"])
        L[e["rung"]]["note_beginner"] = e["note_beginner"]
        L[e["rung"]]["note_seasoned"] = e["note_seasoned"]

    return batch


def validate_batch(batch, cm):
    """Structural truth about the FIXED batch, before it touches canonical."""
    from control_ladder_gate import TYPE_TARGETS
    order = {t: i for i, t in enumerate(TIERS)}
    rungs = 0
    for crop in CROPS:
        for fam in ("pests", "diseases"):
            for p in batch[crop].get(fam, []):
                lad = p.get("control_ladder") or []
                if not lad:
                    return f"{crop}/{p.get('id')}: empty ladder"
                tiers = []
                for i, r in enumerate(lad):
                    rungs += 1
                    m = r.get("method")
                    if m not in cm:
                        return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                    if m == "prune_out_infection":
                        return (f"{crop}/{p.get('id')}#{i}: prune_out_infection survives; it is a "
                                f"woody cut-back-into-clean-tissue method")
                    targets = TYPE_TARGETS.get(p.get("type")) or set()
                    ok = "any" in cm[m]["applies_to"] or (set(cm[m]["applies_to"]) & targets)
                    if not ok:
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
    return None if rungs else "no rungs at all"


def rung_count(batch):
    return sum(len(p.get("control_ladder") or [])
               for crop in CROPS for fam in ("pests", "diseases")
               for p in batch[crop].get(fam, []))


def check(data):
    B = content()
    cm, sc = data["control_methods"], data["source_catalog"]
    by = {c.get("slug"): c for c in data["crops"]}

    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for fam in ("pests", "diseases"):
            if any("control_ladder" in p for p in by[slug].get(fam) or [] if isinstance(p, dict)):
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = fixed_batch()

    for slug in CROPS:
        for fam in ("pests", "diseases"):
            a, b = len(batch[slug].get(fam, [])), len(by[slug].get(fam) or [])
            if a != b:
                return f"{slug}/{fam}: staged {a} problems, canonical {b}; a problem was added or dropped"

    problem = validate_batch(batch, cm)
    if problem:
        return problem

    # 165 staged, minus 8 merges, minus 1 merge_to, plus 3 splits
    expected = 165 - len(B.MERGES) - len(B.MERGE_TO) + len(B.SPLITS)
    if rung_count(batch) != expected:
        return f"rung arithmetic: {rung_count(batch)} rungs, expected {expected}"

    for s in B.ADD_SOURCES:
        if s["source"] not in sc:
            return f"add_source {s['source']!r} not in source_catalog"
        if sc[s["source"]].get("tier") != "T1":
            return f"add_source {s['source']!r} is not T1"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    B = content()
    batch = fixed_batch()
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

    for s in B.ADD_SOURCES:
        crop = by[s["crop"]]
        for fam in ("pests", "diseases"):
            for p in crop.get(fam) or []:
                if isinstance(p, dict) and p.get("id") == s["pid"]:
                    p.setdefault("sources", [])
                    if s["source"] not in p["sources"]:
                        p["sources"].append(s["source"])
                    p.setdefault("anchoring_urls", {})[s["source"]] = {
                        "url": s["url"], "verified": s["verified"]}
    return minted, reused, rung_count(batch)


def verify_post(data):
    B = content()
    by = {c.get("slug"): c for c in data["crops"]}
    for slug in CROPS:
        n = 0
        for fam in ("pests", "diseases"):
            for p in by[slug].get(fam) or []:
                if not isinstance(p, dict):
                    continue
                if not p.get("control_ladder"):
                    return f"{slug}/{p.get('id')}: no ladder after promote"
                if not p.get("id") or not p.get("type"):
                    return f"{slug}: a problem is missing id or type"
                n += 1
        if not n:
            return f"{slug}: no problems"
    # prune_out_infection must remain reachable ONLY from the two genuine cut-back rungs
    left = set()
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                for r in p.get("control_ladder") or []:
                    if r.get("method") == "prune_out_infection":
                        left.add((c.get("slug"), p.get("id")))
    if left != {("apple", "fire-blight"), ("artichoke", "botrytis-gray-mold")}:
        return f"prune_out_infection reachable from {sorted(left)}"
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

    B = content()
    print("PLA-8 batch 1 -- 5 crops laddered, 18 read-fixes applied")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  ids minted   : {minted}   reused: {reused}")
    print(f"  rungs        : 165 staged -> {rungs} promoted "
          f"({len(B.MERGES)} merges, {len(B.MERGE_TO)} merge-to, {len(B.SPLITS)} splits)")
    print(f"  sources added: {len(B.ADD_SOURCES)}")
    print(f"  still open   : {len(B.STILL_OPEN)} rungs, each with a recorded reason")
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
