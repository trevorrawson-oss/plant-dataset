#!/usr/bin/env python3
"""Mutation harness for PLA-8 batch 5, the three beans (PLA-215).

THE `premise` FAMILY IS WHAT THIS BATCH ADDS OVER BATCH 4, and it is the one worth reading. Copying
one crop's ladders onto another is licensed by exactly one fact: their SOURCE prose is byte-identical
in order. Batch 4 asserted that by comparing the two STAGED files, which proves a propagation
happened and proves nothing about whether it was allowed. The premise lives in canonical, so these
mutations attack it there: disable the check, weaken the field set it compares, and break each of
its two directions in turn. A promote that will happily propagate over a premise that has quietly
expired is worse than one that never checked, because the green reads as verification.

THE `readfix` FAMILY carries the subtlest guard in the batch. `off_season_tillage` and
`garden_sanitation` are both cultural, both legal on an insect, and both plausible readings of "work
crop debris into the soil". Only the METHOD MEANING separates them, no gate can see it, and two
independent authoring passes split on it. The guard names the key that may not appear.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch5.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch5.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise: the fact that licenses the propagation, checked in canonical ------------------
    ("premise: check_twin_premise is disabled entirely", "premise", PROMOTE,
     '    problem = check_twin_premise(by)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),
    ("premise: the twin-mismatch branch is disabled", "premise", PROMOTE,
     '    if a != b:\n        bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]',
     '    if False:\n        bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]'),
    ("premise: the sibling-identical branch is disabled", "premise", PROMOTE,
     '    c = prose_signature(by[SIBLING])\n    if c == a:', '    c = prose_signature(by[SIBLING])\n    if False:'),
    ("premise: the compared field set shrinks to the problem name", "premise", PROMOTE,
     'PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",',
     'PROSE_FIELDS = ("name",   "symptoms_beginner_X", "symptoms_seasoned_X", "cause_beginner_X", "cause_seasoned_X",'),
    ("premise: the premise includes the field the promote writes (self-referential)", "premise",
     PROMOTE, '                "prevention_seasoned", "severity", "sources")',
     '                "prevention_seasoned", "severity", "sources", "control_ladder")'),

    # ---- grouping: the staged files carry the premise forward -----------------------------------
    ("grouping: check_grouping is disabled entirely", "grouping", PROMOTE,
     '    for problem in (check_grouping(batch), check_read_fixes(batch, by), check_r5_is_used(batch)):',
     '    for problem in (None, check_read_fixes(batch, by), check_r5_is_used(batch)):'),
    ("grouping: the twin-identity branch is disabled", "grouping", PROMOTE,
     '    if dg[TWIN[0]] != dg[TWIN[1]]:', '    if False:'),
    ("grouping: the sibling-propagation branch is disabled", "grouping", PROMOTE,
     '    if dg[SIBLING] == dg[TWIN[0]]:', '    if False:'),
    ("grouping: staged() propagates the twin over the sibling", "grouping", PROMOTE,
     '    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}',
     '    _b = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}\n'
     '    _b[SIBLING] = _b[TWIN[0]]\n    return _b'),

    # ---- readfix: the four corrections and the one correct divergence --------------------------
    ("readfix: check_read_fixes is disabled entirely", "readfix", PROMOTE,
     '    for problem in (check_grouping(batch), check_read_fixes(batch, by), check_r5_is_used(batch)):',
     '    for problem in (check_grouping(batch), None, check_r5_is_used(batch)):'),
    # NOTE: these guards exist in BOTH check_read_fixes and verify_post and differ only by
    # indentation, so a bare anchor matched twice. Preflight exited HARNESS DEAD rather than
    # mutating whichever came first, and each anchor now carries its own return line.
    ("readfix: the off_season_tillage refusal is disabled in check", "readfix", PROMOTE,
     '    if "off_season_tillage" in ms:\n        return (f"{SIBLING}/{MBB} carries off_season_tillage',
     '    if False:\n        return (f"{SIBLING}/{MBB} carries off_season_tillage'),
    ("readfix: the off_season_tillage refusal is disabled in verify_post", "readfix", PROMOTE,
     '            if "off_season_tillage" in ms:\n                return f"post:',
     '            if False:\n                return f"post:'),
    ("readfix: the garden_sanitation-present check is disabled", "readfix", PROMOTE,
     '    if "garden_sanitation" not in ms:', '    if False:'),
    ("readfix: the anthracnose ordering check is disabled", "readfix", PROMOTE,
     '        if not (ma.index("garden_sanitation") < ma.index("water_at_the_base")):',
     '        if False:'),
    ("readfix: the root-rot ordering check is disabled", "readfix", PROMOTE,
     '        if not (mr.index("sound_sowing_practice") < mr.index("improve_drainage")):',
     '        if False:'),
    ("readfix: the root-injury token list is emptied", "readfix", PROMOTE,
     'ROOT_INJURY_TOKENS = ("damage the roots", "root injury")', 'ROOT_INJURY_TOKENS = ()'),
    ("readfix: the wasp-on-twin check is disabled", "readfix", PROMOTE,
     '        if "augmentative_release" not in mt:', '        if False:'),
    ("readfix: the wasp-on-sibling check is disabled in check", "readfix", PROMOTE,
     '    if "augmentative_release" in ms:\n        return (f"{SIBLING}/{MBB} gained augmentative_release',
     '    if False:\n        return (f"{SIBLING}/{MBB} gained augmentative_release'),
    ("readfix: the wasp-on-sibling check is disabled in verify_post", "readfix", PROMOTE,
     '            if "augmentative_release" in ms:\n                return f"post: {slug}/{MBB} gained augmentative_release"',
     '            if False:\n                return f"post: {slug}/{MBB} gained augmentative_release"'),
    ("readfix: verify_post stops noticing the wasp dropped from the twin", "readfix", PROMOTE,
     '            if "augmentative_release" not in ms:\n                return f"post: {slug}/{MBB} lost augmentative_release"',
     '            if False:\n                return f"post: {slug}/{MBB} lost augmentative_release"'),
    ("readfix: the id guard reads the STAGED name again (batch 4's dead form)", "readfix", PROMOTE,
     '            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""',
     '            name = p.get("name") or ""'),
    ("ids: the id convention table is emptied", "ids", PROMOTE,
     'ID_CONVENTION = {"Aphids": "aphids", "Anthracnose": "anthracnose",',
     'ID_CONVENTION = {"Aphids_X": "aphids", "Anthracnose_X": "anthracnose",'),

    # ---- r5: the catalog round this batch justified ---------------------------------------------
    ("r5: check_r5_is_used is disabled entirely", "r5", PROMOTE,
     '    for problem in (check_grouping(batch), check_read_fixes(batch, by), check_r5_is_used(batch)):',
     '    for problem in (check_grouping(batch), check_read_fixes(batch, by), None):'),
    ("r5: the R5_USE table is emptied", "r5", PROMOTE,
     'R5_USE = {"mexican-bean-beetle": "planting_time_avoidance",', 'R5_USE = {} or {"_x": "_y",'),
    ("r5: the catalog-presence precondition is disabled", "r5", PROMOTE,
     '        if method not in cm:\n            return f"{method} is not in the catalog; the r5 round must land first"',
     '        if method not in cm:\n            pass'),

    # ---- shape ------------------------------------------------------------------------------------
    ("shape: the tier-monotonicity check is disabled", "shape", PROMOTE,
     '            if tiers != sorted(tiers):', '            if False:'),
    ("shape: the EMPTY-ladder check is disabled", "shape", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if not lad:\n                pass'),
    ("shape: the duplicate-method check is disabled", "shape", PROMOTE,
     '                if m in seen:', '                if False:'),
    ("shape: the applies_to coherence check is disabled", "shape", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("shape: the identical-registers check is disabled", "shape", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', '                if False:'),
    ("shape: the per-crop rung count check is disabled", "shape", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),

    # ---- blast --------------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()',
     'def apply_to(data):\n    {c.get("slug"): c for c in data["crops"]}["tomatillo"]["name"] = "MUTATED"\n    batch = staged()'),
    ("blast: verify_post stops comparing the crop set", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: verify_post stops checking bystander crops", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: verify_post stops checking control_methods", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: verify_post stops asserting the twin carries identical ladders", "blast", PROMOTE,
     '    if sig(TWIN[0]) != sig(TWIN[1]):', '    if False:'),
    ("blast: verify_post stops asserting the sibling is distinct", "blast", PROMOTE,
     '    if sig(SIBLING) == sig(TWIN[0]):', '    if False:'),

    # ---- mechanics ------------------------------------------------------------------------------------
    ("mechanics: sig() compares method KEYS again, batch 4's wrong cut", "mechanics", PROMOTE,
     '        return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])\n'
     '                            for r in p["control_ladder"]] for _, p in problems(by[s])],',
     '        return json.dumps([[(r["method"],)\n'
     '                            for r in p["control_ladder"]] for _, p in problems(by[s])],'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '                tgt["type"] = add["type"]\n                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])',
            '                tgt["type"] = add["type"]')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1], SENTINEL[2])]
    for label, f, old in rows:
        n = open(f).read().count(old)
        if n != 1:
            bad.append(f"  {n}x  {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_b5_")
    # The copied promote computes REPO from its OWN path, so STAGING would point into the sandbox
    # and resolve to nothing. Copy the staged batch in and repoint STAGING at it, which also means
    # a mutation may rewrite the staged JSON without touching the repo. (Batch 4's mechanism.)
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch5"), sandbox_staging)
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch5")',
        f'STAGING = {sandbox_staging!r}', 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 BATCH 5, the three beans")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails.")
        return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED.")
        return 1
    print("sentinel         : RED as required\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print(f"  {k:11s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
