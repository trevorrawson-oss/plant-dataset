#!/usr/bin/env python3
"""seed_tray_gate -- validates the register #9 seed-tray cell-protocol fields.

Fields (crop-level, siblings of seedling_light / germination_temp_f):
  tray_sowing : enum {multi_sow_thin_to_one, single_sow, multisow_clump, na}.
                multi_sow_thin_to_one == the default (sow 2-3 seeds per cell, thin to the strongest);
                single_sow == large seed sown 1-2 per cell (cucurbits, big-seed flowers), little thinning;
                multisow_clump == sown as a clump and transplanted AS a clump, not thinned (leek, spring
                onion); na == no cell-tray phase (direct-sown, nursery/vegetative stock, microgreen mat).
                key absent == TODO (uncertified shell).
  pot_up      : enum {recommended, optional, not_needed}, present iff tray_sowing is a REAL tray value
                (the tray-started-from-seed set). recommended == pot up before hardening off (slow
                large-growers outgrow the plug: tomato/pepper/eggplant); optional == you CAN pot up if
                seedlings outgrow their cells but cell -> garden is fine (fast brassicas); not_needed ==
                transplant straight from the cell (cucurbits resent disturbance; thin/grassy seedlings).
                absent for every tray_sowing == 'na' crop (no tray-from-seed phase, nothing to pot up).

Checks (HARD, fire ONLY when a field is present -- unauthored roster stays green; ABSENCE is a coverage
TODO, never a shape violation):
  - tray_sowing enum membership; pot_up enum membership.
  - na <-> seedling_light coherence (present-only, reuse register #6's validated signal): a real tray
    value requires seedling_light == 'bright_default'; 'na' requires seedling_light in
    {'na','blackout_then_bright'}.
  - pot_up present <=> tray_sowing is a real tray value (orphan pot_up bounces; a real tray value missing
    pot_up bounces).
  multisow_clump is RESERVED (0 live members in the current roster, like #6's photoperiod_capped) -- kept
  defined and gate-tested, ready the moment a crop genuinely needs it.

Usage:
  seed_tray_gate.py [PATH]         # validate (default PATH=crops_data_final.json)
  seed_tray_gate.py --coverage     # print SET/na/TODO coverage report + validate

See docs/seed_tray_protocol_contract.md.
"""
import json
import sys

TRAY_SOWING = {"multi_sow_thin_to_one", "single_sow", "multisow_clump", "na"}
REAL_TRAY = {"multi_sow_thin_to_one", "single_sow", "multisow_clump"}  # every value except na
POT_UP = {"recommended", "optional", "not_needed"}
BRIGHT = "bright_default"
NA_SEEDLING = {"na", "blackout_then_bright"}  # seedling_light values that carry tray_sowing == 'na'


def check_crop(c):
    """Return list of violation strings for one crop (empty == clean)."""
    slug = c.get("slug") or c.get("id")
    v = []
    ts = c.get("tray_sowing")
    sl = c.get("seedling_light")
    has_ts = "tray_sowing" in c
    has_pu = "pot_up" in c

    # --- tray_sowing enum membership ---
    if has_ts and ts not in TRAY_SOWING:
        v.append(f"{slug}: tray_sowing {ts!r} not in {sorted(TRAY_SOWING)}")

    # --- na <-> seedling_light coherence (present-only; only meaningful for a valid tray_sowing) ---
    if has_ts and ts in TRAY_SOWING and "seedling_light" in c:
        if ts in REAL_TRAY and sl != BRIGHT:
            v.append(f"{slug}: tray_sowing {ts!r} (a real tray value) but seedling_light {sl!r} "
                     f"(expected 'bright_default' -- a tray value needs an indoor cell-tray phase)")
        if ts == "na" and sl not in NA_SEEDLING:
            v.append(f"{slug}: tray_sowing 'na' but seedling_light {sl!r} not in {sorted(NA_SEEDLING)} "
                     f"(na is for direct-sown/nursery/microgreen -- not a tray-started crop)")

    # --- pot_up present <=> tray_sowing is a real tray value ---
    if has_pu:
        pu = c.get("pot_up")
        if pu not in POT_UP:
            v.append(f"{slug}: pot_up {pu!r} not in {sorted(POT_UP)}")
        if not (has_ts and ts in REAL_TRAY):
            v.append(f"{slug}: pot_up present but tray_sowing {ts!r} is not a real tray value "
                     f"(expected one of {sorted(REAL_TRAY)})")
    else:
        if has_ts and ts in REAL_TRAY:
            v.append(f"{slug}: tray_sowing {ts!r} (a real tray value) but pot_up missing "
                     f"(the pot-up enum is required for every tray-started crop)")

    return v


def coverage(crops):
    tray = {"multi_sow_thin_to_one": [], "single_sow": [], "multisow_clump": [], "na": [], "TODO": []}
    pot = {"recommended": [], "optional": [], "not_needed": [], "absent": []}
    for c in crops:
        slug = c.get("slug") or c.get("id")
        ts = c.get("tray_sowing")
        if "tray_sowing" not in c:
            tray["TODO"].append(slug)
        elif ts in tray:
            tray[ts].append(slug)
        else:
            tray["TODO"].append(slug)  # unknown value: check_crop flags the shape; count as not-set
        pu = c.get("pot_up")
        if "pot_up" not in c:
            pot["absent"].append(slug)
        elif pu in pot:
            pot[pu].append(slug)
        else:
            pot["absent"].append(slug)  # unknown value: check_crop flags the shape; not counted
    return tray, pot


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
        tray, pot = coverage(crops)
        n = len(crops)
        print(f"COVERAGE (of {n} crops):")
        print(f"  tray_sowing: multi_sow_thin_to_one {len(tray['multi_sow_thin_to_one'])} | "
              f"single_sow {len(tray['single_sow'])} | multisow_clump {len(tray['multisow_clump'])} | "
              f"na {len(tray['na'])} | TODO {len(tray['TODO'])}")
        print(f"  pot_up     : recommended {len(pot['recommended'])} | optional {len(pot['optional'])} | "
              f"not_needed {len(pot['not_needed'])} | absent {len(pot['absent'])}")
        if tray["TODO"]:
            print(f"  tray_sowing TODO: {sorted(tray['TODO'])}")

    if violations:
        print(f"\nseed_tray_gate: {len(violations)} VIOLATION(S)")
        for x in violations:
            print("  -", x)
        sys.exit(1)
    print("\nseed_tray_gate: PASS (0 violations)")
    sys.exit(0)


if __name__ == "__main__":
    main()
