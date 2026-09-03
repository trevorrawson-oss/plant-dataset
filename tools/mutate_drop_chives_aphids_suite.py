#!/usr/bin/env python3
"""Mutation harness for the chives aphids retirement (PLA-215).

Families: `target` attacks the pinned position and counts. `refs` attacks the join-key checks that
stop a REFERENCED problem being removed. `companions` attacks the assertion that the entry's one
useful claim outlives it. `finding` attacks the append-only amendment. `snapshot`, `blast`,
`catalog`, `mechanics` follow.

`companions` and `finding` are the families that matter, because this promote DELETES consumer
content. A removal is only safe if what the removed text carried is provably recorded elsewhere,
and only honest if the record that enumerated it is amended rather than silently falsified.

THREE ASSERTIONS ARE WITHDRAWN rather than reported as permanent survivors, each verified redundant
by construction and kept in the promote because it states the contract at the point a future edit
would break it. "The entry was not removed" is detectable by FOUR independent checks -- the
roster problem count, the crop pest count, the empty-dropped-set test, and the entry-still-present
test -- so disabling any one leaves the others to catch it, and no injection can isolate them. The
roster problem count is the one that does the work and it IS injected. A forward assertion is not a
gap, and padding a harness total with one is not coverage.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_drop_chives_aphids.py")
PROMOTE = os.path.join(HERE, "promote_drop_chives_aphids.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("target: the pest count is not asserted", "target", PROMOTE,
     "    if len(lst) != EXPECTED_PESTS_BEFORE:", "    if False:"),
    ("target: the pinned index is not checked", "target", PROMOTE,
     '    if lst[TARGET_INDEX].get("name") != TARGET_NAME:', "    if False:"),
    ("target: a duplicate name is accepted", "target", PROMOTE,
     '    if sum(1 for p in problems(c) if p.get("name") == TARGET_NAME) != 1:', "    if False:"),
    ("target: the pre-state roster count is not checked", "target", PROMOTE,
     "    if problem_count(data) != EXPECTED_PROBLEMS_BEFORE:", "    if False:"),
    ("target: a missing crop is accepted", "target", PROMOTE,
     "    if c is None:", "    if False:"),

    ("refs: a problem id on the target is accepted (join key orphaned)", "refs", PROMOTE,
     '    if target.get("id") is not None:', "    if False:"),
    ("refs: a shipped ladder on the target is accepted", "refs", PROMOTE,
     '    if target.get("control_ladder"):', "    if False:"),
    ("refs: resistance / ladder_delta references are not checked", "refs", PROMOTE,
     "        if key in blob:", "        if False:"),

    ("companions: the survival check stops firing", "companions", PROMOTE,
     "    if len(sites) < MIN_COMPANION_SITES:", "    if False:"),
    ("companions: the floor drops to zero", "companions", PROMOTE,
     "MIN_COMPANION_SITES = 5", "MIN_COMPANION_SITES = 0"),
    ("companions: the claim pattern is emptied", "companions", PROMOTE,
     'COMPANION_CLAIM = re.compile(r"aphid", re.I)', 'COMPANION_CLAIM = re.compile(r"(?!x)x")'),
    ("companions: the scan looks outside companions and finds it anywhere", "companions", PROMOTE,
     '    walk(by_slug(data)[CROP].get("companions") or {}, "companions")',
     '    walk(by_slug(data)[CROP], "crop")'),

    ("finding: the original wording need not be preserved", "finding", PROMOTE,
     "    if not got.startswith(original):", "    if False:"),
    ("finding: leaving it unamended is accepted", "finding", PROMOTE,
     "    if got == original:", "    if False:"),
    ("finding: the appended text need not be a CORRECTION", "finding", PROMOTE,
     '    if "[CORRECTION" not in got[len(original):]:', "    if False:"),
    ("finding: a missing finding is accepted", "finding", PROMOTE,
     '    raise SystemExit("REFUSED: chives has no open finding %r" % FINDING_ID)',
     '    return {"summary": ""}'),
    # NOT a syntax-breaking mutation: a promote that fails to IMPORT reddens the suite for the
    # wrong reason and counts as a false "caught". This one stays valid Python and simply strips the
    # dated marker, so the finding guard is what fires.
    ("finding: the appended text loses its CORRECTION marker", "finding", PROMOTE,
     '    " [CORRECTION 2026-09-03: the source-truth sample ran and the APHIDS entry has been REMOVED. No "',
     '    " Also a note. No "'),

    ("snapshot: problems go back to INDEX keying (a removal shifts the tail)", "snapshot", PROMOTE,
     '                    snap[("PROB", slug, fam, p.get("name"), k)] = json.dumps(',
     '                    snap[("PROB", slug, fam, str(id(p) % 7), k)] = json.dumps('),

    ("blast: added keys are accepted", "blast", PROMOTE,
     "    if added:", "    if False:"),
    ("blast: keys dropped outside the target are accepted", "blast", PROMOTE,
     "    if bad:", "    if False:"),
    ("blast: a change outside the finding is accepted", "blast", PROMOTE,
     '        if k[:2] != ("crop", CROP) or "open_findings" not in k:', "        if False:"),
    ("blast: the changed-leaf count is not pinned", "blast", PROMOTE,
     "    if len(changed) != 1:", "    if False:"),
    ("blast: the post roster count is not pinned", "blast", PROMOTE,
     "    if problem_count(data) != EXPECTED_PROBLEMS_AFTER:", "    if False:"),

    ("catalog: a control_methods change is accepted", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: a source_catalog change is accepted", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the entry is never actually removed", PROMOTE,
            '    c[TARGET_FAMILY] = [p for p in c[TARGET_FAMILY] if p.get("name") != TARGET_NAME]',
            '    _skip = [p for p in c[TARGET_FAMILY] if p.get("name") != TARGET_NAME]')


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
    wd = tempfile.mkdtemp(prefix="mutate_chivesaphid_")
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
    print("MUTATION HARNESS -- retire the chives aphids entry")
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
        print("  %-12s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(todo)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
