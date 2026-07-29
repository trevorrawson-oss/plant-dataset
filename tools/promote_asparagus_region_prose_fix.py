#!/usr/bin/env python3
"""Repair asparagus ca_south_coast's region prose, which contradicts its own cells.

FOUND BY `tools/region_prose_gate.py` ON ITS FIRST RUN, 2026-07-28, on a crop that had passed a
120/120 roster gate. Two contradictions in one prose block, both the R7 defect class -- region
prose and per-cell data are two layers the same guide renders to the same reader, and until this
gate existed nothing compared them.

DEFECT 1 (what the gate caught). The seasoned register says "Frost-free zone 11 is unsuitable" and
the beginner register says "in zone 11 it is not worth planting", while the z11 CELL is rated
`marginal` and carries a full `plant_out`, a `harvest` window, and a suitability note.

WHICH HALF IS WRONG: THE PROSE. The evidence is one-sided.
  - The z11 cell is thoroughly authored (`adjacent_zone_derived`) and its own note says the
    dry-down is "the same mechanism the adjacent zone 10 relies on, and UC's South Coast crown
    window covers this ground."
  - z10 is ALSO "essentially frost-free" and is rated `marginal` on exactly that mechanism. The
    prose asserts z11 is unsuitable one sentence after explaining that frost-free z10 works fine,
    so it contradicts its own stated reasoning as well as the cell.
  - The mechanism is NOT frost-dependent: the crown's rest is imposed by withholding irrigation,
    which a gardener supplies identically in z10 and z11.
  - An `unsuitable` cell is exempt from A47/A48; z11 carries both fields, so it was authored
    deliberately as a productive cell.
  The prose is stale from the arc's suitability re-rate (18/8/13 -> 22/3/14), which is the same
  way `ca_north_coast` was left saying "perennialize only marginally" for two promoted cells.

DEFECT 2 (found while reading, NOT gate-caught, and recorded as a gate gap). The same block ends
"Harvest from February" while ALL THREE cells in the region carry `harvest: "Mar - May"` and every
cell note says spears start in March. No gate compares a region-prose MONTH against its cells'
harvest windows -- region_prose_gate reads suitability and zones only. Fixed here; the gap is
surfaced rather than papered over.

FOOTPRINT: 2 strings, one crop, one region. No cell, no rating, no source touched.
Pre-state is pinned by SHA256 OF EACH EXPECTED STRING rather than a transcribed copy, so a typo
in this script cannot silently overwrite something other than what was reviewed.

  python3 tools/promote_asparagus_region_prose_fix.py            # -> scratch
  python3 tools/promote_asparagus_region_prose_fix.py --promote  # -> canonical
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "crops_data_final.json")
SCRATCH = os.path.join(HERE, "..", "crops_data_final.scratch.json")

EXPECTED_SHA = "05090b3c20ab43ad392450152b367bd1255cee00e4976b3fc10c6c225652b429"

SLUG, REGION = "asparagus", "ca_south_coast"

# key -> (sha256 of the exact pre-state string, replacement)
EDITS = {
    "region_notes_seasoned": (
        "f7e32b1244713454764a902e0d6ea713e175e770865ee655dc0abdb8a8a66a43",
        "On the South Coast the dormant rest has to be imposed rather than waited for: withhold "
        "irrigation in September and October so the ferns dry down. Zone 9 still gets enough "
        "winter cool to back that up and carries a productive bed, and UC publishes a home-garden "
        "crown window for this coast, with production recorded in Orange and Ventura counties. "
        "Zones 10 and 11 are essentially frost-free, so the crown's annual rest depends wholly on "
        "the gardener's dry-down and UC publishes no bed lifespan for either: workable, but beds "
        "you actively manage rather than beds that look after themselves. Harvest runs March into "
        "mid May across all three zones."),
    "region_notes_beginner": (
        "406a15c1775d18fd126fe01a3a9d499220365241b39527e72795388f54311002",
        "Asparagus is worth growing on the South Coast if you are willing to give it a dry rest "
        "each fall: stop watering in September and October and let the ferns brown off. Zone 9 "
        "takes to that well. In the frost-free stretches of zones 10 and 11 it will still crop, "
        "but the bed needs your attention rather than looking after itself. Pick from March into "
        "mid May."),
}


def sha_of_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sha_of(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main():
    promote = "--promote" in sys.argv
    got = sha_of_file(PATH)
    if got != EXPECTED_SHA:
        print("ABORT: canonical drifted from the SHA this fix was authored against.")
        print(f"  expected {EXPECTED_SHA}\n  got      {got}")
        return 1

    data = json.load(open(PATH, encoding="utf-8"))
    crop = next(c for c in data["crops"] if c.get("slug") == SLUG)
    region = crop["regions"][REGION]

    for key, (pre_sha, new) in EDITS.items():
        cur = region.get(key)
        if not isinstance(cur, str):
            print(f"ABORT: {key} is not a string ({type(cur).__name__})")
            return 1
        if sha_of(cur) != pre_sha:
            print(f"ABORT: {key} pre-state hash mismatch -- refusing to overwrite unreviewed text.")
            print(f"  expected {pre_sha}\n  got      {sha_of(cur)}\n  current: {cur[:160]!r}")
            return 1
        region[key] = new

    out = PATH if promote else SCRATCH
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    print(f"wrote {os.path.basename(out)}  ({'CANONICAL' if promote else 'scratch'})")
    print(f"  {SLUG}.{REGION}: {len(EDITS)} string(s) replaced")
    for z, c in sorted(region["resolved_by_zone"].items(), key=lambda kv: int(kv[0])):
        print(f"    z{z}: {c.get('suitability')}  harvest={c.get('harvest')!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
