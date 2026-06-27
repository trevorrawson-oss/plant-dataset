#!/usr/bin/env python3
"""Cross-consistency truth-layer gate -- the deterministic cross-field layer of the C7 defense
(whole_crop_gate A34; incognito-redteam 2026-06-27, Trevor: build deterministic first).

The most likely bot failure mode (C7, "rutabaga that is basil verbatim") is copy-nearest-template
and forget to refit -- so the crop contradicts ITSELF, catchable WITHOUT external truth. The
canonical example: the fabricated crop's PROSE said pH 6.0-7.5 while structured `ph.preferred_range`
was [3.0, 3.4]. This gate cross-checks fields that must agree.

RULE 1 (this increment) -- pH prose vs structured range: the FIRST decimal pH range stated in
`ph.note_seasoned` / `ph.note_beginner` must match `ph.preferred_range` within 0.5 pH units (every
certified anchor states it exactly; the tolerance leaves room for authoring drift so the gate fires
only on a real contradiction). The decimal-required parse skips the "0 to 14 scale" boilerplate and
single-value mentions ("around pH 6.5").

INCREMENT 2 (designed, not yet built -- each needs its own 0-FP pass): harvest-before-plant in a
cell's calendar; a `growing` token in a month the cell's own climate calls hard-frost; rotation
`family` vs the crop's botanical family; a heat_pause whose prose/sources name a different crop.
"""
import re

# A decimal-bearing range: "6.0 to 6.8", "6.0-6.8", "5.5 – 6.5". BOTH endpoints must carry a decimal
# point, so the "0 to 14" pH-scale boilerplate and bare integers are never mistaken for the range.
_PH_RANGE = re.compile(r"(\d+\.\d+)\s*(?:to|-|–|—)\s*(\d+\.\d+)")
_PH_TOLERANCE = 0.5  # pH units of authoring drift tolerated before it counts as a contradiction


def _stated_ph_range(note):
    """The first decimal pH range in `note` as (lo, hi), or None if absent/unparseable."""
    if not isinstance(note, str):
        return None
    m = _PH_RANGE.search(note)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def cross_consistency_violations(crop):
    """Return a list ([] = clean) of cross-field contradictions (no external truth required)."""
    V = []
    ph = crop.get("ph") or {}
    pref = ph.get("preferred_range")
    if isinstance(pref, list) and len(pref) == 2 and all(isinstance(x, (int, float)) for x in pref):
        for reg in ("note_seasoned", "note_beginner"):
            stated = _stated_ph_range(ph.get(reg))
            if stated is None:
                continue
            if (abs(stated[0] - pref[0]) > _PH_TOLERANCE
                    or abs(stated[1] - pref[1]) > _PH_TOLERANCE):
                V.append(f"ph.{reg} states pH {stated[0]}-{stated[1]} but ph.preferred_range is "
                         f"{pref} (disagree by > {_PH_TOLERANCE}); the prose and the rendered Hero "
                         f"pH stat contradict each other")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        vs = cross_consistency_violations(c)
        if vs:
            print(f"  {c.get('slug')}:")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"cross_consistency gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
