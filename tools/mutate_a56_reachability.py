#!/usr/bin/env python3
"""A56 reachability harness -- proof that the newly-armed control-ladder integrity check FIRES.

WHY. A56 arms GREEN: 0 violations roster-wide, and a no-op on the 114 certified crops that carry no
ladder yet. That is exactly the shape of a gate that reads as coverage while providing none, and
this repo has shipped one before (a celebrated check that had fired zero times ever, because an
upstream filter dropped precisely its rows). Green is not evidence. This is.

Each mutation is injected into a SCRATCH canonical and graded through the FULL `whole_crop_gate`,
not through `control_ladder_gate` standalone -- the question is whether the ARM works, not whether
the underlying gate works. A defect that the standalone gate catches but the arm does not would be
invisible to a standalone run.

LIVENESS DEFENSE: a POSITIVE CONTROL (unmutated scratch must PASS) and a SENTINEL (a mutation that
guts the ladder must redden). If either misbehaves the run exits HARNESS DEAD rather than reporting
percentages about a harness that is not grading anything.

Usage: python3 tools/mutate_a56_reachability.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
CROP = "apple"          # a fully-laddered crop, so every family is reachable on it


def _lad(crop, pid):
    for fam in ("pests", "diseases"):
        for p in crop.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    raise SystemExit(f"HARNESS DEAD: {pid} not found on {CROP}")


# ---- one mutation per guard family A56 owns -------------------------------------------------
def m_tier_inversion(d, crop):
    """A conventional spray hoisted above the cultural rung: the least-invasive-first invariant."""
    p = _lad(crop, "codling-moth")
    r = p["control_ladder"]
    r.insert(0, r.pop())


def m_unknown_method(d, crop):
    _lad(crop, "apple-scab")["control_ladder"][0]["method"] = "moon_phase_planting"


def m_applies_to_incoherent(d, crop):
    """An insect-only method on a fungal disease.

    The first version of this mutation used `raise_soil_ph` (fungal_soilborne) on apple scab and
    SURVIVED -- correctly. `problem.type` is coarse: TYPE_TARGETS['fungal'] covers fungal_foliar,
    fungal_soilborne AND disease_general, so any fungal-ish method fits any fungal problem. The
    mutation was wrong, not the gate. Worth knowing while authoring: for a `fungal` problem this
    check only catches a method from a DIFFERENT kingdom, not a foliar/soilborne mismatch.
    `balance_nitrogen` is insect_soft_bodied only, which shares nothing with the fungal set, and it
    is cultural like the rung it replaces so tier monotonicity stays intact and only coherence trips.
    """
    _lad(crop, "apple-scab")["control_ladder"][0]["method"] = "balance_nitrogen"


def m_duplicate_id(d, crop):
    _lad(crop, "fire-blight")["id"] = "apple-scab"


def m_missing_id(d, crop):
    del _lad(crop, "apple-scab")["id"]


def m_non_kebab_id(d, crop):
    _lad(crop, "apple-scab")["id"] = "Apple_Scab"


def m_unrecognized_type(d, crop):
    _lad(crop, "apple-scab")["type"] = "wizardry"


def m_catalog_missing_key(d, crop):
    del d["control_methods"]["sulfur"]["pros"]


def m_catalog_non_t1_source(d, crop):
    d["source_catalog"]["blogspot_hearsay"] = {"tier": "T3", "name": "A Blog"}
    d["control_methods"]["sulfur"]["sources"] = ["blogspot_hearsay"]
    d["control_methods"]["sulfur"]["anchoring_urls"] = {"blogspot_hearsay": {"url": "x"}}


def m_catalog_bad_tier(d, crop):
    d["control_methods"]["sulfur"]["tier"] = "mild"


MUTATIONS = [
    ("tier inversion (spray hoisted above cultural)", "monotonicity", m_tier_inversion),
    ("rung names a method not in the catalog", "referential", m_unknown_method),
    ("method's applies_to does not fit the problem type", "coherence", m_applies_to_incoherent),
    ("two problems share an id", "identity", m_duplicate_id),
    ("a laddered problem loses its id", "identity", m_missing_id),
    ("a problem id is not kebab-case", "identity", m_non_kebab_id),
    ("problem type is not a recognized value", "coherence", m_unrecognized_type),
    ("catalog entry loses a required key", "catalog", m_catalog_missing_key),
    ("catalog entry cites a non-T1 source", "catalog", m_catalog_non_t1_source),
    ("catalog entry carries an invalid tier", "catalog", m_catalog_bad_tier),
]

SENTINEL = ("SENTINEL: every rung stripped from every ladder",
            lambda d, crop: [p.__setitem__("control_ladder", [])
                             for fam in ("pests", "diseases") for p in crop.get(fam) or []
                             if isinstance(p, dict) and "control_ladder" in p])


def run(path):
    """True == whole_crop_gate PASSES. Returns (passed, a56_fired)."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), CROP, path],
                       capture_output=True, text=True, cwd=REPO)
    out = r.stdout + r.stderr
    return "GATE: PASS" in out, "control-ladder:" in out


def stage(fn):
    d = json.loads(open(CANON).read())
    crop = next(c for c in d["crops"] if c["slug"] == CROP)
    before = json.dumps(d, sort_keys=True)
    fn(d, crop)
    if json.dumps(d, sort_keys=True) == before:
        raise SystemExit("HARNESS DEAD: mutation left the canonical unchanged")
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(d, fh, ensure_ascii=False, separators=(",", ":"))
    fh.close()
    return fh.name


def main():
    print("=" * 78)
    print(f"A56 REACHABILITY -- graded through the FULL whole_crop_gate on {CROP}")
    print("=" * 78)

    # POSITIVE CONTROL
    ok, _ = run(CANON)
    if not ok:
        print("HARNESS DEAD: the unmutated canonical does not PASS whole_crop_gate.")
        return 1
    print("positive control : GREEN (unmutated canonical passes)\n")

    # SENTINEL -- note this one must NOT fire A56 (an empty ladder is legitimately absent),
    # so it is checked for the OPPOSITE property: it must NOT be caught. That is the point --
    # A56 owns integrity, not coverage, and proving it stays silent here is proving the
    # coverage floor was NOT armed by accident.
    label, fn = SENTINEL
    p = stage(fn)
    ok, fired = run(p)
    os.unlink(p)
    if fired:
        print(f"HARNESS DEAD: {label} fired A56 -- a COVERAGE floor was armed by mistake.")
        return 1
    print(f"scope check      : A56 correctly SILENT on a stripped ladder ({label})")
    print("                   -> confirms the coverage floor is NOT armed\n")

    caught = survived = 0
    fam = {}
    for label, family, fn in MUTATIONS:
        p = stage(fn)
        ok, fired = run(p)
        os.unlink(p)
        fam.setdefault(family, [0, 0])
        if ok or not fired:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for f in sorted(fam):
        c, s = fam[f]
        print(f"  {f:13s} {c} caught / {c + s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL -- A56 is armed but a guard family is unreachable through it.")
        return 1
    print("\nRESULT: PASS -- every A56 guard family fires through the full gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
