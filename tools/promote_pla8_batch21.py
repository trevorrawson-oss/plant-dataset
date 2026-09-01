#!/usr/bin/env python3
"""PLA-8 BATCH 21 -- FLOWERS & EDIBLE FLOWERS: nasturtium, sunflower, viola.
Base 5409c0ce (batch 20, berries).

26 problems gain `id`, a `type` and a `control_ladder`; **64 rungs**. Roster laddered 88 -> 91.
NO catalog mutation.

--------------------------------------------------------------------------------------------------
THESE ARE NOTE-SCHEMA CROPS. THE PREMISE IS DIFFERENT FROM BATCHES 17-20.
--------------------------------------------------------------------------------------------------
Each problem carries ONLY `name`, `audience`, `severity`, `note_beginner`, `note_seasoned`. There is
no `symptoms_*`, `cause_*`, `organic_treatment_*` or `prevention_*`, and no `sources` or
`anchoring_urls`. That is the companion-flower schema of batches 15 and 16.

**Copying batch 20's promote would have refused this entire batch on its premise check.** The
premise is asserted in BOTH directions: the note pair must be present, and the full-schema fields
must be ABSENT, so a later conversion of these records to the full schema refuses rather than
validating the wrong prose.

Ladders are correspondingly SHORT (64 rungs over 26 problems, against 140 over 39 in batch 20).
Two notes is the whole evidence base; that is the source, not thin authoring.

--------------------------------------------------------------------------------------------------
THE GUARD SHAPE WAS CHOSEN BY MEASUREMENT, NOT INHERITED
--------------------------------------------------------------------------------------------------
Batch 20's headline was that an inherited guard is an assumption. Measured here BEFORE writing:

* **9 of 20 reused-id instances EXACTLY MATCH a shipped ladder** and 11 diverge. Both are correct:
  a generic aphid ladder on a companion flower converges with marigold, borage and calendula because
  the pest and the controls really are generic. So a batch-20-style "every divergence must be
  pinned" guard would be 11 pins of pure noise, and a "must match" guard would be wrong 11 times.
  **Shape comparison is the wrong check for this batch and is not used.**
* The real hazard when ladders converge is an author COPYING a sibling's prose rather than writing
  from the note. So `check_no_shipped_prose_echo` is the guard that earns its place here: identical
  method sequence with independent prose is convergent authoring; identical prose is copying.

--------------------------------------------------------------------------------------------------
THE COMPANION INVERSION, CARRIED FROM BATCHES 15 AND 16
--------------------------------------------------------------------------------------------------
On a companion planting a "pest" can be the POINT of the plant, and nasturtium is the roster's
sharpest case: its own aphid note says gardeners grow it as an aphid trap. `trap_cropping` is
forbidden batch-wide and trap/decoy vocabulary is banned from every rung note, so unplaced trap
content cannot creep back through prose. The trap-stand tending and siting advice is deliberately
UNPLACED: it concerns the trap USE, which is why you grow the plant, not a control of its own
problem.

--------------------------------------------------------------------------------------------------
`bt` IS SCOPED BY CROP, AND THE REASON IS THE CATALOG'S OWN CAUTION
--------------------------------------------------------------------------------------------------
The catalog says: "Bt kurstaki kills the caterpillars of moths and butterflies as a group, including
desirable species such as swallowtails and monarchs; spray only plants with a pest problem, **never
butterfly host plants**."

* **nasturtium/cabbageworms KEEPS its bt rung.** The target is *Pieris rapae*, the introduced cabbage
  white, and all SIX brassicas carrying this same id ship the same bt rung. This is the caution's own
  permitted case: a plant with a pest problem.
* **viola/caterpillars had its bt rung REMOVED at the read.** Viola is a fritillary host, and the
  pest larvae and the desirable native larvae are the same caterpillars on the same leaves. The
  authored rung tried to condition its way out ("leave native fritillary larvae unsprayed"), but Bt
  cannot sort them, so the instruction was not followable. An incoherent recommendation on a plant
  the caution explicitly excludes. The ladder is now `handpick` alone, which is what the note asks
  for, because handpicking CAN sort them.

`check_bt_is_scoped` pins both halves, so neither the removal nor the retention can be quietly
reversed. Viola's own note still recommends Bt, which is FILED as a prose defect.

REFUSALS: base SHA mismatch; a target already laddered; the note pair missing; a full-schema field
PRESENT; a pre-state type present; an id off the convention table; any refused id; a reuse resolving
nowhere or losing its anchor; a new id already taken; `trap_cropping` anywhere; trap/decoy vocabulary
in any note; a bt rung outside its pinned home; a rung note echoing shipped prose; a temperature
figure or ladder vocabulary; a material outside MATERIAL_OK; unknown method; tier decrease;
applies_to incoherence; identical registers; duplicate method; empty ladder; counts off; ANY change
to control_methods, source_catalog, or a bystander.

Guard suite:      tools/test_promote_pla8_batch21.py
Mutation harness: tools/mutate_pla8_batch21_suite.py (PLA-215)
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch21_flowers")
BASE_SHA = "5409c0ce32a87c04d92724aedae17b902a572ab14c01847980078ac158521441"

CROPS = ("nasturtium", "sunflower", "viola")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
NOTE_FIELDS = ("note_beginner", "note_seasoned")
# Fields that must be ABSENT. Their presence means these records were converted to the full schema
# and this promote's premise no longer describes them.
FULL_SCHEMA_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                      "organic_treatment_beginner", "organic_treatment_seasoned",
                      "prevention_beginner", "prevention_seasoned")

EXPECTED_PROBLEMS = {"nasturtium": 8, "sunflower": 9, "viola": 9}
EXPECTED_RUNGS = {"nasturtium": 16, "sunflower": 25, "viola": 23}
TOTAL_RUNGS = 64

ID_CONVENTION = {
    "Aphids": "aphids",
    "Cabbage white caterpillars (imported cabbageworm)": "cabbageworms",
    "Flea beetles": "flea-beetles",
    "Slugs and snails": "slugs-and-snails",
    "Whiteflies and spider mites": "whiteflies",
    "Mosaic and aphid-borne viruses": "aphid-borne-viruses",
    "Bacterial wilt": "southern-bacterial-wilt",
    "Aster yellows": "aster-yellows",
    "Birds and squirrels": "birds-and-squirrels",
    "Sunflower moth and head-clipping weevil": "sunflower-head-insects",
    "Cutworms": "cutworms",
    "Leaf-feeding caterpillars and beetles": "sunflower-defoliators",
    "Sclerotinia (white mold) head and stalk rot": "white-mold",
    "Downy mildew": "downy-mildew",
    "Rust": "sunflower-rust",
    "Septoria leaf spot and powdery mildew": "sunflower-foliar-diseases",
    "Spider mites": "spider-mites",
    "Foliage-feeding caterpillars": "caterpillars",
    "Crown and root rot": "crown-and-root-rot",
    "Powdery mildew": "powdery-mildew",
    "Leaf spots and anthracnose": "viola-leaf-spots",
    "Gray mold (Botrytis blight)": "gray-mold",
}

REUSED_IDS = {
    "aphids": "marigold", "cabbageworms": "cabbage", "flea-beetles": "arugula",
    "slugs-and-snails": "marigold", "whiteflies": "calendula",
    "southern-bacterial-wilt": "eggplant", "aster-yellows": "cosmos",
    "birds-and-squirrels": "fig", "cutworms": "artichoke", "white-mold": "dry-bean",
    "downy-mildew": "sweet-alyssum", "spider-mites": "zinnia", "caterpillars": "sweet-pea",
    "crown-and-root-rot": "parsley", "powdery-mildew": "apple", "gray-mold": "chamomile",
}
NEW_IDS = ("aphid-borne-viruses", "sunflower-head-insects", "sunflower-defoliators",
           "sunflower-rust", "sunflower-foliar-diseases", "viola-leaf-spots")

REFUSED_IDS = {
    "bacterial-wilt": "the cucurbit Erwinia tracheiphila, beetle-vectored; nasturtium's is Ralstonia",
    "bee-balm-rust": "a CROP-SCOPED id for a different rust species",
    "septoria-leaf-spot": "Septoria lycopersici on tomatoes; sunflower's is S. helianthi",
    "anthracnose": "the vegetable Colletotrichum orbiculare generic",
    "cutworm": "the SINGULAR minority variant (1 holder); the plural has 8",
    "flea-beetle": "the SINGULAR minority variant (1 holder); the plural has 31",
    "japanese-beetle": "the SINGULAR minority variant (1 holder); the plural has 6",
    "trap-crop": "not an id; the trap USE is not a problem",
}

# THE COMPANION INVERSION. trap_cropping is the key that would encode the trap USE, which is why the
# plant is grown rather than a control of its own problem.
FORBIDDEN_METHODS = {
    "trap_cropping": "the companion inversion: the trap USE is why you grow nasturtium, not a "
                     "control of nasturtium's own aphid problem",
}
NOTE_BANNED = ("trap", "decoy")

# `bt` is scoped BY CROP, on the catalog's own caution. See the module docstring.
BT_ALLOWED = {("nasturtium", "cabbageworms")}
BT_FORBIDDEN_CROPS = {"viola": "a fritillary host; Bt cannot sort pest larvae from the native "
                               "butterfly larvae the plant is grown to support"}

MATERIAL_OK = {
    ("nasturtium", "aphids"): ("insecticidal_soap",),
    ("nasturtium", "slugs-and-snails"): ("iron_phosphate_slug_bait",),
    ("nasturtium", "whiteflies"): ("insecticidal_soap",),
    ("nasturtium", "cabbageworms"): ("bt",),
    ("sunflower", "aphids"): ("insecticidal_soap",),
    ("viola", "aphids"): ("insecticidal_soap",),
    ("viola", "slugs-and-snails"): ("iron_phosphate_slug_bait",),
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
                for k in NOTE_FIELDS:
                    v = r.get(k)
                    if not v:
                        continue
                    whole.setdefault(v.strip().lower(), "%s/%s/%s" % (c["slug"], p.get("id"),
                                                                      r["method"]))
                    for s in sentences(v):
                        sent.setdefault(s, "%s/%s/%s" % (c["slug"], p.get("id"), r["method"]))
    return whole, sent


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# ------------------------------------------------------------------ pre-state checks
def check_note_schema_premise(by):
    """Asserted in BOTH directions. These are companion-flower records: the note pair must be there,
    and the full-schema fields must NOT be, so a later conversion refuses instead of validating
    prose this promote was not written against."""
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: %s not on the roster" % c)
        for _f, p in problems(by[c]):
            if p.get("control_ladder"):
                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))
            for f in NOTE_FIELDS:
                if not str(p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%s has no %s; the note-schema premise has drifted "
                                     "and every prose comparison below would be vacuous"
                                     % (c, p.get("name"), f))
            for f in FULL_SCHEMA_FIELDS:
                if f in p:
                    raise SystemExit("REFUSED: %s/%s carries %r. These records were note-shaped when "
                                     "this promote was written; if they have been converted, the "
                                     "premise is wrong and the authoring must be redone against the "
                                     "new prose." % (c, p.get("name"), f))


def check_type_set_from_nothing(batch, by):
    checked = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            for p, o in zip(by[c].get(field) or [], batch[c].get(field) or []):
                if p.get("type") is not None:
                    raise SystemExit("REFUSED: %s/%s pre-state already has type %r"
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


def check_singular_variants_not_taken(batch, data):
    """THREE singular/plural splits are live, each with exactly ONE crop on the singular:
    cutworm(1)/cutworms(8), flea-beetle(1)/flea-beetles(31), japanese-beetle(1)/japanese-beetles(6).
    This batch takes the plural every time. Guarded because my own pin table got cutworm WRONG
    (it said reuse the singular, on the belief that the split did not exist yet)."""
    off = roster_ids(data, exclude=CROPS)
    pairs = (("cutworm", "cutworms"), ("flea-beetle", "flea-beetles"),
             ("japanese-beetle", "japanese-beetles"))
    live = 0
    for sing, plur in pairs:
        s, p = off.get(sing) or set(), off.get(plur) or set()
        if s and p:
            live += 1
            if len(s) >= len(p):
                raise SystemExit("REFUSED: %r now has %d holders against %r's %d. This batch takes "
                                 "the plural because it was the majority; re-measure before "
                                 "trusting that." % (sing, len(s), plur, len(p)))
    if live == 0:
        raise SystemExit("REFUSED: none of the singular/plural splits is live any more. If they have "
                         "been repointed, retire this guard deliberately rather than letting it pass.")
    taken = {p["id"] for c in CROPS for _f, p in problems(batch[c])}
    for sing, _plur in pairs:
        if sing in taken:
            raise SystemExit("REFUSED: the batch took the singular %r, widening a known split" % sing)


def check_inversion(batch, cm):
    """The companion inversion, carried from batches 15 and 16."""
    seen_notes = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            ms = [r["method"] for r in p.get("control_ladder") or []]
            for m, why in FORBIDDEN_METHODS.items():
                if m in ms:
                    raise SystemExit("REFUSED: %s/%s carries %r: %s" % (c, p["id"], m, why))
            for r in p.get("control_ladder") or []:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                seen_notes += 1
                for w in NOTE_BANNED:
                    if re.search(r"\b%s\w*\b" % w, blob):
                        raise SystemExit("REFUSED: %s/%s: a note uses %r. The inversion holds: "
                                         "unplaced trap content must not creep back through prose"
                                         % (c, p["id"], w))
    if "trap_cropping" not in cm:
        raise SystemExit("REFUSED: trap_cropping is not in the catalog, so forbidding it is vacuous")
    if seen_notes == 0:
        raise SystemExit("REFUSED: no rung notes scanned; this guard would be vacuous")


def check_bt_is_scoped(batch):
    """The catalog's own caution says never on butterfly host plants. nasturtium's target IS the
    pest butterfly's larvae and six brassicas ship the same rung; viola's pest and its desirable
    native fritillaries are the same caterpillars, so Bt cannot sort them."""
    found = set()
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if "bt" not in [r["method"] for r in p.get("control_ladder") or []]:
                continue
            key = (c, p["id"])
            if c in BT_FORBIDDEN_CROPS:
                raise SystemExit("REFUSED: %s/%s carries a bt rung. %s"
                                 % (c, p["id"], BT_FORBIDDEN_CROPS[c]))
            if key not in BT_ALLOWED:
                raise SystemExit("REFUSED: %s/%s carries an unpinned bt rung" % (c, p["id"]))
            found.add(key)
    if found != BT_ALLOWED:
        raise SystemExit("REFUSED: bt rungs are %r, pinned %r. The removal from viola and the "
                         "retention on nasturtium are BOTH rulings; neither may drift."
                         % (sorted(found), sorted(BT_ALLOWED)))


def check_no_shipped_prose_echo(batch, data):
    """THE guard this batch's measurement selected. 9 of 20 reused-id instances match a shipped
    ladder method-for-method, which is correct convergence on generic pests -- so shape comparison
    is meaningless here and the real hazard is an author copying a sibling's PROSE."""
    whole, sent = shipped_rung_prose(data)
    checked = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for k in NOTE_FIELDS:
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
                        raise SystemExit("REFUSED: %s/%s material rung %r outside MATERIAL_OK %r; "
                                         "this batch scopes every material to the note that names it"
                                         % (c, p["id"], m, ok))
        if n != EXPECTED_RUNGS[c]:
            raise SystemExit("REFUSED: %s has %d rungs, expected %d" % (c, n, EXPECTED_RUNGS[c]))
    if rung_count(batch) != TOTAL_RUNGS:
        raise SystemExit("REFUSED: %d rungs total, expected %d" % (rung_count(batch), TOTAL_RUNGS))


def check(data):
    by = by_slug(data)
    batch = staged()
    cm = data["control_methods"]
    check_note_schema_premise(by)
    check_type_set_from_nothing(batch, by)
    check_ids(batch, by, data)
    check_singular_variants_not_taken(batch, data)
    check_inversion(batch, cm)
    check_bt_is_scoped(batch)
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
