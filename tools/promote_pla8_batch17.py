#!/usr/bin/env python3
"""PLA-8 BATCH 17 -- STONE FRUIT: the Prunus category, six crops in one genus. Base 213cb110.

49 problems gain `id`, `type` and `control_ladder`; **137 rungs** across `apricot` (30),
`cherry-sour` (24), `cherry-sweet` (30), `nectarine` (15), `peach` (16) and `plum` (22).
Roster laddered 73 -> 79.

**NO CATALOG MUTATION.** control_methods stays at 61. Same note-shaped schema as batches 15/16.

--------------------------------------------------------------------------------------------------
IDS WERE PINNED BEFORE THE FAN-OUT, NOT MINTED SIX TIMES
--------------------------------------------------------------------------------------------------
Six species in ONE genus is the exact setup that produced batch 13's defect, where all five agents
independently minted the SAME WRONG bacterial id (convergence is not correctness). So the whole
`ID_CONVENTION` table was adjudicated against each record's own stated taxon BEFORE any agent ran,
and each agent was told to FLAG a pinned id it disagreed with rather than silently change it.

Three REFUSALS are pinned, each verified against the records rather than assumed:

* **`bacterial-spot` is REFUSED.** The roster id sits on five peppers whose disease is a generic
  *Xanthomonas* leaf spot (and is actually NAMED "Bacterial leaf spot" there, so the id is already
  loose). Stone fruit bacterial spot is ***Xanthomonas arboricola* pv. *pruni***, stated outright in
  peach's own `cause_seasoned`. Ships as `bacterial-spot-pruni`.
* **Generic `aphids` is REFUSED in both directions.** apricot's entry names a two-species complex
  (green peach + mealy plum aphid) and plum's says "Two aphids specific to plum"
  (*Brachycaudus helichrysi*, *Hyalopterus pruni*). Neither is the generic roster aphid that sits on
  50 vegetable crops. They ship as `apricot-aphids` and `plum-aphids`.
* **The two cherry fruit flies do NOT merge.** cherry-sour's entry names a THREE-species complex
  (*R. cingulata*, *R. fausta*, *R. indifferens*); cherry-sweet's names *R. indifferens* ALONE. Same
  ruling shape as batch 16's sweet-pea refusal: the record's own prose governs, not the kinship.
  Likewise cherry-sweet's compound "Borers (peachtree and American plum borer)" ships as
  `cherry-borers` and must NOT collapse into the other four crops' `peachtree-borer`
  (*Synanthedon exitiosa* alone).

Three REUSES are pinned, each taxon-verified against the anchor record:
`plum-curculio` (from apple; both records name *Conotrachelus nenuphar*), and
`spotted-wing-drosophila` + `birds` (from strawberry).

The shared `brown-rot` id spans all six DESPITE a 3-3 split in the records, three naming
*M. fructicola* AND *M. laxa* and three naming *M. fructicola* alone. That is a TEMPLATE artifact,
not a taxon split: the six records fall into two near-identical prose families and the species list
tracks the template rather than the host. Recorded, deliberately NOT treated as a refusal.

--------------------------------------------------------------------------------------------------
TWO CROSS-CROP ADJUDICATIONS, BOTH SETTLED AGAINST APPLE'S SHIPPED LADDERS
--------------------------------------------------------------------------------------------------
The parallel authoring produced two inconsistencies on ids shared with already-certified crops.
Both were settled by READING apple's shipped ladders, not by preference:

1. **`plum-curculio` carries NO `handpick` rung.** apple's certified ladder folds jarring into
   `garden_sanitation` ("spread a sheet under the tree and tap the branches to jar the beetles
   down"). nectarine and plum independently folded it the same way; apricot and peach split it out
   and were collapsed. One join key cannot carry three shapes. `check_curculio_shape` guards it,
   INCLUDING on apple, so a future pass cannot drift the anchor either.
2. **`bacterial-spot-pruni` carries a hedged terminal `copper_fungicide` rung on all four crops.**
   apricot and peach originally refused it, reading a rung as an endorsement. apple's certified
   fire-blight ladder ships copper exactly this way ("a limited, preventive help, not a cure, and it
   cannot save wood that is already infected"), so the convention is author-it-hedged: a ladder is a
   menu ordered by invasiveness, and the hedge is what carries the "not reliable" message.

--------------------------------------------------------------------------------------------------
THE SELF-DENIAL GUARD IS NEW IN THIS BATCH, AND IT CAUGHT A LIVE DEFECT TWICE
--------------------------------------------------------------------------------------------------
When adjudication 2 added a terminal copper rung, BOTH apricot and peach turned out to have a
cultural rung whose note asserted the ABSENCE of the rung being added -- "there is no reliable rung
above this one ... which is why this ladder stops at cultural steps" and, surviving a first fix
pass, "once symptoms are showing there is no good home cure **to follow it with**". Shipping either
would have been a ladder that denies its own terminal rung.

`check_no_self_denial` bans structural-terminality claims from every rung note batch-wide. This is a
DEFECT CLASS with no natural term to scan for, which is exactly why it earns a guard: the prose is
locally true and only becomes false when a later rung is added, so it survives every structural
gate and every read that looks at one rung at a time.

REFUSALS: base SHA mismatch; a target without its note pair; any crop already laddered; an id off
the convention table; any refused id (`bacterial-spot`, generic `aphids`) anywhere on a batch crop;
the two cherry splits collapsing in either direction; a reused id resolving nowhere or a new id
already taken; a `handpick` rung on `plum-curculio` on ANY crop including apple; a
`bacterial-spot-pruni` ladder without its hedged terminal copper rung; a structural self-denial in
any note; a material outside its ladder's MATERIAL_OK set; unknown method; tier decrease;
applies_to incoherence; identical registers; duplicate method in one ladder; empty ladder; counts
off; ANY change to control_methods, source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch17.py
Mutation harness: tools/mutate_pla8_batch17_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch17.py [--apply] [--dry-run] [--canonical PATH]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch17_stone_fruit")
BASE_SHA = "213cb1108cd4960add0a0f9d3a2bd73aee4f1108d6fa743c6ce6075fd5cc6c2f"

CROPS = ("apricot", "cherry-sour", "cherry-sweet", "nectarine", "peach", "plum")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")   # rung notes (the ladder's own prose)
# The dual-register pairs a stone fruit problem carries. The ladder RESTATES these; if one is
# missing the rung has nothing to restate and the batch premise is broken.
PREMISE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                  "organic_treatment_beginner", "organic_treatment_seasoned",
                  "prevention_beginner", "prevention_seasoned")

EXPECTED_PROBLEMS = {"apricot": 9, "cherry-sour": 7, "cherry-sweet": 9,
                     "nectarine": 9, "peach": 8, "plum": 7}
EXPECTED_RUNGS = {"apricot": 30, "cherry-sour": 24, "cherry-sweet": 30,
                  "nectarine": 15, "peach": 16, "plum": 22}
TOTAL_RUNGS = 137

# Written out as a LITERAL, never derived from the staged files: an expectation computed from the
# thing it validates is vacuous by construction.
ID_CONVENTION = {
    "Plum curculio": "plum-curculio",
    "Peachtree borer": "peachtree-borer",
    "Aphids": "apricot-aphids",
    "San Jose scale": "san-jose-scale",
    "Catfacing insects (stink bugs and plant bugs)": "catfacing-insects",
    "Brown rot": "brown-rot",
    "Bacterial canker": "bacterial-canker",
    "Bacterial spot": "bacterial-spot-pruni",
    "Shot hole (Coryneum blight)": "shot-hole",
    "Cherry fruit fly": "cherry-fruit-fly",
    "Spotted wing drosophila": "spotted-wing-drosophila",
    "Black cherry aphid": "black-cherry-aphid",
    "Birds": "birds",
    "Cherry leaf spot": "cherry-leaf-spot",
    "Western cherry fruit fly": "western-cherry-fruit-fly",
    "Borers (peachtree and American plum borer)": "cherry-borers",
    "X-disease (cherry buckskin)": "x-disease",
    "Lesser peachtree borer": "lesser-peachtree-borer",
    "Oriental fruit moth": "oriental-fruit-moth",
    "Western flower thrips": "western-flower-thrips",
    "Peach leaf curl": "peach-leaf-curl",
    "Aphids (leaf curl plum aphid and mealy plum aphid)": "plum-aphids",
    "Black knot": "black-knot",
}

# Ids that must already exist on a NON-batch crop (taxon-verified reuse), with their anchor.
REUSED_IDS = {
    "plum-curculio": "apple",
    "spotted-wing-drosophila": "strawberry",
    "birds": "strawberry",
}
# Ids this batch MINTS. None may already exist anywhere on the roster.
NEW_IDS = (
    "peachtree-borer", "apricot-aphids", "san-jose-scale", "catfacing-insects", "brown-rot",
    "bacterial-canker", "bacterial-spot-pruni", "shot-hole", "cherry-fruit-fly",
    "black-cherry-aphid", "cherry-leaf-spot", "western-cherry-fruit-fly", "cherry-borers",
    "x-disease", "lesser-peachtree-borer", "oriental-fruit-moth", "western-flower-thrips",
    "peach-leaf-curl", "plum-aphids", "black-knot",
)
# Ids a batch-17 crop must NEVER carry, with the reason each refusal exists.
REFUSED_IDS = {
    "bacterial-spot": "peppers' generic Xanthomonas leaf spot; stone fruit is X. arboricola pv. pruni",
    "aphids": "generic roster aphid on 50 vegetable crops; both stone fruit entries name species",
    "anthracnose": "not a stone fruit problem in this batch; guards against a drifted mint",
}
# The two intra-batch splits, as (crop, required_id, forbidden_id).
SPLIT_RULES = (
    ("cherry-sour", "cherry-fruit-fly", "western-cherry-fruit-fly"),
    ("cherry-sweet", "western-cherry-fruit-fly", "cherry-fruit-fly"),
    ("cherry-sweet", "cherry-borers", "peachtree-borer"),
    ("apricot", "peachtree-borer", "cherry-borers"),
    ("nectarine", "peachtree-borer", "cherry-borers"),
    ("peach", "peachtree-borer", "cherry-borers"),
    ("plum", "peachtree-borer", "cherry-borers"),
)

FORBIDDEN_METHODS = {
    # Refused deliberately roster-wide (playbook section 7); re-asserted here so a stone fruit
    # ladder cannot quietly reintroduce one.
    "trap_cropping", "floating_row_cover",
}

MATERIAL_OK = {
    ("apricot", "plum-curculio"): ("kaolin_clay",),
    ("apricot", "apricot-aphids"): ("horticultural_oil", "insecticidal_soap"),
    ("apricot", "san-jose-scale"): ("horticultural_oil",),
    ("apricot", "bacterial-canker"): ("copper_fungicide",),
    ("apricot", "bacterial-spot-pruni"): ("copper_fungicide",),
    ("apricot", "shot-hole"): ("copper_fungicide",),
    ("cherry-sour", "black-cherry-aphid"): ("horticultural_oil", "insecticidal_soap"),
    ("cherry-sour", "bacterial-canker"): ("copper_fungicide",),
    ("cherry-sweet", "black-cherry-aphid"): ("horticultural_oil", "insecticidal_soap"),
    ("cherry-sweet", "bacterial-canker"): ("copper_fungicide",),
    ("nectarine", "plum-curculio"): ("kaolin_clay",),
    ("nectarine", "peach-leaf-curl"): ("copper_fungicide",),
    ("nectarine", "bacterial-spot-pruni"): ("copper_fungicide",),
    ("peach", "plum-curculio"): ("kaolin_clay",),
    ("peach", "peach-leaf-curl"): ("copper_fungicide",),
    ("peach", "bacterial-spot-pruni"): ("copper_fungicide",),
    ("plum", "plum-curculio"): ("kaolin_clay",),
    ("plum", "plum-aphids"): ("horticultural_oil", "insecticidal_soap"),
    ("plum", "san-jose-scale"): ("horticultural_oil",),
    ("plum", "bacterial-spot-pruni"): ("copper_fungicide",),
}

# Structural-terminality claims. A rung note may say a MATERIAL does not cure the disease; it may
# NOT say the LADDER ends. See the module docstring: both defects this catches were locally true
# when written and became false the moment a terminal rung was added.
# NARROWED after the first run fired on 15 hits. The target is not the WORD "rung" -- 97 notes on
# 39 already-shipped crops use it, so that is a roster-wide copy sweep, not this batch's business
# (filed; same class as playbook section 7's spaced-degF item). The target is a claim about WHICH
# RUNGS EXIST, because that is the subclass that becomes FALSE when a rung is added later. A note
# should describe the WORLD ("no spray reaches larvae inside the bark") and never the LADDER
# ("which is why this ladder carries no soft chemical rung").
SELF_DENIAL_PATTERNS = (
    r"no (?:\w+ ){0,3}rung",
    r"this ladder (?:deliberately )?(?:carries|has|stops|ends|is)",
    r"(?:top|end|bottom|honest end) of this ladder",
    r"the (?:weight|leverage|balance) of (?:the|this) ladder",
    r"(?:weight|leverage) sits (?:this early|here) in the ladder",
    r"nothing (?:stands )?above (?:this|it)",
    r"no (?:step|rung)s? (?:stands? |sits? )?above",
    r"to follow it with",
)
# Phrases that are ALLOWED and must not be caught: a claim about a MATERIAL, not about the ladder.
# Kept as a positive control so a widened pattern cannot silently start rejecting honest hedges.
SELF_DENIAL_ALLOWED = (
    "no spray reaches the larvae once they are inside",
    "copper is preventive at best rather than curative",
    "there is no cure once this bacterium is established",
)


def hygiene(s):
    """Consumer-copy hygiene, mirrored from batch 16."""
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    if re.search(r"\d\s+°F", s):
        bad.append("spaced degF")
    for w in ("always", "never", "completely", "harmless", "guaranteed"):
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    return bad


def staged():
    out = {}
    for c in CROPS:
        p = os.path.join(STAGING, "out_%s.json" % c)
        if not os.path.exists(p):
            raise SystemExit("REFUSED: missing staged file %s" % p)
        out[c] = json.load(open(p))
    return out


def problems(obj):
    return [(f, p) for f in ("pests", "diseases") for p in obj.get(f) or [] if isinstance(p, dict)]


def rung_count(batch):
    return sum(len(p.get("control_ladder") or []) for b in batch.values() for _f, p in problems(b))


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def roster_ids(data, exclude=()):
    out = {}
    for c in data["crops"]:
        if c["slug"] in exclude:
            continue
        for _f, p in problems(c):
            if p.get("id"):
                out.setdefault(p["id"], set()).add(c["slug"])
    return out


# ------------------------------------------------------------------ pre-state checks
def check_schema_premise(by):
    """Every target carries the prose the ladder restates, and no target is already laddered.

    NOTE THE SCHEMA DIFFERENCE FROM BATCHES 15/16. Those crops were note-shaped
    (`note_beginner`/`note_seasoned`). Stone fruit carries the OLDER full schema: four dual-register
    pairs and no `note_*` field at all. Asserting the note pair here would have refused the whole
    batch, and asserting nothing would have let a stripped record through.
    """
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: %s not on the roster" % c)
        for _f, p in problems(by[c]):
            if p.get("control_ladder"):
                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))
            if "note_beginner" in p or "note_seasoned" in p:
                raise SystemExit("REFUSED: %s/%s is note-shaped; this batch's premise is the full "
                                 "schema and the guard below would not be checking the prose the "
                                 "ladders actually restate" % (c, p.get("name")))
            for f in PREMISE_FIELDS:
                if not (p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%s missing %s" % (c, p.get("name"), f))


def check_type_transition(batch, by):
    """`type` is UPGRADED coarse -> fine, and that is a real edit, not an addition.

    Every unladdered problem carries the legacy coarse value (`pest` in pests[], `disease` in
    diseases[]); all 579 already-laddered problems roster-wide carry a FINE value that
    `control_ladder_gate` resolves method `applies_to` against. This promote performs that upgrade,
    so it is asserted in BOTH states rather than left to a silent overwrite.
    """
    for c in CROPS:
        for field, coarse in (("pests", "pest"), ("diseases", "disease")):
            src = by[c].get(field) or []
            out = batch[c].get(field) or []
            for p, o in zip(src, out):
                if p.get("type") != coarse:
                    raise SystemExit("REFUSED: %s/%s pre-state type %r != legacy %r"
                                     % (c, p.get("name"), p.get("type"), coarse))
                # Coarse-equality FIRST. The other way round, "disease" trips the fine-type
                # membership check and this branch is unreachable -- a guard that can never fire is
                # not coverage, it is decoration.
                if o.get("type") == coarse:
                    raise SystemExit("REFUSED: %s/%s kept the coarse type %r; the ladder gate "
                                     "cannot resolve applies_to against it"
                                     % (c, p.get("name"), coarse))
                if o.get("type") not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s post type %r not a fine type"
                                     % (c, p.get("name"), o.get("type")))


def check_ids(batch, by, data):
    """Convention table, reuse anchors, and mint-freshness. Refusals checked in both directions."""
    existing = roster_ids(data, exclude=CROPS)
    for c in CROPS:
        src = by[c]
        for field in ("pests", "diseases"):
            names = [p.get("name") for p in src.get(field) or []]
            got = [p.get("id") for p in batch[c].get(field) or []]
            if len(names) != len(got):
                raise SystemExit("REFUSED: %s/%s arity %d != %d" % (c, field, len(got), len(names)))
            for n, i in zip(names, got):
                want = ID_CONVENTION.get(n)
                if want is None:
                    raise SystemExit("REFUSED: %s/%r not in ID_CONVENTION" % (c, n))
                if i != want:
                    raise SystemExit("REFUSED: %s/%r id %r != convention %r" % (c, n, i, want))
                if i in REFUSED_IDS:
                    raise SystemExit("REFUSED: %s/%r took refused id %r (%s)"
                                     % (c, n, i, REFUSED_IDS[i]))
    for i, anchor in REUSED_IDS.items():
        if i not in existing:
            raise SystemExit("REFUSED: reused id %r resolves nowhere off-batch" % i)
        if anchor not in existing[i]:
            raise SystemExit("REFUSED: reused id %r missing its anchor crop %r" % (i, anchor))
    for i in NEW_IDS:
        if i in existing:
            raise SystemExit("REFUSED: new id %r already exists on %s" % (i, sorted(existing[i])))


def check_splits(batch):
    """The two Prunus splits, asserted in BOTH directions so a merge cannot pass either way."""
    have = {c: {p.get("id") for _f, p in problems(batch[c])} for c in CROPS}
    for crop, required, forbidden in SPLIT_RULES:
        if required not in have[crop]:
            raise SystemExit("REFUSED: %s lost required id %r" % (crop, required))
        if forbidden in have[crop]:
            raise SystemExit("REFUSED: %s took %r, which belongs to the other split"
                             % (crop, forbidden))


def check_curculio_shape(batch, data):
    """`plum-curculio` is ONE join key across apple + 4 stone fruit and carries no `handpick`.

    Guards apple TOO, so a future pass cannot drift the anchor and leave the batch consistent with
    nothing. Adjudicated against apple's shipped ladder, which folds jarring into garden_sanitation.
    """
    seen = 0
    for c in data["crops"]:
        for _f, p in problems(c):
            if p.get("id") == "plum-curculio" and p.get("control_ladder"):
                seen += 1
                ms = [r["method"] for r in p["control_ladder"]]
                if "handpick" in ms:
                    raise SystemExit("REFUSED: %s/plum-curculio has a handpick rung; apple's "
                                     "shipped ladder folds jarring into garden_sanitation" % c["slug"])
                if "garden_sanitation" not in ms:
                    raise SystemExit("REFUSED: %s/plum-curculio lost garden_sanitation, which "
                                     "carries the jarring action" % c["slug"])
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p.get("id") != "plum-curculio":
                continue
            ms = [r["method"] for r in p.get("control_ladder") or []]
            if "handpick" in ms:
                raise SystemExit("REFUSED: staged %s/plum-curculio has a handpick rung" % c)
    if seen == 0:
        raise SystemExit("REFUSED: no shipped plum-curculio ladder found; the anchor check "
                         "would be vacuous")


def check_bacterial_spot_copper(batch):
    """Every `bacterial-spot-pruni` ladder ends on a hedged copper rung (apple fire-blight shape)."""
    found = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p.get("id") != "bacterial-spot-pruni":
                continue
            found += 1
            L = p.get("control_ladder") or []
            if not L or L[-1]["method"] != "copper_fungicide":
                raise SystemExit("REFUSED: %s/bacterial-spot-pruni does not end on copper_fungicide"
                                 % c)
            blob = " ".join(L[-1][f].lower() for f in ADVICE_FIELDS)
            if not re.search(r"preventive|prevention", blob):
                raise SystemExit("REFUSED: %s copper rung drops the preventive-not-curative hedge" % c)
            if not re.search(r"injur|harm|damage|hurt", blob):
                raise SystemExit("REFUSED: %s copper rung drops the tree-injury hedge" % c)
    if found != 4:
        raise SystemExit("REFUSED: expected 4 bacterial-spot-pruni ladders, found %d" % found)


# The STRUCTURAL rule, applied per sentence. An enumerated phrase list is a PROXY and proxies are
# incomplete: the list above missed "is the base the rest of this ladder sits on", which an author
# found by applying the rule instead of the regex. So the rule is implemented directly -- internal
# vocabulary plus a structural claim in the same sentence -- and the phrase list is kept only as a
# fast, readable statement of the shapes already seen.
LADDER_VOCAB = re.compile(r"\b(?:rung|ladder|tier)s?\b", re.I)
STRUCTURAL_CLAIM = re.compile(
    r"\b(?:base|top|bottom|end|ends|above|below|beneath|underneath|sits?|stands?|carries|carry|"
    r"stops?|first|last|no|nothing|none)\b", re.I)


def check_no_self_denial(batch):
    """No rung note may make a claim about the LADDER. See the module docstring: caught live twice.

    Scope note, deliberate: this bans a structural CLAIM, not the vocabulary on its own. 97 notes
    across 39 already-shipped crops use "rung"/"ladder" as a bare self-referent, so a pure
    vocabulary ban would refuse the roster rather than this batch. That sweep is FILED separately;
    what ships here is free of claims about which rungs exist or where one sits.
    """
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    t = r[f]
                    for pat in SELF_DENIAL_PATTERNS:
                        m = re.search(pat, t.lower())
                        if m:
                            raise SystemExit(
                                "REFUSED: %s/%s/%s %s asserts the ladder ends (%r). A note may say "
                                "a MATERIAL does not cure; it may not say the LADDER stops."
                                % (c, p["id"], r["method"], f, m.group(0)))
                    for sent in re.split(r"(?<=[.;])\s+", t):
                        if LADDER_VOCAB.search(sent) and STRUCTURAL_CLAIM.search(sent):
                            raise SystemExit(
                                "REFUSED: %s/%s/%s %s makes a structural claim about the ladder "
                                "(%r). Describe the WORLD, not the data: a note may say what works "
                                "on the pest, never where a rung sits or which rungs exist."
                                % (c, p["id"], r["method"], f, sent.strip()[:120]))


def check_self_denial_positive_control():
    """The allowed phrases must NOT match. Without this, widening a pattern until it catches
    everything would look like a stronger guard while actually rejecting honest material hedges."""
    for s in SELF_DENIAL_ALLOWED:
        for pat in SELF_DENIAL_PATTERNS:
            if re.search(pat, s.lower()):
                raise SystemExit("REFUSED: self-denial pattern %r rejects the ALLOWED material "
                                 "hedge %r; the guard has over-widened" % (pat, s))
        # The structural rule must not fire on these either. Every allowed hedge contains a
        # structural WORD ("no", "reaches", "best"); it is the absence of ladder VOCABULARY that
        # keeps it legal, and this asserts that both halves are genuinely required.
        if LADDER_VOCAB.search(s) and STRUCTURAL_CLAIM.search(s):
            raise SystemExit("REFUSED: the structural rule rejects the ALLOWED material hedge %r; "
                             "the guard has over-widened" % s)
    # Both halves must be REQUIRED, or the rule is really a one-word ban wearing a conjunction.
    if not STRUCTURAL_CLAIM.search("there is no cure once this bacterium is established"):
        raise SystemExit("REFUSED: STRUCTURAL_CLAIM no longer matches a plain hedge, so the "
                         "conjunction is carrying no weight and the rule is a vocabulary ban")
    if LADDER_VOCAB.search("there is no cure once this bacterium is established"):
        raise SystemExit("REFUSED: LADDER_VOCAB matches a note with no ladder vocabulary")


def validate_batch(batch, cm):
    """Structural validity of every rung, independent of the gates."""
    for c in CROPS:
        probs = problems(batch[c])
        if len(probs) != EXPECTED_PROBLEMS[c]:
            raise SystemExit("REFUSED: %s has %d problems, expected %d"
                             % (c, len(probs), EXPECTED_PROBLEMS[c]))
        n = 0
        for _f, p in probs:
            L = p.get("control_ladder") or []
            if not L:
                raise SystemExit("REFUSED: %s/%s empty ladder" % (c, p.get("id")))
            n += len(L)
            if not p.get("type"):
                raise SystemExit("REFUSED: %s/%s missing type" % (c, p.get("id")))
            seen_methods, last = set(), -1
            for r in L:
                m = r.get("method")
                if m not in cm:
                    raise SystemExit("REFUSED: %s/%s unknown method %r" % (c, p["id"], m))
                if m in FORBIDDEN_METHODS:
                    raise SystemExit("REFUSED: %s/%s forbidden method %r" % (c, p["id"], m))
                if m in seen_methods:
                    raise SystemExit("REFUSED: %s/%s duplicate method %r" % (c, p["id"], m))
                seen_methods.add(m)
                t = TIERS.index(cm[m]["tier"])
                if t < last:
                    raise SystemExit("REFUSED: %s/%s tier decrease at %r" % (c, p["id"], m))
                last = t
                applies = cm[m].get("applies_to") or []
                if "any" not in applies and not _type_ok(p["type"], applies):
                    raise SystemExit("REFUSED: %s/%s method %r illegal for type %r"
                                     % (c, p["id"], m, p["type"]))
                if r.get("note_beginner", "").strip() == r.get("note_seasoned", "").strip():
                    raise SystemExit("REFUSED: %s/%s/%s identical registers" % (c, p["id"], m))
                for f in ADVICE_FIELDS:
                    if not (r.get(f) or "").strip():
                        raise SystemExit("REFUSED: %s/%s/%s missing %s" % (c, p["id"], m, f))
                    bad = hygiene(r[f])
                    if bad:
                        raise SystemExit("REFUSED: %s/%s/%s %s: %s" % (c, p["id"], m, f, bad))
                if cm[m]["tier"] in MATERIAL_TIERS:
                    ok = MATERIAL_OK.get((c, p["id"]), ())
                    if m not in ok:
                        raise SystemExit("REFUSED: %s/%s material rung %r outside MATERIAL_OK %r"
                                         % (c, p["id"], m, ok))
        if n != EXPECTED_RUNGS[c]:
            raise SystemExit("REFUSED: %s has %d rungs, expected %d" % (c, n, EXPECTED_RUNGS[c]))
    tot = rung_count(batch)
    if tot != TOTAL_RUNGS:
        raise SystemExit("REFUSED: %d rungs total, expected %d" % (tot, TOTAL_RUNGS))


# IMPORTED, never retyped. This file originally carried a hand-copy of the gate's table with
# `mite: {"mite"}` where the gate has `mite: {"mite", "insect_general"}`. It never fired here (no
# stone fruit problem is mite-typed) but batch 18 inherited the copy as a template and it WOULD
# have refused `beneficial_predators` on citrus mites, which control_ladder_gate passes and which
# is correct content: predatory mites are the natural enemy. Corrected 2026-08-31.
from control_ladder_gate import TYPE_TARGETS as _TYPE_TARGETS  # noqa: E402


def _type_ok(t, applies):
    return bool(_TYPE_TARGETS.get(t, set()) & set(applies))


def check(data):
    by = by_slug(data)
    batch = staged()
    check_schema_premise(by)
    check_type_transition(batch, by)
    check_ids(batch, by, data)
    check_splits(batch)
    check_curculio_shape(batch, data)
    check_bacterial_spot_copper(batch)
    check_self_denial_positive_control()
    check_no_self_denial(batch)
    validate_batch(batch, data["control_methods"])
    return batch


# ------------------------------------------------------------------ apply
def serialize(data):
    """THE serializer. Used by the promote AND by the guard suite, so a suite doing its own
    json.dumps cannot grade itself and let an indent mutation survive."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    """Leaf-level map of everything this promote must not touch, plus what it must."""
    out = {}
    for c in data["crops"]:
        for f, p in problems(c):
            key = (c["slug"], f, p.get("name"))
            out[key] = (p.get("id"), p.get("type"),
                        len(p.get("control_ladder") or []))
    return out


def apply_to(data):
    batch = check(data)
    by = by_slug(data)
    for c in CROPS:
        src, out = by[c], batch[c]
        for field in ("pests", "diseases"):
            for p, o in zip(src.get(field) or [], out.get(field) or []):
                p["id"] = o["id"]
                p["type"] = o["type"]
                p["control_ladder"] = copy.deepcopy(o["control_ladder"])
    return data


def verify_post(pre, data):
    """Blast radius at LEAF level. `set(pre) == set(post)` FIRST: iterating pre alone makes every
    ADDITION invisible, which was all four PLA-162 defects."""
    post = snapshot(data)
    if set(pre) != set(post):
        added = sorted(set(post) - set(pre))
        dropped = sorted(set(pre) - set(post))
        raise SystemExit("REFUSED: problem set changed. added=%r dropped=%r" % (added[:5], dropped[:5]))
    touched = 0
    for k in pre:
        if pre[k] == post[k]:
            continue
        if k[0] not in CROPS:
            raise SystemExit("REFUSED: bystander crop %s changed at %r" % (k[0], k))
        touched += 1
    if touched != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: %d problems changed, expected %d"
                         % (touched, sum(EXPECTED_PROBLEMS.values())))
    return touched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    # Needed whenever a LATER batch chains through this promote before it is committed:
    # promote_fixture._from_chain invokes `<script> --canonical PATH --expect-sha SHA --apply`.
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    pre = snapshot(data)
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    touched = verify_post(pre, data)

    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this batch mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; this batch mints nothing")

    blob = serialize(data)
    new_sha = hashlib.sha256(blob).hexdigest()
    print("problems laddered : %d" % touched)
    print("rungs             : %d" % TOTAL_RUNGS)
    print("base  SHA         : %s" % sha)
    print("post  SHA         : %s" % new_sha)
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
