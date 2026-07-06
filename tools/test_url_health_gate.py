#!/usr/bin/env python3
"""Tests for the offline non-null-URL gate (post-114 §B, offline half). Run:
    python3 tools/test_url_health_gate.py

WHY: a cited source whose anchoring url is null resolves to nothing. The LIVE layers (regions{} +
claim/top) must carry non-null urls; the legacy zones{} layer is excluded (matches gate F scoping).
OFFLINE only -- liveness (404/redirect) is a separate --online sweep.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from url_health_gate import url_health_violations

def crop(**kw):
    return dict(slug="x", **kw)

# 1. a regions{} anchoring url that is null -> violation
c = crop(regions={"se_gulf": {"anchoring_urls": {"ncsu_ext": {"url": None, "verified": "2026-07-06"}}}})
assert any("ncsu_ext" in v for v in url_health_violations(c)), url_health_violations(c)

# 2. a top-level/claim anchoring url that is empty -> violation
c = crop(storage={"anchoring_urls": {"psu_ext": {"url": "", "verified": "2026-07-06"}}})
assert any("psu_ext" in v for v in url_health_violations(c)), url_health_violations(c)

# 3. a legacy zones{} null url -> NOT flagged (excluded)
c = crop(zones={"8": {"anchoring_urls": {"uga_b577": {"url": None}}}})
assert url_health_violations(c) == [], url_health_violations(c)

# 4. all live-layer urls present -> clean
c = crop(regions={"se_gulf": {"anchoring_urls": {"ncsu_ext": {"url": "https://x/", "verified": "2026-07-06"}}}},
         storage={"anchoring_urls": {"psu_ext": {"url": "https://y/", "verified": "2026-07-06"}}})
assert url_health_violations(c) == [], url_health_violations(c)

print("url_health_gate tests: OK")
