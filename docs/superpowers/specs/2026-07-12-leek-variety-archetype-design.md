# Leek Variety Archetype -- Design Spec (the WINTER-HARDINESS / OVERWINTERING archetype)

- **Date:** 2026-07-12
- **Status:** design, pending Trevor review
- **Canonical at design time:** `e45bcf3c` (count 125, 116 certified)
- **Arc:** the fourth variety archetype, after dry-bean (`annual_dtm`), apple (`tree_fruit`), and onion
  (`photoperiod_annual`). Leek is the **hardiness / overwintering** archetype and the **exemplar** for a
  new, reusable cold/zone-viability honesty engine. Part of the broader remaining-archetypes program
  (mushrooms, artichoke, garlic, and others -- Trevor 2026-07-12); garlic and artichoke are the intended
  engine inheritors (designed separately, see 11).
- **Related specs:** `2026-07-12-onion-variety-pilot-design.md`, `2026-07-11-apple-variety-pilot-design.md`,
  `2026-07-11-dry-bean-variety-pilot-design.md`
- **Related memory:** `onion-variety-pilot-photoperiod`, `shallot-variety-dtm-held`,
  `trevor-north-star-accuracy-authority`, `variety-dtm-load-bearing-deferred`,
  `remaining-gs-anchors-roadmap`

---

## 1. Context and goal

Dry-bean proved the flat per-variety schema on the DTM-annual archetype; apple proved it on the
tree-fruit archetype (season-only, chill-gated); onion proved it on the photoperiod-annual archetype
(bulbing gated by day length). Onion was **schema enrichment** because its honesty engine (A9
`photoperiod_gate`) already existed. Leek is different: it is the **hardiness / overwintering**
archetype, and **its honesty engine does not exist yet** -- so this pilot is an **engine build**, not a
reuse.

Leek (*Allium ampeloprasum*, porrum group) is a cold-tolerant biennial grown as an annual for its
blanched shaft. Its varieties are bred and sold primarily on **winter-hardiness**: fast "summer" types
(King Richard) harvested before hard frost, versus very hardy "overwintering" types (Bandit, Giant
Musselburgh) bred to stand in frozen ground for late-fall-through-spring harvest. That hardiness axis
is a genuine, T1-sourceable, per-zone "will this work where you are?" signal -- the leek analog of
onion's day-length viability -- and almost no consumer source states it cleanly per zone.

Trevor's driver (north star `trevor-north-star-accuracy-authority`): stand up an honest, sourced,
per-zone overwintering-viability signal that makes plant a stronger authority, and build it as a
**reusable cold/zone engine** so the queued hardiness/vernalization crops (garlic, artichoke) inherit
it rather than each paying for a bespoke build.

## 2. The honest framing (the accuracy crux)

Leek differs from onion in a way that decides the whole model. A wrong-day-length onion **will not
bulb** -- a hard fail. But you can grow *some* leek in essentially any zone; a fast summer type is the
**standard, recommended** choice in the North. So cold-hardiness does **not** gate whether leeks grow.
It gates a narrower, real thing: **whether you can leave a hardy leek standing in the ground through
winter for a late-fall-through-spring harvest** (the overwintering payoff).

Therefore the engine asserts **"extended-season / overwintering viability by zone," NOT "grows or
fails."** The app claim reads like: *"you can grow leeks anywhere in season; in zone 6 and milder you
can also overwinter a hardy type like Bandit and harvest into spring; in zone 4, grow a summer type and
harvest by fall."* Applying onion's "won't work here" framing to leek would make plant **less**
accurate, not more.

**Honest hedging (built in, not bolted on):** the overwintering boundary is soft and modifiable --
mulch, reliable snow cover, and microclimate routinely buy a zone or more. The engine states
overwintering viability as a **hedged range**, never a hard zone cutoff (the discipline the tree chill
model already uses). There is a minor warm-end caveat (leeks are cool-season; very hot zones get a
"grow it in the cool season" note), but the load-bearing axis is unambiguously the cold end.

## 3. Governing principles (the contract -- inherited)

The variety contract carries over unchanged (dry-bean 3.1-3.4, apple, onion). Restated for leek:

### 3.1 Flat, sparse override-by-ABSENCE
A variety stores a value only where it differs from the crop default, else inherits by omission. A
load-bearing value is the actual value the app uses. No `delta` overlay.

### 3.2 Source-authoritative, T1-or-it-does-not-ship
A T1 source is the authority for a load-bearing value (`days_to_maturity`, `cold_hardiness_class`, and
the optional `min_temp_f`). T1 ships automatically; any non-T1 datapoint goes on a source manifest for
Trevor's sign-off before the splice. No silent drops/downgrades. **`min_temp_f` is T1-sourced-or-OMITTED
-- never fabricated to look precise (the shallot lesson, `shallot-variety-dtm-held`).** Leek hardiness
is the primary trait leeks are sold on, so a real T1 spine is expected (unlike shallot's dead-end DTM).

### 3.3 Common core + dispatched archetype block
The schema is a universal common core + one archetype block selected by the crop's `variety_archetype`
(absence defaults to `annual_dtm`; leek declares `hardiness_annual`). Section 5.

### 3.4 DTM-anchor inheritance
A variety's `days_to_maturity` inherits the crop `dtm_anchor` (`from_transplant` for leek), never
redefines it. `maturity_class` = DTM class (early/mid/late), kept DISTINCT from `cold_hardiness_class`
(the bloom-vs-ripen discipline from apple: leeks conflate timing and hardiness in casual description,
but they are genuinely different axes).

### 3.5 Soft-gate lifecycle (inherited invariants)
- **INV-1 (no open-ended soft):** the field-addition register row carries the explicit hard-flip
  trigger -- the hardiness-block + engine checks fold into the A39 register-coverage hard floor +
  `gate_all` when the Spec-2 rollout column pass reaches full-roster coverage.
- **INV-2 (validation precedes load-bearing consumption):** plant-astro must not consume leek variety
  `days_to_maturity` or the overwintering-viability signal as load-bearing until leek is gate-clean.

## 4. The crop-level `winter_hardiness` model (new, the `photoperiod`-object analog)

Leek gains a crop-level `winter_hardiness` object, mirroring onion's sourced `photoperiod` object:

- `explainer_beginner` / `explainer_seasoned` -- dual-register, T1-sourced prose explaining the
  summer-leek vs overwintering-leek concept, the zone dependence, and the mulch/microclimate hedge.
- `sources` / `anchoring_urls` -- T1 (Cornell, UMN, extension overwintering guides).

This object is the sourced footing the honesty engine and the app both rest on (never implicit
assumptions). The crop also declares the engine trigger: **`gating_factors` gains a `winter_hardiness`
token** (mirroring onion's `photoperiod` token that fires A9), so the new gate is a no-op off scope.

## 5. Per-variety schema (common core + `hardiness_annual` block)

### 5.1 Universal common core (unchanged)
`id` (slug), `name`, `maturity_class` (enum early|mid|late, the DTM class), `is_reference` (exactly one
true), `confidence_tier` (T1..T4), `note_beginner`, `note_seasoned`, `sources`, `anchoring_urls`.

### 5.2 The `hardiness_annual` archetype block (new)

| field | type | required | notes |
|---|---|---|---|
| `days_to_maturity` | int | yes | Load-bearing, absolute; inherits crop `dtm_anchor: from_transplant`. **Shared `_dtm_checks` machinery** (leek is a DTM archetype like dry-bean/onion; DTM genuinely differentiates leeks, ~75-150 d). T1-sourced. |
| `cold_hardiness_class` | enum `tender`\|`hardy`\|`very_hardy` | yes | Load-bearing overwintering-viability class. `tender` = not for overwintering (harvest by fall); `hardy` = overwinters in mild zones; `very_hardy` = stands hard winters. Kept DISTINCT from `maturity_class`. T1-sourced. |
| `min_temp_f` | int | no | Optional precision layer (option C): the lowest temperature a source states the variety reliably stands. **T1-sourced-or-OMITTED, never fabricated.** Int-shaped, in a plausible low-temp band that ALLOWS negatives for very hardy types (see 5.3) -- do NOT reuse the tree block's positive-int validator. |
| `use` | string | yes | Culinary / season use (e.g. "early fresh use", "overwintering"). Already present. |

`maturity_class` here = DTM class (early/mid/late). **No** bean traits, **No** tree block, **No**
`day_length_type`. This block **replaces leek's current per-variety `season` string** (e.g. "summer to
early fall"), which conflated maturity and hardiness; it splits cleanly into `maturity_class` (timing) +
`cold_hardiness_class` (hardiness) + the prose. All 6 varieties map without a gap.

### 5.3 `min_temp_f` sign note
Very hardy leeks tolerate sub-zero °F, so `min_temp_f` may be a NEGATIVE integer (e.g. -10). The gate's
shape check must accept negative ints within a plausible band (e.g. `[-40, 60]`), NOT reuse the
positive-int check the tree block applies to chill hours. This is called out so the gate refactor does
not blindly copy the tree positive-int validator.

## 6. The honesty engine + gates

### 6.1 The coupling
The engine reads the per-variety `cold_hardiness_class` (+ `min_temp_f` when present) against the
region's winter floor. **Region signal already exists, no new region data needed:** every region carries
`resolved_by_zone` keyed by USDA zone (3-11), and a USDA zone IS a minimum-temperature band by
definition (zone 5 = -20 to -10°F, zone 6 = -10 to 0, zone 7 = 0 to 10, ...); the top-level
`zone_frost_data` table + the tree `region_chill_delivered` precedent confirm the region->zone->climate
coupling pattern. The engine maps a region's zone(s) to a winter floor and produces the overwintering
claim:

- `tender` -> grown in season everywhere; overwintered nowhere (harvest by fall). No overwintering claim.
- `hardy` -> overwinters reliably in roughly zone 7+, hedged down a zone with mulch.
- `very_hardy` -> overwinters reliably in roughly zone 5-6+, hedged.
- Where a variety carries a sourced `min_temp_f`, the engine uses it directly against the zone floor
  (precision); otherwise the class->zone-floor mapping.

**The thresholds above are ILLUSTRATIVE** -- the real ones are T1-sourced at authoring and stated as
hedged ranges, never hard cutoffs. The class->zone-floor mapping is a small sourced constant table, not
per-region data.

### 6.2 Two invariants (adapted from onion, honest to leek biology)
- **Coverage (SOFTER than onion's).** Onion HARD-required a variety per resolved day-length class (a
  wrong onion will not grow). Leek's is narrower: a `tender` summer leek grows in EVERY zone, so no
  region is ever left without a viable leek -- the invariant is only that the recommended set **spans
  the hardiness classes the regions actually use**, so the app can always name an appropriate leek. Leek's
  6 span tender->very_hardy, so it holds. (A `tender`-only recommendation is always valid.)
- **Window-fit.** A `very_hardy` overwintering leek must carry a long-enough season to reach
  winter-standing size before hard cold (spring/summer plant -> next-winter/spring harvest); a `tender`
  type is a spring-plant, summer/fall harvest. The gate checks hardiness-class <-> planting/harvest-window
  coherence.

### 6.3 Two gate pieces
1. **`variety_detail_gate`: a one-line dispatch add (4th archetype).** Add `hardiness_annual`: required =
   common core + `cold_hardiness_class` + `use`; enum-validate `cold_hardiness_class` against
   {tender, hardy, very_hardy}; `min_temp_f` optional int in a plausible band (5.3); **reuse
   `_dtm_checks`** (add `hardiness_annual` to `DTM_ARCHETYPES`). Mechanically identical to how onion's
   `photoperiod_annual` was added. Does NOT contain any hardiness-vs-region logic (that is the new gate).
2. **`overwinter_hardiness_gate` (NEW -- the real build, the A9-analog).** Standalone, TDD, fires on the
   `winter_hardiness` gating token (no-op off scope). Enforces: `cold_hardiness_class` typing + `min_temp_f`
   shape/plausibility; the **coverage** invariant (6.2); the **window-fit** coherence (6.2); the region-zone
   coupling coherence. Adversarial RED proof on real leek shape before content is trusted (bad class enum,
   an overwintering type mis-window-fitted, an absurd `min_temp_f`, a coverage gap -- each bounces).
   Soft/standalone first; INV-1 hard-flip later.

### 6.4 Reuse, tempered (YAGNI)
The `overwinter_hardiness_gate` + the zone-coupling MACHINERY are built to be reused. But leek is a
**survives-cold (hardiness)** problem, while garlic and artichoke are **needs-cold (vernalization)**
problems -- related and zone-coupled, but OPPOSITE polarity. So this spec builds leek's engine cleanly
with the zone-coupling machinery structured for reuse, and does **NOT** pre-generalize the viability RULE
to vernalization. Garlic/artichoke's needs-cold rule is designed when those crops are reached (11).
Building the abstraction before the second real case is how you get the wrong abstraction.

### 6.5 Separation of concerns
`variety_detail_gate` validates the variety's SHAPE; the hardiness-vs-region HONESTY lives ONLY in
`overwinter_hardiness_gate`, never duplicated -- exactly the onion split (variety_detail vs A9).

## 7. `register_completeness` ruling
The new per-variety keys are strings/ints/enums: `cold_hardiness_class` (enum token -> EXCLUDED_KEYS,
like `day_length_type`), `min_temp_f` (int, non-string), `use` (already ruled), common-core keys
(already ruled). The crop-level `winter_hardiness` explainer keys are `_beginner`/`_seasoned`-suffixed
(auto-ruled). So **no new register ruling is expected** -- verify on the scratch battery (A25 = 0
unruled); add a ruling only if a key surfaces.

## 8. Sourcing (the shallot contrast)
Leek hardiness is genuinely sourceable -- it is the primary trait leeks are bred and sold on, covered by
Cornell, UMN, and extension overwintering guides plus seed-catalog hardiness statements. Expect a real T1
spine with some T2 (like onion, unlike shallot's dead end). The crop-level `winter_hardiness` model is
T1-sourced. Per-variety `sources`/`anchoring_urls` carry **T1 ONLY** (leek is certified; whole_crop_gate
E.source-tier fails any non-T1); a T2 hardiness datapoint's honesty lives in `confidence_tier` + prose +
the crop-level model, and `min_temp_f` is omitted rather than cited to a non-T1 source. All prose original
(17 USC 102(b)/Feist), leek voice, dual-register, no em dashes, American English, temps as `°F`.

## 9. Rollout (amend-not-recert)
Leek is already `verified_gs_arc` (certified). This is an amend, not a re-cert. Footprint = leek's
`varieties` + a new crop-level `variety_archetype: "hardiness_annual"` key + the new crop-level
`winter_hardiness` model object + the `gating_factors` `winter_hardiness` token + `verification_status.
source_set` (newly-cited T1 ids). All other crops byte-identical; count 125; COMPACT. The new gate is
tooling (no canonical touch). The 6 varieties map: King Richard (tender/early), Lancelot
(hardy/mid), Large American Flag (hardy/mid heirloom), Tadorna (hardy/mid-late), Bandit (very_hardy/late),
Giant Musselburgh (very_hardy/late heirloom); flagship (`is_reference`) = a reliable all-purpose type,
picked at authoring (Lancelot is the likely default -- the widely-adaptable fall leek).

## 10. Field-addition register entry
Add a row for the hardiness-variety bundle (`cold_hardiness_class` + optional `min_temp_f` as the
archetype's load-bearing fields, sharing `days_to_maturity` with the DTM archetypes) + the new
`overwinter_hardiness_gate` engine, with the explicit INV-1 hard-flip trigger. Note leek as the
hardiness-archetype exemplar and garlic/artichoke as the (separately-designed) engine inheritors.

## 11. Scope boundaries (explicitly OUT)
- **The garlic and artichoke vernalization (needs-cold) rule** -- opposite polarity to leek's
  survives-cold; the engine's zone-coupling machinery is built reusable, but that rule is designed when
  those crops are reached, NOT here.
- **The A9-style crop-level day-length model** -- N/A; leek does not bulb and carries no `day_length_type`.
- **The roster-wide variety rollout + folding in `varieties_detail[]` + roster-wide `variety_archetype`**
  -> Spec 2 (the column pass).
- **Flipping the hardiness checks into the A39 hard floor** -> Spec 2, post-rollout (INV-1).
- **plant-astro overwintering-viability consumption** -> the app handoff, INV-2 (no load-bearing
  consumption until gate-clean).

## 12. Success criteria
- Leek gains the crop-level `winter_hardiness` model (T1-sourced) + the `winter_hardiness` gating token;
  all 6 varieties carry the full section-5 schema, each `days_to_maturity` + `cold_hardiness_class`
  T1-anchored (or Trevor-signed-off), `min_temp_f` present only where T1-sourced, each with an honest
  `confidence_tier`.
- `variety_detail_gate` refactored to dispatch `hardiness_annual` (DTM machinery shared across the DTM
  archetypes; `cold_hardiness_class` enum validated; `min_temp_f` band-checked incl. negatives);
  dry-bean + apple + onion stay green.
- New `overwinter_hardiness_gate` enforces the class/figure shape + the softer coverage + window-fit,
  fires only on the `winter_hardiness` token, adversarial RED proof recorded, and is structured so the
  zone-coupling machinery is reusable (without pre-generalizing the vernalization rule).
- Canonical footprint = leek's `varieties` + `variety_archetype` + `winter_hardiness` model +
  `gating_factors` token + `source_set`; count 125; COMPACT; `gate_all` 116 certified unchanged;
  `release_verify` no new concerns.
- The contract (sections 3-6) is written so garlic/artichoke and the Spec-2 rollout inherit the
  zone-coupling + override + source-authoritative + archetype-dispatch rules without renegotiation.

## 13. Open items to confirm during authoring
- The T1 source id(s) for leek variety hardiness + DTM + the crop-level model (Cornell "Vegetable
  Varieties for Gardeners," UMN, Johnny's-class T2 only if needed -> manifest).
- The sourced class->zone-floor mapping (the hedged overwintering thresholds per hardiness class).
- Per-variety `cold_hardiness_class` + DTM (verify each against its T1 source; class must cohere with the
  overwintering habit; `min_temp_f` only where sourced).
- The flagship pick (likely Lancelot; confirm at authoring).
- Whether every variety reaches T1 or some land honestly at T2 (recorded in `confidence_tier`, never
  forced).
