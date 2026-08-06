#!/usr/bin/env python3
"""RED-first suite for tools/cited_claim_scan.py.

Every expected value here is ENUMERATED FROM THE DOCUMENT BY HAND, never computed from the
scanner it validates ([[computed-guard-expectations-are-vacuous]]). The four HS402 figures are
transcribed from the cached page; the confirmed negatives are transcribed from three reads.

The suite exists because a scan of "every URL lemon cites, for a lemon-adjacent temperature in
the 24-32F band" reported ZERO on 2026-08-05, and the zero was the instrument, not the data.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cited_claim_scan as ccs  # noqa: E402

HS402 = "https://edis.ifas.ufl.edu/publication/HS402"
CLEMSON_COLD = "https://hgic.clemson.edu/cold-tolerance-in-citrus/"
TAMU_CITRUS = "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/"
HS132 = "https://edis.ifas.ufl.edu/publication/HS132"

# Transcribed by hand from the cached HS402 text, 2026-08-06:
#   "defoliated at 22-24F, severe wood damaged at 20F, flowers and young fruit are killed at
#    29F, and mature fruit damaged at 28F to 31F"
# In the 24-32 band that is 24, 29, 28 and 31. The 20F wood figure is deliberately OUT of band.
HS402_IN_BAND = [24, 28, 29, 31]


def cached_text(url):
    p = ccs.cache_path(url)
    if not os.path.exists(p):
        pytest.skip(f"not in tools/.doc_cache: {url}")
    return open(p, encoding="utf-8", errors="replace").read()


# --- the structural facts the finding rests on -------------------------------------------------

def test_lemon_cites_hs402_and_it_is_cached():
    """The document that answers the question is one the crop ALREADY cites."""
    pairs = ccs.cited_urls("lemon")
    urls = {u for _, u in pairs}
    assert HS402 in urls, "lemon no longer cites HS402 -- re-derive the finding"
    assert os.path.exists(ccs.cache_path(HS402)), "HS402 fell out of the doc cache"


def test_honest_scan_finds_every_hs402_figure():
    """The scan with no proximity filter recovers all four in-band lemon figures."""
    found = sorted({h.value for h in ccs.band_hits(cached_text(HS402), 24, 32)})
    for v in HS402_IN_BAND:
        assert v in found, f"HS402 publishes {v}F for lemon and the scan missed it"


def test_the_low_endpoint_of_a_bare_range_is_not_lost():
    """"defoliated at 22-24F" carries its unit ONCE; 22 exists only as a range endpoint.

    Added after a mutation run: deleting range-scanning outright broke nothing, because every
    in-band figure happened to be reachable as a standalone match too. A guard nothing can
    falsify is not a guard ([[computed-guard-expectations-are-vacuous]]). Widening the band to
    20-32 makes the 22 -- and with it the range branch -- load-bearing.
    """
    found = {h.value for h in ccs.band_hits(cached_text(HS402), 20, 32)}
    assert 22 in found, "the low endpoint of 'defoliated at 22-24F' was dropped"
    assert 20 in found, "the standalone 'severe wood damaged at 20F' was dropped"


def test_hs402_is_recognized_as_a_lemon_subject_document():
    """Its TITLE names the crop, so crop-proximity filtering is invalid on it."""
    assert ccs.document_subject_is(cached_text(HS402), "lemon") is True


@pytest.mark.parametrize("url", [CLEMSON_COLD, TAMU_CITRUS, HS132])
def test_the_general_citrus_documents_are_not_subject_documents(url):
    """Clemson/TAMU/HS132 are about CITRUS; none is a lemon monograph."""
    assert ccs.document_subject_is(cached_text(url), "lemon") is False


# --- the bug itself, pinned so it cannot come back ---------------------------------------------

def test_MUTATION_the_proximity_window_reproduces_the_false_zero():
    """Re-introduce the original method and assert it LIES on HS402.

    Without this the fix looks like a preference. The word "lemon" sits 333 characters from the
    temperatures because on a lemon monograph the crop is the section's SUBJECT, not repeated in
    every sentence. Any window under that reports a clean, confident zero.
    """
    text = cached_text(HS402)
    for window in (60, 100, 150, 200, 250, 300):
        lying = ccs.proximity_band_hits(text, "lemon", window, 24, 32)
        assert lying == [], f"window={window} was expected to reproduce the false zero"
    honest = ccs.band_hits(text, 24, 32)
    assert len(honest) >= len(HS402_IN_BAND), "the honest scan must not inherit the bug"


def test_absence_is_refused_when_a_subject_document_is_in_the_set():
    """A zero over a set containing a crop monograph is not reportable as absence."""
    report = ccs.scan_crop("lemon", 24, 32)
    with pytest.raises(ccs.UnreportableAbsence, match="subject document"):
        ccs.assert_absence_reportable(report, used_proximity=True)


def test_absence_is_refused_while_any_cited_url_is_uncached():
    """[[absence-findings-are-document-scoped]] -- an unread URL is UNDETERMINED, not absent."""
    report = ccs.scan_crop("lemon", 24, 32)
    assert report.uncached, "expected some of lemon's cited URLs to be uncached"
    with pytest.raises(ccs.UnreportableAbsence, match="uncached"):
        ccs.assert_absence_reportable(report, used_proximity=False)


def test_MUTATION_a_silently_empty_document_set_is_caught():
    """[[a-clean-zero-can-be-your-own-parser]] -- break the cache lookup, demand a raise.

    If cache_path is broken every document reads as UNCACHED and the scan returns nothing. That
    must be an error, never a clean zero.
    """
    original = ccs.cache_path
    try:
        ccs.cache_path = lambda url: "/nonexistent/" + str(abs(hash(url)))
        report = ccs.scan_crop("lemon", 24, 32)
        with pytest.raises(ccs.UnreportableAbsence):
            ccs.assert_absence_reportable(report, used_proximity=False)
        assert report.cached_count == 0
    finally:
        ccs.cache_path = original


# --- the confirmed negatives, pinned so they are not re-hunted ---------------------------------

def test_clemson_cold_tolerance_carries_no_lemon_damage_temperature():
    """Read 2026-08-05 and again 2026-08-06: satsuma and kumquat 15F only."""
    text = cached_text(CLEMSON_COLD)
    assert ccs.band_hits(text, 24, 32) == []
    assert "lemon" in text.lower(), "expected the taxonomy sentence naming lemons"


def test_hs132_gives_lemon_no_cold_annotation():
    """Its variety table marks calamondin/kumquat 'Cold hardy' and Key lime 'cold sensitive'."""
    text = cached_text(HS132)
    assert re.search(r"Cold hardy", text), "expected the annotations that lemon does NOT carry"
    row = re.search(r"Lemon\s+July-Dec.{0,90}", text)
    assert row, "HS132's lemon row moved -- re-read before trusting this negative"
    assert "old" not in row.group(0).replace("Cold hardy", ""), (
        f"lemon's HS132 row now carries a cold annotation: {row.group(0)!r}"
    )


def test_tamu_citrus_has_only_freeze_protection_operating_points():
    """Its in-band numbers are sprinkler/duration operating points, not a lemon threshold."""
    text = cached_text(TAMU_CITRUS)
    values = {h.value for h in ccs.band_hits(text, 24, 32)}
    assert values, "expected TAMU's operating points to be present"
    assert 29 not in values, "a 29F figure would change the verdict -- re-read the document"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
