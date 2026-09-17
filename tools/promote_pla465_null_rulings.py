#!/usr/bin/env python3
"""promote_pla465_null_rulings -- PLA-465 promote 2: the twelve woody crops whose plant dimensions stay null,
each with Trevor's recorded reason and routing (rulings of 2026-09-17). Base a7f234ce.

WHAT MOVES. On eleven crops, one or two open_findings entries APPENDED to verification_status.open_findings
(twelve entries; pear-asian carries two: the height gap and the recommended-rootstock question, filed on its
own). On plum, ONE dated addendum appended to the SUMMARY of the existing finding
plum_self_fertile_boolean_european_default (the original text byte-identical as a prefix, every other field
untouched). No dimension value, no other key, no other crop.

WHY EACH GUARD EXISTS.
 1. THE RULING IS ABOUT NULLS. Every target crop must be certified and carry null on all three dimension
    keys on the base; a ruling recorded on a crop that carries a value refuses.
 2. RECORDS ARE PINNED BY SHAPE AND VOCABULARY: the eight record keys, blocks_launch false, filed_in_session
    pinned, status in {accepted, deferred} with deferred_to non-null iff deferred, ids unique and absent on
    the base, and the summary + resolution_note free of em dashes (`--` is allowed in a backend record and appears in quoted page text).
 3. THE ADDENDUM TARGETS ONE EXISTING FINDING BY ID AND BY ITS EXACT ORIGINAL SUMMARY: a finding that has
    moved since the spec was written refuses, and the suffix must open with the dated ADDENDUM marker.
 4. THE GATES RUN HERE: plant_dimensions_gate (presence ON) and the launch-blocker rule on every touched crop.
 5. BLAST RADIUS AT THE LEAF, SET BEFORE VALUE: top-level, roster, crop-level and verification_status key
    sets compared before any value; every crop outside the twelve byte-identical; inside them only
    verification_status.open_findings differs, append-only behind a byte-identical prefix, except plum's
    one entry, which must equal the original with the suffix appended and nothing else changed.

Usage:
    promote_pla465_null_rulings.py --check | --out PATH | --expect-sha SHA
"""
import argparse, copy, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla465_null_rulings")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import plant_dimensions_gate as PDG  # noqa: E402

BASE_SHA = "a7f234ce449c6d74b4f1be2398bb808cfe29bebf9a1f7cc51efdcaea56246c93"  # PLA-465 promote 1, 6659f62
ROSTER = 128
CERTIFIED = "verified_gs_arc"
SESSION = "pla465_2026-09-17"
RECORD_KEYS = ("id", "severity", "status", "blocks_launch", "filed_in_session", "summary", "resolution_note", "deferred_to")
STATUSES = ("accepted", "deferred")
ADDENDUM_MARK = " [ADDENDUM 2026-09-17, PLA-465:"
EXPECTED_APPENDS = 12
EXPECTED_CROPS = 12
EXPECTED_ADDENDA = 1


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


def _bad_copy(s):
    """verification_status records are BACKEND text, not consumer copy: `--` is allowed there (quoted page
    text carries it), the em dash is not."""
    return "—" in s


def check_spec_shape(spec):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    rows = spec["appends"]
    if len(rows) != EXPECTED_APPENDS:
        raise SystemExit(f"REFUSED: {len(rows)} appends, pinned {EXPECTED_APPENDS}")
    ids = set()
    for r in rows:
        e = r["entry"]
        if set(e) != set(RECORD_KEYS):
            raise SystemExit(f"REFUSED: record on {r['crop']} has keys {sorted(e)}")
        if e["id"] in ids:
            raise SystemExit(f"REFUSED: record id {e['id']} appears twice")
        ids.add(e["id"])
        if e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:
            raise SystemExit(f"REFUSED: {e['id']} must be non-blocking and filed in {SESSION}")
        if e["status"] not in STATUSES:
            raise SystemExit(f"REFUSED: {e['id']} status {e['status']!r} not in {STATUSES}")
        if (e["status"] == "deferred") != (e["deferred_to"] is not None):
            raise SystemExit(f"REFUSED: {e['id']} deferred_to must be set iff status is deferred")
        if not (e["summary"] or "").strip() or not (e["resolution_note"] or "").strip():
            raise SystemExit(f"REFUSED: {e['id']} has an empty summary or resolution_note")
        if _bad_copy(e["summary"]) or _bad_copy(e["resolution_note"]):
            raise SystemExit(f"REFUSED: {e['id']} carries an em dash")
    a = spec["addendum"]
    if set(a) != {"crop", "id", "original_summary", "suffix"}:
        raise SystemExit("REFUSED: addendum has the wrong shape")
    if not a["suffix"].startswith(ADDENDUM_MARK) or not a["suffix"].endswith("]"):
        raise SystemExit("REFUSED: addendum suffix must open with the dated ADDENDUM marker and close its bracket")
    if _bad_copy(a["suffix"]):
        raise SystemExit("REFUSED: addendum carries an em dash")
    crops = {r["crop"] for r in rows} | {a["crop"]}
    if len(crops) != EXPECTED_CROPS:
        raise SystemExit(f"REFUSED: rulings span {len(crops)} crops, pinned {EXPECTED_CROPS}")
    want = {"appends": EXPECTED_APPENDS, "crops": EXPECTED_CROPS, "addenda": EXPECTED_ADDENDA}
    if spec["expected"] != want:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    a = spec["addendum"]
    for crop in {r["crop"] for r in spec["appends"]} | {a["crop"]}:
        c = idx.get(crop)
        if c is None:
            raise SystemExit(f"REFUSED: ruling crop {crop} is not on the roster")
        if not _certified(c):
            raise SystemExit(f"REFUSED: ruling crop {crop} is not certified")
        if any(c.get(k) is not None for k in PDG.FIELDS):
            raise SystemExit(f"REFUSED: {crop} carries a plant dimension; the ruling is about nulls")
        if not isinstance((c.get("verification_status") or {}).get("open_findings"), list):
            raise SystemExit(f"REFUSED: {crop} verification_status.open_findings is not a list")
    for r in spec["appends"]:
        of = idx[r["crop"]]["verification_status"]["open_findings"]
        if any(x.get("id") == r["entry"]["id"] for x in of):
            raise SystemExit(f"REFUSED: {r['crop']} already carries finding {r['entry']['id']}")
    of = idx[a["crop"]]["verification_status"]["open_findings"]
    hits = [x for x in of if x.get("id") == a["id"]]
    if len(hits) != 1:
        raise SystemExit(f"REFUSED: addendum target {a['id']} matches {len(hits)} findings on {a['crop']}")
    if hits[0].get("summary") != a["original_summary"]:
        raise SystemExit(f"REFUSED: addendum target {a['id']} summary has moved since the spec was written")
    if ADDENDUM_MARK in hits[0]["summary"]:
        raise SystemExit(f"REFUSED: addendum target {a['id']} already carries this addendum")
    return len(spec["appends"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    idx = by_slug(post)
    for r in spec["appends"]:
        idx[r["crop"]]["verification_status"]["open_findings"].append(copy.deepcopy(r["entry"]))
    a = spec["addendum"]
    for x in idx[a["crop"]]["verification_status"]["open_findings"]:
        if x.get("id") == a["id"]:
            x["summary"] = x["summary"] + a["suffix"]
    return post


def check_post(post, spec):
    v = PDG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: plant_dimensions_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for crop in {r["crop"] for r in spec["appends"]} | {spec["addendum"]["crop"]}:
        of = idx[crop]["verification_status"]["open_findings"]
        blockers = [x for x in of if x.get("blocks_launch") and x.get("status") != "resolved"]
        if blockers:
            raise SystemExit(f"REFUSED: {crop} carries a launch blocker after the write: {[b.get('id') for b in blockers]}")


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
    a = spec["addendum"]
    tails = {}
    for r in spec["appends"]:
        tails.setdefault(r["crop"], []).append(r["entry"])
    touched = set(tails) | {a["crop"]}
    n_app = n_add = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if slug not in touched:
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: untouched crop {slug} changed")
            continue
        if set(s) != set(g):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s:
            if k != "verification_status" and _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside verification_status")
        sv, gv = s["verification_status"], g["verification_status"]
        if set(sv) != set(gv):
            raise SystemExit(f"REFUSED: {slug} verification_status key set changed")
        for k in sv:
            if k != "open_findings" and _j(sv[k]) != _j(gv[k]):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")
        pa, pb = sv["open_findings"], gv["open_findings"]
        if len(pb) < len(pa):
            raise SystemExit(f"REFUSED: {slug} open_findings shrank")
        for i, (x, y) in enumerate(zip(pa, pb)):
            if slug == a["crop"] and x.get("id") == a["id"]:
                if set(x) != set(y):
                    raise SystemExit(f"REFUSED: {slug} addendum target key set changed")
                for k in x:
                    if k == "summary":
                        if y[k] != x[k] + a["suffix"]:
                            raise SystemExit(f"REFUSED: {slug} addendum target summary is not the original plus the suffix")
                    elif _j(x[k]) != _j(y[k]):
                        raise SystemExit(f"REFUSED: {slug} addendum target field {k!r} changed")
                n_add += 1
            elif _j(x) != _j(y):
                raise SystemExit(f"REFUSED: {slug} open_findings prefix entry {i} is not byte-identical")
        want_tail = tails.get(slug, [])
        if _j(pb[len(pa):]) != _j(want_tail):
            raise SystemExit(f"REFUSED: {slug} open_findings appended {len(pb) - len(pa)} entries, expected {len(want_tail)} matching the spec")
        n_app += len(want_tail)
    # n_add == EXPECTED_ADDENDA is IMPLIED by the per-entry checks (a missing suffix refuses on the summary
    # comparison), so a refusal on the total could never fire in isolation. Informational only.
    return n_app, n_add


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical
    if args.out and os.path.abspath(args.out) == os.path.abspath(path or CANON):
        sys.exit("REFUSED: --out may not target the canonical; use --expect-sha for the write")
    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} appends on {EXPECTED_CROPS} crops with {EXPECTED_ADDENDA} addendum; vocabulary pinned")
    check_pre_state(spec, data)
    print("  pre-state         every ruling crop certified and null on all three keys; ids absent; the addendum target found by id and exact summary")
    post = apply_to(data, spec)
    check_post(post, spec)
    print("  post gates        plant_dimensions_gate (presence ON) 0; no launch blocker on any touched crop")
    n_app, n_add = verify_post(data, post, spec)
    print(f"  verify post       {n_app} findings appended, {n_add} addendum, nothing else")
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
