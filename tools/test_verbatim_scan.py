#!/usr/bin/env python3
"""Sneak the defect at verbatim_scan and confirm it BOUNCES (CLAUDE.md TDD rule).

The defect class (PLA-160 item 1): a flip-blocking Step 11 criterion that printed
`HARD hits: 0` with exit 0 while comparing ZERO of the crop's cited sources -- it read
an always-empty cache (/tmp/verbatim_cache, .body/.meta format) while the repo populates
tools/.doc_cache (extracted text, sha1(url).txt). "Verbatim clean" was never established
for any certified crop. The fix is a COVERAGE FLOOR: a zero-hit verdict is reportable only
when at least one source was compared and NONE was uncovered; otherwise the scan must exit
non-zero and say so in its own name (verbatim_scan COVERAGE INSUFFICIENT).

Exit contract under test:
  0  no HARD hits AND full coverage (len(sources) > 0 and len(uncovered) == 0)
  1  HARD hits found (adjudication owed) -- unchanged
  2  COVERAGE INSUFFICIENT -- a zero over an unmeasured population is not a verdict

Runs under both pytest and `python3 tools/test_verbatim_scan.py` -- guards live in test
bodies, never under __main__ (promote-guard-tests-belong-in-the-test-body).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, "verbatim_scan.py")
CANON = os.path.join(REPO, "crops_data_final.json")

BENIGN_DOC = (
    "Row spacing recommendations vary with cultivation equipment and irrigation layout. "
    "Trellis construction benefits from weather-resistant hardware rated for outdoor use. "
    "Mulch depth influences moisture retention during extended dry periods in most climates. "
    "Drip lines deliver water efficiently when emitters are matched to bed geometry. "
    "Cover cropping between seasons improves tilth and suppresses opportunistic weeds. "
    "Rotate legume family beds on a multi-year cycle to balance nitrogen contributions. "
    "Soil laboratory reports include cation exchange capacity alongside macronutrient values. "
    "Windbreak plantings moderate transpiration stress on exposed sites near open fields."
)


def _write_fixture(dirpath, prose):
    """A minimal one-crop dataset citing one URL, with one >=40-char prose string."""
    crop = {
        "slug": "testcrop",
        "description_beginner": prose,
        "regions": {
            "r1": {
                "resolved_by_zone": {
                    "7": {"anchoring_urls": {"src_a": {"url": "http://example.edu/guide"}}}
                }
            }
        },
    }
    p = os.path.join(dirpath, "fixture.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"crops": [crop]}, fh, ensure_ascii=False, separators=(",", ":"))
    return p


def _cache_write(cache_dir, url, text):
    os.makedirs(cache_dir, exist_ok=True)
    name = hashlib.sha1(url.encode()).hexdigest() + ".txt"
    with open(os.path.join(cache_dir, name), "w", encoding="utf-8") as fh:
        fh.write(text)


def _run(slug, fixture, cache_dir):
    return subprocess.run(
        [sys.executable, SCRIPT, slug, fixture, "--cache=" + cache_dir],
        capture_output=True, text=True)


PROSE_CLEAN = ("This friendly test crop enjoys steady sunshine and regular light watering "
               "throughout the warm part of the growing season in every home garden.")


def test_zero_coverage_zero_hits_exits_nonzero():
    """THE DEFECT: empty cache + zero hits used to exit 0. It must exit 2 and say why."""
    with tempfile.TemporaryDirectory() as d:
        fixture = _write_fixture(d, PROSE_CLEAN)
        empty_cache = os.path.join(d, "empty_cache")
        os.makedirs(empty_cache)
        r = _run("testcrop", fixture, empty_cache)
        assert r.returncode == 2, (
            "zero sources compared + zero hits must exit 2, got %d\n%s"
            % (r.returncode, r.stdout))
        assert "verbatim_scan COVERAGE INSUFFICIENT" in r.stdout, r.stdout
        assert re.search(r"compared 0 of 1", r.stdout), r.stdout
    print("PASS zero coverage + zero hits exits 2 with COVERAGE INSUFFICIENT")


def test_unreadable_cache_body_is_not_covered():
    """A \\x00FETCHFAIL stub or WAF challenge page cached as content is NOT a compared source
    (waf-block-pages-cached-as-absence)."""
    with tempfile.TemporaryDirectory() as d:
        fixture = _write_fixture(d, PROSE_CLEAN)
        cache = os.path.join(d, "cache")
        _cache_write(cache, "http://example.edu/guide", "\x00FETCHFAIL HTTPError: 403")
        r = _run("testcrop", fixture, cache)
        assert r.returncode == 2, (r.returncode, r.stdout)
        assert "verbatim_scan COVERAGE INSUFFICIENT" in r.stdout, r.stdout
        _cache_write(cache, "http://example.edu/guide",
                     "Request unsuccessful. Incapsula incident ID: 1234" + " pad" * 200)
        r = _run("testcrop", fixture, cache)
        assert r.returncode == 2, (r.returncode, r.stdout)
    print("PASS unreadable cached bodies count as NOT COVERED, exit 2")


def test_full_coverage_clean_exits_zero():
    """The honest zero: every cited source compared, nothing shared -> exit 0."""
    with tempfile.TemporaryDirectory() as d:
        fixture = _write_fixture(d, PROSE_CLEAN)
        cache = os.path.join(d, "cache")
        _cache_write(cache, "http://example.edu/guide", BENIGN_DOC)
        r = _run("testcrop", fixture, cache)
        assert r.returncode == 0, (r.returncode, r.stdout)
        assert "sources text-compared: 1/1" in r.stdout, r.stdout
        assert "COVERAGE INSUFFICIENT" not in r.stdout, r.stdout
    print("PASS full coverage + zero hits exits 0")


def test_hard_hit_still_detected_after_repoint():
    """The gate's own defect class must still bounce: an 8-word verbatim lift from a
    covered source exits 1. Proves the comparison engine survived the cache repoint."""
    lifted = ("mulch depth influences moisture retention during extended dry periods "
              "in most climates")
    with tempfile.TemporaryDirectory() as d:
        fixture = _write_fixture(d, "Gardeners know that " + lifted + " and plan for it.")
        cache = os.path.join(d, "cache")
        _cache_write(cache, "http://example.edu/guide", BENIGN_DOC)
        r = _run("testcrop", fixture, cache)
        assert r.returncode == 1, (r.returncode, r.stdout)
        assert re.search(r"HARD hits.*: [1-9]", r.stdout), r.stdout
    print("PASS 8-word verbatim lift still caught, exit 1")


def test_partial_coverage_with_zero_hits_is_insufficient():
    """One source compared, one uncovered, zero hits -> still exit 2. A partial zero is
    not 'verbatim clean'."""
    with tempfile.TemporaryDirectory() as d:
        fixture = _write_fixture(d, PROSE_CLEAN)
        # add a second cited URL to the fixture
        with open(fixture, encoding="utf-8") as fh:
            data = json.load(fh)
        node = data["crops"][0]["regions"]["r1"]["resolved_by_zone"]["7"]
        node["anchoring_urls"]["src_b"] = {"url": "http://example.edu/other"}
        with open(fixture, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        cache = os.path.join(d, "cache")
        _cache_write(cache, "http://example.edu/guide", BENIGN_DOC)
        r = _run("testcrop", fixture, cache)
        assert r.returncode == 2, (r.returncode, r.stdout)
        assert re.search(r"compared 1 of 2", r.stdout), r.stdout
    print("PASS partial coverage + zero hits exits 2")


def test_default_cache_is_the_repo_doc_cache():
    """The repoint itself: against real canonical with NO --cache flag, a certified crop
    must compare >0 sources (tools/.doc_cache holds 17 of lemon's cited documents; the old
    default /tmp/verbatim_cache compared 0 forever)."""
    r = subprocess.run([sys.executable, SCRIPT, "lemon", CANON],
                       capture_output=True, text=True)
    m = re.search(r"sources text-compared: (\d+)/(\d+)", r.stdout)
    assert m, "coverage line missing:\n%s" % r.stdout[:400]
    compared, total = int(m.group(1)), int(m.group(2))
    assert total > 0, r.stdout
    assert compared > 0, (
        "default cache compared 0/%d sources -- still pointed at the empty cache" % total)
    print("PASS default cache is tools/.doc_cache (%d/%d lemon sources compared)"
          % (compared, total))


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTS:
        t()
    print("ALL verbatim_scan TESTS PASSED (%d)" % len(TESTS))
