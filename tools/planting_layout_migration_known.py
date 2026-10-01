"""PLA-10 R5 migration waivers for sourced_block_ratchet_gate.py -- the ONLY way a planting_layout
entry ships uncited. Ruled 2026-09-30 (spec docs/specs/pla10-field-shape.md, R5 and §2.3).

A crop whose in-row spacing has no page in its cited set is HUNTED inside promote 1. One still without a
page after a RECORDED hunt ships its default entry under a waiver here:
  * keyed by identity (crop + entry id), listed by name;
  * valid only while the entry's `in_row_inches` BYTE-EQUALS the pre-promote `spacing_inches` recorded
    beside it (compact JSON, so [10, 12] and [10.0, 12] differ): moving the value into an entry changes
    where it lives, not what is claimed, and any change to the claim needs a citation;
  * only on a crop of ELIGIBLE, the R5 hunt list as ruled; a waiver off it is refused;
  * able only to shrink: the data commit pins the set it lands with, and a later entry is a new claim.

EMPTY in the tools commit (2026-10-01). Promote 1's data commit fills it from the hunt record, and its
suite proves each `in_row_inches` equals the crop's spacing_inches at canonical c5fc3d13 (the pre-promote
value, read through promote_fixture, never the live file).

Kept as a .py module, not JSON: harnesses that copy tools/*.py into a scratch dir would drop a JSON file
and crash whole_crop_gate at import (measured 2026-09-30 on sourced_block_ratchet_known).
"""
TICKET = "PLA-10"
RULING = "R5 (Trevor, 2026-09-30), widened by W5 (Trevor, 2026-10-01)"
PRE_PROMOTE_CANONICAL = "c5fc3d13764f6d08b24574bbb07ecb15f5cfddeb7ba80f7439a72d8829813e28"
# The ruled eight (R5), plus five admitted by W5 (2026-10-01), which widened eligibility from "no page" to
# "no CITABLE page after a recorded hunt": echinacea and cherry-sour (no page), pomegranate (its page
# disowns the figure), sweet-pea (its only figure is a trellis density, promote 2's) and cherry-sweet
# (R1's basis finding, a commercial figure). Listed by name; a waiver still needs the recorded hunt.
ELIGIBLE = ("bok-choy", "rosemary", "mulberry", "borage", "cosmos", "sweet-alyssum", "bee-balm", "viola",
            "echinacea", "cherry-sour", "pomegranate", "sweet-pea", "cherry-sweet")
# slug -> {"entry_id": str, "in_row_inches": [lo, hi] (the pre-promote spacing_inches, verbatim),
#          "hunt": "<where the recorded hunt lives>"}
WAIVERS = {}
