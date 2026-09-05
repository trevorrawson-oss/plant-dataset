#!/usr/bin/env python3
"""prep -- build the PLA-8 batch 26 (trees and shrubs) staging artefacts from canonical.

READ-ONLY on canonical. Refuses to run if canonical has moved off the pinned base, so every
artefact handed to a fan-out agent is provably a projection of ONE known state.

Artefacts (all in this directory):
  <crop>_source.json            the full crop record, for reviewers who need context beyond problems
  records_problems.json         {crop: {pests: [...], diseases: [...]}} -- the entries under review
  control_methods.json          the 64-method catalog the ladders point into
  source_catalog_admission.txt  every citable catalog key: key, tier, class, name, url, citable_for
  shipped_precedents.json       SHAPE-ONLY exemplars: laddered FULL-schema entries on ids this batch
                                may join, plus whole laddered tree crops as comparable archetypes
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CANON = os.path.join(REPO, "crops_data_final.json")
EXPECTED_SHA = "ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144"

CROPS = ["mulberry", "pawpaw", "pear-asian", "pear-european", "persimmon", "pomegranate"]
# ids this batch may JOIN (decided after the record pass; listed here so exemplars are on hand)
REUSED_CANDIDATES = ["codling-moth", "fire-blight", "stink-bugs", "aphids", "whiteflies", "mealybugs",
                     "scale-insects", "gray-mold", "anthracnose", "birds", "raccoons",
                     "birds-and-squirrels", "crown-and-root-rot", "phytophthora-root-rot",
                     "bacterial-blight", "aster-yellows", "san-jose-scale", "peachtree-borer"]
COMPARABLE = ["fig", "peach", "plum", "lemon", "blueberry"]  # apple is NOTE-schema, measured
FULL = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
        "organic_treatment_beginner", "organic_treatment_seasoned",
        "prevention_beginner", "prevention_seasoned")


def main():
    raw = open(CANON, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    if got != EXPECTED_SHA:
        sys.exit(f"REFUSING: canonical is {got[:8]}, prep is pinned to {EXPECTED_SHA[:8]}")
    data = json.loads(raw.decode("utf-8"))
    by = {c["slug"]: c for c in data["crops"]}

    def dump(name, obj):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    for c in CROPS:
        dump(f"{c}_source.json", by[c])
    dump("records_problems.json", {c: {f: by[c].get(f) or [] for f in ("pests", "diseases")}
                                   for c in CROPS})
    dump("control_methods.json", data["control_methods"])

    cat = data["source_catalog"]
    with open(os.path.join(HERE, "source_catalog_admission.txt"), "w", encoding="utf-8") as f:
        f.write("# key\ttier\tsource_class\tname\turl\tcitable_for   (catalog on %s)\n" % got[:8])
        for k in sorted(cat):
            e = cat[k]
            f.write("\t".join(str(e.get(x) or "").replace("\t", " ").replace("\n", " ")
                              for x in ("id", "tier", "source_class", "name", "url", "citable_for"))
                    + "\n")

    # shipped precedents: FULL schema only, laddered only, never a batch crop
    def is_full(p):
        return all(p.get(k) for k in FULL) and p.get("control_ladder")
    by_id = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for field in ("pests", "diseases"):
            for p in c.get(field) or []:
                if p.get("id") in REUSED_CANDIDATES and is_full(p):
                    rec = {"crop": c["slug"], "field": field}
                    rec.update(p)
                    by_id.setdefault(p["id"], []).append(rec)
    for k in by_id:
        by_id[k] = by_id[k][:3]
    by_crop = {}
    for slug in COMPARABLE:
        c = by[slug]
        rows = [dict({"field": f}, **p) for f in ("pests", "diseases") for p in c.get(f) or []
                if is_full(p)]
        if not rows:
            sys.exit(f"comparable crop {slug} has no FULL-schema laddered problems; pick another")
        by_crop[slug] = rows
    dump("shipped_precedents.json", {
        "_what": ("SHAPE REFERENCE ONLY. Copying any sentence here fails the batch: a promote guard "
                  "compares every authored note against the whole shipped corpus with rare n-grams "
                  "and a similarity ratio taken in BOTH orders, and it has caught multi-donor "
                  "recombination before. Use these to see how long a rung note runs and how the two "
                  "registers differ, then write your own from your record report."),
        "_schema": ("Every entry here is FULL schema (symptoms_*/cause_*/organic_treatment_*/"
                    "prevention_*) and laddered. NOTE-schema crops are excluded: comparing prose "
                    "against one compares absent fields to absent fields and reports identity."),
        "by_reused_id": by_id, "by_comparable_crop": by_crop})

    n = sum(len(by[c].get(f) or []) for c in CROPS for f in ("pests", "diseases"))
    print(f"prep OK on {got[:8]}: {len(CROPS)} crops, {n} problem entries, "
          f"{len(cat)} catalog keys, precedents for {sorted(by_id)} + {COMPARABLE}")


if __name__ == "__main__":
    main()
