#!/usr/bin/env python3
"""PLA-220 borderline-frame export -- correctness suite.

The frame's whole value is that it is COMPLETE and UNSELECTED. Two ways it could
quietly stop being either, and one test for each:

1. DRIFT FROM THE SHIPPED SCANNER. The exporter re-implements verbatim_scan's
   comparison in the opposite direction (source words streamed against a prose
   n-gram index) so it can say WHERE in the document a run matched. An inverted
   re-implementation that disagrees with the tool is a second, unaccountable
   definition of "borderline". `test_matches_verbatim_scan_exactly` runs the real
   tool over all 128 crops and asserts set equality on (crop, path, url, first
   6-gram) -- both directions, so a DROPPED record and an INVENTED one are equally
   fatal.

2. VACUOUS RECORDS. Every added field is recomputed here from the canonical and
   the cache by an independent walk, never trusted from the exporter's own output:
   the run really is shared, it really is MAXIMAL (no n+1 run exists), the quoted
   prose is byte-identical to the live field, and the source context actually
   contains the run it claims to surround. That last one is not hypothetical -- it
   failed on 3 records in the first build, where `Fusarium oxysporum f. sp.
   lycopersici` split at its abbreviations and the context window cut the run in
   half.

The PLA-202 exclusion is asserted to be REAL AND ONLY ITSELF: the excluded hits
must be present in the raw tool output (or the exclusion is decorative) and absent
from the frame (or it did not apply).

Run: python3 -m pytest tools/test_pla220_borderline_frame.py -q   (~50s)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "crops_data_final.json")
CACHE = os.path.join(HERE, ".doc_cache")
EXCL = os.path.join(HERE, "staging", "pla202_rewrites.json")

NORM = re.compile(r"[^a-z0-9°\s]")
BORDERLINE_LINE = re.compile(r'^  (.*?)  vs (\S+)  "(.*)"$')


def nw(text):
    return NORM.sub(" ", text.lower()).split()


def ngrams(words, n):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


@pytest.fixture(scope="module")
def canonical():
    return json.load(open(DATA))


@pytest.fixture(scope="module")
def slugs(canonical):
    return sorted(c["slug"] for c in canonical["crops"])


@pytest.fixture(scope="module")
def frame(slugs):
    """Build the frame once into a temp dir; yield (records, manifest)."""
    out = tempfile.mkdtemp(prefix="pla220_frame_")
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "pla220_borderline_frame.py"),
         f"--out={out}", f"--cache={CACHE}", f"--data={DATA}"],
        cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    records = [json.loads(l) for l in open(os.path.join(out, "_all_records.jsonl"))]
    manifest = json.load(open(os.path.join(out, "_manifest.json")))
    return records, manifest, out


@pytest.fixture(scope="module")
def tool_borderline(slugs):
    """(crop, path, url, first-6gram) straight out of the shipped scanner."""
    got = set()
    for s in slugs:
        r = subprocess.run(
            [sys.executable, os.path.join(HERE, "verbatim_scan.py"), s],
            cwd=ROOT, capture_output=True, text=True)
        body = r.stdout.split("Borderline (6-7 words):", 1)
        assert len(body) == 2, f"{s}: scanner printed no borderline section"
        for line in body[1].split("NOT COVERED (", 1)[0].splitlines():
            m = BORDERLINE_LINE.match(line)
            if m:
                got.add((s, m.group(1), m.group(2), m.group(3)))
    return got


# ------------------------------------------------------------------ 1. no drift
def test_matches_verbatim_scan_exactly(frame, tool_borderline):
    records, manifest, _ = frame
    excluded = {(e["crop_slug"], e["field_path"], e["source_url"])
                for e in manifest["pla202_excluded_hits"]}
    expected = {t for t in tool_borderline if (t[0], t[1], t[2]) not in excluded}
    actual = {(r["crop_slug"], r["field_path"], r["source_url"], r["tool_first_6gram"])
              for r in records}
    assert not expected - actual, f"exporter DROPPED {len(expected - actual)}"
    assert not actual - expected, f"exporter INVENTED {len(actual - expected)}"


def test_no_record_is_lost_to_deduping(frame, tool_borderline):
    """One record per hit -- the record count is the tuple count, not a smaller
    set of distinct fields. A field cited by 5 documents owes 5 records."""
    records, manifest, _ = frame
    assert len(records) == len({(r["crop_slug"], r["field_path"], r["source_url"])
                                for r in records})
    assert len(records) + len(manifest["pla202_excluded_hits"]) == len(tool_borderline)


# ---------------------------------------------------- 2. every field recomputed
def _resolve(crop, path):
    cur = crop
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        cur = cur[int(part[1:-1])] if part.startswith("[") else cur[part]
    return cur


def test_records_are_not_vacuous(frame, canonical):
    records, _, _ = frame
    by_slug = {c["slug"]: c for c in canonical["crops"]}
    docs = {}

    def doc(url):
        if url not in docs:
            p = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest() + ".txt")
            docs[url] = nw(open(p, encoding="utf-8", errors="replace").read())
        return docs[url]

    bad = []
    for r in records:
        rw, run = r["run_words"], r["run_normalized"]
        pw, sw = nw(r["our_prose"]), doc(r["source_url"])
        pg, sg = ngrams(pw, rw), ngrams(sw, rw)
        if rw not in (6, 7):
            bad.append((r, "run_words outside the borderline band"))
        if len(run.split()) != rw:
            bad.append((r, "run length disagrees with run_words"))
        if run not in pg:
            bad.append((r, "run absent from our prose"))
        if run not in sg:
            bad.append((r, "run absent from the source"))
        if ngrams(pw, rw + 1) & ngrams(sw, rw + 1):
            bad.append((r, "run is NOT maximal -- a longer shared run exists"))
        if sorted(pg & sg) != sorted(r["all_maximal_runs"]):
            bad.append((r, "all_maximal_runs is incomplete"))
        if nw(r["run_in_our_prose"]) != run.split():
            bad.append((r, "run_in_our_prose does not normalize back to the run"))
        if _resolve(by_slug[r["crop_slug"]], r["field_path"]) != r["our_prose"]:
            bad.append((r, "our_prose is not byte-identical to the live field"))
    assert not bad, f"{len(bad)} vacuous/incorrect records, first: {bad[0][1]} " \
                    f"({bad[0][0]['crop_slug']} {bad[0][0]['field_path']})"


def test_source_context_contains_its_own_run(frame):
    """The regression that shipped broken once: a context that does not hold the
    run sends the adjudicator to the wrong paragraph."""
    records, _, _ = frame
    missing = [r for r in records
               if not r["source_context"]
               or r["run_normalized"] not in " ".join(nw(r["source_context"]))]
    assert not missing, f"{len(missing)} contexts lose their run, first: " \
                        f"{missing[0]['crop_slug']} {missing[0]['field_path']}"


# ------------------------------------------------- 3. the exclusion is real, and only itself
def test_pla202_exclusion_is_real_and_bounded(frame, tool_borderline):
    records, manifest, _ = frame
    excl_pairs = {(s, p) for s, fields in json.load(open(EXCL)).items() for p in fields}
    assert len(excl_pairs) == 22

    hit_pairs = {(e["crop_slug"], e["field_path"]) for e in manifest["pla202_excluded_hits"]}
    # Decorative-exclusion check: what we claim to have removed was really there.
    tool_pairs = {(t[0], t[1]) for t in tool_borderline}
    assert hit_pairs <= tool_pairs and hit_pairs, "exclusion removed nothing that existed"
    assert hit_pairs <= excl_pairs, "exclusion reached beyond the PLA-202 field list"
    # ...and is really gone.
    assert not {(r["crop_slug"], r["field_path"]) for r in records} & excl_pairs
    # ...and took nothing else with it.
    survivors = {(t[0], t[1]) for t in tool_borderline} - excl_pairs
    assert survivors <= {(r["crop_slug"], r["field_path"]) for r in records}


def test_coverage_is_reported_not_silently_dropped(frame):
    """A borderline count over documents that were never read is understated. The
    manifest must carry the uncovered URLs, with a reason for each."""
    _, manifest, _ = frame
    t = manifest["totals"]
    assert t["sources_uncovered_total"] > 0, \
        "cache became complete -- confirm, then update this expectation deliberately"
    for slug, m in manifest["crops"].items():
        assert len(m["uncovered"]) == m["sources_cited"] - m["sources_text_compared"]
        for u in m["uncovered"]:
            assert u["reason"] and u["url"]


def test_shards_reconstruct_the_whole_frame(frame):
    """Sharding is a file-layout choice, not a subset. Shards must rejoin to the
    complete record list, byte-for-byte."""
    records, manifest, out = frame
    rejoined = []
    for slug in sorted(manifest["crops"]):
        shard = manifest["crops"][slug]["shard"]
        if shard is None:
            assert manifest["crops"][slug]["records"] == 0
            continue
        d = json.load(open(os.path.join(out, shard)))
        assert d["record_count"] == len(d["records"]) == manifest["crops"][slug]["records"]
        rejoined.extend(d["records"])
    assert rejoined == records
