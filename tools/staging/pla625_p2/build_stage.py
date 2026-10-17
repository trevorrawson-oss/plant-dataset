#!/usr/bin/env python3
"""build_stage -- writes ops.json, EVIDENCE.tsv and DECISIONS.tsv for promote_pla625_p2 from p2_texts.py, against the
base canonical (2f67359e, PLA-625 citrus promote 1). Deterministic: run it twice, get the same bytes.

Every op's `old` is read from the base, so a moved base fails the promote's check_pre rather than being papered over.
Row paths are INDEX paths (rootstock_options[i]) because lemon [2] is renamed and lemon [3] / lime [2] are new rows.
A value the ruling leaves as it was is NOT an op: it is a `retained` DECISIONS row, and a retained non-null value still
carries EVIDENCE rows (the row's old citations are dropped, so the value needs its new basis on record).

Op kinds beyond promote 1's: `row` (a ruled new row, appended whole), `rename` (a row's name), `catalog` (a minted
per-publication id, ruling A.1) and `rekey` (promote 1's HS1260 citations moved from uf_ifas_edis to uf_ifas_hs1260,
ruling A.2: mechanical, no value or url changes).

Usage: build_stage.py [--canonical PATH]
"""
import argparse, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, HERE)
import p2_texts as T  # noqa: E402

TODAY = "2026-10-16"
SESSION = "pla625_promote2_2026_10_16"
RULING = "PLA-625 promote 2 ruling (claude.ai comment abaa4aa8, approved by Trevor, 2026-10-14)"
AMEND = "PLA-625 promote 2 amendment (claude.ai comment 07cc6df5, approved by Trevor, 2026-10-16)"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
NOTE_BLOCK = "recommended_rootstock_note"
ROW_FIELDS = ("name", "size_class", "mature_height_ft", "spread_ft", "container_suitable", "container_size_gallons",
              "bearing_age_years", "what_to_ask_nursery", "traits_seasoned", "traits_beginner", "sources",
              "anchoring_urls")
VALUE_FIELDS = ROW_FIELDS[1:7]
PROSE_FIELDS = ("traits_seasoned", "traits_beginner", "what_to_ask_nursery")
HS1260_SCOPE = ("HS1260 scope (promote 1 ruling A.1): Florida commercial groves; relative vigor; averaged across "
                "commercial scions; not scion-specific.")
SECTION = {T.LEMON: "C", T.LIME: "D"}
REKEY_FROM, REKEY_TO = "uf_ifas_edis", "uf_ifas_hs1260"
REKEY_CROPS = ("orange-navel", "grapefruit")


def _ids(labels):
    out = []
    for lab in labels:
        sid = T.SOURCES[lab][0]
        if sid not in out:
            out.append(sid)
    return out


def _anchors(labels):
    out = {}
    for lab in labels:
        sid, url, _sha = T.SOURCES[lab]
        if sid in out and out[sid]["url"] != url:
            raise SystemExit(f"STOP: two URLs under {sid} in one block ({out[sid]['url']} vs {url})")
        out[sid] = {"url": url, "verified": TODAY}
    return out


def _labels_used(keys):
    return {T.QUOTES[k][0] for k in keys}


def _ev(rows, crop, path, field, value, keys):
    for k in keys:
        lab, quote = T.QUOTES[k]
        sid, url, sha = T.SOURCES[lab]
        rows.append({"crop": crop, "entry_id": path, "field": f"{field} ({k})", "value": value, "source_id": sid,
                     "url": url, "sha256": sha, "quote": quote})


def _rekeyed(v):
    if isinstance(v, list):
        return [REKEY_TO if s == REKEY_FROM else s for s in v]
    return {(REKEY_TO if k == REKEY_FROM else k): a for k, a in v.items()}


def build(base):
    crops = {c["slug"]: c for c in base["crops"]}
    ops, ev, dec = [], [], []

    def op(crop, path, kind, old, new, cited_at, reason):
        ops.append({"crop": crop, "path": path, "kind": kind, "old": old, "new": new, "cited_at": cited_at,
                    "reason": reason})

    # catalog first (ruling A.1): the ids every later block cites
    for sid, entry in T.CATALOG.items():
        if sid in base["source_catalog"]:
            raise SystemExit(f"STOP: {sid} already in source_catalog (ruling A.1: use it)")
        op("<catalog>", sid, "catalog", "<absent>", entry, None, f"{RULING} A.1: per-publication id")

    for crop in (T.LEMON, T.LIME):
        c = crops[crop]
        sec = f"{RULING} {SECTION[crop]}"
        rows = T.ROWS[crop]
        have = c["rootstock_options"]
        if [r["name"] for r in have] != [r["old"] for r in rows if not r["new"]]:
            raise SystemExit(f"STOP: {crop} rows are {[r['name'] for r in have]}")
        for i, r in enumerate(rows):
            blk = f"rootstock_options[{i}]"
            labels = set(r["sources"])
            for f, sents in r["prose"].items():
                for n, (s, ks) in enumerate(sents, 1):
                    if not _labels_used(ks) <= labels:
                        raise SystemExit(f"STOP: {crop} {blk}.{f} sentence {n} rests on a page its row does not cite")
            if r["new"]:
                if len(have) != i:
                    raise SystemExit(f"STOP: {crop} new row at {i}, but the base has {len(have)} rows")
                row = {"name": r["name"]}
                for f in VALUE_FIELDS:
                    v, basis = r["values"][f]
                    if v is not None:
                        raise SystemExit(f"STOP: {crop} new row {f} is non-null; this stage stages null new values only")
                    row[f] = None
                    dec.append({"crop": crop, "path": f"{blk}.{f}", "decision": "new-null", "reason": basis})
                for f in PROSE_FIELDS:
                    row[f] = " ".join(s for s, _k in r["prose"][f])
                row["sources"], row["anchoring_urls"] = _ids(r["sources"]), _anchors(r["sources"])
                row = {f: row[f] for f in ROW_FIELDS}
                op(crop, blk, "row", "<absent>", row, blk, f"{sec}: new row")
                for f in PROSE_FIELDS:
                    for n, (s, ks) in enumerate(r["prose"][f], 1):
                        _ev(ev, crop, f"{blk}.{f}", f"sentence {n}", s, ks)
            else:
                old_row = have[i]
                if r["name"] is not None:
                    op(crop, f"{blk}.name", "rename", old_row["name"], r["name"], blk, f"{sec}: renamed")
                    dec.append({"crop": crop, "path": f"{blk}.name", "decision": "renamed",
                                "reason": f"{sec}: Carrizo comes off lemon; no page read names it as a lemon rootstock"})
                for f in VALUE_FIELDS:
                    new, basis = r["values"][f]
                    path = f"{blk}.{f}"
                    if new is None:
                        if old_row[f] is None:
                            dec.append({"crop": crop, "path": path, "decision": "retained",
                                        "reason": f"null kept: {basis}"})
                        else:
                            op(crop, path, "value", old_row[f], None, blk, f"nulled ({sec})")
                            dec.append({"crop": crop, "path": path, "decision": "nulled", "reason": basis})
                        continue
                    if not _labels_used(basis) <= labels:
                        raise SystemExit(f"STOP: {crop} {path} rests on a page its row does not cite")
                    if old_row[f] == new:
                        dec.append({"crop": crop, "path": path, "decision": "retained",
                                    "reason": f"value unchanged, re-based on the row's new sources ({sec})"})
                    else:
                        op(crop, path, "value", old_row[f], new, blk, sec)
                    _ev(ev, crop, path, f, json.dumps(new), basis)
                for f in PROSE_FIELDS:
                    sents = r["prose"][f]
                    path = f"{blk}.{f}"
                    op(crop, path, "prose", old_row[f], " ".join(s for s, _k in sents), blk, sec)
                    for n, (s, ks) in enumerate(sents, 1):
                        _ev(ev, crop, path, f"sentence {n}", s, ks)
                op(crop, f"{blk}.sources", "sources", old_row["sources"], _ids(r["sources"]), blk, sec)
                op(crop, f"{blk}.anchoring_urls", "anchors", old_row["anchoring_urls"], _anchors(r["sources"]), blk,
                   sec)
            if "uf_ifas_hs1260" in _ids(r["sources"]):
                dec.append({"crop": crop, "path": blk, "decision": "hs1260-scope", "reason": HS1260_SCOPE})

        new, basis = T.RECOMMENDED[crop]
        if c["recommended_rootstock"] is None:
            dec.append({"crop": crop, "path": "recommended_rootstock", "decision": "retained", "reason": basis})
        else:
            op(crop, "recommended_rootstock", "value", c["recommended_rootstock"], None, NOTE_BLOCK, f"nulled ({sec})")
            dec.append({"crop": crop, "path": "recommended_rootstock", "decision": "nulled", "reason": basis})
        labels = set(T.NOTE_SOURCES[crop])
        sents = T.NOTE[crop]
        op(crop, NOTE_BLOCK, "prose", c[NOTE_BLOCK], " ".join(s for s, _k in sents), NOTE_BLOCK, sec)
        for n, (s, ks) in enumerate(sents, 1):
            if not _labels_used(ks) <= labels:
                raise SystemExit(f"STOP: {crop} note sentence {n} rests on a page the note does not cite")
            _ev(ev, crop, NOTE_BLOCK, f"sentence {n}", s, ks)
        op(crop, "recommended_rootstock_note_sources", "sources", c["recommended_rootstock_note_sources"],
           _ids(T.NOTE_SOURCES[crop]), NOTE_BLOCK, sec)
        op(crop, "recommended_rootstock_note_anchoring_urls", "anchors", c["recommended_rootstock_note_anchoring_urls"],
           _anchors(T.NOTE_SOURCES[crop]), NOTE_BLOCK, sec)

        add = []
        old_of = c["verification_status"]["open_findings"]
        for fid, summary in T.FINDINGS[crop]:
            if fid in {f["id"] for f in old_of}:
                raise SystemExit(f"STOP: {crop} already carries finding {fid}")
            add.append({"id": fid, "severity": "low", "status": "open", "blocks_launch": False,
                        "filed_in_session": SESSION, "summary": summary,
                        "basis": f"{RULING} C; PLA-609. Non-blocking: the row describes the stock."})
        if add:
            op(crop, "verification_status.open_findings", "record", old_of, old_of + add, None, f"{sec} (PLA-609)")
            dec.append({"crop": crop, "path": "verification_status.open_findings", "decision": "record-only",
                        "reason": f"{len(add)} non-blocking PLA-609 finding(s) appended; no existing finding touched"})

    # ruling A.2: promote 1's HS1260 citations re-keyed, mechanically
    for crop in REKEY_CROPS:
        c = crops[crop]
        blocks = [(f"rootstock_options[{i}]", f"rootstock_options[{i}].sources", f"rootstock_options[{i}].anchoring_urls",
                   r["sources"], r["anchoring_urls"]) for i, r in enumerate(c["rootstock_options"])]
        blocks.append((NOTE_BLOCK, "recommended_rootstock_note_sources", "recommended_rootstock_note_anchoring_urls",
                       c["recommended_rootstock_note_sources"], c["recommended_rootstock_note_anchoring_urls"]))
        for blk, sp, ap, srcs, anc in blocks:
            if REKEY_FROM not in (srcs or []):
                continue
            if anc[REKEY_FROM]["url"] != T.SOURCES["HS1260"][1]:
                raise SystemExit(f"STOP: {crop} {blk} cites {REKEY_FROM} at {anc[REKEY_FROM]['url']}, not HS1260")
            op(crop, sp, "rekey", srcs, _rekeyed(srcs), blk, f"{RULING} A.2: re-key, no value change")
            op(crop, ap, "rekey", anc, _rekeyed(anc), blk, f"{RULING} A.2: re-key, no value change")

    dec += [
        {"crop": "<catalog>", "path": "uf_ifas_ch092", "decision": "source-id",
         "reason": f"{RULING} A.1: minted; replaces uf_ifas_edis (CH092) on lime row 0"},
        {"crop": "<catalog>", "path": "uf_ifas_ch093", "decision": "source-id",
         "reason": f"{RULING} A.1: minted; replaces ufifas_ext (CH093) on lime rows 0 and 1"},
        {"crop": "<catalog>", "path": "uf_ifas_hs1260", "decision": "source-id",
         "reason": f"{RULING} A.1: minted; promote 1's HS1260 references re-keyed onto it (A.2)"},
        {"crop": "lemon", "path": "rootstock_options[0].sources.uf_ifas_hs132", "decision": "kept-hs132",
         "reason": f"{AMEND} item 2: HS132 stays where a row makes the generic retail claim (lemon [0] "
                   f"what_to_ask_nursery sentence 1)"},
        {"crop": "lemon", "path": "rootstock_options[0..1].anchoring_urls.tamu_agrilife", "decision": "anchor-repoint",
         "reason": f"{AMEND} item 3: bare host -> citrus fact sheet; both rows co-cite HS402, so no A63 waiver moves"},
    ]
    return ops, ev, dec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", default=os.path.join(REPO, "crops_data_final.json"))
    args = ap.parse_args(argv)
    with open(args.canonical, encoding="utf-8") as f:
        base = json.load(f)
    ops, ev, dec = build(base)
    with open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for name, cols, rows in (("EVIDENCE.tsv", EVIDENCE_COLS, ev),
                             ("DECISIONS.tsv", ("crop", "path", "decision", "reason"), dec)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    kinds = {}
    for o in ops:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    print(f"ops {len(ops)} {kinds}; evidence {len(ev)}; decisions {len(dec)}")


if __name__ == "__main__":
    main()
