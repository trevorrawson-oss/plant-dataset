#!/usr/bin/env python3
"""Mutation harness for the thin-ladder backfill promote (PLA-215).

Families: `additive` attacks the guards that keep this from rewriting shipped content -- the pinned
prior sequence, the byte-identical existing rungs, and the untouched record prose. That family is
the point of this promote, because it is the FIRST in the arc to edit already-laddered crops.
`warrants` attacks the guard requiring every added rung to be traceable to a phrase in its own
record, which is what would have caught the thin-ladder scan's four false positives. `shape` attacks
the rung and ladder validity checks. `hygiene` attacks the copy rules. `blast` attacks the
post-state set and bystander comparisons. `mechanics` attacks the SHA, the serializer, and the
WIRING of both guards into `main`.

The wiring mutations are present from the start, per the r8 lesson.

WITHDRAWN, not missing: verify_post's added-rung COUNT is a FORWARD assertion. Every ladder is
pinned to its `expect_after` immediately above it, so once those match the number added is
fixed by construction and no post-state mutation can reach it. Per the convention, a
genuinely unreachable forward assertion is documented and withdrawn rather than left
reported as a permanent survivor.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_thin_ladder_backfill.py")
PROMOTE = os.path.join(HERE, "promote_pla8_thin_ladder_backfill.py")
CONTENT = os.path.join(HERE, "build_pla8_thin_ladder_backfill_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- additive -------------------------------------------------------------------------------
    ("additive: a DRIFTED prior ladder is accepted", "additive", PROMOTE,
     "        if before != spec[\"expect_before\"]:", "        if False:"),
    ("additive: a rung may be DROPPED", "additive", PROMOTE,
     "        if dropped:", "        if False:"),
    ("additive: the added set need not match the declared prose", "additive", PROMOTE,
     '        if sorted(added) != sorted(spec["add"]):', "        if False:"),
    ("additive: the post ladder need not match expect_after", "additive", PROMOTE,
     '        if after != spec["expect_after"]:', "        if False:"),
    ("additive: an EXISTING rung's prose may be rewritten", "additive", PROMOTE,
     "                if r != old[r[\"method\"]]:", "                if False:"),
    ("additive: the RECORD prose may be edited", "additive", PROMOTE,
     '            if (p.get(f) or "") != (before_p.get(f) or ""):', "            if False:"),
    ("additive: the added-rung count is not pinned (check)", "additive", PROMOTE,
     "    if total_added != C.EXPECTED_NEW_RUNGS:", "    if False:"),
    ("additive: the problem count is not pinned", "additive", PROMOTE,
     "    if len(C.BACKFILL) != C.EXPECTED_PROBLEMS:", "    if False:"),
    ("additive: the crop set is not pinned", "additive", PROMOTE,
     "    if tuple(sorted({s for s, _ in C.BACKFILL})) != tuple(sorted(C.EXPECTED_CROPS)):",
     "    if False:"),
    ("additive: apply_round skips the expect_before assertion", "additive", CONTENT,
     '        if before != spec["expect_before"]:', "        if False:"),

    # ---- warrants -------------------------------------------------------------------------------
    ("warrants: a rung with NO declared warrant is accepted", "warrants", PROMOTE,
     "            if phrase is None:", "            if False:"),
    ("warrants: a warrant absent from the record is accepted", "warrants", PROMOTE,
     "            if phrase.lower() not in blob:", "            if False:"),
    ("warrants: the warrant coverage count is not pinned", "warrants", PROMOTE,
     "    if seen != C.EXPECTED_NEW_RUNGS:", "    if False:"),
    ("warrants: the WARRANTS table need not cover the added rungs", "warrants", PROMOTE,
     "    if set(C.WARRANTS) != {(s, p, m) for (s, p), sp in C.BACKFILL.items()",
     "    if False and set(C.WARRANTS) != {(s, p, m) for (s, p), sp in C.BACKFILL.items()"),
    ("warrants: check_warrants is never called by check", "warrants", PROMOTE,
     "    return check_warrants(data)", "    return None"),
    ("warrants: a warrant phrase is falsified in the CONTENT", "warrants", CONTENT,
     '    ("beet", "common-scab", "lower_soil_ph"): "do not lime",',
     '    ("beet", "common-scab", "lower_soil_ph"): "apply elemental sulfur",'),

    # ---- shape ----------------------------------------------------------------------------------
    ("shape: a missing target problem is accepted", "shape", PROMOTE,
     "        if p is None:\n            return f\"{slug}/{pid} is not on the roster\"\n        before =",
     "        if False:\n            return f\"{slug}/{pid} is not on the roster\"\n        before ="),
    ("shape: an unknown method is accepted", "shape", PROMOTE,
     "            if m not in cm:", "            if False:"),
    ("shape: a duplicate method is accepted", "shape", PROMOTE,
     "            if m in seen:", "            if False:"),
    ("shape: a tier decrease is accepted", "shape", PROMOTE,
     "            if t < last:", "            if False:"),
    ("shape: applies_to incoherence is accepted", "shape", PROMOTE,
     '            if "any" not in applies and not (set(TYPE_TARGETS.get(p.get("type"), ())) & set(applies)):',
     "            if False:"),
    ("shape: an extra rung key is accepted", "shape", PROMOTE,
     "            if set(rung) != set(ADVICE_FIELDS):", "            if False:"),
    ("shape: identical registers are accepted", "shape", PROMOTE,
     '            if rung["note_beginner"].strip() == rung["note_seasoned"].strip():',
     "            if False:"),
    ("shape: a missing note is accepted", "shape", PROMOTE,
     "                if not rung[f].strip():", "                if False:"),

    # ---- hygiene --------------------------------------------------------------------------------
    ("hygiene: the copy check is disabled", "hygiene", PROMOTE,
     "                bad = hygiene(rung[f])", "                bad = None"),
    ("hygiene: absolutes are allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     "    if False:"),
    ("hygiene: a spaced degF is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\d\\s+°F", s):', "    if False:"),
    ("hygiene: markdown emphasis is allowed", "hygiene", PROMOTE,
     '    if "**" in s or "__" in s:', "    if False:"),
    ("hygiene: a double hyphen is allowed", "hygiene", PROMOTE,
     '    if "--" in s:', "    if False:"),
    ("hygiene: an em dash is allowed", "hygiene", PROMOTE,
     '    if re.search(r"[—–]", s):', "    if False:"),
    ("hygiene: British spellings are allowed", "hygiene", PROMOTE,
     "    for w in BRITISH:", "    for w in ():"),
    ("hygiene: a bare safety claim is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:is|are)\\s+safe\\b", s, re.I):', "    if False:"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: the problem SET may change", "blast", PROMOTE,
     '    if set(pre["problems"]) != set(post["problems"]):', "    if False:"),
    ("blast: a BYSTANDER problem may change", "blast", PROMOTE,
     "        if (slug, p.get(\"id\")) not in targets:", "        if False:"),
    ("blast: the changed-problem count is not pinned", "blast", PROMOTE,
     "    if len(changed) != C.EXPECTED_PROBLEMS:", "    if False:"),
    ("blast: control_methods may change", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', "    if False:"),
    ("blast: source_catalog may change", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the base SHA is not enforced", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: check() is never called by main", "mechanics", PROMOTE,
     "    problem = check(data)\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)",
     "    problem = None\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)"),
    ("mechanics: verify_post() is never called by main", "mechanics", PROMOTE,
     "    problem = verify_post(pre, data)\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)",
     "    problem = None\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)"),
]

SENTINEL = ("SENTINEL: the rungs are never actually attached", CONTENT,
            '        prob["control_ladder"] = rebuilt',
            '        _skip = rebuilt')


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
    wd = tempfile.mkdtemp(prefix="mutate_backfill_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 thin-ladder backfill")
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
