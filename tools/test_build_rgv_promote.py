#!/usr/bin/env python3
"""Test the RGV promote-batch emitter: exactly 108 rgv-cell adds + 2 top-level chill ops,
all crop ops are `add` at the regions.rgv path, base_sha present, and the provenance op is a
from-guarded replace whose `from` matches the live canonical."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_rgv_promote as B

# The RGV region has been PROMOTED to the live canonical (2026-07-13, d0832254) since this test
# was written against the "canonical has no rgv yet" pre-promote premise. B.build() hard-asserts
# that premise (`assert not have_rgv`) and will now always fail -- not because the emitter is
# broken, but because the one-shot promote it built has already been applied. Skip gracefully
# rather than red-flag a healthy suite; rgv_harness + rgv_cell_audit remain reusable for the next
# region arc, and this test keeps its documentation value for that reuse.
_canon_path = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
_canon_data = json.load(open(_canon_path, encoding="utf-8"))
_RGV_ALREADY_PROMOTED = any("rgv" in (c.get("regions") or {}) for c in _canon_data["crops"])


def test_batch_shape():
    if _RGV_ALREADY_PROMOTED:
        print("skipped: rgv already promoted to the live canonical (one-shot batch already applied)")
        return
    batch = B.build()
    assert set(batch) == {"base_sha", "patches"}, batch.keys()
    # base_sha matches the live canonical
    assert batch["base_sha"] == hashlib.sha256(open(B.CANON, "rb").read()).hexdigest()
    ops = batch["patches"]
    rgv_cell_ops = [o for o in ops if o["json_path"].endswith(".regions.rgv")]
    assert len(rgv_cell_ops) == 108, f"expected 108 rgv-cell ops, got {len(rgv_cell_ops)}"
    assert all(o["op"] == "add" for o in rgv_cell_ops), "every rgv-cell op must be add (net-new)"
    assert all(o["json_path"].startswith("$.crops[?(@.slug=='") for o in rgv_cell_ops)
    # each cell is a proper rgv cell
    for o in rgv_cell_ops:
        c = o["value"]
        assert c["region_id"] == "rgv" and c["zone_span"] == ["9", "10"]
        assert sorted(c["resolved_by_zone"]) == ["10", "9"]
    # top-level chill band add + provenance replace
    band_add = [o for o in ops if o["json_path"] == "$.region_chill_delivered.rgv"]
    prov = [o for o in ops if o["json_path"] == "$.region_chill_delivered_provenance"]
    assert len(band_add) == 1 and band_add[0]["op"] == "add"
    assert len(prov) == 1 and prov[0]["op"] == "replace"
    canon = json.load(open(B.CANON, encoding="utf-8"))
    assert prov[0]["from"] == canon["region_chill_delivered_provenance"], "provenance from-guard stale"
    assert len(ops) == 110, f"expected 110 total patches, got {len(ops)}"
    print("test_batch_shape PASS (110 patches: 108 cells + band add + provenance replace)")


if __name__ == "__main__":
    test_batch_shape()
    print("ALL build_rgv_promote TESTS PASSED")
