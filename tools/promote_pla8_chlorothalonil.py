#!/usr/bin/env python3
"""PLA-8: mint `chlorothalonil`, the conventional fungicide the catalog could not express. Base 3a87737a.

ONE NEW KEY in `control_methods`, 55 -> 56. NO existing method is touched, NO crop, NO source_catalog
entry, NO ladder. The rungs are a separate promote.

WHY IT IS OWED. Both `conventional` entries in this catalog are INSECTICIDES (`carbaryl`,
`pyrethroid`), so nothing conventional could reach a fungal problem, and only three methods reached
one at all (`copper_fungicide`, `sulfur`, `biofungicide`). Measured against `3a87737a`:
**chlorothalonil is named in 11 problems' prose, 9 of them ALREADY LADDERED.** Three of those nine
(cucumber, slicing-cucumber, pickling-cucumber anthracnose) name it as the ONLY spray and their
ladders top out at `garden_sanitation`, which is cultural. Those ladders end at "clear the debris"
while the crop's own source says a fungicide suppresses the disease. Named as a gap by batch 3 and
by both bean passes in batch 5.

IT IS ON THE SHELF, AND THAT IS THE TEST THAT MATTERED. UC IPM lists home-garden products by name,
and its footnote says those come from the California DPR database and an annual RETAIL SHELF SURVEY.
Clemson puts chlorothalonil in a home-garden fungicide table with a 0 day pre-harvest interval. Two
extension services recommend it to home gardeners and it is ordinary garden center stock, so the
catalog's job is to name it fairly with honest cautions rather than to omit it.

THE HAZARD PROFILE IS THE HEAVIEST IN THIS CATALOG, AND IT IS STATED RATHER THAN SOFTENED. UC IPM's
Pesticide Active Ingredients Database rates water quality risk to aquatic wildlife **High**, acute
toxicity to people and other mammals **High** (the DANGER signal-word band), and lists the material
on **both the California Prop 65 list and the US EPA list**, where footnote 6 says an active
ingredient appears only if it is "a likely or confirmed carcinogen". Bee rating **II**. Natural
enemies **Low**, the one axis where it compares well with the conventional insecticides.

**THIS IS THE FIRST METHOD IN THE CATALOG CARRYING A CHRONIC-HEALTH DISCLOSURE.** Ruled by Trevor
2026-08-26: if a product is on the shelf for people to buy and use, the ladder names it and states
what it is. Recorded because it sets a precedent, and because `carbaryl` has a chronic profile its
own sheet does not mention -- see the OWED note below.

THE RATINGS CAME FROM A SCREENSHOT, NOT FROM A FETCH, AND THE DIFFERENCE WAS MATERIAL. WebFetch's
markdown parse of that page's two-level hazard table SHIFTED THE COLUMNS: it reported Acute **L**
and three ratings as "Information to be added", against the rendered page's Acute **H**. Acute L vs
H is CAUTION versus DANGER. The prose below is written from the rendered table. This is the
documented `webfetch-markdown-table-column-shift` failure, and it is the second time this catalog
has been bitten by it.

OWED, AND OPENED BY THIS MINT, NOT CLOSED BY IT:
  * `carbaryl` and `pyrethroid` were sourced before that parse bug was known, and neither carries a
    chronic-health line. Both should be re-read against their own UC IPM pages FROM THE RENDERED
    TABLE before their cautions are trusted.
  * `mancozeb` is named alongside chlorothalonil on watermelon and cantaloupe (both unladdered). Its
    UC IPM page exists in the same database; it is not minted here because it was not read.
  * Chlorothalonil sits inside fields named `organic_treatment_seasoned` on all 11 problems. A
    conventional synthetic recommended in a field named `organic_` is a framing defect batch 3
    flagged and this promote neither fixes nor worsens.

REFUSALS: base SHA mismatch; the key already present; a missing required field; `applies_to` not
exactly ['fungal_foliar']; the tier not `conventional`; any hazard disclosure missing from the
cautions; a source not in source_catalog or not T1; a declared source with no anchoring_url; copy
hygiene; and post-state blast radius.

Guard suite:      tools/test_promote_pla8_chlorothalonil.py
Mutation harness: tools/mutate_pla8_chlorothalonil_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_chlorothalonil.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "3a87737a60c544453497f67bc3744d8534a400cbcba795b6e4b23fdcbabc3cb5"

KEY = "chlorothalonil"
VERIFIED = "2026-08-26"

METHOD = {
    "name": "Chlorothalonil",
    "tier": "conventional",
    # Narrow on purpose: every one of the 11 problems naming it is a foliar fungal disease, and
    # Clemson's table lists it for leaf spots, downy mildew, gummy stem blight and powdery mildew.
    "applies_to": ["fungal_foliar"],
    "how_it_works_beginner":
        "Chlorothalonil is a synthetic fungicide that coats the leaf surface and stops fungal "
        "spores from taking hold there. It protects tissue that is still clean and does nothing "
        "for leaves already infected, so it only pays if it goes on before the disease arrives or "
        "at the very first spots, and it has to be repeated on the label's schedule. It is the "
        "strongest thing on a garden center shelf for several leaf diseases, and it carries the "
        "heaviest warnings of anything in this guide, so it belongs at the end of the list rather "
        "than the start. Stopping one step below it is a reasonable choice, not a failure.",
    "how_it_works_seasoned":
        "UC IPM describes it as a broad-spectrum, protectant fungicide that inhibits fungal growth "
        "on plant leaves. Protectant means multi-site contact activity on the leaf surface rather "
        "than systemic movement, so coverage and timing carry the result and reapplication runs on "
        "the label interval through the risk period. The hazard profile is the heaviest of any "
        "method here and is worth reading before reaching for it: UC IPM rates water quality risk "
        "to aquatic wildlife High and acute toxicity to people and other mammals High, the DANGER "
        "signal-word band, with that rating taken from the most sensitive route of entry rather "
        "than from oral toxicity. It appears on both the California Prop 65 list and the US EPA "
        "list, where an active ingredient is listed only as a likely or confirmed carcinogen. Risk "
        "to natural enemies is rated Low, which is the one axis where it compares well against the "
        "conventional insecticides.",
    "best_use":
        "A rescue-only last resort for a foliar disease the cultural and soft rungs have not held, "
        "on a crop whose own guidance names it. Preventive by nature, so it buys nothing applied "
        "late. Distinct from copper fungicide and sulfur, which sit below it and are the softer "
        "options to exhaust first; this is not a routine choice and a reader who declines it has "
        "not skipped a step they owed.",
    "find_it_beginner":
        "Sold for home gardens as Bonide Fung-Onil and GardenTech Daconil Fungicide; on the label, "
        "look for chlorothalonil as the active ingredient. Check that the label lists your crop "
        "before you buy.",
    "pros": [
        "Broad-spectrum and effective against several leaf diseases at once, including some the "
        "softer rungs cannot reach at all",
        "Rated Low risk to natural enemies, so it does not strip out the predators working on the "
        "bed's other problems",
        "Clemson lists a 0 day pre-harvest interval for home garden use, so a treated crop is not "
        "lost to a waiting period",
    ],
    "cons": [
        "Preventive only: it protects clean tissue and does nothing for leaves that are already "
        "infected",
        "Rated High for water quality risk and High for acute toxicity to people and other mammals",
        "One application is rarely the whole job, since it has to be repeated on the label interval "
        "through the risk period",
    ],
    "cautions": [
        "Rated High for water quality risk to aquatic wildlife; keep spray and runoff away from "
        "ponds, streams, storm drains and puddles",
        "UC IPM rates acute toxicity to people and other mammals High, the DANGER signal-word band, "
        "and notes the rating follows the most sensitive route of entry rather than oral toxicity",
        "Listed on both the California Prop 65 list and the US EPA list, where an active ingredient "
        "appears only as a likely or confirmed carcinogen; weigh that before choosing it on a food "
        "crop",
        "Bee rating II: do not apply it, or let it drift, onto anything in flower including weeds, "
        "except between sunset and midnight where the label allows, and do not let it reach water "
        "bees can drink",
        "Many consumer products do not print protective equipment on the label; wear chemical "
        "resistant gloves, long sleeves and goggles regardless",
        "Observe the pre-harvest interval on the label before eating the crop, and read and follow "
        "the label every time",
    ],
    "sources": ["ucanr_ext", "clemson_hgic"],
    "anchoring_urls": {
        "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/"
                             "pesticide-active-ingredients-database/active-ingredient-details/"
                             "?uaiKey=115",
                      "verified": VERIFIED},
        "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/"
                                "cucumber-squash-melon-other-cucurbit-diseases/",
                         "verified": VERIFIED},
    },
}

# Every hazard axis the rendered UC IPM table shows. A method that names a conventional synthetic on
# a home-garden ladder and omits one of these is understating what it is asking the reader to buy.
REQUIRED_DISCLOSURES = {
    "aquatic":    ("water quality", "aquatic"),
    "acute":      ("acute toxicity", "danger"),
    "carcinogen": ("prop 65", "carcinogen"),
    "bees":       ("bee rating ii", "flower"),
    "ppe":        ("gloves", "goggles"),
    "phi":        ("pre-harvest interval",),
}

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


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


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def missing_disclosures(m):
    """Which hazard axes the cautions fail to state. Each needs ALL of its tokens present."""
    blob = " ".join(m.get("cautions") or []).lower()
    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()
                  if not all(t in blob for t in toks))


def check(data):
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    if KEY in cm:
        return f"{KEY} is already in the catalog"
    for f in REQUIRED:
        if f not in METHOD or not METHOD[f]:
            return f"mint is missing required field {f!r}"
    if METHOD["tier"] != "conventional":
        return (f"tier is {METHOD['tier']!r}; this is a synthetic rescue material and belongs at "
                f"the conventional rung or the ladder understates what it is")
    if METHOD["applies_to"] != ["fungal_foliar"]:
        return (f"applies_to must be exactly ['fungal_foliar']; every problem naming this material "
                f"is a foliar fungal disease and a wider scope would put a DANGER-band synthetic "
                f"in front of readers whose sources never mention it")

    # THE DISCLOSURE GUARD. This is the whole reason the method is safe to ship.
    miss = missing_disclosures(METHOD)
    if miss:
        return (f"the cautions do not state {miss}; UC IPM's rendered hazard table rates this High "
                f"for water quality and High for acute toxicity and lists it on the Prop 65 and EPA "
                f"carcinogen lists, and a home-garden ladder that omits any of those understates "
                f"what it is asking the reader to buy")

    for s in METHOD["sources"]:
        if s not in sc:
            return f"source {s!r} is not in source_catalog"
        if (sc[s].get("tier") or "").upper() != "T1":
            return f"source {s!r} is not T1"
        if s not in METHOD["anchoring_urls"]:
            return f"source {s!r} has no anchoring_url"
    for s, a in METHOD["anchoring_urls"].items():
        if s not in METHOD["sources"]:
            return f"anchoring_url {s!r} is not a declared source"
        if not str(a.get("url", "")).startswith("https://"):
            return f"anchoring_url {s!r} is not https"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
            return f"anchoring_url {s!r} has no valid verified date"

    for s in prose_of(METHOD):
        bad = hygiene(s)
        if bad:
            return f"prose fails copy hygiene ({bad}): {s[:70]!r}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": dump(data["source_catalog"]),
            "crops": dump(data["crops"])}


def apply_to(data):
    if KEY in data["control_methods"]:
        raise AssertionError(f"{KEY} already in the catalog")
    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))
    return 1


def verify_post(pre, data):
    cm = data["control_methods"]
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST, or the blast-radius loop answers for them.
    if KEY not in cm:
        return "post: the method was not minted"
    miss = missing_disclosures(cm[KEY])
    if miss:
        return f"post: the shipped cautions do not state {miss}"
    if cm[KEY]["applies_to"] != ["fungal_foliar"]:
        return "post: applies_to is not the narrow scope"
    if cm[KEY]["tier"] != "conventional":
        return "post: the tier is not conventional"

    added = set(post["methods"]) - set(pre["methods"])
    if added != {KEY}:
        return f"post: methods added {sorted(added)}, expected exactly ['{KEY}']"
    if set(pre["methods"]) - set(post["methods"]):
        return "post: a method was dropped"
    for k, before in pre["methods"].items():
        if post["methods"][k] != before:
            return f"post: existing method {k!r} changed, and this promote only mints"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote mints no source"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed; the rungs are a separate promote"
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
    before = len(data["control_methods"])
    apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print(f"PLA-8 -- mint {KEY}, the conventional fungicide the catalog could not express")
    print(f"  control_methods : {before} -> {len(data['control_methods'])}")
    print(f"  tier            : {METHOD['tier']}   applies_to: {METHOD['applies_to']}")
    print(f"  disclosures     : {sorted(REQUIRED_DISCLOSURES)} all stated")
    print(f"  crops touched   : 0   existing methods touched: 0   sources touched: 0")
    print(f"  NOTE            : 9 shipped ladders name this material and gain no rung here; "
          f"the backfill is a separate promote")
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
