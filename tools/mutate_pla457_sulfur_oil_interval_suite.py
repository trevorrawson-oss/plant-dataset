#!/usr/bin/env python3
"""mutate_pla457_sulfur_oil_interval_suite -- mutation harness for the PLA-457 sulfur/oil interval promote suite.

BUILT TO THE PLA-215 BAR. It injects one defect per guard family into a SCRATCH COPY of the promote
source, runs the suite's own drivers against the mutated copy, and requires each to go RED. A
mutation that survives is a guard the suite does not actually test.

THE LIVENESS DEFENSE: anchor preflight (every anchor matches EXACTLY ONCE), a MUTATION-APPLIED
marker asserted on disk, a sentinel that MUST redden, a positive control that must be GREEN, and
bytecode disabled with __pycache__ cleared before every run. Any of those failing exits HARNESS
DEAD, which is the behaviour to expect from a working harness on a bad day.

WHY PER-MUTATION TEST SELECTION. Each mutation names the driver that SHOULD catch it, and only that
driver runs. The selection IS the assertion: a mutation counts as caught only if ITS OWN driver
reddens, not if some other test happens to fall over.

NOT COUNTED AS COVERAGE (forward assertions that cannot fire in isolation on this spec): the
kind/field/kebab shape checks in check_spec_shape, and apply_to's own match-count refusal, which
check_pre_state reaches first.

Usage:
    mutate_pla457_sulfur_oil_interval_suite.py             # all families
    mutate_pla457_sulfur_oil_interval_suite.py --family X  # one family
    mutate_pla457_sulfur_oil_interval_suite.py --list
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla457_sulfur_oil_interval.py"
SUITE = "test_promote_pla457_sulfur_oil_interval.py"
STAGING = "pla457_sulfur_oil_interval"
MARKER = "# MUTATION-APPLIED"

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    ("entry", "base_sha_check_removed", "    if got != BASE_SHA:", "    if False:  " + MARKER,
     "test_main_refuses_a_moved_base"),

    # ---- the widened net (guard 1), the instrument itself
    ("net", "pronoun_arm_on_sulfur_rungs_removed",
     '(m == "sulfur" and has_o) or', '(False) or  ' + MARKER + '\n                                          ',
     "test_the_net_finds_the_five_pronoun_statements"),
    ("net", "pre_count_not_pinned", "    if len(found) != EXPECTED_PRE_STATEMENTS:", "    if False:  " + MARKER,
     "test_refuses_a_pre_count_drift"),
    ("net", "stray_statement_accepted", "    if stray:", "    if False:  " + MARKER,
     "test_refuses_a_statement_the_spec_does_not_rewrite"),
    ("net", "post_count_not_pinned", "    if len(found) != EXPECTED_POST_STATEMENTS:", "    if False:  " + MARKER,
     "test_refuses_a_post_count_change"),
    ("net", "surviving_sub_thirty_accepted",
     '    if bad:\n        raise SystemExit(f"REFUSED: {len(bad)} interval statement(s) survive',
     '    if False:  ' + MARKER + '\n        raise SystemExit(f"REFUSED: {len(bad)} interval statement(s) survive',
     "test_refuses_a_surviving_sub_thirty_statement"),
    ("net", "phi_exclusion_removed",
     "                            if HARVEST_PHI.search(s) and not (SULFUR.search(s) and OIL.search(s) and \"oil spray\" in s):\n                                continue",
     "                            if False:  " + MARKER + "\n                                continue",
     "test_the_net_excludes_mints_harvest_phi"),

    # ---- the scoped claim (guard 3), one regex at a time
    ("scope", "thirty_matches_anything", 'THIRTY = re.compile(r"\\b30 days\\b")', 'THIRTY = re.compile(r"")  ' + MARKER,
     "test_refuses_a_claim_without_the_figure"),
    ("scope", "label_matches_anything", 'LABEL = re.compile(r"\\blabel\\b", re.I)', 'LABEL = re.compile(r"")  ' + MARKER,
     "test_refuses_a_bare_interval"),
    ("scope", "scope_matches_anything", 'SCOPE = re.compile(r"in leaf|has leaves|growing season", re.I)', 'SCOPE = re.compile(r"")  ' + MARKER,
     "test_refuses_a_missing_scope"),
    ("scope", "sub_thirty_never_matches",
     'SUB_30 = re.compile(r"\\b(2|two|three|3|10|14|21)\\s*(weeks?|days?)\\b", re.I)',
     'SUB_30 = re.compile(r"(?!x)x")  ' + MARKER,
     "test_refuses_a_sub_thirty_interval"),
    ("scope", "spec_rows_not_checked_for_scope", '        if not scoped_thirty_with_label(r["new"]):', "        if False:  " + MARKER,
     "test_refuses_a_bare_interval"),

    # ---- hygiene and lifts (guard 4)
    ("hygiene", "em_dash_accepted", "    if DASHES.search(text):", "    if False:  " + MARKER,
     "test_refuses_an_em_dash"),
    ("lift", "lift_check_disabled", "        if shared:\n            return sorted(shared)[0]", "        if False:  " + MARKER + "\n            return sorted(shared)[0]",
     "test_refuses_a_verbatim_lift_from_an_anchor"),
    ("lift", "figure_exemption_swallows_everything", "    return any(ch.isdigit() for ch in gram)", "    return True  " + MARKER,
     "test_figure_runs_are_exempt_but_prose_runs_are_not"),

    # ---- spec shape
    ("spec", "row_count_not_pinned", "    if len(rows) != EXPECTED_NOTES:", "    if False:  " + MARKER,
     "test_refuses_a_row_count_other_than_twenty"),
    ("spec", "duplicate_row_accepted", "        if key in seen:", "        if False:  " + MARKER,
     "test_refuses_a_duplicated_row"),
    ("spec", "self_rewrite_accepted", '        if r["old"] == r["new"]:', "        if False:  " + MARKER,
     "test_refuses_a_self_rewrite"),
    ("spec", "catalog_count_not_pinned", "    if len(new) != EXPECTED_NEW_SOURCES:", "    if False:  " + MARKER,
     "test_refuses_a_second_catalog_id"),
    ("spec", "anchor_source_mismatch_accepted", '        if set(m["add_anchors"]) != set(m["add_sources"]):', "        if False:  " + MARKER,
     "test_refuses_anchors_that_do_not_match_sources"),

    # ---- pre-state
    ("prestate", "drifted_sentence_accepted", '        if text.count(r["old"]) != 1:', "        if False:  " + MARKER,
     "test_refuses_a_drifted_old_sentence"),
    ("prestate", "missing_caution_accepted", '        if cautions.count(m["caution_old"]) != 1:', "        if False:  " + MARKER,
     "test_refuses_a_missing_caution"),
    ("prestate", "existing_catalog_id_overwritten",
     '        if sid in sc:\n            raise SystemExit(f"REFUSED: catalog id {sid!r} already exists',
     '        if False:  ' + MARKER + '\n            raise SystemExit(f"REFUSED: catalog id {sid!r} already exists',
     "test_refuses_a_catalog_id_that_already_exists"),
    ("prestate", "non_t1_source_accepted",
     '            if (entry.get("tier") or "").upper() != "T1":\n                raise SystemExit(f"REFUSED: {k} cites {s!r}, which is not T1")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {k} cites {s!r}, which is not T1")',
     "test_refuses_a_non_t1_source_on_a_caution"),
    ("prestate", "anchor_url_mismatch_accepted", '            if m["add_anchors"][s]["url"] != entry["url"]:', "            if False:  " + MARKER,
     "test_refuses_an_anchor_url_that_differs_from_the_catalog"),
    ("prestate", "bare_host_accepted",
     '        if not u.startswith("https://") or len(u.split("://", 1)[1].strip("/").split("/")) < 2:',
     "        if False:  " + MARKER,
     "test_refuses_a_bare_host_url"),
    ("prestate", "a54_not_run_on_the_admitted_source",
     '    if tv:\n        raise SystemExit(f"REFUSED: the admitted source would fail A54',
     '    if False:  ' + MARKER + '\n        raise SystemExit(f"REFUSED: the admitted source would fail A54',
     "test_refuses_a_document_id_without_a_title_A54"),

    # ---- oregano, registers, catalog gates
    ("oregano", "disagreement_accepted", "    if not all(THIRTY.search(s) for s in stmts):", "    if False:  " + MARKER,
     "test_refuses_oregano_with_one_rung_reverted"),
    ("registers", "identical_registers_accepted", "        if b.strip() == s.strip():", "        if False:  " + MARKER,
     "test_refuses_identical_registers"),
    ("registers", "reword_accepted", "        if _sym(b, s) >= 0.90:", "        if False:  " + MARKER,
     "test_refuses_a_reworded_register"),
    ("gates", "a54_not_run_on_post",
     '    tv = title_violations(post["source_catalog"])\n    if tv:', '    tv = title_violations(post["source_catalog"])\n    if False:  ' + MARKER,
     "test_refuses_a54_on_the_post_state"),
    ("gates", "control_ladder_gate_not_run_on_post", "    v = CLG.all_violations(post)\n    if v:", "    v = CLG.all_violations(post)\n    if False:  " + MARKER,
     "test_refuses_control_ladder_gate_on_the_post_state"),

    # ---- blast radius
    ("blast", "roster_change_invisible",
     '    if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:', "    if False:  " + MARKER,
     "test_refuses_a_roster_change"),
    ("blast", "top_level_change_invisible", '            raise SystemExit(f"REFUSED: top-level key {k!r} changed")', "            pass  " + MARKER,
     "test_refuses_a_touched_top_level_key"),
    ("blast", "untouched_crop_change_invisible", '            raise SystemExit(f"REFUSED: untouched crop {slug} changed")', "            pass  " + MARKER,
     "test_refuses_an_untouched_crop_change"),
    ("blast", "crop_level_key_set_not_compared", "        if set(s_crop) != set(g_crop):", "        if False:  " + MARKER,
     "test_refuses_a_crop_level_addition"),
    ("blast", "entry_key_set_not_compared", "                if set(s) != set(g):", "                if False:  " + MARKER,
     "test_set_comparison_runs_before_value_comparison"),
    ("blast", "entry_field_change_invisible",
     '                        raise SystemExit(f"REFUSED: {slug}/{s.get(\'id\')!r} field {k!r} changed; this promote "',
     '                        pass  ' + MARKER + '  # (f"REFUSED: {slug}/{s.get(\'id\')!r} field {k!r} changed; this promote "',
     "test_refuses_a_prose_field_change_on_a_touched_crop"),
    ("blast", "rung_key_set_not_compared", "                    if set(sr) != set(gr):", "                    if False:  " + MARKER,
     "test_refuses_a_rung_key_set_change"),
    ("blast", "ladder_length_not_compared", "                if len(sl) != len(gl):", "                if False:  " + MARKER,
     "test_refuses_a_ladder_length_change"),
    ("blast", "unrowed_note_change_invisible",
     '                        if row is None:\n                            raise SystemExit(f"REFUSED: {slug}/{s.get(\'id\')!r}/{sr.get(\'method\')}/{k} changed "',
     '                        if False:  ' + MARKER + '\n                            raise SystemExit(f"REFUSED: {slug}/{s.get(\'id\')!r}/{sr.get(\'method\')}/{k} changed "',
     "test_refuses_a_note_change_on_an_unnamed_rung"),
    ("blast", "inexact_replacement_accepted", '                        if gr[k] != sr[k].replace(row["old"], row["new"], 1):', "                        if False:  " + MARKER,
     "test_refuses_a_note_change_without_a_row"),
    ("blast", "leaf_count_not_compared", "    if changed != len(note_rows(spec)):", "    if False:  " + MARKER,
     "test_refuses_fewer_leaves_than_rows"),
    ("blast", "other_method_change_invisible",
     '            raise SystemExit(f"REFUSED: control_methods.{k} changed; only {METHODS} may change")', "            pass  " + MARKER,
     "test_refuses_another_method_changing"),
    ("blast", "method_other_field_change_invisible",
     '                raise SystemExit(f"REFUSED: control_methods.{k}.{key} changed; only cautions, sources and "',
     '                pass  ' + MARKER + '  # (f"REFUSED: control_methods.{k}.{key} changed; only cautions, sources and "',
     "test_refuses_a_non_caution_field_on_a_declared_method"),
    ("blast", "cautions_count_not_compared", '        if len(s["cautions"]) != len(g["cautions"]):', "        if False:  " + MARKER,
     "test_refuses_a_cautions_count_change"),
    ("blast", "second_caution_change_invisible", '        if diff != [(m["caution_old"], m["caution_new"])]:', "        if False:  " + MARKER,
     "test_refuses_a_second_caution_changing"),
    ("blast", "undeclared_source_accepted",
     '        if g["sources"] != s["sources"] + [x for x in m["add_sources"] if x not in s["sources"]]:', "        if False:  " + MARKER,
     "test_refuses_an_undeclared_source_addition"),
    ("blast", "modified_anchor_invisible", '            if s["anchoring_urls"][key] != g["anchoring_urls"][key]:', "            if False:  " + MARKER,
     "test_refuses_a_modified_existing_anchor"),
    ("blast", "dropped_catalog_entry_invisible", "    if dropped:", "    if False:  " + MARKER,
     "test_refuses_a_dropped_catalog_entry"),
    ("blast", "extra_catalog_entry_accepted", '    if added != sorted(spec.get("catalog_new") or {}):', "    if False:  " + MARKER,
     "test_refuses_an_extra_catalog_entry"),
    ("blast", "modified_catalog_entry_invisible", "        if psc[k] != gsc[k]:", "        if False:  " + MARKER,
     "test_refuses_a_modified_existing_catalog_entry"),

    # ---- serializer
    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_one_serializer_shared_with_the_suite"),
]


def sentinel_for(tools_dir):
    """Built from the CURRENT pin value, so a legitimate pin move does not permanently break the
    sentinel and invite someone to delete it."""
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_LEAVES = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_LEAVES pin to build a sentinel from")
    return ("sentinel", "leaf_count_pin_broken",
            m.group(0), f"N_LEAVES = {int(m.group(1)) + 99999}  " + MARKER,
            "test_apply_changes_exactly_the_declared_leaves", SUITE)


def preflight(tools_dir):
    """EVERY ANCHOR MATCHES EXACTLY ONCE, checked before a single result is graded."""
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = []
    for fam, name, old, _new, _sel in MUTATIONS:
        n = src.count(old)
        if n != 1:
            bad.append(f"  {fam}/{name}: anchor matches {n} times, needs exactly 1\n"
                       f"      {old[:90]!r}")
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed. An anchor matching zero times edits "
                 "nothing and reports a FALSE SURVIVOR; one matching twice edits a site nobody "
                 "intended.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla457_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    # promote_fixture.pre_state shells out to `git show` with cwd=REPO, derived from its own path.
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING),
                    os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector):
    """STALE BYTECODE IS A DEAD HARNESS: clear __pycache__ and disable writing it."""
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "-k", selector,
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
    if MARKER not in back:
        return None, "MUTATION-APPLIED marker absent after write"
    if back == clean:
        return None, "file on disk is byte-identical to clean"
    return clean, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        fams = {}
        for fam, name, *_ in MUTATIONS:
            fams.setdefault(fam, []).append(name)
        for f, names in fams.items():
            print(f"{f} ({len(names)})")
            for n in names:
                print(f"    {n}")
        return 0

    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)

        rc, out = run_suite(tools, "test_the_spec_is_the_shape_measured")
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing. Every 'caught' "
                     "below would be meaningless because the suite fails regardless of mutation.")
        print("positive control: unmutated scratch is GREEN")

        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED. The harness is not measuring "
                     "anything and no result below can be trusted.")
        print("sentinel: reddened as required\n")

        muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in muts:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err))
                print(f"  BROKEN   {fam}/{name}: {err}")
                continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == 0:
                survived.append((fam, name, sel))
                print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name))
                print(f"  caught   {fam}/{name}")

        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, "
              f"{len(broken)} broken")
        if broken:
            print("\nBROKEN mutations are HARNESS failures, not survivors. Fix the anchors:")
            for f, n, e in broken:
                print(f"  {f}/{n}: {e}")
        if survived:
            print("\nSURVIVORS are guards the suite does not actually test:")
            for f, n, s in survived:
                print(f"  {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
