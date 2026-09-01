#!/usr/bin/env python3
"""Mutation harness for the r9 catalog promote (PLA-215).

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
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r9.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r9.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r9_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- shape ----------------------------------------------------------------------------------
    ("shape: the widening count is not pinned", "shape", PROMOTE,
     "    if len(C.WIDENINGS) != EXPECTED_WIDENINGS:", "    if False:"),
    ("shape: an undeclared source mint is accepted", "shape", PROMOTE,
     "    if C.NEW_SOURCES:", "    if False:"),
    ("shape: widening an absent method is accepted", "shape", PROMOTE,
     "        if key not in cm:\n            return f\"{key} is not in the catalog, so it cannot be widened\"",
     "        if False:\n            return f\"{key} is not in the catalog, so it cannot be widened\""),
    ("shape: a target outside the vocabulary is accepted", "shape", PROMOTE,
     "            if t not in vocab:", "            if False:"),
    ("shape: re-adding an existing target is accepted", "shape", PROMOTE,
     '            if t in m["applies_to"]:', "            if False:"),

    # ---- sourcing -------------------------------------------------------------------------------
    ("sourcing: an unknown source is accepted", "sourcing", PROMOTE,
     "            if s not in sc:", "            if False:"),
    ("sourcing: a non-T1 source is accepted", "sourcing", PROMOTE,
     '            if (sc[s].get("tier") or "").upper() != "T1":', "            if False:"),
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
     '        "celery blackheart",', ""),

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
     "            bad = hygiene(s)", "            bad = None"),
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
     '    if re.search(r"[—–]", s):', "    if False:"),
    ("hygiene: British spellings are allowed", "hygiene", PROMOTE,
     "    for w in BRITISH:", "    for w in ():"),
    ("hygiene: prose_of skips the list fields", "hygiene", PROMOTE,
     "        out.extend(v if isinstance(v, list) else [v])",
     "        out.extend([] if isinstance(v, list) else [v])"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: the method SET may change", "blast", PROMOTE,
     '    if set(post["methods"]) != set(pre["methods"]):', "    if False:"),
    ("blast: a SECOND method may change", "blast", PROMOTE,
     "    if changed != sorted(C.WIDENINGS):", "    if False:"),
    ("blast: source_catalog may change", "blast", PROMOTE,
     '    if post["sources"] != pre["sources"]:', "    if False:"),
    ("blast: a crop may change", "blast", PROMOTE,
     '    if post["crops"] != pre["crops"]:', "    if False:"),

    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: the base SHA is not enforced", "mechanics", PROMOTE,
     "    if sha != expect:", "    if False:"),
    ("mechanics: the serializer indents", "mechanics", PROMOTE,
     '    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     '    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: check() is never called by main", "mechanics", PROMOTE,
     "    problem = check(data)\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)",
     "    problem = None\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)"),
    ("mechanics: verify_post() is never called by main", "mechanics", PROMOTE,
     "    problem = verify_post(pre, data)\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)",
     "    problem = None\n    if problem:\n        raise SystemExit(\"REFUSED: \" + problem)"),
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
    print("MUTATION HARNESS -- PLA-8 catalog round 9 (the even_watering widening)")
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
