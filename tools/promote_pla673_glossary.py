#!/usr/bin/env python3
"""promote_pla673_glossary -- PLA-673 + PLA-674: the dataset's first term glossary (`hill`, `hilling`), the soil_prep
citation siblings on every crop record, and the ten document-level catalog ids the glossary cites. Base 350eda38
(PLA-666 row figures, ffbbc35).

Nothing here authors a value. The definitions are claude.ai's, approved verbatim by Trevor (2026-10-05, round 2); the
`match` lists, the sibling encoding (D13 null), the scope (D14 all 128 records) and the mints (D4, D6, STOP 2) are
ruled. The stage (built by tools/staging/pla673_glossary/build_stage.py) carries them; this promote applies them and
REFUSES unless every one is backed the way the rulings require. Derived from promote_pla666_row_figures (copied, not
imported: promotes must not import promotes), with the kinds this stage needs.

INPUT (tools/staging/pla673_glossary/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kinds:
                   catalog   crop "<catalog>", path = the new id, new = the entry (appended to source_catalog)
                   glossary  crop "<glossary>", path = the term id, new = the entry (top-level `glossary`, created)
                   sibling   crop = a roster slug, path soil_prep_sources | soil_prep_anchoring_urls, placed right
                             after the crop's last soil_prep_* key (else at the end of the record)
                 `old` is "<absent>" for every op (a key that already exists refuses).
  EVIDENCE.tsv   EVIDENCE_COLS. Glossary rows: crop "<glossary>", entry_id "<term>.<register>[n]", value = sentence n
                 verbatim. Sibling rows: crop = the slug, entry_id = the sibling key.
  DECISIONS.tsv  crop, path, decision, reason.

GUARDS (check_post):
  B  blast radius, sets first: roster identical; top-level keys == pre + {glossary}; every other top-level value
     unchanged; existing catalog entries byte-identical and the added ids == the catalog ops; each crop's changed
     paths == exactly its two sibling keys.
  V  each op: the PRE key is absent; the POST value == new.
  S  siblings: every roster record gets both keys exactly once, after its last soil_prep_* key; a null needs the
     roster null-not-assessed DECISIONS row; a non-null pair names the same ids in sources and anchoring_urls, each
     id in the catalog, each anchor used by an EVIDENCE row at its url, each row's id named and its quote in the
     hashed bytes.
  GL glossary: ids == the staged terms; entry keys == the seven ruled keys in order; term == id; definitions are
     no-dash, °F-clean prose; each register's text == its EVIDENCE sentences joined in order (every sentence evidenced,
     nothing un-evidenced); sources == the anchoring_urls keys in order; every source a catalog id whose url IS the
     anchor's url (document-level ids only) and used by a row; every row's id in sources, url == its anchor, quote
     in the hashed bytes; field_additions entries {field, date, sources, note} with sources within the entry's;
     `match` loads (glossary_sense.build_spec) and classifies the whole post roster (inspected == 232, none
     unclassified).
  C  catalog: a minted entry's id == its key, its url has a MANIFEST row, and an EVIDENCE row cites it at its url.
  D  decisions name a roster crop or "<roster>" / "<catalog>" / "<glossary>".
  G  gate_all on the post-state (every certified crop) must PASS and report its population.
A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla673_glossary.py --check
  promote_pla673_glossary.py --out /path/scratch.json
  promote_pla673_glossary.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, compact, leaf_diff, manifest,  # noqa: E402
                                  refuse, serialize, sha256_bytes)
import glossary_sense  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla673_glossary")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "350eda387fbed55464b16688a3bdc3263214b7c20631da98c7bbcb79f1d487c7"  # PLA-666 row figures, ffbbc35
CATALOG, GLOSSARY, ROSTER, ABSENT = "<catalog>", "<glossary>", "<roster>", "<absent>"
KINDS = ("catalog", "glossary", "sibling")
SIBLINGS = ("soil_prep_sources", "soil_prep_anchoring_urls")
PROSE_KEYS = ("soil_prep_beginner", "soil_prep_seasoned")
ENTRY_KEYS = ("term", "definition_beginner", "definition_seasoned", "sources", "anchoring_urls", "field_additions", "match")
REGISTERS = ("definition_beginner", "definition_seasoned")
FA_KEYS = {"field", "date", "sources", "note"}
HILL_POPULATION = 232
OP_KEYS = {"crop", "path", "kind", "old", "new", "cited_at", "reason"}
DECISION_COLS = ("crop", "path", "decision", "reason")
EM_DASH, EN_DASH = "—", "–"
BARE_DEGREE = re.compile(r"\d\s*(?:degrees?\b|°(?!F))", re.I)
ROW_ID = re.compile(r"^(?P<term>[a-z_]+)\.(?P<reg>definition_beginner|definition_seasoned)\[(?P<n>\d+)\]$")


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


# ---------------------------------------------------------------- the transform
def check_pre(pre, ops):
    idx = by_slug(pre)
    for i, op in enumerate(ops):
        tag = f"op {i} {op['crop']} {op['path']}"
        if op["old"] != ABSENT:
            refuse(f"{tag}: every op of this promote creates a key; `old` must be {ABSENT!r}")
        if op["kind"] == "catalog":
            present = op["path"] in pre["source_catalog"]
        elif op["kind"] == "glossary":
            present = op["path"] in (pre.get("glossary") or {})
        else:
            if op["crop"] not in idx:
                refuse(f"{tag}: {op['crop']} is not a crop")
            if op["path"] not in SIBLINGS:
                refuse(f"{tag}: a sibling op may only create {SIBLINGS}")
            present = op["path"] in idx[op["crop"]]
        if present:
            refuse(f"{tag}: the base value is not the op's `old` (the key already exists)")
    return len(ops)


def apply_to(pre, ops):
    post = copy.deepcopy(pre)
    for op in ops:
        if op["kind"] == "catalog":
            post["source_catalog"][op["path"]] = copy.deepcopy(op["new"])
        elif op["kind"] == "glossary":
            post.setdefault("glossary", {})[op["path"]] = copy.deepcopy(op["new"])
    idx = by_slug(post)
    for slug in dict.fromkeys(op["crop"] for op in ops if op["kind"] == "sibling"):
        c = idx[slug]
        items = list(c.items())
        prose = [i for i, (k, _v) in enumerate(items) if k in PROSE_KEYS]
        at = max(prose) + 1 if prose else len(items)
        add = [(op["path"], copy.deepcopy(op["new"])) for op in ops if op["kind"] == "sibling" and op["crop"] == slug]
        c.clear()
        c.update(items[:at] + add + items[at:])
    return post


def _prose_ok(s, tag):
    if not (isinstance(s, str) and s.strip()):
        refuse(f"{tag}: prose must be a non-empty string")
    if EM_DASH in s or EN_DASH in s:
        refuse(f"{tag}: an em or en dash in consumer copy")
    if BARE_DEGREE.search(s):
        refuse(f"{tag}: a temperature without °F")


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": len(ev), "decisions": len(dec), "siblings": 0, "null_siblings": 0,
         "glossary_terms": 0, "glossary_sentences": 0, "catalog": 0, "hill_inspected": 0}
    pidx, qidx = by_slug(pre), by_slug(post)
    # ---- guard B, sets first
    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:
        refuse("the roster changed (set or order)")
    if list(post) != list(pre) + ["glossary"]:
        refuse(f"top-level keys must be the base's plus `glossary` (appended): {sorted(set(pre) ^ set(post))}")
    for k in pre:
        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):
            refuse(f"top-level {k!r} changed")
    cat_ops = [op for op in ops if op["kind"] == "catalog"]
    for k, v in pre["source_catalog"].items():
        if k not in post["source_catalog"] or compact(post["source_catalog"][k]) != compact(v):
            refuse(f"existing catalog entry {k} changed")
    added = [k for k in post["source_catalog"] if k not in pre["source_catalog"]]
    if added != [op["path"] for op in cat_ops]:
        refuse(f"catalog additions {added[:4]} != the staged catalog ops")
    sib = {}
    for op in ops:
        if op["kind"] == "sibling":
            sib.setdefault(op["crop"], {})[op["path"]] = op
    for slug in pidx:
        diff = {p[0] for p in leaf_diff(pidx[slug], qidx[slug])}
        if diff != set(sib.get(slug, {})):
            refuse(f"{slug}: changed paths {sorted(diff)[:4]} != its staged sibling keys {sorted(sib.get(slug, {}))}")
    # ---- guard V
    for i, op in enumerate(ops):
        tag = f"op {i} {op['crop']} {op['path']}"
        if op["kind"] == "catalog":
            got = post["source_catalog"].get(op["path"], ABSENT)
        elif op["kind"] == "glossary":
            got = post["glossary"].get(op["path"], ABSENT)
        else:
            got = qidx[op["crop"]].get(op["path"], ABSENT)
        if compact(got) != compact(op["new"]):
            refuse(f"{tag}: the post value is not the op's `new`")
    # ---- guard D
    decided = {}
    for d in dec:
        decided.setdefault((d["crop"], d["path"]), set()).add(d["decision"])
        if d["crop"] not in (CATALOG, GLOSSARY, ROSTER) and d["crop"] not in pidx:
            refuse(f"DECISIONS row names {d['crop']}, which is not a crop")
    # ---- evidence rows (shared by S and GL)
    man = manifest(evidence_dir)
    text_cache = {}
    seen = set()
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"], r["sha256"], r["quote"])
        if key in seen:
            refuse(f"{tag}: a duplicate row")
        seen.add(key)
        cached_quote(r, man, evidence_dir, text_cache, tag)
    # ---- guard S
    roster = [c["slug"] for c in pre["crops"]]
    if set(sib) != set(roster) or any(set(v) != set(SIBLINGS) for v in sib.values()):
        refuse("the sibling ops must give EVERY roster record both keys (D14: all records)")
    for slug in roster:
        c = qidx[slug]
        keys = list(c)
        pos = [keys.index(k) for k in SIBLINGS]
        prose = [i for i, k in enumerate(keys) if k in PROSE_KEYS]
        want = (max(prose) + 1) if prose else len(keys) - 2
        if pos != [want, want + 1]:
            refuse(f"{slug}: the siblings are not placed right after the last soil_prep_* key (D15)")
        src, anc = c["soil_prep_sources"], c["soil_prep_anchoring_urls"]
        n["siblings"] += 2
        if src is None and anc is None:
            n["null_siblings"] += 2
            for k in SIBLINGS:
                if "null-not-assessed" not in decided.get((ROSTER, k), ()):
                    refuse(f"{slug}.{k}: a null sibling needs the {ROSTER} null-not-assessed DECISIONS row")
            continue
        if not (isinstance(src, list) and src and isinstance(anc, dict) and anc):
            refuse(f"{slug}: a sourced sibling pair must be a non-empty list and a non-empty map (or both null)")
        if list(src) != list(anc):
            refuse(f"{slug}: soil_prep_sources and soil_prep_anchoring_urls name different ids")
        rows = [r for r in ev if r["crop"] == slug and r["entry_id"] == "soil_prep_sources"]
        for sid in src:
            if sid not in post["source_catalog"]:
                refuse(f"{slug}: {sid} is not a catalog id")
            if not any(r["source_id"] == sid and r["url"] == anc[sid]["url"] for r in rows):
                refuse(f"{slug}: soil_prep anchor {sid} is used by no EVIDENCE row at its url")
        for r in rows:
            if r["source_id"] not in src or anc[r["source_id"]]["url"] != r["url"]:
                refuse(f"{slug}: an EVIDENCE row cites {r['source_id']} at a url the siblings do not carry")
    stray = [r for r in ev if r["crop"] not in (GLOSSARY,) and not (r["crop"] in roster and r["entry_id"] == "soil_prep_sources")]
    if stray:
        refuse(f"an EVIDENCE row sits on no staged op: {stray[0]['crop']} {stray[0]['entry_id']}")
    # ---- guard GL
    gl_ops = [op for op in ops if op["kind"] == "glossary"]
    if list(post["glossary"]) != [op["path"] for op in gl_ops] or not gl_ops:
        refuse("the glossary ids are not exactly the staged terms")
    gl_rows = {}
    for r in ev:
        if r["crop"] != GLOSSARY:
            continue
        m = ROW_ID.match(r["entry_id"])
        if not m or m["term"] not in post["glossary"]:
            refuse(f"glossary EVIDENCE row {r['entry_id']!r} names no staged term / register / sentence")
        gl_rows.setdefault((m["term"], m["reg"]), {}).setdefault(int(m["n"]), []).append(r)
    for tid, e in post["glossary"].items():
        tag = f"glossary.{tid}"
        if tuple(e) != ENTRY_KEYS:
            refuse(f"{tag}: entry keys {list(e)} != the seven ruled keys {list(ENTRY_KEYS)}")
        if e["term"] != tid:
            refuse(f"{tag}: term {e['term']!r} != its id")
        for reg in REGISTERS:
            _prose_ok(e[reg], f"{tag}.{reg}")
            sents = gl_rows.get((tid, reg), {})
            if sorted(sents) != list(range(1, len(sents) + 1)):
                refuse(f"{tag}.{reg}: EVIDENCE sentences are not numbered 1..n")
            texts = []
            for k in sorted(sents):
                vals = {r["value"] for r in sents[k]}
                if len(vals) != 1:
                    refuse(f"{tag}.{reg}[{k}]: rows disagree on the sentence")
                texts.append(vals.pop())
            if " ".join(texts) != e[reg]:
                refuse(f"{tag}.{reg}: the text is not exactly its evidenced sentences joined in order")
            n["glossary_sentences"] += len(texts)
        if not (isinstance(e["sources"], list) and e["sources"] and isinstance(e["anchoring_urls"], dict)):
            refuse(f"{tag}: sources must be a non-empty list and anchoring_urls a map")
        if list(e["sources"]) != list(e["anchoring_urls"]):
            refuse(f"{tag}: sources and anchoring_urls name different ids (or order)")
        rows = [r for (t, _reg), by in gl_rows.items() if t == tid for rs in by.values() for r in rs]
        for sid in e["sources"]:
            cat = post["source_catalog"].get(sid)
            if cat is None:
                refuse(f"{tag}: {sid} is not a catalog id")
            if cat.get("url") != e["anchoring_urls"][sid].get("url"):
                refuse(f"{tag}: {sid} is not a document-level id (its catalog url is not the anchored page)")
            if not any(r["source_id"] == sid for r in rows):
                refuse(f"{tag}: source {sid} is used by no EVIDENCE row")
        for r in rows:
            if r["source_id"] not in e["sources"]:
                refuse(f"{tag}: an EVIDENCE row cites {r['source_id']}, which the entry does not name")
            if e["anchoring_urls"][r["source_id"]]["url"] != r["url"]:
                refuse(f"{tag}: an EVIDENCE row's url is not {r['source_id']}'s anchor")
        fa = e["field_additions"]
        if not isinstance(fa, list) or not fa:
            refuse(f"{tag}: field_additions must be a non-empty list")
        for f in fa:
            if not isinstance(f, dict) or set(f) != FA_KEYS or not set(f["sources"]) <= set(e["sources"]):
                refuse(f"{tag}: a field_additions entry is not {sorted(FA_KEYS)} within the entry's sources")
        n["glossary_terms"] += 1
    try:
        spec = glossary_sense.build_spec(post["glossary"])
        res = glossary_sense.classify_dataset(post, spec, floor=HILL_POPULATION)
    except glossary_sense.Refused as e:
        refuse(f"glossary match: {e}")
    if res.inspected != HILL_POPULATION:
        refuse(f"glossary match inspected {res.inspected} consumer leaves, not {HILL_POPULATION}")
    n["hill_inspected"] = res.inspected
    # ---- guard C
    for op in cat_ops:
        new = op["new"]
        if not isinstance(new, dict) or new.get("id") != op["path"]:
            refuse(f"catalog {op['path']}: its id is {(new or {}).get('id')!r}")
        if not any(new.get("url") in urls for urls in man.values()):
            refuse(f"catalog {op['path']}: its url has no MANIFEST row")
        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):
            refuse(f"catalog {op['path']}: no EVIDENCE row cites it at its url")
        n["catalog"] += 1
    return n


def gate_post(post):
    """gate_all on a scratch copy of the post-state (guard G): every certified crop must PASS, population reported."""
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "post.json")
        with open(p, "wb") as f:
            f.write(serialize(post))
        # The ERA SET (added 2026-10-06 when PLA-673 B2 armed soil_prep): this post-state predates the four squash
        # citations, so it is checked against the waiver set live in its era (sourced_block_ratchet_gate.ERA_ENV, set to
        # the gated file's own sha256: the gate accepts only a registered historical post-state).
        r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), p], capture_output=True, text=True,
                           env=dict(os.environ, SBR_KNOWN_AT_ARMING=sha256_bytes(serialize(post))))
    out = r.stdout + r.stderr
    if r.returncode != 0:
        refuse(f"gate_all rc={r.returncode}: {out[-600:]}")
    m = re.search(r"gate_all: ran whole_crop_gate on (\d+) certified crop", out)
    certified = sum(1 for c in post["crops"] if (c.get("verification_status") or {}).get("status") == "verified_gs_arc")
    if not m or int(m.group(1)) != certified or certified == 0:
        refuse(f"gate_all did not report its population ({m.group(1) if m else 'none'} vs {certified} certified)")
    return int(m.group(1))


def run(pre, ops, ev, dec, evidence_dir, gates=True):
    n = {"base_ops": check_pre(pre, ops)}
    post = apply_to(pre, ops)
    n.update(check_post(pre, post, ops, ev, dec, evidence_dir))
    n["gated_crops"] = gate_post(post) if gates else None
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
    print(f"  inspected         {n['ops']} ops: {n['catalog']} catalog ids, {n['glossary_terms']} glossary terms "
          f"({n['glossary_sentences']} sentences), {n['siblings']} siblings ({n['null_siblings']} null); "
          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; match inspected {n['hill_inspected']} "
          f"consumer leaves; gate_all PASS on {n['gated_crops']} certified crops")
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
