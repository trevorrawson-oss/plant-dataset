#!/usr/bin/env python3
"""build_stage -- writes ops.json, EVIDENCE.tsv and DECISIONS.tsv for promote_pla625_p1 from p1_texts.py, against the
base canonical (59010fe6, the PLA-625 citrus housekeeping landing). Deterministic: run it twice, get the same bytes.

Every op's `old` is read from the base, so a moved base fails the promote's check_pre rather than being papered over.
A value the ruling leaves as it was is NOT an op: it is a `retained` DECISIONS row, and a retained non-null value still
carries EVIDENCE rows (the row's old citations are dropped, so the value needs its new basis on record).

Usage: build_stage.py [--canonical PATH]
"""
import argparse, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, HERE)
import p1_texts as T  # noqa: E402

TODAY = "2026-10-13"
SESSION = "pla625_promote1_2026_10_13"
RULING = "PLA-625 promote 1 ruling (claude.ai comment 6ab0c56a, approved by Trevor, 2026-10-13)"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
NOTE_BLOCK = "recommended_rootstock_note"
ROWS = (T.CARRIZO, T.SWINGLE, T.FD)
PROSE_FIELDS = ("traits_seasoned", "traits_beginner", "what_to_ask_nursery")
HS1260_SCOPE = ("HS1260 scope (ruling A.1): Florida commercial groves; relative vigor; averaged across commercial "
                "scions; not scion-specific.")


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
            raise SystemExit(f"STOP: two URLs under {sid} in one block ({out[sid]['url']} vs {url}) -- ruling C")
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


def build(base):
    crops = {c["slug"]: c for c in base["crops"]}
    ops, ev, dec = [], [], []

    def op(crop, path, kind, old, new, cited_at, reason):
        ops.append({"crop": crop, "path": path, "kind": kind, "old": old, "new": new, "cited_at": cited_at,
                    "reason": reason})

    for crop in T.BOTH:
        c = crops[crop]
        names = [r["name"] for r in c["rootstock_options"]]
        if names != list(ROWS):
            raise SystemExit(f"STOP: {crop} rootstock_options are {names}, the ruling names {list(ROWS)}")
        for i, name in enumerate(ROWS):
            row = c["rootstock_options"][i]
            blk = f"rootstock_options[name={name}]"
            labels = set(T.ROW_SOURCES[name])
            for f, (new, basis) in T.VALUES[name].items():
                path = f"{blk}.{f}"
                if new is None:
                    if row[f] is None:
                        dec.append({"crop": crop, "path": path, "decision": "retained", "reason": f"null kept: {basis}"})
                    else:
                        op(crop, path, "value", row[f], None, blk, f"nulled ({RULING} D)")
                        dec.append({"crop": crop, "path": path, "decision": "nulled", "reason": basis})
                    continue
                if not _labels_used(basis) <= labels:
                    raise SystemExit(f"STOP: {crop} {path} rests on a page its row does not cite")
                if row[f] == new:
                    dec.append({"crop": crop, "path": path, "decision": "retained",
                                "reason": f"value unchanged, re-based on the row's new sources ({RULING} D)"})
                else:
                    op(crop, path, "value", row[f], new, blk, f"{RULING} D")
                _ev(ev, crop, path, f, json.dumps(new), basis)
            for f in PROSE_FIELDS:
                sents = [(s, ks) for s, ks, on in T.PROSE[name][f] if crop in on]
                text = " ".join(s for s, _ks in sents)
                path = f"{blk}.{f}"
                op(crop, path, "prose", row[f], text, blk, f"{RULING} D")
                for n, (s, ks) in enumerate(sents, 1):
                    if not _labels_used(ks) <= labels:
                        raise SystemExit(f"STOP: {crop} {path} sentence {n} rests on a page its row does not cite")
                    _ev(ev, crop, path, f"sentence {n}", s, ks)
            new_src = _ids(T.ROW_SOURCES[name])
            op(crop, f"{blk}.sources", "sources", row["sources"], new_src, blk, f"{RULING} D")
            op(crop, f"{blk}.anchoring_urls", "anchors", row["anchoring_urls"], _anchors(T.ROW_SOURCES[name]), blk,
               f"{RULING} D")
            if "uf_ifas_edis" in new_src:
                dec.append({"crop": crop, "path": blk, "decision": "hs1260-scope", "reason": HS1260_SCOPE})

        labels = set(T.NOTE_SOURCES[crop])
        new, basis = T.RECOMMENDED[crop]
        if new is None:
            op(crop, "recommended_rootstock", "value", c["recommended_rootstock"], None, NOTE_BLOCK,
               f"nulled ({RULING} E)")
            dec.append({"crop": crop, "path": "recommended_rootstock", "decision": "nulled", "reason": basis})
        else:
            if c["recommended_rootstock"] != new:
                raise SystemExit(f"STOP: {crop} recommended_rootstock is {c['recommended_rootstock']!r}, ruled unchanged")
            dec.append({"crop": crop, "path": "recommended_rootstock", "decision": "retained",
                        "reason": f"value unchanged; now FOUND on UCR-3771 ({RULING} E)"})
            _ev(ev, crop, "recommended_rootstock", "recommended_rootstock", json.dumps(new), basis)
        sents = T.NOTE[crop]
        op(crop, NOTE_BLOCK, "prose", c[NOTE_BLOCK], " ".join(s for s, _k in sents), NOTE_BLOCK, f"{RULING} E")
        for n, (s, ks) in enumerate(sents, 1):
            if not _labels_used(ks) <= labels:
                raise SystemExit(f"STOP: {crop} note sentence {n} rests on a page the note does not cite")
            _ev(ev, crop, NOTE_BLOCK, f"sentence {n}", s, ks)
        op(crop, "recommended_rootstock_note_sources", "sources", c["recommended_rootstock_note_sources"],
           _ids(T.NOTE_SOURCES[crop]), NOTE_BLOCK, f"{RULING} E")
        op(crop, "recommended_rootstock_note_anchoring_urls", "anchors", c["recommended_rootstock_note_anchoring_urls"],
           _anchors(T.NOTE_SOURCES[crop]), NOTE_BLOCK, f"{RULING} E")
        if "uf_ifas_edis" in _ids(T.NOTE_SOURCES[crop]):
            dec.append({"crop": crop, "path": NOTE_BLOCK, "decision": "hs1260-scope", "reason": HS1260_SCOPE})

        old_of = c["verification_status"]["open_findings"]
        have = {f["id"] for f in old_of}
        add = []
        for fid, summary in T.FINDINGS[crop]:
            if fid in have:
                raise SystemExit(f"STOP: {crop} already carries finding {fid}")
            add.append({"id": fid, "severity": "low", "status": "open", "blocks_launch": False,
                        "filed_in_session": SESSION, "summary": summary,
                        "basis": f"{RULING} D; PLA-612. Non-blocking: the row describes the stock."})
        op(crop, "verification_status.open_findings", "record", old_of, old_of + add, None, f"{RULING} D (PLA-612)")
        dec.append({"crop": crop, "path": "verification_status.open_findings", "decision": "record-only",
                    "reason": f"{len(add)} non-blocking PLA-612 finding(s) appended; no existing finding touched"})

    dec += [
        {"crop": "<catalog>", "path": "az_coop_ext", "decision": "source-id",
         "reason": "AZ1001 cited as az_coop_ext, the Arizona id orange-navel and grapefruit already carry (ruling C: "
                   "existing id); no id minted"},
        {"crop": "<catalog>", "path": "ucanr_santa_clara_mg", "decision": "source-id",
         "reason": "Santa Clara 'Growing Fabulous Citrus' (319461.pdf) cited as ucanr_santa_clara_mg, the chapter id "
                   "both crops already carry; uc_mg_santa_clara_citrus names a different document ('Growing Great "
                   "Citrus' web page) and is not used; no id minted"},
        {"crop": "<roster>", "path": "small yard", "decision": "clause-gloss",
         "reason": "'a pot or a small yard' maps to 31-018C 'well suited for home-use or container citrus' plus the "
                   "dwarfing effect (~75%); no cited page uses the word 'yard'. Text kept as ruled, mapping recorded."},
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
