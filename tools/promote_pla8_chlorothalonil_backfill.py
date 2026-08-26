#!/usr/bin/env python3
"""PLA-8: attach the chlorothalonil rung to the 9 ladders whose prose already names it. Base 93e32e2b.

9 problems across 6 CERTIFIED crops gain ONE rung each, appended last: `cucumber`,
`slicing-cucumber`, `pickling-cucumber` (downy mildew + anthracnose each) and `green-beans-bush`,
`pole-beans`, `dry-bean` (anthracnose). 18 register strings. No control_method, no source, no crop
outside the six, no other problem.

THIS AMENDS CERTIFIED, SHIPPED CROPS, which is heavier than a catalog round and is why it is its own
promote rather than part of the mint. Every one of the nine already names chlorothalonil in its own
`organic_treatment_seasoned`; the ladder simply could not say it until `d096415`.

--------------------------------------------------------------------------------------------------
AUTHORED PER SENTENCE, NOT PER CROP, AND THE PROMOTE ASSERTS THAT PREMISE
--------------------------------------------------------------------------------------------------
A rung restates the sentence it comes from. Measured against `93e32e2b`, the chlorothalonil-bearing
sentence takes exactly THREE forms across the nine, each shared by three crops:

  A  cucurbit downy mildew  "apply a labeled fungicide such as copper or chlorothalonil, covering
                             leaf undersides, when conditions favor the disease"
  B  cucurbit anthracnose   "apply a labeled fungicide such as chlorothalonil preventatively in
                             wet spells"
  C  bean anthracnose       "a copper fungicide or chlorothalonil can suppress it when started
                             early; cultural control is the mainstay for a home crop"

So three rung texts, each applied to its three crops. `check_shared_sentence` verifies in CANONICAL
that every crop in a group really does carry the same sentence, and refuses if one has drifted --
because a crop whose source says something different needs its own rung, not a copy. This is the
batch-5 twin premise applied at the level of a single sentence rather than a whole record.

--------------------------------------------------------------------------------------------------
GROUP B PRODUCES A LADDER SHAPE THE ROSTER HAS NOT SHIPPED BEFORE, AND IT IS DELIBERATE
--------------------------------------------------------------------------------------------------
The three cucurbit anthracnose ladders currently END at `garden_sanitation`, which is CULTURAL,
because their prose names no softer spray at all. Adding this rung makes them run
**cultural -> conventional**, skipping physical, biological and soft_chemical entirely.

That is legal (tiers only have to be non-decreasing) and it is honest: for anthracnose on these
crops the source offers cleanup and then one synthetic, with nothing in between. But it is a jump,
so the rung prose SAYS SO rather than letting the reader infer that three rungs were forgotten, and
a guard pins that the jump is present in exactly those three and nowhere else. The other six already
top out at `copper_fungicide`, so their new rung is an ordinary step past a soft chemical.

--------------------------------------------------------------------------------------------------
WHAT THE PROSE MUST CARRY
--------------------------------------------------------------------------------------------------
Group C's source hedges three times in one sentence -- "can suppress", "when started early", and
"cultural control is the mainstay for a home crop" -- and all three are carried, because a rung that
promised a cure from a material the source says merely suppresses would be the exact defect this arc
keeps finding. Every rung also points the reader at the method's own cautions rather than restating
them, since the sheet minted in `d096415` carries the full profile including the Prop 65 and EPA
carcinogen listing.

REFUSALS: base SHA mismatch; the method absent from the catalog; a target already carrying the rung;
a shared sentence that has drifted within its group; a rung not appended last; a tier decrease; a
target whose ladder is missing; the cultural-to-conventional jump appearing outside group B; a
dropped hedge; copy hygiene; and post-state blast radius on every crop, method and source.

Guard suite:      tools/test_promote_pla8_chlorothalonil_backfill.py
Mutation harness: tools/mutate_pla8_chlorothalonil_backfill_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_chlorothalonil_backfill.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "93e32e2b49d9e064b0d687dd5814260186fb71341f072a27b8eec36fa0d578ed"

METHOD = "chlorothalonil"
CUCURBITS = ("cucumber", "slicing-cucumber", "pickling-cucumber")
BEANS = ("green-beans-bush", "pole-beans", "dry-bean")
CROPS = CUCURBITS + BEANS

# group -> (the crops it covers, the problem id, the source phrase they must share)
GROUPS = {
    "A": (CUCURBITS, "downy-mildew", "copper or chlorothalonil"),
    "B": (CUCURBITS, "anthracnose", "such as chlorothalonil preventatively"),
    "C": (BEANS, "anthracnose", "chlorothalonil can suppress it when started early"),
}

# The three ladders that will run cultural -> conventional with nothing between.
JUMP_GROUP = "B"

RUNGS = {
    "A": {
        "note_beginner":
            "If downy mildew keeps moving after the copper, chlorothalonil is the other fungicide "
            "this crop's guidance names for it. Cover the undersides of the leaves, since that is "
            "the surface it has to protect, and start when the weather turns to what the disease "
            "likes rather than once the leaves are already covered. Read this one's warnings before "
            "you decide: it is the heaviest thing in this guide, and stopping at the copper is a "
            "real choice.",
        "note_seasoned":
            "The second material named for this disease alongside copper, and applied on the same "
            "terms: undersides covered, begun as conditions turn favorable rather than after "
            "lesions are established. Protectant only, so it defends clean tissue and does nothing "
            "for what is already infected. Weigh the method's own cautions, which are the heaviest "
            "carried by anything in this catalog, against stopping one rung lower.",
    },
    "B": {
        "note_beginner":
            "This is the only spray this crop's guidance names for anthracnose, and it is meant "
            "preventively: it goes on ahead of a wet spell rather than after spots show. Notice the "
            "gap below it. There is no gentler spray listed for this disease on this crop, so the "
            "step under this one is the cleanup, and declining to go further is a reasonable place "
            "to stop rather than a rung skipped. Read this method's warnings before you take it, "
            "because it is a long way up from the step below.",
        "note_seasoned":
            "The only material this crop's guidance names for anthracnose, specified preventively "
            "in wet spells, which is when the infection periods fall. The escalation runs straight "
            "from sanitation to a conventional here because the source offers nothing between the "
            "two, so the jump is a property of the evidence rather than a gap in the ladder. "
            "Declining it leaves the cultural program as the whole of the control, which is what "
            "the source describes for a home crop.",
    },
    "C": {
        "note_beginner":
            "Named alongside copper as the other material that can hold anthracnose back, and only "
            "where it is started early. It suppresses rather than cures, and this crop's guidance "
            "is plain that the cultural steps above are what carries a home crop, so this sits at "
            "the far end rather than being the answer. Read its warnings before choosing it.",
        "note_seasoned":
            "Named with copper as a material that can suppress anthracnose where treatment starts "
            "early; the source calls cultural control the mainstay for a home crop, so this rung "
            "closes a program rather than replacing one. Suppression rather than eradication, and "
            "preventive in its timing, so a late application buys little.",
    },
}

# Qualifiers each group's source attaches, which the rung must not compress away.
REQUIRED_HEDGES = {
    "A": ("protectant only",),
    "B": ("preventiv",),
    "C": ("suppress", "started early", "mainstay"),
}

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise", "favour")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def targets():
    """(group, slug, problem id) for all nine, in a stable order."""
    return [(g, s, pid) for g, (slugs, pid, _) in GROUPS.items() for s in slugs]


def problem(by, slug, pid):
    for fam in ("pests", "diseases"):
        for p in by[slug].get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    return None


def check_shared_sentence(by):
    """THE PREMISE. A rung restates a sentence; three crops share a rung only because they share
    the sentence. Verified in CANONICAL, and refused if one has drifted -- a crop whose source says
    something different needs its own rung rather than a copy of somebody else's."""
    for g, (slugs, pid, phrase) in GROUPS.items():
        for slug in slugs:
            p = problem(by, slug, pid)
            if p is None:
                return f"{slug} has no {pid} problem"
            t = (p.get("organic_treatment_seasoned") or "").lower()
            if phrase not in t:
                return (f"group {g}: {slug}/{pid} no longer carries the shared phrase {phrase!r} in "
                        f"organic_treatment_seasoned, so it does not share this rung's source and "
                        f"needs its own")
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    if METHOD not in cm:
        return f"{METHOD} is not in the catalog; the mint must land first"
    if cm[METHOD]["tier"] != "conventional":
        return f"{METHOD} is not at the conventional tier, so appending it may break monotonicity"

    problem_ = check_shared_sentence(by)
    if problem_:
        return problem_

    order = {t: i for i, t in enumerate(TIERS)}
    for g, slug, pid in targets():
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        p = problem(by, slug, pid)
        lad = p.get("control_ladder")
        if not lad:
            return f"{slug}/{pid} has no ladder to append to"
        ms = [r["method"] for r in lad]
        if METHOD in ms:
            return f"{slug}/{pid} already carries {METHOD}"
        if order[cm[ms[-1]]["tier"]] > order["conventional"]:
            return f"{slug}/{pid} already ends above conventional, so appending would decrease tier"
        # Group B is the only place a cultural top rung is expected.
        top = cm[ms[-1]]["tier"]
        if g == JUMP_GROUP and top != "cultural":
            return (f"{slug}/{pid} is in the jump group but tops out at {top!r}; the deliberate "
                    f"cultural-to-conventional shape no longer describes it")
        if g != JUMP_GROUP and top == "cultural":
            return (f"{slug}/{pid} tops out at cultural but is not in the jump group, so it would "
                    f"gain an undocumented three-tier jump")

    for g, rung in RUNGS.items():
        blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
        for h in REQUIRED_HEDGES[g]:
            if h not in blob:
                return f"group {g}: the source qualifier {h!r} is missing from the rung"
        if rung["note_beginner"] == rung["note_seasoned"]:
            return f"group {g}: the two registers are identical"
        for s in (rung["note_beginner"], rung["note_seasoned"]):
            bad = hygiene(s)
            if bad:
                return f"group {g}: prose fails copy hygiene ({bad}): {s[:60]!r}"
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
    by = {c.get("slug"): c for c in data["crops"]}
    n = 0
    for g, slug, pid in targets():
        p = problem(by, slug, pid)
        p["control_ladder"].append({"method": METHOD,
                                    "note_beginner": RUNGS[g]["note_beginner"],
                                    "note_seasoned": RUNGS[g]["note_seasoned"]})
        n += 1
    return n


def verify_post(pre, data):
    by = {c.get("slug"): c for c in data["crops"]}
    cm = data["control_methods"]
    post = snapshot(data)
    order = {t: i for i, t in enumerate(TIERS)}

    # SUBSTANTIVE INVARIANTS FIRST: below the bystander loop they cannot fire, because a change to
    # a target crop IS a change to a crop. Fifth time this arc has needed that ordering.
    for g, slug, pid in targets():
        p = problem(by, slug, pid)
        ms = [r["method"] for r in p["control_ladder"]]
        if ms.count(METHOD) != 1:
            return f"post: {slug}/{pid} carries {ms.count(METHOD)} {METHOD} rungs, expected 1"
        if ms[-1] != METHOD:
            return f"post: {slug}/{pid} does not end with the new rung"
        ranks = [order[cm[m]["tier"]] for m in ms]
        if ranks != sorted(ranks):
            return f"post: {slug}/{pid} tiers decrease after the append"
        r = p["control_ladder"][-1]
        if (r["note_beginner"], r["note_seasoned"]) != (RUNGS[g]["note_beginner"],
                                                        RUNGS[g]["note_seasoned"]):
            return f"post: {slug}/{pid} did not get group {g}'s rung"

    # The jump shape exists in exactly the three it was authored for.
    jumps = []
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict) or not p.get("control_ladder"):
                    continue
                ms = [r["method"] for r in p["control_ladder"]]
                if METHOD not in ms:
                    continue
                below = [cm[m]["tier"] for m in ms[:-1]]
                if below and set(below) == {"cultural"}:
                    jumps.append((c["slug"], p["id"]))
    expected = sorted((s, GROUPS[JUMP_GROUP][1]) for s in GROUPS[JUMP_GROUP][0])
    if sorted(jumps) != expected:
        return (f"post: the cultural-to-conventional jump appears on {sorted(jumps)}, expected "
                f"exactly {expected}")

    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints nothing"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed"
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
    problem_ = check(data)
    if problem_:
        print("ABORT: " + problem_, file=sys.stderr)
        return 1

    pre = snapshot(data)
    n = apply_to(data)
    problem_ = verify_post(pre, data)
    if problem_:
        print("ABORT (post): " + problem_, file=sys.stderr)
        return 1

    print(f"PLA-8 -- attach the {METHOD} rung to the ladders whose prose already names it")
    print(f"  rungs added  : {n} across {len(CROPS)} certified crops, {n * 2} register strings")
    print(f"  groups       : A cucurbit downy mildew, B cucurbit anthracnose, C bean anthracnose")
    print(f"  jump shape   : {len(GROUPS[JUMP_GROUP][0])} ladders now run cultural -> conventional "
          f"(group {JUMP_GROUP}; their prose names no softer spray)")
    print(f"  methods      : 0 touched   sources: 0 touched   crops outside the six: 0")
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
