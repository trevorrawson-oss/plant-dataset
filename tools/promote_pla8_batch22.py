#!/usr/bin/env python3
"""PLA-8 BATCH 22 -- THE STRAGGLERS: english-cucumber, edamame, pumpkin.
Base fabdaae1 (batch 21, flowers).

26 problems gain `id`, a `type` and a `control_ladder`; **135 rungs**. Roster laddered 91 -> 94.
NO catalog mutation.

These are the three crops left over from families already laddered: english-cucumber from the
cucumbers, edamame from the legumes, pumpkin from the squashes. Every one of them has shipped
siblings, which is what makes this batch's hazard different from every batch before it.

--------------------------------------------------------------------------------------------------
THE PREMISE IS FULL-SCHEMA, AND THE TYPE RULE IS SPLIT BY CROP. BOTH WERE MEASURED, NOT INHERITED.
--------------------------------------------------------------------------------------------------
**Schema: FULL** (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`, `sources`,
`anchoring_urls`) -- the batch 17-20 shape. Batch 21 was NOTE-schema, and copying its
`check_note_schema_premise` would have refused this entire batch on its first guard. Asserted in
BOTH directions here too: the full-schema fields must be present AND the note pair must be absent.

**Type: SPLIT BY CROP -- a fifth distinct situation in six batches.**

  | crop             | pre-state           | rule              |
  |------------------|---------------------|-------------------|
  | english-cucumber | all `None` (9)      | set from nothing  |
  | pumpkin          | all `None` (8)      | set from nothing  |
  | edamame          | all COARSE (5+4)    | upgrade           |

Batch 17 was uniformly coarse, 18 mixed, 19 uniformly fine, 20 and 21 no type at all, 22 split by
crop. The type field is genuinely heterogeneous across this roster; it is measured every batch.
One further pre-state asymmetry, not in the handoff and found by measuring: **edamame's problems
carry `severity` and the other two crops' do not.** Pinned so a schema drift is visible.

--------------------------------------------------------------------------------------------------
THE DIVERGENCE GUARD WAS CHOSEN BY MEASUREMENT AND IT LANDED BETWEEN BATCH 20 AND BATCH 21
--------------------------------------------------------------------------------------------------
Measured BEFORE writing, over the 22 reused-id instances:

* 7 ladders EXACTLY MATCH a shipped sibling and 15 diverge -- almost batch 21's ratio. But batch 21
  concluded from that ratio that shape comparison was meaningless, and **that conclusion does not
  transfer**, because batch 21's crops were companion flowers converging on generic pests while
  these three are TEMPLATE SIBLINGS of already-laddered crops sharing authored prose.
* So the measurement that actually decides the guard is the cross-tab of SOURCE-PROSE identity
  against LADDER identity. **9 template twins exist** (a batch problem whose eight prose fields are
  byte-identical to a shipped sibling's): 6 agree on the ladder and **3 diverge, all of them the
  same one**, pumpkin/downy-mildew against butternut, acorn and spaghetti squash.

That is the batch 3 defect shape exactly -- cucumber and slicing-cucumber shared a byte-identical
`prevention_seasoned` while one keyed it to `resistant_varieties` and the other refused -- and it is
invisible to every gate because it only exists ACROSS crops. `check_template_sibling_divergence`
therefore earns the slot: where the prose is identical the ladder must match, and the single
adjudicated exception is pinned. A batch-20-style "pin every divergence" guard would have been 15
pins of noise here; batch 21's "no shape comparison at all" would have seen none of this.

**The one pinned divergence is correct and the SIBLINGS are the ones with the gap.** The shared
prose says "avoid working among wet vines"; `wet_foliage_discipline` MEANS choosing when you work,
explicitly distinct from watering at the base. Pumpkin carries the rung, the three squashes do not.
Measured roster-wide: 13 laddered problems carry that sentence without the rung. Filed, not fixed --
fixing shipped crops here would trip this promote's own bystander check.

`check_no_shipped_prose_echo` is carried over from batch 21 unchanged and MEASURED before adoption:
0 whole-note echoes and 0 sentence echoes from 270 batch notes against a 5,351-note / 8,840-sentence
shipped corpus. A guard that refuses an input and stays green is a REFUSAL-SPEC pass, and it is
worth most precisely where 7 ladders converge with a sibling: identical shape with independent prose
is convergent authoring, identical prose is copying.

--------------------------------------------------------------------------------------------------
TWO IDS ARE MINTED ALONGSIDE A SHORTER ROSTER ID THAT NAMES A COMPOUND PROBLEM
--------------------------------------------------------------------------------------------------
The pin table checked every intended mint against the roster BY ID, which is the fix batch 21's
failure earned. That check passes an id which merely RESEMBLES a live one, and a substring scan of
all 20 authored ids against the roster found two the table had not adjudicated:

* **`bacterial-blight` (mint) beside `bacterial-blights` (3 holders).** Not a singular/plural split.
  The plural is plural because it names TWO organisms, *Xanthomonas campestris* pv. *phaseoli* and
  *Pseudomonas syringae* pv. *phaseolicola*, on *Phaseolus* beans. Edamame's is one organism,
  *Pseudomonas savastanoi* pv. *glycinea*, on *Glycine max*. Different disease, different id.
* **`cucumber-mosaic-virus` (mint) beside `cucumber-mosaic` (calendula).** calendula's record is
  "Cucumber mosaic **and aster yellows**" -- a virus and a leafhopper-vectored phytoplasma under one
  id. english-cucumber's problem is the single virus. Since an id is the join key a
  `varieties[].resistance` grade hangs off, merging them would assert that resistance to CMV is
  resistance to aster yellows.

`check_scope_variant_ids_not_merged` pins both, anchored on the ORGANISM and the compound scope
rather than on the id strings, so it fails loudly if the reason ever stops being true rather than
quietly passing on a name match. These two are the opposite of the singular/plural class: there the
two ids name the SAME problem, here the shorter id names a WIDER one.

REFUSALS: base SHA mismatch; a target already laddered; a full-schema field missing; a note field
PRESENT; `severity` present or absent against its pinned per-crop shape; a pre-state type that
breaks the split rule; an id off the convention table; any refused id; a reuse resolving nowhere or
losing its anchor; a new id already taken; a scope-variant merge; a singular minority variant; a
template twin diverging outside the pin; a rung note echoing shipped prose; a temperature figure or
ladder vocabulary; a material outside MATERIAL_OK; unknown method; tier decrease; applies_to
incoherence; identical registers; duplicate method; empty ladder; counts off; ANY change to
control_methods, source_catalog, or a bystander.

Guard suite:      tools/test_promote_pla8_batch22.py
Mutation harness: tools/mutate_pla8_batch22_suite.py (PLA-215)
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch22_stragglers")
BASE_SHA = "fabdaae1d3c35d54ccc49704253b5eb4e191700897786c1ec761e340166b5cb6"

CROPS = ("english-cucumber", "edamame", "pumpkin")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")

# The FULL schema. Every one must be present and non-empty on every pre-state problem.
FULL_SCHEMA_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                      "organic_treatment_beginner", "organic_treatment_seasoned",
                      "prevention_beginner", "prevention_seasoned")
# The eight fields a template-twin comparison is made over. Provenance (`sources`,
# `anchoring_urls`) is deliberately excluded: a divergence there is a sourcing defect to log, not a
# reason to demand two ladders match.
PROSE_FIELDS = FULL_SCHEMA_FIELDS
# Must be ABSENT. Their presence means these records were converted to the companion note schema
# and this promote's premise no longer describes them.
NOTE_FIELDS = ("note_beginner", "note_seasoned")

# The type rule, split by crop. Measured; do not inherit it into batch 23.
SET_FROM_NOTHING = ("english-cucumber", "pumpkin")
UPGRADE_FROM_COARSE = ("edamame",)
COARSE_TYPES = ("pest", "disease")
# `severity` is present on edamame's problems and absent on the other two crops'. Pinned so that a
# schema drift on either side is visible rather than silent.
SEVERITY_PRESENT = ("edamame",)

EXPECTED_PROBLEMS = {"english-cucumber": 9, "edamame": 9, "pumpkin": 8}
EXPECTED_RUNGS = {"english-cucumber": 50, "edamame": 43, "pumpkin": 42}
TOTAL_RUNGS = 135

# Keyed by (crop, name): "Downy mildew" is on all three crops, "Aphids" and "Cucumber beetles" on
# two. Batch 21 keyed on the name alone, which cannot express this batch.
ID_CONVENTION = {
    ("english-cucumber", "Two-spotted spider mites"): "two-spotted-spider-mite",
    ("english-cucumber", "Aphids"): "aphids",
    ("english-cucumber", "Whiteflies"): "whiteflies",
    ("english-cucumber", "Cucumber beetles"): "cucumber-beetles",
    ("english-cucumber", "Powdery mildew"): "powdery-mildew",
    ("english-cucumber", "Downy mildew"): "downy-mildew",
    ("english-cucumber", "Gummy stem blight"): "gummy-stem-blight",
    ("english-cucumber", "Gray mold"): "gray-mold",
    ("english-cucumber", "Cucumber mosaic virus"): "cucumber-mosaic-virus",
    ("edamame", "Bean leaf beetle"): "bean-leaf-beetle",
    ("edamame", "Stink bugs"): "stink-bugs",
    ("edamame", "Soybean aphid"): "soybean-aphid",
    ("edamame", "Japanese beetle"): "japanese-beetles",
    ("edamame", "Two-spotted spider mite"): "two-spotted-spider-mite",
    ("edamame", "White mold (Sclerotinia stem rot)"): "white-mold",
    ("edamame", "Bacterial blight"): "bacterial-blight",
    ("edamame", "Downy mildew"): "downy-mildew",
    ("edamame", "Soybean cyst nematode"): "soybean-cyst-nematode",
    ("pumpkin", "Squash vine borer"): "squash-vine-borer",
    ("pumpkin", "Squash bug"): "squash-bug",
    ("pumpkin", "Cucumber beetles"): "cucumber-beetles",
    ("pumpkin", "Aphids"): "aphids",
    ("pumpkin", "Powdery mildew"): "powdery-mildew",
    ("pumpkin", "Downy mildew"): "downy-mildew",
    ("pumpkin", "Bacterial wilt"): "bacterial-wilt",
    ("pumpkin", "Phytophthora blight"): "phytophthora-blight",
}

EXPECTED_TYPES = {
    ("english-cucumber", "two-spotted-spider-mite"): "mite",
    ("english-cucumber", "aphids"): "insect",
    ("english-cucumber", "whiteflies"): "insect",
    ("english-cucumber", "cucumber-beetles"): "insect",
    ("english-cucumber", "powdery-mildew"): "fungal",
    ("english-cucumber", "downy-mildew"): "fungal",
    ("english-cucumber", "gummy-stem-blight"): "fungal",
    ("english-cucumber", "gray-mold"): "fungal",
    ("english-cucumber", "cucumber-mosaic-virus"): "viral",
    ("edamame", "bean-leaf-beetle"): "insect",
    ("edamame", "stink-bugs"): "insect",
    ("edamame", "soybean-aphid"): "insect",
    ("edamame", "japanese-beetles"): "insect",
    ("edamame", "two-spotted-spider-mite"): "mite",
    ("edamame", "white-mold"): "fungal",
    ("edamame", "bacterial-blight"): "bacterial",
    ("edamame", "downy-mildew"): "fungal",
    ("edamame", "soybean-cyst-nematode"): "nematode",
    ("pumpkin", "squash-vine-borer"): "insect",
    ("pumpkin", "squash-bug"): "insect",
    ("pumpkin", "cucumber-beetles"): "insect",
    ("pumpkin", "aphids"): "insect",
    ("pumpkin", "powdery-mildew"): "fungal",
    ("pumpkin", "downy-mildew"): "fungal",
    ("pumpkin", "bacterial-wilt"): "bacterial",
    ("pumpkin", "phytophthora-blight"): "fungal",
}

REUSED_IDS = {   # id -> a crop that must still hold it off-batch
    "aphids": "acorn-squash", "bacterial-wilt": "acorn-squash", "bean-leaf-beetle": "dry-bean",
    "cucumber-beetles": "acorn-squash", "downy-mildew": "acorn-squash", "gray-mold": "chamomile",
    "gummy-stem-blight": "cantaloupe", "japanese-beetles": "blackberry",
    "phytophthora-blight": "banana-pepper", "powdery-mildew": "acorn-squash",
    "squash-bug": "acorn-squash", "squash-vine-borer": "acorn-squash", "stink-bugs": "blackberry",
    "two-spotted-spider-mite": "dry-bean", "white-mold": "dry-bean", "whiteflies": "calendula",
}
NEW_IDS = ("bacterial-blight", "cucumber-mosaic-virus", "soybean-aphid", "soybean-cyst-nematode")

REFUSED_IDS = {
    "bacterial-blights": "TWO Phaseolus organisms (Xanthomonas ... phaseoli and Pseudomonas "
                         "syringae pv. phaseolicola); edamame's is Pseudomonas savastanoi pv. "
                         "glycinea alone",
    "cucumber-mosaic": "calendula's COMPOUND record, cucumber mosaic AND aster yellows phytoplasma",
    "southern-bacterial-wilt": "Ralstonia, soilborne; pumpkin's is the beetle-gut Erwinia",
    "spider-mites": "the generic complex; both records name Tetranychus urticae outright",
    "aphid-borne-viruses": "sunflower's generic virus complex; this one is a named single virus",
    "botrytis-gray-mold": "artichoke's MINORITY variant of the same organism; the majority id "
                          "gray-mold has 5 holders",
    "cutworm": "the SINGULAR minority variant (1 holder); the plural has 8",
    "flea-beetle": "the SINGULAR minority variant (1 holder); the plural has 31",
    "japanese-beetle": "the SINGULAR minority variant (1 holder); the plural has 6",
}

# The three live singular/plural splits, carried from batch 21. Each has exactly ONE crop on the
# singular. Retire this guard in the same change that repoints them.
SINGULAR_PLURAL_PAIRS = (("cutworm", "cutworms"), ("flea-beetle", "flea-beetles"),
                         ("japanese-beetle", "japanese-beetles"))

# Scope-variant adjudications: a SHORTER roster id that names a WIDER problem than the mint beside
# it. Pinned on the SCOPE DIFFERENCE, not on the id strings: `wider_marker` is the extra pathogen
# the shorter id covers, and it must appear in every holder's record and appear in NEITHER the batch
# record; `own_marker` is the organism the batch record names on its own. If any of that stops being
# true the ruling is stale and the guard refuses instead of passing on a name match.
SCOPE_VARIANTS = (
    # (mint, shorter id, its holders, wider_marker, batch record, own_marker)
    ("bacterial-blight", "bacterial-blights", ("dry-bean", "green-beans-bush", "pole-beans"),
     "phaseolicola", ("edamame", "Bacterial blight"), "glycinea"),
    ("cucumber-mosaic-virus", "cucumber-mosaic", ("calendula",),
     "aster yellows", ("english-cucumber", "Cucumber mosaic virus"), "cucumber mosaic virus"),
)

# The ONE adjudicated template-twin divergence. Shared prose says "avoid working among wet vines";
# `wet_foliage_discipline` is exactly that action and the three squashes lack the rung.
TEMPLATE_DIVERGENCE_PINS = {
    ("pumpkin", "downy-mildew"): (("wet_foliage_discipline",), ()),
}

MATERIAL_OK = {
    ("edamame", "bean-leaf-beetle"): ("spinosad",),
    ("edamame", "soybean-aphid"): ("insecticidal_soap",),
    ("edamame", "stink-bugs"): ("pyrethrin",),
    ("edamame", "two-spotted-spider-mite"): ("insecticidal_soap", "horticultural_oil"),
    ("english-cucumber", "aphids"): ("insecticidal_soap", "horticultural_oil"),
    ("english-cucumber", "downy-mildew"): ("copper_fungicide",),
    ("english-cucumber", "powdery-mildew"): ("sulfur",),
    ("english-cucumber", "two-spotted-spider-mite"): ("insecticidal_soap", "horticultural_oil"),
    ("english-cucumber", "whiteflies"): ("insecticidal_soap", "horticultural_oil"),
    ("pumpkin", "aphids"): ("insecticidal_soap", "horticultural_oil"),
    ("pumpkin", "powdery-mildew"): ("sulfur",),
    ("pumpkin", "squash-bug"): ("insecticidal_soap",),
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


def find_problem(data, slug, name):
    for c in data["crops"]:
        if c["slug"] != slug:
            continue
        for _f, p in problems(c):
            if p.get("name") == name:
                return p
    return None


def sentences(text):
    return [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 40]


def shipped_rung_prose(data):
    """Every rung note already on the roster, whole and by sentence, excluding the batch crops."""
    whole, sent = {}, {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = r.get(k)
                    if not v:
                        continue
                    whole.setdefault(v.strip().lower(), "%s/%s/%s" % (c["slug"], p.get("id"),
                                                                      r["method"]))
                    for s in sentences(v):
                        sent.setdefault(s, "%s/%s/%s" % (c["slug"], p.get("id"), r["method"]))
    return whole, sent


def prose_key(p):
    return tuple((f, p.get(f)) for f in PROSE_FIELDS)


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# ------------------------------------------------------------------ pre-state checks
def check_full_schema_premise(by):
    """Asserted in BOTH directions. These are full-schema records: every prose field must be there,
    and the companion note pair must NOT be, so a later conversion refuses instead of validating
    prose this promote was not written against."""
    seen = 0
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: %s not on the roster" % c)
        for _f, p in problems(by[c]):
            if p.get("control_ladder"):
                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))
            for f in FULL_SCHEMA_FIELDS:
                if not str(p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%s has no %s; the full-schema premise has drifted "
                                     "and every prose comparison below would be vacuous"
                                     % (c, p.get("name"), f))
            for f in NOTE_FIELDS:
                if f in p:
                    raise SystemExit("REFUSED: %s/%s carries %r. These records were full-schema when "
                                     "this promote was written; if they have been converted to the "
                                     "companion note shape, the premise is wrong and the authoring "
                                     "must be redone against the new prose." % (c, p.get("name"), f))
            for f in ("sources", "anchoring_urls"):
                if not p.get(f):
                    raise SystemExit("REFUSED: %s/%s has no %s; these records are sourced and the "
                                     "premise says so" % (c, p.get("name"), f))
            has = "severity" in p
            want = c in SEVERITY_PRESENT
            if has != want:
                raise SystemExit("REFUSED: %s/%s severity present=%s, pinned %s. The per-crop "
                                 "schema shape has drifted." % (c, p.get("name"), has, want))
            seen += 1
    if seen != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: premise check covered %d problems, expected %d"
                         % (seen, sum(EXPECTED_PROBLEMS.values())))


def check_type_split_by_crop(batch, by):
    """The fifth type rule in six batches, and the first that is two-sided WITHIN one batch:
    english-cucumber and pumpkin are set from nothing, edamame is upgraded from coarse."""
    if set(SET_FROM_NOTHING) | set(UPGRADE_FROM_COARSE) != set(CROPS):
        raise SystemExit("REFUSED: the type rule does not cover every crop in the batch")
    set_n = upgraded = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                pre = p.get("type")
                if c in SET_FROM_NOTHING:
                    if pre is not None:
                        raise SystemExit("REFUSED: %s/%s pre-state already has type %r; this crop "
                                         "is on the set-from-nothing side"
                                         % (c, p.get("name"), pre))
                    set_n += 1
                else:
                    if pre not in COARSE_TYPES:
                        raise SystemExit("REFUSED: %s/%s pre-state type %r is not coarse; this crop "
                                         "is on the upgrade side" % (c, p.get("name"), pre))
                    want_coarse = "pest" if field == "pests" else "disease"
                    if pre != want_coarse:
                        raise SystemExit("REFUSED: %s/%s in %s carries coarse type %r, expected %r"
                                         % (c, p.get("name"), field, pre, want_coarse))
                    upgraded += 1
                post = o.get("type")
                if post not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s post type %r is not a fine type"
                                     % (c, p.get("name"), post))
                want = EXPECTED_TYPES.get((c, o.get("id")))
                if want is None:
                    raise SystemExit("REFUSED: %s/%s not in EXPECTED_TYPES" % (c, o.get("id")))
                if post != want:
                    raise SystemExit("REFUSED: %s/%s type %r != pinned %r"
                                     % (c, o.get("id"), post, want))
    want_set = sum(EXPECTED_PROBLEMS[c] for c in SET_FROM_NOTHING)
    want_up = sum(EXPECTED_PROBLEMS[c] for c in UPGRADE_FROM_COARSE)
    if (set_n, upgraded) != (want_set, want_up):
        raise SystemExit("REFUSED: type split covered %d set / %d upgraded, expected %d / %d"
                         % (set_n, upgraded, want_set, want_up))


def check_ids(batch, by, data):
    existing = roster_ids(data, exclude=CROPS)
    for c in CROPS:
        for field in ("pests", "diseases"):
            names = [p.get("name") for p in by[c].get(field) or []]
            got = [p.get("id") for p in batch[c].get(field) or []]
            if len(names) != len(got):
                raise SystemExit("REFUSED: %s/%s arity %d != %d" % (c, field, len(got), len(names)))
            for n, i in zip(names, got):
                want = ID_CONVENTION.get((c, n))
                if want is None:
                    raise SystemExit("REFUSED: (%s, %r) not in ID_CONVENTION" % (c, n))
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
    taken = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    if taken != set(REUSED_IDS) | set(NEW_IDS):
        raise SystemExit("REFUSED: the batch takes %r, pinned %r"
                         % (sorted(taken), sorted(set(REUSED_IDS) | set(NEW_IDS))))


def check_singular_variants_not_taken(batch, data):
    """Carried from batch 21. THREE singular/plural splits are live, each with exactly ONE crop on
    the singular. This batch takes the plural. Retire alongside the repoints."""
    off = roster_ids(data, exclude=CROPS)
    live = 0
    for sing, plur in SINGULAR_PLURAL_PAIRS:
        s, p = off.get(sing) or set(), off.get(plur) or set()
        if s and p:
            live += 1
            if len(s) >= len(p):
                raise SystemExit("REFUSED: %r now has %d holders against %r's %d. This batch takes "
                                 "the plural because it was the majority; re-measure before "
                                 "trusting that." % (sing, len(s), plur, len(p)))
    if live != len(SINGULAR_PLURAL_PAIRS):
        raise SystemExit("REFUSED: %d of %d singular/plural splits are still live. A partial repair "
                         "is a change to the fact base this guard encodes; re-measure and either "
                         "narrow the table or retire the guard deliberately."
                         % (live, len(SINGULAR_PLURAL_PAIRS)))
    taken = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    for sing, _plur in SINGULAR_PLURAL_PAIRS:
        if sing in taken:
            raise SystemExit("REFUSED: the batch took the singular %r, widening a known split" % sing)


def check_scope_variant_ids_not_merged(batch, data):
    """Two mints sit beside a SHORTER roster id that names a WIDER problem. Pinned on the organism
    and the compound scope rather than on the id strings, so this fails loudly if the reason stops
    being true instead of quietly passing on a name match."""
    off = roster_ids(data, exclude=CROPS)
    taken = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    checked = 0
    for mint, shorter, holders, wider_marker, batch_key, own_marker in SCOPE_VARIANTS:
        # ORDER MATTERS. Taking the wider id is the failure this guard exists for, and swapping a
        # mint for it also empties `taken` of the mint -- so the staleness branch below would mask
        # it and report the wrong reason. The most serious refusal is tested first.
        if shorter in taken:
            raise SystemExit("REFUSED: the batch took %r, merging a single-pathogen problem into a "
                             "wider-scope id that a resistance grade would then mis-assert"
                             % shorter)
        if mint not in taken:
            raise SystemExit("REFUSED: the batch no longer mints %r; this adjudication is stale"
                             % mint)
        if shorter not in off:
            raise SystemExit("REFUSED: %r is gone from the roster. It was the WIDER-scope id this "
                             "mint was distinguished from; re-adjudicate rather than assuming the "
                             "mint is still right." % shorter)
        if set(off[shorter]) != set(holders):
            raise SystemExit("REFUSED: %r is held by %r, pinned %r. Its scope may have changed."
                             % (shorter, sorted(off[shorter]), sorted(holders)))
        for h in holders:
            blob = ""
            for c in data["crops"]:
                if c["slug"] != h:
                    continue
                for _f, p in problems(c):
                    if p.get("id") == shorter:
                        blob = " ".join(str(p.get(k) or "") for k in
                                        FULL_SCHEMA_FIELDS + NOTE_FIELDS)
            if wider_marker.lower() not in blob.lower():
                raise SystemExit("REFUSED: %s/%s no longer names %r. That extra pathogen is WHY "
                                 "this id was ruled a WIDER problem than %r."
                                 % (h, shorter, wider_marker, mint))
        src = find_problem(data, batch_key[0], batch_key[1])
        if src is None:
            raise SystemExit("REFUSED: %s/%r is gone; the mint %r has no record to justify it"
                             % (batch_key[0], batch_key[1], mint))
        blob = " ".join(str(src.get(k) or "") for k in FULL_SCHEMA_FIELDS)
        if own_marker.lower() not in blob.lower():
            raise SystemExit("REFUSED: %s/%r no longer names %r, which is the ground for minting "
                             "%r rather than reusing %r"
                             % (batch_key[0], batch_key[1], own_marker, mint, shorter))
        if wider_marker.lower() in blob.lower():
            raise SystemExit("REFUSED: %s/%r now ALSO names %r, so it covers the same ground as %r "
                             "and the two ids can no longer be told apart by scope. Re-adjudicate."
                             % (batch_key[0], batch_key[1], wider_marker, shorter))
        checked += 1
    # `checked != len(SCOPE_VARIANTS)` ALONE is vacuous on an empty table (0 != 0 is False), which
    # is the computed-expectation trap. The count of adjudications is itself pinned.
    if not SCOPE_VARIANTS or checked != len(SCOPE_VARIANTS) or checked != 2:
        raise SystemExit("REFUSED: scope-variant check covered %d of %d adjudications, expected 2"
                         % (checked, len(SCOPE_VARIANTS)))


def check_template_sibling_divergence(batch, data):
    """THE guard this batch's measurement selected, and the batch 3 defect made mechanical.

    These three crops are TEMPLATE SIBLINGS of already-laddered crops: 9 of their problems carry
    source prose byte-identical to a shipped sibling's. Where the prose is the same, the ladder
    built from it must be the same, because there is nothing else for a difference to come from.
    The single adjudicated exception is pinned."""
    twins = pinned_hit = 0
    shipped = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if p.get("control_ladder"):
                shipped.setdefault(p["id"], []).append((c["slug"], p))
    by = by_slug(data)
    for c in CROPS:
        for field in ("pests", "diseases"):
            for src, out in zip(by[c].get(field) or [], batch[c].get(field) or []):
                mine = tuple(r["method"] for r in out.get("control_ladder") or [])
                for s, q in shipped.get(out["id"], []):
                    if prose_key(src) != prose_key(q):
                        continue
                    twins += 1
                    sib = tuple(r["method"] for r in q["control_ladder"])
                    if sib == mine:
                        continue
                    pin = TEMPLATE_DIVERGENCE_PINS.get((c, out["id"]))
                    if pin is None:
                        raise SystemExit(
                            "REFUSED: %s/%s shares byte-identical source prose with %s but builds a "
                            "different ladder (%r vs %r). Identical prose cannot support two "
                            "ladders; either the divergence is a defect or it is an adjudicated "
                            "exception that must be pinned." % (c, out["id"], s, list(mine),
                                                                list(sib)))
                    extra = tuple(m for m in mine if m not in sib)
                    miss = tuple(m for m in sib if m not in mine)
                    if (extra, miss) != pin:
                        raise SystemExit(
                            "REFUSED: %s/%s diverges from %s by +%r -%r, pinned +%r -%r"
                            % (c, out["id"], s, list(extra), list(miss), list(pin[0]),
                               list(pin[1])))
                    pinned_hit += 1
    if twins == 0:
        raise SystemExit("REFUSED: no template twins found; this guard would be vacuous. These "
                         "crops are siblings of laddered crops and 9 twins were measured.")
    if pinned_hit == 0:
        raise SystemExit("REFUSED: the pinned divergence never fired. Either it has been silently "
                         "resolved or the twin detection has stopped reaching it.")


def check_no_shipped_prose_echo(batch, data):
    """Carried from batch 21 and re-measured: 0 whole echoes and 0 sentence echoes over 270 batch
    notes against a 5,351-note corpus. Worth most where ladders converge -- identical shape with
    independent prose is convergent authoring, identical prose is copying."""
    whole, sent = shipped_rung_prose(data)
    checked = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = (r.get(k) or "").strip().lower()
                    checked += 1
                    if v in whole:
                        raise SystemExit("REFUSED: %s/%s/%s %s is a verbatim echo of %s"
                                         % (c, p["id"], r["method"], k, whole[v]))
                    for s in sentences(r.get(k) or ""):
                        if s in sent:
                            raise SystemExit("REFUSED: %s/%s/%s %s echoes a shipped sentence from "
                                             "%s: %r" % (c, p["id"], r["method"], k, sent[s], s[:70]))
    if not whole:
        raise SystemExit("REFUSED: no shipped rung prose found; this guard would be vacuous")
    if checked == 0:
        raise SystemExit("REFUSED: no batch notes scanned; this guard would be vacuous")


def check_no_temperature_figures(batch):
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    seen += 1
                    m = TEMP_FIGURE.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s states a temperature (%r)"
                                         % (c, p["id"], r["method"], f, m.group(0)))
    if seen == 0:
        raise SystemExit("REFUSED: no notes scanned for temperatures; this guard would be vacuous")


def check_no_ladder_vocabulary(batch):
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    seen += 1
                    m = LADDER_VOCAB.search(r[f])
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s uses internal vocabulary (%r)"
                                         % (c, p["id"], r["method"], f, m.group(0)))
    if seen == 0:
        raise SystemExit("REFUSED: no notes scanned for vocabulary; this guard would be vacuous")


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
                if set(r) != {"method", "note_beginner", "note_seasoned"}:
                    raise SystemExit("REFUSED: %s/%s/%s rung carries %r, expected exactly "
                                     "method + the note pair" % (c, p["id"], m, sorted(r)))
                if cm[m]["tier"] in MATERIAL_TIERS:
                    ok = MATERIAL_OK.get((c, p["id"]), ())
                    if m not in ok:
                        raise SystemExit("REFUSED: %s/%s material rung %r outside MATERIAL_OK %r; "
                                         "this batch scopes every material to the record that "
                                         "names it" % (c, p["id"], m, ok))
        if n != EXPECTED_RUNGS[c]:
            raise SystemExit("REFUSED: %s has %d rungs, expected %d" % (c, n, EXPECTED_RUNGS[c]))
    if rung_count(batch) != TOTAL_RUNGS:
        raise SystemExit("REFUSED: %d rungs total, expected %d" % (rung_count(batch), TOTAL_RUNGS))


def check(data):
    by = by_slug(data)
    batch = staged()
    cm = data["control_methods"]
    check_full_schema_premise(by)
    check_type_split_by_crop(batch, by)
    check_ids(batch, by, data)
    check_singular_variants_not_taken(batch, data)
    check_scope_variant_ids_not_merged(batch, data)
    check_template_sibling_divergence(batch, data)
    check_no_shipped_prose_echo(batch, data)
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
