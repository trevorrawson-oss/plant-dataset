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


# ---------------------------------------------------------------------------
# --online COVERAGE (PLA-156 owed #3). The ledger covers a handful of the
# live-layer urls; absence from it must never read as clean. `0 known-dead`
# over an unmeasured ledger is indistinguishable from `0 known-dead` over a
# complete one -- so the gate must REPORT its denominator: how many distinct
# LIVE-layer urls have a ledger verdict vs. are UNMEASURED. Exit code stays
# violation-driven (unmeasured is blindness, not a defect).
# ---------------------------------------------------------------------------
from url_health_gate import online_coverage

COV_LEDGER = {
    "https://a.edu/one/": {"status": "live", "offender": False},
    "https://never-cited.edu/": {"status": "dead-404", "offender": True},
}

# 11. 3 distinct live-layer urls, 1 with a ledger verdict -> measured 1 of 3
crops = [crop(regions={"r": {"anchoring_urls": {"s1": {"url": "https://a.edu/one/"},
                                                "s2": {"url": "https://b.edu/two/"}}}}),
         crop(storage={"anchoring_urls": {"s3": {"url": "https://c.edu/three/"}}})]
assert online_coverage(crops, COV_LEDGER) == (1, 3), online_coverage(crops, COV_LEDGER)

# 12. legacy zones{} urls are NOT in the denominator (same scoping as violations)
crops = [crop(zones={"8": {"anchoring_urls": {"z": {"url": "https://zonly.edu/"}}}},
              regions={"r": {"anchoring_urls": {"s1": {"url": "https://a.edu/one/"}}}})]
assert online_coverage(crops, COV_LEDGER) == (1, 1), online_coverage(crops, COV_LEDGER)

# 13. the same url cited on many crops/nodes counts ONCE (distinct urls, not nodes)
crops = [crop(regions={"r": {"anchoring_urls": {"s1": {"url": "https://a.edu/one/"}}}}),
         crop(regions={"q": {"anchoring_urls": {"s9": {"url": "https://a.edu/one/"}}}})]
assert online_coverage(crops, COV_LEDGER) == (1, 1), online_coverage(crops, COV_LEDGER)

# 14. a verdict is a verdict whatever the offender value; ledger rows never cited
#     by a live layer do not inflate either number
crops = [crop(regions={"r": {"anchoring_urls": {"s1": {"url": "https://a.edu/one/"},
                                                "s2": {"url": "https://b.edu/two/"}}}})]
assert online_coverage(crops, COV_LEDGER) == (1, 2), online_coverage(crops, COV_LEDGER)

# 15. null/empty urls are the OFFLINE gate's business; they are not "unmeasured"
crops = [crop(regions={"r": {"anchoring_urls": {"s1": {"url": None}, "s2": {"url": "https://a.edu/one/"}}}})]
assert online_coverage(crops, COV_LEDGER) == (1, 1), online_coverage(crops, COV_LEDGER)

print("url_health_gate (online coverage) tests: OK")


# ---------------------------------------------------------------------------
# CLI wiring: the --online summary line must carry the coverage figures, and
# the exit code must stay violation-driven (unmeasured urls alone -> exit 0).
# Tested through the real CLI so the print cannot silently drop the figure
# (computed-guard-expectations lesson: assert the OUTPUT, not a re-computation).
# ---------------------------------------------------------------------------
import json as _json, subprocess as _sp, tempfile as _tf

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_health_gate.py")

def _run_online(crops_obj, ledger_obj):
    with _tf.NamedTemporaryFile("w", suffix=".json", delete=False) as cf, \
         _tf.NamedTemporaryFile("w", suffix=".json", delete=False) as lf:
        _json.dump(crops_obj, cf); _json.dump(ledger_obj, lf)
        cpath, lpath = cf.name, lf.name
    try:
        return _sp.run([sys.executable, _GATE, "--online", lpath, cpath],
                       capture_output=True, text=True)
    finally:
        os.unlink(cpath); os.unlink(lpath)

# 16. clean data over a mostly-unmeasured ledger: exit 0, but the summary must say
#     how thin the measurement is -- both the measured/total figure and the word
#     UNMEASURED with the unmeasured count.
r = _run_online({"crops": [{"slug": "x", "regions": {"r": {"anchoring_urls": {
        "s1": {"url": "https://a.edu/one/"}, "s2": {"url": "https://b.edu/two/"},
        "s3": {"url": "https://c.edu/three/"}}}}}]},
    {"results": {"https://a.edu/one/": {"status": "live", "offender": False}}})
assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
assert "1/3" in r.stdout and "UNMEASURED" in r.stdout and "2 " in r.stdout, r.stdout

# 17. a hard offender still exits 1, coverage figures still present
r = _run_online({"crops": [{"slug": "x", "regions": {"r": {"anchoring_urls": {
        "s1": {"url": "https://dead.edu/"}}}}}]},
    {"results": {"https://dead.edu/": {"status": "dead-404", "offender": True}}})
assert r.returncode == 1, (r.returncode, r.stdout, r.stderr)
assert "1 known-dead" in r.stdout and "1/1" in r.stdout, r.stdout

print("url_health_gate (online CLI coverage) tests: OK")
