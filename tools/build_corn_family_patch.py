#!/usr/bin/env python3
"""Emit the SHA-guarded corn-family add-batch: 3 net-new crops (field-corn, popcorn,
flint-corn) appended at the next sequential `$.crops[]` indices, PLUS a 4th op that
bumps the top-level `total_crops` counter to match the new roster size. Pure builder --
reads a base canonical (read-only, never written) and the 3 author-validated +
individually gate-clean scratch crop objects, and PRINTS the batch JSON to stdout.
Writes nothing itself; applying (scratch or real) is a separate, explicit step
(apply_patch.py / the operator-run promote).

Op shape (append + counter-bump). Per apply_patch.py's leaf_set, an index == len(list)
APPENDS rather than indexing, so 3 sequential adds at len/len+1/len+2 extend the list one
at a time when applied in order; the trailing replace keeps `total_crops` from going stale
behind the splice (both `from` and `value` derived from the base, never hardcoded):
  {"op":"add",     "json_path":"$.crops[<len>]",   "value": <field-corn object>}
  {"op":"add",     "json_path":"$.crops[<len+1>]", "value": <popcorn object>}
  {"op":"add",     "json_path":"$.crops[<len+2>]", "value": <flint-corn object>}
  {"op":"replace", "json_path":"$.total_crops", "from":<base total_crops>, "value":<+3>}

Order is fixed: field-corn, popcorn, flint-corn (matches the 3 scratch files below and
the GS-anchor design spec). Every string in all 3 objects is asserted em-dash-free
(house style: commas/colons/semicolons/periods, never an em dash, in consumer copy).

Output is COMPACT (separators=(",",":"), no trailing newline) to match the committed
batch. Usage:
  python3 tools/build_corn_family_patch.py > tools/batches/corn_family_add.json
  python3 tools/build_corn_family_patch.py <base.json> > out.json   # explicit base

Post-ship reproducibility: this is a one-shot batch. Once it is promoted, the LIVE
canonical no longer equals the batch's base (the 3 crops are already spliced in), so a
fresh read of the live canonical cannot reproduce the committed batch. When the target
crops are already present in the live canonical, __main__ reconstructs the exact
pre-promote base from git (identified by the committed batch's own base_sha) so the
builder still reproduces its committed batch byte-for-byte -- the reusable-template
reproducibility contract. (Same "one-shot already applied" reality build_rgv_promote hits.)
"""
import hashlib
import json
import subprocess
import sys

CANON = "crops_data_final.json"
COMMITTED_BATCH = "tools/batches/corn_family_add.json"
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


def build(canon_raw=None):
    """Emit the corn-family add-batch dict. `canon_raw` = the raw base-canonical bytes to
    build against; default None -> read the live canonical (`CANON`). Pure: no writes, no
    base selection (the caller / __main__ decides which base bytes to pass)."""
    raw = canon_raw if canon_raw is not None else open(CANON, "rb").read()
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
            f"{expect_slug} already present in the base canonical -- refusing a duplicate add"
        _assert_no_em_dash(crop, expect_slug)
        idx = n + len(patches)
        patches.append({"op": "add", "json_path": f"$.crops[{idx}]", "value": crop})

    # 4th op: keep the top-level `total_crops` counter in sync with the new roster size, so
    # the count field never goes stale behind the crop splice. Both ends are derived from the
    # base (never hardcoded): `from` reads the field itself (the authoritative from-guard,
    # which equals len(crops) on a healthy canonical); `value` adds the count of new crops.
    n_added = len(patches)
    current_total = data["total_crops"]
    patches.append({"op": "replace", "json_path": "$.total_crops",
                    "from": current_total, "value": current_total + n_added})

    return {"base_sha": base_sha, "patches": patches}


def _reconstruct_pre_promote_base(base_sha):
    """Recover the exact pre-promote canonical (content-sha256 == base_sha) from git history,
    so a post-ship run can still reproduce the committed batch. Returns the raw bytes, or None
    if git is unavailable or no matching blob exists."""
    try:
        commits = subprocess.check_output(
            ["git", "log", "--all", "--format=%H", "--", CANON],
            text=True, stderr=subprocess.DEVNULL).split()
    except Exception:
        return None
    for c in commits:
        try:
            blob = subprocess.check_output(["git", "show", f"{c}:{CANON}"],
                                           stderr=subprocess.DEVNULL)
        except Exception:
            continue
        if hashlib.sha256(blob).hexdigest() == base_sha:
            return blob
    return None


def resolve_base_raw():
    """Return the base-canonical bytes to build against: the live canonical normally (a fresh
    pre-promote clone-a-crop run), OR -- if this one-shot batch's crops are ALREADY promoted
    into the live canonical -- the reconstructed pre-promote base, so the builder reproduces
    its committed batch even post-ship."""
    live = open(CANON, "rb").read()
    live_slugs = {c["slug"] for c in json.loads(live)["crops"]}
    if all(slug in live_slugs for _, slug in SCRATCH):
        try:
            committed_sha = json.load(open(COMMITTED_BATCH))["base_sha"]
        except Exception:
            return live  # no committed batch to anchor recovery -> let build() raise the guard
        recon = _reconstruct_pre_promote_base(committed_sha)
        if recon is not None:
            print("note: corn family already promoted into the live canonical; reconstructing "
                  "the pre-promote base from git to reproduce the committed batch", file=sys.stderr)
            return recon
    return live


if __name__ == "__main__":
    base_raw = open(sys.argv[1], "rb").read() if len(sys.argv) > 1 else resolve_base_raw()
    batch = build(base_raw)
    json.dump(batch, sys.stdout, ensure_ascii=False, separators=(",", ":"))
