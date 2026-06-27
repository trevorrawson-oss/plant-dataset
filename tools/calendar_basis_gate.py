#!/usr/bin/env python3
"""calendar_basis enum guard -- the dispatch-key validator (whole_crop_gate A30).

incognito-redteam C1 (2026-06-27): `calendar_basis` is THE field the whole calendar layer
dispatches on. Every calendar gate no-ops itself with a string-equality check against it:
  - A3/A4   perennial      (perennial_chill_gated / perennial_evergreen)
  - A5/A24/A28 annual       (frost_anchored)
  - A9      photoperiod     (off frost_anchored)
  - A10/A11 berries_herbaceous (perennial_herbaceous)
  - A13/A14 woody_ornamental (perennial_woody_ornamental)
  - A15/A16 berries_woody   (berries_woody)
  - A6      indoor          (non_seasonal_indoor)
...and NOTHING validated the field itself. A typo ("frost_anchored "), a case slip
("Frost_anchored"), a synonym ("annual"), or a novel value ("generic_placeholder", the live
heirloom-tomato shell) silently disabled the crop's ENTIRE calendar layer -- the suite still
printed GATE: PASS because every dispatch-keyed gate quietly returned []. This guard makes the
dispatch honest: a calendar_basis outside the known set is a hard cert violation.

This is the SINGLE SOURCE OF TRUTH for the valid archetype bases. (perennial_gate.PERENNIAL_BASES
is the perennial subset; photoperiod/annual gates key on "frost_anchored"; etc.)
"""

# The 7 certified archetype bases (cert anchors as of 2026-06-26, SHA 512e5a8d):
#   frost_anchored             -- annuals (tomato/carrot/.../zinnia) + onion (photoperiod rides it)
#   perennial_chill_gated      -- deciduous fruit trees (peach, apple)
#   perennial_evergreen        -- citrus / evergreen fruit trees (lemon, orange-navel)
#   perennial_herbaceous       -- herbaceous perennials (strawberry / berries_herbaceous)
#   berries_woody              -- woody fruiting shrubs (blueberry)
#   perennial_woody_ornamental -- woody ornamental subshrubs (lavender)
#   non_seasonal_indoor        -- indoor year-round (microgreens / sprouts)
# EXTEND this set ONLY when a new archetype is certified (and add its dispatch gates).
VALID_CALENDAR_BASES = {
    "frost_anchored",
    "perennial_chill_gated",
    "perennial_evergreen",
    "perennial_herbaceous",
    "berries_woody",
    "perennial_woody_ornamental",
    "non_seasonal_indoor",
}


def calendar_basis_violations(crop):
    """Return a list ([] = clean) -- one violation if calendar_basis is not a known base.
    A missing/null/typo/case-slip/synonym/novel value all fail: the crop's calendar layer
    would otherwise be validated by nothing (every calendar gate dispatches on this field)."""
    cb = crop.get("calendar_basis")
    if cb in VALID_CALENDAR_BASES:
        return []
    return [f"calendar_basis {cb!r} is not a known base {sorted(VALID_CALENDAR_BASES)}; an "
            f"unknown/typo/case-slip/novel basis silently no-ops EVERY calendar gate "
            f"(A3/A4/A5/A6/A9/A10/A11/A13/A14/A15/A16/A24/A28), so the crop's whole calendar "
            f"layer would be validated by nothing"]


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in calendar_basis_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
    print(f"calendar_basis gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
