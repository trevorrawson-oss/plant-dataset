#!/usr/bin/env python3
"""Test the RGV promote-batch emitter: exactly 108 rgv-cell adds + 2 top-level chill ops, all crop ops are
`add` at the regions.rgv path, base_sha present, the provenance op is a from-guarded replace whose `from`
matches its base, and -- the strongest check -- the rebuilt batch is BYTE-IDENTICAL to the committed
tools/batches/rgv_region_promote.json.

REPLAYED (kickoff 60 B5, 2026-10-03). The RGV region was promoted to the live canonical on 2026-07-13 (4e2e9e7),
after which this test returned early and PASSED having inspected nothing (PLA-544 side finding). Its real inputs
are all in git: the 7 tracked staging files (unchanged since the promote) and the pre-RGV canonical 7e29f4f4,
which is the committed batch's own base_sha (pinned in promote_fixture.COMMIT_FOR -> 7aaba61). So it builds
against that base, without writing the batch file, and must reproduce the committed batch byte for byte.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_rgv_promote as B  # noqa: E402
import promote_fixture  # noqa: E402

PRE_RGV_SHA = "7e29f4f49f5d416315f81b72d7164e3228dea3e5834edaf09673bc5c58f56204"
BATCH = os.path.join(HERE, "batches", "rgv_region_promote.json")


def test_batch_shape():
    base_raw = promote_fixture.pre_state(PRE_RGV_SHA)
    base = json.loads(base_raw)
    batch = B.build(base_raw=base_raw, write=False)
    assert set(batch) == {"base_sha", "patches"}, batch.keys()
    assert batch["base_sha"] == PRE_RGV_SHA == hashlib.sha256(base_raw).hexdigest()
    ops = batch["patches"]
    rgv_cell_ops = [o for o in ops if o["json_path"].endswith(".regions.rgv")]
    assert len(rgv_cell_ops) == 108, f"expected 108 rgv-cell ops, got {len(rgv_cell_ops)}"
    assert all(o["op"] == "add" for o in rgv_cell_ops), "every rgv-cell op must be add (net-new)"
    assert all(o["json_path"].startswith("$.crops[?(@.slug=='") for o in rgv_cell_ops)
    for o in rgv_cell_ops:
        c = o["value"]
        assert c["region_id"] == "rgv" and c["zone_span"] == ["9", "10"]
        assert sorted(c["resolved_by_zone"]) == ["10", "9"]
    band_add = [o for o in ops if o["json_path"] == "$.region_chill_delivered.rgv"]
    prov = [o for o in ops if o["json_path"] == "$.region_chill_delivered_provenance"]
    assert len(band_add) == 1 and band_add[0]["op"] == "add"
    assert len(prov) == 1 and prov[0]["op"] == "replace"
    assert prov[0]["from"] == base["region_chill_delivered_provenance"], "provenance from-guard is not its base's"
    assert len(ops) == 110, f"expected 110 total patches, got {len(ops)}"
    committed = open(BATCH, "rb").read()
    rebuilt = json.dumps(batch, ensure_ascii=False, indent=1).encode("utf-8")
    assert rebuilt == committed, "the rebuilt batch is not the committed tools/batches/rgv_region_promote.json"
    print("test_batch_shape PASS (110 patches: 108 cells + band add + provenance replace; byte-identical to the "
          "committed batch, replayed from 7e29f4f4)")


if __name__ == "__main__":
    test_batch_shape()
    print("ALL build_rgv_promote TESTS PASSED")
