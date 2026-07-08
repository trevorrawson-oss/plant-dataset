#!/usr/bin/env python3
"""register_coverage_gate -- the present-or-explicit-null HARD gate for the cross-crop register fields.

THE GAP THIS CLOSES (docs/kickoffs/13-register-coverage-gate.md, field_addition_register #8):
the register passes shipped so far -- #4 timing spine, #5 watering.schedule_by_stage, #6 germination/
seedling light, #7 climate thresholds -- are guarded only SOFTLY. Each field's standalone gate
validates SHAPE only WHEN THE FIELD IS PRESENT (so partial rollout stays green); a newly-certified
crop that simply OMITS a whole register set passes clean. This gate is the coverage floor -- the same
present-or-explicit-null pattern as whole_crop_gate A17 (npk_ratio) / A20 (display-readiness), extended
to the register fields: every CERTIFIED crop (verification_status.status == 'verified_gs_arc') must
carry each shipped register field OR its defined null/N-A. Uncertified §E shells are exempt (they
certify with their register sets folded into the per-crop checklist -- this gate is what MAKES that
enforceable). Turn a field's requirement on ONLY after its rollout is complete; #4-#7 + #9 are all
complete on the stable 114 roster, so all five register sets are enforced here.

The per-field N-A predicates are REUSED (imported, never re-encoded) from the standalone gates:
  #4 timing_spine_gate.dtm_empty  -> empty-DTM perennials carry no dtm_anchor (nothing to anchor)
     timing_spine_gate.is_microgreen + SEED_LIKE -> sow_depth required only for a seed-like propagule
                                                     that is not a surface-sown tray
  #7 climate_threshold_gate.INDOOR_SLUGS -> the 8 microgreens are N/A-indoor for climate thresholds
  #6 a null germination_light (no home-from-seed path) and #7 a null heat_threshold_f (heat-lover) /
     chilling_sensitivity_f (cold-adapted) are PRESENT values (the key exists) -- their value-shape is
     the standalone gate's job; this gate only requires the key be there.

Required per certified crop (else a coverage violation):
  #4  propagule (universal); dtm_anchor (unless empty-DTM); sow_depth_inches (seed-like, non-microgreen)
  #5  watering.schedule_by_stage (non-empty)
  #6  germination_light + seedling_light (key present; null is a legit present value)
  #7  heat_threshold_f + frost_tolerance_f + chilling_sensitivity_f (key present; exempt INDOOR_SLUGS)
  #9  tray_sowing (key present; 'na' is a legit present value). pot_up is enforced by seed_tray_gate's
      present-iff-real-value coherence via gate_all, so it is not separately required here.

The ladder (day_range_from_sow) / thin_to_inches / harvest_window_days / divide_every_years are
archetype-OPTIONAL (register #1 graceful-omit + thinning/window/division only where they apply), so
they are NOT hard-required here -- their shape, when present, stays with timing_spine_gate.

Usage:
  register_coverage_gate.py [PATH]          # validate every crop (default crops_data_final.json)
  register_coverage_gate.py [PATH] --coverage   # + per-register certified-coverage report
Exit 1 on any violation.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_spine_gate import SEED_LIKE, dtm_empty, is_microgreen
from climate_threshold_gate import INDOOR_SLUGS

CERTIFIED_STATUS = "verified_gs_arc"


def is_certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED_STATUS


def register_coverage_violations(crop):
    """Return a list of coverage-violation strings ([] = clean OR not-certified). A certified crop must
    carry each shipped register field or its defined null/N-A; an uncertified crop is exempt (no-op)."""
    if not is_certified(crop):
        return []
    slug = crop.get("slug") or crop.get("id") or "?"
    V = []

    # ---- #4 timing spine ----
    if not crop.get("propagule"):
        V.append(f"{slug}: #4 propagule missing (every certified crop declares how it is propagated)")
    if not dtm_empty(crop):
        # a crop with an annual maturity must anchor its DTM; empty-DTM perennials are N/A (skipped).
        if not crop.get("dtm_anchor"):
            V.append(f"{slug}: #4 dtm_anchor missing (a crop with a days_to_maturity must anchor it)")
    if crop.get("propagule") in SEED_LIKE and not is_microgreen(crop):
        # planting depth is meaningful only for a seed-like propagule that is not a surface-sown tray.
        if crop.get("sow_depth_inches") is None:
            V.append(f"{slug}: #4 sow_depth_inches missing (seed-like propagule "
                     f"{crop.get('propagule')!r} carries a planting depth)")

    # ---- #5 watering.schedule_by_stage ----
    if not (crop.get("watering") or {}).get("schedule_by_stage"):
        V.append(f"{slug}: #5 watering.schedule_by_stage missing/empty (per-stage watering is required)")

    # ---- #6 germination / seedling light (null is a PRESENT value -> require the key, not a value) ----
    if "germination_light" not in crop:
        V.append(f"{slug}: #6 germination_light missing (present-or-null: null == no home-from-seed path)")
    if "seedling_light" not in crop:
        V.append(f"{slug}: #6 seedling_light missing ('na' is a real value for direct-sown/nursery stock)")

    # ---- #7 climate thresholds (INDOOR_SLUGS are N/A-indoor; null == heat-lover / cold-adapted) ----
    if slug not in INDOOR_SLUGS:
        for f in ("heat_threshold_f", "frost_tolerance_f", "chilling_sensitivity_f"):
            if f not in crop:
                V.append(f"{slug}: #7 {f} missing (present-or-null required; INDOOR_SLUGS are the only N/A)")

    # ---- #9 seed-tray cell protocol ('na' is a PRESENT value -> require the key, not a value) ----
    # pot_up presence is enforced by seed_tray_gate's present-iff-real-value coherence (run roster-wide
    # by gate_all), so A39 requires only the tray_sowing key.
    if "tray_sowing" not in crop:
        V.append(f"{slug}: #9 tray_sowing missing ('na' is a real value for direct-sown/nursery/microgreen)")

    return V


def _coverage(crops):
    """Per-register certified-coverage tallies (SET / N-A / exempt) for the --coverage report."""
    cert = [c for c in crops if is_certified(c)]
    rep = {"certified": len(cert)}
    rep["dtm_anchor_na (empty-DTM perennials)"] = sum(1 for c in cert if dtm_empty(c))
    rep["sow_depth_na (non-seed-like or microgreen)"] = sum(
        1 for c in cert if not (c.get("propagule") in SEED_LIKE and not is_microgreen(c)))
    rep["climate_exempt (INDOOR_SLUGS)"] = sum(1 for c in cert if (c.get("slug") or c.get("id")) in INDOOR_SLUGS)
    rep["germination_light_null (no home-seed path)"] = sum(
        1 for c in cert if "germination_light" in c and c.get("germination_light") is None)
    return rep


def main():
    args = list(sys.argv[1:])
    show_cov = "--coverage" in args
    args = [a for a in args if a != "--coverage"]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    violations = []
    for c in crops:
        violations += register_coverage_violations(c)

    if show_cov:
        rep = _coverage(crops)
        print(f"REGISTER COVERAGE (of {rep['certified']} certified crops):")
        for k, v in rep.items():
            if k != "certified":
                print(f"  {k}: {v}")

    if violations:
        print(f"\nregister_coverage_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nregister_coverage_gate: PASS (every certified crop carries the #4-#7 + #9 register fields or their N/A)")
    sys.exit(0)


if __name__ == "__main__":
    main()
