# Region Coverage Roadmap Item 5 -- Tier-2 Judged-Belt Ruling Pass -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a cited GENERIC-OK / CONDITIONAL-GO / NEW-REGION ruling for each of the 5 Tier-2
belts (mid-Atlantic, mid-South, Nevada, Utah, Alaska), replacing the roadmap's unsourced "first
reads" -- pure research and documentation, zero canonical or code changes.

**Architecture:** Five fully independent, sequential belt tasks (Task 1-5, in ZIP-count order).
Each task: pick the belt's marquee anchor and real frost dates, build a naive region-blind
calendar for a representative crop basket (`tools/annual_calendar.py`, read-only against the
canonical, run from a scratch helper script that is never committed), find the belt's real T1
extension guidance for the same crops, compare directionally, and write a research note + a
roadmap-doc update. Every task ends with an explicit Trevor checkpoint before the next begins.

**Tech Stack:** Python 3 (`tools/annual_calendar.py`, read-only canonical queries), WebSearch /
WebFetch for real frost-date and T1-source research, Markdown for artifacts.

## Global Constraints

- Canonical `crops_data_final.json` is **READ-ONLY** for this entire plan -- every task only reads
  crop fields (`weeks_indoors`, `days_to_maturity_mid`, `dtm_anchor`, `chill_hours_required` on
  varieties) via `python3 -c "import json; ..."` one-liners. No `apply_patch.py`, no splice, no
  promote, anywhere in this plan.
- **No code changes.** The naive-calendar helper script lives in the scratchpad directory only
  (never `tools/`, never committed) -- it is throwaway research tooling, not a shipped gate.
- **`source_catalog` is NOT written.** It lives inside `crops_data_final.json`; new T1 sources
  found for mid-South/Alaska are cited by institution + URL directly in the research note.
- **T1-sourced-or-it-doesn't-ship.** Every frost date, extension calendar, and chill-hour figure
  in a research note must trace to a real `.edu`/`.gov` extension or government source (or the
  canonical itself for crop biology fields). Where no T1 source is yet catalogued in this dataset
  (mid-South, Alaska), actively search for the real land-grant extension source -- a missing
  catalog entry is a research task, not license to cite a weaker source.
- American English, no fabricated figures -- every date/number in a research note is either read
  from the canonical or cited to a real source found during the task.
- **Sequencing:** Task 1 (mid-Atlantic) -> Task 2 (mid-South) -> Task 3 (Nevada) -> Task 4 (Utah)
  -> Task 5 (Alaska). Each task ends with **STOP -- get Trevor's review of the ruling** before the
  next task starts. This is 5 independent passes, not one combined batch.
- Base canonical `8dd4ac4c` (informational only; never re-stamped, never written).

---

### Task 1: Mid-Atlantic belt ruling (NC/VA/MD/DC/DE-NJ-PA z8)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`
- Modify: `docs/region_coverage_roadmap.md` (the item-5 Tier-2 table row for mid-Atlantic)
- Scratch (not committed): a naive-calendar helper script in the session scratchpad directory

**Interfaces:**
- Consumes: `crops_data_final.json` crop fields (read-only) for `cherry-tomato` (annual),
  `apple` (tree fruit), `blueberry` (belt-relevant third crop); `tools/annual_calendar.py`'s
  `derive_annual_calendar(cell, calendar_basis="frost_anchored")`.
- Produces: the research note + roadmap-doc row; no data consumed by later belt tasks (each is
  independent), but Task 2 reads the roadmap doc's CURRENT state before editing its own row, so
  this task's edit must land (committed) before Task 2 starts.

- [ ] **Step 1: Pick the marquee anchor and find its real frost dates**

NC carries the most ZIPs (793 z8 + 20 z9) of the belt, so NC is the marquee state. Use
WebSearch/WebFetch (fetch via ToolSearch `select:WebSearch,WebFetch` if not already loaded) to
find real last/first frost date normals for a representative NC z8 city (e.g. Raleigh or
Wilmington -- pick whichever has a clean NOAA or NC State Extension frost-date citation). Record
the exact dates, the city, and the source URL.

Expected: two dates (e.g. "last frost ~Apr 5, first frost ~Nov 10") with a citable NOAA or NC
State Extension source.

- [ ] **Step 2: Pull the basket crops' generic biology fields from the canonical (read-only)**

```bash
python3 -c "
import json
d = json.load(open('crops_data_final.json'))
by = {c['slug']: c for c in d['crops']}
for slug in ['cherry-tomato', 'apple', 'blueberry']:
    c = by[slug]
    print(slug, {k: c.get(k) for k in ['weeks_indoors','days_to_maturity_mid','dtm_anchor','frost_tolerance_f']})
"
```

Expected: `cherry-tomato` shows `weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor:
'from_transplant', frost_tolerance_f: 32`; `apple` shows `weeks_indoors: None,
days_to_maturity_mid: None` (season-only -- confirms apple is NOT run through the annual
deriver, it's the chill-hour comparison in Step 4); `blueberry`'s fields print for reference.

- [ ] **Step 3: Build the naive calendar for `cherry-tomato` and derive it**

Write this to a scratch file in the session scratchpad (NOT `tools/`, NOT committed):

```python
import sys, json
sys.path.insert(0, "/Users/trevorrawson/plant-dataset/tools")
import annual_calendar as ac
from datetime import date, timedelta

MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def fmt(d):
    return f"{MON[d.month-1]} {d.day}"

def span(a, b):
    return f"{fmt(a)} - {fmt(b)}"

def naive_cell(last_frost, weeks_indoors, dtm_mid, plant_offset=7, plant_window=14, indoors_window=7):
    plant_start = last_frost + timedelta(days=plant_offset)
    plant_end = plant_start + timedelta(days=plant_window)
    indoors_start = plant_start - timedelta(weeks=weeks_indoors)
    indoors_end = indoors_start + timedelta(days=indoors_window)
    harvest_start = plant_start + timedelta(days=dtm_mid)
    harvest_end = plant_end + timedelta(days=dtm_mid) + timedelta(days=14)
    return {
        "plant_out": span(plant_start, plant_end),
        "start_indoors": span(indoors_start, indoors_end),
        "first_plant_date": fmt(plant_start), "last_plant_date": fmt(plant_end),
        "harvest": span(harvest_start, harvest_end),
        "harvest_start": fmt(harvest_start), "harvest_end": fmt(harvest_end),
    }

# last_frost from Step 1's real citation, year is a placeholder (only month/day render)
last_frost = date(2026, 4, 5)   # REPLACE with Step 1's real NC date
cell = naive_cell(last_frost, weeks_indoors=6, dtm_mid=62)
print(json.dumps(cell, indent=1))
print(ac.derive_annual_calendar(cell, calendar_basis="frost_anchored"))
```

Run it. Expected (with the placeholder Apr 5 date): `plant_out "Apr 12 - Apr 26"`,
`start_indoors "Mar 1 - Mar 8"`, `harvest "Jun 13 - Jul 11"`, and the derived calendar
`['cold_pause','cold_pause','indoors','plant','growing','harvest','harvest','cold_pause', ...]`
(a single spring-to-summer cycle, no fall reflush -- this validated shape; re-run with Step 1's
real frost date before citing it in the note).

- [ ] **Step 4: Research the belt's real T1 guidance for all 3 basket crops**

Using WebSearch/WebFetch: (a) find NC State Extension's (`ncsu_ext`, already catalogued) or
Virginia Cooperative Extension's (`vce_426_331`, already catalogued) real tomato planting-date
guidance for the marquee city/zone -- specifically whether it recommends a single spring cycle or
a second (fall) planting, which the naive Step 3 calendar does not model. (b) find a real
chill-hour estimate for the marquee city (a university extension chill map or a published chill
accumulation figure) and compare it against apple's per-variety `chill_hours_required` range
(query the canonical: `python3 -c "import json; d=json.load(open('crops_data_final.json')); c=[x for x in d['crops'] if x['slug']=='apple'][0]; print([(v['name'], v.get('chill_hours_required')) for v in c['varieties']['recommended']])"`)
to classify apple as effectively `fruits_reliably`/`marginal`/`survives_no_fruit` for this belt.
(c) find real T1 guidance (NC State or a relevant state extension) for `blueberry` in the belt --
the mid-Atlantic is genuine native highbush blueberry range, so this should be well documented.

Expected: 2-3 real citations recorded (institution, URL, the specific date/figure claim).

- [ ] **Step 5: Compare directionally and determine the ruling**

Using the GO / CONDITIONAL-GO / NEW-REGION framework (spec section 5): does the naive single-cycle
tomato calendar miss a real, T1-documented second planting? Does the real chill-hour estimate
classify apple differently than a bare "z8" assumption would suggest? Is blueberry's real guidance
directionally consistent with the naive frost-anchored assumption? Write the verdict.

- [ ] **Step 6: Write the research note**

Create `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md` with these sections: marquee
anchor + frost dates + source; the 3-crop basket with each crop's naive-vs-real comparison;
the chill-hour comparison for apple; the final ruling (GENERIC-OK / CONDITIONAL-GO / NEW-REGION)
with a one-paragraph rationale; a table of every source cited (institution, URL, what it backs).

- [ ] **Step 7: Update the roadmap doc**

In `docs/region_coverage_roadmap.md`'s "Tier-2 rulings pending (item 5 detail)" section, replace
the mid-Atlantic bullet's unsourced "first read" with the cited ruling (one to two sentences +
a link to the research note), mirroring item 1's "Clone honesty record" phrasing.

- [ ] **Step 8: Commit**

```bash
git add docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md docs/region_coverage_roadmap.md
git commit -m "docs(region): Tier-2 ruling -- mid-Atlantic z8 belt (roadmap item 5)"
```

- [ ] **Step 9: STOP -- present the ruling to Trevor**

Summarize the verdict and evidence; get his review before starting Task 2. If he wants the method
adjusted (deeper basket, different marquee city, etc.), apply that adjustment starting in Task 2.

---

### Task 2: Mid-South belt ruling (AR/OK/TN/MO z8)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md`
- Modify: `docs/region_coverage_roadmap.md` (the item-5 row for mid-South)

**Interfaces:**
- Consumes: `crops_data_final.json` fields (read-only) for `cherry-tomato`, `apple`,
  `blackberry`; the roadmap doc as committed at the end of Task 1.
- Produces: the research note + roadmap-doc row.

- [ ] **Step 1: Pick the marquee anchor and find its real frost dates**

AR carries the most ZIPs (460 z8) of the belt, so AR is the marquee state. WebSearch/WebFetch for
real last/first frost normals for a representative AR z8 city (e.g. Little Rock or Fayetteville).
Record dates, city, source URL (NOAA or University of Arkansas Cooperative Extension).

- [ ] **Step 2: Pull the basket crops' generic biology fields from the canonical (read-only)**

```bash
python3 -c "
import json
d = json.load(open('crops_data_final.json'))
by = {c['slug']: c for c in d['crops']}
for slug in ['cherry-tomato', 'apple', 'blackberry']:
    c = by[slug]
    print(slug, {k: c.get(k) for k in ['weeks_indoors','days_to_maturity_mid','dtm_anchor','frost_tolerance_f']})
"
```

- [ ] **Step 3: Build the naive calendar for `cherry-tomato` and derive it**

Reuse the Step-3 helper script from Task 1, substituting this task's real AR last-frost date from
Step 1. Run it and record the resulting `calendar[]`.

- [ ] **Step 4: Research the belt's real T1 guidance -- actively find the missing sources**

No T1 source for AR/OK/TN/MO is yet catalogued in this dataset (confirmed via
`source_catalog` inspection during the design spec). Use WebSearch/WebFetch to find: (a)
University of Arkansas Cooperative Extension's (or Oklahoma State / University of Tennessee /
University of Missouri Extension's) real tomato planting-date guidance for the marquee zone --
specifically single-cycle vs. a second planting. (b) a real chill-hour estimate for the marquee
city, compared against apple's `chill_hours_required` (same query pattern as Task 1 Step 4).
(c) University of Arkansas's blackberry breeding program (`uark.edu` -- Arkansas is the leading US
public blackberry breeding program, so this should be very well documented) for real
`blackberry` planting/harvest guidance. Record institution, URL, and the specific claim for each.

- [ ] **Step 5: Compare directionally and determine the ruling**

Same GO / CONDITIONAL-GO / NEW-REGION framework as Task 1 Step 5, applied to this belt's evidence.

- [ ] **Step 6: Write the research note**

Same structure as Task 1 Step 6, at `docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md`.

- [ ] **Step 7: Update the roadmap doc**

Replace the mid-South bullet's "first read" with the cited ruling, same pattern as Task 1 Step 7.

- [ ] **Step 8: Commit**

```bash
git add docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md docs/region_coverage_roadmap.md
git commit -m "docs(region): Tier-2 ruling -- mid-South z8 belt (roadmap item 5)"
```

- [ ] **Step 9: STOP -- present the ruling to Trevor** before starting Task 3.

---

### Task 3: Nevada belt ruling (z8/z9/z10)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md`
- Modify: `docs/region_coverage_roadmap.md` (the item-5 row for Nevada)

**Interfaces:**
- Consumes: `crops_data_final.json` fields (read-only) for `cherry-tomato`, `apple`, `garlic`;
  the roadmap doc as committed at the end of Task 2.
- Produces: the research note + roadmap-doc row.

- [ ] **Step 1: Pick the marquee anchor and find its real frost dates**

NV's z9 count (94 ZIPs) dominates over z8 (15) and z10 (1), so the marquee anchor is a z9 NV
city (e.g. Reno's warmer valley pockets, or a Las Vegas-adjacent z9 area -- pick whichever has a
clean citation). WebSearch/WebFetch for real frost normals; record dates, city, source (NOAA or
`unr_ext`, already catalogued in this dataset).

- [ ] **Step 2: Pull the basket crops' generic biology fields from the canonical (read-only)**

```bash
python3 -c "
import json
d = json.load(open('crops_data_final.json'))
by = {c['slug']: c for c in d['crops']}
for slug in ['cherry-tomato', 'apple', 'garlic']:
    c = by[slug]
    print(slug, {k: c.get(k) for k in ['weeks_indoors','days_to_maturity_mid','dtm_anchor','frost_tolerance_f']})
"
```

- [ ] **Step 3: Build the naive calendar for `cherry-tomato` and derive it**

Reuse the Task 1 Step-3 helper, substituting Nevada's real frost date. Run it and record the
result. Nevada's high-desert climate (large diurnal swing, low humidity) is the sharpest test of
the naive frost-anchored model so far -- record whether the naive output looks plausible for a
desert climate or clearly wrong (e.g. missing an irrigation-driven extended season UNR documents).

- [ ] **Step 4: Research the belt's real T1 guidance**

Use `unr_ext` (already catalogued) via WebSearch/WebFetch for: (a) real UNR Cooperative Extension
tomato planting-date guidance for the marquee zone. (b) a real chill-hour estimate for the
marquee city (Nevada's high desert typically delivers ample chill -- confirm with a real source)
compared against apple's `chill_hours_required`. (c) UNR or a relevant source for `garlic` --
Nevada's arid climate is genuinely garlic-friendly (compare against `warm_arid`/`low_desert_az`'s
existing garlic sourcing in the canonical, which may itself be a useful cross-reference even
though those regions don't cover NV's states).

- [ ] **Step 5: Compare directionally and determine the ruling**

Same framework as Task 1 Step 5.

- [ ] **Step 6: Write the research note**

Same structure, at `docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md`.

- [ ] **Step 7: Update the roadmap doc**

Replace the Nevada bullet's "first read" with the cited ruling.

- [ ] **Step 8: Commit**

```bash
git add docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md docs/region_coverage_roadmap.md
git commit -m "docs(region): Tier-2 ruling -- Nevada belt (roadmap item 5)"
```

- [ ] **Step 9: STOP -- present the ruling to Trevor** before starting Task 4.

---

### Task 4: Utah belt ruling (z8)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md`
- Modify: `docs/region_coverage_roadmap.md` (the item-5 row for Utah)

**Interfaces:**
- Consumes: `crops_data_final.json` fields (read-only) for `cherry-tomato`, `apple`, `raspberry`;
  the roadmap doc as committed at the end of Task 3.
- Produces: the research note + roadmap-doc row.

- [ ] **Step 1: Pick the marquee anchor and find its real frost dates**

Utah's 15 z8 ZIPs cluster around the warmest parts of the state (e.g. the St. George / Dixie
area). WebSearch/WebFetch for real frost normals for that area; record dates, city, source (NOAA
or `usu_ext`, already catalogued).

- [ ] **Step 2: Pull the basket crops' generic biology fields from the canonical (read-only)**

```bash
python3 -c "
import json
d = json.load(open('crops_data_final.json'))
by = {c['slug']: c for c in d['crops']}
for slug in ['cherry-tomato', 'apple', 'raspberry']:
    c = by[slug]
    print(slug, {k: c.get(k) for k in ['weeks_indoors','days_to_maturity_mid','dtm_anchor','frost_tolerance_f']})
"
```

- [ ] **Step 3: Build the naive calendar for `cherry-tomato` and derive it**

Reuse the Task 1 Step-3 helper, substituting Utah's real frost date. Run it and record the result.

- [ ] **Step 4: Research the belt's real T1 guidance**

Use `usu_ext` (already catalogued) via WebSearch/WebFetch for: (a) real Utah State University
Extension tomato planting-date guidance for the marquee zone. (b) a real chill-hour estimate for
the marquee city compared against apple's `chill_hours_required` -- Utah's high-desert z8 pockets
may have a genuinely different chill profile than the naive same-zone assumption suggests. (c) USU
Extension guidance for `raspberry` (Utah County has a real historical raspberry-growing identity,
so this should be documented).

- [ ] **Step 5: Compare directionally and determine the ruling**

Same framework as Task 1 Step 5.

- [ ] **Step 6: Write the research note**

Same structure, at `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md`.

- [ ] **Step 7: Update the roadmap doc**

Replace the Utah bullet's "first read" with the cited ruling.

- [ ] **Step 8: Commit**

```bash
git add docs/reviews/notes/2026-07-15/tier2_utah_ruling.md docs/region_coverage_roadmap.md
git commit -m "docs(region): Tier-2 ruling -- Utah belt (roadmap item 5)"
```

- [ ] **Step 9: STOP -- present the ruling to Trevor** before starting Task 5.

---

### Task 5: Alaska belt ruling (z8)

**Files:**
- Create: `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md`
- Modify: `docs/region_coverage_roadmap.md` (the item-5 row for Alaska)

**Interfaces:**
- Consumes: `crops_data_final.json` fields (read-only) for `cherry-tomato`, `apple`, `kale`; the
  roadmap doc as committed at the end of Task 4.
- Produces: the research note + roadmap-doc row.

- [ ] **Step 1: Pick the marquee anchor and find its real frost dates**

AK's 13 z8 ZIPs are the southeast panhandle (e.g. Ketchikan), a maritime climate -- the closest
Tier-2 analog to PNW's own inversion. WebSearch/WebFetch for real frost normals for that area;
record dates, city, source (NOAA or UAF Cooperative Extension Service -- not yet catalogued in
this dataset, so this is one of the two belts requiring active new-source research per the
Global Constraints).

- [ ] **Step 2: Pull the basket crops' generic biology fields from the canonical (read-only)**

```bash
python3 -c "
import json
d = json.load(open('crops_data_final.json'))
by = {c['slug']: c for c in d['crops']}
for slug in ['cherry-tomato', 'apple', 'kale']:
    c = by[slug]
    print(slug, {k: c.get(k) for k in ['weeks_indoors','days_to_maturity_mid','dtm_anchor','frost_tolerance_f']})
"
```

- [ ] **Step 3: Build the naive calendar for `cherry-tomato` and derive it**

Reuse the Task 1 Step-3 helper, substituting Alaska's real frost date. Given AK's short season and
maritime moderation (closer to PNW's own inversion than any other Tier-2 belt), pay particular
attention to whether the naive frost-anchored single-cycle model even fits a warm-season crop like
tomato here at all, or whether the real UAF guidance treats it as marginal/container-only.

- [ ] **Step 4: Research the belt's real T1 guidance -- actively find the missing sources**

No T1 source for Alaska is yet catalogued in this dataset. Use WebSearch/WebFetch to find UAF
Cooperative Extension Service's (`.alaska.edu`) real guidance for: (a) tomato viability/planting
in the southeast panhandle zone (likely transplant-only, possibly marginal outdoors -- record
whatever UAF actually says, honestly). (b) a real chill-hour estimate or equivalent cold-hardiness
guidance for the marquee city, compared against apple's `chill_hours_required` -- likely to show
AK's short growing season, not chill delivery, as the binding constraint (record which it is).
(c) UAF guidance for `kale` (cool-season, likely thrives -- Alaska's long summer daylight is
well-documented for outsized cool-season crop growth).

- [ ] **Step 5: Compare directionally and determine the ruling**

Same framework as Task 1 Step 5. Given this belt is the closest analog to PNW's own inversion,
weigh a NEW-REGION signal seriously if the evidence supports it -- do not default to GENERIC-OK
just because the belt is small (13 ZIPs).

- [ ] **Step 6: Write the research note**

Same structure, at `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md`.

- [ ] **Step 7: Update the roadmap doc**

Replace the Alaska bullet's "first read" with the cited ruling. If this is the 5th and final
belt, also update the roadmap's item-5 program-table row status from "OPEN" to a summary status
(e.g. "RULED 2026-07-15" or similar, matching how items 3/4 read "SHIPPED").

- [ ] **Step 8: Commit**

```bash
git add docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md docs/region_coverage_roadmap.md
git commit -m "docs(region): Tier-2 ruling -- Alaska belt (roadmap item 5, final belt)"
```

- [ ] **Step 9: STOP -- present the final ruling to Trevor.** All 5 belts are now ruled; if any
came back NEW-REGION, confirm with Trevor how each should be queued as its own future roadmap
item before considering this arc closed.

---

## Self-Review

**Spec coverage** (each spec section -> task): SS1-2 context/mechanism -> informs every task's
Step 1/3. SS3 belt scope + order -> the 5 tasks in the specified order. SS4 method -> Steps 1-5 of
every task (marquee anchor, naive baseline, T1 research incl. active source-hunting for mid-South/
Alaska, chill-hour comparison, directional compare). SS5 ruling framework -> every task's Step 5.
SS6 sequencing/checkpoints -> every task's Step 9 STOP gate. SS7 artifacts -> every task's Steps
6-7. SS8 scope boundaries (no canonical/gate/code touch) -> the Global Constraints section, honored
throughout (only the scratch helper script touches code, and it is never committed). SS9 success
criteria -> the cumulative effect of all 5 tasks' Step 7 roadmap updates. SS10 open items (marquee
city pick, crop basket pick) -> resolved with concrete defaults in each task's Steps 1-2, with
room to substitute if research reveals a stronger fit (noted inline, not left blank). No gaps.

**Placeholder scan:** the naive-calendar helper script in Task 1 Step 3 is complete, tested code
(validated against the real deriver during plan authoring -- confirmed output shown). The
Step-1/4 "real frost dates" / "real T1 guidance" content is intentionally NOT pre-filled (it is
the research deliverable itself, gathered via WebSearch/WebFetch at execution time), exactly as
the berry-pilot plan's Task 4 left variety prose to be authored rather than invented in advance --
not a placeholder in the disallowed sense (no "TBD", no vague instruction without a concrete
target and format).

**Type consistency:** the naive-calendar helper's cell shape (`plant_out`, `start_indoors`,
`first_plant_date`, `last_plant_date`, `harvest`, `harvest_start`, `harvest_end`) matches exactly
what `tools/annual_calendar.py`'s `derive_annual_calendar(cell, calendar_basis=...)` consumes
(confirmed against `tools/test_annual_calendar.py`'s own fixtures). The crop-field query pattern
(`weeks_indoors`, `days_to_maturity_mid`, `dtm_anchor`, `frost_tolerance_f`) is identical across
all 5 tasks' Step 2. The GO/CONDITIONAL-GO/NEW-REGION verdict vocabulary is identical across all
5 tasks' Step 5 and matches spec section 5 exactly.
