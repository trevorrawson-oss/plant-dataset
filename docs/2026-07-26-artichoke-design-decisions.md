# Artichoke GS arc — design decisions

**Date:** 2026-07-26
**Crop:** artichoke, GS #121 (shell → certified)
**Kickoff:** `docs/2026-07-26-artichoke-gs-arc-kickoff.md` — this document answers its §3.
**Base canonical:** `34025ee3` (verified: `shasum -a 256` matches `LATEST.txt`; tree clean; main ahead 2).

This document exists because the asparagus defect traces to one modeling decision made mid-authoring
whose field-level consequences were never written down. Everything below is decided **before**
authoring, and every decision carries its consequence for **every** affected field.

---

## Part A — constraints derived from the gate suite (verified, not assumed)

These are facts about the machinery, established by reading and running it. They bind the decisions
in Part B regardless of what the biology turns out to say.

### A.1 The region roster is 16 / 39, and that is not a judgment call

`zone_span_gate.EXPECTED_SPANS` defines 16 regions totaling 39 zone cells. A45 pins any populated
region to its canonical span **exactly** and requires `resolved_by_zone` key parity.

Measured across all 128 crops:

| regions | crops | what they are |
|---|---|---|
| 16 | 112 | every certified crop |
| 10 | 8 | artichoke, avocado, olive, 5 mushrooms — **all uncertified shells** |
| 0 | 8 | the microgreens (indoor; region roster legitimately collapses to `{}`) |

**Decision: artichoke goes to 16 regions / 39 cells.** The 10-region roster is not a considered
narrower scope; it is the shell scaffold that every crop starts from and that certification fills.
No certified non-indoor crop has ever shipped at 10. A31 (region roster floor) enforces this
independently of A45.

The shell is short by **19 cells**, not 12 — the kickoff counted the 6 missing regions but not the
missing cells inside regions that already exist:

| region | expected | shell has | missing |
|---|---|---|---|
| `pnw` | 8,9 | — | whole region |
| `mid_atlantic` | 7,8 | — | whole region |
| `mid_south` | 7,8 | — | whole region |
| `nevada` | 8,9,10 | — | whole region |
| `utah_dixie` | 8 | — | whole region |
| `rgv` | 9,10 | — | whole region |
| `se_gulf` | 8,9,10 | 8,9 | z10 |
| `ca_south_coast` | 9,10,11 | 9,10 | z11 |
| `ca_desert` | 9,10,11 | 9,10 | z11 |
| `low_desert_az` | 9,10 | 9 | z10 |
| `hawaii_tropical` | 10,11,12,13 | 11 | z10, z12, z13 |

Column passes must run against the **complete** 39-cell roster (per
`docs/gs_cross_crop_field_addition_v0.md`), so the shells land **before** any authoring pass, not
during one.

### A.2 The DTM decision has a mandatory cascade

From `register_coverage_gate` (A39), reusing `timing_spine_gate` predicates:

- `days_to_maturity` non-empty ⇒ **`dtm_anchor` is REQUIRED** (enum: `from_sow`, `from_transplant`,
  `from_planting`). Asparagus escapes this only because `dtm_empty()` is true for it.
- `propagule` ∈ `{seed, set, clove, tuber}` (`SEED_LIKE`) ⇒ **`sow_depth_inches` is REQUIRED**.
  `transplant`, `division`, `crown`, `bare_root`, `rhizome`, `runner`, `slip` do **not** trigger it.
- `propagule` is required for every certified crop, and is a **single** enum value —
  `{seed, transplant, division, crown, bare_root, rhizome, runner, slip, set, clove, tuber}`.

So "give artichoke a DTM" is not a one-field decision; it pulls in `dtm_anchor`, and the propagule
choice independently pulls in `sow_depth_inches`. Both are cheap to author correctly and both are
R1 traps if the decision is made without noticing them.

### A.3 A46 already permits a year-one harvest

`herbaceous_perennial_gate` rule 4 requires `years_to_first_harvest` to be a non-empty numeric list
with **`min >= 1`**. A crop that yields in its first season is therefore fully representable as
`[1, ...]`. The archetype does **not** assume a multi-year lag — it assumes a *stated* one. This
matters: it means the dual-mode model does not require a gate change.

Also required by A46: `years_to_full_production` non-empty, `productive_lifespan_years` a **positive
int** (not a list — `[20, 50]` would fail), `succession_policy.suitable: false` **with**
`reason_seasoned`, `rotation` present, and every filled cell carrying `suitability` in
`{perennializes, marginal, unsuitable}` with `suitability_note_seasoned` on marginal/unsuitable
plus a non-empty calendar.

### A.4 `planting_layout` must be a STRING

A44 enum; the dict form crashes it. In use roster-wide: `"row"` (1 crop), `"block"` (4).

### A.5 The archetype carve-outs are inherited silently — so they are now audited

`archetype == "herbaceous_perennial"` carries three exemptions, each justified for asparagus
specifically:

| gate | exemption | asparagus justification |
|---|---|---|
| A24 | frost/`cold_pause` on a `plant_out` month | a **dormant crown** goes in while the ground is cold |
| A34 | `harvest` token with no plant-class token | an established bed is planted **once**, not annually |
| A37 | `growing` unreachable from a plant token | the **summer fern** grows after the spring spear harvest |

**A24's justification does not transfer to artichoke by analogy.** In cold zones artichoke does not
plant a dormant crown — it sets out a live, vernalized transplant, which is exactly the frost-tender
transplant A24 exists to protect. Inheriting the exemption there would silently disable a check that
is genuinely appropriate.

Built for this arc: **`tools/carveout_dependency_audit.py`**. It runs each of the three violation
functions twice — once as-is, once on a copy with `archetype` masked to a sentinel — and reports the
diff, which is precisely the set of violations the carve-out is suppressing. Verified: each of the
three modules reads `archetype` exactly once and only for the carve-out, so masking disables the
exemption and nothing else (`calendar_basis` untouched, all three gates still run in full).

Validated adversarially on a scratch copy: a `cold_pause` injected onto a **core harvest** month —
a branch the carve-out explicitly does *not* exempt — still bounces `whole_crop_gate` (A24, 1
violation) **and** is correctly excluded from the audit's diff. The tool distinguishes "suppressed
by the carve-out" from "genuine defect" rather than reporting everything.

Baseline for comparison, asparagus on canonical `34025ee3`: **A24 34 cells, A34 29 cells, A37**
dependent. Every artichoke cell that lands in this diff must have a written agronomic reason.

**Binding acceptance criterion:** artichoke's cold-zone cells — the ones planting a live transplant
rather than a dormant propagule — must pass A24 with the carve-out disabled. Any that do not are
either mis-authored or need their dependence justified in prose.

### A.6 A47 closes half the hole; the other half is now closed too

A47 (hard) requires `plant_out` on every calendared non-`unsuitable` cell of a `perennial: true`
crop. It does **not** look at `harvest`. Asparagus shipped with **zero of both**; A47 would have
caught one.

Built for this arc, TDD RED → GREEN: **`tools/perennial_harvest_gate.py`**, wired as **A48**.

- Scope: `archetype == "herbaceous_perennial"`, deliberately narrower than A47's `perennial is True`.
  Measured: the broader scope floods **195 cells across 5 crops** — thyme, rosemary, oregano, sage,
  lavender, 39 cells each — cut-as-needed herbs with no discrete harvest window. Whether those
  should carry a harvest string is a **separate open ruling**, recorded and not decided here.
- Exemptions mirror A47 exactly (empty calendar = admission state; `unsuitable` = never promise food
  where the crop will not grow), so the two halves of the floor cannot drift apart.
- Ships reporting **0** for asparagus, the only current member — enforcing a convention already met.
- Adversarially verified: stripping the 29 real asparagus `harvest` strings reproduces the shipped
  defect exactly, and A48 reports all 29 through `whole_crop_gate`.
- `gate_all` re-run after wiring: **120/120 PASS**, no collateral.

### A.7 Shell-only keys are dropped on promote

The shell carries scaffolding keys the certified shape does not: `zone_8_presence`,
`zone_10_desert_fold`, `sources_pending_admission`, and the per-cell
`suitability_reason_beginner`/`_seasoned` (the certified field names are
`suitability_note_beginner`/`_seasoned`). Asparagus carries none of the scaffolding. The promote
script drops them.

### A.8 Citation hygiene, operationalized (R3/R4)

`ucanr_ext` and `unr_fs0261` are legitimate **umbrella** catalog entries in wide roster use. The
asparagus R4 failure was not the catalog entry — it was the per-cell `anchoring_urls[id].url`
pointing at a document (the Kings County 2005 crop report; a fact sheet whose only mention of the
crop is `"Stems - asparagus"`) that does not contain the claim.

**So the operational rule for this arc:** truth lives in the per-cell anchoring URL, not the source
id. For every cell, the anchored document must be fetched and the claim sentence confirmed present
before the citation ships.

---

## Part B — the modeling decisions

Research distilled in `scratchpad/research_{mechanism,ipm_varieties,mid_belt,mid_south,pnw_nv_ut}.md`.

### B.0 THE MECHANISM, WRITTEN FIRST (kickoff §3.4 / R5)

Every `marginal`/`unsuitable` rating in this crop must cite one of the clauses below and a source.
If a cell cannot be tied to one of these, it cannot be rated.

> Artichoke has a **quantitative, genotype-dependent vernalization requirement for flower-bud
> initiation** — not an obligate one. Cold advances and synchronizes bolting; its absence reduces the
> *proportion* of plants that bud and delays them, rather than preventing budding. Reported
> requirements span **205 to 1356 hours below 50°F**, and the spread is cultivar-driven, not
> measurement error. Bud quality is capped above **86°F**; heat above roughly **65°F** can also
> **devernalize**, reversing accumulated chilling. Buds are injured at **29.9°F** and severely damaged
> below **24.8°F**. The perennial stand fails at **14 to 15°F** (severe crown loss even under mulch).
> Perennial plantings stay productive **5 to 10 years**.
>
> **Separately, and load-bearing: in cool coastal California the controlling mechanism is not chill
> accumulation at all**, but a continuously extended bud-*induction* period inside a 45-85°F range.

Anchor quotes (all verified at source by the researching agent):

- Quantitative, not obligate — Rutgers FS044: *"'Imperial Star' produced more buds (74%) with **no
  vernalization treatment** compared to 'Green Globe Improved' (57%). When subjected to a cool
  temperature period, 98% of 'Imperial Star' and 86% of the 'Green Globe Improved' plants produced
  buds."* and *"vernalization **promotes** the initiation of these flower buds."*
- Crown kill — OSU *Oregon Vegetables*: *"At temperatures under 15 F severe loss of crowns would be
  expected even with mulch protection."* Independently corroborated by Welbaum 1994: *"Artichokes
  cannot be grown reliably as perennials without winter protection where temperatures are
  consistently below -10C"* (= 14°F).
- Heat ceiling — UC ANR 7221: *"Plants are tolerant of temperatures above 86°F (30°C), but the
  quality of the edible flower bud is reduced."* Three independent T1 sources agree on 86°F.
- Devernalization — Gerakis 1969: *"Air temperatures above 65° immediately after sowing the
  vernalized seed caused devernalization."*
- Stand life — UC ANR 7221 and UC IPM independently: *"5 to 10 years."*

**The California carve-out, stated explicitly so no cell inherits the wrong mechanism.** UC ANR
Publication 7221 — the peer-reviewed California production bulletin, and the strongest source in the
corpus — contains **zero occurrences of "vernal", "chill", "dorman", "photoperiod", or "day length"
in either edition**, verified programmatically. Its entire bud-induction model is a temperature
*range*:

> *"Artichokes are a cool-season crop that grows best in 75°F days and 55°F nights. The temperature
> range for a good crop is from 85°F to 45°F. In areas with cool day and night temperatures (i.e.,
> cool coastal climates), the period of flower bud induction is extended, thereby lengthening the
> production period."*

**Rating a California cell on chill hours would be the asparagus error committed again**, in a crop
where the chill mechanism is otherwise genuine. Coastal California does not accumulate a chill
*event*; it sits inside the induction range more or less continuously. That is why Castroville works.

**Three things this mechanism explicitly does NOT support, and which must not be authored:**

1. **"Summer dormancy" in California is NOT T1.** The cut-back and the roughly one-month irrigation
   gap *are* documented (UC ANR 7221, both editions), but 7221 frames them purely as harvest timing
   and never uses the word. The only source using "dormancy" is an **unattributed** UC Master
   Gardener page which also asserts *"Zones: 3-11"* — flatly incompatible with a 15°F crown kill.
   One false datum on the page is reason to distrust the rest (R3). Texas is different: TAMU EHT-065
   *does* independently describe a summer-dormant crown, for Texas, and may be cited there.
2. **"Day-neutral" is NOT supported.** Berentsen 2024 records the literature as split three ways
   (obligate long-day / short-day / photoperiod-independent), "suggesting a genotype-dependent
   response." No US extension source states any photoperiod effect. Model as photoperiod-agnostic;
   do not assert day-neutrality as fact.
3. **No foliage-damage temperature exists in T1.** The 28°F (UF/IFAS) and 25°F (OSU, TAMU) figures
   are **whole-plant management thresholds** and must not be relabeled as foliage thresholds.

### B.1 THE BIG ONE — one crop, with the mode carried per region

**Decision: ONE crop. The annual/perennial split is modeled as a per-region property, not as two
crops and not as a crop-level flag.**

Why:

- It is one species, one grower intent, and one page. A grower searching "artichoke" in Minnesota and
  one in Monterey want the same crop, differently instructed.
- The split is **regional by nature**, and `regions.<slug>.resolved_by_zone.<zone>` is exactly where
  this dataset already carries per-region behavior. Extension services frame it the same way — UC
  Master Gardener: *"Artichokes are perennial (annual in low desert regions)"*; OSU: *"In Western
  Oregon, artichokes can often be grown as short-lived perennials. In Central and Eastern Oregon,
  gardeners may grow them as annuals"*; UMass: *"In New England, artichokes are not cold hardy enough
  to survive winter reliably and therefore must be grown annually from seed."*
- A two-crop split would duplicate the IPM ladders, the cultivar set, and the source catalog for one
  botanical entity, and would force a grower to pick a lane before knowing which applies to them.

**The decisive gate fact that makes this safe:** A46 rule 4 requires `years_to_first_harvest` to be a
non-empty numeric list with **`min >= 1`**. A crop that yields in its first season is therefore fully
representable. **The archetype does not assume a multi-year lag — it assumes a *stated* one.** So the
dual-mode model needs no gate change.

**Where the mode is recorded, and the R1 verification that it is actually there.** The mode is not a
field; it is carried in four places, and each must be *read* before cert, not assumed:

| carrier | what it must say |
|---|---|
| per-cell `suitability` | whether the *planting persists* (see B.6) |
| per-cell `suitability_note_beginner` / `_seasoned` | on every non-`perennializes` cell: that it is grown as an annual here, and what that means |
| per-cell `plant_out` parenthetical | the organ actually planted in that cell — transplant vs division |
| `region_notes_beginner` / `_seasoned` | the region's mode in prose, re-read against its cells (R7) |

### B.2 Archetype — MOVE to `herbaceous_perennial`, with the carve-outs audited not inherited

**Decision: move `warm_season_fruiting` → `herbaceous_perennial`.** Artichoke is a herbaceous
perennial vegetable; it is the crop the archetype was explicitly built to take second (the gate's own
docstring says *"asparagus, later artichoke"*). A46's requirements are all satisfiable honestly.
`calendar_basis` stays `frost_anchored` — `calendar_basis_gate` maps the archetype to exactly that,
so the move is consistent, and flipping the basis would silently disable six gates.

**The move inherits three carve-outs, and one of them is not justified here.** Per A.5:

- **A24 (frost pause on a `plant_out` month) — justification does NOT transfer.** It exists because a
  dormant crown goes in while the ground is cold. Cold-zone artichoke plants a **live, vernalized
  transplant** — the frost-tender transplant A24 exists to protect. **Binding criterion: every
  cold-zone artichoke cell must pass A24 with the carve-out disabled**, verified via
  `tools/carveout_dependency_audit.py`. Any cell that depends on the exemption must either be
  re-authored or carry a written agronomic reason. Warm-region cells planting divisions in winter may
  legitimately depend on it — that is the asparagus case and it transfers.
- **A34 (harvest with no plant token) — transfers, for perennial cells only.** An established bed
  planted once. Annual-culture cells carry a real plant token and will pass on their own merits.
- **A37 (growing after harvest) — transfers.** The California cut-back-and-regrow cycle is genuinely a
  post-harvest growth phase, documented in UC ANR 7221.

The audit output is a required cert artifact, reviewed cell by cell.

### B.3 `days_to_maturity` — NON-EMPTY. This is the R1 trap, and it is declined.

**Decision: `days_to_maturity = [60, 100]`, `dtm_anchor = "from_transplant"`.**

`[]` would be inherited-by-analogy from asparagus and would be **wrong**: artichoke is grown as a
first-year annual across most of this roster, and an annual grower without a DTM cannot plan. The
kickoff names this precisely and it is the single easiest way to repeat the original defect.

Sourcing, and why this range and not another:

- **VCE 438-108 is the anchor** because it is unambiguous about the operation: *"bud production will
  commence **60 to 100 days after transplanting**."*
- **UMaine Highmoor trials corroborate inside that range**: 75, 85, 88, 90 days after transplanting
  across five cultivars, and 76-94 DAT the following year.
- ⚠ **WSU EM057E's "85-120" is deliberately NOT used to set the anchor.** It appears in a table titled
  *"Seeding recommendations..."* whose other columns are seed-relative, so whether its "Days to
  Maturity" counts from seed or from transplant is ambiguous. That is exactly the R8 hazard —
  confirming what operation a number describes — and an ambiguous datum does not get to define an
  anchored field. Recorded as an open finding.
- UC ANR 7221's *"4 to 6 months"* from transplanting is commercial California and sits outside the
  home-garden range; carried in prose, not in the field.

**Cascade this triggers (A.2), all mandatory:** a non-empty DTM makes **`dtm_anchor` required**. Both
are authored together or neither ships.

### B.4 Propagule — `transplant`, with the other organs documented and verified

**Decision: `propagule = "transplant"`.** The enum takes one value, and across this roster the
dominant home-garden path is unambiguously a transplant — usually the gardener's own, raised indoors
and vernalized:

- VCE 438-108: *"greenhouse-grown transplants should be used instead of direct field seeding."*
- USU: artichoke sits in Group A under **"Plants:"**, not "Seed:", and is the fact sheet's own worked
  example for the seed-indoors-then-transplant path.
- NC State: `T` marks, with *"To grow transplants, seed 6-8 weeks before the 'T' date."*
- TAMU EHT-065: seed started under protection, own seedling set out.
- UC (Master Gardener Handbook Table 13.2): the artichoke row carries an asterisk overriding the
  table's seed default — *"Transplants, shoots, or roots are used for field planting."*

**Consequence:** `transplant` is **not** in `SEED_LIKE`, so `sow_depth_inches` is not required. It
will nonetheless be authored as `[0.25, 0.5]` from WSU's published depth, because most growers of
this crop *do* start their own seed and the number is real. Optional-but-present is honest here;
absent would be a small avoidable gap.

**Where the other organs live — and the R1 obligation attached.** Divisions, offshoots, and crowns
are real and dominant in perennial regions (UC IPM: *"Perennial plantings of artichokes are typically
grown from crown divisions"*; OSU EM 9027's PNW window is for **crown pieces**). They are recorded in:

1. `start_method.notes_seasoned` / `notes_beginner` — the propagation routes in prose, and
2. the per-cell `plant_out` parenthetical, e.g. `"Jul 1 - Jul 31 (crown divisions or nursery
   transplants)"`.

**This is precisely the promise asparagus made and broke.** Its cert plan designated
`start_method`/`year_one_notes` as the home for timing that was then never written. So: **before
cert, both fields are read and confirmed non-null and specific.** Note that artichoke's
`year_one_notes_beginner` / `_seasoned` are currently **null** despite the kickoff listing them as
authored — key presence is not content.

### B.5 Category — `Fruiting Veg` → `Perennial Vegetables`

**Decision: move.** Artichoke is an immature flower bud on a herbaceous perennial, not a fruit. This
reuses the value asparagus already created, so it introduces **no new category** and no new frontend
work beyond the grouping the astro lane already owes for asparagus. Recorded for the astro lane;
`src/pages/index.astro` carries the category list. No bump from this session.

### B.6 The suitability vocabulary under a dual-mode crop — a real tension, resolved conservatively

The enum is `perennializes` / `marginal` / `unsuitable`. For a crop that is a productive **annual**
in cold regions, none of those three says "good crop, just replant it."

**Decision: use the existing enum literally — it answers "does the planting persist?" — and let the
dual-register notes carry the annual-culture instruction.** Cold-zone cells where artichoke crops
well as an annual are rated `marginal`, with notes that say plainly that it is grown as an annual
there and will not survive the winter.

Why not extend the enum with an `annual_only` value: it would be more expressive, but it is a
**frontend-visible vocabulary change** shipping mid-arc into a renderer that does not know the value,
on top of a category move the frontend also has not absorbed yet. The honest content is fully
carryable in the notes today. **Recorded as an open finding and a candidate follow-on**, not
smuggled in as a side effect of this arc.

**What each rating means for this crop, and what may justify it:**

| rating | meaning here | what may justify it |
|---|---|---|
| `perennializes` | the stand persists and crops for years | winter minima stay above the 14-15°F crown-kill line **and** summers do not chronically devernalize |
| `marginal` | crops, but the planting does not persist — annual culture, or a short-lived/protected stand | crown kill at 14-15°F; or heat above 86°F degrading bud quality; or a documented low bud-set proportion |
| `unsuitable` | do not plant | **only** where even annual culture fails |

**Load-bearing consequence of B.0:** because vernalization is *quantitative*, an "insufficient chill"
argument **cannot** carry `unsuitable` — at most `marginal`, and the note must say what actually
degrades (earliness, uniformity, proportion budding), never imply no crop. `unsuitable` needs a
stronger claim, and one exists for the hot subtropics — UF/IFAS HS1289: *"artichokes do not initiate
flower-bud formation or 'bolting' without artificial vernalization in Florida because of insufficient
chilling hours"* and *"bud formation must be artificially induced."* A home grower cannot artificially
vernalize a field. That is a named, cited, mechanism-grounded basis, and it is the only one.

### B.6a Interaction with the post-asparagus hardening kickoff, Item 4

`docs/2026-07-26-post-asparagus-hardening-kickoff.md` landed from a concurrent session mid-arc and
names artichoke directly (*"artichoke will make 21"*). Its Item 4 rules that asparagus's ten
`unsuitable` cells carry a **fabricated all-`growing` calendar** — a field invented to satisfy A32,
the gate-avoidance pattern inverted — and that the fix is **sequenced behind the frontend**: the
renderer must hide `unsuitable` cells first, because emptying the calendars now fails A32 (a
documented, reverted attempt).

**Consequence for this arc, decided rather than inherited:**

1. Artichoke's 8 `unsuitable` cells **keep a non-empty calendar**, because A32 still requires it and
   the carve-out is blocked on frontend work this session does not own.
2. **But the all-`growing` strip is not a fabrication here, and that difference is the point.**
   Asparagus in the tropics does not grow year-round — its strip was invented. Artichoke in the
   tropics genuinely does: UF/IFAS's mechanism is that plants *stay vegetative* and never initiate
   buds. An all-`growing` strip is a literally accurate depiction of what the plant does, and the
   dual-register note carries the consequence — you get leaves, not artichokes. So artichoke joins
   the queued Item 4 fix as a beneficiary, not as eight new instances of the defect.
3. Artichoke's ratings satisfy Item 4's **display rule** (`unsuitable` = structurally impossible,
   not a bad-year risk). Checked cell by cell: fl_peninsula z10/z11, hawaii z10-z13 and se_gulf z10
   have no cool season in any year, which is structural. **One exception worth naming:**
   `ca_desert` z11 is `unsuitable` for a different reason — **no California desert ground reaches
   zone 11**, so it is vacant ground rather than an agronomic verdict. That is the asparagus
   precedent and it is honest, but it is a vacancy, not an impossibility, and the note says so.

### B.7 Per-field consequence table

Every field in kickoff §1, with the decision's consequence. **No field is left implicit.**

| field | now | decision | why / consequence |
|---|---|---|---|
| `archetype` | `warm_season_fruiting` | → `herbaceous_perennial` | activates A46; inherits A24/A34/A37 carve-outs → **audit required** (B.2) |
| `calendar_basis` | `frost_anchored` | **unchanged** | archetype maps to it; flipping would disable six gates |
| `category` | `Fruiting Veg` | → `Perennial Vegetables` | asparagus precedent, no new value; astro lane notified |
| `perennial` / `lifecycle` | `true` / `perennial` | **unchanged** | correct; A46 rules 1-2 satisfied; keys A47 |
| `days_to_maturity` | `[]` | → `[60, 100]` | **the R1 trap declined** (B.3); forces `dtm_anchor` |
| `dtm_anchor` | absent | → `"from_transplant"` | **mandatory** once DTM is non-empty (A.2) |
| `days_to_maturity_mid` | `null` | → mid of range | display convention |
| `years_to_first_harvest` | `[]` | → `[1, 2]` | year 1 under annual/vernalized culture, year 2 for a perennial stand; A46 needs min ≥ 1 ✓ |
| `years_to_full_production` | `[]` | → `[2, 3]` | UMass: *"artichokes will produce in their first year but yields will greatly increase in following years"* |
| `establishment_years` | `null` | → `2` | **NOT a copy of `years_to_first_harvest`** (kickoff §1); years until the stand reaches steady bearing |
| `productive_lifespan_years` | `null` | → `7` | **must be a positive int** (A46 rejects a list); the middle of UC's independently-corroborated 5-10 year replant interval |
| `propagule` | `null` | → `"transplant"` | A40 enum; **not** SEED_LIKE → `sow_depth_inches` not required |
| `sow_depth_inches` | absent | → `[0.25, 0.5]` | optional here; authored from WSU because most growers start their own seed |
| `planting_layout` | `null` | → `"row"` | A44 needs a **string**; the dict form crashes it |
| `start_method` | all null | **authored** | must carry the propagation routes AND their timing — **read and confirmed before cert** (R1) |
| `year_one_notes_*` | **null** (kickoff says authored — it is not) | **authored** | the exact field asparagus promised and never wrote |
| `succession_policy` | `{null, null}` | → `suitable: false` + `reason_seasoned` | A46 rule 3 |
| `rotation` | all null | **authored** | A46 rule 7; must carry the Verticillium rule — do not follow lettuce or strawberry; rotate into brassicas |
| `verification_status.status` | `null` | → `verified_gs_arc` at cert | flips A39-A42 register floor on |
| `regions` | 10 / 20 cells | → **16 / 39 cells** | A31/A45; shells land before any column pass |
| per-cell `suitability` | `null` | authored per B.6 | A46 rule 6 |
| per-cell `plant_out` | `null` | **authored, every non-`unsuitable` calendared cell** | **A47 hard** |
| per-cell `harvest` | `null` | **authored, every non-`unsuitable` calendared cell** | **A48 hard** (new, this arc) |
| `heat_threshold_f` | — | → `86` | three independent T1 sources; a **quality** ceiling, note must say so |
| `frost_tolerance_f` | — | → `25` | whole-plant management threshold (OSU, TAMU). **Not** a foliage number — none exists |
| `chilling_sensitivity_f` | — | → `null` | artichoke is cold-adapted, not chilling-sensitive |
| `germination_temp_f` | `[]` | → `[65, 82]` | WSU EM057E optimum soil temperature range |
| `weeks_indoors` | `null` | → `[6, 8]` | WSU "Weeks to Grow to Transplant Size 6-8"; NC State "seed 6-8 weeks before the T date" |
| `germination_light` / `seedling_light` / `tray_sowing` | — | **real values, not `"na"`** | unlike asparagus, artichoke has a genuine home-from-seed path — an `"na"` here would be a false claim |
| `varieties[].resistance` | — | **honest N/A** | no cultivar × disease grid exists in any extension source (see below) |
| `hardiness_zone_min` / `_max` | `null` | → `null`, with a written reason | **three T1 sources give three incompatible answers** — see below. Picking one would be preferring a source over two others with no basis |

**Two roster-wide honesty constraints that fall out of the research:**

1. **No extension source publishes a per-zone artichoke *calendar*.** Sources frame by state, by
   region, and by last-frost date — confirmed across OSU, WSU, UNR, USU, NMSU, VCE, and UC. So every
   per-zone split this dataset publishes is a **modeling act**, and `resolution_method` must say so
   rather than dressing it as sourced. **There is no zone-3 protocol anywhere in the corpus**; the
   coldest documented trial sites are central Maine (44.23°N), upstate New York, and Connecticut, so
   zones 3-4 are an extrapolation beyond the published record and the cells must say so.

   ⚠️ **Correction to an earlier draft of this document**, which said no source ties artichoke to a
   USDA zone at all. That was too strong. Two crop-specific extension bulletins **do** make zone
   claims — they simply do not agree, with each other or with the measured crown-kill temperature:

   | source | claim | implied winter minimum |
   |---|---|---|
   | UMaine Bulletin #2075 | *"hardy in USDA Plant Hardiness Zone 7 and greater"* | 0 to 10°F |
   | Cornell CALS | *"normally hardy to Zone 6 if well mulched, and occasionally Zone 5 during mild winters"* | −10 to 0°F |
   | OSU *Oregon Vegetables* + Welbaum 1994 | crown kill at **15°F / −10°C** | zone 8a-8b ground |

   The zone claims are *warmer-tolerant* than the measured crown-kill temperature allows. Leaving the
   field null and recording the conflict is the honest resolution; the **temperature thresholds**,
   which are measured and mutually consistent, do the real work in the cell ratings instead.
2. **Per-cultivar disease resistance does not exist.** The four resistance-adjacent statements are
   ungradeable and two contradict each other outright (UC IPM: annuals "more susceptible" than
   perennial Green Globe; UC ANR 7221: "All artichoke varieties are susceptible"). USU's "good
   disease resistance" for Imperial Star names no disease. `resistance` maps ship honest-N/A, and the
   unverifiable 2021 Turkish "moderately resistant" claim is **not carried**.

### B.8 Regions with no source at all — how they get authored

Three regions have a documented **absence**, which is a finding, not a gap to paper over:

- **`mid_south`** — artichoke is listed by **none** of AR/OK/TN/MO. Proof by enumeration.
- **`nevada`** — UNR omits it; its only appearances are an edible-plant-parts anatomy list (*"Flower
  bud - artichoke"*) and a demonstration-garden bed inventory. Neither is a recommendation. This is
  the same failure mode R4 caught on asparagus with `unr_fs0261`'s *"Stems - asparagus"*.
- **`utah_dixie`** — stronger than absence: USU **explicitly disclaims** its statewide dates for
  Washington County (*"Vegetable planting dates for the Washington County area are different than
  most of the rest of Utah"*), and the county material it defers to never mentions artichoke.

**Rule for these:** the cells are authored from the mechanism plus the nearest defensible analog,
`resolution_method` records the derivation honestly (never `extension_regional_guide`), and the notes
state that no regional extension service recommends the crop. Rejected outright: the only southern-
Nevada artichoke calendar on the open web is authored by a **Master Gardener volunteer** on a UNLV
campus-life page — it fails the tier rule and is not used.

### B.9 Conflicts carried, not reconciled

Recorded as `open_findings` rather than silently resolved:

| conflict | resolution |
|---|---|
| NC State publishes `T = 1 year` while **citing** VCE 438-108's *"60 to 100 days after transplanting"* | prefer **VCE** (origin document, own Virginia field trials); NC State appears to have applied a perennial figure to a transplant row |
| OSU EM 9027 (peer-reviewed): **crown pieces**, Aug-Nov + Apr-Jun vs OSU news article: **nursery starts**, May-June | prefer EM 9027 for the window; the news article is the only source for PNW perenniality and stand life, and is tiered below |
| Rutgers (50-60°F, and *"seed vernalization... is not recommended"*) vs CAES (36-40°F **on seed**) | carry both; two experiment stations, opposite recommendations |
| UC IPM ("no vector identified" for curly dwarf) vs UC ANR 7221 ("insect-transmitted") | carry both |
| TAMU EHT-065 (seed→transplant, fall) vs TAMU specialty brief (crown divisions, Texas coast, ~1 yr) | EHT-065 speaks for inland arid z8 |
| NC State's artichoke row is **byte-identical** across mountains / Piedmont / coastal plain | treat as one un-regionalized entry, not three regional judgments |
| **`ca_interior`: four UC sources, four answers** — July (MG Handbook), July (VRIC Home Garden), Dec-seed/March-out "grow as annual" (UCCE Contra Costa), May-seed/July-transplant (UCCE Tulare-Kings), and **"planting not recommended for these areas"** (VRIC *Growing Artichokes*) | the "not recommended" is from the **perennial/root-division** document, so it rules out *perennial* culture, not the crop; the annual sources agree the crop works. Rate `marginal`, annual culture, and say so |
| ANR 7221: late-Aug/Sept cutback → **summer** harvest, vs *California Agriculture* 1992: → **spring and summer** | both UC; carry both |
| `low_desert_az`: AZ1005 Maricopa **transplants Jan 15-Mar 31** vs AZ1615 Yuma **Sept-Oct, harvest May-Jun** | two faculty-reviewed calendars, genuinely different low-desert sub-climates; do not merge |

### B.9a Two source defects that change how cells get anchored

**1. The UC IPM home-garden table is a DEGRADED COPY. Do not cite it for windows.** It reproduces the
same four-district table as the Master Gardener Handbook but **drops both organ notes** and **changes
Desert Valleys from Sept to July** — a value four other UC sources contradict. A cell anchored to it
would inherit an organ-less window and a wrong month. Anchor district windows to the **Handbook Table
13.2** page instead. (UC IPM remains the correct anchor for IPM ladders and cultural tips.)

**2. Table 13.2 itself is adapted from a trade book.** It states its own lineage: *"Adapted from
Vegetable Gardening Illustrated 1994."* It is republished inside a peer-reviewed UC ANR handbook, but
it is **not original UC field research**. That is exactly the provenance class that broke asparagus,
so it is surfaced here rather than laundered: where a district window rests on Table 13.2 alone,
`resolution_method` and the cell's confidence must reflect it.

**3. The organ note exists and artichoke carries the asterisk** — the R8 trap, defused:
*"Planting dates are for seed unless noted otherwise."* + *"\*Transplants, shoots, or roots are used
for field planting."* So the California district windows are **not** seed dates.

### B.10 Citation hygiene — the specific hazards this crop carries (R3/R4)

Four load-bearing documents are **withdrawn, moved, or dead**, and each needs a resolving anchor URL:

| document | status | anchor to use |
|---|---|---|
| **VCE 438-108** (the mid-Atlantic source) | withdrawn from the live VCE site | the VTechWorks **ORIGINAL-bundle** bitstream — the DSpace default bitstream URL returns a **JPEG thumbnail**, not the PDF |
| **Rutgers FS044** | live PDF returns "Missing File" | the landing page (resolves, confirms metadata) or the 2010 Wayback copy |
| **UF/IFAS HS1289** | live EDIS page **HTTP 410 Gone** | the archival PDF, cited **with** its "Archival copy" caveat |
| **UC Davis Postharvest** artichoke sheet | live URL **403** | the Wayback capture |

Every anchoring URL is fetched and the claim sentence confirmed present before it ships (A.8).

---

## Part C — arc status and handoff (2026-07-27)

> **DISCHARGED 2026-07-28. Artichoke certified as GS #121** (canonical `ea3636e7` -> `05090b3c`).
> Part C below is preserved as the historical handoff record and is no longer a to-do list: C.2's
> two findings are applied, C.3's 140 violations are zero, and C.1's SHA guard was deliberately
> re-baselined. **What actually happened, including where this document's own predictions were
> wrong, is Part D.**

### C.1 Where the work lives, and what it has NOT touched

| artifact | state |
|---|---|
| `tools/staging/artichoke/cells.py` | 16 regions / 39 cells authored |
| `tools/staging/artichoke/sources.py` | 17 catalog additions, every URL verified resolving |
| `tools/promote_artichoke.py` | SHA-guarded, **scratch by default**; `--promote` required for canonical |
| `tools/perennial_harvest_gate.py` + test | A48, TDD RED→GREEN, wired |
| `tools/carveout_dependency_audit.py` | diagnostic |
| `crops_data_final.json` | **never written by this arc** |

**The SHA guard fired on 2026-07-27** and correctly refused to promote: canonical moved from
`34025ee3` to `d0114319` and then to `79862bc3` between two consecutive commands, with only the
`asparagus` crop changing and `LATEST.txt` still reading `34025ee3`. A concurrent session is
mid-write on the shared checkout. **Do not rebase `EXPECTED_SHA` until that session lands its work
and the state trio is updated** — re-point it deliberately, then re-run the full gauntlet against
the new base, because the base changing is exactly the condition the guard exists to catch.

### C.2 Two findings that change the build, not yet applied

**1. `survives_no_fruit` fits 7 of the 8 `unsuitable` cells better.**
The post-asparagus hardening kickoff (commit `451e1c8`) documents a five-value suitability
vocabulary with a ruled display behavior: `survives_no_fruit` renders **flagged ornamental-only** —
"the plant lives and gives you no food. Someone may still want the tree." It is already authored on
**118 cells** roster-wide.

That is precisely artichoke's tropical case. UF/IFAS's mechanism is that plants *stay vegetative and
never initiate buds* — the plant thrives, it simply gives no artichokes. And artichoke is genuinely
ornamental: UNR FS-13-05 says it "can be grown for both edible flower buds and showy garden flowers.
The open flowers are purple in color and will grow up to a diameter of 7 inches if not harvested."

So `hawaii_tropical` z10-z13, `fl_peninsula` z10/z11 and `se_gulf` z10 should be
**`survives_no_fruit`**, not `unsuitable`. That is more accurate *and* more useful: under the ruled
display behavior the grower is told "it will live and look good, you will not get artichokes,"
instead of the cell being hidden.

`ca_desert` z11 stays `unsuitable` — it is vacant ground, not an agronomic verdict.

**Blocked on a gate change:** `herbaceous_perennial_gate`'s `SUITABILITY_ENUM` is
`{perennializes, marginal, unsuitable}` — three of the roster's five values. Extending it to accept
`survives_no_fruit` (and `fruits_reliably` for symmetry) is small, well-justified, and TDD-able, but
it is a gate change and belongs with the Item 4 work rather than being slipped in here.

**2. `ca_interior` is no longer framed as annual.** Per Trevor's field experience plus the
sources: a short-lived perennial that persists several years with adequate water and is cut short by
heat, rather than a one-season crop. Rating stays `marginal` — a single heavily-irrigated success
against several neighbouring failures is the textbook `marginal` case — but the *reason* moves from
"summer heat degrades buds" to **summer water demand**, with heat as what the water buys relief
from. Texas A&M links them directly: *"In the summer, irrigation will help keep temperatures down in
the crop canopy to prevent bud opening."*

`productive_lifespan_years` stays **7**, flagged coastal-derived. UC's 5-to-10 is the only sourced
figure and it describes commercial coastal California. **No Central Valley figure is published**;
the candidates in circulation (3-5 hearsay, 3-7 from an AI summary, 3-4 OSU western Oregon, 4-7 UA
Yavapai) are either unsourced, fabricated, or the wrong region. The shortening is stated
qualitatively rather than numerically.

### C.3 Remaining work to certification

140 gate violations, all in one layer: 112 register-fill prose, 16 `region_notes` pairs, 5 display
fields (`ph.preferred_range`, `fertilizer.type/timing/frequency`, `container_notes.container_ref`),
and 7 empty consumer compounds (pests, diseases, growth_stages, notifications, weather_triggers,
failure_diagnostics, tips_by_stage). Research for all of it is distilled in the session scratchpad;
the IPM ladders and cultivars are ready to author, with per-cultivar disease resistance shipping
honest-N/A because no extension source publishes a rating.

### C.4 Corrections this arc made to its own published claims

Recorded because each was asserted with specificity before being checked:

1. *"University of Nevada Extension does not recommend artichoke"* — **false**. UNR publishes both a
   variety guide (FS-13-05) and a planting window (`unlv_mg_svn`, already T1 and cited by 67 crops).
2. *"The asparagus failure was a T2 source laundered as T1"* — **false**. All four were correctly
   tiered T1 extension documents cited for claims they do not contain. See the source-tier kickoff.
3. *"No source ties artichoke to a USDA zone"* — **too strong**. Four do; they simply disagree with
   each other and with the measured crown-kill temperature, which is why the field stays null.
4. The `se_gulf` window was derived from a self-constructed URL that 404'd; the real LSU document
   exists and tightened the window by two weeks.

---

## Part D — what certification actually did (2026-07-28)

Canonical `ea3636e7` -> **`05090b3c`**; 120 -> 121 certified, shells 8 -> 7. `gate_all` **121/121**,
`release_verify` CLEAN, verbatim scan 26/26 sources compared with **0 hard hits**.

### D.1 Both C.2 findings applied, one of them enlarged

**`survives_no_fruit` on 7 cells — and the justification got stronger than C.2 had.** C.2 rested the
case on UF/IFAS's mechanism plus UNR's "showy garden flowers … purple, up to 7 inches". **That UNR
sentence must NOT be used here**, and catching it matters: it describes a plant that *did* bud, and
the whole mechanism in the tropics is that the plant never initiates a bud at all, so it never
flowers either. Citing purple flowers for Hawaii would have been a fabricated consequence of a real
mechanism. The actual evidence is better and comes from the same publication as the mechanism —
UF/IFAS HS1289's own trial reports treated plants forming buds and *"untreated plants remained
vegetative until the end of the growing season"*, plus a description of what you do get: a rosette of
*"arching, deeply toothed, silvery, woolly green leaves that are normally 20 to 32 inches long"*.
The plants did not fail; they grew all season and never bolted.

**`ca_interior` reframed** to a short-lived perennial limited by summer water demand, per C.2.
`productive_lifespan_years` stays 7, flagged coastal-derived, and no Central Valley figure is given.

### D.2 Where this document was wrong

- **B.7 said `varieties[].resistance` ships honest-N/A — correct — but the row assumed artichoke
  would sit inside the flat variety-detail schema.** It cannot: `variety_detail_gate` goes in scope
  on `maturity_class` and then requires a per-variety `days_to_maturity`, and no anchorable
  per-cultivar DTM exists (the circulating UMaine 2021 column states no basis, matches seed-catalog
  copy, and is contradicted by UMaine's own measurements the next year — this arc laundered it once
  already). Artichoke's cultivars are therefore **deliberately outside that gate's scope**, the cost
  is stated (it is a no-op for artichoke), and the fix is named: a herbaceous-perennial variety
  archetype keyed on **chill requirement**, which is what the sources actually differentiate these
  cultivars on.
- **B.6a item 2 said artichoke's all-`growing` tropical strip is "a literally accurate depiction".**
  It is not, once those cells carry a planting window: the shipped strips carry a real `plant` token
  in the real planting month, and Florida's summer is `season_over` because UF/IFAS ends the planting
  there deliberately. Hawaii keeps an unbroken `growing` year because nothing there ends it —
  copying Florida's shape would have imported a summer die-off no source claims for Hawaii.
- **A.6 predicted A48 would be the arc's harvest floor for every non-`unsuitable` cell.** The
  `survives_no_fruit` re-rating split it: A48 now **exempts** that value while A47 still **requires**
  `plant_out` on it.

### D.3 Fields authored natively at cert (register rows 26/27)

`harvest_stop_rule` with a **new `STOP_SIGNALS` member, `bract_opening`**, and `threshold_inches`
made conditional on the signal. `harvest_ramp_weeks` is **NULL** — a first draft invented a
three-year ramp to fill the field's shape and it was retracted; no source publishes one, and it would
describe 6 of 39 cells. Three cells carry a sourced `harvest_duration_weeks`.

### D.4 Gate work, and one live defect found elsewhere

`SUITABILITY_ENUM` widened 3 -> the roster's 5. **A49** (`zone_order_gate`) and **A50**
(`harvest_duration_gate`) hard-flipped into `whole_crop_gate` — artichoke's cert was their stated
trigger. New `tools/region_prose_gate.py` (hardening item 1) **found a live contradiction on
certified asparagus on its first run**: `ca_south_coast` z11 is `marginal` in data while its region
prose says *"Frost-free zone 11 is unsuitable."* Not repaired here — it is an asparagus content call
— and pinned as a known-open expectation in that gate's test. Its roster-wide audit reports 38
findings across 17 crops, all long-certified fruit trees.

### D.5 Source discipline

The arc's own false rejection of `unlv_mg_svn` was **reversed**: it is T1, cited by 67 crops, and the
catalog had already ruled. Re-verified at source by reading the chart's **bar geometry** (its marks
have no text layer) and validating against the garlic and broccoli rows before re-anchoring, which
closed 3 anchoring gaps. `uaex_cardoon` was dropped from the catalog entirely rather than admitted
uncited at T2. All 26 cited URLs fetched; a claim-support sweep flagged 4 low-mention documents and
all 4 adjudicated — two are cited **for a documented absence**, two are drawn-bar charts read
geometrically (AZ1615's artichoke row verified verbatim as *"September-October | May-June"*).
