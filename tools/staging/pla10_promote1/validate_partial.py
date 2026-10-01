#!/usr/bin/env python3
"""validate_partial -- PLA-10 promote 1 SESSION helper: run the promote's per-crop guards on the crops staged
SO FAR (the promote's own --check refuses on the fixed list until all 113 are staged).  Imports the promote and
reuses its functions; nothing here writes.  NOT a gate: session 3 runs the real --check.

Usage: validate_partial.py [--stage DIR] [--evidence DIR] [--only slug,slug]
Exit 0 iff every staged crop passes guards 2 (evidence), 3 (retired anchors), 4 (restatements), 6 (A44 armed per
crop + A62 + A63 + numeric_sanity + display_readiness) and the stage keys are well-formed (load_stage).
"""
import argparse, copy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, TOOLS)
import promote_pla10_planting_layout as P  # noqa: E402
import planting_layout_gate as PLG  # noqa: E402
import sourced_block_ratchet_gate as SBR  # noqa: E402
import bare_host_gate as BH  # noqa: E402
import numeric_sanity_gate as NS  # noqa: E402
import display_readiness_gate as DR  # noqa: E402


def apply_subset(pre, stage):
    post = copy.deepcopy(pre)
    for c in post["crops"]:
        s = stage.get(c["slug"])
        if s is None:
            continue
        entries = copy.deepcopy(s["planting_layout"])
        c["planting_layout"] = entries
        c["spacing_inches"] = PLG.expected_spacing(entries)
        d = PLG.default_entry(entries)
        c["row_spacing_inches"] = d.get("row_spacing_inches") if d else None
        c["row_spacing_reason"] = PLG.expected_row_reason(c)
        c.pop(P.RETIRED, None)
        for name, sp in (s.get("rootstock_spacing") or {}).items():
            row = next(r for r in c.get("rootstock_options") or [] if r.get("name") == name)
            row["spacing_inches"] = sp
        for ed in s.get("edits") or []:
            P.set_at(c, P.resolve(c, ed["path"]), ed["new"])
    return post


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default=P.STAGE)
    ap.add_argument("--evidence", default=P.EVIDENCE)
    ap.add_argument("--only", default=None)
    a = ap.parse_args(argv)
    pre = P.load_canonical()
    stage, ev = P.load_stage(a.stage)
    if a.only:
        keep = set(a.only.split(","))
        stage = {k: v for k, v in stage.items() if k in keep}
        ev = [r for r in ev if r["crop"] in keep]
    pidx = P.by_slug(pre)
    if not stage:
        print("REFUSED: 0 crops staged; nothing inspected"); return 2
    problems = []
    # pre-side checks the promote makes per crop
    for slug, s in stage.items():
        c = pidx.get(slug)
        if c is None or not P.certified(c) or c.get("zone_independent") is True:
            problems.append(f"{slug}: not a certified non-zone_independent crop"); continue
        if (P.RETIRED in c) != ("retired_anchor" in s):
            problems.append(f"{slug}: retired_anchor is required iff the crop carries {P.RETIRED}")
        if ("rootstock_spacing" in s) != (slug in P.ROOTSTOCK_CROPS):
            problems.append(f"{slug}: rootstock_spacing is apple's alone")
        for ed in s.get("edits") or []:
            if set(ed) != {"path", "new", "reason"} or not str(ed["reason"]).strip():
                problems.append(f"{slug}: malformed edit {ed}")
            else:
                try:
                    P.resolve(c, ed["path"])
                except Exception as e:  # noqa
                    problems.append(f"{slug}: edit path {ed['path']!r} does not resolve: {e}")
    post = apply_subset(pre, stage)
    qidx = P.by_slug(post)
    # guard 3
    for slug, s in stage.items():
        if P.RETIRED not in pidx[slug]:
            continue
        disp = s.get("retired_anchor") or {}
        old = pidx[slug][P.RETIRED]
        if set(disp) != set(old):
            problems.append(f"{slug}: retired_anchor names {sorted(disp)}, base anchors {sorted(old)}")
        for sid, how in disp.items():
            if how == "moved":
                if not any((e.get("anchoring_urls") or {}).get(sid, {}).get("url") == old.get(sid, {}).get("url")
                           for e in qidx[slug]["planting_layout"]):
                    problems.append(f"{slug}: {sid} marked moved but no entry anchors {old.get(sid, {}).get('url')}")
            elif not (isinstance(how, dict) and set(how) == {"dropped"} and str(how["dropped"]).strip()):
                problems.append(f"{slug}: {sid} disposition must be 'moved' or {{'dropped': reason}}")
    # guard 4
    for slug, s in stage.items():
        a_, b_ = pidx[slug], qidx[slug]
        moved = P.compact(a_.get("spacing_inches")) != P.compact(b_.get("spacing_inches")) or slug in P.ROOTSTOCK_CROPS
        if not moved:
            continue
        adj = {}
        for r in s.get("restatements") or []:
            if set(r) != {"path", "verdict", "note"} or r["verdict"] not in ("agrees", "edited") or not str(r["note"]).strip():
                problems.append(f"{slug}: malformed restatement {r}"); continue
            adj[P.fmt(P.resolve(a_, r["path"]))] = r["verdict"]
        edited = {P.fmt(P.resolve(a_, ed["path"])) for ed in s.get("edits") or []}
        for p in P.spacing_strings(a_):
            if p not in adj:
                problems.append(f"{slug}: spacing moves {P.compact(a_.get('spacing_inches'))} -> "
                                f"{P.compact(b_.get('spacing_inches'))}; restatement at {p} not adjudicated")
            elif adj[p] == "edited" and p not in edited:
                problems.append(f"{slug}: {p} adjudicated 'edited' but no edit touches it")
    # guard 2
    n_ev = 0
    try:
        n_ev = P.check_evidence(qidx, stage, ev, post.get("source_catalog") or {}, a.evidence)
    except P.Refused as e:
        problems.append(f"evidence: {e}")
    # guard 6 per crop
    for slug in stage:
        c = qidx[slug]
        v = PLG.check_crop(c, armed=True)
        if v:
            problems.append(f"{slug}: A44 {v[:4]}")
        v = NS.numeric_sanity_violations(c) + DR.display_readiness_violations(c)
        if v:
            problems.append(f"{slug}: numeric_sanity / display_readiness {v[:3]}")
    v = SBR.roster(post)[3]
    v = [x for x in v if any(str(x).startswith(s) or f" {s} " in str(x) or f"{s}:" in str(x) for s in stage)]
    if v:
        problems.append(f"A62: {v[:5]}")
    v = BH.roster(post)[4]
    v = [x for x in v if any(s in str(x) for s in stage)]
    if v:
        problems.append(f"A63: {v[:5]}")
    print(f"staged {len(stage)} crop(s), {len(ev)} evidence row(s) read, {n_ev} (entry, field) figures covered")
    moved = [s for s in stage if P.compact(pidx[s].get("spacing_inches")) != P.compact(qidx[s].get("spacing_inches"))]
    print(f"figure moves on {len(moved)}: {moved}")
    if problems:
        print(f"PROBLEMS ({len(problems)}):")
        for p in problems:
            print("  -", p)
        return 1
    print("OK: every staged crop passes the per-crop guards (fixed list NOT checked here)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
