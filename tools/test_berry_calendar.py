#!/usr/bin/env python3
"""Tests for the berries_herbaceous calendar deriver + coherence gate (strawberry,
anchor 13). Run: python3 tools/test_berry_calendar.py

The strawberry calendar is DERIVED data (the tree_calendar lesson): a pure function of
the cell's grown_as + display windows, so it cannot drift from them. Two shapes:
  - PERENNIAL (matted-row, June-bearing spine): dormant winter / growing season /
    bloom / harvest / renovation (month after harvest). Frost dates bracket dormancy.
  - ANNUAL (hot-summer CA/FL): plant in fall, growing, bloom, harvest, season_over.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from berry_calendar import (derive_perennial_berry_calendar, derive_annual_berry_calendar,
                            derive_berry_calendar, berry_calendar_violations)

# 1. PERENNIAL z5: last_frost Apr, first_frost Oct, bloom May, harvest June -> renovation July.
perennial = derive_perennial_berry_calendar("May", "June", "April", "October")
assert perennial == ["dormant", "dormant", "dormant", "growing", "bloom", "harvest",
                     "renovation", "growing", "growing", "growing", "dormant", "dormant"], perennial

# 2. ANNUAL CA z9: plant Oct, bloom Feb, harvest Mar-Jun -> season_over the rest.
annual = derive_annual_berry_calendar("October", "February", "March-June")
assert annual == ["growing", "bloom", "harvest", "harvest", "harvest", "harvest",
                  "season_over", "season_over", "season_over", "plant", "growing", "growing"], annual

# 3. unparseable / empty inputs -> None (the caller owns emptiness)
assert derive_perennial_berry_calendar("", "June", "April", "October") is None
assert derive_annual_berry_calendar("October", "February", "") is None

# 4. dispatch reads the cell shape
cell_p = {"bloom": "May", "harvest": "June", "resolved_from": {"last_frost": "April", "first_frost": "October"}}
assert derive_berry_calendar("perennial", cell_p) == perennial, derive_berry_calendar("perennial", cell_p)
cell_a = {"plant_out": "October", "bloom": "February", "harvest": "March-June"}
assert derive_berry_calendar("annual", cell_a) == annual, derive_berry_calendar("annual", cell_a)
assert derive_berry_calendar("bogus", cell_a) is None

# 5. coherence gate: no-op off-basis
non_berry = {"calendar_basis": "frost_anchored", "regions": {}}
assert berry_calendar_violations(non_berry) == [], "non-berry crop must be a no-op"

# 6. coherence gate: a stored calendar that matches the deriver -> clean
def berry_crop(stored_cal, grown_as="perennial"):
    return {"calendar_basis": "perennial_herbaceous", "regions": {"northern_tier": {
        "resolved_by_zone": {"5": {"grown_as": grown_as, "bloom": "May", "harvest": "June",
            "resolved_from": {"last_frost": "April", "first_frost": "October"},
            "calendar": stored_cal}}}}}
assert berry_calendar_violations(berry_crop(perennial)) == [], berry_calendar_violations(berry_crop(perennial))

# 7. coherence gate: a DRIFTED stored calendar -> violation naming the cell
drift = list(perennial); drift[6] = "growing"   # renovation hand-edited away
assert any("northern_tier" in v and "5" in v and "incoherent" in v
           for v in berry_calendar_violations(berry_crop(drift))), berry_calendar_violations(berry_crop(drift))

# 8. coherence gate: an EMPTY calendar (Step-3.5 admission) -> skipped (no-op)
assert berry_calendar_violations(berry_crop([])) == [], "empty calendar is the admission state -- skip"

print("berry_calendar: all tests passed")
