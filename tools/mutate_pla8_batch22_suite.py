#!/usr/bin/env python3
"""Mutation harness for the batch-22 promote (PLA-215).

Families: `premise` attacks the FULL-schema premise in both directions (prose present, note pair
absent) plus the per-crop `severity` asymmetry. `types` attacks the two-sided split-by-crop rule --
both the set-from-nothing side and the upgrade side, and both coverage counts. `ids` attacks the
convention table (keyed by crop AND name here), the refusals, the reuse anchors and the id-set
coverage assertion. `singular` attacks the guard carried from batch 21, including its refusal on a
PARTIAL repair. `scope` attacks the two compound-vs-single id adjudications, each anchored on the
organism rather than on the id string. `template` attacks the guard this batch's measurement
selected -- the batch 3 defect made mechanical -- including both of its anti-vacuity branches.
`echo`, `temps`, `vocab`, `materials`, `validate`, `blast`, `catalog`, `mechanics` as before.

Every disabled branch has a driver asserting its ONE specific message. Batch 21's two survivors
were both anti-vacuity branches with no driver, so every anti-vacuity branch here is injected
individually rather than assumed covered by the guard's main path.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch22.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch22.py")
STAGING_NAME = "pla8_batch22_stragglers"
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise --------------------------------------------------------------------------------
    ("premise: a missing batch crop is accepted", "premise", PROMOTE,
     "        if c not in by:", "        if False:"),
    ("premise: an already-laddered crop is accepted", "premise", PROMOTE,
     '            if p.get("control_ladder"):\n                raise SystemExit("REFUSED: %s/%s '
     'is already laddered" % (c, p.get("name")))',
     '            if False:\n                raise SystemExit("REFUSED: %s/%s '
     'is already laddered" % (c, p.get("name")))'),
    ("premise: a missing prose field is accepted", "premise", PROMOTE,
     '                if not str(p.get(f) or "").strip():', "                if False:"),
    ("premise: a NOTE-schema conversion is accepted", "premise", PROMOTE,
     "                if f in p:", "                if False:"),
    ("premise: missing sources/anchoring_urls is accepted", "premise", PROMOTE,
     '                if not p.get(f):', "                if False:"),
    ("premise: the severity asymmetry is not pinned", "premise", PROMOTE,
     "            if has != want:", "            if False:"),
    ("premise: the coverage count is not pinned", "premise", PROMOTE,
     "    if seen != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- types ----------------------------------------------------------------------------------
    ("types: the rule need not cover every crop", "types", PROMOTE,
     "    if set(SET_FROM_NOTHING) | set(UPGRADE_FROM_COARSE) != set(CROPS):", "    if False:"),
    ("types: a pre-existing type on the SET side is accepted", "types", PROMOTE,
     "                    if pre is not None:", "                    if False:"),
    ("types: a non-coarse pre type on the UPGRADE side is accepted", "types", PROMOTE,
     "                    if pre not in COARSE_TYPES:", "                    if False:"),
    ("types: the wrong coarse value for the family is accepted", "types", PROMOTE,
     "                    if pre != want_coarse:", "                    if False:"),
    ("types: a non-enum post type is accepted", "types", PROMOTE,
     "                if post not in _TYPE_TARGETS:", "                if False:"),
    ("types: an id missing from EXPECTED_TYPES is accepted", "types", PROMOTE,
     "                if want is None:\n                    raise SystemExit(\"REFUSED: %s/%s not "
     "in EXPECTED_TYPES\" % (c, o.get(\"id\")))",
     "                if False:\n                    raise SystemExit(\"REFUSED: %s/%s not "
     "in EXPECTED_TYPES\" % (c, o.get(\"id\")))"),
    ("types: the post type need not match the pin", "types", PROMOTE,
     "                if post != want:", "                if False:"),
    ("types: the two-sided coverage counts are not pinned", "types", PROMOTE,
     "    if (set_n, upgraded) != (want_set, want_up):", "    if False:"),

    # ---- ids ------------------------------------------------------------------------------------
    ("ids: an arity mismatch is accepted", "ids", PROMOTE,
     "            if len(names) != len(got):", "            if False:"),
    ("ids: an unknown (crop, name) pair is accepted", "ids", PROMOTE,
     "                if want is None:\n                    raise SystemExit(\"REFUSED: (%s, %r) "
     "not in ID_CONVENTION\" % (c, n))",
     "                if False:\n                    raise SystemExit(\"REFUSED: (%s, %r) "
     "not in ID_CONVENTION\" % (c, n))"),
    ("ids: the convention table is never enforced", "ids", PROMOTE,
     "                if i != want:", "                if False:"),
    ("ids: the refusal table is never consulted", "ids", PROMOTE,
     "                if i in REFUSED_IDS:", "                if False:"),
    ("ids: a reused id resolving nowhere is accepted", "ids", PROMOTE,
     "        if i not in existing:", "        if False:"),
    ("ids: a reused id losing its anchor is accepted", "ids", PROMOTE,
     "        if anchor not in existing[i]:", "        if False:"),
    ("ids: a new id that already exists is accepted", "ids", PROMOTE,
     "        if i in existing:", "        if False:"),
    ("ids: the id-set COVERAGE assertion is disabled", "ids", PROMOTE,
     "    if taken != set(REUSED_IDS) | set(NEW_IDS):", "    if False:"),

    # ---- singular -------------------------------------------------------------------------------
    ("singular: a minority singular id may be taken", "singular", PROMOTE,
     "        if sing in taken:", "        if False:"),
    ("singular: a majority FLIP no longer refuses", "singular", PROMOTE,
     "            if len(s) >= len(p):", "            if False:"),
    ("singular: a PARTIAL repair no longer refuses", "singular", PROMOTE,
     "    if live != len(SINGULAR_PLURAL_PAIRS):", "    if False:"),

    # ---- scope ----------------------------------------------------------------------------------
    ("scope: the batch may take the WIDER-scope id", "scope", PROMOTE,
     "        if shorter in taken:", "        if False:"),
    ("scope: dropping the mint no longer refuses", "scope", PROMOTE,
     "        if mint not in taken:", "        if False:"),
    ("scope: the wider id vanishing from the roster is accepted", "scope", PROMOTE,
     "        if shorter not in off:", "        if False:"),
    ("scope: the holder set may drift", "scope", PROMOTE,
     "        if set(off[shorter]) != set(holders):", "        if False:"),
    ("scope: a holder losing the wider marker is accepted", "scope", PROMOTE,
     "            if wider_marker.lower() not in blob.lower():", "            if False:"),
    ("scope: the batch record may lose its own organism", "scope", PROMOTE,
     "        if own_marker.lower() not in blob.lower():", "        if False:"),
    ("scope: the batch record may grow into the wider scope", "scope", PROMOTE,
     "        if wider_marker.lower() in blob.lower():", "        if False:"),
    ("scope: a missing batch record is accepted", "scope", PROMOTE,
     "        if src is None:", "        if False:"),
    ("scope: the adjudication count is not pinned", "scope", PROMOTE,
     "    if not SCOPE_VARIANTS or checked != len(SCOPE_VARIANTS) or checked != 2:",
     "    if False:"),

    # ---- template -------------------------------------------------------------------------------
    ("template: an UNPINNED divergence on identical prose is accepted", "template", PROMOTE,
     "                    if pin is None:", "                    if False and pin is None:"),
    ("template: a pinned divergence of the wrong SHAPE is accepted", "template", PROMOTE,
     "                    if (extra, miss) != pin:", "                    if False:"),
    ("template: twin detection is disabled (every pair looks divergent)", "template", PROMOTE,
     "                    if prose_key(src) != prose_key(q):", "                    if True:"),
    ("template: the no-twins anti-vacuity check is disabled", "template", PROMOTE,
     "    if twins == 0:", "    if False:"),
    ("template: the unreachable-pin anti-vacuity check is disabled", "template", PROMOTE,
     "    if pinned_hit == 0:", "    if False:"),
    ("template: the prose comparison ignores treatment prose", "template", PROMOTE,
     "    return tuple((f, p.get(f)) for f in PROSE_FIELDS)",
     '    return tuple((f, p.get(f)) for f in PROSE_FIELDS[:2])'),

    # ---- echo -----------------------------------------------------------------------------------
    ("echo: a verbatim whole-note echo is accepted", "echo", PROMOTE,
     "                    if v in whole:", "                    if False:"),
    ("echo: a sentence-level echo is accepted", "echo", PROMOTE,
     "                        if s in sent:", "                        if False:"),
    ("echo: the shipped-corpus anti-vacuity check is disabled", "echo", PROMOTE,
     "    if not whole:", "    if False:"),
    ("echo: the batch-scan anti-vacuity check is disabled", "echo", PROMOTE,
     "    if checked == 0:", "    if False:"),
    ("echo: the sentence floor swallows every sentence", "echo", PROMOTE,
     "if len(s.strip()) > 40]", "if len(s.strip()) > 100000]"),

    # ---- temps / vocab --------------------------------------------------------------------------
    ("temps: the temperature scan finds nothing", "temps", PROMOTE,
     "                    m = TEMP_FIGURE.search(r[f])", "                    m = None"),
    ("temps: the temperature anti-vacuity check is disabled", "temps", PROMOTE,
     "    if seen == 0:\n        raise SystemExit(\"REFUSED: no notes scanned for temperatures; "
     "this guard would be vacuous\")",
     "    if False:\n        raise SystemExit(\"REFUSED: no notes scanned for temperatures; "
     "this guard would be vacuous\")"),
    ("vocab: the ladder-vocabulary scan finds nothing", "vocab", PROMOTE,
     "                    m = LADDER_VOCAB.search(r[f])", "                    m = None"),
    ("vocab: the vocabulary anti-vacuity check is disabled", "vocab", PROMOTE,
     "    if seen == 0:\n        raise SystemExit(\"REFUSED: no notes scanned for vocabulary; "
     "this guard would be vacuous\")",
     "    if False:\n        raise SystemExit(\"REFUSED: no notes scanned for vocabulary; "
     "this guard would be vacuous\")"),

    # ---- materials ------------------------------------------------------------------------------
    ("materials: a material outside MATERIAL_OK is accepted", "materials", PROMOTE,
     "                    if m not in ok:", "                    if False:"),

    # ---- validate -------------------------------------------------------------------------------
    ("validate: an unknown method is accepted", "validate", PROMOTE,
     "                if m not in cm:", "                if False:"),
    ("validate: a duplicate method is accepted", "validate", PROMOTE,
     "                if m in seen:", "                if False:"),
    ("validate: a tier decrease is accepted", "validate", PROMOTE,
     "                if t < last:", "                if False:"),
    ("validate: applies_to incoherence is accepted", "validate", PROMOTE,
     '                if "any" not in applies and not _type_ok(p["type"], applies):',
     "                if False:"),
    ("validate: identical registers are accepted", "validate", PROMOTE,
     '                if r.get("note_beginner", "").strip() == r.get("note_seasoned", "").strip():',
     "                if False:"),
    ("validate: a missing rung note is accepted", "validate", PROMOTE,
     '                    if not (r.get(f) or "").strip():', "                    if False:"),
    ("validate: copy hygiene is not enforced", "validate", PROMOTE,
     "                    if bad:", "                    if False:"),
    ("validate: an extra key on a rung is accepted", "validate", PROMOTE,
     '                if set(r) != {"method", "note_beginner", "note_seasoned"}:',
     "                if False:"),
    ("validate: an empty ladder is accepted", "validate", PROMOTE,
     '            if not L:\n                raise SystemExit("REFUSED: %s/%s empty ladder"',
     '            if False:\n                raise SystemExit("REFUSED: %s/%s empty ladder"'),
    ("validate: a problem with no type is accepted", "validate", PROMOTE,
     '            if not p.get("type"):', "            if False:"),
    ("validate: the per-crop problem count is not pinned", "validate", PROMOTE,
     "        if len(probs) != EXPECTED_PROBLEMS[c]:", "        if False:"),
    ("validate: the per-crop rung count is not pinned", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[c]:", "        if False:"),
    ("validate: the TOTAL rung count is not pinned", "validate", PROMOTE,
     "    if rung_count(batch) != TOTAL_RUNGS:", "    if False:"),
    ("validate: the hygiene absolute list is emptied", "validate", PROMOTE,
     '    for w in ("always", "never", "completely", "harmless", "guaranteed"):',
     "    for w in ():"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: the problem-set equality check is disabled", "blast", PROMOTE,
     "    if set(pre) != set(post):", "    if False:"),
    ("blast: a bystander crop may change", "blast", PROMOTE,
     "        if k[0] not in CROPS:", "        if False:"),
    ("blast: the touched count is not pinned", "blast", PROMOTE,
     "    if touched != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- catalog --------------------------------------------------------------------------------
    ("catalog: control_methods may be mutated", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: source_catalog may be mutated", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the base SHA is not enforced", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
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
    wd = tempfile.mkdtemp(prefix="mutate_batch22_")
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
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 22, the stragglers")
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
        print("  %-11s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(MUTATIONS)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
