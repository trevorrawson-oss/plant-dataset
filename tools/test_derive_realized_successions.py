#!/usr/bin/env python3
"""Unit + golden tests for the per-zone realized-succession-count deriver.

Spec: 05-methodology/current/succession_realized_count_spec (v1.1, gap-aware,
LOCKED 2026-06-15). The deriver computes resolved_by_zone.<z>.successions_realized:
  1. year_round cell        -> min(floor(52/interval_weeks), 12)
  2. authored sow-date lists -> min(count(succession_spring)+count(succession_fall), 12)
  3. else (day-precise)      -> split [first_plant_date, last_plant_date] (wrap-aware)
                                at internal heat_pause/cold_pause months, sum
                                floor(span_days/(interval_weeks*7))+1 per sub-window,
                                cap at 12.
ALL outcomes capped at 12 (Trevor 2026-06-15: the year_round practical cap applies
globally -- raw floor reads absurd for long warm windows too).

Run from repo root: python3 tools/test_derive_realized_successions.py
"""
import json, copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from derive_realized_successions import derive_cell_realized, crop_in_scope, backfill_crop, CAP

base = json.load(open("crops_data_final.json"))
crops = {c["slug"]: c for c in base["crops"]}


def cell(slug, region, zone):
    return crops[slug]["regions"][region]["resolved_by_zone"][zone]


# ---------------- 1. year_round cap (rule 1) ----------------
assert derive_cell_realized({"year_round": True}, 2) == 12, "year_round iw2 -> min(26,12)=12"
assert derive_cell_realized({"year_round": True}, 3) == 12, "year_round iw3 -> min(17,12)=12"
assert derive_cell_realized({"year_round": True}, 6) == 8, "year_round iw6 -> min(8,12)=8 (sub-cap)"
# real cells
assert derive_cell_realized(cell("basil", "hawaii_tropical", "11"), 3) == 12, "basil hawaii year_round"
assert derive_cell_realized(cell("zinnia", "hawaii_tropical", "11"), 2) == 12, "zinnia hawaii year_round"
print("PASS rule 1 (year_round cap)")

# ---------------- 2. authored sow-date lists (rule 2) ----------------
assert derive_cell_realized(
    {"succession_spring": "Apr 24, May 15, Jun 5, Jun 26", "succession_fall": "Jun 27, Jul 18"}, 3) == 6, \
    "4 spring + 2 fall dates -> 6"
assert derive_cell_realized({"succession_spring": "a,b,c", "succession_fall": None}, 2) == 3, "spring only"
# 15 dates -> capped at 12
assert derive_cell_realized({"succession_spring": ",".join(str(i) for i in range(15))}, 2) == 12, "list cap"
# golden: the authored northern_tier lists (the ground-truth fixtures)
assert derive_cell_realized(cell("carrot", "northern_tier", "3"), 3) == 6, "carrot NT z3 list"
assert derive_cell_realized(cell("carrot", "northern_tier", "4"), 3) == 7, "carrot NT z4 list"
assert derive_cell_realized(cell("lettuce-leaf", "northern_tier", "6"), 2) == 10, "lettuce NT z6 list"
assert derive_cell_realized(cell("lettuce-leaf", "northern_tier", "7"), 2) == 7, "lettuce NT z7 list"
print("PASS rule 2 (authored lists, list precedence)")

# ---------------- 3a. single clean window, day-precise (rule 3) ----------------
# 14-day window, no pause tokens -> floor(14/21)+1 = 1 (whole-month would wrongly give 2)
nopause = ["growing"] * 12
assert derive_cell_realized(
    {"first_plant_date": "Jun 7", "last_plant_date": "Jun 21", "calendar": nopause}, 3) == 1, \
    "short single window day-precise -> 1"
# real: basil NT z3 (the 14-day window)
assert derive_cell_realized(cell("basil", "northern_tier", "3"), 3) == 1, "basil NT z3 short season"
# real: carrot se_gulf z8 -- Jul15->Mar15 wrap, summer pause OUTSIDE window -> single window
assert derive_cell_realized(cell("carrot", "se_gulf", "8"), 3) == 12, "carrot se_gulf continuous mild winter"
print("PASS rule 3a (single window, day-precise)")

# ---------------- 3b. heat-split: pause INSIDE the window (rule 3) ----------------
# Feb1->Sep30 with May/Jun/Jul heat_pause -> [Feb1,Apr30]=88d (5) + [Aug1,Sep30]=60d (3) = 8
split_cal = ["cold_pause", "plant", "plant", "plant", "heat_pause", "heat_pause",
             "heat_pause", "plant", "plant", "harvest", "harvest", "harvest"]
assert derive_cell_realized(
    {"first_plant_date": "Feb 1", "last_plant_date": "Sep 30", "calendar": split_cal}, 3) == 8, \
    "heat-split window -> 5+3 = 8"
# real: carrot ca_interior z8 (the motivating heat-split case)
assert derive_cell_realized(cell("carrot", "ca_interior", "8"), 3) == 8, "carrot ca_interior heat-split"
print("PASS rule 3b (heat-split, pause inside window)")

# ---------------- 3c. global cap on a derived (non-list, non-year_round) cell ----------------
# Sep1->May15 wrap, pause months OUTSIDE the window -> raw floor(256/21)+1 = 13 -> capped 12
wrap_cal = ["plant", "plant", "plant", "plant", "plant", "heat_pause", "heat_pause",
            "heat_pause", "plant", "plant", "plant", "plant"]
assert derive_cell_realized(
    {"first_plant_date": "Sep 1", "last_plant_date": "May 15", "calendar": wrap_cal}, 3) == 12, \
    "long wrap window raw 13 -> capped 12"
assert derive_cell_realized(cell("carrot", "low_desert_az", "9"), 3) == 12, "carrot low_desert capped"
assert derive_cell_realized(cell("lettuce-leaf", "ca_south_coast", "9"), 2) == 12, "lettuce coastal capped"
print("PASS rule 3c (global cap on derived cells)")

# ---------------- not-derivable -> None ----------------
assert derive_cell_realized({"calendar": ["harvest"] * 12}, 3) is None, "no fp/lp, no plant -> None"
assert derive_cell_realized({}, 3) is None, "empty cell -> None"
print("PASS not-derivable -> None")

# ---------------- scope ----------------
assert crop_in_scope(crops["carrot"]) is True, "carrot in scope"
assert crop_in_scope(crops["lettuce-leaf"]) is True, "lettuce in scope"
assert crop_in_scope(crops["zinnia"]) is True, "zinnia in scope"
assert crop_in_scope(crops["basil"]) is True, "basil in scope"
assert crop_in_scope(crops["cherry-tomato"]) is False, "cherry suitable=False -> out of scope"
assert crop_in_scope(crops["beefsteak-tomato"]) is False, "beefsteak suitable=False -> out of scope"
assert crop_in_scope(crops["microgreens-mix"]) is False, "microgreens indoor/unfilled -> out of scope"
print("PASS scope (suitable & filled & non-indoor)")

# ---------------- backfill: strictly additive + idempotent + reconciliation ----------------
# Baseline-independent: works whether or not the canonical already carries the field.
# The ONLY mutations allowed are successions_realized (per cell) + the two policy counts.
for slug in ["carrot", "basil", "lettuce-leaf", "zinnia"]:
    crop = copy.deepcopy(crops[slug])
    before = {(rk, z): copy.deepcopy(c)
              for rk, r in crop["regions"].items()
              for z, c in r["resolved_by_zone"].items()}
    sp_before = copy.deepcopy(crop["succession_policy"])
    summary = backfill_crop(crop)
    assert summary["in_scope"] is True, f"{slug} in scope"
    realized = []
    for rk, r in crop["regions"].items():
        for z, c in r["resolved_by_zone"].items():
            assert "successions_realized" in c, f"{slug} {rk}.{z} missing successions_realized"
            v = c["successions_realized"]
            assert isinstance(v, int) and 1 <= v <= CAP, f"{slug} {rk}.{z} value {v} out of range"
            realized.append(v)
            b = before[(rk, z)]
            assert not (set(b) - set(c)), f"{slug} {rk}.{z} removed keys {set(b) - set(c)}"
            for k in set(c) | set(b):  # every OTHER key byte-identical to before
                if k == "successions_realized":
                    continue
                assert c.get(k) == b.get(k), f"{slug} {rk}.{z} key {k!r} changed"
    mx = max(realized)
    for k in set(crop["succession_policy"]) | set(sp_before):  # only the 2 counts move
        if k in ("successions", "max_successions_per_season"):
            continue
        assert crop["succession_policy"].get(k) == sp_before.get(k), f"{slug} succ_policy {k!r} changed"
    assert crop["succession_policy"]["successions"] == mx, f"{slug} successions == max"
    assert crop["succession_policy"]["max_successions_per_season"] == mx, f"{slug} max_succ == max"
    # idempotent: a second back-fill changes nothing
    second = backfill_crop(crop)
    assert second["changed"] == [], f"{slug} backfill not idempotent: {second['changed']}"
    print(f"  {slug}: {len(realized)} cells, max={mx}, idempotent")
print("PASS backfill (strictly additive + idempotent + reconciliation)")

# ---------------- backfill no-ops on out-of-scope crops ----------------
for slug in ["cherry-tomato", "beefsteak-tomato", "microgreens-mix"]:
    crop = copy.deepcopy(crops[slug])
    summary = backfill_crop(crop)
    assert summary["in_scope"] is False, f"{slug} not in scope"
    # no successions_realized added anywhere
    for r in crop.get("regions", {}).values():
        for c in (r.get("resolved_by_zone") or {}).values():
            if isinstance(c, dict):
                assert "successions_realized" not in c, f"{slug} should not gain successions_realized"
print("PASS backfill no-op on out-of-scope crops")

print("\nALL PASS test_derive_realized_successions")
