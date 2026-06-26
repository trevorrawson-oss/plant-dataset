# Remediation Corrections Log (accumulate during gate work, fix in ONE pass at the end)

**Purpose.** The gate-hardening arc (B1..B5) stays READ-ONLY on `crops_data_final.json`.
Each gate surfaces data tensions as a byproduct; we LOG them here instead of fixing them
one-off. After the gates are built, claude.ai authors all corrections in ONE source-verified
authoring batch (Tier-1 extension sources), Claude Code promotes + gates, and we update
`CURRENT_STATE.md` / `STATE_HISTORY.md` once.

**Two-for-one.** Several corrections UNLOCK a stronger gate (the data tension is the only
reason the gate had to be loosened). Those are flagged "GATE-UNLOCK" -- after the fix lands,
tighten the named gate.

**Process per remediation session:** append what your gate surfaced; do NOT edit the JSON.

---

## From B1 (A24 annual calendar token placement) -- 2026-06-25

All are display-vs-calendar tensions in CERTIFIED crops. Not biology-wrong, not gate-blocking.
A24 deliberately does NOT flag cold-pause-on-harvest precisely because these cells would
false-positive. **GATE-UNLOCK:** once corrected, add a cold-pause-on-core-harvest rule to
`annual_calendar_violations` (A24).

| Crop / cell | Tension | Correction question + source to check |
|---|---|---|
| `broccoli` northern_tier.z5 | harvest `"May 26 - Oct 29"` (continuous) but calendar Jul = `cold_pause` | Split harvest display into spring + fall windows matching the calendar; is the summer gap `cold_pause` or heat-driven (`heat_pause`/`growing`)? Source: northern-tier extension broccoli calendar (UMN/USU). |
| `broccoli` northern_tier.z6 | harvest `"May 12 - Nov 14"` but calendar Jul = `cold_pause` | same as z5 |
| `broccoli` northern_tier.z7 | harvest `"Apr 26 - Dec 4"` but calendar Jun/Jul/Aug = `cold_pause` | same as z5 (3-month summer gap; continuous Apr-Dec harvest is wrong for z7) |
| `beefsteak-tomato` ca_south_coast.z9 | harvest `"Jul - Dec"` but calendar Dec = `cold_pause` | AMBIGUOUS direction: mild coastal SoCal rarely hard-freezes in Dec, so the `cold_pause` token may be the error (harvest really runs through Dec) rather than the display. Resolve with UC ANR before fixing. |

Note: the broccoli summer-gap relabel touches the `heat_pause` layer -- coordinate with B3
(heat_pause backing) so a relabel to `heat_pause` ships WITH its backing, not before.

---

## From the audit §3 (the ~14 MINOR date nits, 2026-06-25) -- to merge into the same batch

Same-season, ~3-6 weeks, none severe (0 wrong-season across 64 sampled cells).

| Crop / cell | Nit | Source |
|---|---|---|
| `onion` fl_peninsula z10/z11 | North-FL Sep-Dec window applied to South FL; the Nov-Dec tail is ~1-2 months late for S-FL bulbing (UF-IFAS South lists "Oct") | UF-IFAS South FL EP452 |
| `beefsteak-tomato` se_gulf z8 | Sep `plant` token ~6-8 weeks past UGA's fall window (Jun15-Jul15) and inconsistent with its own plant_out (Jul 1-20) | UGA C963 |
| `green-beans-bush` northern z3 | Jul 15 back-edge sow matures ~1 week before Sep 15 frost; UMN caps northern-MN beans at end of June (~2-3 wks optimistic) | UMN |
| `carrot` northern z3 | Apr-Jun plant tokens have no corresponding summer harvest window (only the Jul sowing reaches Sep-Oct); Apr token early for z3 cold soil | UMN/USU |
| low-desert AZ warm crops (tomato, beans) | fall succession set ~3-5 weeks later than AZ1005's Jul-Aug | UA AZ1005 |

---

## From B3 (heat_pause thermal backing, A25) -- 2026-06-25

The B3 gate (`heat_pause_backing_violations`, test-first, GREEN) requires every cell whose
calendar SHOWS a `heat_pause` token to carry a backed `heat_pause` object: non-empty
`months` + `basis_seasoned` prose + >=1 `sources`, each anchored by a URL in
`anchoring_urls`. Decided WITH Trevor (2026-06-25): backing lives at the cell, not in a
shared region-heat table, because heat tolerance is crop+region+zone physiology (in
`ca_desert.z9`, carrot pauses Mar-Aug while zucchini pauses Jul-Aug -- same climate, six
different windows across the crops). 51/64 certified heat_pause cells are already fully
backed; **13 are object-less** -- bare calendar tokens on two warm-season crops. These are
NOT biology-wrong (the summer pause is real); they ship the `heat_pause` calendar token
with no `heat_pause` object at all, so the "too hot to sow" claim has no stated reason or
citation. Back-fill a full `heat_pause` object on each (months matching the calendar token,
`basis_seasoned` prose, >=1 Tier-1 source + `anchoring_urls`).

**GATE-UNLOCK:** B3's gate is BUILT + TDD-green + adversarially proven, but **left UNWIRED**
in `whole_crop_gate.py` (wiring it now would correctly turn these 13 cells RED and break the
18/18 green invariant during a READ-ONLY arc). After this back-fill lands, **wire
`annual_calendar.heat_pause_backing_violations` as A25 in `whole_crop_gate.py`** (one line,
mirror A22/A24) -- the test already encodes the green target.

**Coordinate with the broccoli summer-gap relabel (B1 section above):** if any broccoli
`northern_tier` summer `cold_pause` cell is relabeled to `heat_pause`, that new token ALSO
needs a backing object or A25 will (correctly) flag it. The relabel must ship WITH its
backing, in this same batch.

| Crop / cell | heat_pause months (calendar) | Correction question + source to check |
|---|---|---|
| `zucchini-courgette` se_gulf.z8 | [Jul] | Author a `heat_pause` object: why is deep summer a sowing/setting exclusion for summer squash in the humid SE? Source: UF-IFAS VH021 / UGA C963. |
| `zucchini-courgette` se_gulf.z9 | [Jul] | same as se_gulf.z8 |
| `zucchini-courgette` ca_desert.z9 | [Jul, Aug] | Desert mid-summer heat exclusion for summer squash. Source: UC ANR / UA AZ1005. |
| `zucchini-courgette` ca_desert.z10 | [Jul, Aug] | same as ca_desert.z9 |
| `zucchini-courgette` low_desert_az.z9 | [Jul, Aug] | Low-desert mid-summer heat exclusion. Source: UA AZ1005. |
| `green-beans-bush` se_gulf.z8 | [Jun] | Snap beans drop blossoms above ~85-90°F; back the early-summer exclusion. Source: UGA C963 / UF-IFAS VH021. |
| `green-beans-bush` se_gulf.z9 | [Jun, Jul] | same as se_gulf.z8 (two-month window) |
| `green-beans-bush` ca_interior.z8 | [Jun] | Interior-CA early-summer blossom-drop exclusion. Source: UC ANR. |
| `green-beans-bush` ca_interior.z9 | [Jun] | same as ca_interior.z8 |
| `green-beans-bush` ca_desert.z9 | [Jun, Jul] | Desert blossom-drop exclusion. Source: UC ANR / UA AZ1005. |
| `green-beans-bush` ca_desert.z10 | [Jun, Jul] | same as ca_desert.z9 |
| `green-beans-bush` low_desert_az.z9 | [Jun, Jul, Aug] | Low-desert 3-month blossom-drop exclusion. Source: UA AZ1005. |
| `green-beans-bush` fl_peninsula.z10 | [Jun, Jul] | South-FL summer blossom-drop exclusion. Source: UF-IFAS VH021 / EP452. |

Note: the `months` authored on each object must equal the cell's calendar `heat_pause`
months (A5 `annual_coherence_violations` already enforces that alignment), so use the
"heat_pause months (calendar)" column verbatim.

---

## From B4 (photoperiod day_length_type <-> window fit, A9) -- 2026-06-25

**No data tensions surfaced.** The window-fit rule (added to `photoperiod_violations`, A9)
ran clean across onion's 20 real cells: every cell's `plant_out` season agrees with its
`recommended_day_length_type` (long-day spring-planted, short-day fall/winter-planted,
intermediate fall-to-early-spring). 0 false positives; the 4 injected mismatches (long-day
fall/winter, short-day spring, intermediate summer -- incl. the audit's exact Jan-only
injection) all bounce. Wired live (no back-fill needed); onion stays GATE: PASS.

---

## From B5 (register wiring + companion gates) -- 2026-06-25

Trevor's calls this session: (1) the companion EVIDENCE bar = **option (a)** -- transparency, not
T1-only: every companion must declare an honest `evidence_label` + `confidence`, and a labeled
speculative pairing (mechanistic/low) is allowed (beginners keep folk-wisdom companions). (2) Build
the per-register WHY-FILL gate; **drop the per-entry reachability gate** -- a beginner-only companion
(`good_beginner`/`bad_beginner`) is legitimate curation, NOT a bug. So **orange-navel's beginner-only
goods/bads are correct as-is; no action.**

**Tooling DONE this session (test-first, all green, JSON untouched):**
- `register_fill_gate` over-flag FIXED: it now skips `_seasoned`/`_beginner` children of an
  `{applicable: false}` structured-N/A object (cherry/beefsteak/carrot overwintering). `applicable:
  null` and `applicable: true` still violate.
- `companion_shape_gate`: added `companion_why_fill_violations` + `companion_evidence_violations`
  (separate from the wired A19 -- they are UNWIRED pending back-fill).
- `register_completeness_gate`: extracted per-crop `register_completeness_violations(crop)` and
  **WIRED it into `whole_crop_gate` as A25** (0 FP across all 123 crops -- pure armor, stays green).

**GATE-UNLOCK -- after the back-fill below lands, wire these into `whole_crop_gate`:**
`register_fill_violations`, `companion_why_fill_violations`, `companion_evidence_violations` (each
the next free A-number; A25 register_completeness is already wired).

### B5a. register_fill debt -- 42 unauthored register fields across 6 early-anchor crops
These are real schema-2.9 dual-register prose gaps (the field is FILLED on 14/18 crops; null only on
the early anchors that certified before the field existed). cherry-tomato 8, beefsteak-tomato 8,
carrot 9, lettuce-leaf 11, apple 5, green-beans-bush 1. Patterns to author:

| Field (×count) | Crops | Note |
|---|---|---|
| `fertilizer.amount_{seasoned,beginner}` (8) | cherry, beefsteak, carrot, lettuce | per-feeding amount prose |
| `watering.method_note_{seasoned,beginner}` (8) | same 4 | supplementary watering note |
| `watering.critical_periods_{seasoned,beginner}` (8) | same 4 | drought-sensitive stages |
| `container_notes.self_watering_notes_{seasoned,beginner}` (8) | same 4 | self-watering guidance |
| `start_method.hardening_off_beginner` (2) | carrot, lettuce | direct-sown: author N/A prose or set N/A |
| `moon_phase_preference.source_note_seasoned` (1) | green-beans | |
| `companions.*_beginner_seasoned[*].why_seasoned` (5) | apple | the present-null subset of B5b below |
| `container_notes.overwintering.approach_{seasoned,beginner}` (2) | lettuce | **`applicable: null`** -- DECIDE applicability (set `applicable:false` + N/A, or author the approach); cherry/beefsteak/carrot already use `applicable:false` |

### B5b. companion why-fill debt -- 59 bare-name renders across 14 crops
A companion that renders in a register but lacks that register's `why` shows a bare name. 44 missing
`why_seasoned`, 15 missing `why_beginner`. Worst: apple 10 (its `good_beginner_seasoned` entries have
`why_seasoned: null` AND no `why_beginner` -- bare in both modes). Others: carrot/basil/zucchini/
green-beans/broccoli/onion/strawberry/lavender/zinnia/orange-navel/peach/lemon/blueberry. Rule for the
back-fill: a `*_seasoned`/`*_beginner_seasoned` entry needs `why_seasoned`; a `*_beginner`/
`*_beginner_seasoned` entry needs `why_beginner` (both-bucket entries need both).

### B5c. companion evidence-transparency debt -- 159 gaps (decision a)
Across 140 certified companion entries: **77 lack `evidence_label`**, **82 lack `confidence`**. Author
both on every entry: `evidence_label` in {traditional, extension_backed, research_backed, likely,
mechanistic, disputed}; `confidence` in {low, medium, high}. (Where present today the values are all
valid -- the debt is absent keys, not bad values.) Speculative-but-labeled is allowed.

---

## From Pass 1 (dates + heat_pause) -- LANDED 2026-06-26; deferred items below

Pass 1 landed (content SHA `6c009feb` -> `5fe0a15b`): 16 heat_pause objects (13 zucchini/green-beans +
3 broccoli relabel), broccoli z5/z6/z7 cold_pause->heat_pause + harvest splits, beefsteak ca_south_coast.z9
Dec->harvest + se_gulf.z8 Sep->growing, onion fl_peninsula z10/z11 plant_out->Oct + CC calendar recompute.
Wired `heat_pause_backing` (A28); tightened A24 with cold-pause-on-core-harvest (the broccoli GATE-UNLOCK).

**Deferred (claude.ai left under the conservative rule + one CC surfaced; NOT blockers):**
- `carrot` northern_tier.z3 -- the Apr-Jun succession sowings show no matching spring/summer harvest
  window (display-coherence gap, not a date error). Surface the earlier harvest windows.
- `beefsteak-tomato` + `green-beans-bush` low_desert_az.z9 -- strict UA AZ1005 fall-succession alignment
  (~Jul-Aug) would require reconciling the cell's Jun-Aug heat_pause back-edge WITH the fall window
  together; a methodology choice, surfaced not silently applied.
- `beefsteak-tomato` ca_north_coast.z10 -- a `wait` token sits on a harvest month (Nov); a separate
  `wait`-legibility item (one of the 2 pre-existing z10 release_verify notes), out of Pass-1 scope.
  **GATE-UNLOCK:** once the z10 `wait` tokens are resolved, A24's harvest rule can extend to `wait`.
- (optional) `beefsteak-tomato` ca_south_coast.z9 -- UC ANR supports a harvest tail into January;
  extending the `Jul - Dec` display to "Jul - Jan" is defensible but larger than the Dec->harvest fix.
