#!/usr/bin/env python3
"""Mutation harness for the calcium-disorder methods (PLA-215).

The DISTINCTNESS family is the reason this promote exists and therefore the family that most needs
proving. These two methods were split out precisely because widening the originals would have
shipped prose about aphids on a blossom-end-rot ladder. If the distinctness guards are vacuous, the
split bought nothing and a later edit could drift the copy straight back.

LIVENESS DEFENSE: positive control, sentinel, MUTATION-APPLIED marker, anchor-uniqueness asserted.
"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_ber_methods.py")
PROMOTE = os.path.join(HERE, "promote_pla8_ber_methods.py")
CONTENT = os.path.join(HERE, "build_ber_methods_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("distinctness: the nitrogen method drifts back to aphid copy", "distinctness", CONTENT,
     '"Cation competition at the root surface, not a soil calcium shortage: ammonium, "',
     '"The soft sappy growth too much nitrogen pushes out is what aphids multiply on: ammonium, "'),
    ("distinctness: the mulch method drifts back to strawberry copy", "distinctness", CONTENT,
     '"A moisture buffer, not a splash barrier. Calcium moves with water, so the disorder "',
     '"Straw keeps ripening berries up off wet soil and cuts gray mold. Calcium moves with water, so the disorder "'),
    ("distinctness: the straw_mulch contrast is deleted", "distinctness", CONTENT,
     '"Distinct from the straw mulch used under strawberries, which is a splash and contact "', '"Also good. "'),
    ("distinctness: the balance_nitrogen contrast is deleted", "distinctness", CONTENT,
     '"lever from balancing nitrogen for soft growth, which is about the flush of tender "', '"lever. "'),
    ("distinctness: the mulch method loses its own mechanism", "distinctness", CONTENT,
     '"swings are what interrupt the flow of calcium into developing fruit, which is what "',
     '"swings are generally not ideal, which is what "'),
    ("scope: a third method is appended", "scope", CONTENT,
     'def main():', 'NEW_METHODS["ghost"] = dict(NEW_METHODS["moisture_buffering_mulch"])\n\n\ndef main():'),
    ("shape: a required key is dropped", "shape", CONTENT,
     '"find_it_beginner": (\n            "Straw, shredded leaves, or compost. Anything that holds a loose layer without matting "', '"unused_key": (\n            "x"'),
    ("shape: an invented tier", "shape", CONTENT,
     '"name": "Mulch to steady soil moisture",\n        "tier": "cultural",',
     '"name": "Mulch to steady soil moisture",\n        "tier": "horticultural",'),
    ("sourcing: the anchor points at the wrong document", "sourcing", CONTENT,
     'https://hgic.clemson.edu/factsheet/tomato-diseases-disorders/',
     'https://hgic.clemson.edu/factsheet/strawberry-diseases/'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '"stop disease; it is there to stop the soil swinging between soaked and bone dry. Those "',
     '"stop disease — it is there to stop the soil swinging between soaked and bone dry. Those "'),
    ("mechanics: an absolute enters consumer copy", "mechanics", CONTENT,
     '"Costs nothing, since it is a choice between products you were buying anyway",',
     '"Costs nothing and completely prevents the disorder",'),
    ("blast: a crop is touched", "blast", PROMOTE,
     '    data["control_methods"].update(json.loads(json.dumps(content())))',
     '    data["crops"][0]["name"] = "MUTATED"\n    data["control_methods"].update(json.loads(json.dumps(content())))'),
    ("blast: an existing method is edited", "blast", PROMOTE,
     '    return len(content())',
     '    data["control_methods"]["even_watering"]["applies_to"].append("viral")\n    return len(content())'),
    ("refusal: the already-exists check is disabled", "refusal", PROMOTE,
     '        if k in cm:\n            return f"control_methods.{k} already exists; this promote creates it"',
     '        if False:\n            return ""'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]
SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE, "def apply_to(data):", "def apply_to(data):\n    return 0")

def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0

def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_ber_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\nsys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            n = s.count(old)
            if n != 1:
                shutil.rmtree(wd); raise SystemExit(f"HARNESS DEAD: anchor matches {n}x in {os.path.basename(f)}: {old[:60]!r}")
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd); raise SystemExit("HARNESS DEAD: marker absent")
    return wd

def preflight():
    """Validate EVERY anchor before running any mutation.

    Three anchors in this harness' first draft spanned a Python implicit line continuation, so the
    literal never appeared in the source. Discovering that one mutation at a time wastes a full
    suite run each time AND leaves a partial total on screen that looks like a result. An anchor
    that matches twice is worse still: it edits a site you did not intend and reports a catch for
    the wrong reason. Both are caught here, before anything is graded."""
    bad = []
    for label, _fam, f, old, _new in MUTATIONS + [(SENTINEL[0], "sentinel", SENTINEL[1], SENTINEL[2], SENTINEL[3])]:
        n = open(f).read().count(old)
        if n != 1:
            bad.append(f"  {n}x  [{os.path.basename(f)}] {label}\n        anchor: {old[:78]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(MUTATIONS)+1} anchors match exactly once")
    return True


def main():
    print("="*78); print("MUTATION HARNESS -- calcium-disorder methods"); print("="*78)
    if not preflight(): return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok: print("HARNESS DEAD: POSITIVE CONTROL fails."); return 1
    print("positive control : GREEN\n")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok: print(f"HARNESS DEAD: {label} SURVIVED."); return 1
    print(f"sentinel         : RED as required\n")
    caught = survived = 0; fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0,0])
        if ok: survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:  caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")
    print("\n" + "-"*78)
    for k in sorted(fam):
        c,s = fam[k]; print(f"  {k:13s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-"*78); print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived: print("\nRESULT: FAIL"); return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous."); return 0

if __name__ == "__main__":
    sys.exit(main())
