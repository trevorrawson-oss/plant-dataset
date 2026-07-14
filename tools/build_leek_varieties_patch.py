#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching leek's varieties to the flat HARDINESS_ANNUAL schema
(spec 2026-07-14 leek variety-archetype pilot, the 4th archetype: winter-hardiness / overwintering).
The 6 existing varieties gain the common core + per-variety cold_hardiness_class + days_to_maturity
(dtm_anchor=from_transplant, unchanged crop-level), replacing the retired `season`/`recommended_note`
pair. New crop-level `variety_archetype: "hardiness_annual"` + `winter_hardiness` model object (mirrors
onion's `photoperiod` shape) + `gating_factors` opt-in + folded-in crop descriptions.

DESIGN (see the AUTHORED CONTENT scratchpad leek_authoring_content.md, controller-authored,
T1-researched 2026-07-14):
- Per-variety `sources`/`anchoring_urls` carry T1 ONLY. Every variety cites >=1 catalogued T1 source.
- cold_hardiness_class is T1 for ALL 6 (the archetype spine): RHS + USU + UMN + Cornell.
- Per-variety DTM integer: T1 only for Lancelot (Cornell VVFG, 100 from transplant). The other 5 are
  seed-trade (T2). Per-variety `confidence_tier` = weakest load-bearing datapoint (onion rule) =>
  Lancelot T1, other 5 T2.
- `min_temp_f`: OMITTED on all 6 (no per-variety T1 °F exists; UMN's "near 20°F" is crop-level, lives
  in the winter_hardiness model prose). T1-or-OMIT rule (the shallot lesson).
- exactly ONE is_reference:true => Lancelot (the "good first choice if unsure" default).
- maturity_class = DTM class (early/mid/late), the annual meaning. NO bean/tree fields, NO
  day_length_type, NO season/recommended_note (dropped/split into maturity_class +
  cold_hardiness_class + dual-register notes).

Run: python3 tools/build_leek_varieties_patch.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/leek_varieties_pilot.json"
VERIFIED = "2026-07-14"

# Anchoring URLs per cited T1 source id (fetched + quoted during the sourcing pass, 2026-07-14).
# uf_ifas is the pre-existing leek core-biology source, verified 2026-06-29 -- not cited per-variety
# here, so it never enters URL lookups below, but is kept for completeness/reference.
URL = {
    "usu_ext": "https://extension.usu.edu/yardandgarden/research/leeks-in-the-garden",
    "rhs": "https://www.rhs.org.uk/vegetables/leeks/grow-your-own",
    "cornell_ext": "http://vegvariety.cce.cornell.edu/main/showVarieties.php?searchCriteria=leek",
    "umn_ext": "https://extension.umn.edu/vegetables/growing-leeks",
    "uf_ifas": "https://ask.ifas.ufl.edu/publication/HS1388",
}
UF_IFAS_VERIFIED = "2026-06-29"

# Each variety: _src = [(source_id, url), ...] (T1 only). sources + anchoring_urls derive from it.
VARDEFS = [
    dict(id="king-richard", name="King Richard", maturity_class="early",
         cold_hardiness_class="tender", days_to_maturity=90, use="early fresh use",
         is_reference=False, confidence_tier="T2",
         note_beginner="The fast early leek: it sizes up in about 90 days from transplant, giving tall, tender stems for late summer and fall. King Richard is less cold hardy than the winter types, so plan to use it before hard freezes rather than leaving it standing through winter.",
         note_seasoned="An early, quick-sizing summer-to-fall leek, roughly 90 days from transplant. It is the tender member of the set, best used before hard freezes rather than overwintered. Useful for a first harvest while the maincrop and overwintering types size up behind it.",
         _src=[("usu_ext", URL["usu_ext"]), ("cornell_ext", URL["cornell_ext"])]),
    dict(id="lancelot", name="Lancelot", maturity_class="mid",
         cold_hardiness_class="hardy", days_to_maturity=100, use="all-purpose",
         is_reference=True, confidence_tier="T1",
         note_beginner="A reliable, vigorous maincrop leek for fall harvest, about 100 days from transplant. Lancelot is widely adapted and hardy enough to stand into cold weather, which makes it a good first choice if you are not sure what to grow.",
         note_seasoned="The default maincrop pick: vigorous, uniform, and widely adapted, about 100 days from transplant (Cornell). Hardy through fall and light freezes, though not bred to overwinter like Bandit or Giant Musselburgh. If you grow one leek, grow this one.",
         _src=[("cornell_ext", URL["cornell_ext"]), ("umn_ext", URL["umn_ext"])]),
    dict(id="large-american-flag", name="Large American Flag", maturity_class="mid",
         cold_hardiness_class="hardy", days_to_maturity=120, use="all-purpose heirloom",
         is_reference=False, confidence_tier="T2",
         note_beginner="A dependable open-pollinated standard, also sold as Broad London, with thick shanks for fall harvest in about 120 days from transplant. It is the classic home-garden leek that Utah State and other extension guides still recommend.",
         note_seasoned="The old open-pollinated standard (sold as Broad London), thick-shanked and dependable for fall, roughly 120 days from transplant. Hardy into cold weather; a maincrop workhorse rather than a dedicated overwinterer. USU-listed.",
         _src=[("usu_ext", URL["usu_ext"]), ("cornell_ext", URL["cornell_ext"])]),
    dict(id="tadorna", name="Tadorna", maturity_class="mid",
         cold_hardiness_class="hardy", days_to_maturity=100, use="fall to early winter",
         is_reference=False, confidence_tier="T2",
         note_beginner="A hardy, uniform leek that holds well as the weather turns cold, about 100 days from transplant. Tadorna bridges the gap between the fall maincrop types and the true overwinterers, so you can keep harvesting into early winter.",
         note_seasoned="A hardy, uniform Dutch maincrop, about 100 days from transplant, that stands well into cold and bridges the fall-to-overwintering window. Tougher than the plain fall types but stops short of Bandit or Giant Musselburgh for deep-winter standing.",
         _src=[("cornell_ext", URL["cornell_ext"]), ("rhs", URL["rhs"])]),
    dict(id="bandit", name="Bandit", maturity_class="late",
         cold_hardiness_class="very_hardy", days_to_maturity=120, use="overwintering",
         is_reference=False, confidence_tier="T2",
         note_beginner="The toughest overwintering leek here: a very cold hardy, blue-green type (the Blauwgroene Winter strain) that stands in the garden through winter into spring in milder zones. It is slow and late, about 120 days from transplant, but it is the one to grow to dig leeks fresh in the cold months.",
         note_seasoned="A very hardy, blue-green overwintering leek (Blauwgroene Winter, RHS AGM as Bandit), late and slow at roughly 120 days from transplant but the most weather-tough of the set. It stands hard winters into spring where the class is viable; the headline overwinterer.",
         _src=[("rhs", URL["rhs"]), ("cornell_ext", URL["cornell_ext"])]),
    dict(id="giant-musselburgh", name="Giant Musselburgh", maturity_class="late",
         cold_hardiness_class="very_hardy", days_to_maturity=110, use="overwintering heirloom",
         is_reference=False, confidence_tier="T2",
         note_beginner="A hardy old Scottish heirloom with broad, mild shanks that takes cold well, about 110 days from transplant. It is a traditional pick for a winter standing crop, an open-pollinated alternative to Bandit if you want to save seed or grow a heritage variety.",
         note_seasoned="A broad-shanked Scottish heirloom, open-pollinated, very hardy and traditional for a winter standing crop, roughly 110 days from transplant. The heritage overwinterer alongside Bandit: milder flavored, a touch faster, and seed-saveable.",
         _src=[("cornell_ext", URL["cornell_ext"]), ("rhs", URL["rhs"])]),
]

# Crop-level winter_hardiness model object (mirrors onion.photoperiod shape EXACTLY).
WH_EXPLAINER_BEGINNER = ("Leeks fall into two camps by how much cold they take. Summer and early "
    "types, like King Richard, grow fast and are meant to be eaten in late summer and fall; a hard "
    "freeze will damage them, so harvest before deep winter. Overwintering types, like Bandit and "
    "Giant Musselburgh, are bred to stand right in the garden through winter and be dug fresh in the "
    "cold months. How far north you can overwinter one depends on your zone: the hardiest leeks "
    "shrug off temperatures around 20°F and lower, and a thick mulch of straw or leaves buys roughly "
    "another zone of protection. In the coldest areas, treat even a hardy leek as a fall crop, or "
    "harvest and store it before the ground freezes solid.")
WH_EXPLAINER_SEASONED = ("Leek cold tolerance sorts into three classes the app uses to judge "
    "overwintering viability by zone. Tender types (King Richard) are grown in season and harvested "
    "by fall; they are not overwintered. Hardy maincrop types (Lancelot, Large American Flag, "
    "Tadorna) stand through fall and light freezes and overwinter in milder zones, roughly zone 7 "
    "and warmer, a zone lower under mulch. Very hardy types (Bandit, Giant Musselburgh) stand hard "
    "winters, roughly zone 5 to 6 and warmer, again hedged with mulch and snow cover. UMN reports "
    "some varieties take temperatures near 20°F without harm, and RHS confirms hardy winter leeks "
    "stand the coldest weather unprotected, sweetening with frost. These are hedged ranges, not hard "
    "cutoffs: microclimate, mulch, and a hard-freeze year all shift the line, so the model states "
    "viability as a range and leaves the per-zone call to the app.")
WH_SOURCES = ["umn_ext", "rhs", "cornell_ext", "usu_ext"]

# Crop-level description rewrites (fold in the variety spectrum; Trevor 2026-07-14).
DESCRIPTION_BEGINNER = ("A leek is a mild, sweet relative of the onion, but instead of a bulb you "
    "grow and eat the long white stem. Leeks take a long time, so most gardeners start them indoors "
    "in late winter and plant them deep, then pull soil up around the stems to keep the bottom part "
    "white and tender. The best thing about leeks is that they handle cold: they stand right in the "
    "garden through frost and even taste sweeter for it, so you can dig them up fresh from fall into "
    "winter instead of all at one time. Which leek you plant sets how late you can harvest: fast "
    "early types like King Richard are for late summer and fall, while very hardy overwintering "
    "types like Bandit and Giant Musselburgh are bred to stand out in the cold and be dug through "
    "winter.")
DESCRIPTION_SEASONED = ("Leek (Allium ampeloprasum) is the mild, sweet allium grown not for a bulb "
    "but for its long, thick, blanched white stem, or shank. It is a patient, long-season crop, "
    "usually started indoors in late winter and transplanted deep so soil can be earthed up around "
    "the stem to blanch it. Its great virtue is cold-hardiness: leeks stand in the garden through "
    "hard frost, sweetening with the cold, and are dug fresh from fall into winter rather than "
    "harvested all at once. There is no bulbing and no day-length requirement, so unlike onions you "
    "simply match the variety to how late you want to harvest: an early tender type like King "
    "Richard for summer and fall, hardy maincrop types like Lancelot through the fall, and very "
    "hardy overwinterers like Bandit or Giant Musselburgh to stand through winter into spring.")


def build_variety(vd):
    src = vd["_src"]
    v = {
        "id": vd["id"], "name": vd["name"], "maturity_class": vd["maturity_class"],
        "is_reference": vd.get("is_reference", False),
        "days_to_maturity": vd["days_to_maturity"], "cold_hardiness_class": vd["cold_hardiness_class"],
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
    leek = next(c for c in data["crops"] if c.get("slug") == "leek")

    varieties = [build_variety(vd) for vd in VARDEFS]
    refs = [v["id"] for v in varieties if v["is_reference"]]
    assert refs == ["lancelot"], f"exactly one flagship expected (lancelot), got {refs}"

    cited = sorted({i for v in varieties for i in v["sources"]})

    current_varieties = leek["varieties"]
    new_varieties = dict(current_varieties)
    new_varieties["recommended"] = varieties
    # varieties-level note_beginner/note_seasoned/sources/anchoring_urls carried forward VERBATIM
    # from the loaded canonical -- not rewritten here.

    winter_hardiness = {
        "explainer_beginner": WH_EXPLAINER_BEGINNER,
        "explainer_seasoned": WH_EXPLAINER_SEASONED,
        "sources": WH_SOURCES,
        "anchoring_urls": {i: {"url": URL[i], "verified": VERIFIED} for i in WH_SOURCES},
    }

    current_gating = leek["gating_factors"]
    new_gating = sorted(set(current_gating) | {"winter_hardiness"})

    current_desc_b = leek["description_beginner"]
    current_desc_s = leek["description_seasoned"]

    current_ss = leek["verification_status"]["source_set"]
    new_ss = sorted(set(current_ss) | {"cornell_ext"})

    patch = {"base_sha": sha, "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='leek')].variety_archetype",
         "value": "hardiness_annual"},
        {"op": "add", "json_path": "$.crops[?(@.slug=='leek')].winter_hardiness",
         "value": winter_hardiness},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].gating_factors",
         "from": current_gating, "value": new_gating},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].varieties",
         "from": current_varieties, "value": new_varieties},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].description_beginner",
         "from": current_desc_b, "value": DESCRIPTION_BEGINNER},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].description_seasoned",
         "from": current_desc_s, "value": DESCRIPTION_SEASONED},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='leek')].verification_status.source_set",
         "from": current_ss, "value": new_ss},
    ]}
    os.makedirs("tools/batches", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(varieties)} varieties, cited T1 {cited}, "
          f"source_set +{sorted(set(cited) - set(current_ss))}, "
          f"gating_factors {current_gating} -> {new_gating})")


if __name__ == "__main__":
    main()
