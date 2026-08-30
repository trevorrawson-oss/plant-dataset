#!/usr/bin/env python3
"""PLA-8: attach the disease_escape_sowing rung to the 7 ladders whose prose states it. Base 9f38bb00.

7 problems across 7 CERTIFIED crops gain ONE rung each: the four corns' `common-rust` and the two
peas' `powdery-mildew` (inserted immediately AFTER `resistant_varieties`), and fava's
`broad-bean-rust` (inserted at the FRONT of the ladder). 14 register strings. No control_method, no
source, no crop outside the seven, no other problem.

THIS AMENDS CERTIFIED, SHIPPED CROPS, which is heavier than a catalog round and is why it is its
own promote rather than part of the mint. Every one of the seven already states the escape in its
own prevention prose ("plant early so the crop matures before rust builds late in the season";
"sow early so the crop finishes pod fill before the late-season mildew weather"); the ladder simply
could not say it until the mint landed. Six of the seven shipped that way in earlier batches; fava
shipped in batch 12 with the advice recorded as unplaced.

--------------------------------------------------------------------------------------------------
ONE GROUP, THREE TEXTS, AND THE CORRESPONDENCE IS PINNED ON THE ESCAPE SENTENCES
--------------------------------------------------------------------------------------------------
Unlike trap cropping there is no stated/unstated split: ALL SEVEN state the practice, so every rung
carries the "this crop's guidance" attribution and every rung points at the method's cautions for
the cold-seedbed trade.

The distinctness contract keys on the ESCAPE SENTENCES rather than on whole-field bytes, because
that is what the rung restates. The four corns are byte-identical over all four prose fields; the
two peas differ in their VARIETY-NAME sentences but carry byte-identical escape sentences; fava's
are its own. So: one corn text on four rungs, one pea text on two, one fava text. Identical escape
sentences must yield identical rungs and differing ones differing rungs, both directions
(`check_rung_distinctness`).

--------------------------------------------------------------------------------------------------
PLACEMENT: BESIDE THE OTHER BEFORE-ANYTHING-IS-IN-THE-GROUND DECISION
--------------------------------------------------------------------------------------------------
A sowing date and a variety choice are both settled before anything is in the ground, and the
sources name them in the same breath, so the rung goes at the front of the ladder. On the six whose
ladders open with `resistant_varieties` it lands immediately AFTER it (the crops' own prose puts
resistance first: "the single most effective step"). Fava's ladder has no resistance rung and its
prevention prose LEADS with the escape, so there it lands at index 0. All seven leading runs are
cultural, so monotonicity is preserved; verify_post asserts the exact position on every target.

--------------------------------------------------------------------------------------------------
FAVA'S RUNG STATES A COUNTER-EXPOSURE, SO ITS PREMISE IS ASSERTED IN CANONICAL
--------------------------------------------------------------------------------------------------
The fava rung says the trade is documented on this same crop: its own root-rots entry warns against
sowing into cold, soggy ground. That is a claim about ANOTHER record, so `check_fava_premise`
verifies it against canonical (the batch-5 rule: assert a propagation premise in canonical, not in
staged files) and the promote refuses if that prose ever drops the warning.

--------------------------------------------------------------------------------------------------
THE FOUR EXCLUSIONS ARE PINNED IN BOTH DIRECTIONS
--------------------------------------------------------------------------------------------------
Four problems matched the measurement scan and must never carry the rung, each wrong its own way:

  OPPOSITE   spinach/damping-off. Early sowing into cold soil is what CAUSES this problem; its own
             prose says to wait until the soil is no longer cold and wet. Typed `fungal`, so
             TYPE_TARGETS would ACCEPT the rung -- the one exclusion the gate cannot catch, and
             the reason the list exists.
  INHERENT   radish/black-rot. "The fast radish crop usually finishes before severe disease
             develops" is the crop's SPEED, not a sowing decision; there is no action to place.
  HARVEST    cilantro-coriander/powdery-mildew. "Pick the leaf crop young before mildew builds"
             escapes by early HARVEST, not by sowing date.
  ROGUING    jalapeno/mosaic-viruses. "Remove infected plants early" is roguing; the scan matched
             the word "early" doing a different job.

REFUSALS: base SHA mismatch; the method absent from the catalog or not cultural; a target already
carrying the rung; an escape-sentence premise that has drifted; the fava counter-exposure premise
gone; the distinctness correspondence broken; a missing attribution or cautions pointer; identical
registers; copy hygiene; an exclusion that does not resolve or that carries the rung; a rung not at
its specified position; a tier decrease; and post-state blast radius on every crop, method and
source.

Guard suite:      tools/test_promote_pla8_disease_escape_backfill.py
Mutation harness: tools/mutate_pla8_disease_escape_backfill_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_disease_escape_backfill.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "9f38bb007d3abd5b1cfc970178b9a4405088b0a9de46ff27eaba5163bef7b575"

METHOD = "disease_escape_sowing"
ANCHOR_RUNG = "resistant_varieties"   # the rung the six land after
FRONT = None                          # fava lands at index 0

# (slug, problem id, insert-after method or FRONT, the disease word its escape sentence must name)
TARGETS = (
    ("sweet-corn",       "common-rust",    ANCHOR_RUNG, "rust"),
    ("field-corn",       "common-rust",    ANCHOR_RUNG, "rust"),
    ("popcorn",          "common-rust",    ANCHOR_RUNG, "rust"),
    ("flint-corn",       "common-rust",    ANCHOR_RUNG, "rust"),
    ("sugar-snap-peas",  "powdery-mildew", ANCHOR_RUNG, "mildew"),
    ("snow-peas",        "powdery-mildew", ANCHOR_RUNG, "mildew"),
    ("broad-beans-fava", "broad-bean-rust", FRONT,      "rust"),
)

CROPS = ("sweet-corn", "field-corn", "popcorn", "flint-corn", "sugar-snap-peas", "snow-peas",
         "broad-beans-fava")

# The four fields an escape sentence can live in on these seven.
PROSE_FIELDS = ("prevention_beginner", "prevention_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned")

# Every rung attributes the escape to the crop (all seven state it) and points the reader at the
# method's cautions, which is where the cold-seedbed trade lives.
ATTRIBUTION = "this crop's guidance"
CAUTIONS_POINTER = "cautions"

# THE FOUR. Restated as a literal here rather than imported from the mint: a cross-import couples
# two frozen records and kills the mutation harness. Each carries its own reason; spinach is the
# one the gate cannot catch and the advice INVERTS there.
EXCLUSIONS = (
    ("spinach", "damping-off",
     "OPPOSITE DIRECTION: early sowing into cold soil is what CAUSES damping-off, and this "
     "crop's own prose says to wait until the soil is no longer cold and wet. Typed fungal, so "
     "the type gate would accept the rung while it advised the exact harm."),
    ("radish", "black-rot",
     "INHERENT SPEED, NOT A DECISION: 'the fast radish crop usually finishes before severe "
     "disease develops' describes what radishes are, not a sowing date the reader chooses. "
     "There is no action for a rung to carry."),
    ("cilantro-coriander", "powdery-mildew",
     "ESCAPE BY HARVEST, NOT BY SOWING: 'pick the leaf crop young before mildew builds' moves "
     "the harvest earlier, not the sowing. A rung here would relabel a picking habit as a "
     "calendar decision the source does not make."),
    ("jalapeno", "mosaic-viruses",
     "ROGUING, NOT TIMING: 'remove infected plants early' is sanitation of infected plants; the "
     "scan matched the word 'early' doing a different job. Viral besides, so the type gate also "
     "refuses it."),
)

_CORN = {
    "note_beginner":
        "Plant early in your window so the corn is nearly done before rust gets bad late in "
        "summer, which is this crop's guidance alongside the rust-resistant variety this ladder "
        "starts with. The one limit is the soil itself, since corn seed rots in cold, wet "
        "ground; this method's cautions carry the soil temperatures to wait for.",
    "note_seasoned":
        "An early planting takes the crop through silking and grain fill before rust builds "
        "late in the season, which is this crop's guidance and why the rung sits beside the "
        "resistant hybrid at the front of the ladder: both are settled before anything is in "
        "the ground. The floor is the seedbed, because corn seed sown into cold, wet soil rots "
        "rather than emerges, and this method's cautions carry the temperatures that set it.",
}

_PEA = {
    "note_beginner":
        "Sow as early as the ground can be worked so the crop finishes before the mildew "
        "weather arrives, which is this crop's guidance along with the resistant variety this "
        "ladder starts with. Mildew tends to build late, so an early sowing simply finishes "
        "ahead of it; this method's cautions carry the cold-soil trade that comes with the "
        "early date.",
    "note_seasoned":
        "An early sowing lets the crop finish pod fill before the late-season mildew weather, "
        "which is this crop's guidance, and it works because the pressure is seasonal: mildew "
        "builds late, and spring sowings mostly finish ahead of it. It sits beside the "
        "resistant varieties at the front of the ladder, a when beside their what. The early "
        "edge has its own cost in cold, wet soil, and this method's cautions carry it.",
}

_FAVA = {
    "note_beginner":
        "Sow early so the pods are filled before the warm midsummer weather that brings on "
        "rust; rust shows up late, so an early planting usually finishes before it matters, "
        "which is this crop's guidance. The trade sits at the cold end, and this crop's own "
        "root rot entry says not to sow into soggy ground, so go early without going into mud; "
        "this method's cautions carry the trade.",
    "note_seasoned":
        "Sown early, the crop matures before the warm midsummer weather that drives rust, and "
        "because rust arrives late the pods are usually filled before it matters: this crop's "
        "guidance states the escape in as many words. The counterweight is documented on this "
        "same crop, whose root rots entry warns against sowing into cold, wet, soggy ground, so "
        "the sowing moves as early as the seedbed honestly allows and stops there; this "
        "method's cautions carry the trade.",
}

RUNGS = {
    ("sweet-corn", "common-rust"): _CORN,
    ("field-corn", "common-rust"): _CORN,
    ("popcorn", "common-rust"): _CORN,
    ("flint-corn", "common-rust"): _CORN,
    ("sugar-snap-peas", "powdery-mildew"): _PEA,
    ("snow-peas", "powdery-mildew"): _PEA,
    ("broad-beans-fava", "broad-bean-rust"): _FAVA,
}

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise", "favour")


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


def problem(by, slug, pid):
    for fam in ("pests", "diseases"):
        for p in by[slug].get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    return None


def find_problem(data, slug, ident):
    """A problem matched by `id` OR by `name`, so an exclusion stays resolvable either way."""
    for c in data.get("crops") or []:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):
                    return p
    return None


def escape_sentences(p):
    """The sentences in this problem's prose that state the sowing-date escape."""
    out = []
    for f in PROSE_FIELDS:
        for part in re.split(r"(?<=[.;])\s+", p.get(f) or ""):
            if re.search(r"\b(?:sow|plant)\w*\s+early\b|\bearly\s+(?:planting|sowing)\b",
                         part, re.I):
                out.append(part.strip())
    return out


def check_escape_premise(by):
    """THE PREMISE, VERIFIED IN CANONICAL. Every target's own prose must state the escape, and its
    escape sentence must name the disease being escaped. A crop whose prose has drifted is refused
    rather than given a rung that restates nothing."""
    for slug, pid, _after, word in TARGETS:
        p = problem(by, slug, pid)
        if p is None:
            return f"{slug} has no {pid} problem"
        sents = escape_sentences(p)
        if not sents:
            return (f"{slug}/{pid} no longer states an early-sowing escape in its prose, so the "
                    f"rung has nothing to restate")
        if not any(word in s.lower() for s in sents):
            return (f"{slug}/{pid}: the escape sentence no longer names {word!r}, so the rung "
                    f"would attribute a disease claim the prose does not make")
    return None


def check_fava_premise(by):
    """The fava rung claims the trade is documented on the same crop: its root-rots entry warns
    against sowing into cold, soggy ground. Asserted in CANONICAL, never assumed."""
    p = problem(by, "broad-beans-fava", "root-rots-damping-off")
    if p is None:
        return ("broad-beans-fava has no root-rots-damping-off problem, and the fava rung "
                "attributes the cold-seedbed warning to it")
    blob = " ".join((p.get(f) or "") for f in PROSE_FIELDS).lower()
    if "cold" not in blob or "sow" not in blob:
        return ("broad-beans-fava's root-rots entry no longer carries the cold-seedbed sowing "
                "warning the fava rung attributes to it")
    return None


def escape_key(p):
    """The exact escape sentences, for the identical-escape correspondence."""
    return json.dumps(escape_sentences(p), ensure_ascii=False)


def check_rung_distinctness(by):
    """Identical escape sentences must yield identical rungs, and differing ones differing rungs.

    Keyed on the escape sentences rather than whole-field bytes, because the escape sentence is
    what the rung restates: the two peas differ in their variety-name sentences but share the
    escape byte-for-byte, and forking their rung would imply a distinction the sources do not
    carry. The other direction catches a rung copied onto a crop whose escape says something
    else."""
    rows = [(s, pid) for s, pid, _a, _w in TARGETS]
    for i, (s1, p1) in enumerate(rows):
        for s2, p2 in rows[i + 1:]:
            same_escape = escape_key(problem(by, s1, p1)) == escape_key(problem(by, s2, p2))
            same_rung = RUNGS[(s1, p1)] == RUNGS[(s2, p2)]
            if same_escape and not same_rung:
                return (f"{s1}/{p1} and {s2}/{p2} carry byte-identical escape sentences but "
                        f"different rungs")
            if same_rung and not same_escape:
                return (f"{s1}/{p1} and {s2}/{p2} share a rung but their escape sentences "
                        f"differ, so one of them is being given the other's source")
    return None


def insert_index(lad, after):
    """Where the rung goes: index 0 for FRONT, else immediately after the named rung."""
    if after is None:
        return 0, None
    ms = [r["method"] for r in lad]
    if after not in ms:
        return None, f"ladder has no {after!r} rung to land after"
    if ms.index(after) != 0:
        return None, (f"{after!r} is not the ladder's opening rung, so the "
                      f"before-anything-is-in-the-ground placement premise has drifted")
    return ms.index(after) + 1, None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    if METHOD not in cm:
        return f"{METHOD} is not in the catalog; the mint must land first"
    if cm[METHOD]["tier"] != "cultural":
        return (f"{METHOD} is not at the cultural tier, so a front-of-ladder insert would break "
                f"monotonicity")

    for fn in (check_escape_premise, check_fava_premise, check_rung_distinctness):
        problem_ = fn(by)
        if problem_:
            return problem_

    if set(RUNGS) != {(s, p) for s, p, _a, _w in TARGETS}:
        return "the rung table and the target list disagree"

    for slug, pid, after, _w in TARGETS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        p = problem(by, slug, pid)
        lad = p.get("control_ladder")
        if not lad:
            return f"{slug}/{pid} has no ladder to insert into"
        ms = [r["method"] for r in lad]
        if METHOD in ms:
            return f"{slug}/{pid} already carries {METHOD}"
        _i, bad = insert_index(lad, after)
        if bad:
            return f"{slug}/{pid}: {bad}"

    for (slug, pid), rung in RUNGS.items():
        blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
        if ATTRIBUTION not in blob:
            return (f"{slug}/{pid}: the rung does not attribute the escape to the crop, and all "
                    f"seven state it in their own prose, so the strongest thing it could say "
                    f"goes unsaid")
        if CAUTIONS_POINTER not in blob:
            return (f"{slug}/{pid}: the rung never points the reader at the method's cautions, "
                    f"which is where the cold-seedbed trade lives")
        if rung["note_beginner"] == rung["note_seasoned"]:
            return f"{slug}/{pid}: the two registers are identical"
        for s in (rung["note_beginner"], rung["note_seasoned"]):
            bad = hygiene(s)
            if bad:
                return f"{slug}/{pid}: prose fails copy hygiene ({bad}): {s[:60]!r}"

    # EVERY EXCLUSION MUST RESOLVE, or the refusal it encodes protects nothing while reporting
    # green.
    for slug, ident, reason in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return (f"exclusion {slug}/{ident!r} does not resolve to a problem in canonical, so "
                    f"the refusal it encodes would protect nothing")
        if (slug, ident) in {(s, pid) for s, pid, _a, _w in TARGETS}:
            return f"exclusion {slug}/{ident!r} is also a backfill target, which cannot both be true"
        if not reason.strip():
            return f"exclusion {slug}/{ident!r} carries no reason, so a later pass cannot weigh it"
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
    for slug, pid, after, _w in TARGETS:
        p = problem(by, slug, pid)
        lad = p["control_ladder"]
        i, bad = insert_index(lad, after)
        if bad:
            raise AssertionError(f"{slug}/{pid}: {bad}")
        lad.insert(i, {"method": METHOD,
                       "note_beginner": RUNGS[(slug, pid)]["note_beginner"],
                       "note_seasoned": RUNGS[(slug, pid)]["note_seasoned"]})
        n += 1
    return n


def verify_post(pre, data):
    by = {c.get("slug"): c for c in data["crops"]}
    cm = data["control_methods"]
    post = snapshot(data)
    order = {t: i for i, t in enumerate(TIERS)}

    # SUBSTANTIVE INVARIANTS FIRST: below the bystander loop they cannot fire, because a change to
    # a target crop IS a change to a crop.
    for slug, pid, after, _w in TARGETS:
        p = problem(by, slug, pid)
        lad = p["control_ladder"]
        ms = [r["method"] for r in lad]
        if ms.count(METHOD) != 1:
            return f"post: {slug}/{pid} carries {ms.count(METHOD)} {METHOD} rungs, expected 1"
        idx = ms.index(METHOD)
        want = 0 if after is None else ms.index(after) + 1
        if idx != want:
            return (f"post: {slug}/{pid} put the rung at index {idx}, expected {want} "
                    f"({'the front' if after is None else 'immediately after ' + repr(after)})")
        ranks = [order[cm[m]["tier"]] for m in ms]
        if ranks != sorted(ranks):
            return f"post: {slug}/{pid} tiers decrease after the insert"
        r = lad[idx]
        wantr = RUNGS[(slug, pid)]
        if (r["note_beginner"], r["note_seasoned"]) != (wantr["note_beginner"],
                                                        wantr["note_seasoned"]):
            return f"post: {slug}/{pid} did not get its own rung"

    # THE FOUR COME BEFORE THE LANDED-SET CHECK, DELIBERATELY: checked first, a failure names the
    # exclusion and carries its own reason, and the branch is reachable on its own rather than
    # masked by the broader set comparison below.
    for slug, ident, reason in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return f"post: exclusion {slug}/{ident!r} no longer resolves"
        if any(r.get("method") == METHOD for r in p.get("control_ladder") or []):
            return f"post: {slug}/{ident!r} must never carry a {METHOD} rung. {reason}"

    # The rung landed on exactly the seven, and on nothing else anywhere on the roster.
    landed = []
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                if any(r.get("method") == METHOD for r in p.get("control_ladder") or []):
                    landed.append((c.get("slug"), p.get("id") or p.get("name")))
    expected = sorted((s, pid) for s, pid, _a, _w in TARGETS)
    if sorted(landed) != expected:
        return f"post: the rung landed on {sorted(landed)}, expected exactly {expected}"

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
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

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

    print(f"PLA-8 -- attach the {METHOD} rung to the ladders whose prose states the escape")
    print(f"  rungs added  : {n} across {len(CROPS)} certified crops, {n * 2} register strings")
    print(f"  placement    : after {ANCHOR_RUNG!r} on six; the front of fava's ladder")
    print(f"  texts        : 3 distinct (corn x4, pea x2, fava x1), keyed on the escape sentences")
    print(f"  exclusions   : {len(EXCLUSIONS)} scan matches are REFUSED a rung, spinach's "
          f"damping-off above all")
    print(f"  methods      : 0 touched   sources: 0 touched   crops outside the seven: 0")
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
