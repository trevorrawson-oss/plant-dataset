#!/usr/bin/env python3
"""Mutation harness for the batch-23 promote (PLA-215).

Families: `premise` attacks the FULL-schema premise in both directions plus the severity pin.
`types` attacks the uniform coarse -> fine upgrade on both sides and its coverage count. `ids`
attacks the positional pin table and its coverage assertion. `scope` attacks the two kingdom-level
taxon collisions and the three scope variants, each anchored on the ORGANISM or the scope reason
rather than on the id string, plus the taxon REUSE anchor. `stem` attacks the singular/plural class
an exact-id check cannot see -- including the STEMMER ITSELF, whose first version turned "beetles"
into "beetl" while "beetle" stayed "beetle", so the guard silently skipped the exact pair it exists
for. `twins` attacks the ASSERTED vacuity of batch 22's dropped divergence guard. `precedent`
attacks the guard this batch's measurement selected. `echo`, `temps`, `vocab`, `validate`, `blast`,
`catalog`, `mechanics` follow.

Two guards were LIFTED OUT of main() so this harness can reach them -- a guard that only exists
inside an entry point the suite never calls is untested code wearing a guard's clothes.

Every anti-vacuity branch is injected individually rather than assumed covered by its guard's main
path: batch 21's two survivors were both anti-vacuity branches with no driver.

TWO assertions are WITHDRAWN rather than injected, each verified unreachable by construction and
documented at its site in the promote: `validate`'s total rung count (the sum of per-crop counts
already pinned one line above) and `blast`'s per-crop tally (forced once the touched count is 22,
since only batch crops can be touched and their maxima sum to exactly 22). A forward assertion is
not a gap, and padding a harness total with one is not coverage.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch23.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch23.py")
STAGING_NAME = "pla8_batch23_roots"
MARKER = "# MUTATION-APPLIED"

OFF = "        if False:"

MUTATIONS = [
    # ---- premise ---------------------------------------------------------------------------
    ("premise: a missing batch crop is accepted", "premise", PROMOTE,
     "        if c not in by:", "        if False:"),
    ("premise: a problem-count drift is accepted", "premise", PROMOTE,
     "        if len(got) != EXPECTED_PROBLEMS[c]:", "        if False:"),
    ("premise: an already-laddered target is accepted", "premise", PROMOTE,
     '            if p.get("control_ladder") is not None:', "            if False:"),
    ("premise: a pre-existing id is accepted", "premise", PROMOTE,
     '            if p.get("id") is not None:', "            if False:"),
    ("premise: a missing full-schema field is accepted", "premise", PROMOTE,
     '                if not (p.get(f) or "").strip():', "                if False:"),
    ("premise: a NOTE-schema field is accepted", "premise", PROMOTE,
     "                if f in p:", "                if False:"),
    ("premise: a missing severity is accepted", "premise", PROMOTE,
     '            if not p.get("severity"):', "            if False:"),
    ("premise: missing sources/anchoring_urls is accepted", "premise", PROMOTE,
     '            if not p.get("sources") or not p.get("anchoring_urls"):', "            if False:"),
    ("premise: the coverage count is not pinned", "premise", PROMOTE,
     '    if seen != sum(EXPECTED_PROBLEMS.values()):\n'
     '        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"',
     '    if False:\n'
     '        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"'),

    # ---- types -----------------------------------------------------------------------------
    ("types: a non-coarse pre-state type is accepted", "types", PROMOTE,
     '                if p.get("type") != coarse:', "                if False:"),
    ("types: a staged type off the pin is accepted", "types", PROMOTE,
     '                if o.get("type") != want:', "                if False:"),
    ("types: a type left at the coarse default is accepted", "types", PROMOTE,
     '                if o.get("type") == coarse:', "                if False:"),
    ("types: a length mismatch is accepted", "types", PROMOTE,
     "            if len(pre) != len(post):", "            if False:"),
    ("types: the coverage count is not pinned", "types", PROMOTE,
     '    if seen != sum(EXPECTED_PROBLEMS.values()):\n'
     '        raise SystemExit("REFUSED: type upgrade scanned %d, expected %d"',
     '    if False:\n'
     '        raise SystemExit("REFUSED: type upgrade scanned %d, expected %d"'),

    # ---- ids -------------------------------------------------------------------------------
    ("ids: the pin table size is not asserted", "ids", PROMOTE,
     "    if len(ID_CONVENTION) != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),
    ("ids: a canonical name drift is accepted", "ids", PROMOTE,
     '        if pre[i].get("name") != name:', "        if False:"),
    ("ids: a staged id off the pin is accepted", "ids", PROMOTE,
     '        if post[i].get("id") != pid:', "        if False:"),
    ("ids: the pin COVERAGE assertion is removed", "ids", PROMOTE,
     "    if seen != positions:", "    if False:"),
    ("ids: a duplicate id within a crop is accepted", "ids", PROMOTE,
     "        if len(ids) != len(set(ids)):", "        if False:"),

    # ---- scope -----------------------------------------------------------------------------
    ("scope: a stale scope pin is accepted", "scope", PROMOTE,
     "        if new_id not in staged_ids:", "        if False:"),
    ("scope: a 'minted' id that is already live is accepted", "scope", PROMOTE,
     "        if new_id in live:", "        if False:"),
    ("scope: the resembled id vanishing is accepted", "scope", PROMOTE,
     "        if resembles not in live:", "        if False:"),
    ("scope: the batch's own scope reason vanishing is accepted", "scope", PROMOTE,
     "        if own_reason and own_reason.lower() not in blob.lower():", "        if False:"),
    ("scope: the taxon-collision organism vanishing is accepted", "scope", PROMOTE,
     "            if other_reason.lower() not in oblob.lower():", "            if False:"),
    ("scope: a taxon-REUSE pin missing from the batch is accepted", "scope", PROMOTE,
     "        if pid not in staged_ids:", "        if False:"),
    ("scope: the precedent crop losing the id is accepted", "scope", PROMOTE,
     "        if not hit:", "        if False:"),
    ("scope: the taxon-reuse phrase vanishing is accepted", "scope", PROMOTE,
     "        if phrase.lower() not in blob.lower():", "        if False:"),

    # ---- stem ------------------------------------------------------------------------------
    ("stem: an unadjudicated stem variant is accepted", "stem", PROMOTE,
     '                if (p["id"], lid) not in STEM_VARIANT_PINS:', "                if False:"),
    ("stem: the adjudicated-pair count is not pinned", "stem", PROMOTE,
     "    if pinned != EXPECTED_STEM_VARIANT_HITS:", "    if False:"),
    ("stem: THE STEMMER goes plural-blind again (the original bug)", "stem", PROMOTE,
     '        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:', "        elif False:"),

    # ---- twins -----------------------------------------------------------------------------
    ("twins: a template twin appearing is accepted", "twins", PROMOTE,
     "                    if tuple(pp.get(f) for f in PROSE_FIELDS) == key:",
     "                    if False:"),
    ("twins: the anti-vacuity branch is removed", "twins", PROMOTE,
     '    if compared == 0:\n'
     '        raise SystemExit("REFUSED: no shipped problems compared; the twin premise is '
     'unproven")',
     '    if False:\n'
     '        raise SystemExit("REFUSED: no shipped problems compared; the twin premise is '
     'unproven")'),

    # ---- precedent -------------------------------------------------------------------------
    ("precedent: a rung copied from its precedent crop is accepted", "precedent", PROMOTE,
     "                    if s >= PRECEDENT_COPY_THRESHOLD:", "                    if False:"),
    ("precedent: the anti-vacuity branch is removed", "precedent", PROMOTE,
     '    if compared == 0:\n'
     '        raise SystemExit("REFUSED: check_no_precedent_copy made 0 comparisons; it is '
     'vacuous. "',
     '    if False:\n'
     '        raise SystemExit("REFUSED: check_no_precedent_copy made 0 comparisons; it is '
     'vacuous. "'),
    ("precedent: the threshold is loosened past the measured ceiling", "precedent", PROMOTE,
     "PRECEDENT_COPY_THRESHOLD = 0.70", "PRECEDENT_COPY_THRESHOLD = 0.99"),

    # ---- echo ------------------------------------------------------------------------------
    ("echo: a whole-note echo is accepted", "echo", PROMOTE,
     "                    if v in whole:", "                    if False:"),
    ("echo: a sentence echo is accepted", "echo", PROMOTE,
     "                        if s in sent:", "                        if False:"),
    ("echo: the empty-corpus anti-vacuity branch is removed", "echo", PROMOTE,
     "    if not whole:", "    if False:"),
    ("echo: the no-notes-scanned anti-vacuity branch is removed", "echo", PROMOTE,
     "    if checked == 0:", "    if False:"),

    # ---- temps -----------------------------------------------------------------------------
    ("temps: an unwarranted temperature figure is accepted", "temps", PROMOTE,
     "                            if not (in_src or in_meth):", "                            if False:"),
    ("temps: the pinned figure count is removed", "temps", PROMOTE,
     "    if found != EXPECTED_TEMP_FIGURES:", "    if False:"),

    # ---- vocab -----------------------------------------------------------------------------
    ("vocab: internal ladder vocabulary is accepted", "vocab", PROMOTE,
     "                    if m:", "                    if False:"),
    ("vocab: the anti-vacuity branch is removed", "vocab", PROMOTE,
     "    if seen == 0:", "    if False:"),

    # ---- validate --------------------------------------------------------------------------
    ("validate: an empty ladder is accepted", "validate", PROMOTE,
     "            if not ladder:", "            if False:"),
    ("validate: an unknown method is accepted", "validate", PROMOTE,
     "                if meth not in cm:", "                if False:"),
    ("validate: a duplicate method in one ladder is accepted", "validate", PROMOTE,
     "                if meth in seen_methods:", "                if False:"),
    ("validate: a tier inversion is accepted", "validate", PROMOTE,
     "                if TIERS.index(tier) < last:", "                if False:"),
    ("validate: an applies_to incoherence is accepted", "validate", PROMOTE,
     '                if "any" not in applies and not _type_ok(p.get("type"), applies):',
     "                if False:"),
    ("validate: a missing register is accepted", "validate", PROMOTE,
     "                if not nb or not ns:", "                if False:"),
    ("validate: identical registers are accepted", "validate", PROMOTE,
     "                if nb.strip() == ns.strip():", "                if False:"),
    ("validate: an unexpected rung key is accepted", "validate", PROMOTE,
     '                if set(r) - {"method", "note_beginner", "note_seasoned"}:',
     "                if False:"),
    ("validate: a hygiene violation is accepted", "validate", PROMOTE,
     "                    if bad:", "                    if False:"),
    ("validate: the per-crop rung count is not pinned", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[c]:", "        if False:"),
    ("validate: the absolute vocabulary is emptied", "validate", PROMOTE,
     '    for w in ("always", "never", "completely", "totally", "harmless", "guaranteed",\n'
     '              "eliminate", "eliminates"):',
     '    for w in ():'),

    # ---- blast -----------------------------------------------------------------------------
    ("blast: an unexpected ADDED leaf key is accepted", "blast", PROMOTE,
     "    if unexpected_add:", "    if False:"),
    ("blast: a DROPPED leaf key is accepted", "blast", PROMOTE,
     "    if dropped:", "    if False:"),
    ("blast: the added-key count is not pinned", "blast", PROMOTE,
     "    if len(added) != 2 * sum(EXPECTED_PROBLEMS.values()):", "    if False:"),
    ("blast: a bystander crop change is accepted", "blast", PROMOTE,
     '        if k[0] not in CROPS:', "        if False:"),
    ("blast: a change to an unexpected FIELD is accepted", "blast", PROMOTE,
     '        if k[3] != "type":', "        if False:"),
    ("blast: the touched-problem count is not pinned", "blast", PROMOTE,
     "    if len(touched) != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- catalog ---------------------------------------------------------------------------
    ("catalog: a control_methods change is accepted", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: a source_catalog change is accepted", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    # ---- mechanics -------------------------------------------------------------------------
    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the ladders are never attached", PROMOTE,
            '                p["control_ladder"] = copy.deepcopy(o["control_ladder"])',
            '                _skip = copy.deepcopy(o["control_ladder"])')


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
    wd = tempfile.mkdtemp(prefix="mutate_batch23_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", STAGING_NAME)
    for fn in os.listdir(src_staging):
        if fn.startswith("out_"):
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "%s")' % STAGING_NAME,
        "STAGING = %r" % sandbox_staging, 1)
    # The sandbox copy sits in a temp dir, so its own dirname(dirname(__file__)) would point REPO
    # at /tmp -- breaking CANONICAL, the tools/ import path, and any driver that runs this file as
    # a SUBPROCESS. Pin REPO to the real repo; only STAGING is meant to differ.
    s = s.replace(
        "REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
        "REPO = %r" % REPO, 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 23, the roots")
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
