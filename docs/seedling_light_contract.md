# Seedling / germination light field contract (register #6) -- v1 (design locked)

**Status:** **ROLLOUT COMPLETE 2026-07-07** -- germination_light + seedling_light on all 114 certified
crops (germ SET 85 / N-A 29; seedling bright_default 49 / na 57 / blackout_then_bright 8). Only TODO =
the 10 uncertified §E shells. See the ROLLOUT section at the bottom. (Design was brainstormed and signed
off with Trevor before authoring.) Follows the column-GS-arc method (`docs/gs_cross_crop_field_addition_v0.md`): lock
the field spec, prove it on a diverse pilot (including the legitimately-N/A case), gate it, then roll
out with a coverage report. Carries forward the register #7 "better system" discipline: alongside a
value, store a small CONTROLLED-VOCAB enum saying what it MEANS, so the app can act and message
deterministically -- no free prose, no LLM guess, and it is gate-validatable.

**The core insight (do NOT re-derive -- settled in research + brainstorming):**
- **SEEDLING light is a DEFAULT + a few typed exceptions, NOT a per-crop authored column.** Indoor-
  started seedlings all want the same thing: bright light, ~14-16 h under lights, kept close, to grow
  stocky and avoid etiolation. Our own stage prose confirms it (tomato/pepper/eggplant/celery say
  "strong/bright light, grow stocky"), and it does NOT track the mature plant's sun preference (celery
  is part-shade at maturity but wants bright seedlings). So `seedling_light` is represented as a
  default value + typed exceptions, not 65 identical "bright light" sentences.
- **GERMINATION light genuinely VARIES per crop and is the real information here.** Does the seed need
  light, dark, or neither to sprout. Our roster has real spread: lettuce/celery/chamomile/sweet-alyssum
  need light (surface-sown, "light aids germination" -- stated in our own prose); viola/calendula need
  dark ("light inhibits germination... covered to exclude light" -- also in our prose); the large
  covered-sown middle is neutral. It is NOT bulk-extractable (most crops are silent because they are
  neutral), so it takes a proper sourced classification pass.

**Why now:** register #6 was reopened 2026-07-07. The prior column passes (#4 timing spine, #5
watering, #7 climate) are complete on a stable 114 roster, so this is a clean column pass, not a
mid-certification bolt-on. Consumer: plant-app seedling-light guidance (avoiding leggy seedlings) +
germination guidance (surface-sow vs cover-to-exclude-light), both read gracefully (present-or-omitted).

---

## 1. The fields (crop-level, siblings of `germination_temp_f` / the register #7 climate fields)

| field | type | meaning | when absent / null |
|---|---|---|---|
| `germination_light` | enum, **or `null`** | does the SEED need light, dark, or neither to germinate -- the genuinely per-crop fact | **key absent = TODO** (uncertified shell, not yet reviewed); **`null` = reviewed, legitimately N/A** (crop with no realistic home-from-seed path -- see the N/A rule below) |
| `seedling_light` | enum | the light regime the SEEDLING wants -- a default plus typed exceptions | **key absent = TODO**; every certified crop gets a value (`na` is a real value, not absence) |
| `seedling_light_cap_hours` | int hours | the photoperiod ceiling, present **only** when `seedling_light == photoperiod_capped` | absent for every other `seedling_light` value (mirrors #7's number+enum pairing, e.g. `heat_threshold_f` with `heat_effect`) |

**Enums**
- `germination_light` in { `light_required`, `dark_preferring`, `neutral` }
  - `light_required` -- surface-sown / must not be buried; light aids or is needed for germination
    (lettuce, celery, chamomile, sweet-alyssum, lavender).
  - `dark_preferring` -- must be covered to exclude light; light inhibits germination (viola, calendula,
    plus large-seed dark germinators like nasturtium / sweet-pea).
  - `neutral` -- germinates fine covered at normal depth; light is irrelevant (the large covered-sown
    middle: tomatoes, peppers, brassicas, cucurbits, beans, corn, roots). This is a documented seed
    behavior, NOT a dumping ground -- every neutral call is adjudicated, not assumed.
- `seedling_light` in { `bright_default`, `photoperiod_capped`, `na`, `blackout_then_bright` }
  - `bright_default` -- the ~14-16 h bright regime; seed crops with an indoor tray-start seedling phase.
  - `photoperiod_capped` -- long-day bolt-sensitive seedlings capped at a shorter photoperiod; pairs
    with `seedling_light_cap_hours`. **RESERVED: zero live members in the current roster** (see the
    photoperiod note in section 2). Kept defined and gate-tested so it is ready the moment a crop needs
    it.
  - `na` -- no indoor seedling-under-lights phase: nursery-stock crops (vegetative propagule) + direct-
    sown-only seed crops (roots, beans, direct-sown herbs) that germinate outdoors.
  - `blackout_then_bright` -- the microgreen cycle (blackout -> ~16-18 h bright). The one group where
    seedling light IS the whole growing method; #6 treats microgreens as IN-scope (opposite of #7,
    where they were N/A-indoor).

**Coverage states (the honesty rule, per GS-arc section 3):**
- `germination_light`: `TODO` (key absent, uncertified shell) | `N/A` (`null`, no home-seed path) |
  `SET` (a real enum value).
- `seedling_light`: `TODO` (key absent) | `SET` (any of the four enum values, including `na`).

## 2. Semantics locked

- **`germination_light` N/A rule = "is this realistically home-seed-startable?", NOT "is
  `propagule == 'seed'`".** The `propagule` field keeps telling you the RECOMMENDED path;
  `germination_light` records the seed-germination fact IF you go from seed. The two coexist. This was
  Trevor's source-of-truth call: do not erase a real, sourceable seed behavior just because we
  recommend buying a transplant.
  - `propagule == 'seed'` (75 crops) -> `germination_light` **must be SET** (a real value). Gate-enforced.
  - `propagule != 'seed'` -> **SET** when the crop is a real home-from-seed option (the seed-startable
    herbaceous perennials: lavender, rosemary, thyme, sage, oregano, mint, chives, bee-balm, echinacea,
    + pawpaw), **or `null`** when there is no realistic home-seed path (grafted/named-cultivar fruit
    trees and brambles, citrus, blueberry, elderberry; vegetative-only vegetables garlic/potato/
    sweet-potato/strawberry/onion/shallot). An authored per-crop call; the coverage report shows both
    buckets so nothing is silently skipped.
- **`seedling_light` is a default + typed exceptions.** `bright_default` is the standard; the app shows
  the stocky-seedling guidance for it, the microgreen cycle for `blackout_then_bright`, nothing for
  `na`, and (future) the cap warning for `photoperiod_capped`. The value lets the app pick
  deterministically without reading prose.
- **Photoperiod note (why `photoperiod_capped` has zero live members):** spinach -- the textbook
  seedling-photoperiod case -- is DIRECT-SOWN in our data (`weeks_indoors` unset, `propagule == seed`),
  so its `seedling_light` is `na` and its bolt-risk is already carried by #7's `heat_effect: bolting`.
  The other long-day candidates do not qualify as capped seedlings either: leek bolts from cold
  vernalization (not seedling photoperiod), onion/shallot grow from sets (`na`), lettuce/cilantro bolt
  at maturity. So no current crop takes `photoperiod_capped`. The value + `seedling_light_cap_hours` are
  kept defined and proven by an injected synthetic crop in the gate's RED test.
- **Microgreens (8) are IN-scope for #6.** `germination_light = neutral` (the blackout is a stem-
  elongation technique, not a species light requirement) and `seedling_light = blackout_then_bright`.
  Their regime is already described in their `growth_stages` prose; the enum makes it structured.
- **Amend-not-recert.** Fields are appended to already-certified crops with the source in the
  contract + state-history, not a re-certification (same as the timing-spine + watering + climate fills).
- **Provenance follows the #7 pattern:** logged in this contract's pilot/rollout tables + STATE_HISTORY
  per-batch source-truth sample; no per-crop `_anchoring_urls` field (the germination_light exceptions
  are the sourced claims; the neutral middle is documented archetype seed behavior).

## 3. Decisions confirmed with Trevor (2026-07-07 brainstorm)

1. **Sourcing = full per-crop classification, grouped sourcing.** Every one of the 75 seed crops (+ the
   ~10 seed-startable non-seed crops) is individually adjudicated; the light/dark groups cite a shared
   T1 basis once per group, each borderline gets its own T1 page, and the neutral middle is confirmed as
   documented covered-sown behavior. Accuracy per-crop, effort by group. (Trevor: accuracy over cost.)
2. **Keep `photoperiod_capped` + `seedling_light_cap_hours`** even with zero live members, so it is
   ready as soon as a crop needs it; prove the machinery via a gate RED-test injection.
3. **Microgreens -> `blackout_then_bright`** (a distinct value, not `na`) -- option (a), most honest.
4. **`germination_light` N/A = no-home-seed-path**, not `propagule != seed` (decision above), so the
   ~10 seed-startable herbs carry real germination-light truth. `propagule` still records the
   recommended path.
5. **The full "how to start from seed" method** (seed-start depth/temp/timing prose) for the transplant-
   recommended herbs is OUT of #6 scope and tracked as a new register candidate for a future session.
   #6 completes the LIGHT dimension only.

## 4. Diverse pilot (7 crops -- exercises every enum value + both N/A cases)

| crop | `propagule` | `germination_light` | basis | `seedling_light` | basis |
|---|---|---|---|---|---|
| lettuce-leaf | seed | `light_required` | our prose "barely cover the seed"; classic light-germinator (T1) | `bright_default` | direct-sowable but commonly tray-started, has a seedling phase |
| viola | seed | `dark_preferring` | our prose "keep... dark until emergence... covered to exclude light" | `bright_default` | tray-started (`weeks_indoors` 8) |
| cherry-tomato | seed | `neutral` | covered-sown, light-indifferent (our stage prose: cover with vermiculite) | `bright_default` | tray-started; prose already says "grow stocky under strong light" |
| carrot | seed | `neutral` | covered ~0.25 in, light-indifferent root | `na` | direct-sown only (roots resent transplant) -- the direct-sown N/A case |
| lavender | transplant | `light_required` | seed-startable herb, surface-sown, needs light (T1) -- the seed-startable-non-seed case | `na` | nursery stock, no from-seed seedling phase -- the nursery N/A case |
| apple | bare_root | `null` (N/A) | grafted cultivar, no realistic home-from-seed path -- the germination N/A case | `na` | nursery stock |
| microgreens-mix | seed | `neutral` | species-neutral; blackout is technique not requirement | `blackout_then_bright` | the microgreen cycle -- the in-scope indoor case |

Coverage exercised: `light_required` x2, `dark_preferring` x1, `neutral` x3, germination `null`-N/A x1;
`bright_default` x3, `na` x3 (direct-sown, nursery x2), `blackout_then_bright` x1. `photoperiod_capped`
is exercised only by the gate RED test (no live crop). Every value sourced from the crop's own certified
prose where present, else a T1 page (lavender, viola dark-germination).

## 5. Gate (`tools/seedling_light_gate.py`, TDD RED->GREEN)

Per-crop shape/enum checks (fire only when a field is present -- unauthored roster stays green;
ABSENCE is a coverage TODO, never a shape violation):
- `germination_light` in the enum or `null`.
- **Cross-field coherence (present-only): a seed crop may not be `null`.** If `propagule == 'seed'` and
  `germination_light` is present, it must be a real value, never `null` -- a seed crop always germinates
  from seed, so the "no-home-seed-path" N/A is contradictory. (The stronger "a certified seed crop must
  CARRY germination_light, not omit it" is the DEFERRED register-coverage hard gate, register #8 -- NOT
  this shape gate, which must stay green mid-rollout.)
- `seedling_light` in the enum.
- `seedling_light_cap_hours` present **iff** `seedling_light == photoperiod_capped`; int in a plausible
  range (~8-14 h).
- A `--coverage` report: `germination_light` SET / N-A / TODO; `seedling_light` SET (broken out by value)
  / TODO; an `INDOOR_SLUGS`-style handling BUT with microgreens IN-scope for #6 (they must carry the two
  fields, unlike #7 where they were N/A-indoor).

Adversarially proven before trusted: inject into a SCRATCH copy -- a bad enum; a `propagule==seed` crop
with `germination_light` null/absent; an orphan `seedling_light_cap_hours` (no `photoperiod_capped`); a
`photoperiod_capped` crop MISSING `cap_hours`; a synthetic `photoperiod_capped` crop WITH a valid
`cap_hours` (proves the reserved value is accepted). All bad shapes bounce RED; the clean canonical is
GREEN.

## 6. C11 ruling (register_completeness_gate EXCLUDED_KEYS)

`germination_light` and `seedling_light` are controlled-vocab backend enums (siblings of
`start` / `propagule` / `heat_effect` / `frost_effect`), so they are ruled into
`register_completeness_gate.py` EXCLUDED_KEYS -- a C11 stop-and-ask, surfaced here for confirmation.
`seedling_light_cap_hours` is numeric and needs no ruling (the C11 check only inspects strings).
Regression-check: register_completeness still PASS after the ruling.

## 7. Rollout (held for gate + pilot sign-off)

Archetype-batched across the 114 certified, from each crop's own prose + grouped T1 sourcing,
SHA-guarded, gate-clean, count 124, COMPACT. Suggested batches:
- **Germination groups:** light_required (surface-sown small seed) | dark_preferring (light-inhibited) |
  neutral middle (covered-sown veg/large seed) | seed-startable herbs (the ~10 non-seed SET crops) |
  no-home-seed-path (`null`). Borderlines sourced individually: basil, dill, cilantro, borage, spinach,
  cosmos, parsley, leek, spring-onion.
- **Seedling values:** `bright_default` (tray-started seed crops) | `na` (direct-sown + all nursery
  stock) | `blackout_then_bright` (8 microgreens).
Then fold both fields into the per-crop GS-arc checklist (section 8) and publish the coverage report.
The 10 uncertified shells stay TODO (pick up the fields at certification).

## ROLLOUT (2026-07-07) -- germination_light + seedling_light across all 114 certified

Rolled out in a 7-crop pilot + a 107-crop pass (SHA-guarded, count 124, COMPACT), each field guarded
absent. Final coverage (of 114 certified; the 10 uncertified §E shells stay TODO):
- **germination_light**: SET 85 / N-A 29.
  - `light_required` (9): celery, chamomile, sweet-alyssum, lettuce-leaf (own prose + UC ANR); lavender,
    oregano, rosemary (Johnny's "light is required for germination"); echinacea (Johnny's "need light,
    surface or barely covered"); mint (established tiny-surface-seed light germinator).
  - `dark_preferring` (4): viola, calendula (own prose "light inhibits germination / covered to exclude
    light"); nasturtium, sweet-pea (Johnny's "darkness is required for germination").
  - `neutral` (72): the covered-sown middle (Solanaceae, cucurbits, brassicas, roots, legumes, most
    herbs, marigold/zinnia/cosmos/sunflower, microgreens, pawpaw). Each adjudicated, not assumed.
  - `null` = N-A (29): no realistic home-from-seed path -- grafted/named-cultivar trees + brambles,
    citrus, blueberry, elderberry, garlic/onion/shallot/potato/sweet-potato/strawberry, lemongrass.
- **seedling_light** (fully `weeks_indoors`-driven -- no per-crop guessing): `bright_default` (49, wi>0
  tray-started), `na` (57, wi in {0,None} direct-sown + all nursery stock), `blackout_then_bright` (8
  microgreens). `photoperiod_capped` 0 (reserved, gate-tested).

**Semantic calls made during the pass:**
- **`seedling_light` = `weeks_indoors`**: wi>0 -> the crop has an indoor tray-start seedling phase ->
  `bright_default`; wi in {0,None} -> the seedling stage happens outdoors (direct-sown) -> `na`. This is
  deterministic + gate-checkable, aligned to the app's indoor-start flow.
- **Lettuce corrected pilot->rollout: `bright_default` -> `na`** (Trevor-approved). Lettuce is wi=0
  (direct-sow in our data), same bucket as arugula/spinach/chard; its `germination_light: light_required`
  still stands (a direct-sown crop can still need light to germinate).
- **Seed-startable herbs SET despite non-seed propagule** (lavender/oregano/rosemary/mint/echinacea light;
  thyme/sage/chives/bee-balm neutral; pawpaw neutral): the refined N-A rule working -- record the real
  seed-germination fact, still recommend transplant via `propagule`.
- **Prose-verify-and-fill outcome: no fills needed.** All 8 seed-propagule light/dark exceptions already
  carry the actionable sowing instruction (light: surface-sow/light; dark: viola/calendula explicit,
  nasturtium/sweet-pea give the correct burial depth ½-1 in that achieves darkness). The herb exceptions'
  fuller seed-start prose stays in the deferred follow-on below.

**Gates:** seedling_light_gate PASS (0 violations; coverage as above); register_completeness PASS (C11
ruling holds); whole_crop_gate PASS across a broad archetype sample; release_verify no new violations
(the batch-collateral + broccoli-vs-tomato region-key concerns are expected/pre-existing, not #6).

## 8. Follow-ons
- Fold `germination_light` + `seedling_light` (+ `seedling_light_cap_hours` when it applies) into the
  per-crop GS-arc checklist so newly-certified crops get them natively.
- **Register-coverage HARD gate (Trevor 2026-07-07): decided to build, RETROACTIVE across #4-#7 + #6.**
  Today the register fields are guarded only softly -- each standalone gate validates shape WHEN PRESENT
  (unauthored roster stays green), and "fold into the checklist" is a process step -- so a new crop can
  certify while silently OMITTING them (the backfill-treadmill risk). Close it with a universal
  present-or-explicit-null cert gate modeled on `whole_crop_gate` A17 (npk_ratio) / A20 (display-
  readiness): every CERTIFIED crop (`verified_gs_arc`) must carry each shipped register field or its
  defined null/N-A, exempting the uncertified §E shells + the field's legit-N/A cases (the standalone
  gates' `INDOOR_SLUGS` / propagule-null rules). Turn on PER FIELD only after that field's rollout
  completes. **Scope decision: focus today on #6; if wiring the retroactive #4-#7 gate is too much after
  #6 lands, write a kickoff doc for a separate session instead of forcing it in.** Tracked in
  `docs/field_addition_register.md`.
- **New register candidate:** seed-start METHOD (depth/temp/timing prose) for the transplant-recommended
  herbs -- the fuller "here is how to grow it from seed" that #6's light-only scope leaves out.
- Optional: promote `photoperiod_capped` from reserved to live if a tray-started long-day bolt-sensitive
  crop enters the roster.
