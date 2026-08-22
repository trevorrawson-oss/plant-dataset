#!/usr/bin/env python3
"""Mutation harness for the PLA-8 Round 2 promote suite (PLA-215 convention).

WHY. `test_promote_pla8_variety_ladder_delta.py` is REPLAY-PINNED: pre is rebuilt from the base and
post is the promote's own output, so it is green from birth and "32 tests pass" is not by itself
evidence of anything. This harness is the evidence. It corrupts the STAGED CONTENT and the PROMOTE
one family at a time and requires the suite to notice.

LIVENESS DEFENSE (all three mandatory -- PLA-138's harness silently graded a CLEAN fixture and
reported every mutation as surviving):
  1. MUTATION-APPLIED marker: the staged file about to be graded is read back and asserted changed.
  2. SENTINEL: a mutation that guts the promote MUST redden, else the run exits HARNESS DEAD.
  3. POSITIVE CONTROL: the unmutated pair must pass, or every verdict below is meaningless.

Usage: python3 tools/mutate_pla8_ladder_delta_suite.py
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_variety_ladder_delta.py")
PROMOTE = os.path.join(HERE, "promote_pla8_variety_ladder_delta.py")
CONTENT = os.path.join(HERE, "staging", "pla8_ladder_delta_content.json")


# ---- content mutations: each corrupts the STAGED JSON in one specific way -------------------
def m_add_variety(c):
    """A 23rd variety appears. The PLA-162 blind spot: additions are invisible to a pre-only walk."""
    c["apple"]["ghost-apple"] = copy.deepcopy(c["apple"]["liberty"])


def m_drop_variety(c):
    del c["apple"]["dolgo"]


def m_add_rung(c):
    c["apple"]["liberty"]["apple-scab"]["rungs"].append(
        {"method": "garden_sanitation", "op": "replace", "note_beginner": "z" * 80})


def m_byte_equal_note(c):
    """The headline defect the whole delta exists to prevent: a note copied from its parent."""
    c["apple"]["gala"]["apple-scab"]["rungs"][0]["note_beginner"] = (
        "The surest fix is to plant a scab-resistant apple like Liberty, so you rarely have to "
        "spray at all.")


def m_register_collapse(c):
    r = c["apple"]["liberty"]["apple-scab"]["rungs"][0]
    r["note_seasoned"] = r["note_beginner"]


def m_em_dash(c):
    r = c["apple"]["gala"]["apple-scab"]["rungs"][0]
    r["note_beginner"] = r["note_beginner"].replace(":", " —")


def m_british(c):
    r = c["apple"]["gala"]["apple-scab"]["rungs"][0]
    r["note_beginner"] += " Use sulphur only as a last resort."


def m_absolute(c):
    r = c["apple"]["liberty"]["apple-scab"]["rungs"][0]
    r["note_beginner"] += " It is completely harmless to bees."


def m_overclaim_immune(c):
    r = c["apple"]["liberty"]["apple-scab"]["rungs"][0]
    r["note_beginner"] = "Already done. Liberty cannot catch it at all, so skip this."


def m_strip_hedge(c):
    """Purdue's caution compressed away -- the defect with no term to scan for."""
    for pid in ("apple-scab", "cedar-apple-rust", "powdery-mildew"):
        for r in c["apple"]["dolgo"][pid]["rungs"]:
            if r["method"] == "resistant_varieties":
                r["note_seasoned"] = r["note_seasoned"].split("Resistance is not immunity")[0]


def m_drop_carries_note(c):
    for r in c["apple"]["liberty"]["apple-scab"]["rungs"]:
        if r["op"] == "drop":
            r["note_beginner"] = "should not be here"


def m_dangling_method(c):
    c["apple"]["liberty"]["apple-scab"]["rungs"][0]["method"] = "bird_netting"


def m_unladdered_problem(c):
    c["apple"]["liberty"]["not-a-disease"] = copy.deepcopy(
        c["apple"]["liberty"]["apple-scab"])


def m_stubby_note(c):
    c["apple"]["gala"]["apple-scab"]["rungs"][0]["note_beginner"] = "Skip it."


CONTENT_MUTATIONS = [
    ("content: a 23rd variety is appended", "scope", m_add_variety),
    ("content: a targeted variety is removed", "scope", m_drop_variety),
    ("content: an extra rung operation appears", "counts", m_add_rung),
    ("content: a note is byte-equal to its parent rung", "duplication", m_byte_equal_note),
    ("content: beginner and seasoned collapse to one string", "register", m_register_collapse),
    ("content: an em dash enters consumer copy", "mechanics", m_em_dash),
    ("content: a British spelling enters consumer copy", "mechanics", m_british),
    ("content: an absolute claim enters consumer copy", "mechanics", m_absolute),
    ("content: immune wording outruns its source", "mechanics", m_overclaim_immune),
    ("content: Purdue's hedge is compressed away", "hedge", m_strip_hedge),
    ("content: a drop carries a note_ instead of a why_", "shape", m_drop_carries_note),
    ("content: a rung targets a method not in the parent", "referential", m_dangling_method),
    ("content: a delta targets an unladdered problem id", "referential", m_unladdered_problem),
    ("content: a note is reduced to a stub", "register", m_stubby_note),
]

# ---- promote mutations: corrupt the SCRIPT, not the data -----------------------------------
PROMOTE_MUTATIONS = [
    ("promote: parent-ladder membership check disabled", "referential",
     'if r.get("op") in ("drop", "replace") and r.get("method") not in parent:', "if False:"),
    ("promote: already-exists refusal disabled", "refusal",
     f'if DELTA_KEY in varieties[vid]:', "if False:"),
    ("promote: scope check disabled", "refusal",
     "if slug not in CROPS:", "if False:"),
    ("promote: resistance-grade backing check disabled", "referential",
     "if pid not in grades:", "if False:"),
    ("promote: output is no longer COMPACT", "mechanics",
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", "def apply_to(data, content):",
            "def apply_to(data, content):\n    return 0")


def run_suite(workdir):
    r = subprocess.run([sys.executable, os.path.join(workdir, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout + r.stderr)[-400:]


def stage(content_fn=None, promote_sub=None):
    wd = tempfile.mkdtemp(prefix="mutate_pla8_")
    # The staged suite must resolve `promote_fixture` from the REAL tools dir while importing the
    # MUTATED promote from this temp dir. Its own `sys.path.insert(0, REPO/tools)` computes REPO
    # from __file__, which is wrong in a temp dir, and would shadow the mutation if left to point
    # at the real tools. So the path setup is rewritten explicitly: real tools for the shared
    # helpers, temp dir AHEAD of it for the module under mutation.
    suite_src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\n'
        f'sys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(suite_src)
    # content
    orig_raw = open(CONTENT, "rb").read()
    if content_fn:
        c = json.loads(orig_raw.decode())
        content_fn(c)
        new_raw = json.dumps(c, ensure_ascii=False, indent=1).encode()
        if new_raw == orig_raw:
            raise SystemExit("HARNESS DEAD: content mutation produced an identical file")
        cpath = os.path.join(wd, "content.json")
        open(cpath, "wb").write(new_raw)
    else:
        cpath = CONTENT
    # promote
    src = open(PROMOTE).read()
    if promote_sub:
        old, new = promote_sub
        if src.count(old) != 1:
            raise SystemExit(f"HARNESS DEAD: anchor not unique ({src.count(old)}x): {old[:60]!r}")
        src = src.replace(old, new + "  # MUTATION-APPLIED", 1)
    # the suite pins the content SHA, so a content mutation must also repoint the promote at it
    # and relax that pin -- otherwise EVERY content mutation is caught by the SHA guard alone,
    # which would prove nothing about the other 30 tests.
    src = src.replace(f'CONTENT = os.path.join(REPO, "tools", "staging", '
                      f'"pla8_ladder_delta_content.json")',
                      f'CONTENT = {cpath!r}')
    if content_fn:
        src = src.replace(f'CONTENT_SHA = "{_orig_sha()}"', 'CONTENT_SHA = None')
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(src)
    # liveness defense 1
    back = open(os.path.join(wd, os.path.basename(PROMOTE))).read()
    if promote_sub and "# MUTATION-APPLIED" not in back:
        raise SystemExit("HARNESS DEAD: MUTATION-APPLIED marker absent from staged promote")
    return wd


def _orig_sha():
    import hashlib
    return hashlib.sha256(open(CONTENT, "rb").read()).hexdigest()


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 Round 2 promote suite")
    print("=" * 78)

    wd = stage()
    ok, out = run_suite(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails.\n" + out)
        return 1
    print("positive control : GREEN\n")

    label, old, new = SENTINEL
    wd = stage(promote_sub=(old, new))
    ok, _ = run_suite(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED.")
        return 1
    print(f"sentinel         : RED as required ({label})\n")

    caught = survived = 0
    fam = {}
    for label, family, fn in CONTENT_MUTATIONS:
        wd = stage(content_fn=fn)
        ok, out = run_suite(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")
    for label, family, old, new in PROMOTE_MUTATIONS:
        wd = stage(promote_sub=(old, new))
        ok, out = run_suite(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for f in sorted(fam):
        c, s = fam[f]
        print(f"  {f:12s} {c} caught / {c + s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    total = len(CONTENT_MUTATIONS) + len(PROMOTE_MUTATIONS)
    print(f"TOTAL: {caught} caught, {survived} survived, of {total} injected")
    if survived:
        print("\nRESULT: FAIL -- a guard family is unreachable or its test is vacuous.")
        return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
