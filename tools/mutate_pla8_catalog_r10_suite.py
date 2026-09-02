#!/usr/bin/env python3
"""Mutation harness for the r10 catalog promote (PLA-215).

Families: `shape` attacks the widening's declaration checks. `sourcing` attacks the T1/anchor/https/
date checks. `survive` attacks the guard that keeps the widening ADDITIVE -- 37 shipped rungs were
authored against this method's text -- including its anti-vacuity branch. `unblock` attacks the
assertion that the widening actually reaches the case it was made for. `hygiene` attacks the copy
rules. `blast` attacks the post-state set, count and bystander comparisons. `mechanics` attacks the
SHA, the serializer, and the WIRING of both guards into `main`.

The wiring mutations are here from the start rather than after a survivor pointed at them: r8's
harness proved a suite can drive every branch of `check` and still not prove `main` calls it.

WITHDRAWN, not missing: the method-COUNT check in verify_post is a FORWARD assertion. The set
comparison above it fires first for any addition or removal, so with equal sets the count is
equal by construction and no post-state mutation can reach it; what it guards is BASE DRIFT.
Per the convention, a genuinely unreachable forward assertion is documented and withdrawn
rather than left reported as a permanent survivor.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r10.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r10.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r10_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- shape ----------------------------------------------------------------------------------
    ("shape: the widening count is not pinned", "shape", PROMOTE,
     "    if len(C.WIDENINGS) != EXPECTED_WIDENINGS:", "    if False:"),
    ("shape: widening an absent method is accepted", "shape", PROMOTE,
     "        if key not in cm:\n            return f\"{key} is not in the catalog, so it cannot be widened\"",
     "        if False:\n            return f\"{key} is not in the catalog, so it cannot be widened\""),
    ("shape: a target outside the vocabulary is accepted", "shape", PROMOTE,
     "            if t not in vocab:", "            if False:"),
    ("shape: re-adding an existing target is accepted", "shape", PROMOTE,
     '            if t in m["applies_to"]:', "            if False:"),

    # ---- newsource ------------------------------------------------------------------------------
    # r9 had ONE branch here ("this round adds none"). r10 adds one, so the refusal became a
    # validation and every clause of it needs its own driver.
    ("newsource: the new-source COUNT is not pinned", "newsource", PROMOTE,
     "    if len(C.NEW_SOURCES) != EXPECTED_NEW_SOURCES:", "    if False:"),
    ("newsource: overwriting an existing source_catalog id is accepted", "newsource", PROMOTE,
     "        if sid in sc:", "        if False:"),
    ("newsource: a non-T1 new source is accepted", "newsource", PROMOTE,
     '        if (entry.get("tier") or "").upper() != "T1":\n            return f"new source {sid!r} is not T1"',
     '        if False:\n            return f"new source {sid!r} is not T1"'),
    ("newsource: a non-https new source is accepted", "newsource", PROMOTE,
     '        if not u.startswith("https://"):', "        if False:"),
    ("newsource: a BARE HOST citation is accepted", "newsource", PROMOTE,
     '        if len(u.split("://", 1)[1].strip("/").split("/")) < 2:', "        if False:"),
    ("newsource: a new source with no citable_for is accepted", "newsource", PROMOTE,
     '        if not entry.get("citable_for"):', "        if False:"),
    ("newsource: a TITLELESS minted id reaches the gauntlet (the 121/121 defect)", "newsource",
     PROMOTE, "    if tv:", "    if False:"),

    # ---- sourcing -------------------------------------------------------------------------------
    ("sourcing: a source that exists nowhere is accepted", "sourcing", PROMOTE,
     "            if entry is None:", "            if False:"),
    ("sourcing: a non-T1 cited source is accepted", "sourcing", PROMOTE,
     '            if (entry.get("tier") or "").upper() != "T1":', "            if False:"),
    ("sourcing: a source with no anchor is accepted", "sourcing", PROMOTE,
     '            if s not in w["add_anchors"]:', "            if False:"),
    ("sourcing: an anchor for an undeclared source is accepted", "sourcing", PROMOTE,
     '            if s not in w["add_sources"]:', "            if False:"),
    ("sourcing: a non-https anchor is accepted", "sourcing", PROMOTE,
     '            if not str(a.get("url", "")).startswith("https://"):', "            if False:"),
    ("sourcing: an undated anchor is accepted", "sourcing", PROMOTE,
     '            if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", str(a.get("verified", ""))):',
     "            if False:"),

    # ---- survive --------------------------------------------------------------------------------
    ("survive: the widening may drop an existing claim (check)", "survive", PROMOTE,
     "            if f.lower() not in blob:", "            if False:"),
    ("survive: the anti-vacuity check on MUST_SURVIVE is disabled", "survive", PROMOTE,
     "            if f.lower() not in old:", "            if False:"),
    ("survive: MUST_SURVIVE may name an unwidened method", "survive", PROMOTE,
     "        if w is None:", "        if False:"),
    ("survive: the widening may drop an existing claim (post)", "survive", PROMOTE,
     '            if f.lower() not in " ".join(prose_of(after)).lower():', "            if False:"),
    ("survive: applies_to may LOSE a target", "survive", PROMOTE,
     "        if lost:", "        if False:"),
    ("survive: applies_to may gain an undeclared target", "survive", PROMOTE,
     '        if gained != list(w["add_targets"]):', "        if False:"),
    ("survive: a source may be dropped", "survive", PROMOTE,
     '            if s not in after["sources"]:', "            if False:"),
    ("survive: the MUST_SURVIVE table is emptied in the CONTENT", "survive", CONTENT,
     '        "tested or treated seed",', ""),

    # ---- catalog --------------------------------------------------------------------------------
    # The guard shape r9 did NOT need, because r9 added no source.
    ("catalog: source_catalog may DROP an entry", "catalog", PROMOTE,
     "    if dropped:", "    if False:"),
    ("catalog: source_catalog may gain an UNDECLARED id", "catalog", PROMOTE,
     "    if added != sorted(C.NEW_SOURCES):", "    if False:"),
    ("catalog: an EXISTING source_catalog entry may be modified", "catalog", PROMOTE,
     "        if post[\"sources\"][k] != pre[\"sources\"][k]:", "        if False:"),
    ("catalog: a crop may change", "catalog", PROMOTE,
     '    if post["crops"] != pre["crops"]:', "    if False:"),
    ("catalog: the method SET may change", "catalog", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', "    if False:"),
    ("catalog: a method other than the declared one may change", "catalog", PROMOTE,
     "    if changed != sorted(C.WIDENINGS):", "    if False:"),

    # ---- unblock --------------------------------------------------------------------------------
    ("unblock: a no-op widening is accepted", "unblock", PROMOTE,
     '        if not targets & set(cm[key]["applies_to"]):', "        if False:"),
    ("unblock: a missing unblock crop is accepted", "unblock", PROMOTE,
     "        if crop is None:", "        if False:"),
    ("unblock: a missing unblock problem is accepted", "unblock", PROMOTE,
     "        if prob is None:", "        if False:"),
    ("unblock: the unblock check never runs inside verify_post", "unblock", PROMOTE,
     "    problem = unblocks_its_case(cm)\n    if problem:\n        return \"post: \" + problem",
     "    problem = None\n    if problem:\n        return \"post: \" + problem"),

    # ---- hygiene --------------------------------------------------------------------------------
    ("hygiene: the copy check on new prose is disabled", "hygiene", PROMOTE,
     "                bad = hygiene(s)", "                bad = None"),
    ("hygiene: the list-valued fields are never flattened", "hygiene", PROMOTE,
     "            for s in (v if isinstance(v, list) else [v]):",
     "            for s in ([] if isinstance(v, list) else [v]):"),
    ("hygiene: the anti-vacuity branch is removed", "hygiene", PROMOTE,
     "        if checked == 0:", "        if False:"),
    ("hygiene: absolutes are allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     "    if False:"),
    ("hygiene: a bare F is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\d+\\s*F\\b", s):', "    if False:"),
    ("hygiene: markdown emphasis is allowed", "hygiene", PROMOTE,
     '    if "**" in s or "__" in s:', "    if False:"),
    ("hygiene: a double hyphen is allowed", "hygiene", PROMOTE,
     '    if "--" in s:', "    if False:"),
    ("hygiene: an em dash is allowed", "hygiene", PROMOTE,
     '    if re.search(r"[\u2014\u2013]", s):', "    if False:"),
    ("hygiene: a spaced degF is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\s\u00b0F", s):', "    if False:"),
    ("hygiene: British spelling is allowed", "hygiene", PROMOTE,
     '        if re.search(rf"\\b{w}\\b", s, re.I):', "        if False:"),
    ("hygiene: a bare safety claim is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:is|are)\\s+safe\\b", s, re.I):', "    if False:"),
    ("hygiene: capital Plant mid-sentence is allowed", "hygiene", PROMOTE,
     '    if re.search(r"(?<![.!?]\\s)(?<!^)\\bPlant\\b(?! Pro)", s):', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the base SHA refusal is removed", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: check() is cut out of main", "mechanics", PROMOTE,
     "    problem = check(data)\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)",
     "    problem = None\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)"),
    ("mechanics: serialize stops being compact", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: the target is never actually added", CONTENT,
            '            m["applies_to"] = list(m["applies_to"]) + [t]',
            '            _skip = list(m["applies_to"]) + [t]')


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS] + [(SENTINEL[0], SENTINEL[1], SENTINEL[2])]
    for label, f, old in rows:
        n = open(f).read().count(old)
        if n != 1:
            bad.append("  %dx  %s\n        anchor: %r" % (n, label, old[:76]))
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print("preflight        : all %d anchors match exactly once" % len(rows))
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_cat_r9_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        'REPO = %r\nsys.path.insert(0, %r)\n'
        'sys.path.insert(1, os.path.join(REPO, "tools"))' % (REPO, wd))
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent for %s" % os.path.basename(path))
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 catalog round 10 (certified_clean_stock: widen + generalize)")
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

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print("  SURVIVED  [%s] %s" % (family, label))
        else:
            caught += 1; fam[family][0] += 1
            print("  caught    [%s] %s" % (family, label))

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print("  %-10s %d caught / %d" % (k, c, c + s) + ("" if not s else "   <-- %d SURVIVED" % s))
    print("-" * 78)
    print("TOTAL: %d caught, %d survived, of %d injected" % (caught, survived, len(MUTATIONS)))
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
