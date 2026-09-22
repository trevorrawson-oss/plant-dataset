#!/usr/bin/env python3
"""container_citation_floor_gate -- the PLA-533 RATCHET on uncited container pot sizes.

THE RULE (Trevor, 2026-09-22, ruling 1 on PLA-533):

    The count of CERTIFIED crops carrying a non-null `container_notes.min_pot_gallons` with no
    `sources` or no anchoring URL may go DOWN, never UP.

Armed at **4** on canonical 526788f2, where it is GREEN. It does not wait for those four to be
re-sourced; it arms now so the population cannot grow while PLA-533's audit runs.

WHY IT IS NOT SECTION F, AND WHY SECTION F CANNOT DO THIS. §F asks "did you anchor what you
CITED?" -- its walk fires only on a NON-EMPTY `sources` list, so emptying `sources` makes it
QUIETER rather than louder. Measured on a scratch copy of cabbage: the claim-bearing leaf count
drops 147 -> 146 and the gate still PASSES. A gate that gets greener as you cite less cannot floor
coverage. This gate asks the other question -- "should this number have been cited?" -- which is a
COVERAGE FLOOR in the A57 / A59 pattern.

WHY ROSTER-LEVEL AND NOT A whole_crop_gate A-NUMBER. A ratchet is a property of a COUNT, and a
per-crop gate cannot see a count. A per-crop version would also have to be RED on the four today,
which is exactly what the ruling rejected: armed green, it stops the growth now instead of after
the audit.

THE SET IS PINNED AS WELL AS THE COUNT. A count-only ratchet is defeatable by SUBSTITUTION: close
one, break another, the count is still 4 and a pure count check passes. So the violation is "an
uncited crop that is not one of the KNOWN four", which catches growth AND substitution while
permitting shrinkage automatically -- the ruled direction, preserved exactly. The count ceiling is
asserted too, as a second and independent statement of the same rule.

CLOSING ONE. When a crop is re-sourced, remove it from KNOWN and drop CEILING by one, in the same
commit as the data change. The gate passes at the lower count WITHOUT that edit (shrinkage is
never a violation); the edit is what stops it being re-broken later.

SCOPE, deliberately narrow. Only `min_pot_gallons`, only on CERTIFIED crops, only when it is
non-null. A crop that states no pot size makes no claim to cite: 8 certified crops carry an empty
`container_notes.sources` with all-null numerics and are legitimately silent. Widening this to
every `container_notes` numeric, or to the general §F skip, is separate work -- §F's defect is
general and is scoped on its own (PLA-533 ruling 2).

Usage: container_citation_floor_gate.py [PATH]
"""
import json
import sys

FIELD = "min_pot_gallons"
CERTIFIED = "verified_gs_arc"

# MEASURED 2026-09-22 on canonical 526788f2, enumerated as literals and never computed from the
# scan they bound -- a ceiling derived from the thing it limits would "hold" at any value.
# 102 of the 121 certified crops carry a min_pot_gallons; 98 are cited; these 4 are not.
CEILING = 4
KNOWN = (
    "dry-bean",           # 5 gal (also recommended 5, depth 8) -- sibling of green-beans-bush
    "green-beans-bush",   # 5 gal (also recommended 5, depth 8) -- found via PLA-580's slice
    "grapefruit",         # 20 gal -- sibling of orange-navel
    "orange-navel",       # 15 gal
)


def _cn(crop):
    v = crop.get("container_notes")
    return v if isinstance(v, dict) else {}


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def is_uncited(crop):
    """A certified crop that states a pot size with no citation behind it.

    'no sources OR no anchoring URL' -- either half missing means uncited, because a source id
    with no URL cannot be opened and a URL with no source id is not admitted through the catalog.
    """
    if not _certified(crop):
        return False
    cn = _cn(crop)
    if cn.get(FIELD) is None:
        return False
    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})


def uncited(data):
    return sorted(c["slug"] for c in data.get("crops", []) if is_uncited(c))


def violations(data):
    V = []
    live = uncited(data)
    for slug in live:
        if slug not in KNOWN:
            V.append(f"{slug}: states container_notes.{FIELD} with no sources and/or no anchoring "
                     f"url, and is NOT one of the {CEILING} known uncited crops. The PLA-533 floor "
                     f"is a RATCHET: this population may shrink, never grow. Cite the figure, or "
                     f"(if this is a deliberate, recorded exception) add it to KNOWN and raise "
                     f"CEILING in the same commit, with the reason.")
    if len(live) > CEILING:
        V.append(f"uncited {FIELD} population is {len(live)}, ratchet ceiling is {CEILING}: "
                 f"{live}")
    return V


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    V = violations(data)
    live = uncited(data)
    for v in V:
        print("VIOLATION:", v)
    certified = [c for c in data.get("crops", []) if _certified(c)]
    stating = [c for c in certified if _cn(c).get(FIELD) is not None]
    print(f"container_citation_floor_gate: {len(V)} violation(s); "
          f"{len(live)}/{CEILING} uncited (ratchet ceiling {CEILING}); "
          f"{len(stating) - len(live)} of {len(stating)} certified crops stating a {FIELD} are cited")
    if live:
        print("  uncited: " + ", ".join(live))
    closed = sorted(set(KNOWN) - set(live))
    if closed:
        print(f"  CLOSED since arming ({len(closed)}): " + ", ".join(closed)
              + " -- drop from KNOWN and lower CEILING in the commit that cites them")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
