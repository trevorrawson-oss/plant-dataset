#!/usr/bin/env python3
"""plant_windows tests -- the parser both the de-mux migration and gate A43 stand on.
Every case is a REAL string from the canonical (or its defect-class twin)."""
from plant_windows import spans, window_count, single_date, in_span, months_overlap

# comma-joined discrete windows (bell-pepper se_gulf z8)
assert window_count("Mar 15 - Apr 15, Sep 1 - Sep 20") == 2
# parenthetical comma is NOT a second window (peach)
assert window_count("Apr - May (dormant, bare-root)") == 1
# " or "-joined alternatives are ONE planting choice (lavender)
assert window_count("Oct - Nov or Feb - Mar") == 1
assert spans("Oct - Nov or Feb - Mar")[0].n_alternatives == 2
# single-month window (potato plant_out) -- broke the naive scan
assert window_count("Feb - Mar, Aug") == 2
p = spans("Feb - Mar, Aug")[1]
assert (p.start_month, p.end_month, p.start_day) == (8, 8, None) and p.raw == "Aug"
# full month names (onion)
assert window_count("Oct - Nov, Jan - March") == 2
assert spans("Jan - March")[0].end_month == 3
# bare single months, comma-joined (onion start_indoors)
assert window_count("Sep, Dec") == 2
# null / empty
assert window_count(None) == 0 and window_count("") == 0 and spans(None) == []
# endpoint text preserves authored granularity
s = spans("May 15 - Jun 30, Nov 1 - Nov 30")
assert s[1].start_text == "Nov 1" and s[1].end_text == "Nov 30" and s[1].raw == "Nov 1 - Nov 30"
m = spans("Apr - Jun, Sep - Nov")[1]
assert m.start_text == "Sep" and m.end_text == "Nov"
# single_date
assert single_date("Mar 15") == (3, 15)
assert single_date("Jun") == (6, None)
assert single_date("March") == (3, None)
assert single_date("May 15 - Jun 30") is None and single_date(None) is None
# in_span, incl. year wrap (Nov - Jan)
assert in_span((9, 10), spans("Sep 1 - Sep 20")[0])
assert not in_span((3, 15), spans("Sep 1 - Sep 20")[0])
assert in_span((1, 5), spans("Nov - Jan")[0])
assert in_span((12, None), spans("Nov - Jan")[0])
# months_overlap (pop-1 granularity mismatch: month-string vs day-precision sp)
assert months_overlap(spans("Sep - Nov")[0], spans("Sep 6 - Nov 8")[0])
assert not months_overlap(spans("Mar - May")[0], spans("Oct - Dec")[0])

print("plant_windows tests: OK")
