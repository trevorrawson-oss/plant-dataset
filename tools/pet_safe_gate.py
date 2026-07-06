#!/usr/bin/env python3
"""pet_safe schema gate (post-114 backlog §A) -- validates the consumer-facing pet-toxicity
icon field. Structural + source-tier only; runs OFFLINE (never hits the network -- URL LIVENESS
is a separate --online sweep, shared with §B). The affirmative-non-toxic requirement for `safe`
is review-enforced, not machine-checkable here.

Usage:
  python3 tools/pet_safe_gate.py [crops_data_final.json] [--slugs a,b,c | --all-certified]
Exit 1 on any schema violation OR any required slug missing pet_safe (coverage gap); else 0.
"""
ENUM = {"safe", "toxic", "caution"}
ANIMALS = {"cats", "dogs", "horses"}


def pet_safe_violations(crop, catalog):
    """Return a list of violation strings ([] = clean) for one crop's pet_safe block.
    Absent pet_safe returns [] (coverage_report owns presence)."""
    V = []
    slug = crop.get("slug", "?")
    ps = crop.get("pet_safe")
    if ps is None:
        return V
    if not isinstance(ps, dict):
        return [f"{slug}: pet_safe must be an object, got {type(ps).__name__}"]
    status = ps.get("status")
    if status not in ENUM:
        V.append(f"{slug}: pet_safe.status {status!r} not in {sorted(ENUM)}")
    note = ps.get("note")
    affects = ps.get("affects")
    if status in {"toxic", "caution"}:
        if not (isinstance(note, str) and note.strip()):
            V.append(f"{slug}: pet_safe.note required (non-empty) when status={status!r}")
        if not (isinstance(affects, list) and affects):
            V.append(f"{slug}: pet_safe.affects required (non-empty) when status={status!r}")
    if affects is not None and (not isinstance(affects, list) or any(a not in ANIMALS for a in affects)):
        V.append(f"{slug}: pet_safe.affects {affects!r} must be a subset of {sorted(ANIMALS)}")
    srcs = ps.get("sources")
    if not (isinstance(srcs, list) and srcs):
        V.append(f"{slug}: pet_safe.sources must be a non-empty list")
        srcs = []
    for s in srcs:
        entry = catalog.get(s)
        if entry is None:
            V.append(f"{slug}: pet_safe source {s!r} not in source_catalog")
        elif entry.get("tier") != "T1":
            V.append(f"{slug}: pet_safe source {s!r} is not T1 (tier={entry.get('tier')!r})")
    anch = ps.get("anchoring_urls")
    if not isinstance(anch, dict):
        V.append(f"{slug}: pet_safe.anchoring_urls must be an object")
        anch = {}
    for s in srcs:
        rec = anch.get(s)
        if not isinstance(rec, dict) or not rec.get("url"):
            V.append(f"{slug}: pet_safe.anchoring_urls[{s!r}] missing a non-null url")
    # field_additions provenance (amend-not-recert): a CERTIFIED crop carrying pet_safe must log it.
    # (Newly-certified crops that get pet_safe natively via fold-in are a future case, revisit then.)
    if crop.get("verification_status", {}).get("status") == "verified_gs_arc":
        fa = crop.get("verification_status", {}).get("field_additions") or []
        if not any(isinstance(e, dict) and e.get("field") == "pet_safe" for e in fa):
            V.append(f"{slug}: pet_safe present on a certified crop but no field_additions entry for it")
    return V


def coverage_report(crops, required_slugs):
    """Return (counts, unset). counts = {status: n} over ALL crops carrying a valid status;
    unset = sorted required_slugs that lack a valid pet_safe status."""
    counts = {"safe": 0, "toxic": 0, "caution": 0}
    present = set()
    for c in crops:
        ps = c.get("pet_safe")
        if isinstance(ps, dict) and ps.get("status") in counts:
            counts[ps["status"]] += 1
            present.add(c.get("slug"))
    unset = sorted(s for s in required_slugs if s not in present)
    return counts, unset


if __name__ == "__main__":
    import argparse
    import json
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="crops_data_final.json")
    ap.add_argument("--slugs", help="comma-separated slugs REQUIRED to carry pet_safe (pilot scope)")
    ap.add_argument("--all-certified", action="store_true",
                    help="require pet_safe on ALL verified_gs_arc crops (rollout scope)")
    a = ap.parse_args()

    data = json.load(open(a.path, encoding="utf-8"))
    catalog = data.get("source_catalog", {})
    crops = data["crops"]

    total = 0
    for c in crops:
        for v in pet_safe_violations(c, catalog):
            print(f"  VIOLATION: {v}")
            total += 1

    required = set()
    if a.slugs:
        required = {s.strip() for s in a.slugs.split(",") if s.strip()}
    elif a.all_certified:
        required = {c.get("slug") for c in crops
                    if c.get("verification_status", {}).get("status") == "verified_gs_arc"}
    counts, unset = coverage_report(crops, required)

    print(f"pet_safe coverage: safe={counts['safe']} toxic={counts['toxic']} "
          f"caution={counts['caution']} | unset(required)={len(unset)}")
    if unset:
        print(f"  UNSET (required but missing pet_safe): {unset}")

    sys.exit(1 if (total or unset) else 0)
