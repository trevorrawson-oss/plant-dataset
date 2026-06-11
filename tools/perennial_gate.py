#!/usr/bin/env python3
"""Perennial (tree) cert-gate branch -- the tree-shape invariants the generic
whole_crop_gate does not encode. Fires ONLY for `calendar_basis == "perennial_chill_gated"`
(a no-op for annual crops). Imported + run by whole_crop_gate.py at the Step-11 cert.

See gold_standard_arc_checklist_v1_8_amendment §4-5 + tree_region_model_spec_v1_0.
The NO-FRUIT DIRECTION SPLIT (FLAG A, Trevor 2026-06-10) is the load-bearing rule:
a `survives_no_fruit` cell carries a calendar IFF chill is reliably met (cold-edge, the
tree blooms; an empty calendar UNDER-reports) vs is chill-limited (a calendar OVER-promises).
"""

SUITABILITY_ENUM = {"fruits_reliably", "marginal", "survives_no_fruit", "unsuitable"}


def min_variety_chill(crop, default=400):
    """The crop's lowest recommended-variety chill requirement -- the 'chill reliably met'
    floor for the no-fruit split. Falls back to 400 (peach's Florida King) if unstated."""
    vs = (crop.get("varieties") or {}).get("recommended") or []
    chills = [v.get("chill_hours_required") for v in vs
              if isinstance(v, dict) and isinstance(v.get("chill_hours_required"), (int, float))]
    return min(chills) if chills else default


def perennial_cert_violations(crop):
    """Return a list of violation strings for a perennial_chill_gated crop ([] = clean).
    No-op (returns []) for any other calendar_basis."""
    if crop.get("calendar_basis") != "perennial_chill_gated":
        return []
    V = []
    floor = min_variety_chill(crop)
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        # --- region-constant rule: exactly ONE perennial establishment entry ---
        pl = r.get("plantings") or []
        if not (isinstance(pl, list) and len(pl) == 1):
            V.append(f"{rk}: tree plantings must be exactly 1 establishment entry, got {len(pl)}")
        for p in pl:
            if not isinstance(p, dict):
                continue
            if p.get("track") != "perennial":
                V.append(f"{rk}: plantings track must be 'perennial', got {p.get('track')!r}")
            if p.get("track") in ("succession", "second_planting"):
                V.append(f"{rk}: a tree must not carry succession/second_planting plantings")
            for bad in ("start_indoors", "direct_sow"):
                if bad in p:
                    V.append(f"{rk}: tree establishment entry must not carry {bad}")
        # --- zone-resolved layer: suitability + the no-fruit direction split ---
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            s = cell.get("suitability")
            if s is None:
                # unfilled shell cell (Step 3.5 admission state) -- the region-fill check
                # (whole_crop_gate A2) owns "this region is unauthored"; A3 only enforces the
                # tree invariants on FILLED cells, so a null suitability is skipped, not flagged.
                continue
            if s not in SUITABILITY_ENUM:
                V.append(f"{rk}.{z}: suitability {s!r} not in the 4-value enum")
                continue
            cal = cell.get("calendar") or []
            chill = cell.get("chill_hours_delivered")
            chill_lo = chill[0] if (isinstance(chill, list) and chill) else None
            if s == "unsuitable":
                if cal:
                    V.append(f"{rk}.{z}: unsuitable cell must have an empty calendar")
            elif s == "survives_no_fruit":
                if chill_lo is None:
                    V.append(f"{rk}.{z}: survives_no_fruit cell missing chill_hours_delivered (cannot apply the no-fruit split)")
                elif chill_lo >= floor and not cal:
                    V.append(f"{rk}.{z}: survives_no_fruit with chill met ({chill_lo} >= {floor}) MUST carry a calendar (under-report)")
                elif chill_lo < floor and cal:
                    V.append(f"{rk}.{z}: survives_no_fruit chill-limited ({chill_lo} < {floor}) MUST have an empty calendar (over-promise)")
            else:  # fruits_reliably / marginal
                if not cal:
                    V.append(f"{rk}.{z}: {s} cell must carry a calendar")
    return V
