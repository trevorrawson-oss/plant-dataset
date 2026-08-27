#!/usr/bin/env python3
"""PLA-8 BATCH 8 -- THE LEAFY GREENS, first batch of the fall block. Base f8678ade.

32 problems gain `id`, `type` and `control_ladder`; **153 rungs** across `spinach` (36),
`arugula` (40), `lettuce-leaf` (20) and `bok-choy` (57). NO method minted, NO source, no crop
outside the four. Roster laddered 33 -> 37.

**FOUR INDEPENDENT AUTHORING PASSES**, six crop pairs refused as twins in both directions.

**THE IDS FOLLOW THE ROSTER, INCLUDING TWO DELIBERATE REUSES AND ONE CONVERGENCE.** spinach's
leafminer reuses swiss-chard's `beet-spinach-leafminer` (same pest, Pegomya hyoscyami -- the
exact divergence pair the 2026-08-23 measurement warned about); bok-choy reuses broccoli's
`cabbage-root-maggot`, `clubroot`, `black-rot`; and BOTH "Cabbage caterpillars" entries
(arugula, bok-choy) converge on broccoli's shipped `cabbageworms` rather than minting a
near-synonym for the same brassica caterpillar complex. `cabbage-aphids` is minted DISTINCT
from `aphids` because bok-choy's entry is the Brevicoryne specialist by name and content (the
strawberry `two-spotted-spider-mite` precedent).

--------------------------------------------------------------------------------------------------
THE READ'S ADJUDICATIONS (each pinned below)
--------------------------------------------------------------------------------------------------
**THE COPPER SPLIT ON DOWNY MILDEW IS PROSE-DRIVEN AND RUNS BOTH WAYS.** lettuce-leaf and
bok-choy carry a copper rung because their prose recommends preventive copper outright; spinach's
rung was authored and then DROPPED by the read, because its prose says "copper has limited
efficacy" inside a "cultural control dominates" sentence -- a rung whose own note says "do not
count on them" argues against itself; arugula's prose never names copper and none was authored.
Same method, four crops, the crop's own sourced prose deciding each.

**LETTUCE'S DOWNY MILDEW MUST NOT CARRY crop_rotation.** Its cause prose states the pathogen
"does not survive in the soil"; a rotation rung would contradict the crop's own record. spinach
and arugula DO carry rotation on downy mildew, because their pathogens overwinter on debris and
as oospores per their own prose.

**DIATOMACEOUS EARTH STAYS OUT, EVERYWHERE.** DE remains a deliberately-unminted method
(playbook section 7); a first-draft lettuce rung folded a DE ring into slug_traps_barriers and
the read stripped it. No rung note in this batch may mention it.

**NO neem_oil ON ANY flea-beetles LADDER** -- batch 7's refusal held at authoring time here (no
agent authored it), pinned as a refusal-spec so it stays held.

**ORDER NORMALIZATIONS (batch-6 precedent):** white-rust ships the same five cultural rungs in
the same order on its three carriers; damping-off ships the same three, sowing-first, on its two.

Other prose-driven divergences pinned: only bok-choy's cabbage-aphids carries horticultural_oil
(its prose names it); spinach's flea-beetles has no cultural rung (its prose states no
crucifer-host or debris claim, unlike arugula's and bok-choy's, which carry
garden_sanitation + weed_host_control).

REFUSALS: base SHA mismatch; a crop already laddered; an id off the roster convention; any pair
of staged files or post-state ladders byte-identical; copper on spinach or arugula downy mildew,
or missing from lettuce or bok-choy downy mildew; rotation on lettuce downy mildew; any
"diatomaceous" in any note; neem on any flea-beetles ladder; the white-rust or damping-off
normalization drifting; an unknown method; a tier decrease; applies_to incoherence; identical
registers; problem or rung counts off; any bystander crop, ANY method, or any source changed.

Guard suite:      tools/test_promote_pla8_batch8.py
Mutation harness: tools/mutate_pla8_batch8_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch8.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch8_leafy_greens")
BASE_SHA = "f8678adea533447445ee2679d7d333065763a7481c39371b98d0b39d55aeeec1"

CROPS = ("spinach", "arugula", "lettuce-leaf", "bok-choy")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"spinach": 8, "arugula": 8, "lettuce-leaf": 5, "bok-choy": 11}
EXPECTED_RUNGS = {"spinach": 36, "arugula": 40, "lettuce-leaf": 20, "bok-choy": 57}

PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

ID_CONVENTION = {
    "Spinach leafminer": "beet-spinach-leafminer",
    "Aphids": "aphids",
    "Flea beetles": "flea-beetles",
    "Caterpillars (loopers and armyworms)": "loopers-armyworms",
    "Downy mildew (blue mold)": "downy-mildew",
    "Downy mildew": "downy-mildew",
    "White rust": "white-rust",
    "Damping-off": "damping-off",
    "Fusarium wilt": "fusarium-wilt",
    "Slugs & snails": "slugs-and-snails",
    "Slugs and snails": "slugs-and-snails",
    "Lettuce root aphid": "lettuce-root-aphid",
    "Tipburn": "tipburn",
    "Alternaria and Cercospora leaf spot": "alternaria-cercospora-leaf-spot",
    "Cabbage caterpillars": "cabbageworms",
    "Cabbage aphids": "cabbage-aphids",
    "Cabbage root maggot": "cabbage-root-maggot",
    "Harlequin bug": "harlequin-bug",
    "Clubroot": "clubroot",
    "Black rot": "black-rot",
    "Alternaria leaf spot": "alternaria-leaf-spot",
}

DM = "downy-mildew"
FB = "flea-beetles"
# The copper split on downy mildew, decided by each crop's own prose.
COPPER_ON_DM = ("lettuce-leaf", "bok-choy")
NO_COPPER_ON_DM = ("spinach", "arugula")
# Order-normalized shared ladders (batch-6 precedent).
WHITE_RUST_ORDER = ("resistant_varieties", "crop_rotation", "airflow_spacing",
                    "water_at_the_base", "garden_sanitation")
WHITE_RUST_CROPS = ("spinach", "arugula", "bok-choy")
DAMPING_OFF_ORDER = ("sound_sowing_practice", "improve_drainage", "garden_sanitation")
DAMPING_OFF_CROPS = ("spinach", "arugula")


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


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
    return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                        for r in p["control_ladder"]] for _, p in problems(obj)], sort_keys=True)


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
    """The read's adjudications, pinned. `by` is the CANONICAL crop map (names resolve from
    canonical at the same index; staged problems carry no name)."""
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
                        f"ships {want!r}; ids are join keys and must not diverge between crops")

    # THE COPPER SPLIT, both directions, on each crop's own prose.
    for slug in COPPER_ON_DM:
        ms, _ = ladder_of(batch[slug], DM)
        if ms is None:
            return f"{slug} has no {DM} problem"
        if "copper_fungicide" not in ms:
            return (f"{slug}/{DM} lost its copper rung; this crop's prose recommends preventive "
                    f"copper outright")
    for slug in NO_COPPER_ON_DM:
        ms, _ = ladder_of(batch[slug], DM)
        if ms is None:
            return f"{slug} has no {DM} problem"
        if "copper_fungicide" in ms:
            return (f"{slug}/{DM} carries a copper rung; spinach's prose says copper has limited "
                    f"efficacy and cultural control dominates, and arugula's names no copper at "
                    f"all, so the read dropped it on both")

    # Lettuce's pathogen does not survive in the soil, per its own cause prose.
    ms, _ = ladder_of(batch["lettuce-leaf"], DM)
    if "crop_rotation" in ms:
        return ("lettuce-leaf/downy-mildew carries crop_rotation, but its own cause prose states "
                "the pathogen does not survive in the soil; the rung would contradict the record")
    for slug in ("spinach", "arugula"):
        ms, _ = ladder_of(batch[slug], DM)
        if "crop_rotation" not in ms:
            return (f"{slug}/{DM} lost crop_rotation; its pathogen overwinters on debris and as "
                    f"oospores per its own prose")

    # DE stays out, batch-wide (the deliberately-unminted method).
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            for r in p.get("control_ladder") or []:
                blob = (r.get("note_beginner", "") + " " + r.get("note_seasoned", "")).lower()
                if "diatomaceous" in blob:
                    return (f"{slug}/{p.get('id')}: a note mentions diatomaceous earth, the "
                            f"deliberately-unminted method; the read stripped it and it must "
                            f"stay out")

    # Batch 7's neem refusal, held as a refusal-spec.
    for slug in CROPS:
        ms, _ = ladder_of(batch[slug], FB)
        if ms is None:
            continue  # lettuce has no flea-beetles problem
        if "neem_oil" in ms or "insecticidal_soap" in ms:
            return (f"{slug}/{FB} carries a soft-bodied contact spray; the catalog meaning is "
                    f"soft-bodied smothering and a hard-shelled beetle is the bottom_watering "
                    f"shape, refused batch-wide in batch 7")
        if "floating_row_cover" not in ms:
            return f"{slug}/{FB} lost floating_row_cover, the prose's best single defense"

    # Order normalizations.
    for slug in WHITE_RUST_CROPS:
        ms, _ = ladder_of(batch[slug], "white-rust")
        if ms is None:
            return f"{slug} has no white-rust problem"
        if tuple(ms) != WHITE_RUST_ORDER:
            return (f"{slug}/white-rust is {ms}, not the normalized shared order; the three "
                    f"carriers ship the same five cultural rungs in the same order")
    for slug in DAMPING_OFF_CROPS:
        ms, _ = ladder_of(batch[slug], "damping-off")
        if ms is None:
            return f"{slug} has no damping-off problem"
        if tuple(ms) != DAMPING_OFF_ORDER:
            return (f"{slug}/damping-off is {ms}, not the normalized sowing-first order both "
                    f"crops' prevention prose uses")

    # Prose-driven divergences that must not level out.
    ms, _ = ladder_of(batch["bok-choy"], "cabbage-aphids")
    if ms is None or "horticultural_oil" not in ms:
        return ("bok-choy/cabbage-aphids lost horticultural_oil, the material its own prose "
                "names alongside soap and neem")
    return None


def check_catalog_premises(cm):
    """The corrected chemical-cohort cautions these rungs restate must be on the sheet."""
    spin = " ".join(cm.get("spinosad", {}).get("cautions") or [])
    if "dusk" not in spin:
        return ("spinosad's dusk caution is not on the sheet; the batch's spinosad rungs "
                "restate it")
    neem = " ".join(cm.get("neem_oil", {}).get("cautions") or [])
    if "sunset" not in neem or "midnight" not in neem:
        return ("neem_oil does not carry the medium-band bee caution; the chemical-cohort round "
                "must be on the sheet, since the neem rungs restate its prescription")
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
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
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
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST (unreachable below the bystander loops -- sixth time stated).
    for slug in COPPER_ON_DM:
        ms, _ = ladder_of(by[slug], DM)
        if "copper_fungicide" not in ms:
            return f"post: {slug}/{DM} lost its copper rung"
    for slug in NO_COPPER_ON_DM:
        ms, _ = ladder_of(by[slug], DM)
        if "copper_fungicide" in ms:
            return f"post: {slug}/{DM} gained a copper rung the read ruled out"
    ms, _ = ladder_of(by["lettuce-leaf"], DM)
    if "crop_rotation" in ms:
        return "post: lettuce-leaf/downy-mildew gained the rotation rung its prose contradicts"
    for slug in CROPS:
        ms, _ = ladder_of(by[slug], FB)
        if ms is not None and "neem_oil" in ms:
            return f"post: {slug}/{FB} regained neem_oil"
        for _, p in problems(by[slug]):
            if not p.get("control_ladder"):
                return f"post: {slug}/{p.get('id')}: no ladder after promote"
            for r in p["control_ladder"]:
                if "diatomaceous" in (r["note_beginner"] + " " + r["note_seasoned"]).lower():
                    return f"post: {slug}/{p.get('id')}: a diatomaceous earth mention landed"
    for slug in WHITE_RUST_CROPS:
        ms, _ = ladder_of(by[slug], "white-rust")
        if tuple(ms) != WHITE_RUST_ORDER:
            return f"post: {slug}/white-rust drifted from the normalized order"

    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints and edits nothing there"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"

    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):
                return (f"post: {CROPS[i]} and {CROPS[j]} carry identical ladder CONTENT; they "
                        f"were authored separately and their prose differs")
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

    print("PLA-8 BATCH 8 -- THE LEAFY GREENS (fall block, batch 1 of 5)")
    print(f"  crops        : {', '.join(CROPS)}  (FOUR authoring passes)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused (roster convention, incl. "
          f"beet-spinach-leafminer + cabbageworms reuses)")
    print(f"  read rulings : copper on downy mildew split by PROSE (lettuce+bok-choy YES,")
    print(f"                 spinach dropped, arugula never named); lettuce downy has NO rotation;")
    print(f"                 DE stripped and pinned out; 2 shared ladders order-normalized")
    print(f"  blast radius : 4 crops; methods 0; sources 0; bystanders 0")
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
