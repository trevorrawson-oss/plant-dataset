#!/usr/bin/env python3
"""PLA-8 BATCH 11 -- ALLIUMS + FALL HERBS, fourth batch of the fall block. Base 96cbc68c.

24 problems gain `id`, `type` and `control_ladder`; **81 rungs** across `garlic` (21),
`spring-onion` (16), `dill` (19) and `cilantro-coriander` (25). ONE method WIDENED:
`certified_clean_stock` reaches `nematode`. Roster laddered 46 -> 50.

RE-PINNED 2026-08-28 from base be444e25 onto 96cbc68c, the trap_cropping backfill's output. The
transform is unchanged; only the base moved. `trap_cropping` is now a legal catalog key, and this
batch's standing refusal of it still holds: dill's parsleyworm is relocation-for-CONSERVATION.

--------------------------------------------------------------------------------------------------
THE WIDENING, AND THE CONTROL IT UNBLOCKS
--------------------------------------------------------------------------------------------------
**`certified_clean_stock` WAS ILLEGAL FOR `type: nematode`.** Its applies_to covered viral,
bacterial and the two fungal classes with no `nematode` and no `any`, leaving exactly five methods
legal for a nematode problem. Garlic's stem and bulb nematode prose calls clean, tested,
nematode-free seed stock **"the single most important practice"** and says the pest usually
arrives inside infected cloves -- so the crop's PRIMARY control had nowhere to go.

**WIDENED RATHER THAN MINTED, because the method's own action already is the one the crop needs:**
buy clean stock once, at purchase, before anything is in the ground. Per the r5 rule (G5) a
widening carries its PROSE with it, so `best_use` and `how_it_works_seasoned` now name
planting-stock-borne nematodes rather than implying diseases only. The new rung also preserves a
fact the prose is careful about: **hot-water seed dips are NO LONGER recommended**, because they
reduce the nematode without clearing it -- advice a reader may well meet elsewhere.

--------------------------------------------------------------------------------------------------
THE FIRST MIXED-SCHEMA BATCH
--------------------------------------------------------------------------------------------------
`garlic` and `spring-onion` carry `identification_*` / `management_*` prose fields; `dill` and
`cilantro-coriander` carry the classic `symptoms_*` / `organic_treatment_*` / `prevention_*` set.
**`PROSE_FIELDS` therefore spans BOTH schemas.** Comparing only the classic names would make
`prose_signature` all-None for the two alliums and the twins check VACUOUS for them. Measured
2026-08-28: 12 crops use the newer schema (all 5 alliums, all 7 microgreens), 93 use the classic,
none mix the two, and **none of the 12 had been laddered before this batch**, so no shipped
promote was affected. The remaining alliums and every microgreen batch will hit this.

--------------------------------------------------------------------------------------------------
THE READ'S RULINGS
--------------------------------------------------------------------------------------------------
**COPPER OFF cilantro's bacterial leaf spot.** Its beginner register says flatly "There is no
spray cure in the home garden, so prevention matters most", and the seasoned one names copper only
to bound it ("copper has limited effect once it is established"). A mention that limits is not a
recommendation -- the same shape as spinach's downy mildew in batch 8, ruled the same way.

**dill KEEPS `water_at_the_base` on powdery mildew.** Eight shipped crops already pair those two,
so dropping it would make dill the outlier. Recorded separately: that method's stated mechanism is
splash dispersal, which powdery mildew does not use, so nine crops now rest on it -- a catalog
SCOPE question, not this batch's to fix.

**THE ALLIUM IDS AGREED WITHOUT COORDINATION.** garlic and spring-onion were authored in parallel
and independently minted the same strings for all five shared problems (`onion-thrips`,
`onion-maggot`, `white-rot`, `fusarium-basal-rot`, `botrytis-neck-rot`). This batch is the FIRST
allium ever laddered, so these ids become the convention `onion`, `leek` and `shallot` inherit; a
split at birth would have been expensive and is pinned against here.

**cilantro's `leafhoppers` is MINTED, not carrot's `aster-yellows` REUSED.** Carrot's is a
`diseases[]` entry for the phytoplasma; cilantro's is a `pests[]` entry for the vector, naming two
diseases parenthetically. Reusing would cross a disease id onto an insect record. Its `soft-rot`
DOES reuse cauliflower's `bacterial-soft-rot` -- same Pectobacterium, same wound entry.

REFUSALS: base SHA mismatch; the widening already applied, or disagreeing with its staged spec; a
crop already laddered; an id off the convention; the two alliums disagreeing on a shared id;
copper on cilantro's bacterial leaf spot; garlic's nematode ladder without its clean-stock rung, or
a note resurrecting hot-water dips; `planting_time_avoidance` anywhere in this batch; `handpick` on
a leaf-removal target; any "diatomaceous"/"trap crop"/"pyrethroid" in a note; an unknown method; a
tier decrease; applies_to incoherence; identical registers; counts off; any pair of staged files
byte-identical; any bystander crop, other method, or source changed.

Guard suite:      tools/test_promote_pla8_batch11.py
Mutation harness: tools/mutate_pla8_batch11_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch11.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch11_alliums_herbs")
BASE_SHA = "96cbc68c7f8a1509bf922e85ad424d6a55a3f1c2a45d6288bfa5ba16a2bec67a"

CROPS = ("garlic", "spring-onion", "dill", "cilantro-coriander")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"garlic": 7, "spring-onion": 6, "dill": 5, "cilantro-coriander": 6}
EXPECTED_RUNGS = {"garlic": 21, "spring-onion": 16, "dill": 19, "cilantro-coriander": 25}

# BOTH SCHEMAS. The alliums have no symptoms_/organic_treatment_/prevention_ fields at all, so a
# classic-only list would make prose_signature all-None for them and the twins check vacuous.
PROSE_FIELDS = ("name", "severity", "sources",
                "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "identification_beginner", "identification_seasoned",
                "management_beginner", "management_seasoned")
NEW_SCHEMA_CROPS = ("garlic", "spring-onion")

ID_CONVENTION = {
    "Allium leafminer": "allium-leafminer",
    "Aphids": "aphids",
    "Bacterial leaf spot": "bacterial-leaf-spot",
    "Botrytis neck rot": "botrytis-neck-rot",
    "Damping-off and seedling rot": "damping-off",
    "Fusarium basal rot": "fusarium-basal-rot",
    "Garlic rust": "garlic-rust",
    "Leaf spot / leaf blight": "alternaria-cercospora-leaf-spot",
    "Leafhoppers (and aster yellows / curly top)": "leafhoppers",
    "Onion maggot": "onion-maggot",
    "Onion thrips": "onion-thrips",
    "Parsleyworm (black swallowtail caterpillar)": "parsleyworm",
    "Powdery mildew": "powdery-mildew",
    "Soft rot": "bacterial-soft-rot",
    "Stem and bulb nematode (garlic bloat nematode)": "stem-and-bulb-nematode",
    "White rot": "white-rot",
}
NEW_IDS = ("allium-leafminer", "bacterial-leaf-spot", "botrytis-neck-rot", "fusarium-basal-rot",
           "garlic-rust", "leafhoppers", "onion-maggot", "onion-thrips", "parsleyworm",
           "stem-and-bulb-nematode", "white-rot")
# The five problems both alliums carry; they MUST take the same id or the family splits at birth.
SHARED_ALLIUM_IDS = ("onion-thrips", "onion-maggot", "white-rot", "fusarium-basal-rot",
                     "botrytis-neck-rot")

WIDEN_KEY = "certified_clean_stock"
NEMATODE = "stem-and-bulb-nematode"
# `handpick` means catching free-living insects on a scouting walk. Only these qualify here.
HANDPICK_OK = ("parsleyworm",)


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def staged_widening():
    return json.load(open(os.path.join(STAGING, "widen_certified_clean_stock.json")))


# LITERALS, not read from the staged spec. Deriving them from the file they are checked against
# would make the agreement check vacuous by construction -- batch 10 shipped that defect and the
# mutation harness caught it.
WIDEN_ADD = "nematode"
WIDEN_BEST_USE = (
    "Problems that travel in the planting material itself: seed-borne foliar and vascular "
    "pathogens, viruses carried in cuttings, crowns or divisions, and the nematodes that ride "
    "inside seed cloves, bulbs and sets. Set once, at purchase or propagation, before anything is "
    "in the ground.")
WIDEN_SEASONED_TAIL = (
    " The same logic reaches planting-stock-borne nematodes: the stem and bulb nematode arrives "
    "inside infected garlic cloves, and no in-season measure reaches a pest already inside the "
    "tissue you planted.")


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


def prose_signature(crop):
    return [tuple(json.dumps(p.get(f), sort_keys=True) for f in PROSE_FIELDS)
            for _, p in problems(crop)]


def ladder_signature(obj):
    """Keyed by problem id, not position (batch 10's fix: a positional signature calls two crops
    distinct even with byte-identical ladders in a different order)."""
    return json.dumps({p["id"]: [(r["method"], r["note_beginner"], r["note_seasoned"])
                                 for r in p["control_ladder"]]
                       for _, p in problems(obj)}, sort_keys=True)


# The fields that actually carry ADVICE, in either schema. `cause_*` and `name` exist in both, so
# a comparison restricted to those is not vacuous -- but it is blind to the half of the record the
# ladders are built from, which is exactly where two crops of one family differ.
ADVICE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",
                 "prevention_beginner", "prevention_seasoned",
                 "management_beginner", "management_seasoned")


def check_schema_coverage(by):
    """The twins check must reach each crop's ADVICE-bearing fields, not merely its shared ones.

    This batch spans two schemas: the alliums carry `management_*`, the herbs
    `organic_treatment_*` / `prevention_*`. A classic-only PROSE_FIELDS still compares `name` and
    `cause_*`, so it does not go silently vacuous -- but it stops comparing the prose the ladders
    are actually built from, which is the half that distinguishes two crops of one family. Require
    coverage per crop rather than assuming one schema.
    """
    for slug in CROPS:
        seen = set()
        for _, p in problems(by[slug]):
            seen |= set(p.keys())
        own_advice = seen & set(ADVICE_FIELDS)
        if not own_advice:
            return f"{slug}: no advice-bearing prose field found; the record shape is unexpected"
        if not (own_advice & set(PROSE_FIELDS)):
            return (f"{slug}: PROSE_FIELDS reaches none of its advice-bearing fields "
                    f"({sorted(own_advice)}), so the twins check would compare only names and "
                    f"causes for it; this batch spans two schemas and the list must cover both")
        if slug in NEW_SCHEMA_CROPS and "management_seasoned" not in seen:
            return f"{slug} was expected to use the identification_/management_ schema and does not"
    return None


def check_not_twins(by):
    problem = check_schema_coverage(by)
    if problem:
        return problem
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if prose_signature(by[a]) == prose_signature(by[b]):
                return f"{a} and {b} are byte-identical in canonical, a TRUE TWIN"
    dg = staged_digests()
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if dg[a] == dg[b]:
                return f"the staged files for {a} and {b} are byte-identical, so one was copied"
    return None


def check_read_fixes(batch, by):
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return f"{slug}: problem {name!r} is not in the id-convention table"
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention "
                        f"ships {want!r}; ids are join keys")

    # THE ALLIUM CONVENTION: onion, leek and shallot will inherit these. A split at birth is the
    # expensive failure, so both crops must carry the same string for every shared problem.
    # FORWARD ASSERTION, NOT COVERAGE: ID_CONVENTION is keyed by problem NAME and both alliums use
    # identical names, so one table entry serves both and the loop above always answers first.
    # This cannot fail independently today; it is kept for the case where a later editor adds a
    # second name entry for the same problem, and it is deliberately NOT counted as guard coverage
    # (its mutation is withdrawn from the harness for that reason).
    g_ids = {p["id"] for _, p in problems(batch["garlic"])}
    s_ids = {p["id"] for _, p in problems(batch["spring-onion"])}
    for pid in SHARED_ALLIUM_IDS:
        if pid not in g_ids or pid not in s_ids:
            return (f"the two alliums disagree on {pid!r}: garlic={pid in g_ids}, "
                    f"spring-onion={pid in s_ids}. This batch sets the convention onion, leek and "
                    f"shallot inherit, so a split here propagates")

    # THE WIDENING'S RUNG, and the retired practice it must not resurrect.
    ms, p = ladder_of(batch["garlic"], NEMATODE)
    if ms is None:
        return "garlic has no stem-and-bulb-nematode problem"
    if WIDEN_KEY not in ms:
        return (f"garlic/{NEMATODE} has no {WIDEN_KEY} rung; its prose calls nematode-free seed "
                f"stock the single most important practice, and the widening exists for it")
    if ms[0] != WIDEN_KEY:
        return (f"garlic/{NEMATODE}: {WIDEN_KEY} must lead the ladder, since the prose ranks it "
                f"above everything else")
    blob = " ".join(r["note_beginner"] + " " + r["note_seasoned"] for r in p["control_ladder"])
    if "hot-water" in blob.lower() or "hot water" in blob.lower():
        if "no longer" not in blob.lower():
            return (f"garlic/{NEMATODE}: a note raises hot-water dips without the prose's "
                    f"retirement of them; the source says they only reduce, not eliminate")

    # RULING: a mention that LIMITS is not a recommendation.
    ms, _ = ladder_of(batch["cilantro-coriander"], "bacterial-leaf-spot")
    if ms is None:
        return "cilantro-coriander has no bacterial-leaf-spot problem"
    if "copper_fungicide" in ms:
        return ("cilantro-coriander/bacterial-leaf-spot carries copper, but its beginner register "
                "says there is no spray cure in the home garden and the seasoned one names copper "
                "only to bound it; a limitation is not a recommendation")

    # Batch-wide standing refusals.
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if "planting_time_avoidance" in lad:
                return (f"{slug}/{p.get('id')} carries planting_time_avoidance; nothing in this "
                        f"batch's prose recommends shifting a planting, and a risk description is "
                        f"not a recommendation")
            if "handpick" in lad and p.get("id") not in HANDPICK_OK:
                return (f"{slug}/{p.get('id')} carries handpick, whose meaning is catching "
                        f"free-living insects; removing affected leaves is garden_sanitation")
            if "pyrethroid" in lad:
                return f"{slug}/{p.get('id')} carries the synthetic pyrethroid"
            # `trap_cropping` becomes a legal key when the parallel round lands. NO crop in this
            # batch may take it: dill's parsleyworm is the only mention, and it is
            # relocation-for-CONSERVATION (move the larvae to a spare plant to keep them alive on
            # a host grown partly for the butterflies). The method's meaning ends in destroying
            # the trap, so a rung there reverses the advice.
            if "trap_cropping" in lad:
                return (f"{slug}/{p.get('id')} carries trap_cropping; no prose in this batch "
                        f"recommends the classic action, and dill's parsleyworm is "
                        f"relocation-for-conservation, whose intent is the opposite")
            for r in p.get("control_ladder") or []:
                blob = (r.get("note_beginner", "") + " " + r.get("note_seasoned", "")).lower()
                for word in ("diatomaceous", "trap crop"):
                    if word in blob:
                        return f"{slug}/{p.get('id')}: a note mentions {word}, which has no key"
    return None


def check_catalog_premises(cm):
    m = cm.get(WIDEN_KEY)
    if not m:
        return f"{WIDEN_KEY} is not in the catalog"
    if WIDEN_ADD in m["applies_to"]:
        return f"{WIDEN_KEY} already reaches {WIDEN_ADD}; this promote has already run"
    spec = staged_widening()
    if (spec.get("applies_to_add") != WIDEN_ADD or spec.get("best_use") != WIDEN_BEST_USE
            or spec.get("how_it_works_seasoned") != m["how_it_works_seasoned"] + WIDEN_SEASONED_TAIL):
        return "the staged widening spec disagrees with this promote's literals"
    if "nematode" in m["best_use"].lower():
        return f"{WIDEN_KEY}'s best_use already names nematodes; re-check the premise"
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    order = {t: i for i, t in enumerate(TIERS)}
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
                tiers.append(order[cm[m]["tier"]])
            if tiers != sorted(tiers):
                return f"{crop}/{p.get('id')}: tiers decrease {tiers}"
        if n_prob != EXPECTED_PROBLEMS[crop]:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS[crop]}"
    return None


def widened(cm):
    """The catalog as it will be, for the applies_to check."""
    out = copy.deepcopy(cm)
    m = out[WIDEN_KEY]
    m["applies_to"] = list(m["applies_to"]) + [WIDEN_ADD]
    m["best_use"] = WIDEN_BEST_USE
    m["how_it_works_seasoned"] = m["how_it_works_seasoned"] + WIDEN_SEASONED_TAIL
    return out


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}

    problem = check_catalog_premises(cm)
    if problem:
        return problem
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()
    for problem in (check_not_twins(by), check_read_fixes(batch, by)):
        if problem:
            return problem
    for slug in CROPS:
        a, b = len(problems(batch[slug])), len(problems(by[slug]))
        if a != b:
            return f"{slug}: staged {a} problems, canonical {b}"
    problem = validate_batch(batch, widened(cm))
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
            "methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": dump(data["source_catalog"])}


def apply_to(data):
    m = data["control_methods"][WIDEN_KEY]
    m["applies_to"] = list(m["applies_to"]) + [WIDEN_ADD]
    m["best_use"] = WIDEN_BEST_USE
    m["how_it_works_seasoned"] = m["how_it_works_seasoned"] + WIDEN_SEASONED_TAIL
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
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST (tenth time stated).
    m = json.loads(post["methods"][WIDEN_KEY])
    if WIDEN_ADD not in m["applies_to"]:
        return f"post: {WIDEN_KEY} does not reach {WIDEN_ADD}"
    if m["best_use"] != WIDEN_BEST_USE:
        return f"post: {WIDEN_KEY}'s best_use did not take the widened prose"
    if not m["how_it_works_seasoned"].endswith(WIDEN_SEASONED_TAIL):
        return f"post: {WIDEN_KEY}'s how_it_works_seasoned did not take the widened prose"
    for slug in CROPS:
        for _, p in problems(by[slug]):
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{p.get('id')}: no ladder after promote"
            if "planting_time_avoidance" in lad:
                return f"post: {slug}/{p.get('id')} shipped an unearned timing rung"
            if "handpick" in lad and p.get("id") not in HANDPICK_OK:
                return f"post: {slug}/{p.get('id')} shipped handpick on a leaf-removal target"
            for r in p["control_ladder"]:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                if "diatomaceous" in blob or "trap crop" in blob:
                    return f"post: {slug}/{p.get('id')}: an unminted method reached a note"
    ms, _ = ladder_of(by["garlic"], NEMATODE)
    if not ms or ms[0] != WIDEN_KEY:
        return f"post: garlic/{NEMATODE} lost its leading {WIDEN_KEY} rung"
    ms, _ = ladder_of(by["cilantro-coriander"], "bacterial-leaf-spot")
    if "copper_fungicide" in ms:
        return "post: cilantro's bacterial leaf spot gained the copper rung the read ruled out"
    g_ids = {p["id"] for _, p in problems(by["garlic"])}
    s_ids = {p["id"] for _, p in problems(by["spring-onion"])}
    for pid in SHARED_ALLIUM_IDS:
        if pid not in g_ids or pid not in s_ids:
            return f"post: the alliums shipped a split id on {pid!r}"

    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    if set(post["methods"]) != set(pre["methods"]):
        return "post: control_methods gained or lost a key; this promote widens one and mints none"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    for key, before in pre["methods"].items():
        if key == WIDEN_KEY:
            continue
        if post["methods"][key] != before:
            return f"post: bystander method {key!r} changed"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"

    # FORWARD ASSERTION, NOT COVERAGE. `ladder_signature` is keyed by problem id, and no two crops
    # in THIS batch share an id set (garlic 7, spring-onion 6, dill 5, cilantro 6, all distinct),
    # so this cannot fire here however the ladders are doctored. It was genuinely load-bearing in
    # batch 10, where collards and kale carried identical id sets. Kept for the next batch that
    # pairs same-shaped crops; its mutation is withdrawn from the harness rather than left
    # reporting a coverage gap it cannot earn.
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):
                return f"post: {CROPS[i]} and {CROPS[j]} carry identical ladder CONTENT"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    # CHAIN-REPLAY CONTRACT. promote_fixture._from_chain rebuilds an uncommitted intermediate state
    # by invoking its producing promote as
    #     <script> --canonical PATH --expect-sha SHA --apply
    # so a script any later suite must replay through has to accept exactly that shape. Batch 12
    # sits on this promote's output (parsley reuses `parsleyworm`, which batch 11 mints for dill),
    # and that output is not a commit until batch 11 is committed, so this is a CHAIN member.
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

    print("PLA-8 BATCH 11 -- ALLIUMS + FALL HERBS (fall block, batch 4 of 5)")
    print(f"  crops        : {', '.join(CROPS)}  (FOUR authoring passes, TWO prose schemas)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused ({len(NEW_IDS)} new to the roster)")
    print(f"  widening     : {WIDEN_KEY} reaches {WIDEN_ADD}, unblocking garlic's PRIMARY control")
    print(f"  read rulings : copper OFF cilantro's bacterial leaf spot (a limitation is not a")
    print(f"                 recommendation); the two alliums agree on all 5 shared ids")
    print(f"  blast radius : 4 crops + 1 widened method; sources 0; bystanders 0")
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
