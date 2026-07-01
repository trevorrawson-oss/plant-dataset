# Calendar-coherence bugs (found by Trevor in the rendered guides, 2026-06-30)

Two systemic calendar-derivation bugs surfaced by eyeballing the rendered guides. Both live in
`tools/annual_calendar.py` (`derive_annual_calendar`) and both slipped past every certification
because **the gate suite checks calendar STRUCTURE, not calendar LOGIC** -- there is no invariant
that the 12-token sequence is temporally coherent. Both touch the certified gold-standard anchors
AND the 13 crops live on the site. HIGH PRIORITY -- do these before more authoring.

## Bug 1 -- "growing after harvest"
- **Signature:** a `growing` token whose previous month (wrapped) is `harvest`. You cannot be
  "growing" in a month when nothing was planted before it -- growing must follow plant/indoors.
  (Trevor's example: cabbage `ca_interior` z9 -> `...Dec=harvest, Jan=growing, Feb=plant`.)
- **Scope:** 98 cells across 27 crops, anchors included.
  Per-crop counts: parsnip 12, zucchini-courgette 9, cucumber 9, cabbage 7, orange-navel 6,
  broccoli 5, kohlrabi 5, cauliflower 4, butternut-squash 4, pumpkin 4, cherry-tomato 3,
  beefsteak-tomato 3, basil 3, lettuce-leaf 2, arugula 2, bok-choy 2, cilantro-coriander 2,
  dill 2, eggplant 2, watermelon 2, marigold 2, sunflower 2, zinnia 2, turnip 1, tomatillo 1,
  nasturtium 1, beet 1.
- **Nuance:** flat wrong for DETERMINATE/head crops (cabbage/cauliflower/broccoli) -- the plant is
  cut and done. For INDETERMINATE producers (tomato/basil/cucumber) the plant really is still
  growing-while-producing, but it should render as `harvest`, not `growing`. The fix must
  distinguish, or normalize "still in ground after first harvest" to `harvest`.

## Bug 2 -- "one-month harvest hole"
- **Signature:** a non-harvest month sandwiched between two harvest months (harvest, gap, harvest)
  in the harvest WINDOWS. (Trevor's example: lettuce-leaf `ca_interior` z8 & z9 ->
  `harvest='Sep - Oct, Dec - May'`, November punched out; the Nov calendar token is `plant`.)
- **Scope:** 49 one-month harvest holes across 18 crops, anchors included.
  Per-crop counts: collards 8, kale 5, green-beans-bush 4, lettuce-leaf 4, arugula 3,
  cilantro-coriander 3, dill 3, basil 2, zucchini-courgette 2, broccoli 2, radish 2, parsley 2,
  turnip 2, beet 2, cucumber 2, spinach 1, snow-peas 1, cabbage 1.
- **Nuance:** for a continuous/succession crop in a mild region the harvest should bridge the hole
  (continuous Sep-May). Some holes may be a real gap between two discrete plantings -- the fix
  should bridge holes only inside a continuous producing span, not invent harvest where there is none.

## The fix (Claude Code lane -- TDD a gate, then fix the deriver, then re-derive)
1. **Add a calendar-coherence gate** (TDD, RED before GREEN): inject `harvest->growing` and a
   `harvest, X, harvest` hole into a scratch crop and confirm each bounces. Candidate invariants:
   a `growing` token must be reachable from a `plant`/`indoors` without passing `harvest`; no
   isolated one-month harvest hole inside a continuous harvest run. Adversarially stress it; make
   sure it does NOT false-positive on legit two-crop-per-year gaps (use the certified anchors as
   the 0-false-positive bar).
2. **Fix `derive_annual_calendar`** so it stops emitting both patterns (extend/normalize harvest,
   or `off`/`cold` between crops; bridge holes inside a continuous span).
3. **Re-derive the affected cells** surgically (derive-in-throwaway + splice-into-pristine-snapshot,
   the established technique) -- this changes certified anchors + the live 13, so it is a CONTENT
   release: state trio + release verification + Trevor sign-off. Re-run both scans -> expect 0.

## What NOT to over-correct (preserve these -- they are NOT bugs)
The fix must kill the two IMPOSSIBLE sequences above WITHOUT flattening legitimate seasonal biology.
Do NOT "fix" either of these:
- **Legit planting GAPS.** A crop need not plant every month. A Nov-Dec (deep-winter) planting gap is
  correct: short days (under ~10 h) + cold mean a NEW sowing barely germinates/establishes, so the
  productive windows are fall (establish + crop through winter) and late-winter/spring (as days
  lengthen). Skipping the deep-winter trough for new plantings is right -- do NOT force a `plant`
  token into every month. (In a mild interior valley you *can* stretch some sowings into Nov-Dec; that
  is a variety-pass refinement, not a coherence bug.)
- **The Plant-row-goes-quiet-during-harvest rendering.** When a crop is in the ground being HARVESTED
  (e.g. cool-season crops cropping Nov-Jan in mild ca_interior z9), the Plant row correctly renders
  empty (harvest shows on the Pick row). It LOOKS like a winter gap but the crop is active -- a
  render/UX matter (plant-astro/plant-app), NOT a dataset fix, and NOT a reason to add a cold_pause. A
  cold-hardy cool-season crop in a mild winter is not cold-stopped.

**The litmus:** fix sequences that are LOGICALLY impossible (growing with nothing planted before it; a
harvest run with a single punched-out month). Leave intact anything that is a valid biological CHOICE
(which months to plant; harvesting through a mild winter). When in doubt, ask the original session.

## How they were found
Not by any gate -- Trevor caught both by reading the rendered ca_interior z9 calendars during the
go-live of the first 13. The human-review layer doing exactly what it is for.
