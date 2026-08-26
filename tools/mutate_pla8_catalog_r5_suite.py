#!/usr/bin/env python3
"""Mutation harness for PLA-8 catalog round 5 (PLA-215).

THE `widening` FAMILY IS LOAD-BEARING, and it is the family this repo has no prior harness for.
Every earlier catalog round MINTED; this one also WIDENS two methods that already ship, and a
widening is the one catalog operation that is invisible to every structural gate when it goes
wrong. `balance_nitrogen` reaching a fungal disease while its prose still talks only about aphids
passes `control_ladder_gate`, `whole_crop_gate` and `release_verify`, and is the `bottom_watering`
defect exactly: right key, wrong meaning, twelve rungs deep before anybody read it. The mutations
break the widening in both directions -- evidence removed from the prose, and the old case thrown
away to make room for the new one.

THE `scope` FAMILY exists because both mints were deliberately scoped narrower than the nearest
plausible reading, and a target added on plausibility is what this arc keeps having to undo. One of
these mutations reproduces a real over-reach the guard suite caught during authoring: declaring
`insect_general` on `planting_time_avoidance` would have made it reachable by a spider mite, which
has no emergence window to dodge and no source behind the claim.

THE `hedge` FAMILY carries a NEGATIVE injection the other rounds did not need. UMN writes that a
July sowing "will not suffer any damage"; Clemson hedges the same mechanism with "may escape
damage". The weaker source governs, so one mutation drops Clemson's hedge and another lets UMN's
absolute into consumer prose.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r5.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r5.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r5_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- scope: each mint is scoped to what was READ ---------------------------------------------
    ("scope: wet_foliage widens to disease_general (reaches viral, unsourced)", "scope", CONTENT,
     '"applies_to": ["bacterial", "fungal_foliar"],',
     '"applies_to": ["bacterial", "fungal_foliar", "disease_general"],'),
    ("scope: wet_foliage becomes 'any'", "scope", CONTENT,
     '"applies_to": ["bacterial", "fungal_foliar"],', '"applies_to": ["any"],'),
    ("scope: planting_time regains insect_general (the real mite over-reach)", "scope", CONTENT,
     '"applies_to": ["insect_chewing", "insect_boring"],',
     '"applies_to": ["insect_chewing", "insect_boring", "insect_general"],'),
    ("scope: planting_time gains a disease target", "scope", CONTENT,
     '"applies_to": ["insect_chewing", "insect_boring"],',
     '"applies_to": ["insect_chewing", "insect_boring", "disease_general"],'),
    ("scope: the mint vocabulary check is disabled", "scope", PROMOTE,
     '        bad = [t for t in m["applies_to"] if t not in vocab]', '        bad = []'),
    ("scope: the widening vocabulary check is disabled", "scope", PROMOTE,
     '        bad = [t for t in added if t not in vocab]', '        bad = []'),

    # ---- widening: the family with no prior harness in this arc -----------------------------------
    ("widening: the prose-carries-its-evidence check (G5) is disabled", "widening", PROMOTE,
     '            if token not in blob:', '            if False:'),
    ("widening: balance_nitrogen's evidence tokens are emptied", "widening", PROMOTE,
     '    "balance_nitrogen": ("canopy", "white mold"),', '    "balance_nitrogen": (),'),
    ("widening: augmentative_release's evidence tokens are emptied", "widening", PROMOTE,
     '    "augmentative_release": ("pediobius", "beetle"),', '    "augmentative_release": (),'),
    ("widening: applies_to is REPLACED rather than added to (drops the aphid case)", "widening",
     CONTENT,
     '        m["applies_to"] = list(m["applies_to"]) + list(w["add_applies_to"])',
     '        m["applies_to"] = list(w["add_applies_to"])'),
    ("widening: sources are REPLACED rather than added to", "widening", CONTENT,
     '        m["sources"] = list(m["sources"]) + [s for s in w["add_sources"] if s not in m["sources"]]',
     '        m["sources"] = list(w["add_sources"])'),
    ("widening: the anchor-overwrite refusal is disabled in check", "widening", PROMOTE,
     '            if sid in (cm[key].get("anchoring_urls") or {}):', '            if False:'),
    ("widening: the anchor-overwrite refusal is disabled in apply", "widening", CONTENT,
     '            if sid in anchors:', '            if False:'),
    ("widening: the new UC anchor is filed under the id already in use", "widening", CONTENT,
     '            "ucanr_ext_dry_bean_white_mold": {\n                "url": "https://ipm.ucanr.edu/agriculture/dry-beans/white-mold/", "verified": VERIFIED},',
     '            "ucanr_ext": {\n                "url": "https://ipm.ucanr.edu/agriculture/dry-beans/white-mold/", "verified": VERIFIED},'),
    ("widening: white mold leaves the seasoned register", "widening", CONTENT,
     '                "the microclimate white mold and similar rots need.",',
     '                "the microclimate these rots need.",'),

    # ---- hedge: the qualifiers, and the absolute that must not travel -----------------------------
    ("hedge: Clemson's 'may' is dropped from the seasoned register", "hedge", CONTENT,
     '            "August and that quick-maturing beans sown very early or during late summer may escape "',
     '            "August and that quick-maturing beans sown very early or during late summer escape "'),
    ("hedge: UMD's scale limit becomes a home-garden claim", "hedge", CONTENT,
     '                "in large plantings or community gardens, which is the scale limit worth carrying "',
     '                "in any home garden, which is the scale limit worth carrying "'),
    ("hedge: the local-confirmation caution is dropped", "hedge", CONTENT,
     '"starting point and confirm it locally rather than carrying a date across regions",',
     '"starting point for any region",'),
    ("hedge: the required-hedge check is disabled", "hedge", PROMOTE,
     '            if h.lower() not in blob:', '            if False:'),
    ("hedge: UMN's absolute enters the prose", "hedge", CONTENT,
     '            "Costs nothing and adds no material, since the only thing that changes is the sowing date",',
     '            "A crop sown after the flight will not suffer any damage",'),
    ("hedge: the forbidden-absolute check is disabled", "hedge", PROMOTE,
     '    if any(C.FORBIDDEN_ABSOLUTE.lower() in s.lower() for s in everything):', '    if False:'),

    # ---- sourcing ---------------------------------------------------------------------------------
    ("sourcing: the T1 tier check is disabled", "sourcing", PROMOTE,
     '        if (known[s].get("tier") or "").upper() != "T1":', '        if False:'),
    ("sourcing: the new source loses its title (A54)", "sourcing", CONTENT,
     '        "title": "White Mold / Dry Beans / Agriculture: Pest Management Guidelines / "',
     '        "_title": "White Mold / Dry Beans / Agriculture: Pest Management Guidelines / "'),
    ("sourcing: the A54 title check is disabled", "sourcing", PROMOTE,
     '        if _doc_scoped(entry) and not str(entry.get("title") or "").strip():',
     '        if False:'),
    ("sourcing: the new source is demoted to T2", "sourcing", CONTENT,
     '        "tier": "T1",\n        "citable_for": "UC IPM Pest Management Guidelines: Dry Beans',
     '        "tier": "T2",\n        "citable_for": "UC IPM Pest Management Guidelines: Dry Beans'),
    ("sourcing: a mint source loses its anchoring_url check", "sourcing", PROMOTE,
     '        if s not in m["anchoring_urls"]:', '        if False:'),
    ("sourcing: an anchor stops being https", "sourcing", CONTENT,
     '"umd_ext": {"url": "https://extension.umd.edu/resource/mexican-bean-beetle-vegetables",',
     '"umd_ext": {"url": "http://extension.umd.edu/resource/mexican-bean-beetle-vegetables",'),

    # ---- shape ------------------------------------------------------------------------------------
    ("shape: a required field is dropped from a mint", "shape", CONTENT,
     '        "best_use":\n            "A pest with one main generation',
     '        "_best_use":\n            "A pest with one main generation'),
    ("shape: a mint tier becomes invalid", "shape", CONTENT,
     '        "name": "Staying out of wet foliage",\n        "tier": "cultural",',
     '        "name": "Staying out of wet foliage",\n        "tier": "behavioral",'),
    ("shape: the already-in-catalog refusal is disabled", "shape", PROMOTE,
     '        if key in cm:\n            return f"{key} is already in the catalog"',
     '        if key in cm:\n            pass'),

    # ---- hygiene ----------------------------------------------------------------------------------
    ("hygiene: an absolute claim enters a mint's pros", "hygiene", CONTENT,
     '            "Costs nothing and adds no material, since it only moves a job by a few hours",',
     '            "Costs nothing and always stops the disease spreading",'),
    ("hygiene: the hygiene sweep runs over nothing", "hygiene", PROMOTE,
     '    for s in everything:\n        bad = hygiene(s)', '    for s in []:\n        bad = hygiene(s)'),
    ("hygiene: the absolutes family leaves the hygiene regex", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     '    if False:'),

    # ---- blast ------------------------------------------------------------------------------------
    ("blast: a crop is touched during the round", "blast", CONTENT,
     '    for key, method in MINTS.items():\n        cm[key] = dict(method)',
     '    data["crops"][0]["name"] = "MUTATED"\n    for key, method in MINTS.items():\n        cm[key] = dict(method)'),
    ("blast: an existing bystander method is edited", "blast", CONTENT,
     '    for sid, entry in NEW_SOURCES.items():\n        sc[sid] = dict(entry)',
     '    cm["handpick"]["best_use"] += " Also works in wet foliage."\n    for sid, entry in NEW_SOURCES.items():\n        sc[sid] = dict(entry)'),
    ("blast: verify_post stops checking which methods were added", "blast", PROMOTE,
     '    if added_m != set(C.MINTS):', '    if False:'),
    ("blast: verify_post stops checking crops", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', '    if False:'),
    ("blast: verify_post stops noticing a LOST target", "blast", PROMOTE,
     '        if set(before["applies_to"]) - set(m["applies_to"]):', '        if False:'),
    ("blast: verify_post stops noticing a LOST source", "blast", PROMOTE,
     '        if set(before["sources"]) - set(m["sources"]):', '        if False:'),
    ("blast: verify_post stops checking untouched methods", "blast", PROMOTE,
     '        if post["methods"][k] != before:', '        if False:'),

    # ---- adjudication: the three controls ruled ALREADY HOMED ------------------------------------
    # The ghost is a byte-copy of a VALID mint, so shape, sourcing, hedge and hygiene all pass on
    # it. Only the adjudication guard can object, which is what makes this a reachability proof
    # rather than a mutation an earlier check happens to swallow.
    ("adjudication: a ghost method is minted for an already-homed control", "adjudication", CONTENT,
     '# ------------------------------------------------------------------ widenings',
     'MINTS["weed_host_control"] = dict(MINTS["wet_foliage_discipline"])\n\n'
     '# ------------------------------------------------------------------ widenings'),

    # ---- gate / mechanics --------------------------------------------------------------------------
    ("gate: a mint declares a source that is not in the catalog", "gate", CONTENT,
     '        "sources": ["clemson_hgic", "umn_ext"],', '        "sources": ["clemson_hgic", "umn_extension"],'),
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
    wd = tempfile.mkdtemp(prefix="mutate_r5_")
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
    print("MUTATION HARNESS -- PLA-8 catalog round 5 (2 mints, 2 widenings, 1 source)")
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
        print(f"  {k:13s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
