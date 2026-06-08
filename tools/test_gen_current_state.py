#!/usr/bin/env python3
"""gen_current_state: the GENERATED mechanical sections must reflect true state
(LATEST.txt SHA, all-anchor gate PASS, region fill, flip status), and the prose
slots must be clearly marked for the operator. Run from repo root.
python3 tools/test_gen_current_state.py
"""
import os, sys, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
out = subprocess.run([sys.executable, os.path.join(HERE, "gen_current_state.py")],
                     cwd=ROOT, capture_output=True, text=True)
assert out.returncode == 0, f"generator exited {out.returncode}\n{out.stderr}"
gen = out.stdout
live = open(os.path.join(ROOT, "CURRENT_STATE.md")).read()

# 1. canonical SHA from LATEST.txt appears in the generated pointer AND the live file
sha = next(l.split("SHA:")[1].strip() for l in open(os.path.join(ROOT, "LATEST.txt"))
           if l.startswith("SHA:"))
assert sha in gen, "generated pointer missing canonical SHA"
assert sha in live, "live CURRENT_STATE missing canonical SHA (stale -- regenerate it?)"

# 2. the static SESSION PROTOCOL header is carried through verbatim
assert "SESSION PROTOCOL" in gen, "generated file dropped the protocol header"

# 3. gate record: every verified_gs_arc anchor shows PASS in BOTH gen and live
for anchor in ("lettuce", "cherry", "beefsteak"):
    assert re.search(anchor + r".{0,30}PASS", gen, re.I), f"generated gate-record missing {anchor} PASS"

# 4. region fill state is generated (all anchors 10/10 today)
assert "10/10" in gen or "10 / 10" in gen, "generated region-fill state missing the 10/10 fill"

# 5. flip gates reflect launch_ready true / verified_gs_arc
assert "verified_gs_arc" in gen, "generated flip-gates missing the status"

# 6. the prose slots are clearly marked for the operator
for slot in ("headline", "What just happened", "Active work", "locked decisions"):
    assert re.search(r"FILL:.*" + re.escape(slot), gen, re.I), f"missing FILL slot for {slot!r}"

print("PASS gen_current_state mechanical-section + FILL-slot checks")
