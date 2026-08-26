#!/usr/bin/env python3
"""PLA-8 BATCH 6 -- the two peas. Base 17d0eac7.

16 problems gain `id`, `type` and `control_ladder`; **84 rungs** (42 + 42) across `snow-peas` and
`sugar-snap-peas`. 172 register strings. No control_method, no source, no crop outside the two.
Roster laddered 27 -> 29.

**TWO AUTHORING PASSES FOR TWO CROPS.** There is no twin here and there is no twin left anywhere:
batch 5 consumed the last one. These two share all eight problem NAMES and 82.8% of their prose, so
each was authored independently, and the promote asserts the shape it actually is -- see
`check_not_twins`, which refuses in the direction opposite to batch 5's. If these two ever became
byte-identical, propagation would be available and this batch would be doing double work; if the
staged outputs are identical, one was copied. Both are refused.

--------------------------------------------------------------------------------------------------
THE READ, AND ITS ONE REAL FINDING
--------------------------------------------------------------------------------------------------
**`wet_foliage_discipline` DROPPED from both powdery-mildew ladders.** Both passes authored the rung
and BOTH independently flagged the record as self-contradictory: `cause_seasoned` says the fungus is
"favored by warm days, cool nights, and dry foliage" and that "Spores spread on the wind", while
`prevention_seasoned` says to "avoid working among wet vines". Both wrote the note with NO mechanism
stated because neither could restate a mechanism the entry undercuts. That refusal to invent is what
surfaced it.

The method's own mechanism is free-water transport, and USU says powdery mildews "do not spread in
rain or free water". The catalog now says so on the sheet (`99a19c6`), and this promote requires
that caution to be present before it will run: shipping the ladder without it would leave the trap
in place for the next batch.

**THE DROP IS SCOPED, NOT A BLANKET REMOVAL, AND BOTH HALVES ARE PINNED.**
  * NOT on powdery-mildew, on either crop.
  * STILL on ascochyta-blight, on both crops, where the entry's own cause says "Cool, wet weather
    and splashing water spread them".
  * `airflow_spacing` STAYS on powdery-mildew, because its own `best_use` names powdery mildew and
    humidity rather than free water is what it acts on.
Right use and wrong use of one method, in one crop, held apart by guards.

**Two orderings normalized on `snow-peas`** (root rots, ascochyta blight), where the cross-sibling
check flagged same-method-set-different-order on prose that is 8-of-8 and 7-of-8 identical across
the two crops. Same-tier moves; direction taken from the source's own order, which `sugar-snap-peas`
already matched. Cross-sibling conflicts went 2 -> 0.

--------------------------------------------------------------------------------------------------
THIS BATCH IS WHERE THREE CATALOG ROUNDS GET TESTED AGAINST REAL DATA
--------------------------------------------------------------------------------------------------
  * **r6** corrected `planting_time_avoidance.best_use` from "one main generation" to a predictable
    damage window. Pea weevil has ONE generation a year and a bloom-timed flight, so it is the clean
    case the corrected wording has to admit -- pinned on both crops.
  * **r7** REFUSED to widen that method to a disease target after six T1 documents came back empty.
    Both passes then hit exactly that wall on powdery mildew and reported it. The refusal is
    observable here as data: `planting_time_avoidance` appears on pea-weevil and on no fungal
    problem. Pinned.
  * **r7's mints** are both consumed: `biofungicide` on powdery mildew (the crop's own prose names
    "Sulfur or a labeled biofungicide"), `weed_host_control` on pea aphid and thrips.

REFUSALS: base SHA mismatch; a crop already laddered; the two crops identical in canonical or as
staged; problem-count drift; a rung count off; an unknown method; a tier decrease; applies_to
incoherence; identical registers; an id disagreeing with the roster; any read fix regressed; the
powdery-mildew caution absent from the catalog; any r6/r7 pin missing; any crop outside the two
changed.

Guard suite:      tools/test_promote_pla8_batch6.py
Mutation harness: tools/mutate_pla8_batch6_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch6.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch6")
BASE_SHA = "17d0eac762fc22b07fb5ec6a83c9f08471202e3c5ddf9bb7010fc861af5f0688"

CROPS = ("snow-peas", "sugar-snap-peas")   # a shared-name family at 82.8%: TWO authoring passes
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {s: 8 for s in CROPS}
EXPECTED_RUNGS = {s: 42 for s in CROPS}

PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

# Ids already shipped elsewhere on the roster for the same problem NAME. A disagreement is a
# join-key defect: varieties[].resistance and ladder_delta point at these strings.
ID_CONVENTION = {"Powdery mildew": "powdery-mildew", "Fusarium wilt": "fusarium-wilt"}

PM = "powdery-mildew"
ASC = "ascochyta-blight"
WFD = "wet_foliage_discipline"

# The catalog rounds this batch exercises, as (problem id -> method) pins on EVERY crop.
R7_USE = {PM: "biofungicide", "pea-aphid": "weed_host_control", "thrips": "weed_host_control"}
R6_USE = {"pea-weevil": "planting_time_avoidance"}


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


def check_not_twins(by, batch):
    """THE OPPOSITE OF BATCH 5's PREMISE, AND IT HAS TO BE ASSERTED JUST AS HARD.

    Batch 5 propagated one crop's ladders onto another because their prose was byte-identical, and
    proved that identity in canonical. These two are a shared-name family at 82.8%: they were
    authored independently, and the claim this batch rests on is that they are NOT the same crop.

    Refused in both directions. If canonical ever makes them identical, propagation is available and
    this batch is doing double work. If the two STAGED outputs are identical, one was copied from
    the other and the second pass did not happen.
    """
    a, b = prose_signature(by[CROPS[0]]), prose_signature(by[CROPS[1]])
    if a == b:
        return (f"{CROPS[0]} and {CROPS[1]} are byte-identical in canonical, so they are a TRUE "
                f"TWIN and this batch should author one and propagate, not author both")
    dg = staged_digests()
    if dg[CROPS[0]] == dg[CROPS[1]]:
        return (f"the two staged files are byte-identical, so one was copied from the other; these "
                f"crops share 82.8% of their prose and each needs its own authoring pass")
    return None


def check_read_fixes(batch, by):
    """The read's one real finding, plus the two orderings, plus the pins that keep the drop scoped.

    `by` is the CANONICAL crop map and is required: the staged files carry only
    {id, type, control_ladder} with no `name`, so a problem's name resolves from canonical at the
    same index. Reading `name` off the staged problem is the dead-guard shape batch 4 shipped.
    """
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want and p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the roster ships "
                        f"{want!r}; ids are join keys and must not diverge between passes")

        # THE FINDING: the method's mechanism is free-water transport and powdery mildew does not
        # travel that way. Dropped here, kept where it belongs.
        mpm, _ = ladder_of(batch[slug], PM)
        if mpm is None:
            return f"{slug} has no {PM} problem"
        if WFD in mpm:
            return (f"{slug}/{PM} carries {WFD}, whose mechanism is free moisture as a transport "
                    f"medium; USU states that powdery mildews do not spread in rain or free water, "
                    f"and this crop's own cause field says the fungus is favored by dry foliage and "
                    f"that spores spread on the wind")
        if "airflow_spacing" not in mpm:
            return (f"{slug}/{PM} lost airflow_spacing, which is the method that SHOULD carry the "
                    f"canopy case here and which names powdery mildew in its own best_use")

        # THE DROP IS SCOPED. The same method must survive where splash dispersal is the crop's own
        # stated mechanism, or this was a blanket removal rather than an adjudication.
        masc, _ = ladder_of(batch[slug], ASC)
        if masc is None:
            return f"{slug} has no {ASC} problem"
        if WFD not in masc:
            return (f"{slug}/{ASC} lost {WFD}; that entry's own cause says cool, wet weather and "
                    f"splashing water spread it, so the drop on powdery mildew must not have been "
                    f"applied as a blanket removal")

    # The two orderings the cross-sibling check flagged, on prose identical across both crops.
    for slug in CROPS:
        mrr, _ = ladder_of(batch[slug], "root-rots-damping-off")
        if mrr is None:
            return f"{slug} has no root-rots-damping-off problem"
        # The peas read drainage-then-sowing ("well-drained soil or raised beds ... and never sow
        # peas into soggy ground"), which is the OPPOSITE of the beans in batch 5. Order follows
        # each crop's own prose, not a house convention.
        if mrr.index("improve_drainage") > mrr.index("sound_sowing_practice"):
            return (f"{slug}/root-rots-damping-off: improve_drainage must precede "
                    f"sound_sowing_practice, the order both crops' identical prevention prose uses")
        if mrr[-1] != "resistant_varieties":
            return (f"{slug}/root-rots-damping-off: the partial-tolerance rung belongs last, where "
                    f"the prose puts it as a supplementary hedge")
        masc, _ = ladder_of(batch[slug], ASC)
        if masc.index("garden_sanitation") > masc.index("crop_rotation"):
            return (f"{slug}/{ASC}: garden_sanitation must precede crop_rotation, the order both "
                    f"crops' identical prevention prose uses")
    return None


def check_rounds_are_exercised(batch):
    """r6 corrected a method's criterion and r7 refused to widen it. Both are observable here."""
    for pid, method in list(R7_USE.items()) + list(R6_USE.items()):
        for slug in CROPS:
            ms, _ = ladder_of(batch[slug], pid)
            if ms is None:
                return f"{slug} has no {pid} problem, so {method} cannot be checked"
            if method not in ms:
                return (f"{slug}/{pid} does not use {method}; that method was minted, corrected or "
                        f"widened by a catalog round taken specifically for this batch's prose")
    # r7's refusal, observable as data: the timing method reaches an insect and no disease.
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            ms = [r["method"] for r in p.get("control_ladder") or []]
            if "planting_time_avoidance" in ms and p.get("type") != "insect":
                return (f"{slug}/{p.get('id')} is typed {p.get('type')!r} and carries "
                        f"planting_time_avoidance, a widening r7 REFUSED after six T1 documents "
                        f"came back empty")
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

    # The r8 caution must already be on the sheet. Shipping these ladders without it would leave
    # the trap in place for the 21 other crops whose powdery mildew carries wet-handling advice.
    if WFD not in cm:
        return f"{WFD} is not in the catalog"
    if not any("powdery mildew" in c.lower() for c in (cm[WFD].get("cautions") or [])):
        return (f"{WFD} does not carry the powdery-mildew exception; the catalog round that states "
                f"it must land before these ladders ship")
    for method in set(R7_USE.values()) | set(R6_USE.values()):
        if method not in cm:
            return f"{method} is not in the catalog; its catalog round must land first"

    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()
    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by),
                    check_rounds_are_exercised(batch)):
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

    # SUBSTANTIVE INVARIANTS FIRST. Below the bystander loop they are unreachable, because a change
    # to either crop IS a change to a crop. Fourth time this arc has had to make that ordering.
    for slug in CROPS:
        mpm, _ = ladder_of(by[slug], PM)
        if WFD in mpm:
            return f"post: {slug}/{PM} regained {WFD}"
        if "airflow_spacing" not in mpm:
            return f"post: {slug}/{PM} lost airflow_spacing"
        masc, _ = ladder_of(by[slug], ASC)
        if WFD not in masc:
            return f"post: {slug}/{ASC} lost {WFD}; the drop was scoped to powdery mildew"
        for pid, method in list(R7_USE.items()) + list(R6_USE.items()):
            mm, _ = ladder_of(by[slug], pid)
            if method not in mm:
                return f"post: {slug}/{pid} lost its {method} rung"
        for _, p in problems(by[slug]):
            if not p.get("control_ladder"):
                return f"post: {slug}/{p.get('id')}: no ladder after promote"

    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints no method"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote mints no source"

    def sig(s):
        return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                            for r in p["control_ladder"]] for _, p in problems(by[s])],
                          sort_keys=True)
    if sig(CROPS[0]) == sig(CROPS[1]):
        return ("post: the two crops carry identical ladder CONTENT; they were authored separately "
                "and their prose must differ")
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

    print("PLA-8 BATCH 6 -- the two peas")
    print(f"  crops        : {', '.join(CROPS)}  (shared-name family at 82.8%, TWO authoring passes)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused")
    print(f"  read finding : {WFD} DROPPED from powdery mildew, KEPT on ascochyta")
    print(f"  methods      : 0 touched   sources: 0 touched   crops outside the two: 0")
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
