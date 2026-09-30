#!/usr/bin/env python3
"""mutate_citation_ratchet_gates -- mutation harness for the PLA-607 and PLA-544 gates.

  sourced_block_ratchet_gate.py  <- test_sourced_block_ratchet_gate.py   (PLA-607 + folded PLA-533)
  bare_host_gate.py              <- test_bare_host_gate.py               (PLA-544)

BUILT TO THE PLA-215 BAR: one defect per guard family injected into a SCRATCH COPY of the gate
source; the suite's own driver for that guard must go RED. Liveness: anchor preflight (each anchor
exactly once), MUTATION-APPLIED marker verified on disk, a sentinel per suite that MUST redden, a
positive control that runs the WHOLE unmutated suite first, bytecode off, pytest rc 5 graded
BROKEN (nothing collected is not a catch).

  whole_crop_gate A62/A63 + gate_all <- test_gate_citation_ratchets_a62_a63.py (script-style)

Usage: mutate_citation_ratchet_gates.py [--list] [--only ratchet|bare|wiring]
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
NOTHING_COLLECTED = 5
M = "  " + MARKER

RATCHET = {
    "gate": "sourced_block_ratchet_gate.py",
    "suite": "test_sourced_block_ratchet_gate.py",
    "sentinel": (r'^VICTIM = "cabbage".*$', 'VICTIM = "no-such-crop"' + M,
                 "test_a_clean_crop_passes"),
    "mutations": [
        # --- the "uncited" predicate: the three empty states ------------------------------------
        ("predicate", "empty_list_counts_as_cited",
         "    return isinstance(slot, list) and any(isinstance(s, str) and s.strip() for s in slot)",
         "    return isinstance(slot, list)" + M,
         "test_c1_storage_sources_empty_list_FAILS"),
        ("predicate", "null_counts_as_cited",
         "    return isinstance(slot, list) and any(isinstance(s, str) and s.strip() for s in slot)",
         "    return slot is None or (isinstance(slot, list) and any(isinstance(s, str) and s.strip() for s in slot))" + M,
         "test_c2_storage_sources_null_FAILS"),
        ("predicate", "missing_key_counts_as_cited",
         '            add(name, "sources", is_cited(b.get("sources")))',
         '            add(name, "sources", is_cited(b.get("sources", ["x"])))' + M,
         "test_c3_storage_sources_key_removed_FAILS"),
        ("predicate", "blank_strings_count_as_cited",
         "    return isinstance(slot, list) and any(isinstance(s, str) and s.strip() for s in slot)",
         "    return isinstance(slot, list) and any(isinstance(s, str) for s in slot)" + M,
         "test_a_list_of_blank_strings_is_not_cited"),
        # --- scope: what is a carrier -----------------------------------------------------------
        ("scope", "citation_only_block_counted",
         "        return any(has_content(v) for k, v in block.items() if k not in CITE_KEYS)",
         "        return any(has_content(v) for k, v in block.items())" + M,
         "test_a_block_holding_only_an_anchors_dict_states_nothing"),
        ("scope", "shells_counted",
         "    if not certified(crop):\n        return []\n    V = []",
         "    if False:" + M + "\n        return []\n    V = []",
         "test_an_uncertified_shell_is_exempt"),
        # --- every block kind is reached --------------------------------------------------------
        ("reach", "sibling_blocks_skipped",
         "        if any(has_content(crop.get(k)) for k in carriers):",
         "        if False:" + M,
         "test_c5_harvest_ready_sources_empty_FAILS"),
        ("reach", "tips_skipped",
         "    if isinstance(tips, dict):",
         "    if False:" + M,
         "test_new_tip_without_sources_FAILS"),
        ("reach", "item_families_skipped",
         "        if not isinstance(items, list):\n            continue\n        parent_cited",
         "        if True:" + M + "\n            continue\n        parent_cited",
         "test_new_pest_without_sources_FAILS_by_its_id"),
        ("reach", "parent_never_covers",
         '        parent_cited = parent is not None and is_cited((crop.get(parent) or {}).get("sources"))',
         "        parent_cited = False" + M,
         "test_variety_items_are_covered_by_a_cited_parent"),
        ("reach", "parent_always_covers",
         '        parent_cited = parent is not None and is_cited((crop.get(parent) or {}).get("sources"))',
         "        parent_cited = True" + M,
         "test_variety_items_become_uncited_when_the_parent_loses_its_sources"),
        # --- identity ---------------------------------------------------------------------------
        ("identity", "keyed_items_fall_back_to_index",
         "    if key and isinstance(item, dict) and isinstance(item.get(key), str) and item[key].strip():",
         "    if False:" + M,
         "test_keyed_identity_survives_a_reorder"),
        # --- THE RATCHET ------------------------------------------------------------------------
        ("ratchet", "growth_invisible",
         "        if ident not in KNOWN:",
         "        if False:" + M,
         "test_c1_storage_sources_empty_list_FAILS or test_substitution_FAILS"),
        ("ratchet", "inverted",
         "        if ident not in KNOWN:",
         "        if ident in KNOWN:" + M,
         "test_inspected_population_and_verdict"),
        # --- discovery: naming is part of adding ------------------------------------------------
        ("discovery", "unnamed_never_reported",
         "    for f in unnamed_fields(crop):",
         "    for f in []:" + M,
         "test_a_new_sourced_block_is_UNNAMED_until_named"),
        ("discovery", "excluded_subtrees_walked",
         "                if top and k in EXCLUDED:",
         "                if False:" + M,
         "test_the_excluded_subtrees_are_not_walked or test_no_unnamed_citation_keys_on_canonical"),
        ("discovery", "anchor_only_not_honoured",
         '                    elif path == "" and k in ANCHOR_ONLY:',
         "                    elif False:" + M,
         "test_an_anchor_only_field_is_recorded_not_flagged"),
        ("discovery", "crop_root_siblings_ignored",
         "                    else:\n                        found.add(",
         "                    elif False:" + M + "\n                        found.add(",
         "test_a_new_crop_root_sources_sibling_is_UNNAMED"),
        # --- the folded pot sub-rule ------------------------------------------------------------
        ("pot", "set_check_off",
         '    if pot_uncited(crop) and crop.get("slug") not in POT_KNOWN:',
         "    if False:" + M,
         "test_PROOF_a_fifth_FAILS"),
        ("pot", "ceiling_off",
         "    if len(pot_live) > POT_CEILING:",
         "    if False:" + M,
         "test_the_ceiling_fires_on_a_KNOWN_CEILING_desync"),
        ("pot", "anchors_half_ignored",
         '    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})',
         '    return not (cn.get("sources") or [])' + M,
         "test_sources_without_anchors_is_pot_uncited"),
        ("pot", "ceiling_raised",
         "POT_CEILING = 4",
         "POT_CEILING = 99" + M,
         "test_pot_sub_rule_pins_are_the_folded_four"),
        # --- inspected nothing ------------------------------------------------------------------
        ("refusal", "zero_certified_not_named",
         "    if n_cert == 0:",
         "    if False:" + M,
         "test_zero_certified_REFUSES"),
        ("refusal", "floor_off",
         "    if inspected < MIN_INSPECTED:",
         "    if False:" + M,
         "test_below_floor_REFUSES"),
        ("refusal", "floor_lowered",
         "MIN_INSPECTED = 6500",
         "MIN_INSPECTED = 0" + M,
         "test_floor_is_below_the_measured_population"),
        ("cli", "violation_exits_zero",
         "    return 1 if V else 0",
         "    return 0" + M,
         "test_injection_rc1_names_the_block"),
    ],
}

BARE = {
    "gate": "bare_host_gate.py",
    "suite": "test_bare_host_gate.py",
    "sentinel": (r'^VICTIM = "cabbage".*$', 'VICTIM = "no-such-crop"' + M,
                 "test_a_clean_crop_passes"),
    "mutations": [
        ("predicate", "root_page_not_bare",
         "    return isinstance(url, str) and bool(BARE.fullmatch(url) or ROOT_PAGE.fullmatch(url))",
         "    return isinstance(url, str) and bool(BARE.fullmatch(url))" + M,
         "test_site_root_page_spellings_are_bare"),
        ("predicate", "query_page_called_bare",
         'ROOT_PAGE = re.compile(r"https?://[^/?#]+/(?:index\\.(?:html?|php|aspx?))?(?:#.*)?", re.I)',
         'ROOT_PAGE = re.compile(r"https?://[^/?#]+/(?:index\\.(?:html?|php|aspx?))?(?:[#?].*)?", re.I)' + M,
         "test_a_real_document_is_not_bare"),
        ("sole", "nothing_is_sole",
         "        sole = not (cited - set(bare))",
         "        sole = False" + M,
         "test_a_new_SOLE_bare_anchor_FAILS_by_name"),
        ("sole", "everything_is_sole",
         "        sole = not (cited - set(bare))",
         "        sole = True" + M,
         "test_a_CO_CITED_bare_anchor_is_reported_not_blocking"),
        ("sole", "sources_ignored_in_cited_set",
         "        cited = set(anchors) | {s for s in (sources or []) if isinstance(s, str)}",
         "        cited = set(anchors)" + M,
         "test_an_UNANCHORED_sources_id_still_co_cites"),
        ("reach", "crop_root_siblings_skipped",
         '        if k.endswith("_anchoring_urls"):',
         "        if False:" + M,
         "test_a_crop_root_sibling_anchor_is_walked"),
        ("reach", "nested_nodes_skipped",
         "            for k, v in node.items():\n                if k != \"anchoring_urls\":\n                    walk(v",
         "            for k, v in []:" + M + "\n                if k != \"anchoring_urls\":\n                    walk(v",
         "test_a_bare_anchor_in_a_region_cell_is_walked"),
        ("scope", "shells_counted",
         "    if not certified(crop):\n        return []\n    rows, _",
         "    if False:" + M + "\n        return []\n    rows, _",
         "test_an_uncertified_shell_is_exempt"),
        ("ratchet", "growth_invisible",
         "            for ident, sole, url in rows if sole and ident not in KNOWN]",
         "            for ident, sole, url in rows if False]" + M,
         "test_a_new_SOLE_bare_anchor_FAILS_by_name or test_substitution_FAILS"),
        ("ratchet", "waivers_ignored",
         "            for ident, sole, url in rows if sole and ident not in KNOWN]",
         "            for ident, sole, url in rows if sole]" + M,
         "test_population_and_verdict"),
        ("population", "anchors_not_counted",
         "    return rows, len(anchors)",
         "    return rows, 0" + M,
         "test_population_and_verdict"),
        ("refusal", "zero_certified_not_named",
         "    if n_cert == 0:",
         "    if False:" + M,
         "test_zero_certified_REFUSES"),
        ("refusal", "floor_off",
         "    if inspected < MIN_INSPECTED:",
         "    if False:" + M,
         "test_below_floor_REFUSES"),
        ("refusal", "floor_lowered",
         "MIN_INSPECTED = 28000",
         "MIN_INSPECTED = 0" + M,
         "test_floor"),
        ("cli", "violation_exits_zero",
         "    return 1 if V else 0",
         "    return 0" + M,
         "test_injection_rc1"),
    ],
}

# The WIRING: A62/A63 in whole_crop_gate and the roster half in gate_all, driven by the script-style
# entry-point integration test (run as a script; rc != 0 is caught). Each mutation targets its own
# file, so the fourth tuple field here is the target file, not a pytest selector.
INTEGRATION = "test_gate_citation_ratchets_a62_a63.py"
WIRING = {
    "script": INTEGRATION,
    "sentinel_file": INTEGRATION,
    "sentinel": (r'^CROP = "cabbage"$', 'CROP = "no-such-crop"' + M),
    "mutations": [
        ("wiring", "a62_violations_dropped", "whole_crop_gate.py",
         "for m in _sbrv:\n    fail(", "for m in []:" + M + "\n    fail("),
        ("wiring", "a63_violations_dropped", "whole_crop_gate.py",
         "for m in _bhv:\n    fail(", "for m in []:" + M + "\n    fail("),
        ("wiring", "gate_all_roster_violations_ignored", "gate_all.py",
         "        if _v:\n            for m in _v:", "        if False:" + M + "\n            for m in _v:"),
        ("wiring", "gate_all_refusal_ignored", "gate_all.py",
         "        if _why:", "        if False:" + M),
    ],
}

TARGETS = {"ratchet": RATCHET, "bare": BARE, "wiring": WIRING}


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_cite_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    # gate_all's floor reads the certified count from CLAUDE.md at the run root; without it the
    # wiring target's positive control is REFUSED (measured 2026-09-30, HARNESS DEAD as designed).
    os.symlink(os.path.join(REPO, "CLAUDE.md"), os.path.join(tmp, "CLAUDE.md"))
    return tmp, tools


def run_suite(tools, suite, selector):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools, suite), "-q",
                        "-x", "-k", selector, "--no-header", "-p", "no:cacheprovider"],
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


def run_script(tools, script):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", os.path.join(tools, script)], capture_output=True,
                       text=True, cwd=REPO, env=env)
    return r.returncode, r.stdout + r.stderr


def run_wiring(name, T, tools):
    print(f"==== {name}: whole_crop_gate A62/A63 + gate_all <- {T['script']} (script-style)")
    for fam, n, target, old, _new in T["mutations"]:
        c = open(os.path.join(tools, target), encoding="utf-8").read().count(old)
        if c != 1:
            sys.exit(f"HARNESS DEAD: anchor preflight: {fam}/{n} matches {c} times in {target}")
    print(f"anchor preflight: {len(T['mutations'])}/{len(T['mutations'])} anchors match exactly once")
    rc, out = run_script(tools, T["script"])
    if rc != 0:
        print(out[-2000:])
        sys.exit("HARNESS DEAD: the UNMUTATED integration script is already failing.")
    print("positive control: the unmutated integration script PASSES")
    old, new = T["sentinel"]
    clean, err = apply(tools, T["sentinel_file"], old, new, regex=True)
    if err:
        sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
    rc, _ = run_script(tools, T["script"])
    open(os.path.join(tools, T["sentinel_file"]), "w", encoding="utf-8").write(clean)
    if rc == 0:
        sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
    print("sentinel: reddened as required")
    caught, survived, broken = [], [], []
    for fam, n, target, old, new in T["mutations"]:
        clean, err = apply(tools, target, old, new)
        if err:
            broken.append((fam, n, err))
            print(f"  BROKEN   {fam}/{n}: {err}")
            continue
        rc, _ = run_script(tools, T["script"])
        open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
        if rc == 0:
            survived.append((fam, n, T["script"]))
            print(f"  SURVIVED {fam}/{n}")
        else:
            caught.append((fam, n))
            print(f"  caught   {fam}/{n}")
    print(f"{name}: {len(T['mutations'])} injected: {len(caught)} caught, {len(survived)} survived, "
          f"{len(broken)} broken\n")
    return caught, survived, broken


def run_target(name, T, tools):
    if "script" in T:
        return run_wiring(name, T, tools)
    print(f"==== {name}: {T['gate']} <- {T['suite']}")
    src = open(os.path.join(tools, T["gate"]), encoding="utf-8").read()
    bad = [f"  {f}/{n}: anchor matches {src.count(o)} times" for f, n, o, _x, _s in T["mutations"]
           if src.count(o) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(T['mutations'])}/{len(T['mutations'])} anchors match exactly once")

    rc, out = run_suite(tools, T["suite"], "test_")
    if rc != 0:
        print(out[-2000:])
        sys.exit(f"HARNESS DEAD: the UNMUTATED {T['suite']} is already failing (rc {rc}).")
    print("positive control: the WHOLE unmutated suite is GREEN")

    old, new, sel = T["sentinel"]
    clean, err = apply(tools, T["suite"], old, new, regex=True)
    if err:
        sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
    rc, _ = run_suite(tools, T["suite"], sel)
    open(os.path.join(tools, T["suite"]), "w", encoding="utf-8").write(clean)
    if rc == NOTHING_COLLECTED:
        sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
    if rc == 0:
        sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
    print("sentinel: reddened as required")

    caught, survived, broken = [], [], []
    for fam, n, old, new, sel in T["mutations"]:
        clean, err = apply(tools, T["gate"], old, new)
        if err:
            broken.append((fam, n, err))
            print(f"  BROKEN   {fam}/{n}: {err}")
            continue
        rc, _ = run_suite(tools, T["suite"], sel)
        open(os.path.join(tools, T["gate"]), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            broken.append((fam, n, f"driver {sel!r} collected NO TESTS"))
            print(f"  BROKEN   {fam}/{n}: collected no tests")
        elif rc == 0:
            survived.append((fam, n, sel))
            print(f"  SURVIVED {fam}/{n}  (driver: {sel})")
        else:
            caught.append((fam, n))
            print(f"  caught   {fam}/{n}")
    print(f"{name}: {len(T['mutations'])} injected: {len(caught)} caught, {len(survived)} survived, "
          f"{len(broken)} broken\n")
    return caught, survived, broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only", choices=["bare", "ratchet", "wiring"])
    a = ap.parse_args()
    targets = {a.only: TARGETS[a.only]} if a.only else TARGETS
    if a.list:
        for name, T in targets.items():
            for fam, n, *_ in T["mutations"]:
                print(f"{name}: {fam}/{n}")
        return 0
    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        total = {"caught": 0, "survived": 0, "broken": 0}
        for name, T in targets.items():
            c, s, b = run_target(name, T, tools)
            total["caught"] += len(c)
            total["survived"] += len(s)
            total["broken"] += len(b)
        print(f"TOTAL: {total['caught']} caught, {total['survived']} survived, {total['broken']} broken")
        return 1 if (total["survived"] or total["broken"]) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
