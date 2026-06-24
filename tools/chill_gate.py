#!/usr/bin/env python3
"""Chill-delivered refactor gate (Phase A, audit F2). Two checks:

  chill_delivered_absent_violations(crop)  -- PER-CROP, wired into whole_crop_gate (A18).
    chill_hours_delivered is a CLIMATE datum (how much winter chill a region+zone banks),
    so it must NOT live on a crop. After the refactor the single source of truth is the
    top-level `region_chill_delivered` table; any per-crop chill_hours_delivered (region
    rollup or resolved cell, array OR the old string shape) is a violation. With no per-crop
    overrides + one shared table, "crop-invariant per region+zone" holds by construction.

  chill_table_violations(data)  -- DATASET-LEVEL, run in release_verify.
    `region_chill_delivered` must be a dict region -> {zone -> [lo, hi]} with numeric
    0 <= lo <= hi (normalizes blueberry's old string-typed values).
"""


def chill_delivered_absent_violations(crop):
    """[] = clean. Flags any per-crop chill_hours_delivered (the climate datum belongs in
    the shared region_chill_delivered table, not on the crop)."""
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        if "chill_hours_delivered" in r:
            V.append(f"{rk}: region carries chill_hours_delivered (a climate datum -- it "
                     f"belongs in the shared region_chill_delivered table, not the crop)")
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if isinstance(cell, dict) and "chill_hours_delivered" in cell:
                V.append(f"{rk}.{z}: cell carries chill_hours_delivered (climate datum -- "
                         f"move to the shared region_chill_delivered table)")
    return V


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def chill_table_violations(data):
    """[] = clean. Validates the top-level region_chill_delivered climate table shape."""
    V = []
    table = data.get("region_chill_delivered")
    if not isinstance(table, dict):
        V.append("region_chill_delivered missing or not a dict (the shared chill-delivered "
                 "source of truth must exist)")
        return V
    for rk, zones in table.items():
        if not isinstance(zones, dict):
            V.append(f"region_chill_delivered.{rk}: not a dict of zone -> [lo,hi] "
                     f"(got {type(zones).__name__})")
            continue
        for z, band in zones.items():
            where = f"region_chill_delivered.{rk}.{z}"
            if not (isinstance(band, list) and len(band) == 2):
                V.append(f"{where}: not a 2-element [lo,hi] list (got {band!r})")
                continue
            lo, hi = band
            if not (_is_number(lo) and _is_number(hi)):
                V.append(f"{where}: bounds must be numbers (got {band!r}) -- the string-typed "
                         f"chill value is the F2 bug")
                continue
            if lo < 0:
                V.append(f"{where}: negative lower bound {lo}")
            if lo > hi:
                V.append(f"{where}: lo > hi ({lo} > {hi}) -- bounds out of order")
    return V


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path))
    total = 0
    for v in chill_table_violations(data):
        print(f"  TABLE: {v}"); total += 1
    for c in data["crops"]:
        for v in chill_delivered_absent_violations(c):
            print(f"  {c.get('slug')}: {v}"); total += 1
    print(f"chill gate: {total} violation(s)")
    sys.exit(1 if total else 0)
