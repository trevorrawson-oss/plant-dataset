#!/usr/bin/env python3
"""Mutation harness for the wet_foliage_discipline powdery-mildew exception (PLA-215).

TWO FAMILIES PULL IN OPPOSITE DIRECTIONS AND BOTH MATTER.

`exception` attacks the fix being too weak: emptied token list, a vaguer sentence, the check
disabled. A caution that says "this does not suit every foliar disease" satisfies an is-it-there
check and leaves the next authoring pass exactly where it was.

`overcorrect` attacks the fix being too strong. The tempting move is to drop `fungal_foliar` from
`applies_to`, which would "fix" powdery mildew by breaking ascochyta blight and anthracnose -- the
splash-dispersed foliar fungi this method was minted for, and the use it correctly keeps on the very
same pea crops. Guarding a correction against going too far is as necessary as guarding it against
not going far enough, and this arc has no prior family for it.

`brief` is the family that would have caught the version of this fix nearly shipped. Until
`603f4f8` the authoring brief emitted only `applies_to` and a 150-character slice of `best_use`, so
all 41 caution strings in the catalog were invisible. These mutations break the emission and confirm
the suite notices, because a caution nothing reads is not a guard.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_wet_foliage_pm_exception.py")
PROMOTE = os.path.join(HERE, "promote_pla8_wet_foliage_pm_exception.py")
BATCH = os.path.join(HERE, "ladder_batch.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- exception: the fix being too weak -------------------------------------------------------
    ("exception: the required-token list is emptied", "exception", PROMOTE,
     'MUST_CARRY = ("powdery mildew", "free water", "airflow")', 'MUST_CARRY = ()'),
    ("exception: the token check is disabled", "exception", PROMOTE,
     '    for need in MUST_CARRY:\n        if need not in low:', '    for need in ():\n        if need not in low:'),
    ("exception: the caution stops naming the pathogen", "exception", PROMOTE,
     'CAUTION = ("Powdery mildew is the exception and this does not act on it: USU notes that powdery "',
     'CAUTION = ("Some diseases are an exception and this does not act on them: USU notes that some "'),
    ("exception: the caution stops naming what does the work instead", "exception", PROMOTE,
     '"few hours, so on that one disease it is airflow and spacing that do the work here, not "\n'
     '           "staying out of a wet planting.")',
     '"few hours.")'),
    ("exception: the already-present refusal is disabled", "exception", PROMOTE,
     '    if CAUTION in existing:', '    if False:'),
    ("exception: apply_to REPLACES the cautions instead of appending", "exception", PROMOTE,
     '    m["cautions"] = list(m["cautions"]) + [CAUTION]', '    m["cautions"] = [CAUTION]'),

    # ---- overcorrect: the fix going further than the evidence ------------------------------------
    ("overcorrect: applies_to is narrowed to bacterial only", "overcorrect", PROMOTE,
     'FROZEN_APPLIES_TO = ["bacterial", "fungal_foliar"]', 'FROZEN_APPLIES_TO = ["bacterial"]'),
    ("overcorrect: the frozen-target guard is disabled in check", "overcorrect", PROMOTE,
     '    problem = applies_to_frozen(cm)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),
    ("overcorrect: the frozen-target guard is disabled in verify_post", "overcorrect", PROMOTE,
     '    problem = applies_to_frozen(cm)\n    if problem:\n        return "post: " + problem',
     '    problem = None\n    if problem:\n        return "post: " + problem'),
    ("overcorrect: apply_to drops fungal_foliar while adding the caution", "overcorrect", PROMOTE,
     '    m = data["control_methods"][KEY]\n    m["cautions"] = list(m["cautions"]) + [CAUTION]',
     '    m = data["control_methods"][KEY]\n    m["applies_to"] = ["bacterial"]\n    m["cautions"] = list(m["cautions"]) + [CAUTION]'),

    # ---- brief: a caution nothing reads is not a guard -------------------------------------------
    ("brief: cautions stop being emitted into the authoring brief", "brief", BATCH,
     '            for c in (v.get("cautions") or []):\n                lines.append(f"      CAUTION: {c}")',
     '            for c in ():\n                lines.append(f"      CAUTION: {c}")'),
    ("brief: best_use goes back to the 150-char truncation", "brief", BATCH,
     '            lines.append(f"      MEANS: {v[\'best_use\']}")',
     '            lines.append(f"      MEANS: {v[\'best_use\'][:150]}")'),

    # ---- blast --------------------------------------------------------------------------------------
    ("blast: a crop is touched", "blast", PROMOTE,
     '    anchors = dict(m["anchoring_urls"])',
     '    data["crops"][0]["name"] = "MUTATED"\n    anchors = dict(m["anchoring_urls"])'),
    ("blast: a bystander method is edited", "blast", PROMOTE,
     '    if SOURCE not in m["sources"]:',
     '    data["control_methods"]["airflow_spacing"]["best_use"] += " x"\n    if SOURCE not in m["sources"]:'),
    ("blast: verify_post stops checking untouched methods", "blast", PROMOTE,
     '        if post["methods"][k] != b:', '        if False:'),
    ("blast: verify_post stops checking crops", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),
    ("blast: verify_post stops noticing a dropped existing caution", "blast", PROMOTE,
     '        if c not in m["cautions"]:', '        if False:'),
    ("blast: verify_post stops noticing another field moving", "blast", PROMOTE,
     '        if m.get(f) != v:', '        if False:'),
    ("blast: the anchor-overwrite refusal is disabled in apply", "blast", PROMOTE,
     '    if SOURCE in anchors:\n        raise AssertionError', '    if False:\n        raise AssertionError'),

    # ---- hygiene / mechanics --------------------------------------------------------------------------
    ("hygiene: the hygiene check is disabled", "hygiene", PROMOTE,
     '    bad = hygiene(CAUTION)\n    if bad:', '    bad = hygiene(CAUTION)\n    if False:'),
    ("hygiene: the absolutes family leaves the regex", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '    m["cautions"] = list(m["cautions"]) + [CAUTION]', '    pass')


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
    wd = tempfile.mkdtemp(prefix="mutate_pmx_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, BATCH):
        s = open(f).read()
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- wet_foliage_discipline powdery-mildew exception")
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
        print(f"  {k:12s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
