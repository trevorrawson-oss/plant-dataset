#!/usr/bin/env python3
"""Asparagus timing ARC 2: repair the suitability MECHANISM, then the ratings it distorted.

THE FINDING. Every marginal/unsuitable asparagus cell justified its rating on a CHILL
requirement -- "low-chill", "sustained cold dormant rest", "shallow winter rest" -- cited to
uc_ipm. That source says the opposite. NO T1 source anywhere states a chill-hour requirement for
asparagus (checked across ~15). What uc_ipm actually says, on a home-garden page:

  "If drought or cold weather do not stop vegetative fern growth, shoots will become spindly and
   less vigorous each year."
  "Irrigation is usually stopped in September or October so that the plants will go dormant."

UF/IFAS independently: "Dormancy is usually brought about by cold weather or drought." So
withholding irrigation is UC's standard instruction TO HOME GARDENERS, not a commercial trick.

THE CORRECT MECHANISM, which this pass writes into every affected note:
  1. asparagus needs a reliable ANNUAL DORMANCY WINDOW, delivered by winter cold OR by a
     dependable dry-down; and
  2. fern development is reduced above 85F (UC ANR Pub 7234: "Root and fern development are
     reduced at temperatures below 55F or above 85F").
This is why Mediterranean California works (dependable dry summer) and the summer-WET Gulf and
tropics do not -- UF/IFAS names it "warm AND wet". The old chill framing got the conclusion right
for the tropics by luck and wrong for California by mechanism.

RATING CHANGES (5), each on corrected reasoning:
  ca_north_coast z9, z10   marginal -> perennializes   Marin + Sonoma MG (ucanr.edu) both publish
                                                       15-year bed lifespans, county variety
                                                       lists, and no warm-winter warning at all.
  ca_south_coast z9        marginal -> perennializes   UC IPM publishes a home-garden South Coast
                                                       crown window; Pub 7234 records production
                                                       in Orange and Ventura counties.
  ca_desert z9             marginal -> perennializes   z9 desert (Barstow/Blythe) is COOLER-
                                                       wintered than the z10 valleys UC documents
                                                       as a primary district with 8-10 yr stands.
  se_gulf z10              marginal -> unsuitable      asparagus occurs ZERO times in the UF/IFAS
                                                       Florida vegetable guide (statewide AND
                                                       South Florida editions).

DELIBERATELY LEFT ALONE, with reasoning repaired:
  ca_south_coast z10  stays marginal. The upgrade case COLLAPSED under scrutiny: the "10-15 years"
      claim traces to a .org volunteer-association blog Q&A reworded from statewide boilerplate,
      and San Diego County's actual UCCE planting table omits asparagus entirely. No T1 states a
      stand life for a frost-free coastal bed.
  se_gulf z9          stays marginal (well supported by Mississippi State + UF HS546). Its
      unsupported "heavier Fusarium and rust pressure" clause is DROPPED -- no T1 backs disease as
      a Gulf exclusion, and UGA calls its varieties resistant to rust and Fusarium.
  ca_desert z11       stays unsuitable. Near-vacuous: no California desert ground is z11 (Death
      Valley is 9a). Rating unfalsified, but its note was wrong twice -- it called z11 "the low
      desert" (that is z10) and demanded "sustained cold rest".

NOT CHANGED, ESCALATED INSTEAD -- ca_desert z10. Its `unsuitable` rating is flatly contradicted:
this is Imperial/Coachella, which UC ANR Pub 7234 names one of California's three PRIMARY
asparagus districts and for which UC IPM publishes a home-garden crown window. But promoting it
needs a real 12-token calendar and a sourced crown window built for low-desert phenology (fern
chop late Nov, harvest opening around December), and inventing that calendar to clear a rating is
exactly the fabrication this dataset refuses. Its note is corrected to stop asserting a false
mechanism, and a HIGH-priority open_finding queues the cell for a proper authoring pass.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_suitability.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"
GROWING12 = ["growing"] * 12

# (region, zone) -> new suitability, or None to keep the current rating.
RERATE = {
    ("ca_north_coast", "9"): "perennializes",
    ("ca_north_coast", "10"): "perennializes",
    ("ca_south_coast", "9"): "perennializes",
    ("ca_desert", "9"): "perennializes",
    ("se_gulf", "10"): "unsuitable",
}

# Cells promoted to perennializes: suitability_note_* is dropped (the gate requires it only for
# marginal/unsuitable, and a "why this is marginal" note on a suitable cell is incoherent). The
# cell `notes` prose is rewritten to carry the real guidance instead.
PROMOTED_NOTES = {
    ("ca_north_coast", "9"):
        "On the cool north-coast strip spears emerge in March; harvest March into April, then "
        "carry the ferns through a mild summer. Winter frost is scarce here, so give the crown "
        "its rest from the dry side: stop watering in September or October and let the ferns dry "
        "down and brown before you cut them off. Marin and Sonoma county programs both put a "
        "well-kept bed at 15 years or more.",
    ("ca_north_coast", "10"):
        "In the nearly frost-free bayside pockets spears come in March; harvest March into April, "
        "then run the ferns through a cool summer. With little winter cold to stop growth, the "
        "annual rest has to come from a deliberate fall dry-down: cut off irrigation in September "
        "or October, let the ferns brown, then cut them to the ground. Handled that way the bed "
        "keeps producing for many years.",
    ("ca_south_coast", "9"):
        "On the mild South Coast spears push up by February; harvest February into March, then "
        "carry the ferns through a long warm season. Winters are too gentle to shut the plant "
        "down on their own, so withhold water in September and October and let the ferns dry "
        "down: that dry rest is what recharges the crown for the next spring.",
    ("ca_desert", "9"):
        "On the cooler desert ground spears emerge in February; harvest February into March, then "
        "push the ferns through a very hot summer on steady irrigation. Winter frost plus a "
        "deliberate fall dry-down gives the crown a clean rest. Summer heat above 85°F slows fern "
        "growth, so shade and water matter here, but the bed still pays: UC counts the southern "
        "desert valleys among California's main asparagus districts, with stands holding 8 to 10 "
        "years.",
}

# Rewritten suitability notes for cells that stay marginal/unsuitable. Every one states the real
# mechanism (dormancy window availability, heat ceiling) and never mentions chill.
NOTES = {
    ("ca_south_coast", "10"): (
        "Zone 10 on the South Coast is essentially frost-free, so winter never stops fern growth "
        "on its own and the crown's annual rest depends entirely on the gardener imposing a fall "
        "dry-down. Done faithfully the bed will cycle and crop, but UC publishes no bed lifespan "
        "for this frost-free coastal strip, so treat it as a bed you actively manage rather than "
        "one that looks after itself.",
        "Asparagus can grow here, but it needs a rest every year and your winter is too warm to "
        "give it one. You have to create the rest yourself: stop watering in September or "
        "October, let the ferns dry out and turn brown, then cut them down. If you skip that "
        "step the plant never rests, and the spears get thinner every year."),
    ("ca_desert", "10"): (
        "RATING UNDER REVIEW. This is the Imperial and Coachella valley floor, which UC ANR "
        "publication 7234 names one of California's three primary asparagus districts and for "
        "which UC IPM publishes a home-garden crown-planting window, with commercial stands "
        "holding 8 to 10 years. The previous `unsuitable` call rested on a chill requirement no "
        "source states. The real limits here are heat, with fern development reduced above 85°F, "
        "and a rest period that must come from a managed dry-down rather than winter cold. The "
        "rating is retained only pending a proper cell authoring pass, because promoting it "
        "honestly requires a low-desert calendar this crop does not yet carry.",
        "Asparagus really is grown in this desert, and commercially at that, so do not let the "
        "current rating put you off entirely. What it needs here is heat protection through the "
        "summer and a deliberate dry rest in fall: stop watering, let the ferns brown, cut them "
        "back. We are still working out the right planting calendar for this corner, so treat "
        "our timing guidance as incomplete for now."),
    ("ca_desert", "11"): (
        "No California desert ground actually reaches zone 11 (Death Valley resolves to 9a), so "
        "this cell is effectively vacant rather than a real growing situation. Where a climate is "
        "both frost-free and extremely hot, asparagus gets neither a dependable cold rest nor a "
        "workable fern season, since development is reduced above 85°F, and the crown never banks "
        "its reserves. Cooler desert ground a zone or two up is the better bet.",
        "Skip asparagus at this end of the desert. The plant needs a real rest each year, from "
        "either winter cold or a genuine dry-down, and the hottest frost-free pockets give it "
        "neither on a dependable schedule. Try it on cooler desert ground instead."),
    ("se_gulf", "9"): (
        "The Gulf and lower coastal-plain winter is often too mild to shut the ferns down "
        "completely, so plants keep pushing a few thin spears instead of resting and the crown "
        "never fully recharges. The summer-wet climate closes off the other route to dormancy, "
        "since there is no dependable dry-down to substitute for winter cold. Expect lighter "
        "cuttings and a bed that fades after several years rather than the decades it manages "
        "farther north.",
        "Asparagus will grow here, but do not expect it to last. Your winters usually stay warm "
        "enough that the plant never fully goes to sleep, so it keeps sending up a few thin "
        "spears and slowly wears itself out. You will get some harvests, just lighter ones, and "
        "the bed will fade after a few years."),
    ("se_gulf", "10"): (
        "Asparagus is not a crop for peninsular Florida and the lower Gulf: UF/IFAS omits it "
        "entirely from the Florida vegetable gardening guide, in both the statewide and South "
        "Florida editions, and county Extension states plainly that it cannot be grown "
        "successfully here. The mechanism is warm AND wet: the winter is too mild to force "
        "dormancy, and summer rainfall removes the dry-down that lets mild-winter California "
        "substitute for winter cold. Without either route to a rest, the crown declines.",
        "Skip asparagus here. Florida's Extension service does not even list it among the "
        "vegetables to grow in this part of the state. It needs a real dormant rest each year, "
        "and between the warm winters and the wet summers there is no time of year that gives it "
        "one. Put the bed space into something that thrives here instead."),
    ("nevada", "10"): (
        "Zone 10 in the Las Vegas Valley is the warm edge of asparagus range: winters are often "
        "too mild to stop fern growth on their own, so the annual rest depends on a deliberate "
        "fall dry-down. The desert does at least supply that reliably, which is why this reads "
        "marginal rather than unsuitable, but summer heat above 85°F also slows fern development, "
        "so the crown recharges less each year than it would farther north.",
        "You can grow asparagus here, but it needs help. Stop watering in September or October so "
        "the ferns dry down and the plant gets its rest, and shade it through the worst of the "
        "summer heat. Expect a lighter, shorter-lived bed than a cold-winter garden would get."),
}

# Roster-wide mechanism repair for the remaining unsuitable cells: strip the chill framing, keep
# the (correct) conclusion. These climates fail BOTH routes to dormancy.
BOTH_ROUTES_FAIL = {
    ("ca_south_coast", "11"), ("low_desert_az", "9"), ("low_desert_az", "10"),
    ("rgv", "9"), ("rgv", "10"), ("fl_peninsula", "10"), ("fl_peninsula", "11"),
    ("hawaii_tropical", "10"), ("hawaii_tropical", "11"),
    ("hawaii_tropical", "12"), ("hawaii_tropical", "13"),
}
BOTH_S = ("Asparagus needs a dependable annual rest, reached either through winter cold or "
          "through a genuine dry-down, and this climate supplies neither on a reliable schedule: "
          "the winter never stops fern growth, and there is no dry season long enough to "
          "substitute. Growth runs more or less continuously, the crown never banks its reserves, "
          "and spears come thin and weak before the bed declines outright.")
BOTH_B = ("Skip asparagus here. It has to go dormant and rest for part of every year, and this "
          "climate never gives it that break, so it just keeps growing weakly until it wears "
          "itself out. Put the space into a crop suited to your winters.")

FINDING = {
    "id": "asparagus_ca_desert_z10_rating_contradicted_needs_authoring",
    "summary": "HIGH-PRIORITY CELL, raised 2026-07-26 in timing arc 2 and deliberately NOT "
               "auto-resolved: ca_desert z10 is rated `unsuitable`, but this is the Imperial and "
               "Coachella valley floor, which UC ANR Pub 7234 names one of California's three "
               "PRIMARY asparagus production districts ('the southern desert valleys (Imperial "
               "and Riverside Counties)') and for which UC IPM publishes a home-garden crown "
               "window, with stands holding 8 to 10 years. The `unsuitable` call rested on a "
               "chill requirement no T1 source states. It was NOT flipped in this pass because "
               "promotion requires a real 12-token calendar and a sourced crown window built for "
               "low-desert phenology (fern chop late November, harvest opening near December, "
               "harvest running to early April) -- inventing that calendar to clear a rating "
               "would be exactly the fabrication the T1-or-it-doesn't-ship bar exists to "
               "prevent. Its note now states the real limits (85F fern ceiling, managed dry-down "
               "dormancy) instead of the false one. QUEUED: author the low-desert cell properly, "
               "then re-rate. Also note the region's zone labels do not match USDA 2023 ground "
               "truth -- Antelope Valley and Victorville resolve to z8, below this region's "
               "span, and no California desert ground reaches z11 (Death Valley is 9a), so "
               "ca_desert z11 is an effectively vacant cell.",
    "severity": "medium", "blocks_launch": False, "status": "open",
}


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    n_rate = n_note = n_promo = 0
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            key = (rk, z)

            if key in RERATE:
                new = RERATE[key]
                cell["suitability"] = new
                n_rate += 1
                if new == "perennializes":
                    cell.pop("suitability_note_seasoned", None)
                    cell.pop("suitability_note_beginner", None)
                    cell["notes"] = PROMOTED_NOTES[key]
                    n_promo += 1
                elif new == "unsuitable":
                    # honesty floor: an unsuitable cell shows the honest all-growing placeholder
                    # and carries no planting window (and is A47-exempt by design).
                    cell["calendar"] = list(GROWING12)
                    cell.pop("plant_out", None)
                    cell.pop("harvest", None)

            if key in NOTES:
                s, b = NOTES[key]
                cell["suitability_note_seasoned"], cell["suitability_note_beginner"] = s, b
                n_note += 1
            elif key in BOTH_ROUTES_FAIL:
                cell["suitability_note_seasoned"] = BOTH_S
                cell["suitability_note_beginner"] = BOTH_B
                n_note += 1

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    if FINDING["id"] not in {f.get("id") for f in ofs if isinstance(f, dict)}:
        ofs.append(FINDING)

    from collections import Counter
    split = Counter(c.get("suitability") for r in crop["regions"].values()
                    for c in (r.get("resolved_by_zone") or {}).values()
                    if isinstance(c, dict) and c.get("suitability"))
    print(f"ratings changed   : {n_rate}  (promoted to perennializes: {n_promo})")
    print(f"notes rewritten   : {n_note}")
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
