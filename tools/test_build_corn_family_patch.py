#!/usr/bin/env python3
"""Test the corn-family add-batch emitter: base_sha matches the live canonical, exactly
3 `add` ops appending well-formed field-corn/popcorn/flint-corn objects at the next
sequential indices, each carrying the shared corn-family shape (frost_anchored /
block-planted / one-shot harvest / dry_down-harvest-cure_thresh growth ladder / 12
regions / legacy variety shape with no maturity_class)."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_corn_family_patch as B

EXPECTED_SLUGS = ["field-corn", "popcorn", "flint-corn"]
EXPECTED_GS_TAIL = ["dry_down", "harvest", "cure_thresh"]


def _find_key(obj, key):
    """Recursively collect every value found under `key` anywhere in obj (dict/list)."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                found.append(v)
            found.extend(_find_key(v, key))
    elif isinstance(obj, list):
        for v in obj:
            found.extend(_find_key(v, key))
    return found


def test_batch_shape():
    batch = B.build()
    assert set(batch) == {"base_sha", "patches"}, batch.keys()

    # base_sha matches the live canonical
    canon_sha = hashlib.sha256(open(B.CANON, "rb").read()).hexdigest()
    assert batch["base_sha"] == canon_sha, \
        f"base_sha stale: batch {batch['base_sha']}, live {canon_sha}"

    ops = batch["patches"]
    assert len(ops) == 3, f"expected exactly 3 add ops, got {len(ops)}"

    data = json.loads(open(B.CANON, encoding="utf-8").read())
    n = len(data["crops"])

    for i, (op, expect_slug) in enumerate(zip(ops, EXPECTED_SLUGS)):
        assert op["op"] == "add", f"op {i} is not an add: {op['op']!r}"
        assert op["json_path"] == f"$.crops[{n + i}]", \
            f"op {i} path {op['json_path']!r}, expected $.crops[{n + i}]"
        crop = op["value"]
        assert isinstance(crop, dict), f"op {i} value is not a crop object"
        assert crop.get("slug") == expect_slug, \
            f"op {i} slug {crop.get('slug')!r}, expected {expect_slug!r}"
        assert crop.get("calendar_basis") == "frost_anchored", \
            f"{expect_slug}: calendar_basis {crop.get('calendar_basis')!r}, expected frost_anchored"
        assert crop.get("planting_layout") == "block", \
            f"{expect_slug}: planting_layout {crop.get('planting_layout')!r}, expected block"
        assert "harvest_window_days" not in crop, \
            f"{expect_slug}: harvest_window_days present (one-shot harvest expected absent)"

        gs = crop.get("growth_stages")
        assert isinstance(gs, list) and gs, f"{expect_slug}: growth_stages missing/empty"
        gs_ids = [s.get("id") for s in gs]
        assert gs_ids[-3:] == EXPECTED_GS_TAIL, \
            f"{expect_slug}: growth_stages tail {gs_ids[-3:]}, expected {EXPECTED_GS_TAIL}"

        regions = crop.get("regions") or {}
        assert len(regions) == 12, f"{expect_slug}: {len(regions)} regions, expected 12"

        # legacy variety shape: no maturity_class ANYWHERE under varieties (out of
        # variety_detail_gate scope -- that field belongs to the newer per-variety
        # DTM archetypes, not this crop's flat recommended-list shape)
        mat_classes = _find_key(crop.get("varieties"), "maturity_class")
        assert not mat_classes, \
            f"{expect_slug}: unexpected maturity_class in varieties (legacy shape only): {mat_classes}"

    print(f"test_batch_shape PASS (3 add ops: {EXPECTED_SLUGS} at $.crops[{n}..{n + 2}])")


if __name__ == "__main__":
    test_batch_shape()
    print("ALL build_corn_family_patch TESTS PASSED")
