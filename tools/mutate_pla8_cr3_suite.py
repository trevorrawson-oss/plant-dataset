#!/usr/bin/env python3
"""Mutation harness for PLA-8 catalog r3 (PLA-215).

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
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r3.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r3.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r3_content.py")
MARKER = "# MUTATION-APPLIED"

APPLY_HEAD = '    data["control_methods"].update(json.loads(json.dumps(B.NEW_METHODS)))'

MUTATIONS = [
    # ---- disambiguation ---------------------------------------------------------------------
    ("disambig: prompt_harvest stops naming garden sanitation", "disambig", CONTENT,
     '            "and sap beetles, and where birds and squirrels take ripe fruit. Distinct from garden "',
     '            "and sap beetles, and where birds and squirrels take ripe fruit. Much like the "'),
    ("disambig: sound_sowing stops distinguishing itself from seeding DENSITY", "disambig", CONTENT,
     '            "rate, which is about sowing DENSITY and crowding rather than about how fast the seed "',
     '            "rate, which is a similar sort of sowing decision about how fast the seed "'),
    ("disambig: augmentative_release stops contrasting with conservation", "disambig", CONTENT,
     '            "place. Distinct from beneficial predators, which is about CONSERVING the natural "',
     '            "place. Works alongside other living controls, which involve the natural "'),
    ("disambig: resistant_rootstock stops contrasting with cultivar choice", "disambig", CONTENT,
     '            "already established. Distinct from resistant varieties, which is choosing a different "',
     '            "already established. Similar to picking a tough sort, which is choosing a different "'),
    ("disambig: a mint points at a neighbour that is not in the catalog", "disambig", CONTENT,
     '    "resistant_rootstock": "resistant varieties",',
     '    "resistant_rootstock": "tolerant rootstocks",'),
    # ---- source fidelity --------------------------------------------------------------------
    ("fidelity: augmentative_release drops the starve-or-migrate caveat", "fidelity", CONTENT,
     '            "or migrate elsewhere if prey is not available when they arrive. The commercially "',
     '            "and establish readily once released into the planting. The commercially "'),
    ("fidelity: augmentative_release drops 'naturally occurring predators' outperforming it", "fidelity", CONTENT,
     '            "populations in large plantings or orchards, but the best results come from creating "',
     '            "populations in gardens as well as orchards, and results come from creating "'),
    ("fidelity: the cons stop carrying the limit", "fidelity", CONTENT,
     '            "Released predators starve or move on if prey is not present when they arrive",',
     '            "Works best when released early, before the pest is easy to find",'),
    ("fidelity: sound_sowing drops the measured depth figure", "fidelity", CONTENT,
     '            "compressing that window: vigorously growing seedlings pass through it fairly quickly "',
     '            "compressing that window: seedlings pass through it fairly quickly "'),
    ("fidelity: the pheromone_trap correction is downgraded to a plain gap", "fidelity", CONTENT,
     '    "pheromone_trap": "NOT NEEDED. UF/IFAS EENY-278 shows yellow sticky traps ARE the published "',
     '    "pheromone_trap": "still owed; no anchor found yet. Previously: EENY-278 shows traps are published "'),
    # ---- sourcing ----------------------------------------------------------------------------
    ("sourcing: a recorded quote is attributed to the wrong source id", "sourcing", CONTENT,
     '    {"id": "umn_ext", "for": "resistant_rootstock", "read": "2026-08-24",',
     '    {"id": "ncsu_ext", "for": "resistant_rootstock", "read": "2026-08-24",'),
    ("sourcing: anchoring_urls no longer match sources", "sourcing", CONTENT,
     '        "sources": ["ucanr_ext", "ncsu_ext"],',
     '        "sources": ["ucanr_ext", "ncsu_ext", "umn_ext"],'),
    ("sourcing: a source is minted rather than reused", "sourcing", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["source_catalog"]["invented_source"] = {"tier": "T1", "name": "x"}'),
    # ---- reachability -------------------------------------------------------------------------
    ("reach: a mint targets a class no problem type can reach", "reach", CONTENT,
     '        "applies_to": ["insect_soft_bodied", "mite", "insect_general"],',
     '        "applies_to": ["insect_soft_bodied", "mite", "arachnid_general"],'),
    # ---- blast radius --------------------------------------------------------------------------
    ("blast: an existing method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["control_methods"]["handpick"]["applies_to"].append("viral")'),
    ("blast: a crop is touched", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["crops"][0]["name"] = "MUTATED"'),
    # ---- mechanics ----------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: a spaced degF enters consumer copy", "mechanics", CONTENT,
     '            "width of the seed and favorable germination temperatures at 65 to 70°F for most seeds, "',
     '            "width of the seed and favorable germination temperatures at 65 to 70 °F for most seeds, "'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '            "A grafted plant is two plants joined: the root system of a variety that resists a soil "',
     '            "A grafted plant is two plants joined — the root system of a variety that resists a soil "'),
    ("mechanics: the beginner register falls back on jargon", "mechanics", CONTENT,
     '            "A grafted plant is two plants joined: the root system of a variety that resists a soil "',
     '            "A grafted plant carries a scion above the graft union: the root system of a variety that resists a soil "'),
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
    wd = tempfile.mkdtemp(prefix="mutate_cr3_")
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
    print("MUTATION HARNESS -- PLA-8 catalog r3 (four mints)")
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
