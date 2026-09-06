#!/usr/bin/env python3
"""promote_pla7_container_path -- PLA-7 promote A1 (spec docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md
sections 2, 3, 8 step 2). Base 72371c02.

WHAT MOVES. (1) container_notes.container_path on all 121 certified crops, one row each, null where
container_ok is not true; the 7 shells are not touched (A39 exempts uncertified shells). (2) THREE flips: cherry-sweet, cherry-sour, mulberry become container_ok true with a pot
figure and container_recommended false, on their own notes and rootstock entries (plum is HELD for
PLA-463). (3) The mechanical migration: every container_suitable_varieties[] name that EXACTLY matches
a varieties.recommended[] entry's name (case-insensitive, trimmed) gets container_suitable: true on
that entry; the bare list is left in place for the consumers that still read it. (4) Explicit variety
flags from the spec (mulberry's Dwarf Everbearing, with container_min_gallons 15). (5) gravel_layer
'not_required' -> false. (6) overwintering.applicable null -> true on container-ok crops carrying
overwintering prose. Nothing else.

WHY EACH GUARD EXISTS.
 1. ONE ROW PER CROP, PINNED COUNTS. Every crop appears exactly once; the non-null / null / tray /
    rootstock / cultivar counts are literals pinned BEFORE the first run. A count drift refuses.
 2. EVIDENCE IS PART OF THE ROW. Every rootstock or cultivar row carries a sentence that must be found
    EXACTLY ONCE across that crop's own container_notes prose. A value nobody can point at refuses.
 3. THE FLIPS ARE READ FROM THE PRE-STATE. Each flip crop must be container_ok false with a null pot
    figure before, and must carry a container_suitable rootstock entry (cherries) or a flagged
    variety (mulberry) after. A flip on a crop already true, or with no join to follow, refuses.
 4. THE GATE IS RUN HERE, NOT AT THE GAUNTLET, with presence ON: container_path_gate.all_violations
    on the post-state must be empty, and display_readiness / numeric_sanity on the flipped crops too.
 5. THE MIGRATION IS PINNED: exactly EXPECTED_FLAGS_MECHANICAL exact-name matches, and the set of
    gravel and applicable rows equals the set the pre-state says needs them (none missed, none extra).
    The flag migration is also re-derived independently from the raw container_suitable_varieties list, not solely from mechanical_flags.
 6. BLAST RADIUS AT THE LEAF: set comparisons before value comparisons; only container_notes and
    varieties.recommended may differ; within them only the declared keys; the leaf count is pinned.
    Sub-dict key sets under drainage and overwintering are compared before their values, never assumed equal to the pre-state's keys.

Usage:
    promote_pla7_container_path.py --check
    promote_pla7_container_path.py --out /path/scratch.json
    promote_pla7_container_path.py --expect-sha <sha>       # writes canonical (Task 8, on approval)
"""
import argparse, copy, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla7_container_path")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import container_path_gate as CPG  # noqa: E402  -- imported, never retyped
from display_readiness_gate import display_readiness_violations  # noqa: E402
from numeric_sanity_gate import numeric_sanity_violations  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"  # PLA-450 Option B, 4b826e4
VALUES = CPG.VALUES
EVIDENCE_VALUES = ("rootstock", "cultivar")
ROSTER = 128

# Pinned BEFORE the first run, from gen_spec_skeleton on 72371c02. The read (Task 7) may raise
# EXPECTED_ROOTSTOCK (lemon, lime) or EXPECTED_CULTIVAR; it changes these literals and the suite's
# copies together, BEFORE running, and records why in the outcome doc.
EXPECTED_ROWS = 121
EXPECTED_NON_NULL = 110
EXPECTED_NULL = 11
EXPECTED_TRAY = 8
EXPECTED_ROOTSTOCK = 8
EXPECTED_CULTIVAR = 1
EXPECTED_FLIPS = 3
EXPECTED_FLAGS_MECHANICAL = 134
EXPECTED_FLAGS_EXPLICIT = 1
EXPECTED_GRAVEL = 16
EXPECTED_APPLICABLE = 12
FLIP_KEYS = ("container_ok", "min_pot_gallons", "container_recommended")
# 121 keys + 3 flips x 3 keys + 134 + 1 flags + 1 min_gallons + 16 gravel + 12 applicable
EXPECTED_LEAVES = 121 + 9 + 134 + 1 + 1 + 16 + 12


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


def prose_leaves(cn):
    """Every string leaf under container_notes except sources/anchoring_urls."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("sources", "anchoring_urls"):
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(cn)
    return out


def _varieties(crop):
    v = crop.get("varieties")
    rec = v.get("recommended") if isinstance(v, dict) else None
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def mechanical_flags(data):
    """(slug, exact variety name) for every container_suitable_varieties name that matches an entry."""
    found = set()
    for c in data["crops"]:
        cn = c.get("container_notes") or {}
        names = {(v.get("name") or "").strip().lower(): v.get("name") for v in _varieties(c)}
        for n in cn.get("container_suitable_varieties") or []:
            key = n.strip().lower()
            if key in names:
                found.add((c["slug"], names[key]))
    return found


def check_spec_shape(spec):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    rows = spec["paths"]
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"REFUSED: {len(rows)} path rows, pinned {EXPECTED_ROWS}")
    seen = set()
    for r in rows:
        if r["crop"] in seen:
            raise SystemExit(f"REFUSED: crop {r['crop']} appears twice in paths")
        seen.add(r["crop"])
        v = r["container_path"]
        if v is not None and v not in VALUES:
            raise SystemExit(f"REFUSED: {r['crop']} container_path {v!r} not in {VALUES}")
        if v in EVIDENCE_VALUES and not (r.get("evidence") or "").strip():
            raise SystemExit(f"REFUSED: {r['crop']} is {v} without evidence")
        if v not in EVIDENCE_VALUES and r.get("evidence"):
            raise SystemExit(f"REFUSED: {r['crop']} carries evidence on a {v!r} row")
    counts = {
        "non_null": sum(1 for r in rows if r["container_path"] is not None),
        "null": sum(1 for r in rows if r["container_path"] is None),
        "tray": sum(1 for r in rows if r["container_path"] == "tray"),
        "rootstock": sum(1 for r in rows if r["container_path"] == "rootstock"),
        "cultivar": sum(1 for r in rows if r["container_path"] == "cultivar"),
    }
    pins = {"non_null": EXPECTED_NON_NULL, "null": EXPECTED_NULL, "tray": EXPECTED_TRAY,
            "rootstock": EXPECTED_ROOTSTOCK, "cultivar": EXPECTED_CULTIVAR}
    for k in pins:
        if counts[k] != pins[k]:
            raise SystemExit(f"REFUSED: {k} rows {counts[k]}, pinned {pins[k]}")
    flips = spec["flips"]
    if len(flips) != EXPECTED_FLIPS:
        raise SystemExit(f"REFUSED: {len(flips)} flips, pinned {EXPECTED_FLIPS}")
    for f in flips:
        if set(f) != {"crop"} | set(FLIP_KEYS):
            raise SystemExit(f"REFUSED: flip {f.get('crop')} keys {sorted(f)}")
        if f["container_ok"] is not True or f["container_recommended"] is not False:
            raise SystemExit(f"REFUSED: flip {f['crop']} must set container_ok true and container_recommended false")
        if not (isinstance(f["min_pot_gallons"], int) and 1 <= f["min_pot_gallons"] <= 100):
            raise SystemExit(f"REFUSED: flip {f['crop']} min_pot_gallons {f['min_pot_gallons']!r}")
    if len(spec["variety_flags"]) != EXPECTED_FLAGS_EXPLICIT:
        raise SystemExit(f"REFUSED: {len(spec['variety_flags'])} explicit variety flags, pinned {EXPECTED_FLAGS_EXPLICIT}")
    if len(spec["gravel_normalize"]) != EXPECTED_GRAVEL:
        raise SystemExit(f"REFUSED: {len(spec['gravel_normalize'])} gravel rows, pinned {EXPECTED_GRAVEL}")
    if len(spec["overwinter_applicable_true"]) != EXPECTED_APPLICABLE:
        raise SystemExit(f"REFUSED: {len(spec['overwinter_applicable_true'])} applicable rows, pinned {EXPECTED_APPLICABLE}")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    certified = {c["slug"] for c in data["crops"] if (c.get("verification_status") or {}).get("status")}
    if certified != {r["crop"] for r in spec["paths"]}:
        raise SystemExit("REFUSED: the spec's crops are not the certified roster")
    flips = {f["crop"]: f for f in spec["flips"]}
    for c in data["crops"]:
        cn = c.get("container_notes") or {}
        if "container_path" in cn:
            raise SystemExit(f"REFUSED: {c['slug']} already carries container_path")
        for v in _varieties(c):
            if "container_suitable" in v or "container_min_gallons" in v:
                raise SystemExit(f"REFUSED: {c['slug']}/{v.get('name')} already carries a variety container key")
    for r in spec["paths"]:
        c = idx[r["crop"]]
        cn = c.get("container_notes") or {}
        ok_post = cn.get("container_ok") is True or r["crop"] in flips
        if (r["container_path"] is not None) != ok_post:
            raise SystemExit(f"REFUSED: {r['crop']} row is {r['container_path']!r} but container_ok will be {ok_post}")
        if r["container_path"] in EVIDENCE_VALUES:
            hits = sum(leaf.count(r["evidence"]) for leaf in prose_leaves(cn))
            if hits != 1:
                raise SystemExit(f"REFUSED: {r['crop']} evidence found {hits} times in its container_notes prose, needs exactly 1")
        if r["container_path"] == "rootstock":
            if not any(x.get("container_suitable") is True for x in (c.get("rootstock_options") or []) if isinstance(x, dict)):
                raise SystemExit(f"REFUSED: {r['crop']} is rootstock with no container_suitable rootstock entry")
    for slug, f in flips.items():
        cn = idx[slug].get("container_notes") or {}
        if cn.get("container_ok") is not False or cn.get("min_pot_gallons") is not None:
            raise SystemExit(f"REFUSED: flip {slug} is not container_ok false with a null pot figure on the base")
    want_gravel = {c["slug"] for c in data["crops"]
                   if ((c.get("container_notes") or {}).get("drainage") or {}).get("gravel_layer") == "not_required"}
    if set(spec["gravel_normalize"]) != want_gravel:
        raise SystemExit(f"REFUSED: gravel rows differ from the base's not_required set by {sorted(set(spec['gravel_normalize']) ^ want_gravel)}")
    want_app = set()
    for c in data["crops"]:
        if c["slug"] not in certified:
            continue
        cn = c.get("container_notes") or {}
        ok_post = cn.get("container_ok") is True or c["slug"] in flips
        ow = cn.get("overwintering") or {}
        if ok_post and ow.get("applicable") is None:
            if not (ow.get("approach_seasoned") or cn.get("container_overwintering_seasoned")):
                raise SystemExit(f"REFUSED: {c['slug']} would take applicable true with no overwintering prose")
            want_app.add(c["slug"])
    if set(spec["overwinter_applicable_true"]) != want_app:
        raise SystemExit(f"REFUSED: applicable rows differ from the base by {sorted(set(spec['overwinter_applicable_true']) ^ want_app)}")
    mech = mechanical_flags(data)
    if len(mech) != EXPECTED_FLAGS_MECHANICAL:
        raise SystemExit(f"REFUSED: {len(mech)} exact-name variety matches, pinned {EXPECTED_FLAGS_MECHANICAL}")
    for vf in spec["variety_flags"]:
        c = idx[vf["crop"]]
        ent = [v for v in _varieties(c) if (v.get("name") or "") == vf["name"]]
        if len(ent) != 1:
            raise SystemExit(f"REFUSED: variety flag {vf['crop']}/{vf['name']} matches {len(ent)} entries")
        if (vf["crop"], vf["name"]) in mech:
            raise SystemExit(f"REFUSED: explicit flag {vf['crop']}/{vf['name']} duplicates a mechanical match")
    return len(spec["paths"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    idx = by_slug(post)
    for r in spec["paths"]:
        idx[r["crop"]]["container_notes"]["container_path"] = r["container_path"]
    for f in spec["flips"]:
        cn = idx[f["crop"]]["container_notes"]
        for k in FLIP_KEYS:
            cn[k] = f[k]
    for slug, name in mechanical_flags(data):
        for v in _varieties(idx[slug]):
            if (v.get("name") or "") == name:
                v["container_suitable"] = True
    for vf in spec["variety_flags"]:
        for v in _varieties(idx[vf["crop"]]):
            if (v.get("name") or "") == vf["name"]:
                v["container_suitable"] = True
                v["container_min_gallons"] = vf["container_min_gallons"]
    for slug in spec["gravel_normalize"]:
        idx[slug]["container_notes"]["drainage"]["gravel_layer"] = False
    for slug in spec["overwinter_applicable_true"]:
        idx[slug]["container_notes"]["overwintering"]["applicable"] = True
    return post


def check_post(post, spec):
    v = CPG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: container_path_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for f in spec["flips"]:
        dv = display_readiness_violations(idx[f["crop"]])
        if dv:
            raise SystemExit(f"REFUSED: display_readiness on flipped {f['crop']}: {dv}")
        nv = numeric_sanity_violations(idx[f["crop"]])
        if nv:
            raise SystemExit(f"REFUSED: numeric_sanity on flipped {f['crop']}: {nv}")


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
    flips = {f["crop"]: f for f in spec["flips"]}
    gravel = set(spec["gravel_normalize"])
    applic = set(spec["overwinter_applicable_true"])
    allowed_flags = mechanical_flags(pre) | {(vf["crop"], vf["name"]) for vf in spec["variety_flags"]}
    explicit = {(vf["crop"], vf["name"]): vf for vf in spec["variety_flags"]}
    row_crops = {r["crop"] for r in spec["paths"]}
    leaves = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if slug not in row_crops:
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: shell {slug} changed")
            continue
        if set(s) != set(g):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s:
            if k in ("container_notes", "varieties"):
                continue
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")
        scn, gcn = s["container_notes"], g["container_notes"]
        if set(gcn) - set(scn) != {"container_path"} or set(scn) - set(gcn):
            raise SystemExit(f"REFUSED: {slug} container_notes key set changed other than by adding container_path")
        leaves += 1
        for k in scn:
            if _j(scn[k]) == _j(gcn[k]):
                continue
            if k in FLIP_KEYS and slug in flips and gcn[k] == flips[slug][k]:
                leaves += 1
            elif k == "drainage" and slug in gravel:
                if set(gcn[k]) != set(scn[k]):
                    raise SystemExit(f"REFUSED: {slug} drainage key set changed")
                if {kk for kk in scn[k] if _j(scn[k][kk]) != _j(gcn[k].get(kk))} != {"gravel_layer"} or gcn[k]["gravel_layer"] is not False:
                    raise SystemExit(f"REFUSED: {slug} drainage changed other than gravel_layer -> false")
                leaves += 1
            elif k == "overwintering" and slug in applic:
                if set(gcn[k]) != set(scn[k]):
                    raise SystemExit(f"REFUSED: {slug} overwintering key set changed")
                if {kk for kk in scn[k] if _j(scn[k][kk]) != _j(gcn[k].get(kk))} != {"applicable"} or gcn[k]["applicable"] is not True:
                    raise SystemExit(f"REFUSED: {slug} overwintering changed other than applicable -> true")
                leaves += 1
            else:
                raise SystemExit(f"REFUSED: {slug} container_notes.{k} changed without a spec row")
        sv, gv = _varieties(s), _varieties(g)
        csv_pre = {n.strip().lower() for n in (scn.get("container_suitable_varieties") or []) if isinstance(n, str)}
        if _j(s.get("varieties")) != _j(g.get("varieties")):
            if len(sv) != len(gv):
                raise SystemExit(f"REFUSED: {slug} variety entry count changed")
            for a, b in zip(sv, gv):
                added = set(b) - set(a)
                if set(a) - set(b):
                    raise SystemExit(f"REFUSED: {slug}/{a.get('name')} lost a variety key")
                for k in a:
                    if _j(a[k]) != _j(b[k]):
                        raise SystemExit(f"REFUSED: {slug}/{a.get('name')} variety field {k!r} changed")
                if not added:
                    continue
                key = (slug, b.get("name") or "")
                if key not in allowed_flags:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} gained {sorted(added)} without a match or a row")
                want = {"container_suitable"} | ({"container_min_gallons"} if key in explicit else set())
                if added != want or b["container_suitable"] is not True:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} gained {sorted(added)}, expected {sorted(want)}")
                if key in explicit and b["container_min_gallons"] != explicit[key]["container_min_gallons"]:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} container_min_gallons {b['container_min_gallons']!r} is not the spec's {explicit[key]['container_min_gallons']!r}")
                if key not in explicit and (b.get("name") or "").strip().lower() not in csv_pre:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} flagged but its name is not in the pre-state container_suitable_varieties list")
                leaves += len(added)
        for b in gv:
            if (b.get("name") or "").strip().lower() in csv_pre and b.get("container_suitable") is not True:
                raise SystemExit(f"REFUSED: {slug}/{b.get('name')} matches a container_suitable_varieties name but was not flagged")
    if leaves != EXPECTED_LEAVES:
        raise SystemExit(f"REFUSED: {leaves} leaves changed, pinned {EXPECTED_LEAVES}")
    return leaves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical

    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} rows: {EXPECTED_NON_NULL} non-null / {EXPECTED_NULL} null; {EXPECTED_TRAY} tray, {EXPECTED_ROOTSTOCK} rootstock, {EXPECTED_CULTIVAR} cultivar; {EXPECTED_FLIPS} flips")
    n = check_pre_state(spec, data)
    print(f"  pre-state         {n} crops read; no key present; evidence found once; flips false->; {EXPECTED_FLAGS_MECHANICAL} exact matches; gravel/applicable sets complete")
    post = apply_to(data, spec)
    check_post(post, spec)
    print("  post gates        container_path_gate (presence ON) 0; display_readiness + numeric_sanity clean on the flips")
    leaves = verify_post(data, post, spec)
    print(f"  verify post       {leaves} leaves, nothing else")

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
