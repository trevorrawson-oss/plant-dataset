#!/usr/bin/env python3
"""build_stage -- PLA-10 promote 3 session 2: write crops/<slug>.json + EVIDENCE.tsv from rows.py (the ruled
worklist as data) and restatements.py (the adjudications). Every quote is checked byte-present in its hashed page
and read by T4 before it is written; the promote's --check is the gate, this only refuses early.
Usage: python3 tools/staging/pla10_promote3/build_stage.py [--dump-restatements]"""
import csv, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, HERE)
import promote_pla10_promote3 as P  # noqa: E402
from pla10_promote_common import EVIDENCE_COLS, compact, norm_text, pdf_text, quote_states_ft, ft_endpoints_stated  # noqa
import rows  # noqa: E402
import sidmap  # noqa: E402

TODAY = "2026-10-02"
EV_DIR = os.path.join(REPO, "tools", ".evidence_cache")
# where the crop anchors one URL to two ids, or to none: the choice, stated
SID = {("broad-beans-fava", rows.NC + "vicia-faba/"): "ncsu_ext_toolbox_vicia_faba",
       ("chamomile", "https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/chamomile"): "ucanr_santa_clara_mg"}

# Scope the rulings require RECORDED (session-3 review: the stage `decision` never reaches canonical, so a scope
# kept only there is lost at the promote). Appended to the field_addition note, the record that does land.
TOM_SPAN = ("habit-spanning: Cornell's one range covers determinate and indeterminate tomatoes (worklist 59 section 3 "
            "row 2)")
SCOPE = {
 "habanero": "the page's figure is a general pepper statement; it names habanero (C. chinense) in its variety lists (H2)",
 "cherry-tomato": TOM_SPAN, "beefsteak-tomato": TOM_SPAN, "grape-tomato": TOM_SPAN, "heirloom-tomato": TOM_SPAN,
 "roma-tomato": "determinate: OSU's figure is stated for determinate cultivars, and the crop is determinate",
 "mint": "the page is spearmint (Mentha spicata); the crop is genus-level garden mint and names spearmint the everyday mint",
 "viola": "the page is pansy (Viola x wittrockiana); the crop also covers V. cornuta and V. tricolor",
 "marigold": "cultivar-spanning (dwarf to giant), the genus page for the crop's erecta + patula scope",
 "sunflower": "cultivar-spanning (dwarf to giant)",
 "cosmos": "garden cosmos (C. bipinnatus); the same page states orange cosmos (C. sulphureus) usually 1-3 feet",
 "basil": "the page's range is 'depending on variety', across the basils the crop covers",
}

man = {}
for r in csv.DictReader(open(os.path.join(EV_DIR, "MANIFEST.tsv"), encoding="utf-8"), delimiter="\t"):
    man.setdefault(r["url"], []).append(r)


def page(url):
    r = man[url][-1]
    f = glob.glob(os.path.join(EV_DIR, r["sha256"] + ".*"))
    assert len(f) == 1, url
    raw = open(f[0], "rb").read()
    t = norm_text(pdf_text(raw)) if f[0].endswith(".pdf") else norm_text(raw.decode("utf-8", "replace"))
    return r, t


def sid_for(data, slug, url):
    if (slug, url) in SID:
        return SID[(slug, url)]
    own, glob_, cat = sidmap.candidates(data, slug, url)
    for cand in (own, glob_):
        if len(cand) == 1:
            return cand[0]
    raise SystemExit(f"{slug}: no single source id for {url}: own={own} glob={glob_} cat={cat}")


def fmtv(v):
    return "not authored (null)" if v is None else f"[{', '.join(f'{x:g}' for x in v)}] ft"


def main():
    data = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
    idx = {c["slug"]: c for c in data["crops"]}
    try:
        import restatements as RS
        RESTATE, EDITS = RS.RESTATE, RS.EDITS
    except ImportError:
        RS, RESTATE, EDITS = None, {}, {}
    out = os.path.join(HERE, "crops")
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "*.json")):
        os.remove(f)
    ev_rows, dump = [], "--dump-restatements" in sys.argv
    spec = {}
    for slug, (h, s, ev, dec) in rows.ROWS.items():
        spec[slug] = ("new", h, s, [(f, rows.CORNELL_TOM if q == "{CORNELL}" else u,
                                     None if q == "{CORNELL}" else q) for f, u, q in ev], dec)
    for slug, ev in rows.BACKFILL.items():
        c = idx[slug]
        spec[slug] = ("backfill", c[P.H], c[P.S], [(f, u, q) for f, u, q in ev], None)
    assert set(spec) == set(P.NEW_CROPS) | set(P.BACKFILL_CROPS), set(spec) ^ (set(P.NEW_CROPS) | set(P.BACKFILL_CROPS))
    cornell_q = ("height: 2 to 6 feet staked and pruned plants can grow to well over 6 feet tall in favorable growing "
                 "seasons. spread: 2 to 6 feet")
    for slug in P.NEW_CROPS + P.BACKFILL_CROPS:
        kind, h, s, ev, dec = spec[slug]
        st = {"slug": slug}
        sources, anchors, notes = [], {}, []
        for fields, url, q in ev:
            q = q or cornell_q
            r, text = page(url)
            if q not in text:
                raise SystemExit(f"{slug}: quote not in {url} ({r['sha256'][:8]}): {q!r}")
            # a backfill cites the record's own source id (K3), or its ruled re-point (K1)
            sid = (P.REPOINT.get(slug, (P._records(idx[slug])[0]["sources"][0],))[0] if kind == "backfill"
                   else sid_for(data, slug, url))
            if sid not in sources:
                sources.append(sid)
                anchors[sid] = {"url": url, "verified": r["fetched"]}
            elif anchors[sid]["url"] != url:
                raise SystemExit(f"{slug}: {sid} anchored to two URLs")
            for fl, field, val in (("H", P.H, h), ("S", P.S, s)):
                if fl not in fields:
                    continue
                if val is None:
                    raise SystemExit(f"{slug}: a quote carries {field} but the value is null")
                if not quote_states_ft(field, val, q):
                    raise SystemExit(f"{slug}: T4 reads no endpoint of {val} as {field} in {q!r}")
                ev_rows.append({"crop": slug, "entry_id": P.ENTRY_ID, "field": field, "value": compact(val),
                                "source_id": sid, "url": url, "sha256": r["sha256"], "quote": q})
            notes.append(f"{data['source_catalog'][sid].get('name')}, {url} (raw read {r['fetched']}, {r['bytes']} "
                         f"bytes, sha256 {r['sha256']}); verbatim: \"{q}\"")
        if kind == "backfill":
            n = rows.BACKFILL_ROW[slug]
            how = {"apple": "K1: the record names the s3.wp.wsu.edu URL (neither cited nor cached); the sibling "
                            "re-points to the cited, cached wpcdn copy of the same WSU handbook, which carries the "
                            "sentence (same sha256 as the record's read).",
                   "blueberry": "K2 branch 1: the record's own PSU page fetched and states the [5,8] figure; kept "
                                "and re-hashed, no re-anchor, no PLA-465 value correction. 'or even larger' is an "
                                "open tail on a closed range: recorded."}.get(
                slug, "K3: the sibling anchors the record's own URL, re-hashed this promote; the record keeps its "
                      "historical sha.")
            st["decision"] = (f"Worklist 59 row {n} (CLOSED, backfill): values kept byte-identical "
                              f"({fmtv(h)} / {fmtv(s)}). {how} " + " | ".join(notes))
        else:
            st["decision"] = dec
        st[P.H], st[P.S] = h, s
        if h is not None or s is not None:
            st["sources"], st["anchoring_urls"] = sources, anchors
            if kind == "new":
                st["field_addition"] = {
                    "field": "plant_dimensions", "date": TODAY, "sources": list(sources),
                    "note": (f"PLA-10 promote 3 plant dimensions: mature_height_ft {fmtv(h)}, mature_spread_ft "
                             f"{fmtv(s)}; decision: docs/kickoffs/59-pla10-promote3-worklist.md. "
                             + " | ".join(notes) + (f". Scope: {SCOPE[slug]}" if slug in SCOPE else "")
                             + ". amend-not-recert.")}
        hits = P.height_strings(idx[slug], s is not None) if P._moves(slug, st, idx[slug]) else []
        if dump and hits:
            print(f"=== {slug} H={h} S={s}")
            for p in hits:
                node = idx[slug]
                for seg in P.resolve(idx[slug], p):
                    node = node[seg]
                print(f"  {p}\n      {node}")
        adj = RESTATE.get(slug, {})
        missing = [p for p in hits if p not in adj]
        if missing and not dump:
            raise SystemExit(f"{slug}: unadjudicated restatements {missing}")
        if adj:
            if not P._moves(slug, st, idx[slug]):
                raise SystemExit(f"{slug}: restatements adjudicated but no value moves")
            # scanner hits first (in the scanner's order), then the sweep's scanner-invisible leaves
            order = [p for p in hits if p in adj] + sorted(p for p in adj if p not in hits)
            st["restatements"] = [{"path": p, "verdict": adj[p][0], "note": adj[p][1]} for p in order]
        if EDITS.get(slug):
            st["edits"] = []
            for p, (old, new, why) in EDITS[slug].items():
                if adj.get(p, ("",))[0] != "edited":
                    raise SystemExit(f"{slug}: edit at {p} is not adjudicated 'edited'")
                node = idx[slug]
                for seg in P.resolve(idx[slug], p):
                    node = node[seg]
                if not isinstance(node, str) or node.count(old) != 1:
                    raise SystemExit(f"{slug}: {p}: {old!r} occurs {node.count(old) if isinstance(node, str) else 'n/a'} times")
                st["edits"].append({"path": p, "new": node.replace(old, new), "reason": why})
        for p, (v, _) in adj.items():
            if v == "edited" and p not in (EDITS.get(slug) or {}):
                raise SystemExit(f"{slug}: {p} adjudicated 'edited' with no edit")
        with open(os.path.join(out, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=1)
            f.write("\n")
    # restatement-support rows (Trevor's ceiling rule): each quote byte-present in a hashed page cited on the crop
    sup_rows = []
    for slug, paths in getattr(RS, "SUPPORT", {}).items():
        post_stage = json.load(open(os.path.join(out, slug + ".json"), encoding="utf-8"))
        adj = {r["path"]: r["verdict"] for r in post_stage.get("restatements") or []}
        crop_json = json.dumps(idx[slug], ensure_ascii=False)
        for path, (figure, quotes) in paths.items():
            if adj.get(path) != "agrees":
                raise SystemExit(f"{slug}: support for {path}, which is not adjudicated 'agrees'")
            node = idx[slug]
            for seg in P.resolve(idx[slug], path):
                node = node[seg]
            if figure not in node:
                raise SystemExit(f"{slug}: {path} does not carry the figure {figure!r}")
            for url, q in quotes:
                key = next((u for u in man if u.rstrip("/") == url.rstrip("/")), None)
                if key is None:
                    raise SystemExit(f"{slug}: {url} is not hashed")
                if key.rstrip("/") not in crop_json and key not in crop_json:
                    raise SystemExit(f"{slug}: {url} is not cited on the crop")
                r, text = page(key)
                if q not in text:
                    raise SystemExit(f"{slug}: support quote not in {key} ({r['sha256'][:8]}): {q!r}")
                sup_rows.append({"crop": slug, "entry_id": "restatement-support", "field": path, "value": figure,
                                 "source_id": sid_for(data, slug, key), "url": key, "sha256": r["sha256"], "quote": q})
    with open(os.path.join(HERE, "EVIDENCE_RESTATEMENT_SUPPORT.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EVIDENCE_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(sup_rows)
    print(f"wrote {len(sup_rows)} restatement-support rows", file=sys.stderr)
    with open(os.path.join(HERE, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EVIDENCE_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(ev_rows)
    print(f"wrote {len(spec)} stage files, {len(ev_rows)} evidence rows", file=sys.stderr)


if __name__ == "__main__":
    main()
