#!/usr/bin/env python3
"""mutate_pla10_promote2 -- mutation harness for PLA-10 promote 2's session-1 TOOLS commit (2026-10-02): the
two record allowances (a rootstock row gains a source only while its spacing override is authored; an open
finding's summary gains an APPENDED correction line) and every guard that keeps them that narrow. Extended in
session 2's tools commit (2026-10-02) for T1 (layout entries appended verbatim, the default move, the mirrors
recomputed through planting_layout_gate, restatements on a moved mirror) and T2 (A44's rootstock override key,
driven both as unit tests and through the real whole_crop_gate entry point).

PLA-215 bar: one defect per guard family injected into a SCRATCH COPY of tools/; its named driver must go
RED. Liveness: an anchor preflight (every anchor matches exactly once, or HARNESS DEAD), a MUTATION-APPLIED
marker re-read from disk, a SENTINEL that must redden, and a POSITIVE CONTROL that runs every driver file
WHOLE and unmutated (a pre-red driver would grade its mutation caught for the wrong reason). A pytest rc 5
(nothing collected) is graded BROKEN. The runner is mutate_pla10_promote1.py's, copied unchanged.

Usage: mutate_pla10_promote2.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5

PRT = "test_promote_pla10_promote2.py"
A44T = "test_planting_layout_gate.py"
A44I = "test_gate_planting_layout_a44.py"   # script: the real whole_crop_gate / gate_all entry points
SCRIPTS = {A44I}
PRM = "promote_pla10_promote2.py"
COM = "cited_promote_common.py"
PLG = "planting_layout_gate.py"

# (name, target, old, new, driver file, pytest -k selector)
MUTATIONS = [
    # ---- R: the rootstock allowance --------------------------------------------------------------
    ("r_any_crop", PRM, "            if slug not in ROOTSTOCK_CROPS:", "            if False:",
     PRT, "test_an_override_on_a_crop_off_the_R1_list_REFUSES"),
    ("r_rows_not_all_named", PRM, "            if set(names) != have:", "            if not set(names) <= have:",
     PRT, "test_every_row_must_be_named_missing"),
    ("r_duplicate_row_passes", PRM, "            for nm in sorted({x for x in names if names.count(x) > 1}):",
     "            for nm in []:", PRT, "test_a_row_named_twice_REFUSES"),
    ("r_row_keys_open", PRM, "                if not set(r) <= ROW_KEYS or not {\"name\", \"spacing_inches\"} <= set(r):",
     "                if not {\"name\", \"spacing_inches\"} <= set(r):", PRT, "test_an_unknown_row_key_REFUSES"),
    ("r_pair_order_unchecked", PRM, "and 0 < v[0] <= v[1])", "and 0 < v[0])",
     PRT, "test_an_override_out_of_order_REFUSES"),
    ("r_base_override_ignored", PRM, "            if \"spacing_inches\" in r:", "            if False:",
     PRT, "test_a_base_that_already_carries_an_override_REFUSES"),
    ("r_source_on_null_override", PRM, "                if v is None:\n                    refuse(f\"{tag}: add_source is allowed only",
     "                if False:\n                    refuse(f\"{tag}: add_source is allowed only",
     PRT, "test_add_source_on_a_null_override_REFUSES"),
    ("r_source_already_cited", PRM, "                if a[\"id\"] in (row.get(\"sources\") or []) or a[\"id\"] in (row.get(\"anchoring_urls\") or {}):",
     "                if False:", PRT, "test_add_source_already_cited_by_the_row_REFUSES"),
    ("r_source_off_catalog", PRM, "                if a[\"id\"] not in catalog:", "                if False:",
     PRT, "test_add_source_off_the_catalog_REFUSES"),
    ("r_source_shape_open", PRM, "                if not isinstance(a, dict) or set(a) != ADD_SOURCE_KEYS:",
     "                if not isinstance(a, dict):", PRT, "test_add_source_shape_REFUSES"),
    ("r_bare_host_passes", PRM, "                if is_bare(a[\"url\"]):", "                if False:",
     PRT, "test_a_bare_host_anchor_on_the_added_source_REFUSES"),
    # the obvious defect 1: a source added to a non-spacing rootstock field (or a null-override row)
    ("r_whole_row_writable", PRM, "        allowed.add((\"rootstock_options\", i, \"spacing_inches\"))",
     "        allowed.add((\"rootstock_options\", i))", PRT, "test_a_source_on_a_non_spacing_rootstock_field_REFUSES"),
    ("r_null_row_citation_writable", PRM, "        if r.get(\"add_source\"):\n            allowed.add((\"rootstock_options\", i, \"sources\"))",
     "        if True:\n            allowed.add((\"rootstock_options\", i, \"sources\"))",
     PRT, "test_a_source_added_to_a_NULL_override_row_in_the_post_REFUSES"),
    ("r_all_anchors_writable", PRM, "            allowed.add((\"rootstock_options\", i, \"anchoring_urls\", r[\"add_source\"][\"id\"]))",
     "            allowed.add((\"rootstock_options\", i, \"anchoring_urls\"))",
     PRT, "test_an_existing_anchor_rewritten_REFUSES"),
    ("r_sources_not_append_only", PRM, "                if (rb.get(\"sources\") or []) != list(ra.get(\"sources\") or []) + [add[\"id\"]]:",
     "                if add[\"id\"] not in (rb.get(\"sources\") or []):", PRT, "test_sources_replaced_not_appended_REFUSES"),
    ("r_added_anchor_unchecked", PRM, "                if (rb.get(\"anchoring_urls\") or {}).get(add[\"id\"]) != {\"url\": add[\"url\"], \"verified\": add[\"verified\"]}:",
     "                if False:", PRT, "test_the_added_anchor_not_the_stages_REFUSES"),
    ("r_override_value_unchecked", PRM, "            if \"spacing_inches\" not in rb or compact(rb[\"spacing_inches\"]) != compact(r[\"spacing_inches\"]):",
     "            if False:", PRT, "test_an_override_value_not_the_stages_REFUSES"),
    ("r_dropped_null_passes", PRM, "            if \"spacing_inches\" not in rb or compact(rb[\"spacing_inches\"]) != compact(r[\"spacing_inches\"]):",
     "            if compact(rb.get(\"spacing_inches\")) != compact(r[\"spacing_inches\"]):",
     PRT, "test_a_null_override_dropped_from_the_post_REFUSES"),
    # ---- E: evidence ------------------------------------------------------------------------------
    ("e_coverage_unchecked", PRM, "            if row.get(\"spacing_inches\") is not None and (slug, eid) not in covered:",
     "            if False:", PRT, "test_an_override_without_evidence_REFUSES"),
    ("e_value_unchecked", PRM, "        if compact(holder[r[\"field\"]]) != r[\"value\"]:", "        if False:",
     PRT, "test_a_value_mismatch_REFUSES"),
    ("e_null_row_evidence_passes", PRM, "            if r[\"field\"] != \"spacing_inches\" or holder.get(\"spacing_inches\") is None:",
     "            if r[\"field\"] != \"spacing_inches\":", PRT, "test_evidence_for_a_null_override_REFUSES"),
    ("e_source_not_the_rows", PRM, "        if r[\"source_id\"] not in (holder.get(\"sources\") or []):", "        if False:",
     PRT, "test_the_source_must_be_the_rows"),
    ("e_url_not_the_anchor", PRM, "        if (holder.get(\"anchoring_urls\") or {}).get(r[\"source_id\"], {}).get(\"url\") != r[\"url\"]:",
     "        if False:", PRT, "test_the_url_must_be_the_rows_anchor"),
    ("e_manifest_unchecked", COM, "    if r[\"url\"] not in man.get(r[\"sha256\"], set()):", "    if False:",
     PRT, "test_a_url_not_in_the_manifest_REFUSES"),
    ("e_quote_unchecked", COM, "    if len(q) < 12 or q not in text_cache[r[\"sha256\"]]:", "    if len(q) < 12:",
     PRT, "test_a_quote_not_in_the_bytes_REFUSES"),
    ("e_endpoint_unchecked", PRM, "        if not quote_states(r[\"field\"], json.loads(r[\"value\"]), r[\"quote\"]):",
     "        if False:", PRT, "test_a_quote_that_states_no_endpoint_REFUSES"),
    ("e_hash_unchecked", COM, "        if sha256_bytes(raw) != r[\"sha256\"]:", "        if False:",
     PRT, "test_tampered_bytes_REFUSE"),
    ("e_catalog_unchecked", PRM, "            for sid in row.get(\"sources\") or []:\n                if sid not in catalog:",
     "            for sid in row.get(\"sources\") or []:\n                if False:",
     PRT, "test_a_row_source_off_the_catalog_REFUSES"),
    ("e_common_feet_dropped", COM, "    return bool(ends & nums) or bool({x / 12 for x in ends} & nums)",
     "    return bool(ends & nums)", PRT, "test_apples_owed_overrides_pass_against_the_REAL_hashed_ncsu_bytes"),
    # ---- F: corrections ---------------------------------------------------------------------------
    ("f_format_loose", PRM, "                m = CORRECTION.fullmatch(fc[\"append\"])", "                m = CORRECTION.search(fc[\"append\"])",
     PRT, "test_a_correction_must_be_one_dated_correction_line"),
    ("f_date_unparsed", PRM, "                        datetime.date.fromisoformat(m.group(1))", "                        pass",
     PRT, "test_a_correction_must_be_one_dated_correction_line"),
    ("f_unknown_finding", PRM, "                if len(hits) != 1:\n                    refuse(f\"{slug}: open finding",
     "                if False:\n                    refuse(f\"{slug}: open finding", PRT, "test_a_correction_on_an_unknown_finding_REFUSES"),
    ("f_twice_passes", PRM, "                if fc[\"id\"] in ids:", "                if False:",
     PRT, "test_two_corrections_on_one_finding_in_one_stage_REFUSES"),
    ("f_row_shape_open", PRM, "                if not isinstance(fc, dict) or set(fc) != {\"id\", \"append\"}:",
     "                if not isinstance(fc, dict):", PRT, "test_a_correction_row_shape_REFUSES"),
    ("f_double_apply", PRM, "                if summ.endswith(fc[\"append\"]):", "                if False:",
     PRT, "test_a_correction_already_applied_REFUSES"),
    # the obvious defect 2: a correction that rewrites rather than appends
    ("f_rewrite_passes", PRM, "            if fb.get(\"summary\") != fa[\"summary\"] + fc[\"append\"]:",
     "            if not fb.get(\"summary\", \"\").endswith(fc[\"append\"]):",
     PRT, "test_a_correction_that_REWRITES_rather_than_appends_REFUSES"),
    # the obvious defect 3: an edit to any other verification_status key
    ("f_whole_finding_writable", PRM, "        allowed.add((\"verification_status\", \"open_findings\", _finding_index(pre_crop, fc[\"id\"])[0], \"summary\"))",
     "        allowed.add((\"verification_status\", \"open_findings\", _finding_index(pre_crop, fc[\"id\"])[0]))",
     PRT, "test_a_correction_written_into_basis_REFUSES"),
    ("f_all_findings_writable", PRM, "        allowed.add((\"verification_status\", \"open_findings\", _finding_index(pre_crop, fc[\"id\"])[0], \"summary\"))",
     "        allowed.add((\"verification_status\", \"open_findings\"))",
     PRT, "test_another_findings_summary_edited_REFUSES"),
    ("f_verification_status_writable", PRM, "    return allowed\n", "    return allowed | {(\"verification_status\",)}\n",
     PRT, "test_a_launch_flag_edited_REFUSES"),
    # ---- B: blast radius, sets first ------------------------------------------------------------
    ("b_stray_allowed", PRM, "        if stray:", "        if False:", PRT, "test_a_stray_crop_field_REFUSES"),
    ("b_diff_one_sided", COM, "            if k not in a or k not in b:\n                out.add(path + (k,))",
     "            if k not in a or k not in b:\n                pass", PRT, "test_a_removed_crop_key_REFUSES"),
    ("b_shell_unchecked", PRM, "                refuse(f\"shell {slug} changed\")", "                pass",
     PRT, "test_a_shell_change_REFUSES"),
    ("b_top_level_value_unchecked", PRM, "        if k != \"crops\" and compact(pre[k]) != compact(post[k]):",
     "        if False:", PRT, "test_a_top_level_change_REFUSES"),
    ("b_top_level_set_unchecked", PRM, "    if set(pre) != set(post):", "    if False:",
     PRT, "test_a_top_level_key_added_REFUSES"),
    ("b_roster_order_unchecked", PRM,
     "    if [c[\"slug\"] for c in pre[\"crops\"]] != [c[\"slug\"] for c in post[\"crops\"]]:", "    if False:",
     PRT, "test_a_roster_reorder_REFUSES"),
    ("b_unstaged_crops_skipped", PRM, "        allowed = allowed_paths(a, stage.get(slug, {}))",
     "        if slug not in stage:\n            continue\n        allowed = allowed_paths(a, stage.get(slug, {}))",
     PRT, "test_an_unstaged_crop_edited_REFUSES"),
    ("b_empty_stage_passes", PRM, "    if not stage:\n        refuse(", "    if False:\n        refuse(",
     PRT, "test_an_empty_stage_REFUSES"),
    # ---- G: gates on the post-state --------------------------------------------------------------
    ("g_numeric_not_run", PRM, "            v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)",
     "            v = []", PRT, "test_an_override_over_numeric_sanity_REFUSES"),
    ("g_a63_not_run", PRM, "    v = BH.roster(post)[4]", "    v = []", PRT, "test_A63_runs_on_the_post_state"),
    ("g_a62_not_run", PRM, "    v = SBR.roster(post, mature_dimensions_armed=False, known=SBR.KNOWN_AT_ARMING)[3]", "    v = []", PRT, "test_A62_runs_on_the_post_state"),
    ("g_a44_not_run", PRM, "    if r[\"violations\"]:\n        refuse(f\"planting_layout_gate (armed)",
     "    if False:\n        refuse(f\"planting_layout_gate (armed)", PRT, "test_A44_runs_on_the_post_state"),
    ("g_rootstock_list_widened", PRM, "ROOTSTOCK_CROPS = (\"apple\",)", "ROOTSTOCK_CROPS = (\"apple\", \"pear-asian\")",
     PRT, "test_the_rootstock_crop_list_is_the_literal"),
    # ---- L (T1, session 2): layout entries appended verbatim, the default move, the mirrors -------------
    # the named defect: an entry id re-derived from (arrangement, support) by the transform ...
    ("l_id_rederived_in_transform", PRM, "            entries.extend(copy.deepcopy(s.get(\"planting_layout_add\") or []))",
     "            entries.extend([dict(e, id=f\"{e['arrangement']}-{e['support']}\") for e in s.get(\"planting_layout_add\") or []])",
     PRT, "test_the_clean_layout_stage_passes_and_changes_exactly_what_it_names"),
    # ... and the guard that sees it in the post
    ("l_added_unchecked", PRM, "        if compact(got[k]) != compact(want):", "        if False:",
     PRT, "test_an_entry_id_RE_DERIVED_in_the_post_REFUSES"),
    # the named defect: an existing entry altered
    ("l_existing_unchecked", PRM, "        if compact(got[i]) != compact(want):", "        if False:",
     PRT, "test_an_EXISTING_entry_altered_REFUSES"),
    # the named defect: two defaults (the old one left true; the guard stops comparing the flag)
    ("l_existing_default_flag_ignored", PRM, "        if compact(got[i]) != compact(want):",
     "        if compact({x: y for x, y in got[i].items() if x != 'default'}) != compact({x: y for x, y in want.items() if x != 'default'}):",
     PRT, "test_TWO_DEFAULTS_the_old_default_left_true_REFUSES"),
    ("l_staged_default_true_passes", PRM, "            if e.get(\"default\") is not False:", "            if False:",
     PRT, "test_TWO_DEFAULTS_a_staged_entry_marked_default_REFUSES"),
    ("l_length_unchecked", PRM, "    if not isinstance(got, list) or len(got) != len(base) + len(add):",
     "    if not isinstance(got, list):", PRT, "test_an_existing_entry_dropped_REFUSES"),
    ("l_staged_twice_passes", PRM, "            if eid in staged_ids:", "            if False:",
     PRT, "test_a_staged_id_twice_REFUSES"),
    ("l_existing_id_reused", PRM, "            if eid in base_ids:", "            if False:",
     PRT, "test_a_staged_id_already_on_the_crop_REFUSES"),
    ("l_entry_shape_open", PRM, "        if not (isinstance(add, list) and add and all(isinstance(e, dict) for e in add)):",
     "        if not isinstance(add, list):", PRT, "test_a_staged_entry_that_is_not_an_object_REFUSES"),
    ("l_support_crops_open", PRM, "        if slug not in SUPPORT_CROPS:", "        if False:",
     PRT, "test_an_entry_on_a_crop_off_the_ruled_list_REFUSES"),
    ("l_default_crops_open", PRM, "        if slug not in DEFAULT_MOVE_CROPS:", "        if False:",
     PRT, "test_a_default_move_off_the_ruled_list_REFUSES"),
    ("l_default_names_nothing", PRM, "        if dflt not in base_ids + staged_ids:", "        if False:",
     PRT, "test_a_default_naming_no_entry_REFUSES"),
    ("l_default_already_default", PRM, "        if d is not None and d.get(\"id\") == dflt:", "        if False:",
     PRT, "test_a_default_naming_the_current_default_REFUSES"),
    # the named defect: a default move whose mirror is not recomputed -- the transform, and the guard
    ("l_mirror_not_recomputed", PRM, "            c[\"spacing_inches\"] = PLG.expected_spacing(entries)", "            pass",
     PRT, "test_the_clean_layout_stage_passes_and_changes_exactly_what_it_names"),
    ("l_mirror_unchecked", PRM, "        if k not in b or compact(b[k]) != compact(exp):", "        if False:",
     PRT, "test_a_DEFAULT_MOVE_WHOSE_MIRROR_IS_NOT_RECOMPUTED_REFUSES"),
    ("l_mirrors_writable_unstaged", PRM, "    if _layout_staged(s):\n        allowed |=", "    if True:\n        allowed |=",
     PRT, "test_a_mirror_moved_on_a_crop_with_no_layout_stage_REFUSES"),
    # ---- S (T1): restatements on a moved mirror -------------------------------------------------------
    ("s_unadjudicated_passes", PRM, "        if p not in adj:\n            refuse(f\"{slug}: a mirror moves",
     "        if False:\n            refuse(f\"{slug}: a mirror moves", PRT,
     "test_an_unadjudicated_restatement_on_a_moved_mirror_REFUSES"),
    ("s_row_mirror_not_a_trigger", PRM, "for k in (\"spacing_inches\", \"row_spacing_inches\")\n",
     "for k in (\"spacing_inches\",)\n", PRT, "test_an_unadjudicated_restatement_on_a_moved_mirror_REFUSES"),
    ("s_edited_without_edit", PRM, "        if adj[p] == \"edited\" and p not in edited:", "        if False:",
     PRT, "test_edited_without_an_edit_REFUSES"),
    ("s_note_unchecked", PRM, "                and r[\"verdict\"] in (\"agrees\", \"edited\") and str(r[\"note\"]).strip()):",
     "                and r[\"verdict\"] in (\"agrees\", \"edited\")):", PRT, "test_a_restatement_with_no_note_REFUSES"),
    ("s_stale_restatements_pass", PRM, "        if adj:\n            refuse(f\"{slug}: restatements staged",
     "        if False:\n            refuse(f\"{slug}: restatements staged", PRT,
     "test_restatements_on_a_crop_whose_mirrors_do_not_move_REFUSE"),
    ("s_edit_on_owned_key", PRM, "        if parse_path(ed[\"path\"])[0] in OWNED_HEADS:", "        if False:",
     PRT, "test_an_edit_lands_and_an_edit_on_an_owned_key_REFUSES"),
    ("s_edit_value_unchecked", PRM, "        if compact(node) != compact(ed[\"new\"]):", "        if False:",
     PRT, "test_an_edit_value_not_the_stages_in_the_post_REFUSES"),
    # ---- E (T1): evidence on every added entry ---------------------------------------------------------
    ("e_layout_coverage_unchecked", PRM, "                if e.get(f) is not None and (slug, e[\"id\"], f) not in covered_l:",
     "                if False:", PRT, "test_an_added_entry_without_evidence_REFUSES"),
    ("e_layout_unstaged_entry_passes", PRM, "            if r[\"entry_id\"] not in added:", "            if False:",
     PRT, "test_evidence_for_an_entry_the_stage_does_not_add_REFUSES"),
    ("e_duplicate_row_passes", PRM, "        if key in seen:", "        if False:",
     PRT, "test_a_duplicate_evidence_row_REFUSES"),
    ("e_layout_source_not_the_entrys", PRM, "            holder, what = next(e for e in c[\"planting_layout\"] if e.get(\"id\") == r[\"entry_id\"]), \"entry\"",
     "            holder, what = next(e for e in c[\"planting_layout\"] if e.get(\"id\") == r[\"entry_id\"]), \"entry\"\n            holder = dict(holder, sources=holder.get(\"sources\", []) + [r[\"source_id\"]], anchoring_urls=dict(holder.get(\"anchoring_urls\", {}), **{r[\"source_id\"]: {\"url\": r[\"url\"]}}))",
     PRT, "test_layout_evidence_source_not_the_entrys_REFUSES"),
    # ---- T2: A44's rootstock override key (planting_layout_gate) ---------------------------------------
    ("t2_all_or_none_passes", PLG, "    if len(carriers) != len(rows):", "    if False:", A44T, "test_all_or_none_on_a_crop"),
    ("t2_pair_unchecked", PLG, "        if not is_pair(val):\n            v.append(f\"{tag}: spacing_inches {val!r} is not null",
     "        if False:\n            v.append(f\"{tag}: spacing_inches {val!r} is not null", A44T,
     "test_each_value_is_null_or_a_pair"),
    # the named defect: an override with no source
    ("t2_no_source_passes", PLG, "        if not (isinstance(src, list) and src):", "        if False:",
     A44T, "test_a_non_null_override_with_no_source"),
    ("t2_anchor_unchecked", PLG, "                v.append(f\"{tag}: spacing_inches {val!r}: source {s!r} has no http(s) anchoring url \"\n                         f\"on the row\")",
     "                pass", A44T, "test_a_non_null_override_whose_source_is_not_anchored"),
    ("t2_presence_never_armed", PLG, "        if armed and slug in ROOTSTOCK_OVERRIDE_CROPS and certified(crop):", "        if False:",
     A44T, "test_armed_the_literal_list_must_carry_it"),
    ("t2_off_the_layout_paths", PLG, "    return _layout_check(crop, armed) + _rootstock_violations(slug, crop, rootstock_armed)",
     "    return _layout_check(crop, armed)", A44T, "test_violations_reach_every_layout_path"),
    ("t2_floor_unchecked", PLG, "    if rootstock_armed and r[\"rootstock_rows\"] < ROOTSTOCK_ROW_FLOOR:", "    if False:",
     A44T, "test_armed_refuses_below_the_row_floor"),
    ("t2_rows_unreported", PLG, "        \"rootstock_rows\": sum(len(x) for x in rs),", "        \"rootstock_rows\": sum(len(x) for x in rs[:0]),",
     A44T, "test_roster_reports_the_rows_it_inspected"),
    ("t2_shipped_unarmed", PLG, "ROOTSTOCK_OVERRIDE_ARMED = True", "ROOTSTOCK_OVERRIDE_ARMED = False",
     A44T, "test_the_data_commit_ships_rootstock_armed"),
    # ... and the arming reaches the REAL entry point: whole_crop_gate never passes the armed state on
    ("t2_entry_point_never_armed", PLG, "    rootstock_armed = ROOTSTOCK_OVERRIDE_ARMED if rootstock_armed is None else rootstock_armed\n    slug",
     "    rootstock_armed = False\n    slug", A44I, None),
]
SENTINEL = (PRT, '        self.assertEqual(P.ROOTSTOCK_CROPS, ("apple",))',
            '        self.assertEqual(P.ROOTSTOCK_CROPS, ("apple", "x"))', "test_the_rootstock_crop_list_is_the_literal")


def run_driver(tools, f, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if f in SCRIPTS:
        cmd = [sys.executable, "-B", os.path.join(tools, f)]
    else:
        cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, f), "-q", "-x", "--no-header",
               "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new + "  " + MARKER if "\n" not in new
                                                       else new.replace("\n", "  " + MARKER + "\n", 1), 1))
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_pla10p2_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        bad = [n for n, t, old, *_ in muts if open(os.path.join(tools, t), encoding="utf-8").read().count(old) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        for f in sorted({m[4] for m in muts}):
            rc, out = run_driver(tools, f, None)
            if rc != 0:
                print(out[-2000:])
                sys.exit(f"HARNESS DEAD: the unmutated driver {f} is already failing (rc {rc})")
        print(f"positive control: every driver file WHOLE and unmutated is GREEN "
              f"({len({m[4] for m in muts})} files)")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, f, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc in (0, NOTHING_COLLECTED):
            sys.exit(f"HARNESS DEAD: the sentinel did not redden (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, target, old, new, drv, sel in muts:
            clean, err = apply(tools, target, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, _ = run_driver(tools, drv, sel)
            open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append(name); print(f"  BROKEN   {name}: driver collected nothing")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  ({drv} {sel or '(script)'})")
            else:
                caught.append(name); print(f"  caught   {name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
