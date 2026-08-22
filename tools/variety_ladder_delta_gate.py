#!/usr/bin/env python3
"""variety_ladder_delta_gate -- the variety-level control-ladder delta integrity engine
(PLA-8 Round 1 mechanism, spec 2026-08-22).

SOFT + standalone at birth, exactly like `control_ladder_gate` and `variety_resistance_gate` were.
DORMANT: not wired into whole_crop_gate or gate_all until Round 2's data actually lands -- a roster
gate armed ahead of its data floods a parallel session's gauntlet.

A variety OPTS IN by carrying a non-empty `ladder_delta`. Every other variety and crop is silently
valid, so the un-migrated roster stays green and "no delta" is always the legitimate N/A branch.

    "ladder_delta": {
      "<problem-id>": {
        "basis": "resistance" | "source",
        "sources": ["cornell_ext"],            # required (and T1) when basis == "source"
        "rungs": [
          {"method": "sulfur", "op": "drop", "why_beginner": "...", "why_seasoned": "..."},
          {"method": "garden_sanitation", "op": "replace", "note_beginner": "...",
           "note_seasoned": "..."},
          {"method": "prune_out_infection", "op": "add", "after": "garden_sanitation",
           "note_beginner": "...", "note_seasoned": "..."}
        ]
      }
    }

GUARD FAMILIES (each independently reachable -- see tools/mutate_variety_ladder_delta_suite.py):

  G1 REFERENTIAL  -- the delta keys a real problem `id` on this crop, that problem actually has a
                     `control_ladder`, and every rung `method` resolves: drop/replace against the
                     PARENT ladder, add against `control_methods` and NOT already in the parent.
                     `basis: "resistance"` must be backed by a real grade on this same variety.
  G2 NON-VACUITY  -- a delta that is not a delta: empty `rungs`, a duplicated method, or a
                     `replace` whose note is BYTE-EQUAL to the parent's.
  G3 NEAR-VERBATIM-- a `replace` note whose similarity to the parent note is >= 0.85. This is the
                     load-bearing guard: G2 alone is defeated by changing a single word, which is
                     how the PLA-6 pill duplication survived across 36 crops. (PLA-6's finding that
                     the metric is INVERTED applies to judging register distinctness; for detecting
                     COPYING, high similarity is the correct signal -- same instrument and threshold
                     as `test_no_pair_is_a_near_verbatim_copy`.)
  G4 RESOLVED-ORDER-- the ladder that RESULTS from applying the delta is still softest-first. An
                     `add` must not break the least-invasive-first invariant the arc exists for.

Usage: variety_ladder_delta_gate.py [PATH]
"""
import difflib
import json
import re
import sys

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
TIER_RANK = {t: i for i, t in enumerate(TIERS)}
OPS = {"drop", "replace", "add"}
BASES = {"resistance", "source"}
NEAR_VERBATIM = 0.85
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _norm(s):
    """Whitespace/case-insensitive normalization, so cosmetic reflow cannot dodge G3."""
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def similarity(a, b):
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _problems(crop):
    return list(crop.get("pests") or []) + list(crop.get("diseases") or [])


def _laddered(crop):
    """problem id -> the problem object, for problems that actually carry a ladder."""
    out = {}
    for p in _problems(crop):
        if isinstance(p, dict) and isinstance(p.get("id"), str) and p.get("control_ladder"):
            out[p["id"]] = p
    return out


def _variety_objs(crop):
    v = crop.get("varieties")
    if not isinstance(v, dict):
        return []
    rec = v.get("recommended")
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def resolve_ladder(parent_rungs, rungs):
    """Apply a delta to a parent ladder. Pure; used by G4 and by any future renderer/resolver."""
    drops = {r["method"] for r in rungs if r.get("op") == "drop" and isinstance(r.get("method"), str)}
    repl = {r["method"]: r for r in rungs if r.get("op") == "replace" and isinstance(r.get("method"), str)}
    out = []
    for pr in parent_rungs:
        m = pr.get("method")
        if m in drops:
            continue
        out.append(dict(pr, **{k: v for k, v in repl[m].items()
                               if k.startswith("note_")}) if m in repl else dict(pr))
    for r in rungs:
        if r.get("op") != "add" or not isinstance(r.get("method"), str):
            continue
        new = {k: v for k, v in r.items() if k in ("method",) or k.startswith("note_")}
        after = r.get("after")
        idx = next((i + 1 for i, x in enumerate(out) if x.get("method") == after), len(out))
        out.insert(idx, new)
    return out


def delta_violations(crop, catalog, source_catalog=None):
    V = []
    source_catalog = source_catalog or {}
    slug = crop.get("slug", "?")
    laddered = _laddered(crop)

    for x in _variety_objs(crop):
        d = x.get("ladder_delta")
        if d is None:
            continue  # N/A branch: absence is always valid
        nm = x.get("id") or x.get("name") or "?"
        where = f"{slug}/{nm}"
        if not isinstance(d, dict):
            V.append(f"{where}: ladder_delta must be a dict, got {type(d).__name__}")
            continue
        if not d:
            V.append(f"{where}: ladder_delta is empty (omit the key instead)")
            continue

        for pid, entry in d.items():
            tag = f"{where}/{pid}"
            # -- G1 referential: the problem ------------------------------------------------
            if not (isinstance(pid, str) and ID_RE.match(pid)):
                V.append(f"{tag}: ladder_delta key {pid!r} is not a kebab id")
                continue
            if pid not in laddered:
                known = sorted(laddered)
                V.append(f"{tag}: {pid!r} is not a laddered pest/disease id on {slug} "
                         f"(known: {known})")
                continue
            if not isinstance(entry, dict):
                V.append(f"{tag}: delta entry must be a dict, got {type(entry).__name__}")
                continue

            parent_rungs = laddered[pid]["control_ladder"]
            parent_by_method = {r.get("method"): r for r in parent_rungs}

            basis = entry.get("basis")
            if basis not in BASES:
                V.append(f"{tag}: basis {basis!r} not in {sorted(BASES)}")
            elif basis == "source":
                srcs = entry.get("sources")
                if not (isinstance(srcs, list) and srcs):
                    V.append(f"{tag}: basis 'source' requires a non-empty sources list")
                else:
                    for s in srcs:
                        if s not in source_catalog:
                            V.append(f"{tag}: source {s!r} not in source_catalog")
                        elif source_catalog[s].get("tier") != "T1":
                            V.append(f"{tag}: source {s!r} is not T1")
            elif basis == "resistance":
                grades = x.get("resistance")
                if not (isinstance(grades, dict) and pid in grades):
                    V.append(f"{tag}: basis 'resistance' but the variety carries no resistance "
                             f"grade for {pid!r}")

            rungs = entry.get("rungs")
            if not isinstance(rungs, list):
                V.append(f"{tag}: rungs must be a list, got {type(rungs).__name__}")
                continue
            # -- G2 non-vacuity: an empty delta is not a delta -------------------------------
            if not rungs:
                V.append(f"{tag}: rungs is empty -- that is not a delta")
                continue

            seen = set()
            for r in rungs:
                if not isinstance(r, dict):
                    V.append(f"{tag}: rung must be a dict, got {type(r).__name__}")
                    continue
                m, op = r.get("method"), r.get("op")
                if not (isinstance(m, str) and m):
                    V.append(f"{tag}: rung missing a string 'method'")
                    continue
                if op not in OPS:
                    V.append(f"{tag}/{m}: op {op!r} not in {sorted(OPS)}")
                    continue
                # -- G2 non-vacuity: the same rung twice ------------------------------------
                if m in seen:
                    V.append(f"{tag}/{m}: method appears twice in one delta")
                seen.add(m)

                if op in ("drop", "replace"):
                    # -- G1 referential: against the PARENT ladder --------------------------
                    if m not in parent_by_method:
                        V.append(f"{tag}/{m}: op {op!r} targets a method that is not in "
                                 f"{pid}'s parent ladder (parent: {sorted(parent_by_method)})")
                        continue
                else:  # add
                    if m not in catalog:
                        V.append(f"{tag}/{m}: op 'add' references unknown control_methods key")
                        continue
                    if m in parent_by_method:
                        V.append(f"{tag}/{m}: op 'add' names a method the parent ladder already "
                                 f"has -- use 'replace'")
                        continue
                    if r.get("after") is not None and r["after"] not in parent_by_method:
                        V.append(f"{tag}/{m}: 'after' names {r['after']!r}, not in the parent ladder")

                if op == "drop":
                    for k in ("note_beginner", "note_seasoned"):
                        if k in r:
                            V.append(f"{tag}/{m}: a 'drop' must not carry {k} "
                                     f"(use why_beginner / why_seasoned)")
                else:
                    if not (isinstance(r.get("note_beginner"), str) and r["note_beginner"].strip()):
                        V.append(f"{tag}/{m}: op {op!r} requires a non-empty note_beginner")

                if op == "replace":
                    parent = parent_by_method[m]
                    for k in ("note_beginner", "note_seasoned"):
                        new, old = r.get(k), parent.get(k)
                        if not (isinstance(new, str) and isinstance(old, str)):
                            continue
                        # -- G2 non-vacuity: byte-equal is a duplicate, not a delta ---------
                        if new == old:
                            V.append(f"{tag}/{m}: {k} is BYTE-EQUAL to the parent rung -- "
                                     f"that is a duplicate, not a delta")
                        # -- G3 near-verbatim ----------------------------------------------
                        ratio = similarity(new, old)
                        if ratio >= NEAR_VERBATIM:
                            V.append(f"{tag}/{m}: {k} is a near-verbatim copy of the parent rung "
                                     f"(similarity {ratio:.3f} >= {NEAR_VERBATIM})")

            # -- G4 the RESOLVED ladder is still softest-first -------------------------------
            ranks = []
            for rr in resolve_ladder(parent_rungs, [r for r in rungs if isinstance(r, dict)]):
                mm = catalog.get(rr.get("method")) or {}
                rk = TIER_RANK.get(mm.get("tier"))
                if rk is not None:
                    ranks.append(rk)
            if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):
                V.append(f"{tag}: the RESOLVED ladder is not softest-first (tier ranks {ranks})")
    return V


def all_violations(data):
    catalog = data.get("control_methods") or {}
    srcs = data.get("source_catalog") or {}
    V = []
    for crop in data.get("crops", []):
        V += delta_violations(crop, catalog, srcs)
    return V


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path) as fh:
        data = json.load(fh)
    V = all_violations(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"variety_ladder_delta_gate: {len(V)} violation(s)")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
