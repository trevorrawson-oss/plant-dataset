#!/usr/bin/env python3
"""promote_pla464_rootstock_array -- PLA-464 Option A (Trevor's rulings D1-D6, 2026-09-16). Base d7b33682.

WHAT MOVES (five crops: fig, pomegranate, mulberry, pawpaw, cherry-sour; the 7 shells and the other
116 certified crops byte-identical).
 (1) RETIRE the six rootstock_options[] rows that are not rootstocks: four propagation modes (the
     own-root rows on fig, pomegranate, mulberry, pawpaw) and two genetic-dwarf cultivars (mulberry,
     cherry-sour). Every surviving entry is byte-identical and keeps its order.
 (2) FOLD one crop-specific sentence from the retired row into recommended_rootstock_note on fig,
     mulberry and pawpaw. pomegranate's and cherry-sour's row prose is already carried by the crop
     note, the container notes, or the PLA-463 not_applicable framing copy: nothing is folded there.
 (3) SIBLING STRINGS: fig's recommended_rootstock (it named the retired row) -> null; mulberry's ->
     the surviving row's name.
 (4) RECORDS in verification_status: one field_additions entry per fold-in carrying the row's sources;
     one open_findings entry each on fig and pomegranate (min_pot_gallons now unanchored, PLA-533),
     mulberry (15 gal proven unanchored by a raw read of its ncsu_ext page; KEPT because a
     container_ok crop must carry a pot figure; PLA-533) and cherry-sour (North Star / Meteor figures
     recorded, routed to PLA-7 Plan B).
 (5) mulberry's min_pot_gallons and Dwarf Everbearing's container_min_gallons stay 15, ASSERTED
     unchanged: that is a decision (D5 as amended), not an omission.

WHY EACH GUARD EXISTS.
 1. THE POPULATION IS MEASURED TWICE. The spec names six rows. An independent NAME NET over every
    rootstock_options[] entry on the roster must flag exactly those six and nothing else. A spec row
    the net does not flag refuses; a flagged row the spec forgot refuses.
 2. EACH RETIRED ROW IS PINNED BY CROP, INDEX AND EXACT NAME. An index pointing at another name refuses.
 3. A FOLD-IN IS NEW TEXT: 0 occurrences in the crop's note before, exactly 1 after, and the post note
    must equal the pre note + one space + the sentence, nothing else. No em dash, no `--`.
 4. EVERY SOURCE ID in a fold-in or a record must exist in source_catalog, and a fold-in's
    field_additions record must carry the same sources.
 5. THE GATES RUN HERE with presence on: container_path_gate on the whole post-state,
    display_readiness and numeric_sanity on the five crops.
 6. BLAST RADIUS AT THE LEAF, SET BEFORE VALUE: top-level, roster, crop-level and verification_status
    key sets compared before any value; every crop outside the five byte-identical; inside the five
    only the declared keys differ; rootstock_options post == pre minus the retired indices, entry by
    entry; the two verification_status lists are append-only behind a byte-identical prefix. The kept
    gallons are pinned on the BASE (check_pre_state); container_notes and varieties are outside the
    declared keys, so the generic loop refuses any move.

Usage:
    promote_pla464_rootstock_array.py --check
    promote_pla464_rootstock_array.py --out /path/scratch.json
    promote_pla464_rootstock_array.py --expect-sha <sha>       # writes canonical, on approval only
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla464_rootstock_array")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import container_path_gate as CPG  # noqa: E402  -- imported, never retyped
from display_readiness_gate import display_readiness_violations  # noqa: E402
from numeric_sanity_gate import numeric_sanity_violations  # noqa: E402

BASE_SHA = "d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798"  # PLA-7 promote A1, 4ade2d4
ROSTER = 128
CONCEPTS = ("own_root", "genetic_dwarf")
# The independent net: a rootstock_options[] NAME that names a propagation mode or a cultivar.
NAME_NET = re.compile(r"own[- ]roots?\b|genetic dwarf|ungrafted", re.I)
RECORD_KEYS = ("id", "severity", "status", "blocks_launch", "filed_in_session", "summary", "resolution_note", "deferred_to")
FA_KEYS = ("field", "date", "sources", "note")
SESSION = "pla464_2026-09-16"

# Pinned BEFORE the first run, from the 2026-09-16 measurement on d7b33682.
EXPECTED_RETIRE = 6
EXPECTED_FOLDINS = 3
EXPECTED_RR = 2
EXPECTED_FA = 3
EXPECTED_FINDINGS = 4
EXPECTED_CROPS = 5
MULBERRY_GALLONS = 15
# 6 rows + 3 notes + 2 sibling strings + 3 field_additions + 4 open_findings
EXPECTED_CHANGES = 6 + 3 + 2 + 3 + 4


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def load_canonical(path=None):
    p = path or CANON
    with open(p, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


def staged():
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f)


def _rows(crop):
    r = crop.get("rootstock_options")
    return [x for x in r if isinstance(x, dict)] if isinstance(r, list) else []


def _varieties(crop):
    v = crop.get("varieties")
    rec = v.get("recommended") if isinstance(v, dict) else None
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def net_population(data):
    """(slug, index, name) for every rootstock_options[] entry whose NAME the net flags, roster-wide."""
    return {(c["slug"], i, e.get("name") or "") for c in data["crops"]
            for i, e in enumerate(_rows(c)) if NAME_NET.search(e.get("name") or "")}


def _bad_copy(s):
    return "—" in s or "--" in s


def check_spec_shape(spec):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    rows = spec["retire"]
    if len(rows) != EXPECTED_RETIRE:
        raise SystemExit(f"REFUSED: {len(rows)} retire rows, pinned {EXPECTED_RETIRE}")
    seen = set()
    for r in rows:
        key = (r["crop"], r["index"])
        if key in seen:
            raise SystemExit(f"REFUSED: retire row {key} appears twice")
        seen.add(key)
        if r["concept"] not in CONCEPTS:
            raise SystemExit(f"REFUSED: {r['crop']}[{r['index']}] concept {r['concept']!r} not in {CONCEPTS}")
        if not (r.get("name") or "").strip():
            raise SystemExit(f"REFUSED: {r['crop']}[{r['index']}] retire row has no name")
    retire_crops = {r["crop"] for r in rows}
    if len(retire_crops) != EXPECTED_CROPS:
        raise SystemExit(f"REFUSED: retire rows span {len(retire_crops)} crops, pinned {EXPECTED_CROPS}")
    folds = spec["note_foldins"]
    if len(folds) != EXPECTED_FOLDINS:
        raise SystemExit(f"REFUSED: {len(folds)} fold-ins, pinned {EXPECTED_FOLDINS}")
    fold_crops = [f["crop"] for f in folds]
    if len(set(fold_crops)) != len(fold_crops) or not set(fold_crops) <= retire_crops:
        raise SystemExit("REFUSED: fold-ins must name distinct crops that carry a retired row")
    for f in folds:
        s = f.get("sentence") or ""
        if not s.strip() or not s.endswith("."):
            raise SystemExit(f"REFUSED: fold-in on {f['crop']} is empty or does not end with a period")
        if _bad_copy(s):
            raise SystemExit(f"REFUSED: fold-in on {f['crop']} carries an em dash or `--` (consumer copy)")
        if not f.get("sources"):
            raise SystemExit(f"REFUSED: fold-in on {f['crop']} carries no sources")
    rr = spec["recommended_rootstock"]
    if len(rr) != EXPECTED_RR:
        raise SystemExit(f"REFUSED: {len(rr)} recommended_rootstock rows, pinned {EXPECTED_RR}")
    for r in rr:
        if r["crop"] not in retire_crops or r["from"] == r["to"]:
            raise SystemExit(f"REFUSED: recommended_rootstock row {r['crop']} is not a change on a retire crop")
    mg = spec["mulberry_gallons"]
    if mg.get("kept") is not True or mg.get("min_pot_gallons") != MULBERRY_GALLONS or mg.get("container_min_gallons") != MULBERRY_GALLONS:
        raise SystemExit("REFUSED: mulberry_gallons must be kept at the pinned figure (D5 as amended)")
    fas = spec["field_additions"]
    if len(fas) != EXPECTED_FA:
        raise SystemExit(f"REFUSED: {len(fas)} field_additions, pinned {EXPECTED_FA}")
    by_fold = {f["crop"]: f for f in folds}
    for fa in fas:
        e = fa["entry"]
        if set(e) != set(FA_KEYS) or e["field"] != "recommended_rootstock_note":
            raise SystemExit(f"REFUSED: field_additions on {fa['crop']} has the wrong shape")
        if fa["crop"] not in by_fold or list(e["sources"]) != list(by_fold[fa["crop"]]["sources"]):
            raise SystemExit(f"REFUSED: field_additions on {fa['crop']} does not carry its fold-in's sources")
    ofs = spec["open_findings"]
    if len(ofs) != EXPECTED_FINDINGS:
        raise SystemExit(f"REFUSED: {len(ofs)} open_findings, pinned {EXPECTED_FINDINGS}")
    ids = set()
    for of in ofs:
        e = of["entry"]
        if set(e) != set(RECORD_KEYS):
            raise SystemExit(f"REFUSED: open_findings on {of['crop']} has the wrong shape")
        if e["status"] != "deferred" or e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:
            raise SystemExit(f"REFUSED: open_findings {e['id']} must be deferred, non-blocking, filed in {SESSION}")
        if e["id"] in ids or of["crop"] not in retire_crops:
            raise SystemExit(f"REFUSED: open_findings {e['id']} duplicated or on a crop with no retired row")
        ids.add(e["id"])
    want_expected = {"retire": EXPECTED_RETIRE, "foldins": EXPECTED_FOLDINS, "recommended_rootstock": EXPECTED_RR,
                     "field_additions": EXPECTED_FA, "open_findings": EXPECTED_FINDINGS, "crops": EXPECTED_CROPS,
                     "mulberry_gallons": MULBERRY_GALLONS}
    if spec["expected"] != want_expected:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    catalog = set((data.get("source_catalog") or {}).keys())
    want = {(r["crop"], r["index"], r["name"]) for r in spec["retire"]}
    for r in spec["retire"]:
        c = idx.get(r["crop"])
        if c is None:
            raise SystemExit(f"REFUSED: retire crop {r['crop']} is not on the roster")
        rows = _rows(c)
        if r["index"] >= len(rows) or (rows[r["index"]].get("name") or "") != r["name"]:
            raise SystemExit(f"REFUSED: {r['crop']}[{r['index']}] is not {r['name']!r} on the base")
    got = net_population(data)
    if got != want:
        raise SystemExit(f"REFUSED: the name net flags {sorted(got ^ want)} differently from the spec")
    for f in spec["note_foldins"]:
        c = idx[f["crop"]]
        note = c.get("recommended_rootstock_note")
        if not isinstance(note, str) or not note.strip():
            raise SystemExit(f"REFUSED: {f['crop']} has no recommended_rootstock_note to fold into")
        if note.count(f["sentence"]) != 0:
            raise SystemExit(f"REFUSED: {f['crop']} note already carries the fold-in sentence")
        for s in f["sources"]:
            if s not in catalog:
                raise SystemExit(f"REFUSED: fold-in source {s!r} on {f['crop']} is not in source_catalog")
    for r in spec["recommended_rootstock"]:
        if idx[r["crop"]].get("recommended_rootstock") != r["from"]:
            raise SystemExit(f"REFUSED: {r['crop']} recommended_rootstock is not {r['from']!r} on the base")
    mg = spec["mulberry_gallons"]
    m = idx[mg["crop"]]
    if (m.get("container_notes") or {}).get("min_pot_gallons") != mg["min_pot_gallons"]:
        raise SystemExit("REFUSED: mulberry min_pot_gallons is not the pinned figure on the base")
    dv = [v for v in _varieties(m) if v.get("name") == mg["variety"]]
    if len(dv) != 1 or dv[0].get("container_min_gallons") != mg["container_min_gallons"]:
        raise SystemExit("REFUSED: Dwarf Everbearing container_min_gallons is not the pinned figure on the base")
    for fa in spec["field_additions"]:
        vs = idx[fa["crop"]].get("verification_status") or {}
        if not isinstance(vs.get("field_additions"), list):
            raise SystemExit(f"REFUSED: {fa['crop']} verification_status.field_additions is not a list")
        if any(x.get("field") == "recommended_rootstock_note" for x in vs["field_additions"]):
            raise SystemExit(f"REFUSED: {fa['crop']} already records a recommended_rootstock_note addition")
    for of in spec["open_findings"]:
        vs = idx[of["crop"]].get("verification_status") or {}
        if not isinstance(vs.get("open_findings"), list):
            raise SystemExit(f"REFUSED: {of['crop']} verification_status.open_findings is not a list")
        if any(x.get("id") == of["entry"]["id"] for x in vs["open_findings"]):
            raise SystemExit(f"REFUSED: {of['crop']} already carries finding {of['entry']['id']}")
    return len(spec["retire"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    idx = by_slug(post)
    drop = {}
    for r in spec["retire"]:
        drop.setdefault(r["crop"], set()).add(r["index"])
    for slug, idxs in drop.items():
        idx[slug]["rootstock_options"] = [e for i, e in enumerate(idx[slug]["rootstock_options"]) if i not in idxs]
    for f in spec["note_foldins"]:
        idx[f["crop"]]["recommended_rootstock_note"] = idx[f["crop"]]["recommended_rootstock_note"] + " " + f["sentence"]
    for r in spec["recommended_rootstock"]:
        idx[r["crop"]]["recommended_rootstock"] = r["to"]
    for fa in spec["field_additions"]:
        idx[fa["crop"]]["verification_status"]["field_additions"].append(copy.deepcopy(fa["entry"]))
    for of in spec["open_findings"]:
        idx[of["crop"]]["verification_status"]["open_findings"].append(copy.deepcopy(of["entry"]))
    return post


def check_post(post, spec):
    v = CPG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: container_path_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for slug in sorted({r["crop"] for r in spec["retire"]}):
        dv = display_readiness_violations(idx[slug])
        if dv:
            raise SystemExit(f"REFUSED: display_readiness on {slug}: {dv}")
        nv = numeric_sanity_violations(idx[slug])
        if nv:
            raise SystemExit(f"REFUSED: numeric_sanity on {slug}: {nv}")


def _j(x):
    return json.dumps(x, sort_keys=True)


def verify_post(pre, post, spec):
    """SET COMPARISON BEFORE VALUE COMPARISON."""
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k != "crops" and _j(pre[k]) != _j(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop roster changed")
    touched = {r["crop"] for r in spec["retire"]}
    drop = {}
    for r in spec["retire"]:
        drop.setdefault(r["crop"], set()).add(r["index"])
    folds = {f["crop"]: f for f in spec["note_foldins"]}
    rr = {r["crop"]: r for r in spec["recommended_rootstock"]}
    fas = {fa["crop"]: fa["entry"] for fa in spec["field_additions"]}
    ofs = {of["crop"]: of["entry"] for of in spec["open_findings"]}
    changes = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if slug not in touched:
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: untouched crop {slug} changed")
            continue
        if set(s) != set(g):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s:
            if k in ("rootstock_options", "recommended_rootstock_note", "recommended_rootstock", "verification_status"):
                continue
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the declared keys")
        # (1) rootstock_options: post == pre minus the retired indices, entry by entry
        kept = [e for i, e in enumerate(s["rootstock_options"]) if i not in drop[slug]]
        if len(g["rootstock_options"]) != len(kept):
            raise SystemExit(f"REFUSED: {slug} rootstock_options has {len(g['rootstock_options'])} entries, expected {len(kept)}")
        for a, b in zip(kept, g["rootstock_options"]):
            if _j(a) != _j(b):
                raise SystemExit(f"REFUSED: {slug} surviving rootstock entry {a.get('name')!r} changed")
        changes += len(drop[slug])
        # (2) the note
        if slug in folds:
            want = s["recommended_rootstock_note"] + " " + folds[slug]["sentence"]
            if g["recommended_rootstock_note"] != want:
                raise SystemExit(f"REFUSED: {slug} recommended_rootstock_note is not the pre note plus the fold-in")
            changes += 1
        elif _j(s["recommended_rootstock_note"]) != _j(g["recommended_rootstock_note"]):
            raise SystemExit(f"REFUSED: {slug} recommended_rootstock_note changed without a fold-in row")
        # (3) the sibling string
        if slug in rr:
            if g["recommended_rootstock"] != rr[slug]["to"]:
                raise SystemExit(f"REFUSED: {slug} recommended_rootstock is not the spec's {rr[slug]['to']!r}")
            changes += 1
        elif _j(s["recommended_rootstock"]) != _j(g["recommended_rootstock"]):
            raise SystemExit(f"REFUSED: {slug} recommended_rootstock changed without a spec row")
        # (4) verification_status: key sets first, then append-only lists behind a byte-identical prefix
        sv, gv = s["verification_status"], g["verification_status"]
        if set(sv) != set(gv):
            raise SystemExit(f"REFUSED: {slug} verification_status key set changed")
        for k in sv:
            if k in ("field_additions", "open_findings"):
                continue
            if _j(sv[k]) != _j(gv[k]):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")
        for k, table in (("field_additions", fas), ("open_findings", ofs)):
            a, b = sv[k], gv[k]
            if not isinstance(a, list) or not isinstance(b, list):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} is not a list on both sides")
            if _j(b[:len(a)]) != _j(a):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} prefix is not byte-identical")
            tail = b[len(a):]
            want_tail = [table[slug]] if slug in table else []
            if _j(tail) != _j(want_tail):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} appended {len(tail)} entries, expected {len(want_tail)} matching the spec")
            changes += len(tail)
        # (5) mulberry's gallons: container_notes and varieties are OUTSIDE the declared keys, so any move
        #     is refused by the generic loop above; the pin is asserted on the base in check_pre_state.
    # The change count is informational here: every per-key check above implies it, so a refusal on it
    # could never fire in isolation and would read as coverage.
    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical
    if args.out and os.path.abspath(args.out) == os.path.abspath(path or CANON):
        sys.exit("REFUSED: --out may not target the canonical; use --expect-sha for the write")

    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} retire rows on {EXPECTED_CROPS} crops; {EXPECTED_FOLDINS} fold-ins; {EXPECTED_RR} sibling strings; {EXPECTED_FA} field_additions; {EXPECTED_FINDINGS} findings; mulberry kept at {MULBERRY_GALLONS}")
    n = check_pre_state(spec, data)
    print(f"  pre-state         {n} rows found at their index by exact name; the name net flags exactly those {n} roster-wide; fold-ins absent; siblings and gallons as pinned; records absent; sources in catalog")
    post = apply_to(data, spec)
    check_post(post, spec)
    print("  post gates        container_path_gate (presence ON) 0; display_readiness + numeric_sanity clean on the five crops")
    changes = verify_post(data, post, spec)
    print(f"  verify post       {changes} changes, nothing else")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.out:
        with open(args.out, "wb") as f:
            f.write(blob)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
        return 0
    if args.check:
        print("  --check: nothing written")
        return 0
    if not args.expect_sha:
        sys.exit("REFUSED: writing canonical requires --expect-sha (the gauntleted scratch SHA)")
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
