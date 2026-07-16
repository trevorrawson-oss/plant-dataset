#!/usr/bin/env python3
"""Emit the SHA-guarded corn-family add-batch: 3 net-new crops (field-corn, popcorn,
flint-corn) appended at the next sequential `$.crops[]` indices. Pure builder -- reads
the LIVE canonical (read-only, never written) and the 3 author-validated + individually
gate-clean scratch crop objects, and PRINTS the batch JSON to stdout. Writes nothing
itself; applying (scratch or real) is a separate, explicit step (apply_patch.py /
Task 6's operator-run promote).

Op shape (append, per apply_patch.py's leaf_set: an index == len(list) APPENDS rather
than indexing, so 3 sequential adds at len/len+1/len+2 extend the list one at a time
when applied in order):
  {"op":"add", "json_path":"$.crops[<len>]",   "value": <field-corn object>}
  {"op":"add", "json_path":"$.crops[<len+1>]", "value": <popcorn object>}
  {"op":"add", "json_path":"$.crops[<len+2>]", "value": <flint-corn object>}

Order is fixed: field-corn, popcorn, flint-corn (matches the 3 scratch files below and
the GS-anchor design spec). Every string in all 3 objects is asserted em-dash-free
(house style: commas/colons/semicolons/periods, never an em dash, in consumer copy).

Usage: python3 tools/build_corn_family_patch.py > tools/batches/corn_family_add.json
"""
import hashlib
import json
import sys

CANON = "crops_data_final.json"
SCRATCH = [
    ("/private/tmp/field_corn.json", "field-corn"),
    ("/private/tmp/popcorn.json", "popcorn"),
    ("/private/tmp/flint_corn.json", "flint-corn"),
]
EM_DASH = "—"


def _assert_no_em_dash(obj, ctx):
    """Recursively walk a crop object and refuse any string carrying an em dash --
    house style forbids it in consumer copy (CLAUDE.md); this is a load-bearing gate
    on the 3 author-handoff objects before they ever reach the batch."""
    if isinstance(obj, str):
        if EM_DASH in obj:
            raise AssertionError(f"em dash found in {ctx}: {obj[:80]!r}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _assert_no_em_dash(v, f"{ctx}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _assert_no_em_dash(v, f"{ctx}[{i}]")


def build():
    raw = open(CANON, "rb").read()
    base_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    n = len(data["crops"])
    canon_slugs = {c["slug"] for c in data["crops"]}

    patches = []
    for path, expect_slug in SCRATCH:
        crop = json.load(open(path, encoding="utf-8"))
        assert crop.get("slug") == expect_slug, \
            f"{path}: expected slug {expect_slug!r}, got {crop.get('slug')!r}"
        assert expect_slug not in canon_slugs, \
            f"{expect_slug} already present in the live canonical -- refusing a duplicate add"
        _assert_no_em_dash(crop, expect_slug)
        idx = n + len(patches)
        patches.append({"op": "add", "json_path": f"$.crops[{idx}]", "value": crop})

    return {"base_sha": base_sha, "patches": patches}


if __name__ == "__main__":
    batch = build()
    json.dump(batch, sys.stdout, ensure_ascii=False)
