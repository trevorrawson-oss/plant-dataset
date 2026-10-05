#!/usr/bin/env python3
"""mutate_promote_housekeeping60_phase_c -- mutation harness for the housekeeping-60 Phase C promote (2026-10-04).

One mutation per guard (each switches ONE refusal off in promote_housekeeping60_phase_c.py); the suite test named
beside it must redden. Liveness (PLA-215 bar): anchor preflight (each anchor matches exactly once, else HARNESS DEAD),
a MUTATION-APPLIED marker checked on disk, a sentinel that must redden (the suite's pinned post SHA altered), and a
positive control (the whole suite, unmutated, green first). pytest rc 5 (nothing collected) is graded BROKEN.
Usage: mutate_promote_housekeeping60_phase_c.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
PR, SU = "promote_housekeeping60_phase_c.py", "test_promote_housekeeping60_phase_c.py"
F = "False"

MUTATIONS = [  # (name, anchor, replacement, the test that must redden)
    ("wrong_base", "    if got != BASE_SHA:", "    if " + F + ":", "wrong_base"),
    ("empty_stage", "    if not isinstance(ops, list) or not ops:", "    if " + F + ":", "empty_stage"),
    ("base_drift", '        if compact(got) != compact(op["old"]):', "        if " + F + ":", "drifted_base"),
    ("roster", '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if " + F + ":",
     "roster_change"),
    ("top_keys", "    if set(pre) != set(post):", "    if " + F + ":", "top_level_change"),
    ("top_values", '        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):',
     "        if " + F + ":", "top_level_value_change"),
    ("crop_stray", "        stray = sorted(fmt(list(p)) for p in diff if not any(p[:len(a)] == a for a in allowed))",
     "        stray = []", "stray_change"),
    ("catalog_stray",
     "    stray = sorted(fmt(list(p)) for p in cat_diff if not any(p[:len(a)] == a for a in cat_allowed))",
     "    stray = []", "catalog_stray"),
    ("post_value", "        if compact(got) != compact(want):", "        if " + F + ":", "post_value_not_new"),
    ("noop", '        if compact(got) == compact(op["old"]):', "        if " + F + ":", "noop_op"),
    ("dash", "    if EM_DASH in s or EN_DASH in s:", "    if " + F + ":", "em_dash"),
    ("degree", "    if BARE_DEGREE.search(s):", "    if " + F + ":", "bare_degree"),
    ("append_keeps", '            if not (isinstance(old, str) and isinstance(new, str) and new.startswith(old + " ")):',
     "            if " + F + ":", "edits_the_original"),
    ("append_dated", "            if not CORRECTION.fullmatch(new[len(old) + 1:]):", "            if " + F + ":",
     "without_a_dated"),
    ("null_decision",
     '        if op["kind"] in ("value", "prose") and op["new"] is None and (op["crop"], op["path"]) not in decided:',
     "        if " + F + ":", "null_without_decision"),
    ("record_only",
     '        if op["kind"] == "prose" and op["cited_at"] is None and decided.get((op["crop"], op["path"])) != '
     '"record-only":', "        if " + F + ":", "record_only_without"),
    ("dup_row", "        if key in seen:", "        if " + F + ":", "duplicate_row"),
    ("quote_bytes", "        cached_quote(r, man, evidence_dir, text_cache, tag)", "        pass", "quote_not_in_bytes"),
    ("cited_url", '        if r["url"] not in cited_urls(crop):', "        if " + F + ":", "url_not_cited_on_crop"),
    ("anchors_op_row", '            if (op["new"] or {}).get(r["source_id"], {}).get("url") != r["url"]:',
     "            if " + F + ":", "anchors_op_row_must_be_carried"),
    ("block_anchor", '            if (blk.get("anchoring_urls") or {}).get(r["source_id"], {}).get("url") != r["url"]:',
     "            if " + F + ":", "missing_from_block"),
    ("block_sources", '            if "sources" in blk and r["source_id"] not in blk["sources"]:',
     "            if " + F + ":", "missing_from_sources"),
    ("missing_row",
     '        if op["kind"] in ("prose", "value") and op["new"] is not None and (op["crop"], op["path"]) not in '
     'rows_for:', "        if " + F + ":", "prose_without_evidence"),
    ("unused_anchor",
     '            if sid not in used and decided.get((op["crop"], f"{op[\'path\']}.{sid}")) != "kept":',
     "            if " + F + ":", "unused_unkept_anchor"),
    ("diverge",
     '            if blk is not None and "sources" in blk and set(blk["sources"]) != set(blk.get("anchoring_urls") '
     'or {}):', "            if " + F + ":", "sources_and_anchors_diverge"),
    ("ortho_scope", '            if op["new"] != fixed:', "            if " + F + ":",
     "changes_more_than_spelling"),
    ("ortho_decision", '        if op["kind"] == "orthography" and decided.get((op["crop"], op["path"])) != "orthography-only":',
     "        if " + F + ":", "orthography_op_without"),
    ("correction_brackets", 'CORRECTION = re.compile(r"\\[CORRECTION (\\d{4}-\\d{2}-\\d{2}): (?:[^\\[\\]]|\\[\\d+\\])+\\]")',
     'CORRECTION = re.compile(r"\\[CORRECTION (\\d{4}-\\d{2}-\\d{2}): .+\\]")', "correction_allows_a_path_index"),
    ("gate_rc", "            if r.returncode != 0:", "            if " + F + ":", "gate_failure"),
    ("gate_count", '            passed += r.stdout.count("\\nGATE: PASS")', "            passed += 1",
     "gate_count_is_the_gates_own_verdict"),
    ("gate_verdict_check", "    if passed != len(slugs):", "    if " + F + ":", "gate_count_is_the_gates_own_verdict"),
]
SENTINEL = (SU, 'POST_SHA = "afbd4113', 'POST_SHA = "00000000', "real_stage")


def run_driver(tools, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, SU), "-q", "-x", "--no-header",
           "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new + "  " + MARKER, 1))
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_hk60c_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging", "batches"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        src = open(os.path.join(tools, PR), encoding="utf-8").read()
        bad = [m[0] for m in muts if src.count(m[1]) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        rc, out = run_driver(tools, None)
        if rc != 0:
            print(out[-2000:])
            sys.exit(f"HARNESS DEAD: the unmutated suite is already failing (rc {rc})")
        print("positive control: the WHOLE suite, unmutated, is GREEN")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc in (0, NOTHING_COLLECTED):
            sys.exit(f"HARNESS DEAD: the sentinel did not redden (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, old, new, sel in muts:
            clean, err = apply(tools, PR, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, _ = run_driver(tools, sel)
            open(os.path.join(tools, PR), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append(name); print(f"  BROKEN   {name}: driver collected nothing (-k {sel})")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  (-k {sel})")
            else:
                caught.append(name); print(f"  caught   {name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
