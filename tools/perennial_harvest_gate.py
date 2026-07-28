#!/usr/bin/env python3
"""Herbaceous-perennial HARVEST-window floor (whole_crop_gate A48, artichoke GS arc, 2026-07-26).

THE OTHER HALF OF THE ASPARAGUS DEFECT. Asparagus certified 120/120 while carrying neither
`plant_out` NOR `harvest` on any of its 39 zone cells. A47 (perennial_plant_out_gate) closed the
first half -- the app could not say WHEN TO PLANT. This closes the second -- the app could not say
WHEN TO EXPECT FOOD. On a crop that takes two to three years to yield, that is the more consequential
of the two: a grower who plants at the wrong time loses a season, but a grower with no harvest
expectation cannot tell a healthy establishing bed from a failed one.

Both fields fail the same way and for the same reason: `plant_out` and `harvest` are OPTIONAL, so
every gate that validates them goes VACUOUS when they are absent. A gate that validates a field's
SHAPE cannot notice the field's ABSENCE. A47 fixed that for one field and, by its own scope, could
not fix it for the other.

SCOPE -- archetype == 'herbaceous_perennial'. This is deliberately NARROWER than A47's
`perennial is True`, and the narrowing is evidence-based rather than cautious. Measured on canonical
34025ee3, the broader perennial scope reports 195 cells across five crops -- thyme, rosemary,
oregano, sage, lavender, at 39 cells each. Those are cut-as-needed culinary perennials with no
discrete harvest window; you cut sprigs whenever you cook. Whether they should carry a harvest
string at all is a real question and a SEPARATE ruling. It is recorded here and deliberately not
decided by this gate, because widening the scope to force it would be the "gate floods, so weaken
the gate" trade this suite exists to refuse.

On the archetype scope the gate reports 0 for asparagus, the only current member, so it ships
enforcing a convention the archetype already meets -- the same soft-launch discipline as A47.

TWO EXEMPTIONS, both copied from A47 deliberately so the two halves of the floor cannot drift apart:
  - EMPTY CALENDAR -> skip. An unfilled shell cell is an admission state, not a defect.
  - suitability == "unsuitable" -> skip. Those cells carry an honest all-`growing` calendar under
    the A32 honesty floor. Telling a grower when to expect food from a crop that will not grow
    there is worse than silence -- the same reasoning A47 applies to plant_out.

Usage: python3 tools/perennial_harvest_gate.py [crops_data_final.json]
Exit 1 on any violation.
"""
SKIP_SUITABILITY = {"unsuitable"}
ARCHETYPE = "herbaceous_perennial"


def perennial_harvest_violations(crop):
    """Return a list of violation strings ([] = clean). No-op off the herbaceous_perennial archetype."""
    if crop.get("archetype") != ARCHETYPE:
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
                continue  # never promise food where the crop will not grow
            if not cell.get("harvest"):
                V.append(f"{rk}.{z}: a calendared herbaceous-perennial cell must carry harvest "
                         f"(when food actually arrives, e.g. 'May - Jun'); without it the app can "
                         f"show a planting date but never tell a grower what to expect, which is "
                         f"how asparagus certified unable to answer its own core question")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    crops_hit = set()
    for c in data["crops"]:
        for v in perennial_harvest_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
            crops_hit.add(c.get("slug"))
    print(f"perennial harvest gate: {total} violation(s) across "
          f"{len(crops_hit)} crop(s) / {len(data['crops'])} scanned")
    sys.exit(1 if total else 0)
