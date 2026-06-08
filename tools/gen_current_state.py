#!/usr/bin/env python3
"""gen_current_state.py -- generate the MECHANICAL sections of CURRENT_STATE.md
and leave clearly-marked prose slots.

The CURRENT_STATE.md regen IS the release safety net (a sloppy regen is the most
likely way the single source of truth quietly breaks). This generator derives the
mechanical sections EXACTLY from true state, so the operator only writes the ~4
prose slots and never hand-types a SHA, a gate result, or a fill count.

GENERATED (never hand-type):
  - the static SESSION PROTOCOL header (carried through verbatim from the existing
    CURRENT_STATE.md so it stays self-maintaining)
  - Canonical pointer (SHA + session from LATEST.txt; predecessor chain from git log
    of crops_data_final.json, each commit's CONTENT sha + subject)
  - Gate record (whole_crop_gate per verified_gs_arc anchor + register gate)
  - Region fill state (walk each anchor's regions: filled cells / total + pause/2nd-plant)
  - Flip gates (read each anchor's launch_ready_core/seasoned + status)

HAND-WRITTEN SLOTS (emitted as `<!-- FILL: ... -->`): the headline line, "What just
happened", "Active work + next step", and the locked-decisions/guardrails block.

Usage (from repo root):
  python3 tools/gen_current_state.py            # prints the skeleton to stdout
  python3 tools/gen_current_state.py > CURRENT_STATE.md   # then fill the 4 prose slots
"""
import json, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "crops_data_final.json")
LATEST = os.path.join(ROOT, "LATEST.txt")
STATE = os.path.join(ROOT, "CURRENT_STATE.md")


def read_latest():
    sha = session = date = "?"
    for line in open(LATEST):
        if line.startswith("SHA:"):
            sha = line.split("SHA:", 1)[1].strip()
        elif line.startswith("Session:"):
            session = line.split("Session:", 1)[1].strip()
        elif line.startswith("Date:"):
            date = line.split("Date:", 1)[1].strip()
    return sha, session, date


def static_header():
    """Everything from the top of the existing file through the first `---` rule
    (the title + SESSION PROTOCOL block). Carried through verbatim so it stays in
    sync with whatever discipline is on disk."""
    if not os.path.exists(STATE):
        return "# plant -- CURRENT STATE (live surface)\n\n---\n"
    text = open(STATE).read()
    head, sep, _ = text.partition("\n---\n")
    return head + "\n---\n" if sep else text


def git_content_sha(commit):
    out = subprocess.run(["git", "show", f"{commit}:./crops_data_final.json"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        return None
    import hashlib
    return hashlib.sha256(out.stdout.encode()).hexdigest()


def predecessor_chain(n=7):
    log = subprocess.run(
        ["git", "log", f"-{n}", "--format=%h\t%s", "--", "crops_data_final.json"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip().splitlines()
    rows = []
    for line in log:
        commit, _, subject = line.partition("\t")
        csha = git_content_sha(commit)
        rows.append((csha[:8] if csha else commit, subject))
    return rows


def run_gate(slug):
    out = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, DATA],
                         capture_output=True, text=True).stdout
    line = next((l for l in out.splitlines() if l.startswith("GATE:")), "GATE: ?")
    viol = sum(1 for l in out.splitlines() if "VIOLATION:" in l)
    return ("PASS" if line.startswith("GATE: PASS") else "FAIL"), viol


def run_roster():
    out = subprocess.run([sys.executable, os.path.join(HERE, "register_completeness_gate.py"), DATA],
                         capture_output=True, text=True).stdout
    return "PASS" if "GATE: PASS" in out else "HALT"


def region_fill(crop):
    regions = crop.get("regions") or {}
    total = len(regions)
    filled = sum(1 for r in regions.values() if r.get("region_notes_seasoned"))
    heat = cold = second = 0
    for r in regions.values():
        for cell in (r.get("resolved_by_zone") or {}).values():
            if not isinstance(cell, dict):
                continue
            heat += "heat_pause" in cell
            cold += "cold_pause" in cell
            second += "second_planting" in cell
    return total, filled, heat, cold, second


def main():
    data = json.load(open(DATA))
    sha, session, date = read_latest()
    anchors = [c for c in data["crops"]
               if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]

    P = []  # output lines
    P.append(static_header())
    P.append("")
    P.append(f"<!-- FILL: headline -- one-line cert status. Derived facts: "
             f"{len(anchors)} of 9 anchors verified_gs_arc "
             f"({', '.join(c['slug'] for c in anchors)}); see Flip gates below. -->")
    P.append("")

    P.append("## Canonical pointer")
    P.append(f"- **Current SHA:** `{sha}`. `LATEST.txt` session: `{session}` ({date}).")
    P.append("- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):")
    for csha, subject in predecessor_chain():
        P.append(f"  - `{csha}` -- {subject}")
    P.append("")

    P.append("<!-- FILL: What just happened (this session -- what changed + why) -->")
    P.append("")
    P.append("<!-- FILL: Active work + next step / parked decisions -->")
    P.append("")

    P.append(f"## Gate record (generated {date}, on canonical `{sha[:8]}`)")
    for c in anchors:
        verdict, viol = run_gate(c["slug"])
        P.append(f"- **{c['slug']}: `{verdict}` ({viol})**")
    P.append(f"- **register_completeness_gate: `{run_roster()}`**")
    P.append("")

    P.append("## Region fill state (generated)")
    for c in anchors:
        total, filled, heat, cold, second = region_fill(c)
        extra = []
        if heat: extra.append(f"{heat} heat_pause")
        if cold: extra.append(f"{cold} cold_pause")
        if second: extra.append(f"{second} second_planting")
        tail = (" cells; " + ", ".join(extra)) if extra else " cells"
        P.append(f"- **{c['slug']}: {filled}/{total} region cells filled**{('; ' + ', '.join(extra)) if extra else ''}")
    P.append("")

    P.append("## Flip gates (generated)")
    certified = 0
    for c in anchors:
        vs = c.get("verification_status") or {}
        core = vs.get("launch_ready_core"); seas = vs.get("launch_ready_seasoned")
        st = vs.get("status")
        if core and seas and st == "verified_gs_arc":
            certified += 1
        P.append(f"- **{c['slug']}:** launch_ready_core={core} launch_ready_seasoned={seas} status=`{st}`")
    P.append(f"- **{certified} of 9 anchors certified** (launch_ready true + status `verified_gs_arc`).")
    P.append("")

    P.append("<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->")

    sys.stdout.write("\n".join(P) + "\n")


if __name__ == "__main__":
    main()
