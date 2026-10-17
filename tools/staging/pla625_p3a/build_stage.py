#!/usr/bin/env python3
"""build_stage -- writes ops.json, EVIDENCE.tsv and DECISIONS.tsv for promote_pla625_p3a from p3a_texts.py, against the
base canonical (ef1a4d35, PLA-625 citrus promote 2). Deterministic: run it twice, get the same bytes.

Every op's `old` is read from the base. A prose op carries `subs`: the ruled (old, new) substring pairs, each of whose old
occurs exactly once; the promote re-derives new from old + subs (touched-leaf rule) and refuses a mismatch.

THE CITATION RULE (ruling, "Citation rule"): a touched string whose block already has a non-empty `sources` list gets each
new clause's source added to that block; a block that is uncited (A62-waived: watering on orange-navel / grapefruit,
soil_prep, start_method) or has no sources field (year_one_notes_*) is NOT newly cited: its changed clauses get evidence
rows only (cited_at null).

Usage: build_stage.py [--canonical PATH]
"""
import argparse, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, HERE)
sys.path.insert(0, TOOLS)
import p3a_texts as T  # noqa: E402
from cited_promote_common import resolve  # noqa: E402

TODAY = "2026-10-16"
SESSION = "pla625_promote3a_2026_10_16"
RULING = "PLA-625 promote 3a ruling (claude.ai comment 356a763f, approved by Trevor, 2026-10-16)"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
CITE_KEYS = ("sources", "anchoring_urls")


def get(node, path):
    for s in resolve(node, path):
        node = node[s]
    return node


def block_of(path):
    """The citation block a touched string belongs to (by path shape)."""
    if path.startswith("companions."):
        return "companions"
    if path.startswith("watering."):
        return "watering"
    m = re.match(r"(diseases\[id=[^\]]+\])\.", path)
    if m:
        return m.group(1)
    if path.startswith("tips_by_stage.planting[0]."):
        return "tips_by_stage.planting[0]"
    return None   # soil_prep_*, year_one_notes_*, start_method.*: crop-level or uncited


def is_cited(crop, blk):
    if blk is None:
        return False
    node = get(crop, blk)
    return isinstance(node, dict) and isinstance(node.get("sources"), list) and bool(node["sources"])


def build(base):
    crops = {c["slug"]: c for c in base["crops"]}
    ops, ev, dec = [], [], []
    add_ids = {}   # (crop, blk) -> [labels in order]

    def op(crop, path, kind, old, new, cited_at, reason, subs=None):
        o = {"crop": crop, "path": path, "kind": kind, "old": old, "new": new, "cited_at": cited_at, "reason": reason}
        o["subs"] = subs
        ops.append(o)

    for sid, entry in T.CATALOG.items():
        if sid in base["source_catalog"]:
            raise SystemExit(f"STOP: {sid} already in source_catalog")
        op("<catalog>", sid, "catalog", "<absent>", entry, None, f"{RULING}: HS141 has no id; minted per-publication")

    for (slug, path), subs in sorted(T.EDITS.items()):
        crop = crops[slug]
        old = get(crop, path)
        if not isinstance(old, str):
            raise SystemExit(f"STOP: {slug} {path} is not a string")
        new = old
        pairs = []
        for o_sub, n_sub, keys in subs:
            if o_sub is None:   # a ruled whole-string replacement
                o_sub = new
            if new.count(o_sub) != 1:
                raise SystemExit(f"STOP: {slug} {path}: ruled text occurs {new.count(o_sub)} times: {o_sub[:70]!r}")
            new = new.replace(o_sub, n_sub)
            pairs.append([o_sub, n_sub])
        blk = block_of(path)
        cited = is_cited(crop, blk)
        op(slug, path, "prose", old, new, blk if cited else None, RULING, pairs)
        for n, (o_sub, n_sub, keys) in enumerate(subs, 1):
            if not keys:
                if n_sub:
                    raise SystemExit(f"STOP: {slug} {path} sub {n}: new text with no quote keys")
                dec.append({"crop": slug, "path": path, "decision": "deleted",
                            "reason": f"ruled deletion, no new clause: {(o_sub or '')[:120]}"})
                continue
            for k in keys:
                lab, quote = T.QUOTES[k]
                sid, url, sha = T.SOURCES[lab]
                ev.append({"crop": slug, "entry_id": path, "field": f"sub {n} ({k})", "value": n_sub,
                           "source_id": sid, "url": url, "sha256": sha, "quote": quote})
                if cited:
                    lst = add_ids.setdefault((slug, blk), [])
                    if lab not in lst:
                        lst.append(lab)
        if not cited:
            dec.append({"crop": slug, "path": path, "decision": "evidence-only",
                        "reason": f"block {blk or '(none)'} is uncited or has no sources field: not newly cited "
                                  f"(ruling citation rule); evidence rows for the changed clauses only"})

    # citation blocks: additions, the ruled CG009 removals, the mechanical re-keys, the D repoint
    touched = set(add_ids) | {(c, b) for c, b, _s in T.ANCHOR_REMOVALS} | {(c, b) for c, b, _f, _t in T.REKEYS} \
        | {(c, b) for c, b, _s, _u in T.REPOINTS}
    for slug, blk in sorted(touched):
        node = get(crops[slug], blk)
        srcs, anc = list(node["sources"]), {k: dict(v) for k, v in node["anchoring_urls"].items()}
        new_s, new_a = list(srcs), {k: dict(v) for k, v in anc.items()}
        for c, b, frm, to in T.REKEYS:
            if (c, b) == (slug, blk):
                if frm not in new_s or to in new_s:
                    raise SystemExit(f"STOP: re-key {slug} {blk} {frm}->{to}: state is {new_s}")
                new_s = [to if s == frm else s for s in new_s]
                new_a = {(to if k == frm else k): v for k, v in new_a.items()}
                if to == "uf_ifas_cg009":
                    new_a[to] = {"url": new_a[to]["url"], "verified": TODAY, "note": T.CG009_NOTE}
                dec.append({"crop": slug, "path": f"{blk}.anchoring_urls.{to}", "decision": "rekey",
                            "reason": f"{frm} -> {to} at the same url {new_a[to]['url']} (one id per document per block, "
                                      f"so the block can carry the ruled source; promote 2 ruling A.1 pattern)"})
        for c, b, sid in T.ANCHOR_REMOVALS:
            if (c, b) == (slug, blk):
                if "CG009" not in new_a[sid]["url"]:
                    raise SystemExit(f"STOP: {slug} {blk} {sid} is not the CG009 anchor")
                new_s.remove(sid)
                del new_a[sid]
                dec.append({"crop": slug, "path": f"{blk}.anchoring_urls.{sid}", "decision": "cg009-off",
                            "reason": f"{RULING} C4: CG009 anchor removed"})
        for c, b, sid, url in T.REPOINTS:
            if (c, b) == (slug, blk):
                new_a[sid] = {"url": url, "verified": TODAY}
                dec.append({"crop": slug, "path": f"{blk}.anchoring_urls.{sid}", "decision": "repoint",
                            "reason": f"{RULING} D: the cached home-and-landscape page"})
        for lab in add_ids.get((slug, blk), []):
            sid, url, _sha = T.SOURCES[lab]
            if sid in new_a and new_a[sid]["url"] != url:
                raise SystemExit(f"STOP: {slug} {blk}: {sid} already anchored at {new_a[sid]['url']}, the ruled source is "
                                 f"{url} (one url per id per block)")
            if sid not in new_s:
                new_s.append(sid)
            if sid not in new_a:
                new_a[sid] = {"url": url, "verified": TODAY}
        if new_s != srcs:
            op(slug, f"{blk}.sources", "sources", srcs, new_s, blk, RULING)
        if new_a != anc:
            op(slug, f"{blk}.anchoring_urls", "anchors", anc, new_a, blk, RULING)

    for slug, blk, idx, method in T.LADDER_REMOVE:
        lad = get(crops[slug], f"{blk}.control_ladder")
        if lad[idx]["method"] != method:
            raise SystemExit(f"STOP: {slug} {blk} rung {idx} is {lad[idx]['method']}, not {method}")
        op(slug, f"{blk}.control_ladder", "ladder", lad, lad[:idx] + lad[idx + 1:], blk, f"{RULING} D: rung removed")
        dec.append({"crop": slug, "path": f"{blk}.control_ladder[{idx}]", "decision": "rung-removed",
                    "reason": f"{method}: mulch-for-splash ABSENT on every fetched brown-rot source (ruling 4)"})

    for slug, fid, note in T.FINDING_NOTE:
        of = crops[slug]["verification_status"]["open_findings"]
        hits = [i for i, f in enumerate(of) if f["id"] == fid]
        if len(hits) != 1 or of[hits[0]]["status"] != "open" or "progress_note" in of[hits[0]]:
            raise SystemExit(f"STOP: {slug} {fid} is not one open finding without a progress note")
        new_of = json.loads(json.dumps(of))
        new_of[hits[0]]["progress_note"] = note
        op(slug, "verification_status.open_findings", "record", of, new_of, None, f"{RULING} E, as amended (5dde3208)")
        dec.append({"crop": slug, "path": "verification_status.open_findings", "decision": "record-only",
                    "reason": f"{fid}: progress note appended, status unchanged (stays open past 3a); no other finding "
                              f"touched"})
    for slug, fid in T.FINDING_RESOLVE:
        of = crops[slug]["verification_status"]["open_findings"]
        hits = [i for i, f in enumerate(of) if f["id"] == fid]
        if len(hits) != 1 or of[hits[0]]["status"] != "open":
            raise SystemExit(f"STOP: {slug} {fid} is not one open finding")
        new_of = json.loads(json.dumps(of))
        f = new_of[hits[0]]
        f["status"] = "resolved"
        f["resolved_in_session"] = SESSION
        f["resolution_note"] = T.RESOLUTION_NOTE
        op(slug, "verification_status.open_findings", "record", of, new_of, None, f"{RULING} E")
        dec.append({"crop": slug, "path": "verification_status.open_findings", "decision": "record-only",
                    "reason": f"{fid} resolved per its close condition (independent clause check); no other finding touched"})
    dec.append({"crop": "<roster>", "path": "uf_ifas_cg009", "decision": "cg009-retained",
                "reason": "independent read (stop report 00ee5ba1): 11 clauses only CG009 supports stay cited to it: "
                          "lemon + orange-navel cause_seasoned, cause_beginner, control_ladder[0].note_beginner, "
                          "control_ladder[0].note_seasoned (young-tree overwatering: 'overwatering, especially of young "
                          "trees, promotes buildup of phytophthora populations in the soil'); orange-navel "
                          "prevention_seasoned, control_ladder[1].note_beginner / note_seasoned (Carrizo: 'swingle "
                          "citrumelo and carrizo citrange that are normally tolerant'); quotes verified in c2bc36bb"})
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
