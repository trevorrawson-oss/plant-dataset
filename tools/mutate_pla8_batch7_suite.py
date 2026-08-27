#!/usr/bin/env python3
"""Mutation harness for the batch 7 tomatoes promote (PLA-215).

The load-bearing families are `readfix` (the two adjudications and the splash rungs: the
neem-off-flea-beetles drop and its scoped-not-blanket counterweight, the blossom-end-rot culling
rung, the splash rung and its position, the whitefly divergence in both directions) and `mint`
(the splash_barrier_mulch literal, its staged-spec agreement, and the chemical-cohort premises
these rungs restate). `convention` attacks the id join keys; `twins` the four-independent-passes
premise; `validate`, `blast` and `mechanics` the usual structure.

Note on shadowing, learned while writing the suite: three first-draft guards sat below stronger
neighbours (the small-tomato shape check under the id-convention loop; a roma-neem check under
NEEM_KEPT; an EMPTY driver on a pinned ladder). The first was made reachable by ORDER, the second
deleted as dead code, the third re-aimed -- the mutations below verify the survivors actually
fire.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch7.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch7.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:',
     '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:',
     '            if False:'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the small-tomato shape check is disabled", "readfix", PROMOTE,
     '    for slug in ("beefsteak-tomato", "cherry-tomato"):\n        if ladder_of(batch[slug], "whiteflies")[0] is not None:',
     '    for slug in ():\n        if ladder_of(batch[slug], "whiteflies")[0] is not None:'),
    ("readfix: the neem-on-flea-beetles refusal is disabled", "readfix", PROMOTE,
     '        if "neem_oil" in mfb:\n            return (f"{slug}/{FB} carries neem_oil',
     '        if False:\n            return (f"{slug}/{FB} carries neem_oil'),
    ("readfix: the NEEM_KEPT table is emptied", "readfix", PROMOTE,
     'NEEM_KEPT = {\n    "beefsteak-tomato": ("aphids", "spider-mites"),',
     'NEEM_KEPT = {k: () for k in CROPS} or {\n    "_beefsteak-tomato": ("aphids", "spider-mites"),'),
    ("readfix: the row-cover floor on flea-beetles is disabled", "readfix", PROMOTE,
     '        if "floating_row_cover" not in mfb:',
     '        if False:'),
    ("readfix: the blossom-end-rot culling refusal is disabled", "readfix", PROMOTE,
     '        if "garden_sanitation" not in mber:\n            return (f"{slug}/{BER} has no garden_sanitation rung',
     '        if False:\n            return (f"{slug}/{BER} has no garden_sanitation rung'),
    ("readfix: the missing-splash-rung refusal is disabled in check", "readfix", PROMOTE,
     '            if MINT_KEY not in ms:\n                return (f"{slug}/{pid} has no {MINT_KEY} rung; the crop\'s own prose commands "',
     '            if False:\n                return (f"{slug}/{pid} has no {MINT_KEY} rung; the crop\'s own prose commands "'),
    ("readfix: the splash-position refusal is disabled", "readfix", PROMOTE,
     '            if ms.index(MINT_KEY) != ms.index("water_at_the_base") + 1:',
     '            if False:'),
    ("readfix: the GRAPE_ONLY_WF table is emptied", "readfix", PROMOTE,
     'GRAPE_ONLY_WF = ("horticultural_oil", "weed_host_control")',
     'GRAPE_ONLY_WF = ()'),
    ("readfix: the divergence pin stops checking the grape side", "readfix", PROMOTE,
     '        if m not in gwf:\n            return (f"grape-tomato/whiteflies lost {m}',
     '        if False:\n            return (f"grape-tomato/whiteflies lost {m}'),
    ("readfix: the divergence pin stops checking the roma side", "readfix", PROMOTE,
     '        if m in rwf:\n            return (f"roma-tomato/whiteflies gained {m}',
     '        if False:\n            return (f"roma-tomato/whiteflies gained {m}'),
    ("readfix: verify_post stops checking neem regained", "readfix", PROMOTE,
     '        if "neem_oil" in mfb:\n            return f"post: {slug}/{FB} regained neem_oil"',
     '        if False:\n            return f"post: {slug}/{FB} regained neem_oil"'),
    ("readfix: verify_post stops checking neem kept", "readfix", PROMOTE,
     '            if "neem_oil" not in ms:\n                return f"post: {slug}/{pid} lost neem_oil; the drop was scoped to flea-beetles"',
     '            if False:\n                return f"post: {slug}/{pid} lost neem_oil; the drop was scoped to flea-beetles"'),
    ("readfix: verify_post stops checking the culling rung", "readfix", PROMOTE,
     '        if "garden_sanitation" not in mber:\n            return f"post: {slug}/{BER} lost its culling rung"',
     '        if False:\n            return f"post: {slug}/{BER} lost its culling rung"'),
    ("readfix: verify_post stops checking the splash rungs", "readfix", PROMOTE,
     '            if MINT_KEY not in ms:\n                return f"post: {slug}/{pid} lost its {MINT_KEY} rung"',
     '            if False:\n                return f"post: {slug}/{pid} lost its {MINT_KEY} rung"'),
    ("readfix: verify_post stops checking the whitefly divergence", "readfix", PROMOTE,
     '        if m not in gwf or m in rwf:',
     '        if False:'),
    ("readfix: verify_post stops checking for empty post ladders", "readfix", PROMOTE,
     '            if not p.get("control_ladder"):\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"'),

    # ---- twins ---------------------------------------------------------------------------------
    ("twins: the canonical-prose twin refusal is disabled", "twins", PROMOTE,
     '            if prose_signature(by[a]) == prose_signature(by[b]):',
     '            if False:'),
    ("twins: the staged-digest twin refusal is disabled", "twins", PROMOTE,
     '            if dg[a] == dg[b]:',
     '            if False:'),
    ("twins: the post content-identity refusal is disabled", "twins", PROMOTE,
     '            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):',
     '            if False:'),
    ("twins: the prose-signature field list is emptied", "twins", PROMOTE,
     'PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",\n'
     '                "organic_treatment_beginner", "organic_treatment_seasoned", "prevention_beginner",\n'
     '                "prevention_seasoned", "severity", "sources")',
     'PROSE_FIELDS = ()'),

    # ---- mint ----------------------------------------------------------------------------------
    ("mint: the already-present refusal is disabled", "mint", PROMOTE,
     '    if MINT_KEY in cm:\n        return f"{MINT_KEY} is already in the catalog; this promote has already run"',
     '    if False:\n        return f"{MINT_KEY} is already in the catalog; this promote has already run"'),
    ("mint: the staged-spec agreement check is disabled", "mint", PROMOTE,
     '    if staged_mint().get("entry") != MINT:',
     '    if False:'),
    ("mint: apply_to stops minting the method", "mint", PROMOTE,
     '    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)',
     '    pass'),
    ("mint: verify_post stops requiring the mint verbatim", "mint", PROMOTE,
     '    if json.loads(post["methods"].get(MINT_KEY, "null")) != json.loads(\n            json.dumps(MINT, sort_keys=True)):',
     '    if False:'),
    ("mint: the copper-split premise is disabled", "mint", PROMOTE,
     '    if "copper hydroxide" not in copper:',
     '    if False:'),
    ("mint: the neem-band premise is disabled", "mint", PROMOTE,
     '    if "sunset" not in neem or "midnight" not in neem:',
     '    if False:'),

    # ---- validate ------------------------------------------------------------------------------
    ("validate: the unknown-method refusal is disabled", "validate", PROMOTE,
     '                if m not in cm:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"',
     '                if False:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"'),
    ("validate: the tier-order refusal is disabled", "validate", PROMOTE,
     '            if tiers != sorted(tiers):',
     '            if False:'),
    ("validate: the applies_to refusal is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("validate: the identical-registers refusal is disabled", "validate", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:',
     '                if False:'),
    ("validate: the empty-ladder refusal is disabled", "validate", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if False:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"'),
    ("validate: the duplicate-method refusal is disabled", "validate", PROMOTE,
     '                if m in seen:',
     '                if False:'),
    ("validate: the missing-register refusal is disabled", "validate", PROMOTE,
     '                    if not str(r.get(k) or "").strip():',
     '                    if False:'),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:',
     '        if False:'),
    ("validate: the expected-rung table is zeroed", "validate", PROMOTE,
     'EXPECTED_RUNGS = {"beefsteak-tomato": 35, "cherry-tomato": 35, "grape-tomato": 42, "roma-tomato": 42}',
     'EXPECTED_RUNGS = {"beefsteak-tomato": 0, "cherry-tomato": 0, "grape-tomato": 0, "roma-tomato": 0}'),
    ("validate: the already-laddered refusal is disabled", "validate", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):',
     '    if False:'),
    ("blast: the methods-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]) | {MINT_KEY}:',
     '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:\n            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"',
     '        if False:\n            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"'),
    ("blast: bystander methods stop being compared", "blast", PROMOTE,
     '        if post["methods"][key] != before:',
     '        if False:'),
    ("blast: the source-catalog comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:',
     '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "strawberry")["name"] = "MUTATED"\n    data["control_methods"][MINT_KEY] = copy.deepcopy(MINT)'),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch7_")
    # Sandbox ONLY the staged files the promote reads (the scratch canonicals are ~26MB each and
    # are staging artifacts, not promote inputs), and rewrite STAGING so the staged promote reads
    # the sandbox rather than resolving a path relative to /tmp.
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch7_tomatoes")
    for fn in os.listdir(src_staging):
        if fn.startswith("out_") or fn == "mint_splash_barrier_mulch.json":
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch7_tomatoes")',
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
    print("MUTATION HARNESS -- batch 7 THE TOMATOES (4 crops, 154 rungs, 1 mint)")
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
