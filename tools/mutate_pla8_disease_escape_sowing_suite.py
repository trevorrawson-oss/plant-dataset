#!/usr/bin/env python3
"""Mutation harness for the disease_escape_sowing mint (PLA-215).

THE SAFETY-BEARING HALF OF THIS METHOD IS THE TRADE, NOT THE PRACTICE. The escape is a race the
grower can lose: sowing early trades late-season disease for a cold, wet seedbed, and NC State
quantifies the floor (seed in moist soil below 50°F will often rot). The `disclosure` family
attacks exactly that: empty the axis table, disable the check in `check` and again in
`verify_post`, drop the axis, and strip the sentence out of the shipped cautions.

`contrast` attacks the mint-not-widen ruling (planting_time_avoidance dodges a PUBLISHED flight
window; this races an unpublished weather epidemic). `scope` attacks the narrow applies_to and the
cultural tier. `exclusion` attacks the four scan matches that must never carry the rung, spinach's
damping-off above all -- typed fungal, gate-legal, and the advice inverts there.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_disease_escape_sowing.py")
PROMOTE = os.path.join(HERE, "promote_pla8_disease_escape_sowing.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- disclosure: the cold-seedbed trade, which is what keeps the advice from costing a stand
    ("disclosure: missing_disclosures always reports nothing missing", "disclosure", PROMOTE,
     '    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()\n'
     '                  if not all(t in blob for t in toks))',
     '    return []'),
    ("disclosure: the axis table is emptied", "disclosure", PROMOTE,
     'REQUIRED_DISCLOSURES = {\n    "seed_rot":   ("cold", "rot"),',
     'REQUIRED_DISCLOSURES = {}\n_UNUSED_DISCLOSURES = {\n    "seed_rot":   ("cold", "rot"),'),
    ("disclosure: the threshold axis drops out of the table", "disclosure", PROMOTE,
     '    "threshold":  ("50°f",),\n', ''),
    ("disclosure: the seed_rot axis drops out of the table", "disclosure", PROMOTE,
     '    "seed_rot":   ("cold", "rot"),\n', ''),
    ("disclosure: check stops requiring the disclosures", "disclosure", PROMOTE,
     '    miss = missing_disclosures(METHOD)\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: verify_post stops requiring them on the shipped entry", "disclosure", PROMOTE,
     '    miss = missing_disclosures(cm[KEY])\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: the cautions lose the cold-soil floor", "disclosure", PROMOTE,
     '        "The race can be lost at the start instead of the end. Seed sown into cold, wet soil "\n'
     '        "can rot before it emerges: NC State puts the working floor for sweet corn at 50°F soil "\n'
     '        "for standard varieties and 60°F for the high-sugar types, and states that seed planted "\n'
     '        "in moist soil below those temperatures will often rot. Sow at the early edge of what "\n'
     '        "the seedbed allows, not past it.",',
     '        "Sow at the early edge of your window for the best escape.",'),
    ("disclosure: the cautions lose the not-a-substitute warning", "disclosure", PROMOTE,
     '        "An early sowing shortens the crop\'s overlap with the disease weather rather than "\n'
     '        "preventing infection, so it is a companion to a resistant variety, not a substitute "\n'
     '        "for one. The sources that state the escape put resistance first in the same sentence.",',
     '        "An early sowing gives the crop a strong head start on the disease.",'),

    # ---- contrast: the mint-not-widen ruling ----------------------------------------------------
    ("contrast: the contrast table is emptied", "contrast", PROMOTE,
     'REQUIRED_CONTRASTS = ("flight window", "published", "weather-driven", "what you plant")',
     'REQUIRED_CONTRASTS = ()'),
    ("contrast: check stops requiring the distinctions", "contrast", PROMOTE,
     '    miss = missing_contrasts(METHOD)\n    if miss:',
     '    miss = []\n    if miss:'),
    ("contrast: verify_post stops requiring them", "contrast", PROMOTE,
     '    miss = missing_contrasts(cm[KEY])\n    if miss:',
     '    miss = []\n    if miss:'),
    ("contrast: best_use stops naming the flight-window distinction", "contrast", PROMOTE,
     '        "Distinct from dodging a pest\'s flight window, which extension services publish as local "\n'
     '        "calendar or degree-day dates; the epidemic this races is weather-driven with no "',
     '        "Distinct from dodging a pest\'s active season, which extension services publish as local "\n'
     '        "calendar or degree-day dates; the epidemic this races is weather-driven with no "'),

    # ---- scope: what the method is allowed to reach ---------------------------------------------
    ("scope: the applies_to check is disabled in check", "scope", PROMOTE,
     '    if METHOD["applies_to"] != ["fungal_foliar"]:', '    if False:'),
    ("scope: the applies_to check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["applies_to"] != ["fungal_foliar"]:', '    if False:'),
    ("scope: applies_to widens to disease_general nothing was read for", "scope", PROMOTE,
     '    "applies_to": ["fungal_foliar"],',
     '    "applies_to": ["fungal_foliar", "disease_general"],'),
    ("scope: the tier check is disabled in check", "scope", PROMOTE,
     '    if METHOD["tier"] != "cultural":', '    if False:'),
    ("scope: the tier check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["tier"] != "cultural":', '    if False:'),
    ("scope: the tier becomes physical, misordering every ladder", "scope", PROMOTE,
     '    "name": "Disease-escape sowing",\n    "tier": "cultural",',
     '    "name": "Disease-escape sowing",\n    "tier": "physical",'),

    # ---- exclusion: the four that must never carry the rung -------------------------------------
    ("exclusion: the resolve check is disabled", "exclusion", PROMOTE,
     '    for slug, ident in EXCLUSIONS:\n        if find_problem(data, slug, ident) is None:',
     '    for slug, ident in ():\n        if find_problem(data, slug, ident) is None:'),
    ("exclusion: spinach is typo'd and silently protects nothing", "exclusion", PROMOTE,
     '    ("spinach", "damping-off"),', '    ("spinach", "damping-offf"),'),
    # A REAL rebinding, not `EXCLUSIONS = () or (...)` -- an empty tuple is falsy, so that idiom
    # evaluates straight back to the original and injects nothing.
    ("exclusion: the list is emptied", "exclusion", PROMOTE,
     'EXCLUSIONS = (\n    ("spinach", "damping-off"),',
     'EXCLUSIONS = ()\n_UNUSED_EXCLUSIONS = (\n    ("spinach", "damping-off"),'),
    ("exclusion: verify_post stops checking the four", "exclusion", PROMOTE,
     '    for slug, ident in EXCLUSIONS:\n        p = find_problem(data, slug, ident)',
     '    for slug, ident in ():\n        p = find_problem(data, slug, ident)'),
    ("exclusion: find_problem stops matching by name", "exclusion", PROMOTE,
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

    # ---- hygiene / mechanics --------------------------------------------------------------------
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
    wd = tempfile.mkdtemp(prefix="mutate_descape_")
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
    print("MUTATION HARNESS -- disease_escape_sowing mint, the catalog's 60th method")
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
