#!/usr/bin/env python3
"""Two NEW control methods for calcium-movement disorders (PLA-8, option 2). Base d19abe60.

WHY NEW METHODS RATHER THAN WIDENING THE EXISTING TWO. The blossom-end-rot controls were first
proposed as `applies_to` widenings on `balance_nitrogen` and `straw_mulch`. The biology checked out
and the widening was still wrong, because `applies_to` governs what the GATE accepts and does
nothing to the PROSE a reader sees:

  balance_nitrogen  "The soft, sappy new growth that too much nitrogen pushes out is exactly what
                    aphids multiply on."  -- BER's mechanism is ammoniacal nitrogen COMPETING WITH
                    CALCIUM UPTAKE. Nothing to do with sappy growth, and nothing to do with aphids.
  straw_mulch       "A layer of straw around and between strawberry plants keeps the ripening
                    berries up off the wet soil ... less likely to rot with gray mold."  -- a tomato
                    blossom-end-rot ladder would hand the reader strawberries and gray mold.

Widening alone would have let a bot author a rung that gates clean and reads as a non-sequitur. A
method whose how_it_works has to say "unless it is this other problem, in which case something else
entirely" is two methods. Ruled with Trevor 2026-08-23.

AND WHY THESE DO NOT DUPLICATE `even_watering`, which is already `physiological` and already states
the calcium mechanism: Clemson names TWO levers in one sentence, "Maintain a uniform supply of
moisture through irrigation and adequate soil mulches." Watering is a schedule; mulch is a material
you lay once. A ladder may legitimately carry both, and the prose below says explicitly which is
which so an author does not treat them as interchangeable.

SOURCE, fetched and read 2026-08-23: Clemson HGIC, "Tomato Diseases & Disorders" (already catalogued
T1, already anchoring 5 methods), Blossom End Rot section:
  * "The cause of this disorder is a calcium deficiency in the developing fruit."
  * "Extreme fluctuations in moisture ... and excessive ammoniacal (NH4+) nitrogen, potassium, or
     magnesium fertilization can also increase the chances of blossom end rot"
  * "Avoid ammoniacal nitrogen fertilizers for sidedress applications (beside or around the plants),
     as ammoniacal nitrogen also will compete with calcium for uptake."
  * "Maintain a uniform supply of moisture through irrigation and adequate soil mulches. Mulches
     will not only keep the soil cooler and more evenly moist but will suppress weeds"

Run: python3 tools/build_ber_methods_content.py
"""
import json
import sys

ANCHOR = {"clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/tomato-diseases-disorders/",
                           "verified": "2026-08-23"}}

NEW_METHODS = {
    "moisture_buffering_mulch": {
        "name": "Mulch to steady soil moisture",
        "tier": "cultural",
        "applies_to": ["physiological"],
        "how_it_works_beginner": (
            "Lay an inch or two of mulch over the bed once the soil has warmed. It is not there to "
            "stop disease; it is there to stop the soil swinging between soaked and bone dry. Those "
            "swings are what interrupt the flow of calcium into developing fruit, which is what "
            "causes the sunken dark patch on the blossom end. Mulch also keeps the soil cooler and "
            "holds the weeds down, so you disturb the roots less."
        ),
        "how_it_works_seasoned": (
            "A moisture buffer, not a splash barrier. Calcium moves with water, so the disorder "
            "tracks the variance of soil moisture rather than its average, and mulch flattens that "
            "variance between irrigations. It pairs with a steady watering schedule rather than "
            "replacing one: the mulch smooths what the schedule delivers."
        ),
        "best_use": (
            "Fruiting crops with a history of blossom end rot or of splitting, mulched at planting. "
            "Distinct from the straw mulch used under strawberries, which is a splash and contact "
            "barrier for fruit rots rather than a moisture buffer."
        ),
        "find_it_beginner": (
            "Straw, shredded leaves, or compost. Anything that holds a loose layer without matting "
            "down works; avoid piling it against the stems."
        ),
        "pros": [
            "Addresses the cause of the disorder, which no spray can do",
            "Also suppresses weeds, so there is less root disturbance from cultivating",
        ],
        "cons": [
            "Does nothing for fruit already showing the damage; those are set and will not recover",
            "Laid too early over cold soil it slows warming, which sets the crop back",
        ],
        "sources": ["clemson_hgic"],
        "anchoring_urls": dict(ANCHOR),
    },
    "avoid_ammoniacal_nitrogen": {
        "name": "Avoid ammonium fertilizers",
        "tier": "cultural",
        "applies_to": ["physiological"],
        "how_it_works_beginner": (
            "When you feed a fruiting crop partway through the season, check what form the nitrogen "
            "is in. Ammonium-based fertilizers compete with calcium for uptake, so feeding with one "
            "can bring on the sunken dark patch on the blossom end even when there is plenty of "
            "calcium in the soil. A calcium nitrate feed does the same job without the competition."
        ),
        "how_it_works_seasoned": (
            "Cation competition at the root surface, not a soil calcium shortage: ammonium, "
            "potassium and magnesium all compete with calcium for uptake, so a heavy sidedress of "
            "any of them can trigger the disorder on soil that tests adequate. This is a different "
            "lever from balancing nitrogen for soft growth, which is about the flush of tender "
            "tissue that soft-bodied pests feed on."
        ),
        "best_use": (
            "Sidedressing tomatoes, peppers and other fruiting crops where blossom end rot has "
            "appeared before, especially early in the season when fruit is sizing."
        ),
        "find_it_beginner": (
            "Read the label for the nitrogen source. Ammonium sulfate and ammonium nitrate are the "
            "ones to skip mid-season; calcium nitrate is the usual substitute."
        ),
        "pros": [
            "Costs nothing, since it is a choice between products you were buying anyway",
            "Works on soil that already tests adequate for calcium, where adding more does nothing",
        ],
        "cons": [
            "Only relevant if you sidedress at all; it changes nothing for an unfed crop",
            "Does not fix fruit already affected, and will not help if the real problem is "
            "uneven watering",
        ],
        "cautions": [
            "Soil pH governs how much calcium is available in the first place, so a soil test is "
            "worth more than a fertilizer swap if the disorder recurs every year."
        ],
        "sources": ["clemson_hgic"],
        "anchoring_urls": dict(ANCHOR),
    },
}


def main():
    d = json.load(open("crops_data_final.json"))
    for k in NEW_METHODS:
        if k in d["control_methods"]:
            raise SystemExit(f"ABORT: {k} already exists")
    print(f"new methods: {len(NEW_METHODS)}")
    for k, v in NEW_METHODS.items():
        print(f"   {k:28s} tier={v['tier']:9s} applies_to={v['applies_to']}")
    legal = [k for k, v in d["control_methods"].items()
             if "any" in v["applies_to"] or "physiological" in v["applies_to"]]
    print(f"\nmethods legal for `physiological`: {len(legal)} -> {len(legal) + 2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
