#!/usr/bin/env python3
"""Adversarial tests for tools/verify_demux_footprint.py.

Exercises the auditor's distinguishing logic that a naive re-read misses:
  - the nested resolved_by_zone allowlist walk (per-stage key allow/deny)
  - the clean-stage allowlist (window/envelope keys only clean-legal)
  - the FINDING-1 regression: `regions` entirely absent on one side must
    produce itemized FOOTPRINT: diagnostics, never a traceback.

Uses tempfile copies of the REAL canonical crops_data_final.json -- the
canonical itself is never modified. Run: python3 tools/test_verify_demux_footprint.py
"""
import json
import os
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO_ROOT, "crops_data_final.json")
AUDITOR = os.path.join(REPO_ROOT, "tools", "verify_demux_footprint.py")


def load_canonical():
    with open(CANONICAL, "rb") as f:
        raw = f.read()
    assert not raw.endswith(b"\n"), "canonical unexpectedly has a trailing newline"
    return json.loads(raw.decode("utf-8"))


def crops_of(data):
    return data["crops"] if isinstance(data, dict) and "crops" in data else data


def find_crop(data, slug):
    for c in crops_of(data):
        if c.get("slug") == slug:
            return c
    raise AssertionError(f"slug not found in canonical: {slug}")


def write_compact(data):
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    return path


def run_auditor(candidate_path, slugs, stage):
    return subprocess.run(
        [sys.executable, AUDITOR, candidate_path,
         "--base", CANONICAL, "--slugs", slugs, "--stage", stage],
        capture_output=True, text=True,
    )


def first_region_cell(crop):
    """Return (region_key, zone_key) for the first resolved_by_zone cell."""
    regions = crop["regions"]
    rk = next(iter(regions))
    zk = next(iter(regions[rk]["resolved_by_zone"]))
    return rk, zk


def test_disallowed_nested_cell_key():
    data = load_canonical()
    bp = find_crop(data, "bell-pepper")
    rk, zk = first_region_cell(bp)
    cell = bp["regions"][rk]["resolved_by_zone"][zk]
    assert "resolution_method" in cell
    cell["resolution_method"] = "CORRUPTED"
    # DERIVED, not hardcoded (2026-07-29): this said `== 124` and rotted as the roster grew to 128.
    # It is only a did-the-canonical-load sanity check, so cross-check the file's own declared
    # total rather than freezing a number that changes every time a crop is added.
    assert len(crops_of(data)) == data["total_crops"], (
        "roster length disagrees with the canonical's own total_crops",
        len(crops_of(data)), data["total_crops"])
    path = write_compact(data)
    try:
        result = run_auditor(path, "bell-pepper", "populate")
        assert result.returncode == 1, (
            f"expected exit 1, got {result.returncode}\n{result.stdout}\n{result.stderr}")
        assert "cell key changed: resolution_method" in result.stdout, result.stdout
        assert "Traceback" not in result.stdout and "Traceback" not in result.stderr
    finally:
        os.remove(path)
    print("  test_disallowed_nested_cell_key: OK")


def test_allowed_populate_key():
    data = load_canonical()
    bp = find_crop(data, "bell-pepper")
    rk, zk = first_region_cell(bp)
    cell = bp["regions"][rk]["resolved_by_zone"][zk]
    assert "second_planting" not in cell
    cell["second_planting"] = {
        "start_indoors": None,
        "plant_out": "Sep 1 - Sep 20",
        "harvest_start": "Nov 1",
        "harvest_end": "Nov 30",
        "sources": [],
        "anchoring_urls": {},
    }
    # DERIVED, not hardcoded (2026-07-29): see the note in test_disallowed_nested_cell_key.
    assert len(crops_of(data)) == data["total_crops"]
    path = write_compact(data)
    try:
        result = run_auditor(path, "bell-pepper", "populate")
        assert result.returncode == 0, (
            f"expected exit 0, got {result.returncode}\n{result.stdout}\n{result.stderr}")
    finally:
        os.remove(path)
    print("  test_allowed_populate_key: OK")


def test_clean_stage_allowlist():
    data = load_canonical()
    bp = find_crop(data, "bell-pepper")
    rk, zk = first_region_cell(bp)
    cell = bp["regions"][rk]["resolved_by_zone"][zk]
    assert "harvest_end" in cell
    cell["harvest_end"] = "CHANGED-DATE"
    # DERIVED, not hardcoded (2026-07-29): see the note in test_disallowed_nested_cell_key.
    assert len(crops_of(data)) == data["total_crops"]
    path = write_compact(data)
    try:
        populate_result = run_auditor(path, "bell-pepper", "populate")
        assert populate_result.returncode == 1, (
            "harvest_end is not in the populate allowlist; expected exit 1, got "
            f"{populate_result.returncode}\n{populate_result.stdout}")
        assert "cell key changed: harvest_end" in populate_result.stdout, populate_result.stdout

        clean_result = run_auditor(path, "bell-pepper", "clean")
        assert clean_result.returncode == 0, (
            "harvest_end IS in the clean allowlist; expected exit 0, got "
            f"{clean_result.returncode}\n{clean_result.stdout}")
    finally:
        os.remove(path)
    print("  test_clean_stage_allowlist: OK")


def test_regions_absent_regression():
    """FINDING 1: an absent `regions` key on one side must not crash the
    auditor with a KeyError -- it must degrade to {} and produce itemized
    FOOTPRINT: diagnostics, then keep going (fail CLOSED, never a traceback)."""
    data = load_canonical()
    bp = find_crop(data, "bell-pepper")
    assert "regions" in bp
    del bp["regions"]
    # DERIVED, not hardcoded (2026-07-29): see the note in test_disallowed_nested_cell_key.
    assert len(crops_of(data)) == data["total_crops"]
    path = write_compact(data)
    try:
        result = run_auditor(path, "bell-pepper", "populate")
        assert result.returncode == 1, (
            f"expected exit 1, got {result.returncode}\n{result.stdout}\n{result.stderr}")
        assert "FOOTPRINT:" in result.stdout, result.stdout
        assert "Traceback" not in result.stdout and "Traceback" not in result.stderr, (
            f"auditor must fail CLOSED with diagnostics, not a traceback:\n{result.stderr}")
    finally:
        os.remove(path)
    print("  test_regions_absent_regression: OK")


def test_trailing_newline():
    with open(CANONICAL, "rb") as f:
        raw = f.read()
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(raw + b"\n")
    try:
        result = run_auditor(path, "bell-pepper", "populate")
        assert result.returncode == 1, (
            f"expected exit 1, got {result.returncode}\n{result.stdout}\n{result.stderr}")
        assert "trailing newline" in result.stdout, result.stdout
    finally:
        os.remove(path)
    print("  test_trailing_newline: OK")


def main():
    test_disallowed_nested_cell_key()
    test_allowed_populate_key()
    test_clean_stage_allowlist()
    test_regions_absent_regression()
    test_trailing_newline()
    print("verify_demux_footprint tests: OK")


if __name__ == "__main__":
    main()
