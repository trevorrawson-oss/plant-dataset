#!/usr/bin/env python3
"""Tests for variety_ladder_delta_gate. Run: python3 tools/test_variety_ladder_delta_gate.py

Every guard family gets a CLEAN case (must stay green) and a RED case (must fire). A guard that
refuses a malformed input while staying green on a good one is a REFUSAL-SPEC pass, not vacuity.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_ladder_delta_gate import delta_violations, resolve_ladder, similarity

CATALOG = {
    "garden_sanitation":   {"tier": "cultural"},
    "resistant_varieties": {"tier": "cultural"},
    "prune_out_infection": {"tier": "physical"},
    "fruit_bagging":       {"tier": "physical"},
    "beneficial_predators": {"tier": "biological"},
    "sulfur":              {"tier": "soft_chemical"},
    "pyrethroid":          {"tier": "conventional"},
}
SRCS = {"cornell_ext": {"tier": "T1"}, "blogspot": {"tier": "T3"}}

PARENT = [
    {"method": "garden_sanitation", "note_beginner": "Rake up and destroy the fallen leaves.",
     "note_seasoned": "Leaf litter is the overwintering inoculum; remove it."},
    {"method": "prune_out_infection", "note_beginner": "Cut out the infected shoots.",
     "note_seasoned": "Excise cankers well below the visible margin."},
    {"method": "sulfur", "note_beginner": "Spray sulfur on a protectant schedule.",
     "note_seasoned": "Sulfur on a 7 to 10 day protectant interval from green tip."},
]


def crop(ladder_delta, resistance=None, parent=None):
    return {"slug": "apple",
            "diseases": [{"id": "apple-scab", "control_ladder": parent or PARENT}],
            "varieties": {"recommended": [
                {"id": "liberty", "name": "Liberty",
                 "resistance": resistance if resistance is not None else {"apple-scab": "immune"},
                 "ladder_delta": ladder_delta}]}}


def V(*a, **k):
    return delta_violations(crop(*a, **k), CATALOG, SRCS)


def fires(vs, needle):
    return any(needle in v for v in vs)


# ---------------------------------------------------------------- CLEAN (must stay green)
# a real drop, backed by a real resistance grade
assert V({"apple-scab": {"basis": "resistance", "rungs": [
    {"method": "sulfur", "op": "drop",
     "why_beginner": "Liberty shrugs scab off, so the sulfur spray is wasted effort.",
     "why_seasoned": "Immunity removes the protectant requirement outright."}]}}) == []
# a genuine replace: same method, materially different guidance
assert V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "garden_sanitation", "op": "replace",
     "note_beginner": "Skip the autumn leaf cleanup; on this tree it buys you nothing.",
     "note_seasoned": "Sanitation is not cost-effective where the cultivar carries Vf."}]}}) == []
# an add that keeps the ladder softest-first (physical, placed after the cultural rung)
assert V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "fruit_bagging", "op": "add", "after": "garden_sanitation",
     "note_beginner": "Slip a bag over each young fruit once it sets.",
     "note_seasoned": "Bagging at 1/2 inch fruit excludes the ascospore window entirely."}]}}) == []
# N/A branch: no ladder_delta at all
assert delta_violations({"slug": "apple", "diseases": [{"id": "apple-scab",
    "control_ladder": PARENT}], "varieties": {"recommended": [{"id": "gala"}]}},
    CATALOG, SRCS) == []

# ---------------------------------------------------------------- G1 REFERENTIAL
assert fires(V({"appel-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "drop"}]}}), "is not a laddered pest/disease id")
# a real problem id that carries NO ladder cannot be delta'd
assert fires(delta_violations({"slug": "apple",
    "diseases": [{"id": "fire-blight"}],
    "varieties": {"recommended": [{"id": "liberty", "ladder_delta": {"fire-blight": {
        "basis": "source", "sources": ["cornell_ext"],
        "rungs": [{"method": "sulfur", "op": "drop"}]}}}]}}, CATALOG, SRCS),
    "is not a laddered pest/disease id")
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "kaolin_clay", "op": "drop"}]}}), "is not in")           # not in parent ladder
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "no_such_method", "op": "add", "note_beginner": "x"}]}}), "unknown control_methods")
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "add", "note_beginner": "x"}]}}), "already has")
assert fires(V({"apple-scab": {"basis": "resistance", "rungs": [
    {"method": "sulfur", "op": "drop"}]}}, resistance={}), "carries no resistance grade")
assert fires(V({"apple-scab": {"basis": "source", "sources": ["blogspot"], "rungs": [
    {"method": "sulfur", "op": "drop"}]}}), "is not T1")
assert fires(V({"apple-scab": {"basis": "source", "rungs": [
    {"method": "sulfur", "op": "drop"}]}}), "requires a non-empty sources")
assert fires(V({"apple-scab": {"basis": "vibes", "rungs": [
    {"method": "sulfur", "op": "drop"}]}}), "basis 'vibes' not in")
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "delete"}]}}), "op 'delete' not in")

# ---------------------------------------------------------------- G2 NON-VACUITY
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": []}}),
             "rungs is empty")
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "drop"}, {"method": "sulfur", "op": "drop"}]}}),
    "appears twice")
# the headline defect: a replace that reproduces the parent note verbatim
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "replace",
     "note_beginner": "Spray sulfur on a protectant schedule.",
     "note_seasoned": "Sulfur on a 7 to 10 day protectant interval from green tip."}]}}),
    "BYTE-EQUAL")

# ---------------------------------------------------------------- G3 NEAR-VERBATIM
# one word changed -- G2 is defeated, G3 must still catch it
near = V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "replace",
     "note_beginner": "Spray sulphur on a protectant schedule.",
     "note_seasoned": "Sulfur on a 7 to 10 day protectant interval from green bud."}]}})
assert fires(near, "near-verbatim copy"), near
assert not fires(near, "BYTE-EQUAL"), "G3 must be reachable WITHOUT G2 firing first"
# whitespace/case reflow must not dodge it
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "sulfur", "op": "replace",
     "note_beginner": "  SPRAY   sulfur on a protectant schedule.  "}]}}), "near-verbatim copy")

# ---------------------------------------------------------------- G4 RESOLVED ORDER
# adding a conventional rung ahead of the cultural one breaks softest-first
assert fires(V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "pyrethroid", "op": "add",
     "note_beginner": "Hit it hard and early with a synthetic."}]}, }), "RESOLVED ladder") is False, \
    "appending at the end is legal -- conventional last keeps the order"
bad_order = V({"apple-scab": {"basis": "source", "sources": ["cornell_ext"], "rungs": [
    {"method": "pyrethroid", "op": "add", "after": "garden_sanitation",
     "note_beginner": "Hit it hard and early with a synthetic."}]}})
assert fires(bad_order, "RESOLVED ladder"), bad_order

# ---------------------------------------------------------------- resolver unit checks
assert [r["method"] for r in resolve_ladder(PARENT, [{"method": "sulfur", "op": "drop"}])] == \
    ["garden_sanitation", "prune_out_infection"]
assert resolve_ladder(PARENT, [{"method": "sulfur", "op": "replace",
    "note_beginner": "new"}])[2]["note_beginner"] == "new"
assert [r["method"] for r in resolve_ladder(PARENT, [{"method": "fruit_bagging", "op": "add",
    "after": "garden_sanitation", "note_beginner": "n"}])] == \
    ["garden_sanitation", "fruit_bagging", "prune_out_infection", "sulfur"]
# resolve is non-mutating -- the parent must survive byte-identical
import copy
_snapshot = copy.deepcopy(PARENT)
resolve_ladder(PARENT, [{"method": "sulfur", "op": "replace", "note_beginner": "mutated?"}])
assert PARENT == _snapshot, "resolve_ladder mutated the parent ladder in place"
assert similarity("a b c", "a b c") == 1.0

print("All variety_ladder_delta_gate tests passed.")
