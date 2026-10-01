#!/usr/bin/env python3
"""mutate_pla532_technique_sources_suite -- mutation harness for the PLA-532 catalog-admission promote suite.

BUILT TO THE PLA-215 BAR. One defect per guard, injected into a SCRATCH COPY of the promote source;
each mutation names the suite driver that must catch it, and ONLY that driver runs, so a mutation
counts as caught only if its own driver reddens.

THE LIVENESS DEFENSE: anchor preflight (every anchor matches EXACTLY ONCE), a MUTATION-APPLIED marker
asserted on disk, a sentinel that MUST redden, a positive control that runs the WHOLE unmutated suite
GREEN in the scratch copy (a single-test control can pass while a sibling is already red), and
bytecode disabled with __pycache__ cleared before every run. rc 5 (a selector that collected nothing)
is graded BROKEN, never caught. Any of those failing exits HARNESS DEAD.

The scratch copy links the repo's .git (promote_fixture shells out to `git show`) and the two local
caches (.evidence_cache, .doc_cache) so the positive control's real-evidence test reads what the
promote read.

Usage:
    mutate_pla532_technique_sources_suite.py             # all families
    mutate_pla532_technique_sources_suite.py --family X  # one family
    mutate_pla532_technique_sources_suite.py --list
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
PROMOTE = "promote_pla532_technique_sources.py"
SUITE = "test_promote_pla532_technique_sources.py"
MARKER = "# MUTATION-APPLIED"

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    # ---- guard 0: entry
    ("entry", "base_sha_check_removed", "    if got != BASE_SHA:", "    if False:  " + MARKER,
     "test_main_refuses_a_moved_base"),

    # ---- guard 1: spec shape
    ("spec", "id_count_not_pinned", "    if len(new) != EXPECTED_NEW_SOURCES:", "    if False:  " + MARKER,
     "test_refuses_a_ninth_id"),
    ("spec", "tables_not_compared_as_sets", "        if set(spec[name]) != ids:", "        if False:  " + MARKER,
     "test_refuses_tables_that_disagree"),
    ("spec", "entry_key_set_not_compared", "        if set(e) != ENTRY_KEYS:", "        if False:  " + MARKER,
     "test_refuses_an_extra_key"),
    ("spec", "id_key_mismatch_accepted", '        if e["id"] != sid:', "        if False:  " + MARKER,
     "test_refuses_an_id_that_is_not_its_key"),
    ("spec", "claim_class_vocabulary_unchecked", "        if not cls or not set(cls) <= CLAIM_CLASSES:",
     "        if not cls:  " + MARKER, "test_refuses_an_unknown_claim_class"),
    ("spec", "empty_claim_class_accepted", "        if not cls or not set(cls) <= CLAIM_CLASSES:",
     "        if cls and not set(cls) <= CLAIM_CLASSES:  " + MARKER, "test_refuses_an_empty_claim_class"),
    ("spec", "quoteless_entry_accepted", '        if not spec["quotes"][sid]:', "        if False:  " + MARKER,
     "test_refuses_an_entry_with_no_quote"),

    # ---- guard 2: entry validity
    ("entries", "http_accepted", '        if not (isinstance(url, str) and url.startswith("https://")):',
     "        if False:  " + MARKER, "test_refuses_plain_http"),
    ("entries", "bare_host_accepted", "        if is_bare(url):", "        if False:  " + MARKER,
     "test_refuses_a_bare_host"),
    ("entries", "url_not_matched_to_evidence", '        if url != spec["evidence"][sid]["url"]:', "        if False:  " + MARKER,
     "test_refuses_a_url_other_than_the_fetched_one"),
    ("entries", "non_t1_accepted",
     '        if e["tier"] != "T1" or e["trust_tier"] != "high" or e["source_class"] != "university_extension":',
     "        if False:  " + MARKER, "test_refuses_a_t2"),
    ("entries", "admission_date_unchecked", '        if e["accessed"] != spec["accessed"]:', "        if False:  " + MARKER,
     "test_refuses_a_wrong_admission_date"),
    ("entries", "blank_title_accepted", '        if not (isinstance(e["title"], str) and e["title"].strip()):',
     "        if False:  " + MARKER, "test_refuses_a_blank_title"),
    ("entries", "blank_citable_for_accepted", '        if not (isinstance(e["citable_for"], str) and e["citable_for"].strip()):',
     "        if False:  " + MARKER, "test_refuses_a_blank_citable_for"),

    # ---- guard 3: pre-state
    ("prestate", "catalog_count_not_pinned", "    if len(sc) != EXPECTED_PRE_CATALOG:", "    if False:  " + MARKER,
     "test_refuses_a_moved_catalog_count"),
    ("prestate", "existing_id_overwritten", "        if sid in sc:", "        if False:  " + MARKER,
     "test_refuses_an_id_that_already_exists"),
    ("prestate", "duplicate_url_accepted", '        if e["url"] in urls:', "        if False:  " + MARKER,
     "test_refuses_a_url_already_catalogued"),

    # ---- guard 4: evidence
    ("evidence", "absent_bytes_accepted", "        if not os.path.exists(f):", "        if False:  " + MARKER,
     "test_refuses_absent_raw_bytes"),
    ("evidence", "hash_unchecked", '        if got != ev["sha256"]:', "        if False:  " + MARKER,
     "test_refuses_bytes_that_do_not_hash"),
    ("evidence", "manifest_unchecked", '        if (ev["sha256"], ev["url"]) not in rows:', "        if False:  " + MARKER,
     "test_refuses_a_missing_manifest_row"),
    ("evidence", "absent_text_accepted", "        if text is None:", "        if False:  " + MARKER,
     "test_refuses_absent_cached_text"),
    ("evidence", "quote_unchecked", "            if norm(q) not in body:", "            if False:  " + MARKER,
     "test_refuses_a_quote_not_on_the_page"),

    # ---- guard 5: post-state blast radius
    ("post", "drop_invisible", "    if not set(psc) <= set(qsc):", "    if False:  " + MARKER,
     "test_refuses_a_dropped_entry"),
    ("post", "undeclared_addition_accepted", "    if added != declared:", "    if False:  " + MARKER,
     "test_refuses_an_undeclared_addition"),
    ("post", "existing_entry_edit_invisible",
     "        if json.dumps(psc[k], sort_keys=True, ensure_ascii=False) != json.dumps(qsc[k], sort_keys=True, ensure_ascii=False):",
     "        if False:  " + MARKER, "test_refuses_an_edited_existing_entry"),
    ("post", "top_level_key_set_not_compared", "    if set(pre) != set(post):", "    if False:  " + MARKER,
     "test_refuses_a_new_top_level_key"),
    ("post", "top_level_value_change_invisible", "        if serialize(pre[k]) != serialize(post[k]):", "        if False:  " + MARKER,
     "test_refuses_a_changed_crop"),
    ("post", "a54_not_run", "    if tv:", "    if False:  " + MARKER,
     "test_refuses_an_a54_violation"),
    ("post", "crop_citation_invisible", "        if hit:", "        if False:  " + MARKER,
     "test_verify_post_reaches_the_crop_citation_check"),
    ("post", "cites_misses_sources_lists",
     '                    hit.update(x for x in v if x in ids)\n                elif',
     '                    pass  ' + MARKER + '\n                elif',
     "test_refuses_a_crop_citing_a_new_id"),

    # ---- serializer
    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_the_post_is_compact"),
]


def sentinel_for(tools_dir):
    """Built from the CURRENT pin, so a legitimate pin move does not break the sentinel."""
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r'^OUTPUT_SHA = "([0-9a-f]{64})"$', src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the OUTPUT_SHA pin to build a sentinel from")
    return (m.group(0), f'OUTPUT_SHA = "{"0" * 64}"  ' + MARKER,
            "test_the_replayed_post_is_the_pinned_output")


def preflight(tools_dir):
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = [f"  {fam}/{name}: anchor matches {src.count(old)} times\n      {old[:90]!r}"
           for fam, name, old, _n, _s in MUTATIONS if src.count(old) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed (zero matches edits nothing and reports a "
                 "FALSE SURVIVOR; two matches edit a site nobody intended).\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla532_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    for name in (".evidence_cache", ".doc_cache"):
        os.symlink(os.path.join(HERE, name), os.path.join(tools, name))
    return tmp, tools


def run_suite(tools_dir, selector=None):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "--no-header",
           "-p", "no:cacheprovider"]
    if selector:
        cmd += ["-k", selector]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
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
        return None, "MUTATION-APPLIED marker absent, or file unchanged on disk"
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
            print(f"{f} ({len(names)}): " + ", ".join(names))
        return 0

    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)
        rc, out = run_suite(tools)
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the WHOLE unmutated suite is not green in the scratch copy.")
        print("positive control: whole unmutated suite GREEN in scratch")

        old, new, sel = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, SUITE)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, SUITE), "w", encoding="utf-8").write(clean)
        if rc == 5:
            sys.exit("HARNESS DEAD: the sentinel's selector collected no tests (rc 5)")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED; nothing below can be trusted.")
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
            if rc == 5:
                broken.append((fam, name, f"selector {sel!r} collected no tests (rc 5)"))
                print(f"  BROKEN   {fam}/{name}: selector collected nothing")
            elif rc == 0:
                survived.append((fam, name, sel))
                print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name))
                print(f"  caught   {fam}/{name}")

        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        for f, n, e in broken:
            print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived:
            print(f"  SURVIVOR {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
