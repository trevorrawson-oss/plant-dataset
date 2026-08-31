#!/usr/bin/env python3
"""Mutation harness for the batch-18 promote (PLA-215).

Families: `schema` attacks the full-schema premise and the not-already-laddered premise. `types`
attacks the TWO-SIDED type rule -- citrus is MIXED, so the preservation half (an already-fine type
is never silently rewritten) is attacked separately from the three pinned upgrades and from the
pinned SET. `ids` attacks the convention table, the four refusals and the single reuse anchor.
`sooty` attacks the guard the batch exists for, in all five of its branches including the one that
refuses a base predating the mint. `ants` attacks the mechanism claim -- ordering, the tier the
ordering rests on, and its anti-vacuity check. `divergence` attacks the shared-id ruling in all
four directions, including the dead-exception branch that fires when a permitted divergence
CONVERGES. `temps` and `vocab` attack the two copy scans. `materials`, `validate`, `blast` and
`mechanics` as in batches 13-17. `catalog` attacks the two refusals that live in main() rather than
in check(); batch 17's suite could not reach these, because comparing serializations from the suite
tests the outcome without driving the promote's own guard.

Every disabled branch has a driver in the suite asserting its ONE specific message, so a mutation
cannot be "caught" by an unrelated earlier check and score a false positive.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch18.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch18.py")
STAGING_NAME = "pla8_batch18_acid_citrus"
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
    ("types: a non-enum fine type is accepted", "types", PROMOTE,
     "                if post not in _TYPE_TARGETS:", "                if False:"),
    ("types: an already-fine type may be SILENTLY REWRITTEN", "types", PROMOTE,
     "                    if post != pre:", "                    if False:"),
    ("types: an unpinned fourth upgrade rides along", "types", PROMOTE,
     "                if (c, name) not in EXPECTED_TYPE_UPGRADES:", "                if False:"),
    ("types: a pinned upgrade may land on the wrong fine type", "types", PROMOTE,
     "                if EXPECTED_TYPE_UPGRADES[(c, name)] != (pre, post):",
     "                if False:"),
    ("types: the coarse-typed SET is not pinned", "types", PROMOTE,
     "    if got != set(EXPECTED_TYPE_UPGRADES):", "    if False:"),

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

    # ---- sooty ----------------------------------------------------------------------------------
    ("sooty: sooty-mold may be unladdered again", "sooty", PROMOTE,
     '            if not L:\n                raise SystemExit("REFUSED: %s/sooty-mold is unladdered again',
     '            if False:\n                raise SystemExit("REFUSED: %s/sooty-mold is unladdered again'),
    ("sooty: the ant_exclusion rung may be substituted away", "sooty", PROMOTE,
     '            if "ant_exclusion" not in [r["method"] for r in L]:', "            if False:"),
    ("sooty: sooty-mold may be retyped off fungal", "sooty", PROMOTE,
     '            if p.get("type") != "fungal":', "            if False:"),
    ("sooty: the anti-vacuity check is disabled", "sooty", PROMOTE,
     "    if not found:", "    if False:"),
    ("sooty: a base predating the mint is accepted", "sooty", PROMOTE,
     '    if "ant_exclusion" not in cm:', "    if False:"),

    # ---- ants -----------------------------------------------------------------------------------
    ("ants: ant_exclusion may be re-tiered off physical", "ants", PROMOTE,
     '            if cm["ant_exclusion"]["tier"] != "physical":', "            if False:"),
    ("ants: the exclusion may follow the predators it enables", "ants", PROMOTE,
     '            if "beneficial_predators" in ms and ms.index("ant_exclusion") > ms.index(',
     "            if False and ms.index("),
    ("ants: the anti-vacuity check is disabled", "ants", PROMOTE,
     "    if seen == 0:", "    if False:"),

    # ---- divergence -----------------------------------------------------------------------------
    ("divergence: a converged pin is left standing as a dead exception", "divergence", PROMOTE,
     "            if pid in PERMITTED_DIVERGENCE:", "            if False:"),
    ("divergence: an unpermitted shared-id divergence is accepted", "divergence", PROMOTE,
     "        if allowed is None:", "        if False:"),
    ("divergence: divergence beyond the permitted rung is accepted", "divergence", PROMOTE,
     "        if [m for m in a if m != allowed] != [m for m in b if m != allowed]:",
     "        if False:"),
    ("divergence: the anti-vacuity check is disabled", "divergence", PROMOTE,
     "    if checked == 0:", "    if False:"),

    # ---- temps ----------------------------------------------------------------------------------
    ("temps: the temperature scan finds nothing", "temps", PROMOTE,
     "                    m = TEMP_FIGURE.search(r[f])", "                    m = None"),

    # ---- vocab ----------------------------------------------------------------------------------
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

# The sentinel disables the promote's actual work. If the suite still passes with the ladders never
# attached, the harness is grading nothing and every "caught" above is meaningless.
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
    wd = tempfile.mkdtemp(prefix="mutate_batch18_")
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
    print("MUTATION HARNESS -- PLA-8 batch 18, acid citrus")
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
