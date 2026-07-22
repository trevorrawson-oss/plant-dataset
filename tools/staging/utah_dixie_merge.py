#!/usr/bin/env python3
"""Merge utah_dixie authoring shard files into a class staging file, then report cell count +
gate readiness. Controller-only build helper (subagents never commit). Generic (region-agnostic);
cloned from nevada_merge.py.

Usage:
  python3 tools/staging/utah_dixie_merge.py <class_staging_file> <shard1.json> [shard2.json ...]

Merges each shard's {slug: cell} into <class_staging_file> (which may already hold controller
reference cells). Refuses to overwrite an existing slug with a different cell unless --force.
Writes compact JSON. Prints the merged slug list + count.
"""
import json, sys, os

def load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    target, shards = args[0], args[1:]
    data = load(target)
    added, collided = [], []
    for sp in shards:
        s = load(sp)
        for slug, cell in s.items():
            if slug in data and data[slug] != cell and not force:
                collided.append(slug); continue
            if slug not in data:
                added.append(slug)
            data[slug] = cell
    json.dump(data, open(target, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"merged into {target}: {len(data)} cells total; +{len(added)} new: {sorted(added)}")
    if collided:
        print(f"  COLLISION (existing != shard, not overwritten; use --force to replace): {sorted(collided)}")
    print("  all slugs:", sorted(data.keys()))

if __name__ == "__main__":
    main()
