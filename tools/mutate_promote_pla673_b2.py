#!/usr/bin/env python3
"""mutate_promote_pla673_b2 -- mutation harness for the PLA-673 part B2 promote (2026-10-06).

One mutation per guard (each switches ONE refusal off in promote_pla673_b2.py); the suite test named beside it must
redden. Liveness (PLA-215 bar): anchor preflight (each anchor matches exactly once, else HARNESS DEAD), a
MUTATION-APPLIED marker checked on disk, a sentinel that must redden (the suite's pinned post SHA altered), and a
positive control (the whole suite, unmutated, green first). Grading: pytest rc 1 = caught; rc 0 = SURVIVED; rc 5
(nothing collected) and any other rc (a collection or harness error) = BROKEN.
Derived from mutate_promote_pla673_glossary (same driver), with the mutation table rewritten for this promote.
Usage: mutate_promote_pla673_b2.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
PR, SU = "promote_pla673_b2.py", "test_promote_pla673_b2.py"
F = "False"

MUTATIONS = [  # (name, anchor, replacement, the test that must redden); a leading \n pins the indentation
    ("wrong_base", "    if got != BASE_SHA:", "    if " + F + ":", "wrong_base"),
    ("empty_stage", "    if not isinstance(ops, list) or not ops:", "    if " + F + ":", "empty_stage"),
    ("op_keys", "        if not isinstance(op, dict) or set(op) != OP_KEYS:", "        if " + F + ":", "op_keys_must_be_exact"),
    ("unknown_kind", '        if op["kind"] not in KINDS:', "        if " + F + ":", "unknown_kind"),
    ("empty_reason", '        if not (isinstance(op["reason"], str) and op["reason"].strip()):', "        if " + F + ":", "empty_reason"),
    ("dup_op", "    if dup:", "    if " + F + ":", "staged_twice"),
    ("not_a_crop", '        if op["crop"] != CATALOG and op["crop"] not in idx:', "        if " + F + ":", "not_a_crop"),
    ("drifted_base", '        if compact(got) != compact(op["old"]):', "        if " + F + ":", "drifted_base"),
    ("prose_type", "    if not (isinstance(s, str) and s.strip()):", "    if " + F + ":", "null_prose"),
    ("dash", "    if EM_DASH in s or EN_DASH in s:", "    if " + F + ":", "em_dash"),
    ("degree", "    if BARE_DEGREE.search(s):", "    if " + F + ":", "bare_degree"),
    ("roster", '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if " + F + ":", "roster_change"),
    ("top_keys", "    if set(pre) != set(post):", "    if " + F + ":", "top_level_key_change"),
    ("top_values", '        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):', "        if " + F + ":", "top_level_value_change"),
    ("crop_stray", "\n        if stray:", "\n        if " + F + ":", "stray_crop_change"),
    ("catalog_stray", "\n    if stray:", "\n    if " + F + ":", "catalog_stray"),
    ("post_value", '        if compact(got) != compact(op["new"]):', "        if " + F + ":", "post_value_not_new"),
    ("noop", '        if compact(got) == compact(op["old"]):', "        if " + F + ":", "noop"),
    ("decision_crop", '        if d["crop"] not in (CATALOG, "<roster>") and d["crop"] not in pidx:', "        if " + F + ":", "decision_on_a_crop"),
    ("cited_at", '        if op["kind"] == "prose" and op["cited_at"] is None and \\', "        if " + F + " and \\", "prose_without_cited_at"),
    ("dup_row", "        if key in seen:", "        if " + F + ":", "duplicate_row"),
    ("row_unstaged", '        if op is None or op["kind"] != "prose":', "        if " + F + ":", "row_on_an_unstaged_path"),
    ("quote_bytes", "        cached_quote(r, man, evidence_dir, text_cache, tag)", "        pass", "quote_not_in_bytes"),
    ("url_cited", '        if r["url"] not in cited_urls(crop):', "        if " + F + ":", "url_not_cited_on_crop"),
    ("block_anchor", '            if (blk.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:', "            if " + F + ":", "block_anchor_missing or soil_prep_block_carries"),
    ("block_sources", '            if "sources" in blk and r["source_id"] not in blk["sources"]:', "            if " + F + ":", "block_sources_missing"),
    ("prose_evidence", '        if op["kind"] == "prose" and op["new"] is not None and (op["crop"], op["path"]) not in rows_for:', "        if " + F + ":", "prose_without_evidence"),
    ("anchor_used", '            if sid not in used and "kept" not in decided.get((op["crop"], f"{op[\'path\']}.{sid}"), ()):', "            if " + F + ":", "unused_unkept_anchor"),
    ("ids_diverge", '            if blk is not None and "sources" in blk and set(blk["sources"]) != set(blk.get("anchoring_urls") or {}):', "            if " + F + ":", "sources_and_anchors_diverge"),
    ("cat_id", '        if not isinstance(new, dict) or new.get("id") != op["path"]:', "        if " + F + ":", "catalog_id_must_match"),
    ("cat_evidence", '        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):', "        if " + F + ":", "catalog_mint_must_be_evidenced"),
    ("register_twin", "                if (crop, twin) not in edited:", "                if " + F + ":", "seasoned_without_its_beginner"),
    ("register_identical", "                if _value(qidx[crop], path) == _value(qidx[crop], twin):", "                if " + F + ":", "byte_identical_registers"),
    ("spacing", '        if path.startswith("soil_prep_") and path in set(spacing_strings(qidx[crop])):', "        if " + F + ":", "soil_prep_restating_spacing"),
    ("match_call", '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=HILL_POPULATION)',
     '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=0, refuse=False)', "match_unclassified"),
    ("match_population", "    if res.inspected != HILL_POPULATION:", "    if " + F + ":", "match_population_pinned"),
    ("wcg_rc", "\n            if r.returncode != 0:", "\n            if " + F + ":", "gate_failure"),
    ("wcg_verdicts", "        if passed != len(slugs):", "        if " + F + ":", "gate_count_is"),
    ("gate_all_rc", "\n    if r.returncode != 0:", "\n    if " + F + ":", "gate_all_failure"),
    ("gate_all_population", "    if not m or int(m.group(1)) != certified or certified == 0:", "    if " + F + ":", "gate_all_population"),
]
SENTINEL = (SU, 'POST_SHA = "aaf004a2', 'POST_SHA = "00000000', "real_stage_promotes")


def run_driver(tools, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, SU), "-q", "-x", "--no-header",
           "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new + "  " + MARKER if not new.endswith("\\") else
                                                       new[:-1] + "\\", 1))
    if new.endswith("\\"):           # a continued line cannot carry a trailing comment: mark the file instead
        with open(p, "a", encoding="utf-8") as f:
            f.write("\n" + MARKER + "\n")
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_pla673b2_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging", "batches"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        src = open(os.path.join(tools, PR), encoding="utf-8").read()
        bad = [m[0] for m in muts if src.count(m[1]) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        rc, out = run_driver(tools, None)
        if rc != 0:
            print(out[-2000:])
            sys.exit(f"HARNESS DEAD: the unmutated suite is already failing (rc {rc})")
        print("positive control: the WHOLE suite, unmutated, is GREEN")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc != 1:
            sys.exit(f"HARNESS DEAD: the sentinel did not redden as a test failure (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, old, new, sel in muts:
            clean, err = apply(tools, PR, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, out = run_driver(tools, sel)
            open(os.path.join(tools, PR), "w", encoding="utf-8").write(clean)
            if rc == 1:
                caught.append(name); print(f"  caught   {name}")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  (-k {sel})")
            else:
                broken.append(name); print(f"  BROKEN   {name}: rc {rc} (-k {sel})\n{out[-600:]}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
