#!/usr/bin/env python3
"""Mutation harness for problem_id_collision_gate + its suite (PLA-215 bar, PLA-449 build).

FAMILIES. `distance` attacks check 1's threshold AND its metric, because a guard that fires on the
right branch with the wrong number is the failure mode a harness cannot otherwise see. `plural`,
`normalize` and `conjunct` attack each documented step of the normalization separately -- the steps
are mutually redundant on some pairs, so a single lumped mutation would survive on the others.
`nesting` and `scoping` attack the two independent constraints that keep check 3 from flooding,
one each, since either alone still passes the slug fixture. `registry` attacks the registration
path in BOTH directions: suppressing everything and suppressing nothing are different defects and
different tests catch them. `mechanics` attacks the minted filter and the array walk.

THE REGISTRY CLIQUE MUTATION IS THE ONE WORTH READING. `Registry` expands each entry's id SET into
every pair. Expanding only ADJACENT pairs looks identical on all nine two-id entries and differs
only on the one three-id entry (the aphid family), so it is invisible to every test that does not
reach `apricot-aphids <-> citrus-aphids`. That is the same shape as PLA-162's four green guards.

TWO POSITIVE CONTROLS. The CLEAN fixture must pass, and `distance: threshold to 0` must leave the
name check still finding the same-name pairs -- otherwise a mutation that killed the whole scan
would read as 'check 1 is covered'.

ONE MUTATION WAS WITHDRAWN, not injected. `edit_distance`'s `if a == b: return 0` is an
OPTIMIZATION, not a branch: the DP below returns 0 for that input unaided, so disabling it is an
equivalent mutant and its survival would be noise dressed as a gap. It is annotated at its site.

Includes the anchor PREFLIGHT, the MUTATION-APPLIED marker, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_problem_id_collision_gate.py")
GATE = os.path.join(HERE, "problem_id_collision_gate.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- distance: the threshold AND the metric --------------------------------------------
    ("distance: threshold dropped to 0", "distance",
     "NEAR_DUP_MAX_DISTANCE = 2", "NEAR_DUP_MAX_DISTANCE = 0"),
    ("distance: threshold widened to 4", "distance",
     "NEAR_DUP_MAX_DISTANCE = 2", "NEAR_DUP_MAX_DISTANCE = 4"),
    ("distance: substitution made free", "distance",
     "cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))",
     "cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1]))"),
    ("distance: length prefilter reports 0 instead of over-cap", "distance",
     "        return cap + 1", "        return 0"),

    # ---- plural: the singularizer ------------------------------------------------------------
    ("plural: bare -s strip removed", "plural",
     '    if t.endswith("s"):\n        return t[:-1]', '    if False:\n        return t[:-1]'),
    ("plural: the ss guard removed, so grass/moss get mangled", "plural",
     '    if t.endswith("ss"):\n        return t', '    if False:\n        return t'),
    ("plural: -ies branch removed", "plural",
     '    if t.endswith("ies") and len(t) > 4:', "    if False:"),

    # ---- normalize: each documented step, separately -----------------------------------------
    ("normalize: parenthetical deletion removed", "normalize",
     '    s = _PAREN.sub("", name.lower()).replace("&", " and ")',
     '    s = name.lower().replace("&", " and ")'),
    ("normalize: ampersand no longer folded", "normalize",
     '.replace("&", " and ")', '.replace("&", " & ")'),
    ("normalize: hyphens no longer folded to space", "normalize",
     '    s = _NONWORD.sub("", _HYPHENS.sub(" ", s))', '    s = _NONWORD.sub("", s)'),
    ("normalize: token sorting removed, so word order matters again", "normalize",
     '    return " ".join(sorted(normalize_tokens(name)))',
     '    return " ".join(normalize_tokens(name))'),

    # ---- conjunct: check 3's name half -------------------------------------------------------
    ("conjunct: never splits, so a family is never completed", "conjunct",
     "    if CONJUNCTION not in toks:\n        return set()",
     "    if True:\n        return set()"),
    ("conjunct: splits a name with no conjunction at all", "conjunct",
     "    if CONJUNCTION not in toks:\n        return set()",
     "    if False:\n        return set()"),

    # ---- nesting + scoping: the two independent brakes on check 3 ----------------------------
    ("nesting: id nesting no longer required", "nesting",
     "    return x < y or y < x", "    return True"),
    ("nesting: id nesting never satisfied", "nesting",
     "    return x < y or y < x", "    return False"),
    ("nesting: nesting accepts EQUAL token sets too", "nesting",
     "    return x < y or y < x", "    return x <= y or y <= x"),
    ("scoping: check 3 runs against every id, not just implicated ones", "scoping",
     "    implicated = {i for p in list(hits) for i in p}",
     "    implicated = set(universe)"),

    # ---- registry: both directions, plus the clique ------------------------------------------
    ("registry: suppresses everything", "registry",
     "        return tuple(sorted((a, b))) in self._by_pair", "        return True"),
    ("registry: suppresses nothing", "registry",
     "        return tuple(sorted((a, b))) in self._by_pair", "        return False"),
    ("registry: expands only ADJACENT pairs, not the full clique", "registry",
     "            for j in range(i + 1, len(ids)):", "            for j in range(i + 1, i + 2):"),

    # ---- schema: the microgreen name fallback ------------------------------------------------
    ("schema: name_seasoned no longer read, so microgreen crops go nameless", "schema",
     'DISPLAY_NAME_FIELDS = ("name", "name_seasoned", "name_beginner")',
     'DISPLAY_NAME_FIELDS = ("name",)'),
    ("schema: only the FIRST display field is read", "schema",
     "    return [entry[f] for f in DISPLAY_NAME_FIELDS if entry.get(f)]",
     "    return [entry[f] for f in DISPLAY_NAME_FIELDS[:1] if entry.get(f)]"),

    ("schema: the partial-coverage warning goes quiet", "schema",
     "    return sorted(i for i in (minted or ()) if not names.get(i))", "    return []"),
    ("schema: the warning fires for ids that DO have names", "schema",
     "    return sorted(i for i in (minted or ()) if not names.get(i))",
     "    return sorted(minted or ())"),

    # ---- mechanics ---------------------------------------------------------------------------
    ("mechanics: minted filter passes everything through", "mechanics",
     "        if minted is not None and not (set(p) & set(minted)):",
     "        if False:"),
    ("mechanics: minted ids absent from the data are not compared", "mechanics",
     "    universe = set(crops) | set(minted or ())", "    universe = set(crops)"),
    ("mechanics: diseases[] is not walked", "mechanics",
     '        for field in ("pests", "diseases"):', '        for field in ("pests",):'),
    ("mechanics: findings are deduplicated by kind, losing the second kind", "mechanics",
     "            hits[p][0].add(kind)", "            pass"),
]

SENTINEL = ("SENTINEL: scan returns nothing at all",
            "    out = []\n    for p, (kinds, ev) in hits.items():",
            "    out = []\n    for p, (kinds, ev) in []:")


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1])]
    src = open(GATE).read()
    for label, old in rows:
        n = src.count(old)
        if n != 1:
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(old=None, new=None):
    """A sandbox holding a MUTATED gate and a suite that imports it. HERE/REPO are pinned back to
    the real repo so the canonical and the registry still resolve -- only the CODE is meant to
    differ. Getting this wrong is how PLA-138's harness silently ran the clean fixture."""
    wd = tempfile.mkdtemp(prefix="mutate_pidcollision_")
    s = open(GATE).read()
    if old is not None:
        s = s.replace(old, new + "  " + MARKER, 1)
    s = s.replace('HERE = os.path.dirname(os.path.abspath(__file__))\nREPO = os.path.dirname(HERE)',
                  "HERE = %r\nREPO = %r" % (HERE, REPO), 1)
    open(os.path.join(wd, "problem_id_collision_gate.py"), "w").write(s)

    t = open(SUITE).read()
    t = t.replace('REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
                  'sys.path.insert(0, os.path.join(REPO, "tools"))',
                  'REPO = %r\nsys.path.insert(0, %r)' % (REPO, wd), 1)
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(t)

    if old is not None and MARKER not in open(os.path.join(wd,
                                              "problem_id_collision_gate.py")).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent after injection")
    return wd


def main():
    if not preflight():
        return 2

    wd = stage()
    ok = run(wd)
    shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails (the CLEAN fixture must pass).")
        return 2
    print("positive control : GREEN")

    label, old, new = SENTINEL
    wd = stage(old, new)
    ok = run(wd)
    shutil.rmtree(wd)
    if ok:
        print("HARNESS DEAD: %s SURVIVED." % label)
        return 2
    print("sentinel         : REDDENS\n")

    survivors, by_fam = [], {}
    for label, fam, old, new in MUTATIONS:
        wd = stage(old, new)
        ok = run(wd)
        shutil.rmtree(wd)
        by_fam.setdefault(fam, [0, 0])
        by_fam[fam][1] += 1
        if ok:
            survivors.append(label)
        else:
            by_fam[fam][0] += 1
        print("  %-6s %s" % ("SURVIVED" if ok else "caught", label))

    print("\nby family:")
    for fam in sorted(by_fam):
        c, t = by_fam[fam]
        print("  %-10s %d/%d" % (fam, c, t))
    print("\n%d injected, %d caught, %d survivors"
          % (len(MUTATIONS), len(MUTATIONS) - len(survivors), len(survivors)))
    for s in survivors:
        print("  SURVIVOR: %s" % s)
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
