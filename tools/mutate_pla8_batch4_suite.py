#!/usr/bin/env python3
"""Mutation harness for the PLA-8 batch-4 promote (PLA-215).

THE `hybrid` FAMILY IS LOAD-BEARING AND IS NEW. Batch 2 refuses if its corns DIVERGE; batch 3
refuses if its cucumbers CONVERGE. This batch is both at once -- a verified 40/40 twin pair authored
once and propagated, and a trio at 73-80% authored three times -- so a promote that cannot tell the
two groupings apart would ship one of the two defects those batches exist to prevent. Mutations
break the premise in both directions.

DISTINCTNESS IS ABOUT PROSE, NOT METHOD KEYS. The trio converges on identical method sequences and
that is correct. Comparing method keys refused this batch on its first dry run, so one mutation
re-tightens the check that way and must redden.

THE `readfix` FAMILY guards three corrections found ACROSS siblings, two of them surfaced
mechanically by the new cross-sibling check: copper dropped where the prose names no material,
borer_stem_surgery replacing a handpick rung whose own con is "Misses hidden eggs and tiny larvae",
and a problem id normalized to the roster's shipped spelling because ids are join keys.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch4.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch4.py")
MARKER = "# MUTATION-APPLIED"

APPLY = ('    batch = staged()\n    by = {c.get("slug"): c for c in data["crops"]}\n'
         '    minted = reused = 0')

MUTATIONS = [
    # ---- hybrid: both premises, both directions ------------------------------------------------
    ("hybrid: the twin-identity check is disabled", "hybrid", PROMOTE,
     '    if dg[TWIN[0]] != dg[TWIN[1]]:', '    if False:'),
    ("hybrid: the trio-distinctness check is disabled", "hybrid", PROMOTE,
     '    if len(set(trio_dg.values())) != len(TRIO):', '    if False:'),
    ("hybrid: the twin pair diverges at apply time", "hybrid", PROMOTE, APPLY,
     APPLY + '\n    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["zucchini-courgette"].get(_f, []):\n'
     '            _p["control_ladder"] = _p["control_ladder"][:1]'),
    ("hybrid: acorn is propagated over butternut at apply time", "hybrid", PROMOTE, APPLY,
     APPLY + '\n    import copy as _c\n    for _f in ("pests", "diseases"):\n'
     '        batch["butternut-squash"][_f] = _c.deepcopy(batch["acorn-squash"][_f])'),
    ("hybrid: only the authored twin is promoted", "hybrid", PROMOTE,
     '    for slug in CROPS:\n        crop = by[slug]',
     '    for slug in (AUTHORED,) + TRIO:\n        crop = by[slug]'),
    ("hybrid: the cross-family collision check is disabled", "hybrid", PROMOTE,
     '    if dg[TWIN[0]] in trio_dg.values():', '    if False:'),
    ("hybrid: distinctness re-tightened onto METHOD KEYS (refuses a correct batch)", "hybrid",
     PROMOTE,
     '        return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])\n'
     '                            for r in p["control_ladder"]]',
     '        return json.dumps([[(r["method"],)\n'
     '                            for r in p["control_ladder"]]'),

    # ---- readfix: the three cross-sibling corrections --------------------------------------------
    ("readfix: copper returns to a downy-mildew ladder", "readfix", PROMOTE, APPLY,
     APPLY + '\n    for _p in batch["acorn-squash"].get("diseases", []):\n'
     '        if _p["id"] == "downy-mildew":\n'
     '            _p["control_ladder"].append({"method": "copper_fungicide",\n'
     '                "note_beginner": "Copper helps.", "note_seasoned": "Copper is protective."})'),
    ("readfix: the pre-apply copper guard is disabled", "readfix", PROMOTE,
     '                if p.get("id") == "downy-mildew" and "copper_fungicide" in methods:\n'
     '                    return (f"{slug}/downy-mildew carries copper_fungicide, but this crop\'s prose "',
     '                if False:\n'
     '                    return (f"{slug}/downy-mildew carries copper_fungicide, but this crop\'s prose "'),
    ("readfix: the POST copper guard is disabled", "readfix", PROMOTE,
     '                if p.get("id") == "downy-mildew" and "copper_fungicide" in methods:\n'
     '                    return f"post: {slug}/downy-mildew regained copper_fungicide"',
     '                if False:\n'
     '                    return f"post: {slug}/downy-mildew regained copper_fungicide"'),
    ("readfix: a borer ladder loses the minted method", "readfix", PROMOTE, APPLY,
     APPLY + '\n    for _p in batch["acorn-squash"].get("pests", []):\n'
     '        if _p["id"] == "squash-vine-borer":\n'
     '            _p["control_ladder"] = [_r for _r in _p["control_ladder"]\n'
     '                                    if _r["method"] != BORER_METHOD]'),
    ("readfix: handpick returns to a borer ladder", "readfix", PROMOTE, APPLY,
     APPLY + '\n    for _p in batch["acorn-squash"].get("pests", []):\n'
     '        if _p["id"] == "squash-vine-borer":\n'
     '            _p["control_ladder"].insert(1, {"method": "handpick",\n'
     '                "note_beginner": "Pick the grub out.", "note_seasoned": "Hand removal."})'),
    ("readfix: the borer-method guard is disabled", "readfix", PROMOTE,
     '                    if BORER_METHOD not in methods:', '                    if False:'),
    ("readfix: a problem id reverts to the singular", "readfix", PROMOTE, APPLY,
     APPLY + '\n    for _p in batch["acorn-squash"].get("pests", []):\n'
     '        if _p["id"] == "cucumber-beetles":\n            _p["id"] = "cucumber-beetle"'),
    ("readfix: the id-convention guard is disabled", "readfix", PROMOTE,
     '                if want and p.get("id") != want:', '                if False:'),
    ("readfix: the id guard reads the STAGED name again (its original dead form)", "readfix",
     PROMOTE,
     '                name = (canon[idx].get("name") if idx < len(canon) else None) or ""',
     '                name = p.get("name") or ""'),

    # ---- reach ------------------------------------------------------------------------------------
    ("reach: the EMPTY-ladder check is disabled", "reach", PROMOTE,
     '                if not lad:', '                if False and not lad:'),
    ("reach: the tier-order check is disabled", "reach", PROMOTE,
     '                if tiers != sorted(tiers):', '                if False:'),
    ("reach: the applies_to check is disabled", "reach", PROMOTE,
     '                    if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                    if False:'),
    ("reach: the identical-registers check is disabled", "reach", PROMOTE,
     '                    if r["note_beginner"] == r["note_seasoned"]:', '                    if False:'),
    ("reach: the per-crop rung count is not enforced", "reach", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),
    ("reach: the mint-round precondition is disabled", "reach", PROMOTE,
     '    if BORER_METHOD not in cm:', '    if False:'),

    # ---- ids / blast / mechanics -------------------------------------------------------------------
    ("ids: a canonical id is overwritten by the staged one", "ids", PROMOTE,
     '                if isinstance(tgt.get("id"), str) and tgt["id"]:\n'
     '                    reused += 1\n                else:\n'
     '                    tgt["id"] = add["id"]\n                    minted += 1',
     '                tgt["id"] = add["id"]\n                minted += 1'),
    ("blast: pumpkin is swept in", "blast", PROMOTE, APPLY,
     APPLY + '\n    by["pumpkin"]["name"] = "MUTATED"'),
    ("blast: a batch-3 cucumber is touched", "blast", PROMOTE, APPLY,
     APPLY + '\n    by["cucumber"]["name"] = "MUTATED"'),
    ("blast: a control_method is edited", "blast", PROMOTE, APPLY,
     APPLY + '\n    data["control_methods"][BORER_METHOD]["applies_to"].append("insect_chewing")'),
    ("blast: the staged files are written back", "blast", PROMOTE,
     '    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}',
     '    _b = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}\n'
     '    json.dump(_b["acorn-squash"], open(os.path.join(STAGING, "out_acorn-squash.json"), "w"))\n'
     '    return _b'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: a conventional rung is invented", "mechanics", PROMOTE, APPLY,
     APPLY + '\n    for _p in batch["acorn-squash"].get("pests", []):\n'
     '        if _p["id"] == "squash-bug":\n'
     '            _p["control_ladder"].append({"method": "carbaryl",\n'
     '                "note_beginner": "A last resort.", "note_seasoned": "A rescue material."})'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE, "def apply_to(data):",
            "def apply_to(data):\n    return 0, 0, 0")


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
            bad.append(f"  {n}x  {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_b4_")
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch4"), sandbox_staging)
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch4")',
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
    print("MUTATION HARNESS -- PLA-8 batch 4 (five squashes: a twin pair AND a trio)")
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
