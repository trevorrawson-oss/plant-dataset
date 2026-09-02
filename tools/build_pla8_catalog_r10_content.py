#!/usr/bin/env python3
"""PLA-8 catalog round 10: WIDEN `certified_clean_stock` to reach insect-typed problems, and
GENERALIZE its prose from pathogens to planting-stock-borne pests. Base e6c986e3.

--------------------------------------------------------------------------------------------------
WHY -- and why the widening ALONE would have been a defect
--------------------------------------------------------------------------------------------------
`certified_clean_stock.applies_to` carried no `insect_*` target, so it was ILLEGAL on any problem
typed `insect`. Measured on the live roster: it appears on **93 rungs (55 fungal, 30 bacterial,
6 viral, 2 nematode) and ZERO insect** against this round's base. (86 was the count on b118f19d;
batch 23 added 7 more on its own disease-typed problems.) Two of batch 23's three authoring agents reported it
independently, which is the playbook's own trigger for "that is the catalog, not the authors".

**14 rungs are blocked, and reading them splits into two classes that need different things.**

CLASS A -- 10 rungs, where the reason is a PATHOGEN the stock carries and the insect is the vector:
  * asian-citrus-psyllid on all five citrus: "buy certified disease-free trees" (huanglongbing)
  * aphids on strawberry, raspberry, blackberry: "certified virus-free plants"
  * potato/aphids-virus-vectors and sweet-potato/whiteflies-virus-vectors: virus in the seed or slip
For these the method's EXISTING disease-framed prose is already correct. They are blocked only
because the entry is filed under the vector and therefore typed `insect`.

CLASS B -- 4 rungs, where the reason is THE PEST ITSELF riding inside the planting material:
  * sweet-potato/sweet-potato-weevil: "certified weevil-free slips"
  * raspberry and blackberry /raspberry-crown-borer: "certified, borer-free stock"
  * strawberry/root-crown-weevils: "start with clean stock"
For these the shipped prose would render WRONG. `how_it_works_beginner` said "material that is not
already carrying **the disease**"; `find_it_beginner` said look for "certified **disease-free**" seed
and reject transplants showing "spotting, mottling or wilt", which is disease inspection offered to
a reader dealing with a weevil.

**That is exactly the hazard the playbook names:** `applies_to` governs what the GATE accepts and
does nothing to what a READER sees; widening `balance_nitrogen` to cover blossom-end rot would have
put aphid prose onto a calcium disorder. So the widening is paired with a prose generalization
rather than shipped alone.

--------------------------------------------------------------------------------------------------
WHY GENERALIZE RATHER THAN MINT A SECOND METHOD
--------------------------------------------------------------------------------------------------
The method's own seasoned text ALREADY reaches past pathogens: "the stem and bulb nematode arrives
inside infected garlic cloves, and no in-season measure reaches **a pest** already inside the tissue
you planted." The concept already spans an animal riding in planting stock; only the beginner-facing
text was written as if it did not. Minting "certified pest-free stock" beside "clean planting stock"
would put two near-identical entries in front of a reader for one decision, which is the confusion
`lower_soil_ph` had to be written to escape.

--------------------------------------------------------------------------------------------------
SOURCING -- fetched and READ on 2026-09-02, not taken from a search summary
--------------------------------------------------------------------------------------------------
UC IPM, Caneberries / Raspberry Crown Borer, read verbatim:

    "The use of clean planting stock is necessary to reduce the movement of infested plant stock
     from one field to another."

That is an INSECT, moving between plantings inside planting stock, with clean stock named as the
control. It is the anchor for the generalization and the only source this round adds.

**A search summary was refused as evidence and it mattered.** A web search returned the sentence
"use only certified slips or transplants from weevil-free areas" attributed to NC State's Pests of
Sweetpotato. Fetching the document shows it does NOT contain that sentence; what it says is the
weaker, conditional "If slips for planting cannot be obtained from a weevil-free area, each
sweetpotato chosen for seed should be examined carefully and destroyed if infested." The stronger
sentence was the summarizer's, not the document's.

FILED, NOT FIXED HERE -- a mis-pointed source key on a crop record: sweet-potato's weevil entry says
"Buy **certified**, weevil-free slips" and cites `clemson_hgic_1322_sweet_potato` and `uf_ifas_edis`
IN154. Clemson HGIC 1322 **does not mention the weevil at all**; IN154 says only "The slips or
cutting used to plant the crop should be free of weevils", which supports weevil-free but not
certified. The claim IS supportable -- NCDA&CS states "Purchase only certified and tagged sweetpotato
weevil-free plants from known sources" -- so this is the right claim under the wrong key, the
`vce_426_331` shape, and belongs to the citation cleanup arc rather than to a catalog round.

--------------------------------------------------------------------------------------------------
WHICH TARGET, AND WHAT IT OPENS
--------------------------------------------------------------------------------------------------
`insect_general` ONLY. It is the generic insect target, so it reaches every `insect`-typed problem;
it also reaches `mite`, and that was measured rather than waved at: **zero mite-typed problems on the
roster name certified or clean stock**, so nothing authors it there today. The narrower per-behaviour
targets (`insect_boring`, `insect_chewing`, `insect_soft_bodied`) would each admit only part of the
14 and would need three entries to do one job.

**The prose scopes what the type vocabulary cannot.** The widening makes the method legal on 357
insect-typed problems; 14 are the cases it was read for. `best_use` therefore names slips, crowns and
roots outright, so an author choosing by `best_use` sees the intended case rather than a blanket
permission.

--------------------------------------------------------------------------------------------------
WHAT MUST SURVIVE
--------------------------------------------------------------------------------------------------
**93 shipped rungs already point at this method.** Every claim the text already makes must still be
there afterwards, byte-for-byte inside the new strings, because a widening that quietly rewrote what
the method meant would change 93 rungs' meaning without touching a single crop record. The guard
asserts each fragment by name.

Used by: tools/promote_pla8_catalog_r10.py
"""

VERIFIED = "2026-09-02"

# The one source this round adds. UC IPM is already T1 in source_catalog under other keys; the
# per-document naming convention here is `ucanr_ext_<topic>` (cf. ucanr_ext_spider_mites,
# ucanr_ext_sooty_mold, ucanr_ext_thrips).
NEW_SOURCES = {
    "ucanr_ext_raspberry_crown_borer": {
        "id": "ucanr_ext_raspberry_crown_borer",
        "name": "UC IPM -- Raspberry Crown Borer (Caneberries)",
        # READ OFF THE DOCUMENT on 2026-09-02, never inferred from the id or the URL, which is the
        # inference A54 exists to prevent. The page's own heading is "Raspberry Crown Borer" under
        # the section "Agriculture: Caneberries Pest Management Guidelines"; the shape follows its
        # sibling `uc_ipm_citrus_ants`, the same ipm.ucanr.edu/agriculture/<crop>/<pest>/ family.
        "title": "Raspberry Crown Borer / Caneberries / Agriculture: Pest Management Guidelines / "
                 "UC Statewide IPM Program (UC IPM)",
        "publisher": "UC Statewide Integrated Pest Management Program (UC ANR)",
        "url": "https://ipm.ucanr.edu/agriculture/caneberries/raspberry-crown-borer/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "tier": "T1",
        "accessed": VERIFIED,
        "citable_for": "UC IPM Pest Management Guidelines: Caneberries, UC ANR Publication 3437. "
                       "Cited for the movement of raspberry crown borer between plantings inside "
                       "infested planting stock: \"The use of clean planting stock is necessary to "
                       "reduce the movement of infested plant stock from one field to another.\"",
    },
}

# Fragments the EXISTING method already asserts. 93 shipped rungs were authored against them, so
# each must still be present after the amendment.
MUST_SURVIVE = {
    "certified_clean_stock": (
        "tested or treated seed",
        "cuttings, crowns or divisions",
        "Basil downy mildew is seed-borne",
        "gelatinous exudate in water",
        "Artichoke curly dwarf",
        "stem and bulb nematode arrives inside infected garlic cloves",
        "seed-borne foliar and vascular pathogens",
        "Set once, at purchase or propagation",
        "pathogen-tested",
        "steam or hot-water treated",
    ),
}

_HIW_B = (
    "Start the planting from material that is not already carrying the problem: tested or treated "
    "seed, healthy bought transplants, or, if you propagate your own, cuttings, crowns or divisions "
    "taken only from a clean plant. Several diseases, and a few pests, arrive inside the planting "
    "material rather than turning up later, and for most of those there is no cure once a plant has "
    "it, so this is the decision that does the work."
)

_HIW_S = (
    "Seed- and propagule-borne inoculum starts an epidemic inside the planting rather than at its "
    "edge, which is why clean stock sits ahead of every in-season measure for these diseases. Basil "
    "downy mildew is seed-borne, and seed is now lab-tested and steam treated for it, though basil "
    "seed is not amenable to hot-water treatment because it produces a gelatinous exudate in water. "
    "Artichoke curly dwarf runs the other way: there is no evidence it is seedborne, so seed and the "
    "transplants raised from it are the clean route into new ground where a crown division would "
    "carry the virus in. The same logic reaches planting-stock-borne nematodes: the stem and bulb "
    "nematode arrives inside infected garlic cloves, and no in-season measure reaches a pest already "
    "inside the tissue you planted. It reaches insects on the same footing where the insect spends "
    "part of its life inside the tissue being moved: UC IPM states that clean planting stock is "
    "needed to reduce the movement of infested plant stock from one field to another for raspberry "
    "crown borer, a larva that feeds inside the crown and travels with the plant."
)

_BEST_USE = (
    "Problems that travel in the planting material itself: seed-borne foliar and vascular pathogens, "
    "viruses carried in cuttings, crowns or divisions, the nematodes that ride inside seed cloves, "
    "bulbs and sets, and the insects that overwinter inside crowns, slips and roots. Set once, at "
    "purchase or propagation, before anything is in the ground."
)

_FIND_IT = (
    "Look for seed and plants sold as certified disease-free or pest-free, pathogen-tested, or steam "
    "or hot-water treated; for transplants, slips and crowns, inspect them before buying and pass "
    "over any with spotting, mottling, wilt, or holes and tunneling at the base."
)

_PROS = [
    "Acts before planting, on problems that have no cure once the plant has them",
    "One decision covers the whole planting, and it costs nothing extra to inspect a transplant",
]

_CONS = [
    "Does nothing about the same problem arriving from outside the garden later",
    "Tested or treated seed is not offered for every crop, and not every treatment suits every seed",
]

# The single widening. `add_targets` is a strict ADDITION; `set_fields` replaces whole strings, and
# every MUST_SURVIVE fragment is re-asserted against the result.
WIDENINGS = {
    "certified_clean_stock": {
        "add_targets": ["insect_general"],
        "add_sources": ["ucanr_ext_raspberry_crown_borer"],
        "add_anchors": {
            "ucanr_ext_raspberry_crown_borer": {
                "url": "https://ipm.ucanr.edu/agriculture/caneberries/raspberry-crown-borer/",
                "verified": VERIFIED,
            },
        },
        "set_fields": {
            "how_it_works_beginner": _HIW_B,
            "how_it_works_seasoned": _HIW_S,
            "best_use": _BEST_USE,
            "find_it_beginner": _FIND_IT,
            "pros": _PROS,
            "cons": _CONS,
        },
    },
}

# The cases the widening exists to unblock. Asserted, not assumed: each must be ILLEGAL before and
# LEGAL after. (crop, problem id)
UNBLOCKS = (
    ("sweet-potato", "sweet-potato-weevil"),
    ("sweet-potato", "whiteflies-virus-vectors"),
    ("potato", "aphids-virus-vectors"),
    ("raspberry", "raspberry-crown-borer"),
    ("blackberry", "raspberry-crown-borer"),
    ("strawberry", "root-crown-weevils"),
    ("strawberry", "aphids"),
    ("lemon", "asian-citrus-psyllid"),
)


def apply_round(data):
    cm = data["control_methods"]
    sc = data["source_catalog"]
    for sid, entry in NEW_SOURCES.items():
        if sid in sc:
            raise AssertionError(f"source {sid!r} already exists; this round would overwrite it")
        sc[sid] = dict(entry)
    for key, w in WIDENINGS.items():
        if key not in cm:
            raise AssertionError(f"{key} is not in the catalog, so it cannot be widened")
        m = cm[key]
        for t in w["add_targets"]:
            if t in m["applies_to"]:
                raise AssertionError(f"{key} already applies to {t!r}")
            m["applies_to"] = list(m["applies_to"]) + [t]
        for s in w["add_sources"]:
            if s not in m["sources"]:
                m["sources"] = list(m["sources"]) + [s]
        anchors = dict(m.get("anchoring_urls") or {})
        anchors.update({k: dict(v) for k, v in w["add_anchors"].items()})
        m["anchoring_urls"] = anchors
        for f, v in w["set_fields"].items():
            m[f] = list(v) if isinstance(v, list) else v
    return {"widened": sorted(WIDENINGS), "sources_added": sorted(NEW_SOURCES)}


if __name__ == "__main__":
    import json, os
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    before = dict(d["control_methods"]["certified_clean_stock"])
    n_sc = len(d["source_catalog"])
    s = apply_round(d)
    after = d["control_methods"]["certified_clean_stock"]
    print(f"widened        : {', '.join(s['widened'])}")
    print(f"applies_to     : {before['applies_to']} -> {after['applies_to']}")
    print(f"sources        : {before['sources']} -> {after['sources']}")
    print(f"methods total  : {len(d['control_methods'])} (unchanged)")
    print(f"source_catalog : {n_sc} -> {len(d['source_catalog'])}")
