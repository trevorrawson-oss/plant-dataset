#!/usr/bin/env python3
"""Harvest duration-coherence: a cell's window must be reachable by its own stated duration
(the asparagus three-month artifact class, 2026-07-27).

THE DEFECT THIS EXISTS FOR. After the 2026-07-27 harvest re-source, 24 of asparagus's 29
renderable windows were exactly three calendar months, and six cells carried notes whose own
sourced content contradicted the field: mid_south z7 said "four to six weeks into May" under an
'Apr - Jun' field while its cited MU G6405 states "April 14 to May 30"; northern_tier z5's note
put emergence in "early to mid May" while the field painted April. Every instance was found by a
human reading cells; A34/A36/A29 check that notes EXIST and are dual-register, never what they
SAY. This gate reads the note against the field, mechanically.

THE SEMANTICS IT ENFORCES (ruled 2026-07-27, docs/2026-07-27-harvest-window-semantics-ruling.md).
`harvest` strings are month-granular TOUCH-SETS: "Mar - May" claims harvest occurs somewhere in
each named month. The renderer paints every touched month as a full "harvest" cell (plant-astro
succession.ts discards day numbers), so a named month is a promise, and a month may be named only
if the cell's sourced duration can actually reach it.

THREE SUB-CHECKS, each only where the note gives it something to check:
  REACH  a stated duration ("six to eight weeks") must reach the field's last month from the
         15th of its first month (mid-month convention: starts are month-granular or modeled,
         so mid-month is the unbiased anchor; explicit source dates govern over this arithmetic
         and are settled at authoring time, not here).
  END    a stated harvest end month ("into May", "through March and April") must equal the
         field's last month.
  START  a stated spear-emergence month must equal the field's first month.

SCOPE -- roster-wide, and the width is MEASURED rather than hopeful. On canonical 02fbb5e8:
1,120 renderable month-granular single-window harvest cells across 120 crops; the note-parse
matches anything at all on exactly one crop (asparagus: 15 durations, 27 ends, 28 starts) and
flags 8 findings on 6 cells, all six confirmed real against their cited sources. Zero false
flood anywhere, so there is nothing to narrow: today this is materially an asparagus-idiom check,
kept roster-wide so artichoke (same archetype, same prose conventions, mid-cert) and any later
duration-stating crop buy the check with no scope change.

Clause hygiene: bare "cut" counts as a harvest verb only when it is not fern/irrigation
housekeeping ("cut irrigation", "cut them to the ground", "cut the ferns off/down/back") --
the ca_desert z10 note is the false-positive shape this guards against, and the test suite
pins it.

SOFT, and soft is a stage not a resting state (the zone_order_gate pattern). NOT yet wired into
whole_crop_gate because that file carries the artichoke session's uncommitted A48. HARD-FLIP
TRIGGER: fold in alongside A48/A49 once artichoke certifies. Precedent: control_ladder_gate,
variety_resistance_gate, zone_order_gate.

Usage: python3 tools/harvest_duration_gate.py [crops_data_final.json]
Exit 1 on any violation.
"""
import calendar
import json
import re
import sys

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
_ABBR = {m[:3]: i + 1 for i, m in enumerate(MONTHS)}
_WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}

_MONTH_RE = "|".join(MONTHS) + "|" + "|".join(_ABBR)
_NUM_RE = r"(?:\d+|" + "|".join(_WORDNUM) + ")"
_MOD_RE = r"(?:early\s+|mid\s+|mid-|late\s+|early to mid\s+)?"
_RANGE_SEP = r"(?:\s+to\s+|\s*-\s*to\s*-\s*|\s*[-–]\s*)"


def _month(tok):
    return _ABBR.get(tok.strip().title()[:3])


def _num(tok):
    tok = tok.lower()
    return int(tok) if tok.isdigit() else _WORDNUM[tok]


def field_months(harvest):
    """(start_month, end_month) of a single-window month-granular field, else None.

    None (= skip, never guess) for: absent/blank, two-cycle comma windows, day-granular
    windows ("Mar 20 - Apr 15"), non-month tokens ("Year round").
    """
    if not isinstance(harvest, str) or "," in harvest or any(ch.isdigit() for ch in harvest):
        return None
    parts = [p.strip() for p in harvest.split("-")]
    if len(parts) != 2:
        return None
    a, b = _month(parts[0]), _month(parts[1])
    if a is None or b is None:
        return None
    return a, b


def harvest_clauses(note):
    """Note segments (split on . and ;) that talk about harvesting or cutting SPEARS.

    Bare "cut" is a harvest verb only when not fern/irrigation housekeeping: "cut irrigation",
    "cut them to the ground", "cut it/the ferns off/down/back" are about ending the season,
    not about harvest, and reading them as harvest produced the ca_desert z10 false positive.
    """
    out = []
    for seg in re.split(r"[.;]", note or ""):
        if re.search(r"\b(harvest\w*|spears?)\b", seg, re.I):
            out.append(seg)
        elif re.search(r"\bcut(?:ting)?s?\b(?!\s+(?:irrigation|them\b|it\b|the\s+ferns?|off\b|down\b|back\b))",
                       seg, re.I):
            out.append(seg)
    return out


def stated_duration(note):
    """(wmin, wmax) weeks stated in a harvest clause, else None."""
    for seg in harvest_clauses(note):
        # "six to eight weeks", "6-8 weeks", and the compound-adjective form
        # "a roughly six-to-eight-week window" (harvest_ready_seasoned's shape).
        # The separator must treat "-to-" as one unit: a bare `-` alternative would
        # consume only the first hyphen and then fail to match "to" as a number.
        m = re.search(rf"({_NUM_RE}){_RANGE_SEP}({_NUM_RE})[-\s]+weeks?", seg, re.I)
        if m:
            return _num(m.group(1)), _num(m.group(2))
        m = re.search(rf"(?:about|up to(?: about)?|for(?: about)?)\s+({_NUM_RE})\s+weeks?", seg, re.I)
        if m:
            w = _num(m.group(1))
            return w, w
    return None


def stated_end(note):
    """Harvest end month explicitly stated in a harvest clause, else None."""
    for seg in harvest_clauses(note):
        m = re.search(rf"(?:into|until|through)\s+{_MOD_RE}({_MONTH_RE})\b"
                      rf"(?:\s+and\s+{_MOD_RE}({_MONTH_RE})\b)?", seg, re.I)
        if m:
            return _month(m.group(2) or m.group(1))
    return None


def stated_start(note):
    """Spear-emergence month stated in the note, else None."""
    m = re.search(rf"\bspears?\b[^.;]*?\b(?:emerge|start|push|break|come|follow|begin)[^.;]*?"
                  rf"\b(?:in|by)\s+{_MOD_RE}({_MONTH_RE})\b", note or "", re.I)
    if m:
        return _month(m.group(1))
    return None


def _days_mid_to_first(m1, mk):
    """Days from the 15th of month m1 to the 1st of month mk (forward, may wrap the year)."""
    days = calendar.mdays[m1] - 15
    m = m1 % 12 + 1
    while m != mk:
        days += calendar.mdays[m]
        m = m % 12 + 1
    return days + 1


def duration_violations(crop):
    """List of violation strings ('region z<zone>: KIND: ...'), [] = clean."""
    out = []
    if not isinstance(crop, dict):
        return out
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            fm = field_months(cell.get("harvest"))
            if not fm:
                continue
            m1, mk = fm
            note = cell.get("notes", "")
            dur = stated_duration(note)
            if dur and m1 != mk:
                wmax = dur[1]
                need = _days_mid_to_first(m1, mk)
                if wmax * 7 < need:
                    out.append(
                        f"{rk} z{z}: REACH: field {cell['harvest']!r} needs {need} days from "
                        f"mid-{MONTHS[m1-1]} to touch {MONTHS[mk-1]}, but the note's stated "
                        f"duration tops out at {wmax} weeks = {wmax*7} days. A named month the "
                        f"duration cannot reach is a promise the data does not keep."
                    )
            end = stated_end(note)
            if end is not None and end != mk:
                out.append(
                    f"{rk} z{z}: END: note states harvest ends {MONTHS[end-1]} but field "
                    f"{cell['harvest']!r} ends {MONTHS[mk-1]}. The cell contradicts itself; "
                    f"read the sources to decide which half is the correct one before editing "
                    f"either (docs/2026-07-27-harvest-window-semantics-ruling.md §2)."
                )
            start = stated_start(note)
            if start is not None and start != m1:
                out.append(
                    f"{rk} z{z}: START: note states spears emerge in {MONTHS[start-1]} but field "
                    f"{cell['harvest']!r} starts {MONTHS[m1-1]}. A painted month before emergence "
                    f"is the northern_tier z5 defect shape."
                )
    return out


def ramp_violations(crop):
    """RAMP-FIRST: the ramp's first harvestable bed year must equal the earliest
    year `years_to_first_harvest` allows. See the module header for why equality,
    not range-containment, is the correct rule."""
    ramp = crop.get("harvest_ramp_weeks")
    ytfh = crop.get("years_to_first_harvest")
    if not isinstance(ramp, list) or not ramp:
        return []
    if not (isinstance(ytfh, list) and len(ytfh) == 2 and all(isinstance(x, int) for x in ytfh)):
        return []
    nonzero = [e["bed_year"] for e in ramp
               if isinstance(e, dict) and isinstance(e.get("weeks"), list)
               and len(e["weeks"]) == 2 and e["weeks"][1] > 0
               and isinstance(e.get("bed_year"), int)]
    if not nonzero:
        return [f"RAMP-FIRST: harvest_ramp_weeks has no bed year with a non-zero max, but "
                f"years_to_first_harvest is {ytfh}, which promises a harvest."]
    first, earliest = min(nonzero), min(ytfh)
    if first != earliest:
        return [f"RAMP-FIRST: harvest_ramp_weeks first opens in bed year {first}, but "
                f"years_to_first_harvest {ytfh} allows a harvest as early as year "
                f"{earliest}. Where the establishment literature disagrees the ramp must "
                f"CARRY THE RANGE (an optional [0, N] year), not collapse to the "
                f"conservative end. This is the year-2 [0,0] defect."]
    return []


def _mature_ramp(crop):
    """The highest authored bed_year's weeks, or None."""
    ramp = crop.get("harvest_ramp_weeks")
    if not isinstance(ramp, list) or not ramp:
        return None
    entries = [e for e in ramp if isinstance(e, dict)
               and isinstance(e.get("bed_year"), int)
               and isinstance(e.get("weeks"), list) and len(e["weeks"]) == 2]
    if not entries:
        return None
    top = max(entries, key=lambda e: e["bed_year"])
    return top["bed_year"], top["weeks"]


def ramp_prose_violations(crop):
    """RAMP-PROSE: a bare week count in the crop's harvest_ready_* prose must equal
    the ramp's mature entry. Equality, not overlap: [6,8] and [8,10] share an
    endpoint and are still two different claims about the same bed."""
    mature = _mature_ramp(crop)
    if mature is None:
        return []
    bed_year, weeks = mature
    out = []
    for reg in ("harvest_ready_beginner", "harvest_ready_seasoned"):
        text = crop.get(reg)
        if not isinstance(text, str):
            continue
        dur = stated_duration(text)
        if dur and list(dur) != list(weeks):
            out.append(
                f"RAMP-PROSE: {reg} states {dur[0]} to {dur[1]} weeks but "
                f"harvest_ramp_weeks bed year {bed_year} says {weeks[0]} to {weeks[1]}. "
                f"Two layers of the same crop make different duration claims; decide "
                f"which is sourced before editing either."
            )
    return out


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    hit = set()
    for crop in data["crops"]:
        for v in duration_violations(crop):
            print(f"  {crop.get('slug')}: {v}")
            total += 1
            hit.add(crop.get("slug"))
    print(f"harvest duration gate: {total} violation(s) across {len(hit)} crop(s) / "
          f"{len(data['crops'])} scanned (roster-wide; see header for measured-scope numbers)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"))
