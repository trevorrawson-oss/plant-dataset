#!/usr/bin/env python3
"""mutate_rootstock_prose_gate -- mutation harness for PLA-608 Part 2 (tools/rootstock_prose_gate.py, A64, gate_all).

BUILT TO THE PLA-215 BAR (docs/promote_suite_mutation_convention.md): one defect per guard family injected into a
SCRATCH COPY of tools/; the suite's own driver for that guard must go RED (tools/test_rootstock_prose_gate.py).
Liveness: anchor preflight (each anchor exactly once in its file), a MUTATION-APPLIED marker verified on disk, a
SENTINEL that must redden (the suite's live population blanked), a positive control that runs the WHOLE unmutated suite
first, bytecode off, and pytest rc 5 graded BROKEN (nothing collected is not a catch). Any failure of the liveness
defence exits HARNESS DEAD.

Usage: mutate_rootstock_prose_gate.py [--list]
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
MARKER = "# MUTATION-APPLIED"
M = "  " + MARKER
NOTHING_COLLECTED = 5
SUITE = "test_rootstock_prose_gate.py"
GATE = "rootstock_prose_gate.py"
SENTINEL = (r"^LIVE = G\.roster\(DATA\)$", 'LIVE = G.roster({"crops": []})' + M,
            "test_inspected_fields_and_names_are_the_measurement")

# (family, name, file, anchor, replacement, driver selector)
MUTATIONS = [
    # --- the table ----------------------------------------------------------------------------------------------
    ("table", "synonym_dropped", GATE,
     '    "alemow": [r"alem[eo]?ow", r"(?:Citrus|C\\.)\\s*macrophylla", r"macrophylla"],',
     '    "alemow": [r"alem[eo]?ow"],' + M, "test_synonyms_name_the_same_stock"),
    ("table", "family_never_resolves_through_a_member", GATE,
     "        return nid in fams or bool(FAMILIES[nid][1] & stocks)",
     "        return nid in fams" + M, "test_a_family_term_resolves_through_any_member_row"),
    ("table", "member_resolves_through_its_family", GATE,
     "        return nid in stocks or any(SELECTION_OF.get(s) == nid for s in stocks)",
     "        return nid in stocks or any(nid in m and (m & stocks) for _t, m in FAMILIES.values())" + M,
     "test_a_member_named_resolves_only_to_itself"),
    ("table", "selection_of_two_way", GATE,
     "        return nid in stocks or any(SELECTION_OF.get(s) == nid for s in stocks)",
     "        return nid in stocks or any(SELECTION_OF.get(s) == nid for s in stocks) or SELECTION_OF.get(nid) in stocks" + M,
     "test_selection_of_is_one_way"),
    ("table", "shortest_match_wins", GATE,
     "    cands.sort(key=lambda c: (-(c[1] - c[0]), c[0]))",
     "    cands.sort(key=lambda c: (c[1] - c[0], c[0]))" + M, "test_longest_match_wins"),
    ("table", "cultivar_deny_list_emptied", GATE,
     'NOT_ROOTSTOCKS = [r"(?-i:North\\s+Star)", r"(?-i:Meteor)"]',
     "NOT_ROOTSTOCKS = []" + M, "test_cultivars_are_never_read_as_rootstocks"),
    ("table", "own_root_on_empty_dropped", GATE,
     "    if rows == []:\n        stocks.add(OWN_ROOT)\n",
     "    pass" + M + "\n", "test_own_root_resolves_on_an_authored_empty_list_only"),
    ("table", "own_root_on_every_crop", GATE,
     "    if rows == []:\n        stocks.add(OWN_ROOT)\n",
     "    stocks.add(OWN_ROOT)" + M + "\n", "test_own_root_resolves_on_an_authored_empty_list_only"),
    ("table", "row_name_alias_ignored", GATE,
     "            stocks.add(ROW_NAME_ALIASES[n.strip().lower()])",
     "            pass" + M, "test_a_row_named_only_seedling_holds_apple_seedling"),
    # --- reach: the fields the rule reads ------------------------------------------------------------------------
    ("reach", "note_not_read", GATE,
     "    if isinstance(crop.get(NOTE_FIELD), str):",
     "    if False:" + M, "test_every_named_field_is_read"),
    ("reach", "row_fields_not_read", GATE,
     "        for f in ROW_FIELDS:", "        for f in ():" + M, "test_every_named_field_is_read"),
    ("reach", "container_notes_not_read", GATE,
     '    out += list(_leaves(crop.get("container_notes"), "container_notes"))',
     "    pass" + M, "test_every_named_field_is_read"),
    ("reach", "nested_container_leaves_not_read", GATE,
     '            yield from _leaves(v, f"{path}.{k}")',
     "            pass" + M, "test_every_named_field_is_read"),
    ("reach", "citation_keys_read", GATE,
     "            if CITE.search(k):\n                continue\n",
     "            pass" + M + "\n", "test_citation_keys_and_varieties_are_not_read"),
    ("reach", "recommended_rootstock_read", GATE,
     '    out += list(_leaves(crop.get("container_notes"), "container_notes"))',
     '    out += list(_leaves(crop.get("container_notes"), "container_notes")) + '
     '[("recommended_rootstock", crop.get("recommended_rootstock") or "")]' + M,
     "test_recommended_rootstock_itself_is_not_read"),
    # --- waivers: identity AND character ---------------------------------------------------------------------------
    ("waiver", "character_dropped", GATE,
     '            for m in ms if not m["resolved"] and waiver_key(m) not in known]',
     '            for m in ms if not m["resolved"] and waiver_key(m)[:3] not in {k[:3] for k in known}]' + M,
     "test_a_waived_name_in_a_reworded_sentence_FAILS"),
    ("waiver", "waiver_not_crop_scoped", GATE,
     '            for m in ms if not m["resolved"] and waiver_key(m) not in known]',
     '            for m in ms if not m["resolved"] and m["sentence"] not in {k[3] for k in known}]' + M,
     "test_a_waiver_does_not_cover_the_same_name_on_another_crop"),
    ("waiver", "stale_never_reported", GATE,
     "    stale = sorted(k for k in known if k not in fired)",
     "    stale = []" + M, "test_a_waiver_whose_name_now_resolves_is_STALE"),
    ("waiver", "stale_exits_zero", GATE,
     '    return 1 if (r["violations"] or r["stale"]) else 0',
     '    return 1 if r["violations"] else 0' + M, "test_cli_exit_codes"),
    ("waiver", "sentence_is_the_whole_field", GATE,
     "            return text[start:m.start()].strip()",
     "            return text.strip()" + M, "test_live_unresolved_equals_the_waiver_ledger_exactly"),
    # --- population ------------------------------------------------------------------------------------------------
    ("population", "lost_crop_not_refused", GATE,
     '    if r["lost_crops"]:', "    if False:" + M, "test_injection_5_strip_one_add_one_REFUSES"),
    ("population", "zero_not_refused", GATE,
     '    if r["carrying"] == 0 or r["inspected"] == 0:', "    if False:" + M, "test_zero_population_REFUSES"),
    ("population", "a_crop_skipped", GATE,
     "    for c in carrying:\n        ms, n = scan_crop(c)",
     "    for c in carrying[1:]:" + M + "\n        ms, n = scan_crop(c)",
     "test_population_is_the_21_crops_carrying_the_field_by_identity"),
    ("population", "new_crop_not_inspected", GATE,
     "    carrying = [c for c in crops if has_field(c)]",
     '    carrying = [c for c in crops if has_field(c) and c.get("slug") in KNOWN_POPULATION]' + M,
     "test_injection_4_a_crop_gaining_the_field_moves_the_population"),
    ("population", "limit_line_not_printed", GATE,
     '    print(f"  {LIMIT_LINE}")', "    pass" + M, "test_cli_live_passes_and_prints_its_population_and_limit"),
    # --- wiring: the entry points ----------------------------------------------------------------------------------
    ("wiring", "a64_violations_dropped", "whole_crop_gate.py",
     '    for m in _rpv:\n        fail(f"rootstock-prose: {m}")',
     "    for m in []:" + M + '\n        fail(f"rootstock-prose: {m}")', "test_whole_crop_gate_A64_fails_by_name"),
    ("wiring", "gate_all_roster_half_dropped", "gate_all.py",
     '                            ("rootstock_prose_gate", _rpr["violations"], _rp.refusal(_rpr))):',
     '                            ("rootstock_prose_gate", [], None)):' + M,
     "test_gate_all_runs_the_roster_half_on_a_SHELL"),
]


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_rpg_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    os.symlink(os.path.join(REPO, "CLAUDE.md"), os.path.join(tmp, "CLAUDE.md"))   # gate_all's certified floor
    return tmp, tools


def run_suite(tools, selector):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools, SUITE), "-q", "-x", "-k", selector,
                        "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new, regex=False):
    path = os.path.join(tools, target)
    clean = open(path, encoding="utf-8").read()
    if regex:
        hits = len(re.findall(old, clean, re.M))
        if hits != 1:
            return None, f"sentinel regex matches {hits} times"
        mutated = re.sub(old, new, clean, count=1, flags=re.M)
    else:
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for fam, n, *_ in MUTATIONS:
            print(f"{fam}/{n}")
        return 0
    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        bad = []
        for fam, n, target, old, _new, _sel in MUTATIONS:
            c = open(os.path.join(tools, target), encoding="utf-8").read().count(old)
            if c != 1:
                bad.append(f"  {fam}/{n}: anchor matches {c} times in {target}")
        if bad:
            sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
        print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")
        rc, out = run_suite(tools, "test_")
        if rc != 0:
            print(out[-3000:])
            sys.exit(f"HARNESS DEAD: the UNMUTATED {SUITE} is already failing (rc {rc}).")
        print("positive control: the WHOLE unmutated suite is GREEN")
        old, new, sel = SENTINEL
        clean, err = apply(tools, SUITE, old, new, regex=True)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, SUITE), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
        print("sentinel: reddened as required")
        caught, survived, broken = [], [], []
        for fam, n, target, old, new, sel in MUTATIONS:
            clean, err = apply(tools, target, old, new)
            if err:
                broken.append((fam, n, err))
                print(f"  BROKEN   {fam}/{n}: {err}")
                continue
            rc, _ = run_suite(tools, sel)
            open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, n, f"driver {sel!r} collected NO TESTS"))
                print(f"  BROKEN   {fam}/{n}: collected no tests")
            elif rc == 0:
                survived.append((fam, n, sel))
                print(f"  SURVIVED {fam}/{n}  (driver: {sel})")
            else:
                caught.append((fam, n))
                print(f"  caught   {fam}/{n}")
        print(f"\nTOTAL: {len(MUTATIONS)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
