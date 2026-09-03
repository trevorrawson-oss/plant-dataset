#!/usr/bin/env python3
"""Mutation harness for the allium record corrections, round 2 (PLA-215).

Families: `pins` attacks the pinned text and source sets; `hygiene` empties each vocabulary list;
`retired` attacks each per-claim removal predicate and the whole-problem scan; `required` attacks
the presence checks and their per-register scan; `taxa`, `sources`, `sibling` attack the three
consistency guards; `blast`, `catalog`, `mechanics` follow.

`MatcherBehaviour` in the suite asserts the PREDICATES on constructed text in both directions.
The mutations here that weaken a predicate (a pattern emptied, a negation removed) are caught by
those assertions as well as by the positive controls, which is the point: a branch that fires on
the wrong number is invisible to a branch mutation, so the suite has to assert the number.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_allium_record_corrections_r2.py")
PROMOTE = os.path.join(HERE, "promote_allium_record_corrections_r2.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("pins: the table sizes are not asserted", "pins", PROMOTE,
     "    if len(PROSE) != EXPECTED_PROSE or len(SOURCES) != EXPECTED_SOURCE_SETS:",
     "    if False:"),
    ("pins: an undeclared target is accepted", "pins", PROMOTE,
     "        if (key[0], key[1]) not in TARGETS:", "        if False:"),
    ("pins: a stale prose pin is accepted", "pins", PROMOTE,
     "        if p.get(field) != before:", "        if False:"),
    ("pins: an identical replacement is accepted", "pins", PROMOTE,
     "        if after == before:", "        if False:"),
    ("pins: hygiene on the replacement is skipped", "pins", PROMOTE,
     "        bad = hygiene(after)\n        if bad:", "        bad = hygiene(after)\n        if False:"),
    ("pins: a stale source pin is accepted", "pins", PROMOTE,
     '        if p.get("sources") != before:', "        if False:"),
    ("pins: a duplicated source list is accepted", "pins", PROMOTE,
     "        if sorted(set(after)) != sorted(after) or not after:", "        if False:"),
    ("pins: an id absent from source_catalog is accepted", "pins", PROMOTE,
     '            if sid not in data["source_catalog"]:', "            if False:"),
    ("pins: an anchor outside the new source list is accepted", "pins", PROMOTE,
     "            if sid not in after:", "            if False:"),
    ("pins: a cited id with no document anchor is accepted", "pins", PROMOTE,
     "            if sid not in anchors:", "            if False:"),
    ("pins: a half-edited target is accepted", "pins", PROMOTE,
     "        if not any(k[:2] == (slug, name) for k in PROSE) or (slug, name) not in SOURCES:",
     "        if False:"),
    ("pins: an ambiguous problem name is accepted", "pins", PROMOTE,
     "    if len(hits) != 1:", "    if False:"),

    ("hygiene: the British list is emptied", "hygiene", PROMOTE,
     "    for pat in BRITISH:", "    for pat in ():"),
    ("hygiene: the absolute list is emptied", "hygiene", PROMOTE,
     "    for w in ABSOLUTES:", "    for w in ():"),
    ("hygiene: the false-attribution device is no longer caught", "hygiene", PROMOTE,
     r'''    if re.search(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)", s, re.I):''',
     "    if False:"),
    ("hygiene: ladder vocabulary is no longer caught", "hygiene", PROMOTE,
     r'    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):', "    if False:"),
    ("hygiene: spaced degF is no longer caught", "hygiene", PROMOTE,
     r'    if re.search(r"\d\s+°F", s):', "    if False:"),

    ("retired: the whole guard stops reporting", "retired", PROMOTE,
     "    if left:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)"),
    ("retired: only the first field is scanned, not the whole problem", "retired", PROMOTE,
     "        for k, v in p.items():\n            if isinstance(v, str) and still_present(v):",
     "        for k, v in list(p.items())[:1]:\n            if isinstance(v, str) and still_present(v):"),
    ("retired: the UK feeding-months pattern is emptied", "retired", PROMOTE,
     r' ((CROP, "Leek moth"), lambda t: bool(re.search(r"May to June|August to October", t or "")),',
     r' ((CROP, "Leek moth"), lambda t: False,'),
    ("retired: the two-generation pattern is emptied", "retired", PROMOTE,
     r' ((CROP, "Leek moth"), lambda t: bool(re.search(r"\btwo (?:generations|waves)\b", t or "", re.I)),',
     r' ((CROP, "Leek moth"), lambda t: False,'),
    ("retired: the two-generation pattern loses its word boundary (trips 'two to three')", "retired",
     PROMOTE,
     r'\btwo (?:generations|waves)\b', r'\btwo\b.*(?:generations|waves)\b'),
    ("retired: the moth cover-during pattern is emptied", "retired", PROMOTE,
     r'  lambda t: bool(re.search(r"through the flight periods|during late spring and late summer|"' "\n"
     r'                           r"when the moths are active", t or "", re.I)),',
     "  lambda t: False,"),
    ("retired: the RHS window pattern is emptied", "retired", PROMOTE,
     r'  lambda t: bool(re.search(r"March to April|September to November", t or "")),',
     "  lambda t: False,"),
    ("retired: the leafminer cover-during pattern is emptied", "retired", PROMOTE,
     r'  lambda t: bool(re.search(r"during the (?:two )?flight periods|when the flies are active",' "\n"
     r'                           t or "", re.I)),',
     "  lambda t: False,"),
    ("retired: the soil-only pattern is emptied", "retired", PROMOTE,
     r'  lambda t: bool(re.search(r"pupae in the soil\b", t or "", re.I)),',
     "  lambda t: False,"),
    ("retired: the soil-only pattern widens to any 'soil' (refuses correct text)", "retired", PROMOTE,
     r'pupae in the soil\b', r'the soil'),

    ("required: the whole guard stops reporting", "required", PROMOTE,
     "    if missing:\n        raise SystemExit(\"REFUSED: %r\" % missing)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % missing)"),
    ("required: only the first declared register is checked", "required", PROMOTE,
     "        for f in fields:\n            if not pat.search(p.get(f) or \"\"):",
     "        for f in fields[:1]:\n            if not pat.search(p.get(f) or \"\"):"),
    ("required: the cover-before pattern matches anything", "required", PROMOTE,
     r'  re.compile(r"\bbefore\b"), "cover BEFORE the moths emerge"),',
     r'  re.compile(r""), "cover BEFORE the moths emerge"),'),
    ("required: the generation-count pattern matches 'two generations' too", "required", PROMOTE,
     r'  re.compile(r"\btwo (?:to|or) three (?:generations|rounds)\b"), "the two-to-three generation count"),',
     r'  re.compile(r"\btwo\b"), "the two-to-three generation count"),'),
    ("required: the late-cover evidence pattern matches anything", "required", PROMOTE,
     r'  re.compile(r"\btwo weeks\b"), "the UMass late-cover evidence"),',
     r'  re.compile(r""), "the UMass late-cover evidence"),'),

    ("taxa: the guard stops reporting", "taxa", PROMOTE,
     "        if taxon not in blob:", "        if False:"),

    ("sources: a stale citation may survive", "sources", PROMOTE,
     "    if stale:", "    if False:"),
    ("sources: only `sources` is checked, not anchoring_urls", "sources", PROMOTE,
     '        if RETIRED_SOURCE in (p.get("sources") or []) or RETIRED_SOURCE in (p.get("anchoring_urls") or {}):',
     '        if RETIRED_SOURCE in (p.get("sources") or []):'),

    ("sibling: a sibling losing the phrase is accepted (guard goes vacuous)", "sibling", PROMOTE,
     "        if SIBLING_PHRASE not in blob:", "        if False:"),
    ("sibling: leek not carrying the phrase is accepted", "sibling", PROMOTE,
     "    if not hits:", "    if False:"),

    ("blast: a key added outside sources/anchors is accepted", "blast", PROMOTE,
     '        if "anchoring_urls" not in k and "sources" not in k:', "        if False:"),
    ("blast: a key added outside the declared targets is accepted", "blast", PROMOTE,
     "        if owner(k) not in want_owners:", "        if False:"),
    ("blast: the prose-change count is not pinned", "blast", PROMOTE,
     "    if n_prose != EXPECTED_PROSE:", "    if False:"),
    ("blast: a replacement silently not applied is accepted", "blast", PROMOTE,
     "        if find_problem(data, slug, name).get(field) != after:", "        if False:"),
    ("blast: the new source list is not verified", "blast", PROMOTE,
     '        if p.get("sources") != list(after):', "        if False:"),
    ("blast: anchor keys need not match the source list", "blast", PROMOTE,
     '        if list(p.get("anchoring_urls") or {}) != list(after):', "        if False:"),
    ("blast: a wrong anchor URL is accepted", "blast", PROMOTE,
     '            if (p["anchoring_urls"].get(sid) or {}).get("url") != url:', "            if False:"),
    ("blast: a severity change on a target is accepted", "blast", PROMOTE,
     "        if k:\n            raise SystemExit(\"REFUSED: %s/%s severity changed; not in scope\" % (slug, name))",
     "        if False:\n            raise SystemExit(\"REFUSED: %s/%s severity changed; not in scope\" % (slug, name))"),
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
    ("mechanics: the --canonical flag is ignored", "mechanics", PROMOTE,
     "    a.canonical = a.canonical_flag or a.canonical", "    pass"),
    ("mechanics: the umd anchor is kept instead of repointed", "mechanics", PROMOTE,
     "        for sid, url in anchors.items():\n            au[sid] = {\"url\": url, \"verified\": VERIFIED}",
     "        for sid, url in anchors.items():\n            au.setdefault(sid, {\"url\": url, \"verified\": VERIFIED})"),
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
    wd = tempfile.mkdtemp(prefix="mutate_alliumrec2_")
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
    print("MUTATION HARNESS -- allium record corrections r2 (leek moth + leek allium leaf miner)")
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
