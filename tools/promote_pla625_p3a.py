#!/usr/bin/env python3
"""promote_pla625_p3a -- PLA-625 citrus/rootstock pass, promote 3a: citrus mulch, graft-union height and brown rot, on
lemon, lime, orange-navel, grapefruit and mandarin-clementine. Exact-substring edits to the ruled strings (touched-leaf
rule: every other sentence byte-identical), the ruled citations added to each touched CITED block, CG009 anchors off the
two foot-rot blocks re-keyed to uf_ifas_cg009 (amendment 5dde3208), orange-navel brown rot re-authored (splash_barrier_mulch rung removed, uc_ipm repointed), HS141
and CG009 minted, and grapefruit's mulch finding noted (it stays open past 3a, amendment stop 2). Base ef1a4d35 (PLA-625 citrus promote 2).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (PLA-625 comment 356a763f, 2026-10-16), each
new clause carrying the cached-page quotes it rests on (tools/staging/pla625_p3a/p3a_texts.py). Derived from
promote_pla625_p2 (copied, not imported: promotes must not import promotes).

INPUT (tools/staging/pla625_p3a/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason", "subs"}]. kind: prose (subs = the ruled
                 [old, new] substring pairs; the promote re-derives new), sources / anchors (a touched block's lists),
                 ladder (a control_ladder with one ruled rung removed), record (open_findings: one named finding resolved),
                 catalog (a minted id). cited_at = the block whose citations the string's new clauses join, or null for
                 an evidence-only string (an uncited / sourceless block, ruling citation rule).
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the touched path, value = the new substring, quote = the hashed page span.
  DECISIONS.tsv  crop, path, decision, reason. evidence-only, deleted, rekey, cg009-off, repoint, rung-removed,
                 record-only, kept.

GUARDS (check_post): B blast radius, S scope (ruled path families, five crops), V values, T touched-leaf (new == old with
the subs applied, each old exactly once, nothing else), P prose (each new substring: no dash, no "cultivar", no bare
degree), E evidence (every added clause; cited rows at their block's anchor; evidence-only rows need their DECISIONS row),
A anchors (sources == anchors; an id ADDED to a block supports an evidenced clause of it), X citation moves (an id removed
is a CG009 anchor; a renamed id keeps its url), L ladder (exactly the ruled rung gone, order kept), K record (only the
named finding moves, open -> resolved, with its note), C catalog, H drops (the ruled strings and anchors are gone), M sense
guard, plus G: gates on the post-state. A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla625_p3a.py --check
  promote_pla625_p3a.py --out /path/scratch.json
  promote_pla625_p3a.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)
import glossary_sense  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla625_p3a")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "ef1a4d351e4b26ea0369f5f3da824cb7c81ffcd4e3e1e2013b94b2413dcf6261"  # PLA-625 citrus promote 2
CATALOG = "<catalog>"
ABSENT = "<absent>"
KINDS = ("prose", "sources", "anchors", "ladder", "record", "catalog")
HILL_POPULATION = 224
CROPS = ("lemon", "lime", "orange-navel", "grapefruit", "mandarin-clementine")
FR = "diseases[id=phytophthora-foot-rot]"
BR = "diseases[id=citrus-brown-rot]"
MINTED = ("uf_ifas_hs141", "uf_ifas_cg009")
# amendment 5dde3208, stop 2: the grapefruit mulch finding STAYS OPEN past 3a; it only gains a progress note
NOTED = {("grapefruit", "grapefruit_mulched_basin_contradicted_pla533")}
# amendment stop 1: CG009 stays cited on the two foot-rot blocks, re-keyed to its own id, scope on the anchor
CG009_ID = "uf_ifas_cg009"
CG009_NOTE = "Florida commercial production guide; cited only where no home-garden page covers the claim"
REMOVED_RUNG = ("orange-navel", BR, "splash_barrier_mulch")
BR_UC_IPM = "https://ipm.ucanr.edu/home-and-landscape/brown-rot-of-citrus/"
PENDING = "PENDING-INDEPENDENT-CHECK"
# guard S: the ruled path families (every touched string, plus its block's citation lists)
SCOPE = [re.compile(p + r"\Z") for p in (
    r"companions\.(note_seasoned|note_beginner|bad_beginner\[0\]\.why_beginner|bad_beginner_seasoned\[0\]\.why_beginner"
    r"|bad_seasoned\[0\]\.why_seasoned|sources|anchoring_urls)",
    r"soil_prep_(seasoned|beginner)",
    r"watering\.(method_seasoned|method_beginner|method_note_seasoned|sources|anchoring_urls)",
    re.escape(FR) + r"\.(prevention_seasoned|prevention_beginner|control_ladder\[0\]\.note_(seasoned|beginner)|sources"
                    r"|anchoring_urls)",
    re.escape(BR) + r"\.(prevention_seasoned|prevention_beginner|organic_treatment_seasoned|organic_treatment_beginner"
                    r"|control_ladder|anchoring_urls)",
    r"tips_by_stage\.planting\[0\]\.(text_seasoned|text_beginner|sources|anchoring_urls)",
    r"year_one_notes_(seasoned|beginner)",
    r"start_method\.notes_seasoned",
    r"verification_status\.open_findings",
)]
# guard H: none of these may survive in a touched string
GONE = ("hand's width", "two to three inches", "a couple inches above the soil", "standard recommendation for all citrus",
        "living mulch", "more than six inches", "six inches or more", "at least six inches", "at least a foot from the trunk"
        " is", "mulched, grass-free")
CULTIVAR = re.compile(r"\bcultivars?\b", re.I)
OP_KEYS = {"crop", "path", "kind", "old", "new", "cited_at", "reason", "subs"}
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
    if EM_DASH in s or EN_DASH in s:
        refuse(f"{tag}: an em or en dash in consumer copy")
    if BARE_DEGREE.search(s):
        refuse(f"{tag}: a temperature without °F")
    if CULTIVAR.search(s):
        refuse(f"{tag}: 'cultivar' in consumer copy")


def _cites(crop, blk):
    node = _value(crop, blk)
    if not isinstance(node, dict):
        return None, None
    return node.get("sources"), node.get("anchoring_urls")


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "subs": 0, "evidence_only": 0, "hill_inspected": 0,
         "ids_added": 0, "ids_moved": 0, "minted": 0, "noted": 0}
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
        allowed = staged.get(slug, [])
        stray = sorted(fmt(list(p)) for p in diff if not any(p[:len(a)] == a for a in allowed))
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
                refuse(f"op {i}: catalog op on {op['path']} (ruled mint: {list(MINTED)})")
            continue
        if op["crop"] not in CROPS:
            refuse(f"op {i}: {op['crop']} is outside this promote's five crops")
        if not any(p.match(op["path"]) for p in SCOPE):
            refuse(f"op {i} {op['crop']} {op['path']}: outside the ruled scope")
        if op["kind"] == "catalog":
            refuse(f"op {i}: a catalog op must name <catalog>")
    for crop in CROPS:
        if not any(op["crop"] == crop for op in ops):
            refuse(f"{crop}: the stage names no op on a ruled crop")
    # guard V + T + P
    decided = {}
    for d in dec:
        decided.setdefault((d["crop"], d["path"]), set()).add(d["decision"])
    for i, op in enumerate(ops):
        tag = f"op {i} {op['crop']} {op['path']}"
        got = _value(_target(post, op), op["path"])
        if compact(got) != compact(op["new"]):
            refuse(f"{tag}: the post value is not the op's `new`")
        if compact(got) == compact(op["old"]):
            refuse(f"{tag}: a no-op (new == old)")
        if op["kind"] == "prose":
            if not (isinstance(op["subs"], list) and op["subs"]):
                refuse(f"{tag}: a prose op with no ruled substitutions")
            derived = op["old"]
            for o_sub, n_sub in op["subs"]:
                if not o_sub or derived.count(o_sub) != 1:
                    refuse(f"{tag}: a substitution's old text occurs {derived.count(o_sub) if o_sub else 0} times")
                derived = derived.replace(o_sub, n_sub)
                if n_sub:
                    _prose_ok(n_sub, tag)
                n["subs"] += 1
            if derived != op["new"]:
                refuse(f"{tag}: `new` is not `old` with the ruled substitutions (touched-leaf rule)")
            if not (isinstance(op["new"], str) and op["new"].strip()):
                refuse(f"{tag}: prose must stay a non-empty string")
        elif op["subs"] is not None:
            refuse(f"{tag}: subs on a {op['kind']} op")
    # guard E
    man = manifest(evidence_dir)
    text_cache = {}
    prose = {(op["crop"], op["path"]): op for op in ops if op["kind"] == "prose"}
    rows_for, seen = {}, set()
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"], r["sha256"], r["quote"])
        if key in seen:
            refuse(f"{tag}: a duplicate row")
        seen.add(key)
        op = prose.get((r["crop"], r["entry_id"]))
        if op is None:
            refuse(f"{tag}: not a staged prose op")
        if not any(r["value"] == n_sub and n_sub for _o, n_sub in op["subs"]):
            refuse(f"{tag}: its value is not one of the op's new substrings")
        cached_quote(r, man, evidence_dir, text_cache, tag)
        if r["source_id"] not in post["source_catalog"]:
            refuse(f"{tag}: {r['source_id']} is not in source_catalog")
        if op["cited_at"] is not None:
            srcs, anchors = _cites(qidx[r["crop"]], op["cited_at"])
            if anchors is None:
                refuse(f"{tag}: cited_at {op['cited_at']!r} names no citation block")
            if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:
                refuse(f"{tag}: {op['cited_at']} anchors do not carry {r['source_id']} at the row's url")
            if not srcs or r["source_id"] not in srcs:
                refuse(f"{tag}: {op['cited_at']} sources do not name {r['source_id']}")
        elif "evidence-only" not in decided.get((r["crop"], r["entry_id"]), ()):
            refuse(f"{tag}: an uncited string with no evidence-only DECISIONS row")
        rows_for.setdefault((r["crop"], r["entry_id"], r["value"]), []).append(r)
    n["evidence_rows"] = len(ev)
    for (crop, path), op in sorted(prose.items()):
        for o_sub, n_sub in op["subs"]:
            if n_sub and (crop, path, n_sub) not in rows_for:
                refuse(f"{crop} {path}: the new clause {n_sub[:60]!r} has no EVIDENCE row")
            if not n_sub and "deleted" not in decided.get((crop, path), ()):
                refuse(f"{crop} {path}: a deletion with no `deleted` DECISIONS row")
        if op["cited_at"] is None:
            n["evidence_only"] += 1
    # guard A + X
    blocks = {(op["crop"], op["cited_at"]) for op in ops if op["kind"] in ("sources", "anchors")}
    for crop, blk in sorted(blocks):
        srcs, anchors = _cites(qidx[crop], blk)
        osrcs, oanchors = _cites(pidx[crop], blk)
        if srcs is None or anchors is None or set(srcs) != set(anchors):
            refuse(f"{crop} {blk}: sources and anchoring_urls name different ids")
        if len(srcs) != len(set(srcs)):
            refuse(f"{crop} {blk}: a source id listed twice")
        used = {r["source_id"] for (c, p, _v), rows in rows_for.items() if c == crop and prose[(c, p)]["cited_at"] == blk
                for r in rows}
        decs = lambda sid: decided.get((crop, f"{blk}.anchoring_urls.{sid}"), set())  # noqa: E731
        # the re-key map, read off the rekey DECISIONS rows ("<from> -> <to> at the same url ...")
        remap = {}
        for d in dec:
            if d["crop"] == crop and d["decision"] == "rekey" and d["path"].startswith(f"{blk}.anchoring_urls."):
                m = re.match(r"(\S+) -> (\S+) ", d["reason"])
                to = d["path"].rsplit(".", 1)[1]
                if not m or m.group(2) != to:
                    refuse(f"{crop} {blk}: rekey DECISIONS row for {to} does not name '<from> -> {to}'")
                remap[m.group(1)] = to
        for frm, to in remap.items():
            if frm not in oanchors or to not in anchors or oanchors[frm].get("url") != anchors[to].get("url"):
                refuse(f"{crop} {blk}: re-key {frm} -> {to} does not keep the url")
            n["ids_moved"] += 1
        old_t = {remap.get(k, k): v for k, v in oanchors.items()}
        for sid in sorted(set(anchors) - set(old_t)):
            if sid in used or "kept" in decs(sid):
                n["ids_added"] += 1
            else:
                refuse(f"{crop} {blk}: added id {sid} supports no evidenced clause")
        for sid in sorted(set(old_t) - set(anchors)):
            if "cg009-off" not in decs(sid) or "CG009" not in (old_t[sid].get("url") or ""):
                refuse(f"{crop} {blk}: id {sid} removed with no cg009-off DECISIONS row on a CG009 anchor")
        for sid in sorted(set(anchors) & set(old_t)):
            if anchors[sid]["url"] != old_t[sid]["url"] and "repoint" not in decs(sid):
                refuse(f"{crop} {blk}: {sid} moved url with no repoint DECISIONS row")
    # guard L
    for i, op in enumerate(ops):
        if op["kind"] != "ladder":
            continue
        crop, blk, method = REMOVED_RUNG
        if (op["crop"], op["path"]) != (crop, f"{blk}.control_ladder"):
            refuse(f"op {i}: a ladder op on {op['crop']} {op['path']} (ruled: {crop} {blk})")
        old, new = op["old"], op["new"]
        gone = [r for r in old if r.get("method") == method]
        if len(new) != len(old) - 1 or len(gone) != 1 or [r for r in old if r is not gone[0]] != new:
            refuse(f"op {i}: the ladder is not the base ladder minus the {method} rung, order kept")
    # guard K: only the named finding moves, and only by gaining a progress note (status, and every other field, unchanged)
    for i, op in enumerate(ops):
        if op["kind"] != "record":
            continue
        if "record-only" not in decided.get((op["crop"], op["path"]), ()):
            refuse(f"op {i} {op['crop']}: no record-only DECISIONS row")
        old, new = op["old"], op["new"]
        if [f["id"] for f in old] != [f["id"] for f in new]:
            refuse(f"op {i} {op['crop']}: open_findings ids or order changed")
        for f_old, f_new in zip(old, new):
            if compact(f_old) == compact(f_new):
                continue
            if (op["crop"], f_new["id"]) not in NOTED:
                refuse(f"op {i} {op['crop']} {f_new['id']}: a finding outside the ruled note changed")
            if set(f_new) - set(f_old) != {"progress_note"} or set(f_old) - set(f_new):
                refuse(f"op {i} {f_new['id']}: only a progress_note may be added")
            if compact({k: v for k, v in f_new.items() if k != "progress_note"}) != compact(f_old):
                refuse(f"op {i} {f_new['id']}: a field other than progress_note moved (status stays open)")
            if not (f_new["progress_note"] or "").strip() or PENDING in f_new["progress_note"]:
                refuse(f"op {i} {f_new['id']}: an empty progress note")
            n["noted"] += 1
    # guard C
    for i, op in enumerate(ops):
        if op["kind"] != "catalog":
            continue
        new = op["new"]
        if not isinstance(new, dict) or new.get("id") != op["path"]:
            refuse(f"catalog {op['path']}: its id is {(new or {}).get('id')!r}")
        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):
            refuse(f"catalog {op['path']}: a minted id must be document-scoped and titled")
        if new.get("tier") != "T1":
            refuse(f"catalog {op['path']}: a minted id must be T1")
        man_urls = {u for urls in man.values() for u in urls}
        anchored = [a["url"] for c in CROPS for blk in (FR, "companions", "watering")
                    for k, a in ((_cites(qidx[c], blk)[1]) or {}).items() if k == op["path"]]
        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev) and \
                not (anchored and all(u in man_urls for u in anchored)):
            refuse(f"catalog {op['path']}: neither an EVIDENCE row at its url nor a MANIFEST-listed anchor cites it")
        n["minted"] += 1
    # guard H
    for (crop, path), op in prose.items():
        for g in GONE:
            if g in _value(qidx[crop], path):
                refuse(f"{crop} {path}: still carries {g!r}")
    for crop in ("lemon", "orange-navel"):
        _s, anc = _cites(qidx[crop], FR)
        cg = {k: a for k, a in (anc or {}).items() if "CG009" in (a.get("url") or "")}
        if list(cg) != [CG009_ID] or cg[CG009_ID].get("note") != CG009_NOTE:
            refuse(f"{crop} {FR}: CG009 must be cited once, under {CG009_ID}, with the commercial-page scope note "
                   f"(amendment stop 1); found {sorted(cg)}")
    on_br = _value(qidx["orange-navel"], BR)
    if any(r.get("method") == "splash_barrier_mulch" for r in on_br.get("control_ladder") or []):
        refuse("orange-navel brown rot still carries the splash_barrier_mulch rung (ruling D)")
    if (on_br.get("anchoring_urls") or {}).get("uc_ipm", {}).get("url") != BR_UC_IPM:
        refuse("orange-navel brown rot uc_ipm is not the cached home-and-landscape page (ruling D)")
    for crop, fid in NOTED:
        f = next(x for x in qidx[crop]["verification_status"]["open_findings"] if x["id"] == fid)
        if f.get("status") != "open" or not f.get("progress_note"):
            refuse(f"{crop} {fid}: must stay open and carry its progress note (amendment stop 2)")
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
    print(f"  inspected         {n['ops']} ops ({n['subs']} substitutions); whole_crop_gate PASS on {n['gated_crops']} "
          f"edited crops, then gate_all PASS; {n['evidence_rows']} evidence rows; {n['decisions']} decisions; "
          f"{n['evidence_only']} evidence-only strings; {n['ids_added']} ids added, {n['ids_moved']} re-keyed; "
          f"{n['minted']} minted; {n['noted']} finding noted; match inspected {n['hill_inspected']} consumer leaves")
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
