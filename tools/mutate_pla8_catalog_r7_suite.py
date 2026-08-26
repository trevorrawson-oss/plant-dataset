#!/usr/bin/env python3
"""Mutation harness for PLA-8 catalog round 7 (PLA-215).

THE `refusal` FAMILY IS NEW TO THIS ARC AND IT GUARDS AN ABSENCE. Every guard family built so far
checks that something the promote DID is correct. This one checks that something the promote
DECLINED to do stayed declined: `planting_time_avoidance` gains no disease target, because six T1
documents were read looking for the claim and none makes it. A refusal that leaves no trace cannot
be told apart from an oversight, and the next session would have no way to know the question had
already been asked. These mutations add the target, empty the forbidden list, and disable the guard
in each of the two places it runs.

THE `tier` FAMILY exists because `biofungicide`'s tier is a CONTENT decision, not a label. Tier
decides ladder order; UC IPM says research has not shown these products as effective as oils or
sulfur; so the method has to sit BELOW sulfur, which is what `biological` buys and what
`soft_chemical` would destroy. Mutations move it in both directions.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r7.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r7.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r7_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- refusal: the guard for what the round did NOT do ---------------------------------------
    ("refusal: the forbidden-target list is emptied", "refusal", CONTENT,
     'REFUSED_WIDENING = ("planting_time_avoidance", ("fungal_foliar", "fungal_soilborne",',
     'REFUSED_WIDENING = ("planting_time_avoidance", ("zzz_none", "fungal_soilborne_X",'),
    ("refusal: the guard is disabled in check", "refusal", PROMOTE,
     '    problem = refused_widening_holds(cm)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),
    ("refusal: the guard is disabled in verify_post", "refusal", PROMOTE,
     '    problem = refused_widening_holds(cm)\n    if problem:\n        return "post: " + problem',
     '    problem = None\n    if problem:\n        return "post: " + problem'),
    ("refusal: the intersection test is inverted to always pass", "refusal", PROMOTE,
     '    present = sorted(set(cm[key].get("applies_to") or []) & set(forbidden))',
     '    present = []'),
    ("refusal: apply_round widens the refused method anyway", "refusal", CONTENT,
     '    for key, method in MINTS.items():\n        cm[key] = dict(method)',
     '    cm["planting_time_avoidance"]["applies_to"].append("fungal_foliar")\n'
     '    for key, method in MINTS.items():\n        cm[key] = dict(method)'),

    # ---- tier: a content decision, because tier decides ladder ORDER -----------------------------
    ("tier: biofungicide becomes soft_chemical, colliding with sulfur", "tier", CONTENT,
     '        "tier": "biological",\n        "applies_to": ["fungal_foliar"],',
     '        "tier": "soft_chemical",\n        "applies_to": ["fungal_foliar"],'),
    ("tier: biofungicide becomes conventional, ordering above sulfur", "tier", CONTENT,
     '        "name": "Biological fungicide",', '        "name": "Biological fungicide",\n        "_x": 1,'),
    ("tier: weed_host_control stops being cultural", "tier", CONTENT,
     '        "name": "Clearing the weeds that host it",\n        "tier": "cultural",',
     '        "name": "Clearing the weeds that host it",\n        "tier": "physical",'),

    # ---- scope --------------------------------------------------------------------------------------
    ("scope: weed_host_control gains insect_general (reaches mites, unsourced)", "scope", CONTENT,
     '        "applies_to": ["insect_soft_bodied", "fungal_foliar"],',
     '        "applies_to": ["insect_soft_bodied", "fungal_foliar", "insect_general"],'),
    ("scope: weed_host_control becomes 'any'", "scope", CONTENT,
     '        "applies_to": ["insect_soft_bodied", "fungal_foliar"],', '        "applies_to": ["any"],'),
    ("scope: biofungicide widens to bacterial", "scope", CONTENT,
     '        "applies_to": ["fungal_foliar"],',
     '        "applies_to": ["fungal_foliar", "bacterial"],'),
    ("scope: the vocabulary check is disabled", "scope", PROMOTE,
     '        bad = [t for t in m["applies_to"] if t not in vocab]', '        bad = []'),

    # ---- hedge --------------------------------------------------------------------------------------
    ("hedge: the efficacy limit is softened in the seasoned register", "hedge", CONTENT,
     '"research has not shown these products to be as effective as oils or sulfur in "\n'
     '            "controlling the pathogen.',
     '"research supports these products for "\n            "controlling the pathogen.'),
    ("hedge: the efficacy limit leaves the cons", "hedge", CONTENT,
     '            "Research has not shown these as effective as oils or sulfur, so a bad year can outrun them",',
     '            "A dependable option once the label interval is kept",'),
    ("hedge: the host-specific caution is dropped", "hedge", CONTENT,
     '            "The relationship is host-specific rather than general tidiness, so it is worth knowing "',
     '            "Clear any weeds nearby, since tidiness helps, and it is worth knowing "'),
    ("hedge: the required-hedge check is disabled", "hedge", PROMOTE,
     '            if h.lower() not in blob:', '            if False:'),

    # ---- sourcing -----------------------------------------------------------------------------------
    ("sourcing: the T1 tier check is disabled", "sourcing", PROMOTE,
     '        if (known[s].get("tier") or "").upper() != "T1":', '        if False:'),
    ("sourcing: the new source loses its title (A54)", "sourcing", CONTENT,
     '        "title": "Thrips / Home and Landscape / UC Statewide IPM Program (UC IPM)",',
     '        "_title": "Thrips / Home and Landscape / UC Statewide IPM Program (UC IPM)",'),
    ("sourcing: the A54 title check is disabled", "sourcing", PROMOTE,
     '        if _doc_scoped(entry) and not str(entry.get("title") or "").strip():', '        if False:'),
    ("sourcing: the new source is demoted to T2", "sourcing", CONTENT,
     '        "tier": "T1",\n        "citable_for": "UC IPM Pest Notes 7429.',
     '        "tier": "T2",\n        "citable_for": "UC IPM Pest Notes 7429.'),
    ("sourcing: a declared source loses its anchoring_url check", "sourcing", PROMOTE,
     '        if s not in m["anchoring_urls"]:', '        if False:'),
    ("sourcing: the two UC documents collapse onto one id", "sourcing", CONTENT,
     '            "ucanr_ext_thrips": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html",',
     '            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html",'),

    # ---- shape --------------------------------------------------------------------------------------
    ("shape: a required field is dropped from a mint", "shape", CONTENT,
     '        "best_use":\n            "A bed with a history of aphids',
     '        "_best_use":\n            "A bed with a history of aphids'),
    ("shape: a mint tier becomes invalid", "shape", CONTENT,
     '        "tier": "biological",', '        "tier": "microbial",'),
    ("shape: the already-in-catalog refusal is disabled", "shape", PROMOTE,
     '        if key in cm:\n            return f"{key} is already in the catalog"',
     '        if key in cm:\n            pass'),

    # ---- hygiene ------------------------------------------------------------------------------------
    ("hygiene: an absolute claim enters a mint's pros", "hygiene", CONTENT,
     '            "Costs nothing but the weeding you were half doing anyway, and it acts before the crop "',
     '            "Always stops the pest before the crop "'),
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '        for s in prose_of(m):\n            bad = hygiene(s)', '        for s in []:\n            bad = hygiene(s)'),
    ("hygiene: the absolutes family leaves the regex", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     '    if False:'),

    # ---- blast --------------------------------------------------------------------------------------
    ("blast: a crop is touched during the round", "blast", CONTENT,
     '    for sid, entry in NEW_SOURCES.items():\n        sc[sid] = dict(entry)',
     '    data["crops"][0]["name"] = "MUTATED"\n    for sid, entry in NEW_SOURCES.items():\n        sc[sid] = dict(entry)'),
    ("blast: an existing bystander method is edited", "blast", CONTENT,
     '    for key, method in MINTS.items():\n        cm[key] = dict(method)',
     '    cm["sulfur"]["best_use"] += " Also a biofungicide."\n    for key, method in MINTS.items():\n        cm[key] = dict(method)'),
    ("blast: verify_post stops checking which methods were added", "blast", PROMOTE,
     '    if added_m != set(C.MINTS):', '    if False:'),
    ("blast: verify_post stops checking existing methods", "blast", PROMOTE,
     '        if post["methods"][k] != before:', '        if False:'),
    ("blast: verify_post stops checking existing sources", "blast", PROMOTE,
     '        if post["sources"][k] != before:', '        if False:'),
    ("blast: verify_post stops checking crops", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),
    ("blast: verify_post stops noticing a dropped method", "blast", PROMOTE,
     '    if set(pre["methods"]) - set(post["methods"]):', '    if False:'),

    # ---- mechanics ----------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_round becomes a no-op", CONTENT,
            '    for key, method in MINTS.items():\n        cm[key] = dict(method)',
            '    for key, method in []:\n        cm[key] = dict(method)')


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
    wd = tempfile.mkdtemp(prefix="mutate_r7_")
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
    print("MUTATION HARNESS -- PLA-8 catalog round 7 (2 mints, 1 refusal)")
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
