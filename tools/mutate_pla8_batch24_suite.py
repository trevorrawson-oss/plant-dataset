#!/usr/bin/env python3
"""Mutation harness for the batch-24 promote (PLA-215).

Families. `premise` attacks the SPLIT schema premise in both directions per crop, plus the severity
split -- which runs the OPPOSITE way to the schema split -- from both sides. `types` attacks `type`
as a key SET FROM NOTHING, which is a different guard from batch 23's coarse->fine upgrade. `ids`
attacks the positional pin table and its COVERAGE assertion. `scope` attacks BOTH halves of the
scope split; the own half existed only as an unused tuple element until this suite was written.
`spelling` attacks the reuse across a spelling difference, anchored on the organism. `taxon`
attacks the cross-allium reuse. `stem` attacks the singular/plural class an exact-id check cannot
see, including THE STEMMER ITSELF. `twins` attacks the schema-aware comparison, including a
mutation that restores the EXACT historical bug -- comparing FULL-schema fields on crops that do
not carry them, so 6 of 8 match on `None` and the scan reports 3 twins where there are zero.
`precedent` attacks two passes, a declared-identity pin table, the branch ORDER, and THE METRIC
ITSELF. `echo`, `temps`, `vocab`, `validate`, `blast`, `catalog`, `mechanics` follow.

THE METRIC MUTATIONS ARE THE POINT OF THIS HARNESS.

Batch 23's copy guard was reachable, non-vacuous and mutation-tested 3/3 -- every property this
convention checks -- and it scored the batch's only real copy at 0.431 and passed it. A harness
proves a guard FIRES; it cannot prove the guard MEASURES the right thing, because the branch fires
correctly in every one of these cases and only the NUMBER handed to it is wrong. So the metric
carries mutations of its own (`autojunk`, the per-register combiner, the symmetric max, the prune
floor) aimed at the SUITE's `MetricDiscriminates`, which asserts numbers rather than branches.

Two guards were LIFTED OUT of main() so this harness can reach them. A guard that only exists
inside an entry point the suite never calls is untested code wearing a guard's clothes.

TWO assertions are WITHDRAWN rather than injected, each verified unreachable by construction, the
arithmetic asserted in the suite's `test_the_touched_and_per_crop_counts_are_FORWARD_assertions`,
and both documented at their site in the promote: `verify_post`'s touched-problem count (81 added
keys over at most 3 field names per problem force exactly 27 triples) and its per-crop tally (each
batch crop's pinned count IS its full problem count, and those maxima sum to 27). A forward
assertion is not a gap, and padding a harness total with one is not coverage.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_batch24.py")
PROMOTE = os.path.join(HERE, "promote_pla8_batch24.py")
STAGING_NAME = "pla8_batch24_alliums"
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- premise: the SPLIT schema, both directions, and the inverse severity split -----------
    ("premise: a missing batch crop is accepted", "premise", PROMOTE,
     "        if c not in by:", "        if False:"),
    ("premise: a problem-count drift is accepted", "premise", PROMOTE,
     "        if len(got) != EXPECTED_PROBLEMS[c]:", "        if False:"),
    ("premise: an already-laddered target is accepted", "premise", PROMOTE,
     '            if p.get("control_ladder") is not None:', "            if False:"),
    ("premise: a pre-existing id is accepted", "premise", PROMOTE,
     '            if p.get("id") is not None:', "            if False:"),
    ("premise: a field missing from the crop's OWN schema is accepted", "premise", PROMOTE,
     '                if not (p.get(f) or "").strip():', "                if False:"),
    ("premise: the OTHER schema's fields are accepted (the split stops being checked)",
     "premise", PROMOTE,
     "                if f in p and f not in fields:", "                if False:"),
    ("premise: the other-schema field set is emptied", "premise", PROMOTE,
     "        other = ALLIUM_SCHEMA_FIELDS if fields is FULL_SCHEMA_FIELDS else FULL_SCHEMA_FIELDS",
     "        other = ()"),
    ("premise: every crop is scanned as FULL schema (the brief's original error)",
     "premise", PROMOTE,
     "        fields = SCHEMA_FOR[c]\n"
     "        other = ALLIUM_SCHEMA_FIELDS if fields is FULL_SCHEMA_FIELDS else FULL_SCHEMA_FIELDS",
     "        fields = FULL_SCHEMA_FIELDS\n"
     "        other = ALLIUM_SCHEMA_FIELDS"),
    ("premise: a NOTE-schema field is accepted", "premise", PROMOTE,
     "                if f in p:", "                if False:"),
    ("premise: the severity split is not enforced", "premise", PROMOTE,
     "            if has_sev != SEVERITY_EXPECTED[c]:", "            if False:"),
    ("premise: the severity pin is flipped to uniform-present", "premise", PROMOTE,
     'SEVERITY_EXPECTED = {"chives": False, "leek": True, "onion": True, "shallot": True}',
     'SEVERITY_EXPECTED = {"chives": True, "leek": True, "onion": True, "shallot": True}'),
    ("premise: missing sources/anchoring_urls is accepted", "premise", PROMOTE,
     '            if not p.get("sources") or not p.get("anchoring_urls"):', "            if False:"),
    ("premise: the coverage count is not pinned", "premise", PROMOTE,
     '    if seen != sum(EXPECTED_PROBLEMS.values()):\n'
     '        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"',
     '    if False:\n'
     '        raise SystemExit("REFUSED: schema premise scanned %d problems, expected %d"'),

    # ---- types: SET FROM NOTHING --------------------------------------------------------------
    ("types: a pre-existing type key is accepted", "types", PROMOTE,
     '                if p.get("type") is not None:', "                if False:"),
    ("types: a staged type off the pin is accepted", "types", PROMOTE,
     '                if o.get("type") != want:', "                if False:"),
    ("types: a type outside the gate's type map is accepted", "types", PROMOTE,
     '                if o.get("type") not in _TYPE_TARGETS:', "                if False:"),
    ("types: a staged/canonical length mismatch is accepted", "types", PROMOTE,
     "            if len(pre) != len(post):", "            if False:"),
    ("types: the coverage count is not pinned", "types", PROMOTE,
     '    if seen != sum(EXPECTED_PROBLEMS.values()):\n'
     '        raise SystemExit("REFUSED: type set scanned %d, expected %d"',
     '    if False:\n'
     '        raise SystemExit("REFUSED: type set scanned %d, expected %d"'),

    # ---- ids ----------------------------------------------------------------------------------
    ("ids: the pin table size is not asserted", "ids", PROMOTE,
     "    if len(ID_CONVENTION) != sum(EXPECTED_PROBLEMS.values()):", "    if False:"),
    ("ids: an out-of-range pinned position is accepted", "ids", PROMOTE,
     "        if i >= len(pre) or i >= len(post):", "        if False:"),
    ("ids: a canonical name drift is accepted", "ids", PROMOTE,
     '        if pre[i].get("name") != name:', "        if False:"),
    ("ids: a staged id off the pin is accepted", "ids", PROMOTE,
     '        if post[i].get("id") != pid:', "        if False:"),
    ("ids: the pin COVERAGE assertion is removed", "ids", PROMOTE,
     "    if seen != positions:", "    if False:"),
    ("ids: a duplicate id within a crop is accepted", "ids", PROMOTE,
     "        if len(ids) != len(set(ids)):", "        if False:"),

    # ---- scope: BOTH halves of the split ------------------------------------------------------
    ("scope: a stale scope pin is accepted", "scope", PROMOTE,
     "        if new_id not in staged_ids:", "        if False:"),
    ("scope: a 'minted' id that is already live is accepted", "scope", PROMOTE,
     "        if new_id in live:", "        if False:"),
    ("scope: the resembled id vanishing is accepted", "scope", PROMOTE,
     "        if resembles not in live:", "        if False:"),
    ("scope: the OTHER half (the live storage-rot reason) vanishing is accepted", "scope", PROMOTE,
     "        if other_phrase.lower() not in oblob:", "        if False:"),
    ("scope: the OWN half (chives' foliar-blight reason) vanishing is accepted", "scope", PROMOTE,
     "        if own_phrase.lower() not in sblob:", "        if False:"),
    ("scope: the own-side anchor stops requiring exactly one pinned position", "scope", PROMOTE,
     "        if len(own) != 1:", "        if False:"),

    # ---- spelling ------------------------------------------------------------------------------
    ("spelling: a pin missing from the batch is accepted", "spelling", PROMOTE,
     '        if not hit:\n'
     '            raise SystemExit("REFUSED: spelling pin %s/%s is not in the batch"',
     '        if False:\n'
     '            raise SystemExit("REFUSED: spelling pin %s/%s is not in the batch"'),
    ("spelling: the display name vanishing is accepted", "spelling", PROMOTE,
     "        if src is None:", "        if False:"),
    ("spelling: the ORGANISM anchor vanishing is accepted", "spelling", PROMOTE,
     "        if organism.lower() not in blob:", "        if False:"),

    # ---- taxon ---------------------------------------------------------------------------------
    ("taxon: a reuse pin missing from the batch is accepted", "taxon", PROMOTE,
     "        if pid not in staged_ids:", "        if False:"),
    ("taxon: the precedent crop losing the id is accepted", "taxon", PROMOTE,
     '        if not hit:\n'
     '            raise SystemExit("REFUSED: %r no longer holds %r, so the reuse is unproven"',
     '        if False:\n'
     '            raise SystemExit("REFUSED: %r no longer holds %r, so the reuse is unproven"'),
    ("taxon: the taxon phrase vanishing is accepted", "taxon", PROMOTE,
     "        if phrase.lower() not in blob:", "        if False:"),

    # ---- stem -----------------------------------------------------------------------------------
    ("stem: an unadjudicated stem variant is accepted", "stem", PROMOTE,
     '                if (p["id"], lid) not in STEM_VARIANT_PINS:', "                if False:"),
    ("stem: the adjudicated-pair count is not pinned", "stem", PROMOTE,
     "    if pinned != EXPECTED_STEM_VARIANT_HITS:", "    if False:"),
    ("stem: THE STEMMER goes plural-blind again (the original bug)", "stem", PROMOTE,
     '        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:', "        elif False:"),

    # ---- twins: the schema-aware comparison -----------------------------------------------------
    ("twins: a template twin appearing is accepted", "twins", PROMOTE,
     "                    if tuple(pp.get(k) for k in fields) == key:", "                    if False:"),
    ("twins: THE HISTORICAL BUG -- compare FULL fields on crops that do not carry them",
     "twins", PROMOTE,
     "        fields = SCHEMA_FOR[c]\n        for _f, p in problems(by[c]):",
     "        fields = FULL_SCHEMA_FIELDS\n        for _f, p in problems(by[c]):"),
    ("twins: the batch-side presence filter is removed (absence counts as data)", "twins", PROMOTE,
     "            if not all(p.get(k) for k in fields):", "            if False:"),
    ("twins: the shipped-side presence filter is removed", "twins", PROMOTE,
     "                    if not all(pp.get(k) for k in fields):", "                    if False:"),
    ("twins: the anti-vacuity branch is removed", "twins", PROMOTE,
     '    if compared == 0:\n'
     '        raise SystemExit("REFUSED: no schema-compatible shipped problem was compared; the '
     'twin "',
     '    if False:\n'
     '        raise SystemExit("REFUSED: no schema-compatible shipped problem was compared; the '
     'twin "'),

    # ---- precedent: branches, order, AND the metric ---------------------------------------------
    ("precedent: pass A accepts a copy of the same problem and method", "precedent", PROMOTE,
     '                    if sc >= PRECEDENT_COPY_THRESHOLD:\n'
     '                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s\'s rung '
     'for the "',
     '                    if False:\n'
     '                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s\'s rung '
     'for the "'),
    ("precedent: pass B accepts a rung lifted onto a DIFFERENT problem", "precedent", PROMOTE,
     '                    if sc >= PRECEDENT_COPY_THRESHOLD:\n'
     '                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s\'s rung '
     'for %s "',
     '                    if False:\n'
     '                        raise SystemExit("REFUSED: %s/%s/%s is %.3f similar to %s\'s rung '
     'for %s "'),
    ("precedent: a declared identity naming a crop with no such rung is accepted",
     "precedent", PROMOTE,
     "                    if not match:", "                    if False:"),
    ("precedent: a declared identity that is NOT byte-identical is accepted", "precedent", PROMOTE,
     '                    if (r.get("note_beginner") != nb) or (r.get("note_seasoned") != ns):',
     "                    if False:"),
    ("precedent: an unfound declared identity is accepted", "precedent", PROMOTE,
     "    if declared_seen != set(DECLARED_IDENTITIES):", "    if False:"),
    ("precedent: the pass-A anti-vacuity branch is removed", "precedent", PROMOTE,
     '    if cmp_a == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass A made 0 comparisons; it is vacuous")',
     '    if False:\n'
     '        raise SystemExit("REFUSED: precedent pass A made 0 comparisons; it is vacuous")'),
    ("precedent: the pass-B anti-vacuity branch is removed", "precedent", PROMOTE,
     '    if cmp_b == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass B made 0 comparisons; it is vacuous")',
     '    if False:\n'
     '        raise SystemExit("REFUSED: precedent pass B made 0 comparisons; it is vacuous")'),
    ("precedent: the branch ORDER is restored, making pass B's branch unreachable again",
     "precedent", PROMOTE,
     '    if cmp_b == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass B made 0 comparisons; it is vacuous")\n'
     '    if cmp_a == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass A made 0 comparisons; it is vacuous")',
     '    if cmp_a == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass A made 0 comparisons; it is vacuous")\n'
     '    if cmp_b == 0:\n'
     '        raise SystemExit("REFUSED: precedent pass B made 0 comparisons; it is vacuous")'),
    ("precedent: THE METRIC loses autojunk=False (dilution 1)", "precedent", PROMOTE,
     "            s = max(difflib.SequenceMatcher(None, u, v, autojunk=False).ratio(),\n"
     "                    difflib.SequenceMatcher(None, v, u, autojunk=False).ratio())",
     "            s = max(difflib.SequenceMatcher(None, u, v).ratio(),\n"
     "                    difflib.SequenceMatcher(None, v, u).ratio())"),
    ("precedent: THE METRIC becomes single-order again (dilution 3)", "precedent", PROMOTE,
     "            s = max(difflib.SequenceMatcher(None, u, v, autojunk=False).ratio(),\n"
     "                    difflib.SequenceMatcher(None, v, u, autojunk=False).ratio())",
     "            s = difflib.SequenceMatcher(None, u, v, autojunk=False).ratio()"),
    ("precedent: the per-register combiner becomes a MEAN (dilution 2)", "precedent", PROMOTE,
     "            if s > best:\n                best = s\n        return best",
     "            best = s if best == 0.0 else (best + s) / 2.0\n        return best"),
    ("precedent: the O(1) prune becomes unsound and hides real pairs", "precedent", PROMOTE,
     "            if bound <= best or bound <= floor:", "            if bound <= best + 0.5 or bound <= floor + 0.5:"),
    ("precedent: the threshold is loosened past the measured ceiling", "precedent", PROMOTE,
     "PRECEDENT_COPY_THRESHOLD = 0.70", "PRECEDENT_COPY_THRESHOLD = 0.99"),

    # ---- echo -------------------------------------------------------------------------------------
    ("echo: a whole-note echo is accepted", "echo", PROMOTE,
     "                    if v in whole:", "                    if False:"),
    ("echo: a sentence echo is accepted", "echo", PROMOTE,
     "                        if s in sent:", "                        if False:"),
    ("echo: the DECLARED-IDENTITY exemption is removed (two guards then contradict)",
     "echo", PROMOTE,
     '                if (c, p["id"], r["method"]) in DECLARED_IDENTITIES:\n                    continue',
     '                if False:\n                    continue'),
    ("echo: the empty-corpus anti-vacuity branch is removed", "echo", PROMOTE,
     "    if not whole:", "    if False:"),
    ("echo: the no-notes-scanned anti-vacuity branch is removed", "echo", PROMOTE,
     "    if checked == 0:", "    if False:"),

    # ---- temps -------------------------------------------------------------------------------------
    ("temps: an unwarranted temperature figure is accepted", "temps", PROMOTE,
     "                            if not (in_src or in_meth):",
     "                            if False:"),
    ("temps: the pinned figure count is removed", "temps", PROMOTE,
     "    if found != EXPECTED_TEMP_FIGURES:", "    if False:"),

    # ---- vocab -------------------------------------------------------------------------------------
    ("vocab: internal ladder vocabulary is accepted", "vocab", PROMOTE,
     "                    if m:", "                    if False:"),
    ("vocab: the anti-vacuity branch is removed", "vocab", PROMOTE,
     "    if seen == 0:", "    if False:"),

    # ---- validate ----------------------------------------------------------------------------------
    ("validate: an empty ladder is accepted", "validate", PROMOTE,
     "            if not ladder:", "            if False:"),
    ("validate: an unknown method is accepted", "validate", PROMOTE,
     "                if meth not in cm:", "                if False:"),
    ("validate: a duplicate method in one ladder is accepted", "validate", PROMOTE,
     "                if meth in seen_methods:", "                if False:"),
    ("validate: an unknown tier is accepted", "validate", PROMOTE,
     "                if tier not in TIERS:", "                if False:"),
    ("validate: a tier inversion is accepted", "validate", PROMOTE,
     "                if TIERS.index(tier) < last:", "                if False:"),
    ("validate: an applies_to incoherence is accepted", "validate", PROMOTE,
     '                if "any" not in applies and not _type_ok(p.get("type"), applies):',
     "                if False:"),
    ("validate: a missing register is accepted", "validate", PROMOTE,
     "                if not nb or not ns:", "                if False:"),
    ("validate: identical registers are accepted", "validate", PROMOTE,
     "                if nb.strip() == ns.strip():", "                if False:"),
    ("validate: an unexpected rung key is accepted", "validate", PROMOTE,
     '                if set(r) - {"method", "note_beginner", "note_seasoned"}:',
     "                if False:"),
    ("validate: a hygiene violation is accepted", "validate", PROMOTE,
     "                    if bad:", "                    if False:"),
    ("validate: the per-crop rung count is not pinned", "validate", PROMOTE,
     "        if n != EXPECTED_RUNGS[c]:", "        if False:"),
    ("validate: the absolute vocabulary is emptied", "validate", PROMOTE,
     '    for w in ("always", "never", "completely", "totally", "harmless", "guaranteed",\n'
     '              "eliminate", "eliminates"):',
     "    for w in ():"),
    ("validate: the em/en dash check is removed", "validate", PROMOTE,
     '    if "—" in s or "–" in s:', "    if False:"),

    # ---- blast -------------------------------------------------------------------------------------
    ("blast: a DROPPED leaf key is accepted", "blast", PROMOTE,
     "    if dropped:", "    if False:"),
    ("blast: an unexpected ADDED leaf key is accepted", "blast", PROMOTE,
     "    if unexpected:", "    if False:"),
    ("blast: the added-key count is not pinned", "blast", PROMOTE,
     "    if len(added) != want:", "    if False:"),
    ("blast: a bystander or pre-existing leaf change is accepted", "blast", PROMOTE,
     "        if pre[k] != post[k]:", "        if False:"),
    ("blast: the added-key scope stops being the batch crops", "blast", PROMOTE,
     '    unexpected = {k for k in added\n'
     '                  if not (k[0] in CROPS and k[3] in ("id", "type", "control_ladder"))}',
     "    unexpected = set()"),

    # ---- catalog -----------------------------------------------------------------------------------
    ("catalog: a control_methods change is accepted", "catalog", PROMOTE,
     '    if serialize(data["control_methods"]) != before_cm:', "    if False:"),
    ("catalog: a source_catalog change is accepted", "catalog", PROMOTE,
     '    if serialize(data["source_catalog"]) != before_sc:', "    if False:"),

    # ---- mechanics ---------------------------------------------------------------------------------
    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the ladders are never attached", PROMOTE,
            '                p["control_ladder"] = copy.deepcopy(o["control_ladder"])',
            '                _skip = copy.deepcopy(o["control_ladder"])')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1], SENTINEL[2])]
    for label, f, old in rows:
        with open(f) as fh:
            n = fh.read().count(old)
        if n != 1:
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_batch24_")
    sandbox_staging = os.path.join(wd, "staging")
    os.makedirs(sandbox_staging)
    src_staging = os.path.join(REPO, "tools", "staging", STAGING_NAME)
    for fn in os.listdir(src_staging):
        if fn.startswith("out_"):
            shutil.copy2(os.path.join(src_staging, fn), os.path.join(sandbox_staging, fn))
    with open(SUITE) as fh:
        src = fh.read()
    src = src.replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    with open(os.path.join(wd, os.path.basename(SUITE)), "w") as fh:
        fh.write(src)
    with open(PROMOTE) as fh:
        s = fh.read()
    s = s.replace('STAGING = os.path.join(REPO, "tools", "staging", "%s")' % STAGING_NAME,
                  "STAGING = %r" % sandbox_staging, 1)
    # The sandbox copy sits in a temp dir, so its own dirname(dirname(__file__)) would point REPO
    # at /tmp -- breaking CANONICAL, the tools/ import path, and the SUBPROCESS the suite runs.
    # Pin REPO to the real repo; only STAGING is meant to differ.
    s = s.replace("REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
                  "REPO = %r" % REPO, 1)
    if path == PROMOTE:
        s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
    with open(os.path.join(wd, os.path.basename(PROMOTE)), "w") as fh:
        fh.write(s)
    if path:
        with open(os.path.join(wd, os.path.basename(path))) as fh:
            if MARKER not in fh.read():
                shutil.rmtree(wd)
                raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 batch 24, the alliums")
    print("=" * 78)
    if not preflight():
        return 1
    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails (the CLEAN fixture must pass).")
        return 1
    print("positive control : GREEN")
    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print("HARNESS DEAD: %s SURVIVED." % label)
        return 1
    print("sentinel         : RED as required\n")

    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    todo = [m for m in MUTATIONS if not only or m[1] in only]
    if only:
        print("filter           : families %s -> %d mutations\n" % (",".join(only), len(todo)))

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in todo:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print("  SURVIVED  [%s] %s" % (family, label))
        else:
            caught += 1; fam[family][0] += 1
            print("  caught    [%s] %s" % (family, label))
        sys.stdout.flush()

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print("  %-11s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(todo)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
