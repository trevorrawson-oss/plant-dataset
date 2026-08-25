#!/usr/bin/env python3
"""Mutation harness for the PLA-8 batch-3 promote (PLA-215).

THE `distinct` FAMILY IS THIS BATCH'S LOAD-BEARING ONE, AND IT IS THE INVERSE OF BATCH 2'S `twin`.

Batch 2 asserted the four corns are byte-identical, because one crop was authored and the ladders
were propagated. `ladder_batch.py families` told this session to do the same to the three cucumbers.
That instruction was wrong: its twin signature was `tuple(sorted(problem_name(p)))`, problem NAMES
ONLY, and never compared prose. The cucumbers share 72.2% of their problem fields.

So here a PROPAGATION is the defect, and the mutations perform one in every direction it could
happen: at the staged files, at apply time, by moving a claim onto a crop that never made it, and by
stripping the claim from the crop that did. If a promote can quietly ship three crops carrying each
other's sourced variety claims, the whole reason this batch was authored three times is unverified,
and the next 18 batches inherit the same unchecked assumption in reverse.

THE `readfix` FAMILY guards the delta module. The staged files are the bots' untouched output and
the one fix the read found is applied on top. If the delta can silently become a no-op, or apply at
a stale index, the record stops distinguishing what the authors wrote from what the read changed.

`reach` mutations disable individual validate_batch checks. In batch 1 two such mutations SURVIVED,
because the suite proved only that SOME check fired, never that EACH did.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading, plus a
positive control and a SENTINEL that must redden or the run reports HARNESS DEAD.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch3.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch3.py")
CONTENT = os.path.join(HERE, "build_pla8_batch3_content.py")
MARKER = "# MUTATION-APPLIED"

APPLY_HEAD = "    batch = staged()\n    by = {c.get(\"slug\"): c for c in data[\"crops\"]}\n    minted = reused = 0"

MUTATIONS = [
    # ---- distinct: a propagation reaches canonical -------------------------------------------
    ("distinct: the staged-files-distinct check is disabled", "distinct", PROMOTE,
     '    if len(set(digests.values())) != len(CROPS):',
     '    if False and len(set(digests.values())) != len(CROPS):'),
    ("distinct: cucumber's ladders are propagated onto slicing at apply time", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    import copy as _c\n'
     '    for _f in ("pests", "diseases"):\n'
     '        batch["slicing-cucumber"][_f] = _c.deepcopy(batch["cucumber"][_f])'),
    ("distinct: pickling's ladders are propagated outward onto both siblings", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    import copy as _c\n'
     '    for _s in ("cucumber", "slicing-cucumber"):\n'
     '        for _f in ("pests", "diseases"):\n'
     '            batch[_s][_f] = _c.deepcopy(batch["pickling-cucumber"][_f])'),
    ("distinct: cucumber gains a resistant_varieties rung on BACTERIAL WILT", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _p in batch["cucumber"].get("diseases", []):\n'
     '        if _p["id"] == "bacterial-wilt":\n'
     '            _p["control_ladder"].insert(0, {"method": "resistant_varieties",\n'
     '                "note_beginner": "Pick a wilt-resistant variety.",\n'
     '                "note_seasoned": "Wilt-resistant cultivars are the plant-once lever."})'),
    ("distinct: County Fair is copied onto cucumber", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _p in batch["cucumber"].get("pests", []):\n'
     '        if _p["id"] == "cucumber-beetles":\n'
     '            _p["control_ladder"][0]["note_beginner"] += " Try County Fair."'),
    ("distinct: pickling LOSES its County Fair claim", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["pickling-cucumber"].get(_f, []):\n'
     '            for _r in _p["control_ladder"]:\n'
     '                for _k in ("note_beginner", "note_seasoned"):\n'
     '                    _r[_k] = _r[_k].replace("County Fair", "a tolerant variety")'),
    ("distinct: pickling LOSES its CMV-resistant claim", "distinct", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["pickling-cucumber"].get(_f, []):\n'
     '            for _r in _p["control_ladder"]:\n'
     '                for _k in ("note_beginner", "note_seasoned"):\n'
     '                    _r[_k] = _r[_k].replace("CMV-resistant", "virus-tolerant")'),
    ("distinct: the DISTINCT_CLAIMS loop is disabled", "distinct", PROMOTE,
     '    for crop, pid, method, want in DISTINCT_CLAIMS:\n'
     '        lad = ladder_of(batch[crop], pid)',
     '    for crop, pid, method, want in []:\n'
     '        lad = ladder_of(batch[crop], pid)'),
    ("distinct: the PINNED_PROSE loop is disabled", "distinct", PROMOTE,
     '    for owner, needle in PINNED_PROSE:\n'
     '        for crop in CROPS:\n'
     '            blob = json.dumps(batch[crop], ensure_ascii=False)',
     '    for owner, needle in []:\n'
     '        for crop in CROPS:\n'
     '            blob = json.dumps(batch[crop], ensure_ascii=False)'),
    ("distinct: check_distinctness is never called", "distinct", PROMOTE,
     '    problem = check_distinctness(batch)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),

    # ---- readfix: the delta module -----------------------------------------------------------
    ("readfix: apply_read_fixes becomes a no-op", "readfix", CONTENT,
     '    applied = 0\n    for ins in INSERTS:',
     '    applied = len(INSERTS)\n    for ins in []:'),
    ("readfix: INSERTS is emptied", "readfix", CONTENT,
     'INSERTS = [\n    {',
     'INSERTS = []\nUNUSED = [\n    {'),
    ("readfix: the stale-index guard is disabled", "readfix", CONTENT,
     '        if before != ins["expect_before"]:',
     '        if False and before != ins["expect_before"]:'),
    ("readfix: the rung lands at the WRONG ladder position", "readfix", CONTENT,
     '        lad.insert(ins["index"], dict(ins["rung"]))',
     '        lad.insert(len(lad), dict(ins["rung"]))'),
    ("readfix: the expected read-fix count is not enforced", "readfix", PROMOTE,
     '    if n != EXPECTED_READ_FIXES:',
     '    if False and n != EXPECTED_READ_FIXES:'),

    # ---- reach: individual validate_batch checks disabled -------------------------------------
    ("reach: the EMPTY-ladder check is disabled", "reach", PROMOTE,
     '                if not lad:',
     '                if False and not lad:'),
    ("reach: the tier-order check is disabled", "reach", PROMOTE,
     '                if tiers != sorted(tiers):',
     '                if False and tiers != sorted(tiers):'),
    ("reach: the identical-registers check is disabled", "reach", PROMOTE,
     '                    if r["note_beginner"] == r["note_seasoned"]:',
     '                    if False and r["note_beginner"] == r["note_seasoned"]:'),
    ("reach: the applies_to check is disabled", "reach", PROMOTE,
     '                    if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                    if False:'),
    ("reach: the problem-count check is disabled", "reach", PROMOTE,
     '        if n_prob != EXPECTED_PROBLEMS_PER_CROP:',
     '        if False and n_prob != EXPECTED_PROBLEMS_PER_CROP:'),
    ("reach: the per-crop rung-count check is disabled", "reach", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:',
     '        if False and n != EXPECTED_RUNGS[slug]:'),

    # ---- ids ----------------------------------------------------------------------------------
    ("ids: a canonical id is overwritten by the staged one", "ids", PROMOTE,
     '                if isinstance(tgt.get("id"), str) and tgt["id"]:\n'
     '                    reused += 1\n'
     '                else:\n'
     '                    tgt["id"] = add["id"]\n'
     '                    minted += 1',
     '                tgt["id"] = add["id"]\n'
     '                minted += 1'),

    # ---- blast --------------------------------------------------------------------------------
    ("blast: english-cucumber is swept in", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    by["english-cucumber"]["name"] = "MUTATED"'),
    ("blast: a batch-2 corn is touched", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    by["sweet-corn"]["name"] = "MUTATED"'),
    ("blast: a control_method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["control_methods"]["bt"]["applies_to"].append("viral")'),
    ("blast: the staged files are written back to disk", "blast", PROMOTE,
     '    batch = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}',
     '    batch = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}\n'
     '    json.dump(batch["cucumber"], open(os.path.join(STAGING, "out_cucumber.json"), "w"))'),

    # ---- mechanics ----------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: a bare safety claim enters new rung prose", "mechanics", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _s in CROPS:\n'
     '        for _f in ("pests", "diseases"):\n'
     '            for _p in batch[_s].get(_f, []):\n'
     '                for _r in _p["control_ladder"]:\n'
     '                    if _r["method"] == "sulfur":\n'
     '                        _r["note_beginner"] += " Sulfur is safe on food crops."'),
    ("mechanics: an em dash enters new rung prose", "mechanics", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _p in batch["cucumber"].get("pests", []):\n'
     '        _p["control_ladder"][0]["note_beginner"] += " Watch closely — they move fast."'),
    ("mechanics: anthracnose gains a spray rung it has no material for", "mechanics", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _p in batch["cucumber"].get("diseases", []):\n'
     '        if _p["id"] == "anthracnose":\n'
     '            _p["control_ladder"].append({"method": "copper_fungicide",\n'
     '                "note_beginner": "Copper slows it.", "note_seasoned": "Copper is protective."})'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            "def apply_to(data):", "def apply_to(data):\n    return 0, 0, 0")


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
    """The staged batch is COPIED into the sandbox so a mutation that writes it back cannot damage
    the real authored files. Both the promote AND the delta module are copied every time, so the
    promote's `from build_pla8_batch3_content import ...` always resolves inside the sandbox."""
    wd = tempfile.mkdtemp(prefix="mutate_b3_")
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch3"), sandbox_staging)

    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)

    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch3")',
        f'STAGING = {sandbox_staging!r}', 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)

    c = open(CONTENT).read()
    if path == CONTENT:
        c = c.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(CONTENT)), "w").write(c)

    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 3 (the three cucumbers, NOT a twin group)")
    print("=" * 78)
    if not preflight():
        return 1

    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails -- the clean suite is not green in the sandbox.")
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
