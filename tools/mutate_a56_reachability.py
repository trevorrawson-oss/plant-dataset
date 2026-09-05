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

FOUND DEAD 2026-09-05, and repaired here. This harness had been exiting `HARNESS DEAD` on every run
since 2026-08-24 -- which is the liveness defense working exactly as designed, and nobody re-ran it
to see. Two things had gone stale under it:

  1. Its SENTINEL stripped every ladder to `[]` and asserted A56 stays SILENT, because on
     2026-08-22 an empty ladder was indistinguishable from an absent one. On 2026-08-24
     `ladder_violations` gained the "`[]` is laddered-and-left-blank, a defect in every case"
     check (sweet-corn's raccoons), so the sentinel's own injection became a legitimate A56 hit
     and the harness read its correct catch as a mis-armed coverage floor.
  2. Its premise, "confirms the coverage floor is NOT armed," went false on 2026-09-05 when the
     floor was armed as A57 at the PLA-8 arc close.

The repair is not to delete the check but to point it at what is now true: `[]` MUST redden A56
(the sentinel the convention asks for), and a `None` ladder must redden A57 and NOT A56 -- the
separation that stops one defect being reported twice under two guards. Coverage itself is
`tools/mutate_a57_coverage_floor.py`'s job.

Usage: python3 tools/mutate_a56_reachability.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET   # the gate's tables, not retyped
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


CHOSEN = []          # what the derived coherence mutation actually picked, printed each run


def m_applies_to_incoherent(d, crop):
    """A method from a different kingdom on a fungal disease -- DERIVED from the live catalog.

    THIS MUTATION HAS NOW GONE STALE TWICE, which is why it no longer names a method. The first
    version used `raise_soil_ph` (fungal_soilborne) and survived correctly: `problem.type` is
    coarse, TYPE_TARGETS['fungal'] covers fungal_foliar, fungal_soilborne AND disease_general, so
    any fungal-ish method fits any fungal problem, and this check only catches a DIFFERENT kingdom.
    The replacement, `balance_nitrogen`, was insect_soft_bodied only when it was picked on
    2026-08-22 -- and by 2026-09-05 the catalog had widened it to
    ['insect_soft_bodied', 'fungal_foliar', 'fungal_soilborne'], making the injection legal and the
    mutation a false survivor. A hard-coded method name is a record of what the catalog looked like
    once, and the catalog is the thing under test's own input.

    So: pick, at run time, any CULTURAL method whose applies_to shares nothing with the fungal
    target set. Cultural because it replaces a cultural rung, so tier monotonicity stays intact and
    coherence is the only family that can trip. HARNESS DEAD if the catalog no longer offers one.
    """
    fungal = set(TYPE_TARGETS["fungal"]) | {UNIVERSAL_TARGET}
    picks = sorted(mid for mid, m in d["control_methods"].items()
                   if m.get("tier") == "cultural" and not (set(m.get("applies_to") or []) & fungal))
    if not picks:
        raise SystemExit("HARNESS DEAD: no cultural catalog method is disjoint from the fungal "
                         "targets -- the coherence mutation cannot be built")
    CHOSEN.append((picks[0], sorted(d["control_methods"][picks[0]].get("applies_to") or [])))
    _lad(crop, "apple-scab")["control_ladder"][0]["method"] = picks[0]


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


# Each row carries the SUBSTRING the targeted guard emits. Grading on "A56 fired at all" lets a
# mutation be scored as caught by a DIFFERENT family than the one it aims at -- the
# green-because-an-earlier-check-fires shape. The expected string is the guard's own wording, so a
# reworded message fails loudly here instead of quietly downgrading this harness to a smoke test.
MUTATIONS = [
    ("tier inversion (spray hoisted above cultural)", "monotonicity", m_tier_inversion,
     "is not softest-first"),
    ("rung names a method not in the catalog", "referential", m_unknown_method,
     "references unknown method"),
    ("method's applies_to does not fit the problem type", "coherence", m_applies_to_incoherent,
     "does not fit problem type"),
    ("two problems share an id", "identity", m_duplicate_id, "duplicate id"),
    ("a laddered problem loses its id", "identity", m_missing_id, "missing 'id'"),
    ("a problem id is not kebab-case", "identity", m_non_kebab_id, "id is not kebab-case"),
    ("problem type is not a recognized value", "coherence", m_unrecognized_type,
     "is not a recognized type"),
    ("catalog entry loses a required key", "catalog", m_catalog_missing_key,
     "missing/empty required key"),
    ("catalog entry cites a non-T1 source", "catalog", m_catalog_non_t1_source, "is not T1"),
    ("catalog entry carries an invalid tier", "catalog", m_catalog_bad_tier, "invalid tier"),
]

# The sentinel MUST redden. Emptying every ladder is `ladder_violations`' laddered-and-left-blank
# defect, so A56 owns it and a silent A56 here means the harness is not grading.
SENTINEL = ("SENTINEL: every rung stripped from every ladder (empty, not absent)",
            lambda d, crop: [p.__setitem__("control_ladder", [])
                             for fam in ("pests", "diseases") for p in crop.get(fam) or []
                             if isinstance(p, dict) and "control_ladder" in p])

# The scope check. A56 is INTEGRITY; absence is A57's. Nulling every ladder must redden A57 and
# leave A56 SILENT -- if A56 fired here, one defect would be reported twice under two guards, and
# A56's whole design (no-op on an unladdered problem, which is what makes it free to arm early)
# would be false.
SCOPE = ("SCOPE: every ladder nulled -- A57's defect, not A56's",
         lambda d, crop: [p.__setitem__("control_ladder", None)
                          for fam in ("pests", "diseases") for p in crop.get(fam) or []
                          if isinstance(p, dict)])


def run(path):
    """True == whole_crop_gate PASSES. Returns (passed, a56_fired, a57_fired).

    A56 fails as `control-ladder: ...` and A57 as `control-ladder-coverage: ...`, so the two
    prefixes do not alias -- "control-ladder-coverage:" does not contain "control-ladder:"."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), CROP, path],
                       capture_output=True, text=True, cwd=REPO)
    out = r.stdout + r.stderr
    return "GATE: PASS" in out, "control-ladder:" in out, "control-ladder-coverage:" in out, out


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
    ok, _, _, _ = run(CANON)
    if not ok:
        print("HARNESS DEAD: the unmutated canonical does not PASS whole_crop_gate.")
        return 1
    print("positive control : GREEN (unmutated canonical passes)")

    # SENTINEL -- must redden, or the run is not grading anything.
    label, fn = SENTINEL
    p = stage(fn)
    ok, fired, _, _ = run(p)
    os.unlink(p)
    if ok or not fired:
        print(f"HARNESS DEAD: {label} did NOT redden A56 (fired={fired}, gate passed={ok}).")
        return 1
    print(f"sentinel         : REDDENS ({label})")

    # SCOPE -- absence belongs to A57. A56 must stay silent on it.
    label, fn = SCOPE
    p = stage(fn)
    ok, a56, a57, _ = run(p)
    os.unlink(p)
    if a56 or not a57:
        print(f"HARNESS DEAD: {label} -- A56 fired={a56}, A57 fired={a57}. The integrity and "
              f"coverage guards are not cleanly separated.")
        return 1
    print(f"scope check      : A57 owns absence, A56 SILENT ({label})\n")

    caught = survived = 0
    fam = {}
    for label, family, fn, expect in MUTATIONS:
        p = stage(fn)
        ok, fired, _, out = run(p)
        os.unlink(p)
        fam.setdefault(family, [0, 0])
        on_target = any(expect in l for l in out.splitlines() if "control-ladder:" in l)
        if ok or not fired or not on_target:
            survived += 1; fam[family][1] += 1
            why = "" if fired else " (A56 silent)"
            if fired and not on_target:
                why = f" (A56 fired, but not on {expect!r} -- a DIFFERENT guard caught it)"
            print(f"  SURVIVED  [{family}] {label}{why}")
        else:
            caught += 1; fam[family][0] += 1
            extra = f"  -> picked {CHOSEN[-1][0]} {CHOSEN[-1][1]}" if CHOSEN and fn is m_applies_to_incoherent else ""
            print(f"  caught    [{family}] {label}{extra}")

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
