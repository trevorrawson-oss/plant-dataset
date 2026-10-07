#!/usr/bin/env python3
"""promote_pla673_d -- PLA-673 part D: the pepper Phytophthora blight entry re-authored whole from NC State's factsheet
(PLA-688; bell-pepper and banana-pepper, identical), watermelon's row entry re-sourced to UF VH021 (the layout consensus
ruling) with its crop-root mirror, and watermelon's thinning leaves re-authored in both registers. Base aaf004a2 (B2,
6bce088).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (part D rulings, 2026-10-06), each sentence
mapped to rows of the posted packets (PP pepper, C part C) or to the watermelon thinning quotes (W). The stage
(tools/staging/pla673_d/build_stage.py) carries them; this promote applies them and REFUSES unless every one is backed.
Derived from promote_pla673_b2 (copied, not imported: promotes must not import promotes;
tools/staging/pla673_d/derive_promote.py records the edits).

INPUT (tools/staging/pla673_d/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kind: prose (a consumer string), value (a
                 numeric layout figure or its crop-root mirror), sources / anchors (a citation block's lists), catalog (a
                 NEW source_catalog entry; none staged here). cited_at names the block whose sources / anchoring_urls cite
                 the leaf or value.
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, value = the sentence (or the JSON value), quote = the hashed
                 page sentence.
  DECISIONS.tsv  crop, path, decision, reason.

GUARDS (check_post): B blast radius, V values, P prose, D decisions, E evidence (prose AND value ops), A anchors,
C catalog, R dual register, M sense guard (population pinned), plus:
  I  identical entries: every crop in IDENTICAL carries a byte-identical post value at each path IDENTICAL names
     (the pepper entry is ruled identical on both peppers).
  X  mirror: a staged crop-root `spacing_inches` equals the post `in_row_inches` of the first planting_layout entry
     carrying one, default first (spec §1.6 item 7; planting_layout_gate re-checks it roster-wide in gate_all).
  G  gates on the post-state: whole_crop_gate on every edited crop, then gate_all with its population reported.
A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla673_d.py --check
  promote_pla673_d.py --out /path/scratch.json
  promote_pla673_d.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)
import glossary_sense  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla673_d")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"  # PLA-673 part B2, 6bce088
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "value", "anchors", "sources", "catalog")
# The sense guard's population on the post-state: 225 on aaf004a2, less the two pepper prevention_seasoned leaves (no
# hill-word after the re-author), plus watermelon's thinning.method ("thin to two plants per hill").
HILL_POPULATION = 224
# guard I: paths whose post value must be byte-identical across the named crops (ruled: the pepper entry is identical)
IDENTICAL = {("bell-pepper", "banana-pepper"): ("diseases[id=phytophthora-blight]",)}
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
    n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0,
         "identical": 0, "mirrors": 0}
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
        if op["kind"] == "prose":
            _prose_ok(op["new"], tag)
    # guard D
    # a leaf may carry several decision rows (record-only AND cut AND timing ...): keep them ALL. A dict of one
    # decision per path let the last row mask the record-only row (found by this suite, 2026-10-05).
    decided = {}
    for d in dec:
        decided.setdefault((d["crop"], d["path"]), set()).add(d["decision"])
    for d in dec:
        if d["crop"] not in (CATALOG, "<roster>") and d["crop"] not in pidx:
            refuse(f"DECISIONS row names {d['crop']}, which is not a crop")
    for i, op in enumerate(ops):
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
        if op["kind"] in ("prose", "value") and (op["crop"], op["path"]) not in rows_for:
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
    # guard R: dual register (both edited together; never byte-identical)
    edited = {(op["crop"], op["path"]) for op in ops if op["kind"] == "prose"}
    for crop, path in sorted(edited):
        for a_suf, b_suf in (("_seasoned", "_beginner"), ("_beginner", "_seasoned")):
            if path.endswith(a_suf):
                twin = path[: -len(a_suf)] + b_suf
                if (crop, twin) not in edited:
                    refuse(f"{crop} {path}: re-authored without its {b_suf[1:]} sibling {twin} (dual-register rule)")
                if _value(qidx[crop], path) == _value(qidx[crop], twin):
                    refuse(f"{crop} {path}: byte-identical to {twin} (dual-register rule)")
                n["register_pairs"] += 1
    # guard I: ruled-identical entries are byte-identical on the post-state
    for crops, ipaths in IDENTICAL.items():
        for ip in ipaths:
            vals = {compact(_value(qidx[c], ip)) for c in crops}
            if len(vals) != 1:
                refuse(f"{ip}: not identical across {list(crops)} (ruled identical)")
            n["identical"] += 1
    # guard X: a staged crop-root spacing_inches mirrors the first entry carrying in_row_inches, default first
    for op in ops:
        if op["kind"] == "value" and op["path"] == "spacing_inches":
            entries = sorted(qidx[op["crop"]].get("planting_layout") or [], key=lambda e: not e.get("default"))
            src = next((e for e in entries if e.get("in_row_inches") is not None), None)
            if src is None or compact(src["in_row_inches"]) != compact(qidx[op["crop"]]["spacing_inches"]):
                refuse(f"{op['crop']} spacing_inches {qidx[op['crop']]['spacing_inches']!r} is not the mirror "
                       f"{(src or {}).get('in_row_inches')!r}")
            n["mirrors"] += 1
    # guard M: the glossary's own match classifies the post roster
    try:
        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=HILL_POPULATION)
    except glossary_sense.Refused as e:
        refuse(f"glossary match on the post roster: {e}")
    if res.inspected != HILL_POPULATION:
        refuse(f"glossary match inspected {res.inspected} consumer leaves, not {HILL_POPULATION}")
    n["hill_inspected"] = res.inspected
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
        r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), p], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode != 0:
        refuse(f"gate_all rc={r.returncode}: {out[-600:]}")
    m = re.search(r"gate_all: ran whole_crop_gate on (\d+) certified crop", out)
    certified = sum(1 for c in post["crops"] if (c.get("verification_status") or {}).get("status") == "verified_gs_arc")
    if not m or int(m.group(1)) != certified or certified == 0:
        refuse(f"gate_all did not report its population ({m.group(1) if m else 'none'} vs {certified} certified)")
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
    print(f"  inspected         {n['ops']} ops; whole_crop_gate PASS on {n['gated_crops']} edited crops, then gate_all PASS; "
          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; {n['register_pairs']} register-pair checks; "
          f"{n['identical']} identical-entry checks; {n['mirrors']} mirror checks; "
          f"match inspected {n['hill_inspected']} consumer leaves")
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
