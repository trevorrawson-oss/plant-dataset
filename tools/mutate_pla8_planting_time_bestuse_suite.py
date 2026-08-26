#!/usr/bin/env python3
"""Mutation harness for the planting_time_avoidance best_use correction (PLA-215).

THE `coherence` FAMILY IS LOAD-BEARING AND IT IS NEW TO THIS ARC. Every guard family this repo has
built so far checks that prose CONTAINS what the author said it should. This one checks that the
author's intentions do not contradict each other: a sheet may not demand a single generation as its
criterion while naming, as its own documented case, a pest its own cited source puts at three
generations a year. The r5 suite and its 43-injection harness were both green over exactly that
sentence, because both were asking the first question and the defect lived in the second.

THE `deletion` FAMILY exists because the cheap fix passes an absence check. Strip "one main
generation" and say nothing in its place and every criterion check goes quiet while the field ends
up vaguer than the one it replaced. So the replacement must positively carry the single flight, the
several generations, and the July-August window, and these mutations take each of those away.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_planting_time_bestuse.py")
PROMOTE = os.path.join(HERE, "promote_pla8_planting_time_bestuse.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- coherence: the defect class this promote exists to close ------------------------------
    ("coherence: the replacement keeps the single-generation criterion", "coherence", PROMOTE,
     'NEW = ("A pest whose damage falls in a predictable, locally published stretch of the season, on a "',
     'NEW = ("A pest with one main generation and a published local emergence window, on a "'),
    ("coherence: the criterion list is emptied, so nothing can be detected", "coherence", PROMOTE,
     'SINGLE_GEN_CRITERIA = (\n    "one main generation",', 'SINGLE_GEN_CRITERIA = (\n    "zzz_no_such_phrase",'),
    # NOTE: `for bad in SINGLE_GEN_CRITERIA: if bad in low:` appears TWICE (check and verify_post),
    # so both anchors carry their own `return` line. The preflight caught this as HARNESS DEAD
    # rather than silently mutating whichever came first, which is the point of it.
    ("coherence: the replacement-carries-criterion check is disabled", "coherence", PROMOTE,
     '    for bad in SINGLE_GEN_CRITERIA:\n        if bad in low:\n            return f"the replacement still carries',
     '    for bad in ():\n        if bad in low:\n            return f"the replacement still carries'),
    ("coherence: the other-fields check is disabled", "coherence", PROMOTE,
     '    for bad in SINGLE_GEN_CRITERIA:\n        if bad in others:', '    for bad in ():\n        if bad in others:'),
    ("coherence: verify_post stops re-checking the post state for the criterion", "coherence", PROMOTE,
     '    for bad in SINGLE_GEN_CRITERIA:\n        if bad in low:\n            return f"post:',
     '    for bad in ():\n        if bad in low:\n            return f"post:'),

    # ---- deletion: a fix that only removes ------------------------------------------------------
    ("deletion: MUST_CARRY is emptied, so a bare deletion would pass", "deletion", PROMOTE,
     'MUST_CARRY = ("several generations", "july and august", "single flight")', 'MUST_CARRY = ()'),
    ("deletion: the MUST_CARRY check is disabled", "deletion", PROMOTE,
     '    for need in MUST_CARRY:\n        if need not in low:', '    for need in ():\n        if need not in low:'),
    ("deletion: the replacement drops the several-generations case", "deletion", PROMOTE,
     '"in shape: the squash vine borer has a single flight to get behind, while the Mexican bean "\n'
     '       "beetle runs several generations a year whose damage still concentrates in July and August. "',
     '"in shape, and both are documented. "'),
    ("deletion: the replacement drops the single-flight half", "deletion", PROMOTE,
     '"in shape: the squash vine borer has a single flight to get behind, while the Mexican bean "',
     '"in shape: the squash vine borer is one case, while the Mexican bean "'),

    # ---- base / refusal -------------------------------------------------------------------------
    ("refusal: the base-text check is disabled, so it would run on any base", "refusal", PROMOTE,
     '    if m.get(FIELD) != OLD:', '    if False:'),

    # ---- blast -----------------------------------------------------------------------------------
    ("blast: a crop is touched during the correction", "blast", PROMOTE,
     'def apply_to(data):\n    data["control_methods"][KEY][FIELD] = NEW',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    data["control_methods"][KEY][FIELD] = NEW'),
    ("blast: a second field on the same method is edited", "blast", PROMOTE,
     '    data["control_methods"][KEY][FIELD] = NEW\n    return 1',
     '    data["control_methods"][KEY]["how_it_works_beginner"] += " Extra."\n    data["control_methods"][KEY][FIELD] = NEW\n    return 1'),
    ("blast: verify_post stops comparing the method set", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', '    if False:'),
    ("blast: verify_post stops checking untouched methods", "blast", PROMOTE,
     '        if post["methods"][k] != before:', '        if False:'),
    ("blast: verify_post stops checking crops", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: verify_post stops noticing a second field moving", "blast", PROMOTE,
     '        if m.get(f) != v:', '        if False:'),

    # ---- hygiene / mechanics ---------------------------------------------------------------------
    ("hygiene: the hygiene check is disabled", "hygiene", PROMOTE,
     '    bad = hygiene(NEW)\n    if bad:', '    bad = hygiene(NEW)\n    if False:'),
    ("hygiene: the absolutes family leaves the regex", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            'def apply_to(data):\n    data["control_methods"][KEY][FIELD] = NEW\n    return 1',
            'def apply_to(data):\n    return 1')


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
    wd = tempfile.mkdtemp(prefix="mutate_ptbu_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read()
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- planting_time_avoidance best_use correction")
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
