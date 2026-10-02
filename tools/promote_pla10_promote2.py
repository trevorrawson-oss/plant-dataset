#!/usr/bin/env python3
"""promote_pla10_promote2 -- PLA-10 PROMOTE 2, first rows: apple's rootstock spacing overrides (R1) and the
D1a [CORRECTION ...] appends on the in-canonical *_pilot_spacing_* open findings.
Spec docs/specs/pla10-field-shape.md §5, §10.2; SESSION3_HANDOFF.md owed items 1 and 2. Base cf1d480d
(promote 1, d021116). Built 2026-10-02 in promote 2's session-1 tools commit, BEFORE any stage exists.
Nothing here authors a value. The support entries and heights (spec §10.2) extend this promote in a later
tools commit, with their own stage keys, guards and mutations.

THE TWO RECORD ALLOWANCES (owed items 1 and 2), and nothing wider:
  (R) a rootstock_options[] row may gain spacing_inches ([lo, hi] or null) and, ONLY while that override is
      non-null, ONE new source appended to its `sources` plus that source's `anchoring_urls` key. Every
      other rootstock key, every existing anchor, and a null-override row's citation stay byte-identical.
  (F) an open finding under verification_status.open_findings[], named by its `id`, may have exactly one
      dated correction line APPENDED to its `summary` (docs/verification_log_ref_convention.md format).
      The base summary stays byte-for-byte as the prefix. No other verification_status key is writable:
      status, launch flags, the log ref, field_additions, other findings, and other finding keys refuse.

INPUT (the stage, default tools/staging/pla10_promote2/):
  crops/<slug>.json:
    {"slug": ..., "decision": "<the decision row: page, quoted figure, why>",
     "rootstock_spacing": [{"name": <row name>, "spacing_inches": [lo, hi] | null,
                            "add_source": {"id": <catalog id>, "url": ..., "verified": <date>}}],  # non-null only
     "finding_corrections": [{"id": <open finding id>, "append": " [CORRECTION <date>: <what> -- see <ref>.]"}]}
  EVIDENCE.tsv: crop, entry_id, field, value, source_id, url, sha256, quote (promote 1's columns);
    a rootstock override's entry_id is "rootstock_options[name=<row name>]", field "spacing_inches".

WHY EACH GUARD EXISTS.
 R. OVERRIDES ARE R1'S AND ONLY R1'S. rootstock_spacing is ruled for ROOTSTOCK_CROPS (a literal: apple).
    The stage names EVERY row of the crop exactly once (set equality both ways), so a null is an authored
    claim (M26 = the crop basis), never an omission. The base carries no override yet (measured 0 on
    cf1d480d). A value is null or [lo, hi] with 0 < lo <= hi. add_source is legal only on a non-null
    override, must be a catalog id the row does not already cite, carries exactly id, url, verified, and its
    url is a DOCUMENT, not a bare host (A63's is_bare, imported): A63 fails only a SOLE bare anchor, and the
    added source sits beside the row's existing umd_ext, which states no spacing, so A63 alone would pass a
    number resting on a homepage.
 E. EVERY OVERRIDE IS CITED TO BYTES. A non-null override has an EVIDENCE row naming the same value, a
    source the row cites and the row's own anchoring url; the bytes exist, hash to their name, are in
    MANIFEST.tsv under that url, contain the quote, and the quote states an endpoint (inches or feet).
    The reading is pla10_promote_common's, byte-identical to promote 1's (the suite pins it).
 F. A CORRECTION APPENDS, IT NEVER REWRITES. `append` is exactly one correction line with a real date and a
    "-- see <ref>." pointer, nothing before or after it; the finding id matches exactly one finding; one
    correction per finding per stage; a summary already ending with it refuses (no double-apply). After
    the transform the summary must equal base + append, byte for byte.
 B. BLAST RADIUS, SET BEFORE VALUE. Roster order and top-level key set first, then every non-crop top-level
    value and every shell byte-identical; on each certified crop the changed LEAF paths (two-sided: added
    and removed keys count) are a subset of exactly what (R) and (F) allow for that crop. Then values: each
    override equals the stage's (a dropped null counts), sources == base + [add_source.id], the new anchor
    is the stage's.
 G. THE GATES RUN ON THE POST-STATE: A44 armed, A62's ratchet, A63 bare-host, numeric_sanity (it bounds
    rootstock_options[].spacing_inches at 1-360 in), display_readiness.
 A STAGE THAT NAMES NO CROP REFUSES: an empty stage would "pass" having inspected nothing.

Usage:
  promote_pla10_promote2.py --check [--stage DIR] [--evidence DIR]
  promote_pla10_promote2.py --out /path/scratch.json
  promote_pla10_promote2.py --expect-sha <sha>          # writes canonical, on approval only
"""
import argparse, copy, csv, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import planting_layout_gate as PLG  # noqa: E402
from bare_host_gate import is_bare  # noqa: E402  -- A63's predicate, imported, never retyped
from pla10_promote_common import (EVIDENCE_COLS, compact, leaf_diff, manifest, norm_text,  # noqa: E402
                                  pdf_text, quote_states, serialize, sha256_bytes)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla10_promote2")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "cf1d480dfc926b226f63fde2fbdbc548e9d06487ed749e7431a06710431f2e49"  # promote 1, d021116
CERTIFIED = "verified_gs_arc"

# Literals (R1, ruled 2026-09-30 / 2026-10-01), never computed from the walk they bound.
ROOTSTOCK_CROPS = ("apple",)
STAGE_KEYS = {"slug", "decision", "rootstock_spacing", "finding_corrections"}
ROW_KEYS = {"name", "spacing_inches", "add_source"}
ADD_SOURCE_KEYS = {"id", "url", "verified"}
CORRECTION = re.compile(r" \[CORRECTION (\d{4}-\d{2}-\d{2}): [^\[\]]+ -- see [^\[\]]+\.\]")


class Refused(Exception):
    pass


def refuse(msg):
    raise Refused(msg)


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def certified(c):
    return (c.get("verification_status") or {}).get("status") == CERTIFIED


def fmt(concrete):
    return "".join(f"[{s}]" if isinstance(s, int) else (f".{s}" if i else s) for i, s in enumerate(concrete))


def load_canonical(path=None):
    with open(path or CANON, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        refuse(f"canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


# ---------------------------------------------------------------- stage
def load_stage(stage_dir):
    crops = {}
    for p in sorted(glob.glob(os.path.join(stage_dir, "crops", "*.json"))):
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        slug = os.path.basename(p)[:-5]
        if s.get("slug") != slug:
            refuse(f"stage file {p}: slug {s.get('slug')!r} does not match its file name")
        extra = set(s) - STAGE_KEYS
        if extra:
            refuse(f"stage {slug}: unknown keys {sorted(extra)}")
        if not (isinstance(s.get("decision"), str) and s["decision"].strip()):
            refuse(f"stage {slug}: the decision row is empty")
        crops[slug] = s
    ev = []
    p = os.path.join(stage_dir, "EVIDENCE.tsv")
    if os.path.exists(p):
        with open(p, encoding="utf-8", newline="") as f:
            r = csv.DictReader(f, delimiter="\t")
            if tuple(r.fieldnames or ()) != EVIDENCE_COLS:
                refuse(f"EVIDENCE.tsv columns {r.fieldnames} != {list(EVIDENCE_COLS)}")
            ev = [dict(row) for row in r]
    return crops, ev


def _pair(v):
    return (isinstance(v, list) and len(v) == 2
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v) and 0 < v[0] <= v[1])


def _row_index(crop, name):
    return [i for i, r in enumerate(crop.get("rootstock_options") or []) if r.get("name") == name]


def _finding_index(crop, fid):
    of = (crop.get("verification_status") or {}).get("open_findings") or []
    return [i for i, f in enumerate(of) if isinstance(f, dict) and f.get("id") == fid]


# ---------------------------------------------------------------- the transform
def apply_to(pre, stage):
    post = copy.deepcopy(pre)
    idx = by_slug(post)
    for slug, s in stage.items():
        c = idx[slug]
        for r in s.get("rootstock_spacing") or []:
            row = c["rootstock_options"][_row_index(c, r["name"])[0]]
            row["spacing_inches"] = copy.deepcopy(r["spacing_inches"])
            a = r.get("add_source")
            if a:
                row["sources"] = list(row.get("sources") or []) + [a["id"]]
                row.setdefault("anchoring_urls", {})[a["id"]] = {"url": a["url"], "verified": a["verified"]}
        for fc in s.get("finding_corrections") or []:
            f = c["verification_status"]["open_findings"][_finding_index(c, fc["id"])[0]]
            f["summary"] = f["summary"] + fc["append"]
    return post


# ---------------------------------------------------------------- checks
def check_pre(pre, stage):
    if not stage:
        refuse("the stage names no crop: nothing would be inspected")
    idx = by_slug(pre)
    catalog = pre.get("source_catalog") or {}
    for c in pre["crops"]:
        for r in c.get("rootstock_options") or []:
            if "spacing_inches" in r:
                refuse(f"base already carries rootstock_options[].spacing_inches on {c['slug']} {r.get('name')}")
    n = {"crops": 0, "overrides": 0, "nulls": 0, "sources_added": 0, "corrections": 0}
    for slug, s in stage.items():
        c = idx.get(slug)
        if c is None or not certified(c):
            refuse(f"{slug}: not a certified crop")
        n["crops"] += 1
        rs = s.get("rootstock_spacing")
        if rs is not None:
            if slug not in ROOTSTOCK_CROPS:
                refuse(f"{slug}: rootstock_spacing is ruled for {list(ROOTSTOCK_CROPS)} only (R1)")
            names = [r.get("name") for r in rs]
            for nm in sorted({x for x in names if names.count(x) > 1}):
                refuse(f"{slug}: rootstock row {nm!r} is named twice")
            have = {r.get("name") for r in c.get("rootstock_options") or []}
            if set(names) != have:
                refuse(f"{slug}: rootstock_spacing names != the crop's rows; missing "
                       f"{sorted(have - set(names))}, extra {sorted(set(names) - have)}")
            for r in rs:
                tag = f"{slug} {r['name']}"
                if not set(r) <= ROW_KEYS or not {"name", "spacing_inches"} <= set(r):
                    refuse(f"{tag}: a rootstock_spacing row takes only name, spacing_inches, add_source")
                v = r["spacing_inches"]
                if v is not None and not _pair(v):
                    refuse(f"{tag}: spacing_inches must be null or [lo, hi] with 0 < lo <= hi: {v!r}")
                a = r.get("add_source")
                if a is None:
                    n["overrides" if v is not None else "nulls"] += 1
                    continue
                if v is None:
                    refuse(f"{tag}: add_source is allowed only while authoring a non-null spacing_inches")
                if not isinstance(a, dict) or set(a) != ADD_SOURCE_KEYS:
                    refuse(f"{tag}: add_source needs exactly id, url, verified")
                row = c["rootstock_options"][_row_index(c, r["name"])[0]]
                if a["id"] in (row.get("sources") or []) or a["id"] in (row.get("anchoring_urls") or {}):
                    refuse(f"{tag}: add_source {a['id']!r} is already in the row's sources")
                if a["id"] not in catalog:
                    refuse(f"{tag}: add_source {a['id']!r} is not in source_catalog")
                if is_bare(a["url"]):
                    refuse(f"{tag}: add_source url {a['url']!r} is a bare host; the override's number rests on "
                           f"this source alone (A63 passes a co-cited bare anchor, so the promote refuses it)")
                n["overrides"] += 1
                n["sources_added"] += 1
        fcs = s.get("finding_corrections")
        if fcs is not None:
            ids = []
            for fc in fcs:
                if not isinstance(fc, dict) or set(fc) != {"id", "append"}:
                    refuse(f"{slug}: a finding correction takes exactly id and append: {fc!r}")
                if fc["id"] in ids:
                    refuse(f"{slug}: finding {fc['id']!r} is corrected twice")
                ids.append(fc["id"])
                hits = _finding_index(c, fc["id"])
                if len(hits) != 1:
                    refuse(f"{slug}: open finding {fc['id']!r} matches {len(hits)} findings")
                tag = f"{slug} {fc['id']}"
                m = CORRECTION.fullmatch(fc["append"]) if isinstance(fc["append"], str) else None
                ok = m is not None
                if ok:
                    try:
                        datetime.date.fromisoformat(m.group(1))
                    except ValueError:
                        ok = False
                if not ok:
                    refuse(f"{tag}: append must be exactly one ' [CORRECTION <YYYY-MM-DD>: <what> -- see <ref>.]': "
                           f"{fc['append']!r}")
                summ = c["verification_status"]["open_findings"][hits[0]].get("summary")
                if not isinstance(summ, str):
                    refuse(f"{tag}: the finding has no string summary to append to")
                if summ.endswith(fc["append"]):
                    refuse(f"{tag}: the summary already ends with this correction")
                n["corrections"] += 1
    return n


def allowed_paths(pre_crop, s):
    allowed = set()
    for r in s.get("rootstock_spacing") or []:
        i = _row_index(pre_crop, r["name"])[0]
        allowed.add(("rootstock_options", i, "spacing_inches"))
        if r.get("add_source"):
            allowed.add(("rootstock_options", i, "sources"))
            allowed.add(("rootstock_options", i, "anchoring_urls", r["add_source"]["id"]))
    for fc in s.get("finding_corrections") or []:
        allowed.add(("verification_status", "open_findings", _finding_index(pre_crop, fc["id"])[0], "summary"))
    return allowed


def check_post(pre, post, stage, ev, evidence_dir):
    # guard B, sets first
    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:
        refuse("the roster changed (set or order)")
    if set(pre) != set(post):
        refuse(f"top-level keys changed: {sorted(set(pre) ^ set(post))}")
    for k in pre:
        if k != "crops" and compact(pre[k]) != compact(post[k]):
            refuse(f"top-level {k!r} changed")
    pidx, qidx = by_slug(pre), by_slug(post)
    for slug, a in pidx.items():
        b = qidx[slug]
        if not certified(a):
            if compact(a) != compact(b):
                refuse(f"shell {slug} changed")
            continue
        allowed = allowed_paths(a, stage.get(slug, {}))
        stray = sorted(fmt(list(p)) for p in leaf_diff(a, b)
                       if not any(p[:len(al)] == al for al in allowed))
        if stray:
            refuse(f"{slug}: changed outside what the stage names: {stray[:6]}")
    # guard B, values (guard R / F post-conditions)
    for slug, s in stage.items():
        a, b = pidx[slug], qidx[slug]
        for r in s.get("rootstock_spacing") or []:
            i = _row_index(a, r["name"])[0]
            ra, rb = a["rootstock_options"][i], b["rootstock_options"][i]
            tag = f"{slug} {r['name']}"
            if "spacing_inches" not in rb or compact(rb["spacing_inches"]) != compact(r["spacing_inches"]):
                refuse(f"{tag}: spacing_inches is not the stage's")
            add = r.get("add_source")
            if add:
                if (rb.get("sources") or []) != list(ra.get("sources") or []) + [add["id"]]:
                    refuse(f"{tag}: sources must be the base's plus exactly {add['id']!r}, appended")
                if (rb.get("anchoring_urls") or {}).get(add["id"]) != {"url": add["url"], "verified": add["verified"]}:
                    refuse(f"{tag}: anchoring_urls[{add['id']!r}] is not the stage's add_source")
        for fc in s.get("finding_corrections") or []:
            i = _finding_index(a, fc["id"])[0]
            fa = a["verification_status"]["open_findings"][i]
            fb = b["verification_status"]["open_findings"][i]
            if fb.get("summary") != fa["summary"] + fc["append"]:
                refuse(f"{slug} {fc['id']}: summary must be the base's, byte for byte, plus the append")
    # guard E
    n_ev = check_evidence(qidx, stage, ev, post.get("source_catalog") or {}, evidence_dir)
    # guard G
    r = PLG.roster(post, armed=True)
    if r["violations"]:
        refuse(f"planting_layout_gate (armed): {r['violations'][:5]}")
    why = PLG.refusal(r, armed=True)
    if why:
        refuse(f"planting_layout_gate (armed) REFUSED: {why}")
    import sourced_block_ratchet_gate as SBR
    import bare_host_gate as BH
    import numeric_sanity_gate as NS
    import display_readiness_gate as DR
    v = SBR.roster(post)[3]
    if v:
        refuse(f"A62 on the post-state: {v[:5]}")
    v = BH.roster(post)[4]
    if v:
        refuse(f"A63 on the post-state: {v[:5]}")
    for c in post["crops"]:
        if certified(c):
            v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)
            if v:
                refuse(f"{c['slug']}: numeric_sanity / display_readiness: {v[:3]}")
    return n_ev


ROW_ID = re.compile(r"rootstock_options\[name=([^\]]+)\]")


def check_evidence(post_idx, stage, ev, catalog, evidence_dir):
    man = manifest(evidence_dir)
    covered = set()
    text_cache = {}
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']} {r['field']})"
        c = post_idx.get(r["crop"])
        m = ROW_ID.fullmatch(r["entry_id"])
        hits = _row_index(c, m.group(1)) if (c is not None and m) else []
        if len(hits) != 1:
            refuse(f"{tag}: no such crop/row in the post-state")
        row = c["rootstock_options"][hits[0]]
        if r["field"] != "spacing_inches" or row.get("spacing_inches") is None:
            refuse(f"{tag}: the row carries no {r['field']}")
        if compact(row["spacing_inches"]) != r["value"]:
            refuse(f"{tag}: value {r['value']} != the row's {compact(row['spacing_inches'])}")
        if r["source_id"] not in (row.get("sources") or []):
            refuse(f"{tag}: source {r['source_id']!r} is not in the row's sources")
        if (row.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:
            refuse(f"{tag}: url is not the row's anchoring url for {r['source_id']!r}")
        if r["url"] not in man.get(r["sha256"], set()):
            refuse(f"{tag}: ({r['sha256'][:12]}, url) is not in {evidence_dir}/MANIFEST.tsv")
        files = glob.glob(os.path.join(evidence_dir, r["sha256"] + ".*"))
        if len(files) != 1:
            refuse(f"{tag}: {len(files)} cache files for {r['sha256'][:12]}")
        if r["sha256"] not in text_cache:
            raw = open(files[0], "rb").read()
            if sha256_bytes(raw) != r["sha256"]:
                refuse(f"{tag}: the cached bytes hash to {sha256_bytes(raw)[:12]}, not their name")
            if files[0].endswith(".pdf"):
                text_cache[r["sha256"]] = norm_text(pdf_text(raw))
            else:
                text_cache[r["sha256"]] = norm_text(raw.decode("utf-8", "replace"))
        q = norm_text(r["quote"])
        if len(q) < 12 or q not in text_cache[r["sha256"]]:
            refuse(f"{tag}: the quote is not in the cached bytes: {r['quote'][:80]!r}")
        if not quote_states(r["field"], json.loads(r["value"]), r["quote"]):
            refuse(f"{tag}: the quote states neither endpoint of {r['value']} (inches or feet)")
        covered.add((r["crop"], r["entry_id"]))
    for slug, s in stage.items():
        c = post_idx[slug]
        for rs in s.get("rootstock_spacing") or []:
            row = c["rootstock_options"][_row_index(c, rs["name"])[0]]
            for sid in row.get("sources") or []:
                if sid not in catalog:
                    refuse(f"{slug} {rs['name']}: source {sid!r} is not in source_catalog")
            eid = f"rootstock_options[name={rs['name']}]"
            if row.get("spacing_inches") is not None and (slug, eid) not in covered:
                refuse(f"{slug} {eid}: spacing_inches {compact(row['spacing_inches'])} has no EVIDENCE row")
    return len(covered)


def run(pre, stage, ev, evidence_dir):
    n = check_pre(pre, stage)
    post = apply_to(pre, stage)
    check_post(pre, post, stage, ev, evidence_dir)
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
        stage, ev = load_stage(args.stage)
        post, n = run(pre, stage, ev, args.evidence)
    except Refused as e:
        print(f"REFUSED: {e}")
        return 1
    print(f"  inspected         {n['crops']} staged crops; {n['overrides']} overrides + {n['nulls']} null "
          f"(every evidence-backed), {n['sources_added']} row sources added, {n['corrections']} corrections")
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
