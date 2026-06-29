#!/usr/bin/env python3
"""Behavior-level hardening tests for the inline whole_crop_gate.py checks that are NOT
importable `*_violations` functions (the §3 subset, the dispatch/floor branches). Each
test reproduces an incognito-redteam-audit (2026-06-27) injection in a SCRATCH copy of the
canonical and asserts the live gate now FAILS it (the hole is closed), with a negative
control proving the unmutated crop still PASSES (zero false positives on the certified 18).

Method mirrors the audit: deep-copy the canonical, mutate ONE crop, write a scratch JSON,
run `whole_crop_gate.py <slug> <scratch>` as a subprocess, read the exit code. READ-ONLY on
the canonical -- every mutation lands only in a tempfile.

Run: python3 tools/test_whole_crop_gate_hardening.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANONICAL = os.path.join(ROOT, "crops_data_final.json")
GATE = os.path.join(HERE, "whole_crop_gate.py")

_DATA = json.load(open(CANONICAL, encoding="utf-8"))


def _crop(slug):
    return copy.deepcopy(next(c for c in _DATA["crops"] if c["slug"] == slug))


def run_gate(mutated_crop):
    """Write a scratch dataset with `mutated_crop` swapped in for its slug, run the live
    gate on that slug, return (exit_code, combined_output)."""
    data = copy.deepcopy(_DATA)
    slug = mutated_crop["slug"]
    data["crops"] = [mutated_crop if c["slug"] == slug else c for c in data["crops"]]
    fd, path = tempfile.mkstemp(suffix=".json", prefix="gatehard_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
        p = subprocess.run([sys.executable, GATE, slug, path],
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        os.unlink(path)


def expect_fail(crop, needle, label):
    code, out = run_gate(crop)
    assert code != 0, f"{label}: expected gate FAIL, got PASS (exit 0)\n{out}"
    assert needle.lower() in out.lower(), f"{label}: FAIL but message missing {needle!r}\n{out}"
    print(f"  ok (caught): {label}")


def expect_pass(crop, label):
    code, out = run_gate(crop)
    assert code == 0, f"{label}: expected clean PASS, got FAIL (exit {code})\n{out}"
    print(f"  ok (clean):  {label}")


# ============================================================================
# C9 -- §3 pH nesting accepts an INVERTED preferred_range with tolerated present.
# The check guarded only nesting (tolerated[0]<=preferred[0] and preferred[1]<=
# tolerated[1]); preferred:[9,4] tolerated:[5.8,7.5] passed (Hero stat "9.0 to 4.0").
# ============================================================================
def test_c9_inverted_preferred_range():
    print("C9: §3 pH inverted preferred_range")
    # negative control: the unmutated certified crop passes
    expect_pass(_crop("carrot"), "C9 control: unmutated carrot")
    # the audit injection: preferred low/high inverted, still nested in tolerated
    bad = _crop("carrot")
    bad["ph"] = {**(bad.get("ph") or {}), "preferred_range": [9, 4],
                 "tolerated_range": [5.8, 7.5]}
    expect_fail(bad, "ph", "C9: inverted preferred_range [9,4]")
    # an inverted TOLERATED range is equally wrong
    bad2 = _crop("carrot")
    bad2["ph"] = {**(bad2.get("ph") or {}), "preferred_range": [6.0, 6.8],
                  "tolerated_range": [7.5, 5.8]}
    expect_fail(bad2, "ph", "C9: inverted tolerated_range [7.5,5.8]")


# ============================================================================
# re-audit #2 D9 (shape half) -- gate F must reject a truthy-placeholder anchoring URL.
# `url:"TODO"`/`"pending"` are truthy and passed the old `not au[s].get("url")` check; an
# anchoring URL must be a real http(s) URL. (The CONTENT half + `verified` honesty is the
# source-fidelity layer's job, not this gate -- `verified` is a date string here, not a bool.)
# ============================================================================
def _first_anchored_source(crop):
    """Find a (path-ish) anchoring_urls dict + a source id in it, to mutate its url."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith("anchoring_urls") and isinstance(v, dict):
                    for sid, entry in v.items():
                        if isinstance(entry, dict) and entry.get("url"):
                            found.append((v, sid))
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(crop)
    return found[0] if found else (None, None)


def test_d9_placeholder_url():
    print("D9: gate F rejects a truthy-placeholder anchoring url")
    expect_pass(_crop("carrot"), "D9 control: unmutated carrot (real http urls)")
    bad = _crop("carrot")
    au, sid = _first_anchored_source(bad)
    assert au is not None, "carrot should have an anchored source to mutate"
    au[sid]["url"] = "TODO"          # truthy placeholder -- passed the old `not url` check
    expect_fail(bad, "malformed", "D9: anchoring url 'TODO' (not an http URL)")


if __name__ == "__main__":
    test_c9_inverted_preferred_range()
    test_d9_placeholder_url()
    print("\nALL HARDENING TESTS PASSED")
