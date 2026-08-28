#!/usr/bin/env python3
"""Mutation harness for the trap_cropping mint (PLA-215).

THE SAFETY-BEARING HALF OF THIS METHOD IS THE TIMING, NOT THE PRACTICE. Trap cropping without the
removal step raises the local pest population and parks it beside the crop, so a sheet that
recommends it and understates the deadline is worse than no sheet at all. The `disclosure` family
attacks exactly that: empty the axis table, disable the check in `check` and again in `verify_post`,
drop the axis, and strip the sentence out of the shipped cautions. Each must be refused.

`contrast` attacks the reason this is a NEW KEY rather than a widening of `weed_host_control` or
`crop_rotation`. `scope` attacks the narrow applies_to and the cultural tier. `exclusion` attacks the
six problems that mention trap cropping and must never carry the rung, including the check that they
RESOLVE at all -- a typo'd slug would leave the backfill's refusal protecting nothing while green.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_trap_cropping.py")
PROMOTE = os.path.join(HERE, "promote_pla8_trap_cropping.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- disclosure: the removal deadline, which is what separates a trap from a nursery --------
    ("disclosure: missing_disclosures always reports nothing missing", "disclosure", PROMOTE,
     '    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()\n'
     '                  if not all(t in blob for t in toks))',
     '    return []'),
    # A TRUE emptying, not the `{} or {"_deadline": ...}` idiom this line used to carry. That idiom
    # is NOT inert -- `{}` is falsy so the second dict wins, and the renamed first key makes the
    # guard's lookup raise, which does redden the suite. But it renames one key rather than emptying
    # the table, so the LABEL was wrong and the injection weaker than it read. Emptied for real, the
    # disclosure requirement genuinely vanishes, which is the defect this line claims to inject.
    ("disclosure: the axis table is emptied", "disclosure", PROMOTE,
     'REQUIRED_DISCLOSURES = {\n    "deadline":  ("before eggs hatch",),',
     'REQUIRED_DISCLOSURES = {}\n_UNUSED_DISCLOSURES = {\n    "deadline":  ("before eggs hatch",),'),
    ("disclosure: the deadline axis drops out of the table", "disclosure", PROMOTE,
     '    "deadline":  ("before eggs hatch",),\n', ''),
    ("disclosure: the backfire axis drops out of the table", "disclosure", PROMOTE,
     '    "backfire":  ("works in reverse", "population"),\n', ''),
    ("disclosure: check stops requiring the disclosures", "disclosure", PROMOTE,
     '    miss = missing_disclosures(METHOD)\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: verify_post stops requiring them on the shipped entry", "disclosure", PROMOTE,
     '    miss = missing_disclosures(cm[KEY])\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: the cautions lose the UMass deadline sentence", "disclosure", PROMOTE,
     '        "The patch has to be pulled or treated before the pest breeds. UMass states it as a "\n'
     '        "deadline, that the trap crop must receive an insecticide application or be mechanically "\n'
     '        "destroyed before eggs hatch, and UF/IFAS that once the insects have established on the "\n'
     '        "trap you have to eradicate them to keep them from moving on to the main crop.",',
     '        "The patch has to be pulled or treated at some point after the pest arrives.",'),
    ("disclosure: the cautions lose the backfire warning", "disclosure", PROMOTE,
     '        "A loaded trap left standing works in reverse, raising the local pest population and "\n'
     '        "holding it next to the crop it was meant to protect. If the patch will not be tended and "\n'
     '        "removed on schedule, this is not the rung to choose.",',
     '        "A trap works best when it is tended.",'),

    # ---- contrast: why this is a new key rather than a widening ---------------------------------
    ("contrast: the contrast table is emptied", "contrast", PROMOTE,
     'REQUIRED_CONTRASTS = ("weeds that host", "crop rotation", "removes", "adds")',
     'REQUIRED_CONTRASTS = ()'),
    ("contrast: check stops requiring the distinctions", "contrast", PROMOTE,
     '    miss = missing_contrasts(METHOD)\n    if miss:',
     '    miss = []\n    if miss:'),
    ("contrast: verify_post stops requiring them", "contrast", PROMOTE,
     '    miss = missing_contrasts(cm[KEY])\n    if miss:',
     '    miss = []\n    if miss:'),
    ("contrast: best_use stops naming crop rotation", "contrast", PROMOTE,
     '        "lower the pressure; this deliberately ADDS one to concentrate it. Distinct from crop "\n'
     '        "rotation, which moves the crop away from the problem; this leaves the crop where it is "',
     '        "lower the pressure; this deliberately ADDS one to concentrate it. Unlike other "\n'
     '        "approaches, which move the crop away from the problem; this leaves the crop where it is "'),

    # ---- scope: what the method is allowed to reach ---------------------------------------------
    ("scope: the applies_to check is disabled in check", "scope", PROMOTE,
     '    if METHOD["applies_to"] != ["insect_chewing", "insect_general"]:', '    if False:'),
    ("scope: the applies_to check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["applies_to"] != ["insect_chewing", "insect_general"]:', '    if False:'),
    ("scope: applies_to widens to soft-bodied insects nothing was read for", "scope", PROMOTE,
     '    "applies_to": ["insect_chewing", "insect_general"],',
     '    "applies_to": ["insect_chewing", "insect_general", "insect_soft_bodied"],'),
    ("scope: the tier check is disabled in check", "scope", PROMOTE,
     '    if METHOD["tier"] != "cultural":', '    if False:'),
    ("scope: the tier check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["tier"] != "cultural":', '    if False:'),
    ("scope: the tier becomes physical, misordering every ladder", "scope", PROMOTE,
     '    "name": "Trap cropping",\n    "tier": "cultural",',
     '    "name": "Trap cropping",\n    "tier": "physical",'),

    # ---- exclusion: the six that must never carry the rung --------------------------------------
    ("exclusion: the resolve check is disabled", "exclusion", PROMOTE,
     '    for slug, ident in EXCLUSIONS:\n        if find_problem(data, slug, ident) is None:',
     '    for slug, ident in ():\n        if find_problem(data, slug, ident) is None:'),
    ("exclusion: nasturtium is typo'd and silently protects nothing", "exclusion", PROMOTE,
     '    ("nasturtium", "Aphids"),', '    ("nasturtium", "Aphid"),'),
    # NOT `EXCLUSIONS = () or (...)`. An empty tuple is FALSY, so `() or (...)` evaluates straight
    # back to the original and the injection is inert -- it survived the first run for that reason,
    # and the same broken shape sits in two shipped harnesses in this repo (batch 10 hit it too).
    # This binds the empty tuple for real and parks the original under an unused name.
    ("exclusion: the list is emptied", "exclusion", PROMOTE,
     'EXCLUSIONS = (\n    ("radish", "flea-beetles"),',
     'EXCLUSIONS = ()\n_UNUSED_EXCLUSIONS = (\n    ("radish", "flea-beetles"),'),
    ("exclusion: verify_post stops checking the six", "exclusion", PROMOTE,
     '    for slug, ident in EXCLUSIONS:\n        p = find_problem(data, slug, ident)',
     '    for slug, ident in ():\n        p = find_problem(data, slug, ident)'),
    ("exclusion: find_problem stops matching by name, so the unladdered two vanish", "exclusion",
     PROMOTE,
     '                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):',
     '                if isinstance(p, dict) and ident == p.get("id"):'),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    if KEY in data["control_methods"]:',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n'
     '    if KEY in data["control_methods"]:'),
    ("blast: the mint-only rung check is disabled", "blast", PROMOTE,
     '    landed = rungs_of(data, KEY)\n    if landed:', '    landed = []\n    if landed:'),
    ("blast: verify_post stops comparing the added method set", "blast", PROMOTE,
     '    if added != {KEY}:', '    if False:'),
    ("blast: verify_post stops noticing a dropped method", "blast", PROMOTE,
     '    if set(pre["methods"]) - set(post["methods"]):', '    if False:'),
    ("blast: verify_post stops checking existing methods", "blast", PROMOTE,
     '        if post["methods"][k] != before:', '        if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: verify_post stops checking crops", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),

    # ---- hygiene / mechanics ---------------------------------------------------------------------
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '    for s in prose_of(METHOD):', '    for s in ():'),
    ("hygiene: the absolute-claim family leaves the check", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):\n'
     '        return "absolute claim"',
     '    if False:\n        return "absolute claim"'),
    ("hygiene: the British-spelling family leaves the check", "hygiene", PROMOTE,
     '    for w in BRITISH:\n        if re.search(rf"\\b{w}\\b", s, re.I):',
     '    for w in ():\n        if re.search(rf"\\b{w}\\b", s, re.I):'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))',
            '    _skip = json.loads(json.dumps(METHOD))')


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
    wd = tempfile.mkdtemp(prefix="mutate_trapcrop_")
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
    print("MUTATION HARNESS -- trap_cropping mint, the catalog's 59th method")
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
