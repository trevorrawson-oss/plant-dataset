#!/usr/bin/env python3
"""Integration test: whole_crop_gate A44 (PLA-10 planting_layout list + spacing mirrors), the
display-readiness and timing-spine changes that ride with it, and A44's roster half in gate_all,
driven through the REAL ENTRY POINTS as subprocesses on scratch copies of canonical.
Run: python3 tools/test_gate_planting_layout_a44.py

A driver that never reaches the guarded call site is vacuous, so every injection is read back out of
the entry point's own output. The post-promote SHAPE is proved end to end on two crops: a microgreen
in its promote-1 state (planting_layout [], spacing null, not_applicable) and cabbage with one cited
row entry, each through EVERY whole_crop_gate check, so a gate this arc forgot to teach about the new
shape fails here before it fails a promote. Script-style: a failure RAISES, never sys.exit.
"""
import copy, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
TMP = os.path.join(HERE, "_tmp_a44_fixture.json")
MG = "arugula-microgreens"
ROW = "cabbage"


def scratch(mutate=None):
    d = copy.deepcopy(base)
    if mutate:
        mutate({c["slug"]: c for c in d["crops"]}, d)
    with open(TMP, "w", encoding="utf-8") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    return TMP


def run(script, *args, tools=HERE):
    r = subprocess.run([sys.executable, os.path.join(tools, script), *args],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def tools_copy(edits):
    """A scratch tools/ with `edits` {file: (anchor, replacement)} applied; each anchor must match once."""
    td = tempfile.mkdtemp(prefix="a44_tools_")
    for f in os.listdir(HERE):
        if f.endswith((".py", ".json")) and os.path.isfile(os.path.join(HERE, f)):
            shutil.copy2(os.path.join(HERE, f), td)
    for f, (old, new) in edits.items():
        p = os.path.join(td, f)
        src = open(p, encoding="utf-8").read()
        assert src.count(old) == 1, f"{f}: anchor {old!r} matches {src.count(old)} times"
        open(p, "w", encoding="utf-8").write(src.replace(old, new + "  # MUTATION-APPLIED"))
        assert "MUTATION-APPLIED" in open(p, encoding="utf-8").read()
    return td


def microgreen_post(idx, _d):
    c = idx[MG]
    assert c.get("zone_independent") is True and c.get("spacing_inches") == []
    c.update(planting_layout=[], spacing_inches=None, row_spacing_inches=None,
             row_spacing_reason="not_applicable")


def cabbage_post(idx, _d):
    """One cited row entry, citing a source + url the crop ALREADY cites (so §F and A63 see a real,
    document-pathed anchor), mirrors set by the rule."""
    c = idx[ROW]
    sid, anc = next((s, a) for s, a in c["storage"]["anchoring_urls"].items())
    c.update(planting_layout=[{
        "id": "row-none", "arrangement": "row", "support": "none", "default": True,
        "in_row_inches": list(c["spacing_inches"]), "row_spacing_inches": [24, 36],
        "row_spacing_reason": None, "sources": [sid], "anchoring_urls": {sid: dict(anc)}}],
        row_spacing_inches=[24, 36], row_spacing_reason=None)


try:
    # ---- clean canonical: A44 announced unarmed, every crop it is run on passes ------------
    rc, out = run("whole_crop_gate.py", "sweet-corn", scratch())
    assert "A44. planting_layout list + spacing mirrors" in out and "presence off" in out, out[-800:]
    assert rc == 0 and "GATE: PASS" in out, out[-800:]

    # ---- A44 reaches the entry point: a legacy enum defect, and a list mirror defect -------
    def bad_enum(idx, _d):
        idx["sweet-corn"]["planting_layout"] = "blocks"
    rc, out = run("whole_crop_gate.py", "sweet-corn", scratch(bad_enum))
    assert rc == 1 and "planting_layout: sweet-corn: planting_layout 'blocks' not in" in out, out[-800:]

    def bad_mirror(idx, d):
        cabbage_post(idx, d)
        idx[ROW]["spacing_inches"] = [idx[ROW]["spacing_inches"][0], idx[ROW]["spacing_inches"][1] + 6]
    rc, out = run("whole_crop_gate.py", ROW, scratch(bad_mirror))
    assert rc == 1 and re.search(rf"planting_layout: {ROW}: spacing_inches \[.*\] is not the mirror", out), out[-800:]

    # ---- the post-promote SHAPE passes EVERY whole_crop_gate check --------------------------
    rc, out = run("whole_crop_gate.py", MG, scratch(microgreen_post))
    assert rc == 0 and "GATE: PASS" in out, ("microgreen post-shape", out[-1500:])
    rc, out = run("whole_crop_gate.py", ROW, scratch(cabbage_post))
    assert rc == 0 and "GATE: PASS" in out, ("cabbage post-shape", out[-1500:])

    # ... and the microgreen post-shape needs is_microgreen keyed on zone_independent: with the old
    # predicate (spacing == []) restored in a scratch tools/, the same crop goes red for sow depth.
    td = tools_copy({"timing_spine_gate.py": ('    return crop.get("zone_independent") is True',
                                              '    return crop.get("spacing_inches") == []')})
    try:
        rc, out = run("whole_crop_gate.py", MG, scratch(microgreen_post), tools=td)
        assert rc == 1 and "sow_depth" in out, ("old predicate must redden the null microgreen", out[-1200:])
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- arming reaches whole_crop_gate: PRESENCE_ARMED True reddens a legacy crop ---------
    td = tools_copy({"planting_layout_gate.py": ("PRESENCE_ARMED = False", "PRESENCE_ARMED = True")})
    try:
        rc, out = run("whole_crop_gate.py", "sweet-corn", scratch(), tools=td)
        assert rc == 1 and "presence ARMED" in out and "the string form is retired" in out, out[-1200:]
        rc, out = run("whole_crop_gate.py", "lemon", scratch(), tools=td)
        assert rc == 1 and "lemon: planting_layout absent/null on a certified crop" in out, out[-1200:]
        assert "spacing_inches_anchoring_urls is retired" in out, out[-1200:]
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- gate_all: clean PASS reports A44's population --------------------------------------
    rc, out = run("gate_all.py", scratch())
    assert rc == 0 and "gate_all: PASS" in out, out[-1200:]
    assert re.search(r"planting_layout \(PLA-10, A44\): inspected 121 certified crops, 0 entries; "
                     r"0 list-shaped, 6 legacy string; null spacing on 0; presence off", out), out[-1200:]

    # ---- gate_all: the ROSTER refusal, which no per-crop defect can reach ----------------------
    td = tools_copy({"planting_layout_gate.py": ("CERT_FLOOR = 121", "CERT_FLOOR = 122")})
    try:
        rc, out = run("gate_all.py", scratch(), tools=td)
        assert rc == 2 and ("REFUSED -- planting_layout_gate inspected 121 certified crops, below the "
                            "declared floor 122") in out, out[-1200:]
    finally:
        shutil.rmtree(td, ignore_errors=True)
finally:
    if os.path.exists(TMP):
        os.remove(TMP)

print("PASS A44 entry-point integration: all checks passed")
