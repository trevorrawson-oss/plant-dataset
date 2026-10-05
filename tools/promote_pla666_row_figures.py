#!/usr/bin/env python3
"""promote_pla666_row_figures -- PLA-666: sourced row spacing for raspberry and pawpaw (elderberry decision-only),
with raspberry's two planting-notes leaves re-authored by Trevor (claude.ai) under the touched-leaf rule. Base
afbd4113 (Housekeeping 60 Phase C, 367c702).

Nothing here authors a value. The figures, strings and sources are ruled (PLA-666 Phase A rulings 1-7 and the strings
ruling, 2026-10-05; Linear "PLA-666 row figures: DECISIONS"); the stage (built by
tools/staging/pla666_row_figures/build_stage.py) carries them; this promote applies them and REFUSES unless every one
is backed the way the rulings require. Derived from promote_housekeeping60_phase_c (copied, not imported: promotes
must not import promotes), narrowed to the kinds this stage uses.

INPUT (tools/staging/pla666_row_figures/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}] -- one per changed leaf / key.
                 kind: prose (a consumer string), value (a field value), anchors (an anchoring_urls dict), sources (a
                 sources list), catalog (a NEW source_catalog entry; crop "<catalog>", path = its id), orthography
                 (a spelling-only edit, guard O). `old` is the
                 PRE value verbatim (absent keys: "<absent>"), so a drifted base refuses. `cited_at` is the path of
                 the block whose sources / anchoring_urls carry the leaf's citations, or null (record-only, which
                 needs a DECISIONS row naming the path with decision "record-only").
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, field = a claim tag, value = the claim as written,
                 source_id / url / sha256 / quote = the hashed page sentence.
  DECISIONS.tsv  crop, path, decision, reason -- one per judgment (null values, kept anchors, record-only, rulings,
                 and a decision-only crop such as elderberry).

GUARDS (check_post):
  B  blast radius, sets first: roster and top-level key SETS equal; only staged crops (and staged catalog entries)
     change; every changed leaf lies under a staged op path; every staged op path changed (a no-op refuses).
  V  each op: PRE value == old (or absent); POST value == new.
  O  orthography: new == old with only the ORTHOGRAPHY substitutions applied, plus an "orthography-only" DECISIONS
     row saying the leaf's claims were NOT reviewed.
  P  prose: no em dash, no en dash, no bare degree figure without °F, a non-empty string.
  D  decisions: every null value and every record-only leaf has a DECISIONS row; every DECISIONS row names a roster
     crop or "<catalog>" (a typo'd crop would otherwise record a judgment about nothing).
  E  evidence: every non-null prose / value op carries >= 1 EVIDENCE row; every row sits on a staged prose / value
     op, its quote is in the hashed bytes at its sha (cached_quote), its url is cited on the crop (post), and where
     cited_at names a block, that block's anchoring_urls carries the row's source_id at the row's url (and its
     sources list names it).
  A  anchors: in every block whose anchoring_urls this promote changes, each anchor is used by an EVIDENCE row of a
     leaf cited there, or a DECISIONS row keeps it; `sources` and `anchoring_urls` name the same ids.
  C  catalog: a minted entry's `id` equals its key, and an EVIDENCE row cites that id at the entry's url.
  G  gates on the post-state: whole_crop_gate on every edited crop (counting the gate's own PASS verdicts); the
     wide restatement scanner run over every edited prose leaf, its hits reported (the hand sweep is the review's).
A STAGE THAT NAMES NO OP REFUSES: an empty stage would "pass" having inspected nothing.

Usage:
  promote_pla666_row_figures.py --check [--stage DIR] [--evidence DIR]
  promote_pla666_row_figures.py --out /path/scratch.json
  promote_pla666_row_figures.py --expect-sha <post sha>          # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  height_strings, leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes,
                                  spacing_strings)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla666_row_figures")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"  # Housekeeping 60 Phase C, 367c702
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "value", "anchors", "sources", "catalog", "orthography")
# orthography: a spelling-only edit, exempt from the touched-leaf rule (ruling 1, Trevor, 2026-10-05; the Housekeeping
# 60 Phase C guard). `new` must be `old` with exactly these substitutions applied, and a DECISIONS row
# "orthography-only" must say the claims were NOT reviewed (so a spelling fix cannot read as verification).
ORTHOGRAPHY = {"Dorman Red": "Dormanred"}
OP_KEYS = {"crop", "path", "kind", "old", "new", "cited_at", "reason"}
DECISION_COLS = ("crop", "path", "decision", "reason")
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
        parent, key, _c = _locate(_target(post, op), op["path"])
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
        staged.setdefault(op["crop"], []).append(tuple(resolve(_target(post, op), op["path"])))
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
    # guard V (+ P)
    for i, op in enumerate(ops):
        tag = f"op {i} {op['crop']} {op['path']}"
        got = _value(_target(post, op), op["path"])
        if compact(got) != compact(op["new"]):
            refuse(f"{tag}: the post value is not the op's `new`")
        if compact(got) == compact(op["old"]):
            refuse(f"{tag}: a no-op (new == old)")
        if op["kind"] in ("prose", "orthography"):
            _prose_ok(op["new"], tag)
        if op["kind"] == "orthography":                      # guard O
            fixed = op["old"]
            for wrong, right in ORTHOGRAPHY.items():
                fixed = fixed.replace(wrong, right)
            if op["new"] != fixed:
                refuse(f"{tag}: an orthography op may only apply {ORTHOGRAPHY}")
    # guard D
    # a leaf may carry several decision rows (record-only AND cut AND timing ...): keep them ALL. A dict of one
    # decision per path let the last row mask the record-only row (found by this suite, 2026-10-05).
    decided = {}
    for d in dec:
        decided.setdefault((d["crop"], d["path"]), set()).add(d["decision"])
    for d in dec:
        if d["crop"] != CATALOG and d["crop"] not in pidx:
            refuse(f"DECISIONS row names {d['crop']}, which is not a crop")
    for i, op in enumerate(ops):
        if op["kind"] in ("value", "prose") and op["new"] is None and (op["crop"], op["path"]) not in decided:
            refuse(f"op {i} {op['crop']} {op['path']}: a null value needs a DECISIONS row")
        if op["kind"] == "orthography" and "orthography-only" not in decided.get((op["crop"], op["path"]), ()):
            refuse(f"op {i} {op['crop']} {op['path']}: an orthography op needs an orthography-only DECISIONS row")
        if op["kind"] == "prose" and op["cited_at"] is None and \
                "record-only" not in decided.get((op["crop"], op["path"]), ()):
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
        if op is None or op["kind"] not in ("prose", "value"):
            refuse(f"{tag}: not a staged prose / value op")
        cached_quote(r, man, evidence_dir, text_cache, tag)
        crop = qidx[r["crop"]]
        if r["url"] not in cited_urls(crop):
            refuse(f"{tag}: url is not cited anywhere on {r['crop']} (post)")
        if op["cited_at"] is not None:
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
        if op["kind"] != "anchors":
            continue
        blk_path = op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None
        crop = qidx[op["crop"]]
        used = {r["source_id"] for (c, p), rows in rows_for.items() if c == op["crop"]
                for r in rows if blk_path is not None and paths[(c, p)]["cited_at"] == blk_path}
        for sid in sorted(op["new"] or {}):
            if sid not in used and "kept" not in decided.get((op["crop"], f"{op['path']}.{sid}"), ()):
                refuse(f"op {i} {op['crop']} {op['path']}: anchor {sid} supports no evidenced leaf and no "
                       f"DECISIONS row keeps it")
        if blk_path is not None:
            blk = _block(crop, blk_path)
            if blk is not None and "sources" in blk and set(blk["sources"]) != set(blk.get("anchoring_urls") or {}):
                refuse(f"op {i} {op['crop']} {blk_path}: sources and anchoring_urls name different ids")
    # guard C
    for op in ops:
        if op["kind"] != "catalog":
            continue
        new = op["new"]
        if not isinstance(new, dict) or new.get("id") != op["path"]:
            refuse(f"catalog {op['path']}: its id is {(new or {}).get('id')!r}")
        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):
            refuse(f"catalog {op['path']}: no EVIDENCE row cites it at its url")
    # guard G: the restatement scanner over every edited prose leaf (reported; the review hand-sweeps)
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
            r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, p],
                               capture_output=True, text=True)
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
