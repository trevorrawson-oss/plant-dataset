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


# ============ B5: per-register WHY-FILL (every rendered companion carries its why) ============
# A companion that renders in a register but has no `why` for THAT register shows a bare
# name with no reason (apple's why_seasoned:null; carrot omits why_seasoned entirely). The
# card maps:  good_seasoned/bad_seasoned + good_beginner_seasoned/bad_beginner_seasoned ->
# SEASONED;  good_beginner/bad_beginner + the *_beginner_seasoned buckets -> BEGINNER. So a
# both-bucket (*_beginner_seasoned) entry needs BOTH whys; a *_seasoned entry needs
# why_seasoned; a *_beginner entry needs why_beginner. Skips non-dict / nameless entries
# (the shape gate A19 owns those). Does NOT touch reachability -- a beginner-only companion
# is legitimate curation (Trevor 2026-06-25); it just must carry why_beginner.
from companion_shape_gate import companion_why_fill_violations


def why_clean():
    """why-fill-clean: each entry carries the why for every register it renders in."""
    return {"slug": "carrot", "companions": {
        "good_seasoned": [obj("Radishes", why_seasoned="row marker")],
        "good_beginner_seasoned": [obj("Onions", why_seasoned="allium scent masks the carrot",
                                       why_beginner="their smell deters carrot pests")],
        "good_beginner": [obj("Lettuce", why_beginner="quick ground cover between rows")],
        "bad_seasoned": [obj("Dill", why_seasoned="cross-pollinates and stunts roots")],
        "bad_beginner_seasoned": [obj("Fennel", why_seasoned="allelopathic to most crops",
                                      why_beginner="fennel inhibits nearby plants")],
        "bad_beginner": [obj("Parsnip", why_beginner="same pests and diseases as carrot")],
    }}


# W0. fully why-filled -> no violations.
assert companion_why_fill_violations(why_clean()) == [], companion_why_fill_violations(why_clean())

# W1. NO companions block -> no-op.
assert companion_why_fill_violations({"slug": "x"}) == [], "no companions -> no-op"

# W2. a seasoned-bucket entry missing why_seasoned -> violation.
c = why_clean(); c["companions"]["good_seasoned"] = [obj("Radishes", why_seasoned=None)]
v = companion_why_fill_violations(c)
assert any("good_seasoned" in x and "why_seasoned" in x for x in v), v

# W3. a beginner-bucket entry missing why_beginner -> violation.
c = why_clean(); c["companions"]["good_beginner"] = [obj("Lettuce", why_beginner="  ")]
v = companion_why_fill_violations(c)
assert any("good_beginner" in x and "why_beginner" in x for x in v), v

# W4. a BOTH-bucket entry missing why_seasoned (carrot's real shape: has why_beginner only)
#     -> violation on the SEASONED register (it renders seasoned with a bare name).
c = why_clean()
c["companions"]["good_beginner_seasoned"] = [obj("Onions", why_beginner="smell deters pests")]
v = companion_why_fill_violations(c)
assert any("good_beginner_seasoned" in x and "why_seasoned" in x for x in v), v

# W5. a BOTH-bucket entry missing why_beginner -> violation on the BEGINNER register.
c = why_clean()
c["companions"]["bad_beginner_seasoned"] = [obj("Fennel", why_seasoned="allelopathic")]
v = companion_why_fill_violations(c)
assert any("bad_beginner_seasoned" in x and "why_beginner" in x for x in v), v

# W6. non-dict / nameless entries are the shape gate's job -> why-fill SKIPS them (no double-flag).
c = why_clean(); c["companions"]["good_seasoned"] = ["marigolds", {"plant": "Comfrey"}]
assert companion_why_fill_violations(c) == [], companion_why_fill_violations(c)

# W7. REAL DATA: the known why-fill debt (GATE-UNLOCK; back-fill target). apple is flagged;
#     the total across certified is the logged debt. Asserting the exact count locks it -- a
#     back-fill that closes some MUST update this number (that is the unlock signal).
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    import json
    _data = json.load(open(_path))
    _cert = [c for c in _data["crops"]
             if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    _total = sum(len(companion_why_fill_violations(c)) for c in _cert)
    _apple = next(c for c in _cert if c["slug"] == "apple")
    assert companion_why_fill_violations(_apple), "apple should have why-fill gaps"
    assert _total == 59, ("known companion why-fill debt changed (update after back-fill)", _total)
    print(f"  companion_why_fill_violations: {_total} known render gaps across certified (GATE-UNLOCK): PASS")

print("companion_shape_gate: why-fill tests passed")


# ============ B5: companion EVIDENCE TRANSPARENCY (decision a, Trevor 2026-06-25) ============
# Every companion (good OR bad) must declare its evidence honestly: an `evidence_label` in the
# ruled enum + a `confidence` in {low,medium,high}. This is the transparency bar -- a
# speculative-but-LABELED pairing (mechanistic/low) is allowed (beginners keep folk-wisdom
# companions); an UNLABELED one is not. Skips non-dict / nameless entries (shape gate A19).
from companion_shape_gate import companion_evidence_violations, EVIDENCE_LABELS, EVIDENCE_CONFIDENCE


def ev(name, label="traditional", confidence="medium", **kw):
    return {"name": name, "evidence_label": label, "confidence": confidence, **kw}


def evidence_clean():
    return {"slug": "carrot", "companions": {
        "good_seasoned": [ev("Radishes", "extension_backed", "high")],
        "good_beginner_seasoned": [ev("Onions", "traditional", "medium")],
        "bad_seasoned": [ev("Dill", "mechanistic", "low")],
        "bad_beginner_seasoned": [ev("Fennel", "research_backed", "high")],
    }}


# V0. all entries carry a valid label + confidence -> no violations.
assert companion_evidence_violations(evidence_clean()) == [], companion_evidence_violations(evidence_clean())

# V1. NO companions -> no-op.
assert companion_evidence_violations({"slug": "x"}) == [], "no companions -> no-op"

# V2. missing evidence_label (the 77-entry debt: key absent) -> violation.
c = evidence_clean(); c["companions"]["good_seasoned"] = [{"name": "Radishes", "confidence": "high"}]
v = companion_evidence_violations(c)
assert any("good_seasoned" in x and "evidence_label" in x for x in v), v

# V3. an evidence_label outside the enum -> violation.
c = evidence_clean(); c["companions"]["good_seasoned"] = [ev("Radishes", "folk_wisdom", "high")]
v = companion_evidence_violations(c)
assert any("evidence_label" in x and "folk_wisdom" in x for x in v), v

# V4. missing confidence -> violation.
c = evidence_clean(); c["companions"]["good_seasoned"] = [{"name": "Radishes", "evidence_label": "traditional"}]
v = companion_evidence_violations(c)
assert any("good_seasoned" in x and "confidence" in x for x in v), v

# V5. a confidence outside {low,medium,high} -> violation.
c = evidence_clean(); c["companions"]["good_seasoned"] = [ev("Radishes", "traditional", "maybe")]
v = companion_evidence_violations(c)
assert any("confidence" in x and "maybe" in x for x in v), v

# V6. a labeled-but-speculative pairing (mechanistic/low) is ALLOWED (decision a) -> clean.
c = evidence_clean(); c["companions"]["good_seasoned"] = [ev("Tomatoes", "mechanistic", "low")]
assert companion_evidence_violations(c) == [], companion_evidence_violations(c)

# V7. non-dict / nameless entries are the shape gate's job -> skipped here.
c = evidence_clean(); c["companions"]["good_seasoned"] = ["marigolds", {"plant": "Comfrey"}]
assert companion_evidence_violations(c) == [], companion_evidence_violations(c)

# V8. the enums are the ruled vocab.
assert EVIDENCE_LABELS == {"traditional", "extension_backed", "research_backed",
                           "likely", "mechanistic", "disputed"}, EVIDENCE_LABELS
assert EVIDENCE_CONFIDENCE == {"low", "medium", "high"}, EVIDENCE_CONFIDENCE

# V9. REAL DATA: the known evidence-transparency debt (GATE-UNLOCK; back-fill target).
if os.path.exists(_path):
    _ev_total = sum(len(companion_evidence_violations(c)) for c in _cert)
    assert _ev_total == 159, ("known companion evidence debt changed (update after back-fill)", _ev_total)
    print(f"  companion_evidence_violations: {_ev_total} known label/confidence gaps (GATE-UNLOCK): PASS")

print("companion_shape_gate: evidence tests passed")
