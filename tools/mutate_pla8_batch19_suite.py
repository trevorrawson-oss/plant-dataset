#!/usr/bin/env python3
"""Mutation harness for the batch-19 promote (PLA-215).

Families: `schema` attacks the premise. `types` attacks the STRONG preservation rule -- all 32
problems already carry a fine type, so no change is permitted, and the broken-premise branch is
driven separately. `ids` attacks the convention table, the six refusals and the nine reuse anchors.
`brownrot` attacks the taxon trap in three directions (a citrus taking the stone-fruit id, the id
vanishing off-batch, and the id leaking onto acid citrus) plus its anti-vacuity check. `mites`
attacks the split in BOTH directions, including the retro-split of the acid-citrus composite.
`canker` attacks a STANDING batch 18 ruling, on staged AND on already-shipped crops. `crossbatch`
attacks the guard this batch exists for, which reads CANONICAL rather than only the staging
directory. `temps`, `vocab`, `materials`, `validate`, `blast`, `catalog` and `mechanics` as in
batch 18.

Every disabled branch has a driver in the suite asserting its ONE specific message, so a mutation
cannot be "caught" by an unrelated earlier check and score a false positive.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch19.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch19.py")
STAGING_NAME = "pla8_batch19_sweet_citrus"
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- schema ---------------------------------------------------------------------------------
    ("schema: a missing batch crop is accepted", "schema", PROMOTE,
     "        if c not in by:", "        if False:"),
    ("schema: the premise-field loop runs over nothing", "schema", PROMOTE,
     "            for f in PREMISE_FIELDS:", "            for f in ():"),
    ("schema: an already-laddered crop is accepted", "schema", PROMOTE,
     '            if p.get("control_ladder"):', "            if False:"),

    # ---- types ----------------------------------------------------------------------------------
    ("types: a coarse pre-state type no longer breaks the premise", "types", PROMOTE,
     "                if pre not in _TYPE_TARGETS:", "                if False:"),
    ("types: a type may be silently changed", "types", PROMOTE,
     "                if post != pre:", "                if False:"),
    ("types: the coverage count is not pinned", "types", PROMOTE,
     "    if checked != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- ids ------------------------------------------------------------------------------------
    ("ids: a problem/id arity mismatch is accepted", "ids", PROMOTE,
     "            if len(names) != len(got):", "            if False:"),
    ("ids: an unknown problem name is accepted", "ids", PROMOTE,
     "                if want is None:", "                if False:"),
    ("ids: the convention table is never enforced", "ids", PROMOTE,
     "                if i != want:", "                if False:"),
    ("ids: the refusal table is never consulted", "ids", PROMOTE,
     "                if i in REFUSED_IDS:", "                if False:"),
    ("ids: a reused id resolving nowhere is accepted", "ids", PROMOTE,
     "        if i not in existing:", "        if False:"),
    ("ids: a reused id losing its anchor crop is accepted", "ids", PROMOTE,
     "        if anchor not in existing[i]:", "        if False:"),
    ("ids: a new id that already exists is accepted", "ids", PROMOTE,
     "        if i in existing:", "        if False:"),

    # ---- brownrot -------------------------------------------------------------------------------
    ("brownrot: a citrus may take the stone-fruit id", "brownrot", PROMOTE,
     '            if p.get("id") == "brown-rot":', "            if False:"),
    ("brownrot: the anti-vacuity check is disabled", "brownrot", PROMOTE,
     "    if not found:", "    if False:"),
    ("brownrot: the id may vanish off-batch entirely", "brownrot", PROMOTE,
     "    if not holders:", "    if False:"),
    ("brownrot: the id may leak onto acid citrus", "brownrot", PROMOTE,
     "    if holders & set(ACID):", "    if False:"),

    # ---- mites ----------------------------------------------------------------------------------
    ("mites: a species-specific id may go missing", "mites", PROMOTE,
     "        if pid not in got:", "        if False:"),
    ("mites: sweet citrus may take the composite", "mites", PROMOTE,
     '    if "citrus-mites" in got:', "    if False:"),
    ("mites: the acid-citrus composite may be RETRO-SPLIT", "mites", PROMOTE,
     "    if not composite & set(ACID):", "    if False:"),

    # ---- canker ---------------------------------------------------------------------------------
    ("canker: a staged crop may carry the curative key", "canker", PROMOTE,
     '            if "prune_out_infection" in [r["method"] for r in p.get("control_ladder") or []]:\n'
     '                raise SystemExit("REFUSED: %s/citrus-canker carries prune_out_infection, a CURATIVE "',
     '            if False:\n'
     '                raise SystemExit("REFUSED: %s/citrus-canker carries prune_out_infection, a CURATIVE "'),
    ("canker: an already-SHIPPED crop may undo the ruling", "canker", PROMOTE,
     '                if "prune_out_infection" in [r["method"] for r in p.get("control_ladder") or []]:',
     "                if False:"),
    ("canker: the anti-vacuity check is disabled", "canker", PROMOTE,
     "    if seen == 0:", "    if False:"),

    # ---- crossbatch -----------------------------------------------------------------------------
    ("crossbatch: an unpinned divergence from a SHIPPED crop is accepted", "crossbatch", PROMOTE,
     "        if len(shapes) > 1 and pid not in CROSS_BATCH_DIVERGENCE:", "        if False:"),
    ("crossbatch: a converged pin is left standing as a dead exception", "crossbatch", PROMOTE,
     "        if len(shapes) == 1 and pid in CROSS_BATCH_DIVERGENCE:", "        if False:"),
    ("crossbatch: the anti-vacuity check is disabled", "crossbatch", PROMOTE,
     "    if not shared:", "    if False:"),
    ("crossbatch: the multi-crop id SET is not pinned", "crossbatch", PROMOTE,
     "    if shared != EXPECTED_SHARED_IDS:", "    if False:"),
    ("crossbatch: canonical is never consulted, only the batch", "crossbatch", PROMOTE,
     '    for c in data["crops"]:\n        if c["slug"] in CROPS:\n            continue',
     '    for c in []:\n        if c["slug"] in CROPS:\n            continue'),

    # ---- temps / vocab --------------------------------------------------------------------------
    ("temps: the temperature scan finds nothing", "temps", PROMOTE,
     "                    m = TEMP_FIGURE.search(r[f])", "                    m = None"),
    ("vocab: the ladder-vocabulary scan finds nothing", "vocab", PROMOTE,
     "                    m = LADDER_VOCAB.search(r[f])", "                    m = None"),

    # ---- materials ------------------------------------------------------------------------------
    ("materials: a material outside MATERIAL_OK is accepted", "materials", PROMOTE,
     "                    if m not in ok:", "                    if False:"),

    # ---- validate -------------------------------------------------------------------------------
    ("validate: an unknown method is accepted", "validate", PROMOTE,
     "                if m not in cm:", "                if False:"),
    ("validate: a forbidden method is accepted", "validate", PROMOTE,
     "                if m in FORBIDDEN_METHODS:", "                if False:"),
    ("validate: a duplicate method is accepted", "validate", PROMOTE,
     "                if m in seen:", "                if False:"),
    ("validate: a tier decrease is accepted", "validate", PROMOTE,
     "                if t < last:", "                if False:"),
    ("validate: applies_to incoherence is accepted", "validate", PROMOTE,
     '                if "any" not in applies and not _type_ok(p["type"], applies):',
     "                if False:"),
    ("validate: identical registers are accepted", "validate", PROMOTE,
     '                if r.get("note_beginner", "").strip() == r.get("note_seasoned", "").strip():',
     "                if False:"),
    ("validate: a missing rung note is accepted", "validate", PROMOTE,
     '                    if not (r.get(f) or "").strip():', "                    if False:"),
    ("validate: copy hygiene is not enforced", "validate", PROMOTE,
     "                    if bad:", "                    if False:"),
    ("validate: an empty ladder is accepted", "validate", PROMOTE,
     '            if not L:\n                raise SystemExit("REFUSED: %s/%s empty ladder"',
     '            if False:\n                raise SystemExit("REFUSED: %s/%s empty ladder"'),
    ("validate: a problem with no type is accepted", "validate", PROMOTE,
     '            if not p.get("type"):', "            if False:"),
    ("validate: the per-crop problem count is not pinned", "validate", PROMOTE,
     "        if len(probs) != EXPECTED_PROBLEMS[c]:", "        if False:"),
    ("validate: the per-crop rung count is not pinned", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[c]:", "        if False:"),
    ("validate: the TOTAL rung count is not pinned", "validate", PROMOTE,
     "    if rung_count(batch) != TOTAL_RUNGS:", "    if False:"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: the problem-set equality check is disabled", "blast", PROMOTE,
     "    if set(pre) != set(post):", "    if False:"),
    ("blast: a bystander crop may change", "blast", PROMOTE,
     "        if k[0] not in CROPS:", "        if False:"),
    ("blast: the touched count is not pinned", "blast", PROMOTE,
     "    if touched != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- catalog (main) -------------------------------------------------------------------------
    ("catalog: control_methods may be mutated by this batch", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: source_catalog may be mutated by this batch", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the base SHA is not enforced", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the ladders are never attached", PROMOTE,
            '                p["control_ladder"] = copy.deepcopy(o["control_ladder"])',
            '                _skip = copy.deepcopy(o["control_ladder"])')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    """Every anchor must match EXACTLY ONCE. An anchor matching zero times (typically because it
    spans Python implicit string concatenation) silently mutates nothing and reports SURVIVED for
    the wrong reason; an anchor matching twice edits a site nobody intended. PLA-138."""
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1], SENTINEL[2])]
    for label, f, old in rows:
        n = open(f).read().count(old)
        if n != 1:
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_batch19_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", STAGING_NAME)
    for fn in os.listdir(src_staging):
        if fn.startswith("out_"):
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "%s")' % STAGING_NAME,
        "STAGING = %r" % sandbox_staging, 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 19, sweet citrus")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails (the CLEAN fixture must pass).")
        return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print("HARNESS DEAD: %s SURVIVED." % label)
        return 1
    print("sentinel         : RED as required\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print("  SURVIVED  [%s] %s" % (family, label))
        else:
            caught += 1; fam[family][0] += 1
            print("  caught    [%s] %s" % (family, label))

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print("  %-11s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(MUTATIONS)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
