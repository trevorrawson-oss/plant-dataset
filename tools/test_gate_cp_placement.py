#!/usr/bin/env python3
"""Integration test: whole_crop_gate flags a MIS-NESTED CP field.

A CP field renders as suffixed SIBLINGS at the parent level (container_notes.notes_seasoned,
storage.fridge_seasoned), NOT a nested wrapper (container_notes.shape_requirements.shape_requirements_seasoned).
claude.ai shipped microgreens 6-8 double-nested; the recursive suffix walks (dual-voice + roster)
PASS it -- placement was unenforced. Signature: a key K whose dict value contains a child key
K_seasoned or K_beginner (the suffix redundantly repeats the parent key). Legit grouping objects
(soil_mix.type_seasoned, drainage.saucer_practice_seasoned) are NOT flagged -- the inner stem
differs from the parent key.
Run from repo root: python3 tools/test_gate_cp_placement.py"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

base = json.load(open("crops_data_final.json"))
V = "mis-nested CP field"


def run_gate(slug, mutate=None):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    if mutate:
        mutate(c)
    tmp = os.path.join(HERE, "_tmp_cpplace_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        out = subprocess.run(
            [sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
            capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)
    return out

# a clean certified crop (carries legit grouping objects like soil_mix.type_seasoned) -> NO flag
assert V not in run_gate("cherry-tomato"), "clean crop (legit grouping objects) wrongly flagged"

# inject the double-nest signature -> flag
def misnest(c):
    c["container_notes"]["shape_requirements"] = {
        "shape_requirements_seasoned": "shallow tray", "shape_requirements_beginner": "shallow tray"}
assert V in run_gate("cherry-tomato", misnest), "double-nested CP field should be flagged"

# the same signature buried in a list item (a pests[] entry) -> flag (the walk recurses lists)
def misnest_in_list(c):
    c["pests"] = [{"name_seasoned": "x", "name_beginner": "x",
                   "cause": {"cause_seasoned": "y", "cause_beginner": "y"}}]
assert V in run_gate("cherry-tomato", misnest_in_list), "mis-nest inside a list item should be flagged"

# correct suffixed-sibling placement -> NO flag
def correct(c):
    c["container_notes"]["shape_requirements_seasoned"] = "shallow tray"
    c["container_notes"]["shape_requirements_beginner"] = "shallow tray"
assert V not in run_gate("cherry-tomato", correct), "correct sibling placement wrongly flagged"

print("PASS gate cp placement")
