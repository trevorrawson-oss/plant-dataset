#!/usr/bin/env python3
"""Fold the recommended-variety spectrum into the crop-level descriptions of apple, onion, and dry-bean
(the leek 2026-07-14 template: name representative anchors, not an exhaustive list). Emits a SHA-guarded
COMPACT patch replacing description_beginner + description_seasoned on the 3 crops (6 ops). Apple APPENDS
a sentence; onion + dry-bean weave named examples INLINE into an existing sentence. No new fields;
amend-not-recert. Strings are computed FROM the loaded canonical (append / single-substring replace) so
the patch `from` guards cannot drift.

Run: python3 tools/build_variety_descriptions_patch.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/variety_descriptions_backfill.json"

# apple: append (16 varieties; the descriptions named none). Low/high-chill split + triploids per the pilot.
APPLE_BEG_APPEND = (" The varieties run from familiar cold-climate apples like Honeycrisp, Gala, and Empire "
                    "to low-chill types like Anna, Dorsett Golden, and Ein Shemer that fruit in mild-winter "
                    "areas where standard apples never get enough cold.")
APPLE_SEAS_APPEND = (" The recommended set spans that range, from low-chill Anna, Dorsett Golden, and Ein "
                     "Shemer for mild-winter zones to high-chill Honeycrisp, McIntosh, and Empire for the "
                     "North, plus triploids like Jonagold and Mutsu that need two pollen partners instead of one.")

# onion: inline (weave one representative per day-length class into the existing sentence).
ONION_BEG = (
    "Long-day kinds need very long summer days and suit the North, short-day kinds need only short days and suit the South, and intermediate kinds sit in the middle and grow well across much of the country.",
    "Long-day kinds like Walla Walla need very long summer days and suit the North, short-day kinds like Texas 1015Y need only short days and suit the South, and intermediate kinds like Super Star sit in the middle and grow well across much of the country.",
)
ONION_SEAS = (
    "That threshold is what splits onions into long-day (14 to 16 hours), intermediate-day (12 to 14 hours), and short-day (10 to 12 hours) types, and it is why the right variety depends on your latitude.",
    "That threshold is what splits onions into long-day (14 to 16 hours, such as Walla Walla), intermediate-day (12 to 14 hours, such as Super Star), and short-day (10 to 12 hours, such as Texas 1015Y) types, and it is why the right variety depends on your latitude.",
)

# dry-bean: inline (it already names types; name the specific variety + the heirloom + a maturity hook).
DRYBEAN_BEG = (
    "Common kinds include black beans, pinto, navy, and kidney.",
    "Common kinds include black beans like Black Turtle, plus pinto, navy, kidney, and heirlooms like Jacob's Cattle.",
)
DRYBEAN_SEAS = (
    "Black turtle, pinto, navy, and kidney are all dry types of this one species.",
    "Black Turtle, Pinto, Navy, Kidney, and heirlooms like Jacob's Cattle are all dry types of this one species, differing in seed size, color, and how long they take to dry down (roughly 85 to 110 days).",
)


def crop(data, slug):
    return next(c for c in data["crops"] if c["slug"] == slug)


def replace_once(s, old, new):
    assert old in s, f"substring not found: {old!r}"
    assert s.count(old) == 1, f"substring not unique ({s.count(old)}x): {old!r}"
    return s.replace(old, new)


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)

    ops = []

    def rep(slug, key, oldval, newval):
        assert oldval != newval, f"no-op replace {slug}.{key}"
        assert "—" not in newval, f"em dash in {slug}.{key}"
        ops.append({"op": "replace",
                    "json_path": f"$.crops[?(@.slug=='{slug}')].{key}",
                    "from": oldval, "value": newval})

    apple = crop(data, "apple")
    a_beg, a_seas = apple["description_beginner"], apple["description_seasoned"]
    assert not a_beg.endswith(APPLE_BEG_APPEND.strip()), "apple beginner already appended"
    assert not a_seas.endswith(APPLE_SEAS_APPEND.strip()), "apple seasoned already appended"
    rep("apple", "description_beginner", a_beg, a_beg + APPLE_BEG_APPEND)
    rep("apple", "description_seasoned", a_seas, a_seas + APPLE_SEAS_APPEND)

    onion = crop(data, "onion")
    rep("onion", "description_beginner", onion["description_beginner"],
        replace_once(onion["description_beginner"], *ONION_BEG))
    rep("onion", "description_seasoned", onion["description_seasoned"],
        replace_once(onion["description_seasoned"], *ONION_SEAS))

    db = crop(data, "dry-bean")
    rep("dry-bean", "description_beginner", db["description_beginner"],
        replace_once(db["description_beginner"], *DRYBEAN_BEG))
    rep("dry-bean", "description_seasoned", db["description_seasoned"],
        replace_once(db["description_seasoned"], *DRYBEAN_SEAS))

    patch = {"base_sha": sha, "patches": ops}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(patch, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(ops)} ops: apple/onion/dry-bean description_beginner+seasoned)")


if __name__ == "__main__":
    main()
