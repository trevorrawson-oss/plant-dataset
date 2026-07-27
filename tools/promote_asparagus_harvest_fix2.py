#!/usr/bin/env python3
"""Corrective pass on the asparagus harvest fix: provenance split, the 2 missed cells, prose drift.

Three defects in my own preceding pass (tools/promote_asparagus_harvest_fix.py), all caught by a
post-promote coherence scan rather than by a gate.

1. PROVENANCE DESTROYED. That pass overwrote `resolution_method` with harvest-specific values,
   erasing the plant_out/calendar provenance on 27 cells. `resolution_method` answers "how was
   this cell's PLANTING window reached"; harvest provenance is an ORTHOGONAL axis. Collapsing two
   independent axes into one string loses the cross-product -- exactly the design error I had just
   advised the artichoke session against for source tier. FIX: restore `resolution_method` from
   git HEAD and carry harvest provenance in its own `harvest_resolution_method`.

2. TWO CELLS MISSED. se_gulf z8 and z9 were absent from the window table (27 rows for 29 cells),
   so they kept the two-month artifact AND kept a `resolution_method` describing their planting
   derivation while every neighbour had been switched. Authored here on the same model. Neither
   has a sourced start -- no T1 source gives an asparagus harvest start for the Southeast -- so
   both are `harvest_sourced_duration_modeled_start`, and se_gulf z8's start stays March (its
   existing note and the region's Piedmont framing agree) with duration extended to the sourced
   6-8 weeks.

3. PROSE DRIFT. Changing 22 windows left 9 cell notes and 6 region-note pairs describing the OLD
   windows -- "harvest February into March" on a cell now reading Mar-May. This is the same defect
   class documented in docs/2026-07-26-post-asparagus-hardening-kickoff.md item 1: prose and data
   are separate layers and no gate compares them. I created a fresh instance of it within an hour
   of writing that document up, which is the strongest argument yet for building the gate.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_harvest_fix2.py [--dry-run]
"""
import json
import subprocess
import sys

CANON = "crops_data_final.json"

# se_gulf: the two cells missed by the preceding pass. (first_month_idx, last_month_idx)
MISSED = {
    ("se_gulf", "8"): (2, 4),   # Mar - May: start unsourced but March is coherent with the cell's
                                # own "spears emerge in March"; duration extended to 6-8 wk sourced
    ("se_gulf", "9"): (2, 4),   # Mar - May: start unsourced; no T1 gives a Southeast harvest start
}
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Cell notes rewritten to match the new windows. Only cells whose prose named a month now outside
# the window; the low-desert cells' February references are CROWN-PLANTING months and are correct.
CELL_NOTES = {
    ("mid_atlantic", "8"): "On the warmer Coastal Plain spears break ground in April; harvest April into June for six to eight weeks on an established bed, then let the ferns develop through the long summer and stand until they brown after frost.",
    ("mid_south", "8"): "In the warm Delta lowlands spears push up in April; harvest April into early June, then let the ferns develop through the hot summer to recharge the crown. Snap spears at ground level rather than cutting below the soil to limit fusarium.",
    ("pnw", "9"): "In the mildest maritime pockets spears start in April; harvest into mid June, then let the ferns develop through summer to recharge the crown. Cool maritime springs make the hardiness zone a weak predictor of first cut, so watch the bed rather than the calendar.",
    ("ca_interior", "9"): "The deep peat soils of the Sacramento and San Joaquin Delta have grown asparagus for generations, and once established a crown can keep producing there for up to twenty years. Spears push up in March; harvest March into mid May, which is a long season by national standards, then let the ferns run through the hot summer on steady water. Commercial fields here start cutting in late February, but they force the crop for market; a home bed starts in March.",
    ("nevada", "9"): "On the warm valley floor spears push up in March; harvest for eight to ten weeks into May, then let the ferns grow through the hot summer with steady water and stop irrigating in fall so the crown gets its rest.",
    ("nevada", "10"): "In the warmest, low, frost-scarce pockets spears start in March, but the mild winters blunt the dormant rest asparagus depends on; the bed still cycles and produces, yet vigor tails off sooner than it would higher up. Harvest into May, then water the ferns through summer.",
    ("ca_south_coast", "9"): "On the mild South Coast spears push up in March; harvest March into mid May, then carry the ferns through a long warm season. Winters are too gentle to shut the plant down on its own, so withhold water in September and October and let the ferns dry down: that dry rest is what recharges the crown for the next spring.",
    ("ca_south_coast", "10"): "In the warmest South Coast pockets spears start in March, but the frost-scarce winter barely rests the crown; the bed still cycles and produces, yet vigor tails off sooner than it does inland. Harvest into mid May, then impose the rest yourself by cutting off water in early fall.",
    ("ca_south_coast", "11"): "In the warmest frost-free pockets of the South Coast spears start in March; harvest March into mid May, then carry the ferns through a long warm season. Nothing about the winter here will rest the crown for you, so withhold water in September and October and let the ferns dry down before cutting them back. Set crowns in January or February.",
    ("se_gulf", "8"): "In the cooler upper Southeast, roughly the Piedmont and mountains of north Georgia and the Carolinas, spears emerge in March; harvest March into May for six to eight weeks on an established bed, then let the ferns develop through the hot, humid summer and stand until they brown after frost.",
    ("se_gulf", "9"): "Along the warm coastal plain and Gulf, spears push up in March; harvest into May, then carry the ferns through a long, hot, humid summer. The mild winter often fails to shut the ferns down completely, so the crown never fully recharges and the bed fades sooner than it would farther north.",
}

# Region notes rewritten where they named harvest months that moved.
REGION_NOTES = {
    "warm_arid": (
        "A frost-anchored perennial for the inland Southwest; spears open in early March and an established bed cuts into May, since the long warm season supports one of the longest asparagus harvests in the country. Keep the summer ferns watered so the crown reloads before dormancy, and stop when the spears thin below pencil width.",
        "Asparagus does well in the inland Southwest. Spears start coming up in early March, and once the bed is a few years old you can keep picking into May, which is longer than most of the country gets. Water the ferns through summer, and stop cutting when the new spears get thinner than a pencil."),
    "utah_dixie": (
        "A frost-anchored perennial on the Mojave edge; the Dixie winter still delivers the dormant rest asparagus needs, so spears open in March and an established bed cuts into May. Carry the ferns through the hot summer on steady water, and stop when spears thin below pencil width.",
        "Asparagus works here: the Dixie winter is still cold enough to give the plant its rest. Spears start in March and you can keep picking into May once the bed is established. Water the ferns well through the hot summer, and stop cutting when the new spears get thin."),
    "mid_atlantic": (
        "A frost-anchored perennial; spears open in April across both the Piedmont and the Coastal Plain, and an established bed cuts into June. Let the ferns stand until they brown after frost, then cut them down for beetle and disease sanitation. Stop harvesting when spears thin below pencil width.",
        "Asparagus does well across the mid-Atlantic. Spears come up in April and you can keep picking into June once the bed is established. Leave the ferns up all summer, cut them down after frost browns them, and stop harvesting when the new spears get thinner than a pencil."),
    "mid_south": (
        "A frost-anchored perennial; spears open in April in both the Ozark uplands and the Delta lowlands, and an established bed cuts into early June. Snap spears rather than cutting below the soil to limit fusarium. Let the ferns stand until frost browns them.",
        "Asparagus does well across the mid-South. Spears come up in April and you can keep picking into early June once the bed is established. Snap the spears off at ground level rather than cutting into the soil, which helps keep disease down."),
    "nevada": (
        "A frost-anchored perennial for the Mojave high desert; spears open in March across the region and an established bed cuts into May, then the summer ferns need steady irrigation to reload the crown. In zone 10's mildest pockets the dormant rest is incomplete, so the bed only marginally perennializes and the rest has to come from a deliberate fall dry-down.",
        "Asparagus grows well across most of the Las Vegas Valley; plant crowns of a heat-tolerant variety like UC 157, give the bed deep water, and pick spears from March into May once it is established. In the warmest low pockets you will need to stop watering in fall so the plants get a real rest."),
    "se_gulf": (
        "A frost-anchored perennial across the upper Southeast, where zone 8 gets a real winter rest and perennializes well; spears open in March and an established bed cuts into May. Toward the Gulf the winter is often too mild to shut the ferns down completely, so plants keep pushing thin spears instead of resting, and the summer-wet climate offers no dry-down to substitute. Zone 9 is marginal on that basis, with a bed that fades after several years. Zone 10 is unsuitable: UF/IFAS omits asparagus from the Florida vegetable gardening guide entirely.",
        "Asparagus does well in the cooler upper Southeast: plant crowns of a rust-tolerant variety in the Piedmont or mountains and pick spears from March into May. Farther south the winters stay too warm for the plant to rest properly, and the wet summers do not help either, so expect a thinner, shorter-lived bed on the coastal plain and skip it altogether in the warmest parts of Florida."),
}

FINDING = {
    "id": "asparagus_harvest_fix_self_corrections",
    "summary": "THREE SELF-INFLICTED DEFECTS in the 2026-07-27 harvest re-authoring, all caught by "
               "a post-promote coherence scan rather than by any gate, and corrected in a "
               "follow-up pass. (1) PROVENANCE DESTROYED: the first pass overwrote "
               "`resolution_method` with harvest-specific values, erasing the plant_out/calendar "
               "provenance on 27 cells. resolution_method answers how the PLANTING window was "
               "reached; harvest provenance is an orthogonal axis. This is the identical design "
               "error I had advised the artichoke session against for source tier less than an "
               "hour earlier -- collapsing two independent axes into one string loses the "
               "cross-product. Fixed by restoring resolution_method from git and adding "
               "`harvest_resolution_method`. (2) TWO CELLS MISSED: se_gulf z8 and z9 were absent "
               "from the window table (27 rows for 29 cells), keeping the two-month artifact while "
               "every neighbour was corrected. (3) PROSE DRIFT: 9 cell notes and 6 region-note "
               "pairs still described the OLD windows -- 'harvest February into March' on a cell "
               "now reading Mar-May. That is precisely the defect class written up as item 1 of "
               "the post-asparagus hardening kickoff, reproduced within an hour of documenting it. "
               "The lesson generalizes: any pass that changes a value must re-read the prose that "
               "describes it, and that check needs to be mechanical because doing it by memory "
               "fails even when the author is actively aware of the risk.",
    "severity": "medium", "blocks_launch": False, "status": "resolved",
}


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)

    # 1. restore resolution_method from git HEAD, moving harvest provenance to its own key.
    head = json.loads(subprocess.run(["git", "show", "HEAD:crops_data_final.json"],
                                     capture_output=True, text=True).stdout)
    old = next(c for c in head["crops"] if c.get("slug") == "asparagus")
    restored = 0
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            cur = cell.get("resolution_method")
            if isinstance(cur, str) and cur.startswith("harvest_"):
                cell["harvest_resolution_method"] = cur
                prev = ((old.get("regions") or {}).get(rk) or {}).get(
                    "resolved_by_zone", {}).get(z, {}).get("resolution_method")
                if prev:
                    cell["resolution_method"] = prev
                    restored += 1

    # 2. the two missed cells
    fixed = 0
    for (rk, z), (a, b) in MISSED.items():
        cell = ((crop.get("regions") or {}).get(rk) or {}).get("resolved_by_zone", {}).get(z)
        cal = list(cell.get("calendar") or [])
        cell["calendar"] = ["harvest" if a <= i <= b else ("growing" if t == "harvest" else t)
                            for i, t in enumerate(cal)]
        cell["harvest"] = f"{MON[a]} - {MON[b]}"
        cell["harvest_resolution_method"] = "harvest_sourced_duration_modeled_start"
        fixed += 1

    # 3. prose drift
    n_cell = 0
    for (rk, z), text in CELL_NOTES.items():
        cell = ((crop.get("regions") or {}).get(rk) or {}).get("resolved_by_zone", {}).get(z)
        cell["notes"] = text
        n_cell += 1
    n_reg = 0
    for rk, (s, b) in REGION_NOTES.items():
        r = (crop.get("regions") or {}).get(rk)
        r["region_notes_seasoned"], r["region_notes_beginner"] = s, b
        n_reg += 1

    ofs = crop.setdefault("verification_status", {}).setdefault("open_findings", [])
    if FINDING["id"] not in {f.get("id") for f in ofs if isinstance(f, dict)}:
        ofs.append(FINDING)

    print(f"resolution_method restored (harvest provenance moved out) : {restored} cells")
    print(f"missed cells authored (se_gulf z8/z9)                     : {fixed}")
    print(f"cell notes rewritten                                      : {n_cell}")
    print(f"region note PAIRS rewritten                               : {n_reg}")
    print(f"open_findings                                             : {len(ofs)}")

    if dry:
        print("\n--dry-run: canonical NOT written")
        return
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("\nwrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
