#!/usr/bin/env python3
"""Arc 2 follow-up: bring REGION-level notes into line with the re-rated cells + fixed mechanism.

Caught by a post-promote coherence scan, not by a gate. The cell-level suitability notes were
repaired by promote_asparagus_suitability.py, but `region_notes_seasoned`/`_beginner` are a
SEPARATE consumer-facing layer that still asserted the old chill mechanism AND still described
the OLD ratings -- ca_north_coast, for instance, read "both zones 9 and 10 perennialize only
marginally" after both had been promoted to `perennializes`. That is a direct contradiction
between two strings the same guide renders.

No gate covers this: A36 checks that both registers EXIST, A29 checks they are AUTHORED, but
nothing cross-checks region prose against the per-zone ratings it summarizes. Recorded as an
open_finding so the gap is visible rather than silently fixed.

Every rewrite states the real mechanism -- a reliable annual dormancy window from winter cold OR
a dependable dry-down, plus the 85F fern-development ceiling -- and never mentions chill.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_region_notes.py [--dry-run]
"""
import json
import sys

CANON = "crops_data_final.json"

NOTES = {
    # z9 + z10 both promoted to perennializes on Marin/Sonoma MG evidence.
    "ca_north_coast": (
        "The maritime North Coast is frost-poor, so winter alone will not stop fern growth; the "
        "crown's annual rest comes instead from a deliberate fall dry-down, which is standard UC "
        "practice here (cut irrigation in September or October, let the ferns brown, then cut "
        "them down). Managed that way both zones 9 and 10 carry a lasting bed: the Marin and "
        "Sonoma county programs put a well-kept planting at 15 years or more, with county variety "
        "lists of their own. Harvest from March.",
        "Asparagus does well along California's cool North Coast, as long as you give the plants "
        "their yearly rest yourself. Winters here are too mild to send them to sleep, so stop "
        "watering in September or October and let the ferns dry out and brown before you cut them "
        "back. Do that and a bed can keep producing for 15 years or more."),
    # z9 promoted; z10 stays marginal (no T1 stand life for a frost-free coastal bed); z11 stays
    # unsuitable.
    "ca_south_coast": (
        "On the South Coast the dormant rest has to be imposed rather than waited for: withhold "
        "irrigation in September and October so the ferns dry down. Zone 9 still gets enough "
        "winter cool to back that up and carries a productive bed, and UC publishes a home-garden "
        "crown window for this coast, with production recorded in Orange and Ventura counties. "
        "Zone 10 is essentially frost-free, so it depends wholly on the gardener's dry-down and "
        "no bed lifespan is published for it: workable, but a bed you manage. Frost-free zone 11 "
        "is unsuitable. Harvest from February.",
        "Asparagus is worth growing on the South Coast if you are willing to give it a dry rest "
        "each fall: stop watering in September and October and let the ferns brown off. Zone 9 "
        "takes to that well. In the frost-free stretches of zone 10 it will still crop, but the "
        "bed needs your attention rather than looking after itself, and in zone 11 it is not "
        "worth planting."),
    # z9 promoted (cooler than the z10 valleys UC documents); z10 rating retained pending a proper
    # authoring pass, with the contradiction stated plainly; z11 is effectively vacant ground.
    "ca_desert": (
        "Heat, not winter warmth, is the real limit in the desert: fern development is reduced "
        "above 85°F, so summer shade and steady irrigation decide how well the crown reloads. On "
        "the cooler desert ground of zone 9 frost plus a deliberate fall dry-down gives a clean "
        "rest and the bed persists. Note that UC counts the southern desert valleys among "
        "California's primary asparagus districts, with stands holding 8 to 10 years, so the "
        "current zone 10 rating is under review and its guidance here is incomplete. No "
        "California desert ground actually reaches zone 11.",
        "The desert suits asparagus better than its reputation suggests, especially on the "
        "cooler, higher ground. Give the bed real summer shade and deep water, then stop watering "
        "in fall so the ferns dry down and the plant rests. Asparagus is genuinely farmed in the "
        "hot valleys too, so we are revisiting our advice for the lowest desert."),
    # z10 re-rated to unsuitable on UF/IFAS evidence; z9 stays marginal; the unsupported disease
    # clause is dropped (UGA calls its varieties rust- and Fusarium-resistant).
    "se_gulf": (
        "A frost-anchored perennial across the upper Southeast, where zone 8 gets a real winter "
        "rest and perennializes well; harvest from March in the Piedmont. Toward the Gulf the "
        "winter is often too mild to shut the ferns down completely, so plants keep pushing thin "
        "spears instead of resting, and the summer-wet climate offers no dry-down to substitute. "
        "Zone 9 is marginal on that basis, with a bed that fades after several years. Zone 10 is "
        "unsuitable: UF/IFAS omits asparagus from the Florida vegetable gardening guide entirely.",
        "Asparagus does well in the cooler upper Southeast: plant crowns of a rust-tolerant "
        "variety in the Piedmont or mountains and pick early-spring spears for years. Farther "
        "south the winters stay too warm for the plant to rest properly, and the wet summers do "
        "not help either, so expect a thinner, shorter-lived bed on the coastal plain and skip it "
        "altogether in the warmest parts of Florida."),
    # z10 stays marginal; restate on the dry-down mechanism rather than incomplete cold rest.
    "nevada": (
        "A frost-anchored perennial for the Mojave high desert; harvest from February on the "
        "valley floor and March higher up, then irrigate the summer ferns to reload the crown. "
        "Zone 10's mildest pockets rarely get enough winter cold to stop fern growth on their "
        "own, so the rest there depends on a deliberate fall dry-down, and summer heat above 85°F "
        "slows fern development, which is why those pockets read marginal.",
        "Asparagus grows well across most of the Las Vegas Valley; plant crowns of a heat-"
        "tolerant variety like UC 157, give the bed deep water, and pick very early spring spears "
        "for years. In the warmest low pockets you will need to stop watering in fall so the "
        "plants get a real rest, and shade them through the worst summer heat."),
}

FINDING = {
    "id": "asparagus_region_notes_not_cross_checked_against_cell_ratings",
    "summary": "GATE GAP found 2026-07-26 in timing arc 2, by a manual coherence scan rather than "
               "by any gate. `region_notes_seasoned`/`_beginner` are a SEPARATE consumer-facing "
               "prose layer that summarizes the per-zone suitability ratings, and nothing "
               "cross-checks the two. After arc 2 re-rated cells, the region prose still asserted "
               "the OLD ratings and the OLD (unsourced) chill mechanism -- ca_north_coast read "
               "'both zones 9 and 10 perennialize only marginally' after both had been promoted to "
               "`perennializes`, a direct contradiction between two strings the same guide "
               "renders. A36 checks both registers EXIST and A29 checks they are AUTHORED, but "
               "neither reads what they SAY. Repaired by hand for asparagus across 5 regions. "
               "CANDIDATE GATE: assert that region prose naming a zone and a suitability verb "
               "agrees with that zone's cell rating; needs a flood check first, since region prose "
               "is free text and phrasing varies widely across 128 crops.",
    "severity": "medium", "blocks_launch": False, "status": "open",
}


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    n = 0
    for rk, (seasoned, beginner) in NOTES.items():
        r = (crop.get("regions") or {}).get(rk)
        if not isinstance(r, dict):
            print(f"ABORT: region {rk} not found")
            sys.exit(1)
        r["region_notes_seasoned"] = seasoned
        r["region_notes_beginner"] = beginner
        n += 1

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    if FINDING["id"] not in {f.get("id") for f in ofs if isinstance(f, dict)}:
        ofs.append(FINDING)

    print(f"region note pairs rewritten: {n}")
    print(f"open_findings: {len(ofs)}")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
