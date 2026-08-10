#!/usr/bin/env python3
"""PLA-202: the verbatim rewrite pass -- 25 HARD hits repaired across 22 fields, 15 crops.
Base c16071bc.

Every one of the 121 certified crops' 333 verbatim HARD hits was read and adjudicated
2026-08-10 (docs/2026-08-10-pla202-verbatim-adjudication.md, per-hit ledger
docs/pla202_verbatim_adjudication_c16071bc.json). 308 ruled benign by reading; the 25
rewrite-class hits (R1 attributed near-quote, R2 unattributed lift) are repaired here
with fresh prose authored in the claude.ai lane (2026-08-10 delivery, staged verbatim in
tools/staging/pla202_rewrites.json via pla202_rewrites_build.py). Attribution retained,
content restated; two paraphrase catches rebuilt with new sentence structure. Two
authored deviations beyond the 25, both flagged in the delivery and applied as authored:
raspberry "cultivars"->"varieties" (common-tongue convention) and strawberry's UC
boilerplate-shaped planting-window sentence folded into the transplant sentence.

The transform is REPLACEMENT-ONLY: 22 enumerated string fields move, nothing else --
no sources, findings, cert logs, calendars, or catalog entries. The guard suite
(test_promote_pla202_rewrites.py) proves the blast radius.

Usage: python3 tools/promote_pla202_rewrites.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
STAGED = os.path.join(REPO, 'tools', 'staging', 'pla202_rewrites.json')
BASE_SHA = 'c16071bc34e3f41e0224264adc7d372061ce1b8de9fd2ab61ca5d232b63e4e3b'

PATH_TOKEN = re.compile(r'([^.\[\]]+)|\[(\d+)\]')


def _walk(crop, path):
    """(parent, leaf_key) for a scan-printed path like a.b[2].c."""
    toks = [(m.group(1), m.group(2)) for m in PATH_TOKEN.finditer(path)]
    node = crop
    for key, idx in toks[:-1]:
        node = node[key] if key is not None else node[int(idx)]
    key, idx = toks[-1]
    return node, (key if key is not None else int(idx))


def _pin(cond, msg):
    if not cond:
        print(f'ABORT (pre-state pin failed): {msg}', file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    args = ap.parse_args()

    raw = open(args.canonical, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    _pin(got == BASE_SHA, f'canonical is {got[:8]}, transform written against {BASE_SHA[:8]}')
    data = json.loads(raw)
    rewrites = json.load(open(STAGED))
    n_fields = sum(len(v) for v in rewrites.values())
    _pin(len(rewrites) == 15 and n_fields == 22,
         f'staged table is {len(rewrites)} crops / {n_fields} fields, expected 15 / 22')

    crops = {c['slug']: c for c in data['crops']}

    # -- pre-state pins beyond the SHA (structure the work-order relied on) -----------------
    cz = [crops['cabbage']['regions']['hawaii_tropical']['resolved_by_zone'][z]['zone_notes']
          for z in ('10', '11', '12', '13')]
    _pin(len(set(cz)) == 1, 'cabbage zone_notes are not identical across the four zones')
    z7 = crops['cherry-sour']['regions']['mid_atlantic']['resolved_by_zone']['7'][
        'suitability_note_seasoned']
    z8 = crops['cherry-sour']['regions']['mid_atlantic']['resolved_by_zone']['8'][
        'suitability_note_seasoned']
    _pin(z7.replace('1100 to 1500', '1000 to 1350').replace('zone 7', 'zone 8') == z8,
         'cherry-sour z7/z8 differ by more than the chill clause -- work-order premise false')

    # -- apply: replacement-only ------------------------------------------------------------
    for slug, fields in sorted(rewrites.items()):
        _pin(slug in crops, f'{slug}: not in canonical')
        for path, new in sorted(fields.items()):
            parent, leaf = _walk(crops[slug], path)
            old = parent[leaf]
            _pin(isinstance(old, str), f'{slug}:{path} is not a string')
            _pin(old != new, f'{slug}:{path} already carries the replacement')
            parent[leaf] = new

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN ok: {BASE_SHA[:8]} -> {new_sha[:8]} ({len(out)} bytes, not written)')
        return
    with open(args.canonical, 'wb') as f:
        f.write(out)
    print(f'PROMOTED: {BASE_SHA[:8]} -> {new_sha[:8]}')


if __name__ == '__main__':
    main()
