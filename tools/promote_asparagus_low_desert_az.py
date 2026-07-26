#!/usr/bin/env python3
"""Author asparagus low_desert_az z9/z10 and re-rate -- the same defect as ca_desert z10.

THE DEFECT. low_desert_az z9 and z10 sat at `unsuitable` with all-`growing` placeholder calendars,
justified by the retired chill mechanism. This is the SAME ground as the just-corrected
ca_desert z10: UCCE Imperial's Bell names the production locations outright --

  "Asparagus is grown in four locations in the Lower Colorado Desert; the Cochella Valley, the
   Imperial Valley, Yuma, AZ., and Mexicali, Mexico."

-- so a UC extension source names Arizona low-desert ground as asparagus country in the same
breath as Imperial and Coachella, which the dataset now rates `perennializes`.

MY OWN ERROR, CORRECTED HERE. Arc 2's roster-wide note repair applied a "both routes to dormancy
fail" note to these cells, asserting "there is no dry season long enough to substitute". That is
correct for the summer-WET failures it was written for (Hawaii, peninsular Florida, RGV) and
WRONG for the arid Arizona desert, where a dry-down is the one thing the climate reliably
supplies. The blanket was applied too widely and is fixed here.

EVIDENCE, verified by direct extraction rather than relayed:
  - UA az1615 (Yuma County home-garden calendar, z10a):
      "Asparagus | October-February | March-April | 8 | 4 to 6 | 20 to 24"
      under headers "Planting Window | Harvest Window | Planting Depth (in) | ...". The 8-inch
      depth is a CROWN depth (asparagus seed goes in at about half an inch), and the calendar
      header states "This calendar has been made for seeds unless otherwise noted, but
      transplants can also be planted during these times as well."
  - UA az1005 (Maricopa County home-garden calendar, the z9 side): the asparagus row reads
      "Asparagus 2-3 years T T T T T T T" -- SEVEN transplant marks and ZERO seed marks, against
      a legend of S = Seeds / T = Transplants. Maricopa recommends this crop by crown, with a
      2-to-3-year establishment lag. NOTE: the month POSITIONS of those marks were not reliably
      recoverable from the rotated table, so this source is cited for the transplant-only
      recommendation and the establishment lag, NOT for the window.

WINDOW: mirrors the verified ca_desert z10 authoring, same Lower Colorado Desert. No source
splits z9 from z10, so both carry the same window (the pnw z8/z9 precedent).

THE COUNTERWEIGHT, kept rather than suppressed. `tamu_agrilife` is cited on these cells for "It
produces poorly in areas with mild winters and extremely long, hot summers" -- a real T1 statement
that argues against this rating, and Phoenix/Yuma is squarely that climate. It is retained as a
source and its substance is carried in the prose: production here is lighter and the season
shorter than in cold-winter regions. It does not override direct local extension endorsement of
the crop for local home gardeners, which is what a suitability rating is answering.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_low_desert_az.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"
VERIFIED = "2026-07-26"

CALENDAR = ["cold_pause", "cold_pause", "harvest", "harvest", "growing", "growing",
            "growing", "growing", "growing", "growing", "cold_pause", "cold_pause"]
PLANT_OUT = "Nov 1 - Feb 1 (dormant crowns, one-time planting)"
HARVEST = "Mar - Apr"

NEW_SOURCES = {
    "ua_az1005": {
        "id": "ua_az1005",
        "name": "UA Extension az1005, Vegetable Planting Calendar for Maricopa County",
        "publisher": "University of Arizona Cooperative Extension",
        "url": "https://extension.arizona.edu/sites/default/files/2024-08/az1005-2018.pdf",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "UA Extension home-garden planting calendar for Maricopa County (Phoenix, "
                       "the cooler side of the Arizona low desert). Lists asparagus with "
                       "transplant-only marks and a 2-to-3-year time to harvest. Cited for the "
                       "crown recommendation and establishment lag, not for month placement -- "
                       "the table is rotated and its mark positions did not extract reliably."},
}

NOTES = {
    "9": ("On the cooler side of the Arizona low desert spears come in March; harvest March into "
          "April, then carry the fern through a long, very hot summer on deep, regular water. "
          "Winter will not stop the plant here, so the rest has to be deliberate: cut irrigation "
          "in fall, let the fern dry down, and cut it to the ground before spring. Set crowns "
          "from November into early February. Expect lighter cuttings and a shorter season than a "
          "cold-winter garden gets, since fern growth slows above 85°F."),
    "10": ("On the Yuma-side valley floor asparagus is a genuine local crop, not an experiment: "
           "UC extension lists Yuma alongside the Imperial and Coachella valleys as Lower "
           "Colorado Desert asparagus ground. Spears come in March; harvest March into April, "
           "then run the fern through the summer on deep, regular water. The annual rest comes "
           "from a fall dry-down rather than frost, so stop watering, let the fern brown, and cut "
           "it down before spring. Set crowns from November into early February. Heat above 85°F "
           "slows fern growth, so summer shade and salt management matter more here than cold "
           "ever will."),
}

REGION_NOTES = (
    "Heat, not winter warmth, is the limit in the Arizona low desert: fern development is reduced "
    "above 85°F, so summer water and shade decide how well the crown reloads. The annual rest "
    "comes from a deliberate fall dry-down rather than frost, which this arid climate supplies "
    "readily. UC extension names Yuma alongside the Imperial and Coachella valleys as Lower "
    "Colorado Desert asparagus ground, and the Yuma and Maricopa county calendars both list the "
    "crop for home gardeners. Expect lighter cuttings and a shorter season than a cold-winter "
    "region delivers, and watch soil salinity on a bed meant to hold for a decade.",
    "Asparagus is worth growing in the low desert, which surprises people. Give it deep water and "
    "summer shade, then stop watering in fall so the ferns dry down and the plant gets its rest, "
    "and cut them back before spring. Plant crowns from November into early February and pick "
    "your first spears in March and April once the bed is established. Harvests are lighter than "
    "in cold-winter country, but a well-kept bed lasts for years.",
)

FINDINGS = [
    {
        "id": "asparagus_low_desert_az_rerated_from_retired_chill_mechanism",
        "summary": "low_desert_az z9 and z10 re-rated `unsuitable` -> `perennializes` 2026-07-26, "
                   "closing the last cells resting on the retired chill mechanism. Decisive "
                   "evidence: UCCE Imperial (Bell) names the Lower Colorado Desert asparagus "
                   "locations outright -- 'the Cochella Valley, the Imperial Valley, Yuma, AZ., "
                   "and Mexicali, Mexico' -- so a UC source places Arizona low-desert ground in "
                   "the same production district as cells the dataset already rates "
                   "`perennializes`. Corroborated by two UA home-garden calendars: az1615 (Yuma) "
                   "carries 'Asparagus | October-February | March-April' at an 8-inch planting "
                   "depth (a CROWN depth; seed goes in at about half an inch) with a header "
                   "stating transplants may be planted in the same windows, and az1005 "
                   "(Maricopa) lists asparagus with SEVEN transplant marks and ZERO seed marks "
                   "plus a 2-to-3-year time to harvest. SELF-CORRECTION RECORDED: arc 2's "
                   "roster-wide note repair applied a 'both routes to dormancy fail' note to "
                   "these cells, asserting no dry season is available -- true for the summer-WET "
                   "climates it was written for (Hawaii, peninsular Florida, RGV) and WRONG for "
                   "the arid Arizona desert. A blanket note was applied too widely; when a "
                   "mechanism repair sweeps many cells, re-check each against the mechanism "
                   "rather than assuming the class is uniform.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_low_desert_az_tamu_counterweight",
        "summary": "COUNTERWEIGHT retained on low_desert_az rather than suppressed: "
                   "`tamu_agrilife` states 'It produces poorly in areas with mild winters and "
                   "extremely long, hot summers', and Phoenix/Yuma is squarely that climate. It "
                   "was kept as a cell source and its substance carried in the prose (lighter "
                   "cuttings, shorter season, fern growth slowed above 85F) rather than being "
                   "dropped to make the new rating look cleaner. The rating still moves because a "
                   "suitability call answers whether a local home bed establishes and persists, "
                   "and the local extension services for exactly this ground (UA Yuma and "
                   "Maricopa) list the crop for their own home gardeners while UC names Yuma a "
                   "production location. Also note az1005's mark POSITIONS were not recoverable "
                   "from its rotated table, so it is cited for the transplant-only recommendation "
                   "and the establishment lag only -- the window comes from az1615 and the "
                   "verified ca_desert z10 authoring.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
]


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    cat = data.setdefault("source_catalog", {})
    added = [k for k in NEW_SOURCES if k not in cat]
    for k, v in NEW_SOURCES.items():
        cat.setdefault(k, v)

    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    region = (crop.get("regions") or {}).get("low_desert_az")
    if not isinstance(region, dict):
        print("ABORT: low_desert_az region not found")
        sys.exit(1)

    for z in ("9", "10"):
        cell = (region.get("resolved_by_zone") or {}).get(z)
        if not isinstance(cell, dict):
            print(f"ABORT: low_desert_az z{z} not found")
            sys.exit(1)
        if cell.get("suitability") != "unsuitable":
            print(f"ABORT: expected low_desert_az z{z} `unsuitable`, found {cell.get('suitability')!r}")
            sys.exit(1)

        cell["suitability"] = "perennializes"
        cell["calendar"] = list(CALENDAR)
        cell["plant_out"] = PLANT_OUT
        cell["harvest"] = HARVEST
        cell["notes"] = NOTES[z]
        cell["resolution_method"] = "extension_regional_guide"
        cell.pop("suitability_note_seasoned", None)
        cell.pop("suitability_note_beginner", None)

        srcs = list(cell.get("sources") or [])
        for s in ("ua_az1615", "ua_az1005", "ucce_imperial_lowdesert"):
            if s not in srcs:
                srcs.append(s)
        cell["sources"] = srcs
        au = dict(cell.get("anchoring_urls") or {})
        for s in srcs:
            url = (cat.get(s) or {}).get("url")
            if url and s not in au:
                au[s] = {"url": url, "verified": VERIFIED}
        cell["anchoring_urls"] = au

    region["region_notes_seasoned"], region["region_notes_beginner"] = REGION_NOTES

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    have = {f.get("id") for f in ofs if isinstance(f, dict)}
    for f in FINDINGS:
        if f["id"] not in have:
            ofs.append(f)

    from collections import Counter
    split = Counter(c.get("suitability") for r in crop["regions"].values()
                    for c in (r.get("resolved_by_zone") or {}).values()
                    if isinstance(c, dict) and c.get("suitability"))
    print(f"catalog additions : {added}")
    print(f"low_desert_az z9  : unsuitable -> perennializes")
    print(f"low_desert_az z10 : unsuitable -> perennializes")
    print(f"suitability split : {dict(split)}")
    print(f"open_findings     : {len(ofs)}")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
