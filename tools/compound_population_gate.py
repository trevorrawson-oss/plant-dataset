#!/usr/bin/env python3
"""Consumer-compound population gate (whole_crop_gate A12) -- closes the truthy-but-empty trap
AND the tips rendering-conformance traps (wrong field, orphaned keys).

A consumer compound can be PRESENT yet carry ZERO authored content and still pass every other
gate: an empty list, or a dict of empty lists (`{"established": [], "harvest": []}`), which is
TRUTHY and whose key-count reads non-empty. `register_fill_gate` (pairs) and
`register_completeness_gate` (unruled keys) are both blind to it.

`tips_by_stage` carries THREE distinct rendering traps the generic emptiness check misses, all
found 2026-06-21 across 7 certified crops:
  1. EMPTY        -- no tips at all (lemon, orange, strawberry).
  2. WRONG FIELD  -- tips authored as `tip_seasoned`/`tip_beginner`; the GrowingJourneyCard reads
                     `text_seasoned`/`text_beginner`, so they are invisible (onion).
  3. ORPHANED KEY -- a tip keyed to a stage id that is NOT in `growth_stages`; the renderer does
                     `tipsByStage[stage.id]`, so it is never grabbed (carrot/peach/apple/onion).
INDOOR crops (`non_seasonal_indoor`) carry their tip in `indoor_cycle.tip_*` (rendered by the
IndoorCycleCard, gated by A6) and intentionally do NOT use `tips_by_stage` -- they are EXEMPT.

`empty_compound_violations` + `tips_violations` -> [] each = clean. Both flip-blocking.
"""

# Consumer compounds every complete crop must carry with real content. (tips_by_stage handled
# separately by tips_violations -- it has richer conformance rules + an indoor exemption.)
REQUIRED_ALWAYS = (
    "growth_stages", "notifications", "pests", "diseases", "failure_diagnostics",
)
# Required except where the archetype makes it N/A.
REQUIRED_OUTDOOR_ONLY = ("weather_triggers",)


def content_count(v):
    """Real authored-item count, recursing the trap shapes. None = field absent."""
    if v is None:
        return None
    if isinstance(v, list):
        return len(v)
    if isinstance(v, dict):
        if v and all(isinstance(x, list) for x in v.values()):
            return sum(len(x) for x in v.values())          # dict-of-lists (the tips_by_stage trap)
        return sum(1 for x in v.values() if x)               # dict-of-values
    return 1 if v else 0


def empty_compound_violations(crop):
    V = []
    is_indoor = crop.get("calendar_basis") == "non_seasonal_indoor"
    required = list(REQUIRED_ALWAYS)
    if not is_indoor:
        required += list(REQUIRED_OUTDOOR_ONLY)
    for f in required:
        n = content_count(crop.get(f))
        if n is None:
            V.append(f"{f}: absent (required consumer compound has no content)")
        elif n == 0:
            V.append(f"{f}: present but EMPTY (truthy-but-zero -- recurse caught no authored content)")
    return V


def _growth_stage_ids(crop):
    return {g.get("id") or g.get("stage_id") for g in (crop.get("growth_stages") or [])
            if isinstance(g, dict)}


def tips_violations(crop):
    """tips_by_stage rendering conformance: non-empty + text_ shape + keyed to real growth stages.
    Indoor crops are EXEMPT (their tip surface is indoor_cycle.tip_*, gated by A6)."""
    if crop.get("calendar_basis") == "non_seasonal_indoor":
        return []
    V = []
    tbs = crop.get("tips_by_stage")
    if not isinstance(tbs, dict):
        return [f"tips_by_stage: absent or not a dict ({type(tbs).__name__})"]
    total = sum(len(v) for v in tbs.values() if isinstance(v, list))
    if total == 0:
        V.append("tips_by_stage: present but EMPTY -- no authored tips")
    gids = _growth_stage_ids(crop)
    for key, lst in tbs.items():
        if not isinstance(lst, list) or not lst:
            continue
        if key not in gids:
            V.append(f"tips_by_stage['{key}']: ORPHANED key (not a growth_stage id) -- "
                     f"renderer reads tipsByStage[stage.id], so these tips never render")
        for t in lst:
            if isinstance(t, dict) and "text_seasoned" not in t:
                wrong = sorted(k for k in t if k.endswith("_seasoned")) or ["<none>"]
                V.append(f"tips_by_stage['{key}']: tip uses {wrong}, not text_seasoned -- "
                         f"the renderer reads text_seasoned/text_beginner (invisible otherwise)")
                break
    return V
