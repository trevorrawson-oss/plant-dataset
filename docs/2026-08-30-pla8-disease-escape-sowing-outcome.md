# PLA-8 -- the `disease_escape_sowing` catalog round: outcome

Written 2026-08-30. Gap measurement + ruling: `docs/2026-08-28-pla8-disease-escape-sowing-gap.md`.
Base canonical `7f5079aa`; mint output `9f38bb00`; backfill output `ee0f54a3`.
Model round: `docs/2026-08-28-pla8-trap-cropping-outcome.md` (the same mint + backfill pairing).

---

## 1. WHAT SHIPPED

Two promotes, the chlorothalonil / trap_cropping pairing applied a third time.

| | promote | effect |
| -- | -- | -- |
| 1 | `tools/promote_pla8_disease_escape_sowing.py` | mints `disease_escape_sowing`, control_methods 59 -> 60. Zero crops, zero sources, zero existing methods. |
| 2 | `tools/promote_pla8_disease_escape_backfill.py` | 7 rungs on 7 certified crops, 14 register strings. Zero catalog change. |

Roster laddered stays **53 of 121** -- rungs added to ladders that already existed. Targets: the
four corns' `common-rust`, the two peas' `powdery-mildew`, fava's `broad-bean-rust`. Fava shipped
in batch 12 with this advice recorded as unplaced, so the backfill is 7 rather than 6, exactly as
the gap doc priced it.

## 2. THE RE-MEASUREMENT CONFIRMED THE GAP DOC

Re-run against `7f5079aa` over EVERY string field of every disease-typed problem (the
trap-cropping lesson: the eight standard prose fields are not the population). 34 raw hits, each
READ: **7 real instances on 7 crops**, all foliar fungal. The other 27 are different concepts
wearing similar words -- clean seed, roguing, cultivar choice at seed-buying time, spray timing
before the wet season, warm-soil vigor, radish's inherent speed, cilantro's early harvest. Four of
those became the pinned exclusions (§6).

## 3. THE MINT-NOT-WIDEN RULING, RE-TESTED AND HELD

The gap doc's ruling was a starting position with a stated overturn condition: if the T1
literature framed corn-rust/pea-mildew escape and insect planting-date timing as ONE practice
under a single heading, widen `planting_time_avoidance` instead. It does not: WSU states the
escape inside its powdery-mildew management text, Cornell inside a rust factsheet, and NCSU's only
plant-early sentence is armyworm-specific in its insect section. Different documents, different
organisms, two methods. `planting_time_avoidance` is untouched (byte-identical, along with the
other 58).

**Key named `disease_escape_sowing`, not the doc's proposed `disease_escape_timing`**: all seven
instances are sowing-date decisions on direct-sown crops, and CURRENT_STATE already names the gap
"disease-escape sowing". `applies_to: ['fungal_foliar']` exactly -- tight, per the doc.

## 4. THE ANCHOR HUNT IS THE ROUND'S HEADLINE FINDING

**All four documents pinned on the target problems themselves were fetched first, and NONE states
the escape.**

- NCSU "Organic Sweet Corn Production" (the corns' sole anchor): its rust paragraph recommends
  resistant cultivars only. Its one plant-early sentence ("plant early so that corn matures in
  mid-August before armyworms peak") is about an INSECT, in the insect section.
- RHS "Broad bean rust" (fava's sole anchor): spacing, sanitation, no fungicide for gardeners.
  Nothing on sowing dates.
- UMN "Growing peas" and Clemson "Garden Peas": nothing connecting sowing time to mildew.
- WSU's pinned pea anchor (the Mt Vernon photo gallery): a photo and a pathogen name.

The practice IS published at T1, elsewhere, and the entry anchors there:

- **WSU Hortsense, "Pea: Powdery mildew"** -- THE PRACTICE, verbatim: "Plant peas early. Spring
  crops seldom show serious damage." Plus "often worse in the fall."
- **Cornell, "Common Rust of Sweet Corn"** -- THE TIMING the escape rests on: "usually observed
  for the first time in New York sweet corn crops from mid-June onwards and is prevalent in late
  season plantings"; resistant cultivars for late plantings.
- **NCSU, "Organic Sweet Corn Production"** -- THE COUNTER-EXPOSURE, quantified: minimum soil
  50°F (standard) / 60°F (se, sh2, sy), "Seed planted in moist soil below these temperatures
  will often rot."

**Read and NOT cited, deliberately:** Illinois' "Rusts [Vegetables]" focus page, which search
summaries still quote for "early season sweet corn hybrids often escape infection", redirects to
a generic landing page -- a page that cannot be read is not evidence. USU's vegetable-guide
powdery mildew page carries no timing statement. Purdue ID-405 (pypdf-extracted) corroborates the
seasonality ("if rust develops on early plantings, consider fungicide applications for later
plantings") but does not state the escape.

**FILED, NOT FIXED:** the crop-prose escape sentences themselves are not published by their
problems' pinned anchors (fava's sole anchor is the RHS page that does not carry the advice).
Whether they trace to other documents in each crop's certification set is a verification_log
question for a later pass; this round's rungs attribute to "this crop's guidance", which is true
of the prose, and the METHOD carries its own T1 anchors for the practice.

## 5. THE SAFETY-BEARING HALF IS THE TRADE

The escape is a race the grower can lose at the START: early sowing trades late-season disease
for a cold, wet seedbed. The cautions carry five required axes (`seed_rot`, `threshold` with the
50°F/60°F figures, `not_a_cure`, `resistance` as not-a-substitute, `late_build` scope honesty),
and every rung names the cold trade and points at the method's cautions. Fava's rung goes
further -- its counter-exposure is documented ON THE SAME CROP (the `root-rots-damping-off` entry
warns against sowing into cold, soggy ground), so `check_fava_premise` asserts that prose in
canonical, per the batch-5 rule.

## 6. THE FOUR EXCLUSIONS, PINNED IN BOTH DIRECTIONS

| problem | class | why no rung |
| -- | -- | -- |
| `spinach`/`damping-off` | OPPOSITE | early sowing into cold soil CAUSES it; its prose says wait for warmth. **Typed `fungal`, so TYPE_TARGETS would ACCEPT the rung** -- the one the gate cannot catch, and the reason the list exists |
| `radish`/`black-rot` | INHERENT | the crop's speed, not a sowing decision; no action to place |
| `cilantro-coriander`/`powdery-mildew` | HARVEST | "pick the leaf crop young" moves the harvest, not the sowing |
| `jalapeno`/`mosaic-viruses` | ROGUING | "remove infected plants early" -- the scan matched "early" doing a different job |

Both promotes refuse if any exclusion fails to RESOLVE; each carries its own reason string.

## 7. PLACEMENT AND THE DISTINCTNESS KEY

The rung lands **immediately after `resistant_varieties`** on the six whose ladders open with it
(both are decisions settled before anything is in the ground, and the crops' own prose puts
resistance first: "the single most effective step"), and at the **front of fava's ladder** (no
resistance rung; its prevention prose LEADS with the escape). All leading runs are cultural;
verify_post asserts the exact index on every target plus monotonicity.

**Three texts: corn x4, pea x2, fava x1.** The distinctness correspondence keys on the ESCAPE
SENTENCES rather than whole-field bytes -- the two peas differ in their variety-name sentences
but carry the escape byte-for-byte, so a whole-field key would have forced a fork the sources do
not carry. Corn's four are byte-identical over all four fields. Both directions pinned.

## 8. WHAT THE MUTATION HARNESSES SHOWED

Both suites replay-pinned; no RED phase claimed. Evidence is `VerifyPostIsDriven` plus the
harnesses. Every driver asserts its branch's ONE message -- no hedged ORs, per the trap-cropping
lesson.

- **Mint: 34 injected, 34 caught, 0 survived, FIRST RUN.** Preflight 35/35 anchors matched
  exactly once; positive control GREEN; sentinel RED. disclosure 8/8, scope 6/6, blast 7/7,
  exclusion 5/5, contrast 4/4, hygiene 3/3, mechanics 1/1.
- **Backfill: 30 injected, 30 caught, 0 survived, FIRST RUN.** Preflight 31/31; positive control
  GREEN; sentinel RED. premise 4/4, distinct 3/3, placement 5/5, contract 3/3, exclusion 4/4,
  blast 7/7, content 1/1, hygiene 2/2, mechanics 1/1.

Zero first-run survivors on both is a first for this arc, and it was not luck: the suites were
written against the trap-cropping round's post-mortem (VerifyPostIsDriven first, verbatim check
last in its group, exclusions before the sweep, single-message assertions, real rebindings
instead of the inert `() or` idiom).

## 9. THE GAUNTLET

Run against the applied state (`ee0f54a3`).

- `tools/gate_all.py` -- **121/121 certified crops PASS**
- `whole_crop_gate` -- **PASS on all 7** touched crops
- `control_ladder_gate` -- **0 violations**
- `register_completeness_gate` -- **PASS**, 0 unruled prose fields
- `release_verify` (vs the committed `7f5079aa` base, `--slug sweet-corn`,
  `--expect-changed` the other six) -- **clean, no blocking concerns**; only the 7 declared
  crops changed, `control_methods` the only top-level change, catalog +none -none, reference
  `lettuce-leaf` byte-identical. One non-blocking Step-5.5 review note (a pre-existing
  nevada/z9 heat_pause value-identity, untouched by this round).
- COMPACT preserved; both guard suites green under both runners (63 mint + 52 backfill = 115).

## 10. OWED / CARRIED FORWARD

- **Five crops pick the rung up for free once laddered**, if their prose states the escape when
  their batches run -- check at authoring time rather than assuming (the spring fruiting batch is
  next; peppers/eggplant/okra were not in this scan's hit set).
- **The filed crop-prose sourcing question** (§4): the seven escape sentences vs their problems'
  pinned anchors.
- **The catalog-owed list is unchanged**: `container_culture`, a generic pheromone/monitoring
  trap, diatomaceous earth, `bottom_watering`+bacterial, `straw_mulch`+physiological, `mancozeb`
  at the melons batch.
- `note_seasoned` backfill on the 5 pre-standard crops (53 rungs) still waits for its own round,
  per the batch-12 filing; the 14 new strings here all carry both registers.
