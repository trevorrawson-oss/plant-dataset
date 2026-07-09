#!/usr/bin/env python3
"""verify_demux_footprint.py -- the byte-diff footprint audit for de-mux applies
(spec §9). Independent of apply_patch's own report: reads ONLY the two files.
Exit 1 on any out-of-footprint drift."""
import argparse
import json
import sys

POPULATE_KEYS = {"second_planting", "start_indoors", "plant_out"}
CLEAN_KEYS = {"start_indoors", "plant_out", "harvest",
              "harvest_start", "harvest_end", "first_plant_date", "last_plant_date"}


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--base", required=True)
    ap.add_argument("--slugs", required=True)
    ap.add_argument("--stage", required=True, choices=["populate", "clean"])
    a = ap.parse_args()
    allowed_slugs = set(a.slugs.split(","))
    allowed_keys = POPULATE_KEYS if a.stage == "populate" else CLEAN_KEYS
    raw = open(a.candidate, "rb").read()
    problems = []
    if raw.endswith(b"\n"):
        problems.append("candidate has a trailing newline (must be COMPACT)")
    cand = json.loads(raw.decode("utf-8"))
    base = json.load(open(a.base, encoding="utf-8"))
    cc = cand["crops"] if isinstance(cand, dict) and "crops" in cand else cand
    bc = base["crops"] if isinstance(base, dict) and "crops" in base else base
    if len(cc) != 124 or len(bc) != 124:
        problems.append(f"crop count: base={len(bc)} candidate={len(cc)} (want 124)")
    by_slug_c = {c.get("slug"): c for c in cc}
    for b in bc:
        slug = b.get("slug")
        c = by_slug_c.get(slug)
        if c is None:
            problems.append(f"crop missing from candidate: {slug}")
            continue
        if compact(b) == compact(c):
            if slug in allowed_slugs:
                problems.append(f"batch crop unchanged (op missed?): {slug}")
            continue
        if slug not in allowed_slugs:
            problems.append(f"OUT-OF-FOOTPRINT crop changed: {slug}")
            continue
        # inside a batch crop: only resolved cells, only allowed keys
        for key in set(b) | set(c):
            if key == "regions":
                continue
            if compact(b.get(key)) != compact(c.get(key)):
                problems.append(f"{slug}: top-level key changed: {key}")
        bregs = b.get("regions") or {}
        cregs = c.get("regions") or {}
        for rk in set(bregs) | set(cregs):
            br, cr = bregs.get(rk) or {}, cregs.get(rk) or {}
            for key in set(br) | set(cr):
                if key == "resolved_by_zone":
                    continue
                if compact(br.get(key)) != compact(cr.get(key)):
                    problems.append(f"{slug}.{rk}: region key changed: {key}")
            for z in set(br.get("resolved_by_zone", {}) or {}) | set(cr.get("resolved_by_zone", {}) or {}):
                bz = (br.get("resolved_by_zone") or {}).get(z, {})
                cz = (cr.get("resolved_by_zone") or {}).get(z, {})
                for key in set(bz) | set(cz):
                    if compact(bz.get(key)) != compact(cz.get(key)) and key not in allowed_keys:
                        problems.append(f"{slug}.{rk}.{z}: cell key changed: {key}")
    for p in problems:
        print("FOOTPRINT:", p)
    print(f"verify_demux_footprint: {len(problems)} problems "
          f"({a.stage}, {len(allowed_slugs)} slugs)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
