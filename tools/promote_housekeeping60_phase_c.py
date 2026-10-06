#!/usr/bin/env python3
"""promote_housekeeping60_phase_c -- housekeeping kickoff 60, PHASE C: Trevor's authored strings (claude.ai) applied to
the leaves the Phase A/C quote packets measured, each cited to hashed page bytes. Base b331e5f2 (PLA-10 promote 3).

Nothing here authors a value. The strings are Trevor's, verbatim, in the stage; this promote applies them and REFUSES
unless every one is backed the way the rulings require:

INPUT (tools/staging/housekeeping60/phase_c/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}] -- one per changed leaf / key.
                 kind: prose (a consumer string), value (a field value), anchors (an anchoring_urls dict),
                 sources (a sources list), append (an append-only record gains a [CORRECTION ...] line), catalog
                 (a source_catalog entry; crop "<catalog>"), delete (a key removed). `old` is the PRE value
                 verbatim (absent keys: the string "<absent>"), so a drifted base refuses. `cited_at` is the path
                 of the block whose sources / anchoring_urls carry the leaf's citations, or null (record-only,
                 which needs a DECISIONS row naming the path with decision "record-only").
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, field = a claim tag, value = the claim as written,
                 source_id / url / sha256 / quote = the hashed page sentence. One row per (leaf, source) at least.
  DECISIONS.tsv  crop, path, decision, reason -- one per judgment (null values, kept anchors, record-only, rulings).

GUARDS (check_post):
  B  blast radius, sets first: roster and top-level key SETS equal; only staged crops (and the source_catalog
     entries staged as `catalog`) change; per crop, every changed leaf lies under a staged op path and every
     staged op path changed (a no-op op refuses).
  V  each op: PRE value == old (or absent); POST value == new (or absent for delete).
  P  prose: no em dash, no en dash, no bare degree figure without °F, a non-empty string.
  E  evidence: every prose / value op except a null-by-decision carries >= 1 EVIDENCE row; every row is a staged
     op path on its crop, its quote is in the hashed bytes at its sha (cached_quote: MANIFEST, digest, text), its url
     is cited on the crop (post state); and where cited_at names a block, that block's anchoring_urls carries the
     row's source_id at the row's url (and its sources list, where it has one, names it).
  A  anchors: in every block whose anchoring_urls this promote changes, each anchor is used by an EVIDENCE row of a
     leaf cited there, or a DECISIONS row keeps it; `sources` and `anchoring_urls` name the same ids where both exist.
  R  append: new == old + " " + one dated [CORRECTION YYYY-MM-DD: ...] line.
  O  orthography: new == old with only the ORTHOGRAPHY substitutions applied, plus an "orthography-only" DECISIONS
     row saying the leaf's claims were NOT reviewed (so a spelling fix cannot read as verification).
  D  decisions: every null value, every record-only leaf and every kept anchor has a DECISIONS row.
  G  the gates on the post-state: whole_crop_gate on every edited crop; the wide restatement scanner (B3) run over
     every edited leaf, its hits reported (the hand sweep is the review's).
A STAGE THAT NAMES NO OP REFUSES: an empty stage would "pass" having inspected nothing.

Usage:
  promote_housekeeping60_phase_c.py --check [--stage DIR] [--evidence DIR]
  promote_housekeeping60_phase_c.py --out /path/scratch.json
  promote_housekeeping60_phase_c.py --expect-sha <sha>          # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  height_strings, leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes,
                                  spacing_strings)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "housekeeping60", "phase_c")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d"  # PLA-10 promote 3, 9cea239
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "value", "anchors", "sources", "append", "catalog", "delete", "orthography")
# orthography: a spelling-only edit, exempt from the touched-leaf rule (Trevor, 2026-10-04). `new` must be `old` with
# exactly these substitutions applied, and a DECISIONS row "orthography-only" must say the claims were NOT reviewed.
ORTHOGRAPHY = {"Tomatilloes": "Tomatillos"}
OP_KEYS = {"crop", "path", "kind", "old", "new", "cited_at", "reason"}
DECISION_COLS = ("crop", "path", "decision", "reason")
# one dated correction; a path index like failure_diagnostics[5] may appear inside it, nothing else bracketed
CORRECTION = re.compile(r"\[CORRECTION (\d{4}-\d{2}-\d{2}): (?:[^\[\]]|\[\d+\])+\]")
EM_DASH, EN_DASH = "—", "–"
BARE_DEGREE = re.compile(r"\d\s*(?:degrees?\b|°(?!F))", re.I)


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def load_canonical(path=None):
    with open(path or CANON, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        refuse(f"canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


def _tsv(path, cols, label):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        if tuple(r.fieldnames or ()) != tuple(cols):
            refuse(f"{label} columns {r.fieldnames} != {list(cols)}")
        return [dict(row) for row in r]


def load_stage(stage_dir):
    with open(os.path.join(stage_dir, "ops.json"), encoding="utf-8") as f:
        ops = json.load(f)
    if not isinstance(ops, list) or not ops:
        refuse("the stage names no op")
    for i, op in enumerate(ops):
        if not isinstance(op, dict) or set(op) != OP_KEYS:
            refuse(f"op {i}: keys must be exactly {sorted(OP_KEYS)}")
        if op["kind"] not in KINDS:
            refuse(f"op {i}: unknown kind {op['kind']!r}")
        if not (isinstance(op["reason"], str) and op["reason"].strip()):
            refuse(f"op {i}: an empty reason")
    keys = [(op["crop"], op["path"]) for op in ops]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        refuse(f"an op path staged twice: {dup[:3]}")
    ev = _tsv(os.path.join(stage_dir, "EVIDENCE.tsv"), EVIDENCE_COLS, "EVIDENCE.tsv")
    dec = _tsv(os.path.join(stage_dir, "DECISIONS.tsv"), DECISION_COLS, "DECISIONS.tsv")
    return ops, ev, dec


# ---------------------------------------------------------------- paths
def _get(node, concrete):
    for s in concrete:
        node = node[s]
    return node


def _locate(root, path):
    """(parent, key, concrete) for a path on `root`; the last segment may be absent (a key being created)."""
    concrete = resolve(root, path)
    parent = _get(root, concrete[:-1])
    return parent, concrete[-1], concrete


def _value(root, path):
    try:
        parent, key, _c = _locate(root, path)
    except Refused:
        return ABSENT
    if isinstance(parent, dict):
        return parent[key] if key in parent else ABSENT
    return parent[key]


def _target(data, op):
    if op["crop"] == CATALOG:
        return data["source_catalog"]
    return by_slug(data).get(op["crop"])


# ---------------------------------------------------------------- the transform
def check_pre(pre, ops):
    idx = by_slug(pre)
    for i, op in enumerate(ops):
        if op["crop"] != CATALOG and op["crop"] not in idx:
            refuse(f"op {i}: {op['crop']} is not a crop")
        got = _value(_target(pre, op), op["path"])
        if compact(got) != compact(op["old"]):
            refuse(f"op {i} {op['crop']} {op['path']}: the base value is not the op's `old` "
                   f"({compact(got)[:80]} != {compact(op['old'])[:80]})")
    return len(ops)


def apply_to(pre, ops):
    post = copy.deepcopy(pre)
    for op in ops:
        root = _target(post, op)
        parent, key, _c = _locate(root, op["path"])
        if op["kind"] == "delete":
            del parent[key]
        else:
            parent[key] = copy.deepcopy(op["new"])
    return post


def _prose_ok(s, tag):
    if not (isinstance(s, str) and s.strip()):
        refuse(f"{tag}: prose must be a non-empty string")
    if EM_DASH in s or EN_DASH in s:
        refuse(f"{tag}: an em or en dash in consumer copy")
    if BARE_DEGREE.search(s):
        refuse(f"{tag}: a temperature without °F")


def _block(root, path):
    """The block a cited_at path names, on `root`, or None."""
    v = _value(root, path)
    return v if isinstance(v, dict) else None


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "scanner_hits": 0}
    # guard B, sets first
    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:
        refuse("the roster changed (set or order)")
    if set(pre) != set(post):
        refuse(f"top-level keys changed: {sorted(set(pre) ^ set(post))}")
    for k in pre:
        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):
            refuse(f"top-level {k!r} changed")
    staged = {}
    for op in ops:
        staged.setdefault(op["crop"], []).append(tuple(resolve(_target(post if op["kind"] != "delete" else pre, op),
                                                               op["path"])))
    pidx, qidx = by_slug(pre), by_slug(post)
    for slug in pidx:
        diff = leaf_diff(pidx[slug], qidx[slug])
        allowed = staged.get(slug, [])
        stray = sorted(fmt(list(p)) for p in diff if not any(p[:len(a)] == a for a in allowed))
        if stray:
            refuse(f"{slug}: changed outside the staged ops: {stray[:5]}")
    cat_diff = leaf_diff(pre["source_catalog"], post["source_catalog"])
    cat_allowed = staged.get(CATALOG, [])
    stray = sorted(fmt(list(p)) for p in cat_diff if not any(p[:len(a)] == a for a in cat_allowed))
    if stray:
        refuse(f"source_catalog changed outside the staged ops: {stray[:5]}")
    # guard V
    for i, op in enumerate(ops):
        tag = f"op {i} {op['crop']} {op['path']}"
        got = _value(_target(post, op), op["path"])
        want = ABSENT if op["kind"] == "delete" else op["new"]
        if compact(got) != compact(want):
            refuse(f"{tag}: the post value is not the op's `new`")
        if compact(got) == compact(op["old"]):
            refuse(f"{tag}: a no-op (new == old)")
        if op["kind"] in ("prose", "orthography"):
            _prose_ok(op["new"], tag)                         # guard P
        if op["kind"] == "orthography":                      # guard O
            fixed = op["old"]
            for wrong, right in ORTHOGRAPHY.items():
                fixed = fixed.replace(wrong, right)
            if op["new"] != fixed:
                refuse(f"{tag}: an orthography op may only apply {ORTHOGRAPHY}")
        if op["kind"] == "append":                           # guard R
            old, new = op["old"], op["new"]
            if not (isinstance(old, str) and isinstance(new, str) and new.startswith(old + " ")):
                refuse(f"{tag}: an append must keep the original byte for byte and add after a space")
            if not CORRECTION.fullmatch(new[len(old) + 1:]):
                refuse(f"{tag}: the appended text is not one dated [CORRECTION YYYY-MM-DD: ...] line")
    # guard D
    decided = {(d["crop"], d["path"]): d["decision"] for d in dec}
    for i, op in enumerate(ops):
        if op["kind"] in ("value", "prose") and op["new"] is None and (op["crop"], op["path"]) not in decided:
            refuse(f"op {i} {op['crop']} {op['path']}: a null value needs a DECISIONS row")
        if op["kind"] == "orthography" and decided.get((op["crop"], op["path"])) != "orthography-only":
            refuse(f"op {i} {op['crop']} {op['path']}: an orthography op needs an orthography-only DECISIONS row")
        if op["kind"] == "prose" and op["cited_at"] is None and decided.get((op["crop"], op["path"])) != "record-only":
            refuse(f"op {i} {op['crop']} {op['path']}: no cited_at and no record-only DECISIONS row")
    # guard E
    man = manifest(evidence_dir)
    text_cache = {}
    paths = {(op["crop"], op["path"]): op for op in ops}
    rows_for = {}
    seen = set()
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"], r["sha256"], r["quote"])
        if key in seen:
            refuse(f"{tag}: a duplicate row")
        seen.add(key)
        op = paths.get((r["crop"], r["entry_id"]))
        if op is None or op["kind"] not in ("prose", "value", "anchors"):
            refuse(f"{tag}: not a staged prose / value / anchors op")
        cached_quote(r, man, evidence_dir, text_cache, tag)
        crop = qidx[r["crop"]]
        if r["url"] not in cited_urls(crop):
            refuse(f"{tag}: url is not cited anywhere on {r['crop']} (post)")
        if op["kind"] == "anchors":
            # a re-anchored field value: the row proves the anchor itself, so the anchors dict must carry it
            if (op["new"] or {}).get(r["source_id"], {}).get("url") != r["url"]:
                refuse(f"{tag}: {op['path']} does not carry {r['source_id']} at the row's url")
        elif op["cited_at"] is not None:
            blk = _block(crop, op["cited_at"])
            if blk is None:
                refuse(f"{tag}: cited_at {op['cited_at']!r} names no block")
            if (blk.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:
                refuse(f"{tag}: {op['cited_at']}.anchoring_urls does not carry {r['source_id']} at the row's url")
            if "sources" in blk and r["source_id"] not in blk["sources"]:
                refuse(f"{tag}: {op['cited_at']}.sources does not name {r['source_id']}")
        rows_for.setdefault((r["crop"], r["entry_id"]), []).append(r)
    n["evidence_rows"] = len(ev)
    for i, op in enumerate(ops):
        if op["kind"] in ("prose", "value") and op["new"] is not None and (op["crop"], op["path"]) not in rows_for:
            refuse(f"op {i} {op['crop']} {op['path']}: no EVIDENCE row")
    # guard A
    for i, op in enumerate(ops):
        if op["kind"] != "anchors" or op["crop"] == CATALOG:
            continue
        blk_path = op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None
        crop = qidx[op["crop"]]
        used = {r["source_id"] for (c, p), rows in rows_for.items() if c == op["crop"]
                for r in rows if p == op["path"]
                or (blk_path is not None and paths[(c, p)]["kind"] != "anchors"
                    and paths[(c, p)]["cited_at"] == blk_path)}
        for sid in sorted(op["new"] or {}):
            if sid not in used and decided.get((op["crop"], f"{op['path']}.{sid}")) != "kept":
                refuse(f"op {i} {op['crop']} {op['path']}: anchor {sid} supports no evidenced leaf and no "
                       f"DECISIONS row keeps it")
        if blk_path is not None:
            blk = _block(crop, blk_path)
            if blk is not None and "sources" in blk and set(blk["sources"]) != set(blk.get("anchoring_urls") or {}):
                refuse(f"op {i} {op['crop']} {blk_path}: sources and anchoring_urls name different ids")
    # guard G: the restatement scanner over every edited leaf (reported; the review hand-sweeps)
    for slug in {op["crop"] for op in ops if op["crop"] != CATALOG}:
        crop = qidx[slug]
        edited = {fmt(resolve(crop, op["path"])) for op in ops if op["crop"] == slug and op["kind"] == "prose"}
        hits = set(spacing_strings(crop)) | set(height_strings(crop, crop.get("mature_spread_ft") is not None))
        n["scanner_hits"] += len(hits & edited)
    return n


def gate_post(post, slugs):
    """whole_crop_gate on every edited crop, against a scratch copy of the post-state (guard G)."""
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "post.json")
        with open(p, "wb") as f:
            f.write(serialize(post))
        passed = 0
        for slug in sorted(slugs):
            # The ERA SET (added 2026-10-06 when PLA-673 B2 armed soil_prep): this post-state predates watermelon's
            # soil_prep citation, so A62 checks it against the waiver set live in its era (SBR_KNOWN_AT_ARMING = this post-state's
            # sha256, a registered replay post-state; the gate refuses any other value).
            r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, p],
                               capture_output=True, text=True, env=dict(os.environ, SBR_KNOWN_AT_ARMING=sha256_bytes(serialize(post))))
            if r.returncode != 0:
                refuse(f"whole_crop_gate {slug} rc={r.returncode}: {(r.stdout + r.stderr)[-400:]}")
            # count the gate's OWN verdict, never the input set: a skipped gate must not read as a gated crop
            passed += r.stdout.count("\nGATE: PASS")
    if passed != len(slugs):
        refuse(f"whole_crop_gate printed {passed} PASS verdicts for {len(slugs)} crops")
    return passed


def run(pre, ops, ev, dec, evidence_dir):
    n = {"base_ops": check_pre(pre, ops)}
    post = apply_to(pre, ops)
    n.update(check_post(pre, post, ops, ev, dec, evidence_dir))
    n["gated_crops"] = gate_post(post, {op["crop"] for op in ops if op["crop"] != CATALOG})
    return post, n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--canonical", default=None)
    ap.add_argument("--stage", default=STAGE)
    ap.add_argument("--evidence", default=EVIDENCE)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    path = args.canonical or CANON
    try:
        if args.out and os.path.abspath(args.out) == os.path.abspath(path):
            refuse("--out may not target the canonical; use --expect-sha for the write")
        pre = load_canonical(path)
        ops, ev, dec = load_stage(args.stage)
        post, n = run(pre, ops, ev, dec, args.evidence)
    except Refused as e:
        print(f"REFUSED: {e}")
        return 1
    print(f"  inspected         {n['ops']} ops on {n['gated_crops']} crops; {n['evidence_rows']} evidence rows; "
          f"{n['decisions']} decisions; {n['scanner_hits']} edited leaves the wide scanner flags (evidenced)")
    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        print(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
        return 1
    if args.out:
        with open(args.out, "wb") as f:
            f.write(blob)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
        return 0
    if args.check:
        print("  --check: nothing written")
        return 0
    if not args.expect_sha:
        print("REFUSED: writing canonical requires --expect-sha (the gauntleted scratch SHA)")
        return 1
    with open(path, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
