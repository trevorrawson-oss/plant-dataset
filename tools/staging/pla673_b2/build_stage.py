#!/usr/bin/env python3
"""Build the PLA-673 part B2 promote stage (ops.json, EVIDENCE.tsv, DECISIONS.tsv) from the ruled texts (b2_texts.py)
and the posted packets (B2 / BS / PS / PP, numbered as posted). Base canonical 3ccc25f1.

Every sentence's packet rows are resolved to (page, verbatim quote) through the SAME builders that posted the packets,
so a row number means what the posted packet showed. Each row becomes an EVIDENCE row under the source id the leaf's
citation block names for that page. Prints the post SHA from an INDEPENDENT minimal apply (no promote code).
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
from b2_texts import LEAVES, SOURCES  # noqa: E402

BASE_SHA = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"
TODAY = "2026-10-06"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
DECISION_COLS = ("crop", "path", "decision", "reason")


def _load(path, upto):
    src = open(path, encoding="utf-8").read().split(upto)[0]
    ns = {"__file__": path}
    exec(compile(src, path, "exec"), ns)
    return ns


def packets():
    """{packet: {row: (page_key, url, quote)}} with each builder's own row numbering."""
    b2 = _load(os.path.join(PREP, "build_b2_packet.py"), "def section")
    rr = _load(os.path.join(PREP, "build_b2r2_packets.py"), "def table")
    out = {"B2": {}}
    n = 0
    for rows in (b2["PEP"], b2["SQ"]):
        for _claim, _v, qs in rows:          # B2 numbers QUOTES only (a quote-less claim gets no row)
            for src, q, _scope in qs:
                n += 1
                out["B2"][n] = (src, b2["U"][src], q)
    for key, rows in (("PP", rr["PEPPER"]), ("PS", rr["PARSNIP"]), ("BS", rr["BEGINNER"])):
        out[key], n = {}, 0
        for row in rows:                      # BS/PS/PP number every row (a quote-less claim takes one)
            *_meta, qs = row
            if not qs:
                n += 1
                continue
            for src, q, _scope in qs:
                n += 1
                out[key][n] = (src, rr["U"][src][0], q)
    return out


PAGE_ID = {  # packet page key -> the citation id it is cited under on these leaves
    "clem_egg": "clemson_hgic", "ncsu_pb": "ncsu_ext_phytophthora_blight_peppers", "c1206": "uga_c1206_homegrown_pumpkins",
    "umn_pk": "umn_ext", "umass": "umass_ext_itersonilia_canker", "umn_cp": "umn_ext", "clem_root": "clemson_hgic",
    "rhs": "rhs",
}


def sha_of(url):
    hits = [s for s, us in bp.MAN.items() if url in us]
    assert len(hits) == 1, (url, hits)
    return hits[0]


def compact(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)


def build():
    raw = open(os.path.join(REPO, "crops_data_final.json"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise SystemExit("canonical is not 3ccc25f1")
    pre = json.loads(raw)
    by = {c["slug"]: c for c in pre["crops"]}
    pk = packets()
    mints = json.load(open(os.path.join(HERE, "catalog_mints.json"), encoding="utf-8"))
    ops, ev, dec = [], [], []
    anchors = {}   # (crop, block) -> {sid: url}
    for crop, path, sents in LEAVES:
        block = "<soil_prep>" if path.startswith("soil_prep_") else path.rsplit(".", 1)[0]
        old = by[crop]
        for k in resolve(by[crop], path):
            old = old[k]
        text = " ".join(s for s, _r in sents)
        ops.append({"crop": crop, "path": path, "kind": "prose", "old": old, "new": text,
                    "cited_at": block, "reason": "PLA-673 part B2: approved text (claude.ai, Trevor), round 1/2"})
        for i, (s, refs) in enumerate(sents, 1):
            for packet, row in refs:
                src, url, q = pk[packet][row]
                sid = PAGE_ID[src]
                if sid not in SOURCES[(crop, block)]:
                    raise SystemExit(f"{crop} {path} [{i}]: {packet} {row} is on {sid}, which the block does not cite")
                anchors.setdefault((crop, block), {})
                if anchors[(crop, block)].setdefault(sid, url) != url:
                    raise SystemExit(f"{crop} {block}: {sid} would anchor two urls")
                ev.append({"crop": crop, "entry_id": path, "field": f"sentence {i} ({packet} {row})", "value": s,
                           "source_id": sid, "url": url, "sha256": sha_of(url), "quote": q})
    # citation blocks: sources + anchoring_urls
    for (crop, block), sids in SOURCES.items():
        used = anchors.get((crop, block), {})
        if block == "<soil_prep>":
            spath, apath, old_s, old_a = "soil_prep_sources", "soil_prep_anchoring_urls", None, None
            cur_s, cur_a = by[crop]["soil_prep_sources"], by[crop]["soil_prep_anchoring_urls"]
        else:
            spath, apath = f"{block}.sources", f"{block}.anchoring_urls"
            node = by[crop]
            for k in resolve(by[crop], block):
                node = node[k]
            cur_s, cur_a = node.get("sources", "<absent>"), node.get("anchoring_urls", "<absent>")
        new_a = {}
        for sid in sids:
            if sid in used:
                new_a[sid] = {"url": used[sid], "verified": TODAY}
            elif isinstance(cur_a, dict) and sid in cur_a:
                new_a[sid] = cur_a[sid]                       # kept anchor, byte-identical
                dec.append({"crop": crop, "path": f"{apath}.{sid}", "decision": "kept",
                            "reason": "anchors fields of this entry the B2 re-author did not touch; not re-verified here"})
            else:
                raise SystemExit(f"{crop} {block}: {sid} has neither an evidence url nor an existing anchor")
        ops.append({"crop": crop, "path": spath, "kind": "sources", "old": cur_s, "new": list(sids), "cited_at": None,
                    "reason": "PLA-673 part B2: the leaf's citation, as ruled"})
        ops.append({"crop": crop, "path": apath, "kind": "anchors", "old": cur_a, "new": new_a, "cited_at": None,
                    "reason": "PLA-673 part B2: anchoring map keyed by source id (convention)"})
    for sid, entry in mints.items():
        if sid.startswith("_"):
            continue
        ops.append({"crop": "<catalog>", "path": sid, "kind": "catalog", "old": "<absent>", "new": entry, "cited_at": None,
                    "reason": "PLA-673 part B2: document-level id (rulings 4/5; eggplant ruling)"})
    dec += [
        {"crop": "eggplant", "path": f"{LEAVES[0][1].rsplit('.', 1)[0]}.prevention_seasoned", "decision": "precedence-rule",
         "reason": "RULED 2026-10-06 (methodology v1.4 candidate): within a disease's entry, a pathogen-specific T1 page "
                   "governs over a general rotation paragraph covering several diseases. NC State's P. capsici factsheet "
                   "(eggplant and most cucurbits are hosts; rotation weakened; cereals non-hosts) governs over Clemson's "
                   "three-disease paragraph. CONFLICTING SOURCE recorded: Clemson eggplant 635ebdeb 'instead, rotate with "
                   "cucurbits (squash, zucchini, melons, and cantaloupe), brassicas ..., grasses ..., alliums ..., etc.' "
                   "Clemson's three-year Solanaceae rule stands."},
        {"crop": "parsnip", "path": "diseases[id=itersonilia-canker].anchoring_urls", "decision": "re-keyed",
         "reason": "umass_ext -> umass_ext_itersonilia_canker: the SAME page (UMass canker factsheet), now its document-level "
                   "id, as ruled for diseases[0] and failure_diagnostics[3]; untouched fields that cited it keep the same page"},
        {"crop": "parsnip", "path": "diseases[id=itersonilia-canker].anchoring_urls.usu_ext", "decision": "removed",
         "reason": "usu_ext came from the pre-state block; no B2 sentence cites it and its page (USU root-crop pest index, "
                   "doc_cache fd64745f) only lists 'Itersonilia Canker' by name, so it supports no field of the entry; the "
                   "untouched fields credit UMass. Removed as ruled (Trevor, B2 go-condition 1, 2026-10-06)"},
        {"crop": "parsnip", "path": "growth_stages[id=established]", "decision": "new-citation-block",
         "reason": "the stage had no citation block; growth_stages entries carry sources + anchoring_urls in place "
                   "(113 precedents); rhs is T1 in the catalog, so sentence 1 keeps RHS beside UMN"},
        {"crop": "parsnip", "path": "<inline-attribution>", "decision": "dropped",
         "reason": "the old leaves ended '(UMass)'; the new texts carry sources in the arrays; no consumer source reads the "
                   "inline tag (grep of plant-app src/scripts and plant-astro src/scripts, 2026-10-06)"},
        {"crop": "<roster>", "path": "soil_prep", "decision": "a62-armed",
         "reason": "A62 arms soil_prep in this promote (ruled): waiver set = the 35 certified crops with soil_prep prose and "
                   "null sources after this backfill"},
    ]
    return pre, ops, ev, dec


def minimal_apply(pre, ops):
    """INDEPENDENT of the promote: set each op's value; new keys appended where they are created."""
    post = copy.deepcopy(pre)
    by = {c["slug"]: c for c in post["crops"]}
    for op in ops:
        if op["kind"] == "catalog":
            post["source_catalog"][op["path"]] = copy.deepcopy(op["new"])
            continue
        node = by[op["crop"]]
        keys = resolve(node, op["path"]) if not op["path"].endswith(("sources", "anchoring_urls")) or "." in op["path"] \
            else [op["path"]]
        if op["old"] == "<absent>":
            parent = node
            for k in resolve(node, op["path"].rsplit(".", 1)[0]):
                parent = parent[k]
            parent[op["path"].rsplit(".", 1)[1]] = copy.deepcopy(op["new"])
            continue
        parent = node
        for k in keys[:-1]:
            parent = parent[k]
        parent[keys[-1]] = copy.deepcopy(op["new"])
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
