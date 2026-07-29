#!/usr/bin/env python3
"""Test the corn-family add-batch emitter: base_sha matches the base it built against,
exactly 4 ops -- 3 `add` ops appending well-formed field-corn/popcorn/flint-corn objects
at the next sequential indices (each carrying the shared corn-family shape: frost_anchored
/ block-planted / one-shot harvest / dry_down-harvest-cure_thresh growth ladder / 12
regions / legacy variety shape with no maturity_class) FOLLOWED BY the `replace $.total_crops`
counter-bump op -- and, the strongest check, that re-serializing the batch is BYTE-IDENTICAL
to the committed tools/batches/corn_family_add.json (the builder reproduces its own batch).

This is a one-shot batch. Post-promote the live canonical no longer equals the batch base
(the 3 crops are already spliced in), so the test builds against the exact pre-promote base
reconstructed from git (identified by the committed batch's base_sha), the same way the
builder's __main__ does. Pre-promote (family absent from live) it builds against the live
canonical directly. If the family is promoted AND the pre-promote base cannot be recovered,
it skips gracefully (mirrors build_rgv_promote's post-promote handling)."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_corn_family_patch as B

EXPECTED_SLUGS = ["field-corn", "popcorn", "flint-corn"]
EXPECTED_GS_TAIL = ["dry_down", "harvest", "cure_thresh"]
BATCH = os.path.join(os.path.dirname(HERE), "tools", "batches", "corn_family_add.json")


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


def _base_raw_for_test():
    """The exact base bytes the committed batch was built against: the live canonical if the
    corn family is not yet promoted, else the reconstructed pre-promote base (or None if it
    cannot be recovered from git)."""
    live = open(B.CANON, "rb").read()
    live_slugs = {c["slug"] for c in json.loads(live)["crops"]}
    if all(s in live_slugs for s in EXPECTED_SLUGS):
        committed_sha = json.load(open(BATCH))["base_sha"]
        return B._reconstruct_pre_promote_base(committed_sha)  # bytes or None
    return live


def test_batch_shape():
    base_raw = _base_raw_for_test()
    if base_raw is None:
        print("skipped: corn family promoted and the pre-promote base is not reconstructable "
              "from git (one-shot batch already applied)")
        return

    base = json.loads(base_raw)
    n = len(base["crops"])
    batch = B.build(base_raw)
    assert set(batch) == {"base_sha", "patches"}, batch.keys()

    # base_sha matches the base actually built against
    assert batch["base_sha"] == hashlib.sha256(base_raw).hexdigest(), \
        f"base_sha stale: batch {batch['base_sha']}"

    ops = batch["patches"]
    assert len(ops) == 4, f"expected exactly 4 ops (3 adds + total_crops replace), got {len(ops)}"

    for i, (op, expect_slug) in enumerate(zip(ops[:3], EXPECTED_SLUGS)):
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

    # 4th op: the total_crops counter-bump, both ends derived from the base
    last = ops[3]
    assert last["op"] == "replace", f"op 3 is not a replace: {last['op']!r}"
    assert last["json_path"] == "$.total_crops", \
        f"op 3 path {last['json_path']!r}, expected $.total_crops"
    assert last["from"] == base["total_crops"], \
        f"op 3 from {last['from']!r}, expected base total_crops {base['total_crops']!r}"
    assert last["value"] == len(base["crops"]) + 3, \
        f"op 3 value {last['value']!r}, expected len(base crops)+3 = {len(base['crops']) + 3}"

    # STRONGEST: the builder reproduces its own committed batch byte-for-byte (compact,
    # no trailing newline) -- the reproducibility contract the count-bump op is here to keep.
    rebuilt = json.dumps(batch, ensure_ascii=False, separators=(",", ":")).encode()
    committed = open(BATCH, "rb").read()
    assert rebuilt == committed, \
        "builder no longer reproduces the committed batch byte-for-byte " \
        f"(rebuilt {len(rebuilt)} bytes vs committed {len(committed)} bytes)"

    print(f"test_batch_shape PASS (4 ops: 3 adds at $.crops[{n}..{n + 2}] + total_crops "
          f"{last['from']}->{last['value']}; byte-identical to committed batch)")


# DISCHARGED ONE-SHOT (guard added 2026-07-29). build_corn_family_patch reads its three staged
# crops from session-scoped /private/tmp/*.json files that no longer exist -- the corn-family arc
# shipped 2026-07-16 and those temp inputs went with the session. The builder can no longer run, so
# this test hard-failed with a FileNotFoundError and sat in the "pre-existing failures" bucket,
# where it added noise and hid nothing. Reconstructing the inputs would mean FABRICATING the staged
# crops, which is worse than not testing. So: skip loudly, and name what is not covered.
_STAGED = ["/private/tmp/field_corn.json", "/private/tmp/popcorn.json",
           "/private/tmp/flint_corn.json"]

if __name__ == "__main__":
    _missing = [p for p in _STAGED if not os.path.exists(p)]
    if _missing:
        print("SKIP build_corn_family_patch: staged inputs are gone "
              f"({len(_missing)}/{len(_STAGED)} missing, e.g. {_missing[0]}).")
        print("  The corn-family arc shipped 2026-07-16; its /private/tmp staging was "
              "session-scoped. NOT COVERED: the builder's byte-for-byte reproduction of "
              "tools/batches/corn_family_add.json. Restore the staged crops to re-enable.")
        sys.exit(0)
    test_batch_shape()
    print("ALL build_corn_family_patch TESTS PASSED")
