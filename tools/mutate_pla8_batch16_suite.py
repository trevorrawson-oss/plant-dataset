#!/usr/bin/env python3
"""Mutation harness for the batch-16 promote (PLA-215).

`inversion` attacks the companion-inversion guards (the batch-wide trap refusal, the banned-note
scan now including "decoy", the required lure-trap anti-recommendation on echinacea's beetle
rung). `schema` attacks the note-pair premise. `taxon`/`ids` attack the sweet-pea refusal, the
convention table, the roster premises and the new-id-shipped check verify_post carries because
(unlike batch 15) only one new id doubles as a per-id lookup key. `alignment` includes the
identical-prose direction, driven for the first time this arc. `materials` covers the per-ladder
MATERIAL_OK scoping. `echo`, `validate`, `blast`, `mechanics` as in batches 13-15.

Every disabled branch has a driver asserting its ONE specific message.
Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch16.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch16.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- inversion ------------------------------------------------------------------------------
    ("inversion: trap_cropping leaves the forbidden table", "inversion", PROMOTE,
     '    "trap_cropping": "the companion inversion holds for this batch too",\n', ''),
    ("inversion: the banned-note scan in check runs over nothing", "inversion", PROMOTE,
     "                for word in NOTE_BANNED:\n                    if word in blob:\n"
     "                        return (f\"{slug}/{pid}: a note mentions {word!r}. The companion \"",
     "                for word in ():\n                    if word in blob:\n"
     "                        return (f\"{slug}/{pid}: a note mentions {word!r}. The companion \""),
    ("inversion: the banned-note scan in verify_post runs over nothing", "inversion", PROMOTE,
     "                for word in NOTE_BANNED:\n                    if word in blob:\n"
     "                        return f\"post: {slug}/{pid}: a shipped note mentions {word!r}\"",
     "                for word in ():\n                    if word in blob:\n"
     "                        return f\"post: {slug}/{pid}: a shipped note mentions {word!r}\""),
    ("inversion: the banned vocabulary is emptied", "inversion", PROMOTE,
     'NOTE_BANNED = ("trap crop", "trap-crop", "sacrificial", "banker", "decoy")',
     'NOTE_BANNED = ()\n_UNUSED_BANNED = ("trap crop", "trap-crop", "sacrificial", "banker", "decoy")'),
    ("inversion: the lure-trap requirement in check is disabled", "inversion", PROMOTE,
     '        if "trap" not in blob:\n'
     '            return (f"{slug}/{pid}: the {method} rung dropped the crop\'s own avoid-lure-traps "',
     '        if False:\n'
     '            return (f"{slug}/{pid}: the {method} rung dropped the crop\'s own avoid-lure-traps "'),
    ("inversion: the lure-trap requirement in verify_post is disabled", "inversion", PROMOTE,
     '        if "trap" not in blob:\n'
     '            return f"post: {slug}/{pid} shipped without the lure-trap warning"',
     '        if False:\n'
     '            return f"post: {slug}/{pid} shipped without the lure-trap warning"'),
    ("inversion: the lure-warned table is emptied", "inversion", PROMOTE,
     'LURE_WARNED = (("echinacea", "japanese-beetles", "handpick"),)',
     'LURE_WARNED = ()'),
    ("inversion: the lost-rung branch in check is disabled", "inversion", PROMOTE,
     '        if ms is None or method not in ms:\n'
     '            return f"{slug}/{pid} lost its {method} rung"',
     '        if False:\n'
     '            return f"{slug}/{pid} lost its {method} rung"'),
    ("inversion: the lost-rung branch in verify_post is disabled", "inversion", PROMOTE,
     '        if ms is None or method not in ms:\n'
     '            return f"post: {slug}/{pid} shipped without its {method} rung"',
     '        if False:\n'
     '            return f"post: {slug}/{pid} shipped without its {method} rung"'),

    # ---- schema ---------------------------------------------------------------------------------
    ("schema: the note-pair premise is disabled", "schema", PROMOTE,
     '                if not str(p.get(f) or "").strip():\n'
     '                    return (f"{slug}/{p.get(\'name\')!r} has no {f};',
     '                if False:\n'
     '                    return (f"{slug}/{p.get(\'name\')!r} has no {f};'),

    # ---- taxon / ids ----------------------------------------------------------------------------
    ("taxon: the id-convention check is disabled", "taxon", PROMOTE,
     '            if p.get("id") != want:', "            if False:"),
    ("taxon: the table-miss branch is disabled", "taxon", PROMOTE,
     "            if want is None:", "            if False:"),
    ("taxon: the wrong-organism-present branch is disabled", "taxon", PROMOTE,
     "        if wrong in staged_ids:", "        if False:"),
    ("taxon: the required-id branch is disabled", "taxon", PROMOTE,
     "        if right not in staged_ids:", "        if False:"),
    ("taxon: the refusal table is emptied", "taxon", PROMOTE,
     'TAXON_REFUSED = {\n    "root-and-stem-rots": ("root-rots-damping-off",',
     'TAXON_REFUSED = {}\n_UNUSED_TAXON = {\n    "root-and-stem-rots": ("root-rots-damping-off",'),
    ("taxon: verify_post stops policing the wrong string", "taxon", PROMOTE,
     "        if wrong in shipped:", "        if False:"),
    ("ids: the reuse-resolves premise is disabled", "ids", PROMOTE,
     "        if pid in staged_ids and pid not in base_ids:", "        if False:"),
    ("ids: the new-id-free premise is disabled", "ids", PROMOTE,
     '        if pid in base_ids:\n            return f"{pid!r} is already on the roster',
     '        if False:\n            return f"{pid!r} is already on the roster'),
    ("ids: the new-id-shipped check in verify_post is disabled", "ids", PROMOTE,
     '        if pid not in shipped:\n            return f"post: new id {pid!r} did not ship"',
     '        if False:\n            return f"post: new id {pid!r} did not ship"'),

    # ---- alignment ------------------------------------------------------------------------------
    ("alignment: the pairwise loop runs over nothing", "alignment", PROMOTE,
     "    for i, (s1, id1, a1, l1) in enumerate(rows):",
     "    for i, (s1, id1, a1, l1) in enumerate(()):"),
    ("alignment: the identical-prose direction is disabled", "alignment", PROMOTE,
     "            if id1 == id2 and a1 == a2 and l1 != l2:", "            if False:"),
    ("alignment: the copied-ladder direction is disabled", "alignment", PROMOTE,
     "            if l1 == l2 and a1 != a2:", "            if False:"),

    # ---- materials ------------------------------------------------------------------------------
    ("materials: the forbidden-method sweep runs over nothing", "materials", PROMOTE,
     "            for m, why in FORBIDDEN_METHODS.items():\n                if m in lad:\n"
     "                    return f\"{slug}/{pid} carries {m!r}: {why}\"",
     "            for m, why in {}.items():\n                if m in lad:\n"
     "                    return f\"{slug}/{pid} carries {m!r}: {why}\""),
    ("materials: verify_post's forbidden sweep runs over nothing", "materials", PROMOTE,
     "            for m in FORBIDDEN_METHODS:\n                if m in lad:\n"
     "                    return f\"post: {slug}/{pid} shipped forbidden {m!r}\"",
     "            for m in ():\n                if m in lad:\n"
     "                    return f\"post: {slug}/{pid} shipped forbidden {m!r}\""),
    ("materials: the scoping check in check is disabled", "materials", PROMOTE,
     '                if m in cm and cm[m]["tier"] in MATERIAL_TIERS and m not in allowed:\n'
     '                    return (f"{slug}/{pid} carries material {m!r}, which its own note does not "',
     '                if False:\n'
     '                    return (f"{slug}/{pid} carries material {m!r}, which its own note does not "'),
    ("materials: the scoping check in verify_post is disabled", "materials", PROMOTE,
     '                if m in cm and cm[m]["tier"] in MATERIAL_TIERS and m not in allowed:\n'
     '                    return f"post: {slug}/{pid} shipped unearned material {m!r}"',
     '                if False:\n'
     '                    return f"post: {slug}/{pid} shipped unearned material {m!r}"'),
    ("materials: the MATERIAL_OK map is emptied", "materials", PROMOTE,
     'MATERIAL_OK = {\n    ("echinacea", "aphids"): {"insecticidal_soap"},',
     'MATERIAL_OK = {}\n_UNUSED_MATERIAL = {\n    ("echinacea", "aphids"): {"insecticidal_soap"},'),
    ("materials: the material tiers are emptied", "materials", PROMOTE,
     'MATERIAL_TIERS = ("soft_chemical", "conventional")', "MATERIAL_TIERS = ()"),

    # ---- echo -----------------------------------------------------------------------------------
    ("echo: the scan compares against an empty shipped corpus", "echo", PROMOTE,
     "    whole, sent = shipped_notes(data)\n    for slug in CROPS:",
     "    whole, sent = {}, {}\n    for slug in CROPS:"),
    ("echo: the sentence threshold is raised out of reach", "echo", PROMOTE,
     "                        if s in sent and len(s.split()) >= 10:",
     "                        if s in sent and len(s.split()) >= 1000:"),

    # ---- validate -------------------------------------------------------------------------------
    ("validate: the missing-batch-crop check is disabled", "validate", PROMOTE,
     '        if slug not in by:\n            return f"no crop {slug!r} in canonical"',
     '        if False:\n            return f"no crop {slug!r} in canonical"'),
    ("validate: the already-laddered refusal is disabled", "validate", PROMOTE,
     '            if "control_ladder" in p:\n'
     '                return f"{slug} is already laddered; re-laddering changes shipped ids"',
     '            if False:\n'
     '                return f"{slug} is already laddered; re-laddering changes shipped ids"'),
    ("validate: the staged-canonical parity check is disabled", "validate", PROMOTE,
     '        if a != b:\n            return f"{slug}: staged {a} problems, canonical {b}"',
     '        if False:\n            return f"{slug}: staged {a} problems, canonical {b}"'),
    ("validate: the missing-id-or-type check is disabled", "validate", PROMOTE,
     '            if not p.get("id") or not p.get("type"):', "            if False:"),
    ("validate: the none-ladder check is disabled", "validate", PROMOTE,
     "            if lad is None:", "            if False:"),
    ("validate: the empty-ladder check is disabled", "validate", PROMOTE,
     '            if not lad:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"',
     '            if False:\n                return f"{crop}/{p.get(\'id\')}: control_ladder is EMPTY"'),
    ("validate: the catalog-membership check is disabled", "validate", PROMOTE,
     "                if m not in cm:", "                if False:"),
    ("validate: the duplicate-method check is disabled", "validate", PROMOTE,
     "                if m in seen:", "                if False:"),
    ("validate: the identical-registers check is disabled", "validate", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', "                if False:"),
    ("validate: the missing-note check runs over nothing", "validate", PROMOTE,
     '                for k in ("note_beginner", "note_seasoned"):\n'
     '                    if not str(r.get(k) or "").strip():',
     '                for k in ():\n'
     '                    if not str(r.get(k) or "").strip():'),
    ("validate: the hygiene sweep runs over nothing", "validate", PROMOTE,
     '                for k in ("note_beginner", "note_seasoned"):\n'
     '                    bad = hygiene(r[k])',
     '                for k in ():\n'
     '                    bad = hygiene(r[k])'),
    ("validate: the tier-monotonicity check is disabled", "validate", PROMOTE,
     "            if tiers != sorted(tiers):", "            if False:"),
    ("validate: the applies_to coherence check is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     "                if False:"),
    ("validate: the per-crop problem-count check is disabled", "validate", PROMOTE,
     "        if n_prob != EXPECTED_PROBLEMS[crop]:", "        if False:"),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[slug]:", "        if False:"),
    ("validate: verify_post's no-ladder check is disabled", "validate", PROMOTE,
     '            if not lad:\n                return f"post: {slug}/{pid}: no ladder after promote"',
     '            if False:\n                return f"post: {slug}/{pid}: no ladder after promote"'),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: apply_to also edits a bystander crop", "blast", PROMOTE,
     "def apply_to(data):\n    batch = staged()",
     'def apply_to(data):\n    data["crops"][0]["name"] = "MUTATED"\n    batch = staged()'),
    ("blast: the crop-set comparison is disabled", "blast", PROMOTE,
     '    if set(post["crops"]) != set(pre["crops"]):', "    if False:"),
    ("blast: the bystander value check is disabled", "blast", PROMOTE,
     '        if post["crops"][slug] != before:', "        if False:"),
    ("blast: the catalog immutability check is disabled", "blast", PROMOTE,
     '    if post["methods"] != pre["methods"]:', "    if False:"),
    ("blast: the source immutability check is disabled", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the ladders are never attached", PROMOTE,
            '                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])',
            '                _skip = copy.deepcopy(add["control_ladder"])')


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
    wd = tempfile.mkdtemp(prefix="mutate_batch16_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch16_companions_b")
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
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch16_companions_b")',
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
    print("MUTATION HARNESS -- PLA-8 batch 16, companions B")
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
