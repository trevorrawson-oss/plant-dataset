#!/usr/bin/env python3
"""Align asparagus ca_south_coast z11 with z10 at `marginal` -- the last flagged suitability cell.

WHY THIS CHANGES. z11's `unsuitable` rating was justified ONLY by the chill requirement retired in
timing arc 2, and `unsuitable` is the strongest claim the field can make ("do not plant this").
With the mechanism corrected there is nothing behind it:

  - Coastal southern California is MEDITERRANEAN. The dry-down route to dormancy -- UC IPM's
    standard home-garden instruction, "Irrigation is usually stopped in September or October so
    that the plants will go dormant" -- works identically at z11 and z10.
  - z10, the adjacent cell on the SAME coastal strip, is rated `marginal` on exactly that
    reasoning. z10 and z11 differ by roughly 5F of winter minimum and are both essentially
    frost-free; z11 is 365 frost-free days.
  - UC IPM's South Coast crown window covers "San Luis Obispo County, south" with NO zone
    exclusion, so its stated scope already includes this ground.

A cliff from `marginal` to `unsuitable` between adjacent zones, on no evidence, is itself a claim.
`marginal` is the honest answer here: it grows, it needs a gardener-supplied fall dry-down, and no
source publishes a bed lifespan for a frost-free coastal bed. All three are equally true of z10.

WHY THIS DERIVATION IS ALLOWED WHERE ca_desert z10's WAS NOT. Declining to promote ca_desert z10
without sourcing was right because low-desert phenology is genuinely DISTINCT -- a December
harvest opening, a late-November fern chop -- and none of it could be inherited from a neighbour.
Here the cell is extended from an adjacent zone WITHIN THE SAME REGION, under a UC window whose
own stated scope covers the geography. That is the established pattern in this dataset (pnw z9
from z8; se_gulf z9 via UGA's stated shift rule; mid_atlantic z8 via UMD's), and it is recorded
honestly in resolution_method as `adjacent_zone_derived` rather than dressed up as sourced.

THE CAVEAT CARRIED, NOT HIDDEN: no T1 source addresses z11 specifically, so it inherits z10's
uncertainty about bed lifespan. The notes say so plainly.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_ca_south_coast_z11.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"

CALENDAR = ["cold_pause", "harvest", "harvest", "growing", "growing", "growing",
            "growing", "growing", "growing", "growing", "cold_pause", "cold_pause"]
PLANT_OUT = "Jan 1 - Feb 28 (dormant crowns, one-time planting)"
HARVEST = "Feb - Mar"

NOTE_S = (
    "Zone 11 is the warmest, entirely frost-free pocket of the South Coast, so winter never stops "
    "fern growth and the crown's annual rest depends completely on the gardener imposing a fall "
    "dry-down: cut irrigation in September or October, let the ferns brown, then cut them to the "
    "ground. That is the same mechanism the adjacent zone 10 relies on, and UC's South Coast "
    "crown window covers this ground. What is missing is longevity evidence: no source publishes "
    "a bed lifespan for a frost-free coastal planting, so treat this as a bed you actively manage "
    "rather than one that looks after itself."
)
NOTE_B = (
    "Asparagus will grow in this warm coastal pocket, but it needs a rest every year and the "
    "winter here is far too mild to provide one. You have to create it: stop watering in "
    "September or October, let the ferns dry out and turn brown, then cut them down. Skip that "
    "and the spears get thinner every year. We also cannot say how long a bed lasts this far "
    "from frost, so plant it expecting to tend it."
)
NOTES = (
    "In the warmest frost-free pockets of the South Coast spears can start in February; harvest "
    "February into March, then carry the ferns through a long warm season. Nothing about the "
    "winter here will rest the crown for you, so withhold water in September and October and let "
    "the ferns dry down before cutting them back. Set crowns in January or February."
)

FINDING_RESOLVE = "asparagus_ca_south_coast_z11_rating_under_review"

FINDING = {
    "id": "asparagus_ca_south_coast_z11_derived_from_z10",
    "summary": "ca_south_coast z11 re-rated `unsuitable` -> `marginal` on 2026-07-26, aligning it "
               "with the adjacent z10 on the same coastal strip. Its `unsuitable` rating had been "
               "justified ONLY by the chill mechanism retired in timing arc 2; coastal southern "
               "California is Mediterranean, so the dry-down route to dormancy works identically "
               "at both zones, which differ by roughly 5F of winter minimum and are both "
               "essentially frost-free. UC IPM's South Coast crown window covers 'San Luis Obispo "
               "County, south' with no zone exclusion. HONESTLY DERIVED, NOT SOURCED: no T1 "
               "source addresses z11 specifically, so the cell's calendar, plant_out and harvest "
               "are extended from z10 within the same region under a region-scoped source, and "
               "resolution_method records `adjacent_zone_derived` rather than claiming direct "
               "support. The cell inherits z10's real limitation -- no source publishes a bed "
               "lifespan for a frost-free coastal planting -- which is why it lands at `marginal` "
               "and not `perennializes`, and the notes state it. Contrast ca_desert z10, which "
               "was NOT promoted by derivation, because low-desert phenology (December harvest "
               "opening, late-November fern chop) is genuinely distinct and could not be "
               "inherited from a neighbour; it was authored only once sourced.",
    "severity": "low", "blocks_launch": False, "status": "open",
}


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    zones = ((crop.get("regions") or {}).get("ca_south_coast") or {}).get("resolved_by_zone", {})
    cell, z10 = zones.get("11"), zones.get("10")
    if not isinstance(cell, dict) or not isinstance(z10, dict):
        print("ABORT: ca_south_coast z10/z11 not found")
        sys.exit(1)
    if cell.get("suitability") != "unsuitable":
        print(f"ABORT: expected z11 `unsuitable`, found {cell.get('suitability')!r}")
        sys.exit(1)
    # guard the derivation: z11 is only defensible as an extension of a z10 that still says what
    # we think it says.
    if z10.get("suitability") != "marginal" or z10.get("plant_out") != PLANT_OUT:
        print(f"ABORT: z10 drifted -- suitability={z10.get('suitability')!r} "
              f"plant_out={z10.get('plant_out')!r}; re-derive before running")
        sys.exit(1)

    cell["suitability"] = "marginal"
    cell["calendar"] = list(CALENDAR)
    cell["plant_out"] = PLANT_OUT
    cell["harvest"] = HARVEST
    cell["notes"] = NOTES
    cell["suitability_note_seasoned"] = NOTE_S
    cell["suitability_note_beginner"] = NOTE_B
    cell["resolution_method"] = "adjacent_zone_derived"

    srcs = list(cell.get("sources") or [])
    for s in ("uc_ipm", "ucanr_pub7234"):
        if s not in srcs:
            srcs.append(s)
    cell["sources"] = srcs
    cat = data.get("source_catalog", {})
    au = dict(cell.get("anchoring_urls") or {})
    for s in srcs:
        url = (cat.get(s) or {}).get("url")
        if url and s not in au:
            au[s] = {"url": url, "verified": "2026-07-26"}
    cell["anchoring_urls"] = au

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    for f in ofs:
        if isinstance(f, dict) and f.get("id") == FINDING_RESOLVE:
            f["status"] = "resolved"
            f["summary"] += (" RESOLVED 2026-07-26: aligned with z10 at `marginal`, derivation "
                             "recorded as adjacent_zone_derived.")
    if FINDING["id"] not in {f.get("id") for f in ofs if isinstance(f, dict)}:
        ofs.append(FINDING)

    from collections import Counter
    split = Counter(c.get("suitability") for r in crop["regions"].values()
                    for c in (r.get("resolved_by_zone") or {}).values()
                    if isinstance(c, dict) and c.get("suitability"))
    print(f"ca_south_coast z11 : unsuitable -> {cell['suitability']} (adjacent_zone_derived)")
    print(f"  plant_out        : {PLANT_OUT}")
    print(f"  harvest          : {HARVEST}")
    print(f"suitability split  : {dict(split)}")
    print(f"open_findings      : {len(ofs)}")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
