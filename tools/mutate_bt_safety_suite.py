#!/usr/bin/env python3
"""Mutation harness for the Bt safety-absolute sweep (PLA-215).

THE `safety` FAMILY ATTACKS A THREE-PART SPECIFICATION, and the third part is the one this sweep
exists for. The original sentence was wrong twice: "which is SAFE" (unhedged) and "targets ONLY
caterpillars" (literally true, consumer-misleading, because the non-target risk IS other
caterpillars). A promote that fixes only the first half passes a naive guard while leaving the
reader believing Bt hits nothing they care about. So there are separate mutations for reverting the
absolute, for dropping the qualified toxicity claim, and for dropping the butterfly caveat -- and
one that deletes the sentence outright, which is what "absence of the banned phrase" alone would
happily accept.

THE `scope` FAMILY guards the opposite failure, and both of its mutations do something a careless
sweep would plausibly do: rewrite the four corn crops whose "only" is a correctly-stated EFFICACY
limitation, and sweep in the out-of-scope "spare beneficials" claim.

Includes the anchor PREFLIGHT: every anchor validated to match exactly once before grading.
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_bt_safety.py")
PROMOTE = os.path.join(HERE, "promote_bt_safety.py")
CONTENT = os.path.join(HERE, "build_bt_safety_content.py")
MARKER = "# MUTATION-APPLIED"

CONTENT_FN = "    import build_bt_safety_content as B\n    return B"
APPLY_HEAD = "    B = content()\n    n = 0"

MUTATIONS = [
    # ---- safety: the absolute comes back ---------------------------------------------------
    ("safety: kale reverts to 'which is safe'", "safety", CONTENT,
     '        "Spray a product called Bt, which is low in toxicity to people, pets and bees and acts on "\n'
     '        "caterpillars rather than on insects in general. It cannot tell a pest caterpillar from a "\n'
     '        "butterfly one, so treat only the plants that have a problem. Or pick the caterpillars and "\n'
     '        "eggs off by hand from under the leaves. Spray again after rain, since it washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "collards",',
     '        "Spray a product called Bt, which is safe and targets only caterpillars. Or pick the "\n'
     '        "caterpillars and eggs off by hand from under the leaves. Spray again after rain, since it "\n'
     '        "washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "collards",'),
    # ---- safety: the qualified toxicity claim is hollowed out --------------------------------
    ("safety: spinach drops the qualified toxicity claim", "safety", CONTENT,
     '        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "\n'
     '        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "\n'
     '        "so treat only the plants that have a problem. Or pick them off by hand. Spray again after "\n'
     '        "rain since it washes off.",',
     '        "Spray Bt, which acts on caterpillars rather than on insects in general. It cannot tell a "\n'
     '        "pest caterpillar from a butterfly one, so treat only the plants that have a problem. Or "\n'
     '        "pick them off by hand. Spray again after rain since it washes off.",'),
    # ---- safety: the NON-TARGET caveat is dropped, the half that matters ---------------------
    # NOTE: the first version of this mutation disabled the REFUSAL in check() and SURVIVED, which
    # was a badly-designed mutation rather than a guard gap: with the data still carrying the
    # caveat, removing a refusal changes no output. The mutation now removes the caveat FROM THE
    # DATA, which is the condition the guards actually exist to catch.
    ("safety: the butterfly caveat is dropped from spinach's replacement", "safety", CONTENT,
     '        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "\n'
     '        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "\n'
     '        "so treat only the plants that have a problem. Or pick them off by hand. Spray again after "\n'
     '        "rain since it washes off.",',
     '        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "\n'
     '        "rather than on insects in general. Or pick them off by hand. Spray again after "\n'
     '        "rain since it washes off.",'),
    ("safety: REQUIRED_NONTARGET is weakened to match anything", "safety", CONTENT,
     'REQUIRED_NONTARGET = r"butterfly"',
     'REQUIRED_NONTARGET = r""'),
    # ---- safety: the sentence is deleted rather than fixed ------------------------------------
    ("safety: the claim is deleted instead of corrected", "safety", CONTENT,
     '        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "\n'
     '        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "\n'
     '        "so treat only the plants that have a problem. Or pick them and their eggs off by hand from "\n'
     '        "the undersides of leaves. Spray again after rain, since it washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "bok-choy",',
     '        "Pick them and their eggs off by hand from the undersides of leaves. Spray again after "\n'
     '        "rain, since it washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "bok-choy",'),
    # ---- coverage ----------------------------------------------------------------------------
    ("coverage: only the first two crops are swept", "coverage", PROMOTE,
     CONTENT_FN,
     '    import build_bt_safety_content as B\n'
     '    class _B:\n'
     '        EDITS = B.EDITS[:2]\n'
     '        BANNED = B.BANNED; SCOPE = B.SCOPE\n'
     '        REQUIRED_QUALIFIER = B.REQUIRED_QUALIFIER; REQUIRED_NONTARGET = B.REQUIRED_NONTARGET\n'
     '        CORN_EFFICACY_ONLY = B.CORN_EFFICACY_ONLY; ALREADY_CORRECT = B.ALREADY_CORRECT\n'
     '        SOURCE_READ = B.SOURCE_READ; NOT_FIXED = B.NOT_FIXED\n'
     '    return _B'),
    ("coverage: kohlrabi, the odd wording, is dropped", "coverage", PROMOTE,
     CONTENT_FN,
     '    import build_bt_safety_content as B\n'
     '    class _B:\n'
     '        EDITS = [e for e in B.EDITS if e[0] != "kohlrabi"]\n'
     '        BANNED = B.BANNED; SCOPE = B.SCOPE\n'
     '        REQUIRED_QUALIFIER = B.REQUIRED_QUALIFIER; REQUIRED_NONTARGET = B.REQUIRED_NONTARGET\n'
     '        CORN_EFFICACY_ONLY = B.CORN_EFFICACY_ONLY; ALREADY_CORRECT = B.ALREADY_CORRECT\n'
     '        SOURCE_READ = B.SOURCE_READ; NOT_FIXED = B.NOT_FIXED\n'
     '    return _B'),
    # ---- scope: things a careless sweep would wrongly touch -----------------------------------
    ("scope: the corn efficacy 'only' is rewritten as if it were the class", "scope", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _c in data["crops"]:\n'
     '        if _c.get("slug") in B.CORN_EFFICACY_ONLY:\n'
     '            for _f in ("pests", "diseases"):\n'
     '                for _p in _c.get(_f) or []:\n'
     '                    for _k, _v in list(_p.items()):\n'
     '                        if isinstance(_v, str) and "only works while" in _v:\n'
     '                            _p[_k] = _v.replace("only works while", "works while")'),
    ("scope: the out-of-scope 'spare beneficials' claim is swept in", "scope", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _c in data["crops"]:\n'
     '        for _f in ("pests", "diseases"):\n'
     '            for _p in _c.get(_f) or []:\n'
     '                if not isinstance(_p, dict):\n'
     '                    continue\n'
     '                for _k, _v in list(_p.items()):\n'
     '                    if isinstance(_v, str) and "spare beneficials" in _v:\n'
     '                        _p[_k] = _v.replace("spare beneficials", "are selective")'),
    ("scope: a crop that already had it right is rewritten anyway", "scope", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _c in data["crops"]:\n'
     '        if _c.get("slug") == "dill":\n'
     '            for _f in ("pests", "diseases"):\n'
     '                for _p in _c.get(_f) or []:\n'
     '                    for _k, _v in list(_p.items()):\n'
     '                        if isinstance(_v, str) and "butterflies" in _v:\n'
     '                            _p[_k] = _v.replace("butterflies", "moths")'),
    # ---- blast radius --------------------------------------------------------------------------
    ("blast: a control_method is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n    data["control_methods"]["bt"]["applies_to"].append("viral")'),
    ("blast: a ladder is edited", "blast", PROMOTE,
     APPLY_HEAD,
     APPLY_HEAD + '\n'
     '    for _c in data["crops"]:\n'
     '        for _f in ("pests", "diseases"):\n'
     '            for _p in _c.get(_f) or []:\n'
     '                if isinstance(_p, dict) and _p.get("control_ladder"):\n'
     '                    _p["control_ladder"] = _p["control_ladder"][:-1]'),
    # ---- mechanics ------------------------------------------------------------------------------
    ("mechanics: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("mechanics: the reapplication advice is lost in a rewrite", "mechanics", CONTENT,
     '        "off by hand from under the leaves. Spray again after rain.",\n'
     '    ),\n'
     ']',
     '        "off by hand from under the leaves.",\n'
     '    ),\n'
     ']'),
    ("mechanics: an em dash enters consumer copy", "mechanics", CONTENT,
     '        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "\n'
     '        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "\n'
     '        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "\n'
     '        "off by hand from under the leaves. Spray again after rain, since it washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "cabbage",',
     '        "Spray Bt — low in toxicity to people, pets and bees — which acts on caterpillars "\n'
     '        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "\n'
     '        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "\n'
     '        "off by hand from under the leaves. Spray again after rain, since it washes off.",\n'
     '    ),\n'
     '    (\n'
     '        "cabbage",'),
    # ---- the source record -----------------------------------------------------------------------
    ("record: the source read is rewritten to support the absolute", "record", CONTENT,
     '        "Bt is low in toxicity to people and other mammals when eaten",',
     '        "Bt is safe for people and other mammals when eaten",'),
    ("record: the non-target moth finding is dropped from the record", "record", CONTENT,
     '        "a few studies also found that non-target moths were harmed",',
     '        "no effects on non-target insects were reported",'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            "def apply_to(data):", "def apply_to(data):\n    return 0")


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0


def preflight():
    bad = []
    rows = [(m[0], m[2], m[3]) for m in MUTATIONS]
    rows.append((SENTINEL[0], SENTINEL[1], SENTINEL[2]))
    for label, f, old in rows:
        n = open(f).read().count(old)
        if n != 1:
            bad.append(f"  {n}x  [{os.path.basename(f)}] {label}\n        anchor: {old[:76]!r}")
    if bad:
        print("HARNESS DEAD -- anchors do not match exactly once:\n" + "\n".join(bad))
        return False
    print(f"preflight        : all {len(rows)} anchors match exactly once")
    return True


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_bt_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            s = s.replace(old, (new + "  " + MARKER) if new else MARKER, 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path and MARKER not in open(os.path.join(wd, os.path.basename(path))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: marker absent")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- Bt safety absolute, crop prose")
    print("=" * 78)
    if not preflight():
        return 1

    wd = stage(); ok = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails -- the clean suite is not green.")
        return 1
    print("positive control : GREEN")

    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED -- the harness is not running the mutated code.")
        return 1
    print("sentinel         : RED as required\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print(f"  {k:10s} {c} caught / {c+s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
