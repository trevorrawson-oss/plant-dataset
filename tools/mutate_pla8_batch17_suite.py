#!/usr/bin/env python3
"""Mutation harness for the batch-17 promote (PLA-215).

Families: `schema` attacks the full-schema premise (stone fruit is NOT note-shaped, unlike batches
15/16, so both directions of that premise are driven). `types` attacks the coarse -> fine `type`
upgrade, which is an EDIT rather than an addition and would otherwise happen silently inside
apply_to. `ids` attacks the convention table, the three pinned refusals and the reuse anchors.
`splits` attacks the two Prunus splits in both directions. `curculio` attacks the cross-crop ladder
shape shared with apple, including its own anti-vacuity check. `copper` attacks the hedged terminal
rung adjudication. `selfdenial` attacks the guard this batch introduces, in BOTH of its
implementations (the enumerated phrases and the structural sentence rule) plus its positive control.
`materials`, `validate`, `blast` and `mechanics` as in batches 13-16.

Every disabled branch has a driver in the suite asserting its ONE specific message, so a mutation
cannot be "caught" by an unrelated earlier check and score a false positive.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch17.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch17.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- schema ---------------------------------------------------------------------------------
    ("schema: the premise-field loop runs over nothing", "schema", PROMOTE,
     "            for f in PREMISE_FIELDS:", "            for f in ():"),
    ("schema: a note-shaped record is accepted", "schema", PROMOTE,
     '            if "note_beginner" in p or "note_seasoned" in p:', "            if False:"),
    ("schema: an already-laddered crop is accepted", "schema", PROMOTE,
     '            if p.get("control_ladder"):\n                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))',
     '            if False:\n                raise SystemExit("REFUSED: %s/%s is already laddered" % (c, p.get("name")))'),

    # ---- types ----------------------------------------------------------------------------------
    ("types: a surviving coarse type is accepted", "types", PROMOTE,
     '                if o.get("type") == coarse:', "                if False:"),
    ("types: a non-enum fine type is accepted", "types", PROMOTE,
     '                if o.get("type") not in _TYPE_TARGETS:', "                if False:"),
    ("types: the pre-state coarse premise is not asserted", "types", PROMOTE,
     '                if p.get("type") != coarse:', "                if False:"),

    # ---- ids ------------------------------------------------------------------------------------
    ("ids: the refusal table is never consulted", "ids", PROMOTE,
     "                if i in REFUSED_IDS:", "                if False:"),
    ("ids: the convention table is never enforced", "ids", PROMOTE,
     "                if i != want:", "                if False:"),
    ("ids: an unknown problem name is accepted", "ids", PROMOTE,
     "                if want is None:", "                if False:"),
    ("ids: a reused id resolving nowhere is accepted", "ids", PROMOTE,
     "        if i not in existing:", "        if False:"),
    ("ids: a reused id losing its anchor crop is accepted", "ids", PROMOTE,
     "        if anchor not in existing[i]:", "        if False:"),
    ("ids: a new id that already exists is accepted", "ids", PROMOTE,
     '            raise SystemExit("REFUSED: new id %r already exists on %s" % (i, sorted(existing[i])))',
     "            pass"),

    # ---- splits ---------------------------------------------------------------------------------
    ("splits: a required split id may vanish", "splits", PROMOTE,
     "        if required not in have[crop]:", "        if False:"),
    ("splits: the two cherry ids may merge", "splits", PROMOTE,
     "        if forbidden in have[crop]:", "        if False:"),

    # ---- curculio -------------------------------------------------------------------------------
    ("curculio: a handpick rung on a SHIPPED crop is accepted", "curculio", PROMOTE,
     '                if "handpick" in ms:\n                    raise SystemExit("REFUSED: %s/plum-curculio has a handpick rung; apple\'s "',
     '                if False:\n                    raise SystemExit("REFUSED: %s/plum-curculio has a handpick rung; apple\'s "'),
    ("curculio: a handpick rung on a STAGED crop is accepted", "curculio", PROMOTE,
     '            if "handpick" in ms:\n                raise SystemExit("REFUSED: staged %s/plum-curculio has a handpick rung" % c)',
     '            if False:\n                raise SystemExit("REFUSED: staged %s/plum-curculio has a handpick rung" % c)'),
    ("curculio: the anti-vacuity check is disabled", "curculio", PROMOTE,
     "    if seen == 0:", "    if False:"),

    # ---- copper ---------------------------------------------------------------------------------
    ("copper: the terminal rung need not be copper", "copper", PROMOTE,
     '            if not L or L[-1]["method"] != "copper_fungicide":', "            if False:"),
    ("copper: the preventive-not-curative hedge may be dropped", "copper", PROMOTE,
     '            if not re.search(r"preventive|prevention", blob):', "            if False:"),
    ("copper: the tree-injury hedge may be dropped", "copper", PROMOTE,
     '            if not re.search(r"injur|harm|damage|hurt", blob):', "            if False:"),
    ("copper: the four-ladder count is not pinned", "copper", PROMOTE,
     "    if found != 4:", "    if False:"),

    # ---- selfdenial -----------------------------------------------------------------------------
    ("selfdenial: the enumerated phrase scan runs over nothing", "selfdenial", PROMOTE,
     "                    for pat in SELF_DENIAL_PATTERNS:", "                    for pat in ():"),
    ("selfdenial: the structural sentence rule is disabled", "selfdenial", PROMOTE,
     "                        if LADDER_VOCAB.search(sent) and STRUCTURAL_CLAIM.search(sent):",
     "                        if False:"),
    ("selfdenial: the positive control no longer guards over-widening", "selfdenial", PROMOTE,
     "    for s in SELF_DENIAL_ALLOWED:", "    for s in ():"),

    # ---- materials ------------------------------------------------------------------------------
    ("materials: a material outside MATERIAL_OK is accepted", "materials", PROMOTE,
     "                    if m not in ok:", "                    if False:"),

    # ---- validate -------------------------------------------------------------------------------
    ("validate: an unknown method is accepted", "validate", PROMOTE,
     "                if m not in cm:", "                if False:"),
    ("validate: a tier decrease is accepted", "validate", PROMOTE,
     "                if t < last:", "                if False:"),
    ("validate: applies_to incoherence is accepted", "validate", PROMOTE,
     '                if "any" not in applies and not _type_ok(p["type"], applies):',
     "                if False:"),
    ("validate: identical registers are accepted", "validate", PROMOTE,
     '                if r.get("note_beginner", "").strip() == r.get("note_seasoned", "").strip():',
     "                if False:"),
    ("validate: a duplicate method is accepted", "validate", PROMOTE,
     "                if m in seen_methods:", "                if False:"),
    ("validate: an empty ladder is accepted", "validate", PROMOTE,
     "            if not L:", "            if False:"),
    ("validate: the per-crop rung count is not pinned", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[c]:", "        if False:"),
    ("validate: copy hygiene is not enforced", "validate", PROMOTE,
     "                    if bad:", "                    if False:"),
    ("validate: a forbidden method is accepted", "validate", PROMOTE,
     "                if m in FORBIDDEN_METHODS:", "                if False:"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: the problem-set equality check is disabled", "blast", PROMOTE,
     "    if set(pre) != set(post):", "    if False:"),
    ("blast: a bystander crop may change", "blast", PROMOTE,
     '        if k[0] not in CROPS:', "        if False:"),
    ("blast: the touched count is not pinned", "blast", PROMOTE,
     "    if touched != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     "    return json.dumps(data, ensure_ascii=False, indent=1).encode(\"utf-8\")"),
]

# The sentinel disables the promote's actual work. If the suite still passes with the ladders never
# attached, the harness is grading nothing and every "caught" above is meaningless.
SENTINEL = ("SENTINEL: the ladders are never attached", PROMOTE,
            '                p["control_ladder"] = copy.deepcopy(o["control_ladder"])',
            '                _skip = copy.deepcopy(o["control_ladder"])')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    """Every anchor must match EXACTLY ONCE. An anchor matching zero times (typically because it
    spans Python implicit string concatenation) silently mutates nothing and reports SURVIVED for
    the wrong reason; an anchor matching twice edits a site nobody intended. PLA-138."""
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
    wd = tempfile.mkdtemp(prefix="mutate_batch17_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch17_stone_fruit")
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
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch17_stone_fruit")',
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
    print("MUTATION HARNESS -- PLA-8 batch 17, stone fruit")
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
