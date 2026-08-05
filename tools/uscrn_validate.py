#!/usr/bin/env python3
"""Compare stored spring sowing dates against the MEASURED USCRN soil-temperature record.

    python3 tools/uscrn_validate.py                 # report
    python3 tools/uscrn_validate.py --json OUT      # emit records for the promote

WHAT IS COMPARED, AND WHAT IS DELIBERATELY NOT
----------------------------------------------
Only `direct_sow` arms, and only on crops whose `propagule` is `seed`. That narrowing is not
arbitrary -- it is the one `tools/soil_temp_floor_scan.py` already proved on this roster:
`germination_temp_f` governs a SEED going into the ground, and for a crop that goes out as a
nursery transplant it describes an indoor tray instead (thyme, rosemary and lavender are the
worked examples there). The other 2,978 `uscrn_validation` slots in the file are out of scope by
construction, not by omission:

  * `harvest_start` / `harvest_end` (1,940 slots) -- harvest timing follows days-to-maturity from
    the planting date. A spring soil crossing has no bearing on it.
  * `start_indoors` (326 slots) -- indoors, in a heated house, in a tray. Field soil at 5cm is
    not the governing temperature.
  * `plant_out` / `transplant` (712 slots) -- a real soil gate exists for setting out warm-season
    transplants, but this repo carries no sourced number for it, and `germination_temp_f` is the
    wrong one (that is the seed's requirement, not the seedling's). Inventing one to fill the
    field's shape is the `fill-the-shape-is-the-defect` failure. Left null, on purpose.

THE THRESHOLD comes from the crop, never from a neighbour:
  1. the arm's own declared anchor (`from: soil_temp_40f`) when it has one; else
  2. `germination_temp_f[0]`, the crop's certified germination floor.
A floor that is not on the measured ladder is REFUSED rather than rounded to a neighbour.

THE VERDICT is `status`, and it compares the sowing WINDOW against the measured crossing
distribution -- see `position()` for the four values and why. Two earlier readings were built,
measured, and rejected on this roster, both recorded here so they are not rebuilt:

  * the Phase 1.1 fixed-day bands (within 3 days aligned, 4 to 10 drift, beyond 10 misaligned)
    returned 170 of 228 cells "misaligned", including 16 of the 29 whose arm declares its own
    soil anchor. A zone's own crossing swings 30 to 90 days between p10 and p90, so a 3-day band
    is finer than the quantity it measures and reports variance as error. RETAINED as the
    reported `offset_band`, since the methodology named it, but it is not the verdict.
  * comparing the window's OPENING date against the median crossing returned 67 cells "often too
    cold". A sowing window is a range a gardener picks a day inside, so its opening sits before
    the typical crossing by construction. That is a property of windows, not a defect.

`risk` is the directional read of `status`: sowing weeks after the soil is ready is a choice,
sowing weeks before it is seed in cold wet ground. Only the early side is ever flagged.

Records are keyed to the CELL (crop x zone), not to an arm index: measured against this roster,
arms align positionally with resolved window segments only 51% of the time, so an index-based
write would silently attach half its verdicts to the wrong window.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plant_windows as PW  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
ZONE_TABLE = os.path.join(REPO, 'tools', 'staging', 'uscrn', 'zone_table.json')

SPRING_MONTHS = (1, 6)     # a sowing window opening in Jan-Jun is the spring arm
ALIGNED_DAYS = 3
DRIFT_DAYS = 10
SOIL_ANCHOR_RE = re.compile(r'^soil_temp_(\d+)f$')


def _doy(month, day):
    return datetime.date(2001, month, day).timetuple().tm_yday


def _mmdd(month, day):
    return '%02d-%02d' % (month, day)


def spring_sow_window(window_string):
    """Earliest spring segment -> ((start_month, start_day), (end_month, end_day)), else None.

    Not "the first segment": a mild-zone cell stores its fall arm first (lettuce zone 8 reads
    'Sep 23 - Nov 7, Feb 1 - Feb 22'), and reading position 0 there compares a September date
    against an April soil crossing.
    """
    best = None
    for sp in PW.spans(window_string):
        if not (SPRING_MONTHS[0] <= sp.start_month <= SPRING_MONTHS[1]):
            continue
        start = (sp.start_month, sp.start_day or 1)
        end = (sp.end_month, sp.end_day or _month_end(sp.end_month))
        if _doy(*end) < _doy(*start):        # a span that wraps the year end is not a spring arm
            continue
        if best is None or _doy(*start) < _doy(*best[0]):
            best = (start, end)
    return best


def _month_end(month):
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]


def spring_sow_date(window_string):
    """The spring window's opening date, or None. Kept as the `stored_date` of the record."""
    w = spring_sow_window(window_string)
    return w[0] if w else None


def crop_threshold(crop, arm, ladder=None):
    """(threshold_f, provenance) for this arm, or (None, None) if the crop cannot supply one."""
    m = SOIL_ANCHOR_RE.match(str((arm or {}).get('from') or ''))
    if m:
        thr = int(m.group(1))
        prov = 'declared on the planting arm as %s' % arm['from']
    else:
        g = crop.get('germination_temp_f')
        if not (isinstance(g, list) and len(g) == 2 and isinstance(g[0], (int, float))):
            return None, None
        thr = int(g[0])
        prov = 'germination_temp_f floor for this crop'
    if ladder is not None and str(thr) not in ladder:
        return None, None
    return thr, prov


def classify_offset(offset_days):
    """The Phase 1.1 magnitude bands, retained as a reported figure -- NOT as the verdict.

    MEASURED 2026-08-04, which is why they are not the verdict: across the 480 comparable cells
    the offset runs p10 -33 days to p90 +59, and even the 29 cells whose arm DECLARES its own soil
    anchor land 16/29 outside 10 days. That is not a roster full of defects. A zone's own
    year-to-year crossing spread is 30 to 90 days (p10 to p90), so a fixed 3-day band is finer
    than the thing being measured and reports the variance as error. The bands were specified for
    a comparison against a single station, not against a zone aggregate. `position` below is the
    scale-free reading that survives.
    """
    a = abs(offset_days)
    if a <= ALIGNED_DAYS:
        return 'aligned'
    return 'drift' if a <= DRIFT_DAYS else 'misaligned'


def position(window, stats):
    """Where the measured soil crossing falls relative to the stored sowing WINDOW.

    Comparing the window's OPENING against the median crossing is the wrong test and was the
    first thing built here: a sowing window is a range a gardener picks a day inside, so its
    opening sits before the typical crossing almost by construction. Measured on this roster that
    read returned 67 cells "often too cold" that are nothing of the sort. The question guidance
    actually has to answer is whether a gardener who follows the window lands on warm soil:

      window_too_early  -- the window CLOSES before even the p10 crossing. Follow this cell and
                           in more than nine years in ten every day of the window is cold soil.
                           This is the real defect shape, and it is what caught the desert
                           cucurbits sown on the last-frost date.
      opens_early       -- the window closes after p10 but before the median: the late part of
                           the window works in some years, the opening rarely does.
      brackets_crossing -- the window contains the median crossing. This is the healthy shape.
      opens_late        -- the window opens after the p90 crossing. Not a defect: soil was ready
                           well before, and sowing late is a choice. Reported, never flagged.
    """
    if stats.get('year_round'):
        return 'not_soil_limited'
    (start, end) = window
    s, e = _doy(*start), _doy(*end)

    def d(key):
        v = stats.get(key)
        return _doy(int(v[:2]), int(v[3:])) if v else None
    p10, p50, p90 = d('p10_date'), d('median_date'), d('p90_date')
    if p10 is not None and e < p10:
        return 'window_too_early'
    if p50 is not None and e < p50:
        return 'opens_early'
    if p90 is not None and s > p90:
        return 'opens_late'
    return 'brackets_crossing'


RISK_FOR = {'window_too_early': 'high', 'opens_early': 'moderate'}


def risk_level(window, stats):
    """Directional reading: does this window run ahead of the soil in this zone?"""
    return RISK_FOR.get(position(window, stats))


def build_record(crop, arm, zone, window_string, zone_stats):
    """One `uscrn_validation` record for a (crop, zone) cell, or None when nothing is comparable."""
    thr, prov = crop_threshold(crop, arm, ladder=zone_stats)
    if thr is None:
        return None
    stats = zone_stats.get(str(thr))
    if not stats or not stats.get('median_date'):
        return None
    win = spring_sow_window(window_string)
    if win is None:
        return None
    stored = win[0]

    med = stats['median_date']
    offset = _doy(*stored) - _doy(int(med[:2]), int(med[3:]))
    conf = stats.get('confidence')

    pos = position(win, stats)
    status = 'flagged_for_review' if conf in ('insufficient', 'unreliable') else pos

    note = None
    if stats.get('year_round'):
        note = ('soil at 5cm is already at or above %dF when the year opens in %d%% of watched '
                'years here, so this sowing date is not gated by soil temperature'
                % (thr, round(100 * stats['already_above_rate'])))
    elif conf == 'insufficient':
        note = ('station-years %d below the 30 confidence floor; the comparison is reported but '
                'should not be auto-applied' % stats['station_year_count'])
    elif conf == 'unreliable':
        note = ('%dF is not reached at 5cm in %d%% of watched station-years in this zone, so the '
                'median crossing describes the warm years only'
                % (thr, round(100 * stats['never_rate'])))
    elif stats.get('single_station'):
        note = 'zone summarized from a single USCRN station'

    return {
        'status': status,
        'position': pos,
        'offset_band': classify_offset(offset),
        'risk': RISK_FOR.get(pos),
        'stored_date': _mmdd(*stored),
        'stored_window_end': _mmdd(*win[1]),
        'uscrn_median_date': med,
        'uscrn_p10_date': stats['p10_date'],
        'uscrn_p90_date': stats['p90_date'],
        'offset_days_median': offset,
        'spread_days_p10_p90': stats['spread_days_p10_p90'],
        'station_count': stats['station_count'],
        'station_year_count': stats['station_year_count'],
        'years_covered': '2010-2025',
        'anchor_threshold': 'soil %dF reached at 5cm' % thr,
        'anchor_threshold_basis': prov,
        # NOT `zone_coverage_note_seasoned`, though the pilot used that name when it had
        # something to say. The `_seasoned` suffix is a CONTRACT, not a label: whole_crop_gate A29
        # (register_fill_gate) requires every `_seasoned`/`_beginner` field to be authored prose
        # with a register twin, and it bounced 34 of 121 certified crops when these were written
        # under that name. These are machine-generated methodology annotations on a field that
        # renders nowhere, not the expert half of a dual-register consumer pair.
        'zone_coverage_note': note,
        'source_id': 'uscrn',
        'zone_citations': [],
    }


# ------------------------------------------------------------------ roster walk

def cells(data, table):
    """Yield (crop, container_kind, container_id, zone, arm, window_string, target_path).

    `target_path` locates the single arm the record is written to: plantings[0].direct_sow[0] of
    the cell, which is where the existing pilot records sit.
    """
    for ci, crop in enumerate(data['crops']):
        if crop.get('propagule') != 'seed':
            continue
        for zone, node in sorted((crop.get('zones') or {}).items()):
            arms = (node.get('plantings') or [{}])[0].get('direct_sow') or []
            if not arms or 'uscrn_validation' not in arms[0]:
                continue
            yield (crop, 'zones', zone, zone, arms[0], node.get('direct_sow'),
                   (ci, 'zones', zone))
        for rid, region in sorted((crop.get('regions') or {}).items()):
            arms = (region.get('plantings') or [{}])[0].get('direct_sow') or []
            if not arms or 'uscrn_validation' not in arms[0]:
                continue
            for zone, rnode in sorted((region.get('resolved_by_zone') or {}).items()):
                yield (crop, 'regions', rid, zone, arms[0],
                       rnode.get('direct_sow') or rnode.get('plant_out'), (ci, 'regions', rid))


def build_all(data, table):
    """-> ({target_path_key: record}, skipped Counter). Region cells carry a per-zone breakdown."""
    per_target = collections.defaultdict(dict)
    skipped = collections.Counter()
    for crop, kind, cid, zone, arm, window, target in cells(data, table):
        zt = table.get(str(zone))
        if not zt:
            skipped['zone %s not covered by USCRN' % zone] += 1
            continue
        rec = build_record(crop, arm, zone, window, zt)
        if rec is None:
            skipped['no comparable spring sowing / threshold'] += 1
            continue
        per_target['%d|%s|%s' % target][str(zone)] = rec
    return per_target, skipped


def summarize(by_zone):
    """Collapse a region's per-zone records into one record carrying the breakdown."""
    zones = sorted(by_zone, key=int)
    if len(zones) == 1:
        rec = dict(by_zone[zones[0]])
        rec['zone_scope'] = zones[0]
        # named in BOTH branches: a consumer (and the promote's re-derivation guard) must be able
        # to ask "which zone are these scalars about" without first checking how many there were
        rec['representative_zone'] = zones[0]
        return rec
    # EVERY scalar comes from ONE representative zone -- the median-offset one -- so the record
    # cannot contradict itself. Taking `stored_date` from the worst zone while reporting the
    # median offset produces a record whose own numbers do not subtract to its own verdict.
    rep = sorted(zones, key=lambda z: by_zone[z]['offset_days_median'])[len(zones) // 2]
    base = dict(by_zone[rep])
    risks = [by_zone[z]['risk'] for z in zones]
    risk = 'high' if 'high' in risks else ('moderate' if 'moderate' in risks else None)
    base.update({
        'risk': risk,
        'zone_scope': '%s-%s' % (zones[0], zones[-1]),
        'representative_zone': rep,
        'by_zone': {z: {k: by_zone[z][k] for k in
                        ('status', 'risk', 'stored_date', 'uscrn_median_date',
                         'offset_days_median', 'station_year_count')} for z in zones},
    })
    off_zones = [z for z in zones if by_zone[z]['status'] in ('drift', 'misaligned')]
    if off_zones:
        base['zone_coverage_note'] = (
            'zones %s sit outside the aligned band; see by_zone for the per-zone comparison'
            % ', '.join(off_zones))
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--canonical', default=CANON)
    ap.add_argument('--table', default=ZONE_TABLE)
    ap.add_argument('--json', help='write the records here for the promote step')
    args = ap.parse_args()

    data = json.load(open(args.canonical, encoding='utf-8'))
    table = json.load(open(args.table, encoding='utf-8'))['zones']
    per_target, skipped = build_all(data, table)

    out, status_counts, risk_counts = {}, collections.Counter(), collections.Counter()
    for key, by_zone in per_target.items():
        rec = summarize(by_zone)
        out[key] = rec
        status_counts[rec['status']] += 1
        risk_counts[rec['risk'] or 'none'] += 1

    print('USCRN spring-sowing validation -- direct_sow arms, seed-propagated crops')
    print('=' * 92)
    print('records built            : %d' % len(out))
    print('  by status              : %s' % dict(status_counts.most_common()))
    print('  by directional risk    : %s' % dict(risk_counts.most_common()))
    print('cells skipped            : %s' % dict(skipped.most_common()))
    print()
    flagged = [(k, r) for k, r in out.items() if r['risk'] in ('high', 'moderate')]
    print('DIRECTIONAL RISK -- stored sowing date runs ahead of the measured soil record (%d)'
          % len(flagged))
    print('-' * 92)
    ci_name = {i: c['slug'] for i, c in enumerate(data['crops'])}
    for k, r in sorted(flagged, key=lambda kv: (kv[1]['risk'] != 'high',
                                                kv[1]['offset_days_median'])):
        ci, kind, cid = k.split('|')
        print('  %-5s %-22s %-14s z%-5s stored %s  median %s  off %+4d  %s'
              % (r['risk'], ci_name[int(ci)], cid, r.get('zone_scope', ''),
                 r['stored_date'], r['uscrn_median_date'], r['offset_days_median'],
                 r['anchor_threshold']))
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(out, fh, indent=1)
        print('\nwrote %s' % args.json)
    return 0


if __name__ == '__main__':
    sys.exit(main())
