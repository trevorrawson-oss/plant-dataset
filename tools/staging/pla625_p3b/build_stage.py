#!/usr/bin/env python3
"""build_stage -- writes ops.json, EVIDENCE.tsv and DECISIONS.tsv for promote_pla625_p3b from p3b_texts.py, against the
base canonical (d52c261a, PLA-625 citrus promote 3a). Deterministic: run it twice, get the same bytes. Derived from the
promote 2 builder: mandarin-clementine only, no new rows, no renames, no cross-crop re-keys.

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
import p3b_texts as T  # noqa: E402

TODAY = "2026-10-16"
SESSION = "pla625_promote3b_2026_10_16"
RULING = "PLA-625 promote 3b ruling (claude.ai comment b4271661, approved by Trevor, 2026-10-16)"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
NOTE_BLOCK = "recommended_rootstock_note"
ROW_FIELDS = ("name", "size_class", "mature_height_ft", "spread_ft", "container_suitable", "container_size_gallons",
              "bearing_age_years", "what_to_ask_nursery", "traits_seasoned", "traits_beginner", "sources",
              "anchoring_urls")
VALUE_FIELDS = ROW_FIELDS[1:7]
PROSE_FIELDS = ("traits_seasoned", "traits_beginner", "what_to_ask_nursery")
HS1260_SCOPE = ("HS1260 scope (promote 1 ruling A.1): Florida commercial groves; relative vigor; averaged across "
                "commercial scions; not scion-specific.")


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




def build(base):
    crops = {c["slug"]: c for c in base["crops"]}
    ops, ev, dec = [], [], []

    def op(crop, path, kind, old, new, cited_at, reason):
        ops.append({"crop": crop, "path": path, "kind": kind, "old": old, "new": new, "cited_at": cited_at,
                    "reason": reason})

    for sid, entry in T.CATALOG.items():
        if sid in base["source_catalog"]:
            raise SystemExit(f"STOP: {sid} already in source_catalog (ruling A: use it)")
        op("<catalog>", sid, "catalog", "<absent>", entry, None, f"{RULING} A: per-publication / per-document id")

    crop, c = T.MA, crops[T.MA]
    sec = f"{RULING} B"
    have = c["rootstock_options"]
    if [r["name"] for r in have] != [r["name"] for r in T.ROWS]:
        raise SystemExit(f"STOP: {crop} rows are {[r['name'] for r in have]}")
    for i, r in enumerate(T.ROWS):
        blk = f"rootstock_options[{i}]"
        labels = set(r["sources"])
        old_row = have[i]
        for f in VALUE_FIELDS:
            new, basis = r["values"][f]
            path = f"{blk}.{f}"
            if new is None:
                if old_row[f] is None:
                    dec.append({"crop": crop, "path": path, "decision": "retained", "reason": f"null kept: {basis}"})
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
            for n, (s, ks) in enumerate(sents, 1):
                if not _labels_used(ks) <= labels:
                    raise SystemExit(f"STOP: {crop} {path} sentence {n} rests on a page its row does not cite")
            op(crop, path, "prose", old_row[f], " ".join(s for s, _k in sents), blk, sec)
            for n, (s, ks) in enumerate(sents, 1):
                _ev(ev, crop, path, f"sentence {n}", s, ks)
        op(crop, f"{blk}.sources", "sources", old_row["sources"], _ids(r["sources"]), blk, sec)
        op(crop, f"{blk}.anchoring_urls", "anchors", old_row["anchoring_urls"], _anchors(r["sources"]), blk, sec)
        if "uf_ifas_hs1260" in _ids(r["sources"]):
            dec.append({"crop": crop, "path": blk, "decision": "hs1260-scope", "reason": HS1260_SCOPE})
        for sid in T.DROPPED[r["name"]]:
            if sid in old_row["sources"]:
                dec.append({"crop": crop, "path": f"{blk}.sources.{sid}", "decision": "dropped",
                            "reason": f"{RULING} A: {sid} off the {r['name']} row (names nothing the row says)"})
        if "uf_ifas_edis" in old_row["sources"]:
            dec.append({"crop": crop, "path": f"{blk}.sources.uf_ifas_edis", "decision": "rekey",
                        "reason": f"{RULING} A: CH116 under uf_ifas_edis -> uf_ifas_ch116 (this promote's scope: the rootstock "
                                  f"rows; the crop's other 23 CH116 references are PLA-728's)"})

    new, basis = T.RECOMMENDED
    op(crop, "recommended_rootstock", "value", c["recommended_rootstock"], None, NOTE_BLOCK, f"nulled ({RULING} C)")
    dec.append({"crop": crop, "path": "recommended_rootstock", "decision": "nulled", "reason": basis})
    labels = set(T.NOTE_SOURCES)
    op(crop, NOTE_BLOCK, "prose", c[NOTE_BLOCK], " ".join(s for s, _k in T.NOTE), NOTE_BLOCK, f"{RULING} C")
    for n, (s, ks) in enumerate(T.NOTE, 1):
        if not _labels_used(ks) <= labels:
            raise SystemExit(f"STOP: {crop} note sentence {n} rests on a page the note does not cite")
        _ev(ev, crop, NOTE_BLOCK, f"sentence {n}", s, ks)
    op(crop, "recommended_rootstock_note_sources", "sources", c["recommended_rootstock_note_sources"],
       _ids(T.NOTE_SOURCES), NOTE_BLOCK, f"{RULING} C")
    op(crop, "recommended_rootstock_note_anchoring_urls", "anchors", c["recommended_rootstock_note_anchoring_urls"],
       _anchors(T.NOTE_SOURCES), NOTE_BLOCK, f"{RULING} C")
    dec += [
        {"crop": "<catalog>", "path": "uf_ifas_ch116", "decision": "source-id", "reason": f"{RULING} A: minted"},
        {"crop": "<catalog>", "path": "ucce_placer_nevada_cold_damage", "decision": "source-id",
         "reason": f"{RULING} A: FakeNorton had no catalog id; minted (title read off the page)"},
        {"crop": "<catalog>", "path": "az_coop_ext", "decision": "source-id",
         "reason": "AZ1001 cited as az_coop_ext, the Arizona id (the promote 1 mapping)"},
        {"crop": "<catalog>", "path": "ucce_riverside_citrus_qa", "decision": "source-id",
         "reason": "MaukShea (178097.pdf) = ucce_riverside_citrus_qa (the promote 3a mapping)"},
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
