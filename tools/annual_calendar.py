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
    heat = declared_heat_months(cell)                 # nested heat_pause.months OR flat heat_pause_months
    heat_flip = heat & indoor_core_months(cell)       # action-over-passive: hot months that are core indoor months

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
        if m in heat_flip:
            cal.append("indoors")            # NEW: a real indoor-start action overrides the passive pause
        elif m in heat:
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


# The valid annual calendar token vocabulary (checklist enum, frost_anchored slice).
# `start_indoors` is deliberately ABSENT: SuccessionCard renders the token `indoors`
# (the enum value) and has no case for `start_indoors`, so a `start_indoors` token is
# a rendering-drift bug the gate must catch.
ANNUAL_CALENDAR_TOKENS = {"wait", "indoors", "plant", "growing", "harvest", "late",
                          "cold_pause", "heat_pause", "season_over"}


def annual_coherence_violations(crop):
    """Always-on coherence check for frost_anchored annual calendars -- the annual
    analog of the tree A4 gate. Returns (hard, notes). It does NOT require a calendar
    to be re-derivable (complex multi-cycle cells are legitimately hand-authored), only
    that it is internally consistent:
      HARD (gate-blocking): a calendar that is not length-12, carries a token outside
        the annual enum (catches the `start_indoors` drift + typos), or whose heat_pause
        tokens disagree with the cell's `heat_pause.months` object (the apple/peach
        author-the-two-independently bug, for annuals).
      NOTE (surfaced, non-blocking): a `wait` token -- a pause-legibility review item.
    No-op for non-frost_anchored crops."""
    if crop.get("calendar_basis") != "frost_anchored":
        return [], []
    hard, notes = [], []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            cal = cell.get("calendar")
            if not isinstance(cal, list) or not cal:
                continue
            loc = f"{rk}.z{z}"
            if len(cal) != 12:
                hard.append(f"{loc}: calendar length {len(cal)} != 12")
                continue
            bad = sorted(set(cal) - ANNUAL_CALENDAR_TOKENS)
            if bad:
                hard.append(f"{loc}: invalid calendar token(s) {bad}")
            hp = (cell.get("heat_pause") or {}).get("months")
            if hp is not None:
                cal_hp = [i + 1 for i in range(12) if cal[i] == "heat_pause"]
                if sorted(hp) != sorted(cal_hp):
                    hard.append(f"{loc}: heat_pause.months {sorted(hp)} != calendar heat_pause {sorted(cal_hp)}")
            if "wait" in cal:
                notes.append(f"{loc}: `wait` token (pause-legibility review)")
    return hard, notes


# Days per month for the "core month" (fully-covered) test. February uses 29 so a
# span ending Feb 28 does NOT count February as fully covered -- the conservative
# direction (fewer flags, never a false positive on a leap-agnostic boundary).
_DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _month_day(tok):
    """'Mon DD' -> (month, day); 'Mon' -> (month, None). Unparseable -> (None, None)."""
    if not tok or not isinstance(tok, str):
        return (None, None)
    parts = tok.strip().split()
    m = _month_num(parts[0])
    d = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    return (m, d)


def core_months(display):
    """Months a SINGLE span of the display covers in FULL (day 1 .. last day), i.e.
    unambiguously inside the window rather than clipped at a span boundary. A bare
    'Mon' or a day-less 'MonA - MonB' range treats every month as fully covered
    (no day info to clip). This is the month-rounding guard: a pause on a partly
    covered boundary month is tolerated; a pause on a fully-covered core month is a
    real contradiction. Wrap-aware (e.g. 'Nov 1 - Feb 28')."""
    out = set()
    if not display or not isinstance(display, str):
        return out
    for span in display.replace(";", ",").split(","):
        span = span.strip()
        if not span:
            continue
        if "-" in span:
            a, b = span.split("-", 1)
            ma, da = _month_day(a)
            mb, db = _month_day(b)
            if not ma or not mb:
                continue
            for m in _span(ma, mb):
                start_ok = (m != ma) or (da is None or da <= 1)
                end_ok = (m != mb) or (db is None or db >= _DAYS_IN_MONTH[m - 1])
                if start_ok and end_ok:
                    out.add(m)
        else:
            m, d = _month_day(span)
            if m and d is None:        # a bare month = the whole month
                out.add(m)
    return out


def indoor_core_months(cell):
    """Core (fully day-covered) months of any REAL indoor-start window on this cell:
    top-level `start_indoors` OR `second_planting.start_indoors`. These are the months
    where an indoor-start ACTION is genuinely underway -- the action-over-passive flip
    trigger (a heat_pause month here shows `indoors`, not the passive pause)."""
    out = set(core_months(cell.get("start_indoors")))
    sp = cell.get("second_planting") or {}
    out |= core_months(sp.get("start_indoors"))
    return out


def declared_heat_months(cell):
    """The cell's declared heat-exclusion months: the nested `heat_pause.months`
    object (the authored, sourced form) or the flat `heat_pause_months` (the deriver
    form). Empty set if neither is present (an UNBACKED heat_pause -- legitimate for
    zucchini/green-beans summer cells today; backing them is B3, not this gate)."""
    hp = cell.get("heat_pause")
    if isinstance(hp, dict) and hp.get("months") is not None:
        return set(hp["months"])
    flat = cell.get("heat_pause_months")
    if flat is not None:
        return set(flat)
    return set()


# Frost/dormancy pause tokens that can never coincide with an outdoor planting window
# at ANY granularity (checked coarse). heat_pause is handled separately (core-only +
# declaration-aware) because a heat exclusion legitimately abuts planting/harvest at
# span boundaries (month-rounding).
_FROST_PAUSE_TOKENS = {"cold_pause", "wait"}

_MON_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def annual_calendar_violations(crop):
    """B1 token-PLACEMENT drift gate (whole_crop_gate A24). A frost_anchored annual's
    hand-authored calendar must not place a PAUSE token on a month its own windows say
    is ACTIVE. No-op for non-frost_anchored crops. Returns a list of violation strings.

    This is deliberately NOT a full re-derivation. The Step-5.5 deriver
    (`derive_annual_calendar`) reproduces only the simplest single-season cells
    (basil, zinnia); it cannot reproduce ~190/200 certified annual cells, which are
    legitimately hand-authored multi-cycle / winter-wrapping / heat-inverted /
    year-round-with-plant shapes plus pervasive month-rounding. Wiring the re-deriver
    as a gate would cry wolf on almost every real cell. This gate instead checks the
    audit-B1 defect classes directly, with empirically ZERO false positives across all
    10 certified annuals (200 cells):

      - cold_pause / wait on ANY plant_out month -> a frost/dormancy lockout cannot
        coincide with an outdoor planting window (the pause-on-plant defect).
      - heat_pause on a CORE plant_out or CORE harvest month NOT in the cell's declared
        heat_pause.months -> a heat exclusion sitting on an unambiguous (fully covered)
        planting/harvest month with no backing (the pause-on-plant / pause-on-harvest
        heat defects). "Core" tolerates the month-rounding that legitimately puts a
        heat_pause on a partly-covered span boundary; a declared heat month is excused.
      - cold_pause on a CORE harvest month -> the harvest display over-states into a frost
        month (the old broccoli nt / beefsteak ca_south_coast shape). GATE-UNLOCK wired
        2026-06-26 once the Pass-1 data fix corrected those cells (the summer gap relabeled
        heat_pause + the harvest split); "core" tolerates the partial frost-tail boundary.

    Deliberately NOT checked: cold_pause on a partly-covered boundary harvest month (the
    legitimate frost tail -- month-rounding); a `wait` token on a harvest month (a separate
    pause-legibility item, e.g. beefsteak ca_north_coast.z10, pending its own fix); thermal
    BACKING of a heat_pause (B3, now its own gate A28). Heat_pause/declared-months ALIGNMENT
    stays in `annual_coherence_violations` (A5)."""
    if crop.get("calendar_basis") != "frost_anchored":
        return []
    out = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            cal = cell.get("calendar")
            if not isinstance(cal, list) or len(cal) != 12:
                continue                       # length/shape is A5's job
            loc = f"{rk}.z{z}"
            plant = parse_months(cell.get("plant_out"))
            plant_core = core_months(cell.get("plant_out"))
            harvest_core = core_months(cell.get("harvest"))
            declared = declared_heat_months(cell)
            for i in range(12):
                tok = cal[i]
                m = i + 1
                mon = _MON_ABBR[i]
                if tok in _FROST_PAUSE_TOKENS and m in plant:
                    out.append(f"{loc}: {tok} on plant_out month {mon} "
                               f"(a frost/dormancy pause cannot fall on an outdoor planting window)")
                elif tok == "cold_pause" and m in harvest_core:
                    out.append(f"{loc}: cold_pause on core harvest month {mon} "
                               f"(harvest display over-states into a frost month -- split the harvest "
                               f"or relabel the gap)")
                elif tok == "heat_pause" and m not in declared:
                    if m in plant_core:
                        out.append(f"{loc}: heat_pause on core plant_out month {mon} "
                                   f"not in declared heat_pause.months (pause displaces planting)")
                    elif m in harvest_core:
                        out.append(f"{loc}: heat_pause on core harvest month {mon} "
                                   f"not in declared heat_pause.months (pause displaces harvest)")
    return out


def heat_pause_backing_violations(crop):
    """B3 thermal-backing gate (whole_crop_gate A25). Wherever a frost_anchored annual's
    calendar SHOWS a `heat_pause` token, the cell must carry a backed `heat_pause` object:
    a non-empty `months` list, `basis_seasoned` prose stating the thermal reason, and >=1
    `sources`, each anchored by a URL in `anchoring_urls`. Closes audit B3 (a self-consistent
    heat_pause with zero climate justification ships clean -- a fabricated "too hot to sow"
    claim shown to a grower).

    A heat exclusion is a crop+region+zone PHYSIOLOGY claim, not a shared climate datum:
    in the same desert zone, carrot pauses Mar-Aug while zucchini pauses Jul-Aug. So backing
    lives at the cell (the chill prose-backstop pattern), not in a region table. This is a
    PRESENCE/SHAPE check, not a re-derivation; month<->calendar ALIGNMENT stays in
    `annual_coherence_violations` (A5), and placement stays in `annual_calendar_violations`
    (A24). No-op for non-frost_anchored crops. Returns a list of violation strings."""
    if crop.get("calendar_basis") != "frost_anchored":
        return []
    out = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            cal = cell.get("calendar")
            if not isinstance(cal, list) or "heat_pause" not in cal:
                continue                       # no heat claim shown -> nothing to back
            loc = f"{rk}.z{z}"
            hp = cell.get("heat_pause")
            if not isinstance(hp, dict):
                out.append(f"{loc}: calendar shows heat_pause but the cell carries no "
                           f"heat_pause object (unbacked -- needs months + basis_seasoned + source)")
                continue
            months = hp.get("months")
            if not (isinstance(months, list) and len(months) > 0):
                out.append(f"{loc}: heat_pause.months missing/empty (unbacked heat exclusion)")
            basis = hp.get("basis_seasoned")
            if not (isinstance(basis, str) and basis.strip()):
                out.append(f"{loc}: heat_pause.basis_seasoned prose missing "
                           f"(a heat exclusion needs a stated thermal reason)")
            sources = hp.get("sources")
            if not (isinstance(sources, list) and len(sources) >= 1
                    and all(isinstance(s, str) and s.strip() for s in sources)):
                out.append(f"{loc}: heat_pause.sources missing/empty (>=1 Tier-1 source required)")
            else:
                urls = hp.get("anchoring_urls")
                urls = urls if isinstance(urls, dict) else {}
                for s in sources:
                    a = urls.get(s)
                    if not (isinstance(a, dict) and isinstance(a.get("url"), str) and a["url"].strip()):
                        out.append(f"{loc}: heat_pause source '{s}' has no anchoring_urls URL "
                                   f"(citation not anchored)")
    return out
