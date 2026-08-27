#!/usr/bin/env python3
"""PLA-8 BATCH 7 -- THE TOMATOES. Base 674fab25.

34 problems gain `id`, `type` and `control_ladder`; **154 rungs** across `beefsteak-tomato` (35),
`cherry-tomato` (35), `grape-tomato` (42) and `roma-tomato` (42). Roster laddered 29 -> 33. ONE
method minted: `splash_barrier_mulch`. No source, no other method, no crop outside the four.

**FOUR AUTHORING PASSES FOR FOUR CROPS.** Two shared-name families (beefsteak+cherry at 34.4%,
grape+roma at 68.1%) and no twin anywhere: each crop was authored independently from ITS OWN
prose, and the promote refuses byte-identical staged files or byte-identical post-state ladder
content in ANY of the six crop pairs.

**EVERY ID MATCHES THE ROSTER CONVENTION heirloom-tomato ALREADY SHIPS.** aphids, tomato-hornworm,
flea-beetles, spider-mites, whiteflies, early-blight, blossom-end-rot, septoria-leaf-spot,
late-blight, fusarium-verticillium-wilt. Ids are join keys (varieties[].resistance /
ladder_delta); the convention table below is checked name-by-name and a divergent mint is refused.

--------------------------------------------------------------------------------------------------
THE READ, AND ITS TWO ADJUDICATIONS (the cross-sibling conflicts verify flagged)
--------------------------------------------------------------------------------------------------
**`neem_oil` DROPPED from every flea-beetles ladder.** All four crops' prose names a neem spray
for flea beetles, and the key is LEGAL via applies_to insect_general -- but the catalog entry's
meaning is soft-bodied smothering/antifeedant, and a hard-shelled chewing beetle is a different
target than the entry means. Legal-but-wrong-meaning is the `bottom_watering` shape. Two of four
authoring agents refused it independently with exactly that reasoning; the read ruled their way.
THE DROP IS SCOPED, NOT A BLANKET REMOVAL: neem stays on aphids (all four), spider-mites
(beefsteak, cherry) and whiteflies (roma), where the crop prose and the entry's meaning agree.
The crops' flea-beetle neem advice is a recorded gap plus a finding: neem_oil's applies_to is
wider than its prose scope.

**`garden_sanitation` KEPT on every blossom-end-rot ladder** (added to grape, which had refused
it). The method's own MEANS covers "pulling the first affected leaves or fruit during the
season"; all four crops' prose instructs removing affected fruit; every note keeps the
culling-not-disease-control framing, since the disorder is stated non-contagious.

--------------------------------------------------------------------------------------------------
THE MINT: splash_barrier_mulch
--------------------------------------------------------------------------------------------------
All four agents independently reported the same control blocked: every crop's early-blight AND
septoria prose commands mulching the soil against splash, and no legal key carried it
(moisture_buffering_mulch is physiological-only and MEANS moisture; straw_mulch MEANS a
strawberry fruit barrier). Eight instances with nowhere to go is the playbook's mint signal, and
the melons/mancozeb model applies: growth, not debt. Both UMN anchors were fetched and READ from
live bytes on 2026-08-26; the leaf-spot page carries the mechanism sentence, the
acceptable-mulch list, and the herbicide-residue caution the entry restates. The staged spec
(tools/staging/pla8_batch7_tomatoes/mint_splash_barrier_mulch.json) must agree byte-for-byte
with the literal below, so staging and promote cannot drift apart.

--------------------------------------------------------------------------------------------------
THIS BATCH IS WHERE THE CHEMICAL-COHORT ROUND GETS TESTED AGAINST REAL DATA
--------------------------------------------------------------------------------------------------
The rungs restate the catalog cautions corrected HOURS before authoring, and the premises pin it:
  * copper_fungicide's acute-split caution (octanoate Low ... hydroxide DANGER) must be on the
    sheet -- grape's three copper rungs restate the split by name.
  * neem_oil's medium-band bee caution (sunset-to-midnight sentence) must be on the sheet -- the
    neem rungs' "keep it off anything in flower" is that band's prescription.
Prose-driven sibling divergence is pinned as data: only grape's whitefly ladder carries
horticultural_oil (its prose names hort oil; roma's names neem) and weed_host_control (grape's
prose names weedy alternate hosts; roma's does not).

REFUSALS: base SHA mismatch; the mint already present, or the staged spec disagreeing with the
literal; a crop already laddered; problem-count drift; a rung count off; an id off the roster
convention; a neem rung on any flea-beetles ladder, or neem missing where it was KEPT; a
blossom-end-rot ladder without its culling rung; early-blight/septoria without the splash rung
directly after water_at_the_base; the whitefly divergence collapsing either way; any pair of
staged files or post-state ladders byte-identical; an unknown method; a tier decrease;
applies_to incoherence; identical registers; either chemical-cohort caution absent from the
catalog; any crop outside the four, any other method, or any source changed.

Guard suite:      tools/test_promote_pla8_batch7.py
Mutation harness: tools/mutate_pla8_batch7_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch7.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch7_tomatoes")
BASE_SHA = "674fab251aec7063ffa970f8c81e6156ab6fdbcab1a5800d9a1c93627cdcd740"

CROPS = ("beefsteak-tomato", "cherry-tomato", "grape-tomato", "roma-tomato")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"beefsteak-tomato": 8, "cherry-tomato": 8, "grape-tomato": 9, "roma-tomato": 9}
EXPECTED_RUNGS = {"beefsteak-tomato": 35, "cherry-tomato": 35, "grape-tomato": 42, "roma-tomato": 42}

PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",
                "prevention_seasoned", "severity", "sources")

# Ids already shipped on the roster (heirloom-tomato carries all ten names but Whiteflies, whose
# id follows the same slug rule). A divergent mint is a join-key defect.
ID_CONVENTION = {
    "Aphids": "aphids",
    "Tomato hornworm": "tomato-hornworm",
    "Flea beetles": "flea-beetles",
    "Spider mites": "spider-mites",
    "Whiteflies": "whiteflies",
    "Early blight": "early-blight",
    "Blossom end rot": "blossom-end-rot",
    "Septoria leaf spot": "septoria-leaf-spot",
    "Late blight": "late-blight",
    "Fusarium and Verticillium wilt": "fusarium-verticillium-wilt",
}

MINT_KEY = "splash_barrier_mulch"
MINT = {
    "name": "Splash-barrier mulch",
    "tier": "cultural",
    "applies_to": ["fungal_foliar", "bacterial", "disease_general"],
    "how_it_works_beginner": (
        "A layer of mulch over the soil under the plant puts a barrier between the ground and the "
        "leaves. Many leaf diseases wait in the soil and ride rain splash up onto the lowest "
        "leaves, and mulch stops that ride at the ground."),
    "how_it_works_seasoned": (
        "Mulch covering the soil surface interrupts rain-splash dispersal of soilborne inoculum "
        "onto the lower canopy; landscape fabric, straw, plastic mulch, or dried leaves all serve, "
        "laid before the splash-driven part of the season."),
    "best_use": (
        "Under plants whose leaf diseases carry over in the soil and reach the foliage by rain "
        "splash, such as the tomato leaf blights and spots, laid at planting. Distinct from "
        "moisture buffering mulch, which manages soil moisture swings for disorders such as "
        "blossom end rot, and from straw mulch, which is a fruit-contact and splash barrier under "
        "strawberries."),
    "find_it_beginner": (
        "Any common garden mulch works as the barrier: straw, dried leaves, landscape fabric, or "
        "plastic mulch from the garden center."),
    "pros": [
        "Blocks the main soil-to-leaf route of splash-dispersed diseases without any spray",
        "Several everyday materials work: landscape fabric, straw, plastic mulch, or dried leaves",
    ],
    "cons": [
        "Does nothing against disease already on the foliage or arriving by air",
        "Needs to be in place before the splashy weather, not after spots appear",
    ],
    "cautions": [
        ("Do not use grass clippings or leaves from a lawn treated with an herbicide; residues "
         "carried in the mulch can injure the crop, and tomatoes are sensitive to many lawn "
         "herbicides"),
    ],
    "sources": ["umn_ext"],
    "anchoring_urls": {
        "umn_ext": {
            "url": "https://extension.umn.edu/plant-diseases/tomato-leaf-spot-diseases",
            "verified": "2026-08-26",
        }
    },
}

FB = "flea-beetles"
BER = "blossom-end-rot"
SPLASH_DISEASES = ("early-blight", "septoria-leaf-spot")
# Where the neem drop must NOT have leaked: the prose supports neem on these, per crop.
NEEM_KEPT = {
    "beefsteak-tomato": ("aphids", "spider-mites"),
    "cherry-tomato": ("aphids", "spider-mites"),
    "grape-tomato": ("aphids",),
    "roma-tomato": ("aphids", "whiteflies"),
}
# Prose-driven whitefly divergence between the two crops that have the problem.
GRAPE_ONLY_WF = ("horticultural_oil", "weed_host_control")


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


def staged_mint():
    return json.load(open(os.path.join(STAGING, "mint_splash_barrier_mulch.json")))


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
    """Two shared-name families (34.4% and 68.1%), four independent passes, six pairs refused in
    both directions: identical canonical prose would mean propagation was available; identical
    staged bytes would mean a pass did not happen."""
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
    """The two adjudications, the splash rungs, and the kept-where-it-belongs pins. `by` is the
    CANONICAL crop map: staged problems carry no `name`, so names resolve from canonical at the
    same index (reading them off the staged problem is the dead-guard shape batch 4 shipped)."""
    # SHAPE FIRST: which crops carry which problems. Below the id-convention loop this check is
    # unreachable, because an appended problem has no canonical name and trips the convention
    # refusal instead -- the dead-guard-below-a-stronger-neighbour shape, made reachable by order.
    for slug in ("beefsteak-tomato", "cherry-tomato"):
        if ladder_of(batch[slug], "whiteflies")[0] is not None:
            return f"{slug} gained a whiteflies problem its canonical record does not carry"
        if ladder_of(batch[slug], "fusarium-verticillium-wilt")[0] is not None:
            return f"{slug} gained a wilt problem its canonical record does not carry"

    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return (f"{slug}: problem {name!r} is not in the id-convention table; add its "
                        f"roster ruling before promoting")
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the roster ships "
                        f"{want!r}; ids are join keys and must not diverge between crops")

        # ADJUDICATION 1: neem off every flea-beetles ladder, and NOT as a blanket removal.
        mfb, _ = ladder_of(batch[slug], FB)
        if mfb is None:
            return f"{slug} has no {FB} problem"
        if "neem_oil" in mfb:
            return (f"{slug}/{FB} carries neem_oil, which is legal via insect_general but whose "
                    f"catalog meaning is soft-bodied smothering; a hard-shelled chewing beetle is "
                    f"the bottom_watering shape and the read dropped it on all four crops")
        if "floating_row_cover" not in mfb:
            return f"{slug}/{FB} lost floating_row_cover, the one prose-supported exclusion rung"
        for pid in NEEM_KEPT[slug]:
            ms, _ = ladder_of(batch[slug], pid)
            if ms is None:
                return f"{slug} has no {pid} problem"
            if "neem_oil" not in ms:
                return (f"{slug}/{pid} lost neem_oil; the flea-beetle drop was an adjudication "
                        f"scoped to the wrong-meaning target, not a blanket removal")

        # ADJUDICATION 2: the culling rung on every blossom-end-rot ladder.
        mber, _ = ladder_of(batch[slug], BER)
        if mber is None:
            return f"{slug} has no {BER} problem"
        if "garden_sanitation" not in mber:
            return (f"{slug}/{BER} has no garden_sanitation rung; the method's own MEANS covers "
                    f"pulling first affected fruit and all four crops' prose instructs it")

        # THE MINT'S RUNGS: splash mulch directly after water_at_the_base on both leaf diseases.
        for pid in SPLASH_DISEASES:
            ms, _ = ladder_of(batch[slug], pid)
            if ms is None:
                return f"{slug} has no {pid} problem"
            if MINT_KEY not in ms:
                return (f"{slug}/{pid} has no {MINT_KEY} rung; the crop's own prose commands "
                        f"splash mulching and the mint exists for exactly these eight rungs")
            if ms.index(MINT_KEY) != ms.index("water_at_the_base") + 1:
                return (f"{slug}/{pid}: {MINT_KEY} must sit directly after water_at_the_base, the "
                        f"splash pair the read placed together")

    # The prose-driven whitefly divergence, pinned in both directions.
    gwf, _ = ladder_of(batch["grape-tomato"], "whiteflies")
    rwf, _ = ladder_of(batch["roma-tomato"], "whiteflies")
    if gwf is None or rwf is None:
        return "grape-tomato and roma-tomato must both carry a whiteflies problem"
    for m in GRAPE_ONLY_WF:
        if m not in gwf:
            return (f"grape-tomato/whiteflies lost {m}, which its own prose supports (hort oil "
                    f"named as the material; weeds named as the reservoir)")
        if m in rwf:
            return (f"roma-tomato/whiteflies gained {m}, which its prose does not support; the "
                    f"divergence is prose-driven and must not be leveled")
    # roma/whiteflies keeping neem_oil is already enforced by NEEM_KEPT above; a second check
    # here would be dead code below a stronger neighbour.
    return None


def check_catalog_premises(cm):
    """The chemical-cohort corrections these rungs restate must already be on the sheet."""
    if MINT_KEY in cm:
        return f"{MINT_KEY} is already in the catalog; this promote has already run"
    if staged_mint().get("entry") != MINT:
        return ("the staged mint spec disagrees with this promote's literal; reconcile before "
                "promoting so staging and promote cannot drift apart")
    copper = " ".join(cm.get("copper_fungicide", {}).get("cautions") or [])
    if "copper hydroxide" not in copper:
        return ("copper_fungicide does not carry the acute-split caution naming copper hydroxide; "
                "the chemical-cohort round must land before these ladders ship, since grape's "
                "copper rungs restate the split")
    neem = " ".join(cm.get("neem_oil", {}).get("cautions") or [])
    if "sunset" not in neem or "midnight" not in neem:
        return ("neem_oil does not carry the medium-band bee caution; the chemical-cohort round "
                "must land before these ladders ship, since the neem rungs restate its "
                "prescription")
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

    # The ladders must be legal against the catalog AS IT WILL BE, mint included.
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
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
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

    # SUBSTANTIVE INVARIANTS FIRST. Below the bystander loops they are unreachable, because a
    # change to any of the four crops IS a change to a crop. Fifth time this arc has needed the
    # ordering stated.
    if json.loads(post["methods"].get(MINT_KEY, "null")) != json.loads(
            json.dumps(MINT, sort_keys=True)):
        return f"post: {MINT_KEY} did not land verbatim"
    for slug in CROPS:
        mfb, _ = ladder_of(by[slug], FB)
        if "neem_oil" in mfb:
            return f"post: {slug}/{FB} regained neem_oil"
        for pid in NEEM_KEPT[slug]:
            ms, _ = ladder_of(by[slug], pid)
            if "neem_oil" not in ms:
                return f"post: {slug}/{pid} lost neem_oil; the drop was scoped to flea-beetles"
        mber, _ = ladder_of(by[slug], BER)
        if "garden_sanitation" not in mber:
            return f"post: {slug}/{BER} lost its culling rung"
        for pid in SPLASH_DISEASES:
            ms, _ = ladder_of(by[slug], pid)
            if MINT_KEY not in ms:
                return f"post: {slug}/{pid} lost its {MINT_KEY} rung"
        for _, p in problems(by[slug]):
            if not p.get("control_ladder"):
                return f"post: {slug}/{p.get('id')}: no ladder after promote"
    gwf, _ = ladder_of(by["grape-tomato"], "whiteflies")
    rwf, _ = ladder_of(by["roma-tomato"], "whiteflies")
    for m in GRAPE_ONLY_WF:
        if m not in gwf or m in rwf:
            return f"post: the whitefly divergence collapsed on {m}"

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
        return "post: source_catalog changed, and this promote mints no source"

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

    print("PLA-8 BATCH 7 -- THE TOMATOES")
    print(f"  crops        : {', '.join(CROPS)}  (two shared-name families, FOUR authoring passes)")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused (all on the roster convention)")
    print(f"  read rulings : neem_oil OFF every flea-beetles ladder (kept where prose supports it);")
    print(f"                 garden_sanitation ON every blossom-end-rot ladder")
    print(f"  mint         : {MINT_KEY} (+8 rungs on the two splash diseases x 4 crops)")
    print(f"  blast radius : 4 crops + 1 minted method; sources 0; bystanders 0")
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
