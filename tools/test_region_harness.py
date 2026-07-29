#!/usr/bin/env python3
"""Unit tests for region_harness -- the region-GENERIC off-canonical per-crop gate harness
(Task 2 of the 2026-07-14 maritime PNW region arc). Generalized from test_rgv_harness.py:
region_id + span are now parameters instead of RGV-hardcoded constants.

Runs the REAL whole_crop_gate.py against a SCRATCH canonical (real canonical + a staged
region cell merged) + a SCRATCH tools/ copy with `region_id` patched into
zone_span_gate.EXPECTED_SPANS. The real canonical + real tools/ are never touched -- see
region_harness.py's module docstring for the mechanism. This is the load-bearing interface
for Tasks 4-7, 9 (per-region authoring/gating) across every region arc, not just pnw, so its
contract (`gate_crop(region_id, span, slug, staged_cells) -> (passed, output)`) must hold
exactly.

Run from repo root: cd tools && python3 -m pytest test_region_harness.py -v
(or python3 test_region_harness.py -- matches the rgv_harness convention of also running
standalone; see test_rgv_harness.py for precedent.)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import region_harness

BASE = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
BROC = next(c for c in BASE["crops"] if c["slug"] == "broccoli")
PNW_SPAN = ["8", "9"]


def _valid_pnw_cell():
    # a gate-valid frost-ANCHORED annual cell cloned from broccoli's ca_north_coast cell (z9),
    # re-keyed to the pnw span ["8","9"]
    src_region = BROC["regions"]["ca_north_coast"]
    cell = json.loads(json.dumps(src_region))
    cell["region_id"] = "pnw"
    cell["region_label"] = "Maritime Pacific Northwest: Puget Sound and Willamette Valley"
    cell["zone_span"] = ["8", "9"]
    z0 = sorted(cell["resolved_by_zone"])[0]
    row = cell["resolved_by_zone"][z0]
    cell["resolved_by_zone"] = {"8": json.loads(json.dumps(row)), "9": json.loads(json.dumps(row))}
    return cell


def test_valid_cell_passes():
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {"broccoli": _valid_pnw_cell()})
    assert ok, out
    print("  ok: valid pnw cell PASSES whole_crop_gate")


def test_span_key_mismatch_fails():
    cell = _valid_pnw_cell()
    del cell["resolved_by_zone"]["8"]          # span ["8","9"], keys now only ["9"]
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {"broccoli": cell})
    assert not ok and ("A45" in out or "zone_span" in out or "resolved_by_zone" in out), out
    print("  ok: span/resolved_by_zone key mismatch bounces (A45)")


def test_missing_pnw_fails_a31():
    # `None` EXPLICITLY REMOVES the region. Passing `{}` used to mean "no pnw cell", but the
    # harness builds its scratch canonical from the REAL one, so once pnw actually promoted
    # (2026-07-15) broccoli carried a genuine pnw cell and this assertion inverted -- the gate
    # passed because the data was correct. Removal has to be stated, not implied.
    ok, out = region_harness.gate_crop("pnw", PNW_SPAN, "broccoli", {"broccoli": None})
    assert not ok and "pnw" in out, out
    print("  ok: missing pnw cell bounces (A31 region roster floor)")


if __name__ == "__main__":
    test_valid_cell_passes()
    test_span_key_mismatch_fails()
    test_missing_pnw_fails_a31()
    print("\nALL region_harness TESTS PASSED")
