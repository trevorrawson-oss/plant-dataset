#!/usr/bin/env python3
"""mutate_promote_pla625_p2 -- mutation harness for PLA-625 citrus promote 2 (2026-10-16).

One mutation per guard (each switches ONE refusal off in promote_pla625_p2.py); the suite test named beside it must
redden. Liveness (PLA-215 bar): anchor preflight (each anchor matches exactly once, else HARNESS DEAD), a
MUTATION-APPLIED marker checked on disk, a sentinel that must redden (the suite's pinned post SHA altered), and a
positive control (the whole suite, unmutated, green first). Grading: pytest rc 1 = caught; rc 0 = SURVIVED; rc 5
(nothing collected) and any other rc (a collection or harness error) = BROKEN.
Derived from mutate_promote_pla625_p1 (same driver), with the mutation table rewritten for this promote.
Usage: mutate_promote_pla625_p2.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
PR, SU = "promote_pla625_p2.py", "test_promote_pla625_p2.py"
F = "False"

MUTATIONS = [  # (name, anchor, replacement, the test that must redden); a leading \n pins the indentation
    ("wrong_base", "    if got != BASE_SHA:", "    if " + F + ":", "wrong_base"),
    ("empty_stage", "    if not isinstance(ops, list) or not ops:", "    if " + F + ":", "empty_stage"),
    ("op_keys", "        if not isinstance(op, dict) or set(op) != OP_KEYS:", "        if " + F + ":", "op_keys_must_be_exact"),
    ("unknown_kind", '        if op["kind"] not in KINDS:', "        if " + F + ":", "unknown_kind"),
    ("empty_reason", '        if not (isinstance(op["reason"], str) and op["reason"].strip()):', "        if " + F + ":", "empty_reason"),
    ("dup_op", "    if dup:", "    if " + F + ":", "staged_twice"),
    ("not_a_crop", '        if op["crop"] != CATALOG and op["crop"] not in idx:', "        if " + F + ":", "not_a_crop"),
    ("drifted_base", '        if compact(got) != compact(op["old"]):', "        if " + F + ":", "drifted_base or check_pre_refuses_minting"),
    ("row_append", "            if at is None or at != len(rows):", "            if " + F + ":", "a_new_row_must_append"),
    ("prose_type", "    if not (isinstance(s, str) and s.strip()):", "    if " + F + ":", "null_prose"),
    ("dash", "    if EM_DASH in s or EN_DASH in s:", "    if " + F + ":", "em_dash"),
    ("degree", "    if BARE_DEGREE.search(s):", "    if " + F + ":", "bare_degree"),
    ("cultivar", "    if CULTIVAR.search(s):", "    if " + F + ":", "cultivar"),
    ("lost_row", "    if len(qr) < len(pr):", "    if " + F + ":", "a_lost_row"),
    ("row_leaf_diff", '        diff |= {("rootstock_options", i) + t for t in leaf_diff(pr[i], qr[i])}', "        pass", "stray_edit_on_an_unstaged_row_leaf"),
    ("added_row_diff", '    diff |= {("rootstock_options", i) for i in range(len(pr), len(qr))}', "    pass", "an_unstaged_added_row"),
    ("roster", '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if " + F + ":", "roster_change"),
    ("top_keys", "    if set(pre) != set(post):", "    if " + F + ":", "top_level_key_change"),
    ("top_values", '        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):', "        if " + F + ":", "top_level_value_change"),
    ("crop_keys", "        if set(pidx[slug]) != set(qidx[slug]):", "        if " + F + ":", "crop_key_added"),
    ("crop_stray", "\n        if stray:", "\n        if " + F + ":", "stray_crop_change or launch_flag_is_a_stray"),
    ("catalog_lost", '    if set(pre["source_catalog"]) - set(post["source_catalog"]):', "    if " + F + ":", "catalog_lost_id"),
    ("catalog_stray", "\n    if stray:", "\n    if " + F + ":", "catalog_stray"),
    ("scope_crop", "        if sc is None:", "        if " + F + ":", "crop_outside_the_ruled_scope"),
    ("scope_path", '        if not any(op["path"] == s or op["path"].startswith(s + ".") or op["path"].startswith(s + "[") for s in sc):', "        if " + F + ":", "path_outside_the_ruled_scope or a_rekey_crop_scope"),
    ("scope_rekey_only", '        if (op["crop"] in REKEY_CROPS) != (op["kind"] == "rekey"):', "        if " + F + ":", "a_rekey_crop_takes_rekeys_only"),
    ("scope_catalog", '        if (op["crop"] == CATALOG) != (op["kind"] == "catalog"):', "        if " + F + ":", "a_catalog_op_must_name"),
    ("scope_rows", '        if [r["name"] for r in qidx[crop]["rootstock_options"]] != ROWS[crop]:', "        if " + F + ":", "rows_must_be_the_ruled_list"),
    ("scope_every_crop", '        if not any(op["crop"] == crop for op in ops):', "        if " + F + ":", "a_ruled_crop_with_no_op_but_the_right_rows"),
    ("scope_minted", '    if sorted(op["path"] for op in ops if op["kind"] == "catalog") != sorted(MINTED):', "    if " + F + ":", "catalog_ops_are_exactly"),
    ("post_value", '        if compact(got) != compact(op["new"]):', "        if " + F + ":", "post_value_not_new"),
    ("noop", '        if compact(got) == compact(op["old"]):', "        if " + F + ":", "noop"),
    ("prose_checks", '        if op["kind"] == "prose":\n            _prose_ok(op["new"], tag)', '        if ' + F + ':\n            _prose_ok(op["new"], tag)', "em_dash"),
    ("row_fields", '            if not isinstance(op["new"], dict) or tuple(op["new"]) != ROW_FIELDS:', "            if " + F + ":", "a_new_row_carries_exactly"),
    ("row_prose", '            for f in ROW_PROSE:\n                _prose_ok(op["new"][f], f"{tag}.{f}")', '            for f in ():\n                _prose_ok(op["new"][f], f"{tag}.{f}")', "a_new_rows_prose_is_checked"),
    ("decision_crop", '        if d["crop"] not in (CATALOG, "<roster>") and d["crop"] not in pidx:', "        if " + F + ":", "decision_on_a_crop"),
    ("cited_at", '        if op["kind"] == "prose" and op["cited_at"] is None and \\', "        if " + F + " and \\", "prose_without_cited_at"),
    ("rename_decision", '        if op["kind"] == "rename" and "renamed" not in decided.get((op["crop"], op["path"]), ()):', "        if " + F + ":", "rename_without_a_decision"),
    ("retained_crop", "        if crop not in qidx:", "        if " + F + ":", "retained_on_a_non_crop"),
    ("retained_op", '        if (crop, path) in {(op["crop"], op["path"]) for op in ops}:', "        if " + F + ":", "retained_is_also_an_op"),
    ("retained_moved", "        if compact(_value(pidx[crop], path)) != compact(_value(qidx[crop], path)):", "        if " + F + ":", "retained_value_moved"),
    ("nulled_decision", '            if "nulled" not in decided.get((op["crop"], op["path"]), ()):', "            if " + F + ":", "nulled_without_a_decision"),
    ("new_row_null_value", '                if op["new"][f] is not None:', "                if " + F + ":", "a_new_rows_value_must_be_null"),
    ("new_row_null_decision", '                if "new-null" not in decided.get(leaf, ()):', "                if " + F + ":", "a_new_rows_null_needs_a_decision"),
    ("dup_row", "        if key in seen:", "        if " + F + ":", "duplicate_row"),
    ("nulled_evidence", "        if k in nulled:", "        if " + F + ":", "evidence_for_a_nulled_value"),
    ("row_unstaged", '            refuse(f"{tag}: not a staged prose / value op, a new row\'s prose or a retained leaf")', '            cited_at = _block_of(r["entry_id"])', "row_on_an_unstaged_path"),
    ("quote_bytes", "        cached_quote(r, man, evidence_dir, text_cache, tag)", "        pass", "quote_not_in_bytes"),
    ("url_cited", '        if r["url"] not in cited_urls(crop):', "        if " + F + ":", "url_not_cited_on_crop"),
    ("block_none", "            if anchors is None:", "            if " + F + ":", "cited_at_names_no_block"),
    ("one_url", '            if (anchors.get(r["source_id"]) or {}).get("url") != r["url"]:', "            if " + F + ":", "one_url_per_source_id"),
    ("block_sources", '            if srcs is None or r["source_id"] not in srcs:', "            if " + F + ":", "block_sources_missing"),
    ("op_evidence", '        if op["kind"] in ("prose", "value") and (op["crop"], op["path"]) not in nulled \\', '        if ' + F + ' and (op["crop"], op["path"]) not in nulled \\', "prose_without_evidence or value_without_evidence"),
    ("new_row_evidence", "        if k not in rows_for:", "        if " + F + ":", "a_new_rows_prose_without_evidence"),
    ("retained_evidence", "        if _value(pidx[crop], path) is not None and (crop, path) not in rows_for:", "        if " + F + ":", "retained_value_without_evidence"),
    ("anchor_blocks_rows", '    blocks = {(op["crop"], op["cited_at"]) for op in ops if op["kind"] in ("anchors", "sources", "row")}', '    blocks = {(op["crop"], op["cited_at"]) for op in ops if op["kind"] in ("anchors", "sources")}', "a_new_rows_unused_anchor"),
    ("ids_diverge", "        if srcs is None or anchors is None or set(srcs) != set(anchors):", "        if " + F + ":", "sources_and_anchors_diverge"),
    ("ids_twice", "        if len(srcs) != len(set(srcs)):", "        if " + F + ":", "a_source_listed_twice"),
    ("anchor_used", '            if sid not in used and "kept" not in decided.get((crop_slug, f"{blk}.anchoring_urls.{sid}"), ()):', "            if " + F + ":", "unused_unkept_anchor"),
    ("record_only", '        if "record-only" not in decided.get((op["crop"], op["path"]), ()):', "        if " + F + ":", "record_without_a_record_only_row"),
    ("append_only", "        if len(new) <= len(old) or compact(new[:len(old)]) != compact(old):", "        if " + F + ":", "findings_are_append_only"),
    ("finding_ids", "        if len(ids) != len(set(ids)):", "        if " + F + ":", "a_finding_id_twice"),
    ("finding_blocks", '            if f.get("blocks_launch") is not False or f.get("status") != "open":', "            if " + F + ":", "an_appended_finding_must_not_block"),
    ("finding_dash", '            if EM_DASH in f.get("summary", "") or EN_DASH in f.get("summary", ""):', "            if " + F + ":", "a_dash_in_a_finding"),
    ("catalog_id", '        if not isinstance(new, dict) or new.get("id") != op["path"]:', "        if " + F + ":", "a_minted_ids_id_is_its_path"),
    ("catalog_titled", '        if not (isinstance(new.get("title"), str) and new["title"].strip()) or BARE_HOST.match(new.get("url") or ""):', "        if " + F + ":", "a_minted_id_must_be_titled or a_minted_id_must_be_document_scoped"),
    ("catalog_t1", '        if new.get("tier") != "T1":', "        if " + F + ":", "a_minted_id_must_be_t1"),
    ("catalog_evidenced", '        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):', "        if " + F + ":", "a_minted_id_must_be_evidenced"),
    ("catalog_ids", '        if r["source_id"] not in cat:', "        if " + F + ":", "cited_id_must_be_in_the_catalog"),
    ("register_twin", "                if (crop, twin) not in edited:", "                if " + F + ":", "seasoned_without_its_beginner"),
    ("register_identical", "                if _value(qidx[crop], path) == _value(qidx[crop], twin):", "                if " + F + ":", "byte_identical_registers"),
    ("register_new_row", '        if op["kind"] == "row" and op["new"]["traits_seasoned"] == op["new"]["traits_beginner"]:', "        if " + F + ":", "a_new_rows_registers_byte_identical"),
    ("rekey", "        if REKEY_FROM not in old or compact(new) != compact(want) or list(new) != list(want):", "        if " + F + ":", "a_rekey_that"),
    ("hs132_rows", '            if ("uf_ifas_hs132" in cited) != ((crop, i) in HS132_ROWS):', "            if " + F + ":", "hs132_kept_on_a_row or hs132_dropped"),
    ("bare_host", '                if BARE_HOST.match(a.get("url") or ""):', "                if " + F + ":", "a_bare_host_anchor"),
    ("retired_ids", "            if blk_cited & set(RETIRED_IDS):", "            if " + F + ":", "a_retired_id"),
    ("rekey_undone", "            if REKEY_FROM in blk:", "            if " + F + ":", "a_rekey_left_undone"),
    ("match_call", '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=HILL_POPULATION)',
     '        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=0, refuse=False)', "match_unclassified"),
    ("match_population", "    if res.inspected != HILL_POPULATION:", "    if " + F + ":", "match_population_pinned"),
    ("wcg_rc", "\n            if r.returncode != 0:", "\n            if " + F + ":", "gate_failure"),
    ("wcg_verdicts", "        if passed != len(slugs):", "        if " + F + ":", "gate_count_is"),
    ("gate_all_rc", "\n    if r.returncode != 0:", "\n    if " + F + ":", "gate_all_failure"),
    ("gate_all_population", "    if not m or int(m.group(1)) != certified or certified == 0:", "    if " + F + ":", "gate_all_population"),
]
SENTINEL = (SU, 'POST_SHA = "ef1a4d35', 'POST_SHA = "00000000', "real_stage_promotes")


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
    tmp = tempfile.mkdtemp(prefix="mut_pla625p2_")
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
