#!/usr/bin/env python3
"""PLA-8 BATCH 15 -- COMPANIONS A: the first Companion & Pollinator batch. Base c76f14f1.

33 problems gain `id`, `type` and `control_ladder`; **84 rungs** across `marigold` (19), `zinnia`
(13), `cosmos` (16), `calendula` (18) and `sweet-alyssum` (18). Roster laddered 63 -> 68.
Sequenced per Trevor's 2026-08-31 ruling lifting the companions deferral.

**NO CATALOG MUTATION.** `control_methods` and `source_catalog` come out byte-identical.

--------------------------------------------------------------------------------------------------
THE THIRD SCHEMA, AND THE PREMISE THAT KEEPS EVERY DOWNSTREAM CHECK HONEST
--------------------------------------------------------------------------------------------------
These five crops carry their prose in `note_beginner`/`note_seasoned` ONLY -- no prevention_*, no
management_*, no per-problem sources. `check_schema_premise` asserts every canonical target
problem carries a non-empty note pair, because with empty advice fields the alignment
correspondence would compare tuples of None and pass vacuously (the exact blind spot the
ladder_batch note-schema fix closed for the family cut). Measured before authoring: ZERO
byte-identical note pairs across the five crops, so every ladder is authored per-crop and no
propagation group exists.

--------------------------------------------------------------------------------------------------
THE COMPANION INVERSION IS THE BATCH'S SIGNATURE HAZARD, GUARDED THREE WAYS
--------------------------------------------------------------------------------------------------
These are the crops OTHER plantings use as trap, banker and insectary stands. zinnia's
Japanese-beetle record is a documented INVERTED exclusion from the trap-cropping round ("zinnias
are a known preferred host, which is part of their trap-crop value"), and calendula's aphid note
describes the crop "sometimes grown as a deliberate trap or banker plant". A trap_cropping rung
on any of these tells the reader to destroy the crop they are growing. So:

  1. `trap_cropping` is FORBIDDEN batch-wide.
  2. No rung note may carry trap vocabulary at all (NOTE_BANNED: "trap crop", "trap-crop",
     "sacrificial", "banker"): unplaced content stays unplaced, and a note alluding to trap value
     is how it would creep back.
  3. The half of the insectary story that IS placeable stays placed: alyssum, marigold, zinnia,
     cosmos and calendula recruit predators that suppress their OWN aphids, and those
     `beneficial_predators` rungs are conservation, not conversion.

The pheromone-trap warning cuts the other way and is REQUIRED: both Japanese-beetle records
advise avoiding pheromone traps (they concentrate beetles), and each `handpick` rung must keep
that anti-recommendation ("pheromone" present in the rung), because dropping a crop's own
do-not-do advice is a defect with no token to scan for once it is gone.

--------------------------------------------------------------------------------------------------
IDS AND THE ONE TAXON REFUSAL
--------------------------------------------------------------------------------------------------
**`zinnia-leaf-spots`, NOT `alternaria-leaf-spot`.** Zinnia's spotting is *Alternaria zinniae*
plus *Xanthomonas* -- both zinnia-scoped species -- while the roster's `alternaria-leaf-spot` is
the brassica *A. brassicicola* on seven cole crops. The species-scoped mint follows the
rust-id precedent. `gray-mold` (marigold + cosmos, one string, *Botrytis cinerea*) reuses
strawberry's id; the roster's OTHER Botrytis string (artichoke's `botrytis-gray-mold`) is a
pre-existing divergence FILED by this round, not resolved by it. sweet-alyssum reuses
`cabbageworms` (it is a brassica; same complex) and the alyssum/calendula/marigold rot records
reuse `root-and-stem-rots` / `damping-off` per the lead-name convention.

--------------------------------------------------------------------------------------------------
MATERIALS: THREE EARNED, EVERYTHING ELSE ABSENT
--------------------------------------------------------------------------------------------------
The only materials any note names are insecticidal soap, Bt (alyssum's caterpillars, with the
butterfly-host group caution kept) and iron phosphate bait. Every disease ladder in the batch
ends cultural -- no note names a fungicide of any kind -- and `FORBIDDEN_METHODS` refuses the
entire unearned material list plus the timing/escape keys. Read fixes already applied to staging:
two introduced 90°F figures removed from calendula's soap rungs (the number is standard label
advice but appears nowhere in this crop's notes), and the dubious raise-humidity-by-base-watering
mechanism trimmed from two mite rungs (kept in the SOURCE notes, filed as a prose tension; the
rungs keep the well-supported drought-stress half).

REFUSALS: base SHA mismatch; a target problem without its note pair; any crop already laddered;
an id off the convention table; the zinnia taxon refusal in either direction; a reused id that
resolves nowhere or a new id already taken; trap_cropping anywhere; a banned trap token in any
note; a Japanese-beetle handpick rung losing its pheromone warning; a forbidden method anywhere;
a material on a no-material ladder; the alignment correspondence broken either way; a
shipped-rung echo; unknown method; tier decrease; applies_to incoherence; identical registers;
duplicate method; empty ladder; counts off; ANY change to control_methods, source_catalog, or a
bystander crop.

Guard suite:      tools/test_promote_pla8_batch15.py
Mutation harness: tools/mutate_pla8_batch15_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch15.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch15_companions_a")
BASE_SHA = "c76f14f19f4d2aa208748d0609f14a86bb5753c57fb21840f826e6a9d37599a0"

CROPS = ("marigold", "zinnia", "cosmos", "calendula", "sweet-alyssum")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"marigold": 8, "zinnia": 5, "cosmos": 7, "calendula": 6, "sweet-alyssum": 7}
EXPECTED_RUNGS = {"marigold": 19, "zinnia": 13, "cosmos": 16, "calendula": 18, "sweet-alyssum": 18}

# The companion schema: the ONLY advice-bearing fields on these crops.
ADVICE_FIELDS = ("note_beginner", "note_seasoned")

ID_CONVENTION = {
    "Alternaria and bacterial leaf spot": "zinnia-leaf-spots",
    "Aphids": "aphids",
    "Aster leafhoppers": "aster-leafhoppers",
    "Aster yellows": "aster-yellows",
    "Botrytis blight (gray mold)": "gray-mold",
    "Cabbage-family caterpillars": "cabbageworms",
    "Cucumber mosaic and aster yellows": "cucumber-mosaic",
    "Damping-off": "damping-off",
    "Damping-off and root or stem rot": "damping-off",
    "Downy mildew": "downy-mildew",
    "Flea beetles": "flea-beetles",
    "Gray mold (Botrytis)": "gray-mold",
    "Japanese beetles": "japanese-beetles",
    "Leaf spots and powdery mildew": "leaf-spots",
    "Powdery mildew": "powdery-mildew",
    "Root, stem, and crown rot (damping-off)": "root-and-stem-rots",
    "Slugs and snails": "slugs-and-snails",
    "Spider mites": "spider-mites",
    "Stem canker": "stem-canker",
    "Stem, crown, and root rot": "root-and-stem-rots",
    "Whiteflies": "whiteflies",
}

# zinnia's spotting is A. zinniae + Xanthomonas (zinnia-scoped); the roster string names the
# brassica organism on seven cole crops.
TAXON_REFUSED = {
    "zinnia-leaf-spots": ("alternaria-leaf-spot",
                          "the roster's alternaria-leaf-spot is Alternaria brassicicola on the "
                          "brassicas; zinnia's is A. zinniae plus Xanthomonas, zinnia-scoped "
                          "species"),
}

REUSED_IDS = ("aphids", "spider-mites", "slugs-and-snails", "aster-yellows", "powdery-mildew",
              "gray-mold", "root-and-stem-rots", "damping-off", "whiteflies", "flea-beetles",
              "downy-mildew", "cabbageworms")
NEW_IDS = ("japanese-beetles", "leaf-spots", "zinnia-leaf-spots", "aster-leafhoppers",
           "stem-canker", "cucumber-mosaic")

# THE COMPANION INVERSION. These crops ARE the trap/banker/insectary stands other plantings use;
# a trap rung, or trap vocabulary in a note, tells the reader to destroy the crop they grow.
NOTE_BANNED = ("trap crop", "trap-crop", "sacrificial", "banker")
# Both Japanese-beetle records advise AGAINST pheromone traps; the handpick rung must keep it.
PHEROMONE_WARNED = (("marigold", "japanese-beetles"), ("zinnia", "japanese-beetles"))

FORBIDDEN_METHODS = {
    "trap_cropping": "the companion inversion: these crops ARE trap plants, and the method's "
                     "meaning ends in destroying the planting",
    "disease_escape_sowing": "no companion note states a sow-early fungal escape",
    "planting_time_avoidance": "no companion note states a published pest window",
    "pyrethroid": "no note names a conventional insecticide",
    "carbaryl": "no note names a conventional insecticide",
    "chlorothalonil": "no companion note names any fungicide",
    "mancozeb": "no companion note names any fungicide",
    "copper_fungicide": "no companion note names any fungicide",
    "sulfur": "no companion note names any fungicide",
    "biofungicide": "no companion note names any fungicide",
    "spinosad": "no companion note names this material",
    "neem_oil": "no companion note names this material",
    "horticultural_oil": "no companion note names this material",
}

# Ladders whose notes name no soft_chemical/conventional material at all.
NO_MATERIAL = (
    ("marigold", "japanese-beetles"), ("marigold", "gray-mold"), ("marigold", "leaf-spots"),
    ("marigold", "root-and-stem-rots"), ("marigold", "aster-yellows"),
    ("zinnia", "japanese-beetles"), ("zinnia", "spider-mites"),
    ("zinnia", "powdery-mildew"), ("zinnia", "zinnia-leaf-spots"),
    ("cosmos", "aster-leafhoppers"), ("cosmos", "spider-mites"), ("cosmos", "aster-yellows"),
    ("cosmos", "powdery-mildew"), ("cosmos", "gray-mold"), ("cosmos", "stem-canker"),
    ("calendula", "powdery-mildew"), ("calendula", "damping-off"),
    ("calendula", "cucumber-mosaic"),
    ("sweet-alyssum", "flea-beetles"), ("sweet-alyssum", "root-and-stem-rots"),
    ("sweet-alyssum", "downy-mildew"), ("sweet-alyssum", "damping-off"),
)

TIER_RANK = {t: i for i, t in enumerate(TIERS)}
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


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def problems(obj):
    return [(fam, p) for fam in ("pests", "diseases") for p in (obj.get(fam) or [])
            if isinstance(p, dict)]


def rung_count(batch):
    return sum(len(p.get("control_ladder") or []) for s in CROPS for _, p in problems(batch[s]))


def ladder_of(obj, pid):
    for _, p in problems(obj):
        if p.get("id") == pid:
            return [r["method"] for r in p.get("control_ladder") or []], p
    return None, None


def roster_ids(data):
    return {p["id"] for c in data["crops"] for _, p in problems(c) if p.get("id")}


def advice_key(p):
    return json.dumps([p.get(f) for f in ADVICE_FIELDS], ensure_ascii=False)


def ladder_key(p):
    return json.dumps([(r["method"], r["note_beginner"], r["note_seasoned"])
                       for r in p.get("control_ladder") or []], ensure_ascii=False)


def check_schema_premise(by):
    """Every target problem must carry the note pair, or the alignment correspondence compares
    tuples of None and goes vacuous -- the blind spot the ladder_batch note-schema fix closed."""
    for slug in CROPS:
        for _, p in problems(by[slug]):
            for f in ADVICE_FIELDS:
                if not str(p.get(f) or "").strip():
                    return (f"{slug}/{p.get('name')!r} has no {f}; the companion schema premise "
                            f"has drifted and every prose comparison below would be vacuous")
    return None


def check_alignment(by, batch):
    """Identical note prose + same id <-> identical ladder, both directions (batches 13/14).
    Measured at authoring: no identical pair exists, so the fork direction currently REFUSES
    nothing -- it is the standing guard for the day two companion notes converge."""
    rows = []
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            rows.append((slug, p.get("id"), advice_key(canon[idx][1]), ladder_key(p)))
    for i, (s1, id1, a1, l1) in enumerate(rows):
        for s2, id2, a2, l2 in rows[i + 1:]:
            if id1 == id2 and a1 == a2 and l1 != l2:
                return (f"{s1}/{id1} and {s2}/{id2} carry byte-identical note prose but "
                        f"different ladders; identical prose ships one text set")
            if l1 == l2 and a1 != a2:
                return (f"{s1}/{id1} and {s2}/{id2} share a byte-identical ladder but their "
                        f"note prose differs, so one crop is being given the other's source")
    return None


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 25]


def shipped_notes(data):
    whole, sent = {}, {}
    for c in data["crops"]:
        for _, p in problems(c):
            for r in p.get("control_ladder") or []:
                for k in ("note_beginner", "note_seasoned"):
                    v = r.get(k)
                    if not v:
                        continue
                    whole.setdefault(v, f"{c.get('slug')}/{p.get('id')}/{r['method']}")
                    for s in sentences(v):
                        sent.setdefault(s, f"{c.get('slug')}/{p.get('id')}/{r['method']}")
    return whole, sent


def check_no_shipped_echo(batch, data):
    whole, sent = shipped_notes(data)
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            for r in p.get("control_ladder") or []:
                where = f"{slug}/{p.get('id')}/{r['method']}"
                for k in ("note_beginner", "note_seasoned"):
                    n = r.get(k) or ""
                    if n in whole:
                        return f"{where}: {k} is byte-identical to the shipped {whole[n]}"
                    for s in sentences(n):
                        if s in sent and len(s.split()) >= 10:
                            return (f"{where}: {k} shares a {len(s.split())}-word sentence with "
                                    f"the shipped {sent[s]}: {s!r}")
    return None


def check_read_fixes(batch, by, data):
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return f"{slug}: problem {name!r} is not in the id-convention table"
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention "
                        f"ships {want!r}; ids are join keys and are never re-derived from the "
                        f"name")

    staged_ids = {p["id"] for slug in CROPS for _, p in problems(batch[slug])}
    for right, (wrong, why) in TAXON_REFUSED.items():
        if right not in staged_ids:
            return f"the taxon ruling requires id {right!r}, which no problem in this batch carries"
        if wrong in staged_ids:
            return f"a problem carries {wrong!r}, which is the WRONG ORGANISM: {why}"
    base_ids = roster_ids(data)
    for pid in REUSED_IDS:
        if pid in staged_ids and pid not in base_ids:
            return (f"{pid!r} is declared a REUSE but resolves nowhere on the roster, so this "
                    f"would be a mint wearing a reuse's name")
    for pid in NEW_IDS:
        if pid in base_ids:
            return f"{pid!r} is already on the roster; it is listed as new to this base"

    cm = data["control_methods"]
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            for m, why in FORBIDDEN_METHODS.items():
                if m in lad:
                    return f"{slug}/{pid} carries {m!r}: {why}"
            for r in p.get("control_ladder") or []:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                for word in NOTE_BANNED:
                    if word in blob:
                        return (f"{slug}/{pid}: a note mentions {word!r}. The companion crops "
                                f"ARE the trap and banker stands other plantings use; that "
                                f"content is deliberately unplaced and must not creep back "
                                f"through a note")
    for slug, pid in PHEROMONE_WARNED:
        ms, p = ladder_of(batch[slug], pid)
        if ms is None or "handpick" not in ms:
            return f"{slug}/{pid} lost its handpick rung"
        r = next(r for r in p["control_ladder"] if r["method"] == "handpick")
        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
        if "pheromone" not in blob:
            return (f"{slug}/{pid}: the handpick rung dropped the crop's own avoid-pheromone-"
                    f"traps warning, a do-not-do with no token to scan for once it is gone")
    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(batch[slug], pid)
        if ms is None:
            return f"{slug} has no {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return (f"{slug}/{pid} carries {m!r} ({cm[m]['tier']}), but its notes name no "
                        f"such material")
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    for crop in CROPS:
        n_prob = 0
        for _, p in problems(batch[crop]):
            n_prob += 1
            if not p.get("id") or not p.get("type"):
                return f"{crop}: a problem is missing id or type"
            lad = p.get("control_ladder")
            if lad is None:
                return f"{crop}/{p.get('id')}: no control_ladder"
            if not lad:
                return f"{crop}/{p.get('id')}: control_ladder is EMPTY"
            tiers, seen = [], set()
            for i, r in enumerate(lad):
                m = r.get("method")
                if m not in cm:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                if m in seen:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} appears twice in one ladder"
                seen.add(m)
                targets = TYPE_TARGETS.get(p.get("type")) or set()
                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):
                    return (f"{crop}/{p.get('id')}#{i}: {m!r} applies_to "
                            f"{sorted(cm[m]['applies_to'])} cannot reach type {p.get('type')!r}")
                for k in ("note_beginner", "note_seasoned"):
                    if not str(r.get(k) or "").strip():
                        return f"{crop}/{p.get('id')}#{i}: {k} missing or empty"
                if r["note_beginner"] == r["note_seasoned"]:
                    return f"{crop}/{p.get('id')}#{i}: registers are identical"
                for k in ("note_beginner", "note_seasoned"):
                    bad = hygiene(r[k])
                    if bad:
                        return f"{crop}/{p.get('id')}#{i}: {k} fails copy hygiene ({bad})"
                tiers.append(TIER_RANK[cm[m]["tier"]])
            if tiers != sorted(tiers):
                return f"{crop}/{p.get('id')}: tiers decrease {tiers}"
        if n_prob != EXPECTED_PROBLEMS[crop]:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS[crop]}"
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    problem = check_schema_premise(by)
    if problem:
        return problem
    batch = staged()
    for slug in CROPS:
        a, b = len(problems(batch[slug])), len(problems(by[slug]))
        if a != b:
            return f"{slug}: staged {a} problems, canonical {b}"
    for problem in (check_read_fixes(batch, by, data), check_alignment(by, batch),
                    check_no_shipped_echo(batch, data)):
        if problem:
            return problem
    problem = validate_batch(batch, cm)
    if problem:
        return problem
    for slug in CROPS:
        n = sum(len(p.get("control_ladder") or []) for _, p in problems(batch[slug]))
        if n != EXPECTED_RUNGS[slug]:
            return f"{slug}: {n} rungs, expected {EXPECTED_RUNGS[slug]}"
    if rung_count(batch) != sum(EXPECTED_RUNGS.values()):
        return f"rung count {rung_count(batch)}, expected {sum(EXPECTED_RUNGS.values())}"
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"crops": {c.get("slug"): dump(c) for c in data["crops"]},
            "methods": dump(data["control_methods"]),
            "sources": dump(data["source_catalog"])}


def apply_to(data):
    batch = staged()
    by = {c.get("slug"): c for c in data["crops"]}
    minted = reused = 0
    for slug in CROPS:
        crop = by[slug]
        for fam in ("pests", "diseases"):
            adds = [p for p in (batch[slug].get(fam) or []) if isinstance(p, dict)]
            for i, add in enumerate(adds):
                tgt = crop[fam][i]
                if isinstance(tgt.get("id"), str) and tgt["id"]:
                    reused += 1
                else:
                    tgt["id"] = add["id"]
                    minted += 1
                tgt["type"] = add["type"]
                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])
    return minted, reused, rung_count(batch)


def verify_post(pre, data):
    by = {c.get("slug"): c for c in data["crops"]}
    cm = data["control_methods"]
    post = snapshot(data)

    for slug in CROPS:
        for _, p in problems(by[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{pid}: no ladder after promote"
            for m in FORBIDDEN_METHODS:
                if m in lad:
                    return f"post: {slug}/{pid} shipped forbidden {m!r}"
            for r in p.get("control_ladder") or []:
                blob = ((r.get("note_beginner") or "") + " " + (r.get("note_seasoned") or "")).lower()
                for word in NOTE_BANNED:
                    if word in blob:
                        return f"post: {slug}/{pid}: a shipped note mentions {word!r}"
    for slug, pid in PHEROMONE_WARNED:
        ms, p = ladder_of(by[slug], pid)
        if ms is None or "handpick" not in ms:
            return f"post: {slug}/{pid} shipped without its handpick rung"
        r = next(r for r in p["control_ladder"] if r["method"] == "handpick")
        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
        if "pheromone" not in blob:
            return f"post: {slug}/{pid} shipped without the pheromone-trap warning"
    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(by[slug], pid)
        if ms is None:
            return f"post: {slug} lost its {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return f"post: {slug}/{pid} shipped {m!r}, which its notes rule out"
    # THERE IS NO "new id did not ship" CHECK HERE, and its absence is deliberate: every one of
    # this batch's six new ids is also the key of a NO_MATERIAL or PHEROMONE_WARNED lookup above,
    # so an id that vanished always trips "lost its <id> problem" first and the branch could
    # never fire on its own. An unreachable branch reads as coverage while providing none (the
    # trap-cropping round's rule); the per-id lookups are the real protection.
    shipped = {p["id"] for slug in CROPS for _, p in problems(by[slug])}
    for right, (wrong, _why) in TAXON_REFUSED.items():
        if wrong in shipped:
            return f"post: {wrong!r} shipped, the wrong organism"

    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints and widens NOTHING"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"
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
    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    pre = snapshot(data)
    minted, reused, rungs = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 BATCH 15 -- COMPANIONS A: marigold, zinnia, cosmos, calendula, sweet-alyssum")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted ({len(NEW_IDS)} new to the roster)")
    print(f"  catalog      : UNTOUCHED -- no mint, no widening")
    print(f"  inversion    : trap_cropping forbidden batch-wide; trap vocabulary banned from "
          f"notes; the pheromone anti-recommendation REQUIRED on both Japanese-beetle rungs")
    print(f"  materials    : soap, bt, iron phosphate only; every disease ladder ends cultural")
    print(f"  blast radius : 5 crops; methods 0; sources 0; bystanders 0")
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
