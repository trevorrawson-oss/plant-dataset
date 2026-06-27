#!/usr/bin/env python3
"""Numeric-sanity truth-layer gate -- the deterministic first layer of the C7 defense
(whole_crop_gate A33; incognito-redteam 2026-06-27, Trevor: build deterministic first).

The cert suite validates SHAPE, never that a NUMBER is physically plausible, so the fabricated
"rutabaga that is basil verbatim" (C7) shipped days_to_maturity:[3,5], sunlight_hours:[0,1],
spacing_inches:[120,144] (tree spacing on an annual), ph:[3.0,3.4] -- all well-shaped, all absurd.
This bounds every key numeric to a PHYSICAL range; spacing is ARCHETYPE-AWARE (an annual at 120in is
absurd, a tree at 300in is normal). Bounds carry margin over the observed certified 18 (0 false
positives). It catches the EGREGIOUS / copy-template-don't-refit numeric -- the most likely bot
failure mode; the plausible-but-wrong value that contradicts the PROSE (a pH inside [3,10] vs a
6.0-7.5 prose claim) is the cross-consistency layer's job (truth-layer increment 2), not this one.

Bounds (observed-range -> chosen-bound, margin both sides):
  ph endpoints            4.0-8.0  -> [3.0, 10.0]   (soil pH physical band)
  days_to_maturity        10-120   -> [7, 400]      (nothing edible matures < 7 days)
  sunlight_hours          3-12     -> [1, 18]        (a crop needs >= 1h; indoor carries [] -> skip)
  germination_temp_f      35-95    -> [32, 110]
  variety chill_required  0-1050   -> [0, 2000]
  min/recommended_pot_gal 1-20     -> [1, 100]
  depth_inches_min        1-18     -> [1, 60]
  spacing_inches (annual) 2-48     -> [1, 72]   | (tree/woody) 48-300 -> [1, 360]
"""

# Non-tree spacing ceiling vs tree/woody spacing ceiling (the archetype split).
_TREE_BASES = {"perennial_chill_gated", "perennial_evergreen", "berries_woody"}


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _endpoints(v):
    """A numeric scalar -> [v]; a list of numbers -> the list; anything else -> None (skip)."""
    if _num(v):
        return [v]
    if isinstance(v, list) and v and all(_num(x) for x in v):
        return list(v)
    return None


def numeric_sanity_violations(crop):
    """Return a list ([] = clean) -- one per numeric field whose value(s) fall outside their
    physical bound. Skips absent / empty / non-numeric fields (presence is other gates' job; this
    only sanity-bounds what IS present and numeric)."""
    V = []
    basis = crop.get("calendar_basis")

    def check(value, label, lo, hi):
        pts = _endpoints(value)
        if pts is None:
            return  # absent / empty / non-numeric -> not this gate's concern
        bad = [x for x in pts if not (lo <= x <= hi)]
        if bad:
            V.append(f"{label} {value!r}: value(s) {bad} outside the physical bound [{lo}, {hi}]")

    ph = crop.get("ph") or {}
    check(ph.get("preferred_range"), "ph.preferred_range", 3.0, 10.0)
    check(ph.get("tolerated_range"), "ph.tolerated_range", 3.0, 10.0)
    check(crop.get("days_to_maturity"), "days_to_maturity", 7, 400)
    check(crop.get("sunlight_hours"), "sunlight_hours", 1, 18)
    check(crop.get("germination_temp_f"), "germination_temp_f", 32, 110)

    cn = crop.get("container_notes") or {}
    check(cn.get("min_pot_gallons"), "container_notes.min_pot_gallons", 1, 100)
    check(cn.get("recommended_pot_gallons"), "container_notes.recommended_pot_gallons", 1, 100)
    check(cn.get("depth_inches_min"), "container_notes.depth_inches_min", 1, 60)

    # spacing is ARCHETYPE-AWARE: a non-tree (annual/herbaceous/woody-ornamental subshrub) above
    # ~6ft is absurd; a fruit tree legitimately reaches 25ft (300in). Indoor carries [] -> skipped.
    sp_hi = 360 if basis in _TREE_BASES else 72
    check(crop.get("spacing_inches"), f"spacing_inches (basis={basis})", 1, sp_hi)

    # per-variety chill (numeric form only; A21/A22 own the type lock)
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            check(v.get("chill_hours_required"),
                  f"varieties.recommended[{i}].chill_hours_required", 0, 2000)

    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        vs = numeric_sanity_violations(c)
        if vs:
            print(f"  {c.get('slug')} ({c.get('calendar_basis')}):")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"numeric_sanity gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
