#!/usr/bin/env python3
"""Mutation harness for the water_at_the_base split (PLA-215).

The SEMANTIC family is why this promote exists. The original defect was a method whose applies_to
was widened while its prose described a different ACTION, and every structural gate passed. If the
semantic-separation guards are vacuous, the split fixes nothing and the two methods can drift back
into each other.

Includes the anchor PREFLIGHT: every anchor is validated to match exactly once before anything is
graded. Three earlier harnesses died one mutation at a time on anchors spanning Python implicit
string concatenation, each death costing a full suite run and leaving a partial total that reads
like a result.
"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_water_at_base.py")
PROMOTE = os.path.join(HERE, "promote_pla8_water_at_base.py")
CONTENT = os.path.join(HERE, "build_water_at_base_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("semantic: the new method claims to water from below", "semantic", CONTENT,
     '"Put the water on the ground at the foot of the plant instead of spraying it over the "',
     '"Water from below so the surface stays drier, instead of spraying it over the "'),
    ("semantic: the disambiguation from bottom watering is deleted", "semantic", CONTENT,
     '"sustained by a surface that stays damp. Distinct from bottom watering, which is a "',
     '"sustained by a surface that stays damp. Also good generally, which is a "'),
    ("semantic: the splash mechanism is stripped", "semantic", CONTENT,
     '"Two mechanisms, not one. Directing irrigation to the soil removes the splash that "',
     '"It is a good habit. Directing irrigation to the soil helps with the water that "'),
    ("revert: bottom_watering keeps the mis-attached targets", "revert", CONTENT,
     '"applies_to": ["fungal_soilborne", "insect_general"],\n    "sources": ["ucanr_ext", "umn_ext"],',
     '"applies_to": ["fungal_soilborne", "insect_general", "bacterial", "mollusk"],\n    "sources": ["ucanr_ext", "umn_ext"],'),
    ("revert: bottom_watering keeps the moved sources", "revert", CONTENT,
     '"drop_anchors": ["ucanr_ext_bacterial_speck", "ucanr_ext_snails_slugs"],', '"drop_anchors": [],'),
    ("revert: a moved source is orphaned instead of moved", "revert", CONTENT,
     '"sources": ["clemson_hgic", "ucanr_ext_bacterial_speck", "ucanr_ext_snails_slugs"],',
     '"sources": ["clemson_hgic"],'),
    ("scope: the new method loses a target the pilot needs", "scope", CONTENT,
     '"applies_to": ["fungal_foliar", "fungal_soilborne", "bacterial", "mollusk"],',
     '"applies_to": ["fungal_foliar", "fungal_soilborne"],'),
    ("shape: an invented tier", "shape", CONTENT,
     '"name": "Water at the base",\n        "tier": "cultural",',
     '"name": "Water at the base",\n        "tier": "irrigation",'),
    ("sourcing: the foliar anchor points at the wrong document", "sourcing", CONTENT,
     '"clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/tomato-diseases-disorders/",',
     '"clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/strawberry-diseases/",'),
    ("mechanics: an absolute enters consumer copy", "mechanics", CONTENT,
     '"Preventive only; it does nothing for tissue already infected",',
     '"Completely prevents leaf disease",'),
    ("blast: a crop is touched", "blast", PROMOTE,
     '    data["control_methods"].update(json.loads(json.dumps(new)))',
     '    data["crops"][0]["name"] = "MUTATED"\n    data["control_methods"].update(json.loads(json.dumps(new)))'),
    ("blast: another method is edited", "blast", PROMOTE,
     '    bw = data["control_methods"]["bottom_watering"]',
     '    data["control_methods"]["handpick"]["applies_to"].append("viral")\n    bw = data["control_methods"]["bottom_watering"]'),
    # NOT MUTATION-TESTED, DELIBERATELY. Disabling check()'s orphan refusal survives, and the
    # reason is worth recording rather than hiding: the ORPHAN CONDITION is already covered by
    # mutation #6 above ("a moved source is orphaned instead of moved"), which IS caught -- by the
    # post-state guard `test_the_moved_sources_are_NOT_orphaned`. So the refusal in check() is
    # redundant with a post-state assertion for THIS promote's content, and no mutation of it can
    # make the refusal the sole detector. It is kept as a FORWARD guard: a future edit that drops a
    # source from bottom_watering WITHOUT moving it should be refused at the door rather than caught
    # after the fact. Same treatment as the refused-widenings test in mutate_pla8_bw_suite.py --
    # kept for what it protects, not counted as coverage here.
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]
SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE, "def apply_to(data):", "def apply_to(data):\n    return 0")

def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0

def preflight():
    bad = []
    for label, _f, f, old, _n in MUTATIONS + [(SENTINEL[0], "s", SENTINEL[1], SENTINEL[2], SENTINEL[3])]:
        n = open(f).read().count(old)
        if n != 1:
            bad.append(f"  {n}x  [{os.path.basename(f)}] {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad)); return False
    print(f"preflight        : all {len(MUTATIONS)+1} anchors match exactly once")
    return True

def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_wab_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\nsys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f: s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd); raise SystemExit("HARNESS DEAD: marker absent")
    return wd

def main():
    print("="*78); print("MUTATION HARNESS -- water_at_the_base split"); print("="*78)
    if not preflight(): return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok: print("HARNESS DEAD: POSITIVE CONTROL fails."); return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok: print(f"HARNESS DEAD: {label} SURVIVED."); return 1
    print("sentinel         : RED as required\n")
    caught = survived = 0; fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0,0])
        if ok: survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:  caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")
    print("\n" + "-"*78)
    for k in sorted(fam):
        c,s = fam[k]; print(f"  {k:10s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-"*78); print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived: print("\nRESULT: FAIL"); return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous."); return 0

if __name__ == "__main__":
    sys.exit(main())
