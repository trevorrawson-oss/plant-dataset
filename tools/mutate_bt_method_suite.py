#!/usr/bin/env python3
"""Mutation harness for the Bt CATALOG-method fix (PLA-215).

THE `safety` FAMILY ATTACKS A SIX-PART SPECIFICATION. The old field was wrong twice AND
self-contradictory: "It ONLY AFFECTS CATERPILLARS" in sentence three against "it does not tell good
caterpillars from bad" in sentence six. A promote that fixed only one half, or that deleted the
sentence rather than correcting it, would pass a naive absence check while leaving the reader with
less than they started with. So there is a separate mutation for reverting each construction, for
dropping each required element, and for deleting the claim outright.

THE `leftalone` FAMILY guards the opposite failure and matters just as much here. Thirteen of the
fifteen roster-wide safety-construction hits are CORRECT AS WRITTEN -- "non-toxic" on a cardboard
collar, a glue card and a pheromone lure is literally accurate, and "practically nontoxic" in bt's
own seasoned register is NPIC's term of art. A sweep that flattened those would make the record less
faithful to its sources. Three mutations do exactly that.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_bt_method.py")
PROMOTE = os.path.join(HERE, "promote_bt_method.py")
CONTENT = os.path.join(HERE, "build_bt_method_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- safety: a banned construction comes back -------------------------------------------
    ("safety: 'only affects caterpillars' is restored", "safety", CONTENT,
     '    "proteins wreck its gut, and it stops feeding and dies. It acts on caterpillars rather than on "\n'
     '    "insects in general, so the risk to bees is low, and it is low in toxicity to people and pets, "',
     '    "proteins wreck its gut, and it stops feeding and dies. It only affects caterpillars, "\n'
     '    "so the risk to bees is low, and it is low in toxicity to people and pets, "'),
    ("safety: 'is safe to eat' is restored", "safety", CONTENT,
     '    "who cannot activate the proteins the way a caterpillar\'s gut does. Two things to watch. The "',
     '    "who cannot activate the proteins at all, which is why a treated vegetable is safe to eat. The "'),
    # ---- safety: a required element is dropped -------------------------------------------------
    ("safety: the non-target caveat is dropped", "safety", CONTENT,
     '    "it cannot tell a pest caterpillar from a butterfly one, so spray only the plants that have a "\n'
     '    "pest problem, never a plant you are growing for butterflies."',
     '    "it works best on young caterpillars, so spray only the plants that have a "\n'
     '    "pest problem."'),
    ("safety: the actionable consequence is dropped, the fact kept", "safety", CONTENT,
     '    "pest problem, never a plant you are growing for butterflies."',
     '    "pest problem."'),
    ("safety: the low-toxicity claim loses its mechanism", "safety", CONTENT,
     '    "who cannot activate the proteins the way a caterpillar\'s gut does. Two things to watch. The "',
     '    "and that is all there is to it. Two things to watch. The "'),
    ("safety: the eye/skin irritation warning is lost in the rewrite", "safety", CONTENT,
     '    "spray itself can irritate eyes and skin, so wear gloves and keep it away from your face. And "',
     '    "spray is easy to apply with a hand sprayer. And "'),
    ("safety: the claim is DELETED rather than corrected", "safety", CONTENT,
     '    "proteins wreck its gut, and it stops feeding and dies. It acts on caterpillars rather than on "\n'
     '    "insects in general, so the risk to bees is low, and it is low in toxicity to people and pets, "\n'
     '    "who cannot activate the proteins the way a caterpillar\'s gut does. Two things to watch. The "',
     '    "proteins wreck its gut, and it stops feeding and dies. Two things to watch. The "'),
    ("safety: a REQUIRED pattern is weakened to match anything", "safety", CONTENT,
     '    "qualified toxicity": r"low in toxicity",',
     '    "qualified toxicity": r"",'),
    # ---- leftalone: accurate language gets flattened ---------------------------------------------
    ("leftalone: NPIC's 'practically nontoxic' is scrubbed from the seasoned register", "leftalone", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    _m = data["control_methods"][B.METHOD]\n'
     '    _m["how_it_works_seasoned"] = _m["how_it_works_seasoned"].replace(\n'
     '        "practically nontoxic", "low risk")\n'
     '    return 1'),
    ("leftalone: 'non-toxic' is scrubbed from the cardboard-collar method", "leftalone", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    _s = data["control_methods"]["stem_collars"]\n'
     '    _s["pros"] = [p.replace("non-toxic", "lower risk") for p in _s["pros"]]\n'
     '    return 1'),
    ("leftalone: the cautions entry loses swallowtails and monarchs", "leftalone", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    _m = data["control_methods"][B.METHOD]\n'
     '    _m["cautions"] = ["Spray only plants with a pest problem"]\n'
     '    return 1'),
    ("leftalone: the correct-as-written record is renamed so nothing is compared", "leftalone", CONTENT,
     'CORRECT_AS_WRITTEN = {\n    "stem_collars":',
     'CORRECT_AS_WRITTEN = {\n    "_retired_stem_collars":'),
    # ---- blast -------------------------------------------------------------------------------------
    ("blast: a crop is touched", "blast", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    data["crops"][0]["name"] = "MUTATED"\n    return 1'),
    ("blast: another control_method is edited", "blast", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    data["control_methods"]["handpick"]["applies_to"].append("viral")\n    return 1'),
    ("blast: another bt field is edited", "blast", PROMOTE,
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n    return 1',
     '    data["control_methods"][B.METHOD][B.FIELD] = B.NEW\n'
     '    data["control_methods"][B.METHOD]["best_use"] += " Also good on beetles."\n    return 1'),
    # ---- mechanics -----------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '    "Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, the Bt "\n'
     '    "proteins wreck its gut, and it stops feeding and dies. It acts on caterpillars rather than on "',
     '    "Bt is a natural soil bacterium — when a caterpillar eats leaves sprayed with it, the Bt "\n'
     '    "proteins wreck its gut and it dies. It acts on caterpillars rather than on "'),
    ("mechanics: the beginner register falls back on jargon", "mechanics", CONTENT,
     '    "insects in general, so the risk to bees is low, and it is low in toxicity to people and pets, "',
     '    "Lepidoptera in general, so the risk to bees is low, and kurstaki is low in toxicity to people and pets, "'),
    # ---- record ----------------------------------------------------------------------------------------
    ("record: the source read is rewritten to support the absolute", "record", CONTENT,
     '        "Bt is low in toxicity to people and other mammals when eaten",',
     '        "Bt is safe for people and other mammals when eaten",'),
    ("record: the non-target moth finding is dropped from the record", "record", CONTENT,
     '        "a few studies also found that non-target moths were harmed",',
     '        "no harm to non-target insects was reported",'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            "def apply_to(data):", "def apply_to(data):\n    return 0")


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS]
    rows.append((SENTINEL[0], SENTINEL[1], SENTINEL[2]))
    for label, f, old in rows:
        n = open(f).read().count(old)
        if n != 1:
            bad.append(f"  {n}x  [{os.path.basename(f)}] {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_btm_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- the Bt safety absolute, CATALOG method")
    print("=" * 78)
    if not preflight():
        return 1

    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails -- the clean suite is not green.")
        return 1
    print("positive control : GREEN")

    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED -- the harness is not running the mutated code.")
        return 1
    print("sentinel         : RED as required\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print(f"  {k:10s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
