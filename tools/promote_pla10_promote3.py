#!/usr/bin/env python3
"""promote_pla10_promote3 -- PLA-10 PROMOTE 3: crop-level heights on the 46 crops plan 58 §3.1/§3.2 names, and the
mature_dimensions sibling backfill on PLA-465's 16 (§3.3). Spec docs/specs/pla10-field-shape.md §4; plan
docs/kickoffs/58-pla10-promote2-plan.md §3, §4, §8 (T3-T5); rulings H1-H4, K1-K4 (all TAKEN). Base 31b766e8
(promote 2, 7177af3). Built 2026-10-02 in promote 3's session-1 tools commit, BEFORE any stage exists.
Nothing here authors a value. Promotes do not import promotes; shared reading comes from cited_promote_common.

WHAT IT WRITES, and nothing wider:
  (V) mature_height_ft / mature_spread_ft ([lo, hi] feet, at most 4 decimals, or null) on a NEW crop, as staged.
      A BACKFILL crop's values stay byte-identical, except blueberry's ruled K2 re-anchor (height -> [4, 8]).
  (C) the crop-root sibling pair mature_dimensions_sources + mature_dimensions_anchoring_urls (spec §4.3), on
      every crop that carries a height or spread after the promote, inserted after mature_spread_ft.
  (T3) A THIRD RECORD ALLOWANCE: ONE verification_status.field_additions[] entry with field "plant_dimensions",
      APPENDED, on each NEW crop that authors a value (A59 requires it). Same discipline as promote 2's (F):
      append-only, a named field, nothing else under verification_status writable. A backfill crop already
      carries its PLA-465 record and keeps it byte-identical (K3: the record keeps its historical sha; the
      sibling cites the re-hashed page).
  (S) prose restatements of a moved height, adjudicated (H3: dill's uncited "3 to 5 feet"); an `edited`
      verdict's edit is the only other write.

INPUT (the stage, default tools/staging/pla10_promote3/):
  crops/<slug>.json, one per crop on the FIXED LIST (NEW_CROPS + BACKFILL_CROPS = 62), refused otherwise:
    {"slug": ..., "decision": "<the decision row: page, quoted figure, class, why>",
     "mature_height_ft": [lo, hi] | null, "mature_spread_ft": [lo, hi] | null,       # both keys, always
     "sources": [<catalog id>, ...], "anchoring_urls": {<id>: {"url": ..., "verified": <date>}},  # iff a value
     "field_addition": {"field": "plant_dimensions", "date": ..., "sources": [...], "note": ...},  # NEW + value
     "restatements": [{"path": ..., "verdict": "agrees" | "edited", "note": "..."}],  # iff a value moves
     "edits": [{"path": ..., "new": <value>, "reason": "..."}]}                      # only an `edited` one
  A NEW crop may stage both values null (a decision row turned it CONDITIONAL): it then writes nothing.
  EVIDENCE.tsv: promote 1's columns; entry_id "mature_dimensions", field mature_height_ft | mature_spread_ft.

WHY EACH GUARD EXISTS.
 X. THE FIXED LIST. The staged set equals NEW_CROPS + BACKFILL_CROPS (literals typed from plan 58, never
    computed from the walk they bound); a missing or extra crop refuses, so a partial stage cannot land.
 V. VALUES. Both keys present; each null or [lo, hi] with 0 < lo <= hi and at most 4 decimals (H4: the quotient
    to 4 places, never a looser rounding the quote check cannot match). A NEW crop is null on the base; a
    BACKFILL crop's values equal the base's unless its K2 branch is taken (blueberry: height exactly [4, 8],
    spread the base's or null).
 C. THE SIBLING. A value needs sources (unique catalog ids) and anchoring_urls whose keys are exactly those
    sources, each exactly {url, verified}, url a DOCUMENT (A63's is_bare, imported), verified a date. A crop
    with no value stages no sibling. BACKFILL: the record's own source is cited, and its anchor is the RECORD'S
    URL (K3) unless re-pointed: apple to the cited wpcdn handbook (K1), blueberry to the cited PSU page when
    K2 is taken.
 R. THE RECORD (T3). A NEW crop with a value stages exactly one field_addition, exactly {field, date, sources,
    note}, field "plant_dimensions", sources a non-empty subset of the sibling's; the base carries none (a
    second record refuses). A BACKFILL crop staging one refuses (it already has its record), and so does a
    crop with no value (a record on a crop with no height authored). Post: field_additions == base + [record].
 E. EVERY VALUE IS CITED TO BYTES. Each EVIDENCE row: value == the post's, a source the sibling cites, the
    sibling's anchor url, (sha, url) in MANIFEST.tsv, bytes that hash to their name and contain the quote,
    and quote_states_ft (T4: the field's own dimension, TOL_FT). Every non-null value has rows, and across
    them BOTH endpoints are stated: a one-ended quote cannot carry a range alone.
 S. A MOVED VALUE'S RESTATEMENTS ARE ADJUDICATED (promote 1's pattern; H3). Every prose leaf with a distance
    and a height word (and a width word when a spread is authored) is listed, agrees or edited; restatements
    on a crop whose values do not move refuse; an edit is legal only at an `edited` restatement and never
    touches a key this promote owns or a record.
 B. BLAST RADIUS, SET BEFORE VALUE. Roster order and the top-level key set first, every non-crop value and
    every shell byte-identical; per certified crop the changed leaf paths (two-sided) are a subset of what
    the stage names.
 G. THE GATES RUN ON THE POST-STATE, ARMED: A59 (shape, presence, coverage, and the T5 sibling rule), A62 with
    the mature_dimensions sibling armed, A63 bare-host, numeric_sanity, display_readiness.
 A STAGE THAT NAMES NO CROP REFUSES: an empty stage would "pass" having inspected nothing.

Usage:
  promote_pla10_promote3.py --check [--stage DIR] [--evidence DIR]
  promote_pla10_promote3.py --out /path/scratch.json
  promote_pla10_promote3.py --expect-sha <sha>          # writes canonical, on approval only
"""
import argparse, copy, csv, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from bare_host_gate import is_bare  # noqa: E402  -- A63's predicate, imported, never retyped
from cited_promote_common import (EVIDENCE_COLS, Refused, Stage, cached_quote, check_restatement_support,  # noqa: E402
                                  compact, fmt, height_strings, load_support,
                                  ft_endpoints_stated, leaf_diff, manifest, norm_text, parse_path, pdf_text,
                                  quote_states_ft, refuse, resolve, serialize, set_at, sha256_bytes)

CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla10_promote3")
EVIDENCE = os.path.join(HERE, ".evidence_cache")
BASE_SHA = "31b766e86a01377c88898568171bcb372d3da1d3146fa50f6cbd6288dd8b6369"  # promote 2, 7177af3
CERTIFIED = "verified_gs_arc"
H, S = "mature_height_ft", "mature_spread_ft"
SIB_S, SIB_A = "mature_dimensions_sources", "mature_dimensions_anchoring_urls"
RECORD_FIELD = "plant_dimensions"
ENTRY_ID = "mature_dimensions"

# THE FIXED LIST, typed from plan 58 (literals; the suite pins them against the base, never derives them).
# §3.1: the 11 tip-over crops. §3.2: the 35 closed statements (7 habit-spanning among them, ruled per row).
TIPOVER = ("bell-pepper", "jalapeno", "banana-pepper", "cayenne-pepper", "habanero", "broccoli", "brussels-sprouts",
           "broad-beans-fava", "dill", "eggplant", "cosmos")
CLOSED = ("cherry-tomato", "beefsteak-tomato", "roma-tomato", "grape-tomato", "heirloom-tomato", "tomatillo", "kale",
          "spinach", "green-beans-bush", "edamame", "potato", "sweet-potato", "onion", "okra", "celery", "artichoke",
          "asparagus", "leek", "basil", "cilantro-coriander", "chives", "mint", "lemongrass", "marigold",
          "nasturtium", "sunflower", "borage", "calendula", "zinnia", "chamomile", "sweet-alyssum", "echinacea",
          "bee-balm", "viola", "sweet-pea")
NEW_CROPS = TIPOVER + CLOSED
# §3.3: PLA-465's 16, each carrying one plant_dimensions record (2026-09-16).
BACKFILL_CROPS = ("peach", "nectarine", "apple", "lemon", "blueberry", "thyme", "rosemary", "oregano", "sage", "fig",
                  "pomegranate", "elderberry", "persimmon", "mulberry", "pawpaw", "lavender")
# K1 (TAKEN): apple's record names an s3.wp.wsu.edu URL that is neither cited nor cached; the same WSU handbook
# is cited and cached at the wpcdn URL, which carries the sentence. The sibling cites that one.
REPOINT = {"apple": ("wsu_ext", "https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2109/2019/12/"
                                "fruit_handbook_western_wa.pdf")}
# K2 (RULED): fetch blueberry's record page first; if it states [5, 8], keep and re-hash; otherwise re-anchor to
# the cited PSU page's "usually 4 to 8 feet tall" as a PLA-465 value correction. The branch is the stage's.
K2 = {"blueberry": {"height": [4, 8], "source": "psu_ext",
                    "url": "https://extension.psu.edu/highbush-blueberry-production"}}

OWNED_HEADS = (H, S, SIB_S, SIB_A, "footprint_inches", "verification_status")
STAGE_KEYS = {"slug", "decision", H, S, "sources", "anchoring_urls", "field_addition", "restatements", "edits"}
RECORD_KEYS = {"field", "date", "sources", "note"}
ANCHOR_KEYS = {"url", "verified"}


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


def _date(s):
    try:
        datetime.date.fromisoformat(s)
        return True
    except (TypeError, ValueError):
        return False


def _records(crop):
    fa = (crop.get("verification_status") or {}).get("field_additions") or []
    return [x for x in fa if isinstance(x, dict) and x.get("field") == RECORD_FIELD]


def record_url(crop):
    """The URL the crop's one PLA-465 plant_dimensions record names (its note), for the K3 anchor check."""
    m = re.search(r"https?://[^\s,;)]+", _records(crop)[0].get("note") or "")
    return m.group() if m else None


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
    return Stage(crops, load_support(stage_dir)), ev


def _pair(v):
    return (isinstance(v, list) and len(v) == 2
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v) and 0 < v[0] <= v[1])


def _authors(s):
    return s.get(H) is not None or s.get(S) is not None


def _k2_taken(slug, s, base):
    return slug in K2 and compact(s.get(H)) != compact(base.get(H))


def _moves(slug, s, base):
    return compact(s.get(H)) != compact(base.get(H)) or compact(s.get(S)) != compact(base.get(S))


# ---------------------------------------------------------------- the transform
def _insert_after(crop, after, key, value):
    if key in crop:
        crop[key] = value
        return
    items = list(crop.items())
    i = next((j for j, (k, _) in enumerate(items) if k == after), len(items) - 1)
    crop.clear()
    crop.update(items[:i + 1] + [(key, value)] + items[i + 1:])


def apply_to(pre, stage):
    post = copy.deepcopy(pre)
    idx = by_slug(post)
    for slug, s in stage.items():
        c = idx[slug]
        c[H] = copy.deepcopy(s.get(H))
        c[S] = copy.deepcopy(s.get(S))
        if _authors(s):
            _insert_after(c, S, SIB_S, list(s["sources"]))
            _insert_after(c, SIB_S, SIB_A, copy.deepcopy(s["anchoring_urls"]))
        if s.get("field_addition") is not None:
            c["verification_status"].setdefault("field_additions", []).append(copy.deepcopy(s["field_addition"]))
        for ed in s.get("edits") or []:
            set_at(c, resolve(c, ed["path"]), ed["new"])
    return post


# ---------------------------------------------------------------- checks
def check_pre(pre, stage):
    if not stage:
        refuse("the stage names no crop: nothing would be inspected")
    want = set(NEW_CROPS) | set(BACKFILL_CROPS)
    if set(stage) != want:
        refuse(f"FIXED LIST: staged crops != the 62 plan 58 names; missing {sorted(want - set(stage))}, "
               f"extra {sorted(set(stage) - want)}")
    idx = by_slug(pre)
    catalog = pre.get("source_catalog") or {}
    for c in pre["crops"]:
        for k in (SIB_S, SIB_A):
            if k in c:
                refuse(f"base already carries {k} on {c['slug']}")
    n = {"crops": 0, "authored": 0, "null": 0, "backfilled": 0, "records": 0, "k2": 0, "restatements": 0}
    for slug, s in stage.items():
        c = idx.get(slug)
        if c is None or not certified(c):
            refuse(f"{slug}: not a certified crop")
        n["crops"] += 1
        for f in (H, S):
            if f not in s:
                refuse(f"{slug}: the stage must state {f} (a value or null)")
            v = s[f]
            if v is not None and not _pair(v):
                refuse(f"{slug}: {f} must be null or [lo, hi] with 0 < lo <= hi: {v!r}")
            if v is not None and any(round(x, 4) != x for x in v):
                refuse(f"{slug}: {f} {v!r} carries more than 4 decimals (H4: the quotient to 4 places)")
        if slug in NEW_CROPS:
            _check_pre_new(slug, c, s, catalog, n)
        else:
            _check_pre_backfill(slug, c, s, catalog, n)
        _check_pre_restatements(slug, c, s)
    return n


def _check_sibling(slug, s, catalog):
    src, anc = s.get("sources"), s.get("anchoring_urls")
    if not (isinstance(src, list) and src and all(isinstance(x, str) and x for x in src)):
        refuse(f"{slug}: a value needs sources, a non-empty list of catalog ids: {src!r}")
    if len(set(src)) != len(src):
        refuse(f"{slug}: sources lists a source twice: {src}")
    for sid in src:
        if sid not in catalog:
            refuse(f"{slug}: source {sid!r} is not in source_catalog")
    if not isinstance(anc, dict) or set(anc) != set(src):
        refuse(f"{slug}: anchoring_urls keys must be exactly the sources {src}; got "
               f"{sorted(anc) if isinstance(anc, dict) else anc!r}")
    for sid, a in anc.items():
        if not isinstance(a, dict) or set(a) != ANCHOR_KEYS:
            refuse(f"{slug}: anchoring_urls[{sid!r}] needs exactly url and verified: {a!r}")
        if not (isinstance(a["url"], str) and a["url"].startswith(("http://", "https://"))):
            refuse(f"{slug}: anchoring_urls[{sid!r}] url is not http(s): {a['url']!r}")
        if is_bare(a["url"]):
            refuse(f"{slug}: anchoring_urls[{sid!r}] url {a['url']!r} is a bare host, not a document")
        if not _date(a["verified"]):
            refuse(f"{slug}: anchoring_urls[{sid!r}] verified {a['verified']!r} is not a date")


def _check_pre_new(slug, c, s, catalog, n):
    if c.get(H) is not None or c.get(S) is not None:
        refuse(f"{slug}: a NEW crop must be null on the base; it carries {c.get(H)} / {c.get(S)}")
    if not _authors(s):
        for k in ("sources", "anchoring_urls", "field_addition"):
            if k in s:
                refuse(f"{slug}: no value is authored, so the stage takes no {k} (a record on a crop with no "
                       f"height authored refuses)")
        n["null"] += 1
        return
    n["authored"] += 1
    _check_sibling(slug, s, catalog)
    if _records(c):
        refuse(f"{slug}: the base already carries a {RECORD_FIELD!r} record; a second record refuses")
    fa = s.get("field_addition")
    if fa is None:
        refuse(f"{slug}: an authored value needs its {RECORD_FIELD!r} field_addition record (A59)")
    if not isinstance(fa, dict) or set(fa) != RECORD_KEYS:
        refuse(f"{slug}: field_addition needs exactly {sorted(RECORD_KEYS)}: {fa!r}")
    if fa["field"] != RECORD_FIELD:
        refuse(f"{slug}: field_addition field must be {RECORD_FIELD!r}, got {fa['field']!r}")
    if not _date(fa["date"]):
        refuse(f"{slug}: field_addition date {fa['date']!r} is not a date")
    if not (isinstance(fa["sources"], list) and fa["sources"] and set(fa["sources"]) <= set(s["sources"])):
        refuse(f"{slug}: field_addition sources must be a non-empty subset of the sibling's {s['sources']}")
    if not (isinstance(fa["note"], str) and fa["note"].strip()):
        refuse(f"{slug}: field_addition note is empty")
    n["records"] += 1


def _check_pre_backfill(slug, c, s, catalog, n):
    recs = _records(c)
    if len(recs) != 1 or c.get(H) is None:
        refuse(f"{slug}: a BACKFILL crop carries an authored height and exactly one {RECORD_FIELD!r} record on "
               f"the base; got height {c.get(H)}, {len(recs)} record(s)")
    if "field_addition" in s:
        refuse(f"{slug}: a BACKFILL crop already carries its {RECORD_FIELD!r} record; a second record refuses")
    k2 = _k2_taken(slug, s, c)
    if k2:
        if compact(s[H]) != compact(K2[slug]["height"]):
            refuse(f"{slug}: K2's re-anchor moves the height to exactly {K2[slug]['height']}, not {s[H]}")
        if s[S] is not None and compact(s[S]) != compact(c.get(S)):
            refuse(f"{slug}: under K2 the spread stays the base's {c.get(S)} or goes null, not {s[S]}")
        n["k2"] += 1
    elif compact(s[H]) != compact(c.get(H)) or compact(s[S]) != compact(c.get(S)):
        refuse(f"{slug}: a BACKFILL crop's values stay the base's ({c.get(H)} / {c.get(S)}); got {s[H]} / {s[S]}")
    _check_sibling(slug, s, catalog)
    rsrc = recs[0]["sources"][0] if recs[0].get("sources") else None
    if slug in REPOINT:
        sid, url = REPOINT[slug]
    elif k2:
        sid, url = K2[slug]["source"], K2[slug]["url"]
    else:
        sid, url = rsrc, record_url(c)
    if sid not in s["sources"]:
        refuse(f"{slug}: the backfill must cite {sid!r} (the record's source, or its ruled re-point)")
    if s["anchoring_urls"][sid]["url"] != url:
        refuse(f"{slug}: the backfill anchor for {sid!r} must be {url!r} (K1/K2/K3); got "
               f"{s['anchoring_urls'][sid]['url']!r}")
    n["backfilled"] += 1


def _check_pre_restatements(slug, c, s):
    for r in s.get("restatements") or []:
        if not (isinstance(r, dict) and set(r) == {"path", "verdict", "note"}
                and r["verdict"] in ("agrees", "edited") and str(r["note"]).strip()):
            refuse(f"{slug}: a restatement needs path, verdict agrees|edited, and a note: {r}")
        resolve(c, r["path"])
    for ed in s.get("edits") or []:
        if not (isinstance(ed, dict) and set(ed) == {"path", "new", "reason"} and str(ed["reason"]).strip()):
            refuse(f"{slug}: an edit needs exactly path, new and a reason: {ed}")
        if parse_path(ed["path"])[0] in OWNED_HEADS or parse_path(ed["path"])[0].startswith("mature_dimensions"):
            refuse(f"{slug}: edit {ed['path']!r} touches a key the promote owns or a record")
        resolve(c, ed["path"])


def allowed_paths(pre_crop, s, slug):
    allowed = set()
    if _moves(slug, s, pre_crop):
        allowed |= {(H,), (S,)}
    if _authors(s):
        allowed |= {(SIB_S,), (SIB_A,)}
    if s.get("field_addition") is not None:
        allowed.add(("verification_status", "field_additions"))
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
        allowed = allowed_paths(a, stage.get(slug, {}), slug) if slug in stage else set()
        stray = sorted(fmt(list(p)) for p in leaf_diff(a, b)
                       if not any(p[:len(al)] == al for al in allowed))
        if stray:
            refuse(f"{slug}: changed outside what the stage names: {stray[:6]}")
    # guards V / C / R, values
    n = {"restatements": 0}
    for slug, s in stage.items():
        a, b = pidx[slug], qidx[slug]
        for f in (H, S):
            if f not in b or compact(b[f]) != compact(s[f]):
                refuse(f"{slug}: {f} {compact(b.get(f))} is not the stage's {compact(s[f])}")
        if _authors(s):
            if b.get(SIB_S) != s["sources"] or compact(b.get(SIB_A)) != compact(s["anchoring_urls"]):
                refuse(f"{slug}: the sibling pair is not the stage's")
        elif SIB_S in b or SIB_A in b:
            refuse(f"{slug}: a sibling on a crop with no value")
        fa_a = (a["verification_status"].get("field_additions") or [])
        fa_b = (b["verification_status"].get("field_additions") or [])
        want = fa_a + ([s["field_addition"]] if s.get("field_addition") is not None else [])
        if compact(fa_b) != compact(want):
            refuse(f"{slug}: field_additions must be the base's, byte for byte, plus exactly the staged record")
        _check_post_restatements(slug, a, b, s, n)
    # guard E
    n["evidence_rows"] = check_evidence(qidx, stage, ev, evidence_dir)
    # guard E2 (2026-10-03, PLA-655): the restatement-support rows, mechanically (meaning stays with review)
    adjudicated = {slug: {fmt(resolve(pidx[slug], r["path"])): r["verdict"] for r in s.get("restatements") or []}
                   for slug, s in stage.items()}
    n["support_rows"] = check_restatement_support(stage, qidx, adjudicated, manifest(evidence_dir), evidence_dir)
    # guard G
    import plant_dimensions_gate as PDG
    import sourced_block_ratchet_gate as SBR
    import bare_host_gate as BH
    import numeric_sanity_gate as NS
    import display_readiness_gate as DR
    v = PDG.all_violations(post, presence=True, coverage=True, sibling=True)
    if v:
        refuse(f"A59 (armed: presence, coverage, sibling) on the post-state: {v[:5]}")
    v = SBR.roster(post, mature_dimensions_armed=True)[3]
    if v:
        refuse(f"A62 (mature_dimensions armed) on the post-state: {v[:5]}")
    v = BH.roster(post)[4]
    if v:
        refuse(f"A63 on the post-state: {v[:5]}")
    for c in post["crops"]:
        if certified(c):
            v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)
            if v:
                refuse(f"{c['slug']}: numeric_sanity / display_readiness: {v[:3]}")
    return n


def _check_post_restatements(slug, a, b, s, n):
    adj = {fmt(resolve(a, r["path"])): r["verdict"] for r in s.get("restatements") or []}
    edited = {fmt(resolve(a, ed["path"])) for ed in s.get("edits") or []}
    for p in sorted(edited):
        if adj.get(p) != "edited":
            refuse(f"{slug}: edit at {p} is not at a restatement adjudicated 'edited'")
    if not _moves(slug, s, a):
        if adj:
            refuse(f"{slug}: restatements staged but no value moves")
        return
    for p in height_strings(a, s.get(S) is not None, wide=False):  # landed: the narrow scanner (B3)
        if p not in adj:
            refuse(f"{slug}: a height moves ({compact(a.get(H))} -> {compact(s.get(H))}) and the restatement "
                   f"at {p} is not adjudicated")
        if adj[p] == "edited" and p not in edited:
            refuse(f"{slug}: {p} is adjudicated 'edited' but no edit touches it")
    n["restatements"] += len(adj)
    for ed in s.get("edits") or []:
        node = b
        for seg in resolve(a, ed["path"]):
            node = node[seg]
        if compact(node) != compact(ed["new"]):
            refuse(f"{slug}: {ed['path']} is not the edit's new value")


def check_evidence(post_idx, stage, ev, evidence_dir):
    man = manifest(evidence_dir)
    seen, stated = set(), {}
    text_cache = {}
    for i, r in enumerate(ev):
        tag = f"EVIDENCE.tsv row {i + 2} ({r['crop']} {r['entry_id']} {r['field']})"
        key = (r["crop"], r["entry_id"], r["field"], r["source_id"], r["sha256"], r["quote"])
        if key in seen:
            refuse(f"{tag}: a duplicate row")
        seen.add(key)
        c = post_idx.get(r["crop"])
        if r["crop"] not in stage or c is None:
            refuse(f"{tag}: {r['crop']} is not a staged crop")
        if r["entry_id"] != ENTRY_ID or r["field"] not in (H, S):
            refuse(f"{tag}: a height row names entry {ENTRY_ID!r} and field {H} or {S}")
        if c.get(r["field"]) is None:
            refuse(f"{tag}: the crop carries no {r['field']}")
        if compact(c[r["field"]]) != r["value"]:
            refuse(f"{tag}: value {r['value']} != the crop's {compact(c[r['field']])}")
        if r["source_id"] not in (c.get(SIB_S) or []):
            refuse(f"{tag}: source {r['source_id']!r} is not in {SIB_S}")
        if (c.get(SIB_A) or {}).get(r["source_id"], {}).get("url") != r["url"]:
            refuse(f"{tag}: url is not the sibling's anchoring url for {r['source_id']!r}")
        q = cached_quote(r, man, evidence_dir, text_cache, tag)
        value = json.loads(r["value"])
        if not quote_states_ft(r["field"], value, q):
            refuse(f"{tag}: the quote states neither endpoint of {r['value']} as a {r['field']} (TOL_FT)")
        stated.setdefault((r["crop"], r["field"]), set()).update(ft_endpoints_stated(r["field"], value, q))
    for slug in stage:
        c = post_idx[slug]
        for f in (H, S):
            if c.get(f) is None:
                continue
            got = stated.get((slug, f))
            if got is None:
                refuse(f"{slug}: {f} {compact(c[f])} has no EVIDENCE row")
            if got != set(c[f]):
                refuse(f"{slug}: {f} {compact(c[f])}: the rows state only {sorted(got)}; both endpoints must be "
                       f"stated")
    return len(ev)


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
    print(f"  fixed list        {n['crops']} staged == {len(NEW_CROPS)} new + {len(BACKFILL_CROPS)} backfill")
    print(f"  heights           {n['authored']} authored, {n['null']} null by decision, {n['backfilled']} backfilled "
          f"({n['k2']} K2 re-anchor), {n['records']} plant_dimensions records appended")
    print(f"  evidence          {n['evidence_rows']} rows, both endpoints stated on every value; "
          f"{n['restatements']} restatements adjudicated")
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
