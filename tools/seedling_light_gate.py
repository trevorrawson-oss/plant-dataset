#!/usr/bin/env python3
"""seedling_light_gate -- validates the register #6 germination/seedling-light fields.

Fields (crop-level, siblings of germination_temp_f / the register #7 climate fields):
  germination_light        : enum {light_required, dark_preferring, neutral}, or null.
                             null == reviewed-N/A: crop with no realistic home-from-seed path
                             (grafted trees, citrus, vegetative-only veg). key absent == TODO.
  seedling_light           : enum {bright_default, photoperiod_capped, na, blackout_then_bright}.
                             bright_default == the ~14-16 h bright regime (default for tray-started
                             seed crops); na == no indoor seedling phase (nursery stock + direct-sown);
                             blackout_then_bright == the microgreen cycle (IN-scope for #6, unlike #7);
                             photoperiod_capped == long-day bolt-sensitive seedling (RESERVED, 0 live
                             members today). key absent == TODO.
  seedling_light_cap_hours : int hours, present iff seedling_light == photoperiod_capped.

Checks (HARD, fire ONLY when a field is present -- unauthored roster stays green; ABSENCE is a
coverage TODO, never a shape violation):
  - enum membership (germination_light + seedling_light)
  - cross-field coherence (present-only): a seed crop (propagule == 'seed') may not be
    germination_light null -- a seed crop germinates from seed, so 'no-home-seed-path' N/A is
    contradictory. (The stronger 'a certified seed crop must CARRY germination_light' is the deferred
    register-coverage gate, register #8, not this shape gate.)
  - seedling_light_cap_hours present <=> seedling_light == photoperiod_capped; int in a plausible range.

Usage:
  seedling_light_gate.py [PATH]         # validate (default PATH=crops_data_final.json)
  seedling_light_gate.py --coverage     # print SET/N-A/TODO coverage report + validate

See docs/seedling_light_contract.md.
"""
import json, sys

GERM_LIGHT = {"light_required", "dark_preferring", "neutral"}
SEEDLING_LIGHT = {"bright_default", "photoperiod_capped", "na", "blackout_then_bright"}
CAP_RANGE = (8, 14)   # plausible seedling photoperiod ceiling (hours)


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def check_crop(c):
    """Return list of violation strings for one crop (empty == clean)."""
    slug = c.get("slug") or c.get("id")
    v = []
    prop = c.get("propagule")

    # --- germination_light ---
    if "germination_light" in c:
        gl = c.get("germination_light")
        if gl is None:
            # null == no-home-seed-path N/A; contradictory for a seed crop
            if prop == "seed":
                v.append(f"{slug}: germination_light is null but propagule=='seed' "
                         f"(a seed crop germinates from seed; null=no-home-seed-path is contradictory)")
        elif gl not in GERM_LIGHT:
            v.append(f"{slug}: germination_light {gl!r} not in {sorted(GERM_LIGHT)}")

    # --- seedling_light ---
    sl = c.get("seedling_light")
    if "seedling_light" in c:
        if sl not in SEEDLING_LIGHT:
            v.append(f"{slug}: seedling_light {sl!r} not in {sorted(SEEDLING_LIGHT)}")

    # --- seedling_light_cap_hours present <=> photoperiod_capped ---
    if "seedling_light_cap_hours" in c:
        cap = c.get("seedling_light_cap_hours")
        if sl != "photoperiod_capped":
            v.append(f"{slug}: seedling_light_cap_hours present but seedling_light is {sl!r} "
                     f"(expected 'photoperiod_capped')")
        if not _is_int(cap):
            v.append(f"{slug}: seedling_light_cap_hours {cap!r} is not an int")
        elif not (CAP_RANGE[0] <= cap <= CAP_RANGE[1]):
            v.append(f"{slug}: seedling_light_cap_hours {cap} out of range {CAP_RANGE}")
    else:
        if sl == "photoperiod_capped":
            v.append(f"{slug}: seedling_light=='photoperiod_capped' but seedling_light_cap_hours missing")

    return v


def coverage(crops):
    germ = {"SET": [], "NA": [], "TODO": []}
    seed = {"bright_default": [], "photoperiod_capped": [], "na": [],
            "blackout_then_bright": [], "TODO": []}
    for c in crops:
        slug = c.get("slug") or c.get("id")
        if "germination_light" not in c:
            germ["TODO"].append(slug)
        elif c.get("germination_light") is None:
            germ["NA"].append(slug)
        else:
            germ["SET"].append(slug)
        sl = c.get("seedling_light")
        if "seedling_light" not in c:
            seed["TODO"].append(slug)
        elif sl in seed:
            seed[sl].append(slug)
        else:
            seed["TODO"].append(slug)  # unknown value: check_crop flags the shape; count as not-set
    return germ, seed


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
        germ, seed = coverage(crops)
        n = len(crops)
        print(f"COVERAGE (of {n} crops):")
        print(f"  germination_light: SET {len(germ['SET'])} | N/A {len(germ['NA'])} | TODO {len(germ['TODO'])}")
        print(f"  seedling_light   : bright_default {len(seed['bright_default'])} | "
              f"na {len(seed['na'])} | blackout_then_bright {len(seed['blackout_then_bright'])} | "
              f"photoperiod_capped {len(seed['photoperiod_capped'])} | TODO {len(seed['TODO'])}")
        if germ["TODO"]:
            print(f"  germination_light TODO: {sorted(germ['TODO'])}")

    if violations:
        print(f"\nseedling_light_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nseedling_light_gate: PASS (0 violations)")
    sys.exit(0)


if __name__ == "__main__":
    main()
