#!/usr/bin/env python3
"""Mutation harness for the ant_exclusion mint (PLA-215).

Families: `blast` attacks the no-crop-moves claim, which is a catalog revision's entire safety
argument. `premise` attacks the count and re-mint refusals. `scope` attacks the pinned tier and the
`disease_general` scope -- the two values that make this mint accomplish anything. `anchors` attacks
the mis-pointed-key and unadmitted-source checks. `hygiene` and `mechanics` as elsewhere.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_ant_exclusion.py")
PROMOTE = os.path.join(HERE, "promote_pla8_ant_exclusion.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- blast ----------------------------------------------------------------------------------
    ("blast: a changed crop is accepted", "blast", PROMOTE,
     "        if pre_crops[slug] != post_crops[slug]:", "        if False:"),
    ("blast: a dropped or added crop is accepted", "blast", PROMOTE,
     "    if set(pre_crops) != set(post_crops):", "    if False:"),
    ("blast: an edited existing method is accepted", "blast", PROMOTE,
     "        if serialize(cm[k]) != serialize(pre_cm[k]):", "        if False:"),
    ("blast: an edited existing source is accepted", "blast", PROMOTE,
     "        if serialize(sc[k]) != serialize(pre_sc[k]):", "        if False:"),
    ("blast: the set of added methods is not pinned", "blast", PROMOTE,
     "    if set(cm) - set(pre_cm) != {METHOD_KEY}:", "    if False:"),
    ("blast: the set of added sources is not pinned", "blast", PROMOTE,
     "    if set(sc) - set(pre_sc) != set(NEW_SOURCES):", "    if False:"),

    # ---- premise --------------------------------------------------------------------------------
    ("premise: re-minting an existing key is accepted", "premise", PROMOTE,
     "    if METHOD_KEY in cm:", "    if False:"),
    ("premise: an existing source id is overwritten silently", "premise", PROMOTE,
     "        if sid in sc:", "        if False:"),
    ("premise: the method count premise is not asserted", "premise", PROMOTE,
     "    if len(cm) != EXPECT_METHODS_BEFORE:", "    if False:"),
    ("premise: the source count premise is not asserted", "premise", PROMOTE,
     "    if len(sc) != EXPECT_SOURCES_BEFORE:", "    if False:"),
    ("premise: a missing required field is accepted", "premise", PROMOTE,
     "        if f not in ANT_EXCLUSION:", "        if False:"),

    # ---- scope ----------------------------------------------------------------------------------
    ("scope: the tier is no longer pinned to physical", "scope", PROMOTE,
     '    if ANT_EXCLUSION["tier"] != "physical":', "    if False:"),
    ("scope: disease_general may be dropped, re-blocking sooty mold", "scope", PROMOTE,
     '    if "disease_general" not in ANT_EXCLUSION["applies_to"]:', "    if False:"),

    # ---- anchors --------------------------------------------------------------------------------
    ("anchors: an unadmitted source is accepted", "anchors", PROMOTE,
     "        if sid not in NEW_SOURCES and sid not in sc:", "        if False:"),
    ("anchors: a mis-pointed anchoring url is accepted", "anchors", PROMOTE,
     '        if rec["url"] != want:', "        if False:"),
    ("anchors: sources and anchoring_urls may disagree", "anchors", PROMOTE,
     '    if set(ANT_EXCLUSION["anchoring_urls"]) != set(ANT_EXCLUSION["sources"]):',
     "    if False:"),

    # ---- titles ---------------------------------------------------------------------------------
    ("titles: the required-field loop on new sources runs over nothing", "titles", PROMOTE,
     "        for f in SOURCE_REQUIRED:", "        for f in ():"),
    ("titles: A54's own gate is never called", "titles", PROMOTE,
     '    v = title_violations(data["source_catalog"])   # takes the CATALOG dict, not `data`',
     "    v = []"),

    # ---- hygiene --------------------------------------------------------------------------------
    ("hygiene: prose fields are not scanned", "hygiene", PROMOTE,
     '    for f in ("how_it_works_beginner", "how_it_works_seasoned", "best_use", "find_it_beginner"):',
     "    for f in ():"),
    ("hygiene: list entries are not scanned", "hygiene", PROMOTE,
     '    for lst in ("pros", "cons", "cautions"):', "    for lst in ():"),
    ("hygiene: identical registers are accepted", "hygiene", PROMOTE,
     "    if b == s:", "    if False:"),
    ("hygiene: the absolute-word scan runs over nothing", "hygiene", PROMOTE,
     "    for w in BANNED_ABSOLUTES:", "    for w in ():"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

# If the method is never attached, the suite must not still pass.
SENTINEL = ("SENTINEL: the method is never added to the catalog", PROMOTE,
            '    data["control_methods"][METHOD_KEY] = copy.deepcopy(ANT_EXCLUSION)',
            '    _skip = copy.deepcopy(ANT_EXCLUSION)')


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
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_ant_excl_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read()
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 ant_exclusion mint")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails (the CLEAN fixture must pass).")
        return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print("HARNESS DEAD: %s SURVIVED." % label)
        return 1
    print("sentinel         : RED as required\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print("  SURVIVED  [%s] %s" % (family, label))
        else:
            caught += 1; fam[family][0] += 1
            print("  caught    [%s] %s" % (family, label))

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print("  %-10s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(MUTATIONS)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
