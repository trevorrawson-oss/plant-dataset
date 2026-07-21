#!/usr/bin/env python3
"""Prose-vs-resolved date-window honesty sweep for the mid_south cells.

For every cell: collect the day-level date windows the cell ACTUALLY resolves to (plant_out,
start_indoors, harvest, harvest_start/end, second_planting.*, bloom, and the frost anchors as
single dates), across BOTH zones. Then scan every prose field for explicit "Mon D <sep> Mon D"
ranges and "Mon D" single dates, and flag any that match NO resolved window/anchor within a small
tolerance. This catches the onion/leek/garlic defect class (prose asserting a window the cell does
not carry) that gates cannot see. Flags are candidates for review, not auto-fixes (some are benign
rounding or a legitimately-derived harvest month).
"""
import json
import os
import re

STAGING = "/Users/trevorrawson/plant-dataset/tools/staging"
FILES = ["mid_south_annuals_cool.json", "mid_south_annuals_warm.json",
         "mid_south_trees.json", "mid_south_citrus.json", "mid_south_perennials.json"]
MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
TOL = 4  # days; catches the 5-day onion/leek mismatch, tolerates 1-4 day rounding

PROSE_KEYS = re.compile(r"region_notes|_note$|_notes$|basis_|chill_basis|synthesis|"
                        r"suitability_note|type_note|grown_as_note|frost_risk_note|"
                        r"day_length_note|zone_notes|^notes$|cold_basis")
RANGE_RE = re.compile(r"\b([A-Z][a-z]{2})\s+(\d{1,2})\s*(?:to|through|-|–|—)\s*"
                      r"([A-Z][a-z]{2})\s+(\d{1,2})\b")
SINGLE_RE = re.compile(r"\b([A-Z][a-z]{2})\s+(\d{1,2})\b")


def doy(mon, day):
    if mon not in MON:
        return None
    return CUM[MON[mon] - 1] + int(day)


def _spans(s):
    """Parse a resolved window string into a list of (start_doy, end_doy). Handles 'Mon D - Mon D',
    comma-joined reflush, and single 'Mon D'."""
    out = []
    if not isinstance(s, str):
        return out
    for chunk in s.split(","):
        m = re.findall(r"([A-Z][a-z]{2})\s+(\d{1,2})", chunk)
        if len(m) >= 2:
            a, b = doy(*m[0]), doy(*m[-1])
            if a and b:
                out.append((a, b))
        elif len(m) == 1:
            a = doy(*m[0])
            if a:
                out.append((a, a))
    return out


def resolved_windows(cell):
    """All day-level (start,end) windows + single anchor dates for a cell, both zones."""
    wins, singles = [], set()
    for z, zc in (cell.get("resolved_by_zone") or {}).items():
        if not isinstance(zc, dict):
            continue
        for k in ("plant_out", "start_indoors", "harvest", "bloom"):
            wins += _spans(zc.get(k))
        hs, he = zc.get("harvest_start"), zc.get("harvest_end")
        if hs and he:
            wins += _spans(f"{hs} - {he}")
        sp = zc.get("second_planting") or {}
        for k in ("plant_out", "start_indoors"):
            wins += _spans(sp.get(k))
        if sp.get("harvest_start") and sp.get("harvest_end"):
            wins += _spans(f"{sp['harvest_start']} - {sp['harvest_end']}")
        rf = zc.get("resolved_from") or {}
        for k in ("last_frost", "first_frost"):
            d = _spans(rf.get(k))
            if d:
                singles.add(d[0][0])
    # every window endpoint is also a valid single date to match against
    for a, b in wins:
        singles.add(a)
        singles.add(b)
    return wins, singles


def near_window(p, wins):
    return any(abs(p[0] - a) <= TOL and abs(p[1] - b) <= TOL for a, b in wins)


def near_single(d, singles):
    return any(abs(d - s) <= TOL for s in singles)


def prose_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and PROSE_KEYS.search(k):
                yield path + "." + k, v
            else:
                yield from prose_strings(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from prose_strings(v, f"{path}[{i}]")


def main():
    flags = []
    for f in FILES:
        data = json.load(open(os.path.join(STAGING, f), encoding="utf-8"))
        for slug, cell in data.items():
            wins, singles = resolved_windows(cell)
            for fld, text in prose_strings(cell):
                consumed = []
                for m in RANGE_RE.finditer(text):
                    p = (doy(m.group(1), m.group(2)), doy(m.group(3), m.group(4)))
                    if p[0] and p[1]:
                        consumed.append((m.start(), m.end()))
                        if not near_window(p, wins):
                            flags.append((slug, fld.lstrip("."), m.group(0),
                                          _nearest(p, wins)))
                # single dates NOT already inside a matched range
                for m in SINGLE_RE.finditer(text):
                    if any(a <= m.start() < b for a, b in consumed):
                        continue
                    d = doy(m.group(1), m.group(2))
                    if d and not near_single(d, singles):
                        flags.append((slug, fld.lstrip("."), m.group(0) + " (single)",
                                      f"nearest anchor/endpoint off by >{TOL}d"))
    print(f"=== {len(flags)} prose date mention(s) with no matching resolved window (TOL={TOL}d) ===\n")
    for slug, fld, mention, near in flags:
        print(f"  {slug:22} {fld:55} {mention!r:28} | {near}")
    return flags


def _nearest(p, wins):
    if not wins:
        return "no resolved windows"
    best = min(wins, key=lambda w: abs(p[0] - w[0]) + abs(p[1] - w[1]))
    return f"nearest resolved {_fmt(best[0])}-{_fmt(best[1])}"


def _fmt(d):
    m = 0
    while m < 11 and CUM[m + 1] < d:
        m += 1
    inv = {i: mon for mon, i in MON.items()}
    return f"{inv[m + 1]} {d - CUM[m]}"


if __name__ == "__main__":
    main()
