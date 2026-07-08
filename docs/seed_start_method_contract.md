# Seed-start method / indoor-from-seed OFFER contract (register #11) -- v1 (COMPLETE)

**Status: COMPLETE 2026-07-08** (all 12 in-scope crops; canonical `00e0b6b1` -> `86ccf8c3`). Brainstormed +
scope-locked with Trevor; design spec `docs/superpowers/specs/2026-07-08-herb-seed-start-indoor-offer-design.md`,
plan `docs/superpowers/plans/2026-07-08-herb-seed-start-indoor-offer.md`. A CONTENT + enum-re-adjudication
arc over EXISTING register fields (#4 `weeks_indoors`, #6 `germination_light`/`seedling_light`/
`germination_temp_f`, #9 `tray_sowing`/`pot_up`), NOT a new cross-crop field and NOT a re-certification.

## The gap this closes

Register #6 gave the seed-startable non-seed crops a real `germination_light` (Trevor's source-of-truth
call: record the from-seed fact even when `propagule` recommends a transplant). But #6 keyed `seedling_light`
off the RECOMMENDED path (nursery stock -> `na`), and #9 keyed `tray_sowing` off `seedling_light`, so BOTH
cascaded to `na`. The data therefore ASSERTED an indoor-from-seed path (a set `germination_light`, a
`weeks_indoors`, prose describing an indoor start) while structurally WITHHOLDING the tools to walk it -- a
half-offer. Trevor (2026-07-08): "if we say these can be done indoors and we want to be a source of truth, I
want to be able to offer someone the ability to do it. Just because it's hard doesn't mean people don't want
to do it."

## The decision

**Extend the `germination_light` source-of-truth principle to the rest of the from-seed path.** `propagule`
+ the growth-stage timeline + the region calendar keep tracking the RECOMMENDED path (buy a transplant /
set / division). `start_method` + `seedling_light` + `tray_sowing` + `pot_up` + `weeks_indoors` carry the
fully-sourced ALTERNATIVE from-seed path. The app shows both: "Recommended: transplant" AND "Start from seed
indoors: [complete directions, begin ~N weeks before frost]." This RE-ADJUDICATES the #6/#9
`na`-for-nursery-stock calls for the genuinely seed-startable crops -- that rule was a rollout CONVENTION,
not a gate constraint (proven by scratch spike: no gate has a propagule dependency for `bright_default` /
a real `tray_sowing`, and none forbids `weeks_indoors` on a `perennial_woody_ornamental` crop).

**Scope = "directions" layer only.** Method prose + the crop-level fields, which let the app render the
sowing walkthrough + compute an indoor-start date from `weeks_indoors`. Explicitly DEFERRED (own kickoffs):
the growth-stage arc (a Germination -> Seedling stage prefix) and the per-region indoor-start calendar --
both re-open certified `growth_stages`/`regions` and are not needed to deliver the directions.

`sow_depth_inches` stays PROSE-only: `timing_spine_gate` requires it only for `SEED_LIKE={seed,clove,set,
tuber}` non-microgreens; `transplant`/`division` carry none, and it was left out for onion/shallot too
(the depth lives in prose).

## The 12 crops (final)

| crop | batch | germination_light | seedling_light | tray_sowing | pot_up | weeks_indoors | prose |
|---|---|---|---|---|---|---|---|
| chives | 1 | neutral (unchanged) | na->bright_default | na->**multisow_clump** | +not_needed | 6 (had) | multisow method authored (backs the enum) |
| mint | 1 | light_required (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | 6 (had) | "if you do start from seed" clause (surface-sow/light) |
| bee-balm | 1 | neutral (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | 8 (had) | none (already complete + coherent) |
| echinacea | 1 | light_required (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | 8 (had) | light instruction folded in (barely cover) |
| lavender | 2 | light_required (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | null->10 | "if you do start from seed" clause (stratify + surface-sow) |
| rosemary | 2 | light_required (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | null->10 | "if you do start from seed" clause (surface-sow/light) |
| oregano | 3 | light_required (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | null->8 | indoor-start timing added |
| sage | 3 | neutral (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | null->8 | none (already complete) |
| thyme | 3 | neutral (unch.) | na->bright_default | na->multi_sow_thin_to_one | +optional | null->10 | indoor path added (fine seed, barely cover) |
| pawpaw | 4 | neutral (unch.) | **na (kept)** | **na (kept)** | (none) | None (kept) | full stratification method + `germination_temp_f` []->[75,85] |
| onion | 5 | **null->neutral** | na->bright_default | na->multi_sow_thin_to_one | +optional | 10 (had) | none (already teaches from-seed) |
| shallot | 5 | **null->neutral** | na->bright_default | na->multi_sow_thin_to_one | +optional | 8 (had) | none (already teaches from-seed) |

**pawpaw is the honest exception.** A deciduous fruit tree with recalcitrant seed and a SHADE seedling, so
`bright_default` would misrepresent it and it is a deep-pot single seed, not a cell tray. It keeps
`seedling_light`/`tray_sowing` = `na` (which is TRUE for it) and carries the complete from-seed method in
PROSE + a real `germination_temp_f`. Not a withholding -- the directions are complete.

**lemongrass DEFERRED (correct null).** It shares the `na`-vs-`weeks_indoors` shape but is a genuine no-seed
crop (a grass grown from division / a rooted grocery stalk -- its prose teaches exactly that). `germination_
light = null` is CORRECT; `weeks_indoors = 8` is the division/stalk indoor-start, not a seed-start.

## Sourcing (provenance record; the #6/#9 model -- logged here + STATE_HISTORY, no per-crop field)

- chives -- RHS chives grow-your-own (module multisow: a few seeds per cell, transplant the clump).
- mint -- Johnny's mint key growing info (surface-sow, do not cover, needs light, 6-8 wk before set-out);
  off-type already in mint's own certified prose (Clemson).
- echinacea -- register #6's Johnny's basis ("need light, surface or barely covered"), surfaced in the
  existing stratify + 65-70 F method.
- lavender -- extension/RHS consensus: cold-moist stratify 3-6 wk near 35-41 F, surface-sow (needs light),
  ~70 F, slow (2-4+ wk, 100-200 d to plantable); `weeks_indoors=10` (8-12 wk range).
- rosemary -- Johnny's rosemary key growing info ("start in flats 10-12 weeks before last frost", light
  required, slow/erratic); `weeks_indoors=10`.
- oregano -- extension consensus (6-10 wk indoors); "needs light, do not cover" already authored;
  `weeks_indoors=8`.
- sage -- its own certified prose ("indoors 8-10 wk before frost"); `weeks_indoors=8`, no prose change.
- thyme -- extension consensus (8-10 wk, slow fine seed, barely cover); `weeks_indoors=10`.
- pawpaw -- Kentucky State University pawpaw program: recalcitrant seed (never dry), 70-100 d cold-moist
  stratification near 40 F, sow 1 in deep at 75-85 F, taproot first / shoot ~9 wk, tall tree pot / root
  trainer. `germination_temp_f=[75,85]`.
- onion / shallot -- their own certified prose already teaches from-seed; `germination_light=neutral`
  (covered-sown, light-indifferent allium seed). No prose change.

Original prose, never copied (facts/methods not copyrightable -- 17 U.S.C. 102(b)/Feist; same model as
register #10). Inline cite style = institutions only: chives carries "(RHS)"; Johnny's/extension provenance
is logged here, not inline.

## Gate coherence (VERIFIED -- no new gate, no gate change)

Scratch spikes before authoring + the full battery on every batch: `seed_tray_gate`'s only coherence rule
is `real tray value <-> seedling_light == bright_default` (NO propagule dependency); `seedling_light_gate`
has no propagule rule for `bright_default`, and its only null rule fires on `propagule == 'seed'` (so onion/
shallot's `set` propagule allows null->neutral); `timing_spine_gate` does not validate `weeks_indoors` and
requires `sow_depth_inches` only for `SEED_LIKE`; `woody_ornamental_gate` (A13) checks nothing about these
fields; `register_coverage_gate` (A39) requires only the register KEYS present. Every batch: `whole_crop_gate`
on changed + `seed_tray_gate` + `seedling_light_gate` + `timing_spine_gate` + `register_coverage_gate` +
`register_completeness_gate` + `gate_all` (114/114) + `release_verify` (no new violations, no dash/degrees).

## Coverage delta

- `germination_light`: SET 85 -> **87**, N-A 29 -> **27** (onion/shallot null->neutral). TODO 10 (§E shells).
- `seedling_light`: bright_default 49 -> **60**, na 57 -> **46** (11 crops flipped; pawpaw stays na).
- `tray_sowing`: multi_sow_thin_to_one -> **42**, single_sow 16, **multisow_clump 2** (spring-onion + chives),
  na -> **54**.

## Follow-ons

- **onion `germination_light`** was `null` because #6 keyed the N-A off `propagule`; onion/shallot are now
  corrected. Any other vegetative-propagule crop whose prose teaches a real from-seed path should get the
  same look (none remain among the certified 12-in-scope set; lemongrass is genuinely no-seed).
- **Growth-stage arc (deferred):** a Germination -> Seedling stage prefix so the app's stage TRACKER walks
  the indoor phase (re-opens certified `growth_stages`). Own kickoff if the app needs it.
- **Per-region indoor-start calendar (deferred):** `regions.plantings` indoor-start rows for the
  `perennial_woody_ornamental` crops. Own kickoff; avoid unless the recommended calendar is being reworked.
