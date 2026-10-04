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
    # INJECTION (kickoff 60 B5, 2026-10-03). Since the RGV promote every crop carries a real rgv cell, so an
    # empty staged_cells no longer removes one and this test returned early, PASSING having inspected nothing.
    # Now it builds the harness's own scratch canonical and DELETES broccoli's regions.rgv before gating, so the
    # A31 region-roster floor must fire through the REAL whole_crop_gate on a scratch tools/ copy.
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tools = rgv_harness.build_scratch_tools(os.path.join(tmp, "tools"))
        canon = rgv_harness.scratch_canonical({}, os.path.join(tmp, "canon.json"))
        data = json.load(open(canon, encoding="utf-8"))
        broc = next(c for c in data["crops"] if c["slug"] == "broccoli")
        assert "rgv" in broc.get("regions", {}), "the injection needs a real rgv cell to remove"
        del broc["regions"]["rgv"]
        with open(canon, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
        r = subprocess.run([sys.executable, os.path.join(tools, "whole_crop_gate.py"), "broccoli", canon],
                           capture_output=True, text=True, timeout=120)
        out = r.stdout + r.stderr
    assert r.returncode != 0 and "A31" in out and "rgv" in out, out[-1500:]
    print("  ok: a crop with its rgv cell removed bounces (A31 region roster floor)")

if __name__ == "__main__":
    test_valid_cell_passes()
    test_span_key_mismatch_fails()
    test_missing_rgv_fails_a31()
    print("\nALL rgv_harness TESTS PASSED")
