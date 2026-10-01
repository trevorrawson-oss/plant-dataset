#!/usr/bin/env python3
"""mutate_pla10_promote1 -- mutation harness for PLA-10 promote 1's TOOLS commit (2026-10-01): the A44
rewrite, A62's planting_layout family + R5 migration waivers, is_microgreen, display_readiness,
numeric_sanity's layout bounds, the A25 enum ruling, the gate wiring, and the promote's guards.

PLA-215 bar: one defect per guard family injected into a SCRATCH COPY of tools/; its named driver must go
RED. Liveness: an anchor preflight (every anchor matches exactly once, or HARNESS DEAD), a MUTATION-APPLIED
marker re-read from disk, a SENTINEL that must redden, and a POSITIVE CONTROL that runs every driver file
WHOLE and unmutated (a pre-red driver would grade its mutation caught for the wrong reason). Script-style
drivers run as scripts, never under pytest; a pytest rc 5 (nothing collected) is graded BROKEN.

Usage: mutate_pla10_promote1.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5

A44T = "test_planting_layout_gate.py"
A44E = "test_gate_planting_layout_a44.py"          # script
A62T = "test_sourced_block_ratchet_gate.py"
TST = "test_timing_spine_gate.py"                  # script
DRT = "test_display_readiness_gate.py"             # script
NST = "test_numeric_sanity_gate.py"               # script
RCT = "test_register_completeness_gate.py"        # script
PRT = "test_promote_pla10_planting_layout.py"
SCRIPTS = {A44E, TST, DRT, NST, RCT}

PLG, SBR, PRM = "planting_layout_gate.py", "sourced_block_ratchet_gate.py", "promote_pla10_planting_layout.py"

# (name, target, old, new, driver file, pytest -k selector or None for a script)
MUTATIONS = [
    # ---- A44: planting_layout_gate -------------------------------------------------------------
    ("a44_mirror_ignores_default", PLG,
     "    order = ([d] if d is not None else []) + [e for e in entries if e is not d]",
     "    order = list(entries)", A44T, "test_the_default_wins_even_when_declared_second"),
    ("a44_mirror_never_null", PLG, "        if exp is None and sp is not None:", "        if False:",
     A44T, "test_mirror_non_null_when_no_entry_carries_one"),
    ("a44_row_mirror_unchecked", PLG,
     '    if d is not None and "row_spacing_inches" in crop and rs != d.get("row_spacing_inches"):',
     "    if False:", A44T, "test_crop_root_row_borrowed_from_a_non_default_entry"),
    ("a44_see_layout_any_default", PLG,
     '    if d.get("arrangement") == "hill" and any(', "    if any(",
     A44T, "test_see_layout_on_a_row_default"),
    ("a44_zi_accepts_empty_list", PLG, "        if sp is not None:\n            v.append(f\"{slug}: zone_independent",
     "        if sp not in (None, []):\n            v.append(f\"{slug}: zone_independent",
     A44T, "test_an_empty_list_mirror_surviving_on_a_zone_independent_crop"),
    ("a44_two_defaults_pass", PLG, "    if entries and n_def != 1:", "    if entries and n_def < 1:",
     A44T, "test_3_exactly_one_default"),
    ("a44_unknown_keys_pass", PLG, "            if k not in req and k not in opt:", "            if False:",
     A44T, "test_2_unknown_key"),
    ("a44_id_pair_unchecked", PLG, "        elif arr in ARRANGEMENTS and sup in SUPPORTS and not (",
     "        elif False and not (", A44T, "test_2_id_must_match_its_pair"),
    ("a44_block_without_min_rows", PLG, "    if has_block and mr is None:", "    if False:",
     A44T, "test_4_block_iff_min_rows"),
    ("a44_entry_reason_widened", PLG, "        if rr not in ENTRY_REASONS:", "        if rr not in ROOT_REASONS:",
     A44T, "test_5_entry_reason_is_never_see_layout_or_not_applicable"),
    ("a44_height_on_unsupported", PLG, '        if sup == "none":', "        if False:",
     A44T, "test_6_height_override_only_on_support"),
    ("a44_retired_key_never_refused", PLG, "    if not armed:\n        return []\n    return [f\"{slug}: crop-root {k} is retired",
     "    return []\n    return [f\"{slug}: crop-root {k} is retired", A44T, "RetiredAnchors"),
    ("a44_presence_never_armed", PLG, "            if armed and cert:", "            if False:",
     A44T, "test_presence_on_a_certified_crop"),
    ("a44_string_form_kept", PLG, "            if armed:\n                return [f\"{slug}: planting_layout {pl!r}: the string",
     "            if False:\n                return [f\"{slug}: planting_layout {pl!r}: the string",
     A44T, "test_the_string_form_is_retired"),
    ("a44_zi_entries_allowed", PLG, "    if zi and pl:", "    if False:",
     A44T, "test_1_zone_independent_with_entries"),
    ("a44_crop_floor_dropped", PLG, '    if r["certified"] < CERT_FLOOR:', "    if False:",
     A44T, "test_refuses_below_the_crop_floor"),
    ("a44_entry_floor_dropped", PLG, '    if armed and r["entries"] < ENTRY_FLOOR:', "    if False:",
     A44T, "test_entry_floor_applies_only_armed"),
    ("a44_pair_order_unchecked", PLG, "all(_num(x) for x in v) and 0 < v[0] <= v[1]",
     "all(_num(x) for x in v) and 0 < v[0]", A44T, "test_5_pairs"),
    ("a44_anchor_per_source_unchecked", PLG, "        for s in sorted(set(src) - set(anc)):",
     "        for s in []:", A44T, "test_2_sources_and_anchors"),
    ("a44_lone_qualifier_passes", PLG, "        if len(pids) == 1 and isinstance(pids[0], str)",
     "        if False and isinstance(pids[0], str)", A44T, "test_2_qualifier_without_a_shared_pair"),
    ("a44_duplicate_ids_pass", PLG, "    for d in sorted({x for x in ids if ids.count(x) > 1}):",
     "    for d in []:", A44T, "test_2_duplicate_id"),
    ("a44_entry_null_row_any_reason", PLG, '        elif rs is None and rr != "not_authored":',
     "        elif False:", A44T, "test_5_entry_row_null_iff_not_authored"),
    ("a44_root_reason_with_row", PLG,
     '        if rs is not None and rr is not None:\n            v.append(f"{slug}: row_spacing_reason',
     '        if False:\n            v.append(f"{slug}: row_spacing_reason',
     A44T, "test_reason_non_null_while_row_present"),
    ("a44_migration_any_entry", PLG, '            and e.get("sources") == [] and e.get("anchoring_urls") == {})',
     '            and e.get("sources") == [])', A44T, "test_a_waived_entry_still_needs_both_slots_empty_not_half"),
    ("a44_migration_any_id", PLG, '    return (w is not None and slug in M.ELIGIBLE and e.get("id") == w.get("entry_id")',
     '    return (w is not None and slug in M.ELIGIBLE', A44T, "test_the_waiver_covers_only_its_entry"),
    ("a44_shipped_armed", PLG, "PRESENCE_ARMED = False", "PRESENCE_ARMED = True",
     A44T, "test_the_tools_commit_ships_unarmed"),
    ("a44_not_wired", "whole_crop_gate.py", "_layout = _plg.check_crop(crop)", "_layout = []", A44E, None),
    ("a44_roster_not_in_gate_all", "gate_all.py",
     '                            ("planting_layout_gate", _pl["violations"], _plg.refusal(_pl))):',
     "                            ):", A44E, None),
    # ---- A62: planting_layout family + R5 waivers ------------------------------------------------
    ("a62_family_unnamed", SBR, '    "planting_layout": (("planting_layout",), "id", None),\n', "\n",
     A62T, "test_an_uncited_entry_FAILS_by_its_id"),
    ("a62_waiver_ignores_value", SBR, '    if have != _compact(w.get("in_row_inches")):', "    if False:",
     A62T, "test_a_migration_waiver_holds_only_while_byte_equal"),
    ("a62_waiver_value_loosened", SBR,
     '    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)\n\n\ndef migration_verdict',
     '    return json.dumps([float(x) for x in v] if isinstance(v, list) else v)\n\n\ndef migration_verdict',
     A62T, "test_a_migration_waiver_holds_only_while_byte_equal"),
    ("a62_waiver_off_the_list", SBR, "    if slug not in MIGRATION_ELIGIBLE:", "    if False:",
     A62T, "test_a_migration_waiver_off_the_R5_list_is_REFUSED"),
    ("a62_waiver_any_entry", SBR, ' or m.group(1) != w.get("entry_id"):', ":",
     A62T, "test_a_migration_waiver_names_its_entry"),
    ("a62_waivers_ship_full", "planting_layout_migration_known.py", "WAIVERS = {}",
     'WAIVERS = {"bok-choy": {"entry_id": "row-none", "in_row_inches": [8, 12], "hunt": "x"}}',
     A62T, "test_the_migration_set_is_the_R5_list_and_ships_empty"),
    # ---- is_microgreen / display_readiness / numeric_sanity / A25 -------------------------------
    ("ts_microgreen_truthy", "timing_spine_gate.py", '    return crop.get("zone_independent") is True',
     '    return bool(crop.get("zone_independent"))', TST, None),
    ("ts_microgreen_old_predicate", "timing_spine_gate.py", '    return crop.get("zone_independent") is True',
     '    return crop.get("spacing_inches") == []', TST, None),
    ("dr_null_anywhere", "display_readiness_gate.py",
     '    if sp is None and crop.get("zone_independent") is True:', "    if sp is None:", DRT, None),
    ("dr_zi_excuses_any_shape", "display_readiness_gate.py",
     '    if sp is None and crop.get("zone_independent") is True:',
     '    if crop.get("zone_independent") is True:', DRT, None),
    ("ns_ordering_dropped", "numeric_sanity_gate.py",
     '        if e.get("arrangement") == "row" and ir and rs and rs[-1] < ir[0]:', "        if False:", NST, None),
    ("ns_hill_ceiling_raised", "numeric_sanity_gate.py", "              360 if tree else 120)",
     "              360 if tree else 200)", NST, None),
    ("ns_root_row_unbounded", "numeric_sanity_gate.py",
     '    check(crop.get("row_spacing_inches"), f"row_spacing_inches (basis={basis})", 1, row_hi)',
     "    pass", NST, None),
    ("ns_rootstock_unbounded", "numeric_sanity_gate.py",
     '            check(r.get("spacing_inches"), f"rootstock_options[{i}].spacing_inches", 1, 360)',
     "            pass", NST, None),
    ("ns_plants_per_hill_unbounded", "numeric_sanity_gate.py",
     '        check(e.get("plants_per_hill"), f"{tag}.plants_per_hill", 1, 10)', "        pass", NST, None),
    ("a25_enums_unruled", "register_completeness_gate.py", '    "arrangement", "support", "row_spacing_reason",',
     "", RCT, None),
    # ---- the promote --------------------------------------------------------------------------
    ("p_fixed_list_set", PRM, "    if got != want:", "    if False:", PRT, "test_a_missing_crop_REFUSES"),
    ("p_null_set_unchecked", PRM, "    if nulls != NULL_SPACING_EXPECTED:", "    if False:",
     PRT, "test_null_spacing_beyond_the_microgreens_REFUSES"),
    ("p_base_pin_dropped", PRM, "    if got != BASE_SHA:", "    if False:", PRT, "test_the_base_pin"),
    ("p_evidence_coverage_dropped", PRM, "                if e.get(f) is not None and (slug, e[\"id\"], f) not in covered:",
     "                if False:", PRT, "test_a_figure_without_evidence_REFUSES"),
    ("p_quote_not_searched", PRM, "        if len(q) < 12 or q not in text_cache[r[\"sha256\"]]:",
     "        if len(q) < 12:", PRT, "test_a_quote_not_in_the_bytes_REFUSES"),
    ("p_bytes_unhashed", PRM, "            if sha256_bytes(raw) != r[\"sha256\"]:", "            if False:",
     PRT, "test_tampered_bytes_REFUSE"),
    ("p_value_unchecked", PRM, "        if compact(e[r[\"field\"]]) != r[\"value\"]:", "        if False:",
     PRT, "test_a_value_mismatch_REFUSES"),
    ("p_endpoint_unchecked", PRM, "        if not quote_states(r[\"field\"], json.loads(r[\"value\"]), r[\"quote\"]):",
     "        if False:", PRT, "test_a_quote_that_states_no_endpoint_REFUSES"),
    ("p_feet_not_converted", PRM, "    return bool(ends & nums) or bool({x / 12 for x in ends} & nums)",
     "    return bool(ends & nums)", PRT, "test_feet_on_the_page_states_inches"),
    ("p_manifest_unchecked", PRM, "        if r[\"url\"] not in man.get(r[\"sha256\"], set()):", "        if False:",
     PRT, "test_a_url_not_in_the_manifest_REFUSES"),
    ("p_url_not_the_anchor", PRM, "        if (e.get(\"anchoring_urls\") or {}).get(r[\"source_id\"], {}).get(\"url\") != r[\"url\"]:",
     "        if False:", PRT, "test_the_url_must_be_the_entrys_anchor"),
    ("p_source_not_the_entrys", PRM, "        if r[\"source_id\"] not in (e.get(\"sources\") or []):", "        if False:",
     PRT, "test_the_source_must_be_the_entrys"),
    ("p_catalog_unchecked", PRM, "                if s not in catalog:", "                if False:",
     PRT, "test_a_source_off_the_catalog_REFUSES"),
    ("p_moved_unverified", PRM, "                if not any((e.get(\"anchoring_urls\") or {}).get(sid, {}).get(\"url\") == old[sid][\"url\"]",
     "                if False and not any((e.get(\"anchoring_urls\") or {}).get(sid, {}).get(\"url\") == old[sid][\"url\"]",
     PRT, "test_moved_but_absent_REFUSES"),
    ("p_dropped_without_reason", PRM, "and set(how) == {\"dropped\"} and str(how[\"dropped\"]).strip()):",
     "and set(how) == {\"dropped\"}):", PRT, "test_dropped_needs_a_reason"),
    ("p_disposition_set_unchecked", PRM, "        if set(disp) != set(old):", "        if False:",
     PRT, "test_every_retired_anchor_is_dispositioned"),
    ("p_restatement_unscanned", PRM, "            if p not in adj:", "            if False:",
     PRT, "test_an_unadjudicated_restatement_REFUSES"),
    ("p_edited_without_edit", PRM, "            if adj[p] == \"edited\" and p not in edited:",
     "            if False:", PRT, "test_edited_without_an_edit_REFUSES"),
    ("p_stray_field_allowed", PRM, "        if stray:", "        if False:", PRT, "test_a_stray_crop_field_REFUSES"),
    ("p_diff_one_sided", PRM, "            if k not in a or k not in b:\n                out.add(path + (k,))",
     "            if k not in a or k not in b:\n                pass", PRT, "test_a_removed_crop_key_REFUSES"),
    ("p_shell_unchecked", PRM, "                refuse(f\"shell {slug} changed\")", "                pass",
     PRT, "test_a_shell_change_REFUSES"),
    ("p_top_level_value_unchecked", PRM, "        if k != \"crops\" and compact(pre[k]) != compact(post[k]):",
     "        if False:", PRT, "test_a_top_level_change_REFUSES"),
    ("p_top_level_set_unchecked", PRM, "    if set(pre) != set(post):", "    if False:",
     PRT, "test_a_top_level_key_added_REFUSES"),
    ("p_roster_order_unchecked", PRM,
     "    if [c[\"slug\"] for c in pre[\"crops\"]] != [c[\"slug\"] for c in post[\"crops\"]]:", "    if False:",
     PRT, "test_a_roster_reorder_REFUSES"),
    ("p_layout_not_verbatim", PRM, "            if compact(b[\"planting_layout\"]) != compact(s[\"planting_layout\"]):",
     "            if False:", PRT, "test_a_layout_not_the_stage_verbatim_REFUSES"),
    ("p_record_edit_allowed", PRM, "(RETIRED, \"rootstock_options\", \"verification_status\"):",
     "(RETIRED, \"rootstock_options\"):", PRT, "test_an_edit_to_a_record_REFUSES"),
    ("p_edit_reason_optional", PRM, "            if set(ed) != {\"path\", \"new\", \"reason\"} or not str(ed[\"reason\"]).strip():",
     "            if set(ed) != {\"path\", \"new\", \"reason\"}:", PRT, "test_an_edit_needs_a_reason"),
    ("p_edit_value_unchecked", PRM, "                if compact(node) != compact(ed[\"new\"]):", "                if False:",
     PRT, "test_a_tampered_edit_value_REFUSES"),
    ("p_rootstock_any_crop", PRM, "        if (\"rootstock_spacing\" in s) != (slug in ROOTSTOCK_CROPS):",
     "        if False:", PRT, "test_rootstock_spacing_off_apple_REFUSES"),
    ("p_rootstock_rows_partial", PRM, "            if sorted(s[\"rootstock_spacing\"]) != sorted(names):",
     "            if False:", PRT, "test_every_apple_row_is_present_or_null"),
    ("p_a44_not_run", PRM, "    if r[\"violations\"]:\n        refuse(f\"planting_layout_gate (armed)",
     "    if False:\n        refuse(f\"planting_layout_gate (armed)", PRT, "test_an_entry_that_fails_A44_REFUSES"),
    ("p_numeric_not_run", PRM, "            v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)",
     "            v = []", PRT, "test_a_numeric_bound_REFUSES"),
    ("p_waiver_value_unchecked", PRM, "            if compact(w[\"in_row_inches\"]) != compact(c.get(\"spacing_inches\")):",
     "            if False:", PRT, "test_a_waiver_off_the_base_value_REFUSES"),
    ("p_waiver_off_list", PRM, "            if slug not in MIG.ELIGIBLE:", "            if False:",
     PRT, "test_a_waiver_off_the_R5_list_REFUSES"),
]
SENTINEL = (A44T, '        self.assertEqual((G.CERT_FLOOR, G.ENTRY_FLOOR), (121, 113))',
            '        self.assertEqual((G.CERT_FLOOR, G.ENTRY_FLOOR), (999, 113))', "test_floors_are_literals")


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
    tmp = tempfile.mkdtemp(prefix="mut_pla10p1_")
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
