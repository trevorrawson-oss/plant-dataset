# PLA-8 Round 1 -- variety-level ladder mechanism + the container ruling

**Date:** 2026-08-22
**Canonical measured:** `20a32c47f0bf861e5b93fad71b9af3bbb37643afdb70dccd758e1ee0eb080ea9` (matches `LATEST.txt`; HEAD `8cbfb5c`, tree clean)
**Scope:** reconnaissance + mechanism design. No ladder content authored, no canonical byte changed.

Every number below was measured against `20a32c47` in this session. Where a figure on the issue
disagrees, both are given and the mechanism of the disagreement is named.

---

## 0. The 2026-08-04 header numbers: ALL THREE CONFIRMED

| claim | measured | verdict |
| -- | -- | -- |
| 37 `control_methods` entries | 37 | EXACT |
| 52 of 913 problem objects carry `control_ladder` | 52 of 913 | EXACT |
| across 7 crops | 7 | EXACT |

The header predates several promotes but has not drifted. 192 rungs total.

---

## 1. Item 1 -- apple and strawberry both carry crop-level ladders. NO prerequisite gap.

Both pilot crops are laddered to 100% coverage:

| crop | problems | laddered | rungs |
| -- | -- | -- | -- |
| apple | 8 | **8 / 8** | 35 |
| strawberry | 12 | **12 / 12** | 44 |

The 7 laddered crops are `apple`, `artichoke`, `asparagus`, `broccoli`, `celery`,
`microgreens-mix`, `strawberry`. Every one is laddered on 100% of its problems -- ladder coverage is
all-or-nothing per crop, never partial.

### The two pilot crops are the two most complete ladders on the roster

| crop | problems | rungs | rungs missing `note_seasoned` | problems missing `sources` | ladder-only stubs |
| -- | -- | -- | -- | -- | -- |
| **apple** | 8 | 35 | **0** | **0** | 0 |
| **strawberry** | 12 | 44 | **0** | 12 | 0 |
| broccoli | 7 | 30 | 19 | 0 | 0 |
| celery | 7 | 25 | 18 | 0 | 0 |
| artichoke | 11 | 31 | 9 | 11 | **11** |
| asparagus | 5 | 20 | 7 | 5 | **5** |
| microgreens-mix | 2 | 7 | 1 | 0 | 0 |

Apple is the exemplar: complete register pairs, complete sourcing. Round 2 picked the right crops.

**Two roster-wide observations, neither blocking:**
- **54 of 192 rungs (28%) carry no `note_seasoned`.** The gate permits this. It is concentrated in
  broccoli (19) and celery (18), not in the pilot crops.
- **16 of 52 laddered problems are ladder-only stubs** carrying nothing but
  `{id, name, type, control_ladder}` -- no symptoms, no cause, no prevention, no sources. All 16 are
  on artichoke (11) and asparagus (5). 28 of 52 laddered problems carry no `sources` at all; the
  sourcing backstop for those is the `control_methods` catalog entry, which is T1-gated.

---

## 2. Item 3 -- the actual `varieties.recommended[]` lists

### apple: 16 varieties, all carry `id` and `resistance`

| id | name | resistance |
| -- | -- | -- |
| `dorsett-golden` | Dorsett Golden | scab: susceptible |
| `anna` | Anna | scab: susceptible |
| `ein-shemer` | Ein Shemer | scab: susceptible |
| `zestar` | Zestar! | scab/blight/rust: susceptible; mildew: resistant |
| `mcintosh` | McIntosh | scab/blight: susceptible; rust: resistant; mildew: tolerant |
| `liberty` | Liberty | **scab: immune**; blight: tolerant; rust + mildew: resistant |
| `empire` | Empire | scab/mildew: susceptible; blight: tolerant; rust: resistant |
| `honeycrisp` | Honeycrisp | scab/blight: tolerant; rust/mildew: susceptible |
| `gala` | Gala | scab/blight: susceptible |
| `golden-delicious` | Golden Delicious | all four: susceptible |
| `jonagold` | Jonagold | scab/blight/mildew: susceptible; rust: resistant |
| `mutsu` | Mutsu | all four: susceptible |
| `fuji` | Fuji | scab/blight: susceptible; mildew: resistant |
| `granny-smith` | Granny Smith | scab/blight/mildew: susceptible; rust: resistant |
| `pink-lady` | Pink Lady | scab/blight: susceptible; rust/mildew: resistant |
| `dolgo` | Dolgo | scab/mildew: resistant; rust: tolerant |

### strawberry: 9 varieties, all carry `id`; 6 of 9 carry `resistance`

| id | name | habit | resistance |
| -- | -- | -- | -- |
| `honeoye` | Honeoye | june_bearing | red-stele + verticillium: susceptible |
| `earliglow` | Earliglow | june_bearing | red-stele + verticillium: **resistant** |
| `jewel` | Jewel | june_bearing | red-stele + verticillium: susceptible |
| `allstar` | Allstar | june_bearing | red-stele + verticillium: **resistant** |
| `albion` | Albion | day_neutral | anthracnose: susceptible |
| `seascape` | Seascape | day_neutral | *(none)* |
| `tristar` | Tristar | day_neutral | red-stele + verticillium: **resistant** |
| `ozark-beauty` | Ozark Beauty | everbearing | *(none)* |
| `quinault` | Quinault | everbearing | *(none)* |

---

## 3. Item 4 -- variety-level pest/disease differentiation that ALREADY EXISTS

It exists in three layers, and the structured layer is 20x narrower than the prose layer.

### 3a. Structured: `varieties[].resistance{}` -- 24 varieties, 3 crops, 67 assertions

Keyed on the parent problem's `id`. Values: `susceptible` (39), `resistant` (18), `tolerant` (9),
`immune` (1 -- apple/Liberty on apple-scab).

| crop | varieties with resistance | keys used |
| -- | -- | -- |
| apple | 16 / 16 | apple-scab, cedar-apple-rust, fire-blight, powdery-mildew |
| strawberry | 6 / 9 | anthracnose, red-stele, verticillium-wilt |
| asparagus | 2 / 4 | asparagus-rust, fusarium-crown-rot, purple-spot |

Gated by `tools/variety_resistance_gate.py`, which returns **0 violations**. All 67 keys resolve
against the parent's problem `id`. **This is the join that works, and it is the same key the ladder
hangs off.**

> Note for anyone re-deriving this: a scan that slugifies `pests[].name` instead of reading
> `pests[].id` reports 5 false "no join" failures (`anthracnose` vs `anthracnose-fruit-rot`,
> `red-stele` vs `red-stele-phytophthora-root-rot`, and asparagus's three). The ids are real and
> exact. The gate is correct; the naive join is not.

### 3b. Informal prose: 147 fields across 62 crops

Variety `note` / `note_beginner` / `note_seasoned` / `recommended_note` / `disease_notes` carrying
resistance, susceptibility or pest language. A representative slice:

- **strawberry/Honeoye** (`note_seasoned`): "it carries little disease resistance, so keep it off
  poorly drained sites where red stele and verticillium take hold" -- prose that says exactly what
  the structured `resistance` map says, on the same variety.
- **asparagus/Millennium** (`note_beginner`): "it catches rust more easily than the older Jersey
  hybrids" -- a genuine variety-level differential.
- **pear-european** (10 fields): fire-blight resistance across Hood, Kieffer, Orient -- a crop with
  **no ladder and no problem ids**, so none of it is addressable today.
- **bee-balm, basil, roma-tomato**: resistance claims trapped inside variety **strings**, not objects.

### 3c. The one redundant field: `varieties[].disease_notes`

Exactly one instance roster-wide -- apple/Liberty: *"Immune to apple scab; a strong low-spray
choice."* This restates that variety's own `resistance: {"apple-scab": "immune"}` in prose. It is a
second source of truth for one claim, on one record. Recommend folding into Layer 1 (below) and
retiring the field rather than growing it.

### 3d. 133 variety entries are still bare STRINGS, on 20 crops

`cherry-tomato`, `beefsteak-tomato`, `roma-tomato`, `basil`, `heirloom-tomato`, `grape-tomato`,
`lettuce-leaf`, `tomatillo`, `marigold`, `nasturtium`, `sunflower`, `borage`, `calendula`, `zinnia`,
`cosmos`, `sweet-alyssum`, `echinacea`, `bee-balm`, `viola`, `sweet-pea`.

A string cannot carry an `id`, a `resistance` map, or a delta. Any variety-level mechanism is
structurally unavailable on these 20 crops until they are converted. This does **not** block the
pilot: apple and strawberry are 16/16 and 9/9 objects with ids.

---

## 4. No consumer reads any variety-level pest field YET -- a contract requirement, NOT a blocker

Verified by reading both consumer repos, not inferred:

| field | records | consumer that reads it |
| -- | -- | -- |
| `varieties[].resistance` | 24 varieties / 67 assertions | **NONE** |
| `varieties[].delta` (the A4b shape) | 54 varieties / 133 entries | **NONE** |
| `varieties[].disease_notes` | 1 | **NONE** |

- `plant-astro/src/components/guides/RecommendedVarietiesCard.astro` reads exactly three fields:
  `v.name`, `v.portrait`, `v.descriptor`.
- `resistance`, `disease_notes` and `delta` appear **nowhere** in `plant-astro/src/components` or
  `plant-astro/src/lib`.
- `plant-app/src/lib/varieties.ts` reads `slug, name, id, use, seed_type, recommended_note,
  primary_use, note_*, note, maturity_class, is_reference, hero_description, days_to_maturity,
  confidence_tier, chill_hours_required, bloom_group, bloom_duration_days, triploid` -- and **not**
  `resistance`, `disease_notes` or `delta`. (The `resistance` hits in plant-app are
  `pesticide_safety_education.resistance_note_*`, pesticide-resistance management -- a different
  subject.)

**The crop-level ladder, by contrast, IS live in both**: `plant-astro`'s `PestsDiseasesCard.astro`
renders "The control ladder" for migrated entries, and `plant-app`'s `guide-chapters.ts` builds
`ladder: ladderRungs(level, e.control_ladder)`.

**This does NOT block Round 2, and an earlier draft of this document wrongly said it did.** The
dataset is the source of truth and the consumers follow it via a submodule bump; a variety-level
pest surface that does not render yet because it has not been built yet is ordinary sequencing, not
a defect. The variety render is queued work (PLA-12, which this arc blocks).

**The real lesson from `year_one_notes_*` is narrower than "ship frontend first."** That defect was
not caused by the dataset leading the renderer. It was caused by a renderer eventually being built
against an **unspecified contract** -- so plant-app pointed two establishment pills at one dataset
string and sheared the third out of `harvest_ready_*`, and 36 of 38 perennials went byte-identical
without anyone noticing. The hazard is an unwritten field contract, not an unbuilt component.

**So the obligation this creates is on THIS repo, discharged in section 5f: write the render contract
down now**, so the eventual consumer has a spec to build against instead of guessing. One field per
rendered unit, stated explicitly, is what PLA-6 had to retrofit at the cost of an arc.

Worth knowing regardless: rendering the existing `resistance` map needs **zero** new dataset content
-- 67 assertions are already authored, sourced and gated -- so it is the cheapest possible first
proof of the variety tier whenever that work is picked up.

---

## 5. Item 2 -- the delta-overlay mechanism

### 5a. A4b's principle CONFIRMED, its triple REJECTED for ladders

`{value, parent, changed}` is real and shipped: **54 variety records across 10 crops** (`lemon`,
`lime`, `orange-navel`, `mandarin-clementine`, `grapefruit`, `thyme`, `rosemary`, `oregano`, `sage`,
`lavender`), 133 delta entries. It is internally consistent -- `changed` disagrees with
`value == parent` in **0 of 133** entries. 25 entries are deliberate labelled no-change rows.

But every value in it is a **display string** (`"1,000 hrs"`, `"varies"`), and the triple describes
a **scalar**. A control ladder is an ordered list of structured rungs. `{value, parent, changed}`
cannot express "drop rung 3", "replace rung 1's note", or "insert a rung after garden_sanitation".

**So: keep A4b's architecture (the crop is the entity; a variety carries only what differs), and use
a list-aware delta rather than reusing its triple.**

### 5b. Layer 1 -- DERIVED. `resistance{}` already IS the delta for the dominant case.

`varieties[].resistance` is keyed on the same problem `id` the ladder hangs off. For apple that is a
complete 16-variety x 4-disease matrix, already T1-sourced and already gated. The variety's ladder
can therefore be **computed**, not authored:

> **⚠ CORRECTED 2026-08-22 (same day), by measuring against the actual ladders.** The first version
> of this table said `susceptible` produces "no delta at all" and framed every delta as dropping an
> escalation rung. **Both were wrong, and they missed the two largest and most valuable delta
> classes.** The measurement that caught it: `resistant_varieties` is **rung 0 of 9 of the 20
> laddered problems** across apple and strawberry, and its note literally instructs the reader to
> *choose a resistant variety* -- advice aimed at someone who has, by the time they are reading a
> variety page, already chosen. Under the old table strawberry produced **0** deltas (both diseases
> its varieties are graded on, red-stele and verticillium-wilt, have no escalation rung to drop);
> under the corrected table it produces 11 and the pilot is symmetric again.

| grade | ladder transform |
| -- | -- |
| any non-susceptible, where rung 0 is `resistant_varieties` | **R0-SATISFIED** -- the reader has already completed this rung by choosing this variety. Restate it as done, naming the variety. |
| `susceptible`, where rung 0 is `resistant_varieties` | **R0-INVERTED** -- rung 0 is now useless-to-harmful advice ("choose a resistant variety" to someone holding a susceptible one). Restate it as a load-bearing warning: this variety is not resistant, so the steps below are doing the work. |
| `immune` / `resistant` | additionally **DROP** the `soft_chemical` and `conventional` rungs |
| `tolerant` | additionally **SOFTEN** the escalation language, keep the rungs |
| `susceptible`, no `resistant_varieties` rung | parent ladder unchanged, no delta |

**Measured surface across the two pilot crops: 62 variety x problem graded pairs, and ALL 62
produce a delta** -- 37 R0-INVERTED, 25 R0-SATISFIED, 13 DROP, 6 SOFTEN (classes overlap; a pair can
be both R0-SATISFIED and DROP). Split apple 51 / strawberry 11.

**⚠ The R0-INVERTED class carries the sourcing risk.** It generates 37 new consumer-facing NEGATIVE
claims ("this variety is not resistant to X") straight from a `susceptible` grade. Each is only as
good as the grade behind it, and a wrong grade becomes a wrong statement on a guide page. Spot-check
the grades against their anchors before generating this class at scale -- the 37 are not all equally
well evidenced, and `susceptible` is the value most likely to have been a default rather than a
finding.

The mapping is **one editorial rule authored once**, not per variety. It cannot drift from the
parent because it is derived. It covers all 67 existing assertions on day one with zero new content,
and it is exactly the "least invasive first" thesis applied at variety granularity: a scab-immune
Liberty should never be shown the sulfur rung.

`control_methods.resistant_varieties` already exists (`tier: cultural`, `applies_to: ["any"]`, used
as a rung 16 times, average position 0.4). It is the natural hinge between the two layers.

### 5c. Layer 2 -- AUTHORED, sparse. `ladder_delta`, only where a grade cannot say it.

Keyed by problem `id`, then by rung `method`. **`method` is verified unique within every ladder
(0 repeats across all 192 rungs), so it is a sound delta key.**

```json
"ladder_delta": {
  "apple-scab": {
    "basis": "source",
    "sources": ["cornell_ext"],
    "rungs": [
      {"method": "sulfur", "op": "drop",
       "why_beginner": "...", "why_seasoned": "..."}
    ]
  }
}
```

- `op` is one of `drop` / `replace` / `add`.
- `basis: "resistance"` means Layer 1 produced it and a gate can recompute it from the grade.
- `basis: "source"` means authored, and `sources` is then mandatory and must be T1.
- A `replace` carries `note_beginner` / `note_seasoned`; an `add` carries them plus `after`.

Sits on the variety record beside `resistance`, so it inherits the join that already works.

### 5d. The duplication check the issue asks for -- BUILT, mutation-tested, dormant

`tools/variety_ladder_delta_gate.py` + `tools/test_variety_ladder_delta_gate.py` +
`tools/mutate_variety_ladder_delta_suite.py`. Standalone and soft, wired into nothing.

**⚠ Its 0 on the live canonical is NOT coverage.** `ladder_delta` does not exist anywhere in
`20a32c47`, so the gate has nothing to grade -- a vacuous-looking zero of exactly the kind that
reads as protection while providing none. **The evidence is the mutation harness, not the zero:**
**15 mutations across 5 guard families, 15 CAUGHT, 0 survivors**, sentinel RED (a neutered
`delta_violations` must redden or the run exits HARNESS DEAD), positive control GREEN, and every
staged file read back and asserted to carry the MUTATION-APPLIED marker and to differ from the
original.

**No TDD RED phase is claimed.** The gate and its suite were written together, so the suite is
green from birth; that is the replay-pinned shape, and the mutation harness plus guard reachability
is what stands in for RED. G3 is proven reachable *without* G2 firing first (a one-word change
defeats byte-equality and must still be caught), because a guard that only ever fires behind an
earlier check is vacuous.

The guards:

1. **Referential.** Every `ladder_delta` key is a problem `id` on the parent crop. Every `method` in
   a `drop`/`replace` exists in the parent's ladder for that problem; every `method` in an `add`
   exists in `control_methods` and is absent from the parent ladder. Modeled directly on
   `variety_resistance_gate`, which proves this join holds at 0 violations.
2. **Non-vacuity.** A `replace` whose note is byte-equal to the parent rung's note is a violation.
   An empty `rungs` list is a violation. An `add` naming a method already in the parent ladder is a
   violation.
3. **Near-verbatim.** A `replace` note whose similarity to the parent note is **>= 0.85** is a
   violation. This is the instrument and threshold PLA-6 landed on
   (`test_no_pair_is_a_near_verbatim_copy`), and the direction is correct here: for detecting
   *copying*, high similarity is the signal. (PLA-6's finding that the metric is inverted applies to
   judging register *distinctness*, which is a different question.)

**Guard 3 is the one that matters.** Guard 2 alone is defeated by changing a single word, which is
how the PLA-6 pill duplication survived across 36 crops.

Each guard must be shown to FIRE on an injected instance before it is trusted -- an unmeasured guard
reads as coverage while providing none.

**Do not wire it into `gate_all` at birth.** Standalone + soft, the way `control_ladder_gate` and
`variety_resistance_gate` were born, and dormant until its data lands -- a roster gate armed ahead of
its data floods a parallel session's gauntlet.

### 5e. Already covered -- do NOT rebuild

`tools/control_ladder_gate.py` (0 violations) already enforces catalog integrity + T1 sources, rung
referential soundness, **tier monotonicity (softest-first)**, `applies_to` coherence via its
`TYPE_TARGETS` map, and unique kebab problem ids.

Measured: **0 of 52 ladders violate softest-first.** The least-invasive-first invariant that names
this issue is held perfectly by the data and is already gated. It does not need re-proving.

### 5f. THE RENDER CONTRACT -- write it before the consumer exists, not after

This is the discharge of section 4. PLA-6 cost an arc because the establishment pills were built
against an unstated contract and guessed wrong. The variety pest tier gets its contract stated up
front, so whoever builds the renderer is implementing a spec rather than inferring one.

**C1. One field per rendered unit.** No rendered element may take its text from a field another
element also renders. This is the exact rule PLA-6 had to retrofit (`year_one_notes_*` rescued as
Establishing, plus NEW `first_harvest_notes_*` and `full_harvest_notes_*` -- one field per pill).

**C2. The resolved ladder for a variety is `parent ladder -> Layer 1 -> Layer 2`, in that order,**
and the consumer renders the RESOLVED result. It must not render the parent ladder and the delta as
two separate lists -- that reproduces the duplication the delta exists to remove.

**C3. A variety with no `resistance` entry and no `ladder_delta` for a problem renders the parent
ladder verbatim.** Absence means "no delta", never "no ladder". This is the N/A branch, and it is
the majority case.

**C4. `susceptible` does not change the RUNGS, but it does change rung 0's FRAMING.** (Corrected
same day -- the first version said `susceptible` is never a delta and that a consumer must not
render a difference for it. That is wrong wherever rung 0 is `resistant_varieties`: 37 of the 62
graded pairs are exactly this case, and leaving rung 0 unchanged tells a reader who already owns a
susceptible plant to go choose a resistant one.) So: a `susceptible` grade never adds or removes a
rung, and never earns a "this variety is better" affordance -- but it MUST reframe an unsatisfied
`resistant_varieties` rung rather than repeat it verbatim.

**C5. The grade is the label; the ladder change is the consequence.** `immune` / `resistant` /
`tolerant` / `susceptible` are the four values -- a consumer that fails open on an unrecognized
grade turns a future fifth value into a silent regression, so it must fail CLOSED (render the
parent ladder) and never drop the rung silently.

**C6. `basis` tells the consumer whether it may recompute.** `basis: "resistance"` is reproducible
from the grade; `basis: "source"` is authored and must carry its T1 `sources`, which the consumer
surfaces the same way it surfaces any other sourced claim.

**C7. Nothing in the variety tier may be the ONLY home for a claim.** If a variety delta is the
only place a fact appears, the crop-level record is incomplete -- the crop ladder must stand alone
for a reader who never picks a variety.

---

## 6. Item 5 -- the container ruling

### 6a. The quoted container counts do not reproduce; the qualitative conclusion HOLDS

| issue claim | measured | note |
| -- | -- | -- |
| 101 container refs in `pests[]`/`diseases[]` (32 pests, 69 diseases) | **17 problem objects** (14 pests, 3 diseases), 43 term instances, 15 crops | see mechanism below |
| 0 are container-ONLY pests | **0** -- CONFIRMED by reading all 17 | holds |
| 2 of 52 ladders reference containers | **1 problem object**, 2 rung instances, and 1 of the 2 is a false positive | see 6c |
| 13 crops with pest advice in `container_notes` | **5 crops** carry organism-specific content (6 counting a causal mention) | see 6d |

**The mechanism of the 101:** a substring scan for `pot` matches **`spot` / `spots` / `spotted`
(1,258 instances)** and **`potato` / `potatoes` (~180)**. Disease prose is saturated with "leaf
spot", "purple spot", "ringspot"; that is why the issue's disease count (69) exceeds its pest count
(32). The real distribution is the opposite way round -- pests 14, diseases 3 -- because container
pressure is an arthropod story. A naive substring scan returns 484 objects; word-boundary matching on
real container vocabulary returns 17.

### 6b. Reading the 17: containers modify a rung, they do not gate a ladder. Trevor's ruling holds.

Zero container-only pests, confirmed by reading rather than counting. The nearest counterexample is
**chamomile / mealybugs** -- *"mostly on indoor or container plants"*, *"Uncommon on chamomile
outdoors"*, and its own note concedes *"Not specifically documented on the chamomile extension pages,
so treated as a general container-plant pest."* That is container-**conditioned occurrence** of the
same organism, plus a self-declared sourcing weakness. It does not overturn the ruling, and it is
worth its own look on sourcing grounds.

### 6c. Container content plays THREE roles, and they have different correct homes

| role | count | belongs |
| -- | -- | -- |
| **(a) Severity modifier** -- "worst on greenhouse or container plants" (roma-tomato + grape-tomato whiteflies; thyme/oregano/sage/marigold/zinnia/cosmos spider mites) | 11 of 17 | **stays in the problem's prose.** It is a fact about the organism. |
| **(b) Remedy / escape route** -- "grow in a container of clean mix" to sidestep a soil-borne pathogen (heirloom-tomato wilt, swiss-chard root-knot nematode, fig root-knot nematode, fig birds) | 4 of 17 | **a `control_ladder` rung.** This is a control action, currently trapped in prose. |
| **(c) Container as the risk source** -- lemongrass root rot from a saucer left standing | 2 of 17 | problem prose + `container_notes.drainage`. Already correct. |

Role (b) is the ruling's operative case and it confirms the issue's instinct exactly: the ladder is
where a container caveat lives, as one rung. **It needs a `container_culture` catalog method, which
does not exist** in the 37 -- no entry in `control_methods` covers growing in a container as a
control action.

**A fourth class is pure false positive:** "pot" meaning *debris on the ground*. `lettuce-leaf`
slugs ("clear away the boards, pots, and leaf litter") and `artichoke`'s ladder rung 0 ("Clear
boards, pots, dense ground cover") are habitat-clutter advice, not container culture. This is why
the "2 of 52 ladders" figure is really 1: artichoke rung 0 is clutter, rung 1 ("a copper band around
a raised bed or pot") is genuine.

### 6d. THE FINDING THE ISSUE DID NOT HAVE: there is already a FOURTH home, and it is 97.6% empty

**`container_notes.container_specific_pests` exists on 127 of 128 crops and is populated on 3.**

| crop | value |
| -- | -- |
| basil | `["aphids", "spider_mites"]` |
| artichoke | `["snails and slugs", "aphids"]` |
| lemongrass | `["spider_mites"]` |

Bare strings in three different conventions (kebab-free lowercase, `snake_case`, free prose). No
join to `pests[].id`, no register pair, no sources, no gate, and **no consumer reads it.**

`container_notes` is itself a rich 26-key object on all 128 crops, so this is a real, roster-wide,
schema-blessed field -- it is simply unfilled.

**So PLA-7 would not be authoring a third home. It would be authoring a fifth, alongside an existing
empty one purpose-built for the job.** That is a stronger argument for ruling now than the one on the
issue.

**Ruling: RETIRE `container_specific_pests`; do not fill it.** Filling it creates the second source
of truth the issue exists to prevent, and it cannot carry a register pair or a source, so nothing in
it could ever meet the cert bar. Route the three roles per 6c instead.

**One migration obligation before it can be dropped, and it is not a formality:**

| entry | already covered in `pests[]`? |
| -- | -- |
| artichoke / snails and slugs | YES -- `Snails and slugs (Cornu aspersum, Deroceras reticulatum)` |
| artichoke / aphids | YES -- `Artichoke aphid (Capitophorus elaeagni)` |
| lemongrass / spider_mites | YES -- `Spider mites (indoor and hot, dry conditions)` |
| basil / aphids | YES -- `Aphids` |
| **basil / spider_mites** | **NO -- basil's `pests[]` has no spider-mite entry at all** |

4 of 5 are duplicates of existing entries. **basil/spider_mites is unique content that exists nowhere
else in the record** and would be silently destroyed by a blind retire. It needs a real basil pest
entry (T1-sourced) before the field goes.

### 6e. Genuine container pest advice outside the array

- **cayenne-pepper** and **habanero**, `container_notes.overwintering.approach_seasoned`: *"inspect
  and treat for aphids and other hitchhikers"* -- actionable pest advice, byte-identical across both
  crops (a template family). This is real content in the wrong home.
- **mint**, `self_watering_notes_seasoned`: steady moisture "reduces the drought stress that brings
  on spider mites" -- a role (a) severity modifier, correctly placed.

The other 57 crops whose `container_notes` name a disease word are generic cultural prose
("drainage prevents root rot", "water the soil, not the leaves"), which is correct where it is.
`lemon`, named on the issue, has **no** pest or disease term in `container_notes` at all.

---

## 7. The inline cleanup slice -- re-measured. One of three counts is badly wrong.

Denominators reproduce exactly; the numerators do not. Measured over `*_beginner` string fields.

| term | issue claim | measured (field level) | measured (entry level) | verdict |
| -- | -- | -- | -- | -- |
| `nematode` | 78 of 84 unglossed | **77 of 83** | 66 of 71 entries | **HOLDS** |
| `bolt` / `bolting` | 223 of 317 | **244 of 317** (denominator EXACT) | 183 of 252 entries | roughly holds; my gloss test is stricter |
| `frass` | **24 of 31** | **10 of 31** (denominator EXACT) | **1 of 22 entries** | **WRONG -- overstates ~2.4x** |

**The frass count is the `crown` failure again.** 21 of 31 beginner fields already carry an in-field
gloss. The issue's own text names peach's *"sawdust-like frass"* as the model gloss to borrow -- and
the scan that produced 24 counted those very instances as unglossed. No plausible gloss definition
reproduces 24: parenthetical-only gives 20, "sawdust anywhere" gives 14, the read-verified definition
gives 10.

The 10 field-level misses are almost all the *second* mention inside an entry that already glossed it
(peach, plum, apricot, nectarine and cherry-sweet each gloss in `symptoms_beginner`, then use a bare
"gum and frass" in `organic_treatment_beginner`). That is defensible writing, not a defect.

**Exactly one entry is genuinely exposed**, and it sits in this arc's own territory:

> `artichoke.pests[0]` (Artichoke plume moth) -- the crop's certified ladder rung 1 says *"shows
> small holes and frass around the base"*, and the entry carries **no** `symptoms_beginner` or
> `symptoms_seasoned` at all (it is one of the 16 ladder-only stubs). A beginner meets "frass" cold,
> with nothing in the entry to explain it.

`nematode` is the real slice at 77 fields, and carrot's *"microscopic worms in the soil called
root-knot nematodes"* is the model to borrow, exactly as the issue says.

---

## 8. What Round 2 inherits

**Decided:**
1. Apple and strawberry both carry complete crop-level ladders. No prerequisite gap.
2. A4b's architecture is confirmed; its `{value, parent, changed}` triple is not used for ladders.
3. Layer 1 (derive from `resistance`) + Layer 2 (sparse authored `ladder_delta` keyed by problem `id`
   then rung `method`).
4. The duplication check is 3 guards, near-verbatim at 0.85 being the load-bearing one; standalone
   and dormant at birth; mutation-tested per PLA-215.
5. Container pest advice: severity stays in problem prose, remedy becomes a ladder rung, risk-source
   stays put. `container_specific_pests` is retired, not filled.

**Nothing blocks Round 2.** The variety pest tier does not render yet because it has not been built
yet; that is sequencing, and the render is queued as PLA-12. The obligation it creates falls on this
repo and is discharged as the C1-C7 render contract in 5f.

**Open, non-blocking:**
- A `container_culture` catalog method must be minted for role (b). Not in the 37.
- basil needs a real spider-mite `pests[]` entry before `container_specific_pests` can be retired.
- `varieties[].disease_notes` (1 record, apple/Liberty) duplicates its own `resistance` map.
- 133 string varieties on 20 crops cannot carry any variety-level mechanism.
- chamomile/mealybugs carries a self-declared sourcing weakness.
