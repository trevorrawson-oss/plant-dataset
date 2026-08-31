#!/usr/bin/env python3
"""PLA-8 BATCH 16 -- COMPANIONS B: the batch that closes the Companion & Pollinator category.
Base 098dd0b1.

32 problems gain `id`, `type` and `control_ladder`; **88 rungs** across `echinacea` (15),
`bee-balm` (17), `chamomile` (16), `borage` (8) and `sweet-pea` (32). Roster laddered 68 -> 73,
and with this promote every Companion & Pollinator crop is laddered.

**NO CATALOG MUTATION.** Same note-shaped schema as batch 15, same schema premise guard.

--------------------------------------------------------------------------------------------------
THE SWEET-PEA TAXON RULING IS PINNED AS A REFUSAL
--------------------------------------------------------------------------------------------------
Sweet pea is *Lathyrus*, in the pea tribe but not a garden pea. Its root rots take the ornamental
complex id **`root-and-stem-rots`, NOT the peas' `root-rots-damping-off`** -- fava earned that
reuse on near-verbatim prose-twin evidence, and sweet-pea's prose is not a twin (a generic
Rhizoctonia/Pythium/Fusarium complex in its own words). The Fabeae kinship is still carried where
the prose carries it: the rotation rung restates "rotate off recent pea, bean, or sweet pea
ground" from the record itself. No pea-organism id appears anywhere (sweet-pea has no weevil
problem, so the *Bruchus* trap never arises).

--------------------------------------------------------------------------------------------------
MATERIALS ARE SCOPED PER LADDER, POLLINATOR TENSION FILED NOT SILENTLY RESOLVED
--------------------------------------------------------------------------------------------------
`MATERIAL_OK` maps every ladder allowed any soft_chemical/conventional rung to exactly the
materials its own note names; every other ladder must carry none. Sweet-pea's notes name
spinosad on thrips and caterpillars -- a real tension on a plant grown for bloom and the
pollinators it draws, resolved the chlorothalonil way: the crop's guidance names it, so the rung
ships with bee-timing framing in both registers, and the tension is FILED prominently rather
than resolved by silently dropping a named material.

--------------------------------------------------------------------------------------------------
THE INVERSION AND ANTI-RECOMMENDATION GUARDS CARRY OVER FROM BATCH 15
--------------------------------------------------------------------------------------------------
trap_cropping forbidden batch-wide; trap vocabulary (now including "decoy" -- borage's aphid note
describes decoy use) banned from every rung note, while "insectary" stays LEGAL: describing the
planting recruiting predators for its OWN pests is the placeable half, with no
destroy-the-planting implication. The lure-trap warning is REQUIRED on echinacea's
Japanese-beetle rung (its notes advise against bag-style traps; the first authoring pass dropped
the warning and the read restored it -- the exact class batch 15's pheromone guard exists for).

READ FIXES ALREADY IN STAGING: nine introduced 90°F figures trimmed to number-free heat cautions
(the batch-15 ruling; the crops' notes carry no figure), five real "never" tokens reworded, two
trim seams smoothed, the echinacea lure-trap warning restored.

REFUSALS: base SHA mismatch; a target without its note pair; any crop already laddered; an id off
the convention table; the sweet-pea pea-id refusal in either direction; a reused id resolving
nowhere or a new id already taken; trap_cropping anywhere; banned vocabulary in any note; the
echinacea lure-trap warning missing; a material outside its ladder's MATERIAL_OK set; a forbidden
method; the alignment correspondence broken either way; a shipped-rung echo; unknown method; tier
decrease; applies_to incoherence; identical registers; duplicate method; empty ladder; counts
off; ANY change to control_methods, source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch16.py
Mutation harness: tools/mutate_pla8_batch16_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch16.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch16_companions_b")
BASE_SHA = "098dd0b18cc85aebf05bbb50071ab9ba1c50bf377afb1235d9359cc07d894bfa"

CROPS = ("echinacea", "bee-balm", "chamomile", "borage", "sweet-pea")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"echinacea": 8, "bee-balm": 5, "chamomile": 6, "borage": 3, "sweet-pea": 10}
EXPECTED_RUNGS = {"echinacea": 15, "bee-balm": 17, "chamomile": 16, "borage": 8, "sweet-pea": 32}

ADVICE_FIELDS = ("note_beginner", "note_seasoned")

ID_CONVENTION = {
    "Anthracnose and leaf spots": "anthracnose",
    "Aphids": "aphids",
    "Aster yellows": "aster-yellows",
    "Bacterial and fungal leaf spots": "leaf-spots",
    "Botrytis (gray mold)": "gray-mold",
    "Caterpillars and leafminers": "caterpillars",
    "Crown and root rot in wet soil": "root-and-stem-rots",
    "Damping-off (seedlings)": "damping-off",
    "Downy mildew": "downy-mildew",
    "Eriophyid mites": "eriophyid-mites",
    "Japanese beetles": "japanese-beetles",
    "Mealybugs": "mealybugs",
    "Mosaic and spotted-wilt viruses": "mosaic-viruses",
    "Powdery mildew": "powdery-mildew",
    "Rabbits and deer": "rabbits-and-deer",
    "Root and stem rot in wet soil": "root-and-stem-rots",
    "Root, stem, and crown rots": "root-and-stem-rots",
    "Rust": "bee-balm-rust",
    "Slugs and snails": "slugs-and-snails",
    "Spider mites": "spider-mites",
    "Stalk borer": "stalk-borer",
    "Thrips": "thrips",
    "Thrips (including western flower thrips)": "thrips",
}

# The sweet-pea ruling: the peas' id was earned by fava on prose-twin evidence; sweet-pea's rot
# prose is not a twin, so tribe kinship alone does not carry the string.
TAXON_REFUSED = {
    "root-and-stem-rots": ("root-rots-damping-off",
                           "the peas' id, reused by fava only on near-verbatim prose-twin "
                           "evidence; sweet-pea's rot prose is its own generic complex, and "
                           "Fabeae kinship alone does not carry the join key"),
}

REUSED_IDS = ("aphids", "thrips", "spider-mites", "slugs-and-snails", "powdery-mildew",
              "gray-mold", "damping-off", "root-and-stem-rots", "japanese-beetles",
              "leaf-spots", "aster-yellows", "mosaic-viruses", "anthracnose", "downy-mildew")
NEW_IDS = ("eriophyid-mites", "rabbits-and-deer", "stalk-borer", "bee-balm-rust", "mealybugs",
           "caterpillars")

NOTE_BANNED = ("trap crop", "trap-crop", "sacrificial", "banker", "decoy")
# echinacea's notes advise against bag-style lure traps; the rung must keep the warning.
LURE_WARNED = (("echinacea", "japanese-beetles", "handpick"),)

FORBIDDEN_METHODS = {
    "trap_cropping": "the companion inversion holds for this batch too",
    "disease_escape_sowing": "no note states a sow-early fungal escape",
    "planting_time_avoidance": "no note states a published pest window",
    "pyrethroid": "no note names a conventional insecticide",
    "carbaryl": "no note names a conventional insecticide",
    "chlorothalonil": "no note names any conventional fungicide",
    "mancozeb": "no note names any conventional fungicide",
    "copper_fungicide": "no note names copper",
    "sulfur": "no note names sulfur",
    "biofungicide": "no note names a biofungicide",
    "neem_oil": "no note names neem",
}

# Every ladder allowed any soft_chemical/conventional rung, with exactly the materials its own
# note names. Every ladder NOT listed here must carry no material rung at all.
MATERIAL_OK = {
    ("echinacea", "aphids"): {"insecticidal_soap"},
    ("bee-balm", "spider-mites"): {"insecticidal_soap", "horticultural_oil"},
    ("bee-balm", "aphids"): {"insecticidal_soap", "horticultural_oil"},
    ("chamomile", "aphids"): {"insecticidal_soap"},
    ("chamomile", "thrips"): {"insecticidal_soap"},
    ("chamomile", "mealybugs"): {"insecticidal_soap"},
    ("borage", "aphids"): {"insecticidal_soap"},
    ("sweet-pea", "aphids"): {"insecticidal_soap", "horticultural_oil"},
    ("sweet-pea", "thrips"): {"insecticidal_soap", "spinosad"},
    ("sweet-pea", "spider-mites"): {"insecticidal_soap", "horticultural_oil"},
    ("sweet-pea", "slugs-and-snails"): {"iron_phosphate_slug_bait"},
    ("sweet-pea", "caterpillars"): {"spinosad"},
}

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
    for slug in CROPS:
        for _, p in problems(by[slug]):
            for f in ADVICE_FIELDS:
                if not str(p.get(f) or "").strip():
                    return (f"{slug}/{p.get('name')!r} has no {f}; the companion schema premise "
                            f"has drifted and every prose comparison below would be vacuous")
    return None


def check_alignment(by, batch):
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
            return f"a problem carries {wrong!r}, which is the WRONG JOIN KEY: {why}"
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
            allowed = MATERIAL_OK.get((slug, pid), set())
            for m in lad:
                if m in cm and cm[m]["tier"] in MATERIAL_TIERS and m not in allowed:
                    return (f"{slug}/{pid} carries material {m!r}, which its own note does not "
                            f"name; the batch scopes every material to the ladders that earn it")
            for r in p.get("control_ladder") or []:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                for word in NOTE_BANNED:
                    if word in blob:
                        return (f"{slug}/{pid}: a note mentions {word!r}. The companion "
                                f"inversion holds: unplaced trap/decoy content must not creep "
                                f"back through a note")
    for slug, pid, method in LURE_WARNED:
        ms, p = ladder_of(batch[slug], pid)
        if ms is None or method not in ms:
            return f"{slug}/{pid} lost its {method} rung"
        r = next(r for r in p["control_ladder"] if r["method"] == method)
        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
        if "trap" not in blob:
            return (f"{slug}/{pid}: the {method} rung dropped the crop's own avoid-lure-traps "
                    f"warning, a do-not-do with no token to scan for once it is gone")
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
    # No batch-total rung check: the per-crop counts above sum to the total identically, so a
    # total branch could never fire on its own (the trap-round rule: deleted, not phantom).
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
            allowed = MATERIAL_OK.get((slug, pid), set())
            for m in lad:
                if m in cm and cm[m]["tier"] in MATERIAL_TIERS and m not in allowed:
                    return f"post: {slug}/{pid} shipped unearned material {m!r}"
            for r in p.get("control_ladder") or []:
                blob = ((r.get("note_beginner") or "") + " " + (r.get("note_seasoned") or "")).lower()
                for word in NOTE_BANNED:
                    if word in blob:
                        return f"post: {slug}/{pid}: a shipped note mentions {word!r}"
    for slug, pid, method in LURE_WARNED:
        ms, p = ladder_of(by[slug], pid)
        if ms is None or method not in ms:
            return f"post: {slug}/{pid} shipped without its {method} rung"
        r = next(r for r in p["control_ladder"] if r["method"] == method)
        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
        if "trap" not in blob:
            return f"post: {slug}/{pid} shipped without the lure-trap warning"
    shipped = {p["id"] for slug in CROPS for _, p in problems(by[slug])}
    # Batch 15 could delete this branch because every new id doubled as a per-id lookup key;
    # here only japanese-beetles does, so the other five need their own shipped check.
    for pid in NEW_IDS:
        if pid not in shipped:
            return f"post: new id {pid!r} did not ship"
    for right, (wrong, _why) in TAXON_REFUSED.items():
        if wrong in shipped:
            return f"post: {wrong!r} shipped, the wrong join key"

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

    print("PLA-8 BATCH 16 -- COMPANIONS B: the Companion & Pollinator category closes")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted ({len(NEW_IDS)} new to the roster)")
    print(f"  catalog      : UNTOUCHED")
    print(f"  taxon ruling : sweet-pea takes root-and-stem-rots, NOT the peas' "
          f"root-rots-damping-off (no prose twin)")
    print(f"  materials    : scoped per ladder to what each note names; spinosad tension FILED")
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
