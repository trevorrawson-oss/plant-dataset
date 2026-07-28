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

SEVEN SUB-CHECKS now live here, FOUR per-cell (inside `duration_violations`) and three crop-level
(one call each per crop, wired together in `main`):

  Per-cell, each only where the note gives it something to check:
  REACH          a stated duration ("six to eight weeks") must reach the field's last month from
                 the 15th of its first month (mid-month convention: starts are month-granular or
                 modeled, so mid-month is the unbiased anchor; explicit source dates govern over
                 this arithmetic and are settled at authoring time, not here). Where a cell
                 carries a structured `harvest_duration_weeks` override, the override is
                 authoritative over the note parse for REACH (a source-carried number is more
                 trustworthy than a regex read of prose).
  END            a stated harvest end month ("into May", "through March and April") must equal
                 the field's last month.
  START          a stated spear-emergence month must equal the field's first month.
  OVERRIDE-PROSE where a cell carries BOTH a structured `harvest_duration_weeks` override AND a
                 note that itself states a week count, the two must agree. A structured field and
                 free-text prose making different claims about the same cell is the same class of
                 self-contradiction REACH/END/START catch between field and note; this catches it
                 between two different representations of duration.

  Crop-level, each scanning the whole crop once (not per-cell):
  RAMP-FIRST  (`ramp_violations`) the ramp's first harvestable bed year must EQUAL the earliest
              year `years_to_first_harvest` allows, not merely fall within it. Rationale for
              equality over range-containment: `years_to_first_harvest: [2,3]` on asparagus
              encodes a genuine source disagreement (UMN/Missouri permit a light second-spring
              cut; MSU/UNH say wait for year three). Requiring the ramp's first non-zero bed year
              to equal the minimum forces the ramp to keep year 2 open, which `[0,2]` honestly
              encodes. A range-containment check would PASS on the very defect the rule exists
              for: a ramp whose first non-zero year is 3 would satisfy "the ramp's first
              harvestable year is somewhere in years_to_first_harvest," because 3 is inside
              [2,3], even though it silently drops the year-2 possibility the sources disagree on.
  RAMP-PROSE  (`ramp_prose_violations`) a bare week count stated in the crop's `harvest_ready_*`
              prose must equal the ramp's mature (highest bed_year) entry, again by equality: a
              stated [6,8] and a ramp of [8,10] share an endpoint but are still two different
              claims about the same mature bed.
  STOP-SHAPE  (`stop_rule_violations`) `harvest_stop_rule`, where present, is well-formed
              (known signal, non-descending threshold range, dual-register prose, sourced).
              Absence is the legitimate N/A branch and is silent.

SCOPE -- roster-wide, and the width is MEASURED rather than hopeful. On canonical 02fbb5e8:
1,120 renderable month-granular single-window harvest cells across 120 crops; the note-parse
matches anything at all on exactly one crop (asparagus: 15 durations, 27 ends, 28 starts) and
flags 8 findings on 6 cells, all six confirmed real against their cited sources.

THAT MEASUREMENT'S "ZERO FALSE FLOOD" CLAIM WAS TRUE AND MISLEADING, and the correction is worth
keeping. It was taken when asparagus was the only crop in the canonical with parseable harvest
prose, so it measured this parser against ONE crop's idiom. Run against artichoke's staged cells
(#121, the archetype's other member) it produced FOUR FALSE POSITIVES on 39 cells -- a seedling
vernalization week count and three planting windows, all read as harvest. Artichoke writes long
comma-chained sentences that carry a planting window and a harvest window together; asparagus
writes short ones. Both defects are fixed below (comma-level clause splitting with forward
inheritance; harvest-anchored, last-match end months) and artichoke's real prose is pinned in
the test suite. THE LESSON: "no false positives" measured on a single crop's writing style is a
statement about that style, not about the parser. Re-measure when a new idiom arrives.

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

# Observable stop signals. Extend as archetypes join; an unknown value is a defect,
# because the app dispatches display on it.
STOP_SIGNALS = {"spear_diameter"}


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


_HARVEST_WORD = re.compile(r"\b(harvest\w*|spears?)\b", re.I)
# bare "cut" counts only when it is not fern/irrigation housekeeping
_CUT_WORD = re.compile(
    r"\bcut(?:ting)?s?\b(?!\s+(?:irrigation|them\b|it\b|the\s+ferns?|off\b|down\b|back\b))", re.I)


def harvest_clauses(note):
    """Note segments that talk about harvesting or cutting.

    SPLIT ON COMMAS AS WELL AS . AND ;, and the comma is load-bearing. Asparagus writes short
    sentences, so sentence-level segmentation was enough for it. Artichoke -- the second crop
    this gate met -- chains a PLANTING window and a HARVEST window into one comma-separated
    sentence ("marks artichoke for transplanting from mid January through March, ... and gives
    four to six months to harvest"), and at sentence granularity the planting month and a
    seedling VERNALIZATION week count ("seedlings chilled about three weeks near 40°F") were
    both attributed to harvest. Four false positives on 39 staged cells, all from this.

    Bare "cut" is a harvest verb only when not fern/irrigation housekeeping: "cut irrigation",
    "cut them to the ground", "cut it/the ferns off/down/back" are about ending the season,
    not about harvest, and reading them as harvest produced the ca_desert z10 false positive.
    """
    out = []
    for sentence in re.split(r"[.;]", note or ""):
        carry = False
        for seg in sentence.split(","):
            if _HARVEST_WORD.search(seg) or _CUT_WORD.search(seg):
                carry = True
                out.append(seg)
            elif carry:
                # a comma CONTINUATION of a harvest clause is still about harvest:
                # "so harvest from March into mid May, up to about ten weeks once the bed is
                # four years old". Splitting naively severed that duration from its clause and
                # silently dropped REACH coverage on a live cell. Inheritance runs FORWARD only
                # and resets at . and ; -- artichoke's "seedlings chilled about three weeks ...,
                # and harvest continuing into early October" must NOT reach backward for it.
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
    """Harvest end month stated in a harvest clause, else None.

    TWO RULES, both bought with false positives on real prose:

    HARVEST-ANCHORED. The month phrase counts only if a harvest word appears BEFORE it inside
    the same segment. Without this, "puts artichoke in from September through October and
    harvests it in May and June" reads its PLANTING window as the harvest end -- the segment
    qualifies (it says "harvests"), but the "through October" belongs to the planting half.

    LAST MATCH, NOT FIRST. A note may name the harvest start and the harvest end with the same
    preposition: "pulls first harvest forward INTO JULY and lets picking run INTO OCTOBER". The
    end is the later one; taking the first read a start as an end.
    """
    found = None
    for seg in harvest_clauses(note):
        for m in re.finditer(rf"(?:into|until|through)\s+{_MOD_RE}({_MONTH_RE})\b"
                             rf"(?:\s+and\s+{_MOD_RE}({_MONTH_RE})\b)?", seg, re.I):
            before = seg[:m.start()]
            # the anchor predicate must be the SAME one that qualifies a segment, or a
            # legitimate "cut for six to eight weeks into May" loses its end month
            if not (_HARVEST_WORD.search(before) or _CUT_WORD.search(before)):
                continue
            found = _month(m.group(2) or m.group(1))
    return found


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
            note_dur = stated_duration(note)
            ov = cell.get("harvest_duration_weeks")
            has_ov = (isinstance(ov, list) and len(ov) == 2
                      and all(isinstance(x, int) for x in ov))
            if has_ov and note_dur and list(note_dur) != list(ov):
                out.append(
                    f"{rk} z{z}: OVERRIDE-PROSE: harvest_duration_weeks is "
                    f"{ov[0]}-{ov[1]} weeks but the note states {note_dur[0]}-{note_dur[1]}. "
                    f"The structured override and the prose must agree."
                )
            # a structured override is authoritative over the note parse for REACH
            dur = tuple(ov) if has_ov else note_dur
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


# Crop-level subtrees RAMP-PROSE does not read. `regions`/`zones` are per-cell prose,
# which duration_violations owns and which needs the harvest-clause filter. The rest is
# the audit record and citation machinery, never rendered.
_CROP_PROSE_SKIP_TOP = {"regions", "zones", "verification_status", "sources_summary",
                        "varieties"}


def _crop_prose_strings(crop):
    """Yield (path, text) for every crop-level consumer string."""
    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "sources" or "anchoring_urls" in k:
                    continue
                yield from walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from walk(v, f"{path}[{i}]")
        elif isinstance(node, str):
            yield path, node

    for k, v in crop.items():
        if k in _CROP_PROSE_SKIP_TOP:
            continue
        yield from walk(v, k)


def _bare_week_range(text):
    """(min, max) from an 'N to M weeks' anywhere in the text, else None.

    Deliberately NOT filtered to harvest clauses, unlike the per-cell checks. Cell notes
    need that filter to dodge fern/irrigation housekeeping ("cut irrigation"), but a
    CROP-level week count is about this crop's harvest even when its sentence carries no
    harvest verb -- `notifications[].body_seasoned` opens "You are near the end of the
    roughly six-to-eight-week window", which the clause filter drops on the floor.
    """
    m = re.search(rf"({_NUM_RE}){_RANGE_SEP}({_NUM_RE})[-\s]+weeks?", text, re.I)
    return (_num(m.group(1)), _num(m.group(2))) if m else None


def ramp_prose_violations(crop):
    """RAMP-PROSE: a bare week count in ANY crop-level consumer string must equal the
    ramp's mature entry.

    Equality, not overlap: [6,8] and [8,10] share an endpoint and are still two different
    claims about the same bed.

    SCOPE IS EVERY CROP-LEVEL STRING, and the width is the point. This check first shipped
    reading only `harvest_ready_*`, and that narrowness is exactly why nine other asparagus
    strings went on asserting a superseded six-to-eight-week figure -- in the guide body,
    the stage cards, the watering note, a tip callout and a notification -- while the gate
    reported clean. Measured: the widening is a no-op on every crop without a ramp, which
    today is all of them but one, so there is no flood to narrow away from.
    """
    mature = _mature_ramp(crop)
    if mature is None:
        return []
    bed_year, weeks = mature
    out = []
    for path, text in _crop_prose_strings(crop):
        dur = _bare_week_range(text)
        if dur and list(dur) != list(weeks):
            out.append(
                f"RAMP-PROSE: {path} states {dur[0]} to {dur[1]} weeks but "
                f"harvest_ramp_weeks bed year {bed_year} says {weeks[0]} to {weeks[1]}. "
                f"Two layers of the same crop make different duration claims; decide "
                f"which is sourced before editing either."
            )
    return out


def stop_rule_violations(crop):
    """STOP-SHAPE: harvest_stop_rule, where present, is well-formed. Absence is the
    legitimate N/A branch (a crop with no repeated-cutting season has no stop rule)
    and is silent."""
    rule = crop.get("harvest_stop_rule")
    if rule is None:
        return []
    if not isinstance(rule, dict):
        return ["STOP-SHAPE: harvest_stop_rule must be an object."]
    out = []
    if rule.get("signal") not in STOP_SIGNALS:
        out.append(f"STOP-SHAPE: harvest_stop_rule.signal {rule.get('signal')!r} is not one "
                   f"of {sorted(STOP_SIGNALS)}.")
    t = rule.get("threshold_inches")
    if not (isinstance(t, list) and len(t) == 2
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in t)
            and t[0] <= t[1]):
        out.append(f"STOP-SHAPE: harvest_stop_rule.threshold_inches must be [min, max] "
                   f"non-descending numbers, got {t!r}. Where sources disagree on the number "
                   f"this CARRIES THE RANGE; equal values are allowed when they agree.")
    for k in ("note_beginner", "note_seasoned"):
        if not isinstance(rule.get(k), str) or not rule[k].strip():
            out.append(f"STOP-SHAPE: harvest_stop_rule.{k} must be non-empty dual-register prose.")
    if not rule.get("sources"):
        out.append("STOP-SHAPE: harvest_stop_rule.sources must name at least one source, and only "
                   "documents verified to carry the rule.")
    return out


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    hit = set()
    for crop in data["crops"]:
        crop_level = (ramp_violations(crop) + ramp_prose_violations(crop)
                      + stop_rule_violations(crop))
        for v in crop_level + duration_violations(crop):
            print(f"  {crop.get('slug')}: {v}")
            total += 1
            hit.add(crop.get("slug"))
    print(f"harvest duration gate: {total} violation(s) across {len(hit)} crop(s) / "
          f"{len(data['crops'])} scanned (roster-wide; see header for measured-scope numbers)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"))
