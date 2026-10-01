#!/usr/bin/env python3
"""stage_lane_b -- PLA-10 promote 1 SESSION helper (lane B, judgment): build a crop's stage file and its EVIDENCE
rows from a compact spec in lane_b_specs/<slug>.json, checking every quote against the HASHED bytes in
tools/.evidence_cache (looked up by url through MANIFEST.tsv; a .pdf cache file is read through pypdf, which the
promote does not yet do: see the lane A report of 2026-10-01).  The decision row is the author's; this script only
assembles the entry shape and refuses a quote that is not in the bytes.

Spec (lane_b_specs/<slug>.json):
  {"slug": "...", "decision": "<the decision row>",
   "entries": [{"id": "row-none", "arrangement": "row", "support": "none", "default": true,
                "fields": {"in_row_inches": {"value": [lo,hi], "sid": "...", "url": "...", "quote": "..."},
                           "row_spacing_inches": {...} | null,
                           "hill_spacing_inches": {...}, "plants_per_hill": {...}},
                "sources_extra": []}],
   "retired_anchor": {...}, "rootstock_spacing": {...}, "edits": [...], "restatements": [...]}
Usage: stage_lane_b.py SLUG [SLUG ...] | --all     (rewrites crops/<slug>.json and the crop's rows in EVIDENCE.tsv)
"""
import csv, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, TOOLS)
import promote_pla10_planting_layout as P  # noqa: E402

SPECS = os.path.join(HERE, "lane_b_specs")
CROPS = P.by_slug(P.load_canonical())
VERIFIED = "2026-10-01"
_TEXT = {}


def url_to_sha():
    m = {}
    with open(os.path.join(P.EVIDENCE, "MANIFEST.tsv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            m.setdefault(r["url"], r["sha256"])  # first fetch of a url wins
    return m


def page_text(sha):
    if sha not in _TEXT:
        files = glob.glob(os.path.join(P.EVIDENCE, sha + ".*"))
        assert len(files) == 1, (sha, files)
        raw = open(files[0], "rb").read()
        assert P.sha256_bytes(raw) == sha
        if files[0].endswith(".pdf"):
            import pypdf
            txt = "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(files[0]).pages)
            _TEXT[sha] = (P.norm_text(txt), True)
        else:
            _TEXT[sha] = (P.norm_text(raw.decode("utf-8", "replace")), False)
    return _TEXT[sha]


def build(spec, u2s):
    slug = spec["slug"]
    entries, ev = [], []
    for e in spec["entries"]:
        fields = e["fields"]
        arr = e["arrangement"]
        entry = {"id": e["id"], "arrangement": arr, "support": e.get("support", "none"), "default": e["default"]}
        srcs, anch = [], {}
        ordered = ["in_row_inches", "hill_spacing_inches", "row_spacing_inches", "row_spacing_reason",
                   "plants_per_hill"]
        for f in ordered:
            if f == "row_spacing_reason":
                entry["row_spacing_reason"] = None if entry.get("row_spacing_inches") is not None else "not_authored"
                continue
            spec_f = fields.get(f)
            if f == "row_spacing_inches" and spec_f is None:
                entry["row_spacing_inches"] = None
                continue
            if spec_f is None:
                continue
            val, sid, url, q = spec_f["value"], spec_f["sid"], spec_f["url"], spec_f["quote"]
            sha = u2s.get(url)
            if sha is None:
                raise SystemExit(f"{slug} {e['id']} {f}: url not in MANIFEST.tsv: {url}")
            text, is_pdf = page_text(sha)
            nq = P.norm_text(q)
            if len(nq) < 12 or nq not in text:
                raise SystemExit(f"{slug} {e['id']} {f}: quote not in the hashed bytes{' (pdf text)' if is_pdf else ''}: {q[:90]!r}")
            if not P.quote_states(f, val, q):
                raise SystemExit(f"{slug} {e['id']} {f}: quote states neither endpoint of {val}: {q[:90]!r}")
            entry[f] = val
            if sid not in srcs:
                srcs.append(sid); anch[sid] = {"url": url, "verified": VERIFIED}
            ev.append([slug, e["id"], f, P.compact(val), sid, url, sha, q])
        for sid, url in (e.get("sources_extra") or []):
            if sid not in srcs:
                srcs.append(sid); anch[sid] = {"url": url, "verified": VERIFIED}
        if "rows_per_bed" in e:
            entry["rows_per_bed"] = e["rows_per_bed"]
        entry["sources"] = srcs
        entry["anchoring_urls"] = anch
        entries.append(entry)
    stage = {"slug": slug, "decision": spec["decision"], "planting_layout": entries}
    for k in ("retired_anchor", "rootstock_spacing"):
        if k in spec:
            stage[k] = spec[k]
    # edits: {"path", "new", "reason"} verbatim, or {"path", "replace": [old_fragment, new_fragment], "reason"}
    # resolved against the live canonical (the fragment must occur exactly once in the current string).
    crop = CROPS[slug]
    edits = []
    for ed in spec.get("edits") or []:
        if "replace" in ed:
            node = crop
            for seg in P.resolve(crop, ed["path"]):
                node = node[seg]
            old, new = ed["replace"]
            if not isinstance(node, str) or node.count(old) != 1:
                raise SystemExit(f"{slug}: edit {ed['path']}: fragment occurs {node.count(old) if isinstance(node, str) else 'n/a'} times: {old!r}")
            edits.append({"path": ed["path"], "new": node.replace(old, new), "reason": ed["reason"]})
        else:
            edits.append({"path": ed["path"], "new": ed["new"], "reason": ed["reason"]})
    if edits:
        stage["edits"] = edits
    # restatements: a list of {"path","verdict","note"}, or a dict {path: "agrees: note" | "edited: note"}
    rs = spec.get("restatements")
    if isinstance(rs, dict):
        out = []
        for path, v in rs.items():
            verdict, _, note = v.partition(":")
            out.append({"path": path, "verdict": verdict.strip(), "note": note.strip()})
        rs = out
    if rs:
        stage["restatements"] = rs
        edited_paths = {P.fmt(P.resolve(crop, e["path"])) for e in edits}
        for r in rs:
            if r["verdict"] == "edited" and P.fmt(P.resolve(crop, r["path"])) not in edited_paths:
                raise SystemExit(f"{slug}: restatement {r['path']} says edited but no edit touches it")
        listed = {P.fmt(P.resolve(crop, r["path"])) for r in rs}
        missing = [p for p in P.spacing_strings(crop) if p not in listed]
        if missing:
            raise SystemExit(f"{slug}: scanner paths not adjudicated: {missing}")
    return stage, ev


def main(argv):
    if argv and argv[0] == "--all":
        slugs = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(SPECS, "*.json")))
    else:
        slugs = argv
    u2s = url_to_sha()
    evp = os.path.join(HERE, "EVIDENCE.tsv")
    rows = []
    if os.path.exists(evp):
        with open(evp, encoding="utf-8", newline="") as f:
            rows = [r for r in csv.reader(f, delimiter="\t")][1:]
    for slug in slugs:
        spec = json.load(open(os.path.join(SPECS, f"{slug}.json"), encoding="utf-8"))
        assert spec["slug"] == slug
        stage, ev = build(spec, u2s)
        with open(os.path.join(HERE, "crops", f"{slug}.json"), "w", encoding="utf-8") as f:
            json.dump(stage, f, ensure_ascii=False, indent=2); f.write("\n")
        rows = [r for r in rows if r[0] != slug] + ev
        print(f"{slug}: {len(stage['planting_layout'])} entr{'y' if len(stage['planting_layout'])==1 else 'ies'}, "
              f"{len(ev)} evidence rows, in_row {P.compact(stage['planting_layout'][0].get('in_row_inches'))}")
    with open(evp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(P.EVIDENCE_COLS); w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
