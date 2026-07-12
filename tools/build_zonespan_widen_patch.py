#!/usr/bin/env python3
"""Emit the SHA-guarded apply_patch batch for the region zone-span widen
(spec docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md).

The 2023 USDA map relabeled the cities the warm regions were authored FOR
(Phoenix 9b->10a, Honolulu ->z12, warm CA coast ->z11, New Orleans fringe ->z10),
so the fix is label reconciliation, not re-authoring: clone the donor zone's
resolved row to the new zone label (marked with the established lifted_from_zone
idiom -- the row IS that city's data) and normalize every populated zone_span to
the canonical str-typed value from zone_span_gate.EXPECTED_SPANS.

Footprint: zone_span (normalize) + new resolved_by_zone keys in the 5 widened
regions, across every crop with populated region rows. Nothing else moves.

Run: python3 tools/build_zonespan_widen_patch.py
Then: python3 tools/apply_patch.py tools/batches/zonespan_widen.json
"""
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zone_span_gate import EXPECTED_SPANS, DONORS

CANON = "crops_data_final.json"
OUT = "tools/batches/zonespan_widen.json"


def build_widen_ops(data):
    """Pure op builder: list of apply_patch ops taking `data` to the widened,
    normalized shape. Idempotent: widened input -> []."""
    ops = []
    for crop in data.get("crops", []):
        slug = crop.get("slug")
        for rid, cell in (crop.get("regions") or {}).items():
            rbz = cell.get("resolved_by_zone") or {}
            if not rbz or rid not in EXPECTED_SPANS:
                continue
            base = f"$.crops[?(@.slug=='{slug}')].regions.{rid}"
            for new, donor in sorted((DONORS.get(rid) or {}).items()):
                if new in rbz or donor not in rbz:
                    continue
                row = copy.deepcopy(rbz[donor])
                row["lifted_from_zone"] = donor
                ops.append({"op": "add",
                            "json_path": f"{base}.resolved_by_zone.{new}",
                            "value": row})
            expected = EXPECTED_SPANS[rid]
            if cell.get("zone_span") != expected:
                ops.append({"op": "replace", "json_path": f"{base}.zone_span",
                            "from": cell.get("zone_span"),
                            "value": list(expected)})
    return ops


def main():
    raw = open(CANON, "rb").read()
    data = json.loads(raw.decode("utf-8"))
    ops = build_widen_ops(data)
    if not ops:
        print("no-op: canonical is already widened + normalized")
        return
    patch = {"base_sha": hashlib.sha256(raw).hexdigest(), "patches": ops}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(patch, f, separators=(",", ":"), ensure_ascii=False)
    clones = sum(1 for o in ops if o["op"] == "add")
    spans = sum(1 for o in ops if o["op"] == "replace")
    print(f"wrote {OUT}: {clones} cloned zone rows + {spans} zone_span "
          f"normalizations across {len({o['json_path'].split(chr(39))[1] for o in ops})} crops")


if __name__ == "__main__":
    main()
