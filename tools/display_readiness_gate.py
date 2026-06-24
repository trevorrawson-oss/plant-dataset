#!/usr/bin/env python3
"""Display-readiness cert-gate branch (Phase B, audit F5, 2026-06-24). Imported + run by
whole_crop_gate.py.

WHY: cert validates BIOLOGY + sources but NOT that the fields each guide CARD reads are
present, so a crop can certify and still render a BLANK Hero sun stat / pH stat / Feeding
card. The audit found this concentrated in the two citrus (lemon: sunlight, sunlight_hours,
water, fertilizer grid; orange-navel: ph.preferred_range, container decision, fertilizer
grid). This asserts per-archetype presence so the blank-card defect cannot re-ship at scale.

ARCHETYPE-AWARE -- it respects legitimate N/A:
  - indoor (non_seasonal_indoor): the surface is the IndoorCycleCard, so sunlight_hours / ph /
    spacing / container / fertilizer-grid are NOT demanded (microgreens carry [] / null for them).
  - in-ground trees: container_ok == False is a valid DECISION; no pot value is demanded.

The values themselves are SOURCED figures authored upstream -- this gate enforces PRESENCE,
never correctness (the source-truth layer is sampled, not gated).
"""


def _present(v):
    """Truthy presence: not None, not an empty string/list/dict. (0 / False are not display
    values here; every field this gate guards is a string, a non-empty range list, or a bool
    checked separately.)"""
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def display_readiness_violations(crop):
    """Return a list of violation strings ([] = clean)."""
    V = []
    is_indoor = crop.get("calendar_basis") == "non_seasonal_indoor"

    # ---- universal: every crop's Hero/Watering surface needs these ----
    if not _present(crop.get("sunlight")):
        V.append("sunlight: absent (Hero sun stat renders blank)")
    if not _present(crop.get("water")):
        V.append("water: absent (Watering card / Hero renders blank)")

    if is_indoor:
        return V  # the rest is N/A for the indoor (IndoorCycleCard) surface

    # ---- non-indoor: Hero stat grid + Ph + Feeding + container line ----
    if not _present(crop.get("sunlight_hours")):
        V.append("sunlight_hours: absent (Hero sun-hours stat renders blank)")
    if not _present((crop.get("ph") or {}).get("preferred_range")):
        V.append("ph.preferred_range: absent (Hero pH stat renders blank)")
    if not _present(crop.get("spacing_inches")):
        V.append("spacing_inches: absent (spacing stat / planner placeability)")

    fert = crop.get("fertilizer") or {}
    for fk in ("type", "timing", "frequency"):
        if not _present(fert.get(fk)):
            V.append(f"fertilizer.{fk}: absent (Feeding card grid renders blank)")

    cn = crop.get("container_notes") or {}
    co = cn.get("container_ok")
    if not isinstance(co, bool):
        V.append("container_notes.container_ok: not a boolean decision (True/False); "
                 f"got {co!r} -- the container line has no answer to render")
    elif co and not (_present(cn.get("min_pot_gallons")) or _present(cn.get("depth_inches_min"))):
        V.append("container_notes.container_ok is True but no pot (min_pot_gallons) or tray "
                 "(depth_inches_min) dimension is present")
    return V


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path))
    total = 0
    for c in data["crops"]:
        vs = display_readiness_violations(c)
        if vs:
            print(f"  {c.get('slug')} ({c.get('archetype')}):")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"display_readiness gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
