#!/usr/bin/env python3
"""The asparagus harvest-duration pass: six cells, four field-side and two note-side repairs.

THE RULING THIS IMPLEMENTS (docs/2026-07-27-harvest-window-semantics-ruling.md). `harvest`
strings are month-granular touch-sets, and a month may be named only if the cell's sourced
duration can actually reach it. Under that ruling six cells contradicted themselves; per-cell
source reads decided WHICH HALF of each cell is the correct one. Four fields were wrong, two
notes were wrong. Editing the other half in any of the six would have silenced the half telling
the truth.

FIELD-SIDE (harvest + calendar move together; notes already correct, untouched):
  mid_south z7      Apr - Jun -> Apr - May   MU G6405, cited on the cell: "April 14 to May 30
                                             in southern Missouri" (the Ozark-upland band).
  northern_tier z7  Apr - Jun -> Apr - May   MU's own gradient: the WARMER band stops EARLIER
                                             (bootheel Apr 10 - May 25); no June anywhere in
                                             the z7 geography's rows.
  northern_tier z5  Apr - Jun -> May - Jun   UMN, cited on the cell: "about 6 to 8 weeks, from
                                             early May to late June in Minnesota"; the note
                                             already said "early to mid May". April was painted
                                             before emergence.
  utah_dixie z8     Mar - May -> Mar - Apr   USU: 6 wk yr 4 / up to 8 wk yr 5+; from an early
                                             March St. George emergence the top end only grazes
                                             May 1. Now matches low_desert_az (Mar - Apr), the
                                             same Mojave-edge climate.

NOTE-SIDE (field + calendar already correct, untouched):
  mid_atlantic z7   note carried Rutgers' 6 weeks while the field carried UMD's June: a genuine
                    source disagreement silently split across the two halves of one cell. Per
                    the arc's standing carry-the-range rule the note now states six to ten weeks
                    into June and names both authorities.
  northern_tier z6  note said "into May" against Illinois (cited on the cell): "harvested ...
                    through May or June (as long as 8 to 10 weeks)" and UMN: "Harvest spears
                    until June 30". Single-word repair, May -> June, justified by the cell's own
                    sources (UMN 6-8 and Illinois 8-10 overlap at 8, so no range-carry).

Usage: python3 tools/promote_harvest_duration_pass.py [--write]
Dry-run by default. Aborts on ANY drift from the expected pre-state. Prove the abort by
re-running after --write: the SHA guard must refuse the second pass.
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "02fbb5e88c278d741791644b7774da1182e389db28c12d81245297f0e96ae6dc"

CP, HV, GR = "cold_pause", "harvest", "growing"

# --- exact expected pre-state per cell; any deviation aborts ----------------------------------
REPAIRS = [
    {
        "cell": ("mid_south", "7"),
        "before": {
            "harvest": "Apr - Jun",
            "calendar": [CP, CP, CP, HV, HV, HV, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "In the cooler Ozark uplands spears emerge in April; harvest for four to "
                     "six weeks into May, then let the ferns grow through summer and stand until "
                     "a killing frost, when the crown dies back and rests over winter.",
        },
        "after": {
            "harvest": "Apr - May",
            "calendar": [CP, CP, CP, HV, HV, GR, GR, GR, GR, GR, CP, CP],
        },
    },
    {
        "cell": ("northern_tier", "7"),
        "before": {
            "harvest": "Apr - Jun",
            "calendar": [CP, CP, CP, HV, HV, HV, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "On the mild zone 7 edge spears can push in early April; harvest six to "
                     "eight weeks into May, then let the ferns develop through the summer to "
                     "rebuild the crown ahead of the dormant season.",
        },
        "after": {
            "harvest": "Apr - May",
            "calendar": [CP, CP, CP, HV, HV, GR, GR, GR, GR, GR, CP, CP],
        },
    },
    {
        "cell": ("northern_tier", "5"),
        "before": {
            "harvest": "Apr - Jun",
            "calendar": [CP, CP, CP, HV, HV, HV, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "In zone 5 spears break ground in early to mid May; harvest for six to "
                     "eight weeks into June, then stop and let the ferns grow through summer to "
                     "recharge the crown before it dies back and rests over winter.",
        },
        "after": {
            "harvest": "May - Jun",
            "calendar": [CP, CP, CP, CP, HV, HV, GR, GR, GR, GR, CP, CP],
        },
    },
    {
        "cell": ("utah_dixie", "8"),
        "before": {
            "harvest": "Mar - May",
            "calendar": [CP, CP, HV, HV, HV, GR, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "St. George sits in Utah's warmest, Mojave-edge corner, yet its winters "
                     "still bring frost and a real dormant rest, so asparagus perennializes; "
                     "spears push up early as the soil warms in March, harvest through March and "
                     "April for six to eight weeks, then let the summer ferns recharge the crown "
                     "before winter.",
        },
        "after": {
            "harvest": "Mar - Apr",
            "calendar": [CP, CP, HV, HV, GR, GR, GR, GR, GR, GR, CP, CP],
        },
    },
    {
        "cell": ("mid_atlantic", "7"),
        "before": {
            "harvest": "Apr - Jun",
            "calendar": [CP, CP, CP, HV, HV, HV, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "Across the Piedmont spears emerge in April as the soil warms; harvest for "
                     "about six weeks into May, then let the ferns grow through summer and stand "
                     "until they brown in late fall, when the crown rests through winter.",
        },
        "after": {
            "notes": "Across the Piedmont spears emerge in April as the soil warms; harvest for "
                     "six to ten weeks into June (Rutgers pegs a mature bed at six weeks, "
                     "Maryland at eight to ten, so let spear thickness make the call), then let "
                     "the ferns grow through summer and stand until they brown in late fall, "
                     "when the crown rests through winter.",
        },
    },
    {
        "cell": ("northern_tier", "6"),
        "before": {
            "harvest": "Apr - Jun",
            "calendar": [CP, CP, CP, HV, HV, HV, GR, GR, GR, GR, CP, CP],
            "suitability": "perennializes",
            "notes": "Zone 6 warms a touch earlier, so spears start in April; cut for six to "
                     "eight weeks into May, then leave the ferns to grow all summer and feed the "
                     "crown before fall dieback and winter dormancy.",
        },
        "after": {
            "notes": "Zone 6 warms a touch earlier, so spears start in April; cut for six to "
                     "eight weeks into June, then leave the ferns to grow all summer and feed "
                     "the crown before fall dieback and winter dormancy.",
        },
    },
]

NEW_FINDING = {
    "severity": "medium",
    "blocks_launch": False,
    "status": "resolved",
    "finding": (
        "DURATION PASS COMPLETE 2026-07-27 (docs/2026-07-27-harvest-window-semantics-ruling.md). "
        "RULED: harvest strings are month-granular TOUCH-SETS (verified against the plant-astro "
        "renderer, which discards day numbers and paints whole touched months), but a month may "
        "be named only if the cell's sourced duration can reach it. Under that ruling six cells "
        "contradicted themselves and per-cell source reads decided which half was correct: "
        "FIELD-SIDE repairs mid_south z7 Apr-Jun -> Apr-May (MU G6405: 'April 14 to May 30 in "
        "southern Missouri'), northern_tier z7 Apr-Jun -> Apr-May (MU's gradient: warmer bands "
        "stop earlier, no June in the z7 rows), northern_tier z5 Apr-Jun -> May-Jun (UMN: 'about "
        "6 to 8 weeks, from early May to late June in Minnesota'; April was painted before "
        "emergence), utah_dixie z8 Mar-May -> Mar-Apr (USU 6-8 wk from an early-March emergence "
        "only grazes May 1; now matches low_desert_az). NOTE-SIDE repairs mid_atlantic z7 (the "
        "note took Rutgers' 6 weeks while the field took UMD's June; now carries the range six "
        "to ten weeks into June per the standing carry-the-range rule) and northern_tier z6 "
        "(note 'into May' -> 'into June' per its own cited Illinois 'through May or June (as "
        "long as 8 to 10 weeks)' and UMN 'until June 30'). The other 12 of the brief's 20 "
        "flagged-or-unmeasured cells were examined and check out; mid_south z8 upgraded from "
        "unmeasured to sourced-consistent (UADA FSA-6002: 'spears may be harvested from April "
        "into June'). CLASS CLOSED MECHANICALLY: tools/harvest_duration_gate.py (REACH + END + "
        "START, roster-wide, measured zero flood) reproduces all six defects on pre-fix canonical "
        "02fbb5e8 and returns 0 after this promote; RED-proven via git-pinned historical test in "
        "tools/test_harvest_duration_gate.py. Hard-flip into whole_crop_gate queued behind the "
        "artichoke session's uncommitted A48."
    ),
}


def fail(msg):
    sys.exit(f"ABORT: {msg}")


def main():
    write = "--write" in sys.argv
    raw = open(PATH, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        fail(f"canonical SHA {sha[:16]} != expected {EXPECT_SHA[:16]}")
    print(f"canonical SHA OK: {sha[:16]}")

    data = json.loads(raw.decode("utf-8"))
    if len(data["crops"]) != 128:
        fail(f"crop count {len(data['crops'])} != 128")

    asp = [c for c in data["crops"] if c.get("slug") == "asparagus"]
    if len(asp) != 1:
        fail(f"expected exactly 1 asparagus crop, found {len(asp)}")
    asp = asp[0]

    # pre-state: every expected value, every cell, before anything is touched
    for rep in REPAIRS:
        rk, z = rep["cell"]
        cell = asp["regions"][rk]["resolved_by_zone"][z]
        for k, v in rep["before"].items():
            if cell.get(k) != v:
                fail(f"drift on {rk}.z{z}.{k}\n  have: {cell.get(k)!r}\n  want: {v!r}")
    print(f"pre-state OK: all {len(REPAIRS)} cells match every expected value")

    # reference cells that must be untouched by this pass
    refs = {
        ("mid_south", "8"): "Apr - Jun",       # UADA-sourced, checks out
        ("mid_atlantic", "8"): "Apr - Jun",    # note says June, coherent
        ("pnw", "8"): "Apr - Jun",
        ("northern_tier", "3"): "May - Jun",
        ("northern_tier", "4"): "May - Jun",
        ("low_desert_az", "9"): "Mar - Apr",   # the analog utah_dixie now matches
    }
    for (rk, z), h in refs.items():
        have = asp["regions"][rk]["resolved_by_zone"][z].get("harvest")
        if have != h:
            fail(f"reference cell {rk} z{z} drifted: harvest {have!r} != {h!r}")
    print(f"reference OK: {len(refs)} untouched neighbor cells verified")

    # apply
    for rep in REPAIRS:
        rk, z = rep["cell"]
        cell = asp["regions"][rk]["resolved_by_zone"][z]
        for k, v in rep["after"].items():
            cell[k] = v

    # post-invariants
    for rep in REPAIRS:
        rk, z = rep["cell"]
        cell = asp["regions"][rk]["resolved_by_zone"][z]
        if len(cell["calendar"]) != 12:
            fail(f"{rk} z{z}: calendar length != 12")
        if "harvest" not in cell or not cell["harvest"]:
            fail(f"{rk} z{z}: harvest missing after repair")
        if "—" in cell.get("notes", ""):
            fail(f"{rk} z{z}: em dash in consumer copy")

    # the gate this pass ships must return zero on the repaired crop
    sys.path.insert(0, "tools")
    from harvest_duration_gate import duration_violations
    residue = duration_violations(asp)
    if residue:
        fail("harvest_duration_gate still fires after repair:\n  " + "\n  ".join(residue))
    print("invariant OK: harvest_duration_gate returns 0 on the repaired crop")

    # zone ordering must stay monotonic where we touched starts
    from zone_order_gate import zone_order_violations
    zv = zone_order_violations(asp)
    if zv:
        fail("zone_order_gate fires after repair:\n  " + "\n  ".join(zv))
    print("invariant OK: zone_order_gate returns 0 on the repaired crop")

    vs = asp.setdefault("verification_status", {})
    findings = vs.setdefault("open_findings", [])
    findings.append(NEW_FINDING)
    print(f"open_findings: {len(findings) - 1} -> {len(findings)}")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        fail("trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        for rep in REPAIRS:
            rk, z = rep["cell"]
            what = ", ".join(sorted(rep["after"]))
            print(f"  {rk} z{z}: {what}")
        return

    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    new = hashlib.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new[:8]}")


if __name__ == "__main__":
    main()
