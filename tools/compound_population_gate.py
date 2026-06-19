#!/usr/bin/env python3
"""Consumer-compound population gate (whole_crop_gate A12) -- closes the truthy-but-empty trap.

A consumer compound can be PRESENT yet carry ZERO authored content and still pass every other
gate: an empty list (`[]`), or -- the trap that shipped lemon/orange/strawberry with no tips --
a dict of empty lists (`{"established": [], "harvest": []}`), which is TRUTHY and whose key-count
reads non-empty. register_fill_gate (pairs) and register_completeness_gate (unruled keys) are
both blind to it. This gate recurses into the value and flags any required consumer compound
whose REAL content count is zero.

Archetype carve-out: indoor crops (`non_seasonal_indoor`) have no frost/heat exposure, so
`weather_triggers` is legitimately N/A for them and is not required.

`empty_compound_violations(crop) -> list[str]` ([] = clean). Flip-blocking (wired into
whole_crop_gate). Found 2026-06-19: tips_by_stage shipped empty on 3 certified crops, undetected.
"""

# Consumer compounds every complete crop must carry with real content.
REQUIRED_ALWAYS = (
    "tips_by_stage", "growth_stages", "notifications",
    "pests", "diseases", "failure_diagnostics",
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
