#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching dry-bean's 5 varieties to Full-T1 (spec 2026-07-11).

Footprint = dry-bean's `varieties` object + `verification_status.source_set` (adds wsu_ext, now cited
by pinto + Jacob's Cattle). No other crop moves. Per-variety `sources`/`anchoring_urls` carry the DTM
provenance inline. All 5 DTMs are T1 (source wins): black turtle 105 + navy 85 + kidney 100 (UC ANR
8402), pinto 103 + jacobs 107 (WSU niche-market dry-bean trials); black turtle heirloom history (MSU).

Run: python3 tools/build_dry_bean_varieties_patch.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/dry_bean_varieties_pilot.json"

UC8402 = {"ucanr_ext": {"url": "https://beans.ucdavis.edu/sites/g/files/dgvnsk13961/files/inline-files/80592.pdf",
                        "verified": "2026-07-11"}}
UC_MSU = {"ucanr_ext": UC8402["ucanr_ext"],
          "msu_ext": {"url": "https://www.canr.msu.edu/news/black-beans-and-rice-history-and-fun-facts",
                      "verified": "2026-07-11"}}
WSU = {"wsu_ext": {"url": "https://vegetables.wsu.edu/dry-bean-varieties-for-niche-markets-in-the-usa/",
                   "verified": "2026-07-11"}}

VARIETIES = [
    {"id": "black-turtle", "name": "Black Turtle", "days_to_maturity": 105, "maturity_class": "late",
     "seed_type": "heirloom", "seed_color": "black", "seed_size": "small", "plant_habit": "bush",
     "primary_use": "soup", "is_reference": True, "confidence_tier": "T1",
     "note_beginner": "The classic black bean and a longtime heirloom, a staple across the Americas for "
                      "thousands of years (you may also see it sold as the turtle bean). Small, shiny, "
                      "dark seeds with an earthy flavor. It is one of the slower dry beans to finish, so "
                      "give it a long, warm season and do not rush the harvest.",
     "note_seasoned": "Small, dense black seed on a bush plant; an Americas heirloom that long predates "
                      "modern cultivars. UC Davis lists Black Turtle at 105 or more days and classes it "
                      "as late, so plan on a full season to dry down. Earthy flavor, holds its shape "
                      "when cooked.",
     "sources": ["ucanr_ext", "msu_ext"], "anchoring_urls": UC_MSU},
    {"id": "pinto", "name": "Pinto", "days_to_maturity": 103, "maturity_class": "mid",
     "seed_type": "open_pollinated", "seed_color": "tan speckled", "seed_size": "medium",
     "plant_habit": "half_runner", "primary_use": "multi", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "The everyday tan-and-brown speckled bean behind refried beans and chili. A "
                      "dependable bush or half-runner type that dries down over a full warm season.",
     "note_seasoned": "Tan speckled seed on a bush or half-runner habit; a mid-season dry bean around "
                      "100 to 105 days in trials. The staple field bean: forgiving, productive, widely "
                      "adapted.",
     "sources": ["wsu_ext"], "anchoring_urls": WSU},
    {"id": "navy", "name": "Navy", "days_to_maturity": 85, "maturity_class": "early",
     "seed_type": "open_pollinated", "seed_color": "white", "seed_size": "small", "plant_habit": "bush",
     "primary_use": "baked", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "A small white bean for soups and baked beans. One of the faster dry beans to "
                      "finish, so it is a good pick if your season runs a little short.",
     "note_seasoned": "Small white seed; the fastest of the common dry types at roughly 85 days, at the "
                      "early end of the maturity range UC Davis reports for white beans. Bush habit, a "
                      "good choice where the season is shorter.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC8402},
    {"id": "kidney", "name": "Kidney", "days_to_maturity": 100, "maturity_class": "mid",
     "seed_type": "open_pollinated", "seed_color": "red", "seed_size": "large", "plant_habit": "bush",
     "primary_use": "chili", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "The large red kidney-shaped bean for chili and stews. It wants a full warm "
                      "season to dry down.",
     "note_seasoned": "Large red kidney seed; a moderately late dry bean around 100 days, in the "
                      "dark-red-kidney range UC Davis reports. Holds its shape well in long-cooked "
                      "dishes.",
     "sources": ["ucanr_ext"], "anchoring_urls": UC8402},
    {"id": "jacobs-cattle", "name": "Jacob's Cattle", "days_to_maturity": 107, "maturity_class": "late",
     "seed_type": "heirloom", "seed_color": "white and maroon speckled", "seed_size": "medium",
     "plant_habit": "bush", "primary_use": "multi", "is_reference": False, "confidence_tier": "T1",
     "note_beginner": "A New England heirloom with striking white-and-maroon speckled seeds. It is one "
                      "of the longest to finish, so give it a full season; good either dried or cooked "
                      "fresh from the shell.",
     "note_seasoned": "White-and-maroon speckled heirloom seed; one of the latest of the set at about "
                      "107 days in trials (WSU). Dual-purpose, dry or fresh-shell; reliable in the "
                      "Northeast.",
     "sources": ["wsu_ext"], "anchoring_urls": WSU},
]

NOTE_SEASONED = ("Nearly all common dry beans are bush or half-runner forms of Phaseolus vulgaris, so "
                 "they share this crop's culture; they differ mainly in seed color, size, and days to "
                 "maturity. Match the variety to your season: navy dries down fastest, while black "
                 "turtle and Jacob's cattle run the longest.")
NOTE_BEGINNER = ("Most dry beans are grown the same way; they just look different and take slightly "
                 "different amounts of time. If your season is short, choose a faster type like navy "
                 "rather than a long-season type like black turtle or kidney.")


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    db = next(c for c in data["crops"] if c.get("slug") == "dry-bean")

    current_varieties = db["varieties"]
    new_varieties = dict(current_varieties)
    new_varieties["recommended"] = VARIETIES
    new_varieties["note_seasoned"] = NOTE_SEASONED
    new_varieties["note_beginner"] = NOTE_BEGINNER

    current_ss = db["verification_status"]["source_set"]
    new_ss = sorted(set(current_ss) | {"wsu_ext"})

    patch = {"base_sha": sha, "patches": [
        {"op": "replace", "json_path": "$.crops[?(@.slug=='dry-bean')].varieties",
         "from": current_varieties, "value": new_varieties},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='dry-bean')].verification_status.source_set",
         "from": current_ss, "value": new_ss},
    ]}
    os.makedirs("tools/batches", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(VARIETIES)} varieties, +wsu_ext in source_set)")


if __name__ == "__main__":
    main()
