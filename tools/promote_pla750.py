#!/usr/bin/env python3
"""promote_pla750 -- PLA-750 heat hold: the `sowing_heat_ceiling` field on the 30 reviewed crops (register #35),
`succession_policy.pause_in_heat` false on the 20 with no sourced sowing hold, D4 stage tips, D5 heat_effect
corrections (P5), D6 / catalog mints, and the eight live-data fixes. Base d72aeed3 (PLA-625 citrus promote 3b).

Nothing here authors a value. Every value is ruled (PLA-750 comments 47a09951, b963b423, 7c155149) and staged by
tools/staging/pla750/build_stage.py from p750_texts.py, each new clause carrying the hashed-page quote it rests
on. Guard structure derived from promote_pla625_p3a (copied, not imported: promotes must not import promotes).

INPUT (tools/staging/pla750/): ops.json, EVIDENCE.tsv (EVIDENCE_COLS), DECISIONS.tsv (crop, path, decision,
reason). Op kinds: catalog, field, pause, enum, prose, sources, anchors, tip_add, trigger_drop.

GUARDS (check_post): B blast radius (roster, top-level keys, every leaf change inside a staged op path, catalog
only gains the minted ids), S scope (the 30 ruled crops; each kind on its own path family; every ruled crop
carries a field op), V values (post == new, new != old), T touched-leaf (prose new == old with the ruled subs,
each old sub exactly once), P prose (no dash, no bare degree, no "cultivar" in a new clause or tip text),
E evidence (every cited prose clause, new tip and added citation has a hashed-page row at its block's anchor;
uncited and struck edits need their DECISIONS row; a struck edit only deletes words), F field
(sowing_heat_ceiling_gate SHAPE + PAUSE + BYTES on the whole post roster; inspected exactly 30, held 10),
N enum (exactly the three P5 crops, climate_threshold_gate clean on the post roster, NULL_STRESS_KNOWN firing),
D drops (exactly one named trigger removed, order kept), C catalog (ruled mints, T1, document-scoped, an evidence
row at the url), plus G: whole_crop_gate on every edited crop, then gate_all. A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla750.py --check
  promote_pla750.py --out /path/scratch.json
  promote_pla750.py --expect-sha <post sha>           # writes canonical, on approval only
"""
import argparse, copy, csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)
import climate_threshold_gate  # noqa: E402
import sowing_heat_ceiling_gate as shc  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla750")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "d72aeed3072ef0555bf5ed26a00b8f1d4ee188dd485bfaad8216bdeed770beda"  # PLA-625 citrus promote 3b
CATALOG, ABSENT = "<catalog>", "<absent>"
KINDS = ("catalog", "field", "pause", "enum", "prose", "sources", "anchors", "tip_add", "trigger_drop")
OP_KEYS = {"crop", "path", "kind", "old", "new", "reason", "subs", "cited_at"}
DECISION_COLS = ("crop", "path", "decision", "reason")
HELD = {"spinach": 80, "lettuce-leaf": 80, "cilantro-coriander": 75, "beet": 80, "radish": 75, "kohlrabi": 75,
        "sugar-snap-peas": 80, "snow-peas": 80, "calendula": 86, "viola": 75}
NOT_HELD = ("celery", "spring-onion", "broccoli", "cauliflower", "cabbage", "brussels-sprouts", "kale", "collards",
            "edamame", "borage", "carrot", "arugula", "dill", "turnip", "parsley", "bok-choy", "sweet-pea",
            "nasturtium", "chamomile", "sweet-alyssum")
CROPS = tuple(HELD) + NOT_HELD
ENUMS = {"sweet-pea", "sweet-alyssum", "nasturtium"}
MINTED = ("sare_necphm_arugula", "steiner_2010_arugula", "eberle_2014_calendula", "ucanr_pub7243",
          "tamu_celery_crop_sheet")
D4_STAGES = {("brussels-sprouts", "sprout_formation"), ("cabbage", "head_forming"), ("kale", "harvest"),
             ("collards", "harvest"), ("cilantro-coriander", "established")}
DROPS = {("edamame", "condition", "HEAT_STRESS"), ("chamomile", "condition", "high")}
# the path family each kind may touch
PATHS = {
    "field": re.compile(r"sowing_heat_ceiling\Z"),
    "pause": re.compile(r"succession_policy\.pause_in_heat\Z"),
    "enum": re.compile(r"heat_effect\Z"),
    "prose": re.compile(r"(tips_by_stage\.[a-z_]+\[(\d+|tip_id=[a-z0-9_]+)\]\.text_(seasoned|beginner)"
                        r"|start_method\.notes_(seasoned|beginner)"
                        r"|weather_triggers\[condition=HEAT_STRESS\]\.body_(seasoned|beginner))\Z"),
    "sources": re.compile(r"tips_by_stage\.[a-z_]+\[\d+\]\.sources\Z"),
    "anchors": re.compile(r"tips_by_stage\.[a-z_]+\[\d+\]\.anchoring_urls\Z"),
    "tip_add": re.compile(r"tips_by_stage\.[a-z_]+\Z"),
    "trigger_drop": re.compile(r"weather_triggers\Z"),
}
EM_DASH, EN_DASH = "—", "–"
BARE_DEGREE = re.compile(r"\d\s*(?:degrees?\b|°(?!F))", re.I)
CULTIVAR = re.compile(r"\bcultivars?\b", re.I)
BARE_HOST = re.compile(r"https?://[^/]+/?\Z")
WORD = re.compile(r"[\w°'-]+")
# normalized page text by sha256: content-addressed, so one cache serves every call (cached_quote re-hashes the
# bytes on first read of each digest)
_TEXT = {}


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
    return (ops, _tsv(os.path.join(stage_dir, "EVIDENCE.tsv"), EVIDENCE_COLS, "EVIDENCE.tsv"),
            _tsv(os.path.join(stage_dir, "DECISIONS.tsv"), DECISION_COLS, "DECISIONS.tsv"))


# ---------------------------------------------------------------- paths
def _locate(root, path):
    concrete = resolve(root, path)
    node = root
    for s in concrete[:-1]:
        node = node[s]
    return node, concrete[-1], concrete


def _value(root, path):
    try:
        parent, key, _c = _locate(root, path)
    except Refused:
        return ABSENT
    if isinstance(parent, dict):
        return parent[key] if key in parent else ABSENT
    return parent[key]


def _target(data, op):
    return data["source_catalog"] if op["crop"] == CATALOG else by_slug(data).get(op["crop"])


# ---------------------------------------------------------------- the transform
def check_pre(pre, ops):
    idx = by_slug(pre)
    for i, op in enumerate(ops):
        if op["crop"] != CATALOG and op["crop"] not in idx:
            refuse(f"op {i}: {op['crop']} is not a crop")
        got = _value(_target(pre, op), op["path"])
        if compact(got) != compact(op["old"]):
            refuse(f"op {i} {op['crop']} {op['path']}: the base value is not the op's `old`")
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


def _is_deletion(old, new):
    """new keeps old's words in order and drops at least one: a strike, not new text."""
    ow, nw = WORD.findall(old.lower()), WORD.findall(new.lower())
    it = iter(ow)
    return len(nw) < len(ow) and all(w in it for w in nw)


def check_post(pre, post, ops, ev, dec, evidence_dir):
    n = {"ops": len(ops), "evidence_rows": len(ev), "decisions": len(dec), "subs": 0, "struck": 0,
         "tips_added": 0, "ids_added": 0, "minted": 0, "dropped": 0}
    pidx, qidx = by_slug(pre), by_slug(post)
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
    for slug in pidx:
        added_keys = set(qidx[slug]) - set(pidx[slug])
        if set(pidx[slug]) - set(qidx[slug]) or added_keys - ({"sowing_heat_ceiling"} if slug in CROPS else set()):
            refuse(f"{slug}: top-level crop keys changed: {sorted(set(pidx[slug]) ^ set(qidx[slug]))}")
        diff = leaf_diff(pidx[slug], qidx[slug])
        allowed = staged.get(slug, [])
        stray = sorted(fmt(list(p)) for p in diff if not any(p[:len(a)] == a for a in allowed))
        if stray:
            refuse(f"{slug}: changed outside the staged ops: {stray[:5]}")
    if set(pre["source_catalog"]) - set(post["source_catalog"]):
        refuse("source_catalog lost ids")
    if set(post["source_catalog"]) - set(pre["source_catalog"]) != set(MINTED):
        refuse(f"source_catalog gained {sorted(set(post['source_catalog']) - set(pre['source_catalog']))}, "
               f"not the ruled mints")
    for sid in pre["source_catalog"]:
        if compact(pre["source_catalog"][sid]) != compact(post["source_catalog"][sid]):
            refuse(f"source_catalog {sid} changed")
    # guard S
    for i, op in enumerate(ops):
        if op["crop"] == CATALOG:
            if op["kind"] != "catalog" or op["path"] not in MINTED:
                refuse(f"op {i}: catalog op on {op['path']} (ruled mints: {list(MINTED)})")
            continue
        if op["kind"] == "catalog":
            refuse(f"op {i}: a catalog op must name <catalog>")
        if op["crop"] not in CROPS:
            refuse(f"op {i}: {op['crop']} is outside the 30 ruled crops")
        if not PATHS[op["kind"]].match(op["path"]):
            refuse(f"op {i} {op['crop']} {op['path']}: outside the {op['kind']} path family")
        if op["kind"] == "pause" and (op["crop"] not in NOT_HELD or op["old"] is not True or op["new"] is not False):
            refuse(f"op {i}: pause op on {op['crop']} ({op['old']!r} -> {op['new']!r})")
        if op["kind"] == "enum" and (op["crop"] not in ENUMS or (op["old"], op["new"]) != ("heat_tolerant",
                                                                                          "quality_loss")):
            refuse(f"op {i}: enum op on {op['crop']} ({op['old']!r} -> {op['new']!r})")
    for crop in CROPS:
        if not any(op["crop"] == crop and op["kind"] == "field" for op in ops):
            refuse(f"{crop}: no sowing_heat_ceiling op on a ruled crop")
        if (crop in NOT_HELD) != any(op["crop"] == crop and op["kind"] == "pause" for op in ops):
            refuse(f"{crop}: a pause op must exist exactly for the 20 not-held crops")
    if {op["crop"] for op in ops if op["kind"] == "enum"} != ENUMS:
        refuse("the enum ops are not exactly the three P5 crops")
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
            if derived != op["new"] or not op["new"].strip():
                refuse(f"{tag}: `new` is not `old` with the ruled substitutions (touched-leaf rule)")
        elif op["subs"] is not None:
            refuse(f"{tag}: subs on a {op['kind']} op")
    # guard E
    man, tc = manifest(evidence_dir), _TEXT
    rows_by_entry = {}
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']})"
        cached_quote(r, man, evidence_dir, tc, tag)
        if r["source_id"] not in post["source_catalog"]:
            refuse(f"{tag}: {r['source_id']} is not in source_catalog")
        rows_by_entry.setdefault((r["crop"], r["entry_id"]), []).append(r)
    for op in ops:
        tag = f"{op['crop']} {op['path']}"
        if op["kind"] == "prose":
            rows = rows_by_entry.get((op["crop"], op["path"]), [])
            dset = decided.get((op["crop"], op["path"]), set())
            if "struck" in dset:
                for o_sub, n_sub in op["subs"]:
                    if not _is_deletion(o_sub, n_sub):
                        refuse(f"{tag}: a struck edit adds words ({n_sub[:50]!r})")
                n["struck"] += 1
                continue
            if not rows:
                refuse(f"{tag}: a new clause with no EVIDENCE row")
            for r in rows:
                if not any(r["value"] == n_sub for _o, n_sub in op["subs"]):
                    refuse(f"{tag}: an EVIDENCE row's value is not one of the op's new substrings")
            if op["cited_at"] is None:
                if "evidence-only" not in dset:
                    refuse(f"{tag}: an uncited string with no evidence-only DECISIONS row")
                continue
            anchors = (_value(qidx[op["crop"]], op["cited_at"]) or {}).get("anchoring_urls") or {}
            for r in rows:
                if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:
                    refuse(f"{tag}: {op['cited_at']} does not anchor {r['source_id']} at the row's url")
        elif op["kind"] == "tip_add":
            old, new = op["old"], op["new"]
            if len(new) != len(old) + 1 or compact(new[:-1]) != compact(old):
                refuse(f"{tag}: tip_add must append exactly one tip, existing tips byte-identical")
            t = new[-1]
            if (op["crop"], op["path"].split(".")[1]) not in D4_STAGES:
                refuse(f"{tag}: a tip added outside the ruled stages")
            ids = [x.get("tip_id") for tips in qidx[op["crop"]]["tips_by_stage"].values() for x in tips or []]
            if ids.count(t.get("tip_id")) != 1:
                refuse(f"{tag}: tip_id {t.get('tip_id')!r} is not unique on the crop")
            for k in ("text_seasoned", "text_beginner"):
                if not (isinstance(t.get(k), str) and t[k].strip()):
                    refuse(f"{tag}: the new tip has no {k}")
                _prose_ok(t[k], f"{tag} {k}")
            if set(t.get("sources") or []) != set(t.get("anchoring_urls") or {}) or not t.get("sources"):
                refuse(f"{tag}: the new tip's sources and anchoring_urls differ or are empty")
            rows = rows_by_entry.get((op["crop"], f"{op['path']}[tip_id={t['tip_id']}]"), [])
            for sid in t["sources"]:
                if not any(r["source_id"] == sid and r["url"] == t["anchoring_urls"][sid]["url"] for r in rows):
                    refuse(f"{tag}: the new tip cites {sid} with no EVIDENCE row at its url")
            n["tips_added"] += 1
        elif op["kind"] == "anchors":
            blk = op["cited_at"]
            old = op["old"] if isinstance(op["old"], dict) else {}
            srcs = _value(qidx[op["crop"]], blk + ".sources")
            if set(srcs) != set(op["new"]) or len(srcs) != len(set(srcs)):
                refuse(f"{tag}: sources and anchoring_urls name different ids")
            for sid, a in old.items():
                if compact(op["new"].get(sid)) != compact(a):
                    refuse(f"{tag}: existing anchor {sid} changed or removed")
            for sid in set(op["new"]) - set(old):
                url = op["new"][sid]["url"]
                if BARE_HOST.match(url):
                    refuse(f"{tag}: added anchor {sid} is a bare host")
                hits = [r for (c, e), rs in rows_by_entry.items() if c == op["crop"] and
                        (e == blk or e.startswith(blk + ".")) for r in rs if r["source_id"] == sid and r["url"] == url]
                if not hits:
                    refuse(f"{tag}: added id {sid} supports no EVIDENCE row at {url}")
                n["ids_added"] += 1
        elif op["kind"] == "sources":
            old = op["old"] if isinstance(op["old"], list) else []
            if op["new"][:len(old)] != old:
                refuse(f"{tag}: existing sources reordered or removed")
        elif op["kind"] == "trigger_drop":
            old, new = op["old"], op["new"]
            gone = [x for x in old if not any(compact(x) == compact(y) for y in new)]
            if len(new) != len(old) - 1 or len(gone) != 1 or [x for x in old if x is not gone[0]] != new:
                refuse(f"{tag}: trigger_drop must remove exactly one trigger, order kept")
            key = next(((op["crop"], k, gone[0].get(k)) for k in ("condition",) if
                        (op["crop"], k, gone[0].get(k)) in DROPS), None)
            if key is None or "struck" not in decided.get((op["crop"], f"weather_triggers[{key[1]}={key[2]}]"), ()):
                refuse(f"{tag}: the removed trigger is not a ruled strike with its DECISIONS row")
            n["dropped"] += 1
    # guard F
    held, nulls, _todo = shc.coverage(post["crops"])
    if sorted(held) != sorted(HELD) or sorted(nulls) != sorted(NOT_HELD):
        refuse(f"sowing_heat_ceiling population: held {sorted(held)}, not held {sorted(nulls)}")
    v = []
    shc_cache = _TEXT
    shc_man = shc.load_manifest(evidence_dir)
    for c in post["crops"]:
        v += shc.check_crop(c, post["source_catalog"])
        if "sowing_heat_ceiling" in c:
            v += shc.check_bytes(c, shc_man, evidence_dir, shc_cache)
    if v:
        refuse(f"sowing_heat_ceiling_gate on the post roster: {v[:4]}")
    for slug, t in HELD.items():
        if qidx[slug]["sowing_heat_ceiling"]["temp_f"] != t:
            refuse(f"{slug}: sowing_heat_ceiling.temp_f is not the ruled {t}")
    # P4 (heat_threshold_f unchanged) is enforced by guard B: no op kind may stage it.
    n["field_inspected"] = len(held) + len(nulls)
    # guard N
    cv = [x for c in post["crops"] for x in climate_threshold_gate.check_crop(c)]
    cv += climate_threshold_gate.stale_null_stress(post["crops"])
    if cv:
        refuse(f"climate_threshold_gate on the post roster: {cv[:4]}")
    # guard C
    for op in ops:
        if op["kind"] != "catalog":
            continue
        new = op["new"]
        if not isinstance(new, dict) or new.get("id") != op["path"] or new.get("tier") != "T1":
            refuse(f"catalog {op['path']}: id/tier wrong")
        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):
            refuse(f"catalog {op['path']}: a minted id must be document-scoped and titled")
        if not any(r["source_id"] == op["path"] and r["url"] == new["url"] for r in ev):
            refuse(f"catalog {op['path']}: no EVIDENCE row at its url")
        n["minted"] += 1
    return n


def gate_post(post, slugs):
    """whole_crop_gate on every edited crop, then gate_all, against a scratch copy of the post-state (guard G)."""
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "post.json")
        with open(p, "wb") as f:
            f.write(serialize(post))
        passed = 0
        for slug in sorted(slugs):
            r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, p],
                               capture_output=True, text=True)
            if r.returncode != 0:
                refuse(f"whole_crop_gate {slug} rc={r.returncode}: {(r.stdout + r.stderr)[-500:]}")
            passed += r.stdout.count("\nGATE: PASS")
        if passed != len(slugs):
            refuse(f"whole_crop_gate printed {passed} PASS verdicts for {len(slugs)} crops")
        r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), p], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode != 0:
        refuse(f"gate_all rc={r.returncode}: {out[-800:]}")
    m = re.search(r"gate_all: ran whole_crop_gate on (\d+) certified crop", out)
    certified = sum(1 for c in post["crops"] if (c.get("verification_status") or {}).get("status") == "verified_gs_arc")
    if not m or int(m.group(1)) != certified or certified == 0:
        refuse(f"gate_all did not report its population ({m.group(1) if m else 'none'} vs {certified} certified)")
    return passed


def run(pre, ops, ev, dec, evidence_dir, gates=True):
    n = {"base_ops": check_pre(pre, ops)}
    post = apply_to(pre, ops)
    n.update(check_post(pre, post, ops, ev, dec, evidence_dir))
    n["gated_crops"] = gate_post(post, {op["crop"] for op in ops if op["crop"] != CATALOG}) if gates else 0
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
    print(f"  inspected         {n['ops']} ops ({n['subs']} substitutions, {n['struck']} struck); "
          f"sowing_heat_ceiling on {n['field_inspected']} crops (bytes checked); {n['tips_added']} tips added; "
          f"{n['ids_added']} ids added; {n['minted']} minted; {n['dropped']} triggers dropped; "
          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; whole_crop_gate PASS on "
          f"{n['gated_crops']} edited crops, then gate_all PASS")
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
