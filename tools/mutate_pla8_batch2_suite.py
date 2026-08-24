#!/usr/bin/env python3
"""Mutation harness for the PLA-8 batch-2 promote (PLA-215).

THE `twin` FAMILY IS THIS BATCH'S LOAD-BEARING ONE, and it exists because of how the batch was cut.
Batch 2 is the first grouped by FAMILY rather than size, and the justification is that the four corns
share their prose: ONE crop was authored and the ladders propagated. If a promote can quietly ship
four crops that are NOT identical, the family cut has no verified premise and the next 20 batches
inherit an unchecked assumption. Four mutations break the identity in different places.

THE `raccoons` FAMILY guards the batch's whole causal chain. Raccoons had no expressible rung, an
agent refused to pad it, and that refusal produced BOTH the `exclusion_fencing` mint (r4) and the
empty-ladder gate fix (a256211). If raccoons can silently regress to blank or to a near-miss method,
all of that work is undone in one edit.

`reach` mutations disable individual validate_batch checks. In batch 1 two such mutations SURVIVED,
because the suite proved only that SOME check fired, never that EACH did. That lesson is why
RefusalReachability exists here from the start.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch2.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch2.py")
MARKER = "# MUTATION-APPLIED"

APPLY_HEAD = "    batch = staged()\n    by = {c.get(\"slug\"): c for c in data[\"crops\"]}\n    minted = reused = 0"

MUTATIONS = [
    # ---- twin: the family-cut premise is broken ---------------------------------------------
    ("twin: the identity check is disabled", "twin", PROMOTE,
     '    if len(set(digests.values())) != 1:',
     '    if False and len(set(digests.values())) != 1:'),
    ("twin: one crop gets a different ladder at apply time", "twin", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["popcorn"].get(_f, []):\n'
     '            _p["control_ladder"] = _p["control_ladder"][:1]'),
    ("twin: one crop's prose diverges while its methods match", "twin", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["flint-corn"].get(_f, []):\n'
     '            for _r in _p["control_ladder"]:\n'
     '                _r["note_beginner"] = _r["note_beginner"] + " Extra."'),
    ("twin: only the authored crop is promoted", "twin", PROMOTE,
     '    for slug in CROPS:\n        crop = by[slug]',
     '    for slug in (AUTHORED,):\n        crop = by[slug]'),
    # ---- raccoons: the causal chain of this whole batch ---------------------------------------
    ("raccoons: the ladder regresses to empty", "raccoons", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _s in CROPS:\n'
     '        for _p in batch[_s].get("pests", []):\n'
     '            if _p["id"] == "raccoons":\n'
     '                _p["control_ladder"] = []'),
    ("raccoons: it is repointed to a near-miss vertebrate method", "raccoons", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _s in CROPS:\n'
     '        for _p in batch[_s].get("pests", []):\n'
     '            if _p["id"] == "raccoons":\n'
     '                _p["control_ladder"][0]["method"] = "bird_netting"'),
    ("raccoons: the rung imports the METHOD's figures over the CROP's", "raccoons", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _s in CROPS:\n'
     '        for _p in batch[_s].get("pests", []):\n'
     '            if _p["id"] == "raccoons":\n'
     '                for _k in ("note_beginner", "note_seasoned"):\n'
     '                    _p["control_ladder"][0][_k] = _p["control_ladder"][0][_k].replace(\n'
     '                        "4 and 8", "4 to 6 and 12")'),
    # ---- reach: individual validate_batch checks disabled ---------------------------------------
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
    # ---- ids -----------------------------------------------------------------------------------
    ("ids: a canonical id is overwritten by the staged one", "ids", PROMOTE,
     '                if isinstance(tgt.get("id"), str) and tgt["id"]:\n'
     '                    reused += 1\n'
     '                else:\n'
     '                    tgt["id"] = add["id"]\n'
     '                    minted += 1',
     '                tgt["id"] = add["id"]\n'
     '                minted += 1'),
    # ---- blast -----------------------------------------------------------------------------------
    ("blast: a batch-1 crop is touched", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    by["basil"]["name"] = "MUTATED"'),
    ("blast: a control_method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["control_methods"]["bt"]["applies_to"].append("viral")'),
    ("blast: the staged files are written back to disk", "blast", PROMOTE,
     '    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}',
     '    _b = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}\n'
     '    json.dump(_b["popcorn"], open(os.path.join(STAGING, "out_popcorn.json"), "w"))\n'
     '    return _b'),
    # ---- mechanics ---------------------------------------------------------------------------------
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
     '                    if _r["method"] == "bt":\n'
     '                        _r["note_beginner"] += " Bt is safe for people and pets."'),
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
    the real authored files."""
    wd = tempfile.mkdtemp(prefix="mutate_b2_")
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch2"), sandbox_staging)

    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)

    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch2")',
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
    print("MUTATION HARNESS -- PLA-8 batch 2 (the four corns, family cut)")
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
