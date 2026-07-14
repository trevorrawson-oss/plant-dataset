#!/usr/bin/env python3
"""Emit the atomic RGV promote batch from the staging files. Deterministic; writes NO canonical.

Assembles the 108 authored `regions.rgv` cells (6 staging files) + the top-level
region_chill_delivered.rgv band + the region_chill_delivered_provenance replacement into ONE
SHA-guarded apply_patch batch (`tools/batches/rgv_region_promote.json`). Applying it (Task 10)
adds rgv everywhere at once; the companion `rgv` entry in zone_span_gate.EXPECTED_SPANS is a CODE
edit made in the same promote commit (NOT part of this JSON batch), so gate_all is green before
(no rgv anywhere) and after (rgv everywhere + EXPECTED_SPANS), never mid-flip.

Op shape (verified against tools/batches/zonespan_widen.json + apply_patch.py grammar):
  {"op":"add", "json_path":"$.crops[?(@.slug=='<slug>')].regions.rgv", "value": <cell>}   x108
  {"op":"add", "json_path":"$.region_chill_delivered.rgv", "value": <band>}
  {"op":"replace", "json_path":"$.region_chill_delivered_provenance", "from":<old>, "value":<new>}
"""
import glob
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANON = os.path.join(ROOT, "crops_data_final.json")
STAGING = os.path.join(HERE, "staging")
CELL_FILES = ["rgv_annuals_cool.json", "rgv_annuals_warm.json", "rgv_annuals_flowers.json",
              "rgv_citrus.json", "rgv_trees.json", "rgv_perennials.json"]
BAND_FILE = "rgv_chill_band.json"
OUT = os.path.join(HERE, "batches", "rgv_region_promote.json")
EXPECTED_CELL_COUNT = 108


def build():
    raw = open(CANON, "rb").read()
    base_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    canon_slugs = {c["slug"] for c in data["crops"]}
    have_rgv = {c["slug"] for c in data["crops"] if "rgv" in (c.get("regions") or {})}
    assert not have_rgv, f"canonical already has rgv cells: {sorted(have_rgv)}"

    patches, seen = [], set()
    for fn in CELL_FILES:
        cells = json.load(open(os.path.join(STAGING, fn), encoding="utf-8"))
        for slug, cell in cells.items():
            assert slug not in seen, f"duplicate slug across staging files: {slug}"
            assert slug in canon_slugs, f"staged slug not in canonical: {slug}"
            seen.add(slug)
            patches.append({"op": "add",
                            "json_path": f"$.crops[?(@.slug=='{slug}')].regions.rgv",
                            "value": cell})
    assert len(seen) == EXPECTED_CELL_COUNT, f"expected {EXPECTED_CELL_COUNT} cells, got {len(seen)}"

    band = json.load(open(os.path.join(STAGING, BAND_FILE), encoding="utf-8"))
    # band file keys are dotted json paths: "region_chill_delivered.rgv" (add a subkey) and
    # "region_chill_delivered_provenance" (replace the whole top-level string).
    assert "region_chill_delivered.rgv" in band and "region_chill_delivered_provenance" in band, \
        "chill band staging file missing expected keys"
    patches.append({"op": "add", "json_path": "$.region_chill_delivered.rgv",
                    "value": band["region_chill_delivered.rgv"]})
    patches.append({"op": "replace", "json_path": "$.region_chill_delivered_provenance",
                    "from": data["region_chill_delivered_provenance"],
                    "value": band["region_chill_delivered_provenance"]})

    batch = {"base_sha": base_sha, "patches": patches}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=1)
    print(f"emitted {len(patches)} patches ({len(seen)} rgv cells + 2 top-level) -> {OUT}")
    print(f"base_sha {base_sha}")
    return batch


if __name__ == "__main__":
    build()
