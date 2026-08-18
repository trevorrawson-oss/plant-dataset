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




# --- a cached FILE is not a cached DOCUMENT ----------------------------------------------------

def test_a_cached_fetch_failure_is_not_treated_as_readable(tmp_path, monkeypatch):
    """The fetcher writes its own failures into the cache as content.

    48 `\\x00FETCHFAIL ...` stubs and 10 Incapsula challenge pages were found in tools/.doc_cache
    on 2026-08-06. Unfiltered they report as CACHED and scan clean -- an absence manufactured by
    our own fetcher rather than by the network ([[waf-block-pages-cached-as-absence]]).
    """
    assert ccs.is_document('\x00FETCHFAIL HTTPError: HTTP Error 403: Forbidden') is False
    assert ccs.is_document(' ' * 10 + 'Request unsuccessful. Incapsula incident ID: 1234') is False
    assert ccs.is_document('x' * 50) is False, 'implausibly short'
    assert ccs.is_document('The lemon tree is damaged at 29 degrees F. ' * 20) is True


def test_MUTATION_a_poisoned_cache_entry_is_reported_as_undetermined(monkeypatch):
    """Point one cited URL at a FETCHFAIL stub and assert absence becomes unreportable."""
    real = ccs.cache_path
    poisoned = {}

    def fake(url):
        if url == CLEMSON_COLD:
            return poisoned['path']
        return real(url)

    import tempfile
    d = tempfile.mkdtemp()
    poisoned['path'] = os.path.join(d, 'stub.txt')
    open(poisoned['path'], 'w').write('\x00FETCHFAIL HTTPError: HTTP Error 403: Forbidden')
    monkeypatch.setattr(ccs, 'cache_path', fake)

    report = ccs.scan_crop('lemon', 24, 32)
    states = {url: state for _sid, url, state, _h, _s in report.rows}
    assert states[CLEMSON_COLD] == 'NOT-A-DOCUMENT'
    assert CLEMSON_COLD in {u for _s, u in report.uncached}
    with pytest.raises(ccs.UnreportableAbsence, match='uncached'):
        ccs.assert_absence_reportable(report, used_proximity=False)


# --- PLA-161: the guard could not refuse over documents it never enumerated -------------------
#
# `cited_urls` walked `anchoring_urls` by exact key, so a source id named only in a `sources` or
# `source_set` list never entered `report.rows` and therefore could never enter `report.uncached`.
# The guard that refuses an absence over UNREAD documents was structurally unable to see them.
#
# PLA-161 recorded this as latent -- "protected today only by cache incompleteness",
# `assert_absence_reportable(..., used_proximity=False)` returning True for ZERO of 128 crops. By
# 2026-08-14 it returned True for 58 of 128, and 28 of those had unread list-only documents: the
# guard was actively certifying absence over documents it could not read. A protection that holds
# only while some unrelated thing stays broken is not latent, it is scheduled
# ([[latent-guard-gap-goes-live-when-upstream-completes]]).
#
# Expected values below are transcribed from the dataset BY HAND, never computed from the walk
# they validate ([[computed-guard-expectations-are-vacuous]]).

# lemon names these four ONLY in sources/source_set -- never as an anchoring_urls key.
LEMON_LIST_ONLY = {
    'uc_anr_8100',                 # https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf
    'ucce_placer_nevada_31_018c',  # https://ucanr.edu/sites/default/files/2020-10/63813.pdf
    'umd_ext',                     # https://extension.umd.edu
    'umn_ext',                     # https://extension.umn.edu/vegetables
}

# Crops that PASSED the absence guard on 2026-08-14 while carrying UNCACHED list-only documents.
# Both are deliberately uncached-not-poisoned, so they survive any doc-cache repair.
#   shallot          -> ncsu_ext_bulb_onions, uada_ext_fsa6014
#   english-cucumber -> uiuc_ext
FALSE_PASS_CROPS = ('shallot', 'english-cucumber')


def test_cited_urls_reaches_ids_named_only_in_sources_lists():
    """RED before the widening: the four ids lemon names only in lists must be enumerated."""
    seen = {sid for sid, _url in ccs.cited_urls('lemon')}
    missing = LEMON_LIST_ONLY - seen
    assert not missing, (
        f"cited_urls cannot see {sorted(missing)} -- they are named in sources/source_set and "
        f"resolve through source_catalog, so the guard cannot refuse an absence over them"
    )


def test_every_enumerated_pair_carries_a_usable_url():
    """A widening that emitted (sid, None) would crash the fetcher rather than refuse."""
    for sid, url in ccs.cited_urls('lemon'):
        assert isinstance(url, str) and url, f"{sid} enumerated without a URL"


@pytest.mark.parametrize("slug", FALSE_PASS_CROPS)
def test_absence_is_refused_over_documents_named_only_in_sources_lists(slug):
    """RED before the widening: these crops passed the guard over documents nobody had read."""
    report = ccs.scan_crop(slug, 24, 32)
    with pytest.raises(ccs.UnreportableAbsence, match="uncached"):
        ccs.assert_absence_reportable(report, used_proximity=False)


def test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass():
    """Re-introduce the narrow walk and assert the guard STOPS firing.

    Without this the widening looks like a preference rather than a fix. `anchoring_urls_only`
    is kept in the module as THE WRONG METHOD for exactly this purpose, the same way
    `proximity_band_hits` is.
    """
    for slug in FALSE_PASS_CROPS:
        narrow = {sid for sid, _u in ccs.anchoring_urls_only(slug)}
        wide = {sid for sid, _u in ccs.cited_urls(slug)}
        assert wide - narrow, f"{slug} has no list-only ids -- it cannot pin this regression"

    original = ccs.cited_urls
    try:
        ccs.cited_urls = ccs.anchoring_urls_only
        for slug in FALSE_PASS_CROPS:
            report = ccs.scan_crop(slug, 24, 32)
            assert ccs.assert_absence_reportable(report, used_proximity=False) is True, (
                f"{slug} was expected to reproduce the false pass under the narrow walk"
            )
    finally:
        ccs.cited_urls = original


def test_a_source_id_with_no_resolvable_url_still_blocks_absence(monkeypatch):
    """An id we cannot resolve is UNREAD, not absent -- it must never be dropped silently.

    Every list-only id resolves through source_catalog today (48 of 48). This pins the behaviour
    for the day one does not: dropping it would shrink the denominator, which is the same defect
    in a different costume ([[a-clean-zero-can-be-your-own-parser]]).
    """
    data = ccs._load()
    victim = sorted(LEMON_LIST_ONLY)[0]
    data['source_catalog'][victim] = {'id': victim}  # a catalog row with no url

    report = ccs.scan_crop('lemon', 24, 32, data)
    states = {sid: state for sid, _u, state, _h, _s in report.rows}
    assert states.get(victim) == 'UNRESOLVED', (
        f"{victim} lost its URL and vanished from the report instead of blocking"
    )
    assert victim in {sid for sid, _u in report.uncached}
    with pytest.raises(ccs.UnreportableAbsence):
        ccs.assert_absence_reportable(report, used_proximity=False)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
