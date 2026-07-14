#!/usr/bin/env python3
"""zone_span_gate (A45) -- region zone_span parity, the first guard on zone_span.

WHY: the 2023 USDA map relabeled the marquee cities the regions were authored for
(Phoenix 9b->10a, Honolulu ->z12), and nothing in tools/ read zone_span at all, so
the spans silently went stale and 300+ real ZIPs fell out of region resolution in
the app (docs/2026-07-12-region-zonespan-gaps.md). This gate pins every populated
region cell to ONE canonical, str-typed span and requires resolved_by_zone key
parity, so a span can never drift from its rows (or from crop to crop) again.
Widening a span is a deliberate act: update EXPECTED_SPANS + clone rows, together.

Spec: docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md

check_crop(crop) -> list of violation strings (empty = pass). Wired into
whole_crop_gate as A45 at the widen promote (this gate is RED on pre-widen data
by design -- that is the TDD proof, not a bug).

Standalone roster-wide run: python3 tools/zone_span_gate.py [crops_data_final.json]
"""
import json
import sys

# Canonical spans, str-typed, ascending. 2023-map widened values
# (spec section 4): se_gulf +10, ca_south_coast/ca_desert +11,
# low_desert_az +10, hawaii_tropical +10/+12/+13.
EXPECTED_SPANS = {
    "northern_tier":   ["3", "4", "5", "6", "7"],
    "warm_arid":       ["8"],
    "ca_interior":     ["8", "9"],
    "se_gulf":         ["8", "9", "10"],
    "rgv":             ["9", "10"],
    "ca_north_coast":  ["9", "10"],
    "ca_south_coast":  ["9", "10", "11"],
    "ca_desert":       ["9", "10", "11"],
    "low_desert_az":   ["9", "10"],
    "fl_peninsula":    ["10", "11"],
    "hawaii_tropical": ["10", "11", "12", "13"],
}

# New zone -> donor zone per widened region; consumed by the widen builder and
# by test fixtures. Kept here so gate + builder can never disagree.
DONORS = {
    "low_desert_az":   {"10": "9"},
    "hawaii_tropical": {"10": "11", "12": "11", "13": "11"},
    "ca_south_coast":  {"11": "10"},
    "ca_desert":       {"11": "10"},
    "se_gulf":         {"10": "9"},
}


def check_crop(crop):
    """A45: expected span + span<->resolved_by_zone parity + donor integrity.

    Enforced on CERTIFIED crops only (the same certified-only model gate_all uses):
    uncertified shells legitimately carry narrow / unfilled spans until they are
    authored + certified, at which point the full EXPECTED_SPANS is required. The
    widen builder skips shells for the same reason (cloning their empty cells would
    trip A32), so exempting them here keeps gate and builder in agreement."""
    if (crop.get("verification_status") or {}).get("status") != "verified_gs_arc":
        return []
    out = []
    slug = crop.get("slug", "?")
    for rid, cell in (crop.get("regions") or {}).items():
        if not isinstance(cell, dict):
            out.append(f"{slug}.{rid}: region cell is not an object")
            continue
        rbz = cell.get("resolved_by_zone") or {}
        if not rbz:
            continue  # unpopulated shell: nothing to pin yet
        expected = EXPECTED_SPANS.get(rid)
        if expected is None:
            out.append(f"{slug}.{rid}: unknown region id (add to EXPECTED_SPANS deliberately)")
            continue
        span = cell.get("zone_span")
        if span != expected:
            out.append(f"{slug}.{rid}: zone_span {span!r} != expected {expected!r} "
                       f"(str-typed, ascending)")
        keys = set(rbz.keys())
        if keys != set(expected):
            missing = sorted(set(expected) - keys)
            orphan = sorted(keys - set(expected))
            out.append(f"{slug}.{rid}: resolved_by_zone keys {sorted(keys)} != span "
                       f"(missing {missing}, orphan {orphan})")
        for zone, row in rbz.items():
            if not isinstance(row, dict):
                continue
            donor = row.get("lifted_from_zone")
            if donor is not None and str(donor) not in rbz:
                out.append(f"{slug}.{rid}.{zone}: lifted_from_zone {donor!r} "
                           f"names no resolved row")
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for crop in data["crops"]:
        for v in check_crop(crop):
            print(f"VIOLATION: {v}")
            total += 1
    print(f"zone_span_gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
