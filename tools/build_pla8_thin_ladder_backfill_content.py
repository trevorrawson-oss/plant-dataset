#!/usr/bin/env python3
"""PLA-8 thin-ladder backfill: 8 rungs onto 6 problems across 4 SHIPPED crops. Base 4f33522c.

Every one of these was found by the **thin-ladder scan** run 2026-09-01, and every one is the same
shape: *the problem's own prose names a control that EXISTS in the catalog, is LEGAL for its type,
and is missing from its ladder.* None of these crops is in the roots batch; all six problems ship
today on certified crops.

  scan population : 775 laddered problems / 3,149 rungs; 133 carry <= 2 rungs
  leads generated : 10 over 9 problems
  real            : 6  <- these
  false positives : 4, every one because the prose named the control in order to DISCOUNT it

Two of the six only became fixable in the last two rounds: `beet`/`common-scab` needed
`lower_soil_ph` (r8) and `even_watering` reaching `bacterial` (r9), and `garlic`'s two needed
`cure_and_store` (r8).

--------------------------------------------------------------------------------------------------
WHAT IS AND IS NOT CHANGED
--------------------------------------------------------------------------------------------------
Rungs are ADDED. **No existing rung's prose is touched**, and the guard asserts every one of them is
byte-identical after. Ladder ORDER is re-pinned on three problems so the sequence follows the
record's own order rather than leaving a new rung stranded at the end; every reorder is declared
explicitly in `expect_after` and none of them crosses a tier, because every method involved here is
`cultural`.

`control_methods`, `source_catalog` and every other crop are untouched.

--------------------------------------------------------------------------------------------------
ONE SCAN RESULT CORRECTED WHILE AUTHORING
--------------------------------------------------------------------------------------------------
The scan reported `strawberry`/`red-stele` as carrying a `crop_rotation` rung its prose "names
nowhere". **That was an artifact of the scan's field selection**, which read only the prevention and
treatment fields. `cause_seasoned` says the pathogens "persist for years", which is exactly what
rotation acts on. The rung is supported and stays. Recorded because the scan's own output is now a
document others will read.

Used by: tools/promote_pla8_thin_ladder_backfill.py
"""

# (crop, problem id) -> the exact ladder before, the exact ladder after, and the new rungs' prose.
# `expect_before` is asserted against canonical so a drifted ladder refuses rather than being
# silently rebuilt.
BACKFILL = {
    ("strawberry", "red-stele"): {
        "expect_before": ["resistant_varieties", "crop_rotation"],
        "expect_after": ["improve_drainage", "certified_clean_stock", "resistant_varieties",
                         "crop_rotation"],
        "add": {
            "improve_drainage": {
                "note_beginner":
                    "Put the bed where water drains away, or raise it up before you plant. This rot "
                    "works in cold, soggy ground, so heavy wet soil is the condition it needs and "
                    "the one thing about the site you can still change.",
                "note_seasoned":
                    "Drainage is the site decision this disease turns on: the pathogen is a "
                    "soilborne water mold that thrives in cold, saturated soil, so a raised bed on "
                    "heavy ground removes the condition rather than treating the plant. It is "
                    "settled before planting and cannot be added once the row is in.",
            },
            "certified_clean_stock": {
                "note_beginner":
                    "Buy certified plants rather than taking runners from a patch whose history you "
                    "do not know. The fungus can arrive on the planting stock itself, so what you "
                    "set out decides whether it comes into the bed at all.",
                "note_seasoned":
                    "Certified stock closes a route into the bed that no in-season step reaches, "
                    "since this one travels in planting material. Clean plants set into "
                    "well-drained ground is the whole of the preventive program here, because "
                    "nothing rescues a plant once the root core has gone red.",
            },
        },
    },
    ("fig", "dried-fruit-beetle-souring"): {
        "expect_before": ["resistant_varieties", "garden_sanitation"],
        "expect_after": ["prompt_harvest", "resistant_varieties", "garden_sanitation"],
        "add": {
            "prompt_harvest": {
                "note_beginner":
                    "Pick the figs as soon as they are ripe instead of letting them hang. "
                    "Over-ripe fruit still on the tree is what draws the beetles in, so taking the "
                    "crop on time removes the thing attracting them.",
                "note_seasoned":
                    "Harvest timing is a control here rather than a preference: the beetles are "
                    "drawn to fruit left past ripeness and carry the souring yeasts into it through "
                    "the eye, so shortening that window acts on the attraction itself. It works "
                    "alongside clearing dropped fruit rather than in place of it.",
            },
        },
    },
    ("fig", "fig-endosepsis"): {
        "expect_before": ["resistant_varieties", "garden_sanitation"],
        "expect_after": ["prompt_harvest", "resistant_varieties", "garden_sanitation"],
        "add": {
            "prompt_harvest": {
                "note_beginner":
                    "Take the figs as they ripen rather than leaving them on the tree. The same sap "
                    "beetles that carry this fungus are drawn to fruit that has hung too long.",
                "note_seasoned":
                    "Picking on time narrows the stretch when fruit is attractive to the sap "
                    "beetles that move these fungi. Because there is no in-fruit cure, every "
                    "control acts before infection, and harvest timing is the one that runs "
                    "through the whole ripening period.",
            },
        },
    },
    ("beet", "common-scab"): {
        "expect_before": ["crop_rotation"],
        "expect_after": ["even_watering", "lower_soil_ph", "crop_rotation"],
        "add": {
            "even_watering": {
                "note_beginner":
                    "Keep the bed evenly moist rather than letting it dry out between waterings, "
                    "and pay most attention while the roots are filling out. Dry soil at that stage "
                    "is what lets scab get its hold on the skins.",
                "note_seasoned":
                    "Steady moisture through root sizing is the in-season half of scab control, and "
                    "it is the half still available once the crop is in the ground. The pH decision "
                    "is made before planting; this one is made every week.",
            },
            "lower_soil_ph": {
                "note_beginner":
                    "Hold off on lime for this bed. Scab does better as the soil moves toward "
                    "neutral and beyond, so where a test puts you above about 7.0 the useful move "
                    "is to add nothing that pushes it higher.",
                "note_seasoned":
                    "The lever here is restraint rather than application: skip lime and wood ashes "
                    "where a test shows the bed at or above about 7.0. It is settled before "
                    "planting and pays off in the next crop, which is why it pairs with steady "
                    "moisture, the part that acts on the crop already growing.",
            },
        },
    },
    ("garlic", "botrytis-neck-rot"): {
        "expect_before": ["balance_nitrogen"],
        "expect_after": ["balance_nitrogen", "cure_and_store"],
        "add": {
            "cure_and_store": {
                "note_beginner":
                    "Dry the garlic down after lifting until the necks are tight, then keep it "
                    "somewhere cool, dry and airy. The mold gets into bulbs that were pulled green "
                    "or dried poorly, so the curing is what shuts that door.",
                "note_seasoned":
                    "Curing until the necks are tight and dry is the control this disease turns on, "
                    "since it enters through necks left soft by a green harvest or an inadequate "
                    "cure. Handle gently to avoid the wounds it also uses, and hold the cured crop "
                    "cool, dry and with air moving. Take the conditions from this crop rather than "
                    "from another.",
            },
        },
    },
    ("garlic", "fusarium-basal-rot"): {
        "expect_before": ["certified_clean_stock", "resistant_varieties", "crop_rotation"],
        "expect_after": ["certified_clean_stock", "resistant_varieties", "crop_rotation",
                         "cure_and_store"],
        "add": {
            "cure_and_store": {
                "note_beginner":
                    "Handle the bulbs gently as you lift and dry them, then store them cool and "
                    "dry. This fungus gets in through injuries, so the bruises and nicks of a rough "
                    "harvest are the opening it uses.",
                "note_seasoned":
                    "Gentle handling and correct storage act on the entry route rather than on the "
                    "organism: wounds are what let it in, and this crop's guidance puts cured bulbs "
                    "cool, below about 39°F, and dry. It protects sound bulbs and does nothing for "
                    "one already infected in the ground.",
            },
        },
    },
}

EXPECTED_PROBLEMS = 6
EXPECTED_NEW_RUNGS = 8
EXPECTED_CROPS = ("beet", "fig", "garlic", "strawberry")

# Each added rung must be traceable to a phrase in ITS OWN problem's prose. This is the
# restate-the-record discipline made checkable: a rung whose warrant is not in the record is an
# invention, however plausible.
WARRANTS = {
    ("strawberry", "red-stele", "improve_drainage"): "well-drained soil or raised beds",
    ("strawberry", "red-stele", "certified_clean_stock"): "certified plants",
    ("fig", "dried-fruit-beetle-souring", "prompt_harvest"): "prompt harvest",
    ("fig", "fig-endosepsis", "prompt_harvest"): "pick promptly",
    ("beet", "common-scab", "even_watering"): "evenly moist",
    ("beet", "common-scab", "lower_soil_ph"): "do not lime",
    ("garlic", "botrytis-neck-rot", "cure_and_store"): "necks are tight",
    ("garlic", "fusarium-basal-rot", "cure_and_store"): "store cured bulbs cool",
}


def apply_round(data):
    by = {c["slug"]: c for c in data["crops"]}
    added = 0
    for (slug, pid), spec in BACKFILL.items():
        crop = by[slug]
        prob = None
        for fam in ("pests", "diseases"):
            for p in crop.get(fam) or []:
                if isinstance(p, dict) and p.get("id") == pid:
                    prob = p
        if prob is None:
            raise AssertionError(f"{slug}/{pid} is not on the roster")
        before = [r["method"] for r in prob["control_ladder"]]
        if before != spec["expect_before"]:
            raise AssertionError(f"{slug}/{pid} ladder is {before}, expected {spec['expect_before']}")
        existing = {r["method"]: r for r in prob["control_ladder"]}
        rebuilt = []
        for m in spec["expect_after"]:
            if m in existing:
                rebuilt.append(existing[m])
            else:
                rebuilt.append({"method": m, **spec["add"][m]})
                added += 1
        prob["control_ladder"] = rebuilt
    return {"problems": len(BACKFILL), "rungs_added": added}


if __name__ == "__main__":
    import json, os
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    s = apply_round(d)
    print(f"problems touched : {s['problems']}")
    print(f"rungs added      : {s['rungs_added']}")
