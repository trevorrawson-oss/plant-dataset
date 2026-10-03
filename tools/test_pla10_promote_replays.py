#!/usr/bin/env python3
"""The three PLA-10 promotes, replayed on their REAL stages, must reproduce their landed canonicals byte for byte.

Housekeeping kickoff 60, ruling 5 (2026-10-03): these replace the inspect.getsource identity pins. A pin that
compares promote 1's helper text to a copy says nothing once both are one object; what matters is that the code
at HEAD still turns each promote's pinned pre-state + its committed stage + the hashed evidence into exactly
the canonical that landed. A change to any shared reader (norm_text, pdf_text, manifest, the evidence block,
the restatement scanner, T4) that changes a single verdict or a single byte reddens the promote it touches.

  promote 1  c5fc3d13 -> cf1d480d   (landed d021116)
  promote 2  cf1d480d -> 31b766e8   (landed 7177af3)
  promote 3  31b766e8 -> b331e5f2   (landed 9cea239)

Each test reports the population it inspected (staged crops, evidence rows) and asserts it, so a stage
directory that silently empties cannot pass: an empty replay is "inspected nothing", not green.

THE SCANNER POPULATION. Each promote's restatement guard is one-directional (every scanner hit must be
adjudicated), so a scanner that goes BLIND passes the replay byte for byte: nothing it fails to flag is ever
refused. Measured 2026-10-03, the harness proved it (r_spacing_scanner_blind survived a SHA-only replay). So
each replay also pins the scanner's hit count over its staged crops' PRE-STATE records, and how many staged
adjudications the scanner does not flag (hand-swept leaves; promote 3's 35 are PLA-655's blind spot). A
deliberate scanner change (PLA-655) re-measures these literals with the rows read; it never edits them blind.

NEEDS THE LOCAL EVIDENCE CACHE (tools/.evidence_cache holds the raw bytes; only MANIFEST.tsv is tracked). In a
checkout without it these tests FAIL by name; they never skip, because a replay that did not read the bytes
proves nothing about the reader.
Run: python3 -m pytest tools/test_pla10_promote_replays.py -q
"""
import csv, glob, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla10_planting_layout as P1  # noqa: E402
import promote_pla10_promote2 as P2  # noqa: E402
import promote_pla10_promote3 as P3  # noqa: E402

POST = {
    "P1": "cf1d480dfc926b226f63fde2fbdbc548e9d06487ed749e7431a06710431f2e49",
    "P2": "31b766e86a01377c88898568171bcb372d3da1d3146fa50f6cbd6288dd8b6369",
    "P3": "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d",
}


def _cache_or_fail(P):
    man = os.path.join(P.EVIDENCE, "MANIFEST.tsv")
    with open(man, encoding="utf-8", newline="") as f:
        shas = {r["sha256"] for r in csv.DictReader(f, delimiter="\t")}
    present = {os.path.basename(p).split(".")[0] for p in glob.glob(os.path.join(P.EVIDENCE, "*.*"))}
    missing = shas - present
    if missing:
        raise AssertionError(f"EVIDENCE CACHE INCOMPLETE, NOT A CODE DEFECT: {len(missing)} of {len(shas)} "
                             f"MANIFEST digests have no bytes in {P.EVIDENCE}; the replay cannot read them")


def _scanner_population(P, scan):
    """(scanner hits over every staged crop's pre-state record, staged adjudications the scanner misses)."""
    pre = {c["slug"]: c for c in json.loads(promote_fixture.pre_state(P.BASE_SHA))["crops"]}
    stage, _ev = P.load_stage(P.STAGE)
    hits = missed = 0
    for slug, s in stage.items():
        h = set(scan(pre[slug], s))
        adj = {P.fmt(P.resolve(pre[slug], r["path"])) for r in s.get("restatements") or []}
        hits += len(h)
        missed += len(adj - h)
    return hits, missed


def _replay(P):
    _cache_or_fail(P)
    pre = json.loads(promote_fixture.pre_state(P.BASE_SHA))
    stage, ev = P.load_stage(P.STAGE)
    out = P.run(pre, stage, ev, P.EVIDENCE)
    return out, stage, ev


class Replays(unittest.TestCase):
    def test_promote_1_reproduces_cf1d480d(self):
        (post, n, _r, n_ev), stage, ev = _replay(P1)
        self.assertEqual((n, len(stage), len(ev), n_ev), (113, 113, 203, 203),
                         "promote 1 replay population moved (staged crops, evidence rows, figures)")
        self.assertEqual(P1.sha256_bytes(P1.serialize(post)), POST["P1"])
        self.assertEqual(_scanner_population(P1, lambda a, s: P1.spacing_strings(a)), (762, 1),
                         "promote 1 scanner population moved (hits, adjudicated-but-not-flagged)")

    def test_promote_2_reproduces_31b766e8(self):
        (post, n), stage, ev = _replay(P2)
        self.assertEqual((n["crops"], len(stage), len(ev)), (33, 33, 45),
                         "promote 2 replay population moved (staged crops, evidence rows)")
        self.assertEqual(P2.sha256_bytes(P2.serialize(post)), POST["P2"])
        self.assertEqual(_scanner_population(P2, lambda a, s: P2.spacing_strings(a)), (202, 0),
                         "promote 2 scanner population moved (hits, adjudicated-but-not-flagged)")

    def test_promote_3_reproduces_b331e5f2(self):
        (post, n), stage, ev = _replay(P3)
        self.assertEqual((n["crops"], len(stage), len(ev), n["evidence_rows"]), (62, 62, 98, 98),
                         "promote 3 replay population moved (staged crops, evidence rows)")
        self.assertEqual(P3.sha256_bytes(P3.serialize(post)), POST["P3"])
        self.assertEqual(_scanner_population(P3, lambda a, s: P3.height_strings(a, s.get(P3.S) is not None)),
                         (113, 35), "promote 3 scanner population moved (hits, adjudicated-but-not-flagged)")


if __name__ == "__main__":
    unittest.main()
