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

    # region_chill_delivered is a single top-level crop-invariant table (region -> {zone -> [lo,hi]}),
    # ALSO displayed in-app (TreeGuide "your area banks ~X chill hours"). It carries the same zone
    # gaps as the region calendars, for the same reason. Clone the donor zone's band to each new
    # zone so A3 (perennial no-fruit split) has a band AND the display stays consistent with the
    # cloned calendar. Same-city relabels (low_desert_az, hawaii_tropical) inherit the exact band
    # (honest -- same physical city); the 3 warm-edge gaps (se_gulf, ca_south_coast, ca_desert)
    # inherit a slightly generous band, tracked on the region-coverage roadmap (Trevor-approved
    # 2026-07-12). Value stays a clean [lo,hi] -- the app parses it as number[].
    chill = data.get("region_chill_delivered") or {}
    for rid, mapping in sorted(DONORS.items()):
        rzones = chill.get(rid) or {}
        for new, donor in sorted(mapping.items()):
            if new in rzones or donor not in rzones:
                continue
            ops.append({"op": "add",
                        "json_path": f"$.region_chill_delivered.{rid}.{new}",
                        "value": list(rzones[donor])})
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
    row_clones = sum(1 for o in ops if o["op"] == "add"
                      and o["json_path"].startswith("$.crops"))
    chill_clones = sum(1 for o in ops if o["op"] == "add"
                        and o["json_path"].startswith("$.region_chill_delivered"))
    spans = sum(1 for o in ops if o["op"] == "replace")
    # crop count: only crop-scoped ops carry a quoted slug in json_path (chill ops are
    # top-level table paths with no slug -- bug fix, was a crash via bare split(chr(39))[1]
    # on those paths; the ops themselves were already correct, only this summary line broke).
    crop_paths = {o["json_path"].split(chr(39))[1] for o in ops if chr(39) in o["json_path"]}
    print(f"wrote {OUT}: {row_clones} cloned zone rows + {chill_clones} cloned chill bands "
          f"({row_clones + chill_clones} adds) + {spans} zone_span normalizations "
          f"across {len(crop_paths)} crops")


if __name__ == "__main__":
    main()
