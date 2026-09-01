#!/usr/bin/env python3
"""Mutation harness for the r8 catalog promote (PLA-215).

Families: `shape` attacks the per-mint field, tier and vocabulary checks. `counts` attacks the two
assertions that keep an EMPTY `NEW_SOURCES` from hollowing out the source-mint block. `sourcing`
attacks the T1/anchor/https/date checks. `hedges` attacks the qualifiers the prose must keep.
`opposed` attacks the guard against the live `raise_soil_ph` hazard, including its vacuity branch
and the ORDERING that lets it fire at all. `hygiene` attacks the copy rules. `blast` attacks the
post-state set-equality and bystander comparisons. `mechanics` attacks the SHA and the serializer.

Every disabled branch has a driver asserting its ONE specific message, and every anti-vacuity
branch is injected individually rather than assumed covered by its guard's main path.

Includes the anchor PREFLIGHT, a positive control, and a SENTINEL that must redden.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_r8.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_r8.py")
CONTENT = os.path.join(HERE, "build_pla8_catalog_r8_content.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- counts ---------------------------------------------------------------------------------
    ("counts: the mint count is not pinned", "counts", PROMOTE,
     "    if len(C.MINTS) != EXPECTED_MINTS:", "    if False:"),
    ("counts: an undeclared source mint is accepted", "counts", PROMOTE,
     "    if len(C.NEW_SOURCES) != EXPECTED_NEW_SOURCES:", "    if False:"),

    # ---- shape ----------------------------------------------------------------------------------
    ("shape: a key already in the catalog is accepted", "shape", PROMOTE,
     "        if key in cm:\n            return f\"{key} is already in the catalog\"",
     "        if False:\n            return f\"{key} is already in the catalog\""),
    ("shape: a missing required field is accepted", "shape", PROMOTE,
     "            if f not in m or not m[f]:", "            if False:"),
    ("shape: an unknown tier is accepted", "shape", PROMOTE,
     '        if m["tier"] not in TIERS:', "        if False:"),
    ("shape: applies_to outside the gate vocabulary is accepted", "shape", PROMOTE,
     '        bad = [t for t in m["applies_to"] if t not in vocab]', "        bad = []"),

    # ---- sourcing -------------------------------------------------------------------------------
    ("sourcing: an unknown source is accepted", "sourcing", PROMOTE,
     "        if s not in known:", "        if False:"),
    ("sourcing: a non-T1 source is accepted", "sourcing", PROMOTE,
     '        if (known[s].get("tier") or "").upper() != "T1":', "        if False:"),
    ("sourcing: a source with no anchor is accepted", "sourcing", PROMOTE,
     '        if s not in m["anchoring_urls"]:', "        if False:"),
    ("sourcing: an anchor for an undeclared source is accepted", "sourcing", PROMOTE,
     '        if s not in m["sources"]:', "        if False:"),
    ("sourcing: a non-https anchor is accepted", "sourcing", PROMOTE,
     '        if not str(a.get("url", "")).startswith("https://"):', "        if False:"),
    ("sourcing: an undated anchor is accepted", "sourcing", PROMOTE,
     '        if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", str(a.get("verified", ""))):',
     "        if False:"),

    # ---- hedges ---------------------------------------------------------------------------------
    ("hedges: a dropped source qualifier is accepted", "hedges", PROMOTE,
     "            if h.lower() not in blob:", "            if False:"),
    ("hedges: a hedge naming an unminted method is accepted", "hedges", PROMOTE,
     "        if key not in C.MINTS:", "        if False:"),
    ("hedges: the crop-specific qualifier is dropped from the content", "hedges", CONTENT,
     '    "cure_and_store": ("crop-specific", "chilling injury"),',
     '    "cure_and_store": (),'),

    # ---- opposed --------------------------------------------------------------------------------
    ("opposed: a missing pair member is accepted", "opposed", PROMOTE,
     "        if k not in cm:", "        if False:"),
    ("opposed: the vacuity check on an empty applies_to is disabled", "opposed", PROMOTE,
     "    if not a or not b:", "    if False:"),
    ("opposed: a SHARED target between the two is accepted", "opposed", PROMOTE,
     "    if shared:", "    if False:"),
    ("opposed: losing the prose cross-reference is accepted", "opposed", PROMOTE,
     '    if "opposite" not in blob:', "    if False:"),
    ("opposed: the pair check never runs inside verify_post", "opposed", PROMOTE,
     "    problem = opposed_pair_holds(cm)\n    if problem:\n        return \"post: \" + problem",
     "    problem = None\n    if problem:\n        return \"post: \" + problem"),
    ("opposed: the pair is widened in the CONTENT itself", "opposed", CONTENT,
     '        "applies_to": ["bacterial"],',
     '        "applies_to": ["bacterial", "fungal_soilborne"],'),

    # ---- hygiene --------------------------------------------------------------------------------
    ("hygiene: the whole copy check is disabled", "hygiene", PROMOTE,
     "            bad = hygiene(s)", "            bad = None"),
    ("hygiene: absolutes are allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\\b", s, re.I):',
     "    if False:"),
    ("hygiene: a bare F without a degree sign is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\d+\\s*F\\b", s):', "    if False:"),
    ("hygiene: markdown emphasis is allowed", "hygiene", PROMOTE,
     '    if "**" in s or "__" in s:', "    if False:"),
    ("hygiene: a spaced degF is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\s°F", s):', "    if False:"),
    ("hygiene: a double hyphen is allowed", "hygiene", PROMOTE,
     '    if "--" in s:', "    if False:"),
    ("hygiene: an em dash is allowed", "hygiene", PROMOTE,
     '    if re.search(r"[—–]", s):', "    if False:"),
    ("hygiene: a bare safety claim is allowed", "hygiene", PROMOTE,
     '    if re.search(r"\\b(?:is|are)\\s+safe\\b", s, re.I):', "    if False:"),
    ("hygiene: British spellings are allowed", "hygiene", PROMOTE,
     "    for w in BRITISH:", "    for w in ():"),
    ("hygiene: prose_of skips the list fields", "hygiene", PROMOTE,
     "        out.extend(v if isinstance(v, list) else [v])",
     "        out.extend([] if isinstance(v, list) else [v])"),

    # ---- blast ----------------------------------------------------------------------------------
    ("blast: methods added need not equal the mints", "blast", PROMOTE,
     "    if added_m != set(C.MINTS):", "    if False:"),
    ("blast: a dropped method is accepted", "blast", PROMOTE,
     '    if set(pre["methods"]) - set(post["methods"]):', "    if False:"),
    ("blast: sources added need not equal NEW_SOURCES", "blast", PROMOTE,
     "    if added_s != set(C.NEW_SOURCES):", "    if False:"),
    ("blast: a dropped source is accepted", "blast", PROMOTE,
     '    if set(pre["sources"]) - set(post["sources"]):', "    if False:"),
    ("blast: an existing method may change", "blast", PROMOTE,
     '        if post["methods"][k] != before:', "        if False:"),
    ("blast: an existing source may change", "blast", PROMOTE,
     '        if post["sources"][k] != before:', "        if False:"),
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

SENTINEL = ("SENTINEL: the mints are never written into the catalog", CONTENT,
            "    for key, method in MINTS.items():\n        cm[key] = dict(method)",
            "    for key, method in MINTS.items():\n        _skip = dict(method)")


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
    """Copy the suite, the promote and the content module into a sandbox, apply one mutation, and
    force the suite to import the sandboxed copies rather than the repo's."""
    wd = tempfile.mkdtemp(prefix="mutate_cat_r8_")
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
    print("MUTATION HARNESS -- PLA-8 catalog round 8")
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
