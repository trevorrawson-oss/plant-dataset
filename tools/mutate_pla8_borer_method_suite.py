#!/usr/bin/env python3
"""Mutation harness for the PLA-8 borer_stem_surgery mint (PLA-215).

THE `scope` FAMILY IS LOAD-BEARING. This method exists because `handpick` was the wrong key for a
larva inside a stem -- three authoring agents said so independently, two citing handpick's own con,
"Misses hidden eggs and tiny larvae". The entire value of the mint is that the gate can now tell
those two apart. Widen `applies_to` and the new method becomes a second handpick, reopening the gap
with an extra catalog key to show for it. Mutations widen it in every direction that matters.

THE `hedge` FAMILY exists because BOTH sources qualify this method's success and neither hedge has a
term a scanner would flag. UMN: "you may not be able to save the plant". ISU: "can sometimes be
successfully removed ... during July or early August". Prose that promises a rescue would pass every
structural gate in the repo.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_borer_method.py")
PROMOTE = os.path.join(HERE, "promote_pla8_borer_method.py")
CONTENT = os.path.join(HERE, "build_pla8_borer_method_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- scope: the reason the method exists ---------------------------------------------------
    ("scope: applies_to widens to include insect_chewing (becomes a second handpick)", "scope",
     CONTENT, '"applies_to": ["insect_boring"],', '"applies_to": ["insect_boring", "insect_chewing"],'),
    ("scope: applies_to widens to insect_general", "scope", CONTENT,
     '"applies_to": ["insect_boring"],', '"applies_to": ["insect_general"],'),
    ("scope: applies_to becomes 'any'", "scope", CONTENT,
     '"applies_to": ["insect_boring"],', '"applies_to": ["any"],'),
    ("scope: the narrow-scope check is disabled", "scope", PROMOTE,
     '    if m["applies_to"] != ["insect_boring"]:', '    if False:'),
    ("scope: the post-check no longer verifies scope", "scope", PROMOTE,
     '    if cm[C.KEY]["applies_to"] != ["insect_boring"]:', '    if False:'),

    # ---- hedge: both sources qualify this method ------------------------------------------------
    ("hedge: the failure case is removed from the beginner register", "hedge", CONTENT,
     '"not work every time and you may lose the plant anyway, but the vine is usually lost without it.",',
     '"work reliably once you have found the grub.",'),
    ("hedge: the cons stop carrying the failure case", "hedge", CONTENT,
     '"It may not save the plant, and the cut sets the vine back even when it works",',
     '"The cut sets the vine back a little",'),
    ("hedge: the seasonal window is dropped from both fields", "hedge", CONTENT,
     '"early August and notes that infested plants are often able to live and produce anyway; UMN "',
     '"midsummer and notes that infested plants are often able to live and produce anyway; UMN "'),
    ("hedge: the hedge check is disabled", "hedge", PROMOTE,
     '    else:\n        return "the prose carries no hedge, but BOTH sources qualify this method\'s success"',
     '    else:\n        pass'),
    ("hedge: the window check is disabled", "hedge", PROMOTE,
     '    if "july or early august" not in blob:', '    if False:'),

    # ---- sourcing --------------------------------------------------------------------------------
    ("sourcing: the ISU anchor reverts to the redirecting hortnews url", "sourcing", CONTENT,
     '"iastate_ext": {"url": "https://yardandgarden.extension.iastate.edu/encyclopedia/squash-vine-borer",',
     '"iastate_ext": {"url": "https://hortnews.extension.iastate.edu/squash-vine-borer",'),
    ("sourcing: a source loses its anchoring_url", "sourcing", PROMOTE,
     '        if s not in m["anchoring_urls"]:', '        if False:'),
    ("sourcing: the T1 tier check is disabled", "sourcing", PROMOTE,
     '        if (sc[s].get("tier") or "").upper() != "T1":', '        if False:'),

    # ---- blast -----------------------------------------------------------------------------------
    ("blast: an existing method is edited during the mint", "blast", CONTENT,
     '    cm[KEY] = dict(METHOD)\n    return 1',
     '    cm["handpick"]["applies_to"].append("insect_boring")\n    cm[KEY] = dict(METHOD)\n    return 1'),
    ("blast: handpick is silently widened to cover borers too", "blast", CONTENT,
     '    shape = set(next(iter(cm.values())).keys())',
     '    cm["handpick"]["best_use"] += " Also works on stem borers."\n    shape = set(next(iter(cm.values())).keys())'),
    ("blast: a crop is touched", "blast", PROMOTE,
     'def apply_to(data):\n    return content().apply_mint(data["control_methods"])',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    return content().apply_mint(data["control_methods"])'),

    # ---- shape / mechanics -------------------------------------------------------------------------
    ("shape: a required field is dropped from the mint", "shape", CONTENT,
     '    "best_use":\n        "A vine already wilting', '    "_best_use":\n        "A vine already wilting'),
    ("shape: the tier becomes invalid", "shape", CONTENT, '"tier": "physical",', '"tier": "manual",'),
    ("shape: an absolute claim enters the prose", "shape", CONTENT,
     '"The one option left once a borer is inside the stem, where sprays no longer reach",',
     '"Completely removes the borer and always saves the vine",'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            'def apply_to(data):\n    return content().apply_mint(data["control_methods"])',
            'def apply_to(data):\n    return 0')


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
    wd = tempfile.mkdtemp(prefix="mutate_bsm_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
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
    print("MUTATION HARNESS -- PLA-8 mint borer_stem_surgery")
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
        print(f"  {k:10s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
