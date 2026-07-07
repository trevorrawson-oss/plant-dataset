# Climate-thresholds field contract (register #7) — v1 (rollout complete)

**Status:** **ROLLOUT COMPLETE 2026-07-07** — all 106 outdoor certified crops carry the three fields
(the 8 microgreens are N/A-indoor; the 10 uncertified §E shells are out of scope). Trevor confirmed
decision #1 (keep the `*_effect` enums) and #2 (add `chilling_sensitivity_f`); see the ROLLOUT section
at the bottom for the semantic calls made during the pass. Follows the column-GS-arc method
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

---

## ROLLOUT (2026-07-07) — all three fields across 106 outdoor certified crops

Trevor: keep the effect enums (yes), add `chilling_sensitivity_f` (yes). Rolled out in 6 archetype
batches (warm-fruiting 30, cool-season 25, herbs 12, flowers 13, woody perennials 24, + pilot-chill 2),
each SHA-guarded and gate-clean. Coverage now: heat SET 46 / N-A 60, frost SET 106, chilling SET 29 /
N-A 77; the only TODO is the 10 uncertified shells.

**`chilling_sensitivity_f`** — added as decided. Numeric-only (no effect enum; chilling damage is
uniform). `null` = reviewed-N/A (cold-adapted crop). SET only for the classic chilling-sensitive
GROWING plants (Solanaceae ~45-50, cucurbits 41-50, okra 45, sweet-potato 50, basil 50, lemongrass 40);
cold-tolerant legumes (beans/edamame) and all cool-season/hardy/perennial crops are N/A.

**Semantic calls made during rollout (documented so the notification engine reads them right):**
- **Fruit-tree `frost_tolerance_f` = the spring blossom/bud frost point (~28°F, `foliage_damaged`)**,
  NOT winter wood hardiness. Rationale: that is the actionable in-season weather alert ("cover the
  bloom / expect blossom loss"); winter wood hardiness is a zone/site concern the crop's zone data
  already covers, and a dormant tree ignores a 28°F night. Tender subtropical trees are the exception
  and use their wood hardiness (fig 18, pomegranate 12) since that IS their actionable freeze alert.
  The `frost_effect` enum disambiguates: `killed` (annual dies) vs `foliage_damaged` (perennial
  blossoms/leaves damaged, plant survives) — this is the second place the effect enum earns its keep.
- **"Chill hours" ≠ chilling injury.** The "hours below 45°F" prose on apples/pears/berries/etc. is a
  dormancy *requirement* (the tree NEEDS that cold), not damage — so those crops get `chilling` N/A,
  never a `chilling_sensitivity_f` value.
- **Storage vs growing-plant chilling.** Much cucurbit/tomato "chilling below 50°F" prose is
  post-harvest storage advice; `chilling_sensitivity_f` is the GROWING-plant threshold (same
  physiology, close numbers), and the frost field handles the freeze-kill case separately.
- **Microgreens (8) = N/A-indoor.** Indoor tray crops with no outdoor weather exposure, so all three
  fields are legitimately N/A (same class as the uncertified mushrooms). The gate's `INDOOR_SLUGS`
  set reports them as N/A-indoor rather than TODO; the fields are left absent (not contorting the
  enum semantics).
- **Very-hardy crops without a crop-specific in-prose number** (overwintering alliums, hardy herbs,
  deciduous-tree winter hardiness) use their established USDA-zone hardiness — standard horticulture,
  noted as archetype-sourced, not invented precision.

## Follow-ons
- Fold the three fields into the per-crop GS-arc checklist (GS-arc §5) so newly-certified crops get
  them natively. The 10 uncertified §E shells pick them up at certification.
- Optional `*_night_f` companion for the night-temperature effects deferred from v1 (tomato/pepper
  warm-night poor set, cold-night <55°F pollen failure).
