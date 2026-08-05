#!/usr/bin/env python3
"""Aggregate USCRN station-years into per-USDA-zone soil-temperature crossing statistics.

INPUT   tools/staging/uscrn/station_stats.json   (from tools/uscrn_ingest.py)
OUTPUT  tools/staging/uscrn/zone_table.json      (+ a human-readable report on stdout)

This is the artifact that makes the project a SOURCE rather than a deriver: for each USDA zone
and each threshold on the ladder, the measured distribution of the date 5cm soil temperature
first holds that threshold for 5 consecutive days, over 2010-2025.

FOUR THINGS THIS REFUSES TO DO, each of which would put a confident wrong date in the canonical:

  1. Count an UNWATCHED year as "the soil never got there." A station-year only counts if it has
     MIN_SCAN_DAYS valid 5cm readings in Jan-Jul. Absence of observation is not observation of
     absence.
  2. Publish a median over only the years that crossed, when most years did not. A threshold
     missed in more than NEVER_MAX of watched years is marked `unreliable` -- its median describes
     the warm tail, not the zone.
  3. Hide thin coverage. `station_count`, `station_year_count`, `single_station` and `confidence`
     ride with every record, so a consumer can never mistake 1 station-year for 300.
  4. Report warm-zone SATURATION as a spring event. Where soil sits above the threshold through
     the winter, every year "crosses" on Jan 1 and a median of "01-01" would read as a planting
     signal. Those records carry `year_round: true` and are meant to be read as "this threshold
     is not a seasonal gate in this zone", not as a date.

A zone with no USCRN station is ABSENT from the table. It is never emitted as an empty record.
"""
import argparse
import collections
import datetime
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING = os.path.join(REPO, 'tools', 'staging', 'uscrn')

MIN_SCAN_DAYS = 120        # valid 5cm readings in Jan-Jul for a station-year to be watched
MIN_STATION_YEARS = 30     # the pilot's own confidence floor, kept
NEVER_MAX = 0.25           # above this share of watched-but-uncrossed years, no median is honest
# At/above this share of crossings landing on Jan 1, the threshold is not a seasonal gate in the
# zone -- the soil is already there when the year opens. Measured: zone 8 is 67% already-above at
# 40F, zone 9 79%. A "median crossing date" for those is an artifact of where the calendar starts,
# not a spring event, and must not be read as a planting signal.
YEAR_ROUND_RATE = 0.50


def _doy(mmdd):
    """MM-DD -> day-of-year on a NON-leap reference year, folding Feb 29 onto Feb 28.

    The dataset stores month-day strings with no year, so an emitted '02-29' would be a date
    that does not exist in three years out of four. A leap-day crossing is ~1 station-year in
    1,460 and folding it back one day is far inside the spread of any of these distributions.
    """
    if mmdd == '02-29':
        mmdd = '02-28'
    return datetime.datetime.strptime('2001-' + mmdd, '%Y-%m-%d').date().timetuple().tm_yday


def _mmdd(doy):
    return (datetime.date(2001, 1, 1) + datetime.timedelta(days=doy - 1)).strftime('%m-%d')


def percentile(sorted_vals, q):
    """Nearest-rank percentile over a sorted list (no interpolation between observed years)."""
    if not sorted_vals:
        return None
    k = max(0, min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[k]


def build_zone_table(stations, min_scan_days=MIN_SCAN_DAYS,
                     min_station_years=MIN_STATION_YEARS):
    """[station_stats records] -> {zone: {threshold: stats}}."""
    # zone -> threshold -> {'doys': [...], 'never': n, 'stations': set()}
    acc = collections.defaultdict(lambda: collections.defaultdict(
        lambda: {'doys': [], 'never': 0, 'stations': set()}))

    for st in stations:
        zone = str(st['zone'])
        for year, yrec in (st.get('years') or {}).items():
            if yrec.get('soil_days_jan_jul', 0) < min_scan_days:
                continue                      # unwatched: contributes nothing, in either direction
            for thr, mmdd in (yrec.get('crossings') or {}).items():
                bucket = acc[zone][thr]
                bucket['stations'].add(st['station'])
                if mmdd is None:
                    bucket['never'] += 1
                else:
                    bucket['doys'].append(_doy(mmdd))

    table = {}
    for zone in sorted(acc, key=int):
        table[zone] = {}
        for thr in sorted(acc[zone], key=int):
            b = acc[zone][thr]
            doys = sorted(b['doys'])
            watched = len(doys) + b['never']
            if watched == 0:
                continue
            never_rate = b['never'] / float(watched)
            already = sum(1 for d in doys if d == 1)
            already_rate = already / float(len(doys)) if doys else 0.0
            p10, p50, p90 = (percentile(doys, 0.10), percentile(doys, 0.50),
                             percentile(doys, 0.90))

            if never_rate > NEVER_MAX:
                conf = 'unreliable'
            elif watched < min_station_years:
                conf = 'insufficient'
            else:
                conf = 'high'

            table[zone][thr] = {
                'median_date': _mmdd(p50) if p50 else None,
                'p10_date': _mmdd(p10) if p10 else None,
                'p90_date': _mmdd(p90) if p90 else None,
                'spread_days_p10_p90': (p90 - p10) if (p10 and p90) else None,
                'station_count': len(b['stations']),
                'station_year_count': watched,
                'crossed_count': len(doys),
                'never_count': b['never'],
                'never_rate': round(never_rate, 4),
                'already_above_rate': round(already_rate, 4),
                'year_round': bool(doys) and already_rate >= YEAR_ROUND_RATE,
                'single_station': len(b['stations']) == 1,
                'confidence': conf,
            }
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stats', default=os.path.join(STAGING, 'station_stats.json'))
    ap.add_argument('--out', default=os.path.join(STAGING, 'zone_table.json'))
    ap.add_argument('--threshold', default='50', help='threshold to print in the report')
    args = ap.parse_args()

    with open(args.stats, encoding='utf-8') as fh:
        stats = json.load(fh)
    table = build_zone_table(stats['stations'])

    payload = {
        'method': {
            'source': 'NOAA U.S. Climate Reference Network, daily CRND0103',
            'window': stats['generated_window'],
            'depth_cm': stats['depth_cm'],
            'sustain_days': stats['sustain_days'],
            'thresholds_f': stats['thresholds_f'],
            'zone_assignment': ('each station binned to a USDA zone by the mean of its own '
                                'annual extreme minimum air temperature over the window; USDA '
                                'zones are that quantity binned in 10F steps from -60F'),
            'caveats': [
                'the USDA published map uses a 30-year normal (1991-2020); this window is 16 '
                'years, so a station may sit a half zone off its map placement',
                'a missing daily reading breaks the sustain run rather than being interpolated, '
                'which biases crossing dates late at gappy stations',
                'zones with no USCRN station are absent from this table',
            ],
        },
        'zones': table,
    }
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1)

    thr = args.threshold
    print('USCRN 5cm soil temperature: first %sF sustained %d days, by USDA zone (%d-%d)'
          % (thr, stats['sustain_days'], *stats['generated_window']))
    print('=' * 104)
    print('%-5s %-9s %-9s %-9s %6s %6s %7s %7s %7s  %s'
          % ('zone', 'p10', 'median', 'p90', 'spread', 'stns', 'stn-yrs', 'never', 'yr-round',
             'confidence'))
    print('-' * 104)
    for zone in sorted(table, key=int):
        r = table[zone].get(thr)
        if not r:
            continue
        print('%-5s %-9s %-9s %-9s %6s %6d %7d %7s %7s  %s'
              % (zone, r['p10_date'] or '-', r['median_date'] or '-', r['p90_date'] or '-',
                 r['spread_days_p10_p90'] if r['spread_days_p10_p90'] is not None else '-',
                 r['station_count'], r['station_year_count'],
                 '%.0f%%' % (100 * r['never_rate']), 'yes' if r['year_round'] else '-',
                 r['confidence'] + (' SINGLE-STATION' if r['single_station'] else '')))
    print('-' * 104)
    print('wrote %s' % args.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
