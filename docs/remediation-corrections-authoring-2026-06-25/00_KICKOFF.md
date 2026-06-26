# Corrections Authoring Batch -- Kickoff (claude.ai authors; Claude Code promotes + gates)

**Date:** 2026-06-25
**Role split:** claude.ai AUTHORS the corrections (source-verified prose + values). Claude Code
PROMOTES them into `crops_data_final.json`, runs the gates, wires the deferred gates, and updates
the state trio. Trevor writes the per-pass prompt and refreshes claude.ai project knowledge.

This is the single corrections batch the gate-hardening arc (B1..B5) deferred. **All the gate
TOOLING is built and committed** (`c462c88`); the gates intentionally do NOT yet block on this data
(several are UNWIRED). This batch authors the data; promotion then flips everything green and the
deferred gates get wired.

## Orientation (read first)
- **Master tension list:** `docs/incognito-audit-remediation-corrections-log.md` (every cell/field,
  organized B1 / date-nits / B3 / B5a / B5b / B5c). This kickoff adds the SHAPES, SOURCES, and the
  pass grouping; the log has the per-cell detail.
- **State trio:** `CURRENT_STATE.md` + `STATE_HISTORY.md` + `LATEST.txt` (dataset @ content SHA
  `144b2fb2`, 18/18 certified). Read at session start.
- **Voice:** `docs/per_crop_verification_methodology` dual-register rules govern all `_seasoned` /
  `_beginner` prose. No em dashes in consumer copy; American English; temps as `75°F`.
- **GOTCHA:** canonical JSON is COMPACT (`separators=(",",":")`, no trailing newline). Claude Code
  handles the apply; author content, not file formatting.

## Why 3 passes (Trevor's call, 2026-06-25)
The corrections span very different rigor levels; do them as themed passes, not one monolith:

---

## PASS 1 -- dates + heat_pause (source-heavy; do first)
**Tension source:** corrections-log §"From B1" (4 cold-on-harvest cells) + §"audit §3" (the ~14 date
nits) + §"From B3" (13 object-less heat_pause cells).

**1a. Resolve the two ambiguous calendar directions (T1 first, then author):**
- `broccoli` northern_tier z5/z6/z7: harvest displays run continuous (e.g. z7 "Apr 26 - Dec 4") but
  the calendar marks the summer months `cold_pause`. Decide from the northern-tier source (UMN/USU):
  is the summer gap heat-driven (`heat_pause` -- if so it needs a Pass-1b backing object) or should the
  harvest display split into spring + fall windows? 3-month z7 gap is the clearest.
- `beefsteak-tomato` ca_south_coast.z9: harvest "Jul - Dec" but calendar Dec = `cold_pause`. Mild
  coastal SoCal rarely hard-freezes in December, so the `cold_pause` token may be the error (harvest
  really runs through Dec). Resolve with UC ANR.
- **GATE-UNLOCK:** once these displays are correct, Claude Code tightens A24 with a
  cold-pause-on-core-harvest rule (today A24 cannot flag these because they would false-positive).

**1b. Back-fill the 13 object-less heat_pause cells (zucchini 5, green-beans 8).** Author a full
`heat_pause` object on each (the corrections-log §B3 table lists every cell + its months + candidate
source). The `months` MUST equal the cell's existing calendar `heat_pause` months (A5 enforces that
alignment). Shape, verbatim from a certified cell (cherry-tomato se_gulf.z8):

```json
"heat_pause": {
  "months": [7],
  "classification": "heat_pause",
  "basis_seasoned": "Summer sowing gap is a heat exclusion, not a frost gap: <crop-specific thermal reason, with the numeric threshold where the source gives one>. (Source Name)",
  "sources": ["uga_ext", "ufifas_ext"],
  "anchoring_urls": {
    "uga_ext": {"url": "https://...", "verified": "2026-06-25"},
    "ufifas_ext": {"url": "https://...", "verified": "2026-06-25"}
  }
}
```

**Gate that proves Pass 1b:** `annual_calendar.heat_pause_backing_violations` (built, UNWIRED) goes
from 13 -> 0; then Claude Code wires it.

**Sources:** UF-IFAS (VH021 veg guide, EP452 S-FL), UGA (C963/C943), UC ANR, UA AZ1005, NMSU
(CR457/CR563), UMN, USU, UH-CTAHR (B-91), TAMU AgriLife. Match each cell to its region's extension.

---

## PASS 2 -- companions (the deferred §5 companions reconciliation)
**Tension source:** corrections-log §B5b (59 bare-name `why` gaps) + §B5c (159 evidence gaps).
**Worksheet (the slice):** `companion_worksheet.md` in this folder -- ONE row per entry needing work,
with its bucket / current values / exact TODO. Author straight down the worksheet.

**2a. why-fill (59 slots).** A companion that RENDERS in a register must carry that register's `why`:
- seasoned-rendered bucket (`good_seasoned`, `*_beginner_seasoned`, `bad_seasoned`) -> `why_seasoned`
- beginner-rendered bucket (`good_beginner`, `*_beginner_seasoned`, `bad_beginner`) -> `why_beginner`
- a both-bucket (`*_beginner_seasoned`) entry needs BOTH. Dual-register voice rules apply.

**2b. evidence transparency (159 slots) -- Trevor's decision (a).** Every companion (good AND bad)
declares an honest `evidence_label` + `confidence`. A labeled-but-speculative pairing is ALLOWED
(beginners keep folk-wisdom companions); an UNLABELED one is not.
- `evidence_label` in {`traditional`, `extension_backed`, `research_backed`, `likely`, `mechanistic`,
  `disputed`}; `confidence` in {`low`, `medium`, `high`}.
- Optional richer backing (encouraged for low-confidence / mechanistic entries) -- the `provenance`
  object as on cherry-tomato's Carrots entry: `{label, confidence, reason, verified_against_sources}`.
  The gate requires only `evidence_label` + `confidence`; `provenance` explains the call.

**Gates that prove Pass 2:** `companion_why_fill_violations` (59->0) and
`companion_evidence_violations` (159->0), both built + UNWIRED; wired after.
**Note:** beginner-only companions are LEGITIMATE curation -- do NOT move entries between buckets for
"reachability." (The per-entry reachability gate was dropped on Trevor's call.)

---

## PASS 3 -- register prose (schema-2.9 dual-register fields on the early anchors)
**Tension source:** corrections-log §B5a (42 fields across cherry/beefsteak/carrot/lettuce + green-beans
+ apple's 5 companion whys, which Pass 2 already covers).

Author the null `_seasoned`/`_beginner` prose. These fields are already FILLED on 14/18 crops -- match
that register and depth. Patterns + crops are in the §B5a table. Templates (from basil, already filled):
- `fertilizer.amount_seasoned`: "3 oz per 10 feet of row (granular), or half-label-strength liquid
  every 2-3 weeks in containers"
- `watering.critical_periods_beginner`: "Keep soil moist when seeds are germinating and for the first
  2 weeks after you transplant seedlings into the garden."

**Decision in this pass:** `lettuce-leaf` `container_notes.overwintering.applicable: null` -- decide
applicability. If lettuce overwintering is N/A, set `applicable: false` (the cherry/beefsteak/carrot
pattern); if it applies, author `approach_seasoned`/`approach_beginner`.

**Gate that proves Pass 3:** `register_fill_violations` (the early-anchor count -> 0); wired after.

---

## Promote + gate + wire (Claude Code, after each pass)
1. Apply claude.ai's authored values to `crops_data_final.json` (compact apply; no other edits).
2. Run the relevant built gate(s) -> confirm the pass's count goes to 0, and `whole_crop_gate` stays
   18/18 PASS (+ the per-batch source-truth sample, the un-gateable layer).
3. After ALL passes land: WIRE the deferred gates into `whole_crop_gate` as new A-numbers
   (`heat_pause_backing_violations`, `register_fill_violations`, `companion_why_fill_violations`,
   `companion_evidence_violations`) and tighten A24 with cold-on-core-harvest (the B1 GATE-UNLOCK).
4. This batch CHANGES `crops_data_final.json` content -> bump the plant-astro submodule so the website
   re-renders. Update `CURRENT_STATE.md` / `STATE_HISTORY.md` / `LATEST.txt` once, at the landing commit.

## Discipline
Accuracy over velocity on the DATA (especially Pass 1 dates). Every claim T1-sourced. No em dashes in
consumer copy. Author N/A as N/A (the `applicable:false` flag or N/A prose), never leave a ruled field
null. Trevor approves every commit.
