#!/usr/bin/env python3
"""Tests for the companion-shape cert-gate branch (Phase B, audit F4/F6, 2026-06-24).
Run: python3 tools/test_companion_shape_gate.py

Two render defects this gate arms against, both found in the 2026-06-24 audit:
  F4 -- BARE-STRING entries. A companion stored as a bare string (e.g. "marigolds")
        instead of the certified object {name, ...} is silently DROPPED by
        CompanionsCard.normCompanions (it spreads the string, finds no .name, filters
        it out), so the row renders as NOTHING. Hit lemon/orange/basil/green-beans.
  F6 -- GOODS HIDDEN FROM SEASONED MODE. Companions placed only in the beginner-only
        bucket (good_beginner / bad_beginner) never render in seasoned mode, because the
        card maps good_seasoned + good_beginner_seasoned -> seasoned-readable and
        good_beginner -> beginner-only. Hit apple (all its goods + bads beginner-only).

Contract (companion_shape_violations):
  - NO-OP when the crop carries no `companions` dict.
  - Every entry in every bucket MUST be a dict carrying a non-empty `name` (the certified
    object shape; a bare string or a legacy `plant`-keyed entry with no `name` is rejected).
  - If the crop has ANY good entries, the seasoned-readable good buckets
    (good_seasoned UNION good_beginner_seasoned) must be non-empty. Same for bad.
    (A crop with zero goods -- e.g. a tree whose companion advice is all "keep X away" --
    is vacuously clean on the goods rule.)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from companion_shape_gate import companion_shape_violations


def obj(name, **kw):
    return {"name": name, **kw}


def clean_crop():
    """The certified carrot/onion shape: rich seasoned objects + {name, why_beginner}
    both-bucket objects; the legacy beginner-only buckets empty."""
    return {"slug": "carrot", "companions": {
        "good_seasoned": [obj("Radishes", why_seasoned="row marker")],
        "good_beginner_seasoned": [obj("Onions", why_beginner="smell deters pests")],
        "good_beginner": [],
        "bad_seasoned": [obj("Dill", why_seasoned="cross-pollinates")],
        "bad_beginner_seasoned": [obj("Fennel", why_beginner="inhibitory")],
        "bad_beginner": [],
    }}


# 0. the certified clean shape -> no violations
assert companion_shape_violations(clean_crop()) == [], companion_shape_violations(clean_crop())

# 1. NO companions block -> no-op (indoor microgreens carry none)
assert companion_shape_violations({"slug": "microgreens-mix"}) == [], "no companions -> no-op"

# 2. a BARE STRING in a good bucket -> violation (F4)
c = clean_crop(); c["companions"]["good_seasoned"] = ["marigolds"]
v = companion_shape_violations(c)
assert any("good_seasoned" in x and ("string" in x.lower() or "object" in x.lower()) for x in v), v

# 3. a BARE STRING in a bad bucket -> violation (F4, lemon's bad_seasoned)
c = clean_crop(); c["companions"]["bad_seasoned"] = ["turfgrass within the drip line"]
v = companion_shape_violations(c)
assert any("bad_seasoned" in x for x in v), v

# 4. an object with NO name (apple's legacy `plant`-keyed entry) -> violation
c = clean_crop()
c["companions"]["good_seasoned"] = [{"plant": "Comfrey", "why": "mulch"}]
v = companion_shape_violations(c)
assert any("good_seasoned" in x and "name" in x.lower() for x in v), v

# 5. an object with an EMPTY name -> violation
c = clean_crop(); c["companions"]["good_seasoned"] = [obj("   ", why_seasoned="x")]
assert any("name" in x.lower() for x in companion_shape_violations(c)), companion_shape_violations(c)

# 6. goods ONLY in the beginner-only bucket -> violation (F6, apple)
c = clean_crop()
c["companions"]["good_seasoned"] = []
c["companions"]["good_beginner_seasoned"] = []
c["companions"]["good_beginner"] = [obj("Garlic", why_beginner="pollination partner")]
v = companion_shape_violations(c)
assert any("good" in x and "seasoned" in x.lower() for x in v), v

# 7. bads ONLY in the beginner-only bucket -> violation (F6, apple bads)
c = clean_crop()
c["companions"]["bad_seasoned"] = []
c["companions"]["bad_beginner_seasoned"] = []
c["companions"]["bad_beginner"] = [obj("Black walnut", why_beginner="juglone")]
v = companion_shape_violations(c)
assert any("bad" in x and "seasoned" in x.lower() for x in v), v

# 8. goods reachable via good_beginner_seasoned ALONE (both-bucket) -> clean
c = clean_crop()
c["companions"]["good_seasoned"] = []
# good_beginner_seasoned still has Onions -> seasoned mode sees it
assert companion_shape_violations(c) == [], companion_shape_violations(c)

# 9. a legit beginner-only EXTRA is fine when the seasoned bucket is also populated
c = clean_crop()
c["companions"]["good_beginner"] = [obj("Lettuce", why_beginner="ground cover")]
assert companion_shape_violations(c) == [], companion_shape_violations(c)

# 10. a crop with ZERO goods (tree: only "keep X away") is vacuously clean on the goods rule
c = clean_crop()
for b in ("good_seasoned", "good_beginner_seasoned", "good_beginner"):
    c["companions"][b] = []
assert companion_shape_violations(c) == [], companion_shape_violations(c)

# 11. companions present but NOT a dict (defensive) -> no-op (the dual-voice/other gates own that)
assert companion_shape_violations({"slug": "x", "companions": []}) == [], "non-dict companions -> no-op"

print("companion_shape_gate: all tests passed")
