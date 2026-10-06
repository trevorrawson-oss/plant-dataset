#!/usr/bin/env python3
"""Build the PLA-673 / PLA-674 glossary promote stage (ops.json, EVIDENCE.tsv, DECISIONS.tsv) from the ruled inputs.

Ruled inputs (nothing here authors a value):
  ../pla673_674_prep/definitions.py     the approved definitions, verbatim, each sentence with its packet quotes
                                        (claude.ai, approved by Trevor 2026-10-05, round 2)
  ../pla673_674_prep/build_packets.py   packets 1/2 (the quote numbering the definitions cite) and their pages
  ../pla673_674_prep/glossary_match.json the ruled `match` lists (MATCH SHAPE ruling)
  ../pla673_674_prep/catalog_mints.json  the four part-A mints (D4, D6)
  CHILD_MINTS below                      the six document-level child ids (STOP 2, option (a) widened)
  ../housekeeping60/phase_c/EVIDENCE.tsv the watermelon soil_prep evidence (PLA-674 backfill)

It also computes POST_SHA by an INDEPENDENT minimal apply (no promote code), printed for the suite to pin.
Run from anywhere: python3 tools/staging/pla673_glossary/build_stage.py
"""
import copy, csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.path.dirname(TOOLS)
PREP = os.path.join(TOOLS, "staging", "pla673_674_prep")
sys.path.insert(0, TOOLS)
sys.path.insert(0, PREP)
import build_packets as bp  # noqa: E402
from definitions import DEFINITIONS, SUPPLEMENT  # noqa: E402

BASE_SHA = "350eda387fbed55464b16688a3bdc3263214b7c20631da98c7bbcb79f1d487c7"
TODAY = "2026-10-05"
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")
DECISION_COLS = ("crop", "path", "decision", "reason")
ENTRY_KEYS = ("term", "definition_beginner", "definition_seasoned", "sources", "anchoring_urls", "field_additions", "match")
SIBLINGS = ("soil_prep_sources", "soil_prep_anchoring_urls")

# packet page key (build_packets.SRC) -> the glossary's document-level source id
DOC_ID = {
    "purdue": "purdue_ext_ho8wa", "csu": "csu_ext_cucurbits_07609", "b577": "uga_b577_home_gardening",
    "ncsu": "ncsu_ext_handbook_vegetable", "c1206": "uga_c1206_homegrown_pumpkins", "nmsu": "nmsu_ext_cr457",
    "umn_cuc": "umn_ext_cucumbers", "umn_pot": "umn_ext_potatoes", "umn_carrot": "umn_ext_carrots_parsnips",
    "umn_leek": "umn_ext_leeks", "usu_leek": "usu_ext_leeks", "clem_grits": "clemson_hgic_homegrown_grits",
}

CHILD_MINTS = {
    "umn_ext_potatoes": {
        "id": "umn_ext_potatoes", "name": "UMN Extension -- Growing potatoes in home gardens",
        "title": "Growing potatoes in home gardens", "publisher": "University of Minnesota Extension",
        "url": "https://extension.umn.edu/vegetables/growing-potatoes", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UMN Extension's potato page: hilling (hill soil up around plants once shoots emerge; start when stems are about a foot tall and once or twice more; six to eight inches of soil in total), why (shallow tubers turn green in light; more buried stem, more stolons), the shallow-trench alternative, and the hill as the mound dug at harvest. A document-scoped child of umn_ext.",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2 ruling: glossary entries cite document-level ids only). Raw bytes sha256 fccae103bdc2e2ac8b08f9d82b7669a364f77fccf99adcee19e7a936da692773 (117,871 bytes), an existing MANIFEST row; the url also 301s to the garden-and-home path (same bytes). Title read off the page. Crop-level anchors keep umn_ext (no re-keying)."},
    "umn_ext_carrots_parsnips": {
        "id": "umn_ext_carrots_parsnips", "name": "UMN Extension -- Growing carrots and parsnips in home gardens",
        "title": "Growing carrots and parsnips in home gardens", "publisher": "University of Minnesota Extension",
        "url": "https://extension.umn.edu/vegetables/growing-carrots-and-parsnips", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UMN Extension's carrot and parsnip page. For hilling it states only the CARROT case: 'some carrot varieties will push the tops of the roots up out of the soil. hilling soil around these plants will keep the roots from turning green.' It does not state parsnip hilling. A document-scoped child of umn_ext.",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2). Raw bytes sha256 14d9f7109dab4994e6818b4a0bc62bbdd853a76a47174bf35bedae019dbc287b (117,952 bytes), an existing MANIFEST row. Title read off the page. Crop-level anchors keep umn_ext."},
    "umn_ext_leeks": {
        "id": "umn_ext_leeks", "name": "UMN Extension -- Growing leeks in home gardens",
        "title": "Growing leeks in home gardens", "publisher": "University of Minnesota Extension",
        "url": "https://extension.umn.edu/vegetables/growing-leeks", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UMN Extension's leek page: hill the plants for a longer white shaft, or plant in a furrow and fill it in; hilling as mounding compost or soil around plants set at normal soil level, several times a season. A document-scoped child of umn_ext.",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2). Raw bytes sha256 153697ad9e43f7f5e3e320d7d394d1c19d88a21f56645c579a734bdbfefc22ef (104,533 bytes), an existing MANIFEST row. Title read off the page. Crop-level anchors keep umn_ext."},
    "umn_ext_cucumbers": {
        "id": "umn_ext_cucumbers", "name": "UMN Extension -- Growing cucumbers in home gardens",
        "title": "Growing cucumbers in home gardens", "publisher": "University of Minnesota Extension",
        "url": "https://extension.umn.edu/vegetables/growing-cucumbers", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "UMN Extension's cucumber page: a 'hill' of three or four seeds sown close together; five to six feet between hills; bush types two to three feet between rows or hills. A document-scoped child of umn_ext.",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2; replaces umn_ext in glossary.hill.sources). Raw bytes sha256 5645fa79d76fc167dc3329cf6366c203cfd8a84a89e0d0f08e131fdf8db5202a (121,678 bytes), an existing MANIFEST row. Title read off the page. Crop-level anchors keep umn_ext."},
    "usu_ext_leeks": {
        "id": "usu_ext_leeks", "name": "USU Extension -- How to Grow Leeks in Your Garden",
        "title": "How to Grow Leeks in Your Garden", "publisher": "Utah State University Extension",
        "url": "https://extension.usu.edu/yardandgarden/research/leeks-in-the-garden", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "USU's leek page: hill soil around seeded plants 2-3 times, adding 2-3 inches of banked soil, for taller growth and a longer blanched edible stem; hilling up soil plus mulch to store leeks in the garden in mild areas. A document-scoped child of usu_ext.",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2; replaces usu_ext in glossary.hilling.sources). Raw bytes sha256 ce41cd51a494ba5271a93eb16fc4bfb6f9b95d403980e39f01608ec8bbedb61c (46,899 bytes), an existing MANIFEST row. Title read off the page. Crop-level anchors keep usu_ext."},
    "clemson_hgic_homegrown_grits": {
        "id": "clemson_hgic_homegrown_grits", "name": "Clemson HGIC -- Homegrown Grits (Cory Tanner, 2020)",
        "title": "Homegrown Grits", "publisher": "Clemson University Home & Garden Information Center",
        "url": "https://hgic.clemson.edu/homegrown-grits/", "source_class": "university_extension",
        "trust_tier": "high", "accessed": "2026-10", "tier": "T1",
        "citable_for": "Clemson HGIC post (Cory Tanner, 3 Sep 2020) on heirloom dent corn for grits: plants up to 15 feet; smaller plantings may blow over in a storm unless spaced a little further apart (2 ft) and hilled with soil. A document-scoped child of clemson_hgic. (The page's 'HGIC 1308' is its cross-reference to the sweet corn factsheet, not its own number.)",
        "_admission_provenance": "Minted 2026-10-05 for PLA-673 (STOP 2; replaces clemson_hgic in glossary.hilling.sources). PINNED to MANIFEST sha256 65d1d7cb557bc6f76e8d62ce2704aa880f09f04a0548e0f0b7b43dfc061d4aea (137,753 bytes; the bytes the packet quoted). A SECOND MANIFEST row carries the same url: d533df5cbb9d5dda81b79de3cb4146c6b356374f96b5ed6f535c5d323bf697e8 (137,753 bytes, Safari UA + Sec-Fetch headers, PLA-10 promote 1 session 2); its norm_text differs from 65d1d7cb (per-request content), and the quoted sentence is in both. Crop-level anchors keep clemson_hgic."},
}
PINNED_SHA = {"clemson_hgic_homegrown_grits": "65d1d7cb557bc6f76e8d62ce2704aa880f09f04a0548e0f0b7b43dfc061d4aea"}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def compact(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)


def quote(ref, packet):
    """(page key, quote text) for a packet quote number or a supplement key."""
    if isinstance(ref, str):
        return SUPPLEMENT[ref]
    src, _sense, q = (bp.P1 if packet == "P1" else bp.P2)[ref - 1]
    return src, q


def page(src_key, sid):
    url = bp.SRC[src_key][1]
    sha = PINNED_SHA.get(sid) or bp.full_sha(bp.SRC[src_key][0])
    return url, sha


def build():
    raw = open(os.path.join(REPO, "crops_data_final.json"), "rb").read()
    if sha256(raw) != BASE_SHA:
        raise SystemExit(f"canonical is {sha256(raw)[:8]}, expected {BASE_SHA[:8]}")
    pre = json.loads(raw)
    mints = json.load(open(os.path.join(PREP, "catalog_mints.json"), encoding="utf-8"))
    mints = {k: v for k, v in mints.items() if not k.startswith("_")}
    mints.update(CHILD_MINTS)
    match = json.load(open(os.path.join(PREP, "glossary_match.json"), encoding="utf-8"))
    ops, ev, dec = [], [], []

    # ---- catalog mints (10)
    for sid, entry in mints.items():
        if sid in pre["source_catalog"]:
            raise SystemExit(f"{sid} is already in the catalog")
        ops.append({"crop": "<catalog>", "path": sid, "kind": "catalog", "old": "<absent>", "new": entry,
                    "cited_at": None, "reason": "PLA-673 glossary: document-level source id (D4/D6/STOP 2 rulings)"})

    # ---- glossary entries (2) + their evidence rows
    for tid, t in DEFINITIONS.items():
        anchors = {}
        regs = {}
        for reg in ("definition_beginner", "definition_seasoned"):
            sents = []
            for i, (sentence, packet, refs) in enumerate(t[reg], 1):
                sents.append(sentence)
                for ref in refs:
                    src, q = quote(ref, packet if not isinstance(ref, str) else None)
                    sid = DOC_ID[src]
                    url, sha = page(src, sid)
                    anchors.setdefault(sid, url)
                    ev.append({"crop": "<glossary>", "entry_id": f"{tid}.{reg}[{i}]", "field": "sentence",
                               "value": sentence, "source_id": sid, "url": url, "sha256": sha, "quote": q})
            regs[reg] = " ".join(sents)
        if set(anchors) != set(t["sources"]):
            raise SystemExit(f"{tid}: quoted ids {sorted(anchors)} != ruled sources {sorted(t['sources'])}")
        sources = list(t["sources"])
        rows = [r for r in ev if r["crop"] == "<glossary>" and r["entry_id"].startswith(tid + ".")]
        fa = []
        for reg in ("definition_beginner", "definition_seasoned"):
            used = [s for s in sources if any(r["source_id"] == s and r["entry_id"].startswith(f"{tid}.{reg}") for r in rows)]
            pages = "; ".join(f"{s} {anchors[s]} (sha256 {page_sha(rows, s)})" for s in used)
            n_rows = sum(1 for r in rows if r["entry_id"].startswith(f"{tid}.{reg}"))
            fa.append({"field": f"glossary.{tid}.{reg}", "date": TODAY, "sources": used,
                       "note": (f"PLA-673 glossary.{tid}.{reg}: {len(t[reg])} sentences authored in claude.ai and approved "
                                f"by Trevor 2026-10-05 (round 2), each mapped to verbatim quotes from hashed pages "
                                f"({n_rows} rows in tools/staging/pla673_glossary/EVIDENCE.tsv; packets: Linear 'PLA-673 "
                                f"packet 1: hill' and 'packet 2: hilling'). Pages: {pages}.")})
        entry = {"term": t["term"], "definition_beginner": regs["definition_beginner"],
                 "definition_seasoned": regs["definition_seasoned"], "sources": sources,
                 "anchoring_urls": {s: {"url": anchors[s], "verified": TODAY} for s in sources},
                 "field_additions": fa, "match": match[tid]["match"]}
        assert tuple(entry) == ENTRY_KEYS
        ops.append({"crop": "<glossary>", "path": tid, "kind": "glossary", "old": "<absent>", "new": entry,
                    "cited_at": None, "reason": "PLA-673 glossary entry (definitions approved verbatim 2026-10-05)"})

    # ---- PLA-674 siblings on ALL 128 crop records (D14), null except watermelon's backfill
    phase_c = [r for r in csv.DictReader(open(os.path.join(TOOLS, "staging", "housekeeping60", "phase_c", "EVIDENCE.tsv"),
                                              encoding="utf-8", newline=""), delimiter="\t")
               if r["crop"] == "watermelon" and r["entry_id"] in ("soil_prep_seasoned", "soil_prep_beginner")]
    if len(phase_c) != 14:
        raise SystemExit(f"expected 14 Phase C watermelon soil_prep rows, found {len(phase_c)}")
    wm_sources, wm_anchors = [], {}
    for r in phase_c:
        if r["source_id"] not in wm_anchors:
            wm_sources.append(r["source_id"])
            wm_anchors[r["source_id"]] = {"url": r["url"], "verified": TODAY}
        ev.append({"crop": "watermelon", "entry_id": "soil_prep_sources", "field": f"{r['entry_id']}:{r['field']}",
                   "value": r["value"], "source_id": r["source_id"], "url": r["url"], "sha256": r["sha256"],
                   "quote": r["quote"]})
    for c in pre["crops"]:
        for key in SIBLINGS:
            if key in c:
                raise SystemExit(f"{c['slug']} already carries {key}")
            new = None
            if c["slug"] == "watermelon":
                new = wm_sources if key == "soil_prep_sources" else wm_anchors
            ops.append({"crop": c["slug"], "path": key, "kind": "sibling", "old": "<absent>", "new": copy.deepcopy(new),
                        "cited_at": None, "reason": "PLA-674 citation sibling (D13 null = not assessed; D14 all 128 records)"})

    # ---- decisions
    dec += [
        {"crop": "<roster>", "path": "soil_prep_sources", "decision": "null-not-assessed",
         "reason": "D13 (Trevor 2026-10-05): null = not assessed (PLA-581); [] would read as assessed, no sources"},
        {"crop": "<roster>", "path": "soil_prep_anchoring_urls", "decision": "null-not-assessed",
         "reason": "D13: null = not assessed; astro 23df2d5 accepts null or a non-empty source-id map"},
        {"crop": "<roster>", "path": "soil_prep_sources", "decision": "all-128-records",
         "reason": "D14 (Trevor 2026-10-05): all 128 crop records incl. the 7 uncertified shells (field-inventory rule)"},
        {"crop": "<roster>", "path": "soil_prep_sources", "decision": "known-divergence",
         "reason": "PLA-581 critical_warnings and PLA-10 planting_layout left the 7 shells key-absent; this key does not "
                   "(D14). Backlog issue filed to backfill those keys null on shells for uniformity"},
        {"crop": "<roster>", "path": "soil_prep_sources", "decision": "placement",
         "reason": "D15: immediately after the crop's last soil_prep_* key (the mature_dimensions_* precedent); "
                   "appended at the end on the 88 records with no soil_prep prose"},
        {"crop": "watermelon", "path": "soil_prep_sources", "decision": "backfill",
         "reason": "PLA-674 scope 3: the 14 Housekeeping 60 Phase C EVIDENCE rows for soil_prep_*, re-proven against "
                   "hashed bytes; closes Phase C's record-only step"},
        {"crop": "<glossary>", "path": "hill", "decision": "definitions-verbatim",
         "reason": "approved by Trevor 2026-10-05 (round 2: beginner 2 -> 2+2b, seasoned +2b); 16 sentences"},
        {"crop": "<glossary>", "path": "hilling", "decision": "definitions-verbatim",
         "reason": "approved by Trevor 2026-10-05 (round 2: beginner 4 -> 4+4b, seasoned 7 replaced); 18 sentences"},
        {"crop": "<glossary>", "path": "hill", "decision": "document-level-ids",
         "reason": "STOP 2 option (a) widened: umn_ext -> umn_ext_cucumbers"},
        {"crop": "<glossary>", "path": "hilling", "decision": "document-level-ids",
         "reason": "STOP 2 option (a) widened: umn_ext -> umn_ext_potatoes / _carrots_parsnips / _leeks; usu_ext -> "
                   "usu_ext_leeks; clemson_hgic -> clemson_hgic_homegrown_grits"},
        {"crop": "<glossary>", "path": "hill", "decision": "match-pepper-held",
         "reason": "D8: pepper/eggplant 'beds or hills' tagged none (unsupported claim, re-author pending part B2)"},
        {"crop": "<catalog>", "path": "clemson_hgic_homegrown_grits", "decision": "pinned-sha",
         "reason": "pinned to 65d1d7cb (the quoted bytes); d533df5c, a second MANIFEST row for the url, recorded"},
        {"crop": "<catalog>", "path": "uga_b577_home_gardening", "decision": "one-document-one-id",
         "reason": "D6: uga_b577 is the planting-chart PDF (a9ed2655); 7 crop anchors carrying the bulletin url under "
                   "uga_b577 are NOT re-keyed here (PLA-686)"},
    ]
    return pre, ops, ev, dec


def page_sha(rows, sid):
    shas = {r["sha256"] for r in rows if r["source_id"] == sid}
    assert len(shas) == 1, (sid, shas)
    return shas.pop()


def minimal_apply(pre, ops):
    """INDEPENDENT of the promote: set each op's new value; siblings after the last soil_prep_* key."""
    post = copy.deepcopy(pre)
    for op in ops:
        if op["kind"] == "catalog":
            post["source_catalog"][op["path"]] = copy.deepcopy(op["new"])
        elif op["kind"] == "glossary":
            post.setdefault("glossary", {})[op["path"]] = copy.deepcopy(op["new"])
    for c in post["crops"]:
        mine = [op for op in ops if op["crop"] == c["slug"]]
        if not mine:
            continue
        items = list(c.items())
        last = max([i for i, (k, _v) in enumerate(items) if k in ("soil_prep_beginner", "soil_prep_seasoned")], default=len(items) - 1)
        new = items[:last + 1] + [(op["path"], copy.deepcopy(op["new"])) for op in mine] + items[last + 1:]
        c.clear()
        c.update(new)
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
    print(f"independent minimal apply: {BASE_SHA[:8]} -> {sha256(blob)}")


if __name__ == "__main__":
    main()
