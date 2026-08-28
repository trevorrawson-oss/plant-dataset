#!/usr/bin/env python3
"""Mutation harness for the trap_cropping backfill (PLA-215).

THIS PROMOTE AMENDS TEN LADDERS ON NINE CERTIFIED CROPS, which is the heaviest thing this arc does.
Four families carry it, and each attacks a different way the round could ship wrong advice.

`premise` attacks the split that licenses two different rung contracts: whether the CROP'S OWN prose
states the removal step. The seven harlequin entries do; the three flea beetle entries stop at the
diversion. Disable either direction of that check, or flip a crop's group, and the promote would let
a rung credit a source with advice it never gave.

`species` attacks the propagation defect. The ten name different trap plants and jalapeno's is
NASTURTIUM, not mustard. Let a rung name a plant its crop does not, and a copied rung ships.

`distinct` attacks the prose/rung correspondence in both directions -- a rung copied onto a crop
whose source differs, and the twins needlessly forked.

`exclusion` attacks the six that must never carry the rung, including the resolve check that keeps
the refusal from going vacuous, and the per-exclusion reason that keeps nasturtium's message from
being a generic one.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_trap_cropping_backfill.py")
PROMOTE = os.path.join(HERE, "promote_pla8_trap_cropping_backfill.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise: which crops' prose actually states the removal step ---------------------------
    ("premise: the whole premise pass is disabled", "premise", PROMOTE,
     '    for fn in (check_group_premise, check_species, check_rung_distinctness):',
     '    for fn in ():'),
    ("premise: the DESTROY_STATED direction is disabled", "premise", PROMOTE,
     '        if group == DESTROY_STATED and not states_removal:', '        if False:'),
    ("premise: the DIVERT_ONLY direction is disabled, the one that stops an invented recommendation",
     "premise", PROMOTE,
     '        if group == DIVERT_ONLY and states_removal:', '        if False:'),
    ("premise: the removal vocabulary is emptied, so nothing states a removal", "premise", PROMOTE,
     'REMOVAL_WORDS = ("destroy", "removal", "remove")', 'REMOVAL_WORDS = ()'),
    ("premise: the no-trap-sentence refusal is disabled", "premise", PROMOTE,
     '        if not sents:', '        if False:'),
    ("premise: jalapeno is relabelled DESTROY_STATED although its prose stops at the diversion",
     "premise", PROMOTE,
     '    ("jalapeno",    "flea-beetles",  DIVERT_ONLY),',
     '    ("jalapeno",    "flea-beetles",  DESTROY_STATED),'),
    ("premise: turnip is relabelled DIVERT_ONLY although its prose states removal", "premise",
     PROMOTE,
     '    ("turnip",      "harlequin-bug", DESTROY_STATED),',
     '    ("turnip",      "harlequin-bug", DIVERT_ONLY),'),

    # ---- species: the guard that stops a rung being copied off a sibling ------------------------
    ("species: the species check is disabled", "species", PROMOTE,
     '            if s not in said:', '            if False:'),
    ("species: the no-plant-named refusal is disabled", "species", PROMOTE,
     '        if not named:', '        if False:'),
    ("species: the vocabulary is emptied so no rung names anything", "species", PROMOTE,
     'SPECIES = ("mustard", "arugula", "nasturtium", "rapeseed", "collard", "kale", "crucifer")',
     'SPECIES = ()'),
    ("species: nasturtium leaves the vocabulary, unblinding jalapeno", "species", PROMOTE,
     '"mustard", "arugula", "nasturtium", "rapeseed"', '"mustard", "arugula", "rapeseed"'),
    ("species: jalapeno's rung is given mustard, which its prose never names", "species", PROMOTE,
     '            "Plant a little nasturtium at the edge of the bed to draw beetles off the peppers. "',
     '            "Plant a little mustard at the edge of the bed to draw beetles off the peppers. "'),

    # ---- distinct: the prose/rung correspondence, both ways --------------------------------------
    ("distinct: the copied-rung direction is disabled", "distinct", PROMOTE,
     '            if same_rung and not same_prose:', '            if False:'),
    ("distinct: the forked-twin direction is disabled", "distinct", PROMOTE,
     '            if same_prose and not same_rung:', '            if False:'),
    # Rebinding AFTER the dict literal, not inside it. An `X if False else {...}` injection
    # evaluates the else branch and is inert; this genuinely hands kale collards' rung object.
    ("distinct: kale is handed collards' rung wholesale", "distinct", PROMOTE,
     'TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")',
     'RUNGS[("kale", "harlequin-bug")] = RUNGS[("collards", "harlequin-bug")]\n'
     'TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")'),

    # ---- exclusion: the six that must never carry the rung ---------------------------------------
    ("exclusion: the resolve check is disabled", "exclusion", PROMOTE,
     '    for slug, ident, reason in EXCLUSIONS:\n        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n            return (f"exclusion {slug}/{ident!r} does not resolve to a '
     'problem in canonical, so the "',
     '    for slug, ident, reason in ():\n        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n            return (f"exclusion {slug}/{ident!r} does not resolve to a '
     'problem in canonical, so the "'),
    ("exclusion: verify_post stops checking the six", "exclusion", PROMOTE,
     '    for slug, ident, reason in EXCLUSIONS:\n        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n            return f"post: exclusion {slug}/{ident!r} no longer resolves"',
     '    for slug, ident, reason in ():\n        p = find_problem(data, slug, ident)\n'
     '        if p is None:\n            return f"post: exclusion {slug}/{ident!r} no longer resolves"'),
    ("exclusion: nasturtium is typo'd and silently protects nothing", "exclusion", PROMOTE,
     '    ("nasturtium", "Aphids",', '    ("nasturtium", "Aphid",'),
    ("exclusion: the target-collision check is disabled", "exclusion", PROMOTE,
     '        if (slug, ident) in {(s, pid) for s, pid, _g in TARGETS}:', '        if False:'),
    ("exclusion: the reason requirement is dropped", "exclusion", PROMOTE,
     '        if not reason.strip():', '        if False:'),
    ("exclusion: find_problem stops matching by name, losing the two unladdered ones", "exclusion",
     PROMOTE,
     '                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):',
     '                if isinstance(p, dict) and ident == p.get("id"):'),

    # ---- content: what each rung must and must not say --------------------------------------------
    ("content: the cautions-pointer requirement is dropped", "content", PROMOTE,
     '        if CAUTIONS_POINTER not in blob:', '        if False:'),
    ("content: a DIVERT_ONLY rung may attribute a removal to the crop", "content", PROMOTE,
     '        if group == DIVERT_ONLY and ATTRIBUTION in blob:', '        if False:'),
    ("content: a DESTROY_STATED rung may drop the attribution", "content", PROMOTE,
     '        if group == DESTROY_STATED and ATTRIBUTION not in blob:', '        if False:'),
    ("content: the identical-registers check is disabled", "content", PROMOTE,
     '        if rung["note_beginner"] == rung["note_seasoned"]:', '        if False:'),
    ("content: the hygiene sweep runs over nothing", "content", PROMOTE,
     '        for s in (rung["note_beginner"], rung["note_seasoned"]):', '        for s in ():'),

    # ---- placement --------------------------------------------------------------------------------
    ("placement: the rung is appended LAST, breaking tier order", "placement", PROMOTE,
     '        lad.insert(i, {"method": METHOD,', '        lad.append({"method": METHOD,'),
    ("placement: the rung is inserted at the FRONT of the cultural run", "placement", PROMOTE,
     '        i, bad = cultural_end(lad, cm)\n        if bad:\n'
     '            raise AssertionError(f"{slug}/{pid}: {bad}")',
     '        i, bad = cultural_end(lad, cm)\n        i = 0\n        if bad:\n'
     '            raise AssertionError(f"{slug}/{pid}: {bad}")'),
    ("placement: verify_post stops counting the rung", "placement", PROMOTE,
     '        if ms.count(METHOD) != 1:', '        if False:'),
    ("placement: verify_post stops requiring it at the end of the cultural run", "placement",
     PROMOTE,
     '        if idx + 1 < len(ms) and cm[ms[idx + 1]]["tier"] == "cultural":', '        if False:'),
    # A "sits after a non-cultural rung" branch was here and its mutation SURVIVED run 1: the check
    # is implied by monotonicity (this method is cultural, the lowest rank), so it could never fire
    # on its own. The branch was deleted rather than kept as an unreachable forward assertion, and
    # the injection went with it. Monotonicity below is the reachable check for that state.
    ("placement: verify_post stops checking tier monotonicity", "placement", PROMOTE,
     '        if ranks != sorted(ranks):', '        if False:'),
    ("placement: verify_post stops checking which crop's rung landed", "placement", PROMOTE,
     '        if (r["note_beginner"], r["note_seasoned"]) != (want["note_beginner"],',
     '        if False and (r["note_beginner"], r["note_seasoned"]) != (want["note_beginner"],'),
    ("placement: the already-carries refusal is disabled", "placement", PROMOTE,
     '        if METHOD in ms:\n            return f"{slug}/{pid} already carries {METHOD}"',
     '        if METHOD in ms:\n            pass'),
    ("placement: the mint-landed precondition is disabled", "placement", PROMOTE,
     '    if METHOD not in cm:\n        return f"{METHOD} is not in the catalog; the mint must land first"',
     '    if METHOD not in cm:\n        pass'),

    # ---- blast --------------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    cm = data["control_methods"]',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    cm = data["control_methods"]'),
    ("blast: the landed-set check is disabled", "blast", PROMOTE,
     '    if sorted(landed) != expected:', '    if False:'),
    ("blast: the landed-set compares against itself", "blast", PROMOTE,
     '    expected = sorted((s, pid) for s, pid, _g in TARGETS)', '    expected = sorted(landed)'),
    ("blast: verify_post stops checking bystander crops", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: verify_post stops comparing the crop set", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: verify_post stops checking control_methods", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '        lad.insert(i, {"method": METHOD,', '        _skip = ({"method": METHOD,')


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
    wd = tempfile.mkdtemp(prefix="mutate_trapbf_")
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
    print("MUTATION HARNESS -- trap_cropping backfill, 10 rungs on 9 certified crops")
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
