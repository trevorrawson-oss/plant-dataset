#!/usr/bin/env python3
"""PLA-8: mint `mancozeb`, the second conventional fungicide, ahead of the melons. Base b6d36611.

ONE NEW KEY in `control_methods`, 60 -> 61. NO existing method is touched, NO crop, NO
source_catalog entry, NO ladder. The rungs land in batch 14's own promote (the melons name this
material); minting FIRST is what puts the key in the authoring brief, since agents may only name
catalog keys.

WHY IT IS OWED. cantaloupe's Alternaria leaf blight and watermelon's Anthracnose both say "treat
at the first spots with a labeled fungicide such as chlorothalonil or mancozeb". Chlorothalonil
exists (minted `d096415`); mancozeb was named in that mint's OWED list and deliberately not minted
because it had not been read. Batch 14 is the melons, so the read happened now.

IT IS ON THE SHELF, AND THE TEST RAN THE CARBARYL WAY. UC IPM's California survey lists NO example
home products for mancozeb ("No example products containing this active ingredient can be listed
at this time"), which is the same signal that nearly dropped carbaryl -- and a California shelf
survey is not the world. Clemson's cucurbit-disease factsheet carries mancozeb in its HOME-GARDEN
fungicide table with a named retail product (Southern Ag Dithane M-45), a 5 day pre-harvest
interval, and a gummy stem blight indication; the table is dated as updated 6/25. The row was
verified from the RAW HTML, not a markdown table parse (the column-shift lesson).

THE HAZARD PROFILE, READ THROUGH THE TESTED INSTRUMENT. `tools/ucipm_uaidb.py` (offline positive
control 5/5 green in the same pass) against uaiKey=30:

  water quality        H      (High risk to aquatic wildlife)
  acute toxicity       L      (the CAUTION signal-word band, mildest of the three)
  chronic              on the CA Prop 65 list AND the US EPA list (likely or confirmed carcinogen)
  honey bees           low
  natural enemies      NO RATING ("--")
  mode                 "broad-spectrum, contact, protectant fungicide ... disrupts cellular
                        processes of fungal cells ... kills on contact and provides residual
                        protection from later fungal infections"

This matches the chem-cohort's birth-time read (water H, bees low, acute L, Prop 65 + EPA)
figure for figure, re-verified rather than trusted.

TWO AXES DIFFER FROM CHLOROTHALONIL AND THE ENTRY MUST NOT INHERIT ITS SIBLING'S SENTENCES:
acute is L/CAUTION here (chlorothalonil is H/DANGER), so the acute line is a PRO stated
honestly, not a caution copied across; and natural enemies is UNRATED here (chlorothalonil is
rated Low), so this entry must not claim the natural-enemies advantage its sibling earns --
"unrated is not the same as low" is itself a required disclosure. The 5 day PHI (chlorothalonil:
0 days) is the third divergence and gets its own caution.

REFUSALS: base SHA mismatch; the key already present; a missing required field; `applies_to` not
exactly ['fungal_foliar']; the tier not `conventional`; any hazard disclosure missing from the
cautions; a natural-enemies LOW claim anywhere in the entry (the sibling's pro, unearned here);
a source not in source_catalog or not T1; a declared source with no anchoring_url; copy hygiene;
a crop gaining a rung here; and post-state blast radius.

Guard suite:      tools/test_promote_pla8_mancozeb.py
Mutation harness: tools/mutate_pla8_mancozeb_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_mancozeb.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "b6d366114461fe470aa07c48f18f83ade9e584b86a70898fd12ab5651884088d"

KEY = "mancozeb"
VERIFIED = "2026-08-30"

METHOD = {
    "name": "Mancozeb",
    "tier": "conventional",
    # Narrow on purpose: both problems naming it are foliar fungal diseases, and Clemson's
    # home-garden row lists it for gummy stem blight, another one.
    "applies_to": ["fungal_foliar"],
    "how_it_works_beginner":
        "Mancozeb is a synthetic fungicide that coats the leaf surface, kills the fungal spores "
        "it lands on, and leaves a protective film against the ones that arrive later. It shields "
        "leaves that are still clean and does nothing for tissue already infected, so it only "
        "pays if it goes on before the disease builds or at the very first spots, repeated on "
        "the label's schedule. It sits at the end of the list with the other synthetic rescue "
        "materials, and choosing to stop one rung short of it is a legitimate decision.",
    "how_it_works_seasoned":
        "UC IPM describes it as a broad-spectrum, contact, protectant fungicide that disrupts "
        "cellular processes of fungal cells, killing on contact and providing residual "
        "protection from later infections. Multi-site contact activity means coverage and timing "
        "carry the result, with reapplication on the label interval through the risk period. The "
        "hazard profile reads differently from chlorothalonil, the material the crop guidance "
        "names in the same breath: acute toxicity to people and other mammals is rated Low, the "
        "CAUTION signal-word band, and bee impact is rated low, but water quality risk to "
        "aquatic wildlife is High, it appears on both the California Prop 65 list and the US EPA "
        "list, where an active ingredient is listed only as a likely or confirmed carcinogen, "
        "and UC IPM shows no rating at all for its risk to natural enemies. Clemson carries it "
        "for home gardens with a 5 day pre-harvest interval.",
    "best_use":
        "A rescue-only last resort for a foliar fungal disease the cultural and soft rungs have "
        "not held, on a crop whose own guidance names it, most often in the same breath as "
        "chlorothalonil. Preventive by nature, so it buys nothing applied late. Distinct from "
        "copper fungicide and sulfur, which sit below it and are the softer options to exhaust "
        "first. Distinct from chlorothalonil on the axes a buyer might weigh: milder on acute "
        "toxicity, longer on the pre-harvest wait, and unrated rather than rated Low on natural "
        "enemies. A reader who declines both has not skipped a step they owed.",
    "find_it_beginner":
        "Sold for home gardens as Southern Ag Dithane M-45; on the label, look for mancozeb as "
        "the active ingredient and check that the label lists your crop before you buy. UC IPM's "
        "California shelf survey lists no example products for it, so expect to hunt for it at "
        "garden centers and farm stores rather than finding it beside the common fungicides.",
    "pros": [
        "Broad-spectrum contact protectant that kills spores on contact and leaves residual "
        "protection against later infections",
        "Rated Low for acute toxicity to people and other mammals, the CAUTION signal-word "
        "band, the mildest of the three",
        "Rated low impact on honey bees in UC IPM's database",
    ],
    "cons": [
        "Protectant only: it shields clean tissue and does nothing for leaves already infected",
        "Rated High for water quality risk, and it sits on the same Prop 65 and EPA carcinogen "
        "lists as chlorothalonil",
        "Carries a 5 day pre-harvest interval for home garden use where chlorothalonil's is 0, "
        "and its risk to natural enemies is unrated rather than known to be low",
    ],
    "cautions": [
        "Rated High for water quality risk to aquatic wildlife; keep spray and runoff away from "
        "ponds, streams, storm drains and puddles",
        "Listed on both the California Prop 65 list and the US EPA list, where an active "
        "ingredient appears only as a likely or confirmed carcinogen; weigh that before "
        "choosing it on a food crop",
        "UC IPM shows no rating for its risk to natural enemies. Unrated is not the same as "
        "low, so do not treat it as the gentler choice for a bed where predators are doing "
        "work",
        "Many consumer products do not print protective equipment on the label; wear chemical "
        "resistant gloves, long sleeves and goggles regardless",
        "Observe the 5 day pre-harvest interval Clemson lists for home garden use before "
        "eating the crop, and read and follow the label every time",
    ],
    "sources": ["ucanr_ext", "clemson_hgic"],
    "anchoring_urls": {
        "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/"
                             "pesticide-active-ingredients-database/active-ingredient-details/"
                             "?uaiKey=30",
                      "verified": VERIFIED},
        "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/"
                                "cucumber-squash-melon-other-cucurbit-diseases/",
                         "verified": VERIFIED},
    },
}

# Every load-bearing hazard axis. acute-L and bees-low are stated as pros (honest, favorable);
# the axes below are the ones a home-garden ladder must not understate.
REQUIRED_DISCLOSURES = {
    "aquatic":    ("water quality", "aquatic"),
    "carcinogen": ("prop 65", "carcinogen"),
    "unrated":    ("natural enemies", "unrated is not the same as low"),
    "ppe":        ("gloves", "goggles"),
    "phi":        ("5 day pre-harvest interval",),
}

# The sibling's pro this entry must NOT inherit: chlorothalonil is rated Low on natural enemies;
# mancozeb is UNRATED, and claiming the advantage would invent a rating the database does not
# carry (the neem invented-bee-rating shape). Checked SENTENCE-WISE in both word orders ("Rated
# Low risk to natural enemies" is the house phrasing and puts Low FIRST); a sentence pairing the
# two is legitimate only when it says the rating does not exist.
UNRATED_MARKERS = ("unrated", "no rating")

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


def invented_enemy_rating(m):
    """The sentence, if any, that claims a natural-enemies rating the database does not carry.

    Every legitimate pairing of 'natural enemies' and 'low' in this entry is an
    unrated-is-not-low statement; any other pairing, in either word order, is the
    invented-rating shape that put a bee numeral on chlorothalonil for six hours."""
    for s in prose_of(m):
        for sent in re.split(r"(?<=[.!?])\s+", s):
            low = sent.lower()
            if "natural enemies" not in low or not re.search(r"\blow\b", low):
                continue
            if not any(mk in low for mk in UNRATED_MARKERS):
                return sent
    return None


def rungs_of(data, key):
    out = []
    for c in data.get("crops") or []:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                for r in p.get("control_ladder") or []:
                    if r.get("method") == key:
                        out.append((c.get("slug"), p.get("id") or p.get("name")))
    return sorted(out)


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
        return (f"applies_to must be exactly ['fungal_foliar']; both problems naming this "
                f"material are foliar fungal diseases and a wider scope would put a Prop 65 "
                f"synthetic in front of readers whose sources never mention it")

    miss = missing_disclosures(METHOD)
    if miss:
        return (f"the cautions do not state {miss}; the rendered UC IPM record rates this High "
                f"for water quality, lists it on the Prop 65 and EPA carcinogen lists, and shows "
                f"NO natural-enemies rating, and a home-garden ladder that omits any of those "
                f"understates what it is asking the reader to buy")

    bad = invented_enemy_rating(METHOD)
    if bad:
        return (f"the entry claims a natural-enemies rating the database does not carry: "
                f"{bad[:80]!r}; UC IPM shows no rating, and inventing one is the neem shape")

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

    # SUBSTANTIVE INVARIANTS FIRST; the verbatim check stays LAST of this group so each branch
    # is reachable by a plain post-state mutation.
    if KEY not in cm:
        return "post: the method was not minted"
    miss = missing_disclosures(cm[KEY])
    if miss:
        return f"post: the shipped cautions do not state {miss}"
    bad = invented_enemy_rating(cm[KEY])
    if bad:
        return f"post: the shipped entry claims a natural-enemies rating: {bad[:80]!r}"
    if cm[KEY]["applies_to"] != ["fungal_foliar"]:
        return "post: applies_to is not the narrow scope"
    if cm[KEY]["tier"] != "conventional":
        return "post: the tier is not conventional"
    if cm[KEY] != METHOD:
        return "post: the method did not land verbatim"

    landed = rungs_of(data, KEY)
    if landed:
        return (f"post: {landed} gained a {KEY} rung, and this promote mints only; the rungs "
                f"land in batch 14's own promote")

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
    # CHAIN-REPLAY CONTRACT: batch 14 sits on this mint's output until it commits.
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
    before = len(data["control_methods"])
    apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print(f"PLA-8 -- mint {KEY}, the second conventional fungicide, ahead of the melons")
    print(f"  control_methods : {before} -> {len(data['control_methods'])}")
    print(f"  tier            : {METHOD['tier']}   applies_to: {METHOD['applies_to']}")
    print(f"  disclosures     : {sorted(REQUIRED_DISCLOSURES)} all stated")
    print(f"  divergences     : acute L/CAUTION (pro, stated honestly); natural enemies UNRATED "
          f"(disclosed, never claimed); 5 day PHI")
    print(f"  crops touched   : 0   existing methods touched: 0   sources touched: 0")
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
