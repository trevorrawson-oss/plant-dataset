#!/usr/bin/env python3
"""Mutation harness for the batch 9 roots promote (PLA-215).

The load-bearing family is `readfix`: the handpick adjudication (off the leafminer, KEPT on the
harlequin bug), the five prose-driven divergences in both directions, the three prompt_harvest
uses, the damping-off rung counts, and the standing batch-wide refusals (no DE, no neem/soap on
flea beetles). `convention` attacks the id join keys including beet's singular-to-plural
convergence.

Two guards were found DEAD during suite-writing and fixed rather than decorated: a singular-id
check in check() sat below the ID_CONVENTION loop that already refuses it (deleted), and the
post-side sweep sat below ladder_of pins that crash on a renamed id (hoisted). The mutations
below verify what remains actually fires.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch9.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch9.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:', '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:', '            if False:'),
    ("convention: beet's singular name is rewired back to the singular id", "convention", PROMOTE,
     '    "Flea beetle": "flea-beetles",          # beet\'s singular NAME takes the plural roster id',
     '    "Flea beetle": "flea-beetle",'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the handpick-on-leafminer refusal is disabled", "readfix", PROMOTE,
     '    if "handpick" in ms:\n        return ("beet/beet-spinach-leafminer carries handpick',
     '    if False:\n        return ("beet/beet-spinach-leafminer carries handpick'),
    ("readfix: the leafminer sanitation floor is disabled", "readfix", PROMOTE,
     '    if "garden_sanitation" not in ms:\n        return ("beet/beet-spinach-leafminer lost garden_sanitation',
     '    if False:\n        return ("beet/beet-spinach-leafminer lost garden_sanitation'),
    ("readfix: the harlequin-bug handpick pin is disabled", "readfix", PROMOTE,
     '    if ms is None or "handpick" not in ms:', '    if False:'),
    ("readfix: the copper-alternaria YES side is disabled", "readfix", PROMOTE,
     '        if ms is None or "copper_fungicide" not in ms:\n            return f"{slug}/alternaria-leaf-spot lost its copper rung; its prose names copper"',
     '        if False:\n            return f"{slug}/alternaria-leaf-spot lost its copper rung; its prose names copper"'),
    ("readfix: the copper-alternaria NO side is disabled", "readfix", PROMOTE,
     '        if ms is None or "copper_fungicide" in ms:', '        if False:'),
    ("readfix: the copper-downy pin is disabled", "readfix", PROMOTE,
     '        if ms is None or "copper_fungicide" not in ms:\n            return (f"{slug}/downy-mildew lost its copper rung',
     '        if False:\n            return (f"{slug}/downy-mildew lost its copper rung'),
    ("readfix: the spinosad YES side is disabled", "readfix", PROMOTE,
     '        if ms is None or "spinosad" not in ms:', '        if False:'),
    ("readfix: the spinosad NO side is disabled", "readfix", PROMOTE,
     '        if ms is None or "spinosad" in ms:', '        if False:'),
    ("readfix: the aphid-sanitation YES side is disabled", "readfix", PROMOTE,
     '        if ms is None or "garden_sanitation" not in ms:', '        if False:'),
    ("readfix: the aphid-sanitation NO side is disabled", "readfix", PROMOTE,
     '        if ms is None or "garden_sanitation" in ms:', '        if False:'),
    ("readfix: the damping-off rung-count pin is disabled", "readfix", PROMOTE,
     '        if ms is None or len(ms) != n:', '        if False:'),
    ("readfix: the DAMPING_OFF_RUNGS table is emptied", "readfix", PROMOTE,
     'DAMPING_OFF_RUNGS = {"radish": 2, "carrot": 3, "beet": 3}',
     'DAMPING_OFF_RUNGS = {}'),
    ("readfix: the prompt_harvest pins are disabled", "readfix", PROMOTE,
     '        if ms is None or "prompt_harvest" not in ms:', '        if False:'),
    ("readfix: the PROMPT_HARVEST_USES table is emptied", "readfix", PROMOTE,
     'PROMPT_HARVEST_USES = (("radish", "wireworms"), ("carrot", "carrot-rust-fly"),\n                       ("carrot", "cavity-spot"))',
     'PROMPT_HARVEST_USES = ()'),
    ("readfix: the neem/soap refusal-spec is disabled", "readfix", PROMOTE,
     '        if ms is not None and ("neem_oil" in ms or "insecticidal_soap" in ms):',
     '        if False:'),
    ("readfix: the DE exclusion is disabled in check", "readfix", PROMOTE,
     '                if "diatomaceous" in (r.get("note_beginner", "") + " " +',
     '                if False and "diatomaceous" in (r.get("note_beginner", "") + " " +'),
    ("readfix: verify_post handpick-regained is disabled", "readfix", PROMOTE,
     '    if "handpick" in ms:\n        return "post: beet\'s leafminer regained the wrong-meaning handpick rung"',
     '    if False:\n        return "post: beet\'s leafminer regained the wrong-meaning handpick rung"'),
    ("readfix: verify_post harlequin pin is disabled", "readfix", PROMOTE,
     '    if "handpick" not in ms:\n        return "post: turnip\'s harlequin bug lost handpick; the drop was scoped"',
     '    if False:\n        return "post: turnip\'s harlequin bug lost handpick; the drop was scoped"'),
    ("readfix: verify_post copper-downy is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" not in ms:\n            return f"post: {slug}/downy-mildew lost its copper rung"',
     '        if False:\n            return f"post: {slug}/downy-mildew lost its copper rung"'),
    ("readfix: verify_post copper-alternaria is disabled", "readfix", PROMOTE,
     '        if "copper_fungicide" in ms:\n            return f"post: {slug}/alternaria-leaf-spot gained a copper rung its prose refuses"',
     '        if False:\n            return f"post: {slug}/alternaria-leaf-spot gained a copper rung its prose refuses"'),
    ("readfix: verify_post spinosad pin is disabled", "readfix", PROMOTE,
     '        if "spinosad" in ms:\n            return f"post: {slug}/{FB} gained spinosad its prose does not name"',
     '        if False:\n            return f"post: {slug}/{FB} gained spinosad its prose does not name"'),
    ("readfix: verify_post prompt_harvest pin is disabled", "readfix", PROMOTE,
     '        if "prompt_harvest" not in ms:\n            return f"post: {slug}/{pid} lost prompt_harvest"',
     '        if False:\n            return f"post: {slug}/{pid} lost prompt_harvest"'),
    ("readfix: verify_post singular-id sweep is disabled", "readfix", PROMOTE,
     '            if p.get("id") == "flea-beetle":\n                return f"post: {slug} shipped the singular flea-beetle id"',
     '            if False:\n                return f"post: {slug} shipped the singular flea-beetle id"'),
    ("readfix: verify_post DE sweep is disabled", "readfix", PROMOTE,
     '                if "diatomaceous" in (r["note_beginner"] + " " + r["note_seasoned"]).lower():',
     '                if False:'),
    ("readfix: verify_post empty-ladder sweep is disabled", "readfix", PROMOTE,
     '            if not p.get("control_ladder"):\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{p.get(\'id\')}: no ladder after promote"'),

    # ---- twins ---------------------------------------------------------------------------------
    ("twins: the canonical-prose twin refusal is disabled", "twins", PROMOTE,
     '            if prose_signature(by[a]) == prose_signature(by[b]):', '            if False:'),
    ("twins: the staged-digest twin refusal is disabled", "twins", PROMOTE,
     '            if dg[a] == dg[b]:', '            if False:'),
    ("twins: the post content-identity refusal is disabled", "twins", PROMOTE,
     '            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):',
     '            if False:'),

    # ---- premise -------------------------------------------------------------------------------
    ("premise: the spinosad dusk premise is disabled", "premise", PROMOTE,
     '    if "dusk" not in spin:', '    if False:'),
    ("premise: the prompt_harvest meaning premise is disabled", "premise", PROMOTE,
     '    if "sooner" not in (m.get("best_use") or ""):', '    if False:'),
    ("premise: the already-laddered refusal is disabled", "premise", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

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
    ("validate: the missing-register refusal is disabled", "validate", PROMOTE,
     '                    if not str(r.get(k) or "").strip():', '                    if False:'),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),
    ("validate: the expected-rung table is zeroed", "validate", PROMOTE,
     'EXPECTED_RUNGS = {"turnip": 49, "radish": 29, "carrot": 24, "beet": 32}',
     'EXPECTED_RUNGS = {"turnip": 0, "radish": 0, "carrot": 0, "beet": 0}'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: the methods comparison is disabled", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: the sources comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "spinach")["name"] = "MUTATED"\n    batch = staged()'),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch9_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch9_roots")
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
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch9_roots")',
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
    print("MUTATION HARNESS -- batch 9 THE ROOTS (4 crops, 134 rungs, 0 mints)")
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
