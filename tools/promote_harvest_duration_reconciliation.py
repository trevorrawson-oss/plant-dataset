#!/usr/bin/env python3
"""The asparagus harvest-duration RECONCILIATION: three layers of one crop made to agree.

WHAT THIS FIXES. After the 2026-07-27 duration pass closed the field-vs-note class, three
LAYERS of asparagus still made different claims about the same mature bed:

  1. `harvest_ramp_weeks` bed year 5 said [8, 10].
  2. `harvest_ready_beginner` / `_seasoned` said "about six to eight weeks" / "a roughly
     six-to-eight-week spring window" -- a different claim in the same crop (RAMP-PROSE).
  3. 15 region cells stated a duration in prose; 12 of them disagreed with [8, 10]. Only
     ca_interior z8, nevada z8 and nevada z9 matched it.

THE RULING (owner, 2026-07-28). Bed year 5 becomes [6, 10]. Across eight independently
fetched T1 documents the mature figure spans 6 to 10 weeks (UMN 6-8, Rutgers 6, USU 6-8,
MU 5-8, UMD 8-10, Illinois 8-10, UC ANR 7234 8-10, NMSU max 10) and UC Master Gardener
statewide publishes that exact span: "they may be harvested for 6 to 10 weeks per year."
[8, 10] collapsed a 6-to-10 span to its upper end -- the same false-precision error as the
year-2 [0, 0] collapse, in the same field.

WHAT LANDS (all from tools/staging/harvest_duration/authored.json, authored task 5):
  harvest_stop_rule       NEW crop-level object. signal=spear_diameter, threshold_inches
                          [0.25, 0.5] carrying the NMSU 1/4 in. to UC Marin 1/2 in. spread
                          (MU's 3/8 in. sits inside it), dual-register notes, six sources.
                          The stop rule was prose-only before; the app can now dispatch on it.
  harvest_ramp_weeks[5]   [8, 10] -> [6, 10].
  harvest_ready_beginner  rewritten: bed-age ramp + the spear-caliper stop, no bare week
  harvest_ready_seasoned  count, so the prose no longer restates the ramp in a second voice.
  harvest_duration_weeks  NEW per-cell override on exactly two cells, each on an in-region
                          T1 quote: mid_south z7 [4, 8] (UADA FSA-6002 four-to-six + MU G6405
                          five-to-eight, carry the range) and utah_dixie z8 [6, 8] (USU
                          "Harvest can be 6-8 weeks in following years").
  notes                   mid_south z7 only. Its note and its override are two representations
                          of ONE claim; moving the override to [4, 8] without moving the note
                          off "four to six weeks" fires OVERRIDE-PROSE. They travel together.

WHAT DELIBERATELY DOES NOT LAND. Nine cells were source-checked and left inheriting the crop
default because no cited in-region document publishes a duration (mid_atlantic z7/z8,
northern_tier z3-z7, pnw z8, se_gulf z8, warm_arid z8). se_gulf z8's [6, 8] is quote-backed by
UGA C1026 but that id is absent from source_catalog and uncited on the cell, so it is parked in
`deferred_candidates` rather than promoted. See the staging file's `evidence` block.

Usage: python3 tools/promote_harvest_duration_reconciliation.py [--write]
Dry-run by default. Aborts on ANY drift from the expected pre-state. Prove the abort by
re-running after --write: the SHA guard must refuse the second pass.
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
STAGING = "tools/staging/harvest_duration/authored.json"
EXPECT_SHA = "a995333fd2c0e15d25c6116691d82225311acb85264441e653bc74faf6bb64ce"

# --- exact expected pre-state (captured from canonical a995333f); any deviation aborts -------
EXPECT_RAMP_BED_YEAR = 5
EXPECT_RAMP_WEEKS = [8, 10]

EXPECT_BEGINNER = "On an established bed, start cutting in spring when the spears are about 6 to 8 inches tall and their tips are still tight and closed. Snap each spear off at the ground, or cut it at the soil line, and pick again every day or two, because spears come up fast and open into ferns if you leave them. Keep harvesting for about six to eight weeks, then stop when the new spears thin down to about pencil width. That thinning is the plant telling you it is low on energy, so let the rest grow into ferns to feed the roots for next year. Do not harvest at all the first year after planting, and take only a little the second year."

EXPECT_SEASONED = "On a bearing bed, cut spears at about 6 to 8 inches with the tips still tight, before they begin to open, snapping them off at the soil line or cutting just below it. Harvest every one to three days through a roughly six-to-eight-week spring window; in warm weather spears elongate and fern out fast, so a bed can need daily picking. The signal to stop is the spears themselves: end the season when the majority thin to about pencil diameter, under 3/8 inch, which marks the crown running low on reserves. Cutting past that point drains the crown and weakens next spring's yield, so let the remaining spears grow to fern. Hold off entirely in the planting year and take only a light pick in year two while the crown builds strength."

# region -> zone -> the note this pass replaces. Keys must match the staging file's
# `cell_notes` exactly: a note the promote rewrites without asserting is a note that
# could have drifted underneath it.
EXPECT_CELL_NOTES = {
    ("mid_south", "7"): "In the cooler Ozark uplands spears emerge in April; harvest for four to six weeks into May, then let the ferns grow through summer and stand until a killing frost, when the crown dies back and rests over winter.",
}

# Cells that state a duration MATCHING the crop ramp and therefore correctly receive no
# override. They are the control group: if this pass touched them, the override set is wrong.
REFERENCE_CELLS = {
    ("ca_interior", "8"): {
        "harvest": "Mar - May",
        "notes": "In the cooler valley margins and foothills spears emerge in March; harvest March into May for eight to ten weeks, then let the ferns grow through the hot summer with irrigation, and stop watering in fall so the crown goes dormant and rests over winter.",
    },
    ("nevada", "8"): {
        "harvest": "Mar - May",
        "notes": "In the higher, cooler reaches of the Las Vegas Valley spears emerge in March; harvest March into May for eight to ten weeks, then keep the summer ferns irrigated to recharge the crown before it goes dormant and rests through the cool desert winter.",
    },
    ("nevada", "9"): {
        "harvest": "Mar - May",
        "notes": "On the warm valley floor spears push up in March; harvest for eight to ten weeks into May, then let the ferns grow through the hot summer with steady water and stop irrigating in fall so the crown gets its rest.",
    },
}


NEW_FINDING = {
    "severity": "medium",
    "blocks_launch": False,
    "status": "resolved",
    "finding": (
        "HARVEST-DURATION RECONCILIATION COMPLETE 2026-07-28. Three layers of asparagus made "
        "different claims about the same mature bed and now agree. RULED (owner, 2026-07-28): "
        "harvest_ramp_weeks bed year 5 [8, 10] -> [6, 10]. Eight independently fetched T1 "
        "documents place the mature-bed season between 6 and 10 weeks (UMN 6-8, Rutgers 6, USU "
        "6-8, MU G6405 5-8, UMD 8-10, Illinois 8-10, UC ANR 7234 8-10, NMSU max 10) and UC "
        "Master Gardener statewide publishes the span verbatim ('they may be harvested for 6 to "
        "10 weeks per year'); [8, 10] collapsed that span to its upper end, the same "
        "false-precision error as the year-2 [0,0] collapse in the same field. NEW FIELD "
        "harvest_stop_rule (crop-level): signal 'spear_diameter', threshold_inches [0.25, 0.5] "
        "carrying NMSU's 1/4 in. against UC Marin's 1/2 in. with MU G6405's 3/8 in. inside the "
        "range, dual-register notes, six verified sources. The pencil-diameter stop was prose-only "
        "before, so the app could not dispatch on it. harvest_ready_beginner/_seasoned rewritten "
        "to lead with the bed-age ramp and close on spear caliper, dropping the bare "
        "six-to-eight-week counts that contradicted the ramp (RAMP-PROSE). NEW per-cell field "
        "harvest_duration_weeks on exactly two cells, each on an in-region T1 quote: mid_south z7 "
        "[4, 8] (UADA FSA-6002 'four to six weeks' against MU G6405 'five to eight weeks', carry "
        "the range; its note moves with it because override and prose are two representations of "
        "one claim) and utah_dixie z8 [6, 8] (USU 'Harvest can be 6-8 weeks in following years'). "
        "NINE cells were source-checked and deliberately left inheriting the crop default because "
        "no cited in-region document publishes a duration: mid_atlantic z7/z8, northern_tier "
        "z3/z4/z5/z6/z7, pnw z8, se_gulf z8, warm_arid z8. Two honest gaps surfaced and NOT "
        "papered over: five cell source ids resolve to extension PORTAL ROOTS with zero asparagus "
        "content (ndsu_ext, sdsu_ext, umaine_ext, iastate_ext, uconn_ext, plus mu_ext on "
        "northern_tier z7), and msu_ext returns an 85-character JavaScript shell at all three URL "
        "spellings, so it is cited for nothing here. se_gulf z8's [6, 8] is quote-backed by UGA "
        "C1026 but that id is absent from source_catalog and uncited on the cell, so it is parked "
        "as a deferred candidate. CLASS CLOSED MECHANICALLY: tools/harvest_duration_gate.py "
        "RAMP-FIRST + RAMP-PROSE + STOP-SHAPE + OVERRIDE-PROSE + REACH/END/START returns 0 "
        "roster-wide after this promote, and the two @unittest.expectedFailure pins in "
        "tools/test_harvest_duration_gate.py are removed."
    ),
}


def fail(msg):
    sys.exit(f"ABORT: {msg}")


def cell_of(asp, rk, z):
    try:
        return asp["regions"][rk]["resolved_by_zone"][z]
    except (KeyError, TypeError):
        fail(f"cell {rk} z{z} does not exist")


def main():
    write = "--write" in sys.argv

    raw = open(PATH, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        fail(f"canonical SHA {sha[:16]} != expected {EXPECT_SHA[:16]}")
    print(f"canonical SHA OK: {sha[:16]}")

    authored = json.load(open(STAGING, encoding="utf-8"))
    for k in ("harvest_stop_rule", "ramp_mature", "harvest_ready_beginner",
              "harvest_ready_seasoned", "cell_overrides", "cell_notes"):
        if k not in authored:
            fail(f"staging file is missing {k!r}")
    # cell_notes is load-bearing, not optional: a moved override with a stale note fires
    # OVERRIDE-PROSE. Refuse to run if the two maps have drifted apart in staging.
    if set(authored["cell_notes"]) - set(authored["cell_overrides"]):
        fail("staging cell_notes names a region with no cell_overrides entry")
    if set(EXPECT_CELL_NOTES) != {(rk, z) for rk, zs in authored["cell_notes"].items() for z in zs}:
        fail("staging cell_notes does not match this script's asserted pre-state set")

    data = json.loads(raw.decode("utf-8"))
    if len(data["crops"]) != 128:
        fail(f"crop count {len(data['crops'])} != 128")
    asps = [c for c in data["crops"] if c.get("slug") == "asparagus"]
    if len(asps) != 1:
        fail(f"expected exactly 1 asparagus crop, found {len(asps)}")
    asp = asps[0]

    # --- pre-state: assert every value this pass is about to overwrite -----------------------
    ramp = asp.get("harvest_ramp_weeks")
    if not isinstance(ramp, list):
        fail("harvest_ramp_weeks is not a list")
    mature = [e for e in ramp if isinstance(e, dict) and e.get("bed_year") == EXPECT_RAMP_BED_YEAR]
    if len(mature) != 1:
        fail(f"expected exactly 1 harvest_ramp_weeks entry with bed_year "
             f"{EXPECT_RAMP_BED_YEAR}, found {len(mature)}")
    if mature[0].get("weeks") != EXPECT_RAMP_WEEKS:
        fail(f"drift on harvest_ramp_weeks bed year {EXPECT_RAMP_BED_YEAR}\n"
             f"  have: {mature[0].get('weeks')!r}\n  want: {EXPECT_RAMP_WEEKS!r}")
    if max(e["bed_year"] for e in ramp if isinstance(e, dict)) != EXPECT_RAMP_BED_YEAR:
        fail(f"bed year {EXPECT_RAMP_BED_YEAR} is no longer the ramp's mature entry; "
             f"the RAMP-PROSE comparison would target a different year")

    for reg, want in (("harvest_ready_beginner", EXPECT_BEGINNER),
                      ("harvest_ready_seasoned", EXPECT_SEASONED)):
        if asp.get(reg) != want:
            fail(f"drift on {reg}\n  have: {asp.get(reg)!r}\n  want: {want!r}")

    if "harvest_stop_rule" in asp:
        fail("harvest_stop_rule already exists on asparagus; this pass creates it")

    for (rk, z), want in EXPECT_CELL_NOTES.items():
        have = cell_of(asp, rk, z).get("notes")
        if have != want:
            fail(f"drift on {rk} z{z} notes\n  have: {have!r}\n  want: {want!r}")

    for rk, zones in authored["cell_overrides"].items():
        for z in zones:
            cell = cell_of(asp, rk, z)
            if "harvest_duration_weeks" in cell:
                fail(f"{rk} z{z} already carries harvest_duration_weeks "
                     f"{cell['harvest_duration_weeks']!r}; this pass creates it")
    print(f"pre-state OK: ramp bed year {EXPECT_RAMP_BED_YEAR}, both harvest_ready registers, "
          f"{len(EXPECT_CELL_NOTES)} cell note(s), stop rule absent, override keys absent")

    # --- reference cells: stated duration matches the crop ramp, so no override is due -------
    for (rk, z), want in REFERENCE_CELLS.items():
        cell = cell_of(asp, rk, z)
        for k, v in want.items():
            if cell.get(k) != v:
                fail(f"reference cell {rk} z{z} drifted on {k}\n"
                     f"  have: {cell.get(k)!r}\n  want: {v!r}")
        if (rk, z) in {(a, b) for a, zs in authored["cell_overrides"].items() for b in zs}:
            fail(f"reference cell {rk} z{z} appears in cell_overrides; it must stay untouched")
    print(f"reference OK: {len(REFERENCE_CELLS)} control cells verified pre-apply")

    # --- apply -------------------------------------------------------------------------------
    asp["harvest_stop_rule"] = json.loads(json.dumps(authored["harvest_stop_rule"]))
    mature[0]["weeks"] = list(authored["ramp_mature"])
    asp["harvest_ready_beginner"] = authored["harvest_ready_beginner"]
    asp["harvest_ready_seasoned"] = authored["harvest_ready_seasoned"]

    n_ov = 0
    for rk, zones in authored["cell_overrides"].items():
        for z, weeks in zones.items():
            cell_of(asp, rk, z)["harvest_duration_weeks"] = list(weeks)
            n_ov += 1
    n_notes = 0
    for rk, zones in authored["cell_notes"].items():
        for z, note in zones.items():
            cell_of(asp, rk, z)["notes"] = note
            n_notes += 1
    print(f"applied: stop rule, ramp bed year {EXPECT_RAMP_BED_YEAR} -> "
          f"{authored['ramp_mature']}, 2 registers, {n_ov} override(s), {n_notes} note(s)")

    # --- post: the reference cells must be exactly where they started ------------------------
    for (rk, z), want in REFERENCE_CELLS.items():
        cell = cell_of(asp, rk, z)
        for k, v in want.items():
            if cell.get(k) != v:
                fail(f"reference cell {rk} z{z} was MODIFIED by this pass on {k}")
        if "harvest_duration_weeks" in cell:
            fail(f"reference cell {rk} z{z} gained a harvest_duration_weeks override")
    print(f"reference OK: {len(REFERENCE_CELLS)} control cells untouched post-apply")

    # --- post: no em dash anywhere this pass wrote --------------------------------------------
    written = [asp["harvest_ready_beginner"], asp["harvest_ready_seasoned"],
               asp["harvest_stop_rule"]["note_beginner"],
               asp["harvest_stop_rule"]["note_seasoned"]]
    written += [cell_of(asp, rk, z)["notes"] for rk, zs in authored["cell_notes"].items() for z in zs]
    for s in written:
        if "\u2014" in s:
            fail(f"em dash in consumer copy: {s[:60]!r}")

    # --- post: every invariant this arc shipped must return zero, BEFORE writing --------------
    sys.path.insert(0, "tools")
    from harvest_duration_gate import (
        duration_violations, ramp_violations, ramp_prose_violations, stop_rule_violations,
    )
    from zone_order_gate import zone_order_violations
    for name, fn in (("ramp_violations", ramp_violations),
                     ("ramp_prose_violations", ramp_prose_violations),
                     ("stop_rule_violations", stop_rule_violations),
                     ("duration_violations", duration_violations),
                     ("zone_order_violations", zone_order_violations)):
        residue = fn(asp)
        if residue:
            fail(f"{name} still fires after repair:\n  " + "\n  ".join(residue))
        print(f"invariant OK: {name} returns 0 on the repaired crop")

    vs = asp.setdefault("verification_status", {})
    findings = vs.setdefault("open_findings", [])
    findings.append(NEW_FINDING)
    print(f"open_findings: {len(findings) - 1} -> {len(findings)}")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        fail("trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        print(f"  harvest_stop_rule            ADDED (signal "
              f"{authored['harvest_stop_rule']['signal']!r})")
        print(f"  harvest_ramp_weeks[bed 5]    {EXPECT_RAMP_WEEKS} -> {authored['ramp_mature']}")
        print("  harvest_ready_beginner       REPLACED")
        print("  harvest_ready_seasoned       REPLACED")
        for rk, zones in authored["cell_overrides"].items():
            for z, weeks in zones.items():
                print(f"  {rk} z{z}".ljust(31) + f"harvest_duration_weeks = {list(weeks)}")
        for rk, zones in authored["cell_notes"].items():
            for z in zones:
                print(f"  {rk} z{z}".ljust(31) + "notes REPLACED (moves with the override)")
        print("  verification_status          +1 resolved open_findings entry")
        return

    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    new = hashlib.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new[:8]}")
    print(f"  full new SHA: {new}")


if __name__ == "__main__":
    main()
