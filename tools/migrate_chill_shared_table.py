#!/usr/bin/env python3
"""migrate_chill_shared_table.py -- chill-delivered consolidation (Phase A, audit F2).

Moves the CLIMATE datum chill_hours_delivered off the crops and into ONE shared,
crop-invariant top-level table `region_chill_delivered` (region -> {zone -> [lo,hi]}):
  1. Build the table by consolidating the per-crop per-zone values that peach/apple/
     blueberry carried, per (region, zone), as the UNION [min lo, max hi]. Blueberry's
     string bands ("1200 or more", "under 100", "300 to 500") are parsed to numbers.
  2. Strip chill_hours_delivered from every crop (region rollup + resolved cells).
The per-variety chill-REQUIRED side and the per-crop chill_basis_* prose are untouched.

The seeded numbers are a REALISTIC PLACEHOLDER (union of existing authored bands), NOT
independently sourced -- claude.ai reconciles each cell to one T1-sourced value next.
Idempotent. Canonical write: separators=(",",":"), ensure_ascii=False, no trailing newline.

Run: python3 tools/migrate_chill_shared_table.py [crops_data_final.json]
"""
import json, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
CHILL_CROPS = ("peach", "apple", "blueberry")

PROVENANCE = (
    "PLACEHOLDER (Phase A, 2026-06-24): each [lo,hi] is the union (min lo, max hi) of the "
    "per-crop chill_hours_delivered that peach/apple/blueberry carried at dataset 6e9538e1, "
    "consolidated per region+zone (blueberry string bands parsed). Realistic magnitudes but "
    "NOT independently sourced. claude.ai is reconciling each cell to ONE T1-sourced value "
    "(UC IPM chill maps + regional extension chill data); replace per-cell, never derive from "
    "the USDA zone. The per-variety chill_hours_required (chill NEEDED) is the separate axis."
)


def parse_band(v):
    """Return (lo, hi) from an [lo,hi] list or a blueberry-style string band.
    lo/hi may be None for an open-ended bound ('X or more' has no hi)."""
    if isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) for x in v):
        return float(v[0]), float(v[1])
    if isinstance(v, str):
        s = v.strip().lower()
        nums = [int(n) for n in re.findall(r"\d+", s)]
        if "or more" in s or "or higher" in s:
            return (nums[0] if nums else None), None
        if s.startswith("under") or s.startswith("less than") or s.startswith("below"):
            return 0.0, (float(nums[0]) if nums else None)
        if len(nums) >= 2:
            return float(nums[0]), float(nums[1])
        if len(nums) == 1:
            return float(nums[0]), float(nums[0])
    return None, None


def build_table(crops):
    """region -> {zone -> [lo,hi]} consolidated across the chill crops."""
    los = {}  # (region, zone) -> [lo candidates]
    his = {}
    for c in crops:
        if c.get("slug") not in CHILL_CROPS:
            continue
        for rk, r in (c.get("regions") or {}).items():
            for z, cell in (r.get("resolved_by_zone") or {}).items():
                if not isinstance(cell, dict) or "chill_hours_delivered" not in cell:
                    continue
                lo, hi = parse_band(cell["chill_hours_delivered"])
                if lo is not None:
                    los.setdefault((rk, z), []).append(lo)
                if hi is not None:
                    his.setdefault((rk, z), []).append(hi)
    table = {}
    for (rk, z) in sorted(set(los) | set(his)):
        lo = min(los.get((rk, z), [0]))
        hi = max(his.get((rk, z), los.get((rk, z), [0])))
        table.setdefault(rk, {})[z] = [int(round(lo)), int(round(hi))]
    return table


def strip_per_crop(crops):
    n = 0
    for c in crops:
        for r in (c.get("regions") or {}).values():
            if isinstance(r, dict):
                if r.pop("chill_hours_delivered", None) is not None:
                    n += 1
                for cell in (r.get("resolved_by_zone") or {}).values():
                    if isinstance(cell, dict) and cell.pop("chill_hours_delivered", None) is not None:
                        n += 1
    return n


def insert_after(d, anchor_key, new_pairs):
    out, inserted = {}, False
    for k, v in d.items():
        if k in new_pairs:
            continue
        out[k] = v
        if k == anchor_key:
            out.update(new_pairs); inserted = True
    if not inserted:
        out.update(new_pairs)
    return out


def migrate():
    data = json.load(open(PATH, encoding="utf-8"))
    # Merge any EXISTING table (a prior run / hand-sourced values) under the freshly
    # consolidated per-crop values, so re-running after the strip is a no-op (idempotent)
    # rather than rebuilding to empty. Newly-consolidated cells win where both exist.
    table = {}
    for src in (data.get("region_chill_delivered") or {}, build_table(data["crops"])):
        for rk, zones in src.items():
            for z, band in (zones or {}).items():
                table.setdefault(rk, {})[z] = band
    stripped = strip_per_crop(data["crops"])
    anchor = "region_source_map" if "region_source_map" in data else list(data)[-1]
    data = insert_after(data, anchor, {
        "region_chill_delivered": table,
        "region_chill_delivered_provenance": PROVENANCE,
    })
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))

    cells = sum(len(z) for z in table.values())
    print(f"migrate_chill_shared_table: built region_chill_delivered "
          f"({len(table)} regions, {cells} zone cells); stripped {stripped} per-crop field(s).")
    for rk in sorted(table):
        print(f"  {rk:18} " + "  ".join(f"z{z}={table[rk][z]}" for z in sorted(table[rk], key=int)))


if __name__ == "__main__":
    migrate()
