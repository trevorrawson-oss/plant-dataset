#!/usr/bin/env python3
"""GUARDED PROMOTE 2 of 3: re-derive strawberry's mid_south z7 cell from the anchor it declares.

DATA CHANGE. Consumer-visible planting and harvest dates move. Campaign B, hunt #1.

TWO DEFECTS IN ONE CELL, and they must be fixed together or the result is a coherent-looking
half-fix.

DEFECT 1 -- THE CELL CONTRADICTS ITS OWN DECLARED ANCHOR. `resolved_by_zone.7.resolved_from`
says `last_frost: "Apr 10"` (UAEX FSA6001, Arkansas Frost Zone D, the documented mid_south z7
anchor -- docs/reviews/notes/2026-07-20/mid_south_sources.md s1). Every derived value in the cell
reproduces exactly from **Apr 15** instead, which is `mid_atlantic`'s z7 anchor. Six endpoints,
six exact matches to the wrong region, zero to the declared one:

    arm             stored            from Apr 10 (declared)   from Apr 15 (mid_atlantic)
    plant_out       Apr 1 - Apr 22    Mar 27 - Apr 17          Apr 1 - Apr 22   <-- matches
    bloom           Apr 29 - May 20   Apr 24 - May 15          Apr 29 - May 20  <-- matches
    harvest_start   May 27            May 22                   May 27           <-- matches
    harvest_end     Jun 24            Jun 19                   Jun 24           <-- matches

mid_south was built from the mid_atlantic template. The anchor FIELD was correctly updated to
Apr 10; the resolved date STRINGS were carried across from mid_atlantic's Apr 15 arithmetic. That
is the find-and-replace class this campaign is named for, and it put every Mid-South zone 7
strawberry date five days late.

DEFECT 2 -- THE PLANT_OUT OFFSET MISQUOTES ITS OWN SOURCE. The arm's synthesis_note credits "the
University of Arkansas Cooperative Extension home garden matted-row guidance" for "about two weeks
before the last spring frost". That guidance is FSA6103, re-fetched from raw bytes 2026-08-03
(169,561 bytes, sha256 b55b80b5..., read with pypdf), and it says:

    "Virus-free, one-year-old dormant plants should be set out early in the spring, about three
     or four weeks before the average date of the last frost."

Three or four weeks, not two. So offset_days -14 / window_days 21 (which ran to a week AFTER last
frost) becomes -28 / 7, the document's stated band. The VALUE, the PROSE and the CITATION move
together or not at all -- campaign B's lavender lesson.

THE INVARIANT THIS PROMOTE ESTABLISHES, and the guard that would have caught defect 1 in the first
place: every resolved value in the cell must reproduce EXACTLY from `resolved_from.last_frost` plus
its arm's own offset. Nothing here is hardcoded; the new dates are COMPUTED from the declared
anchor, so the promote cannot reintroduce a foreign one.

WHAT IS DELIBERATELY *NOT* TOUCHED:
  z8          Its arms are absolute (`from: null`, "mid-Sep - early Oct"), so no frost arithmetic
              runs through it and the Apr 15 defect cannot have reached it. Guarded byte-identical.
  bloom arm   The OFFSET stays +14. Trevor ruled 2026-08-03 to leave it: FSA6103 gives only the
   offset    qualitative "Strawberries bloom very early in the spring, and the blossoms are easily
              killed by frost", so re-modelling it would swap one unsourced number for another.
              Only its ANCHOR is corrected here. The CASE 2 finding is filed in promote 3.
  harvest     Already repointed at uada_ext_berries by promote 1. Its April-June sentence covers
   citations  the corrected May 22 - Jun 19 exactly as it covered May 27 - Jun 24.
  the 61      The scan that found this also surfaced 61 other cells whose windows reproduce from
   leads      some other region's anchor. They are UNREAD leads, not defects, and a count is not
              evidence. They get their own read-don't-count pass, not a mass edit here.

FOOTPRINT: 1 new source_catalog entry (`uada_ext_fsa6103`); strawberry mid_south z7 only --
plant_out offset/window, 5 resolved date strings, the regenerated calendar[], 2 prose strings, and
plant_out's citation. z8 and every other crop byte-identical. COMPACT preserved.

    $ python3 tools/promote_strawberry_mid_south_z7_anchor.py --dry-run
    $ python3 tools/promote_strawberry_mid_south_z7_anchor.py --apply
"""
import argparse
import copy
import datetime
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from berry_calendar import derive_berry_calendar  # noqa: E402

CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '0ab9b42b58e5a047d302a4dd865b82b997688ad21129a3bd64f2cc1f5116820c'

SLUG = 'strawberry'
REGION = 'mid_south'
ZONE = '7'
YEAR = 2026

NEW_ID = 'uada_ext_fsa6103'
NEW_URL = 'https://www.uaex.uada.edu/publications/pdf/FSA-6103.pdf'
VERIFIED = '2026-08-03'

# FSA6103: "about three or four weeks before the average date of the last frost"
NEW_OFFSET, NEW_WINDOW = -28, 7
OLD_OFFSET, OLD_WINDOW = -14, 21

OLD_PROSE = 'about two weeks before the last spring frost'
NEW_PROSE = 'three to four weeks before the last spring frost'

CATALOG_ENTRY = {
    'id': NEW_ID,
    'name': 'UAEX FSA6103, Strawberry Production in the Home Garden',
    'publisher': 'University of Arkansas Division of Agriculture, Cooperative Extension Service',
    'url': NEW_URL,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': (
        'UAEX specific publication FSA6103, Arkansas home-garden strawberry. PLANTING DATE, the '
        'load-bearing sentence: "Virus-free, one-year-old dormant plants should be set out early '
        'in the spring, about three or four weeks before the average date of the last frost" -- '
        'backs the mid_south z7 matted-row plant_out band of last_frost -28 to -21. TRAINING '
        'SYSTEM: "Use of the matted-row system is recommended for home garden production", which '
        'backs the z7 perennial matted-row track. It also states that the annual hill or '
        'plasticulture system "is not recommended for home garden strawberry production at this '
        'time due to the susceptibility of these varieties to diseases and the need for soil '
        'fumigation" -- in tension with the uada_ext_berries overview page, which offers the '
        'annual system to home gardeners; recorded as a finding rather than silently resolved. '
        'BLOOM is qualitative only ("Strawberries bloom very early in the spring, and the '
        'blossoms are easily killed by frost") and publishes NO bloom date and NO harvest dates.'
    ),
}


def dt(s):
    return datetime.datetime.strptime('%s %d' % (s.strip(), YEAR), '%b %d %Y')


def fmt(d):
    return d.strftime('%b %-d')


def cell_of(data):
    crop = next(c for c in data['crops'] if c['slug'] == SLUG)
    return crop['regions'][REGION]


def derive_expected(region):
    """Every z7 resolved value, COMPUTED from the cell's own declared anchor. Never hardcoded."""
    cell = region['resolved_by_zone'][ZONE]
    base = dt((cell.get('resolved_from') or {})['last_frost'])
    p = region['plantings'][0]
    out = {}
    for arm in ('plant_out', 'bloom'):
        a = p[arm][0]
        od, wd = a['offset_days'], a['window_days']
        out[arm] = '%s - %s' % (fmt(base + datetime.timedelta(days=od)),
                                fmt(base + datetime.timedelta(days=od + wd)))
    hs = p['harvest_start'][0]['offset_days']
    he = p['harvest_end'][0]['offset_days']
    out['harvest_start'] = fmt(base + datetime.timedelta(days=hs))
    out['harvest_end'] = fmt(base + datetime.timedelta(days=he))
    out['harvest'] = '%s - %s' % (out['harvest_start'], out['harvest_end'])
    return out


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
        print('ABORT: canonical sha %s != expected %s' % (sha[:12], args.expect_sha[:12]))
        return 1
    data = json.loads(raw.decode('utf-8'))
    before = copy.deepcopy(data)

    region = cell_of(data)
    cell = region['resolved_by_zone'][ZONE]
    arm = region['plantings'][0]['plant_out'][0]

    # ---- preflight ---------------------------------------------------------------------------
    if NEW_ID in data['source_catalog']:
        print('ABORT: %s already catalogued -- promote already run' % NEW_ID)
        return 1
    anchor = (cell.get('resolved_from') or {}).get('last_frost')
    if anchor != 'Apr 10':
        print('ABORT: declared anchor is %r, expected Apr 10 -- wrong base or the anchor moved'
              % anchor)
        return 1
    if (arm.get('offset_days'), arm.get('window_days')) != (OLD_OFFSET, OLD_WINDOW):
        print('ABORT: plant_out arm is %r/%r, expected %r/%r'
              % (arm.get('offset_days'), arm.get('window_days'), OLD_OFFSET, OLD_WINDOW))
        return 1

    # The defect must still be present. If the stored values ALREADY reproduce from the declared
    # anchor there is nothing to fix, and running would be acting on a stale record.
    pre_expected = derive_expected(region)
    if all(cell.get(k) == v for k, v in pre_expected.items()):
        print('ABORT: z7 already reproduces from its declared anchor -- nothing to fix')
        return 1
    stale = {k: (cell.get(k), v) for k, v in pre_expected.items() if cell.get(k) != v}
    print('DEFECT CONFIRMED -- %d z7 value(s) do not reproduce from declared anchor %s:'
          % (len(stale), anchor))
    for k, (got, want) in sorted(stale.items()):
        print('   %-14s stored=%-18s from-declared-anchor=%s' % (k, got, want))

    # ---- the edit ----------------------------------------------------------------------------
    data['source_catalog'][NEW_ID] = copy.deepcopy(CATALOG_ENTRY)

    arm['offset_days'], arm['window_days'] = NEW_OFFSET, NEW_WINDOW
    arm['sources'] = [NEW_ID]
    arm['anchoring_urls'] = {NEW_ID: {'url': NEW_URL, 'verified': VERIFIED}}
    if OLD_PROSE not in arm.get('synthesis_note', ''):
        print('ABORT: plant_out synthesis_note does not contain the expected phrase')
        return 1
    arm['synthesis_note'] = arm['synthesis_note'].replace(OLD_PROSE, NEW_PROSE)

    expected = derive_expected(region)
    for k, v in expected.items():
        cell[k] = v

    if OLD_PROSE not in cell.get('grown_as_note_seasoned', ''):
        print('ABORT: z7 grown_as_note_seasoned does not contain the expected phrase')
        return 1
    cell['grown_as_note_seasoned'] = cell['grown_as_note_seasoned'].replace(
        OLD_PROSE, NEW_PROSE)

    new_cal = derive_berry_calendar(cell.get('grown_as'), cell)
    if new_cal is None:
        print('ABORT: calendar deriver returned None for the rebuilt cell')
        return 1
    cell['calendar'] = new_cal

    # ---- guards ------------------------------------------------------------------------------
    fails = []
    b_region = cell_of(before)
    b_cell = b_region['resolved_by_zone'][ZONE]

    # THE core invariant: every resolved value reproduces from the DECLARED anchor.
    for k, v in derive_expected(region).items():
        if cell.get(k) != v:
            fails.append('%s = %r does not reproduce from declared anchor (%r)'
                         % (k, cell.get(k), v))

    # The anchor is the FIXED POINT: the defect must be fixed by moving the dates to the anchor,
    # never by moving the anchor to the dates. Compared against `before`, which is the only form
    # of this check that can actually fail -- a re-read of `cell` cannot, since preflight already
    # asserted Apr 10 and the edit never writes resolved_from.
    if json.dumps(cell.get('resolved_from'), sort_keys=True) != \
       json.dumps(b_cell.get('resolved_from'), sort_keys=True):
        fails.append('resolved_from changed; the anchor is the fixed point here')

    # every stored value must actually have MOVED off the mid_atlantic arithmetic
    ma = dt('Apr 15')
    p = region['plantings'][0]
    for a_name in ('bloom',):
        a = p[a_name][0]
        bad = '%s - %s' % (fmt(ma + datetime.timedelta(days=a['offset_days'])),
                           fmt(ma + datetime.timedelta(days=a['offset_days'] + a['window_days'])))
        if cell.get(a_name) == bad:
            fails.append('%s still equals the mid_atlantic Apr 15 arithmetic' % a_name)

    # NOTE: "did the edit set the arm offsets / the citation" checks lived here and were REMOVED,
    # not left as decoration -- they re-read the same object the edit had just written two dozen
    # lines above, so no input could make them fail. What they were meant to protect is covered by
    # a check that CAN fail: the resolved plant_out string is recomputed from the arm's offsets, so
    # a wrong offset surfaces as a reproduction failure in the core invariant above.

    if set(data['source_catalog']) - set(before['source_catalog']) != {NEW_ID}:
        fails.append('catalog delta is not exactly {%s}' % NEW_ID)

    # prose must no longer misquote the source
    blob = json.dumps(region, ensure_ascii=False)
    if 'two weeks before the last spring frost' in blob:
        fails.append('prose still says "two weeks before the last spring frost"')
    # (the "NEW_PROSE is present" pair that sat here was removed for the same reason: str.replace
    # on a string the preflight proved contains OLD_PROSE always yields NEW_PROSE. The reachable
    # half of that intent is the region-wide scan above, which a stray occurrence elsewhere trips.)

    # NOTE: a "stored calendar equals the deriver's output" check sat here and was REMOVED. It
    # called derive_berry_calendar on the same cell the line above had just filled FROM
    # derive_berry_calendar, so the two agreed by construction under every input including a
    # sabotaged deriver -- mutation testing caught it returning green while the deriver was
    # stubbed to twelve 'dormant' months. The real enforcement is external and does fail:
    # berry_calendar_violations() in the gate suite re-derives from the cell's own dates.
    if len(cell['calendar']) != 12:
        fails.append('calendar[] is not 12 months')

    # z8 and everything outside this cell must be untouched
    if json.dumps(region['resolved_by_zone']['8'], sort_keys=True) != \
       json.dumps(b_region['resolved_by_zone']['8'], sort_keys=True):
        fails.append('z8 changed; it is absolute-windowed and out of scope')
    if json.dumps(region['plantings'][1], sort_keys=True) != \
       json.dumps(b_region['plantings'][1], sort_keys=True):
        fails.append('plantings[1] (z8 track) changed; out of scope')
    for a_name in ('bloom', 'harvest_start', 'harvest_end'):
        a = json.dumps(region['plantings'][0][a_name], sort_keys=True)
        b = json.dumps(b_region['plantings'][0][a_name], sort_keys=True)
        if a != b:
            fails.append('plantings[0].%s arm changed; only plant_out moves' % a_name)
    for c_a, c_b in zip(data['crops'], before['crops']):
        if c_a['slug'] != SLUG and json.dumps(c_a, sort_keys=True) != \
                json.dumps(c_b, sort_keys=True):
            fails.append('crop %s changed; only %s is in scope' % (c_a['slug'], SLUG))
            break
    for rk in region:
        if rk not in ('plantings', 'resolved_by_zone'):
            if json.dumps(region[rk], sort_keys=True) != json.dumps(b_region[rk], sort_keys=True):
                fails.append('mid_south.%s changed; out of scope' % rk)

    if fails:
        print('\nABORT -- %d guard(s) failed:' % len(fails))
        for f in fails:
            print('   x %s' % f)
        return 1

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: output has a trailing newline; canonical is COMPACT with none')
        return 1

    print('\nALL GUARDS PASS. z7 re-derived from its declared anchor %s:' % anchor)
    for k in ('plant_out', 'bloom', 'harvest_start', 'harvest_end', 'harvest'):
        print('   %-14s %-18s -> %s' % (k, b_cell.get(k), cell.get(k)))
    print('   plant_out arm  %+d/%d -> %+d/%d  (FSA6103 three-or-four-weeks band)'
          % (OLD_OFFSET, OLD_WINDOW, NEW_OFFSET, NEW_WINDOW))
    print('   calendar       %s' % (b_cell.get('calendar'),))
    print('             ->   %s' % (cell.get('calendar'),))
    print('   new sha256: %s' % hashlib.sha256(out).hexdigest())
    if args.dry_run:
        print('   DRY RUN -- nothing written.')
        return 0
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('   WRITTEN to %s' % args.canonical)
    return 0


if __name__ == '__main__':
    sys.exit(main())
