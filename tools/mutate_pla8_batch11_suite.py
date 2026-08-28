#!/usr/bin/env python3
"""Mutation harness for the batch 11 alliums + fall herbs promote (PLA-215).

The load-bearing families are `widen` (certified_clean_stock reaching `nematode`, which unblocks
garlic's PRIMARY control, plus the retired-practice guard that stops a note resurrecting hot-water
dips), `schema` (the first mixed-schema batch: the twins comparison must reach each crop's
advice-bearing fields in BOTH schemas), and `readfix` (copper off cilantro's bacterial leaf spot,
the batch-wide trap_cropping and planting_time_avoidance refusals, handpick scoping).

`convention` includes the allium-split mutation: garlic and spring-onion independently agreed on
all five shared ids, and since onion, leek and shallot inherit them, a split at birth is the
expensive failure this batch guards.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""


import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch11.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch11.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- widen ---------------------------------------------------------------------------------
    ("widen: the already-widened refusal is disabled", "widen", PROMOTE,
     '    if WIDEN_ADD in m["applies_to"]:', '    if False:'),
    ("widen: the staged-spec agreement check is disabled", "widen", PROMOTE,
     '    if (spec.get("applies_to_add") != WIDEN_ADD or spec.get("best_use") != WIDEN_BEST_USE',
     '    if False and (spec.get("applies_to_add") != WIDEN_ADD or spec.get("best_use") != WIDEN_BEST_USE'),
    ("widen: apply_to stops widening applies_to", "widen", PROMOTE,
     '    m = data["control_methods"][WIDEN_KEY]\n    m["applies_to"] = list(m["applies_to"]) + [WIDEN_ADD]',
     '    m = data["control_methods"][WIDEN_KEY]'),
    ("widen: apply_to stops moving the prose with the target", "widen", PROMOTE,
     '    m["best_use"] = WIDEN_BEST_USE\n    m["how_it_works_seasoned"] = m["how_it_works_seasoned"] + WIDEN_SEASONED_TAIL\n    batch = staged()',
     '    batch = staged()'),
    ("widen: the garlic clean-stock rung requirement is disabled", "widen", PROMOTE,
     '    if WIDEN_KEY not in ms:\n        return (f"garlic/{NEMATODE} has no {WIDEN_KEY} rung',
     '    if False:\n        return (f"garlic/{NEMATODE} has no {WIDEN_KEY} rung'),
    ("widen: the rung-must-lead check is disabled", "widen", PROMOTE,
     '    if ms[0] != WIDEN_KEY:', '    if False:'),
    ("widen: the hot-water retirement guard is disabled", "widen", PROMOTE,
     '        if "no longer" not in blob.lower():', '        if False:'),
    ("widen: verify_post stops checking applies_to", "widen", PROMOTE,
     '    if WIDEN_ADD not in m["applies_to"]:', '    if False:'),
    ("widen: verify_post stops checking the widened best_use", "widen", PROMOTE,
     '    if m["best_use"] != WIDEN_BEST_USE:', '    if False:'),
    ("widen: verify_post stops checking the widened seasoned prose", "widen", PROMOTE,
     '    if not m["how_it_works_seasoned"].endswith(WIDEN_SEASONED_TAIL):', '    if False:'),
    ("widen: verify_post stops requiring the leading rung", "widen", PROMOTE,
     '    if not ms or ms[0] != WIDEN_KEY:', '    if False:'),

    # ---- schema --------------------------------------------------------------------------------
    ("schema: the advice-coverage check is disabled", "schema", PROMOTE,
     '        if not (own_advice & set(PROSE_FIELDS)):', '        if False:'),
    ("schema: the no-advice-field check is disabled", "schema", PROMOTE,
     '        if not own_advice:', '        if False:'),
    ("schema: PROSE_FIELDS drops the management_ pair", "schema", PROMOTE,
     '                "identification_beginner", "identification_seasoned",\n                "management_beginner", "management_seasoned")',
     '                "identification_beginner", "identification_seasoned")'),
    ("schema: ADVICE_FIELDS is emptied", "schema", PROMOTE,
     'ADVICE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",\n'
     '                 "prevention_beginner", "prevention_seasoned",\n'
     '                 "management_beginner", "management_seasoned")',
     'ADVICE_FIELDS = ()'),
    ("schema: the new-schema expectation is disabled", "schema", PROMOTE,
     '        if slug in NEW_SCHEMA_CROPS and "management_seasoned" not in seen:', '        if False:'),
    ("schema: check_schema_coverage is not called by the twins check", "schema", PROMOTE,
     '    problem = check_schema_coverage(by)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the cilantro copper refusal is disabled", "readfix", PROMOTE,
     '    if "copper_fungicide" in ms:\n        return ("cilantro-coriander/bacterial-leaf-spot carries copper',
     '    if False:\n        return ("cilantro-coriander/bacterial-leaf-spot carries copper'),
    ("readfix: the trap_cropping refusal is disabled", "readfix", PROMOTE,
     '            if "trap_cropping" in lad:', '            if False:'),
    ("readfix: the planting_time_avoidance refusal is disabled", "readfix", PROMOTE,
     '            if "planting_time_avoidance" in lad:\n                return (f"{slug}/{p.get(\'id\')} carries planting_time_avoidance',
     '            if False:\n                return (f"{slug}/{p.get(\'id\')} carries planting_time_avoidance'),
    ("readfix: the handpick scoping is disabled in check", "readfix", PROMOTE,
     '            if "handpick" in lad and p.get("id") not in HANDPICK_OK:\n                return (f"{slug}/{p.get(\'id\')} carries handpick',
     '            if False:\n                return (f"{slug}/{p.get(\'id\')} carries handpick'),
    ("readfix: HANDPICK_OK widens to everything", "readfix", PROMOTE,
     'HANDPICK_OK = ("parsleyworm",)', 'HANDPICK_OK = ("parsleyworm", "garlic-rust", "powdery-mildew", "aphids")'),
    ("readfix: the pyrethroid refusal is disabled", "readfix", PROMOTE,
     '            if "pyrethroid" in lad:', '            if False:'),
    ("readfix: the note scan is disabled in check", "readfix", PROMOTE,
     '                for word in ("diatomaceous", "trap crop"):', '                for word in ():'),
    ("readfix: verify_post copper pin is disabled", "readfix", PROMOTE,
     '    if "copper_fungicide" in ms:\n        return "post: cilantro\'s bacterial leaf spot gained the copper rung the read ruled out"',
     '    if False:\n        return "post: cilantro\'s bacterial leaf spot gained the copper rung the read ruled out"'),
    ("readfix: verify_post timing pin is disabled", "readfix", PROMOTE,
     '            if "planting_time_avoidance" in lad:\n                return f"post: {slug}/{p.get(\'id\')} shipped an unearned timing rung"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')} shipped an unearned timing rung"'),
    ("readfix: verify_post handpick pin is disabled", "readfix", PROMOTE,
     '            if "handpick" in lad and p.get("id") not in HANDPICK_OK:\n                return f"post: {slug}/{p.get(\'id\')} shipped handpick on a leaf-removal target"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')} shipped handpick on a leaf-removal target"'),
    ("readfix: verify_post note scan is disabled", "readfix", PROMOTE,
     '                if "diatomaceous" in blob or "trap crop" in blob:', '                if False:'),
    ("readfix: verify_post empty-ladder sweep is disabled", "readfix", PROMOTE,
     '            if not lad:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"'),

    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:', '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:', '            if False:'),
    ("convention: SHARED_ALLIUM_IDS is emptied", "convention", PROMOTE,
     'SHARED_ALLIUM_IDS = ("onion-thrips", "onion-maggot", "white-rot", "fusarium-basal-rot",\n                     "botrytis-neck-rot")',
     'SHARED_ALLIUM_IDS = ()'),
    ("convention: verify_post allium-split pin is disabled", "convention", PROMOTE,
     '        if pid not in g_ids or pid not in s_ids:\n            return f"post: the alliums shipped a split id on {pid!r}"',
     '        if False:\n            return f"post: the alliums shipped a split id on {pid!r}"'),

    # ---- twins ---------------------------------------------------------------------------------
    ("twins: the canonical-prose twin refusal is disabled", "twins", PROMOTE,
     '            if prose_signature(by[a]) == prose_signature(by[b]):', '            if False:'),
    ("twins: the staged-digest twin refusal is disabled", "twins", PROMOTE,
     '            if dg[a] == dg[b]:', '            if False:'),

    # ---- validate ------------------------------------------------------------------------------
    ("validate: the unknown-method refusal is disabled", "validate", PROMOTE,
     '                if m not in cm:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"',
     '                if False:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"'),
    ("validate: the tier-order refusal is disabled", "validate", PROMOTE,
     '            if tiers != sorted(tiers):', '            if False:'),
    ("validate: the applies_to refusal is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("validate: validate_batch runs against the UNWIDENED catalog", "validate", PROMOTE,
     '    problem = validate_batch(batch, widened(cm))', '    problem = validate_batch(batch, cm)'),
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
     'EXPECTED_RUNGS = {"garlic": 21, "spring-onion": 16, "dill": 19, "cilantro-coriander": 25}',
     'EXPECTED_RUNGS = {"garlic": 0, "spring-onion": 0, "dill": 0, "cilantro-coriander": 0}'),
    ("validate: the already-laddered refusal is disabled", "validate", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: the methods-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: bystander methods stop being compared", "blast", PROMOTE,
     '        if post["methods"][key] != before:', '        if False:'),
    ("blast: the sources comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    m = data["control_methods"][WIDEN_KEY]',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "cabbage")["name"] = "MUTATED"\n    m = data["control_methods"][WIDEN_KEY]'),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch11_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch11_alliums_herbs")
    for fn in os.listdir(src_staging):
        if fn.startswith("out_") or fn == "widen_certified_clean_stock.json":
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch11_alliums_herbs")',
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
    print("MUTATION HARNESS -- batch 11 ALLIUMS + FALL HERBS (4 crops, 81 rungs, 1 widening)")
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
