#!/usr/bin/env python3
"""Offline non-null-URL gate (post-114 §B, offline half). Every anchoring_urls entry in the LIVE
layers (regions{} + claim/top-level) must carry a non-null, non-empty url. The legacy zones{} layer
is EXCLUDED (matches whole_crop_gate gate F scoping). OFFLINE ONLY -- never hits the network; URL
liveness (404/redirect/logo-PDF) is a separate --online sweep, deferred.

Usage: python3 tools/url_health_gate.py [crops_data_final.json]
Exit 1 on any live-layer null/empty url; else 0.
"""


def url_health_violations(crop):
    """Return list of '<slug>: <path>: null/empty url' ([] = clean). Legacy zones{} layer skipped."""
    V = []
    slug = crop.get("slug", "?")

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if (k.endswith("anchoring_urls") and isinstance(v, dict)
                        and not p.startswith("zones")):  # legacy zones{} EXCLUDED
                    for src, rec in v.items():
                        if isinstance(rec, dict) and not rec.get("url"):
                            V.append(f"{slug}: {p}.{src}: null/empty url")
                walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]")

    walk(crop, "")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in url_health_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    print(f"url_health (offline, live layers): {total} null/empty url(s)")
    sys.exit(1 if total else 0)
