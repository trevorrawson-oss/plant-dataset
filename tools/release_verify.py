#!/usr/bin/env python3
"""release_verify.py -- the thorough release-verification for a cell promote.

Codifies the structural checks that `whole_crop_gate.py` (a shape FLOOR) does
NOT cover, so a clean gate is never mistaken for a clean release. Catches the
gate's blind spots WITHOUT reading sources:

  A. collateral      -- only the target crop changed vs base; catalog delta; the
                        reference crop (lettuce) byte-identical; which cells moved.
  B. violation-diff  -- NEW vs CLEARED gate violations the change introduced.
  C. calendar coherence -- no silent `wait` gaps; heat_pause.months aligned with
                        the calendar's pause-months, per filled region cell.
  D. user-facing scan -- `--`/em-dash + spelled-"degrees F" in USER-FACING strings
                        (backend prose excluded, per CLAUDE.md); each hit classified.
  E. exemplar key-diff -- each filled region cell's key structure vs the reference
                        crop's same cell (catches novel keys + vestigial residue).
  F. region_notes    -- both registers present + non-null on every filled cell.

NOT this tool (deferred to Step 5/5.5 + Step 11): the 4-round source side-by-side
(is the biology TRUE), §3 cross-field, the verbatim/copyright scan. This tool
proves a cell is well-SHAPED + self-consistent + exemplar-matched, not correct.

Usage:
  python3 tools/release_verify.py <candidate.json> [--base <base.json>] \\
          [--slug cherry-tomato] [--ref lettuce-leaf]
  --base : if given, runs A + B (the diff checks). Omit to audit a file standalone.
Exit 1 on any CONCERN (so a bot can gate on it).
"""
import json, re, sys, subprocess, os, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from field_classification import is_backend  # the ONE shared backend predicate
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
EMDASH = chr(8212)
PAUSE_TOKENS = {"heat_pause", "cold_pause", "season_over"}

concerns = []   # hard -> block the release
notes = []      # review items surfaced for Step 5/5.5 -> do NOT block
def concern(msg): concerns.append(msg); print(f"  CONCERN: {msg}")
def note(msg): notes.append(msg); print(f"  review (Step 5.5): {msg}")
def ok(msg): print(f"  ok: {msg}")


def load(p): return json.load(open(p))
def crop(data, slug): return next(c for c in data["crops"] if c.get("slug") == slug)


def gate(path, slug):
    out = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, path],
                         capture_output=True, text=True).stdout
    viols = set(l.strip() for l in out.splitlines() if "VIOLATION:" in l)
    final = next((l for l in out.splitlines() if l.startswith("GATE:")), "GATE: ?")
    return viols, final


def scan_user_facing(o, path="", key=""):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            hits += scan_user_facing(v, f"{path}.{k}", k)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            hits += scan_user_facing(x, f"{path}[{i}]", key)  # list items inherit parent key
    elif isinstance(o, str):
        flag = ("--" in o or EMDASH in o or re.search(r"\bdegrees?\s*F\b", o))
        if flag and not is_backend(key, path):
            hits.append((path, o[:60]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--base")
    ap.add_argument("--slug", default="cherry-tomato")
    ap.add_argument("--ref", default="lettuce-leaf")
    a = ap.parse_args()

    cand = load(a.candidate)
    c = crop(cand, a.slug)
    ref = crop(cand, a.ref)
    regions = c.get("regions") or {}
    refregions = ref.get("regions") or {}

    if a.base:
        print("A. collateral (vs base)")
        base = load(a.base)
        changed = [x["slug"] for x, y in zip(cand["crops"], base["crops"]) if x != y]
        if changed == [a.slug]: ok(f"only {a.slug} changed among crops")
        else: concern(f"crops changed = {changed} (expected only {a.slug})")
        tl = [k for k in cand if k != "crops" and cand[k] != base.get(k)]
        cat_delta = sorted(set(cand["source_catalog"]) - set(base["source_catalog"]))
        cat_gone = sorted(set(base["source_catalog"]) - set(cand["source_catalog"]))
        print(f"  top-level(non-crops) changed: {tl} | catalog +{cat_delta or 'none'} -{cat_gone or 'none'}")
        if cat_gone: concern(f"catalog entries DROPPED: {cat_gone}")
        rb = crop(base, a.ref); rc = crop(cand, a.ref)
        if rb == rc: ok(f"reference crop {a.ref} byte-identical")
        else: concern(f"reference crop {a.ref} CHANGED")
        bc = crop(base, a.slug)
        cell_changed = [r for r in regions if regions[r] != (bc.get("regions") or {}).get(r)]
        print(f"  {a.slug} regions changed: {cell_changed}")

        print("B. violation-diff (vs base)")
        vb, _ = gate(a.base, a.slug); vc, _ = gate(a.candidate, a.slug)
        new = sorted(vc - vb)
        if new: concern(f"NEW violations introduced: {new}")
        else: ok("no new violations introduced")
        print(f"  cleared: {sorted(vb - vc) or 'none'}")

    print("Gate (candidate)")
    vc, final = gate(a.candidate, a.slug)
    print(f"  {a.slug}: {final}")
    _, reffinal = gate(a.candidate, a.ref)
    if reffinal.startswith("GATE: PASS"): ok(f"reference {a.ref}: {reffinal.split('(')[0].strip()}")
    else: concern(f"reference {a.ref} not PASS: {reffinal}")

    print("C. calendar coherence (filled cells)")
    cohere_clean = True
    for r, cell in regions.items():
        for z, zc in (cell.get("resolved_by_zone") or {}).items():
            cal = zc.get("calendar")
            if not isinstance(cal, list) or len(cal) != 12:
                continue  # unfilled / no calendar
            # heat_pause object must match the calendar's heat_pause months: a true
            # incoherence (the two were authored independently) -> HARD concern.
            hp = (zc.get("heat_pause") or {}).get("months")
            if hp is not None:
                cal_hp = [i + 1 for i in range(12) if cal[i] == "heat_pause"]
                if sorted(hp) != sorted(cal_hp):
                    concern(f"{r}.z{z}: heat_pause.months {sorted(hp)} != calendar heat_pause {sorted(cal_hp)} (INCOHERENT)")
                    cohere_clean = False
            # a `wait` is a pause-legibility REVIEW item (Step 5.5 classifies it as a
            # legit between-window gap or a cold/heat_pause). Surfaced, not blocking.
            waits = [MON[i] for i in range(12) if cal[i] == "wait"]
            if waits:
                note(f"{r}.z{z}: `wait` months {waits} -- pause-legibility (legit gap vs cold/heat_pause?)")
                cohere_clean = False
    if cohere_clean:
        ok("all filled calendars coherent (no waits; heat_pause aligned)")

    print("D. user-facing dash / spelled-degrees scan")
    hits = scan_user_facing(c)
    if hits:
        for p, s in hits: concern(f"user-facing dash/temp: {p}: {s!r}")
    else: ok("no `--`/em-dash/spelled-degrees in any user-facing string")

    print("E. exemplar key-diff (filled cells vs reference)")
    for r, cell in regions.items():
        if not cell.get("region_notes_seasoned"):
            continue  # only check filled cells
        rcell = refregions.get(r)
        if not rcell:
            continue
        novel = sorted(set(cell) - set(rcell))
        # an EMPTY `sources_pending_admission` is benign scaffold residue (nothing
        # pending -> gate-invisible); note it, do not fail the release on it.
        benign = [k for k in novel if k == "sources_pending_admission" and not cell.get(k)]
        real = [k for k in novel if k not in benign]
        if benign: print(f"  note: {r}: vestigial empty {benign} (benign scaffold residue)")
        if real: concern(f"{r}: novel region keys vs {a.ref}: {real}")
    if not any("novel region keys" in m for m in concerns):
        ok("no novel (non-benign) keys vs reference on any filled cell")

    print("F. region_notes presence")
    missing = [r for r, cell in regions.items()
               if cell.get("region_notes_seasoned") and not cell.get("region_notes_beginner")]
    if missing: concern(f"region_notes_beginner missing where seasoned present: {missing}")
    else: ok("every cell with seasoned notes has beginner notes")

    # G. exemplar value-divergence -- the "byte-identical to <ref>" smell.
    # SHAPE should match the exemplar (checked in E); biological VALUES (calendar
    # tokens, heat_pause months) must be derived from the CROP's own sources. A value
    # byte-identical to the reference is either a legit convergence (must be attested
    # "independently derived, why it converges") or a PASTE. Surfaced, NOT blocked --
    # but every identical value must carry an own-source justification in the entry.
    # This also catches a loose "identical to <ref>" CLAIM that is actually false: if
    # the entry says identical but a cell shows up here as DIFFERS, the claim is wrong.
    print(f"G. exemplar value-divergence (calendar/heat_pause identity vs {a.ref})")
    ident = []
    for r, cell in regions.items():
        rcell = refregions.get(r)
        if not rcell:
            continue
        for z, zc in (cell.get("resolved_by_zone") or {}).items():
            rzc = (rcell.get("resolved_by_zone") or {}).get(z)
            if not rzc:
                continue
            cal, rcal = zc.get("calendar"), rzc.get("calendar")
            if isinstance(cal, list) and cal == rcal:
                ident.append(f"{r}.z{z}.calendar")
            hp = (zc.get("heat_pause") or {}).get("months")
            rhp = (rzc.get("heat_pause") or {}).get("months")
            if hp is not None and hp == rhp:
                ident.append(f"{r}.z{z}.heat_pause.months={hp}")
    if ident:
        note(f"value-IDENTICAL to {a.ref} -- attest each as independently-derived, NOT pasted: {ident}")
    else:
        ok(f"no region calendar/heat_pause byte-identical to {a.ref} (all crop-specific values)")

    # H. shared chill-delivered table (dataset-wide, slug-independent). The F2 refactor moved
    # chill-delivered into one crop-invariant region_chill_delivered table; its [lo,hi] shape is
    # validated here so a malformed (or string-typed) cell cannot ship.
    print("H. shared chill-delivered table (region_chill_delivered shape)")
    from chill_gate import chill_table_violations
    ctv = chill_table_violations(cand)
    if ctv:
        for v in ctv:
            concern(f"chill table: {v}")
    else:
        ok("region_chill_delivered is a well-formed region -> zone -> [lo,hi] table")

    print()
    if notes:
        print(f"  ({len(notes)} review note(s) above -- Step 5/5.5 items, NON-blocking)")
    if concerns:
        print(f"RELEASE-VERIFY: {len(concerns)} CONCERN(S) -- block + review before promoting")
        sys.exit(1)
    print("RELEASE-VERIFY: clean -- no blocking concerns (structural + consistency; biology + pause-legibility are Step 5)")


if __name__ == "__main__":
    main()
