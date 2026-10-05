#!/usr/bin/env python3
"""promote_pla10_promote2 -- PLA-10 PROMOTE 2, first rows: apple's rootstock spacing overrides (R1) and the
D1a [CORRECTION ...] appends on the in-canonical *_pilot_spacing_* open findings.
Spec docs/specs/pla10-field-shape.md §5, §10.2; SESSION3_HANDOFF.md owed items 1 and 2. Base cf1d480d
(promote 1, d021116). Built 2026-10-02 in promote 2's session-1 tools commit, BEFORE any stage exists.
Nothing here authors a value. Session 2's tools commit (T1, plan docs/kickoffs/58-pla10-promote2-plan.md §8)
adds the layout-entry stage key and the default move; heights are promote 3's.

THE TWO RECORD ALLOWANCES (owed items 1 and 2), and nothing wider:
  (R) a rootstock_options[] row may gain spacing_inches ([lo, hi] or null) and, ONLY while that override is
      non-null, ONE new source appended to its `sources` plus that source's `anchoring_urls` key. Every
      other rootstock key, every existing anchor, and a null-override row's citation stay byte-identical.
  (F) an open finding under verification_status.open_findings[], named by its `id`, may have exactly one
      dated correction line APPENDED to its `summary` (docs/verification_log_ref_convention.md format).
      The base summary stays byte-for-byte as the prefix. No other verification_status key is writable:
      status, launch flags, the log ref, field_additions, other findings, and other finding keys refuse.
  (L) T1. A crop on SUPPORT_CROPS may gain planting_layout entries, APPENDED VERBATIM after the existing
      ones (`planting_layout_add`); a crop on DEFAULT_MOVE_CROPS may move its default to a named entry
      (`default`). The three crop-root mirrors are recomputed through planting_layout_gate's own
      expected_spacing / default_entry / expected_row_reason (imported, never retyped). When a mirror
      moves, every restatement promote 1's scanner finds is adjudicated, and an `edited` verdict's edit
      is the only other write. Existing entries stay byte-identical except the `default` flag a move
      flips.

INPUT (the stage, default tools/staging/pla10_promote2/):
  crops/<slug>.json:
    {"slug": ..., "decision": "<the decision row: page, quoted figure, why>",
     "rootstock_spacing": [{"name": <row name>, "spacing_inches": [lo, hi] | null,
                            "add_source": {"id": <catalog id>, "url": ..., "verified": <date>}}],  # non-null only
     "finding_corrections": [{"id": <open finding id>, "append": " [CORRECTION <date>: <what> -- see <ref>.]"}],
     "planting_layout_add": [<entries, spec §1.1, verbatim as they will land, each "default": false>],
     "default": "<entry id>",                                         # a default move, ruled crops only
     "restatements": [{"path": ..., "verdict": "agrees" | "edited", "note": "..."}],  # iff a mirror moves
     "edits": [{"path": ..., "new": <value>, "reason": "..."}]}       # only an `edited` restatement
  EVIDENCE.tsv: crop, entry_id, field, value, source_id, url, sha256, quote (promote 1's columns);
    a rootstock override's entry_id is "rootstock_options[name=<row name>]", field "spacing_inches";
    an added layout entry's entry_id is its id, field one of NUMERIC_FIELDS. One row per
    (crop, entry, field, source); a row naming an entry the stage does not add refuses.

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
    The reading is cited_promote_common's (moved there byte-identically 2026-10-03; the replays pin it).
 F. A CORRECTION APPENDS, IT NEVER REWRITES. `append` is exactly one correction line with a real date and a
    "-- see <ref>." pointer, nothing before or after it; the finding id matches exactly one finding; one
    correction per finding per stage; a summary already ending with it refuses (no double-apply). After
    the transform the summary must equal base + append, byte for byte.
 B. BLAST RADIUS, SET BEFORE VALUE. Roster order and top-level key set first, then every non-crop top-level
    value and every shell byte-identical; on each certified crop the changed LEAF paths (two-sided: added
    and removed keys count) are a subset of exactly what (R) and (F) allow for that crop. Then values: each
    override equals the stage's (a dropped null counts), sources == base + [add_source.id], the new anchor
    is the stage's.
 L. LAYOUT ENTRIES ARE APPENDED, NEVER RE-DERIVED (T1). planting_layout_add and default are ruled for the
    literal crop lists only. A staged id is new to the crop and staged once; a staged entry carries
    default false, so the stage's `default` key is the ONE route to a default (two defaults cannot be
    staged); `default` names an entry and is not already the default. After the transform: the list is
    the base's entries, byte-identical except the flipped `default` flag, followed by the staged entries
    verbatim (ids exactly as staged: the promote never computes an id from (arrangement, support)); the
    three mirrors equal planting_layout_gate's functions over the post entries. Every number on an added
    entry is cited to bytes (guard E, the entry's own source and anchor).
 S. A MOVED MIRROR'S RESTATEMENTS ARE ADJUDICATED (promote 1's guard 4, its scanner copied byte-identical).
    If spacing_inches or row_spacing_inches moves, every scanner hit on the base crop is listed in
    `restatements` (agrees with a note, or edited with its edit); restatements on a crop whose mirrors do
    not move refuse; an edit is legal only at an `edited` restatement and never touches the layout, the
    mirrors, a rootstock row or verification_status.
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
from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, compact, fmt, leaf_diff, manifest,  # noqa: E402
                                  norm_text, parse_path, pdf_text, quote_states, refuse, resolve, serialize,
                                  set_at, sha256_bytes, spacing_strings)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla10_promote2")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "cf1d480dfc926b226f63fde2fbdbc548e9d06487ed749e7431a06710431f2e49"  # promote 1, d021116
CERTIFIED = "verified_gs_arc"

# Literals (R1, ruled 2026-09-30 / 2026-10-01), never computed from the walk they bound.
ROOTSTOCK_CROPS = ("apple",)
# T1 literals (plan 58 §2, ruled 2026-10-02): the crops that may gain entries, and the crops whose default
# may move (S1: the four indeterminate tomatoes, conditional on UNL's cage rows; S5: english-cucumber).
SUPPORT_CROPS = ("acorn-squash", "beefsteak-tomato", "cantaloupe", "cherry-tomato", "cucumber", "english-cucumber",
                 "grape-tomato", "heirloom-tomato", "pickling-cucumber", "roma-tomato", "slicing-cucumber",
                 "strawberry")
DEFAULT_MOVE_CROPS = ("beefsteak-tomato", "cherry-tomato", "english-cucumber", "grape-tomato", "heirloom-tomato")
NUMERIC_FIELDS = ("in_row_inches", "hill_spacing_inches", "row_spacing_inches", "plants_per_hill",
                  "mature_height_ft")  # promote 1's, pinned equal by the suite
OWNED_HEADS = ("planting_layout",) + PLG.MIRROR_KEYS + ("rootstock_options", "verification_status")
STAGE_KEYS = {"slug", "decision", "rootstock_spacing", "finding_corrections", "planting_layout_add", "default",
              "restatements", "edits"}
ROW_KEYS = {"name", "spacing_inches", "add_source"}
ADD_SOURCE_KEYS = {"id", "url", "verified"}
CORRECTION = re.compile(r" \[CORRECTION (\d{4}-\d{2}-\d{2}): [^\[\]]+ -- see [^\[\]]+\.\]")


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
        if _layout_staged(s):
            entries = c["planting_layout"]
            entries.extend(copy.deepcopy(s.get("planting_layout_add") or []))
            if s.get("default") is not None:
                for e in entries:
                    e["default"] = e["id"] == s["default"]
            c["spacing_inches"] = PLG.expected_spacing(entries)
            d = PLG.default_entry(entries)
            c["row_spacing_inches"] = d.get("row_spacing_inches") if d else None
            c["row_spacing_reason"] = PLG.expected_row_reason(c)
        for ed in s.get("edits") or []:
            set_at(c, resolve(c, ed["path"]), ed["new"])
    return post


def _layout_staged(s):
    return "planting_layout_add" in s or "default" in s


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
    n = {"crops": 0, "overrides": 0, "nulls": 0, "sources_added": 0, "corrections": 0, "entries_added": 0,
         "default_moves": 0, "mirror_moves": 0, "restatements": 0}
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
        _check_pre_layout(slug, c, s, n)
    return n


def _check_pre_layout(slug, c, s, n):
    add, dflt = s.get("planting_layout_add"), s.get("default")
    base_ids = [e.get("id") for e in c.get("planting_layout") or [] if isinstance(e, dict)]
    staged_ids = []
    if add is not None:
        if slug not in SUPPORT_CROPS:
            refuse(f"{slug}: planting_layout_add is ruled for {list(SUPPORT_CROPS)} only (plan 58 §2)")
        if not (isinstance(c.get("planting_layout"), list) and c["planting_layout"]):
            refuse(f"{slug}: planting_layout_add on a crop with no ground layout")
        if not (isinstance(add, list) and add and all(isinstance(e, dict) for e in add)):
            refuse(f"{slug}: planting_layout_add must be a non-empty list of entry objects")
        for e in add:
            eid = e.get("id")
            if not isinstance(eid, str):
                refuse(f"{slug}: a staged entry has no string id: {e!r}")
            if eid in staged_ids:
                refuse(f"{slug}: staged entry id {eid!r} is staged twice")
            if eid in base_ids:
                refuse(f"{slug}: staged entry id {eid!r} is already on the crop")
            if e.get("default") is not False:
                refuse(f"{slug} {eid}: a staged entry must carry default false; the default moves only by "
                       f"the stage's `default` key")
            staged_ids.append(eid)
            n["entries_added"] += 1
    if dflt is not None:
        if slug not in DEFAULT_MOVE_CROPS:
            refuse(f"{slug}: a default move is ruled for {list(DEFAULT_MOVE_CROPS)} only (plan 58 S1, S5)")
        if dflt not in base_ids + staged_ids:
            refuse(f"{slug}: default {dflt!r} names no entry")
        d = PLG.default_entry(c.get("planting_layout") or [])
        if d is not None and d.get("id") == dflt:
            refuse(f"{slug}: default {dflt!r} is already the default")
        n["default_moves"] += 1
    for r in s.get("restatements") or []:
        if not (isinstance(r, dict) and set(r) == {"path", "verdict", "note"}
                and r["verdict"] in ("agrees", "edited") and str(r["note"]).strip()):
            refuse(f"{slug}: a restatement needs path, verdict agrees|edited, and a note: {r}")
        resolve(c, r["path"])
    for ed in s.get("edits") or []:
        if not (isinstance(ed, dict) and set(ed) == {"path", "new", "reason"} and str(ed["reason"]).strip()):
            refuse(f"{slug}: an edit needs exactly path, new and a reason: {ed}")
        if parse_path(ed["path"])[0] in OWNED_HEADS:
            refuse(f"{slug}: edit {ed['path']!r} touches a key the promote owns or a record")
        resolve(c, ed["path"])


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
    if _layout_staged(s):
        allowed |= {(k,) for k in ("planting_layout",) + PLG.MIRROR_KEYS}
    for ed in s.get("edits") or []:
        allowed.add(tuple(resolve(pre_crop, ed["path"])))
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
    # guards L and S
    moved = {"mirror_moves": 0, "restatements": 0}
    for slug, s in stage.items():
        a, b = pidx[slug], qidx[slug]
        if _layout_staged(s):
            _check_post_layout(slug, a, b, s)
        _check_post_restatements(slug, a, b, s, moved)
    # guard E
    check_evidence(qidx, stage, ev, post.get("source_catalog") or {}, evidence_dir)
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
    # mature_dimensions_armed=False, explicitly (2026-10-03, promote 3's data commit): A62's mature_dimensions
    # block is promote 3's (T5), armed with the siblings it writes; this promote's post (31b766e8) predates
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
    return moved


def _check_post_layout(slug, a, b, s):
    base, add, dflt = a["planting_layout"], s.get("planting_layout_add") or [], s.get("default")
    got = b.get("planting_layout")
    if not isinstance(got, list) or len(got) != len(base) + len(add):
        refuse(f"{slug}: planting_layout must be the base's {len(base)} entr(y/ies) plus the stage's {len(add)}, "
               f"appended; got {len(got) if isinstance(got, list) else got!r}")
    for i, e in enumerate(base):
        want = copy.deepcopy(e)
        if dflt is not None:
            want["default"] = e.get("id") == dflt
        if compact(got[i]) != compact(want):
            refuse(f"{slug}: existing entry planting_layout[{i}] ({e.get('id')!r}) changed; only the default "
                   f"flag a staged move flips may differ")
    for j, e in enumerate(add):
        k = len(base) + j
        want = copy.deepcopy(e)
        if dflt is not None:
            want["default"] = e["id"] == dflt
        if compact(got[k]) != compact(want):
            refuse(f"{slug}: planting_layout[{k}] is not the stage's entry {e['id']!r}, verbatim")
    d = PLG.default_entry(got)
    for k, exp in (("spacing_inches", PLG.expected_spacing(got)),
                   ("row_spacing_inches", d.get("row_spacing_inches") if d else None),
                   ("row_spacing_reason", PLG.expected_row_reason(b))):
        if k not in b or compact(b[k]) != compact(exp):
            refuse(f"{slug}: {k} {compact(b.get(k))} is not planting_layout_gate's mirror {compact(exp)}")


def _check_post_restatements(slug, a, b, s, moved):
    moves = [f"{k} {compact(a.get(k))} -> {compact(b.get(k))}" for k in ("spacing_inches", "row_spacing_inches")
             if compact(a.get(k)) != compact(b.get(k))]
    adj = {fmt(resolve(a, r["path"])): r["verdict"] for r in s.get("restatements") or []}
    edited = {fmt(resolve(a, ed["path"])) for ed in s.get("edits") or []}
    for p in sorted(edited):
        if adj.get(p) != "edited":
            refuse(f"{slug}: edit at {p} is not at a restatement adjudicated 'edited'")
    if not moves:
        if adj:
            refuse(f"{slug}: restatements staged but no mirror moves")
        return
    moved["mirror_moves"] += 1
    for p in spacing_strings(a, wide=False):  # landed: the narrow scanner (B3)
        if p not in adj:
            refuse(f"{slug}: a mirror moves ({'; '.join(moves)}) and the restatement at {p} is not adjudicated")
        if adj[p] == "edited" and p not in edited:
            refuse(f"{slug}: {p} is adjudicated 'edited' but no edit touches it")
    moved["restatements"] += len(adj)
    for ed in s.get("edits") or []:
        node = b
        for seg in resolve(a, ed["path"]):
            node = node[seg]
        if compact(node) != compact(ed["new"]):
            refuse(f"{slug}: {ed['path']} is not the edit's new value")


ROW_ID = re.compile(r"rootstock_options\[name=([^\]]+)\]")


def check_evidence(post_idx, stage, ev, catalog, evidence_dir):
    man = manifest(evidence_dir)
    covered, covered_l, seen = set(), set(), set()
    text_cache = {}
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']} {r['field']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"])
        if key in seen:
            refuse(f"{tag}: a duplicate; one EVIDENCE row per (crop, entry, field, source)")
        seen.add(key)
        c = post_idx.get(r["crop"])
        m = ROW_ID.fullmatch(r["entry_id"])
        if m:
            hits = _row_index(c, m.group(1)) if c is not None else []
            if len(hits) != 1:
                refuse(f"{tag}: no such crop/row in the post-state")
            holder, what = c["rootstock_options"][hits[0]], "row"
            if r["field"] != "spacing_inches" or holder.get("spacing_inches") is None:
                refuse(f"{tag}: the row carries no {r['field']}")
        else:
            added = [e.get("id") for e in (stage.get(r["crop"]) or {}).get("planting_layout_add") or []]
            if r["entry_id"] not in added:
                refuse(f"{tag}: {r['crop']} {r['entry_id']}: the stage does not add this entry")
            holder, what = next(e for e in c["planting_layout"] if e.get("id") == r["entry_id"]), "entry"
            if r["field"] not in NUMERIC_FIELDS or holder.get(r["field"]) is None:
                refuse(f"{tag}: the entry carries no {r['field']}")
        if compact(holder[r["field"]]) != r["value"]:
            refuse(f"{tag}: value {r['value']} != the {what}'s {compact(holder[r['field']])}")
        if r["source_id"] not in (holder.get("sources") or []):
            refuse(f"{tag}: source {r['source_id']!r} is not in the {what}'s sources")
        if (holder.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:
            refuse(f"{tag}: url is not the {what}'s anchoring url for {r['source_id']!r}")
        q = cached_quote(r, man, evidence_dir, text_cache, tag)
        if not quote_states(r["field"], json.loads(r["value"]), r["quote"]):
            refuse(f"{tag}: the quote states neither endpoint of {r['value']} (inches or feet)")
        covered.add((r["crop"], r["entry_id"]))
        covered_l.add((r["crop"], r["entry_id"], r["field"]))
    for slug, s in stage.items():
        c = post_idx[slug]
        for e in s.get("planting_layout_add") or []:
            for sid in e.get("sources") or []:
                if sid not in catalog:
                    refuse(f"{slug} {e['id']}: source {sid!r} is not in source_catalog")
            for f in NUMERIC_FIELDS:
                if e.get(f) is not None and (slug, e["id"], f) not in covered_l:
                    refuse(f"{slug} {e['id']}: {f} {compact(e[f])} has no EVIDENCE row")
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
    n.update(check_post(pre, post, stage, ev, evidence_dir))
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
    print(f"  layout            {n['entries_added']} entries added, {n['default_moves']} default moves; mirrors "
          f"moved on {n['mirror_moves']} crop(s), {n['restatements']} restatements adjudicated")
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
