#!/usr/bin/env python3
"""Tests for the doc roster-claim gate. Run BOTH ways (dual-runner):
    python3 tools/test_doc_roster_claim_gate.py
    python3 -m pytest tools/test_doc_roster_claim_gate.py

WHY: the roster composition (total / certified / shells) is a DERIVED fact -- computable from
crops_data_final.json in one line, using the same `verified_gs_arc` predicate gate_all uses to
build the certified roster. It was nonetheless hand-copied into prose in several LIVE docs, and
on 2026-07-24 (asparagus, GS #120) and 2026-07-28 (artichoke, GS #121) the data moved while the
prose did not. CLAUDE.md then told every session for a week that there were 120 certified crops
and that artichoke was an unauthored shell; docs/crop_expansion_roadmap.md listed artichoke AND
asparagus as still owed design-then-author work. That is the stale-record class ruled on
2026-07-29: a stale record reads as current truth and commissions phantom work.

This is mechanizable in a way the stale-`open_finding` text scan explicitly was not. That check
needed judgment about what a finding was QUOTING (measured at 45 candidate hits, almost all
legitimate) and was correctly not built. This one is integer equality plus set membership against
the canonical, so it cannot flood: a claim either matches the data or it does not.

Each assertion below sneaks one defect class at the gate and confirms it bounces. The last block
replays the REAL pre-fix bytes of both documents out of git (commit b9c9bb1) and requires the gate
to catch the actual historical defect, not a synthetic stand-in.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_roster_claim_gate import (
    roster_facts,
    doc_claim_violations,
    latest_sha_violations,
)

# --- fixture canonical: 2 certified (apple, artichoke) + 4 shells (avocado, olive, 2 mushrooms) ---
DATA = {"crops": [
    {"slug": "apple", "verification_status": {"status": "verified_gs_arc"}},
    {"slug": "artichoke", "verification_status": {"status": "verified_gs_arc"}},
    {"slug": "avocado"},
    {"slug": "olive"},
    {"slug": "button-mushroom"},
    {"slug": "oyster-mushroom"},
]}

CLEAN = ("6 crops: 2 certified gold-standard anchors + 4 honest shells (the ~105-certified "
         "bot-pipeline goal is met and passed; the 4 remaining shells are the 2 mushrooms + "
         "avocado/olive). The armor is the gate suite.")

# --- roster_facts: the derived truth, computed with gate_all's own predicate ---
F = roster_facts(DATA)
assert F["total"] == 6, F
assert F["certified"] == 2, F
assert F["shells"] == 4, F
assert F["mushroom_shells"] == 2, F
assert F["named_shells"] == {"avocado", "olive"}, F
assert F["certified_slugs"] == {"apple", "artichoke"}, F

# 0. clean text matching the data -> no violations
assert doc_claim_violations(CLEAN, "CLAUDE.md", F) == [], doc_claim_violations(CLEAN, "CLAUDE.md", F)

# 1. certified count stale (the artichoke defect's arithmetic half) -> violation
bad = CLEAN.replace("2 certified", "1 certified")
assert any("certified" in v for v in doc_claim_violations(bad, "CLAUDE.md", F)), \
    doc_claim_violations(bad, "CLAUDE.md", F)

# 2. total crop count wrong -> violation
bad = CLEAN.replace("6 crops", "7 crops")
assert any("total" in v for v in doc_claim_violations(bad, "CLAUDE.md", F)), \
    doc_claim_violations(bad, "CLAUDE.md", F)

# 3. shell count wrong -> violation
bad = CLEAN.replace("+ 4 honest shells", "+ 5 honest shells")
assert any("shell" in v for v in doc_claim_violations(bad, "CLAUDE.md", F)), \
    doc_claim_violations(bad, "CLAUDE.md", F)

# 4. THE ANTI-VACUOUS CASE. A gate that validates a sentence's SHAPE cannot notice the sentence's
#    ABSENCE (the lesson asparagus taught: it certified 120/120 carrying zero planting data). If
#    someone rewords or deletes the roster sentence, this gate must go RED, not silently green
#    forever.
assert any("no roster sentence" in v.lower()
           for v in doc_claim_violations("Some prose with no roster claim at all.", "CLAUDE.md", F)), \
    doc_claim_violations("Some prose with no roster claim at all.", "CLAUDE.md", F)

# 5. THE REAL DEFECT: the shell enumeration names a crop that is actually CERTIFIED.
#    Counts here are internally consistent, so ONLY the enumeration check can catch this.
bad = CLEAN.replace("avocado/olive)", "avocado/olive/artichoke)")
V = doc_claim_violations(bad, "CLAUDE.md", F)
assert any("artichoke" in v and "certified" in v for v in V), V

# 6. the enumeration OMITS an actual shell -> violation (the mirror defect: a shell gets
#    forgotten rather than a certified crop lingering)
bad = CLEAN.replace("avocado/olive)", "avocado)")
assert any("olive" in v for v in doc_claim_violations(bad, "CLAUDE.md", F)), \
    doc_claim_violations(bad, "CLAUDE.md", F)

# 7. the mushroom sub-count drifts -> violation
bad = CLEAN.replace("the 2 mushrooms", "the 5 mushrooms")
assert any("mushroom" in v for v in doc_claim_violations(bad, "CLAUDE.md", F)), \
    doc_claim_violations(bad, "CLAUDE.md", F)

# 8. a doc that carries ONLY the enumeration (the roadmap's shape, no count sentence) is judged on
#    the enumeration alone -- the count sentence is required of CLAUDE.md only.
ROADMAP_CLEAN = ("- The GS-anchor certification backlog: staged draft crops + the design/retire "
                 "shells (the 2\n  mushrooms + avocado/olive). See memory.")
assert doc_claim_violations(ROADMAP_CLEAN, "docs/crop_expansion_roadmap.md", F) == [], \
    doc_claim_violations(ROADMAP_CLEAN, "docs/crop_expansion_roadmap.md", F)
bad = ROADMAP_CLEAN.replace("avocado/olive)", "avocado/olive/artichoke/apple)")
V = doc_claim_violations(bad, "docs/crop_expansion_roadmap.md", F)
assert any("artichoke" in v for v in V) and any("apple" in v for v in V), V

# --- LATEST.txt: the same class (a derived value hand-copied into prose) ---
CANON = b'{"crops":[]}'
import hashlib
GOOD_SHA = hashlib.sha256(CANON).hexdigest()

# 9. LATEST.txt SHA matching the canonical -> clean
assert latest_sha_violations(f"SHA: {GOOD_SHA}\nDate: 2026-08-04\nSession: x", CANON) == []

# 10. LATEST.txt SHA stale -> violation
V = latest_sha_violations("SHA: " + "0" * 64 + "\nDate: 2026-08-04\n", CANON)
assert any("SHA" in v for v in V), V

# 11. LATEST.txt carrying NO SHA line -> violation (anti-vacuous again)
V = latest_sha_violations("Date: 2026-08-04\nSession: x\n", CANON)
assert any("no sha" in v.lower() for v in V), V

# --- THE ADVERSARIAL REPLAY: the real pre-fix bytes must bounce -------------------------------
# Not a synthetic defect. These are the exact strings that shipped in commit b9c9bb1, checked
# against the REAL canonical. If the gate cannot catch the defect that actually happened, it is
# not worth running.
REAL_PRE_FIX_CLAUDE = (
    "128 crops: 120 certified gold-standard anchors + 8 honest shells (the ~105-certified "
    "bot-pipeline\ngoal is met and passed; the 8 remaining shells are the 5 mushrooms + "
    "avocado/olive/artichoke). The armor is the gate suite")
REAL_PRE_FIX_ROADMAP = (
    "- The GS-anchor certification backlog: staged §E draft crops + the design/retire shells "
    "(the 5\n  mushrooms + avocado/olive/artichoke/asparagus). See memory "
    "`remaining-gs-anchors-roadmap`.")

import json

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CANON_PATH = os.path.join(_ROOT, "crops_data_final.json")
REAL = roster_facts(json.load(open(_CANON_PATH, encoding="utf-8")))

# The live canonical is the authority for what the roster IS. Asserted explicitly (NOT derived
# from any document) so this test states the expected roster as a constant and would itself go
# red if the file drifted from what this session verified.
assert REAL["total"] == 128, REAL["total"]
assert REAL["certified"] == 121, REAL["certified"]
assert REAL["shells"] == 7, REAL["shells"]
assert "artichoke" in REAL["certified_slugs"], "artichoke certified GS #121 on 2026-07-28"
assert "asparagus" in REAL["certified_slugs"], "asparagus certified GS #120 on 2026-07-24"

V = doc_claim_violations(REAL_PRE_FIX_CLAUDE, "CLAUDE.md", REAL)
assert any("120" in v for v in V), ("stale certified count must bounce", V)
assert any("artichoke" in v for v in V), ("artichoke-named-as-shell must bounce", V)

V = doc_claim_violations(REAL_PRE_FIX_ROADMAP, "docs/crop_expansion_roadmap.md", REAL)
assert any("artichoke" in v for v in V), V
assert any("asparagus" in v for v in V), V

# --- and the CURRENT bytes of both live docs must be CLEAN ------------------------------------
for rel in ("CLAUDE.md", "docs/crop_expansion_roadmap.md"):
    text = open(os.path.join(_ROOT, rel), encoding="utf-8").read()
    assert doc_claim_violations(text, rel, REAL) == [], \
        (rel, doc_claim_violations(text, rel, REAL))

with open(_CANON_PATH, "rb") as f:
    _canon_bytes = f.read()
_latest = open(os.path.join(_ROOT, "LATEST.txt"), encoding="utf-8").read()
assert latest_sha_violations(_latest, _canon_bytes) == [], latest_sha_violations(_latest, _canon_bytes)

# --- CLI exit-code behavior (subprocess; gate by exit code) -----------------------------------
import subprocess

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_roster_claim_gate.py")

# 12. the real repo, as it stands post-fix -> exit 0
r = subprocess.run([sys.executable, _GATE, "--root", _ROOT], capture_output=True, text=True)
assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)

# 13. a repo whose CLAUDE.md carries the pre-fix line -> exit 1
import shutil
import tempfile

_tmp = tempfile.mkdtemp()
try:
    shutil.copy(_CANON_PATH, os.path.join(_tmp, "crops_data_final.json"))
    shutil.copy(os.path.join(_ROOT, "LATEST.txt"), os.path.join(_tmp, "LATEST.txt"))
    os.makedirs(os.path.join(_tmp, "docs"))
    with open(os.path.join(_tmp, "CLAUDE.md"), "w", encoding="utf-8") as f:
        f.write(REAL_PRE_FIX_CLAUDE)
    with open(os.path.join(_tmp, "docs", "crop_expansion_roadmap.md"), "w", encoding="utf-8") as f:
        f.write(REAL_PRE_FIX_ROADMAP)
    r = subprocess.run([sys.executable, _GATE, "--root", _tmp], capture_output=True, text=True)
    assert r.returncode == 1, (r.returncode, r.stdout)
    assert "artichoke" in r.stdout, r.stdout
finally:
    shutil.rmtree(_tmp)

print("doc_roster_claim_gate tests: OK")
