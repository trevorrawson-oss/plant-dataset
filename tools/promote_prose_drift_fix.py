#!/usr/bin/env python3
"""Repair three asparagus cell notes that contradict their own harvest fields.

PROSE-VS-DATA DRIFT, instances five, six and seven on this crop. The 2026-07-27 harvest
re-source corrected 22 of 29 harvest windows and repaired 11 cell notes that still described
the old values. These three survived that sweep, and a fourth (ca_desert z9) was repaired
earlier today. The data is correct in every case; the consumer-facing prose is not, which means
a reader is told one thing by the note and another by the calendar.

  ca_north_coast z9   note "harvest March into April"                field "Mar - May"
  ca_north_coast z10  note "harvest March into April"                field "Mar - May"
  warm_arid      z8   note "March and April for six to eight weeks"  field "Mar - May"

warm_arid z8 carries a SECOND error inside the same clause. "Six to eight weeks" is NMSU
H-227's year-two-and-three figure; the same page says "From year four on, harvest a maximum of
10 weeks/year." The field correctly encodes the mature window (early March plus ten weeks lands
mid-May); only the note was wrong. Its replacement also carries H-227's stop rule -- "When
average spear groundline diameter declines to 1/4 in., harvest should be stopped" -- because a
ten-week number published without the rule that governs it is the exact gap flagged in
docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md §3.2.

NO FIELD VALUES CHANGE. This pass edits `notes` strings only. Verified by asserting every
harvest/plant_out/calendar value is byte-identical after the write.

Usage: python3 tools/promote_prose_drift_fix.py [--write]
Dry-run by default. Aborts on ANY drift from the expected pre-state.
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "9fe9e33eb4603db9f7e3344059d0f275469ba92424cd6a8aa18423991d96c56a"

EDITS = {
    ("ca_north_coast", "9"): (
        "On the cool north-coast strip spears emerge in March; harvest March into April, then "
        "carry the ferns through a mild summer.",
        "On the cool north-coast strip spears emerge in March; harvest March into May, then "
        "carry the ferns through a mild summer.",
    ),
    ("ca_north_coast", "10"): (
        "In the nearly frost-free bayside pockets spears come in March; harvest March into "
        "April, then run the ferns through a cool summer.",
        "In the nearly frost-free bayside pockets spears come in March; harvest March into "
        "May, then run the ferns through a cool summer.",
    ),
    ("warm_arid", "8"): (
        "spears emerge in March as the soil warms, so harvest through March and April for six "
        "to eight weeks, then let the ferns grow through the long hot summer",
        "spears emerge in March as the soil warms, so harvest from March into mid May, up to "
        "about ten weeks once the bed is four years old, and stop when the spears thin toward a "
        "quarter inch. Then let the ferns grow through the long hot summer",
    ),
}

NEW_FINDING = {
    "severity": "medium",
    "blocks_launch": False,
    "status": "resolved",
    "finding": (
        "PROSE-VS-DATA DRIFT, instances 5-7, repaired 2026-07-27. A systematic scan of all 29 "
        "renderable asparagus cells compared each note's month claims against its own harvest "
        "field and found three survivors of the re-source pass's 11-note repair: "
        "ca_north_coast z9 and z10 both read 'harvest March into April' against a 'Mar - May' "
        "field, and warm_arid z8 read 'March and April for six to eight weeks' against "
        "'Mar - May'. warm_arid z8 carried a second error in the same clause: 'six to eight "
        "weeks' is NMSU H-227's year-2-and-3 figure, while the same page states 'From year four "
        "on, harvest a maximum of 10 weeks/year'; its replacement now carries the mature figure "
        "AND H-227's stop rule ('When average spear groundline diameter declines to 1/4 in., "
        "harvest should be stopped'). NO field values changed. THE PATTERN, now seven instances "
        "on one crop: prose is a separate consumer-facing layer that no gate reads, and every "
        "single instance has been found by hand. A34/A36/A29 check that notes EXIST and are "
        "dual-register; nothing checks what they SAY. This is the strongest evidence yet for "
        "hardening item 1. ALSO CONFIRMED CLEAN in the same scan, so the crop is not "
        "systematically drifted: harvest-string vs calendar-token agreement 29/29, harvest "
        "zone-ordering 0 (new zone_order_gate), window lengths all within the sourced 2-3 month "
        "norm, and warm_arid z8's 'sourced start' claim independently verified against H-227 "
        "('the New Mexico asparagus harvest season begins in southern New Mexico in early "
        "March')."
    ),
}


def main():
    write = "--write" in sys.argv
    raw = open(PATH, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        sys.exit(f"ABORT: canonical SHA {sha[:16]} != expected {EXPECT_SHA[:16]}")
    print(f"canonical SHA OK: {sha[:16]}")

    data = json.loads(raw.decode("utf-8"))
    asp = [c for c in data["crops"] if c.get("slug", "").startswith("asparagus")]
    if len(asp) != 1:
        sys.exit(f"ABORT: expected 1 asparagus, found {len(asp)}")
    asp = asp[0]

    # snapshot every timing value so we can prove none moved
    def snapshot():
        out = {}
        for rk, r in asp["regions"].items():
            for z, c in (r.get("resolved_by_zone") or {}).items():
                out[(rk, z)] = (c.get("harvest"), c.get("plant_out"),
                                tuple(c.get("calendar") or ()), c.get("suitability"))
        return out

    before = snapshot()

    for (rk, z), (old, new) in EDITS.items():
        cell = asp["regions"][rk]["resolved_by_zone"][z]
        note = cell.get("notes") or ""
        if old not in note:
            sys.exit(f"ABORT: expected phrase not found in {rk}.z{z}\n  want: {old!r}\n  have: {note!r}")
        cell["notes"] = note.replace(old, new, 1)
        print(f"  edited {rk}.z{z}")

    after = snapshot()
    if before != after:
        diff = [k for k in before if before[k] != after[k]]
        sys.exit(f"ABORT: field values moved (notes-only pass): {diff}")
    print("invariant OK: every harvest/plant_out/calendar/suitability value byte-identical")

    # prose must now agree with the fields
    for (rk, z) in EDITS:
        note = asp["regions"][rk]["resolved_by_zone"][z]["notes"]
        if "into April" in note and asp["regions"][rk]["resolved_by_zone"][z]["harvest"] == "Mar - May":
            sys.exit(f"ABORT: {rk}.z{z} still says 'into April' against a Mar - May field")
    print("invariant OK: no repaired note still claims the old window")

    # consumer-copy rules
    for (rk, z) in EDITS:
        note = asp["regions"][rk]["resolved_by_zone"][z]["notes"]
        if "—" in note or "--" in note:
            sys.exit(f"ABORT: em dash / double hyphen in consumer copy at {rk}.z{z}")
    print("invariant OK: no em dashes in the repaired consumer copy")

    vs = asp.setdefault("verification_status", {})
    findings = vs.setdefault("open_findings", [])
    findings.append(NEW_FINDING)
    print(f"open_findings: {len(findings) - 1} -> {len(findings)}")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        sys.exit("ABORT: trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        return
    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    new_sha = hashlib.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new_sha[:8]}")


if __name__ == "__main__":
    main()
