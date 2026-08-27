#!/usr/bin/env python3
"""Mutation harness for the batch 8 leafy-greens promote (PLA-215).

The load-bearing family is `readfix`: the copper split on downy mildew (both directions), the
lettuce no-rotation pin, the DE exclusion, the neem-on-flea-beetles refusal-spec, the two order
normalizations, and the bok-choy horticultural_oil divergence. `convention` attacks the id join
keys (this batch carries two deliberate REUSES and one convergence); `twins`, `premise`,
`validate`, `blast` and `mechanics` cover the rest.

Staging is sandboxed per run (only the out_*.json files the promote reads), with STAGING
rewritten in the staged promote -- the fix batch 7's first harness run taught.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch8.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch8.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:',
     '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:',
     '            if False:'),
    ("convention: the leafminer reuse is rewired to a fresh mint", "convention", PROMOTE,
     '    "Spinach leafminer": "beet-spinach-leafminer",',
     '    "Spinach leafminer": "spinach-leafminer",'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the copper-required check is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" not in ms:\n            return (f"{slug}/{DM} lost its copper rung',
     '        if False:\n            return (f"{slug}/{DM} lost its copper rung'),
    ("readfix: the copper-forbidden check is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" in ms:\n            return (f"{slug}/{DM} carries a copper rung',
     '        if False:\n            return (f"{slug}/{DM} carries a copper rung'),
    ("readfix: the copper split tables are emptied", "readfix", PROMOTE,
     'COPPER_ON_DM = ("lettuce-leaf", "bok-choy")\nNO_COPPER_ON_DM = ("spinach", "arugula")',
     'COPPER_ON_DM = ()\nNO_COPPER_ON_DM = ()'),
    ("readfix: the lettuce no-rotation pin is disabled", "readfix", PROMOTE,
     '    if "crop_rotation" in ms:\n        return ("lettuce-leaf/downy-mildew carries crop_rotation',
     '    if False:\n        return ("lettuce-leaf/downy-mildew carries crop_rotation'),
    ("readfix: the spinach/arugula rotation-present pin is disabled", "readfix", PROMOTE,
     '        if "crop_rotation" not in ms:\n            return (f"{slug}/{DM} lost crop_rotation',
     '        if False:\n            return (f"{slug}/{DM} lost crop_rotation'),
    ("readfix: the DE exclusion is disabled in check", "readfix", PROMOTE,
     '                if "diatomaceous" in blob:',
     '                if False:'),
    ("readfix: the neem refusal-spec is disabled", "readfix", PROMOTE,
     '        if "neem_oil" in ms or "insecticidal_soap" in ms:',
     '        if False:'),
    ("readfix: the row-cover floor is disabled", "readfix", PROMOTE,
     '        if "floating_row_cover" not in ms:\n            return f"{slug}/{FB} lost floating_row_cover',
     '        if False:\n            return f"{slug}/{FB} lost floating_row_cover'),
    ("readfix: the white-rust normalization is disabled", "readfix", PROMOTE,
     '        if tuple(ms) != WHITE_RUST_ORDER:\n            return (f"{slug}/white-rust is {ms}',
     '        if False:\n            return (f"{slug}/white-rust is {ms}'),
    ("readfix: the damping-off normalization is disabled", "readfix", PROMOTE,
     '        if tuple(ms) != DAMPING_OFF_ORDER:',
     '        if False:'),
    ("readfix: the hort-oil divergence pin is disabled", "readfix", PROMOTE,
     '    if ms is None or "horticultural_oil" not in ms:',
     '    if False:'),
    ("readfix: verify_post copper-required is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" not in ms:\n            return f"post: {slug}/{DM} lost its copper rung"',
     '        if False:\n            return f"post: {slug}/{DM} lost its copper rung"'),
    ("readfix: verify_post copper-forbidden is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" in ms:\n            return f"post: {slug}/{DM} gained a copper rung the read ruled out"',
     '        if False:\n            return f"post: {slug}/{DM} gained a copper rung the read ruled out"'),
    ("readfix: verify_post lettuce-rotation is disabled", "readfix", PROMOTE,
     '    if "crop_rotation" in ms:\n        return "post: lettuce-leaf/downy-mildew gained the rotation rung its prose contradicts"',
     '    if False:\n        return "post: lettuce-leaf/downy-mildew gained the rotation rung its prose contradicts"'),
    ("readfix: verify_post neem check is disabled", "readfix", PROMOTE,
     '        if ms is not None and "neem_oil" in ms:',
     '        if False:'),
    ("readfix: verify_post DE check is disabled", "readfix", PROMOTE,
     '                if "diatomaceous" in (r["note_beginner"] + " " + r["note_seasoned"]).lower():',
     '                if False:'),
    ("readfix: verify_post empty-ladder check is disabled", "readfix", PROMOTE,
     '            if not p.get("control_ladder"):\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"'),
    ("readfix: verify_post white-rust order check is disabled", "readfix", PROMOTE,
     '        if tuple(ms) != WHITE_RUST_ORDER:\n            return f"post: {slug}/white-rust drifted from the normalized order"',
     '        if False:\n            return f"post: {slug}/white-rust drifted from the normalized order"'),

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

    # ---- premise -------------------------------------------------------------------------------
    ("premise: the spinosad dusk premise is disabled", "premise", PROMOTE,
     '    if "dusk" not in spin:',
     '    if False:'),
    ("premise: the neem band premise is disabled", "premise", PROMOTE,
     '    if "sunset" not in neem or "midnight" not in neem:',
     '    if False:'),
    ("premise: the already-laddered refusal is disabled", "premise", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

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
     'EXPECTED_RUNGS = {"spinach": 36, "arugula": 40, "lettuce-leaf": 20, "bok-choy": 57}',
     'EXPECTED_RUNGS = {"spinach": 0, "arugula": 0, "lettuce-leaf": 0, "bok-choy": 0}'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):',
     '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:\n            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"',
     '        if False:\n            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"'),
    ("blast: the methods comparison is disabled", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:',
     '    if False:'),
    ("blast: the sources comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:',
     '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "strawberry")["name"] = "MUTATED"\n    batch = staged()'),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch8_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch8_leafy_greens")
    for fn in os.listdir(src_staging):
        if fn.startswith("out_"):
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch8_leafy_greens")',
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
    print("MUTATION HARNESS -- batch 8 THE LEAFY GREENS (4 crops, 153 rungs, 0 mints)")
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
