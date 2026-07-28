#!/usr/bin/env python3
"""carveout_dependency_audit -- which cells actually DEPEND on the herbaceous_perennial carve-outs?

WHY THIS EXISTS. Three gates carry an exemption scoped to `archetype == 'herbaceous_perennial'`:

  A24  annual_calendar.annual_calendar_violations       -- frost/cold_pause on a plant_out month
  A34  cross_consistency_gate (rule 2)                  -- `harvest` token with no plant-class token
  A37  calendar_coherence_gate.growing_reachability     -- `growing` unreachable from a plant token

Each was justified for ASPARAGUS specifically: a DORMANT CROWN goes in while the ground is cold
(A24), an established permanent bed is planted once and not in the annual month-strip (A34), and
the summer fern legitimately grows after the spring spear harvest (A37).

Moving a second crop onto the archetype INHERITS all three silently. That is the asparagus failure
mode restated: a defensible modeling call whose field-level consequences go unverified. Artichoke
in particular does NOT plant a dormant crown in cold zones -- it sets out a live, vernalized
transplant -- so A24's justification does not transfer by analogy even though the exemption does.

WHAT THIS DOES. Runs each of the three violation functions twice: once on the crop as-is, and once
on a copy whose `archetype` is masked to a sentinel. Each module reads `archetype` in exactly one
place (verified: one comparison per module), and only for the carve-out, so masking it disables the
exemption and nothing else -- `calendar_basis` is untouched, so all three gates still run in full.

The DIFF is the answer: the exact set of violations the carve-out is suppressing. A cell in that
diff is a cell whose correctness rests on the exemption, and it must be justified in prose. A cell
NOT in the diff passes the gate on its own merits, and the exemption is a no-op for it.

Read the output as: "if this crop were not a herbaceous_perennial, these are the things that would
be reported." Anything listed must have a written agronomic reason.

Usage:
  python3 tools/carveout_dependency_audit.py <slug> [crops_data_final.json]
  python3 tools/carveout_dependency_audit.py --all [crops_data_final.json]

Exit 0 always -- this is a DIAGNOSTIC, not a gate. It reports; a human rules.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from annual_calendar import annual_calendar_violations
from calendar_coherence_gate import growing_reachability_violations
from cross_consistency_gate import cross_consistency_violations

# Any value that is not "herbaceous_perennial" disables the carve-out. A sentinel makes it obvious
# in a traceback that this is a probe and not a real archetype.
MASK = "__carveout_probe__"

CHECKS = (
    ("A24", "frost/cold pause on a plant_out month (dormant-planting carve-out)",
     annual_calendar_violations),
    ("A34", "harvest token with no plant-class token (planted-once carve-out)",
     cross_consistency_violations),
    ("A37", "growing unreachable from a plant token (grows-after-harvest carve-out)",
     growing_reachability_violations),
)


def audit(crop):
    """Return {check_id: [violations suppressed by the archetype carve-out]}.

    A violation is 'suppressed' if it appears with the archetype masked but not with it real.
    Compared as strings, so a violation that survives both runs (a genuine defect the carve-out
    does NOT cover) is correctly excluded -- that one is A-numbered gate business, not ours.
    """
    masked = copy.deepcopy(crop)
    masked["archetype"] = MASK
    out = {}
    for cid, _desc, fn in CHECKS:
        real = set(fn(crop))
        without = set(fn(masked))
        out[cid] = sorted(without - real)
    return out


def report(crop, verbose=True):
    """Print the audit for one crop. Returns the total number of suppressed violations."""
    slug = crop.get("slug")
    arch = crop.get("archetype")
    res = audit(crop)
    total = sum(len(v) for v in res.values())
    print(f"\n=== {slug} (archetype={arch!r}, calendar_basis={crop.get('calendar_basis')!r}) ===")
    if arch != "herbaceous_perennial":
        print("  NOTE: not on the herbaceous_perennial archetype -- the carve-outs are already")
        print("        inactive for this crop, so a non-zero count below is what it WOULD depend")
        print("        on if it were moved onto the archetype.")
    for cid, desc, _fn in CHECKS:
        hits = res[cid]
        print(f"  {cid}: {len(hits):3d} cell(s) depend on the carve-out -- {desc}")
        if verbose:
            for m in hits:
                print(f"       - {m}")
    print(f"  TOTAL carve-out-dependent violations: {total}")
    return total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_all = "--all" in sys.argv
    path = args[-1] if args and args[-1].endswith(".json") else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    if do_all:
        grand = 0
        for c in data["crops"]:
            if c.get("archetype") == "herbaceous_perennial":
                grand += report(c, verbose=True)
        print(f"\nherbaceous_perennial crops audited; {grand} carve-out-dependent violation(s) total")
        return 0
    if not args:
        print(__doc__)
        return 0
    slug = args[0]
    crop = next((c for c in data["crops"] if c.get("slug") == slug), None)
    if crop is None:
        print(f"no such crop: {slug}")
        return 0
    report(crop, verbose=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
