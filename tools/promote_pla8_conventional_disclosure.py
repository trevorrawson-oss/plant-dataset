#!/usr/bin/env python3
"""PLA-8: bring the whole conventional tier to ONE disclosure standard. Base 1330fe5d.

Touches `source_catalog` (one mint) and the `cautions` / `sources` / `anchoring_urls` of the three
`conventional` methods. NO crop, NO ladder, NO rung, NO other method, no other field.

WHY IT IS OWED. `d096415` minted `chlorothalonil` with a six-axis hazard disclosure -- aquatic,
acute, chronic, bees, PPE, pre-harvest interval -- and its own docstring recorded that `carbaryl`
and `pyrethroid` were sourced before the column-shift parse bug was known and should be re-read from
the RENDERED table before their cautions were trusted. They have now been read. The tier was left
with two standards: a reader on the cucumber page got a carcinogen disclosure and a reader on the
apple page got a conventional with no chronic line at all, and the only reason was which ingredient
happened to be sourced last.

THE PARSE THAT PRODUCED THESE NUMBERS WAS VALIDATED BEFORE IT WAS TRUSTED. UC IPM's hazard grid is a
two-level table whose honey-bee cell is an EMPTY `<span>` carrying its value in a CSS class, and
whose every `<th>` embeds an sr-only footnote ending "Information to be added." A markdown flattener
reads those footnotes as data, which is precisely the documented WebFetch defect. This round parsed
the RAW HTML positionally and ran chlorothalonil as a POSITIVE CONTROL: the parse returns water H,
natural enemies L, bees medium, acute H, Prop 65 + US EPA, which is byte-for-byte what the rendered
screenshot showed on 2026-08-26. Only then were the other eleven ingredients read.

THE DEFECT THIS FIXES IS NOT AN OMISSION, IT IS WRONG ADVICE, AND IT IS LIVE ON TEN RUNGS.
Both insecticide entries say "do not apply to flowering plants, and spray at dusk when bees are not
foraging." That sunset-to-midnight allowance is the instruction for UC IPM's MIDDLE bee band. UC IPM
puts carbaryl and every common pyrethroid in its STRICTEST band, whose legend reads "Do not apply or
allow to drift to plants that are flowering including weeds" with no time window at all. We were
granting readers a safe evening window the source withholds, on ten shipped rungs across four food
crops. `chlorothalonil` is genuinely in the middle band, so its window is correct and stays.

WHAT ELSE THE READ FOUND:
  * CARBARYL IS ON BOTH THE CA PROP 65 LIST AND THE US EPA LIST -- the identical chronic profile we
    disclose at length for chlorothalonil, and the entry said nothing. Its acute rating is only Low,
    so the honest sentence is that the short-term risk is mild and the listing is the real concern;
    stating the reassuring half alongside the alarming half is the point of a standard.
  * THE PYRETHROID CHRONIC PICTURE IS SPLIT AND THE SPLIT IS PURCHASING ADVICE. Of the nine common
    ingredients, permethrin, bifenthrin, cypermethrin and zeta-cypermethrin are on the US EPA list;
    cyfluthrin, beta-cyfluthrin, deltamethrin, esfenvalerate and lambda-cyhalothrin are rated no
    known risk. PERMETHRIN IS ON THE LIST, and permethrin is the ingredient this entry names in its
    own title and that the two asparagus rungs name by name.
  * "BEE RATING II" ON CHLOROTHALONIL WAS INVENTED PRECISION, AND IT WAS MINE, SHIPPED THIS MORNING.
    The detail page never uses roman numerals; it renders three CSS bands, and the four-numeral
    scheme appears only inside a footnote describing a different database. The middle band spans II
    and III, so the numeral was a claim the page does not make. The PRESCRIPTION was right and is
    kept verbatim; only the attribution changes.

A SOURCE IS MINTED RATHER THAN REPOINTED, AND THAT IS THE STRUCTURAL POINT. Both the cole-crops
relative-toxicity table and this hazard database are `ucanr_ext`, and `anchoring_urls` holds one URL
per source id. Repointing would have silently orphaned the residual-toxicity claim the cole-crops
table is the anchor for. `ucipm_uaidb` is minted for the home-and-landscape database, which is also
the right SCOPE for a home gardener, and chlorothalonil's anchor moves onto it so the tier cites one
source for one class of claim. That database covers several other owed gaps (mancozeb was read in
the same pass and is NOT minted here because no crop needs it yet).

REFUSALS: base SHA mismatch; a strict-band method whose bee caution grants any evening or sunset
window; the middle-band method losing its window; any of the six disclosure axes missing from any of
the three; the pyrethroid split naming an ingredient on the wrong side; a preserved claim mutating;
a declared source absent from source_catalog, not T1, or lacking an anchoring_url; copy hygiene; and
post-state blast radius.

NOT DONE HERE, AND FLAGGED RATHER THAN DECIDED: UC IPM lists NO home-garden product for carbaryl,
and for the pyrethroids the listed retail products are overwhelmingly mosquito, termite, lawn and
indoor-perimeter products rather than edible-crop products. Under the 2026-08-26 shelf-availability
ruling that is a question about ADMISSION, which is Trevor's call and not a promote's.

Guard suite:      tools/test_promote_pla8_conventional_disclosure.py
Mutation harness: tools/mutate_pla8_conventional_disclosure_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_conventional_disclosure.py [--apply] [--dry-run]
"""
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "1330fe5d7b1533eaa165b0a48ddad1c8c9ef0335aa3db74f2c545bc447046781"
VERIFIED = "2026-08-26"
SOURCE_ID = "ucipm_uaidb"
UAI = "https://ipm.ucanr.edu/home-and-landscape/pesticide-active-ingredients-database"
DETAIL = UAI + "/active-ingredient-details/?uaiKey=%s"

# ---------------------------------------------------------------------------------------------
# MEASURED 2026-08-26 from the RAW HTML grid, chlorothalonil validated against the rendered page.
# uaiKey -> (name, water_quality, natural_enemies, bee_band, acute, chronic)
# ---------------------------------------------------------------------------------------------
RATINGS = {
    "115": ("chlorothalonil",     "H",  "L",  "medium", "H", "prop65+epa"),
    "111": ("carbaryl",           "M",  "MH", "high",   "L", "prop65+epa"),
    "47":  ("permethrin",         "H",  "LH", "high",   "M", "epa"),
    "101": ("bifenthrin",         "H",  "H",  "high",   "H", "epa"),
    "129": ("cyfluthrin",         "H",  "H",  "high",   "H", "nkr"),
    "100": ("beta-cyfluthrin",    "VH", "H",  "high",   "H", "nkr"),
    "130": ("cypermethrin",       "H",  "H",  "high",   "M", "epa"),
    "82":  ("zeta-cypermethrin",  "VH", "MH", "high",   "M", "epa"),
    "133": ("deltamethrin",       "--", "--", "high",   "M", "nkr"),
    "6":   ("esfenvalerate",      "--", "MH", "high",   "M", "nkr"),
    "27":  ("lambda-cyhalothrin", "H",  "H",  "high",   "M", "nkr"),
}
PYRETHROIDS = [v[0] for k, v in RATINGS.items() if v[0] not in ("chlorothalonil", "carbaryl")]
def _pyr(field, want):
    return tuple(sorted(v[0] for v in RATINGS.values() if v[0] in PYRETHROIDS and v[field] == want))


EPA_LISTED = _pyr(5, "epa")
NO_KNOWN_RISK = _pyr(5, "nkr")
ACUTE_HIGH = _pyr(4, "H")

# The bee band each METHOD key sits in, and therefore whether it may grant an evening window.
BAND_OF = {"carbaryl": "high", "pyrethroid": "high", "chlorothalonil": "medium"}
# Legend, verbatim: the strict band is "Do not apply or allow to drift to plants that are flowering
# including weeds" -- no time window. The middle band adds "except when the application is made
# between sunset and midnight if allowed by the pesticide label and regulations."
WINDOW_TOKENS = ("sunset", "dusk", "evening", "at night", "early morning", "not foraging",
                 "late even")

SOURCE = {
    "id": SOURCE_ID,
    "name": "UC IPM -- Pesticide Active Ingredients Database (Home and Landscape)",
    "title": "Pesticide Active Ingredients Database / Home and Landscape / UC Statewide IPM Program (UC IPM)",
    "publisher": "UC ANR",
    "url": UAI + "/",
    "source_class": "university_extension",
    "trust_tier": "high",
    "accessed": "2026-08",
    "tier": "T1",
    "citable_for": (
        "UC IPM's per-active-ingredient hazard grid for HOME AND LANDSCAPE use: water quality risk "
        "to aquatic wildlife, impact on natural enemies, the honey bee precaution band, acute "
        "toxicity to people and other mammals, chronic listings on the CA Prop 65 and US EPA lists, "
        "the standing PPE paragraph, and the example home-garden products drawn from an annual "
        "retail shelf survey. Scoped to home-garden hazard ratings; the agricultural relative-"
        "toxicity tables under `ucanr_ext` remain the anchor for residual duration and for "
        "crop-specific comparative toxicity."),
    "_admission_provenance": (
        "Minted 2026-08-26 (PLA-8 conventional-tier disclosure round). The database was already "
        "cited by `chlorothalonil` under the generic `ucanr_ext` id, which collided with the "
        "cole-crops relative-toxicity table that `carbaryl` and `pyrethroid` anchor for their "
        "residual and natural-enemy claims: one source id, one url slot, two different documents. "
        "Minted rather than repointed so neither claim is orphaned. Twelve ingredient pages were "
        "fetched and parsed from RAW HTML in this pass, with chlorothalonil run as a positive "
        "control against the rendered screenshot of 2026-08-26 before any other page was trusted."),
}

REQUIRED = ("id", "name", "title", "publisher", "url", "source_class", "trust_tier", "accessed",
            "tier", "citable_for")

# Six axes, each refusable BY NAME, on every conventional method. Same standard chlorothalonil set.
DISCLOSURE_AXES = {
    "bees":       ("flower",),
    "aquatic":    ("water quality", "aquatic"),
    "people":     ("acute toxicity",),
    "chronic":    ("us epa list",),
    "ppe":        ("gloves", "goggles"),
    "phi":        ("pre-harvest interval",),
}

PPE = ("Many consumer products do not print protective equipment on the label; wear chemical "
       "resistant gloves, long sleeves and goggles regardless")

CAUTIONS = {
    "carbaryl": [
        ("UC IPM puts carbaryl in its strictest honey bee band: do not apply it, or let it drift, "
         "onto anything in flower including weeds, and do not let it reach water bees can drink "
         "such as puddles."),
        ("Rated Moderate to High for harm to natural enemies, and the residue is long lasting, so "
         "a spray can remove the predators that were holding a second pest down and let that pest "
         "flare weeks later."),
        ("UC IPM rates acute toxicity to people and other mammals Low, the least severe of its "
         "four bands, so the short term risk is the mild half of this ingredient's picture."),
        ("Listed on both the California Prop 65 list and the US EPA list, where an active "
         "ingredient appears only as a likely or confirmed carcinogen. On a food crop that listing "
         "is the reason to think twice, rather than the acute rating above."),
        ("Rated Moderate for water quality risk to aquatic wildlife; keep spray and runoff away "
         "from ponds, streams, storm drains and puddles."),
        "Toxic to earthworms, which are important to healthy soil",
        PPE,
        ("Observe the pre-harvest interval on the label before eating the crop, and always read and "
         "follow the label"),
    ],
    "pyrethroid": [
        ("UC IPM puts every common pyrethroid in its strictest honey bee band: do not apply one, or "
         "let it drift, onto anything in flower including weeds, and do not let it reach water bees "
         "can drink such as puddles."),
        ("Rated High to Very High for water quality risk to aquatic wildlife depending on the "
         "ingredient; keep spray and runoff away from ponds, streams, storm drains and puddles."),
        ("Rated Low to High for harm to natural enemies, most of the common ones at High, and the "
         "residue persists for weeks. Removing the predators is why a pyrethroid can leave aphids "
         "or mites worse off a month later than they were before the spray."),
        ("Which pyrethroid you buy changes the health picture, so read the active ingredient on the "
         "label rather than the brand name. On the US EPA list, where an active ingredient appears "
         "only as a likely or confirmed carcinogen: permethrin, bifenthrin, cypermethrin, "
         "zeta-cypermethrin. Rated no known risk: cyfluthrin, beta-cyfluthrin, deltamethrin, "
         "esfenvalerate, lambda-cyhalothrin."),
        ("UC IPM rates acute toxicity to people and other mammals Moderate for most pyrethroids and "
         "High for bifenthrin, cyfluthrin and beta-cyfluthrin."),
        "More toxic to cats than to dogs or people; keep pets off until the spray is dry",
        PPE,
        ("Observe the pre-harvest interval on the label before eating the crop, and always read and "
         "follow the label"),
    ],
    "chlorothalonil": [
        ("Rated High for water quality risk to aquatic wildlife; keep spray and runoff away from "
         "ponds, streams, storm drains and puddles"),
        ("UC IPM rates acute toxicity to people and other mammals High, the DANGER signal-word "
         "band, and notes the rating follows the most sensitive route of entry rather than oral "
         "toxicity"),
        ("Listed on both the California Prop 65 list and the US EPA list, where an active "
         "ingredient appears only as a likely or confirmed carcinogen; weigh that before choosing "
         "it on a food crop"),
        ("UC IPM's honey bee precaution for chlorothalonil: do not apply it, or let it drift, onto "
         "anything in flower including weeds, except between sunset and midnight where the label "
         "allows, and do not let it reach water bees can drink such as puddles."),
        PPE,
        ("Observe the pre-harvest interval on the label before eating the crop, and read and follow "
         "the label every time"),
    ],
}

# Claims NOT being revalued: they must survive this promote byte for byte.
PRESERVED = {
    "carbaryl": ("Toxic to earthworms, which are important to healthy soil",
                 "Observe the pre-harvest interval on the label before eating the crop, and always "
                 "read and follow the label"),
    "pyrethroid": ("More toxic to cats than to dogs or people; keep pets off until the spray is dry",
                   "Observe the pre-harvest interval on the label before eating the crop, and "
                   "always read and follow the label"),
    "chlorothalonil": (
        "do not apply it, or let it drift, onto anything in flower including weeds, except between "
        "sunset and midnight where the label allows",),
}
# Every field on the three methods other than these must be byte-identical after the promote.
MUTABLE_FIELDS = ("cautions", "sources", "anchoring_urls")
ANCHOR_KEY = {"carbaryl": "111", "pyrethroid": "47", "chlorothalonil": "115"}

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "programme", "practise", "grey", "aluminium", "labelled", "travelled")
ABSOLUTES = ("completely safe", "totally safe", "harmless", "guaranteed", "eliminates all",
             "always safe", "never harmful", "non-toxic to people")


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
    """Word-boundary match that does NOT let 'cypermethrin' match inside 'zeta-cypermethrin'."""
    return re.search(rf"(?<![-\w]){re.escape(name)}\b", blob, re.I) is not None


def band_violation(key, cautions):
    """THE GUARD FOR THE DEFECT THIS PROMOTE EXISTS TO FIX. Refuses the pre-state by design."""
    band = BAND_OF[key]
    bee = [c for c in cautions if "flower" in c.lower()]
    if not bee:
        return f"{key}: no caution mentions flowering plants, so the bee band is unstated"
    blob = " ".join(bee).lower()
    if band == "high":
        for t in WINDOW_TOKENS:
            if t in blob:
                return (f"{key}: sits in UC IPM's strictest bee band, which grants no time window, "
                        f"but its bee caution says '{t}'")
    else:
        if "sunset" not in blob or "midnight" not in blob:
            return (f"{key}: sits in UC IPM's middle bee band, whose legend grants a sunset to "
                    f"midnight exception, but its bee caution does not state one")
    return None


def split_violation(cautions):
    """The pyrethroid chronic split, checked by SIDE so a swapped ingredient cannot pass."""
    hits = [c for c in cautions if "us epa list" in c.lower()]
    if len(hits) != 1:
        return f"pyrethroid: expected exactly one caution naming the US EPA list, found {len(hits)}"
    c = hits[0]
    low = c.lower()
    if "no known risk" not in low:
        return "pyrethroid: the chronic caution names the EPA list but not the no-known-risk side"
    # Each side is the text AFTER its own marker, so a name can only satisfy the side it sits in.
    cut = low.index("no known risk")
    epa_side = low[low.index("us epa list"):cut]
    nkr_side = low[cut:]
    for n in EPA_LISTED:
        if not named(n, epa_side):
            return (f"pyrethroid: {n} is on the US EPA list and is not named on the EPA side of "
                    f"the chronic caution")
        if named(n, nkr_side):
            return f"pyrethroid: {n} is on the US EPA list but is named on the no-known-risk side"
    for n in NO_KNOWN_RISK:
        if not named(n, nkr_side):
            return (f"pyrethroid: {n} is rated no known risk and is not named on the "
                    f"no-known-risk side of the chronic caution")
        if named(n, epa_side):
            return f"pyrethroid: {n} is rated no known risk but is named on the US EPA list side"
    acute = [c for c in cautions if "acute toxicity" in c.lower()]
    if not acute:
        return "pyrethroid: no caution states acute toxicity"
    for n in ACUTE_HIGH:
        if not named(n, " ".join(acute)):
            return (f"pyrethroid: {n} is rated acute High and the acute caution does not name it")
    return None


def check(data):
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}

    if SOURCE_ID in sc:
        return f"{SOURCE_ID} is already in source_catalog"
    for f in REQUIRED:
        if not SOURCE.get(f):
            return f"the minted source is missing required field '{f}'"
    if SOURCE["tier"] != "T1":
        return "the minted source is not T1"

    for key in CAUTIONS:
        if key not in cm:
            return f"{key} is not in control_methods"
        if cm[key].get("tier") != "conventional":
            return f"{key} is not in the conventional tier"

    # PREMISE: the pre-state really does carry the defect this promote claims to fix.
    strict = [k for k, b in BAND_OF.items() if b == "high"]
    if not any(band_violation(k, cm[k].get("cautions") or []) for k in strict):
        return ("no strict-band method grants an evening window in the pre-state, so the defect "
                "this promote exists to fix is not present and it should not run")

    for key, want in CAUTIONS.items():
        if len(set(want)) != len(want):
            return f"{key}: duplicate caution authored"
        blob = " ".join(want).lower()
        # The band check runs FIRST and deliberately: a method with no bee caution at all trips
        # both this and the 'bees' axis, and the band message is the specific one.
        problem = band_violation(key, want)
        if problem:
            return "authored cautions fail the band check: " + problem
        for axis, tokens in DISCLOSURE_AXES.items():
            if not any(t in blob for t in tokens):
                return f"{key}: the '{axis}' disclosure axis is missing from its cautions"
        for c in want:
            h = hygiene(c)
            if h:
                return f"{key}: copy hygiene, {h} in {c[:60]!r}"
        for claim in PRESERVED[key]:
            if not any(claim in c for c in want):
                return f"{key}: preserved claim dropped, {claim[:60]!r}"
            if not any(claim in c for c in (cm[key].get("cautions") or [])):
                return f"{key}: claimed as preserved but absent from the pre-state, {claim[:60]!r}"

    problem = split_violation(CAUTIONS["pyrethroid"])
    if problem:
        return problem

    for key in CAUTIONS:
        srcs = list(cm[key].get("sources") or []) + [SOURCE_ID]
        for s in set(srcs):
            if s != SOURCE_ID and s not in sc:
                return f"{key} declares source {s}, which is not in source_catalog"
            if s != SOURCE_ID and (sc[s].get("tier") or "") != "T1":
                return f"{key} declares source {s}, which is not T1"
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
    data["source_catalog"][SOURCE_ID] = copy.deepcopy(SOURCE)
    for key, cautions in CAUTIONS.items():
        m = data["control_methods"][key]
        m["cautions"] = list(cautions)
        srcs = [s for s in (m.get("sources") or []) if s != SOURCE_ID]
        if key == "chlorothalonil":
            srcs = [s for s in srcs if s != "ucanr_ext"]      # its uaiKey anchor moves to the mint
        m["sources"] = srcs + [SOURCE_ID]
        anchors = dict(m.get("anchoring_urls") or {})
        if key == "chlorothalonil":
            anchors.pop("ucanr_ext", None)
        anchors[SOURCE_ID] = {"url": DETAIL % ANCHOR_KEY[key], "verified": VERIFIED}
        m["anchoring_urls"] = anchors
    return data


def verify_post(pre, data):
    post = snapshot(data)

    # set-equality BEFORE any value comparison, per PLA-162: iterating pre hides additions in post.
    if set(post["crops"]) != set(pre["crops"]):
        return "the crop roster changed"
    if set(post["methods"]) != set(pre["methods"]):
        return "the control_methods roster changed"
    if set(post["sources"]) != set(pre["sources"]) | {SOURCE_ID}:
        return "source_catalog gained or lost something other than the one minted source"

    if post["sources"][SOURCE_ID] != SOURCE:
        return "the minted source did not land verbatim"

    for key in CAUTIONS:
        m = post["methods"][key]
        problem = band_violation(key, m.get("cautions") or [])
        if problem:
            return "post-state fails the band check: " + problem
        blob = " ".join(m.get("cautions") or []).lower()
        for axis, tokens in DISCLOSURE_AXES.items():
            if not any(t in blob for t in tokens):
                return f"post-state {key}: the '{axis}' axis is missing"
        if key == "pyrethroid":
            problem = split_violation(m.get("cautions") or [])
            if problem:
                return "post-state " + problem
        if m.get("cautions") != list(CAUTIONS[key]):
            return f"post-state {key}: cautions are not what was authored"
        if SOURCE_ID not in (m.get("sources") or []):
            return f"post-state {key}: does not declare {SOURCE_ID}"
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            return (f"post-state {key}: anchoring_urls keys do not match sources "
                    f"({sorted(set(m.get('anchoring_urls') or {}))} vs "
                    f"{sorted(set(m.get('sources') or []))})")
        if (m.get("anchoring_urls") or {}).get(SOURCE_ID, {}).get("url") != DETAIL % ANCHOR_KEY[key]:
            return f"post-state {key}: the {SOURCE_ID} anchor does not point at its own page"
        # everything except the three mutable fields is frozen
        for f, v in pre["methods"][key].items():
            if f in MUTABLE_FIELDS:
                continue
            if m.get(f) != v:
                return f"post-state {key}: field '{f}' changed and it was not supposed to"
        if set(m) != set(pre["methods"][key]):
            return f"post-state {key}: the field set changed"

    for key, before in pre["methods"].items():
        if key not in CAUTIONS and post["methods"][key] != before:
            return f"bystander method {key} changed"
    for slug, before in pre["crops"].items():
        if post["crops"][slug] != before:
            return f"bystander crop {slug} changed"
    for sid, before in pre["sources"].items():
        if post["sources"][sid] != before:
            return f"bystander source {sid} changed"
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
    n = sum(len(v) for v in CAUTIONS.values())
    print(f"OK  source_catalog +1 ({SOURCE_ID}); {len(CAUTIONS)} methods re-cautioned, {n} cautions")
    print(f"    base {BASE_SHA[:8]} -> {new_sha[:8]}")
    for k in CAUTIONS:
        print(f"    {k:16s} {len(CAUTIONS[k])} cautions, band={BAND_OF[k]}, anchor uaiKey={ANCHOR_KEY[k]}")
    if apply_flag:
        open(CANONICAL, "wb").write(out)
        print(f"    APPLIED -> {CANONICAL}")
    else:
        print("    dry run; pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
