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


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    cert, failed = run(path)
    print(f"gate_all: ran whole_crop_gate on {len(cert)} certified crop(s)")
    if failed:
        for slug, n in failed:
            print(f"  FAIL {slug} ({n} violation(s))")
        print(f"\ngate_all: {len(failed)} of {len(cert)} certified crop(s) FAILED whole_crop_gate "
              f"-- run `python3 tools/whole_crop_gate.py <slug>` for detail")
        sys.exit(1)
    print("gate_all: PASS -- every certified crop passes the whole suite")
    sys.exit(0)


if __name__ == "__main__":
    main()
