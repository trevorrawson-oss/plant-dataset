#!/usr/bin/env python3
"""Integration test: whole_crop_gate A61 (critical_warnings + container_safety) fires on a scratch
fixture and is a no-op on a canonical carrying neither key. Run: python3 tools/test_gate_critical_warnings_a61.py

The A59/A60 pattern: drive the gate through the REAL ENTRY POINT (whole_crop_gate as a subprocess),
not through the gate function, because a driver that never reaches the guarded call site is vacuous
and that has recurred three times in this repo. Script-style: a failure RAISES, never sys.exit.

The fixture is live canonical, deliberately, because the last block asserts the PRESENCE flag agrees
with the data (the floor arms in the commit that writes the keys). Every injection targets a crop
the PLA-581 promote leaves null, so the test holds on both sides of that write.
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))
URL = "https://extension.illinois.edu/container-gardens/container-size"
REC = {"field": "critical_warnings", "date": "2026-09-23", "sources": ["uiuc_ext"], "note": "test"}


def entry(**kw):
    e = {"id": "a-full-pot-is-heavy", "class": "safety", "severity": "high", "stage": None,
         "title": "A full pot is heavy", "body_seasoned": "Wet mix is heavy; ask an architect.",
         "body_beginner": "Wet soil is heavy; ask the owner first.", "sources": ["uiuc_ext"],
         "anchoring_urls": {"uiuc_ext": {"url": URL, "verified": "2026-09-23"}}}
    e.update(kw)
    return e


def gate(slug, mutate=None, mutate_data=None):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    if mutate:
        mutate(c)
    if mutate_data:
        mutate_data(d)
    tmp = os.path.join(HERE, "_tmp_a61_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


def put(value, record=True):
    def m(c):
        c["critical_warnings"] = value
        if record:
            vs = c["verification_status"]
            vs["field_additions"] = list(vs.get("field_additions") or []) + [REC]
    return m


CROP = "basil"
bc = next(c for c in base["crops"] if c["slug"] == CROP)
assert bc["verification_status"]["status"] == "verified_gs_arc" and bc.get("critical_warnings") is None \
    and not any(x.get("field") == "critical_warnings" for x in bc["verification_status"].get("field_additions") or []), \
    f"{CROP} is no longer a clean fixture; pick a certified crop carrying no critical_warnings value or record"

# The block is present and announced, and the crop as it stands is clean.
out = gate(CROP)
assert "A61. critical_warnings" in out, "A61 block missing from whole_crop_gate"
assert "critical-warnings:" not in out, out

# THE THREE STATES reach the entry point and are reported as distinct states.
out = gate(CROP, put(None, record=False))
assert "critical-warnings:" not in out and "critical_warnings state: null" in out, out
out = gate(CROP, put([]))
assert "critical-warnings:" not in out and "critical_warnings state: empty" in out, out
out = gate(CROP, put([entry()]))
assert "critical-warnings:" not in out and "critical_warnings state: authored" in out, out

# null -> [] WITH NO RECORD: the collapse the three-state rule exists to stop, through the real gate.
out = gate(CROP, put([], record=False))
assert "critical-warnings:" in out and "assessed, none found" in out, out

# The wrong type; a stage off this crop's ladder; a duplicated id; an unknown class.
out = gate(CROP, put("none"))
assert "critical-warnings:" in out and "null, [] or a non-empty list" in out, out
out = gate(CROP, put([entry(stage="bud-break")]))
assert "critical-warnings:" in out and "own growth_stages" in out, out
out = gate(CROP, put([entry(), entry()]))
assert "critical-warnings:" in out and "appears twice" in out, out
out = gate(CROP, put([entry(**{"class": "comfort"})]))
assert "critical-warnings:" in out and "class must be one of" in out, out

# The key on an UNCERTIFIED SHELL bounces, even carrying null.
out = gate("avocado", put(None, record=False))
assert "critical-warnings:" in out and "uncertified" in out, out

# container_safety is checked on every crop's run: a malformed object and a figure both bounce here.
out = gate(CROP, mutate_data=lambda d: d.__setitem__("container_safety", {"warnings": []}))
assert "critical-warnings:" in out and "container_safety must be an object" in out, out
bad = {"warnings": [entry(id="balcony_load", body_seasoned="A wet pot weighs 60 pounds.")],
       "field_additions": [{"field": "container_safety.balcony_load", "date": "2026-09-23",
                            "sources": ["uiuc_ext"],
                            "note": f"{URL} sha256 {'0' * 64} verbatim: \"x\""}]}
out = gate(CROP, mutate_data=lambda d: d.__setitem__("container_safety", bad))
assert "critical-warnings:" in out and "states a figure" in out, out
good = copy.deepcopy(bad); good["warnings"][0]["body_seasoned"] = "Ask an architect about the load."
out = gate(CROP, mutate_data=lambda d: d.__setitem__("container_safety", good))
assert "critical-warnings:" not in out and "container_safety: 1" in out, out

# Presence arms in the same commit that writes the keys, never before: the flag must match the data.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
carrying = any("critical_warnings" in c for c in base["crops"]) or "container_safety" in base
assert ("A61_PRESENCE_ARMED = True" in src) == carrying, \
    "presence floor must arm in the same commit that writes the keys, never before"

if "A61_PRESENCE_ARMED = True" in src:
    # With presence ARMED, a certified crop missing the key bounces, and so does a dataset
    # missing container_safety; the shells stay exempt by status.
    out = gate(CROP, lambda c: c.pop("critical_warnings"))
    assert "critical-warnings:" in out and "missing" in out, out
    out = gate(CROP, mutate_data=lambda d: d.pop("container_safety"))
    assert "critical-warnings:" in out and "container_safety missing" in out, out
    out = gate("avocado")
    assert "critical-warnings: avocado" not in out, out

print("PASS gate A61 critical_warnings + container_safety")
