#!/usr/bin/env python3
"""Mutation harness for the batch-21 promote (PLA-215).

Families: `premise` attacks the NOTE-schema premise in both directions (note pair present, full
schema absent). `types` attacks the set-from-nothing rule. `ids` attacks the convention table, the
five refusals and the sixteen reuse anchors. `singular` attacks a guard whose premise is three live
roster defects, including its refusal when they are repaired. `inversion` attacks the companion
inversion carried from batches 15/16. `bt` attacks a CONTENT ruling in both directions -- the
removal from viola and the retention on nasturtium. `echo` attacks the guard this batch's
measurement selected over shape comparison. `temps`, `vocab`, `materials`, `validate`, `blast`,
`catalog`, `mechanics` as before.

Every disabled branch has a driver asserting its ONE specific message.
Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch21.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch21.py")
STAGING_NAME = "pla8_batch21_flowers"
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise --------------------------------------------------------------------------------
    ("premise: a missing batch crop is accepted", "premise", PROMOTE,
     "        if c not in by:", "        if False:"),
    ("premise: an already-laddered crop is accepted", "premise", PROMOTE,
     '            if p.get("control_ladder"):', "            if False:"),
    ("premise: a missing note is accepted", "premise", PROMOTE,
     '                if not str(p.get(f) or "").strip():', "                if False:"),
    ("premise: a FULL-SCHEMA conversion is accepted", "premise", PROMOTE,
     "                if f in p:", "                if False:"),

    # ---- types ----------------------------------------------------------------------------------
    ("types: a pre-existing type no longer breaks the premise", "types", PROMOTE,
     '                if p.get("type") is not None:', "                if False:"),
    ("types: a non-enum post type is accepted", "types", PROMOTE,
     '                if o.get("type") not in _TYPE_TARGETS:', "                if False:"),
    ("types: the coverage count is not pinned", "types", PROMOTE,
     "    if checked != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- ids ------------------------------------------------------------------------------------
    ("ids: an arity mismatch is accepted", "ids", PROMOTE,
     "            if len(names) != len(got):", "            if False:"),
    ("ids: an unknown problem name is accepted", "ids", PROMOTE,
     "                if want is None:", "                if False:"),
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

    # ---- singular -------------------------------------------------------------------------------
    ("singular: a minority singular id may be taken", "singular", PROMOTE,
     "        if sing in taken:", "        if False:"),
    ("singular: a majority FLIP no longer refuses", "singular", PROMOTE,
     "            if len(s) >= len(p):", "            if False:"),
    ("singular: the guard passes once every split is repaired", "singular", PROMOTE,
     "    if live == 0:", "    if False:"),

    # ---- inversion ------------------------------------------------------------------------------
    ("inversion: trap_cropping is accepted", "inversion", PROMOTE,
     "                if m in ms:", "                if False:"),
    ("inversion: trap/decoy vocabulary in a note is accepted", "inversion", PROMOTE,
     '                    if re.search(r"\\b%s\\w*\\b" % w, blob):', "                    if False:"),
    ("inversion: forbidding an absent method is not caught as vacuous", "inversion", PROMOTE,
     '    if "trap_cropping" not in cm:', "    if False:"),
    ("inversion: the note-scan anti-vacuity check is disabled", "inversion", PROMOTE,
     "    if seen_notes == 0:", "    if False:"),

    # ---- bt -------------------------------------------------------------------------------------
    ("bt: a bt rung on the BUTTERFLY HOST is accepted", "bt", PROMOTE,
     "            if c in BT_FORBIDDEN_CROPS:", "            if False:"),
    ("bt: a bt rung outside its pinned home is accepted", "bt", PROMOTE,
     "            if key not in BT_ALLOWED:", "            if False:"),
    ("bt: losing the PERMITTED bt rung is accepted", "bt", PROMOTE,
     "    if found != BT_ALLOWED:", "    if False:"),

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
     'if len(s.strip()) > 40]', "if len(s.strip()) > 100000]"),

    # ---- temps / vocab --------------------------------------------------------------------------
    ("temps: the temperature scan finds nothing", "temps", PROMOTE,
     "                    m = TEMP_FIGURE.search(r[f])", "                    m = None"),
    ("vocab: the ladder-vocabulary scan finds nothing", "vocab", PROMOTE,
     "                    m = LADDER_VOCAB.search(r[f])", "                    m = None"),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch21_")
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
    print("MUTATION HARNESS -- PLA-8 batch 21, flowers")
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
