#!/usr/bin/env python3
"""Mutation harness for the PLA-8 best_use widening promote (PLA-215).

THE `leftalone` FAMILY IS LOAD-BEARING. The detector flagged 11 methods; the READ spared one.
`bottom_watering`'s best_use already names both its shipped problems and confines the method to
indoor trays and seedlings, and that confinement IS the field's job: `bottom_watering` means water
from below in trays, and twelve authored rungs in batch 1 used it to mean water at the base
outdoors. If a promote can quietly widen or loosen it, this pass re-opens the worst defect the
rollout has produced while reporting success.

THE `content` FAMILY pins each widening to the specific gap it was written to close, so a future
edit cannot reflow the prose and silently drop the reason the string changed at all. The
off_season_tillage pair is a factual correction, not a widening: it named a life stage European corn
borer does not have.

`hygiene` mutations matter more here than in a data promote, because best_use RENDERS. A hygiene
function that quietly returns None is a copy gate that reports success without checking anything.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_bestuse.py")
PROMOTE = os.path.join(HERE, "promote_pla8_bestuse.py")
CONTENT = os.path.join(HERE, "build_pla8_bestuse_content.py")
MARKER = "# MUTATION-APPLIED"

APPLY = "def apply_to(data):\n    C = content()\n    return C.apply_widenings(data[\"control_methods\"])"

MUTATIONS = [
    # ---- leftalone: the method the read spared -------------------------------------------------
    ("leftalone: bottom_watering gets widened too", "leftalone", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    data[\"control_methods\"][\"bottom_watering\"][\"best_use\"] = (\n"
      "        \"Any bed or tray where a damp surface drives damping-off or fungus gnats.\")\n"
      "    return C.apply_widenings")),
    ("leftalone: bottom_watering loses its 'trays' confinement", "leftalone", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    _m = data[\"control_methods\"][\"bottom_watering\"]\n"
      "    _m[\"best_use\"] = _m[\"best_use\"].replace(\"Indoor trays and seedlings, especially \", \"\")\n"
      "    return C.apply_widenings")),
    ("leftalone: water_at_the_base loses its disambiguation from bottom watering", "leftalone",
     PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    _m = data[\"control_methods\"][\"water_at_the_base\"]\n"
      "    _m[\"best_use\"] = _m[\"best_use\"].split(\". Distinct\")[0] + \".\"\n"
      "    return C.apply_widenings")),
    ("leftalone: the EXCLUDED/WIDENINGS overlap check is disabled", "leftalone", PROMOTE,
     '        if key in C.WIDENINGS:\n            return f"{key} is in BOTH EXCLUDED and WIDENINGS"',
     '        if False and key in C.WIDENINGS:\n            return f"{key} is in BOTH EXCLUDED and WIDENINGS"'),

    # ---- scope: exactly 10 strings, one field, zero crops --------------------------------------
    ("scope: a second field on a widened method is edited", "scope", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    data[\"control_methods\"][\"handpick\"][\"tier\"] = \"physical \"\n"
      "    return C.apply_widenings")),
    ("scope: a crop is touched", "scope", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    data[\"crops\"][0][\"name\"] = \"MUTATED\"\n"
      "    return C.apply_widenings")),
    ("scope: a method OUTSIDE the widening set is edited", "scope", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    data[\"control_methods\"][\"sulfur\"][\"best_use\"] += \" Also good on rust.\"\n"
      "    return C.apply_widenings")),
    ("scope: source_catalog is edited", "scope", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    data[\"source_catalog\"][\"umn_ext\"][\"name\"] = \"MUTATED\"\n"
      "    return C.apply_widenings")),
    ("scope: a shipped ladder rung is dropped", "scope", PROMOTE, APPLY,
     APPLY.replace("    return C.apply_widenings", "    for _c in data[\"crops\"]:\n"
      "        for _f in (\"pests\", \"diseases\"):\n"
      "            for _p in (_c.get(_f) or []):\n"
      "                if isinstance(_p, dict) and _p.get(\"control_ladder\"):\n"
      "                    _p[\"control_ladder\"].pop(); return C.apply_widenings(data[\"control_methods\"])\n"
      "    return C.apply_widenings")),

    # ---- content: each widening pinned to the gap it closes ------------------------------------
    ("content: off_season_tillage keeps the wrong 'soil-pupating' mechanism", "content", CONTENT,
     '"new": "A finished bed that carried a pest which stays put over the winter, worked once "',
     '"new": "A finished bed that carried a soil-pupating caterpillar, worked once "'),
    ("content: off_season_tillage loses its garden_sanitation disambiguation", "content", CONTENT,
     '               "turning the stalks under is what reaches them. Distinct from garden sanitation, "\n'
     '               "which clears the surface rather than breaking up what sits in it.",',
     '               "turning the stalks under is what reaches them.",'),
    ("content: resistant_varieties reverts to disease-only", "content", CONTENT,
     '               "black rot, but it also covers varieties a pest is less drawn to, like a tight corn "\n'
     '               "husk against earworm. The natural handoff to variety-level resistance data.",',
     '               "black rot. The natural handoff to variety-level resistance data.",'),
    ("content: floating_row_cover loses the vector-exclusion case", "content", CONTENT,
     '               "against a disease with no cure once it arrives, such as bacterial wilt, where "\n'
     '               "keeping the carrier insect off young plants is the lever that works. Remove for "\n'
     '               "pollination if the crop needs it.",',
     '               "Remove for pollination if the crop needs it.",'),
    ("content: even_watering loses the mite case", "content", CONTENT,
     '               "roughly 1 to 2 inches per week on shallow-rooted crops, and it holds spider mites "\n'
     '               "down too, since they build up fastest on plants that have been left dry and "\n'
     '               "stressed.",',
     '               "roughly 1 to 2 inches per week on shallow-rooted crops.",'),
    ("content: bt loses the non-target butterfly caveat", "content", CONTENT,
     '               "after rain or new growth. It acts on caterpillars as a group, so keep it off "\n'
     '               "plants you are growing for butterflies.",',
     '               "after rain or new growth.",'),
    ("content: balance_nitrogen keeps the crop restriction", "content", CONTENT,
     '        "new": "A preventive feeding habit anywhere aphids and other soft-bodied sap-suckers turn "\n'
     '               "up most years. Heavy nitrogen pushes out the soft new growth they multiply on, "\n'
     '               "whatever the crop.",',
     '        "new": "A preventive feeding habit for aphids and other soft-bodied sap-suckers on leafy "\n'
     '               "and cole crops, plus a note.",'),

    # ---- hygiene: the copy gate itself ---------------------------------------------------------
    ("hygiene: the function always returns None", "hygiene", PROMOTE,
     'def hygiene(s):\n    """Consumer-copy rules; best_use renders in MethodSheet.tsx. Returns a reason or None."""',
     'def hygiene(s):\n    """Consumer-copy rules; best_use renders in MethodSheet.tsx. Returns a reason or None."""\n    return None'),
    ("hygiene: the absolute-claim rule is disabled", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     '    if False:'),
    ("hygiene: the bare-safety-claim rule is disabled", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:is|are)\\s+safe\\b", s, re.I):',
     '    if False:'),
    ("hygiene: it is never called from check()", "hygiene", PROMOTE,
     '        bad = hygiene(w["new"])',
     '        bad = None'),

    # ---- refusal -------------------------------------------------------------------------------
    ("refusal: the already-widened check is disabled", "refusal", PROMOTE,
     '        if cur == w["new"]:\n            return f"{key}: already widened"',
     '        if False:\n            return f"{key}: already widened"'),
    ("refusal: the drifted-text check is disabled", "refusal", PROMOTE,
     '        if cur != w["old"]:\n            return (f"{key}: best_use is not the expected text, so it changed under this pass. "',
     '        if False:\n            return (f"{key}: best_use is not the expected text, so it changed under this pass. "'),
    ("refusal: apply_widenings overwrites instead of refusing on drift", "refusal", CONTENT,
     '        if cur != w["old"]:\n            raise AssertionError(',
     '        if False:\n            raise AssertionError('),
    ("refusal: the widening COUNT is not enforced", "refusal", PROMOTE,
     '    if len(C.WIDENINGS) != 10:',
     '    if False and len(C.WIDENINGS) != 10:'),

    # ---- mechanics -----------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: a widening is reflowed to be SHORTER than the original", "mechanics", CONTENT,
     '        "new": "Low to moderate numbers of anything big enough to spot and slow enough to catch, on "\n'
     '               "a regular scouting routine: cabbageworms, cutworms, beetles, squash bugs, slugs and "\n'
     '               "snails. Best in a small garden where you walk the rows anyway.",',
     '        "new": "Handpick visible pests.",'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE, APPLY,
            "def apply_to(data):\n    return 0")


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
    wd = tempfile.mkdtemp(prefix="mutate_bu_")
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
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 best_use widening (10 widened, 1 deliberately spared)")
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
