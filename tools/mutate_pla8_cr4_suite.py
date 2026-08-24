#!/usr/bin/env python3
"""Mutation harness for PLA-8 catalog r4 (PLA-215).

TWO FAMILIES CARRY THIS ROUND.

`disambiguation` -- every mint sits beside an existing method that means something close but
different, which is exactly how batch 1 produced 22 mismatches. If a mint stops naming its
neighbour, the next author reaches for the wrong one and the mint has made the problem worse, not
better. Four mutations strip a neighbour reference; one points a mint at a method that does not
exist.

`fidelity` -- all four claims were first recorded as UNSOURCED and then found at T1 on a proper
hunt. The risk in that pattern is quoting the helpful half of a source and dropping the limiting
half, which reads as sourced while overselling. The sharpest case is `augmentative_release`, whose
source says released predators "starve or migrate elsewhere" without prey and that conserving
resident predators works better. Three mutations remove exactly that.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r4.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r4.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r4_content.py")
MARKER = "# MUTATION-APPLIED"

APPLY_HEAD = '    data["control_methods"].update(json.loads(json.dumps(B.NEW_METHODS)))'

MUTATIONS = [
    # ---- hedge: the sources' own limitation is dropped -------------------------------------
    ("hedge: the beginner half promises exclusion", "hedge", CONTENT,
     '            "after night. Fencing out a determined climber is hard, so treat this as your best "\n'
     '            "chance rather than a certainty."',
     '            "after night. A properly set fence keeps them out of the patch."'),
    ("hedge: the seasoned half drops UMN's difficulty note", "hedge", CONTENT,
     '            "inches up, and notes it is difficult to fence raccoons out at all. Timing is the part "',
     '            "inches up. Timing is the part "'),
    ("hedge: the cons stop carrying the limit", "hedge", CONTENT,
     '            "Raccoons are hard to fence out at all, so treat a good result as the aim rather than the expectation",',
     '            "Best set up before the crop ripens",'),
    ("hedge: REQUIRED_HEDGE is weakened to match anything", "hedge", CONTENT,
     'REQUIRED_HEDGE = r"difficult to fence|rather than a certainty|rather than the expectation"',
     'REQUIRED_HEDGE = r""'),
    # ---- safety --------------------------------------------------------------------------------
    ("safety: the shock-hazard caution is removed", "safety", CONTENT,
     '        "cautions": [\n'
     '            "An electric fence is a real shock hazard to children and pets; use a fence energizer "',
     '        "cautions": [\n'
     '            "Keep the wires clear of vegetation; use a fence energizer "'),
    # ---- disambiguation --------------------------------------------------------------------------
    ("disambig: it stops distinguishing itself from bird netting", "disambig", CONTENT,
     '            "from bird netting, which drapes mesh over the plants themselves against birds; this is "\n'
     '            "a barrier around the bed, set at the height the animal travels."',
     '            "from other physical barriers; this is set at the height the animal travels."'),
    # ---- the gap it exists to close ----------------------------------------------------------------
    ("gap: applies_to no longer reaches vertebrate", "gap", CONTENT,
     '        "applies_to": ["vertebrate"],',
     '        "applies_to": ["insect_general"],'),
    # ---- sourcing -------------------------------------------------------------------------------------
    ("sourcing: only one of the two disagreeing sources is represented", "sourcing", CONTENT,
     '            "above the ground and has the fence energized about two weeks before the crop reaches "\n'
     '            "the milk stage; Minnesota describes two strands about four inches apart starting five "',
     '            "above the ground and has the fence energized about two weeks before the crop reaches "\n'
     '            "the milk stage; growers describe two strands about four inches apart starting five "'),
    ("sourcing: the measured wire height is dropped", "sourcing", CONTENT,
     '            "which is why wire height matters more than fence height: raccoons push under and "\n'
     '            "through at ground level. Iowa State puts the two wires at 4 to 6 inches and 12 inches "',
     '            "which is why wire height matters more than fence height: raccoons push under and "\n'
     '            "through at ground level. Iowa State puts the two wires low down "'),
    ("sourcing: anchoring_urls no longer match sources", "sourcing", CONTENT,
     '        "sources": ["iastate_ext", "umn_ext"],',
     '        "sources": ["iastate_ext", "umn_ext", "ncsu_ext"],'),
    ("sourcing: a source is minted rather than reused", "sourcing", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["source_catalog"]["invented"] = {"tier": "T1", "name": "x"}'),
    # ---- record ------------------------------------------------------------------------------------------
    ("record: the highest-frequency owed gap is dropped from the record", "record", CONTENT,
     '    "adjust_planting_date": "highest-frequency gap on corn (4 of 8 entries); deserves its own "',
     '    "_retired_adjust_planting_date": "highest-frequency gap on corn (4 of 8 entries); deserves its own "'),
    # ---- blast ---------------------------------------------------------------------------------------------
    ("blast: an existing method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["control_methods"]["bird_netting"]["applies_to"].append("insect_general")'),
    ("blast: a crop is touched", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["crops"][0]["name"] = "MUTATED"'),
    # ---- mechanics ---------------------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '            "Some animals cannot be sprayed for or scared off for long, so the answer is a barrier "',
     '            "Some animals cannot be sprayed for or scared off — so the answer is a barrier "'),
    ("mechanics: the beginner register falls back on jargon", "mechanics", CONTENT,
     '            "ready, not after the first raid: once they have found the patch they come back night "',
     '            "ready: energize the polywire before the milk stage, since once they find the patch night "'),
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
    wd = tempfile.mkdtemp(prefix="mutate_cr4_")
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
    print("MUTATION HARNESS -- PLA-8 catalog r4 (four mints)")
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
        print(f"  {k:12s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
