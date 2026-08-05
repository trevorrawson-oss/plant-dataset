#!/usr/bin/env python3
"""GUARDED PROMOTE: USCRN soil-temperature validation (PLA-110).

    $ python3 tools/promote_uscrn_validation.py --dry-run
    $ python3 tools/promote_uscrn_validation.py --apply

TWO WRITES, AND NOTHING ELSE MOVES. Not a date, not a calendar, not a citation, not a line of
prose; guards prove each separately.

  1. A new top-level `uscrn_soil_temp`, sibling of `zone_frost_data`: the measured distribution of
     the date 5cm soil temperature first holds each threshold for 5 consecutive days, per USDA
     zone, over 2010-2025, from all 113 NOAA USCRN stations. This is MEASUREMENT, not a borrowed
     extension table, and it is the part of this pass that does not depend on the threshold
     question below. `source_catalog.uscrn` already exists at T1 and its own note pins validation
     to the 5cm depth, so this lands under a citation the file already carries.

  2. `uscrn_validation` records on the `direct_sow` arm of `plantings[0]` for every comparable
     cell. Records are keyed to the CELL, not to an arm index: arms align positionally with
     resolved window segments only 51% of the time on this roster.

THE THRESHOLD BASIS, RULED BY TREVOR 2026-08-04. Ship on `germination_temp_f[0]`, the crop's
certified OPTIMAL germination floor, with `anchor_threshold_basis` naming that provenance on every
single record. This is explicitly NOT the finish line: `germination_temp_f` is an optimal band and
not a germination minimum (contract doc says so; cucumber reads 70F against a true minimum near
60F), so the real germination-minimum field is filed separately as PLA-118, and NO app-facing
USCRN-validation claim rests on this pass. A guard asserts the provenance string is present and
correct on every record precisely so that ruling cannot quietly erode.

THE 9 PILOT RECORDS ARE OVERWRITTEN, deliberately. They are not reproducible from the archive by
any method tried, and one of them is wrong: bok-choy / northern_tier is byte-identical to
lettuce-leaf / northern_tier -- same stored_date 03-18, same 14 stations, same 198 station-years --
for a crop that stores no Mar 18 date in ANY zone (its z6 is Mar 22, its z7 Mar 1). G4b and G4c
pin that closed.

NARROWER THAN FIRST WRITTEN, after re-reading the data: the 40F anchor on bok-choy is NOT part of
that defect. It is declared on bok-choy's own arm and sourced to bok-choy's own MSU Extension
prose ("bok choy ... germinates once soil reaches about 40 degrees F"), so it legitimately
overrides the 45F optimal-band floor, and a guard demanding 45F there was asserting an inference
rather than the evidence. What was copied was the record PAYLOAD -- the date and the station
counts -- not the threshold.

Evidence: docs/2026-08-04-uscrn-soil-temp-validation-arc.md.
"""
import argparse
import collections
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uscrn_validate as UV  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
ZONE_TABLE = os.path.join(REPO, 'tools', 'staging', 'uscrn', 'zone_table.json')

BASE_SHA = '4065e23bf7cbfd2945c476c93e7326e9a6d2f0646ac88bac9a66f7b9d857023e'
SESSION = '2026-08-04 USCRN SOIL-TEMP VALIDATION (PLA-110)'
PROVENANCE = 'germination_temp_f floor for this crop'
DECLARED_PREFIX = 'declared on the planting arm as '

# The pilot record this pass is known to be replacing because it is WRONG, not merely stale.
PILOT_DEFECT = ('bok-choy', 'northern_tier')


def slots(crops):
    """Yield (path_tuple, holder_dict) for every uscrn_validation slot in the file."""
    for ci, crop in enumerate(crops):
        for kind in ('zones', 'regions'):
            for cid, node in sorted((crop.get(kind) or {}).items()):
                for pi, planting in enumerate(node.get('plantings') or []):
                    for key in ('direct_sow', 'plant_out', 'transplant',
                                'start_indoors', 'harvest_start', 'harvest_end'):
                        for ai, arm in enumerate(planting.get(key) or []):
                            if isinstance(arm, dict) and 'uscrn_validation' in arm:
                                yield (ci, kind, cid, pi, key, ai), arm


def strip_uscrn(data):
    """A deep copy with every uscrn_validation value blanked and uscrn_soil_temp removed.

    Comparing two of these is what proves the promote touched NOTHING but its own field.
    """
    d = copy.deepcopy(data)
    d.pop('uscrn_soil_temp', None)
    for _p, arm in slots(d['crops']):
        arm['uscrn_validation'] = None
    return d


def retire_pilot(data):
    """Clear EVERY populated slot before the write.

    Two of the nine pilot records sit on `direct_sow[1]`, not `[0]`, so a write keyed to the cell
    never reaches them and they would survive as orphans -- a stale, unreproducible record sitting
    beside a fresh one on the same arm. The whole pilot is being replaced, so nothing is left
    standing. Split out as a function so the guard that catches its absence can be mutation-tested.
    """
    for _p, arm in slots(data['crops']):
        arm['uscrn_validation'] = None


def cell_sources(crop, kind, cid):
    node = (crop.get(kind) or {}).get(cid) or {}
    src = node.get('sources')
    return list(src) if isinstance(src, list) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON)
    ap.add_argument('--table', default=ZONE_TABLE)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    with open(args.canonical, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)
    table_payload = json.load(open(args.table, encoding='utf-8'))
    table = table_payload['zones']

    # PREFLIGHT -- the measured table must cover the ladder the roster actually needs.
    if not table:
        print('ABORT: zone table is empty')
        return 2
    slot_total_before = sum(1 for _ in slots(before['crops']))
    pilot_before = [p for p, a in slots(before['crops']) if a['uscrn_validation']]
    print('preflight: %d uscrn_validation slots, %d populated (the pilot)'
          % (slot_total_before, len(pilot_before)))
    if len(pilot_before) != 9:
        print('ABORT: expected the 9 pilot records, found %d' % len(pilot_before))
        return 2

    # ---- build ---------------------------------------------------------------------------
    per_target, skipped = UV.build_all(data, table)
    records = {k: UV.summarize(v) for k, v in per_target.items()}
    if not records:
        print('ABORT: no records built')
        return 2

    # ---- write ---------------------------------------------------------------------------
    retire_pilot(data)
    print('retired: %d pilot records cleared before the write' % len(pilot_before))

    applied = []
    for key, rec in sorted(records.items()):
        ci, kind, cid = key.split('|')
        crop = data['crops'][int(ci)]
        arm = (crop[kind][cid]['plantings'][0]['direct_sow'])[0]
        if 'uscrn_validation' not in arm:
            print('ABORT: %s %s %s has no uscrn_validation slot to write' % (crop['slug'], kind, cid))
            return 2
        rec = dict(rec)
        rec['zone_citations'] = cell_sources(crop, kind, cid)
        rec['promoted_in_session'] = SESSION
        arm['uscrn_validation'] = rec
        applied.append('%s %s %s' % (crop['slug'], kind, cid))

    data['uscrn_soil_temp'] = table_payload

    # ---- guards ----------------------------------------------------------------------------
    # G1 no slot was created or destroyed, and every built record landed somewhere.
    #    DELIBERATELY ORDERED BEFORE G2: adding or dropping a `uscrn_validation` key also trips
    #    G2's structural comparison, so with the two the other way round this check was
    #    unreachable and its mutation test passed only because an earlier guard fired -- the
    #    `guard-tests-pass-because-an-earlier-check-fires` shape. It stays first because
    #    "slot count moved 3403 -> 3404" says what happened and "something outside
    #    uscrn_validation changed" does not.
    after_paths = [p for p, _a in slots(data['crops'])]
    if len(after_paths) != slot_total_before:
        print('ABORT: slot count moved %d -> %d' % (slot_total_before, len(after_paths)))
        return 2
    populated = [p for p, a in slots(data['crops']) if a['uscrn_validation']]
    if len(populated) != len(records):
        print('ABORT: %d records built but %d slots populated' % (len(records), len(populated)))
        return 2
    print('verified: %d slots unchanged in count, %d now populated'
          % (len(after_paths), len(populated)))

    # G2 nothing outside uscrn_validation / uscrn_soil_temp moved. This is the load-bearing one:
    #    it proves no date, calendar, suitability value, citation or prose string shifted.
    if strip_uscrn(before) != strip_uscrn(data):
        print('ABORT: something outside uscrn_validation changed')
        return 2
    print('verified: no date, calendar, citation or prose string moved')

    # G3 every record names its threshold provenance -- Trevor's ruling, pinned.
    for p, arm in slots(data['crops']):
        r = arm['uscrn_validation']
        if not r:
            continue
        basis = r.get('anchor_threshold_basis')
        if basis != PROVENANCE and not str(basis).startswith(DECLARED_PREFIX):
            print('ABORT: record at %s carries no threshold provenance (%r)' % (p, basis))
            return 2
    print('verified: every record names its threshold provenance')

    # G4 every record's threshold is ITS OWN crop's, never a neighbour's. This is the specific
    #    defect that shipped in the pilot, so it is pinned by value, not by shape.
    for key, rec in records.items():
        ci, kind, cid = key.split('|')
        crop = data['crops'][int(ci)]
        arm = crop[kind][cid]['plantings'][0]['direct_sow'][0]
        want, _prov = UV.crop_threshold(crop, arm, ladder=table.get(
            rec.get('representative_zone') or cid, {}))
        got = int(rec['anchor_threshold'].split()[1].rstrip('F'))
        if want is not None and got != want:
            print('ABORT: %s %s validated at %dF, its own threshold is %dF'
                  % (crop['slug'], cid, got, want))
            return 2
    # G4b every record's stored_date is RE-DERIVED here from the cell's own resolved window,
    #     independently of what build_record put in the record. This is the check that catches
    #     the pilot's actual defect -- a record written against another crop's date -- and it
    #     catches a mis-targeted write generally. Mutation-tested by retargeting a record.
    for key, rec in records.items():
        ci, kind, cid = key.split('|')
        crop = data['crops'][int(ci)]
        node = crop[kind][cid]
        zone = rec.get('representative_zone') or cid
        if kind == 'zones':
            window = node.get('direct_sow')
        else:
            rnode = (node.get('resolved_by_zone') or {}).get(zone) or {}
            window = rnode.get('direct_sow') or rnode.get('plant_out')
        want = UV.spring_sow_date(window)
        if want is None or '%02d-%02d' % want != rec['stored_date']:
            print('ABORT: %s %s/%s stored_date %r is not this cell\'s own spring window (%r)'
                  % (crop['slug'], kind, cid, rec['stored_date'], window))
            return 2
    print('verified: every record uses its own crop threshold and its own stored date')

    # G4c the specific pilot defect, pinned by value. bok-choy/northern_tier carried lettuce's
    #     03-18 -- a date bok-choy stores in no zone (z6 is Mar 22, z7 is Mar 1). Note its 40F
    #     anchor is NOT part of the defect: that is declared on its own arm and sourced to its own
    #     MSU Extension prose ("bok choy ... germinates once soil reaches about 40 degrees F"),
    #     so it legitimately overrides the 45F optimal-band floor.
    bok = next((r for k, r in records.items()
                if data['crops'][int(k.split('|')[0])]['slug'] == PILOT_DEFECT[0]
                and k.split('|')[2] == PILOT_DEFECT[1]), None)
    if bok is not None and bok['stored_date'] == '03-18':
        print('ABORT: %s/%s still carries lettuce\'s 03-18' % PILOT_DEFECT)
        return 2
    print('verified: the pilot copy defect is closed')

    # A "no two crops share an identical record" guard was BUILT AND REMOVED, deliberately.
    # Rationale, so it is not rebuilt: identity between records across crops is NOT the
    # fingerprint of the pilot's copy defect. Six cucurbits (cucumber, english/pickling/slicing
    # cucumber, yellow summer squash, zucchini) legitimately produce byte-identical utah_dixie
    # records -- same 70F floor, same 'Mar 15 - Mar 29' window, same zone, so the same answer is
    # the correct answer. The first version compared whole germination BANDS rather than floors
    # and false-positived on a 90-vs-95 upper bound that has no bearing on the threshold. Once
    # corrected to compare floors it cannot fail at all, because G4a already pins every record's
    # threshold to its own crop's resolution and G4b re-derives every stored_date from its own
    # cell. A guard that cannot be made to fail is worse than no guard, so it is gone.

    # G5 the 9 pilot records were all replaced, none left standing.
    survivors = [p for p in pilot_before
                 if dict(next(a for q, a in slots(data['crops']) if q == p)['uscrn_validation'] or {})
                 == dict(next(a for q, a in slots(before['crops']) if q == p)['uscrn_validation'])]
    if survivors:
        print('ABORT: %d pilot records survived unchanged' % len(survivors))
        return 2
    print('verified: all 9 pilot records replaced')

    # G6 no em dash anywhere in what was written (CLAUDE.md, consumer copy).
    for _p, arm in slots(data['crops']):
        for k, v in (arm['uscrn_validation'] or {}).items():
            if isinstance(v, str) and '—' in v:
                print('ABORT: em dash written in %s' % k)
                return 2
    print('verified: no em dashes written')

    # G7 exact top-level footprint.
    newkeys = set(data) - set(before)
    if newkeys != {'uscrn_soil_temp'}:
        print('ABORT: unexpected new top-level keys %s' % sorted(newkeys))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly one new top-level key, nothing else at top level moved')

    status_counts = collections.Counter(r['status'] for r in records.values())
    print('\n%d records across %d cells' % (len(records), len(applied)))
    print('  by status : %s' % dict(status_counts.most_common()))
    print('  skipped   : %s' % dict(skipped.most_common()))
    print('  zone table: %d zones x %d thresholds'
          % (len(table), len(table_payload['method']['thresholds_f'])))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d records + the measured zone table' % len(records))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
