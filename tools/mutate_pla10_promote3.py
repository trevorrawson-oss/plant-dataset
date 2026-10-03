#!/usr/bin/env python3
"""mutate_pla10_promote3 -- mutation harness for PLA-10 promote 3's session-1 TOOLS commit (2026-10-02): T3 (the
third record allowance: one plant_dimensions field_additions record per newly authored crop), T4
(pla10_promote_common.quote_states_ft and its stated tolerance), T5 (A62's mature_dimensions sibling block and
its arming flag; A59's sibling rule and its flag), and every guard of promote_pla10_promote3 (the fixed list,
values, the sibling, the backfill rulings K1/K2/K3, evidence, restatements, blast radius, the post-state gates
through REACHABILITY drivers that corrupt the stage past check_pre).

PLA-215 bar: one defect per guard family injected into a SCRATCH COPY of tools/; its named driver must go RED.
Liveness: an anchor preflight (every anchor matches exactly once, or HARNESS DEAD), a MUTATION-APPLIED marker
re-read from disk, a SENTINEL that must redden, and a POSITIVE CONTROL that runs every driver file WHOLE and
unmutated (a pre-red driver would grade its mutation caught for the wrong reason). A pytest rc 5 (nothing
collected) is graded BROKEN. The runner is mutate_pla10_promote2.py's, copied unchanged.

Usage: mutate_pla10_promote3.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5

PRT = "test_promote_pla10_promote3.py"
SBT = "test_sourced_block_ratchet_gate.py"
PDT = "test_plant_dimensions_gate.py"
A59I = "test_gate_plant_dimensions_a59.py"   # script: the real whole_crop_gate entry point
SCRIPTS = {A59I}
PRM = "promote_pla10_promote3.py"
COM = "pla10_promote_common.py"
SBR = "sourced_block_ratchet_gate.py"
PDG = "plant_dimensions_gate.py"
WCG = "whole_crop_gate.py"

# (name, target, old, new, driver file, pytest -k selector)
MUTATIONS = [
    # ---- T4: quote_states_ft -------------------------------------------------------------------------
    # the named injection 1: a tolerance that passes 3.9 against "47 inches"
    ("t4_loose_tolerance", COM, "TOL_FT = 0.00005", "TOL_FT = 0.02", PRT, "test_H4_a_LOOSE_rounding_FAILS"),
    # the named injection 2: a spread quoted from a height sentence (dimension class ignored)
    ("t4_any_dimension", COM, "    figs = [v for cls, vals in _ft_groups(quote) if want in cls for v in vals]",
     "    figs = [v for cls, vals in _ft_groups(quote) if cls for v in vals]", PRT,
     "test_a_spread_quoted_from_a_HEIGHT_clause_FAILS"),
    ("t4_inches_not_divided", COM, "            vals.append(x[2] / 12 if nxt == \"in\" else x[2])",
     "            vals.append(x[2])", PRT, "test_H4_broccoli_rounded_quotient_passes"),
    ("t4_compound_inches_dropped", COM,
     "            qty.append([m.start(), m.end(), _num_val(m.group(\"cf\")) + _num_val(m.group(\"ci\")) / 12, \"ft\"])",
     "            qty.append([m.start(), m.end(), _num_val(m.group(\"cf\")), \"ft\"])", PRT,
     "test_a_compound_figure_reads_to_4_places"),
    ("t4_spacing_reads_as_height", COM,
     "    (re.compile(r\"(?:apart|between|deep|long|away|in\\s+length|of\\s+vine)\\b\"), \"\"),",
     "", PRT, "test_vine_run_and_spacing_state_no_dimension"),
    # ---- T5: A62's mature_dimensions sibling block ---------------------------------------------------
    ("t5_a62_not_named", SBR, "    \"mature_dimensions\": (\"mature_height_ft\", \"mature_spread_ft\"),\n}",
     "}", SBT, "test_the_sibling_keys_are_not_UNNAMED"),
    ("t5_a62_flag_ignored", SBR, "        if name == \"mature_dimensions\" and not mature_dimensions_armed:",
     "        if name == \"mature_dimensions\":", SBT, "test_armed_a_height_with_no_sibling_FAILS_by_name"),
    ("t5_a62_always_armed", SBR, "        if name == \"mature_dimensions\" and not mature_dimensions_armed:",
     "        if False:", SBT, "test_unarmed_an_uncited_height_is_not_failed"),
    # armed in the data commit (2026-10-03): the flag mutation is now armed LATE (was armed early, pre-data)
    ("t5_a62_armed_late", SBR, "MATURE_DIMENSIONS_ARMED = True", "MATURE_DIMENSIONS_ARMED = False",
     SBT, "test_the_flag_matches_the_data"),
    # ---- T5: A59's sibling rule ----------------------------------------------------------------------
    # the named injection: a height with no sibling
    ("t5_a59_rule_skipped", PDG, "    if not _certified(crop) or all(crop.get(f) is None for f in RANGE_FIELDS):\n        return []\n    slug = crop.get(\"slug\") or \"?\"\n    src",
     "    if True:\n        return []\n    slug = crop.get(\"slug\") or \"?\"\n    src", PDT, "test_a_height_with_no_sibling_FAILS"),
    ("t5_a59_empty_sibling_passes", PDG, "    if not (isinstance(src, list) and src and all(isinstance(s, str) and s.strip() for s in src)):",
     "    if not isinstance(src, list):", PDT, "test_an_empty_or_blank_sibling_FAILS"),
    # the named injection: a sibling with no anchor
    ("t5_a59_anchor_unchecked", PDG, "        if not (isinstance(url, str) and url.startswith((\"http://\", \"https://\"))):",
     "        if False:", PDT, "test_a_source_with_no_anchor_FAILS"),
    ("t5_a59_armed_late", WCG, "A59_SIBLING_ARMED = True", "A59_SIBLING_ARMED = False", A59I, None),
    # the entry-point call itself (data commit, 2026-10-03): the flag stays True but whole_crop_gate never calls
    # the sibling rule, so only a test driving the real entry point on an uncited pair can see it
    ("t5_a59_entry_call_dropped", WCG, " + (_pd_sibling(crop) if A59_SIBLING_ARMED else [])", "", A59I, None),
    # ---- X / V: the fixed list, values ---------------------------------------------------------------
    ("x_fixed_list_open", PRM, "    if set(stage) != want:", "    if False:", PRT, "test_FIXED_LIST_a_missing_crop_REFUSES"),
    ("x_empty_stage_passes", PRM, "    if not stage:\n        refuse(\"the stage names no crop",
     "    if False:\n        refuse(\"the stage names no crop", PRT, "test_an_empty_stage_REFUSES"),
    ("x_base_sibling_ignored", PRM, "            if k in c:\n                refuse(f\"base already carries",
     "            if False:\n                refuse(f\"base already carries", PRT, "test_a_base_already_carrying_a_sibling_REFUSES"),
    ("v_decimals_unchecked", PRM, "            if v is not None and any(round(x, 4) != x for x in v):",
     "            if False:", PRT, "test_H4_more_than_4_decimals_REFUSES"),
    ("v_order_unchecked", PRM, "and 0 < v[0] <= v[1])", "and 0 < v[0])", PRT, "test_a_value_out_of_order_REFUSES"),
    ("v_value_key_optional", PRM, "            if f not in s:\n                refuse(f\"{slug}: the stage must state",
     "            if False:\n                refuse(f\"{slug}: the stage must state", PRT, "test_a_value_key_missing_REFUSES"),
    ("v_new_base_not_null", PRM, "    if c.get(H) is not None or c.get(S) is not None:\n        refuse(f\"{slug}: a NEW crop",
     "    if False:\n        refuse(f\"{slug}: a NEW crop", PRT, "test_a_NEW_crop_carrying_a_value_on_the_base_REFUSES"),
    ("v_backfill_values_free", PRM, "    elif compact(s[H]) != compact(c.get(H)) or compact(s[S]) != compact(c.get(S)):",
     "    elif False:", PRT, "test_a_backfill_value_moved_REFUSES"),
    ("v_k2_any_value", PRM, "        if compact(s[H]) != compact(K2[slug][\"height\"]):", "        if False:",
     PRT, "test_K2_moves_only_to_the_ruled_value"),
    ("v_k2_spread_free", PRM, "        if s[S] is not None and compact(s[S]) != compact(c.get(S)):", "        if False:",
     PRT, "test_K2_spread_stays_or_goes_null"),
    # ---- C: the sibling --------------------------------------------------------------------------------
    ("c_sources_may_be_empty", PRM, "    if not (isinstance(src, list) and src and all(isinstance(x, str) and x for x in src)):",
     "    if not isinstance(src, list):", PRT, "test_a_value_with_no_sources_REFUSES"),
    ("c_duplicate_source", PRM, "    if len(set(src)) != len(src):", "    if False:", PRT, "test_a_source_twice_REFUSES"),
    ("c_catalog_unchecked", PRM, "        if sid not in catalog:\n            refuse(f\"{slug}: source {sid!r} is not in source_catalog\")",
     "        if False:\n            refuse(f\"{slug}: source {sid!r} is not in source_catalog\")", PRT,
     "test_a_source_off_the_catalog_REFUSES"),
    # the named injection again, at the promote: a sibling source with no anchor
    ("c_anchor_per_source", PRM, "    if not isinstance(anc, dict) or set(anc) != set(src):",
     "    if not isinstance(anc, dict):", PRT, "test_a_SOURCE_WITH_NO_ANCHOR_REFUSES"),
    ("c_anchor_keys_open", PRM, "        if not isinstance(a, dict) or set(a) != ANCHOR_KEYS:",
     "        if not isinstance(a, dict):", PRT, "test_an_anchor_with_extra_keys_REFUSES"),
    ("c_bare_host_passes", PRM, "        if is_bare(a[\"url\"]):", "        if False:", PRT, "test_a_bare_host_anchor_REFUSES"),
    ("c_verified_undated", PRM, "        if not _date(a[\"verified\"]):", "        if False:", PRT, "test_an_undated_anchor_REFUSES"),
    ("c_sibling_on_null_crop", PRM, "        for k in (\"sources\", \"anchoring_urls\", \"field_addition\"):",
     "        for k in (\"field_addition\",):", PRT, "test_a_sibling_on_a_null_crop_REFUSES"),
    ("k3_anchor_any_url", PRM, "    if s[\"anchoring_urls\"][sid][\"url\"] != url:", "    if False:",
     PRT, "test_K3_the_backfill_anchor_is_the_records_url"),
    ("k3_source_any", PRM, "    if sid not in s[\"sources\"]:", "    if False:", PRT, "test_K3_the_backfill_cites_the_records_source"),
    ("k1_repoint_skipped", PRM, "    if slug in REPOINT:", "    if False:", PRT, "test_K1_apple_on_its_records_s3_url_REFUSES"),
    ("k2_url_skipped", PRM, "    elif k2:\n        sid, url = K2[slug][\"source\"], K2[slug][\"url\"]",
     "    elif False:\n        sid, url = K2[slug][\"source\"], K2[slug][\"url\"]", PRT, "test_K2_taken_cites_the_ruled_page"),
    # ---- R (T3): the record allowance ------------------------------------------------------------------
    # the named injections: a record on a crop with no height authored; a second record on one crop
    ("t3_record_on_null_crop", PRM, "        for k in (\"sources\", \"anchoring_urls\", \"field_addition\"):",
     "        for k in (\"sources\", \"anchoring_urls\"):", PRT,
     "test_T3_a_record_on_a_crop_with_NO_HEIGHT_authored_REFUSES"),
    ("t3_second_record_new", PRM, "    if _records(c):\n        refuse(", "    if False:\n        refuse(",
     PRT, "test_T3_a_SECOND_record_on_a_new_crop_REFUSES"),
    ("t3_second_record_backfill", PRM, "    if \"field_addition\" in s:", "    if False:",
     PRT, "test_T3_a_SECOND_record_on_a_backfill_crop_REFUSES"),
    ("t3_record_optional", PRM, "    if fa is None:\n        refuse(", "    if fa is None:\n        return\n        refuse(",
     PRT, "test_T3_a_new_crop_with_a_value_and_no_record_REFUSES"),
    ("t3_record_keys_open", PRM, "    if not isinstance(fa, dict) or set(fa) != RECORD_KEYS:",
     "    if not isinstance(fa, dict):", PRT, "test_T3_record_shape_REFUSES"),
    ("t3_record_any_field", PRM, "    if fa[\"field\"] != RECORD_FIELD:", "    if False:", PRT, "test_T3_record_names_the_field"),
    ("t3_record_sources_free", PRM, "and set(fa[\"sources\"]) <= set(s[\"sources\"])):", "):",
     PRT, "test_T3_record_sources_within_the_sibling"),
    ("t3_record_undated", PRM, "    if not _date(fa[\"date\"]):", "    if False:", PRT, "test_T3_record_dated_and_noted"),
    # the named injection: an edit to any other field_additions entry (and two appended)
    ("t3_post_not_append_only", PRM, "        if compact(fa_b) != compact(want):", "        if False:",
     PRT, "test_T3_ANOTHER_field_additions_entry_edited_REFUSES"),
    ("t3_post_two_records", PRM, "        if compact(fa_b) != compact(want):", "        if len(fa_b) < len(want):",
     PRT, "test_T3_two_records_appended_in_the_post_REFUSES"),
    ("t3_whole_vs_writable", PRM, "        allowed.add((\"verification_status\", \"field_additions\"))",
     "        allowed.add((\"verification_status\",))", PRT, "test_T3_another_verification_status_key_edited_REFUSES"),
    # ---- E: evidence -----------------------------------------------------------------------------------
    ("e_coverage_unchecked", PRM, "            got = stated.get((slug, f))", "            got = stated.get((slug, f), set(c[f]))",
     PRT, "test_a_value_without_evidence_REFUSES"),
    ("e_one_end_enough", PRM, "            if got != set(c[f]):", "            if not got:", PRT,
     "test_a_ONE_ENDED_quote_cannot_carry_a_range"),
    ("e_value_unchecked", PRM, "        if compact(c[r[\"field\"]]) != r[\"value\"]:", "        if False:",
     PRT, "test_a_value_mismatch_REFUSES"),
    ("e_source_unchecked", PRM, "        if r[\"source_id\"] not in (c.get(SIB_S) or []):", "        if False:",
     PRT, "test_the_source_must_be_the_siblings"),
    ("e_url_unchecked", PRM, "        if (c.get(SIB_A) or {}).get(r[\"source_id\"], {}).get(\"url\") != r[\"url\"]:",
     "        if False:", PRT, "test_the_url_must_be_the_siblings_anchor"),
    ("e_manifest_unchecked", PRM, "        if r[\"url\"] not in man.get(r[\"sha256\"], set()):", "        if False:",
     PRT, "test_a_url_not_in_the_manifest_REFUSES"),
    ("e_quote_unchecked", PRM, "        if len(q) < 12 or q not in text_cache[r[\"sha256\"]]:", "        if len(q) < 12:",
     PRT, "test_a_quote_not_in_the_bytes_REFUSES"),
    ("e_dimension_unchecked", PRM, "        if not quote_states_ft(r[\"field\"], value, q):", "        if False:",
     PRT, "test_a_quote_stating_the_WRONG_DIMENSION_REFUSES"),
    ("e_hash_unchecked", PRM, "            if sha256_bytes(raw) != r[\"sha256\"]:", "            if False:",
     PRT, "test_tampered_bytes_REFUSE"),
    ("e_entry_unchecked", PRM, "        if r[\"entry_id\"] != ENTRY_ID or r[\"field\"] not in (H, S):", "        if False:",
     PRT, "test_a_row_naming_another_entry_REFUSES"),
    ("e_field_not_carried", PRM, "        if c.get(r[\"field\"]) is None:", "        if False:",
     PRT, "test_evidence_for_a_field_the_crop_does_not_carry_REFUSES"),
    # ---- S: restatements (H3) --------------------------------------------------------------------------
    ("s_unadjudicated_passes", PRM, "        if p not in adj:\n            refuse(f\"{slug}: a height moves",
     "        if False:\n            refuse(f\"{slug}: a height moves", PRT, "test_H3_an_unadjudicated_restatement_REFUSES"),
    ("s_edited_without_edit", PRM, "        if adj[p] == \"edited\" and p not in edited:", "        if False:",
     PRT, "test_edited_without_an_edit_REFUSES"),
    ("s_edit_anywhere", PRM, "        if adj.get(p) != \"edited\":", "        if False:", PRT,
     "test_an_edit_not_at_an_edited_restatement_REFUSES"),
    ("s_stale_restatements", PRM, "        if adj:\n            refuse(f\"{slug}: restatements staged but no value moves\")",
     "        if False:\n            refuse(f\"{slug}: restatements staged but no value moves\")", PRT,
     "test_restatements_on_a_backfill_crop_whose_values_do_not_move_REFUSE"),
    ("s_owned_key_editable", PRM, "        if parse_path(ed[\"path\"])[0] in OWNED_HEADS or parse_path(ed[\"path\"])[0].startswith(\"mature_dimensions\"):",
     "        if False:", PRT, "test_an_edit_on_an_owned_key_REFUSES"),
    ("s_edit_value_unchecked", PRM, "        if compact(node) != compact(ed[\"new\"]):", "        if False:",
     PRT, "test_an_edit_value_not_the_stages_in_the_post_REFUSES"),
    ("s_note_unchecked", PRM, "                and r[\"verdict\"] in (\"agrees\", \"edited\") and str(r[\"note\"]).strip()):",
     "                and r[\"verdict\"] in (\"agrees\", \"edited\")):", PRT, "test_a_restatement_with_no_note_REFUSES"),
    ("s_scanner_blind", PRM, "                if DIST.search(sent) and any(w.search(sent) for w in words):", "                if False:",
     PRT, "test_the_scanner_finds_dills_5_ft_prose"),
    ("s_width_always", PRM, "    words = (HEIGHT_WORD, WIDTH_WORD) if spread_too else (HEIGHT_WORD,)",
     "    words = (HEIGHT_WORD, WIDTH_WORD)", PRT, "test_width_words_scan_only_when_a_spread_is_authored"),
    # ---- B: blast radius -------------------------------------------------------------------------------
    ("b_roster_unchecked", PRM, "    if [c[\"slug\"] for c in pre[\"crops\"]] != [c[\"slug\"] for c in post[\"crops\"]]:",
     "    if False:", PRT, "test_a_roster_reorder_REFUSES"),
    ("b_top_level_unchecked", PRM, "        if k != \"crops\" and compact(pre[k]) != compact(post[k]):", "        if False:",
     PRT, "test_a_top_level_change_REFUSES"),
    ("b_shell_unchecked", PRM, "            if compact(a) != compact(b):\n                refuse(f\"shell",
     "            if False:\n                refuse(f\"shell", PRT, "test_a_shell_change_REFUSES"),
    ("b_stray_unchecked", PRM, "        if stray:", "        if False:", PRT, "test_an_unstaged_crop_edited_REFUSES"),
    ("b_backfill_values_writable", PRM, "    if _moves(slug, s, pre_crop):\n        allowed |= {(H,), (S,)}",
     "    if True:\n        allowed |= {(H,), (S,)}", PRT, "test_a_backfill_crop_value_changed_in_the_post_REFUSES"),
    ("b_value_unchecked", PRM, "            if f not in b or compact(b[f]) != compact(s[f]):", "            if False:",
     PRT, "test_a_value_not_the_stages_in_the_post_REFUSES"),
    ("b_sibling_unchecked", PRM, "            if b.get(SIB_S) != s[\"sources\"] or compact(b.get(SIB_A)) != compact(s[\"anchoring_urls\"]):",
     "            if False:", PRT, "test_a_sibling_not_the_stages_in_the_post_REFUSES"),
    ("b_sibling_position", PRM, "            _insert_after(c, S, SIB_S, list(s[\"sources\"]))",
     "            c[SIB_S] = list(s[\"sources\"])", PRT,
     "test_the_clean_stage_passes_and_changes_exactly_the_named_leaves"),
    # ---- G: the gates on the post-state, through the REACHABILITY drivers --------------------------------
    ("g_a59_never_run", PRM, "    v = PDG.all_violations(post, presence=True, coverage=True, sibling=True)", "    v = []",
     PRT, "test_REACH_A59_sibling_a_source_with_no_anchor"),
    ("g_a59_sibling_off", PRM, "    v = PDG.all_violations(post, presence=True, coverage=True, sibling=True)",
     "    v = PDG.all_violations(post, presence=True, coverage=True, sibling=False)",
     PRT, "test_REACH_A59_sibling_a_source_with_no_anchor"),
    ("g_a62_unarmed", PRM, "    v = SBR.roster(post, mature_dimensions_armed=True)[3]",
     "    v = SBR.roster(post, mature_dimensions_armed=False)[3]", PRT, "test_REACH_A62_armed_a_blank_sibling_source"),
    ("g_a63_never_run", PRM, "    v = BH.roster(post)[4]", "    v = []", PRT, "test_REACH_A63_a_bare_host_sibling_anchor"),
    ("g_numeric_sanity_dropped", PRM, "            v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)",
     "            v = DR.display_readiness_violations(c)", PRT, "test_numeric_sanity_runs_on_the_post_state"),
]
SENTINEL = (PRT, "        self.assertEqual(C.TOL_FT, 0.00005)", "        self.assertEqual(C.TOL_FT, 0.00006)",
            "test_the_tolerance_is_the_stated_literal")


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
