#!/usr/bin/env python3
"""Perennial planting-data floor (whole_crop_gate A47, 2026-07-25).

THE DEFECT THIS EXISTS TO CATCH. Asparagus certified 120/120 while carrying NO `plant_out`
on any of its 39 zone cells -- the app could not tell a grower when to set crowns. The cert
plan deliberately omitted the field ("an established permanent bed is planted once, so an
annual planting window would misrepresent it") and designated `start_method`/`year_one_notes`
as the new home for the crown window. That home was never built: `start_method` carries no
timing and `year_one_notes` was never authored on the crop. The timing was moved out of the
calendar and then landed nowhere.

Nothing caught it because `plant_out` is OPTIONAL: A24/A43 and the annual-calendar layer all
go VACUOUS when the field is absent, so removing it silently removes its own enforcement.
A gate that only validates a field's SHAPE cannot notice the field's ABSENCE.

THE INVARIANT. Every one of the other 37 perennials already carries `plant_out` on 100% of
its calendared cells -- apple (a 30-year tree planted exactly once) states
`"Apr - May (dormant, bare-root)"`. For a perennial, `plant_out` means the ESTABLISHMENT
window, not an annual replant; the parenthetical carries the one-time framing. So this is a
convention the roster already observes universally and never enforced. Measured 2026-07-25:
asparagus was the ONLY violator (39/39 cells). Zero flood on the other 119 certified crops.

SCOPE. Keys on `perennial is True` -- the field the dataset publishes directly and
herbaceous_perennial_gate rule 1 hard-enforces -- NOT on calendar_basis. calendar_basis
selects which CALENDAR VALIDATION MACHINERY applies (asparagus rides frost_anchored on
purpose, per calendar_basis_gate's archetype->basis map); it is not a perennial-ness signal.
Deriving perennial-ness from it misclassifies 9 crops (chives, mint, lemongrass, echinacea,
bee-balm, artichoke, asparagus, avocado, olive).

TWO EXEMPTIONS, both load-bearing:
  - EMPTY CALENDAR -> skip. An unfilled shell cell (artichoke/avocado/olive: 20 cells, 0
    calendared) is an admission state, not a defect. Matches herbaceous_perennial_gate's
    own `suit is None and not cal` admission branch.
  - suitability == "unsuitable" -> skip. Those cells carry an honest all-`growing` calendar
    under the A32 honesty floor, but telling someone WHEN to plant a crop that will not grow
    there is worse than silence. Asparagus has 13 such cells.
"""
SKIP_SUITABILITY = {"unsuitable"}


def perennial_plant_out_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless crop.perennial is True."""
    if crop.get("perennial") is not True:
        return []
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            if not (cell.get("calendar") or []):
                continue  # unfilled shell cell -- admission state, not a defect
            if cell.get("suitability") in SKIP_SUITABILITY:
                continue  # never tell a grower when to plant what will not grow there
            if not cell.get("plant_out"):
                V.append(f"{rk}.{z}: a calendared perennial cell must carry plant_out (the "
                         f"ESTABLISHMENT window, e.g. 'Apr - May (dormant, bare-root)'); the "
                         f"app has no way to tell a grower when to plant")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    crops_hit = set()
    for c in data["crops"]:
        for v in perennial_plant_out_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
            crops_hit.add(c.get("slug"))
    print(f"perennial plant_out gate: {total} violation(s) across "
          f"{len(crops_hit)} crop(s) / {len(data['crops'])} scanned")
    sys.exit(1 if total else 0)
