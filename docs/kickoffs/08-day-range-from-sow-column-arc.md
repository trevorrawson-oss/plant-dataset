# Kickoff: `day_range_from_sow` column GS arc (register entry #1)

**Created 2026-07-03** (plant-app session, on Trevor's green-light). Method:
`docs/gs_cross_crop_field_addition_v0.md` (the column-arc template). Register:
`docs/field_addition_register.md` entry #1 — this kickoff moves it from **deferred** toward
**contract-locked, scheduled**. Read alongside `07-remaining-gs-anchors.md` for roster position.

## 0. The product goal (Trevor, 2026-07-03 — this reframes the field)

> Give an accurate countdown to harvest based on growth stages — so whether someone starts from
> seed, transplants a seedling, or transplants an established plant, the prediction is accurate to
> a few days.

The app's add/edit flows now ask "what growth stage is it?" for **every annual crop** and anchor the
harvest countdown to the picked stage: `headStartDays = stage.dayStart`, `harvest ≈ days_to_maturity
− (days since planting + headStartDays)`. That anchor is only as good as the per-stage day data:

- Crops **with** `day_range_from_sow` on every stage → real day offsets → countdowns accurate to days.
- Crops **without** → the app synthesizes evenly-spaced estimates over `days_to_maturity` — honest but
  coarse (a "seedling" guessed at day 14 when reality is day 21 shifts the countdown a week).

So this arc is no longer just the seed-trays sprout window (the register's original consumer). It is
the data backbone of stage-anchored harvest prediction across the whole app.

## 1. What changed since the v0 proposal (why kick off now)

1. **Two new consumers** (plant-app, shipped 2026-07-02/03): the growth-stage picker in every
   add/edit sheet (derives `dayStart = day_range_from_sow[0]` per stage) and the harvest countdown it
   anchors. Original consumer (seed-trays sprout window) still stands. All read gracefully —
   present-or-estimated, never fabricated as precise.
2. **Scope upgrade — the contract is per-stage, not germination-only.** The register row describes a
   germination window. The app consumes `day_range_from_sow` on **every** `growth_stages[]` entry.
   Crops with only a germination range would still fall back to estimates for later stages, which is
   where harvest-countdown accuracy actually lives (the "transplanted an established plant" case).
3. **Roster reality:** app-side coverage today is 22 of 50 app-certified crops with full per-stage
   ranges, 28 with none. Annuals among the missing (the ones whose countdowns are currently
   estimates): bok-choy, broccoli, brussels-sprouts, butternut-squash, cabbage, cauliflower,
   collards, cucumber, eggplant, kale, kohlrabi, marigold, nasturtium, pumpkin, spinach, sunflower,
   swiss-chard, watermelon, zinnia, zucchini-courgette (+ microgreens-mix, a special fast case).
   The perennials/trees among the 28 (apple, blueberry, lavender, lemon, orange-navel, peach,
   strawberry) are the legitimately-null lane. Dataset-wide coverage across all 80 certified: run
   the coverage report as step one — don't trust these app-era numbers.

## 2. Field contract (template step 1 — lock before touching any crop)

- **Field:** `growth_stages[].day_range_from_sow = [min, max]` — integer days from sow to reaching
  that stage. On **every stage** of a seed-grown crop, not only germination.
- **Shape gate:** two integers, `0 ≤ min ≤ max`; `min` non-decreasing across a crop's stage order;
  first stage min is typically 0–14 (sow/germination).
- **Semantics:** "days from sow" is from direct seeding; tray-vs-direct is a `weeks_indoors`
  question and does NOT change this field (per v0 §4).
- **Legitimately null (empty is CORRECT, not a gap):** crops not grown from sow by the user —
  perennials/trees from bare-root/nursery stock (their `growth_stages_year_one` is year-scale), and
  future non-plant archetypes (mushrooms). The app already gives these no stage picker.
- **Sourcing:** for most crops this is a *structuring* job — the numbers exist as prose in each
  stage's `what_to_look_for` text; lift into the field, cite the same T1 set already on the stage.
  Where prose has no number for a mid stage, source it — do not interpolate (interpolation is the
  app's fallback job, not the dataset's).
- **Days-to-maturity coupling:** the final/harvest stage's range should be consistent with the
  crop's `days_to_maturity` (the countdown uses both). Flag crops where they disagree rather than
  silently averaging.

## 3. Sequencing (the register's standing principle: never mid-cert)

The register's trigger is "full roster (~123) certified." Position today (see 07-remaining doc):
80 certified, 34 staged drafts → ~114 after the certify waves, then 11 design-case shells.
Pragmatic reading, for Trevor/cert session to ratify:

- **Run the column pass once the 34 staged drafts certify (~114).** The remaining 11 shells are
  almost entirely out-of-band for this field anyway (5 mushrooms = N/A archetype, avocado/olive =
  null-lane trees; only sweet-corn, artichoke, asparagus would ever carry it) — waiting for them
  buys nothing and stalls the app's headline accuracy feature.
- **Do NOT bolt ranges onto the 34 staged drafts now** — they're authored and gate-clean; reopening
  them mid-pipeline is exactly what the standing principle forbids. The post-certify column pass
  catches them.
- **Fold-forward decision (template step 5):** the register currently says "NOT folded into the
  per-crop checklist this round." Recommend revisiting after this pass: with the picker + countdown
  live, every future crop certified without ranges ships with estimated countdowns and reopens the
  backfill treadmill the template exists to prevent.

## 4. Pilot set (template step 2 — stress the contract, not just the happy path)

- **Fast case:** broccoli or cabbage (prose numbers exist; brassica germination is quick and
  well-sourced).
- **Slow case:** a slow germinator from the newly-staged herbs if certified by then (parsley is the
  classic 14–28-day case) — else parsnip-class from the roster.
- **Legitimately-null case:** apple (tree, bare-root) — prove the pilot records "correctly absent,"
  not a TODO.
- **Edge case worth one pilot slot:** microgreens-mix (sow→harvest in ~10 days, stages days apart —
  stresses the min≤max/monotonic gate at small values).

## 5. Rollout gate + coverage (template step 3)

- Schema-validation check (shape + monotonicity above) wherever the existing gate tooling lives.
- Coverage report: per crop × stage — `present / legitimately-null / TODO` — so partial rollout is
  visible, never silent. Publish the report in the batch's MORNING_REPORT style.
- Per-field provenance on amended certified crops (v0 §3): a `field_additions` entry (or
  `verification_status` sub-entry) with the column's source(s) + date. Never reopen the cert.

## 6. Definition of done

1. Contract above ratified (or amended) by the cert session; register row updated (status,
   per-stage scope, new consumers).
2. Pilot 4 crops through the correction + review loop.
3. Column pass across all certified seed-grown crops; coverage report shows zero TODO for annuals.
4. App verification: rebuild guides (`build:guides`), confirm the app's stage derivation prefers
   ranges everywhere (the plant-app session can verify — the derivation and its tests already
   exist; coverage shift is visible in `stagesFor`'s ranged-vs-synthesized split).
5. Fold-forward decision recorded in the register (§3 above).

---
*Cross-refs: `gs_cross_crop_field_addition_v0.md` (method), `field_addition_register.md` (queue),
plant-app `src/lib/crop-stages.ts` (the consuming derivation: authored → ranged → even-spacing),
plant-app memory `crop-sheet-consolidation` (how the picker/countdown shipped).*
