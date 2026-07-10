#!/usr/bin/env python3
"""Tests for the planting_layout conditional-field gate (A44, spec 2026-07-10). Run:
    python3 tools/test_planting_layout_gate.py

WHY: `planting_layout` (block/row/hill/grid/single) is a conditional field -- present ONLY where a
crop needs a non-default spatial planting pattern (corn's wind-pollination block). Checks fire ONLY
when planting_layout is present -- ABSENCE (and null) is a no-op, matching the divide_every_years /
chill conditional-field precedent, so the un-authored roster stays green. `pollination_block_min_rows`
is the numeric companion, required IFF planting_layout == 'block' (int >= 2, not bool). A bad enum
value short-circuits: check_crop returns immediately after flagging it, so a crop with BOTH a bad
enum AND a bad min_rows yields exactly ONE violation, not two. See
docs/superpowers/plans/2026-07-10-corn-grass-archetype.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from planting_layout_gate import check_crop


def C(**kw):
    base = {"slug": "x"}
    base.update(kw)
    return base


# ---------------------------------------------------------------- clean fixtures (-> no violations)
assert check_crop(C()) == [], "absent planting_layout should no-op"
assert check_crop(C(planting_layout=None)) == [], "null planting_layout should no-op"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=4)) == [], \
    "block with a valid min_rows should pass"
assert check_crop(C(planting_layout="row")) == [], "valid row with no min_rows should pass"

# ---------------------------------------------------------------- defect injections (-> violation)
assert check_crop(C(planting_layout="block")) != [], "block without min_rows should fail"
assert check_crop(C(planting_layout="blocks")) != [], "bad enum value should fail"
assert check_crop(C(planting_layout="row", pollination_block_min_rows=4)) != [], \
    "min_rows present on a non-block layout should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=1)) != [], \
    "min_rows below the floor (2) should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows="4")) != [], \
    "min_rows as a string (non-int) should fail"
assert check_crop(C(planting_layout="block", pollination_block_min_rows=True)) != [], \
    "min_rows as a bool should fail (bool is an int subclass -- guard it)"
assert check_crop(C(pollination_block_min_rows=4)) != [], \
    "orphan min_rows with no planting_layout should fail"

# bad enum + bad min_rows together -> enum check short-circuits -> exactly 1 violation, not 2
assert len(check_crop({"slug": "x", "planting_layout": "blocks", "pollination_block_min_rows": 1})) == 1, \
    "bad enum plus bad min_rows should short-circuit to exactly 1 violation"

print("planting_layout_gate tests: OK")
