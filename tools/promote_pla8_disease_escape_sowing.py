#!/usr/bin/env python3
"""PLA-8: mint `disease_escape_sowing`, the gap batch 12 measured and could not fill. Base 7f5079aa.

ONE NEW KEY in `control_methods`, 59 -> 60. NO existing method is touched, NO crop, NO source_catalog
entry, NO ladder. The rungs are a separate promote (`promote_pla8_disease_escape_backfill.py`),
which is the chlorothalonil / trap_cropping pairing applied a third time.

WHY IT IS OWED. Seven problems on seven crops carry the same recommendation in their prose: sow
early so the crop matures before a weather-driven foliar disease builds late in the season (four
corn common-rust entries, two pea powdery-mildew entries, fava's broad-bean-rust). All seven
shipped without the rung because no catalog key could carry it. Measured 2026-08-28
(`docs/2026-08-28-pla8-disease-escape-sowing-gap.md`), re-measured 2026-08-30 against 7f5079aa over
EVERY string field of every disease-typed problem: 34 raw hits READ, 7 real, the rest are different
concepts (clean seed, roguing, cultivar choice, spray timing, warm-soil vigor, inherent crop speed,
early harvest). Every near-miss in the catalog is wrong in a different way:

  planting_time_avoidance  dodges a pest's FLIGHT WINDOW, which extension services publish as local
                           calendar or degree-day dates; this races a weather-driven epidemic with
                           no published start date. Its applies_to carries no disease target, and
                           its best_use ("a pest whose damage falls in a predictable, locally
                           published stretch of the season") is false for late-season rust.
  resistant_varieties      changes WHAT you plant, not WHEN; already first on six of the seven
  crop_rotation            moves the planting in space, not time
  prompt_harvest           acts at the END of the season; this is a decision made at sowing
  sound_sowing_practice    seed quality, depth, soil warmth against damping-off; not the calendar

THE MINT-NOT-WIDEN RULING, RE-TESTED AS THE GAP DOC REQUIRED. The doc's ruling was a starting
position with a stated overturn condition: if the T1 literature framed insect timing and disease
escape as one practice under a single planting-date heading, the widen case should win. It does
not. WSU states the escape inside its powdery-mildew management text; Cornell states the seasonal
asymmetry in a rust factsheet; NCSU's only plant-early sentence is armyworm-specific and sits in
its insect section. The two mechanisms are published in different places about different organisms,
so they stay two methods. (Key named `disease_escape_sowing` rather than the doc's proposed
`disease_escape_timing`: all seven instances are sowing-date decisions on direct-sown crops, and
the state doc already names the gap "disease-escape sowing".)

--------------------------------------------------------------------------------------------------
THE T1 READ ANCHORS THE TRADE, NOT JUST THE PRACTICE, BECAUSE THE TRADE IS THE SAFETY-BEARING HALF
--------------------------------------------------------------------------------------------------
The escape is a race the grower can lose. Sowing early trades late-season disease exposure for a
cold, wet seedbed, and an entry that says "sow early to beat rust" without the counter-exposure is
advice that can cost a stand. Three documents anchor the three claims:

  WSU    Hortsense, "Pea: Powdery mildew" (hortsense.cahnrs.wsu.edu). THE PRACTICE, stated
         directly: "Plant peas early. Spring crops seldom show serious damage." And the seasonal
         asymmetry: "Warm days, cool nights, and humid weather favor development of powdery
         mildew, which is often worse in the fall."

  Cornell "Common Rust of Sweet Corn" (vegetables.cornell.edu). THE TIMING the escape rests on:
         "The disease is therefore usually observed for the first time in New York sweet corn
         crops from mid-June onwards and is prevalent in late season plantings." And "Resistant
         or moderately resistant cultivars should be used for late season plantings."

  NCSU   "Organic Sweet Corn Production" (content.ces.ncsu.edu). THE COUNTER-EXPOSURE, with the
         floor quantified: minimum soil temperature 50(deg)F for standard sweet corn, 60(deg)F for
         the se/sh2/sy genetics, and "Seed planted in moist soil below these temperatures will
         often rot."

READ AND NOT CITED. The four documents pinned on the target problems themselves were fetched
first, and NONE states the escape (NCSU's plant-early sentence is about fall armyworm; RHS's
broad-bean-rust page carries spacing and sanitation only; UMN and Clemson's pea pages carry
nothing on timing). USU's vegetable-guide powdery mildew page has no timing statement. Illinois'
"Rusts [Vegetables]" focus page, which search summaries quote for "early season sweet corn
hybrids often escape infection", redirects to a generic landing page: a page that cannot be read
is not evidence. Purdue ID-405 corroborates the seasonality but does not state the escape.

REFUSALS: base SHA mismatch; the key already present; a missing required field; `applies_to` not
exactly ['fungal_foliar']; the tier not `cultural`; any trade disclosure missing from the
cautions; `best_use` not naming both near-misses; a source not in source_catalog or not T1; a
declared source with no anchoring_url; copy hygiene; a crop gaining a rung here; an exclusion that
does not resolve; and post-state blast radius.

Guard suite:      tools/test_promote_pla8_disease_escape_sowing.py
Mutation harness: tools/mutate_pla8_disease_escape_sowing_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_disease_escape_sowing.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "7f5079aab0fa4167c87e1373b3d28d598bf2379e05e2f8e2047665eabb13b9c3"

KEY = "disease_escape_sowing"
VERIFIED = "2026-08-30"

# THE ENTRY AS A LITERAL, not read from a staged spec and not derived from anything this file also
# validates (batch 10's `MINT = staged_mint()["entry"]` made its own agreement check vacuous).
METHOD = {
    "name": "Disease-escape sowing",
    "tier": "cultural",
    # Narrow on purpose. All seven measured instances are foliar fungal diseases (two rusts and a
    # powdery mildew). No bacterial, viral or soilborne case was read, and declaring those targets
    # would make the method legal on problems no source covers. Widening later is cheap;
    # over-widening at mint time is what put certified_clean_stock and reflective_mulch out of
    # step with their own best_use.
    "applies_to": ["fungal_foliar"],
    "how_it_works_beginner":
        "Some leaf diseases only get going late in the season, once the weather turns their way. "
        "Sowing early means the crop is nearly finished by the time that weather arrives, so "
        "there is less for the disease to spoil. It does not stop the disease from showing up; "
        "it moves the crop out of its path. The catch sits at the other end of the season: seed "
        "sown too early waits in cold, wet soil, where it can rot before it comes up. So this "
        "works best on quick crops, sown as early as the soil honestly allows and no earlier, "
        "with a resistant variety doing the rest of the work.",
    "how_it_works_seasoned":
        "A sowing date is chosen so the crop completes its vulnerable stretch before a "
        "weather-driven foliar epidemic builds. The pressure is seasonal and one-sided: Cornell "
        "first observes common rust in New York sweet corn from mid-June onward and calls it "
        "prevalent in late season plantings, and WSU states the escape for peas directly, plant "
        "peas early, spring crops seldom show serious damage, with powdery mildew often worse in "
        "the fall. The escape shortens the overlap between green leaf and disease weather rather "
        "than preventing infection, which is why the same sources put resistant varieties beside "
        "it. And the race can be lost at the start instead of the end: NC State puts the floor "
        "under the early edge, seed planted in moist soil below 50°F will often rot, 60°F for "
        "the high-sugar corn genetics, so the date moves to the front of the window the seedbed "
        "allows and stops there.",
    "best_use":
        "A quick-maturing, direct-sown crop facing a foliar disease whose weather arrives late "
        "in the season, where the crop's own guidance says an early sowing matures ahead of it. "
        "Distinct from dodging a pest's flight window, which extension services publish as local "
        "calendar or degree-day dates; the epidemic this races is weather-driven with no "
        "published start date, so the escape rests on finishing early, not on missing a "
        "documented window. Distinct from resistant varieties, which change what you plant "
        "rather than when; the two sit together at the front of a ladder and the sources name "
        "them in the same breath. Not worth forcing where the seedbed stays cold and wet, "
        "because seed rot can cost the stand before the disease would have cost the crop.",
    "find_it_beginner":
        "Nothing to buy: this is a decision made at sowing time. Check the seed packet's days to "
        "maturity and your area's planting window, and put the sowing at the early end of that "
        "window rather than the late end. A soil thermometer is the one cheap tool worth having, "
        "since the same early date that beats the disease can be too cold for the seed.",
    "pros": [
        "Costs nothing but a calendar decision, settled once on sowing day",
        "Shortens the weeks the crop and the disease weather overlap, so even a bad disease "
        "year does less damage",
        "Pairs naturally with a resistant variety, and together they are decisions made before "
        "anything is in the ground",
    ],
    "cons": [
        "Only helps against a disease that builds late in the season, and does nothing against "
        "one that arrives early in your area",
        "The early end of the window carries its own risk, since seed sown into cold, wet soil "
        "can rot before it comes up",
        "The margin depends on the year, and a season where the disease weather comes early "
        "shrinks the escape",
    ],
    "cautions": [
        "The race can be lost at the start instead of the end. Seed sown into cold, wet soil "
        "can rot before it emerges: NC State puts the working floor for sweet corn at 50°F soil "
        "for standard varieties and 60°F for the high-sugar types, and states that seed planted "
        "in moist soil below those temperatures will often rot. Sow at the early edge of what "
        "the seedbed allows, not past it.",
        "An early sowing shortens the crop's overlap with the disease weather rather than "
        "preventing infection, so it is a companion to a resistant variety, not a substitute "
        "for one. The sources that state the escape put resistance first in the same sentence.",
        "This helps only where the disease pressure genuinely builds late, the pattern Cornell "
        "documents for sweet corn rust, first seen from mid-June onward and prevalent in late "
        "season plantings, and WSU for pea powdery mildew, often worse in the fall. Where the "
        "disease arrives early, an early sowing buys little and the cold-soil risk remains.",
    ],
    "sources": ["wsu_ext", "cornell_ext", "ncsu_ext"],
    "anchoring_urls": {
        "wsu_ext": {"url": "https://hortsense.cahnrs.wsu.edu/fact-sheet/pea-powdery-mildew/",
                    "verified": VERIFIED},
        "cornell_ext": {"url": "https://www.vegetables.cornell.edu/pest-management/"
                               "disease-factsheets/common-rust-of-sweet-corn/",
                        "verified": VERIFIED},
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu/organic-sweet-corn-production",
                     "verified": VERIFIED},
    },
}

# THE SAFETY GUARD. The escape is a race the grower can lose: an entry that recommends early
# sowing without the cold-seedbed trade tells a reader to rot their stand. Each axis needs ALL of
# its tokens present in the cautions.
REQUIRED_DISCLOSURES = {
    "seed_rot":   ("cold", "rot"),
    "threshold":  ("50°f",),
    "not_a_cure": ("rather than preventing",),
    "resistance": ("not a substitute",),
    "late_build": ("builds late",),
}

# `best_use` must hold this method apart from the two keys it is most likely to be collapsed into.
# planting_time_avoidance was proposed as a widening target and REFUSED; resistant_varieties is the
# rung this one will sit beside on six of seven ladders.
REQUIRED_CONTRASTS = ("flight window", "published", "weather-driven", "what you plant")

# The four problems whose prose MATCHED the scan and must never carry the rung. Each is wrong in
# its own way, and spinach is the dangerous one: it is typed `fungal`, so a rung there would be
# LEGAL per TYPE_TARGETS while advising the exact harm. Restated in the backfill as a literal too;
# a cross-import couples two frozen records and kills the mutation harness.
EXCLUSIONS = (
    ("spinach", "damping-off"),            # OPPOSITE DIRECTION: early sowing into cold soil is
                                           # what CAUSES damping-off; its prose says wait for
                                           # warmth. The one exclusion the gate cannot catch.
    ("radish", "black-rot"),               # inherent crop SPEED, not a sowing decision; and
                                           # bacterial, so the gate also refuses it
    ("cilantro-coriander", "powdery-mildew"),  # escape by early HARVEST, not by sowing date
    ("jalapeno", "mosaic-viruses"),        # roguing ("remove infected plants early"), not a
                                           # sowing date; and viral
)

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
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


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def missing_disclosures(m):
    """Which trade axes the cautions fail to state. Each needs ALL of its tokens present."""
    blob = " ".join(m.get("cautions") or []).lower()
    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()
                  if not all(t in blob for t in toks))


def missing_contrasts(m):
    """Which near-miss distinctions `best_use` fails to draw."""
    blob = (m.get("best_use") or "").lower()
    return sorted(t for t in REQUIRED_CONTRASTS if t not in blob)


def find_problem(data, slug, ident):
    """A problem matched by `id` OR by `name`, so an exclusion stays resolvable either way."""
    for c in data.get("crops") or []:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):
                    return p
    return None


def rungs_of(data, key):
    """Every (slug, problem id or name) carrying a rung for `key`, anywhere on the roster."""
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
    if METHOD["tier"] != "cultural":
        return (f"tier is {METHOD['tier']!r}; a sowing-date decision is a cultural practice and "
                f"any other tier misorders every ladder it lands on")
    if METHOD["applies_to"] != ["fungal_foliar"]:
        return (f"applies_to must be exactly ['fungal_foliar']; all seven measured instances are "
                f"foliar fungal diseases, and a wider scope would make this legal on problems no "
                f"source covers")

    # THE SAFETY GUARD. Without the cold-seedbed trade this sheet tells a reader to rot a stand.
    miss = missing_disclosures(METHOD)
    if miss:
        return (f"the cautions do not state {miss}; the escape is a race the grower can lose, NC "
                f"State quantifies the cold-soil floor, and a sheet that recommends early sowing "
                f"without the trade can cost a reader their stand")

    # The whole reason this is a new key rather than a widening.
    miss = missing_contrasts(METHOD)
    if miss:
        return (f"best_use does not distinguish this method from {miss}; "
                f"planting_time_avoidance dodges a published flight window while this races an "
                f"unpublished weather epidemic, and resistant_varieties changes what you plant "
                f"rather than when, and a reader who cannot tell them apart will pick the wrong "
                f"one")

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

    # EVERY EXCLUSION MUST RESOLVE. A typo in a slug or a problem id would leave the backfill's
    # refusal protecting nothing while still reporting green -- the derived-guard vacuity shape.
    for slug, ident in EXCLUSIONS:
        if find_problem(data, slug, ident) is None:
            return (f"exclusion {slug}/{ident!r} does not resolve to a problem in canonical, so "
                    f"the refusal it encodes would protect nothing")
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

    # SUBSTANTIVE INVARIANTS FIRST, and the verbatim check LAST of this group: `cm[KEY] != METHOD`
    # subsumes every check below it, so placing it first would make the disclosure, contrast,
    # applies_to and tier branches unreachable by any post-state mutation (the masked-guard shape
    # the trap-cropping harness caught).
    if KEY not in cm:
        return "post: the method was not minted"
    miss = missing_disclosures(cm[KEY])
    if miss:
        return f"post: the shipped cautions do not state {miss}"
    miss = missing_contrasts(cm[KEY])
    if miss:
        return f"post: the shipped best_use does not distinguish {miss}"
    if cm[KEY]["applies_to"] != ["fungal_foliar"]:
        return "post: applies_to is not the narrow scope"
    if cm[KEY]["tier"] != "cultural":
        return "post: the tier is not cultural"
    if cm[KEY] != METHOD:
        return "post: the method did not land verbatim"

    # REFUSAL-SPEC. This promote mints only; no ladder anywhere may gain the rung, and the four
    # excluded problems must not carry it in this state or any later one. The four are checked
    # BEFORE the mint-only sweep, so each branch is reachable on its own and a rung on an excluded
    # problem reports WHY it is forbidden rather than the generic mint-only message.
    for slug, ident in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return f"post: exclusion {slug}/{ident!r} no longer resolves"
        if any(r.get("method") == KEY for r in p.get("control_ladder") or []):
            return (f"post: {slug}/{ident!r} carries a {KEY} rung, and it is one of the four "
                    f"scan matches that must never get one")
    landed = rungs_of(data, KEY)
    if landed:
        return (f"post: {landed} gained a {KEY} rung, and this promote mints only; the rungs are "
                f"a separate promote")

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
    # CHAIN-REPLAY CONTRACT: promote_fixture._from_chain invokes this as
    #   <script> --canonical PATH --expect-sha SHA --apply
    # and this mint produces the backfill's base, so it is a CHAIN member.
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

    print(f"PLA-8 -- mint {KEY}, the gap batch 12 measured and could not fill")
    print(f"  control_methods : {before} -> {len(data['control_methods'])}")
    print(f"  tier            : {METHOD['tier']}   applies_to: {METHOD['applies_to']}")
    print(f"  disclosures     : {sorted(REQUIRED_DISCLOSURES)} all stated in the cautions")
    print(f"  contrasts       : best_use holds it apart from planting_time_avoidance and "
          f"resistant_varieties")
    print(f"  crops touched   : 0   existing methods touched: 0   sources touched: 0")
    print(f"  NOTE            : 7 ladders gain no rung here; the backfill is a separate promote, "
          f"and {len(EXCLUSIONS)} scan matches are excluded from it")
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
