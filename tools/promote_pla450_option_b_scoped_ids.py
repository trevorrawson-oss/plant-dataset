#!/usr/bin/env python3
"""promote_pla450_option_b_scoped_ids -- PLA-450 Option B, Trevor's ruling of 2026-09-05.

The PLA-450/451 promote (95e66f6d -> 36d6df6b) HELD two of PLA-450's eight pairs because the taxon
check refuted them: cilantro's `bacterial-leaf-spot` is Pseudomonas syringae pv. coriandricola and
the peppers' `bacterial-spot` is Xanthomonas; edamame's `bacterial-blight` is P. savastanoi pv.
glycinea and the beans' `bacterial-blights` are X. campestris pv. phaseoli plus P. syringae pv.
phaseolicola. The ruling: SCOPE the generic id to its single holder, on the celery-early-blight /
bacterial-spot-pruni / mulberry-bacterial-blight pattern. TWO `id` leaves, nothing else.

WHY SCOPE RATHER THAN REGISTER AS-IS (the deciding argument, from the ruling): the collision gate
checks a MINT, never a REUSE. Registering the pairs would have left two generic ids one word apart
naming different pathogens, and a future Xanthomonas author attaching to cilantro's generic
`bacterial-leaf-spot` would fire nothing. Vacating the generic closes that permanently.

WHAT IS DIFFERENT FROM THE CELERY SPLIT, and why each difference is a guard.

1. THE GENERIC ID VACATES. celery's split left `early-blight` populated on seven other crops. Here
   each generic id is held by ONE crop, so after the rewrite it exists nowhere. `check_pre_state`
   pins the singleton premise (the generic must be held by exactly the target crop) and
   `check_vacated` proves the post-state carries neither generic id anywhere. A generic id that
   survived on a second crop would mean the premise was wrong, and the promote refuses.

2. THE SCOPED ID IS THE GENERIC ID WITH A CROP PREFIX. `check_spec_shape` pins `to` ==
   `<scope>-<from>` so the pattern is mechanical, not free-form.

3. THE ROWS ARE EXACTLY THE RULED PAIRS. `RULED` freezes the two generic ids and the ids they
   diverge from; a spec row on any other id refuses. This promote does not widen.

4. THE REGISTRY IS UPDATED THREE WAYS AND EACH IS CHECKED. (a) two new entries pair each scoped id
   with the generic it diverges from, and each reason must name BOTH organisms AND the anchors the
   PLA-450 session read (WSU; Clemson; ISU and UMN), so the adjudication is sourced where it sits.
   (b) the batch-26 mulberry entry that named edamame's OLD id is repointed to the new one, because
   a registry naming a dead id is a stale record; the promote refuses any entry naming a vacated id.
   (c) the moved mulberry pair must still be registered under the new id.

5. THE PREDICTION IS A GUARD, pinned BEFORE the first run: 36 / 22 / 14 -> 36 / 24 / 12. Raw does
   NOT fall. Per scoped id: the OPEN pair with the generic it diverges from retires with the dead
   id (-1 open) and the scoped id collides NAME_SHARED with that same generic (+1, registered).
   For edamame there is more: the registered (bacterial-blight, mulberry-bacterial-blight) pair
   dies with the id (-1 registered) and comes back as (edamame-bacterial-blight,
   mulberry-bacterial-blight) under the repointed entry (+1 registered), and since the normalized
   name 'bacterial blight' now has THREE owners (beans, mulberry, edamame) the scoped id also pairs
   with mulberry. Net: raw -1 +1 -2 +2 = 36; registered +1 -1 +1 +1 = 24; open -2 = 12. Neither
   scoped id sits within edit distance 2 of any live id (checked on 36d6df6b: nearest is
   mulberry-bacterial-blight at 8), so ID_NEAR_DUP contributes nothing, and no name has a
   conjunction (the beans' "(common and halo)" is inside the deleted parenthetical), so check 3
   contributes nothing. `check_collision_prediction` runs the real gate and refuses any other
   figure. The close-out's own estimate (14 -> 12) was derived first and agrees; agreement is
   evidence, not the pin.

6. A57 STAYS GREEN: every rewritten entry keeps its ladder byte-for-byte, checked before the
   generic field loop so an emptied ladder gets its own message.

Usage:
    promote_pla450_option_b_scoped_ids.py            # check, apply, verify, write
    promote_pla450_option_b_scoped_ids.py --check    # checks only, write nothing
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla450_option_b_scoped_ids")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import problem_id_collision_gate as G  # noqa: E402  -- the real gate, never a retyped copy

BASE_SHA = "36d6df6bf3bdd2cac37dc568742c37655d1a739b20c9991285bd9608463925fd"  # PLA-450/451, c189d65
CROPS = ("cilantro-coriander", "edamame")
FIELDS = ("pests", "diseases")
VARIETY_JOIN_FIELDS = ("resistance", "ladder_delta")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Rule 3. The ruling, frozen: generic id -> (crop that holds it alone, the id it diverges from).
RULED = {
    "bacterial-leaf-spot": ("cilantro-coriander", "bacterial-spot"),
    "bacterial-blight": ("edamame", "bacterial-blights"),
}
# Rule 4a. What each new registry entry must carry: (scoped id, generic it diverges from,
# organism tokens, anchor tokens). Anchors are the T1 reads of the PLA-450 session, not re-derived.
ADJUDICATIONS = (
    ("cilantro-bacterial-leaf-spot", "bacterial-spot",
     ("Pseudomonas syringae pv. coriandricola", "Xanthomonas"), ("WSU",)),
    ("edamame-bacterial-blight", "bacterial-blights",
     ("savastanoi pv. glycinea", "phaseoli", "phaseolicola"), ("Clemson", "ISU", "UMN")),
)
# Rule 4c. A registered pair that MOVES with the id and must still be registered afterwards.
MOVED_PAIRS = (("edamame-bacterial-blight", "mulberry-bacterial-blight"),)

# Rule 5. PINNED BEFORE THE FIRST RUN. Never retune.
PREDICTED_BASELINE = {"raw": 36, "registered": 22, "actionable": 14}
PREDICTED = {"raw": 36, "registered": 24, "actionable": 12}
# THE BASELINE IS MEASURED WITH THE REGISTRY AS COMMITTED WHEN IT WAS MEASURED, not the working
# copy. This promote repoints the mulberry entry off edamame's old id, so the working registry
# read against the PRE-state shows 36 / 21 / 15 -- a transitional figure that is neither state.
# The first --check run refused on exactly that, and the fix is to pin WHICH registry the baseline
# means, not to move the baseline. 074f9e2 is the commit the 36 / 22 / 14 figure was measured at.
BASELINE_REGISTRY_COMMIT = "074f9e2"
# THE POST FIGURE IS MEASURED WITH A STAGED SNAPSHOT OF THE REGISTRY, never the working copy.
# ADDED 2026-09-06: the parent promote's suite read the working registry against replayed states
# and went red the moment this promote repointed one entry. The snapshot is what shipped; the
# write path refuses if the working registry differs from it, and the suite replays from it.
REGISTRY_POST = os.path.join(STAGE, "registry_post.json")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. ONE serializer, shared by the promote and its suite."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    for field in FIELDS:
        for e in crop.get(field) or []:
            yield field, e


def id_index(data):
    idx = {}
    for c in data["crops"]:
        for _, e in problems(c):
            if e.get("id"):
                idx.setdefault(e["id"], set()).add(c["slug"])
    return idx


def variety_refs(data):
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
    return list(spec.get("rows") or [])


# ---------------------------------------------------------------- checks

def check_spec_shape(spec):
    """Rules 2 and 3. Exactly the ruled rows, each a crop-prefixed scoping of its generic id."""
    seen_from = set()
    for r in rows(spec):
        for k in ("kind", "crop", "field", "name", "from", "to", "diverges_from"):
            if not r.get(k):
                raise SystemExit(f"REFUSED: spec row {r!r} is missing {k!r}")
        if r["kind"] != "scope":
            raise SystemExit(f"REFUSED: spec row kind {r['kind']!r}; this promote only scopes")
        if r["field"] not in FIELDS:
            raise SystemExit(f"REFUSED: spec row field {r['field']!r} is not one of {FIELDS}")
        for k in ("from", "to", "diverges_from"):
            if not KEBAB.match(r[k]):
                raise SystemExit(f"REFUSED: spec row {k} id {r[k]!r} is not kebab-case")
        if r["from"] not in RULED:
            raise SystemExit(f"REFUSED: spec row scopes {r['from']!r}, which is not in Trevor's "
                             f"ruling; this promote does not widen")
        crop, diverges = RULED[r["from"]]
        if r["crop"] != crop:
            raise SystemExit(f"REFUSED: {r['from']!r} is ruled on {crop!r}, spec row says {r['crop']!r}")
        if r["diverges_from"] != diverges:
            raise SystemExit(f"REFUSED: {r['from']!r} diverges from {diverges!r} in the ruling, spec "
                             f"row says {r['diverges_from']!r}")
        scope = r["crop"].split("-")[0]
        if r["to"] != f"{scope}-{r['from']}":
            raise SystemExit(f"REFUSED: scoped id {r['to']!r} is not the crop-prefixed generic "
                             f"{scope}-{r['from']}; the pattern is mechanical")
        if r["from"] in seen_from:
            raise SystemExit(f"REFUSED: spec scopes {r['from']!r} twice")
        seen_from.add(r["from"])
    if seen_from != set(RULED):
        raise SystemExit(f"REFUSED: spec covers {sorted(seen_from)}, the ruling covers {sorted(RULED)}")
    if {r["crop"] for r in rows(spec)} != set(CROPS):
        raise SystemExit("REFUSED: spec crops do not match the declared CROPS")
    return len(rows(spec))


def check_pre_state(spec, data):
    """Rule 1's premise. The target exists once by (crop, field, name), carries the generic id and
    a ladder; the generic id is held by EXACTLY this crop (so it will vacate); the scoped id does
    not exist yet; the id it diverges from is live on other crops."""
    idx = by_slug(data)
    ids = id_index(data)
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
            raise SystemExit(f"REFUSED: {r['crop']}/{r['name']!r} has no ladder in the pre-state")
        holders = ids.get(r["from"], set())
        if holders != {r["crop"]}:
            raise SystemExit(f"REFUSED: generic {r['from']!r} is held by {sorted(holders)}, not by "
                             f"{r['crop']!r} alone; the vacate premise is wrong, this is not a "
                             f"singleton scoping")
        if r["to"] in ids:
            raise SystemExit(f"REFUSED: scoped id {r['to']!r} already exists on {sorted(ids[r['to']])}")
        if not (ids.get(r["diverges_from"], set()) - {r["crop"]}):
            raise SystemExit(f"REFUSED: {r['diverges_from']!r} is not live on any other crop; there "
                             f"is nothing to diverge from")
        n += 1
    return n


def check_variety_refs(data, touched):
    """Every variety-level reference resolves on its crop, and none names a touched id."""
    ids_on = {c["slug"]: {e["id"] for _, e in problems(c) if e.get("id")} for c in data["crops"]}
    n = 0
    for slug, vname, jf, pid in variety_refs(data):
        if pid not in ids_on[slug]:
            raise SystemExit(f"REFUSED: {slug}/{vname}/{jf} references {pid!r}, which is not a "
                             f"problem id on {slug}: a dangling variety join")
        if pid in touched:
            raise SystemExit(f"REFUSED: {slug}/{vname}/{jf} references {pid!r}, an id this promote "
                             f"touches; references are not rewritten here")
        n += 1
    if n == 0:
        raise SystemExit("REFUSED: found zero variety references; the join surface has vanished")
    return n


def check_registry(spec):
    """Rule 4, all three ways."""
    reg = json.load(open(G.REGISTRY_PATH, encoding="utf-8"))["deliberately_distinct"]
    by_pair = {}
    for e in reg:
        ids = e["ids"]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                by_pair[frozenset((ids[i], ids[j]))] = e
    for scoped, generic, organisms, anchors in ADJUDICATIONS:
        e = by_pair.get(frozenset((scoped, generic)))
        if e is None:
            raise SystemExit(f"REFUSED: registry has no entry for {scoped!r} / {generic!r}; the "
                             f"ruling is not adjudicated where the gate reads it")
        for org in organisms:
            if org not in e["reason"]:
                raise SystemExit(f"REFUSED: registry reason for {scoped!r} does not name {org!r}; "
                                 f"an adjudication names both organisms")
        for anc in anchors:
            if anc not in e["reason"]:
                raise SystemExit(f"REFUSED: registry reason for {scoped!r} does not cite {anc!r}; "
                                 f"the adjudication must be sourced where it sits")
    vacated = {r["from"] for r in rows(spec)}
    for e in reg:
        stale = vacated & set(e["ids"])
        if stale:
            raise SystemExit(f"REFUSED: registry entry {e['ids']} names vacated id(s) "
                             f"{sorted(stale)}; a registry naming a dead id is a stale record")
    for a, b in MOVED_PAIRS:
        if frozenset((a, b)) not in by_pair:
            raise SystemExit(f"REFUSED: the moved pair {a!r} / {b!r} is not registered; the "
                             f"batch-26 adjudication was lost in the repoint")
    return len(ADJUDICATIONS)


def collision_figures(data, registry=None):
    f = G.scan(data, registry=registry or G.load_registry())
    reg = sum(1 for x in f if x.registered)
    return {"raw": len(f), "registered": reg, "actionable": len(f) - reg}


def baseline_registry():
    """The registry exactly as committed at BASELINE_REGISTRY_COMMIT, read from git so it cannot
    drift with the working copy or with HEAD."""
    import subprocess
    raw = subprocess.run(["git", "-C", REPO, "show",
                          f"{BASELINE_REGISTRY_COMMIT}:tools/problem_id_registry.json"],
                         capture_output=True, text=True, check=True).stdout
    return G.Registry(json.loads(raw)["deliberately_distinct"])


def post_registry():
    """The registry as staged with this promote: the snapshot that shipped."""
    return G.Registry(json.load(open(REGISTRY_POST, encoding="utf-8"))["deliberately_distinct"])


def check_registry_snapshot_is_current():
    """WRITE-PATH GUARD. The staged snapshot must be byte-equal to the working registry at apply
    time, or the suite would replay a registry that never shipped."""
    a = open(REGISTRY_POST, "rb").read()
    b = open(G.REGISTRY_PATH, "rb").read()
    if a != b:
        raise SystemExit("REFUSED: staged registry snapshot differs from the working registry; "
                         "re-stage it or explain the difference before writing")
    return True


def check_collision_prediction(pre, post):
    """Rule 5. Baseline (pre-state, COMMITTED registry) must be what the prediction was made from;
    post (post-state, STAGED registry snapshot) must be what was predicted."""
    base = collision_figures(pre, baseline_registry())
    if base != PREDICTED_BASELINE:
        raise SystemExit(f"REFUSED: pre-state collision figures {base} != the baseline the prediction "
                         f"rests on {PREDICTED_BASELINE}; re-derive the prediction before running")
    got = collision_figures(post, post_registry())
    if got != PREDICTED:
        raise SystemExit(f"REFUSED: post-state collision figures {got} != PREDICTED {PREDICTED}. "
                         f"A figure that differs from the prediction is a finding; stop, do not "
                         f"reconcile after the fact.")
    return got


# ---------------------------------------------------------------- apply / verify

def apply_to(data, spec):
    out = copy.deepcopy(data)
    idx = by_slug(out)
    for r in rows(spec):
        hits = [e for e in idx[r["crop"]][r["field"]]
                if e.get("name") == r["name"] and e.get("id") == r["from"]]
        if len(hits) != 1:
            raise SystemExit(f"REFUSED: apply matched {len(hits)} entries for {r['crop']}/{r['name']!r}")
        hits[0]["id"] = r["to"]
    return out


def check_vacated(post, spec):
    """Rule 1. The generic ids exist nowhere; each scoped id exists exactly on its crop."""
    idx = id_index(post)
    for r in rows(spec):
        if r["from"] in idx:
            raise SystemExit(f"REFUSED: generic {r['from']!r} still carried by {sorted(idx[r['from']])} "
                             f"after the rewrite; it was supposed to vacate")
        if idx.get(r["to"]) != {r["crop"]}:
            raise SystemExit(f"REFUSED: scoped id {r['to']!r} is on {sorted(idx.get(r['to'], ()))}, "
                             f"expected exactly {r['crop']!r}")
    return len(rows(spec))


def check_within_crop_unique(post):
    idx = by_slug(post)
    n = 0
    for slug in CROPS:
        seen = {}
        for _, e in problems(idx[slug]):
            seen[e.get("id")] = seen.get(e.get("id"), 0) + 1
        dup = sorted(p for p, k in seen.items() if k > 1)
        if dup:
            raise SystemExit(f"REFUSED: {slug} carries duplicate id(s) {dup} after the rewrite")
        n += len(seen)
    return n


def verify_post(pre, post, spec):
    """Every changed leaf is one this promote pinned. SET COMPARISON BEFORE VALUE COMPARISON."""
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
                # Rule 6: A57's concern, BEFORE the generic field loop.
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
    print(f"  spec shape           {n} rows, exactly the ruled pairs, each a crop-prefixed generic")
    n = check_pre_state(spec, data)
    print(f"  pre-state            {n} targets found once, each generic id a singleton on its crop")
    touched = {r["from"] for r in rows(spec)} | {r["to"] for r in rows(spec)}
    nv = check_variety_refs(data, touched)
    print(f"  variety refs (pre)   {nv} references resolve, none on a touched id")
    check_registry(spec)
    print("  registry             both adjudications sourced; no entry names a vacated id; moved pair kept")

    post = apply_to(data, spec)
    check_vacated(post, spec)
    print("  vacated              both generic ids exist nowhere; each scoped id on its crop alone")
    nu = check_within_crop_unique(post)
    print(f"  within-crop unique   {nu} ids across the {len(CROPS)} touched crops, no duplicates")
    nv = check_variety_refs(post, touched)
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
    check_registry_snapshot_is_current()
    print("  registry snapshot    staged snapshot == working registry")
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
