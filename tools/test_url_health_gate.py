#!/usr/bin/env python3
"""Tests for the offline non-null-URL gate (post-114 §B, offline half). Run:
    python3 tools/test_url_health_gate.py

WHY: a cited source whose anchoring url is null resolves to nothing. The LIVE layers (regions{} +
claim/top) must carry non-null urls; the legacy zones{} layer is excluded (matches gate F scoping).
OFFLINE only -- liveness (404/redirect) is a separate --online sweep.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from url_health_gate import url_health_violations, online_violations

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

print("url_health_gate (offline) tests: OK")


# ---------------------------------------------------------------------------
# --online mode (post-114 §B, online half). A liveness LEDGER (produced out of
# band by the WebFetch sweep, committed as the record) maps url -> verdict; an
# entry with `offender: true` is a hard-dead url (404 / logo-pdf / redirect-loop).
# online_violations flags any LIVE-layer anchoring url that the ledger marks a
# hard offender. Same scoping as the offline gate: legacy zones{} is EXCLUDED.
# ---------------------------------------------------------------------------
DEAD = "https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf"
LEDGER = {
    DEAD: {"status": "logo-pdf", "offender": True},
    "https://ucanr.edu": {"status": "bare-live", "offender": "role-dependent"},
    "https://extensionpublications.unl.edu/x.htm": {"status": "redirect-live", "offender": "soft"},
    "https://good.edu/live/": {"status": "live", "offender": False},
}

# 5. a LIVE-layer (regions) url that the ledger marks a hard offender -> violation
c = crop(regions={"se_gulf": {"anchoring_urls": {"uga_ext": {"url": DEAD}}}})
assert any("uga_ext" in v for v in online_violations(c, LEDGER)), online_violations(c, LEDGER)

# 6. a claim/top-level url marked offender -> violation
c = crop(storage={"anchoring_urls": {"uga_ext": {"url": DEAD}}})
assert any("uga_ext" in v for v in online_violations(c, LEDGER)), online_violations(c, LEDGER)

# 7. the SAME dead url in a legacy zones{} cell -> NOT flagged (zones excluded)
c = crop(zones={"8": {"anchoring_urls": {"uga_ext": {"url": DEAD}}}})
assert online_violations(c, LEDGER) == [], online_violations(c, LEDGER)

# 8. a bare-live (role-dependent) or soft-redirect url -> NOT a hard violation
c = crop(regions={"ca": {"anchoring_urls": {"ucanr_ext": {"url": "https://ucanr.edu"},
                                            "unl": {"url": "https://extensionpublications.unl.edu/x.htm"}}}})
assert online_violations(c, LEDGER) == [], online_violations(c, LEDGER)

# 9. a url not present in the ledger -> not flagged (unverified != dead)
c = crop(regions={"ca": {"anchoring_urls": {"x": {"url": "https://unseen.edu/page/"}}}})
assert online_violations(c, LEDGER) == [], online_violations(c, LEDGER)

# 10. all live-layer urls live / absent -> clean
c = crop(regions={"ca": {"anchoring_urls": {"g": {"url": "https://good.edu/live/"}}}})
assert online_violations(c, LEDGER) == [], online_violations(c, LEDGER)

print("url_health_gate (online) tests: OK")
