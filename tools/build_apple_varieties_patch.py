#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching apple's varieties to the flat TREE schema (spec
2026-07-11-apple-variety-pilot-design). Batch 1 = the 13 existing + Jonagold + Mutsu (triploids) +
Dolgo (crabapple). Footprint = apple's `varieties` object + a new crop-level `variety_archetype:
"tree_fruit"` key + verification_status.source_set (adds the newly-cited T1 ids). No other crop moves.

DESIGN (see spec s3-6 + the source manifest, scratchpad/apple_source_manifest.md, Trevor-signed
2026-07-11):
- Per-variety `sources`/`anchoring_urls` carry T1 ONLY (bloom_group / ripening / pollination). Every
  variety has >=1 catalogued T1 source, so whole_crop_gate E.source-tier stays green. The gate FAILS
  any non-T1 cited source (src_walk collects every sources/anchoring_urls), and apple is already
  certified -- so nursery (T2) chill sources are NOT cited here.
- chill_hours_required is load-bearing but under-documented at T1 (extension chill data exists mainly
  for warm-climate varieties). Its honesty lives in per-variety `confidence_tier` (T1..T4) + the
  crop-level varieties.note transparency note, NOT in a fake nursery citation. Chill values + tiers
  are Trevor-signed (manifest sections B/C).
- bloom_window_relative is DERIVED from the sourced bloom_group by the fixed 5-band map below (real
  bloom overlaps, so bands overlap); identical for every variety in a group (finer sub-ordering is not
  independently sourced). Dolgo gets a widened window for its long, universal-pollinizer bloom.
- maturity_class = RIPENING season (early/mid/late), kept DISTINCT from bloom_group. The bloom-vs-ripen
  correction: Granny Smith + Pink Lady bloom MID but ripen late (was mis-encoded as late/very-late bloom).

Run: python3 tools/build_apple_varieties_patch.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
OUT = "tools/batches/apple_varieties_pilot.json"
VERIFIED = "2026-07-11"

# bloom_group -> bloom_window_relative (fraction of the regional bloom season; overlapping bands)
BAND = {"very_early": [0.0, 0.2], "early": [0.15, 0.4], "mid": [0.35, 0.62],
        "late": [0.58, 0.82], "very_late": [0.78, 1.0]}

URL = {
    "usu_ext": "https://extension.usu.edu/yardandgarden/research/apple-production-and-variety-recommendations-for-the-utah-home-garden",
    "tamu_agrilife": "https://aggie-horticulture.tamu.edu/fruit-nut/wp-content/uploads/sites/6/2015/04/apples_2015.pdf",
    "uf_ifas": "https://ask.ifas.ufl.edu/publication/MG368",
    "mu_ext": "https://extension.missouri.edu/media/wysiwyg/Extensiondata/Pub/pdf/agguides/hort/g06001.pdf",
    "umaine_ext": "https://extension.umaine.edu/fruit/growing-fruit-trees-in-maine/pollination-requirements/",
    "wsu_ext": "https://s3.wp.wsu.edu/uploads/sites/2076/2024/07/C105-Pollination-of-Fruit-Trees.pdf",
    "ncsu_jonagold": "https://plants.ces.ncsu.edu/plants/malus-domestica-jonagold/",
    "ncsu_mutsu": "https://plants.ces.ncsu.edu/plants/malus-domestica-mutsu/",
    "umn_zestar": "https://mnhardy.umn.edu/zestar",
    "umn_apples": "https://extension.umn.edu/fruit/growing-apples",
    "uariz_ext": "https://www.extension.arizona.edu/sites/default/files/2024-08/az1269.pdf",
    "cornell_liberty": "https://ecommons.cornell.edu/server/api/core/bitstreams/df23bb1a-03c3-4be1-a791-d1517d86dec9/content",
}

# Each variety: _src = [(source_id, url), ...] (T1 only). sources + anchoring_urls derive from it.
# self_fruitful present ONLY where it differs from the crop default (self_fertile=false -> "no").
VARDEFS = [
    # Low-chill trio: chill follows University of Arizona field-cropping evidence (the region model's
    # T1 source), NOT the higher STATED lab requirements from Texas A&M / UF-IFAS. Keeping the field
    # value keeps the chill floor consistent with the low-desert region calendars (Trevor 2026-07-11).
    dict(id="dorsett-golden", name="Dorsett Golden", bloom_group="very_early", maturity_class="early",
         bloom_duration_days=9, chill_hours_required=100, use="fresh eating", triploid=False,
         confidence_tier="T2",
         note_beginner="A low-chill apple bred for mild-winter gardens, sweet and good for fresh eating, ripening early. It pollinates Anna, and University of Arizona Extension reports it cropping well in the low desert.",
         note_seasoned="Low-chill dessert apple; University of Arizona reports it cropping in the low desert around 100 chill hours, though stated lab requirements run higher (Texas A&M 350, UF/IFAS 250 to 300). Very early bloom, early ripening, a reliable pollinizer for Anna.",
         _src=[("uariz_ext", URL["uariz_ext"])]),
    dict(id="anna", name="Anna", bloom_group="very_early", maturity_class="early",
         bloom_duration_days=9, chill_hours_required=200, use="fresh eating", triploid=False,
         confidence_tier="T2",
         note_beginner="One of the best apples for warm-winter regions, crisp and sweet, ripening very early. Plant it near Dorsett Golden so the two pollinate each other; it crops well in the low desert.",
         note_seasoned="Low-chill cultivar, about 200 chill hours as reported cropping in the Arizona low desert (stated lab figures run higher, 250 to 400). Very early bloom, early ripening; pair with Dorsett Golden or Ein Shemer.",
         _src=[("uariz_ext", URL["uariz_ext"])]),
    dict(id="ein-shemer", name="Ein Shemer", bloom_group="very_early", maturity_class="mid",
         bloom_duration_days=8, chill_hours_required=100, use="fresh eating, cooking", triploid=False,
         self_fruitful="partial", confidence_tier="T2",
         note_beginner="A low-chill yellow apple for mild winters, good fresh or cooked, ripening in mid-summer. It sets some fruit on its own but does better with a partner, and it crops in the low desert.",
         note_seasoned="Low-chill cultivar, around 100 chill hours per Arizona low-desert cropping reports (UF/IFAS states 450 as a lab requirement). Very early bloom, mid-season ripening; partially self-fruitful.",
         _src=[("uariz_ext", URL["uariz_ext"])]),
    dict(id="zestar", name="Zestar!", bloom_group="very_early", maturity_class="early",
         bloom_duration_days=9, chill_hours_required=800, use="fresh eating", triploid=False,
         confidence_tier="T4",
         note_beginner="An early-season eating apple from Minnesota, crisp and sweet-tart, ripening in late summer. It is very cold hardy, so winter chill is never the limiting factor where it grows.",
         note_seasoned="Cold-hardy UMN release, very early bloom, early (late-August) ripening. No chill-hour figure is established in the literature; chill is not limiting in its cold-climate range, so the value here is a placeholder.",
         _src=[("umn_ext", URL["umn_zestar"])]),
    dict(id="mcintosh", name="McIntosh", bloom_group="early", maturity_class="mid",
         bloom_duration_days=9, chill_hours_required=900, use="fresh eating, sauce", triploid=False,
         confidence_tier="T2",
         note_beginner="The classic tart, aromatic New England apple for fresh eating and sauce, ripening mid-season. It wants a good stretch of winter cold, so it suits colder regions.",
         note_seasoned="High-chill heirloom (nursery estimate near 900 hours), early-to-mid bloom, mid-season ripening. Tender flesh, excellent for sauce.",
         _src=[("usu_ext", URL["usu_ext"])]),
    dict(id="liberty", name="Liberty", bloom_group="early", maturity_class="mid",
         bloom_duration_days=9, chill_hours_required=800, use="fresh eating", triploid=False,
         confidence_tier="T2", disease_notes="Immune to apple scab; a strong low-spray choice.",
         note_beginner="A disease-resistant apple that shrugs off apple scab, so it is a great low-spray choice, good fresh, ripening mid to late season. A Cornell release built for easy backyard growing.",
         note_seasoned="Scab-immune Cornell cultivar, early bloom, ripe about ten days after McIntosh. Nursery chill estimate near 800 hours; a low-spray standout.",
         _src=[("cornell_ext", URL["cornell_liberty"])]),
    dict(id="empire", name="Empire", bloom_group="mid", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=700, use="fresh eating", triploid=False,
         self_fruitful="partial", confidence_tier="T2",
         note_beginner="A sweet, crisp McIntosh-type apple for fresh eating that ripens in early fall and stores well. It can set some fruit on its own but crops better with a partner nearby.",
         note_seasoned="McIntosh x Red Delicious, mid bloom, late ripening. Listed as partially self-fruitful (Missouri G6001) but sets more when cross-pollinated; nursery chill estimate 600 to 800 hours.",
         _src=[("usu_ext", URL["usu_ext"]), ("mu_ext", URL["mu_ext"])]),
    dict(id="honeycrisp", name="Honeycrisp", bloom_group="mid", maturity_class="mid",
         bloom_duration_days=10, chill_hours_required=800, use="fresh eating", triploid=False,
         confidence_tier="T2",
         note_beginner="The famously crisp, juicy snacking apple, ripening mid-season. It needs a different variety blooming at the same time to pollinate it.",
         note_seasoned="UMN release, mid-season bloom (Utah State labels it early; we keep the common mid classification), mid ripening. Needs a pollinizer; nursery chill estimate 800 to 1000 hours.",
         _src=[("usu_ext", URL["usu_ext"]), ("umn_ext", URL["umn_apples"])]),
    dict(id="gala", name="Gala", bloom_group="mid", maturity_class="mid",
         bloom_duration_days=9, chill_hours_required=600, use="fresh eating", triploid=False,
         self_fruitful="partial", confidence_tier="T1",
         note_beginner="A mild, sweet, reliable apple for fresh eating, ripening in September, and one of the most popular apples grown. It sets some fruit alone but does best with a partner.",
         note_seasoned="Mid bloom, mid ripening, about 600 chill hours (Texas A&M). Shows some self-fertility but crops better cross-pollinated; pairs well with Honeycrisp.",
         _src=[("usu_ext", URL["usu_ext"]), ("tamu_agrilife", URL["tamu_agrilife"]), ("mu_ext", URL["mu_ext"])]),
    dict(id="golden-delicious", name="Golden Delicious", bloom_group="mid", maturity_class="late",
         bloom_duration_days=10, chill_hours_required=700, use="fresh eating, cooking", triploid=False,
         is_reference=True, self_fruitful="partial", confidence_tier="T3",
         note_beginner="A sweet, all-purpose yellow apple that is also the most useful partner in the orchard: it pollinates almost any other apple. Good fresh or cooked, ripening late in the season.",
         note_seasoned="Near-universal pollinizer, partially self-fruitful (semi-self-pollinating per Utah State), mid bloom, late ripening. Chill figure is uncertain (nursery sources range 700 to 1500), so treat it as approximate; note it can be ineffective as a pollinizer for Mutsu.",
         _src=[("usu_ext", URL["usu_ext"]), ("mu_ext", URL["mu_ext"])]),
    dict(id="jonagold", name="Jonagold", bloom_group="mid", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=700, use="fresh eating", triploid=True,
         confidence_tier="T2",
         note_beginner="A large, honeyed, crisp apple that is wonderful fresh, ripening late in the season. Important catch: it cannot pollinate other trees, so it needs two other varieties nearby to fruit well.",
         note_seasoned="Triploid (sterile pollen), confirmed by NC State, Maine, and Missouri Extension; needs two non-triploid pollinizers. Mid bloom, late ripening; nursery chill estimate 700 to 800 hours.",
         _src=[("usu_ext", URL["usu_ext"]), ("ncsu_ext", URL["ncsu_jonagold"]),
               ("umaine_ext", URL["umaine_ext"]), ("mu_ext", URL["mu_ext"])]),
    dict(id="mutsu", name="Mutsu", bloom_group="mid", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=600, use="cooking, fresh eating", triploid=True,
         confidence_tier="T1",
         note_beginner="A big, crisp, slightly tart green-gold apple (also sold as Crispin), great fresh or cooked, ripening late. Like Jonagold it cannot pollinate others and needs two partners of its own.",
         note_seasoned="Triploid (sterile pollen), about 600 chill hours (Texas A&M). Mid bloom, late ripening; needs two non-triploid pollinizers, and Golden Delicious is not a reliable one for it.",
         _src=[("usu_ext", URL["usu_ext"]), ("tamu_agrilife", URL["tamu_agrilife"]),
               ("ncsu_ext", URL["ncsu_mutsu"]), ("umaine_ext", URL["umaine_ext"])]),
    dict(id="fuji", name="Fuji", bloom_group="late", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=600, use="fresh eating, storage", triploid=False,
         confidence_tier="T1",
         note_beginner="A very sweet, dense, long-keeping apple for fresh eating, ripening late in the season, and one of the most widely grown apples. It needs a pollinizer blooming at the same time.",
         note_seasoned="Late bloom, late ripening, about 600 chill hours (Texas A&M; UF/IFAS 575). Self-sterile; stores exceptionally well.",
         _src=[("usu_ext", URL["usu_ext"]), ("tamu_agrilife", URL["tamu_agrilife"])]),
    dict(id="granny-smith", name="Granny Smith", bloom_group="mid", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=600, use="cooking, fresh eating", triploid=False,
         self_fruitful="partial", confidence_tier="T1",
         note_beginner="The tart bright-green cooking and eating apple, ripening very late in the season. A useful point: it blooms in mid-season even though it ripens late, so it can pollinate the mid-season apples.",
         note_seasoned="Mid bloom but late ripening (the bloom/ripen split matters for pairing), about 600 chill hours (UF/IFAS). Listed as partially self-fruitful; needs a long warm season to finish.",
         _src=[("usu_ext", URL["usu_ext"]), ("uf_ifas", URL["uf_ifas"]), ("mu_ext", URL["mu_ext"])]),
    dict(id="pink-lady", name="Pink Lady", bloom_group="mid", maturity_class="late",
         bloom_duration_days=9, chill_hours_required=550, use="fresh eating, storage", triploid=False,
         confidence_tier="T2",
         note_beginner="A crisp, tangy-sweet pink apple that ripens the latest of all and stores for months. Like Granny Smith it blooms mid-season, so it can partner the mid-season apples even though its fruit finishes last.",
         note_seasoned="Cripps Pink; mid bloom, very late ripening (harvest October and later), 500 to 600 chill hours (Texas A&M). Self-sterile; the longest season of the set.",
         _src=[("tamu_agrilife", URL["tamu_agrilife"])]),
    dict(id="dolgo", name="Dolgo", bloom_group="early", bloom_window_relative=[0.15, 0.55],
         maturity_class="early", bloom_duration_days=21, chill_hours_required=500,
         use="pollinizer, jelly", triploid=False, self_fruitful="yes", confidence_tier="T2",
         note_beginner="A flowering crabapple that blooms early and for a long time, which makes it a near-universal pollinizer for a whole row of apples. Its small tart fruit is good for jelly, and it can set fruit on its own.",
         note_seasoned="Long, early bloom spanning several apple groups, so it pollinizes across early-to-mid varieties; self-fertile. Nursery chill estimate about 500 hours; ploidy is not confirmed in a citable source but it is used horticulturally as a fertile pollinizer.",
         _src=[("wsu_ext", URL["wsu_ext"])]),
]

# Crop-level variety-set note: pollination guidance (updated) + the chill-sourcing TRANSPARENCY note.
NOTE_BEGINNER = ("Plant at least two different varieties that bloom around the same time so they can "
                 "pollinate each other. Where winters are mild, choose low-chill kinds like Dorsett "
                 "Golden, Anna, or Ein Shemer. If summers are humid and you want to spray less, Liberty "
                 "resists apple scab. Golden Delicious pollinates almost anything and makes a reliable "
                 "partner, and a Dolgo crabapple blooms early and long enough to pollinate a whole row. "
                 "Two varieties here, Jonagold and Mutsu, cannot pollinate anything and need two other "
                 "partners themselves. One honest note on the numbers: bloom times, ripening, and "
                 "pollination come from university extension guides and are solid, but chill hours (the "
                 "winter cold a tree needs to fruit) are well documented only for warm-climate apples, "
                 "so several cold-climate varieties here carry nursery estimates and a few newer ones "
                 "like Zestar! have no firm figure yet. Treat the chill numbers as a guide, and check "
                 "each variety's confidence tier to see how sure we are.")
NOTE_SEASONED = ("Sixteen cultivars, thirteen dessert and cooking apples plus two triploids (Jonagold, "
                 "Mutsu) and the Dolgo crabapple pollinizer, with bloom group kept distinct from "
                 "ripening season. Pair overlapping bloom groups for cross-pollination; the triploids "
                 "carry sterile pollen and need two non-triploid partners. Bloom group, ripening, and "
                 "pollination are anchored to extension sources (Utah State, Missouri G6001, Texas A&M, "
                 "UF/IFAS, NC State, Maine). Chill-hour data is thinner: extension figures exist mainly "
                 "for warm-climate varieties where chill is limiting, so several cold-climate cultivars "
                 "carry nursery estimates and Zestar! has none established. Chill requirement is "
                 "model-dependent and shifts with local climate; read the per-variety confidence tier "
                 "as the honest measure of each figure.")


def build_variety(vd):
    src = vd.pop("_src")
    v = {
        "id": vd["id"], "name": vd["name"], "maturity_class": vd["maturity_class"],
        "bloom_group": vd["bloom_group"],
        "bloom_window_relative": vd.get("bloom_window_relative") or BAND[vd["bloom_group"]],
        "bloom_duration_days": vd["bloom_duration_days"],
        "chill_hours_required": vd["chill_hours_required"], "use": vd["use"],
        "triploid": vd["triploid"], "is_reference": vd.get("is_reference", False),
        "confidence_tier": vd["confidence_tier"],
        "note_beginner": vd["note_beginner"], "note_seasoned": vd["note_seasoned"],
        "sources": [i for i, _ in src],
        "anchoring_urls": {i: {"url": u, "verified": VERIFIED} for i, u in src},
    }
    if "self_fruitful" in vd:
        v["self_fruitful"] = vd["self_fruitful"]
    if "disease_notes" in vd:
        v["disease_notes"] = vd["disease_notes"]
    return v


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    ap = next(c for c in data["crops"] if c.get("slug") == "apple")

    varieties = [build_variety(dict(vd)) for vd in VARDEFS]
    refs = [v["id"] for v in varieties if v["is_reference"]]
    assert refs == ["golden-delicious"], f"exactly one flagship expected, got {refs}"

    cited = sorted({i for v in varieties for i in v["sources"]})

    current_varieties = ap["varieties"]
    new_varieties = dict(current_varieties)
    new_varieties["recommended"] = varieties
    new_varieties["note_beginner"] = NOTE_BEGINNER
    new_varieties["note_seasoned"] = NOTE_SEASONED
    new_varieties["sources"] = cited
    new_varieties["anchoring_urls"] = {i: {"url": URL_FOR(i), "verified": VERIFIED} for i in cited}

    current_ss = ap["verification_status"]["source_set"]
    new_ss = sorted(set(current_ss) | set(cited))

    patch = {"base_sha": sha, "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='apple')].variety_archetype", "value": "tree_fruit"},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='apple')].varieties",
         "from": current_varieties, "value": new_varieties},
        {"op": "replace", "json_path": "$.crops[?(@.slug=='apple')].verification_status.source_set",
         "from": current_ss, "value": new_ss},
    ]}
    os.makedirs("tools/batches", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)
    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(varieties)} varieties, cited T1 {cited}, "
          f"source_set +{sorted(set(cited) - set(current_ss))})")


def URL_FOR(i):
    # crop-level anchoring uses the canonical URL for each cited source id
    canon = {"usu_ext": URL["usu_ext"], "tamu_agrilife": URL["tamu_agrilife"], "uf_ifas": URL["uf_ifas"],
             "mu_ext": URL["mu_ext"], "umaine_ext": URL["umaine_ext"], "wsu_ext": URL["wsu_ext"],
             "ncsu_ext": URL["ncsu_jonagold"], "umn_ext": URL["umn_apples"], "cornell_ext": URL["cornell_liberty"],
             "uariz_ext": URL["uariz_ext"]}
    return canon[i]


if __name__ == "__main__":
    main()
