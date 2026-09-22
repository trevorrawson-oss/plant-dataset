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
  variety days_to_maturity 21-140  -> [7, 400]     (per-cultivar DTM, bounded like the crop number)
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


def _plants_per_pot_readings(cn):
    """The readings under container_notes.plants_per_pot, or [] (PLA-580, register row 31).

    DELIBERATELY RETYPED rather than imported. This module has NO module-level imports at all --
    five other modules import it, and keeping it dependency-free is why. The retype is the risk
    "import a gate's table, never retype it" warns about, so the agreement with
    plants_per_pot_gate.readings_of is MEASURED in test_plants_per_pot_gate.NumericSanityAgreement
    over the whole value domain, rather than assumed. If you change one, that test fails.
    """
    v = cn.get("plants_per_pot")
    if not isinstance(v, dict):
        return []
    rs = v.get("readings")
    if not isinstance(rs, list):
        return []
    return [r for r in rs if isinstance(r, dict)]


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

    # plants_per_pot (PLA-580, register row 31): a per-pot capacity and the pot size it was
    # measured at. THE 0.5 FLOOR ON at_gallons IS DELIBERATE and differs from the 1..100 that
    # min_pot_gallons and recommended_pot_gallons carry two lines above, because Illinois Extension
    # publishes a HALF-GALLON row ("Half-gallon containers | parsley | 1 plant"). Do NOT "fix" it
    # to 1 to match its neighbours; test_plants_per_pot_gate pins both floors so neither drifts
    # onto the other. The count ceiling of 30 is a sanity bound, not a capacity claim.
    for _i, _r in enumerate(_plants_per_pot_readings(cn)):
        check(_r.get("count"), f"container_notes.plants_per_pot[{_i}].count", 1, 30)
        check(_r.get("at_gallons"), f"container_notes.plants_per_pot[{_i}].at_gallons", 0.5, 100)

    # spacing is ARCHETYPE-AWARE: a non-tree (annual/herbaceous/woody-ornamental subshrub) above
    # ~6ft is absurd; a fruit tree legitimately reaches 25ft (300in). Indoor carries [] -> skipped.
    sp_hi = 360 if basis in _TREE_BASES else 72
    check(crop.get("spacing_inches"), f"spacing_inches (basis={basis})", 1, sp_hi)

    # plant dimensions (PLA-465, register row 30) are ARCHETYPE-AWARE the same way: a tree base may
    # reach 120 ft tall / 80 ft wide (a standard mulberry is 30-60); anything else above 20 ft is absurd
    # (a rosemary at 6, a sunflower at 12, pole beans on a trellis at 10 all fit). footprint_inches is
    # the plant's own width at the ground, never a canopy.
    h_hi, w_hi = (120, 80) if basis in _TREE_BASES else (20, 20)
    check(crop.get("mature_height_ft"), f"mature_height_ft (basis={basis})", 0.1, h_hi)
    check(crop.get("mature_spread_ft"), f"mature_spread_ft (basis={basis})", 0.1, w_hi)
    check(crop.get("footprint_inches"), "footprint_inches", 0.5, 60)

    # per-variety numerics: chill (A21/A22 own the type lock) + a per-variety days_to_maturity, which
    # refines the crop's DTM per cultivar and must be bounded the SAME as the crop-level number -- A33
    # bounded the crop DTM but never the variety DTM, so a fabricated variety (3-day / 500-day) slipped.
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if isinstance(v, dict):
            check(v.get("chill_hours_required"),
                  f"varieties.recommended[{i}].chill_hours_required", 0, 2000)
            check(v.get("days_to_maturity"),
                  f"varieties.recommended[{i}].days_to_maturity", 7, 400)

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
