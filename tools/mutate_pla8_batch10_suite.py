#!/usr/bin/env python3
"""Mutation harness for the batch 10 brassica-family promote (PLA-215).

The load-bearing families are `mint` (the pyrethrin entry: botanical vs synthetic, the strictest
bee band claim that made it worth writing, and its five rungs) and `readfix` (the root-maggot
timing drop and its scoped exception on kohlrabi's flea beetles, the copper pins in both
directions, handpick scoping, and the unminted-method note scan).

Three guards were found DEAD or WEAK while writing the suite and fixed rather than decorated:
two mint-content checks sat below the staged-spec-agreement check that shadows them (drivers now
patch both), and `ladder_signature` was POSITIONAL, so two crops with byte-identical ladders in a
different problem order would have compared as distinct -- it is now keyed by problem id, which
is what makes the identity guard able to catch a wholesale copy at all.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""

import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch10.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch10.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- mint ----------------------------------------------------------------------------------
    ("mint: the already-present refusal is disabled", "mint", PROMOTE,
     '    if MINT_KEY in cm:', '    if False:'),
    ("mint: the staged-spec agreement check is disabled", "mint", PROMOTE,
     '    if staged_mint().get("entry") != MINT:', '    if False:'),
    ("mint: the botanical-vs-synthetic tier check is disabled", "mint", PROMOTE,
     '    if MINT["tier"] != "soft_chemical":', '    if False:'),
    ("mint: the strictest-bee-band requirement is disabled", "mint", PROMOTE,
     '    if "strictest honey bee band" not in bee:', '    if False:'),
    ("mint: apply_to stops minting the method", "mint", PROMOTE,
     '    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)', '    pass'),
    ("mint: verify_post stops requiring the mint verbatim", "mint", PROMOTE,
     '    if json.loads(post["methods"].get(MINT_KEY, "null")) != json.loads(\n            json.dumps(MINT, sort_keys=True)):',
     '    if False:'),
    ("mint: the pyrethroid-present premise is disabled", "mint", PROMOTE,
     '    if "pyrethroid" not in cm:', '    if False:'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the missing-pyrethrin-rung refusal is disabled", "readfix", PROMOTE,
     '        if MINT_KEY not in ms:\n            return (f"{slug}/{HB} has no {MINT_KEY} rung',
     '        if False:\n            return (f"{slug}/{HB} has no {MINT_KEY} rung'),
    ("readfix: the pyrethroid-substitution refusal is disabled in check", "readfix", PROMOTE,
     '            if "pyrethroid" in lad:\n                return (f"{slug}/{p.get(\'id\')} carries pyrethroid',
     '            if False:\n                return (f"{slug}/{p.get(\'id\')} carries pyrethroid'),
    ("readfix: the root-maggot timing refusal is disabled", "readfix", PROMOTE,
     '        if "planting_time_avoidance" in ms:\n            return (f"{slug}/{RM} carries planting_time_avoidance',
     '        if False:\n            return (f"{slug}/{RM} carries planting_time_avoidance'),
    ("readfix: the TIMING_KEPT scope pin is disabled", "readfix", PROMOTE,
     '        if ms is None or "planting_time_avoidance" not in ms:', '        if False:'),
    ("readfix: the TIMING_KEPT table is emptied", "readfix", PROMOTE,
     'TIMING_KEPT = (("kohlrabi", FB),)', 'TIMING_KEPT = ()'),
    ("readfix: the copper-on-black-rot refusal is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" in ms:\n            return (f"{slug}/{BR} carries copper',
     '        if False:\n            return (f"{slug}/{BR} carries copper'),
    ("readfix: the copper-required pin is disabled", "readfix", PROMOTE,
     '        if ms is None or "copper_fungicide" not in ms:', '        if False:'),
    ("readfix: the COPPER_ON table is emptied", "readfix", PROMOTE,
     'COPPER_ON = (("cauliflower", "alternaria-leaf-spot"), ("kohlrabi", "alternaria-leaf-spot"),\n'
     '             ("collards", "alternaria-leaf-spot"), ("kale", "alternaria-leaf-spot"),\n'
     '             ("cabbage", "downy-mildew"), ("cauliflower", "downy-mildew"),\n'
     '             ("kohlrabi", "downy-mildew"), ("collards", "downy-mildew"),\n'
     '             ("kale", "downy-mildew"))',
     'COPPER_ON = ()'),
    ("readfix: the handpick scoping is disabled in check", "readfix", PROMOTE,
     '            if "handpick" in lad and p.get("id") not in HANDPICK_OK:\n                return (f"{slug}/{p.get(\'id\')} carries handpick',
     '            if False:\n                return (f"{slug}/{p.get(\'id\')} carries handpick'),
    ("readfix: the HANDPICK_OK table is widened to everything", "readfix", PROMOTE,
     'HANDPICK_OK = ("cabbageworms", HB)', 'HANDPICK_OK = ("cabbageworms", HB, "downy-mildew", "alternaria-leaf-spot", "aphids")'),
    ("readfix: the diatomaceous scan is disabled in check", "readfix", PROMOTE,
     '                if "diatomaceous" in blob:\n                    return f"{slug}/{p.get(\'id\')}: a note mentions diatomaceous earth"',
     '                if False:\n                    return f"{slug}/{p.get(\'id\')}: a note mentions diatomaceous earth"'),
    ("readfix: the trap-crop scan is disabled in check", "readfix", PROMOTE,
     '                if "trap crop" in blob:', '                if False:'),
    ("readfix: verify_post pyrethroid sweep is disabled", "readfix", PROMOTE,
     '            if "pyrethroid" in lad:\n                return f"post: {slug}/{p.get(\'id\')} shipped the synthetic pyrethroid"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')} shipped the synthetic pyrethroid"'),
    ("readfix: verify_post handpick sweep is disabled", "readfix", PROMOTE,
     '            if "handpick" in lad and p.get("id") not in HANDPICK_OK:\n                return f"post: {slug}/{p.get(\'id\')} shipped handpick on a leaf-removal target"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')} shipped handpick on a leaf-removal target"'),
    ("readfix: verify_post note scan is disabled", "readfix", PROMOTE,
     '                if "diatomaceous" in blob or "trap crop" in blob:', '                if False:'),
    ("readfix: verify_post pyrethrin-rung pin is disabled", "readfix", PROMOTE,
     '        if MINT_KEY not in ms:\n            return f"post: {slug}/{HB} lost its {MINT_KEY} rung"',
     '        if False:\n            return f"post: {slug}/{HB} lost its {MINT_KEY} rung"'),
    ("readfix: verify_post timing pin is disabled", "readfix", PROMOTE,
     '        if "planting_time_avoidance" in ms:\n            return f"post: {slug}/{RM} regained the unearned timing rung"',
     '        if False:\n            return f"post: {slug}/{RM} regained the unearned timing rung"'),
    ("readfix: verify_post black-rot copper pin is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" in ms:\n            return f"post: {slug}/{BR} gained a copper rung its prose does not recommend"',
     '        if False:\n            return f"post: {slug}/{BR} gained a copper rung its prose does not recommend"'),
    ("readfix: verify_post empty-ladder sweep is disabled", "readfix", PROMOTE,
     '            if not lad:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"'),

    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:', '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:', '            if False:'),
    ("convention: the two cabbageworm spellings stop converging", "convention", PROMOTE,
     '    "Cabbageworms and cabbage loopers": "cabbageworms",',
     '    "Cabbageworms and cabbage loopers": "cabbage-caterpillars",'),

    # ---- twins ---------------------------------------------------------------------------------
    ("twins: the canonical-prose twin refusal is disabled", "twins", PROMOTE,
     '            if prose_signature(by[a]) == prose_signature(by[b]):', '            if False:'),
    ("twins: the staged-digest twin refusal is disabled", "twins", PROMOTE,
     '            if dg[a] == dg[b]:', '            if False:'),
    ("twins: the post content-identity refusal is disabled", "twins", PROMOTE,
     '            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):',
     '            if False:'),
    ("twins: ladder_signature reverts to POSITIONAL, missing reordered copies", "twins", PROMOTE,
     '    return json.dumps({p["id"]: [(r["method"], r["note_beginner"], r["note_seasoned"])\n                                 for r in p["control_ladder"]]\n                       for _, p in problems(obj)}, sort_keys=True)',
     '    return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])\n                        for r in p["control_ladder"]] for _, p in problems(obj)], sort_keys=True)'),

    # ---- validate ------------------------------------------------------------------------------
    ("validate: the unknown-method refusal is disabled", "validate", PROMOTE,
     '                if m not in cm:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"',
     '                if False:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"'),
    ("validate: the tier-order refusal is disabled", "validate", PROMOTE,
     '            if tiers != sorted(tiers):', '            if False:'),
    ("validate: the applies_to refusal is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("validate: the identical-registers refusal is disabled", "validate", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', '                if False:'),
    ("validate: the empty-ladder refusal is disabled", "validate", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if False:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"'),
    ("validate: the duplicate-method refusal is disabled", "validate", PROMOTE,
     '                if m in seen:', '                if False:'),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),
    ("validate: the expected-rung table is zeroed", "validate", PROMOTE,
     'EXPECTED_RUNGS = {"cabbage": 47, "cauliflower": 52, "kohlrabi": 52, "collards": 43, "kale": 43}',
     'EXPECTED_RUNGS = {"cabbage": 0, "cauliflower": 0, "kohlrabi": 0, "collards": 0, "kale": 0}'),
    ("validate: the already-laddered refusal is disabled", "validate", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: the methods-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]) | {MINT_KEY}:', '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: bystander methods stop being compared", "blast", PROMOTE,
     '        if post["methods"][key] != before:', '        if False:'),
    ("blast: the sources comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "broccoli")["name"] = "MUTATED"\n    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)'),

    # ---- mechanics -----------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to stops writing the ladders", PROMOTE,
            '                tgt["type"] = add["type"]\n                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])',
            '                tgt["type"] = add["type"]')


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
            bad.append(f"  {n}x  {label}\n        anchor: {old[:78]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_batch10_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch10_brassicas")
    for fn in os.listdir(src_staging):
        if fn.startswith("out_") or fn == "mint_pyrethrin.json":
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch10_brassicas")',
        f'STAGING = {sandbox_staging!r}', 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- batch 10 THE BRASSICA FAMILY (5 crops, 237 rungs, 1 mint)")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails.")
        return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED.")
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
        print(f"  {k:11s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
