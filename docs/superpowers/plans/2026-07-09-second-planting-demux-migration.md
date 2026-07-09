# second_planting De-mux Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the second_planting split (90 TWO_CROP cells extracted, 64 pop-1 cells deduped, 11 alt-window cells or-normalized) and gate the old comma-string shape out of existence, staged so the UI never loses the fall crop.

**Architecture:** One shared window parser (`tools/plant_windows.py`) feeds both a deterministic batch generator (`tools/build_demux_batches.py`, emits `apply_patch.py` batches, never writes canonical) and the new gate (`tools/second_planting_gate.py`, wired as whole_crop_gate A43 in two stages). Three releases: S1 populate (additive) -> S2 plant-astro read-flip -> S3 clean.

**Tech Stack:** Python 3 stdlib only (repo convention), plain-assert test scripts in `tools/test_*.py`, `tools/apply_patch.py` for all canonical writes, plant-astro (Astro/TS) for Stage 2.

**Spec:** `docs/superpowers/specs/2026-07-09-second-planting-demux-migration-design.md` -- read it first; §2 carries every ruling.

## Global Constraints

- **READ-ONLY on `crops_data_final.json`** except the explicit per-batch promotes (Tasks 5-7, 11). Only `apply_patch.py` output ever replaces it.
- **Canonical JSON is COMPACT:** `separators=(",",":")`, `ensure_ascii=False`, NO trailing newline, never `indent=2`. Crop count stays 124.
- **Trevor approves every commit; Trevor confirms every push.** Stop and ask at each commit step.
- **TDD:** every new module gets its failing test run (RED) before implementation (GREEN). The gate is additionally adversarially proven on a scratch copy of the REAL canonical.
- **Scratch files** go in the session scratchpad dir (`$SCRATCH` below), never `/tmp`, never the repo root.
- CURRENT_STATE.md is HAND-MAINTAINED (memory `current-state-md-drift`): prepend the new entry surgically; NEVER run `gen_current_state.py`.
- No em dashes anywhere in dataset strings; `--` fine in docs/commits/code comments.
- Start SHA at plan time: `1372c299...` -- every batch generator run re-reads the CURRENT canonical and stamps its live SHA; apply_patch enforces it.

Set once per session: `export SCRATCH=/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/d1e3c529-c838-4cf1-8e6c-5f875df4ef31/scratchpad`

---

### Task 1: Shared window parser `tools/plant_windows.py`

**Files:**
- Create: `tools/plant_windows.py`
- Test: `tools/test_plant_windows.py`

**Interfaces:**
- Produces: `spans(s) -> [Span]` where `Span = namedtuple("Span", "raw start_text end_text start_month start_day end_month end_day n_alternatives")` (months 1-12, days int or None, texts like `"Nov 1"`); `window_count(s) -> int`; `single_date(s) -> (month, day|None) | None`; `in_span((m,d|None), Span) -> bool` (wrap-aware); `months_overlap(Span, Span) -> bool` (wrap-aware). All tolerate None/non-str input (`[]`/`0`/`None`/`False`).

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/plant-dataset && python3 tools/test_plant_windows.py`
Expected: `ModuleNotFoundError: No module named 'plant_windows'`

- [ ] **Step 3: Write the implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_plant_windows.py`
Expected: `plant_windows tests: OK`

- [ ] **Step 5: Commit (ASK TREVOR FIRST)**

```bash
git add tools/plant_windows.py tools/test_plant_windows.py
git commit -m "feat(demux): shared window parser (plant_windows) -- parens/or/full-months/single-month proof"
```

---

### Task 2: Gate module `tools/second_planting_gate.py`

**Files:**
- Create: `tools/second_planting_gate.py`
- Test: `tools/test_second_planting_gate.py`

**Interfaces:**
- Consumes: `plant_windows.spans/window_count/single_date/in_span`.
- Produces: `check_crop(crop: dict, rules=frozenset("AB")) -> list[str]` (violation strings; empty = clean). CLI: `python3 tools/second_planting_gate.py [crops.json] [--rules B|A|AB]`, exit 1 on any violation. Task 8 wires `check_crop` into whole_crop_gate as A43 with `rules=frozenset("B")`; Task 12 flips to `frozenset("AB")`.

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""second_planting_gate tests -- one synthetic fixture per defect/exempt class
(spec 2026-07-09 §6). Fixtures are self-contained; the adversarial proof on the
REAL canonical is a Task-8/12 wiring step, not a permanent test (canonical state
changes across stages)."""
from second_planting_gate import check_crop

SP = {"start_indoors": None, "plant_out": "Sep 1 - Sep 20",
      "harvest_start": "Nov 1", "harvest_end": "Nov 30",
      "sources": ["x"], "anchoring_urls": {"x": {"url": "https://e.edu", "verified": "2026-07-09"}}}


def crop(suitable, cell, slug="fixture"):
    return {"slug": slug, "succession_policy": {"suitable": suitable},
            "regions": {"r1": {"resolved_by_zone": {"8": cell}}}}


def cell(**kw):
    base = {"start_indoors": None, "plant_out": "Mar 15 - Apr 15",
            "harvest": "May 15 - Jun 30", "harvest_start": "May 15",
            "harvest_end": "Jun 30", "first_plant_date": "Mar 15",
            "last_plant_date": "Apr 15"}
    base.update(kw)
    return base


B = frozenset("B"); A = frozenset("A"); AB = frozenset("AB")

# --- Rule B fires: old comma shape, no second_planting, suitable=false
bad = crop(False, cell(plant_out="Mar 15 - Apr 15, Sep 1 - Sep 20",
                       harvest="May 15 - Jun 30, Nov 1 - Nov 30"))
assert len(check_crop(bad, B)) == 1, check_crop(bad, B)
# --- Rule B fires on a doubled start_indoors too
bad_si = crop(False, cell(start_indoors="Feb 1 - Feb 20, Jun 20 - Jul 10"))
assert len(check_crop(bad_si, B)) == 1
# --- exempt: suitable=true cadence (Decision A)
assert check_crop(crop(True, cell(plant_out="Mar 1 - May 15, Aug 1 - Sep 15")), B) == []
# --- exempt: " or " alternatives (woody herbs / or-normalized alliums)
assert check_crop(crop(False, cell(plant_out="Oct - Nov or Feb - Mar")), B) == []
# --- exempt: harvest-only doubling (reflush peppers, chives/mint)
assert check_crop(crop(False, cell(harvest="May 20 - Jun 30, Sep 10 - Dec 1")), B) == []
# --- exempt: parenthetical comma (peach)
assert check_crop(crop(False, cell(plant_out="Apr - May (dormant, bare-root)")), B) == []
# --- exempt from B: second_planting present (that is Rule A's territory)
mixed = crop(False, cell(plant_out="Mar 15 - Apr 15, Sep 1 - Sep 20",
                         second_planting=dict(SP)))
assert check_crop(mixed, B) == []

# --- Rule A fires: still-doubled top-level alongside second_planting
assert len(check_crop(mixed, A)) == 1, check_crop(mixed, A)
# --- Rule A fires: envelope still carries the fall cycle (harvest_end == sp.harvest_end)
env = crop(False, cell(second_planting=dict(SP), harvest_end="Nov 30"))
assert any("harvest_end" in v for v in check_crop(env, A)), check_crop(env, A)
# --- Rule A fires: last_plant_date sits inside the second_planting window
env2 = crop(False, cell(second_planting=dict(SP), last_plant_date="Sep 20"))
assert any("last_plant_date" in v for v in check_crop(env2, A)), check_crop(env2, A)
# --- Rule A clean: fully de-muxed cell
clean = crop(False, cell(second_planting=dict(SP)))
assert check_crop(clean, AB) == [], check_crop(clean, AB)
# --- no second_planting, no multi-window: silent under both rules
assert check_crop(crop(False, cell()), AB) == []

print("second_planting_gate tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_second_planting_gate.py`
Expected: `ModuleNotFoundError: No module named 'second_planting_gate'`

- [ ] **Step 3: Write the implementation**

```python
#!/usr/bin/env python3
"""second_planting_gate.py -- A43: the de-mux invariant (spec 2026-07-09 §6).

Rule B (wired at Stage-1 close) -- NO UNSTRUCTURED COMMA SHAPE: on a crop with
succession_policy.suitable != True, a resolved cell with >= 2 comma-joined window
spans in start_indoors or plant_out and NO second_planting is a violation. This is
what blocks new crops from re-introducing the old shape. Doubling in `harvest`
alone is legitimate (reflush = two flushes of ONE planting: cayenne/habanero/
jalapeno hot cells, chives/mint); " or "-joined alternatives count once (woody-herb
establishment shape, or-normalized alliums/chard).

Rule A (wired at Stage-3 close) -- DEDUP INVARIANT: a cell WITH second_planting
must be single-span in start_indoors/plant_out/harvest, and its envelope must not
still carry the fall cycle: harvest_end must not parse-equal
second_planting.harvest_end, and last_plant_date must not sit inside the
second_planting plant_out window. (A targeted floor for the two real envelope
defect classes, not a general date audit.)

check_crop(crop, rules) -> [violation strings]. Standalone CLI for fixtures +
roster sweeps: python3 tools/second_planting_gate.py [crops.json] [--rules AB]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plant_windows import spans, window_count, single_date, in_span

PLANTING_FIELDS = ("start_indoors", "plant_out")
ALL_FIELDS = ("start_indoors", "plant_out", "harvest")


def _cells(crop):
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if isinstance(cell, dict):
                yield rk, z, cell


def check_crop(crop, rules=frozenset("AB")):
    v = []
    slug = crop.get("slug", "?")
    suitable = (crop.get("succession_policy") or {}).get("suitable")
    for rk, z, cell in _cells(crop):
        sp = cell.get("second_planting")
        has_sp = isinstance(sp, dict)
        if "B" in rules and not has_sp and suitable is not True:
            for f in PLANTING_FIELDS:
                n = window_count(cell.get(f))
                if n >= 2:
                    v.append(f"B unstructured comma shape: {rk}.{z} {f} carries "
                             f"{n} windows and no second_planting ({slug})")
        if "A" in rules and has_sp:
            for f in ALL_FIELDS:
                if window_count(cell.get(f)) >= 2:
                    v.append(f"A dedup: {rk}.{z} {f} still multi-window alongside "
                             f"second_planting ({slug})")
            he = single_date(cell.get("harvest_end"))
            sp_he = single_date(sp.get("harvest_end"))
            if he and sp_he and he == sp_he:
                v.append(f"A envelope: {rk}.{z} harvest_end still spans the fall "
                         f"cycle ({slug})")
            lpd = single_date(cell.get("last_plant_date"))
            sp_po = spans(sp.get("plant_out"))
            if lpd and sp_po and in_span(lpd, sp_po[0]):
                v.append(f"A envelope: {rk}.{z} last_plant_date sits inside the "
                         f"second_planting window ({slug})")
    return v


if __name__ == "__main__":
    import json
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="crops_data_final.json")
    ap.add_argument("--rules", default="AB", choices=["A", "B", "AB"])
    a = ap.parse_args()
    with open(a.path, encoding="utf-8") as fh:
        data = json.load(fh)
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data
    total = 0
    for c in crops:
        for msg in check_crop(c, frozenset(a.rules)):
            print("VIOLATION:", msg)
            total += 1
    print(f"second_planting_gate: {total} violations (rules={a.rules}, "
          f"crops={len(crops)})")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_second_planting_gate.py`
Expected: `second_planting_gate tests: OK`

- [ ] **Step 5: Baseline sweeps on the real canonical (evidence, not asserts)**

Run: `python3 tools/second_planting_gate.py crops_data_final.json --rules B`
Expected: exit 1; violations span exactly **101 cells** (90 TWO_CROP + 11 ALT_WINDOW). The LINE count runs slightly higher (a cell with both planting fields doubled emits 2 lines, e.g. onion ca_interior) -- record the exact line count as the baseline for the per-batch drop checks in Tasks 5-7. Zero violations on any suitable=true, woody-herb, chives/mint, reflush, or perennial-tree crop -- spot-check the output for lavender/mint/peach/carrot absence.

Run: `python3 tools/second_planting_gate.py crops_data_final.json --rules A`
Expected: exit 1; violations ONLY on the 7 pop-1 crops' 48 mixed cells (the 16 fully de-muxed pop-1 cells must NOT appear -- if any do, STOP: the envelope floor is misfiring; investigate before wiring anything).

- [ ] **Step 6: Commit (ASK TREVOR FIRST)**

```bash
git add tools/second_planting_gate.py tools/test_second_planting_gate.py
git commit -m "feat(gate): second_planting de-mux gate module (A43 rules A+B, unwired; TDD 11 classes)"
```

---

### Task 3: Batch generator `tools/build_demux_batches.py`

**Files:**
- Create: `tools/build_demux_batches.py`
- Test: `tools/test_build_demux_batches.py`

**Interfaces:**
- Consumes: `plant_windows` (all helpers).
- Produces: CLI `python3 tools/build_demux_batches.py --stage populate|clean [--only <batchname>]` writing `tools/batches/second_planting_<name>.json` in apply_patch canonical format (`base_sha` = SHA of the canonical it just read). Pure functions used by tests: `classify(cell) -> "TWO_CROP"|"REFLUSH"|"ALT_WINDOW"|None`, `second_planting_value(cell) -> dict`, `or_norm_ops(slug, rk, z, cell) -> [op]`, `clean_ops(slug, rk, z, cell) -> [op]`.

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""build_demux_batches unit tests -- fixture cells lifted from the canonical
(bell-pepper se_gulf z8 = the spec's worked example; onion/shallot alt cells)."""
from build_demux_batches import classify, second_planting_value, or_norm_ops, clean_ops

BELL = {  # bell-pepper se_gulf z8, verbatim shape
    "start_indoors": None,
    "plant_out": "Mar 15 - Apr 15, Sep 1 - Sep 20",
    "harvest": "May 15 - Jun 30, Nov 1 - Nov 30",
    "harvest_start": "May 15", "harvest_end": "Nov 30",
    "first_plant_date": "Mar 15", "last_plant_date": "Sep 20",
    "sources": ["src_a"], "anchoring_urls": {"src_a": {"url": "https://x.edu", "verified": "2026-01-01"}},
}
REFLUSH = {"start_indoors": None, "plant_out": "Feb 1 - Mar 1",
           "harvest": "May 15 - Jun 30, Oct 1 - Dec 5"}
ALT = {"start_indoors": None, "plant_out": "Oct - Nov, Jan - March",
       "harvest": "Jun - Jul"}

assert classify(BELL) == "TWO_CROP"
assert classify(REFLUSH) == "REFLUSH"
assert classify(ALT) == "ALT_WINDOW"
assert classify({"plant_out": "Mar 15 - Apr 15", "harvest": "May 15 - Jun 30"}) is None

# extraction = the spec §2/§5 worked example, byte-exact
sp = second_planting_value(BELL)
assert sp == {"start_indoors": None, "plant_out": "Sep 1 - Sep 20",
              "harvest_start": "Nov 1", "harvest_end": "Nov 30",
              "sources": ["src_a"],
              "anchoring_urls": {"src_a": {"url": "https://x.edu", "verified": "2026-01-01"}}}, sp

# or-norm: comma -> " or "; the onion ca_north_coast continuity fix is special-cased
ops = or_norm_ops("shallot", "ca_interior", "8", ALT)
assert len(ops) == 1 and ops[0]["value"] == "Oct - Nov or Jan - March" and ops[0]["from"] == ALT["plant_out"]
fix = or_norm_ops("onion", "ca_north_coast", "9",
                  {"start_indoors": "Oct - Nov", "plant_out": "Nov - Jan, Jan - March", "harvest": "Jun"})
assert len(fix) == 1 and fix[0]["value"] == "Nov - March"
two_si = or_norm_ops("onion", "ca_interior", "8",
                     {"start_indoors": "Sep, Dec", "plant_out": "Oct - Nov, Jan - March", "harvest": "Jun - Jul"})
assert {o["value"] for o in two_si} == {"Sep or Dec", "Oct - Nov or Jan - March"}

# clean: strings -> primary span; envelope narrowed; ops from-guarded
cell3 = dict(BELL, second_planting=sp)
cops = {o["json_path"].rsplit(".", 1)[-1]: o for o in clean_ops("bell-pepper", "se_gulf", "8", cell3)}
assert cops["plant_out"]["value"] == "Mar 15 - Apr 15" and cops["plant_out"]["from"] == BELL["plant_out"]
assert cops["harvest"]["value"] == "May 15 - Jun 30"
assert cops["last_plant_date"]["value"] == "Apr 15"
assert cops["harvest_end"]["value"] == "Jun 30"
assert "first_plant_date" not in cops and "harvest_start" not in cops  # already primary
# month-granular second harvest: granularity preserved (potato-style)
pot = {"start_indoors": None, "plant_out": "Feb - Mar, Aug", "harvest": "May - Jun, Nov - Dec",
       "harvest_start": "May 1", "harvest_end": "Dec 31",
       "first_plant_date": "Feb 1", "last_plant_date": "Aug 31",
       "sources": ["s"], "anchoring_urls": {}}
psp = second_planting_value(pot)
assert psp["plant_out"] == "Aug" and psp["harvest_start"] == "Nov" and psp["harvest_end"] == "Dec"
pops = {o["json_path"].rsplit(".", 1)[-1]: o for o in clean_ops("potato", "ca_interior", "8", dict(pot, second_planting=psp))}
assert pops["harvest_end"]["value"] == "Jun"     # primary end, authored granularity
assert pops["last_plant_date"]["value"] == "Mar"  # primary plant_out end text

print("build_demux_batches tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_build_demux_batches.py`
Expected: `ModuleNotFoundError: No module named 'build_demux_batches'`

- [ ] **Step 3: Write the implementation**

```python
#!/usr/bin/env python3
"""build_demux_batches.py -- deterministic generator for the de-mux batches
(spec 2026-07-09 §5, §7). READ-ONLY on the canonical: emits
tools/batches/second_planting_<name>.json for apply_patch.py, the only writer.

--stage populate : S1 -- second_planting ADD ops for the 90 TWO_CROP cells in 3
                   archetype batches; the 13 or-norm/continuity REPLACE ops ride
                   s1_b3. ABORTS if the roster's classification drifts from the
                   spec's pinned scope (counts below).
--stage clean    : S3 -- primary-only REPLACE ops for every second_planting cell
                   (pop-1 dedup + pop-2 clean) + envelope narrowing. Run ONLY
                   after Stage 2 (the plant-astro read-flip) is live.
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plant_windows import spans, window_count, single_date, in_span, months_overlap

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")

S1_BATCHES = {
    "s1_b1_solanaceae": ["banana-pepper", "bell-pepper", "cayenne-pepper",
                         "eggplant", "habanero", "jalapeno", "tomatillo"],
    "s1_b2_cucurbits": ["acorn-squash", "butternut-squash", "cantaloupe",
                        "honeydew-melon", "pumpkin", "spaghetti-squash", "watermelon"],
    "s1_b3_rest": ["onion", "pole-beans", "potato", "shallot", "swiss-chard"],
}
# spec §3 pinned scope -- generator ABORTS on drift (re-measure before overriding).
# REFLUSH = 12: the 8 hot-region pepper cells + chives 1 + mint 3 (harvest-only
# doubling is the same structural pattern; all exempt, zero ops either way).
EXPECT = {"TWO_CROP": 90, "ALT_WINDOW": 11, "REFLUSH": 12}
POP1_CELLS, POP2_CELLS = 64, 90
PLANTING = ("start_indoors", "plant_out")
FIELDS = ("start_indoors", "plant_out", "harvest")
# pop-1 legacy crops (dedup lane); everything else with second_planting = pop-2
POP1_SLUGS = {"beefsteak-tomato", "broccoli", "cherry-tomato", "grape-tomato",
              "heirloom-tomato", "kohlrabi", "roma-tomato"}


def _cells(crop):
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if isinstance(cell, dict):
                yield rk, z, cell


def _path(slug, rk, z, key):
    return f"$.crops[?(@.slug=='{slug}')].regions.{rk}.resolved_by_zone.{z}.{key}"


def _start_key(sp):
    return (sp.start_month, sp.start_day or 1)


def classify(cell):
    """Pattern of a NO-second_planting cell (spec §2/§3); None = single-window."""
    n = {f: window_count(cell.get(f)) for f in FIELDS}
    if max(n.values()) < 2:
        return None
    plant_multi = n["plant_out"] >= 2 or n["start_indoors"] >= 2
    if plant_multi and n["harvest"] >= 2:
        return "TWO_CROP"
    if n["harvest"] >= 2:
        return "REFLUSH"
    return "ALT_WINDOW"


def second_planting_value(cell):
    """Spec §5: the second spans, provenance inherited, granularity preserved."""
    po, hv = spans(cell.get("plant_out")), spans(cell.get("harvest"))
    si = spans(cell.get("start_indoors"))
    assert len(po) == 2, f"TWO_CROP cell needs exactly 2 plant_out spans: {po}"
    assert len(hv) == 2, f"TWO_CROP cell needs exactly 2 harvest spans: {hv}"
    assert len(si) in (0, 1, 2), f"unexpected start_indoors span count: {si}"
    assert _start_key(po[0]) < _start_key(po[1]), f"plant_out not spring-first: {po}"
    assert _start_key(hv[0]) < _start_key(hv[1]), f"harvest not spring-first: {hv}"
    # the fall planting must precede its harvest (harvest may wrap into Jan)
    assert po[1].start_month <= hv[1].start_month or hv[1].start_month <= 2, \
        f"fall plant does not precede fall harvest: {po[1]} vs {hv[1]}"
    return {
        "start_indoors": si[1].raw if len(si) == 2 else None,
        "plant_out": po[1].raw,
        "harvest_start": hv[1].start_text,
        "harvest_end": hv[1].end_text,
        "sources": cell.get("sources"),
        "anchoring_urls": cell.get("anchoring_urls"),
    }


def or_norm_ops(slug, rk, z, cell):
    """ALT_WINDOW cells: comma -> ' or ' (spec §2 B-alt); onion ca_north_coast
    plant_out gets the zone_notes-backed continuity merge (§2 B-fix)."""
    ops = []
    for f in PLANTING:
        val = cell.get(f)
        if window_count(val) < 2:
            continue
        if slug == "onion" and rk == "ca_north_coast" and f == "plant_out":
            new = "Nov - March"
        else:
            new = " or ".join(p.strip() for p in val.split(","))
        ops.append({"op": "replace", "json_path": _path(slug, rk, z, f),
                    "from": val, "value": new})
    return ops


def clean_ops(slug, rk, z, cell):
    """Stage-3 ops for ONE second_planting cell: window strings -> primary span;
    envelope narrowed to primary (spec §2 Decision C). Asserts the dropped span
    overlaps the second_planting counterpart (never byte-equality: pop-1 harvest
    strings are month-granular vs day-granular sp values)."""
    sp = cell["second_planting"]
    ops = []

    def rep(key, frm, val):
        ops.append({"op": "replace", "json_path": _path(slug, rk, z, key),
                    "from": frm, "value": val})

    po, hv = spans(cell.get("plant_out")), spans(cell.get("harvest"))
    for f in FIELDS:
        s = spans(cell.get(f))
        if len(s) < 2:
            continue
        assert len(s) == 2, f"3+ spans unexpected: {slug} {rk}.{z} {f}"
        if f == "harvest":
            ref = (f"{sp['harvest_start']} - {sp['harvest_end']}"
                   if sp.get("harvest_start") else None)
        else:
            ref = sp.get(f)
        if ref:
            refspan = spans(ref)
            assert refspan and months_overlap(s[1], refspan[0]), \
                f"dropped span does not overlap second_planting: {slug} {rk}.{z} {f}"
        rep(f, cell[f], s[0].raw)

    # envelope: only touched when it currently reflects the fall cycle
    sp_po = spans(sp.get("plant_out") or "")
    lpd = single_date(cell.get("last_plant_date"))
    if lpd and sp_po and in_span(lpd, sp_po[0]) and po:
        rep("last_plant_date", cell["last_plant_date"], po[0].end_text)
    he = single_date(cell.get("harvest_end"))
    sp_he = single_date(sp.get("harvest_end") or "")
    if he and hv and ((sp_he and he == sp_he) or (len(hv) == 2 and in_span(he, hv[1]))):
        rep("harvest_end", cell["harvest_end"], hv[0].end_text)
    # first_plant_date / harvest_start must already be primary -- assert, never edit
    fpd = single_date(cell.get("first_plant_date"))
    assert not (fpd and sp_po and in_span(fpd, sp_po[0])), \
        f"first_plant_date sits in the fall window: {slug} {rk}.{z}"
    return ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["populate", "clean"])
    ap.add_argument("--only", help="emit just one batch name")
    ap.add_argument("--base", default=CANON)
    a = ap.parse_args()
    raw = open(a.base, "rb").read()
    base_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    batches = {}
    if a.stage == "populate":
        counts = {"TWO_CROP": 0, "ALT_WINDOW": 0, "REFLUSH": 0}
        slug_batch = {s: b for b, ss in S1_BATCHES.items() for s in ss}
        for crop in crops:
            slug = crop.get("slug")
            if (crop.get("succession_policy") or {}).get("suitable") is not False:
                continue
            for rk, z, cell in _cells(crop):
                if isinstance(cell.get("second_planting"), dict):
                    continue
                pat = classify(cell)
                if pat is None:
                    continue
                counts[pat] += 1
                if pat == "TWO_CROP":
                    b = slug_batch[slug]  # KeyError = unexpected crop -> abort
                    batches.setdefault(b, []).append(
                        {"op": "add", "json_path": _path(slug, rk, z, "second_planting"),
                         "value": second_planting_value(cell)})
                elif pat == "ALT_WINDOW":
                    batches.setdefault("s1_b3_rest", []).extend(
                        or_norm_ops(slug, rk, z, cell))
        assert counts == EXPECT, f"scope drift vs spec: {counts} != {EXPECT}"
    else:  # clean
        n1 = n2 = 0
        for crop in crops:
            slug = crop.get("slug")
            for rk, z, cell in _cells(crop):
                if not isinstance(cell.get("second_planting"), dict):
                    continue
                name = "s3_b1_pop1_dedup" if slug in POP1_SLUGS else "s3_b2_pop2_clean"
                if slug in POP1_SLUGS:
                    n1 += 1
                else:
                    n2 += 1
                ops = clean_ops(slug, rk, z, cell)
                if ops:
                    batches.setdefault(name, []).extend(ops)
        assert n1 == POP1_CELLS and n2 == POP2_CELLS, \
            f"cell-count drift: pop1={n1} pop2={n2}"

    for name, ops in sorted(batches.items()):
        if a.only and name != a.only:
            continue
        out = os.path.join(HERE, "batches", f"second_planting_{name}.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"base_sha": base_sha, "patches": ops}, fh, indent=1,
                      ensure_ascii=False)
        print(f"wrote {out}: {len(ops)} ops")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_build_demux_batches.py`
Expected: `build_demux_batches tests: OK`

- [ ] **Step 5: Dry-run the populate stage against the real canonical (no apply)**

Run: `python3 tools/build_demux_batches.py --stage populate`
Expected output (op counts are the acceptance check):
```
wrote .../second_planting_s1_b1_solanaceae.json: 40 ops
wrote .../second_planting_s1_b2_cucurbits.json: 29 ops
wrote .../second_planting_s1_b3_rest.json: 34 ops
```
(34 = 21 TWO_CROP adds + 13 or-norm/fix replaces.) If the EXPECT assert trips instead, the canonical moved since the spec was measured -- STOP and re-scope with Trevor. Spot-read `second_planting_s1_b1_solanaceae.json`: bell-pepper se_gulf z8 op must equal the spec §6 worked example. Do NOT run `--stage clean` yet (its cells don't have second_planting until S1 lands; the assert will rightly abort).

- [ ] **Step 6: Commit (ASK TREVOR FIRST -- batch JSONs are generated artifacts; commit the tool + tests now, batches land with their applies)**

```bash
git checkout -- tools/batches/ 2>/dev/null || true   # don't commit dry-run artifacts yet
git add tools/build_demux_batches.py tools/test_build_demux_batches.py
git commit -m "feat(demux): deterministic batch generator (populate+clean, scope-pinned, abort-on-drift)"
```

---

### Task 4: Footprint auditor (shared verify step for every apply)

**Files:**
- Create: `tools/verify_demux_footprint.py`

**Interfaces:**
- Consumes: nothing repo-specific (stdlib json).
- Produces: CLI `python3 tools/verify_demux_footprint.py <scratch.json> --base crops_data_final.json --slugs bell-pepper,eggplant,... [--stage populate|clean]`; exit 1 unless: crop count 124 both sides, every crop OUTSIDE --slugs byte-identical (compact re-serialization compare), inside crops changed ONLY in `regions.*.resolved_by_zone.*` at the allowed keys (populate: `second_planting` added + `start_indoors`/`plant_out` or-norm replaces; clean: the six window/envelope string keys), output file COMPACT with no trailing newline.

- [ ] **Step 1: Write the implementation** (verification tooling; its test is the adversarial run in Step 2)

```python
#!/usr/bin/env python3
"""verify_demux_footprint.py -- the byte-diff footprint audit for de-mux applies
(spec §9). Independent of apply_patch's own report: reads ONLY the two files.
Exit 1 on any out-of-footprint drift."""
import argparse
import json
import sys

POPULATE_KEYS = {"second_planting", "start_indoors", "plant_out"}
CLEAN_KEYS = {"start_indoors", "plant_out", "harvest",
              "harvest_start", "harvest_end", "first_plant_date", "last_plant_date"}


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--base", required=True)
    ap.add_argument("--slugs", required=True)
    ap.add_argument("--stage", required=True, choices=["populate", "clean"])
    a = ap.parse_args()
    allowed_slugs = set(a.slugs.split(","))
    allowed_keys = POPULATE_KEYS if a.stage == "populate" else CLEAN_KEYS
    raw = open(a.candidate, "rb").read()
    problems = []
    if raw.endswith(b"\n"):
        problems.append("candidate has a trailing newline (must be COMPACT)")
    cand = json.loads(raw.decode("utf-8"))
    base = json.load(open(a.base, encoding="utf-8"))
    cc = cand["crops"] if isinstance(cand, dict) and "crops" in cand else cand
    bc = base["crops"] if isinstance(base, dict) and "crops" in base else base
    if len(cc) != 124 or len(bc) != 124:
        problems.append(f"crop count: base={len(bc)} candidate={len(cc)} (want 124)")
    by_slug_c = {c.get("slug"): c for c in cc}
    for b in bc:
        slug = b.get("slug")
        c = by_slug_c.get(slug)
        if c is None:
            problems.append(f"crop missing from candidate: {slug}")
            continue
        if compact(b) == compact(c):
            if slug in allowed_slugs:
                problems.append(f"batch crop unchanged (op missed?): {slug}")
            continue
        if slug not in allowed_slugs:
            problems.append(f"OUT-OF-FOOTPRINT crop changed: {slug}")
            continue
        # inside a batch crop: only resolved cells, only allowed keys
        for key in set(b) | set(c):
            if key == "regions":
                continue
            if compact(b.get(key)) != compact(c.get(key)):
                problems.append(f"{slug}: top-level key changed: {key}")
        for rk in set(b.get("regions", {})) | set(c.get("regions", {})):
            br, cr = b["regions"].get(rk, {}), c["regions"].get(rk, {})
            for key in set(br) | set(cr):
                if key == "resolved_by_zone":
                    continue
                if compact(br.get(key)) != compact(cr.get(key)):
                    problems.append(f"{slug}.{rk}: region key changed: {key}")
            for z in set(br.get("resolved_by_zone", {}) or {}) | set(cr.get("resolved_by_zone", {}) or {}):
                bz = (br.get("resolved_by_zone") or {}).get(z, {})
                cz = (cr.get("resolved_by_zone") or {}).get(z, {})
                for key in set(bz) | set(cz):
                    if compact(bz.get(key)) != compact(cz.get(key)) and key not in allowed_keys:
                        problems.append(f"{slug}.{rk}.{z}: cell key changed: {key}")
    for p in problems:
        print("FOOTPRINT:", p)
    print(f"verify_demux_footprint: {len(problems)} problems "
          f"({a.stage}, {len(allowed_slugs)} slugs)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Adversarial proof (RED): it must catch an out-of-footprint edit**

```bash
python3 - <<'EOF'
import json
d = json.load(open('crops_data_final.json'))
d['crops'][0]['sunlight'] = 'CORRUPTED'
import os; os.makedirs(os.environ.get('SCRATCH','.'), exist_ok=True)
open(f"{os.environ['SCRATCH']}/corrupt.json",'w').write(json.dumps(d,separators=(',',':'),ensure_ascii=False))
EOF
python3 tools/verify_demux_footprint.py "$SCRATCH/corrupt.json" --base crops_data_final.json --slugs bell-pepper --stage populate
```
Expected: exit 1, two problems (`OUT-OF-FOOTPRINT crop changed` for crop 0's slug, `batch crop unchanged` for bell-pepper). Then `rm "$SCRATCH/corrupt.json"`.

- [ ] **Step 3: Commit (ASK TREVOR FIRST)**

```bash
git add tools/verify_demux_footprint.py
git commit -m "feat(demux): independent footprint auditor for the de-mux applies"
```

---

### Task 5: Apply S1-B1 solanaceae (40 cells)

**Files:**
- Create: `tools/batches/second_planting_s1_b1_solanaceae.json` (generated)
- Modify: `crops_data_final.json`, `LATEST.txt`

**Interfaces:**
- Consumes: Task 3 generator, Task 4 auditor.
- Produces: canonical with second_planting on the 7 solanaceae crops' TWO_CROP cells.

- [ ] **Step 1: Generate against the CURRENT canonical**

```bash
python3 tools/build_demux_batches.py --stage populate --only s1_b1_solanaceae
```
Expected: `wrote .../second_planting_s1_b1_solanaceae.json: 40 ops`

- [ ] **Step 2: Apply to scratch**

```bash
python3 tools/apply_patch.py tools/batches/second_planting_s1_b1_solanaceae.json --out "$SCRATCH/s1_b1.json"
```
Expected: SHA gate passes; footprint report lists ONLY banana-pepper, bell-pepper, cayenne-pepper, eggplant, habanero, jalapeno, tomatillo.

- [ ] **Step 3: Verify (footprint + gates + release_verify)**

```bash
python3 tools/verify_demux_footprint.py "$SCRATCH/s1_b1.json" --base crops_data_final.json \
  --slugs banana-pepper,bell-pepper,cayenne-pepper,eggplant,habanero,jalapeno,tomatillo --stage populate
for s in banana-pepper bell-pepper cayenne-pepper eggplant habanero jalapeno tomatillo; do
  python3 tools/whole_crop_gate.py "$s" "$SCRATCH/s1_b1.json" || echo "GATE FAIL: $s"
done
python3 tools/release_verify.py "$SCRATCH/s1_b1.json" --base crops_data_final.json --slug bell-pepper
python3 tools/second_planting_gate.py "$SCRATCH/s1_b1.json" --rules B
```
Expected: footprint 0 problems; 7x gate PASS (the existing SECOND_PLANTING_KEYS check must accept the new objects); release_verify's only concerns are the documented multi-crop-batch collateral notes (every "changed" crop is in the batch list); Rule B violations DROP by the 7 crops' TWO_CROP share (bell/banana 8 each, jalapeno 6, eggplant 6, tomatillo 6, cayenne 3, habanero 3 = 40 fewer B-violating cells than the Task 2 Step 5 baseline).

- [ ] **Step 4: Source-truth sample (protocol #6)**

Read one migrated cell against its cited page: bell-pepper `se_gulf` z8's `second_planting` (`Sep 1 - Sep 20` / harvest `Nov 1 - Nov 30`) vs the cell's `anchoring_urls` source. The second window must be plausible for a Gulf fall pepper planting per that source. Record the check in the commit message body.

- [ ] **Step 5: Promote + commit (ASK TREVOR FIRST)**

```bash
cp "$SCRATCH/s1_b1.json" crops_data_final.json
shasum -a 256 crops_data_final.json   # paste into LATEST.txt (SHA + date + session line)
git add crops_data_final.json LATEST.txt tools/batches/second_planting_s1_b1_solanaceae.json
git commit -m "feat(demux): S1-B1 populate second_planting on 40 solanaceae cells (additive)"
```
(The pre-commit release-verify hook runs on the staged canonical; it must pass.)

---

### Task 6: Apply S1-B2 cucurbits (29 cells)

Same 5 steps as Task 5 with:
- Generate: `python3 tools/build_demux_batches.py --stage populate --only s1_b2_cucurbits` -> `29 ops` (regenerated against the post-B1 canonical; base_sha updates automatically).
- Slugs: `acorn-squash,butternut-squash,cantaloupe,honeydew-melon,pumpkin,spaghetti-squash,watermelon`
- Rule B drop: 29 cells (acorn 5, butternut 5, spaghetti 5, pumpkin 5, cantaloupe 3, honeydew 3, watermelon 3).
- Source-truth sample: pumpkin or watermelon fall window vs its cited page.
- Commit: `feat(demux): S1-B2 populate second_planting on 29 cucurbit cells (additive)`

- [ ] Generate, apply, verify (footprint + 7x whole_crop_gate + release_verify + Rule B count), source-truth sample, promote + commit (ASK TREVOR FIRST)

---

### Task 7: Apply S1-B3 rest (21 cells + 13 or-norm/fix ops)

Same 5 steps as Task 5 with:
- Generate: `python3 tools/build_demux_batches.py --stage populate --only s1_b3_rest` -> `34 ops`.
- Slugs: `onion,pole-beans,potato,shallot,swiss-chard`
- After apply, Rule B on the scratch must report **0 violations, exit 0** (all TWO_CROP populated, all ALT_WINDOW or-normalized): `python3 tools/second_planting_gate.py "$SCRATCH/s1_b3.json" --rules B`
- Extra check: onion `ca_north_coast` z9/z10 `plant_out` == `"Nov - March"`; shallot `ca_interior` z8 `plant_out` == `"Oct - Nov or Jan - March"`; onion `ca_interior` `start_indoors` == `"Sep or Dec"`.
- Source-truth sample: pole-beans se_gulf fall window vs its cited page.
- Commit: `feat(demux): S1-B3 populate 21 cells + or-normalize 11 alt-window cells (onion continuity fix)`

- [ ] Generate, apply, verify, confirm Rule B == 0 roster-wide, source-truth sample, promote + commit (ASK TREVOR FIRST)

---

### Task 8: Wire Rule B as A43 + Stage-1 close (state trio, push)

**Files:**
- Modify: `tools/whole_crop_gate.py` (after the A42 block, before A24)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md` (hand-edited), `LATEST.txt` (already bumped in Task 7)

**Interfaces:**
- Consumes: `second_planting_gate.check_crop`.
- Produces: A43 live at `rules=frozenset("B")`; the constant `_DEMUX_RULES` is what Task 12 flips.

- [ ] **Step 1: Wire A43 (Rule B only)**

Insert into `tools/whole_crop_gate.py` directly after the A42 block:

```python
# ---------------- A43. second_planting de-mux invariant (spec 2026-07-09) ----------------
# Rule B (LIVE, Stage-1 close): a suitable!=true cell with >=2 comma-joined windows in a
# PLANTING field (start_indoors/plant_out) and NO second_planting cannot certify -- blocks
# the old multiplexed shape and any new crop re-introducing it. " or "-joined alternatives
# and harvest-only doubling (reflush/bimodal) are legitimate and exempt. Rule A (dedup:
# a cell WITH second_planting is single-window at top level, envelope primary-only) is
# wired at the Stage-3 clean close by flipping _DEMUX_RULES to frozenset("AB").
from second_planting_gate import check_crop as _demux_violations
_DEMUX_RULES = frozenset("B")
print(f"A43. second_planting de-mux invariant (rules={''.join(sorted(_DEMUX_RULES))})")
_dmx = _demux_violations(crop, _DEMUX_RULES)
print(f"  de-mux violations: {len(_dmx)}")
for m in _dmx:
    fail(f"demux: {m}")
```

- [ ] **Step 2: Adversarial proof on a scratch copy of the REAL canonical (RED)**

```bash
python3 - <<'EOF'
import json, os
d = json.load(open('crops_data_final.json'))
bp = [c for c in d['crops'] if c['slug']=='bell-pepper'][0]
cell = bp['regions']['se_gulf']['resolved_by_zone']['8']
del cell['second_planting']                       # simulate a new crop authored old-style
assert ',' in cell['plant_out']                   # still doubled pre-clean -- defect live
open(f"{os.environ['SCRATCH']}/defect_b.json",'w').write(json.dumps(d,separators=(',',':'),ensure_ascii=False))
EOF
python3 tools/whole_crop_gate.py bell-pepper "$SCRATCH/defect_b.json"
```
Expected: **exit 1** with a `demux: B unstructured comma shape: se_gulf.8 plant_out ...` line. (If Stage 3 has NOT run yet the cell's plant_out is still comma-doubled, which is exactly the injected-defect shape.) Then `rm "$SCRATCH/defect_b.json"`.

- [ ] **Step 3: GREEN roster-wide**

```bash
python3 tools/whole_crop_gate.py bell-pepper && python3 tools/whole_crop_gate.py lavender \
  && python3 tools/whole_crop_gate.py mint && python3 tools/whole_crop_gate.py carrot \
  && python3 tools/whole_crop_gate.py lettuce-leaf
python3 tools/gate_all.py
```
Expected: all PASS; gate_all 114/114 (lettuce-leaf = the standing reference-crop regression guard).

- [ ] **Step 4: State trio (hand-edited) + commit + push (ASK TREVOR; HE CONFIRMS THE PUSH)**

Prepend the Stage-1 entry to `CURRENT_STATE.md` (surgical hand edit, NO gen_current_state), append `STATE_HISTORY.md` most-recent-first, confirm `LATEST.txt` carries the post-Task-7 SHA + session line. Entry must record: 90 cells populated + 11 or-normalized + onion fix, celery-roster correction, A43 Rule B live, Rule A deferred to Stage 3, plant-astro flip = next.

```bash
git add tools/whole_crop_gate.py CURRENT_STATE.md STATE_HISTORY.md
git commit -m "feat(gate): A43 second_planting de-mux Rule B live (new crops blocked from comma shape)"
# push only after Trevor confirms:
git push
```

---

### Task 9: Stage 2 -- plant-astro read-layer flip (cross-repo, Trevor-gated)

**Files (in `~/plant-astro`, NEVER the embedded submodule copy):**
- Modify: `src/components/guides/SuccessionCard.astro`, `src/components/guides/PlantingCalendarCard.astro`, `src/lib/today.ts`, `src/lib/plant-window.ts` (+ its `plant-window.test.ts`)

**Behavioral contract (the astro session reads the files first and implements to THIS):**
1. The fall/second track renders from `zoneData.second_planting{start_indoors, plant_out, harvest_start, harvest_end}` when present; when absent there is NO second track. All comma-count synthesis (`hasSecondPlanting = plantChunks.length > 1`, `synthesizedSecondTrack`, DTM-midpoint harvest guessing) is deleted.
2. INTERIM RULE (top-level strings are still doubled until Stage 3): every main-cycle read takes the FIRST comma chunk (the existing `split(',')[0]` idiom), and `second_planting` is the ONLY second-track source -- a cell with both a structured object and a comma tail must not double-render.
3. `" or "` planting strings render as a single window choice (existing woody-herb behavior, now also onion/shallot/chard).
4. suitable=true rhythm mode unchanged (lettuce regression check).

- [ ] **Step 1:** Read the four files + `git log --oneline -5` in `~/plant-astro`; implement to the contract.
- [ ] **Step 2:** `cd ~/plant-astro && npx vitest run && npx astro check` -- green.
- [ ] **Step 3:** Bump the plant-dataset submodule to the Stage-1 commit; `npm run build` -- green (the real end-to-end check; vitest+check alone missed the last break).
- [ ] **Step 4:** `grep -rn "split(',')" src/ | grep -v "\[0\]"` -- every remaining comma-split is a first-chunk main-cycle read or unrelated; no second-track synthesis survives.
- [ ] **Step 5:** Visual spot-check in the built site: broccoli `ca_interior` z9 (pop-1: July fall indoor start on the SuccessionCard), bell-pepper `se_gulf` z8 (pop-2: Sep fall track now visible), onion `ca_interior` z8 (NO second track), lettuce (rhythm unchanged).
- [ ] **Step 6:** Commit + deploy per plant-astro's own ceremony -- **Trevor gates the bump and the deploy**.

---

### Task 10: Generate + apply Stage-3 clean batches

**Files:**
- Create: `tools/batches/second_planting_s3_b1_pop1_dedup.json`, `tools/batches/second_planting_s3_b2_pop2_clean.json` (generated)
- Modify: `crops_data_final.json`, `LATEST.txt`

**PRECONDITION (hard):** Task 9 deployed and confirmed by Trevor. Cleaning before the read-flip erases the fall crop from the UI.

- [ ] **Step 1: Generate**

```bash
python3 tools/build_demux_batches.py --stage clean
```
Expected: two batch files; s3_b1 covers the 7 pop-1 crops (64 cells; 116 window-string replaces + envelope ops), s3_b2 the 17 pop-2 crops (90 cells). The generator's cell-count assert (64/90) and per-field overlap asserts are the drift guard. Record both op counts.

- [ ] **Step 2: Apply s3_b1 to scratch, verify, promote, commit (ASK TREVOR FIRST)**

Same shape as Task 5 steps 2-5 with `--stage clean`, slugs `beefsteak-tomato,broccoli,cherry-tomato,grape-tomato,heirloom-tomato,kohlrabi,roma-tomato`. Extra acceptance: broccoli `ca_interior` z9 ends `plant_out "Dec 1 - Feb 28"`, `harvest "Mar 1 - May 1"`, `harvest_end "May 1"` (the findings-doc worked example); `python3 tools/second_planting_gate.py "$SCRATCH/s3_b1.json" --rules A` violations drop to pop-2's share only. `calendar[]` byte-identical is implied by the footprint auditor (calendar is not an allowed key). Commit: `feat(demux): S3-B1 pop-1 dedup -- 64 cells primary-only (extract precedent, zero loss)`.

- [ ] **Step 3: Apply s3_b2 to scratch, verify, promote, commit (ASK TREVOR FIRST)**

Slugs = the 17 pop-2 crops. Acceptance: bell-pepper `se_gulf` z8 equals the spec §6 AFTER column byte-for-byte (including `last_plant_date "Apr 15"`, `harvest_end "Jun 30"`); `--rules A` AND `--rules B` both report **0 violations roster-wide** on the scratch. Commit: `feat(demux): S3-B2 pop-2 clean -- 90 cells primary-only, envelopes narrowed`.

---

### Task 11: Flip A43 to rules AB (Rule A live)

**Files:**
- Modify: `tools/whole_crop_gate.py` (one line)

- [ ] **Step 1:** Change `_DEMUX_RULES = frozenset("B")` -> `_DEMUX_RULES = frozenset("AB")` (update the comment's "wired at Stage-3" phrasing to "LIVE").
- [ ] **Step 2: Adversarial proof (RED):** re-double a cleaned cell on a scratch copy and confirm the gate bounces it:

```bash
python3 - <<'EOF'
import json, os
d = json.load(open('crops_data_final.json'))
bp = [c for c in d['crops'] if c['slug']=='bell-pepper'][0]
cell = bp['regions']['se_gulf']['resolved_by_zone']['8']
cell['plant_out'] = cell['plant_out'] + ", " + cell['second_planting']['plant_out']  # re-inject the dedup defect
open(f"{os.environ['SCRATCH']}/defect_a.json",'w').write(json.dumps(d,separators=(',',':'),ensure_ascii=False))
EOF
python3 tools/whole_crop_gate.py bell-pepper "$SCRATCH/defect_a.json"
```
Expected: **exit 1** with `demux: A dedup: se_gulf.8 plant_out ...`. Then `rm "$SCRATCH/defect_a.json"`.
- [ ] **Step 3: GREEN:** `python3 tools/whole_crop_gate.py bell-pepper && python3 tools/whole_crop_gate.py broccoli && python3 tools/whole_crop_gate.py lettuce-leaf && python3 tools/gate_all.py` -- all PASS, 114/114.
- [ ] **Step 4: Commit (ASK TREVOR FIRST):** `git add tools/whole_crop_gate.py && git commit -m "feat(gate): A43 Rule A (dedup invariant) live -- de-mux fully enforced"`

---

### Task 12: Stage-3 close -- state trio, convention doc, memory, kickoff

**Files:**
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (post-Task-10 SHA)
- Modify: the crop-authoring checklist doc (locate via `grep -rl "authoring checklist\|crop-authoring" docs/`; if none exists, add the convention to `docs/kickoffs/18-second-planting-demux-migration.md` as a closing section)
- Modify: memory `second-planting-demux-followup.md` (mark COMPLETE, final numbers, celery correction)

- [ ] **Step 1:** Authoring convention text (verbatim): "A suitable=false two-season crop is authored with primary-only top-level windows + a populated `second_planting{}` (four keys + inherited provenance). Alternative establishment windows are `\" or \"`-joined, never comma-joined. A same-plant split harvest is comma-joined in `harvest` only. whole_crop_gate A43 enforces all three."
- [ ] **Step 2:** Full release verification: `python3 tools/gate_all.py` (114/114) + `python3 tools/release_verify.py crops_data_final.json` (standalone audit) + `python3 tools/second_planting_gate.py --rules AB` (0) + the three module tests still green.
- [ ] **Step 3:** State trio hand-edits (Stage-3 entry: 154 cells primary-only, envelopes narrowed, A43 AB live, old shape extinct; flag the shape change for the plant-app lane per `dataset-shape-change-breaks-frontends`).
- [ ] **Step 4:** plant-astro submodule bump #2 + `cd ~/plant-astro && npm run build` -- green; visual re-check bell-pepper se_gulf z8 (fall track intact from second_planting, main card primary-only).
- [ ] **Step 5:** Update memory file + MEMORY.md hook line (COMPLETE, 2026-07 dates absolute).
- [ ] **Step 6:** Commit docs/memory + push (ASK TREVOR; HE CONFIRMS THE PUSH).

---

## Self-Review Notes

- Spec coverage: §2 rulings -> Tasks 3 (classify/or-norm/fix/precision/provenance), §4 parser -> Task 1, §5 extraction -> Task 3, §6 gate + TDD classes -> Tasks 2/8/11, §7 stages -> Tasks 5-10, §8 convention -> Task 12, §9 discipline -> Global Constraints + per-task verify steps, §10 DoD -> Tasks 7 (B==0), 10 (AB==0), 12 (close).
- Rule A envelope check is deliberately the two-defect floor (spec §6 refinement noted in the module docstring).
- Counts cross-checked: 40+29+21=90 adds; 13 or-norm ops (onion ci 2x2, onion cnc 2, shallot 2, chard 5); pop-1 116 doubled fields.
