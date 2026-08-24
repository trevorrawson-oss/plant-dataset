#!/usr/bin/env python3
"""Mutation harness for the PLA-8 batch-1 promote (PLA-215).

THE `merge` FAMILY IS THE ONE THAT MATTERS. Eight of the eighteen fixes merge two rungs into one,
and a merge is the easiest fix in this arc to fake: simply DROPPING the prune_out_infection rung
satisfies "no prune_out_infection survives", passes every structural gate, and silently deletes half
the advice a reader needed. Three mutations do exactly that in different ways, and one guts the
evidence table that is supposed to catch it.

THE `stillopen` FAMILY guards the opposite temptation. Four rungs are deliberately left unfixed
because the method they need cannot be honestly minted yet. Closing one with a near-miss method
would look like a better result (22 of 22 rather than 18 of 22) and be a worse one. Two mutations
close them the tempting way.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch1.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch1.py")
CONTENT = os.path.join(HERE, "build_pla8_batch1_content.py")
MARKER = "# MUTATION-APPLIED"

# The three-line body is IDENTICAL in the MERGES and MERGE_TO loops, so the anchor must include the
# prune_out_infection check_at line to be unique. Preflight caught this as a 2x match.
MERGE_LOOP = ('        check_at(m["crop"], m["pid"], m["drop"], "prune_out_infection")\n'
              '        L[m["keep"]]["note_beginner"] = m["note_beginner"]\n'
              '        L[m["keep"]]["note_seasoned"] = m["note_seasoned"]\n'
              '        L.pop(m["drop"])')

MUTATIONS = [
    # ---- merge: the fix is faked by dropping rather than merging ---------------------------
    ("merge: the prune rung is DROPPED without merging its content", "merge", PROMOTE,
     MERGE_LOOP,
     '        check_at(m["crop"], m["pid"], m["drop"], "prune_out_infection")\n'
     '        L.pop(m["drop"])'),
    ("merge: only the sanitation half survives the merge", "merge", PROMOTE,
     MERGE_LOOP,
     '        check_at(m["crop"], m["pid"], m["drop"], "prune_out_infection")\n'
     '        L[m["keep"]]["note_seasoned"] = m["note_seasoned"]\n'
     '        L.pop(m["drop"])'),
    ("merge: basil's merged note loses the removal half", "merge", CONTENT,
     '            "leaves, and carry them out of the garden. If only part of a plant is affected, cut "\n'
     '            "those heavily infected stems out instead and take them away rather than dropping them "\n'
     '            "on the ground. Every infected plant left standing is shedding spores onto its "\n'
     '            "neighbors.",',
     '            "leaves, and carry them out of the garden. Every infected plant left standing is "\n'
     '            "shedding spores onto its neighbors.",'),
    ("merge: the evidence table is gutted so nothing is compared", "merge", SUITE,
     'MERGE_EVIDENCE = {\n    ("basil", "downy-mildew"):',
     'MERGE_EVIDENCE = {\n    ("_skip", "_skip"): ("", ""),\n    ("basil", "downy-mildew"):'),
    # ---- stillopen: the four open rungs are closed the tempting way ---------------------------
    ("stillopen: fig's nematode rung is closed with a near-miss method", "stillopen", PROMOTE,
     '    for e in B.EDIT_NOTES:',
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["fig"].get(_f, []):\n'
     '            if _p["id"] == "root-knot-nematode":\n'
     '                _p["control_ladder"][0]["method"] = "crop_rotation"\n'
     '    for e in B.EDIT_NOTES:'),
    ("stillopen: the padded pepper-maggot ladder is trimmed anyway", "stillopen", PROMOTE,
     '    for e in B.EDIT_NOTES:',
     '    for _f in ("pests", "diseases"):\n'
     '        for _p in batch["jalapeno"].get(_f, []):\n'
     '            if _p["id"] == "pepper-maggot":\n'
     '                _p["control_ladder"] = _p["control_ladder"][:1]\n'
     '    for e in B.EDIT_NOTES:'),
    ("stillopen: the recorded reasons are emptied so the close looks complete", "stillopen", CONTENT,
     'STILL_OPEN = {\n    "fig/root-knot-nematode":',
     'STILL_OPEN = {\n    "_retired/fig-root-knot-nematode":'),
    # ---- fixes ---------------------------------------------------------------------------------
    ("fixes: a hornworm repoint silently does not happen", "fixes", CONTENT,
     '    {"crop": "jalapeno", "pid": "hornworms", "rung": 0,\n'
     '     "from": "garden_sanitation", "to": "off_season_tillage"},',
     '    {"crop": "jalapeno", "pid": "hornworms", "rung": 0,\n'
     '     "from": "garden_sanitation", "to": "garden_sanitation"},'),
    ("fixes: the jalapeno trap KEY is moved instead of the clause dropped", "fixes", PROMOTE,
     '        L[e["rung"]]["note_beginner"] = e["note_beginner"]\n'
     '        L[e["rung"]]["note_seasoned"] = e["note_seasoned"]\n\n'
     '    return batch',
     '        L[e["rung"]]["method"] = "handpick"\n\n'
     '    return batch'),
    ("fixes: the lure clause survives the rewrite", "fixes", CONTENT,
     '            "Set yellow sticky traps around the edge of the bed, down low near the soil, so you "',
     '            "Set sticky traps baited with the weevil\'s scent lure around the edge of the bed, so you "'),
    ("fixes: a split does not insert its new rung", "fixes", PROMOTE,
     '        L.insert(s["insert_at"], {"method": s["new_method"],',
     '        L.append({"method": "handpick",\n'
     '                  "_unused": s["insert_at"], "_m": s["new_method"],'),
    # ---- ids -------------------------------------------------------------------------------------
    ("ids: a canonical id is overwritten by the staged one", "ids", PROMOTE,
     '                if isinstance(tgt.get("id"), str) and tgt["id"]:\n'
     '                    reused += 1\n'
     '                else:\n'
     '                    tgt["id"] = add["id"]\n'
     '                    minted += 1',
     '                tgt["id"] = add["id"]\n'
     '                minted += 1'),
    # ---- integrity ---------------------------------------------------------------------------------
    ("integrity: the tier-order check is disabled", "integrity", PROMOTE,
     '                if tiers != sorted(tiers):',
     '                if False and tiers != sorted(tiers):'),
    ("integrity: the empty-register check is disabled", "integrity", PROMOTE,
     '                        if not str(r.get(k) or "").strip():',
     '                        if False and not str(r.get(k) or "").strip():'),
    # ---- blast ---------------------------------------------------------------------------------------
    ("blast: an unrelated crop is touched", "blast", PROMOTE,
     '    minted = reused = 0',
     '    minted = reused = 0\n    by["broccoli"]["name"] = "MUTATED"'),
    ("blast: a control_method is edited", "blast", PROMOTE,
     '    minted = reused = 0',
     '    minted = reused = 0\n    data["control_methods"]["handpick"]["applies_to"].append("viral")'),
    # ---- staging ---------------------------------------------------------------------------------------
    ("staging: the authored file is written back to disk", "staging", PROMOTE,
     '    return batch\n\n\ndef validate_batch',
     '    import json as _j\n'
     '    _j.dump(batch["fig"], open(os.path.join(STAGING, "out_fig.json"), "w"))\n'
     '    return batch\n\n\ndef validate_batch'),
    # ---- mechanics ---------------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '            "Strip off the spotted lower leaves as soon as you find them. The sooner they are off "',
     '            "Strip off the spotted lower leaves as soon as you find them — the sooner they are off "'),
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
    wd = tempfile.mkdtemp(prefix="mutate_b1_")
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch1"), sandbox_staging)

    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    if path == SUITE:
        src = src.replace(old, new + "  " + MARKER, 1)
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)

    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if f == PROMOTE:
            s = s.replace(
                'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch1")',
                f'STAGING = {sandbox_staging!r}', 1)
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)

    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 1 (5 crops, 18 read-fixes)")
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
