#!/usr/bin/env python3
"""Promote the staged asparagus reference into the canonical crops_data_final.json (crop #120).

A pure crop replacement: the staged reference (tools/staging/asparagus_reference.json) cites only
source_catalog + control_methods ids that already exist in the canonical (verified before running),
so NO catalog additions are needed -- the only change is the `asparagus` crop dict, shell -> certified.

Writes COMPACT per CLAUDE.md: separators=(",",":"), ensure_ascii=False, NO trailing newline, never
indent. A json round-trip with these separators leaves every UNCHANGED crop byte-identical (Python
preserves dict insertion order), so the diff is asparagus-only.

Usage: python3 tools/promote_asparagus.py
"""
import json
import sys

CANON = "crops_data_final.json"
STAGED = "tools/staging/asparagus_reference.json"


def main():
    data = json.load(open(CANON, encoding="utf-8"))
    ref = json.load(open(STAGED, encoding="utf-8"))["crop"]

    # Guard: the staged crop must not introduce an uncatalogued source or control-method id.
    src_cat = set(data.get("source_catalog", {}))
    cm_cat = set(data.get("control_methods", {}))
    used_src, used_methods = set(), set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("sources", "source_set") and isinstance(v, list):
                    used_src.update(v)
                if k == "anchoring_urls" and isinstance(v, dict):
                    used_src.update(v)
                if k == "method" and isinstance(v, str):
                    used_methods.add(v)
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(ref)
    new_src = sorted(used_src - src_cat)
    new_methods = sorted(used_methods - cm_cat)
    if new_src or new_methods:
        print(f"ABORT: staged crop needs uncatalogued ids -- sources {new_src}, methods {new_methods}")
        sys.exit(1)

    # Splice: replace the asparagus crop dict in place (preserve roster order).
    for i, c in enumerate(data["crops"]):
        if c.get("slug") == "asparagus":
            data["crops"][i] = ref
            break
    else:
        print("ABORT: no asparagus crop found in canonical")
        sys.exit(1)

    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    # No trailing newline (json.dump writes none; do not add one).

    cert = sum(1 for c in data["crops"]
               if (c.get("verification_status") or {}).get("status") == "verified_gs_arc")
    print(f"promoted asparagus -> certified. catalog additions: none. "
          f"certified={cert} total={len(data['crops'])}")


if __name__ == "__main__":
    main()
