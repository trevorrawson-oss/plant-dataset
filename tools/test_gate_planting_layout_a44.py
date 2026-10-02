#!/usr/bin/env python3
"""Integration test: whole_crop_gate A44 (PLA-10 planting_layout list + spacing mirrors), the
display-readiness and timing-spine changes that ride with it, and A44's roster half in gate_all,
driven through the REAL ENTRY POINTS as subprocesses on scratch copies of canonical.
Run: python3 tools/test_gate_planting_layout_a44.py

A driver that never reaches the guarded call site is vacuous, so every injection is read back out of
the entry point's own output. Re-measured for promote 1's DATA commit (A44 ARMED): the live canonical
carries the post-promote shape, so a row crop, a block crop, a hill default, apple and a microgreen
(planting_layout [], spacing null, not_applicable) each pass EVERY whole_crop_gate check, and the
legacy string form, an absent layout and the retired anchor key each redden. Script-style: a failure
RAISES, never sys.exit.
"""
import copy, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
base_idx = {c["slug"]: c for c in base["crops"]}
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


def entry_of(idx, slug):
    return idx[slug]["planting_layout"][0]


# Re-measured 2026-10-01 for PLA-10 promote 1's DATA commit: canonical now carries the post-promote
# shape on every certified crop and A44 is ARMED (planting_layout_gate.PRESENCE_ARMED = True). The
# tools-commit version built that shape by hand on a pre-promote base; here the base IS the shape.
try:
    # ---- clean canonical: A44 announced armed, the post-promote shape passes EVERY check --------
    for slug in ("sweet-corn", MG, ROW, "watermelon", "apple"):
        rc, out = run("whole_crop_gate.py", slug, scratch())
        assert "A44. planting_layout list + spacing mirrors" in out and "presence ARMED" in out, (slug, out[-800:])
        assert rc == 0 and "GATE: PASS" in out, (slug, out[-1500:])
    assert base_idx[MG]["spacing_inches"] is None and base_idx[MG]["planting_layout"] == []
    assert base_idx["watermelon"]["planting_layout"][0]["arrangement"] == "hill"  # a hill default, live

    # ---- A44 reaches the entry point: an entry enum defect, a mirror defect, the string form ----
    def bad_enum(idx, _d):
        entry_of(idx, "sweet-corn")["arrangement"] = "blocks"
    rc, out = run("whole_crop_gate.py", "sweet-corn", scratch(bad_enum))
    assert rc == 1 and "arrangement 'blocks' not in" in out, out[-800:]

    def bad_mirror(idx, _d):
        idx[ROW]["spacing_inches"] = [idx[ROW]["spacing_inches"][0], idx[ROW]["spacing_inches"][1] + 6]
    rc, out = run("whole_crop_gate.py", ROW, scratch(bad_mirror))
    assert rc == 1 and re.search(rf"planting_layout: {ROW}: spacing_inches \[.*\] is not the mirror", out), out[-800:]

    def legacy_string(idx, _d):
        idx["sweet-corn"]["planting_layout"] = "block"
    rc, out = run("whole_crop_gate.py", "sweet-corn", scratch(legacy_string))
    assert rc == 1 and "the string form is retired" in out, out[-1200:]

    def lemon_absent(idx, _d):
        del idx["lemon"]["planting_layout"]
        idx["lemon"]["spacing_inches_anchoring_urls"] = {}
    rc, out = run("whole_crop_gate.py", "lemon", scratch(lemon_absent))
    assert rc == 1 and "lemon: planting_layout absent/null on a certified crop" in out, out[-1200:]
    assert "spacing_inches_anchoring_urls is retired" in out, out[-1200:]

    # ... and the microgreen's null spacing needs is_microgreen keyed on zone_independent: with the old
    # predicate (spacing == []) restored in a scratch tools/, the live microgreen goes red for sow depth.
    td = tools_copy({"timing_spine_gate.py": ('    return crop.get("zone_independent") is True',
                                              '    return crop.get("spacing_inches") == []')})
    try:
        rc, out = run("whole_crop_gate.py", MG, scratch(), tools=td)
        assert rc == 1 and "sow_depth" in out, ("old predicate must redden the null microgreen", out[-1200:])
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- the arming is what refuses the string: DISARMED, the same legacy string passes -----------
    td = tools_copy({"planting_layout_gate.py": ("PRESENCE_ARMED = True", "PRESENCE_ARMED = False")})
    try:
        rc, out = run("whole_crop_gate.py", "sweet-corn", scratch(legacy_string), tools=td)
        assert rc == 0 and "presence off" in out, ("disarmed, a valid legacy string passes", out[-1200:])
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- gate_all: clean PASS reports A44's population --------------------------------------
    rc, out = run("gate_all.py", scratch())
    assert rc == 0 and "gate_all: PASS" in out, out[-1200:]
    assert re.search(r"planting_layout \(PLA-10, A44\): inspected 121 certified crops, 119 entries; "
                     r"121 list-shaped, 0 legacy string; null spacing on 8; presence ARMED", out), out[-1200:]

    # ---- gate_all: the ROSTER refusals, which no per-crop defect can reach ----------------------
    td = tools_copy({"planting_layout_gate.py": ("CERT_FLOOR = 121", "CERT_FLOOR = 122")})
    try:
        rc, out = run("gate_all.py", scratch(), tools=td)
        assert rc == 2 and ("REFUSED -- planting_layout_gate inspected 121 certified crops, below the "
                            "declared floor 122") in out, out[-1200:]
    finally:
        shutil.rmtree(td, ignore_errors=True)
    td = tools_copy({"planting_layout_gate.py": ("ENTRY_FLOOR = 113", "ENTRY_FLOOR = 120")})
    try:
        rc, out = run("gate_all.py", scratch(), tools=td)
        assert rc == 2 and "REFUSED" in out and "119" in out, ("armed entry floor", out[-1200:])
    finally:
        shutil.rmtree(td, ignore_errors=True)

    # ---- T2 (PLA-10 promote 2, 2026-10-02): the rootstock override key reaches the entry points ----
    # Unarmed in the tools commit: the shape rules hold on any crop carrying the key; arming (promote 2's
    # data commit) adds presence on apple and the 5-row floor. apple's owed NCSU overrides, cited per row.
    NC = "ncsu_ext_handbook_tree_fruit"
    NC_A = {"url": "https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts",
            "verified": "2026-10-02"}
    OWED = {"M9": [48, 96], "M26": None, "MM106": [144, 192], "MM111": [168, 216], "seedling": [216, 300]}

    def overrides(drop=None, uncite=None):
        def m(idx, _d):
            for r in idx["apple"]["rootstock_options"]:
                if r["name"] == drop:
                    continue
                r["spacing_inches"] = OWED[r["name"]]
                if OWED[r["name"]] is not None and r["name"] != uncite:
                    r["sources"] = r["sources"] + [NC]
                    r["anchoring_urls"][NC] = dict(NC_A)
                if r["name"] == uncite:
                    r["sources"], r["anchoring_urls"] = [], {}
        return m

    rc, out = run("whole_crop_gate.py", "apple", scratch(overrides()))
    assert rc == 0 and "GATE: PASS" in out, ("clean overrides pass unarmed", out[-1500:])
    rc, out = run("whole_crop_gate.py", "apple", scratch(overrides(drop="MM111")))
    assert rc == 1 and "apple: rootstock_options spacing_inches is on 4 of 5 rows; all-or-none" in out, out[-1200:]
    rc, out = run("whole_crop_gate.py", "apple", scratch(overrides(uncite="MM106")))
    assert rc == 1 and "rootstock_options[2] (MM106): spacing_inches [144, 192] but the row cites no source" in out, \
        out[-1200:]
    td = tools_copy({"planting_layout_gate.py": ("ROOTSTOCK_OVERRIDE_ARMED = False", "ROOTSTOCK_OVERRIDE_ARMED = True")})
    try:
        rc, out = run("whole_crop_gate.py", "apple", scratch(), tools=td)
        assert rc == 1 and "apple: no rootstock_options[].spacing_inches; the override key is armed" in out, \
            ("armed, live apple (no overrides) reddens", out[-1200:])
        rc, out = run("gate_all.py", scratch(overrides()), tools=td)
        assert rc == 0 and "gate_all: PASS" in out and "rootstock overrides on 1 crop(s), 5 row(s), ARMED" in out, \
            ("armed, apple's 5 rows pass gate_all and are reported", out[-1500:])
    finally:
        shutil.rmtree(td, ignore_errors=True)
finally:
    if os.path.exists(TMP):
        os.remove(TMP)

print("PASS A44 entry-point integration: all checks passed")
