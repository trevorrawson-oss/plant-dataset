#!/usr/bin/env python3
"""Mutation harness for the slug-bait safety-absolute promote (PLA-215).

THE SAFETY family is why this promote exists. The defect was consumer copy asserting a pesticide IS
SAFE where the T1 source publishes only a comparative. If those guards are vacuous, the promote can
"fix" the wording while leaving the claim, or strip the sentence and leave nothing, and both read as
a pass. So the safety mutations attack both halves of the specification separately: revert the
absolute, and hollow out the comparative that replaced it.

THE SCOPE family is the unusual one and guards the opposite failure. The Bt absolute on nine other
crops shares the phrase "which is safe". It is real, recorded, and NOT this promote's job. A guard
asserting we did NOT touch it is only worth having if a mutation proves it would notice, so two
mutations here sweep in out-of-scope crops and must be caught.

Includes the anchor PREFLIGHT: every anchor is validated to match exactly once before anything is
graded. `arugula` and `bok-choy` carry BYTE-IDENTICAL prose, so several otherwise-obvious anchors
appear twice in the content module and would silently mutate the wrong crop.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_slug_bait_safety.py")
PROMOTE = os.path.join(HERE, "promote_pla8_slug_bait_safety.py")
CONTENT = os.path.join(HERE, "build_slug_bait_safety_content.py")
MARKER = "# MUTATION-APPLIED"

CONTENT_FN = "    return B.EDITS, B.BANNED, B.REQUIRED_COMPARATIVE"
APPLY_HEAD = "    edits, _banned, _req = content()\n    n = 0"

MUTATIONS = [
    # ---- safety: the absolute comes back -------------------------------------------------
    ("safety: sage reverts to 'pet-safe bait'", "safety", CONTENT,
     '        "iron-phosphate bait, which carries less risk around pets than the older metaldehyde "',
     '        "pet-safe bait, which is fine to use "'),
    ("safety: swiss-chard says the bait IS safe", "safety", CONTENT,
     '        "scatter an iron-phosphate slug bait, which carries less risk around pets and wildlife than "',
     '        "scatter an iron-phosphate slug bait, which is safe around pets and wildlife and not "'),
    # ---- safety: the comparative is hollowed out ------------------------------------------
    ("safety: basil keeps the hedge but loses the comparative entirely", "safety", CONTENT,
     '        "gardens and carry less risk around pets and wildlife than the older metaldehyde baits, "',
     '        "gardens, "'),
    ("safety: lettuce seasoned becomes a bare reassurance with nothing to compare to", "safety", CONTENT,
     '        "(sold as Sluggo and similar) is approved for organic use and is safer around children, "',
     '        "(sold as Sluggo and similar) is approved for organic use and is gentler on children, "'),
    # ---- coverage: an affected field is dropped from the edit list -------------------------
    ("coverage: the sage field the scan missed is dropped again", "coverage", PROMOTE,
     CONTENT_FN,
     "    return B.EDITS[:-1], B.BANNED, B.REQUIRED_COMPARATIVE"),
    ("coverage: lettuce-leaf seasoned is dropped", "coverage", PROMOTE,
     CONTENT_FN,
     '    return ([e for e in B.EDITS if not (e[0] == "lettuce-leaf" and\n'
     '            e[2] == "organic_treatment_seasoned")], B.BANNED, B.REQUIRED_COMPARATIVE)'),
    ("coverage: only the two fields that originally surfaced are fixed", "coverage", PROMOTE,
     CONTENT_FN,
     '    return ([e for e in B.EDITS if e[0] in ("basil", "swiss-chard")],\n'
     '            B.BANNED, B.REQUIRED_COMPARATIVE)'),
    # ---- scope: out-of-scope classes get swept in ------------------------------------------
    ("scope: the Bt absolute is silently swept in on kale", "scope", PROMOTE,
     APPLY_HEAD,
     '    edits, _banned, _req = content()\n'
     '    for _c in data["crops"]:\n'
     '        if _c.get("slug") == "kale":\n'
     '            for _f in ("pests", "diseases"):\n'
     '                for _p in _c.get(_f) or []:\n'
     '                    for _k, _v in list(_p.items()):\n'
     '                        if isinstance(_v, str) and "which is safe" in _v:\n'
     '                            _p[_k] = _v.replace("which is safe", "which is lower risk")\n'
     '    n = 0'),
    ("scope: the correctly-negated cayenne hedge is rewritten", "scope", PROMOTE,
     APPLY_HEAD,
     '    edits, _banned, _req = content()\n'
     '    for _c in data["crops"]:\n'
     '        if _c.get("slug") == "cayenne-pepper":\n'
     '            for _f in ("pests", "diseases"):\n'
     '                for _p in _c.get(_f) or []:\n'
     '                    for _k, _v in list(_p.items()):\n'
     '                        if isinstance(_v, str) and "not completely safe" in _v:\n'
     '                            _p[_k] = _v.replace("not completely safe", "not fully protected")\n'
     '    n = 0'),
    # ---- blast radius ----------------------------------------------------------------------
    ("blast: an unrelated crop is touched", "blast", PROMOTE,
     APPLY_HEAD,
     '    edits, _banned, _req = content()\n    data["crops"][0]["name"] = "MUTATED"\n    n = 0'),
    ("blast: a control_method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     '    edits, _banned, _req = content()\n'
     '    data["control_methods"]["handpick"]["applies_to"].append("viral")\n    n = 0'),
    ("blast: a problem's control_ladder is edited", "blast", PROMOTE,
     APPLY_HEAD,
     '    edits, _banned, _req = content()\n'
     '    for _c in data["crops"]:\n'
     '        for _f in ("pests", "diseases"):\n'
     '            for _p in _c.get(_f) or []:\n'
     '                if isinstance(_p, dict) and _p.get("control_ladder"):\n'
     '                    _p["control_ladder"] = _p["control_ladder"][:-1]\n'
     '    n = 0'),
    # ---- mechanics --------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '        "gardens and carries less risk around pets and wildlife than the older metaldehyde baits, "',
     '        "gardens and carries less risk around pets and wildlife \u2014 unlike metaldehyde baits, "'),
    ("mechanics: a British spelling enters consumer copy", "mechanics", CONTENT,
     '        "pets, birds, fish, and other wildlife than metaldehyde, though it remains a pesticide; it "',
     '        "pets, birds, fish, and wildlife of every colour than metaldehyde, though a pesticide; it "'),
    # ---- the recorded source read -----------------------------------------------------------
    ("record: the source quote is rewritten to support the absolute", "record", CONTENT,
     '    "quote": "have the advantage of being safer for use around children, domestic animals, "',
     '    "quote": "have the advantage of being safe for use around children, domestic animals, "'),
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
    wd = tempfile.mkdtemp(prefix="mutate_sbs_")
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
    print("MUTATION HARNESS -- iron-phosphate slug-bait safety absolute")
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
