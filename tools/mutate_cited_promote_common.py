#!/usr/bin/env python3
"""mutate_cited_promote_common -- mutation harness for the shared cited-promote module (housekeeping kickoff 60,
ruling 5, 2026-10-03).

WHAT IT PROVES. Two guards ship with the consolidation, and each must redden on the defect it exists for:
  REPLAY  (test_pla10_promote_replays.py): a change to a shared reader that moves a single verdict or a single
          byte of any PLA-10 promote's post-state reddens that promote's real-stage replay.
  SURFACE (test_cited_promote_common.py): a promote that stops importing the module, redefines a shared name,
          or reads through the old module; a shim that stops re-exporting a name; a module helper missing
          from SHARED.
WHAT IT DOES NOT CLAIM. A mutation that only disables a REFUSAL (a guard that never fires on the happy path)
cannot move a replay's bytes; those guards are driven by each promote's own suite and harness
(mutate_pla10_promote1/2/3.py), whose COM / helper anchors target this module. Mutations here are chosen to
change happy-path behavior, and each is named for the reader it breaks.

PLA-215 bar: one defect per guard family, injected into a SCRATCH COPY of tools/. Liveness: an anchor preflight
(every anchor matches exactly once, or HARNESS DEAD), a MUTATION-APPLIED marker re-read from disk, a SENTINEL
that must redden, and a POSITIVE CONTROL that runs every driver file WHOLE and unmutated. A pytest rc 5
(nothing collected) is graded BROKEN. The runner is mutate_pla10_promote2.py's, copied unchanged.

Usage: mutate_cited_promote_common.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5

RT = "test_pla10_promote_replays.py"
CT = "test_cited_promote_common.py"
SCRIPTS = set()
CPC = "cited_promote_common.py"
SHIM = "pla10_promote_common.py"
P2 = "promote_pla10_promote2.py"
P3 = "promote_pla10_promote3.py"
R1, R2, R3 = "test_promote_1_reproduces_cf1d480d", "test_promote_2_reproduces_31b766e8", \
    "test_promote_3_reproduces_b331e5f2"

# (name, target, old, new, driver file, pytest -k selector)
MUTATIONS = [
    # ---- REPLAY: the shared readers, each changing happy-path output -------------------------------
    ("r_serialize_escapes_unicode", CPC,
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=True).encode("utf-8")', RT, R3),
    ("r_quote_states_feet_dropped", CPC, "    return bool(ends & nums) or bool({x / 12 for x in ends} & nums)",
     "    return bool(ends & nums)", RT, R2),
    ("r_pdf_text_empty", CPC, '    return "\\n".join((page.extract_text() or "") for page in reader.pages)',
     '    return ""', RT, R3),
    ("r_manifest_url_misread", CPC, '            rows.setdefault(r["sha256"], set()).add(r["url"])',
     '            rows.setdefault(r["sha256"], set()).add(r["url"].upper())', RT, R2),
    ("r_set_at_noop", CPC, "    node[concrete[-1]] = value", "    pass", RT, R3),
    # fmt is NOT replay-observable: every promote decision compares fmt output with fmt output, and the real
    # stage's paths enter through parse_path, so ANY injective change to fmt preserves every verdict and every
    # byte (measured 2026-10-03: r_fmt_path_syntax survived a replay). It is not EQUIVALENT: fmt must invert
    # parse_path, and the suites build stage paths FROM scanner output, so a changed syntax breaks the round
    # trip (105 of 260 suite tests redden on it). Guarded there, by the promote 3 suite:
    ("x_fmt_not_parse_paths_inverse", CPC,
     '    return "".join(f"[{s}]" if isinstance(s, int) else (f".{s}" if i else s) for i, s in enumerate(concrete))',
     '    return "".join(f"({s})" if isinstance(s, int) else (f".{s}" if i else s) for i, s in enumerate(concrete))',
     "test_promote_pla10_promote3.py", "test_width_words_scan_only_when_a_spread_is_authored"),
    ("r_parse_path_index_shift", CPC, "            out.append(int(m.group(2)))",
     "            out.append(int(m.group(2)) + 1)", RT, R3),
    ("r_spacing_scanner_blind", CPC, "                if DIST.search(sent) and SPACING_WORD.search(sent):",
     "                if False:", RT, R2),
    ("r_t4_tolerance_zero", CPC, "TOL_FT = 0.00005", "TOL_FT = 0.0", RT, R3),
    ("r_t4_height_read_as_width", CPC, '    (re.compile(r"(?:tall|high|in\\s+height)\\b"), "H"),',
     '    (re.compile(r"(?:tall|high|in\\s+height)\\b"), "W"),', RT, R3),
    # ---- SURFACE: the consolidation itself ---------------------------------------------------------
    ("s_promote_reads_the_old_module", P3, "from cited_promote_common import (",
     "from pla10_promote_common import (", CT, "test_every_promote_imports_the_shared_module"),
    ("s_promote_redefines_a_helper", P2, "\n\ndef load_canonical(", "\n\ndef compact(v):\n    return repr(v)\n\n\ndef load_canonical(",
     CT, "test_no_promote_redefines_a_shared_name"),
    ("s_shim_drops_a_name", SHIM, "    quote_states_ft,", "", CT, "test_the_shim_reexports_every_name_by_identity"),
    ("s_shim_defines_its_own", SHIM, "    quote_states_ft,\n)\n", "    quote_states_ft,\n)\n\n\ndef norm_text(s):\n    return s\n",
     CT, "test_the_shim_defines_nothing_of_its_own"),
    ("s_module_helper_not_in_shared", CPC, "\n\ndef fmt(concrete):", "\n\ndef _stray():\n    pass\n\n\ndef fmt(concrete):",
     CT, "test_shared_is_the_whole_module_surface"),
]
SENTINEL = (RT, '    "P3": "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d",',
            '    "P3": "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38e",', R3)


def run_driver(tools, f, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if f in SCRIPTS:
        cmd = [sys.executable, "-B", os.path.join(tools, f)]
    else:
        cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, f), "-q", "-x", "--no-header",
               "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new + "  " + MARKER if "\n" not in new
                                                       else new.replace("\n", "  " + MARKER + "\n", 1), 1))
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_cpc_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        bad = [n for n, t, old, *_ in muts if open(os.path.join(tools, t), encoding="utf-8").read().count(old) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        for f in sorted({m[4] for m in muts}):
            rc, out = run_driver(tools, f, None)
            if rc != 0:
                print(out[-2000:])
                sys.exit(f"HARNESS DEAD: the unmutated driver {f} is already failing (rc {rc})")
        print(f"positive control: every driver file WHOLE and unmutated is GREEN "
              f"({len({m[4] for m in muts})} files)")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, f, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc in (0, NOTHING_COLLECTED):
            sys.exit(f"HARNESS DEAD: the sentinel did not redden (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, target, old, new, drv, sel in muts:
            clean, err = apply(tools, target, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, _ = run_driver(tools, drv, sel)
            open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append(name); print(f"  BROKEN   {name}: driver collected nothing")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  ({drv} {sel or '(script)'})")
            else:
                caught.append(name); print(f"  caught   {name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
