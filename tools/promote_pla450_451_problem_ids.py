#!/usr/bin/env python3
"""promote_pla450_451_problem_ids -- PLA-450 (merge duplicate problem ids) + PLA-451 (split celery's
two blights off the tomato/potato ids). ONE promote, NINE leaves, every one of them an `id`.

WHAT THIS PROMOTE IS. A problem `id` is a JOIN KEY: `varieties[].resistance` and
`varieties[].ladder_delta` point at it and nothing else in the dataset does. PLA-448 s4a found eight
pairs of ids naming one problem twice, minted by authoring passes that never checked precedent, and
s4c found the opposite defect on celery: one id (`early-blight`, `late-blight`) spanning crops whose
pathogens differ. Both are join-key defects and both are fixed by rewriting exactly one leaf per
entry. No name, no prose, no ladder, no type moves. `verify_post` pins that at the leaf.

WHAT IS DIFFERENT HERE, and why each difference is a guard rather than a note.

1. SIX MERGES, NOT EIGHT. The taxon check refutes two of PLA-450's pairs, and the entries' OWN cause
   prose is what refutes them. cilantro's `bacterial-leaf-spot` is Pseudomonas syringae pv.
   coriandricola (WSU Mt Vernon, its cited anchor, read 2026-09-05); the peppers' `bacterial-spot`
   is Xanthomonas. edamame's `bacterial-blight` is Pseudomonas savastanoi pv. glycinea (its cited
   ISU anchor; UMN read 2026-09-05); the beans' `bacterial-blights` is Xanthomonas campestris pv.
   phaseoli plus P. syringae pv. phaseolicola (Clemson, its cited anchor, read 2026-09-05). Merging
   either pair would CREATE the defect PLA-451 exists to fix. `check_held_pairs` REFUSES a row on
   either pair; it is a refusal spec, green on the real spec and red under injection. The two pairs
   stay OPEN in the collision gate on purpose: they are a decision Trevor has not made, and the gate
   is the decision surface.

2. MAJORITY WINS IS MEASURED, NOT ASSERTED. For every merge row the `to` id must already live on
   MORE crops than the `from` id, counted from the pre-state. A row pointing the wrong way refuses.

3. THE VARIETY JOIN IS CHECKED ON BOTH STATES. All 129 `resistance` / `ladder_delta` references are
   resolved before and after, and no reference may name a retired id. Measured at 95e66f6d: none of
   the 129 sit on any id this promote touches, so the guard is a refusal spec here -- and it is the
   guard that PLA-12 will need, so it ships tested.

4. THE PREDICTION IS A GUARD. PLA-450's addendum requires the post-promote collision figures to be
   predicted BEFORE the run and compared after. `PREDICTED` was pinned from the 42-pair finding list
   and the gate's own normalization before this file was first executed: raw 36 / registered 22 /
   actionable 14, from 42 / 20 / 22. `check_collision_prediction` runs the real gate on the post
   state and REFUSES on any other figure. A number read off afterward would be just a number; a
   refusal on mismatch is "stop rather than reconcile" written down.

   How 42 -> 36. Eight OPEN pairs retire because their minority id ceases to exist: cutworm,
   flea-beetle, japanese-beetle, botrytis-gray-mold, twospotted-spider-mite (one pair each) and the
   slug family (three pairs: slugs/slugs-and-snails, slugs/snails-and-slugs,
   slugs-and-snails/snails-and-slugs). No registered pair names a retired id, so registered does not
   fall. The two celery mints each collide on NAME_SHARED with the generic id they left ('blight
   early' == 'blight early'; 'blight late' likewise), adding two pairs, both registered in
   problem_id_registry.json with the organism-level reason. Net: raw -8 +2 = 36; registered +2 = 22;
   open -8 = 14. The moved names create no third collision (checked: no other id owns the keys
   'cutworm', 'flea beetle', 'japanese beetle', 'gray mold', 'mite spider twospotted', 'slug' or
   'and slug snail'), and neither celery mint sits within edit distance 2 of any live id.

5. A57 IS ARMED AND MUST STAY GREEN. A merge that drops a ladder is exactly what the coverage floor
   exists to catch, so `verify_post` asserts every rewritten entry keeps a non-empty `control_ladder`
   byte-for-byte, on top of the roster gauntlet.

6. RETIREMENT IS COMPLETE. After apply, no entry anywhere carries a merged-away id (a straggler would
   leave the duplicate half-merged), and each celery mint leaves the generic id populated on the
   other crops (a split that emptied `early-blight` would be a rename, not a split).

Usage:
    promote_pla450_451_problem_ids.py            # check, apply, verify, write
    promote_pla450_451_problem_ids.py --check    # checks only, write nothing
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla450_451_problem_ids")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import problem_id_collision_gate as G  # noqa: E402  -- the real gate, never a retyped copy

BASE_SHA = "95e66f6d1a8ea8550b2df3825d3bcbb00d39056e106d037290737923f74d0879"  # batch 27, the arc's end
CROPS = ("artichoke", "asparagus", "basil", "celery", "strawberry", "swiss-chard")
KINDS = ("merge", "mint")
MINTED = ("celery-early-blight", "celery-late-blight")
FIELDS = ("pests", "diseases")
VARIETY_JOIN_FIELDS = ("resistance", "ladder_delta")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Rule 1. Pairs PLA-450 lists that the taxon check REFUTES. Frozen here so the refusal outlives the
# session that made it; the reason names the organisms, not the id strings.
HELD = {
    frozenset(("bacterial-leaf-spot", "bacterial-spot")):
        "cilantro's is Pseudomonas syringae pv. coriandricola (WSU Mt Vernon); the peppers' is "
        "Xanthomonas. Different pathogens, different hosts: merging would create the PLA-451 defect.",
    frozenset(("bacterial-blight", "bacterial-blights")):
        "edamame's is Pseudomonas savastanoi pv. glycinea (ISU, UMN); the beans' are Xanthomonas "
        "campestris pv. phaseoli and P. syringae pv. phaseolicola (Clemson). Different pathogens.",
}

# Rule 4. PINNED BEFORE THE FIRST RUN, from the 42-pair finding list at 95e66f6d. Never retune.
PREDICTED_BASELINE = {"raw": 42, "registered": 20, "actionable": 22}
PREDICTED = {"raw": 36, "registered": 22, "actionable": 14}

# What the registry must say about each mint, so the split's adjudication is written down where the
# gate reads it. (mint id, generic id, two organism names the reason must carry)
MINT_ADJUDICATIONS = (
    ("celery-early-blight", "early-blight", ("Cercospora", "Alternaria")),
    ("celery-late-blight", "late-blight", ("Septoria", "Phytophthora")),
)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. separators, ensure_ascii=False, no trailing newline, never indent.
    ONE serializer, shared by this promote and its suite: a suite that does its own json.dumps
    grades itself and an indent mutation survives."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    for field in FIELDS:
        for e in crop.get(field) or []:
            yield field, e


def id_index(data):
    """id -> set of crop slugs carrying it."""
    idx = {}
    for c in data["crops"]:
        for _, e in problems(c):
            if e.get("id"):
                idx.setdefault(e["id"], set()).add(c["slug"])
    return idx


def variety_refs(data):
    """(crop, variety name, join field, problem id) for every variety-level problem reference."""
    for c in data["crops"]:
        v = c.get("varieties")
        if not isinstance(v, dict):
            continue
        for x in v.get("recommended") or []:
            if not isinstance(x, dict):
                continue
            for jf in VARIETY_JOIN_FIELDS:
                m = x.get(jf)
                if isinstance(m, dict):
                    for pid in m:
                        yield c["slug"], x.get("name") or x.get("id") or "?", jf, pid


# ---------------------------------------------------------------- load

def load_canonical(path=None):
    raw = open(path or CANON, "rb").read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        sys.exit(f"REFUSED: base SHA mismatch.\n  expected {BASE_SHA}\n  got      {got}")
    return json.loads(raw.decode("utf-8"))


def staged():
    if not os.path.exists(SPEC):
        sys.exit(f"REFUSED: missing spec {SPEC}")
    return json.load(open(SPEC, encoding="utf-8"))


def rows(spec):
    return [r for r in spec.get("rows") or []]


# ---------------------------------------------------------------- checks

def check_spec_shape(spec):
    """Every row is one id rewrite on one entry. Kinds real, ids kebab, from != to, no entry named
    twice, every touched crop declared in CROPS and every declared crop touched, and the mint set
    is exactly MINTED."""
    seen = set()
    touched = set()
    mints = set()
    for r in rows(spec):
        for k in ("kind", "crop", "field", "name", "from", "to"):
            if not r.get(k):
                raise SystemExit(f"REFUSED: spec row {r!r} is missing {k!r}")
        if r["kind"] not in KINDS:
            raise SystemExit(f"REFUSED: spec row kind {r['kind']!r} is not one of {KINDS}")
        if r["field"] not in FIELDS:
            raise SystemExit(f"REFUSED: spec row field {r['field']!r} is not one of {FIELDS}")
        for k in ("from", "to"):
            if not KEBAB.match(r[k]):
                raise SystemExit(f"REFUSED: spec row {k} id {r[k]!r} is not kebab-case")
        if r["from"] == r["to"]:
            raise SystemExit(f"REFUSED: spec row {r['crop']}/{r['name']!r} rewrites an id to itself")
        key = (r["crop"], r["field"], r["name"])
        if key in seen:
            raise SystemExit(f"REFUSED: spec names the same entry twice: {key!r}")
        seen.add(key)
        if r["crop"] not in CROPS:
            raise SystemExit(f"REFUSED: spec touches {r['crop']!r}, which is not a declared crop")
        touched.add(r["crop"])
        if r["kind"] == "mint":
            mints.add(r["to"])
    if touched != set(CROPS):
        raise SystemExit(f"REFUSED: declared crops {sorted(set(CROPS) - touched)} have no spec row")
    if mints != set(MINTED):
        raise SystemExit(f"REFUSED: spec mints {sorted(mints)}, expected exactly {sorted(MINTED)}")
    return len(rows(spec))


def check_held_pairs(spec):
    """Rule 1. A REFUSAL SPEC: refuse any row whose (from, to) is a taxon-refuted pair."""
    for r in rows(spec):
        pair = frozenset((r["from"], r["to"]))
        if pair in HELD:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['name']!r} would merge a taxon-refuted pair "
                             f"{sorted(pair)}: {HELD[pair]}")
    return len(HELD)


def check_pre_state(spec, data):
    """Each target exists exactly once by (crop, field, name), carries the `from` id, and already
    carries a non-empty ladder (the thing A57 must still see afterwards)."""
    idx = by_slug(data)
    n = 0
    for r in rows(spec):
        crop = idx.get(r["crop"])
        if crop is None:
            raise SystemExit(f"REFUSED: crop {r['crop']!r} not in the roster")
        hits = [e for e in crop.get(r["field"]) or [] if e.get("name") == r["name"]]
        if len(hits) != 1:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['field']} matched {len(hits)} entries named "
                             f"{r['name']!r}, need exactly 1")
        e = hits[0]
        if e.get("id") != r["from"]:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['name']!r} carries id {e.get('id')!r}, "
                             f"spec expects {r['from']!r}; the pre-state has drifted")
        if not isinstance(e.get("control_ladder"), list) or not e["control_ladder"]:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['name']!r} has no ladder in the pre-state; "
                             f"an id rewrite is not where that gets fixed")
        n += 1
    return n


def check_direction(spec, data):
    """Rule 2 and rule 6's pre-half. A merge points at the MAJORITY id, which must already live on
    more crops than the minority id and must not already sit on the target crop (that would be a
    within-crop duplicate, not a merge). A mint's `to` must exist NOWHERE yet, and its `from` must
    stay populated elsewhere so the split is a split."""
    idx = id_index(data)
    for r in rows(spec):
        frm, to = idx.get(r["from"], set()), idx.get(r["to"], set())
        if r["kind"] == "merge":
            if len(to - {r["crop"]}) <= len(frm):
                raise SystemExit(f"REFUSED: merge {r['from']!r} -> {r['to']!r} points at the "
                                 f"minority: {r['to']!r} on {len(to - {r['crop']})} other crops, "
                                 f"{r['from']!r} on {len(frm)}. Majority wins; flip the row or "
                                 f"hold it.")
            if r["crop"] in to:
                raise SystemExit(f"REFUSED: {r['crop']} already carries {r['to']!r}; the merge "
                                 f"would create a within-crop duplicate id")
        else:
            if to:
                raise SystemExit(f"REFUSED: mint {r['to']!r} already exists on {sorted(to)}; "
                                 f"a mint must be new")
            if len(frm - {r["crop"]}) < 1:
                raise SystemExit(f"REFUSED: mint {r['to']!r} would empty {r['from']!r}; that is a "
                                 f"rename, not a split")
    return len(rows(spec))


def check_variety_refs(data, retired):
    """Rule 3. Every variety-level problem reference resolves on its own crop, and none names an
    id this promote retires. Runs on the pre-state AND the post-state."""
    ids_on = {c["slug"]: {e["id"] for _, e in problems(c) if e.get("id")} for c in data["crops"]}
    n = 0
    for slug, vname, jf, pid in variety_refs(data):
        if pid not in ids_on[slug]:
            raise SystemExit(f"REFUSED: {slug}/{vname}/{jf} references {pid!r}, which is not a "
                             f"problem id on {slug}: a dangling variety join")
        if pid in retired:
            raise SystemExit(f"REFUSED: {slug}/{vname}/{jf} references {pid!r}, an id this promote "
                             f"retires; the reference would need rewriting and this promote "
                             f"does not rewrite references")
        n += 1
    if n == 0:
        raise SystemExit("REFUSED: found zero variety references; the join surface this promote "
                         "protects has vanished, which is a schema change, not a pass")
    return n


def check_registry(spec):
    """The split's adjudication must be written where the gate reads it, and the registry must not
    keep naming an id this promote retires."""
    reg = json.load(open(G.REGISTRY_PATH, encoding="utf-8"))["deliberately_distinct"]
    by_pair = {}
    for e in reg:
        ids = e["ids"]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                by_pair[frozenset((ids[i], ids[j]))] = e
    for mint, generic, organisms in MINT_ADJUDICATIONS:
        e = by_pair.get(frozenset((mint, generic)))
        if e is None:
            raise SystemExit(f"REFUSED: registry has no entry for {mint!r} / {generic!r}; the split "
                             f"is not adjudicated where the gate reads it")
        for org in organisms:
            if org not in e["reason"]:
                raise SystemExit(f"REFUSED: registry reason for {mint!r} / {generic!r} does not name "
                                 f"{org!r}; an adjudication names both organisms")
    retired = {r["from"] for r in rows(spec) if r["kind"] == "merge"}
    for e in reg:
        stale = retired & set(e["ids"])
        if stale:
            raise SystemExit(f"REFUSED: registry entry {e['ids']} names retired id(s) "
                             f"{sorted(stale)}; a registry naming a dead id is a stale record")
    return len(MINT_ADJUDICATIONS)


def collision_figures(data):
    """The three figures PLA-450 asks for, from the REAL gate with the REAL registry."""
    f = G.scan(data, registry=G.load_registry())
    reg = sum(1 for x in f if x.registered)
    return {"raw": len(f), "registered": reg, "actionable": len(f) - reg}


def check_collision_prediction(pre, post):
    """Rule 4. The baseline must be what the prediction was made from, and the post-state must be
    what was predicted. Any other figure is a finding, and a finding stops the promote."""
    base = collision_figures(pre)
    if base != PREDICTED_BASELINE:
        raise SystemExit(f"REFUSED: pre-state collision figures {base} != the baseline the prediction "
                         f"rests on {PREDICTED_BASELINE}; re-derive the prediction before running")
    got = collision_figures(post)
    if got != PREDICTED:
        raise SystemExit(f"REFUSED: post-state collision figures {got} != PREDICTED {PREDICTED}. "
                         f"A figure that differs from the prediction is a finding; stop, do not "
                         f"reconcile after the fact.")
    return got


# ---------------------------------------------------------------- apply / verify

def apply_to(data, spec):
    """Nine leaves: the `id` of each spec target. Nothing else is touched."""
    out = copy.deepcopy(data)
    idx = by_slug(out)
    for r in rows(spec):
        hits = [e for e in idx[r["crop"]][r["field"]]
                if e.get("name") == r["name"] and e.get("id") == r["from"]]
        if len(hits) != 1:
            raise SystemExit(f"REFUSED: apply matched {len(hits)} entries for {r['crop']}/{r['name']!r}")
        hits[0]["id"] = r["to"]
    return out


def check_retirement_complete(post, spec):
    """Rule 6. No entry anywhere still carries a merged-away id; each mint's generic id still
    lives on the other crops."""
    idx = id_index(post)
    for r in rows(spec):
        if r["kind"] == "merge":
            if r["from"] in idx:
                raise SystemExit(f"REFUSED: retired id {r['from']!r} still carried by "
                                 f"{sorted(idx[r['from']])}; the merge left a straggler")
        else:
            if r["from"] not in idx:
                raise SystemExit(f"REFUSED: generic id {r['from']!r} vanished after the split")
            if r["crop"] in idx[r["from"]]:
                raise SystemExit(f"REFUSED: {r['crop']} still carries {r['from']!r} after minting "
                                 f"{r['to']!r}")
    return sum(1 for r in rows(spec) if r["kind"] == "merge")


def check_within_crop_unique(post):
    """A merge onto an id the crop already held would be the IDENTITY defect control_ladder_gate
    reports; refuse it here first, on the touched crops."""
    idx = by_slug(post)
    n = 0
    for slug in CROPS:
        seen = {}
        for _, e in problems(idx[slug]):
            pid = e.get("id")
            seen[pid] = seen.get(pid, 0) + 1
        dup = sorted(p for p, k in seen.items() if k > 1)
        if dup:
            raise SystemExit(f"REFUSED: {slug} carries duplicate id(s) {dup} after the rewrite")
        n += len(seen)
    return n


def verify_post(pre, post, spec):
    """Every changed leaf must be one this promote pinned. SET COMPARISON BEFORE VALUE COMPARISON:
    iterating `pre` alone makes everything ADDED in `post` invisible."""
    pre_i, post_i = by_slug(pre), by_slug(post)

    if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:
        raise SystemExit("REFUSED: crop roster changed")
    if len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop count changed")
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k == "crops":
            continue
        if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    for slug in pre_i:
        if slug in CROPS:
            continue
        if json.dumps(pre_i[slug], sort_keys=True) != json.dumps(post_i[slug], sort_keys=True):
            raise SystemExit(f"REFUSED: untouched crop {slug} changed")

    targets = {(r["crop"], r["field"], r["name"]): r for r in rows(spec)}
    changed = 0
    for slug in CROPS:
        s_crop, g_crop = pre_i[slug], post_i[slug]
        if set(s_crop) != set(g_crop):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s_crop:
            if k in FIELDS:
                continue
            if json.dumps(s_crop[k], sort_keys=True) != json.dumps(g_crop[k], sort_keys=True):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the problem arrays")
        for field in FIELDS:
            src, got = s_crop.get(field) or [], g_crop.get(field) or []
            if len(src) != len(got):
                raise SystemExit(f"REFUSED: {slug}/{field} entry count {len(src)} -> {len(got)}")
            for s, g in zip(src, got):
                if g.get("name") != s.get("name"):
                    raise SystemExit(f"REFUSED: {slug}/{field} entry order or name changed")
                if set(s) != set(g):
                    raise SystemExit(f"REFUSED: {slug}/{s.get('name')!r} entry key set changed: "
                                     f"added {sorted(set(g) - set(s))}, removed "
                                     f"{sorted(set(s) - set(g))}")
                # A57's concern, checked BEFORE the generic field loop so an emptied ladder gets
                # its own message instead of being masked by "field changed".
                if not isinstance(g.get("control_ladder"), list) or not g["control_ladder"]:
                    raise SystemExit(f"REFUSED: {slug}/{s.get('name')!r} lost its ladder; A57 "
                                     f"would catch this and so does this")
                for k in s:
                    if k == "id":
                        continue
                    if json.dumps(s[k], sort_keys=True) != json.dumps(g[k], sort_keys=True):
                        raise SystemExit(f"REFUSED: {slug}/{s.get('name')!r} field {k!r} changed; "
                                         f"this promote rewrites ids and nothing else")
                r = targets.get((slug, field, s.get("name")))
                if r is None:
                    if g["id"] != s["id"]:
                        raise SystemExit(f"REFUSED: {slug}/{s.get('name')!r} id changed "
                                         f"{s['id']!r} -> {g['id']!r} without a spec row")
                else:
                    if s["id"] != r["from"] or g["id"] != r["to"]:
                        raise SystemExit(f"REFUSED: {slug}/{s.get('name')!r} id {s['id']!r} -> "
                                         f"{g['id']!r} does not match its spec row")
                    changed += 1
    if changed != len(rows(spec)):
        raise SystemExit(f"REFUSED: {changed} id leaves changed, spec has {len(rows(spec))} rows")
    if changed == 0:
        raise SystemExit("REFUSED: nothing changed; the promote would be a no-op")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical

    data = load_canonical(path)
    spec = staged()

    n = check_spec_shape(spec)
    print(f"  spec shape           {n} rows, one id leaf each; mints exactly {sorted(MINTED)}")
    h = check_held_pairs(spec)
    print(f"  held pairs           {h} taxon-refuted pairs, none in the spec (refusal spec)")
    n = check_pre_state(spec, data)
    print(f"  pre-state            {n} targets found once by name, carrying the expected id and a ladder")
    check_direction(spec, data)
    print("  direction            every merge points at the majority id; every mint is new")
    retired = {r["from"] for r in rows(spec) if r["kind"] == "merge"}
    nv = check_variety_refs(data, retired)
    print(f"  variety refs (pre)   {nv} references resolve, none on a retired id")
    check_registry(spec)
    print("  registry             both celery splits adjudicated, no entry names a retired id")

    post = apply_to(data, spec)
    check_retirement_complete(post, spec)
    print("  retirement           no straggler on a merged id; generic blight ids still populated")
    nu = check_within_crop_unique(post)
    print(f"  within-crop unique   {nu} ids across the {len(CROPS)} touched crops, no duplicates")
    nv = check_variety_refs(post, retired)
    print(f"  variety refs (post)  {nv} references resolve")
    fig = check_collision_prediction(data, post)
    print(f"  collision prediction {PREDICTED_BASELINE} -> {fig}  == PREDICTED, as pinned before the run")
    leaves = verify_post(data, post, spec)
    print(f"  verify post          {leaves} id leaves changed, nothing else")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.check and not args.apply:
        print("  --check: nothing written")
        return 0
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
