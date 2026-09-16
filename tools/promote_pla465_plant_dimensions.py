#!/usr/bin/env python3
"""promote_pla465_plant_dimensions -- PLA-465 plant dimensions (spec
docs/superpowers/specs/2026-09-16-pla465-plant-dimensions-field-shape.md; register row 30). Base a98b6cfd.

WHAT MOVES. On every one of the 121 CERTIFIED crops, three new crop-level keys: mature_height_ft,
mature_spread_ft, footprint_inches. The AUTHORED crops (the tree and woody archetypes, from the T1
reads staged in spec.json) take a [lo, hi] height, a [lo, hi] spread or null, and one
verification_status.field_additions[] entry {field: "plant_dimensions", date, sources, note} carrying
the read (institution, URL, verbatim sentence, byte count, sha256). Every other certified crop takes
null on all three (not yet authored). footprint_inches is null on every crop (PLA-429's slot). The 7
uncertified shells are not touched (A39/A59 exempt them by status). Nothing else.

WHY EACH GUARD EXISTS.
 1. AN AUTHORED CROP IS WOODY, CERTIFIED, AND ON THE ROSTER. The spec's crop list is checked against the
    base's archetype and status; a herbaceous or shell crop in the authored list refuses (R1: define for
    121, author the 30).
 2. EVERY AUTHORED VALUE PASSES THE GATE BEFORE IT IS WRITTEN: plant_dimensions_gate.shape_violations
    (imported, never retyped; the pair rules live there and nowhere else) and numeric_sanity_gate on a
    synthetic crop carrying the spec row, so a malformed pair or an absurd figure never reaches apply_to.
 3. PROVENANCE IS PART OF THE ROW: field == "plant_dimensions", date pinned, sources non-empty and in
    source_catalog, the note names the URL and quotes the page. A value nobody can point at refuses.
 4. THE BASE CARRIES NONE OF THE KEYS and no plant_dimensions field_additions entry, on any crop.
 5. THE GATES RUN HERE with presence ON: plant_dimensions_gate.all_violations(presence=True) on the
    post-state must be empty, numeric_sanity and display_readiness clean on every authored crop.
 6. BLAST RADIUS AT THE LEAF, SET BEFORE VALUE: top-level, roster, crop-level and verification_status key
    sets compared before any value; every shell byte-identical; on each certified crop the key set grows
    by exactly the three keys and nothing else differs but field_additions (append-only behind a
    byte-identical prefix); the written values are compared to their OWN spec row; every count pinned.

Usage:
    promote_pla465_plant_dimensions.py --check
    promote_pla465_plant_dimensions.py --out /path/scratch.json
    promote_pla465_plant_dimensions.py --expect-sha <sha>       # writes canonical, on approval only
"""
import argparse, copy, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla465_plant_dimensions")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import plant_dimensions_gate as PDG  # noqa: E402  -- imported, never retyped
from numeric_sanity_gate import numeric_sanity_violations  # noqa: E402
from display_readiness_gate import display_readiness_violations  # noqa: E402

BASE_SHA = "a98b6cfdfd7c5ffdcccdb222ceaa141fdca79e0ed674f991c0dcb396c2534412"  # PLA-464 Option A, a2796ae
ROSTER = 128
CERTIFIED = "verified_gs_arc"
WOODY = ("deciduous_fruit_tree", "evergreen_fruit_tree", "berries_woody", "woody_ornamental")
FIELDS = PDG.FIELDS
FA_KEYS = ("field", "date", "sources", "note")
FA_FIELD = PDG.PROVENANCE_FIELD
FA_DATE = "2026-09-16"

# Pinned BEFORE the first run. EXPECTED_AUTHORED is the count of crops whose T1 read returned a height;
# it is set from the staged reads and recorded in the outcome doc before any run, then never moved.
EXPECTED_KEYS = 121
EXPECTED_AUTHORED = 16  # pinned 2026-09-16 from the staged reads; never moved after the first run
EXPECTED_SHELLS = 7


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


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _synthetic(row, base_crop):
    """A copy of the base crop carrying the spec row's values, for running the gates BEFORE the write."""
    c = copy.deepcopy(base_crop)
    c["mature_height_ft"] = row["mature_height_ft"]
    c["mature_spread_ft"] = row["mature_spread_ft"]
    c["footprint_inches"] = None
    c["verification_status"]["field_additions"] = list(c["verification_status"].get("field_additions") or []) + [row["field_addition"]]
    return c


def check_spec_shape(spec, expected_authored):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    rows = spec["authored"]
    if expected_authored is None or len(rows) != expected_authored:
        raise SystemExit(f"REFUSED: {len(rows)} authored rows, pinned {expected_authored}")
    seen = set()
    for r in rows:
        if r["crop"] in seen:
            raise SystemExit(f"REFUSED: crop {r['crop']} appears twice in authored")
        seen.add(r["crop"])
        if set(r) != {"crop", "mature_height_ft", "mature_spread_ft", "field_addition"}:
            raise SystemExit(f"REFUSED: authored row {r['crop']} has keys {sorted(r)}")
        if r["mature_height_ft"] is None:
            raise SystemExit(f"REFUSED: {r['crop']} is an authored row with no mature_height_ft")
        fa = r["field_addition"]
        if set(fa) != set(FA_KEYS) or fa["field"] != FA_FIELD:
            raise SystemExit(f"REFUSED: {r['crop']} field_addition has the wrong shape")
        if fa["date"] != FA_DATE:
            raise SystemExit(f"REFUSED: {r['crop']} field_addition date {fa['date']!r} is not {FA_DATE}")
        if not fa["sources"]:
            raise SystemExit(f"REFUSED: {r['crop']} field_addition carries no sources")
        if not (fa["note"] or "").strip() or "http" not in fa["note"]:
            raise SystemExit(f"REFUSED: {r['crop']} field_addition note does not name its page")
    if spec["expected"] != {"keys": EXPECTED_KEYS, "authored": expected_authored, "null": EXPECTED_KEYS - expected_authored, "shells": EXPECTED_SHELLS}:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    certified = [c for c in data["crops"] if _certified(c)]
    if len(certified) != EXPECTED_KEYS:
        raise SystemExit(f"REFUSED: {len(certified)} certified crops, pinned {EXPECTED_KEYS}")
    catalog = set((data.get("source_catalog") or {}).keys())
    for c in data["crops"]:
        for f in FIELDS:
            if f in c:
                raise SystemExit(f"REFUSED: {c['slug']} already carries {f}")
        fa = (c.get("verification_status") or {}).get("field_additions")
        if _certified(c) and not isinstance(fa, list):
            raise SystemExit(f"REFUSED: {c['slug']} verification_status.field_additions is not a list")
        if any(isinstance(x, dict) and x.get("field") == FA_FIELD for x in (fa or [])):
            raise SystemExit(f"REFUSED: {c['slug']} already records a {FA_FIELD} addition")
    for r in spec["authored"]:
        c = idx.get(r["crop"])
        if c is None:
            raise SystemExit(f"REFUSED: authored crop {r['crop']} is not on the roster")
        if not _certified(c):
            raise SystemExit(f"REFUSED: authored crop {r['crop']} is not certified")
        if c.get("archetype") not in WOODY:
            raise SystemExit(f"REFUSED: authored crop {r['crop']} archetype {c.get('archetype')!r} is not tree or woody (R1)")
        for s in r["field_addition"]["sources"]:
            if s not in catalog:
                raise SystemExit(f"REFUSED: source {s!r} on {r['crop']} is not in source_catalog")
        syn = _synthetic(r, c)
        v = PDG.shape_violations(syn)
        if v:
            raise SystemExit(f"REFUSED: {r['crop']} spec row fails plant_dimensions_gate: {v}")
        nv = numeric_sanity_violations(syn)
        if nv:
            raise SystemExit(f"REFUSED: {r['crop']} spec row fails numeric_sanity: {nv}")
    return len(spec["authored"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    idx = by_slug(post)
    rows = {r["crop"]: r for r in spec["authored"]}
    for c in post["crops"]:
        if not _certified(c):
            continue
        r = rows.get(c["slug"])
        c["mature_height_ft"] = r["mature_height_ft"] if r else None
        c["mature_spread_ft"] = r["mature_spread_ft"] if r else None
        c["footprint_inches"] = None
        if r:
            c["verification_status"]["field_additions"].append(copy.deepcopy(r["field_addition"]))
    return post


def check_post(post, spec):
    v = PDG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: plant_dimensions_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for r in spec["authored"]:
        nv = numeric_sanity_violations(idx[r["crop"]])
        if nv:
            raise SystemExit(f"REFUSED: numeric_sanity on {r['crop']}: {nv}")
        dv = display_readiness_violations(idx[r["crop"]])
        if dv:
            raise SystemExit(f"REFUSED: display_readiness on {r['crop']}: {dv}")


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
    rows = {r["crop"]: r for r in spec["authored"]}
    keys = authored = nulls = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if not _certified(s):
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: shell {slug} changed")
            continue
        if set(g) != set(s) | set(FIELDS):
            raise SystemExit(f"REFUSED: {slug} crop-level key set is not the base's plus the three keys")
        for k in s:
            if k == "verification_status":
                continue
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the declared keys")
        keys += 1
        if g["footprint_inches"] is not None:
            raise SystemExit(f"REFUSED: {slug} footprint_inches is not null (nobody authors it yet)")
        r = rows.get(slug)
        if r:
            if _j(g["mature_height_ft"]) != _j(r["mature_height_ft"]) or _j(g["mature_spread_ft"]) != _j(r["mature_spread_ft"]):
                raise SystemExit(f"REFUSED: {slug} written dimensions are not the spec row's")
            authored += 1
        else:
            if g["mature_height_ft"] is not None or g["mature_spread_ft"] is not None:
                raise SystemExit(f"REFUSED: {slug} carries a dimension with no authored row")
            nulls += 1
        sv, gv = s["verification_status"], g["verification_status"]
        if set(sv) != set(gv):
            raise SystemExit(f"REFUSED: {slug} verification_status key set changed")
        for k in sv:
            if k != "field_additions" and _j(sv[k]) != _j(gv[k]):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")
        a, b = sv["field_additions"], gv["field_additions"]
        if _j(b[:len(a)]) != _j(a):
            raise SystemExit(f"REFUSED: {slug} field_additions prefix is not byte-identical")
        want_tail = [r["field_addition"]] if r else []
        if _j(b[len(a):]) != _j(want_tail):
            raise SystemExit(f"REFUSED: {slug} field_additions appended {len(b) - len(a)} entries, expected {len(want_tail)} matching the spec")
    # keys == EXPECTED_KEYS and authored/nulls == the spec's split are IMPLIED by the per-crop checks
    # above (every certified crop must carry the three keys; a value without a row refuses), so a refusal
    # on the totals could never fire in isolation and would read as coverage. Informational only.
    return keys, authored, nulls


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
    n = check_spec_shape(spec, EXPECTED_AUTHORED)
    print(f"  spec shape        {n} authored rows; {EXPECTED_KEYS} keys; {EXPECTED_KEYS - n} null; {EXPECTED_SHELLS} shells untouched")
    n = check_pre_state(spec, data)
    print(f"  pre-state         no key on any crop; {n} authored crops certified + woody, sources in catalog, every row passes the gate and the bounds")
    post = apply_to(data, spec)
    check_post(post, spec)
    print("  post gates        plant_dimensions_gate (presence ON) 0; numeric_sanity + display_readiness clean on the authored crops")
    keys, authored, nulls = verify_post(data, post, spec)
    print(f"  verify post       {keys} crops took the keys: {authored} authored, {nulls} null; nothing else")

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
