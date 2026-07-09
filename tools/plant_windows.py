#!/usr/bin/env python3
"""plant_windows.py -- THE shared date-window parser for resolved-cell window strings.

Used by BOTH the de-mux batch generator and second_planting_gate (A43) so the
migration and its gate can never disagree on what counts as a window (spec
2026-07-09 §4). Never a naive comma split: parenthetical commas
("Apr - May (dormant, bare-root)") and " or "-joined alternatives
("Oct - Nov or Feb - Mar") are NOT multi-window shapes.

Grammar (paren-strip first, then split on top-level commas into CHUNKS):
  chunk       = alternative (" or " alternative)*   # alternatives = ONE choice
  alternative = span
  span        = month [day] ["-" month [day]]       # "Mar 15 - Apr 15" | "Jan - March" | "Aug"
Full month names AND 3-letter abbreviations parse. A chunk with no parseable
span (free prose) yields no Span.
"""
import re
from collections import namedtuple

_FULL = ["january", "february", "march", "april", "may", "june", "july",
         "august", "september", "october", "november", "december"]
MONTH_NUM = {}
for _i, _name in enumerate(_FULL, 1):
    MONTH_NUM[_name] = _i
    MONTH_NUM[_name[:3]] = _i

# full names FIRST in the alternation so "March" wins over "Mar"+residue
_MON = "|".join(_FULL + sorted({n[:3] for n in _FULL}))
SPAN_RE = re.compile(rf"\b({_MON})\b\s*(\d{{1,2}})?\s*(?:-\s*\b({_MON})\b\s*(\d{{1,2}})?)?",
                     re.IGNORECASE)
PAREN_RE = re.compile(r"\([^)]*\)")
_OR_RE = re.compile(r"\s+or\s+", re.IGNORECASE)

Span = namedtuple("Span", "raw start_text end_text start_month start_day "
                          "end_month end_day n_alternatives")


def spans(s):
    """Parse a window string into its comma-joined Spans. None/non-str -> []."""
    if not isinstance(s, str):
        return []
    out = []
    for chunk in PAREN_RE.sub("", s).split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        alts = _OR_RE.split(chunk)
        m = SPAN_RE.search(alts[0])
        if not m:
            continue
        sm = MONTH_NUM[m.group(1).lower()]
        sd = int(m.group(2)) if m.group(2) else None
        if m.group(3):
            em = MONTH_NUM[m.group(3).lower()]
            ed = int(m.group(4)) if m.group(4) else None
        else:
            em, ed = sm, sd
        start_text = m.group(1) + (f" {m.group(2)}" if m.group(2) else "")
        end_text = (m.group(3) + (f" {m.group(4)}" if m.group(4) else "")) if m.group(3) else start_text
        out.append(Span(chunk, start_text, end_text, sm, sd, em, ed, len(alts)))
    return out


def window_count(s):
    """How many discrete comma-joined windows a string carries (' or ' counts once)."""
    return len(spans(s))


def single_date(s):
    """'Mar 15' / 'Jun' / 'March' -> (month, day|None); ranges/multi/None -> None."""
    sp = spans(s)
    if len(sp) != 1:
        return None
    p = sp[0]
    if (p.start_month, p.start_day) != (p.end_month, p.end_day):
        return None
    return (p.start_month, p.start_day)


def in_span(md, span):
    """Is (month, day|None) inside span? Wrap-aware; a missing day defaults to 15."""
    m, d = md[0], (md[1] if md[1] is not None else 15)
    a = (span.start_month, span.start_day or 1)
    b = (span.end_month, span.end_day or 31)
    p = (m, d)
    if a <= b:
        return a <= p <= b
    return p >= a or p <= b  # window wraps the year end


def months_overlap(x, y):
    """Do two Spans share any month? Wrap-aware, month granularity."""
    def mset(sp):
        m, out = sp.start_month, {sp.start_month}
        while m != sp.end_month:
            m = m % 12 + 1
            out.add(m)
        return out
    return bool(mset(x) & mset(y))
