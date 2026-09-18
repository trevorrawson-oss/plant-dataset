#!/usr/bin/env python3
"""plant_dimensions_gate -- A59: the crop-level plant-dimension fields (PLA-465 spec 2026-09-16, section 4).

FIELDS (crop top level, register row 30, presence-or-null on every certified crop):
  mature_height_ft   [lo, hi] feet, numbers, 0 < lo <= hi   -- the size a grower should expect on the
  mature_spread_ft   [lo, hi] feet, numbers, 0 < lo <= hi      recommended rootstock, or on own roots
  footprint_inches   positive number, and strictly below spacing_inches[0] when spacing is present
                     (the plant's own width at the ground; PLA-429's slot, authored by nobody yet)

SHAPE fires only when a field is non-null (A39 owns presence), so it arms GREEN on any state that
carries no values. PROVENANCE: a non-null height or spread on a CERTIFIED crop must be backed by a
verification_status.field_additions[] entry with field == "plant_dimensions" (the amend-not-recert
convention the timing-spine and pet_safe passes use), so a later authoring cannot skip the record.
PRESENCE (a certified crop carries all three keys, null being a value) is behind --presence here and
behind A59_PRESENCE_ARMED in whole_crop_gate, flipped in the SAME commit that writes the canonical
carrying the keys, never before (gates arm off the data).

COVERAGE (a woody crop's null must be cane-fruit N/A or explained by a record naming the field) is behind
--presence's sibling --coverage here and behind A59_COVERAGE_ARMED in whole_crop_gate.

Usage:
  plant_dimensions_gate.py [PATH] [--presence] [--coverage]
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berries_woody_gate import _is_cane_fruit  # the sub-form router, IMPORTED, never re-encoded

FIELDS = ("mature_height_ft", "mature_spread_ft", "footprint_inches")
RANGE_FIELDS = ("mature_height_ft", "mature_spread_ft")
CERTIFIED = "verified_gs_arc"
PROVENANCE_FIELD = "plant_dimensions"


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _has_provenance(crop):
    fa = (crop.get("verification_status") or {}).get("field_additions") or []
    return any(isinstance(x, dict) and x.get("field") == PROVENANCE_FIELD for x in fa)


def shape_violations(crop):
    V = []
    slug = crop.get("slug") or "?"
    authored = False
    for f in RANGE_FIELDS:
        v = crop.get(f)
        if v is None:
            continue
        authored = True
        if not (isinstance(v, list) and len(v) == 2 and all(_num(x) for x in v)):
            V.append(f"{slug}: {f} must be a list of two numbers [lo, hi], got {v!r}")
            continue
        lo, hi = v
        if lo <= 0 or hi <= 0:
            V.append(f"{slug}: {f} bounds must be positive, got {v!r}")
        elif lo > hi:
            V.append(f"{slug}: {f} must satisfy lo <= hi, got {v!r}")
    fp = crop.get("footprint_inches")
    if fp is not None:
        if not _num(fp) or fp <= 0:
            V.append(f"{slug}: footprint_inches must be a positive number, got {fp!r}")
        else:
            sp = crop.get("spacing_inches")
            if isinstance(sp, list) and sp and _num(sp[0]) and fp >= sp[0]:
                V.append(f"{slug}: footprint_inches {fp!r} must be strictly below spacing_inches[0] {sp[0]!r}")
    if authored and _certified(crop) and not _has_provenance(crop):
        V.append(f"{slug}: authored plant dimensions on a certified crop with no field_additions entry for {PROVENANCE_FIELD!r}")
    return V


def presence_violations(crop):
    if not _certified(crop):
        return []
    slug = crop.get("slug") or "?"
    return [f"{slug}: {f} missing (present-or-null on a certified crop)" for f in FIELDS if f not in crop]


# WOODY archetypes: the population PLA-465 R1 authors. A null height here is a decision, not a blank.
WOODY_ARCHETYPES = ("deciduous_fruit_tree", "evergreen_fruit_tree", "berries_woody", "woody_ornamental")


def _explained(crop, field):
    """True if some open_findings summary NAMES the field. Field-named, never session- or date-named, so a
    later null-ruling on any field generalizes without touching this gate."""
    of = (crop.get("verification_status") or {}).get("open_findings") or []
    return any(field in (x.get("summary") or "") for x in of if isinstance(x, dict))


def coverage_violations(crop):
    """A certified WOODY crop may carry a null mature_height_ft only if it is CANE FRUIT (biennial canes
    whose every published height is a managed tipping or trellis height, so a mature height is not a
    property of the plant) or if a verification_status record EXPLAINS the null by naming the field.

    This makes the PLA-465 promote-2 rulings load-bearing: the twelve nulls each carry a recorded reason,
    and a thirteenth null cannot appear silently. The cane predicate is IMPORTED from berries_woody_gate
    (the sub-form router), never re-encoded: cane_type is non-null on FOUR crops with three different
    meanings, so "cane_type is set" is NOT the predicate -- blueberry carries 'not_applicable' (bush) and
    elderberry 'multistem_perennial' (shrub), and both legitimately carry a height.

    MEASURED 2026-09-18: on today's canonical the cane branch is REDUNDANT, because PLA-465 promote 2 gave
    raspberry and blackberry records that name the field too, so removing the branch leaves the gate green.
    It is kept because it is REACHABLE and says something the records do not: a cane fruit is N/A
    permanently, where a record is a deferral. A cane crop certified without a record (the next berry) is
    exempt by the predicate alone, which the unit test drives in isolation. Do not read the branch as
    load-bearing on the current data.
    """
    if not _certified(crop) or crop.get("archetype") not in WOODY_ARCHETYPES:
        return []
    if crop.get("mature_height_ft") is not None:
        return []
    if _is_cane_fruit(crop):
        return []
    if _explained(crop, "mature_height_ft"):
        return []
    slug = crop.get("slug") or "?"
    return [f"{slug}: mature_height_ft is null on a woody crop and no record names the field "
            f"(author it, or record why it stays null)"]


def all_violations(data, presence=False, coverage=False):
    V = []
    for c in data.get("crops", []):
        V += shape_violations(c)
        if presence:
            V += presence_violations(c)
        if coverage:
            V += coverage_violations(c)
    return V


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    path = args[0] if args else "crops_data_final.json"
    presence = "--presence" in argv
    coverage = "--coverage" in argv
    with open(path) as fh:
        data = json.load(fh)
    V = all_violations(data, presence=presence, coverage=coverage)
    for v in V:
        print("VIOLATION:", v)
    carrying = sum(1 for c in data["crops"] if all(f in c for f in FIELDS))
    authored = sum(1 for c in data["crops"] if any(c.get(f) is not None for f in FIELDS))
    print(f"plant_dimensions_gate: {len(V)} violation(s); {carrying}/{len(data['crops'])} crops carry the keys, "
          f"{authored} authored; presence {'ARMED' if presence else 'off'}; coverage {'ARMED' if coverage else 'off'}")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
