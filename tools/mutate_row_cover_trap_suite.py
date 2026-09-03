#!/usr/bin/env python3
"""Mutation harness for the row-cover trap-precondition promote (PLA-215).

Families. `targets` attacks the pin table and its size/crop assertions. `adds` attacks the
append-only property that makes this promote incapable of rewriting shipped prose. `clauses`
attacks the precondition test, the hygiene families and the anti-template similarity ceiling.
`coverage` attacks the assertion that makes the fix COMPLETE rather than merely applied. `regex`
attacks THE MEASUREMENT. `blast`, `catalog` and `mechanics` follow.

THE `regex` FAMILY IS THE POINT. Both mutations in it are bugs that were actually written and
actually shipped into a dry run during this promote's authoring: `brassica\\b` (which does not match
"brassicas" and so refused a correct clause) and an enclosure pattern that allowed no object between
the verb and "in" (so "seal emerging flies in" did not match, while shipped house prose depends on
exactly that shape). Neither was a broken branch -- every branch fired correctly -- and neither
would have been caught by injecting a defect into the data. They were caught by asserting the
matcher's behaviour directly. A harness proves a guard FIRES; only assertions on the measurement
prove it MEASURES the right thing.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_row_cover_trap_precondition.py")
PROMOTE = os.path.join(HERE, "promote_row_cover_trap_precondition.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- targets -----------------------------------------------------------------------------
    ("targets: the edit-table size is not asserted", "targets", PROMOTE,
     "    if len(EDITS) != EXPECTED_EDITS:", "    if False:"),
    ("targets: the crop count is not asserted", "targets", PROMOTE,
     "    if len(crops) != EXPECTED_CROPS:", "    if False:"),
    ("targets: a target outside the known row-cover rungs is accepted", "targets", PROMOTE,
     "        if (slug, pid) not in ALL_ROW_COVER_RUNGS:", "        if False:"),
    ("targets: editing an already-correct crop is accepted", "targets", PROMOTE,
     "        if (slug, pid) in ALREADY_CORRECT:", "        if False:"),
    ("targets: a STALE PIN is accepted (writes over text that moved)", "targets", PROMOTE,
     "        if r.get(field) != before:", "        if False:"),
    ("targets: a missing crop is accepted", "targets", PROMOTE,
     "    if c is None:", "    if False:"),
    ("targets: a missing rung is accepted", "targets", PROMOTE,
     '            raise SystemExit("REFUSED: %s/%s has no %s rung" % (slug, pid, method))',
     '            return {"note_beginner": "", "note_seasoned": ""}'),

    # ---- adds --------------------------------------------------------------------------------
    ("adds: the append-only property is removed", "adds", PROMOTE,
     "        if not after.startswith(before):", "        if False:"),
    ("adds: a replacement that adds nothing is accepted", "adds", PROMOTE,
     "        if len(after) <= len(before):", "        if False:"),

    # ---- clauses -----------------------------------------------------------------------------
    ("clauses: a clause missing the precondition is accepted", "clauses", PROMOTE,
     "        if not has_precondition(clause):", "        if False:"),
    ("clauses: has_precondition stops requiring BOTH halves (condition only)", "clauses", PROMOTE,
     "    return bool(PRIOR_CROP.search(text or \"\")) and bool(ENCLOSURE.search(text or \"\"))",
     "    return bool(PRIOR_CROP.search(text or \"\"))"),
    ("clauses: has_precondition stops requiring BOTH halves (consequence only)", "clauses",
     PROMOTE,
     "    return bool(PRIOR_CROP.search(text or \"\")) and bool(ENCLOSURE.search(text or \"\"))",
     "    return bool(ENCLOSURE.search(text or \"\"))"),
    ("clauses: hygiene is not applied", "clauses", PROMOTE,
     "        bad = hygiene(clause)\n        if bad:", "        bad = hygiene(clause)\n        if False:"),
    ("clauses: the em/en dash check is removed", "clauses", PROMOTE,
     '    if "—" in s or "–" in s:', "    if False:"),
    ("clauses: the absolute vocabulary is emptied", "clauses", PROMOTE,
     '    for w in ("always", "completely", "totally", "harmless", "guaranteed", "eliminate",\n'
     '              "eliminates"):',
     "    for w in ():"),
    ("clauses: the British-usage list is emptied", "clauses", PROMOTE,
     "    for pat, label in BRITISH:", "    for pat, label in ():"),
    ("clauses: ladder vocabulary is accepted", "clauses", PROMOTE,
     "    if LADDER_VOCAB.search(s):", "    if False:"),
    ("clauses: the similarity ceiling stops firing", "clauses", PROMOTE,
     "            if s >= CLAUSE_SIMILARITY_CEILING:", "            if False:"),
    ("clauses: the similarity ceiling is loosened past the measured worst", "clauses", PROMOTE,
     "CLAUSE_SIMILARITY_CEILING = 0.70", "CLAUSE_SIMILARITY_CEILING = 0.99"),
    ("clauses: the similarity metric loses autojunk=False", "clauses", PROMOTE,
     "            s = max(difflib.SequenceMatcher(None, clauses[a], clauses[b], autojunk=False).ratio(),\n"
     "                    difflib.SequenceMatcher(None, clauses[b], clauses[a], autojunk=False).ratio())",
     "            s = max(difflib.SequenceMatcher(None, clauses[a], clauses[b]).ratio(),\n"
     "                    difflib.SequenceMatcher(None, clauses[b], clauses[a]).ratio())"),
    ("clauses: the anti-vacuity branch is removed", "clauses", PROMOTE,
     "    if not keys:", "    if False:"),

    # ---- coverage ----------------------------------------------------------------------------
    ("coverage: the beginner-register requirement is removed", "coverage", PROMOTE,
     '        if not has_precondition(r.get("note_beginner") or ""):', "        if False:"),
    ("coverage: the seasoned-register requirement is removed", "coverage", PROMOTE,
     '        if not PRIOR_CROP.search(r.get("note_seasoned") or ""):', "        if False:"),
    ("coverage: the whole guard stops reporting", "coverage", PROMOTE,
     "    if missing:", "    if False:"),
    ("coverage: the denominator shrinks to only the crops this promote edits", "coverage", PROMOTE,
     "    for slug, pid in ALL_ROW_COVER_RUNGS:\n        r = find_rung(data, slug, pid)\n"
     '        if not has_precondition(r.get("note_beginner") or ""):',
     "    for slug, pid in [(k[0], k[1]) for k in EDITS]:\n        r = find_rung(data, slug, pid)\n"
     '        if not has_precondition(r.get("note_beginner") or ""):'),
    ("coverage: the beginner register only has to name the condition", "coverage", PROMOTE,
     '        if not has_precondition(r.get("note_beginner") or ""):\n'
     '            missing.append("%s/%s/note_beginner (needs condition AND consequence)" % (slug, pid))',
     '        if not PRIOR_CROP.search(r.get("note_beginner") or ""):\n'
     '            missing.append("%s/%s/note_beginner (needs condition AND consequence)" % (slug, pid))'),

    # ---- regex: THE MEASUREMENT ---------------------------------------------------------------
    ("regex: PRIOR_CROP goes plural-blind again (the real bug: brassica vs brassicas)", "regex",
     PROMOTE,
     '_CROP_WORDS = r"(?:cabbage[- ]family|brassicas?|crucifers?|alliums?|onions?)"',
     '_CROP_WORDS = r"(?:cabbage[- ]family|brassica|crucifer|allium|onion)"'),
    ("regex: PRIOR_CROP loses the reverse word order", "regex", PROMOTE,
     'PRIOR_CROP = re.compile(r"%s\\b[^.]{0,90}?%s|%s[^.]{0,90}?%s\\b"\n'
     "                        % (_CROP_WORDS, _PRIOR_WORDS, _PRIOR_WORDS, _CROP_WORDS), re.I)",
     'PRIOR_CROP = re.compile(r"%s\\b[^.]{0,90}?%s"\n'
     "                        % (_CROP_WORDS, _PRIOR_WORDS), re.I)"),
    ("regex: PRIOR_CROP loses 'earlier' (the turnip false negative)", "regex", PROMOTE,
     '_PRIOR_WORDS = r"(?:last (?:year|season)|previous|earlier|recently|grew|carried|grown|been out of)"',
     '_PRIOR_WORDS = r"(?:last (?:year|season)|previous|recently|grew|carried|grown|been out of)"'),
    ("regex: ENCLOSURE allows no object between the verb and 'in' (the real bug)", "regex",
     PROMOTE,
     r'    r"(?:seal|shut|trap|hold|held|holds|enclos)\w*\s+(?:\w+\s+){0,3}?in\b"',
     r'    r"(?:seal|shut|trap|hold|held|holds|enclos)\w*\s+(?:them\s+)?in\b"'),
    ("regex: ENCLOSURE goes plural-blind on 'traps'", "regex", PROMOTE,
     r'    r"|\btrap(?:s|ped|ping)?\b"', r'    r"|\btrap\b"'),
    ("regex: PRIOR_CROP accepts a bare rotation instruction", "regex", PROMOTE,
     'PRIOR_CROP = re.compile(r"%s\\b[^.]{0,90}?%s|%s[^.]{0,90}?%s\\b"\n'
     "                        % (_CROP_WORDS, _PRIOR_WORDS, _PRIOR_WORDS, _CROP_WORDS), re.I)",
     'PRIOR_CROP = re.compile(r"rotat|%s\\b[^.]{0,90}?%s|%s[^.]{0,90}?%s\\b"\n'
     "                        % (_CROP_WORDS, _PRIOR_WORDS, _PRIOR_WORDS, _CROP_WORDS), re.I)"),

    # ---- blast -------------------------------------------------------------------------------
    ("blast: an added leaf key is accepted", "blast", PROMOTE,
     "    if added:", "    if False:"),
    ("blast: a dropped leaf key is accepted", "blast", PROMOTE,
     "    if dropped:", "    if False:"),
    ("blast: the changed-leaf count is not pinned", "blast", PROMOTE,
     "    if len(changed) != EXPECTED_EDITS:", "    if False:"),
    ("blast: a change outside a rung register is accepted", "blast", PROMOTE,
     '        if path[0] != "crops" or path[-1] not in ("note_beginner", "note_seasoned"):',
     "        if False:"),
    ("blast: a replacement silently not applied is accepted", "blast", PROMOTE,
     "        if find_rung(data, slug, pid).get(field) != after:", "        if False:"),
    ("blast: the touched-crop set is not pinned", "blast", PROMOTE,
     "    if seen != want_crops:", "    if False:"),
    ("blast: the snapshot stops covering the catalogs", "blast", PROMOTE,
     "    walk(data, ())", '    walk({"crops": data["crops"]}, ())'),

    # ---- catalog -----------------------------------------------------------------------------
    ("catalog: a control_methods change is accepted", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: a source_catalog change is accepted", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    # ---- mechanics ---------------------------------------------------------------------------
    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the replacements are never written", PROMOTE,
            "        find_rung(data, slug, pid)[field] = after",
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
    wd = tempfile.mkdtemp(prefix="mutate_rowcover_")
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
                raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- row-cover trap precondition")
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
    if only:
        print("filter           : families %s -> %d mutations\n" % (",".join(only), len(todo)))

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
