#!/usr/bin/env python3
"""PLA-8 BATCH 10 -- THE BRASSICA FAMILY, third batch of the fall block. Base 4725bcbb.

48 problems gain `id`, `type` and `control_ladder`; **237 rungs** across `cabbage` (47),
`cauliflower` (52), `kohlrabi` (52), `collards` (43) and `kale` (43). ONE method minted:
`pyrethrin`. Roster laddered 41 -> 46. The largest batch of the arc.

--------------------------------------------------------------------------------------------------
THE MINT: `pyrethrin`, AND THE SUBSTITUTION IT PREVENTS
--------------------------------------------------------------------------------------------------
**ALL FIVE CROPS NAME BOTANICAL PYRETHRINS FOR HARLEQUIN BUG AND NO KEY CARRIED IT.** cabbage,
cauliflower and kohlrabi say "Insecticidal soap, pyrethrum, or neem help where pressure is
severe"; collards and kale say "Pyrethrins are permitted in organic production if pressure is
severe." The only near-neighbour in the catalog is `pyrethroid` -- the SYNTHETIC analog, at
CONVENTIONAL tier, whose cautions enumerate permethrin, bifenthrin and cypermethrin. Mapping one
onto the other would swap an organic-permitted botanical for a synthetic and attach the wrong
hazard profile entirely: the neem-on-beetles defect with a safety dimension. **All five authoring
agents independently refused the substitution and reported the control blocked** -- five of five,
the playbook's mint signal at full strength.

**AND THE READING CHANGED WHAT THE ENTRY HAD TO SAY.** Read 2026-08-27 with the validated
raw-HTML parser, chlorothalonil re-run as the POSITIVE CONTROL in the same pass and matching its
2026-08-26 reading exactly. UC IPM uaiKey=53 puts pyrethrins in the **STRICTEST honey bee band** --
the same band as carbaryl and the synthetic pyrethroids, which grants NO evening window at all.
An organically acceptable material a gardener reaches for casually is, on bees, as restricted as
the conventional insecticides. The entry says so in as many words ("Being organically acceptable
does not soften this"), and every one of the five rungs carries it. NPIC corroborates ("highly
toxic to honey bees") and supplies the mitigating half this entry also states: rapid sunlight
breakdown, under 3 percent left on foliage after five days. Acute L, chronic NKR, natural enemies
M, water LH -- the mild halves stated alongside the alarming one, per the disclosure standard.

--------------------------------------------------------------------------------------------------
THE READ'S SECOND RULING: A RISK DESCRIPTION IS NOT A RECOMMENDATION
--------------------------------------------------------------------------------------------------
**`planting_time_avoidance` DROPPED from every cabbage-root-maggot ladder** (it was authored on
four of the five). All five crops' prose says only that the fly *is most active* in cool spring
weather -- a statement of WHEN RISK IS HIGH. None of them recommends shifting the planting.
Turning that into a timing rung authors a recommendation the source never makes: the
`fill-the-shape` defect. The contrast is what proves it: batch 9's turnip and radish DO carry the
recommendation verbatim ("favor fall plantings, which see less pressure than cool wet spring";
"time spring sowings to dodge the main egg-laying flush"), and their shipped rungs stand. Kale's
agent reached this ruling independently and omitted the rung.

**THE DROP IS SCOPED, and the scope is visible inside one crop.** `planting_time_avoidance`
STAYS on kohlrabi's flea-beetles, whose prose does recommend a shift: "favor fall plantings,
which see lighter pressure." Same key, same crop, two problems, one earned and one not.

--------------------------------------------------------------------------------------------------
COPPER, PINNED BY PROSE IN BOTH DIRECTIONS
--------------------------------------------------------------------------------------------------
Copper appears on alternaria and downy mildew wherever the crop's prose recommends it, and on
**NO black-rot ladder anywhere in the batch** -- all five say there is no effective cure and name
no fungicide. Shipped broccoli's black-rot ladder DOES end in copper, so this is a deliberate
cross-crop divergence driven by each crop's own prose, not an oversight; it is recorded as a
finding rather than reconciled here, because the fix (if any) belongs in the prose.

REFUSALS: base SHA mismatch; the mint already present or disagreeing with its staged spec; a crop
already laddered; an id off the convention; `pyrethroid` anywhere in the batch; a harlequin-bug
ladder without its pyrethrin rung; `planting_time_avoidance` on any root-maggot ladder, or missing
from kohlrabi's flea beetles; copper on any black-rot ladder, or missing where prose recommends
it; `handpick` on any leaf-removal target; any "diatomaceous" or "trap crop" in a note; an unknown
method; a tier decrease; applies_to incoherence; identical registers; counts off; any pair of
staged files byte-identical; any bystander crop, other method, or source changed.

Guard suite:      tools/test_promote_pla8_batch10.py
Mutation harness: tools/mutate_pla8_batch10_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch10.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch10_brassicas")
BASE_SHA = "4725bcbbe0cc78046b718c40bb5f97bdcd6638f7f55bec83e1ab465e1a5846f4"

CROPS = ("cabbage", "cauliflower", "kohlrabi", "collards", "kale")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"cabbage": 10, "cauliflower": 10, "kohlrabi": 10, "collards": 9, "kale": 9}
EXPECTED_RUNGS = {"cabbage": 47, "cauliflower": 52, "kohlrabi": 52, "collards": 43, "kale": 43}

PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

ID_CONVENTION = {
    "Alternaria leaf spot": "alternaria-leaf-spot",
    "Aphids": "aphids",
    "Bacterial soft rot (head rot)": "bacterial-soft-rot",
    "Black rot": "black-rot",
    "Blackleg": "blackleg",
    "Cabbage aphids": "cabbage-aphids",
    "Cabbage root maggot": "cabbage-root-maggot",
    "Cabbageworms and cabbage loopers": "cabbageworms",
    "Cabbageworms, loopers, and diamondback moths": "cabbageworms",
    "Clubroot": "clubroot",
    "Downy mildew": "downy-mildew",
    "Flea beetles": "flea-beetles",
    "Fusarium yellows": "fusarium-yellows",
    "Harlequin bug": "harlequin-bug",
}
# Genuinely new to the dataset; every other id above already ships on the roster.
NEW_IDS = ("bacterial-soft-rot", "blackleg", "fusarium-yellows")

MINT_KEY = "pyrethrin"
HB, RM, FB, BR = "harlequin-bug", "cabbage-root-maggot", "flea-beetles", "black-rot"
# The one crop whose FLEA-BEETLE prose recommends a seasonal shift ("favor fall plantings").
TIMING_KEPT = (("kohlrabi", FB),)
# Copper is authored only where the crop's own prose recommends it.
COPPER_ON = (("cauliflower", "alternaria-leaf-spot"), ("kohlrabi", "alternaria-leaf-spot"),
             ("collards", "alternaria-leaf-spot"), ("kale", "alternaria-leaf-spot"),
             ("cabbage", "downy-mildew"), ("cauliflower", "downy-mildew"),
             ("kohlrabi", "downy-mildew"), ("collards", "downy-mildew"),
             ("kale", "downy-mildew"))
# `handpick` means catching free-living insects on a scouting walk; leaf/plant removal is
# garden_sanitation. These are the only two problems in the batch where the target qualifies.
HANDPICK_OK = ("cabbageworms", HB)


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def staged_mint():
    return json.load(open(os.path.join(STAGING, "mint_pyrethrin.json")))


# THE MINT AS A LITERAL, not read from the staged spec. Deriving it from the file it is checked
# against made the agreement check VACUOUS by construction -- the computed-expected-value trap,
# caught by the mutation harness when disabling that check changed nothing. Written out, the
# check now genuinely proves staging and promote have not drifted apart.
MINT = {
    "name": "Pyrethrin (botanical)",
    "tier": "soft_chemical",
    "applies_to": [
        "insect_general",
        "insect_chewing",
        "insect_soft_bodied"
    ],
    "how_it_works_beginner": "Pyrethrin is an insecticide pressed from chrysanthemum flowers. It hits the insect's nervous system on contact and knocks pests down fast, then breaks apart in sunlight within a day or so, which is why it leaves little behind but often needs repeating.",
    "how_it_works_seasoned": "Pyrethrins are a mixture of six related compounds extracted from chrysanthemum flowers that disrupt the insect central nervous system on contact. They degrade rapidly in sunlight, with a half-life near 12 hours on soil and in water and less than 3 percent remaining on treated foliage after five days, so knockdown is quick and residual control is short.",
    "best_use": "A fast-knockdown botanical for a severe insect outbreak the softer rungs have not held, on a crop where you want an organically acceptable material with little persistence. Distinct from the synthetic pyrethroids, which are laboratory analogs of this molecule built to last far longer and sit in the conventional tier; this is the short-lived plant extract.",
    "find_it_beginner": "Sold as pyrethrin or pyrethrum garden insect sprays; on the label look for 'pyrethrins' as the active ingredient. Products combining it with insecticidal soap are common. Note that a similar-looking name, permethrin, is a longer-lasting synthetic, not this.",
    "pros": [
        "Fast knockdown on contact, and acceptable in organic production",
        "Breaks down quickly in sunlight, so it leaves little residue on the crop"
    ],
    "cons": [
        "Contact-only with almost no residual, so it must hit the pest and often needs repeating",
        "Broad-spectrum: it takes beneficial insects along with the pest wherever it lands"
    ],
    "cautions": [
        "UC IPM puts pyrethrins in its strictest honey bee band: do not apply them, or let them drift, onto anything in flower including weeds, and do not let them reach water bees can drink such as puddles. Being organically acceptable does not soften this; the band is the same one the synthetic insecticides sit in.",
        "Rated Moderate for harm to natural enemies, so a spray can remove the predators that were holding a second pest down",
        "Rated Low to High for water quality risk to aquatic wildlife depending on the product; keep spray and runoff away from ponds, streams and storm drains",
        "UC IPM rates acute toxicity to people and other mammals Low, and the chronic rating is no known risk, so the short term and long term risks to the person spraying are the mild half of this ingredient's picture",
        "Many consumer products do not print protective equipment on the label; wear chemical resistant gloves, long sleeves and goggles regardless",
        "Observe the pre-harvest interval on the label before eating the crop, and read and follow the label every time"
    ],
    "sources": [
        "ucipm_uaidb",
        "npic_orst"
    ],
    "anchoring_urls": {
        "ucipm_uaidb": {
            "url": "https://ipm.ucanr.edu/home-and-landscape/pesticide-active-ingredients-database/active-ingredient-details/?uaiKey=53",
            "verified": "2026-08-27"
        },
        "npic_orst": {
            "url": "https://npic.orst.edu/factsheets/pyrethrins.html",
            "verified": "2026-08-27"
        }
    }
}


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
    """Keyed by problem ID, not by position. The crops in this batch order their problems
    differently, so a positional signature would call two crops distinct even with byte-identical
    ladders -- the identity guard would then be unable to catch a wholesale copy. Found by
    writing the driver for it."""
    return json.dumps({p["id"]: [(r["method"], r["note_beginner"], r["note_seasoned"])
                                 for r in p["control_ladder"]]
                       for _, p in problems(obj)}, sort_keys=True)


def check_not_twins(by):
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if prose_signature(by[a]) == prose_signature(by[b]):
                return (f"{a} and {b} are byte-identical in canonical, a TRUE TWIN; author one and "
                        f"propagate rather than authoring both")
    dg = staged_digests()
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if dg[a] == dg[b]:
                return (f"the staged files for {a} and {b} are byte-identical, so one was copied; "
                        f"each crop needs its own authoring pass")
    return None


def check_read_fixes(batch, by):
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return (f"{slug}: problem {name!r} is not in the id-convention table; add its "
                        f"roster ruling before promoting")
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention "
                        f"ships {want!r}; ids are join keys")

        # THE MINT'S RUNGS: every harlequin-bug ladder ends in pyrethrin, and the synthetic
        # never appears anywhere in the batch.
        ms, _ = ladder_of(batch[slug], HB)
        if ms is None:
            return f"{slug} has no {HB} problem"
        if MINT_KEY not in ms:
            return (f"{slug}/{HB} has no {MINT_KEY} rung; this crop's prose names botanical "
                    f"pyrethrins for it and the mint exists for exactly these five rungs")
        for _, p in problems(batch[slug]):
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if "pyrethroid" in lad:
                return (f"{slug}/{p.get('id')} carries pyrethroid, the SYNTHETIC analog at "
                        f"conventional tier; the prose names the BOTANICAL pyrethrins, and "
                        f"substituting swaps the material and its hazard profile")

        # RULING: a risk description is not a recommendation.
        ms, _ = ladder_of(batch[slug], RM)
        if ms is None:
            return f"{slug} has no {RM} problem"
        if "planting_time_avoidance" in ms:
            return (f"{slug}/{RM} carries planting_time_avoidance, but this crop's prose only "
                    f"states that the fly is most active in cool spring weather; it never "
                    f"recommends shifting the planting, unlike batch 9's turnip and radish")

        # No copper on black rot anywhere: all five say there is no cure and name no fungicide.
        ms, _ = ladder_of(batch[slug], BR)
        if ms is None:
            return f"{slug} has no {BR} problem"
        if "copper_fungicide" in ms:
            return (f"{slug}/{BR} carries copper, but this crop's prose names no fungicide for "
                    f"black rot; shipped broccoli's copper rung is not license to add one here")

        # handpick only where the target is a free-living insect.
        for _, p in problems(batch[slug]):
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if "handpick" in lad and p.get("id") not in HANDPICK_OK:
                return (f"{slug}/{p.get('id')} carries handpick, whose meaning is catching "
                        f"free-living insects on a scouting walk; removing affected leaves or "
                        f"plants is garden_sanitation")
            for r in p.get("control_ladder") or []:
                blob = (r.get("note_beginner", "") + " " + r.get("note_seasoned", "")).lower()
                if "diatomaceous" in blob:
                    return f"{slug}/{p.get('id')}: a note mentions diatomaceous earth"
                if "trap crop" in blob:
                    return (f"{slug}/{p.get('id')}: a note mentions trap cropping, which has no "
                            f"catalog key; it is a recorded gap, not a rung")

    for slug, pid in TIMING_KEPT:
        ms, _ = ladder_of(batch[slug], pid)
        if ms is None or "planting_time_avoidance" not in ms:
            return (f"{slug}/{pid} lost planting_time_avoidance; its prose DOES recommend a shift "
                    f"(favor fall plantings, which see lighter pressure), so the root-maggot drop "
                    f"was scoped rather than blanket")
    for slug, pid in COPPER_ON:
        ms, _ = ladder_of(batch[slug], pid)
        if ms is None or "copper_fungicide" not in ms:
            return f"{slug}/{pid} lost its copper rung; this crop's prose recommends copper for it"
    return None


def check_catalog_premises(cm):
    if MINT_KEY in cm:
        return f"{MINT_KEY} is already in the catalog; this promote has already run"
    if staged_mint().get("entry") != MINT:
        return "the staged mint spec disagrees with this promote's literal"
    if "pyrethroid" not in cm:
        return "pyrethroid is not in the catalog, so the substitution this mint prevents is moot"
    if cm["pyrethroid"]["tier"] != "conventional":
        return "pyrethroid is no longer conventional; re-argue the mint's distinction"
    if MINT["tier"] != "soft_chemical":
        return "the mint is not soft_chemical; the crops' prose calls pyrethrins organic-permitted"
    bee = " ".join(MINT.get("cautions") or []).lower()
    if "strictest honey bee band" not in bee:
        return ("the mint's cautions no longer state the strictest bee band, which is the reading "
                "that made this entry worth writing")
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

    cm_post = dict(cm)
    cm_post[MINT_KEY] = MINT
    problem = validate_batch(batch, cm_post)
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
    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)
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

    # SUBSTANTIVE INVARIANTS FIRST (eighth time stated).
    if json.loads(post["methods"].get(MINT_KEY, "null")) != json.loads(
            json.dumps(MINT, sort_keys=True)):
        return f"post: {MINT_KEY} did not land verbatim"
    for slug in CROPS:
        for _, p in problems(by[slug]):
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{p.get('id')}: no ladder after promote"
            if "pyrethroid" in lad:
                return f"post: {slug}/{p.get('id')} shipped the synthetic pyrethroid"
            if "handpick" in lad and p.get("id") not in HANDPICK_OK:
                return f"post: {slug}/{p.get('id')} shipped handpick on a leaf-removal target"
            for r in p["control_ladder"]:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                if "diatomaceous" in blob or "trap crop" in blob:
                    return f"post: {slug}/{p.get('id')}: an unminted method reached a note"
        ms, _ = ladder_of(by[slug], HB)
        if MINT_KEY not in ms:
            return f"post: {slug}/{HB} lost its {MINT_KEY} rung"
        ms, _ = ladder_of(by[slug], RM)
        if "planting_time_avoidance" in ms:
            return f"post: {slug}/{RM} regained the unearned timing rung"
        ms, _ = ladder_of(by[slug], BR)
        if "copper_fungicide" in ms:
            return f"post: {slug}/{BR} gained a copper rung its prose does not recommend"
    for slug, pid in TIMING_KEPT:
        ms, _ = ladder_of(by[slug], pid)
        if "planting_time_avoidance" not in ms:
            return f"post: {slug}/{pid} lost the timing rung its prose DOES recommend"
    for slug, pid in COPPER_ON:
        ms, _ = ladder_of(by[slug], pid)
        if "copper_fungicide" not in ms:
            return f"post: {slug}/{pid} lost its copper rung"

    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    if set(post["methods"]) != set(pre["methods"]) | {MINT_KEY}:
        return "post: control_methods gained or lost something other than the one mint"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    for key, before in pre["methods"].items():
        if post["methods"][key] != before:
            return f"post: bystander method {key!r} changed, and this promote only mints"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"

    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):
                return (f"post: {CROPS[i]} and {CROPS[j]} carry identical ladder CONTENT; they "
                        f"were authored separately from their own prose")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

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

    print("PLA-8 BATCH 10 -- THE BRASSICA FAMILY (fall block, batch 3 of 5)")
    print(f"  crops        : {', '.join(CROPS)}  (FIVE authoring passes)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused ({len(NEW_IDS)} new to the roster)")
    print(f"  mint         : {MINT_KEY} -- botanical, soft_chemical, STRICTEST bee band;")
    print(f"                 blocked in all 5 crops, refused by all 5 agents")
    print(f"  read rulings : planting_time_avoidance OFF every root-maggot ladder (a risk")
    print(f"                 description is not a recommendation), KEPT on kohlrabi's flea beetles")
    print(f"  blast radius : 5 crops + 1 minted method; sources 0; bystanders 0")
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
