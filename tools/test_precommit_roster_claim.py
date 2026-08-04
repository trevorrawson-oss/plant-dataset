#!/usr/bin/env python3
"""Tests for the roster-claim arm of the pre-commit safety net. Run BOTH ways:
    python3 tools/test_precommit_roster_claim.py
    python3 -m pytest tools/test_precommit_roster_claim.py

WHY WIRE IT INTO PRE-COMMIT AT ALL: the existing net SKIPS whenever crops_data_final.json is not
staged, which is exactly the doc-only commit where a roster claim gets edited. And the mirror case
is worse: a certification promote moves the canonical while CLAUDE.md keeps its old numbers, which
is how artichoke (GS #121, 2026-07-28) stayed described as an unauthored shell for a week.

The check reads the INDEX -- the bytes actually about to be committed -- not the working tree, so
fixing CLAUDE.md without staging it does not buy a green commit.

SCOPE: it runs ONLY when the commit touches the canonical, LATEST.txt, or a gated doc. A commit
that touches none of them cannot go stale and must not be blocked. That containment is asserted
below, because a safety net that fires on unrelated commits gets bypassed by habit and then
protects nothing.

A NOTE ON TEST SHAPE (learned the hard way, twice before and once again here): the canonical-
touching cases are asserted against `roster_claim_concerns` DIRECTLY rather than through the hook.
Certifying a crop in a minimal fixture also makes it fail whole_crop_gate, so the pre-existing
regression arm blocks the commit first and an end-to-end assertion on exit code 1 would pass
whether or not this check exists at all. The end-to-end cases below are exactly the ones where the
old arm provably SKIPS (no crop staged), so a block there can only be this check.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precommit_release_verify import roster_claim_concerns

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "precommit_release_verify.py")

CLEAN_CLAUDE = ("# repo\n\n## What this is\n"
                "2 crops: 1 certified gold-standard anchors + 1 honest shells (the 1 remaining "
                "shells are the 0 mushrooms + olive). The armor is the gate suite.\n")
CLEAN_ROADMAP = "- the design/retire shells (the 0 mushrooms + olive). See memory.\n"


def _canonical(certify_olive=False):
    crops = [{"slug": "apple", "verification_status": {"status": "verified_gs_arc"}},
             {"slug": "olive"}]
    if certify_olive:
        crops[1]["verification_status"] = {"status": "verified_gs_arc"}
    return json.dumps({"crops": crops, "source_catalog": {}},
                      separators=(",", ":"), ensure_ascii=False)


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)


def _write(repo, rel, text):
    with open(os.path.join(repo, rel), "w", encoding="utf-8") as f:
        f.write(text)


def _make_repo():
    repo = tempfile.mkdtemp()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    os.makedirs(os.path.join(repo, "docs"))
    canon = _canonical()
    _write(repo, "crops_data_final.json", canon)
    _write(repo, "LATEST.txt",
           "SHA: " + hashlib.sha256(canon.encode("utf-8")).hexdigest() + "\nDate: x\n")
    _write(repo, "CLAUDE.md", CLEAN_CLAUDE)
    _write(repo, "docs/crop_expansion_roadmap.md", CLEAN_ROADMAP)
    _write(repo, "unrelated.txt", "nothing to do with the roster\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    return repo


def _concerns(repo):
    """roster_claim_concerns as the hook calls it: cwd = repo, reading the index."""
    cwd = os.getcwd()
    os.chdir(repo)
    try:
        staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                                capture_output=True, text=True).stdout.split()
        return roster_claim_concerns(staged)
    finally:
        os.chdir(cwd)


def _run_hook(repo):
    r = subprocess.run([sys.executable, HOOK], capture_output=True, text=True, cwd=repo)
    return r.returncode, r.stdout + r.stderr


repos = []
try:
    # 0. the clean base repo, nothing staged -> no concerns
    repo = _make_repo(); repos.append(repo)
    assert _concerns(repo) == [], _concerns(repo)

    # 1. THE PROMOTE CASE. Certifying a crop makes CLAUDE.md's numbers stale in the same instant.
    _write(repo, "crops_data_final.json", _canonical(certify_olive=True))
    _git(repo, "add", "crops_data_final.json")
    C = _concerns(repo)
    assert any("certified" in c for c in C), C
    assert any("olive" in c for c in C), ("olive is now certified but still listed as a shell", C)

    # 2. THE FIX. Updating the docs in the same commit clears it.
    new_canon = _canonical(certify_olive=True)
    _write(repo, "CLAUDE.md",
           "# repo\n\n## What this is\n"
           "2 crops: 2 certified gold-standard anchors + 0 honest shells (the 0 remaining "
           "shells are the 0 mushrooms + none). The armor is the gate suite.\n")
    _write(repo, "docs/crop_expansion_roadmap.md",
           "- the design/retire shells (the 0 mushrooms + none). See memory.\n")
    _write(repo, "LATEST.txt",
           "SHA: " + hashlib.sha256(new_canon.encode("utf-8")).hexdigest() + "\nDate: x\n")
    _git(repo, "add", "-A")
    assert _concerns(repo) == [], _concerns(repo)

    # 3. THE INDEX IS THE AUTHORITY. Fixing the docs in the WORKING TREE without staging them
    #    must still be a concern -- the commit would ship the stale bytes.
    #    EVERY gated doc is fixed in the working tree here, deliberately. An earlier version of
    #    this test fixed only CLAUDE.md, and the roadmap's own (still stale) claim kept the
    #    concern list non-empty, so the assertion passed whether the check read the index or the
    #    working tree. Mutation-testing caught it. With all three fixed on disk and none staged,
    #    the ONLY way to see a concern is to read the index.
    repo2 = _make_repo(); repos.append(repo2)
    canon2 = _canonical(certify_olive=True)
    _write(repo2, "crops_data_final.json", canon2)
    _git(repo2, "add", "crops_data_final.json")
    _write(repo2, "CLAUDE.md",
           "2 crops: 2 certified gold-standard anchors + 0 honest shells (the 0 remaining shells "
           "are the 0 mushrooms + none).\n")          # written but deliberately NOT staged
    _write(repo2, "docs/crop_expansion_roadmap.md",
           "- the design/retire shells (the 0 mushrooms + none).\n")            # also NOT staged
    _write(repo2, "LATEST.txt",
           "SHA: " + hashlib.sha256(canon2.encode("utf-8")).hexdigest() + "\nDate: x\n")  # ditto
    C = _concerns(repo2)
    assert any("CLAUDE.md" in c for c in C), ("an unstaged fix must not clear the concern", C)

    # 4. LATEST.txt drift alone is a concern (same class: a hand-copied derived value).
    repo5 = _make_repo(); repos.append(repo5)
    _write(repo5, "LATEST.txt", "SHA: " + "0" * 64 + "\nDate: x\n")
    _git(repo5, "add", "LATEST.txt")
    assert any("LATEST" in c for c in _concerns(repo5)), _concerns(repo5)

    # --- end-to-end through the hook, ONLY where the pre-existing arm provably skips ----------
    # (no crop staged -> "crops_data_final.json not staged -> skip", so any block below is ours)

    # 5. A DOC-ONLY commit introducing a stale claim must BLOCK. This is precisely the case the
    #    existing net skips entirely.
    repo4 = _make_repo(); repos.append(repo4)
    _write(repo4, "CLAUDE.md",
           "# repo\n\n## What this is\n"
           "2 crops: 9 certified gold-standard anchors + 1 honest shells (the 1 remaining shells "
           "are the 0 mushrooms + olive).\n")
    _git(repo4, "add", "CLAUDE.md")
    code, out = _run_hook(repo4)
    assert code == 1, (code, out)
    assert "9" in out and "roster" in out.lower(), out

    # 6. CONTAINMENT. A commit touching neither the canonical, LATEST.txt, nor a gated doc must
    #    NOT be blocked, even while the docs are stale for an unrelated reason.
    repo3 = _make_repo(); repos.append(repo3)
    _write(repo3, "crops_data_final.json", _canonical(certify_olive=True))
    _git(repo3, "add", "crops_data_final.json")
    _git(repo3, "commit", "-qm", "stale on purpose", "--no-verify")
    _write(repo3, "unrelated.txt", "still nothing to do with the roster\n")
    _git(repo3, "add", "unrelated.txt")
    code, out = _run_hook(repo3)
    assert code == 0, ("unrelated commit must not be blocked by a pre-existing stale claim",
                       code, out)

    # 7. A doc-only commit that keeps the claims true must PASS end-to-end.
    repo6 = _make_repo(); repos.append(repo6)
    _write(repo6, "docs/crop_expansion_roadmap.md",
           "- reworded, still true: the design/retire shells (the 0 mushrooms + olive).\n")
    _git(repo6, "add", "docs/crop_expansion_roadmap.md")
    code, out = _run_hook(repo6)
    assert code == 0, (code, out)
finally:
    for r in repos:
        shutil.rmtree(r, ignore_errors=True)

print("precommit roster-claim tests: OK")
