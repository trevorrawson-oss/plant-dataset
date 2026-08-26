#!/usr/bin/env python3
"""Mutation harness for the chlorothalonil mint (PLA-215).

THE `disclosure` FAMILY IS LOAD-BEARING IN A WAY NO EARLIER FAMILY IN THIS ARC HAS BEEN. Every other
guard in this catalog protects a reader's crop. These protect the reader. Chlorothalonil sits on the
DANGER signal-word band, is rated High for water quality and High for acute toxicity, and appears on
both the California Prop 65 list and the US EPA list, where an active ingredient is listed only as a
likely or confirmed carcinogen.

The ruling that admits it (Trevor, 2026-08-26) is that a product people can buy off a shelf gets
named with its profile stated. That ruling is only honoured if the profile is ACTUALLY stated, so
these mutations remove each hazard axis ONE AT A TIME and require the promote to refuse each by
name. A guard that counted cautions, or looked for "some" hazard language, would let the carcinogen
line vanish while staying green -- and that is precisely the shape of defect this arc has found four
times in prose that read as coverage.

THE `separation` FAMILY pins that this promote mints a key and touches no ladder. Adding a
conventional rung to nine certified crops is its own reviewable act and belongs to its own promote;
a mint that quietly attached rungs would smuggle that past review.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_chlorothalonil.py")
PROMOTE = os.path.join(HERE, "promote_pla8_chlorothalonil.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- disclosure: one injection per hazard axis, plus the machinery that enforces them --------
    ("disclosure: the axis table is emptied", "disclosure", PROMOTE,
     'REQUIRED_DISCLOSURES = {\n    "aquatic":', 'REQUIRED_DISCLOSURES = {} or {\n    "_aquatic":'),
    ("disclosure: the check is disabled", "disclosure", PROMOTE,
     '    miss = missing_disclosures(METHOD)\n    if miss:', '    miss = missing_disclosures(METHOD)\n    if False:'),
    ("disclosure: verify_post stops re-checking the shipped cautions", "disclosure", PROMOTE,
     '    miss = missing_disclosures(cm[KEY])\n    if miss:', '    miss = missing_disclosures(cm[KEY])\n    if False:'),
    ("disclosure: the axis test weakens from ALL tokens to ANY", "disclosure", PROMOTE,
     '                  if not all(t in blob for t in toks))', '                  if not any(t in blob for t in toks))'),
    ("disclosure: the CARCINOGEN caution is deleted", "disclosure", PROMOTE,
     '        "Listed on both the California Prop 65 list and the US EPA list, where an active ingredient "\n'
     '        "appears only as a likely or confirmed carcinogen; weigh that before choosing it on a food "\n'
     '        "crop",',
     '        "Use it thoughtfully on a food crop",'),
    ("disclosure: the ACUTE toxicity caution is deleted", "disclosure", PROMOTE,
     '        "UC IPM rates acute toxicity to people and other mammals High, the DANGER signal-word band, "\n'
     '        "and notes the rating follows the most sensitive route of entry rather than oral toxicity",',
     '        "Handle it with the usual care",'),
    ("disclosure: the AQUATIC caution is deleted", "disclosure", PROMOTE,
     '        "Rated High for water quality risk to aquatic wildlife; keep spray and runoff away from "\n'
     '        "ponds, streams, storm drains and puddles",',
     '        "Apply it tidily",'),
    ("disclosure: the BEE caution is deleted", "disclosure", PROMOTE,
     '        "Bee rating II: do not apply it, or let it drift, onto anything in flower including weeds, "\n'
     '        "except between sunset and midnight where the label allows, and do not let it reach water "\n'
     '        "bees can drink",',
     '        "Mind the pollinators",'),
    ("disclosure: the PPE caution is deleted", "disclosure", PROMOTE,
     '        "Many consumer products do not print protective equipment on the label; wear chemical "\n'
     '        "resistant gloves, long sleeves and goggles regardless",',
     '        "Follow the label for protective equipment",'),
    ("disclosure: the PHI caution is deleted", "disclosure", PROMOTE,
     '        "Observe the pre-harvest interval on the label before eating the crop, and read and follow "\n'
     '        "the label every time",',
     '        "Read the label",'),
    ("disclosure: the beginner register stops saying it is the heavy end", "disclosure", PROMOTE,
     '        "strongest thing on a garden center shelf for several leaf diseases, and it carries the "\n'
     '        "heaviest warnings of anything in this guide, so it belongs at the end of the list rather "\n'
     '        "than the start.',
     '        "strongest thing on a garden center shelf for several leaf diseases, so it is a good "\n'
     '        "choice when you need one.'),

    # ---- scope and tier ---------------------------------------------------------------------------
    ("scope: the tier softens to soft_chemical", "scope", PROMOTE,
     '    "tier": "conventional",', '    "tier": "soft_chemical",'),
    ("scope: the tier check is disabled", "scope", PROMOTE,
     '    if METHOD["tier"] != "conventional":', '    if False:'),
    ("scope: applies_to widens to disease_general", "scope", PROMOTE,
     '    "applies_to": ["fungal_foliar"],', '    "applies_to": ["fungal_foliar", "disease_general"],'),
    ("scope: the applies_to check is disabled", "scope", PROMOTE,
     '    if METHOD["applies_to"] != ["fungal_foliar"]:', '    if False:'),
    ("scope: verify_post stops checking scope and tier", "scope", PROMOTE,
     '    if cm[KEY]["applies_to"] != ["fungal_foliar"]:', '    if False:'),

    # ---- separation: the mint touches no ladder ---------------------------------------------------
    ("separation: apply_to also attaches a rung to a certified crop", "separation", PROMOTE,
     '    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))',
     '    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))\n'
     '    for _c in data["crops"]:\n'
     '        if _c.get("slug") == "cucumber":\n'
     '            for _p in _c.get("diseases") or []:\n'
     '                if _p.get("id") == "anthracnose":\n'
     '                    _p["control_ladder"].append({"method": KEY, "note_beginner": "b", "note_seasoned": "s"})'),
    ("separation: verify_post stops checking crops", "separation", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),

    # ---- sourcing ------------------------------------------------------------------------------------
    ("sourcing: the T1 check is disabled", "sourcing", PROMOTE,
     '        if (sc[s].get("tier") or "").upper() != "T1":', '        if False:'),
    ("sourcing: the anchor drops to the database INDEX, which has no hazard content", "sourcing",
     PROMOTE,
     '        "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/"\n'
     '                             "pesticide-active-ingredients-database/active-ingredient-details/"\n'
     '                             "?uaiKey=115",',
     '        "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/"\n'
     '                             "pesticide-active-ingredients-database/"\n'
     '                             "",'),
    ("sourcing: a declared source loses its anchoring_url check", "sourcing", PROMOTE,
     '        if s not in METHOD["anchoring_urls"]:', '        if False:'),

    # ---- shape / hygiene / blast / mechanics -----------------------------------------------------------
    ("shape: a required field is dropped", "shape", PROMOTE,
     '    "best_use":\n        "A rescue-only last resort', '    "_best_use":\n        "A rescue-only last resort'),
    ("shape: the already-in-catalog refusal is disabled", "shape", PROMOTE,
     '    if KEY in cm:\n        return f"{KEY} is already in the catalog"',
     '    if KEY in cm:\n        pass'),
    ("hygiene: an absolute claim enters the prose", "hygiene", PROMOTE,
     '        "Broad-spectrum and effective against several leaf diseases at once, including some the "',
     '        "Completely effective against several leaf diseases at once, including some the "'),
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '    for s in prose_of(METHOD):\n        bad = hygiene(s)', '    for s in []:\n        bad = hygiene(s)'),
    ("blast: an existing method is edited during the mint", "blast", PROMOTE,
     '    if KEY in data["control_methods"]:\n        raise AssertionError',
     '    data["control_methods"]["sulfur"]["best_use"] += " x"\n    if KEY in data["control_methods"]:\n        raise AssertionError'),
    ("blast: verify_post stops checking existing methods", "blast", PROMOTE,
     '        if post["methods"][k] != before:', '        if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: verify_post stops comparing which methods were added", "blast", PROMOTE,
     '    if added != {KEY}:', '    if False:'),
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))\n    return 1',
            '    return 1')


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
            bad.append(f"  {n}x  {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_chl_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
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
    print("MUTATION HARNESS -- mint chlorothalonil")
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
