#!/usr/bin/env python3
"""Raw-display snake_case cert-gate branch (whole_crop_gate A23, 2026-06-25). Imported + run
by whole_crop_gate.py.

WHY: a handful of user-facing fields are rendered VERBATIM by the guide cards -- FeedingCard
prints fertilizer.type/timing/frequency as-is (the explicit "no Title Case" rule, audit F3),
CareGuideCard prints crop.sunlight as-is, CompanionsCard prints a companion's timing as-is --
and watering.watering_method/drought_tolerance are display-INTENT prose. The 2026-06-25 scan
found 8 of 18 anchors shipping snake_case TOKENS into these (onion fertilizer.type=
'nitrogen_forward', sunlight='full_sun', zucchini companion timing='plant_with', ...), which
render with underscores to growers. The display-readiness gate (A20) checks these fields are
PRESENT, never that they read as prose; release_verify's user-facing scan checks `--`/em-dash/
spelled-degrees, never snake_case -- a confirmed blind spot this branch closes.

This flags a RAW snake_case value (^[a-z0-9]+(_[a-z0-9]+)+$) in any RAW-DISPLAY field
(field_classification.is_raw_display). It is a NO-OP for the categorical TOKEN fields the
renderer maps/humanizes (start_method.start, companions[].category, container
shape_requirements, soil organic_matter_preference, ...) -- those are legitimately snake_case
and must NOT be flagged. Enforces the human-readable SHAPE, never the wording.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_classification import is_raw_display

# A render-verbatim value shows an underscore to a grower whenever it contains an
# underscore-JOINED alphanumeric pair (`word_word`), in ANY case, with or without
# surrounding spaces. The original anchored lowercase predicate
# ^[a-z0-9]+(_[a-z0-9]+)+$ missed "Full_sun" (capital), "Slow_release_granular"
# (capital), and "full sun_partial" (a space-bearing value whose `sun_partial` token
# still renders an underscore) -- incognito-redteam C12. A case-insensitive bare-token
# SEARCH is a strict superset of the old anchored match and closes all three. The 18
# carry zero underscores in any render-verbatim field; hyphens ("Nitrogen-forward",
# "10-10-10", "every 3-4 weeks") and spaces alone never match.
SNAKE = re.compile(r"[A-Za-z0-9]+_[A-Za-z0-9]+")


def raw_display_violations(crop):
    """Return a list of violation strings ([] = clean) -- one per render-verbatim display
    field carrying a raw snake_case value."""
    V = []

    def walk(node, path, key):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k, k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", key)
        elif isinstance(node, str):
            if is_raw_display(key, path) and SNAKE.search(node):
                V.append(f"{path} = {node!r} -- snake_case token in a render-verbatim display "
                         f"field; author human-readable prose")

    walk(crop, "", None)
    return V


if __name__ == "__main__":
    import json
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path))
    total = 0
    for c in data["crops"]:
        vs = raw_display_violations(c)
        if vs:
            print(f"  {c.get('slug')}:")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"raw_display gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
