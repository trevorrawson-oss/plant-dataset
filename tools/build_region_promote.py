#!/usr/bin/env python3
"""Emit the atomic region-column promote batch from the staging files.

Deterministic; performs NO canonical write. Reads the 4 per-class cell staging
files + the chill-band file for <region_id>, emits one apply_patch batch:
  {"base_sha": <live canonical sha256>, "patches": [ add $.crops[?slug].regions.<rid>, ...,
   add $.region_chill_delivered.<rid>, add $.region_chill_delivered_provenance.<rid> ]}

base_sha is stamped from the LIVE canonical at build time. If the canonical moves
before the promote (a concurrent arc lands), re-run this to re-stamp base_sha, or
override with --base-sha. apply_patch.py refuses to apply on a base_sha mismatch,
so a stale batch fails closed (never a silent clobber).

Usage: python3 tools/build_region_promote.py <region_id> [--base-sha SHA]
Generalized from build_rgv_promote.py (region_id param + region-keyed staging).
"""
import argparse
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANON = os.path.join(ROOT, "crops_data_final.json")

# region_id -> (per-class cell staging files, chill-band file)
STAGING = {
    "pnw": (["pnw_annuals.json", "pnw_trees.json", "pnw_citrus.json", "pnw_perennials.json"],
            "pnw_chill_band.json"),
    "mid_atlantic": (["mid_atlantic_annuals_cool.json", "mid_atlantic_annuals_warm.json",
                      "mid_atlantic_trees.json", "mid_atlantic_citrus.json",
                      "mid_atlantic_perennials.json"], "mid_atlantic_chill_band.json"),
    "mid_south": (["mid_south_annuals_cool.json", "mid_south_annuals_warm.json",
                   "mid_south_trees.json", "mid_south_citrus.json",
                   "mid_south_perennials.json"], "mid_south_chill_band.json"),
    "nevada": (["nevada_annuals_warm.json", "nevada_annuals_cool.json",
                "nevada_trees.json", "nevada_citrus.json",
                "nevada_perennials.json"], "nevada_chill_band.json"),
}
EXPECTED_CELLS = {"pnw": 108, "mid_atlantic": 111, "mid_south": 111, "nevada": 111}


def build(region_id, base_sha=None):
    cell_files, band_file = STAGING[region_id]
    if base_sha is None:
        base_sha = hashlib.sha256(open(CANON, "rb").read()).hexdigest()
    patches, seen = [], set()
    for fn in cell_files:
        cells = json.load(open(os.path.join(HERE, "staging", fn), encoding="utf-8"))
        for slug, cell in cells.items():
            assert slug not in seen, f"duplicate slug across staging files: {slug}"
            seen.add(slug)
            patches.append({
                "op": "add",
                "json_path": f"$.crops[?(@.slug=='{slug}')].regions.{region_id}",
                "value": cell,
            })
    band = json.load(open(os.path.join(HERE, "staging", band_file), encoding="utf-8"))
    canon = json.load(open(CANON, encoding="utf-8"))
    band_key = f"region_chill_delivered.{region_id}"
    prov_key = f"region_chill_delivered_provenance.{region_id}"
    # chill band: region_chill_delivered is a dict keyed by region -> add the new region key.
    patches.append({"op": "add", "json_path": f"$.region_chill_delivered.{region_id}",
                    "value": band[band_key]})
    # provenance: region_chill_delivered_provenance is a SINGLE global string (not a per-region
    # dict) -> REPLACE it with the current value + this region's note appended (space-joined,
    # each note self-labels with its region id -- matches the RGV precedent). `from` is the live
    # global string so apply_patch fails closed if it drifted.
    cur_prov = canon["region_chill_delivered_provenance"]
    pnw_note = band[prov_key]
    new_prov = cur_prov if pnw_note in cur_prov else cur_prov.rstrip() + " " + pnw_note
    patches.append({"op": "replace", "json_path": "$.region_chill_delivered_provenance",
                    "from": cur_prov, "value": new_prov})
    # NEW source_catalog entries (regions whose T1 sources were not pre-catalogued, e.g.
    # mid_south's UAEX/NWS publications). Optional file staging/<region>_sources.json =
    # {source_id: entry}. Each becomes an `add $.source_catalog.<id>` patch, landing in the
    # SAME atomic promote as the cells that cite them (so the canonical is never in a state
    # where a cell cites an uncatalogued source). Absent -> no source patches (rgv/pnw/
    # mid_atlantic, whose sources were already catalogued).
    src_path = os.path.join(HERE, "staging", f"{region_id}_sources.json")
    n_sources = 0
    if os.path.exists(src_path):
        new_sources = json.load(open(src_path, encoding="utf-8"))
        for sid, entry in new_sources.items():
            assert sid not in canon.get("source_catalog", {}), \
                f"source id {sid} already in source_catalog (would collide on add)"
            patches.append({"op": "add", "json_path": f"$.source_catalog.{sid}",
                            "value": entry})
            n_sources += 1
    exp = EXPECTED_CELLS.get(region_id)
    if exp is not None:
        assert len(seen) == exp, f"expected {exp} {region_id} cells, got {len(seen)}"
    return {"base_sha": base_sha, "patches": patches}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("region_id")
    ap.add_argument("--base-sha", default=None,
                    help="override base_sha (default: live canonical sha256)")
    a = ap.parse_args()
    batch = build(a.region_id, a.base_sha)
    out = os.path.join(HERE, "batches", f"{a.region_id}_region_promote.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=1)  # batch file may be pretty; canonical stays compact
    n_cells = sum(1 for p in batch["patches"] if p["json_path"].endswith(f".regions.{a.region_id}"))
    n_src = sum(1 for p in batch["patches"] if p["json_path"].startswith("$.source_catalog."))
    n_top = len(batch["patches"]) - n_cells - n_src
    print(f"emitted {len(batch['patches'])} patches ({n_cells} {a.region_id} cells + {n_top} top-level "
          f"+ {n_src} source_catalog); base_sha {batch['base_sha'][:12]}")


if __name__ == "__main__":
    main()
