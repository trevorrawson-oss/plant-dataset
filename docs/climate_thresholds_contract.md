# Climate-thresholds field contract (register #7) — v0 (Phase 1)

**Status:** contract + TDD gate + diverse pilot done; **the semantic decisions below are Trevor's to
confirm before the full-roster rollout.** Follows the column-GS-arc method
(`docs/gs_cross_crop_field_addition_v0.md`): lock the field spec, prove it on a diverse pilot
(including the legitimately-N/A case), gate it, then roll out with a coverage report.

**Why now:** the notifications + WeatherKit build starts ~week of 2026-07-14. A cheap DETERMINISTIC
weather trigger (`forecast_high > heat_threshold_f -> alert`, `forecast_low < frost_tolerance_f ->
alert`) needs these numbers STRUCTURED; today they live only as prose an LLM must read. See memory
`notifications-ai-architecture`. NOTE: the dataset already carries partial notification scaffolding
(`hard_freeze` / `FROST_PROTECT` / "Hard freeze ahead" tip tokens on e.g. broccoli) — these fields
give those triggers their firing numbers.

---

## 1. The fields (crop-level, siblings of the existing `germination_temp_f`)

| field | type | meaning | when absent |
|---|---|---|---|
| `heat_threshold_f` | int °F, **or `null`** | forecast daily **HIGH** at/above which the crop hits its primary heat stress (the "it's too hot, act or expect quality loss" number) | **key absent = TODO** (not yet reviewed); **`null` = reviewed, legitimately N/A** (heat-loving crop with no actionable ceiling) |
| `heat_effect` | enum | WHAT the heat does, so the deterministic alert message is accurate without an LLM | present iff `heat_threshold_f` key is present (int → a stress effect; `null` → `heat_tolerant`) |
| `frost_tolerance_f` | int °F | the temperature at/below which the crop takes cold/frost **damage** — the "protect or harvest" number | **key absent = TODO**; near-universal (every crop has some freeze-damage point) |
| `frost_effect` | enum | whether that damage KILLS the plant or damages foliage/fruit on a plant that survives | present iff `frost_tolerance_f` present |

**Enums**
- `heat_effect` ∈ { `bolting`, `poor_fruit_set`, `crown_failure`, `quality_loss`, `heat_tolerant` }
  - `heat_tolerant` is the N/A marker: it pairs with `heat_threshold_f: null` (heat-lover, no ceiling).
- `frost_effect` ∈ { `killed`, `foliage_damaged` }
  - `killed` = frost-tender, the plant dies (tomato, okra, basil). `foliage_damaged` = hardy/perennial,
    leaves/heads/fruit damaged below the number but the plant survives (kale, broccoli heads, citrus).

**Coverage states (the honesty rule, per GS-arc §3):**
- heat: `TODO` (key absent) · `N/A` (`null` + `heat_tolerant`) · `SET` (int + a stress effect)
- frost: `TODO` (key absent) · `SET` (int + effect)

## 2. Semantics locked

- **Single value each, not a band.** `germination_temp_f` is a band because it is an *optimal range*;
  these are *crossing points* (a threshold), so a single int is correct — and deliberately different
  from the germ field.
- **`heat_threshold_f` is a daytime-HIGH trigger.** Night-temperature effects (tomato/pepper poor set
  on warm nights >75°F or cold nights <55-60°F) are **out of scope for v1** — a possible `*_night_f`
  companion later. One number, one deterministic daytime rule.
- **Coherence invariant (gated):** when both are present, `frost_tolerance_f < heat_threshold_f`.
  (Deliberately NOT `heat_threshold_f > germination_temp_f[1]` — kale germinates to ~85°F but its
  quality/bolt threshold is ~82°F; germination heat and mature-plant heat stress are different
  phenomena.)
- **Amend-not-recert.** Fields are appended to already-certified crops with the source in the
  state-history + contract, not a re-certification (same as the timing-spine + watering fills).

## 3. Decisions flagged for Trevor (confirm before rollout)

1. **Keep the two `*_effect` enums, or go pure-numeric?** The register named only the two numeric
   fields. I added `heat_effect` / `frost_effect` because the register's own example — broccoli's
   86°F is *crown failure* while a tomato's 92°F is *blossom drop* — shows the bare number can't write
   an accurate alert on its own. **Recommend: keep them** (they are what make the deterministic message
   correct, which is the whole point of #7). Dropping a field later is trivial; adding is the work.
2. **Add a third field `chilling_sensitivity_f` (#7b)?** Non-freezing *chilling injury* is a real,
   separate, actionable trigger for warm crops: basil damages below ~50°F, okra/cucumber ~45°F,
   pepper ~40°F — all ABOVE freezing, so `frost_tolerance_f` (a freeze number) misses it. Folding it
   into `frost_tolerance_f` would be inaccurate (basil is not "frost-tolerant to 50°F"). **Recommend:
   yes, as a fast follow-on** on the same arc; the chilling numbers are already in-prose (I logged them
   per pilot crop). Left OUT of v1 to keep this pass to the two register-named fields.
3. **The C11 ruling.** `heat_effect` / `frost_effect` are controlled-vocab backend enums (siblings of
   `start` / `propagule` / `dtm_anchor`), so Phase 1 rules them into
   `register_completeness_gate.py` EXCLUDED_KEYS — a C11 stop-and-ask, surfaced here for confirmation
   (the numeric `heat_threshold_f`/`frost_tolerance_f` need no ruling; the C11 check only inspects
   strings). Regression-checked: register_completeness still PASS.

## 4. Diverse pilot (6 crops, every number sourced from the crop's own certified prose)

| crop | germ band | `heat_threshold_f` / effect | source (prose) | `frost_tolerance_f` / effect | source (prose) |
|---|---|---|---|---|---|
| broccoli | [40,86] | **86** / `crown_failure` | ">=86°F day stalls heading, stops a usable crown" | **28** / `foliage_damaged` | "takes light frost in stride… a hard freeze damages exposed heads" |
| cherry-tomato | [70,85] | **92** / `poor_fruit_set` | "too hot (over 90°F) to set fruit; flowers drop above 95°F" | **32** / `killed` | "a single frost event usually kills the plant outright" |
| kale | [45,85] | **82** / `quality_loss` | "sustained heat above ~80-85°F makes leaves tough and bitter" | **20** / `foliage_damaged` | "a deep freeze below ~20°F may damage exposed leaves" (very hardy) |
| okra | [70,95] | **null** / `heat_tolerant` | tropical heat-lover; no actionable upper trigger | **32** / `killed` | "no cold tolerance: even a light frost kills it" |
| basil | [70,85] | **null** / `heat_tolerant` | heat managed with shade cloth, no ceiling | **32** / `killed` | "blackens and dies at or below 32°F" (chilling <50°F → #7b) |
| lemon | [] | **null** / `heat_tolerant` | evergreen citrus, heat-tolerant with irrigation | **28** / `foliage_damaged` | "high-20s°F… leaves and fruit are damaged" — cover the tree |

The pilot exercises: heat `SET` with three distinct effects (crown/set/quality), heat `N/A` ×3 (okra,
basil, lemon — the honesty case), frost `killed` (tender) vs `foliage_damaged` (hardy + perennial),
and a `[]`-germ perennial. Chilling numbers logged for #7b: basil 50, okra 45, cherry-tomato 50.

## 5. Gate (`tools/climate_threshold_gate.py`, TDD RED→GREEN)

Per-crop shape/range/enum checks + the `frost < heat` coherence invariant + a coverage report
(`SET` / `N/A` / `TODO` for heat; `SET` / `TODO` for frost). Adversarially proven: a defect injected
into a scratch copy (frost ≥ heat; a bad enum; an orphan `heat_effect` with no threshold; a
non-integer) bounces RED; the clean canonical is GREEN.

## 6. Rollout (held for Trevor's sign-off on §3)

Author the two fields across the remaining ~108 certified crops from each crop's own prose, batched by
archetype, SHA-guarded, gate-clean — then fold into the per-crop checklist (GS-arc §5) and publish the
coverage report. Heat-lovers (okra, sweet corn, melons, sweet potato, eggplant, edamame, the warm
flowers) take `heat_tolerant`/`null`; cool-season crops and pollen-limited fruiters take a threshold.
