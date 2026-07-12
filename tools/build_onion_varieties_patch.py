#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching onion's varieties to the flat PHOTOPERIOD schema (spec
2026-07-12-onion-variety-pilot-design). The 6 existing varieties gain the common core + per-variety
days_to_maturity, keeping their day_length_type + use. Footprint = onion's `varieties` object + a new
crop-level `variety_archetype: "photoperiod_annual"` key + verification_status.source_set (adds the one
newly-cited T1 id, msu_ext). No other crop moves.

DESIGN (see spec s3-7 + the source manifest scratchpad/onion_source_manifest.md, Trevor-signed
2026-07-12):
- Per-variety `sources`/`anchoring_urls` carry T1 ONLY (day_length_type + the variety profile). Every
  variety cites >=1 catalogued T1 source, so whole_crop_gate E.source-tier stays green (onion is
  certified; the gate fails any non-T1 cited source).
- days_to_maturity is load-bearing (from_planting anchor, crop band [90,120]). day_length_type is the
  distinctive photoperiod field; the day-length-vs-region honesty (coverage + window-fit) lives in the
  A9 photoperiod_gate and is NOT re-checked here.
- SOURCING OUTCOME (Trevor-signed): 4 T1 / 2 T2. day_length_type is T1-backed for all six. The two T2
  varieties (Cimarron, Super Star) are T2 only on DTM: Cimarron's DTM is DERIVED from NMSU's
  transplant->harvest calendar (no stated integer); Super Star's DTM is seed-trade (Dixondale 95). That
  DTM honesty lives in per-variety `confidence_tier` + prose + the crop-level varieties.note
  transparency note, NOT a fabricated citation (the apple chill pattern).
- maturity_class = DTM class (early/mid/late), the annual meaning. NO bean traits, NO tree block.

Run: python3 tools/build_onion_varieties_patch.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/onion_varieties_pilot.json"
VERIFIED = "2026-07-12"

# Anchoring URLs per cited T1 source id (each a page fetched + quoted during the sourcing pass).
URL = {
    "tamu_agrilife": "https://aggie-horticulture.tamu.edu/vegetable/files/2011/10/onion1.pdf",
    "usu_ext": "https://extension.usu.edu/yardandgarden/research/onions-in-the-garden",
    "osu_ext": "https://horticulture.oregonstate.edu/oregon-vegetables/onions-dry-bulb-western-oregon",
    "uga_ext": "https://fieldreport.caes.uga.edu/publications/B1198/",
    "nmsu_ext": "https://pubs.nmsu.edu/_circulars/CR567/index.html",
    "msu_ext": "https://www.canr.msu.edu/news/best-practices-for-onion-production",
}

# Each variety: _src = [(source_id, url), ...] (T1 only). sources + anchoring_urls derive from it.
# day_length_type + use carry the real canonical values (verified, not blindly copied).
VARDEFS = [
    dict(id="walla-walla", name="Walla Walla", maturity_class="early", day_length_type="long_day",
         days_to_maturity=90, use="sweet fresh-eating", confidence_tier="T1",
         note_beginner="The Pacific Northwest sweet onion: very mild, thin-skinned, and a poor keeper, so eat it fresh. It is a long-day type for northern gardens, and in mild-winter areas it is often set out in fall and carried over for an early-summer harvest, about 90 days after transplanting.",
         note_seasoned="Long-day, about 90 to 100 days from transplant (Oregon State). Thin-skinned and does not store; often fall-set and overwintered in mild-winter regions. Its overwintering habit is a planting practice, not a break from its long-day response.",
         _src=[("osu_ext", URL["osu_ext"]), ("usu_ext", URL["usu_ext"])]),
    dict(id="yellow-sweet-spanish", name="Yellow Sweet Spanish", maturity_class="mid",
         day_length_type="long_day", days_to_maturity=110, use="all-purpose storage",
         confidence_tier="T1",
         note_beginner="A large, dependable long-day yellow for northern gardens, ready about 110 days after transplanting. It is more pungent than the sweet types, which makes it a better keeper for winter storage.",
         note_seasoned="Long-day (Texas A&M lists it by name), about 110 days from transplant. More pungent than the sweet whites and a solid storage onion; matures after Walla Walla and before the short-day types.",
         _src=[("tamu_agrilife", URL["tamu_agrilife"]), ("usu_ext", URL["usu_ext"])]),
    dict(id="super-star", name="Super Star", maturity_class="early", day_length_type="intermediate_day",
         days_to_maturity=95, use="sweet all-purpose", is_reference=True, confidence_tier="T2",
         note_beginner="A widely adaptable intermediate-day white that bulbs across most of the country, which is why it is a safe pick if you are unsure of your latitude. It is mild and sweet, ready about 95 days after transplanting, and like most whites it is not for long storage.",
         note_seasoned="Intermediate-day (Michigan State names it directly), the safe default when latitude is uncertain. About 95 days from transplant per the seed trade; sold in some catalogs as Sierra Blanca, under which name New Mexico State reports a longer season in cooler conditions, so treat the day count as climate-dependent. Mild white, short storage.",
         _src=[("msu_ext", URL["msu_ext"]), ("tamu_agrilife", URL["tamu_agrilife"])]),
    dict(id="cimarron", name="Cimarron", maturity_class="late", day_length_type="intermediate_day",
         days_to_maturity=115, use="storage", confidence_tier="T2",
         note_beginner="An intermediate-day storage onion for the central latitudes, between the long-day North and the short-day South. It is a later, firm-bulbing yellow, ready around 115 days after transplanting.",
         note_seasoned="Intermediate-day yellow (NC State), a later-maturing storage type for the central band. About 115 days from transplant, derived from New Mexico State's transplant-to-harvest calendar rather than a stated day count, so treat it as approximate.",
         _src=[("nmsu_ext", URL["nmsu_ext"])]),
    dict(id="texas-1015y-supersweet", name="Texas 1015Y SuperSweet", maturity_class="mid",
         day_length_type="short_day", days_to_maturity=110, use="sweet fresh-eating",
         confidence_tier="T1",
         note_beginner="A large, very sweet short-day onion for the South, bred by Texas A&M and named for its ideal Rio Grande Valley seeding date, October 15. Set transplants out in fall to winter for a spring harvest, about 110 days after transplanting. It is sweet, so it stores only a couple of months.",
         note_seasoned="Short-day (Texas A&M), about 110 days from transplant. Fall-to-winter set for a spring bulb in the South; very sweet, so storage is short. Named for its October 15 Rio Grande Valley seeding date.",
         _src=[("tamu_agrilife", URL["tamu_agrilife"])]),
    dict(id="yellow-granex", name="Yellow Granex", maturity_class="early", day_length_type="short_day",
         days_to_maturity=100, use="sweet fresh-eating", confidence_tier="T1",
         note_beginner="The classic flat sweet short-day onion, the Vidalia type, for southern gardens. It is mild and juicy, ready about 100 days after transplanting, with a short storage life.",
         note_seasoned="Short-day (University of Georgia; the Vidalia standard), about 100 days from transplant. Flat, mild, and juicy; a fresh-eating sweet onion with a short storage life.",
         _src=[("uga_ext", URL["uga_ext"]), ("tamu_agrilife", URL["tamu_agrilife"])]),
]

# Crop-level variety-set note: day-length-first guidance (preserved) + the DTM-sourcing TRANSPARENCY note.
NOTE_BEGINNER = ("Pick the type that matches where you live first, then pick a flavor. Northern gardeners "
                 "want long-day onions like Walla Walla or Yellow Sweet Spanish. Southern gardeners want "
                 "short-day onions like Texas 1015Y or Yellow Granex. In the middle of the country, or if "
                 "you are not sure, choose an intermediate one like Super Star. Remember that sweet onions "
                 "do not keep long, and stronger onions store for months. The day-length type is the part "
                 "we are most sure of, and it decides where a bulb will form. The days-to-maturity numbers "
                 "are counted from when you set out transplants and shift with the variety and your "
                 "weather, so treat them as a guide and check each onion's confidence tier.")
NOTE_SEASONED = ("Choose by day-length class first, then by use. The set below spans all three classes so "
                 "a grower at any latitude has a fit: long-day (Walla Walla, Yellow Sweet Spanish) for the "
                 "North, intermediate-day (Super Star, Cimarron) for the central band, and short-day "
                 "(Texas 1015Y, Yellow Granex) for the South. As a rule, sweet onions store poorly and "
                 "pungent storage onions keep for months. When in doubt about your latitude, an "
                 "intermediate type is the safest bet. One note on the numbers: day-length class is the "
                 "reliable, well-sourced axis and decides where each onion will bulb. Days to maturity is "
                 "measured from transplant and is inherently variety- and climate-dependent, and several "
                 "figures here come from the seed trade rather than university extension, so read each "
                 "variety's confidence tier as the honest measure of its day count.")


def build_variety(vd):
    src = vd["_src"]
    v = {
        "id": vd["id"], "name": vd["name"], "maturity_class": vd["maturity_class"],
        "is_reference": vd.get("is_reference", False),
        "days_to_maturity": vd["days_to_maturity"], "day_length_type": vd["day_length_type"],
        "use": vd["use"], "confidence_tier": vd["confidence_tier"],
        "note_beginner": vd["note_beginner"], "note_seasoned": vd["note_seasoned"],
        "sources": [i for i, _ in src],
        "anchoring_urls": {i: {"url": u, "verified": VERIFIED} for i, u in src},
    }
    return v


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    on = next(c for c in data["crops"] if c.get("slug") == "onion")

    varieties = [build_variety(vd) for vd in VARDEFS]
    refs = [v["id"] for v in varieties if v["is_reference"]]
    assert refs == ["super-star"], f"exactly one flagship expected (super-star), got {refs}"

    cited = sorted({i for v in varieties for i in v["sources"]})

    current_varieties = on["varieties"]
    new_varieties = dict(current_varieties)
    new_varieties["recommended"] = varieties
    new_varieties["note_beginner"] = NOTE_BEGINNER
    new_varieties["note_seasoned"] = NOTE_SEASONED
    new_varieties["sources"] = cited
    new_varieties["anchoring_urls"] = {i: {"url": URL[i], "verified": VERIFIED} for i in cited}

    current_ss = on["verification_status"]["source_set"]
    new_ss = sorted(set(current_ss) | set(cited))

    patch = {"base_sha": sha, "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='onion')].variety_archetype",
         "value": "photoperiod_annual"},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='onion')].varieties",
         "from": current_varieties, "value": new_varieties},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='onion')].verification_status.source_set",
         "from": current_ss, "value": new_ss},
    ]}
    os.makedirs("tools/batches", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(varieties)} varieties, cited T1 {cited}, "
          f"source_set +{sorted(set(cited) - set(current_ss))})")


if __name__ == "__main__":
    main()
