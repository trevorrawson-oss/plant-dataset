#!/usr/bin/env python3
"""overwinter_hardiness_gate -- the winter-hardiness / overwintering honesty engine (spec 2026-07-12).

SOFT + standalone (timing_spine / variety_detail pattern). A crop OPTS IN via `winter_hardiness` in
gating_factors; off-scope crops are silent. It validates that a crop's per-variety cold-hardiness data
COHERES with an overwintering claim; it does NOT generate the per-region app claim (that is plant-astro,
INV-2). The zone-coupling machinery is reusable (garlic/artichoke inherit it); the survives-cold
viability RULE here is leek-specific -- vernalization (needs-cold) is designed separately.

Separation of concerns: variety SHAPE (cold_hardiness_class enum, min_temp_f band, DTM) is
variety_detail_gate's job and is NOT re-checked here. This gate checks HONESTY only:
  VIOLATIONS (exit 1, in-scope crops): COVERAGE -- the recommended set spans >=2 distinct hardiness
    classes (so the app can recommend a grow-anywhere summer type AND at least one overwintering type).
  WARNINGS (advisory): WINDOW-FIT -- a `very_hardy` variety labeled maturity_class `early`, or a
    `tender` variety labeled `late` (hardiness class should cohere with season length).

Usage: overwinter_hardiness_gate.py [PATH] [--warnings] [--coverage]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_detail_gate import COLD_HARDINESS, _variety_objs  # reuse enum + variety extractor (DRY)


def in_scope(crop):
    """A crop opts into the hardiness engine by declaring `winter_hardiness` in gating_factors.

    NOTE (garlic/artichoke inheritance): this token is a DIFFERENT opt-in from variety_detail_gate's
    shape scope (which keys off `maturity_class` presence). For leek they align. A future inheritor that
    carries the token but not the shape scope would have its cold_hardiness_class read here without
    variety_detail_gate having shape-validated it; the coverage check degrades gracefully (invalid values
    are enum-filtered, never mis-counted), but a token-in-scope-implies-shape-in-scope check is the clean
    hardening when this engine goes roster-wide (INV-1)."""
    return "winter_hardiness" in (crop.get("gating_factors") or [])


def hardiness_violations(crop):
    V = []
    if not in_scope(crop):
        return V
    slug = crop.get("slug", "?")
    classes = {x.get("cold_hardiness_class") for x in _variety_objs(crop)
               if x.get("cold_hardiness_class") in COLD_HARDINESS}
    if len(classes) < 2:
        V.append(f"{slug}: overwintering crop must recommend >=2 hardiness classes (found {sorted(classes)})")
    return V


def hardiness_warnings(crop):
    W = []
    if not in_scope(crop):
        return W
    slug = crop.get("slug", "?")
    for x in _variety_objs(crop):
        nm = x.get("name") or x.get("id") or "?"
        c, mc = x.get("cold_hardiness_class"), x.get("maturity_class")
        if c == "very_hardy" and mc == "early":
            W.append(f"{slug}/{nm}: very_hardy (overwintering) variety labeled 'early' -- expected a longer season")
        if c == "tender" and mc == "late":
            W.append(f"{slug}/{nm}: tender (summer) variety labeled 'late' -- expected a fast season")
    return W


def coverage_report(crops):
    slugs = sorted(c.get("slug") for c in crops if in_scope(c))
    objs = sum(len(_variety_objs(c)) for c in crops if in_scope(c))
    return {"in_scope_crops": len(slugs), "variety_objs": objs, "slugs": slugs}


if __name__ == "__main__":
    args = list(sys.argv[1:])
    show_warn = "--warnings" in args
    show_cov = "--coverage" in args
    args = [a for a in args if a not in ("--warnings", "--coverage")]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    total = 0
    for c in crops:
        for v in hardiness_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    warns = 0
    if show_warn:
        for c in crops:
            for w in hardiness_warnings(c):
                print(f"  WARNING: {w}")
                warns += 1
    cov = coverage_report(crops)
    if show_cov:
        print(f"  COVERAGE: in_scope_crops={cov['in_scope_crops']} variety_objs={cov['variety_objs']} "
              f"slugs={cov['slugs']}")
    print(f"overwinter_hardiness: in_scope={cov['in_scope_crops']} objs={cov['variety_objs']} | "
          f"violations={total} warnings={warns}")
    sys.exit(1 if total else 0)
