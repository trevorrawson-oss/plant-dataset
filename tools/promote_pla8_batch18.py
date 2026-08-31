#!/usr/bin/env python3
"""PLA-8 BATCH 18 -- ACID CITRUS: lemon and lime, the first batch on the new `ant_exclusion`.
Base 2cde361b (the ant_exclusion mint).

24 problems gain `id`, a fine `type` and a `control_ladder`; **78 rungs** across `lemon` (36) and
`lime` (42). Roster laddered 79 -> 81. NO catalog mutation: this batch USES the 62nd method rather
than minting anything.

--------------------------------------------------------------------------------------------------
THIS BATCH EXISTS ON THE OTHER SIDE OF A BLOCKER, AND THE BLOCKER'S FIX IS ITS HEADLINE
--------------------------------------------------------------------------------------------------
Batch 18 could not ship on base 2a9d3c85. `sooty-mold` is typed `fungal` while everything its
record prescribes is INSECT control, `TYPE_TARGETS` forbids a fungal type from naming any insect
method, and lemon honestly emitted `control_ladder: null` rather than stretch a key. The
`ant_exclusion` mint closed that, anchored on UC IPM Pest Notes 74108: "Control of sooty mold begins
with managing the insect creating the honeydew."

So `check_sooty_mold_is_laddered` is not a shape check. It asserts the specific defect that
motivated the mint is gone, and it is the one guard whose failure would mean the mint accomplished
nothing.

--------------------------------------------------------------------------------------------------
FOUR ID REFUSALS, EACH VERIFIED AGAINST THE RECORDS
--------------------------------------------------------------------------------------------------
* Generic `aphids` (50 vegetable crops) is REFUSED. Both citrus entries describe a citrus complex
  that vectors citrus tristeza virus; they ship the shared `citrus-aphids`.
* Generic `spider-mites` (15 crops, twospotted-focused) is REFUSED. lemon's record names citrus red
  mite AND twospotted with DIFFERENT monitoring seasons, so the generic id would lose the red mite
  half outright. They ship the shared `citrus-mites`.
* Generic `anthracnose` (14 crops) is REFUSED, and lime proves why on its own record: its
  `lime-anthracnose` is *Colletotrichum gloeosporioides* while its `postbloom-fruit-drop` is
  *C. acutatum*. TWO Colletotrichum species on ONE crop; the generic id would merge them.
* `bacterial-spot` is REFUSED for citrus canker, which is *Xanthomonas citri*, not the peppers'
  Xanthomonas leaf spot. Ships `citrus-canker`.

ONE REUSE: `mealybugs`, from chamomile. Recorded honestly: chamomile's `cause_seasoned` is EMPTY,
so the join rests on both entries being generically named rather than on a taxon match. Both citrus
records name no species either. Flagged, not hidden.

--------------------------------------------------------------------------------------------------
THE SHARED-ID DIVERGENCE RULE, SETTLED THIS BATCH
--------------------------------------------------------------------------------------------------
Batch 17 ruled that `plum-curculio` could not carry three ladder SHAPES for the same asserted
content. This batch settles the other half: a shared id MAY carry different ladders where the
RECORDS differ.

`citrus-aphids` differs by exactly one rung. lemon carries `ant_exclusion`; lime does not. That is
PROSE-GROUNDED, not two agents guessing: both aphid entries only OBSERVE ants, but lemon's own
sooty mold entry says "Managing ants, which protect those insects, is part of the same fix" and
names those insects as "aphids, scale, mealybugs, or whitefly". lime has no sooty mold entry, so
that sentence exists nowhere in its record, and lime's author declined the rung after checking
field by field.

`citrus-canker` was the OTHER shape and was collapsed: lemon used `prune_out_infection`, lime used
`garden_sanitation`, on near-identical sentences differing by one comma. `garden_sanitation` won
because `prune_out_infection` means "taking the cut well beyond the visible margin, back into clean
tissue" and implies a curative excision the entry explicitly denies ("There is no cure for an
infected tree"). The rung would have contradicted the sentence it restates.

`PERMITTED_DIVERGENCE` pins that state: `citrus-aphids` is the ONLY shared id whose ladders may
differ, and only by the `ant_exclusion` rung. Every other shared id must match method-for-method.

--------------------------------------------------------------------------------------------------
NO TEMPERATURE FIGURE APPEARS IN ANY RUNG
--------------------------------------------------------------------------------------------------
The crops' scale entries say oil is unsafe above 95°F; the catalog's own `horticultural_oil` caution
says 90°F. Both render. The mite entries carry NO figure yet their rungs had imported 95°F from the
scale entry, which is the introduced-figure class batches 15/16 already ruled on.

RULED: trim the figure from every oil rung and let the method's caution carry the number, so no rung
contradicts its own method and the stricter figure governs by construction. This does NOT resolve
the conflict, which still renders from the crops' own `organic_treatment_*` prose; that is filed as
a sourcing question. `check_no_temperature_figures` pins the rung half.

REFUSALS: base SHA mismatch; a target already laddered; an id off the convention table; any refused
id anywhere; a reuse resolving nowhere; a new id already taken; `sooty-mold` unladdered or without
its ant_exclusion rung; ant_exclusion sorting at or after `beneficial_predators`; an unpermitted
shared-id divergence; a temperature figure in any rung; ladder vocabulary in any rung; a material
outside MATERIAL_OK; unknown method; tier decrease; applies_to incoherence; identical registers;
duplicate method; empty ladder; counts off; ANY change to control_methods, source_catalog, or a
bystander crop.

Guard suite:      tools/test_promote_pla8_batch18.py
Mutation harness: tools/mutate_pla8_batch18_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch18.py [--apply] [--dry-run] [--canonical PATH]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch18_acid_citrus")
BASE_SHA = "2cde361bb3b8571576f94637e65d86f557a44e7807d97b2a94c02eb7c3715198"

CROPS = ("lemon", "lime")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
PREMISE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                  "organic_treatment_beginner", "organic_treatment_seasoned",
                  "prevention_beginner", "prevention_seasoned")

EXPECTED_PROBLEMS = {"lemon": 12, "lime": 12}
EXPECTED_RUNGS = {"lemon": 36, "lime": 42}
TOTAL_RUNGS = 78

ID_CONVENTION = {
    "Scale insects": "scale-insects",
    "Aphids": "citrus-aphids",
    "Citrus leafminer": "citrus-leafminer",
    "Spider mites and citrus mites": "citrus-mites",
    "Mealybugs": "mealybugs",
    "Asian citrus psyllid (ACP)": "asian-citrus-psyllid",
    "Phytophthora foot rot, root rot, and gummosis": "phytophthora-foot-rot",
    "Greasy spot": "greasy-spot",
    "Sooty mold": "sooty-mold",
    "Citrus canker": "citrus-canker",
    "Huanglongbing (HLB, citrus greening)": "huanglongbing",
    "Iron and zinc deficiency (high-pH chlorosis)": "iron-zinc-deficiency",
    "Brown citrus aphid and other aphids": "citrus-aphids",
    "Citrus red mite and rust mites": "citrus-mites",
    "Lime anthracnose (withertip)": "lime-anthracnose",
    "Postbloom fruit drop": "postbloom-fruit-drop",
}

# The ONLY three problems whose pre-state type is coarse. Every other one is already fine and must
# be preserved byte-for-byte. Pinned so a fourth upgrade cannot ride along unnoticed.
EXPECTED_TYPE_UPGRADES = {
    ("lemon", "Spider mites and citrus mites"): ("pest", "mite"),
    ("lemon", "Iron and zinc deficiency (high-pH chlorosis)"): ("disease", "physiological"),
    ("lime", "Citrus red mite and rust mites"): ("pest", "mite"),
}

REUSED_IDS = {"mealybugs": "chamomile"}
NEW_IDS = ("scale-insects", "citrus-aphids", "citrus-leafminer", "citrus-mites",
           "asian-citrus-psyllid", "phytophthora-foot-rot", "greasy-spot", "sooty-mold",
           "citrus-canker", "huanglongbing", "iron-zinc-deficiency", "lime-anthracnose",
           "postbloom-fruit-drop")
REFUSED_IDS = {
    "aphids": "generic roster aphid on 50 vegetable crops; citrus entries name a CTV-vectoring complex",
    "spider-mites": "twospotted-focused generic on 15 crops; lemon names citrus red mite too",
    "anthracnose": "generic on 14 crops; lime carries C. gloeosporioides AND C. acutatum separately",
    "bacterial-spot": "the peppers' Xanthomonas leaf spot; citrus canker is X. citri",
}

# The ONLY shared id whose ladders may differ, and the ONLY rung by which they may differ.
PERMITTED_DIVERGENCE = {"citrus-aphids": "ant_exclusion"}

FORBIDDEN_METHODS = {"trap_cropping", "floating_row_cover"}

MATERIAL_OK = {
    ("lemon", "scale-insects"): ("horticultural_oil",),
    ("lemon", "citrus-aphids"): ("horticultural_oil", "insecticidal_soap"),
    ("lemon", "citrus-leafminer"): ("horticultural_oil",),
    ("lemon", "citrus-mites"): ("horticultural_oil",),
    ("lemon", "mealybugs"): ("horticultural_oil", "insecticidal_soap"),
    ("lemon", "greasy-spot"): ("copper_fungicide",),
    ("lemon", "citrus-canker"): ("copper_fungicide",),
    ("lime", "citrus-leafminer"): ("horticultural_oil",),
    ("lime", "citrus-aphids"): ("horticultural_oil", "insecticidal_soap"),
    ("lime", "scale-insects"): ("horticultural_oil",),
    ("lime", "citrus-mites"): ("horticultural_oil",),
    ("lime", "mealybugs"): ("horticultural_oil", "insecticidal_soap"),
    ("lime", "citrus-canker"): ("copper_fungicide",),
    ("lime", "lime-anthracnose"): ("copper_fungicide",),
    ("lime", "greasy-spot"): ("copper_fungicide",),
    ("lime", "postbloom-fruit-drop"): ("copper_fungicide",),
}

TEMP_FIGURE = re.compile(r"\d+\s*°\s*F|\d+\s*degrees", re.I)
LADDER_VOCAB = re.compile(r"\b(?:rung|ladder|tier)s?\b", re.I)

# IMPORTED, never retyped. The first cut of this promote carried its own copy and had
# `mite: {"mite"}` where the gate has `mite: {"mite", "insect_general"}`, which refused
# `beneficial_predators` on citrus-mites even though control_ladder_gate passes it. Predatory mites
# ARE the natural enemy there, so a hand-copied table would have rejected correct content. Batch
# 17's promote carries the same divergence latently; it had no mite-typed problem so it never
# fired, but the copy is wrong there too.
from control_ladder_gate import TYPE_TARGETS as _TYPE_TARGETS  # noqa: E402


def _type_ok(t, applies):
    return bool(_TYPE_TARGETS.get(t, set()) & set(applies))


def hygiene(s):
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


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# ------------------------------------------------------------------ pre-state checks
def check_schema_premise(by):
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: %s not on the roster" % c)
        for _f, p in problems(by[c]):
            if p.get("control_ladder"):
                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))
            for f in PREMISE_FIELDS:
                if not (p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%s missing %s" % (c, p.get("name"), f))


def check_type_transition(batch, by):
    """`type` on citrus is MIXED, unlike stone fruit, and the difference was MEASURED not assumed.

    Batch 17's crops all carried the coarse legacy value, so that promote could assert a clean
    coarse -> fine upgrade. Citrus does not: 21 of these 24 problems ALREADY carry a fine type and
    only 3 are coarse. (Roster-wide the field is messier still: of the unladdered problems, 129
    carry NO type at all, alongside pest/disease/insect/fungal/mite/other. Batch 17's docstring
    generalized from its own six crops; its GUARD was correctly scoped to those crops, but the
    claim around it was wider than what was measured.)

    So the rule here is two-sided, and the second half is the one that matters: an already-fine
    type must be PRESERVED EXACTLY, never quietly rewritten. The three legitimate upgrades are
    pinned by name, so a fourth would refuse rather than ride along.
    """
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                pre, post = p.get("type"), o.get("type")
                name = p.get("name")
                if post not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s post type %r is not a fine type"
                                     % (c, name, post))
                if pre in _TYPE_TARGETS:
                    if post != pre:
                        raise SystemExit("REFUSED: %s/%s SILENT RETYPE %r -> %r. An already-fine "
                                         "type is preserved, not rewritten; changing it moves "
                                         "which methods are legal on the problem."
                                         % (c, name, pre, post))
                    continue
                if (c, name) not in EXPECTED_TYPE_UPGRADES:
                    raise SystemExit("REFUSED: %s/%s upgrades %r -> %r but is not a pinned upgrade"
                                     % (c, name, pre, post))
                if EXPECTED_TYPE_UPGRADES[(c, name)] != (pre, post):
                    raise SystemExit("REFUSED: %s/%s upgrade %r -> %r != pinned %r"
                                     % (c, name, pre, post, EXPECTED_TYPE_UPGRADES[(c, name)]))
    got = {(c, p.get("name")) for c in CROPS for _f, p in problems(by[c])
           if p.get("type") not in _TYPE_TARGETS}
    if got != set(EXPECTED_TYPE_UPGRADES):
        raise SystemExit("REFUSED: the set of coarse-typed problems is %r, pinned %r"
                         % (sorted(got), sorted(EXPECTED_TYPE_UPGRADES)))


def check_ids(batch, by, data):
    existing = roster_ids(data, exclude=CROPS)
    for c in CROPS:
        for field in ("pests", "diseases"):
            names = [p.get("name") for p in by[c].get(field) or []]
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


def check_sooty_mold_is_laddered(batch, cm):
    """THE guard this batch exists for. `sooty-mold` shipped `control_ladder: null` on base
    2a9d3c85 because a fungal type could name no insect method. If it is unladdered again, or has
    lost its ant_exclusion rung, the ant_exclusion mint accomplished nothing."""
    found = False
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p.get("id") != "sooty-mold":
                continue
            found = True
            L = p.get("control_ladder")
            if not L:
                raise SystemExit("REFUSED: %s/sooty-mold is unladdered again (%r). The whole point "
                                 "of the ant_exclusion mint was to make this ladderable." % (c, L))
            if "ant_exclusion" not in [r["method"] for r in L]:
                raise SystemExit("REFUSED: %s/sooty-mold lost its ant_exclusion rung; nothing else "
                                 "in the catalog reaches a fungal type with an insect control" % c)
            if p.get("type") != "fungal":
                raise SystemExit("REFUSED: %s/sooty-mold retyped to %r. If it is no longer fungal "
                                 "the mint's disease_general scope is no longer what carries it"
                                 % (c, p.get("type")))
    if not found:
        raise SystemExit("REFUSED: no sooty-mold problem in the batch; this guard would be vacuous")
    if "ant_exclusion" not in cm:
        raise SystemExit("REFUSED: ant_exclusion is not in the catalog; base is not the mint")


def check_ant_exclusion_precedes_predators(batch, cm):
    """The mechanism claim, asserted on the DATA. The sources say exclude ants SO THAT natural
    enemies can work, so wherever both rungs appear the exclusion must come first."""
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            ms = [r["method"] for r in p.get("control_ladder") or []]
            if "ant_exclusion" not in ms:
                continue
            seen += 1
            if cm["ant_exclusion"]["tier"] != "physical":
                raise SystemExit("REFUSED: ant_exclusion is no longer physical, so it can no "
                                 "longer be ordered before the biological rung it enables")
            if "beneficial_predators" in ms and ms.index("ant_exclusion") > ms.index(
                    "beneficial_predators"):
                raise SystemExit("REFUSED: %s/%s puts ant_exclusion AFTER beneficial_predators; "
                                 "the rung that removes the suppression must precede the rung it "
                                 "enables" % (c, p["id"]))
    if seen == 0:
        raise SystemExit("REFUSED: no ant_exclusion rung in the batch; this guard would be vacuous")


def check_shared_id_divergence(batch):
    """A shared id may carry different ladders where the RECORDS differ (this batch's ruling), but
    every such divergence is pinned by name and by the exact rung that differs. Anything else is
    the batch-17 `plum-curculio` defect: one join key carrying two shapes for the same content."""
    ladders = {}
    for c in CROPS:
        for _f, p in problems(batch[c]):
            ladders.setdefault(p["id"], {})[c] = [r["method"] for r in p.get("control_ladder") or []]
    checked = 0
    for pid, per in sorted(ladders.items()):
        if len(per) < 2:
            continue
        checked += 1
        a, b = per["lemon"], per["lime"]
        if a == b:
            if pid in PERMITTED_DIVERGENCE:
                raise SystemExit("REFUSED: %r is pinned as a PERMITTED divergence but its ladders "
                                 "now match. Remove the pin rather than leaving a dead exception."
                                 % pid)
            continue
        allowed = PERMITTED_DIVERGENCE.get(pid)
        if allowed is None:
            raise SystemExit("REFUSED: shared id %r diverges and is not permitted to. lemon=%r "
                             "lime=%r" % (pid, a, b))
        if [m for m in a if m != allowed] != [m for m in b if m != allowed]:
            raise SystemExit("REFUSED: %r diverges by more than the permitted %r rung. lemon=%r "
                             "lime=%r" % (pid, allowed, a, b))
    if checked == 0:
        raise SystemExit("REFUSED: no shared ids found; this guard would be vacuous")


def check_no_temperature_figures(batch):
    """Ruled this batch: the crops say oil is unsafe above 95°F, the catalog caution says 90°F, and
    the mite entries carry no figure at all yet their rungs had imported one. No rung asserts a
    temperature; the method's caution supplies it, so the stricter figure governs."""
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    m = TEMP_FIGURE.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s states a temperature (%r). The "
                                         "method's own caution carries the figure so no rung can "
                                         "contradict it." % (c, p["id"], r["method"], f, m.group(0)))


def check_no_ladder_vocabulary(batch):
    """Carried forward from batch 17. Internal vocabulary in grower-facing copy, and in this batch
    it also took the form of cross-problem pointers ("the same limits as the scale rung")."""
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    m = LADDER_VOCAB.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s uses internal vocabulary (%r); a "
                                         "grower does not know what a rung is"
                                         % (c, p["id"], r["method"], f, m.group(0)))


def validate_batch(batch, cm):
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
            seen, last = set(), -1
            for r in L:
                m = r.get("method")
                if m not in cm:
                    raise SystemExit("REFUSED: %s/%s unknown method %r" % (c, p["id"], m))
                if m in FORBIDDEN_METHODS:
                    raise SystemExit("REFUSED: %s/%s forbidden method %r" % (c, p["id"], m))
                if m in seen:
                    raise SystemExit("REFUSED: %s/%s duplicate method %r" % (c, p["id"], m))
                seen.add(m)
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
    if rung_count(batch) != TOTAL_RUNGS:
        raise SystemExit("REFUSED: %d rungs total, expected %d" % (rung_count(batch), TOTAL_RUNGS))


def check(data):
    by = by_slug(data)
    batch = staged()
    cm = data["control_methods"]
    check_schema_premise(by)
    check_type_transition(batch, by)
    check_ids(batch, by, data)
    check_sooty_mold_is_laddered(batch, cm)
    check_ant_exclusion_precedes_predators(batch, cm)
    check_shared_id_divergence(batch)
    check_no_temperature_figures(batch)
    check_no_ladder_vocabulary(batch)
    validate_batch(batch, cm)
    return batch


def snapshot(data):
    out = {}
    for c in data["crops"]:
        for f, p in problems(c):
            out[(c["slug"], f, p.get("name"))] = (p.get("id"), p.get("type"),
                                                  len(p.get("control_ladder") or []))
    return out


def apply_to(data):
    batch = check(data)
    by = by_slug(data)
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                p["id"] = o["id"]
                p["type"] = o["type"]
                p["control_ladder"] = copy.deepcopy(o["control_ladder"])
    return data


def verify_post(pre, data):
    post = snapshot(data)
    if set(pre) != set(post):
        raise SystemExit("REFUSED: problem set changed. added=%r dropped=%r"
                         % (sorted(set(post) - set(pre))[:5], sorted(set(pre) - set(post))[:5]))
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
        raise SystemExit("REFUSED: control_methods changed; this batch USES the mint, it does not "
                         "extend the catalog")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed")

    blob = serialize(data)
    print("problems laddered : %d" % touched)
    print("rungs             : %d" % TOTAL_RUNGS)
    print("base  SHA         : %s" % sha)
    print("post  SHA         : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
