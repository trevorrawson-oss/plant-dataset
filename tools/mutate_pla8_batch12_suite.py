#!/usr/bin/env python3
"""Mutation harness for the batch 12 fall-finishers promote (PLA-215).

The load-bearing families are `taxon` (two ids whose obvious reuse names the WRONG ORGANISM,
pinned in both directions), `join` (parsley reusing dill's `parsleyworm` across an uncommitted
batch boundary), `echo` (brussels-sprouts is the sixth brassica, and a copied sibling ladder reads
exactly like authored work) and `readfix`.

`trap` is the family added when the parallel round LANDED mid-build. brussels-sprouts/harlequin-bug
earns a `trap_cropping` rung its prose names outright, and exactly one problem in the batch does:
a rung on parsley's parsleyworm would REVERSE a conservation instruction, since those larvae are
relocated to live. So the family pins the rung's presence, its placement, and its scope in both
directions -- and `premises` inverted at the same moment, from refusing a base that HAS the key to
refusing one that lacks it.

WITHDRAWN, and deliberately not counted as coverage: the `ladder_signature` identity check in
verify_post. It is keyed by problem id and no two crops in this batch share an id set (fava 7,
brussels 9, parsley 6, all disjoint), so it cannot fire here however the ladders are doctored. It
was genuinely load-bearing in batch 10, where collards and kale carried identical id sets. Kept in
the promote for the next same-shaped pair; injecting it would report a survivor for a guard that
is a forward assertion rather than a gap.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch12.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch12.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- taxon ---------------------------------------------------------------------------------
    ("taxon: the required-id half of the ruling is disabled", "taxon", PROMOTE,
     '        if right not in staged_ids:', '        if False:'),
    ("taxon: the refused-id half of the ruling is disabled", "taxon", PROMOTE,
     '        if wrong in staged_ids:', '        if False:'),
    ("taxon: TAXON_REFUSED is emptied in check", "taxon", PROMOTE,
     '    for right, (wrong, why) in TAXON_REFUSED.items():',
     '    for right, (wrong, why) in {}.items():'),
    ("taxon: verify_post stops requiring the ruled id", "taxon", PROMOTE,
     '        if right not in shipped:', '        if False:'),
    ("taxon: verify_post stops refusing the wrong organism", "taxon", PROMOTE,
     '        if wrong in {p["id"] for _, p in problems(by["broad-beans-fava"])}:',
     '        if False:'),

    # ---- join ----------------------------------------------------------------------------------
    ("join: the base-carries-dills-mint check is disabled", "join", PROMOTE,
     '    if PARSLEYWORM not in sibling:', '    if False:'),
    ("join: parsley may drop the shared id", "join", PROMOTE,
     '    if ms is None:\n        return (f"parsley does not carry {PARSLEYWORM!r}',
     '    if False:\n        return (f"parsley does not carry {PARSLEYWORM!r}'),
    ("join: verify_post stops pinning the shared id", "join", PROMOTE,
     '    if ms is None:\n        return f"post: parsley did not ship {PARSLEYWORM!r}, dill\'s id"',
     '    if False:\n        return f"post: parsley did not ship {PARSLEYWORM!r}, dill\'s id"'),

    # ---- premises ------------------------------------------------------------------------------
    ("premises: the base-predates-the-mint refusal is disabled", "premises", PROMOTE,
     '    if "trap_cropping" not in cm:', '    if False:'),
    ("premises: the new-id-already-on-the-roster check is disabled", "premises", PROMOTE,
     '        if pid in ids:', '        if False:'),
    ("premises: the already-laddered refusal is disabled", "premises", PROMOTE,
     '            if "control_ladder" in p:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n                return f"{slug} is already laddered; re-laddering changes shipped ids"'),

    # ---- readfix -------------------------------------------------------------------------------
    ("readfix: the no-material refusal is disabled in check", "readfix", PROMOTE,
     '            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:\n                return (f"{slug}/{pid} carries {m!r} ({cm[m][\'tier\']}), but its prose states no home "',
     '            if False:\n                return (f"{slug}/{pid} carries {m!r} ({cm[m][\'tier\']}), but its prose states no home "'),
    ("readfix: NO_MATERIAL is emptied", "readfix", PROMOTE,
     'NO_MATERIAL = (("broad-beans-fava", "chocolate-spot"),\n'
     '               ("broad-beans-fava", "broad-bean-rust"),\n'
     '               ("broad-beans-fava", "downy-mildew"),\n'
     '               ("brussels-sprouts", "black-rot"),\n'
     '               ("parsley", "septoria-leaf-spot"))',
     'NO_MATERIAL = ()'),
    ("readfix: the tip-pinch rung requirement is disabled", "readfix", PROMOTE,
     '    if "garden_sanitation" not in ms:', '    if False:'),
    ("readfix: the stripped residue clause may return", "readfix", PROMOTE,
     '        if word in blob:', '        if False:'),
    ("readfix: SEED_FLY_BANNED is emptied", "readfix", PROMOTE,
     'SEED_FLY_BANNED = ("manure", "residue", "compost")', 'SEED_FLY_BANNED = ()'),
    ("readfix: the bt hedge requirement is disabled", "readfix", PROMOTE,
     '                if not any(h in low for h in BT_HEDGES):', '                if False:'),
    ("readfix: the bt non-selectivity requirement is disabled", "readfix", PROMOTE,
     '                if BT_NONSELECTIVE not in low:', '                if False:'),
    ("readfix: the timing scope is disabled in check", "readfix", PROMOTE,
     '            if "planting_time_avoidance" in lad and (slug, pid) not in TIMING_OK:\n                return (f"{slug}/{pid} carries planting_time_avoidance',
     '            if False:\n                return (f"{slug}/{pid} carries planting_time_avoidance'),
    ("readfix: TIMING_OK widens to a crop whose prose never recommends the shift", "readfix", PROMOTE,
     'TIMING_OK = (("broad-beans-fava", "black-bean-aphid"), ("broad-beans-fava", "bean-seed-fly"),\n             ("parsley", "carrot-rust-fly"))',
     'TIMING_OK = (("broad-beans-fava", "black-bean-aphid"), ("broad-beans-fava", "bean-seed-fly"),\n             ("parsley", "carrot-rust-fly"), ("brussels-sprouts", "clubroot"))'),
    ("readfix: HANDPICK_OK widens to a tissue-removal target", "readfix", PROMOTE,
     'HANDPICK_OK = ("cabbageworms", "harlequin-bug", "parsleyworm")',
     'HANDPICK_OK = ("cabbageworms", "harlequin-bug", "parsleyworm", "black-bean-aphid")'),
    ("readfix: the handpick scoping is disabled in check", "readfix", PROMOTE,
     '            if "handpick" in lad and pid not in HANDPICK_OK:\n                return (f"{slug}/{pid} carries handpick',
     '            if False:\n                return (f"{slug}/{pid} carries handpick'),
    ("readfix: the pyrethroid refusal is disabled in check", "readfix", PROMOTE,
     '            if "pyrethroid" in lad:\n                return f"{slug}/{pid} carries the synthetic pyrethroid; this batch uses pyrethrin"',
     '            if False:\n                return f"{slug}/{pid} carries the synthetic pyrethroid; this batch uses pyrethrin"'),
    ("trap: the wrong-problem scoping is disabled in check", "trap", PROMOTE,
     '            if "trap_cropping" in lad and (slug, pid) != TRAP_OK:\n                return (f"{slug}/{pid} carries trap_cropping, which only {TRAP_OK} earns in this "',
     '            if False:\n                return (f"{slug}/{pid} carries trap_cropping, which only {TRAP_OK} earns in this "'),
    ("trap: TRAP_OK moves to the crop whose prose would be REVERSED by a rung", "trap", PROMOTE,
     'TRAP_OK = ("brussels-sprouts", "harlequin-bug")', 'TRAP_OK = ("parsley", "parsleyworm")'),
    ("trap: the note-ban exemption widens to every rung", "trap", PROMOTE,
     'NOTE_BAN_EXEMPT = (("brussels-sprouts", "harlequin-bug", "trap_cropping"),)',
     'NOTE_BAN_EXEMPT = tuple((s, p, m) for s in ("brussels-sprouts", "parsley", "broad-beans-fava")\n                        for p in ("harlequin-bug", "parsleyworm", "cabbage-aphids")\n                        for m in ("trap_cropping", "handpick", "garden_sanitation"))'),
    ("trap: verify_post stops requiring the rung at all", "trap", PROMOTE,
     '    if ms is None or "trap_cropping" not in ms:', '    if False:'),
    ("trap: verify_post stops pinning the rung's placement", "trap", PROMOTE,
     '    if ms.index("trap_cropping") != TRAP_INDEX:', '    if False:'),
    ("readfix: NOTE_BANNED is emptied", "readfix", PROMOTE,
     'NOTE_BANNED = ("trap crop", "sacrificial", "relocate", "diatomaceous")', 'NOTE_BANNED = ()'),
    ("readfix: verify_post no-material pin is disabled", "readfix", PROMOTE,
     '            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:\n                return f"post: {slug}/{pid} shipped {m!r}, which its prose rules out"',
     '            if False:\n                return f"post: {slug}/{pid} shipped {m!r}, which its prose rules out"'),
    ("readfix: verify_post timing pin is disabled", "readfix", PROMOTE,
     '            if "planting_time_avoidance" in lad and (slug, pid) not in TIMING_OK:\n                return f"post: {slug}/{pid} shipped an unearned timing rung"',
     '            if False:\n                return f"post: {slug}/{pid} shipped an unearned timing rung"'),
    ("readfix: verify_post handpick pin is disabled", "readfix", PROMOTE,
     '            if "handpick" in lad and pid not in HANDPICK_OK:\n                return f"post: {slug}/{pid} shipped handpick on a tissue-removal target"',
     '            if False:\n                return f"post: {slug}/{pid} shipped handpick on a tissue-removal target"'),
    ("trap: verify_post wrong-problem scoping is disabled", "trap", PROMOTE,
     '            if "trap_cropping" in lad and (slug, pid) != TRAP_OK:\n                return (f"post: {slug}/{pid} shipped trap_cropping',
     '            if False:\n                return (f"post: {slug}/{pid} shipped trap_cropping'),
    ("readfix: verify_post note scan is disabled", "readfix", PROMOTE,
     '                for word in NOTE_BANNED:\n                    if word in low:\n                        return f"post: {slug}/{pid}: a note mentions {word!r}"',
     '                for word in ():\n                    if word in low:\n                        return f"post: {slug}/{pid}: a note mentions {word!r}"'),
    ("readfix: verify_post empty-ladder sweep is disabled", "readfix", PROMOTE,
     '            if not lad:\n                return f"post: {slug}/{pid}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{pid}: no ladder after promote"'),

    # ---- echo ----------------------------------------------------------------------------------
    ("echo: the byte-identical-note refusal is disabled", "echo", PROMOTE,
     '                    if n in whole:', '                    if False:'),
    ("echo: the shared-sentence refusal is disabled", "echo", PROMOTE,
     '                        if s in sent and len(s.split()) >= ECHO_MIN_WORDS:',
     '                        if False:'),
    ("echo: ECHO_MIN_WORDS is raised out of reach", "echo", PROMOTE,
     'ECHO_MIN_WORDS = 10', 'ECHO_MIN_WORDS = 999'),
    ("echo: check_no_shipped_echo is never called", "echo", PROMOTE,
     '    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by, data),\n                    check_no_shipped_echo(batch, data)):',
     '    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by, data),\n                    None):'),
    ("echo: the within-batch duplicate-note refusal is disabled", "echo", PROMOTE,
     '                for n in mine:\n                    if n in seen:', '                for n in mine:\n                    if False:'),

    # ---- schema --------------------------------------------------------------------------------
    ("schema: the advice-coverage check is disabled", "schema", PROMOTE,
     '        if not (own_advice & set(PROSE_FIELDS)):', '        if False:'),
    ("schema: the no-advice-field check is disabled", "schema", PROMOTE,
     '        if not own_advice:', '        if False:'),
    ("schema: the classic-schema expectation is disabled", "schema", PROMOTE,
     '        if slug in CLASSIC_SCHEMA_CROPS and "organic_treatment_seasoned" not in seen:',
     '        if False:'),
    ("schema: ADVICE_FIELDS is emptied", "schema", PROMOTE,
     'ADVICE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",\n'
     '                 "prevention_beginner", "prevention_seasoned",\n'
     '                 "management_beginner", "management_seasoned")',
     'ADVICE_FIELDS = ()'),
    ("schema: check_schema_coverage is not called by the twins check", "schema", PROMOTE,
     '    problem = check_schema_coverage(by)\n    if problem:\n        return problem',
     '    problem = None\n    if problem:\n        return problem'),

    # ---- convention ----------------------------------------------------------------------------
    ("convention: the id-divergence refusal is disabled", "convention", PROMOTE,
     '            if p.get("id") != want:', '            if False:'),
    ("convention: the unknown-name refusal is disabled", "convention", PROMOTE,
     '            if want is None:', '            if False:'),

    # ---- twins ---------------------------------------------------------------------------------
    ("twins: the canonical-prose twin refusal is disabled", "twins", PROMOTE,
     '            if prose_signature(by[a]) == prose_signature(by[b]):', '            if False:'),
    ("twins: the staged-digest twin refusal is disabled", "twins", PROMOTE,
     '            if dg[a] == dg[b]:', '            if False:'),

    # ---- validate ------------------------------------------------------------------------------
    ("validate: the unknown-method refusal is disabled", "validate", PROMOTE,
     '                if m not in cm:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"',
     '                if False:\n                    return f"{crop}/{p.get(\'id\')}#{i}: method {m!r} not in catalog"'),
    ("validate: the tier-order refusal is disabled", "validate", PROMOTE,
     '            if tiers != sorted(tiers):', '            if False:'),
    ("validate: the applies_to refusal is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     '                if False:'),
    ("validate: the identical-registers refusal is disabled", "validate", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', '                if False:'),
    ("validate: the empty-ladder refusal is disabled", "validate", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if False:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"'),
    ("validate: the duplicate-method refusal is disabled", "validate", PROMOTE,
     '                if m in seen:', '                if False:'),
    ("validate: the empty-note refusal is disabled", "validate", PROMOTE,
     '                    if not str(r.get(k) or "").strip():', '                    if False:'),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     '        if n != EXPECTED_RUNGS[slug]:', '        if False:'),
    ("validate: the expected-rung table is zeroed", "validate", PROMOTE,
     'EXPECTED_RUNGS = {"broad-beans-fava": 33, "brussels-sprouts": 49, "parsley": 23}',
     'EXPECTED_RUNGS = {"broad-beans-fava": 0, "brussels-sprouts": 0, "parsley": 0}'),

    # ---- blast ---------------------------------------------------------------------------------
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', '    if False:'),
    ("blast: the methods-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', '    if False:'),
    ("blast: bystander crops stop being compared", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', '        if False:'),
    ("blast: the whole-catalog comparison is disabled", "blast", PROMOTE,
     '        if post["methods"][key] != before:', '        if False:'),
    ("blast: the sources comparison is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', '    if False:'),
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()',
     'def apply_to(data):\n    next(c for c in data["crops"] if c["slug"] == "cabbage")["name"] = "MUTATED"\n    batch = staged()'),
    ("blast: apply_to also edits the catalog", "blast", PROMOTE,
     'def apply_to(data):\n    batch = staged()\n    by = {c.get("slug"): c for c in data["crops"]}',
     'def apply_to(data):\n    batch = staged()\n    data["control_methods"]["crop_rotation"]["best_use"] = "MUTATED"\n    by = {c.get("slug"): c for c in data["crops"]}'),

    # ---- mechanics -----------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to stops writing the ladders", PROMOTE,
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
            bad.append(f"  {n}x  {label}\n        anchor: {old[:78]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_batch12_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch12_fall_finishers")
    for fn in os.listdir(src_staging):
        if fn.startswith("out_"):
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, {wd!r})\n'
        f'sys.path.insert(1, os.path.join(REPO, "tools"))')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read().replace(
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch12_fall_finishers")',
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
    print("MUTATION HARNESS -- batch 12 FALL FINISHERS (3 crops, 104 rungs, 0 catalog edits)")
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
