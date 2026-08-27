#!/usr/bin/env python3
"""PLA-8 BATCH 9 -- THE ROOTS, second batch of the fall block. Base 043a7272.

29 problems gain `id`, `type` and `control_ladder`; **134 rungs** across `turnip` (49),
`radish` (29), `carrot` (24) and `beet` (32). NO method minted, NO source, no crop outside the
four. Roster laddered 37 -> 41.

**THE AUTHORING RUN DIED AND THE OUTPUTS SURVIVED.** All four agents were killed by a spend
limit AFTER writing their files; the files verified complete against source (counts, families,
types, both registers on every rung). What was lost were the four self-reports, so the read did
that work directly instead of starting from the bots' flags. Full record:
`docs/2026-08-27-pla8-batch9-roots-staging-read.md`.

--------------------------------------------------------------------------------------------------
THE READ'S TWO ADJUDICATIONS
--------------------------------------------------------------------------------------------------
**`handpick` DROPPED from beet's leafminer ladder -- a duplicate action under the wrong key.**
Its note said "pick off any leaf with a pale winding trail", which is the SAME action as its own
`garden_sanitation` rung two places above ("pull off the first tunneled leaves"). `handpick`
MEANS catching free-living insects on a scouting routine, "big enough to spot and slow enough to
catch"; a maggot sealed between leaf surfaces is not handpickable, and spinach filed the same
advice under sanitation in batch 8. The `bottom_watering` shape, found only by reading. The drop
is SCOPED: `handpick` stays on turnip's harlequin bug, where the target is a large visible shield
bug, exactly what the method means.

**beet's `flea-beetle` CONVERGED to `flea-beetles`.** The staged file followed swiss-chard, which
ships the roster's lone singular id; 14 crops ship the plural, including turnip and radish in
this same batch. Beet was at FIRST authoring so the id was free to choose. **swiss-chard is NOT
touched** -- its id is a shipped join key and re-deriving one is forbidden; it stays the outlier
filed in batch 8.

--------------------------------------------------------------------------------------------------
FIVE PROSE-DRIVEN DIVERGENCES, EACH VERIFIED AGAINST THE SOURCE AND PINNED BOTH WAYS
--------------------------------------------------------------------------------------------------
  * COPPER on alternaria leaf spot: turnip YES (its prose names copper), radish NO (its prose
    says "radishes usually grow faster than the disease" and names none).
  * COPPER on downy mildew: turnip and beet YES -- both prose call a copper fungicide "a last
    resort", which is a recommendation, unlike spinach's "limited efficacy" undercut that the
    batch-8 read ruled against.
  * SPINOSAD on flea beetles: turnip and radish YES (prose names it), beet NO (its prose stops
    at kaolin clay).
  * `garden_sanitation` on aphids: turnip YES, beet NO; six of seven prose fields differ.
  * DAMPING-OFF rung count: radish ships 2 rungs and no sanitation, because its prose says to
    re-sow the bare spots and never says to remove collapsed seedlings, unlike the four crops
    that do.

**`prompt_harvest` ON THREE PROBLEMS, DELIBERATELY.** The catalog's documented cases are fruit
crops, but its MEANS is "taking the crop you do want, sooner", and each use restates the crop's
own sentence: radish wireworms ("harvest promptly so roots spend less time exposed"), carrot rust
fly ("harvesting promptly rather than leaving roots in the ground"), carrot cavity spot ("harvest
promptly rather than holding mature roots in wet ground"). Same shape as kaolin_clay and
reflective_mulch, whose documented cases are narrower than their action.

REFUSALS: base SHA mismatch; a crop already laddered; an id off the roster convention, or beet
reverting to the singular; `handpick` on any leafminer ladder, or missing from harlequin bug; any
of the five divergences leveling in either direction; any "diatomaceous" in any note; neem or
soap on any flea-beetles ladder; an unknown method; a tier decrease; applies_to incoherence;
identical registers; problem or rung counts off; any pair of staged files or post-state ladders
byte-identical; any bystander crop, ANY method, or any source changed.

Guard suite:      tools/test_promote_pla8_batch9.py
Mutation harness: tools/mutate_pla8_batch9_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch9.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch9_roots")
BASE_SHA = "043a7272e76d640f287df420d319f209de8bd4443ffa75d327175958bf3b76e0"

CROPS = ("turnip", "radish", "carrot", "beet")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"turnip": 9, "radish": 7, "carrot": 6, "beet": 7}
EXPECTED_RUNGS = {"turnip": 49, "radish": 29, "carrot": 24, "beet": 32}

PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

ID_CONVENTION = {
    "Flea beetles": "flea-beetles",
    "Flea beetle": "flea-beetles",          # beet's singular NAME takes the plural roster id
    "Cabbage maggot": "cabbage-root-maggot",
    "Aphids": "aphids",
    "Harlequin bug": "harlequin-bug",
    "Wireworms": "wireworms",
    "Leafminer (beet and spinach leafminer)": "beet-spinach-leafminer",
    "Carrot rust fly": "carrot-rust-fly",
    "Root-knot nematode": "root-knot-nematode",
    "Clubroot": "clubroot",
    "White rust": "white-rust",
    "Downy mildew": "downy-mildew",
    "Alternaria leaf spot": "alternaria-leaf-spot",
    "Black rot": "black-rot",
    "Damping-off": "damping-off",
    "Leaf blight (Alternaria and Cercospora)": "carrot-leaf-blight",
    "Aster yellows": "aster-yellows",
    "Cavity spot": "cavity-spot",
    "Cercospora leaf spot": "cercospora-leaf-spot",
    "Scab": "common-scab",
}

LEAFMINER = "beet-spinach-leafminer"
FB = "flea-beetles"
# The five divergences, as (problem id, method) -> crops that MUST carry it / MUST NOT.
COPPER_ALTERNARIA_YES, COPPER_ALTERNARIA_NO = ("turnip",), ("radish",)
COPPER_DOWNY_YES = ("turnip", "beet")
SPINOSAD_FB_YES, SPINOSAD_FB_NO = ("turnip", "radish"), ("beet",)
APHID_SANITATION_YES, APHID_SANITATION_NO = ("turnip",), ("beet",)
DAMPING_OFF_RUNGS = {"radish": 2, "carrot": 3, "beet": 3}
# prompt_harvest's three deliberate uses, each restating its crop's own harvest-sooner sentence.
PROMPT_HARVEST_USES = (("radish", "wireworms"), ("carrot", "carrot-rust-fly"),
                       ("carrot", "cavity-spot"))


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def problems(obj):
    return [(fam, p) for fam in ("pests", "diseases") for p in (obj.get(fam) or [])
            if isinstance(p, dict)]


def rung_count(batch):
    return sum(len(p.get("control_ladder") or []) for s in CROPS for _, p in problems(batch[s]))


def ladder_of(obj, pid):
    for _, p in problems(obj):
        if p.get("id") == pid:
            return [r["method"] for r in p.get("control_ladder") or []], p
    return None, None


def prose_signature(crop):
    return [tuple(json.dumps(p.get(f), sort_keys=True) for f in PROSE_FIELDS)
            for _, p in problems(crop)]


def ladder_signature(obj):
    return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                        for r in p["control_ladder"]] for _, p in problems(obj)], sort_keys=True)


def check_not_twins(by):
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if prose_signature(by[a]) == prose_signature(by[b]):
                return (f"{a} and {b} are byte-identical in canonical, a TRUE TWIN; author one and "
                        f"propagate rather than authoring both")
    dg = staged_digests()
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if dg[a] == dg[b]:
                return (f"the staged files for {a} and {b} are byte-identical, so one was copied; "
                        f"each crop needs its own authoring pass")
    return None


def check_read_fixes(batch, by):
    """The read's adjudications and the five divergences, pinned. `by` is the CANONICAL crop map;
    staged problems carry no `name`, so names resolve from canonical at the same index."""
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return (f"{slug}: problem {name!r} is not in the id-convention table; add its "
                        f"roster ruling before promoting")
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention "
                        f"ships {want!r}; ids are join keys and must not diverge between crops")

    # ADJUDICATION 1: handpick off the leafminer, and SCOPED (it stays where it belongs).
    ms, _ = ladder_of(batch["beet"], LEAFMINER)
    if ms is None:
        return "beet has no leafminer problem"
    if "handpick" in ms:
        return ("beet/beet-spinach-leafminer carries handpick, whose meaning is catching "
                "free-living insects on a scouting routine; a maggot sealed inside a leaf is not "
                "handpickable, and the rung duplicated the crop's own garden_sanitation action")
    if "garden_sanitation" not in ms:
        return ("beet/beet-spinach-leafminer lost garden_sanitation, which is where removing "
                "mined leaves belongs and where spinach files the same advice")
    ms, _ = ladder_of(batch["turnip"], "harlequin-bug")
    if ms is None or "handpick" not in ms:
        return ("turnip/harlequin-bug lost handpick; the drop was scoped to a wrong-meaning "
                "target, not a blanket removal, and a shield bug is exactly what the method means")

    # ADJUDICATION 2 (the flea-beetles convergence) needs NO check here: the ID_CONVENTION loop
    # above maps beet's singular NAME to the plural id and refuses anything else by name, so a
    # second singular-specific check would be dead code below a stronger neighbour. The post-side
    # equivalent IS reachable (nothing re-derives ids there) and lives in verify_post.

    # THE FIVE DIVERGENCES, both directions.
    for slug in COPPER_ALTERNARIA_YES:
        ms, _ = ladder_of(batch[slug], "alternaria-leaf-spot")
        if ms is None or "copper_fungicide" not in ms:
            return f"{slug}/alternaria-leaf-spot lost its copper rung; its prose names copper"
    for slug in COPPER_ALTERNARIA_NO:
        ms, _ = ladder_of(batch[slug], "alternaria-leaf-spot")
        if ms is None or "copper_fungicide" in ms:
            return (f"{slug}/alternaria-leaf-spot carries copper; its prose names none and says "
                    f"radishes usually grow faster than the disease")
    for slug in COPPER_DOWNY_YES:
        ms, _ = ladder_of(batch[slug], "downy-mildew")
        if ms is None or "copper_fungicide" not in ms:
            return (f"{slug}/downy-mildew lost its copper rung; its prose calls copper a last "
                    f"resort, which is a recommendation")
    for slug in SPINOSAD_FB_YES:
        ms, _ = ladder_of(batch[slug], FB)
        if ms is None or "spinosad" not in ms:
            return f"{slug}/{FB} lost spinosad; its prose names it"
    for slug in SPINOSAD_FB_NO:
        ms, _ = ladder_of(batch[slug], FB)
        if ms is None or "spinosad" in ms:
            return f"{slug}/{FB} carries spinosad; its prose stops at kaolin clay"
    for slug in APHID_SANITATION_YES:
        ms, _ = ladder_of(batch[slug], "aphids")
        if ms is None or "garden_sanitation" not in ms:
            return f"{slug}/aphids lost garden_sanitation, which its own prose supports"
    for slug in APHID_SANITATION_NO:
        ms, _ = ladder_of(batch[slug], "aphids")
        if ms is None or "garden_sanitation" in ms:
            return f"{slug}/aphids gained garden_sanitation; its prose does not carry it"
    for slug, n in DAMPING_OFF_RUNGS.items():
        ms, _ = ladder_of(batch[slug], "damping-off")
        if ms is None or len(ms) != n:
            return (f"{slug}/damping-off has {ms and len(ms)} rungs, expected {n}; radish's prose "
                    f"re-sows bare spots and never says to remove collapsed seedlings")

    # prompt_harvest's three deliberate uses.
    for slug, pid in PROMPT_HARVEST_USES:
        ms, _ = ladder_of(batch[slug], pid)
        if ms is None or "prompt_harvest" not in ms:
            return (f"{slug}/{pid} lost prompt_harvest; its own prose says to harvest promptly "
                    f"rather than leave the roots in the ground")

    # Batch-wide standing refusals.
    for slug in CROPS:
        ms, _ = ladder_of(batch[slug], FB)
        if ms is not None and ("neem_oil" in ms or "insecticidal_soap" in ms):
            return (f"{slug}/{FB} carries a soft-bodied contact spray; a hard-shelled beetle is "
                    f"the bottom_watering shape, refused batch-wide since batch 7")
        for _, p in problems(batch[slug]):
            for r in p.get("control_ladder") or []:
                if "diatomaceous" in (r.get("note_beginner", "") + " " +
                                      r.get("note_seasoned", "")).lower():
                    return (f"{slug}/{p.get('id')}: a note mentions diatomaceous earth, the "
                            f"deliberately-unminted method")
    return None


def check_catalog_premises(cm):
    spin = " ".join(cm.get("spinosad", {}).get("cautions") or [])
    if "dusk" not in spin:
        return "spinosad's dusk caution is not on the sheet; this batch's spinosad rungs restate it"
    m = cm.get("prompt_harvest") or {}
    if "sooner" not in (m.get("best_use") or ""):
        return ("prompt_harvest's best_use no longer states the harvest-sooner action this batch "
                "relies on for wireworms, rust fly and cavity spot")
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    order = {t: i for i, t in enumerate(TIERS)}
    for crop in CROPS:
        n_prob = 0
        for _, p in problems(batch[crop]):
            n_prob += 1
            if not p.get("id") or not p.get("type"):
                return f"{crop}: a problem is missing id or type"
            lad = p.get("control_ladder")
            if lad is None:
                return f"{crop}/{p.get('id')}: no control_ladder"
            if not lad:
                return f"{crop}/{p.get('id')}: control_ladder is EMPTY"
            tiers, seen = [], set()
            for i, r in enumerate(lad):
                m = r.get("method")
                if m not in cm:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                if m in seen:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} appears twice in one ladder"
                seen.add(m)
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

    problem = check_catalog_premises(cm)
    if problem:
        return problem
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()
    for problem in (check_not_twins(by), check_read_fixes(batch, by)):
        if problem:
            return problem
    for slug in CROPS:
        a, b = len(problems(batch[slug])), len(problems(by[slug]))
        if a != b:
            return f"{slug}: staged {a} problems, canonical {b}"
    problem = validate_batch(batch, cm)
    if problem:
        return problem
    for slug in CROPS:
        n = sum(len(p.get("control_ladder") or []) for _, p in problems(batch[slug]))
        if n != EXPECTED_RUNGS[slug]:
            return f"{slug}: {n} rungs, expected {EXPECTED_RUNGS[slug]}"
    if rung_count(batch) != sum(EXPECTED_RUNGS.values()):
        return f"rung count {rung_count(batch)}, expected {sum(EXPECTED_RUNGS.values())}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"crops": {c.get("slug"): dump(c) for c in data["crops"]},
            "methods": dump(data["control_methods"]),
            "sources": dump(data["source_catalog"])}


def apply_to(data):
    batch = staged()
    by = {c.get("slug"): c for c in data["crops"]}
    minted = reused = 0
    for slug in CROPS:
        crop = by[slug]
        for fam in ("pests", "diseases"):
            adds = [p for p in (batch[slug].get(fam) or []) if isinstance(p, dict)]
            for i, add in enumerate(adds):
                tgt = crop[fam][i]
                if isinstance(tgt.get("id"), str) and tgt["id"]:
                    reused += 1
                else:
                    tgt["id"] = add["id"]
                    minted += 1
                tgt["type"] = add["type"]
                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])
    return minted, reused, rung_count(batch)


def verify_post(pre, data):
    by = {c.get("slug"): c for c in data["crops"]}
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST (unreachable below the bystander loops -- seventh time stated).
    for slug in CROPS:
        for _, p in problems(by[slug]):
            if p.get("id") == "flea-beetle":
                return f"post: {slug} shipped the singular flea-beetle id"
            if not p.get("control_ladder"):
                return f"post: {slug}/{p.get('id')}: no ladder after promote"
            for r in p["control_ladder"]:
                if "diatomaceous" in (r["note_beginner"] + " " + r["note_seasoned"]).lower():
                    return f"post: {slug}/{p.get('id')}: a diatomaceous earth mention landed"

    ms, _ = ladder_of(by["beet"], LEAFMINER)
    if "handpick" in ms:
        return "post: beet's leafminer regained the wrong-meaning handpick rung"
    ms, _ = ladder_of(by["turnip"], "harlequin-bug")
    if "handpick" not in ms:
        return "post: turnip's harlequin bug lost handpick; the drop was scoped"
    for slug in COPPER_DOWNY_YES:
        ms, _ = ladder_of(by[slug], "downy-mildew")
        if "copper_fungicide" not in ms:
            return f"post: {slug}/downy-mildew lost its copper rung"
    for slug in COPPER_ALTERNARIA_NO:
        ms, _ = ladder_of(by[slug], "alternaria-leaf-spot")
        if "copper_fungicide" in ms:
            return f"post: {slug}/alternaria-leaf-spot gained a copper rung its prose refuses"
    for slug in SPINOSAD_FB_NO:
        ms, _ = ladder_of(by[slug], FB)
        if "spinosad" in ms:
            return f"post: {slug}/{FB} gained spinosad its prose does not name"
    for slug, pid in PROMPT_HARVEST_USES:
        ms, _ = ladder_of(by[slug], pid)
        if "prompt_harvest" not in ms:
            return f"post: {slug}/{pid} lost prompt_harvest"
    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints and edits nothing there"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"

    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):
                return (f"post: {CROPS[i]} and {CROPS[j]} carry identical ladder CONTENT; they "
                        f"were authored separately and their prose differs")
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
    minted, reused, rungs = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 BATCH 9 -- THE ROOTS (fall block, batch 2 of 5)")
    print(f"  crops        : {', '.join(CROPS)}  (FOUR authoring passes)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused; beet converged to flea-beetles")
    print(f"  read rulings : handpick OFF beet's leafminer (duplicate action, wrong meaning),")
    print(f"                 KEPT on turnip's harlequin bug; 5 prose divergences pinned both ways")
    print(f"  blast radius : 4 crops; methods 0; sources 0; bystanders 0")
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
