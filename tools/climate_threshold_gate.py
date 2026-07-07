#!/usr/bin/env python3
"""climate_threshold_gate -- validates the register #7 climate-threshold fields.

Fields (crop-level, siblings of germination_temp_f):
  heat_threshold_f     : int F, or null (null == reviewed-N/A heat-lover); key absent == TODO
  heat_effect          : enum; present iff heat_threshold_f key present
  frost_tolerance_f    : int F; key absent == TODO
  frost_effect         : enum; present iff frost_tolerance_f present
  chilling_sensitivity_f: int F (non-freezing chilling injury, warm crops), or null
                          (reviewed-N/A: cold-adapted crop); key absent == TODO. Numeric-only,
                          no effect enum (chilling damage is uniform).

Checks (HARD, fire only when a field is present -- unauthored roster stays green):
  - types + plausible ranges
  - enum membership
  - heat_effect present <=> heat_threshold_f present; null threshold <=> heat_effect == heat_tolerant
  - frost_effect present <=> frost_tolerance_f present
  - coherence: when both numeric, frost_tolerance_f < heat_threshold_f

Usage:
  climate_threshold_gate.py [PATH]         # validate (default PATH=crops_data_final.json)
  climate_threshold_gate.py --coverage     # print SET/N-A/TODO coverage report + validate
"""
import json, sys

HEAT_EFFECTS = {"bolting", "poor_fruit_set", "crown_failure", "quality_loss", "heat_tolerant"}
HEAT_STRESS_EFFECTS = HEAT_EFFECTS - {"heat_tolerant"}
FROST_EFFECTS = {"killed", "foliage_damaged"}
HEAT_RANGE = (72, 110)     # plausible daytime-high stress trigger
FROST_RANGE = (-30, 45)    # plausible cold-damage trigger
CHILL_RANGE = (33, 60)     # non-freezing chilling injury (above frost, below ~60F)
# Indoor tray crops -- no outdoor weather exposure, so climate thresholds are legitimately N/A
# (same class as the uncertified mushrooms). Reported as N/A-indoor, not TODO.
INDOOR_SLUGS = {"microgreens-mix", "sunflower-sprouts", "pea-shoots", "radish-microgreens",
                "broccoli-microgreens", "arugula-microgreens", "wheatgrass", "cilantro-microgreens"}

def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

def check_crop(c):
    """Return list of violation strings for one crop (empty == clean)."""
    slug = c.get("slug") or c.get("id")
    v = []
    has_heat_key = "heat_threshold_f" in c
    has_frost_key = "frost_tolerance_f" in c
    ht = c.get("heat_threshold_f")
    he = c.get("heat_effect")
    ft = c.get("frost_tolerance_f")
    fe = c.get("frost_effect")

    # --- heat ---
    if has_heat_key:
        if he is None:
            v.append(f"{slug}: heat_threshold_f present but heat_effect missing")
        elif he not in HEAT_EFFECTS:
            v.append(f"{slug}: heat_effect {he!r} not in {sorted(HEAT_EFFECTS)}")
        if ht is None:
            # reviewed-N/A: must be the heat_tolerant marker
            if he != "heat_tolerant":
                v.append(f"{slug}: heat_threshold_f is null but heat_effect is {he!r} (expected 'heat_tolerant')")
        else:
            if not _is_int(ht):
                v.append(f"{slug}: heat_threshold_f {ht!r} is not an int")
            elif not (HEAT_RANGE[0] <= ht <= HEAT_RANGE[1]):
                v.append(f"{slug}: heat_threshold_f {ht} out of range {HEAT_RANGE}")
            if he == "heat_tolerant":
                v.append(f"{slug}: heat_effect 'heat_tolerant' but heat_threshold_f is a number ({ht})")
    else:
        if he is not None:
            v.append(f"{slug}: heat_effect present but no heat_threshold_f key (orphan)")

    # --- frost ---
    if has_frost_key:
        if not _is_int(ft):
            v.append(f"{slug}: frost_tolerance_f {ft!r} is not an int")
        elif not (FROST_RANGE[0] <= ft <= FROST_RANGE[1]):
            v.append(f"{slug}: frost_tolerance_f {ft} out of range {FROST_RANGE}")
        if fe is None:
            v.append(f"{slug}: frost_tolerance_f present but frost_effect missing")
        elif fe not in FROST_EFFECTS:
            v.append(f"{slug}: frost_effect {fe!r} not in {sorted(FROST_EFFECTS)}")
    else:
        if fe is not None:
            v.append(f"{slug}: frost_effect present but no frost_tolerance_f key (orphan)")

    # --- chilling (numeric-only; null == reviewed-N/A cold-adapted crop; absent == TODO) ---
    cs = c.get("chilling_sensitivity_f")
    if "chilling_sensitivity_f" in c and cs is not None:
        if not _is_int(cs):
            v.append(f"{slug}: chilling_sensitivity_f {cs!r} is not an int")
        elif not (CHILL_RANGE[0] <= cs <= CHILL_RANGE[1]):
            v.append(f"{slug}: chilling_sensitivity_f {cs} out of range {CHILL_RANGE}")

    # --- coherence: frost < chilling < heat where each pair is numeric ---
    if _is_int(ht) and _is_int(ft) and not (ft < ht):
        v.append(f"{slug}: frost_tolerance_f ({ft}) must be < heat_threshold_f ({ht})")
    if _is_int(cs) and _is_int(ft) and not (ft < cs):
        v.append(f"{slug}: frost_tolerance_f ({ft}) must be < chilling_sensitivity_f ({cs})")
    if _is_int(cs) and _is_int(ht) and not (cs < ht):
        v.append(f"{slug}: chilling_sensitivity_f ({cs}) must be < heat_threshold_f ({ht})")

    return v

def coverage(crops):
    heat = {"SET": [], "NA": [], "TODO": []}
    frost = {"SET": [], "TODO": []}
    chill = {"SET": [], "NA": [], "TODO": []}
    indoor = []
    for c in crops:
        slug = c.get("slug") or c.get("id")
        if slug in INDOOR_SLUGS:
            indoor.append(slug)
            continue
        if "heat_threshold_f" not in c:
            heat["TODO"].append(slug)
        elif c.get("heat_threshold_f") is None:
            heat["NA"].append(slug)
        else:
            heat["SET"].append(slug)
        if "frost_tolerance_f" not in c:
            frost["TODO"].append(slug)
        else:
            frost["SET"].append(slug)
        if "chilling_sensitivity_f" not in c:
            chill["TODO"].append(slug)
        elif c.get("chilling_sensitivity_f") is None:
            chill["NA"].append(slug)
        else:
            chill["SET"].append(slug)
    return heat, frost, chill, indoor

def main():
    args = [a for a in sys.argv[1:]]
    show_cov = "--coverage" in args
    args = [a for a in args if a != "--coverage"]
    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    violations = []
    for c in crops:
        violations += check_crop(c)

    if show_cov:
        heat, frost, chill, indoor = coverage(crops)
        n = len(crops)
        print(f"COVERAGE (of {n} crops; {len(indoor)} indoor tray crops N/A, excluded from the counts below):")
        print(f"  heat_threshold_f      : SET {len(heat['SET'])} | N/A {len(heat['NA'])} | TODO {len(heat['TODO'])}")
        print(f"  frost_tolerance_f     : SET {len(frost['SET'])} | TODO {len(frost['TODO'])}")
        print(f"  chilling_sensitivity_f: SET {len(chill['SET'])} | N/A {len(chill['NA'])} | TODO {len(chill['TODO'])}")
        if frost["TODO"]:
            print(f"  frost TODO (uncertified shells, out of scope): {sorted(frost['TODO'])}")

    if violations:
        print(f"\nclimate_threshold_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nclimate_threshold_gate: PASS (0 violations)")
    sys.exit(0)

if __name__ == "__main__":
    main()
