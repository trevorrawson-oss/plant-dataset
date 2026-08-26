#!/usr/bin/env python3
"""PLA-8 BATCH 5 -- the three beans. Base acf33780.

27 problems gain `id`, `type` and `control_ladder`; **131 rungs** (44 + 44 + 43) across `dry-bean`,
`green-beans-bush` and `pole-beans`. No control_method, no source, no crop outside the three.
Roster laddered 24 -> 27.

THE LAST TRUE TWIN ON THE ROSTER, AND THE PROMOTE ASSERTS THE PREMISE IN CANONICAL, NOT JUST IN THE
STAGED FILES. `dry-bean` and `green-beans-bush` carry byte-identical problem prose in order, so one
crop was authored and the other propagated. Batch 4 asserted that premise by comparing the two
STAGED files, which proves the propagation happened but not that it was legitimate. This one checks
the source of the claim: `check_twin_premise` compares the ELEVEN prose fields of all nine problems
straight out of canonical and refuses if they are not identical, and separately refuses if
`pole-beans` does NOT differ. If a future edit makes the beans diverge, this promote stops being
correct and says so, rather than propagating over a premise that has quietly expired.

**TWO AUTHORING PASSES FOR THREE CROPS.** `pole-beans` shares the same nine problem names but only
75.7% of the prose, so it was authored independently. Measured, not assumed: 35 field pairs differ
across the nine problems.

FOUR READ FIXES, EACH PINNED SO IT CANNOT REGRESS (`check_read_fixes`, and again in `verify_post`):

  1. **pole-beans / mexican-bean-beetle: `off_season_tillage` -> `garden_sanitation`.** The batch-1
     defect class. The seasoned clause is BYTE-IDENTICAL on both siblings ("Work crop debris into
     the soil promptly after harvest to remove overwintering shelter") and the two passes filed it
     under different keys. `off_season_tillage` MEANS destroying soil-pupating stages -- its own
     text says "the pupal cells of soil-pupating Lepidoptera such as the hornworms". Mexican bean
     beetle overwinters as ADULTS near woodland edges, which both crops' own `cause` field states.
     Same-sounding action, wrong mechanism. The pole-beans pass flagged this itself and used the key
     anyway: third batch running where a self-flagged loose fit was a real mismatch.
  2 + 3. **green-beans-bush ordering**, on Anthracnose and Bean root rots. The cross-sibling check
     flagged both: same method SET, different order, and the prevention prose the differing rungs
     are built from is byte-identical across the two crops. Same-tier moves, so no claim is added or
     removed. Direction taken from the SOURCE's own order, not from the sibling.
  4. **green-beans-bush / bean-root-rots: the root-injury clause leaves `sound_sowing_practice`.**
     That method's `best_use` ENUMERATES its scope -- "seed quality, depth, soil warmth and
     restrained watering". Handling damage at planting is outside the list. The crop's prose does say
     "Avoid damaging the roots when planting", so it is a real sourced control with no catalog home;
     it is recorded as a gap rather than stretched onto the nearest key. The pole-beans pass refused
     it for the same reason.

A DIVERGENCE THAT IS CORRECT AND IS PINNED AS SUCH: `augmentative_release` appears on the twin's
Mexican bean beetle ladder and NOT on pole-beans'. The twin's prose names the wasp in both registers
("a tiny helper wasp is sold to control them" / "the parasitic wasp Pediobius foveolatus is sold for
biological control"); pole-beans' prose names it in neither. Pinned in BOTH directions, so a later
pass cannot quietly propagate it across or drop it.

THIS IS THE FIRST BATCH AUTHORED AGAINST THE r5 CATALOG ROUND, so the promote requires the three
methods that round produced or widened to actually be reachable here: `planting_time_avoidance` on
Mexican bean beetle, `wet_foliage_discipline` on the bacterial blights, and `balance_nitrogen` on
white mold. Minting a method the batch then does not use would mean the round was not needed.

ID CONVENTION. Three of the nine ids already ship elsewhere on the roster and must match, because a
`pests[]`/`diseases[]` id is a join key: `aphids` (13x), `anthracnose` (5x),
`two-spotted-spider-mite` (1x, strawberry). Checked against the roster's shipped spelling for the
same problem NAME.

RECORDED, NOT THIS BATCH'S TO FIX: the roster carries three spellings for spider mites
(`spider-mites` 4x, `two-spotted-spider-mite` 1x, `twospotted-spider-mite` 1x) and two for flea
beetles. Every one of them faithfully slugs its OWN crop's problem name, so the ids are internally
correct and the divergence is in the NAMES across crops, not in how ids are derived. Nothing joins
across crops today, so it costs nothing yet; a cross-crop query on spider mites would miss two of
six.

REFUSALS: base SHA mismatch; a crop already laddered; the twin premise failing in canonical;
pole-beans matching the twin; the staged twin files diverging; a staged file not matching its
sibling's expected identity; problem-count drift against canonical; a rung count off; an unknown
method; a tier decrease; applies_to incoherence; identical registers; an id disagreeing with the
roster; any read fix regressed; any of the r5 methods unreachable; any crop outside the three
changed.

Guard suite:      tools/test_promote_pla8_batch5.py
Mutation harness: tools/mutate_pla8_batch5_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch5.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch5")
BASE_SHA = "acf337809d9085f748bc45b6dfc38dd9c7e88fb92b1408f53879c6bdc0f970a7"

TWIN = ("dry-bean", "green-beans-bush")   # byte-identical prose in order: one pass, propagated
SIBLING = "pole-beans"                    # 75.7%: its own authoring pass
CROPS = TWIN + (SIBLING,)
AUTHORED = "green-beans-bush"

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {s: 9 for s in CROPS}
EXPECTED_RUNGS = {"dry-bean": 44, "green-beans-bush": 44, "pole-beans": 43}

# The eleven per-problem fields the twin premise rests on. `control_ladder` is deliberately NOT here:
# it is what this promote writes, so including it would make the premise self-referential.
PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

# The roster's shipped spelling for problems this batch also carries. A disagreement is a join-key
# defect, not a style nit: varieties[].resistance and ladder_delta point at these strings.
ID_CONVENTION = {"Aphids": "aphids", "Anthracnose": "anthracnose",
                 "Two-spotted spider mite": "two-spotted-spider-mite"}

# r5's round has to be reachable in this batch, or minting it was not justified.
R5_USE = {"mexican-bean-beetle": "planting_time_avoidance",
          "bacterial-blights": "wet_foliage_discipline",
          "white-mold": "balance_nitrogen"}

MBB = "mexican-bean-beetle"
ROOT_INJURY_TOKENS = ("damage the roots", "root injury")


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


def ladder_of(batch_or_crop, pid):
    for _, p in problems(batch_or_crop):
        if p.get("id") == pid:
            return [r["method"] for r in p.get("control_ladder") or []], p
    return None, None


def prose_signature(crop):
    """The problem prose, in order. The premise the twin propagation rests on."""
    return [tuple(json.dumps(p.get(f), sort_keys=True) for f in PROSE_FIELDS)
            for _, p in problems(crop)]


def check_twin_premise(by):
    """ASSERT THE PREMISE IN CANONICAL, not in the staged output.

    Comparing the two staged files proves a propagation happened; it says nothing about whether it
    was legitimate. What licenses copying one crop's ladders onto another is that their SOURCE prose
    is identical, and that lives in canonical. Checked in both directions: the twin must match, and
    the sibling must NOT, because a sibling that has quietly become identical would mean this batch
    is authoring the same crop twice.
    """
    a, b = prose_signature(by[TWIN[0]]), prose_signature(by[TWIN[1]])
    if len(a) != len(b):
        return f"the twin {TWIN} carry different problem counts ({len(a)} vs {len(b)})"
    if a != b:
        bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        return (f"the twin premise FAILS in canonical: {TWIN} differ on problem index/es {bad}. "
                f"One crop is authored and the other propagated, which is only legitimate while "
                f"their prose is byte-identical in order")
    c = prose_signature(by[SIBLING])
    if c == a:
        return (f"{SIBLING} is byte-identical to the twin in canonical, so it is not a separate "
                f"authoring pass; the batch shape is wrong")
    return None


def check_grouping(batch):
    """The staged files carry the twin identity forward, and the sibling stays distinct."""
    dg = staged_digests()
    if dg[TWIN[0]] != dg[TWIN[1]]:
        return (f"the twin pair {TWIN} is NOT byte-identical as staged ({dg[TWIN[0]][:12]} vs "
                f"{dg[TWIN[1]][:12]}); one crop is authored and the other propagated")
    if dg[SIBLING] == dg[TWIN[0]]:
        return (f"{SIBLING} is byte-identical to the twin pair; it shares 75.7% of their prose and "
                f"must be authored separately, not propagated across the family")
    return None


def check_read_fixes(batch, by):
    """The four fixes the READ applied, plus the one divergence it ruled CORRECT.

    `by` is the CANONICAL crop map and is required, not optional: the staged files carry only
    {id, type, control_ladder} with no `name`, so a problem's name has to be resolved from canonical
    at the same index. Batch 4's version read `p.get("name")` off the staged problem, which is
    always None, so its id guard never fired once while reading as coverage.
    """
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want and p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the roster ships "
                        f"{want!r}; ids are join keys and must not diverge between passes")

    # FIX 1 -- the method-meaning correction on the sibling.
    ms, _ = ladder_of(batch[SIBLING], MBB)
    if ms is None:
        return f"{SIBLING} has no {MBB} problem"
    if "off_season_tillage" in ms:
        return (f"{SIBLING}/{MBB} carries off_season_tillage, whose mechanism is soil-pupating "
                f"stages; this beetle overwinters as adults near woodland edges")
    if "garden_sanitation" not in ms:
        return f"{SIBLING}/{MBB} lost the garden_sanitation rung the read installed"

    for slug in TWIN:
        # FIX 2 -- anthracnose ordering.
        ma, _ = ladder_of(batch[slug], "anthracnose")
        if ma is None:
            return f"{slug} has no anthracnose problem"
        if not (ma.index("garden_sanitation") < ma.index("water_at_the_base")):
            return (f"{slug}/anthracnose: garden_sanitation must precede water_at_the_base, the "
                    f"order its own prevention prose uses and the order the sibling carries")
        # FIX 3 -- root-rot ordering.
        mr, pr = ladder_of(batch[slug], "bean-root-rots")
        if mr is None:
            return f"{slug} has no bean-root-rots problem"
        if not (mr.index("sound_sowing_practice") < mr.index("improve_drainage")):
            return (f"{slug}/bean-root-rots: sound_sowing_practice must precede improve_drainage, "
                    f"the order its own prevention prose uses")
        # FIX 4 -- the root-injury claim is out of sound_sowing_practice.
        for r in pr["control_ladder"]:
            if r["method"] != "sound_sowing_practice":
                continue
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            for tok in ROOT_INJURY_TOKENS:
                if tok in blob:
                    return (f"{slug}/bean-root-rots: sound_sowing_practice claims {tok!r}, which is "
                            f"outside its enumerated scope (seed quality, depth, soil warmth, "
                            f"restrained watering); that control has no catalog home and is "
                            f"recorded as a gap, not stretched onto the nearest key")

    # THE DIVERGENCE THAT IS CORRECT, pinned in BOTH directions.
    for slug in TWIN:
        mt, _ = ladder_of(batch[slug], MBB)
        if "augmentative_release" not in mt:
            return (f"{slug}/{MBB} lost augmentative_release; this crop's prose names the parasitic "
                    f"wasp in both registers")
    if "augmentative_release" in ms:
        return (f"{SIBLING}/{MBB} gained augmentative_release, but this crop's prose names no wasp "
                f"in either register; that would be a claim propagated across a family")
    return None


def check_r5_is_used(batch):
    """r5 minted and widened methods for this batch. If none of them lands, the round was not
    justified by the need it claimed."""
    for pid, method in R5_USE.items():
        for slug in CROPS:
            ms, _ = ladder_of(batch[slug], pid)
            if ms is None:
                return f"{slug} has no {pid} problem, so {method} cannot be checked"
            if method not in ms:
                return (f"{slug}/{pid} does not use {method}; that method was minted or widened by "
                        f"the r5 catalog round specifically for this batch's prose")
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
            tiers = []
            seen = set()
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
    for method in set(R5_USE.values()):
        if method not in cm:
            return f"{method} is not in the catalog; the r5 round must land first"
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"
    problem = check_twin_premise(by)
    if problem:
        return problem
    batch = staged()
    for problem in (check_grouping(batch), check_read_fixes(batch, by), check_r5_is_used(batch)):
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

    # SET EQUALITY BEFORE VALUE COMPARISON (PLA-162), then blast radius.
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

    for slug in CROPS:
        for _, p in problems(by[slug]):
            if not p.get("control_ladder"):
                return f"{slug}/{p.get('id')}: no ladder after promote"

    def sig(s):
        """FULL ladder content, notes included -- not the method sequence.

        Batch 4's first cut compared method KEYS and wrongly refused a correct batch: siblings that
        share prose SHOULD converge on the same keys. What must differ between independently
        authored crops is the PROSE. So the twin is compared on content and must MATCH, and the
        sibling is compared on content and must DIFFER.
        """
        return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                            for r in p["control_ladder"]] for _, p in problems(by[s])],
                          sort_keys=True)

    if sig(TWIN[0]) != sig(TWIN[1]):
        return "post: the twin pair does not carry identical ladders"
    if sig(SIBLING) == sig(TWIN[0]):
        return ("post: the sibling carries ladder CONTENT identical to the twin; it was authored "
                "separately and its prose must differ")

    for slug in CROPS:
        ms, _ = ladder_of(by[slug], MBB)
        if slug == SIBLING:
            if "off_season_tillage" in ms:
                return f"post: {slug}/{MBB} regained off_season_tillage"
            if "augmentative_release" in ms:
                return f"post: {slug}/{MBB} gained augmentative_release"
        else:
            if "augmentative_release" not in ms:
                return f"post: {slug}/{MBB} lost augmentative_release"
        for pid, method in R5_USE.items():
            mm, _ = ladder_of(by[slug], pid)
            if method not in mm:
                return f"post: {slug}/{pid} lost its {method} rung"
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

    print("PLA-8 BATCH 5 -- the three beans")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  twin         : {TWIN}  (authored {AUTHORED}, propagated; premise asserted in canonical)")
    print(f"  sibling      : {SIBLING}  (own authoring pass; distinctness asserted)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused")
    print(f"  methods      : 0 touched   sources: 0 touched   crops outside the three: 0")
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
