#!/usr/bin/env python3
"""gate_all -- run the always-on whole_crop_gate on EVERY certified crop and require PASS.

THE GAP THIS CLOSES: whole_crop_gate validates ONE crop at a time; release_verify runs it only on the
promote target + the reference crop; the pre-commit hook (precommit_release_verify) is a REGRESSION net
-- it blocks NEW violations on CHANGED crops, and deliberately does not require gate == 0. So nothing
asserted that the WHOLE certified roster passes the suite. A coverage/shape regression on an untouched
crop, or a newly-certified crop the operator forgot to gate, could sit green. As the roster scales
toward ~105 certified via the bot pipeline, that is exactly the drift the register-coverage gates
(A39 / A40-A42) were built to stop -- but a gate only binds if it is actually RUN on every crop.

gate_all is the run-all floor: it loops every crop whose verification_status.status == 'verified_gs_arc',
runs whole_crop_gate, and FAILS if any certified crop is not PASS. Uncertified §E shells are EXCLUDED --
they are unfilled shells that legitimately fail the suite until they are authored + certified.

Use it at release (protocol #6, alongside release_verify + the source-truth sample) and in any CI/
pre-release step, so a certified crop can never silently fall out of gate-compliance.

Usage: python3 tools/gate_all.py [crops_data_final.json]
Exit 1 if any certified crop fails whole_crop_gate.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "whole_crop_gate.py")


def run(path):
    """Run whole_crop_gate on every certified crop in `path`. Return (certified_slugs, failed) where
    failed is a list of (slug, violation_count) for each certified crop that did not PASS."""
    data = json.load(open(path, encoding="utf-8"))
    cert = [c.get("slug") for c in data["crops"]
            if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    failed = []
    for slug in cert:
        out = subprocess.run([sys.executable, GATE, slug, path],
                             capture_output=True, text=True).stdout
        lines = out.splitlines()
        if not any(l.startswith("GATE: PASS") for l in lines):
            n = sum(1 for l in lines if "VIOLATION:" in l)
            failed.append((slug, n))
    return cert, failed


def launch_ready(path):
    """(launch_ready_slugs, blocked_slugs) among the certified.

    PLA-466: "certified" and "launch-ready" are DISTINCT. A bare "121/121 PASS" must not be read
    as 121 launch-ready, because a crop can pass every gate while honestly carrying a live
    blocking finding with both launch flags false. Reported alongside the gate verdict so the
    summary matches the state trio rather than contradicting it.
    """
    data = json.load(open(path, encoding="utf-8"))
    ready, blocked = [], []
    for c in data["crops"]:
        vs = c.get("verification_status") or {}
        if vs.get("status") != "verified_gs_arc":
            continue
        if vs.get("launch_ready_core") and vs.get("launch_ready_seasoned"):
            ready.append(c["slug"])
        else:
            blocked.append(c["slug"])
    return ready, blocked


# ---------------------------------------------------------------- THE FLOOR
# gate_all PASSED ON AN EMPTY POPULATION. Measured 2026-09-22: with every crop
# decertified it printed "ran whole_crop_gate on 0 certified crop(s)" and
# "PASS -- gate passes 0/0 certified" and exited 0. It is the gate protocol #6
# requires before every promote and the one every landing record cites, so a
# vacuous pass here is the most expensive one in the repo. Reporting the count
# was never the gap -- it already did that honestly and passed anyway.
#
# The floor is NOT a constant: the certified count moves, so a hardcoded number
# would either block a legitimate change or rot into a rubber stamp. It asserts
# against the number ALREADY RECORDED in CLAUDE.md's count sentence -- the one
# present-tense home for it, already machine-checked against canonical by
# doc_roster_claim_gate with this module's own certified predicate. That gate's
# parser and derived-truth function are IMPORTED, never retyped, because a
# retyped table is how two bugs got in before.
#
# It fails on disagreement in EITHER direction: 0 != 121 catches a vacuous run,
# and 120 != 121 catches a crop silently dropping out of certification.
from doc_roster_claim_gate import COUNT_RE, roster_facts  # noqa: E402


def recorded_certified(root="."):
    """The certified count as CLAUDE.md states it, or None if unreadable."""
    try:
        m = COUNT_RE.search(open(os.path.join(root, "CLAUDE.md"), encoding="utf-8").read())
    except OSError:
        return None
    return int(m.group(2)) if m else None


def main():
    argv = sys.argv[1:]
    expect = None
    if "--expect-certified" in argv:
        i = argv.index("--expect-certified")
        expect = int(argv[i + 1])
        del argv[i:i + 2]
    path = argv[0] if argv else "crops_data_final.json"
    cert, failed = run(path)
    ready, blocked = launch_ready(path)
    print(f"gate_all: ran whole_crop_gate on {len(cert)} certified crop(s)")
    if failed:
        for slug, n in failed:
            print(f"  FAIL {slug} ({n} violation(s))")
        print(f"\ngate_all: {len(failed)} of {len(cert)} certified crop(s) FAILED whole_crop_gate "
              f"-- run `python3 tools/whole_crop_gate.py <slug>` for detail")
        sys.exit(1)
    # ROSTER-LEVEL FLOORS. whole_crop_gate is PER-CROP and structurally cannot see a COUNT, so a
    # ratchet has to run here, once, over the whole roster. PLA-533 ruling 1 (Trevor, 2026-09-22):
    # the population of certified crops stating a container_notes.min_pot_gallons with no citation
    # may go DOWN, never UP. Armed at 4, where it is GREEN -- it does not wait for those four to be
    # re-sourced, it stops the population growing while the audit runs.
    from container_citation_floor_gate import violations as _ccf_violations, uncited as _ccf_uncited
    _ccf = _ccf_violations(json.load(open(path, encoding="utf-8")))
    if _ccf:
        for m in _ccf:
            print(f"  VIOLATION: container-citation-floor: {m}")
        print(f"\ngate_all: container_citation_floor_gate FAILED ({len(_ccf)} violation(s)) "
              f"-- run `python3 tools/container_citation_floor_gate.py` for detail")
        sys.exit(1)

    # "PASS" is load-bearing: tools/test_gate_all.py asserts it appears on a clean run. Both
    # numbers sit on the same line so the verdict can never be read as a launch-ready count.
    # THE FLOOR. `expect` is for a promote whose post-state intentionally moves the
    # count before CLAUDE.md is updated; it is explicit and shows up in the record,
    # which a silent pass never did.
    floor = expect if expect is not None else recorded_certified()
    if floor is None:
        print("gate_all: REFUSED -- no recorded certified count to check against "
              "(CLAUDE.md count sentence unreadable). Pass --expect-certified N.")
        sys.exit(2)
    if len(cert) != floor:
        src = "--expect-certified" if expect is not None else "CLAUDE.md"
        print(f"gate_all: REFUSED -- inspected {len(cert)} certified crop(s) but {src} "
              f"records {floor}. Disagreement in either direction is a defect: too few means "
              f"this run inspected less than it claims, too many means the record is stale. "
              f"A promote that intentionally moves the count passes --expect-certified N.")
        sys.exit(2)

    print(f"gate_all: PASS -- gate passes {len(cert)}/{len(cert)} certified, "
          f"launch-ready {len(ready)}/{len(cert)}")
    print(f"  container-citation floor: {len(_ccf_uncited(json.load(open(path, encoding='utf-8'))))}"
          f" uncited min_pot_gallons (PLA-533 ratchet, may shrink never grow)")
    if blocked:
        print(f"  NOT launch-ready ({len(blocked)}): {', '.join(sorted(blocked))}")
        print("  (CERTIFIED = status verified_gs_arc. LAUNCH-READY = that plus both "
              "launch_ready_* flags. A blocking finding drives the flags, never the status "
              "-- PLA-466.)")
    sys.exit(0)


if __name__ == "__main__":
    main()
