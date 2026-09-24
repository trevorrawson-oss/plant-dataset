#!/usr/bin/env python3
"""mutate_pla581_critical_warnings_suite -- mutation harness for the PLA-581 promote and gate A61.

BUILT TO THE PLA-215 BAR: one defect per guard family injected into a SCRATCH COPY of the source;
the suite's own driver for that guard must go RED. Liveness: anchor preflight (each anchor exactly
once in its own target file), MUTATION-APPLIED marker on disk, a sentinel that MUST redden, a
positive control that runs EVERY suite whole (promote suite, gate suite, and the A61 entry-point
script), bytecode off, pytest rc 5 graded BROKEN.

THE null -> [] CLASS, BY NAME. critical_warnings has three states and null vs [] is the one that
matters: the PLA-533 ratchet collapses them on purpose (`not (x or [])`), and here that idiom would
make every crop read "assessed, none found" and still pass. Four mutations exist for it:
  * one_crop_null_written_as_empty_list  -- the DATA mutation: the promote writes [] for one crop.
  * null_checked_by_truthiness           -- verify_post's identity check replaced by the collapse.
  * state_of_collapses_empty_into_null   -- the gate's reader collapses the two states.
  * empty_list_record_not_required       -- the gate stops requiring a record behind [].
Each must be CAUGHT; the report lists them by name.

NOT COUNTED, removed rather than shipped unreachable:
  * spec rule 9 (a sourceless SAFETY entry), subsumed by rule 8 (sources non-empty on EVERY entry).
  * verify_post's closing `nulls != 121` total, implied by check_pre_state's certified pin plus the
    per-crop identity check.
  * the gate's "stage must be on THIS crop's ladder, not the roster's union" has a driver
    (test_control_1_a_stage_valid_on_another_crop_is_refused_here) but no code mutation: the ladder
    is computed from the crop in one line, and replacing it with a roster-wide set needs the data
    the gate is not handed. Recorded as unmutated, not claimed.

Usage: mutate_pla581_critical_warnings_suite.py [--family X] [--list]
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla581_critical_warnings.py"
GATE = "critical_warnings_gate.py"
SUITE = "test_promote_pla581_critical_warnings.py"
GATE_SUITE = "test_critical_warnings_gate.py"
A61_SCRIPT = "test_gate_critical_warnings_a61.py"
STAGING = "pla581_critical_warnings"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


def off2(two):
    """A two-line anchor whose SECOND line is the guard."""
    a, b = two.split("\n")
    return a + "\n" + off(b)


def off1of2(two):
    """A two-line anchor whose FIRST line is the guard."""
    a, b = two.split("\n")
    return off(a) + "\n" + b


def M(fam, name, old, new, sel, tgt=PROMOTE, suite=SUITE):
    return (fam, name, old, new, sel, tgt, suite)


def G_(fam, name, old, new, sel):
    return (fam, name, old, new, sel, GATE, GATE_SUITE)


p_ = {  # promote anchors
 "entry": "    if got != BASE_SHA:",
 "evidence_empty": "    if not EVIDENCE_HASHES:",
 "spec_base": '    if spec.get("base_sha") != BASE_SHA:',
 "fetch_date": '    if spec.get("fetch_date") != FETCH_DATE:',
 "pages_set": "    if len(by_url) != len(pages) or set(by_url) != set(EVIDENCE_HASHES):",
 "page_digest": '        if p["sha256"] != EVIDENCE_HASHES[url]:',
 "evidence_set": "    if set(ev) != set(EVIDENCE):",
 "evidence_value": '        if [(e["url"], e["sentence"]) for e in ev[wid]] != list(pairs):',
 "scan": "        if d not in MEASURED_DIGESTS and d != BASE_SHA:",
 "cut_set": '    if {c.get("candidate") for c in cut} != EXPECTED_CUT or len(cut) != len(EXPECTED_CUT):',
 "cut_why": '        if set(c) != {"candidate", "why"} or not (c["why"] or "").strip():',
 "cs_keys": "    if set(cs) != set(CWG.CS_KEYS):",
 "ids": '    if [w.get("id") for w in ws] != EXPECTED_IDS:',
 "class_stage": '        if w["class"] != "safety" or w["stage"] is not None:',
 "severity": '        if w["severity"] != EXPECTED_SEVERITY:',
 "title": '        if w["title"] != EXPECTED_TITLES[wid] or w["title"] != copy_ok[wid][0]:',
 "body": '        if (w["body_beginner"], w["body_seasoned"]) != copy_ok[wid][1:]:',
 "sources": '        if sorted(w["sources"]) != sorted(want):',
 "anchors": '            if w["anchoring_urls"].get(s) != {"url": url, "verified": FETCH_DATE}:',
 "records": '    if len(recs) != len(cs["field_additions"]) or set(recs) != {f"{DKEY}.{i}" for i in EXPECTED_IDS}:',
 "record_date": '        if r["date"] != FETCH_DATE:',
 "record_digest": '            if EVIDENCE_HASHES[url] not in r["note"]:',
 "record_verbatim": '            if sentence not in r["note"]:',
 "doc_ids": "    if sorted(out) != sorted(EXPECTED_IDS):",
 "roster": '    if len(data["crops"]) != ROSTER:',
 "certified": "    if len(cert) != EXPECTED_CERTIFIED:",
 "dkey_pre": "    if DKEY in data:",
 "field_pre": "        if FIELD in c:",
 "record_pre": '        if any(isinstance(x, dict) and str(x.get("field", "")).startswith((FIELD, DKEY)) for x in fa):',
 "gate_pre": "    v = CWG.dataset_violations(syn, presence=True)\n    if v:",
 "gate_post": "    v = CWG.all_violations(post, presence=True)\n    if v:",
 "population": "    if p != EXPECTED_POPULATION:",
 "top_keys": "    if set(post) != set(pre) | {DKEY} or DKEY in pre:",
 "top_change": '        if k != "crops" and _j(pre[k]) != _j(post[k]):',
 "cs_written": "    if _j(post[DKEY]) != _j(spec[DKEY]):",
 "roster_change": '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
 "shell": '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
 "crop_keys": "        if set(g) != set(s) | {FIELD}:",
 "field_change": "            if _j(s[k]) != _j(g[k]):",
 "out_canon": "    if args.out and os.path.abspath(args.out) == os.path.abspath(args.canonical or CANON):",
 "expect_mismatch": "    if args.expect_sha and new_sha != args.expect_sha:",
 "expect_required": "    if not args.expect_sha:",
}
EXPECTED_OLD = ('    if spec.get("expected") != {"certified_null": EXPECTED_CERTIFIED, "shells": EXPECTED_SHELLS,\n'
                '                                "warnings": EXPECTED_WARNINGS, "records": EXPECTED_WARNINGS,\n'
                '                                "pages": EXPECTED_PAGES}:')
LOCATE_OLD = '        raise SystemExit("REFUSED: cannot locate section 14 in the approved spec")'
WRAP_OLD = '    for m in re.finditer(r"\\*\\*`(\\w+)`\\*\\*(?:(?!\\*\\*`).)*?\\n\\n- \\*title:\\* \\"(.*?)\\"\\s*\\n- \\*beginner:\\* \\"(.*?)\\"\\s*\\n"'
WRAP_NEW = WRAP_OLD.replace('(?:(?!\\*\\*`).)*?', '[^\\n]*') + "  " + MARKER
NULL_OLD = "        if g[FIELD] is not None:"
APPLY_OLD = "            c[FIELD] = None"

g_ = {  # gate anchors
 "state_null": '    if v is None:\n        return "null"',
 "record_rule": "    if not _has_record(crop):",
 "invalid": '    if st == "invalid":',
 "shell": '    if not _certified(crop):\n        return [f"{slug}: {FIELD} present on an uncertified crop; the shells carry no key "',
 "entry_keys": "    if not isinstance(e, dict) or set(e) != set(ENTRY_KEYS):",
 "id": '    if not (isinstance(e["id"], str) and id_re.fullmatch(e["id"])):',
 "class": '    if e["class"] not in CLASSES:',
 "severity": '    if e["severity"] not in SEVERITIES:',
 "stage": '    if e["stage"] is not None and not (isinstance(e["stage"], str) and e["stage"] in ladder):',
 "prose_empty": "        if not (isinstance(s, str) and s.strip()):",
 "prose_dash": '        if "\u2014" in s or "\u2013" in s:',
 "prose_hyphens": '        if "--" in s:',
 "sources": "    if not (isinstance(srcs, list) and srcs and all(isinstance(s, str) and s for s in srcs)):",
 "catalog": "        if not isinstance(cat, dict):",
 "t1": '        elif cat.get("tier") != "T1":',
 "anchor_missing": "        if not isinstance(a, dict):",
 "anchor_keys": "        if set(a) != set(ANCHOR_KEYS):",
 "anchor_url": '        if not (isinstance(a["url"], str) and a["url"].startswith("http")):',
 "anchor_extra": "    if extra:",
 "dup": "        if i in seen:",
 "presence": "    if FIELD not in crop:\n        return [f\"{crop.get('slug') or '?'}: {FIELD} missing",
 "cs_shape": "    if not isinstance(v, dict) or set(v) != set(CS_KEYS):",
 "cs_empty": "    if not isinstance(ws, list) or not ws:",
 "cs_class": '        if "class" in e and e["class"] != "safety":',
 "cs_figure": "                if m:",
 "cs_records": "    if len(got) != len(ws) or set(got) != want:",
 "cs_record_keys": "        if set(r) != set(RECORD_KEYS):",
 "cs_record_date": '        if not (isinstance(r["date"], str) and _DATE.fullmatch(r["date"])):',
 "cs_credit": '        if sorted(r["sources"] or []) != sorted(e["sources"] or []):',
 "cs_url": "            if u and u not in note:",
 "cs_sha": "        if not _SHA.search(note):",
 "cs_verbatim": '        if "verbatim:" not in note:',
 "cs_dash": '        if "\u2014" in note or "\u2013" in note:',
}
DATE_OLD = '        if not (isinstance(a["verified"], str) and _DATE.fullmatch(a["verified"])):'
CS_PRESENCE_OLD = '                 f"live here once, rendered on every container_ok crop)"] if presence else [])'
SMALL_OLD = '_SMALL = "one|two|three|four|five|six|seven|eight|nine|ten"'
TEENS_OLD = '_TEENS = "eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"'
LARGE_OLD = '_LARGE = "dozen|hundred|thousand"'
TENS_OLD = '_TENS = "thirty|forty|fifty|sixty|seventy|eighty|ninety"'
HALF_OLD = '_HALF = "half"'
BOUNDARY_OLD = '_FIGURE = re.compile(r"\\d|\\b(" + "|".join((_SMALL, _TEENS, _TENS, _HALF, _LARGE)) + r")\\b", re.I)'
REG_OLD = '    if k == "class" and pat.endswith("critical_warnings[]"): return True'
WIRE_OLD = 'for m in _cwv:\n    fail(f"critical-warnings: {m}")'

MUTATIONS = [
 # ---- THE null -> [] CLASS -------------------------------------------------------------------
 M("null_vs_empty", "one_crop_null_written_as_empty_list", APPLY_OLD,
   f'            c[FIELD] = [] if c["slug"] == "basil" else None  {MARKER}',
   "test_the_whole_pipeline_passes_and_writes_null_everywhere"),
 M("null_vs_empty", "null_checked_by_truthiness", NULL_OLD,
   f"        if (g[FIELD] or []):  {MARKER}",
   "test_refuses_an_empty_list_where_the_ruling_writes_null"),
 G_("null_vs_empty", "state_of_collapses_empty_into_null", g_["state_null"],
    f'    if not v:  {MARKER}\n        return "null"',
    "test_control_5_the_reader_never_coerces_null_to_empty"),
 G_("null_vs_empty", "empty_list_record_not_required", g_["record_rule"], off(g_["record_rule"]),
    "test_empty_list_without_a_record_is_refused"),

 # ---- promote: entry + spec shape -------------------------------------------------------------
 M("entry", "base_sha_check_removed", p_["entry"], off(p_["entry"]),
   "test_refuses_a_canonical_that_is_not_the_base"),
 M("spec", "unmeasured_run_accepted", p_["evidence_empty"], off(p_["evidence_empty"]),
   "test_refuses_when_no_digest_is_measured"),
 M("spec", "spec_base_not_checked", p_["spec_base"], off(p_["spec_base"]),
   "test_refuses_a_spec_on_another_base"),
 M("spec", "fetch_date_not_pinned", p_["fetch_date"], off(p_["fetch_date"]),
   "test_refuses_a_fetch_date_drift"),
 M("spec", "expected_block_not_compared", EXPECTED_OLD, f"    if False:  {MARKER}",
   "test_refuses_an_expected_block_drift"),
 M("spec", "page_set_not_pinned", p_["pages_set"], off(p_["pages_set"]),
   "test_refuses_a_page_set_other_than_the_measured_one"),
 M("spec", "digest_swap_between_pages_invisible", p_["page_digest"], off(p_["page_digest"]),
   "test_refuses_digests_swapped_between_two_pages"),
 M("spec", "evidence_set_not_compared", p_["evidence_set"], off(p_["evidence_set"]),
   "test_refuses_evidence_for_a_missing_warning"),
 M("spec", "evidence_sentences_not_compared", p_["evidence_value"], off(p_["evidence_value"]),
   "test_refuses_evidence_other_than_the_ruled_sentences"),
 M("spec", "fabricated_digest_accepted", p_["scan"], off(p_["scan"]),
   "test_refuses_a_fabricated_digest"),
 M("spec", "cut_ledger_not_compared", p_["cut_set"], off(p_["cut_set"]),
   "test_refuses_a_cut_ledger_missing_the_mosquito"),
 M("spec", "reasonless_cut_accepted", p_["cut_why"], off(p_["cut_why"]),
   "test_refuses_a_cut_with_no_reason"),
 M("spec", "container_safety_keys_not_checked", p_["cs_keys"], off(p_["cs_keys"]),
   "test_refuses_an_extra_key_in_container_safety"),
 M("spec", "warning_ids_not_compared", p_["ids"], off(p_["ids"]),
   "test_refuses_a_warning_order_swap or test_refuses_a_fourth_warning"),
 M("spec", "class_or_stage_not_checked", p_["class_stage"], off(p_["class_stage"]),
   "test_refuses_a_non_null_stage"),
 M("spec", "severity_not_pinned", p_["severity"], off(p_["severity"]),
   "test_refuses_a_critical_severity"),
 M("spec", "title_not_pinned", p_["title"], off(p_["title"]),
   "test_refuses_an_edited_title"),
 M("spec", "title_not_compared_to_section_14", p_["title"],
   '        if w["title"] != EXPECTED_TITLES[wid]:  ' + MARKER,
   "test_refuses_a_title_the_spec_doc_does_not_carry"),
 M("spec", "wrapped_header_not_read", WRAP_OLD, WRAP_NEW,
   "test_the_approved_copy_is_read_from_the_spec_document"),
 M("spec", "body_not_compared_to_the_approved_spec", p_["body"], off(p_["body"]),
   "test_refuses_body_copy_not_in_the_approved_spec"),
 M("spec", "sources_not_compared", p_["sources"], off(p_["sources"]),
   "test_refuses_a_dropped_second_source"),
 M("spec", "anchors_not_compared", p_["anchors"], off(p_["anchors"]),
   "test_refuses_an_anchor_at_another_url or test_refuses_an_anchor_verified_on_another_date"),
 M("spec", "record_set_not_compared", p_["records"], off(p_["records"]),
   "test_refuses_a_missing_record"),
 M("spec", "record_date_not_pinned", p_["record_date"], off(p_["record_date"]),
   "test_refuses_a_record_date_drift"),
 M("spec", "record_digest_not_per_page", p_["record_digest"], off(p_["record_digest"]),
   "test_refuses_a_record_quoting_another_pages_digest or test_refuses_a_two_source_record_missing_one_digest "
   "or test_refuses_a_record_missing_the_unanchored_pages_digest"),
 M("spec", "record_sentence_not_required", p_["record_verbatim"], off(p_["record_verbatim"]),
   "test_refuses_a_record_without_its_sentence"),
 M("spec", "spec_doc_section_not_required", LOCATE_OLD, f'        sec = ""  {MARKER}',
   "test_refuses_a_spec_doc_without_section_14"),
 M("spec", "spec_doc_ids_not_compared", p_["doc_ids"], off(p_["doc_ids"]),
   "test_refuses_a_spec_doc_yielding_other_ids"),

 # ---- promote: pre-state ----------------------------------------------------------------------
 M("prestate", "roster_not_pinned", p_["roster"], off(p_["roster"]), "test_refuses_a_roster_drift"),
 M("prestate", "certified_count_not_pinned", p_["certified"], off(p_["certified"]),
   "test_refuses_a_certified_count_drift"),
 M("prestate", "existing_dataset_key_accepted", p_["dkey_pre"], off(p_["dkey_pre"]),
   "test_refuses_a_dataset_already_carrying_container_safety"),
 M("prestate", "existing_crop_key_accepted", p_["field_pre"], off(p_["field_pre"]),
   "test_refuses_a_crop_already_carrying_the_key"),
 M("prestate", "prior_record_accepted", p_["record_pre"], off(p_["record_pre"]),
   "test_refuses_a_prior_record"),
 M("prestate", "gate_not_run_on_the_staged_object", p_["gate_pre"], off2(p_["gate_pre"]),
   "test_refuses_a_staged_object_the_gate_rejects"),

 # ---- promote: post ---------------------------------------------------------------------------
 M("post", "gate_not_run_on_post", p_["gate_post"], off2(p_["gate_post"]),
   "test_refuses_a_post_state_that_fails_the_gate"),
 M("post", "inspected_population_not_pinned", p_["population"], off(p_["population"]),
   "test_refuses_an_inspected_population_other_than_pinned"),

 # ---- promote: blast radius -------------------------------------------------------------------
 M("blast", "top_level_key_set_not_compared", p_["top_keys"], off(p_["top_keys"]),
   "test_refuses_a_top_level_key_addition or test_refuses_a_top_level_key_removal"),
 M("blast", "top_level_change_invisible", p_["top_change"], off(p_["top_change"]),
   "test_refuses_a_source_catalog_change"),
 M("blast", "written_object_not_compared", p_["cs_written"], off(p_["cs_written"]),
   "test_refuses_a_written_object_other_than_the_staged_one"),
 M("blast", "roster_change_invisible", p_["roster_change"], off(p_["roster_change"]),
   "test_refuses_an_appended_crop"),
 M("blast", "shell_change_invisible", p_["shell"], off1of2(p_["shell"]), "test_refuses_a_shell_change"),
 M("blast", "crop_key_set_not_compared", p_["crop_keys"], off(p_["crop_keys"]),
   "test_refuses_a_crop_level_key_addition or test_refuses_a_certified_crop_missing_the_key"),
 M("blast", "outside_change_invisible", p_["field_change"], off(p_["field_change"]),
   "test_refuses_a_change_outside_the_new_key"),
 M("blast", "null_identity_check_removed", NULL_OLD, off(NULL_OLD),
   "test_refuses_a_false_where_the_ruling_writes_null"),

 # ---- promote: the write --------------------------------------------------------------------
 M("write", "out_may_target_the_canonical", p_["out_canon"], off(p_["out_canon"]),
   "test_out_may_not_target_the_canonical"),
 M("write", "expect_sha_mismatch_ignored", p_["expect_mismatch"], off(p_["expect_mismatch"]),
   "test_a_wrong_expect_sha_refuses_and_writes_nothing"),
 M("write", "write_without_expect_sha", p_["expect_required"], off(p_["expect_required"]),
   "test_a_write_requires_expect_sha"),
 M("write", "pending_titles_reported_empty",
   '    return [w["id"] for w in spec[DKEY]["warnings"] if TITLE_PENDING.search(w["title"])]',
   f"    return []  {MARKER}",
   "test_pending_titles_names_every_placeholder_and_only_those or test_a_write_refuses_while_titles_are_pending"),
 M("write", "write_with_pending_titles", "    if pending:", off("    if pending:"),
   "test_a_write_refuses_while_titles_are_pending"),
 M("serialize", "indent_reintroduced",
   '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
   '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
   "test_compact_no_trailing_newline"),

 # ---- gate: critical_warnings per crop --------------------------------------------------------
 G_("gate", "wrong_type_accepted", g_["invalid"], off(g_["invalid"]), "test_a_string_is_refused"),
 G_("gate", "shell_key_accepted", g_["shell"], off1of2(g_["shell"]),
    "test_the_key_on_an_uncertified_shell_is_refused_even_null"),
 G_("gate", "presence_floor_exempts_certified", g_["presence"], off1of2(g_["presence"]),
    "test_presence_requires_the_key_on_a_certified_crop"),
 G_("gate", "entry_key_set_not_checked", g_["entry_keys"], off(g_["entry_keys"]),
    "test_an_extra_key_is_refused"),
 G_("gate", "id_format_not_checked", g_["id"], off(g_["id"]), "test_a_snake_case_id_is_refused_on_a_crop"),
 G_("gate", "class_not_closed", g_["class"], off(g_["class"]), "test_an_unknown_class_is_refused"),
 G_("gate", "severity_not_closed", g_["severity"], off(g_["severity"]), "test_an_unknown_severity_is_refused"),
 G_("gate", "stage_not_on_the_ladder", g_["stage"], off(g_["stage"]),
    "test_control_1_a_stage_off_the_crops_own_ladder_is_refused"),
 G_("gate", "empty_prose_accepted", g_["prose_empty"], off(g_["prose_empty"]),
    "test_an_empty_title_is_refused"),
 G_("gate", "em_dash_accepted", g_["prose_dash"], off(g_["prose_dash"]), "test_an_em_dash_is_refused"),
 G_("gate", "double_hyphen_accepted", g_["prose_hyphens"], off(g_["prose_hyphens"]),
    "test_a_double_hyphen_is_refused"),
 G_("gate", "empty_sources_accepted", g_["sources"], off(g_["sources"]),
    "test_a_sourceless_SAFETY_entry_is_refused_by_the_sources_rule"),
 G_("gate", "uncatalogued_source_accepted", g_["catalog"], off(g_["catalog"]),
    "test_a_source_not_in_the_catalog_is_refused"),
 G_("gate", "non_t1_source_accepted", g_["t1"], off(g_["t1"]), "test_a_non_T1_source_is_refused"),
 G_("gate", "unanchored_source_accepted", g_["anchor_missing"], off(g_["anchor_missing"]),
    "test_a_source_without_an_anchor_is_refused"),
 G_("gate", "anchor_keys_not_checked", g_["anchor_keys"], off(g_["anchor_keys"]),
    "test_an_anchor_with_extra_keys_is_refused"),
 G_("gate", "non_url_accepted", g_["anchor_url"], off(g_["anchor_url"]), "test_a_non_url_is_refused"),
 G_("gate", "verified_date_matched_by_prefix", DATE_OLD,
    '        if not (isinstance(a["verified"], str) and _DATE.search(a["verified"])):  ' + MARKER,
    "test_a_year_prefix_does_not_satisfy_the_date"),
 G_("gate", "extra_anchor_accepted", g_["anchor_extra"], off(g_["anchor_extra"]),
    "test_an_anchor_not_in_sources_is_refused"),
 G_("gate", "duplicate_id_accepted", g_["dup"], off(g_["dup"]),
    "test_control_3_two_entries_sharing_an_id_are_refused"),

 # ---- gate: container_safety ------------------------------------------------------------------
 G_("dataset", "absence_accepted_under_presence", CS_PRESENCE_OLD,
    CS_PRESENCE_OLD.replace("if presence", "if False") + "  " + MARKER,
    "test_absent_is_refused_with_presence"),
 G_("dataset", "object_shape_not_checked", g_["cs_shape"], off(g_["cs_shape"]),
    "test_wrong_top_keys_are_refused"),
 G_("dataset", "empty_warnings_accepted", g_["cs_empty"], off(g_["cs_empty"]),
    "test_empty_warnings_are_refused"),
 G_("dataset", "harvest_class_accepted", g_["cs_class"], off(g_["cs_class"]),
    "test_a_harvest_class_is_refused_here"),
 G_("dataset", "figure_accepted", g_["cs_figure"], off(g_["cs_figure"]), "test_a_digit_is_refused"),
 G_("dataset", "one_to_ten_not_matched", SMALL_OLD, '_SMALL = "NEVERSMALL"  ' + MARKER,
    "test_a_spelled_number_is_refused"),
 G_("dataset", "eleven_to_twenty_not_matched", TEENS_OLD, '_TEENS = "NEVERTEENS"  ' + MARKER,
    "test_a_teen_or_twenty_is_refused"),
 G_("dataset", "thirty_to_ninety_not_matched", TENS_OLD, '_TENS = "NEVERTENS"  ' + MARKER,
    "test_thirty_through_ninety_are_refused"),
 G_("dataset", "half_not_matched", HALF_OLD, '_HALF = "NEVERHALF"  ' + MARKER,
    "test_half_is_refused"),
 G_("dataset", "dozen_hundred_thousand_not_matched", LARGE_OLD, '_LARGE = "NEVERLARGE"  ' + MARKER,
    "test_dozen_hundred_and_thousand_are_refused"),
 G_("dataset", "bare_unit_word_refused_again", LARGE_OLD, '_LARGE = "dozen|hundred|thousand|pounds"  ' + MARKER,
    "test_the_approved_copy_that_denies_a_figure_is_accepted"),
 G_("dataset", "word_boundary_dropped", BOUNDARY_OLD,
    BOUNDARY_OLD.replace('r"\\d|\\b("', 'r"\\d|("') + "  " + MARKER,
    "test_someone_is_not_a_number"),
 G_("dataset", "record_set_not_compared", g_["cs_records"], off(g_["cs_records"]),
    "test_a_missing_record_is_refused or test_an_extra_record_is_refused"),
 G_("dataset", "record_keys_not_checked", g_["cs_record_keys"], off(g_["cs_record_keys"]),
    "test_a_record_with_the_wrong_shape_is_refused"),
 G_("dataset", "record_date_not_checked", g_["cs_record_date"], off(g_["cs_record_date"]),
    "test_a_record_with_a_bad_date_is_refused"),
 G_("dataset", "record_credit_not_checked", g_["cs_credit"], off(g_["cs_credit"]),
    "test_a_record_crediting_another_institution_is_refused"),
 G_("dataset", "record_url_not_checked", g_["cs_url"], off(g_["cs_url"]),
    "test_a_record_that_does_not_name_the_anchor_url_is_refused"),
 G_("dataset", "record_digest_not_required", g_["cs_sha"], off(g_["cs_sha"]),
    "test_a_record_that_quotes_no_digest_is_refused"),
 G_("dataset", "record_verbatim_not_required", g_["cs_verbatim"], off(g_["cs_verbatim"]),
    "test_a_record_that_quotes_no_source_text_is_refused"),
 G_("dataset", "record_em_dash_accepted", g_["cs_dash"], off(g_["cs_dash"]),
    "test_a_record_with_an_em_dash_is_refused"),

 # ---- the register ruling, and the whole_crop_gate wiring through its real entry point ---------
 ("register", "class_ruling_dropped", REG_OLD, f"    if False: return True  {MARKER}",
  "test_an_authored_entry_raises_no_unruled_prose", "register_completeness_gate.py", GATE_SUITE),
 ("wiring", "a61_violations_not_failed", WIRE_OLD, f'for m in []:  {MARKER}\n    fail(f"critical-warnings: {{m}}")',
  None, "whole_crop_gate.py", A61_SCRIPT),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_WARNINGS = P\.EXPECTED_WARNINGS$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_WARNINGS pin to build a sentinel from")
    return ("sentinel", "warnings_pin_broken", m.group(0), "N_WARNINGS = 99999  " + MARKER,
            "test_pins_are_the_literals", SUITE, SUITE)


def preflight(tools_dir):
    cache, bad = {}, []
    for fam, name, old, _new, _sel, tgt, _suite in MUTATIONS:
        if tgt not in cache:
            cache[tgt] = open(os.path.join(tools_dir, tgt), encoding="utf-8").read()
        n = cache[tgt].count(old)
        if n != 1:
            bad.append(f"  {fam}/{name}: anchor matches {n} times in {tgt}\n      {old[:100]!r}")
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once "
          f"across {len(cache)} target files")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla581_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    # A tools/ scratch copy has no .git, and promote_fixture rebuilds the pinned pre-state FROM a
    # commit; the promote re-reads the approved spec from docs/. All three are linked in.
    for name in ("crops_data_final.json", ".git", "docs"):
        os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
    shutil.copytree(os.path.join(HERE, "staging", STAGING), os.path.join(tools, "staging", STAGING),
                    ignore=shutil.ignore_patterns("_raw"))
    return tmp, tools


def run_suite(tools_dir, selector, suite=SUITE):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if suite == A61_SCRIPT:   # script-style: run it AS A SCRIPT, never under pytest (rc 5 = nothing ran)
        r = subprocess.run([sys.executable, "-B", os.path.join(tools_dir, suite)],
                           capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
        return r.returncode, (r.stdout + r.stderr)
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, suite),
                        "-q", "-k", selector, "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
    return r.returncode, (r.stdout + r.stderr)


def apply_mutation(tools_dir, old, new, target):
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
            print(f"{f} ({len(names)})")
            for n in names:
                print(f"    {n}")
        print(f"\n{len(MUTATIONS)} mutations across {len(fams)} families")
        return 0

    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)
        # THE POSITIVE CONTROL IS EVERY SUITE, WHOLE: a driver red on the CLEAN copy would grade its
        # mutation caught for the wrong reason.
        for suite in (SUITE, GATE_SUITE, A61_SCRIPT):
            rc, out = run_suite(tools, "test_", suite)
            if rc != 0:
                print(out[-2500:])
                sys.exit(f"HARNESS DEAD: the UNMUTATED scratch copy of {suite} is already failing.")
            print(f"positive control: the WHOLE unmutated {suite} is GREEN")

        fam, name, old, new, sel, tgt, suite = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel, suite)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
        print("sentinel: reddened as required\n")

        muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
        caught, survived, broken = [], [], []
        for fam, name, old, new, sel, tgt, suite in muts:
            clean, err = apply_mutation(tools, old, new, tgt)
            if err:
                broken.append((fam, name, err)); print(f"  BROKEN   {fam}/{name}: {err}"); continue
            rc, out = run_suite(tools, sel or "test_", suite)
            open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, f"driver {sel!r} collected NO TESTS"))
                print(f"  BROKEN   {fam}/{name}: collected no tests")
            elif rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name}   (driver: {sel or suite})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        named = [n for f, n in caught if f == "null_vs_empty"]
        print(f"null -> [] class, by name: {len(named)} caught: {', '.join(named) or 'NONE'}")
        for f, n, e in broken:
            print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived:
            print(f"  SURVIVED {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
