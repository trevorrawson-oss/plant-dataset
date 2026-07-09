#!/usr/bin/env python3
"""second_planting_gate.py -- A43: the de-mux invariant (spec 2026-07-09 §6).

Rule B (wired at Stage-1 close) -- NO UNSTRUCTURED COMMA SHAPE: on a crop with
succession_policy.suitable != True, a resolved cell with >= 2 comma-joined window
spans in start_indoors or plant_out and NO second_planting is a violation. This is
what blocks new crops from re-introducing the old shape. Doubling in `harvest`
alone is legitimate (reflush = two flushes of ONE planting: cayenne/habanero/
jalapeno hot cells, chives/mint); " or "-joined alternatives count once (woody-herb
establishment shape, or-normalized alliums/chard).

Rule A (wired at Stage-3 close) -- DEDUP INVARIANT: a cell WITH second_planting
must be single-span in start_indoors/plant_out/harvest, and its envelope must sit
INSIDE the primary windows: harvest_end must parse inside the FIRST harvest span,
last_plant_date inside the FIRST plant_out span (containment, not fall-value
equality, so a legitimately shared harvest window -- fava -- passes while an
envelope left spanning the fall cycle fires). (A targeted floor for the two real
envelope defect classes, not a general date audit.)

check_crop(crop, rules) -> [violation strings]. Standalone CLI for fixtures +
roster sweeps: python3 tools/second_planting_gate.py [crops.json] [--rules AB]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plant_windows import spans, window_count, single_date, in_span

PLANTING_FIELDS = ("start_indoors", "plant_out")
ALL_FIELDS = ("start_indoors", "plant_out", "harvest")


def _cells(crop):
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if isinstance(cell, dict):
                yield rk, z, cell


def check_crop(crop, rules=frozenset("AB")):
    v = []
    slug = crop.get("slug", "?")
    suitable = (crop.get("succession_policy") or {}).get("suitable")
    for rk, z, cell in _cells(crop):
        sp = cell.get("second_planting")
        has_sp = isinstance(sp, dict)
        if "B" in rules and not has_sp and suitable is not True:
            for f in PLANTING_FIELDS:
                n = window_count(cell.get(f))
                if n >= 2:
                    v.append(f"B unstructured comma shape: {rk}.{z} {f} carries "
                             f"{n} windows and no second_planting ({slug})")
        if "A" in rules and has_sp:
            for f in ALL_FIELDS:
                if window_count(cell.get(f)) >= 2:
                    v.append(f"A dedup: {rk}.{z} {f} still multi-window alongside "
                             f"second_planting ({slug})")
            # envelope CONTAINMENT (spec §6): the envelope must sit inside the
            # PRIMARY (first) window. Containment, not not-equal-to-the-fall-
            # values, so fava's legitimately shared harvest window passes.
            hv = spans(cell.get("harvest"))
            he = single_date(cell.get("harvest_end"))
            if he and hv and not in_span(he, hv[0]):
                v.append(f"A envelope: {rk}.{z} harvest_end outside the primary "
                         f"harvest window ({slug})")
            po = spans(cell.get("plant_out"))
            lpd = single_date(cell.get("last_plant_date"))
            if lpd and po and not in_span(lpd, po[0]):
                v.append(f"A envelope: {rk}.{z} last_plant_date outside the primary "
                         f"plant window ({slug})")
    return v


if __name__ == "__main__":
    import json
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="crops_data_final.json")
    ap.add_argument("--rules", default="AB", choices=["A", "B", "AB"])
    a = ap.parse_args()
    with open(a.path, encoding="utf-8") as fh:
        data = json.load(fh)
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data
    total = 0
    for c in crops:
        for msg in check_crop(c, frozenset(a.rules)):
            print("VIOLATION:", msg)
            total += 1
    print(f"second_planting_gate: {total} violations (rules={a.rules}, "
          f"crops={len(crops)})")
    sys.exit(1 if total else 0)
