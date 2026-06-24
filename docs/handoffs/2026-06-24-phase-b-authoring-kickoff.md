# Phase B authoring kickoff (claude.ai authoring lane)

**Created:** 2026-06-24 (Claude Code, audit Phase B / F4-F7)
**Lane:** claude.ai AUTHORS the sourced values + copy; Claude Code already ARMED the gates and
did the structural reshape, and will RELEASE (verify -> promote) the patch.
**Depends on:** the Phase B gate commit (companion_shape_gate A19, display_readiness_gate A20,
tips-coverage in A12, + the companion structural reshape). Confirm the canonical SHA in
`CURRENT_STATE.md` before authoring.

## The mission, in one line

Fill the **4 crops still RED** under the new Phase B gates so `whole_crop_gate` returns to
**18/18 green**: lemon + orange-navel display values (F5), apple + onion tips (F7), plus the
companion **why** copy for the entries Claude Code reshaped from bare strings (F4/F6).

## Why this exists + how to check your work

The post-roster audit found systematic, gate-able defect classes. Claude Code wrote a scanner
for each, wired it into `whole_crop_gate`, and fixed everything that was a pure STRUCTURAL
reshape. What remains needs **authored, sourced content**, which is your lane. **The gate is the
spec:** after your patch, every one of these must be 0:

```
python3 tools/whole_crop_gate.py lemon          # -> GATE: PASS
python3 tools/whole_crop_gate.py orange-navel    # -> GATE: PASS
python3 tools/whole_crop_gate.py apple           # -> GATE: PASS
python3 tools/whole_crop_gate.py onion           # -> GATE: PASS
```

Deliver a patch per `docs/handoff_patch_format_v1_0.md` (+ source-catalog mints for any new T1
IDs). Hard rule, as always: **T1 sources only** (university extension / IFAS / UC ANR / etc.).

---

## WORK ITEM 1 -- Display values, F5 (gate A20: `display_readiness_gate.py`)

A crop can certify (biology + sources) and still render a BLANK Hero/Ph/Feeding card. Two citrus
are RED. **Much of the answer already exists in each crop's own sourced prose** (the `note_seasoned`
/ `notes_seasoned` strings cited below) -- this is mostly lifting a render-ready value out of prose
you already authored, then confirming against the cited source.

### lemon (6 blanks)
| field | current | needs |
|---|---|---|
| `sunlight` | `null` | a sun enum (citrus is full sun) |
| `sunlight_hours` | `[]` | `[lo, hi]` integer hours |
| `water` | `null` | a water enum |
| `fertilizer.type` | `null` | render-ready string |
| `fertilizer.timing` | `null` | render-ready string |
| `fertilizer.frequency` | `null` | render-ready string |

The feeding grid is derivable from lemon's existing sourced `fertilizer.notes_seasoned` ("Feed in
light, frequent doses from late winter or early spring through summer, then stop by late summer...").
`npk_ratio` is already `null` + `npk_tag: "Nitrogen-forward"` (correct, ratio-less) -- leave it.

### orange-navel (5 blanks)
| field | current | needs |
|---|---|---|
| `ph.preferred_range` | `[]` | `[lo, hi]` (its `note_seasoned` says "roughly pH 6.0 to 7.0") |
| `container_notes.container_ok` | `null` | a real **True/False decision** (if True, also `min_pot_gallons`) |
| `fertilizer.type` | `null` | render-ready string |
| `fertilizer.timing` | `null` | render-ready string |
| `fertilizer.frequency` | `null` | render-ready string |

`sunlight` / `sunlight_hours` / `water` / `spacing_inches` are already filled on orange -- do not touch.
The feeding grid is derivable from orange's existing sourced `fertilizer.notes_seasoned`.

**Archetype note:** the gate respects legitimate N/A -- in-ground trees may set `container_ok:false`
(peach does); pick the honest answer for citrus (commonly container-friendly -> True + a pot size).

---

## WORK ITEM 2 -- Tips coverage, F7 (gate A12: `tips_violations`)

Every `growth_stages` id must have a renderable tip (`text_seasoned` / `text_beginner`) or the
journey card draws a blank slot. Two single-stage gaps remain:

- **apple** `tips_by_stage.scaffold_formation` -- add a tip (training the scaffold/branch
  framework in the early years). Stage id is `scaffold_formation`.
- **onion** `tips_by_stage.bulb_initiation` -- add a tip (bulbing triggered by daylength +
  temperature; keep water/N steady as bulbing starts). Stage id is `bulb_initiation`.

Shape each new tip exactly like the crop's existing tips: a list of `{text_seasoned, text_beginner,
sources, anchoring_urls}` under the stage-id key. (Use the crop's other `tips_by_stage` entries as
the template; match the dual-register + anchoring conventions so gates B/F stay green.)

---

## WORK ITEM 3 -- Companion `why` copy, F4/F6 (gate A19: `companion_shape_gate.py`)

Claude Code converted the bare-string / wrong-bucket companions to the certified OBJECT shape so
the gate is green and the rows no longer vanish, but the reshaped entries currently carry **only a
`name`** -- they render with a blank rationale until you author the `why`. (apple already kept its
`why` -> renamed to `why_seasoned`; no new apple copy needed.) The sourced rationale already lives
in each crop's companion `note_seasoned` / `note_beginner` -- this is restructuring it into per-entry
`why`, not new claims.

Entries needing `why` (all under `companions.<bucket>`):

- **lemon** -- `bad_seasoned`: "Turfgrass within the drip line", "Moisture-holding mulch against the
  trunk"; `bad_beginner_seasoned`: "Lawn grass", "Weeds at the trunk".
- **orange-navel** -- `good_seasoned`: "Pigeon pea", "Fava bean"; `good_beginner_seasoned`: "Comfrey",
  "Yarrow"; `good_beginner`: "White clover", "Nasturtium", "Marigold"; `bad_beginner_seasoned`:
  "St. Augustine grass"; `bad_beginner`: "Turf grass", "Bermuda grass".
- **basil** -- `good_beginner_seasoned`: "Marigolds", "Tomatoes", "Peppers"; `bad_beginner_seasoned`:
  "Sage", "Fennel". (The strong tomato pairing was moved into the seasoned-readable bucket; give it
  the richest `why`.)

**Follow the certified carrot/onion pattern, and mind RegisterText:**
- `*_seasoned` bucket entries carry `why_seasoned` (no `why_beginner` sibling).
- `*_beginner_seasoned` (both-mode) entries: the card's `RegisterText` BLANKS seasoned mode if only
  `why_beginner` is set. So either (a) give a both-mode entry `why_seasoned` (renders in both via the
  fallback), or (b) use the carrot two-bucket pattern -- the same companion in `good_seasoned`
  (`why_seasoned`) AND `good_beginner_seasoned` (`why_beginner`), reconciled by `name` in the card.
- Optional but ideal: promote the best companions to the rich certified object (add `category` from
  {pest_deterrent, structural, pollinator, soil_health}, `timing`, `provenance`, `sources`,
  `anchoring_urls`) so they group + tag like carrot's.

---

## SMALL RIDERS (optional; Claude Code deferred these as not-mechanical)

1. **blueberry variety chill -> numeric -- REPRESENTATION DECIDED by Claude Code (apply this).**
   Blueberry's 13 `varieties.recommended` store `chill_hours` as an approximate range string
   ("~800-1000", "~250", "~150-300"); the tree varieties use a numeric `chill_hours_required` scalar
   that `chillBuckets` (tree.ts) reads. Normalize blueberry to BOTH, deterministically:
   - **`chill_hours_required`** (numeric SCALAR) = the LOW end of the string. This is the chill-gating
     threshold ("minimum hours to fruit reliably"), semantically identical to the tree scalar, so the
     existing chill machinery reads it directly. (Duke "~800-1000" -> 800; Emerald "~250" -> 250;
     Sharpblue "~150-300" -> 150; Powderblue "~550-650" -> 550; Brightwell "~350-400" -> 350.)
   - **`chill_hours_range`** `[lo,hi]` = the parsed band, for the genuine-range strings (preserves the
     cultivar character for display). Single-value strings ("~1000","~250") -> range omitted/null.
   - **Drop the `chill_hours` string** (the "~" approximate is captured by the rounded scalar + range;
     matches the trees, which carry null `chill_hours`).
   - Deterministic transform -> a small migration; then Claude Code wires a gate (required-present +
     numeric on chill-gated berry varieties) + the card (see rider 2).
2. **Blueberry SHOULD get a chill card -- Claude Code RECOMMENDS building it (a follow-up, not a fold-in).**
   Blueberry is chill-GATED: cultivar choice by region is the whole game (a ~1000 hr northern highbush
   will not fruit in a ~250 hr climate; a ~150 hr southern highbush needs almost no winter chill). The
   crop currently shows growers NO chill info -- a real gap that can cause failure. Build a
   berries_woody analog of the tree `ChillHoursCard`: "your area banks ~X" (from the shared
   `region_chill_delivered` table, Phase A) vs "these cultivars need ~Y" (the normalized scalar above),
   grouping recommended cultivars by chill class (northern highbush / southern highbush / rabbiteye)
   with a "best for your chill" highlight. COUPLED to rider 1 + the shared chill table -> build it in
   the same motion as the combined release. (Trevor: this is a small new card on the berry guide; flagged
   for your nod.)
3. **npk_tag polish (onion / blueberry) -- POLISHED by Claude Code via the copywriting skill (apply):**
   - onion `fertilizer.npk_tag`: "Nitrogen-forward early" -> **"High nitrogen early"** ("forward" was
     jargon, "early" dangled; the taper-at-bulbing nuance stays in the npk_hint prose).
   - blueberry `fertilizer.npk_tag`: "Acid-forming, ammonium N" -> **"Acidic, ammonium-based"**
     ("ammonium N" was cryptic; "ammonium-based" reads as "use azalea/acid food" to a grower).
   - (lemon "Nitrogen-forward" + lavender "Lean soil, minimal feed" read fine; leave them.)

### Layer-2 source-truth corrections (riders 4-6) -- NOW VERIFIED + T1-SOURCED by the Phase C QA pass

The Phase C widened source-truth sample (4 region-scoped agents, ~40 cells; see
`plant-astro/docs/gs-arc-source-truth-qa-2026-06-24.md`) **re-confirmed the two known nits and found
one new MINOR.** Exact corrected values + sources below. Apply these as part of this combined release.
(0 wrong-season errors found anywhere -- the corpus is sound on dates; these are the only 3 cells.)

4. **carrot northern_tier z3 harvest string** -- VERIFIED CLEAN, no cascade, apply as-is.
   - `harvest: "May - Jun, Sep - Oct"` -> `"Sep - Oct"`; `harvest_start: "Jun 23"` -> `"Sep 1"`
     (keep `harvest_end: "Oct 15"`).
   - Source: UMN Extension "Growing carrots and parsnips" (sow ~Apr 15 + fall mid-July; harvest
     Sep-Oct; 65-80d DTM). A May-Jun harvest is unreachable from any z3 sowing.
   - **No cascade:** plant months are unchanged, so `successions_realized: 6` does NOT move, and
     `derive_annual_calendar` reproduces the stored calendar EXACTLY from the corrected `harvest`
     (this turns a non-enforced drift cell into a re-derivable one). Pure coherence repair.

5. **lettuce-leaf ca_interior z8 AND z9 plant window** -- add the dropped fall window (cascades).
   - `plant_out: "Aug 1 - Aug 31, Nov 1 - Mar 31"` -> `"Aug 1 - Oct 31, Nov 1 - Mar 31"` (add the
     plantable **Sep-Oct** fall sowing -> continuous Aug-Mar cool-season run). **The spring side through
     Mar 31 is CORRECT -- do NOT trim it** (UC's spring lettuce window is Feb-Apr; the audit's
     "over-extends to Mar 31" worry was NOT supported by the source).
   - Source: UCCE Sacramento EHN 11 + UC Master Gardeners of Sacramento monthly tips ("transplant
     lettuce February to April **or September to October**"); Sep-Oct is the prime Central Valley fall
     window.
   - **Cascade:** re-resolve via `table_13_2_month_resolution` so Sep/Oct become plant tokens, then
     recompute `successions_realized` (currently 12, GLOBAL cap 12). The two-row harvest still renders
     from the `harvest` string.

6. **carrot low_desert_az z9 heat-gap shift** (NEW, MINOR) -- shift the summer gap one month earlier.
   - Effective plant should be `Jan-Apr + Aug-Dec` with `heat_pause` **May-Jul** (currently includes a
     wrong **May** plant and drops a valid **Aug**; heat_pause is currently Jun-Aug).
   - Source: **UArizona AZ1005** "Vegetable Planting Calendar for Maricopa County" -- carrot sow marks
     only Jan,Feb,Mar,Apr,Aug,Sep,Oct,Nov,Dec (grid machine-parsed; no May/Jun/Jul, soil >85F
     germination ceiling).
   - **Cascade:** re-resolve via `az1005_month_resolution`; recompute `successions_realized` (12).

---

## What Claude Code already shipped (so you don't redo it)

- Gates (test-first, wired into `whole_crop_gate`): **A19** companion shape, **A20** display-readiness
  (archetype-aware), **A12** extended to tips COVERAGE. 33 tooling tests green.
- Companion structural reshape on lemon / orange-navel / basil / green-beans-bush / apple -> all 5
  pass A19 (bare strings objectified, apple's goods/bads moved into seasoned-readable buckets).
- plant-astro `CompanionsCard` hardened (`src/lib/companions-normalize.ts`, unit-tested) so a
  malformed companion can never silently vanish again.
