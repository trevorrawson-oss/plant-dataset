"""PLA-750: build the promote stage (ops.json, EVIDENCE.tsv, DECISIONS.tsv) from p750_texts against the canonical.

Every `old` is READ from the canonical (never typed); every evidence quote is checked against its hashed page
through cited_promote_common.cached_quote before a row is written. A miss refuses.

Usage: python3 tools/staging/pla750/build_stage.py [--canonical PATH] [--evidence DIR]
"""
import argparse, copy, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, TOOLS)
sys.path.insert(0, HERE)
from cited_promote_common import EVIDENCE_COLS, cached_quote, manifest, resolve  # noqa: E402
import p750_texts as T  # noqa: E402

ABSENT = "<absent>"
CATALOG = "<catalog>"


def value(crop, path):
    conc = resolve(crop, path)
    node = crop
    for s in conc[:-1]:
        node = node[s]
    k = conc[-1]
    if isinstance(node, dict) and k not in node:
        return ABSENT
    return node[k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", default=os.path.join(os.path.dirname(TOOLS), "crops_data_final.json"))
    ap.add_argument("--evidence", default=os.path.join(TOOLS, ".evidence_cache"))
    a = ap.parse_args()
    data = json.load(open(a.canonical, encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    man = manifest(a.evidence)
    url_sha = {}
    for sha, urls in man.items():
        for u in urls:
            url_sha.setdefault(u, []).append(sha)
    ops, ev, dec, tc = [], [], [], {}

    def evidence(crop, entry, field, val, sid, url, quote):
        shas = url_sha.get(url, [])
        if not shas:
            raise SystemExit(f"REFUSED: {crop} {entry}: {url} has no hashed bytes")
        last = None
        for sha in shas:
            row = dict(zip(EVIDENCE_COLS, (crop, entry, field, val, sid, url, sha, quote)))
            try:
                cached_quote(row, man, a.evidence, tc, f"{crop} {entry}")
                ev.append(row)
                return
            except Exception as e:  # noqa: BLE001  (Refused)
                last = e
        raise SystemExit(f"REFUSED: {last}")

    def op(crop, path, kind, old, new, reason, subs=None, cited_at=None):
        ops.append({"crop": crop, "path": path, "kind": kind, "old": old, "new": new, "reason": reason,
                    "subs": subs, "cited_at": cited_at})

    for sid, entry in T.MINTS.items():
        if sid in data["source_catalog"]:
            raise SystemExit(f"REFUSED: {sid} already in source_catalog")
        op(CATALOG, sid, "catalog", ABSENT, entry, "PLA-750 D6 / catalog mint, ruling 47a09951")
        evidence(CATALOG, sid, "catalog", sid, sid, entry["url"], {
            "sare_necphm_arugula": "Optimum germination is 75°.",
            "steiner_2010_arugula": "possess satisfactory germination (more than 94%)",
            "eberle_2014_calendula": "calendula seed should be sown in the field only if forecasted soil conditions",
            "ucanr_pub7243": "Green onions are plant- ed during the fall, spring, and summer",
            "tamu_celery_crop_sheet": "Average high temperature above 75°F in month preceding harvest",
        }[sid])
    # the new field (30) + pause flips (20)
    data_cat = dict(data["source_catalog"], **T.MINTS)
    for slug, f in T.FIELDS.items():
        c = by[slug]
        if value(c, "sowing_heat_ceiling") is not ABSENT and value(c, "sowing_heat_ceiling") != ABSENT:
            raise SystemExit(f"REFUSED: {slug} already carries sowing_heat_ceiling")
        for sid in f["sources"]:
            if sid not in data_cat:
                raise SystemExit(f"REFUSED: {slug}: {sid} not in the catalog (nor minted)")
        op(slug, "sowing_heat_ceiling", "field", ABSENT, f, "PLA-750 D1/P1 register #35, ruled table row")
        pause = value(c, "succession_policy.pause_in_heat")
        if pause is not True:
            raise SystemExit(f"REFUSED: {slug} pause_in_heat is {pause!r} on the base, not true")
        if f["temp_f"] is None:
            op(slug, "succession_policy.pause_in_heat", "pause", True, False,
               "PLA-750 ruling 47a09951: no sourced sowing hold")
    for slug, (o, n) in T.ENUMS.items():
        got = value(by[slug], "heat_effect")
        if got != o or by[slug].get("heat_threshold_f") is not None:
            raise SystemExit(f"REFUSED: {slug} heat_effect {got!r} / threshold {by[slug].get('heat_threshold_f')!r}")
        op(slug, "heat_effect", "enum", o, n, "PLA-750 D5 + P5: stress is real, no sourced number")
    # prose
    for crop, path, subs, cited_at, rows, decision in T.PROSE:
        old = value(by[crop], path)
        if not isinstance(old, str):
            raise SystemExit(f"REFUSED: {crop} {path} is not a string on the base")
        new = old
        for o, n in subs:
            if new.count(o) != 1:
                raise SystemExit(f"REFUSED: {crop} {path}: {o[:50]!r} occurs {new.count(o)} times")
            new = new.replace(o, n)
        op(crop, path, "prose", old, new, "PLA-750 ruled edit", subs=[list(s) for s in subs], cited_at=cited_at)
        for sid, url, q in rows:
            nsub = next(n for _o, n in subs if n)
            evidence(crop, path, "prose", nsub, sid, url, q)
        if decision:
            dec.append({"crop": crop, "path": path, "decision": decision,
                        "reason": "unsupported clause struck (PLA-750 live-data finding)" if decision == "struck"
                        else "start_method has no citation block; the clause rests on its EVIDENCE row"})
    # citation additions
    for crop, blk, add in T.CITES:
        node = value(by[crop], blk)
        srcs = list(node.get("sources") or [])
        anc = copy.deepcopy(node.get("anchoring_urls") or {})
        for sid, url in add.items():
            if sid in srcs and anc.get(sid, {}).get("url") == url:
                raise SystemExit(f"REFUSED: {crop} {blk} already cites {sid} at {url}")
            if sid in anc and anc[sid].get("url") != url:
                raise SystemExit(f"REFUSED: {crop} {blk}: {sid} is anchored at another url ({anc[sid]['url']})")
            if sid not in srcs:
                srcs.append(sid)
            anc[sid] = {"url": url, "verified": T.V}
        op(crop, blk + ".sources", "sources", node.get("sources", ABSENT), srcs, "PLA-750 citation for a ruled claim",
           cited_at=blk)
        op(crop, blk + ".anchoring_urls", "anchors", node.get("anchoring_urls", ABSENT), anc,
           "PLA-750 citation for a ruled claim", cited_at=blk)
    for crop, blk, sid, url, q in T.CITE_EVIDENCE:
        evidence(crop, blk, "cite", sid, sid, url, q)
    # new tips
    for crop, stage, t, rows in T.TIP_ADDS:
        path = f"tips_by_stage.{stage}"
        old = value(by[crop], path)
        if old is ABSENT or old == ABSENT or not isinstance(old, list):
            raise SystemExit(f"REFUSED: {crop} {path} is not a tip list on the base")
        ids = {x.get("tip_id") for tips in by[crop]["tips_by_stage"].values() for x in tips or []}
        if t["tip_id"] in ids:
            raise SystemExit(f"REFUSED: {crop} already has a tip {t['tip_id']}")
        op(crop, path, "tip_add", old, old + [t], "PLA-750 D4 stage tip" if stage != "established"
           else "PLA-750 live-data fix: cilantro's 75°F moved to a bolting tip")
        for sid, url, q in rows:
            evidence(crop, f"{path}[tip_id={t['tip_id']}]", "tip", t["tip_id"], sid, url, q)
    # struck triggers
    for crop, k, v, why in T.TRIGGER_DROPS:
        old = value(by[crop], "weather_triggers")
        hits = [x for x in old if x.get(k) == v]
        if len(hits) != 1:
            raise SystemExit(f"REFUSED: {crop} weather_triggers[{k}={v}] matches {len(hits)}")
        op(crop, "weather_triggers", "trigger_drop", old, [x for x in old if x is not hits[0]],
           f"PLA-750 live-data finding: {why}")
        dec.append({"crop": crop, "path": f"weather_triggers[{k}={v}]", "decision": "struck", "reason": why})

    json.dump(ops, open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EVIDENCE_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(ev)
    with open(os.path.join(HERE, "DECISIONS.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["crop", "path", "decision", "reason"], delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(dec)
    kinds = {}
    for o in ops:
        kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
    print(f"stage: {len(ops)} ops {kinds}; {len(ev)} evidence rows (all in hashed bytes); {len(dec)} decisions; "
          f"{len({o['crop'] for o in ops if o['crop'] != CATALOG})} crops")


if __name__ == "__main__":
    main()
