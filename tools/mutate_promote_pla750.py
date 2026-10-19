#!/usr/bin/env python3
"""mutate_promote_pla750 -- proof that test_promote_pla750 catches a regression in every guard family of
tools/promote_pla750.py.

Each mutation disables one guard in a scratch copy of tools/ (the promote edited there, everything else
byte-identical, the stage and the evidence cache read from the real tree), then runs the suite with -x. A
mutation must turn the suite RED.

LIVENESS (PLA-215 convention items 2 and 3):
  * POSITIVE CONTROL  the unmutated scratch copy passes the whole suite.
  * MUTATION-APPLIED  every mutation's `old` text occurs exactly once and the staged source differs.
  * SENTINEL          a check_post that returns before any guard must redden, or HARNESS DEAD.

Usage: python3 tools/mutate_promote_pla750.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = os.path.join(HERE, "promote_pla750.py")
SUITE = "test_promote_pla750.py"

MUTATIONS = [
    ("B-roster", "the roster check is off",
     '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if False:"),
    ("B-stray", "a leaf changed outside the staged ops passes",
     "        if stray:\n            refuse(f\"{slug}: changed outside the staged ops", "        if False:\n            refuse(f\"{slug}: changed outside the staged ops"),
    ("B-catalog-gain", "the catalog may gain any id",
     "    if set(post[\"source_catalog\"]) - set(pre[\"source_catalog\"]) != set(MINTED):", "    if False:"),
    ("B-catalog-edit", "an existing catalog entry may change",
     '        if compact(pre["source_catalog"][sid]) != compact(post["source_catalog"][sid]):', "        if False:"),
    ("S-crops", "an op outside the 30 crops passes",
     '        if op["crop"] not in CROPS:', "        if False:"),
    ("S-paths", "an op outside its path family passes",
     '        if not PATHS[op["kind"]].match(op["path"]):', "        if False:"),
    ("S-pause", "a pause op on a held crop passes",
     '        if op["kind"] == "pause" and (op["crop"] not in NOT_HELD', '        if False and (op["crop"] not in NOT_HELD'),
    ("S-enum", "an enum op to another effect passes",
     '        if op["kind"] == "enum" and (op["crop"] not in ENUMS', '        if False and (op["crop"] not in ENUMS'),
    ("S-field", "a ruled crop with no field op passes",
     '        if not any(op["crop"] == crop and op["kind"] == "field" for op in ops):', "        if False:"),
    ("S-pause-set", "a missing pause op passes",
     '        if (crop in NOT_HELD) != any(op["crop"] == crop and op["kind"] == "pause" for op in ops):', "        if False:"),
    ("V-noop", "a no-op passes",
     '        if compact(got) == compact(op["old"]):', "        if False:"),
    ("T-leaf", "new need not be old with the subs",
     '            if derived != op["new"] or not op["new"].strip():', "            if False:"),
    ("T-count", "a sub whose old text is missing passes",
     "                if not o_sub or derived.count(o_sub) != 1:", "                if False:"),
    ("P-prose", "prose rules are not applied to new clauses",
     "                if n_sub:\n                    _prose_ok(n_sub, tag)", "                if False:\n                    _prose_ok(n_sub, tag)"),
    ("E-rows", "a cited clause with no evidence row passes",
     "            if not rows:\n                refuse(f\"{tag}: a new clause with no EVIDENCE row\")", "            if False:\n                refuse(f\"{tag}: a new clause with no EVIDENCE row\")"),
    ("E-bytes", "evidence quotes are not checked against the hashed bytes",
     "        cached_quote(r, man, evidence_dir, tc, tag)\n", "        pass\n"),
    ("E-anchor", "an evidence row at an unanchored url passes",
     '                if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:', "                if False:"),
    ("E-struck", "a struck edit may add words",
     "                    if not _is_deletion(o_sub, n_sub):", "                    if False:"),
    ("E-decision", "an uncited edit needs no decision",
     '                if "evidence-only" not in dset:', "                if False:"),
    ("E-tip-ev", "a new tip's source needs no evidence",
     '                if not any(r["source_id"] == sid and r["url"] == t["anchoring_urls"][sid]["url"] for r in rows):',
     "                if False:"),
    ("E-tip-one", "a tip_add may append more than one tip",
     '            if len(new) != len(old) + 1 or compact(new[:-1]) != compact(old):', "            if False:"),
    ("E-tip-prose", "new tip text skips the prose rules",
     '                _prose_ok(t[k], f"{tag} {k}")', "                pass"),
    ("E-anchor-ev", "an added anchor needs no evidence",
     "                if not hits:\n                    refuse(f\"{tag}: added id {sid} supports no EVIDENCE row at {url}\")",
     "                if False:\n                    refuse(f\"{tag}: added id {sid} supports no EVIDENCE row at {url}\")"),
    ("F-population", "the held / not-held split is not checked",
     "    if sorted(held) != sorted(HELD) or sorted(nulls) != sorted(NOT_HELD):", "    if False:"),
    ("F-gate", "sowing_heat_ceiling_gate is not run on the post roster",
     "    if v:\n        refuse(f\"sowing_heat_ceiling_gate on the post roster: {v[:4]}\")",
     "    if False:\n        refuse(f\"sowing_heat_ceiling_gate on the post roster: {v[:4]}\")"),
    ("N-climate", "climate_threshold_gate (incl. STALE) is not run on the post roster",
     "    if cv:\n        refuse(f\"climate_threshold_gate on the post roster: {cv[:4]}\")",
     "    if False:\n        refuse(f\"climate_threshold_gate on the post roster: {cv[:4]}\")"),
    ("D-one", "a trigger_drop may remove more than one trigger",
     "            if len(new) != len(old) - 1 or len(gone) != 1 or [x for x in old if x is not gone[0]] != new:",
     "            if False:"),
    ("D-ruled", "any trigger may be dropped",
     '            if key is None or "struck" not in', '            if False and "struck" not in'),
    ("C-tier", "a non-T1 mint passes",
     '        if not isinstance(new, dict) or new.get("id") != op["path"] or new.get("tier") != "T1":', "        if False:"),
    ("C-scope", "a bare-host or untitled mint passes",
     '        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):',
     "        if False:"),
    ("pin", "the base SHA pin is not enforced",
     "    if got != BASE_SHA:", "    if False:"),
    ("pre", "check_pre does not compare the base to `old`",
     '        if compact(got) != compact(op["old"]):\n            refuse(f"op {i} {op[\'crop\']} {op[\'path\']}: the base value',
     '        if False:\n            refuse(f"op {i} {op[\'crop\']} {op[\'path\']}: the base value'),
]
SENTINEL = ("SENTINEL: check_post returns before any guard",
            '    pidx, qidx = by_slug(pre), by_slug(post)\n    # guard B\n',
            '    pidx, qidx = by_slug(pre), by_slug(post)\n    return n\n    # guard B\n')


def run_suite(src, xfirst=True):
    with tempfile.TemporaryDirectory() as td:
        tools = os.path.join(td, "tools")
        shutil.copytree(HERE, tools, ignore=shutil.ignore_patterns(".evidence_cache", ".doc_cache", "staging",
                                                                   "__pycache__", ".pytest_cache"))
        with open(os.path.join(tools, "promote_pla750.py"), "w", encoding="utf-8") as fh:
            fh.write(src)
        os.symlink(os.path.join(HERE, "staging"), os.path.join(tools, "staging"))
        os.symlink(os.path.join(HERE, ".evidence_cache"), os.path.join(tools, ".evidence_cache"))
        os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(td, "crops_data_final.json"))
        os.symlink(os.path.join(REPO, ".git"), os.path.join(td, ".git")) if os.path.isdir(os.path.join(REPO, ".git")) \
            else shutil.copy(os.path.join(REPO, ".git"), os.path.join(td, ".git"))
        args = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + (["-x"] if xfirst else []) + \
               [os.path.join(tools, SUITE)]
        r = subprocess.run(args, capture_output=True, text=True, cwd=td)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]


def stage(orig, old, new, label):
    if orig.count(old) != 1:
        raise SystemExit(f"HARNESS DEAD: {label}: the mutation's text occurs {orig.count(old)} times in the promote")
    src = orig.replace(old, new)
    if src == orig:
        raise SystemExit(f"HARNESS DEAD: {label}: MUTATION-APPLIED marker failed (source unchanged)")
    return src


def main():
    orig = open(PROMOTE, encoding="utf-8").read()
    for _f, label, old, new in MUTATIONS:      # liveness of every injection before spending any suite time
        stage(orig, old, new, label)
    stage(orig, SENTINEL[1], SENTINEL[2], SENTINEL[0])
    rc, tail = run_suite(orig, xfirst=False)
    if rc != 0:
        print(f"HARNESS DEAD: positive control is RED on the unmutated promote: {tail}")
        return 1
    print(f"positive control : GREEN ({tail[0] if tail else ''})")
    label, old, new = SENTINEL
    rc, tail = run_suite(stage(orig, old, new, label))
    if rc == 0:
        print(f"HARNESS DEAD: {label} did not redden the suite")
        return 1
    print(f"sentinel         : REDDENS ({tail[0] if tail else ''})\n")
    caught = survived = 0
    for family, label, old, new in MUTATIONS:
        rc, tail = run_suite(stage(orig, old, new, label))
        if rc == 0:
            survived += 1
            print(f"  SURVIVED  [{family:14s}] {label}", flush=True)
        else:
            caught += 1
            print(f"  caught    [{family:14s}] {label}  ({tail[0] if tail else ''})", flush=True)
    print(f"\nTOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS -- every guard family of promote_pla750 reddens the suite when broken.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
