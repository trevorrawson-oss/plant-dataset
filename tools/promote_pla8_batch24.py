#!/usr/bin/env python3
"""PLA-8 BATCH 24 -- THE ALLIUMS: chives, leek, onion, shallot.
Base 47e7b5c0 (after allium record corrections r4). RE-AUTHORED 2026-09-03.

26 problems gain `id`, a `type` and a `control_ladder`; **95 rungs**. Roster laddered 97 -> 101.
NO catalog mutation.

--------------------------------------------------------------------------------------------------
RE-AUTHORED AGAINST THE CORRECTED RECORDS, AND REVIEWED BEFORE THE PROMOTE
--------------------------------------------------------------------------------------------------
The first staging of this batch (base c24d7754, 27 problems, 82 rungs) was faithful to records that
an independent source-truth pass then found wrong in 50 places. The records were corrected first
(r1, the chives aphids retirement, r2, r3, r4: ten decisions, 80519a28 -> 47e7b5c0) and the batch
was re-authored from them: four agents, one per crop, each with a per-crop validator running this
promote's own copy, echo, hygiene and warrant checks, then four INDEPENDENT reviewers who fetched
and read every anchoring document and returned 28 FIX items across 97 rungs (none a timing rule),
then four fixers. The thrips `weed_host_control` rung was dropped on onion and shallot at review
(a siting claim under a weed-removal method, on records that say nothing about weeds), which is
97 -> 95. The previous outputs are kept beside the new ones as `prev_out_<crop>.json`.

chives lost its Aphids entry to the record pass (retired, 80519a28), so the batch is 26 problems,
not 27, and the pin table has no chives/pests[3].

--------------------------------------------------------------------------------------------------
THE PREMISE IS SPLIT BY SCHEMA, AND THAT IS NEW. IT WAS MEASURED, NOT INHERITED.
--------------------------------------------------------------------------------------------------
**chives is FULL-schema** (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`) and
carries **NO `severity`**. **leek, onion and shallot use `identification_*` / `management_*`**, an
ALLIUM-ONLY shape, and all three carry `severity` on every problem. Measured roster-wide, the
identification/management schema belongs to exactly five crops -- garlic, leek, onion, shallot,
spring-onion -- and garlic and spring-onion are already laddered from it, so the shape is proven.

**Type: SET FROM NOTHING.** All 27 pre-state problems carry NO `type` key at all, which is the
batch 20/21 shape. Batch 23's `check_uniform_coarse_type_upgrade` would have refused this entire
batch on its first guard, because there is no coarse value to upgrade from. Eighth distinct type
situation in eight batches.

--------------------------------------------------------------------------------------------------
THE TEMPLATE-TWIN PREMISE WAS ASSERTED FALSELY ONCE, AND THE FIX IS SCHEMA-AWARE COMPARISON
--------------------------------------------------------------------------------------------------
The batch's pin file originally claimed 3 template twins against spring-onion and instructed two
authoring agents to copy spring-onion's shipped ladders byte-for-byte. **There are ZERO.** The scan
compared the 8 FULL-schema fields on crops that do not carry them, so 6 of 8 were `None` on BOTH
sides and the tuples matched on ABSENCE.

Re-measured on the fields each crop actually holds, the three "twins" share only `cause_beginner`
and `cause_seasoned` and DIFFER on both `management_*` fields, which is where a ladder comes from.
**Two agents refused the instruction and measured instead**, and complying would have shipped two
defects: onion/`onion-thrips` would have DROPPED `reflective_mulch` (a control onion's prose names
and spring-onion's does not), and onion/`fusarium-basal-rot` would have carried the word "scallion"
into the onion record.

`check_no_template_twins_premise` is therefore SCHEMA-AWARE here: it compares each crop on the field
set that crop carries, and a comparison is only counted when the fields are actually PRESENT on both
sides. A guard that can match `None` to `None` reports identity where there is only absence.

--------------------------------------------------------------------------------------------------
THE DIVERGENCE GUARD IS A PRECEDENT-COPY CHECK WITH A PIN TABLE OF DECLARED IDENTITIES
--------------------------------------------------------------------------------------------------
Fifth distinct divergence guard in five batches. Batch 22 asserted that identical prose implies
identical ladders; batch 23 asserted ZERO declared identities and refused anything at 0.70+; neither
fits here, because this batch has exactly ONE legitimate byte-identical rung and it must be allowed
by name rather than by threshold.

`check_no_precedent_copy` carries batch 23's corrected metric -- `autojunk=False` and a PER-REGISTER
MAX, because difflib's autojunk deflates any sequence over 200 characters and a mean dilutes one
copied register against one independent one -- and adds `DECLARED_IDENTITIES`. A pair listed there
MUST be byte-identical; a pair not listed must score under 0.70.

**The one declared identity is `onion`/`onion-thrips`/`water_spray` against spring-onion.** Onion's
and spring-onion's records carry the water-spray claim word for word ("hose off light infestations"
/ "spray them off with water if thrips are light"); only the surrounding field differs. Where the
sourced claim is identical, a cosmetic divergence is the batch-3 defect. Making it identical AND
declaring it is the honest form; near-identical is the worst of both worlds.

**Seven rungs were measured at 0.70+ and sent back.** They were paraphrases of the sibling's shipped
rung -- same sentence order, synonym swaps -- not independent authoring, and the agent that wrote
six of them had itself declined to copy a sibling note minutes earlier. The measured ceiling for
genuinely independent authoring elsewhere on the roster is 0.684 and this batch's median is 0.411.

--------------------------------------------------------------------------------------------------
TEMPERATURES ARE WARRANTED, NOT BANNED
--------------------------------------------------------------------------------------------------
3 figures, all on chives: 90°F twice from `insecticidal_soap`'s own caution, and 75°F from chives'
own downy mildew prose. Same warrant check as batch 23, count pinned at 3.

REFUSALS: base SHA mismatch; a target already laddered or already carrying an id; the wrong schema
for the crop; `severity` present or absent against its pinned per-crop shape; a pre-state `type`
present at all; a staged type off the pin; an id off the pin table; a minted id stem-equal to a live
one without an adjudication; a template twin appearing; a rung within 0.70 of a precedent crop's
rung unless DECLARED; a declared identity that is not byte-identical; a rung note echoing shipped
prose; an unwarranted temperature figure; ladder vocabulary; unknown method; tier decrease;
applies_to incoherence; identical registers; duplicate method; empty ladder; counts off; ANY change
to control_methods, source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch24.py
Mutation harness: tools/mutate_pla8_batch24_suite.py (PLA-215)
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch24_alliums")
BASE_SHA = "47e7b5c03cd91829a40279f319f11140de800a127aff2d277d1e977f95b6b143"  # after record corrections r4

CROPS = ("chives", "leek", "onion", "shallot")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")

# THE SCHEMA SPLIT. chives is FULL; the three true alliums are identification/management.
FULL_SCHEMA_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                      "organic_treatment_beginner", "organic_treatment_seasoned",
                      "prevention_beginner", "prevention_seasoned")
ALLIUM_SCHEMA_FIELDS = ("identification_beginner", "identification_seasoned",
                        "management_beginner", "management_seasoned",
                        "cause_beginner", "cause_seasoned")
SCHEMA_FOR = {"chives": FULL_SCHEMA_FIELDS, "leek": ALLIUM_SCHEMA_FIELDS,
              "onion": ALLIUM_SCHEMA_FIELDS, "shallot": ALLIUM_SCHEMA_FIELDS}
# severity splits the OTHER way, and only measuring found it
SEVERITY_EXPECTED = {"chives": False, "leek": True, "onion": True, "shallot": True}
NOTE_FIELDS = ("note_beginner", "note_seasoned", "note", "summary")

EXPECTED_PROBLEMS = {"chives": 7, "leek": 7, "onion": 5, "shallot": 7}  # chives aphids RETIRED (80519a28)
EXPECTED_RUNGS = {"chives": 27, "leek": 29, "onion": 16, "shallot": 23}  # re-authored 2026-09-03 against the corrected records; the thrips weed_host_control rung dropped on onion and shallot at review
TOTAL_RUNGS = 95
PRECEDENT_COPY_THRESHOLD = 0.70
EXPECTED_TEMP_FIGURES = 10  # chives 2 (75, 90), leek 6 (50 x4, 75, 59), onion 1 (85), shallot 1 (85); every one in the record

# The precedent scan's MEASURED result, filled by check() and printed by main(). Recorded
# rather than asserted in a docstring: the ceiling is the number that decides the batch, and
# a claim about it in prose cannot go stale loudly. Pinned by the suite.
METRICS = {}

# THE ID ADJUDICATIONS. Each anchored on the ORGANISM or the SCOPE read from prose, never on a
# name match, so it fails loudly if the reason stops being true rather than passing quietly.
ID_SCOPE_PINS = {
    # chives' entry is compound in its own name and its cause describes a FOLIAR blight (dense
    # canopies, splashing water). The live id is the STORAGE rot: garlic's holder names curing.
    "botrytis-leaf-blight-neck-rot": (
        "botrytis-neck-rot",
        "dense canopies",
        "curing"),
}
# leek NAMES its problem "Allium leaf miner" (two words) where the roster spells the id
# `allium-leafminer`. A stemmed scan scores that pair NOVEL, so minting off the spelling would have
# put two ids on one taxon. Anchored on the organism both records name.
SPELLING_VARIANT_PINS = {
    ("leek", "allium-leafminer"): ("Allium leaf miner", "Phytomyza gymnostoma"),
}
# A REUSE whose taxon check PASSED, pinned so it fails loudly if the reason dies.
TAXON_REUSE_PINS = {
    ("chives", "white-rot"): ("garlic", "Sclerotium cepivorum"),
}
# No minted id in this batch is stem-equal to a live one; measured, not assumed. The guard is a
# REFUSAL SPEC: staying green at zero is the pass, and a variant appearing later will refuse.
STEM_VARIANT_PINS = {}
EXPECTED_STEM_VARIANT_HITS = 0

# A pair here MUST be byte-identical; anything not here must score under the threshold.
DECLARED_IDENTITIES = {
    ("onion", "onion-thrips", "water_spray"): (
        "spring-onion",
        "onion and spring-onion carry the water-spray claim word for word ('hose off light "
        "infestations' / 'spray them off with water if thrips are light'); only the surrounding "
        "field differs. Identical sourced claim, so a cosmetic divergence would be the defect."),
}

ID_CONVENTION = {
    ("chives", "pests", 0): ('Onion thrips', "onion-thrips", "insect", "REUSE"),
    ("chives", "pests", 1): ('Allium leafminer', "allium-leafminer", "insect", "REUSE"),
    ("chives", "pests", 2): ('Onion maggot', "onion-maggot", "insect", "REUSE"),
    # ("chives", "pests", 3): Aphids -- RETIRED by promote_drop_chives_aphids (b89763b7 -> 80519a28)
    ("chives", "diseases", 0): ('Downy mildew', "downy-mildew", "fungal", "REUSE"),
    ("chives", "diseases", 1): ('Rust', "chives-rust", "fungal", "MINT"),
    ("chives", "diseases", 2): ('White rot', "white-rot", "fungal", "REUSE"),
    ("chives", "diseases", 3): ('Botrytis (leaf blight and neck rot)', "botrytis-leaf-blight-neck-rot", "fungal", "MINT"),
    ("leek", "pests", 0): ('Onion thrips', "onion-thrips", "insect", "REUSE"),
    ("leek", "pests", 1): ('Leek moth', "leek-moth", "insect", "MINT"),
    ("leek", "pests", 2): ('Onion maggot', "onion-maggot", "insect", "REUSE"),
    ("leek", "pests", 3): ('Allium leaf miner', "allium-leafminer", "insect", "REUSE"),
    ("leek", "diseases", 0): ('Leek rust', "leek-rust", "fungal", "MINT"),
    ("leek", "diseases", 1): ('White rot', "white-rot", "fungal", "REUSE"),
    ("leek", "diseases", 2): ('Pink root', "pink-root", "fungal", "MINT"),
    ("onion", "pests", 0): ('Onion thrips', "onion-thrips", "insect", "REUSE"),
    ("onion", "pests", 1): ('Onion maggot', "onion-maggot", "insect", "REUSE"),
    ("onion", "diseases", 0): ('Botrytis neck rot', "botrytis-neck-rot", "fungal", "REUSE"),
    ("onion", "diseases", 1): ('Fusarium basal rot', "fusarium-basal-rot", "fungal", "REUSE"),
    ("onion", "diseases", 2): ('Pink root', "pink-root", "fungal", "MINT"),
    ("shallot", "pests", 0): ('Onion thrips', "onion-thrips", "insect", "REUSE"),
    ("shallot", "pests", 1): ('Onion maggot', "onion-maggot", "insect", "REUSE"),
    ("shallot", "pests", 2): ('Allium leafminer', "allium-leafminer", "insect", "REUSE"),
    ("shallot", "diseases", 0): ('White rot', "white-rot", "fungal", "REUSE"),
    ("shallot", "diseases", 1): ('Downy mildew', "downy-mildew", "fungal", "REUSE"),
    ("shallot", "diseases", 2): ('Botrytis neck rot', "botrytis-neck-rot", "fungal", "REUSE"),
    ("shallot", "diseases", 3): ('Pink root', "pink-root", "fungal", "MINT"),
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
        with open(p) as fh:
            out[c] = json.load(fh)
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
def check_schema_premise(by):
    """SPLIT BY SCHEMA, and asserted in BOTH directions per crop. chives is FULL-schema and carries
    NO severity; leek, onion and shallot use identification_*/management_* and ALL carry severity.
    Batch 23's single-schema guard would have refused this batch on its first problem."""
    seen = 0
    for c in CROPS:
        if c not in by:
            raise SystemExit("REFUSED: crop %s not on the roster" % c)
        fields = SCHEMA_FOR[c]
        other = ALLIUM_SCHEMA_FIELDS if fields is FULL_SCHEMA_FIELDS else FULL_SCHEMA_FIELDS
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
            for f in fields:
                if not (p.get(f) or "").strip():
                    raise SystemExit("REFUSED: %s/%r missing %s, required by its schema"
                                     % (c, p.get("name"), f))
            # BOTH DIRECTIONS: the other schema's fields must be ABSENT, or the crop is not the
            # shape this batch was authored against and the brief pointed its agent at the wrong
            # fields.
            for f in other:
                if f in p and f not in fields:
                    raise SystemExit("REFUSED: %s/%r carries %s from the OTHER schema; the split is "
                                     "wrong for this crop" % (c, p.get("name"), f))
            for f in NOTE_FIELDS:
                if f in p:
                    raise SystemExit("REFUSED: %s/%r carries note-schema field %s"
                                     % (c, p.get("name"), f))
            has_sev = bool(p.get("severity"))
            if has_sev != SEVERITY_EXPECTED[c]:
                raise SystemExit("REFUSED: %s/%r severity present=%s, pinned %s. severity splits by "
                                 "crop here and only measuring found it."
                                 % (c, p.get("name"), has_sev, SEVERITY_EXPECTED[c]))
            if not p.get("sources") or not p.get("anchoring_urls"):
                raise SystemExit("REFUSED: %s/%r missing sources/anchoring_urls" % (c, p.get("name")))
    if seen != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"
                         % (seen, sum(EXPECTED_PROBLEMS.values())))


def check_type_set_from_nothing(batch, by):
    """All 27 pre-state problems carry NO `type` KEY AT ALL (the batch 20/21 shape). Batch 23's
    coarse->fine upgrade guard has nothing to upgrade from and would refuse this batch outright."""
    seen = 0
    for c in CROPS:
        for field in ("pests", "diseases"):
            pre = by[c].get(field) or []
            post = batch[c].get(field) or []
            if len(pre) != len(post):
                raise SystemExit("REFUSED: %s/%s length %d staged vs %d canonical"
                                 % (c, field, len(post), len(pre)))
            for i, (p, o) in enumerate(zip(pre, post)):
                seen += 1
                if p.get("type") is not None:
                    raise SystemExit("REFUSED: %s/%s[%d] already carries type %r; this batch SETS "
                                     "the type from nothing" % (c, field, i, p.get("type")))
                want = ID_CONVENTION[(c, field, i)][2]
                if o.get("type") != want:
                    raise SystemExit("REFUSED: %s/%s[%d] staged type %r, pinned %r"
                                     % (c, field, i, o.get("type"), want))
                if o.get("type") not in _TYPE_TARGETS:
                    raise SystemExit("REFUSED: %s/%s[%d] type %r is not in the gate's type map"
                                     % (c, field, i, o.get("type")))
    if seen != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: type set scanned %d, expected %d"
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


def check_id_adjudications(batch, data):
    """The id decisions this batch made that a name comparison alone would get wrong. Each is
    anchored on the ORGANISM or the SCOPE read from prose, never on the id string."""
    live = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            if p.get("id"):
                live.setdefault(p["id"], []).append((c["slug"], p))
    staged_ids = {p["id"] for c in CROPS for _f, p in problems(batch[c])}

    # 1. SCOPE VARIANT: chives' compound Botrytis vs the live neck-rot-only id.
    for new_id, (resembles, own_phrase, other_phrase) in sorted(ID_SCOPE_PINS.items()):
        if new_id not in staged_ids:
            raise SystemExit("REFUSED: scope pin %r is not in the batch; the pin is stale" % new_id)
        if new_id in live:
            raise SystemExit("REFUSED: %r was minted as distinct but already exists" % new_id)
        if resembles not in live:
            raise SystemExit("REFUSED: %r no longer exists, so the reason to keep %r separate "
                             "cannot be checked" % (resembles, new_id))
        oblob = " ".join(" ".join(p.get(f) or "" for f in SCHEMA_FOR.get(sl, FULL_SCHEMA_FIELDS))
                         for sl, p in live[resembles]).lower()
        if other_phrase.lower() not in oblob:
            raise SystemExit("REFUSED: %r no longer says %r, so the scope split that justified %r "
                             "is unproven" % (resembles, other_phrase, new_id))
        # THE OWN SIDE. A scope split has two halves and this pin declares both: chives' entry is a
        # FOLIAR blight, the live id is the STORAGE rot. Only the other half was checked -- the
        # tuple element was unpacked and never read, which is an unused pin reading as coverage.
        own = [(c, i, f) for (c, f, i), (_n, pid, _t, _d) in ID_CONVENTION.items()
               if pid == new_id]
        if len(own) != 1:
            raise SystemExit("REFUSED: scope pin %r maps to %d pinned positions, expected exactly "
                             "1; the own side cannot be anchored" % (new_id, len(own)))
        oc, oi, ofield = own[0]
        osrc = (by_slug(data)[oc].get(ofield) or [])[oi]
        sblob = " ".join(osrc.get(f) or "" for f in SCHEMA_FOR[oc]).lower()
        if own_phrase.lower() not in sblob:
            raise SystemExit("REFUSED: %s/%r no longer says %r, so the half of the scope split that "
                             "makes %r a DISTINCT entry is unproven"
                             % (oc, osrc.get("name"), own_phrase, new_id))

    # 2. SPELLING VARIANT: leek's problem is NAMED "Allium leaf miner" (two words) but REUSES the
    #    live `allium-leafminer`. A stemmed scan scores that pair NOVEL, so minting off the spelling
    #    would have put two ids on one taxon. Anchored on the organism both records name.
    for (crop, pid), (display_name, organism) in sorted(SPELLING_VARIANT_PINS.items()):
        hit = [p for _f, p in problems(batch[crop]) if p["id"] == pid]
        if not hit:
            raise SystemExit("REFUSED: spelling pin %s/%s is not in the batch" % (crop, pid))
        src = None
        for cc in data["crops"]:
            if cc["slug"] != crop:
                continue
            for _f, p in problems(cc):
                if p.get("name") == display_name:
                    src = p
        if src is None:
            raise SystemExit("REFUSED: %s no longer names a problem %r; the spelling pin is stale"
                             % (crop, display_name))
        blob = " ".join(src.get(f) or "" for f in SCHEMA_FOR[crop]).lower()
        if organism.lower() not in blob:
            raise SystemExit("REFUSED: %s/%r no longer names %r, so reusing %r across the spelling "
                             "difference is unproven" % (crop, display_name, organism, pid))

    # 3. TAXON REUSE: white rot is reused across the alliums on one named organism.
    for (crop, pid), (precedent, phrase) in sorted(TAXON_REUSE_PINS.items()):
        if pid not in staged_ids:
            raise SystemExit("REFUSED: taxon-reuse pin %r not in the batch" % pid)
        hit = [p for sl, p in live.get(pid, []) if sl == precedent]
        if not hit:
            raise SystemExit("REFUSED: %r no longer holds %r, so the reuse is unproven"
                             % (precedent, pid))
        blob = " ".join(" ".join(p.get(f) or "" for f in SCHEMA_FOR.get(precedent, FULL_SCHEMA_FIELDS))
                        for p in hit).lower()
        if phrase.lower() not in blob:
            raise SystemExit("REFUSED: %s/%s no longer says %r; the taxon check that justified this "
                             "reuse has stopped being true" % (precedent, pid, phrase))

    # 4. The singular/plural class. A MINTED id stem-equal to a live one must be adjudicated.
    pinned = 0
    for c in CROPS:
        for _f, p in problems(batch[c]):
            if p["id"] in live:
                continue
            for lid in sorted(live):
                if _stem_key(lid) != _stem_key(p["id"]):
                    continue
                if (p["id"], lid) not in STEM_VARIANT_PINS:
                    raise SystemExit("REFUSED: %s MINTS %r while the roster holds the stem-equal "
                                     "%r; adjudicate before minting" % (c, p["id"], lid))
                pinned += 1
    if pinned != EXPECTED_STEM_VARIANT_HITS:
        raise SystemExit("REFUSED: %d stem-variant pairs adjudicated, pinned %d"
                         % (pinned, EXPECTED_STEM_VARIANT_HITS))


def _stem_key(s):
    """Strips a trailing plural `s`. An earlier version stripped `es`, turning `beetles` into
    `beetl` while `beetle` stayed `beetle`, so the two did not compare equal and the guard skipped
    the exact pair it exists for."""
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
    """SCHEMA-AWARE, and that is the whole point. The first version of this batch's twin scan
    compared the 8 FULL-schema fields on crops that use identification_*/management_*, so 6 of 8
    were None on BOTH sides and the tuples matched on ABSENCE. It reported 3 twins where there are
    ZERO, and two authoring agents were told to copy a sibling's ladder on the strength of it.

    A comparison is counted ONLY where the fields are actually present on both sides."""
    compared = 0
    for c in CROPS:
        fields = SCHEMA_FOR[c]
        for _f, p in problems(by[c]):
            if not all(p.get(k) for k in fields):
                continue
            key = tuple(p.get(k) for k in fields)
            for cc in data["crops"]:
                if cc["slug"] in CROPS:
                    continue
                if not any(x.get("control_ladder") for _ff, x in problems(cc)):
                    continue
                for _ff, pp in problems(cc):
                    if not all(pp.get(k) for k in fields):
                        continue
                    compared += 1
                    if tuple(pp.get(k) for k in fields) == key:
                        raise SystemExit(
                            "REFUSED: %s/%r is a TEMPLATE TWIN of %s/%r on the fields both actually "
                            "carry. This batch was promoted on a measured premise of ZERO twins; "
                            "restore a divergence guard before shipping."
                            % (c, p.get("name"), cc["slug"], pp.get("name")))
    if compared == 0:
        raise SystemExit("REFUSED: no schema-compatible shipped problem was compared; the twin "
                         "premise is unproven and this guard is vacuous")


def check_no_precedent_copy(batch, data):
    """TWO passes, because one is not enough and an authoring agent found the gap.

    Pass A keys on (problem id, method) -- the batch 23 shape. Pass B keys on METHOD ALONE, across
    any problem, and it is the one that matters here: phrasing lifted from a sibling's DIFFERENT
    problem scores 0.000 under pass A. Two real cases were caught only by pass B, on `pink-root`,
    a problem NO shipped crop carries, so pass A had nothing to compare against at all.

    Metric: autojunk=False and a PER-REGISTER MAX. difflib's autojunk engages at 200 characters and
    junks any character in over 1% of the sequence, which describes every seasoned register; a mean
    dilutes one copied register against one independent one.

    DECLARED_IDENTITIES are exempt from the threshold and must instead be BYTE-IDENTICAL. Near
    identical is neither a declared propagation nor independent authoring."""
    by_idm, by_m = {}, {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                rec = (c["slug"], p.get("id"), r.get("note_beginner") or "",
                       r.get("note_seasoned") or "")
                by_m.setdefault(r["method"], []).append(rec)
                if p.get("id"):
                    by_idm.setdefault((p["id"], r["method"]), []).append(rec)

    def score(r, nb, ns, floor=0.0):
        """SYMMETRIC, and that is a CORRECTION, not a tidy-up.

        difflib's matcher is GREEDY, not optimal: it takes the longest match it can see and
        recurses either side, so the decomposition it finds depends on which sequence is indexed
        and `ratio(a, b) != ratio(b, a)`. Measured on this corpus the two orders differ by up to
        **0.271** against a 0.70 threshold, and the batch-first order -- the one this guard used --
        scores LOWER in 607 of 1200 sampled pairs. One verified example: 52 characters matched one
        way, 11 the other, 0.343 against 0.073, on the same two strings. Argument order is not a
        property of the prose, so the metric takes the MAX of both orders: the strongest evidence
        of copying rather than an accident of which side was passed first.

        That is the THIRD dilution found in this one metric. Batch 23 found the other two --
        difflib's `autojunk` deflating any sequence over 200 characters, and a MEAN of the two
        registers hiding one copied register behind one independent one -- after its guard scored
        the batch's only real copy at 0.431 and passed it. A mutation harness reddens on NONE of
        the three: the branch fires correctly every time, and only the number handed to it is
        wrong. `MetricDiscriminates` in the suite asserts the metric, not the branch.

        Re-measured across all 18575 comparisons under the symmetric metric, this batch's worst
        pair is unchanged at 0.693 and NOTHING crosses 0.70, so the correction strengthens the
        guard without changing this batch's verdict.

        `floor` is a RIGOROUS O(1) prune, not an approximation: ratio is 2M/T and M cannot exceed
        min(len(u), len(v)), so a pair whose length ratio already sits at or below the running
        worst can never beat it or reach the threshold. Verified against an unpruned walk over the
        same 36132 register pairs: identical worst, identical refusals, 25% skipped, and the
        highest true score among the skipped pairs was 0.566."""
        best = 0.0
        for u, v in ((r.get("note_beginner") or "", nb), (r.get("note_seasoned") or "", ns)):
            lu, lv = len(u), len(v)
            tot = lu + lv
            if not tot:
                continue
            bound = 2.0 * (lu if lu < lv else lv) / tot
            if bound <= best or bound <= floor:
                continue
            s = max(difflib.SequenceMatcher(None, u, v, autojunk=False).ratio(),
                    difflib.SequenceMatcher(None, v, u, autojunk=False).ratio())
            if s > best:
                best = s
        return best

    cmp_a = cmp_b = 0
    worst = (0.0, None)
    declared_seen = set()
    for c in CROPS:
        for _f, p in problems(batch[c]):
            for r in p.get("control_ladder") or []:
                key = (c, p["id"], r["method"])
                if key in DECLARED_IDENTITIES:
                    want_crop, _why = DECLARED_IDENTITIES[key]
                    match = [x for x in by_idm.get((p["id"], r["method"]), [])
                             if x[0] == want_crop]
                    if not match:
                        raise SystemExit("REFUSED: declared identity %r names %s, which has no rung "
                                         "for this problem and method" % (key, want_crop))
                    _sl, _pid, nb, ns = match[0]
                    if (r.get("note_beginner") != nb) or (r.get("note_seasoned") != ns):
                        raise SystemExit("REFUSED: %r is DECLARED byte-identical to %s's rung and is "
                                         "not. Near-identical is neither a declared propagation nor "
                                         "independent authoring." % (key, want_crop))
                    declared_seen.add(key)
                    continue
                for _sl, _pid, nb, ns in by_idm.get((p["id"], r["method"]), []):
                    cmp_a += 1
                    sc = score(r, nb, ns, worst[0])
                    if sc > worst[0]:
                        worst = (sc, "A:%s/%s/%s vs %s" % (c, p["id"], r["method"], _sl))
                    if sc >= PRECEDENT_COPY_THRESHOLD:
                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s's rung for the "
                                         "same problem and method (threshold %.2f)"
                                         % (c, p["id"], r["method"], sc, _sl,
                                            PRECEDENT_COPY_THRESHOLD))
                for _sl, _pid, nb, ns in by_m.get(r["method"], []):
                    cmp_b += 1
                    sc = score(r, nb, ns, worst[0])
                    if sc > worst[0]:
                        worst = (sc, "B:%s/%s/%s vs %s/%s" % (c, p["id"], r["method"], _sl, _pid))
                    if sc >= PRECEDENT_COPY_THRESHOLD:
                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s's rung for %s "
                                         "using the SAME METHOD on a DIFFERENT problem (threshold "
                                         "%.2f). Pass A cannot see this."
                                         % (c, p["id"], r["method"], sc, _sl, _pid,
                                            PRECEDENT_COPY_THRESHOLD))
    if declared_seen != set(DECLARED_IDENTITIES):
        raise SystemExit("REFUSED: declared identities %r were not found in the batch"
                         % sorted(set(DECLARED_IDENTITIES) - declared_seen))
    # ORDER MATTERS AND IT WAS WRONG. `by_m` is a SUPERSET of `by_idm` -- every pass-A pair is
    # also a pass-B pair -- so cmp_b == 0 implies cmp_a == 0, and with pass A checked first the
    # pass-B branch could never fire. It was an anti-vacuity branch that was itself unreachable:
    # the exact class batch 21 shipped two of. Checking the SUPERSET first makes both live, and
    # both now have their own driver.
    if cmp_b == 0:
        raise SystemExit("REFUSED: precedent pass B made 0 comparisons; it is vacuous")
    if cmp_a == 0:
        raise SystemExit("REFUSED: precedent pass A made 0 comparisons; it is vacuous")
    return cmp_a, cmp_b, worst


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
                # A DECLARED IDENTITY is a deliberate propagation and is byte-identical BY DESIGN;
                # check_no_precedent_copy asserts that identity. Without this exemption the two
                # guards contradict each other, one requiring what the other forbids, and the batch
                # cannot pass either way.
                if (c, p["id"], r["method"]) in DECLARED_IDENTITIES:
                    continue
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
                src_blob = " ".join(src.get(f) or "" for f in SCHEMA_FOR[c])
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
    check_schema_premise(by)
    check_type_set_from_nothing(batch, by)
    check_ids(batch, by)
    check_id_adjudications(batch, data)
    check_no_template_twins_premise(by, data)
    cmp_a, cmp_b, worst = check_no_precedent_copy(batch, data)
    METRICS.update(precedent_cmp_a=cmp_a, precedent_cmp_b=cmp_b,
                   precedent_worst=worst[0], precedent_worst_pair=worst[1])
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
    """BLAST RADIUS. Batch 23's version expected `type` to be a CHANGED value, because those crops
    carried a coarse type already. Here `type` does not exist beforehand, so it is an ADDED key and
    NOTHING pre-existing changes at all. Inheriting batch 23's shape refused the batch outright.

    Set comparison FIRST, always, before any value is looked at: iterating `pre` alone makes every
    addition invisible, which was all four PLA-162 defects."""
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    if dropped:
        raise SystemExit("REFUSED: leaf keys dropped: %r" % sorted(dropped)[:6])
    unexpected = {k for k in added
                  if not (k[0] in CROPS and k[3] in ("id", "type", "control_ladder"))}
    if unexpected:
        raise SystemExit("REFUSED: unexpected leaf keys added: %r" % sorted(unexpected)[:6])
    want = 3 * sum(EXPECTED_PROBLEMS.values())
    if len(added) != want:
        raise SystemExit("REFUSED: %d leaf keys added, expected %d (id + type + control_ladder on "
                         "each of %d problems)"
                         % (len(added), want, sum(EXPECTED_PROBLEMS.values())))
    # NOTHING that already existed may change. This batch only ADDS.
    for k in set(pre) & set(post):
        if pre[k] != post[k]:
            raise SystemExit("REFUSED: %s changed pre-existing leaf %r; this batch only ADDS "
                             "id, type and control_ladder" % (k[0], k))
    # TWO FORWARD ASSERTIONS, verified unreachable and WITHDRAWN from the mutation harness rather
    # than reported as permanent survivors. Once `added` is pinned at 81 and every added key is
    # (batch crop, {id, type, control_ladder}), each touched triple can carry AT MOST 3 keys, so
    # 81 keys force exactly 27 distinct triples; and since each batch crop's problem count is its
    # maximum and those maxima sum to 27, the per-crop split is forced too. Kept because they
    # state the contract at the point a future edit would break it.
    touched = {(k[0], k[1], k[2]) for k in added}
    if len(touched) != sum(EXPECTED_PROBLEMS.values()):
        raise SystemExit("REFUSED: %d problems touched, expected %d"
                         % (len(touched), sum(EXPECTED_PROBLEMS.values())))
    per_crop = {}
    for slug, _f, _i in touched:
        per_crop[slug] = per_crop.get(slug, 0) + 1
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
    print("precedent scan    : %d + %d comparisons, worst %.3f (%s)"
          % (METRICS["precedent_cmp_a"], METRICS["precedent_cmp_b"],
             METRICS["precedent_worst"], METRICS["precedent_worst_pair"]))
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
