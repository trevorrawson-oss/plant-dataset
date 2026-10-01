#!/usr/bin/env python3
"""stage_lane_a -- PLA-10 promote 1 SESSION helper (lane A, mechanical): for each session-2 AGREES row of
worklist 56's TSV, look the page up in the fetch rows, check the row's quotes are substrings of the HASHED bytes
(the promote's own norm_text), and write the crop's stage file + its EVIDENCE rows.  No judgment: a quote that
is not in the bytes, or a page not fetched, is reported and the crop is NOT staged (it moves to lane B).

Usage: stage_lane_a.py FETCH_ROWS_TSV [FETCH_ROWS_TSV ...] --out-evidence FILE [--only slug,slug]
                       [--override overrides.json]
  overrides.json: {slug: {"in_row_quote": "...", "row_quote": "...", "row_inches": "not_authored", "note": "..."}}
  -- a VERBATIM live-page quote replacing a worklist quote that was a table-row description, or a page whose
  wording changed (same figure); "row_inches": "not_authored" withdraws a row figure the promote cannot verify.
  Every override is recorded in the crop's decision row.
"""
import argparse, csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import promote_pla10_planting_layout as P  # noqa: E402

TSV = os.path.join(REPO, "docs", "kickoffs", "56-pla10-promote1-worklist.tsv")
VERIFIED = "2026-10-01"
TEXT = {}


def page_text(sha, ext):
    if sha not in TEXT:
        raw = open(os.path.join(P.EVIDENCE, f"{sha}.{ext}"), "rb").read()
        assert P.sha256_bytes(raw) == sha
        TEXT[sha] = P.norm_text(raw.decode("utf-8", "replace"))
    return TEXT[sha]


def variants(q):
    """Candidate verbatim substrings for a worklist quote that may carry a description prefix."""
    out = [q]
    m = re.findall(r'"([^"]{12,})"', q)
    out += m
    if ": " in q:
        out.append(q.split(": ", 1)[1].strip().strip('"'))
    more = []
    for v in out:
        more.append(v.replace(" | ", " "))
        more.append(re.sub(r"\s*\|\s*", " ", v))
    out += more
    seen, res = set(), []
    for v in out:
        v = v.strip()
        if v and v not in seen:
            seen.add(v); res.append(v)
    return res


def find_quote(q, text):
    for v in variants(q):
        if len(P.norm_text(v)) >= 12 and P.norm_text(v) in text:
            return v
    return None


def parse_pair(s):
    return [x.strip() for x in re.split(r"\s*;\s*", s or "") if x.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("fetch", nargs="+")
    ap.add_argument("--out-evidence", required=True)
    ap.add_argument("--only", default=None)
    ap.add_argument("--override", default=None)
    a = ap.parse_args(argv)
    overrides = json.load(open(a.override, encoding="utf-8")) if a.override else {}
    fetched = {}
    for f in a.fetch:
        for r in csv.reader(open(f, encoding="utf-8"), delimiter="\t"):
            if len(r) >= 9 and r[8] == "ok":
                fetched[r[4]] = (r[0], "pdf" if r[7] == "application/pdf" else "html")
    only = set(a.only.split(",")) if a.only else None
    rows = [r for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t")
            if r["session"] == "2" and r["verdict"] == "AGREES" and (only is None or r["slug"] in only)]
    ev_out, staged, held = [], [], []
    pre = P.load_canonical()
    idx = P.by_slug(pre)
    for r in rows:
        slug = r["slug"]
        ov = overrides.get(slug, {})
        for k, v in ov.items():
            if k in r and isinstance(v, str):
                r[k] = v
        sids, urls = parse_pair(r["source_id"]), parse_pair(r["url"])
        by_sid = dict(zip(sids, urls))
        fields = []  # (field, value, sid, url, quote)
        inq = r["in_row_quote"]
        m = re.match(r"\((\w+)\)\s*(.*)", inq)
        sid_in = sids[0]
        if m:
            sid_in, inq = m.group(1), m.group(2)
        fields.append(("in_row_inches", json.loads(r["in_row_inches"]), sid_in, by_sid[sid_in], inq))
        row_val = r["row_inches"]
        if row_val and row_val != "not_authored":
            rq = r["row_quote"]
            m = re.match(r"\[(\w+)\s+(https?://\S+)\]\s*(.*)", rq)
            sid_r, url_r = sid_in, by_sid[sid_in]
            if m:
                sid_r, url_r, rq = m.group(1), m.group(2), m.group(3)
            else:
                m2 = re.match(r"\((\w+)\)\s*(.*)", rq)
                if m2:
                    sid_r, rq = m2.group(1), m2.group(2); url_r = by_sid[sid_r]
            fields.append(("row_spacing_inches", json.loads(row_val), sid_r, url_r, rq))
        problems, evrows = [], []
        for field, val, sid, url, q in fields:
            if url not in fetched:
                problems.append(f"{field}: page not fetched ({url})"); continue
            sha, ext = fetched[url]
            if ext == "pdf":
                problems.append(f"{field}: page is a PDF; raw bytes carry no searchable text ({url})"); continue
            hit = find_quote(q, page_text(sha, ext))
            if hit is None:
                problems.append(f"{field}: quote not in the hashed bytes: {q[:90]!r}"); continue
            if not P.quote_states(field, val, hit):
                problems.append(f"{field}: matched quote states neither endpoint of {val}: {hit[:90]!r}"); continue
            evrows.append((field, val, sid, url, sha, hit))
        if problems:
            held.append((slug, problems)); continue
        srcs, anch = [], {}
        for field, val, sid, url, sha, hit in evrows:
            if sid not in srcs:
                srcs.append(sid); anch[sid] = {"url": url, "verified": VERIFIED}
        in_row = evrows[0][1]
        row_sp = next((e[1] for e in evrows if e[0] == "row_spacing_inches"), None)
        entry = {"id": "row-none", "arrangement": "row", "support": "none", "default": True,
                 "in_row_inches": in_row, "row_spacing_inches": row_sp,
                 "row_spacing_reason": None if row_sp is not None else "not_authored",
                 "sources": srcs, "anchoring_urls": anch}
        cur = idx[slug].get("spacing_inches")
        assert P.compact(cur) == P.compact(in_row), (slug, cur, in_row)
        parts = [f"AGREES (lane A, mechanical; worklist 56 §4): {e[2]} {e[3]} states \"{e[5]}\" -> {e[0]} {P.compact(e[1])}"
                 for e in evrows]
        if row_sp is None:
            parts.append("no between-rows figure on the cited page: row_spacing_inches not_authored")
        decision = "; ".join(parts) + f". Today's spacing_inches {P.compact(cur)} is unchanged; quotes checked as substrings of the hashed bytes."
        if ov:
            applied = [f"{k} = {v!r}" for k, v in ov.items() if k not in ("note", "retired_anchor_dropped")]
            if applied:
                decision += " Override(s) applied: " + "; ".join(applied) + "."
        if ov.get("note"):
            decision += " " + ov["note"]
        stage = {"slug": slug, "decision": decision, "planting_layout": [entry]}
        if P.RETIRED in idx[slug]:
            ra = {}
            for sid, old in idx[slug][P.RETIRED].items():
                if anch.get(sid, {}).get("url") == old["url"]:
                    ra[sid] = "moved"
                else:
                    reason = (ov.get("retired_anchor_dropped") or {}).get(sid, "PENDING")
                    ra[sid] = {"dropped": reason}
            stage["retired_anchor"] = ra
        path = os.path.join(HERE, "crops", f"{slug}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stage, f, ensure_ascii=False, indent=2); f.write("\n")
        for field, val, sid, url, sha, hit in evrows:
            ev_out.append([slug, "row-none", field, P.compact(val), sid, url, sha, hit])
        staged.append(slug)
    with open(a.out_evidence, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(P.EVIDENCE_COLS)
        w.writerows(ev_out)
    print(f"rows read {len(rows)}; staged {len(staged)}; held {len(held)}; evidence rows {len(ev_out)}")
    print("STAGED:", " ".join(staged))
    for slug, probs in held:
        print(f"HELD {slug}:")
        for p in probs:
            print("   ", p)
    pend = [s for s in staged if P.RETIRED in idx[s]]
    if pend:
        print("retired_anchor to fill by hand (PENDING drops):", pend)
    return 0


if __name__ == "__main__":
    sys.exit(main())
