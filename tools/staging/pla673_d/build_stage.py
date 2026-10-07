#!/usr/bin/env python3
"""Build the PLA-673 part D promote stage (ops.json, EVIDENCE.tsv, DECISIONS.tsv) from the ruled texts (d_texts.py), the
posted packets (PP = pepper, C = part C, numbered as posted) and the watermelon thinning quotes (W). Base canonical aaf004a2.

Every ref resolves to (page url, verbatim quote) through the SAME builders that posted the packets; each becomes an
EVIDENCE row under the source id the leaf's citation block names for that page. Prints the post SHA from an INDEPENDENT
minimal apply (no promote code).
"""
import copy, csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.dirname(TOOLS)
PREP = os.path.join(TOOLS, "staging", "pla673_674_prep")
sys.path.insert(0, TOOLS)
sys.path.insert(0, PREP)
sys.path.insert(0, HERE)
import build_packets as bp  # noqa: E402
from cited_promote_common import resolve  # noqa: E402
from d_texts import LEAVES, VALUES, SOURCES, W, W_URL, PB, ROW, THIN  # noqa: E402

BASE_SHA = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"
TODAY = "2026-10-06"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
DECISION_COLS = ("crop", "path", "decision", "reason")
PAGE_ID = {  # page key -> the citation id it is cited under on these leaves
    "ncsu_pb": "ncsu_ext_phytophthora_blight_peppers", "umn_pep": "umn_ext",
    "uf": "uf_ifas", "uga": "uga_ext", "usu": "usu_ext", "umn": "umn_ext",
}


def _load(path, upto):
    src = open(path, encoding="utf-8").read().split(upto)[0]
    ns = {"__file__": path}
    exec(compile(src, path, "exec"), ns)
    return ns


def refs():
    """{(packet, key): (page_key, url, quote)} with each builder's own row numbering."""
    rr = _load(os.path.join(PREP, "build_b2r2_packets.py"), "def table")
    pc = _load(os.path.join(PREP, "build_partc_packet.py"), "def main")
    out, n = {}, 0
    for row in rr["PEPPER"]:                   # PP numbers every row (a quote-less claim takes one)
        *_meta, qs = row
        if not qs:
            n += 1
            continue
        for src, q, _scope in qs:
            n += 1
            out[("PP", n)] = (src, rr["U"][src][0], q)
    for i, (src, _kind, q) in enumerate(pc["ROWS"], 1):   # C numbers every quote
        out[("C", i)] = (src, pc["SRC"][src][0], q)
    for k, (page, q) in W.items():
        out[("W", k)] = (page, W_URL[page], q)
    return out


def sha_of(url):
    hits = [s for s, us in bp.MAN.items() if url in us]
    assert len(hits) == 1, (url, hits)
    return hits[0]


def _get(crop, path):
    node = crop
    for k in resolve(crop, path):
        node = node[k]
    return node


def build():
    raw = open(os.path.join(REPO, "crops_data_final.json"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise SystemExit("canonical is not aaf004a2")
    pre = json.loads(raw)
    by = {c["slug"]: c for c in pre["crops"]}
    R = refs()
    ops, ev, dec, anchors = [], [], [], {}

    def evidence(crop, path, block, i, value, rlist):
        for ref in rlist:
            src, url, q = R[ref]
            sid = PAGE_ID[src]
            if sid not in SOURCES[(crop, block)]:
                raise SystemExit(f"{crop} {path} [{i}]: {ref} is on {sid}, which {block} does not cite")
            if anchors.setdefault((crop, block), {}).setdefault(sid, url) != url:
                raise SystemExit(f"{crop} {block}: {sid} would anchor two urls")
            ev.append({"crop": crop, "entry_id": path, "field": f"sentence {i} ({ref[0]} {ref[1]})", "value": value,
                       "source_id": sid, "url": url, "sha256": sha_of(url), "quote": q})

    for crop, path, sents in LEAVES:
        block = path.split(".")[0] if path.startswith(THIN) else PB
        text = " ".join(s for s, _r in sents)
        ops.append({"crop": crop, "path": path, "kind": "prose", "old": _get(by[crop], path), "new": text,
                    "cited_at": block, "reason": "PLA-673 part D: approved text (claude.ai, Trevor)"})
        for i, (s, rl) in enumerate(sents, 1):
            evidence(crop, path, block, i, s, rl)
    for crop, path, new, block, rl in VALUES:
        ops.append({"crop": crop, "path": path, "kind": "value", "old": _get(by[crop], path), "new": new,
                    "cited_at": block, "reason": "PLA-673 part D: UF VH021 (24-48 in-row, 60 rows), the consensus ruling"
                    + ("; the crop-root mirror of the first entry carrying in_row_inches" if "." not in path else "")})
        evidence(crop, path, block, 1, json.dumps(new), rl)
    for (crop, block), sids in SOURCES.items():
        node = _get(by[crop], block)
        cur_s, cur_a = node.get("sources", "<absent>"), node.get("anchoring_urls", "<absent>")
        used = anchors.get((crop, block), {})
        new_a = {}
        for sid in sids:
            if sid not in used:
                raise SystemExit(f"{crop} {block}: {sid} supports no evidenced sentence")
            new_a[sid] = {"url": used[sid], "verified": TODAY}
        ops.append({"crop": crop, "path": f"{block}.sources", "kind": "sources", "old": cur_s, "new": list(sids),
                    "cited_at": None, "reason": "PLA-673 part D: the block's citation, as ruled"})
        ops.append({"crop": crop, "path": f"{block}.anchoring_urls", "kind": "anchors", "old": cur_a, "new": new_a,
                    "cited_at": None, "reason": "PLA-673 part D: anchoring map keyed by source id (convention)"})
    dec += [
        {"crop": "watermelon", "path": ROW, "decision": "layout-consensus-rule",
         "reason": "RULED 2026-10-06: where cited T1 sources disagree on a layout figure, the entry takes ONE T1 source whose "
                   "figures sit inside the consensus of the cited sources. UF VH021 is that source: four of six fall within "
                   "24-48 in-row (WSU 24-36, UF 24-48, VT 36-48, NMSU CR457B 24-36) and 60 in rows appear in WSU, UF and VT. "
                   "Recorded as the wide end, NOT cited on this entry: Clemson HGIC (60-72 x 72-96, the previous source) and "
                   "OSU (60 x 72)."},
        {"crop": "watermelon", "path": f"{THIN}.tip_seasoned", "decision": "cut",
         "reason": "the icebox / full-size split is cut: no source draws it; sentences 1-2 re-authored (part D ruling, "
                   "option a): no cited page states three to four seeds (USU 4-6, UGA C1035 4-5, UMN 2-3) or snipping"},
        {"crop": "watermelon", "path": f"{THIN}.method", "decision": "free-text-set",
         "reason": "free text (13 distinct values roster-wide, no enum, no consumer renders it): 'snip extras at soil line' "
                   "is stated by no cited watermelon page; set to 'thin to two plants per hill' (USU, UGA C1035), as ruled"},
        {"crop": "watermelon", "path": f"{THIN}.to_spacing", "decision": "kept",
         "reason": "'2 plants per hill' holds (USU, UGA C1035); left as ruled"},
    ]
    for pep in ("bell-pepper", "banana-pepper"):
        dec += [
            {"crop": pep, "path": f"{PB}.sources", "decision": "removed",
             "reason": "ncsu_ext (the NC State pepper-diseases INDEX page) and clemson_hgic come off: no new claim rests on "
                       "them (PLA-688); the entry cites the factsheet itself + UMN growing-peppers, and is identical on both peppers"},
            {"crop": pep, "path": f"{PB}.organic_treatment_seasoned", "decision": "omitted",
             "reason": "fixed copper deliberately omitted: NC State's copper sentence is for organic FARMS; its home-garden "
                       "sentence says no chemical option is effective"},
            {"crop": pep, "path": f"{PB}.control_ladder[method=improve_drainage]", "decision": "cut",
             "reason": "the old 'drainage correction as the immediate response' claim is cut: NC State states drainage as "
                       "site choice only"},
            {"crop": pep, "path": f"{PB}.control_ladder[method=splash_barrier_mulch].method", "decision": "kept",
             "reason": "the rung id stays (renaming is a structural change); see the bundle README for how consumers render it"},
        ]
    return pre, ops, ev, dec


def minimal_apply(pre, ops):
    """INDEPENDENT of the promote: set each op's value at its resolved path."""
    post = copy.deepcopy(pre)
    by = {c["slug"]: c for c in post["crops"]}
    for op in ops:
        node = by[op["crop"]]
        keys = resolve(node, op["path"])
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = copy.deepcopy(op["new"])
    return post


def main():
    pre, ops, ev, dec = build()
    with open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=1)
    for name, cols, rows in (("EVIDENCE.tsv", EVIDENCE_COLS, ev), ("DECISIONS.tsv", DECISION_COLS, dec)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    post = minimal_apply(pre, ops)
    blob = json.dumps(post, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    kinds = {}
    for op in ops:
        kinds[op["kind"]] = kinds.get(op["kind"], 0) + 1
    print(f"ops {len(ops)} {kinds}; evidence rows {len(ev)}; decisions {len(dec)}")
    print(f"independent minimal apply: {BASE_SHA[:8]} -> {hashlib.sha256(blob).hexdigest()}")


if __name__ == "__main__":
    main()
