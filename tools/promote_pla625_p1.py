#!/usr/bin/env python3
"""promote_pla625_p1 -- PLA-625 citrus/rootstock pass, promote 1: orange-navel + grapefruit rootstock rows. Re-authors
rootstock_options[0..2] (Carrizo citrange, Swingle citrumelo, Flying Dragon trifoliate) on both crops, recommended_rootstock,
recommended_rootstock_note and its sources pair, and appends three non-blocking PLA-612 open findings. Base 59010fe6 (the
PLA-625 citrus housekeeping landing, stops 1 + 2).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (PLA-625 comment 6ab0c56a, 2026-10-13), each
sentence carrying the cached-page quotes it rests on (tools/staging/pla625_p1/p1_texts.py). The stage
(tools/staging/pla625_p1/build_stage.py) carries them; this promote applies them and REFUSES unless every one is backed.
Derived from promote_pla673_d (copied, not imported: promotes must not import promotes).

INPUT (tools/staging/pla625_p1/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kind: prose (a consumer string), value (a
                 row figure, flag or recommended_rootstock), sources / anchors (a citation block's lists, the note pair
                 included), record (verification_status.open_findings, append-only). No catalog kind: ruling C mints no id. cited_at
                 names the block whose sources / anchoring_urls cite the leaf; `recommended_rootstock_note` names the
                 crop-level pair recommended_rootstock_note_sources / _anchoring_urls.
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, value = the sentence (or the JSON value), quote = the hashed
                 page span.
  DECISIONS.tsv  crop, path, decision, reason. `nulled` backs a value op to null (no evidence row allowed); `retained`
                 backs a value the ruling keeps (a non-null one still carries evidence, since its row's old citations go).

GUARDS (check_post): B blast radius, S scope (only the ruled paths on the two crops), V values, P prose (no dash, no
"cultivar", no bare degree), D decisions, E evidence (prose, value AND retained leaves), N nulls, A anchors, K record (append-only, non-blocking, open), C every cited id in the catalog, R dual register, I identical leaves across the
two crops, H drops (no row cites uf_ifas_hs132; no Flying Dragon row cites ucr_citrus), M sense guard (population
pinned), plus G: gates on the post-state (whole_crop_gate on both crops, then gate_all with its population reported).
A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla625_p1.py --check
  promote_pla625_p1.py --out /path/scratch.json
  promote_pla625_p1.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)
import glossary_sense  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla625_p1")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "59010fe6994b95eb52407fa60a6995eedefe5636bd6a52d2f960d4b08641cf68"  # PLA-625 citrus housekeeping landing
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "value", "anchors", "sources", "record")  # no catalog: ruling C mints no id
# The sense guard's population on the post-state: unchanged from the base (no re-authored leaf carries a hill-word).
HILL_POPULATION = 224
CROPS = ("orange-navel", "grapefruit")
ROWS = ("Carrizo citrange", "Swingle citrumelo", "Flying Dragon trifoliate")
NOTE_BLOCK = "recommended_rootstock_note"
NOTE_PAIR = ("recommended_rootstock_note_sources", "recommended_rootstock_note_anchoring_urls")
# guard S: the only paths this promote may touch (ruling B), each crop
SCOPE = tuple(f"rootstock_options[name={r}]" for r in ROWS) + ("recommended_rootstock", NOTE_BLOCK) + NOTE_PAIR + \
    ("verification_status.open_findings",)
# guard I: leaves the ruling makes identical on both crops ("identical on both crops unless marked")
_ROW_LEAVES = ("size_class", "mature_height_ft", "spread_ft", "container_suitable", "container_size_gallons",
               "bearing_age_years", "sources", "anchoring_urls")
IDENTICAL = {CROPS: tuple(f"rootstock_options[name={r}].{f}" for r in ROWS for f in _ROW_LEAVES)
             + tuple(f"rootstock_options[name=Carrizo citrange].{f}" for f in ("traits_beginner", "what_to_ask_nursery"))
             + tuple(f"rootstock_options[name=Flying Dragon trifoliate].{f}"
                     for f in ("traits_seasoned", "traits_beginner", "what_to_ask_nursery"))}
CULTIVAR = re.compile(r"\bcultivars?\b", re.I)
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
    if CULTIVAR.search(s):
        refuse(f"{tag}: 'cultivar' in consumer copy")


def _cites(crop, cited_at):
    """(sources, anchoring_urls) of the block a cited_at names on `crop`, or (None, None). The note's citations are the
    crop-level pair, not a dict of their own."""
    if cited_at == NOTE_BLOCK:
        return crop.get(NOTE_PAIR[0]), crop.get(NOTE_PAIR[1])
    blk = _value(crop, cited_at)
    if not isinstance(blk, dict):
        return None, None
    return blk.get("sources"), blk.get("anchoring_urls")


def _block_of(path):
    """The cited block of a leaf path: a row leaf's row, else the note pair."""
    if path.startswith("rootstock_options["):
        return path.rsplit(".", 1)[0]
    return NOTE_BLOCK


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0,
         "identical": 0, "retained": 0, "nulled": 0, "findings_added": 0}
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
        if set(pidx[slug]) != set(qidx[slug]):
            refuse(f"{slug}: top-level crop keys changed: {sorted(set(pidx[slug]) ^ set(qidx[slug]))}")
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
    # guard S: the ruled scope, both ways (a staged path outside it, or a ruled crop the stage never touches)
    for i, op in enumerate(ops):
        if op["crop"] not in CROPS:
            refuse(f"op {i}: {op['crop']} is outside this promote's two crops")
        if not any(op["path"] == sc or op["path"].startswith(sc + ".") for sc in SCOPE):
            refuse(f"op {i} {op['crop']} {op['path']}: outside the ruled scope")
    for crop in CROPS:
        if [r["name"] for r in qidx[crop]["rootstock_options"]] != list(ROWS):
            refuse(f"{crop}: rootstock_options rows are not {list(ROWS)}")
        if not any(op["crop"] == crop for op in ops):
            refuse(f"{crop}: the stage names no op on a ruled crop")
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
    # a leaf may carry several decision rows: keep them ALL (a dict of one decision per path let the last row mask
    # another, found by the PLA-673 suite, 2026-10-05).
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
    retained = {k for k, v in decided.items() if "retained" in v}
    for crop, path in sorted(retained):
        if crop not in qidx:
            refuse(f"retained {crop} {path}: not a crop")
        if (crop, path) in {(op["crop"], op["path"]) for op in ops}:
            refuse(f"retained {crop} {path}: also staged as an op")
        if compact(_value(pidx[crop], path)) != compact(_value(qidx[crop], path)):
            refuse(f"retained {crop} {path}: the value moved")
        n["retained"] += 1
    # guard N: a value op to null is backed by a `nulled` decision and NO evidence row
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
    rows_for = {}
    seen = set()
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
        if cited_at is not None:
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
    # guard A: every anchor supports an evidenced leaf of its block; sources and anchors name the same ids. (One URL per
    # source id per block, ruling C, is guard E's: every row's url must BE its block's one anchor url for that id.)
    for i, op in enumerate(ops):
        if op["kind"] not in ("anchors", "sources"):
            continue
        blk = op["cited_at"]
        crop = qidx[op["crop"]]
        srcs, anchors = _cites(crop, blk)
        if srcs is None or anchors is None or set(srcs) != set(anchors):
            refuse(f"op {i} {op['crop']} {blk}: sources and anchoring_urls name different ids")
        if len(srcs) != len(set(srcs)):
            refuse(f"op {i} {op['crop']} {blk}: a source id listed twice")
        used = {r["source_id"] for (c, p), rows in rows_for.items() if c == op["crop"]
                for r in rows if (paths[(c, p)]["cited_at"] if (c, p) in paths else _block_of(p)) == blk}
        for sid in sorted(anchors):
            if sid not in used and "kept" not in decided.get((op["crop"], f"{blk}.anchoring_urls.{sid}"), ()):
                refuse(f"op {i} {op['crop']} {blk}: anchor {sid} supports no evidenced leaf and no DECISIONS row "
                       f"keeps it")
    # guard K: open_findings is append-only, and every appended finding is open and non-blocking. (A record op elsewhere is
    # guard S's refusal; a launch flag or status moving is guard B's: neither is an op path.)
    for i, op in enumerate(ops):
        if op["kind"] != "record":
            continue
        if "record-only" not in decided.get((op["crop"], op["path"]), ()):
            refuse(f"op {i} {op['crop']} {op['path']}: no record-only DECISIONS row")
        old, new = op["old"], _value(qidx[op["crop"]], op["path"])
        if len(new) <= len(old) or compact(new[:len(old)]) != compact(old):
            refuse(f"op {i} {op['crop']}: open_findings is not the base list plus appended entries")
        ids = [f["id"] for f in new]
        if len(ids) != len(set(ids)):
            refuse(f"op {i} {op['crop']}: a finding id twice")
        for f in new[len(old):]:
            if f.get("blocks_launch") is not False or f.get("status") != "open":
                refuse(f"op {i} {op['crop']} {f.get('id')}: an appended finding must be open with blocks_launch false")
            if EM_DASH in f.get("summary", "") or EN_DASH in f.get("summary", ""):
                refuse(f"op {i} {op['crop']} {f.get('id')}: a dash in the summary")
            n["findings_added"] += 1
    # guard C: every cited id is a catalog id (this promote mints none; a catalog op is an unknown kind)
    cat = post["source_catalog"]
    cat_ids = set(cat) if isinstance(cat, dict) else {e.get("id") for e in cat}
    for r in ev:
        if r["source_id"] not in cat_ids:
            refuse(f"EVIDENCE cites {r['source_id']}, which is not in source_catalog")
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
    # guard I: ruled-identical leaves are byte-identical on the post-state
    for crops, ipaths in IDENTICAL.items():
        for ip in ipaths:
            vals = {compact(_value(qidx[c], ip)) for c in crops}
            if len(vals) != 1:
                refuse(f"{ip}: not identical across {list(crops)} (ruled identical)")
            n["identical"] += 1
    # guard H: the ruled drops
    for crop in CROPS:
        for r in qidx[crop]["rootstock_options"]:
            cited = set(r.get("sources") or []) | set(r.get("anchoring_urls") or {})
            if "uf_ifas_hs132" in cited:
                refuse(f"{crop} {r['name']}: still cites uf_ifas_hs132 (ruling D: dropped from every row)")
            if r["name"] == "Flying Dragon trifoliate" and "ucr_citrus" in cited:
                refuse(f"{crop} Flying Dragon: still cites ucr_citrus (ruling D: dropped)")
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
          f"{n['identical']} identical-leaf checks; {n['retained']} retained; {n['nulled']} nulled; "
          f"{n['findings_added']} findings appended; "
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
