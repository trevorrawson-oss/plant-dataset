#!/usr/bin/env python3
"""Mutation harness for the disease_escape_sowing backfill (PLA-215).

`premise` attacks the verified-in-canonical premises: every target's prose states the escape and
names its disease, and fava's root-rots entry carries the cold-seedbed warning its rung attributes
to it. `distinct` attacks the escape-sentence correspondence in both directions. `placement`
attacks the exact positions (after resistant_varieties on six, the front on fava) and tier
monotonicity. `contract` attacks the attribution, the cautions pointer and the register split.
`exclusion` attacks the four scan matches, spinach's damping-off above all. `blast` attacks the
whole-roster containment.

Every disabled branch has a driver asserting its ONE specific message; no hedged ORs.
Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_disease_escape_backfill.py")
PROMOTE = os.path.join(HERE, "promote_pla8_disease_escape_backfill.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise: the rung restates the crop's own prose, verified in canonical ----------------
    ("premise: the escape-premise loop runs over nothing", "premise", PROMOTE,
     '    for slug, pid, _after, word in TARGETS:', '    for slug, pid, _after, word in ():'),
    ("premise: escape_sentences invents a hit when the prose has none", "premise", PROMOTE,
     '    return out\n\n\ndef check_escape_premise(by):',
     '    return out or ["sow early stub rust mildew"]\n\n\ndef check_escape_premise(by):'),
    ("premise: the disease-word check is disabled", "premise", PROMOTE,
     '        if not any(word in s.lower() for s in sents):', '        if False:'),
    ("premise: the fava counter-exposure check is disabled", "premise", PROMOTE,
     '    if "cold" not in blob or "sow" not in blob:', '    if False:'),

    # ---- distinct: identical escapes <-> identical rungs, both directions -----------------------
    ("distinct: the correspondence loop runs over nothing", "distinct", PROMOTE,
     '    for i, (s1, p1) in enumerate(rows):', '    for i, (s1, p1) in enumerate(()):'),
    ("distinct: the forked-rung direction is disabled", "distinct", PROMOTE,
     '            if same_escape and not same_rung:', '            if False:'),
    ("distinct: the copied-rung direction is disabled", "distinct", PROMOTE,
     '            if same_rung and not same_escape:', '            if False:'),

    # ---- placement ------------------------------------------------------------------------------
    ("placement: insert_index stops requiring the opening-rung premise", "placement", PROMOTE,
     '    if ms.index(after) != 0:', '    if False:'),
    ("placement: verify_post stops checking the landing index", "placement", PROMOTE,
     '        if idx != want:', '        if False:'),
    ("placement: verify_post stops checking tier monotonicity", "placement", PROMOTE,
     '        if ranks != sorted(ranks):', '        if False:'),
    ("placement: verify_post stops counting duplicate rungs", "placement", PROMOTE,
     '        if ms.count(METHOD) != 1:', '        if False:'),
    ("placement: the rung text landing check is disabled", "placement", PROMOTE,
     '        if (r["note_beginner"], r["note_seasoned"]) != (wantr["note_beginner"],\n'
     '                                                        wantr["note_seasoned"]):',
     '        if False:'),

    # ---- contract: attribution, cautions pointer, registers -------------------------------------
    ("contract: the attribution check is disabled", "contract", PROMOTE,
     '        if ATTRIBUTION not in blob:', '        if False:'),
    ("contract: the cautions-pointer check is disabled", "contract", PROMOTE,
     '        if CAUTIONS_POINTER not in blob:', '        if False:'),
    ("contract: the identical-registers check is disabled", "contract", PROMOTE,
     '        if rung["note_beginner"] == rung["note_seasoned"]:', '        if False:'),

    # ---- exclusion ------------------------------------------------------------------------------
    ("exclusion: check's resolve loop runs over nothing", "exclusion", PROMOTE,
     '    for slug, ident, reason in EXCLUSIONS:\n'
     '        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n'
     '            return (f"exclusion',
     '    for slug, ident, reason in ():\n'
     '        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n'
     '            return (f"exclusion'),
    ("exclusion: verify_post's refusal loop runs over nothing", "exclusion", PROMOTE,
     '    for slug, ident, reason in EXCLUSIONS:\n'
     '        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n'
     '            return f"post: exclusion',
     '    for slug, ident, reason in ():\n'
     '        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n'
     '            return f"post: exclusion'),
    ("exclusion: spinach is typo'd and silently protects nothing", "exclusion", PROMOTE,
     '    ("spinach", "damping-off",', '    ("spinach", "damping-offf",'),
    # A REAL rebinding: `() or (...)` would evaluate straight back to the original.
    ("exclusion: the list is emptied", "exclusion", PROMOTE,
     'EXCLUSIONS = (\n    ("spinach",',
     'EXCLUSIONS = ()\n_UNUSED_EXCLUSIONS = (\n    ("spinach",'),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    by = {c.get("slug"): c for c in data["crops"]}',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n'
     '    by = {c.get("slug"): c for c in data["crops"]}'),
    ("blast: the landed-set check is disabled", "blast", PROMOTE,
     '    if sorted(landed) != expected:', '    if False:'),
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: the bystander value check is disabled", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: the bystander skip widens to every crop", "blast", PROMOTE,
     '        if slug in CROPS:\n            continue', '        if True:\n            continue'),
    ("blast: verify_post stops checking control_methods", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),

    # ---- content: a shipped text drifts; the POST pin is the guard for verbatim texts ----------
    ("content: the corn rung loses its cold-trade sentence", "content", PROMOTE,
     '        "starts with. The one limit is the soil itself, since corn seed rots in cold, wet "\n'
     '        "ground; this method\'s cautions carry the soil temperatures to wait for.",',
     '        "starts with; see this method\'s cautions for more.",'),

    # ---- hygiene / mechanics --------------------------------------------------------------------
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '        for s in (rung["note_beginner"], rung["note_seasoned"]):', '        for s in ():'),
    ("hygiene: the absolute-claim family leaves the check", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):\n'
     '        return "absolute claim"',
     '    if False:\n        return "absolute claim"'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '        lad.insert(i, {"method": METHOD,',
            '        _skip = (i, {"method": METHOD,')


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
    wd = tempfile.mkdtemp(prefix="mutate_descape_bf_")
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
    print("MUTATION HARNESS -- disease_escape_sowing backfill, 7 rungs on 7 certified crops")
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
