#!/usr/bin/env python3
"""PLA-8 BATCH 20 -- BERRIES: blackberry, blueberry, raspberry, elderberry.
Base 50bc203f (batch 19, sweet citrus).

39 problems gain `id`, a `type` and a `control_ladder`; **140 rungs**. Roster laddered 84 -> 88.
NO catalog mutation. The Berries & Shrubs category closes (strawberry was already laddered).

--------------------------------------------------------------------------------------------------
THE TYPE RULE TAKES A THIRD FORM, AND IT WAS MEASURED
--------------------------------------------------------------------------------------------------
Batch 17's crops were uniformly COARSE (`pest`/`disease`) and it asserted a coarse -> fine upgrade.
Batch 18 was MIXED and needed a two-sided rule. Batch 19 was uniformly FINE and took the strong
preservation form.

All 39 problems here carry **NO `type` AT ALL** (`None`). So the rule is a third thing again: every
type is SET from nothing, and a pre-state that already carries any type breaks the premise. Each of
the four batches measured this rather than inheriting the previous batch's assumption, which is the
only reason four different rules are all correct.

--------------------------------------------------------------------------------------------------
THE CROSS-BATCH DIVERGENCE GUARD NEEDED A DIFFERENT DESIGN FROM BATCH 19'S
--------------------------------------------------------------------------------------------------
Batch 19 could assert that a shared id carries ONE ladder shape unless pinned. That assumption is
FALSE here and would have refused a correct batch:

    aphids           50 holders, 17 distinct shapes
    powdery-mildew   28 holders, 12 distinct shapes

Those are broad generics that already diverge roster-wide, and demanding one shape across 50 crops
is not a check, it is a bug. The other shared ids are narrow and coherent:

    birds  3/1     japanese-beetles  3/1     scale-insects  5/1
    spotted-wing-drosophila  3/2            stink-bugs  1/1

So the guard splits them. Narrow ids are shape-compared and every divergence is pinned with the
record-level reason. Broad generics are EXEMPT -- but the exemption is not taken on trust:
`check_broad_generic_exemption_is_earned` re-measures each exempt id and refuses if it is not
actually broad, so a narrow id cannot be smuggled onto the exempt list to silence a real divergence.

--------------------------------------------------------------------------------------------------
THE ANTHRACNOSE TAXON TRAP IS THREE-WAY
--------------------------------------------------------------------------------------------------
One common name, three organisms, per the records' own prose:

* the roster's generic `anthracnose` (14 vegetable crops) is *Colletotrichum orbiculare*
* blackberry and raspberry are ***Elsinoe veneta*** -- a different GENUS -> `cane-anthracnose`
* blueberry is a *Colletotrichum* RIPE FRUIT ROT -> `blueberry-ripe-rot`

`phytophthora-root-rot` is likewise NOT citrus's `phytophthora-foot-rot`: same genus, different
organ, different controls.

--------------------------------------------------------------------------------------------------
A PRE-EXISTING ROSTER DEFECT THIS BATCH REFUSES TO WIDEN
--------------------------------------------------------------------------------------------------
`japanese-beetle` (singular, basil) and `japanese-beetles` (plural, marigold/zinnia/echinacea) are
BOTH live for *Popillia japonica*. blackberry and raspberry name the singular, elderberry the plural,
so name-derived slugs would have put a third crop on each side. All three take the PLURAL.
`check_japanese_beetle_split_not_widened` pins that and also pins the defect itself, so the day basil
is repointed the guard reminds whoever does it that this batch depends on the plural.

REFUSALS: base SHA mismatch; a target already laddered; a pre-state type present; an id off the
convention table; any refused id; a reuse resolving nowhere or losing its anchor; a new id already
taken; the anthracnose split collapsed; the Japanese beetle split widened; an unpinned narrow
divergence or a converged pin; a broad-generic exemption that is not earned; a temperature figure or
ladder vocabulary; a material outside MATERIAL_OK; unknown method; tier decrease; applies_to
incoherence; identical registers; duplicate method; empty ladder; counts off; ANY change to
control_methods, source_catalog, or a bystander.

Guard suite:      tools/test_promote_pla8_batch20.py
Mutation harness: tools/mutate_pla8_batch20_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch20.py [--apply] [--dry-run] [--canonical PATH]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch20_berries")
BASE_SHA = "50bc203faddfb10f2fddb56bc0361c107efc8e3d0095b3a740c34b24d7b78ba8"

CROPS = ("blackberry", "blueberry", "raspberry", "elderberry")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
PREMISE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                  "organic_treatment_beginner", "organic_treatment_seasoned",
                  "prevention_beginner", "prevention_seasoned")

EXPECTED_PROBLEMS = {"blackberry": 11, "blueberry": 10, "raspberry": 10, "elderberry": 8}
EXPECTED_RUNGS = {"blackberry": 45, "blueberry": 36, "raspberry": 38, "elderberry": 21}
TOTAL_RUNGS = 140

ID_CONVENTION = {
    "Spotted-wing drosophila (SWD)": "spotted-wing-drosophila",
    "Spotted-wing drosophila and sap beetles": "spotted-wing-drosophila",
    "Red-necked cane borer": "red-necked-cane-borer",
    "Raspberry crown borer": "raspberry-crown-borer",
    "Raspberry cane borer": "raspberry-cane-borer",
    "Stink bugs": "stink-bugs",
    "Japanese beetle": "japanese-beetles",
    "Japanese beetles": "japanese-beetles",
    "Aphids": "aphids",
    "Birds": "birds",
    "Blueberry maggot": "blueberry-maggot",
    "Scale insects": "scale-insects",
    "Elder shoot and stem borers": "elder-borers",
    "Phytophthora root rot": "phytophthora-root-rot",
    "Rosette (double blossom)": "rosette-double-blossom",
    "Anthracnose": "cane-anthracnose",
    "Anthracnose (ripe rot)": "blueberry-ripe-rot",
    "Cane and spur blight": "cane-blight",
    "Cane blight and spur blight": "cane-blight",
    "Orange rust": "orange-rust",
    "Raspberry mosaic virus complex": "raspberry-mosaic-virus",
    "Mummy berry": "mummy-berry",
    "Botrytis blossom blight (gray mold)": "botrytis-blossom-blight",
    "Stem blight and twig dieback": "stem-blight",
    "Elderberry rust": "elderberry-rust",
    "Powdery mildew": "powdery-mildew",
    "Cane canker and dieback": "cane-canker-dieback",
}

REUSED_IDS = {
    "spotted-wing-drosophila": "strawberry", "birds": "strawberry", "aphids": "strawberry",
    "scale-insects": "lemon", "japanese-beetles": "marigold", "powdery-mildew": "apple",
    "stink-bugs": "okra",
}
NEW_IDS = ("red-necked-cane-borer", "raspberry-crown-borer", "raspberry-cane-borer",
           "blueberry-maggot", "elder-borers", "phytophthora-root-rot", "rosette-double-blossom",
           "cane-anthracnose", "blueberry-ripe-rot", "cane-blight", "orange-rust",
           "raspberry-mosaic-virus", "mummy-berry", "botrytis-blossom-blight", "stem-blight",
           "elderberry-rust", "cane-canker-dieback")

REFUSED_IDS = {
    "anthracnose": "the vegetable generic, Colletotrichum orbiculare; cane anthracnose is Elsinoe veneta",
    "phytophthora-foot-rot": "citrus TRUNK and crown rot; this is a ROOT rot on a different host",
    "japanese-beetle": "the SINGULAR variant on basil; this batch takes the plural, see the split guard",
    "spider-mites": "not a berry problem in these records",
    "brown-rot": "Monilinia on stone fruit",
}

# NARROW shared ids: few holders, coherent shapes, so a divergence is meaningful and must be pinned
# with the record-level reason that justifies it.
NARROW_DIVERGENCE = {
    "spotted-wing-drosophila":
        "Chemistry tracks each record. strawberry names spinosad and a pyrethroid; cherry, and all "
        "four berries here, name no material at all. Rung count also tracks how much cultural "
        "detail each record carries (elderberry 3, blueberry 4, blackberry and raspberry 5).",
    "birds":
        "blueberry names only deterrents and netting; elderberry additionally names a cultivar whose "
        "drooping cyme hides fruit, and prompt harvest.",
    "japanese-beetles":
        "The flower crops carry a longer ladder; the berry records name only handpicking, plus "
        "netting where the record mentions it. blackberry's and raspberry's records say a home "
        "planting usually needs no spray.",
    "scale-insects":
        "The citrus ladders open on ant_exclusion because their records name ants tending the scale. "
        "blueberry's record mentions honeydew and sooty mold but names NO ants, and the method's own "
        "text says there is little reason to reach for it with no ant trail present.",
    "stink-bugs":
        "okra can name a preferred trap plant because its own guidance does; blackberry's record "
        "names none, so trap_cropping is not authorable here.",
}

# BROAD generics: already divergent roster-wide, so shape comparison is meaningless. The exemption is
# RE-MEASURED at run time by check_broad_generic_exemption_is_earned -- it is not taken on trust.
BROAD_GENERIC = ("aphids", "powdery-mildew")
BROAD_MIN_HOLDERS = 20
BROAD_MIN_SHAPES = 5

FORBIDDEN_METHODS = {"trap_cropping", "bt"}

MATERIAL_OK = {
    ("blackberry", "aphids"): ("insecticidal_soap",),
    ("blueberry", "aphids"): ("insecticidal_soap",),
    ("blueberry", "scale-insects"): ("horticultural_oil",),
    ("elderberry", "aphids"): ("insecticidal_soap",),
    ("raspberry", "aphids"): ("insecticidal_soap",),
}

TEMP_FIGURE = re.compile(r"\d+\s*°\s*F|\d+\s*degrees", re.I)
LADDER_VOCAB = re.compile(r"\b(?:rung|ladder|tier)s?\b", re.I)

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


def shapes_off_batch(data, pid):
    """Every distinct ladder shape this id already carries on crops OUTSIDE the batch."""
    out = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if p.get("id") == pid and p.get("control_ladder"):
                out[c["slug"]] = tuple(r["method"] for r in p["control_ladder"])
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


def check_type_is_set_from_nothing(batch, by):
    """MEASURED: all 39 carry NO type at all, so every type is SET rather than upgraded or
    preserved. A pre-state that already carries one breaks the premise this rule rests on."""
    checked = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                if p.get("type") is not None:
                    raise SystemExit("REFUSED: %s/%s pre-state already has type %r. This promote "
                                     "asserts every type is ABSENT; that premise is broken and the "
                                     "set-from-nothing rule is the wrong rule."
                                     % (c, p.get("name"), p.get("type")))
                if o.get("type") not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s post type %r is not a fine type"
                                     % (c, p.get("name"), o.get("type")))
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


def check_anthracnose_taxon_split(batch, data):
    """THREE organisms under one common name. The vegetable generic is Colletotrichum orbiculare;
    blackberry and raspberry are Elsinoe veneta, a different GENUS; blueberry is a Colletotrichum
    ripe fruit rot. Merging any pair would make a resistance grade meaningless."""
    got = {}
    for c in CROPS:
        for _f, p in problems(batch[c]):
            got.setdefault(p["id"], set()).add(c)
    if "anthracnose" in got:
        raise SystemExit("REFUSED: %s took the vegetable generic `anthracnose`; cane anthracnose is "
                         "Elsinoe veneta, a different genus" % sorted(got["anthracnose"]))
    for pid, want in (("cane-anthracnose", {"blackberry", "raspberry"}),
                      ("blueberry-ripe-rot", {"blueberry"})):
        if pid not in got:
            raise SystemExit("REFUSED: %r missing; the three-way anthracnose split is what these "
                             "records assert" % pid)
        if got[pid] != want:
            raise SystemExit("REFUSED: %r sits on %r, pinned %r" % (pid, sorted(got[pid]),
                                                                    sorted(want)))
    if "anthracnose" not in roster_ids(data, exclude=CROPS):
        raise SystemExit("REFUSED: the vegetable `anthracnose` exists nowhere off-batch, so the id "
                         "this split avoids colliding with is gone and the split is unmotivated")


def check_japanese_beetle_split_not_widened(batch, data):
    """A PRE-EXISTING roster defect: `japanese-beetle` (basil) and `japanese-beetles`
    (marigold/zinnia/echinacea) are both live for Popillia japonica. Two of this batch's crops name
    the singular and one the plural, so name-derived slugs would have put a third crop on each
    side. All three take the PLURAL."""
    off = roster_ids(data, exclude=CROPS)
    sing, plur = off.get("japanese-beetle") or set(), off.get("japanese-beetles") or set()
    if not sing or not plur:
        raise SystemExit("REFUSED: the japanese-beetle id split is not in the state this guard was "
                         "written against (singular=%r plural=%r). If basil has been repointed, "
                         "retire this guard deliberately rather than letting it pass."
                         % (sorted(sing), sorted(plur)))
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p["id"] == "japanese-beetle":
                raise SystemExit("REFUSED: %s took the SINGULAR `japanese-beetle`, widening a "
                                 "known roster split" % c)
            if p["id"] == "japanese-beetles":
                seen += 1
    if seen == 0:
        raise SystemExit("REFUSED: no japanese-beetles problem in the batch; this guard would be "
                         "vacuous")


def check_broad_generic_exemption_is_earned(data):
    """The exemption is RE-MEASURED, never trusted. Without this a narrow id could be added to
    BROAD_GENERIC to silence a real divergence, and every other test would still pass."""
    for pid in BROAD_GENERIC:
        sh = shapes_off_batch(data, pid)
        if len(sh) < BROAD_MIN_HOLDERS or len(set(sh.values())) < BROAD_MIN_SHAPES:
            raise SystemExit("REFUSED: %r is exempt from shape comparison but is not broad: "
                             "%d holders / %d distinct shapes, floor is %d / %d. A narrow id must "
                             "be pinned in NARROW_DIVERGENCE, not exempted."
                             % (pid, len(sh), len(set(sh.values())),
                                BROAD_MIN_HOLDERS, BROAD_MIN_SHAPES))


def check_cross_batch_divergence(batch, data):
    """Nine ids already live on shipped crops, so the comparison is against CANONICAL. Broad
    generics are exempt (see above); narrow ids are shape-compared and every divergence is pinned."""
    checked, diverged = set(), set()
    for c in CROPS:
        for _f, p in problems(batch[c]):
            pid = p["id"]
            if pid in BROAD_GENERIC:
                continue
            off = shapes_off_batch(data, pid)
            if not off:
                continue
            checked.add(pid)
            mine = tuple(r["method"] for r in p["control_ladder"])
            if mine not in set(off.values()):
                diverged.add(pid)
                if pid not in NARROW_DIVERGENCE:
                    raise SystemExit("REFUSED: %s/%s diverges from every shipped ladder for that id "
                                     "and is not a pinned divergence. mine=%r shipped=%r"
                                     % (c, pid, list(mine),
                                        {k: list(v) for k, v in sorted(off.items())}))
    for pid in NARROW_DIVERGENCE:
        if pid not in checked:
            raise SystemExit("REFUSED: %r is pinned as a narrow divergence but this batch never "
                             "compared it. Remove the pin rather than leaving a dead exception."
                             % pid)
        if pid not in diverged:
            raise SystemExit("REFUSED: %r is pinned as a narrow divergence but every batch ladder "
                             "for it now MATCHES a shipped one. A pin that no longer describes "
                             "reality is false documentation; remove it." % pid)
    if not checked:
        raise SystemExit("REFUSED: no narrow shared ids compared; this guard would be vacuous")


def check_no_temperature_figures(batch):
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    m = TEMP_FIGURE.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s states a temperature (%r)"
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
    check_type_is_set_from_nothing(batch, by)
    check_ids(batch, by, data)
    check_anthracnose_taxon_split(batch, data)
    check_japanese_beetle_split_not_widened(batch, data)
    check_broad_generic_exemption_is_earned(data)
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
