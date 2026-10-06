#!/usr/bin/env python3
"""mutate_promote_pla673_glossary -- mutation harness for the PLA-673 glossary promote (2026-10-05).

One mutation per guard (each switches ONE refusal off in promote_pla673_glossary.py); the suite test named beside it
must redden. Liveness (PLA-215 bar): anchor preflight (each anchor matches exactly once, else HARNESS DEAD), a
MUTATION-APPLIED marker checked on disk, a sentinel that must redden (the suite's pinned post SHA altered), and a
positive control (the whole suite, unmutated, green first). pytest rc 5 (nothing collected) is graded BROKEN.
Derived from mutate_promote_pla666_row_figures (same driver), with the mutation table rewritten for this promote.
Usage: mutate_promote_pla673_glossary.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
PR, SU = "promote_pla673_glossary.py", "test_promote_pla673_glossary.py"
F = "False"

MUTATIONS = [  # (name, anchor, replacement, the test that must redden)
    ("wrong_base", "    if got != BASE_SHA:", "    if " + F + ":", "wrong_base"),
    ("empty_stage", "    if not isinstance(ops, list) or not ops:", "    if " + F + ":", "empty_stage"),
    ("op_keys", "        if not isinstance(op, dict) or set(op) != OP_KEYS:", "        if " + F + ":", "op_keys_must_be_exact"),
    ("unknown_kind", '        if op["kind"] not in KINDS:', "        if " + F + ":", "unknown_kind"),
    ("empty_reason", '        if not (isinstance(op["reason"], str) and op["reason"].strip()):', "        if " + F + ":", "empty_reason"),
    ("dup_op", "    if dup:", "    if " + F + ":", "staged_twice"),
    ("old_absent", '        if op["old"] != ABSENT:', "        if " + F + ":", "old_must_be_absent"),
    ("not_a_crop", '            if op["crop"] not in idx:', "            if " + F + ":", "not_in_the_roster"),
    ("sibling_paths", '            if op["path"] not in SIBLINGS:', "            if " + F + ":", "only_create_the_two"),
    ("present", "        if present:", "        if " + F + ":", "existing_key or existing_catalog_id"),
    ("roster", '    if [c["slug"] for c in pre["crops"]] != [c["slug"] for c in post["crops"]]:', "    if " + F + ":", "roster_change"),
    ("top_keys", '    if list(post) != list(pre) + ["glossary"]:', "    if " + F + ":", "top_level_key_change"),
    ("top_values", '        if k not in ("crops", "source_catalog") and compact(pre[k]) != compact(post[k]):', "        if " + F + ":", "top_level_value_change"),
    ("catalog_existing", '        if k not in post["source_catalog"] or compact(post["source_catalog"][k]) != compact(v):', "        if " + F + ":", "existing_catalog_entry_change"),
    ("catalog_added", '    if added != [op["path"] for op in cat_ops]:', "    if " + F + ":", "catalog_additions"),
    ("crop_stray", "        if diff != set(sib.get(slug, {})):", "        if " + F + ":", "stray_crop_change"),
    ("post_value", '        if compact(got) != compact(op["new"]):', "        if " + F + ":", "post_value_not_new"),
    ("decision_crop", '        if d["crop"] not in (CATALOG, GLOSSARY, ROSTER) and d["crop"] not in pidx:', "        if " + F + ":", "decision_on_a_crop"),
    ("dup_row", "        if key in seen:", "        if " + F + ":", "duplicate_row"),
    ("quote_bytes", "        cached_quote(r, man, evidence_dir, text_cache, tag)", "        pass", "quote_not_in_bytes"),
    ("all_records", '    if set(sib) != set(roster) or any(set(v) != set(SIBLINGS) for v in sib.values()):', "    if " + F + ":", "every_record_gets"),
    ("placement", "        if pos != [want, want + 1]:", "        if " + F + ":", "sibling_placement"),
    ("null_decision", '                if "null-not-assessed" not in decided.get((ROSTER, k), ()):', "                if " + F + ":", "null_sibling_without"),
    ("pair_shape", '        if not (isinstance(src, list) and src and isinstance(anc, dict) and anc):', "        if " + F + ":", "sourced_pair_shape"),
    ("pair_ids", "        if list(src) != list(anc):", "        if " + F + ":", "sourced_pair_ids_diverge"),
    ("pair_catalog", '            if sid not in post["source_catalog"]:', "            if " + F + ":", "sourced_id_not_in_catalog"),
    ("pair_anchor_used", '            if not any(r["source_id"] == sid and r["url"] == anc[sid]["url"] for r in rows):', "            if " + F + ":", "sibling_anchor_unused"),
    ("pair_row_url", '            if r["source_id"] not in src or anc[r["source_id"]]["url"] != r["url"]:', "            if " + F + ":", "url_not_carried"),
    ("stray_row", "    if stray:", "    if " + F + ":", "unstaged_entry"),
    ("gl_ids", '    if list(post["glossary"]) != [op["path"] for op in gl_ops] or not gl_ops:', "    if " + F + ":", "ids_must_be_the_staged"),
    ("gl_row_id", '        if not m or m["term"] not in post["glossary"]:', "        if " + F + ":", "names_no_term"),
    ("gl_keys", "        if tuple(e) != ENTRY_KEYS:", "        if " + F + ":", "entry_keys"),
    ("gl_term", '        if e["term"] != tid:', "        if " + F + ":", "term_must_be"),
    ("dash", "    if EM_DASH in s or EN_DASH in s:", "    if " + F + ":", "em_dash"),
    ("degree", "    if BARE_DEGREE.search(s):", "    if " + F + ":", "without_F"),
    ("gl_numbering", "            if sorted(sents) != list(range(1, len(sents) + 1)):", "            if " + F + ":", "numbering_gap"),
    ("gl_disagree", "                if len(vals) != 1:", "                if " + F + ":", "rows_disagree"),
    ("gl_join", '            if " ".join(texts) != e[reg]:', "            if " + F + ":", "unevidenced_text"),
    ("gl_src_shape", '        if not (isinstance(e["sources"], list) and e["sources"] and isinstance(e["anchoring_urls"], dict)):', "        if " + F + ":", "sources_must_be_non_empty"),
    ("gl_src_order", '        if list(e["sources"]) != list(e["anchoring_urls"]):', "        if " + F + ":", "sources_and_anchors_order"),
    ("gl_catalog", "            if cat is None:", "            if " + F + ":", "glossary_source_not_in_catalog"),
    ("gl_document_level", '            if cat.get("url") != e["anchoring_urls"][sid].get("url"):', "            if " + F + ":", "portal_id"),
    ("gl_used", '            if not any(r["source_id"] == sid for r in rows):', "            if " + F + ":", "glossary_source_unused"),
    ("gl_row_named", '            if r["source_id"] not in e["sources"]:', "            if " + F + ":", "unnamed_id"),
    ("gl_row_url", '            if e["anchoring_urls"][r["source_id"]]["url"] != r["url"]:', "            if " + F + ":", "row_url_not_its_anchor"),
    ("fa_list", "        if not isinstance(fa, list) or not fa:", "        if " + F + ":", "field_additions_empty"),
    ("fa_shape", '            if not isinstance(f, dict) or set(f) != FA_KEYS or not set(f["sources"]) <= set(e["sources"]):', "            if " + F + ":", "field_additions_shape"),
    ("match_call", "        res = glossary_sense.classify_dataset(post, spec, floor=HILL_POPULATION)", "        res = glossary_sense.classify_dataset(post, spec, floor=0, refuse=False)", "match_must_classify or match_population"),
    ("match_population", "    if res.inspected != HILL_POPULATION:", "    if " + F + ":", "match_population_must_be_exact"),
    ("cat_id", '        if not isinstance(new, dict) or new.get("id") != op["path"]:', "        if " + F + ":", "catalog_id_must_match"),
    ("cat_manifest", '        if not any(new.get("url") in urls for urls in man.values()):', "        if " + F + ":", "catalog_url_needs"),
    ("cat_evidence", '        if not any(r["source_id"] == op["path"] and r["url"] == new.get("url") for r in ev):', "        if " + F + ":", "catalog_mint_must_be_evidenced"),
    ("gate_rc", "    if r.returncode != 0:", "    if " + F + ":", "gate_failure"),
    ("gate_population", "    if not m or int(m.group(1)) != certified or certified == 0:", "    if " + F + ":", "gate_population"),
]
SENTINEL = (SU, 'POST_SHA = "3ccc25f1', 'POST_SHA = "00000000', "real_stage")

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
    tmp = tempfile.mkdtemp(prefix="mut_pla673_")
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
