#!/usr/bin/env python3
"""mutate_promote_pla625_p3a -- mutation harness for PLA-625 citrus promote 3a (2026-10-16).

One mutation per guard (each switches ONE refusal off in promote_pla625_p3a.py); the suite test named beside it must
redden. Liveness (PLA-215 bar): anchor preflight (each anchor matches exactly once, else HARNESS DEAD), a
MUTATION-APPLIED marker checked on disk, a sentinel that must redden (the suite's pinned post SHA altered), and a
positive control (the whole suite, unmutated, green first). Grading: pytest rc 1 = caught; rc 0 = SURVIVED; rc 5
(nothing collected) and any other rc (a collection or harness error) = BROKEN.
Derived from mutate_promote_pla625_p2 (same driver), with the mutation table rewritten for this promote.
Usage: mutate_promote_pla625_p3a.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
PR, SU = "promote_pla625_p3a.py", "test_promote_pla625_p3a.py"
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
    ("dash", "    if EM_DASH in s or EN_DASH in s:", "    if " + F + ":", "em_dash_in_a_new_clause"),
    ("degree", "    if BARE_DEGREE.search(s):", "    if " + F + ":", "bare_degree_in_a_new_clause"),
    ("cultivar", "    if CULTIVAR.search(s):", "    if " + F + ":", "cultivar_in_a_new_clause"),
    ("roster", '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if " + F + ":", "roster_change"),
    ("top_keys", "    if set(pre) != set(post):", "    if " + F + ":", "top_level_key_change"),
    ("top_values", '        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):', "        if " + F + ":", "top_level_value_change"),
    ("crop_keys", "        if set(pidx[slug]) != set(qidx[slug]):", "        if " + F + ":", "crop_key_added"),
    ("crop_stray", "\n        if stray:", "\n        if " + F + ":", "stray_change_on_a_touched_crop or launch_flag_is_a_stray"),
    ("catalog_lost", '    if set(pre["source_catalog"]) - set(post["source_catalog"]):', "    if " + F + ":", "catalog_lost_id"),
    ("catalog_stray", "\n    if stray:", "\n    if " + F + ":", "catalog_stray"),
    ("scope_mint", '            if op["kind"] != "catalog" or op["path"] not in MINTED:', "            if " + F + ":", "catalog_op_outside_the_ruled_mints"),
    ("scope_crop", '        if op["crop"] not in CROPS:', "        if " + F + ":", "crop_outside_the_five"),
    ("scope_path", '        if not any(p.match(op["path"]) for p in SCOPE):', "        if " + F + ":", "path_outside_the_ruled_scope"),
    ("scope_catalog_kind", '        if op["kind"] == "catalog":\n            refuse(f"op {i}: a catalog op must name <catalog>")', '        if ' + F + ':\n            refuse(f"op {i}: a catalog op must name <catalog>")', "a_catalog_kind_on_a_crop"),
    ("scope_every_crop", '        if not any(op["crop"] == crop for op in ops):', "        if " + F + ":", "a_ruled_crop_with_no_op"),
    ("post_value", '        if compact(got) != compact(op["new"]):', "        if " + F + ":", "post_value_not_new"),
    ("noop", '        if compact(got) == compact(op["old"]):', "        if " + F + ":", "test_noop"),
    ("no_subs", '            if not (isinstance(op["subs"], list) and op["subs"]):', "            if " + F + ":", "prose_without_subs"),
    ("sub_once", "                if not o_sub or derived.count(o_sub) != 1:", "                if " + F + ":", "a_sub_whose_old_is_not_once"),
    ("touched_leaf", '            if derived != op["new"]:', "            if " + F + ":", "touched_leaf_rule"),
    ("prose_empty", '            if not (isinstance(op["new"], str) and op["new"].strip()):', "            if " + F + ":", "prose_emptied"),
    ("subs_non_prose", '        elif op["subs"] is not None:', "        elif " + F + ":", "subs_on_a_non_prose_op"),
    ("dup_row", "        if key in seen:", "        if " + F + ":", "duplicate_row"),
    ("row_unstaged", "        if op is None:\n            refuse(f\"{tag}: not a staged prose op\")", "        if op is None:\n            continue", "row_on_an_unstaged_path"),
    ("row_value", '        if not any(r["value"] == n_sub and n_sub for _o, n_sub in op["subs"]):', "        if " + F + ":", "row_value_not_a_new_substring"),
    ("quote_bytes", "        cached_quote(r, man, evidence_dir, text_cache, tag)", "        pass", "quote_not_in_bytes"),
    ("row_catalog", '        if r["source_id"] not in post["source_catalog"]:', "        if " + F + ":", "row_source_not_in_catalog"),
    ("block_none", "            if anchors is None:", "            if " + F + ":", "cited_at_names_no_block"),
    ("block_anchor", '            if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:', "            if " + F + ":", "cited_row_not_at_the_blocks_anchor"),
    ("block_sources", '            if not srcs or r["source_id"] not in srcs:', "            if " + F + ":", "cited_row_not_in_the_blocks_sources"),
    ("evidence_only", '        elif "evidence-only" not in decided.get((r["crop"], r["entry_id"]), ()):', "        elif " + F + ":", "evidence_only_without_its_decision"),
    ("clause_evidence", "            if n_sub and (crop, path, n_sub) not in rows_for:", "            if " + F + ":", "a_new_clause_without_evidence"),
    ("deletion_decision", '            if not n_sub and "deleted" not in decided.get((crop, path), ()):', "            if " + F + ":", "a_deletion_without_its_decision"),
    ("ids_diverge", "        if srcs is None or anchors is None or set(srcs) != set(anchors):", "        if " + F + ":", "sources_and_anchors_diverge"),
    ("ids_twice", "        if len(srcs) != len(set(srcs)):", "        if " + F + ":", "a_source_listed_twice"),
    ("rekey_row", '                if not m or m.group(2) != to:', "                if " + F + ":", "a_rekey_row_that_names_no_from"),
    ("rekey_url", '            if frm not in oanchors or to not in anchors or oanchors[frm].get("url") != anchors[to].get("url"):', "            if " + F + ":", "a_rekey_that_moves_the_url"),
    ("added_used", '            if sid in used or "kept" in decs(sid):\n                n["ids_added"] += 1\n            else:', '            if True:\n                n["ids_added"] += 1\n            else:', "an_added_id_with_no_evidenced_clause"),
    ("removed_decision", '            if "cg009-off" not in decs(sid) or "CG009" not in (old_t[sid].get("url") or ""):', "            if " + F + ":", "an_id_removed_without_a_decision"),
    ("moved_url", '            if anchors[sid]["url"] != old_t[sid]["url"] and "repoint" not in decs(sid):', "            if " + F + ":", "a_url_moved_without_a_repoint"),
    ("ladder_where", '        if (op["crop"], op["path"]) != (crop, f"{blk}.control_ladder"):', "        if " + F + ":", "a_ladder_op_off_the_ruled_entry"),
    ("ladder_rung", "        if len(new) != len(old) - 1 or len(gone) != 1 or [r for r in old if r is not gone[0]] != new:", "        if " + F + ":", "the_wrong_rung_removed or rungs_reordered"),
    ("record_only", '        if "record-only" not in decided.get((op["crop"], op["path"]), ()):', "        if " + F + ":", "record_without_a_record_only_row"),
    ("finding_ids", '        if [f["id"] for f in old] != [f["id"] for f in new]:', "        if " + F + ":", "findings_reordered"),
    ("finding_noted", '            if (op["crop"], f_new["id"]) not in NOTED:', "            if " + F + ":", "another_finding_touched"),
    ("finding_keys", '            if set(f_new) - set(f_old) != {"progress_note"} or set(f_old) - set(f_new):', "            if " + F + ":", "a_finding_field_other_than_the_note_added"),
    ("finding_status", '            if compact({k: v for k, v in f_new.items() if k != "progress_note"}) != compact(f_old):', "            if " + F + ":", "the_finding_resolved_instead_of_noted"),
    ("finding_note_empty", '            if not (f_new["progress_note"] or "").strip() or PENDING in f_new["progress_note"]:', "            if " + F + ":", "an_empty_progress_note"),
    ("catalog_id", '        if not isinstance(new, dict) or new.get("id") != op["path"]:', "        if " + F + ":", "a_minted_ids_id_is_its_path"),
    ("catalog_titled", '        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):', "        if " + F + ":", "a_minted_id_must_be_titled"),
    ("catalog_t1", '        if new.get("tier") != "T1":', "        if " + F + ":", "a_minted_id_must_be_t1"),
    ("catalog_cited", '                not (anchored and all(u in man_urls for u in anchored)):', "                " + F + ":", "a_minted_id_must_be_cited or a_minted_anchor_only_id_needs"),
    ("gone", "            if g in _value(qidx[crop], path):", "            if " + F + ":", "a_ruled_string_survives"),
    ("cg009_key", '        if list(cg) != [CG009_ID] or cg[CG009_ID].get("note") != CG009_NOTE:', "        if " + F + ":", "cg009_without_its_scope_note or cg009_left_under_another_key"),
    ("splash", '    if any(r.get("method") == "splash_barrier_mulch" for r in on_br.get("control_ladder") or []):', "    if " + F + ":", "splash_rung_left_in"),
    ("br_uc_ipm", '    if (on_br.get("anchoring_urls") or {}).get("uc_ipm", {}).get("url") != BR_UC_IPM:', "    if " + F + ":", "brown_rot_uc_ipm_not_repointed"),
    ("finding_open", '        if f.get("status") != "open" or not f.get("progress_note"):', "        if " + F + ":", "the_finding_note_dropped"),
    ("match_call", '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=HILL_POPULATION)',
     '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=0, refuse=False)', "match_unclassified"),
    ("match_population", "    if res.inspected != HILL_POPULATION:", "    if " + F + ":", "match_population_pinned"),
    ("wcg_rc", "\n            if r.returncode != 0:", "\n            if " + F + ":", "gate_failure"),
    ("wcg_verdicts", "        if passed != len(slugs):", "        if " + F + ":", "gate_count_is"),
    ("gate_all_rc", "\n    if r.returncode != 0:", "\n    if " + F + ":", "gate_all_failure"),
    ("gate_all_population", "    if not m or int(m.group(1)) != certified or certified == 0:", "    if " + F + ":", "gate_all_population"),
]
SENTINEL = (SU, 'POST_SHA = "d52c261a', 'POST_SHA = "00000000', "real_stage_promotes")


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
    tmp = tempfile.mkdtemp(prefix="mut_pla625p3a_")
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
