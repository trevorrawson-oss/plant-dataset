#!/usr/bin/env python3
"""Mutation harness for the chlorothalonil backfill (PLA-215).

THIS IS THE ONLY PROMOTE IN THE ARC THAT AMENDS CERTIFIED, SHIPPED CROPS, and it puts the catalog's
heaviest method on nine of their ladders. Two families carry it.

`premise` attacks the fact that licenses three crops to share one rung: they share the SENTENCE the
rung restates. Drift one crop's sentence, empty the group table, disable the check -- each must be
refused, because a crop whose source says something else needs its own rung rather than a copy of
somebody's.

`jump` attacks the shape a reader would notice. Three cucurbit anthracnose ladders will run
cultural -> conventional with nothing between, because their prose names no softer spray. That is
honest, but it is also indistinguishable from three forgotten rungs unless the prose says so and a
guard confines it. These mutations let the jump spread to the other six, remove the sentence that
explains it, and disable the confinement.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_chlorothalonil_backfill.py")
PROMOTE = os.path.join(HERE, "promote_pla8_chlorothalonil_backfill.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise: three crops share a rung only because they share the sentence -----------------
    ("premise: check_shared_sentence is disabled", "premise", PROMOTE,
     '    problem_ = check_shared_sentence(by)\n    if problem_:\n        return problem_',
     '    problem_ = None\n    if problem_:\n        return problem_'),
    ("premise: the phrase test is inverted so any sentence passes", "premise", PROMOTE,
     '            if phrase not in t:', '            if False:'),
    ("premise: group A's phrase weakens to a word every entry contains", "premise", PROMOTE,
     '    "A": (CUCURBITS, "downy-mildew", "copper or chlorothalonil"),',
     '    "A": (CUCURBITS, "downy-mildew", "the"),'),
    ("premise: group C's phrase drops the hedge it is anchored on", "premise", PROMOTE,
     '    "C": (BEANS, "anthracnose", "chlorothalonil can suppress it when started early"),',
     '    "C": (BEANS, "anthracnose", "chlorothalonil"),'),

    # ---- jump: the deliberate cultural -> conventional shape ------------------------------------
    ("jump: the jump-group top-rung check is disabled", "jump", PROMOTE,
     '        if g == JUMP_GROUP and top != "cultural":', '        if False:'),
    ("jump: the non-jump cultural-top check is disabled, letting it spread", "jump", PROMOTE,
     '        if g != JUMP_GROUP and top == "cultural":', '        if False:'),
    ("jump: verify_post stops confining the shape", "jump", PROMOTE,
     '    if sorted(jumps) != expected:', '    if False:'),
    ("jump: the confinement compares against everything rather than group B", "jump", PROMOTE,
     '    expected = sorted((s, GROUPS[JUMP_GROUP][1]) for s in GROUPS[JUMP_GROUP][0])',
     '    expected = sorted(jumps)'),
    ("jump: the prose stops saying the escalation skips three tiers", "jump", PROMOTE,
     '            "preventively: it goes on ahead of a wet spell rather than after spots show. Notice the "\n'
     '            "gap below it. There is no gentler spray listed for this disease on this crop, so the "',
     '            "preventively: it goes on ahead of a wet spell rather than after spots show. There is "\n'
     '            "no gentler spray listed for this disease on this crop, so the "'),

    # ---- hedge: what the sources qualify -----------------------------------------------------------
    ("hedge: the required-hedge table is emptied", "hedge", PROMOTE,
     'REQUIRED_HEDGES = {\n    "A": ("protectant only",),',
     'REQUIRED_HEDGES = {} or {\n    "_A": ("protectant only",),'),
    ("hedge: the hedge check is disabled", "hedge", PROMOTE,
     '        for h in REQUIRED_HEDGES[g]:\n            if h not in blob:', '        for h in ():\n            if h not in blob:'),
    ("hedge: group C stops saying the material only SUPPRESSES", "hedge", PROMOTE,
     '    "C": ("suppress", "started early", "mainstay"),', '    "C": ("started early", "mainstay"),'),
    ("hedge: group C stops saying cultural control is the mainstay", "hedge", PROMOTE,
     '            "early; the source calls cultural control the mainstay for a home crop, so this rung "',
     '            "early; this rung "'),

    # ---- placement: where the rung lands ------------------------------------------------------------
    ("placement: the rung is INSERTED first instead of appended", "placement", PROMOTE,
     '        p["control_ladder"].append({"method": METHOD,', '        p["control_ladder"].insert(0, {"method": METHOD,'),
    ("placement: verify_post stops requiring the rung last", "placement", PROMOTE,
     '        if ms[-1] != METHOD:', '        if False:'),
    ("placement: verify_post stops counting the rung", "placement", PROMOTE,
     '        if ms.count(METHOD) != 1:', '        if False:'),
    ("placement: verify_post stops checking tier monotonicity", "placement", PROMOTE,
     '        if ranks != sorted(ranks):', '        if False:'),
    ("placement: verify_post stops checking which group's rung landed", "placement", PROMOTE,
     '        if (r["note_beginner"], r["note_seasoned"]) != (RUNGS[g]["note_beginner"],',
     '        if False and (r["note_beginner"], r["note_seasoned"]) != (RUNGS[g]["note_beginner"],'),
    ("placement: the already-carries refusal is disabled", "placement", PROMOTE,
     '        if METHOD in ms:\n            return f"{slug}/{pid} already carries {METHOD}"',
     '        if METHOD in ms:\n            pass'),
    ("placement: the mint-landed precondition is disabled", "placement", PROMOTE,
     '    if METHOD not in cm:\n        return f"{METHOD} is not in the catalog; the mint must land first"',
     '    if METHOD not in cm:\n        pass'),
    ("placement: the method-tier precondition is disabled", "placement", PROMOTE,
     '    if cm[METHOD]["tier"] != "conventional":', '    if False:'),

    # ---- blast --------------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    by = {c.get("slug"): c for c in data["crops"]}',
     'def apply_to(data):\n    by = {c.get("slug"): c for c in data["crops"]}\n    by["tomatillo"]["name"] = "MUTATED"'),
    ("blast: verify_post stops checking bystander crops", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: verify_post stops comparing the crop set", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: verify_post stops checking control_methods", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),

    # ---- hygiene / mechanics --------------------------------------------------------------------------
    ("hygiene: the register-identity check is disabled", "hygiene", PROMOTE,
     '        if rung["note_beginner"] == rung["note_seasoned"]:', '        if False:'),
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '        for s in (rung["note_beginner"], rung["note_seasoned"]):', '        for s in ():'),
    ("hygiene: the British-spelling family leaves the check", "hygiene", PROMOTE,
     '    for w in BRITISH:\n        if re.search(rf"\\b{w}\\b", s, re.I):', '    for w in ():\n        if re.search(rf"\\b{w}\\b", s, re.I):'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '        p["control_ladder"].append({"method": METHOD,', '        _skip = ({"method": METHOD,')


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
    wd = tempfile.mkdtemp(prefix="mutate_chlbf_")
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
    print("MUTATION HARNESS -- chlorothalonil backfill, 9 rungs on 6 certified crops")
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
