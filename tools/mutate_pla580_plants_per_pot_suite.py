#!/usr/bin/env python3
"""mutate_pla580_plants_per_pot_suite -- mutation harness for the PLA-580 plants_per_pot promote.

BUILT TO THE PLA-215 BAR: one defect per guard family injected into a SCRATCH COPY of the source;
the suite's own driver for that guard must go RED. Liveness: anchor preflight (each anchor exactly
once in its own target file), MUTATION-APPLIED marker on disk, a sentinel that MUST redden, a
positive control that runs the WHOLE suite (both suites, since two source files are mutated),
bytecode off, pytest rc 5 graded BROKEN.

TWO TARGETS. Most mutations hit the promote. The FORMULA family hits plants_per_pot_gate, because
that is where the ruled consumer contract lives (`at_gallons[hi] / count[min]`, the count>1 switch
predicate, and ruling 2's maximum) and where PLA-539 and PLA-586 read it from. Those four mutations
are what the spec's TWO NAMED CONTROLS exist to catch:
  * `max` -> `min`                     caught by test_control_the_two_reading_conservative_maximum
  * `count[0]` -> `count[1]`           caught by test_control_the_count_min_divisor_on_a_2_6_reading
  * `at_gallons[1]` -> `at_gallons[0]` caught by test_control_at_gallons_hi_is_the_numerator
  * the switch predicate disabled      caught by test_check_post_passes_and_returns_the_effect

NOT COUNTED (removed from the promote rather than shipped unreachable):
  * the duplicate-crop guard the PLA-465 pattern carries. With the row count pinned at 7 and the
    crop SET compared to the 7 ruled crops, a duplicate necessarily shrinks the set, so the set
    comparison answers first. MEASURED: its driver reddened on the set-comparison message, not its
    own. Removed from the promote; the suite records that the defect is still caught, by the
    earlier check.
  * the closing keys / authored / nulls totals in verify_post, implied by the per-crop checks
    (every certified crop must carry the key; a value with no row refuses). `readings` is NOT in
    this list and IS pinned: a row can carry the wrong NUMBER of readings and still match its own
    spec row, so that total is load-bearing and has its own driver.

Usage: mutate_pla580_plants_per_pot_suite.py [--family X] [--list]
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla580_plants_per_pot.py"
GATE = "plants_per_pot_gate.py"
SUITE = "test_promote_pla580_plants_per_pot.py"
GATE_SUITE = "test_plants_per_pot_gate.py"
STAGING = "pla580_plants_per_pot"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


def off2(two):
    """A two-line anchor whose SECOND line is the guard (the first disambiguates a repeated `if`)."""
    a, b = two.split("\n")
    return a + "\n" + off(b)


def off1of2(two):
    """A two-line anchor whose FIRST line is the guard and the second is its raise/continue."""
    a, b = two.split("\n")
    return off(a) + "\n" + b


A = {
 # --- entry -----------------------------------------------------------------------------------
 "entry": "    if got != BASE_SHA:",
 # --- spec shape ------------------------------------------------------------------------------
 "spec_base": '    if spec.get("base_sha") != BASE_SHA:',
 "fetch_date": '    if spec.get("fetch_date") != FA_DATE:',
 "authored_count": "    if expected_crops is None or len(rows) != expected_crops:",
 "crop_set": '    if {r["crop"] for r in rows} != set(EXPECTED_READINGS):',
 "row_keys": '        if set(r) != {"crop", "readings", "field_additions"}:',
 "readings_vs_ruling": "        if got != want:",
 "records_per_reading": '        if len(r["field_additions"]) != len(r["readings"]):',
 "fa_shape": '            if set(fa) != set(FA_KEYS) or fa["field"] != FA_FIELD:',
 "fa_date": '            if fa["date"] != FA_DATE:',
 "fa_sources": '            if not fa["sources"]:',
 "fa_note_page": '            if not (fa["note"] or "").strip() or "http" not in fa["note"]:',
 "fa_note_digest": '            if "sha256" not in fa["note"]:',
 "fa_note_verbatim": '            if "verbatim:" not in fa["note"]:',
 "fa_note_dash": '            if "—" in fa["note"] or "–" in fa["note"]:',
 "credit_match": '            if sorted(rd["sources"]) != sorted(fa["sources"]):',
 "record_url": '                if rd["anchoring_urls"][s]["url"] not in fa["note"]:',
 "readings_total": "    if total != EXPECTED_READINGS_TOTAL:",
 "ledger_empty": "    if not ledger:",
 "ledger_keys": '        if set(e) != {"source_row", "outcome", "why"}:',
 "ledger_outcome": '        if not e["outcome"].startswith(LEDGER_OUTCOMES):',
 "ledger_why": '        if not (e["why"] or "").strip():',
 "ledger_authored": "    if authored_in_ledger != set(EXPECTED_READINGS):",
 "digest_quoted": "        if d not in MEASURED_DIGESTS and d != BASE_SHA:",
 "digest_source_set": '    if set(spec["sources"]) != set(EVIDENCE_HASHES):',
 "digest_per_source": '        if s["sha256"] != EVIDENCE_HASHES[key]:',
 "digest_per_record": '                if EVIDENCE_HASHES.get(src, "\\x00unmeasured") not in fa["note"]:',
 # --- pre-state -------------------------------------------------------------------------------
 "roster": '    if len(data["crops"]) != ROSTER:',
 "certified_count": "    if len(certified) != EXPECTED_KEYS:",
 "existing_key": "        if FIELD in _cn(c):",
 "fa_list": "        if _certified(c) and not isinstance(fa, list):",
 "prior_record": '        if any(isinstance(x, dict) and x.get("field") == FA_FIELD for x in (fa or [])):',
 "off_roster": "        if c is None:",
 "not_certified": '        if not _certified(c):\n            raise SystemExit(f"REFUSED: authored crop {r[\'crop\']} is not certified")',
 "not_container_ok": '        if _cn(c).get("container_ok") is not True:',
 "catalog": "                if s not in catalog:",
 "gate_on_row": "        v = PPG.shape_violations(syn)\n        if v:",
 "bounds_on_row": "        nv = numeric_sanity_violations(syn)\n        if nv:",
 # --- post ------------------------------------------------------------------------------------
 "gate_on_post": "    v = PPG.all_violations(post, presence=True)\n    if v:",
 "bounds_on_post": '        nv = numeric_sanity_violations(idx[r["crop"]])\n        if nv:',
 "display_on_post": '        dv = display_readiness_violations(idx[r["crop"]])\n        if dv:',
 "planner_set": "    if set(got) != set(PLANNER_EFFECT):",
 "planner_figure": '        if got[slug] != want["after_gallons_per_plant"]:',
 "planner_basis": '        if _cn(idx[slug]).get("min_pot_gallons") != want["before_min_pot_gallons"]:',
 # --- blast radius ----------------------------------------------------------------------------
 "top_keys": "    if set(pre) != set(post):",
 "top_change": '        if k != "crops" and _j(pre[k]) != _j(post[k]):',
 "roster_change": '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
 "shell_change": '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
 "crop_keys": "        if set(g) != set(s):",
 "outside_change": '            if _j(s[k]) != _j(g[k]):\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes")',
 "cn_keys": "        if set(gcn) != set(scn) | {FIELD}:",
 "cn_change": "            if _j(scn[k]) != _j(gcn[k]):",
 "value_vs_spec": "            if _j(gcn[FIELD]) != _j(_value(r)):",
 "value_no_row": "            if gcn[FIELD] is not None:",
 "vs_keys": "        if set(sv) != set(gv):",
 "vs_change": '            if k != "field_additions" and _j(sv[k]) != _j(gv[k]):',
 "prefix": "        if _j(b[:len(a)]) != _j(a):",
 "tail": "        if _j(b[len(a):]) != _j(want_tail):",
 "readings_written": "    if readings != EXPECTED_READINGS_TOTAL:",
}

# The expected-block comparison is a three-line `if`, so `off()` cannot dedent it; the whole block
# is replaced instead.
EXPECTED_BLOCK_OLD = (
    '    if spec["expected"] != {"keys": EXPECTED_KEYS, "authored_crops": expected_crops,\n'
    '                            "readings": EXPECTED_READINGS_TOTAL,\n'
    '                            "null": EXPECTED_KEYS - expected_crops, "shells": EXPECTED_SHELLS}:')
EXPECTED_BLOCK_NEW = f"    if False:  {MARKER}"

# THE CONSUMER CONTRACT, in plants_per_pot_gate. These are the four the named controls exist for.
F_DIVISOR_OLD = '    return reading["at_gallons"][1] / reading["count"][0]'
F_DIVISOR_NEW = f'    return reading["at_gallons"][1] / reading["count"][1]  {MARKER}'
F_NUMERATOR_NEW = f'    return reading["at_gallons"][0] / reading["count"][0]  {MARKER}'
F_MAX_OLD = "    return max(conservative_gallons_per_plant(r) for r in rs)"
F_MAX_NEW = f"    return min(conservative_gallons_per_plant(r) for r in rs)  {MARKER}"
F_SWITCH_OLD = '    return any(r.get("count") != [1, 1] for r in readings)'
F_SWITCH_NEW = f"    return True  {MARKER}"
F_READINGS_OLD = "    if not isinstance(v, dict):\n        return []"
F_READINGS_NEW = f"    if False:  {MARKER}\n        return []"

# (family, name, old, new, driver selector, target file, suite file)
MUTATIONS = [
 ("entry", "base_sha_check_removed", A["entry"], off(A["entry"]),
  "test_refuses_a_canonical_that_is_not_the_base", PROMOTE, SUITE),

 ("spec", "spec_base_not_checked", A["spec_base"], off(A["spec_base"]),
  "test_refuses_a_spec_on_another_base", PROMOTE, SUITE),
 ("spec", "fetch_date_not_pinned", A["fetch_date"], off(A["fetch_date"]),
  "test_refuses_a_fetch_date_drift", PROMOTE, SUITE),
 ("spec", "authored_count_not_pinned", A["authored_count"], off(A["authored_count"]),
  "test_refuses_an_authored_count_drift", PROMOTE, SUITE),
 ("spec", "crop_set_not_compared_to_the_ruling", A["crop_set"], off(A["crop_set"]),
  "test_refuses_a_crop_not_in_the_ruling or test_a_duplicated_crop_is_caught_by_the_set_comparison",
  PROMOTE, SUITE),
 ("spec", "row_keys_not_checked", A["row_keys"], off(A["row_keys"]),
  "test_refuses_a_row_with_the_wrong_keys", PROMOTE, SUITE),
 ("spec", "readings_not_compared_to_the_ruling", A["readings_vs_ruling"], off(A["readings_vs_ruling"]),
  "test_refuses_a_count_other_than_the_ruled_one or test_refuses_an_at_gallons_other_than_the_ruled_one "
  "or test_refuses_a_reading_order_swap_on_the_two_reading_crop", PROMOTE, SUITE),
 ("spec", "record_per_reading_not_required", A["records_per_reading"], off(A["records_per_reading"]),
  "test_refuses_a_missing_provenance_record", PROMOTE, SUITE),
 ("spec", "fa_shape_not_checked", A["fa_shape"], off(A["fa_shape"]),
  "test_refuses_a_field_addition_shape", PROMOTE, SUITE),
 ("spec", "fa_date_not_pinned", A["fa_date"], off(A["fa_date"]),
  "test_refuses_a_field_addition_date", PROMOTE, SUITE),
 ("spec", "sourceless_fa_accepted", A["fa_sources"], off(A["fa_sources"]),
  "test_refuses_a_field_addition_without_sources", PROMOTE, SUITE),
 ("spec", "pageless_note_accepted", A["fa_note_page"], off(A["fa_note_page"]),
  "test_refuses_a_note_that_names_no_page", PROMOTE, SUITE),
 ("spec", "digestless_note_accepted", A["fa_note_digest"], off(A["fa_note_digest"]),
  "test_refuses_a_note_that_quotes_no_digest", PROMOTE, SUITE),
 ("spec", "unquoted_note_accepted", A["fa_note_verbatim"], off(A["fa_note_verbatim"]),
  "test_refuses_a_note_that_quotes_no_source_text", PROMOTE, SUITE),
 ("spec", "em_dash_accepted", A["fa_note_dash"], off(A["fa_note_dash"]),
  "test_refuses_an_em_dash_in_a_record", PROMOTE, SUITE),
 ("spec", "wrong_credit_accepted", A["credit_match"], off(A["credit_match"]),
  "test_refuses_a_record_crediting_another_institution", PROMOTE, SUITE),
 ("spec", "record_url_not_checked", A["record_url"], off(A["record_url"]),
  "test_refuses_a_record_that_does_not_name_its_url", PROMOTE, SUITE),
 ("spec", "readings_total_not_pinned", A["readings_total"], off(A["readings_total"]),
  "test_refuses_a_readings_total_drift", PROMOTE, SUITE),
 ("spec", "ledger_not_required", A["ledger_empty"], off(A["ledger_empty"]),
  "test_refuses_a_spec_with_no_source_ledger", PROMOTE, SUITE),
 ("spec", "ledger_keys_not_checked", A["ledger_keys"], off(A["ledger_keys"]),
  "test_refuses_a_ledger_entry_with_wrong_keys", PROMOTE, SUITE),
 ("spec", "ledger_outcome_not_closed", A["ledger_outcome"], off(A["ledger_outcome"]),
  "test_refuses_an_unrecognised_ledger_outcome", PROMOTE, SUITE),
 ("spec", "reasonless_hold_accepted", A["ledger_why"], off(A["ledger_why"]),
  "test_refuses_a_ledger_entry_with_no_reason", PROMOTE, SUITE),
 ("spec", "ledger_authored_set_not_compared", A["ledger_authored"], off(A["ledger_authored"]),
  "test_refuses_a_ledger_that_authors_a_different_set", PROMOTE, SUITE),
 ("spec", "fabricated_digest_accepted", A["digest_quoted"], off(A["digest_quoted"]),
  "test_refuses_a_fabricated_digest", PROMOTE, SUITE),
 ("spec", "source_set_not_pinned", A["digest_source_set"], off(A["digest_source_set"]),
  "test_refuses_a_source_set_other_than_the_measured_one", PROMOTE, SUITE),
 ("spec", "digest_swap_between_sources_invisible", A["digest_per_source"], off(A["digest_per_source"]),
  "test_refuses_digests_swapped_between_the_two_sources", PROMOTE, SUITE),
 ("spec", "record_quoting_the_wrong_page_invisible", A["digest_per_record"], off(A["digest_per_record"]),
  "test_refuses_a_record_quoting_the_other_pages_digest", PROMOTE, SUITE),
 ("spec", "expected_block_not_compared", EXPECTED_BLOCK_OLD, EXPECTED_BLOCK_NEW,
  "test_refuses_an_expected_block_drift", PROMOTE, SUITE),

 ("prestate", "roster_not_pinned", A["roster"], off(A["roster"]),
  "test_refuses_a_roster_drift", PROMOTE, SUITE),
 ("prestate", "certified_count_not_pinned", A["certified_count"], off(A["certified_count"]),
  "test_refuses_a_certified_count_drift", PROMOTE, SUITE),
 ("prestate", "existing_key_accepted", A["existing_key"], off(A["existing_key"]),
  "test_refuses_a_crop_already_carrying_the_key", PROMOTE, SUITE),
 ("prestate", "fa_list_not_checked", A["fa_list"], off(A["fa_list"]),
  "test_refuses_field_additions_not_a_list", PROMOTE, SUITE),
 ("prestate", "prior_record_accepted", A["prior_record"], off(A["prior_record"]),
  "test_refuses_a_prior_plants_per_pot_record", PROMOTE, SUITE),
 ("prestate", "off_roster_accepted", A["off_roster"], off(A["off_roster"]),
  "test_refuses_an_authored_crop_off_the_roster", PROMOTE, SUITE),
 ("prestate", "shell_authoring_accepted", A["not_certified"], off1of2(A["not_certified"]),
  "test_refuses_an_authored_shell", PROMOTE, SUITE),
 ("prestate", "non_container_crop_authoring_accepted", A["not_container_ok"], off(A["not_container_ok"]),
  "test_refuses_an_authored_crop_that_cannot_go_in_a_pot", PROMOTE, SUITE),
 ("prestate", "catalog_not_checked", A["catalog"], off(A["catalog"]),
  "test_refuses_a_source_not_in_catalog", PROMOTE, SUITE),
 ("prestate", "gate_not_run_on_row", A["gate_on_row"], off2(A["gate_on_row"]),
  "test_refuses_a_row_the_gate_rejects", PROMOTE, SUITE),
 ("prestate", "bounds_not_run_on_row", A["bounds_on_row"], off2(A["bounds_on_row"]),
  "test_refuses_a_row_the_bounds_reject", PROMOTE, SUITE),

 ("post", "gate_not_run_on_post", A["gate_on_post"], off2(A["gate_on_post"]),
  "test_refuses_a_post_state_that_fails_the_gate", PROMOTE, SUITE),
 ("post", "bounds_not_run_on_post", A["bounds_on_post"], off2(A["bounds_on_post"]),
  "test_refuses_an_authored_crop_that_fails_the_bounds", PROMOTE, SUITE),
 ("post", "display_not_run_on_post", A["display_on_post"], off2(A["display_on_post"]),
  "test_refuses_an_authored_crop_that_fails_display_readiness", PROMOTE, SUITE),
 ("post", "planner_switch_set_not_pinned", A["planner_set"], off(A["planner_set"]),
  "test_refuses_a_third_crop_switching or test_refuses_a_crop_losing_the_switch", PROMOTE, SUITE),
 ("post", "planner_figure_not_pinned", A["planner_figure"], off(A["planner_figure"]),
  "test_refuses_a_planner_figure_other_than_approved", PROMOTE, SUITE),
 ("post", "planner_basis_not_pinned", A["planner_basis"], off(A["planner_basis"]),
  "test_refuses_a_moved_min_pot_gallons_basis", PROMOTE, SUITE),

 ("blast", "top_level_key_set_not_compared", A["top_keys"], off(A["top_keys"]),
  "test_refuses_a_top_level_key_addition", PROMOTE, SUITE),
 ("blast", "top_level_change_invisible", A["top_change"], off(A["top_change"]),
  "test_refuses_a_top_level_change or test_refuses_a_source_catalog_change", PROMOTE, SUITE),
 ("blast", "roster_change_invisible", A["roster_change"], off(A["roster_change"]),
  "test_refuses_a_roster_change or test_refuses_an_appended_crop", PROMOTE, SUITE),
 ("blast", "shell_change_invisible", A["shell_change"], off1of2(A["shell_change"]),
  "test_refuses_a_shell_change", PROMOTE, SUITE),
 ("blast", "crop_key_set_not_compared", A["crop_keys"], off(A["crop_keys"]),
  "test_refuses_a_crop_level_key_set_drift", PROMOTE, SUITE),
 ("blast", "outside_change_invisible", A["outside_change"], off1of2(A["outside_change"]),
  "test_refuses_a_change_outside_container_notes", PROMOTE, SUITE),
 ("blast", "cn_key_set_not_compared", A["cn_keys"], off(A["cn_keys"]),
  "test_refuses_a_container_notes_key_set_drift or test_refuses_a_container_notes_key_addition",
  PROMOTE, SUITE),
 ("blast", "cn_sibling_change_invisible", A["cn_change"], off(A["cn_change"]),
  "test_refuses_a_change_to_another_container_notes_field or test_refuses_a_prose_change_in_container_notes",
  PROMOTE, SUITE),
 ("blast", "value_not_compared_to_spec", A["value_vs_spec"], off(A["value_vs_spec"]),
  "test_refuses_a_written_value_other_than_the_spec_row or test_refuses_an_extra_reading_on_an_authored_crop",
  PROMOTE, SUITE),
 ("blast", "rowless_value_accepted", A["value_no_row"], off(A["value_no_row"]),
  "test_refuses_a_value_on_a_crop_with_no_row or test_refuses_an_empty_readings_list_on_a_null_crop",
  PROMOTE, SUITE),
 ("blast", "vs_key_set_not_compared", A["vs_keys"], off(A["vs_keys"]),
  "test_refuses_a_verification_status_key_addition", PROMOTE, SUITE),
 ("blast", "vs_change_invisible", A["vs_change"], off(A["vs_change"]),
  "test_refuses_a_verification_status_value_change or test_refuses_a_status_flip", PROMOTE, SUITE),
 ("blast", "prefix_not_compared", A["prefix"], off(A["prefix"]),
  "test_refuses_a_rewritten_field_additions_prefix", PROMOTE, SUITE),
 ("blast", "tail_not_compared", A["tail"], off(A["tail"]),
  "test_refuses_a_record_other_than_the_spec or test_refuses_an_extra_appended_record", PROMOTE, SUITE),
 ("blast", "written_readings_total_not_pinned", A["readings_written"], off(A["readings_written"]),
  "test_refuses_a_readings_count_drift_in_the_written_state", PROMOTE, SUITE),

 # ---- THE CONSUMER CONTRACT. The spec's two named controls are the drivers here. --------------
 ("formula", "count_max_used_as_the_divisor", F_DIVISOR_OLD, F_DIVISOR_NEW,
  "test_control_the_count_min_divisor_on_a_2_6_reading", GATE, SUITE),
 ("formula", "at_gallons_lo_used_as_the_numerator", F_DIVISOR_OLD, F_NUMERATOR_NEW,
  "test_control_at_gallons_hi_is_the_numerator", GATE, SUITE),
 ("formula", "conservative_pick_takes_the_minimum", F_MAX_OLD, F_MAX_NEW,
  "test_control_the_two_reading_conservative_maximum", GATE, SUITE),
 ("formula", "switch_predicate_always_true", F_SWITCH_OLD, F_SWITCH_NEW,
  "test_check_post_passes_and_returns_the_effect", GATE, SUITE),
 ("formula", "readings_of_accepts_a_non_object", F_READINGS_OLD, F_READINGS_NEW,
  "test_readings_of_treats_absent_null_and_empty_alike", GATE, GATE_SUITE),

 # ---- gate shape, driven through the gate's own suite ----------------------------------------
 ("gate", "empty_readings_list_accepted",
  "    if not isinstance(readings, list) or not readings:",
  "    if not isinstance(readings, list):  " + MARKER,
  "test_empty_readings_list_is_refused", GATE, GATE_SUITE),
 ("gate", "scalar_at_gallons_accepted",
  '        if not (isinstance(g, list) and len(g) == 2 and all(_num(x) for x in g)):',
  '        if False:  ' + MARKER,
  "test_refuses_a_scalar_at_gallons", GATE, GATE_SUITE),
 ("gate", "bool_count_accepted",
  "def _int(v):\n    # bool is an int in Python; a count of `true` must not pass as 1.\n    return isinstance(v, int) and not isinstance(v, bool)",
  "def _int(v):\n    # bool is an int in Python; a count of `true` must not pass as 1.\n    return isinstance(v, int)  " + MARKER,
  "test_refuses_a_bool_count", GATE, GATE_SUITE),
 ("gate", "shared_source_across_readings_accepted",
  "            if s in first_seen:",
  "            if False:  " + MARKER,
  "test_refuses_two_readings_sharing_a_source", GATE, GATE_SUITE),
 ("gate", "container_ok_coupling_dropped",
  '    if cn.get("container_ok") is not True:',
  "    if False:  " + MARKER,
  "test_refuses_a_reading_on_a_crop_that_cannot_go_in_a_pot", GATE, GATE_SUITE),
 ("gate", "provenance_not_required",
  "    if not _has_provenance(crop):",
  "    if False:  " + MARKER,
  "test_refuses_an_authored_value_with_no_provenance_record", GATE, GATE_SUITE),
 ("gate", "shell_key_accepted",
  "    if not _certified(crop):\n        V.append(f\"{slug}: {FIELD} present on an uncertified crop; the shells carry no key \"",
  "    if False:  " + MARKER + "\n        V.append(f\"{slug}: {FIELD} present on an uncertified crop; the shells carry no key \"",
  "test_refuses_the_key_on_an_uncertified_shell", GATE, GATE_SUITE),
 ("gate", "verified_date_matched_by_prefix",
  '                if not (isinstance(a["verified"], str) and _DATE.fullmatch(a["verified"])):',
  '                if not (isinstance(a["verified"], str) and _DATE.search(a["verified"])):  ' + MARKER,
  "test_a_year_prefix_does_not_satisfy_the_date", GATE, GATE_SUITE),
 ("gate", "presence_floor_exempts_certified",
  "    if FIELD not in _cn(crop):",
  "    if False:  " + MARKER,
  "test_presence_requires_the_key_on_a_certified_crop", GATE, GATE_SUITE),

 # ---- numeric_sanity's own bounds, and the retype it deliberately carries --------------------
 ("bounds", "count_ceiling_removed",
  '        check(_r.get("count"), f"container_notes.plants_per_pot[{_i}].count", 1, 30)',
  '        pass  ' + MARKER,
  "test_the_bounds_actually_fire", "numeric_sanity_gate.py", GATE_SUITE),
 ("bounds", "at_gallons_floor_raised_to_one",
  '        check(_r.get("at_gallons"), f"container_notes.plants_per_pot[{_i}].at_gallons", 0.5, 100)',
  '        check(_r.get("at_gallons"), f"container_notes.plants_per_pot[{_i}].at_gallons", 1, 100)  ' + MARKER,
  "test_the_half_gallon_floor_is_accepted", "numeric_sanity_gate.py", GATE_SUITE),
 ("bounds", "readers_drift_apart",
  '    v = cn.get("plants_per_pot")\n    if not isinstance(v, dict):\n        return []',
  '    v = cn.get("plants_per_pot")\n    if not isinstance(v, (dict, list)):  ' + MARKER + '\n        return []',
  "test_the_two_readers_agree_on_every_shape", "numeric_sanity_gate.py", GATE_SUITE),

 ("serialize", "indent_reintroduced",
  '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
  '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
  "test_compact_no_trailing_newline", PROMOTE, SUITE),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_READINGS = P\.EXPECTED_READINGS_TOTAL$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_READINGS pin to build a sentinel from")
    return ("sentinel", "readings_pin_broken", m.group(0),
            "N_READINGS = 99999  " + MARKER, "test_pins_are_the_literals", SUITE, SUITE)


def preflight(tools_dir):
    cache = {}
    bad = []
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
    tmp = tempfile.mkdtemp(prefix="mut_pla580_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    # A tools/ scratch copy has no .git, and promote_fixture rebuilds the pinned pre-state FROM a
    # commit, so both the canonical and the repo must be linked in or every fixture load dies.
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING), os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector, suite=SUITE):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
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
        # THE POSITIVE CONTROL IS THE WHOLE SUITE, not the selected driver: a driver that is red on
        # the CLEAN copy would otherwise grade its mutation "caught" for the wrong reason. Both
        # suites run, because this harness mutates three source files between them.
        for suite in (SUITE, GATE_SUITE):
            rc, out = run_suite(tools, "test_", suite)
            if rc != 0:
                print(out[-2500:])
                sys.exit(f"HARNESS DEAD: the UNMUTATED scratch copy of {suite} is already failing; "
                         f"a red driver would grade its mutation caught for the wrong reason.")
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
            rc, out = run_suite(tools, sel, suite)
            open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, f"driver {sel!r} collected NO TESTS"))
                print(f"  BROKEN   {fam}/{name}: collected no tests")
            elif rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        for f, n, e in broken:
            print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived:
            print(f"  SURVIVED {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
