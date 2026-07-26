#!/usr/bin/env python3
"""Author asparagus timing fields (crop #120) -- the gap left by the cert arc.

WHAT THIS FIXES. asparagus certified 120/120 with NO plant_out and NO harvest window string on
any of its 39 zone cells: the app could not tell a grower when to set crowns, on the one crop
whose whole failure mode is "plants it, expects spears". The cert plan omitted the fields
deliberately ("an established permanent bed is planted once") and designated
`start_method`/`year_one_notes` as the crown window's new home -- but `start_method` carries no
timing and `year_one_notes` was never authored. The data moved out of the calendar and landed
nowhere. See docs/2026-07-25-asparagus-timing-gaps.md.

SCOPE (arc 1 of 2). Authors plant_out + harvest on the 25 cells where a T1 window exists,
establishment_years, and year_one_notes. Does NOT touch the suitability map: 7 cells whose
certified ratings are contradicted by T1 (6 CA upgrades + se_gulf z10 -> unsuitable) are
deferred to arc 2, along with the unsourced "chill requirement" reasoning in their notes.
se_gulf z10 gets NO plant_out: UF/IFAS omits asparagus from the Florida vegetable guide
entirely and states it cannot be grown in z10a, so there is no honest window to author.

plant_out ON A PERENNIAL MEANS THE ESTABLISHMENT WINDOW, not an annual replant -- the same
convention apple already uses ("Apr - May (dormant, bare-root)"). The parenthetical carries the
one-time framing for a human reader; the app suppresses it outside the establishment year.

CITATION REPAIR (surgical). Four cited sources do not support crown timing. Three of them ARE
legitimate asparagus sources for what they DO cover, so they stay: msu_ext (real asparagus
guide, no planting date), ucanr_ext (Kings County crop report -- its one timing sentence is
about HARVEST, which is exactly what it is kept for), wsu_ext (hortsense pest page). Only
unr_fs0261 is REMOVED: it is "Home Vegetable Production in Southern Nevada" and its sole
mention of the crop is the string "Stems - asparagus" in a list of edible plant parts. Correct
crown sources are ADDED alongside in every case.

Writes COMPACT per CLAUDE.md: separators=(",",":"), ensure_ascii=False, no trailing newline.

Usage: python3 tools/promote_asparagus_timing.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"
VERIFIED = "2026-07-26"

# 5 new catalog entries; every other source key used below already exists.
NEW_SOURCES = {
    "illinois_ext": {
        "id": "illinois_ext", "name": "University of Illinois Extension",
        "publisher": "University of Illinois Extension",
        "url": "https://extension.illinois.edu/gardening/asparagus",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "Cooperative Extension publications from the University of Illinois, an 1862 "
                       "Land Grant institution. Lower Midwest coverage; carries the soil-workability "
                       "crown-planting anchor."},
    "unr_sp0115": {
        "id": "unr_sp0115", "name": "UNR Extension SP-01-15, Becoming a Desert Gardener",
        "publisher": "University of Nevada, Reno Extension",
        "url": "https://naes.agnt.unr.edu/PMS/Pubs/2001-3427.pdf",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "UNR Extension special publication carrying a Southern Nevada vegetable "
                       "planting guide with an explicit asparagus window. Replaces unr_fs0261 for "
                       "asparagus timing, which does not cover the crop."},
    "wsu_em051e": {
        "id": "wsu_em051e", "name": "WSU EM051E, Home Vegetable Gardening in Washington",
        "publisher": "Washington State University Extension",
        "url": "https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "WSU Extension home-garden manual whose PNW planting calendar carries a "
                       "distinct 'Asparagus, Crown' row separate from 'Asparagus, Seed'."},
    "usu_washco_dates": {
        "id": "usu_washco_dates", "name": "USU Extension Washington County spring planting dates",
        "publisher": "Utah State University Extension",
        "url": "https://extension.usu.edu/washington/files/planting-dates-spring.pdf",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "USU Extension county planting-date sheets, one page per Washington County "
                       "city, naming asparagus crowns explicitly. Authoritative for St. George / "
                       "Utah Dixie, where statewide USU dates run about six weeks late."},
    "ucanr_pub7234": {
        "id": "ucanr_pub7234", "name": "UC ANR Publication 7234, Asparagus Production in California",
        "publisher": "University of California Agriculture and Natural Resources",
        "url": "https://my.ucanr.edu/repository/fileaccess.cfm?article=54042&p=+ZBSTYA",
        "source_class": "university_extension", "trust_tier": "high",
        "accessed": "2026-07", "tier": "T1",
        "citable_for": "UC ANR crop-specific asparagus publication, broken out by California "
                       "production region (desert valleys, Delta, Central Coast). Crown-specific, "
                       "unlike the UC IPM planting-date table, which is a seed table."},
}

# (region, zone) -> (plant_out, [sources to ADD], [sources to REMOVE], resolution_method)
# resolution_method records HOW the window was reached, so a DERIVED row never reads as sourced.
W = "(dormant crowns, one-time planting)"
WINDOWS = {
    # northern_tier: no source gives crown windows BY ZONE; this is a monotonic ladder built
    # from state-scoped T1 sources. The state->zone mapping is editorial and marked as such.
    ("northern_tier", "3"): (f"May 1 - Jun 5 {W}", ["ndsu_ext", "sdsu_ext"], [], "state_source_zone_mapped"),
    ("northern_tier", "4"): (f"Apr 20 - May 25 {W}", ["umaine_ext"], [], "state_source_zone_mapped"),
    ("northern_tier", "5"): (f"Apr 10 - May 20 {W}", ["iastate_ext", "illinois_ext"], [], "state_source_zone_mapped"),
    ("northern_tier", "6"): (f"Apr 1 - May 10 {W}", ["uconn_ext", "illinois_ext"], [], "state_source_zone_mapped"),
    ("northern_tier", "7"): (f"Mar 20 - Apr 20 {W}", ["mu_ext"], [], "state_source_zone_mapped"),
    # mid_atlantic z7 DIRECT (UMD HG16 table, Central MD, last frost Apr 15); z8 applies UMD's
    # own stated "shift a week or two earlier (Eastern Shore)" rule.
    ("mid_atlantic", "7"): (f"Mar 20 - Apr 15 {W}", [], [], "extension_direct"),
    ("mid_atlantic", "8"): (f"Mar 15 - Apr 15 {W}", [], [], "extension_shift_rule_applied"),
    # mid_south z7 DIRECT (MU: southern MO "late March or early April"). z8 (Delta) has NO
    # zone-specific source -- UADA is statewide, MO does not reach z8; anchor-derived.
    ("mid_south", "7"): (f"Mar 20 - Apr 15 {W}", [], [], "extension_direct"),
    ("mid_south", "8"): (f"Mar 1 - Apr 15 {W}", [], [], "soil_workable_anchor_derived"),
    # pnw: WSU EM051E "Asparagus, Crown" row opens at March/Middle; OSU gives the rule
    # ("as soon as the soil is workable", "three to four weeks before last expected frost").
    ("pnw", "8"): (f"Mar 10 - Apr 15 {W}", ["wsu_em051e"], [], "extension_chart_plus_anchor"),
    ("pnw", "9"): (f"Mar 1 - Apr 5 {W}", ["wsu_em051e"], [], "extension_chart_plus_anchor"),
    # warm_arid: the window exists ONLY as a drawn bar in the NMSU chart (no extractable text);
    # recovered from PDF content-stream geometry + visual render. Prose gives only the 50F anchor.
    ("warm_arid", "8"): (f"Feb 1 - Feb 28 {W}", [], [], "extension_chart_geometry"),
    # utah_dixie: statewide USU says April, which is ~6 weeks LATE for St. George. The county
    # source is crown-specific AND city-specific, and its last frost (Mar 30) matches ours.
    ("utah_dixie", "8"): (f"Feb 15 - Mar 15 {W}", ["usu_washco_dates"], [], "county_source_direct"),
    # nevada: unr_fs0261 REMOVED (does not mention asparagus). UNR SP-01-15 is the real source.
    ("nevada", "8"): (f"Feb 8 - Apr 30 {W}", ["unr_sp0115"], ["unr_fs0261"], "extension_regional_guide"),
    ("nevada", "9"): (f"Feb 8 - Apr 30 {W}", ["unr_sp0115"], ["unr_fs0261"], "extension_regional_guide"),
    ("nevada", "10"): (f"Feb 8 - Apr 30 {W}", ["unr_sp0115"], ["unr_fs0261"], "extension_regional_guide"),
    # ca_interior: uc_ipm's crown sentence ("mid to late winter") is on home turf here.
    ("ca_interior", "8"): (f"Jan 1 - Mar 15 {W}", ["ucanr_pub7234"], [], "extension_regional_guide"),
    ("ca_interior", "9"): (f"Jan 1 - Mar 15 {W}", ["ucanr_pub7234"], [], "extension_regional_guide"),
    # se_gulf z8 DIRECT (UGA B577 chart, Middle Georgia); z9 applies UGA's own stated
    # "South Georgia 2 weeks earlier" rule. z10 gets NOTHING -- see module docstring.
    ("se_gulf", "8"): (f"Jan 15 - Mar 15 {W}", [], [], "extension_direct"),
    ("se_gulf", "9"): (f"Jan 1 - Mar 1 {W}", [], [], "extension_shift_rule_applied"),
    # CA coastal/desert: windows are sourced and rating-independent, so they land now even
    # though these cells' SUITABILITY ratings are contested and deferred to arc 2.
    ("ca_north_coast", "9"): (f"Jan 1 - Mar 31 {W}", ["ucanr_marin_mg"], [], "county_source_direct"),
    ("ca_north_coast", "10"): (f"Jan 1 - Mar 31 {W}", ["ucanr_marin_mg"], [], "county_source_zone_mapped"),
    ("ca_south_coast", "9"): (f"Jan 1 - Feb 28 {W}", ["ucanr_pub7234"], [], "extension_regional_guide"),
    ("ca_south_coast", "10"): (f"Jan 1 - Feb 28 {W}", ["ucanr_pub7234"], [], "extension_regional_guide"),
    ("ca_desert", "9"): (f"Feb 1 - Apr 30 {W}", ["ucanr_pub7234"], [], "extension_regional_guide"),
}

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# establishment_years: the DEVELOPMENT figure, deliberately NOT years_to_first_harvest [2,3].
# Penn State names it outright ("until the plants reach full maturity (five years)"); the
# harvest-duration ramp plateaus at year 5 across Rutgers/UMass/Illinois/USU/MSU. Sourced
# independently -- the two fields describe different things and must not be reconciled.
ESTABLISHMENT_YEARS = 5

YEAR_ONE_SEASONED = (
    "Set one-year-old crowns while they are still dormant, as early as the soil can be worked; "
    "the planting year is about root establishment, not spears. Cut nothing the first year and "
    "nothing the second: the fern is the crown's only way to build the reserves that carry every "
    "later harvest. Let the fern stand all season and until it browns after a hard frost, then cut "
    "it down. Expect a first light cut in year 2 or 3, roughly two weeks, lengthening to four and "
    "then six weeks as the bed matures around year 5."
)
YEAR_ONE_BEGINNER = (
    "Plant the crowns while they are still asleep, as soon as the ground can be worked in spring. "
    "You will not pick any asparagus this year, and that is normal. The ferny growth that comes up "
    "is doing the real work: it feeds the roots underground so the bed can feed you for the next "
    "15 to 20 years. Leave the ferns alone all summer, and cut them back only after frost turns "
    "them brown. Your first small harvest comes a couple of years in."
)


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))

    cat = data.setdefault("source_catalog", {})
    added_src = [k for k in NEW_SOURCES if k not in cat]
    for k, v in NEW_SOURCES.items():
        cat.setdefault(k, v)

    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    crop["establishment_years"] = ESTABLISHMENT_YEARS
    crop["year_one_notes_seasoned"] = YEAR_ONE_SEASONED
    crop["year_one_notes_beginner"] = YEAR_ONE_BEGINNER

    n_plant = n_harv = 0
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            suit = cell.get("suitability")
            cal = cell.get("calendar") or []
            if suit not in ("perennializes", "marginal") or len(cal) != 12:
                continue

            # harvest window string: deterministic from the already-authored calendar tokens.
            hm = [i for i, t in enumerate(cal) if t == "harvest"]
            if hm:
                cell["harvest"] = (f"{MON[hm[0]]} - {MON[hm[-1]]}"
                                   if hm[-1] != hm[0] else MON[hm[0]])
                n_harv += 1

            spec = WINDOWS.get((rk, z))
            if not spec:
                continue                       # se_gulf z10: no T1 window exists
            plant_out, add, remove, method = spec
            cell["plant_out"] = plant_out
            cell["resolution_method"] = method
            n_plant += 1

            srcs = [s for s in (cell.get("sources") or []) if s not in remove]
            for s in add:
                if s not in srcs:
                    srcs.append(s)
            cell["sources"] = srcs

            au = {k: v for k, v in (cell.get("anchoring_urls") or {}).items()
                  if k not in remove}
            for s in add:
                url = (cat.get(s) or {}).get("url")
                if url and s not in au:
                    au[s] = {"url": url, "verified": VERIFIED}
            cell["anchoring_urls"] = au

    print(f"source_catalog additions : {added_src}")
    print(f"establishment_years      : {ESTABLISHMENT_YEARS} (ytfh stays {crop.get('years_to_first_harvest')})")
    print(f"year_one_notes           : seasoned+beginner authored")
    print(f"plant_out authored       : {n_plant} cells")
    print(f"harvest authored         : {n_harv} cells")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
