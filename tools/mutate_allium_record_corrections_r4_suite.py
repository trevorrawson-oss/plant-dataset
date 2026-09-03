#!/usr/bin/env python3
"""Mutation harness for the allium record corrections, round 4 (PLA-215): onion thrips.

Families: `pins` (text, rung replacement shape, sources), `hygiene`, `retired`, `rung`, `required`,
`survive`, `chives`, `blast`, `catalog`, `mechanics`. Includes the anchor PREFLIGHT, a positive
control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_allium_record_corrections_r4.py")
PROMOTE = os.path.join(HERE, "promote_allium_record_corrections_r4.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("pins: the table sizes are not asserted", "pins", PROMOTE,
     "    if sizes != want:", "    if False:"),
    ("pins: an undeclared target is accepted", "pins", PROMOTE,
     "        if key not in TARGETS:", "        if False:"),
    ("pins: a stale prose pin is accepted", "pins", PROMOTE,
     "        if p.get(field) != before:", "        if False:"),
    ("pins: an identical replacement is accepted", "pins", PROMOTE,
     "        if after == before:", "        if False:"),
    ("pins: hygiene on a prose replacement is skipped", "pins", PROMOTE,
     "        bad = hygiene(after)\n        if bad:", "        bad = hygiene(after)\n        if False:"),
    ("pins: a rung at the wrong position is accepted", "pins", PROMOTE,
     "        if idx >= len(lad) or lad[idx].get(\"method\") != old:", "        if False:"),
    ("pins: an unknown replacement method is accepted", "pins", PROMOTE,
     "        if new not in cm:", "        if False:"),
    ("pins: a duplicated replacement method is accepted", "pins", PROMOTE,
     "        if any(r.get(\"method\") == new for r in lad):", "        if False:"),
    ("pins: a tier change at the position is accepted", "pins", PROMOTE,
     "        if cm[new].get(\"tier\") != cm[old].get(\"tier\"):", "        if False:"),
    ("pins: a replacement without applies_to any is accepted", "pins", PROMOTE,
     "        if \"any\" not in applies:", "        if False:"),
    ("pins: hygiene on a rung note is skipped", "pins", PROMOTE,
     "            bad = hygiene(note)\n            if bad:", "            bad = hygiene(note)\n            if False:"),
    ("pins: identical rung registers are accepted", "pins", PROMOTE,
     "        if nb.strip() == ns.strip():", "        if False:"),
    ("pins: a shipped target with no ladder is accepted", "pins", PROMOTE,
     "            if not p.get(\"control_ladder\") or not p.get(\"id\"):", "            if False:"),
    ("pins: an unshipped target carrying an id is accepted", "pins", PROMOTE,
     "        elif p.get(\"control_ladder\") is not None or p.get(\"id\") is not None:", "        elif False:"),
    ("pins: a stale source pin is accepted", "pins", PROMOTE,
     '        if p.get("sources") != before:', "        if False:"),
    ("pins: an id absent from source_catalog is accepted", "pins", PROMOTE,
     '            if sid not in data["source_catalog"]:', "            if False:"),
    ("pins: a cited id with no anchor is accepted", "pins", PROMOTE,
     "            if sid not in anchors:\n                raise SystemExit(\"REFUSED: %s/%s cites %r without a document anchor\"",
     "            if False:\n                raise SystemExit(\"REFUSED: %s/%s cites %r without a document anchor\""),
    ("pins: a half-edited target is accepted", "pins", PROMOTE,
     "        if not any(k[:2] == (slug, name) for k in PROSE) or (slug, name) not in SOURCES:", "        if False:"),

    ("hygiene: the absolute list is emptied", "hygiene", PROMOTE,
     "    for w in ABSOLUTES:", "    for w in ():"),
    ("hygiene: ladder vocabulary is no longer caught", "hygiene", PROMOTE,
     r'    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):', "    if False:"),

    ("retired: the whole guard stops reporting", "retired", PROMOTE,
     "    if left:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % left)\n    return len(RETIRED)"),
    ("retired: rung notes are no longer scanned", "retired", PROMOTE,
     "    for r in p.get(\"control_ladder\") or []:\n        for k in (\"note_beginner\", \"note_seasoned\"):",
     "    for r in []:\n        for k in (\"note_beginner\", \"note_seasoned\"):"),
    ("retired: the rotation pattern is emptied", "retired", PROMOTE,
     r'_ROTATE = re.compile(r"\brotat", re.I)', r'_ROTATE = re.compile(r"(?!x)x")'),
    ("retired: the same-spot pattern is emptied", "retired", PROMOTE,
     r'_SAME_SPOT = re.compile(r"do not plant (?:onions|shallots|leeks|garlic|alliums)[^.]*"',
     r'_SAME_SPOT = re.compile(r"(?!x)x"'),
    ("retired: the reflective pattern is emptied", "retired", PROMOTE,
     r' [(t, lambda s: bool(re.search(r"reflective|silver(?:ed|y)?\s+(?:mulch|plastic|film)", s, re.I)),',
     r' [(t, lambda s: False and bool(re.search(r"reflective|silver(?:ed|y)?\s+(?:mulch|plastic|film)", s, re.I)),'),

    ("rung: a surviving crop_rotation rung is accepted", "rung", PROMOTE,
     "            if r.get(\"method\") == \"crop_rotation\":", "            if False:"),
    ("rung: the replacement at the position is not verified", "rung", PROMOTE,
     "        if lad[idx].get(\"method\") != new:", "        if False:"),

    ("required: the whole guard stops reporting", "required", PROMOTE,
     "    if missing:\n        raise SystemExit(\"REFUSED: %r\" % missing)",
     "    if False:\n        raise SystemExit(\"REFUSED: %r\" % missing)"),
    ("required: only the first register is checked", "required", PROMOTE,
     "        for f in fields:\n            if not pat.search(p.get(f) or \"\"):",
     "        for f in fields[:1]:\n            if not pat.search(p.get(f) or \"\"):"),
    ("required: the tolerance pattern matches anything", "required", PROMOTE,
     r' [(t, ("management_seasoned",), re.compile(r"\btolerance\b"), "vigor as TOLERANCE") for t in TARGETS] +',
     r' [(t, ("management_seasoned",), re.compile(r""), "vigor as TOLERANCE") for t in TARGETS] +'),
    ("required: the volunteer pattern matches anything", "required", PROMOTE,
     r' [(t, ("management_seasoned",), re.compile(r"\bvolunteer"), "volunteer and debris sanitation")',
     r' [(t, ("management_seasoned",), re.compile(r""), "volunteer and debris sanitation")'),

    ("survive: the guard stops reporting", "survive", PROMOTE,
     "            if ph not in blob:", "            if False:"),
    ("chives: a chives change is accepted", "chives", PROMOTE,
     "    if moved:", "    if False:"),

    ("blast: an unpinned field on a target may change", "blast", PROMOTE,
     '        if k[-1] not in ("management_seasoned", "management_beginner"):\n            raise SystemExit("REFUSED: %s/%s/%s is not a pinned field of this promote"',
     '        if False:\n            raise SystemExit("REFUSED: %s/%s/%s is not a pinned field of this promote"'),
    ("blast: a leaf of the unreplaced rung may change", "blast", PROMOTE,
     "            if int(k[5][1:-1]) != rung_idx.get(o, -1) or k[-1] not in (\"method\", \"note_beginner\",",
     "            if False and (int(k[5][1:-1]) != rung_idx.get(o, -1) or k[-1] not in (\"method\", \"note_beginner\","),
    ("blast: a key added outside sources/anchors is accepted", "blast", PROMOTE,
     '        if "anchoring_urls" not in k and "sources" not in k:', "        if False:"),
    ("blast: a key added outside the declared targets is accepted", "blast", PROMOTE,
     "        if owner(k) not in want_owners:", "        if False:"),
    ("blast: the prose-change count is not pinned", "blast", PROMOTE,
     "    if n_prose != EXPECTED_PROSE:", "    if False:"),
    ("blast: the rung-leaf count is not pinned", "blast", PROMOTE,
     "    if n_rung != EXPECTED_RUNG_LEAVES:", "    if False:"),
    ("blast: a prose replacement silently not applied is accepted", "blast", PROMOTE,
     "        if find_problem(data, slug, name).get(field) != after:", "        if False:"),
    ("blast: a rung replacement silently not applied is accepted", "blast", PROMOTE,
     "        if (r.get(\"method\"), r.get(\"note_beginner\"), r.get(\"note_seasoned\")) != (new, nb, ns):",
     "        if False:"),
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
    wd = tempfile.mkdtemp(prefix="mutate_alliumrec4_")
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
    print("MUTATION HARNESS -- allium record corrections r4 (onion thrips)")
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
