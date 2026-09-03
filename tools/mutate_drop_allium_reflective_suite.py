#!/usr/bin/env python3
"""Mutation harness for the allium reflective-mulch removal (PLA-215).

Families: `pins` attacks the pinned text, position and ladder shape. `protected` attacks the
assertion that the PEAS keep theirs -- the guard that stops one crop's reason being blanketed
across another's. `coverage` attacks the completeness assertion. `snapshot` attacks the
content-keying that makes a REMOVAL diffable at all. `blast`, `catalog`, `mechanics` follow.

The `snapshot` family matters because this is the repo's first promote that REMOVES a rung. A
path-keyed snapshot reports every rung after the removed one as dropped-and-re-added, which drowns
the single real removal in noise and makes the blast-radius assertion meaningless.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_drop_allium_reflective_mulch.py")
PROMOTE = os.path.join(HERE, "promote_drop_allium_reflective_mulch.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("pins: the edit count is not asserted", "pins", PROMOTE,
     "    if len(PROSE_EDITS) != EXPECTED_PROSE_EDITS:", "    if False:"),
    ("pins: a replacement that still names reflective mulch is accepted", "pins", PROMOTE,
     "    if AFTER == BEFORE or REFLECTIVE.search(AFTER):", "    if False:"),
    ("pins: a non-allium crop can be edited", "pins", PROMOTE,
     "        if slug not in ALLIUM_THRIPS:", "        if False:"),
    ("pins: a stale prose pin is accepted", "pins", PROMOTE,
     "        if find_problem(data, slug, name).get(field) != BEFORE:", "        if False:"),
    ("pins: a wrong ladder length is accepted", "pins", PROMOTE,
     "    if len(lad) != ladder_len:", "    if False:"),
    ("pins: a wrong rung position is accepted", "pins", PROMOTE,
     '    if lad[idx].get("method") != method:', "    if False:"),
    ("pins: an ambiguous duplicate method is accepted", "pins", PROMOTE,
     '    if sum(1 for r in lad if r.get("method") == method) != 1:', "    if False:"),
    ("pins: an ambiguous problem name is accepted", "pins", PROMOTE,
     "    if len(hits) != 1:", "    if False:"),

    ("protected: a pea entry may change", "protected", PROMOTE,
     "    if moved:", "    if False:"),
    ("protected: the pea rung count is not pinned", "protected", PROMOTE,
     "    if n != EXPECTED_PROTECTED_RUNGS:", "    if False:"),
    ("protected: the protected crop list is emptied", "protected", PROMOTE,
     'PROTECTED = ("sugar-snap-peas", "snow-peas")', "PROTECTED = ()"),
    ("protected: the peas are swept into the allium list", "protected", PROMOTE,
     'ALLIUM_THRIPS = ("garlic", "onion", "shallot", "leek", "spring-onion")',
     'ALLIUM_THRIPS = ("garlic", "onion", "shallot", "leek", "spring-onion",\n'
     '                 "sugar-snap-peas", "snow-peas")'),

    ("coverage: leftover prose is accepted", "coverage", PROMOTE,
     "                if isinstance(v, str) and REFLECTIVE.search(v):", "                if False:"),
    ("coverage: a leftover rung is accepted", "coverage", PROMOTE,
     '                if r.get("method") == "reflective_mulch":', "                if False:"),
    ("coverage: the guard stops reporting", "coverage", PROMOTE,
     "    if left:", "    if False:"),
    ("coverage: the denominator shrinks to only the edited crops", "coverage", PROMOTE,
     "    for slug in ALLIUM_THRIPS:\n        c = by_slug(data).get(slug)",
     "    for slug in [e[0] for e in PROSE_EDITS]:\n        c = by_slug(data).get(slug)"),

    ("snapshot: rungs go back to PATH keying (a removal shifts the tail)", "snapshot", PROMOTE,
     '                        snap[("RUNG", slug, p.get("name"), r.get("method"), k)] = v',
     '                        snap[("RUNG", slug, p.get("name"), str(i), k)] = v'),
    ("snapshot: the ladder is left in the path walk as well", "snapshot", PROMOTE,
     '                p.pop("control_ladder", None)', "                pass"),

    ("blast: added keys are accepted", "blast", PROMOTE,
     "    if added:", "    if False:"),
    ("blast: the dropped set is not pinned to the removed rung", "blast", PROMOTE,
     "    if dropped != want_dropped:", "    if False:"),
    ("blast: the changed-leaf count is not pinned", "blast", PROMOTE,
     "    if len(changed) != EXPECTED_PROSE_EDITS:", "    if False:"),
    ("blast: the changed-leaf IDENTITY is not pinned", "blast", PROMOTE,
     "    if changed != want_changed:", "    if False:"),
    ("blast: the post rung total is not pinned", "blast", PROMOTE,
     "    if rung_count(data) != EXPECTED_RUNGS_AFTER:", "    if False:"),

    ("catalog: a control_methods change is accepted", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: a source_catalog change is accepted", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: the pre-state rung total is not checked", "mechanics", PROMOTE,
     "    if rung_count(data) != EXPECTED_RUNGS_BEFORE:", "    if False:"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the rung is never actually removed", PROMOTE,
            '    p["control_ladder"] = [r for r in p["control_ladder"] if r.get("method") != method]',
            '    _skip = [r for r in p["control_ladder"] if r.get("method") != method]')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1], SENTINEL[2])]
    for label, f, old in rows:
        with open(f) as fh:
            n = fh.read().count(old)
        if n != 1:
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_reflective_")
    with open(SUITE) as fh:
        src = fh.read()
    src = src.replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    with open(os.path.join(wd, os.path.basename(SUITE)), "w") as fh:
        fh.write(src)
    with open(PROMOTE) as fh:
        s = fh.read()
    s = s.replace("REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
                  "REPO = %r" % REPO, 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    with open(os.path.join(wd, os.path.basename(PROMOTE)), "w") as fh:
        fh.write(s)
    if path:
        with open(os.path.join(wd, os.path.basename(path))) as fh:
            if MARKER not in fh.read():
                shutil.rmtree(wd)
                raise SystemExit("HARNESS DEAD: marker absent")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- drop reflective mulch from the allium thrips advice")
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

    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    todo = [m for m in MUTATIONS if not only or m[1] in only]
    caught = survived = 0
    fam = {}
    for label, family, f, old, new in todo:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print("  SURVIVED  [%s] %s" % (family, label))
        else:
            caught += 1; fam[family][0] += 1
            print("  caught    [%s] %s" % (family, label))
        sys.stdout.flush()

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print("  %-11s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(todo)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
