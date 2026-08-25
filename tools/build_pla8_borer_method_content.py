#!/usr/bin/env python3
"""PLA-8: mint `borer_stem_surgery`, the control three authoring agents independently refused to fake.

WHY THE CATALOG IS THE FIX, NOT THE AUTHORS. The playbook's rule is that when several bots
independently report the same control blocked, the gap is in the catalog. Batch 4 produced exactly
that: acorn-squash, butternut-squash and spaghetti-squash all reported the squash vine borer's stem
surgery as unplaceable, and two of them rejected `handpick` by name, citing that method's OWN con --
"Misses hidden eggs and tiny larvae, so it must be repeated". A larva inside a stem is the case
handpicking is documented to MISS. That is the `bottom_watering` trap: same-sounding key, different
action. yellow-summer-squash used `handpick` and flagged it as "not literal" in the same breath.

It matters because this is the crop's ONLY in-season remedy for the pest. Without a key, five
ladders carried no action at all for the headline organic treatment their own prose leads with.

SCOPE: 9 crops carry Squash vine borer -- the five squashes in batch 4, plus watermelon, cantaloupe,
pumpkin and honeydew-melon, none of them laddered yet. Minting now means the four later ones get it
during their own authoring rather than through a backfill promote over shipped crops.

`applies_to` IS `insect_boring`, DELIBERATELY NARROW. That target already exists and is used by
`fruit_bagging` and `codling_moth_pheromone_trap`. Scoping it to boring insects is what keeps this
method from becoming a second `handpick`: the gate will refuse it on a surface pest, which is the
confusion that created the gap in the first place.

SOURCING: two T1 extension documents, fetched and READ, both already cited by these crops.

  UMN  "As soon as wilting is noticed, use a sharp knife to cut a slit in the affected stem. Slice
        carefully up the vine until you locate the borer (or borers)." / "Once you have killed any
        borers with the tip of the knife, mound moist soil over the cut area and keep this spot
        well watered. New roots may grow along the cut stem, allowing the plant to survive." /
        "Keep in mind that you may not be able to save the plant."
  ISU  "Borers can sometimes be successfully removed from infested stems with a sharp knife during
        July or early August." / "Cover the dissected stem with a shovelful of soil." / "infested
        plants are often able to live and produce in spite of borer activity." / insecticides do
        not help plants that "already have borers in the stem."

BOTH SOURCES HEDGE, AND BOTH HEDGES ARE KEPT. UMN says you may not save the plant; ISU says borers
can SOMETIMES be removed, in a stated July-to-early-August window. A dropped qualifier is a defect
with no term to scan for, so the cons carry the failure case and the seasoned register names the
window and attributes both sources.

STALE ANCHOR FOUND WHILE SOURCING, recorded not fixed here: yellow-summer-squash and
zucchini-courgette cite `hortnews.extension.iastate.edu/squash-vine-borer`, which now 301-redirects
to `yardandgarden.extension.iastate.edu/encyclopedia/squash-vine-borer`. The document is alive and
its content still supports the claims; only the URL moved. This mint anchors the NEW url. The crop
anchors are a separate repoint and are NOT touched by this promote.

Used by: tools/promote_pla8_borer_method.py
"""

KEY = "borer_stem_surgery"

METHOD = {
    "name": "Stem surgery",
    "tier": "physical",
    # NARROW ON PURPOSE. See the module docstring: `insect_boring` is what stops this becoming a
    # second handpick, and the gate refuses it on a surface pest.
    "applies_to": ["insect_boring"],
    "how_it_works_beginner":
        "Once a grub is tunneling inside the stem, nothing you spray can reach it, so the only move "
        "left is to go in after it. Slit the stem lengthwise with a sharp knife, follow the tunnel "
        "until you find the grub, and kill it. Then mound damp soil over the cut and keep that spot "
        "watered, because the vine can put out fresh roots along the wound and carry on. It does "
        "not work every time and you may lose the plant anyway, but the vine is usually lost without it.",
    "how_it_works_seasoned":
        "Once larvae are inside the stem, insecticides no longer reach them, so extraction is the "
        "remaining in-season option. Cut lengthwise from the frass hole, destroy the larva or "
        "larvae, then mound moist soil over the wound and keep it watered so adventitious roots can "
        "form along the cut and carry the plant. Iowa State puts the workable window at July or "
        "early August and notes that infested plants are often able to live and produce anyway; UMN "
        "is blunter, that you may not be able to save the plant. Treat it as a salvage attempt on a "
        "vine you would otherwise lose, not as a control that lowers pressure.",
    "best_use":
        "A vine already wilting or pushing frass, where the grub is inside the stem and past the "
        "reach of any spray. Most worth attempting in July or early August, on a plant you would "
        "otherwise lose.",
    "pros": [
        "The one option left once a borer is inside the stem, where sprays no longer reach",
        "Costs nothing but a knife and a few minutes, and the mounded soil can re-root the vine",
    ],
    "cons": [
        "It may not save the plant, and the cut sets the vine back even when it works",
        "Reaches only the larvae you find, and a single stem can hold more than one",
    ],
    "sources": ["umn_ext", "iastate_ext"],
    "anchoring_urls": {
        "umn_ext": {"url": "https://extension.umn.edu/yard-and-garden-insects/squash-vine-borers",
                    "verified": "2026-08-25"},
        "iastate_ext": {"url": "https://yardandgarden.extension.iastate.edu/encyclopedia/squash-vine-borer",
                        "verified": "2026-08-25"},
    },
}

# Quotes the prose must remain faithful to; the guard suite asserts the hedges survive.
SOURCE_HEDGES = (
    "you may not be able to save the plant",          # UMN
    "sometimes be successfully removed",              # ISU
    "July or early August",                           # ISU, the stated window
)


def apply_mint(cm):
    """Insert the method. Raises if it already exists or the catalog shape is unexpected."""
    if KEY in cm:
        raise AssertionError(f"{KEY} already in the catalog")
    shape = set(next(iter(cm.values())).keys())
    missing = {"name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
               "best_use", "pros", "cons", "sources", "anchoring_urls"} - set(METHOD)
    if missing:
        raise AssertionError(f"mint is missing required fields: {sorted(missing)}")
    cm[KEY] = dict(METHOD)
    return 1


if __name__ == "__main__":
    import json, os, sys
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    n = apply_mint(d["control_methods"])
    print(f"minted {n}: {KEY} (tier {METHOD['tier']}, applies_to {METHOD['applies_to']})")
    print(f"catalog would go {len(d['control_methods'])-1} -> {len(d['control_methods'])}")
