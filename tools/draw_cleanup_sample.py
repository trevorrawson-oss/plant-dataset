#!/usr/bin/env python3
"""Draw the deterministic, stratified tier-C sample for the cleanup arc's step 0.

DETERMINISTIC AND REPRODUCIBLE ON PURPOSE: no randomness, so anyone can regenerate the exact
same 20 rows and audit that they were not cherry-picked. Stratified across the source ids
carrying the most SOLE citations, and stride-sampled within each id so the picks spread
across crops/regions rather than clustering at one end of a sorted list.
"""
import json
import sys

sys.path.insert(0, '/Users/trevorrawson/plant-dataset/tools')
from bare_host_scan import scan

D = json.load(open('/Users/trevorrawson/plant-dataset/crops_data_final.json', encoding='utf-8'))
rows = [r for r in scan(D) if r[3]]  # SOLE only

def get(crop, path):
    """Resolve a dotted/indexed path to its node."""
    node = crop
    for part in path.split('.'):
        while '[' in part:
            name, _, rest = part.partition('[')
            idx, _, part = rest.partition(']')
            if name:
                node = node[name]
            node = node[int(idx)]
            if part.startswith('.'):
                part = part[1:]
            if not part:
                break
        else:
            node = node[part]
    return node



crops_tmp = {c['slug']: c for c in D['crops']}


def concrete(slug, path):
    """True if the node states a CONCRETE consumer-facing window (a string plant_out/harvest),
    rather than a frost-offset structure or a bloom sub-block. Declared restriction: this pass
    measures whether the STATED WINDOWS are wrong, which is what a grower actually reads."""
    try:
        node = get(crops_tmp[slug], path)
    except Exception:
        return False
    return isinstance(node, dict) and any(
        isinstance(node.get(f), str) for f in ('plant_out', 'harvest'))


by_id = {}
for sid, slug, path, _sole, _url in rows:
    if concrete(slug, path):
        by_id.setdefault(sid, []).append((slug, path))
for sid in by_id:
    by_id[sid].sort()

# strata: the six ids carrying the most SOLE rows, 3 each; then 2 from the next two ids.
order = sorted(by_id, key=lambda s: (-len(by_id[s]), s))
plan = [(sid, 3) for sid in order[:6]] + [(sid, 1) for sid in order[6:8]]


def stride(items, k):
    n = len(items)
    if n <= k:
        return items
    return [items[round(i * n / k)] for i in range(k)]


crops = {c['slug']: c for c in D['crops']}
sample = []
for sid, k in plan:
    for slug, path in stride(by_id[sid], k):
        node = get(crops[slug], path)
        claim = {f: node.get(f) for f in
                 ('plant_out', 'harvest', 'suitability', 'months', 'start', 'end')
                 if isinstance(node, dict) and node.get(f)}
        sample.append((sid, slug, path, claim))

print(f'| # | source id | crop | node | the claim to check |')
print(f'|---|---|---|---|---|')
for i, (sid, slug, path, claim) in enumerate(sample, 1):
    short = path.replace('regions.', '').replace('resolved_by_zone.', 'z')
    bits = '; '.join(f'`{k}` {v!r}' for k, v in claim.items()) or '(see node)'
    if len(bits) > 90:
        bits = bits[:88] + '…'
    print(f'| {i} | `{sid}` | {slug} | `{short}` | {bits} |')
print()
print(f'total sampled: {len(sample)} across {len({s for _, s, _, _ in sample})} crops, '
      f'{len({p.split(".")[1] for _, _, p, _ in sample})} regions, {len(plan)} source ids')
