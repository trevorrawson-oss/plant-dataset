#!/usr/bin/env python3
"""promote_pla625_p3b -- PLA-625 citrus/rootstock pass, promote 3b: mandarin-clementine rootstock rows. Re-authors
rootstock_options[0..2] (Trifoliate orange, Flying Dragon trifoliate, Swingle citrumelo), recommended_rootstock (null),
recommended_rootstock_note and its sources pair; mints uf_ifas_ch116 (CH116) and ucce_placer_nevada_cold_damage
(FakeNorton). Base d52c261a (PLA-625 citrus promote 3a).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (PLA-625 comment b4271661, 2026-10-16), each
sentence carrying the cached-page quotes it rests on (tools/staging/pla625_p3b/p3b_texts.py). Derived from
promote_pla625_p2 (copied, not imported: promotes must not import promotes), with its new-row, rename, re-key and record
branches removed (this promote has none of those ops).

INPUT (tools/staging/pla625_p3b/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kind: prose, value, sources / anchors (a
                 row's lists, or the crop-level note pair), catalog (a minted id; crop "<catalog>", path = the id).
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, value = the sentence (or the JSON value).
  DECISIONS.tsv  crop, path, decision, reason. `nulled` backs a value op to null (no evidence row allowed); `retained`
                 backs a value the ruling keeps (a non-null one still carries evidence).

GUARDS (check_post): B blast radius, S scope (mandarin's rows, recommendation, note and note pair; the two ruled mints),
V values, P prose (no dash, no "cultivar", no bare degree), D decisions, N nulls, E evidence, A anchors, C catalog (minted
ids titled, document-scoped, T1 and evidenced at their url; every cited id catalogued), R dual register, H drops (the ruled
credits off each row; no mandarin row under uf_ifas_edis; uf_ifas_hs132 on no citrus rootstock row but lemon [0], the
retail claim), M sense guard, plus G: gates on the post-state. A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla625_p3b.py --check
  promote_pla625_p3b.py --out /path/scratch.json
  promote_pla625_p3b.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)
import glossary_sense  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla625_p3b")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "d52c261ac66f6637c4be220af052858a1fa920ec64c1d6e5eeec95083fc72487"  # PLA-625 citrus promote 3a
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "value", "anchors", "sources", "catalog")
HILL_POPULATION = 224
CROP = "mandarin-clementine"
ROWS = ["Trifoliate orange (Poncirus trifoliata)", "Flying Dragon trifoliate", "Swingle citrumelo"]
MINTED = ("uf_ifas_ch116", "ucce_placer_nevada_cold_damage")
DROPPED = {0: ("uga_ext",), 1: ("tamu_agrilife",), 2: ("uf_ifas_hs132", "tamu_agrilife")}   # ruling A
CITRUS = ("lemon", "lime", "orange-navel", "grapefruit", "mandarin-clementine")
HS132_ROWS = {("lemon", 0)}   # ruling D: only a row making the generic retail claim keeps uf_ifas_hs132
NOTE_BLOCK = "recommended_rootstock_note"
NOTE_PAIR = ("recommended_rootstock_note_sources", "recommended_rootstock_note_anchoring_urls")
SCOPE = ("rootstock_options", "recommended_rootstock", NOTE_BLOCK) + NOTE_PAIR
CULTIVAR = re.compile(r"\bcultivars?\b", re.I)
OP_KEYS = {"crop", "path", "kind", "old", "new", "cited_at", "reason"}
DECISION_COLS = ("crop", "path", "decision", "reason")
EM_DASH, EN_DASH = "—", "–"
BARE_DEGREE = re.compile(r"\d\s*(?:degrees?\b|°(?!F))", re.I)
BARE_HOST = re.compile(r"https?://[^/]+/?\Z")


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
    concrete = resolve(root, path)
    return _get(root, concrete[:-1]), concrete[-1], concrete


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
        tgt = _target(post, op)
        if op["kind"] == "catalog":
            tgt[op["path"]] = copy.deepcopy(op["new"])
            continue
        parent, key, _c = _locate(tgt, op["path"])
        parent[key] = copy.deepcopy(op["new"])
    return post


def _prose_ok(s, tag):
    if not (isinstance(s, str) and s.strip()):
        refuse(f"{tag}: prose must be a non-empty string")
    if EM_DASH in s or EN_DASH in s:
        refuse(f"{tag}: an em or en dash in consumer copy")
    if BARE_DEGREE.search(s):
        refuse(f"{tag}: a temperature without °F")
    if CULTIVAR.search(s):
        refuse(f"{tag}: 'cultivar' in consumer copy")


def _cites(crop, cited_at):
    if cited_at == NOTE_BLOCK:
        return crop.get(NOTE_PAIR[0]), crop.get(NOTE_PAIR[1])
    blk = _value(crop, cited_at)
    if not isinstance(blk, dict):
        return None, None
    return blk.get("sources"), blk.get("anchoring_urls")


def _block_of(path):
    if path.startswith("rootstock_options["):
        return path.split(".", 1)[0]
    return NOTE_BLOCK


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0,
         "retained": 0, "nulled": 0, "minted": 0}
    # guard B
    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:
        refuse("the roster changed (set or order)")
    if set(pre) != set(post):
        refuse(f"top-level keys changed: {sorted(set(pre) ^ set(post))}")
    for k in pre:
        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):
            refuse(f"top-level {k!r} changed")
    staged = {}
    for op in ops:
        conc = (op["path"],) if op["kind"] == "catalog" else tuple(resolve(_target(post, op), op["path"]))
        staged.setdefault(op["crop"], []).append(conc)
    pidx, qidx = by_slug(pre), by_slug(post)
    for slug in pidx:
        if set(pidx[slug]) != set(qidx[slug]):
            refuse(f"{slug}: top-level crop keys changed: {sorted(set(pidx[slug]) ^ set(qidx[slug]))}")
        diff = leaf_diff(pidx[slug], qidx[slug])
        stray = sorted(fmt(list(p)) for p in diff if not any(p[:len(a)] == a for a in staged.get(slug, [])))
        if stray:
            refuse(f"{slug}: changed outside the staged ops: {stray[:5]}")
    if set(pre["source_catalog"]) - set(post["source_catalog"]):
        refuse("source_catalog lost ids")
    cat_diff = leaf_diff(pre["source_catalog"], post["source_catalog"])
    stray = sorted(fmt(list(p)) for p in cat_diff if not any(p[:len(a)] == a for a in staged.get(CATALOG, [])))
    if stray:
        refuse(f"source_catalog changed outside the staged ops: {stray[:5]}")
    # guard S
    for i, op in enumerate(ops):
        if op["crop"] == CATALOG:
            if op["kind"] != "catalog" or op["path"] not in MINTED:
                refuse(f"op {i}: a catalog op on {op['path']} (ruled mints: {list(MINTED)})")
            continue
        if op["crop"] != CROP:
            refuse(f"op {i}: {op['crop']} is outside this promote's crop")
        if op["kind"] == "catalog":
            refuse(f"op {i}: a catalog op must name <catalog>")
        if not any(op["path"] == s or op["path"].startswith(s + ".") or op["path"].startswith(s + "[") for s in SCOPE):
            refuse(f"op {i} {op['crop']} {op['path']}: outside the ruled scope")
    if [r["name"] for r in qidx[CROP]["rootstock_options"]] != ROWS:
        refuse(f"{CROP}: rootstock_options rows are not {ROWS}")
    if sorted(op["path"] for op in ops if op["kind"] == "catalog") != sorted(MINTED):
        refuse(f"catalog ops are not exactly the ruled ids {list(MINTED)}")
    # guard V + P
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
    decided = {}
    for d in dec:
        decided.setdefault((d["crop"], d["path"]), set()).add(d["decision"])
    for d in dec:
        if d["crop"] not in (CATALOG, "<roster>") and d["crop"] not in pidx:
            refuse(f"DECISIONS row names {d['crop']}, which is not a crop")
    for i, op in enumerate(ops):
        if op["kind"] == "prose" and op["cited_at"] is None:
            refuse(f"op {i} {op['crop']} {op['path']}: prose with no cited_at")
    retained = {k for k, v in decided.items() if "retained" in v}
    for crop, path in sorted(retained):
        if crop not in qidx:
            refuse(f"retained {crop} {path}: not a crop")
        if (crop, path) in {(op["crop"], op["path"]) for op in ops}:
            refuse(f"retained {crop} {path}: also staged as an op")
        if compact(_value(pidx[crop], path)) != compact(_value(qidx[crop], path)):
            refuse(f"retained {crop} {path}: the value moved")
        n["retained"] += 1
    # guard N
    nulled = set()
    for i, op in enumerate(ops):
        if op["kind"] == "value" and op["new"] is None:
            if "nulled" not in decided.get((op["crop"], op["path"]), ()):
                refuse(f"op {i} {op['crop']} {op['path']}: nulled with no `nulled` DECISIONS row")
            nulled.add((op["crop"], op["path"]))
    n["nulled"] = len(nulled)
    # guard E
    man = manifest(evidence_dir)
    text_cache = {}
    paths = {(op["crop"], op["path"]): op for op in ops}
    rows_for, seen = {}, set()
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"], r["sha256"], r["quote"])
        if key in seen:
            refuse(f"{tag}: a duplicate row")
        seen.add(key)
        k = (r["crop"], r["entry_id"])
        op = paths.get(k)
        if k in nulled:
            refuse(f"{tag}: evidence for a value nulled by the ruling")
        if op is not None and op["kind"] in ("prose", "value"):
            cited_at = op["cited_at"]
        elif op is None and k in retained:
            cited_at = _block_of(r["entry_id"])
        else:
            refuse(f"{tag}: not a staged prose / value op or a retained leaf")
        cached_quote(r, man, evidence_dir, text_cache, tag)
        crop = qidx[r["crop"]]
        if r["url"] not in cited_urls(crop):
            refuse(f"{tag}: url is not cited anywhere on {r['crop']} (post)")
        srcs, anchors = _cites(crop, cited_at)
        if anchors is None:
            refuse(f"{tag}: cited_at {cited_at!r} names no citation block")
        if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:
            refuse(f"{tag}: {cited_at} anchors do not carry {r['source_id']} at the row's url")
        if srcs is None or r["source_id"] not in srcs:
            refuse(f"{tag}: {cited_at} sources do not name {r['source_id']}")
        rows_for.setdefault(k, []).append(r)
    n["evidence_rows"] = len(ev)
    for i, op in enumerate(ops):
        if op["kind"] in ("prose", "value") and (op["crop"], op["path"]) not in nulled \
                and (op["crop"], op["path"]) not in rows_for:
            refuse(f"op {i} {op['crop']} {op['path']}: no EVIDENCE row")
    for crop, path in sorted(retained):
        if _value(pidx[crop], path) is not None and (crop, path) not in rows_for:
            refuse(f"retained {crop} {path}: a non-null retained value with no EVIDENCE row")

    def _cited_at_of(c, p):
        return paths[(c, p)]["cited_at"] if (c, p) in paths else _block_of(p)

    # guard A
    for crop_slug, blk in sorted({(op["crop"], op["cited_at"]) for op in ops if op["kind"] in ("anchors", "sources")}):
        srcs, anchors = _cites(qidx[crop_slug], blk)
        if srcs is None or anchors is None or set(srcs) != set(anchors):
            refuse(f"{crop_slug} {blk}: sources and anchoring_urls name different ids")
        if len(srcs) != len(set(srcs)):
            refuse(f"{crop_slug} {blk}: a source id listed twice")
        used = {r["source_id"] for (c, p), rows in rows_for.items() if c == crop_slug
                for r in rows if _cited_at_of(c, p) == blk}
        for sid in sorted(anchors):
            if sid not in used and "kept" not in decided.get((crop_slug, f"{blk}.anchoring_urls.{sid}"), ()):
                refuse(f"{crop_slug} {blk}: anchor {sid} supports no evidenced leaf and no DECISIONS row keeps it")
    # guard C
    cat = post["source_catalog"]
    for op in ops:
        if op["kind"] != "catalog":
            continue
        new = op["new"]
        if not isinstance(new, dict) or new.get("id") != op["path"]:
            refuse(f"catalog {op['path']}: its id is {(new or {}).get('id')!r}")
        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):
            refuse(f"catalog {op['path']}: a minted id must be document-scoped and titled")
        if new.get("tier") != "T1":
            refuse(f"catalog {op['path']}: a minted id must be T1")
        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):
            refuse(f"catalog {op['path']}: no EVIDENCE row cites it at its url")
        n["minted"] += 1
    for r in ev:
        if r["source_id"] not in cat:
            refuse(f"EVIDENCE cites {r['source_id']}, which is not in source_catalog")
    # guard R
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
    # guard H
    for i, r in enumerate(qidx[CROP]["rootstock_options"]):
        cited = set(r.get("sources") or []) | set(r.get("anchoring_urls") or {})
        gone = sorted(cited & set(DROPPED[i]))
        if gone:
            refuse(f"{CROP} {r['name']}: still cites {gone} (ruling A: dropped)")
        if "uf_ifas_edis" in cited:
            refuse(f"{CROP} {r['name']}: still cites uf_ifas_edis (ruling A: CH116 under its own id)")
    for slug in CITRUS:
        for i, r in enumerate(qidx[slug].get("rootstock_options") or []):
            cited = set(r.get("sources") or []) | set(r.get("anchoring_urls") or {})
            if ("uf_ifas_hs132" in cited) != ((slug, i) in HS132_ROWS):
                refuse(f"{slug} {r['name']}: uf_ifas_hs132 {'kept' if 'uf_ifas_hs132' in cited else 'dropped'} "
                       f"(ruling D: only the generic retail claim keeps it)")
    # guard M
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
    print(f"  inspected         {n['ops']} ops; whole_crop_gate PASS on {n['gated_crops']} edited crop, then gate_all PASS; "
          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; {n['register_pairs']} register-pair checks; "
          f"{n['retained']} retained; {n['nulled']} nulled; {n['minted']} ids minted; "
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
