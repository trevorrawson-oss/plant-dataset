#!/usr/bin/env python3
"""Empty the fabricated all-`growing` calendars on `unsuitable` cells.

Hardening item 4 (docs/2026-07-26-post-asparagus-hardening-kickoff.md).

THE DEFECT: 11 cells rated `unsuitable` each carried a 12-token all-`growing` calendar,
i.e. active year-round growth for a crop the same cell's own note says cannot grow there
(artichoke ca_desert z11's note: "effectively vacant rather than a real growing
situation"). Worse than showing nothing. It is the gate-avoidance pattern INVERTED: not
a field deleted to dodge a gate, but a field INVENTED to satisfy one -- the A32 /
herbaceous_perennial calendar floor, whose wording ("still show the honest cycle")
assumed a cycle exists to show.

SEQUENCED CORRECTLY (Trevor's ruling 2026-07-26: frontend first). Both consumers already
refuse to render these cells, VERIFIED not assumed:
  plant-astro  src/lib/regions.ts growableZonesByRegion and src/lib/built-crops.ts
               zonesForCrop both `continue` on suitability === 'unsuitable'
  plant-app    src/lib/suitability.ts maps unsuitable -> 'blocked';
               src/lib/guide-perennial-calendar.ts returns {supported:false}. Its header
               names these very calendars "the motivating defect" and says the app
               "keeps working if those calendars are ever cleaned up upstream".
So emptying them cannot trade a misleading calendar for a blank card.

SCOPE NOTE, deliberately loud: the kickoff doc scoped this to asparagus's 10 cells,
written before artichoke certified. artichoke ca_desert z11 carries the IDENTICAL defect
and is included here, so the class is closed rather than left 10/11 done. That eleventh
cell is called out in the session summary for explicit sign-off.

Guards, all fatal:
  - canonical SHA must match EXPECT_SHA
  - exactly EXPECT_N cells qualify (suitability == 'unsuitable' on a calendar-presence base)
  - every one must currently hold a 12-token all-`growing` calendar (the fabrication
    signature) -- a cell with a DIFFERENT calendar is not this defect and aborts the run
  - every one must carry suitability_note_seasoned (we remove the fake cycle, never the reason)
  - nothing but those `calendar` lists may change

Writes COMPACT per CLAUDE.md: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_empty_unsuitable_calendars.py --dry-run
    $ python3 tools/promote_empty_unsuitable_calendars.py
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
sys.path.insert(0, os.path.join(REPO, 'tools'))
from coverage_floor_gate import CALENDAR_PRESENCE_BASES  # noqa: E402

EXPECT_SHA = 'dc545be63ba24d0e6c3c4cdd2c05da54f66f3708701a4d73efb1e7c4fca3f391'
EXPECT_N = 11
EXPECT_CELLS = {
    ('asparagus', 'se_gulf', '10'), ('asparagus', 'ca_desert', '11'),
    ('asparagus', 'rgv', '9'), ('asparagus', 'rgv', '10'),
    ('asparagus', 'fl_peninsula', '10'), ('asparagus', 'fl_peninsula', '11'),
    ('asparagus', 'hawaii_tropical', '10'), ('asparagus', 'hawaii_tropical', '11'),
    ('asparagus', 'hawaii_tropical', '12'), ('asparagus', 'hawaii_tropical', '13'),
    ('artichoke', 'ca_desert', '11'),
}
FABRICATION_SIGNATURE = ['growing'] * 12


def die(msg):
    print(f'ABORT: {msg}', file=sys.stderr)
    sys.exit(1)


def qualifying(data):
    out = []
    for crop in data['crops']:
        if crop.get('calendar_basis') not in CALENDAR_PRESENCE_BASES:
            continue
        for rk, region in (crop.get('regions') or {}).items():
            for z, cell in ((region or {}).get('resolved_by_zone') or {}).items():
                if isinstance(cell, dict) and cell.get('suitability') == 'unsuitable':
                    out.append((crop['slug'], rk, z, cell))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    raw = open(CANONICAL, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        die(f'canonical SHA drift.\n  expected {EXPECT_SHA}\n  found    {sha}')
    print(f'canonical SHA verified: {sha[:8]}')

    data = json.loads(raw.decode('utf-8'))
    before = copy.deepcopy(data)

    cells = qualifying(data)
    found = {(s, rk, z) for s, rk, z, _ in cells}
    if len(cells) != EXPECT_N:
        die(f'expected {EXPECT_N} qualifying cells, found {len(cells)}: {sorted(found)}')
    if found != EXPECT_CELLS:
        die(f'cell set drift.\n  unexpected: {sorted(found - EXPECT_CELLS)}\n'
            f'  missing:    {sorted(EXPECT_CELLS - found)}')
    print(f'cell set verified: {EXPECT_N} cells across '
          f'{len({s for s, _, _ in found})} crops')

    for slug, rk, z, cell in cells:
        cal = cell.get('calendar') or []
        if cal != FABRICATION_SIGNATURE:
            die(f'{slug}.{rk}.{z} calendar is not the 12-token all-growing fabrication '
                f'signature (got {len(cal)} tokens, {sorted(set(cal))}); this cell is not '
                f'this defect -- adjudicate it by hand')
        if not cell.get('suitability_note_seasoned'):
            die(f'{slug}.{rk}.{z} has no suitability_note_seasoned; refusing to remove the '
                f'calendar and leave a bare downgrade')
    print('all 11 verified: 12-token all-growing calendar + a seasoned reason present')

    for slug, rk, z, cell in cells:
        cell['calendar'] = []
    print('emptied 11 calendars')

    # Footprint proof: ONLY those calendar lists may differ.
    changed = []
    b = {c['slug']: c for c in before['crops']}
    n = {c['slug']: c for c in data['crops']}
    for slug in b:
        if b[slug] == n[slug]:
            continue
        for rk, region in (n[slug].get('regions') or {}).items():
            for z, cell in ((region or {}).get('resolved_by_zone') or {}).items():
                bcell = ((b[slug].get('regions') or {}).get(rk, {})
                         .get('resolved_by_zone', {}).get(z))
                if isinstance(cell, dict) and cell != bcell:
                    diff_keys = {k for k in set(cell) | set(bcell or {})
                                 if cell.get(k) != (bcell or {}).get(k)}
                    if diff_keys != {'calendar'}:
                        die(f'{slug}.{rk}.{z} changed keys {sorted(diff_keys)}, expected '
                            f'only calendar')
                    changed.append((slug, rk, z))
    if sorted(changed) != sorted(found):
        die(f'footprint mismatch: changed {sorted(changed)} vs intended {sorted(found)}')
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            die(f'top-level key {k!r} changed')
    print(f'footprint proven EXACT: {len(changed)} cells, `calendar` only')

    out = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if out.endswith('\n'):
        die('refusing to write a trailing newline')

    if args.dry_run:
        print(f'\nDRY RUN, nothing written. Would become: '
              f'{hashlib.sha256(out.encode("utf-8")).hexdigest()}')
        return 0

    with open(CANONICAL, 'w', encoding='utf-8') as fh:
        fh.write(out)
    new_sha = hashlib.sha256(open(CANONICAL, 'rb').read()).hexdigest()
    print(f'\nwritten. canonical {EXPECT_SHA[:8]} -> {new_sha[:8]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
