#!/usr/bin/env python3
"""Mutation harness for the batch-14 promote (PLA-215).

`conventional` attacks the two-ladders-both-materials scoping (drop a required rung, widen the
earning set, disable either direction). `premise` attacks the mancozeb-present base check and the
Erwinia bacterial-wilt reuse premise. `alignment` attacks the identical-prose correspondence and
the melon crop-neutrality rule. `scoping` attacks the trap, tillage, copper and forbidden-method
refusals. `ids`, `echo`, `validate`, `blast`, `mechanics` as in batch 13.

Every disabled branch has a driver asserting its ONE specific message.
Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch14.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch14.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- conventional ---------------------------------------------------------------------------
    ("conventional: the required-materials loop runs over nothing", "conventional", PROMOTE,
     "    for slug, pid in CONVENTIONAL_ON:\n        ms, _p = ladder_of(batch[slug], pid)",
     "    for slug, pid in ():\n        ms, _p = ladder_of(batch[slug], pid)"),
    ("conventional: the outside-the-two refusal is disabled in check", "conventional", PROMOTE,
     "            for m in CONVENTIONALS:\n                if m in lad and (slug, pid) not in CONVENTIONAL_ON:\n"
     "                    return (f\"{slug}/{pid} carries {m!r}, but only the two ladders whose prose \"",
     "            for m in ():\n                if m in lad and (slug, pid) not in CONVENTIONAL_ON:\n"
     "                    return (f\"{slug}/{pid} carries {m!r}, but only the two ladders whose prose \""),
    ("conventional: the earning set widens to a third ladder", "conventional", PROMOTE,
     'CONVENTIONAL_ON = (("cantaloupe", "alternaria-leaf-blight"), ("watermelon", "anthracnose"))',
     'CONVENTIONAL_ON = (("cantaloupe", "alternaria-leaf-blight"), ("watermelon", "anthracnose"),\n'
     '                   ("honeydew-melon", "gummy-stem-blight"))'),
    ("conventional: verify_post stops policing the two", "conventional", PROMOTE,
     "            for m in CONVENTIONALS:\n                if m in lad and (slug, pid) not in CONVENTIONAL_ON:\n"
     "                    return f\"post: {slug}/{pid} shipped {m!r} outside the two earning ladders\"",
     "            for m in ():\n                if m in lad and (slug, pid) not in CONVENTIONAL_ON:\n"
     "                    return f\"post: {slug}/{pid} shipped {m!r} outside the two earning ladders\""),
    ("conventional: the copper scoping is disabled", "conventional", PROMOTE,
     '            if "copper_fungicide" in lad and (slug, pid) not in COPPER_ON:\n'
     '                return (f"{slug}/{pid} carries copper,',
     '            if False:\n'
     '                return (f"{slug}/{pid} carries copper,'),

    # ---- premise --------------------------------------------------------------------------------
    ("premise: the mancozeb base check is disabled", "premise", PROMOTE,
     '    if "mancozeb" not in cm:', "    if False:"),
    ("premise: the Erwinia check is disabled", "premise", PROMOTE,
     '                if "erwinia" not in blob:', "                if False:"),
    ("premise: the wilt premise inspects only one melon", "premise", PROMOTE,
     '    for slug in ("cantaloupe", "honeydew-melon"):', '    for slug in ("cantaloupe",):'),

    # ---- alignment ------------------------------------------------------------------------------
    ("alignment: the pairwise loop runs over nothing", "alignment", PROMOTE,
     "    for i, (s1, id1, a1, l1) in enumerate(rows):",
     "    for i, (s1, id1, a1, l1) in enumerate(()):"),
    ("alignment: the fork direction is disabled", "alignment", PROMOTE,
     "            if id1 == id2 and a1 == a2 and l1 != l2:", "            if False:"),
    ("alignment: the copied-ladder direction is disabled", "alignment", PROMOTE,
     "            if l1 == l2 and a1 != a2:", "            if False:"),
    ("alignment: the crop-neutrality scan runs over nothing", "alignment", PROMOTE,
     "                for w in MELON_NAMES:", "                for w in ():"),
    ("alignment: the shared-pid set is emptied", "alignment", PROMOTE,
     'MELON_SHARED_PIDS = ("aphids", "spider-mites", "squash-bug", "powdery-mildew", "downy-mildew",\n'
     '                     "gummy-stem-blight")',
     'MELON_SHARED_PIDS = ()\n_UNUSED_SHARED = ("aphids", "spider-mites", "squash-bug", "powdery-mildew", "downy-mildew",\n'
     '                     "gummy-stem-blight")'),

    # ---- scoping --------------------------------------------------------------------------------
    ("scoping: the unearned-trap refusal is disabled", "scoping", PROMOTE,
     '            if "trap_cropping" in lad and (slug, pid) not in TRAP_OK:\n'
     '                return (f"{slug}/{pid} carries trap_cropping, which only okra',
     '            if False:\n'
     '                return (f"{slug}/{pid} carries trap_cropping, which only okra'),
    ("scoping: the trap attribution requirement is disabled", "scoping", PROMOTE,
     "            if ATTRIBUTION not in blob:", "            if False:"),
    ("scoping: the trap cautions pointer requirement is disabled", "scoping", PROMOTE,
     "            if CAUTIONS_POINTER not in blob:", "            if False:"),
    ("scoping: the tillage bound is disabled in check", "scoping", PROMOTE,
     '            if "off_season_tillage" in lad and pid not in TILLAGE_OK_PIDS:\n'
     '                return (f"{slug}/{pid} carries off_season_tillage, earned only',
     '            if False:\n'
     '                return (f"{slug}/{pid} carries off_season_tillage, earned only'),
    ("scoping: the forbidden-method sweep runs over nothing", "scoping", PROMOTE,
     "            for m, why in FORBIDDEN_METHODS.items():", "            for m, why in {}.items():"),
    ("scoping: the no-material loop in check runs over nothing", "scoping", PROMOTE,
     "    for slug, pid in NO_MATERIAL:\n        ms, _p = ladder_of(batch[slug], pid)\n"
     "        if ms is None:\n            return f\"{slug} has no {pid} problem\"\n        cm = data[\"control_methods\"]",
     "    for slug, pid in ():\n        ms, _p = ladder_of(batch[slug], pid)\n"
     "        if ms is None:\n            return f\"{slug} has no {pid} problem\"\n        cm = data[\"control_methods\"]"),
    ("scoping: the no-material loop in verify_post runs over nothing", "scoping", PROMOTE,
     "    for slug, pid in NO_MATERIAL:\n        ms, _p = ladder_of(by[slug], pid)",
     "    for slug, pid in ():\n        ms, _p = ladder_of(by[slug], pid)"),

    # ---- ids ------------------------------------------------------------------------------------
    ("ids: the convention check is disabled", "ids", PROMOTE,
     '            if p.get("id") != want:', "            if False:"),
    ("ids: the reuse-resolves premise is disabled", "ids", PROMOTE,
     "        if pid in staged_ids and pid not in base_ids:", "        if False:"),
    ("ids: the new-id-free premise is disabled", "ids", PROMOTE,
     "        if pid in base_ids:\n            return f\"{pid!r} is already on the roster",
     "        if False:\n            return f\"{pid!r} is already on the roster"),
    ("ids: the shipped-new-ids check is disabled", "ids", PROMOTE,
     "    for pid in NEW_IDS:\n        if pid not in shipped:", "    for pid in ():\n        if pid not in shipped:"),

    # ---- echo -----------------------------------------------------------------------------------
    ("echo: the scan compares against an empty shipped corpus", "echo", PROMOTE,
     "    whole, sent = shipped_notes(data)\n    for slug in CROPS:",
     "    whole, sent = {}, {}\n    for slug in CROPS:"),
    ("echo: the sentence threshold is raised out of reach", "echo", PROMOTE,
     "                        if s in sent and len(s.split()) >= 10:",
     "                        if s in sent and len(s.split()) >= 1000:"),

    # ---- validate -------------------------------------------------------------------------------
    ("validate: the duplicate-method check is disabled", "validate", PROMOTE,
     "                if m in seen:", "                if False:"),
    ("validate: the identical-registers check is disabled", "validate", PROMOTE,
     '                if r["note_beginner"] == r["note_seasoned"]:', "                if False:"),
    ("validate: the tier-monotonicity check is disabled", "validate", PROMOTE,
     "            if tiers != sorted(tiers):", "            if False:"),
    ("validate: the applies_to coherence check is disabled", "validate", PROMOTE,
     '                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):',
     "                if False:"),
    ("validate: the hygiene sweep runs over nothing", "validate", PROMOTE,
     '                for k in ("note_beginner", "note_seasoned"):\n'
     '                    bad = hygiene(r[k])',
     '                for k in ():\n'
     '                    bad = hygiene(r[k])'),
    ("validate: the per-crop rung-count check is disabled", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[slug]:", "        if False:"),

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
    wd = tempfile.mkdtemp(prefix="mutate_batch14_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", "pla8_batch14_okra_tomatillo_melons")
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
        'STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch14_okra_tomatillo_melons")',
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
    print("MUTATION HARNESS -- PLA-8 batch 14, okra + tomatillo + the melons")
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
