#!/usr/bin/env python3
"""Release-lane FILL pass: generate every berries_woody cell's calendar[] from its leaf_habit +
window dates (blueberry, anchor 18). The tree-calendar discipline -- claude.ai authors the DATES,
Claude Code GENERATES the derived array so it cannot drift; whole_crop_gate A16 then checks
coherence. A cell whose windows are not yet authored (deriver -> None) is left [] (the admission
state). No-op off berries_woody. Mirrors derive_berry_calendars / derive_woody_ornamental_calendars.

Usage:
  python3 tools/derive_berry_woody_calendars.py <slug> [in.json] [out.json]
    in  default crops_data_final.json ; out default = in (in place). Reports filled/skipped.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_woody_calendar import derive_berry_woody_calendar


def fill_berry_woody_calendars(crop):
    """Fill calendar[] on every resolved cell of a berries_woody crop via the deriver.
    Returns (filled, skipped) lists of "<region>.<zone>" keys. Idempotent + no-op off-basis."""
    if crop.get("calendar_basis") != "berries_woody":
        return [], []
    filled, skipped = [], []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            cal = derive_berry_woody_calendar(cell.get("leaf_habit"), cell)
            if cal is None:
                skipped.append(f"{rk}.{z}")
            else:
                cell["calendar"] = cal
                filled.append(f"{rk}.{z}")
    return filled, skipped


def main():
    slug = sys.argv[1]
    inp = sys.argv[2] if len(sys.argv) > 2 else "crops_data_final.json"
    out = sys.argv[3] if len(sys.argv) > 3 else inp
    data = json.load(open(inp))
    crop = next(c for c in data["crops"] if c.get("slug") == slug)
    filled, skipped = fill_berry_woody_calendars(crop)
    # canonical compact form (separators, no trailing newline, ensure_ascii=False)
    with open(out, "w") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print(f"filled {len(filled)} calendar(s): {filled}")
    print(f"skipped {len(skipped)} (admission/no-window): {skipped}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
