#!/usr/bin/env python3
"""Prose drift, instances 8 and 9: notes that contradict THEMSELVES as well as their field.

  ca_interior z8  note "harvest March into April for eight to ten weeks"  field "Mar - May"
  nevada      z8  note "harvest March into April for eight to ten weeks"  field "Mar - May"

These two are unambiguous because the sentence disagrees with ITSELF: eight to ten weeks from a
March start lands in MAY, not April. The duration figure is the well-sourced one (California's
mature 8-10 weeks, four independent UC corroborations), so the month phrase is the wrong half and
the field is right. Only the month phrase moves.

DELIBERATELY NOT INCLUDED -- utah_dixie z8. Its note reads "harvest through March and April for
six to eight weeks" against a "Mar - May" field, which LOOKS like the same defect and is not. Six
to eight weeks from a March start reaches late April, not May, so its note is internally
CONSISTENT and it is the FIELD that may be over-extended. That makes it the same class as
mid_south z7 (where MU G6405 states "April 14 to May 30 in southern Missouri" against an
"Apr - Jun" field), and it belongs to the duration pass, not this one. Patching its prose to match
the field would be the ca_desert error in reverse: silencing the half that is telling the truth.

Usage: python3 tools/promote_prose_drift_fix2.py [--write]
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "ff3307615765e266a9ca291cf95977c5c6d28a31480d54f97dddc44a3054379e"

EDITS = {
    ("ca_interior", "8"): (
        "harvest March into April for eight to ten weeks",
        "harvest March into May for eight to ten weeks",
    ),
    ("nevada", "8"): (
        "harvest March into April for eight to ten weeks",
        "harvest March into May for eight to ten weeks",
    ),
}

NEW_FINDING = {
    "severity": "low",
    "blocks_launch": False,
    "status": "resolved",
    "finding": (
        "PROSE DRIFT instances 8-9, repaired 2026-07-27: ca_interior z8 and nevada z8 both read "
        "'harvest March into April for eight to ten weeks' against a 'Mar - May' field. Each "
        "sentence contradicted ITSELF -- eight to ten weeks from March lands in May -- so the "
        "month phrase was the wrong half and the field was right. Month phrase only. "
        "OPENED, NOT CLOSED, BY THE SAME SCAN: five cells state a duration that implies an "
        "EARLIER end than their field claims (mid_atlantic z7 Rutgers-6-weeks vs 'Apr - Jun'; "
        "mid_south z7, where MU G6405 states outright 'April 14 to May 30 in southern Missouri' "
        "against 'Apr - Jun'; northern_tier z7; utah_dixie z8; se_gulf z8). Those were "
        "deliberately NOT patched, because there the PROSE may be the correct half and editing "
        "it would destroy the evidence. Underlying shape: 24 of 29 renderable cells are now "
        "EXACTLY three calendar months, the same uniformity signature as the original defect "
        "where all 29 were exactly two. Three months is right where the sourced duration is "
        "8-10 weeks and too long where it is 4-6 or 6-8. Queued as its own duration pass. "
        "mid_atlantic z7 additionally carries a genuine source disagreement (Rutgers FS1301 '6 "
        "weeks during the fifth and subsequent seasons' vs UMD '8 to 10 weeks per year', both "
        "cited on the same cell), which must CARRY THE RANGE rather than pick a side."
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
    asp = [c for c in data["crops"] if c.get("slug", "").startswith("asparagus")][0]

    def snapshot():
        return {(rk, z): (c.get("harvest"), c.get("plant_out"), tuple(c.get("calendar") or ()),
                          c.get("suitability"))
                for rk, r in asp["regions"].items()
                for z, c in (r.get("resolved_by_zone") or {}).items()}

    before = snapshot()
    for (rk, z), (old, new) in EDITS.items():
        cell = asp["regions"][rk]["resolved_by_zone"][z]
        note = cell.get("notes") or ""
        if old not in note:
            sys.exit(f"ABORT: phrase not found in {rk}.z{z}: {old!r}")
        cell["notes"] = note.replace(old, new, 1)
        print(f"  edited {rk}.z{z}")
    if before != snapshot():
        sys.exit("ABORT: a field value moved in a notes-only pass")
    print("invariant OK: every harvest/plant_out/calendar/suitability value byte-identical")

    for (rk, z) in EDITS:
        n = asp["regions"][rk]["resolved_by_zone"][z]["notes"]
        if "into April" in n:
            sys.exit(f"ABORT: {rk}.z{z} still claims 'into April'")
        if "—" in n or "--" in n:
            sys.exit(f"ABORT: em dash in consumer copy at {rk}.z{z}")
    print("invariant OK: repaired notes clean, no em dashes")

    # utah_dixie z8 must be left ALONE by this pass
    ud = asp["regions"]["utah_dixie"]["resolved_by_zone"]["8"]["notes"]
    if "through March and April for six to eight weeks" not in ud:
        sys.exit("ABORT: utah_dixie z8 was modified; it belongs to the duration pass")
    print("invariant OK: utah_dixie z8 deliberately untouched (duration pass)")

    asp.setdefault("verification_status", {}).setdefault("open_findings", []).append(NEW_FINDING)
    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        sys.exit("ABORT: trailing newline")
    if not write:
        print("\nDRY RUN -- re-run with --write")
        return
    open(PATH, "w", encoding="utf-8", newline="").write(out)
    print(f"\nWRITTEN. canonical {sha[:8]} -> {hashlib.sha256(open(PATH,'rb').read()).hexdigest()[:8]}")


if __name__ == "__main__":
    main()
