#!/usr/bin/env python3
"""PLA-8: attach the trap_cropping rung to the 10 ladders whose prose already names it. Base 86c5396a.

10 problems across 9 CERTIFIED crops gain ONE rung each, inserted at the END OF THE CULTURAL RUN:
`arugula`, `bok-choy` (flea beetles), `jalapeno` (flea beetles), and `bok-choy`, `cabbage`,
`cauliflower`, `collards`, `kale`, `kohlrabi`, `turnip` (harlequin bug). 20 register strings. No
control_method, no source, no crop outside the nine, no other problem.

THIS AMENDS CERTIFIED, SHIPPED CROPS, which is heavier than a catalog round and is why it is its own
promote rather than part of the mint. Every one of the ten already names a trap crop in its own
prevention or organic-treatment prose; the ladder simply could not say it until the mint landed.

--------------------------------------------------------------------------------------------------
TWO GROUPS, AND THE SPLIT IS THE PREMISE THE PROMOTE ASSERTS
--------------------------------------------------------------------------------------------------
Measured against the base, the ten split by WHETHER THE CROP'S OWN PROSE STATES THE REMOVAL STEP:

  DESTROY_STATED (7)  the seven harlequin bug entries. Each one carries the action through to its
                      end, "then destroy it before the main crop is set out" (turnip: "can
                      concentrate the bugs for removal"). These rungs may restate the removal as
                      the crop's own advice, and they say "this crop's guidance" to attribute it.

  DIVERT_ONLY (3)     the three flea beetle entries. Every one of them stops at the diversion:
                      "divert beetles from the main crop", "can draw beetles off the crop". NONE
                      names an endpoint. These rungs therefore route the removal timing through the
                      METHOD's cautions and are FORBIDDEN the attribution phrase, because saying
                      "this crop's guidance" about a removal step would author a recommendation the
                      source never makes. That is the batch-10 planting_time_avoidance ruling
                      applied to a different field: a risk description is not a recommendation, and
                      neither is a partial one.

`check_group_premise` verifies BOTH DIRECTIONS in canonical: every DESTROY_STATED target really does
carry a removal verb in its trap sentence, and every DIVERT_ONLY target really does not. A crop whose
prose has drifted is refused rather than given the other group's contract.

--------------------------------------------------------------------------------------------------
THE SPECIES GUARD IS WHAT STOPS A PROPAGATION DEFECT
--------------------------------------------------------------------------------------------------
The ten name DIFFERENT trap plants: mustard on most, "arugula or mustard" on arugula, NASTURTIUM on
jalapeno, "mustard, collards, or rapeseed" on collards, "mustard, kale, or rapeseed" on kale, and
"mustard or another preferred crucifer" on turnip. Copying one rung text across the group would put
mustard on jalapeno, whose prose names nasturtium and which is not even a brassica. So every species
a rung names is checked against THAT CROP'S OWN canonical prose, and a rung naming a plant its crop
does not name is refused.

Measured over the four prevention/treatment fields, exactly ONE pair is byte-identical: cabbage and
cauliflower. They share one rung text; the other eight are distinct. `check_rung_distinctness` pins
that correspondence IN BOTH DIRECTIONS -- identical prose must yield identical rungs, and differing
prose must yield differing rungs -- which catches a copied rung and a needlessly forked one with the
same check. This is batch 3's cucumber lesson turned into a guard: the propagation that looked safe
because the problem NAMES matched would have erased a sourced control in both directions.

--------------------------------------------------------------------------------------------------
PLACEMENT: END OF THE CULTURAL RUN, NOT THE END OF THE LADDER
--------------------------------------------------------------------------------------------------
Trap cropping is cultural, so appending it last would break tier monotonicity on all ten (every one
of them ends at a physical or soft_chemical rung). It is inserted after the existing cultural rungs
and before the first non-cultural one. It goes AFTER garden_sanitation, weed_host_control,
crop_rotation and planting_time_avoidance rather than before them, because those cost nothing but
attention while this one asks the reader to establish and then destroy a separate planting: least
invasive still comes first WITHIN the tier.

--------------------------------------------------------------------------------------------------
THE SIX EXCLUSIONS ARE PINNED IN BOTH DIRECTIONS
--------------------------------------------------------------------------------------------------
Six problems MENTION trap cropping and must never carry the rung. Three classes:

  INVERTED       radish/flea-beetles, nasturtium/Aphids, zinnia/Japanese beetles. In each the CROP
                 IS THE TRAP, used to protect something else. Radish's own cause_seasoned says
                 crucifers "are used as trap crops to pull beetles off other vegetables"; nasturtium
                 and zinnia are the textbook trap crops. A rung reverses the sentence.
  REPURPOSED     radish/cabbage-root-maggot. "A damaged early sowing can act as a trap crop if
                 removed promptly" repurposes a sowing already lost; it does not establish one.
  CONSERVATION   dill/Parsleyworm and parsley/Parsleyworm. "Relocate the larvae to a sacrificial
                 plant", on a host grown partly for the butterflies. The larvae are being kept
                 ALIVE. A method whose meaning ends in "then destroy the trap" is actively wrong
                 here, not merely redundant.

nasturtium/Aphids and zinnia/Japanese beetles were NOT in the handoff's measurement: its scan covered
the eight standard prose fields, and those two carry theirs in note_beginner/note_seasoned, a shape
used by 91 problems on the shell and ornamental crops. The true scan is 22 problems on 20 crops, not
20 on 18. They add no rungs (both are unladdered) but they are the two records a later pass is most
likely to get wrong, so they are pinned like the rest.

`check` refuses if any exclusion fails to RESOLVE to a real problem -- a typo would leave the refusal
protecting nothing while reporting green -- and `verify_post` refuses if any of them carries the rung.

REFUSALS: base SHA mismatch; the method absent from the catalog; the method not at the cultural tier;
a target already carrying the rung; a group premise that has drifted; a rung naming a species its
crop does not; the prose/rung distinctness correspondence broken; an exclusion that does not resolve
or that carries the rung; a rung not landing at the end of the cultural run; a tier decrease; a
non-contiguous cultural run; a missing cautions pointer; an attribution phrase on a DIVERT_ONLY rung;
identical registers; copy hygiene; and post-state blast radius on every crop, method and source.

Guard suite:      tools/test_promote_pla8_trap_cropping_backfill.py
Mutation harness: tools/mutate_pla8_trap_cropping_backfill_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_trap_cropping_backfill.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "86c5396a185e34a8b07271dc02794bbd54c7a6dba3367dde832e425c23e0bb2b"

METHOD = "trap_cropping"

DESTROY_STATED = "DESTROY_STATED"
DIVERT_ONLY = "DIVERT_ONLY"

# (slug, problem id, group), in a stable order.
TARGETS = (
    ("arugula",     "flea-beetles",  DIVERT_ONLY),
    ("bok-choy",    "flea-beetles",  DIVERT_ONLY),
    ("jalapeno",    "flea-beetles",  DIVERT_ONLY),
    ("bok-choy",    "harlequin-bug", DESTROY_STATED),
    ("cabbage",     "harlequin-bug", DESTROY_STATED),
    ("cauliflower", "harlequin-bug", DESTROY_STATED),
    ("collards",    "harlequin-bug", DESTROY_STATED),
    ("kale",        "harlequin-bug", DESTROY_STATED),
    ("kohlrabi",    "harlequin-bug", DESTROY_STATED),
    ("turnip",      "harlequin-bug", DESTROY_STATED),
)

CROPS = ("arugula", "bok-choy", "jalapeno", "cabbage", "cauliflower", "collards", "kale",
         "kohlrabi", "turnip")

# The four fields a trap sentence can live in on these ten.
PROSE_FIELDS = ("prevention_beginner", "prevention_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned")

# Words that mark the removal step in a crop's OWN prose. DESTROY_STATED targets must have one in
# their trap sentence; DIVERT_ONLY targets must not.
REMOVAL_WORDS = ("destroy", "removal", "remove")

# The trap plants the roster's prose actually names. A rung may name only species its own crop names.
SPECIES = ("mustard", "arugula", "nasturtium", "rapeseed", "collard", "kale", "crucifer")

# Reserved for the group whose source states the removal. A DIVERT_ONLY rung carrying this phrase
# would attribute to the crop a step its prose stops short of.
ATTRIBUTION = "this crop's guidance"

# Every rung must send the reader to the method sheet for the removal deadline, which is where the
# UMass "before eggs hatch" and UF/IFAS eradicate-before-they-move sentences live.
CAUTIONS_POINTER = "cautions"

# THE SIX. Restated as a literal here rather than imported from the mint: a cross-import couples two
# frozen records and kills the mutation harness.
#
# EACH CARRIES ITS OWN REASON, because they are wrong in three different ways and a shared message
# would under-explain the worst of them. nasturtium is the most dangerous: its own text says "on a
# trap stand, monitor and pull or destroy the planting once it is heavily loaded", which READS like
# this method's action, so a later pass could add the rung and feel confirmed by the sentence. But
# this dataset carries nasturtium as an ornamental and edible crop, not as a trap stand, and the
# same record goes on to say aphids get treated normally on such a planting. A rung there tells the
# reader to destroy the crop they are growing.
EXCLUSIONS = (
    ("radish", "flea-beetles",
     "INVERTED: radish IS the trap crop here, used to pull beetles off other vegetables. Its own "
     "cause_seasoned explains that as why radish gets hit hard. A rung reverses the sentence."),
    ("radish", "cabbage-root-maggot",
     "A DIFFERENT ACTION: 'a damaged early sowing can act as a trap crop if removed promptly' "
     "repurposes a sowing already lost, rather than establishing a sacrificial one."),
    ("dill", "Parsleyworm (black swallowtail caterpillar)",
     "OPPOSITE INTENT: the larvae are relocated to a spare dill to KEEP THEM ALIVE, on a host "
     "grown partly for the butterflies. A method meaning 'then destroy the trap' is actively "
     "wrong here, not merely redundant."),
    ("parsley", "Parsleyworm (black swallowtail caterpillar)",
     "OPPOSITE INTENT, as dill: larvae relocated to a sacrificial plant, and many gardeners grow "
     "extra parsley deliberately as a swallowtail host."),
    ("nasturtium", "Aphids",
     "INVERTED, AND THE MOST DANGEROUS OF THE SIX: nasturtium IS the trap crop, and its text "
     "already describes pulling a loaded trap stand, which reads exactly like this method. This "
     "dataset carries nasturtium as an ornamental and edible crop, so a rung tells the reader to "
     "destroy the crop they are growing."),
    ("zinnia", "Japanese beetles",
     "INVERTED: zinnia is named as a preferred host whose trap-crop value protects other plants. "
     "A rung reverses it, on a crop grown for its flowers."),
)

# Per-target rung prose. cabbage and cauliflower share one text because their prose is byte-identical
# over PROSE_FIELDS; every other pair differs, and check_rung_distinctness pins that both ways.
_CABBAGE_CAULI = {
    "note_beginner":
        "Put an early mustard patch in ahead of the main planting so the overwintered bugs settle "
        "there first, then destroy that patch before the crop goes out. Removing it is the step "
        "that counts, because bugs left sitting on it will move across to the crop.",
    "note_seasoned":
        "An early mustard stand draws overwintered adults away from the transplants, and this "
        "crop's guidance takes the action through to the removal, destroying the stand before the "
        "main crop is set out. Leave it standing and the patch holds a breeding population beside "
        "the bed; this method's cautions carry the deadline.",
}

RUNGS = {
    ("arugula", "flea-beetles"): {
        "note_beginner":
            "Sow a small sacrificial patch of arugula or mustard off to one side, ahead of the main "
            "sowing, so the first beetles find it instead of your salad row. Read this method's "
            "cautions for when to pull the patch out, because taking it out on time is what keeps "
            "it working.",
        "note_seasoned":
            "An early sacrificial sowing of arugula or mustard diverts the spring flush off the "
            "main stand, which is worth most while the seedlings are small enough that feeding "
            "sets them back. The removal timing sits in this method's cautions; a patch left "
            "standing once loaded turns the diversion into local population growth.",
    },
    ("bok-choy", "flea-beetles"): {
        "note_beginner":
            "Sow a small sacrificial mustard patch to one side before the main sowing, so the "
            "beetles settle there rather than on your seedlings. Check this method's cautions for "
            "when to take it out, since the patch helps only while it is being managed.",
        "note_seasoned":
            "An early mustard sowing diverts beetles from the main stand through the seedling "
            "stage, which is when the feeding costs most. Take the removal timing from this "
            "method's cautions, because a loaded patch left in place supports the next generation "
            "instead of drawing it away.",
    },
    ("jalapeno", "flea-beetles"): {
        "note_beginner":
            "Plant a little nasturtium at the edge of the bed to draw beetles off the peppers. "
            "Treat it as a sacrificial patch rather than part of the crop, and see this method's "
            "cautions for when to pull it out.",
        "note_seasoned":
            "A nasturtium planting at the bed margin draws flea beetles off the crop by preference "
            "rather than by treating them, which is why it sits among the cultural steps. Its "
            "value depends on the removal step in this method's cautions; left in place once "
            "loaded, the planting raises beetle numbers at the bed edge.",
    },
    ("bok-choy", "harlequin-bug"): {
        "note_beginner":
            "Sow a small mustard patch early, before the bok choy goes out, so the overwintered "
            "bugs gather on it instead. Then destroy that patch, bugs and all, before you set out "
            "the main crop. Pulling it on time is the whole point, since a loaded patch left "
            "standing feeds the next round.",
        "note_seasoned":
            "An early mustard stand aggregates emerging overwintered adults ahead of "
            "transplanting, and this crop's guidance carries the step through to its end, "
            "destroying the stand before the main crop is set out. The removal is what turns a "
            "concentration into a control, and this method's cautions give the timing.",
    },
    ("cabbage", "harlequin-bug"): _CABBAGE_CAULI,
    ("cauliflower", "harlequin-bug"): _CABBAGE_CAULI,
    ("collards", "harlequin-bug"): {
        "note_beginner":
            "Sow an early patch of mustard, or put in a collard planting ahead of the main one, to "
            "pull the overwintered bugs onto it. Then destroy that patch before the main crop goes "
            "out. Taking it out on time is what makes it work rather than backfire.",
        "note_seasoned":
            "An early stand of mustard, collards, or rapeseed aggregates overwintered adults "
            "before the main planting, and this crop's guidance runs it through to destroying the "
            "stand before the crop is set out. Using collards themselves as the trap works because "
            "the preference runs to the family, so that early planting has to be removed rather "
            "than harvested; the timing is in this method's cautions.",
    },
    ("kale", "harlequin-bug"): {
        "note_beginner":
            "Sow an early patch of mustard, or an early kale planting, so the overwintered bugs "
            "collect there rather than on the main row. Then destroy that patch before the main "
            "crop goes out. The patch only helps if it comes out on time.",
        "note_seasoned":
            "An early stand of mustard, kale, or rapeseed concentrates overwintered adults ahead "
            "of the main planting, and this crop's guidance carries it to destroying the stand "
            "before the crop is set out. An early kale planting used this way is a sacrifice "
            "rather than a first harvest, and this method's cautions give the removal deadline.",
    },
    ("kohlrabi", "harlequin-bug"): {
        "note_beginner":
            "Sow a mustard patch early to lure the overwintered bugs away from the crop, then "
            "destroy it before the main planting goes out. Getting the patch out while the bugs "
            "are still on it is the step that matters.",
        "note_seasoned":
            "An early mustard stand pulls overwintered adults off the planting, and this crop's "
            "guidance ends the sequence by destroying the stand before the main crop is set out. "
            "That removal is not tidying up; it is what stops the concentration becoming a local "
            "increase. This method's cautions carry the timing.",
    },
    ("turnip", "harlequin-bug"): {
        "note_beginner":
            "Where this bug comes back year after year, sow a patch of mustard or another "
            "cabbage-family plant it prefers, and let the bugs gather on it so you can take them "
            "out together. This crop's guidance treats the patch as a way to concentrate them for "
            "removal, so plan on pulling it rather than keeping it, and see this method's cautions "
            "for when.",
        "note_seasoned":
            "A mustard stand, or another preferred crucifer, concentrates the bugs where they can "
            "be taken out in one pass, which is how this crop's guidance frames it: a tactic for a "
            "recurring problem rather than a routine step. Removal is the payoff, and this "
            "method's cautions set when it has to happen.",
    },
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


def targets():
    return list(TARGETS)


def problem(by, slug, pid):
    for fam in ("pests", "diseases"):
        for p in by[slug].get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    return None


def find_problem(data, slug, ident):
    """A problem matched by `id` OR by `name`; the unladdered exclusions have no `id`."""
    for c in data.get("crops") or []:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):
                    return p
    return None


def prose_blob(p):
    return " ".join((p.get(f) or "") for f in PROSE_FIELDS)


def prose_key(p):
    """The exact bytes of the four fields, for the identical-prose correspondence."""
    return json.dumps({f: p.get(f) for f in PROSE_FIELDS}, sort_keys=True, ensure_ascii=False)


def trap_sentences(p):
    """The sentences in this problem's prose that actually talk about a trap crop."""
    out = []
    for f in PROSE_FIELDS:
        for part in re.split(r"(?<=[.;])\s+", p.get(f) or ""):
            if re.search(r"trap|sacrificial", part, re.I):
                out.append(part.strip())
    return out


def check_group_premise(by):
    """THE PREMISE, VERIFIED IN CANONICAL, IN BOTH DIRECTIONS.

    A DESTROY_STATED rung restates a removal step, so its crop's trap sentence must contain one. A
    DIVERT_ONLY rung must NOT attribute a removal to the crop, so its crop's trap sentence must NOT
    contain one. A crop whose prose has drifted across that line gets refused rather than handed the
    other group's contract."""
    for slug, pid, group in TARGETS:
        p = problem(by, slug, pid)
        if p is None:
            return f"{slug} has no {pid} problem"
        sents = trap_sentences(p)
        if not sents:
            return (f"{slug}/{pid} no longer names a trap crop in its prose, so the rung has "
                    f"nothing to restate")
        blob = " ".join(sents).lower()
        states_removal = any(w in blob for w in REMOVAL_WORDS)
        if group == DESTROY_STATED and not states_removal:
            return (f"{slug}/{pid} is in {DESTROY_STATED} but its trap sentence no longer states a "
                    f"removal step, so the rung would author a recommendation the source does not "
                    f"make")
        if group == DIVERT_ONLY and states_removal:
            return (f"{slug}/{pid} is in {DIVERT_ONLY} but its trap sentence now states a removal "
                    f"step, so it should carry the {DESTROY_STATED} contract instead of routing "
                    f"the timing through the method")
    return None


def check_species(by):
    """Every trap plant a rung names must be named by THAT crop's own prose."""
    for slug, pid, _g in TARGETS:
        p = problem(by, slug, pid)
        said = prose_blob(p).lower()
        rung = RUNGS[(slug, pid)]
        blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
        named = [s for s in SPECIES if s in blob]
        if not named:
            return f"{slug}/{pid}: the rung names no trap plant at all"
        for s in named:
            if s not in said:
                return (f"{slug}/{pid}: the rung names {s!r}, which this crop's own prose does not; "
                        f"a rung restates its own source rather than a sibling's")
    return None


def check_rung_distinctness(by):
    """Identical prose must yield identical rungs, and differing prose differing rungs.

    Both directions matter. One catches a rung copied onto a crop whose source says something else
    (batch 3's cucumbers, where propagation would have erased a sourced control); the other catches
    a needlessly forked text that implies a distinction the sources do not carry."""
    for i, (s1, p1, _a) in enumerate(TARGETS):
        for s2, p2, _b in TARGETS[i + 1:]:
            same_prose = prose_key(problem(by, s1, p1)) == prose_key(problem(by, s2, p2))
            same_rung = RUNGS[(s1, p1)] == RUNGS[(s2, p2)]
            if same_prose and not same_rung:
                return (f"{s1}/{p1} and {s2}/{p2} carry byte-identical prose but different rungs")
            if same_rung and not same_prose:
                return (f"{s1}/{p1} and {s2}/{p2} share a rung but their prose differs, so one of "
                        f"them is being given the other's source")
    return None


def cultural_end(lad, cm):
    """The index just past the leading cultural run, and a complaint if it is not contiguous."""
    i = 0
    while i < len(lad) and cm[lad[i]["method"]]["tier"] == "cultural":
        i += 1
    for r in lad[i:]:
        if cm[r["method"]]["tier"] == "cultural":
            return None, "a cultural rung sits after a non-cultural one"
    return i, None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    if METHOD not in cm:
        return f"{METHOD} is not in the catalog; the mint must land first"
    if cm[METHOD]["tier"] != "cultural":
        return (f"{METHOD} is not at the cultural tier, so inserting it in the cultural run would "
                f"break monotonicity")

    for fn in (check_group_premise, check_species, check_rung_distinctness):
        problem_ = fn(by)
        if problem_:
            return problem_

    if set(RUNGS) != {(s, p) for s, p, _g in TARGETS}:
        return "the rung table and the target list disagree"

    for slug, pid, _g in TARGETS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        p = problem(by, slug, pid)
        lad = p.get("control_ladder")
        if not lad:
            return f"{slug}/{pid} has no ladder to insert into"
        ms = [r["method"] for r in lad]
        if METHOD in ms:
            return f"{slug}/{pid} already carries {METHOD}"
        _i, bad = cultural_end(lad, cm)
        if bad:
            return f"{slug}/{pid}: {bad}"

    for (slug, pid), rung in RUNGS.items():
        group = next(g for s, p, g in TARGETS if (s, p) == (slug, pid))
        blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
        if CAUTIONS_POINTER not in blob:
            return (f"{slug}/{pid}: the rung never points the reader at the method's cautions, "
                    f"which is where the removal deadline lives")
        if group == DIVERT_ONLY and ATTRIBUTION in blob:
            return (f"{slug}/{pid}: a {DIVERT_ONLY} rung uses the attribution phrase "
                    f"{ATTRIBUTION!r}, which would credit the crop with a removal step its prose "
                    f"stops short of")
        if group == DESTROY_STATED and ATTRIBUTION not in blob:
            return (f"{slug}/{pid}: a {DESTROY_STATED} rung does not attribute the removal to the "
                    f"crop, so the strongest thing it could say goes unsaid")
        if rung["note_beginner"] == rung["note_seasoned"]:
            return f"{slug}/{pid}: the two registers are identical"
        for s in (rung["note_beginner"], rung["note_seasoned"]):
            bad = hygiene(s)
            if bad:
                return f"{slug}/{pid}: prose fails copy hygiene ({bad}): {s[:60]!r}"

    # EVERY EXCLUSION MUST RESOLVE, or the refusal it encodes protects nothing while reporting green.
    for slug, ident, reason in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return (f"exclusion {slug}/{ident!r} does not resolve to a problem in canonical, so the "
                    f"refusal it encodes would protect nothing")
        if (slug, ident) in {(s, pid) for s, pid, _g in TARGETS}:
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
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    n = 0
    for slug, pid, _g in TARGETS:
        p = problem(by, slug, pid)
        lad = p["control_ladder"]
        i, bad = cultural_end(lad, cm)
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

    # SUBSTANTIVE INVARIANTS FIRST: below the bystander loop they cannot fire, because a change to a
    # target crop IS a change to a crop.
    for slug, pid, _g in TARGETS:
        p = problem(by, slug, pid)
        lad = p["control_ladder"]
        ms = [r["method"] for r in lad]
        if ms.count(METHOD) != 1:
            return f"post: {slug}/{pid} carries {ms.count(METHOD)} {METHOD} rungs, expected 1"
        idx = ms.index(METHOD)
        if idx + 1 < len(ms) and cm[ms[idx + 1]]["tier"] == "cultural":
            return (f"post: {slug}/{pid} put the rung inside the cultural run rather than at its "
                    f"end")
        # THERE IS NO "the rung sits after a non-cultural rung" CHECK HERE, and its absence is
        # deliberate. One was written, and the mutation harness showed it SURVIVED being disabled:
        # this method is cultural (check refuses any other tier), and cultural is the lowest rank,
        # so a rung landing after a non-cultural one ALWAYS breaks the monotonicity check below.
        # The branch could never fire on its own. Deleted rather than kept as a forward assertion,
        # because an unreachable branch reads as coverage while providing none -- which is the whole
        # argument behind the PLA-215 bar. The end-of-run check above is the half that IS reachable.
        ranks = [order[cm[m]["tier"]] for m in ms]
        if ranks != sorted(ranks):
            return f"post: {slug}/{pid} tiers decrease after the insert"
        r = lad[idx]
        want = RUNGS[(slug, pid)]
        if (r["note_beginner"], r["note_seasoned"]) != (want["note_beginner"],
                                                        want["note_seasoned"]):
            return f"post: {slug}/{pid} did not get its own rung"

    # THE SIX COME BEFORE THE LANDED-SET CHECK, DELIBERATELY. The set comparison below would catch
    # an excluded problem gaining the rung too, but it would report a diff of ten pairs and say
    # nothing about WHY that one is forbidden. Checked first, the failure names the exclusion and
    # carries its own reason -- and the branch is reachable on its own rather than masked by a
    # broader check that happens to fire earlier.
    for slug, ident, reason in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return f"post: exclusion {slug}/{ident!r} no longer resolves"
        if any(r.get("method") == METHOD for r in p.get("control_ladder") or []):
            return f"post: {slug}/{ident!r} must never carry a {METHOD} rung. {reason}"

    # The rung landed on exactly the ten, and on nothing else anywhere on the roster.
    landed = []
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                if any(r.get("method") == METHOD for r in p.get("control_ladder") or []):
                    landed.append((c.get("slug"), p.get("id") or p.get("name")))
    expected = sorted((s, pid) for s, pid, _g in TARGETS)
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

    ds = sum(1 for _s, _p, g in TARGETS if g == DESTROY_STATED)
    print(f"PLA-8 -- attach the {METHOD} rung to the ladders whose prose already names it")
    print(f"  rungs added  : {n} across {len(CROPS)} certified crops, {n * 2} register strings")
    print(f"  groups       : {ds} {DESTROY_STATED} (prose states the removal), "
          f"{n - ds} {DIVERT_ONLY} (prose stops at the diversion)")
    print(f"  placement    : end of the cultural run on all {n}")
    print(f"  exclusions   : {len(EXCLUSIONS)} problems mention trap cropping and are REFUSED a rung")
    print(f"  methods      : 0 touched   sources: 0 touched   crops outside the nine: 0")
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
