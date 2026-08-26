#!/usr/bin/env python3
"""PLA-8 batch 6 -- the three fixes the READ found, applied to the staged files.

Kept as a script rather than hand-edits so the fixes are reproducible and the promote can re-assert
them. Every anchor is asserted before it is changed.

FIX 1 -- BOTH crops / powdery-mildew: DROP the `wet_foliage_discipline` rung.
  THE METHOD IS LEGAL HERE AND ITS MECHANISM IS WRONG HERE, which is the batch-1 defect class in its
  purest form. `wet_foliage_discipline` says of itself: "Free moisture on the leaf surface is the
  transport medium for splash-dispersed bacteria and for many foliar fungi." Powdery mildew is not
  one of them. USU, a T1 document already anchored elsewhere in this catalog, states it directly:
  "In contrast to many fungi, powdery mildews do not spread in rain or free water. For infection,
  powdery mildews only need high humidity or dew for a few hours."

  AND THE CROP'S OWN RECORD REFUTES IT TOO. `cause_seasoned` says the fungus is "favored by warm
  days, cool nights, and dry foliage" and that "Spores spread on the wind" -- while
  `prevention_seasoned` says to "avoid working among wet vines". Those are two different disease
  physics in one entry, and the rung was resting on the half that is wrong for this pathogen.

  BOTH authoring passes flagged the contradiction unprompted, and both authored the rung anyway with
  NO mechanism stated, because neither could restate a mechanism the entry undercuts. That refusal to
  invent is what surfaced it.

  THE CONTRAST THAT SETTLES IT: `airflow_spacing` STAYS on the same ladder, because its `best_use`
  names powdery mildew explicitly ("the same room helps against gray mold, powdery mildew and
  damping-off") and humidity, not free water, is the mechanism it acts on. One method is sanctioned
  for this pathogen by its own sheet and the other is not.

  `wet_foliage_discipline` also stays on ASCOCHYTA on both crops, which is correct: that entry's own
  cause says "Cool, wet weather and splashing water spread them". Same crop, same method, right use
  and wrong use side by side.

FIX 2 + 3 -- snow-peas ordering, to match the sibling AND the source's own order.
  The cross-sibling check flagged Root rots (8 of 8 prose fields identical across the two crops) and
  Ascochyta blight (7 of 8). Same method SET, different order, built from prose that is identical.
  Both are same-tier (cultural) moves, so no claim is added or removed.

  Direction taken from the SOURCE, not the sibling, and they agree. Root rots prevention reads
  drainage -> sowing -> rotation -> cleanup, with the variety hedge last; Ascochyta prevention reads
  clean seed -> clear old plants -> rotation -> water at base -> stay out when wet. sugar-snap-peas
  already matches both; snow-peas is moved onto it.
"""
import json, os, sys

B = os.path.dirname(os.path.abspath(__file__))
DROP_FROM = "powdery-mildew"
DROP_METHOD = "wet_foliage_discipline"


def load(slug):
    return json.load(open(os.path.join(B, f"out_{slug}.json")))


def save(slug, d):
    json.dump(d, open(os.path.join(B, f"out_{slug}.json"), "w"), ensure_ascii=False, indent=2)


def problems(d):
    return list(d.get("pests") or []) + list(d.get("diseases") or [])


def by_id(d, pid):
    for p in problems(d):
        if p["id"] == pid:
            return p
    raise AssertionError(f"problem {pid!r} not in staged file")


def methods(p):
    return [r["method"] for r in p["control_ladder"]]


def reorder(p, want):
    have = methods(p)
    assert sorted(have) == sorted(want), f"not a permutation: {have} vs {want}"
    assert have != want, f"already in the target order: {have}"
    index = {r["method"]: r for r in p["control_ladder"]}
    p["control_ladder"] = [index[m] for m in want]


def main():
    changed = []

    # ---- FIX 1: both crops -------------------------------------------------------------------
    for slug in ("snow-peas", "sugar-snap-peas"):
        d = load(slug)
        pm = by_id(d, DROP_FROM)
        before = methods(pm)
        assert DROP_METHOD in before, f"{slug}: {DROP_METHOD} is not on the {DROP_FROM} ladder"
        assert "airflow_spacing" in before, (
            f"{slug}: airflow_spacing is missing, and it is the method that SHOULD carry the "
            f"canopy-humidity case here")
        pm["control_ladder"] = [r for r in pm["control_ladder"] if r["method"] != DROP_METHOD]
        # The same method must SURVIVE on ascochyta, where splash dispersal is the crop's own
        # stated mechanism. Dropping it there too would be over-correcting.
        asc = by_id(d, "ascochyta-blight")
        assert DROP_METHOD in methods(asc), (
            f"{slug}: {DROP_METHOD} must remain on ascochyta-blight, whose cause states that "
            f"splashing water spreads it")
        save(slug, d)
        changed.append(f"{slug}/{DROP_FROM}: dropped {DROP_METHOD} ({before} -> {methods(pm)})")

    # ---- FIX 2 + 3: snow-peas ordering --------------------------------------------------------
    d = load("snow-peas")
    rr = by_id(d, "root-rots-damping-off")
    reorder(rr, ["improve_drainage", "sound_sowing_practice", "crop_rotation", "garden_sanitation",
                 "resistant_varieties"])
    changed.append(f"snow-peas/root-rots-damping-off: reordered -> {methods(rr)}")

    asc = by_id(d, "ascochyta-blight")
    reorder(asc, ["certified_clean_stock", "garden_sanitation", "crop_rotation", "water_at_the_base",
                  "wet_foliage_discipline"])
    changed.append(f"snow-peas/ascochyta-blight: reordered -> {methods(asc)}")
    save("snow-peas", d)

    print(f"applied {len(changed)} read fixes:")
    for c in changed:
        print(f"  - {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
