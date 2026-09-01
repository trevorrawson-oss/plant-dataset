#!/usr/bin/env python3
"""PLA-8 BATCH 19 -- SWEET CITRUS: grapefruit, mandarin-clementine, orange-navel.
Base 514903db (batch 18, acid citrus).

32 problems gain `id` and a `control_ladder`; **108 rungs**. Roster laddered 81 -> 84. NO catalog
mutation. Citrus closes here: all five crops are laddered.

--------------------------------------------------------------------------------------------------
THE DEFINING DIFFERENCE FROM EVERY EARLIER BATCH: THE SHARED IDS ARE ALREADY SHIPPED
--------------------------------------------------------------------------------------------------
Batch 18's divergence guard compared lemon against lime, both inside the batch. Nine of this batch's
fifteen ids ALREADY EXIST on lemon or lime at the base commit, so the comparison is against
CANONICAL, not against a sibling in the staging directory. A guard that only looked within the batch
would pass three crops that silently contradict two shipped ones.

`check_cross_batch_divergence` is therefore the guard this batch exists for. It reads every crop on
the roster that carries a shared id, not just the three being promoted.

--------------------------------------------------------------------------------------------------
ZERO TYPE UPGRADES -- THE FIRST BATCH WHERE THE TYPE RULE IS PURE PRESERVATION
--------------------------------------------------------------------------------------------------
Batch 17's crops were all coarse (`pest`/`disease`) and it asserted a clean coarse -> fine upgrade.
Batch 18 was MIXED: 21 already fine, 3 coarse, so its guard was two-sided.

All 32 problems here already carry a fine type. There is no upgrade to allow, so the rule collapses
to its strong form: **no type may change at all.** That is a stricter guard than either predecessor
could use, and it is only correct because it was MEASURED rather than assumed.

--------------------------------------------------------------------------------------------------
THE TAXON TRAP, REFUSED BY NAME
--------------------------------------------------------------------------------------------------
orange-navel's "Brown rot of fruit" must NOT take `brown-rot`. That id belongs to six stone fruit
where the organism is the fungus *Monilinia fructicola*; orange-navel's own record says the cause is
soil-borne *Phytophthora*, "the same water molds that cause foot rot". Same common name, unrelated
organisms: the `pea-weevil` shape. It ships `citrus-brown-rot`, and `check_brown_rot_taxon_split`
asserts both halves -- the citrus id exists, and `brown-rot` reaches no citrus.

It also does not reuse `phytophthora-foot-rot`, though its own prose says that IS the same organism:
different organ, different symptoms, different controls.

--------------------------------------------------------------------------------------------------
THE MITES SPLIT, AND THE COMPOSITE IS NOT RETRO-SPLIT
--------------------------------------------------------------------------------------------------
Acid citrus carries ONE composite `citrus-mites`, and both records say why ("Several mite species
feed by puncturing leaf cells"). Sweet citrus splits them into single-species entries whose records
assert the distinction: grapefruit's rust mite works the RIND and is driven by warmth and humidity
in the Southeast; the red mite works FOLIAGE and is driven by heat and dust. Different family,
organ, and regional driver, so they ship `citrus-rust-mite` and `citrus-red-mite`.

`citrus-mites` on lemon and lime is NOT re-derived. It was pinned one commit ago and those records
are genuinely composite. `check_mite_split` asserts BOTH directions, so a later pass cannot tidy the
model by collapsing the new ids or by splitting the old one.

--------------------------------------------------------------------------------------------------
A STANDING RULING FROM BATCH 18, NOW ENFORCED ROSTER-WIDE
--------------------------------------------------------------------------------------------------
Batch 18 ruled that `citrus-canker` may not carry `prune_out_infection`, because that method means
taking the cut back into clean tissue and implies a curative excision every canker record denies
("There is no cure for an infected tree"). Grapefruit's first authored ladder used it anyway, with
prose that already said "it does not clear the tree" -- honest prose, wrong key. Re-keyed at the
read. `check_canker_is_not_curative` now enforces the ruling on EVERY crop carrying the id, so the
next citrus batch cannot reintroduce it.

REFUSALS: base SHA mismatch; a target already laddered; ANY type change; an id off the convention
table; any refused id anywhere; a reuse resolving nowhere or losing its anchor; a new id already
taken; `brown-rot` on a citrus or `citrus-brown-rot` missing; the mite split collapsed in either
direction; an unpinned cross-batch divergence, or a pinned one that has converged; a curative key on
citrus-canker; a temperature figure or ladder vocabulary in any rung; a material outside
MATERIAL_OK; unknown method; tier decrease; applies_to incoherence; identical registers; duplicate
method; empty ladder; counts off; ANY change to control_methods, source_catalog, or a bystander.

Guard suite:      tools/test_promote_pla8_batch19.py
Mutation harness: tools/mutate_pla8_batch19_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch19.py [--apply] [--dry-run] [--canonical PATH]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch19_sweet_citrus")
BASE_SHA = "514903dbaa59fa66d550fc88525d56dcdfe7150398f6f639e5b5905f1ddf85e4"

CROPS = ("grapefruit", "mandarin-clementine", "orange-navel")
ACID = ("lemon", "lime")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
PREMISE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                  "organic_treatment_beginner", "organic_treatment_seasoned",
                  "prevention_beginner", "prevention_seasoned")

EXPECTED_PROBLEMS = {"grapefruit": 11, "mandarin-clementine": 9, "orange-navel": 12}
EXPECTED_RUNGS = {"grapefruit": 35, "mandarin-clementine": 32, "orange-navel": 41}
TOTAL_RUNGS = 108

ID_CONVENTION = {
    "Asian citrus psyllid": "asian-citrus-psyllid",
    "Citrus rust mite": "citrus-rust-mite",
    "Citrus red mite": "citrus-red-mite",
    "Scale insects": "scale-insects",
    "Aphids": "citrus-aphids",
    "Citrus leafminer": "citrus-leafminer",
    "Katydids and fruit-surface chewers": "katydids",
    "Huanglongbing (citrus greening, HLB)": "huanglongbing",
    "Phytophthora foot rot, root rot, and gummosis": "phytophthora-foot-rot",
    "Greasy spot": "greasy-spot",
    "Melanose": "melanose",
    "Alternaria brown spot": "alternaria-brown-spot",
    "Citrus canker": "citrus-canker",
    "Sooty mold": "sooty-mold",
    "Brown rot of fruit": "citrus-brown-rot",
}

# Every id already living on lemon or lime at the base. The anchor is where the join must still land.
REUSED_IDS = {
    "scale-insects": "lemon", "citrus-aphids": "lemon", "citrus-leafminer": "lemon",
    "phytophthora-foot-rot": "lemon", "greasy-spot": "lemon", "citrus-canker": "lemon",
    "sooty-mold": "lemon", "asian-citrus-psyllid": "lemon", "huanglongbing": "lemon",
}
NEW_IDS = ("melanose", "alternaria-brown-spot", "katydids", "citrus-brown-rot",
           "citrus-rust-mite", "citrus-red-mite")

# Every id this batch puts on MORE THAN ONE crop. The nine reused ones plus `citrus-red-mite`,
# which mandarin-clementine and orange-navel both carry (grapefruit's mite is the RUST mite, a
# different species on a different organ). Written out rather than derived: the first cut asserted
# `len(REUSED_IDS)` here and refused the correct batch, because "shared with acid citrus" and
# "appears on two crops" are not the same set.
EXPECTED_SHARED_IDS = set(REUSED_IDS) | {"citrus-red-mite"}

REFUSED_IDS = {
    "brown-rot": "six stone fruit, Monilinia fructicola; citrus brown rot is soil-borne Phytophthora",
    "citrus-mites": "the acid-citrus COMPOSITE; these records name one mite species each",
    "aphids": "generic roster aphid on 50 vegetable crops",
    "spider-mites": "twospotted-focused generic on 15 crops",
    "anthracnose": "generic on 14 crops",
    "bacterial-spot": "the peppers' Xanthomonas leaf spot; citrus canker is X. citri",
}

# A shared id may carry different ladders across crops ONLY where the RECORDS differ (batch 18's
# rule). Each entry below was adjudicated by reading all the records; the reason is the evidence.
CROSS_BATCH_DIVERGENCE = {
    "citrus-aphids":
        "lime ALONE lacks ant_exclusion. Pinned by batch 18: lime has no sooty mold entry, so the "
        "sentence tying its aphids to ant-tended honeydew exists nowhere in its record.",
    "greasy-spot":
        "lemon and lime say 'avoid overhead wetting of foliage' and carry water_at_the_base. No "
        "sweet-citrus record names an irrigation practice, so none carries that rung.",
    "asian-citrus-psyllid":
        "OPPOSITE ADVICE. lemon and lime say 'spraying your own tree does little' and prescribe "
        "detection, reporting and removing infected trees. All three sweet citrus prescribe oil and "
        "soap on the new flush and name Tamarixia.",
    "citrus-canker":
        "certified_clean_stock, airflow_spacing and resistant_varieties each track whether that "
        "crop's own prevention prose names them; no two of the five records name the same set.",
}

FORBIDDEN_METHODS = {"trap_cropping", "floating_row_cover"}

MATERIAL_OK = {
    ("grapefruit", "asian-citrus-psyllid"): ("insecticidal_soap", "horticultural_oil"),
    ("grapefruit", "citrus-aphids"): ("insecticidal_soap", "horticultural_oil"),
    ("grapefruit", "citrus-canker"): ("copper_fungicide",),
    ("grapefruit", "citrus-leafminer"): ("horticultural_oil",),
    ("grapefruit", "citrus-rust-mite"): ("horticultural_oil", "sulfur"),
    ("grapefruit", "greasy-spot"): ("copper_fungicide",),
    ("grapefruit", "melanose"): ("copper_fungicide",),
    ("grapefruit", "scale-insects"): ("horticultural_oil",),
    ("mandarin-clementine", "alternaria-brown-spot"): ("copper_fungicide",),
    ("mandarin-clementine", "asian-citrus-psyllid"): ("insecticidal_soap", "horticultural_oil"),
    ("mandarin-clementine", "citrus-aphids"): ("insecticidal_soap", "horticultural_oil"),
    ("mandarin-clementine", "citrus-leafminer"): ("horticultural_oil",),
    ("mandarin-clementine", "citrus-red-mite"): ("horticultural_oil",),
    ("mandarin-clementine", "greasy-spot"): ("copper_fungicide",),
    ("mandarin-clementine", "scale-insects"): ("horticultural_oil",),
    ("orange-navel", "asian-citrus-psyllid"): ("insecticidal_soap", "horticultural_oil"),
    ("orange-navel", "citrus-aphids"): ("insecticidal_soap", "horticultural_oil"),
    ("orange-navel", "citrus-brown-rot"): ("copper_fungicide",),
    ("orange-navel", "citrus-canker"): ("copper_fungicide",),
    ("orange-navel", "citrus-leafminer"): ("horticultural_oil",),
    ("orange-navel", "citrus-red-mite"): ("horticultural_oil",),
    ("orange-navel", "greasy-spot"): ("copper_fungicide",),
    ("orange-navel", "scale-insects"): ("horticultural_oil",),
}

TEMP_FIGURE = re.compile(r"\d+\s*°\s*F|\d+\s*degrees", re.I)
LADDER_VOCAB = re.compile(r"\b(?:rung|ladder|tier)s?\b", re.I)

# IMPORTED, never retyped. A hand-copied table had `mite: {"mite"}` where the gate has
# `mite: {"mite", "insect_general"}`, which would REFUSE correct content on the two mite problems.
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


def check_type_preservation(batch, by):
    """MEASURED: all 32 problems already carry a fine type, so there is no upgrade to permit and the
    rule takes its strong form. Any type change at all is refused."""
    checked = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                pre, post = p.get("type"), o.get("type")
                if pre not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s pre-state type %r is COARSE. This promote "
                                     "asserts every type is already fine; that premise is broken "
                                     "and the preservation rule is the wrong rule."
                                     % (c, p.get("name"), pre))
                if post != pre:
                    raise SystemExit("REFUSED: %s/%s type changed %r -> %r. Batch 19 upgrades no "
                                     "type; changing one moves which methods are legal."
                                     % (c, p.get("name"), pre, post))
                checked += 1
    if checked != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: type check covered %d problems, expected %d"
                         % (checked, sum(EXPECTED_PROBLEMS.values())))


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


def check_brown_rot_taxon_split(batch, data):
    """THE TAXON TRAP. `brown-rot` is Monilinia fructicola on six stone fruit; orange-navel's own
    record says its brown rot is soil-borne Phytophthora, a water mold. Same common name, unrelated
    organisms -- reusing the id would merge them and make any resistance grade meaningless."""
    found = False
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p.get("id") == "brown-rot":
                raise SystemExit("REFUSED: %s took `brown-rot`, which is Monilinia on stone fruit; "
                                 "citrus brown rot is Phytophthora" % c)
            if p.get("id") == "citrus-brown-rot":
                found = True
    if not found:
        raise SystemExit("REFUSED: no citrus-brown-rot in the batch; this guard would be vacuous")
    holders = roster_ids(data, exclude=CROPS).get("brown-rot") or set()
    if not holders:
        raise SystemExit("REFUSED: `brown-rot` exists nowhere off-batch, so the id this guard "
                         "protects against colliding with is gone and the split is unmotivated")
    # NOT `holders & set(CROPS)`: `holders` is computed with exclude=CROPS, so that test could
    # never be true and the branch was dead. The reachable, meaningful question is whether the id
    # has already leaked onto the ACID citrus, which do carry ids at this base.
    if holders & set(ACID):
        raise SystemExit("REFUSED: `brown-rot` already reaches an acid citrus (%s); the stone-fruit "
                         "id has been contaminated and the split is no longer clean"
                         % sorted(holders & set(ACID)))


def check_mite_split(batch, data):
    """Asserted in BOTH directions. The new species-specific ids must exist, and the acid-citrus
    COMPOSITE must survive unchanged -- a later pass must not tidy the model by collapsing the new
    ids into `citrus-mites`, nor by re-deriving the composite into species ids."""
    got = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    for pid in ("citrus-rust-mite", "citrus-red-mite"):
        if pid not in got:
            raise SystemExit("REFUSED: %r missing; the mite split is what these records assert"
                             % pid)
    if "citrus-mites" in got:
        raise SystemExit("REFUSED: a sweet citrus took the COMPOSITE `citrus-mites`; these records "
                         "name one mite species each, with different organs and drivers")
    composite = roster_ids(data, exclude=CROPS).get("citrus-mites") or set()
    if not composite & set(ACID):
        raise SystemExit("REFUSED: `citrus-mites` no longer sits on lemon or lime. The composite is "
                         "NOT retro-split; those records genuinely say 'several mite species'.")


def check_canker_is_not_curative(batch, data):
    """A STANDING RULING from batch 18, now enforced roster-wide. `prune_out_infection` means taking
    the cut back into clean tissue and implies a curative excision every canker record denies
    ('no cure', 'without curing existing ones')."""
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p.get("id") != "citrus-canker":
                continue
            seen += 1
            if "prune_out_infection" in [r["method"] for r in p.get("control_ladder") or []]:
                raise SystemExit("REFUSED: %s/citrus-canker carries prune_out_infection, a CURATIVE "
                                 "excision its own record denies" % c)
    for c in ACID:
        for _f, p in problems(by_slug(data)[c]):
            if p.get("id") == "citrus-canker":
                seen += 1
                if "prune_out_infection" in [r["method"] for r in p.get("control_ladder") or []]:
                    raise SystemExit("REFUSED: shipped %s/citrus-canker carries prune_out_infection; "
                                     "the batch 18 ruling has been undone" % c)
    if seen == 0:
        raise SystemExit("REFUSED: no citrus-canker ladder anywhere; this guard would be vacuous")


def check_cross_batch_divergence(batch, data):
    """THE GUARD THIS BATCH EXISTS FOR. Nine ids already live on lemon or lime, so the comparison is
    against CANONICAL and not merely against a sibling in the staging directory. A within-batch
    check would pass three crops that silently contradict two shipped ones."""
    lad = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if p.get("id") and p.get("control_ladder"):
                lad.setdefault(p["id"], {})[c["slug"]] = tuple(
                    r["method"] for r in p["control_ladder"])
    for c in CROPS:
        for _f, p in problems(batch[c]):
            lad.setdefault(p["id"], {})[c] = tuple(r["method"] for r in p["control_ladder"])

    batch_ids = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    shared = set()
    for pid in sorted(batch_ids):
        per = lad.get(pid) or {}
        if len(per) < 2:
            continue
        shared.add(pid)
        shapes = set(per.values())
        if len(shapes) > 1 and pid not in CROSS_BATCH_DIVERGENCE:
            raise SystemExit("REFUSED: shared id %r carries %d different ladders and is not a "
                             "pinned divergence: %r" % (pid, len(shapes),
                                                        {k: list(v) for k, v in sorted(per.items())}))
        if len(shapes) == 1 and pid in CROSS_BATCH_DIVERGENCE:
            raise SystemExit("REFUSED: %r is pinned as a permitted divergence but every crop now "
                             "carries the same ladder. Remove the pin rather than leaving a dead "
                             "exception." % pid)
    if not shared:
        raise SystemExit("REFUSED: no shared ids found; this guard would be vacuous")
    if shared != EXPECTED_SHARED_IDS:
        raise SystemExit("REFUSED: the set of multi-crop ids is %r, pinned %r"
                         % (sorted(shared), sorted(EXPECTED_SHARED_IDS)))


def check_no_temperature_figures(batch):
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    m = TEMP_FIGURE.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s states a temperature (%r); the "
                                         "method's caution carries the figure"
                                         % (c, p["id"], r["method"], f, m.group(0)))


def check_no_ladder_vocabulary(batch):
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    m = LADDER_VOCAB.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s uses internal vocabulary (%r)"
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
    check_type_preservation(batch, by)
    check_ids(batch, by, data)
    check_brown_rot_taxon_split(batch, data)
    check_mite_split(batch, data)
    check_canker_is_not_curative(batch, data)
    check_cross_batch_divergence(batch, data)
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
        raise SystemExit("REFUSED: control_methods changed; this batch mints nothing")
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
