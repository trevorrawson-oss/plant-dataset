#!/usr/bin/env python3
"""Author asparagus ca_desert z10 (Imperial/Coachella low desert) and re-rate it.

THE CELL THIS FIXES. ca_desert z10 was `unsuitable` with an all-`growing` placeholder calendar,
no window, and a note demanding "sustained cold rest". This is the Imperial and Coachella valley
floor -- one of the three areas UC ANR Pub 7234 names as California's PRIMARY asparagus
production districts. Arc 2 corrected the note but deliberately did NOT flip the rating, because
promoting it required a real calendar and inventing one to clear a rating is the fabrication the
T1-or-it-doesn't-ship bar exists to prevent. This pass authors it from sourced low-desert
phenology instead.

THE PROVENANCE OF THE ERROR, now identified. The retired "chill requirement" traces to
PlantVillage ("requires 90-150 days of cold temperature to break dormancy") -- .edu-HOSTED but an
aggregated crop-profile database, not an extension bulletin, and the claim is unattributed there.
Its own cited references are Minnesota, Tennessee, and a UC Davis HOME-GARDEN guide. It is
directly contradicted by UC ANR naming Imperial/Riverside a primary district with a December
harvest. No T1 source states a chilling requirement, chill-hour figure, or cold-days count for
asparagus anywhere.

WHY `perennializes`, in the mechanism's terms:
  - DORMANCY WINDOW: satisfied, by drought rather than cold. UC IPM (home-garden page): "If
    drought or cold weather do not stop vegetative fern growth, shoots will become spindly and
    less vigorous each year", and "Irrigation is usually stopped in September or October so that
    the plants will go dormant." UC IPM even anticipates the frost-free case in its cutback
    instruction: "After the frost turns the ferns brown OR DURING JANUARY IF FERNS ARE STILL
    GREEN, prune them down to the ground."
  - HEAT CEILING: survivable, not persistence-limiting. Fern development is reduced above 85F
    (Pub 7234), but desert fields carry the crop through summer on 10-to-15-day irrigation and
    reach full 5-foot fern. UC 157, the dominant desert cultivar, was BRED AT UC's Desert
    Research and Extension Center in Holtville, in the Imperial Valley, where UC's own page notes
    summer temperatures reach 120F; NMSU lists UC 157 as heat-tolerant.
  - EXISTENCE PROOF: Pub 7234 names "the southern desert valleys (Imperial and Riverside
    Counties)" a primary district; UCCE Imperial's Bell puts low-desert stand life at "10 to 20
    years".
  - HOME-GARDEN PROOF: two independent low-desert extension HOME calendars list asparagus with
    real windows -- UA az1615 (Yuma) and az1005 (Maricopa).

CALENDAR, home-garden (NOT the commercial cycle):
  Nov-Feb cold_pause  the managed rest: irrigation cut in Sep/Oct, fern dries down and is cut
                      (in January if still green). This is also the crown-planting window.
  Mar-Apr harvest     UA az1615 (Yuma, low desert, HOME) gives March-April. Deliberately LATER
                      than the commercial Dec-to-April season, because a backyard bed is not
                      force-started by a late-November fern chop plus a December forcing
                      irrigation. The commercial October cut is market-contingent and excluded.
  May-Oct growing     fern. Coded ACTIVE, not heat_pause: no T1 source says the desert fern
                      stalls, and commercial practice is to irrigate straight through summer to
                      full fern height. A heat_pause token would assert a stop nothing supports.

plant_out Nov 1 - Feb 1 matches UA az1005's transplant-only tick range exactly and sits inside
both UA az1615 (Oct-Feb) and Pub 7234's statewide "October through March is usually best for
establishing asparagus stands with transplants or crowns".

TRAP AVOIDED (again): UC IPM's "Desert Valleys / February-April" row is a SEED window, traceable
verbatim to Pub 7234's "In the low desert, asparagus seed is often spring planted from February
to April". It is NOT a crown window, and UC IPM separately says crowns go in "mid to late winter".

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_ca_desert_z10.py [--dry-run]
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
    "ucanr_pub7234_desert": None,   # placeholder, resolved below to reuse ucanr_pub7234
    "ua_az1615": {
        "id": "ua_az1615", "name": "UA Extension az1615, Yuma County vegetable planting calendar",
        "publisher": "University of Arizona Cooperative Extension",
        "url": "https://extension.arizona.edu/sites/default/files/2024-08/az1615-2020.pdf",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "UA Extension home-garden planting calendar for Yuma County, climatically "
                       "the same low desert as Imperial/Coachella across the state line. Carries "
                       "asparagus planting and harvest windows for backyard growers."},
    "ucce_imperial_lowdesert": {
        "id": "ucce_imperial_lowdesert",
        "name": "UCCE Imperial County, Asparagus in the Low Desert (Bell)",
        "publisher": "University of California Cooperative Extension, Imperial County",
        "url": "http://ucanr.edu/repository/a/?a=161158",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "UCCE Imperial County farm-advisor bulletin specific to low-desert "
                       "asparagus: harvest timing, the late-November fern chop, forcing "
                       "irrigation, and a 10-to-20-year low-desert stand life. Commercial lane."},
}

NOTES = (
    "The low desert is not marginal ground for asparagus: UC ANR names the southern desert "
    "valleys one of California's three primary asparagus districts, and UC 157, the standard "
    "desert variety, was bred at UC's research station in the Imperial Valley. What the crop "
    "needs here is a rest it cannot get from winter. Cut irrigation in September or October and "
    "let the ferns dry down, then cut them to the ground (in January if they are still green), "
    "and set crowns any time from November into early February. Spears follow in March and April "
    "for a home bed; growers who chop and force-irrigate in December cut far earlier. Through the "
    "summer the fern grows on regular deep water, slowed but not stopped by heat above 85°F. Beds "
    "here have run 10 to 20 years."
)

FINDING_RESOLVE = "asparagus_ca_desert_z10_rating_contradicted_needs_authoring"

FINDINGS = [
    {
        "id": "asparagus_chill_claim_provenance_plantvillage",
        "summary": "PROVENANCE of the retired chill mechanism, identified 2026-07-26. The "
                   "'asparagus requires winter chill' reasoning that justified nearly every "
                   "marginal/unsuitable asparagus rating traces to PlantVillage "
                   "(plantvillage.psu.edu): 'Asparagus grows best in regions with hot days and "
                   "cool nights and requires 90-150 days of cold temperature to break dormancy.' "
                   "That host is .edu but is an AGGREGATED CROP-PROFILE DATABASE, not an "
                   "extension bulletin; the claim is unattributed there, and its three cited "
                   "references are Minnesota, Tennessee, and a UC Davis home-garden guide. It is "
                   "directly contradicted by UC ANR naming Imperial/Riverside a primary asparagus "
                   "district with a December harvest, and by NMSU ('asparagus is relatively "
                   "winter hardy, with higher heat, drought, and salt tolerances'). LESSON: a "
                   ".edu HOST is not a T1 SOURCE -- tier on what the document IS (peer-reviewed "
                   "extension bulletin vs aggregated database vs reprinted regional text). Two "
                   "other ucanr.edu-hosted pages failed the same way on this crop: an ANR Small "
                   "Farms page that is a reprinted eastern/midwestern text ('In the east, in the "
                   "cool spring...'), and a Southern California planting schedule credited to "
                   "'Digital Gardener' using Sunset zones.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_ca_desert_z10_harvest_later_than_z9",
        "summary": "ORDERING TENSION accepted 2026-07-26 on the ca_desert ladder: z10 "
                   "(Imperial/Coachella, warmer) now carries a Mar-Apr home harvest while z9 "
                   "(Barstow/Blythe, cooler) carries Feb-Mar -- the warmer zone reads LATER, "
                   "which is counterintuitive. This is a sourced-vs-modeled asymmetry, not a "
                   "biology claim: z10's Mar-Apr comes from UA az1615, the only low-desert "
                   "HOME-GARDEN harvest statement found, whereas z9's Feb-Mar was modeled from "
                   "regional patterns during the 2026-07-24 cert (see the cert's own "
                   "calendar-placement finding). The sourced value was preferred for z10 rather "
                   "than smoothed to preserve a monotonic ladder. Commercial low-desert harvest "
                   "genuinely does run far earlier (first cut mid-December to mid-January, main "
                   "season to early April) because fields are force-started by a late-November "
                   "fern chop plus a December irrigation -- a home bed is not. If z9 is ever "
                   "re-sourced, revisit the pair together.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_low_desert_home_garden_gaps",
        "summary": "HONEST GAPS carried on the ca_desert z10 authoring (2026-07-26): no T1 source "
                   "gives a low-desert-specific CROWN window (Nov 1 - Feb 1 is assembled from "
                   "Pub 7234's statewide Oct-Mar plus UA az1005's transplant-only tick range and "
                   "az1615's Oct-Feb); no UC source addresses home-garden asparagus in Coachella "
                   "or Imperial specifically -- UCCE Imperial lists a Waisen (2022) Coachella "
                   "Valley planting guide in Imperial Agricultural Briefs 25(6):100-102 that is "
                   "not posted at a resolvable URL and is the single most valuable missing "
                   "document for this cell; no source states whether a low-desert home bed's fern "
                   "senesces on its own in a frost-free year or must be forced every year; and no "
                   "source quantifies the summer heat penalty to fern carbohydrate accumulation "
                   "in a 107F July (the 85F ceiling is stated, the consequence is not). Summer is "
                   "therefore coded as ACTIVE growing, not heat_pause -- a pause token would "
                   "assert a stop no source supports. Also note UC MG's 'Asparagus does well "
                   "where winters are cool and the soil occasionally freezes at least a few "
                   "inches deep', which is a real T1 optimum statement retained as a caveat, but "
                   "is contradicted as a LIMIT by UC's own desert production data.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
]

REGION_NOTES = (
    "Heat, not winter warmth, is the real limit in the desert: fern development is reduced above "
    "85°F, so summer shade and steady irrigation decide how well the crown reloads. The rest "
    "period comes from a deliberate fall dry-down rather than frost. Zone 9 on the cooler desert "
    "ground carries a bed well, and the zone 10 valley floor is genuinely productive asparagus "
    "country: UC counts the southern desert valleys among California's primary districts, with "
    "stands running 10 to 20 years. No California desert ground actually reaches zone 11.",
    "The desert suits asparagus far better than its reputation suggests. Give the bed real summer "
    "shade and deep water, then stop watering in fall so the ferns dry down and the plant gets "
    "its rest, and cut the ferns back before spring. Set crowns in late fall or winter. On the "
    "valley floor asparagus is a real local crop, not an experiment.",
)


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    cat = data.setdefault("source_catalog", {})
    added = []
    for k, v in NEW_SOURCES.items():
        if v is None or k in cat:
            continue
        cat[k] = v
        added.append(k)

    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    cell = ((crop.get("regions") or {}).get("ca_desert") or {}).get("resolved_by_zone", {}).get("10")
    if not isinstance(cell, dict):
        print("ABORT: ca_desert z10 cell not found")
        sys.exit(1)
    if cell.get("suitability") != "unsuitable":
        print(f"ABORT: expected ca_desert z10 to be `unsuitable`, found {cell.get('suitability')!r}")
        sys.exit(1)

    cell["suitability"] = "perennializes"
    cell["calendar"] = list(CALENDAR)
    cell["plant_out"] = PLANT_OUT
    cell["harvest"] = HARVEST
    cell["notes"] = NOTES
    cell["resolution_method"] = "extension_regional_guide"
    # promoted out of unsuitable: the "why this will not work" pair no longer applies.
    cell.pop("suitability_note_seasoned", None)
    cell.pop("suitability_note_beginner", None)

    srcs = list(cell.get("sources") or [])
    for s in ("ucanr_pub7234", "ua_az1615", "ucce_imperial_lowdesert"):
        if s not in srcs:
            srcs.append(s)
    cell["sources"] = srcs
    au = dict(cell.get("anchoring_urls") or {})
    for s in srcs:
        url = (cat.get(s) or {}).get("url")
        if url and s not in au:
            au[s] = {"url": url, "verified": VERIFIED}
    cell["anchoring_urls"] = au

    region = crop["regions"]["ca_desert"]
    region["region_notes_seasoned"], region["region_notes_beginner"] = REGION_NOTES

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    for f in ofs:
        if isinstance(f, dict) and f.get("id") == FINDING_RESOLVE:
            f["status"] = "resolved"
            f["summary"] += (" RESOLVED 2026-07-26: cell authored from sourced low-desert "
                             "phenology and re-rated to `perennializes`.")
    have = {f.get("id") for f in ofs if isinstance(f, dict)}
    for f in FINDINGS:
        if f["id"] not in have:
            ofs.append(f)

    from collections import Counter
    split = Counter(c.get("suitability") for r in crop["regions"].values()
                    for c in (r.get("resolved_by_zone") or {}).values()
                    if isinstance(c, dict) and c.get("suitability"))
    print(f"catalog additions : {added}")
    print(f"ca_desert z10     : unsuitable -> {cell['suitability']}")
    print(f"  plant_out       : {PLANT_OUT}")
    print(f"  harvest         : {HARVEST}")
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
