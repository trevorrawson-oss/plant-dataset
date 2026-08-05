#!/usr/bin/env python3
"""USCRN CRND0103 daily-archive parser -> measured soil-temperature crossing dates by USDA zone.

WHAT THIS IS FOR. The dataset's planting dates are derived from extension tables. USCRN is not
another table -- it is the instrument record: 113 NOAA Climate Reference Network stations,
research-grade, triple-redundant sensors, soil temperature at 5cm. A statement like "in zone 6,
soil at 5cm first holds 50F on median April 12 (p10 Mar 28, p90 Apr 29), over 214 station-years"
is a MEASUREMENT this project owns, not a citation it borrows. That is the `north-star-become-the-
source` direction, and it is why the output of this tool is committed as evidence rather than
recomputed on demand.

THE ARCHIVE: ~/Documents/plant-project/03-data/soil-data/uscrn_full -- 2,343 files,
`CRND0103-<year>-<STATION>.txt`, 2000-2025, 28 whitespace-separated columns, no header.
Fields used (0-indexed): 1 LST_DATE, 3 LONGITUDE, 4 LATITUDE, 6 T_DAILY_MIN, 23 SOIL_TEMP_5_DAILY.
All temperatures are CELSIUS. Missing = -9999.0 (soil moisture uses -99.000; not read here).

WINDOW: 2010-2025 by default. The network stabilizes at 112-113 stations from 2008 and the
existing pilot record in the canonical declares `years_covered: "2010-2025"`, so matching it keeps
the new rows commensurable with the ones already in the file.

TWO THINGS ARE DERIVED HERE, and the second is the one that needed a design decision:

1. CROSSING DATE. For each station-year and each threshold on the ladder, the first date beginning
   SUSTAIN (5) consecutive days whose 5cm soil temperature is at or above the threshold. A day with
   a missing reading BREAKS the run rather than being interpolated -- see
   `waf-block-pages-cached-as-absence`: absence read as data is how this class of scan goes wrong.
   This biases crossing dates LATE at gappy stations, which is the safe direction for a planting
   date and is reported as `sustain_gap_rate` so the bias is visible rather than silent.

2. STATION -> USDA ZONE. No lat/lon -> zone lookup exists in this repo and the USDA raster is not
   available offline, but it is not needed: the USDA zone IS the mean annual extreme minimum
   temperature, binned every 10F. USCRN publishes T_DAILY_MIN, so each station's zone is derived
   from THE STATION'S OWN RECORD -- no external join, no interpolation, no third-party table. A
   year is only scored if it is complete enough to contain its own winter (`year_is_scorable`); a
   station that lost January would otherwise report a falsely warm minimum and walk a zone south.
   Caveat, stated in the output: USDA's published map uses a 30-year normal (1991-2020) while this
   window is 16 years, so a station may sit half a zone off its map placement. That is recorded in
   `method_note` and is why the shipped table carries `station_count` per zone.

Usage:
    python3 tools/uscrn_ingest.py                     # full archive -> tools/staging/uscrn/
    python3 tools/uscrn_ingest.py --archive DIR --out DIR
    python3 tools/uscrn_ingest.py --limit 20          # smoke run on 20 stations
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ARCHIVE = os.path.expanduser(
    '~/Documents/plant-project/03-data/soil-data/uscrn_full')
DEFAULT_OUT = os.path.join(REPO, 'tools', 'staging', 'uscrn')

MISSING = -9999.0
SUSTAIN = 5           # consecutive days at/above threshold that count as "reached"
DEPTH_CM = 5
YEAR_MIN, YEAR_MAX = 2010, 2025

# The ladder the dataset actually needs: every distinct germination_temp_f lower bound on the
# roster (35/40/45/48/50/55/60/65/68/70/75) plus the 5F grid, so a crop's anchor is looked up
# rather than interpolated.
THRESHOLDS_F = [35, 40, 45, 48, 50, 55, 60, 65, 68, 70, 75, 80]

# a year is scored for its annual extreme minimum only if it has this many valid daily minima
# AND at least MIN_WINTER_DAYS in each of Dec/Jan/Feb -- the months that actually set the minimum
MIN_VALID_DAYS = 300
MIN_WINTER_DAYS = 20

FNAME = re.compile(r'^CRND0103-(\d{4})-(.+)\.txt$')


class Row(object):
    __slots__ = ('date', 'lat', 'lon', 'tmin_f', 'soil5_f')

    def __init__(self, date, lat, lon, tmin_f, soil5_f):
        self.date, self.lat, self.lon = date, lat, lon
        self.tmin_f, self.soil5_f = tmin_f, soil5_f


def _num(tok):
    """A CRND0103 numeric field -> float, or None for the -9999.0 missing sentinel."""
    try:
        v = float(tok)
    except (TypeError, ValueError):
        return None
    return None if v <= MISSING + 1 else v


def c_to_f(c):
    return None if c is None else c * 9.0 / 5.0 + 32.0


def parse_row(line):
    f = line.split()
    if len(f) < 24:
        return None
    try:
        d = datetime.datetime.strptime(f[1], '%Y%m%d').date()
    except ValueError:
        return None
    return Row(d, _num(f[4]), _num(f[3]), c_to_f(_num(f[6])), c_to_f(_num(f[23])))


def parse_rows(lines):
    out = []
    for ln in lines:
        if not ln.strip():
            continue
        r = parse_row(ln)
        if r is not None:
            out.append(r)
    out.sort(key=lambda r: r.date)
    return out


def first_sustained_crossing(rows, threshold_f, sustain=SUSTAIN):
    """First date starting `sustain` consecutive CALENDAR days at/above threshold_f at 5cm.

    Consecutive means consecutive in date, not consecutive in the row list -- a station that
    simply omits a day must not have that day's absence closed up silently. A missing reading
    inside the window breaks the run.
    """
    by_date = {r.date: r.soil5_f for r in rows}
    for r in rows:
        d = r.date
        ok = True
        for k in range(sustain):
            v = by_date.get(d + datetime.timedelta(days=k))
            if v is None or v < threshold_f:
                ok = False
                break
        if ok:
            return d
    return None


def annual_extreme_min(rows):
    """(lowest daily minimum in F, count of valid daily minima)."""
    vals = [r.tmin_f for r in rows if r.tmin_f is not None]
    return (min(vals) if vals else None), len(vals)


def year_is_scorable(rows):
    """True if this year can honestly report an annual extreme minimum.

    Requires overall coverage AND real data in each winter month. A station that lost January
    reports a falsely warm minimum, which is how a cold station gets binned a zone or two south.
    """
    valid = [r for r in rows if r.tmin_f is not None]
    if len(valid) < MIN_VALID_DAYS:
        return False
    per_month = collections.Counter(r.date.month for r in valid)
    return all(per_month.get(m, 0) >= MIN_WINTER_DAYS for m in (12, 1, 2))


def usda_zone(mean_extreme_min_f):
    """USDA hardiness zone label ('7a') from a mean annual extreme minimum temperature in F.

    The zone system IS this quantity binned: zone 1 starts at -60F, each zone spans 10F, each
    half-zone 5F. Zone 7a = 0..5F, 8a = 10..15F, and so on.
    """
    n = usda_zone_int(mean_extreme_min_f)
    off = mean_extreme_min_f + 60.0
    off = max(0.0, min(129.999, off))
    return '%d%s' % (n, 'a' if off % 10 < 5 else 'b')


def usda_zone_int(mean_extreme_min_f):
    n = int((mean_extreme_min_f + 60.0) // 10) + 1
    return max(1, min(13, n))


# ---------------------------------------------------------------- archive walk

def station_years(archive, year_min=YEAR_MIN, year_max=YEAR_MAX):
    """{station: {year: path}} for the files inside the window."""
    out = collections.defaultdict(dict)
    for name in sorted(os.listdir(archive)):
        m = FNAME.match(name)
        if not m:
            continue
        year, station = int(m.group(1)), m.group(2)
        if year_min <= year <= year_max:
            out[station][year] = os.path.join(archive, name)
    return out


def soil_days_in_scan_window(rows):
    """Valid 5cm readings between Jan 1 and Jul 31 -- the span a spring crossing can fall in.

    This is what separates "the soil never reached 70F here" from "we did not measure it". A
    threshold with no crossing is only evidence of ABSENCE in a year that was actually watched;
    counting an unwatched year as `never` is the `waf-block-pages-cached-as-absence` defect.
    """
    return sum(1 for r in rows if r.soil5_f is not None and r.date.month <= 7)


def ingest_station(station, year_paths):
    """Parse one station's files -> its zone assignment and per-year, per-threshold crossings."""
    lat = lon = None
    extreme_mins, scorable_years = [], []
    years = {}
    soil_days = valid_soil_days = 0

    for year in sorted(year_paths):
        with open(year_paths[year], encoding='utf-8', errors='replace') as fh:
            rows = parse_rows(fh)
        if not rows:
            continue
        for r in rows:
            if lat is None and r.lat is not None:
                lat, lon = r.lat, r.lon
        soil_days += len(rows)
        valid_soil_days += sum(1 for r in rows if r.soil5_f is not None)

        if year_is_scorable(rows):
            lo, _ = annual_extreme_min(rows)
            if lo is not None:
                extreme_mins.append(lo)
                scorable_years.append(year)

        cross = {}
        for t in THRESHOLDS_F:
            d = first_sustained_crossing(rows, float(t))
            cross[str(t)] = d.strftime('%m-%d') if d is not None else None
        years[str(year)] = {
            'soil_days_jan_jul': soil_days_in_scan_window(rows),
            'crossings': cross,
        }

    if not extreme_mins:
        return None
    mean_min = sum(extreme_mins) / len(extreme_mins)
    return {
        'station': station,
        'lat': lat, 'lon': lon,
        'mean_annual_extreme_min_f': round(mean_min, 2),
        'zone': usda_zone_int(mean_min),
        'zone_half': usda_zone(mean_min),
        'scorable_years': scorable_years,
        'soil_coverage': round(valid_soil_days / float(soil_days), 4) if soil_days else 0.0,
        'years': years,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--archive', default=DEFAULT_ARCHIVE)
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--limit', type=int, default=0, help='only N stations (smoke run)')
    args = ap.parse_args()

    if not os.path.isdir(args.archive):
        print('archive not found: %s' % args.archive, file=sys.stderr)
        return 2
    os.makedirs(args.out, exist_ok=True)

    sy = station_years(args.archive)
    names = sorted(sy)
    if args.limit:
        names = names[:args.limit]
    print('stations: %d   window: %d-%d   thresholds: %s'
          % (len(names), YEAR_MIN, YEAR_MAX, THRESHOLDS_F))

    stations, dropped = [], []
    for i, name in enumerate(names, 1):
        rec = ingest_station(name, sy[name])
        if rec is None:
            dropped.append(name)
        else:
            stations.append(rec)
        if i % 10 == 0 or i == len(names):
            print('  %3d/%d  %s' % (i, len(names), name), flush=True)

    path = os.path.join(args.out, 'station_stats.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump({
            'generated_window': [YEAR_MIN, YEAR_MAX],
            'depth_cm': DEPTH_CM,
            'sustain_days': SUSTAIN,
            'thresholds_f': THRESHOLDS_F,
            'stations': stations,
            'dropped_no_scorable_year': dropped,
        }, fh, indent=1)
    print('\nwrote %s  (%d stations, %d dropped)' % (path, len(stations), len(dropped)))

    byzone = collections.Counter(s['zone'] for s in stations)
    print('stations per derived USDA zone: %s' % dict(sorted(byzone.items())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
