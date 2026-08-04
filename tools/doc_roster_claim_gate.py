#!/usr/bin/env python3
"""doc roster-claim gate -- keeps the roster facts stated in LIVE prose equal to the canonical.

The roster composition (total / certified / shells) is DERIVED: computable from
crops_data_final.json with the same `verified_gs_arc` predicate `gate_all` uses to build the
certified roster. It is nonetheless hand-copied into prose, and prose does not move when data
does. On 2026-07-24 asparagus certified as GS #120 and on 2026-07-28 artichoke as GS #121; both
documents below went on asserting the pre-certification roster until 2026-08-04. CLAUDE.md is
read at the top of every session, so it told every session for a week that artichoke was an
unauthored shell.

WHAT IS CHECKED (an enumerated constant, never derived from the documents themselves):
  CLAUDE.md                        count sentence + shell enumeration
  docs/crop_expansion_roadmap.md   shell enumeration
  LATEST.txt                       SHA equals sha256(crops_data_final.json)

WHAT IS DELIBERATELY NOT CHECKED: STATE_HISTORY.md, CURRENT_STATE.md's dated promote entries, and
the dated files under docs/superpowers/. Those are APPEND-ONLY historical records that were
accurate when written; a roster count inside one is a statement about its own date, not a claim
about now. Gating them would demand rewriting history into current tense, which is exactly what
the verification_log_ref convention forbids. Only surfaces that speak in the PRESENT are gated.

Why this is gateable when the stale-`open_finding` scan was not: that check needed judgment about
what a finding was quoting (measured at 45 candidate hits, almost all legitimate, correctly NOT
built). This one is integer equality plus set membership against the canonical, so it cannot
flood -- a claim either matches the data or it does not.

Usage:
  python3 tools/doc_roster_claim_gate.py [--root .]
Exit 1 on any stale claim; else 0.
"""
import hashlib
import re

CERTIFIED = "verified_gs_arc"

# Enumerated on purpose. A gate whose scope is DERIVED from what it validates cannot fail.
DOCS_WITH_COUNT_SENTENCE = ("CLAUDE.md",)
DOCS_WITH_SHELL_ENUMERATION = ("CLAUDE.md", "docs/crop_expansion_roadmap.md")

COUNT_RE = re.compile(
    r"(\d+)\s+crops:\s*(\d+)\s+certified[^+]*?\+\s*(\d+)\s+honest\s+shells", re.S)
ENUM_RE = re.compile(r"shells?\s+(?:are\s+|\()([^.)]*)", re.S)
MUSHROOM_RE = re.compile(r"(\d+)\s+mushrooms")


def roster_facts(data):
    """The derived truth, computed with gate_all's own certified predicate."""
    crops = data["crops"]
    certified_slugs, shell_slugs = set(), set()
    for c in crops:
        slug = c.get("slug")
        if (c.get("verification_status") or {}).get("status") == CERTIFIED:
            certified_slugs.add(slug)
        else:
            shell_slugs.add(slug)
    mushrooms = {s for s in shell_slugs if "mushroom" in (s or "")}
    return {
        "total": len(crops),
        "certified": len(certified_slugs),
        "shells": len(shell_slugs),
        "mushroom_shells": len(mushrooms),
        "named_shells": shell_slugs - mushrooms,
        "certified_slugs": certified_slugs,
    }


def doc_claim_violations(text, label, facts):
    """Return violation strings ([] = clean) for one live document's roster claims."""
    V = []

    if label in DOCS_WITH_COUNT_SENTENCE:
        m = COUNT_RE.search(text)
        if not m:
            # A shape check cannot notice an absence. Reword or delete the sentence and this
            # gate must go red, not quietly green forever.
            V.append(f"{label}: no roster sentence found "
                     f"(expected '<N> crops: <N> certified ... + <N> honest shells')")
        else:
            total, cert, shells = (int(g) for g in m.groups())
            if total != facts["total"]:
                V.append(f"{label}: states total {total} crops, canonical has {facts['total']}")
            if cert != facts["certified"]:
                V.append(f"{label}: states {cert} certified, canonical has {facts['certified']}")
            if shells != facts["shells"]:
                V.append(f"{label}: states {shells} shells, canonical has {facts['shells']}")

    if label in DOCS_WITH_SHELL_ENUMERATION:
        spans = [m.group(1) for m in ENUM_RE.finditer(text)]
        if not spans:
            V.append(f"{label}: no shell enumeration found "
                     f"(expected 'shells are ...' or 'shells (...)')")
        for span in spans:
            for slug in sorted(facts["certified_slugs"]):
                if slug and re.search(rf"\b{re.escape(slug)}\b", span):
                    V.append(f"{label}: shell list names {slug!r}, "
                             f"which is certified ({CERTIFIED})")
            for slug in sorted(facts["named_shells"]):
                if slug and not re.search(rf"\b{re.escape(slug)}\b", span):
                    V.append(f"{label}: shell list omits {slug!r}, an actual uncertified shell")
            mm = MUSHROOM_RE.search(span)
            if mm and int(mm.group(1)) != facts["mushroom_shells"]:
                V.append(f"{label}: states {mm.group(1)} mushrooms, "
                         f"canonical has {facts['mushroom_shells']} uncertified mushroom crops")

    # order-preserving dedupe (two spans can carry the same claim)
    return list(dict.fromkeys(V))


def latest_sha_violations(latest_text, canonical_bytes):
    """LATEST.txt's SHA is the same class of hand-copied derived value."""
    m = re.search(r"SHA:\s*([0-9a-f]{64})", latest_text)
    if not m:
        return ["LATEST.txt: no SHA line found"]
    actual = hashlib.sha256(canonical_bytes).hexdigest()
    if m.group(1) != actual:
        return [f"LATEST.txt: SHA {m.group(1)[:12]}... does not match "
                f"sha256(crops_data_final.json) {actual[:12]}..."]
    return []


if __name__ == "__main__":
    import argparse
    import json
    import os
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    a = ap.parse_args()

    canon_path = os.path.join(a.root, "crops_data_final.json")
    with open(canon_path, "rb") as f:
        canon_bytes = f.read()
    facts = roster_facts(json.loads(canon_bytes.decode("utf-8")))

    violations = []
    for rel in sorted(set(DOCS_WITH_COUNT_SENTENCE) | set(DOCS_WITH_SHELL_ENUMERATION)):
        p = os.path.join(a.root, rel)
        if not os.path.exists(p):
            violations.append(f"{rel}: gated document is missing")
            continue
        violations += doc_claim_violations(open(p, encoding="utf-8").read(), rel, facts)

    latest_p = os.path.join(a.root, "LATEST.txt")
    if not os.path.exists(latest_p):
        violations.append("LATEST.txt: gated document is missing")
    else:
        violations += latest_sha_violations(open(latest_p, encoding="utf-8").read(), canon_bytes)

    for v in violations:
        print(f"  VIOLATION: {v}")
    print(f"doc_roster_claim_gate: canonical = {facts['total']} crops, "
          f"{facts['certified']} certified, {facts['shells']} shells "
          f"({facts['mushroom_shells']} mushrooms + {len(facts['named_shells'])} named) "
          f"| {len(violations)} violation(s)")
    sys.exit(1 if violations else 0)
