#!/usr/bin/env python3
"""Annual calendar deriver (Step 5.5) -- the annual analog of tree_calendar.py.

Derives a frost-anchored annual crop's 12-month `calendar[]` from its resolved
per-zone windows (plant_out / start_indoors / harvest), so the calendar is COMPUTED
from the dates, never hand-authored (v1.9 "compute, never hand-author"). A pure
function + a violations() check for the gate, mirroring tree_calendar.

ALGORITHM (frost-anchored, summer-centered season):
  - year_round cell -> 12x "growing" (continuous; the renderer branches on the flag).
  - else, per month Jan..Dec, first match wins (precedence):
      declared heat_pause > plant > harvest > indoors > growing > cold_pause > wait
  - plant months P: explicit `plant_out` if present (AUTHORITATIVE -- a plant/harvest
    overlap resolves to plant); else the direct-sow first/last-plant envelope MINUS
    the harvest months (the envelope over-counts; the harvest display marks non-plant
    months -- this is what reproduces carrot's two-cycle northern_tier exactly).
  - harvest months H: the `harvest` display, else `harvest_start`..`harvest_end`.
  - indoors months I: `start_indoors`.
  - season = earliest(indoors|plant|first_plant) .. harvest_end; growing fills the
    season minus P/H/I; months outside the season are cold_pause (frost-anchored).

SCOPE (basil archetype + cold multi-cycle): see test_annual_calendar.py. Winter-
wrapping harvest (carrot se_gulf "Sep - May") + lettuce-style heat-inverted two-
cool-season cells need a cycle-segmentation extension -- NOT basil; flagged there.
"""

MONTHS = {name[:3].lower(): i for i, name in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}


def _month_num(tok):
    if not tok or not isinstance(tok, str):
        return None
    return MONTHS.get(tok.strip()[:3].lower())


def _span(a, b):
    """Inclusive wrap-aware month span a..b as an ordered list (e.g. 9..5 wraps)."""
    out, m = [], a
    while True:
        out.append(m)
        if m == b:
            break
        m = m % 12 + 1
    return out


def parse_months(s):
    """A display string -> set of month numbers (1-12). Handles 'Mon - Mon' ranges
    (inclusive, wrap-aware), 'Mon DD - Mon DD', comma/semicolon multi-spans, bare
    'Mon', and 'Year round'. Unparseable / None -> empty set."""
    if not s or not isinstance(s, str):
        return set()
    if "year round" in s.lower():
        return set(range(1, 13))
    out = set()
    for span in s.replace(";", ",").split(","):
        span = span.strip()
        if not span:
            continue
        if "-" in span:
            a, b = span.split("-", 1)
            ma, mb = _month_num(a), _month_num(b)
            if ma and mb:
                out.update(_span(ma, mb))
        else:
            mn = _month_num(span)
            if mn:
                out.add(mn)
    return out


def derive_annual_calendar(cell, calendar_basis="frost_anchored"):
    """Return the 12-element calendar token list for one resolved_by_zone cell."""
    if cell.get("year_round") or (isinstance(cell.get("plant_out"), str)
                                  and "year round" in cell["plant_out"].lower()):
        return ["growing"] * 12

    H = parse_months(cell.get("harvest"))
    if not H:
        hs, he = _month_num(cell.get("harvest_start")), _month_num(cell.get("harvest_end"))
        if hs and he:
            H = set(_span(hs, he))
    I = parse_months(cell.get("start_indoors"))
    heat = set(cell.get("heat_pause_months") or ())

    plant_out = parse_months(cell.get("plant_out"))
    if plant_out:
        P = plant_out                       # explicit windows are authoritative
    else:                                    # direct-sow: envelope MINUS harvest
        fp, lp = _month_num(cell.get("first_plant_date")), _month_num(cell.get("last_plant_date"))
        P = (set(_span(fp, lp)) - H) if (fp and lp) else set()

    active = P | H | I | heat                # token-bearing (active) months
    # cold_pause = the winter off-season, anchored at deep winter (January) and grown
    # contiguously while inactive. A January-active cell is near-year-round -> NO cold_pause,
    # so an inactive SUMMER lull (e.g. South FL Jul/Aug) renders "growing", not a cold pause.
    cold = set()
    if calendar_basis == "frost_anchored" and 1 not in active:
        cold.add(1)
        m = 12                               # walk backward from January
        while m not in active and m not in cold:
            cold.add(m); m = 12 if m == 1 else m - 1
        m = 2                                # walk forward from January
        while m not in active and m not in cold:
            cold.add(m); m = 1 if m == 12 else m + 1

    cal = []
    for m in range(1, 13):
        if m in heat:
            cal.append("heat_pause")
        elif m in P:
            cal.append("plant")
        elif m in H:
            cal.append("harvest")
        elif m in I:
            cal.append("indoors")
        elif m in cold:
            cal.append("cold_pause")
        elif calendar_basis == "frost_anchored":
            cal.append("growing")            # in-season lull (between cycles / summer)
        else:
            cal.append("wait")
    return cal


def annual_calendar_violations(crop):
    """For every resolved cell with a NON-EMPTY calendar, recompute from the cell's
    windows and flag any mismatch (the drift defense, like tree A4). No-op for non-
    frost_anchored crops. Cells that declare a heat_pause must carry `heat_pause_months`
    for the recompute to be exact (basil has none)."""
    if crop.get("calendar_basis") != "frost_anchored":
        return []
    out = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            cal = cell.get("calendar")
            if not cal:
                continue
            exp = derive_annual_calendar(cell, "frost_anchored")
            if cal != exp:
                out.append({"region": rk, "zone": z, "stored": cal, "derived": exp})
    return out
