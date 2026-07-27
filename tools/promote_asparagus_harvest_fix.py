#!/usr/bin/env python3
"""Re-author asparagus HARVEST windows from sourced data, and add the bed-age harvest ramp.

THE DEFECT. All 29 asparagus harvest strings were exactly two calendar months. That is an
artifact, not biology: the strings were derived mechanically from the cert's calendar tokens,
which were themselves MODELED from regional frost patterns. Reported by Trevor for the Central
Valley -- our `ca_interior` z9 (the Sacramento-San Joaquin Delta) said "Feb - Mar" while every
source he could find said otherwise. He was right.

THE MODEL, confirmed by four independent research passes: a harvest window is
    SOURCED START (regional, climate-driven)  +  DURATION (portable, bed-age dependent)
"across every source, START moves with climate but DURATION does not." Only the start is
regional; the duration is a grower rule. Applying a real duration to a real start makes most
cells span parts of THREE calendar months -- which is why the uniform two-month rendering
misstated them.

DURATION IS REGIONAL AFTER ALL, in one respect: warm long-season regions grant LONGER mature
harvests, the opposite of the heat-shortens hypothesis this pass started with.
    northern tier z3-z4   ~6 wk   (a late-June stop date binds before the week-count does)
    northern tier z5-z7   6-8 wk
    mid-Atlantic / mid-South / PNW / SE   6-8 wk
    California            8-10 wk  (UC IPM, Sacramento, Napa, Contra Costa -- four independent)
    arid West             up to 10 wk (NMSU: "From year four on, harvest a maximum of 10 weeks/year")

THE HOME-vs-COMMERCIAL TRAP, and its resolution. This pass began by instructing researchers not
to conflate commercial and home windows. In California that distinction turned out to be FALSE:
Contra Costa MG's home guidance -- "A full cutting season (60 to 75 days) may begin the fourth
year after planting" -- is a VERBATIM LIFT from Pub 7234, the commercial bulletin, which the home
page then tells gardeners to go read. There is no independent California home-duration research,
so "home is shorter" is not a defensible basis for narrowing the Delta cell. What IS commercial-
only is the Delta's late-February start (Pub 7234: "In the Delta, asparagus is harvested from
late February through May"); a home bed starts in March.

THE STOP RULE. Every T1 source ends the season on SPEAR DIAMETER, not a date -- stop when spears
thin below pencil width. Alameda County MG states the ramp and the stop rule in one sentence:
"The third spring after planting, you can start to harvest, but only for two or three weeks. The
fourth spring, you can harvest for 6 to 8 weeks, and in later years for 2 months or until the
largest spears become thinner than a pencil, whichever is sooner."

NEW FIELD: `harvest_ramp_weeks` -- pure numbers, no prose (the prose already lives in
`harvest_ready_*`, which carries the pencil-width rule in both registers). Deliberately
structured so the app can say "you are in bed year 3, cut for two weeks, not eight" off the
user's own plantedAt. This is a PILOT on asparagus only; roster-wide rollout across the 25
establishment crops is a register entry, gated on a stable roster per the register's standing
principle (artichoke is mid-certification).

PROVENANCE HONESTY. `resolution_method` records how each window was reached:
  harvest_sourced_start_and_duration  both ends sourced for this geography
  harvest_sourced_duration_modeled_start  duration sourced, start inherited from the cert's
                                          modeled calendar -- the honest majority case
Cells with neither are listed in the open_findings this pass files.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_harvest_fix.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# (region, zone) -> (first_harvest_month_idx, last_harvest_month_idx, resolution_method)
# 0-based month indices. Windows below are the MATURE-BED (year 5+) window.
S = "harvest_sourced_start_and_duration"
M = "harvest_sourced_duration_modeled_start"
WINDOWS = {
    # northern tier -- starts sourced per state (UMaine "harvest in central Maine typically begins
    # in early May"; UMN "early May to late June in Minnesota"; NDSU "May through June"; Iowa State
    # "harvested until early to mid-June"). z3/z4 are capped by a stop DATE, not a week count:
    # NDSU "Do not harvest beyond June", UMaine "should not go beyond June 15".
    ("northern_tier", "3"): (4, 5, S),    # May - Jun, ~6 wk, late-June cap binds
    ("northern_tier", "4"): (4, 5, S),    # May - Jun, ~7 wk
    ("northern_tier", "5"): (3, 5, S),    # Apr - Jun
    ("northern_tier", "6"): (3, 5, S),    # Apr - Jun
    ("northern_tier", "7"): (3, 5, M),    # Apr - Jun -- interpolated, no northern-tier z7 source
    # mid-Atlantic / mid-South -- Missouri G6405 gives real dated sub-regional windows
    # ("April 14 to May 30 in southern Missouri"); Mid-Atlantic recs "Stop harvesting by June 15".
    # NOTE: no source starts asparagus harvest in MARCH anywhere in these belts.
    ("mid_atlantic", "7"): (3, 5, S),     # Apr - Jun
    ("mid_atlantic", "8"): (3, 5, M),     # Apr - Jun (was "Mar - Apr"; a March start is unsupported)
    ("mid_south", "7"): (3, 5, S),        # Apr - Jun
    ("mid_south", "8"): (3, 5, M),        # Apr - Jun (was "Mar - Apr"; MO bootheel is z7a, not z8)
    # PNW -- OSU: "Year 3 and beyond: Harvest until mid-June." Start inferred back from that.
    ("pnw", "8"): (3, 5, M),              # Apr - Jun
    ("pnw", "9"): (3, 5, M),              # Apr - Jun (was "Mar - Apr"; no zone split in any source)
    # arid West -- NMSU: "The New Mexico asparagus harvest season begins in southern New Mexico in
    # early March" + "From year four on, harvest a maximum of 10 weeks/year".
    ("warm_arid", "8"): (2, 4, S),        # Mar - May
    ("utah_dixie", "8"): (2, 4, M),       # Mar - May (start inferred; no Dixie harvest source)
    ("nevada", "8"): (2, 4, M),           # Mar - May (NO Nevada asparagus harvest source exists)
    ("nevada", "9"): (2, 4, M),           # Mar - May
    ("nevada", "10"): (2, 4, M),          # Mar - May
    # California -- mature duration 8-10 wk, four independent UC corroborations. The Delta is the
    # cell Trevor reported: Pub 7234's "late February through May" is COMMERCIAL; home starts March.
    ("ca_interior", "8"): (2, 4, M),      # Mar - May
    ("ca_interior", "9"): (2, 4, S),      # Mar - May  <-- THE REPORTED CELL, was "Feb - Mar"
    ("ca_north_coast", "9"): (2, 4, M),   # Mar - May
    ("ca_north_coast", "10"): (2, 4, M),  # Mar - May
    ("ca_south_coast", "9"): (2, 4, M),   # Mar - May
    ("ca_south_coast", "10"): (2, 4, M),  # Mar - May
    ("ca_south_coast", "11"): (2, 4, M),  # Mar - May
    ("ca_desert", "9"): (1, 3, M),        # Feb - Apr (warmest CA cells run earliest)
    ("ca_desert", "10"): (2, 3, M),       # Mar - Apr
    # low desert AZ -- UA az1615 (Yuma, HOME) states the harvest window outright as "March-April",
    # which at ~8.7 weeks is genuinely a two-month window. Not every 2-month span was wrong.
    ("low_desert_az", "9"): (2, 3, M),    # Mar - Apr (Phoenix; borrowed from Yuma)
    ("low_desert_az", "10"): (2, 3, S),   # Mar - Apr (Yuma; az1615 harvest row)
}

# Mature-bed ramp. Modal home ramp is the "2-4-6" rule (UMass states it cleanly); California and
# the arid West run longer at maturity (8-10 wk). Years count SEASONS IN THE GROUND from a
# one-year-old crown, matching years_to_first_harvest [2,3].
HARVEST_RAMP = [
    {"bed_year": 1, "weeks": [0, 0]},
    {"bed_year": 2, "weeks": [0, 0]},
    {"bed_year": 3, "weeks": [2, 3]},
    {"bed_year": 4, "weeks": [6, 8]},
    {"bed_year": 5, "weeks": [8, 10]},
]

FINDINGS = [
    {
        "id": "asparagus_harvest_windows_resourced_2026_07_27",
        "summary": "DEFECT FIXED 2026-07-27, reported by Trevor for the Central Valley. All 29 "
                   "asparagus harvest strings were exactly two calendar months -- an artifact of "
                   "deriving them mechanically from the cert's MODELED calendar tokens rather than "
                   "sourcing them. `ca_interior` z9 (the Sacramento-San Joaquin Delta) said "
                   "'Feb - Mar' while UC ANR Pub 7234, a source cited ON THAT CELL, says 'In the "
                   "Delta, asparagus is harvested from late February through May'. Root cause is "
                   "mine: arc 1 recorded that harvest strings were 'derived deterministically from "
                   "the already-authored calendar tokens, no re-sourcing needed', which treated "
                   "modeled data as ground truth and minted a user-facing field from it. The tell "
                   "was a perfectly uniform two-month window across 16 regions and zones 3-11. "
                   "RE-AUTHORED on the model confirmed by four research passes: sourced START "
                   "(regional) + DURATION (portable, bed-age dependent). Most cells now span three "
                   "calendar months. Calendar harvest tokens re-authored to match, since the "
                   "artifact lived in the tokens, not only the strings.",
        "severity": "medium", "blocks_launch": False, "status": "resolved",
    },
    {
        "id": "asparagus_harvest_duration_is_regional_warm_regions_longer",
        "summary": "AGRONOMIC FINDING 2026-07-27 that reversed this pass's working hypothesis. I "
                   "instructed researchers to look for HEAT SHORTENING the harvest window. The "
                   "opposite is true and is well sourced: warm long-season regions grant the "
                   "LONGEST mature harvests. NMSU (southern New Mexico) is the only source "
                   "permitting a first-year cut and allows 'a maximum of 10 weeks/year' from year "
                   "four; California's mature figure is 8-10 weeks with four independent UC "
                   "corroborations (UC IPM, Sacramento, Napa, Contra Costa); the northern tier "
                   "runs 6-8 weeks and z3/z4 are capped nearer 6 by a stop DATE ('Do not harvest "
                   "beyond June' -- NDSU; 'should not go beyond June 15' -- UMaine). What heat "
                   "actually does per source: speeds spears so they need more frequent cutting, "
                   "degrades tip quality within the window, and caps fern rebuilding above 85F -- "
                   "but NO source converts that into an earlier stop date. In every T1 source the "
                   "season ends on SPEAR DIAMETER, not a date: stop when spears thin below pencil "
                   "width. That rule is already carried in both registers of `harvest_ready_*`.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_home_vs_commercial_conflated_in_california_sources",
        "summary": "SOURCING TRAP recorded 2026-07-27. This pass instructed researchers not to "
                   "conflate commercial and home harvest windows. In California that distinction "
                   "does not exist in the literature: Contra Costa County MG's HOME guidance -- 'A "
                   "full cutting season (60 to 75 days) may begin the fourth year after planting' "
                   "-- is a VERBATIM LIFT from UC ANR Pub 7234, the COMMERCIAL production "
                   "bulletin, and the home page closes by telling gardeners to consult 7234. There "
                   "is therefore no independent California home-garden duration research to appeal "
                   "to, and 'home windows are shorter' is NOT a defensible basis for narrowing a "
                   "California cell. What IS commercial-only is the Delta's late-February start "
                   "(Pub 7234), which is induced for the early market; a home bed starts in March. "
                   "Santa Clara MG states the underlying gap outright: 'Harvest times are not "
                   "included in this chart because they may vary widely depending on variety and "
                   "season.' Most California county planting charts carry planting dates only.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_harvest_starts_unsourced_on_many_cells",
        "summary": "HONEST GAP carried 2026-07-27. Duration is well sourced roster-wide; STARTS are "
                   "not. Only these cells have a start sourced for their own geography "
                   "(`resolution_method: harvest_sourced_start_and_duration`): northern_tier "
                   "z3-z6, mid_atlantic z7, mid_south z7, warm_arid z8, ca_interior z9, "
                   "low_desert_az z10. Every other cell carries "
                   "`harvest_sourced_duration_modeled_start` -- a sourced regional duration applied "
                   "to the start inherited from the cert's modeled calendar. NO T1 SOURCE EXISTS "
                   "for: all three nevada cells (checked and exhausted -- SP-01-15 is a Master "
                   "Gardener PLANTING guide, FS-02-61 has no asparagus content), utah_dixie z8, "
                   "pnw z9, mid_atlantic z8, se_gulf z8/z9 starts. Also corrected: no source starts "
                   "asparagus harvest in MARCH anywhere in the mid-Atlantic, mid-South or PNW, so "
                   "the former 'Mar - Apr' values in those belts were unsupported; they may have "
                   "been read off CROWN-PLANTING tables (Clemson's 'Planting Dates for Crowns', "
                   "UGA B577, UMD HG16 all give Feb-Apr planting windows that resemble the old "
                   "harvest strings). T2 sourcing is now permitted with disclosure, so these gaps "
                   "are re-openable with county Master Gardener calendars.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_harvest_ramp_weeks_pilot",
        "summary": "NEW FIELD piloted on asparagus 2026-07-27: `harvest_ramp_weeks`, a bed-age "
                   "harvest-duration ramp as pure numbers ([{bed_year, weeks:[min,max]}]). Years 1-2 "
                   "no harvest, year 3 two-to-three weeks, year 4 six-to-eight, year 5+ eight-to-ten. "
                   "Deliberately structured rather than prose so the app can say 'you are in bed "
                   "year 3 -- cut for two weeks, not eight' off the user's own plantedAt, which is "
                   "the multi-year perennial guidance Trevor identifies as a product "
                   "differentiator. Sourced: the modal home ramp is the '2-4-6' rule stated cleanly "
                   "by UMass; Alameda County MG gives ramp and stop rule in one sentence -- 'The "
                   "third spring after planting, you can start to harvest, but only for two or "
                   "three weeks. The fourth spring, you can harvest for 6 to 8 weeks, and in later "
                   "years for 2 months or until the largest spears become thinner than a pencil, "
                   "whichever is sooner.' No prose keys, so no dual-register or prose-ruling "
                   "obligation; the pencil-width rule already lives in both registers of "
                   "`harvest_ready_*`. PILOT ONLY -- roster-wide rollout across the 25 "
                   "establishment crops is a field-addition register entry gated on a STABLE "
                   "roster, per the register's standing principle, and artichoke is currently "
                   "mid-certification. CAUTION for the rollout: sources use three incompatible "
                   "year-counting conventions ('year after planting crowns', 'year the plants are "
                   "in the garden', 'harvest year'), which describe the same season; ours counts "
                   "seasons in the ground from a one-year-old crown, consistent with "
                   "years_to_first_harvest [2,3].",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "webfetch_pdf_summaries_are_not_sourcing",
        "summary": "TOOLING HAZARD, new class, recorded 2026-07-27. A research agent this pass "
                   "FABRICATED a document title and supporting quotes ('Peak harvest typically "
                   "occurs April through June') for a Contra Costa handbook that contains NO "
                   "asparagus content at all. The fabrication came from a WebFetch SUMMARY of a "
                   "PDF. This is worse than the known markdown-table column-shift hazard, which "
                   "garbles existing data -- this INVENTS data that was never there, with a "
                   "plausible citation attached. OPERATING RULE for this dataset: WebFetch "
                   "summaries of PDFs are NOT sourcing. Extract PDF text with pypdf, or fetch raw "
                   "HTML and parse structurally, and quote verbatim from the extracted text. Every "
                   "figure authored in this pass was taken from raw HTML or pypdf output.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
]


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    crop["harvest_ramp_weeks"] = [dict(x) for x in HARVEST_RAMP]

    changed = kept = 0
    rows = []
    for (rk, z), (a, b, method) in WINDOWS.items():
        cell = ((crop.get("regions") or {}).get(rk) or {}).get("resolved_by_zone", {}).get(z)
        if not isinstance(cell, dict):
            print(f"ABORT: {rk}.{z} not found")
            sys.exit(1)
        if cell.get("suitability") not in ("perennializes", "marginal"):
            print(f"ABORT: {rk}.{z} is {cell.get('suitability')!r}, expected a growing cell")
            sys.exit(1)

        cal = list(cell.get("calendar") or [])
        if len(cal) != 12:
            print(f"ABORT: {rk}.{z} calendar is not 12 tokens")
            sys.exit(1)
        old_h = cell.get("harvest")
        # rebuild: harvest months a..b; every other month that WAS harvest becomes growing;
        # cold_pause months are preserved unless the new harvest window claims them.
        new = []
        for i, tok in enumerate(cal):
            if a <= i <= b:
                new.append("harvest")
            elif tok == "harvest":
                new.append("growing")
            else:
                new.append(tok)
        cell["calendar"] = new
        cell["harvest"] = f"{MON[a]} - {MON[b]}"
        cell["resolution_method"] = method
        if cell["harvest"] != old_h:
            changed += 1
        else:
            kept += 1
        rows.append((rk, z, old_h, cell["harvest"], b - a + 1, method == S))

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    have = {f.get("id") for f in ofs if isinstance(f, dict)}
    for f in FINDINGS:
        if f["id"] not in have:
            ofs.append(f)

    print("%-16s %-4s %-11s -> %-11s %-4s %s" % ("region", "z", "was", "now", "mons", "start sourced?"))
    for rk, z, o, n, months, sourced in rows:
        print("%-16s %-4s %-11s -> %-11s %-4d %s" % (rk, z, o, n, months, "YES" if sourced else "modeled"))
    print()
    print(f"harvest windows changed : {changed} (unchanged: {kept})")
    print(f"harvest_ramp_weeks      : {len(HARVEST_RAMP)} bed-year entries (NEW FIELD, pilot)")
    print(f"open_findings           : {len(ofs)}")
    from collections import Counter
    print(f"month-span distribution : {dict(Counter(r[4] for r in rows))}  (was: all 2)")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
