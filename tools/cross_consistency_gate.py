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

RULE 2 (increment 2) -- harvest-requires-plant: a frost_anchored cell that renders a `harvest`
token must also carry a plant-class token (`plant`/`indoors`); you cannot harvest what was never
planted. Catches the copy-paste that drops the planting tokens. No-op off frost_anchored (trees /
berries plant once at establishment, not in the annual month-strip) and for the herbaceous_perennial
archetype (asparagus's permanent bed).

INCREMENT 2, STILL OPEN (each bottoms out at biology/prose, NOT a clean deterministic gate --
surfaced to Trevor for the LLM-biology-judge layer, not forced here): a `growing` token in a month
the cell's own climate calls hard-frost (needs a per-crop cold-hardiness model -- broccoli/lettuce
grow in cool months legitimately; brushes C14); rotation `family` vs the crop's botanical family
(the `family`/`avoid_after` fields are null on the 18, `good_after` is free-text); a heat_pause
whose prose/sources name a different crop (needs robust crop-name-in-prose detection).
"""
import re

# Plant-class calendar tokens (the annual month-strip): the crop is being established that month.
_PLANT_TOKENS = {"plant", "indoors", "sow", "transplant", "direct_sow", "start_indoors"}

# A pH range: "6.0 to 6.8", "6-7", "5.5 – 6.5". re-audit #2 D12: endpoints may be INTEGER or decimal
# (the old decimal-only predicate let "pH 6 to 7" evade), and the "0 to 14" / "1 to 14" pH-SCALE
# boilerplate is skipped by ITS VALUE (hi >= 12; real soil-pH ranges top out near 8) rather than by
# requiring decimals.
_PH_RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:to|-|–|—)\s*(\d+(?:\.\d+)?)")
_PH_SCALE_HI = 12       # a stated "range" whose high end reaches this is the 0-to-14 pH scale, not a claim
_PH_TOLERANCE = 0.5     # pH units of authoring drift tolerated before it counts as a contradiction


def _stated_ph_range(note):
    """The first REAL pH range in `note` as (lo, hi), or None. Skips the 0/1-to-14 scale boilerplate
    (hi >= _PH_SCALE_HI) so a note that explains the scale before stating the crop's range is read
    correctly."""
    if not isinstance(note, str):
        return None
    for m in _PH_RANGE.finditer(note):
        lo, hi = float(m.group(1)), float(m.group(2))
        if hi < _PH_SCALE_HI:
            return lo, hi
    return None


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

    # RULE 2 -- harvest-requires-plant (frost_anchored ANNUALS only). A herbaceous_perennial
    # (asparagus) is an established permanent bed planted once at establishment, not in the annual
    # month-strip -- the same reason trees/berries are exempt off frost_anchored -- so its steady-
    # state calendar legitimately renders `harvest` (spring spears) with no annual plant token.
    if (crop.get("calendar_basis") == "frost_anchored"
            and crop.get("archetype") != "herbaceous_perennial"):
        for rk, r in (crop.get("regions") or {}).items():
            if not isinstance(r, dict):
                continue
            for z, cell in (r.get("resolved_by_zone") or {}).items():
                if not isinstance(cell, dict):
                    continue
                cal = cell.get("calendar") or []
                if "harvest" in cal and not any(t in _PLANT_TOKENS for t in cal):
                    V.append(f"{rk}.{z}: calendar renders a 'harvest' token but NO plant-class token "
                             f"({sorted(_PLANT_TOKENS)}) -- you cannot harvest what was never planted "
                             f"(a dropped-planting self-contradiction)")
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
