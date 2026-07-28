#!/usr/bin/env python3
"""ca_desert z9 -- repair the seed-window contamination and the zone ordering inversion.

THE DEFECT. `ca_desert` z9 (the cooler desert ground) carried:
    plant_out = "Feb 1 - Apr 30 (dormant crowns, one-time planting)"
    harvest   = "Feb - Apr"
while the WARMER z10 valley floor (Imperial/Coachella) carried plant_out Nov 1 - Feb 1 and
harvest Mar - Apr. The cooler zone therefore claimed to be harvested a MONTH EARLIER than the
warmer zone of the same crop, and the two crown windows did not overlap at all -- a grower in
Blythe and a grower in Coachella were told to plant in seasons four months apart.

ROOT CAUSE, and it is not a modeling judgment. UC ANR Pub 7234 -- already cited on this very
cell -- contains two different sentences:

  CROWNS: "October through March is usually best for establishing asparagus stands with
           transplants or crowns."
  SEED:   "In the low desert, asparagus SEED is often spring planted from February to April,
           taking nearly 2 years to yield substantial production."

Both of z9's values match the SEED sentence exactly (Feb-Apr), and the plant_out runs a full
month past the end of the crown window, on a field explicitly labeled "dormant crowns". This is
the identical failure that produced the original `ca_interior` z9 Delta defect: the right
document, cited on the right cell, read off the wrong sentence.

THE REPAIR, all three values moved together so the cell stays internally coherent:
  plant_out -> "Jan 1 - Mar 1"  -- inside Pub 7234's Oct-Mar crown window, and matching its
               "late winter or early spring" crown statement. Later than z10's Nov 1 - Feb 1,
               which is the correct gradient: cooler ground plants later, not earlier.
  harvest   -> "Mar - May"      -- start no earlier than the warmer z10 (removes the inversion),
               with the later tail the cooler ground actually earns, because in the desert the
               season closes on HEAT and the heat ceiling arrives later at elevation. Consistent
               with the `nevada` Mojave cells (Mar - May), the closest analog in the roster, and
               with California's sourced 8-to-10-week mature duration off a March start.
  calendar  -> Feb moves from `harvest` to `cold_pause`; May moves from `growing` to `harvest`.

The start remains MODELED and `harvest_resolution_method` stays
`harvest_sourced_duration_modeled_start`. No home-garden T1 source publishes a harvest start for
the cooler California desert; see docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md. What
this pass fixes is a value derived from the WRONG SENTENCE, not the absence of a source.

PROSE. The cell note said "spears emerge in February; harvest February into March" -- stale on
BOTH counts (it predates the 2026-07-27 harvest re-source, which had already moved the field to
Feb - Apr without touching the note). Rewritten to match the repaired values.

Usage: python3 tools/promote_ca_desert_z9_fix.py [--write]
Dry-run by default. Aborts on ANY drift from the expected pre-state.
"""
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "0da1d2345f8a6e9806d00ca046ea4bc43b0323673abf734d769915b06c63c96d"

CP, HV, GR = "cold_pause", "harvest", "growing"

# --- exact expected pre-state; any deviation aborts -------------------------------------------
BEFORE = {
    "plant_out": "Feb 1 - Apr 30 (dormant crowns, one-time planting)",
    "harvest": "Feb - Apr",
    "calendar": [CP, HV, HV, HV, GR, GR, GR, GR, GR, GR, CP, CP],
    "suitability": "perennializes",
    "harvest_resolution_method": "harvest_sourced_duration_modeled_start",
}

AFTER = {
    "plant_out": "Jan 1 - Mar 1 (dormant crowns, one-time planting)",
    "harvest": "Mar - May",
    "calendar": [CP, CP, HV, HV, HV, GR, GR, GR, GR, GR, CP, CP],
    "notes": (
        "On the cooler desert ground spears break through in March, just behind the valley "
        "floor, and the cut can run into May because the heat that closes the season arrives "
        "later up here. Set dormant crowns across winter while they are still asleep, then "
        "carry the ferns through a very hot summer on steady irrigation. Winter frost plus a "
        "deliberate fall dry-down gives the crown a clean rest. Fern growth slows above 85°F, "
        "so shade and deep water decide how well the crown reloads, but the bed still pays: UC "
        "counts the southern desert valleys among California's main asparagus districts, with "
        "stands holding 8 to 10 years."
    ),
}

NEW_FINDING = {
    "severity": "medium",
    "blocks_launch": False,
    "status": "resolved",
    "finding": (
        "DEFECT FIXED 2026-07-27 (second pass), ca_desert z9. The cell carried plant_out "
        "'Feb 1 - Apr 30' and harvest 'Feb - Apr', which made the COOLER desert zone claim a "
        "harvest a month EARLIER than the warmer z10 valley floor, with crown windows that did "
        "not overlap at all (z10 was Nov 1 - Feb 1). Root cause: UC ANR Pub 7234, cited on this "
        "cell, says 'October through March is usually best for establishing asparagus stands "
        "with transplants or crowns' but ALSO says 'In the low desert, asparagus SEED is often "
        "spring planted from February to April'. Both of z9's values matched the SEED sentence, "
        "and plant_out ran a month past the end of the crown window on a field labeled 'dormant "
        "crowns'. This is the ca_interior z9 Delta failure repeated: right document, wrong "
        "sentence. Repaired to plant_out 'Jan 1 - Mar 1' (inside the Oct-Mar crown window and "
        "matching 7234's 'late winter or early spring') and harvest 'Mar - May' (no earlier than "
        "the warmer z10, with the later tail cooler ground earns since the desert season closes "
        "on heat; consistent with the nevada Mojave cells). Calendar moved with them. The start "
        "remains MODELED. The cell note, which still read 'spears emerge in February; harvest "
        "February into March' and was stale even against the pre-fix value, was rewritten. "
        "ALSO CONFIRMED IN THIS PASS: z10 is correct and was not touched, UA az1615 (Yuma) "
        "states asparagus 'Planting Window October-February, Harvest Window March-April' "
        "outright, read from the PDF text layer."
    ),
}


def main():
    write = "--write" in sys.argv
    raw = open(PATH, "rb").read()
    import hashlib
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        sys.exit(f"ABORT: canonical SHA {sha[:16]} != expected {EXPECT_SHA[:16]}")
    print(f"canonical SHA OK: {sha[:16]}")

    data = json.loads(raw.decode("utf-8"))
    if data.get("total_crops") != 128 and len(data["crops"]) != 128:
        sys.exit(f"ABORT: crop count {len(data['crops'])} != 128")

    asp = [c for c in data["crops"] if c.get("slug", "").startswith("asparagus")]
    if len(asp) != 1:
        sys.exit(f"ABORT: expected exactly 1 asparagus crop, found {len(asp)}")
    asp = asp[0]

    cell = asp["regions"]["ca_desert"]["resolved_by_zone"]["9"]
    for k, v in BEFORE.items():
        if cell.get(k) != v:
            sys.exit(f"ABORT: drift on ca_desert.z9.{k}\n  have: {cell.get(k)!r}\n  want: {v!r}")
    print("pre-state OK: ca_desert z9 matches all 5 expected values")

    # z10 must be untouched and is the ordering reference
    z10 = asp["regions"]["ca_desert"]["resolved_by_zone"]["10"]
    if z10.get("harvest") != "Mar - Apr" or not z10.get("plant_out", "").startswith("Nov 1 - Feb 1"):
        sys.exit(f"ABORT: z10 reference drifted: harvest={z10.get('harvest')!r} "
                 f"plant_out={z10.get('plant_out')!r}")
    print("reference OK: z10 harvest 'Mar - Apr' / plant_out 'Nov 1 - Feb 1' unchanged")

    for k, v in AFTER.items():
        cell[k] = v

    # ordering invariant: cooler z9 must not start before warmer z10
    MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    s9 = MON.index(cell["harvest"].split(" - ")[0])
    s10 = MON.index(z10["harvest"].split(" - ")[0])
    if s9 < s10:
        sys.exit(f"ABORT: inversion persists -- z9 starts {cell['harvest']} before z10 {z10['harvest']}")
    print(f"invariant OK: z9 harvest starts {MON[s9]} >= z10 {MON[s10]} (inversion cleared)")

    if len(cell["calendar"]) != 12:
        sys.exit("ABORT: calendar length != 12")

    vs = asp.setdefault("verification_status", {})
    findings = vs.setdefault("open_findings", [])
    findings.append(NEW_FINDING)
    print(f"open_findings: {len(findings) - 1} -> {len(findings)}")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        sys.exit("ABORT: trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        print(f"  plant_out : {BEFORE['plant_out']!r}\n           -> {AFTER['plant_out']!r}")
        print(f"  harvest   : {BEFORE['harvest']!r}\n           -> {AFTER['harvest']!r}")
        return

    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    import hashlib as _h
    new = _h.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new[:8]}")


if __name__ == "__main__":
    main()
