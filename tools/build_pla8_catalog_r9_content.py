#!/usr/bin/env python3
"""PLA-8 catalog round 9: WIDEN `even_watering` to reach common scab. Base 6a67a677.

**THIS ROUND MODIFIES AN EXISTING METHOD, WHICH r7 AND r8 BOTH REFUSED TO DO.** Both of those
rounds asserted "NO existing method is touched" and guarded it. This one does the opposite thing on
purpose, so the guard shape is inverted: exactly ONE method changes, exactly which fields change is
pinned, and everything the method already said must SURVIVE byte-for-byte inside the new text.

--------------------------------------------------------------------------------------------------
WHY -- and this round exists because of an error I made in r8
--------------------------------------------------------------------------------------------------
r8's record claimed `even_watering` "already carries" the soil-moisture half of common scab control.
**It does not.** `even_watering.applies_to` was `['physiological', 'mite']`, which does not intersect
`TYPE_TARGETS['bacterial']`, so it was ILLEGAL on common scab, and no other method carried a "keep
the soil evenly moist" instruction for a disease. The claim asserted that a method existed without
checking that it was REACHABLE. Found by the thin-ladder scan the same day; corrected forward in the
live surfaces, with STATE_HISTORY and the r8 commit left byte-for-byte.

Both sources r8 already read say the moisture half is not optional:

  Clemson  "Scab is favored under low soil moisture conditions, so the garden soil must be kept
            moist during the active growing period of the tubers (particularly 4 to 9 weeks after
            planting)."
  PNW/OSU  "High soil moisture for 1 week before emergence and 8 weeks after reduced common scab in
            'Russet Burbank' potatoes. High moisture is defined as 80% or above of available
            moisture, measured at 9 inches in the soil."

--------------------------------------------------------------------------------------------------
WHY WIDEN RATHER THAN MINT
--------------------------------------------------------------------------------------------------
`even_watering` is ALREADY a two-mechanism method: it carries calcium-movement disorders (celery
blackheart, blossom-end rot) and spider mites, each with its own source, under one action. The
ACTION is identical in all three cases -- hold soil moisture steady -- and only the mechanism
differs. Minting a second key for the same action is how a catalog acquires two entries that tell
the same problem the same thing under different names, which is the confusion `lower_soil_ph` had to
be written to escape. So: widen, and carry the third mechanism in the prose with its own sources.

**`bacterial` ONLY, not `disease_general`.** Measured: `bacterial` opens 70 problems,
`disease_general` would open 382 by also reaching every fungal and viral problem, and nothing was
read for those. Common scab's organism is *Streptomyces scabies*, a filamentous bacterium, and
beet/common-scab is already typed `bacterial` on the roster. The evidence is scab-specific, so the
widening is the narrowest one that reaches it.

**The prose scopes what the type vocabulary cannot.** 70 problems become LEGAL; one is the case this
was read for. `best_use` therefore names potatoes and beets and common scab outright, so an author
choosing by `best_use` sees the intended case rather than a blanket permission.

--------------------------------------------------------------------------------------------------
WHAT MUST SURVIVE
--------------------------------------------------------------------------------------------------
**37 shipped rungs already point at this method** (25 mite, 12 physiological). Widening must be
purely additive: every existing claim stays in the text, and no existing target is removed. The
guard asserts each surviving fragment by name, because a widening that quietly rewrites what a
method meant would change 37 rungs' meaning without touching a single crop record.

Used by: tools/promote_pla8_catalog_r9.py
"""

VERIFIED = "2026-09-01"

# No new source IDs: clemson_hgic and osu_ext are already T1 in source_catalog. Both anchors were
# fetched and read on 2026-09-01 for r8 and are reused here for the mechanism they actually state.
NEW_SOURCES = {}

# The fragments the EXISTING method already asserts. Each must still be present after the widening,
# because 37 shipped rungs were authored against them.
MUST_SURVIVE = {
    "even_watering": (
        "celery blackheart",
        "blossom-end rot",
        "spider mites",
        "1 to 2 inches per week",
        "calcium",
    ),
}

# The single widening. `add_targets` is checked as a strict ADDITION; `set_fields` replaces whole
# strings, and every MUST_SURVIVE fragment above is re-asserted against the result.
WIDENINGS = {
    "even_watering": {
        "add_targets": ["bacterial"],
        "add_sources": ["clemson_hgic", "osu_ext"],
        "add_anchors": {
            "clemson_hgic": {
                "url": "https://hgic.clemson.edu/factsheet/irish-sweet-potato-diseases/",
                "verified": VERIFIED,
            },
            "osu_ext": {
                "url": "https://pnwhandbooks.org/plantdisease/host-disease/"
                       "beet-red-beta-vulgaris-common-scab",
                "verified": VERIFIED,
            },
        },
        "set_fields": {
            "how_it_works_beginner":
                "Keep the soil evenly moist so the plant can move calcium steadily to its "
                "fast-growing center. Wild swings between wet and dry are what trigger disorders "
                "such as celery blackheart. The same steady watering does a second job on potatoes "
                "and beets: the organism behind common scab gets its hold while the soil is dry as "
                "the roots are sizing up, so keeping that stretch moist is half of what keeps the "
                "skins clean.",
            "how_it_works_seasoned":
                "Uniform soil moisture sustains the transpiration-driven calcium flow to rapidly "
                "growing tissue; blackheart and blossom-end rot are localized calcium-deficiency "
                "disorders that appear when moisture swings or rapid growth outpace calcium "
                "delivery, not usually from low soil calcium. A separate mechanism applies to "
                "common scab, caused by the soil bacterium Streptomyces scabies: Clemson records "
                "that scab is favored under low soil moisture and that the soil must be kept moist "
                "through the active growing period of the tubers, roughly 4 to 9 weeks after "
                "planting, and the PNW handbook reports high soil moisture from a week before "
                "emergence through eight weeks after reducing scab in trials. Moisture is the half "
                "of scab control that acts during the season; holding soil pH down is the other, "
                "and neither substitutes for the other. It also holds spider mites down, since they "
                "build up fastest on plants that have been left dry and stressed.",
            "best_use":
                "Steady soil moisture instead of a swing between soaked and bone dry. It prevents "
                "the calcium-movement disorders such as celery blackheart and blossom-end rot, at "
                "roughly 1 to 2 inches per week on shallow-rooted crops, and it holds spider mites "
                "down too, since they build up fastest on plants that have been left dry and "
                "stressed. On potatoes and beets it is also half of common scab control, where dry "
                "soil while the roots are sizing is what lets the scab organism take hold; pair it "
                "there with holding the soil pH down, which is the other half.",
        },
        "add_pros": [
            "On a scab-prone bed it is the one control that acts during the season, when the pH "
            "decision has already been made",
        ],
        "add_cons": [
            "The scab benefit is tied to a particular stretch, the weeks when the roots are sizing, "
            "so watering that is steady only outside that window buys little",
        ],
    },
}

# The widening exists to make ONE thing reachable. If it stops being reachable the round is
# pointless, so the promote asserts it rather than assuming it.
UNBLOCKS = (("beet", "common-scab"), )


def apply_round(data):
    cm = data["control_methods"]
    for key, w in WIDENINGS.items():
        if key not in cm:
            raise AssertionError(f"{key} is not in the catalog, so it cannot be widened")
        m = cm[key]
        for t in w["add_targets"]:
            if t in m["applies_to"]:
                raise AssertionError(f"{key} already applies to {t!r}")
            m["applies_to"] = list(m["applies_to"]) + [t]
        for s in w["add_sources"]:
            if s not in m["sources"]:
                m["sources"] = list(m["sources"]) + [s]
        anchors = dict(m.get("anchoring_urls") or {})
        anchors.update({k: dict(v) for k, v in w["add_anchors"].items()})
        m["anchoring_urls"] = anchors
        for f, v in w["set_fields"].items():
            m[f] = v
        m["pros"] = list(m["pros"]) + list(w.get("add_pros") or [])
        m["cons"] = list(m["cons"]) + list(w.get("add_cons") or [])
    return {"widened": sorted(WIDENINGS)}


if __name__ == "__main__":
    import json, os
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    before = dict(d["control_methods"]["even_watering"])
    s = apply_round(d)
    after = d["control_methods"]["even_watering"]
    print(f"widened        : {', '.join(s['widened'])}")
    print(f"applies_to     : {before['applies_to']} -> {after['applies_to']}")
    print(f"sources        : {before['sources']} -> {after['sources']}")
    print(f"methods total  : {len(d['control_methods'])} (unchanged)")
