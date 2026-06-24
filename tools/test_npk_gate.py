#!/usr/bin/env python3
"""Tests for the npk_ratio cert-gate branch (Phase A NPK refactor, 2026-06-24).
Run: python3 tools/test_npk_gate.py

The pill bug (audit F3): the FeedingCard / app pill printed the whole `npk_hint`
PARAGRAPH instead of the N-P-K ratio. The fix surfaces a dedicated, render-ready
`fertilizer.npk_ratio` (a bare "N-P-K" string) with an explicit-null sentinel for
the crops whose feeding guidance is qualitative (citrus, alliums, lavender,
blueberry); those carry a short `npk_tag` instead. This gate makes the field
present-or-explicit-null un-skippable at cert + scale.

Contract (npk_ratio_violations):
  - NO-OP when the crop has no fertilizer.npk_hint surface (indoor microgreens):
    nothing renders the pill, so no ratio is demanded.
  - When a crop HAS an npk_hint, `npk_ratio` MUST be a present key:
      * a bare ratio string matching \\d+-\\d+-\\d+ (e.g. "5-10-10"), OR
      * explicit null AND a non-empty `npk_tag` (the qualitative fallback the
        pill degrades to).
  - A missing key, a malformed ratio, or null-without-tag is a violation.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from npk_gate import npk_ratio_violations


def with_ratio():
    return {"slug": "cherry-tomato",
            "fertilizer": {"npk_hint_seasoned": "high K, e.g. 5-10-10 or 8-32-16",
                           "npk_ratio": "5-10-10"}}


def ratioless():
    return {"slug": "lemon",
            "fertilizer": {"npk_hint_seasoned": "Nitrogen-forward citrus feed.",
                           "npk_ratio": None, "npk_tag": "Nitrogen-forward"}}


# 0. a well-formed ratio crop -> clean
assert npk_ratio_violations(with_ratio()) == [], npk_ratio_violations(with_ratio())

# 1. a ratio-less crop with explicit null + a tag -> clean
assert npk_ratio_violations(ratioless()) == [], npk_ratio_violations(ratioless())

# 2. NO fertilizer block at all -> no-op
assert npk_ratio_violations({"slug": "x"}) == [], "no fertilizer -> no-op"

# 3. a fertilizer block with NO npk_hint (indoor microgreens) -> no-op even without npk_ratio
assert npk_ratio_violations({"slug": "microgreens-mix",
                             "fertilizer": {"type": "none", "frequency": "none"}}) == [], \
    "no npk_hint surface -> no-op"

# 4. has npk_hint but npk_ratio key MISSING -> violation
c = with_ratio(); del c["fertilizer"]["npk_ratio"]
assert any("npk_ratio" in v and "missing" in v.lower() for v in npk_ratio_violations(c)), npk_ratio_violations(c)

# 5. malformed ratio (prose left in the field) -> violation
c = with_ratio(); c["fertilizer"]["npk_ratio"] = "high K such as 5-10-10"
assert any("malformed" in v.lower() for v in npk_ratio_violations(c)), npk_ratio_violations(c)

# 6. explicit null but NO tag -> violation (ratio-less crops must carry the qualitative fallback)
c = ratioless(); del c["fertilizer"]["npk_tag"]
assert any("npk_tag" in v for v in npk_ratio_violations(c)), npk_ratio_violations(c)

# 7. explicit null with an EMPTY tag -> violation
c = ratioless(); c["fertilizer"]["npk_tag"] = "   "
assert any("npk_tag" in v for v in npk_ratio_violations(c)), npk_ratio_violations(c)

# 8. the npk_hint can live on the BEGINNER key alone and still demand a ratio
c = {"slug": "y", "fertilizer": {"npk_hint_beginner": "use a balanced 10-10-10 feed"}}
assert any("npk_ratio" in v and "missing" in v.lower() for v in npk_ratio_violations(c)), npk_ratio_violations(c)

# 9. valid 3-digit phosphate ratio (e.g. 18-46-0 DAP) accepted
c = with_ratio(); c["fertilizer"]["npk_ratio"] = "18-46-0"
assert npk_ratio_violations(c) == [], npk_ratio_violations(c)

print("npk_gate: all tests passed")
