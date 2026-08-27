#!/usr/bin/env python3
"""Mutation harness for the chemical-cohort close-out round (PLA-215).

This promote corrects a false safety rating that is live in a shipped consumer rung, so the
`rating` family is the load-bearing one: the scan that finds "low toxicity to bees" on a
medium-band method is disabled, degraded to never-match, unscoped, and stripped of its premise
drivers, and each must redden the suite. The `split` family attacks the copper acute caution the
same two ways the pyrethroid one was attacked: SIDE (a compound moved to the wrong rating) and
BOUNDARY (`named()` degraded to containment). `preserve`, `kept`, `blast`, `source`, `hygiene`,
`rung` and `mechanics` cover the rest.

The per-method disclosure AXES of this round live as frozen literals in the TEST file, not as
promote code, so there is no promote-side axis loop to disable; their vacuity protection is the
literal itself.

VerifyPostIsDriven was written FIRST this round (the conventional harness's twelve first-run
survivors were eight undriven verify_post guards), so every post-side mutation below has a driver
that doctors the applied post directly.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_chem_cohort.py")
PROMOTE = os.path.join(HERE, "promote_pla8_chem_cohort.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- band ----------------------------------------------------------------------------------
    ("band: band_violation is disabled in check", "band", PROMOTE,
     '        problem = band_violation(key, want)\n        if problem:',
     '        problem = None\n        if problem:'),
    ("band: band_violation is disabled in verify_post", "band", PROMOTE,
     '        problem = band_violation(key, m.get("cautions") or [])\n        if problem:',
     '        problem = None\n        if problem:'),
    ("band: the AUTHORED_BEE list is emptied", "band", PROMOTE,
     'AUTHORED_BEE = ("neem_oil", "horticultural_oil")',
     'AUTHORED_BEE = ()'),
    ("band: the sunset-to-midnight requirement is dropped", "band", PROMOTE,
     '    if "sunset" not in blob or "midnight" not in blob:',
     '    if False:'),
    ("band: the missing-bee-caution refusal is disabled", "band", PROMOTE,
     '    if not bee:\n        return f"{key}: no caution mentions flowering plants, so the bee band is unstated"',
     '    if not bee:\n        return None'),

    # ---- rating: the defect family --------------------------------------------------------------
    ("rating: the post-state scan is disabled in verify_post", "rating", PROMOTE,
     '        problem = false_rating_violation(key, m)\n        if problem:',
     '        problem = None\n        if problem:'),
    ("rating: the scan pattern never matches", "rating", PROMOTE,
     'FALSE_RATING = re.compile(r"low (?:in )?toxicity to (?:bees|[a-z,\' ]*pollinators)", re.I)',
     'FALSE_RATING = re.compile(r"(?!x)x")'),
    ("rating: the copy-field list is emptied", "rating", PROMOTE,
     'COPY_FIELDS = ("cautions", "pros", "cons", "how_it_works_beginner", "how_it_works_seasoned",\n'
     '               "best_use", "find_it_beginner")',
     'COPY_FIELDS = ()'),
    ("rating: the scan stops being scoped to medium-band methods and fires for nobody", "rating", PROMOTE,
     '    if BAND_OF.get(key) != "medium":\n        return None',
     '    if True:\n        return None'),
    ("rating: the caution-defect premise is disabled", "rating", PROMOTE,
     '    if not any(DEFECTS["neem_oil/cautions"] in c for c in cm["neem_oil"].get("cautions") or []):',
     '    if False:'),
    ("rating: the rung pre-state premise is disabled", "rating", PROMOTE,
     '    if rung.get(RUNG["register"]) != RUNG["old"]:',
     '    if False:'),
    ("rating: the residual strawberry scan is disabled in verify_post", "rating", PROMOTE,
     '    if FALSE_RATING.search(json.dumps(post["crops"][RUNG["crop"]], ensure_ascii=False)):',
     '    if False:'),
    ("rating: the authored rung may keep the claim", "rating", PROMOTE,
     '    if FALSE_RATING.search(RUNG["new"]):',
     '    if False:'),

    # ---- split ----------------------------------------------------------------------------------
    ("split: split_violation is disabled in check", "split", PROMOTE,
     '    problem = split_violation(CAUTIONS["copper_fungicide"])\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),
    ("split: split_violation is disabled in verify_post", "split", PROMOTE,
     '        if key == "copper_fungicide":\n            problem = split_violation(m.get("cautions") or [])',
     '        if False:\n            problem = split_violation(m.get("cautions") or [])'),
    ("split: named() degrades to naive containment", "split", PROMOTE,
     '    return re.search(rf"(?<![-\\w]){re.escape(name)}(?![-\\w])", blob, re.I) is not None',
     '    return name.lower() in blob.lower()'),
    ("split: the ACUTE_SIDES table is emptied", "split", PROMOTE,
     'ACUTE_SIDES = {\n    "L": ("copper octanoate", "copper ammonium complex"),',
     'ACUTE_SIDES = {} or {\n    "_L": ("copper octanoate", "copper ammonium complex"),'),
    ("split: a compound may be named on two sides", "split", PROMOTE,
     '            for other, blob in sides.items():\n                if other != rating and named(n, blob):',
     '            for other, blob in sides.items():\n                if False:'),
    ("split: the chronic-absence disclosure stops being required", "split", PROMOTE,
     '    if "none of the four" not in low or "prop 65" not in low or "us epa" not in low:',
     '    if False:'),
    ("split: the one-acute-caution requirement is dropped", "split", PROMOTE,
     '    if len(hits) != 1:',
     '    if False:'),

    # ---- preserve --------------------------------------------------------------------------------
    ("preserve: the PRESERVED table is emptied", "preserve", PROMOTE,
     'PRESERVED = {\n    "copper_fungicide": ("highly to very highly toxic to fish",',
     'PRESERVED = {} or {\n    "_copper_fungicide": ("highly to very highly toxic to fish",'),
    ("preserve: the dropped-claim refusal is disabled", "preserve", PROMOTE,
     '            if not any(claim in c for c in field):',
     '            if False:'),
    ("preserve: the back-door guard is disabled", "preserve", PROMOTE,
     '            if not any(claim in c for c in pre_field):',
     '            if False:'),
    ("preserve: verify_post stops freezing the non-mutable fields", "preserve", PROMOTE,
     "            if m.get(f) != v:\n                return f\"post-state {key}: field '{f}' changed and it was not supposed to\"",
     "            if False:\n                return f\"post-state {key}: field '{f}' changed and it was not supposed to\""),
    ("preserve: verify_post stops comparing the field set", "preserve", PROMOTE,
     '        if set(m) != set(pre["methods"][key]):',
     '        if False:'),
    ("preserve: verify_post stops checking the cautions actually authored", "preserve", PROMOTE,
     '        if m.get("cautions") != list(CAUTIONS[key]):',
     '        if False:'),
    ("preserve: verify_post stops checking the pros actually authored", "preserve", PROMOTE,
     '        if key in PROS and m.get("pros") != list(PROS[key]):',
     '        if False:'),

    # ---- kept ------------------------------------------------------------------------------------
    ("kept: the KEPT_PINS table is emptied", "kept", PROMOTE,
     'KEPT_PINS = {\n    "sulfur": "Can harm released predatory (beneficial) mites",',
     'KEPT_PINS = {} or {\n    "_sulfur": "Can harm released predatory (beneficial) mites",'),
    ("kept: the byte-identical check on kept methods is disabled", "kept", PROMOTE,
     '    for key in KEPT:\n        if post["methods"][key] != pre["methods"][key]:',
     '    for key in ():\n        if post["methods"][key] != pre["methods"][key]:'),

    # ---- blast -----------------------------------------------------------------------------------
    ("blast: the crop roster set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):',
     '    if False:'),
    ("blast: the method roster set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):',
     '    if False:'),
    ("blast: the source roster set comparison is disabled", "blast", PROMOTE,
     '    if set(post["sources"]) != set(pre["sources"]):',
     '    if False:'),
    ("blast: the source byte comparison is disabled", "blast", PROMOTE,
     '    for sid, before in pre["sources"].items():\n        if post["sources"][sid] != before:',
     '    for sid, before in pre["sources"].items():\n        if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if slug != RUNG["crop"] and post["crops"][slug] != before:',
     '        if False:'),
    ("blast: bystander methods stop being compared", "blast", PROMOTE,
     '        if key not in COHORT and post["methods"][key] != before:',
     '        if False:'),
    ("blast: the beyond-the-rung comparison is disabled", "blast", PROMOTE,
     '    if reverted != pre["crops"][RUNG["crop"]]:',
     '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    for key, cautions in CAUTIONS.items():',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    for key, cautions in CAUTIONS.items():'),

    # ---- source ----------------------------------------------------------------------------------
    ("source: the ucipm_uaidb-present premise is disabled", "source", PROMOTE,
     '    if SOURCE_ID not in sc:',
     '    if False:'),
    ("source: the second-run refusal is disabled", "source", PROMOTE,
     '        if SOURCE_ID in (cm[key].get("sources") or []):',
     '        if False:'),
    ("source: verify_post stops requiring anchors to match sources", "source", PROMOTE,
     '        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):',
     '        if False:'),
    ("source: verify_post stops checking the anchor points at its own page", "source", PROMOTE,
     '        if (m.get("anchoring_urls") or {}).get(SOURCE_ID, {}).get("url") != DETAIL % ANCHOR_KEY[key]:',
     '        if False:'),
    ("source: every method anchors the same ingredient page", "source", PROMOTE,
     'ANCHOR_KEY = {"copper_fungicide": "125", "neem_oil": "38", "insecticidal_soap": "50",\n'
     '              "horticultural_oil": "142"}',
     'ANCHOR_KEY = {"copper_fungicide": "115", "neem_oil": "115", "insecticidal_soap": "115",\n'
     '              "horticultural_oil": "115"}'),

    # ---- rung ------------------------------------------------------------------------------------
    ("rung: the landing check is disabled in verify_post", "rung", PROMOTE,
     '    if rung.get(RUNG["register"]) != RUNG["new"]:',
     '    if False:'),
    ("rung: find_rung stops requiring exactly one matching rung", "rung", PROMOTE,
     '    if len(rungs) != 1:',
     '    if False:'),

    # ---- hygiene / mechanics ---------------------------------------------------------------------
    ("hygiene: the caution sweep runs over nothing", "hygiene", PROMOTE,
     '        for c in want:\n            h = hygiene(c)',
     '        for c in ():\n            h = hygiene(c)'),
    ("hygiene: the absolutes family leaves the check", "hygiene", PROMOTE,
     '    for a in ABSOLUTES:\n        if a in s.lower():',
     '    for a in ():\n        if a in s.lower():'),
    ("hygiene: the rung hygiene check is disabled", "hygiene", PROMOTE,
     '    h = hygiene(RUNG["new"])\n    if h:',
     '    h = hygiene(RUNG["new"])\n    if False:'),
    ("hygiene: the dash check is disabled", "hygiene", PROMOTE,
     '    if "—" in s or "–" in s:',
     '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to stops writing the cautions", PROMOTE,
            '    for key, cautions in CAUTIONS.items():\n        m = data["control_methods"][key]',
            '    for key, cautions in {}.items():\n        m = data["control_methods"][key]')


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
            bad.append(f"  {n}x  {label}\n        anchor: {old[:78]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_chemcohort_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read()
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- chemical-cohort close-out (4 methods, 3 kept, 1 rung)")
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
        print(f"  {k:11s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
