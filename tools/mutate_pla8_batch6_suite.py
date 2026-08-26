#!/usr/bin/env python3
"""Mutation harness for PLA-8 batch 6, the two peas (PLA-215).

THE `readfinding` FAMILY IS LOAD-BEARING AND IT IS SHAPED DIFFERENTLY FROM EVERY EARLIER BATCH's.
The read did not simply remove a wrong rung; it SCOPED a method. `wet_foliage_discipline` leaves the
powdery-mildew ladder because its mechanism is free-water transport and powdery mildew does not
travel that way, and it STAYS on the ascochyta ladder on the same two crops, where the entry's own
cause says splashing water spreads it. So the mutations attack from both sides: put the method back
on powdery mildew, and strip it from ascochyta as a blanket removal. A guard that only checked the
removal would be satisfied by deleting the method everywhere, which is the over-correction, and this
harness proves it is not.

THE `nottwins` FAMILY is batch 5's premise inverted. There it was "these two ARE the same, so a
propagation is licensed"; here it is "these two are NOT, so each needed its own pass". Both
directions are refused and both are injected.

THE `rounds` FAMILY checks that three catalog rounds are observable in the shipped data rather than
only in prose: r6's corrected criterion admitting the single-generation pea weevil, r7's two mints
being consumed, and r7's REFUSAL visible as the absence of a disease reaching that method.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch6.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch6.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- readfinding: the scoped drop, attacked from both sides ---------------------------------
    ("readfinding: check_read_fixes is disabled entirely", "readfinding", PROMOTE,
     '    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by),',
     '    for problem in (check_not_twins(by, batch), None,'),
    ("readfinding: the method is allowed back onto powdery mildew (check)", "readfinding", PROMOTE,
     '        if WFD in mpm:\n            return (f"{slug}/{PM} carries {WFD}',
     '        if False:\n            return (f"{slug}/{PM} carries {WFD}'),
    ("readfinding: the method is allowed back onto powdery mildew (verify_post)", "readfinding",
     PROMOTE, '        if WFD in mpm:\n            return f"post: {slug}/{PM} regained {WFD}"',
     '        if False:\n            return f"post: {slug}/{PM} regained {WFD}"'),
    ("readfinding: the ascochyta half is disabled, permitting a BLANKET removal (check)",
     "readfinding", PROMOTE,
     '        if WFD not in masc:\n            return (f"{slug}/{ASC} lost {WFD}',
     '        if False:\n            return (f"{slug}/{ASC} lost {WFD}'),
    ("readfinding: the ascochyta half is disabled in verify_post", "readfinding", PROMOTE,
     '        if WFD not in masc:\n            return f"post: {slug}/{ASC} lost {WFD}',
     '        if False:\n            return f"post: {slug}/{ASC} lost {WFD}'),
    ("readfinding: airflow_spacing is no longer required on powdery mildew", "readfinding", PROMOTE,
     '        if "airflow_spacing" not in mpm:\n            return (f"{slug}/{PM} lost airflow_spacing',
     '        if False:\n            return (f"{slug}/{PM} lost airflow_spacing'),
    ("readfinding: the catalog-caution precondition is disabled", "readfinding", PROMOTE,
     '    if not any("powdery mildew" in c.lower() for c in (cm[WFD].get("cautions") or [])):',
     '    if False:'),
    ("readfinding: the root-rot ordering check is disabled", "readfinding", PROMOTE,
     '        if mrr.index("improve_drainage") > mrr.index("sound_sowing_practice"):', '        if False:'),
    ("readfinding: the ascochyta ordering check is disabled", "readfinding", PROMOTE,
     '        if masc.index("garden_sanitation") > masc.index("crop_rotation"):', '        if False:'),
    ("readfinding: the tolerance rung no longer has to sit last", "readfinding", PROMOTE,
     '        if mrr[-1] != "resistant_varieties":', '        if False:'),

    # ---- nottwins: batch 5's premise, inverted ---------------------------------------------------
    ("nottwins: check_not_twins is disabled entirely", "nottwins", PROMOTE,
     '    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by),',
     '    for problem in (None, check_read_fixes(batch, by),'),
    ("nottwins: the canonical-identity branch is disabled", "nottwins", PROMOTE,
     '    if a == b:\n        return (f"{CROPS[0]} and {CROPS[1]} are byte-identical', '    if False:\n        return (f"{CROPS[0]} and {CROPS[1]} are byte-identical'),
    ("nottwins: the staged-copy branch is disabled", "nottwins", PROMOTE,
     '    if dg[CROPS[0]] == dg[CROPS[1]]:', '    if False:'),
    ("nottwins: verify_post stops asserting the two ladders differ", "nottwins", PROMOTE,
     '    if sig(CROPS[0]) == sig(CROPS[1]):', '    if False:'),
    # The first version of this mutation renamed only the FIRST FIVE fields and left the rest of the
    # tuple intact, so the surviving fields still separated the two crops and it survived. Collapse
    # the whole comparison to the problem name -- which IS identical across these two -- so the
    # signatures genuinely match and the guard has to be the thing that objects.
    ("nottwins: the compared field set collapses to the problem name alone", "nottwins", PROMOTE,
     'PROSE_FIELDS = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",',
     'PROSE_FIELDS = ("name",) if True else ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",'),

    # ---- rounds: three catalog rounds, observable in the data ------------------------------------
    ("rounds: check_rounds_are_exercised is disabled", "rounds", PROMOTE,
     '                    check_rounds_are_exercised(batch)):', '                    None):'),
    ("rounds: the r7 use table is emptied", "rounds", PROMOTE,
     'R7_USE = {PM: "biofungicide", "pea-aphid": "weed_host_control", "thrips": "weed_host_control"}',
     'R7_USE = {}'),
    ("rounds: the r6 use table is emptied", "rounds", PROMOTE,
     'R6_USE = {"pea-weevil": "planting_time_avoidance"}', 'R6_USE = {}'),
    ("rounds: the refused-widening check stops looking at problem type", "rounds", PROMOTE,
     '            if "planting_time_avoidance" in ms and p.get("type") != "insect":', '            if False:'),
    ("rounds: the catalog-presence precondition is disabled", "rounds", PROMOTE,
     '        if method not in cm:\n            return f"{method} is not in the catalog; its catalog round must land first"',
     '        if method not in cm:\n            pass'),

    # ---- shape -------------------------------------------------------------------------------------
    ("shape: the tier-monotonicity check is disabled", "shape", PROMOTE,
     '            if tiers != sorted(tiers):', '            if False:'),
    ("shape: the EMPTY-ladder check is disabled", "shape", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if not lad:\n                pass'),
    ("shape: the duplicate-method check is disabled", "shape", PROMOTE,
     '                if m in seen:', '                if False:'),
    ("shape: the applies_to coherence check is disabled", "shape", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("shape: the identical-registers check is disabled", "shape", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', '                if False:'),
    ("shape: the per-crop rung count check is disabled", "shape", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),
    ("ids: the id convention table is emptied", "ids", PROMOTE,
     'ID_CONVENTION = {"Powdery mildew": "powdery-mildew", "Fusarium wilt": "fusarium-wilt"}',
     'ID_CONVENTION = {}'),
    ("ids: the id guard reads the STAGED name (batch 4's dead form)", "ids", PROMOTE,
     '            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""',
     '            name = p.get("name") or ""'),

    # ---- blast ---------------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()',
     'def apply_to(data):\n    {c.get("slug"): c for c in data["crops"]}["tomatillo"]["name"] = "MUTATED"\n    batch = staged()'),
    ("blast: verify_post stops checking bystander crops", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: verify_post stops checking control_methods", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', '    if False:'),
    ("blast: verify_post stops checking source_catalog", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: verify_post stops comparing the crop set", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),

    # ---- mechanics -------------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            '                tgt["type"] = add["type"]\n                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])',
            '                tgt["type"] = add["type"]')


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
    wd = tempfile.mkdtemp(prefix="mutate_b6_")
    sandbox_staging = os.path.join(wd, "staging")
    shutil.copytree(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch6"), sandbox_staging)
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_ladder_batch6")',
        f'STAGING = {sandbox_staging!r}', 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit(f"HARNESS DEAD: marker absent for {os.path.basename(path)}")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 BATCH 6, the two peas")
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
