#!/usr/bin/env python3
"""Author the PLA-8 control-method catalog extension: 3 new methods + 5 applies_to corrections.

SPEC + FULL PROVENANCE: docs/2026-08-22-control-method-catalog-extension-spec.md. Every claim here
is quoted from a document fetched and READ 2026-08-22; nothing is cited from memory.

WHY THE CATALOG GROWS. Measured against TYPE_TARGETS, `nematode` and `viral` are declared problem
types that ZERO of the 37 methods target, so a nematode or virus problem can only ever reach the 4
methods marked `any`. Five independent authoring bots hit that wall on five unrelated crops the same
afternoon. This is not gate housekeeping: plant-app renders a ladder from whatever methods a problem
resolves to, so those types currently bottom out at four generic rungs and read to a grower as "we
have almost nothing to say about this."

SOURCING CONVENTION, verified against the existing 37 rather than assumed. `water_spray` already
carries source `ucanr_ext` (bare, T1, catalogued) with a DOCUMENT-SPECIFIC `anchoring_urls` entry
pointing at the exact Pest Note. So a new method needs no new source_catalog id: bare `ucanr_ext`
plus its own URL is the house pattern, used by 30 of 37.

THE ONE PLACE THAT BREAKS. `anchoring_urls` is keyed by source id, so one source id carries exactly
one URL. A method that serves two pest types on the strength of TWO documents cannot express both
under a single `ucanr_ext` key. Rather than silently drop the second document or overwrite the
first, the widened methods ADD a document-scoped sibling id (the PLA-253 pattern: add a source,
never replace one), titled from the document per A54.

Run: python3 tools/build_catalog_extension_content.py [--emit PATH]
"""
import argparse
import json
import sys

# ---------------------------------------------------------------- new source_catalog entries
# Titled FROM THE DOCUMENT (<title> read at fetch time), never inferred from the URL -- A54.
NEW_SOURCES = {
    "ucanr_ext_spider_mites": {
        "id": "ucanr_ext_spider_mites",
        "name": "UC IPM Pest Notes -- Spider Mites",
        "title": "Spider Mites / Home and Landscape / UC Statewide IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM Pest Notes 7405. Cited for the MITE-specific efficacy of controls this catalog "
            "already carried for insects only: forceful water spraying ('regular, forceful spraying "
            "of plants with water often will reduce spider mite numbers adequately'), insecticidal "
            "soap and oil ('use an insecticidal oil or insecticidal soap'), and drought stress as a "
            "driver ('Water plants enough so they are not drought stressed, which increases mites "
            "and mite damage')."
        ),
        "_admission_provenance": (
            "Minted 2026-08-22 (PLA-8 catalog extension). Four methods were blocked on `mite` by "
            "applies_to that looks like an artifact of the 7-crop ladder pilot rather than "
            "considered biology. Discovered when a heirloom-tomato authoring pass found the crop's "
            "own prose naming a water blast and consistent watering as the PRIMARY spider-mite "
            "controls while the catalog made both unauthorable. Document fetched (55,187 bytes) and "
            "read before pinning."
        ),
    },
    "ucanr_ext_snails_slugs": {
        "id": "ucanr_ext_snails_slugs",
        "name": "UC IPM Pest Notes -- Snails and Slugs",
        "title": "Snails and Slugs / Home and Landscape / UC Statewide IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM Pest Notes 7427. Cited for hand-picking as a mollusk control: 'Handpick from "
            "plants at night or from fence ledges, undersides of decks, and meter boxes' and "
            "'Hand-picking can be very effective if done thoroughly on a regular basis.'"
        ),
        "_admission_provenance": (
            "Minted 2026-08-22 (PLA-8 catalog extension). `handpick` was insect-only, so a "
            "swiss-chard authoring pass could not author night hand-picking even though the crop's "
            "own slug entry leads its treatment with it. Document fetched (62,477 bytes) and read "
            "before pinning."
        ),
    },
}

# ---------------------------------------------------------------- the three new methods
NEW_METHODS = {
    "soil_solarization": {
        "name": "Soil solarization",
        "tier": "physical",
        # UC IPM 74145: "Solarization controls many soilborne fungi and bacteria, nematodes, and
        # some weeds." This is the method that ends `nematode`'s dead branch.
        "applies_to": ["nematode", "fungal_soilborne", "bacterial", "disease_general"],
        "how_it_works_beginner": (
            "Cover damp, bare soil with clear plastic for four to six weeks in the hottest part of "
            "summer and let the sun cook it. Trapped heat can push the top foot of soil to around "
            "140°F, which kills off a lot of what lives down there: soil-borne fungi and bacteria, "
            "many weed seeds, and a good share of the microscopic soil worms called nematodes. It "
            "costs almost nothing but it costs you the bed for a season."
        ),
        "how_it_works_seasoned": (
            "Transparent film, not black, laid over pre-moistened soil; wet soil conducts heat, so "
            "moisture is doing as much work as the plastic. Four to six weeks at peak insolation "
            "raises the top 12 to 18 inches to lethal temperatures. Effective against soilborne "
            "fungi, bacteria and weeds, and useful but weaker against nematodes."
        ),
        "best_use": (
            "A bed with a known soil-borne problem, treated in the off season before replanting. "
            "Most worthwhile where a nematode or root-rot history has already cost you a crop."
        ),
        "find_it_beginner": (
            "Clear polyethylene sheeting from a hardware or garden store. Clear, not black: black "
            "plastic absorbs the heat instead of letting it through to the soil."
        ),
        "pros": [
            "Nonchemical, and reaches soil-borne problems that sprays cannot touch",
            "Works on fungi, bacteria, weed seeds and nematodes at the same time",
        ],
        "cons": [
            # THE SOURCE'S OWN HEDGE, carried rather than compressed away.
            "Less effective on nematodes than on fungi and weeds, because nematodes can move deeper "
            "into the soil to escape the heat",
            "The effect reaches only about the top foot and lasts roughly a year, so it suits "
            "annual beds or getting a young plant established, not a permanent fix",
            "Takes the bed out of production for four to six weeks of your best growing weather",
        ],
        "cautions": [
            "Needs a genuinely hot, sunny stretch. In cool, windy or cloudy conditions the soil may "
            "never reach the temperatures that make it work."
        ],
        "sources": ["ucanr_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74145.html",
                          "verified": "2026-08-22"}
        },
    },
    "improve_drainage": {
        "name": "Improve drainage",
        "tier": "cultural",
        "applies_to": ["fungal_soilborne", "disease_general"],
        "how_it_works_beginner": (
            "Root rots need wet soil, and they can get going in as little as four to eight hours of "
            "saturated ground. Raised beds, a better-drained spot, and watering that lets the soil "
            "drain between soakings remove the condition the disease depends on. There is no spray "
            "for this; drainage is the control."
        ),
        "how_it_works_seasoned": (
            "Phytophthora and the other soilborne rots are water-mold diseases: free water in the "
            "pore space is what lets them move and infect. UC IPM names proper irrigation the single "
            "most important preventive measure, and puts the saturation window at four to eight "
            "hours. Raised beds are the standard fix for vegetables on heavy ground."
        ),
        "best_use": (
            "Any bed with a history of plants wilting and not recovering after watering, and as "
            "standard practice on heavy or low-lying ground before planting anything susceptible."
        ),
        "pros": [
            "Removes the condition the disease needs rather than treating the plant",
            "Costs nothing on a site you have not planted yet, and helps every crop in the bed",
        ],
        "cons": [
            "Does nothing for a plant already infected; there is no rescue once roots have rotted",
            "Rebuilding a bed or changing a site is real work, and not always possible",
        ],
        "sources": ["ucanr_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74133.html",
                          "verified": "2026-08-22"}
        },
    },
    "reflective_mulch": {
        "name": "Reflective mulch",
        "tier": "cultural",
        # UC IPM 7404 anchors BOTH targets in one sentence; this ends `viral`'s dead branch.
        "applies_to": ["insect_soft_bodied", "viral"],
        "how_it_works_beginner": (
            "Silver-colored mulch laid on the bed bounces light upward and confuses aphids looking "
            "for somewhere to land, so fewer settle on young plants. That matters most because "
            "aphids carry plant viruses from one plant to the next, and a virus has no cure once it "
            "is in. Use it while plants are small; it does less as the canopy closes over it."
        ),
        "how_it_works_seasoned": (
            "Silver reflective mulches have been shown to reduce transmission of aphid-borne viruses "
            "in summer squash, melon and other susceptible vegetables, by repelling incoming alates "
            "rather than by killing anything. The documented benefit is specifically on seedlings "
            "and small plants, so the window is early and closes as foliage covers the mulch."
        ),
        "best_use": (
            "Vegetables with a local history of aphid-transmitted virus, laid at planting while the "
            "crop is still small. Squash, melon and cucumber are the documented cases."
        ),
        "find_it_beginner": (
            "Sold as silver or metallized plastic mulch; aluminum foil laid on the bed does the same "
            "job on a small scale."
        ),
        "pros": [
            "Reduces virus transmission, which no spray can do once a plant is infected",
            "Kills nothing, so natural enemies are untouched",
        ],
        "cons": [
            "The benefit is documented on seedlings and small plants, and fades as the canopy grows "
            "over the mulch",
            "Plastic sheeting to lay, hold down and remove at the end of the season",
        ],
        "sources": ["ucanr_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html",
                          "verified": "2026-08-22"}
        },
    },
}

# ---------------------------------------------------------------- applies_to corrections
# Each is a CORRECTION, not an addition: the method exists and the omission blocked a control the
# source leads with. Each carries the second document as an ADDED source, never a replaced one.
CORRECTIONS = {
    "water_spray":       ("mite", "ucanr_ext_spider_mites"),
    "insecticidal_soap": ("mite", "ucanr_ext_spider_mites"),
    # horticultural_oil is NOT here: it ALREADY carries `mite`. The spec listed it as a
    # correction on the strength of the same source sentence ("insecticidal oil or
    # insecticidal soap"), which was true but redundant. A no-op entry in a corrections
    # table reads as coverage it does not provide, so it is removed rather than left in.
    "even_watering":     ("mite", "ucanr_ext_spider_mites"),
    "handpick":          ("mollusk", "ucanr_ext_snails_slugs"),
}


def build(data):
    cm = data["control_methods"]
    for k in NEW_METHODS:
        if k in cm:
            raise SystemExit(f"ABORT: control_methods.{k} already exists")
    for k in CORRECTIONS:
        if k not in cm:
            raise SystemExit(f"ABORT: control_methods.{k} missing; nothing to correct")
    sc = data["source_catalog"]
    for k in NEW_SOURCES:
        if k in sc:
            raise SystemExit(f"ABORT: source_catalog.{k} already exists")
    return {"new_sources": NEW_SOURCES, "new_methods": NEW_METHODS,
            "corrections": {k: {"add_target": t, "add_source": s}
                            for k, (t, s) in CORRECTIONS.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit")
    a = ap.parse_args()
    data = json.load(open("crops_data_final.json"))
    content = build(data)
    print(f"new source_catalog entries : {len(content['new_sources'])}")
    print(f"new control_methods        : {len(content['new_methods'])}")
    for k, v in content["new_methods"].items():
        print(f"   {k:22s} tier={v['tier']:9s} applies_to={v['applies_to']}")
    print(f"applies_to corrections     : {len(content['corrections'])}")
    for k, v in content["corrections"].items():
        cur = data["control_methods"][k]["applies_to"]
        print(f"   {k:22s} {cur} + {v['add_target']!r}")
    if a.emit:
        json.dump(content, open(a.emit, "w"), ensure_ascii=False, indent=1)
        print(f"\nwrote {a.emit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
