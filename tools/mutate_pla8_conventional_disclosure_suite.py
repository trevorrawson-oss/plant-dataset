#!/usr/bin/env python3
"""Mutation harness for the conventional-tier disclosure round (PLA-215).

THIS PROMOTE CHANGES SAFETY ADVICE THAT IS ALREADY LIVE ON TEN RUNGS ACROSS FOUR FOOD CROPS, so the
guards are load-bearing in a way a wording round's are not.

`band` attacks the defect itself: strict-band methods must be refused for GRANTING an evening window
and the middle-band method for LOSING one. A guard that only checked "some bee language is present"
was green through the entire defect, so these mutations disable each direction separately, empty the
token list, lie about which band a method sits in, and switch off the premise check that stops the
promote running against an already-fixed canonical.

`split` attacks the pyrethroid chronic caution, whose two vacuity traps are SIDE and SUBSTRING. The
sharpest mutation in the file degrades `named()` to plain containment: `permethrin` is a substring of
`cypermethrin`, which is a substring of `zeta-cypermethrin`, so naive containment reports every one
present no matter which side it is on, and the whole split guard silently stops testing anything.

`preserve` attacks the claims NOT being revalued, including the back-door guard: a claim asserted as
preserved that is absent from the pre-state must be refused, or the preservation list becomes a place
to smuggle new prose past review.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_conventional_disclosure.py")
PROMOTE = os.path.join(HERE, "promote_pla8_conventional_disclosure.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- band: the defect this promote exists to fix -------------------------------------------
    ("band: band_violation is disabled in check", "band", PROMOTE,
     '        problem = band_violation(key, want)\n        if problem:',
     '        problem = None\n        if problem:'),
    ("band: band_violation is disabled in verify_post", "band", PROMOTE,
     '        problem = band_violation(key, m.get("cautions") or [])\n        if problem:',
     '        problem = None\n        if problem:'),
    ("band: the window-token list is emptied", "band", PROMOTE,
     'WINDOW_TOKENS = ("sunset", "dusk", "evening", "at night", "early morning", "not foraging",\n'
     '                 "late even")',
     'WINDOW_TOKENS = ()'),
    ("band: the strict-band branch stops firing", "band", PROMOTE,
     '    if band == "high":\n        for t in WINDOW_TOKENS:', '    if False:\n        for t in WINDOW_TOKENS:'),
    ("band: the middle-band branch stops requiring a window", "band", PROMOTE,
     '        if "sunset" not in blob or "midnight" not in blob:', '        if False:'),
    ("band: the missing-bee-caution refusal is disabled", "band", PROMOTE,
     '    if not bee:\n        return f"{key}: no caution mentions flowering plants, so the bee band is unstated"',
     '    if not bee:\n        return None'),
    ("band: carbaryl is declared to sit in the permissive band", "band", PROMOTE,
     'BAND_OF = {"carbaryl": "high", "pyrethroid": "high", "chlorothalonil": "medium"}',
     'BAND_OF = {"carbaryl": "medium", "pyrethroid": "high", "chlorothalonil": "medium"}'),
    ("band: the premise check stops requiring the defect to be present", "band", PROMOTE,
     '    if not any(band_violation(k, cm[k].get("cautions") or []) for k in strict):',
     '    if False:'),

    ("band: the band check is moved back below the axis loop, so the axis answers first", "band", PROMOTE,
     '        problem = band_violation(key, want)\n        if problem:\n            return "authored cautions fail the band check: " + problem\n        for axis, tokens in DISCLOSURE_AXES.items():',
     '        for axis, tokens in DISCLOSURE_AXES.items():'),

    # ---- split: side and substring --------------------------------------------------------------
    ("split: split_violation is disabled in check", "split", PROMOTE,
     '    problem = split_violation(CAUTIONS["pyrethroid"])\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),
    ("split: split_violation is disabled in verify_post", "split", PROMOTE,
     '        if key == "pyrethroid":\n            problem = split_violation(m.get("cautions") or [])',
     '        if False:\n            problem = split_violation(m.get("cautions") or [])'),
    ("split: named() degrades to naive containment", "split", PROMOTE,
     '    return re.search(rf"(?<![-\\w]){re.escape(name)}\\b", blob, re.I) is not None',
     '    return name.lower() in blob.lower()'),
    ("split: the EPA side stops being checked for presence", "split", PROMOTE,
     '        if not named(n, epa_side):', '        if False:'),
    ("split: an EPA ingredient may also appear on the safe side", "split", PROMOTE,
     '        if named(n, nkr_side):\n            return f"pyrethroid: {n} is on the US EPA list but is named on the no-known-risk side"',
     '        if False:\n            return f"pyrethroid: {n} is on the US EPA list but is named on the no-known-risk side"'),
    ("split: the no-known-risk side stops being checked", "split", PROMOTE,
     '        if not named(n, nkr_side):', '        if False:'),
    ("split: the EPA_LISTED table is emptied", "split", PROMOTE,
     'EPA_LISTED = _pyr(5, "epa")', 'EPA_LISTED = ()'),
    ("split: the one-caution requirement is dropped", "split", PROMOTE,
     '    if len(hits) != 1:', '    if False:'),
    ("split: the acute-High ingredients need not be named", "split", PROMOTE,
     '    for n in ACUTE_HIGH:\n        if not named(n, " ".join(acute)):',
     '    for n in ():\n        if not named(n, " ".join(acute)):'),
    ("split: the acute check widens to ANY caution, making it dead code again", "split", PROMOTE,
     '    acute = [c for c in cautions if "acute toxicity" in c.lower()]',
     '    acute = list(cautions)'),
    ("split: the missing-acute-caution refusal is disabled", "split", PROMOTE,
     '    if not acute:\n        return "pyrethroid: no caution states acute toxicity"',
     '    if not acute:\n        return None'),

    # ---- disclosure ------------------------------------------------------------------------------
    ("disclosure: the axis table is emptied", "disclosure", PROMOTE,
     'DISCLOSURE_AXES = {\n    "bees":       ("flower",),', 'DISCLOSURE_AXES = {} or {\n    "_bees":       ("flower",),'),
    ("disclosure: the axis loop in check is disabled", "disclosure", PROMOTE,
     '        for axis, tokens in DISCLOSURE_AXES.items():\n            if not any(t in blob for t in tokens):\n                return f"{key}: the \'{axis}\' disclosure axis is missing from its cautions"',
     '        for axis, tokens in ():\n            if not any(t in blob for t in tokens):\n                return f"{key}: the \'{axis}\' disclosure axis is missing from its cautions"'),
    ("disclosure: the axis loop in verify_post is disabled", "disclosure", PROMOTE,
     '        for axis, tokens in DISCLOSURE_AXES.items():\n            if not any(t in blob for t in tokens):\n                return f"post-state {key}: the \'{axis}\' axis is missing"',
     '        for axis, tokens in ():\n            if not any(t in blob for t in tokens):\n                return f"post-state {key}: the \'{axis}\' axis is missing"'),
    ("disclosure: the duplicate-caution refusal is disabled", "disclosure", PROMOTE,
     '        if len(set(want)) != len(want):', '        if False:'),

    # ---- preserve ---------------------------------------------------------------------------------
    ("preserve: the PRESERVED table is emptied", "preserve", PROMOTE,
     'PRESERVED = {\n    "carbaryl": (', 'PRESERVED = {} or {\n    "_carbaryl": ('),
    ("preserve: the dropped-claim refusal is disabled", "preserve", PROMOTE,
     '            if not any(claim in c for c in want):', '            if False:'),
    ("preserve: the back-door guard is disabled", "preserve", PROMOTE,
     '            if not any(claim in c for c in (cm[key].get("cautions") or [])):', '            if False:'),
    ("preserve: verify_post stops freezing the non-mutable fields", "preserve", PROMOTE,
     '            if m.get(f) != v:\n                return f"post-state {key}: field \'{f}\' changed and it was not supposed to"',
     '            if False:\n                return f"post-state {key}: field \'{f}\' changed and it was not supposed to"'),
    ("preserve: verify_post stops comparing the field set", "preserve", PROMOTE,
     '        if set(m) != set(pre["methods"][key]):', '        if False:'),
    ("preserve: verify_post stops checking the cautions actually authored", "preserve", PROMOTE,
     '        if m.get("cautions") != list(CAUTIONS[key]):', '        if False:'),

    # ---- source ------------------------------------------------------------------------------------
    ("source: the required-field loop is disabled", "source", PROMOTE,
     '    for f in REQUIRED:\n        if not SOURCE.get(f):', '    for f in ():\n        if not SOURCE.get(f):'),
    ("source: the T1 requirement is dropped", "source", PROMOTE,
     '    if SOURCE["tier"] != "T1":', '    if False:'),
    ("source: the already-present refusal is disabled", "source", PROMOTE,
     '    if SOURCE_ID in sc:\n        return f"{SOURCE_ID} is already in source_catalog"',
     '    if SOURCE_ID in sc:\n        pass'),
    ("source: verify_post stops requiring the source to land verbatim", "source", PROMOTE,
     '    if post["sources"][SOURCE_ID] != SOURCE:', '    if False:'),
    ("source: verify_post stops requiring anchors to match sources", "source", PROMOTE,
     '        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):',
     '        if False:'),
    ("source: verify_post stops checking the anchor points at its own page", "source", PROMOTE,
     '        if (m.get("anchoring_urls") or {}).get(SOURCE_ID, {}).get("url") != DETAIL % ANCHOR_KEY[key]:',
     '        if False:'),
    ("source: every method anchors the same ingredient page", "source", PROMOTE,
     'ANCHOR_KEY = {"carbaryl": "111", "pyrethroid": "47", "chlorothalonil": "115"}',
     'ANCHOR_KEY = {"carbaryl": "115", "pyrethroid": "115", "chlorothalonil": "115"}'),

    # ---- blast ---------------------------------------------------------------------------------------
    ("blast: the crop set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: the method set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', '    if False:'),
    ("blast: the source set comparison is disabled", "blast", PROMOTE,
     '    if set(post["sources"]) != set(pre["sources"]) | {SOURCE_ID}:', '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: bystander methods stop being compared", "blast", PROMOTE,
     '        if key not in CAUTIONS and post["methods"][key] != before:', '        if False:'),
    ("blast: bystander sources stop being compared", "blast", PROMOTE,
     '        if post["sources"][sid] != before:', '        if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    data["source_catalog"][SOURCE_ID] = copy.deepcopy(SOURCE)',
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    data["source_catalog"][SOURCE_ID] = copy.deepcopy(SOURCE)'),

    # ---- hygiene / mechanics ---------------------------------------------------------------------------
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '        for c in want:\n            h = hygiene(c)', '        for c in ():\n            h = hygiene(c)'),
    ("hygiene: the British-spelling family leaves the check", "hygiene", PROMOTE,
     '    for w in BRITISH:\n        if re.search(rf"\\b{w}\\b", s, re.I):', '    for w in ():\n        if re.search(rf"\\b{w}\\b", s, re.I):'),
    ("hygiene: the absolutes family leaves the check", "hygiene", PROMOTE,
     '    for a in ABSOLUTES:\n        if a in s.lower():', '    for a in ():\n        if a in s.lower():'),
    ("hygiene: the dash check is disabled", "hygiene", PROMOTE,
     '    if "—" in s or "–" in s:', '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to stops writing the cautions", PROMOTE,
            '    for key, cautions in CAUTIONS.items():', '    for key, cautions in {}.items():')


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
    wd = tempfile.mkdtemp(prefix="mutate_convdisc_")
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
    print("MUTATION HARNESS -- conventional-tier disclosure (3 methods, 1 source, 10 live rungs)")
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
