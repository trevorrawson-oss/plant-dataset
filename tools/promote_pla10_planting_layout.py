#!/usr/bin/env python3
"""promote_pla10_planting_layout -- PLA-10 PROMOTE 1: planting_layout as a list of cited entries, the
spacing mirrors, the six blend repairs, apple's rootstock basis, the microgreens to null.
[RULED 2026-10-01: apple's rootstock_options[].spacing_inches OVERRIDES are DEFERRED (no number lands
uncited); the stage key rootstock_spacing is withdrawn until a tools change lets a promote add a source to
a rootstock row. apple's crop-level basis move still lands, through its planting_layout entry.]
Spec docs/specs/pla10-field-shape.md (§1, §2, §3, §5, §9, §10.1); rulings D1-D12, R1-R5.
Base c5fc3d13 (PLA-532). Built 2026-10-01 in the tools commit; the STAGE is authored in sessions 2-3
(docs/kickoffs/56-pla10-promote1-authoring-worklist.md). Nothing here authors a value.

INPUT (the stage, default tools/staging/pla10_promote1/):
  crops/<slug>.json, one per certified crop that is NOT zone_independent (the fixed list: 113):
    {"slug": ..., "decision": "<the decision row: page, quoted figure, why this default>",
     "planting_layout": [<entries, spec §1.1, verbatim as they will land>],
     "retired_anchor": {<source_id>: "moved" | {"dropped": "<reason>"}}   iff the crop carries
                        spacing_inches_anchoring_urls today (11 crops); "moved" means that exact
                        (source_id, url) is in some entry's anchoring_urls,
     "edits": [{"path": "growth_stages[id=seedling].note_beginner", "new": <value>, "reason": "..."}],
     "restatements": [{"path": ..., "verdict": "agrees" | "edited", "note": "..."}]}
  EVIDENCE.tsv: crop, entry_id, field, value (compact JSON), source_id, url, sha256, quote
    -- one row per (entry, numeric field) at least; the bytes live in tools/.evidence_cache/<sha256>.*
       and are listed in its MANIFEST.tsv (the PLA-532 convention).
  The 8 zone_independent crops take NO stage file: they are written mechanically
  (planting_layout [], spacing_inches null, row_spacing_inches null, row_spacing_reason not_applicable).

WHY EACH GUARD EXISTS.
 1. THE FIXED LIST. The staged crop set equals the certified non-zone_independent set exactly (set
    equality, both directions), and after the promote the null-spacing set equals NULL_SPACING_EXPECTED,
    a literal: the 8 microgreens (spec §10.1, "asserted as an enumerated constant, never derived").
 2. EVERY NUMBER IS CITED TO BYTES. Each numeric field on each entry (in_row_inches, hill_spacing_inches,
    a non-null row_spacing_inches, plants_per_hill, mature_height_ft) has an EVIDENCE row naming the same
    value, a source the entry cites and the entry's own anchoring url; the row's bytes exist, hash to
    their name, are in MANIFEST.tsv under that url, CONTAIN the quote, and the quote states the figure
    (an endpoint in inches or feet). Every entry source is in source_catalog. The only exception is an
    R5 migration waiver (planting_layout_migration_known), whose entry must byte-equal the pre-promote
    spacing_inches; the gate checks the same thing, this checks it against the BASE.
    PDF pages (ruled 2026-10-01): the manifest keeps hashing the RAW PDF bytes (that is the evidence);
    the substring check for a `.pdf` cache file runs against pypdf's text extraction of those bytes,
    because every fetched extension PDF is Flate-compressed and the raw bytes never contain the quote
    (measured on 7 of session 2's 93 crops). The extractor is pinned in PDF_TEXT_EXTRACTOR (pypdf 6.14.2
    at the ruling) so the extraction is reproducible; a different pypdf is a re-measurement, not a
    silent change. Number words: digits, the word table and the IDIOMS table ('a foot' = 1 ft, so
    "with a foot between rows" states 12 in; "two feet" and "a foot or two" read through the word table).
 3. NO ANCHOR IS LOST. A retired spacing_inches_anchoring_urls entry is either moved (that source and
    url appear in an entry) or dropped with a recorded reason (lemon's mis-keyed hs1153, spec §2.4).
 4. RESTATEMENTS ARE ADJUDICATED, NOT SCANNED-AND-HOPED (R3, spec §9). On every crop whose
    spacing_inches moves, every string stating a distance next to a spacing word is listed by path in
    `restatements` ("agrees" with a note, or "edited" with the edit in `edits`). The scanner finds
    candidates; the author decides. An unadjudicated hit REFUSES.
 5. BLAST RADIUS, SET BEFORE VALUE. Roster and top-level key sets compared first; shells and every
    non-crop top-level key byte-identical; on each certified crop the changed LEAF paths (a two-sided
    walk: added and removed keys count) are a subset of what the stage names: the layout and the three
    mirror keys, the retired anchor, and the `edits` paths. Then values: each
    edited leaf equals its `new`, each layout equals its stage verbatim.
 6. THE GATES RUN ON THE POST-STATE, ARMED: planting_layout_gate (presence ON, floors), A62's ratchet
    (an uncited entry fails unless R5-waived), A63 bare-host, numeric_sanity, display_readiness.
 7. NO ROOTSTOCK OVERRIDE (R1's overrides DEFERRED, ruled 2026-10-01): the stage carries no
    rootstock_spacing (load_stage refuses the key as unknown), and a rootstock_options[].spacing_inches
    appearing in the post-state on any crop, apple included, is refused by guard 5 (a change the stage
    does not name). The apple-only override machinery was REMOVED with the ruling rather than left
    unreachable; the owed tools change re-adds it together with the row's own citation.

Usage:
  promote_pla10_planting_layout.py --check [--stage DIR] [--evidence DIR]
  promote_pla10_planting_layout.py --out /path/scratch.json
  promote_pla10_planting_layout.py --expect-sha <sha>          # writes canonical, on approval only
"""
import argparse, copy, csv, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import planting_layout_gate as PLG  # noqa: E402
import planting_layout_migration_known as MIG  # noqa: E402
# The shared readers (evidence, paths, diff, and the guard-4 restatement scanner: a distance next to a spacing
# word in any string leaf outside the citation machinery, deliberately wide, the author adjudicates every hit)
# were written here and moved byte-identically to cited_promote_common on 2026-10-03 (kickoff 60, ruling 5).
from cited_promote_common import (  # noqa: E402  -- the shared readers, moved here 2026-10-03
    PDF_TEXT_EXTRACTOR,
    IDIOMS,
    EVIDENCE_COLS,
    sha256_bytes,
    serialize,
    compact,
    leaf_diff,
    norm_text,
    _numbers,
    quote_states,
    pdf_text,
    manifest,
    Refused,
    refuse,
    DIST,
    SPACING_WORD,
    SKIP_SUBTREES,
    SEG,
    parse_path,
    resolve,
    fmt,
    set_at,
    spacing_strings,
    cached_quote,
)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla10_promote1")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "c5fc3d13764f6d08b24574bbb07ecb15f5cfddeb7ba80f7439a72d8829813e28"  # PLA-532, a181270
CERTIFIED = "verified_gs_arc"

# Literals measured on c5fc3d13 (2026-10-01), never computed from the walk they bound.
EXPECTED_CERTIFIED = 121
EXPECTED_STAGED = 113
NULL_SPACING_EXPECTED = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens",
                         "microgreens-mix", "pea-shoots", "radish-microgreens", "sunflower-sprouts",
                         "wheatgrass")
RETIRED_ANCHOR_CROPS = ("carrot", "celery", "cherry-tomato", "grape-tomato", "lemon", "lime", "potato",
                        "radish", "roma-tomato", "sweet-potato", "tomatillo")
LAYOUT_KEYS = ("planting_layout",) + PLG.MIRROR_KEYS
RETIRED = "spacing_inches_anchoring_urls"
NUMERIC_FIELDS = ("in_row_inches", "hill_spacing_inches", "row_spacing_inches", "plants_per_hill",
                  "mature_height_ft")
STAGE_KEYS = {"slug", "decision", "planting_layout", "retired_anchor", "edits", "restatements"}


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def certified(c):
    return (c.get("verification_status") or {}).get("status") == CERTIFIED


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
        for k in ("decision", "planting_layout"):
            if k not in s:
                refuse(f"stage {slug}: missing {k!r}")
        if not (isinstance(s["decision"], str) and s["decision"].strip()):
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


# ---------------------------------------------------------------- evidence (guard 2)
def check_evidence(post_idx, stage, ev, catalog, evidence_dir):
    man = manifest(evidence_dir)
    covered = set()
    text_cache = {}
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']} {r['field']})"
        c = post_idx.get(r["crop"])
        e = next((x for x in (c or {}).get("planting_layout") or [] if x.get("id") == r["entry_id"]), None)
        if e is None:
            refuse(f"{tag}: no such crop/entry in the post-state")
        if r["field"] not in NUMERIC_FIELDS or r["field"] not in e or e[r["field"]] is None:
            refuse(f"{tag}: the entry carries no {r['field']}")
        if compact(e[r["field"]]) != r["value"]:
            refuse(f"{tag}: value {r['value']} != the entry's {compact(e[r['field']])}")
        if r["source_id"] not in (e.get("sources") or []):
            refuse(f"{tag}: source {r['source_id']!r} is not in the entry's sources")
        if (e.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:
            refuse(f"{tag}: url is not the entry's anchoring url for {r['source_id']!r}")
        q = cached_quote(r, man, evidence_dir, text_cache, tag)
        if not quote_states(r["field"], json.loads(r["value"]), r["quote"]):
            refuse(f"{tag}: the quote states neither endpoint of {r['value']} (inches or feet)")
        covered.add((r["crop"], r["entry_id"], r["field"]))
    for slug in stage:
        c = post_idx[slug]
        for e in c["planting_layout"]:
            for s in e.get("sources") or []:
                if s not in catalog:
                    refuse(f"{slug} {e['id']}: source {s!r} is not in source_catalog")
            if migrated(slug, e):
                continue
            for f in NUMERIC_FIELDS:
                if e.get(f) is not None and (slug, e["id"], f) not in covered:
                    refuse(f"{slug} {e['id']}: {f} {compact(e[f])} has no EVIDENCE row")
    return len(covered)


def migrated(slug, e):
    return PLG.migration_waived(slug, e)


# ---------------------------------------------------------------- the transform
def apply_to(pre, stage):
    post = copy.deepcopy(pre)
    for c in post["crops"]:
        if not certified(c):
            continue
        if c.get("zone_independent") is True:
            c.update(planting_layout=[], spacing_inches=None, row_spacing_inches=None,
                     row_spacing_reason="not_applicable")
            continue
        s = stage[c["slug"]]
        entries = copy.deepcopy(s["planting_layout"])
        c["planting_layout"] = entries
        c["spacing_inches"] = PLG.expected_spacing(entries)
        d = PLG.default_entry(entries)
        c["row_spacing_inches"] = d.get("row_spacing_inches") if d else None
        c["row_spacing_reason"] = PLG.expected_row_reason(c)
        c.pop(RETIRED, None)
        for ed in s.get("edits") or []:
            set_at(c, resolve(c, ed["path"]), ed["new"])
    return post


# ---------------------------------------------------------------- checks
def check_pre(pre, stage):
    crops = pre["crops"]
    cert = [c for c in crops if certified(c)]
    if len(cert) != EXPECTED_CERTIFIED:
        refuse(f"base has {len(cert)} certified crops, expected {EXPECTED_CERTIFIED}")
    zi = sorted(c["slug"] for c in cert if c.get("zone_independent") is True)
    if tuple(zi) != NULL_SPACING_EXPECTED:
        refuse(f"zone_independent set {zi} != the literal {list(NULL_SPACING_EXPECTED)}")
    want = {c["slug"] for c in cert} - set(zi)
    got = set(stage)
    if got != want:
        refuse(f"FIXED LIST: staged crops != certified non-zone_independent crops; missing "
               f"{sorted(want - got)}, extra {sorted(got - want)}")
    if len(got) != EXPECTED_STAGED:
        refuse(f"staged {len(got)} crops, expected {EXPECTED_STAGED}")
    idx = by_slug(pre)
    anch = sorted(c["slug"] for c in cert if RETIRED in c)
    if tuple(anch) != RETIRED_ANCHOR_CROPS:
        refuse(f"base crops carrying {RETIRED} {anch} != the literal {list(RETIRED_ANCHOR_CROPS)}")
    for c in crops:
        for k in ("row_spacing_inches", "row_spacing_reason"):
            if k in c:
                refuse(f"base already carries {k} on {c['slug']}")
        if isinstance(c.get("planting_layout"), list):
            refuse(f"base already carries a list planting_layout on {c['slug']}")
    for slug, s in stage.items():
        c = idx[slug]
        if (RETIRED in c) != ("retired_anchor" in s):
            refuse(f"{slug}: retired_anchor is required iff the crop carries {RETIRED}")
        for ed in s.get("edits") or []:
            if set(ed) != {"path", "new", "reason"} or not str(ed["reason"]).strip():
                refuse(f"{slug}: an edit needs exactly path, new and a reason: {ed}")
            head = parse_path(ed["path"])[0]
            if head in LAYOUT_KEYS + (RETIRED, "rootstock_options", "verification_status"):
                refuse(f"{slug}: edit {ed['path']!r} touches a key the promote owns or a record")
            resolve(c, ed["path"])
        w = MIG.WAIVERS.get(slug)
        if w is not None:
            if slug not in MIG.ELIGIBLE:
                refuse(f"{slug}: a migration waiver off the R5 list")
            if compact(w["in_row_inches"]) != compact(c.get("spacing_inches")):
                refuse(f"{slug}: migration waiver in_row {compact(w['in_row_inches'])} != the base "
                       f"spacing_inches {compact(c.get('spacing_inches'))}")
    return len(got)


def check_post(pre, post, stage, ev, evidence_dir):
    # guard 5, sets first
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
        allowed = {(k,) for k in LAYOUT_KEYS} | {(RETIRED,)}
        s = stage.get(slug, {})
        for ed in s.get("edits") or []:
            allowed.add(tuple(resolve(a, ed["path"])))
        changed = leaf_diff(a, b)
        stray = sorted(fmt(list(p)) for p in changed
                       if not any(p[:len(al)] == al for al in allowed))
        if stray:
            refuse(f"{slug}: changed outside what the stage names: {stray[:6]}")
        if slug in stage:
            if compact(b["planting_layout"]) != compact(s["planting_layout"]):
                refuse(f"{slug}: planting_layout is not the stage's, verbatim")
            for ed in s.get("edits") or []:
                node = b
                for seg in resolve(a, ed["path"]):
                    node = node[seg]
                if compact(node) != compact(ed["new"]):
                    refuse(f"{slug}: {ed['path']} is not the edit's new value")
    # guard 1
    nulls = tuple(sorted(c["slug"] for c in post["crops"] if certified(c) and c.get("spacing_inches") is None))
    if nulls != NULL_SPACING_EXPECTED:
        refuse(f"FIXED LIST: null spacing on {list(nulls)}, expected exactly {list(NULL_SPACING_EXPECTED)}")
    # guard 3
    for slug in RETIRED_ANCHOR_CROPS:
        disp = stage[slug]["retired_anchor"]
        old = pidx[slug][RETIRED]
        if set(disp) != set(old):
            refuse(f"{slug}: retired_anchor names {sorted(disp)}, the base anchors {sorted(old)}")
        for sid, how in disp.items():
            if how == "moved":
                if not any((e.get("anchoring_urls") or {}).get(sid, {}).get("url") == old[sid]["url"]
                           for e in qidx[slug]["planting_layout"]):
                    refuse(f"{slug}: {sid} marked moved, but no entry anchors {old[sid]['url']}")
            elif not (isinstance(how, dict) and set(how) == {"dropped"} and str(how["dropped"]).strip()):
                refuse(f"{slug}: {sid} disposition must be 'moved' or {{'dropped': '<reason>'}}")
    # guard 4
    for slug, s in stage.items():
        a, b = pidx[slug], qidx[slug]
        if compact(a.get("spacing_inches")) == compact(b.get("spacing_inches")):
            continue
        adj = {}
        for r in s.get("restatements") or []:
            if set(r) != {"path", "verdict", "note"} or r["verdict"] not in ("agrees", "edited") \
                    or not str(r["note"]).strip():
                refuse(f"{slug}: a restatement needs path, verdict agrees|edited, and a note: {r}")
            adj[fmt(resolve(a, r["path"]))] = r["verdict"]
        edited = {fmt(resolve(a, ed["path"])) for ed in s.get("edits") or []}
        for p in spacing_strings(a, wide=False):  # landed: the narrow scanner (B3)
            if p not in adj:
                refuse(f"{slug}: spacing_inches moves {compact(a.get('spacing_inches'))} -> "
                       f"{compact(b.get('spacing_inches'))} and the restatement at {p} is not adjudicated")
            if adj[p] == "edited" and p not in edited:
                refuse(f"{slug}: {p} is adjudicated 'edited' but no edit touches it")
    # guard 2
    n_ev = check_evidence(qidx, stage, ev, post.get("source_catalog") or {}, evidence_dir)
    # guard 6. rootstock_armed=False, explicitly (2026-10-02, promote 2's data commit): the rootstock override
    # key is promote 2's (T2), armed with apple's overrides; this promote's post (cf1d480d) predates it and
    # carries none, so the module default would redden this promote's own historical moment.
    r = PLG.roster(post, armed=True, rootstock_armed=False)
    if r["violations"]:
        refuse(f"planting_layout_gate (armed): {r['violations'][:5]}")
    why = PLG.refusal(r, armed=True, rootstock_armed=False)
    if why:
        refuse(f"planting_layout_gate (armed) REFUSED: {why}")
    import sourced_block_ratchet_gate as SBR
    import bare_host_gate as BH
    import numeric_sanity_gate as NS
    import display_readiness_gate as DR
    # mature_dimensions_armed=False, explicitly (2026-10-03, promote 3's data commit): A62's mature_dimensions
    # block is promote 3's (T5), armed with the siblings it writes; this promote's post (cf1d480d) predates
    # it and its heights carry no sibling, so the module default would redden this promote's own moment.
    v = SBR.roster(post, mature_dimensions_armed=False, known=SBR.KNOWN_AT_ARMING)[3]
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
    return r, n_ev


def run(pre, stage, ev, evidence_dir):
    n = check_pre(pre, stage)
    post = apply_to(pre, stage)
    r, n_ev = check_post(pre, post, stage, ev, evidence_dir)
    return post, n, r, n_ev


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
        post, n, r, n_ev = run(pre, stage, ev, args.evidence)
    except Refused as e:
        print(f"REFUSED: {e}")
        return 1
    print(f"  fixed list        {n} staged crops == certified non-zone_independent; null spacing == the "
          f"{len(NULL_SPACING_EXPECTED)} microgreens")
    print(f"  evidence          {n_ev} (entry, field) figures quoted from hashed bytes")
    print(f"  A44 armed         {PLG.summary(r, armed=True)}")
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
