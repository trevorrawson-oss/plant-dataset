#!/usr/bin/env python3
"""planting_layout_gate -- validates the conditional planting_layout field (spec 2026-07-10).

Fields (crop-level):
  planting_layout : enum {block, row, hill, grid, single}. Present ONLY where a crop has a
                    non-default spatial planting pattern the app should render; ABSENT (not null)
                    on every crop that uses standard row spacing. Corn is the only 'block' member
                    (wind pollination -> plant a block of short rows, not one long row).
  pollination_block_min_rows : int >= 2, present IFF planting_layout == 'block' (corn = 4).

Checks (HARD, fire ONLY when planting_layout is present -- unauthored roster stays green; ABSENCE is
never a violation, matching the divide_every_years / chill conditional-field precedent):
  - planting_layout enum membership.
  - block <-> pollination_block_min_rows coherence: 'block' requires the int (>= 2); any non-'block'
    value requires min_rows ABSENT; an orphan min_rows with no layout bounces.

The other enum values (row/hill/grid/single) are DEFINED but unpopulated in this roster -- reserved
for the future garden-planner arc (memory planner-data-model-arc), which takes planting_layout
roster-wide and adds row_spacing + height. NOT an A39 register field (stays conditional).

Usage:
  planting_layout_gate.py [PATH]        # validate (default crops_data_final.json)
  planting_layout_gate.py --coverage    # coverage report + validate
"""
import json
import sys

LAYOUTS = {"block", "row", "hill", "grid", "single"}
MIN_ROWS_FLOOR = 2


def check_crop(c):
    """Return list of violation strings for one crop (empty == clean). No-op off scope."""
    slug = c.get("slug") or c.get("id")
    v = []
    pl = c.get("planting_layout")
    has_mr = "pollination_block_min_rows" in c
    mr = c.get("pollination_block_min_rows")

    # --- no-op off scope: field absent or null ---
    if not c.get("planting_layout"):
        if has_mr and mr is not None:
            v.append(f"{slug}: pollination_block_min_rows present but planting_layout absent/null")
        return v

    # --- enum membership ---
    if pl not in LAYOUTS:
        v.append(f"{slug}: planting_layout {pl!r} not in {sorted(LAYOUTS)}")
        return v  # cannot reason about coherence on a bad enum

    # --- block <-> min_rows coherence ---
    if pl == "block":
        if not has_mr or mr is None:
            v.append(f"{slug}: planting_layout 'block' but pollination_block_min_rows missing")
        elif isinstance(mr, bool) or not isinstance(mr, int) or mr < MIN_ROWS_FLOOR:
            v.append(f"{slug}: pollination_block_min_rows {mr!r} not an int >= {MIN_ROWS_FLOOR}")
    else:
        if has_mr and mr is not None:
            v.append(f"{slug}: planting_layout {pl!r} (not 'block') but pollination_block_min_rows present")
    return v


def coverage(crops):
    cov = {k: [] for k in LAYOUTS}
    cov["absent"] = []
    for c in crops:
        slug = c.get("slug") or c.get("id")
        pl = c.get("planting_layout")
        if not pl:
            cov["absent"].append(slug)
        elif pl in cov:
            cov[pl].append(slug)
        else:
            cov["absent"].append(slug)  # bad value: check_crop flags shape; not counted here
    return cov


def main():
    args = list(sys.argv[1:])
    show_cov = "--coverage" in args
    args = [a for a in args if a != "--coverage"]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    violations = []
    for c in crops:
        violations += check_crop(c)

    if show_cov:
        cov = coverage(crops)
        print(f"COVERAGE (of {len(crops)} crops):")
        print("  planting_layout: " + " | ".join(
            f"{k} {len(cov[k])}" for k in ["block", "row", "hill", "grid", "single", "absent"]))
        for k in ["block", "row", "hill", "grid", "single"]:
            if cov[k]:
                print(f"    {k}: {sorted(cov[k])}")

    if violations:
        print(f"\nplanting_layout_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nplanting_layout_gate: PASS (0 violations)")
    sys.exit(0)


if __name__ == "__main__":
    main()
