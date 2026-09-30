#!/usr/bin/env python3
"""Integration test: whole_crop_gate A62 (PLA-607 sourced-block ratchet) and A63 (PLA-544 bare-host
sole citation), and their roster halves in gate_all, driven through the REAL ENTRY POINTS as
subprocesses on scratch copies of canonical. Run: python3 tools/test_gate_citation_ratchets_a62_a63.py

A driver that never reaches the guarded call site is vacuous (recurred three times in this repo),
so every injection here is read back out of the entry point's own output. Script-style: a failure
RAISES, never sys.exit.
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
CROP = "cabbage"
TMP = os.path.join(HERE, "_tmp_a62_a63_fixture.json")


def scratch(mutate=None):
    d = copy.deepcopy(base)
    if mutate:
        mutate({c["slug"]: c for c in d["crops"]}, d)
    with open(TMP, "w", encoding="utf-8") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    return TMP


def wcg(path, slug=CROP):
    r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, path],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def gate_all(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), path],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def empty_storage(idx, _d):
    idx[CROP]["storage"]["sources"] = []


def bare_storage(idx, _d):
    for m in idx[CROP]["storage"]["anchoring_urls"].values():
        m["url"] = "https://zz.edu"


POT_CROP = "plum"   # certified; container_notes.sources already WAIVED uncited, min_pot_gallons null


def pot_fifth(idx, _d):
    """The one case only the folded pot sub-rule can see. A NEW pot-uncited crop is otherwise
    already caught (sources kept + anchors emptied -> section F; sources emptied -> the general
    ratchet). But plum's container_notes is waived uncited BY IDENTITY, and giving it a figure
    does not change that identity, so the general ratchet stays silent. The pot rule does not."""
    idx[POT_CROP]["container_notes"]["min_pot_gallons"] = 25


try:
    # ---- clean: both blocks announced, the crop passes -------------------------------------
    rc, out = wcg(scratch())
    assert "A62. sourced-block identity ratchet" in out and "A63. bare-host sole citation" in out, out[-800:]
    assert "sourced-block-ratchet:" not in out and "bare-host:" not in out, out[-800:]
    assert rc == 0 and "GATE: PASS" in out, out[-800:]

    # ---- A62 reaches the entry point: [] on a cited block ----------------------------------
    rc, out = wcg(scratch(empty_storage))
    assert rc == 1 and f"sourced-block-ratchet: NEW uncited block {CROP}|storage|sources" in out, out[-800:]

    # ---- A62's folded pot sub-rule reaches the entry point ---------------------------------
    rc, out = wcg(scratch(pot_fifth), POT_CROP)
    assert rc == 1 and "is NOT one of the 4 known uncited crops" in out, out[-800:]
    assert "NEW uncited block" not in out and "anchoring:" not in out, (
        "the pot sub-rule must be the ONLY thing firing here, or this driver proves nothing")

    # ---- A63 reaches the entry point: the node's only citations made bare -------------------
    rc, out = wcg(scratch(bare_storage))
    assert rc == 1 and f"bare-host: NEW sole bare-host citation {CROP}|storage|anchoring_urls|" in out, out[-800:]

    # ---- gate_all: clean PASS reports both populations -------------------------------------
    rc, out = gate_all(scratch())
    assert rc == 0 and "gate_all: PASS" in out, out[-1200:]
    import re
    assert re.search(r"sourced-block ratchet \(PLA-607\): inspected \d+ named blocks, \d+ uncited, "
                     r"all waived by identity", out), out[-1200:]
    assert re.search(r"bare-host \(PLA-544\): inspected \d+ anchors, \d+ SOLE bare, all waived", out), out[-1200:]

    # ---- gate_all: each defect fails the roster run -----------------------------------------
    for mut, needle in ((empty_storage, f"{CROP}|storage|sources"),
                        (bare_storage, f"{CROP}|storage|anchoring_urls|")):
        rc, out = gate_all(scratch(mut))
        assert rc == 1 and CROP in out, (mut.__name__, out[-1200:])

    # ---- gate_all: the ROSTER branch, which no per-crop defect can reach --------------------
    # Every injection above fails whole_crop_gate first, so gate_all exits before its roster
    # block. The roster branch is reachable on exactly one path: the pot sub-rule's KNOWN/CEILING
    # DESYNC (plum added to POT_KNOWN, CEILING left at 4), where every crop passes and only the
    # count can fire. whole_crop_gate runs in its own processes, so the desync is written into a
    # SCRATCH COPY of tools/, not patched in-process, which the subprocesses would never see.
    import shutil, tempfile
    td = tempfile.mkdtemp(prefix="a62_ceiling_")
    try:
        for f in os.listdir(HERE):
            if f.endswith((".py", ".json")) and os.path.isfile(os.path.join(HERE, f)):
                shutil.copy2(os.path.join(HERE, f), td)
        gp = os.path.join(td, "sourced_block_ratchet_gate.py")
        src = open(gp, encoding="utf-8").read()
        anchor = '    "orange-navel",       # 15 gal\n'
        assert src.count(anchor) == 1, "POT_KNOWN anchor moved"
        open(gp, "w", encoding="utf-8").write(
            src.replace(anchor, anchor + f'    "{POT_CROP}",  # MUTATION-APPLIED desync\n'))
        assert "MUTATION-APPLIED desync" in open(gp, encoding="utf-8").read()
        r = subprocess.run([sys.executable, os.path.join(td, "gate_all.py"), scratch(pot_fifth)],
                           capture_output=True, text=True, cwd=REPO)
        out = r.stdout + r.stderr
        assert r.returncode == 1 and "ratchet ceiling is 4" in out, out[-1200:]
        assert "FAIL " + POT_CROP not in out, "the per-crop half must stay quiet on this path"
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- gate_all: an empty population is REFUSED by the ratchets, not passed ----------------
    def decertify(idx, _d):
        for c in idx.values():
            if isinstance(c.get("verification_status"), dict):
                c["verification_status"]["status"] = "draft"
    rc, out = gate_all(scratch(decertify))
    assert rc == 2 and "REFUSED -- sourced_block_ratchet_gate inspected 0 certified crops" in out, out[-800:]
finally:
    if os.path.exists(TMP):
        os.remove(TMP)

print("A62/A63 entry-point integration: all checks passed")
