#!/usr/bin/env python3
"""npk_ratio cert-gate branch (Phase A NPK refactor, 2026-06-24). Imported + run by
whole_crop_gate.py. A no-op for any crop with no fertilizer.npk_hint surface.

WHY: the feeding pill (FeedingCard `.fert-npk` + app `ap-npk`) rendered the whole
`npk_hint` PARAGRAPH instead of a ratio (audit F3, all 18 anchors). The fix is a
dedicated render-ready `fertilizer.npk_ratio` -- a bare "N-P-K" string, derived once
from the (already source-verified) hint -- with an explicit-null sentinel + a short
qualitative `npk_tag` for the crops whose feeding is genuinely ratio-less (citrus,
allium, lavender, blueberry). This gate makes "present-or-explicit-null" un-skippable
so the prose-pill bug cannot re-ship at scale.

`npk_ratio` + `npk_tag` are USER-FACING-CATEGORICAL (read identically by both
registers, like `frequency`/`rate`) -- bare, single-form, no _seasoned/_beginner
twin; ruled into register_completeness_gate's EXCLUDED roster.
"""
import re

RATIO_RE = re.compile(r"^\d{1,3}-\d{1,3}-\d{1,3}$")


def npk_ratio_violations(crop):
    """Return a list of violation strings ([] = clean). No-op when the crop has no
    fertilizer.npk_hint surface (nothing renders the pill, so no ratio is demanded)."""
    fert = crop.get("fertilizer")
    if not isinstance(fert, dict):
        return []
    has_hint = bool(fert.get("npk_hint_seasoned")) or bool(fert.get("npk_hint_beginner"))
    if not has_hint:
        return []
    V = []
    if "npk_ratio" not in fert:
        V.append("fertilizer.npk_ratio missing (a crop with an npk_hint must carry a "
                 "render-ready ratio string or explicit null)")
        return V
    ratio = fert.get("npk_ratio")
    if ratio is None:
        tag = fert.get("npk_tag")
        if not (isinstance(tag, str) and tag.strip()):
            V.append("fertilizer.npk_ratio is null but npk_tag is missing/empty (a "
                     "ratio-less crop must carry a short qualitative npk_tag for the pill)")
    elif not (isinstance(ratio, str) and RATIO_RE.match(ratio.strip())):
        V.append(f"fertilizer.npk_ratio malformed: {ratio!r} (want a bare 'N-P-K' "
                 f"string like '5-10-10', or null)")
    return V


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path))
    total = 0
    for c in data["crops"]:
        for v in npk_ratio_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
    print(f"npk_ratio gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
