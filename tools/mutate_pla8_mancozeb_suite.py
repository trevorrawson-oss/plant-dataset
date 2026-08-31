#!/usr/bin/env python3
"""Mutation harness for the mancozeb mint (PLA-215).

`disclosure` attacks the hazard axes (water H, Prop 65/EPA, the UNRATED natural-enemies honesty,
PPE, the 5 day PHI). `invented` attacks this mint's own family: the detector that refuses a
natural-enemies Low claim the database does not carry, in either word order. `scope` attacks the
narrow applies_to and the conventional tier. `blast` and `mechanics` as usual.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_mancozeb.py")
PROMOTE = os.path.join(HERE, "promote_pla8_mancozeb.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- disclosure -----------------------------------------------------------------------------
    ("disclosure: missing_disclosures always reports nothing missing", "disclosure", PROMOTE,
     '    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()\n'
     '                  if not all(t in blob for t in toks))',
     '    return []'),
    ("disclosure: the axis table is emptied", "disclosure", PROMOTE,
     'REQUIRED_DISCLOSURES = {\n    "aquatic":    ("water quality", "aquatic"),',
     'REQUIRED_DISCLOSURES = {}\n_UNUSED_DISCLOSURES = {\n    "aquatic":    ("water quality", "aquatic"),'),
    ("disclosure: the unrated axis drops out of the table", "disclosure", PROMOTE,
     '    "unrated":    ("natural enemies", "unrated is not the same as low"),\n', ''),
    ("disclosure: the carcinogen axis drops out of the table", "disclosure", PROMOTE,
     '    "carcinogen": ("prop 65", "carcinogen"),\n', ''),
    ("disclosure: check stops requiring the disclosures", "disclosure", PROMOTE,
     '    miss = missing_disclosures(METHOD)\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: verify_post stops requiring them on the shipped entry", "disclosure", PROMOTE,
     '    miss = missing_disclosures(cm[KEY])\n    if miss:',
     '    miss = []\n    if miss:'),
    ("disclosure: the cautions lose the Prop 65 line", "disclosure", PROMOTE,
     '        "Listed on both the California Prop 65 list and the US EPA list, where an active "\n'
     '        "ingredient appears only as a likely or confirmed carcinogen; weigh that before "\n'
     '        "choosing it on a food crop",',
     '        "Read the label before choosing it on a food crop",'),
    ("disclosure: the cautions lose the unrated-enemies honesty", "disclosure", PROMOTE,
     '        "UC IPM shows no rating for its risk to natural enemies. Unrated is not the same as "\n'
     '        "low, so do not treat it as the gentler choice for a bed where predators are doing "\n'
     '        "work",',
     '        "Consider the rest of the bed before spraying",'),

    # ---- invented: the natural-enemies rating the database does not carry -----------------------
    ("invented: the detector always reports nothing", "invented", PROMOTE,
     '    for s in prose_of(m):\n        for sent in re.split(r"(?<=[.!?])\\s+", s):',
     '    for s in ():\n        for sent in re.split(r"(?<=[.!?])\\s+", s):'),
    ("invented: the unrated markers stop excusing nothing (any sentence passes)", "invented", PROMOTE,
     'UNRATED_MARKERS = ("unrated", "no rating")',
     'UNRATED_MARKERS = ("unrated", "no rating", "natural")'),
    ("invented: check stops running the detector", "invented", PROMOTE,
     '    bad = invented_enemy_rating(METHOD)\n    if bad:',
     '    bad = None\n    if bad:'),
    ("invented: verify_post stops running the detector", "invented", PROMOTE,
     '    bad = invented_enemy_rating(cm[KEY])\n    if bad:',
     '    bad = None\n    if bad:'),

    # ---- scope ----------------------------------------------------------------------------------
    ("scope: the applies_to check is disabled in check", "scope", PROMOTE,
     '    if METHOD["applies_to"] != ["fungal_foliar"]:', '    if False:'),
    ("scope: the applies_to check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["applies_to"] != ["fungal_foliar"]:', '    if False:'),
    ("scope: applies_to widens to disease_general nothing was read for", "scope", PROMOTE,
     '    "applies_to": ["fungal_foliar"],',
     '    "applies_to": ["fungal_foliar", "disease_general"],'),
    ("scope: the tier check is disabled in check", "scope", PROMOTE,
     '    if METHOD["tier"] != "conventional":', '    if False:'),
    ("scope: the tier check is disabled in verify_post", "scope", PROMOTE,
     '    if cm[KEY]["tier"] != "conventional":', '    if False:'),
    ("scope: the tier softens to soft_chemical", "scope", PROMOTE,
     '    "name": "Mancozeb",\n    "tier": "conventional",',
     '    "name": "Mancozeb",\n    "tier": "soft_chemical",'),

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
    wd = tempfile.mkdtemp(prefix="mutate_mancozeb_")
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
    print("MUTATION HARNESS -- mancozeb mint, the catalog's 61st method")
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
