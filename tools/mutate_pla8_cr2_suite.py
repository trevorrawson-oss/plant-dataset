#!/usr/bin/env python3
"""Mutation harness for PLA-8 catalog r2 (PLA-215).

THE `shipped` FAMILY IS THE ONE THAT MATTERS MOST HERE, and it is unusual: its mutations perform
THE FIX THIS PROMOTE DELIBERATELY DID NOT MAKE. Narrowing `garden_sanitation` away from in-season
removal is the obvious reading of the batch-1 defect, and it would have broken ~14 of its rungs on
seven already-certified crops. The guards that assert garden_sanitation is byte-identical are only
worth having if a mutation proves they would notice someone doing it. Two do.

`semantic` guards the disambiguation itself: if prune_out_infection stops naming its defining action
or stops pointing at garden_sanitation, the narrowing is decorative and the next batch reaches for
it again.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r2.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r2.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r2_content.py")
MARKER = "# MUTATION-APPLIED"

APPLY_HEAD = ('    cm = data["control_methods"]\n'
              '    cm.update(json.loads(json.dumps(B.NEW_METHODS)))')

MUTATIONS = [
    # ---- semantic: the disambiguation is hollowed out -------------------------------------
    ("semantic: prune stops naming its defining action (clean tissue)", "semantic", CONTENT,
     '        "new": ("Cutting an infection out of a stem or branch by taking the cut well beyond the "',
     '        "new": ("Removing infection from a stem or branch by taking the cut somewhere below the "'),
    ("semantic: prune stops pointing at garden_sanitation", "semantic", CONTENT,
     '                "which is where simply picking off a spotted leaf or a rotted fruit, or pulling a "',
     '                "which is a different sort of thing entirely, along with picking a leaf or pulling a "'),
    ("semantic: off_season_tillage stops distinguishing itself from sanitation", "semantic", CONTENT,
     '            "hornworm, worked once after harvest. Distinct from garden sanitation, which clears "',
     '            "hornworm, worked once after harvest. A tidy-up step much like clearing "'),
    ("semantic: clean_stock drops the basil hot-water caveat", "semantic", CONTENT,
     '            "treated for it, though basil seed is not amenable to hot-water treatment because it "',
     '            "treated for it, and hot-water treatment is the other option because it "'),
    ("semantic: prune beginner no longer leads with WHERE you cut", "semantic", CONTENT,
     '        "new": ("What matters here is where you cut, not that you cut. You take the blade well "',
     '        "new": ("Cut the infected branches off and destroy them. You take the blade well "'),
    # ---- shipped: the fix this promote deliberately did NOT make ----------------------------
    ("shipped: garden_sanitation is narrowed away from in-season leaf removal", "shipped", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    cm["garden_sanitation"]["best_use"] = (\n'
                  '        "End-of-season cleanup and removal of crop debris between crops.")'),
    ("shipped: a certified crop's sanitation rung is repointed", "shipped", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    _p = _problem(data, "broccoli", "downy-mildew")\n'
                  '    _p["control_ladder"][0]["method"] = "prune_out_infection"'),
    # ---- artichoke -------------------------------------------------------------------------
    ("artichoke: the curly-dwarf repoint also rewrites the prose", "artichoke", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    _p = _problem(data, "artichoke", "artichoke-curly-dwarf")\n'
                  '    _p["control_ladder"][1]["note_beginner"] = "Use clean stock."'),
    ("artichoke: the self-refuting crown-rot rung is kept instead of dropped", "artichoke", CONTENT,
     '        "to": None,          # DROP; its roguing content merges into rung 0',
     '        "to": "certified_clean_stock",  # kept'),
    ("artichoke: the dropped rung's content is not merged upward", "artichoke", CONTENT,
     '            "rather than leaving it in the bed. Once a plant is affected, lift it out with its "',
     '            "rather than leaving it in the bed. "'),
    # ---- survivors --------------------------------------------------------------------------
    ("survivors: prune is left reachable from a third site", "survivors", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    _p = _problem(data, "celery", "pink-rot")\n'
                  '    _p["control_ladder"][0]["method"] = "prune_out_infection"'),
    # ---- sourcing ---------------------------------------------------------------------------
    ("sourcing: a mint's anchoring_urls no longer match its sources", "sourcing", CONTENT,
     '        "sources": ["cornell_ext", "ucanr_ext"],',
     '        "sources": ["cornell_ext", "ucanr_ext", "umn_ext"],'),
    ("sourcing: the not-minted record is emptied so the close looks complete", "sourcing", CONTENT,
     'NOT_MINTED = {\n    "pheromone_trap":',
     'NOT_MINTED = {\n    "_disabled_pheromone_trap":'),
    # ---- blast radius ------------------------------------------------------------------------
    ("blast: an unrelated crop is touched", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["crops"][0]["name"] = "MUTATED"'),
    ("blast: the source_catalog is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["source_catalog"]["umn_ext"]["tier"] = "T2"'),
    ("blast: a third control_method is quietly edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    cm["handpick"]["applies_to"].append("viral")'),
    # ---- mechanics ---------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '            "the plant and spend the winter underground as pupae, the resting stage between "',
     '            "the plant and spend the winter underground as pupae — the resting stage between "'),
    ("mechanics: a British spelling enters consumer copy", "mechanics", CONTENT,
     '            "predation and desiccation. It acts on next season\'s emerging adults rather than on "',
     '            "predation and desiccation. Its behaviour acts on next season\'s adults rather than on "'),
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
    wd = tempfile.mkdtemp(prefix="mutate_cr2_")
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
    print("MUTATION HARNESS -- PLA-8 catalog r2 (mints, narrowing, artichoke repoint)")
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
