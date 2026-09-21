#!/usr/bin/env python3
"""mutate_pla465_mandarin_anchor_suite -- mutation harness for PLA-465's ucr_citrus anchor repair.
PLA-215 bar: one defect per guard family into a SCRATCH COPY; the driver for that guard must go RED.
Liveness: anchor preflight, MUTATION-APPLIED marker, a sentinel that must redden, positive control = the
WHOLE suite (a driver already red on the clean copy would grade its mutation caught for the wrong reason,
which is the convention widened at PLA-7 promote A1 and re-run across PLA-464/465), bytecode off, pytest
rc 5 graded BROKEN.

NOT COUNTED, and named here so the gap is a written list rather than silence:
 - the no-op repoint check (removed from the promote: unreachable behind the closed-target vocabulary).
 - the addenda COUNT total (removed from the promote: unreachable behind the per-entry summary compare).
Both are pinned by a driver in the suite that asserts WHICH guard catches the case instead."""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla465_mandarin_anchor.py"
SUITE = "test_promote_pla465_mandarin_anchor.py"
STAGING = "pla465_mandarin_anchor"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


def off1of2(two):
    a, b = two.split("\n")
    return off(a) + "\n" + b


A = {
 "entry": "    if got != BASE_SHA:",
 "spec_base": '    if spec.get("base_sha") != BASE_SHA:',
 "spec_target": '    if spec.get("crop") != CROP or spec.get("source_key") != KEY:',
 "spec_prior": '    if spec.get("old_url") != OLD_URL or spec.get("verified_before") != VERIFIED_BEFORE:',
 "count": '    if len(rows) != EXPECTED["repoints"]:',
 "paths": '    if [r["path"] for r in rows] != list(REPOINT_PATHS):',
 "row_keys": '        if set(r) != {"path", "from", "to", "verified", "why"}:',
 "dup_path": '        if r["path"] in seen:',
 "from_pin": '        if r["from"] != OLD_URL:',
 "to_vocab": '        if r["to"] not in ALLOWED_TARGETS:',
 "verified_after": '        if r["verified"] != VERIFIED_AFTER:',
 "why_text": '        if not (r["why"] or "").strip() or _bad_copy(r["why"]):',
 "split": '    if n0 != EXPECTED["to_crc0279"] or n1 != EXPECTED["to_crc3913"]:',
 "fa_keys": "    if set(fa) != set(FA_KEYS):",
 "fa_field": '    if fa["field"] != FA_FIELD or fa["date"] != VERIFIED_AFTER:',
 "fa_sources": '    if fa["sources"] != [KEY]:',
 "fa_note": '    if not (fa["note"] or "").strip() or _bad_copy(fa["note"]):',
 "fa_urls": '        if frag not in fa["note"]:',
 "add_shape": '    if set(a) != {"id", "mark", "suffix"}:',
 "add_target": '    if a["id"] != FINDING_ID or a["mark"] != ADDENDUM_MARK:',
 "add_marker": '    if not a["suffix"].startswith(ADDENDUM_MARK) or not a["suffix"].endswith("]"):',
 "add_emdash": '    if _bad_copy(a["suffix"]):',
 "expected": '    if spec["expected"] != EXPECTED:',
 "roster": '    if len(data["crops"]) != ROSTER:',
 "off_roster": "    if c is None:",
 "not_certified": '    if (c.get("verification_status") or {}).get("status") != CERTIFIED:',
 "census_pre": "    if found != declared:",
 "anchor_keys_pre": "        if not isinstance(rec, dict) or set(rec) != set(ANCHOR_KEYS):",
 "url_pre": '        if rec["url"] != OLD_URL:',
 "verified_pre": '        if rec["verified"] != VERIFIED_BEFORE:',
 "lists": '    if not isinstance(vs.get("field_additions"), list) or not isinstance(vs.get("open_findings"), list):',
 "fa_present": '    if any(x.get("field") == FA_FIELD for x in vs["field_additions"]):',
 "hits": "    if len(hits) != 1:",
 "already": '    if ADDENDUM_MARK in hits[0].get("summary", ""):',
 "dimension": "    if any(c.get(k) is not None for k in PDG.FIELDS):",
 "census_post": "    if census(c) != set(REPOINT_PATHS) | set(KEEP_PATHS) | set(HELD_PATHS):",
 "keepheld": '        if rec["url"] != OLD_URL or rec["verified"] != VERIFIED_BEFORE:',
 "landed": '        if rec["url"] != url or rec["verified"] != VERIFIED_AFTER:',
 "urlhealth": "    v = UHG.url_health_violations(c)\n    if v:",
 "dimgate": "    g = PDG.all_violations(post, presence=True)\n    if g:",
 "blocker": "    if blockers:",
 "top_keys": "    if set(pre) != set(post):",
 "top_change": '        if k != "crops" and _j(pre[k]) != _j(post[k]):',
 "roster_change": '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
 "untouched": "        if _j(pre_i[slug]) != _j(post_i[slug]):",
 "crop_keys": "    if set(s) != set(g):",
 "anchor_keys_post": "        if set(rec) != set(ANCHOR_KEYS):",
 "beyond": "        if _j(s[k]) != _j(probe[k]):",
 "vs_keys": "    if set(sv) != set(gv):",
 "vs_change": "        if _j(sv[k]) != _j(gv[k]):",
 "fa_len": "    if len(fa_post) != len(fa_pre) + 1:",
 "fa_prefix": "    if _j(fa_post[:len(fa_pre)]) != _j(fa_pre):",
 "fa_tail": '    if _j(fa_post[-1]) != _j(spec["field_addition"]):',
 "add_keys": "            if set(x) != set(y):",
 "add_summary": '                    if y[k] != x[k] + spec["addendum"]["suffix"]:',
 "add_field": "                elif _j(x[k]) != _j(y[k]):",
 "other_finding": "        elif _j(x) != _j(y):",
 # --- the drop and the findings (rulings of 2026-09-20)
 "drop_shape": '    if set(dr) != {"path", "source_key", "from", "why", "must_retain"}:',
 "drop_target": '    if dr["path"] != DROP_PATH or dr["source_key"] != KEY or dr["from"] != OLD_URL:',
 "drop_class": "    if dr[\"path\"] in set(REPOINT_PATHS) | set(KEEP_PATHS) | set(HELD_PATHS):",
 "drop_retain": '    if not dr["must_retain"]:',
 "drop_why": '    if not (dr["why"] or "").strip() or _bad_copy(dr["why"]):',
 "find_count": '    if len(fs) != EXPECTED["findings"]:',
 "find_ids": '    if tuple(f["entry"]["id"] for f in fs) != FINDING_IDS:',
 "find_crop": '        if f["crop"] != CROP:',
 "find_keys": "        if set(e) != set(RECORD_KEYS):",
 "find_block": '        if e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:',
 "find_status": '        if e["status"] not in STATUSES:',
 "find_route": '        if (e["status"] == "deferred") != (e["deferred_to"] is not None):',
 "find_empty": '        if not (e["summary"] or "").strip() or not (e["resolution_note"] or "").strip():',
 "find_emdash": '        if _bad_copy(e["summary"]) or _bad_copy(e["resolution_note"]):',
 "hashes": "        if d not in EVIDENCE_HASHES and d != BASE_SHA:",
 "cells_before": "    if len(declared) != CELLS_BEFORE:",
 "drop_cites": '    if not isinstance(srcs, list) or KEY not in srcs:',
 "drop_uncited_pre": "    if not remaining:",
 "drop_retain_pre": '    if remaining != list(spec["drop"]["must_retain"]):',
 "find_present": "        if any(x.get(\"id\") == fid for x in vs[\"open_findings\"]):",
 "drop_sources_post": '    if KEY in (node.get("sources") or []):',
 "drop_retain_post": '    if node.get("sources") != list(spec["drop"]["must_retain"]):',
 "drop_uncited_post": '    if not node.get("sources"):',
 "drop_applied": '    if KEY in (dnode.get("anchoring_urls") or {}) or KEY in (dnode.get("sources") or []):',
 "of_len": "    if len(of_post) != len(of_pre) + EXPECTED[\"findings\"]:",
 "of_tail": '    if _j(of_post[len(of_pre):]) != _j(want_tail):',
}
MUTATIONS = [
 ("entry", "base_sha_check_removed", A["entry"], off(A["entry"]), "test_refuses_a_canonical_that_is_not_the_base"),
 ("spec", "spec_base_not_checked", A["spec_base"], off(A["spec_base"]), "test_refuses_a_spec_on_another_base"),
 ("spec", "crop_and_key_not_pinned", A["spec_target"], off(A["spec_target"]), "test_refuses_a_spec_targeting_another_crop_or_key"),
 ("spec", "prior_anchor_not_pinned", A["spec_prior"], off(A["spec_prior"]), "test_refuses_a_spec_that_does_not_pin_the_prior_anchor"),
 ("spec", "repoint_count_not_pinned", A["count"], off(A["count"]), "test_refuses_a_repoint_count_drift"),
 ("spec", "repoint_paths_not_pinned", A["paths"], off(A["paths"]), "test_refuses_repoint_paths_that_are_not_the_pinned_set"),
 ("spec", "row_keys_not_checked", A["row_keys"], off(A["row_keys"]), "test_refuses_a_repoint_row_with_the_wrong_keys"),
 ("spec", "duplicate_path_accepted", A["dup_path"], off(A["dup_path"]), "test_refuses_a_duplicated_repoint_path"),
 ("spec", "from_url_not_pinned", A["from_pin"], off(A["from_pin"]), "test_refuses_a_repoint_that_does_not_move_off_the_defective_anchor"),
 ("spec", "target_vocabulary_open", A["to_vocab"], off(A["to_vocab"]), "test_refuses_a_repoint_to_an_unadjudicated_accession"),
 ("spec", "stale_verified_date_accepted", A["verified_after"], off(A["verified_after"]), "test_refuses_a_repoint_carrying_a_stale_verified_date"),
 ("spec", "rationale_not_required", A["why_text"], off(A["why_text"]), "test_refuses_an_empty_or_em_dashed_rationale"),
 ("spec", "target_split_not_pinned", A["split"], off(A["split"]), "test_refuses_a_target_split_drift"),
 ("spec", "fa_keys_not_checked", A["fa_keys"], off(A["fa_keys"]), "test_refuses_a_field_addition_with_the_wrong_keys"),
 ("spec", "fa_field_not_named", A["fa_field"], off(A["fa_field"]), "test_refuses_a_field_addition_that_does_not_name_the_field"),
 ("spec", "fa_source_not_checked", A["fa_sources"], off(A["fa_sources"]), "test_refuses_a_field_addition_crediting_the_wrong_source"),
 ("spec", "fa_note_em_dash_accepted", A["fa_note"], off(A["fa_note"]), "test_refuses_an_em_dashed_provenance_note"),
 ("spec", "fa_note_urls_not_required", A["fa_urls"], off(A["fa_urls"]), "test_refuses_a_provenance_note_that_does_not_name_the_urls"),
 ("spec", "addendum_shape_not_checked", A["add_shape"], off(A["add_shape"]), "test_refuses_an_addendum_shape"),
 ("spec", "addendum_target_not_pinned", A["add_target"], off(A["add_target"]), "test_refuses_an_addendum_targeting_another_finding"),
 ("spec", "addendum_marker_not_checked", A["add_marker"], off(A["add_marker"]), "test_refuses_an_addendum_without_the_dated_marker"),
 ("spec", "addendum_em_dash_accepted", A["add_emdash"], off(A["add_emdash"]), "test_refuses_an_em_dash_in_the_addendum"),
 ("spec", "expected_block_not_compared", A["expected"], off(A["expected"]), "test_refuses_an_expected_block_drift"),
 ("prestate", "roster_not_pinned", A["roster"], off(A["roster"]), "test_refuses_a_roster_drift"),
 ("prestate", "off_roster_accepted", A["off_roster"], off(A["off_roster"]), "test_refuses_a_crop_off_the_roster"),
 ("prestate", "uncertified_accepted", A["not_certified"], off(A["not_certified"]), "test_refuses_an_uncertified_crop"),
 ("prestate", "census_not_compared", A["census_pre"], off(A["census_pre"]), "test_refuses_a_census_with_an_unaccounted_cell or test_refuses_a_census_that_lost_a_cell"),
 ("prestate", "anchor_record_keys_not_checked", A["anchor_keys_pre"], off(A["anchor_keys_pre"]), "test_refuses_an_anchor_record_with_the_wrong_keys"),
 ("prestate", "prior_url_not_asserted", A["url_pre"], off(A["url_pre"]), "test_refuses_a_cell_not_on_the_defective_anchor"),
 ("prestate", "prior_date_not_asserted", A["verified_pre"], off(A["verified_pre"]), "test_refuses_a_cell_at_another_verified_date"),
 ("prestate", "list_shape_not_checked", A["lists"], off(A["lists"]), "test_refuses_field_additions_not_a_list"),
 ("prestate", "existing_provenance_accepted", A["fa_present"], off(A["fa_present"]), "test_refuses_a_provenance_record_already_present"),
 ("prestate", "target_count_not_checked", A["hits"], off(A["hits"]), "test_refuses_an_addendum_target_not_found_once"),
 ("prestate", "applied_addendum_accepted", A["already"], off(A["already"]), "test_refuses_an_addendum_already_applied"),
 ("prestate", "valued_crop_accepted", A["dimension"], off(A["dimension"]), "test_refuses_a_crop_that_carries_a_dimension"),
 ("post", "census_change_invisible", A["census_post"], off(A["census_post"]), "test_refuses_a_census_change_across_the_write"),
 ("post", "keep_and_held_not_pinned", A["keepheld"], off(A["keepheld"]), "test_refuses_a_keep_cell_that_moved or test_refuses_a_held_cell_that_moved"),
 ("post", "repoint_landing_not_checked", A["landed"], off(A["landed"]), "test_refuses_a_repoint_that_did_not_land"),
 ("post", "url_health_not_run", A["urlhealth"], "    v = UHG.url_health_violations(c)\n    if False:  " + MARKER, "test_refuses_a_post_state_that_fails_url_health"),
 ("post", "dimension_gate_not_run", A["dimgate"], "    g = PDG.all_violations(post, presence=True)\n    if False:  " + MARKER, "test_refuses_a_post_state_that_fails_the_dimensions_gate"),
 ("post", "blocker_not_checked", A["blocker"], off(A["blocker"]), "test_refuses_a_launch_blocker_after_the_write"),
 ("blast", "top_level_key_set_not_compared", A["top_keys"], off(A["top_keys"]), "test_refuses_a_top_level_key_addition"),
 ("blast", "top_level_change_invisible", A["top_change"], off(A["top_change"]), "test_refuses_a_top_level_change"),
 ("blast", "roster_change_invisible", A["roster_change"], off(A["roster_change"]), "test_refuses_a_roster_change"),
 ("blast", "untouched_change_invisible", A["untouched"], off(A["untouched"]), "test_refuses_an_untouched_crop_change"),
 ("blast", "crop_key_set_not_compared", A["crop_keys"], off(A["crop_keys"]), "test_refuses_a_crop_level_key_addition"),
 ("blast", "anchor_key_set_not_compared", A["anchor_keys_post"], off(A["anchor_keys_post"]), "test_refuses_an_anchor_record_key_addition"),
 ("blast", "change_beyond_anchors_invisible", A["beyond"], off(A["beyond"]), "test_refuses_a_change_beyond_the_seven_anchor_records or test_refuses_a_prose_change_on_the_repaired_crop"),
 ("blast", "vs_key_set_not_compared", A["vs_keys"], off(A["vs_keys"]), "test_refuses_a_verification_status_key_addition"),
 ("blast", "vs_change_invisible", A["vs_change"], off(A["vs_change"]), "test_refuses_a_verification_status_value_change"),
 ("blast", "extra_field_addition_invisible", A["fa_len"], off(A["fa_len"]), "test_refuses_more_than_one_field_addition_append"),
 ("blast", "fa_prefix_not_compared", A["fa_prefix"], off(A["fa_prefix"]), "test_refuses_a_rewritten_field_additions_prefix"),
 ("blast", "fa_tail_not_compared", A["fa_tail"], off(A["fa_tail"]), "test_refuses_an_appended_field_addition_other_than_the_spec"),
 ("blast", "extra_findings_append_invisible", A["of_len"], off(A["of_len"]), "test_refuses_an_extra_open_findings_append"),
 ("blast", "findings_tail_not_compared", A["of_tail"], off(A["of_tail"]), "test_refuses_an_appended_finding_other_than_the_spec"),
 ("blast", "drop_not_applied_invisible", A["drop_applied"], off(A["drop_applied"]), "test_refuses_a_drop_that_did_not_happen"),
 ("blast", "addendum_key_set_not_compared", A["add_keys"], off(A["add_keys"]), "test_refuses_an_addendum_target_key_addition"),
 ("blast", "addendum_summary_not_compared", A["add_summary"], off(A["add_summary"]), "test_refuses_an_addendum_summary_other_than_original_plus_suffix or test_an_unapplied_addendum_refuses_on_the_summary_not_the_count"),
 ("blast", "addendum_field_change_invisible", A["add_field"], off(A["add_field"]), "test_refuses_an_addendum_target_field_change"),
 ("blast", "other_finding_change_invisible", A["other_finding"], off(A["other_finding"]), "test_refuses_another_open_finding_change"),
 ("drop", "drop_shape_not_checked", A["drop_shape"], off(A["drop_shape"]), "test_refuses_a_drop_block_with_the_wrong_shape"),
 ("drop", "drop_target_not_pinned", A["drop_target"], off(A["drop_target"]), "test_refuses_a_drop_targeting_another_cell_or_key"),
 ("drop", "drop_class_overlap_accepted", A["drop_class"], off(A["drop_class"]), "test_refuses_a_drop_of_a_cell_another_class_claims"),
 ("drop", "retained_source_not_required", A["drop_retain"], off(A["drop_retain"]), "test_refuses_a_drop_that_names_no_retained_source"),
 ("drop", "drop_rationale_not_required", A["drop_why"], off(A["drop_why"]), "test_refuses_an_empty_or_em_dashed_drop_rationale"),
 ("drop", "drop_cite_precondition_skipped", A["drop_cites"], off(A["drop_cites"]), "test_refuses_a_drop_when_the_cell_does_not_cite_the_key"),
 ("drop", "UNCITED_CELL_ACCEPTED", A["drop_uncited_pre"], off(A["drop_uncited_pre"]), "test_refuses_a_drop_that_would_leave_the_cell_uncited"),
 ("drop", "retained_set_drift_invisible", A["drop_retain_pre"], off(A["drop_retain_pre"]), "test_refuses_a_retained_source_set_that_moved_since_staging"),
 ("drop", "dangling_source_credit_accepted", A["drop_sources_post"], off(A["drop_sources_post"]), "test_refuses_a_drop_left_in_sources"),
 ("drop", "post_retained_set_not_checked", A["drop_retain_post"], off(A["drop_retain_post"]), "test_refuses_a_dropped_cell_left_uncited_in_the_post_state"),
 ("findings", "findings_count_not_pinned", A["find_count"], off(A["find_count"]), "test_refuses_a_findings_count_drift"),
 ("findings", "finding_ids_not_pinned", A["find_ids"], off(A["find_ids"]), "test_refuses_finding_ids_that_are_not_the_pinned_ids"),
 ("findings", "finding_crop_not_checked", A["find_crop"], off(A["find_crop"]), "test_refuses_a_finding_on_another_crop"),
 ("findings", "finding_keys_not_checked", A["find_keys"], off(A["find_keys"]), "test_refuses_a_finding_with_the_wrong_keys"),
 ("findings", "blocking_finding_accepted", A["find_block"], off(A["find_block"]), "test_refuses_a_blocking_finding"),
 ("findings", "finding_status_vocab_open", A["find_status"], off(A["find_status"]), "test_refuses_a_finding_status_outside_the_vocabulary"),
 ("findings", "route_iff_not_checked", A["find_route"], off(A["find_route"]), "test_refuses_a_deferred_finding_with_no_route"),
 ("findings", "empty_finding_accepted", A["find_empty"], off(A["find_empty"]), "test_refuses_an_empty_finding_summary"),
 ("findings", "finding_em_dash_accepted", A["find_emdash"], off(A["find_emdash"]), "test_refuses_an_em_dash_in_a_finding"),
 ("findings", "present_finding_accepted", A["find_present"], off(A["find_present"]), "test_refuses_a_finding_already_present"),
 ("evidence", "FABRICATED_SHA256_ACCEPTED", A["hashes"], off(A["hashes"]), "test_refuses_a_fabricated_sha256_anywhere_in_the_spec"),
 ("prestate", "cells_before_not_pinned", A["cells_before"], off(A["cells_before"]), "test_refuses_a_class_enumeration_that_does_not_cover_nineteen"),
 ("serialize", "indent_reintroduced", '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
  '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER, "test_compact_no_trailing_newline"),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_CELLS = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_CELLS pin")
    return ("sentinel", "cells_pin_broken", m.group(0), f"N_CELLS = {int(m.group(1)) + 99999}  " + MARKER,
            "test_pins_are_the_literals", SUITE)


def preflight(tools_dir):
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = [f"  {fam}/{name}: anchor matches {src.count(old)} times\n      {old[:90]!r}"
           for fam, name, old, _n, _s in MUTATIONS if src.count(old) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla465anchor_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING), os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "-k", selector,
                        "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
    return r.returncode, (r.stdout + r.stderr)


def apply_mutation(tools_dir, old, new, target=PROMOTE):
    path = os.path.join(tools_dir, target)
    clean = open(path, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times in {target}"
    mutated = clean.replace(old, new, 1)
    if mutated == clean:
        return None, "replacement produced identical bytes"
    open(path, "w", encoding="utf-8").write(mutated)
    back = open(path, encoding="utf-8").read()
    if MARKER not in back or back == clean:
        return None, "mutation not on disk"
    return clean, None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--family"); ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        fams = {}
        for fam, name, *_ in MUTATIONS:
            fams.setdefault(fam, []).append(name)
        for f, names in fams.items():
            print(f"{f} ({len(names)})"); [print(f"    {n}") for n in names]
        return 0
    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)
        rc, out = run_suite(tools, "test_")
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing; a red driver would grade its mutation caught for the wrong reason.")
        print("positive control: the WHOLE unmutated suite is GREEN")
        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
        print("sentinel: reddened as required\n")
        muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in muts:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err)); print(f"  BROKEN   {fam}/{name}: {err}"); continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, "collected no tests")); print(f"  BROKEN   {fam}/{name}: collected no tests")
            elif rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        for f, n, e in broken: print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived: print(f"  SURVIVED {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
