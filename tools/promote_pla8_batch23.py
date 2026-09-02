#!/usr/bin/env python3
"""PLA-8 BATCH 23 -- THE ROOTS: parsnip, potato, sweet-potato.
Base b118f19d (the thin-ladder backfill).

22 problems gain `id`, a fine `type` and a `control_ladder`; **87 rungs**. Roster laddered 94 -> 97.
NO catalog mutation.

The three crops share ZERO prose with each other, which is why the roots handoff measured a split
into two batches and rejected it: there is no read to amortize and a split only doubles the fixed
overhead.

--------------------------------------------------------------------------------------------------
THE PREMISE IS UNIFORM, AND IT WAS MEASURED RATHER THAN INHERITED FROM BATCH 22
--------------------------------------------------------------------------------------------------
**Schema: FULL** on all 22 (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`,
`sources`, `anchoring_urls`); the note pair is ABSENT. Asserted in both directions.

**Type: UNIFORMLY COARSE -> upgrade.** Every one of the 22 pre-state problems carries exactly
`pest` or `disease`, matching its array. Batch 17 was uniformly coarse, 18 mixed, 19 uniformly fine,
20 and 21 carried no type at all, 22 was split by crop; this is the seventh distinct situation in
seven batches, so it is measured every time. **`severity` is present on all 22** and pinned, because
batch 22 found that asymmetry only by measuring for it.

--------------------------------------------------------------------------------------------------
BATCH 22's DIVERGENCE GUARD IS DROPPED, AND ITS VACUITY IS ASSERTED RATHER THAN ASSUMED
--------------------------------------------------------------------------------------------------
`check_template_sibling_divergence` compares a batch problem whose eight prose fields are
byte-identical to a shipped sibling's. Batch 22 had **9** such template twins. Roots has **0**,
measured against all 94 laddered crops, so the guard would be vacuous and its own anti-vacuity
branch would refuse the batch.

Dropping a guard silently is how a premise stops being checked. `check_no_template_twins_premise`
therefore ASSERTS the zero: if a future roots problem ever acquires a byte-identical twin, this
promote refuses and says which guard has to come back.

--------------------------------------------------------------------------------------------------
THE GUARD THAT REPLACES IT WAS CHOSEN BY MEASURING, AND IT GUARDS THE RISK THIS SESSION CREATED
--------------------------------------------------------------------------------------------------
The copy vector here is NOT sibling-to-sibling. It is CROSS-CROP into a precedent crop: 13 of the 22
ids are REUSED from laddered crops, and each authoring agent was deliberately pointed at that
precedent crop as a shape exemplar (carrot, beet, the tomatoes, eggplant, radish, garlic, fig, okra).
The guard has to protect what the method exposed.

`check_no_precedent_copy` compares every authored rung against every roster rung sharing its
`(problem id, method)` and refuses at similarity **>= 0.70**. The threshold is measured, not chosen:

* Roster-wide comparison FLOODS -- 16,510 shared-(id,method) pairs, 434 byte-identical -- but every
  dense identical cluster is a legitimate PROPAGATION group (peppers, beans, melons, corns,
  brassicas). Byte-identical SOURCE prose is too strict a test for "propagated": the melon trio has
  slightly different source prose and 169 identical rungs anyway. This is exactly the roots
  handoff's warning that the exact-vs-diverging ratio does not pick the guard.
* Narrowed to roots' ACTUAL peers -- crops whose max prose-kinship to any other laddered crop is
  < 0.55, i.e. crops in no propagation group at all -- there are **62 shared-(id,method) rung
  pairs**, and their distribution is the empirical ceiling for independent authoring:
  **per-register max 0.684, median 0.409.** Nothing independent reaches 0.70. The top legitimate
  pair is apple vs strawberry on `powdery-mildew`/`sulfur`: two crops saying the same true thing
  about the same method in their own words.

THE METRIC ITSELF WAS WRONG ONCE, AND THE INDEPENDENT SOURCE-TRUTH PASS CAUGHT IT. The first
version used `difflib.SequenceMatcher` defaults and averaged the two registers. `autojunk` engages
at 200 characters and junks any character appearing in over 1% of the sequence, which describes
every seasoned register, so it deflated precisely the strings the guard exists to compare; the mean
then diluted one copied register against one independent register. Under that metric
`potato`/`common-scab`/`even_watering` scored 0.431 against beet and passed. It is a copy: its
seasoned register scores **0.757** with `autojunk=False`, and shares a 56-character verbatim run.
A guard can be reachable, non-vacuous, mutation-tested and still measure the wrong thing.

REACHABILITY IS MEASURED, because a guard that cannot fire is not coverage: the 13 reused ids carry
**388 existing rungs** to compare against (flea-beetles 109, damping-off 39, early-blight 39,
fusarium-wilt 30, late-blight 24, carrot-rust-fly 13, root-knot-nematode 8, aster-yellows 6,
colorado-potato-beetle 4, wireworms 3, common-scab 3, aster-leafhoppers 1). On the shipped batch it
makes **243 comparisons and tops out at 0.508**. The 9 MINTED ids have no precedent by construction
and are outside this guard's reach; that is a forward condition, documented, NOT padded into a total.

--------------------------------------------------------------------------------------------------
IDS: TWO KINGDOM-LEVEL TAXON COLLISIONS AND TWO SCOPE VARIANTS, ALL FOUND BY A STEMMED SCAN
--------------------------------------------------------------------------------------------------
Batch 21 earned "check every mint BY ID"; batch 22 followed it and still missed two, because an
exact-id check passes an id that merely RESEMBLES a live one. A stemmed token-subset scan over all
216 live ids was run BEFORE authoring, and an exact scan would have missed the first item below:

* `Leafminers` -> the exact scan reported NO live relative. False: `beet-spinach-leafminer`,
  `celery-leafminer`, `allium-leafminer` and `citrus-leafminer` all exist. Singular/plural defeated
  it. There is no bare `leafminer` id and all four live ones are crop-prefixed AND singular, so
  parsnip mints `parsnip-leafminer`. Its prose names no genus, so a genus-bearing id would overclaim.

TAXON COLLISIONS -- same words, different kingdom, both read from the crops' OWN prose:
* `sweet-potato-black-rot` NOT `black-rot`. Live `black-rot` (10 brassicas) is the BACTERIUM
  *Xanthomonas campestris* pv. *campestris*; sweet potato's is the FUNGUS *Ceratocystis fimbriata*.
  The roster even types them differently (bacterial vs fungal), which is the same collision's second
  face.
* `blackleg-bacterial-soft-rot` NOT `blackleg`. Live `blackleg` (cabbage, kohlrabi) is the FUNGUS
  *Phoma lingam*; potato's is BACTERIA in *Pectobacterium*.

SCOPE VARIANTS -- a shorter roster id would name a NARROWER problem:
* `aphids-virus-vectors` NOT `aphids` (x59, a feeding-pest entry). Potato's says outright "Virus
  pressure, not the feeding itself, is the main reason to manage them."
* `whiteflies-virus-vectors` NOT `whiteflies` (x5). Same shape, deliberately parallel.
* `wireworms-root-feeding-larvae` NOT `wireworms` (radish, click beetle larvae ALONE). Sweet
  potato's entry explicitly widens to a complex including *Diabrotica* and *Systena* larvae.

A TAXON CHECK THAT PASSED, and is pinned so it fails loudly if the reason stops being true:
* `common-scab` IS reused. beet's own prose says *Streptomyces scabies* is "the same organism that
  causes potato scab".

`check_stemmed_id_scan` pins each of these on the ORGANISM or the scope, not on the id string, so a
name match cannot quietly satisfy it.

--------------------------------------------------------------------------------------------------
TEMPERATURE FIGURES ARE WARRANTED, NOT BANNED
--------------------------------------------------------------------------------------------------
Batch 22 carried `check_no_temperature_figures`, a blanket refusal. Its three crops contained ZERO
temperature figures, so it was a refusal-spec pass there. Roots contains **5**, and every one is
sourced, so carrying the blanket ban would refuse verified content:

    parsnip/damping-off/sound_sowing_practice  50°F x2  <- the crop's own prose, "about 50°F"
    potato + sweet-potato /insecticidal_soap   90°F x3  <- the METHOD's own caution, "above 90°F"

`check_temperature_figures_warranted` replaces it: every figure must appear in that problem's own
source prose OR in that method's own catalog text. The expected count is pinned, so a figure that
disappears is as visible as one that appears. This is the backfill's `check_warrants` discipline --
restate-the-record made checkable -- rather than a ban that a real source defeats.

REFUSALS: base SHA mismatch; a target already laddered; a full-schema field missing; a note field
PRESENT; `severity` missing; a pre-state type that is not the coarse array default; an id off the
pin table; a taxon collision or scope variant merged; a template twin appearing; a rung within 0.70
of a precedent crop's rung; a rung note echoing shipped prose; an unwarranted temperature figure;
ladder vocabulary; unknown method; tier decrease; applies_to incoherence; identical registers;
duplicate method in a ladder; empty ladder; counts off; ANY change to control_methods,
source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch23.py
Mutation harness: tools/mutate_pla8_batch23_suite.py (PLA-215)
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch23_roots")
BASE_SHA = "b118f19d36d021db95d755225e566843676fe3fa393299f250a8d34bb9605710"

CROPS = ("parsnip", "potato", "sweet-potato")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")

FULL_SCHEMA_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                      "organic_treatment_beginner", "organic_treatment_seasoned",
                      "prevention_beginner", "prevention_seasoned")
PROSE_FIELDS = FULL_SCHEMA_FIELDS
NOTE_FIELDS = ("note_beginner", "note_seasoned", "note", "summary")

EXPECTED_PROBLEMS = {"parsnip": 6, "potato": 8, "sweet-potato": 8}
EXPECTED_RUNGS = {"parsnip": 21, "potato": 35, "sweet-potato": 31}
TOTAL_RUNGS = 87
PRECEDENT_COPY_THRESHOLD = 0.70
EXPECTED_TEMP_FIGURES = 5

# The pin table. `decision` is load-bearing: REUSE means the id already exists on the roster and the
# taxon was checked; MINT means it does not, for the stated reason.
ID_CONVENTION = {
    ("parsnip", "pests", 0): ("Carrot rust fly", "carrot-rust-fly", "insect", "REUSE"),
    ("parsnip", "pests", 1): ("Leafminers", "parsnip-leafminer", "insect", "MINT"),
    ("parsnip", "pests", 2): ("Aster leafhopper (aster yellows vector)", "aster-leafhoppers",
                              "insect", "REUSE"),
    ("parsnip", "diseases", 0): ("Itersonilia canker (parsnip canker)", "itersonilia-canker",
                                 "fungal", "MINT"),
    ("parsnip", "diseases", 1): ("Aster yellows", "aster-yellows", "bacterial", "REUSE"),
    ("parsnip", "diseases", 2): ("Damping-off", "damping-off", "fungal", "REUSE"),
    ("potato", "pests", 0): ("Colorado potato beetle", "colorado-potato-beetle", "insect", "REUSE"),
    ("potato", "pests", 1): ("Flea beetles", "flea-beetles", "insect", "REUSE"),
    ("potato", "pests", 2): ("Aphids and the viruses they spread", "aphids-virus-vectors",
                             "insect", "MINT"),
    ("potato", "pests", 3): ("Wireworms", "wireworms", "insect", "REUSE"),
    ("potato", "diseases", 0): ("Late blight", "late-blight", "fungal", "REUSE"),
    ("potato", "diseases", 1): ("Early blight", "early-blight", "fungal", "REUSE"),
    ("potato", "diseases", 2): ("Common scab", "common-scab", "bacterial", "REUSE"),
    ("potato", "diseases", 3): ("Blackleg and bacterial soft rot", "blackleg-bacterial-soft-rot",
                                "bacterial", "MINT"),
    ("sweet-potato", "pests", 0): ("Sweet potato weevil", "sweet-potato-weevil", "insect", "MINT"),
    ("sweet-potato", "pests", 1): ("Wireworms and root-feeding beetle larvae",
                                   "wireworms-root-feeding-larvae", "insect", "MINT"),
    ("sweet-potato", "pests", 2): ("Flea beetles", "flea-beetles", "insect", "REUSE"),
    ("sweet-potato", "pests", 3): ("Whiteflies and the viruses they spread",
                                   "whiteflies-virus-vectors", "insect", "MINT"),
    ("sweet-potato", "diseases", 0): ("Fusarium wilt (stem rot)", "fusarium-wilt", "fungal", "REUSE"),
    ("sweet-potato", "diseases", 1): ("Root-knot nematode", "root-knot-nematode", "nematode",
                                      "REUSE"),
    ("sweet-potato", "diseases", 2): ("Black rot", "sweet-potato-black-rot", "fungal", "MINT"),
    ("sweet-potato", "diseases", 3): ("Scurf and storage soft rot", "scurf-storage-soft-rot",
                                      "fungal", "MINT"),
}

# Each entry: the id this batch REFUSES to merge into, the live id it resembles, and the ORGANISM or
# SCOPE reason. Anchored on the reason, not the string, so it fails loudly if the reason dies.
ID_SCOPE_PINS = {
    "sweet-potato-black-rot": ("black-rot", "Ceratocystis fimbriata", "Xanthomonas"),
    "blackleg-bacterial-soft-rot": ("blackleg", "Pectobacterium", "Phoma lingam"),
    "aphids-virus-vectors": ("aphids", "Virus pressure, not the feeding itself", None),
    "whiteflies-virus-vectors": ("whiteflies", "Virus pressure, not the feeding itself", None),
    "wireworms-root-feeding-larvae": ("wireworms", "Diabrotica", None),
}
# A REUSE whose taxon check PASSED, pinned so it fails loudly if the stated reason stops being true.
TAXON_REUSE_PINS = {
    ("potato", "common-scab"): ("beet", "the same organism that causes potato scab"),
}

# Where the roster holds TWO stem-equal variants of one problem name, which one this batch takes is
# a decision, not a typing accident. Key: (id the batch takes, the live variant it does NOT take).
STEM_VARIANT_PINS = {
    ("flea-beetles", "flea-beetle"):
        "The batch takes the x32 majority id. swiss-chard's singular `flea-beetle` is a KNOWN open "
        "one-token repoint (roots handoff section 6), not a precedent to spread. Taken on potato "
        "and sweet-potato, hence two hits.",
}
EXPECTED_STEM_VARIANT_HITS = 2

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
    for w in ("always", "never", "completely", "totally", "harmless", "guaranteed",
              "eliminate", "eliminates"):
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
    return [(f, p) for f in ("pests", "diseases")
            for p in obj.get(f) or [] if isinstance(p, dict)]


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def sentences(text):
    return [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+", text or "")
            if len(s.strip()) > 40]


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# ------------------------------------------------------------------ pre-state checks
def check_full_schema_premise(by):
    """FULL schema present AND the note pair absent. Both directions, because batch 22 found that
    copying batch 21's note-schema guard would have refused an entire batch on its first guard."""
    seen = 0
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: crop %s not on the roster" % c)
        got = problems(by[c])
        if len(got) != EXPECTED_PROBLEMS[c]:
            raise SystemExit("REFUSED: %s has %d problems, expected %d"
                             % (c, len(got), EXPECTED_PROBLEMS[c]))
        for _f, p in got:
            seen += 1
            if p.get("control_ladder") is not None:
                raise SystemExit("REFUSED: %s/%r is ALREADY laddered" % (c, p.get("name")))
            if p.get("id") is not None:
                raise SystemExit("REFUSED: %s/%r already carries id %r"
                                 % (c, p.get("name"), p.get("id")))
            for f in FULL_SCHEMA_FIELDS:
                if not (p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%r missing full-schema field %s"
                                     % (c, p.get("name"), f))
            for f in NOTE_FIELDS:
                if f in p:
                    raise SystemExit("REFUSED: %s/%r carries note-schema field %s; this batch is "
                                     "FULL-schema" % (c, p.get("name"), f))
            if not p.get("severity"):
                raise SystemExit("REFUSED: %s/%r has no severity; all 22 carry one"
                                 % (c, p.get("name")))
            if not p.get("sources") or not p.get("anchoring_urls"):
                raise SystemExit("REFUSED: %s/%r missing sources/anchoring_urls" % (c, p.get("name")))
    if seen != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"
                         % (seen, sum(EXPECTED_PROBLEMS.values())))


def check_uniform_coarse_type_upgrade(batch, by):
    """The pre-state type is UNIFORMLY COARSE -- `pest` in pests[], `disease` in diseases[] -- and
    the post-state is the pinned fine type. Seventh distinct type situation in seven batches."""
    seen = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            coarse = "pest" if field == "pests" else "disease"
            pre = by[c].get(field) or []
            post = batch[c].get(field) or []
            if len(pre) != len(post):
                raise SystemExit("REFUSED: %s/%s length %d staged vs %d canonical"
                                 % (c, field, len(post), len(pre)))
            for i, (p, o) in enumerate(zip(pre, post)):
                seen += 1
                if p.get("type") != coarse:
                    raise SystemExit("REFUSED: %s/%s[%d] pre-state type %r, expected coarse %r"
                                     % (c, field, i, p.get("type"), coarse))
                want = ID_CONVENTION[(c, field, i)][2]
                if o.get("type") != want:
                    raise SystemExit("REFUSED: %s/%s[%d] staged type %r, pinned %r"
                                     % (c, field, i, o.get("type"), want))
                if o.get("type") == coarse:
                    raise SystemExit("REFUSED: %s/%s[%d] type was not upgraded off the coarse "
                                     "default" % (c, field, i))
    if seen != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: type upgrade scanned %d, expected %d"
                         % (seen, sum(EXPECTED_PROBLEMS.values())))


def check_ids(batch, by):
    """Every id and name against the pin table, positionally. Ids were pinned BEFORE fan-out
    (batch 17's lesson) and the staged output must not have drifted."""
    if len(ID_CONVENTION) != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: pin table holds %d entries, expected %d"
                         % (len(ID_CONVENTION), sum(EXPECTED_PROBLEMS.values())))
    seen = set()
    for (c, field, i), (name, pid, _t, _d) in sorted(ID_CONVENTION.items()):
        pre = (by[c].get(field) or [])
        post = (batch[c].get(field) or [])
        if i >= len(pre) or i >= len(post):
            raise SystemExit("REFUSED: %s/%s[%d] out of range" % (c, field, i))
        if pre[i].get("name") != name:
            raise SystemExit("REFUSED: %s/%s[%d] canonical name %r, pinned %r"
                             % (c, field, i, pre[i].get("name"), name))
        if post[i].get("id") != pid:
            raise SystemExit("REFUSED: %s/%s[%d] staged id %r, pinned %r"
                             % (c, field, i, post[i].get("id"), pid))
        seen.add((c, field, i))
    # COVERAGE, not a restatement. The first version filled `seen` by iterating ID_CONVENTION and
    # then compared it to ID_CONVENTION, so it could never fail -- a guard derived from what it
    # validates is vacuous, and the mutation harness proved it by surviving.
    positions = {(c, field, i) for c in CROPS for field in ("pests", "diseases")
                 for i in range(len(batch[c].get(field) or []))}
    if seen != positions:
        raise SystemExit("REFUSED: the pin table covers %d positions but the batch holds %d; "
                         "unpinned: %r" % (len(seen), len(positions),
                                           sorted(positions - seen)[:5]))
    # ids are per-crop join keys: unique WITHIN a crop
    for c in CROPS:
        ids = [p.get("id") for _f, p in problems(batch[c])]
        if len(ids) != len(set(ids)):
            raise SystemExit("REFUSED: %s has duplicate problem ids %r" % (c, ids))


def check_stemmed_id_scan(batch, data):
    """Batch 22 checked every mint BY ID and still missed two, because an exact check passes an id
    that merely RESEMBLES a live one. Each pin is anchored on the ORGANISM or the SCOPE reason read
    from the crops' own prose, never on the id string, so a name match cannot quietly satisfy it."""
    live = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if p.get("id"):
                live.setdefault(p["id"], []).append((c["slug"], p))
    staged_ids = {p["id"] for c in CROPS for _f, p in problems(batch[c])}

    for new_id, (resembles, own_reason, other_reason) in sorted(ID_SCOPE_PINS.items()):
        if new_id not in staged_ids:
            raise SystemExit("REFUSED: scope pin %r is not in the batch; the pin is stale" % new_id)
        if new_id in live:
            raise SystemExit("REFUSED: %r was minted as distinct but already exists on the roster"
                             % new_id)
        if resembles not in live:
            raise SystemExit("REFUSED: %r no longer exists on the roster, so the reason to keep "
                             "%r separate can no longer be checked" % (resembles, new_id))
        # the reason must still be readable in THIS batch's own prose
        blob = ""
        for c in CROPS:
            for _f, p in problems(batch[c]):
                if p["id"] == new_id:
                    src = None
                    for cc in data["crops"]:
                        if cc["slug"] != c:
                            continue
                        for _ff, pp in problems(cc):
                            if pp.get("name") == _pin_name(new_id):
                                src = pp
                    if src:
                        blob = " ".join(src.get(f) or "" for f in PROSE_FIELDS)
        if own_reason and own_reason.lower() not in blob.lower():
            raise SystemExit("REFUSED: the stated reason for minting %r (%r) is not in its own "
                             "prose any more" % (new_id, own_reason))
        if other_reason:
            oblob = " ".join(" ".join(p.get(f) or "" for f in PROSE_FIELDS)
                             for _s, p in live[resembles])
            if other_reason.lower() not in oblob.lower():
                raise SystemExit("REFUSED: %r no longer names %r, so the taxon collision that "
                                 "justified %r is unproven" % (resembles, other_reason, new_id))

    for (crop, pid), (precedent, phrase) in sorted(TAXON_REUSE_PINS.items()):
        if pid not in staged_ids:
            raise SystemExit("REFUSED: taxon-reuse pin %r not in the batch" % pid)
        hit = [p for s, p in live.get(pid, []) if s == precedent]
        if not hit:
            raise SystemExit("REFUSED: %r no longer holds %r, so the reuse is unproven"
                             % (precedent, pid))
        blob = " ".join(" ".join(p.get(f) or "" for f in PROSE_FIELDS) for p in hit)
        if phrase.lower() not in blob.lower():
            raise SystemExit("REFUSED: %s/%s no longer says %r; the taxon check that justified "
                             "reusing this id has stopped being true" % (precedent, pid, phrase))

    # THE SINGULAR/PLURAL CLASS -- the exact miss that let two ids through in batch 22, and which
    # an equality check cannot see. Whenever a batch id has a stem-equal SIBLING on the roster, the
    # roster holds two variants of one name and the batch has silently picked one. That choice must
    # be adjudicated in STEM_VARIANT_PINS, not left to whichever id the author happened to type.
    pinned = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for lid in sorted(live):
                if lid == p["id"] or _stem_key(lid) != _stem_key(p["id"]):
                    continue
                if (p["id"], lid) not in STEM_VARIANT_PINS:
                    raise SystemExit(
                        "REFUSED: %s takes %r while the roster also holds the stem-equal %r (on "
                        "%s). Two variants of one name exist; adjudicate which the batch takes and "
                        "pin it." % (c, p["id"], lid,
                                     ", ".join(sorted(s for s, _q in live[lid]))))
                pinned += 1
    if pinned != EXPECTED_STEM_VARIANT_HITS:
        raise SystemExit("REFUSED: %d stem-variant pairs adjudicated, pinned %d. A variant appeared "
                         "or vanished." % (pinned, EXPECTED_STEM_VARIANT_HITS))


def _pin_name(pid):
    for (_c, _f, _i), (name, i, _t, _d) in ID_CONVENTION.items():
        if i == pid:
            return name
    return None


def _stem_key(s):
    """Singular/plural normalisation. The first version of this stripped "es" from "beetles" and
    produced "beetl", while "beetle" stayed "beetle", so the two did NOT compare equal and the
    guard silently skipped the exact pair it exists for. The pre-authoring scan carried the same
    bug and missed `flea-beetle` vs `flea-beetles`; only the handoff's prior knowledge covered it.
    Strip a trailing plural "s" instead, which keeps the singular form as the shared key."""
    out = []
    for t in re.split(r"[^a-z0-9]+", s.lower()):
        if not t:
            continue
        if t.endswith("ies") and len(t) > 4:
            t = t[:-3] + "y"
        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            t = t[:-1]
        out.append(t)
    return tuple(sorted(out))


def check_no_template_twins_premise(by, data):
    """Batch 22's `check_template_sibling_divergence` is DROPPED because roots has ZERO template
    twins, so it would be vacuous and its own anti-vacuity branch would refuse. Dropping a guard
    silently is how a premise stops being checked, so the zero is ASSERTED here instead."""
    compared = 0
    for c in CROPS:
        for _f, p in problems(by[c]):
            key = tuple(p.get(f) for f in PROSE_FIELDS)
            for cc in data["crops"]:
                if cc["slug"] in CROPS:
                    continue
                if not any(x.get("control_ladder") for _ff, x in problems(cc)):
                    continue
                for _ff, pp in problems(cc):
                    compared += 1
                    if tuple(pp.get(f) for f in PROSE_FIELDS) == key:
                        raise SystemExit(
                            "REFUSED: %s/%r is a TEMPLATE TWIN of %s/%r. Roots was promoted on the "
                            "measured premise of zero twins; restore batch 22's "
                            "check_template_sibling_divergence before shipping this."
                            % (c, p.get("name"), cc["slug"], pp.get("name")))
    if compared == 0:
        raise SystemExit("REFUSED: no shipped problems compared; the twin premise is unproven")


def check_no_precedent_copy(batch, data):
    """THE guard chosen for this batch, by measurement. See the module docstring: threshold 0.70
    sits just above a measured independent-authoring ceiling of 0.644 over 207 singleton pairs, and
    the 13 reused ids carry 388 existing rungs to compare against."""
    live = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if not p.get("id"):
                continue
            for r in p.get("control_ladder") or []:
                live.setdefault((p["id"], r["method"]), []).append(
                    (c["slug"], r.get("note_beginner") or "", r.get("note_seasoned") or ""))
    compared = 0
    worst = (0.0, None)
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for slug, nb, ns in live.get((p["id"], r["method"]), []):
                    compared += 1
                    # autojunk=False and PER-REGISTER MAX, both learned the hard way. The first
                    # version used difflib's defaults and averaged the registers, and it scored the
                    # one real copy in this batch at 0.431 -- comfortably "independent". difflib's
                    # autojunk heuristic engages at 200 characters and junks any character present
                    # in more than 1% of the sequence, which describes every seasoned register, so
                    # it deflated exactly the strings that matter. Averaging then diluted a single
                    # copied register against an independent one. The same pair scores 0.757 here.
                    s = max(
                        difflib.SequenceMatcher(None, r.get("note_beginner") or "", nb,
                                                autojunk=False).ratio(),
                        difflib.SequenceMatcher(None, r.get("note_seasoned") or "", ns,
                                                autojunk=False).ratio())
                    if s > worst[0]:
                        worst = (s, "%s/%s/%s vs %s" % (c, p["id"], r["method"], slug))
                    if s >= PRECEDENT_COPY_THRESHOLD:
                        raise SystemExit(
                            "REFUSED: %s/%s/%s is %.3f similar to %s's rung for the same problem "
                            "and method (threshold %.2f). The measured ceiling for independent "
                            "authoring is 0.644."
                            % (c, p["id"], r["method"], s, slug, PRECEDENT_COPY_THRESHOLD))
    if compared == 0:
        raise SystemExit("REFUSED: check_no_precedent_copy made 0 comparisons; it is vacuous. "
                         "13 reused ids should reach 388 existing rungs.")
    return compared, worst


def check_no_shipped_prose_echo(batch, data):
    """Carried from batch 21/22 unchanged. A guard that refuses an input and stays green is a
    REFUSAL-SPEC pass. Identical shape with independent prose is convergent authoring; identical
    prose is copying, and this batch pointed every agent at a precedent crop."""
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
                    tag = "%s/%s/%s" % (c["slug"], p.get("id"), r["method"])
                    whole.setdefault(v.strip().lower(), tag)
                    for s in sentences(v):
                        sent.setdefault(s, tag)
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
                                             "%s: %r"
                                             % (c, p["id"], r["method"], k, sent[s], s[:70]))
    if not whole:
        raise SystemExit("REFUSED: no shipped rung prose found; this guard would be vacuous")
    if checked == 0:
        raise SystemExit("REFUSED: no batch notes scanned; this guard would be vacuous")


def check_temperature_figures_warranted(batch, by, cm):
    """Batch 22 BANNED temperature figures outright and its crops contained none, so the ban was a
    refusal-spec pass. Roots contains 5 and every one is sourced, so a ban would refuse verified
    content. Each figure must appear in the problem's OWN prose or in the METHOD's own catalog text.
    The count is pinned, so a figure that vanishes is as visible as one that appears."""
    found = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            for i, p in enumerate(batch[c].get(field) or []):
                src = (by[c].get(field) or [])[i]
                src_blob = " ".join(src.get(f) or "" for f in PROSE_FIELDS)
                for r in p.get("control_ladder") or []:
                    m = cm.get(r["method"]) or {}
                    meth_blob = json.dumps(m, ensure_ascii=False)
                    for k in ADVICE_FIELDS:
                        for hit in TEMP_FIGURE.findall(r.get(k) or ""):
                            found += 1
                            num = re.sub(r"\D", "", hit)
                            in_src = num in re.sub(r"\s+", "", src_blob)
                            in_meth = num in re.sub(r"\s+", "", meth_blob)
                            if not (in_src or in_meth):
                                raise SystemExit(
                                    "REFUSED: %s/%s/%s %s states %r, which appears neither in the "
                                    "problem's own prose nor in the method's catalog text"
                                    % (c, p["id"], r["method"], k, hit))
    if found != EXPECTED_TEMP_FIGURES:
        raise SystemExit("REFUSED: found %d temperature figures, pinned %d. A figure was added or "
                         "removed without adjudication." % (found, EXPECTED_TEMP_FIGURES))


def check_no_ladder_vocabulary(batch):
    seen = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                for f in ADVICE_FIELDS:
                    seen += 1
                    m = LADDER_VOCAB.search(r.get(f) or "")
                    if m:
                        raise SystemExit("REFUSED: %s/%s/%s %s uses internal vocabulary (%r)"
                                         % (c, p["id"], r["method"], f, m.group(0)))
    if seen == 0:
        raise SystemExit("REFUSED: no notes scanned for vocabulary; this guard would be vacuous")


def validate_batch(batch, cm):
    total = 0
    for c in CROPS:
        n = 0
        for _f, p in problems(batch[c]):
            ladder = p.get("control_ladder")
            if not ladder:
                raise SystemExit("REFUSED: %s/%s has an empty ladder" % (c, p.get("id")))
            seen_methods = set()
            last = -1
            for r in ladder:
                n += 1
                total += 1
                meth = r.get("method")
                if meth not in cm:
                    raise SystemExit("REFUSED: %s/%s names unknown method %r"
                                     % (c, p.get("id"), meth))
                if meth in seen_methods:
                    raise SystemExit("REFUSED: %s/%s repeats method %r" % (c, p.get("id"), meth))
                seen_methods.add(meth)
                tier = cm[meth].get("tier")
                if tier not in TIERS:
                    raise SystemExit("REFUSED: %s/%s method %r has unknown tier %r"
                                     % (c, p.get("id"), meth, tier))
                if TIERS.index(tier) < last:
                    raise SystemExit("REFUSED: %s/%s tier decreases at %r"
                                     % (c, p.get("id"), meth))
                last = max(last, TIERS.index(tier))
                applies = cm[meth].get("applies_to") or []
                if "any" not in applies and not _type_ok(p.get("type"), applies):
                    raise SystemExit("REFUSED: %s/%s (%s) uses %r whose applies_to %r does not "
                                     "reach it" % (c, p.get("id"), p.get("type"), meth, applies))
                nb, ns = r.get("note_beginner"), r.get("note_seasoned")
                if not nb or not ns:
                    raise SystemExit("REFUSED: %s/%s/%s missing a register"
                                     % (c, p.get("id"), meth))
                if nb.strip() == ns.strip():
                    raise SystemExit("REFUSED: %s/%s/%s registers are identical"
                                     % (c, p.get("id"), meth))
                if set(r) - {"method", "note_beginner", "note_seasoned"}:
                    raise SystemExit("REFUSED: %s/%s/%s has unexpected rung keys %r"
                                     % (c, p.get("id"), meth,
                                        sorted(set(r) - {"method", "note_beginner",
                                                         "note_seasoned"})))
                for f in ADVICE_FIELDS:
                    bad = hygiene(r[f])
                    if bad:
                        raise SystemExit("REFUSED: %s/%s/%s %s: %s"
                                         % (c, p.get("id"), meth, f, ", ".join(bad)))
        if n != EXPECTED_RUNGS[c]:
            raise SystemExit("REFUSED: %s has %d rungs, expected %d" % (c, n, EXPECTED_RUNGS[c]))
    # FORWARD ASSERTION, verified and WITHDRAWN from the mutation harness rather than reported as
    # a permanent survivor. `total` is the sum of the per-crop counts each already pinned against
    # EXPECTED_RUNGS[c] on the line above, and TOTAL_RUNGS == sum(EXPECTED_RUNGS.values()) is pinned
    # by the suite, so no post-state mutation can make this fire while the per-crop checks pass.
    if total != TOTAL_RUNGS:
        raise SystemExit("REFUSED: %d rungs total, expected %d" % (total, TOTAL_RUNGS))


def check(data):
    by = by_slug(data)
    batch = staged()
    cm = data["control_methods"]
    check_full_schema_premise(by)
    check_uniform_coarse_type_upgrade(batch, by)
    check_ids(batch, by)
    check_stemmed_id_scan(batch, data)
    check_no_template_twins_premise(by, data)
    check_no_precedent_copy(batch, data)
    check_no_shipped_prose_echo(batch, data)
    check_temperature_figures_warranted(batch, by, cm)
    check_no_ladder_vocabulary(batch)
    validate_batch(batch, cm)
    return batch


def snapshot(data):
    """LEAF level. Every problem field on every crop on the roster, plus a per-crop blob of
    everything that is not a problem array. `set(pre) == set(post)` is compared BEFORE any value
    comparison in verify_post, because iterating `pre` alone makes every ADDITION invisible --
    all four PLA-162 defects."""
    snap = {}
    for c in data["crops"]:
        slug = c["slug"]
        for field in ("pests", "diseases"):
            for i, p in enumerate(c.get(field) or []):
                for k, v in p.items():
                    snap[(slug, field, i, k)] = json.dumps(v, ensure_ascii=False, sort_keys=True)
        rest = {k: v for k, v in c.items() if k not in ("pests", "diseases")}
        snap[(slug, "__crop__", -1, "__rest__")] = json.dumps(rest, ensure_ascii=False,
                                                              sort_keys=True)
    return snap


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
    # SET COMPARISON FIRST, always, before any value is looked at.
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    unexpected_add = {k for k in added if not (k[0] in CROPS and k[3] in ("id", "control_ladder"))}
    if unexpected_add:
        raise SystemExit("REFUSED: unexpected leaf keys added: %r" % sorted(unexpected_add)[:6])
    if dropped:
        raise SystemExit("REFUSED: leaf keys dropped: %r" % sorted(dropped)[:6])
    if len(added) != 2 * sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: %d leaf keys added, expected %d (id + control_ladder on each of "
                         "%d problems)" % (len(added), 2 * sum(EXPECTED_PROBLEMS.values()),
                                           sum(EXPECTED_PROBLEMS.values())))
    touched = set()
    for k in set(pre) & set(post):
        if pre[k] == post[k]:
            continue
        if k[0] not in CROPS:
            raise SystemExit("REFUSED: bystander crop %s changed at %r" % (k[0], k))
        if k[3] != "type":
            raise SystemExit("REFUSED: %s changed an unexpected field %r; this batch sets id, type "
                             "and control_ladder only" % (k[0], k[3]))
        touched.add((k[0], k[1], k[2]))
    if len(touched) != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: %d problems had type upgraded, expected %d"
                         % (len(touched), sum(EXPECTED_PROBLEMS.values())))
    per_crop = {}
    for slug, _f, _i in touched:
        per_crop[slug] = per_crop.get(slug, 0) + 1
    # FORWARD ASSERTION, verified and WITHDRAWN from the mutation harness. `touched` holds only
    # batch-crop positions (a bystander raises above), so each crop contributes at most its own
    # problem count; those maxima sum to exactly 22, so the len(touched) == 22 check on the line
    # above already forces this split. Kept as a statement of intent, not counted as coverage.
    if per_crop != EXPECTED_PROBLEMS:
        raise SystemExit("REFUSED: per-crop problem counts %r, expected %r"
                         % (per_crop, EXPECTED_PROBLEMS))
    return len(touched)


def check_catalog_untouched(before_cm, before_sc, data):
    """Lifted out of main() so the suite and the mutation harness can REACH it. A guard that only
    exists inside an entry point the suite never calls is untested code wearing a guard's clothes."""
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this batch mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed")


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

    check_catalog_untouched(before_cm, before_sc, data)

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
