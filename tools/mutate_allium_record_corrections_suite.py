#!/usr/bin/env python3
"""Mutation harness for the allium record corrections, round 1 (PLA-215).

Families: `pins` attacks the pinned text, severity and source sets. `variety` attacks THE
MEASUREMENT -- the negation-aware check that distinguishes "choose a tolerant variety" from "there
is no resistant variety". `retired` attacks the per-claim removal assertions. `sources` attacks the
stale-citation check. `blast`, `catalog`, `mechanics` follow.

The `variety` family is the point. The first version of that guard pattern-matched the words and
refused this promote's own replacement text, which says there is NO resistant variety -- the
opposite claim. Every branch fired correctly; the predicate was wrong. Only assertions on the
predicate's behaviour find that, which is why `VarietyCheckRecognisesNegation` exists.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_allium_record_corrections_r1.py")
PROMOTE = os.path.join(HERE, "promote_allium_record_corrections_r1.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("pins: the table sizes are not asserted", "pins", PROMOTE,
     "    if len(PROSE) != EXPECTED_PROSE or len(SEVERITY) != EXPECTED_SEVERITY \\",
     "    if False and len(PROSE) != EXPECTED_PROSE or False and len(SEVERITY) != EXPECTED_SEVERITY \\"),
    ("pins: an undeclared target is accepted", "pins", PROMOTE,
     "        if (key[0], key[1]) not in TARGETS:", "        if False:"),
    ("pins: a stale prose pin is accepted", "pins", PROMOTE,
     "        if p.get(field) != before:", "        if False:"),
    ("pins: an identical replacement is accepted", "pins", PROMOTE,
     "        if after == before:", "        if False:"),
    ("pins: hygiene on the replacement is skipped", "pins", PROMOTE,
     "        bad = hygiene(after)\n        if bad:", "        bad = hygiene(after)\n        if False:"),
    ("pins: the British list is emptied", "pins", PROMOTE,
     "    for pat in BRITISH:", "    for pat in ():"),
    ("pins: the absolute list is emptied", "pins", PROMOTE,
     "    for w in ABSOLUTES:", "    for w in ():"),
    ("pins: a stale severity pin is accepted", "pins", PROMOTE,
     "        if got != before:", "        if False:"),
    ("pins: an unknown new severity is accepted", "pins", PROMOTE,
     '        if after not in ("low", "medium", "high"):', "        if False:"),
    ("pins: a stale source pin is accepted", "pins", PROMOTE,
     '        if p.get("sources") != before:', "        if False:"),
    ("pins: an id absent from source_catalog is accepted", "pins", PROMOTE,
     '            if sid not in data["source_catalog"]:', "            if False:"),
    ("pins: an anchor outside the new source list is accepted", "pins", PROMOTE,
     "            if sid not in after:", "            if False:"),
    ("pins: an ambiguous problem name is accepted", "pins", PROMOTE,
     "    if len(hits) != 1:", "    if False:"),

    ("variety: the check goes back to naive pattern matching (the real bug)", "variety", PROMOTE,
     "    for m in _VARIETY.finditer(text or \"\"):\n        if not _NEGATED.search(text[:m.start()]):\n"
     "            return True\n    return False",
     "    return bool(_VARIETY.search(text or \"\"))"),
    ("variety: the negation vocabulary is emptied", "variety", PROMOTE,
     r'_NEGATED = re.compile(r"\b(?:no|not|none|never|without|lack\w*)\b[^.]{0,60}$", re.I)',
     r'_NEGATED = re.compile(r"(?!x)x")'),
    ("variety: the check stops recognising a recommendation at all", "variety", PROMOTE,
     '_VARIETY = re.compile(r"(?:rust[- ])?(?:tolerant|resistant)[- ]?variet(?:y|ies)", re.I)',
     '_VARIETY = re.compile(r"(?!x)x")'),

    ("retired: the whole guard stops reporting", "retired", PROMOTE,
     "    if left:", "    if False:"),
    ("retired: only the edited field is scanned, not the whole problem", "retired", PROMOTE,
     "        for k, v in p.items():\n            if isinstance(v, str) and still_present(v):",
     "        for k, v in list(p.items())[:1]:\n            if isinstance(v, str) and still_present(v):"),
    ("retired: the fabricated-figure pattern is emptied", "retired", PROMOTE,
     r' (("shallot", "White rot"), lambda t: bool(re.search(r"20\s*(?:to|-)\s*30", t or "")),',
     r' (("shallot", "White rot"), lambda t: False,'),
    ("retired: the British-verb pattern is emptied", "retired", PROMOTE,
     r' (("leek", "Leek rust"), lambda t: bool(re.search(r"\bbin\b", t or "", re.I)),',
     r' (("leek", "Leek rust"), lambda t: False,'),
    ("retired: the UK seasonal pattern is emptied", "retired", PROMOTE,
     r'  lambda t: bool(re.search(r"mid-summer|late autumn|\bautumn\b", t or "", re.I)),',
     r'  lambda t: False,'),

    ("sources: a stale citation may survive", "sources", PROMOTE,
     "    if stale:", "    if False:"),
    ("sources: only `sources` is checked, not anchoring_urls", "sources", PROMOTE,
     '             if s in (p.get("sources") or []) or s in (p.get("anchoring_urls") or {})]',
     '             if s in (p.get("sources") or [])]'),

    ("blast: a key added outside sources/anchors is accepted", "blast", PROMOTE,
     '        if "anchoring_urls" not in k and "sources" not in k:', "        if False:"),
    ("blast: a key added outside the declared targets is accepted", "blast", PROMOTE,
     "        if owner(k) not in want_owners:", "        if False:"),
    ("blast: the prose-change count is not pinned", "blast", PROMOTE,
     "    if n_prose != EXPECTED_PROSE:", "    if False:"),
    ("blast: a replacement silently not applied is accepted", "blast", PROMOTE,
     "        if find_problem(data, slug, name).get(field) != after:", "        if False:"),
    ("blast: severity silently not applied is accepted", "blast", PROMOTE,
     '        if find_problem(data, slug, name).get("severity") != after:', "        if False:"),
    ("blast: the new source list is not verified", "blast", PROMOTE,
     '        if p.get("sources") != list(after):', "        if False:"),
    ("blast: anchor keys need not match the source list", "blast", PROMOTE,
     '        if list(p.get("anchoring_urls") or {}) != list(after):', "        if False:"),
    ("blast: changes outside the declared targets are accepted", "blast", PROMOTE,
     "    if touched - want_owners:", "    if False:"),

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

SENTINEL = ("SENTINEL: the prose replacements are never written", PROMOTE,
            "        find_problem(data, slug, name)[field] = after",
            "        _skip = after")


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
    wd = tempfile.mkdtemp(prefix="mutate_alliumrec_")
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
    print("MUTATION HARNESS -- allium record corrections r1")
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
