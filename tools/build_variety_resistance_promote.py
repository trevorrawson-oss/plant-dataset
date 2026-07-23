#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT promote patch for the variety disease-resistance pilot (apple +
strawberry; spec 2026-07-23-variety-resistance-pilot-design.md). Assembles FOUR staged content
drops into ONE atomic batch:

  1. control_methods    -- current 24 + 13 NEW methods (fruit_bagging, kaolin_clay, ... straw_mulch),
                            staged at tools/staging/variety_resist_catalog_content.json.
  2. source_catalog      -- current + NEW T1 entries: the 2 catalog-content additions
                            (ohio_state_ext, ucanr_ext_woolly_apple_aphid) + 7 resistance-table
                            page-specific sub-ids (cornell_ext_apple_disease/apple_scab/
                            apple_fireblight, purdue_ext_bp132w, umn_ext_apple_scab,
                            cornell_ext_strawberry_redstele, ncsu_ext_strawberry_anthracnose,
                            umaine_ext_2184). See NEW_SOURCES below; every id is T1.
  3. Apple/Strawberry `pests` + `diseases` -- REPLACED wholesale by the migrated ladder content
     (tools/staging/{apple,strawberry}_ladders_content.json): drops the legacy organic_treatment_*
     fields, adds a stable kebab `id` + ordered `control_ladder` per problem (Scope B, the
     pest/IPM control-ladder arc's vocabulary that this pilot's `resistance` keys reference).
  4. Apple/Strawberry `varieties` -- the current object with (a) each graded variety's `resistance`
     map merged onto its row (tools/staging/{apple,strawberry}_resistance_content.json:
     {variety_id: {disease_id: grade}}), and (b) the resistance-table source ids folded into
     varieties.sources / varieties.anchoring_urls (crop-level, not per-variety). Strawberry also
     picks up the already-catalogued `mu_ext` (Missouri G6135), which resistance_sources.md cites as
     a corroborating source for 4 of the 6 graded strawberry varieties (earliglow/jewel/allstar/
     tristar) -- the "+ any other strawberry-grade source named" clause in the task-9 brief.

HONESTY MODEL (carried from the staged content, not re-derived here): a `resistance` grade exists
ONLY where a fetched T1 source states a level for that exact cultivar; absence is silence, not a
default. This builder does not invent or drop grades -- it is pure assembly + referential
self-checking of what Tasks 4-8 already produced and reviewed.

SELF-CHECKS (assert before writing the batch; a failure here means the staged content and this
builder disagree, not that the gates will catch it later):
  - every control_ladder `method` in the rebuilt apple/strawberry pests+diseases resolves in the
    MERGED control_methods catalog;
  - every `resistance` key on every graded apple/strawberry variety equals an `id` present in that
    crop's REBUILT pests+diseases (never the pre-migration set);
  - every source id cited anywhere in the rebuilt apple/strawberry content (pests/diseases/
    varieties) resolves in the MERGED source_catalog, at tier T1.

All `from` guards are read from the LOADED canonical (never hand-typed), so apply_patch's
from-guards cannot silently drift against a stale assumption.

Run: python3 tools/build_variety_resistance_promote.py
"""
import hashlib
import json
import os

CANON = "crops_data_final.json"
STAGING = "tools/staging"
OUT = "tools/batches/variety_resistance_promote.json"
VERIFIED = "2026-07-23"

CATALOG_CONTENT = f"{STAGING}/variety_resist_catalog_content.json"
APPLE_LADDERS = f"{STAGING}/apple_ladders_content.json"
STRAWBERRY_LADDERS = f"{STAGING}/strawberry_ladders_content.json"
APPLE_RESISTANCE = f"{STAGING}/apple_resistance_content.json"
STRAWBERRY_RESISTANCE = f"{STAGING}/strawberry_resistance_content.json"

# -- NEW source_catalog entries (all T1). Two are the catalog-content additions (ladder-level
# claims); seven are page-specific sub-ids under already-catalogued T1 parents, minted here to
# anchor the resistance-table provenance without a one-id/two-url collision (the umn_ext_broccoli /
# ucanr_ext_8256 precedent). URLs + verification dates are taken verbatim from
# tools/staging/variety_resist_catalog_sources.md and tools/staging/resistance_sources.md.
NEW_SOURCES = {
    "ohio_state_ext": {
        "id": "ohio_state_ext",
        "name": "Ohio State University Extension (Ohioline)",
        "publisher": "Ohio State University Extension",
        "url": "https://ohioline.osu.edu/factsheet/plpath-fru-36",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Ohio State University Extension (Ohioline) factsheet PLPATH-FRU-36, "
                         "Botrytis Fruit Rot (Gray Mold) of strawberry; anchors the straw-mulch "
                         "fruit-rot barrier claim. A standalone institution, distinct from osu_ext "
                         "(Oregon State University)."),
        "_admission_provenance": ("Minted 2026-07-23 (variety-resistance pilot, Task 4 catalog "
                                   "additions). Verified 2026-07-23."),
    },
    "ucanr_ext_woolly_apple_aphid": {
        "id": "ucanr_ext_woolly_apple_aphid",
        "name": "UC IPM -- Woolly Apple Aphid (home garden)",
        "publisher": "UC ANR / UC IPM",
        "url": "https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/PESTS/woolyapaph.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("UC IPM home-garden Woolly Apple Aphid page; anchors "
                         "horticultural_oil's partial-control-of-aphids claim, distinct from the "
                         "pn7405 spider-mite page. Parent portal entry: ucanr_ext."),
        "_admission_provenance": ("Minted 2026-07-23 (variety-resistance pilot Task 4 "
                                   "fidelity-review IMPORTANT fix). Page sub-id under the trusted "
                                   "parent ucanr_ext (T1); inherits tier. Verified 2026-07-23."),
    },
    "cornell_ext_apple_disease": {
        "id": "cornell_ext_apple_disease",
        "name": "Cornell Apple Variety Database -- Disease Susceptibility Ranking of Apples",
        "publisher": "Cornell University",
        "url": "https://blogs.cornell.edu/applevarietydatabase/disease-susceptibility-of-common-apples/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Cornell Apple Variety Database disease-susceptibility table (fire blight, "
                         "apple scab, powdery mildew, cedar-apple rust, leaf spots) across common "
                         "apple cultivars; the primary source for the apple variety resistance "
                         "matrix. Parent portal entry: cornell_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 7). Verified 2026-07-23.",
    },
    "cornell_ext_apple_scab": {
        "id": "cornell_ext_apple_scab",
        "name": "Cornell Khan Lab -- Apple Scab Susceptibility of Common Cultivars",
        "publisher": "Cornell University (Khan Lab, Cornell AgriTech Geneva)",
        "url": "https://blogs.cornell.edu/khanlab/extension/apple-scab-susceptibility-of-common-cultivars/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Cornell AgriTech (Geneva) Khan Lab apple-scab susceptibility ranking, "
                         "corroborating the apple scab resistance grades. Parent portal entry: "
                         "cornell_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 7). Verified 2026-07-23.",
    },
    "cornell_ext_apple_fireblight": {
        "id": "cornell_ext_apple_fireblight",
        "name": "Cornell Khan Lab -- Fire Blight Susceptibility of Common Apple Cultivars",
        "publisher": "Cornell University (Khan Lab, Cornell AgriTech Geneva)",
        "url": "https://blogs.cornell.edu/khanlab/extension/fire-blight-susceptibility-of-common-apple-cultivars/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Cornell AgriTech (Geneva) Khan Lab fire-blight susceptibility ranking, "
                         "corroborating the apple fire-blight resistance grades. Parent portal "
                         "entry: cornell_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 7). Verified 2026-07-23.",
    },
    "purdue_ext_bp132w": {
        "id": "purdue_ext_bp132w",
        "name": "Purdue Extension BP-132-W -- Disease Susceptibility of Common Apple Cultivars",
        "publisher": "Purdue University Cooperative Extension",
        "url": "https://www.extension.purdue.edu/extmedia/BP/BP-132-W.pdf",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Purdue Extension BP-132-W (Beckerman), an independent disease-"
                         "susceptibility table for apple scab, fire blight, juniper rusts "
                         "(cedar-apple rust), and powdery mildew across common cultivars; the "
                         "second independent apple variety resistance source. Parent portal "
                         "entry: purdue_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 7). Verified 2026-07-23.",
    },
    "umn_ext_apple_scab": {
        "id": "umn_ext_apple_scab",
        "name": "UMN Extension -- Apple scab of apples and crabapples",
        "publisher": "UMN Extension",
        "url": "https://extension.umn.edu/plant-diseases/apple-scab",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("UMN Extension apple-scab page; supplies the explicit \"immune\" wording "
                         "governing Liberty's apple-scab resistance grade. Parent portal entry: "
                         "umn_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 7). Verified 2026-07-23.",
    },
    "cornell_ext_strawberry_redstele": {
        "id": "cornell_ext_strawberry_redstele",
        "name": "Cornell -- Red Stele Root Rot of Strawberry",
        "publisher": "Cornell University",
        "url": "https://blogs.cornell.edu/livegpath/gallery/strawberries/red-stele-root-rot-of-strawberry/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("Cornell (LivGpath) Red Stele Root Rot of Strawberry page; corroborates "
                         "the strawberry red-stele resistant-variety list (Earliglow, Allstar, "
                         "Tristar). Parent portal entry: cornell_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 8). Verified 2026-07-23.",
    },
    "ncsu_ext_strawberry_anthracnose": {
        "id": "ncsu_ext_strawberry_anthracnose",
        "name": "NC State Extension -- Anthracnose Fruit Rot of Strawberry",
        "publisher": "NC State University",
        "url": "https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-strawberry",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("NC State Extension Anthracnose Fruit Rot of Strawberry page; the sole "
                         "source naming Albion as susceptible to anthracnose fruit rot on black "
                         "plastic. Parent portal entry: ncsu_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 8). Verified 2026-07-23.",
    },
    "umaine_ext_2184": {
        "id": "umaine_ext_2184",
        "name": "UMaine Extension Bulletin #2184 -- Strawberry Varieties for Maine",
        "publisher": "University of Maine Cooperative Extension",
        "url": "https://extension.umaine.edu/publications/2184e/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-07",
        "tier": "T1",
        "citable_for": ("UMaine Cooperative Extension Bulletin #2184, Strawberry Varieties for "
                         "Maine; the primary source for the per-variety red-stele and "
                         "verticillium-wilt resistance grades. Parent portal entry: umaine_ext."),
        "_admission_provenance": "Minted 2026-07-23 (variety-resistance pilot Task 8). Verified 2026-07-23.",
    },
}

# Resistance-table source ids folded into each crop's crop-level `varieties.sources` /
# `varieties.anchoring_urls` (NOT per-variety -- see task-9 brief step 4). mu_ext is already
# catalogued (T1, generic Missouri Extension parent) so it needs no NEW_SOURCES entry; its url here
# is the specific G6135 strawberry-cultivar circular resistance_sources.md cites.
APPLE_RESIST_SOURCE_URLS = {
    "cornell_ext_apple_disease": NEW_SOURCES["cornell_ext_apple_disease"]["url"],
    "cornell_ext_apple_scab": NEW_SOURCES["cornell_ext_apple_scab"]["url"],
    "cornell_ext_apple_fireblight": NEW_SOURCES["cornell_ext_apple_fireblight"]["url"],
    "purdue_ext_bp132w": NEW_SOURCES["purdue_ext_bp132w"]["url"],
    "umn_ext_apple_scab": NEW_SOURCES["umn_ext_apple_scab"]["url"],
}
STRAWBERRY_RESIST_SOURCE_URLS = {
    "umaine_ext_2184": NEW_SOURCES["umaine_ext_2184"]["url"],
    "cornell_ext_strawberry_redstele": NEW_SOURCES["cornell_ext_strawberry_redstele"]["url"],
    "ncsu_ext_strawberry_anthracnose": NEW_SOURCES["ncsu_ext_strawberry_anthracnose"]["url"],
    "mu_ext": "https://extension.missouri.edu/publications/g6135",
}


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def crop(data, name):
    return next(c for c in data["crops"] if c.get("name") == name)


def merge_control_methods(current, new_methods):
    dup = set(current) & set(new_methods)
    assert not dup, f"control_methods id collision (already catalogued): {sorted(dup)}"
    merged = dict(current)
    merged.update(new_methods)
    return merged


def merge_source_catalog(current, new_sources):
    dup = set(current) & set(new_sources)
    assert not dup, f"source_catalog id collision (already catalogued): {sorted(dup)}"
    for sid, s in new_sources.items():
        assert s.get("tier") == "T1", f"{sid}: NEW_SOURCES entry must be tier T1"
    merged = dict(current)
    merged.update(new_sources)
    return merged


def assert_ladders_resolve(label, problems, methods_catalog):
    """Every control_ladder rung's method resolves in the (merged) control_methods catalog."""
    for p in problems:
        for rung in (p.get("control_ladder") or []):
            mid = rung.get("method")
            assert mid in methods_catalog, f"{label}/{p.get('id')}: unknown control_ladder method {mid!r}"


def build_varieties(crop_label, current_varieties, resistance_map, extra_source_urls, valid_problem_ids):
    """Return a new `varieties` object: current_varieties with each graded variety's `resistance`
    map merged onto its row, and the resistance-table source ids folded into
    varieties.sources/anchoring_urls. Every resistance id is asserted against valid_problem_ids
    (the REBUILT pests+diseases id set for this crop, not the pre-migration one)."""
    new_recommended = []
    graded_ids = set()
    for v in current_varieties["recommended"]:
        v = dict(v)
        grades = resistance_map.get(v["id"])
        if grades:
            for did in grades:
                assert did in valid_problem_ids, (
                    f"{crop_label}/{v['id']}: resistance id {did!r} is not a pest/disease id "
                    f"on the rebuilt {crop_label} (known: {sorted(valid_problem_ids)})")
            v["resistance"] = dict(grades)
            graded_ids.add(v["id"])
        new_recommended.append(v)

    orphaned = set(resistance_map) - graded_ids
    assert not orphaned, f"{crop_label}: resistance content cites unknown variety id(s) {sorted(orphaned)}"

    new_varieties = dict(current_varieties)
    new_varieties["recommended"] = new_recommended

    cur_sources = current_varieties.get("sources") or []
    new_varieties["sources"] = sorted(set(cur_sources) | set(extra_source_urls))

    cur_anchors = current_varieties.get("anchoring_urls") or {}
    new_anchors = dict(cur_anchors)
    for sid, url in extra_source_urls.items():
        new_anchors[sid] = {"url": url, "verified": VERIFIED}
    new_varieties["anchoring_urls"] = new_anchors
    return new_varieties


def collect_source_ids(obj):
    """Recursively collect every id referenced via a `sources` list or `anchoring_urls` dict key
    anywhere under obj (mirrors whole_crop_gate's E.source-tier src_walk)."""
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "sources" and isinstance(v, list):
                    ids.update(x for x in v if isinstance(x, str))
                if k == "anchoring_urls" and isinstance(v, dict):
                    ids.update(v.keys())
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(obj)
    return ids


def assert_sources_resolve(label, pieces, catalog):
    cited = set()
    for piece in pieces:
        cited |= collect_source_ids(piece)
    missing = sorted(s for s in cited if s not in catalog)
    assert not missing, f"{label}: source id(s) not in rebuilt source_catalog: {missing}"
    non_t1 = sorted(s for s in cited if catalog[s].get("tier") != "T1")
    assert not non_t1, f"{label}: non-T1 source id(s) cited: {non_t1}"
    return cited


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)

    catalog_new_methods = load_json(CATALOG_CONTENT)
    apple_ladders = load_json(APPLE_LADDERS)
    sb_ladders = load_json(STRAWBERRY_LADDERS)
    apple_resistance = load_json(APPLE_RESISTANCE)
    sb_resistance = load_json(STRAWBERRY_RESISTANCE)

    assert len(catalog_new_methods) == 13, f"expected 13 new control_methods, got {len(catalog_new_methods)}"

    current_methods = data["control_methods"]
    new_methods = merge_control_methods(current_methods, catalog_new_methods)

    current_catalog = data["source_catalog"]
    new_catalog = merge_source_catalog(current_catalog, NEW_SOURCES)

    apple = crop(data, "Apple")
    strawberry = crop(data, "Strawberry")

    cur_apple_pests, cur_apple_diseases = apple["pests"], apple["diseases"]
    cur_sb_pests, cur_sb_diseases = strawberry["pests"], strawberry["diseases"]

    new_apple_pests, new_apple_diseases = apple_ladders["pests"], apple_ladders["diseases"]
    new_sb_pests, new_sb_diseases = sb_ladders["pests"], sb_ladders["diseases"]

    assert_ladders_resolve("apple", new_apple_pests + new_apple_diseases, new_methods)
    assert_ladders_resolve("strawberry", new_sb_pests + new_sb_diseases, new_methods)

    apple_problem_ids = {p["id"] for p in new_apple_pests + new_apple_diseases}
    sb_problem_ids = {p["id"] for p in new_sb_pests + new_sb_diseases}

    new_apple_varieties = build_varieties(
        "apple", apple["varieties"], apple_resistance, APPLE_RESIST_SOURCE_URLS, apple_problem_ids)
    new_sb_varieties = build_varieties(
        "strawberry", strawberry["varieties"], sb_resistance, STRAWBERRY_RESIST_SOURCE_URLS, sb_problem_ids)

    apple_cited = assert_sources_resolve(
        "apple", [new_apple_pests, new_apple_diseases, new_apple_varieties], new_catalog)
    sb_cited = assert_sources_resolve(
        "strawberry", [new_sb_pests, new_sb_diseases, new_sb_varieties], new_catalog)

    patches = [
        {"op": "replace", "json_path": "$.control_methods",
         "from": current_methods, "value": new_methods},
        {"op": "replace", "json_path": "$.source_catalog",
         "from": current_catalog, "value": new_catalog},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Apple')].pests",
         "from": cur_apple_pests, "value": new_apple_pests},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Apple')].diseases",
         "from": cur_apple_diseases, "value": new_apple_diseases},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Apple')].varieties",
         "from": apple["varieties"], "value": new_apple_varieties},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Strawberry')].pests",
         "from": cur_sb_pests, "value": new_sb_pests},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Strawberry')].diseases",
         "from": cur_sb_diseases, "value": new_sb_diseases},
        {"op": "replace", "json_path": "$.crops[?(@.name=='Strawberry')].varieties",
         "from": strawberry["varieties"], "value": new_sb_varieties},
    ]

    patch = {"base_sha": sha, "patches": patches}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(patch, fh, ensure_ascii=False, indent=1)

    print(f"wrote {OUT} (base_sha {sha[:12]}, {len(patches)} ops)")
    print(f"  control_methods {len(current_methods)} -> {len(new_methods)} "
          f"(+{sorted(set(new_methods) - set(current_methods))})")
    print(f"  source_catalog {len(current_catalog)} -> {len(new_catalog)} "
          f"(+{sorted(set(new_catalog) - set(current_catalog))})")
    print(f"  apple pests {len(cur_apple_pests)}->{len(new_apple_pests)}, "
          f"diseases {len(cur_apple_diseases)}->{len(new_apple_diseases)}, "
          f"graded varieties {sorted(apple_resistance)}")
    print(f"  strawberry pests {len(cur_sb_pests)}->{len(new_sb_pests)}, "
          f"diseases {len(cur_sb_diseases)}->{len(new_sb_diseases)}, "
          f"graded varieties {sorted(sb_resistance)}")
    print(f"  apple varieties.sources +{sorted(set(APPLE_RESIST_SOURCE_URLS))}")
    print(f"  strawberry varieties.sources +{sorted(set(STRAWBERRY_RESIST_SOURCE_URLS))}")
    print(f"  distinct source ids cited: apple {len(apple_cited)}, strawberry {len(sb_cited)}")


if __name__ == "__main__":
    main()
