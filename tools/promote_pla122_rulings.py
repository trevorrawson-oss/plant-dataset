#!/usr/bin/env python3
"""GUARDED PROMOTE: Trevor's rulings on the five open campaign C findings (PLA-122).

UNLIKE the two promotes before it, THIS ONE MOVES CONSUMER-FACING STRINGS. Four resolved
`plant_out` windows change and three display strings are reconciled, so the blanket "not one
consumer string moves" guard is replaced by a tighter one: an ENUMERATED set of exact
before/after values, with a guard proving nothing else in those cells moved.

Evidence: docs/2026-08-05-pla122-rulings.md. Base `ca40d90f`.

THE FEB 1 -> FEB 15 TIGHTENING, AND WHY THE PRECOMPUTE WORRY INVERTS. PLA-122 flagged that these
cells are `resolution_method: static_precompute` and warned that patching the resolved string
leaves the upstream rule (`plant_out` from `last_frost`, `offset_days: 14`) able to regenerate
Feb 1. Measured before touching anything, and it is the other way round:

    cell                          declared last_frost   rule gives    stored (before)
    cantaloupe/watermelon z9,z10  Jan 31                Feb 14        Feb 1

**The rule never produced Feb 1.** Jan 31 + 14 = Feb 14, so the stored Feb 1 was the value that
did NOT reproduce, and this ruling moves the cells to within one day of what their own declared
anchor already implies. AZ1005's first seed mark (Feb 15) and the cell's own frost arithmetic
(Feb 14) are two independent lines landing in the same place. No offset needs reconciling; the
edit makes these cells MORE reproducible, not less. A guard pins that relationship so a later
offset change cannot silently break it.

Nothing re-runs the precompute over existing cells either: `build_region_shells.py` reshapes
key-sets idempotently and no-clobber, `build_mid_south_cells.py` is a one-off region build, and
every other tool touching `offset_days` alongside `resolved_by_zone` is a one-off promote, a gate
or a scan. `frost_anchor_reproduction_gate` reports 0 violations over 1,409 cells and cannot be
tripped by this edit, since it fires only when two or more arm types agree on a DIFFERENT anchor.

THE LATE ENDS STAY. Trevor's ruling: late is the safe direction, and both divergences are already
filed. So cantaloupe keeps Aug 15 against the document's Jul 15, and neither `harvest` arm moves.

WATERMELON'S SUMMER PLANTING IS DECLARED, NOT DROPPED. AZ1005 gives low-desert watermelon S at
Feb 15, Mar 1 and Mar 15 and nothing else all year, which is a document actively indicating no
second window rather than merely being silent. Trevor was offered dropping it outright and did not
take that; the finding flips to `accepted_modeled` with the reasoning recorded, and the two
`second_planting` nodes stay on the institution root exactly as the previous promote left them.

TURNIP IS A DISPLAY-STRING RECONCILIATION, NOT A DATA CHANGE -- the check PLA-122 asked for.
`first_plant_date` already reads `Sep 1` and `last_plant_date` already reads `May 31`, matching UC
Master Gardeners San Diego ("Coastal: Seeds can be planted from September to May"). Only the
human-readable `plant_out` was stuck at `Sep - Oct`. So the sourced window was already in the data
and only its rendering understated it. A guard asserts `first_plant_date` and `last_plant_date` do
NOT move, which is what makes this provably a reconciliation.

  The wrap-around format is this crop's own: its `harvest` string already reads `Nov - May`.

  CHECKED AND DELIBERATELY NOT CHANGED: the `calendar` array still marks Sep and Oct as `plant`
  and Nov through May as `harvest`. Those months are now both, and a calendar cell carries ONE
  token per month, so the overlap cannot be expressed. Harvest is the more useful signal for a
  reader standing in January. This is the ribbon-granularity limit PLA-122 already identified as
  an app-rendering question in the Code lane, and it is recorded rather than papered over.

GARLIC AND LAVENDER ARE DECLARATIONS, NOT EDITS. No date moves on either. garlic gains a
`plantings_provenance` block on `rgv` in the shape its own other thirteen regions already use, and
both findings flip to `accepted` with Trevor's reasoning recorded in a `resolution` field, the
convention campaign B's rulings established.

    $ python3 tools/promote_pla122_rulings.py --dry-run
    $ python3 tools/promote_pla122_rulings.py --apply
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'ca40d90f008b645a8a01791b30d454759c42d905e1b3fc552ab0c25f9bf07e49'
SESSION = 'pla122_rulings_2026_08_05'

# --- the date edits, EVERY value enumerated before and after -----------------------------------
# (slug, region, zone) -> {field: (before, after)}
DATE_EDITS = {}
for _s in ('cantaloupe', 'watermelon'):
    for _z in ('9', '10'):
        DATE_EDITS[(_s, 'low_desert_az', _z)] = {
            'plant_out': ('Feb 1 - Mar 15', 'Feb 15 - Mar 15'),
            'first_plant_date': ('Feb 1', 'Feb 15'),
        }
for _z in ('9', '10', '11'):
    DATE_EDITS[('turnip', 'ca_south_coast', _z)] = {
        'plant_out': ('Sep - Oct', 'Sep - May'),
    }

# turnip's window was ALREADY in the data; these must be untouched, which is what proves the
# change is a display reconciliation rather than a data change.
TURNIP_PINNED = {'first_plant_date': 'Sep 1', 'last_plant_date': 'May 31'}

# The melons' spring start must land within this many days of `last_frost + offset_days`, read
# from each cell's OWN declared anchor. Before this promote the gap was 13 days.
ANCHOR_TOLERANCE_DAYS = 1

GARLIC_PROVENANCE = {
    'model': 'author_fresh',
    'basis': (
        'Fall-planted overwintering cycle. plant_out (Oct 15 - Nov 15) is sourced: Texas A&M '
        'AgriLife Bexar County garlic guidance, which this crop already cites in se_gulf and '
        'warm_arid, states garlic "can be planted in the late fall" and that "if planted in '
        'October, may have tops showing above the soil and be well rooted by November". '
        'HARVEST IS MODELED, not individually source-verified: harvest_start (Apr 13) is derived '
        'as plant_out plus 180 days and no Rio Grande Valley table publishes a garlic row at all. '
        'Both the RGV Homeowner Vegetable Guide 2022 and Vegetable Crops of the Lower Rio Grande '
        'Valley were read directly 2026-08-05 and neither lists garlic. Trevor ruled 2026-08-05 '
        'that Apr 13 stands with this declaration rather than reverting to the May or June figure '
        'the Bexar County and se_gulf material implies, because the Rio Grande Valley is '
        'genuinely warmer than both and reverting would import a colder region\'s number. '
        'See rgv_garlic_harvest_start_runs_ahead_of_every_source.'),
    'supersedes': None,
}

# --- the rulings, transcribed ------------------------------------------------------------------
# (slug, finding id) -> (new status, resolution prose)
RULINGS = {
    ('cantaloupe', 'low_desert_az_cantaloupe_window_runs_past_az1005_at_both_ends'): (
        'accepted',
        'RULED 2026-08-05 (PLA-122). Spring open TIGHTENED Feb 1 to Feb 15 to match AZ1005\'s '
        'first seed mark. The Feb 1 open was unsourced and early in the direction that costs a '
        'reader a planting, and the cell already cites AZ1005, so it was citing a document that '
        'disagreed with it. Confirmed while applying: Feb 15 is also within one day of what this '
        'cell\'s OWN declared anchor implies (last_frost Jan 31 plus the arm\'s 14-day offset '
        'gives Feb 14), so the document and the frost arithmetic agree and the previous Feb 1 '
        'reproduced from neither. The LATE end stays at Aug 15 against the document\'s Jul 15: '
        'late is the safe direction for a direct-sown cucurbit, and the divergence stays on the '
        'record here rather than being edited away.'),
    ('watermelon', 'low_desert_az_watermelon_summer_planting_absent_from_az1005'): (
        'accepted_modeled',
        'RULED 2026-08-05 (PLA-122). Spring open TIGHTENED Feb 1 to Feb 15, same reasoning and '
        'same anchor confirmation as cantaloupe. The Jul 15 to Aug 15 second planting is '
        'DECLARED MODELED and kept: AZ1005 marks low-desert watermelon at Feb 15, Mar 1 and Mar '
        '15 and nothing else all year, which is a document actively indicating no second window '
        'rather than merely being silent about one, and that is stronger evidence than absence. '
        'Dropping the second planting outright was offered and NOT taken. Its two nodes stay on '
        'the institution root rather than citing AZ1005, because AZ1005 contradicts them.'),
    ('garlic', 'rgv_garlic_harvest_start_runs_ahead_of_every_source'): (
        'accepted',
        'RULED 2026-08-05 (PLA-122). harvest_start stays at Apr 13, DECLARED MODELED via this '
        'region\'s new plantings_provenance block. No new source exists: the RGV Homeowner '
        'Vegetable Guide 2022 and Vegetable Crops of the Lower Rio Grande Valley were both read '
        'directly and neither lists garlic at all, consistent with campaign C\'s zero-rows '
        'finding. Keeping Apr 13 with an explicit modeled label beats reverting to a figure known '
        'to be derived for a colder region: Bexar County and our own se_gulf rows say May to '
        'June, and the Rio Grande Valley is genuinely warmer than both.'),
    ('lavender', 'warm_arid_lavender_plant_out_window_is_unsourced'): (
        'accepted',
        'RULED 2026-08-05 (PLA-122). DECLARED MODELED; no date changes. University of Arizona '
        'Cooperative Extension, the other in-region T1 institution, was searched alongside '
        'general desert-lavender sources: no university-published source gives a planting window '
        'for Lavandula in the desert Southwest. What exists is consumer and blog tier and is not '
        'T1-admissible. Those non-citable sources do converge on late fall or early spring while '
        'avoiding May through September, which brackets the existing Apr-May / Sep-Oct window, so '
        'the window is probably not wrong, only uncited. More searching will not find this. '
        'SEPARATE AND NOT IN THIS PATCH: the two mislabelled source ids this finding also records '
        '(nmsu_chart pointing at lowwaterplants.nmsu.edu, nmsu_donaana_mg pointing at RR-770) '
        'need new catalog ids minted and belong to the structural lane as their own issue.'),
    ('turnip', 'ca_south_coast_turnip_source_supports_a_wider_window_than_we_publish'): (
        'accepted',
        'RULED 2026-08-05 (PLA-122). Confirmed by direct fetch of mastergardenersd.org/turnip/: '
        '"Coastal: Seeds can be planted from September to May." UC Master Gardeners San Diego, '
        'T1, unambiguous. THE CHECK PLA-122 ASKED FOR, and the answer is that this was a DISPLAY '
        'reconciliation and not a data change: first_plant_date already read Sep 1 and '
        'last_plant_date already read May 31, so the sourced window was in the data all along and '
        'only the human-readable plant_out string was stuck at "Sep - Oct". That string now reads '
        '"Sep - May", the wrap-around format this crop\'s own harvest string already uses. '
        'CHECKED AND DELIBERATELY NOT CHANGED: the calendar array still marks Sep and Oct plant '
        'and Nov through May harvest. Those months are now both, and a calendar cell carries one '
        'token per month, so the overlap cannot be represented; harvest is the more useful signal '
        'for a reader standing in January. That is the ribbon-granularity limit recorded in '
        'PLA-122 as an app-rendering question, not a data defect.'),
}

CROPS = ('cantaloupe', 'garlic', 'lavender', 'turnip', 'watermelon')

# Hand-written, never derived from the edit tables. G7 checks the data against these AND these
# against the tables, in both directions.
CELLS_CHANGED_PER_CROP = {'cantaloupe': 2, 'watermelon': 2, 'turnip': 3, 'garlic': 0,
                          'lavender': 0}

# The finding ids this promote is ALLOWED to move, written out longhand. G6 first checks this
# against RULINGS and then checks the data against this. A first version computed it as
# `{fid for _s, fid in RULINGS}`, which made G6 incapable of firing: every status change the
# promote makes comes from RULINGS, so the permitted set always contained it by construction.
# Sixth instance of that shape in three promotes -- see the lesson in the session doc.
RULED_IDS = (
    'ca_south_coast_turnip_source_supports_a_wider_window_than_we_publish',
    'low_desert_az_cantaloupe_window_runs_past_az1005_at_both_ends',
    'low_desert_az_watermelon_summer_planting_absent_from_az1005',
    'rgv_garlic_harvest_start_runs_ahead_of_every_source',
    'warm_arid_lavender_plant_out_window_is_unsourced',
)
EM_DASH = chr(8212)


def parse_md(s, year=2026):
    return dt.datetime.strptime('%s %d' % (s, year), '%b %d %Y').date()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON)
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
    crops = {c['slug']: c for c in data['crops']}

    # PREFLIGHT 1 -- every enumerated BEFORE value is still exactly what this promote expects.
    for (slug, region, zone), fields in sorted(DATE_EDITS.items()):
        cell = crops[slug]['regions'][region]['resolved_by_zone'][zone]
        for field, (old, _new) in sorted(fields.items()):
            if cell.get(field) != old:
                print('ABORT: %s %s z%s %s expected %r, found %r'
                      % (slug, region, zone, field, old, cell.get(field)))
                return 2
    print('preflight: all %d cells carry their pinned pre-state values' % len(DATE_EDITS))

    # PREFLIGHT 2 -- turnip's already-correct data fields, pinned so the claim that this is a
    # DISPLAY reconciliation is checkable rather than asserted.
    for zone in ('9', '10', '11'):
        cell = crops['turnip']['regions']['ca_south_coast']['resolved_by_zone'][zone]
        for field, want in sorted(TURNIP_PINNED.items()):
            if cell.get(field) != want:
                print('ABORT: turnip z%s %s is %r, expected %r -- the premise that the sourced '
                      'window is already in the data does not hold' % (zone, field, cell.get(field), want))
                return 2
    print('preflight: turnip already stores Sep 1 / May 31, so this is a display reconciliation')

    # PREFLIGHT 3 -- every ruling targets a finding that exists and is currently open.
    for (slug, fid), (_st, _res) in sorted(RULINGS.items()):
        got = [f for f in ((crops[slug].get('verification_status') or {}).get('open_findings')
                           or []) if f.get('id') == fid]
        if len(got) != 1:
            print('ABORT: %s carries %d findings with id %s, expected 1' % (slug, len(got), fid))
            return 2
        if got[0].get('status') != 'open':
            print('ABORT: %s %s is %r, not open -- already ruled?'
                  % (slug, fid, got[0].get('status')))
            return 2
    print('preflight: all %d findings present and open' % len(RULINGS))

    if 'plantings_provenance' in crops['garlic']['regions']['rgv']:
        print('ABORT: garlic rgv already carries plantings_provenance')
        return 2

    # ---- edits -----------------------------------------------------------------------------
    applied = []
    for (slug, region, zone), fields in sorted(DATE_EDITS.items()):
        cell = crops[slug]['regions'][region]['resolved_by_zone'][zone]
        for field, (_old, new) in sorted(fields.items()):
            cell[field] = new
        applied.append('%s %s z%s  %s' % (slug, region, zone,
                                          ', '.join('%s -> %r' % (f, v[1])
                                                    for f, v in sorted(fields.items()))))
    crops['garlic']['regions']['rgv']['plantings_provenance'] = copy.deepcopy(GARLIC_PROVENANCE)
    applied.append('garlic rgv  + plantings_provenance (harvest declared MODELED)')

    for (slug, fid), (status, resolution) in sorted(RULINGS.items()):
        f = [x for x in crops[slug]['verification_status']['open_findings']
             if x.get('id') == fid][0]
        f['status'] = status
        f['resolution'] = resolution
        f['resolved_in_session'] = SESSION
        applied.append('%s ruling %s -> %s' % (slug, fid, status))

    # ---- guards ----------------------------------------------------------------------------
    bmap = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}

    # G1 -- THE ANCHOR CHECK, and the direct answer to PLA-122's precompute worry. Each melon
    # cell's new spring start must sit within tolerance of `last_frost + offset_days` read from
    # that cell's OWN declared anchor. Before this promote the gap was 13 days; after it, 1.
    for (slug, region, zone), fields in sorted(DATE_EDITS.items()):
        if 'first_plant_date' not in fields:
            continue
        cell = crops[slug]['regions'][region]['resolved_by_zone'][zone]
        anchor = (cell.get('resolved_from') or {}).get('last_frost')
        arm = crops[slug]['regions'][region]['plantings'][0]['plant_out'][0]
        if not anchor or arm.get('from') != 'last_frost':
            print('ABORT: %s %s z%s cannot be anchor-checked' % (slug, region, zone))
            return 2
        implied = parse_md(anchor) + dt.timedelta(days=arm['offset_days'])
        gap = abs((parse_md(cell['first_plant_date']) - implied).days)
        if gap > ANCHOR_TOLERANCE_DAYS:
            print('ABORT: %s %s z%s new start %s is %d days from its own anchor arithmetic (%s + '
                  '%d = %s)' % (slug, region, zone, cell['first_plant_date'], gap, anchor,
                                arm['offset_days'], implied.strftime('%b %-d')))
            return 2
    print('verified: every tightened start is within %d day of its own declared frost anchor'
          % ANCHOR_TOLERANCE_DAYS)

    # G2 -- inside every touched cell, ONLY the enumerated fields moved. This is what replaces the
    # blanket consumer-copy tripwire the previous promotes used.
    for (slug, region, zone), fields in sorted(DATE_EDITS.items()):
        b = bmap[slug]['regions'][region]['resolved_by_zone'][zone]
        a = aa[slug]['regions'][region]['resolved_by_zone'][zone]
        moved = {k for k in set(b) | set(a) if b.get(k) != a.get(k)}
        if moved != set(fields):
            print('ABORT: %s %s z%s moved %s, expected exactly %s'
                  % (slug, region, zone, sorted(moved), sorted(fields)))
            return 2
    print('verified: inside every touched cell, ONLY the enumerated fields moved')

    # G3 -- the melons' harvest arms, second_planting and calendar are untouched. Trevor's ruling
    # keeps the late ends and keeps watermelon's summer planting; this proves neither drifted.
    for slug in ('cantaloupe', 'watermelon'):
        for zone in ('9', '10'):
            b = bmap[slug]['regions']['low_desert_az']['resolved_by_zone'][zone]
            a = aa[slug]['regions']['low_desert_az']['resolved_by_zone'][zone]
            for key in ('harvest', 'harvest_start', 'harvest_end', 'second_planting', 'calendar',
                        'last_plant_date'):
                if b.get(key) != a.get(key):
                    print('ABORT: %s z%s %s changed and must not have' % (slug, zone, key))
                    return 2
    print('verified: melon harvest arms, second_planting and calendars are byte-identical')

    # G4 -- turnip's DATA fields did not move. Without this the "display reconciliation" claim is
    # just prose.
    for zone in ('9', '10', '11'):
        b = bmap['turnip']['regions']['ca_south_coast']['resolved_by_zone'][zone]
        a = aa['turnip']['regions']['ca_south_coast']['resolved_by_zone'][zone]
        for key in ('first_plant_date', 'last_plant_date', 'harvest', 'calendar', 'heat_pause'):
            if b.get(key) != a.get(key):
                print('ABORT: turnip z%s %s changed -- this was meant to be display only' % (zone, key))
                return 2
    print('verified: turnip first/last_plant_date, harvest, calendar and heat_pause untouched')

    # G5 -- rulings landed with the right status and carry their reasoning.
    for (slug, fid), (status, _res) in sorted(RULINGS.items()):
        f = [x for x in aa[slug]['verification_status']['open_findings']
             if x.get('id') == fid][0]
        if f.get('status') != status:
            print('ABORT: %s %s is %r, expected %r' % (slug, fid, f.get('status'), status))
            return 2
        if not f.get('resolution') or f.get('resolved_in_session') != SESSION:
            print('ABORT: %s %s lost its resolution or session stamp' % (slug, fid))
            return 2
        if 'RULED 2026-08-05' not in f['resolution']:
            print('ABORT: %s %s resolution carries no ruling date' % (slug, fid))
            return 2
        if EM_DASH in f['resolution']:
            print('ABORT: em dash in %s resolution' % fid)
            return 2
    if EM_DASH in GARLIC_PROVENANCE['basis']:
        print('ABORT: em dash in the garlic provenance basis')
        return 2
    print('verified: %d rulings landed with status, resolution and session stamp' % len(RULINGS))

    # G6 -- NO OTHER finding anywhere changed status. A ruling promote that quietly closes a
    # neighbouring finding is the failure this guards.
    if sorted(RULED_IDS) != sorted(fid for _s, fid in RULINGS):
        print('ABORT: RULED_IDS disagrees with RULINGS\n  only in RULED_IDS: %s\n  only in RULINGS: %s'
              % (sorted(set(RULED_IDS) - {f for _s, f in RULINGS}),
                 sorted({f for _s, f in RULINGS} - set(RULED_IDS))))
        return 2
    ruled = set(RULED_IDS)
    for slug in bmap:
        bf = {f.get('id'): f.get('status') for f
              in ((bmap[slug].get('verification_status') or {}).get('open_findings') or [])
              if isinstance(f, dict)}
        af = {f.get('id'): f.get('status') for f
              in ((aa[slug].get('verification_status') or {}).get('open_findings') or [])
              if isinstance(f, dict)}
        for fid in set(bf) | set(af):
            if bf.get(fid) != af.get(fid) and fid not in ruled:
                print('ABORT: %s finding %s changed status and is not in this ruling set'
                      % (slug, fid))
                return 2
    print('verified: no finding outside the ruling set changed status')

    # G7 exact footprint, checked against HAND-WRITTEN constants in both directions.
    changed = sorted(s for s in bmap if bmap[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
        return 2
    if sorted(CELLS_CHANGED_PER_CROP) != sorted(CROPS):
        print('ABORT: CELLS_CHANGED_PER_CROP does not cover exactly CROPS')
        return 2
    for slug in CROPS:
        want = CELLS_CHANGED_PER_CROP[slug]
        from_table = sum(1 for (s, _r, _z) in DATE_EDITS if s == slug)
        if want != from_table:
            print('ABORT: CELLS_CHANGED_PER_CROP[%s] = %d but DATE_EDITS holds %d'
                  % (slug, want, from_table))
            return 2
        got = 0
        for rn, r in bmap[slug].get('regions', {}).items():
            for z, bcell in (r.get('resolved_by_zone') or {}).items():
                if bcell != aa[slug]['regions'][rn]['resolved_by_zone'][z]:
                    got += 1
        if got != want:
            print('ABORT: %s had %d resolved cells change, expected %d' % (slug, got, want))
            return 2
    for k in before:
        if k == 'crops':
            continue
        if before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly %d crops and %d resolved cells changed, nothing else at top level'
          % (len(CROPS), sum(CELLS_CHANGED_PER_CROP.values())))

    print('\n%d edits:' % len(applied))
    for a in applied:
        print('  ' + a)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits across %d crops' % (len(applied), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
