#!/usr/bin/env python3
"""Mutation harness for the allium record corrections, round 3 (PLA-215).

Families: `pins` (pinned text, rung notes, shipped/unshipped shape, severity, sources), `hygiene`,
`retired` (each predicate family plus the whole-problem scan INCLUDING rung notes), `required`,
`survive`, `urls`, `uniform`, `blast`, `catalog`, `mechanics`.

WITHDRAWN, with the reason in the suite (`test_rung_shape_checks_are_FORWARD_assertions`): the
rung-count and duplicate-method checks in verify_post are forward assertions masked by the key-set
and rung-leaf-count checks. A forward assertion is not a gap; padding a harness total with one is
not coverage.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_allium_record_corrections_r3.py")
PROMOTE = os.path.join(HERE, "promote_allium_record_corrections_r3.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("pins: the table sizes are not asserted", "pins", PROMOTE,
     "    if sizes != want:", "    if False:"),
    ("pins: an undeclared target is accepted", "pins", PROMOTE,
     "        if key not in TARGETS:", "        if False:"),
    ("pins: a stale prose pin is accepted", "pins", PROMOTE,
     "        if p.get(field) != before:", "        if False:"),
    ("pins: a stale rung note pin is accepted", "pins", PROMOTE,
     "        if r.get(field) != before:", "        if False:"),
    ("pins: a rung note on an unshipped target is accepted", "pins", PROMOTE,
     "        if (slug, name) not in SHIPPED:\n            raise SystemExit(\"REFUSED: %s/%s is not a shipped target",
     "        if False:\n            raise SystemExit(\"REFUSED: %s/%s is not a shipped target"),
    ("pins: an unshipped target already carrying an id is accepted", "pins", PROMOTE,
     "        elif p.get(\"control_ladder\") is not None or p.get(\"id\") is not None:",
     "        elif False:"),
    ("pins: a shipped target without a ladder is accepted", "pins", PROMOTE,
     "            if not p.get(\"control_ladder\") or not p.get(\"id\"):", "            if False:"),
    ("pins: hygiene on a prose replacement is skipped", "pins", PROMOTE,
     "        bad = hygiene(after)\n        if bad:\n            raise SystemExit(\"REFUSED: %s/%s/%s replacement: %s\" % (slug, name, field,",
     "        bad = hygiene(after)\n        if False:\n            raise SystemExit(\"REFUSED: %s/%s/%s replacement: %s\" % (slug, name, field,"),
    ("pins: hygiene on a rung note replacement is skipped", "pins", PROMOTE,
     "        bad = hygiene(after)\n        if bad:\n            raise SystemExit(\"REFUSED: %s/%s/%s/%s replacement: %s\"",
     "        bad = hygiene(after)\n        if False:\n            raise SystemExit(\"REFUSED: %s/%s/%s/%s replacement: %s\""),
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
    ("pins: a cited id with no anchor is accepted", "pins", PROMOTE,
     '            if sid not in anchors and sid not in (p.get("anchoring_urls") or {}):',
     "            if False:"),
    ("pins: a target with no edit is accepted", "pins", PROMOTE,
     "        if (slug, name) not in {k for k in keys}:", "        if False:"),
    ("pins: an ambiguous problem name is accepted", "pins", PROMOTE,
     "    if len(hits) != 1:\n        raise SystemExit(\"REFUSED: %s has %d problems named",
     "    if False:\n        raise SystemExit(\"REFUSED: %s has %d problems named"),
    ("pins: an ambiguous rung method is accepted", "pins", PROMOTE,
     "    if len(hits) != 1:\n        raise SystemExit(\"REFUSED: %s/%s carries %d rungs",
     "    if False:\n        raise SystemExit(\"REFUSED: %s/%s carries %d rungs"),

    ("hygiene: the British list is emptied", "hygiene", PROMOTE,
     "    for pat in BRITISH:", "    for pat in ():"),
    ("hygiene: the absolute list is emptied", "hygiene", PROMOTE,
     "    for w in ABSOLUTES:", "    for w in ():"),
    ("hygiene: ladder vocabulary is no longer caught", "hygiene", PROMOTE,
     r'    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):', "    if False:"),
    ("hygiene: the false-attribution device is no longer caught", "hygiene", PROMOTE,
     r'''    if re.search(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)", s, re.I):''',
     "    if False:"),

    ("retired: the whole guard stops reporting", "retired", PROMOTE,
     "    if left:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)"),
    ("retired: rung notes are no longer scanned", "retired", PROMOTE,
     "    for r in p.get(\"control_ladder\") or []:\n        for k in (\"note_beginner\", \"note_seasoned\"):",
     "    for r in []:\n        for k in (\"note_beginner\", \"note_seasoned\"):"),
    ("retired: the residue pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"\bresidues?\b", s, re.I)), "the residue carryover mechanism")',
     r' [(t, lambda s: False, "the residue carryover mechanism")'),
    ("retired: the emergence pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"\bat (?:emergence|establishment)\b", s, re.I)),',
     r' [(t, lambda s: False and bool(re.search(r"\bat (?:emergence|establishment)\b", s, re.I)),'),
    ("retired: the debris-carryover pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"debris carries the pest over|carr(?:y|ies) over in (?:allium|old|leftover) "',
     r' [(t, lambda s: False and bool(re.search(r"debris carries the pest over|carr(?:y|ies) over in (?:allium|old|leftover) "'),
    ("retired: the debris-carryover pattern regresses to `carries?` (misses 'carry over')", "retired", PROMOTE,
     r'carr(?:y|ies) over in (?:allium|old|leftover) "', r'carries? over in (?:allium|old|leftover) "'),
    ("retired: the debris-carryover pattern loses its object (refuses 'allium ground')", "retired", PROMOTE,
     r'r"(?:\w+ )?(?:residue|debris|material|scraps)", s, re.I)),',
     r'r"", s, re.I)),'),
    ("retired: the false-attribution pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"\bthe guidance\b|guidance (?:names|asks|points)", s, re.I)),',
     r' [(t, lambda s: False and bool(re.search(r"\bthe guidance\b|guidance (?:names|asks|points)", s, re.I)),'),
    ("retired: the clean-stock pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"\bclean\b", s, re.I)), "the clean-stock claim") for t in _PINK_TARGETS] +',
     r' [(t, lambda s: False, "the clean-stock claim") for t in _PINK_TARGETS] +'),
    ("retired: the clean-stock pattern loses its word boundary (refuses 'cleanup')", "retired", PROMOTE,
     r're.search(r"\bclean\b", s, re.I)), "the clean-stock claim")',
     r're.search(r"clean", s, re.I)), "the clean-stock claim")'),
    ("retired: the senescing pattern is emptied", "retired", PROMOTE,
     r' [(_BOT, lambda s: bool(re.search(r"senesc", s, re.I)), "in-season senescing-leaf removal"),',
     r' [(_BOT, lambda s: False, "in-season senescing-leaf removal"),'),
    ("retired: the gray-mold pattern is emptied", "retired", PROMOTE,
     r'  (_BOT, lambda s: bool(re.search(r"gray fuzzy mold|gray sporulation|gray-mold", s, re.I)),',
     r'  (_BOT, lambda s: False and bool(re.search(r"gray fuzzy mold|gray sporulation|gray-mold", s, re.I)),'),
    ("retired: the splash pattern is emptied", "retired", PROMOTE,
     r'  (_BOT, lambda s: bool(re.search(r"splash", s, re.I)), "the splash-dispersal mechanism")]',
     r'  (_BOT, lambda s: False, "the splash-dispersal mechanism")]'),

    ("required: the whole guard stops reporting", "required", PROMOTE,
     "    if missing:\n        raise SystemExit(\"REFUSED: %r\" % missing)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % missing)"),
    ("required: only the first declared register is checked", "required", PROMOTE,
     "        for f in fields:\n            if not pat.search(p.get(f) or \"\"):",
     "        for f in fields[:1]:\n            if not pat.search(p.get(f) or \"\"):"),
    ("required: the trap-precondition pattern matches anything", "required", PROMOTE,
     r'_TRAP = re.compile(r"do not cover a bed that grew (?:alliums|leeks or onions|onions or leeks) last year|"',
     r'_TRAP = re.compile(r"|do not cover a bed that grew (?:alliums|leeks or onions|onions or leeks) last year|"'),
    ("required: the rotation-caveat pattern matches anything", "required", PROMOTE,
     r'   re.compile(r"rotation (?:reduces the disease rather than clearing it|helps but does not clear)", re.I),',
     r'   re.compile(r"", re.I),'),
    ("required: the leaf-wetness figure pattern matches anything", "required", PROMOTE,
     r' [(_BOT, ("symptoms_seasoned", "cause_seasoned"), re.compile(r"20 (?:or more hours|hours or more)"),',
     r' [(_BOT, ("symptoms_seasoned", "cause_seasoned"), re.compile(r""),'),

    ("survive: the guard stops reporting", "survive", PROMOTE,
     "            if ph not in blob:", "            if False:"),
    ("urls: the guard stops reporting", "urls", PROMOTE,
     "    if left:\n        raise SystemExit(\"REFUSED: retired anchors survive: %r\" % left)",
     "    if False:\n        raise SystemExit(\"REFUSED: retired anchors survive: %r\" % left)"),
    ("urls: the retired list is emptied", "urls", PROMOTE,
     "            for bad in RETIRED_URLS:", "            for bad in ():"),
    ("uniform: the guard stops reporting", "uniform", PROMOTE,
     "            if got != want:", "            if False:"),

    ("blast: an unpinned field on a target may change", "blast", PROMOTE,
     "        if k[-1] not in pinned.get(o, set()):", "        if False:"),
    ("blast: an unpinned rung note on a shipped target may change", "blast", PROMOTE,
     "            if (meth, k[-1]) not in rung_pins.get(o, set()):", "            if False:"),
    ("blast: a key added outside sources/anchors is accepted", "blast", PROMOTE,
     '        if "anchoring_urls" not in k and "sources" not in k:', "        if False:"),
    ("blast: a key added outside the declared targets is accepted", "blast", PROMOTE,
     "        if owner(k) not in want_owners:", "        if False:"),
    ("blast: the prose-change count is not pinned", "blast", PROMOTE,
     "    if n_prose != EXPECTED_PROSE:", "    if False:"),
    ("blast: the rung-note count is not pinned", "blast", PROMOTE,
     "    if n_rung != EXPECTED_RUNG_NOTES:", "    if False:"),
    ("blast: the severity count is not pinned", "blast", PROMOTE,
     "    if n_sev != EXPECTED_SEVERITY:", "    if False:"),
    ("blast: a prose replacement silently not applied is accepted", "blast", PROMOTE,
     "        if find_problem(data, slug, name).get(field) != after:\n            raise SystemExit(\"REFUSED: %s/%s/%s did not receive",
     "        if False:\n            raise SystemExit(\"REFUSED: %s/%s/%s did not receive"),
    ("blast: a rung note silently not applied is accepted", "blast", PROMOTE,
     "        if find_rung(data, slug, name, method).get(field) != after:", "        if False:"),
    ("blast: the new source list is not verified", "blast", PROMOTE,
     '        if p.get("sources") != list(after):', "        if False:"),
    ("blast: anchor keys need not match the source list", "blast", PROMOTE,
     '        if list(p.get("anchoring_urls") or {}) != list(after):', "        if False:"),
    ("blast: a wrong anchor URL is accepted", "blast", PROMOTE,
     '            if (p["anchoring_urls"].get(sid) or {}).get("url") != url:', "            if False:"),
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
    ("mechanics: a repointed anchor is kept instead of replaced", "mechanics", PROMOTE,
     "        for sid, url in anchors.items():\n            au[sid] = {\"url\": url, \"verified\": VERIFIED}",
     "        for sid, url in anchors.items():\n            au.setdefault(sid, {\"url\": url, \"verified\": VERIFIED})"),
    ("mechanics: the --canonical flag is ignored", "mechanics", PROMOTE,
     "    a.canonical = a.canonical_flag or a.canonical", "    pass"),
]

SENTINEL = ("SENTINEL: the prose replacements are never written", PROMOTE,
            "    for (slug, name, field), (_b, after) in PROSE.items():\n        find_problem(data, slug, name)[field] = after",
            "    for (slug, name, field), (_b, after) in PROSE.items():\n        _skip = after")


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
    wd = tempfile.mkdtemp(prefix="mutate_alliumrec3_")
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
    print("MUTATION HARNESS -- allium record corrections r3 (the repoint round)")
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
