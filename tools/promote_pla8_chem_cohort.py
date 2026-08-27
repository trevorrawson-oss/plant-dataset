#!/usr/bin/env python3
"""PLA-8: the chemical-cohort close-out -- the seven pilot-era soft chemicals re-read. Base 04b5aa69.

This is the round that closes the catalog's safety-bearing surface. Of 56 methods, ten are a
chemical a person applies to food; three (the conventional tier) were re-read on 2026-08-26 and
these seven -- copper_fungicide, sulfur, neem_oil, spinosad, insecticidal_soap, horticultural_oil,
iron_phosphate_slug_bait -- are the rest, sourced at the 2026-07-22/23 pilot and never held against
UC IPM's hazard database. After this promote the catalog audit is DECLARED CLOSED.

THE READ USED THE VALIDATED INSTRUMENT. `tools/ucipm_uaidb.py` parses the two-level hazard grid
from RAW HTML (the bee cell is an empty <span> carrying its value in a CSS class; a markdown
flattener column-shifts). The offline control (`tools/test_ucipm_uaidb.py`) passed in this pass,
and chlorothalonil (uaiKey=115) was re-fetched LIVE as the positive control before any of the
thirteen pages below were trusted: H / L / medium / H / Prop 65 + US EPA, matching the rendered
screenshot of 2026-08-26.

WHAT THE READ FOUND. Four methods change, three survive byte for byte:

  * NEEM'S BEE RATING WAS INVENTED, AND IT LIVES IN THREE FIELDS. The caution says "UC IPM rates
    neem low in toxicity to bees"; UC IPM's band for neem oil (38) AND azadirachtin (91) is
    MEDIUM, and pn7404 -- the caution's own anchor -- makes no bee-rating claim for neem at all.
    The same false rating sits in the entry's `pros` ("Low toxicity to people, pets, and
    pollinators") and in ONE live rung: strawberry / aphids / note_seasoned. The PRESCRIPTION
    (apply at dusk) is the medium band's own sunset-to-midnight allowance and is kept; only the
    rating claim changes. Same shape as chlorothalonil's "Bee rating II".
  * THE COPPER CLASS SPLITS ON ACUTE AND THE SPLIT IS PURCHASING ADVICE. Copper octanoate (the
    copper soap; the only one of the four with home products in UC IPM's retail survey, and the
    form our own find_it names) and copper ammonium complex are acute Low; copper oxychloride
    sulfate is Moderate; copper hydroxide is HIGH, the DANGER signal-word band. None of the four
    carries a chronic listing. The entry said nothing about any of this; the new caution names
    which. (Copper hydroxide alone carries a bee band, medium; the home form is unrated, the
    entry gives no bee timing advice, so no bee caution is authored -- recorded, not forgotten.)
  * INSECTICIDAL SOAP IS ACUTE MODERATE, and the entry's pros claimed "Low toxicity to people,
    pets, and pollinators". The pollinator half is right (bee band: low); the people/mammal half
    is not. The pro is narrowed to the supported half and a caution states the Moderate rating
    with its mild counterweights (chronic no known risk, lowest bee band).
  * HORTICULTURAL OIL IS BEE-MEDIUM AND SAID NOTHING. Its sibling contact sprays (neem, spinosad)
    both carry bee cautions; this one advised nothing either way, which is silence rather than
    wrong advice, but under the disclosure standard a contact spray in the medium band states its
    window. The standard medium-band sentence is appended.

THE THREE KEPT BYTE FOR BYTE, EACH VERIFIED AGAINST ITS PAGE, NOT SKIPPED:
  * spinosad (64): band medium -- its "spray at dusk" is the band's own allowance, and "do not
    apply to flowering plants" is stricter than the band requires. Chronic NKR. Correct as shipped.
  * sulfur (70): bees low (no precaution owed), natural enemies L-to-H with the H half already
    disclosed via the predatory-mite caution, acute L, chronic NKR. Correct as shipped.
  * iron_phosphate_slug_bait (24): bees low, acute Very Low, chronic NKR. The entry means iron
    phosphate, not ferric sodium EDTA (8, also read: the OTHER slug-bait chemistry, acute L), and
    every safety claim is the comparative "safer ... than metaldehyde", which survives.

ANCHORS ARE ADDED, NO SOURCE IS MINTED: `ucipm_uaidb` was minted by the conventional round; the
four changed methods declare it and anchor their OWN ingredient pages. The three kept methods do
not gain a source, because their entries' claims still rest on their pest notes; their uaidb
verification is recorded here and in the close-out, not in their `sources`.

REFUSALS: base SHA mismatch; the neem defect absent from any of its three fields (premise); a
medium-band method claiming a low bee rating anywhere in its copy; an authored medium-band bee
caution losing its sunset-to-midnight window; a copper named on the wrong side of the acute split;
a disclosure axis missing; a preserved claim dropped or smuggled; `ucipm_uaidb` absent from
source_catalog; copy hygiene; and blast radius (three kept methods, every bystander method, every
other crop, and the ENTIRE source_catalog must be byte-identical).

Guard suite:      tools/test_promote_pla8_chem_cohort.py
Mutation harness: tools/mutate_pla8_chem_cohort_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_chem_cohort.py [--apply] [--dry-run]
"""
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "04b5aa69b2f1fd209d84c4affb975cb78df0ee59657f9259b2896edbbe11c5f9"
VERIFIED = "2026-08-26"
SOURCE_ID = "ucipm_uaidb"
UAI = "https://ipm.ucanr.edu/home-and-landscape/pesticide-active-ingredients-database"
DETAIL = UAI + "/active-ingredient-details/?uaiKey=%s"

# ---------------------------------------------------------------------------------------------
# MEASURED 2026-08-26 from the RAW HTML grid; chlorothalonil re-fetched live as the positive
# control before any other page was trusted. uaiKey -> (name, water, nat_enemies, bee, acute,
# chronic). "--" is an empty cell on the page; "unrated" is a bee cell with no band class.
# ---------------------------------------------------------------------------------------------
RATINGS = {
    "115": ("chlorothalonil",                "H",   "L",  "medium",  "H",  "prop65+epa"),
    "123": ("copper ammonium complex",       "--",  "--", "unrated", "L",  "nkr"),
    "124": ("copper hydroxide",              "LH",  "--", "medium",  "H",  "nkr"),
    "125": ("copper octanoate",              "--",  "--", "unrated", "L",  "nkr"),
    "126": ("copper oxychloride sulfate",    "--",  "--", "unrated", "M",  "nkr"),
    "70":  ("sulfur",                        "L",   "LH", "low",     "L",  "nkr"),
    "38":  ("neem oil",                      "L",   "L",  "medium",  "L",  "nkr"),
    "91":  ("azadirachtin",                  "M",   "LM", "medium",  "VL", "nkr"),
    "64":  ("spinosad",                      "L",   "LM", "medium",  "L",  "nkr"),
    "50":  ("potassium salts of fatty acids", "--", "LM", "low",     "M",  "nkr"),
    "142": ("horticultural oil",             "NKR", "L",  "medium",  "L",  "nkr"),
    "24":  ("iron phosphate",                "--",  "L",  "low",     "VL", "nkr"),
    "8":   ("ferric sodium EDTA",            "--",  "--", "low",     "L",  "nkr"),
}

# The bee band each METHOD trades under, from the governing ingredient rows above. The copper
# class is "mixed": hydroxide medium, the home-garden form (octanoate) unrated, and the entry
# gives no bee timing advice, so no bee caution is authored for it.
BAND_OF = {
    "copper_fungicide": "mixed",
    "sulfur": "low",
    "neem_oil": "medium",
    "spinosad": "medium",
    "insecticidal_soap": "low",
    "horticultural_oil": "medium",
    "iron_phosphate_slug_bait": "low",
}
COHORT = tuple(BAND_OF)
KEPT = ("sulfur", "spinosad", "iron_phosphate_slug_bait")
# The methods whose authored bee caution must carry the medium band's sunset-to-midnight window.
AUTHORED_BEE = ("neem_oil", "horticultural_oil")

# A medium-band method may not claim a low bee/pollinator rating in ANY of its copy fields.
# Deliberately scoped: insecticidal_soap IS bee-low, so its "Low toxicity to bees" pro is CORRECT
# and must not be flagged -- the token-scan lesson from the conventional round.
FALSE_RATING = re.compile(r"low (?:in )?toxicity to (?:bees|[a-z,' ]*pollinators)", re.I)
COPY_FIELDS = ("cautions", "pros", "cons", "how_it_works_beginner", "how_it_works_seasoned",
               "best_use", "find_it_beginner")

# The copper acute split, by ingredient. A test freezes this as a literal AND cross-checks the
# RATINGS rows, so neither can drift alone.
ACUTE_SIDES = {
    "L": ("copper octanoate", "copper ammonium complex"),
    "M": ("copper oxychloride sulfate",),
    "H": ("copper hydroxide",),
}

BEE_SENTENCE = ("UC IPM's honey bee precaution for %s: do not apply it, or let it drift, onto "
                "anything in flower including weeds, except between sunset and midnight where the "
                "label allows, and do not let it reach water bees can drink such as puddles.")

COPPER_SPLIT_CAUTION = (
    "Which copper compound you buy changes the acute hazard, so read the active ingredient on the "
    "label rather than the brand name. UC IPM rates acute toxicity to people and other mammals "
    "Low for copper octanoate, the copper soap named on home-garden products, and for copper "
    "ammonium complex, Moderate for copper oxychloride sulfate, and High, the DANGER signal-word "
    "band, for copper hydroxide; none of the four carries a California Prop 65 or US EPA chronic "
    "listing.")

SOAP_ACUTE_CAUTION = (
    "UC IPM rates acute toxicity to people and other mammals Moderate for potassium salts of "
    "fatty acids; wear chemical resistant gloves, long sleeves and goggles when mixing and "
    "spraying, since many consumer products do not print protective equipment on the label. Its "
    "chronic rating is no known risk, and its honey bee precaution is UC IPM's lowest band.")

# Post-state cautions, in full, per changed method. Unchanged lines are the pre-state's bytes.
CAUTIONS = {
    "copper_fungicide": [
        ("Copper is highly to very highly toxic to fish and aquatic life; do not let spray or "
         "runoff reach ponds, streams, or storm drains"),
        "Copper accumulates at the soil surface and persists, so limit repeat use over the years",
        "Follow the label rate; too much copper can injure foliage",
        COPPER_SPLIT_CAUTION,
    ],
    "neem_oil": [
        BEE_SENTENCE % "neem oil",
        "Do not apply in high heat above 90°F or to drought-stressed plants",
    ],
    "insecticidal_soap": [
        "Can burn foliage on water-stressed plants or when the temperature is above 90°F",
        "Kills soft-bodied beneficials it directly wets, so spray only where pests are",
        SOAP_ACUTE_CAUTION,
    ],
    "horticultural_oil": [
        "Do not use oils on water-stressed plants or when temperatures exceed 90°F",
        ("Do not apply sulfur within 2 weeks of an oil spray, since the combination can injure "
         "foliage"),
        BEE_SENTENCE % "horticultural oil",
    ],
}

# Post-state pros where a pro carried the false or unsupported claim. Second lines are pre bytes.
PROS = {
    "neem_oil": [
        "Low toxicity to people and pets, and accepted for organic use",
        "Little persistent residue, so it has relatively small impact on beneficials that arrive later",
    ],
    "insecticidal_soap": [
        "Low toxicity to bees and other pollinators, and accepted for organic use",
        "Leaves no toxic residue, so beneficials that arrive after the spray are not harmed",
    ],
}

# Defect strings: each must be PRESENT in the pre-state (premise) and ABSENT from the post.
DEFECTS = {
    "neem_oil/cautions": "rates neem low in toxicity to bees",
    "neem_oil/pros": "Low toxicity to people, pets, and pollinators",
    "insecticidal_soap/pros": "Low toxicity to people, pets, and pollinators",
}

# Claims NOT being revalued: byte-for-byte in pre AND post of their field.
PRESERVED = {
    "copper_fungicide": ("highly to very highly toxic to fish",
                         "limit repeat use over the years"),
    "neem_oil": ("Do not apply in high heat above 90°F or to drought-stressed plants",),
    "insecticidal_soap": ("Can burn foliage on water-stressed plants",
                          "Leaves no toxic residue"),
    "horticultural_oil": ("Do not apply sulfur within 2 weeks of an oil spray",),
}

# Kept-method claims verified against the read; pinned so a later pass cannot quietly drop them.
KEPT_PINS = {
    "sulfur": "Can harm released predatory (beneficial) mites",
    "spinosad": "spray at dusk when bees are not foraging",
    "iron_phosphate_slug_bait": "safer for use around children, pets, birds, fish, and other "
                                "wildlife than metaldehyde",
}

MUTABLE = {
    "copper_fungicide": ("cautions", "sources", "anchoring_urls"),
    "neem_oil": ("cautions", "pros", "sources", "anchoring_urls"),
    "insecticidal_soap": ("cautions", "pros", "sources", "anchoring_urls"),
    "horticultural_oil": ("cautions", "sources", "anchoring_urls"),
}
ANCHOR_KEY = {"copper_fungicide": "125", "neem_oil": "38", "insecticidal_soap": "50",
              "horticultural_oil": "142"}

# The one live rung carrying the false neem rating: strawberry / aphids / note_seasoned.
RUNG = {
    "crop": "strawberry",
    "problem": "aphids",
    "method": "neem_oil",
    "register": "note_seasoned",
    "old": ("Neem works by contact smothering and as an antifeedant and growth regulator; low "
            "toxicity to bees but, as a contact spray, apply at dusk. Avoid above 90°F or on "
            "stressed plants."),
    "new": ("Neem works by contact smothering and as an antifeedant and growth regulator; a "
            "contact spray, so apply at dusk to avoid wetting foraging bees. Avoid above 90°F or "
            "on stressed plants."),
}

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "programme", "practise", "grey", "aluminium", "labelled", "travelled")
ABSOLUTES = ("completely safe", "totally safe", "harmless", "guaranteed", "eliminates all",
             "always safe", "never harmful", "non-toxic to people", "safest")


def hygiene(s):
    if "—" in s or "–" in s:
        return "em or en dash"
    if "--" in s:
        return "double hyphen in consumer copy"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling '{w}'"
    for a in ABSOLUTES:
        if a in s.lower():
            return f"safety absolute '{a}'"
    if re.search(r"\d\s*°\s+F", s):
        return "spaced degree unit"
    return None


def named(name, blob):
    """Word-boundary match on BOTH ends; 'copper' alone must not satisfy 'copper hydroxide',
    and 'copper octanoate-free' must not satisfy 'copper octanoate'."""
    return re.search(rf"(?<![-\w]){re.escape(name)}(?![-\w])", blob, re.I) is not None


def false_rating_violation(key, method):
    """A medium-band method may not claim a low bee/pollinator rating in any copy field."""
    if BAND_OF.get(key) != "medium":
        return None
    for f in COPY_FIELDS:
        v = method.get(f)
        texts = v if isinstance(v, list) else ([v] if v else [])
        for t in texts:
            if FALSE_RATING.search(t):
                return (f"{key}: claims a low bee or pollinator rating in '{f}' while UC IPM's "
                        f"band is medium: {t[:70]!r}")
    return None


def band_violation(key, cautions):
    """An authored medium-band bee caution must keep the sunset-to-midnight window."""
    if key not in AUTHORED_BEE:
        return None
    bee = [c for c in cautions if "flower" in c.lower()]
    if not bee:
        return f"{key}: no caution mentions flowering plants, so the bee band is unstated"
    blob = " ".join(bee).lower()
    if "sunset" not in blob or "midnight" not in blob:
        return (f"{key}: sits in UC IPM's middle bee band, whose legend grants a sunset to "
                f"midnight exception, but its bee caution does not state one")
    return None


def split_violation(cautions):
    """The copper acute split, checked by SIDE so a compound on the wrong rating cannot pass."""
    hits = [c for c in cautions if "acute toxicity" in c.lower()]
    if len(hits) != 1:
        return (f"copper_fungicide: expected exactly one caution naming acute toxicity, "
                f"found {len(hits)}")
    low = hits[0].lower()
    for marker in (" low for ", "moderate for", "high,"):
        if marker not in low:
            return f"copper_fungicide: the acute caution lost its '{marker.strip()}' side"
    i_low = low.index(" low for ")
    i_mod = low.index("moderate for")
    i_high = low.index("high,")
    if not i_low < i_mod < i_high:
        return "copper_fungicide: the acute caution's sides are out of order"
    sides = {"L": low[i_low:i_mod], "M": low[i_mod:i_high], "H": low[i_high:]}
    for rating, names in ACUTE_SIDES.items():
        for n in names:
            if not named(n, sides[rating]):
                return (f"copper_fungicide: {n} is rated {rating} and is not named on that side "
                        f"of the acute caution")
            for other, blob in sides.items():
                if other != rating and named(n, blob):
                    return f"copper_fungicide: {n} is named on the {other} side as well"
    if "none of the four" not in low or "prop 65" not in low or "us epa" not in low:
        return "copper_fungicide: the acute caution lost the chronic-absence disclosure"
    return None


def find_rung(data):
    crops = [c for c in data.get("crops") or [] if c.get("slug") == RUNG["crop"]]
    if len(crops) != 1:
        return None, f"expected exactly one crop with slug {RUNG['crop']!r}, found {len(crops)}"
    probs = [p for p in crops[0].get("pests") or [] if p.get("id") == RUNG["problem"]]
    if len(probs) != 1:
        return None, f"{RUNG['crop']}: expected exactly one problem {RUNG['problem']!r}"
    rungs = [r for r in probs[0].get("control_ladder") or [] if r.get("method") == RUNG["method"]]
    if len(rungs) != 1:
        return None, (f"{RUNG['crop']}/{RUNG['problem']}: expected exactly one {RUNG['method']} "
                      f"rung, found {len(rungs)}")
    return rungs[0], None


def check(data):
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}

    if SOURCE_ID not in sc:
        return f"{SOURCE_ID} is not in source_catalog; the conventional round should have minted it"
    if (sc[SOURCE_ID].get("tier") or "") != "T1":
        return f"{SOURCE_ID} is not T1"

    for key in COHORT:
        if key not in cm:
            return f"{key} is not in control_methods"
        if cm[key].get("tier") != "soft_chemical":
            return f"{key} is not in the soft_chemical tier"
    for key in CAUTIONS:
        if SOURCE_ID in (cm[key].get("sources") or []):
            return f"{key} already declares {SOURCE_ID}; this round has already run"

    # PREMISE: the false neem rating really is present, in all three of its fields.
    if not any(DEFECTS["neem_oil/cautions"] in c for c in cm["neem_oil"].get("cautions") or []):
        return ("neem_oil's cautions do not carry the false low-bee rating, so the defect this "
                "promote exists to fix is not present and it should not run")
    for slot in ("neem_oil/pros", "insecticidal_soap/pros"):
        key = slot.split("/")[0]
        if not any(DEFECTS[slot] in p for p in cm[key].get("pros") or []):
            return f"{key}'s pros do not carry the claim this promote narrows; it should not run"
    rung, problem = find_rung(data)
    if problem:
        return problem
    if rung.get(RUNG["register"]) != RUNG["old"]:
        return (f"the {RUNG['crop']} rung's {RUNG['register']} is not the recorded pre-state "
                f"string; re-read before editing")

    # PREMISE: the scan that licenses the fix fires on the pre-state.
    if not false_rating_violation("neem_oil", cm["neem_oil"]):
        return "the false-rating scan does not fire on neem_oil's pre-state; wrong premise"
    if not FALSE_RATING.search(RUNG["old"]):
        return "the false-rating scan does not fire on the rung's pre-state; wrong premise"

    # The three kept methods still carry the claims the read verified.
    for key, pin in KEPT_PINS.items():
        blob = json.dumps(cm[key], ensure_ascii=False)
        if pin not in blob:
            return f"kept method {key} no longer carries its verified claim {pin[:50]!r}"

    # Authored copy passes its own guards before anything is written.
    for key, want in CAUTIONS.items():
        if len(set(want)) != len(want):
            return f"{key}: duplicate caution authored"
        problem = band_violation(key, want)
        if problem:
            return "authored cautions fail the band check: " + problem
        for c in want:
            h = hygiene(c)
            if h:
                return f"{key}: copy hygiene, {h} in {c[:60]!r}"
        for claim in PRESERVED[key]:
            field = CAUTIONS[key] if any(claim in c for c in CAUTIONS[key]) else PROS.get(key, [])
            if not any(claim in c for c in field):
                return f"{key}: preserved claim dropped, {claim[:60]!r}"
            pre_field = list(cm[key].get("cautions") or []) + list(cm[key].get("pros") or [])
            if not any(claim in c for c in pre_field):
                return f"{key}: claimed as preserved but absent from the pre-state, {claim[:60]!r}"
    for key, want in PROS.items():
        for p in want:
            h = hygiene(p)
            if h:
                return f"{key}: copy hygiene in pros, {h} in {p[:60]!r}"
    h = hygiene(RUNG["new"])
    if h:
        return f"rung: copy hygiene, {h}"
    if FALSE_RATING.search(RUNG["new"]):
        return "the authored rung still claims a low bee rating"

    problem = split_violation(CAUTIONS["copper_fungicide"])
    if problem:
        return problem

    for key in CAUTIONS:
        for s in cm[key].get("sources") or []:
            if s not in sc:
                return f"{key} declares source {s}, which is not in source_catalog"
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    return {
        "crops": {c.get("slug"): copy.deepcopy(c) for c in data.get("crops") or []},
        "methods": copy.deepcopy(data.get("control_methods") or {}),
        "sources": copy.deepcopy(data.get("source_catalog") or {}),
    }


def apply_to(data):
    for key, cautions in CAUTIONS.items():
        m = data["control_methods"][key]
        m["cautions"] = list(cautions)
        if key in PROS:
            m["pros"] = list(PROS[key])
        srcs = [s for s in (m.get("sources") or []) if s != SOURCE_ID]
        m["sources"] = srcs + [SOURCE_ID]
        anchors = dict(m.get("anchoring_urls") or {})
        anchors[SOURCE_ID] = {"url": DETAIL % ANCHOR_KEY[key], "verified": VERIFIED}
        m["anchoring_urls"] = anchors
    rung, problem = find_rung(data)
    if problem:
        raise SystemExit("apply_to: " + problem)
    rung[RUNG["register"]] = RUNG["new"]
    return data


def verify_post(pre, data):
    post = snapshot(data)

    # set-equality BEFORE any value comparison, per PLA-162: iterating pre hides additions in post.
    if set(post["crops"]) != set(pre["crops"]):
        return "the crop roster changed"
    if set(post["methods"]) != set(pre["methods"]):
        return "the control_methods roster changed"
    if set(post["sources"]) != set(pre["sources"]):
        return "the source_catalog roster changed and this round mints nothing"
    for sid, before in pre["sources"].items():
        if post["sources"][sid] != before:
            return f"source {sid} changed and this round touches no source"

    for key in CAUTIONS:
        m = post["methods"][key]
        problem = band_violation(key, m.get("cautions") or [])
        if problem:
            return "post-state fails the band check: " + problem
        problem = false_rating_violation(key, m)
        if problem:
            return "post-state fails the rating scan: " + problem
        if key == "copper_fungicide":
            problem = split_violation(m.get("cautions") or [])
            if problem:
                return "post-state " + problem
        if m.get("cautions") != list(CAUTIONS[key]):
            return f"post-state {key}: cautions are not what was authored"
        if key in PROS and m.get("pros") != list(PROS[key]):
            return f"post-state {key}: pros are not what was authored"
        if SOURCE_ID not in (m.get("sources") or []):
            return f"post-state {key}: does not declare {SOURCE_ID}"
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            return (f"post-state {key}: anchoring_urls keys do not match sources "
                    f"({sorted(set(m.get('anchoring_urls') or {}))} vs "
                    f"{sorted(set(m.get('sources') or []))})")
        if (m.get("anchoring_urls") or {}).get(SOURCE_ID, {}).get("url") != DETAIL % ANCHOR_KEY[key]:
            return f"post-state {key}: the {SOURCE_ID} anchor does not point at its own page"
        for f, v in pre["methods"][key].items():
            if f in MUTABLE[key]:
                continue
            if m.get(f) != v:
                return f"post-state {key}: field '{f}' changed and it was not supposed to"
        if set(m) != set(pre["methods"][key]):
            return f"post-state {key}: the field set changed"

    for key in KEPT:
        if post["methods"][key] != pre["methods"][key]:
            return f"kept method {key} changed and it was verified byte-for-byte"
    for key, before in pre["methods"].items():
        if key not in COHORT and post["methods"][key] != before:
            return f"bystander method {key} changed"

    # The rung: the new string landed, the old is gone, and NOTHING else in strawberry moved.
    rung, problem = find_rung(data)
    if problem:
        return "post-state: " + problem
    if rung.get(RUNG["register"]) != RUNG["new"]:
        return "post-state: the rung edit did not land"
    reverted = copy.deepcopy(post["crops"][RUNG["crop"]])
    for p in reverted.get("pests") or []:
        if p.get("id") == RUNG["problem"]:
            for r in p.get("control_ladder") or []:
                if r.get("method") == RUNG["method"]:
                    r[RUNG["register"]] = RUNG["old"]
    if reverted != pre["crops"][RUNG["crop"]]:
        return "post-state: strawberry changed beyond the one rung register"
    for slug, before in pre["crops"].items():
        if slug != RUNG["crop"] and post["crops"][slug] != before:
            return f"bystander crop {slug} changed"
    if FALSE_RATING.search(json.dumps(post["crops"][RUNG["crop"]], ensure_ascii=False)):
        return "post-state: strawberry still carries a low-bee-rating claim"
    return None


def main():
    apply_flag = "--apply" in sys.argv
    raw = open(CANONICAL, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != BASE_SHA:
        print(f"REFUSED: base SHA mismatch\n  expected {BASE_SHA}\n  found    {sha}")
        return 1
    data = json.loads(raw)

    problem = check(data)
    if problem:
        print(f"REFUSED: {problem}")
        return 1

    pre = snapshot(data)
    data = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print(f"REFUSED (post): {problem}")
        return 1

    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    print(f"OK  chemical cohort closed: {len(CAUTIONS)} methods changed, {len(KEPT)} verified "
          f"byte-for-byte, 1 rung register corrected, 0 sources minted")
    print(f"    base {BASE_SHA[:8]} -> {new_sha[:8]}")
    for k in CAUTIONS:
        print(f"    {k:20s} {len(CAUTIONS[k])} cautions, band={BAND_OF[k]}, anchor uaiKey={ANCHOR_KEY[k]}")
    for k in KEPT:
        print(f"    {k:20s} KEPT byte-for-byte, band={BAND_OF[k]}")
    print(f"    {RUNG['crop']}/{RUNG['problem']}/{RUNG['method']}/{RUNG['register']} corrected")
    if apply_flag:
        open(CANONICAL, "wb").write(out)
        print(f"    APPLIED -> {CANONICAL}")
    else:
        print("    dry run; pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
