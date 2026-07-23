#!/usr/bin/env python3
"""variety_resistance_gate -- validates the per-variety `resistance` map (spec 2026-07-23).

SOFT + standalone (control_ladder / variety_detail pattern): a variety OPTS IN by carrying a
non-empty `resistance` dict; every other variety and crop is silently valid -- the un-migrated
roster stays green, and a variety with no documented resistance is the legit N/A branch, never a
violation.

VIOLATIONS (exit 1): a `resistance` key that is not a real pest/disease `id` on that crop
(referential); a grade outside the enum; a malformed shape (resistance not a dict, key not kebab,
value not a string).

Hard-flip into whole_crop_gate A39 + gate_all is deferred to the roster-wide rollout (INV-1).

Usage: variety_resistance_gate.py [PATH]
"""
import json, os, re, sys

GRADES = {"immune", "resistant", "tolerant", "susceptible"}
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _problem_ids(crop):
    ids = set()
    for key in ("pests", "diseases"):
        for p in crop.get(key, []) or []:
            pid = p.get("id")
            if isinstance(pid, str):
                ids.add(pid)
    return ids


def _variety_objs(crop):
    v = crop.get("varieties")
    if not isinstance(v, dict):
        return []
    rec = v.get("recommended")
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def resistance_violations(crop):
    V = []
    slug = crop.get("slug", "?")
    valid_ids = _problem_ids(crop)
    for x in _variety_objs(crop):
        r = x.get("resistance")
        if r is None:
            continue  # N/A branch: absence is always valid
        nm = x.get("name") or x.get("id") or "?"
        if not isinstance(r, dict):
            V.append(f"{slug}/{nm}: resistance must be a dict, got {type(r).__name__}")
            continue
        for did, grade in r.items():
            if not (isinstance(did, str) and KEBAB_RE.match(did)):
                V.append(f"{slug}/{nm}: resistance key {did!r} is not a kebab id")
            elif did not in valid_ids:
                V.append(f"{slug}/{nm}: resistance key {did!r} is not a pest/disease id on {slug} "
                         f"(known: {sorted(valid_ids)})")
            if not isinstance(grade, str):
                V.append(f"{slug}/{nm}: resistance[{did!r}] value must be a string, "
                         f"got {type(grade).__name__}")
            elif grade not in GRADES:
                V.append(f"{slug}/{nm}: resistance[{did!r}] grade {grade!r} not in {sorted(GRADES)}")
    return V


def all_violations(data):
    V = []
    for crop in data.get("crops", []):
        V += resistance_violations(crop)
    return V


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path) as fh:
        data = json.load(fh)
    V = all_violations(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"variety_resistance_gate: {len(V)} violation(s)")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
