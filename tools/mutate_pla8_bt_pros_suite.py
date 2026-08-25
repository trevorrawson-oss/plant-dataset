#!/usr/bin/env python3
"""Mutation harness for the PLA-8 bt.pros[1] promote (PLA-215).

THE `contradiction` FAMILY IS LOAD-BEARING, because this defect was never structural. Both fields
were well-formed and each was individually defensible; what was wrong was that MethodSheet.tsx
renders them on one sheet, pros first, so a reader met "sparing most beneficial insects" seventeen
lines before "kills ... swallowtails and monarchs". Mutations here restore the contradiction in
every way it could come back: the old text, a paraphrase of it, deleting the pro outright (which
would satisfy a naive banned-construction check while leaving the reader worse off), and gutting the
caution instead so the two agree by weakening the true half.

THE `leftalone` FAMILY guards the 39 selectivity sentences the sweep read and spared. 40 hits, 1
defect. A later pass "finishing the job" by scrubbing neem_oil's "once it dries" or iron
phosphate's comparative "safer THAN metaldehyde" would make the record less accurate, not more.

THE `vocabulary` FAMILY exists because of how this defect survived. The c13ddea5 sweep READ this
exact field and cleared it, asking safe/non-toxic/completely/harmless -- a vocabulary that cannot
see "targets caterpillars only". A pattern that matches nothing reports success without checking.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_bt_pros.py")
PROMOTE = os.path.join(HERE, "promote_pla8_bt_pros.py")
MARKER = "# MUTATION-APPLIED"

APPLY = ('def apply_to(data):\n    pros = data["control_methods"][METHOD]["pros"]\n'
         '    if pros[INDEX] != OLD:\n'
         '        raise AssertionError(f"pros[{INDEX}] drifted; refusing to overwrite")\n'
         '    pros[INDEX] = NEW\n    return 1')

MUTATIONS = [
    # ---- contradiction: the sheet argues with itself again -------------------------------------
    ("contradiction: the replacement IS the old text", "contradiction", PROMOTE,
     'NEW = "Acts on caterpillars as a group, sparing bees and most other beneficials"',
     'NEW = "Targets caterpillars only, sparing most beneficial insects"'),
    ("contradiction: a paraphrase restores the 'only' claim", "contradiction", PROMOTE,
     'NEW = "Acts on caterpillars as a group, sparing bees and most other beneficials"',
     'NEW = "Hits only caterpillars, leaving beneficial insects unharmed"'),
    ("contradiction: the pro is DELETED rather than corrected", "contradiction", PROMOTE, APPLY,
     'def apply_to(data):\n    data["control_methods"][METHOD]["pros"].pop(INDEX)\n    return 1'),
    ("contradiction: the CAUTION is gutted so the two agree", "contradiction", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"][METHOD]["cautions"][0] = "Follow the label."\n    return 1')),
    ("contradiction: the true selectivity claim is dropped entirely", "contradiction", PROMOTE,
     'NEW = "Acts on caterpillars as a group, sparing bees and most other beneficials"',
     'NEW = "A biological option accepted for organic use"'),
    ("contradiction: the instruction is repeated a fourth time on the sheet", "contradiction",
     PROMOTE,
     'NEW = "Acts on caterpillars as a group, sparing bees and most other beneficials"',
     'NEW = "Acts on caterpillars as a group, so keep it off plants you are growing for butterflies"'),

    # ---- vocabulary: the pattern that has to be able to see the defect --------------------------
    ("vocabulary: BANNED is weakened to match nothing", "vocabulary", PROMOTE,
     'BANNED = re.compile(r"\\bonly\\b(?=[^.;]*\\b(?:beneficial|bee|pollinator|butterfl|wildlife)\\b)", re.I)',
     'BANNED = re.compile(r"(?!x)x")'),
    ("vocabulary: BANNED reverts to the sweep vocabulary that MISSED this", "vocabulary", PROMOTE,
     'BANNED = re.compile(r"\\bonly\\b(?=[^.;]*\\b(?:beneficial|bee|pollinator|butterfl|wildlife)\\b)", re.I)',
     'BANNED = re.compile(r"\\b(?:safe|non-toxic|completely|harmless)\\b", re.I)'),
    ("vocabulary: the BANNED-matches-OLD self-check is disabled", "vocabulary", PROMOTE,
     '    if not BANNED.search(OLD):',
     '    if False:'),

    # ---- leftalone: the 39 correct hedges -------------------------------------------------------
    ("leftalone: neem_oil's 'once it dries' qualifier is scrubbed", "leftalone", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"]["neem_oil"]["best_use"] = (\n'
      '        "Light, early soft-bodied infestations where you want an option that spares beneficials.")\n'
      '    return 1')),
    ("leftalone: iron phosphate's comparative becomes an absolute", "leftalone", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"]["iron_phosphate_slug_bait"]["pros"][0] = (\n'
      '        "Safe for use around children, pets, birds, fish, and other wildlife")\n'
      '    return 1')),
    ("leftalone: bt's pros[0] NPIC term of art is rewritten", "leftalone", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"][METHOD]["pros"][0] = "Nontoxic to people, pets and bees"\n'
      '    return 1')),
    ("leftalone: the LEFT_ALONE assertion loop is disabled", "leftalone", PROMOTE,
     '    for path, text in LEFT_ALONE.items():\n        try:\n            cur = _at(data, path)',
     '    for path, text in []:\n        try:\n            cur = _at(data, path)'),

    # ---- scope ---------------------------------------------------------------------------------
    ("scope: another method is edited", "scope", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"]["sulfur"]["best_use"] += " Also rust."\n    return 1')),
    ("scope: a crop is touched", "scope", PROMOTE, APPLY,
     APPLY.replace("    return 1", '    data["crops"][0]["name"] = "MUTATED"\n    return 1')),
    ("scope: a ladder rung is dropped", "scope", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    for _c in data["crops"]:\n'
      '        for _f in ("pests", "diseases"):\n'
      '            for _p in (_c.get(_f) or []):\n'
      '                if isinstance(_p, dict) and _p.get("control_ladder"):\n'
      '                    _p["control_ladder"].pop(); return 1\n    return 1')),
    ("scope: a different bt field is edited", "scope", PROMOTE, APPLY,
     APPLY.replace("    return 1",
      '    data["control_methods"][METHOD]["cons"].append("Extra con.")\n    return 1')),

    # ---- refusal / mechanics -------------------------------------------------------------------
    ("refusal: the drifted-text check is disabled", "refusal", PROMOTE,
     '    if pros[INDEX] != OLD:\n        return f"{METHOD}.pros[{INDEX}] is not the expected text; found {pros[INDEX]!r}"',
     '    if False:\n        return f"{METHOD}.pros[{INDEX}] is not the expected text; found {pros[INDEX]!r}"'),
    ("refusal: the already-applied check is disabled", "refusal", PROMOTE,
     '    if pros[INDEX] == NEW:\n        return "already applied"',
     '    if False:\n        return "already applied"'),
    ("refusal: apply overwrites instead of raising on drift", "refusal", PROMOTE,
     '    if pros[INDEX] != OLD:\n        raise AssertionError(f"pros[{INDEX}] drifted; refusing to overwrite")',
     '    if False:\n        raise AssertionError(f"pros[{INDEX}] drifted; refusing to overwrite")'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE, APPLY,
            "def apply_to(data):\n    return 0")


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
    wd = tempfile.mkdtemp(prefix="mutate_btp_")
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
    print("MUTATION HARNESS -- PLA-8 bt.pros[1], the 'only' selectivity overclaim")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails -- the clean suite is not green in the sandbox.")
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
        print(f"  {k:14s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
