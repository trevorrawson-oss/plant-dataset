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

# The qualitative summer-heat-adequacy verdict for a `heat_accumulation` crop (orange,
# grapefruit). A COARSE ripening-adequacy band, not a GDD number (evergreen amendment
# section 3): high (desert) / adequate (warm inland) / marginal (borderline) /
# insufficient (cool-coastal -- frost-safe but fruit stays sour). Ordinal hot -> cold.
HEAT_BASIS_ENUM = {"high", "adequate", "marginal", "insufficient"}

# Both permanent-tree calendar bases run these invariants. `perennial_chill_gated` =
# deciduous (chill Goldilocks band); `perennial_evergreen` = evergreen (citrus/avocado/
# olive, no dormancy). See tree_region_model_evergreen_amendment_v1_0.
PERENNIAL_BASES = {"perennial_chill_gated", "perennial_evergreen"}


def _is_number(v):
    # a bool passes isinstance(_, int) in Python -- exclude it, it is not a chill value.
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def gating_factors(crop):
    """The crop's suitability gate(s). Authored explicitly on evergreen anchors; a
    `perennial_chill_gated` crop with none defaults to chill+cold (so peach/apple --
    which predate the field -- hit the exact chill direction-split path unchanged)."""
    g = crop.get("gating_factors")
    if g:
        return g
    return (["chill_hours", "cold_hardiness"]
            if crop.get("calendar_basis") == "perennial_chill_gated" else ["cold_hardiness"])


def min_variety_chill(crop, default=400):
    """The crop's lowest recommended-variety chill requirement -- the 'chill reliably met'
    floor for the no-fruit split. Falls back to 400 (peach's Florida King) if unstated."""
    vs = (crop.get("varieties") or {}).get("recommended") or []
    chills = [v.get("chill_hours_required") for v in vs
              if isinstance(v, dict) and isinstance(v.get("chill_hours_required"), (int, float))]
    return min(chills) if chills else default


def perennial_cert_violations(crop, chill_table=None):
    """Return a list of violation strings for a permanent-tree crop ([] = clean).
    No-op (returns []) for any non-perennial calendar_basis. The universal invariants
    apply to every perennial base; the no-fruit DIRECTION SPLIT is keyed on
    gating_factors -- chill-gated crops get the chill Goldilocks split, a cold-only
    evergreen does not (colder is monotonically worse -- no warm-edge no-chill failure).

    `chill_table` is the shared, crop-invariant region_chill_delivered table
    (region -> {zone -> [lo,hi]}); the no-fruit split reads the DELIVERED band from it,
    NOT from a per-cell crop field (the F2 refactor). whole_crop_gate passes
    data["region_chill_delivered"]; a chill-gated crop with no table entry for a
    survives_no_fruit cell cannot apply the split (a violation)."""
    if crop.get("calendar_basis") not in PERENNIAL_BASES:
        return []
    V = []
    chill_table = chill_table or {}
    chill_gated = "chill_hours" in gating_factors(crop)
    heat_gated = "heat_accumulation" in gating_factors(crop)
    # C2 (incognito-redteam 2026-06-27): a perennial_chill_gated crop IS chill-gated by
    # definition, so "chill_hours" must be in its EFFECTIVE gating_factors (the no-fruit split
    # basis). peach/apple ship gating_factors:null -> the default carries chill_hours -> covered;
    # but an EXPLICIT list that drops the token silently flips chill_gated=False and skips the
    # split (an over-promising calendar then ships). This is the missing mirror of
    # berries_woody_gate.py:59, scoped to perennial_chill_gated only (a cold-only evergreen is
    # legitimately not chill-gated, so it is exempt).
    if crop.get("calendar_basis") == "perennial_chill_gated" and not chill_gated:
        V.append("a perennial_chill_gated crop must keep 'chill_hours' in gating_factors "
                 "(the no-fruit chill split basis); got %r" % (crop.get("gating_factors"),))
    # D5 (re-audit #2): the heat floor below only runs when heat_gated; a crop carrying heat
    # machinery (any cell with a heat_summer_basis) that drops the 'heat_accumulation' token would
    # silently no-op it. Mirror of the C2 chill guard (and the C5 photoperiod machinery guard):
    # heat machinery present => the token must be present.
    if not heat_gated:
        has_heat_cells = any(
            isinstance(cell, dict) and cell.get("heat_summer_basis") is not None
            for r in (crop.get("regions") or {}).values() if isinstance(r, dict)
            for cell in (r.get("resolved_by_zone") or {}).values())
        if has_heat_cells:
            V.append("a crop carrying heat_summer_basis cells must keep 'heat_accumulation' in "
                     "gating_factors (the heat floor basis); got %r" % (crop.get("gating_factors"),))
    floor = min_variety_chill(crop) if chill_gated else None
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
                # D4 (re-audit #2): a null suitability is the Step-3.5 admission state ONLY on an
                # UNFILLED cell. A FILLED cell (one carrying a calendar that renders a 12-month fruit
                # strip) with null suitability evaded EVERY suitability/no-fruit/heat invariant below
                # while the calendar shipped -- a fruit calendar in a zone the tree may die in. Flag
                # it; A2 still owns the truly-unfilled (no-calendar) cells.
                if cell.get("calendar"):
                    V.append(f"{rk}.{z}: filled cell (carries a calendar) has a null suitability -- "
                             f"it renders a calendar while skipping the suitability/no-fruit/heat "
                             f"invariants; a calendar-bearing cell must declare its suitability")
                continue
            if s not in SUITABILITY_ENUM:
                V.append(f"{rk}.{z}: suitability {s!r} not in the 4-value enum")
                continue
            cal = cell.get("calendar") or []
            chill = (chill_table.get(rk) or {}).get(z)  # shared region+zone delivered band
            chill_lo = chill[0] if (isinstance(chill, list) and chill) else None
            if s == "unsuitable":
                if cal:
                    V.append(f"{rk}.{z}: unsuitable cell must have an empty calendar")
            elif s == "survives_no_fruit":
                # the chill direction-split applies only to a chill-gated tree (a chill
                # Goldilocks band: cold-edge blooms -> calendar; chill-edge -> empty). A
                # cold-only evergreen has no such band, so survives_no_fruit may carry a
                # calendar (blooms in mild years) or be empty (no dependable crop) -- both honest.
                if chill_gated:
                    if chill_lo is None:
                        V.append(f"{rk}.{z}: survives_no_fruit cell has no delivered band in region_chill_delivered (missing -- cannot apply the no-fruit split)")
                    elif chill_lo >= floor and not cal:
                        V.append(f"{rk}.{z}: survives_no_fruit with chill met ({chill_lo} >= {floor}) MUST carry a calendar (under-report)")
                    elif chill_lo < floor and cal:
                        V.append(f"{rk}.{z}: survives_no_fruit chill-limited ({chill_lo} < {floor}) MUST have an empty calendar (over-promise)")
            else:  # fruits_reliably / marginal
                if not cal:
                    V.append(f"{rk}.{z}: {s} cell must carry a calendar")
            # --- heat-accumulation FLOOR (orange/grapefruit; evergreen amendment section 4):
            # a frost-safe cell that cannot bank enough summer heat to ripen sweet fruit is
            # capped BELOW fruits_reliably -- the third no-fruit direction (vs the cold-only
            # monotone + the chill Goldilocks band). `unsuitable` is cold-decided (heat moot),
            # so the heat datum is not demanded there. ---
            if heat_gated and s != "unsuitable":
                hb = cell.get("heat_summer_basis")
                if hb is None:
                    V.append(f"{rk}.{z}: heat-gated cell missing heat_summer_basis (cannot apply the heat floor)")
                elif hb not in HEAT_BASIS_ENUM:
                    V.append(f"{rk}.{z}: heat_summer_basis {hb!r} not in {sorted(HEAT_BASIS_ENUM)}")
                elif hb == "insufficient" and s == "fruits_reliably":
                    V.append(f"{rk}.{z}: heat_summer_basis 'insufficient' cannot be fruits_reliably (needs summer heat to sweeten the crop)")
    return V


def perennial_variety_chill_violations(crop):
    """Variety-chill TYPE lock for deciduous fruit trees (whole_crop_gate A22). Fires ONLY for
    calendar_basis == perennial_chill_gated (a no-op for evergreen citrus, which is NOT chill-
    gated, and for annuals). The deciduous-tree analog of the berries_woody A21 lock: every
    recommended variety must carry a NUMERIC chill_hours_required (a string/None violates) and
    NO legacy string `chill_hours`.

    Why this is a real gate, not just a display nicety: min_variety_chill() above silently SKIPS
    non-numeric chill_hours_required values, so a string variety chill was previously unreported
    AND dropped that variety from the no-fruit-split `floor` -- a bad string could silently shift
    the floor and reclassify survives_no_fruit calendar cells. (Closes incognito-audit B2, the
    deciduous-tree analog of the berries_woody string->numeric lock. 2026-06-25.)

    Unlike the berries_woody lock this does NOT require a chill_hours_range key -- deciduous tree
    varieties carry a single chill_hours_required scalar, no range shape.
    """
    if crop.get("calendar_basis") != "perennial_chill_gated":
        return []
    V = []
    for i, v in enumerate((crop.get("varieties") or {}).get("recommended") or []):
        if not isinstance(v, dict):
            continue
        name = v.get("name")
        if not _is_number(v.get("chill_hours_required")):
            V.append(f"varieties.recommended[{i}] ({name!r}): chill_hours_required must be "
                     f"numeric (the chill-gating threshold + the no-fruit-split floor); "
                     f"got {v.get('chill_hours_required')!r}")
        if isinstance(v.get("chill_hours"), str):
            V.append(f"varieties.recommended[{i}] ({name!r}): a string chill_hours "
                     f"({v.get('chill_hours')!r}) is the dropped legacy form -- use a numeric "
                     f"chill_hours_required")
    return V
