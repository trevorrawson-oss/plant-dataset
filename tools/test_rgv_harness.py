#!/usr/bin/env python3
"""Unit tests for rgv_harness -- the off-canonical per-crop gate harness for the RGV
(Rio Grande Valley) region column (Task 2 of the 2026-07-13 RGV/subtropical-TX arc).

Runs the REAL whole_crop_gate.py against a SCRATCH canonical (real canonical + a
staged rgv cell merged) + a SCRATCH tools/ copy with `rgv` patched into
zone_span_gate.EXPECTED_SPANS. The real canonical + real tools/ are never touched --
see rgv_harness.py's module docstring for the mechanism. This is the load-bearing
interface for Tasks 4-7 (per-crop rgv authoring/gating), so its contract
(`gate_crop(slug, staged_cells) -> (passed, output)`) must hold exactly.

Run from repo root: python3 tools/test_rgv_harness.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import rgv_harness

BASE = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
BROC = next(c for c in BASE["crops"] if c["slug"] == "broccoli")

# The RGV region has been PROMOTED to the live canonical (2026-07-13, d0832254). Once real, every
# certified crop (broccoli included) already carries a real regions.rgv cell, so
# test_missing_rgv_fails_a31's "canonical has no rgv yet" premise no longer holds: merging an EMPTY
# staged_cells dict onto broccoli's already-rgv-carrying regions no longer reproduces a missing-rgv
# A31 failure. Detected below so that test can skip gracefully instead of red-flagging a healthy
# harness; rgv_harness itself (and this fixture machinery) stays reusable for the next region arc.
_RGV_ALREADY_PROMOTED = "rgv" in (BROC.get("regions") or {})


def _valid_rgv_cell():
    """A minimal-but-gate-valid frost-free annual cell cloned from broccoli's hawaii
    cell, re-keyed to the rgv span ["9", "10"]. `lifted_from_zone` on the donor row
    is nulled out: the source row (hawaii zone "10") carries lifted_from_zone:"11",
    a dangling reference once re-keyed to the rgv span (zone "11" no longer exists in
    the cell) -- left as-is it trips A45 donor integrity, NOT a real rgv defect, so
    the fixture must be a genuinely clean cell rather than a raw hawaii clone."""
    haw = BROC["regions"]["hawaii_tropical"]
    cell = json.loads(json.dumps(haw))
    cell["region_id"] = "rgv"
    cell["region_label"] = "Rio Grande Valley: Subtropical South Texas"
    cell["zone_span"] = ["9", "10"]
    src = json.loads(json.dumps(cell["resolved_by_zone"][sorted(cell["resolved_by_zone"])[0]]))
    src["lifted_from_zone"] = None
    cell["resolved_by_zone"] = {"9": json.loads(json.dumps(src)), "10": json.loads(json.dumps(src))}
    return cell


def test_valid_cell_passes():
    ok, out = rgv_harness.gate_crop("broccoli", {"broccoli": _valid_rgv_cell()})
    assert ok, out
    print("  ok: valid rgv cell PASSES whole_crop_gate")


def test_span_key_mismatch_fails():
    cell = _valid_rgv_cell()
    del cell["resolved_by_zone"]["9"]          # span says ["9","10"], keys now only ["10"]
    ok, out = rgv_harness.gate_crop("broccoli", {"broccoli": cell})
    assert not ok and ("A45" in out or "zone_span" in out or "resolved_by_zone" in out), out
    print("  ok: span/resolved_by_zone key mismatch bounces (A45)")


def test_missing_rgv_fails_a31():
    if _RGV_ALREADY_PROMOTED:
        print("  skipped: rgv already promoted to the live canonical (broccoli already carries a "
              "real regions.rgv cell, so an empty staged_cells no longer reproduces a missing-rgv "
              "A31 failure)")
        return
    ok, out = rgv_harness.gate_crop("broccoli", {})   # no rgv cell added
    assert not ok and "rgv" in out, out
    print("  ok: missing rgv cell bounces (A31 region roster floor)")


if __name__ == "__main__":
    test_valid_cell_passes()
    test_span_key_mismatch_fails()
    test_missing_rgv_fails_a31()
    print("\nALL rgv_harness TESTS PASSED")
